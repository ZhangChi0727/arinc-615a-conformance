# Build the TAES first draft

Class files `vendor/IEEEtaes.cls` and `vendor/IEEEtaes.bst` come from the official
original-research zip linked on the TAES author-information page
(`IEEEtaes.cls` 2022/02/15 V1.1). They remain IEEE/Aptara template files.
Do not treat the zip, sample PDF, sample figures, or template author/DOI/volume
fields as manuscript content.

Working directory: this folder. Do not enable unrestricted `\write18`.
Outputs go to the ignored `build/` directory. Successful PDFs are copied to
`artifacts/publications/cltav/` only after the builder checks exit codes.

```text
python scripts/build_taes_manuscript.py
python scripts/check_taes_manuscript.py
```

The builder must be invoked from the repository root:

```text
python scripts/build_taes_manuscript.py
```

Required local tools: `pdflatex`, `bibtex`. If they are missing the builder
exits non-zero with a capability error. It does not reuse a previous PDF.

Engine record (fill from the local run): TeX engine version is written into
`build/build_record.json` and echoed by the checker.
