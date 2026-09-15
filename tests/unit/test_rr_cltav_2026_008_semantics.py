from __future__ import annotations

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


def catalog(data: dict, rid: str) -> dict:
    return next(row for row in data["timingCatalog"] if row["requirementId"] == rid)


def elapsed_from_declared_origin(timing: dict, events: dict[str, float]) -> float:
    if timing.get("clockStart") != "CORRELATED-TRIGGER-TIMESTAMP":
        raise AssertionError(f"unsupported clockStart {timing.get('clockStart')}")
    trigger = timing["trigger"]
    response = timing["response"]
    if trigger not in events:
        raise KeyError(f"timeline lacks trigger {trigger}")
    if response not in events:
        raise KeyError(f"timeline lacks response {response}")
    return events[response] - events[trigger]


def interval_holds(timing: dict, events: dict[str, float]) -> bool:
    elapsed = elapsed_from_declared_origin(timing, events)
    lower, upper = timing["lowerBound"], timing["upperBound"]
    return lower <= elapsed <= upper


def test_close_timeline_uses_request_origin_not_expiry_delay() -> None:
    data = m1_package()
    assert m1_errors(data) == []
    close = req(data, "CRS-M1-00521")["timing"]
    window = req(data, "CRS-M1-00520")["timing"]
    host = req(data, "CRS-M1-00391")["timing"]
    assert close["trigger"] == "FIND-REQUEST-SENT"
    assert close["trigger"] == window["trigger"]
    assert close["clockStart"] == "CORRELATED-TRIGGER-TIMESTAMP"
    assert close["cancellation"] == window["cancellation"] == host["cancellation"] == "FIND-ABORT-DOES-NOT-WAIVE-WINDOWS"

    on_time = {
        window["trigger"]: 0,
        window["response"]: 3,
        close["response"]: 3,
    }
    assert interval_holds(window, on_time)
    assert interval_holds(close, on_time)

    early = dict(on_time)
    early[close["response"]] = 1
    assert not interval_holds(close, early)

    late = dict(on_time)
    late[close["response"]] = 6
    assert not interval_holds(close, late)

    shifted = {
        window["trigger"]: 10,
        window["response"]: 13,
        close["response"]: 13,
    }
    assert interval_holds(close, shifted)
    assert interval_holds(window, shifted)

    host_ok = {host["trigger"]: 10, host["response"]: 11}
    host_late = {host["trigger"]: 10, host["response"]: 12.1}
    assert interval_holds(host, host_ok)
    assert not interval_holds(host, host_late)


def test_reverting_close_trigger_to_expiry_fails_after_refresh() -> None:
    data = m1_package()
    req(data, "CRS-M1-00521")["timing"]["trigger"] = req(data, "CRS-M1-00520")["timing"]["response"]
    refresh_m1(data)
    found = m1_errors(data)
    assert any("shifting the time origin" in item or "RC-FIND-CLOSE-AT-EXPIRY" in item for item in found)

    model = m2_package()
    row = catalog(model, "CRS-M1-00521")
    row["trigger"] = "FIND-ANSWER-WINDOW-LIFETIME-ELAPSED"
    row["pairingPolicy"] = "PAIR-WINDOW-EXPIRY-WITH-REGISTRATION-CLOSE"
    refresh_m2(model)
    found = m2_errors(model)
    assert any("trigger drifted from M1" in item or "pairingPolicy drifted from M1" in item for item in found)
