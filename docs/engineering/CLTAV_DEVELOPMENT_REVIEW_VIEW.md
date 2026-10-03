# CL-TAV Development Readiness Review View

> Generated from `configs/engineering/cltav_development_contracts.json`; do not edit.

- Control: `CR-2026-016`; decisions DD-038, DD-039, DD-040
- Bound M1 requirements: 863; disposition total: 863; readiness: `READINESS-BLOCKED`; claim: `SPECIFICATION-ONLY`

## Inputs

- `ARINC615A3-M1-CRS` — `configs/requirements/arinc_615a3_m1_crs.json` — SHA-256 `7f35f538fff2d9f8204360f650a1b5c794f9969497ad9ef3f1dfe114248a315f` — Bound protocol requirement universe
- `CLTAV-INTERFACE-REGISTRY` — `configs/research/cltav_interface_registry.json` — SHA-256 `a65679b902cf51d31aa613c133919c3cd2c66dbc6c65eb3cc58d9bf3530d329d` — Accepted interface vocabulary

## Tool requirements

| ID | Owner | Source relation | Acceptance | Requirement |
|---|---|---|---|---|
| `TR-CAPTURE-INTAKE` | `MOD-CAPTURE` | `ENGINEERING-DECISION` | `AC-SYN-TRANSFER` | Preserve capture identity and clock scope |
| `TR-DATAGRAM-REASSEMBLY` | `MOD-REASSEMBLY` | `PROTOCOL-DERIVED` | `AC-SYN-TRANSFER` | Reconstruct only provenance-consistent IPv4 datagrams |
| `TR-TRANSFER-RECONSTRUCTION` | `MOD-TRANSFER` | `PROTOCOL-DERIVED` | `AC-SYN-TRANSFER` | Reconstruct bounded TFTP transfer candidates |
| `TR-PROTOCOL-EVENT` | `MOD-TRANSFER` | `METHOD-DERIVED` | `AC-SYN-TRANSFER` | Derive typed protocol events without inventing application facts |
| `TR-OWNERSHIP` | `MOD-OWNERSHIP` | `METHOD-DERIVED` | `AC-SYN-TRANSFER` | Resolve response ownership conservatively |
| `TR-OBSERVATION-ASSESSMENT` | `MOD-OBSERVATION` | `METHOD-DERIVED` | `AC-SYN-TRANSFER` | Assess observations with explicit timing uncertainty |
| `TR-HISTORY-COMPATIBILITY` | `MOD-OBSERVATION` | `METHOD-DERIVED` | `AC-SYN-TRANSFER` | Update finite compatibility history conservatively |
| `TR-TRACEABLE-FINDING` | `MOD-OBSERVATION` | `ENGINEERING-DECISION` | `AC-SYN-TRANSFER` | Report bounded findings without fault-truth claims |

### `TR-CAPTURE-INTAKE` — Preserve capture identity and clock scope
- Trigger: A caller supplies one manifest-bound capture reference.
- Preconditions: The manifest audit has established a matching relative path, byte size and SHA-256.
- Inputs: `CAPTURE-IDENTITY`; outputs: `PACKET-REF`
- Action: Create a capture-scoped identity; retain section, interface and raw-tick provenance without inferring clock accuracy.
- Error/unknown: Unreadable blocks, unsupported link types and unknown clock accuracy are explicit decode or UNKNOWN metadata outcomes, never IUT FAIL.
- Evidence: CaptureIdentity and PacketRef raw provenance fields.
- Interfaces: `IF-EXECUTE-RECORD`; CRS: —

### `TR-DATAGRAM-REASSEMBLY` — Reconstruct only provenance-consistent IPv4 datagrams
- Trigger: PacketRef records contain IPv4 fragmentation metadata.
- Preconditions: All fragments retain capture, section and interface scope.
- Inputs: `PACKET-REF`; outputs: `DATAGRAM-RECORD`
- Action: Group fragments by scoped identity, retain every source reference, and classify missing or conflicting coverage without last-fragment overwrite.
- Error/unknown: Missing, truncated or overlapping fragments yield an incomplete or conflict record; they do not yield a complete UDP payload.
- Evidence: DatagramRecord fragment references and coverage classification.
- Interfaces: `IF-EXECUTE-RECORD`; CRS: —

### `TR-TRANSFER-RECONSTRUCTION` — Reconstruct bounded TFTP transfer candidates
- Trigger: A complete or classified-incomplete UDP datagram is available.
- Preconditions: Initial request and dynamic TID evidence are distinguishable from ordinary UDP traffic.
- Inputs: `DATAGRAM-RECORD`; outputs: `TRANSFER-RECORD`
- Action: Associate request, option negotiation, DATA/ACK, WAIT, ERROR and ABORT evidence while preserving ambiguity and block-size confirmation state.
- Error/unknown: A rejected option uses its protocol default (including default block size); only missing or insufficient confirmation evidence yields UNKNOWN, and block-wrap beyond the declared bound yields UNSUPPORTED.
- Evidence: TransferRecord endpoint, TID, option and completion evidence.
- Interfaces: `IF-EXECUTE-RECORD`; CRS: `CRS-M1-00021`, `CRS-M1-00025`, `CRS-M1-00032`

### `TR-PROTOCOL-EVENT` — Derive typed protocol events without inventing application facts
- Trigger: A TransferRecord has usable wire evidence.
- Preconditions: The event layer is explicitly WIRE, PARSE-RESULT, APPLICATION or ENVIRONMENT.
- Inputs: `TRANSFER-RECORD`; outputs: `PROTOCOL-EVENT`
- Action: Emit typed events with correlation keys, full raw references and a parse-confidence boundary.
- Error/unknown: Unobservable application decisions remain absent or UNKNOWN; they are not inferred from model state.
- Evidence: ProtocolEvent correlation key and raw PacketRef chain.
- Interfaces: `IF-OBS-INTERPRET`; CRS: —

### `TR-OWNERSHIP` — Resolve response ownership conservatively
- Trigger: A ProtocolEvent may answer a declared request instance.
- Preconditions: Matching policy and event order are available for the candidate instance set.
- Inputs: `PROTOCOL-EVENT`; outputs: `OWNERSHIP-RESULT`
- Action: Apply the declared UNIQUE-KEY, FIFO or MOST-RECENT policy and preserve cancellation, supersession and ambiguity evidence.
- Error/unknown: A response with incompatible possible owners is ambiguous and cannot be consumed as a unique response.
- Evidence: OwnershipResult policy, request instance and supporting event references.
- Interfaces: `IF-OBS-INTERPRET`; CRS: —

### `TR-OBSERVATION-ASSESSMENT` — Assess observations with explicit timing uncertainty
- Trigger: A uniquely owned or explicitly incomplete observation is available.
- Preconditions: Measurement interval, declared domain and error basis are available or explicitly invalid.
- Inputs: `OWNERSHIP-RESULT`, `PROTOCOL-EVENT`; outputs: `OBSERVATION-ASSESSMENT`
- Action: Apply interval topology and the declared conformance domain to produce a four-valued assessment.
- Error/unknown: Empty measurement-domain intersection or invalid time chain is ERROR; boundary overlap is INCONCLUSIVE.
- Evidence: ObservationAssessment interval, domain and uncertainty references.
- Interfaces: `IF-OBS-INTERPRET`; CRS: —

### `TR-HISTORY-COMPATIBILITY` — Update finite compatibility history conservatively
- Trigger: ObservationAssessment returns a normalized admissible outcome.
- Preconditions: The HistoryHandle belongs to the SessionContext and retains its versioned frontiers.
- Inputs: `OBSERVATION-ASSESSMENT`, `HISTORY-HANDLE`; outputs: `HISTORY-HANDLE`
- Action: Intersect only an accepted compatible set with the current hypothesis set and preserve per-hypothesis history.
- Error/unknown: ERROR, UNKNOWN-EFFECT and resource exhaustion do not exclude hypotheses or revive excluded hypotheses.
- Evidence: HistoryHandle version and compatible-state frontier references.
- Interfaces: `IF-HIST-UPDATE`; CRS: —

### `TR-TRACEABLE-FINDING` — Report bounded findings without fault-truth claims
- Trigger: A completed assessment or a named blocked/unknown condition is available.
- Preconditions: All supporting records retain their capture and interpretation provenance.
- Inputs: `OBSERVATION-ASSESSMENT`, `INTAKE-METADATA`; outputs: `FINDING-RECORD`
- Action: Emit observation facts, judgment basis, scope and unresolved assumptions separately from root-cause labels.
- Error/unknown: Unknown topology, clock, configuration or root cause remains explicit and cannot become a fault label.
- Evidence: FindingRecord evidence links and applicability scope.
- Interfaces: `IF-OBS-INTERPRET`; CRS: —

## Slices and dependencies

- `SLICE-OFFLINE-UPLOAD-INFORMATION` — offline capture to traceable report — 176 requirement uses
- dependency `DEP-INTEGRITY`: `BLOCKED`

## Slice membership relations

| Slice | Requirement |
|---|---|
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00021` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00025` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00032` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00071` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00072` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00073` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00074` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00075` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00076` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00077` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00078` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00079` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00080` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00081` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00082` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00083` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00084` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00085` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00086` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00087` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00088` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00089` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00090` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00091` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00093` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00094` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00095` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00096` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00097` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00098` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00099` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00100` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00101` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00102` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00103` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00104` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00105` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00106` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00107` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00108` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00109` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00124` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00125` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00126` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00127` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00128` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00129` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00130` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00131` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00132` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00133` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00134` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00135` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00136` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00137` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00138` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00139` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00140` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00141` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00142` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00143` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00144` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00145` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00146` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00147` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00148` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00149` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00150` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00151` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00152` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00153` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00154` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00155` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00156` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00157` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00158` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00159` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00160` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00161` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00162` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00163` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00164` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00165` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00166` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00186` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00282` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00283` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00284` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00285` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00286` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00287` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00288` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00289` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00290` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00291` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00292` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00293` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00294` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00295` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00296` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00297` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00298` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00299` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00300` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00301` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00302` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00303` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00304` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00305` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00306` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00307` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00308` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00309` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00310` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00311` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00312` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00313` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00314` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00315` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00316` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00317` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00318` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00319` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00320` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00321` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00322` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00323` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00324` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00325` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00326` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00327` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00328` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00329` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00330` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00331` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00332` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00333` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00346` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00347` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00348` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00349` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00350` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00351` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00352` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00353` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00354` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00355` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00356` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00357` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00358` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00359` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00360` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00361` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00362` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00363` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00364` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00365` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00366` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00367` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00368` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00369` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00370` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00371` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00372` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00373` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00374` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00375` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00376` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00378` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00618` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00620` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00622` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00632` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00645` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00646` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00647` |

## Disposition summary

| Disposition | Count |
|---|---:|
| `DEPENDENCY-BLOCKED` | 6 |
| `FIRST-SLICE-IMPLEMENTATION` | 170 |
| `LATER-SERVICE` | 137 |
| `NOT-TOOL-OBLIGATION` | 550 |

## All requirement dispositions

| Requirement | Disposition | First slice | Module | Record | Acceptance | Rationale |
|---|---|---|---|---|---|---|
| `CRS-M1-00001` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00002` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00003` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00004` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00005` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00006` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00007` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00008` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00009` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00010` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00011` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00012` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00013` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00014` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00015` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00016` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00017` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00018` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00019` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00020` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00021` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. |
| `CRS-M1-00022` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00023` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00024` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00025` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. |
| `CRS-M1-00026` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00027` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00028` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00029` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00030` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00031` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00032` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. |
| `CRS-M1-00033` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00034` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00035` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00036` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00037` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00038` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00039` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00040` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00041` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00042` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00043` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00044` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00045` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00046` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00047` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00048` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00049` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00050` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00051` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00052` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00053` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00054` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00055` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00056` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00057` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00058` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00059` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00060` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00061` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00062` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00063` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00064` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00065` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00066` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00067` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00068` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00069` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00070` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00071` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00072` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00073` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00074` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00075` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00076` | `DEPENDENCY-BLOCKED` | `True` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00077` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00078` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00079` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00080` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00081` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00082` | `DEPENDENCY-BLOCKED` | `True` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00083` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00084` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00085` | `DEPENDENCY-BLOCKED` | `True` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00086` | `DEPENDENCY-BLOCKED` | `True` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00087` | `DEPENDENCY-BLOCKED` | `True` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00088` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00089` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00090` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00091` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00092` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00093` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00094` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00095` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00096` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00097` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00098` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00099` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00100` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00101` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00102` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00103` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00104` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00105` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00106` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00107` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00108` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00109` | `DEPENDENCY-BLOCKED` | `True` | `—` | `—` | `—` | First-slice input requires a separately established integrity dependency. |
| `CRS-M1-00110` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00111` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00112` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00113` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00114` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00115` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00116` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00117` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00118` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00119` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00120` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00121` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00122` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00123` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00124` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00125` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00126` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00127` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00128` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00129` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00130` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00131` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00132` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00133` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00134` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00135` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00136` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00137` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00138` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00139` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00140` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00141` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00142` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00143` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00144` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00145` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00146` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00147` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00148` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00149` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00150` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00151` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00152` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00153` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00154` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00155` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00156` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00157` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00158` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00159` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00160` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00161` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00162` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00163` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00164` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00165` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00166` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00167` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00168` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00169` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00170` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00171` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00172` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00173` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00174` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00175` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00176` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00177` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00178` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00179` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00180` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00181` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00182` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00183` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00184` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00185` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00186` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. |
| `CRS-M1-00187` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00188` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00189` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00190` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00191` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00192` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00193` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00194` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00195` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00196` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00197` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00198` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00199` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00200` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00201` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00202` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00203` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00204` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00205` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00206` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00207` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00208` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00209` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00210` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00211` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00212` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00213` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00214` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00215` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00216` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00217` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00218` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00219` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00220` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00221` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00222` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00223` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00224` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00225` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00226` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00227` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00228` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00229` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00230` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00231` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00232` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00233` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00234` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00235` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00236` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00237` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00238` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00239` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00240` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00241` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00242` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00243` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00244` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00245` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00246` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00247` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00248` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00249` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00250` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00251` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00252` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00253` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00254` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00255` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00256` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00257` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00258` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00259` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00260` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00261` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00262` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00263` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00264` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00265` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00266` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00267` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00268` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00269` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00270` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00271` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00272` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00273` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00274` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00275` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00276` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00277` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00278` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00279` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00280` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00281` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00282` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00283` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00284` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00285` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00286` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00287` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00288` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00289` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00290` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00291` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00292` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00293` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00294` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00295` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00296` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00297` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00298` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00299` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00300` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00301` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00302` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00303` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00304` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00305` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00306` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00307` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00308` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00309` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00310` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00311` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00312` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00313` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00314` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00315` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00316` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00317` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00318` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00319` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00320` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00321` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00322` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00323` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00324` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00325` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00326` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00327` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00328` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00329` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00330` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00331` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00332` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00333` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00334` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00335` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00336` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00337` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00338` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00339` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00340` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00341` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00342` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00343` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00344` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00345` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00346` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00347` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00348` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00349` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00350` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00351` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00352` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00353` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00354` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00355` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00356` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00357` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00358` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00359` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00360` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00361` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00362` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00363` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00364` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00365` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00366` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00367` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00368` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00369` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00370` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00371` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00372` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00373` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00374` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00375` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00376` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00377` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00378` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. |
| `CRS-M1-00379` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00380` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00381` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00382` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00383` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00384` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00385` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00386` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00387` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00388` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00389` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00390` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00391` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00392` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00393` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00394` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00395` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00396` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00397` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00398` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00399` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00400` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00401` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00402` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00403` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00404` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00405` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00406` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00407` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00408` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00409` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00410` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00411` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00412` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00413` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00414` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00415` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00416` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00417` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00418` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00419` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00420` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00421` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00422` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00423` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00424` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00426` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00427` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00428` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00429` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00430` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00431` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00432` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00433` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00434` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00435` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00436` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00437` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00438` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00439` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00440` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00441` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00442` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00443` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00444` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00445` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00446` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00447` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00448` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00449` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00450` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00451` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00452` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00453` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00454` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00455` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00456` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00457` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00458` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00459` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00460` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00461` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00462` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00463` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00464` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00465` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00466` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00467` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00468` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00469` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00470` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00471` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00472` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00473` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00474` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00475` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00476` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00477` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00478` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00479` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00480` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00481` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00482` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00483` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00484` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00485` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00486` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00487` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00488` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00489` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00490` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00491` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00492` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00493` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00494` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00495` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00496` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00497` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00498` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00499` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00500` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00501` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00502` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00503` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00504` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00505` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00506` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00507` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00508` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00509` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00510` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00511` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00512` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00513` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00514` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00515` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00516` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00517` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00518` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00519` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00520` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00521` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00522` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00523` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00524` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00525` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00526` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00527` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00528` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00529` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00530` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00531` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00532` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00533` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00534` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00535` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00536` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00537` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00538` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00539` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00540` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00541` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00542` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00543` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00544` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00545` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00546` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00547` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00548` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00549` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00550` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00551` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00552` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00553` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00554` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00555` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00556` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00557` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00558` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00559` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00560` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00561` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00562` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00563` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00564` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00565` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00566` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00567` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00568` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00569` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00570` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00571` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00572` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00573` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00574` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00575` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00576` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00577` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00578` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00579` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00580` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00581` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00582` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00583` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00584` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00585` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00586` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00587` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00588` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00589` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00590` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00591` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00592` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00593` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00594` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00595` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00596` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00597` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00598` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00599` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00600` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00601` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00602` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00603` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00604` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00605` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00606` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00607` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00608` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00609` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00610` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00611` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00612` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00613` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00614` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00615` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00616` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00617` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00618` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |
| `CRS-M1-00619` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00620` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. |
| `CRS-M1-00621` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00622` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |
| `CRS-M1-00623` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00624` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00625` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00626` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00627` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00628` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00629` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00630` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00631` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00632` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |
| `CRS-M1-00633` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00634` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00635` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00636` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00637` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00638` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00639` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00640` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00641` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00642` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00643` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00644` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00645` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |
| `CRS-M1-00646` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |
| `CRS-M1-00647` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. |
| `CRS-M1-00648` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00649` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00650` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00651` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00652` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00653` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00654` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00655` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00656` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00657` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00658` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00659` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00660` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00661` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00662` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00663` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00664` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00665` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00666` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00667` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00668` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00669` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00670` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00671` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00672` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00673` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00674` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00675` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00676` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00677` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00678` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00679` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00680` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00681` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00682` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00683` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00684` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00685` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00686` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00687` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00688` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00689` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00690` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00691` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00692` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00693` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00694` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00695` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00696` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00697` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00698` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00699` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00700` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00701` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00702` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00703` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00704` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00705` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00706` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00707` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00708` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00709` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00710` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00711` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00712` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00713` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00714` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00715` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00716` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00717` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00718` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00719` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00720` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00721` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00722` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00723` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00724` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00725` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00726` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00727` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00728` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00729` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00730` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00731` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00732` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00733` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00734` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00735` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00736` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00737` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00738` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00739` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00740` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00741` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00742` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00743` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00744` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00745` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00746` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00747` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00748` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00749` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00750` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00751` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00752` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00753` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00754` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00755` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00756` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00757` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00758` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00759` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00760` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00761` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00762` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00763` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00764` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00765` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00766` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00767` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00768` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00769` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00770` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00771` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00772` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00773` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00774` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00775` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00776` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00777` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00778` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00779` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00780` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00781` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00782` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00783` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00784` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00785` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00786` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00787` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00788` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00789` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00790` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00791` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00792` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00793` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00794` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00795` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00796` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00797` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00798` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00799` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00800` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00801` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00802` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00803` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00804` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00805` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00806` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00807` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00808` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00809` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00810` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00811` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00812` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00813` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00814` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00815` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00816` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00817` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00818` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00819` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00820` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00821` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00822` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00823` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00824` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00825` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00826` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00827` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00828` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00829` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00830` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00831` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00832` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00833` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00834` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00835` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00836` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00837` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00838` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00839` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00840` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00841` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00842` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00843` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00844` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00845` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00846` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00847` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00848` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00849` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00850` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00851` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00852` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00853` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00854` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00855` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00856` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00857` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00858` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00859` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00860` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00861` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00862` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00863` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |
| `CRS-M1-00864` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. |

# 中文版

# CL-TAV 开发就绪评审视图

> 由同一权威 JSON 生成，禁止手工修改。

- 控制：`CR-2026-016`；设计决策：`DD-038`, `DD-039`, `DD-040`
- 绑定 M1 需求：863；处置合计：863；就绪状态：`READINESS-BLOCKED`；主张边界：`SPECIFICATION-ONLY`

## 输入身份

- `ARINC615A3-M1-CRS` — `configs/requirements/arinc_615a3_m1_crs.json` — SHA-256 `7f35f538fff2d9f8204360f650a1b5c794f9969497ad9ef3f1dfe114248a315f` — 受控协议需求全集
- `CLTAV-INTERFACE-REGISTRY` — `configs/research/cltav_interface_registry.json` — SHA-256 `a65679b902cf51d31aa613c133919c3cd2c66dbc6c65eb3cc58d9bf3530d329d` — 已接受的接口词汇表

## 工具需求

| ID | 责任模块 | 来源关系 | 验收 | 需求 |
|---|---|---|---|---|
| `TR-CAPTURE-INTAKE` | `MOD-CAPTURE` | `ENGINEERING-DECISION` | `AC-SYN-TRANSFER` | 保留捕获身份与时钟作用域 |
| `TR-DATAGRAM-REASSEMBLY` | `MOD-REASSEMBLY` | `PROTOCOL-DERIVED` | `AC-SYN-TRANSFER` | 仅重组来源一致的 IPv4 数据报 |
| `TR-TRANSFER-RECONSTRUCTION` | `MOD-TRANSFER` | `PROTOCOL-DERIVED` | `AC-SYN-TRANSFER` | 重建有界 TFTP 传输候选 |
| `TR-PROTOCOL-EVENT` | `MOD-TRANSFER` | `METHOD-DERIVED` | `AC-SYN-TRANSFER` | 在不虚构应用事实的前提下派生带类型协议事件 |
| `TR-OWNERSHIP` | `MOD-OWNERSHIP` | `METHOD-DERIVED` | `AC-SYN-TRANSFER` | 保守解析响应所有权 |
| `TR-OBSERVATION-ASSESSMENT` | `MOD-OBSERVATION` | `METHOD-DERIVED` | `AC-SYN-TRANSFER` | 以显式时序不确定性评估观测 |
| `TR-HISTORY-COMPATIBILITY` | `MOD-OBSERVATION` | `METHOD-DERIVED` | `AC-SYN-TRANSFER` | 保守更新有限相容历史 |
| `TR-TRACEABLE-FINDING` | `MOD-OBSERVATION` | `ENGINEERING-DECISION` | `AC-SYN-TRANSFER` | 在不作故障真值主张的前提下报告有界发现 |

### `TR-CAPTURE-INTAKE` — 保留捕获身份与时钟作用域
- 触发：调用方提供清单绑定的捕获引用。
- 前置条件：清单审计已确认相对路径、大小和 SHA-256。
- 输入：`CAPTURE-IDENTITY`；输出：`PACKET-REF`
- 动作：建立捕获作用域身份，保留 section、interface 与原始 ticks 来源，不推断时钟精度。
- 错误／未知：不可读块、未支持链路类型和未知时钟精度返回解码或 UNKNOWN 元数据，不是 IUT FAIL。
- 证据：CaptureIdentity 与 PacketRef 的原始来源字段。
- 接口：`IF-EXECUTE-RECORD`；CRS：—

### `TR-DATAGRAM-REASSEMBLY` — 仅重组来源一致的 IPv4 数据报
- 触发：PacketRef 含 IPv4 分片元数据。
- 前置条件：所有分片保留 capture、section 与 interface 作用域。
- 输入：`PACKET-REF`；输出：`DATAGRAM-RECORD`
- 动作：按作用域身份分组，保留全部来源并分类缺失或冲突覆盖。
- 错误／未知：缺片、截断或重叠产生不完整或冲突记录，不产生完整 UDP 载荷。
- 证据：DatagramRecord 分片引用与覆盖分类。
- 接口：`IF-EXECUTE-RECORD`；CRS：—

### `TR-TRANSFER-RECONSTRUCTION` — 重建有界 TFTP 传输候选
- 触发：存在完整或已分类不完整的 UDP 数据报。
- 前置条件：初始请求与动态 TID 证据可同普通 UDP 区分。
- 输入：`DATAGRAM-RECORD`；输出：`TRANSFER-RECORD`
- 动作：关联请求、选项协商、DATA/ACK、WAIT、ERROR 与 ABORT，保留歧义和块大小确认状态。
- 错误／未知：显式拒绝选项采用协议默认值；仅确认信息不足为 UNKNOWN；超出块回绕界为 UNSUPPORTED。
- 证据：TransferRecord 的端点、TID、选项与完成证据。
- 接口：`IF-EXECUTE-RECORD`；CRS：`CRS-M1-00021`, `CRS-M1-00025`, `CRS-M1-00032`

### `TR-PROTOCOL-EVENT` — 在不虚构应用事实的前提下派生带类型协议事件
- 触发：TransferRecord 含可用线上证据。
- 前置条件：事件层已明确为 WIRE、PARSE-RESULT、APPLICATION 或 ENVIRONMENT。
- 输入：`TRANSFER-RECORD`；输出：`PROTOCOL-EVENT`
- 动作：产生带关联键、完整原始引用和解析可信边界的类型化事件。
- 错误／未知：不可观察的应用决定保持缺失或 UNKNOWN，不从模型状态推断。
- 证据：ProtocolEvent 关联键及原始 PacketRef 链。
- 接口：`IF-OBS-INTERPRET`；CRS：—

### `TR-OWNERSHIP` — 保守解析响应所有权
- 触发：ProtocolEvent 可能响应已声明的请求实例。
- 前置条件：候选实例集合具匹配策略和事件顺序。
- 输入：`PROTOCOL-EVENT`；输出：`OWNERSHIP-RESULT`
- 动作：应用 UNIQUE-KEY、FIFO 或 MOST-RECENT，并保留取消、替代和歧义证据。
- 错误／未知：可能所有者不相容时为歧义，不能作为唯一响应消费。
- 证据：OwnershipResult 的策略、请求实例和支持事件引用。
- 接口：`IF-OBS-INTERPRET`；CRS：—

### `TR-OBSERVATION-ASSESSMENT` — 以显式时序不确定性评估观测
- 触发：存在唯一归属或明确不完整的观测。
- 前置条件：测量区间、声明域和误差依据可用或已明确无效。
- 输入：`OWNERSHIP-RESULT`, `PROTOCOL-EVENT`；输出：`OBSERVATION-ASSESSMENT`
- 动作：以区间拓扑和声明符合性域产生四值评估。
- 错误／未知：测量域交集为空为 ERROR；边界重叠为 INCONCLUSIVE。
- 证据：ObservationAssessment 区间、域和不确定性引用。
- 接口：`IF-OBS-INTERPRET`；CRS：—

### `TR-HISTORY-COMPATIBILITY` — 保守更新有限相容历史
- 触发：ObservationAssessment 返回规范化可接纳结果。
- 前置条件：HistoryHandle 属于 SessionContext 并保留有版本前沿。
- 输入：`OBSERVATION-ASSESSMENT`, `HISTORY-HANDLE`；输出：`HISTORY-HANDLE`
- 动作：仅将接纳的相容集合与当前假设集合相交，并保留逐假设历史。
- 错误／未知：ERROR、UNKNOWN-EFFECT 和资源耗尽不排除或复活假设。
- 证据：HistoryHandle 版本及相容状态前沿引用。
- 接口：`IF-HIST-UPDATE`；CRS：—

### `TR-TRACEABLE-FINDING` — 在不作故障真值主张的前提下报告有界发现
- 触发：存在完成评估或具名 blocked/unknown 条件。
- 前置条件：所有支持记录保留捕获和解释来源。
- 输入：`OBSERVATION-ASSESSMENT`, `INTAKE-METADATA`；输出：`FINDING-RECORD`
- 动作：输出观测事实、判断依据、范围和未决假设，并与根因标签分离。
- 错误／未知：未知拓扑、时钟、配置或根因保持显式，不能成为故障标签。
- 证据：FindingRecord 证据链接和适用范围。
- 接口：`IF-OBS-INTERPRET`；CRS：—

## 切片与依赖

- `SLICE-OFFLINE-UPLOAD-INFORMATION` — 离线捕获至可追踪报告 — 176 条需求用途
- 依赖 `DEP-INTEGRITY`：`BLOCKED`

## 切片成员关系

| 切片 | 需求 |
|---|---|
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00021` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00025` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00032` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00071` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00072` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00073` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00074` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00075` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00076` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00077` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00078` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00079` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00080` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00081` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00082` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00083` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00084` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00085` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00086` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00087` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00088` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00089` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00090` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00091` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00093` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00094` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00095` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00096` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00097` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00098` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00099` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00100` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00101` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00102` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00103` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00104` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00105` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00106` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00107` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00108` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00109` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00124` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00125` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00126` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00127` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00128` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00129` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00130` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00131` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00132` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00133` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00134` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00135` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00136` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00137` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00138` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00139` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00140` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00141` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00142` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00143` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00144` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00145` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00146` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00147` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00148` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00149` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00150` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00151` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00152` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00153` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00154` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00155` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00156` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00157` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00158` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00159` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00160` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00161` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00162` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00163` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00164` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00165` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00166` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00186` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00282` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00283` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00284` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00285` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00286` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00287` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00288` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00289` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00290` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00291` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00292` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00293` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00294` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00295` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00296` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00297` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00298` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00299` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00300` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00301` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00302` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00303` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00304` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00305` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00306` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00307` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00308` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00309` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00310` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00311` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00312` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00313` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00314` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00315` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00316` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00317` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00318` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00319` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00320` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00321` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00322` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00323` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00324` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00325` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00326` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00327` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00328` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00329` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00330` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00331` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00332` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00333` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00346` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00347` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00348` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00349` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00350` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00351` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00352` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00353` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00354` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00355` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00356` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00357` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00358` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00359` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00360` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00361` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00362` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00363` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00364` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00365` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00366` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00367` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00368` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00369` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00370` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00371` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00372` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00373` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00374` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00375` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00376` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00378` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00618` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00620` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00622` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00632` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00645` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00646` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00647` |

## 处置摘要

| 处置 | 数量 |
|---|---:|
| `DEPENDENCY-BLOCKED` | 6 |
| `FIRST-SLICE-IMPLEMENTATION` | 170 |
| `LATER-SERVICE` | 137 |
| `NOT-TOOL-OBLIGATION` | 550 |

## 全部需求处置

| 需求 | 处置 | 首轮 | 模块 | 记录 | 验收 | 理由 |
|---|---|---|---|---|---|---|
| `CRS-M1-00001` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00002` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00003` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00004` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00005` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00006` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00007` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00008` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00009` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00010` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00011` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00012` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00013` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00014` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00015` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00016` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00017` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00018` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00019` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00020` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00021` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 COMMON 时序、TFTP 传输或末块观测合同。 |
| `CRS-M1-00022` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00023` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00024` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00025` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 COMMON 时序、TFTP 传输或末块观测合同。 |
| `CRS-M1-00026` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00027` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00028` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00029` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00030` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00031` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00032` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 COMMON 时序、TFTP 传输或末块观测合同。 |
| `CRS-M1-00033` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00034` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00035` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00036` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00037` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00038` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00039` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00040` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00041` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00042` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00043` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00044` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00045` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00046` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00047` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00048` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00049` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00050` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00051` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00052` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00053` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00054` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00055` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00056` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00057` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00058` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00059` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00060` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00061` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00062` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00063` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00064` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00065` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00066` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00067` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00068` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00069` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00070` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00071` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00072` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00073` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00074` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00075` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00076` | `DEPENDENCY-BLOCKED` | `True` | `—` | `—` | `—` | 首轮输入需要单独建立的完整性依赖。 |
| `CRS-M1-00077` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00078` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00079` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00080` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00081` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00082` | `DEPENDENCY-BLOCKED` | `True` | `—` | `—` | `—` | 首轮输入需要单独建立的完整性依赖。 |
| `CRS-M1-00083` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00084` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00085` | `DEPENDENCY-BLOCKED` | `True` | `—` | `—` | `—` | 首轮输入需要单独建立的完整性依赖。 |
| `CRS-M1-00086` | `DEPENDENCY-BLOCKED` | `True` | `—` | `—` | `—` | 首轮输入需要单独建立的完整性依赖。 |
| `CRS-M1-00087` | `DEPENDENCY-BLOCKED` | `True` | `—` | `—` | `—` | 首轮输入需要单独建立的完整性依赖。 |
| `CRS-M1-00088` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00089` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00090` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00091` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00092` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00093` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00094` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00095` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00096` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00097` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00098` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00099` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00100` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00101` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00102` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00103` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00104` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00105` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00106` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00107` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00108` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00109` | `DEPENDENCY-BLOCKED` | `True` | `—` | `—` | `—` | 首轮输入需要单独建立的完整性依赖。 |
| `CRS-M1-00110` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00111` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00112` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00113` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00114` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00115` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00116` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00117` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00118` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00119` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00120` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00121` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00122` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00123` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00124` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00125` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00126` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00127` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00128` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00129` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00130` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00131` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00132` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00133` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00134` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00135` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00136` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00137` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00138` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00139` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00140` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00141` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00142` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00143` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00144` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00145` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00146` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00147` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00148` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00149` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00150` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00151` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00152` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00153` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00154` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00155` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00156` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00157` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00158` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00159` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00160` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00161` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00162` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00163` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00164` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00165` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00166` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00167` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00168` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00169` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00170` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00171` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00172` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00173` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00174` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00175` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00176` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00177` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00178` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00179` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00180` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00181` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00182` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00183` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00184` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00185` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00186` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 COMMON 时序、TFTP 传输或末块观测合同。 |
| `CRS-M1-00187` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00188` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00189` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00190` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00191` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00192` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00193` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00194` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00195` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00196` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00197` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00198` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00199` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00200` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00201` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00202` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00203` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00204` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00205` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00206` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00207` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00208` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00209` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00210` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00211` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00212` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00213` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00214` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00215` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00216` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00217` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00218` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00219` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00220` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00221` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00222` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00223` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00224` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00225` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00226` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00227` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00228` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00229` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00230` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00231` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00232` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00233` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00234` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00235` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00236` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00237` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00238` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00239` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00240` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00241` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00242` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00243` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00244` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00245` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00246` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00247` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00248` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00249` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00250` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00251` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00252` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00253` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00254` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00255` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00256` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00257` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00258` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00259` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00260` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00261` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00262` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00263` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00264` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00265` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00266` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00267` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00268` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00269` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00270` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00271` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00272` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00273` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00274` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00275` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00276` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00277` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00278` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00279` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00280` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00281` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00282` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00283` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00284` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00285` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00286` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00287` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00288` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00289` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00290` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00291` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00292` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00293` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00294` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00295` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00296` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00297` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00298` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00299` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00300` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00301` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00302` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00303` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00304` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00305` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00306` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00307` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00308` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00309` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00310` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00311` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00312` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00313` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00314` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00315` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00316` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00317` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00318` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00319` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00320` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00321` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00322` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00323` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00324` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00325` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00326` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00327` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00328` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00329` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00330` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00331` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00332` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00333` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00334` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00335` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00336` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00337` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00338` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00339` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00340` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00341` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00342` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00343` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00344` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00345` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00346` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00347` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00348` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00349` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00350` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00351` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00352` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00353` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00354` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00355` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00356` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00357` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00358` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00359` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00360` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00361` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00362` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00363` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00364` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00365` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00366` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00367` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00368` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00369` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00370` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00371` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00372` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00373` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00374` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00375` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00376` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00377` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00378` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 |
| `CRS-M1-00379` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00380` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00381` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00382` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00383` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00384` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00385` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00386` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00387` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00388` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00389` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00390` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00391` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00392` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00393` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00394` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00395` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00396` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00397` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00398` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00399` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00400` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00401` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00402` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00403` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00404` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00405` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00406` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00407` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00408` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00409` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00410` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00411` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00412` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00413` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00414` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00415` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00416` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00417` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00418` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00419` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00420` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00421` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00422` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00423` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00424` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00426` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00427` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00428` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00429` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00430` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00431` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00432` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00433` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00434` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00435` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00436` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00437` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00438` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00439` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00440` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00441` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00442` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00443` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00444` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00445` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00446` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00447` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00448` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00449` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00450` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00451` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00452` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00453` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00454` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00455` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00456` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00457` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00458` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00459` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00460` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00461` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00462` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00463` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00464` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00465` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00466` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00467` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00468` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00469` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00470` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00471` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00472` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00473` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00474` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00475` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00476` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00477` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00478` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00479` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00480` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00481` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00482` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00483` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00484` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00485` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00486` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00487` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00488` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00489` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00490` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00491` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00492` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00493` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00494` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00495` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00496` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00497` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00498` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00499` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00500` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00501` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00502` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00503` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00504` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00505` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00506` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00507` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00508` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00509` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00510` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00511` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00512` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00513` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00514` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00515` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00516` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00517` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00518` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00519` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00520` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00521` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00522` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00523` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00524` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00525` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00526` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00527` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00528` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00529` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00530` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00531` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00532` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00533` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00534` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00535` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00536` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00537` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00538` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00539` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00540` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00541` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00542` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00543` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00544` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00545` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00546` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00547` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00548` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00549` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00550` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00551` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00552` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00553` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00554` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00555` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00556` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00557` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00558` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00559` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00560` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00561` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00562` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00563` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00564` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00565` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00566` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00567` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00568` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00569` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00570` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00571` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00572` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00573` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00574` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00575` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00576` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00577` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00578` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00579` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00580` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00581` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00582` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00583` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00584` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00585` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00586` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00587` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00588` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00589` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00590` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00591` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00592` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00593` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00594` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00595` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00596` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00597` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00598` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00599` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00600` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00601` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00602` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00603` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00604` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00605` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00606` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00607` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00608` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00609` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00610` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00611` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00612` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00613` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00614` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00615` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00616` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00617` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00618` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 TFTP 传输身份、选项确认、请求布局或终止重建。 |
| `CRS-M1-00619` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00620` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 COMMON 时序、TFTP 传输或末块观测合同。 |
| `CRS-M1-00621` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00622` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 TFTP 传输身份、选项确认、请求布局或终止重建。 |
| `CRS-M1-00623` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00624` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00625` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00626` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00627` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00628` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00629` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00630` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00631` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00632` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 TFTP 传输身份、选项确认、请求布局或终止重建。 |
| `CRS-M1-00633` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00634` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00635` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00636` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00637` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00638` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00639` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00640` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00641` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00642` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00643` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00644` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00645` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 TFTP 传输身份、选项确认、请求布局或终止重建。 |
| `CRS-M1-00646` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 TFTP 传输身份、选项确认、请求布局或终止重建。 |
| `CRS-M1-00647` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 TFTP 传输身份、选项确认、请求布局或终止重建。 |
| `CRS-M1-00648` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00649` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00650` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00651` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00652` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00653` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00654` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00655` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00656` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00657` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00658` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00659` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00660` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00661` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00662` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00663` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00664` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00665` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00666` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00667` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00668` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00669` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00670` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00671` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00672` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00673` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00674` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00675` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00676` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00677` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00678` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00679` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00680` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00681` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00682` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00683` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00684` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00685` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00686` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00687` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00688` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00689` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00690` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00691` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00692` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00693` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00694` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00695` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00696` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00697` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00698` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00699` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00700` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00701` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00702` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00703` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00704` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00705` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00706` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00707` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00708` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00709` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00710` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00711` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00712` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00713` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00714` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00715` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00716` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00717` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00718` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00719` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00720` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00721` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00722` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00723` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00724` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00725` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00726` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00727` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00728` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00729` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00730` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00731` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00732` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00733` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00734` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00735` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00736` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00737` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00738` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00739` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00740` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00741` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00742` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00743` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00744` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00745` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00746` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00747` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00748` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00749` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00750` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00751` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00752` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00753` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00754` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00755` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00756` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00757` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00758` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00759` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00760` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00761` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00762` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00763` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00764` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00765` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00766` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00767` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00768` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00769` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00770` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00771` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00772` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00773` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00774` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00775` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00776` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00777` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00778` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00779` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00780` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00781` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00782` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00783` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00784` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00785` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00786` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00787` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00788` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00789` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00790` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00791` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00792` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00793` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00794` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00795` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00796` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00797` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00798` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00799` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00800` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00801` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00802` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00803` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00804` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00805` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00806` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00807` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00808` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00809` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00810` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00811` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00812` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00813` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00814` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00815` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00816` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00817` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00818` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00819` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00820` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00821` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00822` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00823` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00824` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00825` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00826` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00827` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00828` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00829` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00830` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00831` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00832` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00833` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00834` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00835` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00836` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00837` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00838` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00839` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00840` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00841` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00842` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00843` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00844` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00845` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00846` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00847` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00848` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00849` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00850` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00851` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00852` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00853` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00854` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00855` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00856` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00857` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00858` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00859` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00860` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00861` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00862` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00863` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
| `CRS-M1-00864` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 |
