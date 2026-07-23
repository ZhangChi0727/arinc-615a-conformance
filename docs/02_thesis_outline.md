# Academic Thesis Outline — ARINC 615A / 665 Conformance Verification  
*(Engineer’s perspective — **not** a Master’s graduation thesis)*

Status: **v1.3** — confirmed: academic thesis from an engineer’s perspective; probabilistic extension added.  
**Repo pointers:** research workstream → [`RESEARCH_OUTLINE.md`](../RESEARCH_OUTLINE.md); code vs thesis split → [`TRACKS.md`](../TRACKS.md); engineering milestones → [`PROJECT_PLAN.md`](../PROJECT_PLAN.md).

---

## What this document is (and is not)

| Is | Is not |
|---|---|
| Academic argument: problem → related work → method → system → experiments → discussion | School-templated 开题 / 答辩章节凑页数 |
| Engineer’s viewpoint: implementable architecture, test oracles, validation evidence | Pure theory without a working artifact |
| Cite public standards (ARINC, RFCs) and literature | Dump of company KPI forms or internal ICD text |
| Dual-role conformance tool as the **research object** | “I completed my probation tasks” narrative |

Company deliverables (需求文档, 测试指南, etc.) may **reuse** the same technical content, but they do **not** dictate chapter structure.

**Confidentiality:** use generic terms in the thesis (DLS, THW, member LRU). Keep OHMS/DCAS/IDU names in private notes only.

---

## Working titles

**English:**  
*A Dual-Role Simulation Approach to Conformance Verification of the ARINC 615A Data Load Protocol (with Minimal ARINC 665 Support)*

**Chinese:**  
*面向 ARINC 615A 数据加载协议符合性验证的双角色仿真方法（含 ARINC 665 最小支持）*

---

## Core research question

> How can a **project-agnostic conformance verification method**, based on a series of stable test points derived from the ARINC 615A standard, fully prove protocol conformance while remaining compatible with project-specific extended test requirements?

**Claim to defend:**  
A project-agnostic conformance verification method, built on a stable set of verification points derived from the ARINC 615A standard, can fully prove protocol conformance when all points pass. This method is compatible with project-specific extended test sets without compromising the base conformance proof. The software architecture (dual-role simulator, L4 engine, etc.) is our implementation vehicle, not the innovation itself.

---

## Recommended structure (academic paper / monograph style)

Length is flexible (e.g. long paper ~15–40 pages, or short monograph). Prefer **tight argument** over chapter padding.

### Abstract
- Problem: load/download verification often stays at program ICD level; no project-agnostic method exists to fully prove 615A protocol conformance.  
- Method: a conformance verification method based on stable verification points (base test set, standard-derived) with compatibility for project-specific extended test sets; enhanced with layered DTMC/HMM-based confidence quantification.  
- Results: base test set execution proves conformance; mutation verification proves detection; probabilistic model quantifies confidence and enables fault localization.  
- Contribution: the verification method itself (project-agnostic, stable test points, extensible, quantitatively confident, diagnostically capable); the software prototype is engineering work that implements the method.

### 1. Introduction
1.1 Engineering context: why standardized data load matters in civil avionics  
1.2 Gap: ICD/functional tests vs **protocol conformance**  
1.3 Research question and scope (615A focus; 665 minimal; network/TFTP path only)  
1.4 Contributions (3–4 bullets)  
1.5 Paper organization  

### 2. Background and Related Work
*(Grounded in tutorial-driven protocol study; high-level thesis and docs as research basis)*  
2.1 Protocol stack: Ethernet/AFDX context → UDP → TFTP → 615A → 665 (comparison, not encyclopedia)  
2.2 ARINC 615A operations and session model (UPLOAD/DOWNLOAD; virtual files; status)  
2.3 ARINC 665 LSAP essentials (only fields needed for oracles)  
2.4 ARINC 664 Loadable Unit data format (as input to 615A transfers)  
2.5 Conformance / interoperability testing concepts  
2.6 Related tools and prior art; positioning of this work  
2.7 High-level thesis and docs as research basis for tutorial-driven protocol study  

### 3. Conformance Verification Method
*(The innovation — a project-agnostic method, not a software architecture description)*  
3.1 Method overview: stable verification points derived from the ARINC 615A standard; base test set proves conformance; extended test set accommodates project-specific requirements  
3.2 Verification-point formalism: precondition / stimulus / expected / verdict / standard reference  
3.3 **Base test set** — stable, project-agnostic, derived from 615A standard (the conformance proof)  
3.4 **Extended test set** — project-specific, compatible with specific project ICD test requirements; varies by client (does not alter base proof)  
3.5 Conformance proof argument: why passing all base verification points implies protocol conformance  
3.6 **Probabilistic confidence quantification** — layered DTMC/HMM model; verification confidence semantics; conservative parameter estimation from self-loop and mutation data  
3.7 **FMEA/FMEDA integration** — per-transition failure mode catalog; diagnostic coverage; Viterbi-based fault localization on verification failure  
3.8 Scope boundaries and non-goals

### 4. System Design (Engineering Work)
*(How we implement the method — not the contribution itself)*  
4.1 Implementation overview: dual-role simulator as the experimental instrument  
4.2 Layered architecture (I/O → TFTP → 615A → 665 → L4 engine → verdict/report)  
4.3 Role Controller and role-agnostic protocol core  
4.4 L4 engine decomposition — selector → injector → verdict  
4.5 664 LU data generator — produces valid ARINC 664 load units as test input  
4.6 Fault injection and oracle design  
4.7 Implementation notes (prototype language, interfaces) — subordinate to the method  

### 5. Experiments and Results
5.1 Setup: loopback topology; metrics (verdict accuracy, coverage of base test set)  
5.2 **Base test set execution** — all nominal scenarios (both role directions); proves conformance if all pass  
5.3 **Mutation verification** — inject faults (bad check value, wrong block rollover, ignored blksize, missing status); proves detection capability  
5.4 **Confidence metric computation** — per-layer confidence vector, path-level confidence, weakest-link lower bound from self-loop and mutation data  
5.5 **Fault localization demonstration** — inject known fault, observe Viterbi localization accuracy vs. FMEA prediction  
5.6 **Extended test set** (optional) — project-specific scenarios if client ICD available  
5.7 Optional external peer (loader simulator / LRU) if available — clearly labeled as supplementary  
5.8 Threats to validity  

### 6. Discussion
6.1 What the results imply for protocol-level V&V practice  
6.2 Relation to project-specific ICD testing (complementary, not replacement)  
6.3 Limitations (minimal 665; timing precision of high-level prototype; access to peers)  
6.4 Transferable ideas (layered oracles, dual-role peers) — brief, no career digression  

### 7. Conclusion
- Answer the research question  
- Restate contributions  
- Future work: deeper FIND/INFORMATION, broader 665, native timing path, automation/CI  

### References
RFCs, ARINC 615A/665 (public), TFTP/loader literature, conformance-testing methodology papers.

### Appendix (optional)
- Condensed verification-point tables  
- Annotated capture fragments  
- Minimal algorithm / state-machine figures  

---

## Contributions (draft — refine after experiments)

1. **Method (innovation):** A project-agnostic conformance verification method based on stable verification points derived from the ARINC 615A standard. The base test set fully proves protocol conformance; extended test sets accommodate project-specific requirements without altering the base proof.  
2. **Framing:** Distinguishing protocol conformance verification (standard-derived, project-agnostic) from program ICD testing (project-specific, interface-level).  
3. **Quantification (innovation):** A probabilistic confidence model based on layered DTMC/HMM with verification-confidence semantics, providing quantified conformance evidence and FMEA/FMEDA-integrated fault localization via Viterbi inference.  
4. **Artifact (engineering work):** An executable prototype that implements the method — dual-role simulator, L4 engine (selector/injector/verdict), 664 LU data generator. This is our work, not the innovation.  
5. **Evidence:** Empirical proof that (a) passing the complete base test set implies protocol conformance, (b) mutation verification confirms detection capability, and (c) confidence metrics quantify the degree of assurance.

---

## What changed vs the previous (Master’s) outline

| Previous (discarded framing) | Now |
|---|---|
| 工程硕士 chapters, page quotas, 开题/答辩 | Academic sections: RQ → method → experiments |
| KPI docs as primary chapter drivers | Technical argument first; company docs are side products |
| Long “详细设计与实现” school chapter | Design subordinate to **method**; implementation supports reproducibility |
| Heavy school template placeholders | Flexible length; publishable skeleton |

---

## Alignment with the software project (still valid)

**Project workflow:** Tutorial (664/665/615A study) → Software engineering → Thesis (methodology summary)

| Thesis section | Engineering work |
|---|---|
| §2 | Tutorial-driven protocol study (grounded in high-level thesis/docs as research basis) |
| §2–3 | Phase 0 study + base/extended test set definitions (the method) |
| §3.6–3.7 | Layered DTMC/HMM model + FMEA table design (the quantification) |
| §4 | Software architecture + prototype (the implementation of the method) |
| §5–6 | Experiments: base test set execution, mutation verification, confidence computation, fault localization (the evidence) |

The **software remains the experimental platform** of the academic thesis—not the thesis’s only purpose as a “graduation deliverable.” The **thesis summarizes** the verification methodology from the software engineering practice.

---

## Open choices (confirm when ready)

1. **Target length / venue:** standalone technical thesis, journal/conference paper, or internal academic-style report?  
2. **Depth of 665:** keep “minimal support” in title, or demote 665 entirely to an implementation subsection?  
3. **FIND / INFORMATION:** in experimental scope, or explicitly out of scope?

*Next step when you confirm (1)–(3): freeze abstract + contribution bullets, then draft §1 Introduction.*
