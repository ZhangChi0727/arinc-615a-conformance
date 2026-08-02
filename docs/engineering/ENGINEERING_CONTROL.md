# Engineering Implementation Plan

| Field | Value |
|---|---|
| **Plan ID** | EIP-2026-001 |
| **Version** | 1.2 |
| **Status** | Approved for staged implementation |
| **Methodology baseline** | RB-2026-001-v4.2 |

## Engineering objective

Build a reproducible verification instrument that implements the Test path,
produces analysis-ready evidence, and enforces the baseline's scope and gate
semantics. The software is an experimental and engineering instrument; its
existence alone is not evidence of conformance.

## Target architecture

```text
Controlled CRS and models
        |
        v
Case catalog -> selector -> runner -> protocol peer/IUT
                    |          |
                    v          v
                 injector    observations
                                  |
                                  v
                              oracle/verdict
                                  |
                                  v
                  immutable evidence package
                         |              |
                         v              v
                 coverage/mutation   diagnosis/calibration
```

## Components

| Component | Responsibility | Planned location |
|---|---|---|
| Requirement/model schemas | IDs, applicability, obligations, trace relations | `configs/`, `docs/control/contracts/` |
| TFTP core | Packets, options, retry, duplicate, timeout, rollover | `src/a615a_sim/tftp/` |
| 615A session | DOWNLOAD/UPLOAD observable state machines | `src/a615a_sim/session/` |
| Timing model | clocks, guards, invariants, resets, timing obligations | `src/a615a_sim/timing/` |
| Minimal data artifacts | Only 665/664 constraints required by the controlled scope | `src/a615a_sim/lsap/` |
| Role controller | DLS/THW mode without duplicating protocol logic | `src/a615a_sim/roles/` |
| Verification engine | Selection, injection, robust discrete/timing oracle, verdict, reset, run control | `src/a615a_sim/engine/` |
| Evidence writer | Immutable run manifest, traces, measurements, verdicts | `src/a615a_sim/evidence/` |
| Analysis tools | Coverage, mutation, intervals, calibration, diagnosis | `src/a615a_sim/analysis/` |
| CLI/reporting | Reproducible commands and human/machine reports | `src/a615a_sim/cli.py`, `src/a615a_sim/report/` |

## Increment plan

| Increment | Scope | Acceptance evidence | Governing gate |
|---|---|---|---|
| E0 | Baseline schemas and IDs | Schema tests; example CRS/TP/VC round-trip | RG1 |
| E1 | TFTP protocol core hardening | Unit tests for nominal, duplicate, retry, wrong-TID, rollover | Engineering review |
| E2 | Clock-augmented observable 615A EFSM | Reviewed states, data/clock guards, invariants, resets, timing catalog, trace map | RG2 |
| E3 | VC engine and robust oracle API | Discrete and interval-timing examples for all four verdicts; boundary/reset tests | RG3 |
| E4 | Dual-role loopback timing instrument | Reproducible DOWNLOAD/UPLOAD runs; monotonic timestamps, error budget, manifest | RG4/G2 |
| E5 | Coverage and mutation pipeline | B0/B1/B2-U/B2-T/B3 reports; invalid/equivalent handling; held-out split | G3 |
| E6 | Evidence integrity and reporting | Raw-to-derived reproduction from clean checkout | RG5 |
| E7 | Optional calibration and diagnosis | Held-out evaluation and sensitivity reports | G4–G6 |

## Cross-cutting engineering requirements

- every execution records baseline, CRS, model, VCS, IUT, tool, and environment versions;
- PASS/FAIL/INCONCLUSIVE/ERROR remain distinct end to end;
- oracles are testable independently of the runner;
- time is measured from a declared monotonic source; timestamp source,
  resolution, observation points, and uncertainty budget are evidence;
- timing PASS requires the complete observation interval to be contained in the
  allowed interval; invalid timing instrumentation produces ERROR;
- reset and isolation are explicit case operations;
- base and extended VCS results are separable;
- raw evidence is append-only; transformations create derived artifacts;
- method inputs are imported through versioned schemas and semantic contracts;
  internal Python APIs are not research or tutorial interfaces;
- exported evidence manifests carry the upstream artifact versions and stable
  IDs required by research, publication, and executable tutorials;
- stochastic tools record seeds and repeated-seed results;
- proprietary standard text never enters public fixtures.

## Quality strategy

| Level | Purpose |
|---|---|
| Unit | Packet, data/clock guard, clock reset, robust oracle, schema, statistic, and serialization correctness |
| Contract | Stable interfaces between runner, peer, oracle, and evidence writer |
| Integration | DLS↔THW sessions, timer/reset behavior, failures, and evidence provenance |
| Scenario | Requirement-derived discrete/timed VCs and mutation detection |
| Reproduction | Rebuild a published table from a clean environment |

CI must test supported Python versions and reject schema, traceability, or
evidence-manifest violations once those validators exist.

## Definition of engineering baseline readiness

- E0–E4 are complete;
- RG0–RG4 are approved;
- at least one end-to-end VC preserves a complete evidence package;
- the package is reproduced on a clean checkout;
- no empirical claim exceeds T1;
- known limitations and deviations are recorded.

---

# 中文版

## 工程目标

实现一套可复现验证仪器：执行测试路径、产生可分析证据，并强制执行 v4.2 的范围、时序和门禁语义。主要组件包括需求/模型 schema、TFTP 核心、615A 会话、时钟与时序义务模型、双角色控制器、VC 引擎、稳健 oracle、证据写入、覆盖/变异/时序/校准/诊断分析和 CLI 报告。

## 目标架构

```text
受控需求/模型 -> VC 引擎 -> 双角色协议执行 -> oracle
                                      |          |
                                      +-> 证据 <-+
                                             |
                                  覆盖/变异/时序/统计分析
```

## 组件

组件包括需求/模型 schema、TFTP 核心、615A 会话、时钟与时序义务模型、双角色控制器、VC 引擎、稳健 oracle、证据写入器、分析管线以及 CLI/报告层。

## 增量计划

- E0：基线 schema 和 ID；
- E1：TFTP 核心加固；
- E2：带时钟 615A EFSM，包括数据/时钟守卫、不变量、复位和时序目录；
- E3：离散与区间时序 oracle API，覆盖四类判定和边界/复位测试；
- E4：双角色环回时序仪器，保存单调时间戳、误差预算和 manifest；
- E5–E7：覆盖/变异、证据复现及可选校准/诊断。

## 横向工程要求

每次执行记录完整版本链；四类判定端到端分离；oracle 可独立测试；时间来自声明的单调源；时间戳源、分辨率、位置和误差预算属于证据；只有完整观测区间包含于允许区间时才可判时序 PASS；仪器无效必须判 ERROR；原始证据只追加，派生产物保留全部输入和脚本版本。方法输入只通过版本化 schema 和语义契约导入，Python 内部 API 不是研究或教程接口；导出的证据清单必须携带研究、出版和可执行教程所需的上游版本与稳定 ID。

## 质量策略

使用单元、契约、集成和场景测试，覆盖离散/时序边界、重置、重复、乱序、超时、无响应、证据完整性和故障注入；工具失败必须与 IUT FAIL 分离。

## 工程基线就绪定义

只有 schema、版本脊柱、四类判定、单调时钟、误差预算、证据 manifest、端到端干运行和相关门禁均完成时，工程基线才可称为就绪。
