# Academic Thesis Outline — ARINC 615A / 665 Conformance Verification  
*(Engineer’s perspective — **not** a Master’s graduation thesis)*

Status: **v1.2** — confirmed: academic thesis from an engineer’s perspective.  
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

> How can a **controllable, dual-role (DLS/THW) simulation environment**, grounded in TFTP and ARINC 615A (plus minimal 665 load packaging), systematically expose **protocol-level** conformant and non-conformant behavior—beyond project-specific ICD spot checks?

**Claim to defend:**  
A role-switchable simulator plus an explicit test-point catalog and mutation-style negative cases constitutes a reusable **conformance verification method**, not merely a one-sided loader or target stub.

---

## Recommended structure (academic paper / monograph style)

Length is flexible (e.g. long paper ~15–40 pages, or short monograph). Prefer **tight argument** over chapter padding.

### Abstract
- Problem: load/download verification often stays at program ICD level.  
- Method: dual-role simulation + 615A session model + minimal 665 codec + Pass/Fail catalog.  
- Results: loopback + mutation experiments (optional HW/simulator cross-check).  
- Contribution: architecture + catalog + empirical evidence.

### 1. Introduction
1.1 Engineering context: why standardized data load matters in civil avionics  
1.2 Gap: ICD/functional tests vs **protocol conformance**  
1.3 Research question and scope (615A focus; 665 minimal; network/TFTP path only)  
1.4 Contributions (3–4 bullets)  
1.5 Paper organization  

### 2. Background and Related Work
2.1 Protocol stack: Ethernet/AFDX context → UDP → TFTP → 615A → 665 (comparison, not encyclopedia)  
2.2 ARINC 615A operations and session model (UPLOAD/DOWNLOAD; virtual files; status)  
2.3 ARINC 665 LSAP essentials (only fields needed for oracles)  
2.4 Conformance / interoperability testing concepts  
2.5 Related tools and prior art; positioning of this work  

### 3. Conformance Requirements Model
*(Academic “what must be true,” not a company 需求文档 dump)*  
3.1 Roles and use cases (DLS-mode, THW-mode, self-test)  
3.2 Requirement domains (session, options, list transfer, data, status, 665 checks, errors, timing)  
3.3 Test-point formalism: precondition / stimulus / expected / verdict / standard reference  
3.4 Scope boundaries and non-goals  

### 4. Method and System Design
4.1 Method overview: dual-role simulation as the experimental instrument  
4.2 Layered architecture (I/O → TFTP → 615A → 665 → scenario engine → verdict/report)  
4.3 Role Controller and role-agnostic protocol core *(central design contribution)*  
4.4 Fault injection and oracle design  
4.5 Implementation notes (prototype language, interfaces) — keep subordinate to method  

### 5. Experiments and Results
5.1 Setup: loopback topology; metrics (verdict accuracy, coverage of catalog)  
5.2 Nominal scenarios (both role directions)  
5.3 Mutation / negative scenarios (e.g. bad check value, wrong block rollover, ignored blksize, missing status)  
5.4 Optional external peer (loader simulator / LRU) if available — clearly labeled as supplementary  
5.5 Threats to validity  

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
- Condensed test-point tables  
- Annotated capture fragments  
- Minimal algorithm / state-machine figures  

---

## Contributions (draft — refine after experiments)

1. **Problem framing:** distinguish protocol conformance verification from program ICD testing for 615A-class load paths.  
2. **Method:** dual-role (DLS/THW) simulation with a shared, role-agnostic TFTP/615A core.  
3. **Artifact:** executable prototype + explicit test-point / oracle model (incl. minimal 665 checks).  
4. **Evidence:** loopback and mutation results showing detection of known non-conformances.

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

| Thesis section | Engineering work |
|---|---|
| §2–3 | Phase 0 study + test-point catalog |
| §4 | Architecture + Role Controller + prototype |
| §5–6 | Validation tiers (loopback, mutation, optional HW) |

The **software remains the experimental platform** of the academic thesis—not the thesis’s only purpose as a “graduation deliverable.”

---

## Open choices (confirm when ready)

1. **Target length / venue:** standalone technical thesis, journal/conference paper, or internal academic-style report?  
2. **Depth of 665:** keep “minimal support” in title, or demote 665 entirely to an implementation subsection?  
3. **FIND / INFORMATION:** in experimental scope, or explicitly out of scope?

*Next step when you confirm (1)–(3): freeze abstract + contribution bullets, then draft §1 Introduction.*
