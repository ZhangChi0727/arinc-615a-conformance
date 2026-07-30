# Study and Methodology Index

The approved methodology baseline is authoritative. The proposed v4.2 package
is in review and becomes frozen only after approval and merge. Tutorial lessons
are supporting material and must identify which baseline/tool release they
explain.

## Research reports

| ID | Title | Language | Status |
|---|---|---|---|
| RR-2026-001 | [A Test-and-Analysis Methodology for ARINC 615A Conformance Verification / 面向 ARINC 615A 符合性验证的测试—分析方法论](RR-2026-001_test_analysis_conformance_methodology.md) | English + 中文 | v4.2 proposed bilingual methodology baseline; approval pending |

Baseline declaration: [`../BASELINE.md`](../BASELINE.md)

Controlled terminology: [`../terminology.md`](../terminology.md)

## Planned study sequence

| Order | Topic | Status | Must connect to |
|---|---|---|---|
| 0 | Vocabulary and abbreviations | Use controlled terminology | `docs/terminology.md` |
| 1 | Ethernet/IP/UDP/TFTP foundations | Planned | observation boundary |
| 2 | TFTP state, retry, duplicate, timeout, rollover | Planned | EFSM and obligations |
| 3 | ARINC 615A DOWNLOAD/UPLOAD | Planned | CRS and base VCs |
| 4 | Minimal ARINC 665/664 constraints | Planned | scoped data oracles |
| 5 | Execute and inspect one VC | Planned | evidence manifest and verdicts |
| 6 | Coverage/mutation interpretation | Planned | T0–T2 claim boundaries |

Missing lessons are planned work, not broken required dependencies.

---

## 中文版

冻结方法论具有最高内部权威。教程仅为辅助材料，必须标明其解释的基线和工具版本。

研究顺序依次为：术语；以太网/IP/UDP/TFTP 基础；TFTP 状态、重试、重复、超时和回卷；ARINC 615A DOWNLOAD/UPLOAD；最小 ARINC 665/664 约束；执行并检查一个 VC；覆盖、时序和变异解释。尚未完成的课程属于计划工作，不构成依赖损坏。
