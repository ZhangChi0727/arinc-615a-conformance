# A Conformance Verification Methodology for the ARINC 615A Protocol: Requirements-Based Testing and Probabilistic Confidence Analysis

**Research Report RR-2026-001**

| | |
|---|---|
| **Version** | 3.0 |
| **Date** | 2026-07-23 |
| **Status** | PR #4: Test-and-Analysis reframing; title change; theoretical mapping; numerical examples; FMEA dictionary; terminology alignment |
| **Classification** | Internal — Academic Research |

---

## Abstract

Protocol conformance verification in avionics data loading remains largely ad hoc, relying on project-specific ICD testing without a systematic method to prove protocol-level compliance. This report presents a **conformance verification methodology** for the ARINC 615A data load protocol, comprising two complementary verification methods aligned with DO-178C §6.4: **Requirements-Based Testing** (§4–5) and **Probabilistic Confidence Analysis** (§6).

The Testing component integrates five established theoretical pillars: (1) the ISO/IEC 9646 conformance testing derivation chain, (2) ETSI test purpose formulation, (3) FSM-based coverage criteria (W/Wp/HSI methods), (4) ioco conformance theory, and (5) mutation-based test adequacy validation. We propose a five-stage derivation process — requirement extraction, test purpose derivation, verification case specification, coverage validation, and adequacy proof — and formalize it with six definitions. The method is instantiated for the ARINC 615A data load protocol, with a base/extended VCS separation mirroring ISO 9646 conformance classes. A structured assurance argument justifies the claim that passing all base verification cases provides high-confidence conformance evidence within a stated fault model.

The Analysis component introduces a probabilistic conformance confidence model based on layered Discrete-Time Markov Chains (DTMC) and Hidden Markov Models (HMM). The transition matrix entries are interpreted as *verification confidence* (Bayesian epistemic measure), not intrinsic IUT behavioral probabilities. Each protocol layer (UDP, TFTP, 615A, 665, 664) is modeled as an independent sub-state machine with role tagging and block-type segmentation. Parameters are estimated conservatively from self-loop verification data and mutation testing results, avoiding unvalidated independence assumptions. The framework further integrates FMEA/FMEDA for failure mode analysis and Viterbi-based fault localization upon verification failure.

The novelty lies not in any single technique but in their systematic integration into a transferable, auditable verification methodology — combining requirements-based testing with probabilistic confidence analysis — for data load protocol conformance.

**Keywords:** protocol conformance verification, requirements-based testing, probabilistic confidence analysis, verification case derivation, requirement coverage, ARINC 615A, mutation testing, ISO/IEC 9646, DO-178C, Markov chain, Hidden Markov Model, verification confidence, FMEA, fault localization

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

### 2.6 Theoretical Foundation → Method Mapping

The five theoretical pillars in §2.1–2.5 each support specific stages of the Testing methodology (§4–5). The Analysis component (§6) introduces independent mathematical tools not derived from §2.

| Theoretical Pillar | Supported Stage(s) | Role |
|--------------------|--------------------|------|
| ISO/IEC 9646 (§2.1) | §4.1–4.7 (full pipeline) | Derivation chain: Standard → CRS → TP → ATS → Executable; conformance classes → base/extended separation |
| ETSI TR 102 840 (§2.2) | §4.2–4.4 | Surjective mapping rule (each requirement ≥ 1 test purpose); operational derivation process |
| EFSM model (§2.3) | §4.5 (coverage L2/L3) | State/transition coverage criteria; also the modeling language for §6 layered state machines |
| ioco theory (§2.4) | §5 (formal argument) | VCs as sampled test traces approximating ioco conformance; theoretical anchor for Def. 5 |
| FSM mutation testing (§2.5) | §4.6 (adequacy proof) | W/Wp/HSI transition coverage guarantees; mutation adequacy as finite fault model bound |

**Key observation:** All of §2 supports the **Testing** component (§4–5). The **Analysis** component (§6) introduces an independent mathematical toolkit (DTMC, HMM, Bayesian estimation, FMEA/FMEDA) not derived from §2. The two components are complementary verification methods per DO-178C §6.4 (see §5.5).

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

### 4.8 Human Intervention vs. Automation

| Stage | Human Intervention | Automatable | Semi-automatable |
|-------|-------------------|-------------|------------------|
| §4.2 Requirement Extraction | Interpret normative clauses; classify (functional/data/timing/error/session); judge "shall" scope | ID assignment; standard reference recording; formatting | — |
| §4.3 Test Purpose Derivation | Derive TPs from requirements (domain knowledge); judge positive/negative/boundary adequacy | — | Template-based TP derivation (positive/negative/boundary heuristics); human review required |
| §4.4 VC Specification | Design preconditions, stimuli, expected results, verdict criteria (protocol expertise) | Schema formatting; ID generation; cross-referencing; YAML→Excel export | Template-based VC draft from TP; human review before finalization |
| §4.5 Coverage Validation | Interpret coverage gaps; decide if gaps are acceptable | Coverage matrix construction; surjectivity check; L1–L6 metric computation; gap reporting | — |
| §4.6 Adequacy Proof | Design fault model (protocol knowledge); interpret surviving mutants | Mutant generation (given fault model); mutant execution; mutation score computation | Mutant prioritization |

**Pattern:** Stages closer to specification interpretation (1–3) require more human expertise; stages closer to execution and computation (4–5) are more automatable. The Analysis component (§6) is fully automatable in execution (state tracking, parameter estimation, confidence computation, Viterbi localization), but state machine design and result interpretation require human judgment.

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
**Def. 5 (Conformance Evidence):** Under the assumed Conformance Requirement Set CRS(S) and fault model F, if the VCS covers CRS(S) and every verification case verdict is PASS, then this constitutes **sufficient evidence to claim protocol conformance within the scope of CRS(S) and F** — not an unrestricted proof over all possible behaviors or faults outside F.
**Def. 6 (Adequacy):** VCS adequate for F iff ∀m ∈ (F \ equiv), ∃vc ∈ VCS : vc kills m

### 5.3 Limitations

1. Not exhaustive (infinite input space)
2. Fault-model-dependent (guarantee bounded by model)
3. Specification-dependent (ambiguity affects interpretation)
4. Temporal limitations (timing conformance needs specialized measurement)

### 5.5 Verification Method Classification (Test vs. Analysis)

DO-178C §6.4 defines four verification methods: Test, Analysis, Review, and Demonstration. This methodology employs two:

| DO-178C Method | This Methodology | Scope |
|----------------|-----------------|-------|
| **Test** | §4–5: Requirements-Based Testing | Generate VCs → execute against IUT → pass/fail verdicts → coverage validation → mutation adequacy |
| **Analysis** | §6: Probabilistic Confidence Analysis | Quantify confidence from test evidence → FMEA/FMEDA diagnosis → Viterbi fault localization |
| Review | Not in scope | Code/design inspection |
| Demonstration | Not in scope | Functional observation without detailed measurement |

**Relationship:** Testing and Analysis are **complementary, not sequential**. Testing produces evidence (verdicts, traces); Analysis interprets that evidence (confidence metrics, fault diagnosis). Analysis does not generate new test executions — it evaluates existing results.

```
              Conformance Verification
              ╱                       ╲
    Testing (§4–5)              Analysis (§6)
         │                            │
   Execute VCs → verdicts      Quantify confidence → diagnose
         │                            │
         └────── Evidence ────────────┘
              ╲                       ╱
           Conformance Claim
        (scoped to CRS + F)
```

**Implication for the document title:** The methodology is not merely "verification case generation" (which covers only §4) but a complete verification methodology comprising Testing and Analysis.

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

**Role of the DTMC in this revision (PR #2):** The layered DTMC is retained as an **interpretation model** — a structured way to narrate protocol phases and to organize epistemic confidence labels along legal transitions. It is **not** claimed here as the sole, final mathematical foundation of conformance proof (that remains Def. 1–6 + coverage + mutation adequacy). Further abstraction (e.g. Protocol Evidence Graph / labeled transition graph without requiring a stochastic kernel) is recorded as **theory debt for PR #4**.

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

The verification process is modeled as a Hidden Markov Model. **Hidden states, observations, and parameters must not be conflated:**

| Concept | Symbol | Role |
|---------|--------|------|
| **Hidden state** | \(Z_k\) | Latent implementation conformance / fault class at step \(k\) (unobservable) |
| **Observation** | \(X_k\) | Test verdict at step \(k\): \(X_k \in \{\mathrm{PASS},\mathrm{FAIL}\}\) |
| **Parameters** | \(\theta\) | Model parameters only: initial distribution, transition kernel, emission kernel — **not** the hidden state |

**Example hidden-state alphabet (extensible):**  
\(\{ \mathrm{Conforming},\ \mathrm{RetryFault},\ \mathrm{TimeoutFault},\ \mathrm{SequenceFault},\ \mathrm{FileIntegrityFault},\ \ldots \}\).

**Emission (illustrative, to be calibrated):**  
\(P(X_k=\mathrm{PASS}\mid Z_k=\mathrm{Conforming})=1-\alpha\),  
\(P(X_k=\mathrm{PASS}\mid Z_k\neq\mathrm{Conforming})=\beta\),  
where \(\alpha\) is a false-FAIL rate and \(\beta\) is an escape / missed-detection rate (bounded using mutation evidence where available).

**Transition:** \(P(Z_{k+1}\mid Z_k)\) is a separate latent dynamics kernel (fault persistence / recovery assumptions). It is **not** identified with per-state epistemic confidence labels used in §6.6; the layered DTMC in §6.3 remains an **interpretation model** for protocol structure and confidence narration (see Theory Debt → PR #4 for further formalization).

**Available inference (once \(\theta\) is fixed):**
- **Forward algorithm:** likelihood of an observation sequence under the HMM
- **Viterbi algorithm:** on failure, most likely hidden-state path → fault localization aid
- **Baum-Welch (EM):** parameter learning only with sufficient data and conservative constraints (e.g. lower bounds on \(\beta\) from mutation escapes)

### 6.6 Confidence Metrics

**Metric 1 — Weakest link (conservative lower bound):**
\[
C_{\mathrm{protocol}} = \min_{\ell}\min_{s} \theta_{s}^{(\ell)}
\]
**Justification (safety / conservative assurance):** This metric is **intentionally conservative**. In safety-engineering and assurance practice, a chain of obligations is often bounded by its weakest verified link: if any critical verified element has low epistemic confidence, the overall claim should not exceed that lower bound. Metric 1 is therefore a **Conservative Assurance Metric**, not an estimate of average behavior. Unverified elements (\(\theta=\bot\)) are excluded from the \(\min\) or force the claim to remain incomplete (policy must be stated when reporting).

**Metric 2 — Path confidence along the verification evidence graph (conditional accumulation):**
Let a critical verification path induce an ordered evidence sequence \(v_0,v_1,\ldots,v_m\) (states or transition checks visited by the VCs). Path confidence is accumulated **conditionally along this evidence graph**, not by assuming mutually independent events:
\[
C_{\mathrm{path}} = \prod_{i=1}^{m} P(v_i \mid v_{i-1})
\]
where \(P(v_i\mid v_{i-1})\) denotes the epistemic confidence assigned to step \(i\) given that step \(i-1\) has been accepted under the layered interpretation model (operationally instantiated by the estimated confidence label for the corresponding edge/state transition).  

**Explicit non-claim:** We do **not** treat \(\{v_i\}\) as unconditionally independent Bernoulli trials. A naive product of unrelated marginals \(\prod \theta_i\) without the conditional/evidence-graph reading is **disallowed** as a conformance metric.

**Metric 3 — Layered confidence vector:**
\[
C = (C_{\mathrm{UDP}}, C_{\mathrm{TFTP}}, C_{\mathrm{615A}}, C_{\mathrm{665}}, C_{\mathrm{664}})^{\mathsf{T}}
\]

Reporting: Metrics 1 and 2 simultaneously. Metric 1 for safety-critical lower bound; Metric 2 for per-operation path confidence under the conditional accumulation rule.

### 6.7 FMEA/FMEDA Integration and Fault Localization

**Per-transition FMEA:**
Each transition (sᵢ → sⱼ) has associated failure modes, local/global effects, severity (S), detection method (VC reference), and diagnostic coverage (DC).

**FMEDA quantification:**
DC_i = (failure modes detected by VCs) / (total failure modes for transition i)

Relationship to mutation testing: mutation score is used as an **empirical estimator** of diagnostic coverage DC (not a mathematical identity).

**FMEA ↔ Mutation Mapping Dictionary (template):**

| Transition | Failure Mode ID | Failure Mode | Local Effect | Global Effect | Severity | Detecting VC | Mutant Operator | Detected? |
|------------|----------------|--------------|--------------|---------------|----------|-------------|-----------------|----------|
| S1→S2 | FM-TFTP-01 | OACK ignored | blksize stays default | Transfer may fail on large files | Medium | VC-TFTP-NEG-003 | Remove OACK handling | Yes |
| S3_mid→S3_mid | FM-TFTP-02 | Block counter not incremented | Duplicate DATA sent | Receiver rejects; transfer stalls | High | VC-TFTP-XFER-007 | Freeze block_num | Yes |
| S3_roll→S3_first | FM-TFTP-03 | Rollover 65535→0 instead of →1 | Sequence error at receiver | Transfer aborted | High | VC-TFTP-ROLL-001 | next_block returns 0 | Yes |
| S3'_mid→S3_mid | FM-TFTP-04 | Retransmit with wrong block number | Receiver sequence error | Transfer aborted | High | VC-TFTP-RETX-002 | Corrupt retransmit block_num | Yes |
| S4→S4' | FM-TFTP-05 | Duplicate DATA appended | Data corruption | File integrity failure | Critical | VC-TFTP-DUP-001 | Remove duplicate check | Yes |
| S1→S6 | FM-TFTP-06 | Timeout not enforced | Hangs indefinitely | Session never completes | Medium | VC-TFTP-TMO-001 | Set timeout=∞ | Yes |

*This table is a template; the complete dictionary is populated per protocol layer during VC development (see PR #5 engineering scope).*

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

### 6.10 Numerical Toy Example

**Scenario:** TFTP layer, state S3_mid (middle block transfer), self-loop verification with n = 50 repeated executions.

**Step 1 — Parameter estimation:**
- Observed: c = 48 PASS, 2 FAIL out of n = 50
- Frequentist estimate: θ̂ = 48/50 = 0.96
- 95% Clopper-Pearson CI: θ ∈ [0.863, 0.995]
- Jeffreys posterior (if n were small): Beta(48.5, 2.5), posterior mean = 48.5/51 = 0.951

**Step 2 — Weakest-link metric (Metric 1):**
Suppose per-layer minimum confidences after full VCS execution:

| Layer | min θ_s | Limiting state |
|-------|---------|----------------|
| UDP | 0.99 | U1' (retransmit) |
| TFTP | 0.96 | S3_mid (middle block) |
| 615A | 0.98 | A3 (transfer active) |
| 665 | 1.00 | — (all pass) |
| 664 | 1.00 | — (all pass) |

C_protocol = min(0.99, 0.96, 0.98, 1.00, 1.00) = **0.96** (limited by TFTP S3_mid)

**Step 3 — Path confidence (Metric 2):**
Critical DOWNLOAD path: S0→S1→S2→S3_first→S3_mid→S3_last→S5

| Step | Transition | P(v_i \| v_{i-1}) |
|------|-----------|-------------------|
| 1 | S0→S1 | 0.99 |
| 2 | S1→S2 | 0.98 |
| 3 | S2→S3_first | 0.99 |
| 4 | S3_first→S3_mid | 0.97 |
| 5 | S3_mid→S3_last | 0.96 |
| 6 | S3_last→S5 | 0.99 |

C_path = 0.99 × 0.98 × 0.99 × 0.97 × 0.96 × 0.99 = **0.893**

**Step 4 — Layered confidence vector (Metric 3):**
C = (0.99, 0.96, 0.98, 1.00, 1.00)ᵀ

**Interpretation:**
- Metric 1 (0.96): Conservative lower bound — "we are at least 96% confident in the weakest verified element"
- Metric 2 (0.893): Path-level confidence — "the probability that the entire DOWNLOAD path is correctly implemented, given conditional evidence accumulation"
- Metric 3: Identifies TFTP as the limiting layer; directs future verification effort to S3_mid self-loop sampling

**Mutation evidence integration:**
If mutation testing on S3_mid yields mutation score = 5/5 (all mutants killed), this provides evidence that DC(S3_mid) ≥ 1.0 within the stated fault model, strengthening the confidence in θ̂ = 0.96 (the 2 FAILs are likely environmental, not conformance failures).

---

## 7. Positioning and Novelty

| Aspect | ISO 9646 | ETSI/TTCN | DO-178C | **This method** |
|--------|----------|-----------|---------|------------------|
| Domain | OSI protocols | Telecom | Airborne SW | Data load protocols |
| Derivation | Std → ATS | Std → TTCN | Req → Test | Std → VCS |
| Coverage | Req + PICS | TP coverage | Req + structural | Req + state + transition + mutation |
| Proof | Implicit | Implicit | Structural | Explicit argument + mutation |
| Extensibility | Conformance classes | Profiles | N/A | Base/Extended separation |
| Verification methods | Test only | Test only | Test + Analysis + Review + Demo | **Test + Analysis** (complementary) |
| Quantification | None | None | Structural coverage | Probabilistic confidence + FMEA diagnosis |
| Multi-protocol | Per-protocol ATS | Per-protocol suite | Per-project | **Method is protocol-agnostic; instantiated for 615A** |

**Novelty:** Systematic integration of established techniques into a project-agnostic, auditable verification methodology with: (1) explicit conformance argument, (2) mutation-based adequacy proof, (3) formal base/extended non-interference, (4) domain instantiation for ARINC 615A, (5) **probabilistic confidence quantification via layered DTMC/HMM with conservative data-driven estimation**, (6) **FMEA/FMEDA-integrated fault localization via Viterbi inference**, (7) **Test-and-Analysis dual-path verification aligned with DO-178C §6.4**.

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
| 9 | How to extend coverage criteria for timing-critical protocols (L7 timing coverage)? | Multi-protocol generalization |
| 10 | How to adapt the methodology for stateless/message-based protocols (e.g., raw CAN)? | Multi-protocol generalization |
| 11 | Can the methodology be instantiated for ARINC 825 (CAN bus) as a second protocol instance? | Generalization evidence |

---

## 9. Conclusions and Next Steps

This report establishes a **conformance verification methodology** for the ARINC 615A data load protocol, comprising two complementary verification methods: Requirements-Based Testing (§4–5) and Probabilistic Confidence Analysis (§6). The five-stage derivation, grounded in ISO 9646, ioco theory, and mutation testing, provides a rigorous yet practical framework for protocol conformance verification. The layered DTMC/HMM extension transforms binary pass/fail verdicts into quantified confidence metrics with diagnostic capability.

The methodology is designed to be **protocol-agnostic** in its derivation process, coverage criteria, and analytical framework; ARINC 615A serves as the sole protocol instance in this work. Generalization to other protocols (e.g., ARINC 825, automotive bus protocols) is identified as future research.

**Immediate next steps (research/theory — PR #4 scope):**
1. Instantiate Stage 1: extract complete CRS from ARINC 615A
2. Build coverage matrix against existing VCs; identify gaps
3. Define protocol-specific fault model
4. Draft thesis §3 using Definitions 1–6 + Test-and-Analysis framing
5. Execute mutation verification on prototype

**Engineering next steps (PR #5 scope — after theory frozen):**
6. Complete per-layer sub-state machine modeling (TFTP first, then 615A/UDP/665/664)
7. Populate FMEA ↔ mutation mapping dictionary per layer
8. Implement self-loop verification data collection in simulator
9. Compute confidence metrics from prototype execution data
10. Calibrate emission probabilities (α, β) from experimental data
11. Build TFTP EFSM formal model for L2/L3 coverage automation
12. Integrate VC skill → simulator → coverage → mutation pipeline

**Future research (beyond PR #5):**
13. ARINC 825 (CAN bus) as second protocol instance
14. Timing coverage criteria (L7) for real-time protocols
15. Stateless/message-based protocol adaptation
16. Protocol Evidence Graph formalization (TD-01)

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
