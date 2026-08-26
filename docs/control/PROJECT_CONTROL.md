# Integrated Project Plan

| Field | Value |
|---|---|
| **Plan ID** | IPP-2026-001 |
| **Version** | 1.4 |
| **Status** | Active under effective and frozen RB-2026-001-v4.2.1; GVS-bound v4.3 migration candidate under CR-2026-004 |
| **Baseline** | RB-2026-001-v4.2.1 effective; RB-2026-001-v4.3 migration candidate bound to MethodDefinitionCommit `48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b` |
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
8. cross-workstream dependencies use the controlled contracts in
   `contracts/DOMAIN_BOUNDARIES.md`
   rather than implementation internals or implicit “latest” state;
9. transferability wording matches the presence or absence of replication.

## 3. Workstreams

| Workstream | Owner role | Canonical plan | Primary outputs |
|---|---|---|---|
| W0 Governance | Project/research lead | `docs/control/` | baseline, decisions, risks, gates, reader releases |
| W1 Requirements | Requirements researchers | `docs/control/contracts/`, `docs/research/RESEARCH_CONTROL.md` | applicability, CRS, obligation model |
| W2 Methodology and modeling | Method researchers | `docs/research/` | formal semantics, clock-augmented EFSM, trace relations, TPs, VCs, robust oracles |
| W3 Instrument | Engineering lead | `docs/engineering/ENGINEERING_CONTROL.md` | simulator, engine, evidence writer |
| W4 Experiments | Experiment/statistics lead | `docs/research/EXPERIMENT_PLAN.md` | registrations, raw/derived evidence |
| W5 Analysis | Research team | report §§6–8 | discrete/timed coverage, mutation, dependence, calibration, diagnosis |
| W6 Publication | Research lead | `docs/research/publication/` | papers, thesis, replication report tied to reviewed claims |
| W7 Tutorial | Technical educator | `docs/tutorial/TUTORIAL_CONTROL.md`, `artifacts/tutorials/` | version-pinned teaching, exercises, and runbooks |

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

- retain RB-2026-001-v4.2 and its PR #6 release provenance as the frozen
  methodological predecessor;
- retain the completed CR-2026-003, DD-014, relocation, reader-report,
  bilingual-parity, and validator review trace for v4.2.1;
- use `BRR-RB-2026-001-v4.2.1` to identify the PR #7 release commit and tag;
- do not relabel v4.1/v4.2 evidence merely because repository paths changed.

### v4.3 candidate baseline

- establish `TMP-XRB-ARINC615A-01` through
  [`EXTERNAL_GVS_BINDING.md`](contracts/EXTERNAL_GVS_BINDING.md), bound to the
  immutable Candidate GVS Core definition at
  `48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b`;
- limit this repository's authority to the ARINC 615A Profile, Product Binding,
  Project Configuration, instance engineering, instance research, and instance
  evidence;
- migrate Verification Objectives, Objective Satisfaction Records, the
  Compliance Evidence Index, Evidence Manifests, test conformity, and problem
  closure without redefining generic method objects;
- treat L0–L7, A0–A4, R0–R5, RG, and G as ARINC Profile/project candidate
  semantics, pending independent review;
- keep compatibility `NOT-DETERMINED`, evaluation `NOT-EXERCISED`, and PR #9
  Draft until the independent migration review completes;
- do not promote any existing empirical, compatibility, certification, or
  authority-acceptance claim by the restructuring alone.

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
  `contracts/DOMAIN_BOUNDARIES.md`; research and tutorials must not import mutable implementation
  internals, and engineering must not promote scientific claims.

## 9. Information architecture

The repository has two deliberately different surfaces:

- the **reader release surface** is the root README plus versioned deliverables
  below `artifacts/`;
- the **developer control plane** is `docs/`, entered through exactly one
  control document for project, research, engineering, and tutorial work.

The four control documents are indexes, ownership declarations, and lifecycle
controls. They do not absorb atomic baselines, contracts, change requests,
decisions, gate records, experiment protocols, designs, evidence manifests, or
increment records. Stable artifact IDs and versions, not file paths alone,
provide controlled traceability.

Root machine files such as `pyproject.toml`, `.gitignore`, and automation
configuration remain where their tools discover them. They are not
reader-facing documents.

## 10. Reporting system

Each engineering or research increment closes with internal assurance records
that identify the baseline, source commit, requirements, tool/configuration,
tests, evidence manifests, analyses, open deviations, risks, and gate status.
These records remain in their owning developer product line; engineering uses
the [`Increment Assurance Record template`](../engineering/increments/IAR_TEMPLATE.md).
Baseline publication is captured separately in a Baseline Release Record such
as [`BRR-RB-2026-001-v4.2`](baselines/BRR-RB-2026-001-v4.2.md).

Each reader-facing update is released as one self-contained bilingual report
under `artifacts/reports/current/`. It summarizes the relevant internal
records, links stable sources, distinguishes results from plans, and states all
unearned claims. A new release moves the preceding current report unchanged to
`artifacts/reports/archive/`; the root README is updated to point directly to
the replacement. Reader reports do not become normative merely because they
are easier to read.

---

# 中文版

## 1. 使命

形成、评价并工程化一种测试—分析方法，为 ARINC 615A 提供有边界、可复现的离散与时序符合性决策证据。

## 2. 成功准则

项目成功要求：适用 CRS 和观测边界受控；所有义务可追踪至已评审 VC；每条时序义务具备触发/响应语义、时钟模型、边界分区和误差预算；工具产生来源完整的带时戳证据；留出离散/时序故障诚实评价有限检测能力；概率、诊断和可迁移性措辞只能由相应门禁晋级；科学结果、工程发布、论文和教程均引用其上游产物 ID 与适用门禁记录，并且跨工作流依赖只通过 `contracts/DOMAIN_BOUNDARIES.md` 定义的受控契约发生。

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

RB-2026-001-v4.2 及 PR #6 发布来源作为冻结方法论前序保留；保留已完成的 CR-2026-003、
DD-014、v4.2.1 迁移、读者报告、双语对等及校验器评审轨迹；通过
`BRR-RB-2026-001-v4.2.1` 标识 PR #7 发布提交与标签；不得仅因仓库路径变化而重标
v4.1/v4.2 证据。

### v4.3 候选基线

通过 [`EXTERNAL_GVS_BINDING.md`](contracts/EXTERNAL_GVS_BINDING.md) 建立
`TMP-XRB-ARINC615A-01`，并固定绑定 Candidate GVS Core 提交
`48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b`。本仓库只对 ARINC 615A
Profile、Product Binding、Project Configuration、实例工程、实例研究和实例证据负责。
VO、OSR、CEI、Evidence Manifest、测试符合性和问题关闭按实例语义迁移，不重定义通用
方法对象；L0–L7、A0–A4、R0–R5、RG 和 G 均作为 ARINC Profile/项目候选语义。
兼容性保持 `NOT-DETERMINED`，评价保持 `NOT-EXERCISED`，PR #9 在独立迁移评审完成前
保持 Draft；重构本身不晋级任何经验、兼容性、认证或权威接受主张。

### 第一研究增量

建立适用性、CRS 和裁决 schema，注册 EXP-001 并执行 RG0 范围评审。

### 第一工程增量

建立 schema 校验、证据清单、单调时间戳和误差预算，同时保持现有测试基线。

## 6. 管理节奏

每周评审工作流；每个 PR 说明门禁影响；每个门禁产生独立签字结论；每月复核风险和范围；实验先注册后评审；发布前执行主张—证据审计。

## 7. 完成定义

工作项只有在受控路径存在产物、测试通过、版本与追踪完整、评审发现关闭或被显式接受、风险/偏差更新且主张不超过已获得层级时才算完成。时序结果还必须保存单调时钟、时间戳位置、分辨率、误差预算和边界判定依据。

## 8. 依赖与约束

P1–P2 依赖受控 ARINC 615A 材料；公开产物不得泄露专有条款。T3 依赖代表性校准实例，可以合法地保持不可用。外部同行或硬件提高外部有效性，但不能替代受控 oracle 和来源检查；P7 需要单独选择并投入第二协议。各工作流只能通过 `contracts/DOMAIN_BOUNDARIES.md` 定义的契约共享标识与证据；研究和教程不得导入可变实现内部结构，工程不得自行晋级科学主张。

## 9. 信息架构

仓库有两个刻意分离的界面：

- **读者发布面**由根 README 和 `artifacts/` 下的版本化交付物组成；
- **开发者控制平面**是 `docs/`，项目、研究、工程和教程工作各自恰有一份控制文档作为入口。

四份控制文档承担索引、所有权声明和生命周期控制，不吞并原子化的基线、契约、变更请求、
决策、门禁记录、实验方案、设计、证据清单或增量记录。受控追踪依靠稳定产物 ID 和版本，
而不只依靠文件路径。

`pyproject.toml`、`.gitignore` 和自动化配置等根目录机器文件继续位于工具约定的发现位置；
它们不是面向读者的文档。

## 10. 报告体系

每个工程或研究增量以内部保证记录结束；该记录标识基线、源提交、需求、工具/配置、测试、
证据清单、分析、开放偏差、风险和门禁状态。这些记录留在其所属开发者产品支线中；工程使用
[`增量保证记录模板`](../engineering/increments/IAR_TEMPLATE.md)。基线发布另以基线发布记录
保存，例如 [`BRR-RB-2026-001-v4.2`](baselines/BRR-RB-2026-001-v4.2.md)。

随后，每次面向读者的更新以 `artifacts/reports/current/` 下的一份自包含双语报告发布。
它汇总相关内部记录，链接稳定来源，区分结果与计划，并声明全部尚未获得的主张。新报告
发布时，上一份当前报告原样迁入 `artifacts/reports/archive/`，根 README 直接改指新报告。
读者报告不会因为易读而自动取得规范地位。
