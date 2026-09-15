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


def m1_package() -> dict:
    return json_load(m1.PACKAGE_PATH)


def m2_package() -> dict:
    return json_load(m2.PACKAGE_PATH)


def json_load(path) -> dict:
    import json

    return json.loads(path.read_text(encoding="utf-8"))


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


def test_legal_expanded_source_bindings_remain_accepted() -> None:
    data = m1_package()
    assert m1_errors(data) == []
    assert req(data, "CRS-M1-00390")["sourceTextHash"] == m1.REGISTERED_FIND_ANSWER_HASH
    assert req(data, "CRS-M1-00520")["sourceTextHash"] == m1.FIND_ANSWER_WINDOW_HASH
    assert req(data, "CRS-M1-00392")["sourceTextHash"] == m1.FIND_INFORMATION_LOCATION_HASH
    assert "CRS-M1-00425" not in {row["id"] for row in data["requirements"]}
    model = m2_package()
    assert m2_errors(model) == []
    assert model["scope"]["services"] == ["UPLOAD", "INFORMATION"]
    assert model["scope"]["afdxSelected"] is False


def test_find_neighbour_identity_swap_fails_after_fingerprint_refresh() -> None:
    data = m1_package()
    window = req(data, "CRS-M1-00520")
    register = req(data, "CRS-M1-00390")
    register["sourceTextHash"] = window["sourceTextHash"]
    register["sourceUnitId"] = window["sourceUnitId"]
    register["semantic"] = copy.deepcopy(window["semantic"])
    register["rhoRA"]["sourceCoverageId"] = "COV-M1-01605"
    refresh_m1(data)
    found = m1_errors(data)
    assert any("register-valid-answers" in item for item in found)

    data = m1_package()
    info = req(data, "CRS-M1-00392")
    info["sourceTextHash"] = m1.REGISTERED_FIND_ANSWER_HASH
    info["semantic"]["objects"] = ["LATE-OR-MISSING-FIND-ANSWER"]
    refresh_m1(data)
    found = m1_errors(data)
    assert any("message-structure or FIND-packet-data" in item or "00392" in item for item in found)


def test_download_field_encoding_repeat_and_sentinel_mutations_fail() -> None:
    data = m1_package()
    req(data, "CRS-M1-00460")["fieldConstraint"]["encodingRule"] = "UNSIGNED-INT-BIG-ENDIAN"
    refresh_m1(data)
    assert any("Protocol Version is not two ASCII characters" in item for item in m1_errors(data))

    data = m1_package()
    req(data, "CRS-M1-00474")["fieldConstraint"]["encodingRule"] = "UNSIGNED-INT-BIG-ENDIAN"
    refresh_m1(data)
    assert any("Download List Ratio is not three ASCII characters" in item for item in m1_errors(data))

    data = m1_package()
    req(data, "CRS-M1-00464")["fieldConstraint"]["repeatScope"] = "PER-FILE-RECORD"
    req(data, "CRS-M1-00465")["fieldConstraint"]["repeatScope"] = "PER-FILE-RECORD"
    refresh_m1(data)
    assert any("cannot repeat per file record" in item for item in m1_errors(data))

    data = m1_package()
    req(data, "CRS-M1-00473")["fieldConstraint"]["specialValues"] = []
    refresh_m1(data)
    assert any("0xFFFF not-given sentinel" in item for item in m1_errors(data))


def test_deleting_root_index_or_header_ownership_fails() -> None:
    for cov_id, rid in (
        ("COV-M1-00739", "CRS-M1-00522"),
        ("COV-M1-00740", "CRS-M1-00523"),
        ("COV-M1-01618", "CRS-M1-00524"),
    ):
        data = m1_package()
        cov(data, cov_id)["requirementIds"] = []
        data["requirements"] = [row for row in data["requirements"] if row["id"] != rid]
        refresh_m1(data)
        found = m1_errors(data)
        assert any(cov_id in item and "lost its CRS owner" in item for item in found), found


def test_may_risk_permission_and_lost_alternative_fail() -> None:
    data = m1_package()
    template = copy.deepcopy(req(data, "CRS-M1-00426"))
    template["id"] = "CRS-M1-00425"
    template["conformanceEffect"] = "OPTIONAL"
    template["semantic"]["action"] = "PERMIT-UNABLE-WRITE-FAILURE"
    data["requirements"].append(template)
    data["requirements"].sort(key=lambda row: row["id"])
    refresh_m1(data)
    assert any("write-failure risk cannot remain a permitted CRS action" in item for item in m1_errors(data))

    data = m1_package()
    req(data, "CRS-M1-00392")["semantic"]["objects"] = ["MESSAGE-STRUCTURE"]
    req(data, "CRS-M1-00392")["conformanceEffect"] = "OPTIONAL"
    refresh_m1(data)
    found = m1_errors(data)
    assert any("alternative" in item or "unconditioned permission" in item for item in found)

    data = m1_package()
    req(data, "CRS-M1-00519")["semantic"]["objects"] = ["ARINC-664-4-ADDRESS-RULES"]
    refresh_m1(data)
    assert any("664P4 or integrator-identified" in item for item in m1_errors(data))


def test_missing_or_swapped_find_timing_fails() -> None:
    data = m1_package()
    req(data, "CRS-M1-00520").pop("timing")
    refresh_m1(data)
    found = m1_errors(data)
    assert any("FIND answer registration window" in item or "window bounds" in item for item in found)

    data = m1_package()
    req(data, "CRS-M1-00520")["timing"]["upperBound"] = 2
    req(data, "CRS-M1-00391")["timing"]["upperBound"] = 3
    refresh_m1(data)
    found = m1_errors(data)
    assert any("0-to-3-second" in item or "0-to-2-second" in item or "same upper bound" in item for item in found)

    data = m1_package()
    req(data, "CRS-M1-00520")["timing"]["timingFamily"] = "FIND-HOST-ANSWER-DEADLINE"
    req(data, "CRS-M1-00391")["timing"]["timingFamily"] = "FIND-ANSWER-REGISTRATION-WINDOW"
    refresh_m1(data)
    found = m1_errors(data)
    assert any("registration window" in item or "host answer deadline" in item for item in found)


def test_chinese_english_action_dump_fails() -> None:
    data = m1_package()
    req(data, "CRS-M1-00498")["generatedSemanticProjectionZh"] = (
        "在实现并使用媒体定义 DOWNLOAD 时，数据加载器协议层必须执行“on accept, TFTP-write LNR to the target”。"
    )
    refresh_m1(data)
    assert any("Chinese view dumps an English action" in item for item in m1_errors(data))


def test_new_scope_cannot_activate_bound_m2_find_download_or_afdx() -> None:
    data = m1_package()
    data["profileScope"]["instanceBoundOperations"] = ["UPLOAD", "INFORMATION", "FIND"]
    refresh_m1(data)
    found = m1_errors(data)
    assert any("instance bound operations" in item or "current instance bound" in item for item in found)

    model = m2_package()
    model["scope"]["services"] = ["UPLOAD", "INFORMATION", "FIND"]
    refresh_m2(model)
    found = m2_errors(model)
    assert any("cannot activate DOWNLOAD, FIND, or AFDX" in item for item in found)

    model = m2_package()
    model["scope"]["afdxSelected"] = True
    refresh_m2(model)
    found = m2_errors(model)
    assert found
    assert any("AFDX" in item or "schema" in item or "False" in item for item in found)

    model = m2_package()
    model["model"]["transitions"][0]["id"] = "T_FIND_IRQ"
    refresh_m2(model)
    found = m2_errors(model)
    assert any("cannot execute FIND or DOWNLOAD" in item for item in found)
