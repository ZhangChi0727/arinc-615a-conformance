# Research and Publication Outline

| Field | Value |
|---|---|
| **Version** | 2.2 |
| **Status** | Aligned with RB-2026-001-v4.2 |
| **Detailed research plan** | [`docs/research/RESEARCH_PLAN.md`](docs/research/RESEARCH_PLAN.md) |

## Working title

**English:** *A Test-and-Analysis Methodology for ARINC 615A Conformance Verification*

**Chinese:** *面向 ARINC 615A 符合性验证的测试—分析方法论*

## Central question

> How can complementary requirements-based Test and bounded evidence Analysis
> produce auditable, reproducible, and engineering-useful ARINC 615A
> conformance decisions?

The report's RQ1–RQ6 decompose this question into derivation, coverage, bounded
adequacy, evidence interpretation, diagnosis, and transferability.

## Contributions to evaluate

1. an auditable many-to-many standard→TP→VC derivation framework;
2. a closed Test-and-Analysis verification loop;
3. an assurance argument separating traceability, execution, detection
   adequacy, and calibrated interpretation;
4. deterministic timed-conformance semantics with measurement uncertainty;
5. a finite-fault-domain evaluation with held-out discrete and timing faults;
6. Review and Inspection gates that connect scientific discipline to
   engineering release control;
7. a reproducible instrument and artifact chain;
8. conditional evidence about calibration, diagnosis, and transferability.

These are research propositions until supported by the claim/evidence matrix.

## Publication structure

| Section | Purpose |
|---|---|
| Abstract | Problem, method, achieved evidence, contribution, boundaries |
| 1 Introduction | Engineering problem, research gap, questions, value |
| 2 Background | ARINC 615A scope, conformance theory, verification methods |
| 3 Methodology | Test/Analysis loop, objects, tiers, discrete and timed formal core |
| 4 Research instrument | Dual-role peer, VC engine, evidence provenance |
| 5 Evaluation design | Baselines, held-out faults, calibration, controls |
| 6 Results | Traceability, execution, adequacy, optional T3/diagnosis |
| 7 Discussion | Academic and engineering implications, validity, transfer |
| 8 Conclusion | Answers limited to achieved gates |
| Appendices | Schemas, condensed matrices, reproduction instructions |

## Writing order

1. freeze introduction, background boundaries, and method from the baseline;
2. draft experiment protocol before collecting confirmatory evidence;
3. write instrument details against released engineering versions;
4. generate results from controlled datasets and scripts;
5. record the baseline, experiment, evidence-manifest, analysis, and gate IDs
   for every reported result;
6. write discussion and conclusion only after claim/evidence review.

Implementation completion is not a publication result by itself, and a PASS
suite is not an unrestricted conformance proof.

---

# 中文版

工作题目为《面向 ARINC 615A 符合性验证的测试—分析方法论》。核心问题是：互补的基于需求测试和有限证据分析如何产生可审计、可复现且对工程有用的离散与时序符合性决策？

## 工作题目

英文题目为 *A Test-and-Analysis Methodology for ARINC 615A Conformance Verification*；中文题目为《面向 ARINC 615A 符合性验证的测试—分析方法论》。

## 核心问题

互补的基于需求测试和有限证据分析如何产生可审计、可复现且对工程有用的 ARINC 615A 符合性决策？RQ1–RQ6 分解为导出、覆盖、有限充分性、证据解释、诊断和可迁移性。

## 待评价贡献

包括多对多标准—TP—VC 导出、测试—分析闭环、分离追踪/执行/检测/校准的保证论证、带测量不确定性的确定性时序语义、含留出离散/时序故障的有限故障域、评审/检查门、可复现工具链，以及条件式校准/诊断/迁移证据。这些在主张—证据矩阵支持前都只是研究命题。

## 论文结构

论文依次包含摘要、引言、背景、方法论、研究工具、评价设计、结果、讨论、结论和复现附录；每一部分的措辞必须受已获得证据门约束。

## 写作顺序

必须先冻结引言边界和方法、再在收集验证性证据前完成实验协议、随后依据受控工程版本和数据生成结果；每项报告结果必须记录基线、实验、证据清单、分析和门禁 ID，最后经主张—证据评审撰写讨论和结论。实现完成或测试 PASS 本身不是论文结果或无限定符合性证明。
