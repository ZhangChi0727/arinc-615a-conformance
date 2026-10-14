from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from check_experiment_design import (  # noqa: E402
    REQUIRED_BINDINGS,
    _population_sets,
    accounting_summary,
    validate_design,
)
from sync_experiment_design import (  # noqa: E402
    END,
    START,
    reconcile_text,
    render_shared_block,
    sync,
)


DESIGN = json.loads((ROOT / "configs/research/cltav_experiment_design.json").read_text(encoding="utf-8"))


def errors_for(mutator) -> list[str]:
    candidate = copy.deepcopy(DESIGN)
    mutator(candidate)
    return validate_design(ROOT, candidate)


def _run_git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


@pytest.fixture()
def isolated_snapshot_repo() -> tuple[Path, dict]:
    workspace_tmp = ROOT / "tmp"
    workspace_tmp.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="experiment-snapshot-", dir=workspace_tmp) as directory:
        root = Path(directory)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Experiment test"], cwd=root, check=True)

        base = DESIGN["identity"]["baseCommit"]
        for relative in REQUIRED_BINDINGS:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            blob = subprocess.check_output(["git", "cat-file", "blob", f"{base}:{relative}"], cwd=ROOT)
            target.write_bytes(blob)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "accepted inputs"], cwd=root, check=True)
        commit = _run_git(root, "rev-parse", "HEAD")

        schema_target = root / "configs/research/cltav_experiment_design.schema.json"
        schema_target.parent.mkdir(parents=True, exist_ok=True)
        schema_target.write_bytes((ROOT / "configs/research/cltav_experiment_design.schema.json").read_bytes())

        candidate = copy.deepcopy(DESIGN)
        candidate["identity"]["baseCommit"] = commit
        for binding in candidate["inputBindings"]:
            relative = binding["path"]
            binding["gitBlobOid"] = _run_git(root, "rev-parse", f"{commit}:{relative}")
            binding["sha256"] = hashlib.sha256((root / relative).read_bytes()).hexdigest()
        yield root, candidate


def test_repository_experiment_design_is_valid_and_reordering_is_semantic_noop() -> None:
    assert validate_design(ROOT) == []
    candidate = copy.deepcopy(DESIGN)
    candidate["inputBindings"].reverse()
    candidate["metrics"].reverse()
    candidate["scenarios"].reverse()
    candidate["dependencies"].reverse()
    assert validate_design(ROOT, candidate) == []


def test_v01_binding_roles_oid_and_sha_are_mandatory() -> None:
    assert errors_for(lambda d: d["inputBindings"].pop(0))
    assert errors_for(lambda d: d["inputBindings"][0].pop("role"))
    assert any("OID" in item or "Git blob" in item for item in errors_for(lambda d: d["inputBindings"][0].update(gitBlobOid="0" * 40)))
    assert any("SHA-256 mismatch" in item for item in errors_for(lambda d: d["inputBindings"][0].update(sha256="0" * 64)))


def test_v02_authority_consumers_use_committed_blobs_only(isolated_snapshot_repo: tuple[Path, dict]) -> None:
    root, candidate = isolated_snapshot_repo
    registry_path = root / "configs/research/cltav_interface_registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["experimentInterfaces"][0]["outputs"].append("onlyWorktree")
    registry_path.write_text(json.dumps(registry), encoding="utf-8")

    assert validate_design(root, candidate) == []
    candidate["metrics"][0]["requiredFields"].append("IF-EXP-SCENE.onlyWorktree")
    errors = validate_design(root, candidate)
    assert any("unknown interface output" in item for item in errors)


def test_v03_error_and_nonsingleton_fail_are_not_singleton_decisions() -> None:
    populations = _population_sets(DESIGN)
    assert "ATT-007" not in populations["POP-ANSWERED"]
    assert "ATT-002" not in populations["POP-SINGLETON-DECISION"]
    assert "ATT-003" in populations["POP-SINGLETON-DECISION"]
    assert errors_for(lambda d: d["syntheticWalkthroughs"][6].update(localizationDecisionIssued=True))


def test_v04_zero_answer_and_conditional_error_denominators() -> None:
    candidate = copy.deepcopy(DESIGN)
    for row in candidate["syntheticWalkthroughs"]:
        row["outcome"] = "NOT-ANSWERED"
    summary = accounting_summary(candidate)
    assert summary["answeredCoverage"] == "0/12"
    assert summary["conditionalDetectionError"] == "N/A"

    candidate = copy.deepcopy(DESIGN)
    candidate["syntheticWalkthroughs"][0]["outcome"] = "FAIL"
    assert accounting_summary(candidate)["conditionalDetectionError"] == "1/3"


def test_v05_excluded_unresolved_abstain_and_pairing_remain_visible_without_duplication() -> None:
    populations = _population_sets(DESIGN)
    summary = accounting_summary(DESIGN)
    assert len(populations["POP-ATTEMPTS"]) == 12
    assert summary["equivalentFault"] == 1
    assert summary["unresolvedFault"] == 1
    assert summary["abstain"] == 1
    assert populations["POP-PAIRED-ELIGIBLE"] == {"PAIR-01"}
    assert populations["POP-ROUNDS"] == {"ATT-001"}
    assert any("duplicate synthetic attempt" in item for item in errors_for(lambda d: d["syntheticWalkthroughs"][1].update(attemptId="ATT-001")))


def test_v06_t5_contains_a_real_interval_overlap_and_rejects_endpoint_or_unit_drift() -> None:
    row = next(row for row in DESIGN["syntheticWalkthroughs"] if row["id"] == "SYN-T5-OVERLAP")
    assert row["observationInterval"] == {"lower": 5.0, "upper": 5.2, "unit": "s"}
    assert any("interval overlap" in item for item in errors_for(lambda d: next(row for row in d["syntheticWalkthroughs"] if row["id"] == "SYN-T5-OVERLAP")["requirementInterval"].update(upper=4.9)))
    assert any("units" in item for item in errors_for(lambda d: next(row for row in d["syntheticWalkthroughs"] if row["id"] == "SYN-T5-OVERLAP")["observationInterval"].update(unit="ms")))


def test_v07_stop_priority_is_stage_sensitive() -> None:
    assert any("Stop-Empty" in item for item in errors_for(lambda d: next(row for row in d["syntheticWalkthroughs"] if row["id"] == "SYN-STOP-EMPTY").update(stage="TERMINAL")))

    def forge_budget_singleton(data: dict) -> None:
        row = next(row for row in data["syntheticWalkthroughs"] if row["id"] == "SYN-PRE-ACTION")
        row.update(finalHypotheses=["h-normal"], localizationDecisionIssued=True, singletonDecisionIssued=True)

    assert any("masquerade" in item for item in errors_for(forge_budget_singleton))


def test_v08_recovery_projects_to_preparation_once() -> None:
    summary = accounting_summary(DESIGN)
    assert summary["projectedCostTotals"]["preparation"] == 6
    assert errors_for(lambda d: d["costAccounting"]["detailToProjection"].update(recovery="retry"))
    assert any("fair-comparison" in item for item in errors_for(lambda d: d["arms"][1]["costComponents"].append("acquisition")))


def test_v09_scenario_and_acceptance_matrix_references_are_exact() -> None:
    assert DESIGN["scenarios"][4]["crsDisposition"] == "TOOL-OR-EXPERIMENT-N/A"
    assert DESIGN["scenarios"][4]["crsRefs"] == []
    assert any("unknown acceptance-case" in item for item in errors_for(lambda d: d["scenarios"][0]["acceptanceCaseRefs"].append("AC-BOGUS")))
    assert any("bound Git development authority" in item for item in errors_for(lambda d: d["scenarios"][7].update(serviceScope="UPLOAD")))
    assert errors_for(lambda d: d["acceptanceMatrixDispositions"].pop())


def test_v10_runtime_equivalence_is_not_mutation_truth() -> None:
    def conflate(data: dict) -> None:
        dep = next(row for row in data["dependencies"] if row["id"] == "DEP-EQUIV")
        dep["proposalFields"][0]["path"] = "IF-EQUIV.mutationTruth"

    assert any("must not redefine runtime IF-EQUIV" in item for item in errors_for(conflate))


def test_v11_typed_truth_visibility_rejects_algorithm_leakage() -> None:
    def leak(data: dict) -> None:
        data["arms"][0]["visibleInputs"].append({"ref": "IF-EXP-TRUTH.truthRecord", "role": "ALGORITHM-INITIAL"})

    assert any("truth leakage" in item for item in errors_for(leak))
    assert all(row["truthReference"]["visibility"] == "EVALUATOR-ONLY" for row in DESIGN["syntheticWalkthroughs"])


def test_v12_coordinated_deletion_cannot_bypass_closure() -> None:
    def delete_decision_everywhere(data: dict) -> None:
        data["pendingDecisions"] = [row for row in data["pendingDecisions"] if row["id"] != "DEC-CLOCK"]
        data["designAdmission"]["blockingDecisionIds"].remove("DEC-CLOCK")
        for dependency in data["dependencies"]:
            dependency["decisionIds"] = [item for item in dependency["decisionIds"] if item != "DEC-CLOCK"]

    def delete_metric_everywhere(data: dict) -> None:
        data["metrics"] = [row for row in data["metrics"] if row["id"] != "MET-ANSWERED-COVERAGE"]
        for family in data["comparisonFamilies"]:
            family["metricIds"] = [item for item in family["metricIds"] if item != "MET-ANSWERED-COVERAGE"]
        for dependency in data["dependencies"]:
            dependency["consumers"] = [item for item in dependency["consumers"] if item != "MET-ANSWERED-COVERAGE"]
        next(row for row in data["metrics"] if row["id"] == "MET-ABLATION-DELTA")["parentMetricIds"].remove("MET-ANSWERED-COVERAGE")

    assert errors_for(delete_decision_everywhere)
    assert any("metric set must remain complete" in item for item in errors_for(delete_metric_everywhere))
    assert any("dependencies must remain complete" in item for item in errors_for(lambda d: d["dependencies"].pop(0)))


def test_v13_invalid_nested_schema_returns_stable_diagnostics_not_exception() -> None:
    errors = errors_for(lambda d: d["syntheticWalkthroughs"][0].update(chargedCost="not-an-object"))
    assert errors
    assert all(item.startswith("schema ") for item in errors)


def test_v14_generated_bilingual_tables_reject_drift_but_ignore_order_and_line_endings(
    isolated_snapshot_repo: tuple[Path, dict],
) -> None:
    reordered = copy.deepcopy(DESIGN)
    for key in ("scenarios", "acceptanceMatrixDispositions", "metrics", "analysisPlans", "dependencies", "pendingDecisions"):
        reordered[key].reverse()
    assert render_shared_block(reordered) == render_shared_block(DESIGN)

    source = f"head\r\n{START}\r\nstale\r\n{END}\r\ntail\r\n"
    reconciled = reconcile_text(source, render_shared_block(DESIGN))
    assert "stale" not in reconciled
    assert "\r" not in reconciled

    root, candidate = isolated_snapshot_repo
    design_path = root / "configs/research/cltav_experiment_design.json"
    design_path.write_text(json.dumps(candidate), encoding="utf-8")
    spec_path = root / "docs/research/EXPERIMENT_IMPLEMENTATION_SPEC.md"
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(f"before\n{START}\nstale\n{END}\nafter\n", encoding="utf-8")
    before = spec_path.read_bytes()
    candidate["inputBindings"][0]["sha256"] = "0" * 64
    design_path.write_text(json.dumps(candidate), encoding="utf-8")
    ok, message = sync(root, write=True)
    assert not ok and "validation failed" in message
    assert spec_path.read_bytes() == before


def test_v15_primary_metrics_have_analysis_decision_and_freeze_gates() -> None:
    primary = [row for row in DESIGN["metrics"] if row["primary"]]
    assert primary
    assert all(row["analysisPlanId"] for row in primary)
    analysis = {row["id"]: row for row in DESIGN["analysisPlans"]}
    assert all(analysis[row["analysisPlanId"]]["freezeDecisionId"] == "DEC-SAMPLE" for row in primary)
    assert any("valid analysis plan" in item for item in errors_for(lambda d: next(row for row in d["metrics"] if row["primary"]).__setitem__("analysisPlanId", "AN-BOGUS")))


def test_repository_spec_is_synchronized() -> None:
    ok, message = sync(ROOT, write=False)
    assert ok, message
