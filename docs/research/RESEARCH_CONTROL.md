# Research Control

This document controls ARINC-domain research, experiments and claim ownership.
Current lifecycle state is shown only in the [root README](../../README.md) and
[`project-status.json`](../../project-status.json). Controlled source identities
are in [`controlled_sources.json`](../../configs/research/controlled_sources.json).
The successor research method is **CL-TAV** (Closed-Loop Test–Analysis
Verification) under [CR-2026-012](../control/changes/CR-2026-012.md). The
protocol CRS authority remains the
[`CRS/applicability package`](../../configs/requirements/arinc_615a3_m1_crs.json);
its [review view](../control/requirements/ARINC615A3_M1_CRS_REVIEW_VIEW.md) is generated.
Historical merged M1 bytes remain a preserved identity. Expanding that package
creates a **new** successor identity; it does not rewrite frozen blobs and does
not transplant PR #13/#14 approvals. The merged bounded M2 package is
[`observable timed model`](../../configs/models/arinc_615a3_m2_model.json); it
covers the bound UPLOAD/INFORMATION input only. New CRS services are
model-refinement pending. M3 implementation stays blocked. The successor
development-ready PR is not this increment.

## 1. Research objective and authority boundary

Evaluate **CL-TAV**: a closed loop of test, observation, constraint verdict /
diagnosis and next-test selection for protocol conformance verification and
fault localization, using ARINC 615A as the case. CRS, SysML, models and
evidence mechanisms support that loop; they do not replace it. The combination
of Test and Analysis is not claimed as a first invention.

Evaluate how the commit-bound Candidate GVS Core can still be refined into a
credible ARINC 615A Profile, Binding, Configuration and evidence-producing
instance. The method repository owns Generic objects and cross-instance
synthesis. This repository owns ARINC source/applicability research, product
semantics, IUT refinement, instance execution and bounded feedback. It may
specialize but may not reverse-define the Generic Core.
Cross-instance generalization and RQ8 closure remain the method repository's
synthesis responsibility and are not completed by deleting historical RQ6 from
the successor report. ARINC research is conducted under, not in place of, the Candidate GVS Core.

Protocol CRS scope under CR-2026-012 includes INFORMATION, UPLOAD, Media
Defined DOWNLOAD, Operator Defined DOWNLOAD, FIND, and source-stated
interrupt/reject/exception/retry obligations, plus a complete applicability
audit of 665-5, 664P2/P3-1/P7 and the registered RFCs. Ordinary Ethernet,
Compliant, Profiled and AFDX are configuration variants, not one instance.
ARINC 645 unique algorithm details remain `BLOCKED-SOURCE-645`; already
explicit 615A/665 integrity obligations stay in the CRS.

## 2. Method Inputs → ARINC Domain/Product Refinement → Instance Evidence → Controlled Feedback

| Content | Authority | ARINC responsibility |
|---|---|---|
| Generic objects, relations and Core/Profile/Binding/Configuration contract | Method repository immutable commits | Instantiate and qualify; never redefine |
| Observation → Oracle → Result → Evidence → Argument → Claim | Method repository | Realize and audit the chain in the ARINC domain |
| ARINC 615A protocol authority | ARINC repository source register | Use only registered ARINC 615A-3; do not reproduce proprietary text |
| ARINC 665 data formats | ARINC repository source register | Use 665-5 only within requirement-level applicability decisions; never claim 665-3 equivalence |
| CRC/check-value/naming algorithms | ARINC 645, currently open | Keep affected integrity capabilities unearned until source, applicability and CRS gates close |
| Protocol states, messages, timing and errors | ARINC repository | Refine a lightweight observable timed EFSM after CRS approval |
| IUT, environment, tools, clocks and error budget | ARINC repository | Establish only through a reviewed Project Configuration |
| Tests, analyses and execution evidence | ARINC repository | Produce instance-scoped results; no automatic Generic promotion |
| Method finding | Method repository decides | Submit a Framework Change Proposal with bounded ARINC evidence |

## 3. Source and model discipline

ARINC 615A-3 is the sole active protocol authority. `A4` is a wire value, not an
edition. Historical source assumptions are non-authoritative and are governed by
the controlled source register and change record. ARINC 665-5 is in full
applicability audit for triggered load-data/media-set clauses. ARINC 645 remains
the only unacquired original standard; it blocks unique algorithm details, not
whole obligation classes already stated in 615A/665. Source migration
requires an acquired/identified source, applicability delta, CR and independent
review; no future edition is preselected. “Study later” is not an acceptable
blanket disposition for an already-held source unit.

The protocol behavioural model remains one lightweight observable timed EFSM.
CL-TAV wraps Test and Analysis into an explicit diagnosis and next-test loop
(candidate: DD-029). The merged M2 EFSM does not automatically cover expanded
CRS services. DTMC, HMM/ML and Bayesian calibration stay out of the default
algorithm; TTCN-3 is neither a dependency nor selected platform. Confirmatory
experiments are planned in this increment and not executed.

## 4. One research sequence, mapped to the serial delivery route

| Research stage | Research activity | Delivery stages |
|---|---|---|
| R0 | source and scope control | M0 source/route adoption; M1 CRS/applicability |
| R1 | requirements and observation boundary | M1 CRS; M2 Profile/Binding inputs |
| R2 | behavioral and timed refinement | M2 EFSM; M3 executable foundations; M4 bootstrap |
| R3 | configured execution | M5 base Upload VCS; M6 Configuration; M7 execution |
| R4 | bounded adequacy and diagnosis | M8 finite-fault coverage/mutation |
| R5 | replication and synthesis | M9 separately approved scope expansion and later cross-instance work |

R0–R5 are research views of M0–M9, not a competing lifecycle. Each delivery
stage is serial and independently reviewed. Historical merged M1 is a preserved
input identity. CR-2026-012 is a successor protocol-CRS expansion, not M3.
M3 must not start in this increment. Expanding CRS does not flip
SCOPE-EXPANSION-GATE by itself and does not grant the old M2 new-service
coverage. A later development-ready PR, after this CRS is accepted, supplies
tool requirements and implementation contracts.

## 5. Open-source and claim discipline

L1 architecture/behavior reference is allowed with project/version/license and
observation records. L2 black-box/differential use may be approved later with a
fixed identity and license; conclusions remain instance-scoped. L3 source,
constants and test vectors are prohibited pending independent license, source-
cleanliness and architecture-fit review. Open-source implementations never
replace standards authority.

Experiments are registered before confirmatory execution. Raw observations are
immutable; transformations, oracle versions, uncertainty and exclusions are
recorded. Evidence is admitted only after identity, provenance, applicability
and credibility review. No current work establishes Configuration, instance
evaluation, protocol conformance, certification or authority acceptance.

# 中文版

本文档控制 ARINC 领域研究、实验和主张归属。当前生命周期状态只在[根 README](../../README.md)
和 [`project-status.json`](../../project-status.json) 展示；来源身份由
[`controlled_sources.json`](../../configs/research/controlled_sources.json) 控制。
后继研究方法为 [CR-2026-012](../control/changes/CR-2026-012.md) 下的 **CL-TAV**。
协议 CRS 权威仍为
[`CRS/适用性数据包`](../../configs/requirements/arinc_615a3_m1_crs.json)；
[评审视图](../control/requirements/ARINC615A3_M1_CRS_REVIEW_VIEW.md) 为生成物。
历史已合并 M1 字节是保留身份；扩大该包产生**新**后继身份，不改写冻结 blob，也不移植
PR #13／#14 批准。已合并有界 M2 为
[`可观测时序模型`](../../configs/models/arinc_615a3_m2_model.json)，只覆盖其绑定的
UPLOAD／INFORMATION 输入；新 CRS 服务为模型细化待完成。本增量不启动 M3，也不是
开发就绪后继 PR。

## 1. 研究目标与权威边界

评价 **CL-TAV**：以测试、观测、约束判定／诊断与后续测试选择构成闭环，用于协议符合性
验证与故障定位，并以 ARINC 615A 为案例。CRS、SysML、模型与证据机制是支撑，不能替代
该闭环。不把 Test 与 Analysis 的组合宣称为首次发明。

仍评价不可变提交绑定的 Candidate GVS Core 如何精化为可信的 ARINC 615A Profile、
Binding、Configuration 和证据生产实例。方法仓库拥有 Generic 对象和跨实例综合；本仓库
拥有 ARINC 来源／适用性研究、产品语义、IUT 精化、实例执行和有边界反馈。可以专门化，
不能反向定义 Generic Core。跨实例推广和 RQ8 关闭仍由方法仓库综合，不因删除历史
RQ6 而视为完成。

CR-2026-012 下协议 CRS 范围包括 INFORMATION、UPLOAD、Media Defined DOWNLOAD、
Operator Defined DOWNLOAD、FIND 及来源已规定的中断／拒绝／异常／重试，并对 665-5、
664P2／P3-1／P7 与已登记 RFC 做完整适用性审计。普通 Ethernet、Compliant、Profiled、
AFDX 是配置变体，不是同一实例。ARINC 645 独有算法细节保持 `BLOCKED-SOURCE-645`。

## 2. 方法输入 → ARINC 领域／产品精化 → 实例证据 → 受控反馈

| 内容 | 权威 | ARINC 责任 |
|---|---|---|
| Generic 对象、关系及四层契约 | 方法仓库不可变提交 | 实例化和限定，不重定义 |
| Observation → Oracle → Result → Evidence → Argument → Claim | 方法仓库 | 在 ARINC 领域实现并审计该链 |
| ARINC 615A 协议权威 | 本仓库来源登记册 | 只使用登记的 615A-3，不复刻专有正文 |
| ARINC 665 数据格式 | 本仓库来源登记册 | 仅按需求级适用性决定使用 665-5，不声称等价 665-3 |
| CRC/check-value/命名算法 | 当前开放的 ARINC 645 | 来源、适用性和 CRS 门关闭前不得取得相关完整性能力 |
| 协议状态、消息、时序与错误 | 本仓库 | CRS 批准后精化轻量可观测 timed EFSM |
| IUT、环境、工具、时钟与误差预算 | 本仓库 | 仅通过受评审 Project Configuration 建立 |
| Test、Analysis 与执行证据 | 本仓库 | 产生实例范围结果，不自动晋级 Generic 结论 |
| 方法 finding | 方法仓库决定 | 用有边界 ARINC 证据提交 Framework Change Proposal |

## 3. 来源与模型纪律

615A-3 是唯一活动协议权威；`A4` 是线值而非版次。历史来源假设不具权威性，并由受控来源
登记册与变更记录治理。665-5 对其触发的加载数据／媒体集条款做完整适用性审计。645 是
唯一未取得的原文，只阻塞独有算法细节，不删除 615A／665 已明示的义务类别。来源迁移需
取得并登记来源、完成适用性差分、CR 和独立评审；不预选未来版本。已有来源活动条款不得
再用“以后研究”作为笼统处置。

协议行为模型仍是单一轻量可观测 timed EFSM。CL-TAV 把 Test 与 Analysis 做成显式诊断与
后续测试闭环（候选：DD-029）。已合并 M2 不自动覆盖扩大后的 CRS 服务。默认算法不引入
DTMC、HMM／ML 或 Bayesian calibration；TTCN-3 不是依赖或选定平台。本增量只规划确认性
实验，不执行。

## 4. 单一研究序列与串行交付路线的映射

| 研究阶段 | 研究活动 | 交付阶段 |
|---|---|---|
| R0 | 来源与范围控制 | M0 来源/路线采纳；M1 CRS/适用性 |
| R1 | 需求与观测边界 | M1 CRS；M2 Profile/Binding 输入 |
| R2 | 行为与时序精化 | M2 EFSM；M3 可执行基础；M4 bootstrap |
| R3 | 配置化执行 | M5 Upload 基础 VCS；M6 Configuration；M7 执行 |
| R4 | 有界充分性与诊断 | M8 有限故障域覆盖/mutation |
| R5 | 复现与综合 | M9 单独批准的范围扩展及以后跨实例工作 |

R0～R5 是 M0～M9 的研究视图，不是竞争生命周期。交付阶段串行且分别评审。历史已合并 M1
是保留输入身份。CR-2026-012 是后继协议 CRS 扩大，不是 M3。本增量不得启动 M3。扩大 CRS
本身不翻转 SCOPE-EXPANSION-GATE，也不授予旧 M2 新服务覆盖。扩大 CRS 被接受后，后继
开发就绪 PR 再提供工具需求与实现契约。

## 5. 开源与主张纪律

L1 架构/行为参考需记录项目/版本/许可证和观察；L2 黑盒/差分使用以后可在固定身份和许可证
后批准，结论保持实例范围；L3 源码、常量和测试向量在独立许可证、来源洁净度和架构适配评审
前禁止。开源实现不能代替标准权威。

确认性执行前登记实验；原始 Observation 不可变，并记录变换、oracle 版本、不确定性和排除。
Evidence 只有在身份、来源、适用性和可信度评审后准入。当前工作不建立 Configuration、实例
评价、协议符合性、认证或权威接受。
