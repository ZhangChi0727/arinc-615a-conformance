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
