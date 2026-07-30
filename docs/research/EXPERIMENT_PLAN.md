# Experiment Plan

| Field | Value |
|---|---|
| **Plan ID** | EXP-PLAN-2026-001 |
| **Version** | 1.1 |
| **Status** | Baseline protocol; individual experiments require registration |
| **Governing report** | RR-2026-001 v4.2 §§8–12 |

## Experiment registry

Create one directory per experiment:

```text
artifacts/experiments/EXP-YYYY-NNN/
  registration.yaml
  environment.json
  cases.json
  raw/
  derived/
  scripts/
  results.md
  deviations.md
  review/
```

Large or confidential raw data may be stored outside Git, but its immutable
identifier, checksum, access classification, and retention location must remain
in `registration.yaml`.

## Required registration fields

- experiment ID, owner, date, hypothesis, and RQ;
- baseline, CRS, EFSM, VCS, IUT, tool, and environment versions;
- experimental unit and sampling unit;
- inclusion/exclusion rules for runs and mutants;
- development/held-out split procedure;
- primary and secondary outcomes;
- sample-size or stopping rationale;
- randomization, reset, isolation, and seed policy;
- time source, timestamp locations, resolution, trigger/response pairing,
  clock-reset semantics, and timing-error budget where timing is observed;
- planned statistical model and uncertainty interval;
- deviation handling and applicable gates.

## Core studies

### EXP-001 — Requirement extraction reproducibility

Two reviewers independently extract and classify requirements. Report agreement
before adjudication, disagreement types, adjudication effort, and final CRS
changes. Do not use agreement alone as evidence of semantic correctness.

### EXP-002 — Coverage and derivation comparison

Compare the following baselines from RR-2026-001:

- B0 existing engineering/ICD set;
- B1 traceability only;
- B2-U requirement plus untimed EFSM obligation coverage;
- B2-T B2-U plus clock-augmented EFSM, timing partitions, and robust timing oracle;
- B3 B2-T refined using development mutants.

Primary outcomes are obligation coverage and held-out detection. Report VCS
size, derivation effort, execution time, review findings, and rework.

### EXP-003 — Finite-fault-domain adequacy

Pre-register fault operators, classify invalid/equivalent mutants, keep
development and held-out instances separate, and report every survivor.
The evaluation population is \(\mathcal M_{\mathrm{eval}}\); no result is
generalized beyond it without a separately justified sampling model.

### EXP-004 — Deterministic timed conformance

For each selected timing obligation, register trigger/response/cancellation and
silence semantics, \(L_r,U_r\), units, time source, timestamp chain, clock
resets, and an auditable error budget. Exercise early, nominal, boundary, late,
and no-response partitions as applicable. Compare B2-U with B2-T, evaluate
robust versus naive point-threshold verdicts against controlled timing truth,
and evaluate held-out timing faults. Report every timing
PASS/FAIL/INCONCLUSIVE/ERROR and preserve the observation interval and boundary
margin.

### EXP-005 — Operational repeatability

For selected obligations, execute valid repeated runs under a declared regime.
Report \(c_j/n_j\), exact intervals, INCONCLUSIVE/ERROR counts, order effects,
clustering checks, drift, clock metadata, and reset integrity. For timing
obligations, define success only through the robust timing oracle. This study
estimates operational PASS probability, not conformance belief.

### EXP-006 — Calibration and probabilistic interpretation

Use independently adjudicated conforming and held-out nonconforming instances
to estimate true-PASS and false-PASS rates. Propagate parameter uncertainty and
evaluate prior sensitivity. If calibration is unrepresentative or too small,
stop at T2.

### EXP-007 — Failure diagnosis

Evaluate simple interpretable baselines before temporal models. Split by fault
instance, report macro metrics and abstention, and prohibit HMM use unless the
temporal-state, identifiability, data, and performance conditions in §7.4 hold.

## Analysis controls

- keep exploratory and confirmatory analyses visibly separate;
- calculate intervals for proportions and differences;
- disclose multiple comparisons and class imbalance;
- report missing, excluded, inconclusive, and erroneous observations;
- preserve original held-out outcomes after any VCS revision;
- make each table and figure reproducible from versioned scripts and data.

## Experiment release gate

An experiment result may enter a thesis, paper, or release claim only when:

1. the registration and deviations are complete;
2. raw-to-derived provenance is reproducible;
3. applicable RG5/G4/G5/G6 records are approved;
4. wording matches the achieved assurance tier;
5. negative and inconclusive results remain visible.

---

## 中文版

### 实验注册要求

每项实验都要记录 ID、负责人、日期、假设/RQ、基线/CRS/模型/VCS/IUT/工具/环境版本、实验与抽样单位、纳入排除规则、开发/留出划分、主要结局、停止理由、随机化/重置/隔离/种子、统计模型、偏差和门禁。观察时序时还必须记录时间源、时间戳位置和分辨率、触发/响应配对、时钟复位及误差预算。

### 核心实验

- EXP-001：双人独立需求提取、分歧和裁决；
- EXP-002：比较 B0、B1、B2-U、B2-T 和 B3 的义务覆盖、规模、工时和留出检测；
- EXP-003：预注册有限故障域，分离开发/留出实例并报告全部存活体；
- EXP-004：确定性时序符合性。注册触发/响应/取消/静默语义和 \([L_r,U_r]\)，覆盖过早、标称、边界、过晚及无响应，比较稳健 oracle 与朴素点阈值，并使用留出时序故障；
- EXP-005：运行重复性。报告区间、顺序、聚类、漂移、时钟元数据和重置完整性；
- EXP-006：仅用独立符合/不符合实例进行校准；不足时停留在 T2；
- EXP-007：先评价简单可解释诊断基线，只有满足物理状态含义、可识别性、数据量和性能条件时才使用 HMM。

### 发布门

只有注册和偏差完整、原始到派生证据可复现、适用门禁获批、措辞与层级一致且负向/不确定结果仍可见时，实验结果才能进入论文或发布主张。
