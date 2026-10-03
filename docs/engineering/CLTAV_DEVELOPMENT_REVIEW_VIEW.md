# CL-TAV Development Readiness Review View

> Generated from `configs/engineering/cltav_development_contracts.json`; do not edit.

- Control: `CR-2026-016`; decisions DD-038, DD-039, DD-040
- Bound M1 requirements: 863; disposition total: 863; readiness: `READINESS-BLOCKED`; claim: `SPECIFICATION-ONLY`

## Inputs

- `ARINC615A3-M1-CRS` — `configs/requirements/arinc_615a3_m1_crs.json` — SHA-256 `7f35f538fff2d9f8204360f650a1b5c794f9969497ad9ef3f1dfe114248a315f` — Bound protocol requirement universe
- `CLTAV-INTERFACE-REGISTRY` — `configs/research/cltav_interface_registry.json` — SHA-256 `a65679b902cf51d31aa613c133919c3cd2c66dbc6c65eb3cc58d9bf3530d329d` — Accepted interface vocabulary

## Slices and dependencies

- `SLICE-OFFLINE-UPLOAD-INFORMATION` — offline capture to traceable report — 176 requirement uses
- dependency `DEP-INTEGRITY`: `BLOCKED`

## Disposition summary

| Disposition | Count |
|---|---:|
| `DEPENDENCY-BLOCKED` | 6 |
| `FIRST-SLICE-IMPLEMENTATION` | 170 |
| `LATER-SERVICE` | 137 |
| `NOT-TOOL-OBLIGATION` | 550 |

## First-slice uses

| Requirement | Module | Record | Acceptance | Rationale |
|---|---|---|---|---|
| `CRS-M1-00021` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. |
| `CRS-M1-00025` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. |
| `CRS-M1-00032` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. |
| `CRS-M1-00071` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00072` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00073` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00074` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00075` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00076` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00077` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00078` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00079` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00080` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00081` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00082` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00083` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00084` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00085` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00086` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00087` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00088` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00089` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00090` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00091` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00093` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00094` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00095` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00096` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00097` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00098` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00099` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00100` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00101` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00102` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00103` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00104` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00105` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00106` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00107` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00108` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00109` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00124` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00125` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00126` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00127` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00128` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00129` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00130` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00131` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00132` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00133` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00134` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00135` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00136` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00137` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00138` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00139` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00140` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00141` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00142` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00143` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00144` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00145` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00146` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00147` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00148` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00149` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00150` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00151` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00152` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00153` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00154` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00155` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00156` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00157` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00158` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00159` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00160` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00161` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00162` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00163` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00164` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00165` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00166` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00186` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. |
| `CRS-M1-00282` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00283` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00284` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00285` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00286` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00287` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00288` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00289` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00290` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00291` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00292` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00293` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00294` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00295` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00296` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00297` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00298` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00299` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00300` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00301` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00302` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00303` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00304` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00305` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00306` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00307` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00308` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00309` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00310` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00311` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00312` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00313` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00314` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00315` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00316` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00317` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00318` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00319` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00320` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00321` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00322` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00323` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00324` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00325` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00326` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00327` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00328` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00329` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00330` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00331` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00332` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00333` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00346` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00347` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00348` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00349` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00350` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00351` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00352` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00353` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00354` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00355` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00356` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00357` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00358` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00359` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00360` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00361` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00362` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00363` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00364` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00365` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00366` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00367` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00368` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00369` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00370` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00371` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00372` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00373` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00374` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00375` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00376` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00378` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00618` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |
| `CRS-M1-00620` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. |
| `CRS-M1-00622` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |
| `CRS-M1-00632` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |
| `CRS-M1-00645` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |
| `CRS-M1-00646` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |
| `CRS-M1-00647` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |

# 中文版

# CL-TAV 开发就绪评审视图

> 由同一权威 JSON 生成，禁止手工修改。

- 绑定 M1 需求：863；处置合计：863；就绪状态：`READINESS-BLOCKED`；主张边界：`SPECIFICATION-ONLY`

## 输入身份

- `ARINC615A3-M1-CRS` — `configs/requirements/arinc_615a3_m1_crs.json` — SHA-256 `7f35f538fff2d9f8204360f650a1b5c794f9969497ad9ef3f1dfe114248a315f` — Bound protocol requirement universe
- `CLTAV-INTERFACE-REGISTRY` — `configs/research/cltav_interface_registry.json` — SHA-256 `a65679b902cf51d31aa613c133919c3cd2c66dbc6c65eb3cc58d9bf3530d329d` — Accepted interface vocabulary

## 切片与依赖

- `SLICE-OFFLINE-UPLOAD-INFORMATION` — offline capture to traceable report — 176 条需求用途
- 依赖 `DEP-INTEGRITY`：`BLOCKED`

## 处置摘要

| 处置 | 数量 |
|---|---:|
| `DEPENDENCY-BLOCKED` | 6 |
| `FIRST-SLICE-IMPLEMENTATION` | 170 |
| `LATER-SERVICE` | 137 |
| `NOT-TOOL-OBLIGATION` | 550 |

## 首轮用途

| 需求 | 模块 | 记录 | 验收 | 理由 |
|---|---|---|---|---|
| `CRS-M1-00021` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. |
| `CRS-M1-00025` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. |
| `CRS-M1-00032` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. |
| `CRS-M1-00071` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00072` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00073` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00074` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00075` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00076` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00077` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00078` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00079` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00080` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00081` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00082` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00083` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00084` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00085` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00086` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00087` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00088` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00089` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00090` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00091` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00093` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00094` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00095` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00096` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00097` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00098` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00099` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00100` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00101` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00102` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00103` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00104` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00105` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00106` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00107` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00108` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00109` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00124` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00125` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00126` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00127` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00128` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00129` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00130` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00131` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00132` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00133` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00134` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00135` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00136` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00137` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00138` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00139` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00140` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00141` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00142` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00143` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00144` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00145` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00146` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00147` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00148` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00149` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00150` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00151` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00152` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00153` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00154` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00155` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00156` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00157` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00158` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00159` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00160` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00161` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00162` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00163` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00164` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00165` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00166` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00186` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. |
| `CRS-M1-00282` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00283` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00284` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00285` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00286` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00287` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00288` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00289` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00290` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00291` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00292` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00293` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00294` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00295` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00296` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00297` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00298` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00299` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00300` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00301` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00302` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00303` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00304` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00305` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00306` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00307` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00308` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00309` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00310` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00311` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00312` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00313` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00314` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00315` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00316` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00317` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00318` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00319` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00320` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00321` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00322` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00323` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00324` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00325` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00326` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00327` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00328` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00329` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00330` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00331` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00332` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00333` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00346` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00347` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00348` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00349` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00350` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00351` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00352` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00353` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00354` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00355` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00356` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00357` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00358` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00359` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00360` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00361` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00362` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00363` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00364` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00365` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00366` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00367` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00368` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00369` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00370` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00371` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00372` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00373` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00374` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00375` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00376` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00378` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00618` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |
| `CRS-M1-00620` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. |
| `CRS-M1-00622` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |
| `CRS-M1-00632` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |
| `CRS-M1-00645` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |
| `CRS-M1-00646` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |
| `CRS-M1-00647` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |
