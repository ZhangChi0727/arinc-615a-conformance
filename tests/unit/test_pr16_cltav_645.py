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


def test_645_leaves_are_atomic_and_capability_open() -> None:
    crs = _crs()
    audit = _audit()
    bound = audit["boundPackage"]
    assert crs["artifactVersion"] == bound["artifactVersion"]
    assert crs["artifactVersion"].startswith("M1-CANDIDATE-")
    assert len(crs["coverageLedger"]) == bound["coverageCount"]
    assert len(crs["requirements"]) == bound["requirementCount"]
    rows_645 = [row for row in crs["requirements"] if row["source"]["sourceId"] == "ARINC-645"]
    ids = [row["id"] for row in rows_645]
    assert ids == sorted(set(ids))
    assert len(ids) >= 39
    actions = {str((row.get("semantic") or {}).get("action") or "") for row in rows_645}
    for action in (
        "BIND-CRC-TRANSMISSION-BIT-REFLECTION",
        "PAD-SHORT-INPUT-TO-CRC-REGISTER-SIZE",
        "INCLUDE-NECESSARY-DATA-FOR-EACH-LOADING-INTERFACE",
    ):
        assert action in actions
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
    row_544 = next(row for row in crs["requirements"] if row["id"] == "CRS-M1-00544")
    assert "blocked by ARINC 645" not in row_544["generatedSemanticProjectionEn"]
    assert "CRS-M1-00819" in row_544["generatedSemanticProjectionEn"]


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


def test_645_crc_file_byte_order_is_a_dedicated_triggered_leaf() -> None:
    crs = _crs()
    audit = _audit()
    row = next(item for item in crs["requirements"] if item["id"] == "CRS-M1-00864")
    assert row["source"]["clause"] == "4.3.2"
    assert row["source"]["pdfPage"] == 30
    assert row["semantic"]["action"] == "PROCESS-CRC-FILE-BYTES-IN-OCCURRENCE-ORDER"
    assert row["semantic"]["objects"] == ["CRC", "FILE-BYTE-SEQUENCE"]
    assert "check-value byte order" in row["generatedSemanticProjectionEn"]
    assert "校验值的字节序" in row["generatedSemanticProjectionZh"]
    source_645 = next(
        item for item in audit["supportingSourceApplicabilityAudit"]["sources"]
        if item["sourceId"] == "ARINC-645"
    )
    unit = next(item for item in source_645["units"] if item["id"] == "SAU-645-4-3-2-FILE-BYTE-ORDER")
    assert unit["leafRequirementIds"] == ["CRS-M1-00864"]


def test_645_crc_variants_cannot_be_reintroduced_as_universal_obligations() -> None:
    crs = _crs()
    audit = _audit()
    for req_id in ("CRS-M1-00860", "CRS-M1-00862"):
        row = next(item for item in crs["requirements"] if item["id"] == req_id)
        assert row["conformanceEffect"] == "INFORMATIVE"
        assert row["semantic"]["condition"] != "WHEN-615A-INTEGRITY-REQUIRES-A-645-CRC"
    changed = copy.deepcopy(crs)
    row = next(item for item in changed["requirements"] if item["id"] == "CRS-M1-00860")
    row["conformanceEffect"] = "CONDITIONAL-REQUIRED"
    row["semantic"]["condition"] = "WHEN-615A-INTEGRITY-REQUIRES-A-645-CRC"
    _refresh_crs(changed)
    assert any("universal" in item for item in baseline.arinc_645_closure_errors(audit, changed, _m2()))


def test_645_check_value_commentary_zh_continues_after_the_check_value() -> None:
    row = next(item for item in _crs()["requirements"] if item["id"] == "CRS-M1-00838")
    zh = row["generatedSemanticProjectionZh"]
    assert "越过该校验值" in zh
    assert "继续处理其后的数据字段" in zh
    assert "校验值后面的数据字段" not in zh


def test_645_pdf30_adjacent_crc_clauses_have_explicit_non_obligation_dispositions() -> None:
    audit = _audit()
    source_645 = next(
        item for item in audit["supportingSourceApplicabilityAudit"]["sources"]
        if item["sourceId"] == "ARINC-645"
    )
    units = {item["id"]: item for item in source_645["units"]}
    assert units["SAU-645-BODY-PRE"]["clause"] == "1-4.2"
    assert units["SAU-645-BODY-PRE"]["pdfPages"] == [7, 29]
    for unit_id, clause in (
        ("SAU-645-4-3-1-CRC-DEFINITION", "4.3.1"),
        ("SAU-645-4-3-2-1-BIT-ORDERING", "4.3.2.1"),
        ("SAU-645-4-3-2-2-BIT-SHIFTING", "4.3.2.2"),
    ):
        unit = units[unit_id]
        assert unit["clause"] == clause
        assert unit["pdfPages"] == [30, 30]
        assert unit["applicabilityDecision"] == "OUT-OF-PROFILE"
        assert unit["conformanceEffect"] == "INFORMATIVE"
        assert unit["leafCrsStatus"] == "NOT-REQUIRED"


def test_645_pdf30_clause_dispositions_are_fail_closed() -> None:
    audit = _audit()
    crs = _crs()
    source_645 = next(
        item for item in audit["supportingSourceApplicabilityAudit"]["sources"]
        if item["sourceId"] == "ARINC-645"
    )
    source_645["units"] = [
        item for item in source_645["units"]
        if item["id"] != "SAU-645-4-3-2-1-BIT-ORDERING"
    ]
    assert any("4.3.2.1" in item for item in baseline.arinc_645_closure_errors(audit, crs, _m2()))


ALG_DIR = ROOT / "docs/research/publication/algorithms"
ALG_MODULE_FILES = {
    "ALG-CLTAV-01": "ALG-CLTAV-01.tex",
    "ALG-CLTAV-05": "ALG-CLTAV-05-selection.tex",
    "ALG-CLTAV-06": "ALG-CLTAV-06-timing.tex",
    "ALG-CLTAV-07": "ALG-CLTAV-07-history.tex",
    "ALG-CLTAV-02": "ALG-CLTAV-02.tex",
    "ALG-CLTAV-03": "ALG-CLTAV-03.tex",
    "ALG-CLTAV-04": "ALG-CLTAV-04.tex",
    "ALG-CLTAV-APPENDIX": "CLTAV_ALGORITHM_APPENDIX.tex",
}


def _algorithms(overrides: dict[str, str] | None = None) -> dict[str, str]:
    overrides = overrides or {}
    return {
        module: overrides.get(module, (ALG_DIR / name).read_text(encoding="utf-8"))
        for module, name in ALG_MODULE_FILES.items()
    }


def _corpus(overrides: dict[str, str] | None = None) -> str:
    return "\n".join(_algorithms(overrides).values())


def _contract(registry=None, puml=None, plan=None, alg=None, overrides=None):
    merged = dict(overrides or {})
    if alg is not None:
        merged["ALG-CLTAV-01"] = alg
    return baseline.cltav_algorithm_contract_errors(
        _algorithms(merged),
        puml if puml is not None else PUML_PATH.read_text(encoding="utf-8"),
        plan if plan is not None else EXP_PLAN.read_text(encoding="utf-8"),
        registry,
    )


def _effect_errors(registry: dict, overrides: dict[str, str] | None = None, main_override=None) -> list[str]:
    algorithms = _algorithms(overrides)
    corpus = "\n".join(algorithms.values())
    main_text = main_override if main_override is not None else algorithms["ALG-CLTAV-01"]
    return baseline._algorithm_effect_errors(
        corpus, registry["dataflow"], registry["interfaces"],
        registry["sessionHandles"]["SessionContext"], main_algorithm=main_text,
    )


def test_nonexistent_dataflow_port_is_rejected() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["dataflow"][0]["output"] = "NONEXISTENT"
    errors = _contract(registry)
    assert any("NONEXISTENT" in item and "port" in item for item in errors)


def test_truth_to_select_is_rejected() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["recordFlowWalkthroughs"][0]["truthToSelect"] = True
    errors = _contract(registry)
    assert any("truthToSelect" in item for item in errors)


def test_duplicate_experiment_interface_id_is_rejected() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["experimentInterfaces"].append(copy.deepcopy(registry["experimentInterfaces"][0]))
    errors = _contract(registry)
    assert any("duplicate interface ids" in item for item in errors)


def test_undeclared_walk_path_is_rejected() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["recordFlowWalkthroughs"][0]["path"] = ["IF-UNDECLARED"]
    errors = _contract(registry)
    assert any("IF-UNDECLARED" in item for item in errors)


def test_missing_walk_records_are_rejected() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["recordFlowWalkthroughs"][0].pop("records", None)
    errors = _contract(registry)
    assert any("typed records" in item for item in errors)


def test_owned_algorithm_pdf_is_allowed_on_pr_changed_set() -> None:
    changed = baseline.changed_files_for_event({"artifacts/publications/cltav/ALG-CLTAV-01.pdf"})
    errors = baseline.prohibited_source_artifact_errors(changed)
    assert errors == []


def test_unregistered_and_source_pdfs_are_rejected_on_pr_changed_set() -> None:
    changed = baseline.changed_files_for_event({
        "artifacts/publications/cltav/UNREGISTERED.pdf",
        "local-references/ARINC 645-1 2021.pdf",
        "tmp/out-of-tree.pdf",
    })
    errors = baseline.prohibited_source_artifact_errors(changed)
    assert any("UNREGISTERED.pdf" in item for item in errors)
    assert any("local-references" in item for item in errors)
    assert any("tmp/out-of-tree.pdf" in item for item in errors)


def _effect_q(q: str, effect: str, *, prep_err: bool = False, unconfirmed: bool = False) -> str:
    """Branch order of the delivered S7 text: invalidate, then not-sent, then unconfirmed."""
    if prep_err or effect == "UNKNOWN-EFFECT":
        return "UNKNOWN"
    if effect == "CONFIRMED-NOT-SENT":
        return q
    if unconfirmed:
        return "UNKNOWN"
    return q


def test_delivered_s_steps_keep_snapshot_and_effect_classes() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    assert _effect_errors(registry) == []
    body = _corpus()
    assert r"\mathrm{effect}=\texttt{UNKNOWN-EFFECT}" in body
    assert r"\texttt{CONFIRMED-NOT-SENT}$}" in body
    assert "stays UNKNOWN" in body
    assert _effect_q("KNOWN", "CONFIRMED-NOT-SENT") == "KNOWN"
    assert _effect_q("UNKNOWN", "NONE", unconfirmed=True) == "UNKNOWN"
    assert _effect_q("KNOWN", "UNKNOWN-EFFECT") == "UNKNOWN"
    import re
    hist_match = re.search(r"\\IFhist\$\((.*?)\)\$", body, re.S)
    hist = hist_match.group(1) if hist_match else ""
    assert "qUsedAtSelect" in hist and "postSummary" in hist and "qStatus" not in hist
    assert "sole writer" in body
    method = METHOD_REPORT.read_text(encoding="utf-8")
    for token in (
        "KNOWN, confirmed not sent, retry remains",
        "snapshot UNKNOWN and new target both visible",
        "qUsedAtSelect` kept",
        "next read is not the old KNOWN",
        "S7, not S8",
        "Executed observation leaves",
        "KNOWN 且确认未发送",
        "快照 UNKNOWN 与新目标同时可见",
        "执行后观测使",
    ):
        assert token in method


def test_successor_summary_and_final_action_contracts_are_enforced() -> None:
    """R29: next iteration consumes confirmed q1; snapshot names the executed final action."""
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    assert _effect_errors(registry) == []
    main = _algorithms()["ALG-CLTAV-01"]
    alg07 = _algorithms()["ALG-CLTAV-07"]
    corpus = _corpus()
    assert "one-step minimax" in corpus
    assert main.find("SelectAndAdmit") < main.find("actionId")
    assert main.find("actionId") < main.find("ExecuteAndRecord")
    assert r"\IFexec" in corpus
    assert r"\Gamma'.\mathrm{currentSummary}\leftarrow z.\mathrm{postSummary}" in alg07
    assert "confirmed Prep with no valid Iz advances operation history and preserves H" in json.dumps(registry)
    assert "summaryConfirmed=false with UNKNOWN-EFFECT rather than retaining a stale known summary" in json.dumps(registry)

    deleted_commit = alg07.replace(r"\Gamma'.\mathrm{currentSummary}\leftarrow z.\mathrm{postSummary}", "", 1)
    errors = _contract(overrides={"ALG-CLTAV-07": deleted_commit})
    assert any("S9 must commit currentSummary" in item for item in errors)
    inverted_guard = alg07.replace(
        r"$z.\mathrm{summaryConfirmed}$ is true",
        r"$z.\mathrm{summaryConfirmed}$ is false",
        1,
    )
    errors = _contract(overrides={"ALG-CLTAV-07": inverted_guard})
    assert any("S9 must commit currentSummary" in item for item in errors)

    stale = copy.deepcopy(registry)
    stale["dataflow"] = [
        edge for edge in stale["dataflow"]
        if not (edge.get("from") == "IF-OBS-INTERPRET" and edge.get("to") == "SessionContext")
    ]
    errors = _contract(stale)
    assert any("IF-OBS-INTERPRET postSummary" in item for item in errors)

    early_snapshot = main.replace("SelectAndAdmit", "actionId SelectAndAdmit", 1)
    errors = _effect_errors(registry, main_override=early_snapshot)
    assert any("actionId" in item for item in errors)


def test_unconfirmed_prep_successor_is_not_allowed_to_retain_known_summary() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    prep_escape = "($z.\\mathrm{kind}$ is Prep and $z.\\mathrm{prepResultEvaluated}$ and $z.\\mathrm{summaryConfirmed}$ is false)"
    corpus = _corpus()
    assert prep_escape in corpus
    assert "clear $\\Gamma.\\mathrm{currentSummary}$" in corpus
    prep = next(row for row in registry["interfaces"] if row["id"] == "IF-PREP-RECOVER")
    assert {"targetConfirmed", "summaryConfirmed", "postSummary"}.issubset(prep["outputs"])
    assert "targetConfirmed=false may coexist with summaryConfirmed=true for Prep" in prep["guarantee"]

    escaping = _algorithms()["ALG-CLTAV-04"].replace(prep_escape, r"\textit{false}")
    errors = _contract(overrides={"ALG-CLTAV-04": escaping})
    assert any("unconfirmed Prep successor summary" in item for item in errors)

    ambiguous = copy.deepcopy(registry)
    prep = next(row for row in ambiguous["interfaces"] if row["id"] == "IF-PREP-RECOVER")
    prep["outputs"].remove("summaryConfirmed")
    errors = _contract(ambiguous)
    assert any("targetConfirmed" in item and "summaryConfirmed" in item for item in errors)


def test_test_summary_and_confirmed_not_sent_prep_control_paths_are_enforced() -> None:
    """R31: TEST binds q1; not-sent Prep cannot turn default false into UNKNOWN."""
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    assert _effect_errors(registry) == []
    corpus = _corpus()
    alg03 = _algorithms()["ALG-CLTAV-03"]
    assert r"z.\mathrm{summaryConfirmed}\leftarrow\textbf{true}" in alg03
    assert "CONFIRMED-NOT-SENT" in corpus and "prepResultEvaluated" in corpus

    unbound_test = alg03.replace(r"z.\mathrm{summaryConfirmed}\leftarrow\textbf{true}", r"z.I_z\leftarrow\textbf{true}", 1)
    errors = _contract(overrides={"ALG-CLTAV-03": unbound_test})
    assert errors

    not_sent_invalidated = _algorithms()["ALG-CLTAV-04"].replace(
        r"$z.\mathrm{prepResultEvaluated}$ and $z.\mathrm{summaryConfirmed}$ is false",
        r"$z.\mathrm{summaryConfirmed}$ is false",
    )
    errors = _contract(overrides={"ALG-CLTAV-04": not_sent_invalidated})
    assert any("unconfirmed Prep successor summary" in item for item in errors)


def _summary_path(
    kind: str, effect: str, current: str, *, obs_summary: str | None = None,
    prep_evaluated: bool = False, prep_summary: str | None = None, target_confirmed: bool = False,
) -> tuple[str, str | None, int, str]:
    """Bounded R31 decision table for the delivered S6--S9 control contract."""
    if effect == "CONFIRMED-NOT-SENT":
        return "KNOWN", current, 1, "unchanged"
    if effect == "UNKNOWN-EFFECT":
        return "UNKNOWN", None, 1, "conservative-unknown"
    summary = prep_summary if prep_evaluated else obs_summary
    if kind == "PREP" and prep_evaluated and summary is None:
        return "UNKNOWN", None, 1, "conservative-unknown"
    if kind == "RECOVER" and prep_evaluated and not target_confirmed:
        return "UNKNOWN", None, 1, "conservative-unknown"
    if kind == "RECOVER":
        return "KNOWN", summary, 0, "snapshot-history"
    return "KNOWN", summary, 0, "snapshot-history"


def test_r31_cross_path_acceptance_matrix() -> None:
    """Normal TEST commits q1; Prep not-sent preserves q0; failed confirmation cannot leak q0."""
    assert _summary_path("TEST", "NONE", "q0", obs_summary="q1") == ("KNOWN", "q1", 0, "snapshot-history")
    assert _summary_path("TEST", "UNKNOWN-EFFECT", "q0") == ("UNKNOWN", None, 1, "conservative-unknown")
    assert _summary_path("PREP", "CONFIRMED-NOT-SENT", "q0") == ("KNOWN", "q0", 1, "unchanged")
    assert _summary_path("PREP", "NONE", "q0", prep_evaluated=True) == ("UNKNOWN", None, 1, "conservative-unknown")
    assert _summary_path("PREP", "NONE", "q0", prep_evaluated=True, prep_summary="q0") == ("KNOWN", "q0", 0, "snapshot-history")
    assert _summary_path("RECOVER", "NONE", "q0", prep_evaluated=True, prep_summary="q1") == ("UNKNOWN", None, 1, "conservative-unknown")
    assert _summary_path("RECOVER", "NONE", "q0", prep_evaluated=True, prep_summary="q1", target_confirmed=True) == ("KNOWN", "q1", 0, "snapshot-history")


def _fig05():
    graphs = json.loads((ROOT / "configs/research/cltav_figure_graphs.json").read_text(encoding="utf-8"))
    figure = graphs["figures"]["FIG-CL-TAV-05-closed-loop-activity.svg"]
    svg = (ROOT / "artifacts/publications/cltav/figures/FIG-CL-TAV-05-closed-loop-activity.svg").read_text(encoding="utf-8")
    import xml.etree.ElementTree as ET
    root = ET.fromstring(svg)
    pairs = {(src, dst) for src, dst, *_ in baseline._svg_labeled_edges(root)}
    return figure, pairs, root


def test_fig05_normal_continue_reaches_next_s1() -> None:
    figure, pairs, root = _fig05()
    assert baseline._figure05_control_errors(figure, pairs, root) == []
    assert ("S9", "S10") in pairs and ("S10", "S1") in pairs
    assert ("S7", "LoopS1") in pairs


def test_fig05_rejects_missing_continue_changed_endpoint_and_inverted_guard() -> None:
    figure, pairs, root = _fig05()
    missing = copy.deepcopy(figure)
    missing["edges"] = [row for row in missing["edges"] if row.get("id") != "E-S10-S1"]
    missing_pairs = pairs - {("S10", "S1")}
    errors = baseline._figure05_control_errors(missing, missing_pairs, root)
    assert any("S10->S1" in item or "S10" in item and "S1" in item for item in errors)
    moved = copy.deepcopy(figure)
    for row in moved["edges"]:
        if row.get("id") == "E-S10-S1":
            row["to"] = "S2"
    moved_pairs = (pairs - {("S10", "S1")}) | {("S10", "S2")}
    errors = baseline._figure05_control_errors(moved, moved_pairs, root)
    assert any("S10->S1" in item for item in errors)
    inverted = copy.deepcopy(figure)
    for row in inverted["edges"]:
        if row.get("id") == "E-S10-S1":
            row["polarity"] = "stop"
    errors = baseline._figure05_control_errors(inverted, pairs, root)
    assert any("polarity inverted" in item for item in errors)


def _owned_row(path: str, sources: list[str]) -> dict:
    return {
        "path": path,
        "kind": "OWNED-GENERATED-PUBLICATION",
        "trackedSources": sources,
        "generator": "XeLaTeX via ALG-CLTAV-01-wrapper.tex",
        "notProprietarySource": True,
        "safetyCheck": "typeset algorithm form",
    }


def test_owned_pdf_registration_fail_closed(tmp_path: Path) -> None:
    owned = json.loads((ROOT / "configs/research/cltav_owned_generated_artifacts.json").read_text(encoding="utf-8"))
    dropped = copy.deepcopy(owned)
    dropped["artifacts"][0].pop("trackedSources")
    dropped["artifacts"][0].pop("generator")
    errors = baseline.prohibited_source_artifact_errors(
        {"artifacts/publications/cltav/ALG-CLTAV-01.pdf"},
        registry=dropped,
    )
    assert any("trackedSources" in item or "generator" in item for item in errors)
    errors = baseline.prohibited_source_artifact_errors(
        {"docs/source-copy.pdf"},
        registry={"artifacts": [{"path": "docs/source-copy.pdf", "notProprietarySource": True}]},
    )
    assert errors
    pub = tmp_path / "artifacts/publications/cltav"
    src = tmp_path / "docs/research/publication/algorithms"
    pub.mkdir(parents=True)
    src.mkdir(parents=True)
    pdf = pub / "owned.pdf"
    tex = src / "ALG.tex"
    pdf.write_bytes(b"%PDF-1.4\n")
    tex.write_text("algorithm\n", encoding="utf-8")
    rel_pdf = "artifacts/publications/cltav/owned.pdf"
    rel_tex = "docs/research/publication/algorithms/ALG.tex"
    good = {"artifacts": [_owned_row(rel_pdf, [rel_tex])]}
    assert baseline.prohibited_source_artifact_errors(
        {rel_pdf}, registry=good, root=tmp_path, tracked_paths={rel_pdf, rel_tex},
    ) == []
    assert baseline.prohibited_source_artifact_errors(
        {rel_pdf}, registry=good, root=tmp_path, tracked_paths={rel_pdf},
    )
    fake = {"artifacts": [_owned_row(rel_pdf, ["docs/missing.tex"])]}
    assert any("ordinary file" in item or "tracked" in item for item in baseline.prohibited_source_artifact_errors(
        {rel_pdf}, registry=fake, root=tmp_path, tracked_paths={rel_pdf, "docs/missing.tex"},
    ))
    outside = {"artifacts": [_owned_row("docs/source-copy.pdf", [rel_tex])]}
    (tmp_path / "docs").mkdir(exist_ok=True)
    (tmp_path / "docs/source-copy.pdf").write_bytes(b"%PDF-1.4\n")
    assert any("PDF under" in item for item in baseline.prohibited_source_artifact_errors(
        {"docs/source-copy.pdf"},
        registry=outside,
        root=tmp_path,
        tracked_paths={"docs/source-copy.pdf", rel_tex},
    ))
    escaped = {"artifacts": [_owned_row("artifacts/publications/../owned.pdf", [rel_tex])]}
    assert any("traversal" in item or "PDF under" in item for item in baseline.prohibited_source_artifact_errors(
        set(), registry=escaped, root=tmp_path, tracked_paths={rel_tex},
    ))
    absolute = {"artifacts": [_owned_row(str(pdf), [rel_tex])]}
    assert any("repository-relative" in item for item in baseline.prohibited_source_artifact_errors(
        set(), registry=absolute, root=tmp_path, tracked_paths={rel_tex},
    ))
    secret = tmp_path / "local-references"
    secret.mkdir()
    (secret / "note.tex").write_text("source\n", encoding="utf-8")
    proprietary = {"artifacts": [_owned_row(rel_pdf, ["local-references/note.tex"])]}
    assert any("prohibited" in item or "traversal" in item or "ordinary file" in item for item in baseline.prohibited_source_artifact_errors(
        {rel_pdf},
        registry=proprietary,
        root=tmp_path,
        tracked_paths={rel_pdf, "local-references/note.tex"},
    ))


def test_owned_pdf_registration_rejects_symlink_escape(tmp_path: Path) -> None:
    pub = tmp_path / "artifacts/publications/cltav"
    src = tmp_path / "docs/research/publication/algorithms"
    pub.mkdir(parents=True)
    src.mkdir(parents=True)
    pdf = pub / "owned.pdf"
    tex = src / "ALG.tex"
    pdf.write_bytes(b"%PDF-1.4\n")
    tex.write_text("algorithm\n", encoding="utf-8")
    rel_tex = "docs/research/publication/algorithms/ALG.tex"
    link_rel = "artifacts/publications/cltav/escape.pdf"
    link = tmp_path / link_rel
    try:
        link.symlink_to(pdf)
    except OSError:
        pytest.skip("symbolic-link creation is unavailable on this host")
    linked = {"artifacts": [_owned_row(link_rel, [rel_tex])]}
    assert any("symbolic link" in item for item in baseline.prohibited_source_artifact_errors(
        {link_rel},
        registry=linked,
        root=tmp_path,
        tracked_paths={link_rel, rel_tex},
    ))


# ---------------------------------------------------------------------------
# F-B: persisted source-disposition regression matrix for the PDF-30 adjacent
# CRC clauses. Every negative exercises the production governance entry
# (baseline.governed_source_errors) that check_repo_baseline.main() invokes.
# ---------------------------------------------------------------------------
PDF30_ADJACENT_UNITS = (
    "SAU-645-4-3-1-CRC-DEFINITION",
    "SAU-645-4-3-2-1-BIT-ORDERING",
    "SAU-645-4-3-2-2-BIT-SHIFTING",
)


def _arinc645_source(audit: dict) -> dict:
    return next(
        item
        for item in audit["supportingSourceApplicabilityAudit"]["sources"]
        if item["sourceId"] == "ARINC-645"
    )


def test_645_pdf30_adjacent_units_pass_at_head() -> None:
    assert baseline.governed_source_errors(_audit(), _crs(), _m2()) == []


def test_645_pdf30_units_remain_informative_not_universal_must() -> None:
    source_645 = _arinc645_source(_audit())
    for unit_id in PDF30_ADJACENT_UNITS:
        unit = next(item for item in source_645["units"] if item["id"] == unit_id)
        assert unit["applicabilityDecision"] == "OUT-OF-PROFILE"
        assert unit["conformanceEffect"] == "INFORMATIVE"
        assert unit["leafCrsStatus"] == "NOT-REQUIRED"
    assert baseline.governed_source_errors(_audit(), _crs(), _m2()) == []


@pytest.mark.parametrize("unit_id", PDF30_ADJACENT_UNITS)
def test_645_pdf30_unit_deletion_is_rejected(unit_id: str) -> None:
    audit = _audit()
    source_645 = _arinc645_source(audit)
    source_645["units"] = [item for item in source_645["units"] if item["id"] != unit_id]
    errors = baseline.governed_source_errors(audit, _crs(), _m2())
    assert any("explicit non-obligation disposition" in item for item in errors)


@pytest.mark.parametrize("unit_id", PDF30_ADJACENT_UNITS)
def test_645_pdf30_unit_page_mislocation_is_rejected(unit_id: str) -> None:
    audit = _audit()
    source_645 = _arinc645_source(audit)
    unit = next(item for item in source_645["units"] if item["id"] == unit_id)
    unit["pdfPages"] = [29, 29]
    errors = baseline.governed_source_errors(audit, _crs(), _m2())
    assert any("explicit non-obligation disposition" in item for item in errors)


def test_645_prebody_absorbing_crc_definition_is_rejected() -> None:
    for mutate in (
        lambda unit: unit.update(pdfPages=[7, 30]),
        lambda unit: unit.update(clause="1-4.3.1"),
    ):
        audit = _audit()
        source_645 = _arinc645_source(audit)
        pre = next(item for item in source_645["units"] if item["id"] == "SAU-645-BODY-PRE")
        mutate(pre)
        errors = baseline.governed_source_errors(audit, _crs(), _m2())
        assert any("untriggered pre-body must end" in item for item in errors)


def test_645_surveyed_page_without_clause_disposition_is_rejected() -> None:
    audit = _audit()
    source_645 = _arinc645_source(audit)
    assert 30 in source_645["pageAccount"]["surveyedPdfPages"]
    source_645["units"] = [
        item for item in source_645["units"] if item["id"] not in PDF30_ADJACENT_UNITS
    ]
    errors = baseline.governed_source_errors(audit, _crs(), _m2())
    assert any("explicit non-obligation disposition" in item for item in errors)
