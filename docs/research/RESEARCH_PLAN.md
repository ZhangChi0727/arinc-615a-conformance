# Research Plan

| Field | Value |
|---|---|
| **Plan ID** | RP-2026-001 |
| **Version** | 1.0 |
| **Status** | Approved for baseline execution |
| **Methodology baseline** | RB-2026-001-v4.1 |
| **Primary report** | [`../study/RR-2026-001_test_analysis_conformance_methodology_en.md`](../study/RR-2026-001_test_analysis_conformance_methodology_en.md) |

## Objective

Evaluate whether an auditable Test-and-Analysis workflow can produce useful,
bounded, and reproducible ARINC 615A conformance evidence while improving
engineering traceability, defect detection, diagnosis, and release decisions.

## Research questions and work packages

| RQ | Work package | Principal output | Decision criterion |
|---|---|---|---|
| RQ1 Derivation | WP1 Scope and CRS | Applicability declaration, CRS, adjudication log | RG0–RG1 passed |
| RQ2 Coverage | WP2 Model and VCS | EFSM, trace relations, coverage matrices, VCs | RG2–RG3 and G1 passed |
| RQ3 Bounded adequacy | WP3 Fault study | Operator catalog, development/held-out mutants, results | G3 passed; held-out rate reported |
| RQ4 Evidence interpretation | WP4 Repeatability and calibration | Run model, intervals, calibration dataset, sensitivity analysis | G4–G5 passed before T3 |
| RQ5 Diagnosis | WP5 Diagnostic evaluation | Features, baseline classifier, held-out metrics | G6 passed before localization claim |
| RQ6 Transferability | WP6 Replication | Second-protocol instance and comparative analysis | G7 passed |

## Research sequence

### Phase R0 — Baseline and registration

- freeze RB-2026-001-v4.1;
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

- construct the observable EFSM;
- establish \(\rho_{RT}\), \(\rho_{TV}\), and requirement/model-target mappings;
- derive positive, negative, boundary, timing, data, and sequence cases;
- independently review oracle logic and reset procedures.

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
| H2 | Development-mutant refinement improves held-out fault detection | B2 versus B3 | Held-out detection-rate difference with interval |
| H3 | Gate reviews reduce downstream escaped defects | Ungated or earlier artifact revisions | Escape rate and rework effort |
| H4 | Calibrated evidence outperforms raw PASS frequency as a probabilistic forecast | Raw-frequency baseline | Brier score/log loss on held-out instances |
| H5 | Feature-based diagnosis outperforms severity-only ranking | FMEA severity baseline | Macro F1, Top-3 recall, abstention curve |

H4 and H5 are conditional research extensions. Failure to obtain representative
calibration or sufficient fault instances is a reportable result, not permission
to weaken the gate.

## Publication units

1. methodology and formal semantics;
2. ARINC 615A CRS/EFSM/VCS construction study;
3. finite-fault-domain adequacy experiment;
4. optional calibrated-evidence and diagnosis study;
5. second-protocol replication.

Each unit must distinguish planned methods from observed results and preserve
negative evidence.
