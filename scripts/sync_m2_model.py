#!/usr/bin/env python3
"""Validate the authoritative M2 model package and render its review-only view."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PATH = ROOT / "configs/models/arinc_615a3_m2_model.json"
SCHEMA_PATH = ROOT / "configs/models/m2_model_package.schema.json"
VIEW_PATH = ROOT / "docs/control/models/ARINC615A3_M2_MODEL_REVIEW_VIEW.md"
SOURCE_REGISTER_PATH = ROOT / "configs/research/controlled_sources.json"
M1_PATH = ROOT / "configs/requirements/arinc_615a3_m1_crs.json"
EXPR_OPS = {"ADD", "SUB", "MUL", "DIV"}
CLOSED_ACTION_WITHOUT_EVIDENCE = {"CLOSED", "CLOSED-IN-THIS-PR"}
GITHUB_APPROVED = "APPROVED"


class M2Error(ValueError):
    pass


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def git_blob(commit: str, path: str) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", f"{commit}:{path}"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def expr_errors(node: Any, symbols: set[str], path: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(node, dict) or "kind" not in node:
        return [f"{path} is not a restricted AST"]
    kind = node["kind"]
    if kind == "LITERAL":
        if not isinstance(node.get("value"), (int, float)):
            errors.append(f"{path} literal value is not numeric")
    elif kind == "SYMBOL":
        name = node.get("name")
        if name not in symbols:
            errors.append(f"{path} symbol {name} is undefined")
    elif kind == "BINARY":
        if node.get("op") not in EXPR_OPS:
            errors.append(f"{path} uses unsupported operator {node.get('op')}")
        errors.extend(expr_errors(node.get("left"), symbols, path + ".left"))
        errors.extend(expr_errors(node.get("right"), symbols, path + ".right"))
    else:
        errors.append(f"{path} AST kind {kind} is not permitted")
    if "eval" in json.dumps(node).lower() or "__" in json.dumps(node):
        errors.append(f"{path} contains disallowed evaluation payload")
    return errors


def graph_errors(model: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    states = {row["id"]: row for row in model.get("states", [])}
    events = {row["id"] for row in model.get("events", [])}
    clocks = {row["id"] for row in model.get("clocks", [])}
    initial = model.get("initialState")
    if initial not in states:
        errors.append("model has no valid initial state")
        return errors
    trans = model.get("transitions", [])
    ids = [row.get("id") for row in trans]
    if len(ids) != len(set(ids)):
        errors.append("duplicate transition id")
    outgoing: dict[str, list[str]] = defaultdict(list)
    incoming: dict[str, list[str]] = defaultdict(list)
    for row in trans:
        src, tgt, event = row.get("source"), row.get("target"), row.get("event")
        if src not in states or tgt not in states:
            errors.append(f"transition {row.get('id')} has a dangling state")
        if event not in events:
            errors.append(f"transition {row.get('id')} has an unknown event")
        for clock in row.get("resets", []):
            if clock not in clocks:
                errors.append(f"transition {row.get('id')} resets unknown clock {clock}")
        if src in states:
            outgoing[src].append(row.get("id"))
        if tgt in states:
            incoming[tgt].append(row.get("id"))
    reachable: set[str] = set()
    queue = deque([initial])
    while queue:
        node = queue.popleft()
        if node in reachable:
            continue
        reachable.add(node)
        for row in trans:
            if row.get("source") == node and row.get("target") not in reachable:
                queue.append(row["target"])
    unexplained = sorted(set(states) - reachable)
    if unexplained:
        errors.append(f"unreachable states without explanation: {unexplained}")
    terminals = {sid for sid, row in states.items() if row.get("terminal")}
    for sid, row in states.items():
        if row.get("terminal") and sid not in {"S_ABORTED", "S_FAILED", "S_INF_REJECTED", "S_UPL_REJECTED", "S_UPL_COMPLETE"}:
            errors.append(f"unexpected terminal {sid}")
    return errors


def package_errors(
    data: dict[str, Any],
    register: dict[str, Any] | None = None,
    m1: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    register = register or json.loads(SOURCE_REGISTER_PATH.read_text(encoding="utf-8"))
    m1 = m1 or json.loads(M1_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        jsonschema.Draft202012Validator(schema).validate(data)
    except jsonschema.ValidationError as exc:
        errors.append(f"schema: {exc.message}")
        return errors

    acc = data["inputAcceptance"]
    if acc.get("githubReviewState") == GITHUB_APPROVED:
        errors.append("network inputAcceptance cannot disguise COMMENTED as APPROVED")
    if acc.get("independenceClaim") not in {
        "NOT-CLAIMED-NAMED-INDEPENDENT-REVIEWER",
        "REPOSITORY-OWNER-ACCEPTED-CONTROL-SIGNOFF",
    } and "NOT-CLAIMED" not in str(acc.get("independenceClaim")):
        errors.append("inputAcceptance independence claim is not controlled")
    if acc.get("mergeSecondParent") != acc.get("approvedHead"):
        errors.append("inputAcceptance second parent is not the approved Head")
    if acc.get("mergeParents") != [acc.get("mergeParents", [None, None])[0], acc.get("approvedHead")]:
        if not (isinstance(acc.get("mergeParents"), list) and len(acc["mergeParents"]) == 2 and acc["mergeParents"][1] == acc.get("approvedHead")):
            errors.append("inputAcceptance merge parents must be exactly two with approved Head second")
    if acc.get("mainCiHead") != acc.get("mergeCommit"):
        errors.append("CI binding is not the merge commit")
    recorded_tree = acc.get("mergeTree")
    try:
        actual_tree = subprocess.check_output(
            ["git", "rev-parse", f"{acc.get('mergeCommit')}^{{tree}}"],
            cwd=ROOT, text=True, stderr=subprocess.DEVNULL,
        ).strip()
        if actual_tree and recorded_tree and actual_tree != recorded_tree:
            errors.append("inputAcceptance merge tree disagrees with git")
    except (OSError, subprocess.CalledProcessError):
        pass
    for item in acc.get("inputs", []):
        blob = git_blob(acc.get("baseCommit", ""), item.get("path", ""))
        if blob and blob != item.get("gitBlobOid"):
            errors.append(f"input blob disagrees for {item.get('path')}")
        if item.get("gitBlobOid") and len(str(item.get("gitBlobOid"))) != 40:
            errors.append(f"input blob oid is not a git object id: {item.get('path')}")

    m1_ids = [row["id"] for row in m1["requirements"]]
    disp = data["requirementDispositions"]
    disp_ids = [row.get("requirementId") for row in disp]
    if sorted(disp_ids) != sorted(m1_ids):
        errors.append("requirement dispositions do not partition M1 requirements")
    if len(disp_ids) != len(set(disp_ids)):
        errors.append("duplicate requirement disposition")
    kinds_by_req: dict[str, set[str]] = defaultdict(set)
    for row in disp:
        if isinstance(row.get("requirementId"), str) and isinstance(row.get("kind"), str):
            kinds_by_req[row["requirementId"]].add(row["kind"])
    dual = [
        rid
        for rid, kinds in kinds_by_req.items()
        if kinds & {"MODELED", "MODELED-TIMING"} and "DEFERRED" in kinds
    ]
    if dual:
        errors.append("requirement cannot be implemented and deferred")

    traces = data["traceRelations"]
    if len({row["id"] for row in traces}) != len(traces):
        errors.append("duplicate trace id")
    modeled = {row["requirementId"] for row in disp if row["kind"] in {"MODELED", "MODELED-TIMING", "DATA-CONSTRAINT", "SCOPE-CONSTRAINT", "DEPENDENCY-BLOCKED", "INTERFACE-PREMISE"}}
    traced = {row["requirementId"] for row in traces}
    missing = sorted(set(m1_ids) - traced)
    if missing:
        errors.append(f"included obligations lack traces: {missing[:8]}")
    trans_ids = {row["id"] for row in data["model"]["transitions"]}
    clock_ids = {row["id"] for row in data["model"]["clocks"]}
    var_ids = {row["id"] for row in data["model"]["variables"]}
    iface_ids = set(data["model"].get("interfaces", {}))
    for row in traces:
        kind, target = row.get("targetKind"), row.get("targetId")
        if kind == "TRANSITION" and target not in trans_ids:
            errors.append(f"trace {row.get('id')} points at missing transition")
        if kind == "CLOCK" and target not in clock_ids:
            errors.append(f"trace {row.get('id')} points at missing clock")
        if kind == "VARIABLE" and target not in var_ids:
            errors.append(f"trace {row.get('id')} points at missing variable")
        if kind == "INTERFACE" and target not in iface_ids:
            errors.append(f"trace {row.get('id')} points at missing interface")
        req = next((item for item in m1["requirements"] if item["id"] == row.get("requirementId")), None)
        if req and row.get("polarity") != req["semantic"]["polarity"]:
            errors.append(f"trace {row.get('id')} polarity drifted from M1")
        if req and row.get("sourceModality") != req["sourceModality"]:
            errors.append(f"trace {row.get('id')} modality drifted from M1")

    errors.extend(graph_errors(data["model"]))
    dl_out = set(data["scope"]["observationBoundary"]["dataLoader"]["outputs"])
    th_out = set(data["scope"]["observationBoundary"]["targetHardware"]["outputs"])
    if dl_out & th_out & {"EV_DL_RRQ_LCI", "EV_TH_ACCEPT_INF"}:
        # overlapping generic events are allowed; send/receive of LCI must not swap
        pass
    if "EV_DL_RRQ_LCI" in th_out:
        errors.append("data-loader LCI RRQ cannot be a target-hardware output")
    if "EV_TH_ACCEPT_INF" in dl_out:
        errors.append("target-hardware accept cannot be a data-loader output")
    if data["scope"].get("afdxSelected") or data["scope"].get("p3ProfiledDeviations"):
        errors.append("scope cannot activate AFDX or P3 profiled deviations")
    if data["scope"].get("networkMode") != "COMPLIANT":
        errors.append("network mode must remain COMPLIANT")

    symbols = {row["id"] for row in data["model"]["parameters"]} | clock_ids
    for row in data["timingCatalog"]:
        lower, upper = row.get("lowerBound"), row.get("upperBound")
        if isinstance(lower, (int, float)) and isinstance(upper, (int, float)) and lower > upper:
            errors.append(f"timing {row.get('id')} bounds are reversed")
        if row.get("boundKind") == "UNRESOLVED" and row.get("staticCheck") not in {"NOT-CHECKED", "UNRESOLVED"}:
            errors.append(f"timing {row.get('id')} unresolved bound cannot be PASS")
        if row.get("expression"):
            errors.extend(expr_errors(row["expression"], symbols, f"timing:{row.get('id')}"))
        if row.get("clockId") not in clock_ids:
            errors.append(f"timing {row.get('id')} clock is missing")
        if row.get("unit") not in {"s", "ms", "us", "ns", "1"}:
            errors.append(f"timing {row.get('id')} unit drifted")
        if not row.get("errorBudgetClass"):
            errors.append(f"timing {row.get('id')} lacks error-budget semantics")
        if not row.get("observationWindow"):
            errors.append(f"timing {row.get('id')} lacks observation window")

    nrr = m1.get("networkReferenceReview", {})
    m1_rel = {row["id"] for row in nrr.get("relations", [])}
    m2_rel = {row["relationId"] for row in data["networkRelationDispositions"]}
    if m1_rel != m2_rel:
        errors.append("network relations are not fully disposed")
    if len({row.get("m2Disposition") for row in data["networkRelationDispositions"]}) < 2:
        errors.append("network dispositions cannot be a single blanket class")
    if all(row.get("m2Disposition") == "NOT-APPLICABLE" for row in data["networkRelationDispositions"]):
        errors.append("network dispositions cannot all be NOT-APPLICABLE")

    caps = {row["id"]: row for row in register.get("capabilities", [])}
    for cap in caps.values():
        if cap.get("status") == "ESTABLISHED":
            errors.append(f"capability {cap['id']} cannot be ESTABLISHED in this M2 candidate")
    if "ARINC-645" not in {row["id"] for row in register.get("openDependencies", [])}:
        errors.append("ARINC 645 open dependency was removed")
    blocked = caps.get("CRC-VALIDATION", {}).get("blockedBy", [])
    if "ARINC-645" not in blocked:
        errors.append("CRC-VALIDATION is no longer blocked by ARINC-645")
    if data["model"]["interfaces"]["IF_INTEGRITY"].get("blockedBy") != ["ARINC-645"]:
        errors.append("integrity interface lost its ARINC 645 guard")

    for row in data["actions"]:
        status = row.get("status")
        if status in CLOSED_ACTION_WITHOUT_EVIDENCE and not row.get("evidence") and row.get("id") not in {"README-P2-DISPLAY"}:
            errors.append(f"action {row.get('id')} closed without evidence")
        if status in CLOSED_ACTION_WITHOUT_EVIDENCE and row.get("id") in {"A-4", "F-1", "F-2", "NET-ISSUE-EDITION"}:
            errors.append(f"action {row.get('id')} cannot be silently CLOSED")
        if not row.get("ownerRole") or not row.get("deadlineGate"):
            errors.append(f"action {row.get('id')} lacks ownerRole or deadlineGate")

    summary = data["inventorySummary"]
    expected = {
        "requirementCount": len(m1["requirements"]),
        "dispositionCount": len(disp),
        "traceCount": len(traces),
        "stateCount": len(data["model"]["states"]),
        "transitionCount": len(data["model"]["transitions"]),
        "timingCount": len(data["timingCatalog"]),
        "dispositionsFingerprint": fingerprint(disp),
        "modelFingerprint": fingerprint(data["model"]),
        "timingFingerprint": fingerprint(data["timingCatalog"]),
        "inputFingerprint": fingerprint(acc),
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            errors.append(f"inventorySummary.{key} disagrees after mutation")

    rc = data["reviewControl"]
    if rc.get("reviewHead") != "UNBOUND-DRAFT":
        errors.append("reviewHead must remain UNBOUND-DRAFT on the candidate")
    if rc.get("rg2") not in {"PENDING-EXTERNAL-REVIEW", "PENDING-EXTERNAL-INDEPENDENT-REVIEW"}:
        errors.append("RG2 cannot be self-approved")
    if data["analysisScope"].get("timedReachability") in {None, "PASS"}:
        errors.append("timed reachability cannot be claimed PASS")

    refinements = data["sourceRefinements"]
    if any(row.get("relation") in {"SHARED-WORDS-PROVE-EQUIVALENCE", "BROADCAST-ALL"} for row in refinements):
        errors.append("unsupported refinement relation")
    if not any(row.get("id") == "REF-A2-NO-RFC-1785-ACTIVE-EDGE" for row in refinements):
        errors.append("RFC-1785 negative inventory is missing")
    return errors


def render(data: dict[str, Any]) -> str:
    acc = data["inputAcceptance"]
    model = data["model"]
    lines = [
        "# ARINC 615A-3 M2 observable timed model — review view",
        "",
        "> Generated from `configs/models/arinc_615a3_m2_model.json` by `python scripts/sync_m2_model.py --write`. Do not edit this view.",
        "",
        "## Input acceptance",
        "",
        f"- Approved Head: `{acc['approvedHead']}`",
        f"- Merge: `{acc['mergeCommit']}` parents `{acc['mergeParents'][0]}` + `{acc['mergeParents'][1]}`",
        f"- Tree: `{acc['mergeTree']}`",
        f"- CI: {acc['mainCiUrl']} on `{acc['mainCiHead']}`",
        f"- Sign-off: {acc['signOffUrl']} (`{acc['githubReviewState']}`, `{acc['recordedConclusion']}`)",
        f"- Independence: `{acc['independenceClaim']}`",
        f"- M1 NET-ISSUE-EDITION snapshot blocksM1Approval=`{acc['m1NetIssueEditionSnapshot']['blocksM1Approval']}` — {acc['m1NetIssueEditionSnapshot']['interpretationEn']}",
        "",
        "## Scope",
        "",
        f"- Services: {', '.join(data['scope']['services'])}; deferred {', '.join(data['scope']['deferredServices'])}",
        f"- Network: `{data['scope']['networkMode']}`; AFDX selected `{data['scope']['afdxSelected']}`; P3 profiled `{data['scope']['p3ProfiledDeviations']}`",
        f"- Form: `{model['form']}`; initial `{model['initialState']}`",
        f"- States {len(model['states'])}, transitions {len(model['transitions'])}, clocks {len(model['clocks'])}, events {len(model['events'])}",
        "",
        "## Model states",
        "",
        "| ID | Terminal | Summary |",
        "|---|---|---|",
    ]
    for row in model["states"]:
        lines.append(f"| `{row['id']}` | {row['terminal']} | {row['summaryEn']} |")
    lines += ["", "## Transitions", "", "| ID | Source | Event | Target | Guard | Resets | Requirements |", "|---|---|---|---|---|---|---|"]
    for row in model["transitions"]:
        lines.append(
            f"| `{row['id']}` | `{row['source']}` | `{row['event']}` | `{row['target']}` | `{row['guard']}` | {', '.join(row['resets']) or '—'} | {', '.join(f'`{i}`' for i in row['requirementIds'])} |"
        )
    lines += ["", "## Timing catalog", "", "| ID | CRS | Trigger → response | Clock | Bounds | Check |", "|---|---|---|---|---|---|"]
    for row in data["timingCatalog"]:
        lines.append(
            f"| `{row['id']}` | `{row['requirementId']}` | `{row['trigger']}` → `{row['response']}` | `{row['clockId']}` | `{row['lowerBound']}..{row['upperBound']} {row['unit']}` | `{row['staticCheck']}` |"
        )
    lines += ["", "## Actions", "", "| ID | Status | Owner | Gate |", "|---|---|---|---|"]
    for row in data["actions"]:
        lines.append(f"| `{row['id']}` | `{row['status']}` | `{row['ownerRole']}` | `{row['deadlineGate']}` |")
    lines += ["", "## Source refinements", ""]
    for row in data["sourceRefinements"]:
        lines.append(f"- `{row['id']}` — `{row['disposition']}` — {row.get('rationaleEn', '')}")
    lines += ["", "## Network relation dispositions", ""]
    for row in data["networkRelationDispositions"]:
        lines.append(f"- `{row['relationId']}` → `{row['m2Disposition']}` (M1 `{row['m1Disposition']}`)")
    lines += ["", "## Analysis boundary", "", f"- Untimed: `{data['analysisScope']['untimedReachability']}`", f"- Timed: `{data['analysisScope']['timedReachability']}`", f"- Unproven: {', '.join(data['analysisScope']['unproven'])}", ""]
    lines += ["", "# 中文版", "", "# ARINC 615A-3 M2 可观测时序模型——评审视图", "", "> 由 `configs/models/arinc_615a3_m2_model.json` 经 `python scripts/sync_m2_model.py --write` 生成，禁止手改。", ""]
    lines += [
        "## 输入接受",
        "",
        f"- 批准 Head：`{acc['approvedHead']}`",
        f"- 合并：`{acc['mergeCommit']}` 父提交 `{acc['mergeParents'][0]}` + `{acc['mergeParents'][1]}`",
        f"- 树：`{acc['mergeTree']}`",
        f"- CI：{acc['mainCiUrl']} @ `{acc['mainCiHead']}`",
        f"- 签署：{acc['signOffUrl']}（`{acc['githubReviewState']}`，`{acc['recordedConclusion']}`）",
        f"- 独立性：`{acc['independenceClaim']}`",
        f"- M1 NET-ISSUE-EDITION 快照 blocksM1Approval=`{acc['m1NetIssueEditionSnapshot']['blocksM1Approval']}` — 该布尔值不重新否定已发生合并。",
        "",
        "## 范围",
        "",
        f"- 服务：{', '.join(data['scope']['services'])}；延期 {', '.join(data['scope']['deferredServices'])}",
        f"- 网络：`{data['scope']['networkMode']}`；AFDX `{data['scope']['afdxSelected']}`；P3 裁剪 `{data['scope']['p3ProfiledDeviations']}`",
        f"- 形式：`{model['form']}`；初态 `{model['initialState']}`",
        f"- 状态 {len(model['states'])}，迁移 {len(model['transitions'])}，时钟 {len(model['clocks'])}，事件 {len(model['events'])}",
        "",
        "## 模型状态",
        "",
        "| ID | 终止 | 摘要 |",
        "|---|---|---|",
    ]
    for row in model["states"]:
        lines.append(f"| `{row['id']}` | {row['terminal']} | {row['summaryEn']} |")
    lines += ["", "## 迁移", "", "| ID | 源 | 事件 | 目标 | 守卫 | 复位 | 需求 |", "|---|---|---|---|---|---|---|"]
    for row in model["transitions"]:
        lines.append(
            f"| `{row['id']}` | `{row['source']}` | `{row['event']}` | `{row['target']}` | `{row['guard']}` | {', '.join(row['resets']) or '—'} | {', '.join(f'`{i}`' for i in row['requirementIds'])} |"
        )
    lines += ["", "## 时序目录", "", "| ID | CRS | 触发 → 响应 | 时钟 | 边界 | 检查 |", "|---|---|---|---|---|---|"]
    for row in data["timingCatalog"]:
        lines.append(
            f"| `{row['id']}` | `{row['requirementId']}` | `{row['trigger']}` → `{row['response']}` | `{row['clockId']}` | `{row['lowerBound']}..{row['upperBound']} {row['unit']}` | `{row['staticCheck']}` |"
        )
    lines += ["", "## 行动", "", "| ID | 状态 | 责任 | 门禁 |", "|---|---|---|---|"]
    for row in data["actions"]:
        lines.append(f"| `{row['id']}` | `{row['status']}` | `{row['ownerRole']}` | `{row['deadlineGate']}` |")
    lines += ["", "## 来源精化", ""]
    for row in data["sourceRefinements"]:
        lines.append(f"- `{row['id']}` — `{row['disposition']}` — {row.get('rationaleZh') or row.get('rationaleEn', '')}")
    lines += ["", "## 网络关系处置", ""]
    for row in data["networkRelationDispositions"]:
        lines.append(f"- `{row['relationId']}` → `{row['m2Disposition']}`（M1 `{row['m1Disposition']}`）")
    lines += ["", "## 分析边界", "", f"- 无时：`{data['analysisScope']['untimedReachability']}`", f"- 定时：`{data['analysisScope']['timedReachability']}`", f"- 未证明：{', '.join(data['analysisScope']['unproven'])}", ""]
    return "\n".join(lines)


def load_package() -> dict[str, Any]:
    data = json.loads(PACKAGE_PATH.read_text(encoding="utf-8"))
    errors = package_errors(data)
    if errors:
        raise M2Error("; ".join(errors[:12]))
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        data = load_package()
        expected = render(data)
    except (OSError, json.JSONDecodeError, M2Error) as exc:
        print(f"M2 model validation failed: {exc}", file=sys.stderr)
        return 1
    if args.write:
        VIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
        VIEW_PATH.write_text(expected, encoding="utf-8", newline="\n")
        return 0
    actual = VIEW_PATH.read_text(encoding="utf-8") if VIEW_PATH.exists() else ""
    if actual != expected:
        print("generated M2 review view is stale; run sync_m2_model.py --write", file=sys.stderr)
        return 1
    summary = data["inventorySummary"]
    print(
        "M2 model validation passed: "
        f"requirements={summary['requirementCount']}, transitions={summary['transitionCount']}, timing={summary['timingCount']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
