# Project Plan — Track A (Code / Engineering Tool)

Status: **v0.1**  
Related: [`TRACKS.md`](TRACKS.md) · [`RESEARCH_OUTLINE.md`](RESEARCH_OUTLINE.md)

---

## 1. Product goal

Build a **dual-role protocol conformance simulation environment** that can act as:

- **DLS-mode** — Data Loader (drive tests against a Target Hardware), and/or  
- **THW-mode** — Target Hardware (be driven by a Data Loader),

for **ARINC 615A** over TFTP/UDP, with **minimal ARINC 665** support (valid `.LUH` / `.LUP` build & check).

**Non-goals (for now):** full 665 media-set manufacturing, ARINC 615-3/429 path, production-grade GUI, claiming ASPICE certification.

---

## 2. Locked decisions

| Topic | Decision |
|---|---|
| Roles | Both, switchable (Role Controller) |
| Language | Python first; optional C/C++ TFTP later |
| 665 scope | Minimal |
| Validation | Self-loopback + mutation required; real simulator/HW optional |
| Confidentiality | Real names OK in `docs/work/`; genericize in thesis |

---

## 3. Repository layout (code-facing)

```
src/
  a615a_sim/           # installable package root
    tftp/              # RFC 1350 + options + rollover-to-1
    session/           # 615A virtual-file state machines
    lsap/              # minimal 665 codec
    roles/             # Role Controller (DLS / THW)
    engine/            # scenario runner, fault injection, verdicts
    report/            # JSON / text reports
    cli.py             # entry point
tests/
  unit/                # tftp, lsap, parsers
  integration/         # loopback DLS↔THW
  scenarios/           # conformance scenarios (mutation etc.)
configs/
  examples/            # sample peer addresses, scenario YAML/JSON
scripts/
  run_loopback.py      # quick demo
  build_pptx.py        # optional study deck rebuild
artifacts/             # local run outputs (gitignored reports OK)
```

---

## 4. Milestones (code only)

| ID | Milestone | Done when | Approx. |
|---|---|---|---|
| **C0** | Repo skeleton + package importable | `python -m a615a_sim.cli --help` works | Week 0 |
| **C1** | TFTP core | RRQ/WRQ/DATA/ACK/ERROR/OACK; timeout retry; rollover→1; unit tests | |
| **C2** | Role-agnostic transfer API | Same engine used as client or server | |
| **C3** | 615A session (Operator DOWNLOAD) | `.LNO`→`.LNL`/`.LNA`→data + `.LNS` side channel | |
| **C4** | 615A UPLOAD (minimal happy path) | Init + list/status family enough for one nominal load | |
| **C5** | Minimal 665 codec | Build/parse `.LUH`; check value; THW ID mismatch detect | |
| **C6** | Scenario engine + fault injection | Catalog scenarios executable; JSON verdict report | |
| **C7** | Loopback validation suite | DLS-mode ↔ THW-mode on localhost green | |
| **C8** | Mutation suite | Known-bad peers detected (rollover, checksum, blksize, status) | |
| **C9** *(optional)* | External peer | Talk to OHMS simulator / real THW when available | |
| **C10** *(stretch)* | Native TFTP hot path | C/C++ optional optimization | |

---

## 5. Intermediate engineering products

| Product | Location |
|---|---|
| Runnable CLI tool | `src/a615a_sim/` |
| Unit + integration tests | `tests/` |
| Example configs / scenarios | `configs/examples/` |
| Design notes for implementers | `docs/design/` (create when coding starts) |
| Work-only notes (ICD names, KPI) | `docs/work/` (not for public thesis) |

Company-facing documents (需求、测试指南) may be **exported later** from design notes + scenario catalog; they are **not** the driver of this plan.

---

## 6. Definition of Done (MVP)

MVP is complete when:

1. Loopback Operator DOWNLOAD (nominal) Passes in both role assignments (who is DLS/THW).  
2. At least **four** mutation cases Fail correctly with clear verdict reasons.  
3. Minimal LSAP with wrong check value is rejected (or flagged) per oracle.  
4. One machine-readable report (JSON) produced per run.  
5. README documents how to run loopback in &lt;10 steps.

---

## 7. Dependencies on Track B (thesis)

Code track **does not wait** for finished thesis prose.  
Thesis track **consumes** Code milestones C7–C8 results for experiments.

Shared inputs both need early:

- Phase 0 study notes → `docs/study/`  
- Draft test-point list → `docs/requirements/test_points.md` (to create)

---

## 8. Next code action

1. Create `src/a615a_sim` package skeleton (C0).  
2. Implement TFTP unit tests + minimal server/client on localhost (C1).  
3. Do **not** start thesis chapter drafting inside `src/`.
