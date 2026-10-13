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
`CLTAV-HISTORICAL-CAPTURES` version `1.0`.  Its identity audit covered all 23
registered captures before the local intake run.  The runtime source used for
that run was immutable commit
`b6f4ac216d51e55c7f34b4747bf2f0a7320a75ed`; the later serial integration of
the parallel paper line does not alter `src/cltav_offline/`.

The ignored, local-only corpus index was written under `.cltav-local/` and has
SHA-256:

`6f195b513824865afa5037cb72da59ae3acc99a894c65c6cfb37652912c53bac`

Aggregate result only:

| Measure | Result |
|---|---:|
| Registered capture identities audited | 23 |
| Corpus outputs published | 23 captures plus one corpus index |
| `COMPLETE` reconstructions | 2 |
| `COMPLETE-WITH-CONTROLLED-ISSUES` reconstructions | 21 |
| `RESOURCE-EVIDENCE-RECORD-LIMIT` diagnostics | 21 |
| `TRUNCATED-IPV4-PAYLOAD` diagnostics | 2 |

These figures are an intake-support boundary, not a success rate, a protocol
verdict, an experimental denominator, or a statement about the captured
systems.  No local root, filename, address, payload, annotation, topology,
clock characterization, configuration, or root-cause label is stored in Git.

## 3. Public verification entry points

```text
python -m pip install -e ".[dev]"
cltav-offline --version
pytest -q tests/unit/test_cltav_offline_intake.py
python scripts/audit_capture_manifest.py --manifest configs/research/cltav_historical_capture_manifest.json --corpus-root <authorized-local-corpus-root>
python -m cltav_offline corpus --manifest configs/research/cltav_historical_capture_manifest.json --corpus-root <authorized-local-corpus-root> --output-dir .cltav-local/offline-intake/corpus --source-commit <immutable-40-hex-head>
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

## 5. Follow-on boundary

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

历史输入为调用方提供的探索性清单 `CLTAV-HISTORICAL-CAPTURES` 版本 `1.0`。本地接入运行前已审计全部 23 份已登记捕获的身份。该运行使用的运行源码为不可变提交
`b6f4ac216d51e55c7f34b4747bf2f0a7320a75ed`；随后串行集成的并行论文线没有改动 `src/cltav_offline/`。

已忽略、仅本地保存的 corpus 索引写入 `.cltav-local/`，其 SHA-256 为：

`6f195b513824865afa5037cb72da59ae3acc99a894c65c6cfb37652912c53bac`

仅记录聚合结果：

| 指标 | 结果 |
|---|---:|
| 已审计的登记捕获身份 | 23 |
| 已发布的 corpus 输出 | 23 份捕获加一个 corpus 索引 |
| `COMPLETE` 重建 | 2 |
| `COMPLETE-WITH-CONTROLLED-ISSUES` 重建 | 21 |
| `RESOURCE-EVIDENCE-RECORD-LIMIT` 诊断 | 21 |
| `TRUNCATED-IPV4-PAYLOAD` 诊断 | 2 |

这些数字是接入支持边界，而不是成功率、协议判定、实验分母或关于被捕获系统的结论。本报告不向 Git 提交本地根、文件名、地址、载荷、注释、拓扑、时钟特性、配置或根因标签。

## 3. 公开验证入口

```text
python -m pip install -e ".[dev]"
cltav-offline --version
pytest -q tests/unit/test_cltav_offline_intake.py
python scripts/audit_capture_manifest.py --manifest configs/research/cltav_historical_capture_manifest.json --corpus-root <authorized-local-corpus-root>
python -m cltav_offline corpus --manifest configs/research/cltav_historical_capture_manifest.json --corpus-root <authorized-local-corpus-root> --output-dir .cltav-local/offline-intake/corpus --source-commit <immutable-40-hex-head>
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

## 5. 后继边界

这些证据可在后续通过经评审的 evidence manifest 被消费。所有权、观测判定、历史更新、主动执行、完整性建立、故障真值、实验记账或任何符合性／能力主张使用它之前，都需要单独的后继变更和评审。
