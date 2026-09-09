#!/usr/bin/env python3
"""Validate the authoritative M2 model package and render its review-only view."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path, PurePosixPath
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PATH = ROOT / "configs/models/arinc_615a3_m2_model.json"
SCHEMA_PATH = ROOT / "configs/models/m2_model_package.schema.json"
VIEW_PATH = ROOT / "docs/control/models/ARINC615A3_M2_MODEL_REVIEW_VIEW.md"
SOURCE_REGISTER_PATH = ROOT / "configs/research/controlled_sources.json"
M1_PATH = ROOT / "configs/requirements/arinc_615a3_m1_crs.json"
EXPR_OPS = {"ADD", "SUB", "MUL", "DIV"}
COMPARE_OPS = {"EQ", "NE", "LT", "LE", "GT", "GE"}
AST_KINDS = {"TRUE", "COMPARE", "AND", "VAR", "CLOCK", "SYMBOL", "LITERAL", "ENUM", "ASSIGN", "BINARY"}
CLOSED_ACTION_WITHOUT_EVIDENCE = {"CLOSED", "CLOSED-IN-THIS-PR"}
FORBIDDEN_SELF_APPROVE = {
    "APPROVE", "APPROVED", "AUTHOR-APPROVED", "SELF-APPROVED", "SELF-APPROVE",
}
GIT_OID_RE = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_M1_INPUT_PATHS = (
    "configs/requirements/arinc_615a3_m1_crs.json",
    "configs/requirements/m1_crs_package.schema.json",
    "configs/requirements/m1_rg0_source_inventory_anchor.json",
    "configs/requirements/m1_semantic_review_assertions.json",
    "configs/requirements/m1_source_section_spans.json",
    "configs/requirements/m1_supplement_dispositions.json",
    "docs/control/requirements/ARINC615A3_M1_CRS_REVIEW_VIEW.md",
)
NARRATIVE_PAIRS = (
    ("summaryEn", "summaryZh"),
    ("noteEn", "noteZh"),
    ("rationaleEn", "rationaleZh"),
    ("meaningEn", "meaningZh"),
    ("predicateEn", "predicateZh"),
    ("behaviorEn", "behaviorZh"),
    ("acceptanceEn", "acceptanceZh"),
    ("compositionEn", "compositionZh"),
    ("eventMappingEn", "eventMappingZh"),
    ("silenceRuleEn", "silenceRuleZh"),
    ("stepSemanticsEn", "stepSemanticsZh"),
    ("finiteDomainEn", "finiteDomainZh"),
    ("errorBudgetEn", "errorBudgetZh"),
    ("observationRoleEn", "observationRoleZh"),
    ("conflictNoteEn", "conflictNoteZh"),
    ("interpretationEn", "interpretationZh"),
    ("delayEn", "delayZh"),
    ("discreteEn", "discreteZh"),
    ("raceEn", "raceZh"),
    ("endpointEn", "endpointZh"),
)
GENERIC_FILE_VARIABLES = {"VAR_PROTOCOL_FILE"}


class M2Error(ValueError):
    pass


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def git_output(git_root: Path, args: list[str]) -> str | None:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=git_root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def git_blob(commit: str, path: str, git_root: Path | None = None) -> str | None:
    return git_output(git_root or ROOT, ["rev-parse", f"{commit}:{path}"])


def require_git_object(git_root: Path, oid: Any, expected: str, label: str) -> list[str]:
    if not isinstance(oid, str) or not GIT_OID_RE.fullmatch(oid):
        return [f"{label} is not a complete git object id"]
    typ = git_output(git_root, ["cat-file", "-t", oid])
    if typ is None:
        return [f"{label} git object is missing"]
    if typ != expected:
        return [f"{label} is {typ}, expected {expected}"]
    return []


def walk_nodes(node: Any) -> list[Any]:
    found: list[Any] = []
    if isinstance(node, dict):
        found.append(node)
        for value in node.values():
            found.extend(walk_nodes(value))
    elif isinstance(node, list):
        for item in node:
            found.extend(walk_nodes(item))
    return found


def ast_clocks(node: Any) -> set[str]:
    return {item["name"] for item in walk_nodes(node) if item.get("kind") == "CLOCK" and item.get("name")}


def ast_symbols(node: Any) -> set[str]:
    names: set[str] = set()
    for item in walk_nodes(node):
        if item.get("kind") in {"SYMBOL", "VAR", "CLOCK"} and item.get("name"):
            names.add(item["name"])
        if item.get("kind") == "ASSIGN" and item.get("target"):
            names.add(item["target"])
    return names


def expr_unit(node: Any) -> str | None:
    if not isinstance(node, dict):
        return None
    kind = node.get("kind")
    if kind in {"LITERAL", "SYMBOL", "CLOCK", "BINARY"}:
        return node.get("unit")
    return None


def ast_errors(
    node: Any,
    symbols: set[str],
    variables: dict[str, dict[str, Any]],
    clocks: set[str],
    path: str,
    *,
    allow_assign: bool = False,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(node, dict) or "kind" not in node:
        return [f"{path} is not a restricted AST"]
    kind = node["kind"]
    if kind not in AST_KINDS:
        return [f"{path} AST kind {kind} is not permitted"]
    dumped = json.dumps(node)
    if "eval" in dumped.lower() or "__" in dumped:
        errors.append(f"{path} contains disallowed evaluation payload")
    if kind == "TRUE":
        return errors
    if kind == "LITERAL":
        value = node.get("value")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            errors.append(f"{path} literal value is not numeric")
        elif isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            errors.append(f"{path} literal is NaN or Infinity")
        return errors
    if kind == "ENUM":
        if not isinstance(node.get("value"), str) or not node["value"]:
            errors.append(f"{path} enum value is missing")
        return errors
    if kind == "SYMBOL":
        if node.get("name") not in symbols:
            errors.append(f"{path} symbol {node.get('name')} is undefined")
        return errors
    if kind == "VAR":
        if node.get("name") not in variables:
            errors.append(f"{path} variable {node.get('name')} is undeclared")
        return errors
    if kind == "CLOCK":
        if node.get("name") not in clocks:
            errors.append(f"{path} clock {node.get('name')} is undeclared")
        return errors
    if kind == "COMPARE":
        if node.get("op") not in COMPARE_OPS:
            errors.append(f"{path} uses unsupported comparison {node.get('op')}")
        errors.extend(ast_errors(node.get("left"), symbols, variables, clocks, path + ".left"))
        errors.extend(ast_errors(node.get("right"), symbols, variables, clocks, path + ".right"))
        return errors
    if kind == "AND":
        args = node.get("args")
        if not isinstance(args, list) or not args:
            errors.append(f"{path} AND requires arguments")
        else:
            for index, arg in enumerate(args):
                errors.extend(ast_errors(arg, symbols, variables, clocks, f"{path}.args[{index}]"))
        return errors
    if kind == "BINARY":
        if node.get("op") not in EXPR_OPS:
            errors.append(f"{path} uses unsupported operator {node.get('op')}")
        left, right = node.get("left"), node.get("right")
        errors.extend(ast_errors(left, symbols, variables, clocks, path + ".left"))
        errors.extend(ast_errors(right, symbols, variables, clocks, path + ".right"))
        if node.get("op") == "DIV" and isinstance(right, dict) and right.get("kind") == "LITERAL" and right.get("value") == 0:
            errors.append(f"{path} divides by zero")
        if node.get("op") in {"ADD", "SUB"}:
            left_unit, right_unit = expr_unit(left), expr_unit(right)
            if left_unit and right_unit and left_unit != right_unit:
                errors.append(f"{path} adds or subtracts mismatched units {left_unit} and {right_unit}")
        return errors
    if kind == "ASSIGN":
        if not allow_assign:
            errors.append(f"{path} assignment is not permitted here")
            return errors
        target = node.get("target")
        if target not in variables:
            errors.append(f"{path} updates undeclared variable {target}")
        errors.extend(ast_errors(node.get("value"), symbols, variables, clocks, path + ".value"))
        return errors
    errors.append(f"{path} AST kind {kind} is not permitted")
    return errors


def narrative_errors(node: Any, path: str = "") -> list[str]:
    errors: list[str] = []
    if isinstance(node, dict):
        for en_key, zh_key in NARRATIVE_PAIRS:
            english = node.get(en_key)
            if not english:
                continue
            zh = node.get(zh_key)
            if not isinstance(zh, str) or not zh.strip():
                errors.append(f"{path}.{zh_key} is missing; English fallback is not allowed")
            elif zh == english:
                errors.append(f"{path}.{zh_key} reuses English text")
        for key, value in node.items():
            errors.extend(narrative_errors(value, f"{path}.{key}" if path else key))
    elif isinstance(node, list):
        for index, item in enumerate(node):
            errors.extend(narrative_errors(item, f"{path}[{index}]"))
    return errors


def graph_errors(model: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    states = {row["id"]: row for row in model.get("states", [])}
    events = {row["id"]: row for row in model.get("events", [])}
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
        if event in set(row.get("outputs") or []):
            errors.append(f"transition {row.get('id')} double-counts its input event as output")
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
    for sid, row in states.items():
        if row.get("terminal") and outgoing.get(sid):
            errors.append(f"terminal {sid} has outgoing transitions")
    return errors


def sequence_errors(model: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    edges = {(row["source"], row["target"]) for row in model.get("transitions", [])}
    states = {row["id"] for row in model.get("states", [])}
    for constraint in model.get("sequenceConstraints", []):
        order = constraint.get("requiredStateOrder") or []
        if any(state not in states for state in order):
            errors.append(f"sequence {constraint.get('id')} names an unknown state")
        for forbidden in constraint.get("forbiddenEdges") or []:
            if tuple(forbidden) in edges:
                errors.append(
                    f"sequence {constraint.get('id')} forbidden edge {forbidden[0]}->{forbidden[1]} is present"
                )
        adjacency: dict[str, set[str]] = defaultdict(set)
        for src, tgt in edges:
            adjacency[src].add(tgt)
        for start, finish in zip(order, order[1:]):
            seen = {start}
            queue = deque([start])
            found = False
            while queue:
                node = queue.popleft()
                if node == finish:
                    found = True
                    break
                for nxt in adjacency[node]:
                    if nxt not in seen:
                        seen.add(nxt)
                        queue.append(nxt)
            if not found:
                errors.append(f"sequence {constraint.get('id')} has no path {start}->{finish}")
    return errors


def timeout_guard_errors(model: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    events = {row["id"]: row for row in model.get("events", [])}
    for row in model.get("transitions", []):
        event = events.get(row.get("event"), {})
        if event.get("visibility") != "ENVIRONMENT":
            continue
        clock_name = event.get("enablingClock")
        if not clock_name:
            errors.append(f"environment event {event.get('id')} lacks enablingClock")
            continue
        if clock_name not in ast_clocks(row.get("guard")):
            errors.append(f"timeout transition {row.get('id')} is not enabled by clock {clock_name}")
    return errors


def clock_reset_errors(model: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    trans = {row["id"]: row for row in model.get("transitions", [])}
    for clock in model.get("clocks", []):
        for tid in clock.get("resetOn", []):
            if tid not in trans:
                errors.append(f"clock {clock['id']} resetOn unknown transition {tid}")
            elif clock["id"] not in trans[tid].get("resets", []):
                errors.append(f"clock {clock['id']} resetOn {tid} is not in that transition resets")
    return errors


def input_identity_errors(acc: dict[str, Any], git_root: Path) -> list[str]:
    errors: list[str] = []
    if acc.get("githubReviewState") in FORBIDDEN_SELF_APPROVE:
        errors.append("network inputAcceptance cannot disguise COMMENTED as APPROVED")
    if acc.get("recordedConclusion") in FORBIDDEN_SELF_APPROVE:
        errors.append("inputAcceptance cannot self-approve the recorded conclusion")
    independence = str(acc.get("independenceClaim") or "")
    if "NOT-CLAIMED" not in independence:
        errors.append("inputAcceptance independence claim is not controlled")
    if "ONLINE" in independence.upper() or "ONLINE" in str(acc.get("signOffKind") or "").upper():
        errors.append("offline validation cannot claim online sign-off verification")

    errors.extend(require_git_object(git_root, acc.get("approvedHead"), "commit", "approvedHead"))
    errors.extend(require_git_object(git_root, acc.get("mergeCommit"), "commit", "mergeCommit"))
    errors.extend(require_git_object(git_root, acc.get("mergeTree"), "tree", "mergeTree"))
    errors.extend(require_git_object(git_root, acc.get("approvedHeadTree"), "tree", "approvedHeadTree"))
    parents = acc.get("mergeParents")
    if not isinstance(parents, list) or len(parents) != 2:
        errors.append("inputAcceptance merge parents must be exactly two")
        return errors
    errors.extend(require_git_object(git_root, parents[0], "commit", "mergeParents[0]"))
    errors.extend(require_git_object(git_root, parents[1], "commit", "mergeParents[1]"))
    if acc.get("mergeSecondParent") != acc.get("approvedHead"):
        errors.append("inputAcceptance second parent is not the approved Head")
    if parents[1] != acc.get("approvedHead"):
        errors.append("inputAcceptance merge parents must be exactly two with approved Head second")
    if acc.get("mainCiHead") != acc.get("mergeCommit"):
        errors.append("CI binding is not the merge commit")

    actual_parents = git_output(git_root, ["rev-parse", f"{acc.get('mergeCommit')}^@"])
    if actual_parents is None:
        errors.append("mergeCommit parents cannot be read from git")
    else:
        actual = actual_parents.split()
        if len(actual) != 2:
            errors.append("mergeCommit does not have exactly two parents")
        elif actual != parents:
            errors.append("recorded merge parents disagree with git")
        elif actual[1] != acc.get("approvedHead"):
            errors.append("git second parent is not the approved Head")

    merge_tree = git_output(git_root, ["rev-parse", f"{acc.get('mergeCommit')}^{{tree}}"])
    approved_tree = git_output(git_root, ["rev-parse", f"{acc.get('approvedHead')}^{{tree}}"])
    if merge_tree is None:
        errors.append("mergeCommit tree cannot be read from git")
    elif merge_tree != acc.get("mergeTree"):
        errors.append("inputAcceptance merge tree disagrees with git")
    if approved_tree is None:
        errors.append("approvedHead tree cannot be read from git")
    elif approved_tree != acc.get("approvedHeadTree"):
        errors.append("approvedHeadTree disagrees with git")
    if acc.get("approvedHeadTree") != acc.get("mergeTree"):
        errors.append("approvedHeadTree must equal the merge tree")

    inputs = acc.get("inputs") or []
    if not inputs:
        errors.append("inputAcceptance inputs are empty")
    paths = [item.get("path") for item in inputs]
    if len(paths) != len(set(paths)):
        errors.append("inputAcceptance input paths are not unique")
    missing_required = [path for path in REQUIRED_M1_INPUT_PATHS if path not in paths]
    if missing_required:
        errors.append(f"inputAcceptance omits required M1 inputs: {missing_required}")
    for item in inputs:
        path = item.get("path", "")
        try:
            posix = PurePosixPath(path)
        except Exception:
            errors.append(f"input path is not relative-safe: {path}")
            continue
        if posix.is_absolute() or ".." in posix.parts:
            errors.append(f"input path is not relative-safe: {path}")
            continue
        errors.extend(require_git_object(git_root, item.get("gitBlobOid"), "blob", f"input {path}"))
        merge_blob = git_blob(str(acc.get("mergeCommit") or ""), path, git_root)
        if merge_blob is None:
            errors.append(f"merge blob for {path} is missing")
        elif merge_blob != item.get("gitBlobOid"):
            errors.append(f"input blob disagrees for {path}")
        worktree_path = git_root / path
        if not worktree_path.is_file():
            errors.append(f"worktree input is missing: {path}")
        else:
            work_blob = git_output(git_root, ["hash-object", str(worktree_path)])
            if work_blob is None:
                errors.append(f"worktree blob for {path} cannot be hashed")
            elif work_blob != item.get("gitBlobOid"):
                errors.append(f"worktree blob disagrees for {path}")
    return errors


def resolve_target(
    kind: str,
    target: str,
    model: dict[str, Any],
    timing_ids: set[str],
) -> bool:
    if kind == "TRANSITION":
        return target in {row["id"] for row in model["transitions"]}
    if kind == "CLOCK":
        return target in {row["id"] for row in model["clocks"]}
    if kind == "VARIABLE":
        return target in {row["id"] for row in model["variables"]}
    if kind == "INTERFACE":
        return target in set(model.get("interfaces", {}))
    if kind == "SCOPE":
        return target == "SCOPE"
    if kind == "TIMING":
        return target in timing_ids
    if kind == "FIELD-CONSTRAINT":
        return target in {row["id"] for row in model.get("fieldConstraints", [])}
    if kind == "STATUS-CONSTRAINT":
        return target in {row["id"] for row in model.get("statusConstraints", [])}
    if kind == "OBJECT-CONSTRAINT":
        return target in {row["id"] for row in model.get("objectConstraints", [])}
    return False


def package_errors(
    data: dict[str, Any],
    register: dict[str, Any] | None = None,
    m1: dict[str, Any] | None = None,
    git_root: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    git_root = Path(git_root or ROOT)
    register = register or json.loads(SOURCE_REGISTER_PATH.read_text(encoding="utf-8"))
    m1 = m1 or json.loads(M1_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        jsonschema.Draft202012Validator(schema).validate(data)
    except jsonschema.ValidationError as exc:
        errors.append(f"schema: {exc.message}")
        return errors

    errors.extend(input_identity_errors(data["inputAcceptance"], git_root))
    errors.extend(narrative_errors(data))

    m1_ids = [row["id"] for row in m1["requirements"]]
    m1_by_id = {row["id"]: row for row in m1["requirements"]}
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
    traced = {row["requirementId"] for row in traces}
    missing = sorted(set(m1_ids) - traced)
    if missing:
        errors.append(f"included obligations lack traces: {missing[:8]}")

    model = data["model"]
    timing_ids = {row["id"] for row in data["timingCatalog"]}
    for row in traces:
        kind, target = row.get("targetKind"), row.get("targetId")
        if target in GENERIC_FILE_VARIABLES:
            errors.append(f"trace {row.get('id')} uses a generic file variable instead of a field constraint")
        if not resolve_target(str(kind), str(target), model, timing_ids):
            errors.append(f"trace {row.get('id')} points at missing {kind}")
        req = m1_by_id.get(row.get("requirementId"))
        if req and row.get("polarity") != req["semantic"]["polarity"]:
            errors.append(f"trace {row.get('id')} polarity drifted from M1")
        if req and row.get("sourceModality") != req["sourceModality"]:
            errors.append(f"trace {row.get('id')} modality drifted from M1")

    traces_by_req: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in traces:
        traces_by_req[row["requirementId"]].append(row)
    for row in disp:
        rid = row["requirementId"]
        targets = set(row.get("modelTargetIds") or [])
        traced_targets = {item["targetId"] for item in traces_by_req.get(rid, [])}
        if targets != traced_targets:
            errors.append(f"disposition {rid} targets are not bidirectional with traces")
        req = m1_by_id.get(rid)
        if req and req.get("fieldConstraint"):
            kinds = {item["targetKind"] for item in traces_by_req.get(rid, [])}
            if "FIELD-CONSTRAINT" not in kinds:
                errors.append(f"{rid} field constraint is not traced to a field predicate")
        if req and req.get("timing"):
            if not any(item["targetKind"] == "TIMING" for item in traces_by_req.get(rid, [])):
                errors.append(f"{rid} timing obligation is not traced to the timing catalog")

    trans_by_id = {row["id"]: row for row in model["transitions"]}
    for row in model["transitions"]:
        for rid in row.get("requirementIds") or []:
            if rid not in m1_by_id:
                errors.append(f"transition {row['id']} cites unknown requirement {rid}")
            elif not any(
                item["targetKind"] == "TRANSITION" and item["targetId"] == row["id"]
                for item in traces_by_req.get(rid, [])
            ):
                errors.append(f"transition {row['id']} requirement {rid} lacks a reverse trace")

    errors.extend(graph_errors(model))
    errors.extend(sequence_errors(model))
    errors.extend(timeout_guard_errors(model))
    errors.extend(clock_reset_errors(model))

    dl_out = set(data["scope"]["observationBoundary"]["dataLoader"]["outputs"])
    if "EV_DL_RRQ_LCI" in data["scope"]["observationBoundary"]["targetHardware"]["outputs"]:
        errors.append("data-loader LCI RRQ cannot be a target-hardware output")
    if "EV_TH_ACCEPT_INF" in dl_out:
        errors.append("target-hardware accept cannot be a data-loader output")
    if data["scope"].get("afdxSelected") or data["scope"].get("p3ProfiledDeviations"):
        errors.append("scope cannot activate AFDX or P3 profiled deviations")
    if data["scope"].get("networkMode") != "COMPLIANT":
        errors.append("network mode must remain COMPLIANT")

    variables = {row["id"]: row for row in model["variables"]}
    for name, row in variables.items():
        if "initial" not in row:
            errors.append(f"variable {name} has no initial value")
        if row.get("type") == "ENUM" and row.get("initial") not in set(row.get("domain") or []):
            errors.append(f"variable {name} initial is outside its domain")
    clocks = {row["id"] for row in model["clocks"]}
    symbols = {row["id"] for row in model["parameters"]} | clocks
    for row in model["transitions"]:
        errors.extend(ast_errors(row.get("guard"), symbols, variables, clocks, f"transition:{row.get('id')}.guard"))
        for index, update in enumerate(row.get("updates") or []):
            errors.extend(
                ast_errors(
                    update, symbols, variables, clocks,
                    f"transition:{row.get('id')}.updates[{index}]",
                    allow_assign=True,
                )
            )
        for output in row.get("outputs") or []:
            if output not in {event["id"] for event in model["events"]}:
                errors.append(f"transition {row.get('id')} output {output} is unknown")
    for row in model.get("invariants", []):
        errors.extend(ast_errors(row.get("expression"), symbols, variables, clocks, f"invariant:{row.get('id')}"))

    m1_timing_ids = {row["id"] for row in m1["requirements"] if "timing" in row}
    catalog_req_ids = {row["requirementId"] for row in data["timingCatalog"]}
    if m1_timing_ids != catalog_req_ids:
        errors.append("timing catalog is not bound to every M1 timing obligation")
    for row in data["timingCatalog"]:
        req = m1_by_id.get(row.get("requirementId"))
        timing = (req or {}).get("timing") or {}
        if timing:
            if row.get("unit") != timing.get("unit"):
                errors.append(f"timing {row.get('id')} unit drifted from M1 without conversion")
            if row.get("sourceRelation") != timing.get("sourceRelation"):
                errors.append(f"timing {row.get('id')} sourceRelation drifted from M1")
            if row.get("upperBoundary") != timing.get("upperBoundary") or row.get("lowerBoundary") != timing.get("lowerBoundary"):
                errors.append(f"timing {row.get('id')} endpoint drifted from M1")
        lower, upper = row.get("lowerBound"), row.get("upperBound")
        if isinstance(lower, (int, float)) and isinstance(upper, (int, float)) and lower > upper:
            errors.append(f"timing {row.get('id')} bounds are reversed")
        if row.get("boundKind") == "UNRESOLVED" and row.get("staticCheck") not in {"NOT-CHECKED", "UNRESOLVED"}:
            errors.append(f"timing {row.get('id')} unresolved bound cannot be PASS")
        errors.extend(ast_errors(row.get("expression"), symbols, variables, clocks, f"timing:{row.get('id')}"))
        if row.get("clockId") not in clocks:
            errors.append(f"timing {row.get('id')} clock is missing")
        if not row.get("errorBudgetClass"):
            errors.append(f"timing {row.get('id')} lacks error-budget semantics")
        if not row.get("observationWindow"):
            errors.append(f"timing {row.get('id')} lacks observation window")
        if row.get("requirementId") == "CRS-M1-00188":
            names = ast_symbols(row.get("expression"))
            required = {"DLP_TO", "DURATION_TIME", "DLP_RETRY", "TFTP_RETRY", "TFTP_TO"}
            if not required <= names:
                errors.append("timing CRS-M1-00188 AST dropped retry or duration terms")
            if "NETWORK_TERM" in names:
                errors.append("timing CRS-M1-00188 invented NETWORK_TERM")

    nrr = m1.get("networkReferenceReview", {})
    m1_rel = {row["id"] for row in nrr.get("relations", [])}
    m2_rel = {row["relationId"] for row in data["networkRelationDispositions"]}
    if m1_rel != m2_rel:
        errors.append("network relations are not fully disposed")
    if len({row.get("m2Disposition") for row in data["networkRelationDispositions"]}) < 2:
        errors.append("network dispositions cannot be a single blanket class")
    if all(row.get("m2Disposition") == "NOT-APPLICABLE" for row in data["networkRelationDispositions"]):
        errors.append("network dispositions cannot all be NOT-APPLICABLE")

    assumption_ids = {row["id"] for row in nrr.get("infrastructureAssumptions", [])}
    premise_ids = {row["id"] for row in data["infrastructurePremises"]}
    if not assumption_ids <= premise_ids:
        errors.append("infrastructure premises omit M1 assumptions")

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
    if data["model"]["interfaces"]["IF_TFTP_BLOCKSIZE"].get("status") == "ESTABLISHED":
        errors.append("block-size capability cannot be ESTABLISHED")

    silent_close = {"A-4", "F-1", "F-2", "NET-ISSUE-EDITION", "M1-FILE-IDENTITY-6-4-4"}
    for row in data["actions"]:
        status = row.get("status")
        if status in CLOSED_ACTION_WITHOUT_EVIDENCE and not row.get("evidence"):
            errors.append(f"action {row.get('id')} closed without evidence")
        if status in CLOSED_ACTION_WITHOUT_EVIDENCE and row.get("id") in silent_close:
            errors.append(f"action {row.get('id')} cannot be silently CLOSED")
        if not row.get("ownerRole") or not row.get("deadlineGate"):
            errors.append(f"action {row.get('id')} lacks ownerRole or deadlineGate")

    summary = data["inventorySummary"]
    expected = {
        "requirementCount": len(m1["requirements"]),
        "dispositionCount": len(disp),
        "traceCount": len(traces),
        "stateCount": len(model["states"]),
        "transitionCount": len(model["transitions"]),
        "timingCount": len(data["timingCatalog"]),
        "dispositionsFingerprint": fingerprint(disp),
        "modelFingerprint": fingerprint(model),
        "timingFingerprint": fingerprint(data["timingCatalog"]),
        "inputFingerprint": fingerprint(data["inputAcceptance"]),
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            errors.append(f"inventorySummary.{key} disagrees after mutation")
    for key, payload in (
        ("refinementFingerprint", data["sourceRefinements"]),
        ("actionFingerprint", data["actions"]),
        ("premiseFingerprint", data["infrastructurePremises"]),
    ):
        if summary.get(key) and summary.get(key) != fingerprint(payload):
            errors.append(f"inventorySummary.{key} disagrees after mutation")

    rc = data["reviewControl"]
    if rc.get("reviewHead") != "UNBOUND-DRAFT":
        errors.append("reviewHead must remain UNBOUND-DRAFT on the candidate")
    for field in ("rg0", "rg1", "rg2"):
        if rc.get(field) in FORBIDDEN_SELF_APPROVE:
            errors.append(f"{field} cannot be self-approved")
    if data["analysisScope"].get("timedReachability") in {None, "PASS"}:
        errors.append("timed reachability cannot be claimed PASS")

    refinements = data["sourceRefinements"]
    if any(row.get("relation") in {"SHARED-WORDS-PROVE-EQUIVALENCE", "BROADCAST-ALL"} for row in refinements):
        errors.append("unsupported refinement relation")
    rfc_targets = {row.get("toSourceId") for row in refinements}
    if any("TFTP-BLOCK-SIZE" in (m1_by_id[rid]["semantic"]["objects"]) for rid in m1_ids if rid in m1_by_id):
        if "RFC-2348" not in rfc_targets:
            errors.append("block-size obligation has no RFC-2348 candidate edge")
    named_rfc = {
        dep
        for req in m1["requirements"]
        for dep in req.get("dependencyIds", [])
    }
    for dep in register.get("openDependencies", []):
        source_id = dep.get("id")
        if not isinstance(source_id, str) or not source_id.startswith("RFC-"):
            continue
        if source_id in {"RFC-1785", "RFC-2349"} and f"DEP-{source_id}" not in named_rfc:
            if not any(
                row.get("toSourceId") == source_id and "NO-" in str(row.get("relation"))
                for row in refinements
            ):
                errors.append(f"negative inventory is missing for {source_id}")
    for row in refinements:
        target_req = row.get("toRequirementId")
        if target_req and target_req not in m1_by_id:
            errors.append(f"refinement {row.get('id')} toRequirementId is not an M1 requirement")
        source_req = row.get("fromRequirementId")
        if source_req and source_req not in m1_by_id:
            errors.append(f"refinement {row.get('id')} fromRequirementId is not an M1 requirement")
        locator = row.get("toLocator") or {}
        if locator.get("sourceId", "").startswith("RFC-"):
            dep = next((item for item in register.get("openDependencies", []) if item["id"] == locator["sourceId"]), None)
            public = (dep or {}).get("publicRetrieval") or {}
            if locator.get("retrievedSha256") and locator["retrievedSha256"] != public.get("retrievedSha256"):
                errors.append(f"refinement {row.get('id')} RFC hash disagrees with the register")
            if not locator.get("clause"):
                errors.append(f"refinement {row.get('id')} RFC locator lacks a section clause")
            if locator.get("sourceUnitId") in {None, locator.get("sourceId")}:
                errors.append(f"refinement {row.get('id')} RFC locator is not section-atomic")
    return errors


def _table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return lines


def _ast(node: Any) -> str:
    return json.dumps(node, ensure_ascii=False, separators=(",", ":"))


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
        f"- Tree: `{acc['mergeTree']}` / approved-head tree `{acc['approvedHeadTree']}`",
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
        f"- {model['stepSemanticsEn']}",
        f"- {data['scope']['observationBoundary']['eventMappingEn']}",
        "",
        "## Events",
        "",
    ]
    lines += _table(
        ["ID", "Visibility", "Summary"],
        [[f"`{row['id']}`", row["visibility"], row["summaryEn"]] for row in model["events"]],
    )
    lines += ["", "## States", ""]
    lines += _table(
        ["ID", "Terminal", "Summary"],
        [[f"`{row['id']}`", str(row["terminal"]), row["summaryEn"]] for row in model["states"]],
    )
    lines += ["", "## Variables", ""]
    lines += _table(
        ["ID", "Type", "Initial", "Domain"],
        [[
            f"`{row['id']}`",
            row["type"],
            str(row["initial"]),
            ", ".join(row.get("domain") or []) or "—",
        ] for row in model["variables"]],
    )
    lines += ["", "## Parameters", ""]
    lines += _table(
        ["ID", "Unit", "Kind", "Value", "Meaning"],
        [[
            f"`{row['id']}`",
            row["unit"],
            row["kind"],
            str(row.get("value")),
            row["meaningEn"],
        ] for row in model["parameters"]],
    )
    lines += ["", "## Clocks", ""]
    lines += _table(
        ["ID", "Scope", "Correlation", "Reset on", "Meaning"],
        [[
            f"`{row['id']}`",
            row["scope"],
            row["correlationKey"],
            ", ".join(f"`{item}`" for item in row["resetOn"]),
            row["meaningEn"],
        ] for row in model["clocks"]],
    )
    lines += ["", "## Invariants", ""]
    lines += _table(
        ["ID", "States", "AST", "Note"],
        [[
            f"`{row['id']}`",
            ", ".join(f"`{item}`" for item in row["states"]),
            f"`{_ast(row['expression'])}`",
            row["noteEn"],
        ] for row in model["invariants"]],
    )
    lines += ["", "## Transitions", ""]
    lines += _table(
        ["ID", "Source", "Event", "Target", "Guard", "Updates", "Outputs", "Resets", "Requirements"],
        [[
            f"`{row['id']}`",
            f"`{row['source']}`",
            f"`{row['event']}`",
            f"`{row['target']}`",
            f"`{_ast(row['guard'])}`",
            f"`{_ast(row['updates'])}`" if row["updates"] else "—",
            ", ".join(f"`{item}`" for item in row["outputs"]) or "—",
            ", ".join(row["resets"]) or "—",
            ", ".join(f"`{item}`" for item in row["requirementIds"]),
        ] for row in model["transitions"]],
    )
    lines += ["", "## Sequence constraints", ""]
    for row in model["sequenceConstraints"]:
        lines.append(
            f"- `{row['id']}` order {' → '.join(f'`{item}`' for item in row['requiredStateOrder'])}; "
            f"forbidden {row['forbiddenEdges']}; {row['noteEn']}"
        )
    lines += ["", "## Field constraints", ""]
    lines += _table(
        ["ID", "File", "Field", "CRS", "Check"],
        [[
            f"`{row['id']}`",
            row["protocolFile"],
            row["fieldId"],
            f"`{row['m1RequirementId']}`",
            row["checkLocation"],
        ] for row in model["fieldConstraints"]],
    )
    lines += ["", "## Status constraints", ""]
    lines += _table(
        ["ID", "CRS", "Code", "Check"],
        [[
            f"`{row['id']}`",
            f"`{row['m1RequirementId']}`",
            str(row.get("code") or row.get("kind")),
            row["checkLocation"],
        ] for row in model["statusConstraints"]],
    )
    lines += ["", "## Object constraints", ""]
    lines += _table(
        ["ID", "CRS", "Action", "Check"],
        [[
            f"`{row['id']}`",
            f"`{row['m1RequirementId']}`",
            row["action"],
            row["checkLocation"],
        ] for row in model["objectConstraints"]],
    )
    lines += ["", "## Interfaces", ""]
    for name, row in model["interfaces"].items():
        lines.append(f"- `{name}` `{row['kind']}` — {row['noteEn']}")
    lines += ["", "## Timing catalog", ""]
    lines += _table(
        ["ID", "CRS", "Clock", "Bounds", "AST", "Resets", "Endpoints", "Check", "Window"],
        [[
            f"`{row['id']}`",
            f"`{row['requirementId']}`",
            f"`{row['clockId']}`",
            f"{row['lowerBound']}..{row['upperBound']} {row['unit']}",
            f"`{_ast(row['expression'])}`",
            ", ".join(row["resets"]) or "—",
            f"{row['lowerBoundary']}/{row['upperBoundary']}",
            f"`{row['staticCheck']}`",
            row["observationWindow"],
        ] for row in data["timingCatalog"]],
    )
    lines += ["", "## Requirement dispositions", ""]
    lines += _table(
        ["CRS", "Kind", "Targets"],
        [[
            f"`{row['requirementId']}`",
            row["kind"],
            ", ".join(f"`{item}`" for item in row["modelTargetIds"]),
        ] for row in data["requirementDispositions"]],
    )
    lines += ["", "## Trace relations", ""]
    lines += _table(
        ["ID", "CRS", "Kind", "Target", "Rationale"],
        [[
            f"`{row['id']}`",
            f"`{row['requirementId']}`",
            row["targetKind"],
            f"`{row['targetId']}`",
            row["rationaleEn"],
        ] for row in data["traceRelations"]],
    )
    lines += ["", "## Infrastructure premises", ""]
    for row in data["infrastructurePremises"]:
        lines.append(f"- `{row['id']}` `{row['status']}` — {row['behaviorEn']}")
    lines += ["", "## Actions", ""]
    lines += _table(
        ["ID", "Status", "Owner", "Gate", "Note"],
        [[f"`{row['id']}`", f"`{row['status']}`", row["ownerRole"], row["deadlineGate"], row["noteEn"]] for row in data["actions"]],
    )
    lines += ["", "## Source refinements", ""]
    for row in data["sourceRefinements"]:
        locator = row.get("toLocator") or {}
        lines.append(
            f"- `{row['id']}` — `{row['disposition']}` — {row['rationaleEn']} "
            f"(to `{row.get('toRequirementId') or row.get('toSourceId')}` {locator.get('clause') or ''})"
        )
    lines += ["", "## Network relation dispositions", ""]
    for row in data["networkRelationDispositions"]:
        lines.append(f"- `{row['relationId']}` → `{row['m2Disposition']}` (M1 `{row['m1Disposition']}`)")
    lines += [
        "",
        "## Analysis boundary",
        "",
        f"- Untimed: `{data['analysisScope']['untimedReachability']}`",
        f"- Timed: `{data['analysisScope']['timedReachability']}`",
        f"- Unproven: {', '.join(data['analysisScope']['unproven'])}",
        "",
        "## Review control",
        "",
        f"- rg0 `{data['reviewControl']['rg0']}`; rg1 `{data['reviewControl']['rg1']}`; rg2 `{data['reviewControl']['rg2']}`",
        f"- reviewHead `{data['reviewControl']['reviewHead']}`; formalApproval `{data['reviewControl']['formalApproval']}`",
        "",
        "# 中文版",
        "",
        "# ARINC 615A-3 M2 可观测时序模型——评审视图",
        "",
        "> 由 `configs/models/arinc_615a3_m2_model.json` 经 `python scripts/sync_m2_model.py --write` 生成，禁止手改。",
        "",
        "## 输入接受",
        "",
        f"- 批准 Head：`{acc['approvedHead']}`",
        f"- 合并：`{acc['mergeCommit']}` 父提交 `{acc['mergeParents'][0]}` + `{acc['mergeParents'][1]}`",
        f"- 树：`{acc['mergeTree']}`／批准 Head 树 `{acc['approvedHeadTree']}`",
        f"- CI：{acc['mainCiUrl']} @ `{acc['mainCiHead']}`",
        f"- 签署：{acc['signOffUrl']}（`{acc['githubReviewState']}`，`{acc['recordedConclusion']}`）",
        f"- 独立性：`{acc['independenceClaim']}`",
        f"- M1 NET-ISSUE-EDITION 快照 blocksM1Approval=`{acc['m1NetIssueEditionSnapshot']['blocksM1Approval']}` — {acc['m1NetIssueEditionSnapshot']['interpretationZh']}",
        "",
        "## 范围",
        "",
        f"- 服务：{', '.join(data['scope']['services'])}；延期 {', '.join(data['scope']['deferredServices'])}",
        f"- 网络：`{data['scope']['networkMode']}`；AFDX `{data['scope']['afdxSelected']}`；P3 裁剪 `{data['scope']['p3ProfiledDeviations']}`",
        f"- 形式：`{model['form']}`；初态 `{model['initialState']}`",
        f"- {model['stepSemanticsZh']}",
        f"- {data['scope']['observationBoundary']['eventMappingZh']}",
        "",
        "## 事件",
        "",
    ]
    lines += _table(
        ["ID", "可见性", "摘要"],
        [[f"`{row['id']}`", row["visibility"], row["summaryZh"]] for row in model["events"]],
    )
    lines += ["", "## 状态", ""]
    lines += _table(
        ["ID", "终止", "摘要"],
        [[f"`{row['id']}`", str(row["terminal"]), row["summaryZh"]] for row in model["states"]],
    )
    lines += ["", "## 变量", ""]
    lines += _table(
        ["ID", "类型", "初值", "域"],
        [[
            f"`{row['id']}`",
            row["type"],
            str(row["initial"]),
            ", ".join(row.get("domain") or []) or "—",
        ] for row in model["variables"]],
    )
    lines += ["", "## 参数", ""]
    lines += _table(
        ["ID", "单位", "种类", "值", "含义"],
        [[
            f"`{row['id']}`",
            row["unit"],
            row["kind"],
            str(row.get("value")),
            row["meaningZh"],
        ] for row in model["parameters"]],
    )
    lines += ["", "## 时钟", ""]
    lines += _table(
        ["ID", "范围", "关联", "复位", "含义"],
        [[
            f"`{row['id']}`",
            row["scope"],
            row["correlationKey"],
            ", ".join(f"`{item}`" for item in row["resetOn"]),
            row["meaningZh"],
        ] for row in model["clocks"]],
    )
    lines += ["", "## 不变量", ""]
    lines += _table(
        ["ID", "状态", "AST", "说明"],
        [[
            f"`{row['id']}`",
            ", ".join(f"`{item}`" for item in row["states"]),
            f"`{_ast(row['expression'])}`",
            row["noteZh"],
        ] for row in model["invariants"]],
    )
    lines += ["", "## 迁移", ""]
    lines += _table(
        ["ID", "源", "事件", "目标", "守卫", "更新", "输出", "复位", "需求"],
        [[
            f"`{row['id']}`",
            f"`{row['source']}`",
            f"`{row['event']}`",
            f"`{row['target']}`",
            f"`{_ast(row['guard'])}`",
            f"`{_ast(row['updates'])}`" if row["updates"] else "—",
            ", ".join(f"`{item}`" for item in row["outputs"]) or "—",
            ", ".join(row["resets"]) or "—",
            ", ".join(f"`{item}`" for item in row["requirementIds"]),
        ] for row in model["transitions"]],
    )
    lines += ["", "## 顺序约束", ""]
    for row in model["sequenceConstraints"]:
        lines.append(
            f"- `{row['id']}` 顺序 {' → '.join(f'`{item}`' for item in row['requiredStateOrder'])}；"
            f"禁止 {row['forbiddenEdges']}；{row['noteZh']}"
        )
    lines += ["", "## 字段约束", ""]
    lines += _table(
        ["ID", "文件", "字段", "CRS", "检查点"],
        [[
            f"`{row['id']}`",
            row["protocolFile"],
            row["fieldId"],
            f"`{row['m1RequirementId']}`",
            row["checkLocation"],
        ] for row in model["fieldConstraints"]],
    )
    lines += ["", "## 状态约束", ""]
    lines += _table(
        ["ID", "CRS", "代码", "检查点"],
        [[
            f"`{row['id']}`",
            f"`{row['m1RequirementId']}`",
            str(row.get("code") or row.get("kind")),
            row["checkLocation"],
        ] for row in model["statusConstraints"]],
    )
    lines += ["", "## 对象约束", ""]
    lines += _table(
        ["ID", "CRS", "动作", "检查点"],
        [[
            f"`{row['id']}`",
            f"`{row['m1RequirementId']}`",
            row["action"],
            row["checkLocation"],
        ] for row in model["objectConstraints"]],
    )
    lines += ["", "## 接口", ""]
    for name, row in model["interfaces"].items():
        lines.append(f"- `{name}` `{row['kind']}` — {row['noteZh']}")
    lines += ["", "## 时序目录", ""]
    lines += _table(
        ["ID", "CRS", "时钟", "边界", "AST", "复位", "端点", "检查", "窗口"],
        [[
            f"`{row['id']}`",
            f"`{row['requirementId']}`",
            f"`{row['clockId']}`",
            f"{row['lowerBound']}..{row['upperBound']} {row['unit']}",
            f"`{_ast(row['expression'])}`",
            ", ".join(row["resets"]) or "—",
            f"{row['lowerBoundary']}/{row['upperBoundary']}",
            f"`{row['staticCheck']}`",
            row["observationWindow"],
        ] for row in data["timingCatalog"]],
    )
    lines += ["", "## 需求处置", ""]
    lines += _table(
        ["CRS", "种类", "目标"],
        [[
            f"`{row['requirementId']}`",
            row["kind"],
            ", ".join(f"`{item}`" for item in row["modelTargetIds"]),
        ] for row in data["requirementDispositions"]],
    )
    lines += ["", "## 追踪关系", ""]
    lines += _table(
        ["ID", "CRS", "种类", "目标", "理由"],
        [[
            f"`{row['id']}`",
            f"`{row['requirementId']}`",
            row["targetKind"],
            f"`{row['targetId']}`",
            row["rationaleZh"],
        ] for row in data["traceRelations"]],
    )
    lines += ["", "## 基础设施前提", ""]
    for row in data["infrastructurePremises"]:
        lines.append(f"- `{row['id']}` `{row['status']}` — {row['behaviorZh']}")
    lines += ["", "## 行动", ""]
    lines += _table(
        ["ID", "状态", "责任", "门禁", "说明"],
        [[f"`{row['id']}`", f"`{row['status']}`", row["ownerRole"], row["deadlineGate"], row["noteZh"]] for row in data["actions"]],
    )
    lines += ["", "## 来源精化", ""]
    for row in data["sourceRefinements"]:
        locator = row.get("toLocator") or {}
        lines.append(
            f"- `{row['id']}` — `{row['disposition']}` — {row['rationaleZh']} "
            f"（至 `{row.get('toRequirementId') or row.get('toSourceId')}` {locator.get('clause') or ''}）"
        )
    lines += ["", "## 网络关系处置", ""]
    for row in data["networkRelationDispositions"]:
        lines.append(f"- `{row['relationId']}` → `{row['m2Disposition']}`（M1 `{row['m1Disposition']}`）")
    lines += [
        "",
        "## 分析边界",
        "",
        f"- 无时：`{data['analysisScope']['untimedReachability']}`",
        f"- 定时：`{data['analysisScope']['timedReachability']}`",
        f"- 未证明：{', '.join(data['analysisScope']['unproven'])}",
        "",
        "## 评审控制",
        "",
        f"- rg0 `{data['reviewControl']['rg0']}`；rg1 `{data['reviewControl']['rg1']}`；rg2 `{data['reviewControl']['rg2']}`",
        f"- reviewHead `{data['reviewControl']['reviewHead']}`；formalApproval `{data['reviewControl']['formalApproval']}`",
        "",
    ]
    return "\n".join(lines)


def load_package(git_root: Path | None = None) -> dict[str, Any]:
    data = json.loads(PACKAGE_PATH.read_text(encoding="utf-8"))
    errors = package_errors(data, git_root=git_root)
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
