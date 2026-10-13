---
name: cltav-literature-review
description: Build or update the CL-TAV evidence map, literature ledgers, related-work synthesis, or source-grounded research gaps for the IEEE TAES manuscript.
---

# CL-TAV Literature Review

Use the repository's living evidence-map workflow. Read
`docs/research/RESEARCH_ENVIRONMENT.md` and
`docs/research/RESEARCH_CONTROL.md` before changing research records.

Before broad retrieval, state the question, intended use, comparison axes, and
the databases to search. There is no permanent cutoff date; record the actual
date of every search execution. Preserve exact queries, filters, counts, and
export references in `configs/research/literature/search_log.csv`.

Use DOI first for deduplication, then stable database identifiers, then
normalized title/author/year. Keep title/abstract and full-text screening
separate. Recommend decisions, but leave boundary inclusion, standard
interpretation, and novelty wording to a named human reviewer.

Extract propositions with page, section, table, figure, or clause locators.
Commit paraphrases, not substantial copyrighted excerpts. Keep private excerpt
notes in Zotero or `local-references/` and record only their private reference.
Map material claims through the evidence ledger before drafting synthesis.

Do not treat open-source behavior as protocol authority, infer a negative result
from absence of search hits, call the review systematic without the necessary
protocol, or convert planned experiments into results.

Read [references/ledger-contract.md](references/ledger-contract.md) when adding
or reviewing ledger rows.
