# Repository Research Baseline

| Field | Value |
|---|---|
| **Baseline ID** | RB-2026-001-v4.1 |
| **Effective date** | 2026-07-26 |
| **Status** | Frozen methodology baseline |
| **Authoritative report** | [`study/RR-2026-001_test_analysis_conformance_methodology_en.md`](study/RR-2026-001_test_analysis_conformance_methodology_en.md) |
| **Synchronized translation** | [`study/RR-2026-001_测试分析符合性验证方法论_zh.md`](study/RR-2026-001_测试分析符合性验证方法论_zh.md) |

## Meaning of “frozen”

The baseline is sufficiently precise to govern requirement extraction, model construction, verification-case design, tool implementation, experiments, evidence interpretation, and claim release.

The following are frozen unless changed through the process in
[`management/CHANGE_CONTROL.md`](management/CHANGE_CONTROL.md):

- the complementary Test-and-Analysis architecture;
- the ARINC 615A instance scope and explicit non-claims;
- the separation of protocol, traceability, evidence, and inference objects;
- the T0–T3 assurance tiers;
- the formal traceability, finite-fault-domain, repeatability, and calibrated-inference semantics;
- the RG0–RG6 Review/Inspection gates and G0–G7 evidence gates;
- the rule that empirical results may strengthen only the claims supported by passed gates.

## What remains open

Freezing the methodology does not assert that the empirical research is complete. The following must be produced and reviewed:

- controlled ARINC 615A applicability declaration and CRS;
- observable EFSM and trace relations;
- executable base VCS and independently reviewed oracles;
- development and held-out fault sets;
- execution, coverage, mutation, and diagnostic datasets;
- calibration data for any T3 posterior;
- second-protocol replication before any protocol-independence claim.

Changes to these empirical artifacts normally advance the project without changing the baseline. A baseline revision is required only when they expose an error or necessary semantic change in the frozen method.

## Authority order

When repository documents disagree, apply this order:

1. controlled external standard and approved applicability declaration;
2. this baseline declaration;
3. the English RR-2026-001 v4.1 report;
4. approved design decisions and gate records;
5. research and engineering plans;
6. implementation notes, tutorials, proposals, and historical reviews.

Historical documents remain evidence of project evolution; they are not normative when superseded by this baseline.

## Baseline manifest

| Control item | Canonical location |
|---|---|
| Methodology | `docs/study/RR-2026-001_test_analysis_conformance_methodology_en.md` |
| Terminology | `docs/terminology.md` |
| Program plan | `PROJECT_PLAN.md` |
| Research plan | `docs/research/RESEARCH_PLAN.md` |
| Experiment plan | `docs/research/EXPERIMENT_PLAN.md` |
| Claim/evidence control | `docs/research/CLAIM_EVIDENCE_MATRIX.md` |
| Engineering implementation | `docs/engineering/IMPLEMENTATION_PLAN.md` |
| Research architecture | `docs/architecture.md` |
| Review gates | `docs/review/REVIEW_GUIDELINE.md` |
| Decisions | `docs/review/DESIGN_DECISIONS.md` |
| Change control | `docs/management/CHANGE_CONTROL.md` |
| Risks | `docs/management/RISK_REGISTER.md` |

## Baseline acceptance checks

- [x] English and Chinese reports have synchronized structures and mathematics.
- [x] Equations (1)–(14), numerical examples, and boundary conditions were checked.
- [x] Test, Analysis, Review, Inspection, and Demonstration roles are separated.
- [x] Scope and non-claims are centralized.
- [x] Repository plans no longer rely on unrestricted proof language.
- [x] Current unit-test suite passes before research implementation begins.
- [ ] Baseline files committed, tagged, and linked from the active GitHub PR.
