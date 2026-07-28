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

## Review cadence

- review at every RG gate and monthly during active implementation;
- escalate Critical-impact risks immediately;
- close a risk only with evidence, not elapsed time;
- record accepted residual risk in the applicable gate decision.
