# Baseline and Change Control

| Field | Value |
|---|---|
| **Process ID** | CMP-2026-001 |
| **Applies to** | RB-2026-001-v4.1 and controlled descendants |
| **Owner** | Research lead |

## Change classes

| Class | Examples | Approval |
|---|---|---|
| **Editorial** | spelling, formatting, link repair with no semantic effect | document owner |
| **Artifact** | new CRS item, VC, mutant, result, or implementation conforming to baseline | applicable gate owner |
| **Interpretive** | changed standard interpretation, oracle, applicability, or equivalence decision | independent methodology review |
| **Baseline** | changed RQ, scope, formal semantics, assurance tier, or gate rule | formal CR and RG6-style independent approval |

## Baseline change request

Create `docs/management/changes/CR-YYYY-NNN.md` containing:

- problem and triggering evidence;
- affected baseline clauses and downstream artifacts;
- scientific and engineering impact;
- alternatives considered;
- migration and re-evaluation plan;
- review findings and disposition;
- new version and effective date if approved.

## Rules

1. Do not silently edit a frozen claim after seeing experimental results.
2. Corrections to mathematical errors are mandatory baseline changes, not
   editorial changes.
3. Scope expansion requires applicability, observation, fault-model, schedule,
   and confidentiality impact analysis.
4. Superseded documents remain in history and link to the replacing baseline.
5. Every released evidence package records the exact baseline identifier.
6. A baseline version is immutable after its release commit/tag; subsequent
   changes create a new version.

## Git and PR policy

- branch new work from an up-to-date `main`;
- use `codex/` for Codex-created branches unless a project branch is specified;
- keep methodology, engineering, and evidence changes separable where practical;
- PR descriptions identify affected RQs, gates, claims, and baseline;
- methodology changes require a methodology reviewer independent of the author;
- raw evidence changes require provenance and reproduction checks;
- squash only when the resulting commit preserves useful baseline and gate IDs.

Recommended baseline tag after approval: `research-baseline/RB-2026-001-v4.1`.
