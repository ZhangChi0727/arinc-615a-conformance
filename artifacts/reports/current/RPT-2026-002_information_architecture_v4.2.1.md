# RPT-2026-002 — Information Architecture and Reporting Baseline

| Field | Value |
|---|---|
| Audience | readers, reviewers, engineering and research stakeholders |
| Update | repository information architecture and reporting system |
| Method basis | RR-2026-001 v4.2, unchanged |
| Candidate package | RB-2026-001-v4.2.1 |
| Status | Candidate reader release; independent review pending |

Controlled sources: [candidate baseline](../../../docs/control/baselines/RB-2026-001-v4.2.1.md),
[change request](../../../docs/control/changes/CR-2026-003.md),
[project control](../../../docs/control/PROJECT_CONTROL.md), and
[v4.2 release record](../../../docs/control/baselines/BRR-RB-2026-001-v4.2.md).

## 1. Executive result

The repository now separates its reader release surface from its developer
control plane. The root README points to this single, self-contained update;
all other reader deliverables live under `artifacts/`. Project governance,
methodology research, engineering, and tutorials each have one control entry,
while evidence-bearing records remain atomic and traceable.

## 2. What changed

Root planning documents and directory README files were replaced by four
developer control entries. Baselines, contracts, change requests, decisions,
gate records, experiments, designs, and historical reviews were relocated into
their owning product lines. The existing Phase 0 HTML report was retained in
the report archive.

## 3. Reporting system

An engineering or research increment first produces controlled internal
records: requirement and design versions, tests, evidence manifests, analyses,
review findings, and gate decisions. A reader update then selects and explains
those records in one report. The report cites stable IDs and versions, states
unearned claims, and never substitutes narrative for source evidence.

`artifacts/reports/current/` contains one current reader report. When a new
reader update is released, the preceding report moves unchanged to
`artifacts/reports/archive/`. Tutorials and software release packages use their
own artifact areas but follow the same provenance rule.

## 4. Methodological continuity

No equation, timing obligation, robust timing verdict, T0–T3 assurance tier,
RG0–RG6 review gate, or G0–G7 evidence gate is changed. The authoritative
mathematical report remains RR-2026-001 v4.2. This update changes how governed
work becomes discoverable and reportable.

## 5. Current limits and next gate

The new arrangement does not claim empirical conformance, mutation adequacy,
diagnostic performance, or calibrated probability. Those claims remain
unearned until their named experiments and gates pass. Before v4.2.1 freezes,
an independent review must confirm complete relocation, link integrity,
bilingual parity, validator coverage, and absence of semantic methodology
change.

---

# 中文版

| 字段 | 内容 |
|---|---|
| 读者 | 读者、评审者、工程及研究相关方 |
| 更新 | 仓库信息架构与报告体系 |
| 方法基础 | RR-2026-001 v4.2，未修改 |
| 候选包 | RB-2026-001-v4.2.1 |
| 状态 | 候选读者发布；等待独立评审 |

受控来源：[候选基线](../../../docs/control/baselines/RB-2026-001-v4.2.1.md)、
[变更请求](../../../docs/control/changes/CR-2026-003.md)、
[项目控制](../../../docs/control/PROJECT_CONTROL.md)和
[v4.2 发布记录](../../../docs/control/baselines/BRR-RB-2026-001-v4.2.md)。

## 1. 执行结果

仓库现已分离面向读者的发布面与面向开发者的控制平面。根 README 指向这一份自包含
更新；其它读者交付物全部位于 `artifacts/`。项目治理、方法论研究、工程和教程各有一个
控制入口，而承载证据的记录继续保持原子性与可追踪性。

## 2. 变更内容

根目录计划文档和各目录 README 已由四个开发者控制入口替代。基线、契约、变更请求、
决策、门禁记录、实验、设计和历史评审被迁移到其所属产品支线。既有 Phase 0 HTML
报告保留在报告归档区。

## 3. 报告体系

工程或研究增量首先产生受控内部记录：需求与设计版本、测试、证据清单、分析、评审发现
及门禁决定。随后，一次读者更新用一份报告选择并解释这些记录。报告引用稳定 ID 和版本，
声明尚未获得的主张，并且绝不用叙述替代源证据。

`artifacts/reports/current/` 只包含一份当前读者报告。新的读者更新发布时，上一份报告原样
迁入 `artifacts/reports/archive/`。教程和软件发布包使用各自的产物区域，但遵循相同的来源规则。

## 4. 方法论连续性

本次更新不改变任何公式、时序义务、稳健时序判定、T0–T3 保证层级、RG0–RG6 评审门或
G0–G7 证据门。权威数学报告仍为 RR-2026-001 v4.2。本次更新只改变受治理工作如何被发现
和汇总为报告。

## 5. 当前边界与下一门禁

新结构不主张已经获得经验符合性、变异充分性、诊断性能或校准概率。这些主张在具名实验
与门禁通过前仍未获得。v4.2.1 冻结前，独立评审必须确认迁移完整、链接有效、中英文对等、
校验器覆盖充分且方法论语义没有变化。
