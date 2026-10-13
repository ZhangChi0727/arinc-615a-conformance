# Literature ledger contract

## Search log

Use a stable ID such as `SEARCH-YYYY-NNN`. One row represents one query actually
executed against one database. Query revisions and reruns create new rows.

## Screening ledger

Use `CAND-YYYY-NNN` for a candidate and a stable `source_id` shared with the
evidence and claim ledgers. Allowed stages are `TITLE-ABSTRACT` and `FULL-TEXT`.
Recommended decisions are `INCLUDE`, `EXCLUDE`, and `UNCERTAIN`. A human name or
role is required before a boundary decision is final.

`full_text_status` distinguishes `FULL-TEXT`, `ABSTRACT-ONLY`,
`METADATA-ONLY`, and `INACCESSIBLE`. Never infer full-text methods or results
from an abstract.

## Evidence ledger

Use `EVID-YYYY-NNN`. A locator must be specific enough for another reviewer to
find the proposition. Use access levels `FULL-TEXT`, `ABSTRACT-ONLY`, or
`METADATA-ONLY`. Use support states `DIRECT`, `PARTIAL`, `CONTRADICTS`,
`CONTEXT`, `INFERENCE`, or `UNVERIFIED`.

The proposition is a faithful paraphrase. `private_note_ref` may point to a
Zotero item/note key or an ignored local file; it must not expose proprietary or
redistribution-restricted text.

## Claim-citation ledger

Use `MAP-YYYY-NNN`. Relationships are `SUPPORTS`, `QUALIFIES`, `CONTRADICTS`,
or `CONTEXT`. Status is `DRAFT`, `HUMAN-REVIEWED`, or `REJECTED`. Every
inference records its scope limit. Manuscript prose cannot upgrade an
unverified mapping.
