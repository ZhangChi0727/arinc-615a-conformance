"""Render the controlled bilingual 615A UPLOAD LUR-start scenario view.

The JSON package is the only editable scenario authority.  This script refuses
to write a reader view until the package, its controlled Git snapshots, and
its source/M2 relations validate successfully.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any, Iterable

from check_615a_scenarios import PACKAGE_PATH, ROOT, validate_package


VIEW_PATH = Path("docs/engineering/CLTAV_615A_SCENARIO_PROTOTYPE.md")
SOURCE_ORDER = (
    "SRC-LIST-OFFER-PRECONDITION",
    "SRC-LUS-READY",
    "SRC-LUR-WRQ",
    "SRC-LUR-ACK",
    "SRC-LUR-DATA",
)
ACTION_ORDER = (
    "ACT-INSPECT-NO-WRQ-BEFORE-READY",
    "ACT-PREP-ENTER-READY-WINDOW",
    "ACT-TEST-ACK-BEFORE-DATA",
    "ACT-RECOVER-RECONFIRM-READY",
)
CASE_ORDER = (
    "CASE-NORMAL-CONTROL-TIMELINE",
    "CASE-EARLY-WRQ-TIMELINE",
    "CASE-EARLY-DATA-TIMELINE",
    "CASE-UNKNOWN-RECOVER-CONTINUATION",
    "CASE-RESOURCE-ADMISSION-BLOCK",
)
WITNESS_ORDER = (
    "WIT-FINITE-NO-WRQ-TEST",
    "WIT-PUBLIC-SUMMARY",
    "WIT-P3-UNAVAILABLE",
    "WIT-SUCCESSOR-AND-RECOVER",
)
EXPERIMENT_INTERFACE_ORDER = (
    "IF-EXP-SCENE",
    "IF-EXP-INJECT",
    "IF-EXP-TRUTH",
    "IF-EXP-COLLECT",
    "IF-EXP-RUN",
    "IF-EXP-FILTER",
    "IF-EXP-EVAL",
)
TRACEABILITY_ORDER = (
    "MAP-LIST-OFFER-PRECONDITION",
    "MAP-NO-WRQ-FINITE-TEST",
    "MAP-PREP-READY",
    "MAP-LUR-ORDER-TEST",
    "MAP-RECOVER-READY",
)


def plain_text(value: object) -> str:
    """Render controlled free text without allowing Markdown-table injection."""

    text = str(value).replace("\r\n", "\n").replace("\r", "\n")
    return (
        html.escape(text, quote=False)
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("|", "\\|")
        .replace("\n", "<br>")
    )


def _bool(value: bool, *, chinese: bool) -> str:
    if chinese:
        return "是" if value else "否"
    return "yes" if value else "no"


def _cell(value: Any, *, chinese: bool = False) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return _bool(value, chinese=chinese)
    if isinstance(value, list):
        return "<br>".join(_cell(item, chinese=chinese) for item in value) if value else "—"
    if isinstance(value, dict):
        return "; ".join(f"{plain_text(key)}={_cell(item, chinese=chinese)}" for key, item in sorted(value.items()))
    return plain_text(value)


def _table(headers: list[str], rows: Iterable[Iterable[Any]], *, chinese: bool = False) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    lines.extend("| " + " | ".join(_cell(value, chinese=chinese) for value in row) + " |" for row in rows)
    return lines


def _rows(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = data.get(key)
    if not isinstance(value, list):
        return []
    return sorted((row for row in value if isinstance(row, dict)), key=lambda row: str(row.get("id", row.get("interfaceId", ""))))


def _ordered(rows: Iterable[dict[str, Any]], order: Iterable[str], key: str = "id") -> list[dict[str, Any]]:
    by_id = {str(row.get(key, "")): row for row in rows}
    return [by_id[row_id] for row_id in order if row_id in by_id]


def _zh(data: dict[str, Any], key: str) -> str:
    translations = data["translationsZh"]
    return str(translations[key])


def _render_actions(data: dict[str, Any], *, chinese: bool) -> list[str]:
    lines: list[str] = []
    heading = "## Controlled actions / 受控动作" if not chinese else "## 受控动作"
    lines.extend([heading, ""])
    for action in _ordered(_rows(data, "actionLibrary"), ACTION_ORDER):
        action_id = str(action["id"])
        zh = action["zh"]
        if chinese:
            lines.extend([
                f"### `{action_id}` — {plain_text(_zh(data, f'actions.{action_id}.summary'))}",
                f"- 类别：`{action['kind']}`；资格：{plain_text(zh['eligibility'])}",
                f"- 公开刺激：{plain_text(zh['publicStimulus'])}",
                f"- 观测模式：{plain_text(zh['observationMode'])}；成本：{_cell(action['cost'], chinese=True)}",
                f"- 后继确认：{plain_text(zh['successorConfirmation'])}",
                f"- 未确认效果：{plain_text(zh['unconfirmedEffectDisposition'])}",
                f"- 历史提交：{plain_text(zh['historyDisposition'])}",
                f"- 检查：{_cell(action['inspection'], chinese=True)}",
                f"- 摘要来源（公开）：{_cell(action['summaryDerivation']['publicSources'], chinese=True)}；禁止私有来源：{_cell(action['summaryDerivation']['forbiddenPrivateSources'], chinese=True)}",
                "- 可能结果：",
            ])
            lines.extend(_table(
                ["可见量", "后继摘要", "摘要确认条件", "相容假设"],
                ((
                    row["observable"], row["postSummary"], row["summaryConfirmedWhenZh"], row["compatibleHypotheses"],
                ) for row in action["possibleOutcomes"]),
                chinese=True,
            ))
            lines.extend([
                f"- 未评估义务：{_cell(action['nonEvaluatedObligations'], chinese=True)}",
                "",
            ])
        else:
            lines.extend([
                f"### `{action_id}` — {plain_text(action['kind'])}",
                f"- Eligibility: {plain_text(action['eligibility'])}",
                f"- Public stimulus: {plain_text(action['publicStimulus'])}",
                f"- Observation mode: `{action['observationMode']}`; cost: {_cell(action['cost'])}",
                f"- Successor confirmation: `{action['successorConfirmation']}`",
                f"- Unconfirmed-effect disposition: `{action['unconfirmedEffectDisposition']}`",
                f"- History disposition: `{action['historyDisposition']}`",
                f"- Inspection: {_cell(action['inspection'])}",
                f"- Public summary sources: {_cell(action['summaryDerivation']['publicSources'])}; prohibited private sources: {_cell(action['summaryDerivation']['forbiddenPrivateSources'])}",
                "- Possible outcomes:",
            ])
            lines.extend(_table(
                ["Observable", "Post-summary", "Summary confirmed when", "Compatible hypotheses"],
                ((
                    row["observable"], row["postSummary"], row["summaryConfirmedWhen"], row["compatibleHypotheses"],
                ) for row in action["possibleOutcomes"]),
            ))
            lines.extend([
                f"- Non-evaluated obligations: {_cell(action['nonEvaluatedObligations'])}",
                "",
            ])
    return lines


def _render_cases(data: dict[str, Any], *, chinese: bool) -> list[str]:
    lines = ["## Timelines / 时线" if not chinese else "## 场景时线", ""]
    headers = (
        ["Case / 案例", "Purpose", "Round", "Action", "Visible events", "Public summary", "Candidates", "Continue", "Resource admission", "Resource reason", "Resource mode", "Available rounds", "Required rounds", "Cost charged", "Successor disposition"]
        if not chinese
        else ["案例", "场景说明", "轮次", "动作", "可见事件", "公开摘要", "候选集", "继续", "资源准入", "资源原因", "资源模式", "可用轮次", "所需轮次", "动作收费", "后继处置"]
    )
    rows = []
    for case in _ordered(_rows(data, "cases"), CASE_ORDER):
        case_id = str(case["id"])
        purpose = case["purpose"] if not chinese else _zh(data, f"cases.{case_id}.summary")
        for round_ in case["rounds"]:
            resource = round_.get("resourceExpectation") if isinstance(round_.get("resourceExpectation"), dict) else {}
            rows.append((
                case_id, purpose, round_["round"], round_["actionId"],
                round_["expectedVisibleEvents"], round_["expectedPublicSummary"],
                round_["expectedCandidates"], round_["continues"],
                resource.get("admission"), resource.get("reason"), resource.get("mode"), resource.get("availableRounds"), resource.get("requiredRounds"),
                resource.get("actionCostCharged"), resource.get("successorDisposition"),
            ))
    lines.extend(_table(headers, rows, chinese=chinese))
    lines.append("")
    return lines


def _render_fault_variants(data: dict[str, Any], *, chinese: bool) -> list[str]:
    """Render the installed and observable single-fault variants explicitly."""

    variants = sorted(
        (row for row in data["lifecycle"]["faultInjection"]["variants"] if isinstance(row, dict)),
        key=lambda row: str(row.get("hypothesisId", "")),
    )
    if chinese:
        headers = ["假设", "安装目标", "控制器回读", "激活可见量", "算法可见性"]
    else:
        headers = ["Hypothesis", "Installation target", "Controller readback", "Activation observable", "Algorithm visibility"]
    return _table(
        headers,
        (
            (
                row["hypothesisId"],
                row["installationTarget"],
                row["controllerReadback"],
                row["activationObservable"],
                row["algorithmVisibility"],
            )
            for row in variants
        ),
        chinese=chinese,
    )


def _render_object_contract(data: dict[str, Any], *, chinese: bool) -> list[str]:
    """Render the bounded surrogate/peer contract without inventing an implementation."""

    contract = data["objectContract"]
    states = sorted(contract["stateVariables"], key=lambda row: str(row["id"]))
    guards = sorted(contract["guardTransitions"], key=lambda row: str(row["id"]))
    stimuli = sorted(contract["publicStimuli"], key=lambda row: str(row["id"]))
    outputs = sorted(contract["visibleOutputs"], key=lambda row: str(row["id"]))
    payload = contract["semanticPayloadBoundary"]
    private = contract["privateBoundary"]
    lifecycle = contract["lifecycleBoundary"]
    identity = contract["implementationIdentityPlan"]
    if chinese:
        lines = [
            "## 对象与对端合同", "",
            f"- 阶段：`{contract['stage']}`；对象：`{contract['objectKind']}`；对端：`{contract['peerKind']}`。",
            "", "### 状态与不变量", "",
        ]
        lines.extend(_table(
            ["状态", "M2／来源锚点", "初值", "所有者", "中文不变量"],
            ((row["id"], row["sourceAnchor"], row["initial"], row["owner"], row["meaningZh"]) for row in states),
            chinese=True,
        ))
        lines.extend(["", "### 守卫与故障旁路", ""])
        lines.extend(_table(
            ["守卫", "来源关系", "所需状态", "正常可见输出", "故障旁路", "中文说明"],
            ((
                row["id"], row["sourceRelationId"], row["requiresState"], row["normalVisibleOutputId"],
                row["faultBypassHypothesisId"], row["meaningZh"],
            ) for row in guards),
            chinese=True,
        ))
        lines.extend(["", "### 公开刺激与可见输出", ""])
        lines.extend(_table(
            ["类型", "标识", "来源关系", "事件", "可见性", "中文说明"],
            (("公开刺激", row["id"], row["sourceRelationId"], row["eventId"], row["visibility"], row["meaningZh"]) for row in stimuli),
            chinese=True,
        ))
        lines.extend(_table(
            ["类型", "标识", "来源关系", "事件", "可见性", "中文说明"],
            (("可见输出", row["id"], row["sourceRelationId"], row["eventId"], row["visibility"], row["meaningZh"]) for row in outputs),
            chinese=True,
        ))
        lines.extend([
            "", "### 文件角色、语义 opcode 与私有投影", "",
            f"- {plain_text(payload['meaningZh'])}",
            f"- 文件角色：`{payload['fileRole']}`；语义 opcode：{_cell(payload['semanticOpcodes'], chinese=True)}；载荷表示：`{payload['payloadRepresentation']}`；不是 wire 报文实现：{_bool(payload['notWirePacketImplementation'], chinese=True)}。",
            f"- {plain_text(private['meaningZh'])}",
            f"- 仅评估方：{_cell(private['evaluatorOnly'], chinese=True)}；算法禁止：{_cell(private['algorithmForbidden'], chinese=True)}；允许公开投影：{_cell(private['permittedAlgorithmProjection'], chinese=True)}。",
            "", "### 故障撤销与实现身份计划", "",
            f"- {plain_text(lifecycle['meaningZh'])}",
            f"- 安装生命周期：`{lifecycle['faultInstallationLifetime']}`；撤销动作：`{lifecycle['faultRevocationAction']}`；撤销证据：`{lifecycle['revocationEvidence']}`。",
            f"- {plain_text(identity['meaningZh'])}",
            f"- 身份状态：`{identity['status']}`；后续实现必须绑定：{_cell(identity['requiredAtImplementation'], chinese=True)}。",
            "",
        ])
        return lines

    lines = [
        "## Object and peer contract", "",
        f"- Stage: `{contract['stage']}`; object: `{contract['objectKind']}`; peer: `{contract['peerKind']}`.",
        "", "### State and invariants", "",
    ]
    lines.extend(_table(
        ["State", "M2/source anchor", "Initial", "Owner", "Invariant"],
        ((row["id"], row["sourceAnchor"], row["initial"], row["owner"], row["invariant"]) for row in states),
    ))
    lines.extend(["", "### Guards and fault bypasses", ""])
    lines.extend(_table(
        ["Guard", "Source relation", "Required state", "Normal visible output", "Fault bypass"],
        ((
            row["id"], row["sourceRelationId"], row["requiresState"], row["normalVisibleOutputId"],
            row["faultBypassHypothesisId"],
        ) for row in guards),
    ))
    lines.extend(["", "### Public stimuli and visible outputs", ""])
    lines.extend(_table(
        ["Type", "Identifier", "Source relation", "Event", "Visibility"],
        (("Public stimulus", row["id"], row["sourceRelationId"], row["eventId"], row["visibility"]) for row in stimuli),
    ))
    lines.extend(_table(
        ["Type", "Identifier", "Source relation", "Event", "Visibility"],
        (("Visible output", row["id"], row["sourceRelationId"], row["eventId"], row["visibility"]) for row in outputs),
    ))
    lines.extend([
        "", "### File role, semantic opcode and private projection", "",
        f"- File role: `{payload['fileRole']}`; semantic opcodes: {_cell(payload['semanticOpcodes'])}; payload representation: `{payload['payloadRepresentation']}`; not a wire-packet implementation: {_bool(payload['notWirePacketImplementation'], chinese=False)}.",
        f"- Evaluator-only: {_cell(private['evaluatorOnly'])}; algorithm-forbidden: {_cell(private['algorithmForbidden'])}; permitted public projection: {_cell(private['permittedAlgorithmProjection'])}.",
        "", "### Fault revocation and implementation identity plan", "",
        f"- Installation lifetime: `{lifecycle['faultInstallationLifetime']}`; revocation action: `{lifecycle['faultRevocationAction']}`; revocation evidence: `{lifecycle['revocationEvidence']}`.",
        f"- Identity status: `{identity['status']}`; implementation must bind: {_cell(identity['requiredAtImplementation'])}.",
        f"- Not established: {plain_text(identity['notEstablished'])}",
        "",
    ])
    return lines


def render(data: dict[str, Any]) -> str:
    """Render a deterministic, bilingual reader view from one package."""

    identity = data["identity"]
    control = data["controlBinding"]
    scope = data["scope"]
    domain = data["hypothesisDomain"]
    clock = data["timeAndObservation"]
    lifecycle = data["lifecycle"]
    sources = _ordered(_rows(data, "sourceRelations"), SOURCE_ORDER)
    traceability = _ordered(_rows(data, "traceabilityMatrix"), TRACEABILITY_ORDER)
    witnesses = _ordered(_rows(data, "feasibilityWitnesses"), WITNESS_ORDER)
    relations = _ordered(_rows(data, "experimentRelations"), EXPERIMENT_INTERFACE_ORDER, key="interfaceId")
    inputs = sorted(data["acceptedInputs"], key=lambda row: str(row["path"]))

    lines = [
        "# 615A UPLOAD LUR-Start Engineering Scenario Prototype",
        "",
        "> Generated from `configs/engineering/cltav_615a_scenarios.json`; do not edit this view directly. "
        "It is a bounded engineering specification, not a protocol conformance verdict, experiment result, or capability claim.",
        "",
        f"- Artifact: `{data['artifactId']}`; family: `{identity['scenarioFamilyId']}`; version: `{identity['version']}`",
        f"- Control: `{identity['changeRequest']}` / `{identity['decision']}`; accepted authority commit: `{identity['acceptedAuthorityCommit']}`",
        f"- Immutable G0 control record: `{control['path']}` @ `{control['controlCommit']}`; Git blob `{control['gitBlobOid']}`; SHA-256 `{control['rawSha256']}`",
        f"- Classification: `{identity['runClassification']}`; stage: `{identity['stageStatus']}`",
        "",
        "## Accepted authority snapshot",
        "",
    ]
    lines.extend(_table(
        ["Path", "Role", "Commit", "Git blob", "SHA-256"],
        ((row['path'], row['role'], row['commit'], row['gitBlobOid'], row['rawSha256']) for row in inputs),
    ))
    lines.extend([
        "", "## Scope and boundary", "",
        f"- Operation / roles: `{scope['operation']}` / {_cell(scope['roles'])}",
        f"- Start / end: `{scope['startBoundary']}` / `{scope['endBoundary']}`",
        f"- Prepared but not executed: {_cell(scope['preparedButNotExecuted'])}",
        f"- Not evaluated: {_cell(scope['notEvaluatedObligations'])}",
        f"- Experiment relation: `{scope['relationshipToExperimentScenario']['scenarioId']}` / `{scope['relationshipToExperimentScenario']['relation']}` — {plain_text(scope['relationshipToExperimentScenario']['reason'])}",
    ])
    lines.extend(_render_object_contract(data, chinese=False))
    lines.extend(["## Source-to-model control relations", ""])
    lines.extend(_table(
        ["Relation", "CRS / source unit", "Source locator", "Semantic opcode class", "File role", "M2 transition / event / direction", "CRS actor → receiver", "Use", "State boundary", "Controlled source assertions", "Scenario rationale"],
        ((
            row['id'], [row['requirementId'], row['sourceUnitId'], f"doc/PDF {row['documentPage']}/{row['pdfPage']}"],
            row['sourceLocator'], row['semanticOpcodeClass'], row['fileRole'],
            [row['transitionId'], row['eventId'], row['eventDirection']], [row['actor'], row['receiver']],
            [row['scenarioUse'], f"executed={_bool(row['executedByScenario'], chinese=False)}", f"wire={_bool(not row['notWireOpcode'], chinese=False)}"],
            [f"before: {row['stateFacts']['before']}", f"after: {row['stateFacts']['after']}"],
            row['stateFacts']['assertions'],
            row['scenarioRationale'],
        ) for row in sources),
    ))
    lines.extend(["", "## A-stage source / interface / acceptance matrix", ""])
    lines.extend(_table(
        ["State or action", "Source relations", "Visible evidence", "Existing interface use", "Acceptance witness", "Not covered"],
        ((
            row["stateOrActionId"], row["sourceRelationIds"], row["visibleEvidence"],
            [row["interfaceUse"], *row["existingInterfaceIds"]], row["acceptanceWitnessIds"], row["notCovered"],
        ) for row in traceability),
    ))
    lines.extend(["", "## Finite hypothesis domain", ""])
    lines.extend(_table(
        ["Hypothesis", "Kind", "Definition", "Algorithm boundary"],
        ((row['id'], row['kind'], row['definition'], "fault activation is evaluator-only") for row in _rows(domain, "members")),
    ))
    lines.extend([
        "", f"- Algorithm may know: {_cell(domain['algorithmMayKnow'])}",
        f"- Algorithm must not receive: {_cell(domain['algorithmMustNotReceive'])}",
        f"- Limit: {plain_text(domain['coverageLimit'])}", "",
    ])
    lines.extend(_render_actions(data, chinese=False))
    lines.extend([
        "## Clock, observation, reset and recovery", "",
        f"- Clock: `{clock['virtualClockId']}` / `{clock['tickRepresentation']}` — {plain_text(clock['tickMeaning'])}",
        f"- Uncertainty: `{clock['uncertaintyIdentity']}` / `{clock['uncertaintyModel']}`; same tick: {plain_text(clock['sameTickOrdering'])}",
        f"- Ownership: `{clock['ownershipPolicy']}`; finite boundary: {plain_text(clock['finiteObservationBoundary'])}",
        "", "## Resource admission and accounting boundary", "",
        f"- Admission owner / accounting owner: `{data['resourceContract']['admissionOwner']}` / `{data['resourceContract']['accountingOwner']}`",
        f"- Controlled modes: {_cell(data['resourceContract']['allowedModes'])}; admission boundary: `{data['resourceContract']['admissionBoundary']}`",
        f"- ROUNDS: {plain_text(data['resourceContract']['roundsMeaning'])}",
        f"- BUDGET: {plain_text(data['resourceContract']['budgetMeaning'])}",
        f"- Post-dispatch error: `{data['resourceContract']['postDispatchError']}`; not evaluated: {_cell(data['resourceContract']['notEvaluated'])}",
        "",
        "## Fault-installation and activation variants", "",
        f"- Full reset: {_cell(lifecycle['fullReset']['scope'])}; evidence `{lifecycle['fullReset']['successEvidence']}`; protocol abort={_bool(lifecycle['fullReset']['notProtocolAbort'], chinese=False)}",
        f"- Fault injection: install `{lifecycle['faultInjection']['installationEvidence']}`; activate `{lifecycle['faultInjection']['activationEvidence']}`; unconfirmed `{lifecycle['faultInjection']['unconfirmedDisposition']}`",
        f"- Installation lifetime: `{lifecycle['faultInjection']['installationLifetime']}`; revocation action: `{lifecycle['faultInjection']['revocationAction']}`; revocation evidence: `{lifecycle['faultInjection']['revocationEvidence']}`; revocation failure: `{lifecycle['faultInjection']['revocationFailureDisposition']}`",
    ])
    lines.extend(_render_fault_variants(data, chinese=False))
    lines.extend([
        "",
        f"- Recover: requires `{lifecycle['recover']['requires']}`; distinct target/summary={lifecycle['recover']['targetAndSummaryAreDistinct']}; failure `{lifecycle['recover']['confirmationFailureDisposition']}`",
        "",
    ])
    lines.extend(_render_cases(data, chinese=False))
    lines.extend(["## Experiment-interface handoffs", ""])
    lines.extend(_table(
        ["Interface", "Engineering handoff", "Public projection", "Evaluator projection", "Shared-component risk", "Not admitted"],
        ((
            row['interfaceId'], row['engineeringHandoff'], row['publicProjection'], row['evaluatorProjection'],
            row['sharedComponentRisk'], row['notAdmitted'],
        ) for row in relations),
    ))
    lines.extend(["", "## Feasibility witnesses", ""])
    lines.extend(_table(
        ["Witness", "Entry point", "Bounded claim"],
        ((row['id'], row['entryPoint'], row['claim']) for row in witnesses),
    ))
    lines.extend(["", "## Explicit limitations", ""])
    lines.extend(f"- {plain_text(item)}" for item in data["limitations"])

    lines.extend([
        "", "# 中文版", "",
        "# 615A UPLOAD LUR 起始工程场景原型", "",
        "> 本视图由 `configs/engineering/cltav_615a_scenarios.json` 生成，禁止直接修改。它是有限工程规格，不是协议符合性判定、实验结果或能力主张。",
        "",
        f"- {plain_text(_zh(data, 'identity.title'))}",
        f"- 控制：`{identity['changeRequest']}` / `{identity['decision']}`；已接受权威提交：`{identity['acceptedAuthorityCommit']}`",
        f"- 不可变 G0 控制记录：`{control['path']}` @ `{control['controlCommit']}`；Git blob `{control['gitBlobOid']}`；SHA-256 `{control['rawSha256']}`",
        f"- 分类：`{identity['runClassification']}`；阶段：`{identity['stageStatus']}`",
        "", "## 已接受权威快照", "",
    ])
    lines.extend(_table(
        ["路径", "角色", "提交", "Git blob", "SHA-256"],
        ((row['path'], row['role'], row['commit'], row['gitBlobOid'], row['rawSha256']) for row in inputs),
    ))
    lines.extend([
        "", "## 范围与边界", "",
        f"- {plain_text(_zh(data, 'scope.summary'))}",
        f"- 操作／角色：`{scope['operation']}` / {_cell(scope['roles'])}",
        f"- 起点／终点：`{scope['startBoundary']}` / `{scope['endBoundary']}`",
        f"- 已准备但未执行：{_cell(scope['preparedButNotExecuted'])}",
        f"- 未评估：{_cell(scope['notEvaluatedObligations'])}",
        f"- 实验关系：`{scope['relationshipToExperimentScenario']['scenarioId']}` / `{scope['relationshipToExperimentScenario']['relation']}` — {plain_text(_zh(data, 'scope.relationship.reason'))}",
    ])
    lines.extend(_render_object_contract(data, chinese=True))
    lines.extend(["## 来源到模型的控制关系", ""])
    lines.extend(_table(
        ["关系", "CRS／来源单元", "来源定位", "语义 opcode 类", "文件角色", "M2 迁移／事件／方向", "CRS 参与方", "场景用途", "状态边界", "场景理由", "中文控制说明"],
        ((
            row['id'], [row['requirementId'], row['sourceUnitId'], f"文档/PDF {row['documentPage']}/{row['pdfPage']}"],
            row['sourceLocator'], row['semanticOpcodeClass'], row['fileRole'],
            [row['transitionId'], row['eventId'], row['eventDirection']], [row['actor'], row['receiver']],
            [row['scenarioUse'], f"执行={_bool(row['executedByScenario'], chinese=True)}", f"报文={_bool(not row['notWireOpcode'], chinese=True)}"],
            [f"前：{row['stateFacts']['before']}", f"后：{row['stateFacts']['after']}"],
            row['scenarioRationaleZh'],
            _zh(data, f"sourceRelations.{row['id']}.summary"),
        ) for row in sources),
        chinese=True,
    ))
    lines.extend(["", "## A 阶段来源／接口／验收矩阵", ""])
    lines.extend(_table(
        ["状态或动作", "来源关系", "可见证据", "既有接口用途", "验收见证", "未覆盖边界", "中文说明"],
        ((
            row["stateOrActionId"], row["sourceRelationIds"], row["visibleEvidence"],
            [row["interfaceUse"], *row["existingInterfaceIds"]], row["acceptanceWitnessIds"], row["notCovered"],
            _zh(data, f"traceability.{row['id']}.summary"),
        ) for row in traceability),
    ))
    lines.extend(["", "## 有限假设域", ""])
    lines.extend(_table(
        ["假设", "类别", "中文说明", "算法边界"],
        ((row['id'], row['kind'], _zh(data, f"hypotheses.{row['id']}.summary"), "故障激活仅评估方可见") for row in _rows(domain, "members")),
        chinese=True,
    ))
    lines.extend([
        "", f"- 算法可知：{_cell(domain['algorithmMayKnow'])}",
        f"- 算法不得接收：{_cell(domain['algorithmMustNotReceive'])}",
        f"- 覆盖边界：{plain_text(domain['coverageLimitZh'])}", "",
    ])
    lines.extend(_render_actions(data, chinese=True))
    lines.extend([
        "## 时钟、观测、复位和恢复", "",
        f"- {plain_text(_zh(data, 'timeAndObservation.summary'))}",
        f"- 时钟：`{clock['virtualClockId']}` / `{clock['tickRepresentation']}`；不确定性：`{clock['uncertaintyIdentity']}` / `{clock['uncertaintyModel']}`",
        "", "## 资源准入与记账边界", "",
        f"- {plain_text(_zh(data, 'resourceContract.summary'))}",
        f"- 准入所有者／记账所有者：`{data['resourceContract']['admissionOwner']}` / `{data['resourceContract']['accountingOwner']}`",
        f"- 受控模式：{_cell(data['resourceContract']['allowedModes'], chinese=True)}；准入边界：`{data['resourceContract']['admissionBoundary']}` — {plain_text(data['resourceContract']['zh']['admissionBoundary'])}",
        f"- ROUNDS：{plain_text(data['resourceContract']['zh']['roundsMeaning'])}",
        f"- BUDGET：{plain_text(data['resourceContract']['zh']['budgetMeaning'])}",
        f"- 调度后错误：`{data['resourceContract']['postDispatchError']}` — {plain_text(data['resourceContract']['zh']['postDispatchError'])}；未评估：{plain_text(data['resourceContract']['zh']['notEvaluated'])}",
        "", "## 故障安装与激活变体", "",
        f"- {plain_text(_zh(data, 'lifecycle.fullReset.summary'))}",
        f"- {plain_text(_zh(data, 'lifecycle.faultInjection.summary'))}",
        f"- 故障安装生命周期：`{lifecycle['faultInjection']['installationLifetime']}`；撤销动作：`{lifecycle['faultInjection']['revocationAction']}`；撤销证据：`{lifecycle['faultInjection']['revocationEvidence']}`；撤销失败：`{lifecycle['faultInjection']['revocationFailureDisposition']}`。",
    ])
    lines.extend(_render_fault_variants(data, chinese=True))
    lines.extend([
        "",
        f"- {plain_text(_zh(data, 'lifecycle.recover.summary'))}",
        "",
    ])
    lines.extend(_render_cases(data, chinese=True))
    lines.extend(["## 实验接口交接", ""])
    lines.extend(_table(
        ["接口", "工程交接", "公开投影", "评估方投影", "共享组件风险", "不准入内容"],
        ((
            row['interfaceId'], row['zh']['engineeringHandoff'], row['zh']['publicProjection'],
            row['zh']['evaluatorProjection'], row['zh']['sharedComponentRisk'], row['zh']['notAdmitted'],
        ) for row in relations),
        chinese=True,
    ))
    lines.extend(["", "## 可行性见证", ""])
    lines.extend(_table(
        ["见证", "入口", "中文受限主张"],
        ((row['id'], row['entryPoint'], _zh(data, f"feasibilityWitnesses.{row['id']}.summary")) for row in witnesses),
    ))
    lines.extend(["", "## 明确限制", ""])
    lines.extend(f"- {plain_text(_zh(data, f'limitations.{index}'))}" for index, _item in enumerate(data["limitations"]))
    return "\n".join(lines) + "\n"


def _normalized(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def sync(root: Path = ROOT, *, write: bool = False) -> tuple[bool, str]:
    """Validate first, then write or compare the derived reader view."""

    root = root.resolve()
    try:
        data = json.loads((root / PACKAGE_PATH).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, f"cannot load scenario package: {type(exc).__name__}: {exc}"
    errors = validate_package(root, data)
    if errors:
        return False, "scenario package validation failed; view was not changed:\n" + "\n".join(f"- {item}" for item in errors)
    expected = render(data)
    path = root / VIEW_PATH
    try:
        actual = path.read_text(encoding="utf-8") if path.exists() else ""
    except OSError as exc:
        return False, f"cannot read scenario view: {type(exc).__name__}: {exc}"
    if _normalized(actual) == expected:
        return True, "615A scenario reader view is synchronized"
    if not write:
        return False, "615A scenario reader view is stale; run python scripts/sync_615a_scenarios.py --write"
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected, encoding="utf-8", newline="\n")
    except OSError as exc:
        return False, f"cannot write scenario reader view: {type(exc).__name__}: {exc}"
    return True, "615A scenario reader view synchronized"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--write", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root")
    args = parser.parse_args(argv)
    ok, message = sync(args.root.resolve(), write=args.write)
    print(message, file=sys.stdout if ok else sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
