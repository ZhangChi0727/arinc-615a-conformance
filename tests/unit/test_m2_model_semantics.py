from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
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

ZERO_OID = "0" * 40
LEGAL_UPLOAD = (
    "T_UPL_LUI_RRQ",
    "T_UPL_LUI_XFER",
    "T_UPL_EVAL",
    "T_UPL_ACCEPT_INIT",
    "T_UPL_LIST_OFFER",
    "T_UPL_WAIT_LUS0001",
    "T_UPL_LUR_WRQ",
    "T_UPL_LUR_ACK",
    "T_UPL_LUR_XFER",
    "T_UPL_FILE_RRQ",
)


def package() -> dict:
    return json.loads(m2.PACKAGE_PATH.read_text(encoding="utf-8"))


def register() -> dict:
    return json.loads(m2.SOURCE_REGISTER_PATH.read_text(encoding="utf-8"))


def errors(
    data: dict,
    source_register: dict | None = None,
    git_root: Path | None = None,
    m1: dict | None = None,
) -> list[str]:
    return m2.package_errors(data, register=source_register, git_root=git_root, m1=m1)


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
        refinementFingerprint=m2.fingerprint(data["sourceRefinements"]),
        actionFingerprint=m2.fingerprint(data["actions"]),
        premiseFingerprint=m2.fingerprint(data["infrastructurePremises"]),
        witnessFingerprint=m2.fingerprint(data.get("discreteWitnesses")),
        blockingFingerprint=m2.fingerprint(data.get("blockingInputs")),
        endpointBindingFingerprint=m2.fingerprint(data.get("sequenceEndpointBindings")),
    )


def git_env() -> dict[str, str]:
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = "m2"
    env["GIT_AUTHOR_EMAIL"] = "m2@example.com"
    env["GIT_COMMITTER_NAME"] = "m2"
    env["GIT_COMMITTER_EMAIL"] = "m2@example.com"
    return env


def test_package_is_valid_and_view_is_current() -> None:
    data = package()
    assert errors(data) == []
    assert m2.VIEW_PATH.read_text(encoding="utf-8") == m2.render(data)


def test_generated_view_is_bilingual_and_locates_objects() -> None:
    text = m2.VIEW_PATH.read_text(encoding="utf-8")
    en_text, zh_text = text.split("# 中文版", 1)
    assert baseline.document_shape(en_text) == baseline.document_shape(zh_text)
    data = package()
    required_ids = (
        [row["id"] for row in data["model"]["states"]]
        + [row["id"] for row in data["model"]["transitions"]]
        + [row["id"] for row in data["timingCatalog"]]
        + [row["id"] for row in data["actions"]]
        + [row["id"] for row in data["sourceRefinements"]]
        + [row["requirementId"] for row in data["requirementDispositions"]]
        + [row["id"] for row in data["infrastructurePremises"]]
        + [row["id"] for row in data["model"]["variables"]]
        + [row["id"] for row in data["model"]["parameters"]]
        + [row["id"] for row in data["model"]["clocks"]]
        + [row["id"] for row in data["model"]["events"]]
        + list(data["model"]["interfaces"])
    )
    for object_id in required_ids:
        assert object_id in en_text
        assert object_id in zh_text
    assert "VAR_PROTOCOL_FILE" not in en_text
    assert data["model"]["states"][0]["summaryZh"] in zh_text
    assert data["model"]["states"][0]["summaryEn"] in en_text


def test_recorded_input_identity_matches_git() -> None:
    data = package()
    acc = data["inputAcceptance"]
    assert acc["mergeParents"][1] == acc["approvedHead"]
    assert acc["mergeSecondParent"] == acc["approvedHead"]
    assert acc["approvedHeadTree"] == acc["mergeTree"]
    assert acc["mainCiHead"] == acc["mergeCommit"]
    assert acc["githubReviewState"] != "APPROVED"
    assert "NOT-CLAIMED" in acc["independenceClaim"]
    assert acc["m1NetIssueEditionSnapshot"]["blocksM1Approval"] is True
    successor = acc.get("successorDelta") or {}
    preserved = {item["path"]: item["gitBlobOid"] for item in successor.get("preservedFrozenInputs") or []}
    assert successor.get("doesNotTransplantFrozenApproval") is True
    assert preserved
    for item in acc["inputs"]:
        frozen = preserved[item["path"]]
        assert m2.git_blob(acc["mergeCommit"], item["path"]) == frozen
        work = m2.git_output(ROOT, ["hash-object", str(ROOT / item["path"])])
        assert work == item["gitBlobOid"]


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
        acc["approvedHeadTree"] = acc["mergeTree"]
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
    assert any("missing" in item for item in errors(data))


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
    assert any("terminal" in item for item in errors(data))


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
    unresolved = data["timingCatalog"][0]
    unresolved["boundKind"] = "UNRESOLVED"
    unresolved["staticCheck"] = "PASS"
    refresh_summary(data)
    assert any("unresolved bound" in item for item in errors(data))
    data = package()
    expr_row = next(
        item
        for item in data["timingCatalog"]
        if any(node.get("kind") == "BINARY" for node in m2.walk_nodes(item.get("expression")))
    )
    binary = next(node for node in m2.walk_nodes(expr_row["expression"]) if node.get("kind") == "BINARY")
    binary["op"] = "POW"
    refresh_summary(data)
    assert any("unsupported operator" in item for item in errors(data))
    data = package()
    expr_row = next(
        item
        for item in data["timingCatalog"]
        if any(node.get("kind") == "SYMBOL" for node in m2.walk_nodes(item.get("expression")))
    )
    symbol = next(node for node in m2.walk_nodes(expr_row["expression"]) if node.get("kind") == "SYMBOL")
    symbol["name"] = "NOT_A_DEFINED_SYMBOL"
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
    assert errors(data)
    data = package()
    data["timingCatalog"][0]["clockId"] = "CLK_MISSING"
    refresh_summary(data)
    assert any("clock is missing" in item for item in errors(data))


def test_capability_and_scope_guards_hold() -> None:
    data = package()
    data["scope"]["afdxSelected"] = True
    refresh_summary(data)
    assert errors(data)
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
    assert errors(data)
    data = package()
    data["reviewControl"]["reviewHead"] = "SELF-BOUND"
    refresh_summary(data)
    assert any("UNBOUND-DRAFT" in item for item in errors(data))
    data = package()
    data["analysisScope"]["timedReachability"] = "PASS"
    refresh_summary(data)
    assert errors(data)


def test_missing_negative_rfc_inventory_is_rejected() -> None:
    data = package()
    data["sourceRefinements"] = [
        row for row in data["sourceRefinements"] if row.get("toSourceId") != "RFC-1785"
    ]
    refresh_summary(data)
    assert any("RFC-1785" in item for item in errors(data))


def test_non_behavior_obligations_may_map_to_data_or_interface_kinds() -> None:
    data = package()
    kinds = {row["kind"] for row in data["requirementDispositions"]}
    assert {"DATA-CONSTRAINT", "INTERFACE-PREMISE", "DEPENDENCY-BLOCKED", "SCOPE-CONSTRAINT"} <= kinds
    assert errors(data) == []


def _follow(data: dict, ids: tuple[str, ...]) -> list[str]:
    trans = {row["id"]: row for row in data["model"]["transitions"]}
    states = [trans[ids[0]]["source"]]
    for tid in ids:
        row = trans[tid]
        assert row["source"] == states[-1]
        states.append(row["target"])
    return states


def test_upload_list_then_lur_then_file_is_a_legal_path() -> None:
    data = package()
    states = _follow(data, LEGAL_UPLOAD)
    assert states == [
        "S_IDLE",
        "S_UPL_LUI_RRQ",
        "S_UPL_LUI_XFER",
        "S_UPL_EVALUATE",
        "S_UPL_LIST_SENT",
        "S_UPL_WAIT_LUS0001",
        "S_UPL_WAIT_LUS0001",
        "S_UPL_LUR_WRQ",
        "S_UPL_LUR_ACK",
        "S_UPL_LUR_XFER",
        "S_UPL_FILE_RRQ",
    ]
    wait_targets = {
        row["targetId"] for row in data["traceRelations"] if row["requirementId"] == "CRS-M1-00364"
    }
    assert wait_targets
    assert all(target.startswith("T_UPL_") or target.startswith("S_UPL_") for target in wait_targets)


def test_skipping_lur_or_crossing_information_into_upload_files_fails() -> None:
    data = package()
    data["model"]["transitions"].append({
        "id": "T_SKIP_LUR",
        "source": "S_UPL_EVALUATE",
        "event": "EV_TH_RRQ_FILE",
        "guard": {"kind": "TRUE"},
        "updates": [],
        "resets": [],
        "outputs": [],
        "target": "S_UPL_FILE_RRQ",
        "requirementIds": ["CRS-M1-00368"],
        "noteEn": "illegal skip",
        "noteZh": "非法跳过",
    })
    refresh_summary(data)
    assert any("forbidden edge" in item for item in errors(data))
    data = package()
    data["model"]["transitions"].append({
        "id": "T_CROSS_MAP",
        "source": "S_INF_EVALUATE",
        "event": "EV_DL_DATA_FILE",
        "guard": {"kind": "TRUE"},
        "updates": [],
        "resets": [],
        "outputs": [],
        "target": "S_UPL_FILE_XFER",
        "requirementIds": ["CRS-M1-00370"],
        "noteEn": "illegal cross map",
        "noteZh": "非法跨服务映射",
    })
    refresh_summary(data)
    assert any("forbidden edge" in item for item in errors(data))


def test_source_equation_keeps_retry_terms_and_rejects_endpoint_drift() -> None:
    data = package()
    row = next(item for item in data["timingCatalog"] if item["requirementId"] == "CRS-M1-00188")
    assert "DLP-RETRY" in row["sourceRelation"]
    assert "TFTP-RETRY" in row["sourceRelation"]
    assert "2*(TFTP-TO/4)" in row["sourceRelation"]
    names = m2.ast_symbols(row["expression"])
    assert {"DLP_TO", "DURATION_TIME", "DLP_RETRY", "TFTP_RETRY", "TFTP_TO"} <= names
    row["expression"] = {
        "kind": "BINARY",
        "op": "SUB",
        "left": {"kind": "SYMBOL", "name": "DLP_TO", "unit": "s"},
        "right": {"kind": "SYMBOL", "name": "TFTP_TO", "unit": "s"},
        "unit": "s",
    }
    refresh_summary(data)
    assert any("retry" in item or "00188" in item for item in errors(data))
    data = package()
    row = next(item for item in data["timingCatalog"] if item["requirementId"] == "CRS-M1-00188")
    row["upperBoundary"] = "CLOSED"
    refresh_summary(data)
    assert any("endpoint" in item for item in errors(data))


def test_timeout_transitions_require_clock_guards() -> None:
    data = package()
    timeout = next(row for row in data["model"]["transitions"] if row["event"] == "EV_TIMEOUT_TFTP")
    assert "CLK_TFTP" in m2.ast_clocks(timeout["guard"])
    timeout["guard"] = {"kind": "TRUE"}
    refresh_summary(data)
    assert any("not enabled by clock" in item for item in errors(data))


def test_field_constraints_are_not_dumped_onto_a_generic_variable() -> None:
    data = package()
    counts = {}
    for row in data["traceRelations"]:
        if row["targetKind"] == "VARIABLE":
            counts[row["targetId"]] = counts.get(row["targetId"], 0) + 1
    assert "VAR_PROTOCOL_FILE" not in counts
    crs34 = next(row for row in data["requirementDispositions"] if row["requirementId"] == "CRS-M1-00034")
    assert "IF_TFTP_BLOCKSIZE" in crs34["modelTargetIds"]
    crs315 = next(row for row in data["traceRelations"] if row["requirementId"] == "CRS-M1-00315")
    assert crs315["targetKind"] == "FIELD-CONSTRAINT"
    data["traceRelations"].append({
        "id": "TR-GENERIC",
        "requirementId": "CRS-M1-00315",
        "targetKind": "VARIABLE",
        "targetId": "VAR_PROTOCOL_FILE",
        "polarity": crs315["polarity"],
        "sourceModality": crs315["sourceModality"],
        "rationaleCode": "dump",
        "rationaleEn": "generic dump",
        "rationaleZh": "泛化倾倒",
    })
    refresh_summary(data)
    assert any("generic file variable" in item for item in errors(data))


def test_blocksize_and_lui_lur_source_edges() -> None:
    data = package()
    assert any(
        row.get("toSourceId") == "RFC-2348" and row["fromRequirementId"] == "CRS-M1-00034"
        for row in data["sourceRefinements"]
    )
    blocked = [row for row in data["sourceRefinements"] if row["reviewStatus"] == "OPEN-M1-CORRECTION"]
    assert {row["fromRequirementId"] for row in blocked}.isdisjoint({"CRS-M1-00143", "CRS-M1-00315", "CRS-M1-00365"})
    active = [
        row
        for row in data["sourceRefinements"]
        if row["fromRequirementId"] in {"CRS-M1-00143", "CRS-M1-00315", "CRS-M1-00365"}
    ]
    assert len(active) >= 3
    assert all(row["reviewStatus"] != "OPEN-M1-CORRECTION" for row in active)
    rfc = next(row for row in data["sourceRefinements"] if row.get("toSourceId") == "RFC-2347")
    assert rfc["toLocator"]["clause"]
    assert rfc["toLocator"]["retrievedSha256"]
    data["sourceRefinements"] = [row for row in data["sourceRefinements"] if row.get("toSourceId") != "RFC-2348"]
    refresh_summary(data)
    assert any("RFC-2348" in item for item in errors(data))


def test_successor_m1_identities_are_lur_lus_and_data_loader() -> None:
    m1 = json.loads((ROOT / "configs/requirements/arinc_615a3_m1_crs.json").read_text(encoding="utf-8"))
    by_id = {row["id"]: row for row in m1["requirements"]}
    for rid in [f"CRS-M1-00{n}" for n in range(309, 316)]:
        assert by_id[rid]["fieldConstraint"]["protocolFile"] == "LUR", rid
    lur_left = [
        row["id"]
        for row in m1["requirements"]
        if (row.get("source") or {}).get("clause") == "6.4.5"
        and (row.get("fieldConstraint") or {}).get("protocolFile") == "LUR"
    ]
    assert lur_left == []
    lus = [
        row
        for row in m1["requirements"]
        if (row.get("fieldConstraint") or {}).get("protocolFile") == "LUS"
    ]
    assert lus
    assert all((row.get("source") or {}).get("clause") == "6.4.5" for row in lus)
    assert by_id["CRS-M1-00365"]["semantic"]["actor"] == "DATA-LOADER"
    assert by_id["CRS-M1-00365"]["semantic"]["receiver"] == "TARGET-HARDWARE"
    assert by_id["CRS-M1-00366"]["semantic"]["actor"] == "TARGET-HARDWARE"
    assert by_id["CRS-M1-00366"]["semantic"]["receiver"] == "DATA-LOADER"
    assert by_id["CRS-M1-00367"]["semantic"]["actor"] == "DATA-LOADER"
    assert by_id["CRS-M1-00367"]["semantic"]["receiver"] == "TARGET-HARDWARE"
    assert "LUR" in by_id["CRS-M1-00143"]["semantic"]["objects"]
    data = package()
    successor = data["inputAcceptance"]["successorDelta"]
    assert successor["doesNotTransplantFrozenApproval"] is True
    assert successor["predecessorInputCommit"]
    assert successor["predecessorInputTree"]
    assert {item["path"] for item in successor["predecessorInputBlobs"]} == {
        item["path"] for item in data["inputAcceptance"]["inputs"]
    }
    assert data["reviewControl"]["blocksFinalApproval"] is True
    identity = next(row for row in data["blockingInputs"] if row["id"] == "M1-FILE-IDENTITY-6-4-4")
    assert identity["status"] == "CLOSED-BY-SUCCESSOR-M1-DELTA"
    net = next(row for row in data["blockingInputs"] if row["id"] == "NET-ISSUE-EDITION")
    assert net["status"].startswith("ACCEPTED-CURRENT-EDITION")
    assert "P3-1" in net["status"]
    assert "AFDX-DEFERRED" in net["status"]
    assert (ROOT / "docs/control/changes" / f"{successor['changeRequest']}.md").is_file()
    assert (ROOT / "docs/control/changes" / f"{successor['authorizationRequest']}.md").is_file()


def test_open_m1_correction_cannot_be_closed() -> None:
    data = package()
    row = next(item for item in data["actions"] if item["id"] == "M1-FILE-IDENTITY-6-4-4")
    row["status"] = "CLOSED"
    row["evidence"] = ["forced"]
    refresh_summary(data)
    assert any("silently CLOSED" in item or "OPEN-M1-CORRECTION" in item for item in errors(data))
    data = package()
    data["reviewControl"]["blocksFinalApproval"] = False
    refresh_summary(data)
    assert any("blocksFinalApproval" in item for item in errors(data))


def _apply_review_mutation(name: str, data: dict) -> None:
    if name == "timingCatalog=[]":
        data["timingCatalog"] = []
    elif name == "sourceRefinements-empty-shell":
        data["sourceRefinements"] = [{"id": "REF-A2-NO-RFC-1785-ACTIVE-EDGE"}]
    elif name == "actions=[]":
        data["actions"] = []
    elif name == "infrastructurePremises=[]":
        data["infrastructurePremises"] = []
    elif name == "undeclared-guard-update":
        data["model"]["transitions"][0]["guard"] = {
            "kind": "COMPARE",
            "op": "LT",
            "left": {"kind": "CLOCK", "name": "MISSING_CLOCK"},
            "right": {"kind": "LITERAL", "value": 999},
        }
        data["model"]["transitions"][0]["updates"] = [
            {"kind": "ASSIGN", "target": "UNDECLARED", "value": {"kind": "ENUM", "value": "nonsense"}}
        ]
    elif name == "mergeParents[0]=zeros":
        data["inputAcceptance"]["mergeParents"][0] = ZERO_OID
    elif name == "inputs=[]":
        data["inputAcceptance"]["inputs"] = []
    elif name == "approved-heads-zeros":
        data["inputAcceptance"]["approvedHead"] = ZERO_OID
        data["inputAcceptance"]["mergeSecondParent"] = ZERO_OID
        data["inputAcceptance"]["mergeParents"][1] = ZERO_OID
    elif name == "rg0=APPROVE":
        data["reviewControl"]["rg0"] = "APPROVE"
    elif name == "timing-unit-s-to-ms":
        data["timingCatalog"][0]["unit"] = "ms"
    elif name == "toRequirementId-missing":
        data["sourceRefinements"][0]["toRequirementId"] = "CRS-M1-99999"
    else:
        raise AssertionError(name)


@pytest.mark.parametrize(
    "name",
    [
        "timingCatalog=[]",
        "sourceRefinements-empty-shell",
        "actions=[]",
        "infrastructurePremises=[]",
        "undeclared-guard-update",
        "mergeParents[0]=zeros",
        "inputs=[]",
        "approved-heads-zeros",
        "rg0=APPROVE",
        "timing-unit-s-to-ms",
        "toRequirementId-missing",
    ],
)
def test_review_mutations_fail_after_fingerprint_refresh(name: str) -> None:
    data = copy.deepcopy(package())
    _apply_review_mutation(name, data)
    refresh_summary(data)
    assert errors(data), name


def test_legal_additional_action_still_passes() -> None:
    data = package()
    data["actions"].append({
        "id": "EXTRA-REVIEW-NOTE",
        "status": "OPEN",
        "ownerRole": "M2-AUTHOR",
        "deadlineGate": "PROFILE-MODEL-REFINEMENT-GATE",
        "evidence": [],
        "noteEn": "Additional open note does not remove required actions.",
        "noteZh": "额外开放说明不删除必需行动。",
    })
    refresh_summary(data)
    assert errors(data) == []


def test_missing_git_objects_fail_closed(tmp_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True, text=True)
    assert any("missing" in item or "cannot be read" in item for item in errors(package(), git_root=tmp_path))


def test_tmp_repo_two_parent_identity(tmp_path: Path) -> None:
    env = git_env()
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True, text=True)
    first = tmp_path / "configs" / "requirements"
    first.mkdir(parents=True)
    marker = first / "arinc_615a3_m1_crs.json"
    marker.write_text("{}\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True, text=True)
    subprocess.run(["git", "commit", "-m", "base"], cwd=tmp_path, check=True, capture_output=True, text=True, env=env)
    first_parent = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True).strip()
    subprocess.run(["git", "checkout", "-b", "feature"], cwd=tmp_path, check=True, capture_output=True, text=True)
    marker.write_text('{"ok": true}\n', encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True, text=True)
    subprocess.run(["git", "commit", "-m", "head"], cwd=tmp_path, check=True, capture_output=True, text=True, env=env)
    approved = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True).strip()
    subprocess.run(["git", "checkout", "-"], cwd=tmp_path, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "merge", "--no-ff", "feature", "-m", "merge"],
        cwd=tmp_path, check=True, capture_output=True, text=True, env=env,
    )
    merge = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True).strip()
    tree = subprocess.check_output(["git", "rev-parse", f"{merge}^{{tree}}"], cwd=tmp_path, text=True).strip()
    blob = subprocess.check_output(
        ["git", "rev-parse", f"{merge}:configs/requirements/arinc_615a3_m1_crs.json"],
        cwd=tmp_path, text=True,
    ).strip()
    acc = {
        "githubReviewState": "COMMENTED",
        "recordedConclusion": "APPROVE WITH ACTIONS",
        "independenceClaim": "NOT-CLAIMED-NAMED-INDEPENDENT-REVIEWER",
        "signOffKind": "REPOSITORY-OWNER-ACCEPTED-CONTROL-SIGNOFF",
        "approvedHead": approved,
        "mergeCommit": merge,
        "mergeParents": [first_parent, approved],
        "mergeSecondParent": approved,
        "mergeTree": tree,
        "approvedHeadTree": tree,
        "mainCiHead": merge,
        "inputs": [
            {"path": path, "gitBlobOid": blob, "role": "M1-IMMUTABLE-INPUT"}
            for path in m2.REQUIRED_M1_INPUT_PATHS
        ],
    }
    missing = m2.input_identity_errors(acc, tmp_path)
    assert missing
    forged = copy.deepcopy(acc)
    forged["mergeParents"][0] = ZERO_OID
    assert m2.input_identity_errors(forged, tmp_path)


def test_chinese_view_does_not_reuse_english_summaries() -> None:
    data = package()
    data["model"]["states"][0]["summaryZh"] = data["model"]["states"][0]["summaryEn"]
    refresh_summary(data)
    assert any("reuses English" in item for item in errors(data))


def _first_clock_ge(node: dict) -> dict:
    for item in m2.walk_nodes(node):
        if (
            item.get("kind") == "COMPARE"
            and item.get("op") == "GE"
            and item.get("left", {}).get("kind") == "CLOCK"
        ):
            return item
    raise AssertionError("missing clock GE compare")


def test_round2_mutations_fail_after_fingerprint_refresh() -> None:
    data = copy.deepcopy(package())
    timeout = next(row for row in data["model"]["transitions"] if row["event"] == "EV_TIMEOUT_TFTP")
    _first_clock_ge(timeout["guard"])["op"] = "LT"
    refresh_summary(data)
    assert any("not enabled by clock" in item for item in errors(data))

    data = copy.deepcopy(package())
    equation = next(item for item in data["timingCatalog"] if item["requirementId"] == "CRS-M1-00188")
    assert equation["expression"]["op"] == "GT"
    equation["expression"]["op"] = "LT"
    refresh_summary(data)
    assert any("equation structure" in item or "source relation" in item for item in errors(data))

    data = copy.deepcopy(package())
    assign = next(
        node
        for row in data["model"]["transitions"]
        for node in row.get("updates") or []
        if node.get("kind") == "ASSIGN" and node.get("value", {}).get("kind") == "ENUM"
    )
    assign["value"]["value"] = "OUTSIDE-DOMAIN"
    refresh_summary(data)
    assert any("outside domain" in item for item in errors(data))

    data = copy.deepcopy(package())
    data["model"]["fieldConstraints"][0]["widthBitsExpression"] = "999"
    refresh_summary(data)
    assert any("widthBitsExpression" in item or "axis" in item for item in errors(data))

    data = copy.deepcopy(package())
    rfc = next(row for row in data["sourceRefinements"] if row.get("toSourceId") == "RFC-2348")
    rfc["toLocator"]["clause"] = "NONEXISTENT-SECTION"
    refresh_summary(data)
    assert any("atomic part" in item for item in errors(data))


def test_wait_lower_bound_is_not_an_upper_bound() -> None:
    data = package()
    row = next(item for item in data["timingCatalog"] if item["requirementId"] == "CRS-M1-00032")
    assert row["constraintKind"] == "NOT-BEFORE-LOWER-BOUND"
    assert row["expression"]["op"] == "GE"
    assert row["clockId"] == "CLK_WAIT"
    assert any("WAIT" in item for item in row["resets"])
    row["expression"]["op"] = "LE"
    refresh_summary(data)
    assert any("wait lower bound" in item or "not CLK_WAIT >=" in item for item in errors(data))


def test_legal_commutative_add_and_payload_path_still_pass() -> None:
    data = package()
    equation = next(item for item in data["timingCatalog"] if item["requirementId"] == "CRS-M1-00188")
    add = next(node for node in m2.walk_nodes(equation["expression"]) if node.get("kind") == "BINARY" and node.get("op") == "ADD")
    add["left"], add["right"] = add["right"], add["left"]
    refresh_summary(data)
    assert errors(data) == []
    data = package()
    accept = next(row for row in data["model"]["transitions"] if row["id"] == "T_UPL_ACCEPT_INIT")
    assert any(node.get("kind") == "PAYLOAD" for node in m2.walk_nodes(accept["guard"]))
    assert data["model"]["events"]
    assert any(row["id"] == "EV_DL_WRQ_LUR" for row in data["model"]["events"])
    assert errors(data) == []
    assert data["reviewControl"]["blocksFinalApproval"] is True
    assert any(row["id"] == "W-LUR-AFTER-READY" for row in data["discreteWitnesses"])
    lur = next(row for row in data["model"]["transitions"] if row["id"] == "T_UPL_LUR_WRQ")
    assert lur["event"] == "EV_DL_WRQ_LUR"


def _witness(data: dict, wid: str) -> dict:
    return next(row for row in data["discreteWitnesses"] if row["id"] == wid)


def test_list_ready_is_required_before_lur_wrq() -> None:
    data = package()
    assert errors(data) == []
    offered = _witness(data, "W-LIST-OFFERED-NOT-READY")
    assert offered["steps"][-1]["transitionId"] == "T_UPL_LUR_WRQ"
    assert offered["steps"][-1]["expectEnabled"] is False
    ready = _witness(data, "W-LUR-AFTER-READY")
    ids = [step["transitionId"] for step in ready["steps"]]
    assert ids.index("T_UPL_WAIT_LUS0001") < ids.index("T_UPL_LUR_WRQ")
    lus = next(step for step in ready["steps"] if step["transitionId"] == "T_UPL_WAIT_LUS0001")
    assert lus["expectVariables"]["targetListReady"] == "TRUE"
    wait = _witness(data, "W-WAIT-NOT-BEFORE")
    wait_ids = [step["transitionId"] for step in wait["steps"]]
    assert wait_ids.index("T_UPL_WAIT_LUS0001") < wait_ids.index("T_UPL_LUR_WRQ")
    session = _witness(data, "W-SESSION-RESET")
    assert session["steps"][-1]["transitionId"] == "T_UPL_LUR_WRQ"
    assert session["steps"][-1]["expectEnabled"] is False
    start = next(step for step in session["steps"] if step["transitionId"] == "T_UPL_LUI_RRQ_AFTER_INF")
    assert start["expectVariables"]["targetListReady"] == "FALSE"

    data = copy.deepcopy(package())
    witness = _witness(data, "W-LUR-AFTER-READY")
    witness["steps"] = [step for step in witness["steps"] if step.get("transitionId") != "T_UPL_WAIT_LUS0001"]
    refresh_summary(data)
    assert any("enablement" in item or "W-LUR-AFTER-READY" in item for item in errors(data))

    data = copy.deepcopy(package())
    wrq = next(row for row in data["model"]["transitions"] if row["id"] == "T_UPL_LUR_WRQ")
    wrq["guard"]["args"] = [
        item for item in wrq["guard"]["args"] if item.get("left", {}).get("name") != "targetListReady"
    ]
    refresh_summary(data)
    assert any("list-ready" in item or "LUS 0001" in item for item in errors(data))


def _binding(data: dict, requirement_id: str) -> dict:
    return next(row for row in data["sequenceEndpointBindings"] if row["requirementId"] == requirement_id)


def _event(data: dict, event_id: str) -> dict:
    return next(row for row in data["model"]["events"] if row["id"] == event_id)


def test_lur_write_endpoints_match_visual_chart() -> None:
    data = package()
    assert errors(data) == []
    expected = {
        "CRS-M1-00365": ("T_UPL_LUR_WRQ", "EV_DL_WRQ_LUR", "DATA-LOADER", "TARGET-HARDWARE", "DL-TO-TH"),
        "CRS-M1-00366": ("T_UPL_LUR_ACK", "EV_TH_ACK_LUR", "TARGET-HARDWARE", "DATA-LOADER", "TH-TO-DL"),
        "CRS-M1-00367": ("T_UPL_LUR_XFER", "EV_DL_DATA_LUR", "DATA-LOADER", "TARGET-HARDWARE", "DL-TO-TH"),
    }
    for rid, (tid, eid, actor, receiver, direction) in expected.items():
        row = _binding(data, rid)
        assert row["transitionId"] == tid
        assert row["eventId"] == eid
        assert row["actor"] == actor
        assert row["receiver"] == receiver
        assert row["direction"] == direction
        assert row["layer"] == "NETWORK-VISIBLE"
        assert _event(data, eid)["direction"] == direction
        assert "DLA" not in {row["actor"], row["receiver"]}
    ready = _witness(data, "W-LUR-AFTER-READY")
    ids = [step["transitionId"] for step in ready["steps"]]
    assert ids.index("T_UPL_LUR_WRQ") < ids.index("T_UPL_LUR_ACK") < ids.index("T_UPL_LUR_XFER")


def test_lur_endpoint_mutations_fail_after_fingerprint_refresh() -> None:
    m1 = json.loads((ROOT / "configs/requirements/arinc_615a3_m1_crs.json").read_text(encoding="utf-8"))
    by_id = {row["id"]: row for row in m1["requirements"]}

    by_id["CRS-M1-00365"]["semantic"]["receiver"] = "DLA"
    found = errors(package(), m1=m1)
    assert any("CRS-M1-00365" in item and "receiver" in item for item in found)
    assert not any("receiver is not DLA" in item for item in found)

    by_id["CRS-M1-00365"]["semantic"]["receiver"] = "DATA-LOADER"
    found = errors(package(), m1=m1)
    assert any("CRS-M1-00365" in item and ("receiver" in item or "endpoint" in item) for item in found)

    by_id["CRS-M1-00365"]["semantic"]["receiver"] = "TARGET-HARDWARE"
    by_id["CRS-M1-00366"]["semantic"]["actor"] = "DATA-LOADER"
    by_id["CRS-M1-00366"]["semantic"]["receiver"] = "TARGET-HARDWARE"
    found = errors(package(), m1=m1)
    assert any("CRS-M1-00366" in item and ("actor" in item or "receiver" in item or "endpoint" in item) for item in found)

    data = copy.deepcopy(package())
    _event(data, "EV_TH_ACK_LUR")["direction"] = "DL-TO-TH"
    refresh_summary(data)
    assert any("CRS-M1-00366" in item and "direction" in item for item in errors(data))

    data = copy.deepcopy(package())
    _event(data, "EV_DL_DATA_LUR")["direction"] = "TH-TO-DL"
    refresh_summary(data)
    assert any("CRS-M1-00367" in item and "direction" in item for item in errors(data))

    data = copy.deepcopy(package())
    _binding(data, "CRS-M1-00365")["receiver"] = "DATA-LOADER"
    refresh_summary(data)
    assert any("CRS-M1-00365" in item and ("endpoint" in item or "receiver" in item or "direction" in item) for item in errors(data))


def _first_binary(node: dict, op: str) -> dict:
    for item in m2.walk_nodes(node):
        if item.get("kind") == "BINARY" and item.get("op") == op:
            return item
    raise AssertionError(op)


def _rewrite_retry_grouping(expr: dict) -> None:
    for node in m2.walk_nodes(expr):
        if node.get("kind") != "BINARY" or node.get("op") != "MUL":
            continue
        left, right = node.get("left") or {}, node.get("right") or {}
        if left.get("op") == "MUL":
            inner_right = left.get("right") or {}
            if inner_right.get("op") == "ADD" and right.get("name") == "TFTP_TO":
                node["left"] = left["left"]
                node["right"] = {
                    "kind": "BINARY",
                    "op": "ADD",
                    "left": inner_right["left"],
                    "right": {
                        "kind": "BINARY",
                        "op": "MUL",
                        "left": inner_right["right"],
                        "right": right,
                        "unit": node.get("unit"),
                    },
                    "unit": node.get("unit"),
                }
                return
        if left.get("op") == "ADD" and right.get("name") == "TFTP_TO":
            node["op"] = "ADD"
            node["left"] = left["left"]
            node["right"] = {
                "kind": "BINARY",
                "op": "MUL",
                "left": left["right"],
                "right": right,
                "unit": node.get("unit"),
            }
            return
    raise AssertionError("retry grouping not found")


def test_equation_structure_mutations_fail_after_fingerprint_refresh() -> None:
    source = next(
        item["sourceRelation"]
        for item in package()["timingCatalog"]
        if item["requirementId"] == "CRS-M1-00188"
    )
    parsed = m2.parse_source_equation(source)
    assert parsed is not None and parsed["op"] == "GT"

    data = copy.deepcopy(package())
    equation = next(item for item in data["timingCatalog"] if item["requirementId"] == "CRS-M1-00188")
    equation["expression"]["left"], equation["expression"]["right"] = (
        equation["expression"]["right"],
        equation["expression"]["left"],
    )
    refresh_summary(data)
    assert any("equation structure" in item for item in errors(data))

    data = copy.deepcopy(package())
    equation = next(item for item in data["timingCatalog"] if item["requirementId"] == "CRS-M1-00188")
    div = _first_binary(equation["expression"], "DIV")
    div["left"], div["right"] = div["right"], div["left"]
    refresh_summary(data)
    assert any("equation structure" in item for item in errors(data))

    data = copy.deepcopy(package())
    equation = next(item for item in data["timingCatalog"] if item["requirementId"] == "CRS-M1-00188")
    _rewrite_retry_grouping(equation["expression"])
    refresh_summary(data)
    assert any("equation structure" in item for item in errors(data))

    data = copy.deepcopy(package())
    equation = next(item for item in data["timingCatalog"] if item["requirementId"] == "CRS-M1-00188")
    four = next(
        node
        for node in m2.walk_nodes(equation["expression"])
        if node.get("kind") == "LITERAL" and node.get("value") == 4
    )
    four["value"] = 5
    refresh_summary(data)
    assert any("equation structure" in item for item in errors(data))
