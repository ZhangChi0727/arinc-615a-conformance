# Engineering Control

This document controls implementation, tools, configurations and evidence
production. Current status remains in the [root README](../../README.md).

## 1. Engineering objective and current boundary

Build an injectable ARINC 615A verification instrument that realizes approved
Profile/Binding artifacts and produces reproducible Observation, Result and
Evidence records. M0 adopts direction only: it creates no codec, protocol
operation, EFSM, case, procedure, oracle or Project Configuration.

## 2. Target dependency architecture

```text
protocol_profile / source identity / capability
              ↓
protocol_files codecs
              ↓
DatagramIO + Clock + TraceSink
              ↓
TftpSession
              ↓
ARINC 615A adaptation
              ↓
Information / Upload / Download / FIND operations
              ↓
TP / Case / Procedure / Oracle
              ↓
Observation / Result / Evidence / Decision / Claim
```

Each layer is independently replaceable and testable. `DatagramIO`, `Clock` and
`TraceSink` are injectable boundaries for deterministic tests, timing-error
control and complete traces. Transport cannot import operation or claim logic;
tools cannot promote evidence or claims. Information may bootstrap engineering
without changing the formal base claim. Upload remains the first formal base
VCS operation, followed by Download; Information/FIND expansion needs a later
scope decision.

## 3. Behavioral and analysis direction

Use one lightweight observable timed EFSM as the shared behavioral/timing/oracle
skeleton after M1 CRS approval. Retain Test-Analysis, with initial Analysis
limited to obligation traceability, state/transition/timing coverage, robust
timing margins and measurement-error budgets, and finite-fault mutation/held-
out adequacy. DTMC is not protocol semantics; HMM/ML diagnosis and Bayesian
calibration are deferred. FMEA may classify/prioritize faults, not decide
conformance. TTCN-3 is not a dependency or selected execution platform.

## 4. Open-source reuse boundary

| Level | Policy |
|---|---|
| L1 architecture/behavior reference | Allowed only with project, version, license and observed architecture recorded; never standards authority |
| L2 black-box/differential IUT | May be approved later with fixed version/license; conclusions remain instance-scoped |
| L3 source/constants/test vectors | Prohibited until independent license, source-cleanliness and architecture-fit review |

Project ARIEL (GPL-2.0) and Thomas Vogt's MPL-2.0, 615A-4-based implementation
are L1 candidates only. No source, constant, vector or derivative is imported by
M0.

## 5. Serial delivery and quality gates

M0 controls direction; M1 derives CRS/applicability; M2 refines the model; M3
creates executable foundations; M4 bootstraps Information; M5 establishes the
first formal Upload VCS; M6 establishes a real Configuration; M7 executes; M8
assesses finite-fault adequacy; M9 expands scope through a new decision. A stage
cannot start before the prior stage is approved, merged, checked and cleaned.

Every executable increment must bind approved requirements/model/cases and
record tool, dependency, environment and configuration identities. Tests,
static checks, traceability, evidence schema, bilingual controls and independent
review are release gates. Passing unit tests never establishes protocol
conformance, certification readiness or authority acceptance.

# 中文版

本文档控制实现、工具、配置和证据生产。当前状态仍只在[根 README](../../README.md) 中展示。

## 1. 工程目标与当前边界

构建可注入的 ARINC 615A 验证仪器，实现已批准 Profile/Binding 并产生可复现 Observation、
Result 与 Evidence。M0 只采纳方向，不创建 codec、协议操作、EFSM、用例、规程、oracle 或
Project Configuration。

## 2. 目标依赖架构

```text
协议 Profile / 来源身份 / 能力
              ↓
协议文件 codec
              ↓
DatagramIO + Clock + TraceSink
              ↓
TftpSession
              ↓
ARINC 615A adaptation
              ↓
Information / Upload / Download / FIND 操作
              ↓
TP / Case / Procedure / Oracle
              ↓
Observation / Result / Evidence / Decision / Claim
```

各层可独立替换和测试。`DatagramIO`、`Clock`、`TraceSink` 是确定性测试、时序误差控制和完整
trace 的注入边界。传输层不得导入操作或主张逻辑，工具不得晋级证据或主张。Information 可
用于工程 bootstrap，但不改变正式 base claim。Upload 仍是首个正式 base VCS 操作，随后是
Download；扩大 Information/FIND 需后续范围决定。

## 3. 行为与分析方向

M1 CRS 批准后使用单一轻量可观测 timed EFSM 作为行为/时序/oracle 骨架。保留 Test-
Analysis，首轮 Analysis 仅覆盖义务追踪、状态/迁移/时序覆盖、稳健时序裕量与测量误差预算、
有限故障域 mutation/held-out adequacy。DTMC 不是协议语义；延期 HMM/ML 诊断和 Bayesian
calibration。FMEA 只能分类/排序故障，不能判定符合性。TTCN-3 不是依赖或选定执行平台。

## 4. 开源复用边界

| 等级 | 政策 |
|---|---|
| L1 架构/行为参考 | 仅在记录项目、版本、许可证和所观察架构时允许；永远不是标准权威 |
| L2 黑盒/差分 IUT | 以后可在固定版本/许可证后批准；结论保持实例范围 |
| L3 源码/常量/测试向量 | 独立许可证、来源洁净度和架构适配评审前禁止 |

Project ARIEL（GPL-2.0）和 Thomas Vogt 基于 615A-4 的 MPL-2.0 实现仅是 L1 候选。M0 不
导入源码、常量、向量或派生物。

## 5. 串行交付与质量门

M0 控制方向；M1 派生 CRS/适用性；M2 精化模型；M3 创建可执行基础；M4 bootstrap
Information；M5 建立首个正式 Upload VCS；M6 建立真实 Configuration；M7 执行；M8 评价
有限故障域充分性；M9 通过新决定扩展范围。前一阶段批准、合并、检查和清理前不得启动下一阶段。

每个可执行增量必须绑定批准的需求/模型/用例，并记录工具、依赖、环境和配置身份。测试、静态
检查、追踪、证据 schema、双语控制和独立评审是发布门。单元测试通过不能建立协议符合性、认证
准备度或权威接受。
