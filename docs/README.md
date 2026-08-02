# Documentation Map

This directory is organized by decision purpose. Start with the lifecycle and
authority declared in [`BASELINE.md`](BASELINE.md), not with historical
proposals.

| Area | Purpose | Canonical entry |
|---|---|---|
| **Baseline** | What is approved/effective and authoritative | [`BASELINE.md`](BASELINE.md) |
| **Methodology** | Formal Test-and-Analysis method, semantics, and controlled report | [`methodology/00_INDEX.md`](methodology/00_INDEX.md) |
| **Research** | Questions, hypotheses, experiments, claims, evidence | [`research/RESEARCH_PLAN.md`](research/RESEARCH_PLAN.md) |
| **Engineering** | Instrument and verification-pipeline implementation | [`engineering/IMPLEMENTATION_PLAN.md`](engineering/IMPLEMENTATION_PLAN.md) |
| **Publication** | Manuscripts, figures, notes, and replication reports | [`../thesis/README.md`](../thesis/README.md) |
| **Tutorials** | Downstream teaching and reproducible instance walkthroughs | [`../tutorial/README.md`](../tutorial/README.md) |
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

# 中文版

文档按决策用途组织：基线说明冻结内容；`docs/methodology/` 定义正式方法语义；`docs/research/` 管理问题、实验、分析和主张；`docs/engineering/`、`src/` 与 `tests/` 管理工程实现；`thesis/` 承载受主张—证据门约束的出版材料；`tutorial/common/` 与 `tutorial/arinc615a/` 仅作为下游教学和复现路径。需求目录管理适用性、CRS 和追踪；设计目录管理带时钟 EFSM、schema 和接口；评审/管理目录管理门禁、决策、变更和风险。历史提案不是当前权威。

## 文档生命周期

受控文档状态包括 Draft、In Review、Approved、Frozen Baseline、Superseded 和 Archived。命名采用 RR、CRS、TP、VC、EXP、GR、DD 和 CR 前缀。关键文档在英文正文末尾直接附中文版，不建立平行语言文件。

每份受控文档应记录版本、状态、负责人和治理门禁；生成证据还必须记录工具版本、配置、数据集和来源。

## 命名

`RR-*` 表示研究报告，`CRS-*` 表示受控符合性需求集，`TP-*` 表示测试目的，`VC-*` 表示验证用例，`EXP-*` 表示注册实验，`GR-*` 表示门禁评审记录，`DD-*` 表示持久设计/研究决策，`CR-*` 表示基线变更请求。
