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
