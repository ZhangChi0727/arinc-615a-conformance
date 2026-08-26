# Objective Satisfaction Record Contract

| Field | Value |
|---|---|
| **Version** | 1.0 |
| **Baseline** | RB-2026-001-v4.3 |
| **Classification** | ARINC/Profile candidate — certification-oriented |
| **Generic correspondence** | composite Result/SufficiencyAssessment/Decision/Claim linkage: NOT-DETERMINED |
| **Authority acceptance** | NOT ESTABLISHED |
| **Related object** | Verification Objective |

An Objective Satisfaction Record (OSR) records the reviewed conclusion that a
Verification Objective is closed by controlled evidence. It is not an automatic
aggregation of execution verdicts.

The OSR is an instance composite, not one asserted Generic GVS Core object or a
generic sufficiency algorithm. Evidence characterization, sufficiency reasoning,
decision, and claim linkage remain explicit and independently reviewable.

## Conceptual schema

```yaml
objectiveSatisfactionRecordId: OSR-...
objectiveId: VO-...
objectiveVersion: ...

supportingResultRefs: []
supportingEvidenceItems:
  - evidenceItemId: EVI-...
    evidenceItemVersion: ...
    admissionDecisionRef: EAD-...
    credibilityAssessmentRef: ECA-...
supportingExecutionManifests: []  # provenance only; never direct satisfaction
supportingAnalysisRefs: []
supportingReviewRefs: []
supportingProblemClosureRefs: []

sufficiencyAssessmentRef: SA-...
argumentRef: ARG-...
decisionRef: DEC-...
decisionVersion: ...

objectiveStatus:
  - SATISFIED
  - NOT_SATISFIED
  - OPEN
  - INCOMPLETE

rationale: ...

openProblems: []
deviations: []

reviewedBy: ...
reviewRecordRef: ...
```

## Rules

- objective satisfaction is a reviewed conclusion, not an automatic aggregation;
- every `SATISFIED` conclusion references controlled Results, characterized
  Evidence Items, a SufficiencyAssessment/Argument, and a versioned Decision;
- manifests provide provenance only; a manifest or PASS without admitted
  Evidence Items and the reviewed reasoning/Decision cannot yield `SATISFIED`;
- `INCONCLUSIVE` or invalid supporting executions must not silently disappear;
- open major problems prevent `SATISFIED` unless a controlled disposition
  explicitly allows otherwise and is recorded;
- evidence version mismatch invalidates the closure record;
- a case-level `PASS` never automatically promotes an objective to `SATISFIED`.

## Status semantics

`SATISFIED`, `NOT_SATISFIED`, `OPEN`, and `INCOMPLETE` are objective-level
states and are distinct from the execution-level `PASS`, `FAIL`,
`INCONCLUSIVE`, and `ERROR` verdicts and from compliance claim status. No
automatic state promotion across layers is permitted.

## Non-claims

These states are project-defined and are not FAA, EASA, CAAC, RTCA, SAE, or
EUROCAE authority assurance levels.

---

# 中文版

| 字段 | 内容 |
|---|---|
| **版本** | 1.0 |
| **基线** | RB-2026-001-v4.3 |
| **分类** | ARINC/Profile 候选——面向认证 |
| **Generic 对应** | Result/SufficiencyAssessment/Decision/Claim linkage 复合：NOT-DETERMINED |
| **权威接受** | 尚未建立 |
| **相关对象** | 验证目标 |

目标满足记录（OSR）记录由受控证据关闭某验证目标的受评审结论。它不是执行判定的自动聚合。

OSR 是实例复合工件，不被声明为单个 Generic GVS Core 对象或通用充分性算法。证据表征、
充分性推理、决定和主张链接保持显式且可独立评审。

## 概念 schema

```yaml
objectiveSatisfactionRecordId: OSR-...
objectiveId: VO-...
objectiveVersion: ...

supportingResultRefs: []
supportingEvidenceItems:
  - evidenceItemId: EVI-...
    evidenceItemVersion: ...
    admissionDecisionRef: EAD-...
    credibilityAssessmentRef: ECA-...
supportingExecutionManifests: []  # 只提供来源；不得直接形成满足结论
supportingAnalysisRefs: []
supportingReviewRefs: []
supportingProblemClosureRefs: []

sufficiencyAssessmentRef: SA-...
argumentRef: ARG-...
decisionRef: DEC-...
decisionVersion: ...

objectiveStatus:
  - SATISFIED
  - NOT_SATISFIED
  - OPEN
  - INCOMPLETE

rationale: ...

openProblems: []
deviations: []

reviewedBy: ...
reviewRecordRef: ...
```

## 规则

目标满足是受评审结论而非自动聚合；每个 `SATISFIED` 必须引用受控 Result、经表征准入的
Evidence Item、SufficiencyAssessment/Argument 和版本化 Decision；manifest 只提供来源，
没有准入 Evidence Item 与受评审推理/Decision 时，manifest 或 PASS 不得形成 `SATISFIED`；
`INCONCLUSIVE` 或无效支持执行不得静默消失；除非受控处置明确允许并已记录，否则未解决重大
问题禁止 `SATISFIED`；证据版本不匹配使关闭记录失效；用例级 `PASS` 不得自动晋级目标。

## 状态语义

`SATISFIED`、`NOT_SATISFIED`、`OPEN`、`INCOMPLETE` 为目标级状态，区别于执行级 `PASS`、`FAIL`、`INCONCLUSIVE`、`ERROR` 判定与合规主张状态。禁止跨层自动状态晋级。

## 非主张

这些状态为项目自定义，不是 FAA、EASA、CAAC、RTCA、SAE 或 EUROCAE 的权威保证层级。
