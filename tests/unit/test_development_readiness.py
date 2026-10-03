import copy
import importlib.util
import json
from pathlib import Path
import hashlib
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("development_readiness", ROOT / "scripts" / "check_development_readiness.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
sys.path.insert(0, str(ROOT / "scripts"))
SYNC_SPEC = importlib.util.spec_from_file_location("sync_development_readiness", ROOT / "scripts" / "sync_development_readiness.py")
assert SYNC_SPEC and SYNC_SPEC.loader
SYNC = importlib.util.module_from_spec(SYNC_SPEC)
SYNC_SPEC.loader.exec_module(SYNC)
PACKAGE = json.loads((ROOT / "configs" / "engineering" / "cltav_development_contracts.json").read_text(encoding="utf-8"))


def errors(data):
    return MODULE.package_errors(data)


def run_main(monkeypatch, tmp_path, capsys, data):
    package = tmp_path / "package.json"
    package.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(MODULE, "PACKAGE_PATH", package)
    code = MODULE.main()
    return code, capsys.readouterr()


def test_current_candidate_is_blocked_but_valid():
    assert PACKAGE["reviewBoundary"]["readiness"] == "READINESS-BLOCKED"
    assert errors(copy.deepcopy(PACKAGE)) == []


def test_slice_identity_and_edge_rules():
    duplicate_id = copy.deepcopy(PACKAGE)
    duplicate_id["implementationSlices"].append({"id": duplicate_id["implementationSlices"][0]["id"], "scope": "different", "scopeZh": "不同", "requirementIds": ["CRS-M1-00420"]})
    assert any("repeats a slice ID" in item for item in errors(duplicate_id))

    duplicate_edge = copy.deepcopy(PACKAGE)
    duplicate_edge["implementationSlices"][0]["requirementIds"].append(duplicate_edge["implementationSlices"][0]["requirementIds"][0])
    assert any("repeats a requirement use" in item for item in errors(duplicate_edge))

    shared = copy.deepcopy(PACKAGE)
    shared["implementationSlices"].append({"id": "SLICE-SHARED", "scope": "legal shared consumer", "scopeZh": "合法共享消费者", "requirementIds": [shared["implementationSlices"][0]["requirementIds"][0]]})
    assert errors(shared) == []


def test_use_edges_must_resolve_to_m1_and_disposition():
    non_m1 = copy.deepcopy(PACKAGE)
    non_m1["implementationSlices"][0]["requirementIds"].append("CRS-M1-99999")
    assert any("non-M1" in item for item in errors(non_m1))

    required = next(row for row in PACKAGE["protocolInputDispositions"] if row["firstSliceRequired"] and row["disposition"] == "FIRST-SLICE-IMPLEMENTATION")
    downgraded = copy.deepcopy(PACKAGE)
    row = next(item for item in downgraded["protocolInputDispositions"] if item["inputRequirementId"] == required["inputRequirementId"])
    row.update(disposition="NOT-TOOL-OBLIGATION")
    row.pop("moduleId"); row.pop("recordId"); row.pop("acceptanceCaseId")
    assert any("required use has no implementation" in item for item in errors(downgraded))


def test_all_first_slice_references_are_closed_independently():
    row = next(item for item in PACKAGE["protocolInputDispositions"] if item["disposition"] == "FIRST-SLICE-IMPLEMENTATION")
    for field in ("moduleId", "recordId", "acceptanceCaseId"):
        mutated = copy.deepcopy(PACKAGE)
        target = next(item for item in mutated["protocolInputDispositions"] if item["inputRequirementId"] == row["inputRequirementId"])
        target[field] = "MISSING-REFERENCE"
        assert errors(mutated), field


def test_ready_is_stage_locked_even_with_trimmed_relations_or_evidence():
    for evidence in ([], [""], ["   "], ["README.md"]):
        mutated = copy.deepcopy(PACKAGE)
        mutated["reviewBoundary"] = {"readiness": "READY", "claims": "SPECIFICATION-ONLY", "completionEvidence": evidence}
        assert any("READY is prohibited" in item for item in errors(mutated))


def test_ready_lock_survives_actual_pruning(monkeypatch, tmp_path, capsys):
    mutated = copy.deepcopy(PACKAGE)
    removed = {row["inputRequirementId"] for row in mutated["protocolInputDispositions"] if row["firstSliceRequired"] and row["disposition"] == "DEPENDENCY-BLOCKED"}
    assert removed
    for slice_ in mutated["implementationSlices"]:
        slice_["requirementIds"] = [item for item in slice_["requirementIds"] if item not in removed]
    for row in mutated["protocolInputDispositions"]:
        if row["inputRequirementId"] in removed:
            row["firstSliceRequired"] = False
    mutated["reviewBoundary"] = {"readiness": "READY", "claims": "SPECIFICATION-ONLY", "completionEvidence": ["README.md"]}
    code, captured = run_main(monkeypatch, tmp_path, capsys, mutated)
    assert code == 1
    assert "READY is prohibited" in captured.err


def test_main_returns_exit_codes_for_candidate_and_bad_binding(monkeypatch, tmp_path, capsys):
    code, captured = run_main(monkeypatch, tmp_path, capsys, copy.deepcopy(PACKAGE))
    assert code == 0
    assert "readiness=READINESS-BLOCKED" in captured.out
    bad = copy.deepcopy(PACKAGE)
    bad["inputBindings"][0]["sha256"] = "0" * 64
    code, captured = run_main(monkeypatch, tmp_path, capsys, bad)
    assert code == 1
    assert "content identity differs" in captured.err


def test_bound_inputs_are_consumed_once_from_git_blobs_not_worktree(monkeypatch):
    bound_paths = {ROOT / item["path"] for item in PACKAGE["inputBindings"]}
    original_read_text = Path.read_text
    original_check_output = MODULE.subprocess.check_output
    reads = []

    def reject_bound_worktree_reads(path, *args, **kwargs):
        if path in bound_paths:
            raise AssertionError("bound input was consumed from the worktree")
        return original_read_text(path, *args, **kwargs)

    def count_blob_reads(command, *args, **kwargs):
        if command[:2] == ["git", "show"]:
            reads.append(command[2])
        return original_check_output(command, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", reject_bound_worktree_reads)
    monkeypatch.setattr(MODULE.subprocess, "check_output", count_blob_reads)
    assert errors(copy.deepcopy(PACKAGE)) == []
    expected = {f"HEAD:{item['path']}" for item in PACKAGE["inputBindings"]}
    assert set(reads) == expected
    assert len(reads) == len(expected)


def test_bound_git_snapshot_survives_bad_worktree_inputs(monkeypatch, tmp_path):
    """The verifier must consume committed bytes, not any worktree read API."""
    repo = tmp_path / "snapshot-repo"
    for relative in (
        "configs/requirements/arinc_615a3_m1_crs.json",
        "configs/research/cltav_interface_registry.json",
        "configs/engineering/cltav_development_contracts.schema.json",
    ):
        source = ROOT / relative
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "test"], cwd=repo, check=True)
    subprocess.run(["git", "add", "configs"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "snapshot"], cwd=repo, check=True)

    candidate = copy.deepcopy(PACKAGE)
    for binding in candidate["inputBindings"]:
        raw = subprocess.check_output(["git", "show", f"HEAD:{binding['path']}"], cwd=repo)
        binding["sha256"] = hashlib.sha256(raw).hexdigest()

    # Deliberately invalid worktree bytes after the immutable snapshot exists.
    (repo / "configs/requirements/arinc_615a3_m1_crs.json").write_text("{}", encoding="utf-8")
    (repo / "configs/research/cltav_interface_registry.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(MODULE, "ROOT", repo)
    monkeypatch.setattr(MODULE, "SCHEMA_PATH", repo / "configs/engineering/cltav_development_contracts.schema.json")
    monkeypatch.setattr(MODULE, "M1_PATH", repo / "configs/requirements/arinc_615a3_m1_crs.json")
    assert errors(candidate) == []


def test_missing_and_forged_references_report_the_target_contract():
    row = next(item for item in PACKAGE["protocolInputDispositions"] if item["disposition"] == "FIRST-SLICE-IMPLEMENTATION")
    for field, label in (("moduleId", "module"), ("recordId", "record"), ("acceptanceCaseId", "acceptance case")):
        for value in (None, "MISSING-REFERENCE"):
            mutated = copy.deepcopy(PACKAGE)
            target = next(item for item in mutated["protocolInputDispositions"] if item["inputRequirementId"] == row["inputRequirementId"])
            if value is None:
                target.pop(field)
            else:
                target[field] = value
            assert any(label in item for item in errors(mutated))


def test_legal_new_use_then_isolated_downgrade():
    candidate = copy.deepcopy(PACKAGE)
    extra = next(row for row in candidate["protocolInputDispositions"] if not row["firstSliceRequired"])
    candidate["implementationSlices"][0]["requirementIds"].append(extra["inputRequirementId"])
    extra.update(firstSliceRequired=True, disposition="FIRST-SLICE-IMPLEMENTATION", rationale="Synthetic legal first-slice extension.", moduleId="MOD-TRANSFER", recordId="PROTOCOL-EVENT", acceptanceCaseId="AC-SYN-TRANSFER")
    assert errors(candidate) == []
    extra["disposition"] = "NOT-TOOL-OBLIGATION"
    assert any("required use has no implementation" in item for item in errors(candidate))


def test_review_view_renders_every_disposition_and_bilingual_authority_fields():
    view = SYNC.render(copy.deepcopy(PACKAGE))
    assert "## All requirement dispositions" in view
    assert "## 全部需求处置" in view
    assert "## Slice membership relations" in view
    assert "## 切片成员关系" in view
    english_inputs = view.split("## Inputs\n", 1)[1].split("## Slices and dependencies", 1)[0]
    chinese_inputs = view.split("## 输入身份\n", 1)[1].split("## 切片与依赖", 1)[0]
    chinese_control = view.split("# CL-TAV 开发就绪评审视图", 1)[1].split("## 输入身份", 1)[0]
    assert f"Control: `{PACKAGE['control']['changeRequest']}`" in view
    assert f"控制：`{PACKAGE['control']['changeRequest']}`" in chinese_control
    for decision in PACKAGE["control"]["decisions"]:
        assert f"`{decision}`" in chinese_control
    for binding in PACKAGE["inputBindings"]:
        assert binding["purpose"] in english_inputs
        assert binding["purposeZh"] not in english_inputs
        assert binding["purposeZh"] in chinese_inputs
        assert binding["purpose"] not in chinese_inputs
    for row in PACKAGE["protocolInputDispositions"]:
        assert row["inputRequirementId"] in view
        assert row["rationale"] in view
        assert row["rationaleZh"] in view
    for slice_ in PACKAGE["implementationSlices"]:
        assert slice_["scope"] in view
        assert slice_["scopeZh"] in view
        for requirement_id in slice_["requirementIds"]:
            assert f"| `{slice_['id']}` | `{requirement_id}` |" in view


def test_review_view_escapes_table_rationales_without_losing_row_structure():
    candidate = copy.deepcopy(PACKAGE)
    row = candidate["protocolInputDispositions"][0]
    row["rationale"] = "English left | right\nnext line"
    row["rationaleZh"] = "中文左侧 | 右侧\n下一行"
    view = SYNC.render(candidate)
    english = view.split("## All requirement dispositions\n", 1)[1].split("# 中文版", 1)[0]
    chinese = view.split("## 全部需求处置\n", 1)[1]
    english_row = next(line for line in english.splitlines() if f"`{row['inputRequirementId']}`" in line)
    chinese_row = next(line for line in chinese.splitlines() if f"`{row['inputRequirementId']}`" in line)
    assert english_row.endswith("English left \\| right<br>next line |")
    assert chinese_row.endswith("中文左侧 \\| 右侧<br>下一行 |")
    assert sum(char == "|" and (index == 0 or english_row[index - 1] != "\\") for index, char in enumerate(english_row)) == 8
    assert sum(char == "|" and (index == 0 or chinese_row[index - 1] != "\\") for index, char in enumerate(chinese_row)) == 8


def test_review_view_detects_nonfirst_disposition_and_slice_relation_changes():
    baseline = SYNC.render(copy.deepcopy(PACKAGE))
    candidate = copy.deepcopy(PACKAGE)
    nonfirst = next(row for row in candidate["protocolInputDispositions"] if not row["firstSliceRequired"])
    nonfirst["rationale"] = "Changed non-first-slice rationale."
    nonfirst["rationaleZh"] = "已变更的非首轮理由。"
    assert SYNC.render(candidate) != baseline

    candidate = copy.deepcopy(PACKAGE)
    first_ids = candidate["implementationSlices"][0]["requirementIds"]
    moved, retained = first_ids[0], first_ids[1]
    candidate["implementationSlices"][0]["requirementIds"].remove(moved)
    candidate["implementationSlices"].append({"id": "SLICE-SECOND", "scope": "legal partition", "scopeZh": "合法分区", "requirementIds": [moved]})
    assert errors(candidate) == []
    partitioned = SYNC.render(candidate)
    candidate["implementationSlices"][0]["requirementIds"].remove(retained)
    candidate["implementationSlices"][0]["requirementIds"].append(moved)
    candidate["implementationSlices"][1]["requirementIds"] = [retained]
    assert errors(candidate) == []
    assert SYNC.render(candidate) != partitioned


def test_review_generator_refuses_invalid_authority_and_detects_stale_view(monkeypatch, tmp_path, capsys):
    package = tmp_path / "package.json"
    view = tmp_path / "review.md"
    package.write_text(json.dumps(PACKAGE), encoding="utf-8")
    view.write_text("preserve this failed-publication marker\n", encoding="utf-8")
    monkeypatch.setattr(SYNC, "PACKAGE", package)
    monkeypatch.setattr(SYNC, "VIEW", view)
    invalid = copy.deepcopy(PACKAGE)
    invalid["protocolInputDispositions"][0].pop("rationaleZh")
    package.write_text(json.dumps(invalid), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["sync_development_readiness.py", "--write"])
    assert SYNC.main() == 1
    assert view.read_text(encoding="utf-8") == "preserve this failed-publication marker\n"

    package.write_text(json.dumps(PACKAGE), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["sync_development_readiness.py", "--write"])
    assert SYNC.main() == 0
    changed = copy.deepcopy(PACKAGE)
    changed["implementationSlices"][0]["scopeZh"] = "已变更的中文范围"
    package.write_text(json.dumps(changed), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["sync_development_readiness.py", "--check"])
    assert SYNC.main() == 1
    assert "stale" in capsys.readouterr().err
