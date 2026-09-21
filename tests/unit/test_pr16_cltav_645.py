from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


baseline = _load("check_repo_baseline", ROOT / "scripts/check_repo_baseline.py")
m1 = _load("sync_m1_crs", ROOT / "scripts/sync_m1_crs.py")
m2 = _load("sync_m2_model", ROOT / "scripts/sync_m2_model.py")

CRS_PATH = ROOT / "configs/requirements/arinc_615a3_m1_crs.json"
AUDIT_PATH = ROOT / "configs/research/cltav_protocol_source_audit.json"
REGISTRY_PATH = ROOT / "configs/research/cltav_interface_registry.json"
M2_PATH = ROOT / "configs/models/arinc_615a3_m2_model.json"
LOOP_PATH = ROOT / "scripts/cltav_loop_spec.py"
ALG_PATH = ROOT / "docs/research/publication/algorithms/ALG-CLTAV-01.tex"
PUML_PATH = ROOT / "docs/research/publication/models/FIG-CL-TAV-09-experiment-architecture.puml"
LOOP_SPEC = ROOT / "tests/unit/test_cltav_loop_spec.py"
EXP_PLAN = ROOT / "docs/research/EXPERIMENT_PLAN.md"
METHOD_REPORT = ROOT / "docs/research/methodology/RR-2026-001_test_analysis_conformance_methodology.md"
GUIDE = ROOT / "docs/research/publication/PUBLICATION_GUIDE.md"
OUTLINE = ROOT / "docs/research/publication/RESEARCH_OUTLINE.md"


def _crs() -> dict:
    return json.loads(CRS_PATH.read_text(encoding="utf-8"))


def _audit() -> dict:
    return json.loads(AUDIT_PATH.read_text(encoding="utf-8"))


def _m2() -> dict:
    return json.loads(M2_PATH.read_text(encoding="utf-8"))


def _refresh_crs(data: dict) -> None:
    data["inventorySummary"]["coverageFingerprint"] = m1.fingerprint(data["coverageLedger"])
    data["inventorySummary"]["requirementsFingerprint"] = m1.fingerprint(data["requirements"])
    data["reviewControl"]["sourceInventoryFingerprint"] = m1.fingerprint(m1.source_inventory_projection(data))


def test_arinc_645_binding_this_pr_is_true() -> None:
    audit = _audit()
    arinc645 = next(
        source
        for source in audit["supportingSourceApplicabilityAudit"]["sources"]
        if source["sourceId"] == "ARINC-645"
    )
    assert arinc645["status"] == "BOUNDED-AUDIT-COMPLETE"
    assert arinc645["independentApproval"] is False
    assert audit["blockedSource"]["boundThisPr"] is True
    assert audit["blockedSource"]["localFileAcquired"] is True
    assert audit["supportingSourceApplicabilityAudit"]["645BindingThisPr"] is True
    assert audit["remainingSourceWork"]["arinc645BindingThisPr"] is True
    assert audit["remainingSourceWork"]["arinc645CapabilityEstablishmentThisPr"] is False


def test_m1_candidate_24_counts_and_unique_645_leaves() -> None:
    crs = _crs()
    assert crs["artifactVersion"] == "M1-CANDIDATE-24"
    assert len(crs["coverageLedger"]) == 3145
    assert len(crs["requirements"]) == 855
    rows_645 = [row for row in crs["requirements"] if row["source"]["sourceId"] == "ARINC-645"]
    ids = [row["id"] for row in rows_645]
    assert ids == [f"CRS-M1-{n:05d}" for n in range(818, 857)]
    assert len(ids) == 39
    assert all(row["reviewStatus"] == "PENDING-EXTERNAL-INDEPENDENT-REVIEW" for row in rows_645)
    assert all(row["interpretationStatus"] == "CANDIDATE-SOURCE-UNIT-BOUND" for row in rows_645)
    assert {row["rationaleCode"] for row in rows_645} == {
        "615A-TRIGGERED-645-SEMANTIC-MODEL-REFINEMENT-PENDING"
    }
    assert "GAP-ARINC-645" in {gap for row in rows_645 for gap in row["gapIds"]}
    prefix = next(
        row
        for row in rows_645
        if (row.get("semantic") or {}).get("action") == "PREFIX-HEADER-FILENAME"
        or "PREFIX-HEADER" in str((row.get("semantic") or {}).get("action") or "")
    )
    objects = list((prefix.get("semantic") or {}).get("objects") or [])
    assert "DATA-FILE-NAME" not in objects
    assert "SUPPORT-FILE-NAME" not in objects


def test_645_capabilities_remain_not_established() -> None:
    audit = _audit()
    remaining = audit["remainingSourceWork"]
    assert remaining["arinc645CapabilityEstablishmentThisPr"] is False
    assert remaining["crcValidationEstablishedThisPr"] is False
    assert remaining["checkValueValidationEstablishedThisPr"] is False
    assert remaining["namingAlgorithmValidationEstablishedThisPr"] is False
    assert remaining["completeIntegrityValidationEstablishedThisPr"] is False
    gap = remaining["arinc645RemainingWorkAfterThisPr"]
    assert gap["id"] == "GAP-ARINC-645"
    assert gap["status"] == "NOT-ESTABLISHED"
    for key in (
        "crcValidation",
        "checkValueValidation",
        "namingAlgorithmValidation",
        "completeIntegrityValidation",
    ):
        assert gap[key]["status"] == "CAPABILITY-NOT-ESTABLISHED"
        assert gap[key]["establishedThisPr"] is False
    m2_data = _m2()
    blocked = m2_data["model"]["interfaces"]["IF_INTEGRITY"]["blockedBy"]
    assert "ARINC-645" in blocked


def test_665_sau_pointers_keep_integrity_blocked() -> None:
    audit = _audit()
    src_665 = next(
        source
        for source in audit["supportingSourceApplicabilityAudit"]["sources"]
        if source["sourceId"] == "ARINC-665-5"
    )
    by_id = {unit["id"]: unit for unit in src_665["units"]}
    for unit_id in ("SAU-665-4", "SAU-665-5"):
        unit = by_id[unit_id]
        assert unit["leafCrsStatus"] == "EXISTING-LEAF-VIA-645"
        assert unit["refinementStatus"] == "POINTS-TO-BOUND-645-LEAF"
        assert unit["blockedCapability"] == "IF_INTEGRITY"
        assert "CRS-M1-00818" in unit["leafRequirementIds"] or "CRS-M1-00822" in unit["leafRequirementIds"]
    traces = {row["requirementId"]: row for row in _m2()["traceRelations"]}
    for req_id in ("CRS-M1-00818", "CRS-M1-00819", "CRS-M1-00820", "CRS-M1-00821"):
        assert traces[req_id]["targetKind"] == "SCOPE"
        assert traces[req_id]["rationaleCode"] == "645-CRS-MODEL-REFINEMENT-PENDING"


def test_stop_645_is_named_remaining_work_not_missing_file() -> None:
    loop = LOOP_PATH.read_text(encoding="utf-8")
    method = METHOD_REPORT.read_text(encoding="utf-8")
    assert "Stop-645" in loop
    assert "named remaining 645-dependent obligation" in method
    assert "file missing" in method
    assert "file-missing" not in loop.lower()


def test_n25_01_recover_observation_asserts_stop_empty() -> None:
    spec = LOOP_SPEC.read_text(encoding="utf-8")
    assert "test_recover_observation_class_is_also_intersected" in spec
    assert 'assert session.stop == "Stop-Empty"' in spec


def test_algorithm_and_experiment_contract_ids() -> None:
    alg = ALG_PATH.read_text(encoding="utf-8")
    puml = PUML_PATH.read_text(encoding="utf-8")
    plan = EXP_PLAN.read_text(encoding="utf-8")
    for contract_id in (
        "IF-PRED-OBS",
        "IF-HIST-UPDATE",
        "IF-OBS-INTERPRET",
        "IF-SELECT-ADMIT",
        "IF-EXECUTE-RECORD",
        "IF-PREP-RECOVER",
        "IF-EQUIV",
        "IF-RESOURCE-STOP",
    ):
        assert contract_id in alg
        assert contract_id in puml
        assert contract_id in plan
    for exp_id in ("EXP-CLTAV-DETECT", "EXP-CLTAV-LOCATE", "EXP-CLTAV-ABLATION"):
        assert exp_id in puml
        assert exp_id in plan
    for arm in ("CL-T", "CL-A", "CL-TA", "CL-LOOP"):
        assert arm in puml
        assert arm in plan
    assert "evaluator-only" in puml
    assert "forbidden leakage" in puml


def test_publication_positioning_is_tentative_not_final() -> None:
    guide = GUIDE.read_text(encoding="utf-8")
    outline = OUTLINE.read_text(encoding="utf-8")
    assert "IEEE Transactions on Aerospace and Electronic Systems" in guide
    assert "Aerospace Science and Technology" in guide
    assert "PENDING-INSTITUTIONAL-RANKING-CHECK" in guide
    assert "2026-09-20" in guide
    assert "ARINC 615A" in outline
    assert "CL-TAV" in outline
    assert "IEEE TAES" in outline or "Transactions on Aerospace and Electronic Systems" in outline


def test_removing_645_source_fails() -> None:
    audit = _audit()
    crs = _crs()
    supporting = audit["supportingSourceApplicabilityAudit"]
    supporting["sources"] = [row for row in supporting["sources"] if row["sourceId"] != "ARINC-645"]
    errors = baseline.supporting_source_audit_errors(audit, crs)
    assert any("missing sources" in item for item in errors)


def test_645_locator_swap_fails_after_fingerprint_refresh() -> None:
    crs = _crs()
    audit = _audit()
    donor = next(row for row in crs["requirements"] if row["id"] == "CRS-M1-00824")
    target = next(row for row in crs["requirements"] if row["id"] == "CRS-M1-00818")
    target["source"] = copy.deepcopy(donor["source"])
    target["sourceTextHash"] = donor["sourceTextHash"]
    _refresh_crs(crs)
    audit["boundPackage"]["coverageFingerprint"] = crs["inventorySummary"]["coverageFingerprint"]
    audit["boundPackage"]["requirementsFingerprint"] = crs["inventorySummary"]["requirementsFingerprint"]
    errors = baseline.supporting_source_audit_errors(audit, crs)
    assert errors


def test_establishing_645_capability_by_source_bind_fails() -> None:
    audit = _audit()
    crs = _crs()
    remaining = audit["remainingSourceWork"]
    remaining["arinc645CapabilityEstablishmentThisPr"] = True
    remaining["crcValidationEstablishedThisPr"] = True
    remaining["arinc645RemainingWorkAfterThisPr"]["crcValidation"]["status"] = "ESTABLISHED"
    remaining["arinc645RemainingWorkAfterThisPr"]["crcValidation"]["establishedThisPr"] = True
    remaining["arinc645RemainingWorkAfterThisPr"]["status"] = "ESTABLISHED"
    errors = baseline.arinc_645_closure_errors(audit, crs, _m2())
    assert any("must not establish" in item for item in errors)


def test_pinning_m2_to_current_head_fails() -> None:
    data = _m2()
    acc = data["inputAcceptance"]
    acc["successorDelta"]["currentInputArtifactCommit"] = m2.git_output(ROOT, ["rev-parse", "HEAD"])
    errors = m2.successor_input_errors(acc, ROOT, acc.get("inputs") or [])
    assert any("must not be the current HEAD" in item for item in errors)


def test_algorithm_missing_interface_id_is_rejected() -> None:
    text = ALG_PATH.read_text(encoding="utf-8").replace("IF-PRED-OBS", "IF-MISSING")
    errors = baseline.cltav_algorithm_contract_errors(text, PUML_PATH.read_text(encoding="utf-8"), EXP_PLAN.read_text(encoding="utf-8"))
    assert any("IF-PRED-OBS" in item for item in errors)


def test_undeclared_interface_call_is_rejected() -> None:
    text = ALG_PATH.read_text(encoding="utf-8") + "\n% IF-UNDECLARED\n"
    errors = baseline.cltav_algorithm_contract_errors(
        text,
        PUML_PATH.read_text(encoding="utf-8"),
        EXP_PLAN.read_text(encoding="utf-8"),
    )
    assert any("undeclared interface call IF-UNDECLARED" in item for item in errors)


def test_removing_pred_call_while_keeping_macro_is_rejected() -> None:
    text = ALG_PATH.read_text(encoding="utf-8")
    start = text.find(r"\begin{algorithm}")
    mutated = text[:start] + text[start:].replace(r"\IFpred", r"\IFsel")
    errors = baseline.cltav_algorithm_contract_errors(
        mutated,
        PUML_PATH.read_text(encoding="utf-8"),
        EXP_PLAN.read_text(encoding="utf-8"),
    )
    assert any("IF-PRED-OBS" in item for item in errors)


def test_duplicate_interface_id_is_rejected() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["interfaces"].append(copy.deepcopy(registry["interfaces"][0]))
    errors = baseline.cltav_algorithm_contract_errors(
        ALG_PATH.read_text(encoding="utf-8"),
        PUML_PATH.read_text(encoding="utf-8"),
        EXP_PLAN.read_text(encoding="utf-8"),
        registry,
    )
    assert any("duplicate interface ids" in item for item in errors)


def test_missing_history_handle_is_rejected() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    hist = next(row for row in registry["interfaces"] if row["id"] == "IF-HIST-UPDATE")
    hist["inputs"] = ["H"]
    hist["outputs"] = ["Hprime"]
    errors = baseline.cltav_algorithm_contract_errors(
        ALG_PATH.read_text(encoding="utf-8"),
        PUML_PATH.read_text(encoding="utf-8"),
        EXP_PLAN.read_text(encoding="utf-8"),
        registry,
    )
    assert any("HistoryHandle" in item for item in errors)


def test_missing_prep_confirmation_output_is_rejected() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    prep = next(row for row in registry["interfaces"] if row["id"] == "IF-PREP-RECOVER")
    prep["outputs"] = ["prepError"]
    errors = baseline.cltav_algorithm_contract_errors(
        ALG_PATH.read_text(encoding="utf-8"),
        PUML_PATH.read_text(encoding="utf-8"),
        EXP_PLAN.read_text(encoding="utf-8"),
        registry,
    )
    assert any("confirmation" in item for item in errors)


def test_truth_to_arms_without_forbidden_is_rejected() -> None:
    puml = PUML_PATH.read_text(encoding="utf-8").replace("forbidden leakage", "visible copy")
    errors = baseline.cltav_algorithm_contract_errors(
        ALG_PATH.read_text(encoding="utf-8"),
        puml,
        EXP_PLAN.read_text(encoding="utf-8"),
    )
    assert any("must not give evaluator truth to comparison arms" in item for item in errors)


def test_experiment_missing_denominator_is_rejected() -> None:
    plan = EXP_PLAN.read_text(encoding="utf-8").replace("unconfirmed-injection", "xxxx")
    errors = baseline.cltav_algorithm_contract_errors(
        ALG_PATH.read_text(encoding="utf-8"),
        PUML_PATH.read_text(encoding="utf-8"),
        plan,
    )
    assert any("unconfirmed-injection" in item for item in errors)


def test_645_prefix_on_data_or_support_fails_after_refresh() -> None:
    crs = _crs()
    audit = _audit()
    row = next(
        item
        for item in crs["requirements"]
        if "PREFIX-HEADER" in str((item.get("semantic") or {}).get("action") or "")
    )
    row.setdefault("semantic", {}).setdefault("objects", []).append("DATA-FILE-NAME")
    _refresh_crs(crs)
    errors = baseline.arinc_645_closure_errors(audit, crs, _m2())
    assert any("must not apply to Data or Support" in item for item in errors)


def test_645_case_rule_as_lsp_identity_fails() -> None:
    crs = _crs()
    row = next(item for item in crs["requirements"] if item["id"] == "CRS-M1-00826")
    row["generatedSemanticProjectionEn"] = (row.get("generatedSemanticProjectionEn") or "") + " not distinct LSPs"
    errors = baseline.arinc_645_closure_errors(_audit(), crs, _m2())
    assert any("different-LSP identity" in item for item in errors)


def test_645_crc64_check_on_pdf_34_fails() -> None:
    crs = _crs()
    row = next(
        item
        for item in crs["requirements"]
        if str((item.get("semantic") or {}).get("action") or "") in {
            "BIND-CRC-64-CHECK-TO-256-BYTE-VECTOR",
            "BIND-CRC-64-CHECK",
            "BIND-CRC-64-REFIN",
        }
        or "BIND-CRC-64-CHECK" in str((item.get("semantic") or {}).get("action") or "")
        or "BIND-CRC-64-REFIN" in str((item.get("semantic") or {}).get("action") or "")
    )
    row.setdefault("source", {})["pdfPage"] = 34
    errors = baseline.arinc_645_closure_errors(_audit(), crs, _m2())
    assert any("PDF 34" in item for item in errors)


def test_645_front_matter_including_crc_body_fails() -> None:
    audit = _audit()
    source_645 = next(
        item
        for item in audit["supportingSourceApplicabilityAudit"]["sources"]
        if item["sourceId"] == "ARINC-645"
    )
    source_645["pageAccount"]["frontMatterPdfPages"] = [1, 31]
    errors = baseline.arinc_645_closure_errors(audit, _crs(), _m2())
    assert any("front matter" in item for item in errors)
