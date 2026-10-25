# Bounded CL-TAV session runtime implementation

| Control | Value |
|---|---|
| Authorization | CR-2026-021 / DD-045 |
| Initial kernel checkpoint | PR #25 `87f9330306be411a3d2d580a356070072dcf903f` |
| Scope | Finite reference session coordination and in-process synthetic engineering validation |
| Status | Candidate implementation on a Draft PR; independent review required |

## Authority-to-runtime mapping

This table is traceability for code; it is not a second method, requirements or
experiment authority.  Every production invocation loads its declared Git-object input
directly and emits the commit/path/raw-byte SHA-256 identities it consumed.

| Controlled authority | Runtime projection | Production check | Boundary |
|---|---|---|---|
| `CLTAV-DEVELOPMENT-CONTRACTS` / `AR-FINITE` | `RuntimeAuthorityBinding`, `ModelContext`, finite path kernel | exact AR-FINITE interface IDs, record IDs and runtime parameters | Finite declared syntax and limits only; no general solver. |
| Interface registry: `SessionContext`, `HistoryHandle`, `IF-PRED-OBS` through `IF-RESOURCE-STOP` | `SessionContext`, `HistoryHandle`, later session adapters | exact eight-interface binding and ownership checks | Selection remains read-only; S3/S8/S9 responsibilities remain distinct. |
| CR-2026-016 / DD-038–040 | Source and evidence boundary | source identity and synthetic-only labels | Does not execute or promote first-slice requirements. |
| CR-2026-017 / DD-041 | Optional future offline-record adapter | separately tested adapter only | Does not turn capture intake into active execution. |
| CR-2026-019 / DD-043 and experiment design | Evaluator-only identity and evidence fields | no truth object accepted by algorithm input | No experiment admission, denominator result or scientific claim. |

## Named interface bridge

The runtime does not unpack positional tuples.  `RuntimeAuthorityBinding`
requires the exact registry output names and exposes the following one-to-one
aliases for all eight algorithm interfaces.  A missing, reordered or
conflicting name is a controlled binding error, not a default value.

| Interface | Named runtime fields |
|---|---|
| `IF-PRED-OBS` | `prediction.classes`, `prediction.gapDiagnostic` |
| `IF-SELECT-ADMIT` | `selection.kind`, `selection.actionId`, `selection.classes`, `selection.admission` |
| `IF-EXECUTE-RECORD` | `execution.visibleRecord`, `execution.effectClass`, `execution.executionAttemptId` |
| `IF-OBS-INTERPRET` | observation class, effect, summary confirmation/post-summary, ownership and measurement fields |
| `IF-PREP-RECOVER` | target/summary confirmation, error, eligibility, declared target, evidence and post-summary |
| `IF-HIST-UPDATE` | `history.after`, `history.after.hypotheses`, `stop.empty` |
| `IF-EQUIV` | explicit `established`, `notEstablished`, `unknown` tags |
| `IF-RESOURCE-STOP` | stop reason, final hypotheses and trace |

The current B/C-2A checkpoint implements normal TEST, named
prediction-gap/Prep, and UNKNOWN-session Recover routes through controlled
read-only admission decisions.  A
current TEST prediction gap withholds TEST minimax even when another TEST has
classes; eligible PREP is then evaluated by that same resource decision.
The GAP revokes the whole current TEST scoring set, including any unaffordable
TEST-derived A2 conclusion: with no eligible PREP, the exit remains the named
prediction gap; only an eligible but unaffordable PREP may produce A2 on that
fallback route.
The implemented B/C-2A branch closes `CONFIRMED-NOT-SENT`, unknown effect and
post-dispatch errors, Prep successor confirmation, eligible/unaffordable/no
eligible Recover (A4/A5), S7 retry caps, Recover-only S8 adoption and S9's
sole successor-summary commitment.  B/C-2B accepts only raw ordered
observation material from the synthetic environment.  `ReferenceSession`
freezes a typed `InterpretationContract`, which owns event encodings, pairing
policy, interval semantics, clock/unit/error identities and deadline
authority.  Raw material is bound to the issued execution/action/evidence
identity before it is retained; it cannot set its own policy, validity flags,
deadline or expected verdict.  The resulting `verdict` is limited to PASS,
FAIL, INCONCLUSIVE and ERROR; `scoreDisposition` is separate.  `answered` is
true exactly when `scoreDisposition == ANSWERED` and the verdict is PASS or
FAIL, so INCONCLUSIVE is never answered.  A METHOD-ONLY result is an
`ENGINEERING-WITNESS` with `answered=false`, even where its finite boundary
calculation yields PASS or FAIL.  Ownership or clock/error-basis ERROR follows
S7, while no assessment directly rewrites compatible history.  This does not
make the runtime a protocol stack, a physical clock calibration, a reviewed
protocol deadline engine, or an IUT claim.  Stop-Empty/equivalence and the
production evidence/CLI boundary remain explicit later B/C work.

## B/C-2 coverage status

`VERIFIED` means the named public-entry regression demonstrates the stated
sub-behaviour. `PARTIAL` means only the stated sub-behaviour is demonstrated;
`PENDING` means this checkpoint makes no implementation-completeness claim.
The fixed candidate Head, command and result belong in the subsequent limited
review or gate record. The paths below are durable test locators, not a
substitute for that evidence identity.

| ID | Status | Durable public-entry evidence or retained boundary |
|---|---|---|
| BC-01 | PARTIAL | `session::test_two_round_feedback_consumes_committed_summary_and_changes_selection`; `recovery::test_confirmed_summary_only_prep_propagates_declared_model_successor`; fresh/tampered checkpoint combinations remain later work. |
| BC-02 | PARTIAL | `session::test_two_round_feedback_consumes_committed_summary_and_changes_selection`; more visible-result/action combinations remain. |
| BC-03 | VERIFIED | `session::test_prediction_keeps_overlapping_classes_and_names_a_current_gap`; `session::test_unaffordable_best_test_and_no_information_test_do_not_displace_router`; bounded model only. |
| BC-04 | PARTIAL | `session::test_prediction_gap_revokes_an_unaffordable_test_score_before_a2`; full tie/cost/ID production matrix remains. |
| BC-05 | VERIFIED | `session::test_current_test_gap_is_named_and_eligible_prep_uses_the_same_admission_entry`; Recovery A4/A5 tests; ownership/T5 are outside this result. |
| BC-06 | PARTIAL | summary-only Prep q0→q1 and unconfirmed-Prep recovery regressions; full Recover continuation remains. |
| BC-07 | PARTIAL | confirmed, unconfirmed and target-only Recover public regressions; complete recovery-estimation boundary remains. |
| BC-08 | VERIFIED | confirmed-not-sent and CNS/UNKNOWN stale-delivery regressions; finite synthetic boundary. |
| BC-09 | PARTIAL | retry-cap, duplicate and post-dispatch error tests; all return contexts/final stop policy remain. |
| BC-10 | VERIFIED | shared-uncertainty and frozen-identity interpretation regressions; no physical calibration claim. |
| BC-11 | PARTIAL | full-history merge and resume/history regressions; complete same-round Stop-Empty policy remains. |
| BC-12 | VERIFIED | infeasible/multi-path and conservative-path retention regressions; finite bounds only. |
| BC-13 | PARTIAL | Raw material cannot inject policy/deadline/verdict. FIFO/MOST-RECENT, explicit cancellation/supersession, session-seeded ACTIVE ownership context for incremental deltas or exact cumulative reappearance, terminal request/response exclusion, and conflict quarantine are covered by `interpretation` and `session` regressions. A conflict may seal an uncontested new response but cannot reclassify an existing request identity; every emitted ledger state must remain replayable as a portable checkpoint. Bounded synthetic traces only. |
| BC-14 | PARTIAL | Frozen-contract interval containment/separation/boundary tests, plus empty physical domain and invalid clock/unit/error basis. Contract/material/clock/unit/uncertainty checks occur before deadline authority branching; no physical calibration claim. |
| BC-15 | PARTIAL | No-response uses cancellation/supersession, qualified horizon and deadline-authority regressions. METHOD-ONLY/UNRESOLVED never becomes a scored deadline. In pure reviewed semantics, closed upper bound uses `earliest > U` and open upper bound uses `earliest >= U`; this runtime rejects REVIEWED authority without a controlled registry. |
| BC-16 | PENDING | Empty/Singleton/645/Equivalent/Budget priority remains later B/C work. |
| BC-17 | PENDING | Equivalence proof and its bounded proof domain remain later B/C work. |
| BC-18 | PARTIAL | public execution-request isolation regression; complete action/state environment matrix remains. |
| BC-19 | VERIFIED | evaluator-truth exclusion and extra-truth-field rejection regressions; later evaluator work remains separate. |
| BC-20 | PARTIAL | S0 unset-status and committed/retry regressions; reset/Recover/attempt reconstruction matrix remains. |
| BC-21 | PARTIAL | public `ReferenceSession.step` malformed/identity regressions; independent CLI and reproducible-run boundary remains. |
| BC-22 | PENDING | Publication transaction and rollback are outside this in-process checkpoint. |
| BC-23 | PENDING | A non-editable repository-external wheel is outside this checkpoint. |
| BC-24 | PARTIAL | kernel/session offline regressions; complete no-network entry evidence remains. |

## Initial type boundary

`HistoryHandle.initial` represents S0 input.  It permits an empty member-status
map because a status need not exist before processing.  `HistoryHandle.committed`
represents an S9/processed result and requires one controlled status for every
surviving member.  Empty `H` is legal only as a processed Stop-Empty result.
`SessionContext` separates `KNOWN` plus a confirmed summary from session-level
`UNKNOWN`, which carries no usable current summary.  `CONSERVATIVE-UNKNOWN` is
instead a per-member `HistoryHandle` status; it preserves a candidate without
pretending that its session summary remains usable.

Each surviving `H` member carries a nonempty, bounded tuple of current frontier
provenance references, rather than a single flattened representative.  The
finite predictor propagates every path independently: an infeasible path in a
known member removes only that known path, while an unsupported or bounded
calculation retains its source path as conservative.  For an already
conservative member, an otherwise infeasible source remains a conservative
witness because its earlier unknown effect cannot establish an exclusion.
Conservative membership prevents an unproved
observation-based exclusion; it does not skip the admitted action transition.
Consequently, a feasible conservative path still carries its computed state,
clock/store update, path-length increment and terminal provenance into every
completed normal observation class, while the member is committed as
`CONSERVATIVE-UNKNOWN`.  It is never turned into a synthetic observable outcome.
If no completed visible class is
available, or the declared observation-class bound is exceeded, the result is a
named prediction gap and TEST selection is withheld.

## Execution and experiment-identity bridge

An engineering session always has a `runId`, `sessionId`, immutable
`snapshotId`, `actionId`, and one `executionAttemptId` for each dispatch.  The
optional `experimentAttemptId` is a foreign key to a later registered
experiment unit; it is absent in the present engineering fixtures.  Retrying
therefore creates a new execution identity without manufacturing a second
experimental sample.  A repeated or malformed returned execution identity is
rejected without S9 commitment; it never becomes a second history update.

`issuedToExecutor` means that S4's admitted immutable action was handed to the
execution interface.  It does **not** mean that a network packet was sent or
that an IUT was stimulated.  Each issued execution records its resource view
before/after, five declared detail-charge components
(`acquisition`, `computation`, `preparation`, `recovery`, `retry`) and a
separate four-component projection where preparation contains recovery exactly
once.  The session selector sees only the causal resource mode, remaining
resource and declared action cost; audit-only outcome/status fields never flow
back into selection.

`ROUNDS` consumes exactly one issued action, irrespective of the action's
declared monetary/computational cost.  `BUDGET` consumes that declared cost.
After S4, an execution-side exception, malformed execution result, invalid
result identity, or ordinary failure during returned-record validation,
interpretation, or S9 preparation does not restore the pre-issue state: it
retains the one charge and expected attempt identity, records a controlled S7
error, sets the session to `UNKNOWN`, marks every retained history member
`CONSERVATIVE-UNKNOWN`, and does not invoke S8/S9.  If
a returned result includes a typed successor environment, that actual successor
is retained even when its record is rejected.  A normal record which claims
summary confirmation but omits its post-summary is the same controlled
post-dispatch error.  `CONFIRMED-NOT-SENT` is distinct: because no action was
sent, it bypasses interpretation and Prep/Recover confirmation; it is charged
once, increments the controlled retry state, but preserves the prior history
and known summary.  Its evidence `resolution_code` records the controlled branch
selected during public-ledger replay; it is not yet an independently recomputed
proof that a retained rejected response caused that branch.  A retry reaches
`Stop-Error` only at its
declared cap; it does not lose the charged resource fact or silently become a
budget stop.

The public `SessionContext` therefore carries the resource remainder, retry
count/cap, confirmed Recover target/evidence, and error/unknown histories in
addition to the current summary.  S8 alone may restore `KNOWN` and write the
confirmed Recover target/evidence.  S9 is the sole post-effect committer of a
confirmed successor `currentSummary` (S0 seeds it and S7 may clear it): a
confirmed Prep summary may advance it even when the Prep target was not
confirmed, while a Recover needs both target and summary confirmation.  A
summary-only confirmation preserves `H`; only a valid observation class can
derive the new compatible-history intersection.  Target and summary
confirmation are independent typed return facts: target-only is a valid but
insufficient result, so an unconfirmed Prep summary or a Recover missing either
confirmation follows S7 rather than being misclassified as a malformed record.
A summary-only confirmed Prep (and a Recover that has satisfied its own S8/S9
confirmation condition) preserves `H` and performs no observation-class
intersection.  It nevertheless applies the admitted frozen finite transition to
every retained frontier path and commits the successor frontier provenance and
history version. An already `CONSERVATIVE-UNKNOWN` path is propagated but
remains `CONSERVATIVE-UNKNOWN`; only a path whose propagation is unsupported,
infeasible, or bound-limited retains its source path as conservative. No member
is silently removed or promoted. `postSummary` commits only `currentSummary`;
it is never decoded as a model control state.
For an S0 history, an absent optional member-status entry is not a positive
`KNOWN` assertion: a committed member is conservatively classified whenever
its retained history says so, any source or result frontier path says so, or
the propagation itself is unresolved.
The same aggregate is consumed by the next normal prediction and committed
observation class, so a known observation may still eliminate known-incompatible
members without excluding a retained conservative path.

Before any effect branch for an adapter-supplied record, the session validates
the complete visible-record domain and its field combinations:
identity/action/evidence references are nonblank strings (their accepted value
is not rewritten), and confirmation is Boolean.  A contract-bound `TEST`
record either carries one owned response with a visible observation, a
confirmed nonempty post-summary, an exact measurement tick and the frozen
uncertainty identity, or has the exclusive no-response shape:
`effectClass=NONE` with no response ID, measurement interval/tick, uncertainty
identity, observable or post-summary.  The latter is neither
`CONFIRMED-NOT-SENT` nor eligible for S9; declaring silence while an owned
response is present is ERROR.  A normal typed
`PREP`/`RECOVER` result instead carries its explicit target/summary/error
contract and may lawfully be summary-only, with no observation or measurement
tick; that contract selects S7, S8, or S9.  Non-normal records cannot
manufacture the fields that their branch forbids.  The narrowly synthesized
placeholder used for an adapter exception is not an adapter-supplied visible
record; it exists only to retain the issued identity and one charged S7
transition in the evidence ledger.  A rejected response is retained separately
from the expected issued record, so an incorrect returned attempt identity
cannot overwrite the request identity in the charged evidence.  Ordinary
adapter exceptions are controlled post-dispatch errors; this does not catch
process-interrupt exceptions.  A record which repeats an already processed
execution identity is an inbound stale delivery only if it first passes the
complete closed visible-record validation for the canonical record's original
action, and then matches that canonical record (already retained under its
frozen snapshot) recursively with exact runtime types and values. Exact comparison includes nested
`PrepRecoverResult`, Boolean confirmation fields, measurement scalar types,
effect/field combinations, and nonblank identity/evidence fields; Python `==`
is not an exact comparison.  The record is never validated under an action
selected for a later round.  A genuinely exact old TEST, PREP, RECOVER,
CONFIRMED-NOT-SENT, or UNKNOWN-EFFECT delivery remains idempotent even when the
currently admissible action has another kind.  A same-identity record that
fails either condition is a controlled ingress error.  Conversely, a
mismatched record returned *after* a newly issued action is a post-dispatch
error, not a duplicate: the actual typed successor and one charge are retained
through S7.

The finite model is JSON-detached at construction.  Its nested guard/update
AST is retained only in canonical frozen form and decoded afresh for each
kernel call.  Before S0 accepts it, the factory-issued model token verifies
the exact source JSON identity and a digest over every finite value consumed
by the coordinator (actions/costs, ASTs, frontiers, limits and uncertainty).
Likewise, the binding revalidates both raw Git snapshots and its reconstructed
finite projection; the development commit/path/blob triple must equal the
verified model context triple.  `ReferenceSession` then reconstructs private
model and binding projections, so a caller-held alias cannot rewrite accepted
authority before or after S0.  The declared append-only live provenance
publication store remains compatible with the supplied model; causal replay
uses an isolated copy before it validates retained evidence.  S3 selection,
admission, charging, evidence, causal replay and later propagation consume
only those private projections; they never reread a caller-held model or
binding as authority after S0.  This is a finite authority-closure rule, not
a general Python sandbox: it protects the declared model/actions/uncertainty/
provenance roots and the actual binding identity fields consumed by this
runtime.  Before selection, a resumed state must
belong to this run/session/model, retain its exact development/interface
authority binding and frozen S0 seed identity, and close its `H`, frontier
provenance, history version, evidence, and execution identities; validation
failure occurs before charge or dispatch.  A target session never re-signs a
foreign S0 state with its own binding. Before S4, validated top-level frontier
and event-identity maps are copied into private immutable proxies, so an
adapter holding a caller's backing dictionary cannot rewrite checked S0 facts
during dispatch. A fresh dispatch checkpoint recursively reconstructs the
finite retained public closure (including `OwnershipEvent`, retained evidence,
assessment and ownership-replay values) before the adapter runs; this prevents
an adapter that retained an old frozen nested value from using an object-level
mutation escape hatch to rewrite the lineage consumed after S4. The public state is replayed read-only from this
session's frozen S0 seed through each retained evidence item, so summary,
resource, snapshot/action, authority, history and frontier values must be the
causal terminal state of that ledger.  This replay neither calls the environment
nor issues another action or writes the shared provenance store.  A
complete checkpoint whose derived records are absent from a fresh target cache
remains resumable when that detached replay closes; its next propagation uses
the detached verified context rather than treating cache absence as a prediction
gap or rehydrating the target cache.  An already locally verified source-record
closure may instead be reused by its own session continuation.  A finite
multi-path S0 seed is permitted only when
declared at session construction, bound to this model/context, and then frozen;
hand-assembled replacement frontiers are not an alternate resume authority.
Each declared path must close over verified model provenance during replay,
rather than merely a target's mutable cache, but a bounded
bundle does not require its paths to have equal history lengths.

The synthetic environment likewise normalizes and detaches each nested outcome
value that it actually consumes.  Modifying a caller's source rational mapping
after construction cannot change a later visible measurement; a changed
environment requires an explicit new declaration and instance.  It carries at
most one explicit inbound delivery; a resumed session consumes that delivery
before it may admit or issue another action.

`U` is a bounded, typed uncertainty snapshot (`clockId`, `timeUnit=ticks`,
exact nonnegative maximum error and identity), not a label.  Prediction forms
per-hypothesis measurement windows with that snapshot; interpretation checks
the returned measurement tick and the same frozen uncertainty identity before
S9.  Separately, the B/C-2B assessor compares the raw interval with the
frozen contract: containment is PASS, separation is FAIL, boundary overlap is
INCONCLUSIVE, and invalid structure/clock/unit/error basis is ERROR.  This is
only a finite engineering witness, not calibrated clock accuracy or a protocol
timing verdict.

The existing label-class check admits an observable label when its tick lies in
at least one compatible per-hypothesis window.  It remains a deliberately
coarse, conservative label-class boundary.  The separate B/C-2B assessment is
contract-scoped and finite; neither component establishes per-hypothesis
protocol timing, physical clock calibration, reviewed deadline authority or a
conformance verdict.

For an owned response, the public `measurementTick` must also equal the exact
timestamp difference between that response and the request selected by the
controlled ownership policy; a merely interval-contained tick is not enough.
The session retains the complete typed ownership replay rather than only the
selected `responseId`: every response token is consumed and every non-active
request disposition is terminal.  Before each later ownership decision it
seeds the replay with the verified ledger's still-ACTIVE request identities,
global sequence/timestamp order, and request encoding.  Therefore a legal
incremental raw delta may omit terminal receipts and retained ACTIVE requests;
an exact cumulative reappearance is permitted only as confirmation, never as a
second obligation.  A changed field/kind, cross-role reuse, duplicate response
or duplicate terminal request takes S7.  A newly introduced request must be
ordered after the seeded context; otherwise the runtime reports insufficient
ownership context rather than guessing a local numbering epoch.  A replacement
request must actually terminate its named current ACTIVE predecessor before it
can satisfy a non-concurrent admission rule: a stale target is not an admission
token.  A complete CANCEL/SUPERSEDE transaction for another key is ignored only
when it names neither a retained ACTIVE controlled request nor any matching request in
the complete raw trace; a foreign-key event that targets a current *or future*
controlled request is still validated and rejected when incompatible.  Those
cross-round replay conflicts quarantine newly observed, uncontested response
facts but never change a retained request into a response (or vice versa), so
the state it emits remains self-validating and replayable in a fresh equivalent
coordinator. For no response, clock/error-basis validation occurs before a
cancellation/supersession can yield NOT-APPLICABLE; an invalid basis is ERROR,
not an administrative escape. A timely termination needs no elapsed-horizon
reading; when a legal incremental delta carries only the terminating event,
the verified retained ACTIVE trigger supplies the timestamp needed to assess
that termination. For an ACTIVE obligation, an unqualified observation horizon remains
PENDING-HORIZON even when no elapsed reading exists; only a qualified reviewed
deadline determination requires a nonnegative earliest admissible elapsed
horizon. A supplied invalid elapsed reading remains ERROR.

Pairing and reset are deliberately not inferred from a Recover action.  A
future experiment adapter must link paired units with `pairingId`, retain a
separate confirmed `resetId` and `resetEvidenceRef` for each arm, and keep that
evidence distinct from session-internal recovery.  The present synthetic
engineering runs have no registered experiment attempt or paired-reset claim.

The implementation must return controlled diagnostics at serialization and
session boundaries.  Python constructor `ValueError` is an internal input
boundary, not an IUT verdict; later production entry points map it to a named
tool error without publishing an invalid evidence package.

## Open work and evidence boundary

**Deferred B/C-3 audit obligation (A01).** Public replay currently preserves a
raw rejected response and its named `resolution_code`, but does not yet
recompute and verify their causal relation. B/C-3 evidence/CLI work owns the
closure: identity, target and visible-record errors must retain a present,
domain-valid raw response whose minimum cause agrees with the code; a pure tool
exception must not manufacture one. The closing gate is a public
evidence-transaction/CLI negative-mutation test for modified and deleted raw
responses. Until then this runtime claims controlled preservation, not exact
branch-cause proof.

The binding/type layer now executes bounded synthetic TEST/Prep/Recover actions
and, only for bound finite synthetic material, resolves ownership and performs
contract-scoped interval assessment.  It does not establish ownership of a
real protocol service, calibrated timing, reviewed deadline authority, IUT
behaviour or runtime integrity.  B/C-3 still owns durable
evidence-transaction/CLI causal closure.  The Researcher startup contract
review is recorded; independent review of the new fixed implementation head
remains pending.  All later runs remain `SYNTHETIC-ENGINEERING-VALIDATION`
until separately reviewed; they are not confirmation experiments or protocol
conformance cases.

# 中文版

# 有界 CL-TAV 会话运行时实现

| 控制项 | 取值 |
|---|---|
| 授权 | CR-2026-021／DD-045 |
| 初始内核检查点 | PR #25 `87f9330306be411a3d2d580a356070072dcf903f` |
| 范围 | 有限参考会话协调与进程内合成工程验证 |
| 状态 | Draft PR 上的候选实现；需要独立评审 |

## 权威到运行时映射

下表是代码追踪，而不是第二套方法、需求或实验权威。每次调用均直接加载其声明的 Git
对象输入，并输出实际消费的 commit／path／原始字节 SHA-256 身份。

| 受控权威 | 运行时投影 | 生产检查 | 边界 |
|---|---|---|---|
| `CLTAV-DEVELOPMENT-CONTRACTS`／`AR-FINITE` | `RuntimeAuthorityBinding`、`ModelContext`、有限路径内核 | 精确核验 AR-FINITE 接口 ID、记录 ID 和运行参数 | 仅声明语法和限额；不是通用求解器。 |
| 接口登记：`SessionContext`、`HistoryHandle`、`IF-PRED-OBS` 至 `IF-RESOURCE-STOP` | `SessionContext`、`HistoryHandle`、后续会话适配器 | 精确核验八个接口绑定和职责 | 选择保持只读；S3／S8／S9 职责保持分离。 |
| CR-2026-016／DD-038～040 | 来源和证据边界 | 来源身份和仅合成标签 | 不执行或晋级首轮需求。 |
| CR-2026-017／DD-041 | 未来可选的离线记录适配器 | 仅通过独立测试的适配器 | 不把捕获接入转为主动执行。 |
| CR-2026-019／DD-043 与实验设计 | 仅评价端的身份和证据字段 | 算法输入不得接受真值对象 | 不准入实验、不产出分母结果或科学主张。 |

## 具名接口桥接

运行时绝不解构位置元组。`RuntimeAuthorityBinding` 要求接口登记输出名称精确一致，并为全部
八个算法接口公开下列一对一别名。缺失、重排或冲突的名称是受控绑定错误，不得用默认值掩盖。

| 接口 | 具名运行时字段 |
|---|---|
| `IF-PRED-OBS` | `prediction.classes`、`prediction.gapDiagnostic` |
| `IF-SELECT-ADMIT` | `selection.kind`、`selection.actionId`、`selection.classes`、`selection.admission` |
| `IF-EXECUTE-RECORD` | `execution.visibleRecord`、`execution.effectClass`、`execution.executionAttemptId` |
| `IF-OBS-INTERPRET` | 观测类、效果、摘要确认／后继摘要、所有权和测量字段 |
| `IF-PREP-RECOVER` | 目标／摘要确认、错误、资格、声明目标、证据和后继摘要 |
| `IF-HIST-UPDATE` | `history.after`、`history.after.hypotheses`、`stop.empty` |
| `IF-EQUIV` | 显式 `established`、`notEstablished`、`unknown` 标签 |
| `IF-RESOURCE-STOP` | 停止理由、最终假设和 trace |

当前 B/C-2A 检查点通过受控的只读准入决定实现普通 TEST、具名 prediction-gap／Prep 路径以及
UNKNOWN 会话的 Recover 路径。
当前 TEST prediction gap 即使与另一具有 classes 的 TEST 同时存在，也会先抑制 TEST minimax；
随后由同一资源决定检查合格 Prep。已实现的 B/C-2A 分支覆盖
`CONFIRMED-NOT-SENT`、unknown effect 和派发后错误、Prep 后继确认、合格／付不起／无合格
Recover（A4/A5）、S7 retry cap、仅 Recover 的 S8 采纳以及 S9 对后继摘要的唯一提交。
B/C-2B 只从合成环境接收原始有序观测材料；`ReferenceSession` 冻结类型化
`InterpretationContract`，独占事件编码、配对策略、区间语义、时钟／单位／误差身份及 deadline
authority。原始材料须先绑定实际 execution/action/evidence 身份才可保留；不得自行声明 policy、
有效性标志、deadline 或预期判定。`verdict` 仅可为 PASS、FAIL、INCONCLUSIVE、ERROR；
`scoreDisposition` 独立保存。仅当 `scoreDisposition == ANSWERED` 且判定为 PASS 或 FAIL 时
`answered=true`；INCONCLUSIVE 永远不是 answered。METHOD-ONLY 即使算得边界 PASS/FAIL，仍为
`ENGINEERING-WITNESS` 且 `answered=false`。所有权或时钟／误差依据 ERROR 进入 S7；任何评估均
不得直接改写相容历史。这不使 runtime 成为协议栈、物理时钟校准、已审定的协议 deadline 引擎或
IUT 主张。Stop-Empty／等价及生产 evidence／CLI 边界仍是后续 B/C 工作。

GAP 会撤销整个当前 TEST 评分集，包括由不可负担 TEST 推导出的 A2：没有合格 Prep 时出口仍为
具名 prediction gap；只有合格但不可负担的 Prep 才能在该 fallback 路径产生 A2。

## B/C-2 覆盖状态

`VERIFIED` 表示具名公共入口回归已展示所述子行为；`PARTIAL` 表示仅展示所述子行为；
`PENDING` 表示本检查点不主张实现完整性。固定候选 Head、命令和结果必须由后续限定复审或
门禁记录绑定。下列路径是持久化测试定位，不替代该证据身份。

| ID | 状态 | 持久化公共入口证据或明确保留边界 |
|---|---|---|
| BC-01 | PARTIAL | 两轮反馈和仅摘要 Prep 的 q0→q1 回归；新鲜／篡改 checkpoint 的组合仍属后续工作。 |
| BC-02 | PARTIAL | 两轮反馈改变后继选择的回归；更多可见结果／动作组合仍待覆盖。 |
| BC-03 | VERIFIED | 重叠 classes、当前 GAP 和无信息 TEST 的回归；仅限有界模型。 |
| BC-04 | PARTIAL | GAP 撤销不可负担 TEST 评分的 A2 回归；完整 tie／cost／ID 生产矩阵仍待完成。 |
| BC-05 | VERIFIED | 当前 TEST GAP 与同一准入入口的合格 Prep 回归，以及 Recover A4/A5；ownership／T5 不在本结论内。 |
| BC-06 | PARTIAL | 仅摘要 Prep q0→q1 和未确认 Prep 的候选保留回归；完整 Recover 后继仍待完成。 |
| BC-07 | PARTIAL | 已确认、未确认和仅目标确认 Recover 的公共回归；完整恢复估计边界仍待完成。 |
| BC-08 | VERIFIED | CONFIRMED-NOT-SENT 及 CNS／UNKNOWN 过期投递回归；仅限有限合成边界。 |
| BC-09 | PARTIAL | retry-cap、重复投递和派发后错误回归；所有返回上下文／最终停止策略仍待完成。 |
| BC-10 | VERIFIED | 共享 uncertainty 与冻结 identity 解释回归；不主张物理时钟校准。 |
| BC-11 | PARTIAL | 完整 history 合并和 resume/history 回归；完整同轮 Stop-Empty 策略仍待完成。 |
| BC-12 | VERIFIED | 不可行／多路径及保守路径保留回归；仅限有限边界。 |
| BC-13 | PARTIAL | 原始材料不得注入 policy／deadline／判定。FIFO/MOST-RECENT、显式取消／替代、由 session 注入的 ACTIVE ownership 上下文（支持增量 delta 或精确的累计再次出现）、终态 request／response 排除及冲突隔离均由 `interpretation` 和 `session` 回归覆盖。冲突可封存无争议的新 response，但不得重分类既有 request 身份；每个发出的账本 state 都必须能作为可移植 checkpoint 重放。仅为有界 synthetic 事件迹。 |
| BC-14 | PARTIAL | 冻结合同的区间包含／分离／边界测试，以及空物理域、无效时钟／单位／误差依据。contract/material/clock/unit/uncertainty 必须先于 deadline authority 分支校验；不主张物理校准。 |
| BC-15 | PARTIAL | 无响应使用取消／替代、合格 horizon 和 deadline authority 回归。METHOD-ONLY／UNRESOLVED 永远不得成为可计分 deadline。纯 reviewed 语义中，闭上界使用 `earliest > U`，开上界使用 `earliest >= U`；本 runtime 没有受控 registry 时拒绝 REVIEWED authority。 |
| BC-16 | PENDING | Empty/Singleton/645/Equivalent/Budget 优先级属于后续 B/C 工作。 |
| BC-17 | PENDING | 等价证明及其有界证明域属于后续 B/C 工作。 |
| BC-18 | PARTIAL | 公共执行请求隔离回归；完整 action/state 环境矩阵仍待完成。 |
| BC-19 | VERIFIED | evaluator truth 排除和额外 truth 字段拒绝回归；后续评价端工作保持分离。 |
| BC-20 | PARTIAL | S0 未设置状态及 committed/retry 回归；reset／Recover／attempt 重建矩阵仍待完成。 |
| BC-21 | PARTIAL | 公共 `ReferenceSession.step` 畸形／身份回归；独立 CLI 和可复现运行边界仍待完成。 |
| BC-22 | PENDING | 发布事务和回滚不属于本进程内检查点。 |
| BC-23 | PENDING | 仓库外不可编辑 wheel 不属于本检查点。 |
| BC-24 | PARTIAL | kernel/session 离线回归；完整无网络入口证据仍待完成。 |

## 初始类型边界

`HistoryHandle.initial` 表示 S0 输入；因处理前成员状态可以尚未设置，允许空状态表。
`HistoryHandle.committed` 表示 S9／已处理结果，要求每个存活成员都有一个受控状态。空
`H` 只可作为已处理的 Stop-Empty 结果。`SessionContext` 将带确认摘要的 `KNOWN` 与不
携带可用当前摘要的会话级 `UNKNOWN` 分开。`CONSERVATIVE-UNKNOWN` 则是每个
`HistoryHandle` 成员的状态：它保留候选，绝不声称会话摘要仍可使用。

每个存活的 `H` 成员均携带非空且有界的当前 frontier provenance 引用元组，而不是一个被
扁平化的代表。有限预测器逐路径传播：已知成员中的不可行路径只会排除该已知路径；不支持或受限的计算
则将其源路径保留为保守路径。对已属保守的成员，即使某源路径表面不可行，也仍须保留为保守见证，因为
其先前未知效果不能证明该路径可被排除。保守成员只阻止未经证明的基于观测的排除，不得跳过已准入动作的
transition。因此，可行的保守路径仍将其计算得到的状态、clock/store 更新、path-length 递增和末端
provenance 带入每个已完成的普通观测类，同时成员以 `CONSERVATIVE-UNKNOWN` 提交；它绝不会被伪造为
一个可观测结果。若没有已完成的可见类，或
超过声明的观测类上限，则结果为具名 prediction gap，并抑制 TEST 选择。

实现必须在序列化和会话边界返回受控诊断。Python 构造器的 `ValueError` 是内部输入
边界，不是 IUT 判定；后续生产入口会将其映射为具名工具错误，且不发布无效证据包。

## 执行与实验身份桥接

工程会话始终具有 `runId`、`sessionId`、不可变 `snapshotId`、`actionId`，且每次派发
均有一个 `executionAttemptId`。可选的 `experimentAttemptId` 是后续已登记实验单位的外键；
当前工程 fixture 中该字段为空。因此，重试会产生新的执行身份，但不会伪造第二个实验样本。
重复或畸形的返回执行身份会在 S9 提交前被拒绝；它绝不会变成第二次历史更新。

`issuedToExecutor` 表示 S4 已将准入后的不可变动作交给执行接口；**不**表示网络报文已发送
或 IUT 已被刺激。每次 issued 执行记录其前后资源视图、五项声明的费用明细
（`acquisition`、`computation`、`preparation`、`recovery`、`retry`）及独立的四维投影；
投影中的 preparation 恰好折叠一次 recovery。会话选择器只读取因果资源模式、剩余资源和
声明动作成本；仅审计的 outcome/status 字段绝不回流到选择。

`ROUNDS` 每次 issued 恰好消耗一个动作，和动作声明的金钱／计算成本无关；`BUDGET` 才消耗该
声明成本。S4 之后发生执行侧异常、畸形执行返回、返回身份无效，或已返回记录的校验、解释、S9
提交准备出现普通错误时，均不得恢复到派发前状态：保留一次计费和期望的 attempt 身份，记录受控 S7
错误，将会话置为 `UNKNOWN`、把全部保留的 history 成员标为 `CONSERVATIVE-UNKNOWN`，且不得调用
S8／S9。若返回结果包含有类型的后继环境，即使其
记录被拒绝，也保留该实际后继环境。声称已确认摘要却缺少后继摘要的普通记录，同样属于派发后的
受控错误。`CONFIRMED-NOT-SENT` 与此不同：因为动作根本没有发送，它绕过解释和 Prep/Recover
确认；它恰好计费一次、增加受控 retry 状态，但保留此前 history 和已知摘要。其 evidence 的
`resolution_code` 记录公共账本重放中选取的受控分支；它尚不是对保留的 rejected response
确实导致该分支的独立重算证明。只有达到声明的 retry cap 才进入 `Stop-Error`；它不会丢失已计费
事实，也不会静默变成 budget stop。

因此，公开的 `SessionContext` 除当前摘要外还保存 resource remainder、retry count/cap、已确认
Recover 的 target/evidence 以及 error/unknown histories。只有 S8 可以恢复 `KNOWN` 并写入已确认的
Recover 目标／证据；S9 是确认后继 `currentSummary` 的唯一派发后提交者（S0 负责初始值，S7 可以清空它）。Prep 目标未确认但后继摘要已确认时，S9
仍可推进该摘要；Recover 必须同时确认目标和摘要。目标确认和摘要确认是彼此独立的有类型返回
事实：只确认目标是合法但不足的结果；未确认摘要的 Prep，或任一确认缺失的 Recover，均走 S7，
而不是被误分为畸形记录。仅摘要确认的 Prep（以及已满足其自身 S8/S9 确认条件的 Recover）保持
`H`，且不做观测类交集。它仍对每条保留 frontier 路径应用已准入、冻结的有限 transition，并提交
后继 frontier provenance 与 history version。已有 `CONSERVATIVE-UNKNOWN` 路径仍会传播但保持
`CONSERVATIVE-UNKNOWN`；只有传播不支持、不可行、受限的路径才以保守方式保留源路径。不得静默
删除或提升任何成员。`postSummary` 只提交 `currentSummary`，绝不得解码为模型控制状态。
对于 S0 history，缺少可选成员状态项不是对 `KNOWN` 的正向断言：若保留 history、任一源或结果
frontier 路径已表明保守，或传播本身未决，则提交后的成员必须按保守状态分类。
下一次普通预测和已提交的观测类也消费同一汇总：已知观测仍可排除已知且不相容的成员，但不得
排除保留的保守路径。

进入任何针对适配器返回记录的 effect 分支前，会话校验完整的可见记录域及其字段组合：身份／动作／
证据引用均为非空白字符串（接受后的值不被改写），确认字段为 Boolean。绑定合同的 `TEST` 记录要么
携带一个已归属响应的可见观测、已确认的非空后继摘要、精确 measurement tick 和冻结的 uncertainty
identity，要么采用唯一的无响应形态：`effectClass=NONE`，且不得带 response ID、测量区间／tick、
uncertainty identity、observable 或 post-summary。后者不是 `CONFIRMED-NOT-SENT`，不得进入 S9；
声明无响应却同时存在已归属响应属于 ERROR。普通的有类型 `PREP`／`RECOVER` 结果则携带其显式
target／summary／error 合同，并可合法地仅确认摘要、没有观测
或 measurement tick；该合同决定走 S7、S8 还是 S9。非普通记录不得伪造其分支禁止的字段。为适配器
异常合成的窄占位记录不是适配器返回的可见记录；它只用于在 evidence 账本中保留 issued identity 和一次已计费
的 S7 转换。被拒绝的返回记录与期望的 issued 记录分开保存，错误返回的 attempt identity 不得覆盖已计费
证据中的请求身份。普通适配器异常属于派发后的受控错误；这不捕获进程中断类异常。若返回记录重用
已经处理过的 execution identity，只有先按该规范已处理记录的原 action 通过完整、封闭的可见记录校验，
且随后以递归的运行时类型和值精确匹配该规范记录（其本身已绑定冻结 snapshot），它才是入站过期投递。精确比较覆盖嵌套
`PrepRecoverResult`、Boolean 确认字段、测量标量类型、effect／字段组合以及非空白 identity／evidence
字段；Python `==` 不是精确比较。不得按后续轮次当前选择的 action 校验该记录。即使当前可准入 action 的
kind 不同，真正精确的旧 TEST、PREP、RECOVER、CONFIRMED-NOT-SENT 或 UNKNOWN-EFFECT 投递仍应幂等
消费。相同 identity 但任一条件不满足的记录属于受控入口错误。相反，若在已经发出一个新动作后才返回不匹配的
记录，它是派发后错误而不是重复：实际的有类型后继和一次计费均通过 S7 保留。

有限模型在构造时会与 JSON 源对象断开。嵌套 guard／update AST 只以规范化冻结形式保留，每次
内核调用再重新解码。S0 接纳前，工厂签发的 model token 会核验精确的源 JSON identity，以及协调器
实际消费的全部有限值（action／cost、AST、frontier、limit 和 uncertainty）的摘要。binding 同样会重新
核验两份 raw-Git snapshot 及其重建出的有限投影；development 的 commit／path／blob 三元组必须与已验证
model context 的三元组完全相同。随后 `ReferenceSession` 重建私有 model 与 binding 投影，因此调用方
持有的 alias 无法在 S0 前或之后重写已接纳的 authority。已声明的 append-only live provenance
publication store 仍与提供的 model 保持兼容；因果重放在核验保留 evidence 前使用它的隔离副本。S3 的选择、
准入、计费、evidence、因果重放和后续传播只消费这些私有投影；S0 之后绝不重新把调用方持有的 model 或
binding 当作 authority。这是一条有限 authority-closure 规则，而非通用 Python sandbox：它保护本运行时实际消费的
已声明 model／action／uncertainty／provenance root 和 binding identity 字段。选择前，恢复的 state 必须属于本 run／session／model，保留精确的 development/interface authority
绑定和冻结的 S0 seed identity，且其 `H`、frontier provenance、history version、evidence 与 execution
identity 必须闭合；验证失败发生在计费或派发前。目标会话绝不会以自身绑定重新签署外来的 S0 state。
S4 前，已验证的顶层 frontier 与 event-identity map 会复制为私有的不可变 proxy，因此即使适配器持有
调用方的 backing dictionary，也不能在派发期间改写已经核对的 S0 事实。适配器运行前还会递归重构
有限的保留公共闭包（包括 `OwnershipEvent`、保留 evidence、assessment 和 ownership-replay 值）；这会阻止
一个持有旧 frozen 嵌套值的适配器借由对象级变异逃逸改写 S4 后消费的 lineage。公共 state 会从
本会话冻结的 S0 seed 逐条只读重放保留的 evidence，因此摘要、资源、snapshot／action、权威、
history 与 frontier 必须是该账本的因果终态。该重放既不调用环境，也不再派发动作。有限多路径 S0
seed 仅可在会话构造时声明、绑定到本 model/context 后冻结；手工拼装的替换 frontier 不是恢复权威。
重放也不写共享 provenance store。若完整 checkpoint
的派生记录尚不在一个新目标缓存中，但该分离重放能够闭合，它仍可恢复；其后继传播使用同一个分离的已验证
context，而不会把缓存缺失当作 prediction gap，也不会回填目标缓存。已在本地验证的 source-record 闭包可以
由其自身会话的后继计算复用。每一条声明路径必须在重放中闭合到已验证 model provenance，而不是仅闭合到目标的
可变缓存；但有界 bundle 不要求各路径具有相同的历史长度。

合成环境同样会规范化并断开它实际消费的每一项嵌套 outcome 值。构造后修改调用方的源有理数
mapping 不会改变后续可见 measurement；改变环境必须显式创建新的声明和实例。它至多携带一条显式
入站投递；恢复的会话在准入或发出下一动作前先消费该投递。

`U` 是有界且有类型的 uncertainty snapshot（`clockId`、`timeUnit=ticks`、精确的非负最大误差和
身份），不是标签。预测用该 snapshot 为每个 hypothesis 形成测量窗口；解释在 S9 前核对返回的
measurement tick 以及同一冻结的 uncertainty identity。另行由 B/C-2B assessor 将原始区间与冻结
合同对照：包含为 PASS、分离为 FAIL、边界交叠为 INCONCLUSIVE、结构／时钟／单位／误差依据无效
为 ERROR。这只是有限工程见证，不是经校准的时钟准确度或协议时序判定。

既有的标签类检查只要某个相容 hypothesis 的窗口包含该 tick，便接纳该 observable label；它仍是
有意保守的粗粒度边界。独立的 B/C-2B assessment 仅限合同范围和有限材料；两者都不建立逐
hypothesis 的协议时序、物理时钟校准、已审定 deadline authority 或符合性判定。

对已归属的 response，公开的 `measurementTick` 还必须精确等于该 response 与由受控 ownership
policy 选中的 request 之间的 timestamp 差；仅落在区间内的 tick 不足以通过。会话保留完整的类型化
ownership replay，而不是只保留选中的 `responseId`：每个 response token 都会被消费，每个非 ACTIVE
request disposition 都成为终态。每次后续 ownership 判定前，session 都将已验证账本中仍为 ACTIVE 的 request
identity、全局 sequence／timestamp 顺序和 request 编码作为 seed 注入 replay。因此，合法的增量原始 delta
可以省略终态 receipt 和保留的 ACTIVE request；若提供累计迹中的再次出现，它只能与既有 event 精确相同，
不能建立第二个 obligation。字段／kind 改变、跨角色重用、重复 response 或重复的终态 request 均进入 S7。
新引入的 request 必须可排序在 seed 之后；不能排序时必须报告 ownership context 不足，而不得猜测本地重编号的
epoch。替代 request 必须实际终止其具名的当前 ACTIVE 前驱，才可以满足非并发准入条件；已终态的旧 target 不是
准入令牌。其他 key 的完整 CANCEL/SUPERSEDE 事务仅在其既不指向已保留的 ACTIVE 受控 request、也不指向完整原始事件迹中
任何匹配 request 时才被忽略；若外键事件指向当前或未来的受控 request，仍必须核验并在不相容时拒绝。这些跨轮重放冲突会隔离新观察到且无争议的 response 事实，
但绝不把已保留的 request 变为 response（或反过来），所以其发出的 state 始终可自校验并在一个等价的新协调器中重放。
对于无 response，clock／error-basis 必须先于取消／替代产生 NOT-APPLICABLE 前校验；依据无效时为
ERROR，不得用管理性事件规避。及时的终止不需要 elapsed-horizon 读数；若合法的增量 delta 只携带终止
事件，则用已经验证的、保留的 ACTIVE trigger 提供计算该终止所需的 timestamp。对于 ACTIVE obligation，即使
尚未得到 elapsed 读数，只要 observation horizon 尚未合格，仍为 PENDING-HORIZON；只有合格的
reviewed deadline 判定才要求非负的 earliest admissible elapsed horizon。已经给出的非法 elapsed
读数仍为 ERROR。

配对和复位绝不从 Recover 动作推断。后续实验适配器必须用 `pairingId` 链接配对单位，为每个
臂保留独立、已确认的 `resetId` 与 `resetEvidenceRef`，并将该证据与会话内恢复分开。当前合成
工程运行没有登记实验 attempt 或配对复位主张。

## 待完成工作和证据边界

**延期至 B/C-3 的审计义务（A01）。** 当前公共重放会保留原始 rejected response 及其具名
`resolution_code`，但尚未重算并验证二者的因果关系。B/C-3 的 evidence／CLI 工作负责关闭：
identity、target 和可见记录错误必须保留存在且域有效的原始返回，其最小原因必须与该 code 一致；
纯工具异常不得凭空制造此类返回。关闭门为公共 evidence-transaction／CLI 对“修改或删除原始
返回”的负变异测试。在此之前，本运行时只主张受控保留，不主张精确的分支因果证明。

绑定／类型层现已执行有界合成 TEST／Prep／Recover 动作，并且只针对已经绑定的有限合成材料解析
ownership、进行合同范围内的区间 assessment；它不建立真实协议服务的 ownership、校准时序、已审定
deadline authority、IUT 行为或运行完整性。B/C-3 仍负责持久化 evidence-transaction／CLI 的因果
闭合。Researcher 启动合同核对已记录；对新的固定实现 Head 的独立复审仍 pending。后续运行在独立
复审前均保持 `SYNTHETIC-ENGINEERING-VALIDATION`，不是确认性实验或协议符合性用例。
