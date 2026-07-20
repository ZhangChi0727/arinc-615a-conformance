# ARINC 615A / 665 Protocol Conformance

Civil-aviation **data-load protocol conformance**: a dual-role simulation tool, a beginner tutorial path, and an academic thesis (engineer’s perspective).

| Pillar | Folder / docs | Outcome |
|---|---|---|
| **Software** | `src/`, `tests/`, `configs/` · [PROJECT_PLAN.md](PROJECT_PLAN.md) | Dual-role (DLS/THW) ARINC 615A simulator (+ minimal 665) |
| **Tutorial** | `tutorial/`, `docs/study/` | From network basics → TFTP → 615A → run a demo |
| **Thesis** | `thesis/`, [RESEARCH_OUTLINE.md](RESEARCH_OUTLINE.md) | Academic argument + experiments using the tool |

How code vs thesis work is split: **[TRACKS.md](TRACKS.md)**.

---

## Repository layout

```
├── src/a615a_sim/       # Software (Python package)
├── tests/               # Unit / integration / scenarios
├── configs/examples/    # Sample configs
├── tutorial/            # Hands-on tutorial entry
├── docs/study/          # Phase 0 lessons & glossary
├── docs/requirements/   # Verification-point drafts
├── docs/design/         # Engineering design notes
├── thesis/              # Drafts, notes, figures
├── PROJECT_PLAN.md      # Software milestones
├── RESEARCH_OUTLINE.md  # Research / thesis outline
└── TRACKS.md            # Code ↔ Thesis division
```

---

## Quick start (software skeleton)

```bash
# from repo root
python -m pip install -e ".[dev]"
python -m a615a_sim.cli --help
pytest
```

Implementation milestones: [PROJECT_PLAN.md](PROJECT_PLAN.md).

---

## Status

| Area | Status |
|---|---|
| Repo structure & plans | Ready |
| Software | Skeleton (`a615a-sim` CLI) |
| Tutorial lessons | Index in `docs/study/` — lessons being restored |
| Thesis | Outline ready; prose not started |

---

## License / confidentiality

- Cite **public** ARINC / RFC materials in the thesis.  
- Do **not** commit employer-only ICD text or proprietary training binaries.  
- Use generic terms (DLS, THW) in public thesis drafts under `thesis/`.
