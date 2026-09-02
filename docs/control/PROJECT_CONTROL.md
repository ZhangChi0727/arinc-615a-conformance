# Project Control

This control document defines stable project mission, workstreams, lifecycle
gates and responsibilities. Current release, increment, stop and next-step
state is owned by the [root README](../../README.md) and
[`project-status.json`](../../project-status.json).

## 1. Mission

Produce and evaluate a bounded, reproducible Test-and-Analysis approach for
ARINC 615A, with Review and Inspection gates controlling artifacts, evidence
and claims.

## 2. Authority and records

- The method repository owns Generic verification objects and method rules.
- This repository owns the ARINC Profile, Product Binding, Project
  Configuration, instance design, execution and evidence.
- Baselines, change requests, reviews, decisions and historical evidence are
  atomic records. They are never rewritten to display current status.
- README is the sole human-readable current-status surface; JSON is its
  machine-readable source.

## 3. Workstreams

| Workstream | Responsibility | Stable entry |
|---|---|---|
| Governance | change classification, gates, risks and releases | [`CHANGE_CONTROL.md`](CHANGE_CONTROL.md) |
| Requirements | applicability, CRS and verification obligations | [`contracts/`](contracts/) |
| Research | ARINC refinement, experiments and bounded claims | [`RESEARCH_CONTROL.md`](../research/RESEARCH_CONTROL.md) |
| Engineering | implementation, configuration, tests and evidence production | [`ENGINEERING_CONTROL.md`](../engineering/ENGINEERING_CONTROL.md) |
| Tutorials | generic and ARINC-specific learning products | [`TUTORIAL_CONTROL.md`](../tutorial/TUTORIAL_CONTROL.md) |

## 4. Lifecycle

1. Control applicability, observation boundaries and requirements.
2. Define reviewed models, cases, procedures and oracles.
3. Establish Project Configuration from real controlled values.
4. Execute and preserve observations and provenance.
5. Evaluate observations with versioned oracles to produce results.
6. Admit characterized evidence and assess argument sufficiency.
7. Release only claims supported by approved evidence and decisions.

Parallel work is allowed only where it does not pre-empt an unresolved
upstream gate.

Source control and implementation are serial: an acquired source identity and
open dependencies are registered before applicability/CRS; reviewed CRS
precedes model refinement; reviewed model/profile precedes implementation; and
Project Configuration precedes execution. M0–M9 are the controlled delivery
stages for this lifecycle. A later stage PR cannot open before the prior stage
is approved, merged, checked and cleaned.

## 5. Gate discipline

Every increment identifies its inputs, configuration, evidence, open
deviations and affected claims. An item is complete only when acceptance tests
pass, trace links exist and findings are closed or explicitly accepted.
Independent review is required where the controlling baseline or change class
requires it.

## 6. Current-state discipline

Every pull request updates both `README.md` and `project-status.json`, even when
all lifecycle states remain unchanged. README records the increment, current
stop and next step. Detailed review transfer belongs in the PR description;
no new HANDOFF or current-status Markdown is created.

# 中文版

本控制文档规定稳定的项目使命、工作流、生命周期门禁和责任。当前发布、增量、停点及
下一步由[根 README](../../README.md)与
[`project-status.json`](../../project-status.json)统一管理。

## 1. 使命

形成并评价有边界、可复现的 ARINC 615A 测试—分析方法，由 Review 与 Inspection 门禁
控制产物、证据和主张。

## 2. 权威与记录

- 方法仓库拥有通用验证对象和方法规则；
- 本仓库拥有 ARINC Profile、Product Binding、Project Configuration、实例设计、执行和证据；
- baseline、CR、Review、决策和历史证据是原子记录，不为展示当前状态而改写；
- README 是唯一的人类可读当前状态界面，JSON 是其机器可读来源。

## 3. 工作流

| 工作流 | 职责 | 稳定入口 |
|---|---|---|
| 治理 | 变更分类、门禁、风险与发布 | [`CHANGE_CONTROL.md`](CHANGE_CONTROL.md) |
| 需求 | 适用性、CRS 与验证义务 | [`contracts/`](contracts/) |
| 研究 | ARINC 精化、实验与有边界主张 | [`RESEARCH_CONTROL.md`](../research/RESEARCH_CONTROL.md) |
| 工程 | 实现、配置、测试与证据生产 | [`ENGINEERING_CONTROL.md`](../engineering/ENGINEERING_CONTROL.md) |
| 教程 | 通用及 ARINC 专用学习产品 | [`TUTORIAL_CONTROL.md`](../tutorial/TUTORIAL_CONTROL.md) |

## 4. 生命周期

1. 控制适用性、观测边界和需求；
2. 定义并评审模型、case、procedure 与 oracle；
3. 使用真实受控值建立 Project Configuration；
4. 执行并保存 Observation 与来源；
5. 由版本化 Oracle 评价 Observation 并生成 Result；
6. 准入经表征的 Evidence 并评价论证充分性；
7. 仅发布获得批准证据和决定支持的主张。

只有在不预断未解决上游门禁时才允许并行工作。

来源控制与实现必须串行：先登记已取得来源身份和开放依赖，再进行适用性/CRS；受评审 CRS
先于模型精化；受评审模型/Profile 先于实现；Project Configuration 先于执行。M0～M9 是该
生命周期的受控交付阶段；前一阶段批准、合并、检查并清理前不得开启后一阶段 PR。

## 5. 门禁纪律

每个增量都要识别输入、配置、证据、开放偏差和受影响主张。只有验收测试通过、追踪关系
存在且 finding 已关闭或被明确接受，工作项才算完成。控制 baseline 或变更类别要求时，
必须进行独立评审。

## 6. 当前状态纪律

每个 PR 都必须同时更新 `README.md` 与 `project-status.json`，即使生命周期状态完全不变。
README 记录本次增量、当前停点和下一步；详细评审移交写入 PR 描述，不再创建 HANDOFF
或 current-status Markdown。
