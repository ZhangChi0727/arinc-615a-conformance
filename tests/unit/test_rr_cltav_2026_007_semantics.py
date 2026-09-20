from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
M1_SPEC = importlib.util.spec_from_file_location("sync_m1_crs", ROOT / "scripts/sync_m1_crs.py")
assert M1_SPEC and M1_SPEC.loader
m1 = importlib.util.module_from_spec(M1_SPEC)
M1_SPEC.loader.exec_module(m1)
M2_SPEC = importlib.util.spec_from_file_location("sync_m2_model", ROOT / "scripts/sync_m2_model.py")
assert M2_SPEC and M2_SPEC.loader
m2 = importlib.util.module_from_spec(M2_SPEC)
M2_SPEC.loader.exec_module(m2)


def json_load(path) -> dict:
    import json

    return json.loads(path.read_text(encoding="utf-8"))


def m1_package() -> dict:
    return json_load(m1.PACKAGE_PATH)


def m2_package() -> dict:
    return json_load(m2.PACKAGE_PATH)


def m1_errors(data: dict) -> list[str]:
    return m1.package_errors(data)


def m2_errors(data: dict) -> list[str]:
    return m2.package_errors(data)


def refresh_m1(data: dict) -> None:
    summary = data["inventorySummary"]
    summary.update(
        coverageCount=len(data["coverageLedger"]),
        requirementCount=len(data["requirements"]),
        dependencyCount=len(data["dependencies"]),
        gapCount=len(data["gaps"]),
        coverageFingerprint=m1.fingerprint(data["coverageLedger"]),
        requirementsFingerprint=m1.fingerprint(data["requirements"]),
    )
    data["reviewControl"]["sourceInventoryFingerprint"] = m1.fingerprint(m1.source_inventory_projection(data))


def refresh_m2(data: dict) -> None:
    summary = data["inventorySummary"]
    summary.update(
        requirementCount=len(data["requirementDispositions"]),
        dispositionCount=len(data["requirementDispositions"]),
        traceCount=len(data["traceRelations"]),
        timingCount=len(data["timingCatalog"]),
        dispositionsFingerprint=m2.fingerprint(data["requirementDispositions"]),
        modelFingerprint=m2.fingerprint(data["model"]),
        timingFingerprint=m2.fingerprint(data["timingCatalog"]),
        inputFingerprint=m2.fingerprint(data["inputAcceptance"]),
        actionFingerprint=m2.fingerprint(data["actions"]),
    )


def req(data: dict, rid: str) -> dict:
    return next(row for row in data["requirements"] if row["id"] == rid)


def cov(data: dict, cid: str) -> dict:
    return next(row for row in data["coverageLedger"] if row["id"] == cid)


def catalog(data: dict, rid: str) -> dict:
    return next(row for row in data["timingCatalog"] if row["requirementId"] == rid)


def exact_event_holds(elapsed_s: float, source_constant_s: float) -> bool:
    return elapsed_s == source_constant_s


def host_deadline_holds(elapsed_s: float, upper_s: float) -> bool:
    return 0 <= elapsed_s <= upper_s


def test_legal_window_deadline_and_field_contracts_remain_accepted() -> None:
    data = m1_package()
    assert m1_errors(data) == []
    window = req(data, "CRS-M1-00520")["timing"]
    close = req(data, "CRS-M1-00521")["timing"]
    host = req(data, "CRS-M1-00391")["timing"]
    assert window["intervalRole"] == "EXACT-SOURCE-CONSTANT"
    assert close["intervalRole"] == "EXACT-SOURCE-CONSTANT"
    assert host["intervalRole"] == "DEADLINE-FROM-ZERO-TO-SOURCE-CONSTANT"
    assert not exact_event_holds(1, window["upperBound"])
    assert exact_event_holds(3, close["upperBound"])
    assert host_deadline_holds(1, host["upperBound"])
    assert not host_deadline_holds(2.1, host["upperBound"])
    assert host_deadline_holds(1, host["upperBound"]) and not exact_event_holds(1, window["upperBound"])
    exception = req(data, "CRS-M1-00472")["fieldConstraint"]
    estimated = req(data, "CRS-M1-00473")["fieldConstraint"]
    assert exception["presenceCondition"] == "ALWAYS"
    assert estimated["presenceCondition"] == "ALWAYS"
    assert exception["useCondition"] == "WHEN-STATUS-CODE-0002-OR-0004"
    assert estimated["inactiveRequiredValue"] == "0x0000"
    assert estimated["valueDomain"]["activeMax"] == 32767
    assert cov(data, "COV-M1-00741")["requirementIds"] == ["CRS-M1-00525"]
    model = m2_package()
    assert m2_errors(model) == []
    close_row = catalog(model, "CRS-M1-00521")
    assert close_row["constraintKind"] == "CONSTANT-DEFINITION"
    assert close_row["expression"]["op"] == "EQ"


def test_early_registration_close_and_le3_catalog_fail() -> None:
    data = m1_package()
    req(data, "CRS-M1-00521")["timing"]["lowerBound"] = 0
    req(data, "CRS-M1-00521")["timing"]["upperBound"] = 3
    refresh_m1(data)
    found = m1_errors(data)
    assert any("early-close interval" in item or "RC-FIND-CLOSE-AT-EXPIRY" in item for item in found)

    model = m2_package()
    row = catalog(model, "CRS-M1-00521")
    row["constraintKind"] = "DURATION-UPPER-BOUND"
    row["expression"] = {
        "kind": "COMPARE",
        "op": "LE",
        "left": {"kind": "CLOCK", "name": "CLK_FIND"},
        "right": {"kind": "LITERAL", "value": 3, "unit": "s"},
    }
    refresh_m2(model)
    found = m2_errors(model)
    assert any("early-satisfying upper bound" in item or "not an equality" in item for item in found)


def test_host_deadline_is_not_the_three_second_window() -> None:
    data = m1_package()
    req(data, "CRS-M1-00391")["timing"]["upperBound"] = 3
    refresh_m1(data)
    found = m1_errors(data)
    assert any("RC-FIND-HOST-DEADLINE" in item or "cannot share the same upperBound" in item for item in found)

    data = m1_package()
    req(data, "CRS-M1-00391")["timing"]["lowerBound"] = 2
    req(data, "CRS-M1-00391")["timing"]["upperBound"] = 2
    refresh_m1(data)
    found = m1_errors(data)
    assert any("cannot collapse to an exact arrival time" in item or "RC-FIND-HOST-DEADLINE" in item for item in found)


def test_status_field_omission_and_unconditional_zero_fail() -> None:
    data = m1_package()
    req(data, "CRS-M1-00472")["fieldConstraint"]["presenceCondition"] = "WHEN-STATUS-CODE-0002-OR-0004"
    refresh_m1(data)
    found = m1_errors(data)
    assert any("cannot omit a physically present field" in item or "RC-LNS-EXCEPTION-TIMER" in item for item in found)

    data = m1_package()
    req(data, "CRS-M1-00473")["fieldConstraint"]["specialValues"].append(
        {"code": "0x0000", "meaningCode": "ESTIMATED-TIME-UNUSED-FOR-OTHER-STATUS"}
    )
    refresh_m1(data)
    found = m1_errors(data)
    assert any("unconditional unused sentinel" in item or "UNUSED-FOR-OTHER-STATUS" in item for item in found)

    data = m1_package()
    req(data, "CRS-M1-00473")["fieldConstraint"]["valueDomain"]["activeMax"] = 65535
    refresh_m1(data)
    found = m1_errors(data)
    assert any("activeMax" in item for item in found)


def test_start_at_one_ownership_and_value_mutations_fail() -> None:
    data = m1_package()
    cov(data, "COV-M1-00741")["requirementIds"] = []
    data["requirements"] = [row for row in data["requirements"] if row["id"] != "CRS-M1-00525"]
    refresh_m1(data)
    found = m1_errors(data)
    assert any("COV-M1-00741" in item and "lost its CRS owner" in item for item in found)

    data = m1_package()
    req(data, "CRS-M1-00525")["semantic"]["action"] = "START-DNLD-DATA-NUMBER-AT-TWO"
    refresh_m1(data)
    found = m1_errors(data)
    assert any("RC-DNLD-START-AT-ONE" in item for item in found)


def test_unresolved_note_ref_fails() -> None:
    data = m1_package()
    data["fieldNoteRegistry"] = [row for row in data["fieldNoteRegistry"] if row["id"] != "LNR-FILE-NAME-REPEAT"]
    refresh_m1(data)
    found = m1_errors(data)
    assert any("LNR-FILE-NAME-REPEAT" in item and "fieldNoteRegistry" in item for item in found)
