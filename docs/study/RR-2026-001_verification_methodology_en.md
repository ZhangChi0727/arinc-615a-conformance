# A Methodology for Systematic Verification Case Set Generation from Protocol Requirement Specifications: Theoretical Foundations and Application to ARINC 615A Conformance Verification

**Research Report RR-2026-001**

| | |
|---|---|
| **Version** | 2.0 |
| **Date** | 2026-07-23 |
| **Status** | Reviewed (Phase 1–5 + Probabilistic Extension) |
| **Classification** | Internal — Academic Research |

---

## Abstract

Protocol conformance verification in avionics data loading remains largely ad hoc, relying on project-specific ICD testing without a systematic method to prove protocol-level compliance. This report presents a project-agnostic methodology for generating a verification case set (VCS) from a protocol requirement specification, such that complete coverage of the requirement set constitutes sufficient evidence of conformance. The methodology integrates five established theoretical pillars: (1) the ISO/IEC 9646 conformance testing derivation chain, (2) ETSI test purpose formulation, (3) FSM-based coverage criteria (W/Wp/HSI methods), (4) ioco conformance theory, and (5) mutation-based test adequacy validation. We propose a five-stage derivation process — requirement extraction, test purpose derivation, verification case specification, coverage validation, and adequacy proof — and formalize it with six definitions. The method is instantiated for the ARINC 615A data load protocol, with a base/extended VCS separation mirroring ISO 9646 conformance classes. A structured assurance argument justifies the claim that passing all base verification cases provides high-confidence conformance evidence within a stated fault model.

As a quantitative extension, we introduce a probabilistic conformance confidence model based on layered Discrete-Time Markov Chains (DTMC) and Hidden Markov Models (HMM). The transition matrix entries are interpreted as *verification confidence* (Bayesian epistemic measure), not intrinsic IUT behavioral probabilities. Each protocol layer (UDP, TFTP, 615A, 665, 664) is modeled as an independent sub-state machine with role tagging and block-type segmentation. Parameters are estimated conservatively from self-loop verification data and mutation testing results, avoiding unvalidated independence assumptions. The framework further integrates FMEA/FMEDA for failure mode analysis and Viterbi-based fault localization upon verification failure.

The novelty lies not in any single technique but in their systematic integration into a transferable, auditable method for data load protocol conformance, now enhanced with quantitative confidence assessment and diagnostic capability.

**Keywords:** protocol conformance verification, verification case generation, requirement coverage, ARINC 615A, mutation testing, ISO/IEC 9646, conformance testing methodology, Markov chain, Hidden Markov Model, verification confidence, FMEA, fault localization

---

## 1. Introduction

### 1.1 Problem Context

Civil avionics systems rely on standardized data loading protocols (ARINC 615A, built upon TFTP/UDP/Ethernet) to transfer software and configuration data to line-replaceable units. Current verification practice typically operates at the **program ICD level** — testing interface behaviors specific to a particular aircraft program — without a systematic method to prove **protocol-level conformance** against the ARINC 615A standard itself.

### 1.2 Research Gap

No project-agnostic method exists in the literature that:
- Systematically derives a complete verification case set from ARINC 615A normative requirements
- Provides a formal coverage argument linking requirement coverage to conformance evidence
- Validates detection capability through mutation-based adequacy proof
- Separates base conformance (standard-derived, stable) from extended testing (project-specific)

### 1.3 Research Question

> **RQ:** How can a project-agnostic methodology systematically generate a verification case set (VCS) from a protocol requirement specification such that:
> 1. **Coverage completeness** — every conformance requirement in the base requirement set is addressed by at least one verification case;
> 2. **Conformance proof** — passing all base VCs constitutes sufficient evidence of protocol conformance;
> 3. **Detection capability** — the VCS can detect non-conformance (validated via mutation/fault injection);
> 4. **Extensibility** — project-specific extended VCs can be added without compromising the base conformance proof?

### 1.4 Sub-questions

| ID | Sub-question |
|----|-------------|
| SQ1 | What formal derivation chain maps standard clauses → conformance requirements → test purposes → verification cases? |
| SQ2 | What coverage criteria are necessary and sufficient for protocol conformance? |
| SQ3 | How is the "completeness implies conformance" argument formally justified? |
| SQ4 | How does the base/extended separation relate to conformance classes in ISO 9646? |

### 1.5 Scope

- **In scope:** Methodology and theory; ARINC 615A DOWNLOAD/UPLOAD over TFTP; base + extended VCS design
- **Out of scope:** Software implementation details; FIND/INFORMATION services; full ARINC 665 codec verification

---

## 2. Theoretical Foundations

### 2.1 ISO/IEC 9646 Conformance Testing Methodology

ISO/IEC 9646 (1994) defines the canonical methodology for protocol conformance testing:

| Concept | Definition | Relevance |
|---------|-----------|-----------|
| Conformance requirement | A requirement in the standard that an IUT must satisfy | Derived from ARINC 615A clauses |
| Test purpose | A focused statement of what aspect of conformance a test verifies | Maps 1:1 or 1:N to VCs |
| Abstract Test Suite (ATS) | Complete set of abstract test cases covering all conformance requirements | Our "base VCS" |
| PICS | Declaration of which options/features an implementation supports | Determines applicable subset |
| Conformance class | Requirements grouped by capability level | Base vs. extended separation |
| Test derivation | Standard → Requirements → Test Purposes → Abstract Test Cases → Executable Tests | Our derivation chain |

**Key principle:** "Conformance testing is not intended to be exhaustive; a successfully passed test suite does not imply a 100% guarantee of conformance. But it does ensure, with a high degree of confidence, that the IUT conforms to the specified requirements" (ISO/IEC 9646-1, §1).

### 2.2 ETSI Test Specification Methodology (TR 102 840)

ETSI TR 102 840 provides the operational derivation process:

```
Standard/Specification
  → Identify conformance requirements
    → Formulate test purposes (one per requirement or requirement group)
      → Derive abstract test cases (preconditions + stimulus + expected behavior)
        → Implement executable test cases (TTCN-3)
```

**Coverage rule:** Each conformance requirement must be covered by at least one test purpose; each test purpose by at least one test case. This creates a **surjective mapping** from test cases to requirements.

### 2.3 Formal Models for Protocol Specification

| Model | Strengths | Limitations | Applicability |
|-------|-----------|-------------|---------------|
| FSM | Simple; W/Wp/HSI guarantee transition coverage | State explosion; no data | Classic protocols |
| EFSM | Variables, guards, actions | Undecidability; harder generation | Industrial protocols |
| LTS | Foundation for ioco; nondeterminism | No data; infinite-state complex | Formal conformance |
| CEFSM | Distributed protocols | Composition complexity | OSI, telecom |
| Petri Nets | Concurrency, synchronization | Test generation immature | Parallel protocols |
| UML Statecharts | Industry-standard; hierarchical | Semantics gaps | MBSE, DO-178C |

**For ARINC 615A:** The protocol is a session-based state machine (IDLE → SETUP → TRANSFER → COMPLETE/ERROR) with data parameters. An **EFSM model** is most appropriate.

### 2.4 ioco Conformance Theory (Tretmans, 1996)

The input/output conformance relation provides formal grounding:

- Specification S is a labelled transition system
- Implementation I is an input-output transition system
- **I ioco S** iff: for every trace σ of S, outputs(I, σ) ⊆ outputs(S, σ)

Our verification cases are **sampled test traces** checking whether IUT responses remain within specification-allowed behavior. "All VCs pass" is a sampled approximation of full ioco conformance.

### 2.5 FSM-Based Test Generation Methods

| Method | Coverage Guarantee | Reference |
|--------|-------------------|-----------|
| W-method | Detects output + transfer faults up to k extra states | Chow (1978) |
| Wp-method | Same guarantee, smaller suites | Fujiwara et al. (1991) |
| HSI-method | Harmonized state identification | Luo et al. (1994) |
| H-method | Improved via harmonized traces | Dorofeeva et al. (2003) |
| Mutation-based | Kills all non-equivalent mutants in fault model | Petrenko (2016) |

**Key insight:** "A test suite T is complete w.r.t. fault model F if, for every non-equivalent mutant M ∈ F, ∃t ∈ T that distinguishes the specification from M" (Bochmann, 1991; Petrenko, 2016).

We adopt a **requirement-driven** approach (not pure FSM traversal) because ARINC 615A is specified in natural language + tables, and requirement coverage is auditable. Completeness is **validated** via mutation/fault injection.

---

## 3. Related Work

### 3.1 Requirements-Based Test Generation (RBTG)

Yang et al. (2025) survey 267 RBTG papers. Key findings:
- Requirements classified as: NL → Semi-formal → Model-based → Formal → Hybrid
- Generation approaches: rule-based, model checking, search-based, NLP/LLM-based
- Coverage criteria: requirement, scenario, state/transition, data-flow
- **Gap:** RBTG focuses on software requirements; protocol conformance requirements (normative "shall" clauses) are underrepresented

### 3.2 Protocol Conformance Testing

| Work | Approach | Relevance |
|------|----------|-----------|
| ISO/IEC 9646 (1994) | Requirement → test purpose → ATS | Direct ancestor |
| ETSI TTCN-3 suites | Executable conformance tests | Operational template |
| Schieferdecker (2000) | TTCN-based formal derivation | TP → TC mapping |
| Dssouli et al. (1999) | FSM-based, complete fault coverage | Fault model approach |
| Petrenko (2016) | SMT-solving + mutant killing | Formal completeness |
| Li et al. (2021) | Model-based testing (StateAFL) | Fuzzing + state model |

### 3.3 Avionics Verification Standards

| Standard | Relevance |
|----------|-----------|
| DO-178C (RTCA, 2011) | Requirements-based testing at all DAL levels |
| DO-330 (RTCA, 2011) | Tool qualification for certification |
| ARINC 615A (SAE) | Protocol under test |
| ARINC 665 (SAE) | LSAP file structure |
| ARINC 664 (SAE) | AFDX/LU data format |

DO-178C §6.4.4.2 requires requirements-based testing — our method is analogous but at the protocol conformance level.

### 3.4 Mutation Testing for Adequacy

A test suite T is **mutation-adequate** if it kills all non-equivalent mutants. Key references: DeMillo et al. (1978), Jia & Harman (2011), Petrenko (2016), Nicourt et al. (2024).

### 3.5 Conformance Classes (Base/Extended Separation)

Analogous structures: PROFINET CC-A/B/C, ODVA conformance + interoperability, 3GPP base + profile-specific. Our base/extended model mirrors ISO 9646 conformance class hierarchy with a formal non-interference property.

---

## 4. Proposed Methodology

### 4.1 Five-Stage Derivation

```
Stage 1: Requirement Extraction
  Standard text → Conformance Requirement Set (CRS)

Stage 2: Test Purpose Derivation
  CRS → Test Purpose Set (TPS) [surjective mapping]

Stage 3: Verification Case Specification
  TPS → Abstract Verification Case Set (AVCS)

Stage 4: Coverage Validation
  AVCS × CRS → Coverage Matrix [verify surjectivity]

Stage 5: Adequacy Proof
  Mutation/Fault Injection → Detection Capability Evidence
```

### 4.2 Stage 1: Requirement Extraction

**Input:** ARINC 615A normative clauses  
**Process:**
1. Identify all normative statements ("shall", "must", "is required to")
2. Classify: Functional / Data / Timing / Error handling / Session
3. Assign unique IDs (e.g., `REQ-615A-DL-001`)
4. Record standard reference (clause, page)

**Output:** CRS = {r₁, r₂, ..., rₙ}

### 4.3 Stage 2: Test Purpose Derivation

Each rᵢ must be covered by ≥1 test purpose tpⱼ. Derivation heuristics:
1. **Positive:** Verify correct behavior per requirement
2. **Negative:** Verify error handling on violation
3. **Boundary:** Verify behavior at limits (e.g., max block size)

Mapping: CRS → TPS is surjective; one requirement may yield multiple TPs (1:N).

### 4.4 Stage 3: Verification Case Specification

Each TP refines into ≥1 abstract verification case with schema:
- VC-ID, Title, Function Allocation (DLS/THW), Priority
- Preconditions, Stimulus/Steps, Expected Result, Verdict Criteria
- Test Purpose Reference, Requirement Reference, Standard Reference
- Verification Status, Approval Status

### 4.5 Stage 4: Coverage Validation

**Hierarchical coverage criteria:**

| Level | Criterion | Necessity |
|-------|-----------|-----------|
| L1 | Requirement coverage (∀r ∈ CRS, ∃VC) | Mandatory |
| L2 | State coverage (all protocol states visited) | Mandatory |
| L3 | Transition coverage (all transitions exercised) | Mandatory |
| L4 | Data-flow coverage (fields tested at boundaries) | Recommended |
| L5 | Negative coverage (error conditions triggered) | Recommended |
| L6 | Sequence coverage (end-to-end scenarios) | Optional |

L1+L2+L3 = minimum conformance proof; L4+L5 = strengthened; L6 = system-level.

### 4.6 Stage 5: Adequacy Proof

**Fault model categories:** Packet format / State transition / Timing / Data integrity / Session / Option handling

**Process:** Generate mutants → Execute base VCS → Compute mutation score  
**Adequacy claim:** Score = 1.0 → VCS detects all faults in model

### 4.7 Base/Extended Separation

| Layer | Source | Purpose | Stability |
|-------|--------|---------|-----------|
| Base VCS | ARINC 615A standard | Prove conformance | Stable |
| Extended VCS | Project ICD | Project-specific assurance | Varies |

Extended VCs are additive; they do not modify or invalidate the base proof.

---

## 5. Formal Argument

### 5.1 Assurance Argument Structure

```
CLAIM: IUT conforms to ARINC 615A specification

├── ARG 1: Requirement Coverage
│   └── Coverage matrix demonstrates surjective mapping
├── ARG 2: Behavioral Coverage
│   └── All states + transitions exercised
├── ARG 3: Detection Capability
│   └── Mutation verification kills all non-equivalent mutants
└── ARG 4: Scope Boundary
    └── Explicit non-goals; confidence relative to fault model
```

### 5.2 Formal Definitions

**Def. 1 (CRS):** CRS(S) = {r | r is a normative requirement in standard S}  
**Def. 2 (VC):** vc = (id, pre, stimulus, expected, verdict, ref), ref ∈ CRS(S)  
**Def. 3 (VCS):** VCS = {vc₁, ..., vcₘ}  
**Def. 4 (Coverage):** VCS covers CRS(S) iff ∀r ∈ CRS(S), ∃vc ∈ VCS : vc.ref = r  
**Def. 5 (Conformance Evidence):** If VCS covers CRS(S) ∧ all vc verdict = PASS → IUT demonstrates conformance within CRS scope + fault model  
**Def. 6 (Adequacy):** VCS adequate for F iff ∀m ∈ (F \ equiv), ∃vc ∈ VCS : vc kills m

### 5.3 Limitations

1. Not exhaustive (infinite input space)
2. Fault-model-dependent (guarantee bounded by model)
3. Specification-dependent (ambiguity affects interpretation)
4. Temporal limitations (timing conformance needs specialized measurement)

---

## 6. Probabilistic Extension: Quantitative Conformance Confidence Modeling

### 6.1 Semantic Foundation

**Binding decision:** Transition matrix entries P(sᵢ, sⱼ) represent *verification confidence* — a Bayesian epistemic measure of our belief that the IUT correctly executes transition (sᵢ → sⱼ), given experimental evidence. They do NOT represent intrinsic IUT behavioral probabilities.

**Uncertainty boundary:**
- **Deterministic (model side):** State set S, legal transition topology, coverage criteria, verdict rules
- **Uncertain (IUT side):** Whether the IUT actually conforms at each test point — quantified as epistemic probability

This interpretation avoids ontological commitment to IUT randomness while enabling rigorous statistical inference.

### 6.2 Protocol Temporal Flow and State Enumeration

The ARINC 615A protocol stack is modeled per layer. The TFTP layer (representative example) has the following complete state set:

| State | Name | Self-loop? | Description |
|-------|------|-----------|-------------|
| S0 | IDLE | — | No active session |
| S1 | WAIT_OACK | Yes (retry) | Request sent, awaiting negotiation response |
| S2 | WAIT_ACK0 | No (transient) | OACK received, ACK(0) sent |
| S3_first | XFER_FIRST | Yes | First block DATA(1) transmission |
| S3_mid | XFER_MID | Yes (core) | Middle blocks DATA(2..65534) |
| S3_last | XFER_LAST | No | Final block (len < blksize) |
| S3_roll | XFER_ROLLOVER | Yes | Block number rollover (65535→1) |
| S3'_first | RETX_FIRST | Yes (bounded) | First block retransmission |
| S3'_mid | RETX_MID | Yes (bounded) | Middle block retransmission |
| S4 | XFER_RECV | Yes (core) | Receiving DATA, sending ACK (UPLOAD) |
| S4' | XFER_DUP | Yes | Duplicate DATA handling |
| S5 | COMPLETE | — | Transfer successfully finished |
| S6 | ERROR_LOCAL | — | Local error (timeout exhausted, sequence error) |
| S7 | ERROR_REMOTE | — | Remote ERROR received |
| S8 | ERROR_TID | Yes | Unknown TID packet received |

**Block segmentation rule:** Block transmission states are segmented into four categories (first/middle/last/rollover) — not a single state, not full 65535-state enumeration.

**Rollover handling:** S3_roll is triggered when counter c = 65535 within S3_mid. Modeled as an extended state (S3_mid, c) where c is a local counter variable; Markov property holds on the extended state space.

### 6.3 Layered DTMC Architecture

**Design principles:**
1. Each protocol layer (UDP, TFTP, 615A, 665, 664) has an independent sub-state machine
2. Unified chain with role tagging (DLS/THW) — one model, two role perspectives
3. Retransmission states are independent from normal transmission states
4. Inter-layer coupling: upper layer treats lower layer as atomic operation (success/failure)

**Layer hierarchy:**
```
615A Session Layer:  [Select Op] → [Establish] → [Transfer] → [Status] → [Complete]
                                          │ calls
TFTP Layer:          [RRQ/WRQ] → [OACK] → [DATA loop] → [Complete]
                                          │ uses
UDP Layer:           [Send datagram] → [Wait response] → [Timeout/Receive]
```

**Markov property scope:**
- Within each layer: DTMC (discrete-time Markov chain) holds
- Between layers: Semi-Markov (logic is Markovian; timing is not)
- For verification confidence: we model logical correctness, not timing → DTMC per layer suffices

### 6.4 Parameter Estimation (Conservative, Data-Driven)

**Source of data:** Self-loop verification (repeated tests at same state) + mutation testing (fault injection results).

**Self-loop i.i.d. scope:** Only samples at the SAME state via self-loop verification are i.i.d. Cross-state dependencies are modeled via the Markov chain structure, NOT assumed independent.

**Estimation methods:**

| Scenario | Method | Rationale |
|----------|--------|----------|
| Sufficient data (n ≥ 30) | Frequentist: θ̂ = c/n | No prior needed |
| Sparse data (n < 10) | Jeffreys prior Beta(1/2, 1/2) | Non-informative; no subjective input |
| Never directly tested | Mark as "unverified" | No probability assigned |
| Mutation provides indirect evidence | Lower-bound constraint | Detection capability ≥ observed |

**Confidence interval (exact, no asymptotic assumption):**
Clopper-Pearson: θ ∈ [Beta⁻¹(α/2; c, n−c+1), Beta⁻¹(1−α/2; c+1, n−c)]

**Cross-state dependency handling:**
- Causal dependency: encoded in chain topology (if P(sᵢ,sⱼ)=0, no dependency)
- Common-cause failures: identified via shared components (checksum, byte-order, timeout); validated by mutation testing across all affected states
- Functional independence: argued per pair, not assumed globally

### 6.5 HMM Formulation

The verification process is naturally a Hidden Markov Model:

- **Hidden states:** IUT's true conformance status θ₁, θ₂, ..., θₙ (unobservable)
- **Observations:** Test results X₁, X₂, ..., Xₙ ∈ {PASS, FAIL}
- **Emission probability:** P(Xₖ = PASS | θₖ = conforming) = θₖ
- **Transition probability:** P(θₖ₊₁ | θₖ) given by the DTMC structure

**Available inference:**
- **Forward algorithm:** Compute P(observation sequence | model) → path-level confidence
- **Viterbi algorithm:** On failure, find most likely fault state sequence → fault localization
- **Baum-Welch (EM):** Parameter learning from data — used only when data is sufficient; conservative constraints applied

### 6.6 Confidence Metrics

**Metric 1 — Weakest link (conservative lower bound):**
C_protocol = min_l min_s θ_s

**Metric 2 — Path product (Markov decomposition):**
For critical path S0→S1→S2→S3_first→S3_mid^(k)→S3_last→S5:
C_path = ∏ θ_s (product over path states)

This requires only the Markov property (conditional independence given current state), NOT global independence.

**Metric 3 — Layered confidence vector:**
C = (C_UDP, C_TFTP, C_615A, C_665, C_664)ᵀ

Reporting: Metrics 1 and 2 simultaneously. Metric 1 for safety-critical lower bound; Metric 2 for per-operation confidence.

### 6.7 FMEA/FMEDA Integration and Fault Localization

**Per-transition FMEA:**
Each transition (sᵢ → sⱼ) has associated failure modes, local/global effects, severity (S), detection method (VC reference), and diagnostic coverage (DC).

**FMEDA quantification:**
DC_i = (failure modes detected by VCs) / (total failure modes for transition i)

Relationship to mutation testing: mutation score ≈ diagnostic coverage DC.

**Fault localization on failure (Viterbi + FMEA):**
1. Observe failure sequence X₁, ..., Xₖ, Xₖ₊₁ = FAIL
2. Viterbi algorithm → most likely fault state s*
3. Query FMEA table for s* → ranked failure modes by severity
4. Output: diagnostic report with suspected failure mode + recommended investigation

**Closed loop:**
```
Model (DTMC/HMM) → Execute VCs → PASS: compute confidence metrics
                                → FAIL: Viterbi localization → FMEA diagnosis → failure mode report
```

### 6.8 Mathematical Toolkit Inventory

| Tool | Role in Framework | Applicability |
|------|-------------------|---------------|
| DTMC (per layer) | State-transition structure | Core |
| HMM | Hidden conformance inference | Core |
| Bayesian estimation | Parameter inference from sparse data | Core |
| Clopper-Pearson CI | Exact confidence intervals | Core |
| Bayesian Network (DAG) | Conditional dependency structure between test points | High |
| SPRT | Optimal stopping criterion for self-loop verification | High |
| FMEA/FMEDA | Failure mode catalog + diagnostic coverage | High |
| Viterbi algorithm | Fault localization | High |
| Fault Tree Analysis (FTA) | Top-down failure causation (complements FMEA) | Medium |
| Equivalence testing (TOST) | Timing parameter conformance | Medium |
| Statistical process control | Cross-run consistency monitoring | Optional |
| Information entropy | VC prioritization (most informative next test) | Optional |

### 6.9 Assumptions and Limitations (Strict Disclosure)

1. **Self-loop i.i.d.:** Valid within same-state repeated verification; NOT assumed across states
2. **Markov property:** Holds per layer with complete state encoding; rollover requires extended state
3. **Common-cause failures:** Identified by shared-component analysis + mutation coverage; residual risk acknowledged
4. **No unvalidated priors:** Jeffreys prior used only for sparse data; never subjective priors
5. **Model determinism:** Protocol specification is deterministic; probability describes epistemic uncertainty only
6. **Fault model bounded:** Detection guarantee holds only within the stated fault model

---

## 7. Positioning and Novelty

| Aspect | ISO 9646 | ETSI/TTCN | DO-178C | **This method** |
|--------|----------|-----------|---------|-----------------|
| Domain | OSI protocols | Telecom | Airborne SW | Data load protocols |
| Derivation | Std → ATS | Std → TTCN | Req → Test | Std → VCS |
| Coverage | Req + PICS | TP coverage | Req + structural | Req + state + transition + mutation |
| Proof | Implicit | Implicit | Structural | Explicit argument + mutation |
| Extensibility | Conformance classes | Profiles | N/A | Base/Extended separation |

**Novelty:** Systematic integration of established techniques into a project-agnostic, auditable method with: (1) explicit conformance argument, (2) mutation-based adequacy proof, (3) formal base/extended non-interference, (4) domain instantiation for ARINC 615A, (5) **probabilistic confidence quantification via layered DTMC/HMM with conservative data-driven estimation**, (6) **FMEA/FMEDA-integrated fault localization via Viterbi inference**.

---

## 8. Open Questions

| # | Question | Impact |
|---|----------|--------|
| 1 | How to handle ARINC 615A optional features (PICS-like selection)? | Applicable VC subset |
| 2 | Minimum mutation set for adequate fault coverage? | Stage 5 cost |
| 3 | Can derivation be partially automated? | Scalability |
| 4 | Formal proof of base/extended non-interference? | Theoretical rigor |
| 5 | Sufficient confidence level for certification authorities? | Practical acceptance |
| 6 | Optimal granularity for per-layer sub-state machines? | Model tractability |
| 7 | How to validate the Markov property empirically per layer? | Model validity |
| 8 | SPRT stopping thresholds for self-loop verification? | Test efficiency |

---

## 9. Conclusions and Next Steps

This report establishes the theoretical foundations for a systematic VCS generation methodology, extended with a probabilistic confidence quantification framework. The five-stage derivation, grounded in ISO 9646, ioco theory, and mutation testing, provides a rigorous yet practical framework for ARINC 615A conformance verification. The layered DTMC/HMM extension transforms binary pass/fail verdicts into quantified confidence metrics with diagnostic capability.

**Immediate next steps:**
1. Instantiate Stage 1: extract complete CRS from ARINC 615A
2. Build coverage matrix against existing VCs; identify gaps
3. Define protocol-specific fault model
4. Draft thesis §3 using Definitions 1–6 + probabilistic extension
5. Execute mutation verification on prototype
6. **Complete per-layer sub-state machine modeling (TFTP first, then 615A/UDP/665/664)**
7. **Design FMEA table template linking transitions → failure modes → VCs → mutants**
8. **Implement self-loop verification data collection in simulator**
9. **Compute example confidence metrics from prototype execution data**

---

## References

[1] ISO/IEC 9646-1:1994. Conformance testing methodology and framework — Part 1: General concepts.  
[2] ISO/IEC 9646-2:1994. Part 2: Abstract Test Suite specification.  
[3] ETSI TR 102 840 V1.2.1. Test specification development methodology.  
[4] RTCA DO-178C (2011). Software Considerations in Airborne Systems and Equipment Certification.  
[5] ARINC 615A-4 (SAE). Software Data Loader Using Ethernet Interface.  
[6] Chow, T.S. (1978). Testing software design modeled by finite-state machines. IEEE TSE.  
[7] Fujiwara, S. et al. (1991). Test selection based on finite state models. IEEE TSE.  
[8] Bochmann, G.v. & Petrenko, A. (1994). Protocol testing: Review of methods and relevance for software testing.  
[9] Petrenko, A. (2016). Test Generation by Constraint Solving and FSM Mutant Killing. IFIP ICTSS.  
[10] Tretmans, J. (1996). Conformance testing with labelled transition systems. Formal Aspects of Computing.  
[11] Bourdonov, I.B. et al. (2006). Formal Conformance Testing of Systems with Refused Inputs and Forbidden Actions.  
[12] Luthmann, L. et al. (2015). Towards an I/O Conformance Testing Theory for Software Product Lines.  
[13] Yang, Z. et al. (2025). Requirements-Based Test Generation: A Comprehensive Survey. ACM Computing Surveys.  
[14] Mustafa, A. et al. (2021). Automated Test Case Generation from Requirements: A Systematic Literature Review.  
[15] Zhu, H. (1997). Software Unit Test Coverage and Adequacy. ACM Computing Surveys.  
[16] DeMillo, R.A. et al. (1978). Hints on test data selection. IEEE Computer.  
[17] Jia, Y. & Harman, M. (2011). An Analysis and Survey of the Development of Mutation Testing. IEEE TSE.  
[18] Nicourt, E. et al. (2024). Using Mutation Testing To Improve and Minimize Test Suites. IEEE ICST.  
[19] Dssouli, R. et al. (1999). Test development for communication protocols. DSA.  
[20] Schieferdecker, I. (2000). Conformance Testing with TTCN.  
[21] Li, Y. et al. (2021). Model-Based Testing of Networked Applications. arXiv:2102.00378.  
[22] ARINC 665 (SAE). Loadable Software Aircraft Parts (LSAP).  
[23] ARINC 664 (SAE). Aircraft Data Network (AFDX).  
[24] DDCI (2024). ARINC 615A Data Loading — Target Data Loader Component Overview.  
[25] Rabiner, L.R. (1989). A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition. Proceedings of the IEEE.  
[26] Wald, A. (1945). Sequential Tests of Statistical Hypotheses. Annals of Mathematical Statistics.  
[27] IEC 60812:2018. Failure Modes and Effects Analysis (FMEA and FMEDA).  
[28] Vesely, W.E. et al. (1981). Fault Tree Handbook. NUREG-0492, US NRC.  
[29] Clopper, C.J. & Pearson, E.S. (1934). The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial. Biometrika.  
[30] Jeffreys, H. (1946). An Invariant Form for the Prior Probability in Estimation Problems. Proceedings of the Royal Society A.

---

*AI-assisted research disclosure: This report was produced with AI-assisted research tools. All references have been verified against published sources. The methodology synthesis represents the author's original integration of established techniques.*
