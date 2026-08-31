# Tutorial Control

This document controls tutorial production and publication. Current project
state is linked from the [root README](../../README.md), not duplicated here.

## 1. Product lines

| Product | Scope | Source |
|---|---|---|
| Common Verification Tutorial | protocol-independent method concepts and exercises | [`COMMON_TUTORIAL_PLAN.md`](sources/COMMON_TUTORIAL_PLAN.md) |
| ARINC 615A Tutorial | instance walkthrough using only releasable project material | [`ARINC615A_TUTORIAL_PLAN.md`](sources/ARINC615A_TUTORIAL_PLAN.md) |

## 2. Dependency and traceability rule

Tutorials cite versioned method, research and engineering artifacts. They may
explain a released baseline and tool behavior but never become a normative
source, replace a review record or import proprietary protocol text.

Each tutorial release declares `normative: false`, `explains_baseline`,
`explains_tool_release` and the required configuration/evidence prerequisites.

## 3. Promotion and feedback rule

Tutorial clarity findings return to the owning workstream as issues or change
proposals. Tutorial examples cannot promote compatibility, configuration,
evaluation, certification or RQ8 state.

# 中文版

本文档控制教程生产与发布。当前项目状态从[根 README](../../README.md)进入，不在此重复。

## 1. 产品线

| 产品 | 范围 | 来源 |
|---|---|---|
| 通用验证教程 | 与协议无关的方法概念及练习 | [`COMMON_TUTORIAL_PLAN.md`](sources/COMMON_TUTORIAL_PLAN.md) |
| ARINC 615A 教程 | 仅使用可发布项目材料的实例讲解 | [`ARINC615A_TUTORIAL_PLAN.md`](sources/ARINC615A_TUTORIAL_PLAN.md) |

## 2. 依赖与追踪规则

教程引用版本化的方法、研究和工程产物。教程可以解释已发布 baseline 和工具行为，但不能
成为规范来源、替代评审记录或引入专有协议原文。

每次教程发布声明 `normative: false`、`explains_baseline`、
`explains_tool_release` 以及必要的配置／证据前置条件。

## 3. 晋级与反馈规则

教程清晰度问题通过 issue 或变更提案反馈给所属工作流。教程示例不能晋级兼容性、配置、
评价、认证或 RQ8 状态。
