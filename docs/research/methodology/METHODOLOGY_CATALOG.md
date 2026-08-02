# Methodology Index

This directory contains the authoritative Test-and-Analysis methodology and its
formal semantics. The v4.2 package is approved by
`GR-PR6-RB-2026-001-v4.2` and becomes frozen only after PR #6 is merged.
Research plans, engineering internals,
publication drafts, and tutorials are intentionally outside this directory.

## Controlled report

| ID | Title | Language | Status |
|---|---|---|---|
| RR-2026-001 | [A Test-and-Analysis Methodology for ARINC 615A Conformance Verification / 面向 ARINC 615A 符合性验证的测试—分析方法论](RR-2026-001_test_analysis_conformance_methodology.md) | English + 中文 | v4.2 effective and frozen through PR #6 |

Baseline declaration: [`../../control/baselines/RB-2026-001-v4.2.md`](../../control/baselines/RB-2026-001-v4.2.md)

Controlled terminology: [`../../control/contracts/TERMINOLOGY.md`](../../control/contracts/TERMINOLOGY.md)

Dependency and traceability contracts: [`../../control/contracts/DOMAIN_BOUNDARIES.md`](../../control/contracts/DOMAIN_BOUNDARIES.md)

## Downstream consumers

| Consumer | Canonical entry | Permitted use |
|---|---|---|
| Research and experiments | [`../RESEARCH_CONTROL.md`](../RESEARCH_CONTROL.md) | register and evaluate bounded propositions against this method version |
| Engineering implementation | [`../../engineering/ENGINEERING_CONTROL.md`](../../engineering/ENGINEERING_CONTROL.md) | implement controlled models, cases, verdicts, and evidence interfaces |
| Publication | [`../publication/PUBLICATION_GUIDE.md`](../publication/PUBLICATION_GUIDE.md) | report only gate-supported methods, results, and limitations |
| Common tutorial | [`../../tutorial/sources/COMMON_TUTORIAL_PLAN.md`](../../tutorial/sources/COMMON_TUTORIAL_PLAN.md) | teach reusable verification concepts without normative authority |
| ARINC 615A tutorial | [`../../tutorial/sources/ARINC615A_TUTORIAL_PLAN.md`](../../tutorial/sources/ARINC615A_TUTORIAL_PLAN.md) | reproduce a named baseline/tool/example combination |

Downstream artifacts cite the report version and applicable gate record. They
cannot alter this directory by interpretation; changes return through formal
change control.

---

# 中文版

本目录只承载权威测试—分析方法论及其形式语义。v4.2 已由 `GR-PR6-RB-2026-001-v4.2` 批准，只有 PR #6 合并后才会生效并冻结。研究计划、工程内部结构、出版草稿和教程均有意放在本目录之外。

## 受控报告

| ID | 标题 | 语言 | 状态 |
|---|---|---|---|
| RR-2026-001 | [面向 ARINC 615A 符合性验证的测试—分析方法论 / A Test-and-Analysis Methodology for ARINC 615A Conformance Verification](RR-2026-001_test_analysis_conformance_methodology.md) | English + 中文 | v4.2 已经 PR #6 生效并冻结 |

基线声明：[`../../control/baselines/RB-2026-001-v4.2.md`](../../control/baselines/RB-2026-001-v4.2.md)

受控术语：[`../../control/contracts/TERMINOLOGY.md`](../../control/contracts/TERMINOLOGY.md)

依赖与追踪契约：[`../../control/contracts/DOMAIN_BOUNDARIES.md`](../../control/contracts/DOMAIN_BOUNDARIES.md)

## 下游消费者

| 消费者 | 权威入口 | 允许用途 |
|---|---|---|
| 研究与实验 | [`../RESEARCH_CONTROL.md`](../RESEARCH_CONTROL.md) | 针对本方法版本注册并评价有边界的研究命题 |
| 工程实现 | [`../../engineering/ENGINEERING_CONTROL.md`](../../engineering/ENGINEERING_CONTROL.md) | 实现受控模型、用例、判定和证据接口 |
| 出版 | [`../publication/PUBLICATION_GUIDE.md`](../publication/PUBLICATION_GUIDE.md) | 仅报告门禁支持的方法、结果和局限 |
| 通用教程 | [`../../tutorial/sources/COMMON_TUTORIAL_PLAN.md`](../../tutorial/sources/COMMON_TUTORIAL_PLAN.md) | 教授可复用验证概念，但不具有规范权威 |
| ARINC 615A 教程 | [`../../tutorial/sources/ARINC615A_TUTORIAL_PLAN.md`](../../tutorial/sources/ARINC615A_TUTORIAL_PLAN.md) | 复现具名基线、工具和示例组合 |

下游产物必须引用报告版本和适用门禁记录。下游解释不能修改本目录；任何变更必须通过正式变更控制返回上游。
