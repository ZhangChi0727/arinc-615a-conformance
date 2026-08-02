# ARINC 615A Test-and-Analysis Conformance Verification

Research and engineering repository for an auditable ARINC 615A conformance
verification methodology and its dual-role experimental instrument.

The repository is governed by methodology baseline
[`RB-2026-001-v4.2`](docs/BASELINE.md), approved by
`GR-PR6-RB-2026-001-v4.2` and frozen only after PR #6 is merged. The baseline
defines two complementary paths:

- **Test:** derive and execute requirement-based Verification Cases;
- **Analysis:** evaluate traceability, discrete and timed coverage, bounded
  fault detection, measurement uncertainty, repeated-run dependence, and diagnosis.

Review and Inspection gates control the artifacts and claims produced by both
paths.

## Start here

| Need | Document |
|---|---|
| Understand baseline status and authority | [`docs/BASELINE.md`](docs/BASELINE.md) |
| Read the methodology | [Bilingual report: English + 中文](docs/methodology/RR-2026-001_test_analysis_conformance_methodology.md) |
| See the integrated program | [`PROJECT_PLAN.md`](PROJECT_PLAN.md) |
| Plan research and experiments | [`docs/research/RESEARCH_PLAN.md`](docs/research/RESEARCH_PLAN.md) |
| Implement the instrument | [`docs/engineering/IMPLEMENTATION_PLAN.md`](docs/engineering/IMPLEMENTATION_PLAN.md) |
| Learn verification foundations | [`tutorial/common/README.md`](tutorial/common/README.md) |
| Follow the ARINC 615A instance path | [`tutorial/arinc615a/README.md`](tutorial/arinc615a/README.md) |
| Navigate all documents | [`docs/README.md`](docs/README.md) |

## Repository structure

```text
src/                    verification instrument
tests/                  unit, contract, integration, and scenarios
configs/                schemas, cases, and controlled examples
artifacts/              local/generated experimental evidence
docs/
  methodology/          authoritative method and formal semantics
  research/             research, experiment, and claim control
  engineering/          implementation plan
  requirements/         applicability, CRS, TP, VC, traceability
  design/               clock-augmented EFSM, evidence, and software design
  review/               gates, decisions, and review records
  management/           change and risk control
  proposal/             historical/proposed changes
thesis/                 publication drafts, notes, and figures
tutorial/
  common/               protocol-independent verification foundations
  arinc615a/            version-pinned ARINC 615A instance walkthroughs
```

## Current state

| Area | State |
|---|---|
| Methodology | v4.2 approved with deterministic timed-conformance semantics; effective/frozen on merge of PR #6 |
| Empirical assurance | T0–T3 not yet earned; evidence work starts at RG0/RG1 |
| Engineering | TFTP core skeleton and tests exist; 48 tests currently pass |
| Repository governance | Program, research, implementation, experiment, risk, and change plans established |

## Quick start

```bash
python -m pip install -e ".[dev]"
python -m a615a_sim.cli --help
pytest
```

## Evidence and confidentiality

- Do not commit proprietary ARINC or employer-only ICD text.
- Use stable source references and hashes in public CRS artifacts.
- Keep project-specific names and private notes under `docs/work/`.
- Do not call a result “conformance proof,” “diagnostic coverage,” or a
  “conformance probability” unless the relevant claim and gate requirements are
  satisfied.

---

# 中文版

本仓库用于研究并实现可审计的 ARINC 615A 测试—分析符合性验证方法。当前受
[`RB-2026-001-v4.2`](docs/BASELINE.md)
治理；v4.2 已由 `GR-PR6-RB-2026-001-v4.2` 批准，只有 PR #6 合并后才生效并冻结：

- **测试路径：** 从适用需求导出并执行验证用例，产生离散判定、带时戳迹和测量证据；
- **分析路径：** 评价追踪、离散/时序覆盖、有限故障检测、测量不确定性、运行依赖和诊断；
- **评审与检查：** 控制需求、带时钟模型、oracle、时钟/误差预算、证据和发布主张。

## 从这里开始

阅读顺序：先看[基线声明](docs/BASELINE.md)，再看[中英合并研究报告](docs/methodology/RR-2026-001_test_analysis_conformance_methodology.md)，随后按需进入[项目计划](PROJECT_PLAN.md)、[研究计划](docs/research/RESEARCH_PLAN.md)、[工程实施计划](docs/engineering/IMPLEMENTATION_PLAN.md)、[通用验证教程](tutorial/common/README.md)和[ARINC 615A 实例教程](tutorial/arinc615a/README.md)。

## 仓库结构

```text
src/                    验证工具
tests/                  单元、契约、集成和场景测试
configs/                schema、用例和受控示例
artifacts/              本地/生成的实验证据
docs/                   方法论、研究、工程、需求、设计、评审和管理
thesis/                 论文草稿、笔记和图表
tutorial/common/        协议无关的验证基础
tutorial/arinc615a/     绑定版本的 ARINC 615A 实例教程
```

## 当前状态

方法论 v4.2 已批准、等待 PR #6 合并生效；T0–T3 经验保证尚未获得；当前工程骨架的 48 项测试通过；项目、研究、实施、实验、风险和变更计划已建立。

## 快速开始

```bash
python -m pip install -e ".[dev]"
python -m a615a_sim.cli --help
pytest
```

## 证据与保密

公开仓库不得提交专有 ARINC 或雇主 ICD 原文。没有通过相应证据门时，不得使用“全面证明符合”“诊断覆盖率”或“符合性概率”等超范围措辞。
