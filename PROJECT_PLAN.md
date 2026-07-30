# Integrated Project Plan

| Field | Value |
|---|---|
| **Plan ID** | IPP-2026-001 |
| **Version** | 1.1 |
| **Status** | Active |
| **Baseline** | RB-2026-001-v4.2 |
| **Planning horizon** | Baseline freeze through second-protocol replication |

## 1. Mission

Produce, evaluate, and operationalize a Test-and-Analysis methodology that
supports bounded, reproducible ARINC 615A conformance decisions and generates
credible scientific and engineering evidence.

## 2. Success criteria

The program succeeds when:

1. the applicable CRS and observation boundary are controlled;
2. every applicable verification obligation is traceable to reviewed VCs;
3. every applicable timing obligation has reviewed trigger/response semantics,
   a clock model, boundary partitions, and a measurement-error budget;
4. the instrument produces reproducible, provenance-complete timestamped evidence;
5. held-out discrete and timing faults provide an honest measure of bounded detection adequacy;
6. probabilistic or diagnostic claims are released only after their gates pass;
7. scientific results and engineering releases use the same versioned artifacts;
8. transferability wording matches the presence or absence of replication.

## 3. Workstreams

| Workstream | Owner role | Canonical plan | Primary outputs |
|---|---|---|---|
| W0 Governance | Project/research lead | `docs/BASELINE.md`, `docs/management/` | baseline, decisions, risks, gates |
| W1 Requirements | Requirements researchers | `docs/research/RESEARCH_PLAN.md` | applicability, CRS, obligation model |
| W2 Modeling and VCS | Method/test researchers | research + architecture docs | clock-augmented EFSM, timed traces, TPs, VCs, robust oracles |
| W3 Instrument | Engineering lead | `docs/engineering/IMPLEMENTATION_PLAN.md` | simulator, engine, evidence writer |
| W4 Experiments | Experiment/statistics lead | `docs/research/EXPERIMENT_PLAN.md` | registrations, raw/derived evidence |
| W5 Analysis | Research team | report §§6–8 | discrete/timed coverage, mutation, dependence, calibration, diagnosis |
| W6 Publication | Research lead | `RESEARCH_OUTLINE.md`, `thesis/` | papers, thesis, replication report |
| W7 Tutorial | Technical educator | `tutorial/`, `docs/study/` | reproducible learning/runbooks |

Roles may be held by the same person, but independent review is required where
the baseline specifies it.

## 4. Integrated roadmap

| Stage | Main work | Exit products | Required decisions |
|---|---|---|---|
| P0 Baseline | Freeze method and repository control | RB-2026-001-v4.2, plans, risks | Baseline accepted |
| P1 Scope/CRS | Applicability, observation boundary, dual extraction | CRS, adjudication, source manifest | RG0, RG1, G0 |
| P2 Model/VCS | clock-augmented EFSM, timed traces, obligations, cases, robust oracles | Model/timing package, base VCS | RG2, RG3, G1; T0 |
| P3 Instrument | Runner, roles, clocks, error budget, reset, logging, evidence | Reproducible end-to-end timed run | RG4, G2 readiness |
| P4 T1 execution | Execute controlled VCS | Raw evidence, verdict report | G2; T1 result |
| P5 T2 adequacy | Development and held-out fault study | Mutation and held-out report | RG5, G3; T2 result |
| P6 Optional T3/diagnosis | Calibration, dependence, classifiers | Sensitivity and diagnostic reports | G4–G6 |
| P7 Transfer | Second protocol instance | Replication and comparative analysis | G7 |

Stages are evidence-driven, not calendar-driven. Parallel implementation is
allowed only when it does not pre-empt an unresolved upstream gate.

## 5. Near-term execution backlog

### Baseline release

- review and approve `CR-2026-001` and the v4.2 baseline package;
- merge the baseline PR only after the mathematical, bilingual, and governance
  review gates pass;
- create the recommended baseline tag after merge;
- migrate downstream identifiers and re-evaluate timing claims instead of
  relabeling v4.1 evidence.

### First research increment

- create the applicability-declaration schema;
- create the CRS item schema without proprietary text fields;
- define dual-review extraction instructions and adjudication form;
- register EXP-001;
- conduct RG0 scope review.

### First engineering increment

- add schema validation and example objects;
- preserve the existing 48-test green baseline;
- document current TFTP behavior and gaps against E1;
- add an evidence-manifest schema before new session implementation.
- implement monotonic timestamp capture and an explicit timing-error budget before
  using timing results for conformance verdicts.

## 6. Management cadence

| Cadence | Activity | Output |
|---|---|---|
| Weekly | Workstream review | completed work, blockers, next evidence |
| Per PR | Repository, engineering, methodology, and/or research review | explicit outcome and gate impact |
| Per gate | Independent gate review | signed findings and decision |
| Monthly | Risk and scope review | updated risk register and residual risks |
| Per experiment | Registration then result review | deviations and reproducibility record |
| Per release | Claim/evidence audit | approved wording and manifest |

## 7. Definition of done

A work item is done only when:

- its artifact exists at the controlled path;
- acceptance criteria and relevant tests pass;
- versions and upstream/downstream trace links are recorded;
- review findings are closed or explicitly accepted;
- risks and deviations are updated;
- claim wording remains within the achieved assurance tier.

## 8. Dependencies and constraints

- Access to controlled ARINC 615A material is required for P1–P2.
- Public repository artifacts must not reproduce proprietary clauses.
- T3 depends on representative calibration instances and may legitimately remain
  unavailable.
- External peer or hardware access improves external validity but does not
  replace controlled loopback, oracle, and provenance checks.
- P7 needs a separately selected and resourced second protocol.

---

## 中文版

### 1. 使命

形成、评价并工程化一种测试—分析方法，为 ARINC 615A 提供有边界、可复现的离散与时序符合性决策证据。

### 2. 成功准则

项目成功要求：适用 CRS 和观测边界受控；所有义务可追踪至已评审 VC；每条时序义务具备触发/响应语义、时钟模型、边界分区和误差预算；工具产生来源完整的带时戳证据；留出离散/时序故障诚实评价有限检测能力；概率、诊断和可迁移性措辞只能由相应门禁晋级。

### 3. 工作流与路线

- W0 治理：基线、变更、风险和门禁；
- W1 需求：适用性、CRS 和义务模型；
- W2 模型/VCS：带时钟 EFSM、时戳迹、TP、VC 和稳健 oracle；
- W3 工具：运行器、时钟、误差预算、证据写入；
- W4 实验：注册、原始/派生证据；
- W5 分析：离散/时序覆盖、变异、依赖、校准和诊断；
- W6/W7：论文、复现和教程。

路线依次经过 P0 基线、P1 范围/CRS、P2 带时钟模型/VCS、P3 仪器、P4 T1 执行、P5 T2 充分性、P6 可选 T3/诊断和 P7 第二协议复现。阶段由证据而非日历驱动，未解决的上游门禁不得被并行实现绕过。

### 4. 完成定义

工作项只有在受控路径存在产物、测试通过、版本与追踪完整、评审发现关闭或被显式接受、风险/偏差更新且主张不超过已获得层级时才算完成。时序结果还必须保存单调时钟、时间戳位置、分辨率、误差预算和边界判定依据。
