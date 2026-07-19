# Research Outline — Track B (Academic Thesis, Engineer’s Perspective)

Status: **v0.1**  
Related: [`TRACKS.md`](TRACKS.md) · [`PROJECT_PLAN.md`](PROJECT_PLAN.md) · [`docs/02_thesis_outline.md`](docs/02_thesis_outline.md)

> This is **not** a Master’s graduation thesis outline.  
> It is an **academic thesis** written from an engineer’s perspective: research question, method, artifact as experimental platform, evidence, discussion.

---

## 1. Research question

> How can a **controllable, dual-role (DLS/THW) simulation environment**, grounded in TFTP and ARINC 615A (with minimal ARINC 665 packaging support), systematically expose **protocol-level** conformant and non-conformant behavior—beyond project-specific ICD spot checks?

---

## 2. Claim to defend

A role-switchable simulator, an explicit test-point/oracle model, and mutation-style negative cases form a reusable **conformance verification method** for 615A-class load paths—not merely a one-sided loader or target stub.

---

## 3. Contributions (draft)

1. **Framing** — Protocol conformance vs program ICD testing for data-load paths.  
2. **Method** — Dual-role simulation with a shared, role-agnostic TFTP/615A core.  
3. **Artifact** — Executable prototype + oracle/test-point model (minimal 665).  
4. **Evidence** — Loopback + mutation results demonstrating detection of known faults.

---

## 4. Paper / monograph structure

| § | Title | Purpose |
|---|---|---|
| | Abstract | Problem, method, results, contribution |
| 1 | Introduction | Context, gap, RQ, scope, contributions |
| 2 | Background & related work | Stack, 615A, 665 (minimal), conformance theory, prior tools |
| 3 | Conformance requirements model | Domains, TP formalism, boundaries |
| 4 | Method & system design | Dual-role method, architecture, Role Controller, oracles |
| 5 | Experiments & results | Setup, nominal, mutation, optional external peer, threats to validity |
| 6 | Discussion | Implications, complementarity to ICD testing, limits |
| 7 | Conclusion | Answer RQ; future work |
| | References / optional appendix | Standards, captures, condensed TP tables |

Detail and confidentiality notes: `docs/02_thesis_outline.md`.

---

## 5. Thesis workstream (writing milestones)

| ID | Milestone | Done when |
|---|---|---|
| **T0** | Freeze RQ + title + scope bullets | This file + outline agree |
| **T1** | Related-work notes (annotated bib) | `thesis/notes/related_work.md` |
| **T2** | Requirements model draft (§3) | Formal TP table in `thesis/` or `docs/requirements/` |
| **T3** | Method section draft (§4) | Architecture + Role Controller argued |
| **T4** | Experiment plan | What will be measured before coding finishes |
| **T5** | Results write-up (§5) | Uses Track A C7–C8 outputs |
| **T6** | Discussion + conclusion | Limits & future work honest |
| **T7** | Full draft polish | Generic names only; refs consistent |

---

## 6. What thesis work is *not*

- Filling school 开题/答辩 templates or page quotas.  
- Pasting company KPI forms or internal ICD text.  
- Treating “tool finished” as automatically “thesis finished” without experiments/discussion.  
- Career mapping (e.g. automotive J1939) inside the thesis body.

---

## 7. Bridge from Code track (evidence pipeline)

```
Track A (C7 loopback, C8 mutation)
        → artifacts/reports/*.json
        → thesis/figures/ + §5 tables
        → discussion in §6
```

Thesis may start T0–T4 **before** code MVP; T5 **requires** experimental runs.

---

## 8. Open choices (confirm soon)

1. **Venue / length** — long standalone thesis, journal/conference paper, or internal academic-style report?  
2. **665 visibility** — keep in title as “minimal support,” or demote to a subsection?  
3. **FIND / INFORMATION** — in experimental scope, or explicit future work?

---

## 9. Next thesis action

1. Confirm the three open choices above.  
2. Draft Abstract + §1 Introduction skeleton under `thesis/drafts/`.  
3. Keep implementation chatter in `PROJECT_PLAN.md` / issues — not in thesis prose.
