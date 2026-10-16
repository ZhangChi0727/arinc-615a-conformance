"""Render and reconcile the bilingual shared experiment-design tables."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

from check_experiment_design import DESIGN_PATH, ROOT, accounting_summary, validate_design


SPEC_PATH = Path("docs/research/EXPERIMENT_IMPLEMENTATION_SPEC.md")
START = "<!-- experiment-design-shared:start -->"
END = "<!-- experiment-design-shared:end -->"


def _cell(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "yes / 是" if value else "no / 否"
    if isinstance(value, list):
        return "<br>".join(_cell(item) for item in value) if value else "—"
    if isinstance(value, dict):
        return "; ".join(f"{key}={_cell(item)}" for key, item in sorted(value.items()))
    return str(value).replace("|", "\\|").replace("\n", " ")


def _table(headers: list[str], rows: Iterable[Iterable[Any]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    output.extend("| " + " | ".join(_cell(value) for value in row) + " |" for row in rows)
    return "\n".join(output)


ZH = {
    "ALGORITHM-INITIAL": "算法初始可见",
    "ALGORITHM-OWN-ACTION": "算法自身动作所得",
    "EVALUATOR-ONLY": "仅评估方可见",
    "PRIMARY": "主要",
    "SECONDARY": "次要",
    "EXPLORATORY": "探索性",
    "CANDIDATE-METHOD": "候选方法",
    "WAIT-DEC-SAMPLE": "等待样本量决定",
    "DETERMINISTIC-EXHAUSTIVE": "确定性穷举",
    "INDEPENDENT-RANDOMIZED": "独立随机",
    "PAIRED-OR-CLUSTERED": "配对或聚类",
    "FLOW-ONLY": "仅流程描述",
}


def _bilingual_token(value: Any) -> str:
    text = str(value)
    return f"{text} / {ZH[text]}" if text in ZH else text


def render_shared_block(data: dict[str, Any]) -> str:
    claims = sorted(data["claimArguments"], key=lambda row: row["claimId"])
    arms = sorted(data["arms"], key=lambda row: row["id"])
    scenarios = sorted(data["scenarios"], key=lambda row: row["id"])
    dispositions = sorted(data["acceptanceMatrixDispositions"], key=lambda row: row["id"])
    metrics = sorted(data["metrics"], key=lambda row: row["id"])
    field_contracts = sorted(data["metricFieldContracts"], key=lambda row: row["field"])
    dependencies = sorted(data["dependencies"], key=lambda row: row["id"])
    decisions = sorted(data["pendingDecisions"], key=lambda row: row["id"])
    analyses = sorted(data["analysisPlans"], key=lambda row: row["id"])
    comparisons = sorted(data["comparisonFamilies"], key=lambda row: row["id"])
    choices = sorted(data["analysisChoiceWalkthroughs"], key=lambda row: row["id"])
    contrasts = sorted(data["registeredContrasts"], key=lambda row: row["id"])
    timelines = sorted(data["protocolTimelineWalkthroughs"], key=lambda row: row["id"])
    update_relations = sorted(data["updateDecisionRelations"], key=lambda row: row["interpretationDisposition"])
    interpretation_contracts = sorted(data["walkthroughInterpretationContracts"], key=lambda row: row["walkthroughId"])
    translations = data["translationsZh"]
    summary = accounting_summary(data)

    def zh(group: str, row_id: str) -> str:
        return translations[f"{group}.{row_id}.summary"]

    def proposal(field: dict[str, Any]) -> list[Any]:
        return [
            f"{field['path']} ({field['type']}; {field['visibility']})",
            *[
                f"member {item['name']}:{item['type']} [{item['role']}]"
                for item in field.get("members", [])
            ],
            *[
                f"forbidden {name}" for name in field.get("limits", {}).get("forbiddenMembers", [])
            ],
        ]

    parts = [
        START,
        "",
        "> Generated from `configs/research/cltav_experiment_design.json`; edit the JSON and run "
        "`python scripts/sync_experiment_design.py --write`. / 本区由结构化设计合同生成；请勿直接修改。",
        "",
        "### Claim and arm boundary / 主张与实验臂边界",
        "",
        _table(
            ["Claim / 主张", "Bounded proposition", "Assumptions", "Falsifiers", "Controlled Chinese / 受控中文", "Gate / 门禁"],
            ((row["claimId"], row["boundedProposition"], row["assumptions"], row["falsifiers"], zh("claimArguments", row["claimId"]), row["reviewGate"]) for row in claims),
        ),
        "",
        _table(
            ["Arm / 实验臂", "Visible inputs / 可见输入", "Actions", "Feedback / 反馈", "Prohibited", "Controlled Chinese / 受控中文"],
            ((row["id"], [f"{item['ref']} ({_bilingual_token(item['role'])})" for item in row["visibleInputs"]], row["actions"], row["feedback"], row["prohibitedRefs"], zh("arms", row["id"])) for row in arms),
        ),
        "",
        _table(
            ["Registered contrast / 注册对比", "Family / 实验族", "Arms / 实验臂", "Parent metrics / 父指标"],
            ((row["id"], row["familyId"], row["armIds"], row["parentMetricIds"]) for row in contrasts),
        ),
        "",
        "### Scenario contract / 场景合同",
        "",
        _table(
            ["Scenario / 场景", "Scope / 服务", "Development + CRS / 开发与需求", "Acceptance / 验收", "Perturbation", "Records / 记录", "Admission", "Controlled Chinese / 受控中文"],
            (
                (
                    row["id"], row["serviceScope"],
                    [row["developmentScenarioRef"], row["crsDisposition"], *row["crsRefs"]],
                    [*row["acceptanceCaseRefs"], *row["acceptanceMatrixRefs"]],
                    [row["perturbationPoint"], row["truthConfirmation"], row["observableOutcome"]],
                    row["requiredRecords"], row["admissionRule"], zh("scenarios", row["id"]),
                )
                for row in scenarios
            ),
        ),
        "",
        "### Acceptance-matrix disposition / 验收矩阵处置",
        "",
        _table(
            ["AM id / 编号", "Disposition / 处置", "Consumers / 使用方", "Rationale / 理由"],
            ((row["id"], row["disposition"], row["consumerRefs"], row["rationale"]) for row in dispositions),
        ),
        "",
        "### Metric dictionary / 指标字典",
        "",
        _table(
            ["Metric / 指标", "Population / 分母总体", "Numerator / 分子总体", "Calculation", "Missing + censoring", "Required fields / 必需字段", "Controlled Chinese / 受控中文", "Analysis / 分析", "Primary / 主要"],
            (
                (
                    row["id"], row["populationId"], row["numeratorPopulationId"], row["calculation"],
                    [row["missingRule"], row["censoringRule"], f"zero={row['zeroDenominator']}"],
                    row["requiredFields"], zh("metrics", row["id"]), row["analysisPlanId"], row["primary"],
                )
                for row in metrics
            ),
        ),
        "",
        "### Metric-field handoff / 指标字段交接",
        "",
        _table(
            ["Field / 字段", "Kind + source / 类型与来源", "Inputs + rule / 输入与规则", "Proposal / 提议", "Producer / 生产者", "Visibility + compatibility / 可见性与兼容性", "Dependency + closure / 依赖与闭合", "Consumers / 使用指标"],
            (
                (
                    row["field"], [row["sourceKind"], row["sourcePath"]], [*row["sourceInputPaths"], row["derivationRule"]],
                    f"proposal={row['proposalFieldPath']}", row["producerRole"],
                    [row["visibility"], row["backwardCompatibility"]], [row["dependencyId"], row["closureMilestone"]],
                    row["consumerMetricIds"],
                )
                for row in field_contracts
            ),
        ),
        "",
        "### Analysis decisions / 分析决定",
        "",
        _table(
            ["Plan / 方案", "Estimand", "Unit + pairing / 单位与配对", "Estimator + interval", "Applicability", "Controlled Chinese / 受控中文", "Method status / 方法状态", "Evidence / 方法证据", "Freeze / 冻结决定"],
            (
                (
                    row["id"], row["estimand"], [row["unit"], row["pairing"]],
                    [row["estimator"], row["interval"], _bilingual_token(row["choiceBranch"]), _bilingual_token(row["missingInputResult"])], row["applicability"],
                    zh("analysisPlans", row["id"]), row["methodStatus"], [*row["methodEvidenceIds"], *row["sourceLocators"]], row["freezeDecisionId"],
                )
                for row in analyses
            ),
        ),
        "",
        "### Comparison families / 比较族",
        "",
        _table(
            ["Family / 比较族", "Class / 类别", "Metrics / 指标", "Contrasts", "Joint conclusion", "Multiplicity", "Controlled Chinese / 受控中文"],
            ((row["id"], _bilingual_token(row["classification"]), row["metricIds"], row["contrasts"], row["jointConclusion"], row["multiplicityDisposition"], zh("comparisonFamilies", row["id"])) for row in comparisons),
        ),
        "",
        "### Engineering dependencies / 工程依赖",
        "",
        _table(
            ["Dependency / 依赖", "Consumers / 使用方", "Current ref / 当前引用", "Evidence + producer", "State + typed proposal / 状态与类型化提议", "Decisions / 决定", "Closure + follow-up", "Controlled Chinese / 受控中文", "Milestone / 里程碑"],
            (
                (
                    row["id"], row["consumers"], row["currentReference"], [row["neededEvidence"], row["producer"]],
                    [row["state"], *[item for field in row["proposalFields"] for item in proposal(field)]], row["decisionIds"],
                    [row["closureTest"], row["minimumFollowUp"]], zh("dependencies", row["id"]), row["blockingMilestone"],
                )
                for row in dependencies
            ),
        ),
        "",
        "### Interpretation/update decision relation / 解释与更新决定关系",
        "",
        _table(
            ["Interpretation / 解释", "Update source / 更新来源", "Update status / 更新状态", "Preserve history / 保留历史", "Current decision / 当前决定"],
            (
                (
                    row["interpretationDisposition"], row["updateSource"], row["updateStatus"],
                    row["preserveHistory"], row["currentDecisionPermitted"],
                )
                for row in update_relations
            ),
        ),
        "",
        _table(
            ["Walkthrough / 走查", "Interpretation / 解释", "Update source / 更新来源"],
            ((row["walkthroughId"], row["interpretationDisposition"], row["updateSource"]) for row in interpretation_contracts),
        ),
        "",
        "### Hypothetical method-choice walkthroughs / 假设性方法选择见证",
        "",
        _table(
            ["Choice / 选择", "Label / 标签", "Inputs / 输入", "Branch / 分支", "Result / 结果", "Rationale / 理由"],
            ((row["id"], "HYPOTHETICAL-NOT-RESULT / 假设示例，非结果", [row["domainEnumeration"], row["randomAssignment"], row["dependence"], f"pair={row['pairingEvidence']}", f"cluster={row['clusterEvidence']}", f"unit={row['independentUnit']}"] , _bilingual_token(row["selectedBranch"]), _bilingual_token(row["result"]), row["rationale"]) for row in choices),
        ),
        "",
        "### CRS-M1-00101 protocol timelines / CRS-M1-00101 协议时间线",
        "",
        _table(
            ["Timeline / 时间线", "Trigger / 触发", "Observed / 观测", "Elapsed / 经过时间", "Expiry / 到期端点", "Abort duty / 中止义务", "Finite observation / 有限观察终点", "Outcome / 结果"],
            (
                (
                    row["id"], row["trigger"], row["receivedEvent"], row["elapsedSeconds"],
                    row["timerExpiryBoundary"],
                    [row["abortObligation"], f"completionBound={row['abortCompletionBoundSeconds']}"],
                    [f"end={row['observationEndSeconds']}", f"qualified={row['observationEndQualified']}"],
                    row["outcome"],
                )
                for row in timelines
            ),
        ),
        "",
        "### Open decisions / 待定决定",
        "",
        _table(
            ["Decision / 决定", "Owner / 负责人", "Inputs", "Procedure", "Freeze / 冻结点", "Closure witness", "Controlled Chinese / 受控中文"],
            (
                (
                    row["id"], row["ownerRole"], row["inputEvidence"], row["selectionProcedure"],
                    row["freezeBy"], row["closureWitness"], zh("pendingDecisions", row["id"]),
                )
                for row in decisions
            ),
        ),
        "",
        "### Synthetic accounting witness / 合成记账见证",
        "",
        _table(
            ["Attempts / 尝试", "Answered / 已回答", "Coverage / 覆盖", "Conditional error / 条件错误", "Localization coverage / 定位覆盖", "Projected cost / 投影成本", "Review/setup / 评审准备工作量"],
            [
                (
                    summary["attempts"], summary["answered"], summary["answeredCoverage"],
                    summary["conditionalDetectionError"], summary["localizationDecisionCoverage"],
                    summary["projectedCostTotals"], summary["reviewSetupEffort"],
                )
            ],
        ),
        "",
        END,
    ]
    return "\n".join(parts)


def reconcile_text(text: str, generated: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if normalized.count(START) != 1 or normalized.count(END) != 1:
        raise ValueError("spec must contain exactly one generated-block marker pair")
    before, remainder = normalized.split(START, 1)
    _, after = remainder.split(END, 1)
    return before + generated + after


def sync(root: Path = ROOT, *, write: bool = False) -> tuple[bool, str]:
    errors = validate_design(root)
    if errors:
        return False, "authority/design validation failed; spec was not changed:\n" + "\n".join(f"- {item}" for item in errors)
    try:
        data = json.loads((root / DESIGN_PATH).read_text(encoding="utf-8"))
        path = root / SPEC_PATH
        current = path.read_text(encoding="utf-8")
        expected = reconcile_text(current, render_shared_block(data))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return False, f"cannot reconcile experiment spec: {exc}"
    current_normalized = current.replace("\r\n", "\n").replace("\r", "\n")
    if current_normalized == expected:
        return True, "experiment design spec is synchronized"
    if not write:
        return False, "experiment design spec has generated-table drift; run with --write"
    path.write_text(expected, encoding="utf-8", newline="\n")
    return True, "experiment design spec synchronized"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--write", action="store_true")
    args = parser.parse_args()
    ok, message = sync(write=args.write)
    print(message)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
