# Research and Verification Architecture

| Field | Value |
|---|---|
| **Version** | 2.0 |
| **Status** | Baseline-aligned |
| **Governing method** | RB-2026-001-v4.1 |

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
   Observable EFSM       Test Purposes / VCs
          |                     |
          +----------+----------+
                     v
             Test execution path
        configuration -> stimulus -> oracle
                     |
                     v
        verdicts + traces + measurements
                     |
                     v
              Analysis path
 traceability | coverage | faults | uncertainty | diagnosis
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
| Protocol model | Observable EFSM/IOLTS | Modeling |
| Traceability | \(\rho_{RT}\), \(\rho_{TV}\), model-target relations | Method |
| Verification case | Preconditions, stimulus, oracle, reset, evidence schema | Test |
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
(\text{baseline},S,P,O,\text{CRS},G,V,\text{IUT},E,\text{tool},\text{experiment}).
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
