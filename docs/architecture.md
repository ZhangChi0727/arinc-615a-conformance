# Research Architecture

Authoritative overview of the research workflow (not the software module tree).  
Implementation details live under `PROJECT_PLAN.md` and `src/`; this document describes the **method pipeline**.

```
ARINC Specification (public standard)
        │
        ▼
Requirement Extraction          →  CRS / Requirement Items
        │
        ▼
Verification Point              →  testable obligations + oracles
        │
        ▼
Requirement Model               →  coverage relations, protocol graphs / EFSM views
        │
        ▼
Test Case (Verification Case)   →  preconditions, stimulus, expected, verdict
        │
        ▼
Execution                       →  dual-role simulator / peers / lab
        │
        ▼
Evidence                        →  logs, traces, Pass/Fail records
        │
        ▼
Confidence                      →  optional quantitative assurance metrics
        │
        ▼
Conformance Claim               →  scoped to CRS + fault model (+ project class)
```

## Base vs extended

| Path | Source | Role |
|------|--------|------|
| Base | ARINC 615A (and agreed supporting RFCs/665 minimal scope) | Project-agnostic conformance claim |
| Extended | Project ICD / customer extras | Additive assurance; must not rewrite base cases |

## Where artifacts live

| Stage | Typical location |
|-------|------------------|
| Study / methodology | `docs/study/` |
| Terminology | `docs/terminology.md` |
| Engineering plan | `PROJECT_PLAN.md` |
| Research outline | `RESEARCH_OUTLINE.md` |
| Cases / templates | `configs/` |
| Software instrument | `src/`, `tests/` |
| Thesis prose | `thesis/` |

## Non-goals of this document

- Does not redefine probabilistic formulas (see research reports under `docs/study/`).
- Does not replace module-level software design docs under `docs/design/`.
