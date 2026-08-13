# A Test-and-Analysis Methodology for ARINC 615A Conformance Verification
<!-- Bilingual controlled edition: authoritative English followed by Chinese translation. -->
## Requirements-Based Testing, Bounded Evidence Analysis, and Independent Review Gates

**Research Report RR-2026-001**

| Field | Value |
|---|---|
| **Version** | 4.2 research baseline |
| **Date** | 2026-07-30 |
| **Status** | Effective and frozen through PR #6 under GR-PR6-RB-2026-001-v4.2; empirical claims remain conditional on §10 |
| **Primary instance** | ARINC 615A DOWNLOAD/UPLOAD services over TFTP |
| **Classification** | Internal — Academic Research |
| **Normative language** | The English section is authoritative; a synchronized Chinese translation is appended to this file |

---

## Abstract

Protocol conformance verification must convert normative requirements into credible engineering decisions. It therefore needs both dynamic evidence from executing an Implementation Under Test (IUT) and disciplined analysis of coverage, detection capability, uncertainty, and failure causes. This report presents an integrated Test-and-Analysis methodology for ARINC 615A conformance verification.

The **Test path** derives an applicable Conformance Requirement Set (CRS), Test Purposes (TPs), and executable Verification Cases (VCs), then executes them against the IUT to produce verdicts, timestamped traces, and measurements. The **Analysis path** evaluates traceability, model-based coverage, deterministic timing conformance, finite-fault-domain adequacy, repeated-run behavior, calibrated evidence, and failure diagnosis. Test and Analysis are complementary: Test creates controlled observations; Analysis determines what those observations support and where further verification effort is needed.

Independent **Review and Inspection gates** govern the quality of requirements, protocol models, verification cases, oracles, execution readiness, evidence packages, and released claims. These static activities support the two primary paths without being presented as independent research contributions. Demonstration may support stakeholder acceptance, but it is not the principal method for detailed protocol conformance.

The resulting framework aims to create both academic value—clear semantics, bounded claims, and empirically evaluable hypotheses—and engineering value—reviewable artifacts, automation points, release gates, diagnostic outputs, and reproducible decision records.

**Keywords:** protocol conformance verification; Test-and-Analysis; requirements-based testing; engineering assurance; traceability; timed EFSM; robust timing oracle; measurement uncertainty; ARINC 615A; finite fault domain; mutation testing; calibrated evidence; Bayesian inference; review gate; inspection

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
3. **Deterministic timed-conformance semantics.** Timestamped traces, clock-augmented EFSMs, explicit measurement-error budgets, and robust verdict rules prevent timing measurements from being treated as exact.
4. **Scoped assurance argument.** A formal separation between coverage, valid execution, and bounded fault-detection evidence.
5. **Finite fault-domain adequacy method.** A reproducible mutation workflow with explicit equivalent/invalid-mutant handling and held-out evaluation faults, including timing faults.
6. **Calibrated evidence semantics.** A separation between operational PASS probability, likelihood evidence, and posterior belief in conformance.
7. **Independent quality gates.** Review and Inspection gates covering scope, requirements, models, cases, oracles, execution readiness, evidence, and claim release.
8. **Evaluation protocol.** An empirically testable design with baselines, metrics, leakage controls, and decision gates.

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
- Alur and Dill provide the clock, guard, and reset foundations of timed
  automata [21]. This report uses a clock-augmented EFSM adaptation rather than
  claiming full timed-automata equivalence.
- JCGM 100 provides general rules for expressing measurement uncertainty [22],
  while JCGM 106 addresses the role of uncertainty in conformity assessment
  [23]. The robust interval verdict in §3.6 is this methodology's conservative
  decision rule and must still be validated for the timing instrument.
- NASA systems-engineering guidance commonly classifies requirement verification methods as Test, Analysis, Inspection, and Demonstration [19]. Review is treated here as a static governance activity aligned with software review practice rather than forced into that four-method taxonomy [20].

The intended novelty is the **auditable integration and empirical evaluation** of these ideas for ARINC 615A: a complementary Test-and-Analysis loop, applicability-controlled requirement extraction, obligation-sensitive traceability, uncertainty-aware timed conformance, explicit finite-fault-domain bounds, held-out fault evaluation, calibrated evidence gates, and independent artifact reviews. Until the artifacts and experiments in §§8–10 are completed, this novelty remains a research hypothesis rather than an established result.

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
| **Protocol model** | Describe legal observable behavior, including normative real-time constraints | clock-augmented EFSM/timed IOLTS \(G_T\) | Not required |
| **Traceability model** | Link requirements, purposes, cases, and model targets | Relations \(\rho\) | No |
| **Evidence record** | Preserve execution conditions, observations, and verdicts | Dataset \(\mathcal{E}\) | Observations only |
| **Inference/diagnosis model** | Interpret calibrated evidence | Likelihood/Bayesian model | Yes, if calibrated |

The protocol model is not an evidence model. An edge in the protocol graph denotes a possible or required behavior; it is not assigned a "transition probability" merely because confidence evidence is attached to it.

### 2.3 Assurance tiers

> **v4.3 supersession note.** Under candidate baseline `RB-2026-001-v4.3`
> ([`CR-2026-004`](../../../docs/control/changes/CR-2026-004.md)), the single
> T0–T3 ladder below is superseded by two orthogonal axes:
> certification-oriented assurance states **A0–A4** and research-evidence maturity
> states **R0–R5**. A single execution `PASS` no longer automatically satisfies an
> objective or supports a claim; objective and compliance status are reviewed
> conclusions. Mutation, calibration, diagnosis, and transferability become
> research-only and do not grant certification status. The T0–T3 descriptions
> are retained below as the historical wording and are still valid only under the
> `RB-2026-001-v4.2` baseline; they are not silently relabeled in v4.3.
> Mathematical and timed-conformance semantics are unchanged.

| Tier | Claim | Minimum supporting artifacts |
|---|---|---|
| **T0 — Traceability** | Every applicable requirement is linked to at least one executable case | CRS, TP/VC relations |
| **T1 — Observed conformance** | The IUT produced acceptable observations for the executed cases under recorded conditions | T0 + valid execution records |
| **T2 — Bounded detection adequacy** | The VCS distinguishes the specification from every non-equivalent member of the declared evaluated fault set | T1 + mutation/fault results |
| **T3 — Calibrated evidence** | Evidence changes belief in specified conformance propositions according to a validated observation model | T2 + calibration and sensitivity analysis |

Higher tiers do not erase the boundaries of lower tiers. A Tier T3 number cannot compensate for missing traceability or invalid executions. Under v4.3, T0 corresponds to A1 traceable definition, T1 to A2/A3 valid evidence and reviewed objective satisfaction, and T2/T3 to R2–R5 research maturity, not to higher certification-oriented assurance.

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
v=(id,\ role,\ pre,\ stimulus,\ oracle,\ refs,\ targets,\ reset,\ timingSchema,\ evidenceSchema).
\]

Where:

- `pre` defines executable preconditions;
- `stimulus` defines controlled actions and inputs;
- `oracle` maps observations to a verdict;
- `refs\subseteq R_{\mathrm{app}}` records requirement references;
- `targets` records EFSM states, transitions, data partitions, timing bounds, and fault classes;
- `reset` defines isolation and state restoration;
- `timingSchema` defines the time source, timestamp locations, clock resets, trigger/response pairing, admissible interval, and measurement-error budget;
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

### 3.6 Deterministic timed-conformance model

Four different notions must not be conflated:

1. **logical sequence**, meaning the order of protocol events;
2. **normative real time**, meaning deadlines, minimum delays, retry intervals, and timeout behavior;
3. **run-order dependence**, meaning drift, clustering, warm-up, or state leakage across executions;
4. **latent temporal dynamics**, meaning a hidden fault or degradation state that genuinely changes over physical time.

The first two belong to the core conformance model. The third belongs to experimental analysis. The fourth is an optional diagnostic extension and does not follow from an EFSM trace.

Let an observed timed trace be:

\[
\sigma_T=\bigl((a_0,t_0),(a_1,t_1),\ldots,(a_m,t_m)\bigr),
\qquad t_0\le t_1\le\cdots\le t_m,
\tag{T1}
\]

where timestamps use a declared monotonic time basis. For a trigger event
\(a_i\) and its requirement-defined response \(a_j\), define
\(\Delta t_{ij}=t_j-t_i\). Each requirement declares an admissible set
\(I_r\), including the inclusivity of each finite endpoint. A bounded response
obligation is:

\[
a_i@t_i\Longrightarrow
\exists j>i:
a_j@t_j\land \Delta t_{ij}\in I_r,
\tag{T2}
\]

The timing catalog defines event predicates
\(\mathrm{Trig}_r\), \(\mathrm{Resp}_r\), \(\mathrm{Cancel}_r\), and
\(\mathrm{Supersede}_r\), plus a correlation key and an explicit pairing policy
(for example unique-key, FIFO, or most-recent). A trigger creates a distinct
active obligation instance. A response discharges only the active instance
selected by the declared key and pairing policy; an ambiguous or invalid match
is `ERROR`, not an IUT `FAIL`. A matching cancellation closes the selected
instance as cancelled at its trace index, so later silence cannot produce a
no-response `FAIL`. Unless the requirement explicitly permits concurrent
instances, a superseding trigger closes the old instance as superseded and
starts a new instance with a new clock origin. Cancellation and supersession
are obligation dispositions, not timing verdicts, and remain in the trace.
Equal timestamps are ordered by trace index, so an event can affect an
obligation only when its index is later than the trigger. A requirement with no
minimum delay uses \(L_r=0\). Silence through the deadline is a timed
observation, not missing data.

For an observation horizon \(t_H\), encode an active obligation with no observed
response by the distinguished trace event \(\bot_r@t_H\):

\[
\bot_r@t_H
\ \Longleftrightarrow\
\mathrm{active}_r(i,t_H)
\land (t_H-t_i>U_r)
\land
\nexists j>i:\bigl(a_j\in\mathrm{Resp}_r\bigr)\land(t_i<t_j\le t_H).
\]

Here \(\mathrm{active}_r(i,t_H)\) means that the instance created at index
\(i\) has not been discharged, cancelled, or superseded under those matching
rules through horizon \(t_H\). The displayed strict inequality defines
\(\bot_r@t_H\) for a closed upper bound, where a response exactly at \(U_r\)
is admissible. For an open upper bound, the corresponding expiry test is
\(t_H-t_i\ge U_r\). Thus \(\bot_r@t_H\) is a formal observation of an expired,
still-active obligation with no matching response, not a synonym for an absent
log record.

The clock-augmented observable EFSM is:

\[
G_T=(Q,q_0,X,C,\Sigma_I,\Sigma_O,\Delta_T,\mathrm{Inv}),
\tag{T3}
\]

where \(C\) is a finite set of clocks, \(\mathrm{Inv}\) contains state invariants, and a timed transition contains a data guard, a clock guard, and a set of clocks to reset:

\[
\tau_T=(q,input,g_X(X),g_C(C),action(X),reset_C,output,q').
\]

\(G_T\) remains deterministic or nondeterministic according to its declared protocol semantics; it is not a stochastic process.

Timing observations are not exact. Let:

\[
\widehat{\Delta t}_{ij}=\Delta t_{ij}+e_{ij},
\qquad |e_{ij}|\le\varepsilon_{ij},
\qquad
I_{\mathrm{obs}}=
[\widehat{\Delta t}_{ij}-\varepsilon_{ij},
 \widehat{\Delta t}_{ij}+\varepsilon_{ij}]
\cap D_r,
\tag{T4}
\]

where \(\varepsilon_{ij}\) is a justified bound from a reviewed, versioned
budget applicable to the declared environment and measurement path. The budget
enumerates clock resolution/quantization, clock accuracy and drift, timestamp
insertion location, scheduler latency, network-capture latency, software-layer
processing latency, inter-device synchronization error, and common path or
instrument bias. Each component records its source, bound, sign model, and
correlation class. Algebraically common terms may be removed only when the same
error enters both timestamps with the same sign and the reviewed measurement
design demonstrates cancellation. Independence alone does not justify
root-sum-square reduction of a worst-case conformance bound; independent
components and shared bias remain distinguished, and any probabilistic
combination is reported separately from \(\varepsilon_{ij}\). The physical
domain is \(D_r=[0,\infty)\) only when non-negative delay is
a reviewed property of the trigger/response and timestamp design; otherwise
\(D_r=\mathbb{R}\). If the intersection is empty, the observation contradicts
the declared measurement model and the execution is `ERROR`, not a clamped
verdict.

For the declared allowed interval \(I_r\), whether closed, open, or half-open,
the robust timing oracle is:

\[
\mathrm{TimingVerdict}_r=
\begin{cases}
\mathrm{PASS},& I_{\mathrm{obs}}\subseteq I_r,\\
\mathrm{FAIL},& I_{\mathrm{obs}}\cap I_r=\varnothing,\\
\mathrm{INCONCLUSIVE},&\text{otherwise}.
\end{cases}
\tag{T5}
\]

If the time source, timestamp chain, trigger/response pairing, or declared
error bound is invalid, the execution is `ERROR`, not `INCONCLUSIVE`.
This set-containment rule is deliberately conservative near a boundary:
measurement resolution cannot be converted into false precision.
For \(\bot_r@t_H\) with a closed upper bound, a no-response `FAIL` is robust
only when the earliest admissible elapsed horizon satisfies
\(\widehat{\Delta t}_{iH}-\varepsilon_{iH}>U_r\) and the obligation remains
active. For an open upper bound, the corresponding test is
\(\widehat{\Delta t}_{iH}-\varepsilon_{iH}\ge U_r\). Otherwise the result is
`INCONCLUSIVE` or `ERROR` according to the preceding rules. In particular, a
nominal timeout smaller than the measurement-error margin is not a `FAIL`.

Every applicable timing requirement must trace to:

- its trigger, response, cancellation, supersession, correlation/pairing,
  concurrency, and silence semantics;
- \(L_r,U_r\), units, clock start/reset events, and source reference;
- the observation points and monotonic time basis;
- a reviewed error-budget ID/version, applicable environment, component sources,
  correlation/common-bias rationale, and resulting \(\varepsilon_{ij}\);
- early, nominal, boundary, late, and no-response partitions as applicable.

### 3.7 Finite fault domain

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

### 3.8 Weighted mutation score

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

### 4.3 Stage C — Build the clock-augmented observable EFSM

1. Define externally observable states and variables.
2. Extract every applicable timing obligation into trigger, response, cancellation, silence, lower/upper bound, unit, and reset semantics.
3. Encode data guards, clock guards, state invariants, clock resets, options, retry counters, timeout conditions, block-number behavior, and terminal states.
4. Link each state, transition, timing constraint, and reset to requirements.
5. Review the model and its observability against the CRS.
6. Treat every protocol-specific claim, including rollover and timing rules, as unresolved until it has an exact standard reference.

**Exit artifact:** clock-augmented EFSM, timing-obligation catalog, and requirement-to-model relation.

### 4.4 Stage D — Derive Test Purposes

For each applicable requirement and obligation type, derive purposes using:

- nominal behavior;
- invalid input or forbidden output;
- equivalence-class and boundary values;
- state/transition reachability;
- timeout and retry thresholds;
- duplicate, reordering, and sequence faults;
- end-to-end session sequences where required.
- for every bounded timing obligation, early, nominal, lower/upper-boundary,
  late, and no-response partitions where semantically applicable.

Test Purpose derivation is human-reviewed. Automated generation may propose candidates but cannot silently establish normative meaning.

**Exit artifact:** TP catalog and \(\rho_{RT}\).

### 4.5 Stage E — Specify Verification Cases

Each case includes:

- stable identifier and version;
- role allocation;
- initial IUT and peer state;
- exact test data and partitions;
- steps and controlled timing;
- time source, timestamp locations, trigger/response pairing, clock resets,
  admissible interval, and measurement-error budget;
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
- timing-partition and clock-reset coverage;
- negative/error coverage;
- required sequence coverage.

A single aggregate percentage is not used to conceal a missing mandatory category.

### 4.7 Stage G — Construct the fault domain

Fault operators are derived from:

- requirement misinterpretations;
- EFSM guard/action/target changes;
- field encoding faults;
- timeout/retry threshold shifts, missing or spurious clock resets, wrong timer
  start events, non-monotonic time sources, and cross-session timer leakage;
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
- timestamp-source identity, resolution, uncertainty budget, and clock/reset events;
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
- robust timing verdicts, timing-bound/partition coverage, and observed
  measurement-margin distribution;
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
| **RG2 — Model and traceability** | Inspection + technical review | Clock-augmented EFSM, timing catalog, requirement-model map, \(\rho_{RT}\) | Discrete/timed model consistency, observability, and trace completeness approved |
| **RG3 — VC and oracle readiness** | Inspection + peer review | TP/VC catalog, robust oracle logic, reset and uncertainty plans | Cases executable; trigger/response, timing bounds, uncertainty, and verdict semantics independently reviewable |
| **RG4 — Execution readiness** | Inspection | IUT configuration, tools, clocks, timestamp chain, environment, data, logging | Configuration and timing instrument controlled; error budget and dry run accepted |
| **RG5 — Evidence integrity** | Inspection + analysis review | Timestamped raw traces, verdicts, mutations, exclusions, derived timing results | Evidence provenance, clock metadata, exclusions, and calculations reproducible |
| **RG6 — Claim release** | Independent review | Assurance argument, limitations, results, deviations | Claim wording matches achieved evidence gates and open risks |

Each gate produces signed findings and one of `APPROVE`, `APPROVE WITH ACTIONS`, or `REWORK`. The reviewer should be independent of the artifact author where interpretation, oracle correctness, or claim release is at stake.

---

## 5. Assurance Argument

> **v4.3 supersession note.** Under candidate baseline `RB-2026-001-v4.3`
> ([`CR-2026-004`](../../../docs/control/changes/CR-2026-004.md)), the argument
> below is reinterpreted through the certification-oriented chain: obligation →
> Verification Objective → verification activity → evidence → reviewed Objective
> Satisfaction → Compliance Evidence Index. The claims C0–C6 still describe the
> engineering substance but are reclassified: C1–C3 map to assurance states
> A1–A3, while C4–C5 (detection adequacy and calibration) are research-evidence
> claims mapped to R2–R5 and are not higher certification-oriented assurance
> tiers. The mathematical propositions 1–3 below are unchanged; only their
> role in the assurance argument is clarified. Internal gates are project-defined
> and are not authority review gates.

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
|   +-- Preconditions, resets, timestamped traces, robust oracle records,
|       clock metadata, uncertainty budgets, tool versions
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

> **v4.3 supersession note.** Under candidate baseline `RB-2026-001-v4.3`, the
> calibrated conformance belief of section 6.3 is classified as a
> **research-evidence** claim (R4 maturity), not a certification-oriented
> assurance claim. Failure to reach a calibrated interpretation does not block
> certification-oriented closure (A4). A calibrated posterior is not required to
> establish ordinary protocol verification evidence, and Bayesian or statistical
> calibration is not a certification objective. The equations and measurement
> semantics of this section are unchanged; only their classification within the
> assurance model is clarified by v4.3.

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

Equation (13) assumes that every \(p_j\) is itself a defensible marginal for
the target proposition and evidence regime. A common uncalibrated instrument
bias can shift several marginals together; the algebraic Fréchet bounds do not
remove that shared measurement bias. The project must model or bound the
common bias, recalibrate with independent reference evidence, or withhold the
joint scalar claim.

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
| **B2-U** | Requirement + untimed EFSM obligation coverage |
| **B2-T** | B2-U + clock-augmented EFSM, timing partitions, and robust timing oracle |
| **B3** | B2-T refined using development mutants |

### 8.2 Primary metrics

- applicable requirement coverage;
- obligation coverage by category;
- state, transition, guard, and data-partition coverage;
- timing-bound, timing-partition, and clock-reset coverage;
- robust timing PASS/FAIL/INCONCLUSIVE/ERROR counts;
- held-out timing-fault detection and false-verdict rate;
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

### 8.3 Timed-conformance analysis

For each timing obligation \(r\), report:

- the allowed interval \(I_r\), observation interval \(I_{\mathrm{obs}}\), and
  signed margin to each boundary;
- the time source, resolution, error-budget components, and trigger/response
  pairing rule;
- robust verdict counts by timing partition and environment;
- held-out detection by timing-fault operator;
- median and declared upper quantiles of observed delay as operational
  performance descriptors, never as substitutes for the deterministic verdict;
- order, batch, reset, autocorrelation, clustering, and drift diagnostics.

Let \(D_{r,k}\) be the measured delay for valid repetition \(k\), and define
\(Y^{(T)}_{r,k}=1\) only when the robust timing verdict is PASS. Then
\(\widehat q^{(T)}_r=\sum_kY^{(T)}_{r,k}/n_r\) estimates operational timing-PASS
probability under the declared repeated-run regime. It is not the probability
that a fixed IUT conforms. If order, batch, or shared-state effects are present,
use a beta-binomial, mixed-effects model, or cluster bootstrap rather than an
i.i.d. Bernoulli interval.

### 8.4 Quantitative-evidence metrics

When T3 is enabled:

- Brier score;
- log loss;
- reliability/calibration curve;
- Expected Calibration Error with binning sensitivity;
- posterior sensitivity to priors and calibration uncertainty;
- coverage of stated intervals where repeated datasets are available.

### 8.5 Diagnostic metrics

- Top-1/Top-3 accuracy;
- macro F1;
- per-class recall;
- abstention-performance curve;
- time-to-localization;
- comparison with severity-only FMEA ranking.

### 8.6 Experimental controls

- pre-register the final fault operators and held-out split;
- version all tools, cases, models, and datasets;
- validate monotonic-clock behavior, timestamp resolution, trigger/response
  pairing, and the uncertainty budget before collecting confirmatory evidence;
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

### 9.4 Robust timing verdict

Suppose a synthetic response must occur in:

\[
I_r=[100,120]\ \mathrm{ms}
\]

and the reviewed end-to-end measurement error is
\(\varepsilon=3\ \mathrm{ms}\).

- If \(\widehat{\Delta t}=115\ \mathrm{ms}\), then
  \(I_{\mathrm{obs}}=[112,118]\ \mathrm{ms}\subseteq I_r\): `PASS`.
- If \(\widehat{\Delta t}=118\ \mathrm{ms}\), then
  \(I_{\mathrm{obs}}=[115,121]\ \mathrm{ms}\): `INCONCLUSIVE`, because the
  measurement cannot establish either satisfaction or violation.
- If \(\widehat{\Delta t}=124\ \mathrm{ms}\), then
  \(I_{\mathrm{obs}}=[121,127]\ \mathrm{ms}\) is disjoint from \(I_r\):
  `FAIL`.

Reporting 118 ms as an exact PASS would discard known measurement uncertainty.
The example demonstrates oracle semantics only; it does not define an ARINC
615A timing value.

---

## 10. Evidence Gates and Research Decision Rules

| Gate | Requirement | If not met |
|---|---|---|
| **G0 — Scope** | Standard edition, roles, services, PICS-like applicability fixed | No base claim |
| **G1 — Traceability** | Equations (1) and (2) satisfied and reviewed | T0 incomplete |
| **G2 — Execution validity** | Preconditions, reset, environment, timestamp chain, uncertainty budget, and oracle evidence valid | Invalid instrument/environment is ERROR; unresolved boundary evidence is INCONCLUSIVE |
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
- Timing triggers, resets, cancellation, or silence semantics may be modeled incorrectly.
- An unjustified error budget may create false PASS, false FAIL, or excessive INCONCLUSIVE verdicts.
- A posterior may reflect the calibration set more than the target IUT population.

### 11.2 Internal validity

- Shared state or environment can violate run independence.
- Development mutants can leak into held-out evaluation.
- Tool defects can be misclassified as IUT failures.
- Execution order may affect results.
- Clock drift, scheduler load, network asymmetry, or cross-session timer state
  may create dependent timing observations.

### 11.3 External validity

- One ARINC 615A implementation does not establish transferability.
- A simulator may not reproduce target-network timing or hardware behavior.
- Results for TFTP-centered services may not transfer to stateless, broadcast, or real-time protocols.

### 11.4 Conclusion validity

- Small fault sets produce wide uncertainty.
- Equivalent-mutant classification may be subjective.
- Multiple comparisons and class imbalance may inflate diagnostic conclusions.
- Point estimates without uncertainty can overstate evidence.
- A common uncalibrated instrument bias can couple multiple estimated
  marginals; Fréchet bounds on those estimates do not restore validity.

Mitigations include dual review, adjudication logs, held-out faults, negative-result preservation, sensitivity analysis, replication packages, and a second protocol instance.

---

## 12. Reproducibility Package

The research release should contain, subject to proprietary-text restrictions:

```text
requirements/
  applicability.yaml
  crs.csv
  crs_adjudication.md
models/
  a615a_timed_efsm.*
  timing_obligations.yaml
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
  timing.*
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
4. Build the clock-augmented observable ARINC 615A EFSM, timing catalog, and trace model; pass RG2.
5. Derive TPs and VCs, validate robust timing and discrete oracle logic, and pass RG3.
6. Complete traceability and obligation coverage.

**Research output:** T0 methodology and artifacts.

### Phase 2 — Bounded adequacy

7. Define fault operators and FMEA/FMECA mapping.
8. Build development and held-out fault sets.
9. Pass RG4 execution-readiness inspection.
10. Execute mutation and held-out evaluation.
11. Execute the timing-boundary, clock-reset, uncertainty, and held-out timing-fault study.
12. Reproduce the evidence package and pass RG5.
13. Compare B0, B1, B2-U, B2-T, and B3 baselines.

**Research output:** T1/T2 evidence and empirical evaluation.

### Phase 3 — Calibrated evidence and diagnosis

14. Calibrate false-fail and missed-detection behavior.
15. Evaluate Bayes factors, posteriors, and sensitivity.
16. Train and evaluate the baseline diagnostic model.
17. Consider HMM/Bayesian-network extensions only if supported by physical state meaning and sufficient data.
18. Pass RG6 before releasing any quantitative conformance claim.

**Research output:** optional T3 evidence.

### Phase 4 — Transferability

19. Apply the method to a second protocol selected for contrasting characteristics.
20. Identify invariant and protocol-specific steps.
21. Revise the claimed contribution based on cross-instance evidence.

**Research output:** evidence for or against protocol independence.

---

## 14. Conclusion

This report establishes an integrated Test-and-Analysis methodology for constructing and evaluating a scoped ARINC 615A conformance-assurance argument.

The **Test path** operationalizes applicable requirements as controlled stimuli, observable behavior, executable oracles, verdicts, and reproducible timestamped traces. The **Analysis path** determines which discrete and timed obligations were covered, whether timing verdicts remain valid under measurement uncertainty, how well the VCS detects declared fault classes, what uncertainty the observations support, and which verification action should follow. Neither path is sufficient alone: Analysis without Test lacks controlled empirical observations, while Test without Analysis cannot justify the scope or strength of its conclusions.

Independent Review and Inspection gates turn this research logic into an engineering control system. They prevent unresolved ambiguity, incomplete traceability, weak oracle logic, uncontrolled execution configurations, irreproducible evidence, and overstated claims from propagating downstream.

The central academic contribution is a precise separation of semantics—logical sequence, deterministic real-time conformance, run-order dependence, latent temporal dynamics, coverage, valid execution, bounded detection adequacy, operational repeatability, calibrated belief, and diagnosis—together with propositions and experiments that can evaluate their relationships. The central engineering contribution is a reusable artifact chain and decision process that directs effort toward observable risk, prevents timing instrumentation from creating false precision, preserves evidence, exposes rework early, and supports auditable release decisions.

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
| \(G_T\) | Clock-augmented observable EFSM specification |
| \(C\) | Finite set of model clocks |
| \(\sigma_T\) | Timestamped observable trace |
| \(\bot_r@t_H\) | Active timing obligation with no response observed through horizon \(t_H\) |
| \(I_r=[L_r,U_r]\) | Requirement-defined admissible timing interval |
| \(I_{\mathrm{obs}}\) | Observation interval after applying the measurement-error bound |
| \(D_r\) | Reviewed physical domain of the measured delay; normally \([0,\infty)\) only when justified |
| \(\varepsilon_{ij}\) | Justified timing-measurement error bound |
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
- [ ] Every timing obligation defines trigger, response, cancellation/silence,
      bounds, units, clock resets, and source references
- [ ] Monotonic time source, timestamp locations, resolution, and uncertainty
      budget are reviewed
- [ ] Robust timing oracle and early/nominal/boundary/late/no-response
      partitions are covered where applicable
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
- [ ] Timing margins, clock metadata, order effects, clustering, and drift
      diagnostics are retained
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

[21] Alur, R., & Dill, D. L. (1994). A Theory of Timed Automata.
*Theoretical Computer Science*, 126(2), 183–235.
https://doi.org/10.1016/0304-3975(94)90010-8

[22] Joint Committee for Guides in Metrology (2008). *Evaluation of
Measurement Data — Guide to the Expression of Uncertainty in Measurement*,
JCGM 100:2008. https://doi.org/10.59161/JCGM100-2008E

[23] Joint Committee for Guides in Metrology (2012). *The Role of Measurement
Uncertainty in Conformity Assessment*, JCGM 106:2012.
https://doi.org/10.59161/JCGM106-2012

---

*AI-assisted research disclosure: AI tools assisted with drafting and consistency checking. Mathematical claims, standard interpretations, references, and experimental conclusions require accountable human review. The report does not state that a reference has been verified unless its bibliographic metadata and the cited proposition have both been checked.*

## 15. v4.3 Certification-Oriented Evidence Architecture

Under candidate baseline `RB-2026-001-v4.3`, this report's mathematics and
timed-conformance semantics are inherited unchanged; equations 1–14 and timed
equations T1–T5 are not modified. The architecture is extended with a
certification-oriented evidence model: requirement → Verification Objective →
verification definition → controlled execution → Execution Evidence Manifest →
Objective Satisfaction → Compliance Evidence Index.

The T0–T3 ladder of section 2.3 is superseded by two orthogonal axes:
certification-oriented assurance states A0–A4 and research-evidence maturity
states R0–R5. Execution verdict, objective status, and compliance status are
distinct; no `PASS` automatically satisfies an objective or supports a claim.
Mutation adequacy, calibration, diagnosis, and transferability are
research-only and do not grant certification status. These states are
project-defined and are not authority assurance levels. See
[`CERTIFICATION_EVIDENCE_BASIS.md`](CERTIFICATION_EVIDENCE_BASIS.md) and the
compliance/objective contracts under `docs/control/contracts/`.

---

# 中文版

> 本部分是前述英文规范正文的同步中文译本；若解释存在差异，以英文部分为准。

# 面向 ARINC 615A 符合性验证的测试—分析方法论
## 基于需求的测试、有限证据分析与独立评审门

**研究报告 RR-2026-001**

| 字段 | 内容 |
|---|---|
| **版本** | 4.2 研究基线 |
| **日期** | 2026-07-30 |
| **状态** | 已经 PR #6 在 GR-PR6-RB-2026-001-v4.2 下生效并冻结；经验性主张受 §10 证据门约束 |
| **主要实例** | 基于 TFTP 的 ARINC 615A DOWNLOAD/UPLOAD 服务 |
| **密级** | 内部——学术研究 |
| **规范语言** | 同一文件中的英文部分为权威版本；本部分为同步中文译本 |

---

## 摘要

协议符合性验证必须把规范性需求转化为可信的工程决策。因此，它既需要通过执行受测实现（IUT）获得动态证据，也需要严谨分析覆盖、检测能力、不确定性和故障原因。本报告提出一种面向 ARINC 615A 符合性验证的一体化测试—分析（Test-and-Analysis）方法论。

**测试路径**导出适用符合性需求集（CRS）、测试目的（TP）和可执行验证用例（VC），随后针对 IUT 执行这些用例，产生判定、带时间戳的迹和测量结果。**分析路径**评价追踪性、模型覆盖、确定性时序符合性、有限故障域充分性、重复运行行为、校准证据和故障诊断。测试与分析相互补充：测试产生受控观测，分析说明这些观测能够支持什么结论，以及下一步应将验证资源投入何处。

独立的**评审与检查门**控制需求、协议模型、验证用例、oracle、执行就绪性、证据包和对外主张的质量。这些静态活动支持两条主要路径，但不被包装成独立研究创新。演示可用于利益相关者验收，但不是详细协议符合性验证的主要方法。

该框架同时追求学术价值——语义清晰、主张边界明确、假设可经验评价——和工程价值——产物可评审、流程可自动化、发布有门禁、结果可诊断、决策可复现。

**关键词：** 协议符合性验证；测试—分析；基于需求的测试；工程保证；追踪性；带时钟 EFSM；稳健时序 oracle；测量不确定性；ARINC 615A；有限故障域；变异测试；校准证据；贝叶斯推断；评审门；检查

---

## 1. 研究目标与价值

### 1.1 问题

ARINC 615A 验证通常围绕项目 ICD 组织。该做法对系统集成是必要的，但不能自动形成与规范性标准直接关联、可在项目间复用的协议级符合性论证。

本研究的问题是：

> 如何导出、执行并评价一套可复用的 ARINC 615A 符合性验证用例集，使所有主张均可追踪至适用规范性需求，受到显式观测模型和故障模型约束，并由可复现证据支持？

### 1.2 研究问题

| ID | 研究问题 | 所需证据 |
|---|---|---|
| **RQ1——导出** | 如何将适用规范性需求转化为可审计测试目的和可执行验证用例？ | CRS、追踪关系、评审一致性、用例模式 |
| **RQ2——覆盖** | 声明范围内必须覆盖哪些需求、模型、数据、时序、负向和序列义务？ | 覆盖义务与覆盖矩阵 |
| **RQ3——有限充分性** | VCS 在声明的有限故障域中检测不符合性的能力如何？ | 有效变异体目录、留出故障、变异结果 |
| **RQ4——证据解释** | 在不混淆运行重复性和符合性概率的前提下，重复 PASS/FAIL 能支持什么结论？ | 观测模型、区间、校准数据 |
| **RQ5——诊断** | 失败特征能否以有用且可复现的精度定位故障类别？ | 故障注入数据集、混淆矩阵、Top-k 指标 |
| **RQ6——可迁移性** | 当方法应用到第二种协议时，哪些步骤保持有效？ | 第二协议实例；仅凭 615A 无法回答 |

### 1.3 一体化方法论命题

本方法论由两条主要且相互强化的验证路径构成：

1. **测试（Test）：** 在受控前置条件、刺激、时序和 oracle 下与 IUT 交互，产生判定、迹、测量结果和可复现执行记录。
2. **分析（Analysis）：** 检查需求、模型、追踪、覆盖、变异体、重复观测、不确定性和失败特征，产生充分性评价、证据边界、诊断排序和新增测试建议。

二者形成闭环工程过程：

```text
需求与协议模型
      |
      v
测试设计 -> 测试执行 -> 观测与判定
   ^                       |
   |                       v
   +---- 分析 <- 覆盖、充分性、不确定性、诊断
             |
             v
       工程决策 / 下一项验证行动
```

评审与检查门控制进入和离开该闭环的产物。

### 1.4 学术价值与工程价值

| 价值维度 | 形成的价值 |
|---|---|
| **学术价值** | 显式语义；形式化追踪关系；有边界的充分性主张；经过校准的推断；可经验评价的假设；将可迁移性作为研究问题 |
| **工程价值** | 标准到用例的追踪；可复用基础 VCS；受控扩展 VCS；评审门；可执行证据模式；留出故障评价；诊断输出；可审计发布决策 |

学术贡献使推理可辩护；工程贡献使这种推理可以落地、评审和维护。

### 1.5 本报告主张的贡献

1. **可追踪导出框架。** 支持适用性、复合需求和一对多/多对多映射的需求—测试模型。
2. **互补测试—分析工作流。** 动态执行产生证据，分析评价充分性、不确定性并决定后续行动。
3. **确定性时序符合性语义。** 通过带时间戳的迹、带时钟 EFSM、显式测量误差预算和稳健判定规则，避免把时序测量当成精确值。
4. **范围受限保证论证。** 对覆盖、有效执行和有限故障检测证据作形式化区分。
5. **有限故障域充分性方法。** 包含等价/无效变异体处理、时序故障和留出故障评价的可复现变异流程。
6. **校准证据语义。** 区分运行 PASS 概率、似然证据和符合性后验信念。
7. **独立质量门。** 评审与检查覆盖范围、需求、模型、用例、oracle、执行就绪性、证据和主张发布。
8. **评价协议。** 包含基线、指标、数据泄漏控制和决策门槛的可经验检验设计。

### 1.6 科学定位与创新边界

本方法是一种综合，不声称发明了基于需求或基于模型的符合性测试。

- ISO/IEC 9646 提供符合性测试框架和抽象测试套语境 [1][2]。
- Tretmans 提供输入/输出符合关系及测试生成的形式化基础 [4]。
- Chow 和 Fujiwara 等人在显式状态机假设下给出有限状态机检查实验基础 [5][6]。
- ETSI TR 102 840 提供在标准化环境中应用基于系统模型测试生成的非规范性建议，特别讨论追踪性和从系统模型生成测试 [3]。
- Petrenko 等人给出使用约束求解的有限故障域和变异体杀死方法 [7]。
- Jia 和 Harman 综述变异测试证据及其已知限制 [8]。
- Yang 等人的综述展示了基于需求的测试生成范围，并说明必须区分输入表示、生成产物和评价方法 [9]。
- Li 等人展示了对非确定性作显式处理的网络应用严格模型化测试 [10]。
- Alur 和 Dill 给出了时序自动机的时钟、守卫和复位基础 [21]。本报告采用带时钟 EFSM 的工程适配，不宣称与完整时序自动机形式体系等价。
- JCGM 100 给出表达测量不确定性的一般规则 [22]，JCGM 106 讨论测量不确定性在符合性评价中的作用 [23]。§3.6 的稳健区间判定是本方法论采用的保守决策规则，仍须针对具体时序仪器验证。
- NASA 系统工程指南通常将需求验证方法分为测试、分析、检查和演示 [19]。本报告将评审视为与软件工作产品评审实践一致的静态治理活动，而不强行纳入该四方法分类 [20]。

预期创新是将这些思想在 ARINC 615A 场景中进行**可审计集成和经验评价**：互补测试—分析闭环、适用性受控的需求提取、义务敏感的追踪、考虑测量不确定性的时序符合性、显式有限故障域边界、留出故障评价、校准证据门槛，以及独立产物评审。在完成 §§8–10 的产物和实验前，该创新仍是研究假设，不是已被证实的结果。

DO-178C 仅作为相邻保证背景 [16]，不是本方法或测试/分析/检查分类的形式化来源。FMEA/FMECA 采用 IEC 60812 术语 [14]。未来若使用 HMM，必须建立独立验证的时序诊断模型，不能从协议图直接推导 [15]。

---

## 范围、边界与非主张

### ARINC 615A 实例范围

**包含**

- DLS 和 THW 角色；
- DOWNLOAD 和 UPLOAD 会话行为；
- 上述服务涉及的 TFTP/UDP 行为；
- 请求协商、DATA/ACK 传输、重试、超时、重复、序列、错误、末块及已声明回卷行为；
- 适用 CRS 中显式定义的协议字段和时序义务。

**不包含在基础符合性主张中**

- FIND 和 INFORMATION 服务；
- 无限定 ARINC 665 文件内容符合性；
- 无限定 ARINC 664 网络符合性；
- 认证信用；
- 未在 CRS 中表达的性能、安全和鲁棒性属性；
- 声明有限故障域之外的故障。

ARINC 665 和 ARINC 664 可以作为环境假设或测试数据约束出现。除非纳入它们各自的适用需求和验证证据，否则不为其分配符合性分数。

### 明确不作出的主张

本报告不主张：

- 有限测试集能够证明所有可能行为的符合性；
- 结构覆盖等价于故障检测能力；
- 变异分数自动泛化到全部真实故障；
- 重复 PASS 频率等于固定 IUT 符合的概率；
- 协议层在统计意义上相互独立；
- 未校准标量是协议级概率；
- 单一 ARINC 615A 实例能够证明协议无关性；
- 本方法提供认证批准或替代认证机构评审。

---

## 2. 概念架构

### 2.1 验证活动及其角色

| 活动 | 在本方法论中的主要角色 | 典型输入 | 典型输出 |
|---|---|---|---|
| **测试** | 根据需求导出的 oracle 动态执行 IUT | IUT、VC、环境、协议对端 | 判定、报文迹、测量值、执行记录 |
| **分析** | 判断覆盖、充分性、不确定性、依赖关系和可能故障原因 | CRS、模型、测试证据、变异体、校准数据 | 覆盖矩阵、充分性结果、区间/后验、诊断排序 |
| **检查** | 使用规定检查表核对产物的客观属性 | CRS 条目、追踪矩阵、模式、日志、发布包 | 缺陷、完整性发现、签署的检查记录 |
| **评审** | 独立评价技术判断并批准是否通过门禁 | 解释、EFSM、VC、oracle 逻辑、分析和主张 | 评审发现、理由、批准/返工决定 |
| **演示** | 在详细测量不是主要目的时展示利益相关者可见的运行能力 | 集成场景或原型 | 已观测能力和验收证据 |

测试与分析是两条主要技术路径；检查与评审构成横向静态保证层。演示是可选活动，不能替代需要精确报文、时序或状态观测的协议义务测试证据。

### 2.2 分离的分析对象

本基线严格分离此前被混合使用的四种对象。

| 对象 | 用途 | 数学形式 | 是否可以包含概率？ |
|---|---|---|---|
| **协议模型** | 描述合法可观测行为，包括规范性实时时间约束 | 带时钟 EFSM/时序 IOLTS \(G_T\) | 非必需 |
| **追踪模型** | 关联需求、目的、用例和模型目标 | 关系 \(\rho\) | 否 |
| **证据记录** | 保存执行条件、观测和判定 | 数据集 \(\mathcal{E}\) | 仅包含观测 |
| **推断/诊断模型** | 解释经过校准的证据 | 似然/贝叶斯模型 | 可以，但必须校准 |

协议模型不是证据模型。协议图上的边表示可能或必须发生的行为；不能仅仅因为某条边附有置信证据，就将其称为“转移概率”。

### 2.3 保证层级

> **v4.3 超越说明。** 在候选基线 `RB-2026-001-v4.3`
> （[`CR-2026-004`](../../../docs/control/changes/CR-2026-004.md)）下，下方的
> 单一 T0–T3 阶梯被两个正交轴超越：面向认证保证状态 **A0–A4** 与研究证据成熟度
> 状态 **R0–R5**。单个执行 `PASS` 不再自动满足目标或支持主张；目标状态与合规状态
> 为受评审结论。突变、校准、诊断和迁移性转为仅研究扩展，不授予认证状态。下方 T0–T3
> 描述作为历史措辞保留，仅对 `RB-2026-001-v4.2` 基线有效；v4.3 中不静默重标。
> 数学与时序符合性语义不变。

| 层级 | 主张 | 最低支持产物 |
|---|---|---|
| **T0——追踪性** | 每条适用需求均关联至少一个可执行用例 | CRS、TP/VC 关系 |
| **T1——观测符合性** | IUT 在已记录条件下对已执行用例产生了可接受观测 | T0 + 有效执行记录 |
| **T2——有限检测充分性** | VCS 能区分规范和声明评价故障集中每个非等价成员 | T1 + 变异/故障结果 |
| **T3——校准证据** | 证据依据经过验证的观测模型改变对符合性命题的信念 | T2 + 校准和敏感性分析 |

高层级不能抵消低层级的缺失。任何 T3 数字都不能弥补追踪性缺失或无效执行。在 v4.3 下，T0 对应 A1 可追踪定义，T1 对应 A2/A3 有效证据与受评审目标满足，T2/T3 对应 R2–R5 研究成熟度，而非更高面向认证保证。

---

## 3. 形式化核心

### 3.1 标准、能力声明与适用需求

设：

- \(S\) 为固定版本的协议标准；
- \(P\) 为实现适用性声明，包括角色、服务、选项和明确排除项；
- \(O\) 为观测边界，即验证系统允许使用的报文、时序、状态、日志和文件级现象；
- \(R(S)\) 为从标准提取的规范性需求项集合；
- \(R_{\mathrm{app}}(S,P)\subseteq R(S)\) 为对 \(P\) 适用的需求。

每个需求项 \(r\in R(S)\) 包含：

\[
r=(id,\ source,\ textHash,\ modality,\ applicability,\ category,\ interpretation)
\]

`source` 包含标准版本、条款、表格/图编号和页码。`textHash` 在不公开复制专有标准文本的情况下支持受控追踪。

需求根据其验证义务分类，而不是服从一个全局固定覆盖层级：

\[
\mathrm{Obl}(r)\subseteq
\{\mathrm{functional},\mathrm{state},\mathrm{transition},\mathrm{data},
\mathrm{timing},\mathrm{negative},\mathrm{sequence}\}.
\]

### 3.2 测试目的与验证用例

令 \(T\) 为测试目的集合，\(V\) 为验证用例集合。

追踪性表示为：

\[
\rho_{RT}\subseteq R_{\mathrm{app}}\times T,
\qquad
\rho_{TV}\subseteq T\times V.
\]

这里刻意不使用一对一函数。一个需求可能产生多个目的，一个目的可能需要多个用例，一个用例也可能支持多个需求。

验证用例定义为：

\[
v=(id,\ role,\ pre,\ stimulus,\ oracle,\ refs,\ targets,\ reset,\ timingSchema,\ evidenceSchema).
\]

其中：

- `pre` 定义可执行前置条件；
- `stimulus` 定义受控动作和输入；
- `oracle` 将观测映射为判定；
- `refs\subseteq R_{\mathrm{app}}` 保存需求引用；
- `targets` 保存 EFSM 状态、转移、数据分区、时序界限和故障类别；
- `reset` 定义隔离和状态恢复；
- `timingSchema` 定义时间源、时间戳位置、时钟复位、触发/响应配对、允许区间和测量误差预算；
- `evidenceSchema` 定义强制日志和测量。

### 3.3 判定语义

对 IUT \(I\)、验证用例 \(v\) 和受控环境 \(e\)：

\[
\mathrm{Verdict}(I,v,e)\in
\{\mathrm{PASS},\mathrm{FAIL},\mathrm{INCONCLUSIVE},\mathrm{ERROR}\}.
\]

- **PASS：** 前置条件满足，观测符合 oracle。
- **FAIL：** 前置条件满足，观测违反 oracle。
- **INCONCLUSIVE：** 无法确认适用性或前置条件，或者观测不足。
- **ERROR：** 验证工具或环境使本次执行失效。

不得将 `INCONCLUSIVE` 和 `ERROR` 静默转化为 PASS，也不得从报告中静默删除。

### 3.4 需求追踪覆盖

当且仅当下式成立时，VCS 对 \(R_{\mathrm{app}}\) 具有追踪完备性：

\[
\forall r\in R_{\mathrm{app}},
\ \exists t\in T,\exists v\in V:
(r,t)\in\rho_{RT}\land(t,v)\in\rho_{TV}.
\tag{1}
\]

义务覆盖还要求：

\[
\forall r\in R_{\mathrm{app}},\
\forall o\in\mathrm{Obl}(r),\
\exists v\in V:\mathrm{Covers}(v,r,o).
\tag{2}
\]

式（1）检查追踪关系是否存在，式（2）检查每种必需义务是否有充分用例。两者均不能单独证明 oracle 正确性或故障检测能力。

### 3.5 协议行为模型

可观测协议模型定义为扩展有限状态机：

\[
G=(Q,q_0,X,\Sigma_I,\Sigma_O,\Delta)
\]

其中：

- \(Q\) 为控制状态集合；
- \(q_0\) 为初始状态；
- \(X\) 为数据变量、计数器、协商选项、重试状态和相关历史组成的向量；
- \(\Sigma_I,\Sigma_O\) 为输入、输出字母表；
- \(\Delta\) 为带守卫的转移关系。

转移定义为：

\[
\tau=(q,\ input,\ guard(X),\ action(X),\ output,\ q').
\]

本基线不假设马尔科夫性。未来若引入概率时序模型，必须独立证明其状态表达是充分的。

### 3.6 确定性时序符合性模型

必须区分以下四种概念：

1. **逻辑序列**：协议事件的先后顺序；
2. **规范性实时时间**：截止时间、最小延迟、重试间隔和超时行为；
3. **运行顺序依赖**：多次执行之间的漂移、聚类、预热效应或状态泄漏；
4. **隐含时序动力学**：故障或退化状态确实随物理时间变化。

前两者属于核心符合性模型，第三者属于实验分析，第四者仅是可选诊断扩展，不能从一条 EFSM 迹自动推出。

定义可观测时戳迹：

\[
\sigma_T=\bigl((a_0,t_0),(a_1,t_1),\ldots,(a_m,t_m)\bigr),
\qquad t_0\le t_1\le\cdots\le t_m,
\tag{T1}
\]

其中时间戳使用已声明的单调时间基准。对触发事件 \(a_i\) 及需求定义的响应事件 \(a_j\)，令
\(\Delta t_{ij}=t_j-t_i\)。每条需求声明允许集合 \(I_r\)，包括每个有限端点是否包含。有界响应义务为：

\[
a_i@t_i\Longrightarrow
\exists j>i:
a_j@t_j\land \Delta t_{ij}\in I_r,
\tag{T2}
\]

时序目录必须定义事件谓词 \(\mathrm{Trig}_r\)、\(\mathrm{Resp}_r\)、
\(\mathrm{Cancel}_r\) 和 \(\mathrm{Supersede}_r\)，以及关联键和显式配对策略（例如唯一键、FIFO 或最近触发）。一次触发创建一个独立有效义务实例。响应只能解除由声明的关联键和配对策略选中的有效实例；配对歧义或无效属于 `ERROR`，不是 IUT `FAIL`。匹配的取消事件在其迹索引处把所选实例终止为“已取消”，之后的静默不得产生无响应 `FAIL`。除非需求明确允许并发实例，替代触发会把旧实例终止为“已替代”，并以新的时钟原点创建新实例。取消和替代是义务处置而不是时序判定，且必须保留在迹中。相同时间戳按迹索引排序；事件只有在索引晚于触发时才能影响该义务。没有最小延迟的需求取 \(L_r=0\)。持续静默直至截止时间本身是时序观测，不是缺失数据。

对观测终点 \(t_H\)，用特殊迹事件 \(\bot_r@t_H\) 编码义务仍有效但未观测到响应：

\[
\bot_r@t_H
\ \Longleftrightarrow\
\mathrm{active}_r(i,t_H)
\land (t_H-t_i>U_r)
\land
\nexists j>i:\bigl(a_j\in\mathrm{Resp}_r\bigr)\land(t_i<t_j\le t_H).
\]

其中 \(\mathrm{active}_r(i,t_H)\) 表示索引 \(i\) 创建的实例截至 \(t_H\) 尚未按上述匹配规则被响应解除、取消或替代。式中的严格不等式定义闭合上界情形，此时恰在 \(U_r\) 的响应仍合格；开上界的对应到期条件为 \(t_H-t_i\ge U_r\)。因此 \(\bot_r@t_H\) 是“已经到期、仍有效且没有匹配响应”的正式观测，不是缺少日志记录的同义词。

带时钟的可观测 EFSM 定义为：

\[
G_T=(Q,q_0,X,C,\Sigma_I,\Sigma_O,\Delta_T,\mathrm{Inv}),
\tag{T3}
\]

其中 \(C\) 是有限时钟集合，\(\mathrm{Inv}\) 是状态不变量；时序转移包含数据守卫、时钟守卫和需要复位的时钟集合：

\[
\tau_T=(q,input,g_X(X),g_C(C),action(X),reset_C,output,q').
\]

\(G_T\) 是否确定由声明的协议语义决定；它不是随机过程。

时序观测不是精确值。令：

\[
\widehat{\Delta t}_{ij}=\Delta t_{ij}+e_{ij},
\qquad |e_{ij}|\le\varepsilon_{ij},
\qquad
I_{\mathrm{obs}}=
[\widehat{\Delta t}_{ij}-\varepsilon_{ij},
 \widehat{\Delta t}_{ij}+\varepsilon_{ij}]
\cap D_r,
\tag{T4}
\]

其中 \(\varepsilon_{ij}\) 来自经评审、版本化且适用于声明环境和测量路径的误差预算。预算逐项列出时钟分辨率/量化、时钟精度与漂移、时间戳插入位置、调度延迟、网络捕获延迟、软件层处理延迟、设备间同步误差，以及公共路径或仪器偏差；每个分量记录来源、界限、符号模型和相关类别。只有同一误差以相同符号进入两个时间戳，且经评审的测量设计证明其代数相消时，才能删除公共项。独立性本身不能证明最坏情况符合性误差界可以采用均方根合成；独立分量和公共偏差必须区分，任何概率合成也必须与 \(\varepsilon_{ij}\) 分开报告。只有当触发/响应关系和时间戳设计经评审确认延迟物理上非负时，才取
\(D_r=[0,\infty)\)；否则取 \(D_r=\mathbb{R}\)。若交集为空，则观测与声明的测量模型矛盾，本次执行应记为 `ERROR`，不得通过截断强行产生判定。

对声明的允许区间 \(I_r\)（闭、开或半开均可），稳健时序 oracle 为：

\[
\mathrm{TimingVerdict}_r=
\begin{cases}
\mathrm{PASS},& I_{\mathrm{obs}}\subseteq I_r,\\
\mathrm{FAIL},& I_{\mathrm{obs}}\cap I_r=\varnothing,\\
\mathrm{INCONCLUSIVE},&\text{其他情况}.
\end{cases}
\tag{T5}
\]

如果时间源、时间戳链、触发/响应配对或声明的误差界无效，则本次执行为 `ERROR`，而不是 `INCONCLUSIVE`。该集合包含规则在边界附近刻意保持保守，禁止把测量分辨率包装成虚假精度。闭合上界下，对
\(\bot_r@t_H\)，只有在义务保持有效且最早可能经过时间满足
\(\widehat{\Delta t}_{iH}-\varepsilon_{iH}>U_r\) 时，才能稳健地判定“无响应
FAIL”；开上界的对应条件为
\(\widehat{\Delta t}_{iH}-\varepsilon_{iH}\ge U_r\)。否则按前述规则判为 `INCONCLUSIVE` 或 `ERROR`。特别是，名义超时量小于测量误差余量时不得判 `FAIL`。

每条适用时序需求都必须追踪到：

- 触发、响应、取消、替代、关联/配对、并发和静默语义；
- \(L_r,U_r\)、单位、时钟启动/复位事件和来源引用；
- 观测点和单调时间基准；
- 经评审的误差预算 ID/版本、适用环境、分量来源、相关性/公共偏差理由及最终 \(\varepsilon_{ij}\)；
- 适用的过早、标称、边界、过晚和无响应分区。

### 3.7 有限故障域

故障域定义为：

\[
\mathcal{F}=(G,\preceq,\mathcal{M})
\]

其中 \(G\) 为规范模型，\(\preceq\) 为声明的符合关系，\(\mathcal{M}\) 为有限候选不符合实现或变异体集合。

按下列集合对 \(\mathcal{M}\) 分类：

- \(\mathcal{M}_{\mathrm{invalid}}\)：结构错误或不可执行变异体；
- \(\mathcal{M}_{\mathrm{exec}}=\mathcal{M}\setminus\mathcal{M}_{\mathrm{invalid}}\)：可构建且可执行的变异体；
- \(\mathcal{M}_{\mathrm{equiv}}\subseteq\mathcal{M}_{\mathrm{exec}}\)：在声明观测范围内与 \(G\) 行为等价的变异体；
- \(\mathcal{M}_{\mathrm{eval}}=\mathcal{M}_{\mathrm{exec}}\setminus\mathcal{M}_{\mathrm{equiv}}\)：用于评价的有效非等价变异体。

最终分类互不相交：
\(\mathcal{M}=\mathcal{M}_{\mathrm{invalid}}\mathbin{\dot\cup}
\mathcal{M}_{\mathrm{equiv}}\mathbin{\dot\cup}\mathcal{M}_{\mathrm{eval}}\)。

用例 \(v\) 杀死变异体 \(m\) 当且仅当：

\[
\mathrm{Kill}(v,m)=1
\iff
\mathrm{Verdict}(G,v,e)=\mathrm{PASS}
\land
\mathrm{Verdict}(m,v,e)=\mathrm{FAIL},
\tag{3}
\]

并且二者使用等价受控条件和有效 oracle。

这里的 \(\mathrm{Verdict}(G,v,e)\) 表示由可执行参考模型或从 \(G\) 独立验证导出的 oracle 所产生的参考判定；它不假设抽象 EFSM 本身可以直接执行。

VCS 相对于 \(\mathcal{M}_{\mathrm{eval}}\) 完备，当且仅当：

\[
\forall m\in \mathcal{M}_{\mathrm{eval}},
\ \exists v\in V:\mathrm{Kill}(v,m)=1.
\tag{4}
\]

式（4）是有限主张，不对 \(\mathcal{M}_{\mathrm{eval}}\) 之外的故障作出结论。

### 3.8 加权变异分数

若所有评价变异体具有相同权重且
\(|\mathcal{M}_{\mathrm{eval}}|>0\)：

\[
\mathrm{MS}=
\frac{\sum_{m\in \mathcal{M}_{\mathrm{eval}}}
\mathbf{1}[\exists v\in V:\mathrm{Kill}(v,m)]}
{|\mathcal{M}_{\mathrm{eval}}|}.
\tag{5}
\]

若专家论证的非负权重 \(w_m\) 表示不同失效模式的重要程度，且
\(\sum_m w_m>0\)：

\[
\mathrm{WMS}=
\frac{\sum_{m\in \mathcal{M}_{\mathrm{eval}}}
w_m\mathbf{1}[\exists v\in V:\mathrm{Kill}(v,m)]}
{\sum_{m\in \mathcal{M}_{\mathrm{eval}}}w_m}.
\tag{6}
\]

必须公开权重、依据和敏感性分析。除非变异体能够合理代表目标失效模式总体，否则不得把变异分数称为 FMEDA 诊断覆盖。

---

## 4. 方法

### 4.1 阶段 A——冻结范围和适用性

1. 固定 ARINC 615A 版本和已批准解释。
2. 记录 DLS/THW 角色及包含服务。
3. 记录支持选项、边界和环境假设。
4. 生成适用性声明 \(P\)。
5. 为需求提取安排独立评审者。

**出口产物：** 签署的范围和适用性记录。

### 4.2 阶段 B——提取并裁决 CRS

两名评审者独立识别规范性陈述，并将复合条款拆分为原子需求项，然后裁决：

- 遗漏需求；
- 适用性判断差异；
- 模态歧义；
- 复合义务；
- 表格、时序值和错误行为引用。

同时报告原始一致性与裁决后结果。分类决策可以报告 Cohen's \(\kappa\)，但由于其受类别分布影响，百分比一致率和分歧表仍为必需产物。

**出口产物：** 版本化 CRS 和裁决日志。

### 4.3 阶段 C——建立带时钟的可观测 EFSM

1. 定义外部可观测状态和变量。
2. 将每条适用时序义务提取为触发、响应、取消、静默、上下界、单位和复位语义。
3. 编码数据守卫、时钟守卫、状态不变量、时钟复位、选项、重试计数器、超时、块号行为和终止状态。
4. 将每个状态、转移、时序约束和复位关联至需求。
5. 对照 CRS 评审模型及其可观测性。
6. 所有协议特定主张（包括回卷和时序规则）在获得精确标准引用前均视为未解决。

**出口产物：** 带时钟 EFSM、时序义务目录和需求—模型关系。

### 4.4 阶段 D——导出测试目的

针对每条适用需求及其义务类型，从以下角度导出目的：

- 正常行为；
- 非法输入或禁止输出；
- 等价类和边界值；
- 状态/转移可达性；
- 超时和重试阈值；
- 重复、乱序和序列故障；
- 规范要求的端到端会话序列。
- 对每条有界时序义务，在语义适用时覆盖过早、标称、上下边界、过晚和无响应分区。

测试目的必须经过人工评审。自动化工具可以提出候选项，但不能静默决定规范含义。

**出口产物：** TP 目录和 \(\rho_{RT}\)。

### 4.5 阶段 E——定义验证用例

每个用例包含：

- 稳定标识和版本；
- 角色分配；
- IUT 与对端初始状态；
- 精确测试数据和分区；
- 步骤与受控时序；
- 时间源、时间戳位置、触发/响应配对、时钟复位、允许区间和测量误差预算；
- 期望可观测迹；
- 判定 oracle；
- 需求和模型目标；
- 重置/隔离程序；
- 证据字段；
- 工具和环境版本。

**出口产物：** 可执行或可直接实现的 VCS 及 \(\rho_{TV}\)。

### 4.6 阶段 F——验证覆盖

分别报告：

- 需求追踪覆盖；
- 各类别义务覆盖；
- 状态覆盖；
- 转移覆盖；
- 守卫/数据分区覆盖；
- 时序边界覆盖；
- 时序分区和时钟复位覆盖；
- 负向/错误覆盖；
- 必需序列覆盖。

不得用单一综合百分比掩盖某一必需类别的缺失。

### 4.7 阶段 G——构造故障域

故障算子来源包括：

- 需求误解；
- EFSM 守卫、动作和目标改变；
- 字段编码故障；
- 超时/重试阈值偏移、缺失或多余时钟复位、错误计时器启动事件、非单调时间源和跨会话计时器泄漏；
- 数据完整性故障；
- 已知实现缺陷模式；
- 专家 FMEA/FMECA 分析。

用于改进 VCS 的变异体构成 \(\mathcal{M}_{\mathrm{dev}}\)。最终评价前预先确定一个不相交集合 \(\mathcal{M}_{\mathrm{holdout}}\)：

\[
\mathcal{M}_{\mathrm{dev}}\cap \mathcal{M}_{\mathrm{holdout}}=\varnothing.
\]

在可能情况下，将真实历史故障纳入 \(\mathcal{M}_{\mathrm{holdout}}\)。必须报告开发故障和留出故障之间可能存在的泄漏。

### 4.8 阶段 H——执行并保存证据

每次执行至少保存：

- IUT 构建版本/hash；
- 仿真器和工具版本；
- 配置；
- 随机种子和输入文件 hash；
- 单调时钟时间戳；
- 时间戳源身份、分辨率、误差预算和时钟/复位事件；
- 报文迹；
- 状态/转移迹；
- oracle 输入及决策；
- 环境健康状态；
- 最终判定。

### 4.9 阶段 I——评价与修订

评价：

- T0/T1/T2 保证层级；
- 留出故障检测率；
- VCS 规模和执行成本；
- 稳健时序判定、时序边界/分区覆盖和观测测量裕量分布；
- 存活变异体；
- 无效/等价变异体比例；
- 评审者一致性；
- 启用诊断时的诊断精度；
- 启用概率推断时的校准质量。

任何存活留出故障都必须触发对需求、模型、目的、oracle 或实现缺口的分析。可以据此修订 VCS，但原始留出结果必须保留。

### 4.10 评审与检查门

| 门 | 主要静态活动 | 入口产物 | 出口准则 |
|---|---|---|---|
| **RG0——范围** | 评审 | 标准版本、服务、角色、适用性草案 | 范围和主张边界获批 |
| **RG1——CRS** | 检查 + 评审 | 独立提取的需求 | 来源引用、原子性、适用性和裁决完成 |
| **RG2——模型与追踪** | 检查 + 技术评审 | 带时钟 EFSM、时序目录、需求—模型映射、\(\rho_{RT}\) | 离散/时序模型一致性、可观测性和追踪完整性获批 |
| **RG3——VC 与 oracle 就绪** | 检查 + 同行评审 | TP/VC 目录、稳健 oracle 逻辑、重置和不确定性计划 | 用例可执行；触发/响应、时序界限、不确定性和判定语义可独立评审 |
| **RG4——执行就绪** | 检查 | IUT 配置、工具、时钟、时间戳链、环境、数据、日志方案 | 配置和时序仪器受控；误差预算和试运行获批 |
| **RG5——证据完整性** | 检查 + 分析评审 | 带时戳原始迹、判定、变异结果、排除项、派生时序结果 | 证据来源、时钟元数据、排除理由和计算可复现 |
| **RG6——主张发布** | 独立评审 | 保证论证、边界、结果、偏差 | 主张措辞与已通过证据门及未决风险一致 |

每个门形成签署的评审发现，并给出 `APPROVE`、`APPROVE WITH ACTIONS` 或 `REWORK` 决定。涉及解释、oracle 正确性或主张发布时，评审者原则上应独立于产物作者。

---

## 5. 保证论证

> **v4.3 超越说明。** 在候选基线 `RB-2026-001-v4.3`
> （[`CR-2026-004`](../../../docs/control/changes/CR-2026-004.md)）下，下述
> 论证通过面向认证的链条重新解释：义务→验证目标→验证活动→证据→受评审的目标满足→
> 合规证据索引。主张 C0–C6 仍描述工程实质，但其分类被重划：C1–C3 映射到保证状态
> A1–A3，而 C4–C5（检测充分性和校准）为研究证据主张，映射到 R2–R5，不是更高面向
> 认证保证层级。下方数学命题 1–3 不变；仅澄清其在保证论证中的角色。内部门为项目
> 自定义，非权威评审门。

### 5.1 顶层主张

> 对于固定标准版本 \(S\)、适用性声明 \(P\)、观测边界 \(O\)、受控环境 \(E\) 和评价故障集 \(\mathcal{M}_{\mathrm{eval}}\)，记录证据支持以下主张：IUT 对所有有效执行的基础验证用例表现出 oracle 可接受行为，且 VCS 检测到了其声明覆盖的每个已评价非等价故障成员。

这是证据支持的范围受限主张，不是对 IUT 全部可能行为的无限定定理。

### 5.2 论证结构

```text
C0  范围受限符合性证据足以支持声明用途。
|
+-- C1  适用需求集受到控制且可追踪。
|   +-- CRS、适用性声明、裁决日志
|
+-- C2  每种适用验证义务均关联一个或多个用例。
|   +-- rho_RT、rho_TV、覆盖矩阵
|
+-- C3  执行有效，判定可复现。
|   +-- 前置条件、重置、带时戳迹、稳健 oracle 记录、
|       时钟元数据、误差预算、工具版本
|
+-- C4  检测能力受到明确边界约束并经过测量。
|   +-- 故障域、等价变异分析、留出结果
|
+-- C5  定量解释经过校准且受假设约束。
|   +-- 校准数据集、似然模型、敏感性分析
|
+-- C6  独立门禁控制产物和主张质量。
    +-- 检查记录、评审发现、批准项、未决行动
```

### 5.3 命题 1——追踪关系复合

若每个 \(r\in R_{\mathrm{app}}\) 至少关联一个 \(t\in T\)，且每个这样的 \(t\) 至少关联一个 \(v\in V\)，则式（1）成立。

**证明。** 任取 \(r\in R_{\mathrm{app}}\)。根据第一个前提，存在 \(t\) 使 \((r,t)\in\rho_{RT}\)。根据第二个前提，存在 \(v\) 使 \((t,v)\in\rho_{TV}\)。因此式（1）要求的存在量词见证成立。由于 \(r\) 任意，结果对全部适用需求成立。 \(\square\)

该命题只证明追踪关系复合，不证明 \(t\)、\(v\) 或 oracle 的语义充分性。

### 5.4 命题 2——基础/扩展逻辑不变性

令 \(V_B\) 为基础 VCS，\(V_E\) 为项目扩展 VCS。定义基础主张函数：

\[
\Gamma_B:\mathrm{Results}|_{V_B}\rightarrow
\{\mathrm{supported},\mathrm{not\ supported},\mathrm{incomplete}\}.
\]

若 \(\Gamma_B\) 只依赖结果在 \(V_B\) 上的投影，则当基础结果不变时，加入 \(V_E\) 不改变逻辑基础主张：

\[
\Gamma_B(\mathrm{Results}|_{V_B})
=
\Gamma_B((\mathrm{Results}\cup \mathrm{Results}_E)|_{V_B}).
\]

这是逻辑不变性，而不是执行隔离。运行时非干扰还需要重置、顺序和环境控制。

### 5.5 命题 3——有限变异体可区分性

若式（4）成立，则 \(\mathcal{M}_{\mathrm{eval}}\) 的每个成员都能在声明的 oracle 和环境下被至少一个用例与 \(G\) 区分。

该结论直接来自式（3）的 `Kill` 定义。除非给出合理的故障域泛化关系，否则不能将结论推广到 \(\mathcal{M}_{\mathrm{eval}}\) 之外。

---

## 6. 避免语义混淆的定量证据

> **v4.3 超越说明。** 在候选基线 `RB-2026-001-v4.3` 下，6.3 节的校准符合性信念被
> 归类为**研究证据**主张（R4 成熟度），而非面向认证保证主张。未达校准解释不阻塞
> 面向认证的关闭（A4）。建立普通协议验证证据无需校准后验，贝叶斯或统计校准不是认证
> 目标。本节的方程与测量语义不变；只有其在保证模型中的分类由 v4.3 澄清。

### 6.1 必须区分的三种量

| 量 | 含义 | 常用符号 |
|---|---|---|
| **覆盖** | 某目标是否至少存在一个充分用例 | \(\mathrm{Cov}\) |
| **运行重复性** | 在定义的重复执行制度下得到 PASS 的概率 | \(q_j\) |
| **符合性认知信念** | 在校准模型和证据下，相信固定符合性命题成立的程度 | \(p_j\) |

覆盖不是概率，运行重复性也不自动等于符合性信念。

### 6.2 运行重复性模型

对验证义务 \(j\)，将有效重复执行编码为：

\[
Y_{j,r}=
\begin{cases}
1,&\mathrm{PASS}\\
0,&\mathrm{FAIL}.
\end{cases}
\]

只有在预先声明的条件独立同分布制度下，才采用：

\[
Y_{j,r}\mid q_j\sim\mathrm{Bernoulli}(q_j).
\tag{7}
\]

若 \(n_j\) 次有效执行中有 \(c_j\) 次 PASS：

\[
\hat q_j=\frac{c_j}{n_j}.
\tag{8}
\]

精确双侧 \(1-\delta\) Clopper–Pearson 区间为：

\[
\left[
B^{-1}\!\left(\frac{\delta}{2};c_j,n_j-c_j+1\right),
B^{-1}\!\left(1-\frac{\delta}{2};c_j+1,n_j-c_j\right)
\right],
\tag{9}
\]

并对 \(c_j=0\) 或 \(c_j=n_j\) 使用标准边界约定。

返回同一协议状态并不能保证 i.i.d.。该假设要求受控重置、稳定配置、适当的执行顺序随机化，以及对共享批次或环境效应的分析。若存在过度离散或聚类，应使用 beta-binomial、混合效应模型或聚类 bootstrap。

`INCONCLUSIVE` 和 `ERROR` 单独报告；除非预先定义处理政策，否则不得计入 \(n_j\)。

### 6.3 经过校准的符合性命题

定义：

\[
C_j=
\begin{cases}
1,&\text{固定 IUT 符合义务 }j\\
0,&\text{固定 IUT 不符合义务 }j.
\end{cases}
\]

对声明的 IUT 总体和执行机制定义预测率：

\[
s_j=P(Y=1\mid C_j=1)
\]

表示真 PASS 概率（即一减误失败概率），并令：

\[
b_j=P(Y=1\mid C_j=0)
\]

表示假 PASS、漏检或逃逸概率。对下述似然比，假设
\(0<s_j<1\) 且 \(0<b_j<1\)；边界值必须采用相应的极限似然，
不能通过零似然相除处理。

在条件独立假设下，对 \(c\) 次 PASS 和 \(f\) 次 FAIL：

\[
L_1=s_j^c(1-s_j)^f,\qquad
L_0=b_j^c(1-b_j)^f.
\tag{10}
\]

支持符合性相对于不符合性的贝叶斯因子为：

\[
\mathrm{BF}_{10}=\frac{L_1}{L_0}.
\tag{11}
\]

给定显式先验 \(\pi_j=P(C_j=1)\)：

\[
P(C_j=1\mid Y)=
\frac{\pi_j L_1}
{\pi_j L_1+(1-\pi_j)L_0}.
\tag{12}
\]

只有当 \(s_j\)、\(b_j\)、条件独立性和先验均有合理依据时，式（12）才有效。优先报告似然或贝叶斯因子，并给出后验对一系列先验的敏感性。

### 6.4 校准要求

- 用符合参考实现或经独立裁决的符合执行估计 \(s_j\)。
- 用具有代表性的**留出**不符合实现或故障估计 \(b_j\)。
- 保留 \(s_j\)、\(b_j\) 的不确定性，不得只代入点估计而不做敏感性分析。
- 当不同故障类别检测能力差异明显时，按类别校准。
- 若校准集过小、不具代表性或已用于设计同一测试，则不得报告后验。

未满足门槛时，只报告 T0–T2 证据。

### 6.5 组合多个义务

令：

\[
p_j=P(C_j=1\mid \mathcal{E})
\]

表示 \(J\) 个义务的后验。在没有依赖模型时，联合符合概率满足 Fréchet 界：

\[
\max\left(0,\sum_{j=1}^{J}p_j-(J-1)\right)
\le
P\left(\bigcap_{j=1}^{J}\{C_j=1\}\mid \mathcal{E}\right)
\le
\min_j p_j.
\tag{13}
\]

式（13）要求每个 \(p_j\) 本身都是针对目标命题和证据制度的可辩护边际概率。共同的未校准仪表偏差可能同时移动多个边际；代数上的 Fréchet
界不会消除这种共享测量偏差。项目必须对共同偏差建模或给出界限、使用独立参考证据重新校准，或者不发布联合标量主张。

因此：

- \(\min_j p_j\) 是联合符合概率的**上界**，不是下界；
- 只有独立性成立时才能相乘边际概率；
- 只有合理的一阶 Markov 结构成立时才能相乘一阶条件概率；
- 当下界没有信息时，不报告单一标量。

本基线使用：

1. 经校准时的义务向量 \((p_1,\ldots,p_J)\)；
2. 式（13）的无依赖区间；
3. 按服务、角色和故障类别分组的结果。

### 6.6 不排除未验证元素

适用义务若没有有效证据，则标记为 `UNVERIFIED`。不得为了改善汇总结果而将其移除。相应高层主张为 `INCOMPLETE`。

---

## 7. 故障诊断

### 7.1 基线诊断模型

令 \(F\in\{f_0,f_1,\ldots,f_K\}\) 表示无故障或声明故障类别。令 \(X\) 为失败特征向量，包含：

- VC 判定；
- 错误码；
- 超时特征；
- 报文/字段异常；
- 最后接受状态/转移；
- 重试次数；
- 完整性检查结果。

贝叶斯诊断模型为：

\[
P(F=f\mid X=x)
\propto
P(X=x\mid F=f)P(F=f).
\tag{14}
\]

似然由故障注入数据估计。朴素条件独立分解只能作为显式声明的基线；相关特征需要贝叶斯网络、正则化分类器或其他经验证模型。

### 7.2 与 FMEA/FMECA 的关系

FMEA/FMECA 记录：

- 对象或转移；
- 失效模式及原因；
- 局部和全局影响；
- 严重度；
- 检测 VC；
- 对应故障算子；
- 证据状态。

严重度不是概率，也不由诊断分类器推断。可以综合后验诊断概率和独立治理的严重度对故障排序，但组合规则必须显式定义。

### 7.3 评价

使用按故障实例划分的交叉验证或留出集评价诊断，并报告：

- 混淆矩阵；
- Top-1 和 Top-3 准确率；
- macro precision、recall 和 F1；
- 若输出概率，报告校准结果；
- 分故障类别结果；
- 低置信条件下的拒判率。

### 7.4 时序诊断模型的选用规则

只有满足下列条件时才考虑 HMM：

- 隐故障状态预期随时间变化；
- 序列索引具有一致物理含义；
- 转移和发射参数可识别；
- 存在足够时序故障数据；
- HMM 的表现超过简单诊断基线。

固定实现中的故障在一系列测试中被观测，并不自动满足这些条件。因此 HMM/Viterbi 属于未来候选，不是核心方法。

---

## 8. 评价设计

### 8.1 基线

| ID | 方法 |
|---|---|
| **B0** | 现有工程/ICD 测试集 |
| **B1** | 仅需求追踪 |
| **B2-U** | 需求 + 无时钟 EFSM 义务覆盖 |
| **B2-T** | B2-U + 带时钟 EFSM、时序分区和稳健时序 oracle |
| **B3** | 使用开发变异体改进的 B2-T |

### 8.2 主要指标

- 适用需求覆盖；
- 分类别义务覆盖；
- 状态、转移、守卫和数据分区覆盖；
- 时序边界、时序分区和时钟复位覆盖；
- 稳健时序 PASS/FAIL/INCONCLUSIVE/ERROR 数量；
- 留出时序故障检测率和错误判定率；
- 开发变异分数；
- 带区间估计的留出故障检测率；
- VCS 规模；
- 导出和评审工时；
- 评审缺陷密度、行动关闭率和下游缺陷逃逸率；
- 门禁周转时间和返工工时；
- 执行时间；
- 无效/等价变异体比例；
- 存活故障分析；
- 评审者一致性。

### 8.3 时序符合性分析

对每条时序义务 \(r\)，报告：

- 允许区间 \(I_r\)、观测区间 \(I_{\mathrm{obs}}\) 和到每个边界的带符号裕量；
- 时间源、分辨率、误差预算分量和触发/响应配对规则；
- 按时序分区和环境统计的稳健判定数量；
- 按时序故障算子统计的留出检测结果；
- 观测延迟的中位数和声明的高分位数，但仅作为运行性能描述，不替代确定性判定；
- 顺序、批次、重置、自相关、聚类和漂移诊断。

令 \(D_{r,k}\) 为有效重复 \(k\) 的测量延迟，仅当稳健时序判定为 PASS 时定义
\(Y^{(T)}_{r,k}=1\)。于是
\(\widehat q^{(T)}_r=\sum_kY^{(T)}_{r,k}/n_r\)
估计声明重复运行制度下的运行时序 PASS 概率，而不是固定 IUT 符合的概率。如果存在顺序、批次或共享状态效应，应使用 beta-binomial、混合效应模型或 cluster bootstrap，而不是独立同分布 Bernoulli 区间。

### 8.4 定量证据指标

启用 T3 时报告：

- Brier score；
- log loss；
- 可靠性/校准曲线；
- 具有分箱敏感性分析的 Expected Calibration Error；
- 后验对先验和校准不确定性的敏感性；
- 存在重复数据集时，所声明区间的实际覆盖。

### 8.5 诊断指标

- Top-1/Top-3 准确率；
- macro F1；
- 分类别召回率；
- 拒判—性能曲线；
- 定位耗时；
- 与仅按 FMEA 严重度排序的基线比较。

### 8.6 实验控制

- 预注册最终故障算子和留出划分；
- 对所有工具、用例、模型和数据集版本化；
- 在收集确认性证据前验证单调时钟行为、时间戳分辨率、触发/响应配对和误差预算；
- 存在顺序效应时随机化执行顺序；
- 根据用例模式在用例间重置 IUT；
- 条件允许时，将测试设计人员与留出故障裁决人员分离；
- 保存负向结果和存活故障；
- 对随机工具同时保存固定种子和独立重复种子。

---

## 9. 合成数值示例

本节仅演示计算，**不构成** ARINC 615A 证据。

### 9.1 单义务证据

假设义务 \(j\) 的校准结果为：

\[
s_j=0.95,\qquad b_j=0.20.
\]

IUT 随后产生四次 PASS、一次 FAIL：

\[
c=4,\qquad f=1.
\]

根据式（10）：

\[
L_1=0.95^4(0.05),\qquad
L_0=0.20^4(0.80).
\]

因此：

\[
\mathrm{BF}_{10}
=
\frac{0.95^4(0.05)}{0.20^4(0.80)}
\approx31.817.
\]

当先验 \(\pi_j=0.5\)：

\[
P(C_j=1\mid Y)\approx0.9695.
\]

后验依赖先验：

| 先验 \(\pi_j\) | 后验 |
|---:|---:|
| 0.1 | 0.7795 |
| 0.5 | 0.9695 |
| 0.9 | 0.9965 |

这就是后验必须同时报告贝叶斯因子和先验敏感性的原因。

### 9.2 多个义务

假设三个经过校准的义务后验为：

\[
(p_1,p_2,p_3)=(0.97,0.95,0.96).
\]

在没有依赖模型时，式（13）给出：

\[
\max(0,0.97+0.95+0.96-2)
\le P(C_1\land C_2\land C_3\mid \mathcal{E})
\le0.95,
\]

即：

\[
0.88\le P(C_1\land C_2\land C_3\mid \mathcal{E})\le0.95.
\]

若额外假设独立，则乘积为：

\[
0.97\times0.95\times0.96=0.88464.
\]

除非独立性得到论证，否则不使用乘积，基线仍报告无依赖区间。

### 9.3 变异证据

若杀死五个开发变异体，可辩护的表述是：

> VCS 杀死了声明开发集中 5/5 个有效、非等价变异体。

不能表述为：

> 诊断覆盖率至少为 100%。

泛化能力必须使用 \(\mathcal{M}_{\mathrm{holdout}}\) 或真实缺陷评价。

### 9.4 稳健时序判定

假设一个合成响应必须发生在：

\[
I_r=[100,120]\ \mathrm{ms}
\]

经评审的端到端测量误差为 \(\varepsilon=3\ \mathrm{ms}\)。

- 若 \(\widehat{\Delta t}=115\ \mathrm{ms}\)，则
  \(I_{\mathrm{obs}}=[112,118]\ \mathrm{ms}\subseteq I_r\)：`PASS`。
- 若 \(\widehat{\Delta t}=118\ \mathrm{ms}\)，则
  \(I_{\mathrm{obs}}=[115,121]\ \mathrm{ms}\)：`INCONCLUSIVE`，因为测量既不能确定满足，也不能确定违反。
- 若 \(\widehat{\Delta t}=124\ \mathrm{ms}\)，则
  \(I_{\mathrm{obs}}=[121,127]\ \mathrm{ms}\) 与 \(I_r\) 不相交：`FAIL`。

把 118 ms 当成精确 PASS 会丢弃已知测量不确定性。本例只说明 oracle 语义，不定义任何 ARINC 615A 时序值。

---

## 10. 证据门槛与研究决策规则

| 门槛 | 要求 | 未满足时 |
|---|---|---|
| **G0——范围** | 固定标准版本、角色、服务和 PICS 式适用性 | 不作基础主张 |
| **G1——追踪** | 式（1）、（2）满足并经过评审 | T0 不完整 |
| **G2——执行有效性** | 前置条件、重置、环境、时间戳链、误差预算和 oracle 证据有效 | 无效仪器/环境记为 ERROR；边界证据无法判定时记为 INCONCLUSIVE |
| **G3——故障域质量** | 完成有效/等价处理和留出划分 | 不作 T2 泛化 |
| **G4——校准** | 有代表性地估计 \(s_j,b_j\) 及其不确定性 | 不报告符合性后验 |
| **G5——依赖性** | 依赖模型得到论证和验证 | 只报告 Fréchet 界/向量 |
| **G6——诊断** | 留出诊断性能超过基线 | 不宣称自动故障定位 |
| **G7——可迁移性** | 完成第二协议实例 | 不宣称协议无关性 |

这些门槛决定项目在各阶段能够作出的主张。工程进度不能豁免未满足的研究门槛。

---

## 11. 有效性威胁

### 11.1 构念有效性

- 规范性需求可能被错误拆分或解释。
- 变异体可能无法代表真实不符合性。
- PASS/FAIL oracle 可能遗漏相关观测。
- 时序触发、复位、取消或静默语义可能建模错误。
- 无依据的误差预算可能产生错误 PASS、错误 FAIL 或过多 INCONCLUSIVE。
- 后验可能更多反映校准集，而非目标 IUT 总体。

### 11.2 内部有效性

- 共享状态或环境可能破坏运行独立性。
- 开发变异体信息可能泄漏至留出评价。
- 工具缺陷可能被误判为 IUT 失败。
- 执行顺序可能影响结果。
- 时钟漂移、调度器负载、网络不对称或跨会话计时器状态可能造成相关时序观测。

### 11.3 外部有效性

- 单个 ARINC 615A 实现不能建立可迁移性。
- 仿真器可能无法重现目标网络时序或硬件行为。
- 以 TFTP 为中心的服务结果可能无法迁移到无状态、广播或实时协议。

### 11.4 结论有效性

- 小故障集导致较大不确定性。
- 等价变异体分类可能带有主观性。
- 多重比较和类别不平衡可能夸大诊断结论。
- 不带不确定性的点估计可能夸大证据。
- 共同的未校准仪表偏差可能耦合多个估计边际；对这些估计应用
  Fréchet 界并不能恢复其有效性。

缓解措施包括双人评审、裁决日志、留出故障、保存负向结果、敏感性分析、复现包和第二协议实例。

---

## 12. 复现包

在遵守专有标准文本限制的前提下，研究发布包应包含：

```text
requirements/
  applicability.yaml
  crs.csv
  crs_adjudication.md
models/
  a615a_timed_efsm.*
  timing_obligations.yaml
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
  timing.*
  mutation.*
  calibration.*
  diagnosis.*
```

所有报告表格和图必须能够从版本化原始数据及脚本重现。专有标准文本使用稳定引用和 hash 表示，不复制到公开产物。

---

## 13. 研究路线图

### 阶段 1——可辩护测试核心

1. 冻结范围和适用性。
2. 通过 RG0 范围评审。
3. 提取并裁决完整 CRS；通过 RG1。
4. 建立带时钟的可观测 ARINC 615A EFSM、时序目录和追踪模型；通过 RG2。
5. 导出 TP 和 VC，验证稳健时序及离散 oracle 逻辑，并通过 RG3。
6. 完成追踪及义务覆盖。

**研究输出：** T0 方法和产物。

### 阶段 2——有限充分性

7. 定义故障算子及 FMEA/FMECA 映射。
8. 建立开发和留出故障集。
9. 通过 RG4 执行就绪性检查。
10. 执行变异和留出评价。
11. 执行时序边界、时钟复位、不确定性和留出时序故障研究。
12. 复现证据包并通过 RG5。
13. 比较 B0、B1、B2-U、B2-T 和 B3 基线。

**研究输出：** T1/T2 证据和经验评价。

### 阶段 3——校准证据与诊断

14. 校准误失败和漏检行为。
15. 评价贝叶斯因子、后验和敏感性。
16. 训练并评价基线诊断模型。
17. 只有物理状态含义明确且数据充分时才考虑 HMM/贝叶斯网络扩展。
18. 任何定量符合性主张发布前均须通过 RG6。

**研究输出：** 可选 T3 证据。

### 阶段 4——可迁移性

19. 将方法应用于具有不同特性的第二种协议。
20. 识别不变步骤和协议特定步骤。
21. 根据跨实例证据修订贡献主张。

**研究输出：** 支持或反驳协议无关性的证据。

---

## 14. 结论

本报告建立了一套用于构造和评价 ARINC 615A 范围受限符合性保证论证的一体化测试—分析方法论。

**测试路径**将适用需求落实为受控刺激、可观测行为、可执行 oracle、判定和可复现带时戳迹。**分析路径**判断覆盖了哪些离散和时序义务、时序判定在测量不确定性下是否仍然有效、VCS 对声明故障类别的检测能力如何、观测支持何种不确定性结论，以及下一步应采取什么验证行动。两条路径都不可单独替代另一条：没有测试，分析缺少受控经验观测；没有分析，测试无法说明其结论的范围和强度。

独立评审与检查门把研究逻辑转化为工程控制系统，阻止未解决的歧义、不完整追踪、薄弱 oracle 逻辑、失控执行配置、不可复现证据和过度主张向下游传播。

核心学术贡献是精确区分逻辑序列、确定性实时时间符合性、运行顺序依赖、隐含时序动力学、覆盖、有效执行、有限检测充分性、运行重复性、校准信念和诊断等语义，并用命题和实验评价它们之间的关系。核心工程贡献是形成可复用产物链和决策过程，将资源导向可观测风险，防止时序仪器制造虚假精度，尽早暴露返工，保存证据，并支持可审计发布决策。

因此，该方法论既是研究基线，也是工程运行模型。其价值将通过 §10 的证据门、§4.10 的独立评审门、留出故障研究、校准实验和第二协议复现实验逐步建立。

---

## 附录 A——符号表

| 符号 | 含义 |
|---|---|
| \(S\) | 固定协议标准版本 |
| \(P\) | 实现适用性声明 |
| \(O\) | 声明的观测边界 |
| \(R(S)\) | 提取的规范性需求项 |
| \(R_{\mathrm{app}}\) | 对 \(P\) 适用的需求 |
| \(T\) | 测试目的集合 |
| \(V\) | 验证用例集合 |
| \(\rho_{RT}\) | 需求—测试目的关系 |
| \(\rho_{TV}\) | 测试目的—验证用例关系 |
| \(G_T\) | 带时钟的可观测 EFSM 规范 |
| \(C\) | 有限模型时钟集合 |
| \(\sigma_T\) | 带时间戳的可观测迹 |
| \(\bot_r@t_H\) | 义务保持有效但直到观测终点 \(t_H\) 仍未观测到响应 |
| \(I_r=[L_r,U_r]\) | 需求定义的允许时序区间 |
| \(I_{\mathrm{obs}}\) | 应用测量误差界后的观测区间 |
| \(D_r\) | 经评审的延迟物理定义域；仅在有依据时通常取 \([0,\infty)\) |
| \(\varepsilon_{ij}\) | 有依据的时序测量误差界 |
| \(\mathcal{M}_{\mathrm{exec}}\) | 可构建且可执行的变异体集合 |
| \(\mathcal{M}_{\mathrm{equiv}}\) | 在观测范围内等价的可执行变异体集合 |
| \(\mathcal{M}_{\mathrm{eval}}\) | 已评价有效、非等价故障集 |
| \(\mathcal{E}\) | 已记录证据数据集 |
| \(q_j\) | 义务 \(j\) 的运行 PASS 概率 |
| \(C_j\) | 义务 \(j\) 的固定潜在符合性命题 |
| \(s_j\) | \(P(\mathrm{PASS}\mid C_j=1)\) |
| \(b_j\) | \(P(\mathrm{PASS}\mid C_j=0)\) |
| \(\pi_j\) | \(C_j=1\) 的先验概率 |
| \(p_j\) | 后验概率 \(P(C_j=1\mid \mathcal{E})\) |

---

## 附录 B——最低报告检查表

- [ ] 固定标准版本和精确范围
- [ ] 版本化适用性声明
- [ ] CRS 经独立评审和裁决
- [ ] 所有来源按条款/表格/页码引用
- [ ] 导出需求、TP、VC 和模型关系
- [ ] 全部必需义务类别得到覆盖
- [ ] EFSM 变量包含相关历史、计数器、选项和重试状态
- [ ] 每条时序义务定义触发、响应、取消/静默、界限、单位、时钟复位和来源引用
- [ ] 单调时间源、时间戳位置、分辨率和误差预算经过评审
- [ ] 在适用处覆盖稳健时序 oracle 及过早/标称/边界/过晚/无响应分区
- [ ] 判定包含 PASS/FAIL/INCONCLUSIVE/ERROR
- [ ] 定义重置和隔离程序
- [ ] 变异体分类为有效/等价/无效
- [ ] 开发和留出故障集相互分离
- [ ] 变异结果包含不确定性和存活体
- [ ] 未经校准不报告后验
- [ ] 未分析依赖性不报告单一汇总标量
- [ ] 使用留出故障实例评价诊断
- [ ] 保存原始数据、脚本、版本和种子
- [ ] 保留负向及不确定结果
- [ ] 保留时序裕量、时钟元数据、顺序效应、聚类和漂移诊断
- [ ] 主张边界在范围、结果和结论中保持一致

---

## 参考文献

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

[16] RTCA DO-178C (2011). *Software Considerations in Airborne Systems and Equipment Certification.* 本报告仅将其作为相邻软件保证背景，不宣称直接满足认证要求。

[17] ARINC 615A-4. *Software Data Loader Using Ethernet Interface.* 受控 CRS 必须记录精确条款和页码。

[18] NIST. *Conformance Testing.* https://www.nist.gov/itl/ai/applied-ai-research-group/conformance-testing

[19] NASA (2016). *NASA Systems Engineering Handbook*, NASA/SP-2016-6105 Rev 2. https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf

[20] ISO/IEC 20246:2017. *Software and systems engineering — Work product reviews.* https://www.iso.org/standard/67407.html

[21] Alur, R., & Dill, D. L. (1994). A Theory of Timed Automata.
*Theoretical Computer Science*, 126(2), 183–235.
https://doi.org/10.1016/0304-3975(94)90010-8

[22] Joint Committee for Guides in Metrology (2008). *Evaluation of
Measurement Data — Guide to the Expression of Uncertainty in Measurement*,
JCGM 100:2008. https://doi.org/10.59161/JCGM100-2008E

[23] Joint Committee for Guides in Metrology (2012). *The Role of Measurement
Uncertainty in Conformity Assessment*, JCGM 106:2012.
https://doi.org/10.59161/JCGM106-2012

---

*AI 辅助研究披露：AI 工具协助完成草拟和一致性检查。数学主张、标准解释、参考文献和实验结论均须由可问责的人类评审者复核。只有在书目信息和所支持命题均已检查后，报告才可声明某条引用已经验证。*

## 15. 面向认证的 v4.3 证据架构

在候选基线 `RB-2026-001-v4.3` 下，本报告的数学与时序符合性语义原样继承；式 1–14 与时序式 T1–T5 不变。架构扩展为面向认证的证据模型：需求→验证目标→验证定义→受控执行→执行证据清单→目标满足→合规证据索引。

第 2.3 节的 T0–T3 阶梯由两个正交轴替代：面向认证保证状态 A0–A4 与研究证据成熟度状态 R0–R5。执行判定、目标状态与合规状态相互区别；任何 `PASS` 不得自动满足目标或支持主张。突变充分性、校准、诊断和迁移性为仅研究扩展，不授予认证状态。这些状态为项目自定义，非权威保证层级。见 [`CERTIFICATION_EVIDENCE_BASIS.md`](CERTIFICATION_EVIDENCE_BASIS.md) 及 `docs/control/contracts/` 下的合规/目标契约。
