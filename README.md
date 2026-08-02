# ARINC 615A Conformance Verification

This repository develops an auditable Test-and-Analysis methodology and a
dual-role engineering instrument for scoped ARINC 615A conformance
verification. Review and Inspection gates control the artifacts and claims
produced by both paths.

## Current reader release

The single reader-facing entry for this update is the bilingual
[`RPT-2026-002 Information Architecture and Reporting Baseline`](artifacts/reports/current/RPT-2026-002_information_architecture_v4.2.1.md).
It explains what is established, what remains unearned, and where the
supporting controlled records reside.

The frozen mathematical and methodological content remains
[`RR-2026-001 v4.2`](docs/research/methodology/RR-2026-001_test_analysis_conformance_methodology.md).
The proposed `RB-2026-001-v4.2.1` changes repository information architecture
and reporting control only; it does not change equations, timed semantics,
assurance tiers, or claim rules.

## Developer control entry points

| Product line | Control document | Responsibility |
|---|---|---|
| Project governance | [`PROJECT_CONTROL.md`](docs/control/PROJECT_CONTROL.md) | baselines, contracts, changes, gates, risks, releases, and reporting |
| Methodology research and publication | [`RESEARCH_CONTROL.md`](docs/research/RESEARCH_CONTROL.md) | method, experiments, claims, and publication inputs |
| Engineering instrument | [`ENGINEERING_CONTROL.md`](docs/engineering/ENGINEERING_CONTROL.md) | implementation increments, tests, schemas, and evidence production |
| Verification tutorials | [`TUTORIAL_CONTROL.md`](docs/tutorial/TUTORIAL_CONTROL.md) | protocol-independent and ARINC 615A learning products |

These four documents are navigation and control surfaces. Atomic records such
as change requests, decisions, gate records, experiment protocols, evidence
manifests, and increment assurance records remain separate and versioned.

## Repository structure

```text
README.md                 only reader-facing document at repository root
pyproject.toml             Python package/build/test metadata (machine-facing)
.github/ and .gitignore    automation and repository configuration
src/                       verification instrument source
tests/                     executable engineering checks
configs/                   controlled machine-readable inputs and templates
scripts/                   maintenance and validation automation
docs/                      developer control plane
  control/                 project governance and shared contracts
  research/                methodology, experiments, claims, publication inputs
  engineering/             implementation control, design, increments
  tutorial/                tutorial control and source plans
artifacts/                 all reader-facing and generated deliverables
  reports/current/         exactly one current reader update
  reports/archive/         superseded reader reports
  tutorials/               published tutorial outputs
  releases/                distributable release packages
  evidence/                generated evidence packages (normally not committed)
local-references/          ignored local research inputs; never published
```

`pyproject.toml` remains at the root because Python packaging, editable
installation, test discovery, and development tools locate project metadata
there by convention. It is executable configuration, not a reader report.

## Quick start

```bash
python -m pip install -e ".[dev]"
python -m a615a_sim.cli --help
pytest
python scripts/check_repo_baseline.py
```

Do not commit proprietary ARINC or employer-only ICD text. A passing test suite
is engineering evidence, not by itself a conformance proof or a scientific
result.

---

# 中文版

本仓库研究并实现一种可审计的 ARINC 615A 测试—分析符合性验证方法。测试与分析相互补充，
评审与检查门控制二者产生的产物及可发布主张。

## 当前读者发布

本次更新唯一的面向读者入口是双语
[`RPT-2026-002 信息架构与报告基线`](artifacts/reports/current/RPT-2026-002_information_architecture_v4.2.1.md)。
它说明已经建立的内容、尚未获得的保证以及支撑性受控记录的位置。

冻结的数学与方法论内容仍为
[`RR-2026-001 v4.2`](docs/research/methodology/RR-2026-001_test_analysis_conformance_methodology.md)。
候选 `RB-2026-001-v4.2.1` 只改变仓库信息架构和报告控制，不修改公式、时序语义、
保证层级或主张规则。

## 开发者控制入口

| 产品支线 | 控制文档 | 职责 |
|---|---|---|
| 项目治理 | [`PROJECT_CONTROL.md`](docs/control/PROJECT_CONTROL.md) | 基线、契约、变更、门禁、风险、发布和报告 |
| 方法论研究与出版 | [`RESEARCH_CONTROL.md`](docs/research/RESEARCH_CONTROL.md) | 方法、实验、主张和出版输入 |
| 工程工具 | [`ENGINEERING_CONTROL.md`](docs/engineering/ENGINEERING_CONTROL.md) | 实现增量、测试、schema 和证据生产 |
| 验证教程 | [`TUTORIAL_CONTROL.md`](docs/tutorial/TUTORIAL_CONTROL.md) | 通用及 ARINC 615A 学习产品 |

这四份文档是导航和控制界面。变更请求、设计决策、门禁记录、实验方案、证据清单和增量
保证记录等原子记录继续独立保存并受版本控制。

## 仓库结构

```text
README.md                 根目录唯一面向读者的文档
pyproject.toml             面向机器的 Python 包、构建和测试元数据
.github/ 和 .gitignore     自动化与仓库配置
src/                       验证工具源码
tests/                     可执行工程检查
configs/                   受控机器可读输入及模板
scripts/                   维护与验证自动化
docs/                      面向开发者的控制平面
  control/                 项目治理及共享契约
  research/                方法论、实验、主张和出版输入
  engineering/             实现控制、设计和增量
  tutorial/                教程控制及源计划
artifacts/                 全部面向读者及生成的交付物
  reports/current/         唯一当前读者更新
  reports/archive/         已被替代的读者报告
  tutorials/               已发布教程产物
  releases/                可分发发布包
  evidence/                生成证据包（通常不提交）
local-references/          被忽略的本地研究输入，不发布
```

`pyproject.toml` 留在根目录，是因为 Python 打包、可编辑安装、测试发现和开发工具按约定
从项目根查找这些元数据。它是可执行配置，不是面向读者的报告。

## 快速开始

```bash
python -m pip install -e ".[dev]"
python -m a615a_sim.cli --help
pytest
python scripts/check_repo_baseline.py
```

不得提交专有 ARINC 或雇主内部 ICD 原文。测试套件通过属于工程证据，本身既不是符合性
证明，也不是科学研究结果。
