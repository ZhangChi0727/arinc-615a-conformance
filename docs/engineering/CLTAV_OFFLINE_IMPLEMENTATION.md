# Bounded CL-TAV offline intake implementation

| Control | Value |
|---|---|
| Authorization | CR-2026-017 / DD-041 |
| Specification inputs | CR-2026-016 / DD-038–040 and the current controlled development package |
| Scope | Read-only capture intake through bounded reconstruction evidence |
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
| UDP/TFTP association and bounded file-role/header parsing | `MOD-TRANSFER` / `TR-TRANSFER-RECONSTRUCTION`, `TR-PROTOCOL-EVENT` | `TRANSFER-RECORD`, `PROTOCOL-EVENT`, `AC-SYN-TRANSFER` | `IF-EXECUTE-RECORD` is used only as the existing intake/output compatibility boundary; `IF-OBS-INTERPRET` is not invoked as an ownership or verdict oracle. |
| Versioned JSON evidence envelope | `MOD-CAPTURE` → `MOD-TRANSFER` output chain | `PACKET-REF`, `DATAGRAM-RECORD`, `TRANSFER-RECORD`, `PROTOCOL-EVENT` | It does not create `OWNERSHIP-RESULT`, `OBSERVATION-ASSESSMENT`, `HISTORY-HANDLE`, or `FINDING-RECORD`. |

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

Input identity is byte count plus SHA-256.  Corpus mode verifies safe relative
paths, resolved-root containment, resolved file identity, size/hash and a
two-way manifest inventory before processing. The input is hashed again after
processing; a change prevents publication.

## 3. Reconstruction rules and limits

- Ethernet with up to four VLAN tags and IPv4 are decoded at declared offsets;
  unsupported linktypes, short headers, invalid IHL/lengths and invalid
  non-final fragment lengths are named diagnostics.
- An IPv4 reconstruction key includes capture, interface, source, destination,
  protocol and identification. Duplicate bytes are retained once; conflicting
  overlap produces `CONFLICT` without later-byte overwrite. EOF and resource
  eviction produce `GAPPED` with `INCOMPLETE-DATAGRAM` or a resource reason.
- UDP length must fit the complete IPv4 payload exactly. Checksum presence is
  recorded but checksum validity is `NOT-EVALUATED`.
- A TFTP session starts from an observed RRQ/WRQ to the configured service
  port, then binds the server's selected TID from a matching reverse packet.
  It does not assume every later packet remains on port 69, nor associate an
  ambiguous packet to an arbitrary request.
- RRQ/WRQ, OACK, ACK, DATA and ERROR layouts are strict. Option status is
  `ACCEPTED`, `DEFAULTED` (512 only when non-acceptance is evidenced), or
  `UNKNOWN`. A short data block ends a transfer only under a known effective
  block size; exact-size data requires an observed zero-length terminator.
  Duplicate blocks do not duplicate a file; conflicting blocks do not replace
  earlier content.
- LCI/LCL/LCS/LUI/LUR/LUS parsing is bounded to source-bound leading fields.
  It preserves fixed-width ASCII versions/ratios, conditionally used but
  physically present timers, and `0xFFFF` estimated-time absence. Remaining
  bytes remain explicitly unparsed. No checksum, file integrity, acceptance or
  conformance conclusion is produced.

All listed numeric bounds are implementation resource limits—not protocol
timeouts or product requirements—and appear in each output envelope.

## 4. Command line, publication and exit status

```text
python -m pip install -e ".[dev]"
cltav-offline inspect --input <capture> --capture-id <stable-id> \
  --output .cltav-local/offline-intake/<stable-id>.json --source-commit <40-hex-head>
cltav-offline corpus --manifest configs/research/cltav_historical_capture_manifest.json \
  --corpus-root <authorized-local-corpus-root> \
  --output-dir .cltav-local/offline-intake/corpus --source-commit <40-hex-head>
```

`0` means the bounded reconstruction completed without controlled issues;
`2` means an output was written but contains a controlled unknown, unsupported
condition, conflict or incomplete reconstruction; `1` is a fatal invocation,
identity, input or publication failure. These codes are tool-operation states,
not ARINC 615A verdict values.

Single-file output is written to a staged sibling and atomically replaced only
after JSON validation. Corpus mode stages every per-capture output and its
index, then swaps the directory with rollback of an existing directory on a
failed publication. Neither mode writes into its capture input.

## 5. Evidence and research boundary

The output schema is
[`cltav_offline_intake_evidence.schema.json`](../../configs/engineering/cltav_offline_intake_evidence.schema.json).
It excludes raw payload, absolute local paths, root-cause labels and a
conformance PASS/FAIL. Its evidence envelope always declares
`conformanceVerdict: NOT-EVALUATED` and transfer integrity
`NOT-EVALUATED`.

Historical capture runs are exploratory parser/reconstruction evidence only.
They can help later engineering and paper work cite a tool release, an input
identity and an explicit support boundary. They cannot establish runtime
integrity, controlled execution, fault truth, an experimental denominator,
product conformance, certification readiness or authority acceptance. The
paper line consumes a reviewed evidence manifest later; this implementation
does not modify manuscript sources, PDF or research claims.

# 中文版

# 有界 CL-TAV 离线接入实现

| 控制项 | 取值 |
|---|---|
| 授权 | CR-2026-017／DD-041 |
| 规格输入 | CR-2026-016／DD-038～040 及当前受控开发包 |
| 范围 | 从只读捕获接入到有界重建证据 |
| 状态 | Draft PR 上的候选实现；需要独立评审 |

## 1. 目的与合同映射

`cltav-offline` 只实现一个方向：

`捕获 → PACKET-REF → DATAGRAM-RECORD → TRANSFER-RECORD → PROTOCOL-EVENT → 证据索引`。

下表是实现追踪，而非平行需求包，也不代表下游模块已经运行。

| 运行入口或输出 | 受控模块／工具需求 | 受控记录／验收见证 | 边界 |
|---|---|---|---|
| `inspect` 输入身份与 pcap／pcapng 读取器 | `MOD-CAPTURE`／`TR-CAPTURE-INTAKE` | `CAPTURE-IDENTITY`、`INTAKE-METADATA`、`PACKET-REF`、`AC-SYN-TRANSFER` | 调用方提供的只读输入；不主张实时捕获或时钟精度。 |
| Ethernet/VLAN/IPv4 与有限分片累加器 | `MOD-REASSEMBLY`／`TR-DATAGRAM-REASSEMBLY` | `PACKET-REF`、`DATAGRAM-RECORD`、`AC-SYN-TRANSFER` | `COMPLETE`、`GAPPED`、`CONFLICT` 是重建状态，不是产品判定。 |
| UDP/TFTP 关联与有界文件角色／头解析 | `MOD-TRANSFER`／`TR-TRANSFER-RECONSTRUCTION`、`TR-PROTOCOL-EVENT` | `TRANSFER-RECORD`、`PROTOCOL-EVENT`、`AC-SYN-TRANSFER` | `IF-EXECUTE-RECORD` 仅作为已有接入／输出相容边界；不调用 `IF-OBS-INTERPRET` 作为所有权或判定 oracle。 |
| 版本化 JSON 证据 envelope | `MOD-CAPTURE` → `MOD-TRANSFER` 输出链 | `PACKET-REF`、`DATAGRAM-RECORD`、`TRANSFER-RECORD`、`PROTOCOL-EVENT` | 不创建 `OWNERSHIP-RESULT`、`OBSERVATION-ASSESSMENT`、`HISTORY-HANDLE` 或 `FINDING-RECORD`。 |

## 2. 已支持的接入与不确定性规则

初始本地头部调查表明，23 份已登记探索文件均为 little-endian pcapng，使用 Ethernet linktype 1 和 Enhanced Packet Block。实现也通过合成测试接纳经典 pcap 的字节序和 micro/nanosecond 变体。其他 pcapng 块要么是已知元数据块，要么以 `UNSUPPORTED-PCAPNG-BLOCK` 具名诊断；不得静默当作完整包覆盖。

每个 `PACKET-REF` 保留容器字节偏移、包索引、捕获与原始长度、接口身份、linktype，以及以整数 tick 加分母表示的时间戳。pcapng section/interface 时钟域彼此不同；工具不推断同步、精度、拓扑、设备版本、配置或根因。缺失时间信息保持显式。

输入身份由字节数和 SHA-256 表示。corpus 模式在处理前核验安全相对路径、解析后根内包含、解析后文件身份、大小／散列和双向清单盘点；处理后再次散列输入，若变化则拒绝发布。

## 3. 重建规则与限额

- Ethernet（最多四层 VLAN）与 IPv4 按声明偏移解码；不支持 linktype、短头、非法 IHL／长度和非法非末分片长度均产生具名诊断。
- IPv4 重建键包含捕获、接口、源、目的、协议与 identification。相同字节仅保留一次；冲突重叠产生 `CONFLICT`，不得以后续字节覆盖。EOF 与资源驱逐产生带 `INCOMPLETE-DATAGRAM` 或资源原因的 `GAPPED`。
- UDP 长度必须精确落在完整 IPv4 载荷内。记录 checksum 是否存在，但 checksum 有效性为 `NOT-EVALUATED`。
- TFTP 会话从指向配置服务端口的已观察 RRQ／WRQ 开始，再由匹配的反向包绑定服务端选择的 TID。不得假定后续包仍用 69 端口，也不得把歧义包任意关联至请求。
- RRQ／WRQ、OACK、ACK、DATA、ERROR 布局均严格校验。选项状态为 `ACCEPTED`、`DEFAULTED`（仅在已证实未接受时取 512）或 `UNKNOWN`。短 DATA 仅在已知有效块大小下终止传输；等长数据必须观察到零长度末块。重复块不得重复文件；冲突块不得替换原内容。
- LCI／LCL／LCS／LUI／LUR／LUS 仅解析来源约束的前导字段。保留定宽 ASCII 版本／比率、条件使用但物理存在的计时字段，以及 `0xFFFF` Estimated Time 未提供的含义。剩余字节显式未解析；不产生 checksum、文件完整性、接受或符合性结论。

所有列出的数值上限都是实现资源限额，而不是协议超时或产品需求；每个输出 envelope 都记录这些限额。

## 4. 命令行、发布与退出状态

```text
python -m pip install -e ".[dev]"
cltav-offline inspect --input <capture> --capture-id <stable-id> \
  --output .cltav-local/offline-intake/<stable-id>.json --source-commit <40-hex-head>
cltav-offline corpus --manifest configs/research/cltav_historical_capture_manifest.json \
  --corpus-root <authorized-local-corpus-root> \
  --output-dir .cltav-local/offline-intake/corpus --source-commit <40-hex-head>
```

`0` 表示有界重建完成且无受控问题；`2` 表示已写入输出，但包含受控未知、不支持条件、冲突或未完成重建；`1` 表示致命调用、身份、输入或发布错误。这些代码是工具运行状态，不是 ARINC 615A 判定值。

单文件输出先写入同目录 staging 文件，JSON 校验后才原子替换。corpus 模式先 staging 所有逐文件输出与索引，随后交换目录；发布失败时回滚现有目录。两种模式都不写入捕获输入。

## 5. 证据与研究边界

输出 schema 为
[`cltav_offline_intake_evidence.schema.json`](../../configs/engineering/cltav_offline_intake_evidence.schema.json)。
它排除原始载荷、绝对本地路径、根因标签和符合性 PASS/FAIL。证据 envelope 始终声明 `conformanceVerdict: NOT-EVALUATED`，传输完整性为 `NOT-EVALUATED`。

历史抓包运行只是探索性解析／重建证据。它可使后续工程和论文工作引用工具发布、输入身份和明确的支持边界；不能建立运行完整性、受控执行、故障真值、实验分母、产品符合性、认证准备度或权威接受。论文线在后续消费经过评审的 evidence manifest；本实现不修改稿件源、PDF 或研究主张。
