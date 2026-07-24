# Proposal — PR #5 Engineering Implementation & Data Collection

**Status:** Draft (pending PR #4 merge and theory freeze)  
**Scope:** Engineering implementation, experimental data collection, and pipeline integration — **no** theoretical changes.

---

## Objective

Implement the engineering artifacts required to operationalize the frozen theoretical architecture from PR #4. This PR transforms the methodology from a theoretical framework into an executable, data-producing verification pipeline.

**Prerequisite:** PR #4 merged (theory frozen). No changes to §4–5 derivation logic, §6 mathematical framework, or formal definitions.

---

## In scope

| # | Item | Description | Deliverable |
|---|------|-------------|-------------|
| 1 | Per-layer sub-state machine modeling | Complete TFTP (priority), then 615A/UDP/665/664 state machines | State machine specs in `docs/design/` |
| 2 | TFTP EFSM formal model | Operational EFSM for L2/L3 coverage automation | EFSM spec + coverage tool integration |
| 3 | FMEA ↔ mutation dictionary population | Complete per-layer dictionary (template from §6.7) | FMEA tables in `configs/` |
| 4 | Self-loop verification data collection | Implement repeated same-state testing in simulator | Data collection scripts + raw data |
| 5 | Emission probability calibration | Calibrate (α, β) from experimental mutation data | Calibration report |
| 6 | Confidence metric computation | Compute C_protocol, C_path, C vector from prototype data | Computation scripts + results |
| 7 | VC→simulator→coverage→mutation pipeline | End-to-end integration of verification pipeline | Pipeline scripts + CI integration |
| 8 | Viterbi fault localization demo | Inject known faults; demonstrate localization accuracy | Experiment scripts + results |

---

## Out of scope

- Theoretical changes to RR-2026-001 (frozen at PR #4)
- ARINC 825 / multi-protocol instantiation (future research)
- Timing coverage L7 (future research)
- Protocol Evidence Graph formalization TD-01 (future research)
- New verification case derivation methodology changes

---

## Theory debt addressed

| ID | How addressed |
|----|---------------|
| TD-03 | Path confidence P(v_i\|v_{i-1}) estimation from experimental self-loop data |
| TD-04 | θ=⊥ reporting policy: exercised in computation (choose P3a or P3b based on data) |

---

## Dependencies

- PR #4 merged (theory frozen)
- Simulator prototype functional (existing `src/a615a_sim/`)
- VC skill operational (existing `verification-case` skill)

---

## Acceptance criteria

1. All 5 protocol layers have documented sub-state machines
2. TFTP EFSM model produces L2/L3 coverage metrics automatically
3. FMEA dictionary has ≥ 6 entries per layer (matching §6.7 template density)
4. Self-loop data collected for ≥ 3 states with n ≥ 30 each
5. Confidence metrics computed and match §6.10 toy example structure
6. Pipeline runs end-to-end: VC definition → simulation → verdict → coverage → mutation score
7. At least one fault localization demonstration with Viterbi output

---

## Estimated effort

This is primarily an engineering and data-collection PR. Estimated scope: medium-large (multiple subsystems touched, experimental runs required).

---

## Merge strategy

Squash-and-merge into `main` after review. Branch name: `feature/pr0005-engineering-implementation`.
