"""Render the single-authority CL-TAV development review view."""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

import check_development_readiness as readiness

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "configs/engineering/cltav_development_contracts.json"
VIEW = ROOT / "docs/engineering/CLTAV_DEVELOPMENT_REVIEW_VIEW.md"


def plain_text(value: object) -> str:
    """Render controlled free text without allowing it to alter Markdown structure."""
    text = str(value).replace("\r\n", "\n").replace("\r", "\n")
    return html.escape(text, quote=False).replace("\\", "\\\\").replace("`", "\\`").replace("|", "\\|").replace("\n", "<br>")


def render(data: dict) -> str:
    rows = data["protocolInputDispositions"]
    counts = {name: sum(row["disposition"] == name for row in rows) for name in sorted({row["disposition"] for row in rows})}
    lines = [
        "# CL-TAV Development Readiness Review View", "",
        "> Generated from `configs/engineering/cltav_development_contracts.json`; do not edit.", "",
        f"- Control: `{data['control']['changeRequest']}`; decisions {', '.join(data['control']['decisions'])}",
        f"- Bound M1 requirements: {len(rows)}; disposition total: {sum(counts.values())}; readiness: `{data['reviewBoundary']['readiness']}`; claim: `{data['reviewBoundary']['claims']}`",
        "", "## Inputs", "",
    ]
    lines += [f"- `{item['artifactId']}` — `{item['path']}` — SHA-256 `{item['sha256']}` — {plain_text(item['purpose'])}" for item in data["inputBindings"]]
    lines += ["", "## Record contracts", "", "| ID | Owner | Fields | Uncertainty |", "|---|---|---|---|"]
    lines += [f"| `{item['id']}` | `{item['ownerModuleId']}` | {', '.join(f'`{field}`' for field in item['fields'])} | {plain_text(item['uncertainty'])} |" for item in data["recordContracts"]]
    for item in data["recordContracts"]:
        lines += ["", f"### `{item['id']}` — {plain_text(item['title'])}", f"- Ownership: {plain_text(item['ownership'])}", f"- Uncertainty: {plain_text(item['uncertainty'])}", f"- Source requirements: {', '.join(f'`{value}`' for value in item.get('sourceRequirementIds', [])) or 'None'}", f"- Error behavior: {plain_text(item['errorBehavior'])}", f"- Field definitions: `{json.dumps(item['fieldDefinitions'], ensure_ascii=False, sort_keys=True)}`", f"- Valid example: `{json.dumps(item['example'], ensure_ascii=False, sort_keys=True)}`", f"- Invalid example: `{json.dumps(item['invalidExample'], ensure_ascii=False, sort_keys=True)}`", f"- Expected rejection: `{json.dumps(item['invalidExpected'], ensure_ascii=False, sort_keys=True)}`", f"- Rejection reason: {plain_text(item['invalidReason'])}"]
    lines += ["", "## Tool requirements", "", "| ID | Owner | Source relation | Acceptance | Requirement |", "|---|---|---|---|---|"]
    lines += [f"| `{item['id']}` | `{item['ownerModuleId']}` | `{item['sourceRelationship']}` | `{item['acceptanceCaseId']}` | {plain_text(item['title'])} |" for item in data["toolRequirements"]]
    for item in data["toolRequirements"]:
        lines += ["", f"### `{item['id']}` — {plain_text(item['title'])}", f"- Trigger: {plain_text(item['trigger'])}", f"- Preconditions: {plain_text('; '.join(item['preconditions']))}", f"- Inputs: {', '.join(f'`{value}`' for value in item['inputRecordIds'])}; outputs: {', '.join(f'`{value}`' for value in item['outputRecordIds'])}", f"- Action: {plain_text(item['action'])}", f"- Error/unknown: {plain_text(item['errorUnknown'])}", f"- Evidence: {plain_text(item['evidence'])}", f"- Interfaces: {', '.join(f'`{value}`' for value in item['interfaceIds'])}; CRS: {', '.join(f'`{value}`' for value in item['protocolRequirementIds']) or '—'}; control/method: {', '.join(f'`{value}`' for value in item['traceability'])}"]
    lines += ["", "## Module contracts", "", "Upstream policy: every cross-module input producer must be directly or transitively reachable through `upstreamModuleIds`; external inputs and records produced by the consuming module itself require no upstream edge.", ""]
    for item in data["moduleContracts"]:
        lines += [
            f"### `{item['id']}` — {plain_text(item['title'])}",
            f"- Responsibility: {plain_text(item['responsibility'])}",
            f"- Preconditions: {plain_text('; '.join(item['preconditions']))}",
            f"- Inputs: {', '.join(f'`{value}`' for value in item['inputRecordIds'])}; outputs: {', '.join(f'`{value}`' for value in item['outputRecordIds'])}",
            f"- Requirements: {', '.join(f'`{value}`' for value in item['toolRequirementIds'])}; interfaces: {', '.join(f'`{value}`' for value in item['interfaceIds'])}",
            f"- Acceptance: {', '.join(f'`{value}`' for value in item['acceptanceCaseIds'])}; runtime parameters: {', '.join(f'`{value}`' for value in item['runtimeParameterIds'])}; upstream: {', '.join(f'`{value}`' for value in item['upstreamModuleIds']) or 'None'}",
            "- Steps:",
        ]
        lines += [f"  - `{step['id']}`: {plain_text(step['action'])}" for step in item["steps"]]
        lines += [f"- Invariants: {plain_text('; '.join(item['invariants']))}", "- Failure outcomes:"]
        lines += [f"  - `{outcome['code']}` — when {plain_text(outcome['condition'])} Result: {plain_text(outcome['result'])}" for outcome in item["failureOutcomes"]]
        lines += ["- Output value mappings:"]
        lines += [f"  - `{mapping['recordId']}.{mapping['field']}` → {', '.join(f'`{value}`' for value in mapping['emittedValues'])}: {plain_text(mapping['meaning'])}" for mapping in item["outputValueMappings"]] or ["  - None"]
    lines += ["", "## Bounded algorithm refinement", ""]
    for refinement in data["algorithmRefinements"]:
        lines += [f"### `{refinement['id']}` — {plain_text(refinement['title'])}", f"- Boundary: {plain_text(refinement['boundary'])}", f"- Representation: {plain_text(refinement['representation'])}", f"- Conservative behavior: {plain_text(refinement['conservatism'])}", f"- Complexity boundary: {plain_text(refinement['complexity'])}", "- Interface bindings:"]
        lines += [f"  - `{binding['interfaceId']}` — inputs {', '.join(f'`{value}`' for value in binding['inputTypes'])}; outputs {', '.join(f'`{value}`' for value in binding['outputTypes'])}; read: {plain_text(binding['readOwnership'])}; write: {plain_text(binding['writeOwnership'])}; failures: {', '.join(f'`{value}`' for value in binding['failureTags'])}; parameters: {', '.join(f'`{value}`' for value in binding['runtimeParameterIds'])}; time: {plain_text(binding['timeContract'])}; acceptance: {', '.join(f'`{value}`' for value in binding['acceptanceCaseIds'])}; location: `{binding['implementationLocation']}`" for binding in refinement["interfaceBindings"]]
    lines += ["", "## Runtime parameter contracts", ""]
    for item in data["runtimeParameterContracts"]:
        lines += [f"### `{item['id']}` — {plain_text(item['title'])}", f"- Unit/domain: {plain_text(item['unit'])} / `{item['domain']}`", f"- Configuration: {plain_text(item['configurationRequirement'])}", f"- Owner scope: {plain_text(item['ownerScope'])}", f"- Exhaustion: {plain_text(item['exhaustionBehavior'])}", f"- Acceptance: {', '.join(f'`{value}`' for value in item['acceptanceCaseIds'])}"]
    lines += ["", "## Acceptance cases", ""]
    for item in data["acceptanceCases"]:
        lines += [f"### `{item['id']}` — {plain_text(item['title'])}", f"- Inputs: {', '.join(f'`{value}`' for value in item['inputRecordIds'])}", f"- Tools: {', '.join(f'`{value}`' for value in item['toolRequirementIds'])}; modules: {', '.join(f'`{value}`' for value in item['moduleIds'])}; interfaces: {', '.join(f'`{value}`' for value in item['algorithmInterfaceIds'])}", f"- Expected: {plain_text(item['expectedContractOutput'])}", f"- Prohibited: {plain_text(item['prohibitedOutput'])}", f"- Basis: {plain_text(item['basis'])}; witness: `{item['witnessLevel']}`; runtime: `{item['runtimeExecutionStatus']}`"]
    lines += ["", "## Slices and dependencies", ""]
    lines += [f"- `{item['id']}` — {plain_text(item['scope'])} — {len(item['requirementIds'])} requirement uses" for item in data["implementationSlices"]]
    lines += [f"- dependency `{item['id']}`: `{item['status']}`" for item in data["implementationDependencies"]]
    lines += ["", "## Slice membership relations", "", "| Slice | Requirement |", "|---|---|"]
    lines += [f"| `{item['id']}` | `{requirement_id}` |" for item in data["implementationSlices"] for requirement_id in item["requirementIds"]]
    lines += [
        "", "## Disposition summary", "",
        "| Disposition | Count |", "|---|---:|",
    ]
    lines += [f"| `{name}` | {count} |" for name, count in counts.items()]
    lines += ["", "## All requirement dispositions", "", "| Requirement | Disposition | First slice | Module | Record | Acceptance | Rationale |", "|---|---|---|---|---|---|---|"]
    lines += [f"| `{row['inputRequirementId']}` | `{row['disposition']}` | `{row['firstSliceRequired']}` | `{row.get('moduleId','—')}` | `{row.get('recordId','—')}` | `{row.get('acceptanceCaseId','—')}` | {plain_text(row['rationale'])} |" for row in rows]
    lines += ["", "# 中文版", "", "# CL-TAV 开发就绪评审视图", "", "> 由同一权威 JSON 生成，禁止手工修改。", "", f"- 控制：`{data['control']['changeRequest']}`；设计决策：{', '.join(f'`{decision}`' for decision in data['control']['decisions'])}", f"- 绑定 M1 需求：{len(rows)}；处置合计：{sum(counts.values())}；就绪状态：`{data['reviewBoundary']['readiness']}`；主张边界：`{data['reviewBoundary']['claims']}`", "", "## 输入身份", ""]
    lines += [f"- `{item['artifactId']}` — `{item['path']}` — SHA-256 `{item['sha256']}` — {plain_text(item['purposeZh'])}" for item in data["inputBindings"]]
    lines += ["", "## 记录合同", "", "| ID | 责任模块 | 字段 | 不确定性 |", "|---|---|---|---|"]
    lines += [f"| `{item['id']}` | `{item['ownerModuleId']}` | {', '.join(f'`{field}`' for field in item['fields'])} | {plain_text(item['uncertaintyZh'])} |" for item in data["recordContracts"]]
    for item in data["recordContracts"]:
        lines += ["", f"### `{item['id']}` — {plain_text(item['titleZh'])}", f"- 所有权：{plain_text(item['ownershipZh'])}", f"- 不确定性：{plain_text(item['uncertaintyZh'])}", f"- 来源需求：{', '.join(f'`{value}`' for value in item.get('sourceRequirementIds', [])) or '无'}", f"- 错误行为：{plain_text(item['errorBehaviorZh'])}", f"- 字段定义：`{json.dumps(item['fieldDefinitions'], ensure_ascii=False, sort_keys=True)}`", f"- 有效示例：`{json.dumps(item['example'], ensure_ascii=False, sort_keys=True)}`", f"- 无效示例：`{json.dumps(item['invalidExample'], ensure_ascii=False, sort_keys=True)}`", f"- 预期拒绝：`{json.dumps(item['invalidExpected'], ensure_ascii=False, sort_keys=True)}`", f"- 拒绝理由：{plain_text(item['invalidReasonZh'])}"]
    lines += ["", "## 工具需求", "", "| ID | 责任模块 | 来源关系 | 验收 | 需求 |", "|---|---|---|---|---|"]
    lines += [f"| `{item['id']}` | `{item['ownerModuleId']}` | `{item['sourceRelationship']}` | `{item['acceptanceCaseId']}` | {plain_text(item['titleZh'])} |" for item in data["toolRequirements"]]
    for item in data["toolRequirements"]:
        lines += ["", f"### `{item['id']}` — {plain_text(item['titleZh'])}", f"- 触发：{plain_text(item['triggerZh'])}", f"- 前置条件：{plain_text('；'.join(item['preconditionsZh']))}", f"- 输入：{', '.join(f'`{value}`' for value in item['inputRecordIds'])}；输出：{', '.join(f'`{value}`' for value in item['outputRecordIds'])}", f"- 动作：{plain_text(item['actionZh'])}", f"- 错误／未知：{plain_text(item['errorUnknownZh'])}", f"- 证据：{plain_text(item['evidenceZh'])}", f"- 接口：{', '.join(f'`{value}`' for value in item['interfaceIds'])}；CRS：{', '.join(f'`{value}`' for value in item['protocolRequirementIds']) or '—'}；控制／方法：{', '.join(f'`{value}`' for value in item['traceability'])}"]
    lines += ["", "## 模块合同", "", "上游策略：每个跨模块输入的生产者必须能通过 `upstreamModuleIds` 直接或传递到达；外部输入以及由消费模块自身产生的记录无需上游边。", ""]
    for item in data["moduleContracts"]:
        lines += [
            f"### `{item['id']}` — {plain_text(item['titleZh'])}",
            f"- 职责：{plain_text(item['responsibilityZh'])}",
            f"- 前置条件：{plain_text('；'.join(item['preconditionsZh']))}",
            f"- 输入：{', '.join(f'`{value}`' for value in item['inputRecordIds'])}；输出：{', '.join(f'`{value}`' for value in item['outputRecordIds'])}",
            f"- 需求：{', '.join(f'`{value}`' for value in item['toolRequirementIds'])}；接口：{', '.join(f'`{value}`' for value in item['interfaceIds'])}",
            f"- 验收：{', '.join(f'`{value}`' for value in item['acceptanceCaseIds'])}；运行参数：{', '.join(f'`{value}`' for value in item['runtimeParameterIds'])}；上游：{', '.join(f'`{value}`' for value in item['upstreamModuleIds']) or '无'}",
            "- 步骤：",
        ]
        lines += [f"  - `{step['id']}`：{plain_text(step['actionZh'])}" for step in item["steps"]]
        lines += [f"- 不变量：{plain_text('；'.join(item['invariantsZh']))}", "- 失败结果："]
        lines += [f"  - `{outcome['code']}` — 条件：{plain_text(outcome['conditionZh'])} 结果：{plain_text(outcome['resultZh'])}" for outcome in item["failureOutcomes"]]
        lines += ["- 输出值映射："]
        lines += [f"  - `{mapping['recordId']}.{mapping['field']}` → {', '.join(f'`{value}`' for value in mapping['emittedValues'])}：{plain_text(mapping['meaningZh'])}" for mapping in item["outputValueMappings"]] or ["  - 无"]
    lines += ["", "## 有界算法细化", ""]
    for refinement in data["algorithmRefinements"]:
        lines += [f"### `{refinement['id']}` — {plain_text(refinement['titleZh'])}", f"- 边界：{plain_text(refinement['boundaryZh'])}", f"- 表示：{plain_text(refinement['representationZh'])}", f"- 保守行为：{plain_text(refinement['conservatismZh'])}", f"- 复杂度边界：{plain_text(refinement['complexityZh'])}", "- 接口绑定："]
        lines += [f"  - `{binding['interfaceId']}` — 输入：{', '.join(f'`{value}`' for value in binding['inputTypes'])}；输出：{', '.join(f'`{value}`' for value in binding['outputTypes'])}；读取：{plain_text(binding['readOwnership'])}；写入：{plain_text(binding['writeOwnership'])}；失败：{', '.join(f'`{value}`' for value in binding['failureTags'])}；参数：{', '.join(f'`{value}`' for value in binding['runtimeParameterIds'])}；时序：{plain_text(binding['timeContractZh'])}；验收：{', '.join(f'`{value}`' for value in binding['acceptanceCaseIds'])}；位置：`{binding['implementationLocation']}`" for binding in refinement["interfaceBindings"]]
    lines += ["", "## 运行参数合同", ""]
    for item in data["runtimeParameterContracts"]:
        lines += [f"### `{item['id']}` — {plain_text(item['titleZh'])}", f"- 单位／域：{plain_text(item['unit'])} / `{item['domain']}`", f"- 配置条件：{plain_text(item['configurationRequirementZh'])}", f"- 责任范围：{plain_text(item['ownerScope'])}", f"- 耗尽行为：{plain_text(item['exhaustionBehaviorZh'])}", f"- 验收：{', '.join(f'`{value}`' for value in item['acceptanceCaseIds'])}"]
    lines += ["", "## 验收案例", ""]
    for item in data["acceptanceCases"]:
        lines += [f"### `{item['id']}` — {plain_text(item['titleZh'])}", f"- 输入：{', '.join(f'`{value}`' for value in item['inputRecordIds'])}", f"- 工具：{', '.join(f'`{value}`' for value in item['toolRequirementIds'])}；模块：{', '.join(f'`{value}`' for value in item['moduleIds'])}；接口：{', '.join(f'`{value}`' for value in item['algorithmInterfaceIds'])}", f"- 预期：{plain_text(item['expectedContractOutput'])}", f"- 禁止：{plain_text(item['prohibitedOutput'])}", f"- 依据：{plain_text(item['basisZh'])}；见证：`{item['witnessLevel']}`；运行：`{item['runtimeExecutionStatus']}`"]
    lines += ["", "## 切片与依赖", ""]
    lines += [f"- `{item['id']}` — {plain_text(item['scopeZh'])} — {len(item['requirementIds'])} 条需求用途" for item in data["implementationSlices"]]
    lines += [f"- 依赖 `{item['id']}`：`{item['status']}`" for item in data["implementationDependencies"]]
    lines += ["", "## 切片成员关系", "", "| 切片 | 需求 |", "|---|---|"]
    lines += [f"| `{item['id']}` | `{requirement_id}` |" for item in data["implementationSlices"] for requirement_id in item["requirementIds"]]
    lines += ["", "## 处置摘要", "", "| 处置 | 数量 |", "|---|---:|"]
    lines += [f"| `{name}` | {count} |" for name, count in counts.items()]
    lines += ["", "## 全部需求处置", "", "| 需求 | 处置 | 首轮 | 模块 | 记录 | 验收 | 理由 |", "|---|---|---|---|---|---|---|"]
    lines += [f"| `{row['inputRequirementId']}` | `{row['disposition']}` | `{row['firstSliceRequired']}` | `{row.get('moduleId','—')}` | `{row.get('recordId','—')}` | `{row.get('acceptanceCaseId','—')}` | {plain_text(row['rationaleZh'])} |" for row in rows]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.loads(PACKAGE.read_text(encoding="utf-8"))
    errors = readiness.package_errors(data)
    if errors:
        print("development review view refused: " + "; ".join(errors), file=sys.stderr)
        return 1
    expected = render(data)
    actual = VIEW.read_text(encoding="utf-8") if VIEW.exists() else ""
    if args.write:
        VIEW.write_text(expected, encoding="utf-8", newline="\n")
        return 0
    if actual != expected:
        print("development review view is stale; run sync_development_readiness.py --write", file=sys.stderr)
        return 1
    print("development review view is synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
