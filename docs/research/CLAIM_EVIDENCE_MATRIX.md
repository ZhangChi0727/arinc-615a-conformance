# Claim–Evidence Matrix

This matrix controls what may be stated in reports, releases, and thesis text.
Status is earned by evidence; implementation progress alone cannot promote it.

| Claim ID | Permitted claim | Required evidence | Gate | Initial status |
|---|---|---|---|---|
| C-T0 | Every applicable obligation is linked to reviewed executable cases | Controlled CRS, \(\rho_{RT}\), \(\rho_{TV}\), obligation matrix | RG1–RG3, G1 | Planned |
| C-T1 | The IUT exhibited accepted behavior for named valid executions | T0 plus raw traces, configuration, oracle records, verdicts | RG4–RG5, G2 | Planned |
| C-T2 | The VCS detected all claimed members of the named evaluated fault set | T1 plus mutant catalog, equivalence decisions, held-out results | G3 | Planned |
| C-T3 | Evidence updates belief in named conformance propositions under a calibrated model | T2 plus independent calibration, prior and dependence sensitivity | G4–G5 | Optional |
| C-DIAG | The diagnostic model localizes declared fault classes at reported performance | Held-out fault instances, baselines, calibration/abstention results | G6 | Optional |
| C-XFER | Specified method elements transfer beyond ARINC 615A | Completed second-protocol instance | G7 | Future |
| C-ENG | The verification pipeline is reproducible for a named release | CI, manifests, checksums, runbook, reproducibility record | RG4–RG5 | Planned |

## Wording rules

Use:

- “traceability-complete for CRS version …”;
- “PASS was observed under configuration …”;
- “detected \(k/n\) evaluated valid non-equivalent mutants”;
- “posterior under the stated prior and calibrated observation model …”.

Avoid:

- “the finite suite proves all protocol behavior”;
- “100% coverage proves conformance”;
- “mutation score is diagnostic coverage” without a population argument;
- “PASS frequency is the probability the IUT conforms”;
- “protocol-independent” before C-XFER is supported.

## Status transitions

`Planned → Evidence Collected → In Review → Supported/Not Supported/Incomplete`

Every transition must name an artifact version and gate record. `Not Supported`
and `Incomplete` are valid research outcomes and must not be erased by editing
the claim after observing results.
