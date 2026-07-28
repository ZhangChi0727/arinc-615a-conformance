# Review and Gate Guideline

| Field | Value |
|---|---|
| **Version** | 2.0 |
| **Status** | Baseline-aligned |
| **Source** | RR-2026-001 v4.1 §4.10 |

## Review types

| Type | Focus |
|---|---|
| Repository | placement, naming, links, confidentiality, baseline references |
| Engineering | behavior, interfaces, tests, reproducibility, tool failure modes |
| Methodology | requirements, models, oracles, fault domain, mathematical semantics |
| Research | questions, hypotheses, baselines, validity, citations, claim strength |
| Evidence | provenance, exclusions, calculations, raw-to-derived reproduction |
| Claim release | correspondence between wording, achieved tier, risks, and gates |

One PR or gate may require several review types.

## RG0–RG6

| Gate | Entry | Required reviewers | Approval focus |
|---|---|---|---|
| RG0 Scope | standard, roles, services, applicability, observation draft | method + engineering | feasible, bounded scope |
| RG1 CRS | dual extraction and adjudication | requirements + independent method | source, atomicity, applicability |
| RG2 Model/trace | EFSM and mappings | protocol + method | observability, consistency, completeness |
| RG3 VC/oracle | cases, oracle, reset, evidence schema | test + independent protocol | executability and verdict validity |
| RG4 Execution | IUT/tool/environment configuration | engineering + test | control, dry run, tool validity |
| RG5 Evidence | raw and derived packages | evidence + analysis | provenance, exclusions, reproduction |
| RG6 Claim | assurance argument and proposed wording | independent research + engineering authority | achieved gates and residual risk |

Independence means the reviewer did not solely author the judgment being
approved. A small team may use role separation and a recorded second pass.

## Outcomes

Use exactly:

- `APPROVE`;
- `APPROVE WITH ACTIONS`;
- `REWORK`.

`APPROVE WITH ACTIONS` must identify owners and deadlines and cannot be used for
an unresolved mathematical error, invalid oracle, missing provenance, or
overstated claim.

## Finding severity

| Severity | Meaning |
|---|---|
| Must | Blocks the gate or merge |
| Should | Required follow-up with named owner |
| Nice | Optional improvement |

## Gate record

Store durable records as `docs/review/gates/GR-<gate>-<date>-<artifact>.md`:

```text
artifact and version
baseline and applicable claim IDs
reviewers and independence statement
entry criteria
findings and dispositions
residual risks
decision
sign-off date
```

## Theory debt

Theory debt is permitted only when:

- it does not contradict the frozen baseline;
- it is irrelevant to the current released claim;
- it has an owner, trigger, and destination;
- claim wording excludes the unresolved theory.

DTMC edge-confidence, first-order path products, and HMM-based localization are
not active baseline mechanisms. They may re-enter only through baseline change
control supported by appropriate data and validation.
