# Temporary GVS Instance Mapping

| Field | Value |
|---|---|
| **Register ID** | TMP-MAP-ARINC615A-01 |
| **Version** | 0.1-candidate |
| **Method instance** | `TMP-ARINC615A-01` |
| **MethodDefinitionCommit** | `48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b` |
| **Source proposal** | PR #9 starting head `53a98447bcfa862f082ce443d69115067d3ff2f1` |
| **Compatibility** | NOT-DETERMINED |
| **Review status** | PENDING INDEPENDENT REVIEW |

## 1. Mapping rule

This is an instance-side realization/binding matrix, not a copy of the external
Core or a declaration of equivalence. Direction is always **ARINC object → one
primary relation → Framework candidate/role**. Every row has exactly one
primary relation and one status from `NOT-DETERMINED`, `CANDIDATE`, `PARTIAL`,
`CONFLICT`, or `OUT-OF-SCOPE`. Missing research or identity is
`NOT-DETERMINED`, not `CONFLICT`.

## 2. Candidate mapping population

| Row | External candidate/role locator | Local ARINC object | Primary relation | Status | Rationale | Open dependency | Migration impact | Review |
|---|---|---|---|---|---|---|---|---|
| M01 | `Applicability/Profile Declaration` | PICS-like declaration | `realizes` | `CANDIDATE` | controls capability/applicability and applicable CRS population; is not Verification Basis | ISO/IEC 9646 Task 002 and Profile review | retain declaration separately from basis items | pending |
| M02 | `VerificationBasisElement` | applicable CRS item | `candidate-correspondence` | `CANDIDATE` | an applicable normative item may play a typed basis role; no frozen Core class is asserted | source-locator and typed-role review | preserve locator/applicability provenance | pending |
| M03 | `VerificationObligation` | Verification Objective | `candidate-correspondence` | `NOT-DETERMINED` | local VO may address an obligation role, but equivalence and Generic ownership are unreviewed | method and instance semantic review | keep VO as ARINC/Profile object | pending |
| M04 | `VerificationCase` | Test Purpose | `candidate-correspondence` | `NOT-DETERMINED` | Test Purpose correspondence is not presumed | ISO/IEC 9646 Task 002 | keep TP and VC distinct | pending |
| M05 | `VerificationCase` | Verification Case / procedure | `instantiates` | `CANDIDATE` | Binding/engineering realizes executable case and procedure roles | case/procedure/configuration review | separate reusable procedure from run values | pending |
| M06 | `Oracle` | discrete/timing rule | `implements` | `CANDIDATE` | rule evaluates observations; concrete parameters belong to Binding/Configuration | Oracle interface review | version rule and parameters separately | pending |
| M07 | `Result` | verdict | `instantiates` | `CANDIDATE` | verdict is an evaluated result, not the Oracle | result-state review | preserve rule inputs and result separately | pending |
| M08 | `Observation` | packet trace / timestamp / log | `instantiates` | `CANDIDATE` | captured facts are observations/raw records with provenance | evidence characterization policy | prohibit automatic Evidence admission | pending |
| M09 | `Evidence` | Evidence Manifest / execution record | `candidate-correspondence` | `NOT-DETERMINED` | manifest is a provenance container; evidence role requires explicit characterization | Evidence admission/credibility study | keep raw record, manifest, Result, and Evidence Item distinct | pending |
| M10 | `SufficiencyAssessment` | Objective Satisfaction Record | `candidate-correspondence` | `NOT-DETERMINED` | OSR combines Result, sufficiency reasoning, Decision, and Claim linkage; it is not one Core object | RQ4 and instance semantic review | retain composite nature and reviewed closure | pending |
| M11 | `Claim` | Compliance Evidence Index | `indexes` | `NOT-DETERMINED` | CEI is reviewer-facing navigation; it is not Claim, Argument, or Evidence Architecture | instance migration and independent review | preserve index-only role | pending |
| M12 | `Configuration` | Test Conformity Record | `candidate-correspondence` | `NOT-DETERMINED` | local configuration/provenance/conformity artifact does not establish authority conformity | identity/version and Profile review | link to configuration without authority promotion | pending |
| M13 | `Anomaly/Change/Impact` | Problem/Deviation Closure Record | `candidate-correspondence` | `NOT-DETERMINED` | local composite closure overlaps several lifecycle roles without established equivalence | lifecycle/state/authority review | keep state transitions explicit | pending |
| M14 | `Obligation/Coverage aspect` | L0–L7 ARINC evidence view | `classifies` | `CANDIDATE` | useful ARINC/Profile view; not Generic architecture | Profile review | label every use local candidate | pending |
| M15 | `Assurance/research extension points` | A0–A4 and R0–R5 | `specializes` | `CANDIDATE` | ARINC/Profile assurance and instance research taxonomy; not authority or Core levels | Profile and claim review | prevent Generic/authority promotion | pending |
| M16 | `CompositeGate` | RG0–RG6 / G0–G7 | `specializes` | `CANDIDATE` | project/Profile gate package may specialize review/decision flow; compatibility is unreviewed | CompositeGate compatibility review | retain internal-gate non-claim | pending |
| M17 | `Configuration` | Project Configuration `TMP-PC-ARINC615A-01` | `instantiates` | `CANDIDATE` | a future concrete run configuration may instantiate the role | actual controlled values | status remains NOT YET ESTABLISHED | pending |

No row is compatibility-approved. PR #9-derived rows remain unmerged external
candidates with no active semantic authority until independent migration review
and release. Future row changes require immutable identities, rationale,
dependency, impact, and review.

## 3. Mandatory semantic separations

- applicability declaration is not a basis item;
- basis/requirement is not automatically a Verification Obligation;
- Test Purpose is not automatically a Verification Case;
- Oracle is not verdict/result;
- raw record and manifest are not automatically Evidence Items;
- Evidence characterization is not Argument use;
- objective status, claim support, compliance status, and authority acceptance
  are different states;
- binding compatibility is not empirical instance evaluation.

---

# 中文版

# 临时 GVS 实例映射

| 字段 | 值 |
|---|---|
| **登记册 ID** | TMP-MAP-ARINC615A-01 |
| **版本** | 0.1-candidate |
| **方法实例** | `TMP-ARINC615A-01` |
| **MethodDefinitionCommit** | `48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b` |
| **源提案** | PR #9 起始 head `53a98447bcfa862f082ce443d69115067d3ff2f1` |
| **兼容性** | NOT-DETERMINED |
| **评审状态** | 等待独立评审 |

## 1. 映射规则

本文件是实例侧 realization/binding matrix，不是外部 Core 副本或等价声明。方向始终为
“ARINC 对象 → 唯一 primary relation → Framework candidate/role”。每行恰有一个主关系，
状态只能是 `NOT-DETERMINED`、`CANDIDATE`、`PARTIAL`、`CONFLICT` 或 `OUT-OF-SCOPE`。
缺少研究或身份时使用 `NOT-DETERMINED`，不得误用 `CONFLICT`。

## 2. 候选映射总体

| 行 | 外部候选/角色定位 | 本地 ARINC 对象 | 主关系 | 状态 | 理由 | 开放依赖 | 迁移影响 | 评审 |
|---|---|---|---|---|---|---|---|---|
| M01 | `Applicability/Profile Declaration` | PICS-like declaration | `realizes` | `CANDIDATE` | 控制能力/适用性及适用 CRS 总体；不是 Verification Basis | ISO/IEC 9646 Task 002 与 Profile 评审 | 声明与 basis item 分离 | 待审 |
| M02 | `VerificationBasisElement` | applicable CRS item | `candidate-correspondence` | `CANDIDATE` | 适用规范项可能承担 typed basis role；不声称冻结 Core class | 来源定位与 typed-role 评审 | 保留定位和适用性来源 | 待审 |
| M03 | `VerificationObligation` | Verification Objective | `candidate-correspondence` | `NOT-DETERMINED` | VO 可能承担义务角色，但等价和 Generic 所有权未经评审 | 方法与实例语义评审 | VO 保持 ARINC/Profile 对象 | 待审 |
| M04 | `VerificationCase` | Test Purpose | `candidate-correspondence` | `NOT-DETERMINED` | 不预设 Test Purpose 对应关系 | ISO/IEC 9646 Task 002 | TP 与 VC 分离 | 待审 |
| M05 | `VerificationCase` | Verification Case / procedure | `instantiates` | `CANDIDATE` | Binding/工程实现可执行 case 与 procedure 角色 | case/procedure/configuration 评审 | 可复用规程与运行值分离 | 待审 |
| M06 | `Oracle` | discrete/timing rule | `implements` | `CANDIDATE` | 规则评价观测；具体参数属于 Binding/Configuration | Oracle 接口评审 | 规则与参数分别版本化 | 待审 |
| M07 | `Result` | verdict | `instantiates` | `CANDIDATE` | verdict 是评价结果，不是 Oracle | 结果状态评审 | 规则输入与结果分离 | 待审 |
| M08 | `Observation` | packet trace / timestamp / log | `instantiates` | `CANDIDATE` | 捕获事实是带来源的观测/原始记录 | 证据表征政策 | 禁止自动准入 Evidence | 待审 |
| M09 | `Evidence` | Evidence Manifest / execution record | `candidate-correspondence` | `NOT-DETERMINED` | manifest 是来源容器；Evidence 角色需要显式表征 | 证据准入/可信度研究 | 区分 raw、manifest、Result 与 Evidence Item | 待审 |
| M10 | `SufficiencyAssessment` | Objective Satisfaction Record | `candidate-correspondence` | `NOT-DETERMINED` | OSR 组合 Result、充分性推理、Decision 与 Claim 链接，不是单个 Core 对象 | RQ4 与实例语义评审 | 保留复合属性与受评审关闭 | 待审 |
| M11 | `Claim` | Compliance Evidence Index | `indexes` | `NOT-DETERMINED` | CEI 仅供评审导航，不是 Claim、Argument 或 Evidence Architecture | 实例迁移与独立评审 | 保留仅索引角色 | 待审 |
| M12 | `Configuration` | Test Conformity Record | `candidate-correspondence` | `NOT-DETERMINED` | 本地配置/来源/符合性工件不建立权威符合性 | 身份/版本及 Profile 评审 | 链接配置但不晋级权威 | 待审 |
| M13 | `Anomaly/Change/Impact` | Problem/Deviation Closure Record | `candidate-correspondence` | `NOT-DETERMINED` | 本地复合关闭跨多个生命周期角色，未建立等价 | 生命周期/状态/权威评审 | 显式保留状态转换 | 待审 |
| M14 | `Obligation/Coverage aspect` | L0–L7 ARINC evidence view | `classifies` | `CANDIDATE` | 有用的 ARINC/Profile 视图；不是 Generic 架构 | Profile 评审 | 每次使用标记为本地候选 | 待审 |
| M15 | `Assurance/research extension points` | A0–A4 and R0–R5 | `specializes` | `CANDIDATE` | ARINC/Profile 保证和实例研究 taxonomy；不是权威/Core 层级 | Profile 与主张评审 | 禁止 Generic/权威晋级 | 待审 |
| M16 | `CompositeGate` | RG0–RG6 / G0–G7 | `specializes` | `CANDIDATE` | 项目/Profile 门包可能特化评审/决定流；兼容性未经评审 | CompositeGate 兼容性评审 | 保留内部门非主张 | 待审 |
| M17 | `Configuration` | Project Configuration `TMP-PC-ARINC615A-01` | `instantiates` | `CANDIDATE` | 未来具体运行配置可以实例化该角色 | 实际受控值 | 状态保持 NOT YET ESTABLISHED | 待审 |

没有任何行已通过兼容性评审。PR #9 派生行在独立迁移评审和发布前保持未合并外部候选，
不具有生效语义权威。未来改行必须具备不可变身份、理由、依赖、影响和评审。

## 3. 强制语义分离

- 适用性声明不是 basis item；
- basis/requirement 不自动成为 Verification Obligation；
- Test Purpose 不自动成为 Verification Case；
- Oracle 不是 verdict/result；
- raw record 和 manifest 不自动成为 Evidence Item；
- Evidence 表征不是 Argument 使用；
- objective、claim support、compliance 与 authority acceptance 状态不同；
- binding compatibility 不是经验实例评价。
