# Research and Publication Outline

| Field | Value |
|---|---|
| **Version** | 2.0 |
| **Status** | Aligned with RB-2026-001-v4.1 |
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
4. a finite-fault-domain evaluation with held-out faults;
5. Review and Inspection gates that connect scientific discipline to
   engineering release control;
6. a reproducible instrument and artifact chain;
7. conditional evidence about calibration, diagnosis, and transferability.

These are research propositions until supported by the claim/evidence matrix.

## Publication structure

| Section | Purpose |
|---|---|
| Abstract | Problem, method, achieved evidence, contribution, boundaries |
| 1 Introduction | Engineering problem, research gap, questions, value |
| 2 Background | ARINC 615A scope, conformance theory, verification methods |
| 3 Methodology | Test/Analysis loop, objects, tiers, formal core |
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
5. write discussion and conclusion only after claim/evidence review.

Implementation completion is not a publication result by itself, and a PASS
suite is not an unrestricted conformance proof.
