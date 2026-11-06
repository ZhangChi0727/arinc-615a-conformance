# 615A UPLOAD LUR-Start Engineering Scenario Prototype

> Generated from `configs/engineering/cltav_615a_scenarios.json`; do not edit this view directly. It is a bounded engineering specification, not a protocol conformance verdict, experiment result, or capability claim.

- Artifact: `CLTAV-615A-SCENARIO-PACKAGE`; family: `ENG-UPLOAD-LUR-START`; version: `0.2.0-b-candidate`
- Control: `CR-2026-022` / `DD-046`; accepted authority commit: `c577f34e98b91083a69f0a731a990c01aa7fa08b`
- Immutable G0 control record: `docs/control/changes/CR-2026-022.md` @ `331abdf26b550111df56226a88ca5a6a989c1d76`; Git blob `e031045720207218bbc24c810e7f4d33d5d76791`; SHA-256 `d4db86a0eb6e2d9d81504865126d91728a3463ecf9090bf169b8180e26448719`
- Classification: `SYNTHETIC-ENGINEERING-VALIDATION`; stage: `B-OBJECT-LIFECYCLE-CANDIDATE-PENDING-INDEPENDENT-REVIEW`

## Accepted authority snapshot

| Path | Role | Commit | Git blob | SHA-256 |
|---|---|---|---|---|
| configs/engineering/cltav_development_contracts.json | DEVELOPMENT-CONTRACT | c577f34e98b91083a69f0a731a990c01aa7fa08b | aad74f8c5ac3ab47a5c7b4b85e51e1174c6b664e | 3331fadf2786133f161eded9d1fb42066ca58d7dd510ce6e775da1cd89a5aae1 |
| configs/engineering/cltav_runtime_applicability.json | RUNTIME-APPLICABILITY | c577f34e98b91083a69f0a731a990c01aa7fa08b | b18b0f66741c313e8eb50f964606e5332d60236b | 5fe77badebe95da8c88b8480647e80b96cd5bd9ee5ac5609f0aed80cca4c70f8 |
| configs/models/arinc_615a3_m2_model.json | ACCEPTED-M2 | c577f34e98b91083a69f0a731a990c01aa7fa08b | 9e311e60824194c5f15174543a28cdc070321a0a | 32b92b1eb4a54c603386363a3cdf3a0fc4d1c44af7cead2115a4226282fa1684 |
| configs/requirements/arinc_615a3_m1_crs.json | ACCEPTED-CRS | c577f34e98b91083a69f0a731a990c01aa7fa08b | 44b471aa25ceb6af0d0a6fdd610e25cd02f92b7b | 56e214f089e6563e53e3991e7a8e7892f163840bb2c1d7d39f4a9ce92fc16758 |
| configs/research/cltav_experiment_design.json | EXPERIMENT-DESIGN | c577f34e98b91083a69f0a731a990c01aa7fa08b | 426240668cb8112347fd37c8d2ee56b36078bddb | c0161e2772825ce0a471dbf79e0ac27bf7ade20579655bfccacc8c6d2e451178 |
| configs/research/cltav_interface_registry.json | INTERFACE-REGISTRY | c577f34e98b91083a69f0a731a990c01aa7fa08b | a7202e42f07e69b5d9c1f95137e093c16e1c1ab8 | a65679b902cf51d31aa613c133919c3cd2c66dbc6c65eb3cc58d9bf3530d329d |
| pyproject.toml | INSTALLATION-CONTRACT | c577f34e98b91083a69f0a731a990c01aa7fa08b | 577ea125717d0ece52c17a6bfaee3c5b3b9c55f8 | d8aee77b0f7850255b9a4991004d819f0259cab5e7dde6dab20efb344c77e0b3 |
| src/cltav_runtime/session.py | RUNTIME-SEAM | c577f34e98b91083a69f0a731a990c01aa7fa08b | 7c73ae9a87d1098b1a527abf20705a7affe7abae | d13ce2aadfe35262dc2e628ddbf262de2c518f84afd17a06536defd0aba36c57 |
| src/cltav_runtime/synthetic.py | RUNTIME-SEAM | c577f34e98b91083a69f0a731a990c01aa7fa08b | 1eebb2854ae702302aee172a00ce5ff3e090263e | 9410082b4c8ecf2f35457046829477d51392423477aa687a433ec020da644271 |

## Scope and boundary

- Operation / roles: `UPLOAD` / DATA-LOADER<br>TARGET-HARDWARE
- Start / end: `LIST-SUBMISSION-PRECONDITION-RECORDED` / `LUR-CONTROL-SLICE-OBSERVATION-END`
- Prepared but not executed: EV_DL_OFFER_LIST<br>UPLOAD-INITIALIZATION<br>FULL-LUR-BYTES<br>CRC-CHECK-VALUE-NAMING
- Not evaluated: FULL-UPLOAD-COMPLETION<br>LUR-PAYLOAD-INTEGRITY<br>CRC-CHECK-VALUE-NAMING-CAPABILITY<br>PROTOCOL-NO-RESPONSE-DEADLINE<br>REAL-NETWORK-OR-IUT<br>FOUR-ARM-EXPERIMENT
- Experiment relation: `SC-NORMAL-UPLOAD` / `PREPARES-INTERFACE` — The LUR-start slice records engineering interfaces only; it does not demonstrate qualified UPLOAD completion or admitted experiment execution.
## Object and peer contract

- Stage: `B-OBJECT-LIFECYCLE-CANDIDATE-PENDING-INDEPENDENT-REVIEW`; object: `IN-PROCESS-CONTROLLED-DATA-LOADER-SURROGATE`; peer: `IN-PROCESS-CONTROLLED-TARGET-HARDWARE-DRIVER`.

### State and invariants

| State | M2/source anchor | Initial | Owner | Invariant |
|---|---|---|---|---|
| LIST-ACCEPTED | M2-VARIABLE:listAccepted | FALSE | DATA-LOADER | The normal WRQ guard reads FALSE and only the controlled WRQ transition writes TRUE. |
| LIST-OFFERED | M2-VARIABLE:listOffered | FALSE | DATA-LOADER | The named application-layer list-submission preparation boundary establishes this state; it is not a fabricated wire event. |
| MATCHING-LUR-ACK | M2-STATE:S_UPL_LUR_ACK | FALSE | DATA-LOADER | Only a current-session ACK correlated to the preceding LUR WRQ establishes this state for normal DATA emission. |
| TARGET-LIST-READY | M2-VARIABLE:targetListReady | FALSE | DATA-LOADER | Only the current-session EV_TH_LUS0001 stimulus establishes readiness; readiness does not itself accept the list. |
| TH-MATCHING-LUR-WRQ-RECEIVED | M2-STATE:S_UPL_LUR_WRQ | FALSE | TARGET-HARDWARE | Only a current-session LUR WRQ establishes the peer state that permits the matching TH ACK emission. |

### Guards and fault bypasses

| Guard | Source relation | Required state | Normal visible output | Fault bypass |
|---|---|---|---|---|
| GUARD-DATA-AFTER-MATCHING-ACK | SRC-LUR-DATA | MATCHING-LUR-ACK=TRUE | OUT-DL-DATA-LUR | EARLY-DATA |
| GUARD-TH-ACK-AFTER-MATCHING-WRQ | SRC-LUR-ACK | TH-MATCHING-LUR-WRQ-RECEIVED=TRUE | OUT-TH-ACK-LUR | NO-FAULT-BYPASS |
| GUARD-WRQ-AFTER-READY | SRC-LUR-WRQ | LIST-OFFERED=TRUE<br>TARGET-LIST-READY=TRUE<br>LIST-ACCEPTED=FALSE | OUT-DL-WRQ-LUR | EARLY-WRQ |

### Public stimuli and visible outputs

| Type | Identifier | Source relation | Event | Visibility |
|---|---|---|---|---|
| Public stimulus | STIM-LIST-SUBMISSION-PRECONDITION | SRC-LIST-OFFER-PRECONDITION | EV_DL_OFFER_LIST | APPLICATION |
| Public stimulus | STIM-TH-ACK-LUR | SRC-LUR-ACK | EV_TH_ACK_LUR | NETWORK-VISIBLE |
| Public stimulus | STIM-TH-LUS0001 | SRC-LUS-READY | EV_TH_LUS0001 | NETWORK-VISIBLE |
| Type | Identifier | Source relation | Event | Visibility |
|---|---|---|---|---|
| Visible output | OUT-DL-DATA-LUR | SRC-LUR-DATA | EV_DL_DATA_LUR | NETWORK-VISIBLE |
| Visible output | OUT-DL-WRQ-LUR | SRC-LUR-WRQ | EV_DL_WRQ_LUR | NETWORK-VISIBLE |
| Visible output | OUT-TH-ACK-LUR | SRC-LUR-ACK | EV_TH_ACK_LUR | NETWORK-VISIBLE |

### File role, semantic opcode and private projection

- File role: `LUR`; semantic opcodes: WRQ<br>ACK<br>DATA; payload representation: `OPAQUE-NO-LUR-BYTE-PAYLOAD-OR-CHECKSUM-EVALUATED`; not a wire-packet implementation: yes.
- Evaluator-only: ACTIVE-FAULT-ID<br>FAULT-INSTALLATION-READBACK<br>FAULT-ACTIVATION-RECORD<br>PRIVATE-LOADER-STATE<br>EXPECTED-FINAL-H; algorithm-forbidden: ACTIVE-FAULT-ID<br>FAULT-INSTALLATION-READBACK<br>FAULT-ACTIVATION-RECORD<br>PRIVATE-LOADER-STATE<br>EXPECTED-FINAL-H; permitted public projection: DECLARED-HYPOTHESIS-DOMAIN<br>DECLARED-PREDICTIONS<br>PUBLIC-SCENE-CONFIGURATION<br>TYPED-ACTION-AND-OBSERVATION-INTERFACE.

### Fault revocation and implementation identity plan

- Installation lifetime: `CURRENT-ENGINEERING-ATTEMPT-UNTIL-FULL-RESET`; revocation action: `FULL-RESET-REVOKES-ALL-NAMED-VARIANTS`; revocation evidence: `RESET-READBACK-FAULT-INSTALLATION-STATE-CLEARED`.
- Identity status: `SOURCE-OBJECT-CANDIDATE-PENDING-INDEPENDENT-REVIEW`; source root: `src/cltav_615a`; direct entry point: `cltav_615a.LurStartController`; downstream implementation must bind: OBJECT-SOURCE-COMMIT<br>OBJECT-DISTRIBUTION-IDENTITY<br>ADAPTER-SOURCE-IDENTITY.
- B source identity scheme: `CLTAV-615A-LOADED-SOURCE-SHA256-LF-V1`; load verification: `MODULE-CODE-EQUALITY-FROZEN-SOURCE-AND-CONSTRUCTOR-DRIFT-CHECK`; audit linkage: `FROZEN-MANIFEST-IN-ATTEMPT-AUDIT-SHARED-CODE-IDENTITY`.
- B bound source files: src/cltav_615a/__init__.py<br>src/cltav_615a/controller.py<br>src/cltav_615a/objects.py<br>src/cltav_615a/source_identity.py<br>src/cltav_615a/types.py.
- B binds the five tracked ordinary source files to the executing module code, freezes their LF-normalized content hashes, and rejects missing or changed source before construction. Reset, installation, activation and attempt audit reference that manifest identity. A caller run label is evaluator-only and cannot replace it; public events contain neither label nor source identity. This is controlled normal-load provenance, not a malicious-code sandbox. C adapter and D distribution binding remain unestablished; a review commit pin complements, not replaces, the B content binding.
- Not established: The bounded source-controlled Loader/TH surrogate is available only for direct synthetic engineering validation; no real-IUT identity, CL-TAV adapter, experiment execution, or protocol conformance behavior is established.

## Source-to-model control relations

| Relation | CRS / source unit | Source locator | Semantic opcode class | File role | M2 transition / event / direction | CRS actor → receiver | Use | State boundary | Controlled source assertions | Scenario rationale |
|---|---|---|---|---|---|---|---|---|---|---|
| SRC-LIST-OFFER-PRECONDITION | CRS-M1-00363<br>SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E005-1CC34400D27E<br>doc/PDF 53/65 | ARINC-615A-3 §6.3.2 / Section 6.3.2 sequence chart A / SEQUENCE-EVENT E005 | APPLICATION-NO-WIRE | LOAD-LIST | T_UPL_LIST_OFFER<br>EV_DL_OFFER_LIST<br>APPLICATION-NO-WIRE | DLA<br>TARGET-HARDWARE | PRECONDITION-ONLY<br>executed=no<br>wire=no | before: UPLOAD-INITIALIZATION-ACCEPTED<br>after: LIST-OFFERED | Application-level list submission is recorded as a named preparation boundary.<br>DLA is not a WRQ, ACK, or DATA network endpoint in this scenario. | Records the named application-layer list-offer prerequisite without dispatching a network event. |
| SRC-LUS-READY | CRS-M1-00364<br>SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E006-298771587D83<br>doc/PDF 53/65 | ARINC-615A-3 §6.3.2 / Section 6.3.2 sequence chart A / SEQUENCE-EVENT E006 | SEMANTIC-LUS-READY-NO-RAW-PACKET | LUS-0001 | T_UPL_WAIT_LUS0001<br>EV_TH_LUS0001<br>TH-TO-DL | DLA<br>TARGET-HARDWARE | VISIBLE-STIMULUS<br>executed=yes<br>wire=yes | before: listOffered=TRUE;listAccepted=FALSE<br>after: targetListReady=TRUE;listAccepted=FALSE | LUS-0001 establishes target readiness for this session.<br>LUS-0001 does not accept the list and does not start LUR. | Provides the current-session readiness stimulus without accepting the list or dispatching LUR. |
| SRC-LUR-WRQ | CRS-M1-00365<br>SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E007-7726A816FFE7<br>doc/PDF 53/65 | ARINC-615A-3 §6.3.2 / Section 6.3.2 sequence chart A / SEQUENCE-EVENT E007 | TFTP-WRQ-SEMANTIC | LUR | T_UPL_LUR_WRQ<br>EV_DL_WRQ_LUR<br>DL-TO-TH | DATA-LOADER<br>TARGET-HARDWARE | VISIBLE-OBJECT-EVENT<br>executed=yes<br>wire=yes | before: listOffered=TRUE;targetListReady=TRUE;listAccepted=FALSE<br>after: listAccepted=TRUE | The source condition LIST-ACCEPTED is represented at the semantic level.<br>The M2 guard reads listAccepted=FALSE before this transition writes TRUE. | Binds the DATA-LOADER readiness/list-acceptance guard to the visible semantic LUR WRQ emission. |
| SRC-LUR-ACK | CRS-M1-00366<br>SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E008-F1D3B51077A3<br>doc/PDF 53/65 | ARINC-615A-3 §6.3.2 / Section 6.3.2 sequence chart A / SEQUENCE-EVENT E008 | TFTP-ACK-SEMANTIC | LUR | T_UPL_LUR_ACK<br>EV_TH_ACK_LUR<br>TH-TO-DL | TARGET-HARDWARE<br>DATA-LOADER | VISIBLE-STIMULUS<br>executed=yes<br>wire=yes | before: S_UPL_LUR_WRQ<br>after: S_UPL_LUR_ACK | The matching ACK is specific to the preceding LUR WRQ. | Binds the TARGET-HARDWARE peer response to the preceding matching semantic LUR WRQ. |
| SRC-LUR-DATA | CRS-M1-00367<br>SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E009-9A7CD75981CB<br>doc/PDF 53/65 | ARINC-615A-3 §6.3.2 / Section 6.3.2 sequence chart A / SEQUENCE-EVENT E009 | TFTP-DATA-SEMANTIC | LUR | T_UPL_LUR_XFER<br>EV_DL_DATA_LUR<br>DL-TO-TH | DATA-LOADER<br>TARGET-HARDWARE | VISIBLE-OBJECT-EVENT<br>executed=yes<br>wire=yes | before: S_UPL_LUR_ACK<br>after: S_UPL_LUR_XFER | Normal execution emits DATA only after the matching ACK state.<br>EARLY-DATA is a named local guard bypass, not an ACK timeout assertion. | Binds normal DATA emission to the matching-ACK state; the named fault bypass remains evaluator-only. |

## Scenario source / interface / acceptance matrix

| State or action | Source relations | Visible evidence | Existing interface use | Acceptance witness | Not covered |
|---|---|---|---|---|---|
| LIST-SUBMISSION-PRECONDITION-RECORDED | SRC-LIST-OFFER-PRECONDITION | Named application-layer list-submission preparation record; no fabricated wire event. | PRECONDITION-NO-DISPATCH | WIT-FINITE-NO-WRQ-TEST | UPLOAD-INITIALIZATION-TRANSPORT<br>REAL-NETWORK-OR-IUT |
| ACT-INSPECT-NO-WRQ-BEFORE-READY | SRC-LUS-READY<br>SRC-LUR-WRQ | Bounded public journal-prefix predicate plus current inspection-completion receipt. | FINITE-TEST-OBSERVATION-AND-HISTORY<br>IF-EXECUTE-RECORD<br>IF-OBS-INTERPRET<br>IF-HIST-UPDATE | WIT-FINITE-NO-WRQ-TEST<br>WIT-PUBLIC-SUMMARY | PROTOCOL-NO-RESPONSE-DEADLINE<br>PHYSICAL-CLOCK-CALIBRATION |
| ACT-PREP-ENTER-READY-WINDOW | SRC-LUS-READY | Current-session EV_TH_LUS0001 journal event and TH ready receipt. | PREP-RECEIPT-AND-CONFIRMATION<br>IF-EXECUTE-RECORD<br>IF-PREP-RECOVER<br>IF-HIST-UPDATE | WIT-PUBLIC-SUMMARY | FULL-UPLOAD-COMPLETION |
| ACT-TEST-ACK-BEFORE-DATA | SRC-LUR-WRQ<br>SRC-LUR-ACK<br>SRC-LUR-DATA | Bounded current-correlation journal order for LUR WRQ, matching ACK and LUR DATA, plus the completed order-check receipt. | FINITE-TEST-OBSERVATION-AND-HISTORY<br>IF-EXECUTE-RECORD<br>IF-OBS-INTERPRET<br>IF-HIST-UPDATE | WIT-PUBLIC-SUMMARY | LUR-PAYLOAD-INTEGRITY<br>FULL-UPLOAD-COMPLETION |
| ACT-RECOVER-RECONFIRM-READY | SRC-LUS-READY | Exact retained current-session post-dispatch public prefix, followed only by the current ready read-back and its completed public receipt. | UNKNOWN-TO-QUALIFIED-RECOVER<br>IF-EXECUTE-RECORD<br>IF-PREP-RECOVER<br>IF-HIST-UPDATE | WIT-SUCCESSOR-AND-RECOVER | PHYSICAL-DEVICE-RECOVERY |

## Finite hypothesis domain

| Hypothesis | Kind | Definition | Algorithm boundary |
|---|---|---|---|
| EARLY-DATA | SINGLE-FAULT | After LUR WRQ, the loader actually bypasses the matching-ACK guard and emits LUR DATA before that ACK. | fault activation is evaluator-only |
| EARLY-WRQ | SINGLE-FAULT | The loader actually bypasses the readiness guard and emits LUR WRQ after the list-submission boundary but before LUS-0001. | fault activation is evaluator-only |
| NORMAL | NORMAL | The loader waits for session-local LUS-0001, emits LUR WRQ, waits for the matching TH ACK, then emits LUR DATA. | fault activation is evaluator-only |

- Algorithm may know: DECLARED-HYPOTHESIS-DOMAIN<br>DECLARED-PREDICTIONS<br>PUBLIC-SCENE-CONFIGURATION
- Algorithm must not receive: ACTIVE-FAULT-ID<br>FAULT-INSTALLATION-READBACK<br>FAULT-ACTIVATION-RECORD<br>PRIVATE-LOADER-STATE<br>EXPECTED-FINAL-H
- Limit: The finite domain is an engineering diagnostic domain only; a surviving member is neither a protocol PASS nor a real-device root-cause finding.

## Controlled actions / 受控动作

### `ACT-INSPECT-NO-WRQ-BEFORE-READY` — TEST
- Eligibility: LIST-SUBMISSION-PRECONDITION-RECORDED and no session-local LUS-0001 journal event
- Public stimulus: Complete one bounded inspection of the current visible journal prefix.
- Observation mode: `FINITE-ENGINEERING-LOG-CHECK`; cost: acquisition=1; computation=1; preparation=0; retry=0
- Successor confirmation: `PUBLIC-OBSERVATION-SUMMARY-CONFIRMATION`
- Unconfirmed-effect disposition: `UNKNOWN-EFFECT-REQUIRES-QUALIFIED-RECOVER`
- History disposition: `SUBMIT-CONFIRMED-SUMMARY-THROUGH-IF-HIST-UPDATE`
- Inspection: completionReceipt=INSPECT-NO-WRQ-BEFORE-READY-COMPLETED; fabricatedProtocolResponse=no; finiteHorizonTicks=1; isProtocolNoResponseVerdict=no; journalPredicate=NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001
- Public summary sources: VISIBLE-JOURNAL-PREFIX<br>INSPECTION-COMPLETION-RECEIPT; prohibited private sources: ACTIVE-FAULT-ID<br>FAULT-ACTIVATION-RECORD<br>PRIVATE-LOADER-STATE
- Public-evidence projection contract: completionReceipt=INSPECT-NO-WRQ-BEFORE-READY-COMPLETED; correlationBinding=CURRENT-OPERATION-CORRELATION; inspectedRange=RECEIPT-BOUNDED-CONTIGUOUS-CLOSED-PREFIX; invalidOrUnconfirmedDisposition=UNKNOWN-EFFECT-REQUIRES-QUALIFIED-RECOVER; ordering=STABLE-SEQUENCE-NUMBER; projectionKind=CURRENT-SESSION-BOUNDED-JOURNAL-RECEIPT; receiptMustBeCompleted=yes; sessionBinding=CURRENT-SESSION
- Possible outcomes:
| Observable | Post-summary | Summary confirmed when | Compatible hypotheses |
|---|---|---|---|
| NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001 | Q-PRE-READY-NO-WRQ | The public inspection receipt and the public no-WRQ journal predicate agree. | NORMAL<br>EARLY-DATA |
| EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001 | Q-EARLY-WRQ-OBSERVED | The public inspection receipt is bound to the current journal event order. | EARLY-WRQ |
- Non-evaluated obligations: PROTOCOL-NO-RESPONSE-DEADLINE<br>PHYSICAL-CLOCK-CALIBRATION

### `ACT-PREP-ENTER-READY-WINDOW` — PREP
- Eligibility: Q-PRE-READY-NO-WRQ is confirmed and the session has affordable preparation resource
- Public stimulus: TH emits the session-local visible EV_TH_LUS0001 ready stimulus.
- Observation mode: `VISIBLE-PREPARATION-EVENT`; cost: acquisition=0; computation=1; preparation=1; retry=0
- Successor confirmation: `PREP-SUMMARY-COMMIT-SEPARATE-FROM-TARGET-STATUS`
- Unconfirmed-effect disposition: `PREP-EFFECT-BRANCH-TABLE-REQUIRED`
- History disposition: `SUBMIT-CONFIRMED-SUMMARY-THROUGH-IF-HIST-UPDATE`
- Inspection: completionReceipt=TH-LUS0001-READY-RECEIPT; fabricatedProtocolResponse=no; finiteHorizonTicks=1; isProtocolNoResponseVerdict=no; journalPredicate=EV_TH_LUS0001-RECORDED-FOR-CURRENT-SESSION
- Public summary sources: VISIBLE-JOURNAL-PREFIX<br>TH-LUS0001-READY-RECEIPT; prohibited private sources: ACTIVE-FAULT-ID<br>FAULT-ACTIVATION-RECORD<br>PRIVATE-LOADER-STATE
- Public-evidence projection contract: completionReceipt=TH-LUS0001-READY-RECEIPT; correlationBinding=CURRENT-OPERATION-CORRELATION; inspectedRange=RECEIPT-BOUNDED-CONTIGUOUS-CLOSED-PREFIX; invalidOrUnconfirmedDisposition=EXECUTED-UNCONFIRMED-SUMMARY-REQUIRES-UNKNOWN; ordering=STABLE-SEQUENCE-NUMBER; projectionKind=CURRENT-SESSION-BOUNDED-JOURNAL-RECEIPT; receiptMustBeCompleted=yes; sessionBinding=CURRENT-SESSION
- Possible outcomes:
| Observable | Post-summary | Summary confirmed when | Compatible hypotheses |
|---|---|---|---|
| EV_TH_LUS0001 | Q-TARGET-READY | The public ready receipt is bound to the current session and is present in the visible journal. | NORMAL<br>EARLY-DATA |
- Prep effect branches:
| Branch | Effect class | Target confirmation | Summary confirmation | History disposition | q disposition | Successor disposition | Charge disposition |
|---|---|---|---|---|---|---|---|
| confirmed | NONE | TARGET-CONFIRMED | SUMMARY-CONFIRMED | COMMIT-CONFIRMED-HISTORY | KNOWN-S9-COMMIT | PRESERVE-RETURNED-SUCCESSOR | CHARGE-ONCE |
| confirmedNotSent | CONFIRMED-NOT-SENT | NO-DISPATCH-CONFIRMED | NO-SUCCESSOR-SUMMARY | PRESERVE-EXISTING-HISTORY | PRESERVE-KNOWN-SUMMARY | NO-OBJECT-ADVANCE | CHARGE-ONCE |
| executedSummaryUnconfirmed | UNKNOWN-EFFECT | ACTUAL-SUCCESSOR-MAY-HAVE-EXECUTED | SUCCESSOR-SUMMARY-UNCONFIRMED | PRESERVE-CONSERVATIVE-HISTORY | UNKNOWN-REQUIRES-QUALIFIED-RECOVER | PRESERVE-RETURNED-SUCCESSOR | CHARGE-ONCE |
| targetNotReachedWithConfirmedSuccessor | NONE | TARGET-NOT-REACHED-BUT-SUCCESSOR-CONFIRMED | SUMMARY-CONFIRMED | COMMIT-CONFIRMED-HISTORY | KNOWN-S9-COMMIT | PRESERVE-RETURNED-SUCCESSOR | CHARGE-ONCE |
- Non-evaluated obligations: FULL-UPLOAD-COMPLETION

### `ACT-TEST-ACK-BEFORE-DATA` — TEST
- Eligibility: Q-TARGET-READY is confirmed and the session has an affordable TEST
- Public stimulus: Drive one bounded loader control step and inspect the visible LUR WRQ, TH ACK and loader DATA event order.
- Observation mode: `FINITE-JOURNAL-ORDER-CHECK`; cost: acquisition=1; computation=1; preparation=0; retry=0
- Successor confirmation: `PUBLIC-OBSERVATION-SUMMARY-CONFIRMATION`
- Unconfirmed-effect disposition: `UNKNOWN-EFFECT-REQUIRES-QUALIFIED-RECOVER`
- History disposition: `SUBMIT-CONFIRMED-SUMMARY-THROUGH-IF-HIST-UPDATE`
- Inspection: completionReceipt=LUR-ORDER-CHECK-COMPLETED; fabricatedProtocolResponse=no; finiteHorizonTicks=3; isProtocolNoResponseVerdict=no; journalPredicate=EV_DL_WRQ_LUR followed either by matching EV_TH_ACK_LUR before EV_DL_DATA_LUR, or by EV_DL_DATA_LUR before any matching ACK
- Public summary sources: VISIBLE-JOURNAL-PREFIX<br>LUR-ORDER-CHECK-COMPLETED; prohibited private sources: ACTIVE-FAULT-ID<br>FAULT-ACTIVATION-RECORD<br>PRIVATE-LOADER-STATE
- Public-evidence projection contract: completionReceipt=LUR-ORDER-CHECK-COMPLETED; correlationBinding=CURRENT-OPERATION-CORRELATION; inspectedRange=RECEIPT-BOUNDED-CONTIGUOUS-CLOSED-PREFIX; invalidOrUnconfirmedDisposition=UNKNOWN-EFFECT-REQUIRES-QUALIFIED-RECOVER; ordering=STABLE-SEQUENCE-NUMBER; projectionKind=CURRENT-SESSION-BOUNDED-JOURNAL-RECEIPT; receiptMustBeCompleted=yes; sessionBinding=CURRENT-SESSION
- Possible outcomes:
| Observable | Post-summary | Summary confirmed when | Compatible hypotheses |
|---|---|---|---|
| WRQ-ACK-DATA-IN-ORDER | Q-LUR-ORDER-ASSESSED | The completed current-correlation prefix contains a matching ACK before its first DATA after WRQ. | NORMAL |
| DATA-BEFORE-MATCHING-ACK | Q-LUR-ORDER-ASSESSED | The completed current-correlation prefix contains the first DATA after WRQ before any matching ACK; a later ACK cannot change that observed order. | EARLY-DATA |
- Non-evaluated obligations: LUR-PAYLOAD-INTEGRITY<br>FULL-UPLOAD-COMPLETION

### `ACT-RECOVER-RECONFIRM-READY` — RECOVER
- Eligibility: SessionContext is UNKNOWN and a declared ready target can be publicly re-confirmed within the finite object boundary
- Public stimulus: Request the controlled TH ready read-back and retain its visible journal receipt.
- Observation mode: `VISIBLE-RECOVER-READBACK`; cost: acquisition=0; computation=1; preparation=1; retry=0
- Successor confirmation: `TARGET-AND-SUMMARY-CONFIRMED-SEPARATELY`
- Unconfirmed-effect disposition: `DO-NOT-MARK-KNOWN`
- History disposition: `SUBMIT-CONFIRMED-SUMMARY-THROUGH-IF-HIST-UPDATE`
- Inspection: completionReceipt=RECOVER-READY-READBACK-COMPLETED; fabricatedProtocolResponse=no; finiteHorizonTicks=1; isProtocolNoResponseVerdict=no; journalPredicate=EXACT-RETAINED-POST-DISPATCH-PREFIX-EXTENDED-BY-CURRENT-SESSION-READY-READBACK
- Public summary sources: VISIBLE-JOURNAL-PREFIX<br>RECOVER-READY-READBACK-COMPLETED; prohibited private sources: ACTIVE-FAULT-ID<br>FAULT-ACTIVATION-RECORD<br>PRIVATE-LOADER-STATE
- Public-evidence projection contract: completionReceipt=RECOVER-READY-READBACK-COMPLETED; correlationBinding=CURRENT-OPERATION-CORRELATION; inspectedRange=RECEIPT-BOUNDED-CONTIGUOUS-CLOSED-PREFIX; invalidOrUnconfirmedDisposition=DO-NOT-MARK-KNOWN; ordering=STABLE-SEQUENCE-NUMBER; projectionKind=CURRENT-SESSION-BOUNDED-JOURNAL-RECEIPT; receiptMustBeCompleted=yes; sessionBinding=CURRENT-SESSION
- Possible outcomes:
| Observable | Post-summary | Summary confirmed when | Compatible hypotheses |
|---|---|---|---|
| RECOVER-READY-READBACK | Q-TARGET-READY | The public recover receipt extends the exact retained post-dispatch public prefix only by the current-session ready read-back; it re-confirms ready without replaying or rewinding an earlier action. | NORMAL<br>EARLY-DATA |
- Non-evaluated obligations: PHYSICAL-DEVICE-RECOVERY

## Clock, observation, reset and recovery

- Clock: `CLK-VIRTUAL-615A-SLICE` / `NONNEGATIVE-INTEGER` — One deterministic engineering scheduler tick; it is not a calibrated physical duration.
- Uncertainty: `U-VIRTUAL-EXACT-ENGINEERING-ONLY` / `ZERO-WIDTH-VIRTUAL-ENGINEERING-MODEL`; same tick: Stable sequenceNumber establishes happens-before for same-tick events.
- Ownership: `CURRENT-SESSION-MATCHING-CORRELATION-ONLY`; finite boundary: A completed inspection horizon bounds the simulated object check only and never establishes a protocol timeout or no-response FAIL.

## Resource admission and accounting boundary

- Admission owner / accounting owner: `IF-SELECT-ADMIT` / `REFERENCE-SESSION`
- Controlled modes: ROUNDS<br>BUDGET; admission boundary: `CHECK-BEFORE-DISPATCH`
- ROUNDS: A positive remaining execution count admits the next bounded action; it is not a monetary budget.
- BUDGET: The declared engineering action cost must be affordable before dispatch.
- Post-dispatch error: `CHARGE-ONCE-PRESERVE-ACTUAL-SUCCESSOR`; not evaluated: REAL-HARDWARE-COST<br>EXPERIMENT-ARM-FAIRNESS

## Fault-installation and activation variants

- Full reset: LOADER-STATE<br>TH-STATE<br>VIRTUAL-CLOCK<br>EVENT-JOURNAL<br>PENDING-DELIVERY<br>CORRELATION-ID-SEQUENCE<br>FAULT-INSTALLATION-STATE; evidence `RESET-READBACK-AND-EMPTY-NEW-ATTEMPT-JOURNAL`; not a protocol abort=yes
- Fault injection: install `CONTROLLER-READBACK-OF-NAMED-GUARD-OR-EMISSION-VARIANT`; activate `INDEPENDENT-JOURNAL-BRANCH-ACTIVATION`; unconfirmed `RETAIN-ATTEMPT-AS-UNCONFIRMED-NOT-NORMAL`
- Installation lifetime: `CURRENT-ENGINEERING-ATTEMPT-UNTIL-FULL-RESET`; revocation action: `FULL-RESET-REVOKES-ALL-NAMED-VARIANTS`; revocation evidence: `RESET-READBACK-FAULT-INSTALLATION-STATE-CLEARED`; revocation failure: `RETAIN-ATTEMPT-AS-INVALID-NOT-NORMAL`
| Hypothesis | Installation target | Controller readback | Activation observable | Algorithm visibility |
|---|---|---|---|---|
| EARLY-DATA | LOADER-MATCHING-ACK-GUARD-BYPASS | READBACK-MATCHING-ACK-GUARD-BYPASS-ACTIVE | EV_DL_DATA_LUR-BEFORE-MATCHING-EV_TH_ACK_LUR | EVALUATOR-ONLY |
| EARLY-WRQ | LOADER-READINESS-GUARD-BYPASS | READBACK-READINESS-GUARD-BYPASS-ACTIVE | EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001 | EVALUATOR-ONLY |

- Recover: requires `UNKNOWN-EFFECT`; distinct target/summary=True; failure `DO-NOT-MARK-KNOWN`

## Scenario entry and continuation contexts

| Case / 案例 | Entry kind | Session binding | Correlation binding | q status | Current summary | Compatible hypotheses | Completed actions | Retained public prefix |
|---|---|---|---|---|---|---|---|---|
| CASE-NORMAL-CONTROL-TIMELINE | FRESH-ATTEMPT | NEW-CURRENT-SESSION | NEW-CURRENT-OPERATION-CORRELATION | KNOWN | SCENE-ENTRY | NORMAL<br>EARLY-WRQ<br>EARLY-DATA | — | LIST-SUBMISSION-PRECONDITION-RECORDED |
| CASE-EARLY-WRQ-TIMELINE | FRESH-ATTEMPT | NEW-CURRENT-SESSION | NEW-CURRENT-OPERATION-CORRELATION | KNOWN | SCENE-ENTRY | NORMAL<br>EARLY-WRQ<br>EARLY-DATA | — | LIST-SUBMISSION-PRECONDITION-RECORDED |
| CASE-EARLY-DATA-TIMELINE | FRESH-ATTEMPT | NEW-CURRENT-SESSION | NEW-CURRENT-OPERATION-CORRELATION | KNOWN | SCENE-ENTRY | NORMAL<br>EARLY-WRQ<br>EARLY-DATA | — | LIST-SUBMISSION-PRECONDITION-RECORDED |
| CASE-UNKNOWN-RECOVER-CONTINUATION | INHERITED-CONTINUATION | CURRENT-SESSION-ONLY | CURRENT-OPERATION-CORRELATION | KNOWN | Q-PRE-READY-NO-WRQ | NORMAL<br>EARLY-DATA | ACT-INSPECT-NO-WRQ-BEFORE-READY | LIST-SUBMISSION-PRECONDITION-RECORDED<br>INSPECT-NO-WRQ-BEFORE-READY-COMPLETED<br>NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001 |
| CASE-RESOURCE-ADMISSION-BLOCK | INHERITED-CONTINUATION | CURRENT-SESSION-ONLY | CURRENT-OPERATION-CORRELATION | KNOWN | Q-TARGET-READY | NORMAL<br>EARLY-DATA | ACT-INSPECT-NO-WRQ-BEFORE-READY<br>ACT-PREP-ENTER-READY-WINDOW | LIST-SUBMISSION-PRECONDITION-RECORDED<br>INSPECT-NO-WRQ-BEFORE-READY-COMPLETED<br>EV_TH_LUS0001<br>TH-LUS0001-READY-RECEIPT |

### UNKNOWN to Recover contract

| Trigger | Action | Round | May-have visible events | Session disposition | Recover entry q | Required public evidence | Target/summary confirmation | Rewind rule | Unconfirmed Recover |
|---|---|---|---|---|---|---|---|---|---|
| POST-DISPATCH-TEST-SUMMARY-CONFIRMATION-FAILURE | ACT-TEST-ACK-BEFORE-DATA | 2 | EV_DL_WRQ_LUR<br>EV_TH_ACK_LUR<br>EV_DL_DATA_LUR | UNKNOWN-PRESERVE-ACTUAL-SUCCESSOR-AND-POST-DISPATCH-JOURNAL | UNKNOWN | CURRENT-SESSION-READY-READBACK<br>RECOVER-READY-READBACK-COMPLETED<br>EXACT-RETAINED-POST-DISPATCH-PUBLIC-PREFIX<br>RECOVER-READY-READBACK-ONLY-EXTENSION | SEPARATE-REQUIRED-NO-REWIND-OR-REPLAY | NO-REWIND-TO-Q-PRE-READY-NO-WRQ | REMAIN-UNKNOWN |

## Timelines / 时线

| Case / 案例 | Purpose | Round | Action | Visible events | Public summary | Candidates | Continue | Resource admission | Resource reason | Resource mode | Available rounds | Required rounds | Cost charged | Successor disposition |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CASE-NORMAL-CONTROL-TIMELINE | Hand-audited normal control-slice timeline; not a complete UPLOAD claim. | 1 | ACT-INSPECT-NO-WRQ-BEFORE-READY | NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001 | Q-PRE-READY-NO-WRQ | NORMAL<br>EARLY-DATA | yes | — | — | — | — | — | — | — |
| CASE-NORMAL-CONTROL-TIMELINE | Hand-audited normal control-slice timeline; not a complete UPLOAD claim. | 2 | ACT-PREP-ENTER-READY-WINDOW | EV_TH_LUS0001 | Q-TARGET-READY | NORMAL<br>EARLY-DATA | yes | — | — | — | — | — | — | — |
| CASE-NORMAL-CONTROL-TIMELINE | Hand-audited normal control-slice timeline; not a complete UPLOAD claim. | 3 | ACT-TEST-ACK-BEFORE-DATA | EV_DL_WRQ_LUR<br>EV_TH_ACK_LUR<br>EV_DL_DATA_LUR | Q-LUR-ORDER-ASSESSED | NORMAL | no | — | — | — | — | — | — | — |
| CASE-EARLY-WRQ-TIMELINE | The object faults by actually emitting LUR WRQ before the session-local ready event. | 1 | ACT-INSPECT-NO-WRQ-BEFORE-READY | EV_DL_WRQ_LUR | Q-EARLY-WRQ-OBSERVED | EARLY-WRQ | no | — | — | — | — | — | — | — |
| CASE-EARLY-DATA-TIMELINE | The object faults by actually emitting LUR DATA after WRQ but before the matching TH ACK. | 1 | ACT-INSPECT-NO-WRQ-BEFORE-READY | NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001 | Q-PRE-READY-NO-WRQ | NORMAL<br>EARLY-DATA | yes | — | — | — | — | — | — | — |
| CASE-EARLY-DATA-TIMELINE | The object faults by actually emitting LUR DATA after WRQ but before the matching TH ACK. | 2 | ACT-PREP-ENTER-READY-WINDOW | EV_TH_LUS0001 | Q-TARGET-READY | NORMAL<br>EARLY-DATA | yes | — | — | — | — | — | — | — |
| CASE-EARLY-DATA-TIMELINE | The object faults by actually emitting LUR DATA after WRQ but before the matching TH ACK. | 3 | ACT-TEST-ACK-BEFORE-DATA | EV_DL_WRQ_LUR<br>EV_DL_DATA_LUR | Q-LUR-ORDER-ASSESSED | EARLY-DATA | no | — | — | — | — | — | — | — |
| CASE-UNKNOWN-RECOVER-CONTINUATION | A tool-side UNKNOWN-EFFECT witness that continues only after a separate Recover target and public summary confirmation. | 1 | ACT-PREP-ENTER-READY-WINDOW | EV_TH_LUS0001 | Q-TARGET-READY | NORMAL<br>EARLY-DATA | yes | — | — | — | — | — | — | — |
| CASE-UNKNOWN-RECOVER-CONTINUATION | A tool-side UNKNOWN-EFFECT witness that continues only after a separate Recover target and public summary confirmation. | 2 | ACT-TEST-ACK-BEFORE-DATA | EXECUTION-EFFECT-UNKNOWN | NONE | NORMAL<br>EARLY-DATA | yes | — | — | — | — | — | — | — |
| CASE-UNKNOWN-RECOVER-CONTINUATION | A tool-side UNKNOWN-EFFECT witness that continues only after a separate Recover target and public summary confirmation. | 3 | ACT-RECOVER-RECONFIRM-READY | RECOVER-READY-READBACK | Q-TARGET-READY | NORMAL<br>EARLY-DATA | yes | — | — | — | — | — | — | — |
| CASE-RESOURCE-ADMISSION-BLOCK | A pre-dispatch insufficient-resource witness: the requested bounded TEST is not sent, no object event is emitted, no action cost is charged, and the pre-dispatch successor is retained. | 1 | ACT-TEST-ACK-BEFORE-DATA | NO-DISPATCH-INSUFFICIENT-RESOURCE | NONE | NORMAL<br>EARLY-DATA | no | NOT-ADMITTED | INSUFFICIENT-RESOURCE-BEFORE-DISPATCH | ROUNDS | 0 | 1 | no | PRE-DISPATCH-SUCCESSOR-UNCHANGED |

## Experiment-interface handoffs

| Interface | Engineering handoff | Public projection | Evaluator projection | Shared-component risk | Not admitted |
|---|---|---|---|---|---|
| IF-EXP-SCENE | Stable scenario family, public configuration and preparation boundary only. | Scenario family, public configuration, preparation boundary and attempt identity only. | No active fault, controller state or private loader state is released through this handoff. | Scenario and source interpretation are shared with the predictor and remain a disclosed common-mode risk. | No formal experiment scenario, real-IUT run or qualified UPLOAD completion is admitted. |
| IF-EXP-INJECT | Installation, controller read-back, activation and unconfirmed-attempt records remain distinct. | Only the resulting visible journal may be consumed by the algorithm path. | Named fault plan, controller read-back, activation record and unconfirmed disposition remain evaluator-only. | The controller, read-back and object branch are authored together; no independent injection oracle is claimed. | An installed or planned variant is not automatically a confirmed fault truth or experimental injection plan. |
| IF-EXP-TRUTH | Evaluator-only surrogate truth with explicit shared-component risk. | No truth hypothesis, installation result or equivalence disposition enters the algorithm projection. | Surrogate truth is retained only for later evaluator/audit comparison with its provenance. | Object, source interpretation, clock and event DTOs can be shared with the predictor or evaluator. | No independent oracle, root-cause label or scientific detection claim is established. |
| IF-EXP-COLLECT | This run's visible journal and resource log only. | Current-run visible journal, resource log and stable attempt references only. | Private controller/read-back records remain separate from the algorithm-visible collection. | Shared event serialization and journal ordering remain implementation risks to disclose. | No cross-arm borrowing, historical capture truth, or complete evidence package is established. |
| IF-EXP-RUN | CL-LOOP engineering run, stop and trace identities only. | CL-LOOP engineering attempt identity, typed session context, stop and trace reference only. | Evaluator truth and fault activation remain outside the typed session context. | The limited loop, predictor and adapter remain a single engineering chain, not independent arms. | No four-arm runner, performance comparison or real-IUT execution is admitted. |
| IF-EXP-FILTER | Retain not-run, unconfirmed and invalid attempts for later accounting. | Named attempt disposition and trace reference are retained without silently deleting failures. | Unconfirmed installation and invalid-record reasons remain available to audit accounting. | Disposition categories share the same engineering controller and are not an independent quality filter. | No valid-sample denominator, scientific exclusion rule or confirmed experiment dataset is established. |
| IF-EXP-EVAL | Preserve linked evidence and permissions; do not calculate experiment metrics. | Linked public evidence and the declared permission boundary only. | Evaluator/audit evidence remains associated by stable reference without becoming algorithm input. | Evidence comparison shares the scenario source and event model with the engineering chain. | No detection, localization, answered denominator, effect size or formal experiment metric is calculated. |

## Feasibility witnesses

| Witness | Entry point | Bounded claim |
|---|---|---|
| WIT-FINITE-NO-WRQ-TEST | ReferenceSession unbound normal TEST path | A nonempty finite inspection observable, public confirmed summary and exact virtual tick can be returned without claiming protocol no-response semantics. |
| WIT-PUBLIC-SUMMARY | Scenario adapter public-journal projection | A typed current-session/current-correlation bounded public journal prefix plus a completed receipt deterministically derives the declared postSummary; invalid receipt identity, range or completion never confirms or shrinks H, regardless of evaluator-only active-fault label. |
| WIT-P3-UNAVAILABLE | RuntimeAuthorityBinding with actual new model/binding path | A control slice that does not evaluate integrity retains P3-UNAVAILABLE and named non-evaluated obligations rather than reusing an old applicability fixture. |
| WIT-SUCCESSOR-AND-RECOVER | Restricted SyntheticEnvironment subclass seam | An inherited H/q/prefix, returned successor, pending journal delivery and post-dispatch TEST summary-confirmation failure preserve the evolved typed object for UNKNOWN; qualified current-session Recover re-confirms a distinct ready target and summary without rewinding to the pre-ready continuation state. |

## Explicit limitations

- No complete UPLOAD, file transfer, CRC, check-value, naming or integrity-capability conclusion.
- No protocol no-response deadline, physical timing calibration, real network, IUT, SIL/HIL or conformance verdict.
- No four-arm runner, pre-experiment, confirmatory result, independent truth or C1/C2 scientific claim.

# 中文版

# 615A UPLOAD LUR 起始工程场景原型

> 本视图由 `configs/engineering/cltav_615a_scenarios.json` 生成，禁止直接修改。它是有限工程规格，不是协议符合性判定、实验结果或能力主张。

- ARINC 615A UPLOAD 的 LUR 起始控制切片工程场景包；仅用于受控合成工程对象和规格走查。
- 控制：`CR-2026-022` / `DD-046`；已接受权威提交：`c577f34e98b91083a69f0a731a990c01aa7fa08b`
- 不可变 G0 控制记录：`docs/control/changes/CR-2026-022.md` @ `331abdf26b550111df56226a88ca5a6a989c1d76`；Git blob `e031045720207218bbc24c810e7f4d33d5d76791`；SHA-256 `d4db86a0eb6e2d9d81504865126d91728a3463ecf9090bf169b8180e26448719`
- 分类：`SYNTHETIC-ENGINEERING-VALIDATION`；阶段：`B-OBJECT-LIFECYCLE-CANDIDATE-PENDING-INDEPENDENT-REVIEW`

## 已接受权威快照

| 路径 | 角色 | 提交 | Git blob | SHA-256 |
|---|---|---|---|---|
| configs/engineering/cltav_development_contracts.json | DEVELOPMENT-CONTRACT | c577f34e98b91083a69f0a731a990c01aa7fa08b | aad74f8c5ac3ab47a5c7b4b85e51e1174c6b664e | 3331fadf2786133f161eded9d1fb42066ca58d7dd510ce6e775da1cd89a5aae1 |
| configs/engineering/cltav_runtime_applicability.json | RUNTIME-APPLICABILITY | c577f34e98b91083a69f0a731a990c01aa7fa08b | b18b0f66741c313e8eb50f964606e5332d60236b | 5fe77badebe95da8c88b8480647e80b96cd5bd9ee5ac5609f0aed80cca4c70f8 |
| configs/models/arinc_615a3_m2_model.json | ACCEPTED-M2 | c577f34e98b91083a69f0a731a990c01aa7fa08b | 9e311e60824194c5f15174543a28cdc070321a0a | 32b92b1eb4a54c603386363a3cdf3a0fc4d1c44af7cead2115a4226282fa1684 |
| configs/requirements/arinc_615a3_m1_crs.json | ACCEPTED-CRS | c577f34e98b91083a69f0a731a990c01aa7fa08b | 44b471aa25ceb6af0d0a6fdd610e25cd02f92b7b | 56e214f089e6563e53e3991e7a8e7892f163840bb2c1d7d39f4a9ce92fc16758 |
| configs/research/cltav_experiment_design.json | EXPERIMENT-DESIGN | c577f34e98b91083a69f0a731a990c01aa7fa08b | 426240668cb8112347fd37c8d2ee56b36078bddb | c0161e2772825ce0a471dbf79e0ac27bf7ade20579655bfccacc8c6d2e451178 |
| configs/research/cltav_interface_registry.json | INTERFACE-REGISTRY | c577f34e98b91083a69f0a731a990c01aa7fa08b | a7202e42f07e69b5d9c1f95137e093c16e1c1ab8 | a65679b902cf51d31aa613c133919c3cd2c66dbc6c65eb3cc58d9bf3530d329d |
| pyproject.toml | INSTALLATION-CONTRACT | c577f34e98b91083a69f0a731a990c01aa7fa08b | 577ea125717d0ece52c17a6bfaee3c5b3b9c55f8 | d8aee77b0f7850255b9a4991004d819f0259cab5e7dde6dab20efb344c77e0b3 |
| src/cltav_runtime/session.py | RUNTIME-SEAM | c577f34e98b91083a69f0a731a990c01aa7fa08b | 7c73ae9a87d1098b1a527abf20705a7affe7abae | d13ce2aadfe35262dc2e628ddbf262de2c518f84afd17a06536defd0aba36c57 |
| src/cltav_runtime/synthetic.py | RUNTIME-SEAM | c577f34e98b91083a69f0a731a990c01aa7fa08b | 1eebb2854ae702302aee172a00ce5ff3e090263e | 9410082b4c8ecf2f35457046829477d51392423477aa687a433ec020da644271 |

## 范围与边界

- 该切片仅覆盖清单提交后的 LUS-0001 就绪、LUR WRQ、匹配 ACK 与 LUR DATA 的有限控制边界；不构成完整 UPLOAD 或设备符合性结论。
- 操作／角色：`UPLOAD` / DATA-LOADER<br>TARGET-HARDWARE
- 起点／终点：`LIST-SUBMISSION-PRECONDITION-RECORDED` / `LUR-CONTROL-SLICE-OBSERVATION-END`
- 已准备但未执行：EV_DL_OFFER_LIST<br>UPLOAD-INITIALIZATION<br>FULL-LUR-BYTES<br>CRC-CHECK-VALUE-NAMING
- 未评估：FULL-UPLOAD-COMPLETION<br>LUR-PAYLOAD-INTEGRITY<br>CRC-CHECK-VALUE-NAMING-CAPABILITY<br>PROTOCOL-NO-RESPONSE-DEADLINE<br>REAL-NETWORK-OR-IUT<br>FOUR-ARM-EXPERIMENT
- 实验关系：`SC-NORMAL-UPLOAD` / `PREPARES-INTERFACE` — 该 LUR 起始切片只准备工程接口，不证明合格的 UPLOAD 完成，也不证明已准入的实验执行。
## 对象与对端合同

- 阶段：`B-OBJECT-LIFECYCLE-CANDIDATE-PENDING-INDEPENDENT-REVIEW`；对象：`IN-PROCESS-CONTROLLED-DATA-LOADER-SURROGATE`；对端：`IN-PROCESS-CONTROLLED-TARGET-HARDWARE-DRIVER`。

### 状态与不变量

| 状态 | M2／来源锚点 | 初值 | 所有者 | 中文不变量 |
|---|---|---|---|---|
| LIST-ACCEPTED | M2-VARIABLE:listAccepted | FALSE | DATA-LOADER | 正常 WRQ 守卫必须读取 FALSE，且只有受控 WRQ 迁移才可将其写为 TRUE。 |
| LIST-OFFERED | M2-VARIABLE:listOffered | FALSE | DATA-LOADER | 该状态只由具名的应用层清单提交准备边界建立，不得伪造为 wire 事件。 |
| MATCHING-LUR-ACK | M2-STATE:S_UPL_LUR_ACK | FALSE | DATA-LOADER | 只有与前序 LUR WRQ 相关联的当前会话 ACK 才能建立该状态并允许正常 DATA 发射。 |
| TARGET-LIST-READY | M2-VARIABLE:targetListReady | FALSE | DATA-LOADER | 只有当前会话的 EV_TH_LUS0001 刺激可以建立就绪；就绪本身不表示清单已接受。 |
| TH-MATCHING-LUR-WRQ-RECEIVED | M2-STATE:S_UPL_LUR_WRQ | FALSE | TARGET-HARDWARE | 只有当前会话的 LUR WRQ 才能建立允许目标硬件发射匹配 ACK 的对端状态。 |

### 守卫与故障旁路

| 守卫 | 来源关系 | 所需状态 | 正常可见输出 | 故障旁路 | 中文说明 |
|---|---|---|---|---|---|
| GUARD-DATA-AFTER-MATCHING-ACK | SRC-LUR-DATA | MATCHING-LUR-ACK=TRUE | OUT-DL-DATA-LUR | EARLY-DATA | 正常 DATA 必须在匹配 ACK 后发射；EARLY-DATA 仅在对象分支中绕过匹配 ACK 守卫。 |
| GUARD-TH-ACK-AFTER-MATCHING-WRQ | SRC-LUR-ACK | TH-MATCHING-LUR-WRQ-RECEIVED=TRUE | OUT-TH-ACK-LUR | NO-FAULT-BYPASS | 目标硬件仅在当前会话收到匹配 LUR WRQ 后发射 ACK；本轮没有对端 ACK 故障旁路。 |
| GUARD-WRQ-AFTER-READY | SRC-LUR-WRQ | LIST-OFFERED=TRUE<br>TARGET-LIST-READY=TRUE<br>LIST-ACCEPTED=FALSE | OUT-DL-WRQ-LUR | EARLY-WRQ | 正常 WRQ 必须在清单已提供、目标已就绪且尚未接受清单时发射；EARLY-WRQ 仅在对象分支中绕过该就绪守卫。 |

### 公开刺激与可见输出

| 类型 | 标识 | 来源关系 | 事件 | 可见性 | 中文说明 |
|---|---|---|---|---|---|
| 公开刺激 | STIM-LIST-SUBMISSION-PRECONDITION | SRC-LIST-OFFER-PRECONDITION | EV_DL_OFFER_LIST | APPLICATION | 清单提交是受控的应用层准备记录，不作为网络 opcode 或对象自行发射的事件。 |
| 公开刺激 | STIM-TH-ACK-LUR | SRC-LUR-ACK | EV_TH_ACK_LUR | NETWORK-VISIBLE | 目标硬件仅对当前会话中前序 LUR WRQ 的匹配请求给出 ACK。 |
| 公开刺激 | STIM-TH-LUS0001 | SRC-LUS-READY | EV_TH_LUS0001 | NETWORK-VISIBLE | 目标硬件向数据加载器给出当前会话的 LUS-0001 就绪刺激。 |
| 类型 | 标识 | 来源关系 | 事件 | 可见性 | 中文说明 |
|---|---|---|---|---|---|
| 可见输出 | OUT-DL-DATA-LUR | SRC-LUR-DATA | EV_DL_DATA_LUR | NETWORK-VISIBLE | 数据加载器发出的 LUR DATA 是受限控制片段中的可见对象事件。 |
| 可见输出 | OUT-DL-WRQ-LUR | SRC-LUR-WRQ | EV_DL_WRQ_LUR | NETWORK-VISIBLE | 数据加载器发出的 LUR WRQ 是受限控制片段中的可见对象事件。 |
| 可见输出 | OUT-TH-ACK-LUR | SRC-LUR-ACK | EV_TH_ACK_LUR | NETWORK-VISIBLE | 目标硬件发出的匹配 LUR ACK 是受限控制片段中的可见对端事件。 |

### 文件角色、语义 opcode 与私有投影

- WRQ、ACK、DATA 与 LUR 仅作为来源绑定的语义事件和文件角色处理；本阶段不实现 UDP/IP 报文、LUR 字节载荷或校验和。
- 文件角色：`LUR`；语义 opcode：WRQ<br>ACK<br>DATA；载荷表示：`OPAQUE-NO-LUR-BYTE-PAYLOAD-OR-CHECKSUM-EVALUATED`；不是 wire 报文实现：是。
- 活动故障、安装回读、激活记录、对象私有状态和预期最终候选只限评估方；算法只能经既有有类型动作／观测接口使用公开投影。
- 仅评估方：ACTIVE-FAULT-ID<br>FAULT-INSTALLATION-READBACK<br>FAULT-ACTIVATION-RECORD<br>PRIVATE-LOADER-STATE<br>EXPECTED-FINAL-H；算法禁止：ACTIVE-FAULT-ID<br>FAULT-INSTALLATION-READBACK<br>FAULT-ACTIVATION-RECORD<br>PRIVATE-LOADER-STATE<br>EXPECTED-FINAL-H；允许公开投影：DECLARED-HYPOTHESIS-DOMAIN<br>DECLARED-PREDICTIONS<br>PUBLIC-SCENE-CONFIGURATION<br>TYPED-ACTION-AND-OBSERVATION-INTERFACE。

### 故障撤销与实现身份计划

- 故障安装只在当前工程尝试中有效；全量 reset 必须撤销全部具名变体，并产生故障安装状态已清除的回读证据。
- 安装生命周期：`CURRENT-ENGINEERING-ATTEMPT-UNTIL-FULL-RESET`；撤销动作：`FULL-RESET-REVOKES-ALL-NAMED-VARIANTS`；撤销证据：`RESET-READBACK-FAULT-INSTALLATION-STATE-CLEARED`。
- B 阶段提供具有实际加载源码内容身份的 Loader／TH 替身，只用于直接合成工程验证；不建立真实 IUT 身份、CL-TAV 适配器、实验执行或协议符合性行为。后续交付仍须关联评审源码提交、分发制品身份和适配器源码身份。
- 身份状态：`SOURCE-OBJECT-CANDIDATE-PENDING-INDEPENDENT-REVIEW`；源码根：`src/cltav_615a`；直接入口：`cltav_615a.LurStartController`；后续实现必须绑定：OBJECT-SOURCE-COMMIT<br>OBJECT-DISTRIBUTION-IDENTITY<br>ADAPTER-SOURCE-IDENTITY。
- B 源码身份方案：`CLTAV-615A-LOADED-SOURCE-SHA256-LF-V1`；加载核验：`MODULE-CODE-EQUALITY-FROZEN-SOURCE-AND-CONSTRUCTOR-DRIFT-CHECK`；审计关联：`FROZEN-MANIFEST-IN-ATTEMPT-AUDIT-SHARED-CODE-IDENTITY`。
- B 绑定源码：src/cltav_615a/__init__.py<br>src/cltav_615a/controller.py<br>src/cltav_615a/objects.py<br>src/cltav_615a/source_identity.py<br>src/cltav_615a/types.py。
- B 将五个受跟踪普通源码文件与实际执行的模块代码核对，冻结 LF 规范化内容散列，构造前拒绝源码缺失或漂移。复位、安装、激活和尝试审计共同引用该清单身份。调用者运行标签仅限评估方，不能替代源码身份；公开事件不含标签或源码身份。这是受控正常加载的来源核验，不是恶意代码沙箱。C 适配器与 D 分发身份仍未建立；评审提交定位补充而不替代 B 内容绑定。
- 尚未建立：该受控源码 Loader／TH 替身仅用于直接合成工程验证；尚未建立真实 IUT 身份、CL-TAV 适配器、实验执行或协议符合性行为。

## 来源到模型的控制关系

| 关系 | CRS／来源单元 | 来源定位 | 语义 opcode 类 | 文件角色 | M2 迁移／事件／方向 | CRS 参与方 | 场景用途 | 状态边界 | 场景理由 | 中文控制说明 |
|---|---|---|---|---|---|---|---|---|---|---|
| SRC-LIST-OFFER-PRECONDITION | CRS-M1-00363<br>SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E005-1CC34400D27E<br>文档/PDF 53/65 | ARINC-615A-3 §6.3.2 / Section 6.3.2 sequence chart A / SEQUENCE-EVENT E005 | APPLICATION-NO-WIRE | LOAD-LIST | T_UPL_LIST_OFFER<br>EV_DL_OFFER_LIST<br>APPLICATION-NO-WIRE | DLA<br>TARGET-HARDWARE | PRECONDITION-ONLY<br>执行=否<br>报文=否 | 前：UPLOAD-INITIALIZATION-ACCEPTED<br>后：LIST-OFFERED | 记录具名的应用层清单提交前置，不调度网络事件。 | 应用层清单提交只记录为前置准备边界；DLA 不是本场景 WRQ、ACK 或 DATA 的网络端点。 |
| SRC-LUS-READY | CRS-M1-00364<br>SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E006-298771587D83<br>文档/PDF 53/65 | ARINC-615A-3 §6.3.2 / Section 6.3.2 sequence chart A / SEQUENCE-EVENT E006 | SEMANTIC-LUS-READY-NO-RAW-PACKET | LUS-0001 | T_UPL_WAIT_LUS0001<br>EV_TH_LUS0001<br>TH-TO-DL | DLA<br>TARGET-HARDWARE | VISIBLE-STIMULUS<br>执行=是<br>报文=是 | 前：listOffered=TRUE;listAccepted=FALSE<br>后：targetListReady=TRUE;listAccepted=FALSE | 提供当前会话的就绪刺激，但不接受清单，也不调度 LUR。 | LUS-0001 只建立当前会话的目标就绪状态；不得据此把清单写为已接受，或直接开始 LUR。 |
| SRC-LUR-WRQ | CRS-M1-00365<br>SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E007-7726A816FFE7<br>文档/PDF 53/65 | ARINC-615A-3 §6.3.2 / Section 6.3.2 sequence chart A / SEQUENCE-EVENT E007 | TFTP-WRQ-SEMANTIC | LUR | T_UPL_LUR_WRQ<br>EV_DL_WRQ_LUR<br>DL-TO-TH | DATA-LOADER<br>TARGET-HARDWARE | VISIBLE-OBJECT-EVENT<br>执行=是<br>报文=是 | 前：listOffered=TRUE;targetListReady=TRUE;listAccepted=FALSE<br>后：listAccepted=TRUE | 把 DATA-LOADER 的就绪／清单接受守卫绑定到可见的语义 LUR WRQ 发射。 | DATA-LOADER 仅在列表已提供、目标已就绪且列表尚未接受时发送 LUR WRQ；迁移后才写入已接受。 |
| SRC-LUR-ACK | CRS-M1-00366<br>SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E008-F1D3B51077A3<br>文档/PDF 53/65 | ARINC-615A-3 §6.3.2 / Section 6.3.2 sequence chart A / SEQUENCE-EVENT E008 | TFTP-ACK-SEMANTIC | LUR | T_UPL_LUR_ACK<br>EV_TH_ACK_LUR<br>TH-TO-DL | TARGET-HARDWARE<br>DATA-LOADER | VISIBLE-STIMULUS<br>执行=是<br>报文=是 | 前：S_UPL_LUR_WRQ<br>后：S_UPL_LUR_ACK | 把 TARGET-HARDWARE 对端响应绑定到前序匹配的语义 LUR WRQ。 | TARGET-HARDWARE 只从 LUR WRQ 状态发送匹配的 LUR ACK，不能因同一操作名而无条件接受 ACK。 |
| SRC-LUR-DATA | CRS-M1-00367<br>SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E009-9A7CD75981CB<br>文档/PDF 53/65 | ARINC-615A-3 §6.3.2 / Section 6.3.2 sequence chart A / SEQUENCE-EVENT E009 | TFTP-DATA-SEMANTIC | LUR | T_UPL_LUR_XFER<br>EV_DL_DATA_LUR<br>DL-TO-TH | DATA-LOADER<br>TARGET-HARDWARE | VISIBLE-OBJECT-EVENT<br>执行=是<br>报文=是 | 前：S_UPL_LUR_ACK<br>后：S_UPL_LUR_XFER | 把正常 DATA 发射绑定到匹配 ACK 状态；具名故障旁路仍仅评估方可见。 | DATA-LOADER 只在匹配 ACK 后发送 LUR DATA；EARLY-DATA 是受限的、评估方可见的单故障分支。 |

## 场景来源／接口／验收矩阵

| 状态或动作 | 来源关系 | 可见证据 | 既有接口用途 | 验收见证 | 未覆盖边界 | 中文说明 |
|---|---|---|---|---|---|---|
| LIST-SUBMISSION-PRECONDITION-RECORDED | SRC-LIST-OFFER-PRECONDITION | Named application-layer list-submission preparation record; no fabricated wire event. | PRECONDITION-NO-DISPATCH | WIT-FINITE-NO-WRQ-TEST | UPLOAD-INITIALIZATION-TRANSPORT<br>REAL-NETWORK-OR-IUT | 列表提交仅是命名的应用层前置记录，不调度网络动作，也不伪造 wire 事件。 |
| ACT-INSPECT-NO-WRQ-BEFORE-READY | SRC-LUS-READY<br>SRC-LUR-WRQ | Bounded public journal-prefix predicate plus current inspection-completion receipt. | FINITE-TEST-OBSERVATION-AND-HISTORY<br>IF-EXECUTE-RECORD<br>IF-OBS-INTERPRET<br>IF-HIST-UPDATE | WIT-FINITE-NO-WRQ-TEST<br>WIT-PUBLIC-SUMMARY | PROTOCOL-NO-RESPONSE-DEADLINE<br>PHYSICAL-CLOCK-CALIBRATION | 有限无 WRQ 检查由执行、解释和历史接口消费公开日志／回执；它不评价协议无响应期限。 |
| ACT-PREP-ENTER-READY-WINDOW | SRC-LUS-READY | Current-session EV_TH_LUS0001 journal event and TH ready receipt. | PREP-RECEIPT-AND-CONFIRMATION<br>IF-EXECUTE-RECORD<br>IF-PREP-RECOVER<br>IF-HIST-UPDATE | WIT-PUBLIC-SUMMARY | FULL-UPLOAD-COMPLETION | 准备动作把当前会话 LUS-0001 公开刺激交给执行、Prep/Recover 和历史接口；仅在摘要确认后提交下一轮历史，不宣称完整上传。 |
| ACT-TEST-ACK-BEFORE-DATA | SRC-LUR-WRQ<br>SRC-LUR-ACK<br>SRC-LUR-DATA | Bounded current-correlation journal order for LUR WRQ, matching ACK and LUR DATA, plus the completed order-check receipt. | FINITE-TEST-OBSERVATION-AND-HISTORY<br>IF-EXECUTE-RECORD<br>IF-OBS-INTERPRET<br>IF-HIST-UPDATE | WIT-PUBLIC-SUMMARY | LUR-PAYLOAD-INTEGRITY<br>FULL-UPLOAD-COMPLETION | 顺序 TEST 把 WRQ、ACK、DATA 的可见顺序交给执行、解释和历史接口；不评价 LUR 负载完整性。 |
| ACT-RECOVER-RECONFIRM-READY | SRC-LUS-READY | Exact retained current-session post-dispatch public prefix, followed only by the current ready read-back and its completed public receipt. | UNKNOWN-TO-QUALIFIED-RECOVER<br>IF-EXECUTE-RECORD<br>IF-PREP-RECOVER<br>IF-HIST-UPDATE | WIT-SUCCESSOR-AND-RECOVER | PHYSICAL-DEVICE-RECOVERY | UNKNOWN 后的 Recover 通过执行、Prep/Recover 和历史接口重新确认独立目标与摘要；失败不得产生 KNOWN。 |

## 有限假设域

| 假设 | 类别 | 中文说明 | 算法边界 |
|---|---|---|---|
| EARLY-DATA | SINGLE-FAULT | 单故障分支：实际绕过匹配 ACK 守卫，在 ACK 前发出 LUR DATA。 | 故障激活仅评估方可见 |
| EARLY-WRQ | SINGLE-FAULT | 单故障分支：实际绕过就绪守卫，在 LUS-0001 前发出 LUR WRQ。 | 故障激活仅评估方可见 |
| NORMAL | NORMAL | 正常分支：等待会话本地 LUS-0001，再依次出现 LUR WRQ、匹配 ACK 与 LUR DATA。 | 故障激活仅评估方可见 |

- 算法可知：DECLARED-HYPOTHESIS-DOMAIN<br>DECLARED-PREDICTIONS<br>PUBLIC-SCENE-CONFIGURATION
- 算法不得接收：ACTIVE-FAULT-ID<br>FAULT-INSTALLATION-READBACK<br>FAULT-ACTIVATION-RECORD<br>PRIVATE-LOADER-STATE<br>EXPECTED-FINAL-H
- 覆盖边界：有限假设域仅用于工程诊断；剩余成员既不表示协议 PASS，也不表示已定位真实设备根因。

## 受控动作

### `ACT-INSPECT-NO-WRQ-BEFORE-READY` — 有限工程日志检查：区分就绪前无 WRQ 与提前 WRQ；它不是协议无响应判定，也不伪造协议响应。
- 类别：`TEST`；资格：已记录清单提交前提，且当前会话日志中尚无 LUS-0001。
- 公开刺激：完成一次对当前可见日志前缀的有界检查。
- 观测模式：有限工程日志检查。；成本：acquisition=1; computation=1; preparation=0; retry=0
- 后继确认：通过公开观测与公开摘要确认实际后继。
- 未确认效果：未确认效果进入 UNKNOWN，且只能经合格 Recover 继续。
- 历史提交：仅将已确认摘要经 IF-HIST-UPDATE 提交给后续历史。
- 检查：completionReceipt=INSPECT-NO-WRQ-BEFORE-READY-COMPLETED; fabricatedProtocolResponse=否; finiteHorizonTicks=1; isProtocolNoResponseVerdict=否; journalPredicate=NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001
- 摘要来源（公开）：VISIBLE-JOURNAL-PREFIX<br>INSPECTION-COMPLETION-RECEIPT；禁止私有来源：ACTIVE-FAULT-ID<br>FAULT-ACTIVATION-RECORD<br>PRIVATE-LOADER-STATE
- 公开证据投影合同：completionReceipt=INSPECT-NO-WRQ-BEFORE-READY-COMPLETED; correlationBinding=CURRENT-OPERATION-CORRELATION; inspectedRange=RECEIPT-BOUNDED-CONTIGUOUS-CLOSED-PREFIX; invalidOrUnconfirmedDisposition=UNKNOWN-EFFECT-REQUIRES-QUALIFIED-RECOVER; ordering=STABLE-SEQUENCE-NUMBER; projectionKind=CURRENT-SESSION-BOUNDED-JOURNAL-RECEIPT; receiptMustBeCompleted=是; sessionBinding=CURRENT-SESSION
- 可能结果：
| 可见量 | 后继摘要 | 摘要确认条件 | 相容假设 |
|---|---|---|---|
| NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001 | Q-PRE-READY-NO-WRQ | 公开检查完成回执与公开日志中的无 WRQ 判据一致时，才确认摘要。 | NORMAL<br>EARLY-DATA |
| EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001 | Q-EARLY-WRQ-OBSERVED | 公开检查完成回执与当前日志事件顺序绑定时，才确认摘要。 | EARLY-WRQ |
- 未评估义务：PROTOCOL-NO-RESPONSE-DEADLINE<br>PHYSICAL-CLOCK-CALIBRATION

### `ACT-PREP-ENTER-READY-WINDOW` — 准备动作：由目标硬件发出当前会话可见的 LUS-0001，并以公开回执确认就绪摘要。
- 类别：`PREP`；资格：Q-PRE-READY-NO-WRQ 已确认，且会话拥有可负担的准备资源。
- 公开刺激：目标硬件发出当前会话可见的 EV_TH_LUS0001 就绪刺激。
- 观测模式：可见准备事件。；成本：acquisition=0; computation=1; preparation=1; retry=0
- 后继确认：Prep 的摘要提交与目标状态必须分开判定；只有摘要确认控制提交。
- 未确认效果：必须按四分支效果表处置，不能把已执行但摘要未确认误作确认未发送。
- 历史提交：仅将已确认摘要经 IF-HIST-UPDATE 提交给后续历史。
- 检查：completionReceipt=TH-LUS0001-READY-RECEIPT; fabricatedProtocolResponse=否; finiteHorizonTicks=1; isProtocolNoResponseVerdict=否; journalPredicate=EV_TH_LUS0001-RECORDED-FOR-CURRENT-SESSION
- 摘要来源（公开）：VISIBLE-JOURNAL-PREFIX<br>TH-LUS0001-READY-RECEIPT；禁止私有来源：ACTIVE-FAULT-ID<br>FAULT-ACTIVATION-RECORD<br>PRIVATE-LOADER-STATE
- 公开证据投影合同：completionReceipt=TH-LUS0001-READY-RECEIPT; correlationBinding=CURRENT-OPERATION-CORRELATION; inspectedRange=RECEIPT-BOUNDED-CONTIGUOUS-CLOSED-PREFIX; invalidOrUnconfirmedDisposition=EXECUTED-UNCONFIRMED-SUMMARY-REQUIRES-UNKNOWN; ordering=STABLE-SEQUENCE-NUMBER; projectionKind=CURRENT-SESSION-BOUNDED-JOURNAL-RECEIPT; receiptMustBeCompleted=是; sessionBinding=CURRENT-SESSION
- 可能结果：
| 可见量 | 后继摘要 | 摘要确认条件 | 相容假设 |
|---|---|---|---|
| EV_TH_LUS0001 | Q-TARGET-READY | 公开就绪回执绑定当前会话且位于可见日志中时，才确认摘要。 | NORMAL<br>EARLY-DATA |
- Prep 效果分支：
| 分支 | 效果类 | 目标确认 | 摘要确认 | 历史处置 | q 处置 | 后继处置 | 收费 | 中文说明 |
|---|---|---|---|---|---|---|---|---|
| confirmed | NONE | TARGET-CONFIRMED | SUMMARY-CONFIRMED | COMMIT-CONFIRMED-HISTORY | KNOWN-S9-COMMIT | PRESERVE-RETURNED-SUCCESSOR | CHARGE-ONCE | 目标与摘要均确认时，提交已确认历史与 KNOWN 摘要，保留返回后继并只计费一次。 |
| confirmedNotSent | CONFIRMED-NOT-SENT | NO-DISPATCH-CONFIRMED | NO-SUCCESSOR-SUMMARY | PRESERVE-EXISTING-HISTORY | PRESERVE-KNOWN-SUMMARY | NO-OBJECT-ADVANCE | CHARGE-ONCE | 明确确认未发送时，保持既有 H 和 KNOWN 摘要，不推进对象，并只计费一次。 |
| executedSummaryUnconfirmed | UNKNOWN-EFFECT | ACTUAL-SUCCESSOR-MAY-HAVE-EXECUTED | SUCCESSOR-SUMMARY-UNCONFIRMED | PRESERVE-CONSERVATIVE-HISTORY | UNKNOWN-REQUIRES-QUALIFIED-RECOVER | PRESERVE-RETURNED-SUCCESSOR | CHARGE-ONCE | 已执行但后继摘要无法公开确认时，保留实际返回后继、把历史保守化并进入 UNKNOWN；只计费一次。 |
| targetNotReachedWithConfirmedSuccessor | NONE | TARGET-NOT-REACHED-BUT-SUCCESSOR-CONFIRMED | SUMMARY-CONFIRMED | COMMIT-CONFIRMED-HISTORY | KNOWN-S9-COMMIT | PRESERVE-RETURNED-SUCCESSOR | CHARGE-ONCE | 目标未达但实际后继摘要已确认时，仍按已确认摘要提交 KNOWN，不能误归 UNKNOWN。 |
- 未评估义务：FULL-UPLOAD-COMPLETION

### `ACT-TEST-ACK-BEFORE-DATA` — 有限顺序检查：观察 LUR WRQ、匹配 ACK 与 DATA 的公开顺序，区分正常与提前 DATA。
- 类别：`TEST`；资格：Q-TARGET-READY 已确认，且会话拥有可负担的 TEST 资源。
- 公开刺激：驱动一个有界加载器控制步，并检查当前关联的完整前缀中 LUR WRQ、TH ACK 和加载器 DATA 的顺序。
- 观测模式：有限日志顺序检查。；成本：acquisition=1; computation=1; preparation=0; retry=0
- 后继确认：通过公开观测与公开摘要确认实际后继。
- 未确认效果：未确认效果进入 UNKNOWN，且只能经合格 Recover 继续。
- 历史提交：仅将已确认摘要经 IF-HIST-UPDATE 提交给后续历史。
- 检查：completionReceipt=LUR-ORDER-CHECK-COMPLETED; fabricatedProtocolResponse=否; finiteHorizonTicks=3; isProtocolNoResponseVerdict=否; journalPredicate=EV_DL_WRQ_LUR followed either by matching EV_TH_ACK_LUR before EV_DL_DATA_LUR, or by EV_DL_DATA_LUR before any matching ACK
- 摘要来源（公开）：VISIBLE-JOURNAL-PREFIX<br>LUR-ORDER-CHECK-COMPLETED；禁止私有来源：ACTIVE-FAULT-ID<br>FAULT-ACTIVATION-RECORD<br>PRIVATE-LOADER-STATE
- 公开证据投影合同：completionReceipt=LUR-ORDER-CHECK-COMPLETED; correlationBinding=CURRENT-OPERATION-CORRELATION; inspectedRange=RECEIPT-BOUNDED-CONTIGUOUS-CLOSED-PREFIX; invalidOrUnconfirmedDisposition=UNKNOWN-EFFECT-REQUIRES-QUALIFIED-RECOVER; ordering=STABLE-SEQUENCE-NUMBER; projectionKind=CURRENT-SESSION-BOUNDED-JOURNAL-RECEIPT; receiptMustBeCompleted=是; sessionBinding=CURRENT-SESSION
- 可能结果：
| 可见量 | 后继摘要 | 摘要确认条件 | 相容假设 |
|---|---|---|---|
| WRQ-ACK-DATA-IN-ORDER | Q-LUR-ORDER-ASSESSED | 已完成的当前操作关联前缀在 WRQ 后的首个 DATA 之前包含匹配 ACK 时，才确认摘要。 | NORMAL |
| DATA-BEFORE-MATCHING-ACK | Q-LUR-ORDER-ASSESSED | 已完成的当前操作关联前缀中，WRQ 后的首个 DATA 先于任何匹配 ACK；后续 ACK 不得改变这一已观测顺序时，才确认摘要。 | EARLY-DATA |
- 未评估义务：LUR-PAYLOAD-INTEGRITY<br>FULL-UPLOAD-COMPLETION

### `ACT-RECOVER-RECONFIRM-READY` — 恢复动作：仅在 UNKNOWN 效果后，用独立的公开就绪回读重新确认目标与摘要；失败不得标记为已知。
- 类别：`RECOVER`；资格：SessionContext 为 UNKNOWN，且可在有限对象边界内公开重新确认具名就绪目标。
- 公开刺激：请求受控的目标硬件就绪回读，并以该回读仅扩展保留的调度后公开前缀。
- 观测模式：可见 Recover 回读。；成本：acquisition=0; computation=1; preparation=1; retry=0
- 后继确认：Recover 目标确认与摘要确认必须分别成立。
- 未确认效果：确认失败不得标记为 KNOWN。
- 历史提交：仅将已确认摘要经 IF-HIST-UPDATE 提交给后续历史。
- 检查：completionReceipt=RECOVER-READY-READBACK-COMPLETED; fabricatedProtocolResponse=否; finiteHorizonTicks=1; isProtocolNoResponseVerdict=否; journalPredicate=EXACT-RETAINED-POST-DISPATCH-PREFIX-EXTENDED-BY-CURRENT-SESSION-READY-READBACK
- 摘要来源（公开）：VISIBLE-JOURNAL-PREFIX<br>RECOVER-READY-READBACK-COMPLETED；禁止私有来源：ACTIVE-FAULT-ID<br>FAULT-ACTIVATION-RECORD<br>PRIVATE-LOADER-STATE
- 公开证据投影合同：completionReceipt=RECOVER-READY-READBACK-COMPLETED; correlationBinding=CURRENT-OPERATION-CORRELATION; inspectedRange=RECEIPT-BOUNDED-CONTIGUOUS-CLOSED-PREFIX; invalidOrUnconfirmedDisposition=DO-NOT-MARK-KNOWN; ordering=STABLE-SEQUENCE-NUMBER; projectionKind=CURRENT-SESSION-BOUNDED-JOURNAL-RECEIPT; receiptMustBeCompleted=是; sessionBinding=CURRENT-SESSION
- 可能结果：
| 可见量 | 后继摘要 | 摘要确认条件 | 相容假设 |
|---|---|---|---|
| RECOVER-READY-READBACK | Q-TARGET-READY | 公开 Recover 回执仅以当前会话就绪回读扩展精确保留的调度后公开前缀；它重新确认就绪，但不得重放或回退先前动作时，才确认摘要。 | NORMAL<br>EARLY-DATA |
- 未评估义务：PHYSICAL-DEVICE-RECOVERY

## 时钟、观测、复位和恢复

- 时钟为精确的虚拟工程调度 tick；同 tick 用稳定序号排序。有限观察窗口只界定模拟对象检查，绝不证明协议超时或无响应 FAIL。
- 时钟：`CLK-VIRTUAL-615A-SLICE` / `NONNEGATIVE-INTEGER`；不确定性：`U-VIRTUAL-EXACT-ENGINEERING-ONLY` / `ZERO-WIDTH-VIRTUAL-ENGINEERING-MODEL`

## 资源准入与记账边界

- 资源由既有会话在调度前准入；ROUNDS 是剩余执行次数而非金额，BUDGET 是可负担工程费用。执行后错误仍保留实际后继，不能借资源规则回滚对象。
- 准入所有者／记账所有者：`IF-SELECT-ADMIT` / `REFERENCE-SESSION`
- 受控模式：ROUNDS<br>BUDGET；准入边界：`CHECK-BEFORE-DISPATCH` — 准入必须在调度前完成；资源不足时不得发出动作。
- ROUNDS：ROUNDS 表示剩余可执行次数，不是金额预算。
- BUDGET：BUDGET 表示工程动作的声明成本必须在调度前可负担。
- 调度后错误：`CHARGE-ONCE-PRESERVE-ACTUAL-SUCCESSOR` — 动作已经发出后发生错误时，只计费一次并保留实际后继，不得回滚对象。；未评估：本阶段不评估真实硬件成本或实验臂公平性。

## 故障安装与激活变体

- 每次全量复位同时清理装载器、目标硬件、虚拟时钟、日志、待交付、关联编号和故障安装状态；它不是协议中止。
- 故障安装、控制器回读和独立日志激活是不同证据；未确认的尝试保留为未确认，不得改写为正常。
- 故障安装生命周期：`CURRENT-ENGINEERING-ATTEMPT-UNTIL-FULL-RESET`；撤销动作：`FULL-RESET-REVOKES-ALL-NAMED-VARIANTS`；撤销证据：`RESET-READBACK-FAULT-INSTALLATION-STATE-CLEARED`；撤销失败：`RETAIN-ATTEMPT-AS-INVALID-NOT-NORMAL`。
| 假设 | 安装目标 | 控制器回读 | 激活可见量 | 算法可见性 |
|---|---|---|---|---|
| EARLY-DATA | LOADER-MATCHING-ACK-GUARD-BYPASS | READBACK-MATCHING-ACK-GUARD-BYPASS-ACTIVE | EV_DL_DATA_LUR-BEFORE-MATCHING-EV_TH_ACK_LUR | EVALUATOR-ONLY |
| EARLY-WRQ | LOADER-READINESS-GUARD-BYPASS | READBACK-READINESS-GUARD-BYPASS-ACTIVE | EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001 | EVALUATOR-ONLY |

- Recover 以 UNKNOWN 效果为前提，且恢复目标与确认摘要必须不同；确认失败不产生 KNOWN。

## 场景入口与续接上下文

| 案例 | 入口类型 | 会话绑定 | 关联绑定 | q 状态 | 当前摘要 | 相容假设 | 已完成动作 | 保留公开前缀 |
|---|---|---|---|---|---|---|---|---|
| CASE-NORMAL-CONTROL-TIMELINE | FRESH-ATTEMPT | NEW-CURRENT-SESSION | NEW-CURRENT-OPERATION-CORRELATION | KNOWN | SCENE-ENTRY | NORMAL<br>EARLY-WRQ<br>EARLY-DATA | — | LIST-SUBMISSION-PRECONDITION-RECORDED |
| CASE-EARLY-WRQ-TIMELINE | FRESH-ATTEMPT | NEW-CURRENT-SESSION | NEW-CURRENT-OPERATION-CORRELATION | KNOWN | SCENE-ENTRY | NORMAL<br>EARLY-WRQ<br>EARLY-DATA | — | LIST-SUBMISSION-PRECONDITION-RECORDED |
| CASE-EARLY-DATA-TIMELINE | FRESH-ATTEMPT | NEW-CURRENT-SESSION | NEW-CURRENT-OPERATION-CORRELATION | KNOWN | SCENE-ENTRY | NORMAL<br>EARLY-WRQ<br>EARLY-DATA | — | LIST-SUBMISSION-PRECONDITION-RECORDED |
| CASE-UNKNOWN-RECOVER-CONTINUATION | INHERITED-CONTINUATION | CURRENT-SESSION-ONLY | CURRENT-OPERATION-CORRELATION | KNOWN | Q-PRE-READY-NO-WRQ | NORMAL<br>EARLY-DATA | ACT-INSPECT-NO-WRQ-BEFORE-READY | LIST-SUBMISSION-PRECONDITION-RECORDED<br>INSPECT-NO-WRQ-BEFORE-READY-COMPLETED<br>NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001 |
| CASE-RESOURCE-ADMISSION-BLOCK | INHERITED-CONTINUATION | CURRENT-SESSION-ONLY | CURRENT-OPERATION-CORRELATION | KNOWN | Q-TARGET-READY | NORMAL<br>EARLY-DATA | ACT-INSPECT-NO-WRQ-BEFORE-READY<br>ACT-PREP-ENTER-READY-WINDOW | LIST-SUBMISSION-PRECONDITION-RECORDED<br>INSPECT-NO-WRQ-BEFORE-READY-COMPLETED<br>EV_TH_LUS0001<br>TH-LUS0001-READY-RECEIPT |

### UNKNOWN 到 Recover 合同

| 触发 | 动作 | 轮次 | 可能已发生的可见事件 | 会话处置 | Recover 入口 q | 所需公开证据 | 目标／摘要确认 | 回退规则 | 未确认 Recover |
|---|---|---|---|---|---|---|---|---|---|
| POST-DISPATCH-TEST-SUMMARY-CONFIRMATION-FAILURE | ACT-TEST-ACK-BEFORE-DATA | 2 | EV_DL_WRQ_LUR<br>EV_TH_ACK_LUR<br>EV_DL_DATA_LUR | UNKNOWN-PRESERVE-ACTUAL-SUCCESSOR-AND-POST-DISPATCH-JOURNAL | UNKNOWN | CURRENT-SESSION-READY-READBACK<br>RECOVER-READY-READBACK-COMPLETED<br>EXACT-RETAINED-POST-DISPATCH-PUBLIC-PREFIX<br>RECOVER-READY-READBACK-ONLY-EXTENSION | SEPARATE-REQUIRED-NO-REWIND-OR-REPLAY | NO-REWIND-TO-Q-PRE-READY-NO-WRQ | REMAIN-UNKNOWN |

## 场景时线

| 案例 | 场景说明 | 轮次 | 动作 | 可见事件 | 公开摘要 | 候选集 | 继续 | 资源准入 | 资源原因 | 资源模式 | 可用轮次 | 所需轮次 | 动作收费 | 后继处置 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CASE-NORMAL-CONTROL-TIMELINE | 正常控制时线：先有限检查无提前 WRQ，再建立就绪窗口，最后检查 WRQ—ACK—DATA 顺序。 | 1 | ACT-INSPECT-NO-WRQ-BEFORE-READY | NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001 | Q-PRE-READY-NO-WRQ | NORMAL<br>EARLY-DATA | 是 | — | — | — | — | — | — | — |
| CASE-NORMAL-CONTROL-TIMELINE | 正常控制时线：先有限检查无提前 WRQ，再建立就绪窗口，最后检查 WRQ—ACK—DATA 顺序。 | 2 | ACT-PREP-ENTER-READY-WINDOW | EV_TH_LUS0001 | Q-TARGET-READY | NORMAL<br>EARLY-DATA | 是 | — | — | — | — | — | — | — |
| CASE-NORMAL-CONTROL-TIMELINE | 正常控制时线：先有限检查无提前 WRQ，再建立就绪窗口，最后检查 WRQ—ACK—DATA 顺序。 | 3 | ACT-TEST-ACK-BEFORE-DATA | EV_DL_WRQ_LUR<br>EV_TH_ACK_LUR<br>EV_DL_DATA_LUR | Q-LUR-ORDER-ASSESSED | NORMAL | 否 | — | — | — | — | — | — | — |
| CASE-EARLY-WRQ-TIMELINE | 提前 WRQ 时线：有限检查直接在公开日志中发现 LUS-0001 前的 WRQ。 | 1 | ACT-INSPECT-NO-WRQ-BEFORE-READY | EV_DL_WRQ_LUR | Q-EARLY-WRQ-OBSERVED | EARLY-WRQ | 否 | — | — | — | — | — | — | — |
| CASE-EARLY-DATA-TIMELINE | 提前 DATA 时线：先完成同一就绪前检查与准备，再由顺序检查发现匹配 ACK 前的 DATA。 | 1 | ACT-INSPECT-NO-WRQ-BEFORE-READY | NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001 | Q-PRE-READY-NO-WRQ | NORMAL<br>EARLY-DATA | 是 | — | — | — | — | — | — | — |
| CASE-EARLY-DATA-TIMELINE | 提前 DATA 时线：先完成同一就绪前检查与准备，再由顺序检查发现匹配 ACK 前的 DATA。 | 2 | ACT-PREP-ENTER-READY-WINDOW | EV_TH_LUS0001 | Q-TARGET-READY | NORMAL<br>EARLY-DATA | 是 | — | — | — | — | — | — | — |
| CASE-EARLY-DATA-TIMELINE | 提前 DATA 时线：先完成同一就绪前检查与准备，再由顺序检查发现匹配 ACK 前的 DATA。 | 3 | ACT-TEST-ACK-BEFORE-DATA | EV_DL_WRQ_LUR<br>EV_DL_DATA_LUR | Q-LUR-ORDER-ASSESSED | EARLY-DATA | 否 | — | — | — | — | — | — | — |
| CASE-UNKNOWN-RECOVER-CONTINUATION | UNKNOWN 续接时线：准备后发生未确认的执行效果，随后只有通过独立 Recover 才能恢复公开就绪摘要。 | 1 | ACT-PREP-ENTER-READY-WINDOW | EV_TH_LUS0001 | Q-TARGET-READY | NORMAL<br>EARLY-DATA | 是 | — | — | — | — | — | — | — |
| CASE-UNKNOWN-RECOVER-CONTINUATION | UNKNOWN 续接时线：准备后发生未确认的执行效果，随后只有通过独立 Recover 才能恢复公开就绪摘要。 | 2 | ACT-TEST-ACK-BEFORE-DATA | EXECUTION-EFFECT-UNKNOWN | NONE | NORMAL<br>EARLY-DATA | 是 | — | — | — | — | — | — | — |
| CASE-UNKNOWN-RECOVER-CONTINUATION | UNKNOWN 续接时线：准备后发生未确认的执行效果，随后只有通过独立 Recover 才能恢复公开就绪摘要。 | 3 | ACT-RECOVER-RECONFIRM-READY | RECOVER-READY-READBACK | Q-TARGET-READY | NORMAL<br>EARLY-DATA | 是 | — | — | — | — | — | — | — |
| CASE-RESOURCE-ADMISSION-BLOCK | 资源准入边界：资源不足时在调度前拒绝动作，不产生对象事件、不收费且保持调度前后继。 | 1 | ACT-TEST-ACK-BEFORE-DATA | NO-DISPATCH-INSUFFICIENT-RESOURCE | NONE | NORMAL<br>EARLY-DATA | 否 | NOT-ADMITTED | INSUFFICIENT-RESOURCE-BEFORE-DISPATCH | ROUNDS | 0 | 1 | 否 | PRE-DISPATCH-SUCCESSOR-UNCHANGED |

## 实验接口交接

| 接口 | 工程交接 | 公开投影 | 评估方投影 | 共享组件风险 | 不准入内容 |
|---|---|---|---|---|---|
| IF-EXP-SCENE | 仅移交稳定场景族、公开配置和准备边界。 | 仅投影场景族、公开配置、准备边界和尝试身份。 | 该交接不得释放活动故障、控制器状态或加载器私有状态。 | 场景与来源解释与预测器共享，必须披露其共同模式风险。 | 不准入正式实验场景、真实 IUT 运行或合格 UPLOAD 完成。 |
| IF-EXP-INJECT | 安装、控制器回读、激活和未确认尝试记录必须保持分离。 | 算法路径只能消费所得可见日志。 | 具名故障计划、控制器回读、激活记录和未确认处置仅评估方可见。 | 控制器、回读和对象分支由同一作者实现，不主张独立的注入 oracle。 | 已安装或已计划的变体不自动成为已确认故障真值或实验注入计划。 |
| IF-EXP-TRUTH | 替代真值仅供评估方可见，并显式保留共享组件风险。 | 真值假设、安装结果和等价性处置均不得进入算法投影。 | 替代真值仅保留给后续评估／审计比较，并记录其来源。 | 对象、来源解释、时钟和事件 DTO 可能与预测器或评估器共享。 | 不建立独立 oracle、真实根因标签或科学检测主张。 |
| IF-EXP-COLLECT | 只移交本次运行的可见日志与资源日志。 | 只投影当前运行的可见日志、资源日志和稳定尝试引用。 | 私有控制器／回读记录与算法可见采集保持分离。 | 共享事件序列化和日志排序仍是必须披露的实现风险。 | 不建立跨臂借用、历史抓包真值或完整证据包。 |
| IF-EXP-RUN | 只移交 CL-LOOP 工程运行、停止和迹标识。 | 只投影 CL-LOOP 工程尝试身份、有类型会话上下文、停止和迹引用。 | 评估方真值和故障激活保持在有类型会话上下文之外。 | 有限闭环、预测器和适配器仍是一条工程链，不是独立实验臂。 | 不准入四臂运行器、性能比较或真实 IUT 执行。 |
| IF-EXP-FILTER | 为后续记账保留未运行、未确认和无效尝试。 | 保留具名尝试处置和迹引用，不得静默删除失败。 | 未确认安装和无效记录原因必须可供审计记账。 | 处置类别共享同一工程控制器，不构成独立质量过滤器。 | 不建立有效样本分母、科学排除规则或已确认实验数据集。 |
| IF-EXP-EVAL | 保留关联证据与权限；不得计算实验指标。 | 只投影关联的公开证据和声明的权限边界。 | 评估／审计证据以稳定引用关联，但不得成为算法输入。 | 证据比较与工程链共享场景来源和事件模型。 | 不得计算检测、定位、已回答分母、效应量或正式实验指标。 |

## 可行性见证

| 见证 | 入口 | 中文受限主张 |
|---|---|---|
| WIT-FINITE-NO-WRQ-TEST | ReferenceSession unbound normal TEST path | 无绑定的正常 TEST 可返回非空有限检查观测、公开确认摘要和精确虚拟 tick，而不声称协议无响应语义。 |
| WIT-PUBLIC-SUMMARY | Scenario adapter public-journal projection | 带类型的当前会话／当前关联有界公开日志前缀与已完成回执必须确定地产生声明的 postSummary；回执身份、范围或完成状态无效时不得确认或缩小 H，且与仅评估方可见的故障标签无关。 |
| WIT-P3-UNAVAILABLE | RuntimeAuthorityBinding with actual new model/binding path | 不评估完整性的控制切片保留 P3-UNAVAILABLE 和已命名的未评估义务，不借用旧适用性夹具。 |
| WIT-SUCCESSOR-AND-RECOVER | Restricted SyntheticEnvironment subclass seam | 继承的 H／q／前缀、返回后继、待交付日志和执行后 TEST 摘要确认失败路径须保留演进后的有类型对象以进入 UNKNOWN；合格的当前会话 Recover 重新确认独立就绪目标与摘要，但不得回退为就绪前续接状态。 |

## 明确限制

- 不作完整 UPLOAD、文件传输、CRC、校验值、命名或完整性能力结论。
- 不作协议无响应截止、物理计时校准、真实网络、IUT、SIL/HIL 或符合性判定。
- 不运行四臂实验、预实验或确认性实验，也不产生独立真值或 C1/C2 科学主张。
