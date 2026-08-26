# Compliance Evidence Index Contract

| Field | Value |
|---|---|
| **Version** | 1.0 |
| **Baseline** | RB-2026-001-v4.3 |
| **Classification** | ARINC/Profile candidate — certification-oriented |
| **Generic correspondence** | Claim: NOT-DETERMINED; primary relation `indexes` |
| **Authority acceptance** | NOT ESTABLISHED |
| **Role** | first reviewer-facing evidence index |

The Compliance Evidence Index (CEI) is the first local reviewer-facing evidence
index. It lets a reviewer navigate from a compliance claim down to
objectives, activities, executions, evidence, problems, and conclusions. The
Execution Evidence Manifest is not the top-level compliance artifact.

The CEI only indexes these records. CEI completeness does not make it a Claim,
Argument, Evidence Item, or Evidence Architecture, and does not establish claim
truth, sufficiency, compliance, or authority acceptance.

## Evidence hierarchy

```text
Compliance Evidence Index (navigation only)
    → versioned Claim + status Decision + Argument
    → Objective Satisfaction + SufficiencyAssessment
    → characterized Evidence Items + Results
    → Observation / Raw Records + provenance manifests
```

## Conceptual schema

```yaml
complianceEvidenceIndexId: CEI-...
baselineId: RB-2026-001-v4.3
applicabilityId: ...
requirementSetId: ...
crsVersion: ...

claimEntries:
  - claimRef: CLM-...
    claimVersion: ...
    argumentRef: ARG-...
    statusDecisionRef: DEC-...
    asOfVersion: ...
    requirementRefs: []
    objectiveRefs: []
    objectiveSatisfactionRefs: []
    sufficiencyAssessmentRefs: []
    evidenceItemRefs: []
    resultRefs: []
    provenanceManifestRefs: []
    deviationRefs: []
    problemRefs: []
    statusSnapshot:
      - SUPPORTED
      - NOT_SUPPORTED
      - OPEN
      - NOT_ASSESSED
    limitations: []
```

## Rules

- the authoritative Claim and status Decision live outside the CEI; the index
  copies a status snapshot only from `statusDecisionRef` and never decides it;
- every snapshot carries `claimRef`, `claimVersion`, `statusDecisionRef`, and
  `asOfVersion`, plus the referenced Argument/OSR/Evidence chain;
- `NOT_ASSESSED` is a valid state and must not be hidden;
- the index references stable artifact IDs and versions, never informal "latest";
- limitations and non-claims accompany every released claim.

## Non-claims

Protocol conformance does not establish aircraft-level airworthiness
compliance. ARINC 615A conformance is only one possible element of a
higher-level system or compliance argument. A finite test suite does not prove
all possible implementation behavior.

---

# 中文版

| 字段 | 内容 |
|---|---|
| **版本** | 1.0 |
| **基线** | RB-2026-001-v4.3 |
| **分类** | ARINC/Profile 候选——面向认证 |
| **Generic 对应** | Claim：NOT-DETERMINED；主关系 `indexes` |
| **权威接受** | 尚未建立 |
| **角色** | 首份面向审查的证据索引 |

合规证据索引（CEI）是首份本地面向评审的证据索引。它让评审者从合规主张向下导航至
目标、活动、执行、证据、问题与结论；执行证据清单不是顶层合规产物。

CEI 只索引这些记录。CEI 完整不使其成为 Claim、Argument、Evidence Item 或 Evidence
Architecture，也不建立主张真实性、充分性、合规性或权威接受。

## 证据层次

```text
合规证据索引（只导航）
    → 版本化 Claim + 状态 Decision + Argument
    → Objective Satisfaction + SufficiencyAssessment
    → 经表征 Evidence Item + Result
    → Observation / Raw Record + 来源 manifest
```

## 概念 schema

```yaml
complianceEvidenceIndexId: CEI-...
baselineId: RB-2026-001-v4.3
applicabilityId: ...
requirementSetId: ...
crsVersion: ...

claimEntries:
  - claimRef: CLM-...
    claimVersion: ...
    argumentRef: ARG-...
    statusDecisionRef: DEC-...
    asOfVersion: ...
    requirementRefs: []
    objectiveRefs: []
    objectiveSatisfactionRefs: []
    sufficiencyAssessmentRefs: []
    evidenceItemRefs: []
    resultRefs: []
    provenanceManifestRefs: []
    deviationRefs: []
    problemRefs: []
    statusSnapshot:
      - SUPPORTED
      - NOT_SUPPORTED
      - OPEN
      - NOT_ASSESSED
    limitations: []
```

## 规则

权威 Claim 与状态 Decision 位于 CEI 之外；索引只从 `statusDecisionRef` 复制状态快照，不在
CEI 内裁决。每个快照必须带 `claimRef`、`claimVersion`、`statusDecisionRef`、`asOfVersion`
以及所引用的 Argument/OSR/Evidence 链；`NOT_ASSESSED` 是有效状态且不得隐藏；索引只引用
稳定 ID/版本，不引用“最新”；每个已发布主张都附有限制与非主张。

## 非主张

协议符合性不确立航空器级适航合规。ARINC 615A 符合性只是更高层系统或合规论证的一个可能要素。有限测试套件不足以证明全部实现行为。
