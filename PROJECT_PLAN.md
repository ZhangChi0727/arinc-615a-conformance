# Integrated Project Plan

| Field | Value |
|---|---|
| **Plan ID** | IPP-2026-001 |
| **Version** | 1.0 |
| **Status** | Active |
| **Baseline** | RB-2026-001-v4.1 |
| **Planning horizon** | Baseline freeze through second-protocol replication |

## 1. Mission

Produce, evaluate, and operationalize a Test-and-Analysis methodology that
supports bounded, reproducible ARINC 615A conformance decisions and generates
credible scientific and engineering evidence.

## 2. Success criteria

The program succeeds when:

1. the applicable CRS and observation boundary are controlled;
2. every applicable verification obligation is traceable to reviewed VCs;
3. the instrument produces reproducible, provenance-complete evidence;
4. held-out faults provide an honest measure of bounded detection adequacy;
5. probabilistic or diagnostic claims are released only after their gates pass;
6. scientific results and engineering releases use the same versioned artifacts;
7. transferability wording matches the presence or absence of replication.

## 3. Workstreams

| Workstream | Owner role | Canonical plan | Primary outputs |
|---|---|---|---|
| W0 Governance | Project/research lead | `docs/BASELINE.md`, `docs/management/` | baseline, decisions, risks, gates |
| W1 Requirements | Requirements researchers | `docs/research/RESEARCH_PLAN.md` | applicability, CRS, obligation model |
| W2 Modeling and VCS | Method/test researchers | research + architecture docs | EFSM, traces, TPs, VCs, oracles |
| W3 Instrument | Engineering lead | `docs/engineering/IMPLEMENTATION_PLAN.md` | simulator, engine, evidence writer |
| W4 Experiments | Experiment/statistics lead | `docs/research/EXPERIMENT_PLAN.md` | registrations, raw/derived evidence |
| W5 Analysis | Research team | report §§6–8 | coverage, mutation, calibration, diagnosis |
| W6 Publication | Research lead | `RESEARCH_OUTLINE.md`, `thesis/` | papers, thesis, replication report |
| W7 Tutorial | Technical educator | `tutorial/`, `docs/study/` | reproducible learning/runbooks |

Roles may be held by the same person, but independent review is required where
the baseline specifies it.

## 4. Integrated roadmap

| Stage | Main work | Exit products | Required decisions |
|---|---|---|---|
| P0 Baseline | Freeze method and repository control | RB-2026-001-v4.1, plans, risks | Baseline accepted |
| P1 Scope/CRS | Applicability, observation boundary, dual extraction | CRS, adjudication, source manifest | RG0, RG1, G0 |
| P2 Model/VCS | EFSM, traces, obligations, cases, oracles | Model package, base VCS | RG2, RG3, G1; T0 |
| P3 Instrument | Runner, roles, reset, logging, evidence | Reproducible end-to-end run | RG4, G2 readiness |
| P4 T1 execution | Execute controlled VCS | Raw evidence, verdict report | G2; T1 result |
| P5 T2 adequacy | Development and held-out fault study | Mutation and held-out report | RG5, G3; T2 result |
| P6 Optional T3/diagnosis | Calibration, dependence, classifiers | Sensitivity and diagnostic reports | G4–G6 |
| P7 Transfer | Second protocol instance | Replication and comparative analysis | G7 |

Stages are evidence-driven, not calendar-driven. Parallel implementation is
allowed only when it does not pre-empt an unresolved upstream gate.

## 5. Near-term execution backlog

### Baseline release

- approve and commit the baseline manifest and control documents;
- update the active PR to replace the superseded v3.0 report;
- create the recommended baseline tag after merge;
- archive or label historical theory proposals as superseded.

### First research increment

- create the applicability-declaration schema;
- create the CRS item schema without proprietary text fields;
- define dual-review extraction instructions and adjudication form;
- register EXP-001;
- conduct RG0 scope review.

### First engineering increment

- add schema validation and example objects;
- preserve the existing 48-test green baseline;
- document current TFTP behavior and gaps against E1;
- add an evidence-manifest schema before new session implementation.

## 6. Management cadence

| Cadence | Activity | Output |
|---|---|---|
| Weekly | Workstream review | completed work, blockers, next evidence |
| Per PR | Repository, engineering, methodology, and/or research review | explicit outcome and gate impact |
| Per gate | Independent gate review | signed findings and decision |
| Monthly | Risk and scope review | updated risk register and residual risks |
| Per experiment | Registration then result review | deviations and reproducibility record |
| Per release | Claim/evidence audit | approved wording and manifest |

## 7. Definition of done

A work item is done only when:

- its artifact exists at the controlled path;
- acceptance criteria and relevant tests pass;
- versions and upstream/downstream trace links are recorded;
- review findings are closed or explicitly accepted;
- risks and deviations are updated;
- claim wording remains within the achieved assurance tier.

## 8. Dependencies and constraints

- Access to controlled ARINC 615A material is required for P1–P2.
- Public repository artifacts must not reproduce proprietary clauses.
- T3 depends on representative calibration instances and may legitimately remain
  unavailable.
- External peer or hardware access improves external validity but does not
  replace controlled loopback, oracle, and provenance checks.
- P7 needs a separately selected and resourced second protocol.
