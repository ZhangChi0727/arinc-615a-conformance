# Experiment Plan

| Field | Value |
|---|---|
| **Plan ID** | EXP-PLAN-2026-001 |
| **Version** | 1.0 |
| **Status** | Baseline protocol; individual experiments require registration |
| **Governing report** | RR-2026-001 v4.1 §§8–12 |

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
- planned statistical model and uncertainty interval;
- deviation handling and applicable gates.

## Core studies

### EXP-001 — Requirement extraction reproducibility

Two reviewers independently extract and classify requirements. Report agreement
before adjudication, disagreement types, adjudication effort, and final CRS
changes. Do not use agreement alone as evidence of semantic correctness.

### EXP-002 — Coverage and derivation comparison

Compare B0–B3 from RR-2026-001:

- B0 existing engineering/ICD set;
- B1 traceability only;
- B2 requirement plus EFSM obligation coverage;
- B3 B2 refined using development mutants.

Primary outcomes are obligation coverage and held-out detection. Report VCS
size, derivation effort, execution time, review findings, and rework.

### EXP-003 — Finite-fault-domain adequacy

Pre-register fault operators, classify invalid/equivalent mutants, keep
development and held-out instances separate, and report every survivor.
The evaluation population is \(\mathcal M_{\mathrm{eval}}\); no result is
generalized beyond it without a separately justified sampling model.

### EXP-004 — Operational repeatability

For selected obligations, execute valid repeated runs under a declared regime.
Report \(c_j/n_j\), exact intervals, INCONCLUSIVE/ERROR counts, order effects,
clustering checks, and reset integrity. This study estimates operational PASS
probability, not conformance belief.

### EXP-005 — Calibration and probabilistic interpretation

Use independently adjudicated conforming and held-out nonconforming instances
to estimate true-PASS and false-PASS rates. Propagate parameter uncertainty and
evaluate prior sensitivity. If calibration is unrepresentative or too small,
stop at T2.

### EXP-006 — Failure diagnosis

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
