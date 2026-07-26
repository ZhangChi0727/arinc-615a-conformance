# Controlled Terminology

| Field | Value |
|---|---|
| **Version** | 2.0 |
| **Status** | Baseline-controlled |
| **Authority** | RB-2026-001-v4.1 |

## Core verification terms

| Term | Definition |
|---|---|
| **IUT** | Implementation Under Test: the fixed protocol implementation and configuration being evaluated. |
| **Applicability declaration** | Controlled statement of supported roles, services, options, and exclusions used to derive applicable requirements. |
| **Observation boundary** | Packet, timing, state, log, file, and environment phenomena permitted for verification decisions. |
| **CRS** | Conformance Requirement Set: atomic, applicable normative requirement items with controlled source references and interpretations. |
| **Verification obligation** | A functional, state, transition, data, timing, negative, or sequence aspect that must be covered for a requirement. |
| **TP** | Test Purpose: focused statement of the behavior or obligation a test is intended to verify. |
| **VC** | Verification Case: executable preconditions, stimulus, oracle, references, targets, reset, and evidence schema. |
| **VCS** | Verification Case Set: a controlled collection of VCs. |
| **Base VCS** | Cases derived from the applicable standard CRS for the base scoped claim. |
| **Extended VCS** | Additive project/ICD-specific cases whose results remain distinguishable from the base VCS. |
| **Oracle** | Rule or procedure mapping valid observations to PASS/FAIL while preserving INCONCLUSIVE/ERROR conditions. |
| **Evidence** | Versioned raw or derived records supporting a named claim, including provenance and conditions. |
| **Coverage** | Degree to which a named target set is addressed; not itself a conformance probability. |
| **Conformance** | Agreement with the declared applicable requirements under the stated observation, environment, and claim scope. |

## Verification activities

| Term | Definition |
|---|---|
| **Test** | Dynamic interaction with the IUT under controlled conditions to produce observations, measurements, and verdicts. |
| **Analysis** | Evaluation of requirements, models, traces, coverage, faults, uncertainty, dependencies, or diagnosis to determine what evidence supports and what action follows. |
| **Inspection** | Checklist-driven examination of objective artifact properties and completeness. |
| **Review** | Independent evaluation of technical judgments and progression through a gate. |
| **Demonstration** | Stakeholder-visible operation used where detailed measurement is not the primary objective; optional in this methodology. |

## Assurance and quantitative terms

| Term | Definition |
|---|---|
| **T0 Traceability** | Every applicable obligation is linked to reviewed executable cases. |
| **T1 Observed conformance** | Accepted behavior was observed for named valid executions under recorded conditions. |
| **T2 Bounded detection adequacy** | The VCS distinguishes all claimed members of a declared evaluated fault set. |
| **T3 Calibrated evidence** | Evidence updates belief in named conformance propositions under a validated observation model. |
| **Finite fault domain** | Explicit finite set of candidate nonconforming implementations or mutants used to bound a detection claim. |
| **Equivalent mutant** | Executable mutant indistinguishable from the specification within the declared observation scope. |
| **Mutation score** | Fraction or justified weighted fraction of evaluated valid non-equivalent mutants killed by the VCS. |
| **Operational PASS probability** | PASS probability under a defined repeated-run regime; not automatically belief that a fixed IUT conforms. |
| **Calibration** | Independent estimation and validation of observation-model behavior such as true-PASS and false-PASS rates. |
| **Posterior conformance belief** | Conditional probability of a named fixed conformance proposition under declared prior, likelihood, calibration, and dependence assumptions. |
| **Diagnostic model** | Separately validated model ranking fault classes from failure features; severity is governed separately. |

## Protocol roles

| Term | Definition |
|---|---|
| **DLS** | Data Loader System: loader-side ARINC 615A peer. |
| **THW** | Target Hardware: target-side ARINC 615A peer. |
| **EFSM** | Extended Finite State Machine containing control states, variables, guards, actions, inputs, and outputs. |
| **PICS-like declaration** | Project applicability artifact analogous in purpose to a Protocol Implementation Conformance Statement. |

## Usage rules

- Use PASS, FAIL, INCONCLUSIVE, and ERROR as distinct verdicts.
- Use “traceability-complete,” “observed,” or “bounded detection” instead of
  unrestricted “proved conformance.”
- Do not call mutation score FMEDA diagnostic coverage without a defensible
  target failure-mode population and mapping.
- Do not call protocol-edge labels transition probabilities unless they form a
  validated stochastic kernel.
- HMM is a candidate temporal diagnostic model, not a baseline synonym for the
  protocol model.
