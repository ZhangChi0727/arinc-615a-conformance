from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("sync_m1_crs", ROOT / "scripts/sync_m1_crs.py")
assert SPEC and SPEC.loader
m1 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m1)


def package() -> dict:
    return json.loads(m1.PACKAGE_PATH.read_text(encoding="utf-8"))


def errors(data: dict) -> list[str]:
    return m1.package_errors(data)


def refresh_summary(data: dict) -> None:
    summary = data["inventorySummary"]
    summary.update(
        coverageCount=len(data["coverageLedger"]),
        requirementCount=len(data["requirements"]),
        dependencyCount=len(data["dependencies"]),
        gapCount=len(data["gaps"]),
        coverageFingerprint=m1.fingerprint(data["coverageLedger"]),
        requirementsFingerprint=m1.fingerprint(data["requirements"]),
    )


def refresh_all_mutable_fingerprints(data: dict) -> None:
    refresh_summary(data)
    data["reviewControl"]["sourceInventoryFingerprint"] = m1.fingerprint(m1.source_inventory_projection(data))


def test_package_is_valid_and_view_is_current() -> None:
    data = package()
    assert errors(data) == []
    assert m1.VIEW_PATH.read_text(encoding="utf-8") == m1.render(data)


def test_every_requirement_exposes_reviewable_semantic_roles() -> None:
    data = package()
    forbidden = {"APPLICABLE-SOURCE-CONDITION", "CAPABILITY-OR-STATE-OBSERVABLE", "SOURCE-DEFINED-ACTION"}
    for row in data["requirements"]:
        semantic = row["semantic"]
        assert semantic["actor"]
        assert semantic["condition"] not in forbidden
        assert semantic["action"] not in forbidden
        assert semantic["objects"] != ["SOURCE-IDENTIFIED-OBJECT"]
        assert semantic["observableEffect"] not in forbidden


def test_deleted_first_middle_or_last_coverage_is_rejected() -> None:
    for index in (0, len(package()["coverageLedger"]) // 2, -1):
        data = package()
        data["coverageLedger"].pop(index)
        assert errors(data)


def test_duplicate_and_reordered_ids_are_rejected() -> None:
    data = package()
    data["coverageLedger"][1]["id"] = data["coverageLedger"][0]["id"]
    assert any("duplicate" in item for item in errors(data))
    data = package()
    data["requirements"][0], data["requirements"][1] = data["requirements"][1], data["requirements"][0]
    assert any("sorted" in item for item in errors(data))


def test_summary_cannot_be_cooperatively_changed_without_fingerprints() -> None:
    data = package()
    data["inventorySummary"]["coverageCount"] -= 1
    assert errors(data)


def test_dangling_requirement_dependency_and_gap_are_rejected() -> None:
    data = package()
    mapped = next(row for row in data["coverageLedger"] if row["requirementIds"])
    mapped["requirementIds"] = ["CRS-MISSING"]
    assert any("dangling requirement" in item for item in errors(data))
    data = package(); data["requirements"][0]["dependencyIds"] = ["DEP-MISSING"]
    assert any("dangling dependency" in item for item in errors(data))
    data = package(); data["requirements"][0]["gapIds"] = ["GAP-MISSING"]
    assert any("dangling gap" in item for item in errors(data))


def test_should_cannot_be_downgraded_and_may_cannot_be_upgraded() -> None:
    data = package()
    should = next(row for row in data["requirements"] if row["sourceModality"] == "SHOULD")
    should["conformanceEffect"] = "INFORMATIVE"; refresh_summary(data)
    assert errors(data)
    data = package()
    may = next(row for row in data["requirements"] if row["sourceModality"] == "MAY")
    may["conformanceEffect"] = "REQUIRED"; refresh_summary(data)
    assert errors(data)


def test_rg0_rg1_and_formal_activation_cannot_be_promoted() -> None:
    for path, value in (("rg0", "APPROVED"), ("rg1", "APPROVED")):
        data = package(); data["reviewControl"][path] = value
        assert errors(data)
    data = package(); data["activation"]["formalApproval"] = "APPROVED"
    assert errors(data)


def test_665_requirement_edges_require_a_matching_auditable_relation() -> None:
    data = package()
    row = next(item for item in data["requirements"] if item.get("triggeredByRequirementIds"))
    row["triggeredByRequirementIds"] = []; refresh_summary(data)
    assert any("trigger relations do not match" in item for item in errors(data))
    data = package()
    row = next(item for item in data["requirements"] if item["source"]["sourceId"] == "ARINC-665-5")
    row["bounded665Decision"] = "EQUIVALENT-TO-665-3"; refresh_summary(data)
    assert any("invalid bounded decision" in item for item in errors(data))


def test_arinc_645_gap_cannot_be_removed_or_promoted() -> None:
    data = package(); data["gaps"] = []; refresh_summary(data)
    assert any("ARINC 645 gap" in item for item in errors(data))
    data = package(); data["gaps"][0]["status"] = "ESTABLISHED"; refresh_summary(data)
    assert any("ARINC 645 gap" in item for item in errors(data))


def test_timing_fields_and_unknown_unbounded_distinction_are_enforced() -> None:
    data = package(); row = next(item for item in data["requirements"] if "timing" in item)
    row["timing"].pop("trigger"); refresh_summary(data)
    assert any("timing fields missing" in item for item in errors(data))


def test_rho_ra_must_close_to_the_mapped_coverage_row() -> None:
    data = package(); data["requirements"][0]["rhoRA"]["sourceCoverageId"] = "COV-MISSING"; refresh_summary(data)
    assert any("rho_RA" in item for item in errors(data))


def test_private_text_paths_and_reversible_payloads_are_rejected() -> None:
    mutations = [
        ("rawSourceText", "proprietary sentence"),
        ("pdfPath", r"C:\\Users\\alice\\standard.pdf"),
        ("payload", "A" * 200),
    ]
    for key, value in mutations:
        data = package(); data["requirements"][0][key] = value; refresh_summary(data)
        assert errors(data)


def test_compound_obligation_requires_inseparable_rationale() -> None:
    data = package(); row = data["requirements"][0]
    row["obligations"] = ["ORDERING", "DIRECTION"]; row.pop("inseparableRationale", None); refresh_summary(data)
    assert any("inseparable rationale" in item for item in errors(data))


def test_open_dependency_cannot_be_closed_without_source_binding() -> None:
    data = package(); dep = next(item for item in data["dependencies"] if item["id"] == "DEP-RFC-1350")
    dep["status"] = "REGISTERED-SUPPORTING-SOURCE"; refresh_summary(data)
    assert any("lacks a controlled source binding" in item for item in errors(data))


def test_coordinated_locator_page_and_hash_forgery_is_stopped_by_rg0_anchor() -> None:
    data = package()
    requirement = data["requirements"][0]
    coverage = next(row for row in data["coverageLedger"] if requirement["id"] in row["requirementIds"])
    for row in (requirement, coverage):
        row["source"]["clause"] = "FORGED-CLAUSE"
        row["source"]["documentPage"] += 1
        row["source"]["pdfPage"] += 1
        row["sourceTextHash"] = "f" * 64
    refresh_all_mutable_fingerprints(data)
    assert any("RG0 anchor sourceInventoryFingerprint" in item for item in errors(data))


def test_coverage_and_requirement_semantics_cannot_diverge() -> None:
    data = package()
    requirement = data["requirements"][0]
    requirement["sourceModality"] = "MAY"
    requirement["conformanceEffect"] = "OPTIONAL"
    refresh_summary(data)
    found = errors(data)
    assert any("disagrees with coverage" in item for item in found)


def test_coordinated_coverage_requirement_deletion_is_stopped_by_rg0_anchor() -> None:
    data = package()
    coverage = next(row for row in data["coverageLedger"] if len(row["requirementIds"]) == 1)
    requirement_id = coverage["requirementIds"][0]
    data["coverageLedger"] = [row for row in data["coverageLedger"] if row["id"] != coverage["id"]]
    data["requirements"] = [row for row in data["requirements"] if row["id"] != requirement_id]
    refresh_all_mutable_fingerprints(data)
    assert any("RG0 anchor" in item for item in errors(data))


def test_arbitrary_timing_added_to_non_timing_source_is_stopped() -> None:
    data = package()
    template = copy.deepcopy(next(row["timing"] for row in data["requirements"] if "timing" in row))
    template.update(provenanceKind="FIXED-SOURCE-CONSTANT", sourceParameter="FORGED-TIMER", lowerBound=0, upperBound=999)
    target = next(row for row in data["requirements"] if "timing" not in row)
    target["timing"] = template
    refresh_summary(data)
    assert any("timingProvenanceFingerprint" in item for item in errors(data))


def test_table_rows_sequence_events_and_dependency_identities_are_anchored() -> None:
    for kind in ("TABLE-ROW", "SEQUENCE-EVENT"):
        data = package()
        index = next(i for i, row in enumerate(data["coverageLedger"]) if row["source"]["fragmentKind"] == kind and not row["requirementIds"])
        data["coverageLedger"].pop(index)
        refresh_all_mutable_fingerprints(data)
        assert any(f"{kind.lower().replace('-', '')}"[:5] in item.lower() or "coverageCount" in item for item in errors(data))
    data = package()
    data["dependencies"][0]["sourceId"] = "RFC-1350-RFC-2347"
    refresh_summary(data)
    assert any("combines multiple source identities" in item for item in errors(data))


def test_cross_reference_cannot_move_a_unit_to_another_clause() -> None:
    data = package()
    coverage = next(row for row in data["coverageLedger"] if row["source"]["pdfPage"] == 94 and row["source"]["clause"] == "6.4.7")
    coverage["source"]["clause"] = "6.4.10"
    for requirement_id in coverage["requirementIds"]:
        data["requirements"][int(requirement_id.rsplit("-", 1)[1]) - 1]["source"]["clause"] = "6.4.10"
    refresh_all_mutable_fingerprints(data)
    assert any("controlled clause page span" in item for item in errors(data))


def test_appendix_namespace_cannot_be_removed() -> None:
    data = package()
    coverage = next(row for row in data["coverageLedger"] if row["source"]["clause"].startswith("A-"))
    coverage["source"]["clause"] = coverage["source"]["clause"].removeprefix("A-")
    refresh_all_mutable_fingerprints(data)
    assert any("controlled namespace APPENDIX-A" in item for item in errors(data))


def test_prose_atomicity_and_table_exclusive_ownership_are_enforced() -> None:
    data = package()
    prose = next(row for row in data["coverageLedger"] if row["source"]["fragmentKind"] == "PROSE-SENTENCE")
    prose["atomicity"]["sentenceCount"] = 2
    refresh_all_mutable_fingerprints(data)
    assert any("exactly one sentence" in item for item in errors(data))
    data = package()
    row = next(item for item in data["coverageLedger"] if item["source"].get("tableOrFigure") == "Table 6.4.10-1")
    row["source"].update(fragmentKind="PROSE-SENTENCE", fragmentOrdinal=4, tableOrFigure=None)
    row["atomicity"].update(ownershipKind="PROSE-SENTENCE", sentenceCount=1)
    refresh_all_mutable_fingerprints(data)
    assert any("prose co-owners" in item for item in errors(data))


def test_generic_semantics_empty_tokens_and_direction_reversal_are_rejected() -> None:
    for field, value in (
        ("condition", "SOURCE-BOUND-OBSERVABLE-TRIGGER"),
        ("action", "SATISFY-"),
        ("objects", ["CLAUSE-SPECIFIC-SUBJECT-MATTER"]),
    ):
        data = package(); row = data["requirements"][0]
        row["semantic"][field] = value; refresh_summary(data)
        assert any("non-reviewable semantic fallback" in item for item in errors(data))
    data = package()
    row = next(item for item in data["requirements"] if item["sourceTextHash"] == "00560acc8acc232b1eb1c81882c7270c775e75b59793df9f3829c7a6a4b838c2")
    row["semantic"]["action"] = "PROHIBIT-COMBINATION"; refresh_summary(data)
    assert any("failed for semantic" in item for item in errors(data))


def test_rg1_assertions_cover_every_requirement_and_bind_polarity() -> None:
    data = package()
    row = next(item for item in data["requirements"] if item["semantic"]["polarity"] == "NEGATIVE")
    row["semantic"]["polarity"] = "AFFIRMATIVE"
    refresh_summary(data)
    assert any("failed for semantic" in item for item in errors(data))


def test_reviewed_checksum_and_non_failure_propositions_cannot_regress() -> None:
    for action in (
        "LOCATE-REQUESTED-FILE-USING-INCLUDED-CRC",
        "RETURN-FILE-CHECKSUM-COMPUTED-BY-INDICATED-ALGORITHM",
        "ACKNOWLEDGE-CHECKSUM-OPTION-IF-ALGORITHM-SUPPORTED",
        "CALCULATE-AND-VALIDATE-RECEIVED-FILE-CHECKSUM",
        "DO-NOT-FAIL-TFTP-TRANSFER-ON-CHECKSUM-VALIDATION-FAILURE",
    ):
        data = package()
        row = next(item for item in data["requirements"] if item["semantic"]["action"] == action)
        row["semantic"]["action"] = "USE-CRC"
        refresh_summary(data)
        assert any("failed for semantic" in item for item in errors(data))


def test_reviewed_timing_equations_cannot_be_relabelled_or_dropped() -> None:
    data = package()
    row = next(item for item in data["requirements"] if item.get("timing", {}).get("sourceParameter") == "TFTP-TO-DIVIDED-BY-2")
    row["timing"]["sourceRelation"] = "TFTP-PACKET-ANSWER-DEADLINE"
    refresh_summary(data)
    assert any("failed for timing" in item for item in errors(data))
    data = package()
    row = next(item for item in data["requirements"] if item.get("timing", {}).get("sourceParameter") == "DLP-TO-EQUATION")
    row.pop("timing")
    refresh_summary(data)
    assert any("failed for timing" in item for item in errors(data))


def test_timing_semantics_cannot_collapse_to_one_placeholder_tuple() -> None:
    data = package()
    template = copy.deepcopy(next(row["timing"] for row in data["requirements"] if "timing" in row))
    for row in data["requirements"]:
        if "timing" in row:
            row["timing"].update({key: template[key] for key in ("timingFamily", "trigger", "response", "cancellation", "supersedingTrigger", "correlationKey", "pairingPolicy")})
    refresh_summary(data)
    assert any("generic shared event semantics" in item for item in errors(data))


def test_665_profile_scope_and_requirement_edges_are_distinct() -> None:
    data = package()
    row = next(row for row in data["requirements"] if row.get("triggerRelations"))
    row["triggerRelations"][0]["rationaleCode"] = "SHARED-NONEXISTENT-OBJECT"
    refresh_summary(data)
    assert any("unsupported requirement-level trigger rationale" in item for item in errors(data))
    data = package(); row = next(item for item in data["requirements"] if item["source"]["sourceId"] == "ARINC-665-5")
    row["profileScopeTriggerIds"] = row["profileScopeTriggerIds"][:1]; refresh_summary(data)
    assert any("profile-scope trigger set" in item for item in errors(data))


def test_profile_scope_cannot_change_the_controlled_m1_operations() -> None:
    data = package()
    data["profileScope"]["baseOperation"] = "DOWNLOAD"
    refresh_summary(data)
    assert any("baseOperation must remain UPLOAD" in item for item in errors(data))
    data = package()
    data["profileScope"]["extraField"] = "SILENT-SCOPE-CHANGE"
    refresh_summary(data)
    assert any("only the controlled M1 scope fields" in item for item in errors(data))


def test_source_bindings_must_match_the_controlled_register() -> None:
    data = package()
    binding = next(item for item in data["sourceBindings"] if item["sourceId"] == "ARINC-615A-3")
    binding["sha256"] = "0" * 64
    refresh_summary(data)
    assert any("sha256 disagrees with the controlled register" in item for item in errors(data))
    data = package()
    binding = next(item for item in data["sourceBindings"] if item["sourceId"] == "ARINC-615A-3")
    binding["role"] = "HISTORICAL-SUPERSEDED"
    refresh_summary(data)
    assert any("role disagrees with the controlled register" in item for item in errors(data))
    data = package()
    data["sourceBindings"].append({"sourceId": "RFC-1350", "role": "OPEN-DEPENDENCY", "sha256": "a" * 64})
    refresh_summary(data)
    assert any("is not in the controlled register" in item for item in errors(data))


def test_rhora_must_remain_a_closed_candidate_binding() -> None:
    data = package()
    data["requirements"][0]["rhoRA"]["transcription"] = "proprietary sentence"
    refresh_summary(data)
    assert any("rhoRA is not a closed candidate binding" in item for item in errors(data))


def test_generic_observable_effect_is_rejected() -> None:
    data = package()
    data["requirements"][0]["semantic"]["observableEffect"] = "STATE-OR-ENCODING-OUTCOME-OBSERVABLE"
    refresh_summary(data)
    assert any("generic observableEffect" in item for item in errors(data))


def test_draft_merge_evidence_cannot_be_manufactured() -> None:
    data = package()
    data["activation"]["mergeEvidence"] = "ORDINARY-TWO-PARENT-MERGE"
    refresh_summary(data)
    assert any("merge evidence must remain absent" in item for item in errors(data))


def test_registered_pdf_pages_are_accounted_by_span_or_exclusion() -> None:
    register = json.loads((ROOT / "configs/research/controlled_sources.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "configs/requirements/m1_source_section_spans.json").read_text(encoding="utf-8"))
    assert m1.page_account_errors(manifest, register) == []
    broken = json.loads(json.dumps(manifest))
    broken["excludedRanges"][0]["pdfPages"] = [1, 11]
    assert any("incomplete" in item for item in m1.page_account_errors(broken, register))
    overlap = json.loads(json.dumps(manifest))
    overlap["excludedRanges"][0]["pdfPages"] = [1, 13]
    assert any("overlaps" in item for item in m1.page_account_errors(overlap, register))


def test_structured_status_meaning_display_and_footnote_are_anchored() -> None:
    data = package()
    row = next(item for item in data["requirements"] if item.get("statusTableConstraint", {}).get("kind") == "STATUS-CODE")
    row["statusTableConstraint"]["meaningCode"] = "REVERSED-MEANING"
    refresh_summary(data)
    assert any("statusTableFingerprint" in item for item in errors(data))
    data = package()
    footnote = next(item for item in data["requirements"] if item.get("statusTableConstraint", {}).get("kind") == "DISPLAY-FOOTNOTE")
    coverage_id = footnote["rhoRA"]["sourceCoverageId"]
    data["requirements"] = [item for item in data["requirements"] if item["id"] != footnote["id"]]
    next(item for item in data["coverageLedger"] if item["id"] == coverage_id)["requirementIds"] = []
    refresh_all_mutable_fingerprints(data)
    assert any("statusTableFingerprint" in item for item in errors(data))
