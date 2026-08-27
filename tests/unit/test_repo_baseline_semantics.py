"""Negative regression tests for PR #9 cross-repository governance checks."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "check_repo_baseline", ROOT / "scripts/check_repo_baseline.py"
)
assert SPEC is not None and SPEC.loader is not None
baseline = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(baseline)


def source(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_mapping_rejects_missing_method_source_row() -> None:
    text = source("docs/control/contracts/GVS_INSTANCE_MAPPING.md")
    broken = text.replace("| R06 |", "| X06 |", 1)
    errors = baseline.mapping_reconciliation_errors(broken)
    assert any("source row R06" in error for error in errors)


def test_mapping_rejects_combined_case_and_procedure_identity() -> None:
    text = source("docs/control/contracts/GVS_INSTANCE_MAPPING.md")
    broken = text.replace(
        "| R08 | `VerificationProcedure` | procedure |",
        "| R08 | `VerificationCase` | VC |",
        1,
    )
    errors = baseline.mapping_reconciliation_errors(broken)
    assert any("R08" in error or "independent rows" in error for error in errors)


def test_mapping_rejects_fabricated_external_locator() -> None:
    text = source("docs/control/contracts/GVS_INSTANCE_MAPPING.md")
    broken = text.replace(
        "| A01 | `INSTANCE-ONLY-ADDITIONAL` | `VerificationCase` |",
        "| A01 | `INSTANCE-ONLY-ADDITIONAL` | `FabricatedGenericRole` |",
        1,
    )
    errors = baseline.mapping_reconciliation_errors(broken)
    assert any("unknown external role locator" in error for error in errors)


def test_mapping_rejects_high_risk_status_strengthening() -> None:
    text = source("docs/control/contracts/GVS_INSTANCE_MAPPING.md")
    gate_broken = text.replace(
        "| R15 | `CompositeGate` | RG/G gate package | PR #9 / v4.3 candidate | `specializes` | `NOT-DETERMINED` |",
        "| R15 | `CompositeGate` | RG/G gate package | PR #9 / v4.3 candidate | `specializes` | `CANDIDATE` |",
        1,
    )
    config_broken = text.replace(
        "| A07 | `INSTANCE-ONLY-ADDITIONAL` | `Configuration` | future Project Configuration `TMP-PC-ARINC615A-01` | PR #9 / v4.3 candidate | `no-direct-correspondence` | `NOT-DETERMINED` |",
        "| A07 | `INSTANCE-ONLY-ADDITIONAL` | `Configuration` | future Project Configuration `TMP-PC-ARINC615A-01` | PR #9 / v4.3 candidate | `instantiates` | `CANDIDATE` |",
        1,
    )
    assert any("R15" in error for error in baseline.mapping_reconciliation_errors(gate_broken))
    assert any("A07" in error for error in baseline.mapping_reconciliation_errors(config_broken))


def test_acceptance_check_rejects_missing_id_and_stale_reference() -> None:
    baseline_text = source("docs/control/baselines/RB-2026-001-v4.3.md")
    cr_text = source("docs/control/changes/CR-2026-004.md")
    missing = cr_text.replace("| AC-12 |", "| AX-12 |", 1)
    assert any("acceptance IDs differ" in error for error in baseline.acceptance_criteria_errors(baseline_text, missing))
    stale = baseline_text + "\nSee section " + "21 for acceptance."
    assert any("stale nonexistent" in error for error in baseline.acceptance_criteria_errors(stale, cr_text))


def test_cr_metadata_check_rejects_bilingual_identity_drift() -> None:
    text = source("docs/control/changes/CR-2026-004.md")
    english, chinese = text.split(baseline.ZH_MARKER, 1)
    chinese = chinese.replace(baseline.METHOD_DEFINITION_COMMIT, "0" * 40, 1)
    errors = baseline.cr_bilingual_metadata_errors(english + baseline.ZH_MARKER + chinese)
    assert any("Chinese CR metadata differs for method commit" in error for error in errors)


def test_observation_result_check_rejects_result_as_observation() -> None:
    pbc = source("docs/control/contracts/ARINC615A_PROFILE_BINDING_CONFIGURATION.md")
    handoff = source("docs/control/reviews/PR9_GVS_MIGRATION_REVIEW_HANDOFF.md")
    broken = pbc + "\nA verdict/result is an observation.\n"
    errors = baseline.observation_result_errors(broken, handoff)
    assert any("incorrectly defines" in error for error in errors)


def test_evidence_chain_check_rejects_missing_control_refs() -> None:
    architecture = source("docs/control/contracts/ARCHITECTURE.md")
    osr = source("docs/control/contracts/OBJECTIVE_SATISFACTION_RECORD.md")
    cei = source("docs/control/contracts/COMPLIANCE_EVIDENCE_INDEX.md")
    manifest = source("docs/engineering/design/EVIDENCE_MANIFEST.md")

    broken_osr = osr.replace("supportingEvidenceItems", "uncontrolledItems", 1)
    assert any(
        "supportingEvidenceItems" in error
        for error in baseline.evidence_chain_errors(architecture, broken_osr, cei, manifest)
    )

    broken_cei = cei.replace("statusDecisionRef", "localStatusSource", 1)
    assert any(
        "statusDecisionRef" in error
        for error in baseline.evidence_chain_errors(architecture, osr, broken_cei, manifest)
    )

def acknowledgement_texts() -> tuple[str, str, str, str, str, str]:
    return (
        source("docs/control/contracts/EXTERNAL_GVS_BINDING.md"),
        source("docs/control/contracts/GVS_INSTANCE_MAPPING.md"),
        source("docs/control/contracts/ARINC615A_PROFILE_BINDING_CONFIGURATION.md"),
        source("docs/control/baselines/RB-2026-001-v4.3.1.md"),
        source("docs/control/changes/CR-2026-005.md"),
        source("docs/control/reviews/PR10_GVS_DISPOSITION_ACK_REVIEW_HANDOFF.md"),
    )


def ack_errors(parts: tuple[str, str, str, str, str, str]) -> list[str]:
    return baseline.third_handshake_acknowledgement_errors(*parts)


def test_acknowledgement_rejects_swapped_method_identities() -> None:
    parts = list(acknowledgement_texts())
    parts[0] = parts[0].replace(
        f"| **MethodDefinitionCommit** | `{baseline.METHOD_DEFINITION_COMMIT}` |",
        f"| **MethodDefinitionCommit** | `{baseline.METHOD_DISPOSITION_COMMIT}` |",
        1,
    ).replace(
        f"| **MethodCompatibilityDispositionCommit** | `{baseline.METHOD_DISPOSITION_COMMIT}` |",
        f"| **MethodCompatibilityDispositionCommit** | `{baseline.METHOD_DEFINITION_COMMIT}` |",
        1,
    )
    errors = ack_errors(tuple(parts))
    assert any("binding MethodDefinitionCommit identity differs" in error for error in errors)
    assert any("binding MethodCompatibilityDispositionCommit identity differs" in error for error in errors)


def test_acknowledgement_rejects_wrong_arinc_release_identity() -> None:
    parts = list(acknowledgement_texts())
    parts[3] = parts[3].replace(baseline.ARINC_V43_RELEASE_COMMIT, "0" * 40)
    errors = ack_errors(tuple(parts))
    assert any("baseline is missing controlled identity" in error for error in errors)


def test_acknowledgement_rejects_missing_qualification() -> None:
    parts = list(acknowledgement_texts())
    parts[4] = parts[4].replace("| Q-09 |", "| Q-X9 |", 1)
    errors = ack_errors(tuple(parts))
    assert any("qualification IDs differ" in error for error in errors)


def test_acknowledgement_rejects_evaluation_or_configuration_promotion() -> None:
    parts = list(acknowledgement_texts())
    parts[1] = parts[1].replace("NOT-EXERCISED", "INSTANCE-EXERCISED", 1)
    errors = ack_errors(tuple(parts))
    assert any("mapping controlled Instance evaluation differs" in error for error in errors)
    assert any("prohibited promotion: INSTANCE-EXERCISED" in error for error in errors)

    parts = list(acknowledgement_texts())
    parts[2] = parts[2].replace("NOT YET ESTABLISHED", "ESTABLISHED", 1)
    errors = ack_errors(tuple(parts))
    assert any("PBC controlled Project Configuration differs" in error for error in errors)


def test_acknowledgement_rejects_mutable_or_wrong_commit_bound_locator() -> None:
    parts = list(acknowledgement_texts())
    parts[0] = parts[0].replace(
        f"/blob/{baseline.METHOD_DEFINITION_COMMIT}/",
        "/blob/main/",
        1,
    )
    assert any("wrong or mutable commit-bound association" in error for error in ack_errors(tuple(parts)))

    parts = list(acknowledgement_texts())
    parts[0] = parts[0].replace(
        f"/blob/{baseline.METHOD_DEFINITION_COMMIT}/docs/02_verification_framework/generic_verification_suite_core.md",
        f"/blob/{baseline.METHOD_DISPOSITION_COMMIT}/docs/02_verification_framework/generic_verification_suite_core.md",
        1,
    )
    assert any("wrong or mutable commit-bound association" in error for error in ack_errors(tuple(parts)))


def test_acknowledgement_rejects_false_native_approval_state() -> None:
    parts = list(acknowledgement_texts())
    parts[5] = parts[5].replace("Platform state `COMMENTED`", "Platform state `APPROVED`", 1)
    errors = ack_errors(tuple(parts))
    assert any("natural-person review truth is missing" in error for error in errors)
