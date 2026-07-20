# Tracks: Software · Tutorial · Thesis

The repo has **three end products**. Software and thesis are the main parallel workstreams; tutorial is the shared on-ramp.

```
                    ┌─────────────────────┐
                    │  Tutorial / study     │
                    │  docs/study, tutorial │
                    └──────────┬──────────┘
               ┌───────────────┴───────────────┐
               ▼                               ▼
    ┌─────────────────────┐       ┌─────────────────────┐
    │  TRACK A — Software  │       │  TRACK B — Thesis    │
    │  src/, tests/        │       │  thesis/, research   │
    └─────────────────────┘       └─────────────────────┘
```

---

## TRACK A — Code / engineering tool

| | |
|---|---|
| **Goal** | Dual-role (DLS/THW) simulator + test engine for ARINC 615A (+ minimal 665) |
| **Success looks like** | Runnable software; automated Pass/Fail; loopback + mutation verification green |
| **Primary folder** | `src/`, `tests/`, `configs/`, `scripts/` |
| **Plan document** | [`PROJECT_PLAN.md`](PROJECT_PLAN.md) |
| **Tone** | Implementation, APIs, milestones, bugs |
| **May use** | Internal names (OHMS, IDU…) in private notes under `docs/work/` |
| **Does not need** | Literature survey, research questions, academic contribution claims |

**Typical activities:** implement TFTP → 615A session → 665 codec → scenarios → CLI/report.

---

## TRACK B — Academic thesis (engineer’s perspective)

| | |
|---|---|
| **Goal** | Defend a **research question** with method + experiments (not a graduation-school template) |
| **Success looks like** | Clear RQ → related work → method → results → discussion; cite public standards |
| **Primary folder** | `thesis/` |
| **Outline document** | [`RESEARCH_OUTLINE.md`](RESEARCH_OUTLINE.md) (detail also in `docs/02_thesis_outline.md`) |
| **Tone** | Problem, gap, contribution, validity |
| **Must use** | Generic terms in public text (DLS, THW, member LRU) |
| **Does not need** | Full production GUI, every KPI form, school page quotas |

**Typical activities:** refine RQ, survey related work, define oracle model, report experiments from Track A.

---

## How they connect (briefly)

| Shared | Owned by Code | Owned by Thesis |
|---|---|---|
| Protocol understanding (`docs/study/`) | `src/` implementation | Argument & narrative in `thesis/` |
| Verification-point ideas | Executable verification scenarios in `tests/` / configs | Formal requirements model in thesis §3 |
| Validation runs | CI / pytest / reports under `artifacts/` (optional) | Tables/figures in thesis §5–6 |

**Rule of thumb:**  
- If you are asking "does the packet match the state machine?" → **Code track**.  
- If you are asking "does this answer the research question?" → **Thesis track**.
- If you are asking "does this peer conform to the standard?" → **Verification**.

---

## Suggested weekly rhythm (example)

| Day focus | Track |
|---|---|
| Study / standards reading | Shared → feeds both |
| Implement or fix a milestone | Code |
| Write 1–2 pages or refine outline | Thesis |
| Run experiments, paste results into thesis | Bridge (Code produces, Thesis consumes) |

Keep commits separable when possible: `feat(tftp): ...` vs `docs(thesis): ...`.
