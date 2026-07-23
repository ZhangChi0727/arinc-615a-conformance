# Review Guideline

Standardize future pull-request reviews. A single PR may receive more than one review type.

## Review types

### 1. Repository Review

Checks structure, naming, docs placement, secrets/binaries policy, and consistency with `TRACKS.md` / `README.md`.

Typical questions:
- Are new files in the right track (`src/` vs `docs/` vs `thesis/`)?
- Are proprietary or oversized binaries excluded?
- Do cross-links resolve?

### 2. Engineering Review

Checks code, tests, CI, APIs, and implementability against `PROJECT_PLAN.md`.

Typical questions:
- Do tests fail for the right reasons?
- Is the change scoped to the stated milestone?
- Any regressions in TFTP/session behavior?

### 3. Methodology Review

Checks verification-method soundness: requirement→case derivation, coverage claims, fault model, base/extended separation.

Typical questions:
- Are coverage and conformance claims scoped?
- Are definitions consistent with `docs/terminology.md`?
- Any unjustified statistical independence or over-strong proof language?

### 4. Research Review

Checks academic framing: RQ, related work, novelty boundary, thesis outline alignment, citation hygiene.

Typical questions:
- Is the contribution claimed clearly (method vs software instrument)?
- Confidentiality / genericization respected in public text?

## Outcomes

Each review should end with one of:

| Outcome | Meaning |
|---------|---------|
| **APPROVED** | No blocking issues for this review type |
| **APPROVED WITH COMMENTS** | Non-blocking improvements suggested |
| **REQUEST CHANGES** | Blocking issues must be resolved before merge (for that concern) |

Repository-wide merge still requires green CI and project branch-protection rules.

## Review artifacts

- Store durable review write-ups under `docs/review/` (e.g. `PR0002_REVIEW.md`).
- Record lasting design choices in `docs/review/DESIGN_DECISIONS.md`.
