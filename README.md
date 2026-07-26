# ARINC 615A Test-and-Analysis Conformance Verification

Research and engineering repository for an auditable ARINC 615A conformance
verification methodology and its dual-role experimental instrument.

The repository is governed by frozen methodology baseline
[`RB-2026-001-v4.1`](docs/BASELINE.md). The baseline defines two complementary
paths:

- **Test:** derive and execute requirement-based Verification Cases;
- **Analysis:** evaluate traceability, coverage, bounded fault detection,
  uncertainty, and diagnosis.

Review and Inspection gates control the artifacts and claims produced by both
paths.

## Start here

| Need | Document |
|---|---|
| Understand what is frozen | [`docs/BASELINE.md`](docs/BASELINE.md) |
| Read the methodology | [English report](docs/study/RR-2026-001_test_analysis_conformance_methodology_en.md) · [中文报告](docs/study/RR-2026-001_测试分析符合性验证方法论_zh.md) |
| See the integrated program | [`PROJECT_PLAN.md`](PROJECT_PLAN.md) |
| Plan research and experiments | [`docs/research/RESEARCH_PLAN.md`](docs/research/RESEARCH_PLAN.md) |
| Implement the instrument | [`docs/engineering/IMPLEMENTATION_PLAN.md`](docs/engineering/IMPLEMENTATION_PLAN.md) |
| Navigate all documents | [`docs/README.md`](docs/README.md) |

## Repository structure

```text
src/                    verification instrument
tests/                  unit, contract, integration, and scenarios
configs/                schemas, cases, and controlled examples
artifacts/              local/generated experimental evidence
docs/
  study/                frozen methodology and study material
  research/             research, experiment, and claim control
  engineering/          implementation plan
  requirements/         applicability, CRS, TP, VC, traceability
  design/               EFSM and software design
  review/               gates, decisions, and review records
  management/           change and risk control
  proposal/             historical/proposed changes
thesis/                 publication drafts, notes, and figures
tutorial/               learning and operational walkthroughs
```

## Current state

| Area | State |
|---|---|
| Methodology | v4.1 frozen as a research-method baseline |
| Empirical assurance | T0–T3 not yet earned; evidence work starts at RG0/RG1 |
| Engineering | TFTP core skeleton and tests exist; 48 tests currently pass |
| Repository governance | Program, research, implementation, experiment, risk, and change plans established |

## Quick start

```bash
python -m pip install -e ".[dev]"
python -m a615a_sim.cli --help
pytest
```

## Evidence and confidentiality

- Do not commit proprietary ARINC or employer-only ICD text.
- Use stable source references and hashes in public CRS artifacts.
- Keep project-specific names and private notes under `docs/work/`.
- Do not call a result “conformance proof,” “diagnostic coverage,” or a
  “conformance probability” unless the relevant claim and gate requirements are
  satisfied.
