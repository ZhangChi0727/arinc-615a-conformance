# Engineering Implementation Plan

| Field | Value |
|---|---|
| **Plan ID** | EIP-2026-001 |
| **Version** | 1.0 |
| **Status** | Approved for staged implementation |
| **Methodology baseline** | RB-2026-001-v4.1 |

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
| Requirement/model schemas | IDs, applicability, obligations, trace relations | `configs/schemas/`, `docs/requirements/` |
| TFTP core | Packets, options, retry, duplicate, timeout, rollover | `src/a615a_sim/tftp/` |
| 615A session | DOWNLOAD/UPLOAD observable state machines | `src/a615a_sim/session/` |
| Minimal data artifacts | Only 665/664 constraints required by the frozen scope | `src/a615a_sim/lsap/` |
| Role controller | DLS/THW mode without duplicating protocol logic | `src/a615a_sim/roles/` |
| Verification engine | Selection, injection, oracle, verdict, reset, run control | `src/a615a_sim/engine/` |
| Evidence writer | Immutable run manifest, traces, measurements, verdicts | `src/a615a_sim/evidence/` |
| Analysis tools | Coverage, mutation, intervals, calibration, diagnosis | `src/a615a_sim/analysis/` |
| CLI/reporting | Reproducible commands and human/machine reports | `src/a615a_sim/cli.py`, `src/a615a_sim/report/` |

## Increment plan

| Increment | Scope | Acceptance evidence | Governing gate |
|---|---|---|---|
| E0 | Baseline schemas and IDs | Schema tests; example CRS/TP/VC round-trip | RG1 |
| E1 | TFTP protocol core hardening | Unit tests for nominal, duplicate, retry, wrong-TID, rollover | Engineering review |
| E2 | Observable 615A EFSM | Reviewed state variables, transitions, guards, trace map | RG2 |
| E3 | VC engine and oracle API | Deterministic examples for all four verdicts; reset tests | RG3 |
| E4 | Dual-role loopback instrument | Reproducible DOWNLOAD/UPLOAD runs and manifest | RG4/G2 |
| E5 | Coverage and mutation pipeline | B0–B3 reports; invalid/equivalent handling; held-out split | G3 |
| E6 | Evidence integrity and reporting | Raw-to-derived reproduction from clean checkout | RG5 |
| E7 | Optional calibration and diagnosis | Held-out evaluation and sensitivity reports | G4–G6 |

## Cross-cutting engineering requirements

- every execution records baseline, CRS, model, VCS, IUT, tool, and environment versions;
- PASS/FAIL/INCONCLUSIVE/ERROR remain distinct end to end;
- oracles are testable independently of the runner;
- reset and isolation are explicit case operations;
- base and extended VCS results are separable;
- raw evidence is append-only; transformations create derived artifacts;
- stochastic tools record seeds and repeated-seed results;
- proprietary standard text never enters public fixtures.

## Quality strategy

| Level | Purpose |
|---|---|
| Unit | Packet, guard, oracle, schema, statistic, and serialization correctness |
| Contract | Stable interfaces between runner, peer, oracle, and evidence writer |
| Integration | DLS↔THW sessions, resets, failures, and evidence provenance |
| Scenario | Requirement-derived VCs and mutation detection |
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
