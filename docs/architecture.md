# Research and Verification Architecture

| Field | Value |
|---|---|
| **Version** | 2.1 |
| **Status** | Baseline-aligned |
| **Governing method** | RB-2026-001-v4.2 |

## End-to-end control flow

```text
Standard + applicability + observation boundary
                     |
                     v
          CRS and obligation model
                     |
          +----------+----------+
          |                     |
          v                     v
 Clock-augmented EFSM    Test Purposes / VCs
          |                     |
          +----------+----------+
                     v
             Test execution path
        configuration -> stimulus -> oracle
                     |
                     v
  verdicts + timestamped traces + measurements
                     |
                     v
              Analysis path
 traceability | timed coverage | faults | uncertainty | diagnosis
                     |
                     v
          scoped assurance argument
                     |
                     v
           engineering/research decision
```

Review and Inspection gates act across the flow. They do not replace dynamic
execution or quantitative analysis.

## Controlled objects

| Object | Canonical form | Owner |
|---|---|---|
| Applicability | PICS-like declaration | Requirements |
| CRS | Versioned requirement items and source hashes | Requirements |
| Protocol model | Clock-augmented observable EFSM/timed IOLTS | Modeling |
| Traceability | \(\rho_{RT}\), \(\rho_{TV}\), model-target relations | Method |
| Verification case | Preconditions, stimulus, robust oracle, timing/error schema, reset, evidence schema | Test |
| Evidence | Immutable run and analysis datasets | Engineering/experiment |
| Inference model | Registered likelihood, calibration, diagnosis model | Analysis |
| Claim | Claim ID, tier, scope, evidence, gate decision | Governance |

## Gates

| Artifact progression | Static gate | Evidence gate |
|---|---|---|
| Scope enters CRS work | RG0 | G0 |
| CRS enters modeling | RG1 | — |
| Model/trace enters case derivation | RG2 | G1 preparation |
| VCs/oracles enter implementation | RG3 | G1 |
| Tool/config enters execution | RG4 | G2 |
| Evidence enters analysis/publication | RG5 | G3–G6 as applicable |
| Claim enters release | RG6 | achieved G0–G7 |

## Base and extended VCS

The base VCS is derived from the controlled applicable standard requirements.
The extended VCS is project-specific and additive. Results, configuration, and
claims for the two sets remain distinguishable. Adding extended cases cannot
repair missing base traceability or silently change the base claim.

## Version spine

Every run and derived result must identify:

\[
(\text{baseline},S,P,O,\text{CRS},G_T,V,\text{IUT},E,\text{clock},\text{tool},\text{experiment}).
\]

The tuple is implemented as manifest identifiers, not inferred from folder
names or the latest Git commit.

## Repository realization

| Architecture layer | Location |
|---|---|
| Baseline/method | `docs/BASELINE.md`, `docs/study/` |
| Research control | `docs/research/` |
| Requirements and traceability | `docs/requirements/`, future `configs/` schemas |
| Model/design | `docs/design/` |
| Instrument | `src/a615a_sim/` |
| Automated checks | `tests/` |
| Experiment evidence | `artifacts/experiments/` or controlled external store |
| Review/change/risk | `docs/review/`, `docs/management/` |
| Publication | `thesis/` |

---

## 中文版

端到端控制流从标准、适用性和观测边界进入 CRS/义务模型，再分流至带时钟可观测 EFSM 与 TP/VC，汇合后执行测试，产生判定、带时戳迹和测量，随后分析追踪、离散/时序覆盖、故障、不确定性和诊断，最后形成范围受限保证论证。评审与检查横跨整个流程。

受控对象包括适用性、CRS、带时钟协议模型、追踪关系、含时序/误差 schema 的 VC、不可变证据、独立注册的推断模型和由门禁控制的主张。每次运行和派生结果必须记录
\((基线,S,P,O,CRS,G_T,V,IUT,E,时钟,工具,实验)\)，不得从目录名或“最新提交”推断版本。
