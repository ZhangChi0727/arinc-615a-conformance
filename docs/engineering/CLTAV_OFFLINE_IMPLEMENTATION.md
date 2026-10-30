# Bounded CL-TAV offline intake implementation

| Control | Value |
|---|---|
| Authorization | CR-2026-017 / DD-041 |
| Specification inputs | CR-2026-016 / DD-038–040 and the current controlled development package |
| Scope | Read-only capture intake through bounded reconstruction evidence and a limited non-scoring replay bridge |
| Status | Candidate implementation on a Draft PR; independent review required |

## 1. Purpose and contract mapping

`cltav-offline` implements one direction only:

`capture → PACKET-REF → DATAGRAM-RECORD → TRANSFER-RECORD → PROTOCOL-EVENT → evidence index`.

The following mapping is implementation traceability, not a parallel
requirements package or a claim that a downstream module has run.

| Runtime entry or output | Controlled module / tool requirement | Controlled records / acceptance witness | Boundary |
|---|---|---|---|
| `inspect` input identity and pcap/pcapng reader | `MOD-CAPTURE` / `TR-CAPTURE-INTAKE` | `CAPTURE-IDENTITY`, `INTAKE-METADATA`, `PACKET-REF`, `AC-SYN-TRANSFER` | Caller-provided, read-only input; no live capture or clock-accuracy claim. |
| Ethernet/VLAN/IPv4 and finite fragment accumulator | `MOD-REASSEMBLY` / `TR-DATAGRAM-REASSEMBLY` | `PACKET-REF`, `DATAGRAM-RECORD`, `AC-SYN-TRANSFER` | `COMPLETE`, `GAPPED`, and `CONFLICT` are reconstruction states, not product verdicts. |
| UDP/TFTP association and bounded file-role/header parsing | `MOD-TRANSFER` / `TR-TRANSFER-RECONSTRUCTION`, `TR-PROTOCOL-EVENT` | `TRANSFER-RECORD`, `PROTOCOL-EVENT`, `AC-SYN-TRANSFER` | The G4 bridge consumes only source-rebuilt evidence and calls public `replay_ownership` for an explicitly unqualified structural trace. It never calls `assess_observation`, and neither interface is a verdict oracle for a passive capture. |
| Versioned JSON evidence envelope, adapter projection and G4 replay | `MOD-CAPTURE` → `MOD-TRANSFER` output chain | `PACKET-REF`, `DATAGRAM-RECORD`, `TRANSFER-RECORD`, `PROTOCOL-EVENT`, `OFFLINE-REPLAY` | A versioned projection identifies its controlled contract snapshot and records non-projectable unknowns explicitly. A bridge record may retain an unqualified structural ownership replay, but it creates no `OBSERVATION-ASSESSMENT`, `HISTORY-HANDLE`, qualified ownership result, or `FINDING-RECORD`. |

## 2. Supported intake and uncertainty rules

The initial local header survey found the 23 registered exploratory files to
be little-endian pcapng with Ethernet linktype 1 and Enhanced Packet Blocks.
The implementation also accepts classic pcap byte-order and micro/nanosecond
variants through synthetic tests. Other pcapng block types are either known
metadata blocks or named `UNSUPPORTED-PCAPNG-BLOCK` diagnostics; they are not
silently treated as complete packet coverage.

Each `PACKET-REF` retains the container byte offset, packet index, capture and
original length, interface identity, linktype, and timestamp as integer ticks
plus a denominator.  pcapng section/interface clock domains are distinct; the
tool does not infer synchronization, accuracy, topology, device version,
configuration or root cause. Missing time information is explicit.

Payload bytes exist only while the bounded decoder needs them. Completed
datagrams retain their declared payload length and provenance after UDP/TFTP
processing. A completed transfer may retain only a separately bounded parse
payload long enough to derive its declared first-slice information; raw block
bytes are then released while their digests remain available for provenance.
Neither serialized evidence nor retained result records keep raw capture/file
bytes.

Input identity is byte count plus SHA-256. Corpus mode verifies safe relative
paths, resolved-root containment, resolved file identity, size/hash and a
two-way manifest inventory before processing. Before it creates a staging
directory, it also resolves the corpus root, manifest, every input and the
requested output target. The target is rejected if it is equal to, inside, or
contains an input, the manifest or their parent boundary; a symbolic-link or
junction alias does not relax that check. A pre-existing target may be
replaced only when it is an exact, tool-owned result directory. The input is
hashed again after processing; a change prevents publication.

## 3. Reconstruction rules and limits

- Ethernet with up to four VLAN tags and IPv4 are decoded at declared offsets;
  unsupported linktypes, short headers, invalid IHL/lengths and invalid
  non-final fragment lengths are named diagnostics.
- An IPv4 reconstruction key includes capture, section, interface, link domain,
  VLAN context, source, destination, protocol and identification. Duplicate
  bytes are retained once; conflicting
  overlap produces `CONFLICT` without later-byte overwrite. EOF and resource
  eviction produce `GAPPED` with `INCOMPLETE-DATAGRAM` or a resource reason.
  Per-datagram byte and fragment-count bounds, plus active-datagram bounds,
  are implementation controls and produce named resource evidence rather than
  a protocol-timeout conclusion.
- UDP length must fit the complete IPv4 payload exactly. Checksum presence is
  recorded but checksum validity is `NOT-EVALUATED`.
- A TFTP session starts from an observed RRQ/WRQ to the configured service
  port, then binds the server's selected TID from a matching reverse packet in
  the same section/interface/link/VLAN context. It does not assume every later
  packet remains on port 69, nor associate an ambiguous packet to an arbitrary
  request or across a capture domain.
- RRQ/WRQ, OACK, ACK, DATA and ERROR layouts are strict. Option status is
  `ACCEPTED`, `DEFAULTED` (512 only when non-acceptance is evidenced by the
  request/response path), or `UNKNOWN`. OACK values must be numeric, in the
  request direction and within the requested upper bound. A short data block
  ends a transfer only under a known effective block size; exact-size data
  requires an observed zero-length terminator. Duplicate blocks do not
  duplicate a file; conflicting blocks do not replace earlier content. Once a
  transfer is `CONFLICT`, `ERROR`, or resource-truncated, later ordinary data
  cannot restore it to `COMPLETE`, and derived payload, length and application
  events are withdrawn. Once terminal block *n* is observed, a later block
  above *n*, or a different terminal block, is a conflict; a missing block
  below *n* may still arrive and complete the observed finite block set.
- LCI/LCL/LCS/LUI/LUR/LUS parsing is bounded to source-bound leading fields.
  It preserves fixed-width ASCII versions/ratios, conditionally used but
  physically present timers, and `0xFFFF` estimated-time absence. Remaining
  bytes remain explicitly unparsed. No checksum, file integrity, acceptance or
  conformance conclusion is produced.

All listed numeric bounds are implementation resource limits—not protocol
timeouts or product requirements—and appear in each output envelope. The
shared retained-evidence budget covers packet references, diagnostics,
interface metadata, datagrams, transfers and events. It reserves space for a
named stop record and records the unconsumed suffix rather than claiming
complete processing. `maxActiveTransferBytes` separately bounds raw active
TFTP blocks; `maxCompletedPayloadBytes` separately bounds completed payload
held for finite header parsing. Each resource diagnostic keeps input SHA-256
plus the last consumed packet/index/offset/context evidence; it never needs
retained payload bytes to remain traceable.

The envelope is a closed, versioned record contract. Publication runs the
declared Draft 2020-12 JSON Schema and cross-record semantic checks before an
atomic replacement. It verifies configured bounds, declared counts, unique
identifiers, source-reference closure, default/accepted/unknown block-size
rules, and the typed adapter projection. The runtime loads both its evidence
schema and the accepted-record definitions as package resources; the build
copies the exact controlled source bytes, and the runtime verifies the
development-contract snapshot identity before it projects records. Its textual
JSON content hash canonicalises only CRLF record separators to LF, so the
accepted Git content identity is stable across Windows and Linux builds. Every
normal projection is validated by the shared public record validator and its
parentage is checked against the originating capture evidence. Unsupported or
unknown fields remain explicitly non-projectable rather than being guessed or
zero-filled.

## 4. Command line, publication and exit status

```text
python -m pip install -e ".[dev]"
cltav-offline inspect --input <capture> --capture-id <stable-id> \
  --output .cltav-local/offline-intake/<stable-id>.json [--source-commit <caller-claim-40-hex>]
cltav-offline corpus --manifest configs/research/cltav_historical_capture_manifest.json \
  --corpus-root <authorized-local-corpus-root> \
  --output-dir .cltav-local/offline-intake/corpus [--source-commit <caller-claim-40-hex>]
cltav-offline replay --input <capture> --offline-evidence <inspect-output.json> \
  --output .cltav-local/offline-replay/<stable-id>.json
cltav-offline validate-replay --input <capture> --offline-evidence <inspect-output.json> \
  --bridge .cltav-local/offline-replay/<stable-id>.json
```

`0` means the bounded reconstruction completed without controlled issues;
`2` means an output was written but contains a controlled unknown, unsupported
condition, conflict, incomplete reconstruction, or a per-capture input fault
in corpus mode; `1` is a fatal invocation, identity, controlled-resource,
schema, tool, or publication failure. A malformed capture is represented as
per-file `FATAL-INPUT-ERROR` evidence only in corpus mode. A tool or
controlled-resource failure aborts the staged corpus transaction and never
fabricates a capture-level input error. These codes are tool-operation states,
not ARINC 615A verdict values.

`replay` is separate from active synthetic execution. It first rebuilds the
actual PR22 intake envelope from the named capture bytes, then requires the
supplied envelope and its controlled projection to be exactly equal to that
rebuild before adapting source witnesses. A successful replay or validation
returns `0` even when the bounded source says `GAPPED`, `CONFLICT`, partial,
or non-projectable: those are retained as named `NOT-SCORED` evidence, not
quietly promoted to a protocol answer. A bridge output is canonical JSON and
is staged and relation-validated before replacement. It may replace only an
existing bridge artifact for the same rebuilt source relation; a failed stage
or ordinary failed swap preserves the previous bytes, while an exceptional
rollback failure preserves its named backup rather than deleting it.

`--source-commit` is optional caller provenance. If supplied, it must be a
lowercase 40-character Git object ID and is recorded as
`CLAIMED-UNVERIFIED`; if omitted, the claim is `UNAVAILABLE`. The command does
not inspect `GITHUB_SHA`, the current directory, or a local Git checkout to
manufacture a claim. Every output instead records a deterministic runtime
source-snapshot SHA-256 and exact controlled-contract identities. These are
separate assertions: a syntactically valid caller claim is not presented as a
verified build identity.

Single-file output is written to a staged sibling and atomically replaced only
after JSON and semantic validation. Corpus mode stages every per-capture output
and its index under a verified contained directory, then swaps the directory
with rollback of an existing owned directory on a failed publication. Unsafe
capture identifiers are rejected before a path is constructed. Neither mode
writes into its capture input or its manifest boundary.

## 5. Evidence and research boundary

The output schema is
[`cltav_offline_intake_evidence.schema.json`](../../configs/engineering/cltav_offline_intake_evidence.schema.json).
It is executed at publication time, not merely published as documentation. It
excludes raw payload, absolute local paths, root-cause labels and a conformance
PASS/FAIL. Its evidence envelope always declares
`conformanceVerdict: NOT-EVALUATED` and transfer integrity
`NOT-EVALUATED`.

Historical capture runs are exploratory parser/reconstruction evidence only.
They can help later engineering and paper work cite a tool release, an input
identity and an explicit support boundary. They cannot establish runtime
integrity, controlled execution, fault truth, an experimental denominator,
product conformance, certification readiness or authority acceptance. The
paper line consumes a reviewed evidence manifest later; this implementation
does not modify manuscript sources, PDF or research claims.

The `OFFLINE-REPLAY` artifact is likewise passive. It preserves capture,
packet, datagram, transfer and event references; producer quality; clock
domain, tick resolution and unknown accuracy; and controlled non-projectable
reasons. It never issues an action, charges a cost, applies a reset, updates
history, claims a response deadline, creates protocol PASS/FAIL, or attributes
an IUT failure. A request/final-data pair is only a structural candidate when
the production source proves both witnesses; unknown/cross-domain clocks,
missing/ambiguous lineage, cancellation or supersession facts not produced by
the bounded decoder, and unresolved deadlines are not inferred and cannot
affect scoring.

# 中文版

# 有界 CL-TAV 离线接入实现

| 控制项 | 取值 |
|---|---|
| 授权 | CR-2026-017／DD-041 |
| 规格输入 | CR-2026-016／DD-038～040 及当前受控开发包 |
| 范围 | 从只读捕获接入到有界重建证据及受限、非评分的回放桥接 |
| 状态 | Draft PR 上的候选实现；需要独立评审 |

## 1. 目的与合同映射

`cltav-offline` 只实现一个方向：

`捕获 → PACKET-REF → DATAGRAM-RECORD → TRANSFER-RECORD → PROTOCOL-EVENT → 证据索引`。

下表是实现追踪，而非平行需求包，也不代表下游模块已经运行。

| 运行入口或输出 | 受控模块／工具需求 | 受控记录／验收见证 | 边界 |
|---|---|---|---|
| `inspect` 输入身份与 pcap／pcapng 读取器 | `MOD-CAPTURE`／`TR-CAPTURE-INTAKE` | `CAPTURE-IDENTITY`、`INTAKE-METADATA`、`PACKET-REF`、`AC-SYN-TRANSFER` | 调用方提供的只读输入；不主张实时捕获或时钟精度。 |
| Ethernet/VLAN/IPv4 与有限分片累加器 | `MOD-REASSEMBLY`／`TR-DATAGRAM-REASSEMBLY` | `PACKET-REF`、`DATAGRAM-RECORD`、`AC-SYN-TRANSFER` | `COMPLETE`、`GAPPED`、`CONFLICT` 是重建状态，不是产品判定。 |
| UDP/TFTP 关联与有界文件角色／头解析 | `MOD-TRANSFER`／`TR-TRANSFER-RECONSTRUCTION`、`TR-PROTOCOL-EVENT` | `TRANSFER-RECORD`、`PROTOCOL-EVENT`、`AC-SYN-TRANSFER` | G4 桥接只消费可按来源重建的证据，并仅调用公开 `replay_ownership` 对显式不合格的结构迹回放；绝不调用 `assess_observation`，两个接口均不得被当作被动捕获的判定 oracle。 |
| 版本化 JSON 证据 envelope、适配投影和 G4 回放 | `MOD-CAPTURE` → `MOD-TRANSFER` 输出链 | `PACKET-REF`、`DATAGRAM-RECORD`、`TRANSFER-RECORD`、`PROTOCOL-EVENT`、`OFFLINE-REPLAY` | 版本化投影标识受控合同快照，并明确登记无法投影的未知项；桥接记录可保留不合格的结构所有权回放，但不创建 `OBSERVATION-ASSESSMENT`、`HISTORY-HANDLE`、合格的所有权结果或 `FINDING-RECORD`。 |

## 2. 已支持的接入与不确定性规则

初始本地头部调查表明，23 份已登记探索文件均为 little-endian pcapng，使用 Ethernet linktype 1 和 Enhanced Packet Block。实现也通过合成测试接纳经典 pcap 的字节序和 micro/nanosecond 变体。其他 pcapng 块要么是已知元数据块，要么以 `UNSUPPORTED-PCAPNG-BLOCK` 具名诊断；不得静默当作完整包覆盖。

每个 `PACKET-REF` 保留容器字节偏移、包索引、捕获与原始长度、接口身份、linktype，以及以整数 tick 加分母表示的时间戳。pcapng section/interface 时钟域彼此不同；工具不推断同步、精度、拓扑、设备版本、配置或根因。缺失时间信息保持显式。

载荷字节只在有界解码器实际需要时保留。完成的数据报在 UDP／TFTP 处理后仅保留声明的载荷长度和来源。完成传输只能在独立限额内暂留解析载荷，以导出其声明的首切片信息；随后释放原始块字节，同时保留用于来源追踪的摘要。序列化证据和留存结果均不保存原始捕获／文件字节。

输入身份由字节数和 SHA-256 表示。corpus 模式在处理前核验安全相对路径、解析后根内包含、解析后文件身份、大小／散列和双向清单盘点；创建 staging 前还解析并核验 corpus 根、manifest、每个输入及请求的输出目标。若目标等于、位于或包含任何输入、manifest 或其父边界，即拒绝；符号链接或 junction 别名不得绕过该关系。已有目标只有在确认为本工具的精确结果目录时才允许替换。处理后再次散列输入，若变化则拒绝发布。

## 3. 重建规则与限额

- Ethernet（最多四层 VLAN）与 IPv4 按声明偏移解码；不支持 linktype、短头、非法 IHL／长度和非法非末分片长度均产生具名诊断。
- IPv4 重建键包含捕获、section、接口、链路域、VLAN 上下文、源、目的、协议与 identification。相同字节仅保留一次；冲突重叠产生 `CONFLICT`，不得以后续字节覆盖。EOF 与资源驱逐产生带 `INCOMPLETE-DATAGRAM` 或资源原因的 `GAPPED`。每数据报字节与分片数量上限，以及活跃数据报上限，都是实现控制；触发时产生具名资源证据，而不是协议超时结论。
- UDP 长度必须精确落在完整 IPv4 载荷内。记录 checksum 是否存在，但 checksum 有效性为 `NOT-EVALUATED`。
- TFTP 会话从指向配置服务端口的已观察 RRQ／WRQ 开始，再由同一 section／接口／链路／VLAN 上下文中的匹配反向包绑定服务端选择的 TID。不得假定后续包仍用 69 端口，也不得跨捕获域或把歧义包任意关联至请求。
- RRQ／WRQ、OACK、ACK、DATA、ERROR 布局均严格校验。选项状态为 `ACCEPTED`、`DEFAULTED`（仅当请求／响应路径已证明未接受时才取 512）或 `UNKNOWN`。OACK 值必须是数值、方向正确并且不超过请求上界。短 DATA 仅在已知有效块大小下终止传输；等长数据必须观察到零长度末块。重复块不得重复文件；冲突块不得替换原内容。一旦传输进入 `CONFLICT`、`ERROR` 或资源截断，普通后继 DATA 不得使其恢复 `COMPLETE`，派生载荷、长度和应用事件须同步撤销。一旦观察到末块 *n*，随后出现大于 *n* 的块或不同末块即为冲突；小于 *n* 的缺块仍可在之后到达并完成该有限块集合。
- LCI／LCL／LCS／LUI／LUR／LUS 仅解析来源约束的前导字段。保留定宽 ASCII 版本／比率、条件使用但物理存在的计时字段，以及 `0xFFFF` Estimated Time 未提供的含义。剩余字节显式未解析；不产生 checksum、文件完整性、接受或符合性结论。

所有列出的数值上限都是实现资源限额，而不是协议超时或产品需求；每个输出 envelope 都记录这些限额。共享证据保留预算覆盖 packet ref、诊断、接口元数据、数据报、传输和事件；为具名停止记录预留空间，并登记未消费后缀而不宣称全量处理。`maxActiveTransferBytes` 单独约束活跃 TFTP 原始块，`maxCompletedPayloadBytes` 单独约束已完成传输为有限头解析而保留的载荷。每个资源诊断保留输入 SHA-256 以及最后已消费的包／索引／偏移／上下文证据，不依赖保留载荷也能追溯。

该 envelope 是封闭且有版本的记录合同。发布前实际执行声明的 Draft 2020-12 JSON Schema 和跨记录语义检查，之后才可原子替换已有制品。它检查已配置限额、声明计数、唯一 ID、来源引用闭合、默认／已接受／未知块大小规则以及类型化适配投影。运行时将证据 schema 和已接受记录定义作为包资源加载；构建复制精确的受控源字节，运行时在投影前核验开发合同快照身份。其文本 JSON 内容散列仅将 CRLF 记录分隔符规范化为 LF，因此已接受的 Git 内容身份在 Windows 和 Linux 构建间稳定。每个可投影普通记录均经共享公共记录验证器校验，其父子来源链亦须回指原始捕获证据。无法表达的未知项以具名不可投影原因保留，不得猜测或以零填充。

## 4. 命令行、发布与退出状态

```text
python -m pip install -e ".[dev]"
cltav-offline inspect --input <capture> --capture-id <stable-id> \
  --output .cltav-local/offline-intake/<stable-id>.json [--source-commit <caller-claim-40-hex>]
cltav-offline corpus --manifest configs/research/cltav_historical_capture_manifest.json \
  --corpus-root <authorized-local-corpus-root> \
  --output-dir .cltav-local/offline-intake/corpus [--source-commit <caller-claim-40-hex>]
cltav-offline replay --input <capture> --offline-evidence <inspect-output.json> \
  --output .cltav-local/offline-replay/<stable-id>.json
cltav-offline validate-replay --input <capture> --offline-evidence <inspect-output.json> \
  --bridge .cltav-local/offline-replay/<stable-id>.json
```

`0` 表示有界重建完成且无受控问题；`2` 表示已写入输出，但包含受控未知、不支持条件、冲突、未完成重建，或 corpus 模式下逐捕获的输入故障；`1` 表示致命调用、身份、受控资源、schema、工具或发布错误。畸形捕获仅在 corpus 模式下以逐文件 `FATAL-INPUT-ERROR` 证据表示；工具或受控资源失败会中止整个 staging 事务，绝不伪造成某一捕获的输入错误。这些代码是工具运行状态，不是 ARINC 615A 判定值。

`replay` 与主动合成执行严格分开。它先从所指捕获字节重建实际 PR22 intake envelope，再要求给定 envelope 及其受控投影与该重建结果完全相等，之后才适配来源见证。即使有界来源标为 `GAPPED`、`CONFLICT`、部分解析或不可投影，成功的 replay／validation 也返回 `0`：这些状态会以具名 `NOT-SCORED` 证据保留，绝不能静默升级为协议答案。桥接输出是 canonical JSON，在替换前先 staging 并作关系校验；只能替换属于同一已重建来源关系的既有桥接制品。staging 失败或普通替换失败时保持旧字节；若回滚本身异常，则保留具名 backup，不得删除旧制品。

`--source-commit` 是可选的调用方来源声明。若给出，必须是小写 40 位 Git 对象 ID，并标为 `CLAIMED-UNVERIFIED`；若未给出，标为 `UNAVAILABLE`。命令不会读取 `GITHUB_SHA`、当前目录或本地 Git checkout 来制造声明。每个输出改为记录确定性的运行源码快照 SHA-256 及精确的受控合同身份。这些是不同强度的断言：语法正确的调用方声明不得表述成已核验构建身份。

单文件输出先写入同目录 staging 文件，JSON 和语义校验后才原子替换。corpus 模式在已验证的包含目录内 staging 所有逐文件输出与索引，随后交换目录；发布失败时回滚已有的工具拥有目录。不安全的捕获 ID 会在构造路径前被拒绝。两种模式都不写入捕获输入或 manifest 边界。

## 5. 证据与研究边界

输出 schema 为
[`cltav_offline_intake_evidence.schema.json`](../../configs/engineering/cltav_offline_intake_evidence.schema.json)。
它在发布时实际执行，而不只是作为文档发布。它排除原始载荷、绝对本地路径、根因标签和符合性 PASS/FAIL。证据 envelope 始终声明 `conformanceVerdict: NOT-EVALUATED`，传输完整性为 `NOT-EVALUATED`。

历史抓包运行只是探索性解析／重建证据。它可使后续工程和论文工作引用工具发布、输入身份和明确的支持边界；不能建立运行完整性、受控执行、故障真值、实验分母、产品符合性、认证准备度或权威接受。论文线在后续消费经过评审的 evidence manifest；本实现不修改稿件源、PDF 或研究主张。

`OFFLINE-REPLAY` 制品同样是被动的。它保留 capture、packet、datagram、transfer 和 event 引用，生产者质量，clock domain、tick 分辨率和未知精度，以及受控的不可投影原因；绝不发出动作、计费、施加复位、更新历史、主张响应期限、产生协议 PASS/FAIL，或归因 IUT 失败。只有生产来源同时证明 request/final-data 两个见证时，二者才可形成结构候选；未知／跨域时钟、缺失／歧义来源、有界解码器未产生的 cancellation 或 supersession 事实，以及未决期限，均不得被推断，也不得影响评分。
