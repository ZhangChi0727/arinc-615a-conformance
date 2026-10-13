# CL-TAV Research Environment

This environment supports reusable literature review, evidence integration,
quantitative figures, and IEEE TAES manuscript preparation. It is a living
evidence map: there is no permanent retrieval cutoff, but every search run has
an execution date, exact query, filters, result count, and export identity.

It does not replace [`RESEARCH_CONTROL.md`](RESEARCH_CONTROL.md), the controlled
source register, experiment registration, independent review, or human author
accountability.

## 1. Research surfaces

| Surface | Authority and use |
|---|---|
| `configs/research/research_environment.json` | Machine-readable environment policy and path registry |
| `configs/research/literature/search_log.csv` | One row per executed database query |
| `configs/research/literature/screening_ledger.csv` | Candidate identity and human-owned inclusion decision |
| `configs/research/literature/evidence_ledger.csv` | Source proposition, locator, access level, and verification state |
| `configs/research/literature/claim_citation_ledger.csv` | Mapping from project or manuscript claims to extracted evidence |
| `configs/research/quantitative_figure_manifest.json` | Reproducibility contract for data-derived publication figures |
| `docs/research/publication/drafts/taes-cltav/references.bib` | Current TAES draft bibliography |
| `local-references/` and Zotero | Private full text, lawful copies, and annotations; never published from this repository |

The existing protocol source register remains the authority for ARINC and RFC
source identity. The literature ledgers add research-use evidence; they do not
promote an academic paper, implementation, or secondary source into protocol
authority.

## 2. Zotero and Better BibTeX

Create a Zotero collection named `CL-TAV TAES` and use stable Better BibTeX
citation keys. Recommended child collections are `Inbox`, `Screened-In`,
`Screened-Out`, `Background`, `Methods`, `Contrary-Evidence`, and
`Standards-Guidance`.

Use these tags where applicable:

- `full-text`, `abstract-only`, `metadata-only`;
- `peer-reviewed`, `preprint`, `standard`, `regulatory`, `implementation`;
- `verified-metadata`, `verified-proposition`, `correction`, `retraction-check`;
- project claim IDs such as `CL-DETECT`, `CL-LOCATE`, and `CL-ABLATION`.

Better BibTeX may export the selected collection to
`configs/research/literature/zotero-library.bib`. Do not copy attachments into
the repository. Promotion from that export into the manuscript bibliography is
deliberate: verify bibliographic metadata and at least one proposition before a
source supports a material manuscript claim.

## 3. Reusable review workflow

1. Define the question, intended reader, comparison axes, and current search
   scope. A living review still records the date of each execution.
2. Search IEEE Xplore, ACM Digital Library, Scopus, and Web of Science. Use
   Crossref and OpenAlex for discovery and metadata cross-checking; use Google
   Scholar for supplementary citation chasing rather than as the only search
   record.
3. Append every executed query to `search_log.csv`. Preserve exported result
   files privately when license terms prohibit redistribution.
4. Deduplicate by DOI, then stable database identifier, then normalized
   title/author/year. Preserve the duplicate resolution in screening notes.
5. Record title/abstract and full-text decisions separately. A qualified human
   owns final inclusion, exclusion, and conflict resolution.
6. Extract propositions with a page, section, table, figure, or clause locator.
   Store a paraphrase in Git. Keep substantial verbatim excerpts only in Zotero
   or another lawful private store and reference them by private note ID.
7. Map material manuscript claims to evidence before drafting. Distinguish
   direct support, partial support, contradiction, contextual use, and inference.
8. Synthesize by comparison axis or evidence pattern. Do not write a sequence
   of isolated paper summaries and do not infer novelty from an unsuccessful
   search alone.
9. Re-run targeted searches when the manuscript scope changes and before
   submission. Record each rerun rather than replacing earlier rows.

Do not call this a systematic review unless its protocol, database coverage,
deduplication, screening, and reporting obligations have actually been met.
The default description is `living evidence map` or `reproducible scoped
literature review`.

## 4. Quantitative analysis and figures

Install the repository's currently declared development dependencies in an
isolated environment:

```text
python -m venv .venv-research
.venv-research\Scripts\python -m pip install -e ".[dev]"
```

No `research` extra or quantitative plotting stack is currently declared.
When a registered figure first requires NumPy, pandas, SciPy, Matplotlib or a
similar package, add only the needed pinned dependency through a separately
reviewed dependency change and record its version in the figure manifest. The
empty manifest does not require those packages and does not constitute a
result.

Notebooks are exploratory. A number or figure used in the paper must be
generated by a script from registered inputs. Each quantitative figure entry
records source data, generator, parameters, random seed when applicable, output
paths, hashes, and review state. Prefer vector PDF/SVG for publication; use PNG
only when raster output is necessary.

The existing PlantUML architecture figures remain governed by
`cltav_figure_graphs.json` and `cltav_owned_generated_artifacts.json`. The new
quantitative manifest does not duplicate their authority.

## 5. Validation

Run from the repository root:

```text
python scripts/check_research_environment.py
python scripts/check_research_environment.py --tools
python -m pytest tests/unit/test_research_environment.py -q
```

The default check is deterministic and network-free. `--tools` reports local
capabilities for Python, TeX, bibliography, PlantUML, Graphviz, Pandoc, and SVG
inspection; optional missing tools are reported without converting a source-only
change into a failure.

## 6. Human gates

Human approval remains required for lawful source access, boundary screening,
standard interpretation, novelty wording, confirmatory experiment parameters,
raw-observation authenticity, author and institutional information, conflicts
and funding disclosure, venue submission, AI-use disclosure, and final
scientific approval.

Automation may prepare a decision packet, but it must not fill a human gate by
inference.
