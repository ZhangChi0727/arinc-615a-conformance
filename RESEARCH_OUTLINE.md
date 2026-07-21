# Research Outline — Track B (Academic Thesis, Engineer’s Perspective)

Status: **v0.1**  
Related: [`TRACKS.md`](TRACKS.md) · [`PROJECT_PLAN.md`](PROJECT_PLAN.md) · [`docs/02_thesis_outline.md`](docs/02_thesis_outline.md)

> This is **not** a Master’s graduation thesis outline.  
> It is an **academic thesis** written from an engineer’s perspective: research question, method, artifact as experimental platform, evidence, discussion.

---

## 1. Research question

> How can a **project-agnostic conformance verification method**, based on a series of stable test points derived from the ARINC 615A standard, fully prove protocol conformance while remaining compatible with project-specific extended test requirements?

---

## 2. Claim to defend

A project-agnostic conformance verification method, built on a stable set of verification points derived from the ARINC 615A standard, can fully prove protocol conformance when all points pass. This method is compatible with project-specific extended test sets without compromising the base conformance proof. The software architecture (dual-role simulator, L4 engine, etc.) is our implementation vehicle, not the innovation itself.

---

## 3. Contributions (draft)

1. **Method (innovation):** A project-agnostic conformance verification method based on stable verification points derived from the ARINC 615A standard. The base test set fully proves protocol conformance; extended test sets are compatible with specific project ICD test requirements without altering the base proof.
2. **Framing:** Distinguishing protocol conformance verification (standard-derived, project-agnostic) from program ICD testing (project-specific, interface-level).
3. **Artifact (engineering work):** An executable prototype that implements the method — dual-role simulator, L4 engine (selector/injector/verdict), 664 LU data generator. This is our work, not the innovation.
4. **Evidence:** Empirical proof that (a) passing the complete base test set implies protocol conformance, and (b) mutation verification confirms the test set can detect non-conformance.

---

## 4. Paper / monograph structure

| § | Title | Purpose |
|---|---|---|
| | Abstract | Problem, method, results, contribution |
| 1 | Introduction | Context, gap, RQ, scope, contributions |
| 2 | Background & related work | Stack, 615A, 665 (minimal), conformance theory, prior tools |
| 3 | Conformance verification method | Stable verification points (base test set, standard-derived); extended test set (project-specific); VP formalism; conformance proof argument |
| 4 | System design (engineering work) | Dual-role simulator, L4 engine, Role Controller, 664 LU generator — implementation of the method, not the contribution |
| 5 | Experiments & results | Base test set execution (conformance proof), mutation verification (detection proof), extended test set (optional), threats to validity |
| 6 | Discussion | Implications, complementarity to ICD testing, limits |
| 7 | Conclusion | Answer RQ; future work |
| | References / optional appendix | Standards, captures, condensed VP tables |

Detail and confidentiality notes: `docs/02_thesis_outline.md`.

---

## 5. Thesis workstream (writing milestones)

| ID | Milestone | Done when |
|---|---|---|
| **T0** | Freeze RQ + title + scope bullets | This file + outline agree |
| **T1** | Related-work notes (annotated bib) | `thesis/notes/related_work.md` — high-level thesis and docs as research basis |
| **T2** | Requirements model draft (§3) | Formal VP table in `thesis/` or `docs/requirements/` |
| **T3** | Method section draft (§4) | Conformance verification method argued; software architecture described as implementation |
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

## 7. Project workflow and research basis

**Workflow:**
1. **Tutorial** — Study protocols (664, 665, 615A); figure out how to verify conformance; form stable tutorials with test docs. Refer to high-level thesis and docs as research basis.
2. **Software** — Implement the conformance verification tool based on stable tutorials.
3. **Thesis** — Summarize the academic or engineering verification methodology from software engineering practice.

**Research basis:** When collecting and organizing tutorials, refer to high-level thesis and docs (conformance testing theory, protocol verification literature, ARINC standards) as the theoretical foundation. The tutorials bridge between high-level theory and hands-on protocol understanding.

**Evidence pipeline:**
```
High-level thesis/docs → Tutorials (664/665/615A) → Stable test docs
    → Software engineering (C0–C8) → artifacts/reports/*.json
    → Thesis §5 tables/figures → §6 discussion
```

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
