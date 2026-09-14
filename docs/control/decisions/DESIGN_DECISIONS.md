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

## DD-007 — Freeze RR-2026-001 v4.1 as the methodology baseline

**Decision:** Adopt `RB-2026-001-v4.1` as the normative research-method
baseline for subsequent requirements, engineering, experiments, analysis, and
publication work.

**Why:** The report now separates analytical objects, bounds every assurance
tier, resolves the blocking probability and fault-domain errors, and defines
operational review/evidence gates.

**Date:** 2026-07-26
**Status:** Active; supersedes any inconsistent methodology language in earlier
outlines and proposals.

---

## DD-008 — Test and Analysis are complementary primary paths

**Decision:** Test produces controlled observations and verdict evidence;
Analysis evaluates coverage, adequacy, uncertainty, and diagnosis. Neither is
treated as sufficient alone.

**Why:** This architecture creates both scientific evaluability and an
engineering feedback loop.

**Date:** 2026-07-26
**Status:** Active

---

## DD-009 — Review and Inspection are cross-cutting gates

**Decision:** Implement RG0–RG6 as independent static controls across the
Test-and-Analysis loop. Demonstration remains optional and cannot replace
detailed protocol evidence.

**Why:** Artifact defects and overstated claims need prevention before they
propagate into execution or release.

**Date:** 2026-07-26
**Status:** Active

---

## DD-010 — Retire DTMC/HMM as baseline conformance machinery

**Decision:** Protocol behavior remains an EFSM/IOLTS; calibrated inference and
diagnosis use separately defined models. DTMC edge labels, weakest-link
“probabilities,” path products, and HMM/Viterbi localization are not baseline
claims.

**Why:** Protocol topology, evidence, and stochastic inference are different
mathematical objects. Temporal models require independently demonstrated state
meaning, identifiability, data sufficiency, and comparative performance.

**Date:** 2026-07-26
**Status:** Active; supersedes DD-002 where it described DTMC/HMM vocabulary as
the active quantitative story.

---

## DD-011 — Gate-earned claim release

**Decision:** All research and engineering claim wording is controlled by
`docs/research/CLAIM_EVIDENCE_MATRIX.md`. T0–T3, diagnosis, engineering
reproducibility, and transferability are promoted only by their required
evidence and gates.

**Why:** Repository progress and passing tests are not substitutes for an
assurance argument.

**Date:** 2026-07-26
**Status:** Active

---

## DD-012 — Add deterministic timed conformance without restoring stochastic protocol semantics

**Decision:** Adopt `RB-2026-001-v4.2`. Extend the observable EFSM with clocks,
clock guards, invariants, and resets; represent executions as timestamped
traces; and use an interval-based robust timing oracle with an explicit
measurement-error budget. Co-locate the Chinese translation after each key
English document rather than maintaining parallel language files.

**Why:** Timing obligations are already in scope, but v4.1 did not give them a
complete mathematical or measurement semantics. A point-threshold oracle can
create false precision near a boundary. Co-located translations reduce
structural drift. Protocol topology remains deterministic/nondeterministic as
declared and is not converted into a DTMC or HMM.

**Date:** 2026-07-30

**Status:** Active. Approved by `GR-PR6-RB-2026-001-v4.2` and made effective by
the merge of PR #6. v4.2 supersedes v4.1 as the current methodology baseline
identifier, while DD-010 remains active. v4.1 evidence is not automatically
relabelled as v4.2 evidence.

### 中文

采用 `RB-2026-001-v4.2`：在可观测 EFSM 中加入时钟、时钟守卫、不变量和复位；将执行表示为带时戳迹；以显式测量误差预算驱动区间式稳健时序 oracle；关键英文文档末尾直接附中文译本。原因是 v4.1 已将时序义务纳入范围，却没有完整数学和测量语义，点阈值会在边界制造虚假精度。该决定不恢复 DTMC/HMM 协议语义。

---

## DD-013 — Separate product domains through controlled, traceable contracts

**Decision:** Treat methodology research/publication, engineering
implementation, and verification tutorials as distinct product domains. Keep
governance and controlled requirements as their shared contract layer. Move the
authoritative report from `docs/study/` to `docs/methodology/`; separate common
and ARINC 615A tutorial entry points; and require cross-domain dependencies to
identify upstream artifact versions and applicable gate records. Publication
and tutorials remain downstream. Evidence-driven feedback changes an upstream
contract only through CR/DD and Review control.

**Why:** Complete independence is neither possible nor useful: research needs
engineering evidence, engineering implements method semantics, and tutorials
explain both. Explicit direction and trace records reduce accidental coupling
without breaking the integrated verification loop.

**Date:** 2026-07-31

**Status:** Active. Approved by `GR-PR6-RB-2026-001-v4.2` and made effective by
the merge of PR #6. Product domains are coupled only through controlled contracts;
tutorials are non-normative, publication cannot modify methodology, and
upstream-changing feedback enters through CR/DD and Review control.

The locations established by this decision were reorganized by active
DD-014/CR-2026-003 through PR #7, without changing the dependency semantics.

---

## DD-014 — Separate the reader release surface from the developer control plane

**Decision:** Adopt the information architecture and reporting contract in
CR-2026-003. Keep only the reader-oriented README at the repository root; keep
machine-discovered configuration at its conventional root paths; place all
reader deliverables under `artifacts/`; and give project, research,
engineering, and tutorial work one control entry each. Preserve evidence and
governance records as separate traceable artifacts. Release every reader update
as one self-contained report directly linked from the root README.

**Why:** Readers need one coherent release narrative, whereas developers need
atomic records, ownership, and audit history. Treating those needs as separate
surfaces reduces navigation noise without flattening the assurance argument or
weakening traceability.

**Date:** 2026-08-02

**Status:** Active. Approved by `GR-PR7-RB-2026-001-v4.2.1` and made effective
by the merge of PR #7. The review confirmed relocation completeness, link integrity,
bilingual parity, validator coverage, and no change to RR-2026-001 v4.2
mathematical or methodological semantics.

---

## DD-015 — Control ARINC 615A-3 as the sole active protocol source

**Decision:** Adopt ARINC 615A-3 as the sole active 615A protocol authority,
ARINC 665-5 as a bounded data-format reference, and ARINC 645 as an open
dependency. Withdraw every active 615A-4 dependency or target while preserving
registered frozen history as `HISTORICAL-SUPERSEDED`. The wire value `A4` is not
an edition identifier.

**Why:** Source identity must precede CRS derivation. Conflating wire version,
edition, later data formats, or open integrity algorithms would produce
untraceable requirements and false capability claims.

**Scope:** Source roles and migration control only; no standard text, CRS,
applicability decision, implementation or conformance conclusion is created.

**Status:** Disposition `ADOPT`, with formal activation governed by CR-2026-006.
Approval and ordinary-merge evidence are externally verified, not automated.

---

## DD-016 — Use a lightweight observable timed EFSM and bounded Test-Analysis

**Decision:** Retain one lightweight observable timed EFSM and complementary
Test-Analysis. Initially bound Analysis to obligation traceability,
state/transition/timing coverage, robust timing/error budgets, and finite-domain
mutation or held-out adequacy. Defer DTMC protocol semantics, HMM/ML diagnosis
and Bayesian calibration. FMEA may prioritize faults but cannot decide
conformance. TTCN-3 is neither a dependency nor a selected platform.

**Why:** This is the smallest route that preserves auditable engineering and
publishable analysis without introducing unidentifiable or uncalibrated models
before CRS, Configuration and execution data exist.

**Scope:** Technical direction only; no EFSM, oracle, test case, analysis model
or execution platform is implemented or selected here.

**Status:** Disposition `ADOPT`; formal activation uses the CR-2026-006 gate and
does not assert that approval or merge has occurred.

---

## DD-017 — Adopt injectable layers, gated open-source reuse and M0–M9 serial delivery

**Decision:** Use independently replaceable protocol-file, injected IO/clock/
trace, TFTP, 615A adaptation, operation, verification and evidence layers.
Allow L1 reference-only reuse with identity/license records; allow future L2
black-box comparison with fixed identity/license; prohibit L3 source/constants/
vectors until independent license, cleanliness and architecture-fit review.
Deliver M0–M9 serially, with M1 CRS/applicability next and no parallel stage PR.

**Why:** Injection makes timing and evidence deterministic; directional layers
contain change. Gated reuse prevents license and source-authority contamination,
and serial gates prevent implementation from outrunning requirements.

**Scope:** Target architecture and delivery policy only. No named open-source
implementation is registered for reuse, and no third-party material is copied.

**Status:** Disposition `ADOPT`; formal activation uses the CR-2026-006 gate and
M1 remains prohibited until approval and ordinary merge are externally verified.

## DD-018 — Use one authoritative M1 package and joint RG0/RG1 activation

**Decision:** The machine-readable M1 package is the sole authority; its Markdown
review view is generated. Audit the full 615A-3 scope and only 615A-3/service-
triggered 665-5 dependencies. Preserve source modality separately from
conformance effect. RG0 and RG1 close together only on one unchanged Head.

**Why:** One authority prevents status drift; complete coverage prevents keyword
selection bias; bounded dependency use prevents a later edition from silently
rewriting the active protocol. External GitHub approval is not created by local
Git history or automation.

**Scope:** M1 static requirements, applicability, dependencies and review only.
No model, Configuration, execution evidence, baseline, tag or conformance claim.

**Status:** Candidate disposition `ADOPT` under CR-2026-007; RG0/RG1 and formal
activation remain pending external independent review and ordinary merge.

## DD-019 — Defer direct 615A-to-665 requirement edges to M2

**Decision:** M1 admits ARINC 665-5 only at bounded Profile scope. Direct
requirement-level refinement, producer-constraint, and consumer-tolerance
edges remain prohibited until M2 performs attachment-anchored reconciliation.

**Why:** Shared words or data-object names do not prove implication. An edge
requires explicit evidence binding both source propositions.

**Status:** Candidate under CR-2026-007; it does not authorize M2 entry.

## DD-020 — Use generated projections and remove tautological semantic fields

**Decision:** Rename the deterministic bilingual template output to
`generatedSemanticProjectionEn/Zh` and treat it only as a drift anchor. Remove
the redundant requirement-level `roles`, `operations`, `category`, and
`obligations` fields; derive their display values from `semantic`.

**Why:** A generated template is not independent review evidence, and fields
forced to equal one semantic element carry no additional information.

**Status:** Candidate under CR-2026-007, pending full RG0/RG1 review.

## DD-021 — Reclassify Attachment 3 and Appendix E from informative to explicit deferral

**Decision:** ARINC 615A-3 Attachment 3 (FIND protocol detail) and Appendix E
(Data Loading Over AFDX) may no longer be classified
`NON-PROTOCOL-PRODUCT-OR-INFORMATIVE` while the corresponding profile-level
capability is deferred or the underlying dependency is not bound. Attachment 3
leaves are recorded as `DEFERRED-FUTURE-SCOPE` with rationale `DEFERRED-FIND-M9`;
Appendix E leaves are recorded as `DEFERRED-FUTURE-SCOPE` with rationale
`DEFERRED-AFDX-DEPLOYMENT-M2-INFRASTRUCTURE-BINDING`.

**Why:** Attachment 3 provides the normative definition of FIND while §5.3.3 is
already deferred; an "informative" tag on the definition contradicts the
deferral. Appendix E specifies deployment-normative constraints for AFDX
transport whose ultimate blockers are ARINC 664 Part 7 (not yet acquired) and
Part 2 (now bound); this should be closed by an explicit M2 infrastructure-
binding condition rather than hidden behind an informative tag.

**Scope:** Only coverage-ledger leaf reclassification; no CRS requirement is
added or removed, no `currentStop` moves.

**Status:** Candidate under CR-2026-007, pending external independent review.

## DD-022 — Controlled handling of public IETF RFCs

**Decision:** Public IETF RFCs (768, 791, 1123, 1350, 1785, 2347, 2348, 2349)
are not registered in `configs/research/controlled_sources.json` `sources[]`
(which is reserved for proprietary material subject to `SAR-2026-001`
identity-match). They remain in `openDependencies[]` with an added
`publicRetrieval` sub-object recording canonical URL, retrieval date, byte
count, and SHA-256. The text files themselves are stored under
`local-references/rfc/` (covered by `.gitignore`) and not committed.

**Why:** The existing baseline check enforces `LOCAL-PROPRIETARY-NO-REPOSITORY-COPY`
handling and independent acquisition-record matching for every `sources[]`
entry — public text does not fit that model. Keeping RFCs in `openDependencies`
preserves the correct "capability not yet established" semantics while
`publicRetrieval` records the exact version identity we intend to bind against
at requirement level.

**Scope:** Only registers RFC identity and retrieval metadata; does not
promote RFCs to requirement-level evidence, and does not clear the blocked
status of any `RFC-*`-affected capability.

**Status:** Candidate under CR-2026-007, pending external independent review.

---

## DD-023 — Receive network references without manufacturing applicability closure

Record P3-1 and P7 base-edition identities under CR-2026-007, retaining open
edition, network applicability and independent approval obligations. The received
editions are candidate inputs, not an assertion about the latest published standard.
The network inspection register distinguishes regions inspected for context from
atomic requirement coverage. The user selects Compliant Network, without P3
deviations. RFC 1122 is independently registered as a received public source.
The IPv4/UDP host service remains an unestablished infrastructure prerequisite,
not a complete RFC inventory or implementation conformance claim. M2 must plan
its substantiation before execution Configuration approval. Independent review
must accept the historical editions and this scope boundary. AFDX, its AID future-supplement reference, and addressing
choices remain deferred. Source receipt establishes no implementation capability.
Review the remaining applicability before further normative promotion; retain DD-019
and DD-020. Actual approval and merge facts are recorded externally on the unchanged
Head and ordinary merge, without a dedicated post-merge synchronization commit.

---

## DD-024 — Bind M2 to an observable timed EFSM with restricted clocks

M2 delivers one machine M = (S, s0, V, C, P, E, T, Inv) for UPLOAD and
INFORMATION, with Data Loader and Target Hardware as observation projections of
the same state. Timing uses restricted ASTs, explicit clocks, clock-enabled
timeouts and source-bound error-budget classes. Attachment 4 equations retain
retry and network-transmission terms. Unresolved bounds remain NOT-CHECKED. The
package is the model authority; M1 remains the immutable CRS input. No codec,
executable engine, TP/VC or Project Configuration is authorized.

**Scope:** Candidate model and obligation traces under CR-2026-008.

**Status:** Candidate under CR-2026-008, pending external independent review.

---

## DD-025 — Separate M1 input acceptance from technical action closure

Record the owner-accepted COMMENTED sign-off, ordinary two-parent merge, tree and
main CI in M2 `inputAcceptance`. Do not rewrite merged M1 bytes, fabricate a
GitHub APPROVED review, or claim a named independent reviewer. CR-2026-007 closing
text transfers residual actions to CR-2026-008; transfer is not technical closure.
Historical edition acceptance remains a conditional input until independent RG0
says otherwise.

**Scope:** Control-plane recording of merged M1 facts; not a ledger-only PR.

**Status:** Candidate under CR-2026-008, pending external independent review.

---

## DD-026 — Keep infrastructure premises distinct from established capabilities

Source-explicit 615A→665 and TFTP-option edges may be candidate refinements when
both ends are located. CRS-M1-00034 is a block-size candidate to RFC 2348 §2;
the conflicted 6.4.4 LUI/LUR file identity does not emit an active 665 edge.
IPv4/UDP and RFC 1122/1123 remain infrastructure premises with substantiation
planned for Project Configuration. ARINC 645 continues to block integrity
success. AFDX, FIND, media-set services and P3 profiled deviations stay deferred
or excluded. No behavior capability becomes ESTABLISHED in this candidate.

**Scope:** Premises, refinements and capability guards used by the M2 model.

**Status:** Candidate under CR-2026-008, pending external independent review.

---

## DD-027 — Successor M1 delta for file identity, without rewriting the frozen tree

A 6.4.4 LUI/LUR file-identity conflict and the §6.3.2 LUR WRQ actor mismatch remain
OPEN-M1-CORRECTION. That stop is correct and is not closure. The current M2
candidate must not request final RG0/RG1/RG2 APPROVE while those inputs stay
conflicted. After user authorization, a successor M1 package may correct only those
identities in new ordinary commits and new blob OIDs. Historical merge
`9bf18124d405b656815bc9eb524ae29bb4f04f56` and its frozen bytes stay unchanged
as a preserved record. Successor `inputAcceptance` is a new identity and must
not transplant the original merge approval onto new blobs. CR-2026-009 is one
authorization request with two pending items (6.4.4 file identity and
CRS-M1-00365 WRQ actor), authorizable together or separately; neither is
executed until authorized. NET-ISSUE-EDITION remains a separate independent
RG0 decision; OPEN text is not edition acceptance. CR-2026-009 records the
authorization request.

**Scope:** Input-correction authorization; not an M1 rewrite and not M2 final approval.

**Status:** Candidate under CR-2026-008 / CR-2026-009 / CR-2026-011. Owner
authorization granted 2026-09-10; successor delta executed under CR-2026-011;
independent RG1 still required.

### 2026-09-10 T1 execution

CR-2026-011 executes Items A and B plus the owner-authorized 6.4.5 LUR→LUS
companion. Successor `inputAcceptance` is a new identity and does not transplant
the frozen merge approval. `reviewControl.blocksFinalApproval` stays true.

### 2026-09-10 LUR write endpoints after RR-M2-2026-004

Independent review withdrew “receiver remains DLA” as mixing application-layer
DLA with a network-visible TFTP WRQ. The same CR-2026-009 Item B class now
records DATA-LOADER→TARGET-HARDWARE WRQ, TARGET-HARDWARE→DATA-LOADER ACK, and
DATA-LOADER→TARGET-HARDWARE DATA. This remains a bounded M2 baseline, not a
development-ready CRS.

---

## DD-028 — Adopt CL-TAV as the successor research method and two-PR sequence

**Decision (determined name and sequence; not a novelty claim):** The research
method name is **闭环测试—分析协同验证方法** / **Closed-Loop Test–Analysis
Verification**, abbreviated **CL-TAV**. The core is the closed loop
test → observation → constraint verdict / diagnosis → next-test selection.
CRS, SysML, models and evidence mechanisms support that loop; they are not a
substitute for the contribution.

Candidate thesis titles:

- CL-TAV：面向协议符合性验证与故障定位的闭环测试—分析协同方法——以 ARINC 615A 为例
- CL-TAV: Closed-Loop Test–Analysis Verification for Protocol Conformance and Fault Localization—An ARINC 615A Case Study

Two sequential PRs:

1. This increment (CR-2026-012): method report, paper plan, expanded protocol CRS.
2. A later PR: development-ready tool/verification/implementation contracts, only
   after the expanded protocol CRS is independently accepted.

RR-2026-001 v4.2 remains a preserved historical identity at the PR #6 freeze.
DD-007’s freeze is not a ban on successor revision. A successor method text is
allowed when an old→new disposition list and independent mathematical review
exist. Historical commit objects continue to verify against their original
bytes.

Original RQ1–RQ6 are retained as a mapping, not silently completed by deletion:

| Historical RQ | Disposition under CL-TAV |
|---|---|
| RQ1 Derivation | Supporting: still required for auditable CRS→TP/VC; not the primary research question of this increment |
| RQ2 Coverage | Supporting: coverage obligations remain; they feed Analysis constraints |
| RQ3 Bounded adequacy | Maps into the detection experiment family |
| RQ4 Evidence interpretation | Maps into the uncertainty / incomplete-observation research question |
| RQ5 Diagnosis | Becomes part of the closed-loop core (candidate update and next-test selection) |
| RQ6 Transferability | Not answered by this 615A instance; remains future work, not a completed claim |

Suggested successor RQs (candidate wording until the method report lands):

1. How does CL-TAV form a consistent loop among test observations, constraint
   verdicts, fault hypotheses and next-test selection?
2. Under the same budget, what is the effect of the closed loop versus fixed
   Test, appropriately defined Analysis, and non-feedback T+A on detection,
   localization and cost?
3. How do timing uncertainty, insufficient observation and incomplete
   model/fault domains affect algorithm conclusions and stopping?

**Scope:** Method naming, RQ mapping, two-PR sequence, historical method identity.

**Status:** Candidate under CR-2026-012. Name and sequence are taken as determined
by the executing work order. Independent review still required. Combination of
Test and Analysis is not claimed as a first invention.

---

## DD-029 — Candidate CL-TAV algorithm, observation abstraction and stop rules

**Decision status: CANDIDATE design direction.** This is the §17.3 stop. It is
not “user already decided.” Algorithm-related assertions must not be hardened
until the user or a named method reviewer confirms the direction. Source audit
and outline work that do not depend on these choices may continue.

### Adopted baseline (candidate)

Use a finite hypothesis set, set-valued compatibility and a bounded budget.
Do not require probability priors. Do not introduce HMM/DTMC/Bayesian machinery
unless a later CR states a distinct problem that those tools uniquely address.

Objects:

- \(H_0\): declared initial hypothesis set, including a no-fault / specified
  normal-behaviour hypothesis or an explicit “no no-fault element” rule.
- \(q_k\): current session / IUT-facing state and executed history. Test
  selection must not assume the IUT resets every round.
- \(H_k \subseteq H_0\): hypotheses still compatible with observations after
  round \(k\).
- \(T(q_k)\): tests executable in \(q_k\). Each test has \(\mathrm{cost}(t)>0\)
  in one declared unit (do not mix seconds, bytes and counts in one budget).
- \(O(h,t,q_k)\): abstract observations allowed by the declared model; may
  include timeout / data / timing partitions. Under nondeterminism, sets for
  different \(h\) may overlap.
- \(I_{z_k}\): feasible observation set corresponding to the actual measurement,
  including measurement uncertainty. Instrument/correlation failure returns
  `ERROR` and does **not** exclude hypotheses.

Candidate update (compatibility, not probability):

\[
H_{k+1} = \{ h \in H_k \mid O(h,t_k,q_k) \cap I_{z_k} \neq \emptyset \}.
\]

State and history must be updated with the executed test, the recorded
observation class, and correlation keys. The set formula alone is not a complete
algorithm.

### Selection rule (candidate) and alternatives

For every executable test with remaining budget \(\ge \mathrm{cost}(t)\),
compute the worst-case remaining candidate count over visible observation
classes:

\[
s(t) = \max_{o \in \mathrm{Obs}(t,q_k)} \bigl|\{ h \in H_k \mid O(h,t,q_k) \cap o \neq \emptyset \}\bigr|.
\]

Select \(\arg\min_t s(t)\). Ties: smaller \(\mathrm{cost}(t)\), then stable
test id. This is an interpretable minimax baseline, **not** claimed optimal.

Rejected as the default (may appear later as comparison arms, not replacements
without a new DD):

| Alternative | Why not default |
|---|---|
| Shannon information gain | Requires a probability distribution and usually disjoint partitions |
| Unit-cost expected remaining-set reduction | Still needs a distribution or an undeclared uniform prior |
| Multi-step lookahead | Higher complexity; only justified if the one-step baseline is shown insufficient |

Single-fault first: \(H_0\) contains one no-fault hypothesis plus one hypothesis
per declared fault. Multi-fault combinations are an optional later expansion
because \(|H|\) grows combinatorially; if enabled, they must be an explicit
finite subset, not “all combinations.”

Continuous time/data are used only through declared finite conservative
partitions. Direct enumeration applies only when \(O\) is a finite computable
partition.

### Stop / return semantics (candidate)

| Condition | Return | Forbidden shortcut |
|---|---|---|
| Budget exhausted | Current \(H_k\) and unnamed pending obligations | Invent a unique location |
| \(|H_{k+1}|=1\) | Locate only inside the declared hypothesis domain and valid observation conditions | Automatic protocol PASS |
| Several remaining, no distinguishing executable test | Indistinguishable set | Repeat the same test forever |
| \(H_{k+1}=\emptyset\) | Model / hypothesis / observation inconsistency; keep diagnostic data | Pick the “nearest” fault |
| Instrument `ERROR` | Invalid tool/correlation/record; distinct from IUT `FAIL` | Use ERROR to exclude faults |
| Named 645-blocked item | Explicit inconclusive | Silent removal from the coverage denominator |

### Complexity accounting (candidate)

Count: \(|H_k|\), \(|T(q_k)|\), number of observation classes per test, and
oracle/constraint evaluation as **not** \(O(1)\) unless a later bound says so.
A one-step minimax pass is \(O(|T| \cdot |H| \cdot |O_{\mathrm{class}}|)\) plus
oracle cost. Do not hide oracle or trace-correlation cost.

### Three walk-throughs (illustrative, not 615A constants)

1. **Timing with error (teaching numbers only; not CRS values).** Allowed
   interval \(I=[0,10]\,\mathrm{ms}\), error bound \(\varepsilon=1\,\mathrm{ms}\).
   Measured 8 ms → \(J=[7,9]\subseteq I\) → time constraint PASS. Measured 10 ms
   → \(J=[9,11]\) overlaps \(I\) → INCONCLUSIVE. Measured 12 ms → \(J=[11,13]\)
   disjoint from \(I\) → FAIL. Missing/mismatched records are `ERROR`, not a
   simple timeout FAIL.
2. **Feedback changes the next test.** \(H=\{h_1,h_2,h_3,h_4\}\), equal cost.
   \(t_a\) splits \(\{h_1,h_2\}\) vs \(\{h_3,h_4\}\) (worst remaining 2);
   \(t_b\) splits \(\{h_1\}\) vs \(\{h_2,h_3,h_4\}\) (worst remaining 3). Choose
   \(t_a\). After observing the first class, recompute from the new \(q_{k+1}\)
   to separate \(h_1/h_2\); do not replay the first-round menu. If no separator
   remains, return \(\{h_1,h_2\}\).
3. **Budget exhaustion.** If the distinguishing test for \(\{h_1,h_2\}\) costs
   more than remaining budget, stop and return that set. Do not borrow budget
   from another unit.

### Confirmation checklist (design direction only)

Please confirm or replace:

1. Minimax remaining-set selection as the default, with the listed alternatives
   as comparison arms only.
2. Single-fault \(H_0\) plus optional explicit finite multi-fault subset.
3. Set-valued compatibility; no default probability.
4. Stop/return table above.
5. SysML 1.6 notation-based views (DD-030) and M2 bound-input isolation (DD-030).

**Scope:** Candidate algorithm and experimental comparison logic; not an
implementation and not a proved theorem.

**Status:** Candidate under CR-2026-012, awaiting concentrated design-direction
confirmation. Not independent mathematical approval.

---

## DD-030 — Expand protocol CRS, split tool requirements, isolate the bound M2 input

**Decision (candidate schema/organization; protocol facts still come from
sources):**

1. **Protocol CRS vs tool requirements.** This increment expands only protocol
   CRS. Tool-module software requirements, APIs, configuration bindings and
   TP/VC oracles belong to the successor development-ready PR. Protocol rows
   must still carry actor / condition / action / objects / receiver / polarity
   and bilingual paraphrase. Source-explicit field, status, timing and error
   semantics cannot be omitted as “implementation detail.”
2. **Operations in scope.** INFORMATION, UPLOAD, Media Defined DOWNLOAD,
   Operator Defined DOWNLOAD, FIND, and source-stated interrupt/reject/
   exception/retry. Historical `DEFERRED-FIND-M9` and `DEFERRED-DOWNLOAD-M9`
   rows are re-opened **item by item**; they are not batch-renamed to applicable.
3. **Configuration predicates.** Ordinary Ethernet, Compliant Network, Profiled
   Network and AFDX are distinct dimensions. The current Compliant instance
   identity is unchanged. Other variants may be conditional CRS. Arbitrary
   Cartesian products are not assumed legal.
4. **ARINC 645.** Unique algorithm/constant/naming details stay
   `BLOCKED-SOURCE-645`. Explicit 615A/665 integrity *obligations* remain.
   Surrogates test call/state propagation only and cannot earn algorithm
   conformance.
5. **Old M2 isolation.** Merged model `M2-CANDIDATE-6` stays bound to its
   recorded input blob OIDs. Expanding CRS must not claim that model covers new
   services. New obligations receive disposition `MODEL-REFINEMENT-PENDING` (or
   an equivalent versioned code) with a real rationale, not a pointer to a
   generic variable. Validators must resolve: historical model ↔ bound input
   version; successor CRS ↔ its own schema/version. Do not delete coverage
   checks to pass CI.
6. **SysML.** Candidate notation is SysML 1.6. No modelling tool is purchased.
   Editable sources live under `docs/research/publication/models/`; reader
   exports under `artifacts/publications/cltav/figures/`. If only PlantUML or
   similar text rendering is available, figures are labelled “SysML 1.6
   notation-based views; executable/metamodel conformance is not claimed.”
   Ordinary flowcharts are not a complete SysML model. `satisfy`/`verify` in
   diagrams are model relations, not executed verification.

Minimum view set (IDs assigned when figures are added): context/use case;
requirement layers (method / protocol / tool); BDD of Test, Observation,
Analysis, Diagnosis, Selection, Evidence; IBD of ports; closed-loop activity;
one diagnostic sequence; verification-session state distinct from protocol
state; timing/cost parametric constraints; plus one source→CRS→constraint/
test→tool-function→evidence example.

**Scope:** CRS expansion policy, variant predicates, 645 limitation, M2 input
isolation, SysML organization.

**Status:** Candidate under CR-2026-012. Independent RG0/RG1 still required for
source interpretation. Schema details may be minimized if alternatives, reasons
and negative examples are recorded.

# 中文版

本决策日志只追加、不重写历史。有效决策包括：以可审计验证点/用例为主单位；把“置信”解释为有条件的认识性证据；用有限故障域和变异评价检测能力；分离基础与扩展 VCS；把双角色模拟器定位为仪器而非学术创新；以测试和分析为互补主路径；以评审和检查作为横向门禁；停用 DTMC 边概率、最弱链路、路径乘积和默认 HMM 定位；所有主张由证据门晋级。

## DD-001——以验证点为主要单位

以可审计的需求义务、TP 和 VC 为主要推理与追踪单位。

## DD-002——分层定量模型（历史）

保留原 RR-2026-001 的历史陈述，但其 DTMC/HMM 核心已由 DD-010 取代。

## DD-003——贝叶斯/证据置信语言

“置信”仅表示满足校准、先验和模型条件时的认识性证据。

## DD-004——用变异分析评价充分性

在声明的有限故障域内，以有效、非等价变异体评价检测能力。

## DD-005——基础与扩展 VCS 分离

扩展实验不得修改基础用例的规范性 oracle。

## DD-006——双角色模拟器是仪器

模拟器用于受控刺激、观测和故障注入，不被单独宣称为学术创新。

## DD-007——冻结 RR-2026-001 v4.1

保留历史决定；若 v4.2 获批，其当前基线标识由 DD-012 取代。

## DD-008——测试与分析互补

测试产生受控观察，分析评价证据范围和强度，二者均不可单独完成方法论。

## DD-009——评审和检查是横向门禁

Review 与 Inspection 控制静态产物和主张，而非被强行并入动态 Test。

## DD-010——停用 DTMC/HMM 基线机制

协议保持 EFSM/IOLTS；概率推断和诊断使用独立定义并验证的模型。

## DD-011——主张由门禁获得

所有研究和工程措辞由主张—证据矩阵及相应门禁晋级。

## DD-012——加入确定性时序符合性而不恢复随机协议语义

DD-012 已由 `GR-PR6-RB-2026-001-v4.2` 批准，并已在 PR #6 合并时生效：v4.2 取代 v4.1 作为当前方法论基线标识，同时保持 DD-010 有效；加入确定性时序语义和误差感知 oracle，但不把协议图变成随机过程。v4.1 证据不得自动改标为 v4.2 证据。

### 中文

本节是英文 DD-012 内嵌中文说明的对应结构；独立评审结论已记录，但合并前不得提前改为 Active。

## DD-013——通过受控可追踪契约分离产品领域

把方法论研究/出版、工程实现和验证教程视为不同产品领域，以治理和受控需求作为共享契约层。权威报告从 `docs/study/` 迁移至 `docs/methodology/`；通用教程和 ARINC 615A 教程使用不同入口；跨领域依赖必须标明上游产物版本和适用门禁记录。出版和教程保持下游地位；证据反馈只有通过 CR/DD 与评审控制才能修改上游契约。

完全独立既不可能也无益：研究需要工程证据，工程实现方法语义，教程解释二者。明确依赖方向与追踪记录能够在不破坏综合验证闭环的情况下减少偶然耦合。本决定已由 `GR-PR6-RB-2026-001-v4.2` 批准，并已在 PR #6 合并时与 DD-012 同时生效。产品域通过受控契约耦合；教程不具规范性，出版不得反向修改方法论，改变上游契约的反馈必须通过 CR/DD 和评审控制进入。该决定建立的路径已由生效的 DD-014/CR-2026-003 经 PR #7 重组，但依赖语义不变。

## DD-014——分离读者发布面与开发者控制平面

采用 CR-2026-003 的信息架构和报告契约：根目录只保留面向读者的 README；工具按约定发现的
机器配置继续位于根目录；全部读者交付物置于 `artifacts/`；项目、研究、工程和教程各有一个
控制入口；证据与治理记录继续作为独立可追踪产物保存；每次读者更新以一份自包含报告发布，
并由根 README 直接链接。

读者需要连贯的发布叙述，开发者则需要原子记录、所有权和审计历史。分离两个界面可以减少
导航噪声，同时不压平保证论证或削弱追踪。本决定已由 `GR-PR7-RB-2026-001-v4.2.1`
批准，并已随 PR #7 合并生效。独立评审已确认迁移完整、链接有效、中英文对等、校验器覆盖充分，且
RR-2026-001 v4.2 的数学与方法论语义未改变。

## DD-015——以 ARINC 615A-3 作为唯一活动协议来源

**决定：** 采纳 ARINC 615A-3 为唯一活动 615A 协议权威，665-5 为有边界的数据格式
参考，645 为开放依赖；撤销全部活动 615A-4 依赖或目标，同时把登记的冻结历史保持为
`HISTORICAL-SUPERSEDED`。线协议值 `A4` 不是标准版次。

**理由：** 来源身份必须先于 CRS。混淆线版本、标准版次、后续数据格式或开放的完整性
算法会产生不可追踪需求和虚假能力主张。

**范围：** 仅控制来源角色与迁移；不创建标准正文、CRS、适用性决定、实现或符合性结论。

**状态：** 处置为 `ADOPT`，正式激活由 CR-2026-006 控制；批准与普通合并证据由外部核验。

## DD-016——采用轻量可观测 timed EFSM 与有界 Test-Analysis

**决定：** 保留单一轻量可观测 timed EFSM 和互补的 Test-Analysis。首轮 Analysis 仅承担
义务追踪、状态/迁移/时序覆盖、稳健时序/误差预算以及有限故障域 mutation/held-out
adequacy。延期 DTMC 协议语义、HMM/ML 诊断和 Bayesian calibration。FMEA 只能为故障
排序，不能判定符合性；TTCN-3 不是依赖或选定平台。

**理由：** 这是在 CRS、Configuration 和执行数据存在前兼顾可审计工程和可发表分析、同时
避免不可识别或不可校准模型的最小路线。

**范围：** 仅为技术方向；本决定不实现或选择 EFSM、oracle、用例、分析模型或执行平台。

**状态：** 处置为 `ADOPT`；正式激活使用 CR-2026-006 门，且不声称批准或合并已经发生。

## DD-017——采用可注入分层、受门禁的开源复用和 M0～M9 串行交付

**决定：** 协议文件、注入式 IO/时钟/trace、TFTP、615A 适配、操作、验证和证据层可独立
替换。L1 参考复用需身份/许可证记录；L2 未来黑盒比较需固定身份/许可证；L3 源码/常量/
向量在独立许可证、洁净度和架构适配评审前禁止。M0～M9 串行交付，下一步仅为 M1 CRS/
适用性，不并行开启阶段 PR。

**理由：** 注入边界支持确定性时序和证据，方向性分层控制变化；受门禁复用避免许可证和
来源权威污染，串行门防止实现越过需求。

**范围：** 仅为目标架构与交付政策。本变更不登记任何具名开源实现用于复用，也不复制
第三方材料。

**状态：** 处置为 `ADOPT`；正式激活使用 CR-2026-006 门，批准与普通合并经外部核验前禁止 M1。

## DD-018——采用单一 M1 权威数据包及 RG0/RG1 联合激活

**决定：** 机器可读 M1 数据包是唯一权威，Markdown 评审视图是生成物。对 615A-3 做完整范围审计，只审计由 615A-3／所选服务触发的 665-5 依赖；来源模态与符合性效果分离。RG0 与 RG1 只在同一不变 Head 上联合关闭。

**理由：** 单一权威防止状态漂移，完整覆盖避免关键词选择偏差，有边界依赖防止后续版次静默改写活动协议。本地 Git 历史或自动化不能制造外部 GitHub 批准。

**范围：** 仅限 M1 静态需求、适用性、依赖和评审；不创建模型、Configuration、执行证据、baseline、tag 或符合性主张。

**状态：** 在 CR-2026-007 下候选处置为 `ADOPT`；RG0/RG1 与正式激活仍等待外部独立评审和普通合并。

## DD-019——将直接 615A→665 需求边延期到 M2

**决定：** M1 仅在有界 Profile 范围准入 ARINC 665-5。直接需求精化、生成方约束和消费方容忍边继续禁止，直至 M2 完成 attachment 锚定协调。

**理由：** 共享词汇或数据对象名称不能证明蕴含关系；一条边必须由同时绑定两个来源命题的明确证据支持。

**状态：** 在 CR-2026-007 下为候选，不授权进入 M2。

## DD-020——采用生成投影并删除同义冗余语义字段

**决定：** 将确定性双语模板输出重命名为 `generatedSemanticProjectionEn/Zh`，仅作为漂移锚；删除需求级 `roles`、`operations`、`category` 和 `obligations` 冗余字段，显示值由 `semantic` 导出。

**理由：** 生成模板不是独立评审证据；被强制等于单个语义元素的字段不携带额外信息。

**状态：** 在 CR-2026-007 下为候选，等待完整 RG0/RG1 复审。

## DD-021——附件 3 与附录 E 从"信息性"重分类为显式延期

**决定：** ARINC 615A-3 附件 3（FIND 协议详解）与附录 E（AFDX 数据加载部署）在 Profile 层已延期或依赖尚未绑定的情况下，不得使用 `NON-PROTOCOL-PRODUCT-OR-INFORMATIVE` 归口，而应显式记为 `DEFERRED-FUTURE-SCOPE`，理由码分别为 `DEFERRED-FIND-M9` 与 `DEFERRED-AFDX-DEPLOYMENT-M2-INFRASTRUCTURE-BINDING`。

**理由：** 附件 3 提供 FIND 的规范性定义，而 §5.3.3 主体已延期 FIND；"信息性"归口与延期结论冲突。附录 E 规定 AFDX 部署下的规范性约束，其真正阻塞在 ARINC 664 P7（未获取）与 P2（现已绑定），应通过明确的 M2 基础设施绑定条件封闭。

**范围：** 仅重分类覆盖账本 leaf；不新增或删除 CRS 需求，也不移动 currentStop。

**状态：** 在 CR-2026-007 下为候选，等待外部独立复审。

## DD-022——公共 IETF RFC 的受控处理

**决定：** 公共 IETF RFC（768、791、1123、1350、1785、2347、2348、2349）不进入 `configs/research/controlled_sources.json` 的 `sources[]`（其为专有材料专用），而是留在 `openDependencies[]`，并附上 `publicRetrieval` 子对象记录规范 URL、检索日期、字节数与 SHA-256；文件本体保存在 `local-references/rfc/`（`.gitignore` 覆盖）且不入库。

**理由：** 现有 baseline 检查要求 `sources[]` 项目具备"专有本地非仓储副本"处置策略与独立采购记录匹配，公共文本不符合该模型。将 RFC 保留在 `openDependencies` 保持"能力仍未建立"的正确语义，同时通过 `publicRetrieval` 记录我们意图使用的具体版本身份。

**范围：** 仅登记 RFC 身份与检索元数据；不将其提升为需求级证据，也不解除 `RFC-*` 对应能力的阻塞状态。

**状态：** 在 CR-2026-007 下为候选，等待外部独立复审。

## DD-023——接收网络来源并选择 Compliant 范围，不制造适用性闭合

在 CR-2026-007 下登记 P3-1 与 P7 初版身份，保留版次、网络适用性与独立批准义务。
所获版次为候选输入，不声称是最新标准。网络检查登记区分上下文检查区域与原子需求覆盖。
用户选择 Compliant Network，不采用 P3 偏差；RFC 1122 单独登记为已取得公共来源。
IPv4/UDP 主机服务仍是未建立的基础设施前提，不代表完整 RFC 清单或实现符合性。
M2 须规划其验证，之后才可批准执行 Configuration；独立评审须接受历史版次与此范围边界。
AFDX、AID 未来补充版引用与寻址选择仍延期。来源接收不建立实现能力。
继续保留 DD-019/DD-020，在进一步规范晋级前评审剩余适用性。
真实批准和合并事实由不变 Head 上的外部记录与普通合并承载，不新增专门 post-merge 同步提交。

## DD-024——将 M2 绑定到带受限时钟的可观测 timed EFSM

M2 为 UPLOAD 与 INFORMATION 交付一台机器 M = (S, s0, V, C, P, E, T, Inv)，
数据加载器与目标硬件是同一状态的观测投影。时序使用受限 AST、显式时钟、时钟
使能超时和有来源的误差预算类别。附件 4 方程保留重试与网络传输项。未解析边界
保持 NOT-CHECKED。数据包是模型权威；M1 仍为不可变 CRS 输入。不授权 codec、
可执行引擎、TP/VC 或 Project Configuration。

**范围：** CR-2026-008 下的候选模型与义务追踪。

**状态：** 在 CR-2026-008 下为候选，等待外部独立复审。

## DD-025——将 M1 输入接受与技术行动关闭分开

在 M2 `inputAcceptance` 中记录所有者接受的 COMMENTED 签署、普通两父合并、树和
main CI。不改写已合并 M1 字节，不伪造 GitHub APPROVED Review，不声称具名独立
评审者。CR-2026-007 结案将残余行动转交 CR-2026-008；转交不是技术关闭。
历史版次接受仍为有条件输入，直至独立 RG0 另有决定。

**范围：** 合并后 M1 事实的控制平面记录；不是纯落账 PR。

**状态：** 在 CR-2026-008 下为候选，等待外部独立复审。

## DD-026——将基础设施前提与已建立能力分开

两端均可定位时，615A→665 与 TFTP 选项边可作为候选精化。CRS-M1-00034 是指向
RFC 2348 §2 的块大小候选；冲突的 6.4.4 LUI/LUR 文件身份不发出活动 665 边。
IPv4/UDP 与 RFC 1122/1123 仍为基础设施前提，其验证计划用于 Project
Configuration。ARINC 645 继续阻塞完整性成功。AFDX、FIND、媒体集服务和 P3
裁剪偏差保持延期或排除。本候选不把任何行为能力改为 ESTABLISHED。

**范围：** M2 模型使用的前提、精化与能力守卫。

**状态：** 在 CR-2026-008 下为候选，等待外部独立复审。

## DD-027——用后继 M1 增量纠正文件身份，不改写冻结树

6.4.4 的 LUI/LUR 文件身份冲突以及 §6.3.2 的 LUR WRQ 参与者不一致仍为
OPEN-M1-CORRECTION。该停线是正确行为，不是关闭。在这些输入仍冲突时，当前 M2
候选不得请求最终 RG0/RG1/RG2 APPROVE。用户授权后，后继 M1 数据包可仅在新的
普通提交与新 blob 中纠正这些身份。历史合并
`9bf18124d405b656815bc9eb524ae29bb4f04f56` 及其冻结字节作为保留记录保持不变。
后继 `inputAcceptance` 是新身份，不得把原合并批准移植到新 blob。CR-2026-009
是一份授权请求，含两项待授权事项（6.4.4 文件身份与 CRS-M1-00365 WRQ 参与者），
可一并或分开授权；获授权前均不执行。NET-ISSUE-EDITION 仍是独立的 RG0 决定；OPEN 文字不是
版次接受。CR-2026-009 记录该授权请求。

**范围：** 输入纠正授权；不是改写 M1，也不是 M2 最终批准。

**状态：** 在 CR-2026-008／CR-2026-009／CR-2026-011 下为候选。所有者授权已于
2026-09-10 到位；后继增量由 CR-2026-011 执行；仍须独立 RG1。

### 2026-09-10 T1 执行

CR-2026-011 执行事项 A、B 以及所有者授权的 6.4.5 LUR→LUS 伴随。后继
`inputAcceptance` 是新身份，不移植冻结合并批准。`reviewControl.blocksFinalApproval`
保持为真。

### 2026-09-10 RR-M2-2026-004 之后的 LUR 写端点

独立评审撤回“receiver 保持 DLA”，因其把应用层 DLA 与网络可见 TFTP WRQ 混为一谈。
同一 CR-2026-009 事项 B 类别现记录 DATA-LOADER→TARGET-HARDWARE WRQ、
TARGET-HARDWARE→DATA-LOADER ACK、DATA-LOADER→TARGET-HARDWARE DATA。这仍是有界
M2 基线，不是开发就绪 CRS。

## DD-028——采用 CL-TAV 作为后继研究方法与两 PR 顺序

方法正式名称为闭环测试—分析协同验证方法 / Closed-Loop Test–Analysis
Verification，简称 CL-TAV。核心是测试→观测→约束判定／诊断→后续测试选择。
RR-2026-001 v4.2 的冻结身份保留；允许在旧→新处置清单与独立数学审查下修订。
本增量做方法／大纲／扩大协议 CRS；后继 PR 才做开发就绪。不把 Test 与 Analysis
的组合宣称为首次发明。原 RQ1–RQ6 按 DD-028 英文表映射，不因删正文而视为完成。

**范围：** 方法命名、RQ 映射、两 PR 顺序、历史方法身份。

**状态：** 在 CR-2026-012 下为候选。名称与顺序取自执行工作单的已确定项；仍须独立评审。

## DD-029——候选 CL-TAV 算法、观测抽象与停止规则

**状态为候选设计方向，不是“用户已决定”。** 来源审计与不依赖这些选择的大纲工作可以继续。在用户或指定方法评审者确认方向前，不得把算法相关断言写硬。

### 采用的基线（候选）

采用有限假设集、集合式相容与有界预算。不要求概率先验。除非后继 CR 证明 HMM／DTMC／Bayesian 能单独解决一个不同问题，否则不引入这些机制。

对象：\(H_0\) 为声明的初始假设集（含无故障或明确的无“无故障”规则）；\(q_k\) 为当前会话／面向 IUT 的状态与已执行历史，选择测试不得假设每轮自动复位；\(H_k \subseteq H_0\) 为第 \(k\) 轮后仍相容的假设；\(T(q_k)\) 为当前可执行测试，每个测试 \(\mathrm{cost}(t)>0\) 且预算单位单一；\(O(h,t,q_k)\) 为声明模型允许的抽象观测，非确定时不同 \(h\) 的集合可重叠；\(I_{z_k}\) 为测量对应的可行观测集合，仪器／关联失败返回 `ERROR`，不用它排除假设。

候选更新（相容，不是概率）：

\[
H_{k+1} = \{ h \in H_k \mid O(h,t_k,q_k) \cap I_{z_k} \neq \emptyset \}.
\]

必须同时更新状态、历史、已执行测试、观测类别和关联键。仅有该集合公式不算完整算法。

### 选择规则（候选）与替代方案

对每个可执行且剩余预算 \(\ge \mathrm{cost}(t)\) 的测试，按可见观测类计算最坏剩余候选数：

\[
s(t) = \max_{o \in \mathrm{Obs}(t,q_k)} \bigl|\{ h \in H_k \mid O(h,t,q_k) \cap o \neq \emptyset \}\bigr|.
\]

选择 \(\arg\min_t s(t)\)。并列时先更小 \(\mathrm{cost}(t)\)，再稳定测试 ID。这是可解释的极小极大基线，**不**声称最优。

默认不采用（可作比较臂，无新 DD 不得替换）：

| 替代 | 不作默认的原因 |
|---|---|
| Shannon 信息增益 | 需要概率分布，且通常要求互斥分区 |
| 单位成本期望剩余集缩减 | 仍需要分布或未声明的均匀先验 |
| 多步前瞻 | 复杂度更高；仅在一步基线被证明不足时才有理由 |

单故障优先：\(H_0\) 含一个无故障假设加上每个已声明故障一个假设。多故障组合只作为可选的显式有限子集，因为 \(|H|\) 组合爆炸；不得写成“所有组合”。

连续时间／数据只通过已声明的有限保守分区使用。仅当 \(O\) 为有限可计算分区时直接枚举。

### 停止／返回语义（候选）

| 条件 | 返回 | 禁止捷径 |
|---|---|---|
| 预算耗尽 | 当前 \(H_k\) 与未决义务 | 伪造唯一定位 |
| \(|H_{k+1}|=1\) | 仅在声明假设域与有效观测条件下定位 | 自动协议 PASS |
| 多个剩余且无区分性可执行测试 | 不可区分集合 | 无限重复同一测试 |
| \(H_{k+1}=\emptyset\) | 模型／假设／观测不一致；保留诊断数据 | 硬选“最接近”故障 |
| 仪器 `ERROR` | 工具／关联／记录无效；与 IUT `FAIL` 分开 | 用 ERROR 排除故障 |
| 具名 645 阻塞项 | 显式未决 | 从覆盖分母静默删除 |

### 复杂度记账（候选）

计入 \(|H_k|\)、\(|T(q_k)|\)、每测试观测类数，以及 oracle／约束评价（除非后继给出界限，否则**不是** \(O(1)\)）。一步极小极大为 \(O(|T| \cdot |H| \cdot |O_{\mathrm{class}}|)\) 加上 oracle 代价。不得隐藏 oracle 或 trace 关联代价。

### 三项走查（示例，不是 615A 常数）

1. **带误差的时序（仅教学数值，不得写入 CRS）。** 允许区间 \(I=[0,10]\,\mathrm{ms}\)，误差界 \(\varepsilon=1\,\mathrm{ms}\)。测得 8 ms → \(J=[7,9]\subseteq I\) → 时间约束 PASS。测得 10 ms → \(J=[9,11]\) 与 \(I\) 重叠 → INCONCLUSIVE。测得 12 ms → \(J=[11,13]\) 与 \(I\) 不相交 → FAIL。缺记录或错配是 `ERROR`，不是简单超时 FAIL。
2. **反馈改变下一测试。** \(H=\{h_1,h_2,h_3,h_4\}\)，成本相同。\(t_a\) 划分为 \(\{h_1,h_2\}\) 与 \(\{h_3,h_4\}\)（最坏剩余 2）；\(t_b\) 划分为 \(\{h_1\}\) 与 \(\{h_2,h_3,h_4\}\)（最坏剩余 3）。选择 \(t_a\)。观测到第一类后，从新的 \(q_{k+1}\) 再计算以区分 \(h_1/h_2\)；不要重放第一轮菜单。若无区分测试，返回 \(\{h_1,h_2\}\)。
3. **预算耗尽。** 若区分 \(\{h_1,h_2\}\) 的测试成本超过剩余预算，停止并返回该集合。不得从另一单位借预算。

### 确认清单（仅设计方向）

请确认或替换：

1. 以最坏剩余候选数最小化为默认选择，所列替代仅作比较臂。
2. 单故障 \(H_0\)，外加可选的显式有限多故障子集。
3. 集合式相容；无默认概率。
4. 上表停止／返回规则。
5. SysML 1.6 记法视图与 M2 绑定输入隔离（DD-030）。

**范围：** 候选算法与实验比较逻辑；不是实现，也不是已证明定理。

**状态：** 在 CR-2026-012 下为候选，等待集中设计方向确认。不是独立数学批准。

## DD-030——扩大协议 CRS、分离工具需求、隔离已绑定 M2 输入

本增量只扩大协议 CRS，不写工具模块软件需求。INFORMATION／UPLOAD／两种 DOWNLOAD／
FIND 及来源已规定的中断／拒绝／异常／重试逐项重审，禁止批量改状态词。网络模式与
部署类型分维；已选 Compliant 实例身份不变。645 只阻塞独有算法细节。旧模型
`M2-CANDIDATE-6` 仍绑定其输入 blob；新义务标为模型细化待完成，不得指向泛化变量
以通过覆盖检查。SysML 1.6 为候选记法；无建模器时可用文本渲染，但须标明非可执行／
非完整元模型符合性。

**范围：** CRS 扩大政策、变体谓词、645 局限、M2 输入隔离、SysML 组织。

**状态：** 在 CR-2026-012 下为候选。来源解释仍须独立 RG0／RG1。
