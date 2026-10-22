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
prediction-gap/Prep routes.  Recover, full S7/S8 coverage, ownership/T5 and
all Stop-Empty-producing paths remain explicit B/C-2 work; this table does not
claim their execution is complete.

## Initial type boundary

`HistoryHandle.initial` represents S0 input.  It permits an empty member-status
map because a status need not exist before processing.  `HistoryHandle.committed`
represents an S9/processed result and requires one controlled status for every
surviving member.  Empty `H` is legal only as a processed Stop-Empty result.
`SessionContext` separates `KNOWN` plus a confirmed summary from `UNKNOWN` or
`CONSERVATIVE-UNKNOWN`, which carry no usable current summary.

## Execution and experiment-identity bridge

An engineering session always has a `runId`, `sessionId`, immutable
`snapshotId`, `actionId`, and one `executionAttemptId` for each dispatch.  The
optional `experimentAttemptId` is a foreign key to a later registered
experiment unit; it is absent in the present engineering fixtures.  Retrying
therefore creates a new execution identity without manufacturing a second
experimental sample.  A repeated delivery of an existing execution identity
is rejected before it can be charged or committed again.

`issuedToExecutor` means that S4's admitted immutable action was handed to the
execution interface.  It does **not** mean that a network packet was sent or
that an IUT was stimulated.  Each issued execution records its resource view
before/after, five declared detail-charge components
(`acquisition`, `computation`, `preparation`, `recovery`, `retry`) and a
separate four-component projection where preparation contains recovery exactly
once.  The session selector sees only the causal resource mode, remaining
resource and declared action cost; audit-only outcome/status fields never flow
back into selection.

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
Researcher review of experiment contracts and manuscript wording is pending.
All later runs remain `SYNTHETIC-ENGINEERING-VALIDATION` until separately
reviewed; they are not confirmation experiments or protocol conformance cases.

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

当前 B/C-1 检查点实现普通 TEST 以及具名 prediction-gap／Prep 路径。Recover、完整 S7／S8
覆盖、ownership／T5 和全部可产生 Stop-Empty 的路径仍是显式 B/C-2 工作；本表不主张它们已经
执行完成。

## 初始类型边界

`HistoryHandle.initial` 表示 S0 输入；因处理前成员状态可以尚未设置，允许空状态表。
`HistoryHandle.committed` 表示 S9／已处理结果，要求每个存活成员都有一个受控状态。空
`H` 只可作为已处理的 Stop-Empty 结果。`SessionContext` 将带确认摘要的 `KNOWN` 与不
携带可用当前摘要的 `UNKNOWN`／`CONSERVATIVE-UNKNOWN` 分开。

实现必须在序列化和会话边界返回受控诊断。Python 构造器的 `ValueError` 是内部输入
边界，不是 IUT 判定；后续生产入口会将其映射为具名工具错误，且不发布无效证据包。

## 执行与实验身份桥接

工程会话始终具有 `runId`、`sessionId`、不可变 `snapshotId`、`actionId`，且每次派发
均有一个 `executionAttemptId`。可选的 `experimentAttemptId` 是后续已登记实验单位的外键；
当前工程 fixture 中该字段为空。因此，重试会产生新的执行身份，但不会伪造第二个实验样本。
同一执行身份的重复投递会在再次计费或提交前被拒绝。

`issuedToExecutor` 表示 S4 已将准入后的不可变动作交给执行接口；**不**表示网络报文已发送
或 IUT 已被刺激。每次 issued 执行记录其前后资源视图、五项声明的费用明细
（`acquisition`、`computation`、`preparation`、`recovery`、`retry`）及独立的四维投影；
投影中的 preparation 恰好折叠一次 recovery。会话选择器只读取因果资源模式、剩余资源和
声明动作成本；仅审计的 outcome/status 字段绝不回流到选择。

配对和复位绝不从 Recover 动作推断。后续实验适配器必须用 `pairingId` 链接配对单位，为每个
臂保留独立、已确认的 `resetId` 与 `resetEvidenceRef`，并将该证据与会话内恢复分开。当前合成
工程运行没有登记实验 attempt 或配对复位主张。

## 待完成工作和证据边界

绑定／类型层尚不执行动作、不推断所有权、不建立协议时序、不运行 IUT，也不建立运行
完整性。Researcher 对实验合同和论文措辞的核对仍为 pending。后续运行在独立复审前均
保持 `SYNTHETIC-ENGINEERING-VALIDATION`，不是确认性实验或协议符合性用例。
