# Proposal — PR #4 Methodology Refinement

**Status:** Backlog (after PR #2 Must merge)  
**Scope:** Mathematical / methodological formalization only — **no** repository restructuring.

---

## Objective

Resolve **theory debt** left explicit in RR-2026-001 v2.1:

- Keep advancing quantified confidence and diagnosis;
- Reposition (not necessarily delete) the DTMC as an interpretation model vs. a Protocol Evidence Graph / labeled transition graph;
- Unify emission probability, EFSM coverage artifacts, FMEA↔mutation maps, numerical examples, EN/ZH parity.

---

## In scope (Should from Reply.md)

| Item | Notes |
|------|--------|
| DTMC repositioning | Interpretation model → optional Protocol Evidence Graph abstraction |
| Protocol Evidence Graph | Labeled graph; avoid requiring stochastic kernels for epistemic labels |
| Emission probability unification | Calibrate \(\alpha,\beta\); document estimation |
| EFSM for 615A session | Make L2/L3 coverage operational beyond TFTP-only sketch |
| FMEA ↔ mutation mapping | Replace informal “≈ DC” with explicit dictionary |
| Numerical toy examples | Worked \(\theta\), CI, \(C_{wl}\), \(C_{path}\) |
| EN/ZH synchronization | After each math edit |

## Out of scope

- Repository terminology/architecture/review process (PR #3)
- Software implementation of session layer (separate engineering PRs)
- Changing research questions wholesale

---

## Theory debt register (seed)

| ID | Temporary working definition | Intended refinement |
|----|------------------------------|---------------------|
| TD-01 | Layered DTMC as interpretation model | Evidence-graph formalization; clarify non-kernel epistemic labels |
| TD-02 | HMM latent dynamics vs protocol graph | Separate kernels; relate \(Z_k\) path to visited edges |
| TD-03 | Conditional path confidence \(P(v_i\|v_{i-1})\) | Fully specify estimation from experiments |
| TD-04 | Unverified \(\theta=\bot\) reporting policy | Choose and freeze P3a vs P3b |

---

## Merge dependency

Do **not** start implementation work for PR #4 until PR #2 Must items are on `main` (or explicitly waived).
