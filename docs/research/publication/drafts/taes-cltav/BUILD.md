# Build the TAES first draft

Run every command from the repository root. Isolated outputs go to
`docs/research/publication/drafts/taes-cltav/build/`. Published PDFs are
copied only after staged compile and validation succeed.

```text
python scripts/build_taes_manuscript.py
python scripts/check_taes_manuscript.py
```

Required tools: `pdflatex`, `bibtex`. If they are missing the builder exits
non-zero with a capability error. Shell escape is disabled. `TEXINPUTS` and
`BSTINPUTS` use the process path separator.

The checker prints the recorded engine and source hash after a successful
validation. Vendor class/bst whitespace is documented in `vendor/PROVENANCE.md`.

Scoped diff-check (excludes vendor templates):

```text
git diff --check 1e960d20c418e183af7f05603bc02ac1733d58c3..HEAD -- . ":!docs/research/publication/drafts/taes-cltav/vendor/*"
```
