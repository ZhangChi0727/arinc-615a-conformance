# Terminology

Single source of truth for project terms.  
Future documents should reference this file instead of redefining terms inline.

| Term | Definition |
|------|------------|
| **Verification Point** | A testable obligation derived from the protocol standard (or an approved project extension), with clear pass/fail meaning. |
| **Requirement** | A normative obligation in a specification (e.g. ARINC 615A “shall” clause) or an approved project ICD item. |
| **Requirement Item** | A uniquely identified element of a requirement set (CRS entry), used for traceability into verification points and cases. |
| **Evidence** | Recorded artifacts from execution or analysis (logs, verdicts, traces, reports) that support a conformance or coverage claim. |
| **Oracle** | The rule or procedure that maps observed behavior to Pass/Fail (expected result + verdict logic). |
| **Coverage** | The extent to which a verification case set addresses a defined target set (requirements, states, transitions, mutants, etc.). |
| **Confidence** | A quantitative or qualitative measure of assurance in conformance *given evidence*; not an intrinsic random property of the IUT unless explicitly modeled as such. |
| **Conformance** | Agreement of an IUT with a stated requirement set and scope (standard and/or project class), within an explicit fault/observation model. |
| **Fault Model** | The finite set of fault classes or mutants against which detection capability is claimed. |
| **Mutation** | Deliberate seeding of a fault/mutant to assess whether the verification case set can detect non-conformance. |
| **IUT** | Implementation Under Test — the specific protocol implementation being verified for conformance (ISO/IEC 9646 term). |
| **CRS** | Conformance Requirement Set — the set of normative requirements extracted from a protocol standard (Def. 1 in RR-2026-001). |
| **VC** | Verification Case — a single testable unit with preconditions, stimulus, expected result, verdict, and standard reference (Def. 2). Distinct from VCS (the set). |
| **ICD** | Interface Control Document — project-specific interface specification; source of extended VCS requirements. |
| **Testing** | DO-178C §6.4 verification method: execution of the IUT against expected results. In this methodology, encompasses §4–5 (requirements-based derivation, VC execution, coverage validation, mutation adequacy). Distinguished from internal development testing (unit test, integration test). |
| **Analysis** | DO-178C §6.4 verification method: evaluation of evidence without additional IUT execution. In this methodology, encompasses §6 (probabilistic confidence modeling, FMEA, fault localization). |

## Probabilistic / mathematical terms

| Term | Definition |
|------|------------|
| **DTMC** | Discrete-Time Markov Chain — used as an interpretation model for protocol phase structure and epistemic confidence narration (theory debt TD-01 pending further formalization). |
| **HMM** | Hidden Markov Model — models the verification process: hidden conformance/fault class \(Z_k\), observation \(X_k\), parameters \(\theta\). |
| **FMEA** | Failure Mode and Effects Analysis — systematic enumeration of failure modes per transition, with local/global effects and severity. |
| **FMEDA** | Failure Modes, Effects, and Diagnostic Analysis — extends FMEA with diagnostic coverage quantification. |
| **DC** | Diagnostic Coverage — fraction of failure modes detected by the verification case set for a given transition. |
| **SPRT** | Sequential Probability Ratio Test — optimal stopping criterion for self-loop verification sampling. |
| **EFSM** | Extended Finite State Machine — state machine with variables, guards, and actions; the formal model for ARINC 615A session behavior. |

## ISO/IEC 9646 and conformance testing terms

| Term | Definition |
|------|------------|
| **PICS** | Protocol Implementation Conformance Statement — declaration of which options/features an implementation supports; determines applicable VC subset. |
| **ATS** | Abstract Test Suite — complete set of abstract test cases covering all conformance requirements (ISO/IEC 9646 term; our "base VCS"). |
| **TP** | Test Purpose — a focused statement of what aspect of conformance a test verifies (ETSI term); maps 1:1 or 1:N to VCs. |
| **ioco** | Input-output conformance (Tretmans, 1996) — formal relation: I ioco S iff outputs(I,σ) ⊆ outputs(S,σ) for all traces σ of S. |

## ARINC domain terms

| Term | Definition |
|------|------------|
| **LSAP** | Loadable Software Aircraft Part — the data unit defined by ARINC 665; the content transferred by ARINC 615A. |
| **LU** | Loadable Unit — the data container defined by ARINC 664; the physical file format for data loading. |
| **AFDX** | Avionics Full-Duplex Switched Ethernet — the network standard defined by ARINC 664; transport layer for data loading. |

## Related role terms (protocol)

| Term | Definition |
|------|------------|
| **DLS** | Data Loader System — loader-side peer in ARINC 615A. |
| **THW** | Target Hardware — target-side peer in ARINC 615A. |
| **VCS** | Verification Case Set — the collection of verification cases under study. |
| **Base VCS** | Standard-derived, project-agnostic cases used for the base conformance claim. |
| **Extended VCS** | Project/ICD-specific cases; additive and must not invalidate the base claim. |

## Notes

- Prefer these spellings in English docs; Chinese glosses may appear in bilingual reports but should map 1:1 to this table.
- Research reports may introduce additional formal symbols; those symbols must still bind to terms defined here.
- **Testing vs. development testing:** "Testing" (capitalized, or as compound term "Requirements-Based Testing") denotes the DO-178C verification method. Internal development activities always use qualified forms: "unit test", "integration test", "regression test" — never bare "Test" without qualifier.
- **DTMC status:** Retained as interpretation model per PR #2 review; further formalization (Protocol Evidence Graph) is theory debt TD-01.
