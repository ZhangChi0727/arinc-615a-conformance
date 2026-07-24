# Proposal — PR #4 Methodology Reframing

**Status:** Executed (branch `feature/pr0004-methodology-reframing`)  
**Scope:** Test-and-Analysis reframing of RR-2026-001; terminology alignment; theoretical mapping; numerical examples; FMEA dictionary; multi-protocol positioning.

---

## Objective

Reframe RR-2026-001 from “verification case generation” to a complete **conformance verification methodology** comprising two complementary DO-178C §6.4 methods:

- **Testing** (§4–5): Requirements-Based Testing
- **Analysis** (§6): Probabilistic Confidence Analysis

Additionally: expand terminology, add theory→method mapping, provide numerical examples, populate FMEA dictionary template, position for multi-protocol generalization.

---

## Change groups (executed)

| Group | Description | Status |
|-------|-------------|--------|
| A | Terminology expansion (+18 entries in `docs/terminology.md`) | ✅ Done |
| B1–B2 | Title + abstract rewrite (EN + ZH) | ✅ Done |
| B3 | New §2.6 Theoretical Foundation → Method Mapping | ✅ Done |
| B4 | New §4.8 Human Intervention vs. Automation | ✅ Done |
| B5 | New §5.5 Verification Method Classification (Test vs. Analysis) | ✅ Done |
| B6 | New §6.10 Numerical Toy Example | ✅ Done |
| B7 | §6.7 FMEA ↔ Mutation Mapping Dictionary (template) | ✅ Done |
| B8 | §7 Positioning table + novelty update (3 new rows + item 7) | ✅ Done |
| B9 | §8 Open questions 9–11 (multi-protocol generalization) | ✅ Done |
| B10 | §9 Restructured next steps (PR#4 / PR#5 / future) | ✅ Done |
| B11 | EN/ZH synchronization | ✅ Done |
| D | Design decisions DD-007/008/009 | ✅ Done |
| E | This proposal doc update | ✅ Done |
| F | Thesis outline update | ✅ Done |
| G | PR #5 proposal creation | ✅ Done |

---

## Deferred to PR #5 (engineering)

| Item | Notes |
|------|--------|
| Emission probability calibration | Calibrate \(\alpha,\beta\) from experimental data |
| EFSM formal model for 615A | Make L2/L3 coverage operational |
| FMEA dictionary population | Complete per-layer (template provided in §6.7) |
| Self-loop data collection | Implement in simulator |
| Confidence metric computation | From prototype execution data |
| VC→simulator→coverage→mutation pipeline | Integration |

## Out of scope (future research)

- ARINC 825 (CAN bus) second protocol instance
- Timing coverage criteria (L7) for real-time protocols
- Stateless/message-based protocol adaptation
- Protocol Evidence Graph formalization (TD-01)

---

## Theory debt register (updated)

| ID | Temporary working definition | Intended refinement | Status |
|----|------------------------------|---------------------|--------|
| TD-01 | Layered DTMC as interpretation model | Evidence-graph formalization; clarify non-kernel epistemic labels | **Deferred** (future research; Analysis math) |
| TD-02 | HMM latent dynamics vs protocol graph | Separate kernels; relate \(Z_k\) path to visited edges | Open |
| TD-03 | Conditional path confidence \(P(v_i\|v_{i-1})\) | Fully specify estimation from experiments | Open (PR #5 data) |
| TD-04 | Unverified \(\theta=\bot\) reporting policy | Choose and freeze P3a vs P3b | Open |

---

## Key decisions made

- **DD-007:** Test-and-Analysis dual-path framing (DO-178C §6.4)
- **DD-008:** ARINC 615A sole instance; multi-protocol = future research
- **DD-009:** PR #4 (theory) / PR #5 (engineering) separation

---

## Merge dependency

PR #2 and PR #3 must be merged before PR #4 (satisfied).
