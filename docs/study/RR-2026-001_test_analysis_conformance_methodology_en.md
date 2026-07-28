# A Test-and-Analysis Methodology for ARINC 615A Conformance Verification
## Requirements-Based Testing, Bounded Evidence Analysis, and Independent Review Gates

**Research Report RR-2026-001**

| Field | Value |
|---|---|
| **Version** | 4.1 research baseline |
| **Date** | 2026-07-26 |
| **Status** | Normative research baseline; empirical claims remain conditional on the evidence gates defined in §10 |
| **Primary instance** | ARINC 615A DOWNLOAD/UPLOAD services over TFTP |
| **Classification** | Internal — Academic Research |
| **Normative language** | The English report is authoritative; the Chinese report is a synchronized translation |

---

## Abstract

Protocol conformance verification must convert normative requirements into credible engineering decisions. It therefore needs both dynamic evidence from executing an Implementation Under Test (IUT) and disciplined analysis of coverage, detection capability, uncertainty, and failure causes. This report presents an integrated Test-and-Analysis methodology for ARINC 615A conformance verification.

The **Test path** derives an applicable Conformance Requirement Set (CRS), Test Purposes (TPs), and executable Verification Cases (VCs), then executes them against the IUT to produce verdicts, traces, and measurements. The **Analysis path** evaluates traceability, model-based coverage, finite-fault-domain adequacy, repeated-run behavior, calibrated evidence, and failure diagnosis. Test and Analysis are complementary: Test creates controlled observations; Analysis determines what those observations support and where further verification effort is needed.

Independent **Review and Inspection gates** govern the quality of requirements, protocol models, verification cases, oracles, execution readiness, evidence packages, and released claims. These static activities support the two primary paths without being presented as independent research contributions. Demonstration may support stakeholder acceptance, but it is not the principal method for detailed protocol conformance.

The resulting framework aims to create both academic value—clear semantics, bounded claims, and empirically evaluable hypotheses—and engineering value—reviewable artifacts, automation points, release gates, diagnostic outputs, and reproducible decision records.

**Keywords:** protocol conformance verification; Test-and-Analysis; requirements-based testing; engineering assurance; traceability; ARINC 615A; finite fault domain; mutation testing; calibrated evidence; Bayesian inference; review gate; inspection

---

## 1. Research Objective and Value

### 1.1 Problem

ARINC 615A verification is often organized around project-specific Interface Control Documents (ICDs). That practice is necessary for integration, but it does not by itself establish a reusable protocol-level argument tied to the normative standard.

The research problem is:

> How can a verification team derive, execute, and evaluate a reusable ARINC 615A conformance test suite so that every claim is traceable to an applicable normative requirement, bounded by an explicit observation and fault model, and supported by reproducible evidence?

### 1.2 Research questions

| ID | Research question | Required evidence |
|---|---|---|
| **RQ1 — Derivation** | How can applicable normative requirements be transformed into auditable test purposes and executable verification cases? | CRS, trace relations, reviewer agreement, case schemas |
| **RQ2 — Coverage** | Which requirement, model, data, timing, negative, and sequence obligations must be covered for the declared scope? | Coverage obligations and matrices |
| **RQ3 — Bounded adequacy** | How effectively does the VCS detect non-conformance within a declared finite fault domain? | Valid mutant catalog, held-out faults, mutation results |
| **RQ4 — Evidence interpretation** | What can repeated PASS/FAIL observations support without conflating execution repeatability with conformance probability? | Observation model, intervals, calibration data |
| **RQ5 — Diagnosis** | Can failure signatures identify fault classes with useful and reproducible accuracy? | Fault-injection dataset, confusion matrix, Top-k metrics |
| **RQ6 — Transferability** | Which parts of the method remain valid when applied to a second protocol? | Second-instance study; not answered by the 615A instance alone |

### 1.3 Integrated-method thesis

The methodology is organized around two primary, mutually reinforcing verification paths:

1. **Test:** interact with the IUT under controlled preconditions, stimuli, timing, and oracles; produce verdicts, traces, measurements, and reproducible execution records.
2. **Analysis:** examine requirements, models, traceability, coverage, mutants, repeated observations, uncertainty, and failure signatures; produce adequacy assessments, evidence bounds, diagnostic rankings, and recommendations for additional tests.

The relationship is a closed engineering loop:

```text
Requirements and protocol model
        |
        v
Test design -> Test execution -> Observations and verdicts
     ^                                 |
     |                                 v
     +---- Analysis <- Coverage, adequacy, uncertainty, diagnosis
                 |
                 v
        Engineering decision / next verification action
```

Review and Inspection gates control the artifacts entering and leaving this loop.

### 1.4 Academic and engineering value

| Value dimension | Value created |
|---|---|
| **Academic** | Explicit semantics; formal trace relations; bounded adequacy claims; calibrated inference; hypotheses that can be empirically evaluated; transferability as a research question |
| **Engineering** | Standard-to-case traceability; reusable base VCS; controlled extended VCS; review gates; executable evidence schemas; held-out fault evaluation; diagnostic outputs; auditable release decisions |

The academic contribution supplies defensible reasoning. The engineering contribution makes that reasoning operational, reviewable, and maintainable.

### 1.5 Contributions claimed by this report

1. **Traceable derivation framework.** A many-to-many requirements-to-tests model that supports applicability, compound requirements, and multiple cases per purpose.
2. **Complementary Test-and-Analysis workflow.** A closed loop in which dynamic execution produces evidence and analysis evaluates sufficiency, uncertainty, and next actions.
3. **Scoped assurance argument.** A formal separation between coverage, valid execution, and bounded fault-detection evidence.
4. **Finite fault-domain adequacy method.** A reproducible mutation workflow with explicit equivalent/invalid-mutant handling and held-out evaluation faults.
5. **Calibrated evidence semantics.** A separation between operational PASS probability, likelihood evidence, and posterior belief in conformance.
6. **Independent quality gates.** Review and Inspection gates covering scope, requirements, models, cases, oracles, execution readiness, evidence, and claim release.
7. **Evaluation protocol.** An empirically testable design with baselines, metrics, leakage controls, and decision gates.

### 1.6 Scientific positioning and novelty boundary

The method is a synthesis, not a claim to have invented requirements-based or model-based conformance testing.

- ISO/IEC 9646 supplies the conformance-testing framework and Abstract Test Suite context [1][2].
- Tretmans provides the formal input/output conformance and test-generation foundation [4].
- Chow and Fujiwara et al. provide finite-state-machine checking-experiment foundations under explicit machine assumptions [5][6].
- ETSI TR 102 840 provides non-normative recommendations for applying model-based test generation in standardization; it specifically treats traceability and generation from system models [3].
- Petrenko et al. provide finite fault-domain and mutant-killing techniques using constraint solving [7].
- Mutation-testing evidence and its known limitations are surveyed by Jia and Harman [8].
- Yang et al. show the breadth of requirements-based test generation and the need to distinguish input representations, generated artifacts, and evaluation methods [9].
- Li et al. demonstrate rigorous model-based testing of a networked application with explicit treatment of nondeterminism [10].
- NASA systems-engineering guidance commonly classifies requirement verification methods as Test, Analysis, Inspection, and Demonstration [19]. Review is treated here as a static governance activity aligned with software review practice rather than forced into that four-method taxonomy [20].

The intended novelty is the **auditable integration and empirical evaluation** of these ideas for ARINC 615A: a complementary Test-and-Analysis loop, applicability-controlled requirement extraction, obligation-sensitive traceability, explicit finite-fault-domain bounds, held-out fault evaluation, calibrated evidence gates, and independent artifact reviews. Until the artifacts and experiments in §§8–10 are completed, this novelty remains a research hypothesis rather than an established result.

DO-178C is adjacent assurance context [16], not the formal source of the method or of the Test/Analysis/Inspection taxonomy. FMEA/FMECA follows IEC 60812 terminology [14]. HMM concepts, if later used, follow a separately validated temporal diagnostic model rather than being inferred from the protocol graph [15].

---

## Scope, Boundaries, and Non-Claims

### Scope of the ARINC 615A instance

**Included**

- DLS and THW roles;
- DOWNLOAD and UPLOAD session behavior;
- TFTP/UDP behavior exercised by those services;
- request negotiation, DATA/ACK transfer, retry, timeout, duplicate, sequence, error, final-block, and declared rollover behavior;
- protocol fields and timing obligations explicitly present in the applicable CRS.

**Excluded from the base claim**

- FIND and INFORMATION services;
- unrestricted ARINC 665 file-content conformance;
- unrestricted ARINC 664 network conformance;
- certification credit;
- performance, security, and robustness properties not represented in the CRS;
- faults outside the declared finite fault domain.

ARINC 665 and ARINC 664 may appear as environmental assumptions or test-data constraints. They are not assigned a conformance score unless their own applicable requirements and verification evidence are included.

### Explicit non-claims

This report does not claim that:

- a finite test suite proves conformance for all possible behaviors;
- structural coverage is equivalent to fault-detection capability;
- a mutation score generalizes automatically to all real faults;
- repeated PASS frequency is a probability that a fixed IUT conforms;
- protocol layers are statistically independent;
- an uncalibrated scalar is a protocol-level probability;
- ARINC 615A alone proves protocol independence;
- the method provides certification approval or replaces authority review.

---

## 2. Conceptual Architecture

### 2.1 Verification activities and their roles

| Activity | Primary role in this methodology | Typical inputs | Typical outputs |
|---|---|---|---|
| **Test** | Dynamically exercise the IUT against requirement-derived oracles | IUT, VC, environment, protocol peer | Verdicts, packet traces, measurements, execution records |
| **Analysis** | Determine coverage, adequacy, uncertainty, dependencies, and likely fault causes | CRS, model, Test evidence, mutants, calibration data | Coverage matrices, adequacy results, intervals/posteriors, diagnostic rankings |
| **Inspection** | Check objective artifact properties using a defined checklist | CRS entries, trace matrices, schemas, logs, release package | Defects, completeness findings, signed inspection record |
| **Review** | Independently evaluate technical judgments and approve progression through gates | Interpretations, EFSM, VCs, oracle logic, analyses, claims | Review findings, rationale, approval/rework decision |
| **Demonstration** | Show stakeholder-visible operation where detailed measurement is not the main objective | Integrated scenario or prototype | Observed capability and acceptance evidence |

Test and Analysis are the two primary technical paths. Inspection and Review form a cross-cutting static assurance layer. Demonstration is optional and cannot replace detailed Test evidence for protocol obligations requiring precise packet, timing, or state observations.

### 2.2 Separated analytical objects

The baseline separates four objects that were previously conflated.

| Object | Purpose | Mathematical form | May carry probabilities? |
|---|---|---|---|
| **Protocol model** | Describe legal observable behavior | EFSM/IOLTS \(G\) | Not required |
| **Traceability model** | Link requirements, purposes, cases, and model targets | Relations \(\rho\) | No |
| **Evidence record** | Preserve execution conditions, observations, and verdicts | Dataset \(\mathcal{E}\) | Observations only |
| **Inference/diagnosis model** | Interpret calibrated evidence | Likelihood/Bayesian model | Yes, if calibrated |

The protocol model is not an evidence model. An edge in the protocol graph denotes a possible or required behavior; it is not assigned a "transition probability" merely because confidence evidence is attached to it.

### 2.3 Assurance tiers

| Tier | Claim | Minimum supporting artifacts |
|---|---|---|
| **T0 — Traceability** | Every applicable requirement is linked to at least one executable case | CRS, TP/VC relations |
| **T1 — Observed conformance** | The IUT produced acceptable observations for the executed cases under recorded conditions | T0 + valid execution records |
| **T2 — Bounded detection adequacy** | The VCS distinguishes the specification from every non-equivalent member of the declared evaluated fault set | T1 + mutation/fault results |
| **T3 — Calibrated evidence** | Evidence changes belief in specified conformance propositions according to a validated observation model | T2 + calibration and sensitivity analysis |

Higher tiers do not erase the boundaries of lower tiers. A Tier T3 number cannot compensate for missing traceability or invalid executions.

---

## 3. Formal Core

### 3.1 Standard, profile, and applicable requirements

Let:

- \(S\) be a fixed edition of a protocol standard;
- \(P\) be the implementation applicability declaration, including supported roles, services, options, and declared exclusions;
- \(O\) be the observation boundary: the packet, timing, state, log, and file-level phenomena the verification system is permitted to use;
- \(R(S)\) be the set of extracted normative requirement items;
- \(R_{\mathrm{app}}(S,P)\subseteq R(S)\) be the requirements applicable to \(P\).

Every requirement item \(r\in R(S)\) contains:

\[
r=(id,\ source,\ textHash,\ modality,\ applicability,\ category,\ interpretation)
\]

`source` includes the standard edition, clause, table/figure identifier, and page. `textHash` supports controlled internal traceability without reproducing proprietary standard text in a public artifact.

Requirements are classified by their verification obligations, not by one global coverage hierarchy:

\[
\mathrm{Obl}(r)\subseteq
\{\mathrm{functional},\mathrm{state},\mathrm{transition},\mathrm{data},
\mathrm{timing},\mathrm{negative},\mathrm{sequence}\}.
\]

### 3.2 Test purposes and verification cases

Let \(T\) be the set of Test Purposes and \(V\) the set of Verification Cases.

Traceability is represented by relations:

\[
\rho_{RT}\subseteq R_{\mathrm{app}}\times T,
\qquad
\rho_{TV}\subseteq T\times V.
\]

This is intentionally not modeled as a one-to-one function. One requirement may generate several purposes; one purpose may require several cases; one case may support several requirements.

A Verification Case is:

\[
v=(id,\ role,\ pre,\ stimulus,\ oracle,\ refs,\ targets,\ reset,\ evidenceSchema).
\]

Where:

- `pre` defines executable preconditions;
- `stimulus` defines controlled actions and inputs;
- `oracle` maps observations to a verdict;
- `refs\subseteq R_{\mathrm{app}}` records requirement references;
- `targets` records EFSM states, transitions, data partitions, timing bounds, and fault classes;
- `reset` defines isolation and state restoration;
- `evidenceSchema` defines mandatory logs and measurements.

### 3.3 Verdict semantics

For an IUT \(I\), verification case \(v\), and controlled environment \(e\):

\[
\mathrm{Verdict}(I,v,e)\in
\{\mathrm{PASS},\mathrm{FAIL},\mathrm{INCONCLUSIVE},\mathrm{ERROR}\}.
\]

- **PASS:** all preconditions were satisfied and the observation met the oracle.
- **FAIL:** preconditions were satisfied and the observation violated the oracle.
- **INCONCLUSIVE:** applicability or preconditions could not be established, or the observation was insufficient.
- **ERROR:** the verification instrument or environment invalidated the execution.

`INCONCLUSIVE` and `ERROR` are never silently converted to PASS or excluded from reporting.

### 3.4 Requirement traceability coverage

The VCS is traceability-complete for \(R_{\mathrm{app}}\) iff:

\[
\forall r\in R_{\mathrm{app}},
\ \exists t\in T,\exists v\in V:
(r,t)\in\rho_{RT}\land(t,v)\in\rho_{TV}.
\tag{1}
\]

Obligation coverage additionally requires:

\[
\forall r\in R_{\mathrm{app}},\
\forall o\in\mathrm{Obl}(r),\
\exists v\in V:\mathrm{Covers}(v,r,o).
\tag{2}
\]

Equation (1) checks trace existence. Equation (2) checks whether every required obligation type has an adequate case. Neither equation alone proves oracle correctness or detection capability.

### 3.5 Protocol behavioral model

The observable protocol model is an Extended Finite State Machine:

\[
G=(Q,q_0,X,\Sigma_I,\Sigma_O,\Delta)
\]

where:

- \(Q\) is the control-state set;
- \(q_0\) is the initial state;
- \(X\) is the vector of data variables, counters, negotiated options, retry state, and relevant history;
- \(\Sigma_I,\Sigma_O\) are input and output alphabets;
- \(\Delta\) is the guarded transition relation.

A transition is:

\[
\tau=(q,\ input,\ guard(X),\ action(X),\ output,\ q').
\]

The Markov property is **not** assumed. If a probabilistic temporal model is later introduced, its state sufficiency must be demonstrated separately.

### 3.6 Finite fault domain

A fault domain is:

\[
\mathcal{F}=(G,\preceq,\mathcal{M})
\]

where \(G\) is the specification model, \(\preceq\) is the declared conformance relation, and \(\mathcal{M}\) is a finite set of candidate nonconforming implementations or mutants.

Classify \(\mathcal{M}\) using:

- \(\mathcal{M}_{\mathrm{invalid}}\): malformed or non-executable mutants;
- \(\mathcal{M}_{\mathrm{exec}}=\mathcal{M}\setminus\mathcal{M}_{\mathrm{invalid}}\): buildable and executable mutants;
- \(\mathcal{M}_{\mathrm{equiv}}\subseteq\mathcal{M}_{\mathrm{exec}}\): mutants behaviorally equivalent to \(G\) within the declared observation scope;
- \(\mathcal{M}_{\mathrm{eval}}=\mathcal{M}_{\mathrm{exec}}\setminus\mathcal{M}_{\mathrm{equiv}}\): evaluated valid, non-equivalent mutants.

The final classes are disjoint:
\(\mathcal{M}=\mathcal{M}_{\mathrm{invalid}}\mathbin{\dot\cup}
\mathcal{M}_{\mathrm{equiv}}\mathbin{\dot\cup}\mathcal{M}_{\mathrm{eval}}\).

A case \(v\) kills mutant \(m\) iff:

\[
\mathrm{Kill}(v,m)=1
\iff
\mathrm{Verdict}(G,v,e)=\mathrm{PASS}
\land
\mathrm{Verdict}(m,v,e)=\mathrm{FAIL},
\tag{3}
\]

with equivalent controlled conditions and a valid oracle.

Here \(\mathrm{Verdict}(G,v,e)\) denotes the reference verdict produced from an executable reference model or an independently validated oracle derived from \(G\); it does not assume that an abstract EFSM is directly executable.

The VCS is complete relative to \(\mathcal{M}_{\mathrm{eval}}\) iff:

\[
\forall m\in \mathcal{M}_{\mathrm{eval}},
\ \exists v\in V:\mathrm{Kill}(v,m)=1.
\tag{4}
\]

Equation (4) is a bounded statement. It says nothing about faults outside \(\mathcal{M}_{\mathrm{eval}}\).

### 3.7 Weighted mutation score

If all evaluated mutants have equal standing and
\(|\mathcal{M}_{\mathrm{eval}}|>0\):

\[
\mathrm{MS}=
\frac{\sum_{m\in \mathcal{M}_{\mathrm{eval}}}
\mathbf{1}[\exists v\in V:\mathrm{Kill}(v,m)]}
{|\mathcal{M}_{\mathrm{eval}}|}.
\tag{5}
\]

If expert-justified nonnegative weights \(w_m\) represent distinct
failure-mode importance and \(\sum_m w_m>0\):

\[
\mathrm{WMS}=
\frac{\sum_{m\in \mathcal{M}_{\mathrm{eval}}}
w_m\mathbf{1}[\exists v\in V:\mathrm{Kill}(v,m)]}
{\sum_{m\in \mathcal{M}_{\mathrm{eval}}}w_m}.
\tag{6}
\]

Weights, their rationale, and sensitivity analysis must be published. A mutation score is not called FMEDA diagnostic coverage unless the evaluated mutants are a defensible representation of the target failure-mode population.

---

## 4. Method

### 4.1 Stage A — Freeze scope and applicability

1. Fix the ARINC 615A edition and any approved interpretations.
2. Record DLS/THW roles and included services.
3. Record supported options, limits, and environmental assumptions.
4. Produce \(P\), the applicability declaration.
5. Assign independent reviewers for requirement extraction.

**Exit artifact:** signed scope and applicability record.

### 4.2 Stage B — Extract and adjudicate the CRS

Two reviewers independently identify normative statements and split compound clauses into atomic requirement items. They then reconcile:

- missed requirements;
- differing applicability judgments;
- ambiguous modalities;
- compound obligations;
- references to tables, timing values, and error behavior.

Report both raw and adjudicated agreement. Cohen's \(\kappa\) may be reported for categorical decisions, but percentage agreement and the disagreement table remain mandatory because \(\kappa\) can be prevalence-sensitive.

**Exit artifact:** versioned CRS with source hashes and an adjudication log.

### 4.3 Stage C — Build the observable EFSM

1. Define externally observable states and variables.
2. Encode guards, options, retry counters, timeout conditions, block-number behavior, and terminal states.
3. Link each transition to requirements.
4. Review the EFSM against the CRS.
5. Treat every protocol-specific claim, including rollover rules, as unresolved until it has an exact standard reference.

**Exit artifact:** EFSM and requirement-to-transition relation.

### 4.4 Stage D — Derive Test Purposes

For each applicable requirement and obligation type, derive purposes using:

- nominal behavior;
- invalid input or forbidden output;
- equivalence-class and boundary values;
- state/transition reachability;
- timeout and retry thresholds;
- duplicate, reordering, and sequence faults;
- end-to-end session sequences where required.

Test Purpose derivation is human-reviewed. Automated generation may propose candidates but cannot silently establish normative meaning.

**Exit artifact:** TP catalog and \(\rho_{RT}\).

### 4.5 Stage E — Specify Verification Cases

Each case includes:

- stable identifier and version;
- role allocation;
- initial IUT and peer state;
- exact test data and partitions;
- steps and controlled timing;
- expected observable trace;
- verdict oracle;
- requirement and model targets;
- reset/isolation procedure;
- evidence fields;
- instrument and environment version.

**Exit artifact:** executable or implementation-ready VCS and \(\rho_{TV}\).

### 4.6 Stage F — Validate coverage

Coverage is reported separately:

- requirement traceability coverage;
- obligation coverage;
- state coverage;
- transition coverage;
- guard/data-partition coverage;
- timing-bound coverage;
- negative/error coverage;
- required sequence coverage.

A single aggregate percentage is not used to conceal a missing mandatory category.

### 4.7 Stage G — Construct the fault domain

Fault operators are derived from:

- requirement misinterpretations;
- EFSM guard/action/target changes;
- field encoding faults;
- timeout and retry faults;
- data-integrity faults;
- known implementation defect patterns;
- expert FMEA/FMECA analysis.

Mutants used to improve the VCS form \(\mathcal{M}_{\mathrm{dev}}\). A disjoint set \(\mathcal{M}_{\mathrm{holdout}}\), selected before final evaluation, estimates generalization:

\[
\mathcal{M}_{\mathrm{dev}}\cap \mathcal{M}_{\mathrm{holdout}}=\varnothing.
\]

Where possible, seed realistic historical faults in \(\mathcal{M}_{\mathrm{holdout}}\). Leakage between development and held-out faults must be reported.

### 4.8 Stage H — Execute and preserve evidence

For every execution, preserve:

- IUT build/hash;
- simulator and tool versions;
- configuration;
- seed and input file hashes;
- monotonic timestamps;
- packet trace;
- state/transition trace;
- oracle inputs and decision;
- environment health;
- final verdict.

### 4.9 Stage I — Evaluate and revise

Evaluate:

- T0/T1/T2 assurance tiers;
- held-out fault detection;
- VCS size and execution cost;
- surviving mutants;
- invalid/equivalent-mutant rate;
- inter-reviewer agreement;
- diagnostic accuracy, if diagnosis is enabled;
- calibration, if probabilistic inference is enabled.

Any surviving held-out fault triggers analysis of the requirement, model, purpose, oracle, or implementation gap. The VCS may then be revised, but the original held-out result remains reported.

### 4.10 Review and Inspection gates

| Gate | Primary static activity | Entry artifact | Exit criterion |
|---|---|---|---|
| **RG0 — Scope** | Review | Standard edition, services, roles, applicability draft | Scope and claim boundary approved |
| **RG1 — CRS** | Inspection + review | Independently extracted requirements | Source references, atomicity, applicability, and adjudication complete |
| **RG2 — Model and traceability** | Inspection + technical review | EFSM, requirement-transition map, \(\rho_{RT}\) | Model consistency and trace completeness approved |
| **RG3 — VC and oracle readiness** | Inspection + peer review | TP/VC catalog, oracle logic, reset plans | Cases executable, deterministic where required, and independently reviewable |
| **RG4 — Execution readiness** | Inspection | IUT configuration, tools, environment, data, logging | Configuration controlled and dry run accepted |
| **RG5 — Evidence integrity** | Inspection + analysis review | Raw traces, verdicts, mutations, exclusions | Evidence provenance, exclusions, and calculations reproducible |
| **RG6 — Claim release** | Independent review | Assurance argument, limitations, results, deviations | Claim wording matches achieved evidence gates and open risks |

Each gate produces signed findings and one of `APPROVE`, `APPROVE WITH ACTIONS`, or `REWORK`. The reviewer should be independent of the artifact author where interpretation, oracle correctness, or claim release is at stake.

---

## 5. Assurance Argument

### 5.1 Top-level claim

> For the fixed standard edition \(S\), applicability declaration \(P\), observation boundary \(O\), controlled environments \(E\), and evaluated fault set \(\mathcal{M}_{\mathrm{eval}}\), the recorded evidence supports the claim that the IUT exhibited behavior accepted by all validly executed base verification cases and that the VCS detected every evaluated non-equivalent fault member it was claimed to cover.

This is an evidence-backed scoped claim, not an unrestricted theorem about all possible IUT behavior.

### 5.2 Argument structure

```text
C0  Scoped conformance evidence is sufficient for the declared use.
|
+-- C1  The applicable requirement set is controlled and traceable.
|   +-- CRS, applicability declaration, adjudication log
|
+-- C2  Every applicable verification obligation has one or more cases.
|   +-- Relations rho_RT and rho_TV, coverage matrices
|
+-- C3  Executions are valid and verdicts are reproducible.
|   +-- Preconditions, resets, traces, oracle records, tool versions
|
+-- C4  Detection capability is bounded and measured.
|   +-- Fault domain, equivalent-mutant analysis, held-out results
|
+-- C5  Quantitative interpretations are calibrated and assumption-bounded.
|   +-- Calibration datasets, likelihood model, sensitivity analysis
|
+-- C6  Independent gates control artifact and claim quality.
    +-- Inspection records, review findings, approvals, open actions
```

### 5.3 Proposition 1 — Traceability composition

If every \(r\in R_{\mathrm{app}}\) is related to at least one \(t\in T\), and every such \(t\) is related to at least one \(v\in V\), then Equation (1) holds.

**Proof.** Fix arbitrary \(r\in R_{\mathrm{app}}\). By the first premise, choose \(t\) with \((r,t)\in\rho_{RT}\). By the second premise, choose \(v\) with \((t,v)\in\rho_{TV}\). Therefore the existential witnesses required by Equation (1) exist. Since \(r\) was arbitrary, the result holds for all applicable requirements. \(\square\)

This proposition proves trace composition only. It does not prove semantic adequacy of \(t\), \(v\), or the oracle.

### 5.4 Proposition 2 — Logical base/extended invariance

Let \(V_B\) be the base VCS and \(V_E\) an extended project-specific VCS. Define the base claim function:

\[
\Gamma_B:\mathrm{Results}|_{V_B}\rightarrow
\{\mathrm{supported},\mathrm{not\ supported},\mathrm{incomplete}\}.
\]

If \(\Gamma_B\) depends only on the projection of results onto \(V_B\), then adding \(V_E\) does not change the logical base claim for unchanged base results:

\[
\Gamma_B(\mathrm{Results}|_{V_B})
=
\Gamma_B((\mathrm{Results}\cup \mathrm{Results}_E)|_{V_B}).
\]

This is logical invariance, not execution isolation. Operational non-interference additionally requires reset, order, and environment controls.

### 5.5 Proposition 3 — Bounded mutant distinguishability

If Equation (4) holds, then every member of \(\mathcal{M}_{\mathrm{eval}}\) is distinguished from \(G\) by at least one case under the declared oracle and environment.

This follows directly from the definition of `Kill` in Equation (3). The proposition cannot be generalized beyond \(\mathcal{M}_{\mathrm{eval}}\) without a justified fault-domain relation.

---

## 6. Quantitative Evidence Without Semantic Conflation

### 6.1 Three quantities that must remain distinct

| Quantity | Meaning | Typical notation |
|---|---|---|
| **Coverage** | Whether a target has at least one adequate case | \(\mathrm{Cov}\) |
| **Operational repeatability** | PASS probability under a defined repeated-run regime | \(q_j\) |
| **Epistemic conformance belief** | Belief that a fixed conformance proposition is true, given a calibrated model and evidence | \(p_j\) |

Coverage is not a probability. Operational repeatability is not automatically conformance belief.

### 6.2 Operational repeatability model

For verification obligation \(j\), let valid repeated executions produce:

\[
Y_{j,r}=
\begin{cases}
1,&\mathrm{PASS}\\
0,&\mathrm{FAIL}.
\end{cases}
\]

Under a predeclared conditionally independent and identically distributed regime:

\[
Y_{j,r}\mid q_j\sim\mathrm{Bernoulli}(q_j).
\tag{7}
\]

If \(c_j\) of \(n_j\) valid runs pass:

\[
\hat q_j=\frac{c_j}{n_j}.
\tag{8}
\]

An exact two-sided \(1-\delta\) Clopper–Pearson interval is:

\[
\left[
B^{-1}\!\left(\frac{\delta}{2};c_j,n_j-c_j+1\right),
B^{-1}\!\left(1-\frac{\delta}{2};c_j+1,n_j-c_j\right)
\right],
\tag{9}
\]

with standard boundary conventions for \(c_j=0\) or \(c_j=n_j\).

The i.i.d. condition is not guaranteed by returning to the same protocol state. It requires controlled reset, stable configuration, randomized run order where appropriate, and analysis of shared-run or environmental effects. If overdispersion or clustering is present, use a beta-binomial, mixed-effects model, or cluster bootstrap.

`INCONCLUSIVE` and `ERROR` counts are reported separately and are not included in \(n_j\) without a predefined policy.

### 6.3 Calibrated conformance proposition

Let:

\[
C_j=
\begin{cases}
1,&\text{the fixed IUT conforms to obligation }j\\
0,&\text{the fixed IUT does not conform to obligation }j.
\end{cases}
\]

Define predictive rates for the declared IUT population and execution regime:

\[
s_j=P(Y=1\mid C_j=1)
\]

as the true-PASS probability (one minus the false-fail probability), and:

\[
b_j=P(Y=1\mid C_j=0)
\]

as the false-PASS, missed-detection, or escape probability. For the displayed
likelihood ratios, assume \(0<s_j<1\) and \(0<b_j<1\); boundary values require
the corresponding limiting likelihood and must not be handled by dividing
zero likelihoods.

For \(c\) PASS and \(f\) FAIL observations under conditional independence:

\[
L_1=s_j^c(1-s_j)^f,\qquad
L_0=b_j^c(1-b_j)^f.
\tag{10}
\]

The Bayes factor supporting conformance over non-conformance is:

\[
\mathrm{BF}_{10}=\frac{L_1}{L_0}.
\tag{11}
\]

Given a declared prior \(\pi_j=P(C_j=1)\):

\[
P(C_j=1\mid Y)=
\frac{\pi_j L_1}
{\pi_j L_1+(1-\pi_j)L_0}.
\tag{12}
\]

Equation (12) is valid only if \(s_j\), \(b_j\), conditional independence, and the prior are defensible. Prefer reporting the likelihood or Bayes factor together with posterior sensitivity over a range of priors.

### 6.4 Calibration requirements

- Estimate \(s_j\) using conforming reference implementations or independently adjudicated conforming executions.
- Estimate \(b_j\) using representative **held-out** nonconforming implementations or faults.
- Preserve uncertainty in \(s_j\) and \(b_j\); do not substitute point estimates without sensitivity analysis.
- Calibrate by fault class when detection differs materially across faults.
- Do not report a posterior if the calibration set is too small, unrepresentative, or reused to design the same test.

When these gates are not met, report T0–T2 evidence only.

### 6.5 Combining obligations

Let:

\[
p_j=P(C_j=1\mid \mathcal{E})
\]

for \(J\) obligations. Without a dependence model, the joint conformance probability satisfies the Fréchet bounds:

\[
\max\left(0,\sum_{j=1}^{J}p_j-(J-1)\right)
\le
P\left(\bigcap_{j=1}^{J}\{C_j=1\}\mid \mathcal{E}\right)
\le
\min_j p_j.
\tag{13}
\]

Therefore:

- \(\min_j p_j\) is an **upper**, not lower, bound on joint conformance;
- multiplying marginals requires independence;
- multiplying first-order conditionals requires a justified first-order Markov structure;
- a single scalar is not reported when the lower bound is uninformative.

The baseline report uses:

1. the obligation vector \((p_1,\ldots,p_J)\), when calibrated;
2. the dependence-free interval in Equation (13);
3. subgroup results by service, role, and fault class.

### 6.6 No unverified-element exclusion

If an applicable obligation has no valid evidence, it is marked `UNVERIFIED`. It is not removed from an aggregate to improve the result. The corresponding higher-level claim is `INCOMPLETE`.

---

## 7. Failure Diagnosis

### 7.1 Baseline diagnostic model

Let \(F\in\{f_0,f_1,\ldots,f_K\}\) denote no fault or a declared fault class. Let \(X\) be a failure-signature vector containing:

- VC verdicts;
- error codes;
- timeout signatures;
- packet/field anomalies;
- last accepted state/transition;
- retry counts;
- integrity-check results.

A Bayesian diagnostic model is:

\[
P(F=f\mid X=x)
\propto
P(X=x\mid F=f)P(F=f).
\tag{14}
\]

The likelihood is estimated from fault-injection data. A naive conditional-independence factorization may be used only as a declared baseline; correlated signatures require a Bayesian network, regularized classifier, or another validated model.

### 7.2 FMEA/FMECA relationship

FMEA/FMECA records:

- item or transition;
- failure mode and cause;
- local and global effects;
- severity;
- detecting VCs;
- corresponding fault operators;
- evidence status.

Severity is not a probability and is not inferred by the diagnostic classifier. Ranking suspected faults may combine posterior diagnostic probability and separately governed severity, but the combination rule must be explicit.

### 7.3 Evaluation

Evaluate diagnosis using fault-instance-level cross-validation or a held-out set. Report:

- confusion matrix;
- Top-1 and Top-3 accuracy;
- macro-averaged precision, recall, and F1;
- calibration if probabilities are emitted;
- results by fault class;
- abstention rate for low-confidence cases.

### 7.4 Decision rule for temporal diagnostic models

An HMM is justified only when:

- the hidden fault state is expected to change over time;
- the sequence index has a consistent physical meaning;
- transition and emission parameters are identifiable;
- sufficient temporal fault data exist;
- HMM performance exceeds simpler diagnostic baselines.

A fixed implementation fault observed across a sequence of tests does not automatically satisfy these conditions. HMM/Viterbi analysis is therefore a future candidate, not a core method.

---

## 8. Evaluation Design

### 8.1 Baselines

Compare:

| ID | Method |
|---|---|
| **B0** | Existing engineering/ICD test set |
| **B1** | Requirement traceability only |
| **B2** | Requirement + EFSM obligation coverage |
| **B3** | B2 refined using development mutants |

### 8.2 Primary metrics

- applicable requirement coverage;
- obligation coverage by category;
- state, transition, guard, and data-partition coverage;
- development mutation score;
- held-out fault detection rate with interval estimates;
- VCS size;
- derivation and review effort;
- review-defect density, action-closure rate, and downstream defect-escape rate;
- gate turnaround time and rework effort;
- execution time;
- invalid/equivalent-mutant rate;
- surviving-fault analysis;
- reviewer agreement.

### 8.3 Quantitative-evidence metrics

When T3 is enabled:

- Brier score;
- log loss;
- reliability/calibration curve;
- Expected Calibration Error with binning sensitivity;
- posterior sensitivity to priors and calibration uncertainty;
- coverage of stated intervals where repeated datasets are available.

### 8.4 Diagnostic metrics

- Top-1/Top-3 accuracy;
- macro F1;
- per-class recall;
- abstention-performance curve;
- time-to-localization;
- comparison with severity-only FMEA ranking.

### 8.5 Experimental controls

- pre-register the final fault operators and held-out split;
- version all tools, cases, models, and datasets;
- randomize execution order when order effects are plausible;
- reset the IUT between cases according to the case schema;
- separate test-design personnel from held-out fault adjudication where practical;
- preserve negative results and surviving faults;
- use fixed seeds plus repeated independent seeds for stochastic tools.

---

## 9. Synthetic Worked Example

This section demonstrates calculations only. It is **not** ARINC 615A evidence.

### 9.1 Single-obligation evidence

Suppose calibration for obligation \(j\) establishes:

\[
s_j=0.95,\qquad b_j=0.20.
\]

The IUT then produces four PASS and one FAIL observation:

\[
c=4,\qquad f=1.
\]

From Equation (10):

\[
L_1=0.95^4(0.05),\qquad
L_0=0.20^4(0.80).
\]

Therefore:

\[
\mathrm{BF}_{10}
=
\frac{0.95^4(0.05)}{0.20^4(0.80)}
\approx31.817.
\]

For prior \(\pi_j=0.5\):

\[
P(C_j=1\mid Y)\approx0.9695.
\]

The posterior depends on the prior:

| Prior \(\pi_j\) | Posterior |
|---:|---:|
| 0.1 | 0.7795 |
| 0.5 | 0.9695 |
| 0.9 | 0.9965 |

This sensitivity is why the Bayes factor and prior range must accompany the posterior.

### 9.2 Multiple obligations

Suppose three calibrated obligation posteriors are:

\[
(p_1,p_2,p_3)=(0.97,0.95,0.96).
\]

Without a dependence model, Equation (13) gives:

\[
\max(0,0.97+0.95+0.96-2)
\le P(C_1\land C_2\land C_3\mid \mathcal{E})
\le0.95,
\]

so:

\[
0.88\le P(C_1\land C_2\land C_3\mid \mathcal{E})\le0.95.
\]

Under an additional independence assumption, the product would be:

\[
0.97\times0.95\times0.96=0.88464.
\]

The product is not used unless independence is justified. The dependence-free interval remains the baseline.

### 9.3 Mutation evidence

If five development mutants are killed, the defensible statement is:

> The VCS killed 5/5 valid, non-equivalent mutants in the declared development set.

It is not:

> Diagnostic coverage is at least 100%.

Generalization must be evaluated using \(\mathcal{M}_{\mathrm{holdout}}\) or real defects.

---

## 10. Evidence Gates and Research Decision Rules

| Gate | Requirement | If not met |
|---|---|---|
| **G0 — Scope** | Standard edition, roles, services, PICS-like applicability fixed | No base claim |
| **G1 — Traceability** | Equations (1) and (2) satisfied and reviewed | T0 incomplete |
| **G2 — Execution validity** | Preconditions, reset, environment, and oracle evidence valid | Exclude run as ERROR/INCONCLUSIVE |
| **G3 — Fault-domain quality** | Valid/equivalent handling and held-out split complete | No T2 generalization |
| **G4 — Calibration** | Representative estimates of \(s_j,b_j\) with uncertainty | No conformance posterior |
| **G5 — Dependence** | Dependence model justified and validated | Use Fréchet bounds/vector only |
| **G6 — Diagnosis** | Held-out diagnostic performance exceeds baseline | Do not claim automated localization |
| **G7 — Transferability** | Second protocol instance completed | Do not claim protocol independence |

These gates define what the project may claim at each stage. Engineering progress does not waive a failed research gate.

---

## 11. Threats to Validity

### 11.1 Construct validity

- Normative requirements may be split or interpreted incorrectly.
- Mutants may not represent real non-conformance.
- PASS/FAIL oracles may omit relevant observables.
- A posterior may reflect the calibration set more than the target IUT population.

### 11.2 Internal validity

- Shared state or environment can violate run independence.
- Development mutants can leak into held-out evaluation.
- Tool defects can be misclassified as IUT failures.
- Execution order may affect results.

### 11.3 External validity

- One ARINC 615A implementation does not establish transferability.
- A simulator may not reproduce target-network timing or hardware behavior.
- Results for TFTP-centered services may not transfer to stateless, broadcast, or real-time protocols.

### 11.4 Conclusion validity

- Small fault sets produce wide uncertainty.
- Equivalent-mutant classification may be subjective.
- Multiple comparisons and class imbalance may inflate diagnostic conclusions.
- Point estimates without uncertainty can overstate evidence.

Mitigations include dual review, adjudication logs, held-out faults, negative-result preservation, sensitivity analysis, replication packages, and a second protocol instance.

---

## 12. Reproducibility Package

The research release should contain, subject to proprietary-text restrictions:

```text
docs/requirements/
  applicability.yaml
  crs.csv
  crs_adjudication.md
models/
  a615a_efsm.*
  requirement_transition_map.csv
verification/
  test_purposes.yaml
  verification_cases/
  traceability_matrix.csv
faults/
  operators.yaml
  mutant_manifest.csv
  equivalence_decisions.csv
experiments/
  preregistration.md
  environments/
  raw/
  processed/
analysis/
  coverage.*
  mutation.*
  calibration.*
  diagnosis.*
```

Every reported table and figure must be reproducible from versioned raw data and scripts. Proprietary standard text is represented by stable references and hashes, not copied into public artifacts.

---

## 13. Research Roadmap

### Phase 1 — Defensible testing core

1. Freeze scope and applicability.
2. Pass RG0 scope review.
3. Extract and adjudicate the complete CRS; pass RG1.
4. Build the observable ARINC 615A EFSM and trace model; pass RG2.
5. Derive TPs and VCs, validate oracle logic, and pass RG3.
6. Complete traceability and obligation coverage.

**Research output:** T0 methodology and artifacts.

### Phase 2 — Bounded adequacy

7. Define fault operators and FMEA/FMECA mapping.
8. Build development and held-out fault sets.
9. Pass RG4 execution-readiness inspection.
10. Execute mutation and held-out evaluation.
11. Reproduce the evidence package and pass RG5.
12. Compare B0–B3 baselines.

**Research output:** T1/T2 evidence and empirical evaluation.

### Phase 3 — Calibrated evidence and diagnosis

13. Calibrate false-fail and missed-detection behavior.
14. Evaluate Bayes factors, posteriors, and sensitivity.
15. Train and evaluate the baseline diagnostic model.
16. Consider HMM/Bayesian-network extensions only if supported by data.
17. Pass RG6 before releasing any quantitative conformance claim.

**Research output:** optional T3 evidence.

### Phase 4 — Transferability

18. Apply the method to a second protocol selected for contrasting characteristics.
19. Identify invariant and protocol-specific steps.
20. Revise the claimed contribution based on cross-instance evidence.

**Research output:** evidence for or against protocol independence.

---

## 14. Conclusion

This report establishes an integrated Test-and-Analysis methodology for constructing and evaluating a scoped ARINC 615A conformance-assurance argument.

The **Test path** operationalizes applicable requirements as controlled stimuli, observable behavior, executable oracles, verdicts, and reproducible traces. The **Analysis path** determines which obligations were covered, how well the VCS detects declared fault classes, what uncertainty the observations support, and which verification action should follow. Neither path is sufficient alone: Analysis without Test lacks controlled empirical observations, while Test without Analysis cannot justify the scope or strength of its conclusions.

Independent Review and Inspection gates turn this research logic into an engineering control system. They prevent unresolved ambiguity, incomplete traceability, weak oracle logic, uncontrolled execution configurations, irreproducible evidence, and overstated claims from propagating downstream.

The central academic contribution is a precise separation of semantics—coverage, valid execution, bounded detection adequacy, operational repeatability, calibrated belief, and diagnosis—together with propositions and experiments that can evaluate their relationships. The central engineering contribution is a reusable artifact chain and decision process that directs effort toward observable risk, preserves evidence, exposes rework early, and supports auditable release decisions.

The methodology therefore provides a research baseline and an engineering operating model. Its value will be established incrementally through the evidence gates in §10, independent review gates in §4.10, held-out-fault studies, calibration experiments, and a second-protocol replication.

---

## Appendix A — Symbol Table

| Symbol | Meaning |
|---|---|
| \(S\) | Fixed protocol-standard edition |
| \(P\) | Implementation applicability declaration |
| \(O\) | Declared observation boundary |
| \(R(S)\) | Extracted normative requirement items |
| \(R_{\mathrm{app}}\) | Requirements applicable to \(P\) |
| \(T\) | Test Purpose set |
| \(V\) | Verification Case set |
| \(\rho_{RT}\) | Requirement-to-Test-Purpose relation |
| \(\rho_{TV}\) | Test-Purpose-to-Verification-Case relation |
| \(G\) | Observable EFSM specification |
| \(\mathcal{M}_{\mathrm{exec}}\) | Buildable and executable mutant set |
| \(\mathcal{M}_{\mathrm{equiv}}\) | Executable mutants equivalent within the observation scope |
| \(\mathcal{M}_{\mathrm{eval}}\) | Evaluated valid, non-equivalent fault set |
| \(\mathcal{E}\) | Recorded evidence dataset |
| \(q_j\) | Operational PASS probability for obligation \(j\) |
| \(C_j\) | Fixed latent conformance proposition for obligation \(j\) |
| \(s_j\) | \(P(\mathrm{PASS}\mid C_j=1)\) |
| \(b_j\) | \(P(\mathrm{PASS}\mid C_j=0)\) |
| \(\pi_j\) | Prior probability for \(C_j=1\) |
| \(p_j\) | Posterior probability \(P(C_j=1\mid \mathcal{E})\) |

---

## Appendix B — Minimum Reporting Checklist

- [ ] Standard edition and exact scope fixed
- [ ] Applicability declaration versioned
- [ ] CRS independently reviewed and adjudicated
- [ ] All source clauses referenced by clause/table/page
- [ ] Requirement, TP, VC, and model relations exported
- [ ] Mandatory obligation categories fully covered
- [ ] EFSM variables include relevant history, counters, options, and retry state
- [ ] Verdict includes PASS/FAIL/INCONCLUSIVE/ERROR
- [ ] Reset and isolation procedures defined
- [ ] Mutants classified as valid/equivalent/invalid
- [ ] Development and held-out fault sets separated
- [ ] Mutation results include uncertainty and survivors
- [ ] No posterior reported without calibration
- [ ] No scalar aggregate reported without dependence analysis
- [ ] Diagnostic results evaluated on held-out fault instances
- [ ] Raw data, scripts, versions, and seeds preserved
- [ ] Negative and inconclusive results retained
- [ ] Claim boundaries remain consistent across scope, results, and conclusion

---

## References

[1] ISO/IEC 9646-1:1994. *Information technology — Open Systems Interconnection — Conformance testing methodology and framework — Part 1: General concepts.*

[2] ISO/IEC 9646-2:1994. *Information technology — Open Systems Interconnection — Conformance testing methodology and framework — Part 2: Abstract Test Suite specification.*

[3] ETSI TR 102 840 V1.2.1 (2011). *Methods for Testing and Specifications (MTS); Model-based testing in standardisation.*

[4] Tretmans, J. (1996). Conformance Testing with Labelled Transition Systems: Implementation Relations and Test Generation. *Computer Networks and ISDN Systems*, 29(1), 49–79. https://doi.org/10.1016/S0169-7552(96)00017-7

[5] Chow, T. S. (1978). Testing Software Design Modeled by Finite-State Machines. *IEEE Transactions on Software Engineering*, SE-4(3), 178–187.

[6] Fujiwara, S., von Bochmann, G., Khendek, F., Amalou, M., & Ghedamsi, A. (1991). Test Selection Based on Finite State Models. *IEEE Transactions on Software Engineering*, 17(6), 591–603.

[7] Petrenko, A., Nguena Timo, O., & Ramesh, S. (2016). Test Generation by Constraint Solving and FSM Mutant Killing. In *ICTSS 2016*, LNCS 9976, 36–51. https://doi.org/10.1007/978-3-319-47443-4_3

[8] Jia, Y., & Harman, M. (2011). An Analysis and Survey of the Development of Mutation Testing. *IEEE Transactions on Software Engineering*, 37(5), 649–678. https://doi.org/10.1109/TSE.2010.62

[9] Yang, Z., Huang, R., Cui, C., Niu, N., & Towey, D. (2025). Requirements-Based Test Generation: A Comprehensive Survey. *ACM Transactions on Software Engineering and Methodology*. https://doi.org/10.1145/3771727

[10] Li, Y., Pierce, B. C., & Zdancewic, S. (2021). Model-Based Testing of Networked Applications. In *ISSTA 2021*, 529–539. https://doi.org/10.1145/3460319.3464798

[11] DeMillo, R. A., Lipton, R. J., & Sayward, F. G. (1978). Hints on Test Data Selection: Help for the Practicing Programmer. *Computer*, 11(4), 34–41.

[12] Clopper, C. J., & Pearson, E. S. (1934). The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial. *Biometrika*, 26(4), 404–413.

[13] Jeffreys, H. (1946). An Invariant Form for the Prior Probability in Estimation Problems. *Proceedings of the Royal Society A*, 186(1007), 453–461.

[14] IEC 60812:2018. *Failure modes and effects analysis (FMEA and FMECA).*

[15] Rabiner, L. R. (1989). A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition. *Proceedings of the IEEE*, 77(2), 257–286.

[16] RTCA DO-178C (2011). *Software Considerations in Airborne Systems and Equipment Certification.* Used as adjacent software-assurance context; this report does not claim direct certification compliance.

[17] ARINC 615A-4. *Software Data Loader Using Ethernet Interface.* Exact clauses and pages shall be recorded in the controlled CRS.

[18] NIST. *Conformance Testing.* https://www.nist.gov/itl/ai/applied-ai-research-group/conformance-testing

[19] NASA (2016). *NASA Systems Engineering Handbook*, NASA/SP-2016-6105 Rev 2. https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf

[20] ISO/IEC 20246:2017. *Software and systems engineering — Work product reviews.* https://www.iso.org/standard/67407.html

---

*AI-assisted research disclosure: AI tools assisted with drafting and consistency checking. Mathematical claims, standard interpretations, references, and experimental conclusions require accountable human review. The report does not state that a reference has been verified unless its bibliographic metadata and the cited proposition have both been checked.*
