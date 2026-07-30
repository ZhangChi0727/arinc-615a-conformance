# Documentation Map

This directory is organized by decision purpose. Start with the frozen
[`BASELINE.md`](BASELINE.md), not with historical proposals.

| Area | Purpose | Canonical entry |
|---|---|---|
| **Baseline** | What is frozen and authoritative | [`BASELINE.md`](BASELINE.md) |
| **Methodology** | Formal Test-and-Analysis research report | [`study/00_INDEX.md`](study/00_INDEX.md) |
| **Research** | Questions, hypotheses, experiments, claims, evidence | [`research/RESEARCH_PLAN.md`](research/RESEARCH_PLAN.md) |
| **Engineering** | Instrument and verification-pipeline implementation | [`engineering/IMPLEMENTATION_PLAN.md`](engineering/IMPLEMENTATION_PLAN.md) |
| **Management** | Change control and risk governance | [`management/CHANGE_CONTROL.md`](management/CHANGE_CONTROL.md) |
| **Architecture** | End-to-end research and artifact flow | [`architecture.md`](architecture.md) |
| **Requirements** | Applicability, CRS, TP/VC traceability | [`requirements/README.md`](requirements/README.md) |
| **Design** | EFSM, schemas, interfaces, tool qualification notes | [`design/README.md`](design/README.md) |
| **Review** | Gates, decisions, current review records | [`review/REVIEW_GUIDELINE.md`](review/REVIEW_GUIDELINE.md) |
| **Proposals** | Historical or proposed changes | [`proposal/`](proposal/) |
| **Work notes** | Private or project-specific material | [`work/README.md`](work/README.md) |

## Document lifecycle

Use one of these status labels:

| Status | Meaning |
|---|---|
| **Draft** | In development; not a decision source |
| **In Review** | Submitted to a named gate |
| **Approved** | Accepted for its declared artifact version |
| **Frozen Baseline** | Normative until formal change control succeeds |
| **Superseded** | Retained for history; not authoritative |
| **Archived** | Closed record with no active maintenance |

Every controlled document should identify its version, status, owner, and
governing gate. Generated evidence must additionally identify tool versions,
configuration, dataset, and provenance.

## Naming

- `RR-*`: research reports;
- `CRS-*`: controlled conformance requirement sets;
- `TP-*`: Test Purposes;
- `VC-*`: Verification Cases;
- `EXP-*`: registered experiments;
- `GR-*`: gate review records;
- `DD-*`: durable design or research decisions;
- `CR-*`: baseline change requests.

---

## 中文版

文档按决策用途组织：基线说明冻结内容；方法报告定义正式语义；研究目录管理问题、实验和主张；工程目录管理工具实现；需求目录管理适用性、CRS 和追踪；设计目录管理带时钟 EFSM、schema 和接口；评审/管理目录管理门禁、决策、变更和风险。历史提案不是当前权威。

受控文档状态包括 Draft、In Review、Approved、Frozen Baseline、Superseded 和 Archived。命名采用 RR、CRS、TP、VC、EXP、GR、DD 和 CR 前缀。关键文档在英文正文末尾直接附中文版，不建立平行语言文件。
