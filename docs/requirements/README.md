# Controlled Requirements and Traceability

This area owns applicability, CRS, discrete/timing TP/VC derivation, timing
obligations, and traceability artifacts.
It is governed by RG0–RG3 and must not contain proprietary standard text in a
public repository.

## Planned controlled artifacts

| Artifact | Suggested file | Gate |
|---|---|---|
| Applicability and observation declaration | `APPLICABILITY.md` | RG0 |
| CRS item schema and extraction instructions | `CRS_SCHEMA.md` | RG1 |
| Controlled CRS export | `CRS-<version>.csv/json` | RG1 |
| Adjudication log | `CRS_ADJUDICATION.md` | RG1 |
| Traceability schema | `TRACEABILITY_SCHEMA.md` | RG2/RG3 |
| Timing-obligation catalog | `TIMING_OBLIGATIONS-<version>.yaml/json` | RG1/RG2 |
| Requirement→TP→VC matrix | generated CSV/JSON | G1 |

## CRS minimum fields

`id`, `standardEdition`, `sourceReference`, `textHash`, `modality`,
`applicability`, `category`, `interpretation`, `obligations`, `status`,
`reviewRecord`; timing obligations additionally require trigger, response,
cancellation/silence, bounds, units, clock start/resets, inclusivity, and source.

## Rules

- two reviewers independently extract requirements before adjudication;
- requirement IDs remain stable after approval;
- source references identify edition, clause/table/figure, and controlled page;
- applicability and interpretation changes create reviewed revisions;
- requirement text is replaced by a hash or approved paraphrase in public data;
- no VC is “covered” merely because a link exists; obligation and oracle
  adequacy require review.

---

## 中文版

本目录负责适用性、CRS、离散/时序 TP/VC 导出、时序义务和追踪。公开仓库不得保存专有标准原文。CRS 的时序义务必须定义触发、响应、取消/静默、界限、单位、时钟开始/复位、边界包含性和来源；时序义务目录在 RG1/RG2 受控。存在链接不等于覆盖，义务、稳健 oracle 和误差预算仍需评审。
