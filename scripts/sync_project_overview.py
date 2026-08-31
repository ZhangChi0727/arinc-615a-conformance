#!/usr/bin/env python3
"""Synchronize the governed README status block from project-status.json."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "project-status.json"
README_PATH = ROOT / "README.md"
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")

# STABLE_INVARIANT: schema vocabulary, not mutable lifecycle state.
ALLOWED_REPOSITORY_ROLES = {"method", "instance"}
ALLOWED_COMPATIBILITY = {
    "NOT-DETERMINED",
    "REVIEWED-COMPATIBLE-WITH-QUALIFICATION",
    "REVIEWED-INCOMPATIBLE",
}
ALLOWED_CONFIGURATION = {"NOT YET ESTABLISHED", "ESTABLISHED"}
ALLOWED_EVALUATION = {"NOT-EXERCISED", "INSTANCE-EXERCISED"}
ALLOWED_RQ8 = {"OPEN", "CLOSED"}
ALLOWED_HANDSHAKE = {"INCOMPLETE", "COMPLETE"}
EXPECTED_QUALIFICATIONS = {f"Q-{number:02d}" for number in range(1, 10)}


class StatusError(ValueError):
    """Raised when the governed status document is invalid."""


def _get(data: dict[str, Any], dotted: str) -> Any:
    value: Any = data
    for key in dotted.split("."):
        if not isinstance(value, dict) or key not in value:
            raise KeyError(dotted)
        value = value[key]
    return value


def load_status(path: Path = STATUS_PATH) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StatusError(f"cannot load {path}: {exc}") from exc
    errors = status_errors(data, path.parent)
    if errors:
        raise StatusError("; ".join(errors))
    return data


def status_errors(data: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    required = (
        "schemaVersion", "updatedAt", "repository.role", "repository.displayRole",
        "repository.url", "currentIncrement.title", "currentIncrement.titleZh",
        "currentIncrement.summary", "currentIncrement.summaryZh",
        "currentIncrement.stateChanges", "currentIncrement.stateChangesZh",
        "currentIncrement.unchangedBoundaries",
        "currentIncrement.unchangedBoundariesZh", "development.phase",
        "development.currentStop.id", "development.currentStop.statusPath",
        "development.currentStop.objective", "development.currentStop.objectiveZh",
        "development.nextSteps", "development.nextStepsZh",
        "release.currentBaselineId", "release.tag", "release.commit",
        "release.tagObject", "release.peeledTarget", "release.thirdHandshake",
        "release.assessedSource.baselineId", "release.assessedSource.tag",
        "release.assessedSource.commit", "release.assessedSource.tagObject",
        "methodInputs.repository", "methodInputs.methodDefinition.version",
        "methodInputs.methodDefinition.commit",
        "methodInputs.compatibilityDisposition.commit",
        "methodInputs.compatibilityDisposition.status",
        "methodInputs.compatibilityDisposition.qualificationIds",
        "crossRepository.methodology.repository",
        "crossRepository.methodology.projectManagementMerge",
        "crossRepository.methodology.schemaVersion",
        "crossRepository.methodology.thirdHandshakeStatusPath",
        "claimsBoundary.projectConfigurationStatus",
        "claimsBoundary.instanceEvaluation", "claimsBoundary.rq8",
        "claimsBoundary.protocolConformanceEstablished",
        "claimsBoundary.certificationReady", "claimsBoundary.authorityAccepted",
        "claimsBoundary.activationRecords",
        "temporaryControls", "governance.requiredPullRequestFiles",
        "governance.readmeMarkers.start", "governance.readmeMarkers.end",
    )
    for dotted in required:
        try:
            value = _get(data, dotted)
        except KeyError:
            errors.append(f"missing required field: {dotted}")
            continue
        if value in (None, ""):
            errors.append(f"empty required field: {dotted}")

    commit_fields = (
        "release.commit", "release.tagObject", "release.peeledTarget",
        "release.assessedSource.commit", "release.assessedSource.tagObject",
        "methodInputs.methodDefinition.commit",
        "methodInputs.compatibilityDisposition.commit",
        "crossRepository.methodology.projectManagementMerge",
        "release.historicalProvenance.methodApprovedHead",
        "release.historicalProvenance.legacyReleaseCommit",
        "release.historicalProvenance.controlStateCommit",
        "release.historicalProvenance.migrationStartingHead",
    )
    for dotted in commit_fields:
        try:
            value = _get(data, dotted)
        except KeyError:
            errors.append(f"missing immutable identity: {dotted}")
        else:
            if not isinstance(value, str) or not COMMIT_RE.fullmatch(value):
                errors.append(f"invalid immutable identity: {dotted}")

    try:
        if _get(data, "repository.role") not in ALLOWED_REPOSITORY_ROLES:
            errors.append("invalid repository role")
        if _get(data, "methodInputs.compatibilityDisposition.status") not in ALLOWED_COMPATIBILITY:
            errors.append("invalid compatibility status")
        if _get(data, "claimsBoundary.projectConfigurationStatus") not in ALLOWED_CONFIGURATION:
            errors.append("invalid Project Configuration status")
        if _get(data, "claimsBoundary.instanceEvaluation") not in ALLOWED_EVALUATION:
            errors.append("invalid instance-evaluation status")
        if _get(data, "claimsBoundary.rq8") not in ALLOWED_RQ8:
            errors.append("invalid RQ8 status")
        if _get(data, "release.thirdHandshake") not in ALLOWED_HANDSHAKE:
            errors.append("invalid third-handshake status")
        stop = _get(data, "development.currentStop")
        if "status" in stop:
            errors.append("development.currentStop.status duplicates its authoritative statusPath")
        if stop.get("statusPath") != "claimsBoundary.projectConfigurationStatus":
            errors.append("current stop must derive from claimsBoundary.projectConfigurationStatus")
        peer = _get(data, "crossRepository.methodology")
        if "thirdHandshake" in peer:
            errors.append("crossRepository.methodology.thirdHandshake duplicates release.thirdHandshake")
        if peer.get("thirdHandshakeStatusPath") != "release.thirdHandshake":
            errors.append("cross-repository handshake must derive from release.thirdHandshake")
        qualifications = set(_get(data, "methodInputs.compatibilityDisposition.qualificationIds"))
        if qualifications != EXPECTED_QUALIFICATIONS:
            errors.append("qualification population differs from controlled Q-01 through Q-09")
        if _get(data, "release.commit") != _get(data, "release.peeledTarget"):
            errors.append("annotated release tag does not peel to the release commit")
        if _get(data, "methodInputs.methodDefinition.commit") == _get(
            data, "methodInputs.compatibilityDisposition.commit"
        ):
            errors.append("method definition and compatibility disposition are conflated")
        if _get(data, "schemaVersion") != _get(data, "crossRepository.methodology.schemaVersion"):
            errors.append("cross-repository schemaVersion differs")
    except KeyError:
        pass

    claim_keys = (
        "protocolConformanceEstablished", "certificationReady", "authorityAccepted",
    )
    boundary = data.get("claimsBoundary", {})
    activations = boundary.get("activationRecords", {})
    if not isinstance(activations, dict):
        errors.append("claimsBoundary.activationRecords must be an object")
        activations = {}
    for claim in claim_keys:
        value = boundary.get(claim)
        if not isinstance(value, bool):
            errors.append(f"claimsBoundary.{claim} must be boolean")
            continue
        if not value:
            continue
        activation = activations.get(claim)
        if not isinstance(activation, dict):
            errors.append(f"true claim {claim} requires an activation record")
            continue
        decision_path = activation.get("decisionPath")
        evidence_refs = activation.get("evidenceRefs")
        if not isinstance(decision_path, str) or not (root / decision_path).is_file():
            errors.append(f"true claim {claim} requires an existing controlled decisionPath")
        if not isinstance(evidence_refs, list) or not evidence_refs:
            errors.append(f"true claim {claim} requires non-empty evidenceRefs")
        elif any(not isinstance(item, str) or not (root / item).exists() for item in evidence_refs):
            errors.append(f"true claim {claim} has unresolved evidenceRefs")

    for dotted in (
        "release.records.baselinePath", "release.records.changePath",
        "release.records.historicalReaderReportPath",
        "release.records.migrationReviewPath",
        "release.records.acknowledgementReviewPath",
    ):
        try:
            target = root / _get(data, dotted)
        except KeyError:
            errors.append(f"missing controlled record path: {dotted}")
        else:
            if not target.is_file():
                errors.append(f"controlled record path does not exist: {dotted}")

    errors.extend(temporary_control_errors(data))
    return errors


def temporary_control_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    controls = data.get("temporaryControls", [])
    if not isinstance(controls, list):
        return ["temporaryControls must be a list"]
    for index, control in enumerate(controls):
        label = f"temporaryControls[{index}]"
        if not isinstance(control, dict):
            errors.append(f"{label} must be an object")
            continue
        required = {"id", "temporary", "status", "owner", "introducedBy", "retireWhen"}
        missing = sorted(required - set(control))
        if missing:
            errors.append(f"{label} missing {', '.join(missing)}")
            continue
        if control["temporary"] is not True:
            errors.append(f"{label}.temporary must be true")
        retire = control["retireWhen"]
        if not isinstance(retire, dict) or not {"path", "equals"} <= set(retire):
            errors.append(f"{label}.retireWhen needs path and equals")
            continue
        try:
            actual = _get(data, str(retire["path"]))
        except KeyError:
            errors.append(f"{label} has unknown retirement path")
            continue
        if actual == retire["equals"]:
            errors.append(f"{label} retirement condition is fulfilled; remove the control")
    return errors


def _short(value: str) -> str:
    return value[:12]


def _commit_link(repository: str, commit: str) -> str:
    return f"[`{_short(commit)}`]({repository}/commit/{commit})"


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def render_status_block(data: dict[str, Any]) -> str:
    release = data["release"]
    method = data["methodInputs"]
    compatibility = method["compatibilityDisposition"]
    boundary = data["claimsBoundary"]
    stop = data["development"]["currentStop"]
    stop_status = _get(data, stop["statusPath"])
    increment = data["currentIncrement"]
    repository = data["repository"]["url"]
    qualifications_en = "–".join((compatibility["qualificationIds"][0], compatibility["qualificationIds"][-1]))
    qualifications_zh = "～".join((compatibility["qualificationIds"][0], compatibility["qualificationIds"][-1]))
    baseline_path = release["records"]["baselinePath"]
    release_link = f"{repository}/tree/{release['tag']}"
    definition = method["methodDefinition"]
    return f"""## Current development picture

| Dimension | Controlled state |
|---|---|
| Repository role | {data['repository']['displayRole']} |
| Current release | [`{release['currentBaselineId']}`]({baseline_path}) / annotated [`{release['tag']}`]({release_link}) |
| Method input | {definition['version']} at {_commit_link(method['repository'], definition['commit'])} |
| Third handshake | `{release['thirdHandshake']}` |
| Compatibility | `{compatibility['status']}` under {qualifications_en} |
| Project Configuration | `{boundary['projectConfigurationStatus']}` |
| Instance evaluation | `{boundary['instanceEvaluation']}` |
| RQ8 | `{boundary['rq8']}` |

## Current increment

**{increment['title']}**

{_bullets(increment['summary'])}

State changes:

{_bullets(increment['stateChanges'])}

Unchanged boundaries:

{_bullets(increment['unchangedBoundaries'])}

## Current stop

`{stop['id']}` — **{stop_status}**: {stop['objective']}

## Next development steps

{_bullets(data['development']['nextSteps'])}

## 当前开发图景

| 维度 | 受控状态 |
|---|---|
| 仓库角色 | ARINC 615A Profile、Binding、Configuration、实例工程与证据的权威仓库 |
| 当前发布 | [`{release['currentBaselineId']}`]({baseline_path}) / annotated [`{release['tag']}`]({release_link}) |
| 方法输入 | {definition['version']} @ {_commit_link(method['repository'], definition['commit'])} |
| 第三次握手 | `{release['thirdHandshake']}` |
| 兼容性 | 受 {qualifications_zh} 限定的 `{compatibility['status']}` |
| Project Configuration | `{boundary['projectConfigurationStatus']}` |
| 实例评价 | `{boundary['instanceEvaluation']}` |
| RQ8 | `{boundary['rq8']}` |

## 本次集成增量

**{increment['titleZh']}**

{_bullets(increment['summaryZh'])}

状态变化：

{_bullets(increment['stateChangesZh'])}

保持不变的边界：

{_bullets(increment['unchangedBoundariesZh'])}

## 当前停点

`{stop['id']}` — **{stop_status}**：{stop['objectiveZh']}

## 下一步开发计划

{_bullets(data['development']['nextStepsZh'])}
"""


def replace_status_block(readme: str, data: dict[str, Any]) -> str:
    markers = data["governance"]["readmeMarkers"]
    start, end = markers["start"], markers["end"]
    if readme.count(start) != 1 or readme.count(end) != 1:
        raise StatusError("README must contain exactly one governed marker pair")
    before, remainder = readme.split(start, 1)
    _, after = remainder.split(end, 1)
    return f"{before}{start}\n{render_status_block(data).rstrip()}\n{end}{after}"


def synchronized_readme(
    data: dict[str, Any], readme_path: Path = README_PATH
) -> tuple[str, str]:
    current = readme_path.read_text(encoding="utf-8")
    return current, replace_status_block(current, data)


def diff_text(current: str, expected: str) -> str:
    return "".join(difflib.unified_diff(
        current.splitlines(keepends=True), expected.splitlines(keepends=True),
        fromfile="README.md (current)", tofile="README.md (generated)",
    ))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        data = load_status()
        current, expected = synchronized_readme(data)
    except StatusError as exc:
        print(f"project overview error: {exc}", file=sys.stderr)
        return 1
    if current == expected:
        print("project overview is synchronized")
        return 0
    if args.write:
        README_PATH.write_text(expected, encoding="utf-8", newline="\n")
        print("README governed status block updated")
        return 0
    print(diff_text(current, expected), file=sys.stderr)
    print("run scripts/sync_project_overview.py --write", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
