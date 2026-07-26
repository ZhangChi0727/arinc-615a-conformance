# Traceability Schema

Traceability is relational and many-to-many.

## Required relations

| Relation | Source | Target | Required metadata |
|---|---|---|---|
| `rho_RT` | CRS requirement | Test Purpose | obligation, rationale, reviewer |
| `rho_TV` | Test Purpose | Verification Case | coverage role, polarity, reviewer |
| `rho_RM` | CRS obligation | EFSM/model target | state/transition/guard/data/timing target |
| `rho_VF` | Verification Case | fault class/operator | expected detection mechanism |
| `rho_VE` | Verification Case execution | evidence record | run and manifest IDs |

## Integrity checks

- every applicable requirement has at least one `rho_RT`;
- every requirement obligation has an adequate reviewed VC;
- every TP has at least one executable VC;
- every VC references controlled requirements and model targets;
- dangling, retired, or version-mismatched IDs fail validation;
- base and extended relations are distinguishable;
- coverage reports show missing links rather than dropping them.

## Export

Use machine-readable CSV or JSON plus a human-readable generated matrix. The
machine-readable relation set is authoritative; generated views identify the
source version and generation command.
