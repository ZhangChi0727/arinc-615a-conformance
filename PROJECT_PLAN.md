# Integrated Project Plan

| Field | Value |
|---|---|
| **Plan ID** | IPP-2026-001 |
| **Version** | 1.2 |
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
7. scientific results, engineering releases, publications, and tutorials cite
   their upstream artifact IDs and applicable gate records;
8. cross-workstream dependencies use the controlled contracts in `TRACKS.md`
   rather than implementation internals or implicit “latest” state;
9. transferability wording matches the presence or absence of replication.

## 3. Workstreams

| Workstream | Owner role | Canonical plan | Primary outputs |
|---|---|---|---|
| W0 Governance | Project/research lead | `docs/BASELINE.md`, `docs/management/` | baseline, decisions, risks, gates |
| W1 Requirements | Requirements researchers | `docs/requirements/`, `docs/research/RESEARCH_PLAN.md` | applicability, CRS, obligation model |
| W2 Methodology and modeling | Method researchers | `docs/methodology/`, `docs/research/`, `docs/architecture.md` | formal semantics, clock-augmented EFSM, trace relations, TPs, VCs, robust oracles |
| W3 Instrument | Engineering lead | `docs/engineering/IMPLEMENTATION_PLAN.md` | simulator, engine, evidence writer |
| W4 Experiments | Experiment/statistics lead | `docs/research/EXPERIMENT_PLAN.md` | registrations, raw/derived evidence |
| W5 Analysis | Research team | report §§6–8 | discrete/timed coverage, mutation, dependence, calibration, diagnosis |
| W6 Publication | Research lead | `RESEARCH_OUTLINE.md`, `thesis/` | papers, thesis, replication report tied to reviewed claims |
| W7 Tutorial | Technical educator | `tutorial/common/`, `tutorial/arinc615a/` | version-pinned teaching, exercises, and runbooks |

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
- Workstreams may share identifiers and evidence only through the contracts in
  `TRACKS.md`; research and tutorials must not import mutable implementation
  internals, and engineering must not promote scientific claims.

---

# 中文版

## 1. 使命

形成、评价并工程化一种测试—分析方法，为 ARINC 615A 提供有边界、可复现的离散与时序符合性决策证据。

## 2. 成功准则

项目成功要求：适用 CRS 和观测边界受控；所有义务可追踪至已评审 VC；每条时序义务具备触发/响应语义、时钟模型、边界分区和误差预算；工具产生来源完整的带时戳证据；留出离散/时序故障诚实评价有限检测能力；概率、诊断和可迁移性措辞只能由相应门禁晋级；科学结果、工程发布、论文和教程均引用其上游产物 ID 与适用门禁记录，并且跨工作流依赖只通过 `TRACKS.md` 定义的受控契约发生。

## 3. 工作流

- W0 治理：基线、变更、风险和门禁；
- W1 需求：适用性、CRS 和义务模型；
- W2 方法论/模型：形式语义、带时钟 EFSM、迹关系、TP、VC 和稳健 oracle；
- W3 工具：运行器、时钟、误差预算、证据写入；
- W4 实验：注册、原始/派生证据；
- W5 分析：离散/时序覆盖、变异、依赖、校准和诊断；
- W6 出版：与已评审主张绑定的论文、学位论文和复现报告；
- W7 教程：分为通用验证教程和 ARINC 615A 实例教程，仅消费具名基线、工具发布和稳定示例。

## 4. 综合路线

路线依次经过 P0 基线、P1 范围/CRS、P2 带时钟模型/VCS、P3 仪器、P4 T1 执行、P5 T2 充分性、P6 可选 T3/诊断和 P7 第二协议复现。阶段由证据而非日历驱动，未解决的上游门禁不得被并行实现绕过。

## 5. 近期执行清单

### 基线发布

评审并批准 CR-2026-001 和 v4.2 基线包；只有数学、双语和治理门禁均通过后才能合并；合并后建立基线标签；既有 v4.1 证据不得改标，时序主张必须迁移或重评。

### 第一研究增量

建立适用性、CRS 和裁决 schema，注册 EXP-001 并执行 RG0 范围评审。

### 第一工程增量

建立 schema 校验、证据清单、单调时间戳和误差预算，同时保持现有测试基线。

## 6. 管理节奏

每周评审工作流；每个 PR 说明门禁影响；每个门禁产生独立签字结论；每月复核风险和范围；实验先注册后评审；发布前执行主张—证据审计。

## 7. 完成定义

工作项只有在受控路径存在产物、测试通过、版本与追踪完整、评审发现关闭或被显式接受、风险/偏差更新且主张不超过已获得层级时才算完成。时序结果还必须保存单调时钟、时间戳位置、分辨率、误差预算和边界判定依据。

## 8. 依赖与约束

P1–P2 依赖受控 ARINC 615A 材料；公开产物不得泄露专有条款。T3 依赖代表性校准实例，可以合法地保持不可用。外部同行或硬件提高外部有效性，但不能替代受控 oracle 和来源检查；P7 需要单独选择并投入第二协议。各工作流只能通过 `TRACKS.md` 定义的契约共享标识与证据；研究和教程不得导入可变实现内部结构，工程不得自行晋级科学主张。
