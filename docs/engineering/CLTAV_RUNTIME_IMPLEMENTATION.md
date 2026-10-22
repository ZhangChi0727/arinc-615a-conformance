# Bounded CL-TAV session runtime implementation

| Control | Value |
|---|---|
| Authorization | CR-2026-021 / DD-045 |
| Initial kernel checkpoint | PR #25 `87f9330306be411a3d2d580a356070072dcf903f` |
| Scope | Finite reference session coordination and in-process synthetic engineering validation |
| Status | Candidate implementation on a Draft PR; independent review required |

## Authority-to-runtime mapping

This table is traceability for code; it is not a second method, requirements or
experiment authority.  Every invocation loads its declared Git-object input
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

The current B/C-1 checkpoint implements the normal TEST and named
prediction-gap/Prep routes through one read-only admission decision.  A
current TEST prediction gap withholds TEST minimax even when another TEST has
classes; eligible PREP is then evaluated by that same resource decision.
The GAP revokes the whole current TEST scoring set, including any unaffordable
TEST-derived A2 conclusion: with no eligible PREP, the exit remains the named
prediction gap; only an eligible but unaffordable PREP may produce A2 on that
fallback route.
Recover, full S7/S8 coverage, ownership/T5 and
all Stop-Empty-producing paths remain explicit B/C-2 work; this table does not
claim their execution is complete.

## Initial type boundary

`HistoryHandle.initial` represents S0 input.  It permits an empty member-status
map because a status need not exist before processing.  `HistoryHandle.committed`
represents an S9/processed result and requires one controlled status for every
surviving member.  Empty `H` is legal only as a processed Stop-Empty result.
`SessionContext` separates `KNOWN` plus a confirmed summary from `UNKNOWN` or
`CONSERVATIVE-UNKNOWN`, which carry no usable current summary.

Each surviving `H` member carries a nonempty, bounded tuple of current frontier
provenance references, rather than a single flattened representative.  The
finite predictor propagates every path independently: an infeasible path removes
only that path, while an unsupported or bounded calculation retains its source
path as conservative.  A conservative member is retained in every completed
normal observation class and is committed as `CONSERVATIVE-UNKNOWN`; it is never
turned into a synthetic observable outcome.  If no completed visible class is
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
result identity, or observation outside the frozen snapshot does not restore
the pre-issue state: it retains the one charge and expected attempt identity,
records a controlled error, sets the session to `CONSERVATIVE-UNKNOWN`, and
does not invoke S9.  If a returned result includes a typed successor environment,
that actual successor is retained even when its record is rejected.  A normal
record which claims summary confirmation but omits its post-summary is the same
controlled post-dispatch error.  `CONFIRMED-NOT-SENT` is distinct: it is charged once but
preserves the prior history and known summary.

Before any effect branch, the session validates the complete visible-record
domain and its field combinations: identity/action/evidence references are
nonempty strings; confirmation is Boolean; normal records carry a visible
observation, a confirmed nonempty post-summary, an exact measurement tick and
the frozen uncertainty identity; non-normal records cannot manufacture those
fields.  A rejected response is retained separately from the expected issued
record, so an incorrect returned attempt identity cannot overwrite the request
identity in the charged evidence.  Ordinary adapter exceptions are controlled
post-dispatch errors; this does not catch process-interrupt exceptions.

The finite model is JSON-detached at construction.  Its nested guard/update
AST is retained only in canonical frozen form and decoded afresh for each
kernel call, so a post-construction source mutation cannot change behaviour
without changing the model identity.  Before selection, a resumed state must
belong to this run/session/model and close its `H`, frontier provenance,
history version, evidence, and execution identities; validation failure occurs
before charge or dispatch.  The public state is replayed read-only from this
session's frozen S0 seed through each retained evidence item, so summary,
resource, snapshot/action, authority, history and frontier values must be the
causal terminal state of that ledger.  This replay neither calls the environment
nor issues another action or writes the shared provenance store: successor
calculation uses a detached copy of the already verified source records.  A
finite multi-path S0 seed is permitted only when
declared at session construction, bound to this model/context, and then frozen;
hand-assembled replacement frontiers are not an alternate resume authority.
Each declared path must close over this model's provenance, but a bounded
bundle does not require its paths to have equal history lengths.

The synthetic environment likewise normalizes and detaches each nested outcome
value that it actually consumes.  Modifying a caller's source rational mapping
after construction cannot change a later visible measurement; a changed
environment requires an explicit new declaration and instance.

`U` is a bounded, typed uncertainty snapshot (`clockId`, `timeUnit=ticks`,
exact nonnegative maximum error and identity), not a label.  Prediction forms
per-hypothesis measurement windows with that snapshot; interpretation checks
the returned measurement tick and the same frozen uncertainty identity before
S9.  This is only finite synthetic engineering behavior, not calibrated clock
accuracy or a protocol timing verdict.

Interpretation currently admits an observable label when its tick lies in at
least one compatible per-hypothesis window.  That is a deliberately coarse,
conservative label-class boundary: it is not a per-hypothesis timing exclusion,
physical clock calibration, T5 implementation, or deadline verdict.

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

The binding/type layer does not yet execute an action, infer ownership,
establish protocol timing, run an IUT or establish runtime integrity.  The
Researcher startup contract review is recorded; independent review of the new
fixed implementation head remains pending.  All later runs remain
`SYNTHETIC-ENGINEERING-VALIDATION` until separately reviewed; they are not
confirmation experiments or protocol conformance cases.

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

当前 B/C-1 检查点通过同一个只读准入决定实现普通 TEST 以及具名 prediction-gap／Prep 路径。
当前 TEST prediction gap 即使与另一具有 classes 的 TEST 同时存在，也会先抑制 TEST minimax；
随后由同一资源决定检查合格 Prep。Recover、完整 S7／S8 覆盖、ownership／T5 和全部可产生
Stop-Empty 的路径仍是显式 B/C-2 工作；本表不主张它们已经执行完成。

GAP 会撤销整个当前 TEST 评分集，包括由不可负担 TEST 推导出的 A2：没有合格 Prep 时出口仍为
具名 prediction gap；只有合格但不可负担的 Prep 才能在该 fallback 路径产生 A2。

## 初始类型边界

`HistoryHandle.initial` 表示 S0 输入；因处理前成员状态可以尚未设置，允许空状态表。
`HistoryHandle.committed` 表示 S9／已处理结果，要求每个存活成员都有一个受控状态。空
`H` 只可作为已处理的 Stop-Empty 结果。`SessionContext` 将带确认摘要的 `KNOWN` 与不
携带可用当前摘要的 `UNKNOWN`／`CONSERVATIVE-UNKNOWN` 分开。

每个存活的 `H` 成员均携带非空且有界的当前 frontier provenance 引用元组，而不是一个被
扁平化的代表。有限预测器逐路径传播：不可行路径只会排除自身；不支持或受限的计算则将其
源路径保留为保守路径。保守成员会保留在每个已完成的普通观测类中，并以
`CONSERVATIVE-UNKNOWN` 提交；它绝不会被伪造为一个可观测结果。若没有已完成的可见类，或
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
声明成本。S4 之后发生执行侧异常、畸形执行返回、返回身份无效，或观测不属于冻结 snapshot 时，
均不得恢复到派发前状态：保留一次计费和期望的 attempt 身份，记录受控错误，将会话置为
`CONSERVATIVE-UNKNOWN`，且不得调用 S9。若返回结果包含有类型的后继环境，即使其记录被拒绝，
也保留该实际后继环境。声称已确认摘要却缺少后继摘要的普通记录，同样属于派发后的受控错误。
`CONFIRMED-NOT-SENT` 与此不同：它恰好计费一次，
但保留此前 history 和已知摘要。

进入任何 effect 分支前，会话校验完整的可见记录域及其字段组合：身份／动作／证据引用均为非空
字符串，确认字段为 Boolean；普通记录携带可见观测、已确认的非空后继摘要、精确测量 tick 和
冻结的 uncertainty identity；非普通记录不得伪造这些字段。被拒绝的返回记录与期望的 issued
记录分开保存，错误返回的 attempt identity 不得覆盖已计费证据中的请求身份。普通适配器异常
属于派发后的受控错误；这不捕获进程中断类异常。

有限模型在构造时会与 JSON 源对象断开。嵌套 guard／update AST 只以规范化冻结形式保留，每次
内核调用再重新解码；因此，构造后修改源对象不会在不改变 model identity 的情况下改变行为。
选择前，恢复的 state 必须属于本 run／session／model，且其 `H`、frontier provenance、history
version、evidence 与 execution identity 必须闭合；验证失败发生在计费或派发前。公共 state 会从
本会话冻结的 S0 seed 逐条只读重放保留的 evidence，因此摘要、资源、snapshot／action、权威、
history 与 frontier 必须是该账本的因果终态。该重放既不调用环境，也不再派发动作。有限多路径 S0
seed 仅可在会话构造时声明、绑定到本 model/context 后冻结；手工拼装的替换 frontier 不是恢复权威。
每一条声明路径都必须闭合到该 model 的 provenance，但有界 bundle 不要求各路径具有相同的历史长度。
重放也不写共享 provenance store：后继计算只使用已验证 source record 的分离副本。

合成环境同样会规范化并断开它实际消费的每一项嵌套 outcome 值。构造后修改调用方的源有理数
mapping 不会改变后续可见 measurement；改变环境必须显式创建新的声明和实例。

`U` 是有界且有类型的 uncertainty snapshot（`clockId`、`timeUnit=ticks`、精确的非负最大误差和
身份），不是标签。预测用该 snapshot 为每个 hypothesis 形成测量窗口；解释在 S9 前核对返回的
measurement tick 以及同一冻结的 uncertainty identity。这仅是有限合成工程行为，不是经校准的
时钟准确度或协议时序判定。

当前解释只要某个相容 hypothesis 的窗口包含该 tick，便接纳该 observable label。它是有意保守的
标签类粗粒度边界：不是逐 hypothesis 的时序排除、物理时钟校准、T5 实现或 deadline 判定。

配对和复位绝不从 Recover 动作推断。后续实验适配器必须用 `pairingId` 链接配对单位，为每个
臂保留独立、已确认的 `resetId` 与 `resetEvidenceRef`，并将该证据与会话内恢复分开。当前合成
工程运行没有登记实验 attempt 或配对复位主张。

## 待完成工作和证据边界

绑定／类型层尚不执行动作、不推断所有权、不建立协议时序、不运行 IUT，也不建立运行
完整性。Researcher 启动合同核对已记录；对新的固定实现 Head 的独立复审仍 pending。后续运行
在独立复审前均保持 `SYNTHETIC-ENGINEERING-VALIDATION`，不是确认性实验或协议符合性用例。
