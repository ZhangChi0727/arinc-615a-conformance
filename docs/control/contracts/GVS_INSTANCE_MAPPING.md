# Temporary GVS Instance Reconciliation Mapping

| Field | Value |
|---|---|
| **Register ID** | TMP-MAP-ARINC615A-01 |
| **Version** | 0.3-candidate |
| **Method instance** | `TMP-ARINC615A-01` |
| **MethodDefinitionCommit** | `48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b` |
| **MethodCompatibilityDispositionCommit** | `c02330d21fe2d3e89e7e2d6352872d52461a6dda` |
| **Method mapping register** | `arinc_615a_object_mapping_register.md`, version 0.2, 18 controlled source rows |
| **Source proposal** | PR #9 starting head `53a98447bcfa862f082ce443d69115067d3ff2f1` |
| **Compatibility** | REVIEWED-COMPATIBLE-WITH-QUALIFICATION — Q-01–Q-09 |
| **Instance evaluation** | NOT-EXERCISED |
| **Project Configuration** | NOT YET ESTABLISHED |
| **Review status** | METHOD DISPOSITION ACKNOWLEDGED — LOCAL INDEPENDENT REVIEW PENDING |

## 1. Reconciliation rule

This is an instance-side reconciliation matrix, not a Core copy, equivalence
claim, or compatibility result. The first table contains exactly one disposition
for each of the external method register's 18 controlled rows, in the same
order. Active v4.2.1 objects and PR #9 candidates retain distinct source
identities. Direction is always **ARINC object → one primary relation → external
candidate/role**. Relations and statuses reproduce the method-side row without
strengthening it.

Allowed statuses are `NOT-DETERMINED`, `CANDIDATE`, `PARTIAL`, `CONFLICT`, and
`OUT-OF-SCOPE`. Missing identity or research is `NOT-DETERMINED`, not
`CONFLICT`. Additional local taxonomies appear only in the separate
**instance-only additional rows** table and cannot hide a missing source row.

## 1.1 Third-handshake disposition acknowledgement

MethodCompatibilityDispositionCommit
`c02330d21fe2d3e89e7e2d6352872d52461a6dda` confirmed all 18 method rows and
all 7 instance-only rows without changing a primary relation or row status.
Source labels containing “PR #9 / v4.3 candidate” remain historical provenance,
not current merge-state assertions. Q-01–Q-09 remain mandatory; in particular,
`NOT-DETERMINED` and `PARTIAL` rows stay open, evaluation stays
`NOT-EXERCISED`, and configuration stays `NOT YET ESTABLISHED`.
## 2. Method-side 18-row reconciliation

| Source row | External candidate/role locator | Local ARINC object | Source baseline | Primary relation | Status | Rationale | Open dependency | Migration impact | Review |
|---|---|---|---|---|---|---|---|---|---|
| R01 | `Applicability/Profile Declaration` | PICS-like declaration | active v4.2.1 | `realizes` | `CANDIDATE` | controls capability/applicability and applicable CRS population; is not Verification Basis | ISO/IEC 9646 Task 002; Profile review | retain declaration separately from basis items | pending |
| R02 | `VerificationBasisElement` | applicable CRS item | active v4.2.1 | `candidate-correspondence` | `CANDIDATE` | an applicable normative item may play a typed basis role; no frozen Core class is asserted | Task 002 and mapping review | preserve CRS locator and applicability provenance | pending |
| R03 | `VerificationObligation` | current ARINC requirement-obligation aspect | active v4.2.1 | `no-direct-correspondence` | `NOT-DETERMINED` | legacy structure exposes no controlled identity whose semantics can be compared | obligation identity/semantics review | do not retrofit a stable ID into the frozen legacy baseline | pending |
| R04 | `VerificationObligation` | PR #9 Verification Objective | PR #9 / v4.3 candidate | `candidate-correspondence` | `NOT-DETERMINED` | VO may address the missing intermediary, but semantics remain unmerged and unreviewed | instance migration/compatibility review | UNMERGED EXTERNAL CANDIDATE — NO ACTIVE SEMANTIC AUTHORITY | pending |
| R05 | `Obligation/Coverage aspect` | functional/state/timing and related classifications | active v4.2.1 | `classifies` | `CANDIDATE` | local classifications may qualify obligation/coverage views without becoming a universal Core level | Task 002 and coverage study | keep T0–T3/Profile taxonomy out of Generic promotion | pending |
| R06 | `VerificationStrategy` | Test-and-Analysis allocation | active v4.2.1 | `realizes` | `PARTIAL` | allocation covers only a bounded strategy-decision subset | strategy criteria and rationale review | retain omitted environment/coverage/evidence decisions | pending |
| R07 | `VerificationCase` | VC | active v4.2.1 | `instantiates` | `CANDIDATE` | VC is a candidate case realization; Test Purpose equivalence is not presumed | Task 002 Test Purpose study | map Test Purpose only after locator-backed study | pending |
| R08 | `VerificationProcedure` | procedure | active v4.2.1 | `instantiates` | `CANDIDATE` | executable steps may instantiate the procedure role | procedure/configuration review | separate reusable procedure from run configuration | pending |
| R09 | `Observation` | packet trace/timestamp/log | active v4.2.1 | `instantiates` | `CANDIDATE` | captured facts are observations/raw records with provenance | evidence characterization rules | do not auto-promote trace/log to Evidence | pending |
| R10 | `Result` | verdict | active v4.2.1 | `instantiates` | `CANDIDATE` | verdict is an evaluated Result, not Observation or the Oracle rule | Oracle/Result review | preserve Observation, rule, and Result separately | pending |
| R11 | `Oracle` | discrete/robust timing rule | active v4.2.1 | `implements` | `CANDIDATE` | rule evaluates controlled Observations against expected constraints and produces a Result | ISO-G04 and Task 002 | version rule and parameters in Binding/Configuration | pending |
| R12 | `Evidence` | characterized execution/analysis record | active v4.2.1 | `candidate-correspondence` | `NOT-DETERMINED` | raw records require identity, provenance, applicability, credibility, and admission characterization before Evidence role | Evidence admission/credibility study | manifests remain provenance containers, not automatic Evidence Items | pending |
| R13 | `Argument` | scoped assurance reasoning | active v4.2.1 | `realizes` | `PARTIAL` | some reasoning may support a scope; full Argument equivalence is not shown | Claim/Argument boundary review | retain explicit inference and limitations | pending |
| R14 | `Claim` | PR #9 CEI claim entry candidate | PR #9 / v4.3 candidate | `indexes` | `NOT-DETERMINED` | CEI navigates to a versioned Claim/Decision; it is not Claim, Argument, or Evidence Architecture | instance migration and independent review | UNMERGED EXTERNAL CANDIDATE — NO ACTIVE SEMANTIC AUTHORITY | pending |
| R15 | `CompositeGate` | RG/G gate package | PR #9 / v4.3 candidate | `specializes` | `NOT-DETERMINED` | decomposition and compatibility with CompositeGate are unreviewed | CompositeGate compatibility review | UNMERGED EXTERNAL CANDIDATE — NO ACTIVE SEMANTIC AUTHORITY | pending |
| R16 | `Configuration` | IUT/setup/procedure identity | active v4.2.1 | `instantiates` | `CANDIDATE` | the active identity bundle may instantiate the candidate Configuration role | identity/version contract | keep legacy identity distinct from future Project Configuration | pending |
| R17 | `Anomaly/Change/Impact` | Problem Closure plus CR/DD | active v4.2.1 | `candidate-correspondence` | `NOT-DETERMINED` | overlap may exist, but lifecycle/state/authority equivalence is unknown | change/closure review | preserve legacy states and map transitions explicitly | pending |
| R18 | `SufficiencyAssessment` | PR #9 OSR/claim-review candidate | PR #9 / v4.3 candidate | `candidate-correspondence` | `NOT-DETERMINED` | OSR may contribute to sufficiency reasoning but is not assumed equivalent to one Core object | RQ4 semantics and instance review | UNMERGED EXTERNAL CANDIDATE — NO ACTIVE SEMANTIC AUTHORITY | pending |

Coverage of the external controlled population is **18/18**. No local row is
reused to conceal two external roles: `VerificationCase` and
`VerificationProcedure` have independent identities and dispositions.

## 3. Instance-only additional rows

These rows describe local v4.3 artifacts that are not separate rows in the
method-side register. `Row class = INSTANCE-ONLY-ADDITIONAL` is mandatory. A
real external role is named only as a review target; `no-direct-correspondence /
NOT-DETERMINED` means no correspondence is asserted.

| Local row | Row class | External review-target locator | Local ARINC object | Source baseline | Primary relation | Status | Rationale | Open dependency | Migration impact | Review |
|---|---|---|---|---|---|---|---|---|---|---|
| A01 | `INSTANCE-ONLY-ADDITIONAL` | `VerificationCase` | Test Purpose | PR #9 / v4.3 candidate | `no-direct-correspondence` | `NOT-DETERMINED` | Test Purpose is not preassigned to VerificationCase | ISO/IEC 9646 Task 002 | retain TP and VC separately | pending |
| A02 | `INSTANCE-ONLY-ADDITIONAL` | `Evidence` | Execution Evidence Manifest | PR #9 / v4.3 candidate | `no-direct-correspondence` | `NOT-DETERMINED` | manifest is a provenance container, not an admitted Evidence Item | Evidence characterization policy | add characterized Evidence refs outside manifest identity | pending |
| A03 | `INSTANCE-ONLY-ADDITIONAL` | `Configuration` | Test Conformity Record | PR #9 / v4.3 candidate | `no-direct-correspondence` | `NOT-DETERMINED` | local conformity/provenance record is not authority conformity or a Core Configuration | identity/Configuration review | retain as Profile/Binding control | pending |
| A04 | `INSTANCE-ONLY-ADDITIONAL` | `Argument` | L0–L7 ARINC evidence view | PR #9 / v4.3 candidate | `no-direct-correspondence` | `NOT-DETERMINED` | view spans basis, objective, execution, evidence, satisfaction, and argument; no single Core role corresponds | Profile architecture review | label strictly instance/Profile view | pending |
| A05 | `INSTANCE-ONLY-ADDITIONAL` | `SufficiencyAssessment` | A0–A4 ARINC assurance states | PR #9 / v4.3 candidate | `no-direct-correspondence` | `NOT-DETERMINED` | local assurance taxonomy is not a Generic extension point or authority level | Profile/claim review | prohibit Generic/authority promotion | pending |
| A06 | `INSTANCE-ONLY-ADDITIONAL` | `SufficiencyAssessment` | R0–R5 instance research maturity | PR #9 / v4.3 candidate | `no-direct-correspondence` | `NOT-DETERMINED` | research maturity is local and does not determine assurance or certification state | research/claim review | keep research and assurance states orthogonal | pending |
| A07 | `INSTANCE-ONLY-ADDITIONAL` | `Configuration` | future Project Configuration `TMP-PC-ARINC615A-01` | PR #9 / v4.3 candidate | `no-direct-correspondence` | `NOT-DETERMINED` | no controlled values exist, so no Configuration instance is established | actual controlled values | status remains NOT YET ESTABLISHED; prohibit execution/evaluation | pending |

## 4. Mandatory semantic chain

```text
Observation/raw record
  → Oracle evaluation
  → Result/verdict
  → identity/provenance/applicability/credibility/admission characterization
  → Evidence Item
  → Argument / SufficiencyAssessment
  → reviewed Decision / versioned Claim
```

Applicability declaration is not a basis item; basis/requirement is not
automatically a Verification Obligation; Test Purpose is not automatically a
VerificationCase; manifest or PASS is not automatically Evidence or Objective
Satisfaction; CEI indexes but does not decide; compatibility is not empirical
instance evaluation. L0–L7, A0–A4, and R0–R5 are not Generic GVS Core levels.

---

# 中文版

# 临时 GVS 实例闭合映射

| 字段 | 值 |
|---|---|
| **登记册 ID** | TMP-MAP-ARINC615A-01 |
| **版本** | 0.3-candidate |
| **方法实例** | `TMP-ARINC615A-01` |
| **MethodDefinitionCommit** | `48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b` |
| **MethodCompatibilityDispositionCommit** | `c02330d21fe2d3e89e7e2d6352872d52461a6dda` |
| **方法映射登记册** | `arinc_615a_object_mapping_register.md`，版本 0.2，18 个受控源行 |
| **源提案** | PR #9 起始 head `53a98447bcfa862f082ce443d69115067d3ff2f1` |
| **兼容性** | REVIEWED-COMPATIBLE-WITH-QUALIFICATION——受 Q-01–Q-09 限定 |
| **实例评价** | NOT-EXERCISED |
| **Project Configuration** | NOT YET ESTABLISHED |
| **评审状态** | 已确认方法处置——等待本地独立评审 |

## 1. 闭合规则

本文件是实例侧 reconciliation matrix，不是 Core 副本、等价主张或兼容性结果。第一张表按
相同顺序对外部方法登记册 18 个受控行逐一且唯一处置。active v4.2.1 对象与 PR #9 候选保留
不同来源身份。方向始终为“ARINC 对象 → 唯一主关系 → 外部候选/角色”，关系与状态复现方法侧
行，不得静默加强。允许状态为 `NOT-DETERMINED`、`CANDIDATE`、`PARTIAL`、`CONFLICT` 和
`OUT-OF-SCOPE`。其它本地 taxonomy 只进入独立附加表，不能掩盖源行遗漏。

## 1.1 第三次握手处置确认

MethodCompatibilityDispositionCommit
`c02330d21fe2d3e89e7e2d6352872d52461a6dda` 在不改变任何主关系或行状态的前提下确认
18 个方法行及 7 个仅实例行。包含“PR #9 / v4.3 candidate”的来源标签是历史来源记录，不是
当前合并状态主张。Q-01–Q-09 仍为强制限定；尤其是 `NOT-DETERMINED` 和 `PARTIAL` 行保持
开放、评价保持 `NOT-EXERCISED`、配置保持 `NOT YET ESTABLISHED`。
## 2. 方法侧 18 行闭合

| 源行 | 外部候选/角色定位 | 本地 ARINC 对象 | 来源基线 | 主关系 | 状态 | 理由 | 开放依赖 | 迁移影响 | 评审 |
|---|---|---|---|---|---|---|---|---|---|
| R01 | `Applicability/Profile Declaration` | PICS-like declaration | active v4.2.1 | `realizes` | `CANDIDATE` | 控制适用性与 CRS 总体；不是 Verification Basis | Task 002；Profile 评审 | 声明与 basis item 分离 | 待审 |
| R02 | `VerificationBasisElement` | applicable CRS item | active v4.2.1 | `candidate-correspondence` | `CANDIDATE` | 可能承担 typed basis role；不声称冻结 Core class | Task 002 与映射评审 | 保留定位与适用性来源 | 待审 |
| R03 | `VerificationObligation` | current ARINC requirement-obligation aspect | active v4.2.1 | `no-direct-correspondence` | `NOT-DETERMINED` | legacy 结构没有可比较语义的受控身份 | 义务身份/语义评审 | 不向冻结基线补造 ID | 待审 |
| R04 | `VerificationObligation` | PR #9 Verification Objective | PR #9 / v4.3 candidate | `candidate-correspondence` | `NOT-DETERMINED` | VO 可能承担中介角色，但语义未评审 | 实例迁移/兼容性评审 | 未合并候选——无生效权威 | 待审 |
| R05 | `Obligation/Coverage aspect` | functional/state/timing and related classifications | active v4.2.1 | `classifies` | `CANDIDATE` | 本地分类可限定 obligation/coverage，不成为通用 Core 层级 | Task 002 与 coverage 研究 | 禁止 taxonomy 晋级 Generic | 待审 |
| R06 | `VerificationStrategy` | Test-and-Analysis allocation | active v4.2.1 | `realizes` | `PARTIAL` | 只覆盖有界策略决定子集 | 策略准则评审 | 保留未覆盖决定 | 待审 |
| R07 | `VerificationCase` | VC | active v4.2.1 | `instantiates` | `CANDIDATE` | VC 是候选 case；不预设 TP 等价 | Task 002 | TP 需独立研究 | 待审 |
| R08 | `VerificationProcedure` | procedure | active v4.2.1 | `instantiates` | `CANDIDATE` | 可执行步骤可能实例化 procedure | procedure/configuration 评审 | procedure 与运行配置分离 | 待审 |
| R09 | `Observation` | packet trace/timestamp/log | active v4.2.1 | `instantiates` | `CANDIDATE` | 捕获事实是 Observation/raw record | Evidence 表征规则 | 禁止自动晋级 Evidence | 待审 |
| R10 | `Result` | verdict | active v4.2.1 | `instantiates` | `CANDIDATE` | verdict 是 Result，不是 Observation 或 Oracle | Oracle/Result 评审 | 三者分离 | 待审 |
| R11 | `Oracle` | discrete/robust timing rule | active v4.2.1 | `implements` | `CANDIDATE` | 评价 Observation 并产生 Result | ISO-G04 与 Task 002 | 版本化规则/参数 | 待审 |
| R12 | `Evidence` | characterized execution/analysis record | active v4.2.1 | `candidate-correspondence` | `NOT-DETERMINED` | raw 承担 Evidence 前需身份、来源、适用性、可信度与准入表征 | Evidence 准入研究 | manifest 不自动成为 Evidence Item | 待审 |
| R13 | `Argument` | scoped assurance reasoning | active v4.2.1 | `realizes` | `PARTIAL` | 部分推理可能支持限定范围；未证明完整等价 | Claim/Argument 评审 | 保留推断与限制 | 待审 |
| R14 | `Claim` | PR #9 CEI claim entry candidate | PR #9 / v4.3 candidate | `indexes` | `NOT-DETERMINED` | CEI 导航到版本化 Claim/Decision，不是 Claim/Argument/Architecture | 实例迁移评审 | 未合并候选——无生效权威 | 待审 |
| R15 | `CompositeGate` | RG/G gate package | PR #9 / v4.3 candidate | `specializes` | `NOT-DETERMINED` | 分解与兼容性未经评审 | CompositeGate 评审 | 未合并候选——无生效权威 | 待审 |
| R16 | `Configuration` | IUT/setup/procedure identity | active v4.2.1 | `instantiates` | `CANDIDATE` | active 身份组合可能实例化 Configuration | 身份/版本契约 | 与未来配置分离 | 待审 |
| R17 | `Anomaly/Change/Impact` | Problem Closure plus CR/DD | active v4.2.1 | `candidate-correspondence` | `NOT-DETERMINED` | 生命周期/状态/权威等价未知 | 变更/关闭评审 | 保留 legacy 状态 | 待审 |
| R18 | `SufficiencyAssessment` | PR #9 OSR/claim-review candidate | PR #9 / v4.3 candidate | `candidate-correspondence` | `NOT-DETERMINED` | OSR 可能参与充分性推理，不预设单一 Core 等价 | RQ4 与实例评审 | 未合并候选——无生效权威 | 待审 |

外部受控总体覆盖为 **18/18**。`VerificationCase` 与 `VerificationProcedure` 有独立身份和处置。

## 3. 仅实例附加行

下列本地产物在方法侧登记册中没有独立源行，必须标记 `INSTANCE-ONLY-ADDITIONAL`；真实外部
角色只作为评审目标，`no-direct-correspondence / NOT-DETERMINED` 表示不声称对应。

| 本地行 | 行类别 | 外部评审目标定位 | 本地 ARINC 对象 | 来源基线 | 主关系 | 状态 | 理由 | 开放依赖 | 迁移影响 | 评审 |
|---|---|---|---|---|---|---|---|---|---|---|
| A01 | `INSTANCE-ONLY-ADDITIONAL` | `VerificationCase` | Test Purpose | PR #9 / v4.3 candidate | `no-direct-correspondence` | `NOT-DETERMINED` | TP 不预设为 VerificationCase | Task 002 | TP/VC 分离 | 待审 |
| A02 | `INSTANCE-ONLY-ADDITIONAL` | `Evidence` | Execution Evidence Manifest | PR #9 / v4.3 candidate | `no-direct-correspondence` | `NOT-DETERMINED` | manifest 是来源容器，不是准入 Evidence Item | Evidence 表征政策 | 另行引用 characterized Evidence | 待审 |
| A03 | `INSTANCE-ONLY-ADDITIONAL` | `Configuration` | Test Conformity Record | PR #9 / v4.3 candidate | `no-direct-correspondence` | `NOT-DETERMINED` | 本地记录不是权威符合性或 Core Configuration | Configuration 评审 | 保持 Profile/Binding 控制 | 待审 |
| A04 | `INSTANCE-ONLY-ADDITIONAL` | `Argument` | L0–L7 ARINC evidence view | PR #9 / v4.3 candidate | `no-direct-correspondence` | `NOT-DETERMINED` | 跨多个角色，无单一 Core 对应 | Profile 架构评审 | 严格标为实例/Profile 视图 | 待审 |
| A05 | `INSTANCE-ONLY-ADDITIONAL` | `SufficiencyAssessment` | A0–A4 ARINC assurance states | PR #9 / v4.3 candidate | `no-direct-correspondence` | `NOT-DETERMINED` | 本地 taxonomy 不是 Generic extension point/权威层级 | Profile/claim 评审 | 禁止晋级 | 待审 |
| A06 | `INSTANCE-ONLY-ADDITIONAL` | `SufficiencyAssessment` | R0–R5 instance research maturity | PR #9 / v4.3 candidate | `no-direct-correspondence` | `NOT-DETERMINED` | 本地研究状态不决定保证/认证 | research/claim 评审 | 与保证状态正交 | 待审 |
| A07 | `INSTANCE-ONLY-ADDITIONAL` | `Configuration` | future Project Configuration `TMP-PC-ARINC615A-01` | PR #9 / v4.3 candidate | `no-direct-correspondence` | `NOT-DETERMINED` | 无受控值，未建立 Configuration 实例 | 实际受控值 | 保持 NOT YET ESTABLISHED；禁止评价 | 待审 |

## 4. 强制语义链

```text
Observation/raw record
  → Oracle evaluation
  → Result/verdict
  → identity/provenance/applicability/credibility/admission characterization
  → Evidence Item
  → Argument / SufficiencyAssessment
  → reviewed Decision / versioned Claim
```

适用性声明不是 basis item；basis/requirement 不自动成为 VerificationObligation；Test Purpose
不自动成为 VerificationCase；manifest 或 PASS 不自动成为 Evidence 或 Objective Satisfaction；
CEI 只索引、不裁决；compatibility 不是经验实例评价。
L0–L7、A0–A4 和 R0–R5 不是 Generic GVS Core 层级。
