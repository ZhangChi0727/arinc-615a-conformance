# Controlled Requirements and Traceability

This area owns applicability, CRS, TP/VC derivation, and traceability artifacts.
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
| Requirement→TP→VC matrix | generated CSV/JSON | G1 |

## CRS minimum fields

`id`, `standardEdition`, `sourceReference`, `textHash`, `modality`,
`applicability`, `category`, `interpretation`, `obligations`, `status`,
`reviewRecord`.

## Rules

- two reviewers independently extract requirements before adjudication;
- requirement IDs remain stable after approval;
- source references identify edition, clause/table/figure, and controlled page;
- applicability and interpretation changes create reviewed revisions;
- requirement text is replaced by a hash or approved paraphrase in public data;
- no VC is “covered” merely because a link exists; obligation and oracle
  adequacy require review.
