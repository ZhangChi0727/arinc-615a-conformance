from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("sync_m2_model", ROOT / "scripts/sync_m2_model.py")
assert SPEC and SPEC.loader
m2 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m2)

BASELINE_SPEC = importlib.util.spec_from_file_location(
    "check_repo_baseline", ROOT / "scripts/check_repo_baseline.py"
)
assert BASELINE_SPEC and BASELINE_SPEC.loader
baseline = importlib.util.module_from_spec(BASELINE_SPEC)
BASELINE_SPEC.loader.exec_module(baseline)


def package() -> dict:
    return json.loads(m2.PACKAGE_PATH.read_text(encoding="utf-8"))


def register() -> dict:
    return json.loads(m2.SOURCE_REGISTER_PATH.read_text(encoding="utf-8"))


def errors(data: dict, source_register: dict | None = None) -> list[str]:
    return m2.package_errors(data, register=source_register)


def flip_hex(value: str) -> str:
    return ("0" if value[:1] != "0" else "1") + value[1:]


def refresh_summary(data: dict) -> None:
    summary = data["inventorySummary"]
    summary.update(
        requirementCount=len(data["requirementDispositions"]),
        dispositionCount=len(data["requirementDispositions"]),
        traceCount=len(data["traceRelations"]),
        stateCount=len(data["model"]["states"]),
        transitionCount=len(data["model"]["transitions"]),
        timingCount=len(data["timingCatalog"]),
        dispositionsFingerprint=m2.fingerprint(data["requirementDispositions"]),
        modelFingerprint=m2.fingerprint(data["model"]),
        timingFingerprint=m2.fingerprint(data["timingCatalog"]),
        inputFingerprint=m2.fingerprint(data["inputAcceptance"]),
    )


def test_package_is_valid_and_view_is_current() -> None:
    data = package()
    assert errors(data) == []
    assert m2.VIEW_PATH.read_text(encoding="utf-8") == m2.render(data)


def test_generated_view_is_bilingual() -> None:
    text = m2.VIEW_PATH.read_text(encoding="utf-8")
    en_text, zh_text = text.split("# 中文版", 1)
    assert baseline.document_shape(en_text) == baseline.document_shape(zh_text)


def test_recorded_input_identity_matches_git() -> None:
    data = package()
    acc = data["inputAcceptance"]
    assert acc["mergeParents"][1] == acc["approvedHead"]
    assert acc["mergeSecondParent"] == acc["approvedHead"]
    assert acc["mainCiHead"] == acc["mergeCommit"]
    assert acc["githubReviewState"] != "APPROVED"
    assert "NOT-CLAIMED" in acc["independenceClaim"]
    assert acc["m1NetIssueEditionSnapshot"]["blocksM1Approval"] is True
    for item in acc["inputs"]:
        blob = m2.git_blob(acc["baseCommit"], item["path"])
        assert blob == item["gitBlobOid"]


@pytest.mark.parametrize("mutation", ["blob", "parent", "tree", "ci", "review"])
def test_wrong_input_identity_is_rejected(mutation: str) -> None:
    data = package()
    acc = data["inputAcceptance"]
    if mutation == "blob":
        acc["inputs"][0]["gitBlobOid"] = flip_hex(acc["inputs"][0]["gitBlobOid"])
    elif mutation == "parent":
        acc["mergeParents"][1] = flip_hex(acc["approvedHead"])
        acc["mergeSecondParent"] = acc["mergeParents"][1]
    elif mutation == "tree":
        acc["mergeTree"] = flip_hex(acc["mergeTree"])
    elif mutation == "ci":
        acc["mainCiHead"] = flip_hex(acc["mergeCommit"])
    else:
        acc["githubReviewState"] = "APPROVED"
    refresh_summary(data)
    assert errors(data)


def test_deleted_requirement_and_traces_still_fail_after_fingerprint_refresh() -> None:
    data = package()
    rid = data["requirementDispositions"][0]["requirementId"]
    data["requirementDispositions"] = [
        row for row in data["requirementDispositions"] if row["requirementId"] != rid
    ]
    data["traceRelations"] = [row for row in data["traceRelations"] if row["requirementId"] != rid]
    refresh_summary(data)
    assert any(
        "partition" in item or "lack traces" in item or "inventorySummary" in item
        for item in errors(data)
    )


def test_duplicate_ids_and_dangling_targets_are_rejected() -> None:
    data = package()
    data["requirementDispositions"][1]["requirementId"] = data["requirementDispositions"][0]["requirementId"]
    refresh_summary(data)
    assert any("duplicate" in item for item in errors(data))
    data = package()
    data["traceRelations"][0]["targetKind"] = "TRANSITION"
    data["traceRelations"][0]["targetId"] = "T_DOES_NOT_EXIST"
    refresh_summary(data)
    assert any("missing transition" in item for item in errors(data))


def test_polarity_and_modality_drift_are_rejected() -> None:
    data = package()
    row = next(item for item in data["traceRelations"] if item.get("polarity"))
    row["polarity"] = "MUST-NOT" if row["polarity"] != "MUST-NOT" else "MUST"
    refresh_summary(data)
    assert any("polarity" in item for item in errors(data))
    data = package()
    row = next(item for item in data["traceRelations"] if item.get("sourceModality"))
    row["sourceModality"] = "shall_not" if row["sourceModality"] != "shall_not" else "shall"
    refresh_summary(data)
    assert any("modality" in item for item in errors(data))


def test_send_cannot_be_swapped_onto_the_peer_output() -> None:
    data = package()
    data["scope"]["observationBoundary"]["targetHardware"]["outputs"].append("EV_DL_RRQ_LCI")
    refresh_summary(data)
    assert any("data-loader LCI" in item for item in errors(data))


def test_graph_rejects_missing_initial_dangling_and_unexpected_terminal() -> None:
    data = package()
    data["model"]["initialState"] = "S_MISSING"
    refresh_summary(data)
    assert any("initial state" in item for item in errors(data))
    data = package()
    data["model"]["transitions"][0]["target"] = "S_MISSING"
    refresh_summary(data)
    assert any("dangling" in item for item in errors(data))
    data = package()
    complete = next(row for row in data["model"]["states"] if row["id"] == "S_INF_COMPLETE")
    complete["terminal"] = True
    refresh_summary(data)
    assert any("unexpected terminal" in item for item in errors(data))


def test_timing_rejects_reversed_bounds_unresolved_pass_and_bad_ast() -> None:
    data = package()
    row = next(
        item for item in data["timingCatalog"] if isinstance(item.get("lowerBound"), (int, float))
    )
    row["lowerBound"] = 9
    row["upperBound"] = 1
    refresh_summary(data)
    assert any("reversed" in item for item in errors(data))
    data = package()
    unresolved = next(item for item in data["timingCatalog"] if item.get("boundKind") == "UNRESOLVED")
    unresolved["staticCheck"] = "PASS"
    refresh_summary(data)
    assert any("unresolved bound" in item for item in errors(data))
    data = package()
    expr_row = next(
        item
        for item in data["timingCatalog"]
        if isinstance(item.get("expression"), dict) and item["expression"].get("kind") == "BINARY"
    )
    expr_row["expression"]["op"] = "POW"
    refresh_summary(data)
    assert any("unsupported operator" in item for item in errors(data))
    data = package()
    expr_row = next(
        item
        for item in data["timingCatalog"]
        if isinstance(item.get("expression"), dict) and item["expression"].get("kind") == "BINARY"
    )
    expr_row["expression"]["left"]["name"] = "NOT_A_DEFINED_SYMBOL"
    refresh_summary(data)
    assert any("undefined" in item for item in errors(data))
    data = package()
    expr_row = next(item for item in data["timingCatalog"] if isinstance(item.get("expression"), dict))
    expr_row["expression"]["note"] = "eval hidden"
    refresh_summary(data)
    assert any("disallowed evaluation" in item for item in errors(data))


def test_unit_and_clock_drift_are_rejected() -> None:
    data = package()
    data["timingCatalog"][0]["unit"] = "weeks"
    refresh_summary(data)
    assert any("unit drifted" in item for item in errors(data))
    data = package()
    data["timingCatalog"][0]["clockId"] = "CLK_MISSING"
    refresh_summary(data)
    assert any("clock is missing" in item for item in errors(data))


def test_capability_and_scope_guards_hold() -> None:
    data = package()
    data["scope"]["afdxSelected"] = True
    refresh_summary(data)
    assert any("AFDX" in item for item in errors(data))
    data = package()
    data["model"]["interfaces"]["IF_INTEGRITY"]["blockedBy"] = []
    refresh_summary(data)
    assert any("645" in item for item in errors(data))
    mutated = register()
    next(row for row in mutated["capabilities"] if row["id"] == "CRC-VALIDATION")["status"] = "ESTABLISHED"
    assert any("ESTABLISHED" in item for item in errors(package(), mutated))
    mutated = register()
    mutated["openDependencies"] = [row for row in mutated["openDependencies"] if row["id"] != "ARINC-645"]
    assert any("645" in item for item in errors(package(), mutated))


def test_action_cannot_close_without_evidence_or_silently_close_deferred_work() -> None:
    data = package()
    row = next(item for item in data["actions"] if item["id"] == "A-4")
    row["status"] = "CLOSED"
    refresh_summary(data)
    assert any("A-4" in item for item in errors(data))
    data = package()
    row = next(item for item in data["actions"] if item["id"] == "NET-ISSUE-EDITION")
    row["status"] = "CLOSED"
    row["evidence"] = ["none"]
    refresh_summary(data)
    assert any("NET-ISSUE-EDITION" in item for item in errors(data))
    data = package()
    row = next(item for item in data["actions"] if item["id"] == "F-1")
    row["status"] = "CLOSED-IN-THIS-PR"
    row["evidence"] = []
    refresh_summary(data)
    assert errors(data)


def test_network_dispositions_cannot_be_a_blanket_class() -> None:
    data = package()
    for row in data["networkRelationDispositions"]:
        row["m2Disposition"] = "NOT-APPLICABLE"
    refresh_summary(data)
    assert any("NOT-APPLICABLE" in item or "blanket" in item for item in errors(data))


def test_self_approval_and_timed_pass_are_rejected() -> None:
    data = package()
    data["reviewControl"]["rg2"] = "APPROVED"
    refresh_summary(data)
    assert any("RG2" in item for item in errors(data))
    data = package()
    data["reviewControl"]["reviewHead"] = "SELF-BOUND"
    refresh_summary(data)
    assert any("UNBOUND-DRAFT" in item for item in errors(data))
    data = package()
    data["analysisScope"]["timedReachability"] = "PASS"
    refresh_summary(data)
    assert any("timed reachability" in item for item in errors(data))


def test_missing_negative_rfc_inventory_is_rejected() -> None:
    data = package()
    data["sourceRefinements"] = [
        row for row in data["sourceRefinements"] if row["id"] != "REF-A2-NO-RFC-1785-ACTIVE-EDGE"
    ]
    refresh_summary(data)
    assert any("RFC-1785" in item for item in errors(data))


def test_non_behavior_obligations_may_map_to_data_or_interface_kinds() -> None:
    data = package()
    kinds = {row["kind"] for row in data["requirementDispositions"]}
    assert {"DATA-CONSTRAINT", "INTERFACE-PREMISE", "DEPENDENCY-BLOCKED", "SCOPE-CONSTRAINT"} <= kinds
    assert errors(data) == []
