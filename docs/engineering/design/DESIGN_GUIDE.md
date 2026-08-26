# Design Area

Baseline-aligned engineering and model design lives here.

Under the v4.3 migration candidate, these designs realize the local ARINC 615A
Product Binding and future Project Configuration. They may implement external
Core/Profile extension points through versioned interfaces but do not define
Generic Core semantics. Every design identifies its owning layer.

| Design family | Required contents | Gate |
|---|---|---|
| Clock-augmented EFSM | states, variables, inputs/outputs, data/clock guards, invariants, resets, history | RG2 |
| Trace mapping | requirements/obligations to model targets | RG2 |
| VC/oracle | schemas, discrete/robust timing verdict logic, error budget, reset/isolation, evidence fields | RG3 |
| Tool architecture | interfaces, failure modes, configuration control | RG4 |
| Evidence package | manifest, raw/derived layout, provenance checks | RG4/RG5 |
| Verification objective and closure | objective schema, objective satisfaction, compliance index | RG2/RG6 |
| Test conformity | test article, setup, and procedure conformity records | RG4 |
| Problem and deviation closure | problem records, dispositions, closure review | RG5/RG6 |
| Analysis pipeline | discrete/timed coverage, mutation, dependence, statistics, diagnosis contracts | RG5 |

Design notes are not approved merely by being committed. Each controlled design
identifies its status, version, baseline, owner, and gate record.

---

# 中文版

本目录保存与基线一致的工程和模型设计：带时钟 EFSM 必须包含状态、变量、输入输出、数据/时钟守卫、不变量、复位和历史；追踪连接需求/义务与模型目标；VC/oracle 设计包含离散及稳健时序判定、误差预算、重置/隔离和证据字段；工具、证据包和分析管线分别由 RG4/RG5 控制。提交文件不等于获得批准，每个受控设计都必须标明状态、版本、基线、负责人和门禁记录。

在 v4.3 迁移候选下，这些设计实现本地 ARINC 615A Product Binding 和未来 Project
Configuration。它们可通过版本化接口实现外部 Core/Profile 扩展点，但不定义 Generic Core
语义；每份设计都必须标明所属层。
