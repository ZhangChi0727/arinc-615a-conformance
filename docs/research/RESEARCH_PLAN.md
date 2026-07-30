# Research Plan

| Field | Value |
|---|---|
| **Plan ID** | RP-2026-001 |
| **Version** | 1.1 |
| **Status** | Approved for baseline execution |
| **Methodology baseline** | RB-2026-001-v4.2 |
| **Primary report** | [`../study/RR-2026-001_test_analysis_conformance_methodology.md`](../study/RR-2026-001_test_analysis_conformance_methodology.md) |

## Objective

Evaluate whether an auditable Test-and-Analysis workflow can produce useful,
bounded, and reproducible ARINC 615A conformance evidence while improving
engineering traceability, defect detection, diagnosis, and release decisions.

## Research questions and work packages

| RQ | Work package | Principal output | Decision criterion |
|---|---|---|---|
| RQ1 Derivation | WP1 Scope and CRS | Applicability declaration, CRS, adjudication log | RG0–RG1 passed |
| RQ2 Coverage | WP2 Timed model and VCS | clock-augmented EFSM, timing catalog, trace relations, coverage matrices, VCs | RG2–RG3 and G1 passed |
| RQ3 Bounded adequacy | WP3 Fault study | Operator catalog, development/held-out mutants, results | G3 passed; held-out rate reported |
| RQ4 Evidence interpretation | WP4 Repeatability and calibration | Run model, intervals, calibration dataset, sensitivity analysis | G4–G5 passed before T3 |
| RQ5 Diagnosis | WP5 Diagnostic evaluation | Features, baseline classifier, held-out metrics | G6 passed before localization claim |
| RQ6 Transferability | WP6 Replication | Second-protocol instance and comparative analysis | G7 passed |

## Research sequence

### Phase R0 — Baseline and registration

- freeze RB-2026-001-v4.2;
- establish document ownership, change control, risks, and claim matrix;
- register the first CRS extraction and inter-reviewer study.

**Exit:** repository baseline is internally consistent and reproducible.

### Phase R1 — Requirements and observation boundary

- record standard edition, services, roles, options, exclusions, and observation boundary;
- perform two independent normative-requirement extractions;
- adjudicate disagreements without publishing proprietary standard text;
- classify every applicable requirement by verification obligation.

**Exit:** RG0, RG1, and G0 passed.

### Phase R2 — Behavioral model and verification cases

- construct the clock-augmented observable EFSM and timing-obligation catalog;
- establish \(\rho_{RT}\), \(\rho_{TV}\), and requirement/model-target mappings;
- derive positive, negative, data, sequence, and early/nominal/boundary/late/no-response timing cases;
- independently review discrete and robust timing oracle logic, clock/reset semantics, and measurement-error budgets.

**Exit:** RG2, RG3, and G1 passed; T0 achieved.

### Phase R3 — Execution and bounded adequacy

- freeze tool, environment, IUT configuration, seeds, and logging;
- execute the base VCS and preserve every PASS/FAIL/INCONCLUSIVE/ERROR;
- pre-register development and held-out fault splits;
- evaluate mutation adequacy and held-out detection.

**Exit:** RG4, RG5, G2, and G3 passed; T1/T2 results available.

### Phase R4 — Quantitative evidence and diagnosis

- evaluate repeated-run assumptions and operational PASS intervals;
- estimate false-fail and false-PASS behavior from independent calibration data;
- report likelihood/Bayes-factor results with prior sensitivity only when valid;
- compare diagnostic models against simple baselines and permit abstention.

**Exit:** G4–G6 passed for any T3 or diagnosis claim.

### Phase R5 — Transferability

- select a protocol with contrasting state, timing, or transport characteristics;
- repeat the minimum R1–R3 artifact chain;
- identify invariant and protocol-specific method components.

**Exit:** G7 passed; RQ6 answered with cross-instance evidence.

## Pre-registered hypotheses

| ID | Hypothesis | Comparator | Primary metric |
|---|---|---|---|
| H1 | Requirement+EFSM derivation increases obligation coverage | Existing ICD/engineering set B0 | Coverage by obligation category |
| H2 | Development-mutant refinement improves held-out fault detection | B2-T versus B3 | Held-out detection-rate difference with interval |
| H3 | Gate reviews reduce downstream escaped defects | Ungated or earlier artifact revisions | Escape rate and rework effort |
| H4 | Calibrated evidence outperforms raw PASS frequency as a probabilistic forecast | Raw-frequency baseline | Brier score/log loss on held-out instances |
| H5 | Feature-based diagnosis outperforms severity-only ranking | FMEA severity baseline | Macro F1, Top-3 recall, abstention curve |
| HT1 | A clock-augmented model exposes timing obligations missed by an untimed EFSM | B2-U versus B2-T | Added valid timing obligations and timing-partition coverage |
| HT2 | An uncertainty-aware timing oracle reduces unsupported boundary verdicts | Naive point-threshold oracle | False-verdict and INCONCLUSIVE rates against controlled truth |
| HT3 | Timing-boundary and timing-mutant refinement improves held-out timing-fault detection | B2-T versus B3 | Held-out timing-fault detection-rate difference |

H4 and H5 are conditional research extensions. Failure to obtain representative
calibration or sufficient fault instances is a reportable result, not permission
to weaken the gate.

## Publication units

1. methodology and formal semantics;
2. ARINC 615A CRS/EFSM/VCS construction study;
3. deterministic timed-conformance and measurement-uncertainty study;
4. finite-fault-domain adequacy experiment;
5. optional calibrated-evidence and diagnosis study;
6. second-protocol replication.

Each unit must distinguish planned methods from observed results and preserve
negative evidence.

---

## 中文版

### 目标与研究问题

研究目标是评价一条可审计测试—分析流程能否产生有用、有边界且可复现的 ARINC 615A 离散与时序符合性证据，并改善追踪、故障检测、诊断和发布决策。RQ1–RQ6 继续覆盖导出、覆盖、有限充分性、证据解释、诊断和可迁移性；RQ2 的模型对象升级为带时钟 EFSM 和时序义务目录。

### 研究阶段

1. R0：冻结 RB-2026-001-v4.2，建立变更、风险和主张控制。
2. R1：固定标准、角色、服务、观测边界并双人提取 CRS。
3. R2：建立带时钟 EFSM；追踪状态、转移、时钟守卫和复位；导出离散及过早/标称/边界/过晚/无响应用例；独立评审稳健时序 oracle 和误差预算。
4. R3：冻结工具、IUT、环境、时钟和日志，执行基础 VCS，并用开发/留出离散与时序故障评价有限充分性。
5. R4：分析重复运行依赖、校准和诊断；条件不足时停留在 T2。
6. R5：用具有不同状态、时序或传输特性的第二协议复现。

### 预注册假设

除原 H1–H5 外，HT1 比较无时钟 B2-U 与带时钟 B2-T 的义务发现能力；HT2 比较误差感知 oracle 与朴素点阈值的错误判定；HT3 检验时序边界和时序变异改进是否提高留出时序故障检测率。所有否定和不完整结果均为有效研究结果，不得通过事后放宽门禁消除。
