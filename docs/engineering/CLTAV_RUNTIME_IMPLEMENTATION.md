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

## Initial type boundary

`HistoryHandle.initial` represents S0 input.  It permits an empty member-status
map because a status need not exist before processing.  `HistoryHandle.committed`
represents an S9/processed result and requires one controlled status for every
surviving member.  Empty `H` is legal only as a processed Stop-Empty result.
`SessionContext` separates `KNOWN` plus a confirmed summary from `UNKNOWN` or
`CONSERVATIVE-UNKNOWN`, which carry no usable current summary.

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

## 初始类型边界

`HistoryHandle.initial` 表示 S0 输入；因处理前成员状态可以尚未设置，允许空状态表。
`HistoryHandle.committed` 表示 S9／已处理结果，要求每个存活成员都有一个受控状态。空
`H` 只可作为已处理的 Stop-Empty 结果。`SessionContext` 将带确认摘要的 `KNOWN` 与不
携带可用当前摘要的 `UNKNOWN`／`CONSERVATIVE-UNKNOWN` 分开。

实现必须在序列化和会话边界返回受控诊断。Python 构造器的 `ValueError` 是内部输入
边界，不是 IUT 判定；后续生产入口会将其映射为具名工具错误，且不发布无效证据包。

## 待完成工作和证据边界

绑定／类型层尚不执行动作、不推断所有权、不建立协议时序、不运行 IUT，也不建立运行
完整性。Researcher 对实验合同和论文措辞的核对仍为 pending。后续运行在独立复审前均
保持 `SYNTHETIC-ENGINEERING-VALIDATION`，不是确认性实验或协议符合性用例。
