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

## DD-007 — Test-and-Analysis dual-path verification (DO-178C §6.4)

**Decision:** Frame the methodology as two complementary verification methods per DO-178C §6.4: **Testing** (§4–5, Requirements-Based Testing) and **Analysis** (§6, Probabilistic Confidence Analysis). The document title reflects both: “Conformance Verification Methodology … Requirements-Based Testing and Probabilistic Confidence Analysis.”  
**Why:** §4–5 produce evidence (verdicts, traces); §6 interprets that evidence (confidence metrics, fault diagnosis). They are complementary, not sequential. This framing aligns with DO-178C’s recognized verification method taxonomy and clarifies that the methodology is more than “test case generation.”  
**Terminology discipline:** “Testing” (capitalized/compound) = verification method; “unit test” / “integration test” (always qualified) = software development activity.  
**Date:** 2026-07  
**Status:** Active

---

## DD-008 — ARINC 615A as sole protocol instance; multi-protocol as future research

**Decision:** Keep ARINC 615A as the **sole protocol instance** in this work. ARINC 825 (CAN bus), timing coverage (L7), and stateless/message-based protocol adaptation are identified as **future research** (beyond PR #5).  
**Why:** The method is designed to be protocol-agnostic in derivation process, coverage criteria, and analytical framework. However, adding a second instance requires separate theoretical work (timing model, stateless adaptation) that would dilute the current contribution. A single well-developed instance with explicit generalization discussion is stronger for a thesis than two shallow instances.  
**Date:** 2026-07  
**Status:** Active

---

## DD-009 — Executable instantiation scope and PR separation

**Decision:** Separate research/theory (PR #4) from engineering/data (PR #5). PR #4 freezes the theoretical architecture; PR #5 implements: EFSM formal model, emission calibration, self-loop data collection, FMEA dictionary population, and VC→simulator→coverage→mutation pipeline. Protocol Evidence Graph formalization remains theory debt (TD-01), classified as Analysis math work.  
**Why:** Theory must be stable before engineering commits to implementation. Mixing theoretical revisions with engineering changes in one PR creates review complexity and risks circular dependencies.  
**Date:** 2026-07  
**Status:** Active
