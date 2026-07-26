# Study and Methodology Index

The frozen methodology is authoritative. Tutorial lessons are supporting
material and must identify which baseline/tool release they explain.

## Research reports

| ID | Title | Language | Status |
|---|---|---|---|
| RR-2026-001 | [A Test-and-Analysis Methodology for ARINC 615A Conformance Verification](RR-2026-001_test_analysis_conformance_methodology_en.md) | English | v4.1 frozen methodology baseline |
| RR-2026-001 | [面向 ARINC 615A 符合性验证的测试—分析方法论](RR-2026-001_测试分析符合性验证方法论_zh.md) | 中文 | v4.1 同步译本 |

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
