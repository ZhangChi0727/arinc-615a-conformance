# Problem and Deviation Closure Record Contract

| Field | Value |
|---|---|
| **Version** | 1.0 |
| **Baseline** | RB-2026-001-v4.3 |
| **Classification** | A — certification-grounded |
| **Replaces** | unstructured `deviations: []` concept |

Problems and deviations are controlled, traceable objects rather than free-text
flags. Open major problems prevent objective satisfaction unless a controlled
disposition explicitly allows otherwise.

## Conceptual schema

```yaml
problemId: PRB-...
type:
  - REQUIREMENT
  - TEST
  - TOOL
  - ENVIRONMENT
  - CONFIGURATION
  - IMPLEMENTATION
  - EVIDENCE
  - INTERPRETATION

severity: ...
description: ...

affectedRequirements: []
affectedObjectives: []
affectedVerificationCases: []
affectedEvidenceManifests: []

disposition:
  - OPEN
  - FIXED
  - ACCEPTED_LIMITATION
  - NOT_REPRODUCIBLE
  - DUPLICATE
  - INVALID_TEST
  - WAIVED

correctiveAction: ...
regressionRequired: true
reverificationRefs: []

closureRationale: ...
closureReviewRef: ...
```

## Rules

- every problem traces to affected requirements, objectives, verification
  cases, and evidence manifests;
- closure is reviewed and recorded, not self-declared;
- `ACCEPTED_LIMITATION` must state the residual risk and the scope it bounds;
- regression and reverification references are mandatory when required;
- closed problems remain queryable; they are not deleted.

## Non-claims

Dispositions are project-controlled. They do not constitute authority
conformity decisions or grant certification credit.

---

# 中文版

| 字段 | 内容 |
|---|---|
| **版本** | 1.0 |
| **基线** | RB-2026-001-v4.3 |
| **分类** | A——面向认证 |
| **替代** | 非结构化 `deviations: []` 概念 |

问题与偏差是受控、可追踪的对象，而非自由文本标记。除非受控处置明确允许，未解决重大问题禁止目标满足。

## 概念 schema

```yaml
problemId: PRB-...
type:
  - REQUIREMENT
  - TEST
  - TOOL
  - ENVIRONMENT
  - CONFIGURATION
  - IMPLEMENTATION
  - EVIDENCE
  - INTERPRETATION

severity: ...
description: ...

affectedRequirements: []
affectedObjectives: []
affectedVerificationCases: []
affectedEvidenceManifests: []

disposition:
  - OPEN
  - FIXED
  - ACCEPTED_LIMITATION
  - NOT_REPRODUCIBLE
  - DUPLICATE
  - INVALID_TEST
  - WAIVED

correctiveAction: ...
regressionRequired: true
reverificationRefs: []

closureRationale: ...
closureReviewRef: ...
```

## 规则

每个问题追踪到受影响需求、目标、验证用例和证据清单；关闭经评审并记录而非自声明；`ACCEPTED_LIMITATION` 必须说明残余风险及其限定范围；需要时必须提供回归与重验证引用；已关闭问题保持可查询，不得删除。

## 非主张

处置由项目受控。它们不构成权威符合性决定，也不授予认证信用。