# Design Decisions

Log of important research/engineering decisions and their rationale.

Append new entries; do not rewrite history—add superseding entries instead.

---

## DD-001 — Verification Point as primary unit

**Decision:** Use *Verification Point* (and verification cases derived from it) as the primary auditable unit linking standards to execution.

**Why:** Auditable traceability for conformance arguments; aligns with requirements-based verification practice and ISO 9646-style derivation.

**Date:** 2026-07

**Status:** Active

---

## DD-002 — Layered quantitative model (as stated in RR-2026-001)

**Decision:** RR-2026-001 introduces a layered quantitative confidence story (reported there using DTMC/HMM vocabulary) on top of the VCS methodology.

**Why:** Move from binary Pass/Fail alone toward scoped assurance metrics and diagnostic hooks.

**Date:** 2026-07

**Status:** Active in research docs; **formalization under methodology review** (see PR #2 review notes). Future PRs may refine mathematical presentation without abandoning the goal of quantified confidence.

---

## DD-003 — Bayesian / evidence-based confidence language

**Decision:** Treat quantitative “confidence” as **epistemic / evidence-based** assurance given tests, not as an unexplained intrinsic randomness of the IUT.

**Why:** Protocol specs are largely deterministic; uncertainty is about our knowledge of the IUT under a fault/observation model.

**Date:** 2026-07

**Status:** Active

---

## DD-004 — Mutation analysis for adequacy

**Decision:** Use mutation / fault injection to support detection-capability claims for the base VCS.

**Why:** Requirement coverage alone does not prove detection power; mutation provides an explicit finite fault model bound.

**Date:** 2026-07

**Status:** Active

---

## DD-005 — Base vs extended VCS separation

**Decision:** Keep a stable, standard-derived **base** VCS separate from project-specific **extended** cases.

**Why:** Preserve a reusable conformance claim while remaining compatible with customer ICD extras.

**Date:** 2026-07

**Status:** Active

---

## DD-006 — Dual-role simulator as instrument, not the claimed innovation

**Decision:** Position the dual-role software as the experimental / engineering instrument; academic novelty centers on the verification method.

**Why:** Matches the project’s academic-thesis framing (engineer perspective).

**Date:** 2026-07

**Status:** Active

---

## DD-007 — Freeze RR-2026-001 v4.1 as the methodology baseline

**Decision:** Adopt `RB-2026-001-v4.1` as the normative research-method
baseline for subsequent requirements, engineering, experiments, analysis, and
publication work.

**Why:** The report now separates analytical objects, bounds every assurance
tier, resolves the blocking probability and fault-domain errors, and defines
operational review/evidence gates.

**Date:** 2026-07-26
**Status:** Active; supersedes any inconsistent methodology language in earlier
outlines and proposals.

---

## DD-008 — Test and Analysis are complementary primary paths

**Decision:** Test produces controlled observations and verdict evidence;
Analysis evaluates coverage, adequacy, uncertainty, and diagnosis. Neither is
treated as sufficient alone.

**Why:** This architecture creates both scientific evaluability and an
engineering feedback loop.

**Date:** 2026-07-26
**Status:** Active

---

## DD-009 — Review and Inspection are cross-cutting gates

**Decision:** Implement RG0–RG6 as independent static controls across the
Test-and-Analysis loop. Demonstration remains optional and cannot replace
detailed protocol evidence.

**Why:** Artifact defects and overstated claims need prevention before they
propagate into execution or release.

**Date:** 2026-07-26
**Status:** Active

---

## DD-010 — Retire DTMC/HMM as baseline conformance machinery

**Decision:** Protocol behavior remains an EFSM/IOLTS; calibrated inference and
diagnosis use separately defined models. DTMC edge labels, weakest-link
“probabilities,” path products, and HMM/Viterbi localization are not baseline
claims.

**Why:** Protocol topology, evidence, and stochastic inference are different
mathematical objects. Temporal models require independently demonstrated state
meaning, identifiability, data sufficiency, and comparative performance.

**Date:** 2026-07-26
**Status:** Active; supersedes DD-002 where it described DTMC/HMM vocabulary as
the active quantitative story.

---

## DD-011 — Gate-earned claim release

**Decision:** All research and engineering claim wording is controlled by
`docs/research/CLAIM_EVIDENCE_MATRIX.md`. T0–T3, diagnosis, engineering
reproducibility, and transferability are promoted only by their required
evidence and gates.

**Why:** Repository progress and passing tests are not substitutes for an
assurance argument.

**Date:** 2026-07-26
**Status:** Active
