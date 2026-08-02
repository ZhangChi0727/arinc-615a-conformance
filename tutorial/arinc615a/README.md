# ARINC 615A Conformance Verification Tutorial

| Field | Value |
|---|---|
| **Tutorial type** | `arinc615a` |
| **Status** | Planned architecture; executable lessons await controlled artifacts |
| **Normative** | No |
| **Explains baseline** | RB-2026-001-v4.2 approved; effective on merge of PR #6 |
| **Explains tool release** | Not assigned |

## Scope and prerequisites

This path instantiates the common verification concepts for the scoped ARINC
615A project. It consumes an approved applicability declaration, CRS/model/VCS
versions, a released instrument, stable examples, and evidence manifests. It
does not reproduce proprietary standard text and does not replace the
authoritative methodology or engineering documentation.

## Planned walkthrough

1. select the common prerequisites for Test, Analysis, Review, and Inspection;
2. identify the ARINC 615A roles, services, observation boundary, and explicit
   non-claims;
3. read a controlled applicability item and CRS entry;
4. follow requirement-to-model-to-TP-to-VC traceability;
5. inspect discrete and timed oracle semantics and the measurement-error budget;
6. execute one VC with a pinned tool/configuration/environment combination;
7. interpret PASS, FAIL, INCONCLUSIVE, and ERROR from its immutable evidence;
8. reproduce a coverage or finite-fault-domain result without overstating it.

## Exercise trace record

Every executable exercise records `tutorial_id`, `explains_baseline`,
`explains_tool_release`, applicability/CRS/model/VCS versions, IUT and
environment IDs, example artifact IDs, evidence-manifest IDs, and applicable
gate records. A missing required identifier makes the exercise a conceptual
example, not a reproducibility claim.

The current local verification-plan notes remain source material until their
claims, terminology, and examples are reconciled with these contracts.

---

# 中文版

| 字段 | 内容 |
|---|---|
| **教程类型** | `arinc615a` |
| **状态** | 架构已规划；可执行课程等待受控产物 |
| **规范性** | 否 |
| **解释基线** | RB-2026-001-v4.2 已批准；PR #6 合并后生效 |
| **解释工具发布** | 尚未指定 |

## 范围与先修条件

本路径把通用验证概念实例化到限定范围的 ARINC 615A 项目。它消费已批准适用性声明、CRS/模型/VCS 版本、已发布工具、稳定示例和证据清单。它不复制专有标准原文，也不取代权威方法论或工程文档。

## 计划讲解路径

1. 选择 Test、Analysis、Review 和 Inspection 所需通用先修课程；
2. 识别 ARINC 615A 角色、服务、观测边界和明确非主张；
3. 阅读受控适用性条目和 CRS 条目；
4. 跟踪需求—模型—TP—VC 关系；
5. 检查离散/时序 oracle 语义和测量误差预算；
6. 使用固定工具/配置/环境组合执行一个 VC；
7. 从不可变证据解释 PASS、FAIL、INCONCLUSIVE 和 ERROR；
8. 复现覆盖或有限故障域结果且不夸大主张。

## 练习追踪记录

每个可执行练习记录 `tutorial_id`、`explains_baseline`、`explains_tool_release`、适用性/CRS/模型/VCS 版本、IUT 与环境 ID、示例产物 ID、证据清单 ID 和适用门禁记录。缺少必需标识时，该练习只能称为概念示例，不能称为复现主张。

当前本地验证计划笔记继续作为素材，直至其主张、术语和示例与上述契约完成协调。
