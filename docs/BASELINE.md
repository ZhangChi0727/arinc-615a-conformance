# Repository Research Baseline

| Field | Value |
|---|---|
| **Baseline ID** | RB-2026-001-v4.2 |
| **Proposed effective date** | 2026-07-30 |
| **Status** | In Review — becomes the frozen methodology baseline after approval and merge |
| **Authoritative bilingual report** | [`study/RR-2026-001_test_analysis_conformance_methodology.md`](study/RR-2026-001_test_analysis_conformance_methodology.md) |

## Meaning of “frozen”

The baseline is sufficiently precise to govern requirement extraction, model construction, verification-case design, tool implementation, experiments, evidence interpretation, and claim release.

The following are frozen unless changed through the process in
[`management/CHANGE_CONTROL.md`](management/CHANGE_CONTROL.md):

- the complementary Test-and-Analysis architecture;
- the ARINC 615A instance scope and explicit non-claims;
- the separation of protocol, traceability, evidence, and inference objects;
- the separation of logical sequence, deterministic real-time conformance,
  run-order dependence, and latent temporal dynamics;
- the clock-augmented EFSM, timestamped-trace, robust timing-oracle, and
  measurement-uncertainty semantics;
- the T0–T3 assurance tiers;
- the formal traceability, finite-fault-domain, repeatability, and calibrated-inference semantics;
- the RG0–RG6 Review/Inspection gates and G0–G7 evidence gates;
- the rule that empirical results may strengthen only the claims supported by passed gates.

## What remains open

Freezing the methodology does not assert that the empirical research is complete. The following must be produced and reviewed:

- controlled ARINC 615A applicability declaration and CRS;
- clock-augmented observable EFSM and trace relations;
- controlled timing-obligation catalog, clock/error budget, and timed model;
- executable base VCS and independently reviewed oracles;
- development and held-out fault sets;
- execution, coverage, mutation, and diagnostic datasets;
- calibration data for any T3 posterior;
- second-protocol replication before any protocol-independence claim.

Changes to these empirical artifacts normally advance the project without changing the baseline. A baseline revision is required only when they expose an error or necessary semantic change in the frozen method.

## Authority order

When repository documents disagree, apply this order:

1. controlled external standard and approved applicability declaration;
2. this baseline declaration;
3. the authoritative English section of RR-2026-001 v4.2;
4. approved design decisions and gate records;
5. research and engineering plans;
6. implementation notes, tutorials, proposals, and historical reviews.

Historical documents remain evidence of project evolution; they are not normative when superseded by this baseline.

## Baseline manifest

| Control item | Canonical location |
|---|---|
| Methodology | `docs/study/RR-2026-001_test_analysis_conformance_methodology.md` |
| Terminology | `docs/terminology.md` |
| Program plan | `PROJECT_PLAN.md` |
| Research plan | `docs/research/RESEARCH_PLAN.md` |
| Experiment plan | `docs/research/EXPERIMENT_PLAN.md` |
| Claim/evidence control | `docs/research/CLAIM_EVIDENCE_MATRIX.md` |
| Engineering implementation | `docs/engineering/IMPLEMENTATION_PLAN.md` |
| Research architecture | `docs/architecture.md` |
| Review gates | `docs/review/REVIEW_GUIDELINE.md` |
| Decisions | `docs/review/DESIGN_DECISIONS.md` |
| Change control | `docs/management/CHANGE_CONTROL.md` |
| Risks | `docs/management/RISK_REGISTER.md` |

## Baseline acceptance checks

- [x] English and Chinese versions are co-located and structurally synchronized.
- [x] Equations (1)–(14), timed equations (T1)–(T5), numerical examples, and boundary conditions were checked.
- [x] Timing constraints use robust interval verdicts with explicit error budgets.
- [x] Test, Analysis, Review, Inspection, and Demonstration roles are separated.
- [x] Scope and non-claims are centralized.
- [x] Repository plans no longer rely on unrestricted proof language.
- [x] Current unit-test suite passes before research implementation begins.
- [ ] v4.2 baseline files committed, tagged, and linked from the active GitHub PR.

---

## 中文版

| 字段 | 内容 |
|---|---|
| **基线 ID** | RB-2026-001-v4.2 |
| **拟生效日期** | 2026-07-30 |
| **状态** | 评审中——批准并合并后成为冻结方法论基线 |
| **权威双语报告** | [`study/RR-2026-001_test_analysis_conformance_methodology.md`](study/RR-2026-001_test_analysis_conformance_methodology.md) |

### “冻结”的含义

本基线足以约束需求提取、带时钟协议模型、验证用例、工具实现、实验、证据解释和主张发布。除非通过
[`management/CHANGE_CONTROL.md`](management/CHANGE_CONTROL.md)
完成正式变更，否则以下内容保持冻结：

- 互补的测试—分析架构和明确的范围/非主张；
- 协议、追踪、证据与推断对象之间的分离；
- 逻辑序列、确定性实时时间符合性、运行顺序依赖和隐含时序动力学之间的分离；
- 带时钟 EFSM、带时戳迹、稳健时序 oracle 和测量不确定性语义；
- T0–T3 层级、RG0–RG6 评审门和 G0–G7 证据门；
- 经验结果只能强化已通过门禁所支持的主张。

### 尚待完成

冻结方法不等于研究已经完成。仍需建立并评审适用性声明、CRS、带时钟 EFSM、时序义务目录、基础 VCS、稳健 oracle、时钟与误差预算、开发/留出故障集、执行和分析数据，以及第二协议复现实验。经验产物若暴露方法错误或必要语义变化，必须发布新的基线版本。

### 权威顺序

文档冲突时依次采用：受控外部标准与适用性声明、本基线声明、RR-2026-001 v4.2 英文部分、已批准设计决策和门禁记录、研究/工程计划、实现说明和历史材料。中文部分用于同步理解；解释不一致时以英文部分为准。
