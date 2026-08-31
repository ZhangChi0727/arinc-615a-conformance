"""Negative regression tests for data-driven repository governance."""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path


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


def test_archived_reader_report_path_must_resolve() -> None:
    data = status()
    data["release"]["records"]["historicalReaderReportPath"] = "artifacts/reports/archive/missing.md"
    assert any("historicalReaderReportPath" in error for error in baseline.sync.status_errors(data, ROOT))


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


def test_status_rejects_method_identity_conflation() -> None:
    data = status()
    data["methodInputs"]["compatibilityDisposition"]["commit"] = data["methodInputs"]["methodDefinition"]["commit"]
    assert any("conflated" in error for error in baseline.sync.status_errors(data, ROOT))


def test_math_and_mapping_frozen_payloads_are_unchanged() -> None:
    count, digest = baseline.display_math_fingerprint(source(baseline.REPORT_PATH.relative_to(ROOT)))
    assert count == baseline.REPORT_DISPLAY_MATH_BLOCKS
    assert digest == baseline.REPORT_DISPLAY_MATH_SHA256
    assert baseline.mapping_reconciliation_errors(source("docs/control/contracts/GVS_INSTANCE_MAPPING.md")) == []
