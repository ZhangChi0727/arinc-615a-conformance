# Increment Assurance Record Template

| Field | Required value |
|---|---|
| Record ID | `IAR-<increment>` |
| Product/version | named engineering or research increment |
| Source commit | immutable Git commit |
| Governing baseline | exact baseline ID |
| External method binding | binding ID and immutable MethodDefinitionCommit |
| Profile / Product Binding | temporary or stable IDs and versions |
| Project Configuration | controlled ID/version or `NOT YET ESTABLISHED` |
| Inputs | requirement, applicability, CRS, verification objective, model, VCS, tool/config/environment IDs |
| Evidence | test results, raw/derived evidence, execution evidence manifest, test conformity, problem closure IDs |
| Conformance | test article, setup, and procedure conformity status; tool qualification status |
| Review state | gate records, open deviations, accepted risks |
| Release decision | accepted, rejected, conditional, or not submitted |
| Compatibility / evaluation | `NOT-DETERMINED` / `NOT-EXERCISED` unless separately reviewed evidence changes them |

## Required assurance narrative

The record states the increment objective; changed controlled objects; tests
and analyses performed; results and failures; evidence provenance; unresolved
findings; affected claims; rollback or migration needs; and the exact gate
decision. Test names and comments must describe the behavior actually exercised.
A claimed boundary or rollover requires evidence that reaches that boundary or
an explicit, reviewed test seam.

## README status integration

An Increment Assurance Record is developer-facing and does not create a
separate reader report or HANDOFF. In the same pull request, an accepted
increment updates `project-status.json` and the generated README status block,
including the increment, current stop, next step and unchanged boundaries.
README links the underlying evidence manifest and gate decision where the
accepted state depends on them.

---

# 中文版

| 字段 | 必填内容 |
|---|---|
| 记录 ID | `IAR-<increment>` |
| 产品/版本 | 具名工程或研究增量 |
| 源提交 | 不可变 Git 提交 |
| 治理基线 | 精确基线 ID |
| 外部方法绑定 | 绑定 ID 与不可变 MethodDefinitionCommit |
| Profile / Product Binding | 临时或稳定 ID 及版本 |
| Project Configuration | 受控 ID/版本或 `NOT YET ESTABLISHED` |
| 输入 | 需求、适用性、CRS、验证目标、模型、VCS、工具/配置/环境 ID |
| 证据 | 测试结果、原始/派生证据、执行证据清单、测试件符合性与问题关闭 ID |
| 符合性 | 测试件、装置与规程符合性状态；工具鉴定状态 |
| 评审状态 | 门禁记录、开放偏差和已接受风险 |
| 发布决定 | 接受、拒绝、有条件接受或未提交 |
| 兼容性 / 评价 | 除非独立受评审证据改变，否则为 `NOT-DETERMINED` / `NOT-EXERCISED` |

## 必需保证叙述

记录必须说明增量目标、变更的受控对象、执行的测试和分析、结果与失败、证据来源、未解决
发现、受影响主张、回退或迁移需求以及精确门禁决定。测试名称和注释必须描述实际执行的
行为。若主张某个边界或编号回卷，证据必须真正到达该边界，或使用显式且经评审的测试缝。

## README 状态集成

增量保证记录面向开发者，不创建独立 reader report 或 HANDOFF。已接受增量必须在同一 PR
更新 `project-status.json` 和生成的 README 状态区块，记录增量、当前停点、下一步及保持
不变的边界；当已接受状态依赖底层证据清单和门禁决定时，README 必须链接这些记录。
