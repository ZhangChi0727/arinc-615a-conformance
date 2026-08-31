# Research Control

This document controls ARINC-domain research, experiments and claim ownership.
Current lifecycle state is shown only in the [root README](../../README.md) and
[`project-status.json`](../../project-status.json).

## 1. Research objective

Evaluate how a commit-bound Candidate GVS Core can be refined into a credible
ARINC 615A Profile, Binding, Configuration and evidence-producing instance.
The work seeks both scientific insight and usable engineering decisions while
keeping claims bounded by available sources, configurations and observations.

## 2. Method Inputs → ARINC Domain/Product Refinement → Instance Evidence → Controlled Feedback

| Research content | Authority | ARINC treatment |
|---|---|---|
| Generic verification objects and relations | Method repository | Cite immutable method commits and instantiate; do not redefine |
| Observation → Oracle → Result → Evidence → Argument → Claim | Method repository | Implement, constrain and evaluate the chain in the ARINC context |
| Coverage, Sufficiency and Reviewability dimensions | Method repository | Produce ARINC-specific observations and instance results |
| Core/Profile/Binding/Configuration layering | Method repository | Establish the ARINC Profile, Binding and real Configuration |
| ARINC applicability and CRS | ARINC repository | Conduct domain/product research without reproducing proprietary text |
| Protocol states, messages, timing, errors and robustness | ARINC repository | Refine observable ARINC domain semantics |
| IUT, environment, tools, clocks and error budget | ARINC repository | Control as Project Configuration |
| Test Purpose, Case, Procedure and fault model | ARINC repository | Design product/domain verification artifacts |
| Execution evidence, experimental results and ARINC claims | ARINC repository | Keep instance-scoped; no automatic Generic promotion |
| Finding about the method | Method repository decides | Submit a Framework Change Proposal; never modify the Core implicitly |

## 3. Input and refinement rules

1. ARINC research is conducted under, not in place of, the Candidate GVS Core.
2. Generic method inputs use immutable commit-bound locators; neither
   repository's mutable `main` branch is a controlled semantic identity.
3. ARINC may specialize generic objects into domain and product artifacts but
   may not reverse-define the Generic Core.
4. ARINC findings may support, qualify or falsify candidate method claims.
   Cross-instance generalization and RQ8 closure remain the method repository's
   synthesis responsibility.
5. Without an established Project Configuration and execution results, this
   repository remains in research and engineering preparation.

## 4. Research sequence

| Stage | Research activity | Controlled output |
|---|---|---|
| R0 | source and scope control | applicability declaration, source manifest, registration |
| R1 | requirements and observation boundary | CRS, obligations, adjudication record |
| R2 | behavioral and timed refinement | model, timing semantics, test purposes, cases and oracles |
| R3 | configured execution | observations, results, evidence manifests and deviations |
| R4 | bounded adequacy and diagnosis | mutation, coverage, calibration and diagnostic analyses |
| R5 | replication and synthesis | cross-instance comparison and explicitly bounded transfer claims |

## 5. Experiment and claim discipline

Experiments are registered before confirmatory execution. Raw observations are
immutable; transformations, oracle versions, uncertainty and exclusions are
recorded. A result becomes admissible evidence only after identity,
provenance, applicability and credibility are reviewed. Publications cite the
applicable configuration, evidence and decision records and state unearned
claims explicitly.

# 中文版

本文档控制 ARINC 领域研究、实验和主张归属。当前生命周期状态只在
[根 README](../../README.md)与 [`project-status.json`](../../project-status.json) 中展示。

## 1. 研究目标

评价由不可变提交绑定的 Candidate GVS Core 如何精化为可信的 ARINC 615A Profile、
Binding、Configuration 及证据生产实例。在可用来源、配置和观测边界内，同时追求科学
认识和可用工程决策。

## 2. 方法输入 → ARINC 领域／产品精化 → 实例证据 → 受控反馈

| 研究内容 | 权威 | ARINC 处理方式 |
|---|---|---|
| 通用验证对象及关系 | 方法仓库 | 引用不可变方法提交并实例化，不重新定义 |
| Observation → Oracle → Result → Evidence → Argument → Claim | 方法仓库 | 在 ARINC 场景实现、约束和评价该链 |
| Coverage、Sufficiency、Reviewability 等维度 | 方法仓库 | 形成 ARINC 特定 Observation 与实例 Result |
| Core/Profile/Binding/Configuration 分层 | 方法仓库 | 建立 ARINC Profile、Binding 与真实 Configuration |
| ARINC 适用性与 CRS | ARINC 仓库 | 开展领域／产品研究且不复刻专有原文 |
| 协议状态、消息、时序、错误与鲁棒性 | ARINC 仓库 | 精化可观测的 ARINC 领域语义 |
| IUT、环境、工具、时钟与误差预算 | ARINC 仓库 | 作为 Project Configuration 受控 |
| Test Purpose、Case、Procedure 与故障模型 | ARINC 仓库 | 设计产品／领域验证产物 |
| 执行证据、实验结果与 ARINC 主张 | ARINC 仓库 | 保持实例范围，不自动晋级为 Generic 结论 |
| 关于方法的问题 | 方法仓库决定 | 提交 Framework Change Proposal，不隐式修改 Core |

## 3. 输入与精化规则

1. ARINC 研究位于 Candidate GVS Core 之下，而不是取代它；
2. 通用方法输入使用不可变 commit-bound locator；任一仓库可变的 `main` 都不是受控语义身份；
3. ARINC 可把通用对象精化为领域和产品产物，但不能反向定义 Generic Core；
4. ARINC finding 可以支持、限定或反证候选方法主张；跨实例推广和 RQ8 关闭仍由方法仓库综合；
5. 在 Project Configuration 和执行结果尚未建立时，本仓库仍处于研究／工程准备状态。

## 4. 研究序列

| 阶段 | 研究活动 | 受控输出 |
|---|---|---|
| R0 | 来源与范围控制 | 适用性声明、来源清单、注册 |
| R1 | 需求与观测边界 | CRS、义务、裁决记录 |
| R2 | 行为与时序精化 | 模型、时序语义、TP、case 和 oracle |
| R3 | 配置化执行 | Observation、Result、Evidence Manifest 和偏差 |
| R4 | 有边界充分性与诊断 | 变异、覆盖、校准和诊断分析 |
| R5 | 复现与综合 | 跨实例比较及明确受限的迁移主张 |

## 5. 实验与主张纪律

确认性执行前必须注册实验。原始 Observation 不可变；转换、Oracle 版本、不确定度和排除项
必须记录。Result 只有在身份、来源、适用性和可信度经评审后才能成为准入 Evidence。
出版物必须引用适用 Configuration、Evidence 和 Decision，并明确陈述尚未获得的主张。
