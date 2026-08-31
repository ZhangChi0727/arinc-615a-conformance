# Engineering Control

This document controls implementation, configuration, testing and evidence
production. Current increment and stop state are owned by the
[root README](../../README.md) and [`project-status.json`](../../project-status.json).

## 1. Engineering objective

Build a deterministic, inspectable instrument that executes reviewed ARINC
verification procedures, records clock-characterized observations and
produces provenance-complete outputs without promoting its own claims.

## 2. Stable architecture

| Component | Responsibility |
|---|---|
| Configuration loader | validate IUT, environment, tool and procedure identities |
| Protocol roles | exercise bounded data-loader interactions |
| Case/procedure runner | execute versioned preconditions, actions and cleanup |
| Observation capture | preserve packets, timestamps, logs and environment facts |
| Oracle evaluator | transform observations into versioned results |
| Evidence writer | package characterized evidence and provenance |

The evidence chain remains: Observation → Oracle evaluation → Result →
Evidence → Argument/SufficiencyAssessment → Decision → versioned Claim.

## 3. Increment discipline

Each engineering increment declares requirements, configuration assumptions,
tests, evidence outputs, limitations and affected claims. It updates README and
`project-status.json` in the same pull request and records “unchanged” when no
lifecycle state changes.

## 4. Quality and configuration gates

- deterministic unit and integration tests;
- explicit block-number, timeout and retry boundary tests;
- monotonic timestamps and reviewed measurement-error budgets;
- schema validation and provenance-complete evidence manifests;
- negative tests for unsupported claim promotion;
- Python 3.10, 3.11 and 3.12 CI.

No execution result is interpreted before a real Project Configuration exists.
Tool success is evidence about the tool and run, not by itself protocol
conformance or certification evidence.

# 中文版

本文档控制实现、配置、测试与证据生产。当前增量和停点由
[根 README](../../README.md)与 [`project-status.json`](../../project-status.json) 管理。

## 1. 工程目标

构建确定、可检查的工具，执行已评审 ARINC 验证规程，记录经时钟表征的 Observation，
产生来源完整的输出，并且不自行晋级主张。

## 2. 稳定架构

| 组件 | 职责 |
|---|---|
| 配置加载器 | 校验 IUT、环境、工具和规程身份 |
| 协议角色 | 执行有边界的数据加载交互 |
| Case／procedure runner | 执行版本化前置条件、动作与清理 |
| Observation 捕获 | 保存报文、时戳、日志和环境事实 |
| Oracle evaluator | 将 Observation 转换为版本化 Result |
| Evidence writer | 封装经表征的 Evidence 与来源 |

证据链保持为：Observation → Oracle evaluation → Result → Evidence →
Argument/SufficiencyAssessment → Decision → versioned Claim。

## 3. 增量纪律

每个工程增量声明需求、配置假设、测试、证据输出、限制和受影响主张，并在同一 PR 更新
README 与 `project-status.json`；没有生命周期状态变化时也要明确记录“不变”。

## 4. 质量与配置门禁

- 确定性单元测试与集成测试；
- 显式的块号、超时和重试边界测试；
- 单调时戳与经评审的测量误差预算；
- schema 校验与来源完整的 Evidence Manifest；
- 防止不受支持主张晋级的负例；
- Python 3.10、3.11 和 3.12 CI。

在真实 Project Configuration 建立之前不得解释执行结果。工具成功仅是工具和运行的证据，
本身不是协议符合性或认证证据。
