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


def test_665_rows_require_a_615a3_trigger_and_bounded_decision() -> None:
    data = package()
    row = next(item for item in data["requirements"] if item["source"]["sourceId"] == "ARINC-665-5")
    row["triggeredByRequirementIds"] = []; refresh_summary(data)
    assert any("lacks a 615A-3 trigger" in item for item in errors(data))
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
