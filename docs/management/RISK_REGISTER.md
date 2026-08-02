# Risk Register

| ID | Risk | Probability | Impact | Leading indicator | Mitigation / response | Owner | Gate |
|---|---|---:|---:|---|---|---|---|
| R-01 | Standard interpretation error | Medium | Critical | Reviewer disagreement or ambiguous clause | Independent extraction, adjudication log, stable source references | Research lead | RG1 |
| R-02 | Observation boundary cannot see required behavior | Medium | High | Oracle relies on unavailable internal state | Revise observation boundary or mark obligation unverifiable | Method owner | RG0/RG2 |
| R-03 | Base VCS has trace links but weak oracles | Medium | Critical | Mutants survive despite nominal coverage | Oracle review, negative cases, held-out faults | Test lead | RG3/G3 |
| R-04 | Mutant population is unrepresentative | High | High | High invalid/equivalent rate; narrow operators | Pre-registration, FMEA mapping, real-defect comparison, bounded wording | Research lead | G3 |
| R-05 | Repeat runs are dependent | Medium | High | Order effects, clustering, state leakage | Reset checks, randomization, mixed/cluster models | Experiment lead | G2/G4 |
| R-06 | Calibration is too small or biased | High | High | Extreme estimates, wide intervals, reused faults | Independent held-out calibration; stop at T2 if inadequate | Statistics owner | G4 |
| R-07 | Diagnostic model leaks fault instances | Medium | High | Train/test share derived instances | Fault-instance split, frozen pipeline, simple baselines | Analysis owner | G6 |
| R-08 | Tool defect is mistaken for IUT failure | Medium | Critical | Reference peers fail inconsistently | Unit/contract tests, validated oracle, tool-failure ERROR verdict | Engineering lead | RG4/G2 |
| R-09 | Proprietary standard or ICD text is exposed | Low | Critical | Raw clauses appear in public files | Hashes and stable references; private work area; release inspection | Repository owner | RG1/RG6 |
| R-10 | Scope expansion delays core evidence | High | Medium | FIND/INFORMATION, full 665, GUI added early | Enforce baseline scope and CR process | Project lead | RG0 |
| R-11 | Research and implementation versions drift | Medium | High | Evidence lacks baseline/CRS/VCS IDs | Machine-readable manifests and release checklist | Configuration owner | RG5 |
| R-12 | Second-protocol replication is never completed | Medium | Medium | Transferability deferred without owner | Keep C-XFER explicitly unsupported; schedule R5 separately | Research lead | G7 |
| R-13 | Timing semantics are incomplete or paired to the wrong events | Medium | Critical | Ambiguous trigger/reset/cancellation or inconsistent reviewers | Timing-obligation schema, source trace, independent RG1–RG3 review | Method owner | RG1–RG3 |
| R-14 | Timing instrument creates false precision | Medium | Critical | Boundary verdicts change with capture point/resolution | Monotonic clock, timestamp-chain validation, explicit error budget, robust interval oracle | Engineering lead | RG3–RG5/G2 |
| R-15 | Timing runs are dependent or drift over time | Medium | High | Autocorrelation, batch/order effects, warm-up or cross-session timer state | Randomization, reset checks, batch metadata, drift diagnostics, mixed/cluster models | Experiment lead | RG4–RG5/G4 |
| R-16 | Cross-domain contract or tutorial drift | Medium | High | A paper/tutorial cites “latest,” omits artifact IDs, imports implementation internals, or changes verdict wording | Version/trace spine, non-normative tutorial marker, link/contract validation, CR/DD feedback | Configuration owner | RG5–RG6 |

## Review cadence

- review at every RG gate and monthly during active implementation;
- escalate Critical-impact risks immediately;
- close a risk only with evidence, not elapsed time;
- record accepted residual risk in the applicable gate decision.

---

# 中文版

风险登记表控制标准解释、观测边界、oracle、故障代表性、重复运行依赖、校准偏差、诊断泄漏、工具误判、保密、范围蔓延、版本漂移和第二协议延期。v4.2 新增：R-13 时序触发/复位/取消/配对语义不完整；R-14 时间戳链或误差预算制造虚假精度；R-15 执行顺序、批次、预热或跨会话计时器导致时序依赖/漂移；R-16 论文/教程引用“最新”状态、遗漏产物 ID、导入实现内部结构或改变判定措辞而导致跨领域契约漂移。它们分别由时序 schema 和独立评审、单调时钟及稳健区间 oracle、随机化/重置/批次元数据和混合/聚类模型，以及版本/追踪脊柱、非规范教程标记、契约校验与 CR/DD 反馈缓解。

## 评审节奏

每月以及每个相关门禁前复核概率、影响、触发信号、缓解、负责人和剩余风险；Critical 风险未获明确接受时阻塞相应主张或发布。
