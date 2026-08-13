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
| Verification Objective schema | `VERIFICATION_OBJECTIVE.md` | RG2/RG3 |
| Timing-obligation catalog | `TIMING_OBLIGATIONS-<version>.yaml/json` | RG1/RG2 |
| Requirement→objective→TP→VC matrix | generated CSV/JSON | G1 |

## CRS minimum fields

`id`, `standardEdition`, `sourceReference`, `textHash`, `modality`,
`applicability`, `category`, `interpretation`, `obligations`, `status`,
`reviewRecord`; timing obligations additionally require trigger, response,
cancellation/silence, bounds, units, clock start/resets, inclusivity, and source.

## Rules

- two reviewers independently extract requirements before adjudication;
- requirement IDs remain stable after approval;
- each applicable obligation maps to at least one Verification Objective before it
  is considered closed;
- a single execution `PASS` does not close an obligation; objective satisfaction
  is a reviewed conclusion;
- source references identify edition, clause/table/figure, and controlled page;
- applicability and interpretation changes create reviewed revisions;
- requirement text is replaced by a hash or approved paraphrase in public data;
- no VC is “covered” merely because a link exists; obligation and oracle
  adequacy require review.

---

# 中文版

本目录负责适用性、CRS、离散/时序 TP/VC 导出、时序义务和追踪。公开仓库不得保存专有标准原文。CRS 的时序义务必须定义触发、响应、取消/静默、界限、单位、时钟开始/复位、边界包含性和来源；时序义务目录在 RG1/RG2 受控。存在链接不等于覆盖，义务、稳健 oracle 和误差预算仍需评审。

## 计划中的受控产物

包括 RG0 的适用性/观测声明，RG1 的 CRS schema、受控导出和裁决日志，RG2/RG3 的追踪 schema，RG1/RG2 的时序义务目录，以及满足 G1 的需求→TP→VC 机器可读矩阵。

## CRS 最小字段

至少包含 `id`、标准版本、来源、文本 hash、模态、适用性、类别、解释、义务、状态和评审记录；时序义务还要包含触发、响应、取消/静默、界限、单位、时钟开始/复位、边界包含性和来源。

## 规则

两名评审者独立提取后裁决；批准后的需求 ID 稳定；来源定位到版本、条款/表/图和受控页；适用性/解释变化形成评审修订；公开数据用 hash 或批准释义替代专有原文；只有链接不能证明 VC 覆盖，义务和 oracle 充分性必须评审。
