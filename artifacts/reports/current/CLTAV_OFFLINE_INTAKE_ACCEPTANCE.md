# CL-TAV bounded offline intake acceptance evidence

| Control | Value |
|---|---|
| Report ID | `RPT-CLTAV-OFFLINE-INTAKE-2026-001` |
| Authorization | `CR-2026-017` / `DD-041` |
| Work order | `WO-CLTAV-OFFLINE-IMPLEMENTATION-2026-001` |
| Candidate status | Draft-PR candidate; independent review required |
| Evidence kind | Offline intake and reconstruction evidence, not a conformance result |

## 1. Accepted scope and exclusions

The candidate implements only the following deterministic, read-only path:

`capture → PACKET-REF → DATAGRAM-RECORD → TRANSFER-RECORD → PROTOCOL-EVENT → evidence index`.

It accepts caller-provided capture files, produces versioned JSON evidence, and
uses bounded resources and transactional publication.  It does **not** send
network traffic, interact with an IUT, execute a complete CL-TAV loop, create
a solver, establish CRC or file integrity, issue an ARINC 615A PASS/FAIL,
identify a root cause, establish runtime integrity, activate M3, create a
Project Configuration, or make a capability, certification, or experimental
claim.  The output declares `conformanceVerdict: NOT-EVALUATED`.

The implementation-to-contract mapping and operating boundary are maintained
in [`CLTAV_OFFLINE_IMPLEMENTATION.md`](../../../docs/engineering/CLTAV_OFFLINE_IMPLEMENTATION.md).
That mapping reuses the controlled capture, reassembly, transfer, record, and
acceptance identities; it is not a parallel requirements package.

## 2. Reproducible local evidence

The historical input is the caller-provided exploratory manifest
`CLTAV-HISTORICAL-CAPTURES` version `1.0`. Its identity audit covered all 23
registered captures before the local intake run. The run records a deterministic
runtime-source snapshot instead of treating a caller-provided Git OID as a
verified build identity:

`ec0bd173836ed285f8c02a2d115e5725033f1af8f0152d2f7f993e611462e345`

The caller supplied `9cfb35ab1a231228b907f7e5b4af3487aea88c66`, which the
evidence correctly labels `CLAIMED-UNVERIFIED`. The consumed development
contract is the exact snapshot
`configs/engineering/cltav_development_contracts.json` with SHA-256
`3331fadf2786133f161eded9d1fb42066ca58d7dd510ce6e775da1cd89a5aae1`.

The ignored, local-only corpus index was written under `.cltav-local/` and has
SHA-256:

`a8b091d02f98eed6c15704bb3f857bd9eab90abb4f7738cc1c3495c49fdddd0b`

Aggregate result only:

| Measure | Result |
|---|---:|
| Registered capture identities audited | 23 |
| Corpus outputs published | 23 captures plus one corpus index |
| `COMPLETE` reconstructions | 0 |
| `COMPLETE-WITH-CONTROLLED-ISSUES` reconstructions | 23 |
| Runtime source snapshot | `ec0bd17…1462e345` |
| Source-claim status | `CLAIMED-UNVERIFIED` |

These figures are an intake-support boundary, not a success rate, a protocol
verdict, an experimental denominator, or a statement about the captured
systems. In particular, controlled issues are retained rather than tuned away
to manufacture a `COMPLETE` result. No local root, filename, address, payload,
annotation, topology, clock characterization, configuration, or root-cause
label is stored in Git.

## 3. Public verification entry points

```text
python -m pip install -e ".[dev]"
cltav-offline --version
pytest -q tests/unit/test_cltav_offline_intake.py
python scripts/audit_capture_manifest.py --manifest configs/research/cltav_historical_capture_manifest.json --corpus-root <authorized-local-corpus-root>
python -m cltav_offline corpus --manifest configs/research/cltav_historical_capture_manifest.json --corpus-root <authorized-local-corpus-root> --output-dir .cltav-local/offline-intake/corpus [--source-commit <caller-claim-40-hex>]
```

The full repository gate sequence is recorded in the Draft PR and its CI run
for the immutable PR head.  It includes the development-readiness checker,
M1/M2 synchronization, project overview synchronization, baseline checker,
manuscript checker, full test suite, strict Python compilation, and
`git diff --check`.  CI uses public synthetic fixtures only; it does not
depend on the local corpus.

## 4. Work-order acceptance trace

| ID | Evidence |
|---|---|
| E-01 | `CR-2026-017`, `DD-041`, and preserved historical `CR-2026-016`; global executable/M3 gate remains blocked. |
| E-02 | Dedicated `codex/cltav-offline-intake-runtime` branch and isolated worktree; exactly one Draft PR is the external delivery artifact. |
| E-03 | Installed `cltav-offline` CLI plus end-to-end synthetic pcap/pcapng tests cover the complete output chain. |
| E-04 | Closed JSON schema and runtime envelope validation in `configs/engineering/cltav_offline_intake_evidence.schema.json` and `src/cltav_offline/evidence.py`. |
| E-05 | Integer timestamp representation, section/interface clock separation, capture identity checks, and named truncation/link diagnostics. |
| E-06 | Bounded IPv4 reconstruction with `COMPLETE`, `GAPPED`, and `CONFLICT`, conflict preservation, provenance, and resource diagnostics. |
| E-07 | Production-path tests for request/TID binding, OACK accepted/defaulted/unknown behavior, short blocks, zero terminators, duplicate blocks, and gaps. |
| E-08 | Bounded LCI/LCL/LCS/LUI/LUR/LUS extraction with source-bound fields and explicit unparsed remainder; no codec-completeness claim. |
| E-09 | Envelope declares conformance and transfer integrity `NOT-EVALUATED`; no ownership, T5, history, CRC, or active-loop result is emitted. |
| E-10 | Streamed readers, declared resource limits, deterministic normalization tests, atomic single-file publication, corpus rollback, and named diagnostics. |
| E-11 | Manifest audit and 23-capture local run summarized in section 2; only aggregate, non-sensitive identity evidence is retained here. |
| E-12 | Public synthetic fixtures and CLI tests; no live network operation or private-corpus CI dependency. |
| E-13 | This record plus the design/contract mapping document define the paper handoff boundary without modifying paper claims. |
| E-14 | Full repository gates and final-head CI are required before independent review; their commands are listed in section 3. |
| E-15 | The PR comparison against its current base isolates this runtime/documentation increment; protected inputs remain controlled rather than rewritten for implementation convenience. |
| E-16 | The Draft PR must bind local/remote CI to its final 40-hex head and must retain `Draft`; it does not activate a capability or configuration state. |

## 5. PR #22 remediation closure evidence

The following records corrective evidence for the independent review findings.
It is a candidate-side trace, not an independent approval.

| Finding | Corrective boundary exercised by public tests |
|---|---|
| P22-F01 | Corpus publication resolves input, manifest and output identities before staging; it rejects equal, descendant, ancestor and alias targets, unsafe capture IDs and unowned targets; rollback leaves prior output intact. |
| P22-F02 | Terminal TFTP `CONFLICT`, protocol `ERROR` and resource outcomes cannot be revived by later data; derived completion data/events are withdrawn; duplicate requests, TID binding, OACK limits, defaulted/unknown options and rollover are exercised. |
| P22-F03 | Reassembly and transfer association include section, interface, link-domain and VLAN context; cross-domain fragments/requests do not merge. |
| P22-F04 | A versioned adapter binds the exact accepted contract snapshot, projects the four accepted record types from normal production evidence and records non-projectable unknowns without fabricated values. The production-path test invokes the public record validator for every normal projection. |
| P22-F05 | Publication executes the declared JSON Schema plus cross-record checks; malformed normal and fatal envelopes fail before replacement. |
| P22-F06 | Shared retained-record limits cover success and diagnostic paths, reserve a stop record, and retain SHA/index/offset/context traceability without raw payload. |
| P22-F07 | Partial, malformed and opaque first-slice results remain distinct from parsed application events. |
| P22-F08 | Short pcapng structural input returns a named controlled error; legal EPB options and supported container variants remain accepted. |
| P22-A01 | Full-range whitespace checking is a required final gate. |
| P22-A02 | Git OIDs are caller claims only; runtime source and controlled-contract content identities are recorded separately, without CWD, Git or environment inference. |

### R2 candidate-side closure trace

This trace records the candidate implementation evidence for the seven
remediation areas identified during independent review. It is not an
independent finding closure or approval.

| Finding | Candidate-side corrective boundary exercised by public tests |
|---|---|
| R2-F01 | The normal evidence-to-record projection is a production gate: it verifies the exact controlled development-contract resource, validates every projected record with the shared public validator, and rejects invalid source disposition or parentage before publication. |
| R2-F02 | A terminal TFTP block creates a finite terminal set: later blocks above it or a different terminal block cause `CONFLICT`; a previously missing lower block can still complete the set. Completed sessions are excluded from active-session eviction. |
| R2-F03 | Corpus mode publishes a per-file `FATAL-INPUT-ERROR` only for an input fault. Tool, schema, controlled-resource, or publication failure aborts the staged transaction and preserves prior owned output. |
| R2-F04 | Active raw TFTP blocks and completed parse payloads have separate configured bounds. The shared evidence limit retains a named stop witness with last-consumed packet/index/offset information and does not claim unconsumed suffixes were scanned. |
| R2-F05 | Parsed, partial, malformed, and opaque first-slice outcomes remain distinct. A non-`PARSED` outcome is a controlled issue and produces exit status `2`, not a successful parser claim. |
| R2-F06 | pcap/pcapng capture length inconsistencies are explicit non-projectable conditions. SPB payload length follows its declared original/snapshot semantics, excluding alignment padding; illegal short or extra SPB bodies are rejected. |
| R2-F07 | The installed noneditable wheel carries the exact controlled contract/schema resources. A real installed `cltav-offline` entry point is exercised from an unrelated working directory; missing or changed controlled resources prevent replacement and use a named tool failure. |

## 6. Follow-on boundary

This evidence may later be consumed through a reviewed evidence manifest.  A
follow-on change, separately reviewed, is required before ownership,
observation verdicts, history update, active execution, integrity establishment,
fault truth, experimental accounting, or any conformance/capability claim can
use it.

# 中文版：CL-TAV 有界离线接入验收证据

| 控制项 | 取值 |
|---|---|
| 报告 ID | `RPT-CLTAV-OFFLINE-INTAKE-2026-001` |
| 授权 | `CR-2026-017`／`DD-041` |
| 工作单 | `WO-CLTAV-OFFLINE-IMPLEMENTATION-2026-001` |
| 候选状态 | Draft PR 候选；需要独立评审 |
| 证据类型 | 离线接入与重建证据，不是符合性结果 |

## 1. 已接受范围与排除项

候选实现只覆盖以下确定性、只读路径：

`捕获 → PACKET-REF → DATAGRAM-RECORD → TRANSFER-RECORD → PROTOCOL-EVENT → 证据索引`。

它接纳调用方提供的捕获文件，产出版本化 JSON 证据，并采用有界资源和事务发布。它**不**发送网络流量、不与 IUT 交互、不执行完整 CL-TAV 闭环、不创建求解器、不建立 CRC 或文件完整性、不作 ARINC 615A PASS／FAIL、不定位根因、不建立运行完整性、不激活 M3、不创建 Project Configuration，也不作能力、认证或实验主张。输出声明 `conformanceVerdict: NOT-EVALUATED`。

实现到合同的映射维护在 [`CLTAV_OFFLINE_IMPLEMENTATION.md`](../../../docs/engineering/CLTAV_OFFLINE_IMPLEMENTATION.md)。该映射复用受控的捕获、重组、传输、记录和验收身份；它不是平行需求包。

## 2. 可复现的本地证据

历史输入为调用方提供的探索性清单 `CLTAV-HISTORICAL-CAPTURES` 版本 `1.0`。本地接入运行前已审计全部 23 份已登记捕获的身份。该运行记录确定性的运行源码快照，而不把调用方给出的 Git OID 当作已核验构建身份：

`ec0bd173836ed285f8c02a2d115e5725033f1af8f0152d2f7f993e611462e345`

调用方给出了 `9cfb35ab1a231228b907f7e5b4af3487aea88c66`，证据将其正确标为 `CLAIMED-UNVERIFIED`。所消费的开发合同为精确快照
`configs/engineering/cltav_development_contracts.json`，SHA-256 为
`3331fadf2786133f161eded9d1fb42066ca58d7dd510ce6e775da1cd89a5aae1`。

已忽略、仅本地保存的 corpus 索引写入 `.cltav-local/`，其 SHA-256 为：

`a8b091d02f98eed6c15704bb3f857bd9eab90abb4f7738cc1c3495c49fdddd0b`

仅记录聚合结果：

| 指标 | 结果 |
|---|---:|
| 已审计的登记捕获身份 | 23 |
| 已发布的 corpus 输出 | 23 份捕获加一个 corpus 索引 |
| `COMPLETE` 重建 | 0 |
| `COMPLETE-WITH-CONTROLLED-ISSUES` 重建 | 23 |
| 运行源码快照 | `ec0bd17…1462e345` |
| 来源声明状态 | `CLAIMED-UNVERIFIED` |

这些数字是接入支持边界，而不是成功率、协议判定、实验分母或关于被捕获系统的结论。尤其是，受控问题被保留而非通过调高限额等方式消除以制造 `COMPLETE` 结果。本报告不向 Git 提交本地根、文件名、地址、载荷、注释、拓扑、时钟特性、配置或根因标签。

## 3. 公开验证入口

```text
python -m pip install -e ".[dev]"
cltav-offline --version
pytest -q tests/unit/test_cltav_offline_intake.py
python scripts/audit_capture_manifest.py --manifest configs/research/cltav_historical_capture_manifest.json --corpus-root <authorized-local-corpus-root>
python -m cltav_offline corpus --manifest configs/research/cltav_historical_capture_manifest.json --corpus-root <authorized-local-corpus-root> --output-dir .cltav-local/offline-intake/corpus [--source-commit <caller-claim-40-hex>]
```

完整仓库门禁序列记录在绑定不可变 PR Head 的 Draft PR 及其 CI 中，包括开发就绪检查器、M1/M2 同步、项目概览同步、baseline 检查器、稿件检查器、全量测试、严格 Python 编译和 `git diff --check`。CI 只使用公开合成夹具，不依赖本地语料。

## 4. 工作单验收追踪

| ID | 证据 |
|---|---|
| E-01 | `CR-2026-017`、`DD-041` 及保留的历史 `CR-2026-016`；全局 executable/M3 门禁继续阻塞。 |
| E-02 | 专用 `codex/cltav-offline-intake-runtime` 分支和隔离工作树；恰好一个 Draft PR 是外部交付物。 |
| E-03 | 已安装的 `cltav-offline` CLI 和端到端合成 pcap/pcapng 测试覆盖完整输出链。 |
| E-04 | `configs/engineering/cltav_offline_intake_evidence.schema.json` 与 `src/cltav_offline/evidence.py` 中的封闭 JSON schema 和运行时 envelope 校验。 |
| E-05 | 整数时间戳表示、section/interface 时钟分离、捕获身份校验和具名截断／link 诊断。 |
| E-06 | 有界 IPv4 重组，含 `COMPLETE`、`GAPPED`、`CONFLICT`、冲突保留、来源链和资源诊断。 |
| E-07 | 覆盖请求/TID 绑定、OACK 的 accepted/defaulted/unknown、短块、零末块、重复块和缺口的生产路径测试。 |
| E-08 | 有界 LCI/LCL/LCS/LUI/LUR/LUS 提取，使用来源约束字段并显式保留未解析余量；不作完整 codec 主张。 |
| E-09 | envelope 声明符合性和传输完整性均为 `NOT-EVALUATED`；不输出所有权、T5、历史、CRC 或主动闭环结果。 |
| E-10 | 流式读取器、声明的资源限额、确定性归一化测试、单文件原子发布、corpus 回滚和具名诊断。 |
| E-11 | 第 2 节汇总清单审计和 23 份捕获的本地运行；这里只保留聚合、非敏感身份证据。 |
| E-12 | 公开合成夹具和 CLI 测试；没有实时网络操作或私有语料 CI 依赖。 |
| E-13 | 本记录及设计／合同映射文档定义论文交接边界，不改动论文主张。 |
| E-14 | 独立评审前必须完成全仓门禁和最终 Head CI；第 3 节列出命令。 |
| E-15 | PR 相对当前 base 的比较隔离本运行时／文档增量；受保护输入继续受控，不为实现便利而重写。 |
| E-16 | Draft PR 必须将本地／远端 CI 绑定到最终 40 位 Head 并保持 Draft；它不激活能力或配置状态。 |

## 5. PR #22 修正关闭证据

下表记录独立评审发现的候选侧修正证据；它不是独立批准。

| 发现项 | 公开测试所覆盖的修正边界 |
|---|---|
| P22-F01 | corpus 发布在 staging 前解析输入、manifest 和输出身份；拒绝相等、子目录、祖先和别名目标、不安全捕获 ID 及非工具拥有目标；回滚保留旧输出。 |
| P22-F02 | TFTP 的终态 `CONFLICT`、协议 `ERROR` 和资源结果不得被后续 DATA 复活；派生完成数据／事件同步撤销；覆盖重复请求、TID 绑定、OACK 上界、defaulted/unknown 选项及回绕。 |
| P22-F03 | 重组和传输关联纳入 section、接口、链路域和 VLAN 上下文；跨域分片／请求不得合并。 |
| P22-F04 | 版本化适配器绑定精确的已接受合同快照，从正常生产证据投影四类已接受记录，并以不伪造值的方式登记无法投影的未知项。生产路径测试会对每个正常投影调用公共记录验证器。 |
| P22-F05 | 发布实际执行声明的 JSON Schema 和跨记录检查；畸形普通／fatal envelope 均在替换前失败。 |
| P22-F06 | 共享保留限额覆盖成功与诊断路径、预留停止记录，并在不保留原始载荷时保留 SHA／索引／偏移／上下文出处。 |
| P22-F07 | PARTIAL、MALFORMED 和 OPAQUE 首切片结果与已解析的应用事件保持区分。 |
| P22-F08 | 短 pcapng 结构输入返回具名受控错误；合法 EPB options 和已支持容器变体继续接纳。 |
| P22-A01 | 全范围空白检查是最终必跑门禁。 |
| P22-A02 | Git OID 仅是调用方声明；运行源码和受控合同内容身份分开记录，不从 CWD、Git 或环境推导。 |

### R2 候选侧关闭追踪

本追踪记录独立评审所列七项修正领域的候选实现证据；它不是独立发现项关闭或批准。

| 发现项 | 公开测试所覆盖的候选侧修正边界 |
|---|---|
| R2-F01 | 普通证据到记录的投影是生产门禁：它核验精确的受控开发合同资源，以共享公共验证器校验每个投影记录，并在发布前拒绝无效的来源处置或父子链。 |
| R2-F02 | TFTP 末块形成有限末端集合：随后出现大于末块的块或不同末块会产生 `CONFLICT`；此前缺失的较低块仍可补齐该集合。已完成会话不参加活跃会话驱逐。 |
| R2-F03 | corpus 模式仅为输入故障发布逐文件 `FATAL-INPUT-ERROR`。工具、schema、受控资源或发布失败会中止 staging 事务并保留原有工具拥有输出。 |
| R2-F04 | 活跃 TFTP 原始块和已完成解析载荷分别具有配置上限。共享证据限额保留带最后已消费包／索引／偏移信息的具名停止见证，且不声称已扫描未消费后缀。 |
| R2-F05 | 已解析、部分解析、畸形和不透明的首切片结果保持区分。非 `PARSED` 结果属于受控问题并返回退出状态 `2`，不构成成功的解析器主张。 |
| R2-F06 | pcap/pcapng 捕获长度不一致是显式不可投影条件。SPB 载荷长度遵从声明的 original/snapshot 语义并排除对齐填充；非法过短或附加 SPB body 会被拒绝。 |
| R2-F07 | 已安装的非 editable wheel 携带精确的受控合同／schema 资源。真实已安装的 `cltav-offline` 入口从无关工作目录运行；缺失或改变的受控资源会阻止替换并返回具名工具失败。 |

## 6. 后继边界

这些证据可在后续通过经评审的 evidence manifest 被消费。所有权、观测判定、历史更新、主动执行、完整性建立、故障真值、实验记账或任何符合性／能力主张使用它之前，都需要单独的后继变更和评审。
