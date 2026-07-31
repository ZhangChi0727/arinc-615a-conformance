# Methodology Index

This directory contains the authoritative Test-and-Analysis methodology and its
formal semantics. The proposed v4.2 package remains in review and becomes
frozen only after approval and merge. Research plans, engineering internals,
publication drafts, and tutorials are intentionally outside this directory.

## Controlled report

| ID | Title | Language | Status |
|---|---|---|---|
| RR-2026-001 | [A Test-and-Analysis Methodology for ARINC 615A Conformance Verification / 面向 ARINC 615A 符合性验证的测试—分析方法论](RR-2026-001_test_analysis_conformance_methodology.md) | English + 中文 | v4.2 proposed bilingual methodology baseline; approval pending |

Baseline declaration: [`../BASELINE.md`](../BASELINE.md)

Controlled terminology: [`../terminology.md`](../terminology.md)

Dependency and traceability contracts: [`../../TRACKS.md`](../../TRACKS.md)

## Downstream consumers

| Consumer | Canonical entry | Permitted use |
|---|---|---|
| Research and experiments | [`../research/RESEARCH_PLAN.md`](../research/RESEARCH_PLAN.md) | register and evaluate bounded propositions against this method version |
| Engineering implementation | [`../engineering/IMPLEMENTATION_PLAN.md`](../engineering/IMPLEMENTATION_PLAN.md) | implement controlled models, cases, verdicts, and evidence interfaces |
| Publication | [`../../thesis/README.md`](../../thesis/README.md) | report only gate-supported methods, results, and limitations |
| Common tutorial | [`../../tutorial/common/README.md`](../../tutorial/common/README.md) | teach reusable verification concepts without normative authority |
| ARINC 615A tutorial | [`../../tutorial/arinc615a/README.md`](../../tutorial/arinc615a/README.md) | reproduce a named baseline/tool/example combination |

Downstream artifacts cite the report version and applicable gate record. They
cannot alter this directory by interpretation; changes return through formal
change control.

---

# 中文版

本目录只承载权威测试—分析方法论及其形式语义。v4.2 提议包仍在评审中，只有批准并合并后才会冻结。研究计划、工程内部结构、出版草稿和教程均有意放在本目录之外。

## 受控报告

| ID | 标题 | 语言 | 状态 |
|---|---|---|---|
| RR-2026-001 | [面向 ARINC 615A 符合性验证的测试—分析方法论 / A Test-and-Analysis Methodology for ARINC 615A Conformance Verification](RR-2026-001_test_analysis_conformance_methodology.md) | English + 中文 | v4.2 提议双语方法论基线；等待批准 |

基线声明：[`../BASELINE.md`](../BASELINE.md)

受控术语：[`../terminology.md`](../terminology.md)

依赖与追踪契约：[`../../TRACKS.md`](../../TRACKS.md)

## 下游消费者

| 消费者 | 权威入口 | 允许用途 |
|---|---|---|
| 研究与实验 | [`../research/RESEARCH_PLAN.md`](../research/RESEARCH_PLAN.md) | 针对本方法版本注册并评价有边界的研究命题 |
| 工程实现 | [`../engineering/IMPLEMENTATION_PLAN.md`](../engineering/IMPLEMENTATION_PLAN.md) | 实现受控模型、用例、判定和证据接口 |
| 出版 | [`../../thesis/README.md`](../../thesis/README.md) | 仅报告门禁支持的方法、结果和局限 |
| 通用教程 | [`../../tutorial/common/README.md`](../../tutorial/common/README.md) | 教授可复用验证概念，但不具有规范权威 |
| ARINC 615A 教程 | [`../../tutorial/arinc615a/README.md`](../../tutorial/arinc615a/README.md) | 复现具名基线、工具和示例组合 |

下游产物必须引用报告版本和适用门禁记录。下游解释不能修改本目录；任何变更必须通过正式变更控制返回上游。
