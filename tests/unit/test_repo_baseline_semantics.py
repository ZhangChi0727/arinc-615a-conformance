"""Negative regression tests for data-driven repository governance."""

from __future__ import annotations

import copy
import importlib.util
import hashlib
import json
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "check_repo_baseline", ROOT / "scripts/check_repo_baseline.py"
)
assert SPEC and SPEC.loader
baseline = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(baseline)


def source(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def status() -> dict:
    return copy.deepcopy(baseline.STATUS)


def controlled_sources() -> dict:
    return copy.deepcopy(baseline.CONTROLLED_SOURCES)


def integrated_status_errors(data: dict) -> list[str]:
    generated = baseline.sync.replace_status_block(source("README.md"), data, baseline.CONTROLLED_SOURCES)
    return baseline.governed_status_errors(data, generated)


def integrated_source_errors(register: dict, data: dict | None = None) -> list[str]:
    data = status() if data is None else data
    generated = baseline.sync.replace_status_block(source("README.md"), data, register)
    return baseline.governed_status_errors(data, generated, register)


def mapping_line(text: str, row_id: str) -> str:
    return next(line for line in text.splitlines() if line.startswith(f"| {row_id} |"))


def acknowledgement_texts() -> tuple[str, str, str, str, str, str]:
    records = baseline.STATUS["release"]["records"]
    return (
        source("docs/control/contracts/EXTERNAL_GVS_BINDING.md"),
        source("docs/control/contracts/GVS_INSTANCE_MAPPING.md"),
        source("docs/control/contracts/ARINC615A_PROFILE_BINDING_CONFIGURATION.md"),
        source(records["baselinePath"]),
        source(records["changePath"]),
        source(records["acknowledgementReviewPath"]),
    )


def ack_errors(parts: tuple[str, str, str, str, str, str]) -> list[str]:
    return baseline.third_handshake_acknowledgement_errors(*parts)


def test_mapping_rejects_missing_method_source_row() -> None:
    text = source("docs/control/contracts/GVS_INSTANCE_MAPPING.md")
    broken = text.replace("| R06 |", "| X06 |", 1)
    assert any("source row R06" in error for error in baseline.mapping_reconciliation_errors(broken))


def test_mapping_rejects_combined_case_and_procedure_identity() -> None:
    text = source("docs/control/contracts/GVS_INSTANCE_MAPPING.md")
    line = mapping_line(text, "R08")
    broken = text.replace(line, line.replace("VerificationProcedure", "VerificationCase").replace("procedure", "VC"), 1)
    assert any("R08" in error or "independent rows" in error for error in baseline.mapping_reconciliation_errors(broken))


def test_mapping_rejects_fabricated_external_locator() -> None:
    text = source("docs/control/contracts/GVS_INSTANCE_MAPPING.md")
    line = mapping_line(text, "A01")
    broken = text.replace(line, line.replace("VerificationCase", "FabricatedGenericRole"), 1)
    assert any("unknown external role locator" in error for error in baseline.mapping_reconciliation_errors(broken))


def test_mapping_rejects_relation_or_status_strengthening() -> None:
    text = source("docs/control/contracts/GVS_INSTANCE_MAPPING.md")
    source_line = mapping_line(text, "R15")
    broken_source = text.replace(source_line, source_line.replace("NOT-DETERMINED", "CANDIDATE", 1), 1)
    assert any("R15" in error for error in baseline.mapping_reconciliation_errors(broken_source))
    additional_line = mapping_line(text, "A07")
    broken_additional = text.replace(
        additional_line,
        additional_line.replace("no-direct-correspondence", "instantiates", 1).replace("NOT-DETERMINED", "CANDIDATE", 1),
        1,
    )
    assert any("A07" in error for error in baseline.mapping_reconciliation_errors(broken_additional))


def test_acceptance_check_rejects_missing_id_and_stale_reference() -> None:
    assessed = baseline.STATUS["release"]["assessedSource"]
    baseline_text = source(assessed["baselinePath"])
    cr_text = source(assessed["changePath"])
    missing = cr_text.replace("| AC-12 |", "| AX-12 |", 1)
    assert any("acceptance IDs differ" in error for error in baseline.acceptance_criteria_errors(baseline_text, missing))
    stale = baseline_text + "\nSee section " + "21 for acceptance."
    assert any("stale nonexistent" in error for error in baseline.acceptance_criteria_errors(stale, cr_text))


def test_cr_metadata_rejects_bilingual_identity_drift() -> None:
    text = source(baseline.STATUS["release"]["assessedSource"]["changePath"])
    english, chinese = text.split(baseline.ZH_MARKER, 1)
    broken = english + baseline.ZH_MARKER + chinese.replace(baseline.METHOD_DEFINITION_COMMIT, "0" * 40, 1)
    assert any("Chinese CR metadata differs for method commit" in error for error in baseline.cr_bilingual_metadata_errors(broken))


def test_observation_result_rejects_result_as_observation() -> None:
    pbc = source("docs/control/contracts/ARINC615A_PROFILE_BINDING_CONFIGURATION.md")
    handoff = source(baseline.STATUS["release"]["records"]["migrationReviewPath"])
    errors = baseline.observation_result_errors(pbc + "\nA verdict/result is an observation.\n", handoff)
    assert any("incorrectly defines" in error for error in errors)


def test_evidence_chain_rejects_missing_control_refs() -> None:
    architecture = source("docs/control/contracts/ARCHITECTURE.md")
    osr = source("docs/control/contracts/OBJECTIVE_SATISFACTION_RECORD.md")
    cei = source("docs/control/contracts/COMPLIANCE_EVIDENCE_INDEX.md")
    manifest = source("docs/engineering/design/EVIDENCE_MANIFEST.md")
    broken_osr = osr.replace("supportingEvidenceItems", "uncontrolledItems", 1)
    assert any("supportingEvidenceItems" in error for error in baseline.evidence_chain_errors(architecture, broken_osr, cei, manifest))
    broken_cei = cei.replace("statusDecisionRef", "localStatusSource", 1)
    assert any("statusDecisionRef" in error for error in baseline.evidence_chain_errors(architecture, osr, broken_cei, manifest))


def test_acknowledgement_rejects_swapped_method_identities() -> None:
    parts = list(acknowledgement_texts())
    definition = baseline.METHOD_DEFINITION_COMMIT
    disposition = baseline.METHOD_DISPOSITION_COMMIT
    parts[0] = parts[0].replace(definition, "X" * 40).replace(disposition, definition).replace("X" * 40, disposition)
    errors = ack_errors(tuple(parts))
    assert any("MethodDefinitionCommit identity differs" in error for error in errors)
    assert any("MethodCompatibilityDispositionCommit identity differs" in error for error in errors)


def test_acknowledgement_rejects_assessed_and_acknowledgement_release_swap() -> None:
    parts = list(acknowledgement_texts())
    assessed = baseline.ARINC_V43_RELEASE_COMMIT
    acknowledgement = baseline.STATUS["release"]["commit"]
    parts[3] = parts[3].replace(assessed, acknowledgement)
    assert any("baseline is missing controlled identity" in error for error in ack_errors(tuple(parts)))


def test_acknowledgement_rejects_missing_qualification() -> None:
    parts = list(acknowledgement_texts())
    qualification = sorted(baseline.ACK_QUALIFICATION_IDS)[-1]
    parts[4] = parts[4].replace(f"| {qualification} |", "| Q-X |", 1)
    assert any("qualification IDs differ" in error for error in ack_errors(tuple(parts)))


def test_acknowledgement_rejects_evaluation_or_configuration_promotion() -> None:
    parts = list(acknowledgement_texts())
    promoted_evaluation = next(value for value in baseline.sync.ALLOWED_EVALUATION if value != baseline.EVALUATION_STATUS)
    parts[1] = parts[1].replace(baseline.EVALUATION_STATUS, promoted_evaluation, 1)
    assert any("Instance evaluation differs" in error for error in ack_errors(tuple(parts)))
    parts = list(acknowledgement_texts())
    promoted_configuration = next(value for value in baseline.sync.ALLOWED_CONFIGURATION if value != baseline.CONFIGURATION_STATUS)
    parts[2] = parts[2].replace(baseline.CONFIGURATION_STATUS, promoted_configuration, 1)
    assert any("Project Configuration differs" in error for error in ack_errors(tuple(parts)))


def test_acknowledgement_rejects_mutable_or_wrong_commit_locator() -> None:
    parts = list(acknowledgement_texts())
    parts[0] = parts[0].replace(f"/blob/{baseline.METHOD_DEFINITION_COMMIT}/", "/blob/" + "main/", 1)
    assert any("wrong or mutable" in error for error in ack_errors(tuple(parts)))
    parts = list(acknowledgement_texts())
    parts[0] = parts[0].replace(
        f"/blob/{baseline.METHOD_DEFINITION_COMMIT}/docs/02_verification_framework/generic_verification_suite_core.md",
        f"/blob/{baseline.METHOD_DISPOSITION_COMMIT}/docs/02_verification_framework/generic_verification_suite_core.md",
        1,
    )
    assert any("wrong or mutable" in error for error in ack_errors(tuple(parts)))


def test_mapping_review_rejects_wrong_full_disposition_identity() -> None:
    text = source("docs/control/contracts/GVS_INSTANCE_MAPPING.md")
    wrong = baseline.METHOD_DISPOSITION_COMMIT[:7] + "0" * 33
    english = text.replace(
        f"method disposition `{baseline.METHOD_DISPOSITION_COMMIT}`;",
        f"method disposition `{wrong}`;",
        1,
    )
    assert any("English mapping row R01" in error for error in baseline.mapping_reconciliation_errors(english))
    boundary, chinese = text.split(baseline.ZH_MARKER, 1)
    chinese = chinese.replace(
        f"方法处置 `{baseline.METHOD_DISPOSITION_COMMIT}`；",
        f"方法处置 `{wrong}`；",
        1,
    )
    broken = boundary + baseline.ZH_MARKER + chinese
    assert any("Chinese mapping row R01" in error for error in baseline.mapping_reconciliation_errors(broken))


def test_acknowledgement_rejects_literal_markdown_damage() -> None:
    parts = list(acknowledgement_texts())
    parts[3] = parts[3].replace("## Controlled content\n", "## Controlled content`n- ", 1)
    assert any("Markdown line-break damage" in error for error in ack_errors(tuple(parts)))


def test_readme_drift_is_detected() -> None:
    data = status()
    current = source("README.md")
    broken = current.replace(data["release"]["currentBaselineId"], "obsolete-release", 1)
    assert baseline.sync.replace_status_block(broken, data) != broken


def test_controlled_source_register_and_generated_readme_are_valid() -> None:
    assert baseline.governed_status_errors(
        status(), source("README.md"), controlled_sources()
    ) == []


def test_readme_renders_network_display_groups() -> None:
    readme = source("README.md")
    assert "`ARINC-664-2`" in readme
    assert "`ARINC-664-3`" in readme
    assert "`ARINC-665-5`" in readme
    assert "BOUNDED-ACTIVE" in readme
    assert "`ARINC-664-7`" in readme
    assert "CONDITIONAL-DEPLOYMENT" in readme
    assert "M2 package" in readme


def test_new_display_group_appears_without_python_change() -> None:
    register = controlled_sources()
    extra = copy.deepcopy(next(item for item in register["sources"] if item.get("displayGroup")))
    extra["id"] = "FIXTURE-DISPLAY-SOURCE"
    extra["displayGroup"] = "FIXTURE-GROUP"
    register["sources"].append(extra)
    generated = baseline.sync.replace_status_block(source("README.md"), status(), register)
    assert "`FIXTURE-DISPLAY-SOURCE`" in generated
    assert "FIXTURE-GROUP" in generated


def test_non_authority_source_without_display_group_is_rejected() -> None:
    register = controlled_sources()
    item = next(row for row in register["sources"] if row.get("role") != "CURRENT-PROTOCOL-AUTHORITY")
    item.pop("displayGroup", None)
    assert any("displayGroup" in error for error in integrated_source_errors(register))


def test_source_rejects_non_615a3_current_authority() -> None:
    register = controlled_sources()
    register["currentProtocolAuthorityId"] = "ARINC-615A-4"
    assert any(
        "single current protocol authority" in error
        for error in baseline.controlled_source_errors(status(), register)
    )


def test_source_rejects_each_615a3_identity_mutation() -> None:
    mutations = {
        "edition": "615A-4",
        "pageCount": 175,
        "byteCount": 1875920,
        "sha256": "0" * 64,
    }
    for field, value in mutations.items():
        register = controlled_sources()
        register["sources"][0][field] = value
        assert any("ARINC-615A-3" in error for error in integrated_source_errors(register)), field


def test_source_identity_cannot_be_repaired_with_a_self_hash() -> None:
    register = controlled_sources()
    register["sources"][0]["pageCount"] = 175
    register["sources"][0]["identitySeal"] = hashlib.sha256(
        b"attacker-controlled replacement seal"
    ).hexdigest()
    assert any("independent acquisition record" in error for error in integrated_source_errors(register))


def test_source_rejects_wire_version_as_edition() -> None:
    register = controlled_sources()
    register["sources"][0]["edition"] = register["sources"][0]["wireVersion"]
    assert any("edition" in error or "wire version" in error for error in integrated_source_errors(register))


def test_source_rejects_unbounded_665_equivalence() -> None:
    register = controlled_sources()
    register["sources"][1]["equivalentReplacementFor"] = ["ARINC-665-3"]
    assert any("applicability/equivalence" in error for error in integrated_source_errors(register))


def test_source_rejects_integrity_promotion_while_645_open() -> None:
    register = controlled_sources()
    register["capabilities"][-1]["status"] = "ESTABLISHED"
    assert any("cannot be established" in error for error in integrated_source_errors(register))


def test_source_rejects_prefilled_615a4_migration_target() -> None:
    register = controlled_sources()
    register["futureSourceMigration"]["target"] = "ARINC-615A-4"
    assert any("idle future source migration" in error for error in integrated_source_errors(register))


def test_source_rejects_platform_selection_without_gate() -> None:
    register = controlled_sources()
    register["technicalDirection"]["executionPlatform"]["selected"] = "TTCN-3"
    assert any("execution platform" in error for error in integrated_source_errors(register))


def test_source_rejects_incomplete_reuse_levels() -> None:
    register = controlled_sources()
    del register["technicalDirection"]["openSourceReuse"]["L3"]
    assert any("L1/L2/L3" in error for error in integrated_source_errors(register))


def test_source_rejects_unsafe_or_untracked_frozen_history_paths() -> None:
    for invalid in ("/etc/passwd", "../../README.md", "README.md"):
        register = controlled_sources()
        register["historicalAssumptions"][0]["frozenRecords"][0]["path"] = invalid
        assert integrated_source_errors(register), invalid


def init_git_fixture(root: Path, relative: Path, payload: bytes) -> None:
    target = root / relative
    target.parent.mkdir(parents=True)
    target.write_bytes(payload)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "core.autocrlf", "false"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
    subprocess.run(["git", "add", relative.as_posix()], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)


def test_frozen_history_uses_head_blob_not_checkout_newlines(tmp_path: Path) -> None:
    record_path = Path("artifacts/reports/current/frozen-history.md")
    target = tmp_path / record_path
    canonical = b"line one\nline two\n"
    init_git_fixture(tmp_path, record_path, canonical)
    record = [{
        "path": record_path.as_posix(),
        "byteCount": len(canonical),
        "sha256": hashlib.sha256(canonical).hexdigest(),
    }]
    target.write_bytes(b"line one\r\nline two\r\n")
    assert baseline.frozen_record_errors(record, tmp_path, {record_path.as_posix()}) == []


def test_frozen_history_rejects_committed_crlf_blob(tmp_path: Path) -> None:
    record_path = Path("artifacts/reports/current/frozen-history.md")
    canonical = b"line one\nline two\n"
    init_git_fixture(tmp_path, record_path, canonical)
    target = tmp_path / record_path
    target.write_bytes(b"line one\r\nline two\r\n")
    subprocess.run(["git", "add", record_path.as_posix()], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "crlf blob"], cwd=tmp_path, check=True)
    record = [{
        "path": record_path.as_posix(),
        "byteCount": len(canonical),
        "sha256": hashlib.sha256(canonical).hexdigest(),
    }]
    errors = baseline.frozen_record_errors(record, tmp_path, {record_path.as_posix()})
    assert any("committed Git blob" in error for error in errors)


def test_source_rejects_symbolic_link_frozen_history(tmp_path: Path) -> None:
    real = tmp_path / "real.md"
    link_path = Path("artifacts/reports/current/link.md")
    link = tmp_path / link_path
    link.parent.mkdir(parents=True)
    real.write_text("history\n", encoding="utf-8")
    try:
        link.symlink_to(real)
    except OSError:
        pytest.skip("symbolic-link creation is unavailable on this host")
    register = controlled_sources()
    register["historicalAssumptions"][0]["frozenRecords"][0]["path"] = link_path.as_posix()
    assert any("symbolic link" in error for error in baseline.controlled_source_errors(
        status(), register, root=tmp_path, tracked_paths={link_path.as_posix()}
    ))


def test_source_rejects_proprietary_and_extraction_artifacts() -> None:
    changed = {
        "docs/source.pdf", "local-references/private.txt",
        "tests/vectors/standard_extract.txt", "tmp/change.patch", "tmp/review.diff",
    }
    errors = baseline.prohibited_source_artifact_errors(changed)
    assert len(errors) == len(changed)


def test_source_rejects_readme_register_drift() -> None:
    register = controlled_sources()
    register["sources"][0]["wireVersion"] = "ZZ"
    errors = baseline.governed_status_errors(status(), source("README.md"), register)
    assert any("README governed block differs" in error for error in errors)


def test_status_rejects_bypassing_m1_gate() -> None:
    data = status()
    data["development"]["currentStop"] = {
        "id": "PROJECT-CONFIGURATION-GATE",
        "statusPath": "claimsBoundary.projectConfigurationStatus",
        "objective": "skip",
        "objectiveZh": "skip",
    }
    assert any("current stop" in error or "statusPath" in error for error in integrated_status_errors(data))


def test_protected_states_reject_premature_promotion() -> None:
    mutations = (
        ("claimsBoundary", "projectConfigurationStatus", "ESTABLISHED"),
        ("claimsBoundary", "instanceEvaluation", "INSTANCE-EXERCISED"),
        ("claimsBoundary", "rq8", "CLOSED"),
        ("claimsBoundary", "protocolConformanceEstablished", True),
        ("claimsBoundary", "certificationReady", True),
        ("claimsBoundary", "authorityAccepted", True),
    )
    for section, key, value in mutations:
        data = status()
        data[section][key] = value
        errors = integrated_source_errors(controlled_sources(), data)
        assert any("protected state changed" in error for error in errors), key


def test_source_register_rejects_duplicate_ids() -> None:
    for collection in ("sources", "openDependencies", "historicalAssumptions", "roadmap"):
        register = controlled_sources()
        register[collection].append(copy.deepcopy(register[collection][0]))
        assert any(f"{collection} contains duplicate id" in error for error in integrated_source_errors(register)), collection


def test_active_controls_reject_every_historical_alias_form(tmp_path: Path) -> None:
    register = controlled_sources()
    tracked: set[str] = set()
    for raw in register["activeControlSurfacePaths"]:
        target = tmp_path / raw
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("Controlled surface.\n", encoding="utf-8")
        tracked.add(raw)
    target = tmp_path / register["activeControlSurfacePaths"][0]
    prohibited = (
        "615A-4 是唯一活动协议权威。\n",
        "Historical 615A-4 wording has current technical authority.\n",
        "[ARINC 615A-4](https://example.com/source) is the current protocol authority.\n",
        "ARINC 615A-4 is the\ncurrent protocol authority.\n",
        "ARINC-615A-4 is not the current protocol authority.\n",
    )
    for text in prohibited:
        target.write_text(text, encoding="utf-8")
        errors = baseline._active_authority_text_errors(register, tmp_path, tracked)
        assert any("names historical source" in error for error in errors), text
    target.write_text(
        "Historical source assumptions are non-authoritative and are governed by "
        "the controlled source register and change record.\n",
        encoding="utf-8",
    )
    assert baseline._active_authority_text_errors(register, tmp_path, tracked) == []


def test_historical_aliases_must_be_nonempty_unique_and_include_id() -> None:
    tracked = set(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines())
    cases = (
        ([], "non-empty textAliases"),
        (["ARINC-615A-4", "   ", "ARINC 615A-4", "615A-4"], "blank textAliases"),
        (["ARINC-615A-4", "arinc-615a-4", "ARINC 615A-4", "615A-4"], "duplicate textAliases"),
        (["ARINC 615A-4", "615A-4"], "arinc-615a-4"),
        (["ARINC-615A-4", "615A-4"], "arinc 615a-4"),
        (["ARINC-615A-4", "ARINC 615A-4"], "615a-4"),
    )
    for aliases, expected in cases:
        register = controlled_sources()
        register["historicalAssumptions"][0]["textAliases"] = aliases
        errors = baseline._active_authority_text_errors(register, ROOT, tracked)
        assert any(expected in error for error in errors), aliases


def test_historical_inventory_and_canonical_id_are_required() -> None:
    tracked = set(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines())
    for history, expected in (
        (None, "non-empty list"),
        ([], "non-empty list"),
        ([{"id": "INVALID", "textAliases": ["INVALID"]}], "invalid canonical id"),
    ):
        register = controlled_sources()
        if history is None:
            del register["historicalAssumptions"]
        else:
            register["historicalAssumptions"] = history
        errors = baseline._active_authority_text_errors(register, ROOT, tracked)
        assert any(expected in error for error in errors), history


def test_historical_alias_inventory_may_be_extended() -> None:
    register = controlled_sources()
    register["historicalAssumptions"][0]["textAliases"].append("legacy edition alias")
    assert integrated_source_errors(register) == []


def test_pruned_history_or_aliases_fail_closed() -> None:
    for mutate in (
        lambda register: register.update(historicalAssumptions=[]),
        lambda register: register["historicalAssumptions"][0].update(textAliases=["ARINC-615A-4"]),
    ):
        register = controlled_sources()
        mutate(register)
        generated = baseline.sync.replace_status_block(source("README.md"), status(), register)
        assert baseline.governed_status_errors(status(), generated, register)


def test_pruned_aliases_still_scan_required_designation(tmp_path: Path) -> None:
    register = controlled_sources()
    register["historicalAssumptions"][0]["textAliases"] = ["ARINC-615A-4"]
    tracked: set[str] = set()
    for raw in register["activeControlSurfacePaths"]:
        target = tmp_path / raw
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("Controlled surface.\n", encoding="utf-8")
        tracked.add(raw)
    (tmp_path / register["activeControlSurfacePaths"][0]).write_text(
        "615A-4 是唯一活动协议权威。\n", encoding="utf-8",
    )
    errors = baseline._active_authority_text_errors(register, tmp_path, tracked)
    assert any("lacks required forms" in error for error in errors)
    assert any("names historical source" in error for error in errors)


def test_required_aliases_are_scanned_across_all_active_surfaces(tmp_path: Path) -> None:
    register = controlled_sources()
    aliases = register["historicalAssumptions"][0]["textAliases"]
    tracked: set[str] = set()
    for index, raw in enumerate(register["activeControlSurfacePaths"]):
        target = tmp_path / raw
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"Controlled reference: {aliases[index % len(aliases)]}\n", encoding="utf-8")
        tracked.add(raw)
    errors = baseline._active_authority_text_errors(register, tmp_path, tracked)
    for raw in register["activeControlSurfacePaths"]:
        assert any(raw in error for error in errors), raw


def test_named_history_remains_allowed_outside_active_surfaces() -> None:
    register = controlled_sources()
    tracked = set(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines())
    history = register["historicalAssumptions"][0]
    aliases = history["textAliases"]
    assert any(alias in source("docs/control/changes/CR-2026-006.md") for alias in aliases)
    assert any(
        any(alias in source(record["path"]) for alias in aliases)
        for record in history["frozenRecords"]
    )
    assert baseline._active_authority_text_errors(register, ROOT, tracked) == []


def test_active_control_surfaces_cannot_be_empty_duplicate_or_incomplete() -> None:
    tracked = set(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines())
    for surfaces in (
        [],
        ["docs/research/RESEARCH_CONTROL.md"] * 2,
        ["docs/research/RESEARCH_CONTROL.md"],
    ):
        register = controlled_sources()
        register["activeControlSurfacePaths"] = surfaces
        assert baseline._active_authority_text_errors(register, ROOT, tracked)


def test_active_control_surfaces_reject_unsafe_and_untracked_paths() -> None:
    tracked = set(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines())
    for invalid in ("/etc/passwd", "../../README.md", "docs/research/not-tracked.md"):
        register = controlled_sources()
        register["activeControlSurfacePaths"][0] = invalid
        assert baseline._active_authority_text_errors(register, ROOT, tracked), invalid


def test_roadmap_accepts_m1_transition_without_python_change() -> None:
    register = controlled_sources()
    roadmap = register["roadmap"]
    for index, row in enumerate(roadmap):
        if index == 0:
            row["status"] = "COMPLETED-EXTERNALLY-VERIFIED"
        elif index == 1:
            row["status"] = "DISPOSITION-ADOPT"
        elif index == 2:
            row["status"] = "NEXT-BLOCKED-BY-FINAL-GATE"
        else:
            row["status"] = "BLOCKED-BY-PREDECESSOR"
    register["lifecycle"]["currentStageId"] = roadmap[1]["id"]
    register["lifecycle"]["nextStageId"] = roadmap[2]["id"]
    data = status()
    gates = data["development"]["gates"]
    for index, row in enumerate(roadmap):
        if index == 0:
            gates[row["gateId"]] = "COMPLETED-EXTERNALLY-VERIFIED"
        elif index == 1:
            gates[row["gateId"]] = "EXTERNAL-VERIFICATION-REQUIRED"
        elif index == 2:
            gates[row["gateId"]] = "NOT YET ESTABLISHED"
        else:
            gates[row["gateId"]] = "BLOCKED"
    next_stage = roadmap[2]
    data["development"]["currentStop"]["id"] = next_stage["gateId"]
    data["development"]["currentStop"]["statusPath"] = f"development.gates.{next_stage['gateId']}"
    assert integrated_source_errors(register, data) == []


def test_serial_roadmap_rejects_bypasses() -> None:
    mutations = (
        lambda roadmap: roadmap[3].update(dependsOn=[]),
        lambda roadmap: roadmap[3].update(dependsOn=[roadmap[1]["id"]]),
        lambda roadmap: roadmap[3].update(status="READY"),
        lambda roadmap: roadmap[3].update(status="COMPLETED-EXTERNALLY-VERIFIED"),
        lambda roadmap: roadmap[3].update(gateId=roadmap[2]["gateId"]),
    )
    for mutate in mutations:
        register = controlled_sources()
        mutate(register["roadmap"])
        assert integrated_source_errors(register)


def test_development_gates_must_match_roadmap() -> None:
    for mutate in (
        lambda gates: gates.pop(next(iter(gates))),
        lambda gates: gates.update({"UNREGISTERED-GATE": "BLOCKED"}),
    ):
        data = status()
        mutate(data["development"]["gates"])
        assert any("development.gates" in error for error in integrated_source_errors(controlled_sources(), data))


def test_gate_values_must_match_stage_position() -> None:
    register = controlled_sources()
    current_gate = next(
        row["gateId"] for row in register["roadmap"]
        if row["id"] == register["lifecycle"]["currentStageId"]
    )
    cases = (
        ("SCOPE-EXPANSION-GATE", "ESTABLISHED"),
        (current_gate, "COMPLETED-EXTERNALLY-VERIFIED"),
    )
    for gate_id, value in cases:
        data = status()
        data["development"]["gates"][gate_id] = value
        assert any(f"roadmap gate {gate_id} status" in error for error in integrated_source_errors(controlled_sources(), data))


def test_completed_stage_gate_must_be_closed() -> None:
    register = controlled_sources()
    data = status()
    completed_gate = register["roadmap"][0]["gateId"]
    data["development"]["gates"][completed_gate] = "BLOCKED"
    errors = integrated_source_errors(register, data)
    assert any("COMPLETED-EXTERNALLY-VERIFIED" in error for error in errors)


def test_readme_rejects_stale_release_candidate_wording() -> None:
    readme = source("README.md")
    broken = readme.replace("| Current release |", "| Current release | Draft candidate —", 1)
    assert any("Draft/candidate" in error for error in baseline.overview_semantic_errors(broken))


def test_pull_request_requires_readme_and_status() -> None:
    assert baseline.pr_required_file_errors(status(), {"project-status.json"}) == ["pull request must update README.md"]
    assert baseline.pr_required_file_errors(status(), {"README.md"}) == ["pull request must update project-status.json"]


def test_temporary_control_is_rejected_after_retirement() -> None:
    data = status()
    data["temporaryControls"] = [{
        "id": "temporary-test", "temporary": True, "status": "ACTIVE",
        "owner": "test", "introducedBy": "test",
        "retireWhen": {"path": "release.thirdHandshake", "equals": data["release"]["thirdHandshake"]},
    }]
    assert any("retirement condition is fulfilled" in error for error in baseline.sync.temporary_control_errors(data))


def test_status_rejects_duplicate_current_stop_status() -> None:
    data = status()
    data["development"]["currentStop"]["status"] = "ESTABLISHED"
    assert any("duplicates its authoritative statusPath" in error for error in integrated_status_errors(data))


def test_status_rejects_invalid_authoritative_handshake() -> None:
    data = status()
    data["release"]["thirdHandshake"] = "UNREVIEWED"
    assert any("invalid third-handshake" in error for error in integrated_status_errors(data))


def test_status_rejects_duplicate_cross_repository_handshake() -> None:
    data = status()
    data["crossRepository"]["methodology"]["thirdHandshake"] = "PENDING"
    assert any("duplicates release.thirdHandshake" in error for error in integrated_status_errors(data))


def test_status_rejects_unsubstantiated_protocol_conformance() -> None:
    data = status()
    data["claimsBoundary"]["protocolConformanceEstablished"] = True
    assert any("protocolConformanceEstablished requires an activation record" in error for error in integrated_status_errors(data))


def test_status_rejects_unsubstantiated_certification_readiness() -> None:
    data = status()
    data["claimsBoundary"]["certificationReady"] = True
    assert any("certificationReady requires an activation record" in error for error in integrated_status_errors(data))


def test_status_rejects_unsubstantiated_authority_acceptance() -> None:
    data = status()
    data["claimsBoundary"]["authorityAccepted"] = True
    assert any("authorityAccepted requires an activation record" in error for error in integrated_status_errors(data))


def activated_status(decision_path: str, evidence_ref: str) -> dict:
    data = status()
    claim = "protocolConformanceEstablished"
    data["claimsBoundary"][claim] = True
    data["claimsBoundary"]["activationRecords"][claim] = {
        "decisionPath": decision_path,
        "evidenceRefs": [evidence_ref],
    }
    return data


def test_claim_activation_rejects_absolute_and_traversal_paths() -> None:
    for invalid in ("/etc/passwd", "../../README.md"):
        errors = integrated_status_errors(activated_status(invalid, invalid))
        assert any("repository-relative" in error for error in errors), invalid


def test_claim_activation_rejects_status_surfaces_and_control_prose() -> None:
    cases = (
        ("README.md", "README.md"),
        ("project-status.json", "project-status.json"),
        ("docs/control/contracts/PROJECT_CONTROL.md", "README.md"),
    )
    for decision, evidence in cases:
        errors = integrated_status_errors(activated_status(decision, evidence))
        assert any("permitted controlled location" in error for error in errors), decision


def test_claim_activation_rejects_decision_without_matching_semantics(tmp_path: Path) -> None:
    decision = tmp_path / "docs/control/decisions/unrelated.md"
    evidence = tmp_path / "artifacts/evidence/run.json"
    decision.parent.mkdir(parents=True)
    evidence.parent.mkdir(parents=True)
    decision.write_text(
        "Claim: certificationReady\nDecision status: APPROVED\nDecision version: DEC-1\n",
        encoding="utf-8",
    )
    evidence.write_text("{}\n", encoding="utf-8")
    data = activated_status(decision.relative_to(tmp_path).as_posix(), evidence.relative_to(tmp_path).as_posix())
    tracked = {decision.relative_to(tmp_path).as_posix(), evidence.relative_to(tmp_path).as_posix()}
    errors = baseline.sync.activation_record_errors(data, tmp_path, tracked)
    assert any("does not identify the activated claim" in error for error in errors)


def test_claim_activation_accepts_controlled_tracked_decision_and_evidence(tmp_path: Path) -> None:
    decision = tmp_path / "docs/control/gates/protocol-conformance.md"
    evidence = tmp_path / "artifacts/evidence/verification-result.json"
    decision.parent.mkdir(parents=True)
    evidence.parent.mkdir(parents=True)
    decision.write_text(
        "Claim: protocolConformanceEstablished\n"
        "Decision status: APPROVED\n"
        "Decision identity: DEC-2026-001@0123456789abcdef\n",
        encoding="utf-8",
    )
    evidence.write_text('{"result": "PASS"}\n', encoding="utf-8")
    data = activated_status(decision.relative_to(tmp_path).as_posix(), evidence.relative_to(tmp_path).as_posix())
    tracked = {decision.relative_to(tmp_path).as_posix(), evidence.relative_to(tmp_path).as_posix()}
    assert baseline.sync.activation_record_errors(data, tmp_path, tracked) == []


def test_historical_reader_report_path_must_resolve() -> None:
    data = status()
    data["release"]["records"]["historicalReaderReportPath"] = "artifacts/reports/archive/missing.md"
    assert any("historicalReaderReportPath" in error for error in baseline.sync.status_errors(data, ROOT))


def test_iar_template_rejects_reader_report_handoff() -> None:
    text = source("docs/engineering/increments/IAR_TEMPLATE.md")
    broken = text + "\n## Reader-report " + "handoff\n"
    assert baseline.reader_handoff_text_errors(broken, "IAR_TEMPLATE.md")


def test_research_ownership_rejects_generic_core_capture() -> None:
    text = source("docs/research/RESEARCH_CONTROL.md")
    broken = text.replace("may not reverse-define the Generic Core", "may redefine the Generic Core", 1)
    assert any("reverse-define" in error for error in baseline.research_ownership_errors(broken))


def test_lifecycle_literals_are_rejected_in_governance_code() -> None:
    data = status()
    tags = {data["release"]["tag"], data["release"]["assessedSource"]["tag"]}
    sha = data["release"]["commit"]
    tag = data["release"]["tag"]
    numbered_pr = "PR " + "#" + "999"
    mutable = "origin/" + "main"
    errors = baseline.lifecycle_literal_text_errors(
        f'CURRENT_COMMIT = "{sha}"\nCURRENT_TAG = "{tag}"\n# {numbered_pr}\nREF = "{mutable}"',
        "negative.py", tags,
    )
    assert len(errors) == 4


def test_dynamic_script_discovery_rejects_each_lifecycle_escape(tmp_path: Path) -> None:
    data = status()
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    candidate = scripts / "new_operation.py"
    numbered_pr = "PR " + "#" + "999"
    mutable = "origin/" + "main"
    machine_paths = (
        "E:" + "\\" + "Project\\private",
        "D:" + "\\" + "Work\\private",
        "C:" + "\\" + "temp\\private",
        "/Users/" + "alice/private",
        "/home/" + "alice/private",
        "file:" + "///tmp/private",
    )
    cases = (
        f'VALUE = "{data["release"]["commit"]}"',
        f'VALUE = "{numbered_pr}"',
        f'VALUE = "{data["release"]["tag"]}"',
        f'VALUE = "{mutable}"',
        *(f'VALUE = r"{machine}"' for machine in machine_paths),
    )
    for content in cases:
        candidate.write_text(content, encoding="utf-8")
        assert baseline.lifecycle_literal_errors(data, tmp_path), content


def test_status_rejects_method_identity_conflation() -> None:
    data = status()
    data["methodInputs"]["compatibilityDisposition"]["commit"] = data["methodInputs"]["methodDefinition"]["commit"]
    assert any("conflated" in error for error in baseline.sync.status_errors(data, ROOT))


def test_historical_methodology_math_identity_is_preserved() -> None:
    identity = baseline.load_method_math_identity()
    freeze = identity["historicalFreeze"]
    text = baseline.git_show_file(freeze["commit"], identity["reportPath"])
    assert text is not None
    count, digest = baseline.display_math_fingerprint(text)
    assert count == freeze["displayMathBlocks"]
    assert digest == freeze["displayMathSha256"]
    assert identity["successor"]["independentMathematicalApproval"] is False
    assert identity["successor"]["independentReviewApproval"] is False
    assert identity["successor"]["historicalMathCheckDoesNotProveSuccessorMath"] is True


def test_method_report_frozen_history_must_pin_freeze_commit() -> None:
    register = controlled_sources()
    records = register["historicalAssumptions"][0]["frozenRecords"]
    method = next(row for row in records if row["path"].endswith("RR-2026-001_test_analysis_conformance_methodology.md"))
    assert method["commit"] == baseline.load_method_math_identity()["historicalFreeze"]["commit"]
    tracked = set(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines())
    assert baseline.frozen_record_errors(records, ROOT, tracked) == []
    method.pop("commit")
    errors = baseline.frozen_record_errors(records, ROOT, tracked)
    assert any("historical freeze commit" in error for error in errors)


def test_protocol_source_audit_rejects_batch_rename_and_id_drift() -> None:
    audit = json.loads(source("configs/research/cltav_protocol_source_audit.json"))
    crs = json.loads(source("configs/requirements/arinc_615a3_m1_crs.json"))
    assert baseline.protocol_source_audit_errors(audit, crs) == []
    flipped = copy.deepcopy(audit)
    flipped["notBatchStatusRename"] = False
    flipped["status"] = "READY-TO-GENERATE-REQUIREMENTS"
    flipped["requirementGenerationAllowed"] = True
    errors = baseline.protocol_source_audit_errors(flipped, crs)
    assert any("batch status rename" in error for error in errors)
    assert any("declared audit-phase" in error for error in errors)
    missing = copy.deepcopy(audit)
    missing["deferredUnits"]["DEFERRED-DOWNLOAD-M9"] = [
        {
            "id": "COV-M1-00001",
            "sourceUnitId": "UNRELATED-SOURCE",
            "clause": "UNRELATED",
            "tableOrFigure": None,
            "documentPage": 1,
            "pdfPage": 1,
            "fragmentKind": "PROSE-SENTENCE",
            "fragmentOrdinal": 1,
            "applicabilityDecision": "DEFERRED-FUTURE-SCOPE",
            "requirementIds": [],
        }
    ]
    assert any("DEFERRED-DOWNLOAD-M9" in error for error in baseline.protocol_source_audit_errors(missing, crs))
    implicit = copy.deepcopy(audit)
    del implicit["requirementGenerationAllowed"]
    assert any("requirementGenerationAllowed" in error for error in baseline.protocol_source_audit_errors(implicit, crs))


def test_protocol_source_audit_rejects_locator_and_duplicate_drift() -> None:
    audit = json.loads(source("configs/research/cltav_protocol_source_audit.json"))
    crs = json.loads(source("configs/requirements/arinc_615a3_m1_crs.json"))
    fake_row = {
        "id": "COV-M1-00001",
        "sourceUnitId": "UNRELATED-SOURCE",
        "clause": "UNRELATED",
        "tableOrFigure": None,
        "documentPage": 1,
        "pdfPage": 1,
        "fragmentKind": "PROSE-SENTENCE",
        "fragmentOrdinal": 1,
        "applicabilityDecision": "DEFERRED-FUTURE-SCOPE",
        "requirementIds": [],
    }
    mutated = copy.deepcopy(audit)
    mutated["deferredUnits"]["DEFERRED-DOWNLOAD-M9"] = [dict(fake_row)]
    assert any("IDs" in error for error in baseline.protocol_source_audit_errors(mutated, crs))
    duplicated = copy.deepcopy(audit)
    duplicated["deferredUnits"]["DEFERRED-DOWNLOAD-M9"] = [dict(fake_row), dict(fake_row)]
    assert any("duplicate" in error for error in baseline.protocol_source_audit_errors(duplicated, crs))
    missing_field = copy.deepcopy(audit)
    missing_field["deferredUnits"]["DEFERRED-DOWNLOAD-M9"] = [dict(fake_row)]
    del missing_field["deferredUnits"]["DEFERRED-DOWNLOAD-M9"][0]["clause"]
    assert any("clause" in error for error in baseline.protocol_source_audit_errors(missing_field, crs))
    drifted = copy.deepcopy(audit)
    drifted["summary"]["deferredFutureScope"]["byRationale"]["DEFERRED-DOWNLOAD-M9"] = 99
    assert any("summary count" in error for error in baseline.protocol_source_audit_errors(drifted, crs))
    groups = copy.deepcopy(audit)
    groups["clauseGroups"]["DEFERRED-DOWNLOAD-M9"] = [
        {"clause": "UNRELATED", "tableOrFigure": None, "count": 1, "coverageIds": ["COV-M1-00001"]}
    ]
    assert any("clauseGroups" in error for error in baseline.protocol_source_audit_errors(groups, crs))
    for field in baseline.AUDIT_UNIT_FIELDS:
        if field == "id":
            continue
        field_mutated = copy.deepcopy(audit)
        field_mutated["deferredUnits"]["DEFERRED-DOWNLOAD-M9"] = [dict(fake_row)]
        row = field_mutated["deferredUnits"]["DEFERRED-DOWNLOAD-M9"][0]
        if field == "requirementIds":
            row[field] = ["CRS-UNRELATED"]
        elif isinstance(row.get(field), int):
            row[field] = int(row[field] or 0) + 99999
        else:
            row[field] = f"UNRELATED-{field}"
        errors = baseline.protocol_source_audit_errors(field_mutated, crs)
        assert any("IDs" in error or field in error for error in errors), field
    total = copy.deepcopy(audit)
    total["summary"]["deferredFutureScope"]["total"] = 99999
    assert any("deferredFutureScope.total" in error for error in baseline.protocol_source_audit_errors(total, crs))
    app = copy.deepcopy(audit)
    app["summary"]["applicabilityDecisions"]["DEFERRED-FUTURE-SCOPE"] = 99999
    assert any("applicabilityDecisions" in error for error in baseline.protocol_source_audit_errors(app, crs))
    bound_count = copy.deepcopy(audit)
    bound_count["boundPackage"]["coverageCount"] = 1
    assert any("boundPackage.coverageCount" in error for error in baseline.protocol_source_audit_errors(bound_count, crs))
    missing_reread = copy.deepcopy(audit)
    missing_reread["status"] = "SOURCE-UNIT-AUDIT-IN-PROGRESS"
    missing_reread["requirementGenerationAllowed"] = False
    missing_reread.pop("sourceReread", None)
    assert any("sourceReread" in error for error in baseline.protocol_source_audit_errors(missing_reread, crs))
    promoted = copy.deepcopy(audit)
    commentary = next(
        row
        for row in promoted["sourceReread"]["units"]
        if row["frozenSourceModality"] == "COMMENTARY"
    )
    commentary["candidateApplicability"] = "APPLICABLE"
    assert any("commentary" in error for error in baseline.protocol_source_audit_errors(promoted, crs))
    dropped = copy.deepcopy(audit)
    dropped["sourceReread"]["units"] = dropped["sourceReread"]["units"][1:]
    dropped["sourceReread"]["unitsRead"] = len(dropped["sourceReread"]["units"])
    assert any(
        "DEFERRED-FIND-M9" in error and "IDs" in error
        for error in baseline.protocol_source_audit_errors(dropped, crs)
    )
    mixed = copy.deepcopy(audit)
    media = next(
        row
        for row in mixed["sourceReread"]["units"]
        if row.get("downloadMode") == "MEDIA-DEFINED"
    )
    media["downloadMode"] = "OPERATOR-DEFINED"
    assert any(
        "Media Defined and Operator Defined" in error
        for error in baseline.protocol_source_audit_errors(mixed, crs)
    )
    dropped_download = copy.deepcopy(audit)
    download_units = [
        row
        for row in dropped_download["sourceReread"]["units"]
        if row.get("frozenRationaleCode") == "DEFERRED-DOWNLOAD-M9"
    ]
    dropped_download["sourceReread"]["units"] = [
        row
        for row in dropped_download["sourceReread"]["units"]
        if row.get("id") != download_units[0]["id"]
    ]
    dropped_download["sourceReread"]["unitsRead"] = len(dropped_download["sourceReread"]["units"])
    assert any(
        "DEFERRED-DOWNLOAD-M9" in error and "IDs" in error
        for error in baseline.protocol_source_audit_errors(dropped_download, crs)
    )
    activated = copy.deepcopy(audit)
    afdx = next(
        row
        for row in activated["sourceReread"]["units"]
        if row.get("frozenRationaleCode") == "DEFERRED-AFDX-DEPLOYMENT-M2-INFRASTRUCTURE-BINDING"
    )
    afdx["candidateApplicability"] = "APPLICABLE"
    assert any(
        "Compliant instance" in error
        for error in baseline.protocol_source_audit_errors(activated, crs)
    )
    dropped_afdx = copy.deepcopy(audit)
    afdx_units = [
        row
        for row in dropped_afdx["sourceReread"]["units"]
        if row.get("frozenRationaleCode") == "DEFERRED-AFDX-DEPLOYMENT-M2-INFRASTRUCTURE-BINDING"
    ]
    dropped_afdx["sourceReread"]["units"] = [
        row
        for row in dropped_afdx["sourceReread"]["units"]
        if row.get("id") != afdx_units[0]["id"]
    ]
    dropped_afdx["sourceReread"]["unitsRead"] = len(dropped_afdx["sourceReread"]["units"])
    assert any(
        "DEFERRED-AFDX-DEPLOYMENT-M2-INFRASTRUCTURE-BINDING" in error and "IDs" in error
        for error in baseline.protocol_source_audit_errors(dropped_afdx, crs)
    )


def test_find_required_reread_candidates_have_crs_rows() -> None:
    audit = json.loads(source("configs/research/cltav_protocol_source_audit.json"))
    crs = json.loads(source("configs/requirements/arinc_615a3_m1_crs.json"))
    ledger = {row["id"]: row for row in crs["coverageLedger"]}
    req_ids = {row["id"] for row in crs["requirements"]}
    generated = 0
    for unit in audit["sourceReread"]["units"]:
        if unit.get("frozenRationaleCode") != "DEFERRED-FIND-M9":
            continue
        row = ledger[unit["id"]]
        assert row["rationaleCode"] != "DEFERRED-FIND-M9"
        if unit["candidateConformanceEffect"] in {"REQUIRED", "OPTIONAL"}:
            assert row["requirementIds"], unit["id"]
            assert row["requirementIds"][0] in req_ids
            generated += 1
        else:
            assert row["requirementIds"] == []
            assert row["applicabilityDecision"] in {"OUT-OF-PROFILE", "APPLICABLE-SUPPORTING", "CONDITIONAL"}
    assert generated == 34
    assert crs["artifactVersion"] == "M1-CANDIDATE-11"


def test_download_and_afdx_required_reread_candidates_have_crs_rows() -> None:
    audit = json.loads(source("configs/research/cltav_protocol_source_audit.json"))
    crs = json.loads(source("configs/requirements/arinc_615a3_m1_crs.json"))
    ledger = {row["id"]: row for row in crs["coverageLedger"]}
    req_ids = {row["id"] for row in crs["requirements"]}
    download = 0
    afdx = 0
    for unit in audit["sourceReread"]["units"]:
        code = unit.get("frozenRationaleCode")
        if code not in {"DEFERRED-DOWNLOAD-M9", "DEFERRED-AFDX-DEPLOYMENT-M2-INFRASTRUCTURE-BINDING"}:
            continue
        row = ledger[unit["id"]]
        assert row["rationaleCode"] != code
        if code == "DEFERRED-AFDX-DEPLOYMENT-M2-INFRASTRUCTURE-BINDING":
            assert row["applicabilityDecision"] in {"CONDITIONAL", "OUT-OF-PROFILE"}
            assert row["applicabilityDecision"] not in {"APPLICABLE-BASE", "APPLICABLE-SUPPORTING"}
        if unit["candidateConformanceEffect"] in {"REQUIRED", "OPTIONAL"}:
            assert row["requirementIds"], unit["id"]
            assert row["requirementIds"][0] in req_ids
            if code == "DEFERRED-DOWNLOAD-M9":
                download += 1
            else:
                afdx += 1
        else:
            assert row["requirementIds"] == []
    assert download == 103
    assert afdx == 3
    assert crs["artifactVersion"] == "M1-CANDIDATE-11"


def test_protocol_source_audit_allows_declared_future_status_pairs() -> None:
    audit = json.loads(source("configs/research/cltav_protocol_source_audit.json"))
    crs = json.loads(source("configs/requirements/arinc_615a3_m1_crs.json"))
    in_progress = copy.deepcopy(audit)
    in_progress["status"] = "SOURCE-UNIT-AUDIT-IN-PROGRESS"
    in_progress["requirementGenerationAllowed"] = False
    assert baseline.protocol_source_audit_errors(in_progress, crs) == []
    partial = copy.deepcopy(audit)
    partial["status"] = "PARTIAL-CRS-GENERATION-IN-PROGRESS"
    partial["requirementGenerationAllowed"] = True
    assert not any(
        "requirementGenerationAllowed" in error or "declared audit-phase" in error
        for error in baseline.protocol_source_audit_errors(partial, crs)
    )
    complete = copy.deepcopy(audit)
    complete["status"] = "AUDIT-COMPLETE-REQUIREMENT-GENERATION-ALLOWED"
    complete["requirementGenerationAllowed"] = True
    errors = baseline.protocol_source_audit_errors(complete, crs)
    assert not any("requirementGenerationAllowed" in error for error in errors)
    assert not any("declared audit-phase" in error for error in errors)
    complete["requirementGenerationAllowed"] = False
    assert any(
        "requirementGenerationAllowed" in error
        for error in baseline.protocol_source_audit_errors(complete, crs)
    )


def test_supporting_source_audit_production_gate_rejects_missing_duplicate_and_empty_leaves() -> None:
    audit = json.loads(source("configs/research/cltav_protocol_source_audit.json"))
    crs = json.loads(source("configs/requirements/arinc_615a3_m1_crs.json"))
    assert baseline.protocol_source_audit_errors(audit, crs) == []
    missing = copy.deepcopy(audit)
    del missing["supportingSourceApplicabilityAudit"]
    assert any(
        "supportingSourceApplicabilityAudit is required" in error
        for error in baseline.protocol_source_audit_errors(missing, crs)
    )
    duplicated = copy.deepcopy(audit)
    duplicated["supportingSourceApplicabilityAudit"]["sources"].append(
        copy.deepcopy(duplicated["supportingSourceApplicabilityAudit"]["sources"][0])
    )
    errors = baseline.protocol_source_audit_errors(duplicated, crs)
    assert any("duplicate sourceId" in error for error in errors)
    empty_leaves = copy.deepcopy(audit)
    unit = next(
        row
        for source in empty_leaves["supportingSourceApplicabilityAudit"]["sources"]
        for row in source["units"]
        if row.get("leafCrsStatus") == "LEAF-CRS-EMITTED"
    )
    unit["leafCoverageIds"] = []
    unit["leafRequirementIds"] = []
    assert any(
        "missing leafCoverageIds" in error
        for error in baseline.protocol_source_audit_errors(empty_leaves, crs)
    )
    cross = copy.deepcopy(audit)
    foreign = next(
        row["id"]
        for row in crs["requirements"]
        if row["source"]["sourceId"] == "ARINC-615A-3"
    )
    rfc_unit = next(
        row
        for source in cross["supportingSourceApplicabilityAudit"]["sources"]
        if source["sourceId"] == "RFC-2348"
        for row in source["units"]
        if row.get("leafCrsStatus") == "LEAF-CRS-EMITTED"
    )
    rfc_unit["leafRequirementIds"] = [foreign]
    assert any(
        "leafRequirementIds do not match" in error or "is from ARINC-615A-3" in error
        for error in baseline.protocol_source_audit_errors(cross, crs)
    )
    fake_denom = copy.deepcopy(audit)
    fake_denom["supportingSourceApplicabilityAudit"]["sources"][0]["coverageDenominator"]["count"] = 1
    assert any(
        "coverageDenominator.count" in error
        for error in baseline.protocol_source_audit_errors(fake_denom, crs)
    )
    extension = copy.deepcopy(audit)
    first_source = extension["supportingSourceApplicabilityAudit"]["sources"][0]
    extra = copy.deepcopy(first_source["units"][-1])
    extra["id"] = extra["id"] + "-EXTENSION"
    extra["clause"] = str(extra.get("clause") or "CLAUSE") + "-EXTENSION"
    extra["leafCrsStatus"] = "NOT-REQUIRED"
    extra["applicabilityDecision"] = "OUT-OF-PROFILE"
    extra["conformanceEffect"] = "INFORMATIVE"
    extra.pop("leafCoverageIds", None)
    extra.pop("leafRequirementIds", None)
    extra.pop("remainingSubunits", None)
    first_source["units"].append(extra)
    first_source["coverageDenominator"]["count"] = len(first_source["units"])
    assert baseline.supporting_source_audit_errors(extension, crs) == []
    timeout = next(
        row
        for source in audit["supportingSourceApplicabilityAudit"]["sources"]
        if source["sourceId"] == "RFC-2349"
        for row in source["units"]
        if row["id"] == "SAU-2349-TO"
    )
    tsize = next(
        row
        for source in audit["supportingSourceApplicabilityAudit"]["sources"]
        if source["sourceId"] == "RFC-2349"
        for row in source["units"]
        if row["id"] == "SAU-2349-TS"
    )
    swapped = copy.deepcopy(audit)
    swapped_timeout = next(
        row
        for source in swapped["supportingSourceApplicabilityAudit"]["sources"]
        if source["sourceId"] == "RFC-2349"
        for row in source["units"]
        if row["id"] == "SAU-2349-TO"
    )
    swapped_timeout["leafCoverageIds"] = list(tsize["leafCoverageIds"])
    swapped_timeout["leafRequirementIds"] = list(tsize["leafRequirementIds"])
    swapped_errors = baseline.protocol_source_audit_errors(swapped, crs)
    assert any("admitted leaf-unit set" in error or "outside the unit locator scope" in error for error in swapped_errors)
    demoted = copy.deepcopy(audit)
    demoted_timeout = next(
        row
        for source in demoted["supportingSourceApplicabilityAudit"]["sources"]
        if source["sourceId"] == "RFC-2349"
        for row in source["units"]
        if row["id"] == "SAU-2349-TO"
    )
    demoted_timeout["leafCrsStatus"] = "NOT-REQUIRED"
    demoted_timeout.pop("leafCoverageIds", None)
    demoted_timeout.pop("leafRequirementIds", None)
    demoted_timeout.pop("admittedLeafUnits", None)
    assert any(
        "cannot be NOT-REQUIRED" in error
        for error in baseline.protocol_source_audit_errors(demoted, crs)
    )
    trimmed = copy.deepcopy(audit)
    trimmed_timeout = next(
        row
        for source in trimmed["supportingSourceApplicabilityAudit"]["sources"]
        if source["sourceId"] == "RFC-2349"
        for row in source["units"]
        if row["id"] == "SAU-2349-TO"
    )
    trimmed_timeout["admittedLeafUnits"] = trimmed_timeout["admittedLeafUnits"][:1]
    assert any(
        "admitted leaf-unit set" in error
        for error in baseline.protocol_source_audit_errors(trimmed, crs)
    )
    same_source_wrong_clause = copy.deepcopy(audit)
    wrong = next(
        row
        for source in same_source_wrong_clause["supportingSourceApplicabilityAudit"]["sources"]
        if source["sourceId"] == "RFC-2349"
        for row in source["units"]
        if row["id"] == "SAU-2349-TO"
    )
    wrong["admittedLeafUnits"] = copy.deepcopy(tsize["admittedLeafUnits"])
    wrong["leafCoverageIds"] = list(tsize["leafCoverageIds"])
    wrong["leafRequirementIds"] = list(tsize["leafRequirementIds"])
    assert any(
        "outside the unit locator scope" in error or "admitted coverage" in error
        for error in baseline.protocol_source_audit_errors(same_source_wrong_clause, crs)
    )
    batch = next(
        row
        for source in audit["supportingSourceApplicabilityAudit"]["sources"]
        if source["sourceId"] == "ARINC-665-5"
        for row in source["units"]
        if row["id"] == "SAU-665-2-3"
    )
    assert any(
        str(item.get("clause") or "").startswith("2.3") and str(item.get("clause") or "") != "2.3"
        for item in batch["admittedLeafUnits"]
    )
    assert timeout["clause"] != tsize["clause"]


def _rfc2349_timeout_unit(audit: dict) -> dict:
    return next(
        row
        for source in audit["supportingSourceApplicabilityAudit"]["sources"]
        if source["sourceId"] == "RFC-2349"
        for row in source["units"]
        if row["id"] == "SAU-2349-TO"
    )


def _strip_leaf_refs(unit: dict) -> None:
    for key in ("leafCoverageIds", "leafRequirementIds", "admittedLeafUnits"):
        unit.pop(key, None)


@pytest.mark.parametrize("leaf_status", sorted(baseline.SUPPORTING_LEAF_STATUSES))
def test_required_timeout_unit_cannot_drop_leaves_by_status_change(leaf_status: str) -> None:
    audit = json.loads(source("configs/research/cltav_protocol_source_audit.json"))
    crs = json.loads(source("configs/requirements/arinc_615a3_m1_crs.json"))
    broken = copy.deepcopy(audit)
    unit = _rfc2349_timeout_unit(broken)
    assert unit["applicabilityDecision"] == "APPLICABLE-SUPPORTING"
    assert unit["conformanceEffect"] == "REQUIRED"
    unit["leafCrsStatus"] = leaf_status
    _strip_leaf_refs(unit)
    errors = baseline.protocol_source_audit_errors(broken, crs)
    assert errors
    if leaf_status == "NOT-REQUIRED":
        assert any("cannot be NOT-REQUIRED" in error for error in errors)
    elif leaf_status in baseline.SUPPORTING_UNBOUND_LEAF_STATUSES:
        assert any("cannot use an unbound leaf status" in error for error in errors)
    else:
        assert any("missing leafCoverageIds" in error or "admitted leaf-unit set" in error for error in errors)


def test_forged_unbound_disposition_does_not_authorize_timeout_unit() -> None:
    audit = json.loads(source("configs/research/cltav_protocol_source_audit.json"))
    crs = json.loads(source("configs/requirements/arinc_615a3_m1_crs.json"))
    broken = copy.deepcopy(audit)
    supporting = broken["supportingSourceApplicabilityAudit"]
    legal = copy.deepcopy(supporting["unboundDispositions"][0])
    unit = _rfc2349_timeout_unit(broken)
    forged = {
        "id": "UD-FORGED-TIMEOUT",
        "auditUnitId": unit["id"],
        "sourceId": "RFC-2349",
        "clause": unit["clause"],
        "affectedRequirementId": unit["leafRequirementIds"][0],
        "affectedCoverageId": unit["leafCoverageIds"][0],
        "rationaleCode": unit["rationaleCode"],
        "status": legal["status"],
        "notIndependentApproval": True,
        "unfinishedScopeEn": legal["unfinishedScopeEn"],
        "unfinishedScopeZh": legal["unfinishedScopeZh"],
    }
    supporting["unboundDispositions"].append(forged)
    unit["leafCrsStatus"] = next(iter(baseline.SUPPORTING_UNBOUND_LEAF_STATUSES))
    unit["unboundDispositionId"] = forged["id"]
    _strip_leaf_refs(unit)
    errors = baseline.protocol_source_audit_errors(broken, crs)
    assert any("cannot use an unbound leaf status" in error for error in errors)


def test_recorded_unbound_disposition_keeps_affected_identity_and_unfinished_scope() -> None:
    audit = json.loads(source("configs/research/cltav_protocol_source_audit.json"))
    crs = json.loads(source("configs/requirements/arinc_615a3_m1_crs.json"))
    assert baseline.protocol_source_audit_errors(audit, crs) == []
    supporting = audit["supportingSourceApplicabilityAudit"]
    legal_unit = next(
        row
        for source in supporting["sources"]
        for row in source["units"]
        if row.get("leafCrsStatus") in baseline.SUPPORTING_UNBOUND_LEAF_STATUSES
    )
    disposition = next(
        row
        for row in supporting["unboundDispositions"]
        if row["id"] == legal_unit["unboundDispositionId"]
    )
    assert disposition["auditUnitId"] == legal_unit["id"]
    assert disposition["sourceId"]
    assert disposition["clause"] == legal_unit["clause"]
    assert disposition["rationaleCode"] == legal_unit["rationaleCode"]
    assert disposition["affectedRequirementId"] in {row["id"] for row in crs["requirements"]}
    assert disposition["affectedCoverageId"] in {row["id"] for row in crs["coverageLedger"]}
    assert disposition["unfinishedScopeEn"]
    assert disposition["unfinishedScopeZh"]
    missing_list = copy.deepcopy(audit)
    del missing_list["supportingSourceApplicabilityAudit"]["unboundDispositions"]
    assert any(
        "unboundDispositions is required" in error
        for error in baseline.protocol_source_audit_errors(missing_list, crs)
    )
    dropped = copy.deepcopy(audit)
    dropped_unit = next(
        row
        for source in dropped["supportingSourceApplicabilityAudit"]["sources"]
        for row in source["units"]
        if row.get("leafCrsStatus") in baseline.SUPPORTING_UNBOUND_LEAF_STATUSES
    )
    dropped_unit.pop("unboundDispositionId")
    assert any(
        "missing unboundDispositionId" in error
        for error in baseline.protocol_source_audit_errors(dropped, crs)
    )
    forged_identity = copy.deepcopy(audit)
    forged_identity["supportingSourceApplicabilityAudit"]["unboundDispositions"][0]["affectedCoverageId"] = "COV-FORGED"
    assert any(
        "unbound affected coverage" in error
        for error in baseline.protocol_source_audit_errors(forged_identity, crs)
    )


def test_cltav_outline_rejects_title_only_chapters() -> None:
    text = source("docs/research/publication/RESEARCH_OUTLINE.md")
    assert baseline.cltav_outline_errors(text) == []
    stripped = text.replace("- **Claim:**", "- **Title:**", 1)
    assert any("claim" in error for error in baseline.cltav_outline_errors(stripped))


def test_cltav_sysml_rejects_missing_stop_class() -> None:
    models = {
        name: source(f"docs/research/publication/models/{name}")
        for name in baseline.CLTAV_PUML_FILES
    }
    assert baseline.cltav_sysml_errors(models) == []
    models["FIG-CL-TAV-05-closed-loop-activity.puml"] = models[
        "FIG-CL-TAV-05-closed-loop-activity.puml"
    ].replace("Stop-Budget", "StopLater")
    assert any("Stop-Budget" in error for error in baseline.cltav_sysml_errors(models))
    machines = {
        name: source(f"docs/research/publication/models/{name}")
        for name in baseline.CLTAV_PUML_FILES
    }
    machines["FIG-CL-TAV-07-two-state-machines.puml"] += "\nInformation --> Upload\n"
    assert any("Information" in error for error in baseline.cltav_sysml_errors(machines))
    assert baseline.cltav_figure_errors() == []


def test_math_and_mapping_frozen_payloads_are_unchanged() -> None:
    test_historical_methodology_math_identity_is_preserved()
    assert baseline.mapping_reconciliation_errors(source("docs/control/contracts/GVS_INSTANCE_MAPPING.md")) == []
