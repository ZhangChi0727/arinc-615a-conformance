# Scripts

Automation scripts should support one of:

- schema and traceability validation;
- controlled execution and evidence capture;
- mutation/fault generation with registered seeds;
- raw-to-derived analysis reproduction;
- report/table generation;
- repository link and baseline consistency checks.

Each research script records its inputs, outputs, version, and deterministic
settings. Historical one-off PR/review scripts beginning with `_` are not part
of the frozen research pipeline unless promoted through review.

Current controlled check:

```bash
python scripts/check_repo_baseline.py
```

It validates required baseline files, local document links, bilingual report
structure, mathematical delimiters, equation numbering, and legacy filenames.
