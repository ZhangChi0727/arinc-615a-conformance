# Verification Objective Contract

| Field | Value |
|---|---|
| **Version** | 1.0 |
| **Baseline** | RB-2026-001-v4.3 |
| **Classification** | ARINC/Profile candidate — certification-oriented |
| **Generic correspondence** | VerificationObligation: NOT-DETERMINED |
| **Authority acceptance** | NOT ESTABLISHED |
| **Supersedes** | none (new layer above Test Purpose) |

A Verification Objective (VO) states what fact must be demonstrated to close a
referenced requirement obligation. A test case is not itself an assurance
objective: one requirement may require several test, analysis, inspection, or
review activities before it can be considered closed.

## Conceptual schema

```yaml
objectiveId: VO-...
version: ...
status: DRAFT | REVIEWED | APPROVED | RETIRED

requirementRefs:
  - CRS-...

objectiveType:
  - functional
  - state
  - transition
  - data
  - timing
  - negative
  - sequence
  - integration
  - configuration
  - recovery

statement: >
  What fact must be demonstrated to close the referenced requirement obligation.

acceptanceCriteria:
  - ...

verificationMethods:
  - TEST
  - ANALYSIS
  - REVIEW
  - INSPECTION
  - DEMONSTRATION

testPurposeRefs: []
verificationCaseRefs: []
analysisRefs: []
reviewRefs: []

requiredEvidenceClasses:
  - raw_trace
  - configuration
  - timing
  - review
  - analysis

closureRule:
  allRequiredActivitiesComplete: true
  unresolvedMajorProblemsAllowed: false

reviewRecordRefs: []
```

## Semantics

- one requirement can map to multiple verification objectives;
- one objective can require multiple methods or activities;
- one verification case can support multiple objectives only when traceability
  is explicit;
- objectives are not automatically satisfied by a case `PASS`;
- satisfaction is a reviewed conclusion recorded in an Objective Satisfaction
  Record, not an automatic aggregation.

## Classification note

This is a local ARINC/Profile candidate object. It may correspond to a
VerificationObligation role, but equivalence and Generic definition authority
are `NOT-DETERMINED`. Its aviation-oriented structure does not establish
authority approval or make the object part of the Generic GVS Core.

## Non-claims

- certification-oriented does not mean certification-approved;
- a Verification Objective is project-defined and is not an authority-mandated
  data item copied from a standard;
- satisfying all objectives does not establish aircraft-level airworthiness.

---

# 中文版

| 字段 | 内容 |
|---|---|
| **版本** | 1.0 |
| **基线** | RB-2026-001-v4.3 |
| **分类** | ARINC/Profile 候选——面向认证 |
| **Generic 对应** | VerificationObligation：NOT-DETERMINED |
| **权威接受** | 尚未建立 |
| **替代** | 无（位于测试目的之上的新层） |

验证目标（VO）声明为关闭所引用需求义务而必须证明的事实。测试用例本身不是保证目标：一个需求在关闭前可能需要多项测试、分析、检查或评审活动。

## 概念 schema

```yaml
objectiveId: VO-...
version: ...
status: DRAFT | REVIEWED | APPROVED | RETIRED

requirementRefs:
  - CRS-...

objectiveType:
  - functional
  - state
  - transition
  - data
  - timing
  - negative
  - sequence
  - integration
  - configuration
  - recovery

statement: >
  为关闭所引用需求义务而必须证明的事实。

acceptanceCriteria:
  - ...

verificationMethods:
  - TEST
  - ANALYSIS
  - REVIEW
  - INSPECTION
  - DEMONSTRATION

testPurposeRefs: []
verificationCaseRefs: []
analysisRefs: []
reviewRefs: []

requiredEvidenceClasses:
  - raw_trace
  - configuration
  - timing
  - review
  - analysis

closureRule:
  allRequiredActivitiesComplete: true
  unresolvedMajorProblemsAllowed: false

reviewRecordRefs: []
```

## 语义

一个需求可映射到多个验证目标；一个目标可需要多种方法或活动；一个验证用例仅在追踪明确时才可支持多个目标；目标不会因用例 `PASS` 而自动满足；满足是记录在目标满足记录中的受评审结论，而非自动聚合。

## 分类说明

本对象是本地 ARINC/Profile 候选。它可能对应 VerificationObligation 角色，但等价性和
Generic 定义权均为 `NOT-DETERMINED`。其面向航空的结构不建立权威批准，也不使该对象
成为 Generic GVS Core 的一部分。

## 非主张

面向认证不等于已获认证；验证目标是项目自定义对象，不是从标准复制的权威强制数据项；满足全部目标不构成航空器级适航。
