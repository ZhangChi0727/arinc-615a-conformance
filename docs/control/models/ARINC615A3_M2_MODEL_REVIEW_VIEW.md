# ARINC 615A-3 M2 observable timed model — review view

> Generated from `configs/models/arinc_615a3_m2_model.json` by `python scripts/sync_m2_model.py --write`. Do not edit this view.

## Input acceptance

- Approved Head: `d9d844306acafd99d14ed382d1dc34dedfe837a0`
- Merge: `9bf18124d405b656815bc9eb524ae29bb4f04f56` parents `75e38e08cbcab7c55ad14581e1fc605bc4106bc4` + `d9d844306acafd99d14ed382d1dc34dedfe837a0`
- Tree: `2810bcaa76003eef791348607b068d76d91b5103` / approved-head tree `2810bcaa76003eef791348607b068d76d91b5103`
- CI: https://github.com/ZhangChi0727/arinc-615a-conformance/actions/runs/34303792744 on `9bf18124d405b656815bc9eb524ae29bb4f04f56`
- Sign-off: https://github.com/ZhangChi0727/arinc-615a-conformance/pull/13#issuecomment-5594842302 (`COMMENTED`, `APPROVE WITH ACTIONS`)
- Independence: `NOT-CLAIMED-NAMED-INDEPENDENT-REVIEWER`
- M1 NET-ISSUE-EDITION snapshot blocksM1Approval=`True` — Historical snapshot on the merged M1 tree. External owner sign-off and merge bound that Head. The boolean does not reopen the merge. CR-2026-009 accepted 664P3-1 as this M2 input edition; 664P7 remains recorded and AFDX stays unselected.
- Successor delta `CR-2026-012` authorized by `CR-2026-009`; doesNotTransplantFrozenApproval=`True`
- Predecessor input artifact commit `402e8371b0237aec4691bab0b44e502f4ac1a7c4` tree `26ea73a18fafbd4ba93c9dbb2890eb8453b0ad97`
- Current input artifact commit `bcaa4efea6e2695e3063c5a2596e9a0f019c070d` tree `103cbc1fb5c75dd2efdf6243af0302f2a83d0800`

## Scope

- Services: UPLOAD, INFORMATION; deferred DOWNLOAD, FIND
- Network: `COMPLIANT`; AFDX selected `False`; P3 profiled `False`
- Form: `M=(S,s0,V,C,P,E,T,Inv)`; initial `S_IDLE`
- Delay grows clocks in C; variables stay unchanged; invariants hold. A discrete step binds the input event's typed payload, evaluates the guard (PAYLOAD names read that payload, not implicit variable writes), then updates, then resets matching clock instances, then outputs, then the target. Timeout and WAIT-elapsed events are enabled only by COMPARE(enablingCompare) between enablingClock and enablingBound. The input event is the stimulus; outputs are additional emissions and must not repeat the stimulus as a second message.
- NETWORK-VISIBLE events are TFTP opcodes on a named file role. LUR is a TFTP write: DL WRQ, TH ACK, DL DATA. APPLICATION payload.decision is a typed ENUM evaluated in the guard before lastDecision is written. PARSE-RESULT/LOCAL events are derived from received files or local analysis and are not additional wire opcodes. ENVIRONMENT timeouts and WAIT-elapsed are enabled only by COMPARE(enablingCompare) of enablingClock and enablingBound.

## Events

| ID | Visibility | Summary |
|---|---|---|
| `EV_DL_RRQ_LCI` | NETWORK-VISIBLE | DL TFTP RRQ for LCI |
| `EV_TH_DATA_LCI` | NETWORK-VISIBLE | TH TFTP DATA of LCI |
| `EV_DL_APP_INF_RESPONSE` | APPLICATION | DL initialization response after LCI analysis |
| `EV_TH_WRQ_LCL` | NETWORK-VISIBLE | TH TFTP WRQ for LCL |
| `EV_DL_ACK_LCL` | NETWORK-VISIBLE | DL ACK of LCL WRQ |
| `EV_TH_DATA_LCL` | NETWORK-VISIBLE | TH TFTP DATA of LCL |
| `EV_DL_APP_INF` | APPLICATION | DL application consumes LCL |
| `EV_TH_WRQ_LCS` | NETWORK-VISIBLE | TH TFTP WRQ for LCS |
| `EV_TH_DATA_LCS` | NETWORK-VISIBLE | TH TFTP DATA of LCS |
| `EV_DL_APP_INF_STATUS` | APPLICATION | DL application consumes LCS |
| `EV_DL_RRQ_LUI` | NETWORK-VISIBLE | DL TFTP RRQ for LUI |
| `EV_TH_DATA_LUI` | NETWORK-VISIBLE | TH TFTP DATA of LUI |
| `EV_DL_APP_UPL_RESPONSE` | APPLICATION | DL initialization response after LUI analysis |
| `EV_DL_OFFER_LIST` | APPLICATION | DL offers the load list after init accept |
| `EV_TH_LUS0001` | NETWORK-VISIBLE | TH LUS with status 0001 while list not accepted |
| `EV_DL_WRQ_LUR` | NETWORK-VISIBLE | DL TFTP WRQ for LUR after list accept |
| `EV_TH_ACK_LUR` | NETWORK-VISIBLE | TH ACK of LUR WRQ |
| `EV_DL_DATA_LUR` | NETWORK-VISIBLE | DL TFTP DATA of LUR list |
| `EV_TH_RRQ_FILE` | NETWORK-VISIBLE | TH TFTP RRQ for a requested upload file |
| `EV_DL_FILE_UNAVAIL` | NETWORK-VISIBLE | DL reports requested file unavailable |
| `EV_DL_DATA_FILE` | NETWORK-VISIBLE | DL TFTP DATA of requested upload file |
| `EV_TH_FILE_STATUS` | LOCAL | TH records per-file LUS status after reception |
| `EV_TH_MORE_FILES` | LOCAL | TH selects another file or moves to status |
| `EV_TH_WRQ_LUS` | NETWORK-VISIBLE | TH TFTP WRQ for LUS status |
| `EV_TH_DATA_LUS` | NETWORK-VISIBLE | TH TFTP DATA of LUS |
| `EV_DL_APP_UPL_STATUS` | APPLICATION | DL application consumes LUS |
| `EV_LOCAL_EVAL` | LOCAL | Local evaluation; not claimed observed on the network |
| `EV_ABORT_DL` | NETWORK-VISIBLE | DL abort |
| `EV_ABORT_TH` | NETWORK-VISIBLE | TH abort |
| `EV_TFTP_ACK` | NETWORK-VISIBLE | Generic TFTP ACK on the active file channel |
| `EV_TFTP_ERROR` | NETWORK-VISIBLE | TFTP error |
| `EV_TIMEOUT_TFTP` | ENVIRONMENT | TFTP clock expired; enabled only when CLK_TFTP >= TFTP_TO |
| `EV_TIMEOUT_DLP` | ENVIRONMENT | DLP clock expired; enabled only when CLK_DLP >= DLP_TO |
| `EV_TIMEOUT_EXCEPTION` | ENVIRONMENT | Exception clock expired; enabled only when CLK_EXCEPTION >= EXCEPTION_TIMER |
| `EV_WAIT_RECEIVED` | PARSE-RESULT | WAIT message received; starts the not-before delay clock |
| `EV_WAIT_ELAPSED` | ENVIRONMENT | WAIT delay elapsed; enabled only when CLK_WAIT >= MESSAGE_TIMER_VALUE |
| `EV_OP_COMPLETE` | PARSE-RESULT | Completion decided from LCS/LUS status, not a forged success |

## States

| ID | Terminal | Summary |
|---|---|---|
| `S_IDLE` | False | No active operation |
| `S_INF_LCI_RRQ` | False | INFORMATION LCI RRQ outstanding |
| `S_INF_LCI_XFER` | False | LCI TFTP transfer |
| `S_INF_EVALUATE` | False | Local LCI analysis; not network-visible |
| `S_INF_REJECTED` | True | INFORMATION initialization rejected |
| `S_INF_LCL_WRQ` | False | TH WRQ for LCL after init accept |
| `S_INF_LCL_XFER` | False | LCL list transfer |
| `S_INF_APP` | False | Application consumes LCL |
| `S_INF_LCS_WRQ` | False | TH WRQ for LCS status |
| `S_INF_LCS_XFER` | False | LCS status transfer |
| `S_INF_COMPLETE` | False | INFORMATION complete; may bootstrap UPLOAD |
| `S_INF_EXCEPTION` | False | INFORMATION exception wait |
| `S_UPL_LUI_RRQ` | False | UPLOAD LUI RRQ outstanding |
| `S_UPL_LUI_XFER` | False | LUI TFTP transfer |
| `S_UPL_EVALUATE` | False | Local LUI analysis; not network-visible |
| `S_UPL_REJECTED` | True | UPLOAD initialization rejected |
| `S_UPL_LIST_SENT` | False | DL offered the load list after init accept |
| `S_UPL_WAIT_LUS0001` | False | Wait LUS-0001 while list not yet accepted |
| `S_UPL_LUR_WRQ` | False | DL WRQ for LUR after list accept (TFTP write) |
| `S_UPL_LUR_ACK` | False | TH ACK of LUR write request |
| `S_UPL_LUR_XFER` | False | LUR list transfer; distinct from file data |
| `S_UPL_FILE_RRQ` | False | TH RRQ for a requested upload file |
| `S_UPL_FILE_UNAVAIL` | False | Requested file unavailable |
| `S_UPL_FILE_XFER` | False | Requested upload file transfer |
| `S_UPL_FILE_STATUS` | False | TH writes per-file LUS status |
| `S_UPL_MORE_FILES` | False | More files required or status update due |
| `S_UPL_LUS_WRQ` | False | TH WRQ for LUS status update |
| `S_UPL_LUS_XFER` | False | LUS status transfer |
| `S_UPL_STATUS_APP` | False | Application consumes LUS |
| `S_UPL_COMPLETE` | True | UPLOAD completed without treating abort as success |
| `S_UPL_EXCEPTION` | False | UPLOAD exception wait |
| `S_WAIT_RETRY` | False | WAIT-message delay; retry not enabled before the carried timer |
| `S_ABORTING` | False | Abort in progress |
| `S_ABORTED` | True | Aborted terminal |
| `S_FAILED` | True | Failed terminal |

## Variables

| ID | Type | Initial | Domain |
|---|---|---|---|
| `activeOperation` | ENUM | NONE | NONE, INFORMATION, UPLOAD |
| `lastDecision` | ENUM | NONE | NONE, ACCEPT, REJECT |
| `waitResume` | ENUM | NONE | NONE, UPL_FILE, UPL_LUR, INF_LCI, INF_LCL |
| `listOffered` | ENUM | FALSE | FALSE, TRUE |
| `targetListReady` | ENUM | FALSE | FALSE, TRUE |
| `listAccepted` | ENUM | FALSE | FALSE, TRUE |
| `lciComplete` | ENUM | FALSE | FALSE, TRUE |
| `lclComplete` | ENUM | FALSE | FALSE, TRUE |
| `luiComplete` | ENUM | FALSE | FALSE, TRUE |
| `lurComplete` | ENUM | FALSE | FALSE, TRUE |
| `requestedFileAvailable` | ENUM | TRUE | TRUE, FALSE |
| `moreFilesRequired` | ENUM | FALSE | TRUE, FALSE |
| `statusCode` | ENUM | NONE | NONE, 0X0001, 0X0003, FROM-LCS, FROM-LUS, EXCEPTION |
| `integrityClaim` | ENUM | FALSE | FALSE, TRUE |
| `fileBytes` | INT | 0 | — |
| `tftpRetries` | INT | 0 | — |
| `dlpRetries` | INT | 0 | — |

## Parameters

| ID | Unit | Kind | Value | Meaning |
|---|---|---|---|---|
| `TFTP_TO` | s | FIXED-SOURCE-CONSTANT | 2 | Defines the 2s TFTP constant; responses are not required to occur at exactly 2s. |
| `DLP_TO` | s | FIXED-SOURCE-CONSTANT | 13 | Defines the 13s DLP constant; it is not a claim that every gap lasts 13s. |
| `TFTP_RETRY` | 1 | SYMBOLIC-SOURCE-PARAMETER | None | Attachment 4 TFTP retry count. |
| `DLP_RETRY` | 1 | SYMBOLIC-SOURCE-PARAMETER | None | Attachment 4 DLP retry count. |
| `DURATION_TIME` | s | SYMBOLIC-SOURCE-PARAMETER | None | Observed inter-transfer duration in the Attachment 4 inequality. |
| `EXCEPTION_TIMER` | s | MESSAGE-CARRIED-PARAMETER | None | Exception timer carried by LCS/LUS. |
| `MESSAGE_TIMER_VALUE` | s | MESSAGE-CARRIED-PARAMETER | None | Wait-message timer value. |
| `MAX_JITTER` | us | SYMBOLIC-SOURCE-PARAMETER | None | Observed max_jitter in the 664-7 End-System output formulas. |
| `LMAX_I` | 1 | SYMBOLIC-SOURCE-PARAMETER | None | Per-VL maximum frame length Lmax_i in octets. Indexed over the configured VL set; values may differ. The 20-octet overhead is added inside the sum for each VL. |
| `NBW` | 1 | SYMBOLIC-SOURCE-PARAMETER | None | Positive medium bandwidth Nbw in bits/s. The load term is seconds before *1000000 conversion to us. Division by zero is undefined. |
| `FRAME_DELAY` | us | SYMBOLIC-SOURCE-PARAMETER | None | Frame delay added to the 150 us TX technological-latency bound. |
| `TECH_LAT_TX` | us | SYMBOLIC-SOURCE-PARAMETER | None | Measured TX technological latency between the named endpoints. |
| `TECH_LAT_RX` | us | SYMBOLIC-SOURCE-PARAMETER | None | Measured RX technological latency between the named endpoints. |

## Clocks

| ID | Scope | Correlation | Reset on | Meaning |
|---|---|---|---|---|
| `CLK_TFTP` | PER-CORRELATION-KEY | TFTP-PEER-AND-TRANSFER | `T_INF_LCI_RRQ`, `T_UPL_LUI_RRQ`, `T_UPL_LUR_WRQ`, `T_UPL_FILE_RRQ` | Time since last TFTP packet of the correlated transfer. |
| `CLK_DLP` | PER-CORRELATION-KEY | TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE | `T_INF_ACCEPT_INIT`, `T_UPL_ACCEPT_INIT`, `T_UPL_LUR_WRQ`, `T_UPL_FILE_RRQ` | Inter-operation / inter-transfer DLP clock. |
| `CLK_EXCEPTION` | PER-CORRELATION-KEY | STATUS-EXCEPTION-OBJECT | `T_ENTER_UPL_EXC`, `T_ENTER_INF_EXC`, `T_INF_LCS_WRQ` | Exception silence clock. |
| `CLK_WAIT` | PER-CORRELATION-KEY | TFTP-PEER-AND-REJECTED-TRANSFER-REQUEST | `T_WAIT_FROM_UPL_FILE`, `T_WAIT_FROM_UPL_LUR`, `T_WAIT_FROM_INF_LCI`, `T_WAIT_FROM_INF_LCL` | Delay since the WAIT message that forbids retry until the carried timer elapses. |
| `CLK_FIND` | PER-CORRELATION-KEY | FIND-REQUEST-INSTANCE |  | Observational FIND request/answer clock. Bound M2 transitions do not reset it. |
| `CLK_AFDX_ES` | PER-CORRELATION-KEY | AFDX-END-SYSTEM-MEASUREMENT-INSTANCE |  | Observational AFDX End-System technological-latency and jitter clock. Bound M2 transitions do not reset it. |

## Invariants

| ID | States | AST | Note |
|---|---|---|---|
| `INV-NO-FILE-BEFORE-LUR` | `S_UPL_EVALUATE`, `S_UPL_LIST_SENT`, `S_UPL_WAIT_LUS0001`, `S_UPL_LUR_WRQ`, `S_UPL_LUR_ACK` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"lurComplete"},"right":{"kind":"ENUM","value":"FALSE"}}` | File RRQ is disabled until LUR completes. |
| `INV-INTEGRITY-FALSE` | `S_UPL_COMPLETE` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"integrityClaim"},"right":{"kind":"ENUM","value":"FALSE"}}` | Completion cannot claim integrity while 645 is open. |

## Transitions

| ID | Source | Event | Target | Guard | Updates | Outputs | Resets | Requirements |
|---|---|---|---|---|---|---|---|---|
| `T_INF_LCI_RRQ` | `S_IDLE` | `EV_DL_RRQ_LCI` | `S_INF_LCI_RRQ` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"NONE"}}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"INFORMATION"}},{"kind":"ASSIGN","target":"lastDecision","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"waitResume","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"listOffered","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"targetListReady","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"listAccepted","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lurComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"luiComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lciComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lclComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"statusCode","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"integrityClaim","value":{"kind":"ENUM","value":"FALSE"}}]` | — | CLK_TFTP | `CRS-M1-00347` |
| `T_INF_LCI_XFER` | `S_INF_LCI_RRQ` | `EV_TH_DATA_LCI` | `S_INF_LCI_XFER` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | `[{"kind":"ASSIGN","target":"lciComplete","value":{"kind":"ENUM","value":"TRUE"}}]` | — | CLK_TFTP | `CRS-M1-00348` |
| `T_INF_EVAL` | `S_INF_LCI_XFER` | `EV_LOCAL_EVAL` | `S_INF_EVALUATE` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | — | — | — | `CRS-M1-00349` |
| `T_INF_ACCEPT_INIT` | `S_INF_EVALUATE` | `EV_DL_APP_INF_RESPONSE` | `S_INF_LCL_WRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"PAYLOAD","name":"decision"},"right":{"kind":"ENUM","value":"ACCEPT"}}]}` | `[{"kind":"ASSIGN","target":"lastDecision","value":{"kind":"ENUM","value":"ACCEPT"}}]` | — | CLK_DLP | `CRS-M1-00349`, `CRS-M1-00351` |
| `T_INF_REJECT` | `S_INF_EVALUATE` | `EV_DL_APP_INF_RESPONSE` | `S_INF_REJECTED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"PAYLOAD","name":"decision"},"right":{"kind":"ENUM","value":"REJECT"}}]}` | `[{"kind":"ASSIGN","target":"lastDecision","value":{"kind":"ENUM","value":"REJECT"}},{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00350` |
| `T_INF_LCL_WRQ` | `S_INF_LCL_WRQ` | `EV_TH_WRQ_LCL` | `S_INF_LCL_WRQ` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | — | — | CLK_TFTP | `CRS-M1-00351` |
| `T_INF_LCL_ACK` | `S_INF_LCL_WRQ` | `EV_DL_ACK_LCL` | `S_INF_LCL_XFER` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | — | — | CLK_TFTP | `CRS-M1-00352` |
| `T_INF_LCL_XFER` | `S_INF_LCL_XFER` | `EV_TH_DATA_LCL` | `S_INF_APP` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | `[{"kind":"ASSIGN","target":"lclComplete","value":{"kind":"ENUM","value":"TRUE"}}]` | — | CLK_TFTP | `CRS-M1-00353` |
| `T_INF_APP` | `S_INF_APP` | `EV_DL_APP_INF` | `S_INF_LCS_WRQ` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | — | — | — | `CRS-M1-00354` |
| `T_INF_LCS_WRQ` | `S_INF_LCS_WRQ` | `EV_TH_WRQ_LCS` | `S_INF_LCS_XFER` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | — | — | CLK_TFTP, CLK_EXCEPTION | `CRS-M1-00355` |
| `T_INF_LCS_XFER` | `S_INF_LCS_XFER` | `EV_TH_DATA_LCS` | `S_INF_COMPLETE` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | `[{"kind":"ASSIGN","target":"statusCode","value":{"kind":"ENUM","value":"FROM-LCS"}},{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | CLK_TFTP | `CRS-M1-00356`, `CRS-M1-00357`, `CRS-M1-00358` |
| `T_INF_SESSION_END` | `S_INF_COMPLETE` | `EV_OP_COMPLETE` | `S_IDLE` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"NONE"}}` | — | — | — | `CRS-M1-00358` |
| `T_UPL_LUI_RRQ` | `S_IDLE` | `EV_DL_RRQ_LUI` | `S_UPL_LUI_RRQ` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"NONE"}}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"ASSIGN","target":"lastDecision","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"waitResume","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"listOffered","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"targetListReady","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"listAccepted","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lurComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"luiComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lciComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lclComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"statusCode","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"integrityClaim","value":{"kind":"ENUM","value":"FALSE"}}]` | — | CLK_TFTP | `CRS-M1-00359`, `CRS-M1-00360` |
| `T_UPL_LUI_RRQ_AFTER_INF` | `S_INF_COMPLETE` | `EV_DL_RRQ_LUI` | `S_UPL_LUI_RRQ` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"NONE"}}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"ASSIGN","target":"lastDecision","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"waitResume","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"listOffered","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"targetListReady","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"listAccepted","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lurComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"luiComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lciComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lclComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"statusCode","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"integrityClaim","value":{"kind":"ENUM","value":"FALSE"}}]` | — | CLK_TFTP | `CRS-M1-00360` |
| `T_UPL_LUI_XFER` | `S_UPL_LUI_RRQ` | `EV_TH_DATA_LUI` | `S_UPL_LUI_XFER` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | `[{"kind":"ASSIGN","target":"luiComplete","value":{"kind":"ENUM","value":"TRUE"}}]` | — | CLK_TFTP | `CRS-M1-00361` |
| `T_UPL_EVAL` | `S_UPL_LUI_XFER` | `EV_LOCAL_EVAL` | `S_UPL_EVALUATE` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | — | — | — | `CRS-M1-00362` |
| `T_UPL_ACCEPT_INIT` | `S_UPL_EVALUATE` | `EV_DL_APP_UPL_RESPONSE` | `S_UPL_LIST_SENT` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"PAYLOAD","name":"decision"},"right":{"kind":"ENUM","value":"ACCEPT"}}]}` | `[{"kind":"ASSIGN","target":"lastDecision","value":{"kind":"ENUM","value":"ACCEPT"}}]` | — | CLK_DLP | `CRS-M1-00362`, `CRS-M1-00363` |
| `T_UPL_REJECT` | `S_UPL_EVALUATE` | `EV_DL_APP_UPL_RESPONSE` | `S_UPL_REJECTED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"PAYLOAD","name":"decision"},"right":{"kind":"ENUM","value":"REJECT"}}]}` | `[{"kind":"ASSIGN","target":"lastDecision","value":{"kind":"ENUM","value":"REJECT"}},{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00362` |
| `T_UPL_LIST_OFFER` | `S_UPL_LIST_SENT` | `EV_DL_OFFER_LIST` | `S_UPL_WAIT_LUS0001` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | `[{"kind":"ASSIGN","target":"listOffered","value":{"kind":"ENUM","value":"TRUE"}}]` | — | CLK_DLP | `CRS-M1-00363`, `CRS-M1-00364` |
| `T_UPL_WAIT_LUS0001` | `S_UPL_WAIT_LUS0001` | `EV_TH_LUS0001` | `S_UPL_WAIT_LUS0001` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"listOffered"},"right":{"kind":"ENUM","value":"TRUE"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"listAccepted"},"right":{"kind":"ENUM","value":"FALSE"}}]}` | `[{"kind":"ASSIGN","target":"statusCode","value":{"kind":"ENUM","value":"0X0001"}},{"kind":"ASSIGN","target":"targetListReady","value":{"kind":"ENUM","value":"TRUE"}}]` | — | CLK_EXCEPTION | `CRS-M1-00364` |
| `T_UPL_LUR_WRQ` | `S_UPL_WAIT_LUS0001` | `EV_DL_WRQ_LUR` | `S_UPL_LUR_WRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"listOffered"},"right":{"kind":"ENUM","value":"TRUE"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"targetListReady"},"right":{"kind":"ENUM","value":"TRUE"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"listAccepted"},"right":{"kind":"ENUM","value":"FALSE"}}]}` | `[{"kind":"ASSIGN","target":"listAccepted","value":{"kind":"ENUM","value":"TRUE"}}]` | — | CLK_TFTP, CLK_DLP | `CRS-M1-00365` |
| `T_UPL_LUR_ACK` | `S_UPL_LUR_WRQ` | `EV_TH_ACK_LUR` | `S_UPL_LUR_ACK` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | — | — | CLK_TFTP | `CRS-M1-00366` |
| `T_UPL_LUR_XFER` | `S_UPL_LUR_ACK` | `EV_DL_DATA_LUR` | `S_UPL_LUR_XFER` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | `[{"kind":"ASSIGN","target":"lurComplete","value":{"kind":"ENUM","value":"TRUE"}}]` | — | CLK_TFTP | `CRS-M1-00367` |
| `T_UPL_FILE_RRQ` | `S_UPL_LUR_XFER` | `EV_TH_RRQ_FILE` | `S_UPL_FILE_RRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"lurComplete"},"right":{"kind":"ENUM","value":"TRUE"}}]}` | — | — | CLK_TFTP, CLK_DLP | `CRS-M1-00368` |
| `T_UPL_FILE_RRQ_MORE` | `S_UPL_MORE_FILES` | `EV_TH_RRQ_FILE` | `S_UPL_FILE_RRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"moreFilesRequired"},"right":{"kind":"ENUM","value":"TRUE"}}]}` | — | — | CLK_TFTP | `CRS-M1-00368`, `CRS-M1-00372` |
| `T_UPL_FILE_UNAVAIL` | `S_UPL_FILE_RRQ` | `EV_DL_FILE_UNAVAIL` | `S_UPL_FILE_UNAVAIL` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"requestedFileAvailable"},"right":{"kind":"ENUM","value":"FALSE"}}]}` | — | — | — | `CRS-M1-00369` |
| `T_UPL_FILE_XFER` | `S_UPL_FILE_RRQ` | `EV_DL_DATA_FILE` | `S_UPL_FILE_XFER` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"requestedFileAvailable"},"right":{"kind":"ENUM","value":"TRUE"}}]}` | `[{"kind":"ASSIGN","target":"fileBytes","value":{"kind":"LITERAL","value":0}}]` | — | CLK_TFTP | `CRS-M1-00370` |
| `T_UPL_FILE_STATUS` | `S_UPL_FILE_XFER` | `EV_TH_FILE_STATUS` | `S_UPL_FILE_STATUS` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | — | — | — | `CRS-M1-00371` |
| `T_UPL_MORE_FILES` | `S_UPL_FILE_STATUS` | `EV_TH_MORE_FILES` | `S_UPL_MORE_FILES` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | — | — | — | `CRS-M1-00372` |
| `T_UPL_TO_LUS` | `S_UPL_MORE_FILES` | `EV_TH_WRQ_LUS` | `S_UPL_LUS_WRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"moreFilesRequired"},"right":{"kind":"ENUM","value":"FALSE"}}]}` | — | — | CLK_TFTP | `CRS-M1-00373` |
| `T_UPL_LUS_XFER` | `S_UPL_LUS_WRQ` | `EV_TH_DATA_LUS` | `S_UPL_LUS_XFER` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | `[{"kind":"ASSIGN","target":"statusCode","value":{"kind":"ENUM","value":"FROM-LUS"}}]` | — | CLK_TFTP, CLK_EXCEPTION | `CRS-M1-00374` |
| `T_UPL_STATUS_APP` | `S_UPL_LUS_XFER` | `EV_DL_APP_UPL_STATUS` | `S_UPL_STATUS_APP` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | — | — | — | `CRS-M1-00375` |
| `T_UPL_COMPLETE` | `S_UPL_STATUS_APP` | `EV_OP_COMPLETE` | `S_UPL_COMPLETE` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"statusCode"},"right":{"kind":"ENUM","value":"0X0003"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"integrityClaim"},"right":{"kind":"ENUM","value":"FALSE"}}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00376` |
| `T_UPL_STATUS_REPEAT` | `S_UPL_STATUS_APP` | `EV_TH_MORE_FILES` | `S_UPL_MORE_FILES` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"NE","left":{"kind":"VAR","name":"statusCode"},"right":{"kind":"ENUM","value":"0X0003"}}]}` | — | — | — | `CRS-M1-00376` |
| `T_INF_TFTP_TO` | `S_INF_LCI_RRQ` | `EV_TIMEOUT_TFTP` | `S_FAILED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_TFTP"},"right":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"}}]}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00177` |
| `T_UPL_TFTP_TO` | `S_UPL_LUI_RRQ` | `EV_TIMEOUT_TFTP` | `S_FAILED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_TFTP"},"right":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"}}]}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00177` |
| `T_UPL_LUR_TFTP_TO` | `S_UPL_LUR_WRQ` | `EV_TIMEOUT_TFTP` | `S_FAILED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_TFTP"},"right":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"}}]}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00177` |
| `T_UPL_FILE_TFTP_TO` | `S_UPL_FILE_RRQ` | `EV_TIMEOUT_TFTP` | `S_FAILED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_TFTP"},"right":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"}}]}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00177` |
| `T_UPL_DLP_TO` | `S_UPL_WAIT_LUS0001` | `EV_TIMEOUT_DLP` | `S_FAILED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}]}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00187` |
| `T_UPL_LUR_DLP_TO` | `S_UPL_LUR_XFER` | `EV_TIMEOUT_DLP` | `S_FAILED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}]}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00187`, `CRS-M1-00188` |
| `T_UPL_EXC_TO` | `S_UPL_EXCEPTION` | `EV_TIMEOUT_EXCEPTION` | `S_FAILED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}]}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00101`, `CRS-M1-00108` |
| `T_INF_EXC_TO` | `S_INF_EXCEPTION` | `EV_TIMEOUT_EXCEPTION` | `S_FAILED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}]}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00101` |
| `T_ENTER_UPL_EXC` | `S_UPL_WAIT_LUS0001` | `EV_TH_DATA_LUS` | `S_UPL_EXCEPTION` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | `[{"kind":"ASSIGN","target":"statusCode","value":{"kind":"ENUM","value":"EXCEPTION"}}]` | — | CLK_EXCEPTION | `CRS-M1-00099` |
| `T_ENTER_INF_EXC` | `S_INF_LCS_XFER` | `EV_DL_APP_INF_STATUS` | `S_INF_EXCEPTION` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | `[{"kind":"ASSIGN","target":"statusCode","value":{"kind":"ENUM","value":"EXCEPTION"}}]` | — | CLK_EXCEPTION | `CRS-M1-00099` |
| `T_WAIT_FROM_UPL_FILE` | `S_UPL_FILE_XFER` | `EV_WAIT_RECEIVED` | `S_WAIT_RETRY` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | `[{"kind":"ASSIGN","target":"waitResume","value":{"kind":"ENUM","value":"UPL_FILE"}}]` | — | CLK_WAIT | `CRS-M1-00032` |
| `T_WAIT_FROM_UPL_LUR` | `S_UPL_LUR_XFER` | `EV_WAIT_RECEIVED` | `S_WAIT_RETRY` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | `[{"kind":"ASSIGN","target":"waitResume","value":{"kind":"ENUM","value":"UPL_LUR"}}]` | — | CLK_WAIT | `CRS-M1-00032` |
| `T_WAIT_FROM_INF_LCI` | `S_INF_LCI_XFER` | `EV_WAIT_RECEIVED` | `S_WAIT_RETRY` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | `[{"kind":"ASSIGN","target":"waitResume","value":{"kind":"ENUM","value":"INF_LCI"}}]` | — | CLK_WAIT | `CRS-M1-00032` |
| `T_WAIT_FROM_INF_LCL` | `S_INF_LCL_XFER` | `EV_WAIT_RECEIVED` | `S_WAIT_RETRY` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | `[{"kind":"ASSIGN","target":"waitResume","value":{"kind":"ENUM","value":"INF_LCL"}}]` | — | CLK_WAIT | `CRS-M1-00032` |
| `T_WAIT_RETRY_UPL_FILE` | `S_WAIT_RETRY` | `EV_WAIT_ELAPSED` | `S_UPL_FILE_RRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_WAIT"},"right":{"kind":"SYMBOL","name":"MESSAGE_TIMER_VALUE","unit":"s"}}]},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"waitResume"},"right":{"kind":"ENUM","value":"UPL_FILE"}}]}` | — | — | CLK_TFTP | `CRS-M1-00032` |
| `T_WAIT_RETRY_UPL_LUR` | `S_WAIT_RETRY` | `EV_WAIT_ELAPSED` | `S_UPL_LUR_WRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_WAIT"},"right":{"kind":"SYMBOL","name":"MESSAGE_TIMER_VALUE","unit":"s"}}]},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"waitResume"},"right":{"kind":"ENUM","value":"UPL_LUR"}}]}` | — | — | CLK_TFTP | `CRS-M1-00032` |
| `T_WAIT_RETRY_INF_LCI` | `S_WAIT_RETRY` | `EV_WAIT_ELAPSED` | `S_INF_LCI_RRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_WAIT"},"right":{"kind":"SYMBOL","name":"MESSAGE_TIMER_VALUE","unit":"s"}}]},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"waitResume"},"right":{"kind":"ENUM","value":"INF_LCI"}}]}` | — | — | CLK_TFTP | `CRS-M1-00032` |
| `T_WAIT_RETRY_INF_LCL` | `S_WAIT_RETRY` | `EV_WAIT_ELAPSED` | `S_INF_LCL_WRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_WAIT"},"right":{"kind":"SYMBOL","name":"MESSAGE_TIMER_VALUE","unit":"s"}}]},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"waitResume"},"right":{"kind":"ENUM","value":"INF_LCL"}}]}` | — | — | CLK_TFTP | `CRS-M1-00032` |
| `T_ABORT_DL` | `S_UPL_FILE_XFER` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_TH` | `S_UPL_FILE_XFER` | `EV_ABORT_TH` | `S_ABORTING` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | — | — | — | `CRS-M1-00340` |
| `T_ABORTED` | `S_ABORTING` | `EV_OP_COMPLETE` | `S_ABORTED` | `{"kind":"TRUE"}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00340`, `CRS-M1-00341` |
| `T_ABORT_FROM_S_INF_LCI_RRQ` | `S_INF_LCI_RRQ` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_INF_LCL_XFER` | `S_INF_LCL_XFER` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_INF_LCS_XFER` | `S_INF_LCS_XFER` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_INF_EXCEPTION` | `S_INF_EXCEPTION` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_WAIT_RETRY` | `S_WAIT_RETRY` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_UPL_LUI_XFER` | `S_UPL_LUI_XFER` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_UPL_LIST_SENT` | `S_UPL_LIST_SENT` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_UPL_WAIT_LUS0001` | `S_UPL_WAIT_LUS0001` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_UPL_LUR_XFER` | `S_UPL_LUR_XFER` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_UPL_LUS_XFER` | `S_UPL_LUS_XFER` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |

## Sequence constraints

- `SEQ-UPL-LIST-BEFORE-FILE` order `S_UPL_EVALUATE` → `S_UPL_LIST_SENT` → `S_UPL_WAIT_LUS0001` → `S_UPL_LUR_WRQ` → `S_UPL_LUR_ACK` → `S_UPL_LUR_XFER` → `S_UPL_FILE_RRQ`; forbidden [['S_UPL_EVALUATE', 'S_UPL_FILE_RRQ'], ['S_UPL_EVALUATE', 'S_UPL_FILE_XFER'], ['S_UPL_LIST_SENT', 'S_UPL_FILE_RRQ'], ['S_UPL_WAIT_LUS0001', 'S_UPL_FILE_RRQ'], ['S_UPL_WAIT_LUS0001', 'S_UPL_FILE_XFER'], ['S_INF_EVALUATE', 'S_UPL_FILE_XFER']]; Figure 6.3.2 A requires list accept and LUR transfer before file RRQ.
- `SEQ-INF-LCL-BEFORE-LCS` order `S_INF_EVALUATE` → `S_INF_LCL_WRQ` → `S_INF_LCL_XFER` → `S_INF_LCS_WRQ`; forbidden [['S_INF_EVALUATE', 'S_INF_LCS_XFER']]; INFORMATION list (LCL) precedes LCS status.

## Field constraints

| ID | File | Field | CRS | Check |
|---|---|---|---|---|
| `FC-LCI-FIELD-FILE-LENGTH` | LCI | FIELD-FILE-LENGTH | `CRS-M1-00282` | LCI-FILE-BYTES |
| `FC-LCI-FIELD-PROTOCOL-VERSION` | LCI | FIELD-PROTOCOL-VERSION | `CRS-M1-00283` | LCI-FILE-BYTES |
| `FC-LCI-FIELD-OPERATION-ACCEPTANCE-STATUS-CODE` | LCI | FIELD-OPERATION-ACCEPTANCE-STATUS-CODE | `CRS-M1-00284` | LCI-FILE-BYTES |
| `FC-LCI-FIELD-STATUS-DESCRIPTION-LENGTH` | LCI | FIELD-STATUS-DESCRIPTION-LENGTH | `CRS-M1-00285` | LCI-FILE-BYTES |
| `FC-LCI-FIELD-STATUS-DESCRIPTION` | LCI | FIELD-STATUS-DESCRIPTION | `CRS-M1-00286` | LCI-FILE-BYTES |
| `FC-LCL-FIELD-FILE-LENGTH` | LCL | FIELD-FILE-LENGTH | `CRS-M1-00287` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-PROTOCOL-VERSION` | LCL | FIELD-PROTOCOL-VERSION | `CRS-M1-00288` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-NUMBER-OF-TARGET-HARDWARE` | LCL | FIELD-NUMBER-OF-TARGET-HARDWARE | `CRS-M1-00289` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-LITERAL-NAME-LENGTH` | LCL | FIELD-LITERAL-NAME-LENGTH | `CRS-M1-00290` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-LITERAL-NAME` | LCL | FIELD-LITERAL-NAME | `CRS-M1-00291` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-SERIAL-NUMBER-LENGTH` | LCL | FIELD-SERIAL-NUMBER-LENGTH | `CRS-M1-00292` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-SERIAL-NUMBER` | LCL | FIELD-SERIAL-NUMBER | `CRS-M1-00293` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-NUMBER-OF-PART-NUMBERS` | LCL | FIELD-NUMBER-OF-PART-NUMBERS | `CRS-M1-00294` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-PART-NUMBER-LENGTH` | LCL | FIELD-PART-NUMBER-LENGTH | `CRS-M1-00295` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-PART-NUMBER` | LCL | FIELD-PART-NUMBER | `CRS-M1-00296` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-AMENDMENT-LENGTH` | LCL | FIELD-AMENDMENT-LENGTH | `CRS-M1-00297` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-AMENDMENT` | LCL | FIELD-AMENDMENT | `CRS-M1-00298` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-PART-DESIGNATION-LENGTH` | LCL | FIELD-PART-DESIGNATION-LENGTH | `CRS-M1-00299` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-PART-DESIGNATION-TEXT` | LCL | FIELD-PART-DESIGNATION-TEXT | `CRS-M1-00300` | LCL-FILE-BYTES |
| `FC-LCS-FIELD-FILE-LENGTH` | LCS | FIELD-FILE-LENGTH | `CRS-M1-00301` | LCS-FILE-BYTES |
| `FC-LCS-FIELD-PROTOCOL-VERSION` | LCS | FIELD-PROTOCOL-VERSION | `CRS-M1-00302` | LCS-FILE-BYTES |
| `FC-LCS-FIELD-COUNTER` | LCS | FIELD-COUNTER | `CRS-M1-00303` | LCS-FILE-BYTES |
| `FC-LCS-FIELD-INFORMATION-OPERATION-STATUS-CODE` | LCS | FIELD-INFORMATION-OPERATION-STATUS-CODE | `CRS-M1-00304` | LCS-FILE-BYTES |
| `FC-LCS-FIELD-EXCEPTION-TIMER` | LCS | FIELD-EXCEPTION-TIMER | `CRS-M1-00305` | LCS-FILE-BYTES |
| `FC-LCS-FIELD-ESTIMATED-TIME` | LCS | FIELD-ESTIMATED-TIME | `CRS-M1-00306` | LCS-FILE-BYTES |
| `FC-LCS-FIELD-STATUS-DESCRIPTION-LENGTH` | LCS | FIELD-STATUS-DESCRIPTION-LENGTH | `CRS-M1-00307` | LCS-FILE-BYTES |
| `FC-LCS-FIELD-STATUS-DESCRIPTION` | LCS | FIELD-STATUS-DESCRIPTION | `CRS-M1-00308` | LCS-FILE-BYTES |
| `FC-LUR-FIELD-FILE-LENGTH` | LUR | FIELD-FILE-LENGTH | `CRS-M1-00309` | LUR-FILE-BYTES |
| `FC-LUR-FIELD-PROTOCOL-VERSION` | LUR | FIELD-PROTOCOL-VERSION | `CRS-M1-00310` | LUR-FILE-BYTES |
| `FC-LUR-FIELD-NUMBER-OF-HEADER-FILES` | LUR | FIELD-NUMBER-OF-HEADER-FILES | `CRS-M1-00311` | LUR-FILE-BYTES |
| `FC-LUR-FIELD-HEADER-FILE-NAME-LENGTH` | LUR | FIELD-HEADER-FILE-NAME-LENGTH | `CRS-M1-00312` | LUR-FILE-BYTES |
| `FC-LUR-FIELD-HEADER-FILE-NAME` | LUR | FIELD-HEADER-FILE-NAME | `CRS-M1-00313` | LUR-FILE-BYTES |
| `FC-LUR-FIELD-LOAD-PART-NUMBER-NAME-LENGTH` | LUR | FIELD-LOAD-PART-NUMBER-NAME-LENGTH | `CRS-M1-00314` | LUR-FILE-BYTES |
| `FC-LUR-FIELD-LOAD-PART-NUMBER-NAME` | LUR | FIELD-LOAD-PART-NUMBER-NAME | `CRS-M1-00315` | LUR-FILE-BYTES |
| `FC-LUS-FIELD-FILE-LENGTH` | LUS | FIELD-FILE-LENGTH | `CRS-M1-00316` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-PROTOCOL-VERSION` | LUS | FIELD-PROTOCOL-VERSION | `CRS-M1-00317` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-UPLOAD-OPERATION-STATUS-CODE` | LUS | FIELD-UPLOAD-OPERATION-STATUS-CODE | `CRS-M1-00318` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-UPLOAD-STATUS-DESCRIPTION-LENGTH` | LUS | FIELD-UPLOAD-STATUS-DESCRIPTION-LENGTH | `CRS-M1-00319` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-UPLOAD-STATUS-DESCRIPTION` | LUS | FIELD-UPLOAD-STATUS-DESCRIPTION | `CRS-M1-00320` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-COUNTER` | LUS | FIELD-COUNTER | `CRS-M1-00321` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-EXCEPTION-TIMER` | LUS | FIELD-EXCEPTION-TIMER | `CRS-M1-00322` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-ESTIMATED-TIME` | LUS | FIELD-ESTIMATED-TIME | `CRS-M1-00323` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-LOAD-LIST-RATIO` | LUS | FIELD-LOAD-LIST-RATIO | `CRS-M1-00324` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-NUMBER-OF-HEADER-FILES` | LUS | FIELD-NUMBER-OF-HEADER-FILES | `CRS-M1-00325` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-HEADER-FILE-NAME-LENGTH` | LUS | FIELD-HEADER-FILE-NAME-LENGTH | `CRS-M1-00326` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-HEADER-FILE-NAME` | LUS | FIELD-HEADER-FILE-NAME | `CRS-M1-00327` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-LOAD-PART-NUMBER-NAME-LENGTH` | LUS | FIELD-LOAD-PART-NUMBER-NAME-LENGTH | `CRS-M1-00328` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-LOAD-PART-NUMBER-NAME` | LUS | FIELD-LOAD-PART-NUMBER-NAME | `CRS-M1-00329` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-LOAD-RATIO` | LUS | FIELD-LOAD-RATIO | `CRS-M1-00330` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-LOAD-STATUS` | LUS | FIELD-LOAD-STATUS | `CRS-M1-00331` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-LOAD-STATUS-DESCRIPTION-LENGTH` | LUS | FIELD-LOAD-STATUS-DESCRIPTION-LENGTH | `CRS-M1-00332` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-LOAD-STATUS-DESCRIPTION` | LUS | FIELD-LOAD-STATUS-DESCRIPTION | `CRS-M1-00333` | LUS-FILE-BYTES |
| `FC-LNR-FIELD-FILE-LENGTH` | LNR | FIELD-FILE-LENGTH | `CRS-M1-00459` | LNR-FILE-BYTES |
| `FC-LNR-FIELD-PROTOCOL-VERSION` | LNR | FIELD-PROTOCOL-VERSION | `CRS-M1-00460` | LNR-FILE-BYTES |
| `FC-LNR-FIELD-NUMBER-OF-FILES` | LNR | FIELD-NUMBER-OF-FILES | `CRS-M1-00461` | LNR-FILE-BYTES |
| `FC-LNR-FIELD-FILE-NAME-LENGTH` | LNR | FIELD-FILE-NAME-LENGTH | `CRS-M1-00462` | LNR-FILE-BYTES |
| `FC-LNR-FIELD-FILE-NAME` | LNR | FIELD-FILE-NAME | `CRS-M1-00463` | LNR-FILE-BYTES |
| `FC-LNR-FIELD-USER-DEFINED-DATA-LENGTH` | LNR | FIELD-USER-DEFINED-DATA-LENGTH | `CRS-M1-00464` | LNR-FILE-BYTES |
| `FC-LNR-FIELD-USER-DEFINED-DATA` | LNR | FIELD-USER-DEFINED-DATA | `CRS-M1-00465` | LNR-FILE-BYTES |
| `FC-LNS-FIELD-FILE-LENGTH` | LNS | FIELD-FILE-LENGTH | `CRS-M1-00466` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-PROTOCOL-VERSION` | LNS | FIELD-PROTOCOL-VERSION | `CRS-M1-00467` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-DOWNLOAD-OPERATION-STATUS-CODE` | LNS | FIELD-DOWNLOAD-OPERATION-STATUS-CODE | `CRS-M1-00468` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-DOWNLOAD-STATUS-DESCRIPTION-LENGTH` | LNS | FIELD-DOWNLOAD-STATUS-DESCRIPTION-LENGTH | `CRS-M1-00469` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-DOWNLOAD-STATUS-DESCRIPTION` | LNS | FIELD-DOWNLOAD-STATUS-DESCRIPTION | `CRS-M1-00470` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-COUNTER` | LNS | FIELD-COUNTER | `CRS-M1-00471` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-EXCEPTION-TIMER` | LNS | FIELD-EXCEPTION-TIMER | `CRS-M1-00472` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-ESTIMATED-TIME` | LNS | FIELD-ESTIMATED-TIME | `CRS-M1-00473` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-DOWNLOAD-LIST-RATIO` | LNS | FIELD-DOWNLOAD-LIST-RATIO | `CRS-M1-00474` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-NUMBER-OF-FILES` | LNS | FIELD-NUMBER-OF-FILES | `CRS-M1-00475` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-FILE-NAME-LENGTH` | LNS | FIELD-FILE-NAME-LENGTH | `CRS-M1-00476` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-FILE-NAME` | LNS | FIELD-FILE-NAME | `CRS-M1-00477` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-FILE-STATUS` | LNS | FIELD-FILE-STATUS | `CRS-M1-00478` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-FILE-STATUS-DESCRIPTION-LENGTH` | LNS | FIELD-FILE-STATUS-DESCRIPTION-LENGTH | `CRS-M1-00479` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-FILE-STATUS-DESCRIPTION` | LNS | FIELD-FILE-STATUS-DESCRIPTION | `CRS-M1-00480` | LNS-FILE-BYTES |
| `FC-LNL-FIELD-FILE-LENGTH` | LNL | FIELD-FILE-LENGTH | `CRS-M1-00481` | LNL-FILE-BYTES |
| `FC-LNL-FIELD-PROTOCOL-VERSION` | LNL | FIELD-PROTOCOL-VERSION | `CRS-M1-00482` | LNL-FILE-BYTES |
| `FC-LNL-FIELD-NUMBER-OF-FILES` | LNL | FIELD-NUMBER-OF-FILES | `CRS-M1-00483` | LNL-FILE-BYTES |
| `FC-LNL-FIELD-FILE-NAME-LENGTH` | LNL | FIELD-FILE-NAME-LENGTH | `CRS-M1-00484` | LNL-FILE-BYTES |
| `FC-LNL-FIELD-FILE-NAME` | LNL | FIELD-FILE-NAME | `CRS-M1-00485` | LNL-FILE-BYTES |
| `FC-LNL-FIELD-FILE-DESCRIPTION-LENGTH` | LNL | FIELD-FILE-DESCRIPTION-LENGTH | `CRS-M1-00486` | LNL-FILE-BYTES |
| `FC-LNL-FIELD-FILE-DESCRIPTION` | LNL | FIELD-FILE-DESCRIPTION | `CRS-M1-00487` | LNL-FILE-BYTES |
| `FC-LNA-FIELD-FILE-LENGTH` | LNA | FIELD-FILE-LENGTH | `CRS-M1-00488` | LNA-FILE-BYTES |
| `FC-LNA-FIELD-PROTOCOL-VERSION` | LNA | FIELD-PROTOCOL-VERSION | `CRS-M1-00489` | LNA-FILE-BYTES |
| `FC-LNA-FIELD-NUMBER-OF-FILES` | LNA | FIELD-NUMBER-OF-FILES | `CRS-M1-00490` | LNA-FILE-BYTES |
| `FC-LNA-FIELD-FILE-NAME-LENGTH` | LNA | FIELD-FILE-NAME-LENGTH | `CRS-M1-00491` | LNA-FILE-BYTES |
| `FC-LNA-FIELD-FILE-NAME` | LNA | FIELD-FILE-NAME | `CRS-M1-00492` | LNA-FILE-BYTES |
| `FC-LUB-FIELD-BATCH-FILE-LENGTH` | LUB | FIELD-BATCH-FILE-LENGTH | `CRS-M1-00546` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-BATCH-FILE-FORMAT-VERSION` | LUB | FIELD-BATCH-FILE-FORMAT-VERSION | `CRS-M1-00547` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-SPARE` | LUB | FIELD-SPARE | `CRS-M1-00548` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-POINTER-TO-BATCH-FILE-PN-LENGTH` | LUB | FIELD-POINTER-TO-BATCH-FILE-PN-LENGTH | `CRS-M1-00549` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-POINTER-TO-NUMBER-OF-TARGET-HW-ID-LOAD-LIST-BLOCKS` | LUB | FIELD-POINTER-TO-NUMBER-OF-TARGET-HW-ID-LOAD-LIST-BLOCKS | `CRS-M1-00550` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-EXPANSION-POINT-1` | LUB | FIELD-EXPANSION-POINT-1 | `CRS-M1-00551` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-BATCH-FILE-PN-LENGTH` | LUB | FIELD-BATCH-FILE-PN-LENGTH | `CRS-M1-00552` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-BATCH-FILE-PN` | LUB | FIELD-BATCH-FILE-PN | `CRS-M1-00553` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-COMMENT-LENGTH` | LUB | FIELD-COMMENT-LENGTH | `CRS-M1-00554` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-COMMENT` | LUB | FIELD-COMMENT | `CRS-M1-00555` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-EXPANSION-POINT-2` | LUB | FIELD-EXPANSION-POINT-2 | `CRS-M1-00556` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-NUMBER-OF-TARGET-HW-ID-LOAD-LIST-BLOCKS` | LUB | FIELD-NUMBER-OF-TARGET-HW-ID-LOAD-LIST-BLOCKS | `CRS-M1-00557` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-POINTER-TO-NEXT-TARGET-HW-ID-LOAD-LIST-BLOCK` | LUB | FIELD-POINTER-TO-NEXT-TARGET-HW-ID-LOAD-LIST-BLOCK | `CRS-M1-00558` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-TARGET-HW-ID-POS-LENGTH` | LUB | FIELD-TARGET-HW-ID-POS-LENGTH | `CRS-M1-00559` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-TARGET-HW-ID-POS` | LUB | FIELD-TARGET-HW-ID-POS | `CRS-M1-00560` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-NUMBER-OF-LOADS-FOR-TARGET-HW-ID-POS` | LUB | FIELD-NUMBER-OF-LOADS-FOR-TARGET-HW-ID-POS | `CRS-M1-00561` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-HEADER-FILE-NAME-LENGTH` | LUB | FIELD-HEADER-FILE-NAME-LENGTH | `CRS-M1-00562` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-HEADER-FILE-NAME` | LUB | FIELD-HEADER-FILE-NAME | `CRS-M1-00563` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-LOAD-PN-LENGTH` | LUB | FIELD-LOAD-PN-LENGTH | `CRS-M1-00564` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-LOAD-PN` | LUB | FIELD-LOAD-PN | `CRS-M1-00565` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-EXPANSION-POINT-3` | LUB | FIELD-EXPANSION-POINT-3 | `CRS-M1-00566` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-BATCH-FILE-CRC` | LUB | FIELD-BATCH-FILE-CRC | `CRS-M1-00567` | LUB-FILE-BYTES |

## Status constraints

| ID | CRS | Code | Check |
|---|---|---|---|
| `ST-CRS-M1-00334` | `CRS-M1-00334` | 0X0001 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00335` | `CRS-M1-00335` | 0X1000 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00336` | `CRS-M1-00336` | 0X1002 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00337` | `CRS-M1-00337` | 0X0002 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00338` | `CRS-M1-00338` | 0X0003 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00339` | `CRS-M1-00339` | 0X0004 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00340` | `CRS-M1-00340` | 0X1003 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00341` | `CRS-M1-00341` | 0X1004 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00342` | `CRS-M1-00342` | 0X1005 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00343` | `CRS-M1-00343` | 0X1007 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00344` | `CRS-M1-00344` | 0X1007 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00345` | `CRS-M1-00345` | DISPLAY-FOOTNOTE | STATUS-FILE-AND-DISPLAY |

## Object constraints

| ID | CRS | Action | Check |
|---|---|---|---|
| `OBJ-MINIMUM-ARINC-665-COMPATIBILITY-CAPABILITIES-IMPLEMENT-REQUIRED-ARINC-665-CA-CRS-M1-00191` | `CRS-M1-00191` | IMPLEMENT-REQUIRED-ARINC-665-CAPABILITIES | ARINC-665-DATA-OBJECT |
| `OBJ-ARINC-665-SHOULD-MODALITY-TREAT-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY-CRS-M1-00192` | `CRS-M1-00192` | TREAT-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY | ARINC-665-DATA-OBJECT |
| `OBJ-ARINC-665-MAY-MODALITY-TREAT-MAY-AS-OPTIONAL-CAPABILITY-CRS-M1-00193` | `CRS-M1-00193` | TREAT-MAY-AS-OPTIONAL-CAPABILITY | ARINC-665-DATA-OBJECT |
| `OBJ-OPTIONAL-ARINC-665-CAPABILITY-CONDITIONALLY-IMPLEMENT-OPTIONAL-CAPABILITY-AS-CRS-M1-00194` | `CRS-M1-00194` | CONDITIONALLY-IMPLEMENT-OPTIONAL-CAPABILITY-AS-SPECIFIED | ARINC-665-DATA-OBJECT |
| `OBJ-DATA-FIELD-TYPE-INTERPRET-FIELDS-AS-NUMERIC-BY-DEFAULT-CRS-M1-00195` | `CRS-M1-00195` | INTERPRET-FIELDS-AS-NUMERIC-BY-DEFAULT | ARINC-665-DATA-OBJECT |
| `OBJ-ARINC-665-FILE-PROHIBIT-UNDEFINED-FIELD-INSERTION-CRS-M1-00196` | `CRS-M1-00196` | PROHIBIT-UNDEFINED-FIELD-INSERTION | ARINC-665-DATA-OBJECT |
| `OBJ-FILE-VERSION-COMPATIBILITY-ENCODE-CRS-M1-00197` | `CRS-M1-00197` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-TARGET-HARDWARE-ID-MANUFACTURER-IDENTIFIER-PREFIX-TARGET-HARDWARE-ID-WITH-MA-CRS-M1-00198` | `CRS-M1-00198` | PREFIX-TARGET-HARDWARE-ID-WITH-MANUFACTURER-CODE | ARINC-665-DATA-OBJECT |
| `OBJ-MANUFACTURER-IDENTIFIER-ASSIGN-CRS-M1-00199` | `CRS-M1-00199` | ASSIGN | ARINC-665-DATA-OBJECT |
| `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ASSIGN-GENERIC-TARGET-HARDWARE-ID-CRS-M1-00200` | `CRS-M1-00200` | ASSIGN-GENERIC-TARGET-HARDWARE-ID | ARINC-665-DATA-OBJECT |
| `OBJ-REDUNDANT-CHANNEL-LOADS-DISTRIBUTE-REDUNDANT-LOADS-INTERNALLY-CRS-M1-00201` | `CRS-M1-00201` | DISTRIBUTE-REDUNDANT-LOADS-INTERNALLY | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-ENSURE-CARDINALITY-CRS-M1-00202` | `CRS-M1-00202` | ENSURE-CARDINALITY | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-COORDINATE-CRS-M1-00203` | `CRS-M1-00203` | COORDINATE | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-ASSIGN-CRS-M1-00204` | `CRS-M1-00204` | ASSIGN | ARINC-665-DATA-OBJECT |
| `OBJ-LOADABLE-SOFTWARE-PART-NUMBER-FORMAT-CRS-M1-00205` | `CRS-M1-00205` | FORMAT | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-EXCLUDE-EMBEDDED-BLANKS-CRS-M1-00206` | `CRS-M1-00206` | EXCLUDE-EMBEDDED-BLANKS | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-DO-NOT-ENFORCE-SPECIFIC-PART-NUMBER-FORMAT-CRS-M1-00207` | `CRS-M1-00207` | DO-NOT-ENFORCE-SPECIFIC-PART-NUMBER-FORMAT | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-PROCESS-NONCONFORMING-PART-NUMBER-FORMATS-CRS-M1-00208` | `CRS-M1-00208` | PROCESS-NONCONFORMING-PART-NUMBER-FORMATS | ARINC-665-DATA-OBJECT |
| `OBJ-NETWORK-INTERFACE-DESIGN-CRS-M1-00209` | `CRS-M1-00209` | DESIGN | ARINC-665-DATA-OBJECT |
| `OBJ-NETWORK-INTERFACE-FORMAT-CRS-M1-00210` | `CRS-M1-00210` | FORMAT | ARINC-665-DATA-OBJECT |
| `OBJ-ATA-PART-NUMBER-DELIMITERS-SEPARATE-DELIMITERS-FROM-LETTERS-CRS-M1-00211` | `CRS-M1-00211` | SEPARATE-DELIMITERS-FROM-LETTERS | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-ENCODE-CRS-M1-00212` | `CRS-M1-00212` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-ATA-PART-NUMBER-CHARACTER-SET-EXCLUDE-AMBIGUOUS-LETTER-O-CRS-M1-00213` | `CRS-M1-00213` | EXCLUDE-AMBIGUOUS-LETTER-O | ARINC-665-DATA-OBJECT |
| `OBJ-MMM-CODE-INTERPRET-CONFUSED-MMM-CHARACTERS-AS-ALPHABETIC-CRS-M1-00214` | `CRS-M1-00214` | INTERPRET-CONFUSED-MMM-CHARACTERS-AS-ALPHABETIC | ARINC-665-DATA-OBJECT |
| `OBJ-CHECK-CHARACTERS-COMPUTE-CRS-M1-00215` | `CRS-M1-00215` | COMPUTE | ARINC-665-DATA-OBJECT |
| `OBJ-HEADER-FILE-SOFTWARE-PART-FORMAT-CRS-M1-00216` | `CRS-M1-00216` | FORMAT | ARINC-665-DATA-OBJECT |
| `OBJ-HEADER-FILE-SOFTWARE-PART-ENCODE-CRS-M1-00217` | `CRS-M1-00217` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-HEADER-FILE-DEFINE-CRS-M1-00218` | `CRS-M1-00218` | DEFINE | ARINC-665-DATA-OBJECT |
| `OBJ-BINARY-FIELD-ENCODING-ENCODE-CRS-M1-00219` | `CRS-M1-00219` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-OPERATION-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00220` | `CRS-M1-00220` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-BINARY-FIELD-ENCODING-ENCODE-CRS-M1-00221` | `CRS-M1-00221` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-TARGET-HARDWARE-ID-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00222` | `CRS-M1-00222` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-IMPLEMENT-CRS-M1-00223` | `CRS-M1-00223` | IMPLEMENT | ARINC-665-DATA-OBJECT |
| `OBJ-NETWORK-INTERFACE-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00224` | `CRS-M1-00224` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ENSURE-UNIQUE-CRS-M1-00225` | `CRS-M1-00225` | ENSURE-UNIQUE | ARINC-665-DATA-OBJECT |
| `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ENCODE-CRS-M1-00226` | `CRS-M1-00226` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-TARGET-HARDWARE-ID-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00227` | `CRS-M1-00227` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-DATA-FILE-CONSTRAIN-CRS-M1-00228` | `CRS-M1-00228` | CONSTRAIN | ARINC-665-DATA-OBJECT |
| `OBJ-DATA-FILE-SET-ZERO-CRS-M1-00229` | `CRS-M1-00229` | SET-ZERO | ARINC-665-DATA-OBJECT |
| `OBJ-DATA-FILE-FORMAT-CRS-M1-00230` | `CRS-M1-00230` | FORMAT | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-NETWORK-INTERFACE-DEFINE-CRS-M1-00231` | `CRS-M1-00231` | DEFINE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00232` | `CRS-M1-00232` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00233` | `CRS-M1-00233` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00234` | `CRS-M1-00234` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-NETWORK-INTERFACE-ENCODE-CRS-M1-00235` | `CRS-M1-00235` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-NETWORK-INTERFACE-IMPLEMENT-CRS-M1-00236` | `CRS-M1-00236` | IMPLEMENT | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-NETWORK-INTERFACE-ENCODE-CRS-M1-00237` | `CRS-M1-00237` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-NETWORK-INTERFACE-DEFINE-CRS-M1-00238` | `CRS-M1-00238` | DEFINE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00239` | `CRS-M1-00239` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-NETWORK-INTERFACE-VALIDATE-CRS-M1-00240` | `CRS-M1-00240` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-HEADER-FILE-VALIDATE-CRS-M1-00241` | `CRS-M1-00241` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00242` | `CRS-M1-00242` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00243` | `CRS-M1-00243` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00244` | `CRS-M1-00244` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00245` | `CRS-M1-00245` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00246` | `CRS-M1-00246` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00247` | `CRS-M1-00247` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-HEADER-FILE-CRC-DEFINE-CRS-M1-00248` | `CRS-M1-00248` | DEFINE | ARINC-665-DATA-OBJECT |
| `OBJ-HEADER-FILE-CRC-COMPUTE-CRS-M1-00249` | `CRS-M1-00249` | COMPUTE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-NETWORK-INTERFACE-DEFINE-CRS-M1-00250` | `CRS-M1-00250` | DEFINE | ARINC-665-DATA-OBJECT |
| `OBJ-DATA-FILE-SOFTWARE-PART-ENCODE-CRS-M1-00251` | `CRS-M1-00251` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-SOFTWARE-PART-NETWORK-INTERFACE-ENCODE-CRS-M1-00252` | `CRS-M1-00252` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-MAY-USE-BATCH-FILE-FORMAT-CRS-M1-00526` | `CRS-M1-00526` | MAY-USE-BATCH-FILE-FORMAT | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-LET-BATCH-FILE-SELECT-LSPS-PER-TARGET-HW-POSITION-CRS-M1-00527` | `CRS-M1-00527` | LET-BATCH-FILE-SELECT-LSPS-PER-TARGET-HW-POSITION | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-IDENTIFY-BATCH-FILE-WITH-LUB-EXTENSION-CRS-M1-00528` | `CRS-M1-00528` | IDENTIFY-BATCH-FILE-WITH-LUB-EXTENSION | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-MATCH-REFERENCED-HEADER-FILE-NAME-CASE-CRS-M1-00529` | `CRS-M1-00529` | MATCH-REFERENCED-HEADER-FILE-NAME-CASE | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-PREFIX-BATCH-FILE-NAME-WITH-MANUFACTURER-CODE-CRS-M1-00530` | `CRS-M1-00530` | PREFIX-BATCH-FILE-NAME-WITH-MANUFACTURER-CODE | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-KEEP-BATCH-FILE-NAME-UNIQUE-PER-MANUFACTURER-CODE-CRS-M1-00531` | `CRS-M1-00531` | KEEP-BATCH-FILE-NAME-UNIQUE-PER-MANUFACTURER-CODE | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-KEEP-BATCH-FILE-PART-NUMBER-UNIQUE-AMONG-LSP-AND-BFP-CRS-M1-00532` | `CRS-M1-00532` | KEEP-BATCH-FILE-PART-NUMBER-UNIQUE-AMONG-LSP-AND-BFP | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-REFERENCE-COMPLETE-HEADER-FILE-NAME-WITHOUT-PATH-CRS-M1-00533` | `CRS-M1-00533` | REFERENCE-COMPLETE-HEADER-FILE-NAME-WITHOUT-PATH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-USE-BATCH-FILE-ONLY-TO-AUTOMATE-MULTI-LSP-SETUP-CRS-M1-00534` | `CRS-M1-00534` | USE-BATCH-FILE-ONLY-TO-AUTOMATE-MULTI-LSP-SETUP | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-DO-NOT-TRANSFER-BATCH-FILE-TO-TARGET-HARDWARE-CRS-M1-00535` | `CRS-M1-00535` | DO-NOT-TRANSFER-BATCH-FILE-TO-TARGET-HARDWARE | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-INCLUDE-BATCH-FILE-CONTENT-DEFINED-BY-TABLE-2-3-1-1-CRS-M1-00536` | `CRS-M1-00536` | INCLUDE-BATCH-FILE-CONTENT-DEFINED-BY-TABLE-2-3-1-1 | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ENCODE-BATCH-FILE-LENGTH-IN-16-BIT-WORDS-CRS-M1-00537` | `CRS-M1-00537` | ENCODE-BATCH-FILE-LENGTH-IN-16-BIT-WORDS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-MAKE-BATCH-FILE-PN-COMPLIANT-WITH-SOFTWARE-LOAD-PN-FORMAT-CRS-M1-00538` | `CRS-M1-00538` | MAKE-BATCH-FILE-PN-COMPLIANT-WITH-SOFTWARE-LOAD-PN-FORMAT | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-KEEP-BATCH-FILE-PN-DISTINCT-FROM-LSP-AND-MSP-CRS-M1-00539` | `CRS-M1-00539` | KEEP-BATCH-FILE-PN-DISTINCT-FROM-LSP-AND-MSP | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-SET-LAST-LOAD-LIST-BLOCK-POINTER-TO-ZERO-CRS-M1-00540` | `CRS-M1-00540` | SET-LAST-LOAD-LIST-BLOCK-POINTER-TO-ZERO | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-MATCH-TARGET-HW-ID-POS-TO-TARGET-HARDWARE-CRS-M1-00541` | `CRS-M1-00541` | MATCH-TARGET-HW-ID-POS-TO-TARGET-HARDWARE | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-MATCH-HEADER-FILE-NAME-TO-LISTED-LSP-CRS-M1-00542` | `CRS-M1-00542` | MATCH-HEADER-FILE-NAME-TO-LISTED-LSP | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-MATCH-LOAD-PN-TO-LSP-FOR-TARGET-HW-ID-POS-CRS-M1-00543` | `CRS-M1-00543` | MATCH-LOAD-PN-TO-LSP-FOR-TARGET-HW-ID-POS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-DEFINE-BATCH-FILE-FORMAT-VERSION-IN-16-BITS-CRS-M1-00568` | `CRS-M1-00568` | DEFINE-BATCH-FILE-FORMAT-VERSION-IN-16-BITS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-TAKE-BATCH-FILE-FORMAT-VERSION-FROM-CLAUSE-1-4-1-CRS-M1-00569` | `CRS-M1-00569` | TAKE-BATCH-FILE-FORMAT-VERSION-FROM-CLAUSE-1-4-1 | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-USE-SPARE-TO-ALIGN-FOLLOWING-POINTERS-ON-4-BYTE-BOUNDARIES-CRS-M1-00570` | `CRS-M1-00570` | USE-SPARE-TO-ALIGN-FOLLOWING-POINTERS-ON-4-BYTE-BOUNDARIES | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-POINT-TO-BATCH-FILE-PN-LENGTH-FROM-START-IN-16-BIT-WORDS-CRS-M1-00571` | `CRS-M1-00571` | POINT-TO-BATCH-FILE-PN-LENGTH-FROM-START-IN-16-BIT-WORDS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-POINT-TO-LOAD-LIST-BLOCK-COUNT-FROM-START-IN-16-BIT-WORDS-CRS-M1-00572` | `CRS-M1-00572` | POINT-TO-LOAD-LIST-BLOCK-COUNT-FROM-START-IN-16-BIT-WORDS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-MAY-GROW-FILE-FORMAT-AT-EXPANSION-POINTS-CRS-M1-00573` | `CRS-M1-00573` | MAY-GROW-FILE-FORMAT-AT-EXPANSION-POINTS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-BATCH-FILE-PN-LENGTH-CRS-M1-00574` | `CRS-M1-00574` | EXCLUDE-NUL-PAD-FROM-BATCH-FILE-PN-LENGTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ENCODE-BATCH-FILE-PN-AS-8-BIT-ASCII-CRS-M1-00575` | `CRS-M1-00575` | ENCODE-BATCH-FILE-PN-AS-8-BIT-ASCII | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ALLOCATE-BATCH-FILE-PN-EVEN-OCTET-WIDTH-CRS-M1-00576` | `CRS-M1-00576` | ALLOCATE-BATCH-FILE-PN-EVEN-OCTET-WIDTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-PAD-ODD-BATCH-FILE-PN-WITH-NUL-CRS-M1-00577` | `CRS-M1-00577` | PAD-ODD-BATCH-FILE-PN-WITH-NUL | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-COMMENT-LENGTH-CRS-M1-00578` | `CRS-M1-00578` | EXCLUDE-NUL-PAD-FROM-COMMENT-LENGTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-SET-COMMENT-LENGTH-ZERO-WHEN-NO-COMMENT-CRS-M1-00579` | `CRS-M1-00579` | SET-COMMENT-LENGTH-ZERO-WHEN-NO-COMMENT | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ENCODE-COMMENT-AS-8-BIT-ASCII-CRS-M1-00580` | `CRS-M1-00580` | ENCODE-COMMENT-AS-8-BIT-ASCII | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ALLOCATE-COMMENT-EVEN-OCTET-WIDTH-CRS-M1-00581` | `CRS-M1-00581` | ALLOCATE-COMMENT-EVEN-OCTET-WIDTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-PAD-ODD-COMMENT-WITH-NUL-CRS-M1-00582` | `CRS-M1-00582` | PAD-ODD-COMMENT-WITH-NUL | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-OMIT-COMMENT-FIELD-WHEN-COMMENT-LENGTH-ZERO-CRS-M1-00583` | `CRS-M1-00583` | OMIT-COMMENT-FIELD-WHEN-COMMENT-LENGTH-ZERO | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-COUNT-TARGET-HW-ID-LOAD-LIST-BLOCKS-IN-BATCH-FILE-CRS-M1-00584` | `CRS-M1-00584` | COUNT-TARGET-HW-ID-LOAD-LIST-BLOCKS-IN-BATCH-FILE | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-POINT-TO-NEXT-LOAD-LIST-BLOCK-IN-RELATIVE-16-BIT-WORDS-CRS-M1-00585` | `CRS-M1-00585` | POINT-TO-NEXT-LOAD-LIST-BLOCK-IN-RELATIVE-16-BIT-WORDS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-TARGET-HW-ID-POS-LENGTH-CRS-M1-00586` | `CRS-M1-00586` | EXCLUDE-NUL-PAD-FROM-TARGET-HW-ID-POS-LENGTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ENCODE-TARGET-HW-ID-POS-AS-8-BIT-ASCII-CRS-M1-00587` | `CRS-M1-00587` | ENCODE-TARGET-HW-ID-POS-AS-8-BIT-ASCII | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ALLOCATE-TARGET-HW-ID-POS-EVEN-OCTET-WIDTH-CRS-M1-00588` | `CRS-M1-00588` | ALLOCATE-TARGET-HW-ID-POS-EVEN-OCTET-WIDTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-PAD-ODD-TARGET-HW-ID-POS-WITH-NUL-CRS-M1-00589` | `CRS-M1-00589` | PAD-ODD-TARGET-HW-ID-POS-WITH-NUL | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-KEEP-TARGET-HW-ID-POS-CONSISTENT-WITH-LISTED-LSP-HEADERS-CRS-M1-00590` | `CRS-M1-00590` | KEEP-TARGET-HW-ID-POS-CONSISTENT-WITH-LISTED-LSP-HEADERS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-COUNT-LOADS-IN-THE-TARGET-HW-ID-LOAD-LIST-BLOCK-CRS-M1-00591` | `CRS-M1-00591` | COUNT-LOADS-IN-THE-TARGET-HW-ID-LOAD-LIST-BLOCK | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-HEADER-FILE-NAME-LENGTH-CRS-M1-00592` | `CRS-M1-00592` | EXCLUDE-NUL-PAD-FROM-HEADER-FILE-NAME-LENGTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ENCODE-HEADER-FILE-NAME-AS-8-BIT-ASCII-CRS-M1-00593` | `CRS-M1-00593` | ENCODE-HEADER-FILE-NAME-AS-8-BIT-ASCII | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ALLOCATE-HEADER-FILE-NAME-EVEN-OCTET-WIDTH-CRS-M1-00594` | `CRS-M1-00594` | ALLOCATE-HEADER-FILE-NAME-EVEN-OCTET-WIDTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-PAD-ODD-HEADER-FILE-NAME-WITH-NUL-CRS-M1-00595` | `CRS-M1-00595` | PAD-ODD-HEADER-FILE-NAME-WITH-NUL | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-USE-HEADER-FILE-NAME-WITHOUT-PATH-CRS-M1-00596` | `CRS-M1-00596` | USE-HEADER-FILE-NAME-WITHOUT-PATH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-KEEP-HEADER-FILE-NAME-FREE-OF-BACKSLASH-CRS-M1-00597` | `CRS-M1-00597` | KEEP-HEADER-FILE-NAME-FREE-OF-BACKSLASH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-INCLUDE-HEADER-FILE-NAME-EXTENSIONS-AND-DELIMITERS-CRS-M1-00598` | `CRS-M1-00598` | INCLUDE-HEADER-FILE-NAME-EXTENSIONS-AND-DELIMITERS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-DEFINE-LOAD-PN-LENGTH-AS-CHARACTER-COUNT-CRS-M1-00599` | `CRS-M1-00599` | DEFINE-LOAD-PN-LENGTH-AS-CHARACTER-COUNT | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-LOAD-PN-LENGTH-CRS-M1-00600` | `CRS-M1-00600` | EXCLUDE-NUL-PAD-FROM-LOAD-PN-LENGTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ENCODE-LOAD-PN-AS-8-BIT-ASCII-CRS-M1-00601` | `CRS-M1-00601` | ENCODE-LOAD-PN-AS-8-BIT-ASCII | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ALLOCATE-LOAD-PN-EVEN-OCTET-WIDTH-CRS-M1-00602` | `CRS-M1-00602` | ALLOCATE-LOAD-PN-EVEN-OCTET-WIDTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-PAD-ODD-LOAD-PN-WITH-NUL-CRS-M1-00603` | `CRS-M1-00603` | PAD-ODD-LOAD-PN-WITH-NUL | ARINC-665-DATA-OBJECT |
| `OBJ-SUPPORTING-GIVE-664P3-PRECEDENCE-OVER-CONFLICTING-RFC-OPTIONS-CRS-M1-00604` | `CRS-M1-00604` | GIVE-664P3-PRECEDENCE-OVER-CONFLICTING-RFC-OPTIONS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-GENERATE-AND-CHECK-UDP-CHECKSUM-CRS-M1-00605` | `CRS-M1-00605` | GENERATE-AND-CHECK-UDP-CHECKSUM | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-IMPLEMENT-IPV4-IN-ACCORDANCE-WITH-P3-FIGURE-3-4-1-1-CRS-M1-00606` | `CRS-M1-00606` | IMPLEMENT-IPV4-IN-ACCORDANCE-WITH-P3-FIGURE-3-4-1-1 | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-FILTER-AND-POLICE-FRAMES-FOR-INTEGRITY-LENGTH-BUDGET-AND-DESTINATION-CRS-M1-00608` | `CRS-M1-00608` | FILTER-AND-POLICE-FRAMES-FOR-INTEGRITY-LENGTH-BUDGET-AND-DESTINATION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-AFDX-NOT-APPLICABLE-PROFILE-ITEMS-AS-MUST-NOT-CRS-M1-00609` | `CRS-M1-00609` | TREAT-AFDX-NOT-APPLICABLE-PROFILE-ITEMS-AS-MUST-NOT | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-UDP-LENGTH-TO-HEADER-PLUS-DATA-OCTETS-CRS-M1-00610` | `CRS-M1-00610` | SET-UDP-LENGTH-TO-HEADER-PLUS-DATA-OCTETS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-COMPUTE-UDP-CHECKSUM-OVER-PSEUDO-HEADER-HEADER-AND-DATA-CRS-M1-00611` | `CRS-M1-00611` | COMPUTE-UDP-CHECKSUM-OVER-PSEUDO-HEADER-HEADER-AND-DATA | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-UDP-LENGTH-AT-LEAST-EIGHT-OCTETS-CRS-M1-00628` | `CRS-M1-00628` | KEEP-UDP-LENGTH-AT-LEAST-EIGHT-OCTETS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-IMPLEMENT-IPV4-FRAGMENTATION-AND-REASSEMBLY-CRS-M1-00613` | `CRS-M1-00613` | IMPLEMENT-IPV4-FRAGMENTATION-AND-REASSEMBLY | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-SILENTLY-DISCARD-NON-IPV4-VERSION-CRS-M1-00614` | `CRS-M1-00614` | SILENTLY-DISCARD-NON-IPV4-VERSION | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-VERIFY-IP-HEADER-CHECKSUM-AND-SILENTLY-DISCARD-BAD-CRS-M1-00629` | `CRS-M1-00629` | VERIFY-IP-HEADER-CHECKSUM-AND-SILENTLY-DISCARD-BAD | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-SUPPORT-IPV4-REASSEMBLY-CRS-M1-00630` | `CRS-M1-00630` | SUPPORT-IPV4-REASSEMBLY | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-GENERATE-AND-VALIDATE-UDP-CHECKSUMS-CRS-M1-00615` | `CRS-M1-00615` | GENERATE-AND-VALIDATE-UDP-CHECKSUMS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-SILENTLY-DISCARD-UDP-DATAGRAM-WITH-INVALID-CHECKSUM-CRS-M1-00631` | `CRS-M1-00631` | SILENTLY-DISCARD-UDP-DATAGRAM-WITH-INVALID-CHECKSUM | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-USE-FIVE-TFTP-PACKET-TYPES-IDENTIFIED-BY-OPCODE-CRS-M1-00617` | `CRS-M1-00617` | USE-FIVE-TFTP-PACKET-TYPES-IDENTIFIED-BY-OPCODE | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ASSIGN-TID-ON-RRQ-OR-WRQ-WITHOUT-MAIL-MODE-CRS-M1-00618` | `CRS-M1-00618` | ASSIGN-TID-ON-RRQ-OR-WRQ-WITHOUT-MAIL-MODE | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-PLACE-OPCODE-IN-TFTP-HEADER-CRS-M1-00619` | `CRS-M1-00619` | PLACE-OPCODE-IN-TFTP-HEADER | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-RRQ-WRQ-AS-OPCODE-FILENAME-AND-MODE-CRS-M1-00632` | `CRS-M1-00632` | ENCODE-RRQ-WRQ-AS-OPCODE-FILENAME-AND-MODE | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-TERMINATE-TFTP-FILENAME-WITH-NUL-CRS-M1-00633` | `CRS-M1-00633` | TERMINATE-TFTP-FILENAME-WITH-NUL | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-DATA-PACKET-WITH-BLOCK-NUMBER-AND-DATA-CRS-M1-00634` | `CRS-M1-00634` | ENCODE-DATA-PACKET-WITH-BLOCK-NUMBER-AND-DATA | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-LIMIT-TFTP-DATA-FIELD-TO-ZERO-THROUGH-512-BYTES-CRS-M1-00635` | `CRS-M1-00635` | LIMIT-TFTP-DATA-FIELD-TO-ZERO-THROUGH-512-BYTES | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-ACK-PACKET-WITH-OPCODE-4-AND-BLOCK-NUMBER-CRS-M1-00636` | `CRS-M1-00636` | ENCODE-ACK-PACKET-WITH-OPCODE-4-AND-BLOCK-NUMBER | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-ERROR-PACKET-AS-OPCODE-ERROR-CODE-AND-MESSAGE-CRS-M1-00637` | `CRS-M1-00637` | ENCODE-ERROR-PACKET-AS-OPCODE-ERROR-CODE-AND-MESSAGE | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-TERMINATE-ON-DATA-PACKET-OF-0-TO-511-BYTES-CRS-M1-00620` | `CRS-M1-00620` | TERMINATE-ON-DATA-PACKET-OF-0-TO-511-BYTES | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-SEND-ERROR-PACKET-OPCODE-5-CRS-M1-00621` | `CRS-M1-00621` | SEND-ERROR-PACKET-OPCODE-5 | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ACKNOWLEDGE-OPTION-NEGOTIATION-WITH-OACK-CRS-M1-00622` | `CRS-M1-00622` | ACKNOWLEDGE-OPTION-NEGOTIATION-WITH-OACK | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-TERMINATE-TRANSFER-WITH-ERROR-CODE-8-CRS-M1-00623` | `CRS-M1-00623` | TERMINATE-TRANSFER-WITH-ERROR-CODE-8 | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-APPEND-OPTIONS-TO-RRQ-OR-WRQ-CRS-M1-00624` | `CRS-M1-00624` | APPEND-OPTIONS-TO-RRQ-OR-WRQ | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-BLKSIZE-AS-ASCII-OCTETS-FROM-8-THROUGH-65464-CRS-M1-00625` | `CRS-M1-00625` | ENCODE-BLKSIZE-AS-ASCII-OCTETS-FROM-8-THROUGH-65464 | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-BLKSIZE-VALUE-IN-ASCII-CRS-M1-00638` | `CRS-M1-00638` | ENCODE-BLKSIZE-VALUE-IN-ASCII | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-NEGOTIATE-BLKSIZE-LESS-OR-EQUAL-TO-CLIENT-VALUE-CRS-M1-00639` | `CRS-M1-00639` | NEGOTIATE-BLKSIZE-LESS-OR-EQUAL-TO-CLIENT-VALUE | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-USE-OACK-BLKSIZE-OR-TERMINATE-WITH-ERROR-8-CRS-M1-00640` | `CRS-M1-00640` | USE-OACK-BLKSIZE-OR-TERMINATE-WITH-ERROR-8 | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-TIMEOUT-AS-ASCII-SECONDS-FROM-1-THROUGH-255-CRS-M1-00626` | `CRS-M1-00626` | ENCODE-TIMEOUT-AS-ASCII-SECONDS-FROM-1-THROUGH-255 | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ECHO-CLIENT-TIMEOUT-VALUE-IN-OACK-CRS-M1-00641` | `CRS-M1-00641` | ECHO-CLIENT-TIMEOUT-VALUE-IN-OACK | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-REQUEST-TSIZE-ZERO-ON-RRQ-AND-RETURN-SIZE-IN-OACK-CRS-M1-00627` | `CRS-M1-00627` | REQUEST-TSIZE-ZERO-ON-RRQ-AND-RETURN-SIZE-IN-OACK | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-SPECIFY-TSIZE-ON-WRQ-AND-ECHO-IN-OACK-CRS-M1-00642` | `CRS-M1-00642` | SPECIFY-TSIZE-ON-WRQ-AND-ECHO-IN-OACK | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-MAY-ABORT-RRQ-WITH-ERROR-CODE-3-CRS-M1-00643` | `CRS-M1-00643` | MAY-ABORT-RRQ-WITH-ERROR-CODE-3 | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-MAY-ABORT-WRQ-WITH-ERROR-CODE-3-CRS-M1-00644` | `CRS-M1-00644` | MAY-ABORT-WRQ-WITH-ERROR-CODE-3 | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-TERMINATE-ON-DATA-SHORTER-THAN-NEGOTIATED-BLKSIZE-CRS-M1-00645` | `CRS-M1-00645` | TERMINATE-ON-DATA-SHORTER-THAN-NEGOTIATED-BLKSIZE | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-SEND-ZERO-LENGTH-FINAL-DATA-WHEN-FILE-IS-INTEGRAL-MULTIPLE-OF-BLKSIZE-CRS-M1-00646` | `CRS-M1-00646` | SEND-ZERO-LENGTH-FINAL-DATA-WHEN-FILE-IS-INTEGRAL-MULTIPLE-OF-BLKSIZE | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-IGNORE-UNACKNOWLEDGED-OPTION-AND-KEEP-DEFAULT-PARAMETERS-CRS-M1-00647` | `CRS-M1-00647` | IGNORE-UNACKNOWLEDGED-OPTION-AND-KEEP-DEFAULT-PARAMETERS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-VERSION-AS-4-BITS-CRS-M1-00648` | `CRS-M1-00648` | ENCODE-VERSION-AS-4-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-IHL-AS-4-BITS-CRS-M1-00649` | `CRS-M1-00649` | ENCODE-IHL-AS-4-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-TOS-AS-8-BITS-CRS-M1-00650` | `CRS-M1-00650` | ENCODE-TOS-AS-8-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-TOTAL-LENGTH-AS-16-BITS-CRS-M1-00651` | `CRS-M1-00651` | ENCODE-TOTAL-LENGTH-AS-16-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-IDENTIFICATION-AS-16-BITS-CRS-M1-00652` | `CRS-M1-00652` | ENCODE-IDENTIFICATION-AS-16-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-FLAGS-AS-3-BITS-CRS-M1-00653` | `CRS-M1-00653` | ENCODE-FLAGS-AS-3-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-FRAGMENT-OFFSET-AS-13-BITS-CRS-M1-00654` | `CRS-M1-00654` | ENCODE-FRAGMENT-OFFSET-AS-13-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-TTL-AS-8-BITS-CRS-M1-00655` | `CRS-M1-00655` | ENCODE-TTL-AS-8-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-PROTOCOL-AS-8-BITS-CRS-M1-00656` | `CRS-M1-00656` | ENCODE-PROTOCOL-AS-8-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-HEADER-CHECKSUM-AS-16-BITS-CRS-M1-00657` | `CRS-M1-00657` | ENCODE-HEADER-CHECKSUM-AS-16-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-SOURCE-ADDRESS-AS-32-BITS-CRS-M1-00658` | `CRS-M1-00658` | ENCODE-SOURCE-ADDRESS-AS-32-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-DESTINATION-ADDRESS-AS-32-BITS-CRS-M1-00659` | `CRS-M1-00659` | ENCODE-DESTINATION-ADDRESS-AS-32-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-DO-NOT-SUPPORT-TFTP-MAIL-TRANSFER-MODE-CRS-M1-00660` | `CRS-M1-00660` | DO-NOT-SUPPORT-TFTP-MAIL-TRANSFER-MODE | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-COUNT-UDP-LENGTH-INCLUDING-EIGHT-OCTET-HEADER-CRS-M1-00661` | `CRS-M1-00661` | COUNT-UDP-LENGTH-INCLUDING-EIGHT-OCTET-HEADER | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-NEVER-RESEND-CURRENT-DATA-ON-DUPLICATE-ACK-CRS-M1-00662` | `CRS-M1-00662` | NEVER-RESEND-CURRENT-DATA-ON-DUPLICATE-ACK | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-USE-ADAPTIVE-TFTP-RETRANSMISSION-TIMEOUT-CRS-M1-00663` | `CRS-M1-00663` | USE-ADAPTIVE-TFTP-RETRANSMISSION-TIMEOUT | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-PROVIDE-CONFIGURABLE-TFTP-PATHNAME-ACCESS-CONTROL-CRS-M1-00664` | `CRS-M1-00664` | PROVIDE-CONFIGURABLE-TFTP-PATHNAME-ACCESS-CONTROL | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-SILENTLY-IGNORE-BROADCAST-TFTP-REQUEST-CRS-M1-00665` | `CRS-M1-00665` | SILENTLY-IGNORE-BROADCAST-TFTP-REQUEST | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ALLOW-ONLY-ONE-SOURCE-END-SYSTEM-PER-VL-CRS-M1-00666` | `CRS-M1-00666` | ALLOW-ONLY-ONE-SOURCE-END-SYSTEM-PER-VL | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-VL-AS-UNIDIRECTIONAL-ONE-TO-MANY-CONNECTION-CRS-M1-00667` | `CRS-M1-00667` | TREAT-VL-AS-UNIDIRECTIONAL-ONE-TO-MANY-CONNECTION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-BAG-AS-MINIMUM-INTERVAL-BETWEEN-CONSECUTIVE-VL-FRAMES-CRS-M1-00668` | `CRS-M1-00668` | TREAT-BAG-AS-MINIMUM-INTERVAL-BETWEEN-CONSECUTIVE-VL-FRAMES | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-BOUND-VL-FRAME-ARRIVAL-BY-MAXIMUM-ADMISSIBLE-JITTER-CRS-M1-00669` | `CRS-M1-00669` | BOUND-VL-FRAME-ARRIVAL-BY-MAXIMUM-ADMISSIBLE-JITTER | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-CHARACTERISE-VL-BANDWIDTH-BY-BAG-AND-LMAX-CRS-M1-00670` | `CRS-M1-00670` | CHARACTERISE-VL-BANDWIDTH-BY-BAG-AND-LMAX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ACCOMMODATE-VL-FRAMES-UP-TO-1518-BYTES-CRS-M1-00671` | `CRS-M1-00671` | ACCOMMODATE-VL-FRAMES-UP-TO-1518-BYTES | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-HANDLE-BAG-VALUES-FROM-1-MS-TO-128-MS-CRS-M1-00672` | `CRS-M1-00672` | HANDLE-BAG-VALUES-FROM-1-MS-TO-128-MS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RESTRICT-BAG-TO-POWERS-OF-TWO-MILLISECONDS-CRS-M1-00673` | `CRS-M1-00673` | RESTRICT-BAG-TO-POWERS-OF-TWO-MILLISECONDS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-IDENTIFY-VL-ONLY-BY-MAC-DESTINATION-ADDRESS-CRS-M1-00675` | `CRS-M1-00675` | IDENTIFY-VL-ONLY-BY-MAC-DESTINATION-ADDRESS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-MEASURE-IHL-IN-32-BIT-WORDS-CRS-M1-00676` | `CRS-M1-00676` | MEASURE-IHL-IN-32-BIT-WORDS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-IHL-AT-LEAST-5-CRS-M1-00677` | `CRS-M1-00677` | KEEP-IHL-AT-LEAST-5 | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-MEASURE-IPV4-TOTAL-LENGTH-IN-OCTETS-INCLUDING-HEADER-AND-DATA-CRS-M1-00678` | `CRS-M1-00678` | MEASURE-IPV4-TOTAL-LENGTH-IN-OCTETS-INCLUDING-HEADER-AND-DATA | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-MEASURE-FRAGMENT-OFFSET-IN-8-OCTET-UNITS-CRS-M1-00679` | `CRS-M1-00679` | MEASURE-FRAGMENT-OFFSET-IN-8-OCTET-UNITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ALLOW-IPV4-OPTIONS-TO-BE-PRESENT-OR-ABSENT-CRS-M1-00680` | `CRS-M1-00680` | ALLOW-IPV4-OPTIONS-TO-BE-PRESENT-OR-ABSENT | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-PAD-IPV4-HEADER-TO-32-BIT-BOUNDARY-CRS-M1-00681` | `CRS-M1-00681` | PAD-IPV4-HEADER-TO-32-BIT-BOUNDARY | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-PROVIDE-SECURE-RELIABLE-PARTITION-DATA-EXCHANGE-CRS-M1-00607` | `CRS-M1-00607` | PROVIDE-SECURE-RELIABLE-PARTITION-DATA-EXCHANGE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-IMPLEMENT-IPV4-ADDRESSING-AND-FRAGMENTATION-CRS-M1-00612` | `CRS-M1-00612` | IMPLEMENT-IPV4-ADDRESSING-AND-FRAGMENTATION | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-APPLY-RFC-1123-TFTP-HOST-NOTES-WITHOUT-ADOPTING-MAIL-NETASCII-OR-BROADCAST-RRQ-CRS-M1-00616` | `CRS-M1-00616` | APPLY-RFC-1123-TFTP-HOST-NOTES-WITHOUT-ADOPTING-MAIL-NETASCII-OR-BROADCAST-RRQ | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-TX-TECHNOLOGICAL-LATENCY-BELOW-150US-PLUS-FRAME-DELAY-CRS-M1-00682` | `CRS-M1-00682` | KEEP-TX-TECHNOLOGICAL-LATENCY-BELOW-150US-PLUS-FRAME-DELAY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-RX-TECHNOLOGICAL-LATENCY-BELOW-150-MICROSECONDS-CRS-M1-00683` | `CRS-M1-00683` | KEEP-RX-TECHNOLOGICAL-LATENCY-BELOW-150-MICROSECONDS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-BOUND-MAX-JITTER-BY-40US-PLUS-VL-LOAD-TERM-CRS-M1-00684` | `CRS-M1-00684` | BOUND-MAX-JITTER-BY-40US-PLUS-VL-LOAD-TERM | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-BOUND-MAX-JITTER-BY-500-MICROSECONDS-EQUATION-CRS-M1-00685` | `CRS-M1-00685` | BOUND-MAX-JITTER-BY-500-MICROSECONDS-EQUATION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-MAC-SOURCE-AS-INDIVIDUAL-AND-LOCALLY-ADMINISTERED-CRS-M1-00686` | `CRS-M1-00686` | ENCODE-MAC-SOURCE-AS-INDIVIDUAL-AND-LOCALLY-ADMINISTERED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-MAC-SOURCE-CONSTANT-FIELD-TO-000000100000000000000000-CRS-M1-00687` | `CRS-M1-00687` | SET-MAC-SOURCE-CONSTANT-FIELD-TO-000000100000000000000000 | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-MAC-SOURCE-INDIVIDUAL-ADDRESS-BIT-TO-ZERO-CRS-M1-00688` | `CRS-M1-00688` | SET-MAC-SOURCE-INDIVIDUAL-ADDRESS-BIT-TO-ZERO | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-MAC-SOURCE-LOCALLY-ADMINISTERED-BIT-TO-ONE-CRS-M1-00689` | `CRS-M1-00689` | SET-MAC-SOURCE-LOCALLY-ADMINISTERED-BIT-TO-ONE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-MAC-SOURCE-USER-DEFINED-ID-AS-16-BITS-CRS-M1-00690` | `CRS-M1-00690` | ENCODE-MAC-SOURCE-USER-DEFINED-ID-AS-16-BITS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-USER-DEFINED-ID-FOR-UNIQUE-MEANINGFUL-HOST-IDENTITY-CRS-M1-00691` | `CRS-M1-00691` | USE-USER-DEFINED-ID-FOR-UNIQUE-MEANINGFUL-HOST-IDENTITY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-INTERFACE-ID-TO-IDENTIFY-REDUNDANT-AFDX-NETWORK-CRS-M1-00692` | `CRS-M1-00692` | USE-INTERFACE-ID-TO-IDENTIFY-REDUNDANT-AFDX-NETWORK | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-INTERFACE-ID-001-AS-NETWORK-A-CRS-M1-00693` | `CRS-M1-00693` | ENCODE-INTERFACE-ID-001-AS-NETWORK-A | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-INTERFACE-ID-010-AS-NETWORK-B-CRS-M1-00694` | `CRS-M1-00694` | ENCODE-INTERFACE-ID-010-AS-NETWORK-B | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-VL-JITTER-AT-OR-BELOW-500-MICROSECONDS-CRS-M1-00674` | `CRS-M1-00674` | KEEP-VL-JITTER-AT-OR-BELOW-500-MICROSECONDS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-PROVIDE-ADN-ADDRESS-DETERMINATION-GUIDANCE-CRS-M1-00695` | `CRS-M1-00695` | PROVIDE-ADN-ADDRESS-DETERMINATION-GUIDANCE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-KNOW-DESTINATION-ADDRESSES-AT-CONFIGURATION-TIME-CRS-M1-00696` | `CRS-M1-00696` | KNOW-DESTINATION-ADDRESSES-AT-CONFIGURATION-TIME | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-DEFINE-ADN-ADDRESSING-PLAN-AND-RULES-CRS-M1-00697` | `CRS-M1-00697` | DEFINE-ADN-ADDRESSING-PLAN-AND-RULES | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-IANA-WELL-KNOWN-UDP-PORTS-FOR-STANDARD-SERVICES-INCLUDING-TFTP-CRS-M1-00698` | `CRS-M1-00698` | USE-IANA-WELL-KNOWN-UDP-PORTS-FOR-STANDARD-SERVICES-INCLUDING-TFTP | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ACCESS-PRIVATE-AERO-APPS-VIA-INTEGRATOR-OR-664P4-UDP-PORTS-CRS-M1-00699` | `CRS-M1-00699` | ACCESS-PRIVATE-AERO-APPS-VIA-INTEGRATOR-OR-664P4-UDP-PORTS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-DO-NOT-REASSIGN-WELL-KNOWN-COTS-PORTS-0-1023-CRS-M1-00700` | `CRS-M1-00700` | DO-NOT-REASSIGN-WELL-KNOWN-COTS-PORTS-0-1023 | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-DO-NOT-ROUTE-PRIVATE-ADDRESSES-OUTSIDE-THE-NETWORK-CRS-M1-00701` | `CRS-M1-00701` | DO-NOT-ROUTE-PRIVATE-ADDRESSES-OUTSIDE-THE-NETWORK | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-PROFILED-AERO-NETWORK-AS-IETF-PRIVATE-APPLICATION-CRS-M1-00702` | `CRS-M1-00702` | TREAT-PROFILED-AERO-NETWORK-AS-IETF-PRIVATE-APPLICATION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-PRIVATE-NETWORK-ID-FOR-PROFILED-NETWORKS-CRS-M1-00703` | `CRS-M1-00703` | USE-PRIVATE-NETWORK-ID-FOR-PROFILED-NETWORKS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ASSIGN-MAC-UNICAST-ADDRESSES-AT-CONFIGURATION-TIME-CRS-M1-00704` | `CRS-M1-00704` | ASSIGN-MAC-UNICAST-ADDRESSES-AT-CONFIGURATION-TIME | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-MAC-ADDRESSES-UNIQUE-UNDER-INTEGRATOR-SCHEME-CRS-M1-00705` | `CRS-M1-00705` | KEEP-MAC-ADDRESSES-UNIQUE-UNDER-INTEGRATOR-SCHEME | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-MAC-UL-BIT-WHEN-INTEGRATOR-ASSIGNS-ADDRESSES-CRS-M1-00706` | `CRS-M1-00706` | SET-MAC-UL-BIT-WHEN-INTEGRATOR-ASSIGNS-ADDRESSES | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-ALL-NETWORK-ADDRESSES-UNIQUE-CRS-M1-00707` | `CRS-M1-00707` | KEEP-ALL-NETWORK-ADDRESSES-UNIQUE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RESERVE-UDP-TCP-PORT-59-FOR-615A-DATA-LOADER-TFTP-CRS-M1-00708` | `CRS-M1-00708` | RESERVE-UDP-TCP-PORT-59-FOR-615A-DATA-LOADER-TFTP | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ASSIGN-UDP-PORT-24922-TO-FIND-PROTOCOL-CLIENT-CRS-M1-00709` | `CRS-M1-00709` | ASSIGN-UDP-PORT-24922-TO-FIND-PROTOCOL-CLIENT | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ALLOCATE-TABLE-2-1-ADDRESSES-FROM-RFC1918-PRIVATE-RANGES-CRS-M1-00710` | `CRS-M1-00710` | ALLOCATE-TABLE-2-1-ADDRESSES-FROM-RFC1918-PRIVATE-RANGES | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-MEASURE-TX-TECHNOLOGICAL-LATENCY-BETWEEN-PARTITION-DATA-AND-PHYSICAL-MEDIA-CRS-M1-00711` | `CRS-M1-00711` | MEASURE-TX-TECHNOLOGICAL-LATENCY-BETWEEN-PARTITION-DATA-AND-PHYSICAL-MEDIA | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-START-TX-TECHNOLOGICAL-LATENCY-WHEN-LAST-PARTITION-BIT-IS-AVAILABLE-CRS-M1-00712` | `CRS-M1-00712` | START-TX-TECHNOLOGICAL-LATENCY-WHEN-LAST-PARTITION-BIT-IS-AVAILABLE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-END-TX-TECHNOLOGICAL-LATENCY-WHEN-LAST-FRAME-BIT-IS-ON-MEDIA-CRS-M1-00713` | `CRS-M1-00713` | END-TX-TECHNOLOGICAL-LATENCY-WHEN-LAST-FRAME-BIT-IS-ON-MEDIA | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-MEASURE-TX-TECHNOLOGICAL-LATENCY-WITH-EMPTY-BUFFERS-NO-CONTENTION-AND-NO-IP-FRAGMENTATION-CRS-M1-00714` | `CRS-M1-00714` | MEASURE-TX-TECHNOLOGICAL-LATENCY-WITH-EMPTY-BUFFERS-NO-CONTENTION-AND-NO-IP-FRAGMENTATION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-DISTINGUISH-TECHNOLOGICAL-LATENCY-FROM-CONFIGURATION-LOAD-LATENCY-CRS-M1-00715` | `CRS-M1-00715` | DISTINGUISH-TECHNOLOGICAL-LATENCY-FROM-CONFIGURATION-LOAD-LATENCY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-DEFINE-TECHNOLOGICAL-LATENCY-AS-ACCEPT-PROCESS-AND-BEGIN-TX-WITH-NO-OTHER-TASK-CRS-M1-00716` | `CRS-M1-00716` | DEFINE-TECHNOLOGICAL-LATENCY-AS-ACCEPT-PROCESS-AND-BEGIN-TX-WITH-NO-OTHER-TASK | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ADD-FRAME-DELAY-FOR-PHYSICAL-LAYER-DELIVERY-CRS-M1-00717` | `CRS-M1-00717` | ADD-FRAME-DELAY-FOR-PHYSICAL-LAYER-DELIVERY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-START-RX-TECHNOLOGICAL-LATENCY-WHEN-LAST-FRAME-BIT-IS-RECEIVED-CRS-M1-00718` | `CRS-M1-00718` | START-RX-TECHNOLOGICAL-LATENCY-WHEN-LAST-FRAME-BIT-IS-RECEIVED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-END-RX-TECHNOLOGICAL-LATENCY-WHEN-LAST-DATA-BIT-IS-AVAILABLE-TO-PARTITION-CRS-M1-00719` | `CRS-M1-00719` | END-RX-TECHNOLOGICAL-LATENCY-WHEN-LAST-DATA-BIT-IS-AVAILABLE-TO-PARTITION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-MEASURE-RX-TECHNOLOGICAL-LATENCY-WITH-EMPTY-BUFFERS-AND-NO-CONTENTION-CRS-M1-00720` | `CRS-M1-00720` | MEASURE-RX-TECHNOLOGICAL-LATENCY-WITH-EMPTY-BUFFERS-AND-NO-CONTENTION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SATISFY-BOTH-MAX-JITTER-EQUATIONS-SIMULTANEOUSLY-CRS-M1-00721` | `CRS-M1-00721` | SATISFY-BOTH-MAX-JITTER-EQUATIONS-SIMULTANEOUSLY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-MAX-JITTER-AS-MICROSECONDS-NBW-AS-BITS-PER-SECOND-AND-LMAX-AS-OCTETS-CRS-M1-00722` | `CRS-M1-00722` | TREAT-MAX-JITTER-AS-MICROSECONDS-NBW-AS-BITS-PER-SECOND-AND-LMAX-AS-OCTETS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-COMPOSE-MAC-SOURCE-AS-24-PLUS-16-PLUS-3-PLUS-5-BIT-FIELDS-CRS-M1-00723` | `CRS-M1-00723` | COMPOSE-MAC-SOURCE-AS-24-PLUS-16-PLUS-3-PLUS-5-BIT-FIELDS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-MAC-SOURCE-CONSTANT-TAIL-TO-00000-CRS-M1-00724` | `CRS-M1-00724` | SET-MAC-SOURCE-CONSTANT-TAIL-TO-00000 | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-MAC-SOURCE-CONSTRUCTION-ALGORITHM-AS-NOT-UNIQUELY-RECOMMENDED-CRS-M1-00725` | `CRS-M1-00725` | TREAT-MAC-SOURCE-CONSTRUCTION-ALGORITHM-AS-NOT-UNIQUELY-RECOMMENDED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-INTERFACE-ID-000-AS-NOT-USED-CRS-M1-00726` | `CRS-M1-00726` | RECORD-INTERFACE-ID-000-AS-NOT-USED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-INTERFACE-ID-011-AS-NOT-USED-CRS-M1-00727` | `CRS-M1-00727` | RECORD-INTERFACE-ID-011-AS-NOT-USED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-INTERFACE-ID-100-AS-NOT-USED-CRS-M1-00728` | `CRS-M1-00728` | RECORD-INTERFACE-ID-100-AS-NOT-USED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-INTERFACE-ID-101-AS-NOT-USED-CRS-M1-00729` | `CRS-M1-00729` | RECORD-INTERFACE-ID-101-AS-NOT-USED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-INTERFACE-ID-110-AS-SOURCE-NOR-USED-CRS-M1-00730` | `CRS-M1-00730` | RECORD-INTERFACE-ID-110-AS-SOURCE-NOR-USED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-INTERFACE-ID-111-AS-NOT-USED-CRS-M1-00731` | `CRS-M1-00731` | RECORD-INTERFACE-ID-111-AS-NOT-USED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-P3-RFC-OPTION-RESTRICTION-PHILOSOPHY-CRS-M1-00732` | `CRS-M1-00732` | RECORD-P3-RFC-OPTION-RESTRICTION-PHILOSOPHY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-P3-CONTENTS-LIMITED-TO-RFC-DELTAS-CRS-M1-00733` | `CRS-M1-00733` | RECORD-P3-CONTENTS-LIMITED-TO-RFC-DELTAS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-COMPOSE-AFDX-SWITCH-FROM-FIVE-FUNCTIONAL-BLOCKS-CRS-M1-00734` | `CRS-M1-00734` | COMPOSE-AFDX-SWITCH-FROM-FIVE-FUNCTIONAL-BLOCKS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-CONTROL-AFDX-SWITCH-FUNCTIONS-WITH-STATIC-CONFIGURATION-TABLES-CRS-M1-00735` | `CRS-M1-00735` | CONTROL-AFDX-SWITCH-FUNCTIONS-WITH-STATIC-CONFIGURATION-TABLES | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-SWITCH-END-SYSTEM-TO-COMPLY-WITH-SECTION-3-EXCEPT-REDUNDANCY-CRS-M1-00736` | `CRS-M1-00736` | REQUIRE-SWITCH-END-SYSTEM-TO-COMPLY-WITH-SECTION-3-EXCEPT-REDUNDANCY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-SWITCH-END-SYSTEM-UNICAST-MAC-AS-SOURCE-ADDRESS-CRS-M1-00737` | `CRS-M1-00737` | USE-SWITCH-END-SYSTEM-UNICAST-MAC-AS-SOURCE-ADDRESS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-615A-SESSION-ACROSS-OPS-TO-DL-TRANSITION-CRS-M1-00738` | `CRS-M1-00738` | KEEP-615A-SESSION-ACROSS-OPS-TO-DL-TRANSITION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-615A-AND-665-TO-UPLOAD-SWITCH-SOFTWARE-AND-CONFIGURATION-CRS-M1-00739` | `CRS-M1-00739` | USE-615A-AND-665-TO-UPLOAD-SWITCH-SOFTWARE-AND-CONFIGURATION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-AFDX-SWITCH-PHYSICAL-LAYER-TO-COMPLY-WITH-664P2-CRS-M1-00740` | `CRS-M1-00740` | REQUIRE-AFDX-SWITCH-PHYSICAL-LAYER-TO-COMPLY-WITH-664P2 | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-AS-NOT-USED-ON-AFDX-CRS-M1-00741` | `CRS-M1-00741` | TREAT-UDP-IP-OPTIONS-AS-NOT-USED-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-UDP-CHECKSUM-GENERATE-AND-CHECK-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00742` | `CRS-M1-00742` | TREAT-UDP-CHECKSUM-GENERATE-AND-CHECK-AS-NOT-APPLICABLE-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-AFDX-END-SYSTEM-INTERNET-LAYER-TO-IMPLEMENT-IP-CRS-M1-00743` | `CRS-M1-00743` | REQUIRE-AFDX-END-SYSTEM-INTERNET-LAYER-TO-IMPLEMENT-IP | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-AFDX-END-SYSTEM-INTERNET-LAYER-TO-IMPLEMENT-ICMP-CRS-M1-00744` | `CRS-M1-00744` | REQUIRE-AFDX-END-SYSTEM-INTERNET-LAYER-TO-IMPLEMENT-ICMP | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SILENTLY-DISCARD-NON-IPV4-DATAGRAMS-CRS-M1-00745` | `CRS-M1-00745` | SILENTLY-DISCARD-NON-IPV4-DATAGRAMS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-AFDX-UDP-CHECKSUM-UNUSED-COMMENT-CRS-M1-00746` | `CRS-M1-00746` | RECORD-AFDX-UDP-CHECKSUM-UNUSED-COMMENT | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-SILENT-BAD-UDP-CHECKSUM-DISCARD-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00747` | `CRS-M1-00747` | TREAT-SILENT-BAD-UDP-CHECKSUM-DISCARD-AS-NOT-APPLICABLE-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-PASS-ICMP-MESSAGES-TO-APPLICATION-LIMITED-TO-ECHO-REQUEST-CRS-M1-00748` | `CRS-M1-00748` | PASS-ICMP-MESSAGES-TO-APPLICATION-LIMITED-TO-ECHO-REQUEST | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-UDP-PORT-UNREACHABLE-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00749` | `CRS-M1-00749` | TREAT-UDP-PORT-UNREACHABLE-AS-NOT-APPLICABLE-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-FORBID-REMOTE-MULTIHOMING-AT-APPLICATION-LAYER-ON-AFDX-CRS-M1-00750` | `CRS-M1-00750` | FORBID-REMOTE-MULTIHOMING-AT-APPLICATION-LAYER-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-LOCAL-MULTIHOMING-ON-AFDX-CRS-M1-00751` | `CRS-M1-00751` | REQUIRE-LOCAL-MULTIHOMING-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-LOG-DISCARDED-DATAGRAMS-ON-AFDX-CRS-M1-00752` | `CRS-M1-00752` | LOG-DISCARDED-DATAGRAMS-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-DISCARDED-DATAGRAMS-IN-COUNTER-ON-AFDX-CRS-M1-00753` | `CRS-M1-00753` | RECORD-DISCARDED-DATAGRAMS-IN-COUNTER-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ENTER-OPS-AFTER-COMPATIBLE-INIT-WHEN-SHOP-INACTIVE-CRS-M1-00754` | `CRS-M1-00754` | ENTER-OPS-AFTER-COMPATIBLE-INIT-WHEN-SHOP-INACTIVE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-PROVIDE-OPS-MODE-615A-INFORMATION-AND-FIND-CRS-M1-00755` | `CRS-M1-00755` | PROVIDE-OPS-MODE-615A-INFORMATION-AND-FIND | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ENTER-DL-FROM-INIT-ONLY-WHEN-GROUND-AND-COMPATIBILITY-FAIL-OR-EMPTY-CRS-M1-00756` | `CRS-M1-00756` | ENTER-DL-FROM-INIT-ONLY-WHEN-GROUND-AND-COMPATIBILITY-FAIL-OR-EMPTY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ENTER-DL-FROM-OPS-ONLY-WHEN-GROUND-UPLOAD-INIT-AND-HEADER-ACCEPTED-CRS-M1-00757` | `CRS-M1-00757` | ENTER-DL-FROM-OPS-ONLY-WHEN-GROUND-UPLOAD-INIT-AND-HEADER-ACCEPTED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-PROVIDE-DL-MODE-615A-INFORMATION-UPLOAD-AND-FIND-CRS-M1-00758` | `CRS-M1-00758` | PROVIDE-DL-MODE-615A-INFORMATION-UPLOAD-AND-FIND | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-SEND-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00759` | `CRS-M1-00759` | TREAT-UDP-IP-OPTIONS-SEND-AS-NOT-APPLICABLE-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-DOWN-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00760` | `CRS-M1-00760` | TREAT-UDP-IP-OPTIONS-DOWN-AS-NOT-APPLICABLE-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-GATEWAY-FORWARDING-SPEC-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00761` | `CRS-M1-00761` | TREAT-GATEWAY-FORWARDING-SPEC-AS-NOT-APPLICABLE-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-EMBEDDED-GATEWAY-SWITCH-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00762` | `CRS-M1-00762` | TREAT-EMBEDDED-GATEWAY-SWITCH-AS-NOT-APPLICABLE-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-NON-GATEWAY-DEFAULT-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00763` | `CRS-M1-00763` | TREAT-NON-GATEWAY-DEFAULT-AS-NOT-APPLICABLE-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-AFDX-GATEWAY-AUTOCONFIGURATION-ROW-UNMARKED-CRS-M1-00764` | `CRS-M1-00764` | RECORD-AFDX-GATEWAY-AUTOCONFIGURATION-ROW-UNMARKED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-PERFORM-OPS-FILTERING-POLICING-SWITCHING-FROM-OPS-CONFIG-CRS-M1-00765` | `CRS-M1-00765` | PERFORM-OPS-FILTERING-POLICING-SWITCHING-FROM-OPS-CONFIG | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-OPS-FAULT-HEALTHY-INDICATOR-TO-HEALTHY-CRS-M1-00766` | `CRS-M1-00766` | SET-OPS-FAULT-HEALTHY-INDICATOR-TO-HEALTHY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-DL-UPLOAD-AS-PREFERABLY-EXCLUSIVE-CRS-M1-00767` | `CRS-M1-00767` | TREAT-DL-UPLOAD-AS-PREFERABLY-EXCLUSIVE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-DEDICATE-SWITCH-TO-UPLOAD-DURING-DL-UPLOAD-CRS-M1-00768` | `CRS-M1-00768` | DEDICATE-SWITCH-TO-UPLOAD-DURING-DL-UPLOAD | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-DEFAULT-RECEPTION-VL-FOR-DATALOADING-CRS-M1-00769` | `CRS-M1-00769` | REQUIRE-DEFAULT-RECEPTION-VL-FOR-DATALOADING | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-TWELVE-PIN-POSITION-IDENTIFICATION-AS-EXAMPLE-CRS-M1-00770` | `CRS-M1-00770` | RECORD-TWELVE-PIN-POSITION-IDENTIFICATION-AS-EXAMPLE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-STATED-TWELVE-PIN-DEFINITIONS-IF-TWELVE-PINS-CHOSEN-CRS-M1-00771` | `CRS-M1-00771` | USE-STATED-TWELVE-PIN-DEFINITIONS-IF-TWELVE-PINS-CHOSEN | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-DEFAULT-CONFIGURATION-TABLE-RESIDENT-CRS-M1-00772` | `CRS-M1-00772` | KEEP-DEFAULT-CONFIGURATION-TABLE-RESIDENT | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-DEFAULT-PHYSICAL-PORT-SPEED-100MBPS-WITHOUT-AUTONEG-CRS-M1-00773` | `CRS-M1-00773` | SET-DEFAULT-PHYSICAL-PORT-SPEED-100MBPS-WITHOUT-AUTONEG | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-DEFAULT-RECEPTION-VL-FIELDS-IN-NONVOLATILE-MEMORY-CRS-M1-00774` | `CRS-M1-00774` | REQUIRE-DEFAULT-RECEPTION-VL-FIELDS-IN-NONVOLATILE-MEMORY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-DEFAULT-TRANSMISSION-VL-FIELDS-IN-NONVOLATILE-MEMORY-CRS-M1-00775` | `CRS-M1-00775` | REQUIRE-DEFAULT-TRANSMISSION-VL-FIELDS-IN-NONVOLATILE-MEMORY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-DEFAULT-TRANSMISSION-VL-FOR-DATALOADING-ACKNOWLEDGE-CRS-M1-00776` | `CRS-M1-00776` | REQUIRE-DEFAULT-TRANSMISSION-VL-FOR-DATALOADING-ACKNOWLEDGE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-OPS-CONFIGURATION-FILE-615A-665-FIELD-LOADABLE-CRS-M1-00777` | `CRS-M1-00777` | REQUIRE-OPS-CONFIGURATION-FILE-615A-665-FIELD-LOADABLE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-FILTERING-POLICING-FORWARDING-TABLE-PARAMETER-SET-CRS-M1-00778` | `CRS-M1-00778` | REQUIRE-FILTERING-POLICING-FORWARDING-TABLE-PARAMETER-SET | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-LISTED-PARAMETERS-TO-CONFIGURE-FILTER-POLICE-FORWARD-CRS-M1-00779` | `CRS-M1-00779` | REQUIRE-LISTED-PARAMETERS-TO-CONFIGURE-FILTER-POLICE-FORWARD | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-PERFORM-DL-END-SYSTEM-FROM-DEFAULT-CONFIGURATION-TABLE-CRS-M1-00780` | `CRS-M1-00780` | PERFORM-DL-END-SYSTEM-FROM-DEFAULT-CONFIGURATION-TABLE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-DL-FAULT-HEALTHY-INDICATOR-TO-HEALTHY-CRS-M1-00781` | `CRS-M1-00781` | SET-DL-FAULT-HEALTHY-INDICATOR-TO-HEALTHY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RETURN-TO-INIT-AT-END-OF-DL-MODE-CRS-M1-00782` | `CRS-M1-00782` | RETURN-TO-INIT-AT-END-OF-DL-MODE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-DL-MODE-END-AS-615A-DATA-LOADING-FUNCTION-END-CRS-M1-00783` | `CRS-M1-00783` | TREAT-DL-MODE-END-AS-615A-DATA-LOADING-FUNCTION-END | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-LIMIT-SWITCH-FIELD-LOADABLE-SOFTWARE-TO-OPS-CONFIG-AND-OPS-SOFTWARE-CRS-M1-00784` | `CRS-M1-00784` | LIMIT-SWITCH-FIELD-LOADABLE-SOFTWARE-TO-OPS-CONFIG-AND-OPS-SOFTWARE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-FIELD-LOADABLE-FILES-IDENTICAL-ACROSS-AIRCRAFT-SWITCHES-CRS-M1-00785` | `CRS-M1-00785` | REQUIRE-FIELD-LOADABLE-FILES-IDENTICAL-ACROSS-AIRCRAFT-SWITCHES | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-MAKE-SWITCH-CONFIGURATION-ACCESSIBLE-VIA-615A-INFORMATION-CRS-M1-00786` | `CRS-M1-00786` | MAKE-SWITCH-CONFIGURATION-ACCESSIBLE-VIA-615A-INFORMATION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-LEARN-DATALOADER-IP-FROM-SOURCE-ADDRESS-CRS-M1-00787` | `CRS-M1-00787` | LEARN-DATALOADER-IP-FROM-SOURCE-ADDRESS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-PIN-PROGRAMMING-FOR-POSITION-AND-DEFAULT-MAC-IP-CRS-M1-00788` | `CRS-M1-00788` | USE-PIN-PROGRAMMING-FOR-POSITION-AND-DEFAULT-MAC-IP | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-READ-PROGRAM-PINS-IN-INIT-ONLY-WHEN-GROUND-BEFORE-SAFETY-TEST-CRS-M1-00789` | `CRS-M1-00789` | READ-PROGRAM-PINS-IN-INIT-ONLY-WHEN-GROUND-BEFORE-SAFETY-TEST | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-DO-NOT-READ-PROGRAM-PINS-WHEN-GROUND-CONDITION-FALSE-CRS-M1-00790` | `CRS-M1-00790` | DO-NOT-READ-PROGRAM-PINS-WHEN-GROUND-CONDITION-FALSE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-LAST-MEMORIZED-PIN-VALUES-WHEN-NOT-GROUND-CRS-M1-00791` | `CRS-M1-00791` | USE-LAST-MEMORIZED-PIN-VALUES-WHEN-NOT-GROUND | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-CHECK-TWELVE-PROGRAM-PINS-WITH-PARITY-BIT-CRS-M1-00792` | `CRS-M1-00792` | CHECK-TWELVE-PROGRAM-PINS-WITH-PARITY-BIT | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-MEMORIZE-PROGRAM-PINS-IN-NVM-AFTER-PARITY-PASS-CRS-M1-00793` | `CRS-M1-00793` | MEMORIZE-PROGRAM-PINS-IN-NVM-AFTER-PARITY-PASS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ACQUIRE-SWITCH-POSITION-WITH-TWELVE-PINS-P1-P12-CRS-M1-00794` | `CRS-M1-00794` | ACQUIRE-SWITCH-POSITION-WITH-TWELVE-PINS-P1-P12 | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-CODE-PIN-GROUND-AS-ONE-CRS-M1-00795` | `CRS-M1-00795` | CODE-PIN-GROUND-AS-ONE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-CODE-PIN-OPEN-AS-ZERO-CRS-M1-00796` | `CRS-M1-00796` | CODE-PIN-OPEN-AS-ZERO | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-PROCESS-AT-LEAST-4096-VLS-IN-FILTER-POLICE-FORWARD-CRS-M1-00797` | `CRS-M1-00797` | PROCESS-AT-LEAST-4096-VLS-IN-FILTER-POLICE-FORWARD | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-INPUT-PHYSICAL-PORT-CRS-M1-00798` | `CRS-M1-00798` | INCLUDE-FILTER-TABLE-PER-VL-INPUT-PHYSICAL-PORT | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-OUTPUT-PHYSICAL-PORTS-CRS-M1-00799` | `CRS-M1-00799` | INCLUDE-FILTER-TABLE-PER-VL-OUTPUT-PHYSICAL-PORTS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-MAC-DESTINATION-CRS-M1-00800` | `CRS-M1-00800` | INCLUDE-FILTER-TABLE-PER-VL-MAC-DESTINATION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-BAG-CRS-M1-00801` | `CRS-M1-00801` | INCLUDE-FILTER-TABLE-PER-VL-BAG | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-MAX-JITTER-CRS-M1-00802` | `CRS-M1-00802` | INCLUDE-FILTER-TABLE-PER-VL-MAX-JITTER | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-ACCOUNT-CRS-M1-00803` | `CRS-M1-00803` | INCLUDE-FILTER-TABLE-PER-VL-ACCOUNT | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-SMAX-CRS-M1-00804` | `CRS-M1-00804` | INCLUDE-FILTER-TABLE-PER-VL-SMAX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-SMIN-CRS-M1-00805` | `CRS-M1-00805` | INCLUDE-FILTER-TABLE-PER-VL-SMIN | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-PRIORITIZATION-CRS-M1-00806` | `CRS-M1-00806` | INCLUDE-FILTER-TABLE-PER-VL-PRIORITIZATION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-MAX-DELAY-CRS-M1-00807` | `CRS-M1-00807` | INCLUDE-FILTER-TABLE-PER-PORT-MAX-DELAY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-STATE-CRS-M1-00808` | `CRS-M1-00808` | INCLUDE-FILTER-TABLE-PER-PORT-STATE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-SPEED-CRS-M1-00809` | `CRS-M1-00809` | INCLUDE-FILTER-TABLE-PER-PORT-SPEED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-LOW-PRIORITY-BUFFER-CRS-M1-00810` | `CRS-M1-00810` | INCLUDE-FILTER-TABLE-PER-PORT-LOW-PRIORITY-BUFFER | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-HIGH-PRIORITY-BUFFER-CRS-M1-00811` | `CRS-M1-00811` | INCLUDE-FILTER-TABLE-PER-PORT-HIGH-PRIORITY-BUFFER | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-VL-IDENTIFIER-CRS-M1-00812` | `CRS-M1-00812` | INCLUDE-DEFAULT-RX-VL-IDENTIFIER | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-SMAX-CRS-M1-00813` | `CRS-M1-00813` | INCLUDE-DEFAULT-RX-SMAX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-BAG-CRS-M1-00814` | `CRS-M1-00814` | INCLUDE-DEFAULT-RX-BAG | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-VL-IDENTIFIER-CRS-M1-00815` | `CRS-M1-00815` | INCLUDE-DEFAULT-TX-VL-IDENTIFIER | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-BAG-CRS-M1-00816` | `CRS-M1-00816` | INCLUDE-DEFAULT-TX-BAG | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-SMAX-CRS-M1-00817` | `CRS-M1-00817` | INCLUDE-DEFAULT-TX-SMAX | ARINC-664-NETWORK-CONSTRAINT |

## Interfaces

- `IF_TFTP` `ABSTRACT-TRANSPORT` — Does not reconstruct the full TFTP/IPv4 stack.
- `IF_TFTP_BLOCKSIZE` `OPTION-CAPABILITY` — 615A 5.3.2.3.8.1 requires Data Loader block-size / network-interface capability. RFC 2348 §2 is the candidate option encoding. Capability remains NOT-ESTABLISHED.
- `IF_INTEGRITY` `DEPENDENCY-GUARDED` — Integrity success is not assumed.
- `IF_NETWORK` `INFRASTRUCTURE-PREMISE` — Compliant IPv4/UDP host service is a premise for Project Configuration.

## Timing catalog

| ID | CRS | Clock | Kind | Bounds | AST | Resets | Endpoints | Check | Window |
|---|---|---|---|---|---|---|---|---|---|
| `TIM-CRS-M1-00032` | `CRS-M1-00032` | `CLK_WAIT` | NOT-BEFORE-LOWER-BOUND | MESSAGE_TIMER_VALUE..None s | `{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_WAIT"},"right":{"kind":"SYMBOL","name":"MESSAGE_TIMER_VALUE","unit":"s"}}` | T_WAIT_FROM_UPL_FILE, T_WAIT_FROM_UPL_LUR, T_WAIT_FROM_INF_LCI, T_WAIT_FROM_INF_LCL | CLOSED/UNRESOLVED | `RELATION-BOUND` | RETRY-NOT-BEFORE-CARRIED-TIMER |
| `TIM-CRS-M1-00094` | `CRS-M1-00094` | `CLK_DLP` | DEADLINE-UPPER-BOUND | None..DLP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00097` | `CRS-M1-00097` | `CLK_DLP` | DEADLINE-UPPER-BOUND | None..DLP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00098` | `CRS-M1-00098` | `CLK_DLP` | DEADLINE-UPPER-BOUND | None..DLP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00099` | `CRS-M1-00099` | `CLK_EXCEPTION` | DEADLINE-UPPER-BOUND | None..EXCEPTION_TIMER s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}` | T_ENTER_UPL_EXC, T_ENTER_INF_EXC, T_INF_LCS_WRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00100` | `CRS-M1-00100` | `CLK_EXCEPTION` | DEADLINE-UPPER-BOUND | None..EXCEPTION_TIMER s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}` | T_ENTER_UPL_EXC, T_ENTER_INF_EXC, T_INF_LCS_WRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00101` | `CRS-M1-00101` | `CLK_EXCEPTION` | DEADLINE-UPPER-BOUND | None..EXCEPTION_TIMER s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}` | T_ENTER_UPL_EXC, T_ENTER_INF_EXC, T_INF_LCS_WRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00102` | `CRS-M1-00102` | `CLK_DLP` | DEADLINE-UPPER-BOUND | None..DLP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00106` | `CRS-M1-00106` | `CLK_EXCEPTION` | DEADLINE-UPPER-BOUND | None..EXCEPTION_TIMER s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}` | T_ENTER_UPL_EXC, T_ENTER_INF_EXC, T_INF_LCS_WRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00107` | `CRS-M1-00107` | `CLK_EXCEPTION` | DEADLINE-UPPER-BOUND | None..EXCEPTION_TIMER s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}` | T_ENTER_UPL_EXC, T_ENTER_INF_EXC, T_INF_LCS_WRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00108` | `CRS-M1-00108` | `CLK_EXCEPTION` | DEADLINE-UPPER-BOUND | None..EXCEPTION_TIMER s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}` | T_ENTER_UPL_EXC, T_ENTER_INF_EXC, T_INF_LCS_WRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00168` | `CRS-M1-00168` | `CLK_TFTP` | DEADLINE-UPPER-BOUND | None..TFTP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_TFTP"},"right":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"}}` | T_INF_LCI_RRQ, T_UPL_LUI_RRQ, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00176` | `CRS-M1-00176` | `CLK_DLP` | DEADLINE-UPPER-BOUND | None..DLP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00177` | `CRS-M1-00177` | `CLK_TFTP` | CONSTANT-DEFINITION | 2..2 s | `{"kind":"LITERAL","value":2,"unit":"s"}` | T_INF_LCI_RRQ, T_UPL_LUI_RRQ, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | CLOSED/CLOSED | `CONSTANT-DEFINITION` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00178` | `CRS-M1-00178` | `CLK_TFTP` | SOURCE-EQUATION | 0..TFTP-TO-DIVIDED-BY-4 s | `{"kind":"COMPARE","op":"LE","left":{"kind":"SYMBOL","name":"DURATION_TIME","unit":"s"},"right":{"kind":"BINARY","op":"DIV","left":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"},"right":{"kind":"LITERAL","value":4,"unit":"1"},"unit":"s"}}` | T_INF_LCI_RRQ, T_UPL_LUI_RRQ, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | CLOSED/CLOSED | `EQUATION-STRUCTURAL` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00179` | `CRS-M1-00179` | `CLK_DLP` | SOURCE-EQUATION | 0..TFTP-TO-DIVIDED-BY-2 s | `{"kind":"COMPARE","op":"LE","left":{"kind":"SYMBOL","name":"DURATION_TIME","unit":"s"},"right":{"kind":"BINARY","op":"DIV","left":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"},"right":{"kind":"LITERAL","value":2,"unit":"1"},"unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | CLOSED/CLOSED | `EQUATION-STRUCTURAL` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00184` | `CRS-M1-00184` | `CLK_DLP` | DEADLINE-UPPER-BOUND | None..DLP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00185` | `CRS-M1-00185` | `CLK_DLP` | DEADLINE-UPPER-BOUND | None..DLP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00186` | `CRS-M1-00186` | `CLK_DLP` | PROHIBITION-WINDOW-UPPER-BOUND | None..DLP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00187` | `CRS-M1-00187` | `CLK_DLP` | CONSTANT-DEFINITION | 13..13 s | `{"kind":"LITERAL","value":13,"unit":"s"}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | CLOSED/CLOSED | `CONSTANT-DEFINITION` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00188` | `CRS-M1-00188` | `CLK_DLP` | SOURCE-EQUATION | 0..DLP-TO-MINUS-RETRY-AND-NETWORK-TERMS s | `{"kind":"COMPARE","op":"GT","left":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"},"right":{"kind":"BINARY","op":"ADD","left":{"kind":"SYMBOL","name":"DURATION_TIME","unit":"s"},"right":{"kind":"BINARY","op":"ADD","left":{"kind":"BINARY","op":"MUL","left":{"kind":"BINARY","op":"MUL","left":{"kind":"SYMBOL","name":"DLP_RETRY","unit":"1"},"right":{"kind":"BINARY","op":"ADD","left":{"kind":"SYMBOL","name":"TFTP_RETRY","unit":"1"},"right":{"kind":"LITERAL","value":1,"unit":"1"},"unit":"1"},"unit":"1"},"right":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"},"unit":"s"},"right":{"kind":"BINARY","op":"ADD","left":{"kind":"BINARY","op":"MUL","left":{"kind":"SYMBOL","name":"TFTP_RETRY","unit":"1"},"right":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"},"unit":"s"},"right":{"kind":"BINARY","op":"MUL","left":{"kind":"LITERAL","value":2,"unit":"1"},"right":{"kind":"BINARY","op":"DIV","left":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"},"right":{"kind":"LITERAL","value":4,"unit":"1"},"unit":"s"},"unit":"s"},"unit":"s"},"unit":"s"},"unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | CLOSED/OPEN | `EQUATION-STRUCTURAL` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00305` | `CRS-M1-00305` | `CLK_EXCEPTION` | DEADLINE-UPPER-BOUND | None..EXCEPTION_TIMER s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}` | T_ENTER_UPL_EXC, T_ENTER_INF_EXC, T_INF_LCS_WRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00322` | `CRS-M1-00322` | `CLK_EXCEPTION` | DEADLINE-UPPER-BOUND | None..EXCEPTION_TIMER s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}` | T_ENTER_UPL_EXC, T_ENTER_INF_EXC, T_INF_LCS_WRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00520` | `CRS-M1-00520` | `CLK_FIND` | CONSTANT-DEFINITION | 3..3 s | `{"kind":"LITERAL","value":3,"unit":"s"}` | — | CLOSED/CLOSED | `CONSTANT-DEFINITION` | FIND-ANSWER-WINDOW-LIFETIME |
| `TIM-CRS-M1-00391` | `CRS-M1-00391` | `CLK_FIND` | DEADLINE-UPPER-BOUND | 0..2 s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_FIND"},"right":{"kind":"LITERAL","value":2,"unit":"s"}}` | — | CLOSED/CLOSED | `RELATION-BOUND` | FIND-HOST-ANSWER-UPPER-BOUND |
| `TIM-CRS-M1-00521` | `CRS-M1-00521` | `CLK_FIND` | CONSTANT-DEFINITION | 3..3 s | `{"kind":"COMPARE","op":"EQ","left":{"kind":"CLOCK","name":"CLK_FIND"},"right":{"kind":"LITERAL","value":3,"unit":"s"}}` | — | CLOSED/CLOSED | `CONSTANT-DEFINITION` | FIND-REGISTRATION-CLOSE-AT-EXPIRY |
| `TIM-CRS-M1-00682` | `CRS-M1-00682` | `CLK_AFDX_ES` | SOURCE-EQUATION | 0..ONE-HUNDRED-FIFTY-MICROSECONDS-PLUS-FRAME-DELAY us | `{"kind":"COMPARE","op":"LT","left":{"kind":"SYMBOL","name":"TECH_LAT_TX","unit":"us"},"right":{"kind":"BINARY","op":"ADD","left":{"kind":"LITERAL","value":150,"unit":"us"},"right":{"kind":"SYMBOL","name":"FRAME_DELAY","unit":"us"},"unit":"us"}}` | — | CLOSED/OPEN | `EQUATION-STRUCTURAL` | AFDX-TX-TECH-LATENCY-STRICT-OPEN-BOUND |
| `TIM-CRS-M1-00683` | `CRS-M1-00683` | `CLK_AFDX_ES` | SOURCE-EQUATION | 0..150 us | `{"kind":"COMPARE","op":"LT","left":{"kind":"SYMBOL","name":"TECH_LAT_RX","unit":"us"},"right":{"kind":"LITERAL","value":150,"unit":"us"}}` | — | CLOSED/OPEN | `EQUATION-STRUCTURAL` | AFDX-RX-TECH-LATENCY-STRICT-OPEN-BOUND |
| `TIM-CRS-M1-00684` | `CRS-M1-00684` | `CLK_AFDX_ES` | SOURCE-EQUATION | 0..FORTY-MICROSECONDS-PLUS-CONVERTED-VL-LOAD-TERM us | `{"kind":"COMPARE","op":"LE","left":{"kind":"SYMBOL","name":"MAX_JITTER","unit":"us"},"right":{"kind":"BINARY","op":"ADD","left":{"kind":"LITERAL","value":40,"unit":"us"},"right":{"kind":"BINARY","op":"MUL","left":{"kind":"BINARY","op":"DIV","left":{"kind":"BINARY","op":"MUL","left":{"kind":"LITERAL","value":8,"unit":"1"},"right":{"kind":"SUM","index":"I","domain":"CONFIGURED-VL-SET","unit":"1","body":{"kind":"BINARY","op":"ADD","left":{"kind":"LITERAL","value":20,"unit":"1"},"right":{"kind":"SYMBOL","name":"LMAX_I","unit":"1"},"unit":"1"}},"unit":"1"},"right":{"kind":"SYMBOL","name":"NBW","unit":"1"},"unit":"s"},"right":{"kind":"LITERAL","value":1000000,"unit":"1"},"unit":"us"},"unit":"us"}}` | — | CLOSED/CLOSED | `EQUATION-STRUCTURAL` | AFDX-MAX-JITTER-LOAD-EQUATION |
| `TIM-CRS-M1-00685` | `CRS-M1-00685` | `CLK_AFDX_ES` | SOURCE-EQUATION | 0..500 us | `{"kind":"COMPARE","op":"LE","left":{"kind":"SYMBOL","name":"MAX_JITTER","unit":"us"},"right":{"kind":"LITERAL","value":500,"unit":"us"}}` | — | CLOSED/CLOSED | `EQUATION-STRUCTURAL` | AFDX-MAX-JITTER-500US-EQUATION |

## Requirement dispositions

| CRS | Kind | Targets |
|---|---|---|
| `CRS-M1-00001` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00002` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00003` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00004` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00005` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00006` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00007` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00008` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00009` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00010` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00011` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00012` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00013` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00014` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00015` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00016` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00017` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00018` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00019` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00020` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00021` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00022` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00023` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00024` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00025` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00026` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00027` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00028` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00029` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00030` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00031` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00032` | MODELED-TIMING | `IF_TFTP`, `TIM-CRS-M1-00032`, `CLK_WAIT`, `T_WAIT_FROM_UPL_FILE`, `T_WAIT_FROM_UPL_LUR`, `T_WAIT_FROM_INF_LCI`, `T_WAIT_FROM_INF_LCL`, `T_WAIT_RETRY_UPL_FILE`, `T_WAIT_RETRY_UPL_LUR`, `T_WAIT_RETRY_INF_LCI`, `T_WAIT_RETRY_INF_LCL` |
| `CRS-M1-00033` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00034` | INTERFACE-PREMISE | `IF_TFTP_BLOCKSIZE` |
| `CRS-M1-00035` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00036` | INTERFACE-PREMISE | `IF_TFTP_BLOCKSIZE` |
| `CRS-M1-00037` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00038` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00039` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00040` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00041` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00042` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00043` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00044` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00045` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00046` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00047` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00048` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00049` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00050` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00051` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00052` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00053` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00054` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00055` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00056` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00057` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00058` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00059` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00060` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00061` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00062` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00063` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00064` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00065` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00066` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00067` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00068` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00069` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00070` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00071` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00072` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00073` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00074` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00075` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00076` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00077` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00078` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00079` | MODELED | `T_UPL_LUR_XFER` |
| `CRS-M1-00080` | MODELED | `T_UPL_LUS_XFER` |
| `CRS-M1-00081` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00082` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00083` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00084` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00085` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00086` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00087` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00088` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00089` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00090` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00091` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00092` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00093` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00094` | MODELED-TIMING | `T_INF_LCI_XFER`, `TIM-CRS-M1-00094`, `CLK_DLP` |
| `CRS-M1-00095` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00096` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00097` | MODELED-TIMING | `T_INF_LCI_XFER`, `TIM-CRS-M1-00097`, `CLK_DLP` |
| `CRS-M1-00098` | MODELED-TIMING | `T_INF_LCI_XFER`, `TIM-CRS-M1-00098`, `CLK_DLP` |
| `CRS-M1-00099` | MODELED-TIMING | `T_INF_LCI_XFER`, `TIM-CRS-M1-00099`, `CLK_EXCEPTION`, `T_ENTER_UPL_EXC`, `T_ENTER_INF_EXC` |
| `CRS-M1-00100` | MODELED-TIMING | `T_INF_LCI_XFER`, `TIM-CRS-M1-00100`, `CLK_EXCEPTION` |
| `CRS-M1-00101` | MODELED-TIMING | `T_INF_LCI_XFER`, `TIM-CRS-M1-00101`, `CLK_EXCEPTION`, `T_UPL_EXC_TO`, `T_INF_EXC_TO` |
| `CRS-M1-00102` | MODELED-TIMING | `T_UPL_LUS_XFER`, `TIM-CRS-M1-00102`, `CLK_DLP` |
| `CRS-M1-00103` | MODELED | `T_UPL_LUS_XFER` |
| `CRS-M1-00104` | MODELED | `T_UPL_LUS_XFER` |
| `CRS-M1-00105` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00106` | MODELED-TIMING | `T_UPL_FILE_XFER`, `TIM-CRS-M1-00106`, `CLK_EXCEPTION` |
| `CRS-M1-00107` | MODELED-TIMING | `T_UPL_FILE_XFER`, `TIM-CRS-M1-00107`, `CLK_EXCEPTION` |
| `CRS-M1-00108` | MODELED-TIMING | `T_UPL_LUS_XFER`, `TIM-CRS-M1-00108`, `CLK_EXCEPTION`, `T_UPL_EXC_TO` |
| `CRS-M1-00109` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00110` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00111` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00112` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00113` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00114` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00115` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00116` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00117` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00118` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00119` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00120` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00121` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00122` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00123` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00124` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00125` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00126` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00127` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00128` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00129` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00130` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00131` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00132` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00133` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00134` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00135` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00136` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00137` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00138` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00139` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00140` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00141` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00142` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00143` | MODELED | `T_UPL_LUR_XFER` |
| `CRS-M1-00144` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00145` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00146` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00147` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00148` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00149` | MODELED | `T_UPL_LUS_XFER` |
| `CRS-M1-00150` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00151` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00152` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00153` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00154` | MODELED | `T_UPL_LUS_XFER` |
| `CRS-M1-00155` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00156` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00157` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00158` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00159` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00160` | MODELED | `T_UPL_LUS_XFER` |
| `CRS-M1-00161` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00162` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00163` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00164` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00165` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00166` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00167` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00168` | MODELED-TIMING | `IF_TFTP`, `TIM-CRS-M1-00168`, `CLK_TFTP` |
| `CRS-M1-00169` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00170` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00171` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00172` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00173` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00174` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00175` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00176` | SCOPE-CONSTRAINT | `SCOPE`, `TIM-CRS-M1-00176`, `CLK_DLP` |
| `CRS-M1-00177` | SCOPE-CONSTRAINT | `SCOPE`, `TIM-CRS-M1-00177`, `CLK_TFTP`, `T_INF_TFTP_TO`, `T_UPL_TFTP_TO`, `T_UPL_LUR_TFTP_TO`, `T_UPL_FILE_TFTP_TO` |
| `CRS-M1-00178` | MODELED-TIMING | `IF_TFTP`, `TIM-CRS-M1-00178`, `CLK_TFTP` |
| `CRS-M1-00179` | MODELED-TIMING | `IF_TFTP`, `TIM-CRS-M1-00179`, `CLK_DLP` |
| `CRS-M1-00180` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00181` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00182` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00183` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00184` | MODELED-TIMING | `IF_TFTP`, `TIM-CRS-M1-00184`, `CLK_DLP` |
| `CRS-M1-00185` | SCOPE-CONSTRAINT | `SCOPE`, `TIM-CRS-M1-00185`, `CLK_DLP` |
| `CRS-M1-00186` | SCOPE-CONSTRAINT | `SCOPE`, `TIM-CRS-M1-00186`, `CLK_DLP` |
| `CRS-M1-00187` | SCOPE-CONSTRAINT | `SCOPE`, `TIM-CRS-M1-00187`, `CLK_DLP`, `T_UPL_DLP_TO`, `T_UPL_LUR_DLP_TO` |
| `CRS-M1-00188` | MODELED-TIMING | `IF_TFTP`, `TIM-CRS-M1-00188`, `CLK_DLP`, `T_UPL_LUR_DLP_TO` |
| `CRS-M1-00189` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00190` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00191` | DATA-CONSTRAINT | `OBJ-MINIMUM-ARINC-665-COMPATIBILITY-CAPABILITIES-IMPLEMENT-REQUIRED-ARINC-665-CA-CRS-M1-00191` |
| `CRS-M1-00192` | DATA-CONSTRAINT | `OBJ-ARINC-665-SHOULD-MODALITY-TREAT-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY-CRS-M1-00192` |
| `CRS-M1-00193` | DATA-CONSTRAINT | `OBJ-ARINC-665-MAY-MODALITY-TREAT-MAY-AS-OPTIONAL-CAPABILITY-CRS-M1-00193` |
| `CRS-M1-00194` | DATA-CONSTRAINT | `OBJ-OPTIONAL-ARINC-665-CAPABILITY-CONDITIONALLY-IMPLEMENT-OPTIONAL-CAPABILITY-AS-CRS-M1-00194` |
| `CRS-M1-00195` | DATA-CONSTRAINT | `OBJ-DATA-FIELD-TYPE-INTERPRET-FIELDS-AS-NUMERIC-BY-DEFAULT-CRS-M1-00195` |
| `CRS-M1-00196` | DATA-CONSTRAINT | `OBJ-ARINC-665-FILE-PROHIBIT-UNDEFINED-FIELD-INSERTION-CRS-M1-00196` |
| `CRS-M1-00197` | DATA-CONSTRAINT | `OBJ-FILE-VERSION-COMPATIBILITY-ENCODE-CRS-M1-00197` |
| `CRS-M1-00198` | DATA-CONSTRAINT | `OBJ-TARGET-HARDWARE-ID-MANUFACTURER-IDENTIFIER-PREFIX-TARGET-HARDWARE-ID-WITH-MA-CRS-M1-00198` |
| `CRS-M1-00199` | DATA-CONSTRAINT | `OBJ-MANUFACTURER-IDENTIFIER-ASSIGN-CRS-M1-00199` |
| `CRS-M1-00200` | DATA-CONSTRAINT | `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ASSIGN-GENERIC-TARGET-HARDWARE-ID-CRS-M1-00200` |
| `CRS-M1-00201` | DATA-CONSTRAINT | `OBJ-REDUNDANT-CHANNEL-LOADS-DISTRIBUTE-REDUNDANT-LOADS-INTERNALLY-CRS-M1-00201` |
| `CRS-M1-00202` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-ENSURE-CARDINALITY-CRS-M1-00202` |
| `CRS-M1-00203` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-COORDINATE-CRS-M1-00203` |
| `CRS-M1-00204` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-ASSIGN-CRS-M1-00204` |
| `CRS-M1-00205` | DATA-CONSTRAINT | `OBJ-LOADABLE-SOFTWARE-PART-NUMBER-FORMAT-CRS-M1-00205` |
| `CRS-M1-00206` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-EXCLUDE-EMBEDDED-BLANKS-CRS-M1-00206` |
| `CRS-M1-00207` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-DO-NOT-ENFORCE-SPECIFIC-PART-NUMBER-FORMAT-CRS-M1-00207` |
| `CRS-M1-00208` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-PROCESS-NONCONFORMING-PART-NUMBER-FORMATS-CRS-M1-00208` |
| `CRS-M1-00209` | DATA-CONSTRAINT | `OBJ-NETWORK-INTERFACE-DESIGN-CRS-M1-00209` |
| `CRS-M1-00210` | DATA-CONSTRAINT | `OBJ-NETWORK-INTERFACE-FORMAT-CRS-M1-00210` |
| `CRS-M1-00211` | DATA-CONSTRAINT | `OBJ-ATA-PART-NUMBER-DELIMITERS-SEPARATE-DELIMITERS-FROM-LETTERS-CRS-M1-00211` |
| `CRS-M1-00212` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-ENCODE-CRS-M1-00212` |
| `CRS-M1-00213` | DATA-CONSTRAINT | `OBJ-ATA-PART-NUMBER-CHARACTER-SET-EXCLUDE-AMBIGUOUS-LETTER-O-CRS-M1-00213` |
| `CRS-M1-00214` | DATA-CONSTRAINT | `OBJ-MMM-CODE-INTERPRET-CONFUSED-MMM-CHARACTERS-AS-ALPHABETIC-CRS-M1-00214` |
| `CRS-M1-00215` | DATA-CONSTRAINT | `OBJ-CHECK-CHARACTERS-COMPUTE-CRS-M1-00215` |
| `CRS-M1-00216` | DATA-CONSTRAINT | `OBJ-HEADER-FILE-SOFTWARE-PART-FORMAT-CRS-M1-00216` |
| `CRS-M1-00217` | DATA-CONSTRAINT | `OBJ-HEADER-FILE-SOFTWARE-PART-ENCODE-CRS-M1-00217` |
| `CRS-M1-00218` | DATA-CONSTRAINT | `OBJ-HEADER-FILE-DEFINE-CRS-M1-00218` |
| `CRS-M1-00219` | DATA-CONSTRAINT | `OBJ-BINARY-FIELD-ENCODING-ENCODE-CRS-M1-00219` |
| `CRS-M1-00220` | DATA-CONSTRAINT | `OBJ-OPERATION-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00220` |
| `CRS-M1-00221` | DATA-CONSTRAINT | `OBJ-BINARY-FIELD-ENCODING-ENCODE-CRS-M1-00221` |
| `CRS-M1-00222` | DATA-CONSTRAINT | `OBJ-TARGET-HARDWARE-ID-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00222` |
| `CRS-M1-00223` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-IMPLEMENT-CRS-M1-00223` |
| `CRS-M1-00224` | DATA-CONSTRAINT | `OBJ-NETWORK-INTERFACE-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00224` |
| `CRS-M1-00225` | DATA-CONSTRAINT | `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ENSURE-UNIQUE-CRS-M1-00225` |
| `CRS-M1-00226` | DATA-CONSTRAINT | `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ENCODE-CRS-M1-00226` |
| `CRS-M1-00227` | DATA-CONSTRAINT | `OBJ-TARGET-HARDWARE-ID-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00227` |
| `CRS-M1-00228` | DATA-CONSTRAINT | `OBJ-DATA-FILE-CONSTRAIN-CRS-M1-00228` |
| `CRS-M1-00229` | DATA-CONSTRAINT | `OBJ-DATA-FILE-SET-ZERO-CRS-M1-00229` |
| `CRS-M1-00230` | DATA-CONSTRAINT | `OBJ-DATA-FILE-FORMAT-CRS-M1-00230` |
| `CRS-M1-00231` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00232` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00233` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00234` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00235` | DATA-CONSTRAINT | `OBJ-NETWORK-INTERFACE-ENCODE-CRS-M1-00235` |
| `CRS-M1-00236` | DATA-CONSTRAINT | `OBJ-NETWORK-INTERFACE-IMPLEMENT-CRS-M1-00236` |
| `CRS-M1-00237` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-NETWORK-INTERFACE-ENCODE-CRS-M1-00237` |
| `CRS-M1-00238` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00239` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00240` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00241` | DATA-CONSTRAINT | `OBJ-HEADER-FILE-VALIDATE-CRS-M1-00241` |
| `CRS-M1-00242` | DATA-CONSTRAINT | `OBJ-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00242` |
| `CRS-M1-00243` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00244` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00245` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00246` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00247` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00248` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00249` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00250` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00251` | DATA-CONSTRAINT | `OBJ-DATA-FILE-SOFTWARE-PART-ENCODE-CRS-M1-00251` |
| `CRS-M1-00252` | DATA-CONSTRAINT | `OBJ-SOFTWARE-PART-NETWORK-INTERFACE-ENCODE-CRS-M1-00252` |
| `CRS-M1-00253` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00254` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00255` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00256` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00257` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00258` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00259` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00260` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00261` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00262` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00263` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00264` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00265` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00266` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00267` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00268` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00269` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00270` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00271` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00272` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00273` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00274` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00275` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00276` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00277` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00278` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00279` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00280` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00281` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00282` | DATA-CONSTRAINT | `FC-LCI-FIELD-FILE-LENGTH` |
| `CRS-M1-00283` | DATA-CONSTRAINT | `FC-LCI-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00284` | DATA-CONSTRAINT | `FC-LCI-FIELD-OPERATION-ACCEPTANCE-STATUS-CODE` |
| `CRS-M1-00285` | DATA-CONSTRAINT | `FC-LCI-FIELD-STATUS-DESCRIPTION-LENGTH` |
| `CRS-M1-00286` | DATA-CONSTRAINT | `FC-LCI-FIELD-STATUS-DESCRIPTION` |
| `CRS-M1-00287` | DATA-CONSTRAINT | `FC-LCL-FIELD-FILE-LENGTH` |
| `CRS-M1-00288` | DATA-CONSTRAINT | `FC-LCL-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00289` | DATA-CONSTRAINT | `FC-LCL-FIELD-NUMBER-OF-TARGET-HARDWARE` |
| `CRS-M1-00290` | DATA-CONSTRAINT | `FC-LCL-FIELD-LITERAL-NAME-LENGTH` |
| `CRS-M1-00291` | DATA-CONSTRAINT | `FC-LCL-FIELD-LITERAL-NAME` |
| `CRS-M1-00292` | DATA-CONSTRAINT | `FC-LCL-FIELD-SERIAL-NUMBER-LENGTH` |
| `CRS-M1-00293` | DATA-CONSTRAINT | `FC-LCL-FIELD-SERIAL-NUMBER` |
| `CRS-M1-00294` | DATA-CONSTRAINT | `FC-LCL-FIELD-NUMBER-OF-PART-NUMBERS` |
| `CRS-M1-00295` | DATA-CONSTRAINT | `FC-LCL-FIELD-PART-NUMBER-LENGTH` |
| `CRS-M1-00296` | DATA-CONSTRAINT | `FC-LCL-FIELD-PART-NUMBER` |
| `CRS-M1-00297` | DATA-CONSTRAINT | `FC-LCL-FIELD-AMENDMENT-LENGTH` |
| `CRS-M1-00298` | DATA-CONSTRAINT | `FC-LCL-FIELD-AMENDMENT` |
| `CRS-M1-00299` | DATA-CONSTRAINT | `FC-LCL-FIELD-PART-DESIGNATION-LENGTH` |
| `CRS-M1-00300` | DATA-CONSTRAINT | `FC-LCL-FIELD-PART-DESIGNATION-TEXT` |
| `CRS-M1-00301` | DATA-CONSTRAINT | `FC-LCS-FIELD-FILE-LENGTH` |
| `CRS-M1-00302` | DATA-CONSTRAINT | `FC-LCS-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00303` | DATA-CONSTRAINT | `FC-LCS-FIELD-COUNTER` |
| `CRS-M1-00304` | DATA-CONSTRAINT | `FC-LCS-FIELD-INFORMATION-OPERATION-STATUS-CODE` |
| `CRS-M1-00305` | DATA-CONSTRAINT | `FC-LCS-FIELD-EXCEPTION-TIMER`, `TIM-CRS-M1-00305`, `CLK_EXCEPTION` |
| `CRS-M1-00306` | DATA-CONSTRAINT | `FC-LCS-FIELD-ESTIMATED-TIME` |
| `CRS-M1-00307` | DATA-CONSTRAINT | `FC-LCS-FIELD-STATUS-DESCRIPTION-LENGTH` |
| `CRS-M1-00308` | DATA-CONSTRAINT | `FC-LCS-FIELD-STATUS-DESCRIPTION` |
| `CRS-M1-00309` | DATA-CONSTRAINT | `FC-LUR-FIELD-FILE-LENGTH` |
| `CRS-M1-00310` | DATA-CONSTRAINT | `FC-LUR-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00311` | DATA-CONSTRAINT | `FC-LUR-FIELD-NUMBER-OF-HEADER-FILES` |
| `CRS-M1-00312` | DATA-CONSTRAINT | `FC-LUR-FIELD-HEADER-FILE-NAME-LENGTH` |
| `CRS-M1-00313` | DATA-CONSTRAINT | `FC-LUR-FIELD-HEADER-FILE-NAME` |
| `CRS-M1-00314` | DATA-CONSTRAINT | `FC-LUR-FIELD-LOAD-PART-NUMBER-NAME-LENGTH` |
| `CRS-M1-00315` | DATA-CONSTRAINT | `FC-LUR-FIELD-LOAD-PART-NUMBER-NAME` |
| `CRS-M1-00316` | DATA-CONSTRAINT | `FC-LUS-FIELD-FILE-LENGTH` |
| `CRS-M1-00317` | DATA-CONSTRAINT | `FC-LUS-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00318` | DATA-CONSTRAINT | `FC-LUS-FIELD-UPLOAD-OPERATION-STATUS-CODE` |
| `CRS-M1-00319` | DATA-CONSTRAINT | `FC-LUS-FIELD-UPLOAD-STATUS-DESCRIPTION-LENGTH` |
| `CRS-M1-00320` | DATA-CONSTRAINT | `FC-LUS-FIELD-UPLOAD-STATUS-DESCRIPTION` |
| `CRS-M1-00321` | DATA-CONSTRAINT | `FC-LUS-FIELD-COUNTER` |
| `CRS-M1-00322` | DATA-CONSTRAINT | `FC-LUS-FIELD-EXCEPTION-TIMER`, `TIM-CRS-M1-00322`, `CLK_EXCEPTION` |
| `CRS-M1-00323` | DATA-CONSTRAINT | `FC-LUS-FIELD-ESTIMATED-TIME` |
| `CRS-M1-00324` | DATA-CONSTRAINT | `FC-LUS-FIELD-LOAD-LIST-RATIO` |
| `CRS-M1-00325` | DATA-CONSTRAINT | `FC-LUS-FIELD-NUMBER-OF-HEADER-FILES` |
| `CRS-M1-00326` | DATA-CONSTRAINT | `FC-LUS-FIELD-HEADER-FILE-NAME-LENGTH` |
| `CRS-M1-00327` | DATA-CONSTRAINT | `FC-LUS-FIELD-HEADER-FILE-NAME` |
| `CRS-M1-00328` | DATA-CONSTRAINT | `FC-LUS-FIELD-LOAD-PART-NUMBER-NAME-LENGTH` |
| `CRS-M1-00329` | DATA-CONSTRAINT | `FC-LUS-FIELD-LOAD-PART-NUMBER-NAME` |
| `CRS-M1-00330` | DATA-CONSTRAINT | `FC-LUS-FIELD-LOAD-RATIO` |
| `CRS-M1-00331` | DATA-CONSTRAINT | `FC-LUS-FIELD-LOAD-STATUS` |
| `CRS-M1-00332` | DATA-CONSTRAINT | `FC-LUS-FIELD-LOAD-STATUS-DESCRIPTION-LENGTH` |
| `CRS-M1-00333` | DATA-CONSTRAINT | `FC-LUS-FIELD-LOAD-STATUS-DESCRIPTION` |
| `CRS-M1-00334` | DATA-CONSTRAINT | `ST-CRS-M1-00334` |
| `CRS-M1-00335` | DATA-CONSTRAINT | `ST-CRS-M1-00335` |
| `CRS-M1-00336` | DATA-CONSTRAINT | `ST-CRS-M1-00336` |
| `CRS-M1-00337` | DATA-CONSTRAINT | `ST-CRS-M1-00337` |
| `CRS-M1-00338` | DATA-CONSTRAINT | `ST-CRS-M1-00338` |
| `CRS-M1-00339` | DATA-CONSTRAINT | `ST-CRS-M1-00339` |
| `CRS-M1-00340` | DATA-CONSTRAINT | `ST-CRS-M1-00340`, `T_ABORT_TH`, `T_ABORTED` |
| `CRS-M1-00341` | DATA-CONSTRAINT | `ST-CRS-M1-00341`, `T_ABORT_DL`, `T_ABORTED`, `T_ABORT_FROM_S_INF_LCI_RRQ`, `T_ABORT_FROM_S_INF_LCL_XFER`, `T_ABORT_FROM_S_INF_LCS_XFER`, `T_ABORT_FROM_S_INF_EXCEPTION`, `T_ABORT_FROM_S_WAIT_RETRY`, `T_ABORT_FROM_S_UPL_LUI_XFER`, `T_ABORT_FROM_S_UPL_LIST_SENT`, `T_ABORT_FROM_S_UPL_WAIT_LUS0001`, `T_ABORT_FROM_S_UPL_LUR_XFER`, `T_ABORT_FROM_S_UPL_LUS_XFER` |
| `CRS-M1-00342` | DATA-CONSTRAINT | `ST-CRS-M1-00342` |
| `CRS-M1-00343` | DATA-CONSTRAINT | `ST-CRS-M1-00343` |
| `CRS-M1-00344` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00345` | DATA-CONSTRAINT | `ST-CRS-M1-00345` |
| `CRS-M1-00346` | MODELED | `T_INF_LCI_RRQ` |
| `CRS-M1-00347` | MODELED | `T_INF_LCI_RRQ` |
| `CRS-M1-00348` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00349` | MODELED | `T_INF_EVAL`, `T_INF_ACCEPT_INIT` |
| `CRS-M1-00350` | MODELED | `T_INF_REJECT` |
| `CRS-M1-00351` | MODELED | `T_INF_LCL_WRQ`, `T_INF_ACCEPT_INIT` |
| `CRS-M1-00352` | MODELED | `T_INF_LCL_ACK` |
| `CRS-M1-00353` | MODELED | `T_INF_LCL_XFER` |
| `CRS-M1-00354` | MODELED | `T_INF_APP` |
| `CRS-M1-00355` | MODELED | `T_INF_LCS_WRQ` |
| `CRS-M1-00356` | MODELED | `T_INF_LCS_XFER` |
| `CRS-M1-00357` | MODELED | `T_INF_LCS_XFER` |
| `CRS-M1-00358` | MODELED | `T_INF_LCS_XFER`, `T_INF_SESSION_END` |
| `CRS-M1-00359` | MODELED | `T_UPL_LUI_RRQ` |
| `CRS-M1-00360` | MODELED | `T_UPL_LUI_RRQ`, `T_UPL_LUI_RRQ_AFTER_INF` |
| `CRS-M1-00361` | MODELED | `T_UPL_LUI_XFER` |
| `CRS-M1-00362` | MODELED | `T_UPL_EVAL`, `T_UPL_ACCEPT_INIT`, `T_UPL_REJECT` |
| `CRS-M1-00363` | MODELED | `T_UPL_ACCEPT_INIT`, `T_UPL_LIST_OFFER` |
| `CRS-M1-00364` | MODELED | `T_UPL_LIST_OFFER`, `T_UPL_WAIT_LUS0001` |
| `CRS-M1-00365` | MODELED | `T_UPL_LUR_WRQ` |
| `CRS-M1-00366` | MODELED | `T_UPL_LUR_ACK` |
| `CRS-M1-00367` | MODELED | `T_UPL_LUR_XFER` |
| `CRS-M1-00368` | MODELED | `T_UPL_FILE_RRQ`, `T_UPL_FILE_RRQ_MORE` |
| `CRS-M1-00369` | MODELED | `T_UPL_FILE_UNAVAIL` |
| `CRS-M1-00370` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00371` | MODELED | `T_UPL_FILE_STATUS` |
| `CRS-M1-00372` | MODELED | `T_UPL_MORE_FILES`, `T_UPL_FILE_RRQ_MORE` |
| `CRS-M1-00373` | MODELED | `T_UPL_TO_LUS` |
| `CRS-M1-00374` | MODELED | `T_UPL_LUS_XFER` |
| `CRS-M1-00375` | MODELED | `T_UPL_STATUS_APP` |
| `CRS-M1-00376` | MODELED | `T_UPL_COMPLETE`, `T_UPL_STATUS_REPEAT` |
| `CRS-M1-00377` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00378` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00379` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00380` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00381` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00382` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00383` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00384` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00385` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00386` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00387` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00388` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00389` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00390` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00391` | SCOPE-CONSTRAINT | `SCOPE`, `TIM-CRS-M1-00391`, `CLK_FIND` |
| `CRS-M1-00392` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00393` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00394` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00395` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00396` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00397` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00398` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00399` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00400` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00401` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00402` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00403` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00404` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00405` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00406` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00407` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00408` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00409` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00410` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00411` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00412` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00413` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00414` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00415` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00416` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00417` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00418` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00419` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00420` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00421` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00422` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00423` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00424` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00426` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00427` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00428` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00429` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00430` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00431` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00432` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00433` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00434` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00435` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00436` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00437` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00438` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00439` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00440` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00441` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00442` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00443` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00444` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00445` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00446` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00447` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00448` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00449` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00450` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00451` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00452` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00453` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00454` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00455` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00456` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00457` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00458` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00459` | DATA-CONSTRAINT | `FC-LNR-FIELD-FILE-LENGTH` |
| `CRS-M1-00460` | DATA-CONSTRAINT | `FC-LNR-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00461` | DATA-CONSTRAINT | `FC-LNR-FIELD-NUMBER-OF-FILES` |
| `CRS-M1-00462` | DATA-CONSTRAINT | `FC-LNR-FIELD-FILE-NAME-LENGTH` |
| `CRS-M1-00463` | DATA-CONSTRAINT | `FC-LNR-FIELD-FILE-NAME` |
| `CRS-M1-00464` | DATA-CONSTRAINT | `FC-LNR-FIELD-USER-DEFINED-DATA-LENGTH` |
| `CRS-M1-00465` | DATA-CONSTRAINT | `FC-LNR-FIELD-USER-DEFINED-DATA` |
| `CRS-M1-00466` | DATA-CONSTRAINT | `FC-LNS-FIELD-FILE-LENGTH` |
| `CRS-M1-00467` | DATA-CONSTRAINT | `FC-LNS-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00468` | DATA-CONSTRAINT | `FC-LNS-FIELD-DOWNLOAD-OPERATION-STATUS-CODE` |
| `CRS-M1-00469` | DATA-CONSTRAINT | `FC-LNS-FIELD-DOWNLOAD-STATUS-DESCRIPTION-LENGTH` |
| `CRS-M1-00470` | DATA-CONSTRAINT | `FC-LNS-FIELD-DOWNLOAD-STATUS-DESCRIPTION` |
| `CRS-M1-00471` | DATA-CONSTRAINT | `FC-LNS-FIELD-COUNTER` |
| `CRS-M1-00472` | DATA-CONSTRAINT | `FC-LNS-FIELD-EXCEPTION-TIMER` |
| `CRS-M1-00473` | DATA-CONSTRAINT | `FC-LNS-FIELD-ESTIMATED-TIME` |
| `CRS-M1-00474` | DATA-CONSTRAINT | `FC-LNS-FIELD-DOWNLOAD-LIST-RATIO` |
| `CRS-M1-00475` | DATA-CONSTRAINT | `FC-LNS-FIELD-NUMBER-OF-FILES` |
| `CRS-M1-00476` | DATA-CONSTRAINT | `FC-LNS-FIELD-FILE-NAME-LENGTH` |
| `CRS-M1-00477` | DATA-CONSTRAINT | `FC-LNS-FIELD-FILE-NAME` |
| `CRS-M1-00478` | DATA-CONSTRAINT | `FC-LNS-FIELD-FILE-STATUS` |
| `CRS-M1-00479` | DATA-CONSTRAINT | `FC-LNS-FIELD-FILE-STATUS-DESCRIPTION-LENGTH` |
| `CRS-M1-00480` | DATA-CONSTRAINT | `FC-LNS-FIELD-FILE-STATUS-DESCRIPTION` |
| `CRS-M1-00481` | DATA-CONSTRAINT | `FC-LNL-FIELD-FILE-LENGTH` |
| `CRS-M1-00482` | DATA-CONSTRAINT | `FC-LNL-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00483` | DATA-CONSTRAINT | `FC-LNL-FIELD-NUMBER-OF-FILES` |
| `CRS-M1-00484` | DATA-CONSTRAINT | `FC-LNL-FIELD-FILE-NAME-LENGTH` |
| `CRS-M1-00485` | DATA-CONSTRAINT | `FC-LNL-FIELD-FILE-NAME` |
| `CRS-M1-00486` | DATA-CONSTRAINT | `FC-LNL-FIELD-FILE-DESCRIPTION-LENGTH` |
| `CRS-M1-00487` | DATA-CONSTRAINT | `FC-LNL-FIELD-FILE-DESCRIPTION` |
| `CRS-M1-00488` | DATA-CONSTRAINT | `FC-LNA-FIELD-FILE-LENGTH` |
| `CRS-M1-00489` | DATA-CONSTRAINT | `FC-LNA-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00490` | DATA-CONSTRAINT | `FC-LNA-FIELD-NUMBER-OF-FILES` |
| `CRS-M1-00491` | DATA-CONSTRAINT | `FC-LNA-FIELD-FILE-NAME-LENGTH` |
| `CRS-M1-00492` | DATA-CONSTRAINT | `FC-LNA-FIELD-FILE-NAME` |
| `CRS-M1-00493` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00494` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00495` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00496` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00497` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00498` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00499` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00500` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00501` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00502` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00503` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00504` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00505` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00506` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00507` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00508` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00509` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00510` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00511` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00512` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00513` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00514` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00515` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00516` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00517` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00518` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00519` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00520` | SCOPE-CONSTRAINT | `SCOPE`, `TIM-CRS-M1-00520`, `CLK_FIND` |
| `CRS-M1-00521` | SCOPE-CONSTRAINT | `SCOPE`, `TIM-CRS-M1-00521`, `CLK_FIND` |
| `CRS-M1-00522` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00523` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00524` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00525` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00526` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-MAY-USE-BATCH-FILE-FORMAT-CRS-M1-00526` |
| `CRS-M1-00527` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-LET-BATCH-FILE-SELECT-LSPS-PER-TARGET-HW-POSITION-CRS-M1-00527` |
| `CRS-M1-00528` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-IDENTIFY-BATCH-FILE-WITH-LUB-EXTENSION-CRS-M1-00528` |
| `CRS-M1-00529` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-MATCH-REFERENCED-HEADER-FILE-NAME-CASE-CRS-M1-00529` |
| `CRS-M1-00530` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-PREFIX-BATCH-FILE-NAME-WITH-MANUFACTURER-CODE-CRS-M1-00530` |
| `CRS-M1-00531` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-BATCH-FILE-NAME-UNIQUE-PER-MANUFACTURER-CODE-CRS-M1-00531` |
| `CRS-M1-00532` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-BATCH-FILE-PART-NUMBER-UNIQUE-AMONG-LSP-AND-BFP-CRS-M1-00532` |
| `CRS-M1-00533` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-REFERENCE-COMPLETE-HEADER-FILE-NAME-WITHOUT-PATH-CRS-M1-00533` |
| `CRS-M1-00534` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-USE-BATCH-FILE-ONLY-TO-AUTOMATE-MULTI-LSP-SETUP-CRS-M1-00534` |
| `CRS-M1-00535` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-DO-NOT-TRANSFER-BATCH-FILE-TO-TARGET-HARDWARE-CRS-M1-00535` |
| `CRS-M1-00536` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-INCLUDE-BATCH-FILE-CONTENT-DEFINED-BY-TABLE-2-3-1-1-CRS-M1-00536` |
| `CRS-M1-00537` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-BATCH-FILE-LENGTH-IN-16-BIT-WORDS-CRS-M1-00537` |
| `CRS-M1-00538` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-MAKE-BATCH-FILE-PN-COMPLIANT-WITH-SOFTWARE-LOAD-PN-FORMAT-CRS-M1-00538` |
| `CRS-M1-00539` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-BATCH-FILE-PN-DISTINCT-FROM-LSP-AND-MSP-CRS-M1-00539` |
| `CRS-M1-00540` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-SET-LAST-LOAD-LIST-BLOCK-POINTER-TO-ZERO-CRS-M1-00540` |
| `CRS-M1-00541` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-MATCH-TARGET-HW-ID-POS-TO-TARGET-HARDWARE-CRS-M1-00541` |
| `CRS-M1-00542` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-MATCH-HEADER-FILE-NAME-TO-LISTED-LSP-CRS-M1-00542` |
| `CRS-M1-00543` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-MATCH-LOAD-PN-TO-LSP-FOR-TARGET-HW-ID-POS-CRS-M1-00543` |
| `CRS-M1-00544` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00545` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00546` | DATA-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-LENGTH` |
| `CRS-M1-00547` | DATA-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-FORMAT-VERSION` |
| `CRS-M1-00548` | DATA-CONSTRAINT | `FC-LUB-FIELD-SPARE` |
| `CRS-M1-00549` | DATA-CONSTRAINT | `FC-LUB-FIELD-POINTER-TO-BATCH-FILE-PN-LENGTH` |
| `CRS-M1-00550` | DATA-CONSTRAINT | `FC-LUB-FIELD-POINTER-TO-NUMBER-OF-TARGET-HW-ID-LOAD-LIST-BLOCKS` |
| `CRS-M1-00551` | DATA-CONSTRAINT | `FC-LUB-FIELD-EXPANSION-POINT-1` |
| `CRS-M1-00552` | DATA-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-PN-LENGTH` |
| `CRS-M1-00553` | DATA-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-PN` |
| `CRS-M1-00554` | DATA-CONSTRAINT | `FC-LUB-FIELD-COMMENT-LENGTH` |
| `CRS-M1-00555` | DATA-CONSTRAINT | `FC-LUB-FIELD-COMMENT` |
| `CRS-M1-00556` | DATA-CONSTRAINT | `FC-LUB-FIELD-EXPANSION-POINT-2` |
| `CRS-M1-00557` | DATA-CONSTRAINT | `FC-LUB-FIELD-NUMBER-OF-TARGET-HW-ID-LOAD-LIST-BLOCKS` |
| `CRS-M1-00558` | DATA-CONSTRAINT | `FC-LUB-FIELD-POINTER-TO-NEXT-TARGET-HW-ID-LOAD-LIST-BLOCK` |
| `CRS-M1-00559` | DATA-CONSTRAINT | `FC-LUB-FIELD-TARGET-HW-ID-POS-LENGTH` |
| `CRS-M1-00560` | DATA-CONSTRAINT | `FC-LUB-FIELD-TARGET-HW-ID-POS` |
| `CRS-M1-00561` | DATA-CONSTRAINT | `FC-LUB-FIELD-NUMBER-OF-LOADS-FOR-TARGET-HW-ID-POS` |
| `CRS-M1-00562` | DATA-CONSTRAINT | `FC-LUB-FIELD-HEADER-FILE-NAME-LENGTH` |
| `CRS-M1-00563` | DATA-CONSTRAINT | `FC-LUB-FIELD-HEADER-FILE-NAME` |
| `CRS-M1-00564` | DATA-CONSTRAINT | `FC-LUB-FIELD-LOAD-PN-LENGTH` |
| `CRS-M1-00565` | DATA-CONSTRAINT | `FC-LUB-FIELD-LOAD-PN` |
| `CRS-M1-00566` | DATA-CONSTRAINT | `FC-LUB-FIELD-EXPANSION-POINT-3` |
| `CRS-M1-00567` | DEPENDENCY-BLOCKED | `FC-LUB-FIELD-BATCH-FILE-CRC`, `IF_INTEGRITY` |
| `CRS-M1-00568` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-DEFINE-BATCH-FILE-FORMAT-VERSION-IN-16-BITS-CRS-M1-00568` |
| `CRS-M1-00569` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-TAKE-BATCH-FILE-FORMAT-VERSION-FROM-CLAUSE-1-4-1-CRS-M1-00569` |
| `CRS-M1-00570` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-USE-SPARE-TO-ALIGN-FOLLOWING-POINTERS-ON-4-BYTE-BOUNDARIES-CRS-M1-00570` |
| `CRS-M1-00571` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-POINT-TO-BATCH-FILE-PN-LENGTH-FROM-START-IN-16-BIT-WORDS-CRS-M1-00571` |
| `CRS-M1-00572` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-POINT-TO-LOAD-LIST-BLOCK-COUNT-FROM-START-IN-16-BIT-WORDS-CRS-M1-00572` |
| `CRS-M1-00573` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-MAY-GROW-FILE-FORMAT-AT-EXPANSION-POINTS-CRS-M1-00573` |
| `CRS-M1-00574` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-BATCH-FILE-PN-LENGTH-CRS-M1-00574` |
| `CRS-M1-00575` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-BATCH-FILE-PN-AS-8-BIT-ASCII-CRS-M1-00575` |
| `CRS-M1-00576` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-BATCH-FILE-PN-EVEN-OCTET-WIDTH-CRS-M1-00576` |
| `CRS-M1-00577` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-BATCH-FILE-PN-WITH-NUL-CRS-M1-00577` |
| `CRS-M1-00578` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-COMMENT-LENGTH-CRS-M1-00578` |
| `CRS-M1-00579` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-SET-COMMENT-LENGTH-ZERO-WHEN-NO-COMMENT-CRS-M1-00579` |
| `CRS-M1-00580` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-COMMENT-AS-8-BIT-ASCII-CRS-M1-00580` |
| `CRS-M1-00581` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-COMMENT-EVEN-OCTET-WIDTH-CRS-M1-00581` |
| `CRS-M1-00582` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-COMMENT-WITH-NUL-CRS-M1-00582` |
| `CRS-M1-00583` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-OMIT-COMMENT-FIELD-WHEN-COMMENT-LENGTH-ZERO-CRS-M1-00583` |
| `CRS-M1-00584` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-COUNT-TARGET-HW-ID-LOAD-LIST-BLOCKS-IN-BATCH-FILE-CRS-M1-00584` |
| `CRS-M1-00585` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-POINT-TO-NEXT-LOAD-LIST-BLOCK-IN-RELATIVE-16-BIT-WORDS-CRS-M1-00585` |
| `CRS-M1-00586` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-TARGET-HW-ID-POS-LENGTH-CRS-M1-00586` |
| `CRS-M1-00587` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-TARGET-HW-ID-POS-AS-8-BIT-ASCII-CRS-M1-00587` |
| `CRS-M1-00588` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-TARGET-HW-ID-POS-EVEN-OCTET-WIDTH-CRS-M1-00588` |
| `CRS-M1-00589` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-TARGET-HW-ID-POS-WITH-NUL-CRS-M1-00589` |
| `CRS-M1-00590` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-TARGET-HW-ID-POS-CONSISTENT-WITH-LISTED-LSP-HEADERS-CRS-M1-00590` |
| `CRS-M1-00591` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-COUNT-LOADS-IN-THE-TARGET-HW-ID-LOAD-LIST-BLOCK-CRS-M1-00591` |
| `CRS-M1-00592` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-HEADER-FILE-NAME-LENGTH-CRS-M1-00592` |
| `CRS-M1-00593` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-HEADER-FILE-NAME-AS-8-BIT-ASCII-CRS-M1-00593` |
| `CRS-M1-00594` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-HEADER-FILE-NAME-EVEN-OCTET-WIDTH-CRS-M1-00594` |
| `CRS-M1-00595` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-HEADER-FILE-NAME-WITH-NUL-CRS-M1-00595` |
| `CRS-M1-00596` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-USE-HEADER-FILE-NAME-WITHOUT-PATH-CRS-M1-00596` |
| `CRS-M1-00597` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-HEADER-FILE-NAME-FREE-OF-BACKSLASH-CRS-M1-00597` |
| `CRS-M1-00598` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-INCLUDE-HEADER-FILE-NAME-EXTENSIONS-AND-DELIMITERS-CRS-M1-00598` |
| `CRS-M1-00599` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-DEFINE-LOAD-PN-LENGTH-AS-CHARACTER-COUNT-CRS-M1-00599` |
| `CRS-M1-00600` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-LOAD-PN-LENGTH-CRS-M1-00600` |
| `CRS-M1-00601` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-LOAD-PN-AS-8-BIT-ASCII-CRS-M1-00601` |
| `CRS-M1-00602` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-LOAD-PN-EVEN-OCTET-WIDTH-CRS-M1-00602` |
| `CRS-M1-00603` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-LOAD-PN-WITH-NUL-CRS-M1-00603` |
| `CRS-M1-00604` | DATA-CONSTRAINT | `OBJ-SUPPORTING-GIVE-664P3-PRECEDENCE-OVER-CONFLICTING-RFC-OPTIONS-CRS-M1-00604` |
| `CRS-M1-00605` | DATA-CONSTRAINT | `OBJ-SUPPORTING-GENERATE-AND-CHECK-UDP-CHECKSUM-CRS-M1-00605` |
| `CRS-M1-00606` | DATA-CONSTRAINT | `OBJ-SUPPORTING-IMPLEMENT-IPV4-IN-ACCORDANCE-WITH-P3-FIGURE-3-4-1-1-CRS-M1-00606` |
| `CRS-M1-00607` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-SECURE-RELIABLE-PARTITION-DATA-EXCHANGE-CRS-M1-00607` |
| `CRS-M1-00608` | DATA-CONSTRAINT | `OBJ-SUPPORTING-FILTER-AND-POLICE-FRAMES-FOR-INTEGRITY-LENGTH-BUDGET-AND-DESTINATION-CRS-M1-00608` |
| `CRS-M1-00609` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-AFDX-NOT-APPLICABLE-PROFILE-ITEMS-AS-MUST-NOT-CRS-M1-00609` |
| `CRS-M1-00610` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-UDP-LENGTH-TO-HEADER-PLUS-DATA-OCTETS-CRS-M1-00610` |
| `CRS-M1-00611` | DATA-CONSTRAINT | `OBJ-SUPPORTING-COMPUTE-UDP-CHECKSUM-OVER-PSEUDO-HEADER-HEADER-AND-DATA-CRS-M1-00611` |
| `CRS-M1-00612` | DATA-CONSTRAINT | `OBJ-SUPPORTING-IMPLEMENT-IPV4-ADDRESSING-AND-FRAGMENTATION-CRS-M1-00612` |
| `CRS-M1-00613` | DATA-CONSTRAINT | `OBJ-SUPPORTING-IMPLEMENT-IPV4-FRAGMENTATION-AND-REASSEMBLY-CRS-M1-00613` |
| `CRS-M1-00614` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SILENTLY-DISCARD-NON-IPV4-VERSION-CRS-M1-00614` |
| `CRS-M1-00615` | DATA-CONSTRAINT | `OBJ-SUPPORTING-GENERATE-AND-VALIDATE-UDP-CHECKSUMS-CRS-M1-00615` |
| `CRS-M1-00616` | DATA-CONSTRAINT | `OBJ-SUPPORTING-APPLY-RFC-1123-TFTP-HOST-NOTES-WITHOUT-ADOPTING-MAIL-NETASCII-OR-BROADCAST-RRQ-CRS-M1-00616` |
| `CRS-M1-00617` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-FIVE-TFTP-PACKET-TYPES-IDENTIFIED-BY-OPCODE-CRS-M1-00617` |
| `CRS-M1-00618` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ASSIGN-TID-ON-RRQ-OR-WRQ-WITHOUT-MAIL-MODE-CRS-M1-00618` |
| `CRS-M1-00619` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PLACE-OPCODE-IN-TFTP-HEADER-CRS-M1-00619` |
| `CRS-M1-00620` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TERMINATE-ON-DATA-PACKET-OF-0-TO-511-BYTES-CRS-M1-00620` |
| `CRS-M1-00621` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SEND-ERROR-PACKET-OPCODE-5-CRS-M1-00621` |
| `CRS-M1-00622` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ACKNOWLEDGE-OPTION-NEGOTIATION-WITH-OACK-CRS-M1-00622` |
| `CRS-M1-00623` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TERMINATE-TRANSFER-WITH-ERROR-CODE-8-CRS-M1-00623` |
| `CRS-M1-00624` | DATA-CONSTRAINT | `OBJ-SUPPORTING-APPEND-OPTIONS-TO-RRQ-OR-WRQ-CRS-M1-00624` |
| `CRS-M1-00625` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-BLKSIZE-AS-ASCII-OCTETS-FROM-8-THROUGH-65464-CRS-M1-00625` |
| `CRS-M1-00626` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-TIMEOUT-AS-ASCII-SECONDS-FROM-1-THROUGH-255-CRS-M1-00626` |
| `CRS-M1-00627` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUEST-TSIZE-ZERO-ON-RRQ-AND-RETURN-SIZE-IN-OACK-CRS-M1-00627` |
| `CRS-M1-00628` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-UDP-LENGTH-AT-LEAST-EIGHT-OCTETS-CRS-M1-00628` |
| `CRS-M1-00629` | DATA-CONSTRAINT | `OBJ-SUPPORTING-VERIFY-IP-HEADER-CHECKSUM-AND-SILENTLY-DISCARD-BAD-CRS-M1-00629` |
| `CRS-M1-00630` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SUPPORT-IPV4-REASSEMBLY-CRS-M1-00630` |
| `CRS-M1-00631` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SILENTLY-DISCARD-UDP-DATAGRAM-WITH-INVALID-CHECKSUM-CRS-M1-00631` |
| `CRS-M1-00632` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-RRQ-WRQ-AS-OPCODE-FILENAME-AND-MODE-CRS-M1-00632` |
| `CRS-M1-00633` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TERMINATE-TFTP-FILENAME-WITH-NUL-CRS-M1-00633` |
| `CRS-M1-00634` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-DATA-PACKET-WITH-BLOCK-NUMBER-AND-DATA-CRS-M1-00634` |
| `CRS-M1-00635` | DATA-CONSTRAINT | `OBJ-SUPPORTING-LIMIT-TFTP-DATA-FIELD-TO-ZERO-THROUGH-512-BYTES-CRS-M1-00635` |
| `CRS-M1-00636` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-ACK-PACKET-WITH-OPCODE-4-AND-BLOCK-NUMBER-CRS-M1-00636` |
| `CRS-M1-00637` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-ERROR-PACKET-AS-OPCODE-ERROR-CODE-AND-MESSAGE-CRS-M1-00637` |
| `CRS-M1-00638` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-BLKSIZE-VALUE-IN-ASCII-CRS-M1-00638` |
| `CRS-M1-00639` | DATA-CONSTRAINT | `OBJ-SUPPORTING-NEGOTIATE-BLKSIZE-LESS-OR-EQUAL-TO-CLIENT-VALUE-CRS-M1-00639` |
| `CRS-M1-00640` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-OACK-BLKSIZE-OR-TERMINATE-WITH-ERROR-8-CRS-M1-00640` |
| `CRS-M1-00641` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ECHO-CLIENT-TIMEOUT-VALUE-IN-OACK-CRS-M1-00641` |
| `CRS-M1-00642` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SPECIFY-TSIZE-ON-WRQ-AND-ECHO-IN-OACK-CRS-M1-00642` |
| `CRS-M1-00643` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MAY-ABORT-RRQ-WITH-ERROR-CODE-3-CRS-M1-00643` |
| `CRS-M1-00644` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MAY-ABORT-WRQ-WITH-ERROR-CODE-3-CRS-M1-00644` |
| `CRS-M1-00645` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TERMINATE-ON-DATA-SHORTER-THAN-NEGOTIATED-BLKSIZE-CRS-M1-00645` |
| `CRS-M1-00646` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SEND-ZERO-LENGTH-FINAL-DATA-WHEN-FILE-IS-INTEGRAL-MULTIPLE-OF-BLKSIZE-CRS-M1-00646` |
| `CRS-M1-00647` | DATA-CONSTRAINT | `OBJ-SUPPORTING-IGNORE-UNACKNOWLEDGED-OPTION-AND-KEEP-DEFAULT-PARAMETERS-CRS-M1-00647` |
| `CRS-M1-00648` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-VERSION-AS-4-BITS-CRS-M1-00648` |
| `CRS-M1-00649` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-IHL-AS-4-BITS-CRS-M1-00649` |
| `CRS-M1-00650` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-TOS-AS-8-BITS-CRS-M1-00650` |
| `CRS-M1-00651` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-TOTAL-LENGTH-AS-16-BITS-CRS-M1-00651` |
| `CRS-M1-00652` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-IDENTIFICATION-AS-16-BITS-CRS-M1-00652` |
| `CRS-M1-00653` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-FLAGS-AS-3-BITS-CRS-M1-00653` |
| `CRS-M1-00654` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-FRAGMENT-OFFSET-AS-13-BITS-CRS-M1-00654` |
| `CRS-M1-00655` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-TTL-AS-8-BITS-CRS-M1-00655` |
| `CRS-M1-00656` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-PROTOCOL-AS-8-BITS-CRS-M1-00656` |
| `CRS-M1-00657` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-HEADER-CHECKSUM-AS-16-BITS-CRS-M1-00657` |
| `CRS-M1-00658` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-SOURCE-ADDRESS-AS-32-BITS-CRS-M1-00658` |
| `CRS-M1-00659` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-DESTINATION-ADDRESS-AS-32-BITS-CRS-M1-00659` |
| `CRS-M1-00660` | DATA-CONSTRAINT | `OBJ-SUPPORTING-DO-NOT-SUPPORT-TFTP-MAIL-TRANSFER-MODE-CRS-M1-00660` |
| `CRS-M1-00661` | DATA-CONSTRAINT | `OBJ-SUPPORTING-COUNT-UDP-LENGTH-INCLUDING-EIGHT-OCTET-HEADER-CRS-M1-00661` |
| `CRS-M1-00662` | DATA-CONSTRAINT | `OBJ-SUPPORTING-NEVER-RESEND-CURRENT-DATA-ON-DUPLICATE-ACK-CRS-M1-00662` |
| `CRS-M1-00663` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-ADAPTIVE-TFTP-RETRANSMISSION-TIMEOUT-CRS-M1-00663` |
| `CRS-M1-00664` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-CONFIGURABLE-TFTP-PATHNAME-ACCESS-CONTROL-CRS-M1-00664` |
| `CRS-M1-00665` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SILENTLY-IGNORE-BROADCAST-TFTP-REQUEST-CRS-M1-00665` |
| `CRS-M1-00666` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ALLOW-ONLY-ONE-SOURCE-END-SYSTEM-PER-VL-CRS-M1-00666` |
| `CRS-M1-00667` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-VL-AS-UNIDIRECTIONAL-ONE-TO-MANY-CONNECTION-CRS-M1-00667` |
| `CRS-M1-00668` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-BAG-AS-MINIMUM-INTERVAL-BETWEEN-CONSECUTIVE-VL-FRAMES-CRS-M1-00668` |
| `CRS-M1-00669` | DATA-CONSTRAINT | `OBJ-SUPPORTING-BOUND-VL-FRAME-ARRIVAL-BY-MAXIMUM-ADMISSIBLE-JITTER-CRS-M1-00669` |
| `CRS-M1-00670` | DATA-CONSTRAINT | `OBJ-SUPPORTING-CHARACTERISE-VL-BANDWIDTH-BY-BAG-AND-LMAX-CRS-M1-00670` |
| `CRS-M1-00671` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ACCOMMODATE-VL-FRAMES-UP-TO-1518-BYTES-CRS-M1-00671` |
| `CRS-M1-00672` | DATA-CONSTRAINT | `OBJ-SUPPORTING-HANDLE-BAG-VALUES-FROM-1-MS-TO-128-MS-CRS-M1-00672` |
| `CRS-M1-00673` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RESTRICT-BAG-TO-POWERS-OF-TWO-MILLISECONDS-CRS-M1-00673` |
| `CRS-M1-00674` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-VL-JITTER-AT-OR-BELOW-500-MICROSECONDS-CRS-M1-00674` |
| `CRS-M1-00675` | DATA-CONSTRAINT | `OBJ-SUPPORTING-IDENTIFY-VL-ONLY-BY-MAC-DESTINATION-ADDRESS-CRS-M1-00675` |
| `CRS-M1-00676` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-IHL-IN-32-BIT-WORDS-CRS-M1-00676` |
| `CRS-M1-00677` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-IHL-AT-LEAST-5-CRS-M1-00677` |
| `CRS-M1-00678` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-IPV4-TOTAL-LENGTH-IN-OCTETS-INCLUDING-HEADER-AND-DATA-CRS-M1-00678` |
| `CRS-M1-00679` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-FRAGMENT-OFFSET-IN-8-OCTET-UNITS-CRS-M1-00679` |
| `CRS-M1-00680` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ALLOW-IPV4-OPTIONS-TO-BE-PRESENT-OR-ABSENT-CRS-M1-00680` |
| `CRS-M1-00681` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PAD-IPV4-HEADER-TO-32-BIT-BOUNDARY-CRS-M1-00681` |
| `CRS-M1-00682` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-TX-TECHNOLOGICAL-LATENCY-BELOW-150US-PLUS-FRAME-DELAY-CRS-M1-00682`, `TIM-CRS-M1-00682`, `CLK_AFDX_ES` |
| `CRS-M1-00683` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-RX-TECHNOLOGICAL-LATENCY-BELOW-150-MICROSECONDS-CRS-M1-00683`, `TIM-CRS-M1-00683`, `CLK_AFDX_ES` |
| `CRS-M1-00684` | DATA-CONSTRAINT | `OBJ-SUPPORTING-BOUND-MAX-JITTER-BY-40US-PLUS-VL-LOAD-TERM-CRS-M1-00684`, `TIM-CRS-M1-00684`, `CLK_AFDX_ES` |
| `CRS-M1-00685` | DATA-CONSTRAINT | `OBJ-SUPPORTING-BOUND-MAX-JITTER-BY-500-MICROSECONDS-EQUATION-CRS-M1-00685`, `TIM-CRS-M1-00685`, `CLK_AFDX_ES` |
| `CRS-M1-00686` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-MAC-SOURCE-AS-INDIVIDUAL-AND-LOCALLY-ADMINISTERED-CRS-M1-00686` |
| `CRS-M1-00687` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-SOURCE-CONSTANT-FIELD-TO-000000100000000000000000-CRS-M1-00687` |
| `CRS-M1-00688` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-SOURCE-INDIVIDUAL-ADDRESS-BIT-TO-ZERO-CRS-M1-00688` |
| `CRS-M1-00689` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-SOURCE-LOCALLY-ADMINISTERED-BIT-TO-ONE-CRS-M1-00689` |
| `CRS-M1-00690` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-MAC-SOURCE-USER-DEFINED-ID-AS-16-BITS-CRS-M1-00690` |
| `CRS-M1-00691` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-USER-DEFINED-ID-FOR-UNIQUE-MEANINGFUL-HOST-IDENTITY-CRS-M1-00691` |
| `CRS-M1-00692` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-INTERFACE-ID-TO-IDENTIFY-REDUNDANT-AFDX-NETWORK-CRS-M1-00692` |
| `CRS-M1-00693` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-INTERFACE-ID-001-AS-NETWORK-A-CRS-M1-00693` |
| `CRS-M1-00694` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-INTERFACE-ID-010-AS-NETWORK-B-CRS-M1-00694` |
| `CRS-M1-00695` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-ADN-ADDRESS-DETERMINATION-GUIDANCE-CRS-M1-00695` |
| `CRS-M1-00696` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KNOW-DESTINATION-ADDRESSES-AT-CONFIGURATION-TIME-CRS-M1-00696` |
| `CRS-M1-00697` | DATA-CONSTRAINT | `OBJ-SUPPORTING-DEFINE-ADN-ADDRESSING-PLAN-AND-RULES-CRS-M1-00697` |
| `CRS-M1-00698` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-IANA-WELL-KNOWN-UDP-PORTS-FOR-STANDARD-SERVICES-INCLUDING-TFTP-CRS-M1-00698` |
| `CRS-M1-00699` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ACCESS-PRIVATE-AERO-APPS-VIA-INTEGRATOR-OR-664P4-UDP-PORTS-CRS-M1-00699` |
| `CRS-M1-00700` | DATA-CONSTRAINT | `OBJ-SUPPORTING-DO-NOT-REASSIGN-WELL-KNOWN-COTS-PORTS-0-1023-CRS-M1-00700` |
| `CRS-M1-00701` | DATA-CONSTRAINT | `OBJ-SUPPORTING-DO-NOT-ROUTE-PRIVATE-ADDRESSES-OUTSIDE-THE-NETWORK-CRS-M1-00701` |
| `CRS-M1-00702` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-PROFILED-AERO-NETWORK-AS-IETF-PRIVATE-APPLICATION-CRS-M1-00702` |
| `CRS-M1-00703` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-PRIVATE-NETWORK-ID-FOR-PROFILED-NETWORKS-CRS-M1-00703` |
| `CRS-M1-00704` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ASSIGN-MAC-UNICAST-ADDRESSES-AT-CONFIGURATION-TIME-CRS-M1-00704` |
| `CRS-M1-00705` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-MAC-ADDRESSES-UNIQUE-UNDER-INTEGRATOR-SCHEME-CRS-M1-00705` |
| `CRS-M1-00706` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-UL-BIT-WHEN-INTEGRATOR-ASSIGNS-ADDRESSES-CRS-M1-00706` |
| `CRS-M1-00707` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-ALL-NETWORK-ADDRESSES-UNIQUE-CRS-M1-00707` |
| `CRS-M1-00708` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RESERVE-UDP-TCP-PORT-59-FOR-615A-DATA-LOADER-TFTP-CRS-M1-00708` |
| `CRS-M1-00709` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ASSIGN-UDP-PORT-24922-TO-FIND-PROTOCOL-CLIENT-CRS-M1-00709` |
| `CRS-M1-00710` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ALLOCATE-TABLE-2-1-ADDRESSES-FROM-RFC1918-PRIVATE-RANGES-CRS-M1-00710` |
| `CRS-M1-00711` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-TX-TECHNOLOGICAL-LATENCY-BETWEEN-PARTITION-DATA-AND-PHYSICAL-MEDIA-CRS-M1-00711` |
| `CRS-M1-00712` | DATA-CONSTRAINT | `OBJ-SUPPORTING-START-TX-TECHNOLOGICAL-LATENCY-WHEN-LAST-PARTITION-BIT-IS-AVAILABLE-CRS-M1-00712` |
| `CRS-M1-00713` | DATA-CONSTRAINT | `OBJ-SUPPORTING-END-TX-TECHNOLOGICAL-LATENCY-WHEN-LAST-FRAME-BIT-IS-ON-MEDIA-CRS-M1-00713` |
| `CRS-M1-00714` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-TX-TECHNOLOGICAL-LATENCY-WITH-EMPTY-BUFFERS-NO-CONTENTION-AND-NO-IP-FRAGMENTATION-CRS-M1-00714` |
| `CRS-M1-00715` | DATA-CONSTRAINT | `OBJ-SUPPORTING-DISTINGUISH-TECHNOLOGICAL-LATENCY-FROM-CONFIGURATION-LOAD-LATENCY-CRS-M1-00715` |
| `CRS-M1-00716` | DATA-CONSTRAINT | `OBJ-SUPPORTING-DEFINE-TECHNOLOGICAL-LATENCY-AS-ACCEPT-PROCESS-AND-BEGIN-TX-WITH-NO-OTHER-TASK-CRS-M1-00716` |
| `CRS-M1-00717` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ADD-FRAME-DELAY-FOR-PHYSICAL-LAYER-DELIVERY-CRS-M1-00717` |
| `CRS-M1-00718` | DATA-CONSTRAINT | `OBJ-SUPPORTING-START-RX-TECHNOLOGICAL-LATENCY-WHEN-LAST-FRAME-BIT-IS-RECEIVED-CRS-M1-00718` |
| `CRS-M1-00719` | DATA-CONSTRAINT | `OBJ-SUPPORTING-END-RX-TECHNOLOGICAL-LATENCY-WHEN-LAST-DATA-BIT-IS-AVAILABLE-TO-PARTITION-CRS-M1-00719` |
| `CRS-M1-00720` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-RX-TECHNOLOGICAL-LATENCY-WITH-EMPTY-BUFFERS-AND-NO-CONTENTION-CRS-M1-00720` |
| `CRS-M1-00721` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SATISFY-BOTH-MAX-JITTER-EQUATIONS-SIMULTANEOUSLY-CRS-M1-00721` |
| `CRS-M1-00722` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-MAX-JITTER-AS-MICROSECONDS-NBW-AS-BITS-PER-SECOND-AND-LMAX-AS-OCTETS-CRS-M1-00722` |
| `CRS-M1-00723` | DATA-CONSTRAINT | `OBJ-SUPPORTING-COMPOSE-MAC-SOURCE-AS-24-PLUS-16-PLUS-3-PLUS-5-BIT-FIELDS-CRS-M1-00723` |
| `CRS-M1-00724` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-SOURCE-CONSTANT-TAIL-TO-00000-CRS-M1-00724` |
| `CRS-M1-00725` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-MAC-SOURCE-CONSTRUCTION-ALGORITHM-AS-NOT-UNIQUELY-RECOMMENDED-CRS-M1-00725` |
| `CRS-M1-00726` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-000-AS-NOT-USED-CRS-M1-00726` |
| `CRS-M1-00727` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-011-AS-NOT-USED-CRS-M1-00727` |
| `CRS-M1-00728` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-100-AS-NOT-USED-CRS-M1-00728` |
| `CRS-M1-00729` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-101-AS-NOT-USED-CRS-M1-00729` |
| `CRS-M1-00730` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-110-AS-SOURCE-NOR-USED-CRS-M1-00730` |
| `CRS-M1-00731` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-111-AS-NOT-USED-CRS-M1-00731` |
| `CRS-M1-00732` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-P3-RFC-OPTION-RESTRICTION-PHILOSOPHY-CRS-M1-00732` |
| `CRS-M1-00733` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-P3-CONTENTS-LIMITED-TO-RFC-DELTAS-CRS-M1-00733` |
| `CRS-M1-00734` | DATA-CONSTRAINT | `OBJ-SUPPORTING-COMPOSE-AFDX-SWITCH-FROM-FIVE-FUNCTIONAL-BLOCKS-CRS-M1-00734` |
| `CRS-M1-00735` | DATA-CONSTRAINT | `OBJ-SUPPORTING-CONTROL-AFDX-SWITCH-FUNCTIONS-WITH-STATIC-CONFIGURATION-TABLES-CRS-M1-00735` |
| `CRS-M1-00736` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-SWITCH-END-SYSTEM-TO-COMPLY-WITH-SECTION-3-EXCEPT-REDUNDANCY-CRS-M1-00736` |
| `CRS-M1-00737` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-SWITCH-END-SYSTEM-UNICAST-MAC-AS-SOURCE-ADDRESS-CRS-M1-00737` |
| `CRS-M1-00738` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-615A-SESSION-ACROSS-OPS-TO-DL-TRANSITION-CRS-M1-00738` |
| `CRS-M1-00739` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-615A-AND-665-TO-UPLOAD-SWITCH-SOFTWARE-AND-CONFIGURATION-CRS-M1-00739` |
| `CRS-M1-00740` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-AFDX-SWITCH-PHYSICAL-LAYER-TO-COMPLY-WITH-664P2-CRS-M1-00740` |
| `CRS-M1-00741` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-AS-NOT-USED-ON-AFDX-CRS-M1-00741` |
| `CRS-M1-00742` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-CHECKSUM-GENERATE-AND-CHECK-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00742` |
| `CRS-M1-00743` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-AFDX-END-SYSTEM-INTERNET-LAYER-TO-IMPLEMENT-IP-CRS-M1-00743` |
| `CRS-M1-00744` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-AFDX-END-SYSTEM-INTERNET-LAYER-TO-IMPLEMENT-ICMP-CRS-M1-00744` |
| `CRS-M1-00745` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SILENTLY-DISCARD-NON-IPV4-DATAGRAMS-CRS-M1-00745` |
| `CRS-M1-00746` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-AFDX-UDP-CHECKSUM-UNUSED-COMMENT-CRS-M1-00746` |
| `CRS-M1-00747` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-SILENT-BAD-UDP-CHECKSUM-DISCARD-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00747` |
| `CRS-M1-00748` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PASS-ICMP-MESSAGES-TO-APPLICATION-LIMITED-TO-ECHO-REQUEST-CRS-M1-00748` |
| `CRS-M1-00749` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-PORT-UNREACHABLE-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00749` |
| `CRS-M1-00750` | DATA-CONSTRAINT | `OBJ-SUPPORTING-FORBID-REMOTE-MULTIHOMING-AT-APPLICATION-LAYER-ON-AFDX-CRS-M1-00750` |
| `CRS-M1-00751` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-LOCAL-MULTIHOMING-ON-AFDX-CRS-M1-00751` |
| `CRS-M1-00752` | DATA-CONSTRAINT | `OBJ-SUPPORTING-LOG-DISCARDED-DATAGRAMS-ON-AFDX-CRS-M1-00752` |
| `CRS-M1-00753` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-DISCARDED-DATAGRAMS-IN-COUNTER-ON-AFDX-CRS-M1-00753` |
| `CRS-M1-00754` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENTER-OPS-AFTER-COMPATIBLE-INIT-WHEN-SHOP-INACTIVE-CRS-M1-00754` |
| `CRS-M1-00755` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-OPS-MODE-615A-INFORMATION-AND-FIND-CRS-M1-00755` |
| `CRS-M1-00756` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENTER-DL-FROM-INIT-ONLY-WHEN-GROUND-AND-COMPATIBILITY-FAIL-OR-EMPTY-CRS-M1-00756` |
| `CRS-M1-00757` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENTER-DL-FROM-OPS-ONLY-WHEN-GROUND-UPLOAD-INIT-AND-HEADER-ACCEPTED-CRS-M1-00757` |
| `CRS-M1-00758` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-DL-MODE-615A-INFORMATION-UPLOAD-AND-FIND-CRS-M1-00758` |
| `CRS-M1-00759` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-SEND-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00759` |
| `CRS-M1-00760` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-DOWN-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00760` |
| `CRS-M1-00761` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-GATEWAY-FORWARDING-SPEC-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00761` |
| `CRS-M1-00762` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-EMBEDDED-GATEWAY-SWITCH-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00762` |
| `CRS-M1-00763` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-NON-GATEWAY-DEFAULT-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00763` |
| `CRS-M1-00764` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-AFDX-GATEWAY-AUTOCONFIGURATION-ROW-UNMARKED-CRS-M1-00764` |
| `CRS-M1-00765` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PERFORM-OPS-FILTERING-POLICING-SWITCHING-FROM-OPS-CONFIG-CRS-M1-00765` |
| `CRS-M1-00766` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-OPS-FAULT-HEALTHY-INDICATOR-TO-HEALTHY-CRS-M1-00766` |
| `CRS-M1-00767` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-DL-UPLOAD-AS-PREFERABLY-EXCLUSIVE-CRS-M1-00767` |
| `CRS-M1-00768` | DATA-CONSTRAINT | `OBJ-SUPPORTING-DEDICATE-SWITCH-TO-UPLOAD-DURING-DL-UPLOAD-CRS-M1-00768` |
| `CRS-M1-00769` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-DEFAULT-RECEPTION-VL-FOR-DATALOADING-CRS-M1-00769` |
| `CRS-M1-00770` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-TWELVE-PIN-POSITION-IDENTIFICATION-AS-EXAMPLE-CRS-M1-00770` |
| `CRS-M1-00771` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-STATED-TWELVE-PIN-DEFINITIONS-IF-TWELVE-PINS-CHOSEN-CRS-M1-00771` |
| `CRS-M1-00772` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-DEFAULT-CONFIGURATION-TABLE-RESIDENT-CRS-M1-00772` |
| `CRS-M1-00773` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-DEFAULT-PHYSICAL-PORT-SPEED-100MBPS-WITHOUT-AUTONEG-CRS-M1-00773` |
| `CRS-M1-00774` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-DEFAULT-RECEPTION-VL-FIELDS-IN-NONVOLATILE-MEMORY-CRS-M1-00774` |
| `CRS-M1-00775` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-DEFAULT-TRANSMISSION-VL-FIELDS-IN-NONVOLATILE-MEMORY-CRS-M1-00775` |
| `CRS-M1-00776` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-DEFAULT-TRANSMISSION-VL-FOR-DATALOADING-ACKNOWLEDGE-CRS-M1-00776` |
| `CRS-M1-00777` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-OPS-CONFIGURATION-FILE-615A-665-FIELD-LOADABLE-CRS-M1-00777` |
| `CRS-M1-00778` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-FILTERING-POLICING-FORWARDING-TABLE-PARAMETER-SET-CRS-M1-00778` |
| `CRS-M1-00779` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-LISTED-PARAMETERS-TO-CONFIGURE-FILTER-POLICE-FORWARD-CRS-M1-00779` |
| `CRS-M1-00780` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PERFORM-DL-END-SYSTEM-FROM-DEFAULT-CONFIGURATION-TABLE-CRS-M1-00780` |
| `CRS-M1-00781` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-DL-FAULT-HEALTHY-INDICATOR-TO-HEALTHY-CRS-M1-00781` |
| `CRS-M1-00782` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RETURN-TO-INIT-AT-END-OF-DL-MODE-CRS-M1-00782` |
| `CRS-M1-00783` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-DL-MODE-END-AS-615A-DATA-LOADING-FUNCTION-END-CRS-M1-00783` |
| `CRS-M1-00784` | DATA-CONSTRAINT | `OBJ-SUPPORTING-LIMIT-SWITCH-FIELD-LOADABLE-SOFTWARE-TO-OPS-CONFIG-AND-OPS-SOFTWARE-CRS-M1-00784` |
| `CRS-M1-00785` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-FIELD-LOADABLE-FILES-IDENTICAL-ACROSS-AIRCRAFT-SWITCHES-CRS-M1-00785` |
| `CRS-M1-00786` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MAKE-SWITCH-CONFIGURATION-ACCESSIBLE-VIA-615A-INFORMATION-CRS-M1-00786` |
| `CRS-M1-00787` | DATA-CONSTRAINT | `OBJ-SUPPORTING-LEARN-DATALOADER-IP-FROM-SOURCE-ADDRESS-CRS-M1-00787` |
| `CRS-M1-00788` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-PIN-PROGRAMMING-FOR-POSITION-AND-DEFAULT-MAC-IP-CRS-M1-00788` |
| `CRS-M1-00789` | DATA-CONSTRAINT | `OBJ-SUPPORTING-READ-PROGRAM-PINS-IN-INIT-ONLY-WHEN-GROUND-BEFORE-SAFETY-TEST-CRS-M1-00789` |
| `CRS-M1-00790` | DATA-CONSTRAINT | `OBJ-SUPPORTING-DO-NOT-READ-PROGRAM-PINS-WHEN-GROUND-CONDITION-FALSE-CRS-M1-00790` |
| `CRS-M1-00791` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-LAST-MEMORIZED-PIN-VALUES-WHEN-NOT-GROUND-CRS-M1-00791` |
| `CRS-M1-00792` | DATA-CONSTRAINT | `OBJ-SUPPORTING-CHECK-TWELVE-PROGRAM-PINS-WITH-PARITY-BIT-CRS-M1-00792` |
| `CRS-M1-00793` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MEMORIZE-PROGRAM-PINS-IN-NVM-AFTER-PARITY-PASS-CRS-M1-00793` |
| `CRS-M1-00794` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ACQUIRE-SWITCH-POSITION-WITH-TWELVE-PINS-P1-P12-CRS-M1-00794` |
| `CRS-M1-00795` | DATA-CONSTRAINT | `OBJ-SUPPORTING-CODE-PIN-GROUND-AS-ONE-CRS-M1-00795` |
| `CRS-M1-00796` | DATA-CONSTRAINT | `OBJ-SUPPORTING-CODE-PIN-OPEN-AS-ZERO-CRS-M1-00796` |
| `CRS-M1-00797` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PROCESS-AT-LEAST-4096-VLS-IN-FILTER-POLICE-FORWARD-CRS-M1-00797` |
| `CRS-M1-00798` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-INPUT-PHYSICAL-PORT-CRS-M1-00798` |
| `CRS-M1-00799` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-OUTPUT-PHYSICAL-PORTS-CRS-M1-00799` |
| `CRS-M1-00800` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-MAC-DESTINATION-CRS-M1-00800` |
| `CRS-M1-00801` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-BAG-CRS-M1-00801` |
| `CRS-M1-00802` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-MAX-JITTER-CRS-M1-00802` |
| `CRS-M1-00803` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-ACCOUNT-CRS-M1-00803` |
| `CRS-M1-00804` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-SMAX-CRS-M1-00804` |
| `CRS-M1-00805` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-SMIN-CRS-M1-00805` |
| `CRS-M1-00806` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-PRIORITIZATION-CRS-M1-00806` |
| `CRS-M1-00807` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-MAX-DELAY-CRS-M1-00807` |
| `CRS-M1-00808` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-STATE-CRS-M1-00808` |
| `CRS-M1-00809` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-SPEED-CRS-M1-00809` |
| `CRS-M1-00810` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-LOW-PRIORITY-BUFFER-CRS-M1-00810` |
| `CRS-M1-00811` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-HIGH-PRIORITY-BUFFER-CRS-M1-00811` |
| `CRS-M1-00812` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-VL-IDENTIFIER-CRS-M1-00812` |
| `CRS-M1-00813` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-SMAX-CRS-M1-00813` |
| `CRS-M1-00814` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-BAG-CRS-M1-00814` |
| `CRS-M1-00815` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-VL-IDENTIFIER-CRS-M1-00815` |
| `CRS-M1-00816` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-BAG-CRS-M1-00816` |
| `CRS-M1-00817` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-SMAX-CRS-M1-00817` |
| `CRS-M1-00818` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00819` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00820` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00821` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00822` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00823` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00824` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00825` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00826` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00827` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00828` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00829` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00830` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00831` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00832` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00833` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00834` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00835` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00836` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00837` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00838` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00839` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00840` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00841` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00842` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00843` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00844` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00845` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00846` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00847` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00848` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00849` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00850` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00851` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00852` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00853` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00854` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00855` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00856` | SCOPE-CONSTRAINT | `SCOPE` |

## Trace relations

| ID | CRS | Kind | Target | Rationale |
|---|---|---|---|---|
| `TR-CRS-M1-00001-0001` | `CRS-M1-00001` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00002-0002` | `CRS-M1-00002` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00003-0003` | `CRS-M1-00003` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00004-0004` | `CRS-M1-00004` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00005-0005` | `CRS-M1-00005` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00006-0006` | `CRS-M1-00006` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00007-0007` | `CRS-M1-00007` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00008-0008` | `CRS-M1-00008` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00009-0009` | `CRS-M1-00009` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00010-0010` | `CRS-M1-00010` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00011-0011` | `CRS-M1-00011` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00012-0012` | `CRS-M1-00012` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00013-0013` | `CRS-M1-00013` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00014-0014` | `CRS-M1-00014` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00015-0015` | `CRS-M1-00015` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00016-0016` | `CRS-M1-00016` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00017-0017` | `CRS-M1-00017` | SCOPE | `SCOPE` | Non-behavior / profile obligation ENCODE kept as a scope or applicability constraint. |
| `TR-CRS-M1-00018-0018` | `CRS-M1-00018` | INTERFACE | `IF_NETWORK` | Network infrastructure premise; capability not established. |
| `TR-CRS-M1-00019-0019` | `CRS-M1-00019` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00020-0020` | `CRS-M1-00020` | INTERFACE | `IF_TFTP` | TFTP interface premise for TRANSFER. |
| `TR-CRS-M1-00021-0021` | `CRS-M1-00021` | SCOPE | `SCOPE` | Non-behavior / profile obligation USE kept as a scope or applicability constraint. |
| `TR-CRS-M1-00022-0022` | `CRS-M1-00022` | INTERFACE | `IF_TFTP` | TFTP interface premise for DO-NOT-FAIL-TRANSFER-FOR-UNIMPLEMENTED-OPTION. |
| `TR-CRS-M1-00023-0023` | `CRS-M1-00023` | INTERFACE | `IF_TFTP` | TFTP interface premise for ABSENT-AFTER-BOUNDARY. |
| `TR-CRS-M1-00024-0024` | `CRS-M1-00024` | INTERFACE | `IF_TFTP` | TFTP interface premise for TRANSFER. |
| `TR-CRS-M1-00025-0025` | `CRS-M1-00025` | INTERFACE | `IF_TFTP` | TFTP interface premise for USE-WELL-KNOWN-PORT. |
| `TR-CRS-M1-00026-0026` | `CRS-M1-00026` | SCOPE | `SCOPE` | Non-behavior / profile obligation USE kept as a scope or applicability constraint. |
| `TR-CRS-M1-00027-0027` | `CRS-M1-00027` | SCOPE | `SCOPE` | Non-behavior / profile obligation ENCODE kept as a scope or applicability constraint. |
| `TR-CRS-M1-00028-0028` | `CRS-M1-00028` | SCOPE | `SCOPE` | Non-behavior / profile obligation ENCODE kept as a scope or applicability constraint. |
| `TR-CRS-M1-00029-0029` | `CRS-M1-00029` | INTERFACE | `IF_TFTP` | TFTP interface premise for REPORT-RESOURCE-UNAVAILABLE. |
| `TR-CRS-M1-00030-0030` | `CRS-M1-00030` | INTERFACE | `IF_TFTP` | TFTP interface premise for REPORT-RESOURCE-UNAVAILABLE. |
| `TR-CRS-M1-00031-0031` | `CRS-M1-00031` | INTERFACE | `IF_TFTP` | TFTP interface premise for TRANSFER. |
| `TR-CRS-M1-00032-0032` | `CRS-M1-00032` | INTERFACE | `IF_TFTP` | TFTP interface premise for ABORT-AND-RESTART-AFTER-DELAY. |
| `TR-CRS-M1-00032-0033` | `CRS-M1-00032` | TIMING | `TIM-CRS-M1-00032` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00032-0034` | `CRS-M1-00032` | CLOCK | `CLK_WAIT` | Clock used by this timing obligation. |
| `TR-CRS-M1-00032-0454` | `CRS-M1-00032` | TRANSITION | `T_WAIT_FROM_UPL_FILE` | Transition T_WAIT_FROM_UPL_FILE cites this obligation. |
| `TR-CRS-M1-00032-0455` | `CRS-M1-00032` | TRANSITION | `T_WAIT_FROM_UPL_LUR` | Transition T_WAIT_FROM_UPL_LUR cites this obligation. |
| `TR-CRS-M1-00032-0456` | `CRS-M1-00032` | TRANSITION | `T_WAIT_FROM_INF_LCI` | Transition T_WAIT_FROM_INF_LCI cites this obligation. |
| `TR-CRS-M1-00032-0457` | `CRS-M1-00032` | TRANSITION | `T_WAIT_FROM_INF_LCL` | Transition T_WAIT_FROM_INF_LCL cites this obligation. |
| `TR-CRS-M1-00032-0458` | `CRS-M1-00032` | TRANSITION | `T_WAIT_RETRY_UPL_FILE` | Transition T_WAIT_RETRY_UPL_FILE cites this obligation. |
| `TR-CRS-M1-00032-0459` | `CRS-M1-00032` | TRANSITION | `T_WAIT_RETRY_UPL_LUR` | Transition T_WAIT_RETRY_UPL_LUR cites this obligation. |
| `TR-CRS-M1-00032-0460` | `CRS-M1-00032` | TRANSITION | `T_WAIT_RETRY_INF_LCI` | Transition T_WAIT_RETRY_INF_LCI cites this obligation. |
| `TR-CRS-M1-00032-0461` | `CRS-M1-00032` | TRANSITION | `T_WAIT_RETRY_INF_LCL` | Transition T_WAIT_RETRY_INF_LCL cites this obligation. |
| `TR-CRS-M1-00033-0035` | `CRS-M1-00033` | INTERFACE | `IF_NETWORK` | Network infrastructure premise; capability not established. |
| `TR-CRS-M1-00034-0036` | `CRS-M1-00034` | INTERFACE | `IF_TFTP_BLOCKSIZE` | Block-size capability premise; RFC 2348 candidate edge is separate. |
| `TR-CRS-M1-00035-0037` | `CRS-M1-00035` | SCOPE | `SCOPE` | Non-behavior / profile obligation IMPLEMENT kept as a scope or applicability constraint. |
| `TR-CRS-M1-00036-0038` | `CRS-M1-00036` | INTERFACE | `IF_TFTP_BLOCKSIZE` | Block-size capability premise; RFC 2348 candidate edge is separate. |
| `TR-CRS-M1-00037-0039` | `CRS-M1-00037` | INTERFACE | `IF_NETWORK` | Network infrastructure premise; capability not established. |
| `TR-CRS-M1-00038-0040` | `CRS-M1-00038` | INTERFACE | `IF_TFTP` | TFTP interface premise for COMPARE. |
| `TR-CRS-M1-00039-0041` | `CRS-M1-00039` | INTERFACE | `IF_NETWORK` | Network infrastructure premise; capability not established. |
| `TR-CRS-M1-00040-0042` | `CRS-M1-00040` | INTERFACE | `IF_NETWORK` | Network infrastructure premise; capability not established. |
| `TR-CRS-M1-00041-0043` | `CRS-M1-00041` | INTERFACE | `IF_NETWORK` | Network infrastructure premise; capability not established. |
| `TR-CRS-M1-00042-0044` | `CRS-M1-00042` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00043-0045` | `CRS-M1-00043` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00044-0046` | `CRS-M1-00044` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00045-0047` | `CRS-M1-00045` | INTERFACE | `IF_NETWORK` | Network infrastructure premise; capability not established. |
| `TR-CRS-M1-00046-0048` | `CRS-M1-00046` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00047-0049` | `CRS-M1-00047` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00048-0050` | `CRS-M1-00048` | INTERFACE | `IF_TFTP` | TFTP interface premise for TRANSFER. |
| `TR-CRS-M1-00049-0051` | `CRS-M1-00049` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00050-0052` | `CRS-M1-00050` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00051-0053` | `CRS-M1-00051` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00052-0054` | `CRS-M1-00052` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00053-0055` | `CRS-M1-00053` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00054-0056` | `CRS-M1-00054` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00055-0057` | `CRS-M1-00055` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00056-0058` | `CRS-M1-00056` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00057-0059` | `CRS-M1-00057` | SCOPE | `SCOPE` | Non-behavior / profile obligation FAIL kept as a scope or applicability constraint. |
| `TR-CRS-M1-00058-0060` | `CRS-M1-00058` | INTERFACE | `IF_NETWORK` | Network infrastructure premise; capability not established. |
| `TR-CRS-M1-00059-0061` | `CRS-M1-00059` | INTERFACE | `IF_TFTP` | TFTP interface premise for COMPLY. |
| `TR-CRS-M1-00060-0062` | `CRS-M1-00060` | INTERFACE | `IF_TFTP` | TFTP interface premise for SEND. |
| `TR-CRS-M1-00061-0063` | `CRS-M1-00061` | INTERFACE | `IF_NETWORK` | Network infrastructure premise; capability not established. |
| `TR-CRS-M1-00062-0064` | `CRS-M1-00062` | SCOPE | `SCOPE` | Non-behavior / profile obligation ALLOW-ANY-ORDER-WHILE-SERIALIZING-PER-TARGET kept as a scope or applicability constraint. |
| `TR-CRS-M1-00063-0065` | `CRS-M1-00063` | SCOPE | `SCOPE` | Non-behavior / profile obligation ABORT kept as a scope or applicability constraint. |
| `TR-CRS-M1-00064-0066` | `CRS-M1-00064` | SCOPE | `SCOPE` | Non-behavior / profile obligation IMPLEMENT kept as a scope or applicability constraint. |
| `TR-CRS-M1-00065-0067` | `CRS-M1-00065` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00066-0068` | `CRS-M1-00066` | INTERFACE | `IF_TFTP` | TFTP interface premise for TRANSFER. |
| `TR-CRS-M1-00067-0069` | `CRS-M1-00067` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00068-0070` | `CRS-M1-00068` | INTERFACE | `IF_TFTP` | TFTP interface premise for TRANSFER. |
| `TR-CRS-M1-00069-0071` | `CRS-M1-00069` | INTERFACE | `IF_NETWORK` | Network infrastructure premise; capability not established. |
| `TR-CRS-M1-00070-0072` | `CRS-M1-00070` | INTERFACE | `IF_NETWORK` | Network infrastructure premise; capability not established. |
| `TR-CRS-M1-00071-0073` | `CRS-M1-00071` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00072-0074` | `CRS-M1-00072` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00073-0075` | `CRS-M1-00073` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00074-0076` | `CRS-M1-00074` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00075-0077` | `CRS-M1-00075` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00076-0078` | `CRS-M1-00076` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00077-0079` | `CRS-M1-00077` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00078-0080` | `CRS-M1-00078` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00079-0081` | `CRS-M1-00079` | TRANSITION | `T_UPL_LUR_XFER` | UPLOAD list-file obligation on the LUR stage. |
| `TR-CRS-M1-00080-0082` | `CRS-M1-00080` | TRANSITION | `T_UPL_LUS_XFER` | UPLOAD status obligation on the LUS stage. |
| `TR-CRS-M1-00081-0083` | `CRS-M1-00081` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00082-0084` | `CRS-M1-00082` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00083-0085` | `CRS-M1-00083` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00084-0086` | `CRS-M1-00084` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00085-0087` | `CRS-M1-00085` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00086-0088` | `CRS-M1-00086` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00087-0089` | `CRS-M1-00087` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00088-0090` | `CRS-M1-00088` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00089-0091` | `CRS-M1-00089` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00090-0092` | `CRS-M1-00090` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00091-0093` | `CRS-M1-00091` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00092-0094` | `CRS-M1-00092` | SCOPE | `SCOPE` | Non-behavior / profile obligation ABORT kept as a scope or applicability constraint. |
| `TR-CRS-M1-00093-0095` | `CRS-M1-00093` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00094-0096` | `CRS-M1-00094` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00094-0097` | `CRS-M1-00094` | TIMING | `TIM-CRS-M1-00094` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00094-0098` | `CRS-M1-00094` | CLOCK | `CLK_DLP` | Clock used by this timing obligation. |
| `TR-CRS-M1-00095-0099` | `CRS-M1-00095` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00096-0100` | `CRS-M1-00096` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00097-0101` | `CRS-M1-00097` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00097-0102` | `CRS-M1-00097` | TIMING | `TIM-CRS-M1-00097` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00097-0103` | `CRS-M1-00097` | CLOCK | `CLK_DLP` | Clock used by this timing obligation. |
| `TR-CRS-M1-00098-0104` | `CRS-M1-00098` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00098-0105` | `CRS-M1-00098` | TIMING | `TIM-CRS-M1-00098` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00098-0106` | `CRS-M1-00098` | CLOCK | `CLK_DLP` | Clock used by this timing obligation. |
| `TR-CRS-M1-00099-0107` | `CRS-M1-00099` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00099-0108` | `CRS-M1-00099` | TIMING | `TIM-CRS-M1-00099` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00099-0109` | `CRS-M1-00099` | CLOCK | `CLK_EXCEPTION` | Clock used by this timing obligation. |
| `TR-CRS-M1-00099-0452` | `CRS-M1-00099` | TRANSITION | `T_ENTER_UPL_EXC` | Transition T_ENTER_UPL_EXC cites this obligation. |
| `TR-CRS-M1-00099-0453` | `CRS-M1-00099` | TRANSITION | `T_ENTER_INF_EXC` | Transition T_ENTER_INF_EXC cites this obligation. |
| `TR-CRS-M1-00100-0110` | `CRS-M1-00100` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00100-0111` | `CRS-M1-00100` | TIMING | `TIM-CRS-M1-00100` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00100-0112` | `CRS-M1-00100` | CLOCK | `CLK_EXCEPTION` | Clock used by this timing obligation. |
| `TR-CRS-M1-00101-0113` | `CRS-M1-00101` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00101-0114` | `CRS-M1-00101` | TIMING | `TIM-CRS-M1-00101` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00101-0115` | `CRS-M1-00101` | CLOCK | `CLK_EXCEPTION` | Clock used by this timing obligation. |
| `TR-CRS-M1-00101-0449` | `CRS-M1-00101` | TRANSITION | `T_UPL_EXC_TO` | Transition T_UPL_EXC_TO cites this obligation. |
| `TR-CRS-M1-00101-0451` | `CRS-M1-00101` | TRANSITION | `T_INF_EXC_TO` | Transition T_INF_EXC_TO cites this obligation. |
| `TR-CRS-M1-00102-0116` | `CRS-M1-00102` | TRANSITION | `T_UPL_LUS_XFER` | UPLOAD status obligation on the LUS stage. |
| `TR-CRS-M1-00102-0117` | `CRS-M1-00102` | TIMING | `TIM-CRS-M1-00102` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00102-0118` | `CRS-M1-00102` | CLOCK | `CLK_DLP` | Clock used by this timing obligation. |
| `TR-CRS-M1-00103-0119` | `CRS-M1-00103` | TRANSITION | `T_UPL_LUS_XFER` | UPLOAD status obligation on the LUS stage. |
| `TR-CRS-M1-00104-0120` | `CRS-M1-00104` | TRANSITION | `T_UPL_LUS_XFER` | UPLOAD status obligation on the LUS stage. |
| `TR-CRS-M1-00105-0121` | `CRS-M1-00105` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00106-0122` | `CRS-M1-00106` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00106-0123` | `CRS-M1-00106` | TIMING | `TIM-CRS-M1-00106` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00106-0124` | `CRS-M1-00106` | CLOCK | `CLK_EXCEPTION` | Clock used by this timing obligation. |
| `TR-CRS-M1-00107-0125` | `CRS-M1-00107` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00107-0126` | `CRS-M1-00107` | TIMING | `TIM-CRS-M1-00107` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00107-0127` | `CRS-M1-00107` | CLOCK | `CLK_EXCEPTION` | Clock used by this timing obligation. |
| `TR-CRS-M1-00108-0128` | `CRS-M1-00108` | TRANSITION | `T_UPL_LUS_XFER` | UPLOAD status obligation on the LUS stage. |
| `TR-CRS-M1-00108-0129` | `CRS-M1-00108` | TIMING | `TIM-CRS-M1-00108` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00108-0130` | `CRS-M1-00108` | CLOCK | `CLK_EXCEPTION` | Clock used by this timing obligation. |
| `TR-CRS-M1-00108-0450` | `CRS-M1-00108` | TRANSITION | `T_UPL_EXC_TO` | Transition T_UPL_EXC_TO cites this obligation. |
| `TR-CRS-M1-00109-0131` | `CRS-M1-00109` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00110-0132` | `CRS-M1-00110` | SCOPE | `SCOPE` | Non-behavior / profile obligation ABORT kept as a scope or applicability constraint. |
| `TR-CRS-M1-00111-0133` | `CRS-M1-00111` | SCOPE | `SCOPE` | Non-behavior / profile obligation ABORT kept as a scope or applicability constraint. |
| `TR-CRS-M1-00112-0134` | `CRS-M1-00112` | SCOPE | `SCOPE` | Non-behavior / profile obligation ABORT kept as a scope or applicability constraint. |
| `TR-CRS-M1-00113-0135` | `CRS-M1-00113` | SCOPE | `SCOPE` | Non-behavior / profile obligation ABORT kept as a scope or applicability constraint. |
| `TR-CRS-M1-00114-0136` | `CRS-M1-00114` | SCOPE | `SCOPE` | Non-behavior / profile obligation ABORT kept as a scope or applicability constraint. |
| `TR-CRS-M1-00115-0137` | `CRS-M1-00115` | INTERFACE | `IF_NETWORK` | Network infrastructure premise; capability not established. |
| `TR-CRS-M1-00116-0138` | `CRS-M1-00116` | SCOPE | `SCOPE` | Non-behavior / profile obligation IMPLEMENT kept as a scope or applicability constraint. |
| `TR-CRS-M1-00117-0139` | `CRS-M1-00117` | INTERFACE | `IF_NETWORK` | Network infrastructure premise; capability not established. |
| `TR-CRS-M1-00118-0140` | `CRS-M1-00118` | INTERFACE | `IF_NETWORK` | Network infrastructure premise; capability not established. |
| `TR-CRS-M1-00119-0141` | `CRS-M1-00119` | SCOPE | `SCOPE` | Non-behavior / profile obligation ABORT kept as a scope or applicability constraint. |
| `TR-CRS-M1-00120-0142` | `CRS-M1-00120` | SCOPE | `SCOPE` | Non-behavior / profile obligation ABORT kept as a scope or applicability constraint. |
| `TR-CRS-M1-00121-0143` | `CRS-M1-00121` | SCOPE | `SCOPE` | Non-behavior / profile obligation ENCODE kept as a scope or applicability constraint. |
| `TR-CRS-M1-00122-0144` | `CRS-M1-00122` | SCOPE | `SCOPE` | Non-behavior / profile obligation ENCODE kept as a scope or applicability constraint. |
| `TR-CRS-M1-00123-0145` | `CRS-M1-00123` | SCOPE | `SCOPE` | Non-behavior / profile obligation ENCODE kept as a scope or applicability constraint. |
| `TR-CRS-M1-00124-0146` | `CRS-M1-00124` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00125-0147` | `CRS-M1-00125` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00126-0148` | `CRS-M1-00126` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00127-0149` | `CRS-M1-00127` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00128-0150` | `CRS-M1-00128` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00129-0151` | `CRS-M1-00129` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00130-0152` | `CRS-M1-00130` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00131-0153` | `CRS-M1-00131` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00132-0154` | `CRS-M1-00132` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00133-0155` | `CRS-M1-00133` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00134-0156` | `CRS-M1-00134` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00135-0157` | `CRS-M1-00135` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00136-0158` | `CRS-M1-00136` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00137-0159` | `CRS-M1-00137` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00138-0160` | `CRS-M1-00138` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00139-0161` | `CRS-M1-00139` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00140-0162` | `CRS-M1-00140` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00141-0163` | `CRS-M1-00141` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00142-0164` | `CRS-M1-00142` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00143-0165` | `CRS-M1-00143` | TRANSITION | `T_UPL_LUR_XFER` | UPLOAD list-file obligation on the LUR stage. |
| `TR-CRS-M1-00144-0166` | `CRS-M1-00144` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00145-0167` | `CRS-M1-00145` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00146-0168` | `CRS-M1-00146` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00147-0169` | `CRS-M1-00147` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00148-0170` | `CRS-M1-00148` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00149-0171` | `CRS-M1-00149` | TRANSITION | `T_UPL_LUS_XFER` | UPLOAD status obligation on the LUS stage. |
| `TR-CRS-M1-00150-0172` | `CRS-M1-00150` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00151-0173` | `CRS-M1-00151` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00152-0174` | `CRS-M1-00152` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00153-0175` | `CRS-M1-00153` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00154-0176` | `CRS-M1-00154` | TRANSITION | `T_UPL_LUS_XFER` | UPLOAD status obligation on the LUS stage. |
| `TR-CRS-M1-00155-0177` | `CRS-M1-00155` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00156-0178` | `CRS-M1-00156` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00157-0179` | `CRS-M1-00157` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00158-0180` | `CRS-M1-00158` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00159-0181` | `CRS-M1-00159` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00160-0182` | `CRS-M1-00160` | TRANSITION | `T_UPL_LUS_XFER` | UPLOAD status obligation on the LUS stage. |
| `TR-CRS-M1-00161-0183` | `CRS-M1-00161` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00162-0184` | `CRS-M1-00162` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00163-0185` | `CRS-M1-00163` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00164-0186` | `CRS-M1-00164` | TRANSITION | `T_UPL_FILE_XFER` | UPLOAD file-thread obligation after LUR. |
| `TR-CRS-M1-00165-0187` | `CRS-M1-00165` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00166-0188` | `CRS-M1-00166` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00167-0189` | `CRS-M1-00167` | INTERFACE | `IF_TFTP` | TFTP interface premise for RETRY. |
| `TR-CRS-M1-00168-0190` | `CRS-M1-00168` | INTERFACE | `IF_TFTP` | TFTP interface premise for TRANSFER. |
| `TR-CRS-M1-00168-0191` | `CRS-M1-00168` | TIMING | `TIM-CRS-M1-00168` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00168-0192` | `CRS-M1-00168` | CLOCK | `CLK_TFTP` | Clock used by this timing obligation. |
| `TR-CRS-M1-00169-0193` | `CRS-M1-00169` | SCOPE | `SCOPE` | Non-behavior / profile obligation ACKNOWLEDGE kept as a scope or applicability constraint. |
| `TR-CRS-M1-00170-0194` | `CRS-M1-00170` | INTERFACE | `IF_TFTP` | TFTP interface premise for RETRY. |
| `TR-CRS-M1-00171-0195` | `CRS-M1-00171` | INTERFACE | `IF_TFTP` | TFTP interface premise for RETRY. |
| `TR-CRS-M1-00172-0196` | `CRS-M1-00172` | SCOPE | `SCOPE` | Non-behavior / profile obligation PROVIDE kept as a scope or applicability constraint. |
| `TR-CRS-M1-00173-0197` | `CRS-M1-00173` | INTERFACE | `IF_TFTP` | TFTP interface premise for RETRY. |
| `TR-CRS-M1-00174-0198` | `CRS-M1-00174` | SCOPE | `SCOPE` | Non-behavior / profile obligation DECLARE-FATAL-ERROR kept as a scope or applicability constraint. |
| `TR-CRS-M1-00175-0199` | `CRS-M1-00175` | SCOPE | `SCOPE` | Non-behavior / profile obligation FAIL kept as a scope or applicability constraint. |
| `TR-CRS-M1-00176-0200` | `CRS-M1-00176` | SCOPE | `SCOPE` | Non-behavior / profile obligation ADJUST-UPWARD kept as a scope or applicability constraint. |
| `TR-CRS-M1-00176-0201` | `CRS-M1-00176` | TIMING | `TIM-CRS-M1-00176` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00176-0202` | `CRS-M1-00176` | CLOCK | `CLK_DLP` | Clock used by this timing obligation. |
| `TR-CRS-M1-00177-0203` | `CRS-M1-00177` | SCOPE | `SCOPE` | Non-behavior / profile obligation SET-CONSTANT kept as a scope or applicability constraint. |
| `TR-CRS-M1-00177-0204` | `CRS-M1-00177` | TIMING | `TIM-CRS-M1-00177` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00177-0205` | `CRS-M1-00177` | CLOCK | `CLK_TFTP` | Clock used by this timing obligation. |
| `TR-CRS-M1-00177-0442` | `CRS-M1-00177` | TRANSITION | `T_INF_TFTP_TO` | Transition T_INF_TFTP_TO cites this obligation. |
| `TR-CRS-M1-00177-0443` | `CRS-M1-00177` | TRANSITION | `T_UPL_TFTP_TO` | Transition T_UPL_TFTP_TO cites this obligation. |
| `TR-CRS-M1-00177-0444` | `CRS-M1-00177` | TRANSITION | `T_UPL_LUR_TFTP_TO` | Transition T_UPL_LUR_TFTP_TO cites this obligation. |
| `TR-CRS-M1-00177-0445` | `CRS-M1-00177` | TRANSITION | `T_UPL_FILE_TFTP_TO` | Transition T_UPL_FILE_TFTP_TO cites this obligation. |
| `TR-CRS-M1-00178-0206` | `CRS-M1-00178` | INTERFACE | `IF_TFTP` | TFTP interface premise for LIMIT-SINGLE-TFTP-PACKET-TRANSMISSION-DURATION. |
| `TR-CRS-M1-00178-0207` | `CRS-M1-00178` | TIMING | `TIM-CRS-M1-00178` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00178-0208` | `CRS-M1-00178` | CLOCK | `CLK_TFTP` | Clock used by this timing obligation. |
| `TR-CRS-M1-00179-0209` | `CRS-M1-00179` | INTERFACE | `IF_TFTP` | TFTP interface premise for LIMIT-TFTP-PACKET-PROCESSING-DURATION. |
| `TR-CRS-M1-00179-0210` | `CRS-M1-00179` | TIMING | `TIM-CRS-M1-00179` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00179-0211` | `CRS-M1-00179` | CLOCK | `CLK_DLP` | Clock used by this timing obligation. |
| `TR-CRS-M1-00180-0212` | `CRS-M1-00180` | INTERFACE | `IF_TFTP` | TFTP interface premise for RETRY. |
| `TR-CRS-M1-00181-0213` | `CRS-M1-00181` | INTERFACE | `IF_TFTP` | TFTP interface premise for RETRY. |
| `TR-CRS-M1-00182-0214` | `CRS-M1-00182` | SCOPE | `SCOPE` | Non-behavior / profile obligation ENCODE kept as a scope or applicability constraint. |
| `TR-CRS-M1-00183-0215` | `CRS-M1-00183` | INTERFACE | `IF_TFTP` | TFTP interface premise for SEND. |
| `TR-CRS-M1-00184-0216` | `CRS-M1-00184` | INTERFACE | `IF_TFTP` | TFTP interface premise for TRANSFER. |
| `TR-CRS-M1-00184-0217` | `CRS-M1-00184` | TIMING | `TIM-CRS-M1-00184` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00184-0218` | `CRS-M1-00184` | CLOCK | `CLK_DLP` | Clock used by this timing obligation. |
| `TR-CRS-M1-00185-0219` | `CRS-M1-00185` | SCOPE | `SCOPE` | Non-behavior / profile obligation ADJUST-UPWARD kept as a scope or applicability constraint. |
| `TR-CRS-M1-00185-0220` | `CRS-M1-00185` | TIMING | `TIM-CRS-M1-00185` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00185-0221` | `CRS-M1-00185` | CLOCK | `CLK_DLP` | Clock used by this timing obligation. |
| `TR-CRS-M1-00186-0222` | `CRS-M1-00186` | SCOPE | `SCOPE` | Non-behavior / profile obligation DO-NOT-PRODUCE-LCS-DURING-TIMELY-LCI-LCL-SEQUENCE kept as a scope or applicability constraint. |
| `TR-CRS-M1-00186-0223` | `CRS-M1-00186` | TIMING | `TIM-CRS-M1-00186` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00186-0224` | `CRS-M1-00186` | CLOCK | `CLK_DLP` | Clock used by this timing obligation. |
| `TR-CRS-M1-00187-0225` | `CRS-M1-00187` | SCOPE | `SCOPE` | Non-behavior / profile obligation PROVIDE kept as a scope or applicability constraint. |
| `TR-CRS-M1-00187-0226` | `CRS-M1-00187` | TIMING | `TIM-CRS-M1-00187` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00187-0227` | `CRS-M1-00187` | CLOCK | `CLK_DLP` | Clock used by this timing obligation. |
| `TR-CRS-M1-00187-0446` | `CRS-M1-00187` | TRANSITION | `T_UPL_DLP_TO` | Transition T_UPL_DLP_TO cites this obligation. |
| `TR-CRS-M1-00187-0447` | `CRS-M1-00187` | TRANSITION | `T_UPL_LUR_DLP_TO` | Transition T_UPL_LUR_DLP_TO cites this obligation. |
| `TR-CRS-M1-00188-0228` | `CRS-M1-00188` | INTERFACE | `IF_TFTP` | TFTP interface premise for BOUND-INTER-TRANSFER-DURATION-BY-DLP-EQUATION. |
| `TR-CRS-M1-00188-0229` | `CRS-M1-00188` | TIMING | `TIM-CRS-M1-00188` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00188-0230` | `CRS-M1-00188` | CLOCK | `CLK_DLP` | Clock used by this timing obligation. |
| `TR-CRS-M1-00188-0448` | `CRS-M1-00188` | TRANSITION | `T_UPL_LUR_DLP_TO` | Transition T_UPL_LUR_DLP_TO cites this obligation. |
| `TR-CRS-M1-00189-0231` | `CRS-M1-00189` | INTERFACE | `IF_TFTP` | TFTP interface premise for RETRY. |
| `TR-CRS-M1-00190-0232` | `CRS-M1-00190` | INTERFACE | `IF_NETWORK` | Network infrastructure premise; capability not established. |
| `TR-CRS-M1-00191-0233` | `CRS-M1-00191` | OBJECT-CONSTRAINT | `OBJ-MINIMUM-ARINC-665-COMPATIBILITY-CAPABILITIES-IMPLEMENT-REQUIRED-ARINC-665-CA-CRS-M1-00191` | 665/data-object predicate OBJ-MINIMUM-ARINC-665-COMPATIBILITY-CAPABILITIES-IMPLEMENT-REQUIRED-ARINC-665-CA-CRS-M1-00191. |
| `TR-CRS-M1-00192-0234` | `CRS-M1-00192` | OBJECT-CONSTRAINT | `OBJ-ARINC-665-SHOULD-MODALITY-TREAT-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY-CRS-M1-00192` | 665/data-object predicate OBJ-ARINC-665-SHOULD-MODALITY-TREAT-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY-CRS-M1-00192. |
| `TR-CRS-M1-00193-0235` | `CRS-M1-00193` | OBJECT-CONSTRAINT | `OBJ-ARINC-665-MAY-MODALITY-TREAT-MAY-AS-OPTIONAL-CAPABILITY-CRS-M1-00193` | 665/data-object predicate OBJ-ARINC-665-MAY-MODALITY-TREAT-MAY-AS-OPTIONAL-CAPABILITY-CRS-M1-00193. |
| `TR-CRS-M1-00194-0236` | `CRS-M1-00194` | OBJECT-CONSTRAINT | `OBJ-OPTIONAL-ARINC-665-CAPABILITY-CONDITIONALLY-IMPLEMENT-OPTIONAL-CAPABILITY-AS-CRS-M1-00194` | 665/data-object predicate OBJ-OPTIONAL-ARINC-665-CAPABILITY-CONDITIONALLY-IMPLEMENT-OPTIONAL-CAPABILITY-AS-CRS-M1-00194. |
| `TR-CRS-M1-00195-0237` | `CRS-M1-00195` | OBJECT-CONSTRAINT | `OBJ-DATA-FIELD-TYPE-INTERPRET-FIELDS-AS-NUMERIC-BY-DEFAULT-CRS-M1-00195` | 665/data-object predicate OBJ-DATA-FIELD-TYPE-INTERPRET-FIELDS-AS-NUMERIC-BY-DEFAULT-CRS-M1-00195. |
| `TR-CRS-M1-00196-0238` | `CRS-M1-00196` | OBJECT-CONSTRAINT | `OBJ-ARINC-665-FILE-PROHIBIT-UNDEFINED-FIELD-INSERTION-CRS-M1-00196` | 665/data-object predicate OBJ-ARINC-665-FILE-PROHIBIT-UNDEFINED-FIELD-INSERTION-CRS-M1-00196. |
| `TR-CRS-M1-00197-0239` | `CRS-M1-00197` | OBJECT-CONSTRAINT | `OBJ-FILE-VERSION-COMPATIBILITY-ENCODE-CRS-M1-00197` | 665/data-object predicate OBJ-FILE-VERSION-COMPATIBILITY-ENCODE-CRS-M1-00197. |
| `TR-CRS-M1-00198-0240` | `CRS-M1-00198` | OBJECT-CONSTRAINT | `OBJ-TARGET-HARDWARE-ID-MANUFACTURER-IDENTIFIER-PREFIX-TARGET-HARDWARE-ID-WITH-MA-CRS-M1-00198` | 665/data-object predicate OBJ-TARGET-HARDWARE-ID-MANUFACTURER-IDENTIFIER-PREFIX-TARGET-HARDWARE-ID-WITH-MA-CRS-M1-00198. |
| `TR-CRS-M1-00199-0241` | `CRS-M1-00199` | OBJECT-CONSTRAINT | `OBJ-MANUFACTURER-IDENTIFIER-ASSIGN-CRS-M1-00199` | 665/data-object predicate OBJ-MANUFACTURER-IDENTIFIER-ASSIGN-CRS-M1-00199. |
| `TR-CRS-M1-00200-0242` | `CRS-M1-00200` | OBJECT-CONSTRAINT | `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ASSIGN-GENERIC-TARGET-HARDWARE-ID-CRS-M1-00200` | 665/data-object predicate OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ASSIGN-GENERIC-TARGET-HARDWARE-ID-CRS-M1-00200. |
| `TR-CRS-M1-00201-0243` | `CRS-M1-00201` | OBJECT-CONSTRAINT | `OBJ-REDUNDANT-CHANNEL-LOADS-DISTRIBUTE-REDUNDANT-LOADS-INTERNALLY-CRS-M1-00201` | 665/data-object predicate OBJ-REDUNDANT-CHANNEL-LOADS-DISTRIBUTE-REDUNDANT-LOADS-INTERNALLY-CRS-M1-00201. |
| `TR-CRS-M1-00202-0244` | `CRS-M1-00202` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-ENSURE-CARDINALITY-CRS-M1-00202` | 665/data-object predicate OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-ENSURE-CARDINALITY-CRS-M1-00202. |
| `TR-CRS-M1-00203-0245` | `CRS-M1-00203` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-COORDINATE-CRS-M1-00203` | 665/data-object predicate OBJ-LOAD-PART-NUMBER-COORDINATE-CRS-M1-00203. |
| `TR-CRS-M1-00204-0246` | `CRS-M1-00204` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-ASSIGN-CRS-M1-00204` | 665/data-object predicate OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-ASSIGN-CRS-M1-00204. |
| `TR-CRS-M1-00205-0247` | `CRS-M1-00205` | OBJECT-CONSTRAINT | `OBJ-LOADABLE-SOFTWARE-PART-NUMBER-FORMAT-CRS-M1-00205` | 665/data-object predicate OBJ-LOADABLE-SOFTWARE-PART-NUMBER-FORMAT-CRS-M1-00205. |
| `TR-CRS-M1-00206-0248` | `CRS-M1-00206` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-EXCLUDE-EMBEDDED-BLANKS-CRS-M1-00206` | 665/data-object predicate OBJ-LOAD-PART-NUMBER-EXCLUDE-EMBEDDED-BLANKS-CRS-M1-00206. |
| `TR-CRS-M1-00207-0249` | `CRS-M1-00207` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-DO-NOT-ENFORCE-SPECIFIC-PART-NUMBER-FORMAT-CRS-M1-00207` | 665/data-object predicate OBJ-LOAD-PART-NUMBER-DO-NOT-ENFORCE-SPECIFIC-PART-NUMBER-FORMAT-CRS-M1-00207. |
| `TR-CRS-M1-00208-0250` | `CRS-M1-00208` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-PROCESS-NONCONFORMING-PART-NUMBER-FORMATS-CRS-M1-00208` | 665/data-object predicate OBJ-LOAD-PART-NUMBER-PROCESS-NONCONFORMING-PART-NUMBER-FORMATS-CRS-M1-00208. |
| `TR-CRS-M1-00209-0251` | `CRS-M1-00209` | OBJECT-CONSTRAINT | `OBJ-NETWORK-INTERFACE-DESIGN-CRS-M1-00209` | 665/data-object predicate OBJ-NETWORK-INTERFACE-DESIGN-CRS-M1-00209. |
| `TR-CRS-M1-00210-0252` | `CRS-M1-00210` | OBJECT-CONSTRAINT | `OBJ-NETWORK-INTERFACE-FORMAT-CRS-M1-00210` | 665/data-object predicate OBJ-NETWORK-INTERFACE-FORMAT-CRS-M1-00210. |
| `TR-CRS-M1-00211-0253` | `CRS-M1-00211` | OBJECT-CONSTRAINT | `OBJ-ATA-PART-NUMBER-DELIMITERS-SEPARATE-DELIMITERS-FROM-LETTERS-CRS-M1-00211` | 665/data-object predicate OBJ-ATA-PART-NUMBER-DELIMITERS-SEPARATE-DELIMITERS-FROM-LETTERS-CRS-M1-00211. |
| `TR-CRS-M1-00212-0254` | `CRS-M1-00212` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-ENCODE-CRS-M1-00212` | 665/data-object predicate OBJ-LOAD-PART-NUMBER-ENCODE-CRS-M1-00212. |
| `TR-CRS-M1-00213-0255` | `CRS-M1-00213` | OBJECT-CONSTRAINT | `OBJ-ATA-PART-NUMBER-CHARACTER-SET-EXCLUDE-AMBIGUOUS-LETTER-O-CRS-M1-00213` | 665/data-object predicate OBJ-ATA-PART-NUMBER-CHARACTER-SET-EXCLUDE-AMBIGUOUS-LETTER-O-CRS-M1-00213. |
| `TR-CRS-M1-00214-0256` | `CRS-M1-00214` | OBJECT-CONSTRAINT | `OBJ-MMM-CODE-INTERPRET-CONFUSED-MMM-CHARACTERS-AS-ALPHABETIC-CRS-M1-00214` | 665/data-object predicate OBJ-MMM-CODE-INTERPRET-CONFUSED-MMM-CHARACTERS-AS-ALPHABETIC-CRS-M1-00214. |
| `TR-CRS-M1-00215-0257` | `CRS-M1-00215` | OBJECT-CONSTRAINT | `OBJ-CHECK-CHARACTERS-COMPUTE-CRS-M1-00215` | 665/data-object predicate OBJ-CHECK-CHARACTERS-COMPUTE-CRS-M1-00215. |
| `TR-CRS-M1-00216-0258` | `CRS-M1-00216` | OBJECT-CONSTRAINT | `OBJ-HEADER-FILE-SOFTWARE-PART-FORMAT-CRS-M1-00216` | 665/data-object predicate OBJ-HEADER-FILE-SOFTWARE-PART-FORMAT-CRS-M1-00216. |
| `TR-CRS-M1-00217-0259` | `CRS-M1-00217` | OBJECT-CONSTRAINT | `OBJ-HEADER-FILE-SOFTWARE-PART-ENCODE-CRS-M1-00217` | 665/data-object predicate OBJ-HEADER-FILE-SOFTWARE-PART-ENCODE-CRS-M1-00217. |
| `TR-CRS-M1-00218-0260` | `CRS-M1-00218` | OBJECT-CONSTRAINT | `OBJ-HEADER-FILE-DEFINE-CRS-M1-00218` | 665/data-object predicate OBJ-HEADER-FILE-DEFINE-CRS-M1-00218. |
| `TR-CRS-M1-00219-0261` | `CRS-M1-00219` | OBJECT-CONSTRAINT | `OBJ-BINARY-FIELD-ENCODING-ENCODE-CRS-M1-00219` | 665/data-object predicate OBJ-BINARY-FIELD-ENCODING-ENCODE-CRS-M1-00219. |
| `TR-CRS-M1-00220-0262` | `CRS-M1-00220` | OBJECT-CONSTRAINT | `OBJ-OPERATION-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00220` | 665/data-object predicate OBJ-OPERATION-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00220. |
| `TR-CRS-M1-00221-0263` | `CRS-M1-00221` | OBJECT-CONSTRAINT | `OBJ-BINARY-FIELD-ENCODING-ENCODE-CRS-M1-00221` | 665/data-object predicate OBJ-BINARY-FIELD-ENCODING-ENCODE-CRS-M1-00221. |
| `TR-CRS-M1-00222-0264` | `CRS-M1-00222` | OBJECT-CONSTRAINT | `OBJ-TARGET-HARDWARE-ID-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00222` | 665/data-object predicate OBJ-TARGET-HARDWARE-ID-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00222. |
| `TR-CRS-M1-00223-0265` | `CRS-M1-00223` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-IMPLEMENT-CRS-M1-00223` | 665/data-object predicate OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-IMPLEMENT-CRS-M1-00223. |
| `TR-CRS-M1-00224-0266` | `CRS-M1-00224` | OBJECT-CONSTRAINT | `OBJ-NETWORK-INTERFACE-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00224` | 665/data-object predicate OBJ-NETWORK-INTERFACE-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00224. |
| `TR-CRS-M1-00225-0267` | `CRS-M1-00225` | OBJECT-CONSTRAINT | `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ENSURE-UNIQUE-CRS-M1-00225` | 665/data-object predicate OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ENSURE-UNIQUE-CRS-M1-00225. |
| `TR-CRS-M1-00226-0268` | `CRS-M1-00226` | OBJECT-CONSTRAINT | `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ENCODE-CRS-M1-00226` | 665/data-object predicate OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ENCODE-CRS-M1-00226. |
| `TR-CRS-M1-00227-0269` | `CRS-M1-00227` | OBJECT-CONSTRAINT | `OBJ-TARGET-HARDWARE-ID-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00227` | 665/data-object predicate OBJ-TARGET-HARDWARE-ID-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00227. |
| `TR-CRS-M1-00228-0270` | `CRS-M1-00228` | OBJECT-CONSTRAINT | `OBJ-DATA-FILE-CONSTRAIN-CRS-M1-00228` | 665/data-object predicate OBJ-DATA-FILE-CONSTRAIN-CRS-M1-00228. |
| `TR-CRS-M1-00229-0271` | `CRS-M1-00229` | OBJECT-CONSTRAINT | `OBJ-DATA-FILE-SET-ZERO-CRS-M1-00229` | 665/data-object predicate OBJ-DATA-FILE-SET-ZERO-CRS-M1-00229. |
| `TR-CRS-M1-00230-0272` | `CRS-M1-00230` | OBJECT-CONSTRAINT | `OBJ-DATA-FILE-FORMAT-CRS-M1-00230` | 665/data-object predicate OBJ-DATA-FILE-FORMAT-CRS-M1-00230. |
| `TR-CRS-M1-00231-0273` | `CRS-M1-00231` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00232-0274` | `CRS-M1-00232` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00233-0275` | `CRS-M1-00233` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00234-0276` | `CRS-M1-00234` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00235-0277` | `CRS-M1-00235` | OBJECT-CONSTRAINT | `OBJ-NETWORK-INTERFACE-ENCODE-CRS-M1-00235` | 665/data-object predicate OBJ-NETWORK-INTERFACE-ENCODE-CRS-M1-00235. |
| `TR-CRS-M1-00236-0278` | `CRS-M1-00236` | OBJECT-CONSTRAINT | `OBJ-NETWORK-INTERFACE-IMPLEMENT-CRS-M1-00236` | 665/data-object predicate OBJ-NETWORK-INTERFACE-IMPLEMENT-CRS-M1-00236. |
| `TR-CRS-M1-00237-0279` | `CRS-M1-00237` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-NETWORK-INTERFACE-ENCODE-CRS-M1-00237` | 665/data-object predicate OBJ-LOAD-PART-NUMBER-NETWORK-INTERFACE-ENCODE-CRS-M1-00237. |
| `TR-CRS-M1-00238-0280` | `CRS-M1-00238` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00239-0281` | `CRS-M1-00239` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00240-0282` | `CRS-M1-00240` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00241-0283` | `CRS-M1-00241` | OBJECT-CONSTRAINT | `OBJ-HEADER-FILE-VALIDATE-CRS-M1-00241` | 665/data-object predicate OBJ-HEADER-FILE-VALIDATE-CRS-M1-00241. |
| `TR-CRS-M1-00242-0284` | `CRS-M1-00242` | OBJECT-CONSTRAINT | `OBJ-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00242` | 665/data-object predicate OBJ-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00242. |
| `TR-CRS-M1-00243-0285` | `CRS-M1-00243` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00244-0286` | `CRS-M1-00244` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00245-0287` | `CRS-M1-00245` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00246-0288` | `CRS-M1-00246` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00247-0289` | `CRS-M1-00247` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00248-0290` | `CRS-M1-00248` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00249-0291` | `CRS-M1-00249` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00250-0292` | `CRS-M1-00250` | INTERFACE | `IF_INTEGRITY` | Integrity interface remains blocked by ARINC 645. |
| `TR-CRS-M1-00251-0293` | `CRS-M1-00251` | OBJECT-CONSTRAINT | `OBJ-DATA-FILE-SOFTWARE-PART-ENCODE-CRS-M1-00251` | 665/data-object predicate OBJ-DATA-FILE-SOFTWARE-PART-ENCODE-CRS-M1-00251. |
| `TR-CRS-M1-00252-0294` | `CRS-M1-00252` | OBJECT-CONSTRAINT | `OBJ-SOFTWARE-PART-NETWORK-INTERFACE-ENCODE-CRS-M1-00252` | 665/data-object predicate OBJ-SOFTWARE-PART-NETWORK-INTERFACE-ENCODE-CRS-M1-00252. |
| `TR-CRS-M1-00253-0295` | `CRS-M1-00253` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00254-0296` | `CRS-M1-00254` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00255-0297` | `CRS-M1-00255` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00256-0298` | `CRS-M1-00256` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00257-0299` | `CRS-M1-00257` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00258-0300` | `CRS-M1-00258` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00259-0301` | `CRS-M1-00259` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00260-0302` | `CRS-M1-00260` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00261-0303` | `CRS-M1-00261` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00262-0304` | `CRS-M1-00262` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00263-0305` | `CRS-M1-00263` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00264-0306` | `CRS-M1-00264` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00265-0307` | `CRS-M1-00265` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00266-0308` | `CRS-M1-00266` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00267-0309` | `CRS-M1-00267` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00268-0310` | `CRS-M1-00268` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00269-0311` | `CRS-M1-00269` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00270-0312` | `CRS-M1-00270` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00271-0313` | `CRS-M1-00271` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00272-0314` | `CRS-M1-00272` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00273-0315` | `CRS-M1-00273` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00274-0316` | `CRS-M1-00274` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00275-0317` | `CRS-M1-00275` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00276-0318` | `CRS-M1-00276` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00277-0319` | `CRS-M1-00277` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00278-0320` | `CRS-M1-00278` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00279-0321` | `CRS-M1-00279` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00280-0322` | `CRS-M1-00280` | SCOPE | `SCOPE` | Scope / deferred-service / profile constraint; not a file-variable stand-in. |
| `TR-CRS-M1-00281-0323` | `CRS-M1-00281` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00282-0324` | `CRS-M1-00282` | FIELD-CONSTRAINT | `FC-LCI-FIELD-FILE-LENGTH` | Field predicate FC-LCI-FIELD-FILE-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00283-0325` | `CRS-M1-00283` | FIELD-CONSTRAINT | `FC-LCI-FIELD-PROTOCOL-VERSION` | Field predicate FC-LCI-FIELD-PROTOCOL-VERSION at the named protocol file bytes. |
| `TR-CRS-M1-00284-0326` | `CRS-M1-00284` | FIELD-CONSTRAINT | `FC-LCI-FIELD-OPERATION-ACCEPTANCE-STATUS-CODE` | Field predicate FC-LCI-FIELD-OPERATION-ACCEPTANCE-STATUS-CODE at the named protocol file bytes. |
| `TR-CRS-M1-00285-0327` | `CRS-M1-00285` | FIELD-CONSTRAINT | `FC-LCI-FIELD-STATUS-DESCRIPTION-LENGTH` | Field predicate FC-LCI-FIELD-STATUS-DESCRIPTION-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00286-0328` | `CRS-M1-00286` | FIELD-CONSTRAINT | `FC-LCI-FIELD-STATUS-DESCRIPTION` | Field predicate FC-LCI-FIELD-STATUS-DESCRIPTION at the named protocol file bytes. |
| `TR-CRS-M1-00287-0329` | `CRS-M1-00287` | FIELD-CONSTRAINT | `FC-LCL-FIELD-FILE-LENGTH` | Field predicate FC-LCL-FIELD-FILE-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00288-0330` | `CRS-M1-00288` | FIELD-CONSTRAINT | `FC-LCL-FIELD-PROTOCOL-VERSION` | Field predicate FC-LCL-FIELD-PROTOCOL-VERSION at the named protocol file bytes. |
| `TR-CRS-M1-00289-0331` | `CRS-M1-00289` | FIELD-CONSTRAINT | `FC-LCL-FIELD-NUMBER-OF-TARGET-HARDWARE` | Field predicate FC-LCL-FIELD-NUMBER-OF-TARGET-HARDWARE at the named protocol file bytes. |
| `TR-CRS-M1-00290-0332` | `CRS-M1-00290` | FIELD-CONSTRAINT | `FC-LCL-FIELD-LITERAL-NAME-LENGTH` | Field predicate FC-LCL-FIELD-LITERAL-NAME-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00291-0333` | `CRS-M1-00291` | FIELD-CONSTRAINT | `FC-LCL-FIELD-LITERAL-NAME` | Field predicate FC-LCL-FIELD-LITERAL-NAME at the named protocol file bytes. |
| `TR-CRS-M1-00292-0334` | `CRS-M1-00292` | FIELD-CONSTRAINT | `FC-LCL-FIELD-SERIAL-NUMBER-LENGTH` | Field predicate FC-LCL-FIELD-SERIAL-NUMBER-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00293-0335` | `CRS-M1-00293` | FIELD-CONSTRAINT | `FC-LCL-FIELD-SERIAL-NUMBER` | Field predicate FC-LCL-FIELD-SERIAL-NUMBER at the named protocol file bytes. |
| `TR-CRS-M1-00294-0336` | `CRS-M1-00294` | FIELD-CONSTRAINT | `FC-LCL-FIELD-NUMBER-OF-PART-NUMBERS` | Field predicate FC-LCL-FIELD-NUMBER-OF-PART-NUMBERS at the named protocol file bytes. |
| `TR-CRS-M1-00295-0337` | `CRS-M1-00295` | FIELD-CONSTRAINT | `FC-LCL-FIELD-PART-NUMBER-LENGTH` | Field predicate FC-LCL-FIELD-PART-NUMBER-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00296-0338` | `CRS-M1-00296` | FIELD-CONSTRAINT | `FC-LCL-FIELD-PART-NUMBER` | Field predicate FC-LCL-FIELD-PART-NUMBER at the named protocol file bytes. |
| `TR-CRS-M1-00297-0339` | `CRS-M1-00297` | FIELD-CONSTRAINT | `FC-LCL-FIELD-AMENDMENT-LENGTH` | Field predicate FC-LCL-FIELD-AMENDMENT-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00298-0340` | `CRS-M1-00298` | FIELD-CONSTRAINT | `FC-LCL-FIELD-AMENDMENT` | Field predicate FC-LCL-FIELD-AMENDMENT at the named protocol file bytes. |
| `TR-CRS-M1-00299-0341` | `CRS-M1-00299` | FIELD-CONSTRAINT | `FC-LCL-FIELD-PART-DESIGNATION-LENGTH` | Field predicate FC-LCL-FIELD-PART-DESIGNATION-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00300-0342` | `CRS-M1-00300` | FIELD-CONSTRAINT | `FC-LCL-FIELD-PART-DESIGNATION-TEXT` | Field predicate FC-LCL-FIELD-PART-DESIGNATION-TEXT at the named protocol file bytes. |
| `TR-CRS-M1-00301-0343` | `CRS-M1-00301` | FIELD-CONSTRAINT | `FC-LCS-FIELD-FILE-LENGTH` | Field predicate FC-LCS-FIELD-FILE-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00302-0344` | `CRS-M1-00302` | FIELD-CONSTRAINT | `FC-LCS-FIELD-PROTOCOL-VERSION` | Field predicate FC-LCS-FIELD-PROTOCOL-VERSION at the named protocol file bytes. |
| `TR-CRS-M1-00303-0345` | `CRS-M1-00303` | FIELD-CONSTRAINT | `FC-LCS-FIELD-COUNTER` | Field predicate FC-LCS-FIELD-COUNTER at the named protocol file bytes. |
| `TR-CRS-M1-00304-0346` | `CRS-M1-00304` | FIELD-CONSTRAINT | `FC-LCS-FIELD-INFORMATION-OPERATION-STATUS-CODE` | Field predicate FC-LCS-FIELD-INFORMATION-OPERATION-STATUS-CODE at the named protocol file bytes. |
| `TR-CRS-M1-00305-0347` | `CRS-M1-00305` | FIELD-CONSTRAINT | `FC-LCS-FIELD-EXCEPTION-TIMER` | Field predicate FC-LCS-FIELD-EXCEPTION-TIMER at the named protocol file bytes. |
| `TR-CRS-M1-00305-0348` | `CRS-M1-00305` | TIMING | `TIM-CRS-M1-00305` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00305-0349` | `CRS-M1-00305` | CLOCK | `CLK_EXCEPTION` | Clock used by this timing obligation. |
| `TR-CRS-M1-00306-0350` | `CRS-M1-00306` | FIELD-CONSTRAINT | `FC-LCS-FIELD-ESTIMATED-TIME` | Field predicate FC-LCS-FIELD-ESTIMATED-TIME at the named protocol file bytes. |
| `TR-CRS-M1-00307-0351` | `CRS-M1-00307` | FIELD-CONSTRAINT | `FC-LCS-FIELD-STATUS-DESCRIPTION-LENGTH` | Field predicate FC-LCS-FIELD-STATUS-DESCRIPTION-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00308-0352` | `CRS-M1-00308` | FIELD-CONSTRAINT | `FC-LCS-FIELD-STATUS-DESCRIPTION` | Field predicate FC-LCS-FIELD-STATUS-DESCRIPTION at the named protocol file bytes. |
| `TR-CRS-M1-00309-0353` | `CRS-M1-00309` | FIELD-CONSTRAINT | `FC-LUR-FIELD-FILE-LENGTH` | Field predicate FC-LUR-FIELD-FILE-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00310-0354` | `CRS-M1-00310` | FIELD-CONSTRAINT | `FC-LUR-FIELD-PROTOCOL-VERSION` | Field predicate FC-LUR-FIELD-PROTOCOL-VERSION at the named protocol file bytes. |
| `TR-CRS-M1-00311-0355` | `CRS-M1-00311` | FIELD-CONSTRAINT | `FC-LUR-FIELD-NUMBER-OF-HEADER-FILES` | Field predicate FC-LUR-FIELD-NUMBER-OF-HEADER-FILES at the named protocol file bytes. |
| `TR-CRS-M1-00312-0356` | `CRS-M1-00312` | FIELD-CONSTRAINT | `FC-LUR-FIELD-HEADER-FILE-NAME-LENGTH` | Field predicate FC-LUR-FIELD-HEADER-FILE-NAME-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00313-0357` | `CRS-M1-00313` | FIELD-CONSTRAINT | `FC-LUR-FIELD-HEADER-FILE-NAME` | Field predicate FC-LUR-FIELD-HEADER-FILE-NAME at the named protocol file bytes. |
| `TR-CRS-M1-00314-0358` | `CRS-M1-00314` | FIELD-CONSTRAINT | `FC-LUR-FIELD-LOAD-PART-NUMBER-NAME-LENGTH` | Field predicate FC-LUR-FIELD-LOAD-PART-NUMBER-NAME-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00315-0359` | `CRS-M1-00315` | FIELD-CONSTRAINT | `FC-LUR-FIELD-LOAD-PART-NUMBER-NAME` | Field predicate FC-LUR-FIELD-LOAD-PART-NUMBER-NAME at the named protocol file bytes. |
| `TR-CRS-M1-00316-0360` | `CRS-M1-00316` | FIELD-CONSTRAINT | `FC-LUS-FIELD-FILE-LENGTH` | Field predicate FC-LUS-FIELD-FILE-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00317-0361` | `CRS-M1-00317` | FIELD-CONSTRAINT | `FC-LUS-FIELD-PROTOCOL-VERSION` | Field predicate FC-LUS-FIELD-PROTOCOL-VERSION at the named protocol file bytes. |
| `TR-CRS-M1-00318-0362` | `CRS-M1-00318` | FIELD-CONSTRAINT | `FC-LUS-FIELD-UPLOAD-OPERATION-STATUS-CODE` | Field predicate FC-LUS-FIELD-UPLOAD-OPERATION-STATUS-CODE at the named protocol file bytes. |
| `TR-CRS-M1-00319-0363` | `CRS-M1-00319` | FIELD-CONSTRAINT | `FC-LUS-FIELD-UPLOAD-STATUS-DESCRIPTION-LENGTH` | Field predicate FC-LUS-FIELD-UPLOAD-STATUS-DESCRIPTION-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00320-0364` | `CRS-M1-00320` | FIELD-CONSTRAINT | `FC-LUS-FIELD-UPLOAD-STATUS-DESCRIPTION` | Field predicate FC-LUS-FIELD-UPLOAD-STATUS-DESCRIPTION at the named protocol file bytes. |
| `TR-CRS-M1-00321-0365` | `CRS-M1-00321` | FIELD-CONSTRAINT | `FC-LUS-FIELD-COUNTER` | Field predicate FC-LUS-FIELD-COUNTER at the named protocol file bytes. |
| `TR-CRS-M1-00322-0366` | `CRS-M1-00322` | FIELD-CONSTRAINT | `FC-LUS-FIELD-EXCEPTION-TIMER` | Field predicate FC-LUS-FIELD-EXCEPTION-TIMER at the named protocol file bytes. |
| `TR-CRS-M1-00322-0367` | `CRS-M1-00322` | TIMING | `TIM-CRS-M1-00322` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00322-0368` | `CRS-M1-00322` | CLOCK | `CLK_EXCEPTION` | Clock used by this timing obligation. |
| `TR-CRS-M1-00323-0369` | `CRS-M1-00323` | FIELD-CONSTRAINT | `FC-LUS-FIELD-ESTIMATED-TIME` | Field predicate FC-LUS-FIELD-ESTIMATED-TIME at the named protocol file bytes. |
| `TR-CRS-M1-00324-0370` | `CRS-M1-00324` | FIELD-CONSTRAINT | `FC-LUS-FIELD-LOAD-LIST-RATIO` | Field predicate FC-LUS-FIELD-LOAD-LIST-RATIO at the named protocol file bytes. |
| `TR-CRS-M1-00325-0371` | `CRS-M1-00325` | FIELD-CONSTRAINT | `FC-LUS-FIELD-NUMBER-OF-HEADER-FILES` | Field predicate FC-LUS-FIELD-NUMBER-OF-HEADER-FILES at the named protocol file bytes. |
| `TR-CRS-M1-00326-0372` | `CRS-M1-00326` | FIELD-CONSTRAINT | `FC-LUS-FIELD-HEADER-FILE-NAME-LENGTH` | Field predicate FC-LUS-FIELD-HEADER-FILE-NAME-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00327-0373` | `CRS-M1-00327` | FIELD-CONSTRAINT | `FC-LUS-FIELD-HEADER-FILE-NAME` | Field predicate FC-LUS-FIELD-HEADER-FILE-NAME at the named protocol file bytes. |
| `TR-CRS-M1-00328-0374` | `CRS-M1-00328` | FIELD-CONSTRAINT | `FC-LUS-FIELD-LOAD-PART-NUMBER-NAME-LENGTH` | Field predicate FC-LUS-FIELD-LOAD-PART-NUMBER-NAME-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00329-0375` | `CRS-M1-00329` | FIELD-CONSTRAINT | `FC-LUS-FIELD-LOAD-PART-NUMBER-NAME` | Field predicate FC-LUS-FIELD-LOAD-PART-NUMBER-NAME at the named protocol file bytes. |
| `TR-CRS-M1-00330-0376` | `CRS-M1-00330` | FIELD-CONSTRAINT | `FC-LUS-FIELD-LOAD-RATIO` | Field predicate FC-LUS-FIELD-LOAD-RATIO at the named protocol file bytes. |
| `TR-CRS-M1-00331-0377` | `CRS-M1-00331` | FIELD-CONSTRAINT | `FC-LUS-FIELD-LOAD-STATUS` | Field predicate FC-LUS-FIELD-LOAD-STATUS at the named protocol file bytes. |
| `TR-CRS-M1-00332-0378` | `CRS-M1-00332` | FIELD-CONSTRAINT | `FC-LUS-FIELD-LOAD-STATUS-DESCRIPTION-LENGTH` | Field predicate FC-LUS-FIELD-LOAD-STATUS-DESCRIPTION-LENGTH at the named protocol file bytes. |
| `TR-CRS-M1-00333-0379` | `CRS-M1-00333` | FIELD-CONSTRAINT | `FC-LUS-FIELD-LOAD-STATUS-DESCRIPTION` | Field predicate FC-LUS-FIELD-LOAD-STATUS-DESCRIPTION at the named protocol file bytes. |
| `TR-CRS-M1-00334-0380` | `CRS-M1-00334` | STATUS-CONSTRAINT | `ST-CRS-M1-00334` | Status-code predicate ST-CRS-M1-00334. |
| `TR-CRS-M1-00335-0381` | `CRS-M1-00335` | STATUS-CONSTRAINT | `ST-CRS-M1-00335` | Status-code predicate ST-CRS-M1-00335. |
| `TR-CRS-M1-00336-0382` | `CRS-M1-00336` | STATUS-CONSTRAINT | `ST-CRS-M1-00336` | Status-code predicate ST-CRS-M1-00336. |
| `TR-CRS-M1-00337-0383` | `CRS-M1-00337` | STATUS-CONSTRAINT | `ST-CRS-M1-00337` | Status-code predicate ST-CRS-M1-00337. |
| `TR-CRS-M1-00338-0384` | `CRS-M1-00338` | STATUS-CONSTRAINT | `ST-CRS-M1-00338` | Status-code predicate ST-CRS-M1-00338. |
| `TR-CRS-M1-00339-0385` | `CRS-M1-00339` | STATUS-CONSTRAINT | `ST-CRS-M1-00339` | Status-code predicate ST-CRS-M1-00339. |
| `TR-CRS-M1-00340-0386` | `CRS-M1-00340` | STATUS-CONSTRAINT | `ST-CRS-M1-00340` | Status-code predicate ST-CRS-M1-00340. |
| `TR-CRS-M1-00340-0463` | `CRS-M1-00340` | TRANSITION | `T_ABORT_TH` | Transition T_ABORT_TH cites this obligation. |
| `TR-CRS-M1-00340-0464` | `CRS-M1-00340` | TRANSITION | `T_ABORTED` | Transition T_ABORTED cites this obligation. |
| `TR-CRS-M1-00341-0387` | `CRS-M1-00341` | STATUS-CONSTRAINT | `ST-CRS-M1-00341` | Status-code predicate ST-CRS-M1-00341. |
| `TR-CRS-M1-00341-0462` | `CRS-M1-00341` | TRANSITION | `T_ABORT_DL` | Transition T_ABORT_DL cites this obligation. |
| `TR-CRS-M1-00341-0465` | `CRS-M1-00341` | TRANSITION | `T_ABORTED` | Transition T_ABORTED cites this obligation. |
| `TR-CRS-M1-00341-0466` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_INF_LCI_RRQ` | Transition T_ABORT_FROM_S_INF_LCI_RRQ cites this obligation. |
| `TR-CRS-M1-00341-0467` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_INF_LCL_XFER` | Transition T_ABORT_FROM_S_INF_LCL_XFER cites this obligation. |
| `TR-CRS-M1-00341-0468` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_INF_LCS_XFER` | Transition T_ABORT_FROM_S_INF_LCS_XFER cites this obligation. |
| `TR-CRS-M1-00341-0469` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_INF_EXCEPTION` | Transition T_ABORT_FROM_S_INF_EXCEPTION cites this obligation. |
| `TR-CRS-M1-00341-0470` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_WAIT_RETRY` | Transition T_ABORT_FROM_S_WAIT_RETRY cites this obligation. |
| `TR-CRS-M1-00341-0471` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_UPL_LUI_XFER` | Transition T_ABORT_FROM_S_UPL_LUI_XFER cites this obligation. |
| `TR-CRS-M1-00341-0472` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_UPL_LIST_SENT` | Transition T_ABORT_FROM_S_UPL_LIST_SENT cites this obligation. |
| `TR-CRS-M1-00341-0473` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_UPL_WAIT_LUS0001` | Transition T_ABORT_FROM_S_UPL_WAIT_LUS0001 cites this obligation. |
| `TR-CRS-M1-00341-0474` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_UPL_LUR_XFER` | Transition T_ABORT_FROM_S_UPL_LUR_XFER cites this obligation. |
| `TR-CRS-M1-00341-0475` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_UPL_LUS_XFER` | Transition T_ABORT_FROM_S_UPL_LUS_XFER cites this obligation. |
| `TR-CRS-M1-00342-0388` | `CRS-M1-00342` | STATUS-CONSTRAINT | `ST-CRS-M1-00342` | Status-code predicate ST-CRS-M1-00342. |
| `TR-CRS-M1-00343-0389` | `CRS-M1-00343` | STATUS-CONSTRAINT | `ST-CRS-M1-00343` | Status-code predicate ST-CRS-M1-00343. |
| `TR-CRS-M1-00344-0390` | `CRS-M1-00344` | SCOPE | `SCOPE` | DOWNLOAD-only status code remains out of this UPLOAD/INFORMATION candidate. |
| `TR-CRS-M1-00345-0391` | `CRS-M1-00345` | STATUS-CONSTRAINT | `ST-CRS-M1-00345` | Status-code predicate ST-CRS-M1-00345. |
| `TR-CRS-M1-00346-0392` | `CRS-M1-00346` | TRANSITION | `T_INF_LCI_RRQ` | Sequence-chart obligation maps to T_INF_LCI_RRQ. |
| `TR-CRS-M1-00347-0393` | `CRS-M1-00347` | TRANSITION | `T_INF_LCI_RRQ` | Sequence-chart obligation maps to T_INF_LCI_RRQ. |
| `TR-CRS-M1-00348-0394` | `CRS-M1-00348` | TRANSITION | `T_INF_LCI_XFER` | Sequence-chart obligation maps to T_INF_LCI_XFER. |
| `TR-CRS-M1-00349-0395` | `CRS-M1-00349` | TRANSITION | `T_INF_EVAL` | Sequence-chart obligation maps to T_INF_EVAL. |
| `TR-CRS-M1-00349-0396` | `CRS-M1-00349` | TRANSITION | `T_INF_ACCEPT_INIT` | Sequence-chart obligation maps to T_INF_ACCEPT_INIT. |
| `TR-CRS-M1-00350-0397` | `CRS-M1-00350` | TRANSITION | `T_INF_REJECT` | Sequence-chart obligation maps to T_INF_REJECT. |
| `TR-CRS-M1-00351-0398` | `CRS-M1-00351` | TRANSITION | `T_INF_LCL_WRQ` | Sequence-chart obligation maps to T_INF_LCL_WRQ. |
| `TR-CRS-M1-00351-0441` | `CRS-M1-00351` | TRANSITION | `T_INF_ACCEPT_INIT` | Transition T_INF_ACCEPT_INIT cites this obligation. |
| `TR-CRS-M1-00352-0399` | `CRS-M1-00352` | TRANSITION | `T_INF_LCL_ACK` | Sequence-chart obligation maps to T_INF_LCL_ACK. |
| `TR-CRS-M1-00353-0400` | `CRS-M1-00353` | TRANSITION | `T_INF_LCL_XFER` | Sequence-chart obligation maps to T_INF_LCL_XFER. |
| `TR-CRS-M1-00354-0401` | `CRS-M1-00354` | TRANSITION | `T_INF_APP` | Sequence-chart obligation maps to T_INF_APP. |
| `TR-CRS-M1-00355-0402` | `CRS-M1-00355` | TRANSITION | `T_INF_LCS_WRQ` | Sequence-chart obligation maps to T_INF_LCS_WRQ. |
| `TR-CRS-M1-00356-0403` | `CRS-M1-00356` | TRANSITION | `T_INF_LCS_XFER` | Sequence-chart obligation maps to T_INF_LCS_XFER. |
| `TR-CRS-M1-00357-0404` | `CRS-M1-00357` | TRANSITION | `T_INF_LCS_XFER` | Sequence-chart obligation maps to T_INF_LCS_XFER. |
| `TR-CRS-M1-00358-0405` | `CRS-M1-00358` | TRANSITION | `T_INF_LCS_XFER` | Sequence-chart obligation maps to T_INF_LCS_XFER. |
| `TR-CRS-M1-00358-0406` | `CRS-M1-00358` | TRANSITION | `T_INF_SESSION_END` | Sequence-chart obligation maps to T_INF_SESSION_END. |
| `TR-CRS-M1-00359-0407` | `CRS-M1-00359` | TRANSITION | `T_UPL_LUI_RRQ` | Sequence-chart obligation maps to T_UPL_LUI_RRQ. |
| `TR-CRS-M1-00360-0408` | `CRS-M1-00360` | TRANSITION | `T_UPL_LUI_RRQ` | Sequence-chart obligation maps to T_UPL_LUI_RRQ. |
| `TR-CRS-M1-00360-0409` | `CRS-M1-00360` | TRANSITION | `T_UPL_LUI_RRQ_AFTER_INF` | Sequence-chart obligation maps to T_UPL_LUI_RRQ_AFTER_INF. |
| `TR-CRS-M1-00361-0410` | `CRS-M1-00361` | TRANSITION | `T_UPL_LUI_XFER` | Sequence-chart obligation maps to T_UPL_LUI_XFER. |
| `TR-CRS-M1-00362-0411` | `CRS-M1-00362` | TRANSITION | `T_UPL_EVAL` | Sequence-chart obligation maps to T_UPL_EVAL. |
| `TR-CRS-M1-00362-0412` | `CRS-M1-00362` | TRANSITION | `T_UPL_ACCEPT_INIT` | Sequence-chart obligation maps to T_UPL_ACCEPT_INIT. |
| `TR-CRS-M1-00362-0413` | `CRS-M1-00362` | TRANSITION | `T_UPL_REJECT` | Sequence-chart obligation maps to T_UPL_REJECT. |
| `TR-CRS-M1-00363-0414` | `CRS-M1-00363` | TRANSITION | `T_UPL_ACCEPT_INIT` | Sequence-chart obligation maps to T_UPL_ACCEPT_INIT. |
| `TR-CRS-M1-00363-0415` | `CRS-M1-00363` | TRANSITION | `T_UPL_LIST_OFFER` | Sequence-chart obligation maps to T_UPL_LIST_OFFER. |
| `TR-CRS-M1-00364-0416` | `CRS-M1-00364` | TRANSITION | `T_UPL_LIST_OFFER` | Sequence-chart obligation maps to T_UPL_LIST_OFFER. |
| `TR-CRS-M1-00364-0417` | `CRS-M1-00364` | TRANSITION | `T_UPL_WAIT_LUS0001` | Sequence-chart obligation maps to T_UPL_WAIT_LUS0001. |
| `TR-CRS-M1-00365-0418` | `CRS-M1-00365` | TRANSITION | `T_UPL_LUR_WRQ` | Sequence-chart obligation maps to T_UPL_LUR_WRQ. |
| `TR-CRS-M1-00366-0419` | `CRS-M1-00366` | TRANSITION | `T_UPL_LUR_ACK` | Sequence-chart obligation maps to T_UPL_LUR_ACK. |
| `TR-CRS-M1-00367-0420` | `CRS-M1-00367` | TRANSITION | `T_UPL_LUR_XFER` | Sequence-chart obligation maps to T_UPL_LUR_XFER. |
| `TR-CRS-M1-00368-0421` | `CRS-M1-00368` | TRANSITION | `T_UPL_FILE_RRQ` | Sequence-chart obligation maps to T_UPL_FILE_RRQ. |
| `TR-CRS-M1-00368-0422` | `CRS-M1-00368` | TRANSITION | `T_UPL_FILE_RRQ_MORE` | Sequence-chart obligation maps to T_UPL_FILE_RRQ_MORE. |
| `TR-CRS-M1-00369-0423` | `CRS-M1-00369` | TRANSITION | `T_UPL_FILE_UNAVAIL` | Sequence-chart obligation maps to T_UPL_FILE_UNAVAIL. |
| `TR-CRS-M1-00370-0424` | `CRS-M1-00370` | TRANSITION | `T_UPL_FILE_XFER` | Sequence-chart obligation maps to T_UPL_FILE_XFER. |
| `TR-CRS-M1-00371-0425` | `CRS-M1-00371` | TRANSITION | `T_UPL_FILE_STATUS` | Sequence-chart obligation maps to T_UPL_FILE_STATUS. |
| `TR-CRS-M1-00372-0426` | `CRS-M1-00372` | TRANSITION | `T_UPL_MORE_FILES` | Sequence-chart obligation maps to T_UPL_MORE_FILES. |
| `TR-CRS-M1-00372-0427` | `CRS-M1-00372` | TRANSITION | `T_UPL_FILE_RRQ_MORE` | Sequence-chart obligation maps to T_UPL_FILE_RRQ_MORE. |
| `TR-CRS-M1-00373-0428` | `CRS-M1-00373` | TRANSITION | `T_UPL_TO_LUS` | Sequence-chart obligation maps to T_UPL_TO_LUS. |
| `TR-CRS-M1-00374-0429` | `CRS-M1-00374` | TRANSITION | `T_UPL_LUS_XFER` | Sequence-chart obligation maps to T_UPL_LUS_XFER. |
| `TR-CRS-M1-00375-0430` | `CRS-M1-00375` | TRANSITION | `T_UPL_STATUS_APP` | Sequence-chart obligation maps to T_UPL_STATUS_APP. |
| `TR-CRS-M1-00376-0431` | `CRS-M1-00376` | TRANSITION | `T_UPL_COMPLETE` | Sequence-chart obligation maps to T_UPL_COMPLETE. |
| `TR-CRS-M1-00376-0432` | `CRS-M1-00376` | TRANSITION | `T_UPL_STATUS_REPEAT` | Sequence-chart obligation maps to T_UPL_STATUS_REPEAT. |
| `TR-CRS-M1-00377-0433` | `CRS-M1-00377` | SCOPE | `SCOPE` | Non-behavior / profile obligation RECEIVE kept as a scope or applicability constraint. |
| `TR-CRS-M1-00378-0434` | `CRS-M1-00378` | SCOPE | `SCOPE` | Non-behavior / profile obligation WAIT kept as a scope or applicability constraint. |
| `TR-CRS-M1-00379-0435` | `CRS-M1-00379` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND-TFTP-WRITE-REQUEST kept as a scope or applicability constraint. |
| `TR-CRS-M1-00380-0436` | `CRS-M1-00380` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00381-0437` | `CRS-M1-00381` | SCOPE | `SCOPE` | Non-behavior / profile obligation STOP kept as a scope or applicability constraint. |
| `TR-CRS-M1-00382-0438` | `CRS-M1-00382` | INTERFACE | `IF_TFTP` | TFTP interface premise for TRANSFER. |
| `TR-CRS-M1-00383-0439` | `CRS-M1-00383` | SCOPE | `SCOPE` | Non-behavior / profile obligation SEND kept as a scope or applicability constraint. |
| `TR-CRS-M1-00384-0440` | `CRS-M1-00384` | SCOPE | `SCOPE` | Non-behavior / profile obligation TERMINATE kept as a scope or applicability constraint. |
| `TR-CRS-M1-00385-0476` | `CRS-M1-00385` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00386-0477` | `CRS-M1-00386` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00387-0478` | `CRS-M1-00387` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00388-0479` | `CRS-M1-00388` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00389-0480` | `CRS-M1-00389` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00390-0481` | `CRS-M1-00390` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00391-0482` | `CRS-M1-00391` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00391-0618` | `CRS-M1-00391` | TIMING | `TIM-CRS-M1-00391` | FIND timing is catalogued for later error-interval judgement; bound M2 does not run FIND. |
| `TR-CRS-M1-00391-0619` | `CRS-M1-00391` | CLOCK | `CLK_FIND` | FIND clock is observational in the catalog only. |
| `TR-CRS-M1-00392-0483` | `CRS-M1-00392` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00393-0484` | `CRS-M1-00393` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00394-0485` | `CRS-M1-00394` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00395-0486` | `CRS-M1-00395` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00396-0487` | `CRS-M1-00396` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00397-0488` | `CRS-M1-00397` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00398-0489` | `CRS-M1-00398` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00399-0490` | `CRS-M1-00399` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00400-0491` | `CRS-M1-00400` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00401-0492` | `CRS-M1-00401` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00402-0493` | `CRS-M1-00402` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00403-0494` | `CRS-M1-00403` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00404-0495` | `CRS-M1-00404` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00405-0496` | `CRS-M1-00405` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00406-0497` | `CRS-M1-00406` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00407-0498` | `CRS-M1-00407` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00408-0499` | `CRS-M1-00408` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00409-0500` | `CRS-M1-00409` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00410-0501` | `CRS-M1-00410` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00411-0502` | `CRS-M1-00411` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00412-0503` | `CRS-M1-00412` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00413-0504` | `CRS-M1-00413` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00414-0505` | `CRS-M1-00414` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00415-0506` | `CRS-M1-00415` | SCOPE | `SCOPE` | FIND obligation is recorded in expanded CRS; bound M2 does not model FIND behavior. |
| `TR-CRS-M1-00416-0507` | `CRS-M1-00416` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00417-0508` | `CRS-M1-00417` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00418-0509` | `CRS-M1-00418` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00419-0510` | `CRS-M1-00419` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00420-0511` | `CRS-M1-00420` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00421-0512` | `CRS-M1-00421` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00422-0513` | `CRS-M1-00422` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00423-0514` | `CRS-M1-00423` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00424-0515` | `CRS-M1-00424` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00426-0517` | `CRS-M1-00426` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00427-0518` | `CRS-M1-00427` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00428-0519` | `CRS-M1-00428` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00429-0520` | `CRS-M1-00429` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00430-0521` | `CRS-M1-00430` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00431-0522` | `CRS-M1-00431` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00432-0523` | `CRS-M1-00432` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00433-0524` | `CRS-M1-00433` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00434-0525` | `CRS-M1-00434` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00435-0526` | `CRS-M1-00435` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00436-0527` | `CRS-M1-00436` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00437-0528` | `CRS-M1-00437` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00438-0529` | `CRS-M1-00438` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00439-0530` | `CRS-M1-00439` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00440-0531` | `CRS-M1-00440` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00441-0532` | `CRS-M1-00441` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00442-0533` | `CRS-M1-00442` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00443-0534` | `CRS-M1-00443` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00444-0535` | `CRS-M1-00444` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00445-0536` | `CRS-M1-00445` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00446-0537` | `CRS-M1-00446` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00447-0538` | `CRS-M1-00447` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00448-0539` | `CRS-M1-00448` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00449-0540` | `CRS-M1-00449` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00450-0541` | `CRS-M1-00450` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00451-0542` | `CRS-M1-00451` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00452-0543` | `CRS-M1-00452` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00453-0544` | `CRS-M1-00453` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00454-0545` | `CRS-M1-00454` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00455-0546` | `CRS-M1-00455` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00456-0547` | `CRS-M1-00456` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00457-0548` | `CRS-M1-00457` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00458-0549` | `CRS-M1-00458` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00459-0550` | `CRS-M1-00459` | FIELD-CONSTRAINT | `FC-LNR-FIELD-FILE-LENGTH` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00460-0551` | `CRS-M1-00460` | FIELD-CONSTRAINT | `FC-LNR-FIELD-PROTOCOL-VERSION` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00461-0552` | `CRS-M1-00461` | FIELD-CONSTRAINT | `FC-LNR-FIELD-NUMBER-OF-FILES` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00462-0553` | `CRS-M1-00462` | FIELD-CONSTRAINT | `FC-LNR-FIELD-FILE-NAME-LENGTH` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00463-0554` | `CRS-M1-00463` | FIELD-CONSTRAINT | `FC-LNR-FIELD-FILE-NAME` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00464-0555` | `CRS-M1-00464` | FIELD-CONSTRAINT | `FC-LNR-FIELD-USER-DEFINED-DATA-LENGTH` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00465-0556` | `CRS-M1-00465` | FIELD-CONSTRAINT | `FC-LNR-FIELD-USER-DEFINED-DATA` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00466-0557` | `CRS-M1-00466` | FIELD-CONSTRAINT | `FC-LNS-FIELD-FILE-LENGTH` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00467-0558` | `CRS-M1-00467` | FIELD-CONSTRAINT | `FC-LNS-FIELD-PROTOCOL-VERSION` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00468-0559` | `CRS-M1-00468` | FIELD-CONSTRAINT | `FC-LNS-FIELD-DOWNLOAD-OPERATION-STATUS-CODE` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00469-0560` | `CRS-M1-00469` | FIELD-CONSTRAINT | `FC-LNS-FIELD-DOWNLOAD-STATUS-DESCRIPTION-LENGTH` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00470-0561` | `CRS-M1-00470` | FIELD-CONSTRAINT | `FC-LNS-FIELD-DOWNLOAD-STATUS-DESCRIPTION` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00471-0562` | `CRS-M1-00471` | FIELD-CONSTRAINT | `FC-LNS-FIELD-COUNTER` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00472-0563` | `CRS-M1-00472` | FIELD-CONSTRAINT | `FC-LNS-FIELD-EXCEPTION-TIMER` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00473-0564` | `CRS-M1-00473` | FIELD-CONSTRAINT | `FC-LNS-FIELD-ESTIMATED-TIME` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00474-0565` | `CRS-M1-00474` | FIELD-CONSTRAINT | `FC-LNS-FIELD-DOWNLOAD-LIST-RATIO` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00475-0566` | `CRS-M1-00475` | FIELD-CONSTRAINT | `FC-LNS-FIELD-NUMBER-OF-FILES` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00476-0567` | `CRS-M1-00476` | FIELD-CONSTRAINT | `FC-LNS-FIELD-FILE-NAME-LENGTH` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00477-0568` | `CRS-M1-00477` | FIELD-CONSTRAINT | `FC-LNS-FIELD-FILE-NAME` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00478-0569` | `CRS-M1-00478` | FIELD-CONSTRAINT | `FC-LNS-FIELD-FILE-STATUS` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00479-0570` | `CRS-M1-00479` | FIELD-CONSTRAINT | `FC-LNS-FIELD-FILE-STATUS-DESCRIPTION-LENGTH` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00480-0571` | `CRS-M1-00480` | FIELD-CONSTRAINT | `FC-LNS-FIELD-FILE-STATUS-DESCRIPTION` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00481-0572` | `CRS-M1-00481` | FIELD-CONSTRAINT | `FC-LNL-FIELD-FILE-LENGTH` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00482-0573` | `CRS-M1-00482` | FIELD-CONSTRAINT | `FC-LNL-FIELD-PROTOCOL-VERSION` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00483-0574` | `CRS-M1-00483` | FIELD-CONSTRAINT | `FC-LNL-FIELD-NUMBER-OF-FILES` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00484-0575` | `CRS-M1-00484` | FIELD-CONSTRAINT | `FC-LNL-FIELD-FILE-NAME-LENGTH` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00485-0576` | `CRS-M1-00485` | FIELD-CONSTRAINT | `FC-LNL-FIELD-FILE-NAME` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00486-0577` | `CRS-M1-00486` | FIELD-CONSTRAINT | `FC-LNL-FIELD-FILE-DESCRIPTION-LENGTH` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00487-0578` | `CRS-M1-00487` | FIELD-CONSTRAINT | `FC-LNL-FIELD-FILE-DESCRIPTION` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00488-0579` | `CRS-M1-00488` | FIELD-CONSTRAINT | `FC-LNA-FIELD-FILE-LENGTH` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00489-0580` | `CRS-M1-00489` | FIELD-CONSTRAINT | `FC-LNA-FIELD-PROTOCOL-VERSION` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00490-0581` | `CRS-M1-00490` | FIELD-CONSTRAINT | `FC-LNA-FIELD-NUMBER-OF-FILES` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00491-0582` | `CRS-M1-00491` | FIELD-CONSTRAINT | `FC-LNA-FIELD-FILE-NAME-LENGTH` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00492-0583` | `CRS-M1-00492` | FIELD-CONSTRAINT | `FC-LNA-FIELD-FILE-NAME` | DOWNLOAD field constraint is recorded; bound M2 does not model DOWNLOAD behavior. |
| `TR-CRS-M1-00493-0584` | `CRS-M1-00493` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00494-0585` | `CRS-M1-00494` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00495-0586` | `CRS-M1-00495` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00496-0587` | `CRS-M1-00496` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00497-0588` | `CRS-M1-00497` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00498-0589` | `CRS-M1-00498` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00499-0590` | `CRS-M1-00499` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00500-0591` | `CRS-M1-00500` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00501-0592` | `CRS-M1-00501` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00502-0593` | `CRS-M1-00502` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00503-0594` | `CRS-M1-00503` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00504-0595` | `CRS-M1-00504` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00505-0596` | `CRS-M1-00505` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00506-0597` | `CRS-M1-00506` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00507-0598` | `CRS-M1-00507` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00508-0599` | `CRS-M1-00508` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00509-0600` | `CRS-M1-00509` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00510-0601` | `CRS-M1-00510` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00511-0602` | `CRS-M1-00511` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00512-0603` | `CRS-M1-00512` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00513-0604` | `CRS-M1-00513` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00514-0605` | `CRS-M1-00514` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00515-0606` | `CRS-M1-00515` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00516-0607` | `CRS-M1-00516` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00517-0608` | `CRS-M1-00517` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00518-0609` | `CRS-M1-00518` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00519-0610` | `CRS-M1-00519` | SCOPE | `SCOPE` | DOWNLOAD/AFDX obligation is recorded in expanded CRS; bound M2 does not model that behavior. |
| `TR-CRS-M1-00520-0611` | `CRS-M1-00520` | SCOPE | `SCOPE` | Expanded CRS recorded; bound M2 does not execute FIND/DOWNLOAD. |
| `TR-CRS-M1-00520-0612` | `CRS-M1-00520` | TIMING | `TIM-CRS-M1-00520` | Expanded CRS recorded; bound M2 does not execute FIND/DOWNLOAD. |
| `TR-CRS-M1-00520-0613` | `CRS-M1-00520` | CLOCK | `CLK_FIND` | Expanded CRS recorded; bound M2 does not execute FIND/DOWNLOAD. |
| `TR-CRS-M1-00521-0614` | `CRS-M1-00521` | SCOPE | `SCOPE` | Expanded CRS recorded; bound M2 does not execute FIND/DOWNLOAD. |
| `TR-CRS-M1-00521-0621` | `CRS-M1-00521` | TIMING | `TIM-CRS-M1-00521` | FIND timing is catalogued for later error-interval judgement; bound M2 does not run FIND. |
| `TR-CRS-M1-00521-0622` | `CRS-M1-00521` | CLOCK | `CLK_FIND` | FIND clock is observational in the catalog only. |
| `TR-CRS-M1-00522-0615` | `CRS-M1-00522` | SCOPE | `SCOPE` | Expanded CRS recorded; bound M2 does not execute FIND/DOWNLOAD. |
| `TR-CRS-M1-00523-0616` | `CRS-M1-00523` | SCOPE | `SCOPE` | Expanded CRS recorded; bound M2 does not execute FIND/DOWNLOAD. |
| `TR-CRS-M1-00524-0617` | `CRS-M1-00524` | SCOPE | `SCOPE` | Expanded CRS recorded; bound M2 does not execute FIND/DOWNLOAD. |
| `TR-CRS-M1-00525-0620` | `CRS-M1-00525` | SCOPE | `SCOPE` | Expanded CRS recorded; bound M2 does not execute FIND/DOWNLOAD. |
| `TR-CRS-M1-00526-0623` | `CRS-M1-00526` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-MAY-USE-BATCH-FILE-FORMAT-CRS-M1-00526` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00527-0624` | `CRS-M1-00527` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-LET-BATCH-FILE-SELECT-LSPS-PER-TARGET-HW-POSITION-CRS-M1-00527` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00528-0625` | `CRS-M1-00528` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-IDENTIFY-BATCH-FILE-WITH-LUB-EXTENSION-CRS-M1-00528` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00529-0626` | `CRS-M1-00529` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-MATCH-REFERENCED-HEADER-FILE-NAME-CASE-CRS-M1-00529` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00530-0627` | `CRS-M1-00530` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-PREFIX-BATCH-FILE-NAME-WITH-MANUFACTURER-CODE-CRS-M1-00530` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00531-0628` | `CRS-M1-00531` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-BATCH-FILE-NAME-UNIQUE-PER-MANUFACTURER-CODE-CRS-M1-00531` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00532-0629` | `CRS-M1-00532` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-BATCH-FILE-PART-NUMBER-UNIQUE-AMONG-LSP-AND-BFP-CRS-M1-00532` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00533-0630` | `CRS-M1-00533` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-REFERENCE-COMPLETE-HEADER-FILE-NAME-WITHOUT-PATH-CRS-M1-00533` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00534-0631` | `CRS-M1-00534` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-USE-BATCH-FILE-ONLY-TO-AUTOMATE-MULTI-LSP-SETUP-CRS-M1-00534` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00535-0632` | `CRS-M1-00535` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-DO-NOT-TRANSFER-BATCH-FILE-TO-TARGET-HARDWARE-CRS-M1-00535` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00536-0633` | `CRS-M1-00536` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-INCLUDE-BATCH-FILE-CONTENT-DEFINED-BY-TABLE-2-3-1-1-CRS-M1-00536` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00537-0634` | `CRS-M1-00537` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-BATCH-FILE-LENGTH-IN-16-BIT-WORDS-CRS-M1-00537` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00538-0635` | `CRS-M1-00538` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-MAKE-BATCH-FILE-PN-COMPLIANT-WITH-SOFTWARE-LOAD-PN-FORMAT-CRS-M1-00538` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00539-0636` | `CRS-M1-00539` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-BATCH-FILE-PN-DISTINCT-FROM-LSP-AND-MSP-CRS-M1-00539` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00540-0637` | `CRS-M1-00540` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-SET-LAST-LOAD-LIST-BLOCK-POINTER-TO-ZERO-CRS-M1-00540` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00541-0638` | `CRS-M1-00541` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-MATCH-TARGET-HW-ID-POS-TO-TARGET-HARDWARE-CRS-M1-00541` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00542-0639` | `CRS-M1-00542` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-MATCH-HEADER-FILE-NAME-TO-LISTED-LSP-CRS-M1-00542` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00543-0640` | `CRS-M1-00543` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-MATCH-LOAD-PN-TO-LSP-FOR-TARGET-HW-ID-POS-CRS-M1-00543` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00544-0641` | `CRS-M1-00544` | INTERFACE | `IF_INTEGRITY` | CRC algorithm identity remains blocked by unbound ARINC 645; integrity interface stays not established. |
| `TR-CRS-M1-00545-0642` | `CRS-M1-00545` | INTERFACE | `IF_INTEGRITY` | CRC algorithm identity remains blocked by unbound ARINC 645; integrity interface stays not established. |
| `TR-CRS-M1-00546-0643` | `CRS-M1-00546` | FIELD-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-LENGTH` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00547-0644` | `CRS-M1-00547` | FIELD-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-FORMAT-VERSION` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00548-0645` | `CRS-M1-00548` | FIELD-CONSTRAINT | `FC-LUB-FIELD-SPARE` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00549-0646` | `CRS-M1-00549` | FIELD-CONSTRAINT | `FC-LUB-FIELD-POINTER-TO-BATCH-FILE-PN-LENGTH` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00550-0647` | `CRS-M1-00550` | FIELD-CONSTRAINT | `FC-LUB-FIELD-POINTER-TO-NUMBER-OF-TARGET-HW-ID-LOAD-LIST-BLOCKS` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00551-0648` | `CRS-M1-00551` | FIELD-CONSTRAINT | `FC-LUB-FIELD-EXPANSION-POINT-1` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00552-0649` | `CRS-M1-00552` | FIELD-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-PN-LENGTH` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00553-0650` | `CRS-M1-00553` | FIELD-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-PN` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00554-0651` | `CRS-M1-00554` | FIELD-CONSTRAINT | `FC-LUB-FIELD-COMMENT-LENGTH` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00555-0652` | `CRS-M1-00555` | FIELD-CONSTRAINT | `FC-LUB-FIELD-COMMENT` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00556-0653` | `CRS-M1-00556` | FIELD-CONSTRAINT | `FC-LUB-FIELD-EXPANSION-POINT-2` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00557-0654` | `CRS-M1-00557` | FIELD-CONSTRAINT | `FC-LUB-FIELD-NUMBER-OF-TARGET-HW-ID-LOAD-LIST-BLOCKS` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00558-0655` | `CRS-M1-00558` | FIELD-CONSTRAINT | `FC-LUB-FIELD-POINTER-TO-NEXT-TARGET-HW-ID-LOAD-LIST-BLOCK` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00559-0656` | `CRS-M1-00559` | FIELD-CONSTRAINT | `FC-LUB-FIELD-TARGET-HW-ID-POS-LENGTH` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00560-0657` | `CRS-M1-00560` | FIELD-CONSTRAINT | `FC-LUB-FIELD-TARGET-HW-ID-POS` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00561-0658` | `CRS-M1-00561` | FIELD-CONSTRAINT | `FC-LUB-FIELD-NUMBER-OF-LOADS-FOR-TARGET-HW-ID-POS` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00562-0659` | `CRS-M1-00562` | FIELD-CONSTRAINT | `FC-LUB-FIELD-HEADER-FILE-NAME-LENGTH` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00563-0660` | `CRS-M1-00563` | FIELD-CONSTRAINT | `FC-LUB-FIELD-HEADER-FILE-NAME` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00564-0661` | `CRS-M1-00564` | FIELD-CONSTRAINT | `FC-LUB-FIELD-LOAD-PN-LENGTH` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00565-0662` | `CRS-M1-00565` | FIELD-CONSTRAINT | `FC-LUB-FIELD-LOAD-PN` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00566-0663` | `CRS-M1-00566` | FIELD-CONSTRAINT | `FC-LUB-FIELD-EXPANSION-POINT-3` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00567-0664` | `CRS-M1-00567` | FIELD-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-CRC` | 665 batch-file table row recorded as a field constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00567-0665` | `CRS-M1-00567` | INTERFACE | `IF_INTEGRITY` | CRC algorithm identity remains blocked by unbound ARINC 645; integrity interface stays not established. |
| `TR-CRS-M1-00568-0666` | `CRS-M1-00568` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-DEFINE-BATCH-FILE-FORMAT-VERSION-IN-16-BITS-CRS-M1-00568` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00569-0667` | `CRS-M1-00569` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-TAKE-BATCH-FILE-FORMAT-VERSION-FROM-CLAUSE-1-4-1-CRS-M1-00569` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00570-0668` | `CRS-M1-00570` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-USE-SPARE-TO-ALIGN-FOLLOWING-POINTERS-ON-4-BYTE-BOUNDARIES-CRS-M1-00570` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00571-0669` | `CRS-M1-00571` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-POINT-TO-BATCH-FILE-PN-LENGTH-FROM-START-IN-16-BIT-WORDS-CRS-M1-00571` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00572-0670` | `CRS-M1-00572` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-POINT-TO-LOAD-LIST-BLOCK-COUNT-FROM-START-IN-16-BIT-WORDS-CRS-M1-00572` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00573-0671` | `CRS-M1-00573` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-MAY-GROW-FILE-FORMAT-AT-EXPANSION-POINTS-CRS-M1-00573` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00574-0672` | `CRS-M1-00574` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-BATCH-FILE-PN-LENGTH-CRS-M1-00574` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00575-0673` | `CRS-M1-00575` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-BATCH-FILE-PN-AS-8-BIT-ASCII-CRS-M1-00575` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00576-0674` | `CRS-M1-00576` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-BATCH-FILE-PN-EVEN-OCTET-WIDTH-CRS-M1-00576` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00577-0675` | `CRS-M1-00577` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-BATCH-FILE-PN-WITH-NUL-CRS-M1-00577` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00578-0676` | `CRS-M1-00578` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-COMMENT-LENGTH-CRS-M1-00578` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00579-0677` | `CRS-M1-00579` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-SET-COMMENT-LENGTH-ZERO-WHEN-NO-COMMENT-CRS-M1-00579` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00580-0678` | `CRS-M1-00580` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-COMMENT-AS-8-BIT-ASCII-CRS-M1-00580` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00581-0679` | `CRS-M1-00581` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-COMMENT-EVEN-OCTET-WIDTH-CRS-M1-00581` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00582-0680` | `CRS-M1-00582` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-COMMENT-WITH-NUL-CRS-M1-00582` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00583-0681` | `CRS-M1-00583` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-OMIT-COMMENT-FIELD-WHEN-COMMENT-LENGTH-ZERO-CRS-M1-00583` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00584-0682` | `CRS-M1-00584` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-COUNT-TARGET-HW-ID-LOAD-LIST-BLOCKS-IN-BATCH-FILE-CRS-M1-00584` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00585-0683` | `CRS-M1-00585` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-POINT-TO-NEXT-LOAD-LIST-BLOCK-IN-RELATIVE-16-BIT-WORDS-CRS-M1-00585` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00586-0684` | `CRS-M1-00586` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-TARGET-HW-ID-POS-LENGTH-CRS-M1-00586` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00587-0685` | `CRS-M1-00587` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-TARGET-HW-ID-POS-AS-8-BIT-ASCII-CRS-M1-00587` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00588-0686` | `CRS-M1-00588` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-TARGET-HW-ID-POS-EVEN-OCTET-WIDTH-CRS-M1-00588` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00589-0687` | `CRS-M1-00589` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-TARGET-HW-ID-POS-WITH-NUL-CRS-M1-00589` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00590-0688` | `CRS-M1-00590` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-TARGET-HW-ID-POS-CONSISTENT-WITH-LISTED-LSP-HEADERS-CRS-M1-00590` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00591-0689` | `CRS-M1-00591` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-COUNT-LOADS-IN-THE-TARGET-HW-ID-LOAD-LIST-BLOCK-CRS-M1-00591` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00592-0690` | `CRS-M1-00592` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-HEADER-FILE-NAME-LENGTH-CRS-M1-00592` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00593-0691` | `CRS-M1-00593` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-HEADER-FILE-NAME-AS-8-BIT-ASCII-CRS-M1-00593` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00594-0692` | `CRS-M1-00594` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-HEADER-FILE-NAME-EVEN-OCTET-WIDTH-CRS-M1-00594` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00595-0693` | `CRS-M1-00595` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-HEADER-FILE-NAME-WITH-NUL-CRS-M1-00595` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00596-0694` | `CRS-M1-00596` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-USE-HEADER-FILE-NAME-WITHOUT-PATH-CRS-M1-00596` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00597-0695` | `CRS-M1-00597` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-HEADER-FILE-NAME-FREE-OF-BACKSLASH-CRS-M1-00597` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00598-0696` | `CRS-M1-00598` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-INCLUDE-HEADER-FILE-NAME-EXTENSIONS-AND-DELIMITERS-CRS-M1-00598` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00599-0697` | `CRS-M1-00599` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-DEFINE-LOAD-PN-LENGTH-AS-CHARACTER-COUNT-CRS-M1-00599` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00600-0698` | `CRS-M1-00600` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-LOAD-PN-LENGTH-CRS-M1-00600` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00601-0699` | `CRS-M1-00601` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-LOAD-PN-AS-8-BIT-ASCII-CRS-M1-00601` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00602-0700` | `CRS-M1-00602` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-LOAD-PN-EVEN-OCTET-WIDTH-CRS-M1-00602` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00603-0701` | `CRS-M1-00603` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-LOAD-PN-WITH-NUL-CRS-M1-00603` | 665 batch-file predicate recorded as a data-object constraint; bound M2 does not execute batch loading. |
| `TR-CRS-M1-00604-0805` | `CRS-M1-00604` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-GIVE-664P3-PRECEDENCE-OVER-CONFLICTING-RFC-OPTIONS-CRS-M1-00604` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00605-0806` | `CRS-M1-00605` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-GENERATE-AND-CHECK-UDP-CHECKSUM-CRS-M1-00605` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00606-0807` | `CRS-M1-00606` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-IMPLEMENT-IPV4-IN-ACCORDANCE-WITH-P3-FIGURE-3-4-1-1-CRS-M1-00606` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00607-0883` | `CRS-M1-00607` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-SECURE-RELIABLE-PARTITION-DATA-EXCHANGE-CRS-M1-00607` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00608-0809` | `CRS-M1-00608` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-FILTER-AND-POLICE-FRAMES-FOR-INTEGRITY-LENGTH-BUDGET-AND-DESTINATION-CRS-M1-00608` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00609-0810` | `CRS-M1-00609` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-AFDX-NOT-APPLICABLE-PROFILE-ITEMS-AS-MUST-NOT-CRS-M1-00609` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00610-0811` | `CRS-M1-00610` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-UDP-LENGTH-TO-HEADER-PLUS-DATA-OCTETS-CRS-M1-00610` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00611-0812` | `CRS-M1-00611` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-COMPUTE-UDP-CHECKSUM-OVER-PSEUDO-HEADER-HEADER-AND-DATA-CRS-M1-00611` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00612-0884` | `CRS-M1-00612` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-IMPLEMENT-IPV4-ADDRESSING-AND-FRAGMENTATION-CRS-M1-00612` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00613-0815` | `CRS-M1-00613` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-IMPLEMENT-IPV4-FRAGMENTATION-AND-REASSEMBLY-CRS-M1-00613` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00614-0816` | `CRS-M1-00614` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SILENTLY-DISCARD-NON-IPV4-VERSION-CRS-M1-00614` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00615-0819` | `CRS-M1-00615` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-GENERATE-AND-VALIDATE-UDP-CHECKSUMS-CRS-M1-00615` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00616-0885` | `CRS-M1-00616` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-APPLY-RFC-1123-TFTP-HOST-NOTES-WITHOUT-ADOPTING-MAIL-NETASCII-OR-BROADCAST-RRQ-CRS-M1-00616` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00617-0822` | `CRS-M1-00617` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-FIVE-TFTP-PACKET-TYPES-IDENTIFIED-BY-OPCODE-CRS-M1-00617` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00618-0823` | `CRS-M1-00618` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ASSIGN-TID-ON-RRQ-OR-WRQ-WITHOUT-MAIL-MODE-CRS-M1-00618` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00619-0824` | `CRS-M1-00619` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PLACE-OPCODE-IN-TFTP-HEADER-CRS-M1-00619` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00620-0831` | `CRS-M1-00620` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TERMINATE-ON-DATA-PACKET-OF-0-TO-511-BYTES-CRS-M1-00620` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00621-0832` | `CRS-M1-00621` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SEND-ERROR-PACKET-OPCODE-5-CRS-M1-00621` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00622-0833` | `CRS-M1-00622` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ACKNOWLEDGE-OPTION-NEGOTIATION-WITH-OACK-CRS-M1-00622` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00623-0834` | `CRS-M1-00623` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TERMINATE-TRANSFER-WITH-ERROR-CODE-8-CRS-M1-00623` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00624-0835` | `CRS-M1-00624` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-APPEND-OPTIONS-TO-RRQ-OR-WRQ-CRS-M1-00624` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00625-0836` | `CRS-M1-00625` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-BLKSIZE-AS-ASCII-OCTETS-FROM-8-THROUGH-65464-CRS-M1-00625` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00626-0840` | `CRS-M1-00626` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-TIMEOUT-AS-ASCII-SECONDS-FROM-1-THROUGH-255-CRS-M1-00626` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00627-0842` | `CRS-M1-00627` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUEST-TSIZE-ZERO-ON-RRQ-AND-RETURN-SIZE-IN-OACK-CRS-M1-00627` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00628-0813` | `CRS-M1-00628` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-UDP-LENGTH-AT-LEAST-EIGHT-OCTETS-CRS-M1-00628` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00629-0817` | `CRS-M1-00629` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-VERIFY-IP-HEADER-CHECKSUM-AND-SILENTLY-DISCARD-BAD-CRS-M1-00629` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00630-0818` | `CRS-M1-00630` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SUPPORT-IPV4-REASSEMBLY-CRS-M1-00630` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00631-0820` | `CRS-M1-00631` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SILENTLY-DISCARD-UDP-DATAGRAM-WITH-INVALID-CHECKSUM-CRS-M1-00631` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00632-0825` | `CRS-M1-00632` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-RRQ-WRQ-AS-OPCODE-FILENAME-AND-MODE-CRS-M1-00632` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00633-0826` | `CRS-M1-00633` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TERMINATE-TFTP-FILENAME-WITH-NUL-CRS-M1-00633` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00634-0827` | `CRS-M1-00634` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-DATA-PACKET-WITH-BLOCK-NUMBER-AND-DATA-CRS-M1-00634` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00635-0828` | `CRS-M1-00635` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-LIMIT-TFTP-DATA-FIELD-TO-ZERO-THROUGH-512-BYTES-CRS-M1-00635` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00636-0829` | `CRS-M1-00636` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-ACK-PACKET-WITH-OPCODE-4-AND-BLOCK-NUMBER-CRS-M1-00636` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00637-0830` | `CRS-M1-00637` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-ERROR-PACKET-AS-OPCODE-ERROR-CODE-AND-MESSAGE-CRS-M1-00637` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00638-0837` | `CRS-M1-00638` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-BLKSIZE-VALUE-IN-ASCII-CRS-M1-00638` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00639-0838` | `CRS-M1-00639` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-NEGOTIATE-BLKSIZE-LESS-OR-EQUAL-TO-CLIENT-VALUE-CRS-M1-00639` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00640-0839` | `CRS-M1-00640` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-OACK-BLKSIZE-OR-TERMINATE-WITH-ERROR-8-CRS-M1-00640` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00641-0841` | `CRS-M1-00641` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ECHO-CLIENT-TIMEOUT-VALUE-IN-OACK-CRS-M1-00641` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00642-0843` | `CRS-M1-00642` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SPECIFY-TSIZE-ON-WRQ-AND-ECHO-IN-OACK-CRS-M1-00642` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00643-0844` | `CRS-M1-00643` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MAY-ABORT-RRQ-WITH-ERROR-CODE-3-CRS-M1-00643` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00644-0845` | `CRS-M1-00644` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MAY-ABORT-WRQ-WITH-ERROR-CODE-3-CRS-M1-00644` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00645-0846` | `CRS-M1-00645` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TERMINATE-ON-DATA-SHORTER-THAN-NEGOTIATED-BLKSIZE-CRS-M1-00645` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00646-0847` | `CRS-M1-00646` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SEND-ZERO-LENGTH-FINAL-DATA-WHEN-FILE-IS-INTEGRAL-MULTIPLE-OF-BLKSIZE-CRS-M1-00646` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00647-0848` | `CRS-M1-00647` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-IGNORE-UNACKNOWLEDGED-OPTION-AND-KEEP-DEFAULT-PARAMETERS-CRS-M1-00647` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00648-0849` | `CRS-M1-00648` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-VERSION-AS-4-BITS-CRS-M1-00648` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00649-0850` | `CRS-M1-00649` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-IHL-AS-4-BITS-CRS-M1-00649` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00650-0851` | `CRS-M1-00650` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-TOS-AS-8-BITS-CRS-M1-00650` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00651-0852` | `CRS-M1-00651` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-TOTAL-LENGTH-AS-16-BITS-CRS-M1-00651` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00652-0853` | `CRS-M1-00652` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-IDENTIFICATION-AS-16-BITS-CRS-M1-00652` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00653-0854` | `CRS-M1-00653` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-FLAGS-AS-3-BITS-CRS-M1-00653` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00654-0855` | `CRS-M1-00654` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-FRAGMENT-OFFSET-AS-13-BITS-CRS-M1-00654` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00655-0856` | `CRS-M1-00655` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-TTL-AS-8-BITS-CRS-M1-00655` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00656-0857` | `CRS-M1-00656` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-PROTOCOL-AS-8-BITS-CRS-M1-00656` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00657-0858` | `CRS-M1-00657` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-HEADER-CHECKSUM-AS-16-BITS-CRS-M1-00657` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00658-0859` | `CRS-M1-00658` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-SOURCE-ADDRESS-AS-32-BITS-CRS-M1-00658` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00659-0860` | `CRS-M1-00659` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-DESTINATION-ADDRESS-AS-32-BITS-CRS-M1-00659` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00660-0861` | `CRS-M1-00660` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-DO-NOT-SUPPORT-TFTP-MAIL-TRANSFER-MODE-CRS-M1-00660` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00661-0862` | `CRS-M1-00661` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-COUNT-UDP-LENGTH-INCLUDING-EIGHT-OCTET-HEADER-CRS-M1-00661` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00662-0863` | `CRS-M1-00662` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-NEVER-RESEND-CURRENT-DATA-ON-DUPLICATE-ACK-CRS-M1-00662` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00663-0864` | `CRS-M1-00663` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-ADAPTIVE-TFTP-RETRANSMISSION-TIMEOUT-CRS-M1-00663` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00664-0865` | `CRS-M1-00664` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-CONFIGURABLE-TFTP-PATHNAME-ACCESS-CONTROL-CRS-M1-00664` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00665-0866` | `CRS-M1-00665` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SILENTLY-IGNORE-BROADCAST-TFTP-REQUEST-CRS-M1-00665` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00666-0867` | `CRS-M1-00666` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ALLOW-ONLY-ONE-SOURCE-END-SYSTEM-PER-VL-CRS-M1-00666` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00667-0868` | `CRS-M1-00667` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-VL-AS-UNIDIRECTIONAL-ONE-TO-MANY-CONNECTION-CRS-M1-00667` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00668-0869` | `CRS-M1-00668` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-BAG-AS-MINIMUM-INTERVAL-BETWEEN-CONSECUTIVE-VL-FRAMES-CRS-M1-00668` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00669-0870` | `CRS-M1-00669` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-BOUND-VL-FRAME-ARRIVAL-BY-MAXIMUM-ADMISSIBLE-JITTER-CRS-M1-00669` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00670-0871` | `CRS-M1-00670` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-CHARACTERISE-VL-BANDWIDTH-BY-BAG-AND-LMAX-CRS-M1-00670` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00671-0872` | `CRS-M1-00671` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ACCOMMODATE-VL-FRAMES-UP-TO-1518-BYTES-CRS-M1-00671` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00672-0873` | `CRS-M1-00672` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-HANDLE-BAG-VALUES-FROM-1-MS-TO-128-MS-CRS-M1-00672` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00673-0874` | `CRS-M1-00673` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RESTRICT-BAG-TO-POWERS-OF-TWO-MILLISECONDS-CRS-M1-00673` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00674-0899` | `CRS-M1-00674` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-VL-JITTER-AT-OR-BELOW-500-MICROSECONDS-CRS-M1-00674` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00675-0876` | `CRS-M1-00675` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-IDENTIFY-VL-ONLY-BY-MAC-DESTINATION-ADDRESS-CRS-M1-00675` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00676-0877` | `CRS-M1-00676` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-IHL-IN-32-BIT-WORDS-CRS-M1-00676` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00677-0878` | `CRS-M1-00677` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-IHL-AT-LEAST-5-CRS-M1-00677` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00678-0879` | `CRS-M1-00678` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-IPV4-TOTAL-LENGTH-IN-OCTETS-INCLUDING-HEADER-AND-DATA-CRS-M1-00678` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00679-0880` | `CRS-M1-00679` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-FRAGMENT-OFFSET-IN-8-OCTET-UNITS-CRS-M1-00679` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00680-0881` | `CRS-M1-00680` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ALLOW-IPV4-OPTIONS-TO-BE-PRESENT-OR-ABSENT-CRS-M1-00680` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00681-0882` | `CRS-M1-00681` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PAD-IPV4-HEADER-TO-32-BIT-BOUNDARY-CRS-M1-00681` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00682-0886` | `CRS-M1-00682` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-TX-TECHNOLOGICAL-LATENCY-BELOW-150US-PLUS-FRAME-DELAY-CRS-M1-00682` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00682-0937` | `CRS-M1-00682` | TIMING | `TIM-CRS-M1-00682` | AFDX timing is catalogued as a conditional network constraint; bound M2 does not execute AFDX. |
| `TR-CRS-M1-00682-0938` | `CRS-M1-00682` | CLOCK | `CLK_AFDX_ES` | AFDX End-System clock is observational in the catalog only. |
| `TR-CRS-M1-00683-0887` | `CRS-M1-00683` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-RX-TECHNOLOGICAL-LATENCY-BELOW-150-MICROSECONDS-CRS-M1-00683` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00683-0939` | `CRS-M1-00683` | TIMING | `TIM-CRS-M1-00683` | AFDX timing is catalogued as a conditional network constraint; bound M2 does not execute AFDX. |
| `TR-CRS-M1-00683-0940` | `CRS-M1-00683` | CLOCK | `CLK_AFDX_ES` | AFDX End-System clock is observational in the catalog only. |
| `TR-CRS-M1-00684-0888` | `CRS-M1-00684` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-BOUND-MAX-JITTER-BY-40US-PLUS-VL-LOAD-TERM-CRS-M1-00684` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00684-0941` | `CRS-M1-00684` | TIMING | `TIM-CRS-M1-00684` | AFDX timing is catalogued as a conditional network constraint; bound M2 does not execute AFDX. |
| `TR-CRS-M1-00684-0942` | `CRS-M1-00684` | CLOCK | `CLK_AFDX_ES` | AFDX End-System clock is observational in the catalog only. |
| `TR-CRS-M1-00685-0889` | `CRS-M1-00685` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-BOUND-MAX-JITTER-BY-500-MICROSECONDS-EQUATION-CRS-M1-00685` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00685-0943` | `CRS-M1-00685` | TIMING | `TIM-CRS-M1-00685` | AFDX timing is catalogued as a conditional network constraint; bound M2 does not execute AFDX. |
| `TR-CRS-M1-00685-0944` | `CRS-M1-00685` | CLOCK | `CLK_AFDX_ES` | AFDX End-System clock is observational in the catalog only. |
| `TR-CRS-M1-00686-0890` | `CRS-M1-00686` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-MAC-SOURCE-AS-INDIVIDUAL-AND-LOCALLY-ADMINISTERED-CRS-M1-00686` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00687-0891` | `CRS-M1-00687` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-SOURCE-CONSTANT-FIELD-TO-000000100000000000000000-CRS-M1-00687` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00688-0892` | `CRS-M1-00688` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-SOURCE-INDIVIDUAL-ADDRESS-BIT-TO-ZERO-CRS-M1-00688` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00689-0893` | `CRS-M1-00689` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-SOURCE-LOCALLY-ADMINISTERED-BIT-TO-ONE-CRS-M1-00689` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00690-0894` | `CRS-M1-00690` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-MAC-SOURCE-USER-DEFINED-ID-AS-16-BITS-CRS-M1-00690` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00691-0895` | `CRS-M1-00691` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-USER-DEFINED-ID-FOR-UNIQUE-MEANINGFUL-HOST-IDENTITY-CRS-M1-00691` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00692-0896` | `CRS-M1-00692` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-INTERFACE-ID-TO-IDENTIFY-REDUNDANT-AFDX-NETWORK-CRS-M1-00692` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00693-0897` | `CRS-M1-00693` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-INTERFACE-ID-001-AS-NETWORK-A-CRS-M1-00693` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00694-0898` | `CRS-M1-00694` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-INTERFACE-ID-010-AS-NETWORK-B-CRS-M1-00694` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00695-0900` | `CRS-M1-00695` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-ADN-ADDRESS-DETERMINATION-GUIDANCE-CRS-M1-00695` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution or activate AFDX. |
| `TR-CRS-M1-00696-0901` | `CRS-M1-00696` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KNOW-DESTINATION-ADDRESSES-AT-CONFIGURATION-TIME-CRS-M1-00696` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution or activate AFDX. |
| `TR-CRS-M1-00697-0902` | `CRS-M1-00697` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-DEFINE-ADN-ADDRESSING-PLAN-AND-RULES-CRS-M1-00697` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution or activate AFDX. |
| `TR-CRS-M1-00698-0903` | `CRS-M1-00698` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-IANA-WELL-KNOWN-UDP-PORTS-FOR-STANDARD-SERVICES-INCLUDING-TFTP-CRS-M1-00698` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution or activate AFDX. |
| `TR-CRS-M1-00699-0904` | `CRS-M1-00699` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ACCESS-PRIVATE-AERO-APPS-VIA-INTEGRATOR-OR-664P4-UDP-PORTS-CRS-M1-00699` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution or activate AFDX. |
| `TR-CRS-M1-00700-0905` | `CRS-M1-00700` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-DO-NOT-REASSIGN-WELL-KNOWN-COTS-PORTS-0-1023-CRS-M1-00700` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution or activate AFDX. |
| `TR-CRS-M1-00701-0906` | `CRS-M1-00701` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-DO-NOT-ROUTE-PRIVATE-ADDRESSES-OUTSIDE-THE-NETWORK-CRS-M1-00701` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution or activate AFDX. |
| `TR-CRS-M1-00702-0907` | `CRS-M1-00702` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-PROFILED-AERO-NETWORK-AS-IETF-PRIVATE-APPLICATION-CRS-M1-00702` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution or activate AFDX. |
| `TR-CRS-M1-00703-0908` | `CRS-M1-00703` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-PRIVATE-NETWORK-ID-FOR-PROFILED-NETWORKS-CRS-M1-00703` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution or activate AFDX. |
| `TR-CRS-M1-00704-0909` | `CRS-M1-00704` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ASSIGN-MAC-UNICAST-ADDRESSES-AT-CONFIGURATION-TIME-CRS-M1-00704` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution or activate AFDX. |
| `TR-CRS-M1-00705-0910` | `CRS-M1-00705` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-MAC-ADDRESSES-UNIQUE-UNDER-INTEGRATOR-SCHEME-CRS-M1-00705` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution or activate AFDX. |
| `TR-CRS-M1-00706-0911` | `CRS-M1-00706` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-UL-BIT-WHEN-INTEGRATOR-ASSIGNS-ADDRESSES-CRS-M1-00706` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution or activate AFDX. |
| `TR-CRS-M1-00707-0912` | `CRS-M1-00707` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-ALL-NETWORK-ADDRESSES-UNIQUE-CRS-M1-00707` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution or activate AFDX. |
| `TR-CRS-M1-00708-0913` | `CRS-M1-00708` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RESERVE-UDP-TCP-PORT-59-FOR-615A-DATA-LOADER-TFTP-CRS-M1-00708` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution or activate AFDX. |
| `TR-CRS-M1-00709-0914` | `CRS-M1-00709` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ASSIGN-UDP-PORT-24922-TO-FIND-PROTOCOL-CLIENT-CRS-M1-00709` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution or activate AFDX. |
| `TR-CRS-M1-00710-0915` | `CRS-M1-00710` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ALLOCATE-TABLE-2-1-ADDRESSES-FROM-RFC1918-PRIVATE-RANGES-CRS-M1-00710` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution or activate AFDX. |
| `TR-CRS-M1-00711-0916` | `CRS-M1-00711` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-TX-TECHNOLOGICAL-LATENCY-BETWEEN-PARTITION-DATA-AND-PHYSICAL-MEDIA-CRS-M1-00711` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00712-0917` | `CRS-M1-00712` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-START-TX-TECHNOLOGICAL-LATENCY-WHEN-LAST-PARTITION-BIT-IS-AVAILABLE-CRS-M1-00712` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00713-0918` | `CRS-M1-00713` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-END-TX-TECHNOLOGICAL-LATENCY-WHEN-LAST-FRAME-BIT-IS-ON-MEDIA-CRS-M1-00713` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00714-0919` | `CRS-M1-00714` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-TX-TECHNOLOGICAL-LATENCY-WITH-EMPTY-BUFFERS-NO-CONTENTION-AND-NO-IP-FRAGMENTATION-CRS-M1-00714` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00715-0920` | `CRS-M1-00715` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-DISTINGUISH-TECHNOLOGICAL-LATENCY-FROM-CONFIGURATION-LOAD-LATENCY-CRS-M1-00715` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00716-0921` | `CRS-M1-00716` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-DEFINE-TECHNOLOGICAL-LATENCY-AS-ACCEPT-PROCESS-AND-BEGIN-TX-WITH-NO-OTHER-TASK-CRS-M1-00716` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00717-0922` | `CRS-M1-00717` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ADD-FRAME-DELAY-FOR-PHYSICAL-LAYER-DELIVERY-CRS-M1-00717` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00718-0923` | `CRS-M1-00718` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-START-RX-TECHNOLOGICAL-LATENCY-WHEN-LAST-FRAME-BIT-IS-RECEIVED-CRS-M1-00718` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00719-0924` | `CRS-M1-00719` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-END-RX-TECHNOLOGICAL-LATENCY-WHEN-LAST-DATA-BIT-IS-AVAILABLE-TO-PARTITION-CRS-M1-00719` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00720-0925` | `CRS-M1-00720` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-RX-TECHNOLOGICAL-LATENCY-WITH-EMPTY-BUFFERS-AND-NO-CONTENTION-CRS-M1-00720` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00721-0926` | `CRS-M1-00721` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SATISFY-BOTH-MAX-JITTER-EQUATIONS-SIMULTANEOUSLY-CRS-M1-00721` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00722-0927` | `CRS-M1-00722` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-MAX-JITTER-AS-MICROSECONDS-NBW-AS-BITS-PER-SECOND-AND-LMAX-AS-OCTETS-CRS-M1-00722` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00723-0928` | `CRS-M1-00723` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-COMPOSE-MAC-SOURCE-AS-24-PLUS-16-PLUS-3-PLUS-5-BIT-FIELDS-CRS-M1-00723` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00724-0929` | `CRS-M1-00724` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-SOURCE-CONSTANT-TAIL-TO-00000-CRS-M1-00724` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00725-0930` | `CRS-M1-00725` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-MAC-SOURCE-CONSTRUCTION-ALGORITHM-AS-NOT-UNIQUELY-RECOMMENDED-CRS-M1-00725` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00726-0931` | `CRS-M1-00726` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-000-AS-NOT-USED-CRS-M1-00726` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00727-0932` | `CRS-M1-00727` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-011-AS-NOT-USED-CRS-M1-00727` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00728-0933` | `CRS-M1-00728` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-100-AS-NOT-USED-CRS-M1-00728` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00729-0934` | `CRS-M1-00729` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-101-AS-NOT-USED-CRS-M1-00729` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00730-0935` | `CRS-M1-00730` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-110-AS-SOURCE-NOR-USED-CRS-M1-00730` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00731-0936` | `CRS-M1-00731` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-111-AS-NOT-USED-CRS-M1-00731` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00732-0945` | `CRS-M1-00732` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-P3-RFC-OPTION-RESTRICTION-PHILOSOPHY-CRS-M1-00732` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00733-0946` | `CRS-M1-00733` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-P3-CONTENTS-LIMITED-TO-RFC-DELTAS-CRS-M1-00733` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00734-0947` | `CRS-M1-00734` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-COMPOSE-AFDX-SWITCH-FROM-FIVE-FUNCTIONAL-BLOCKS-CRS-M1-00734` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00735-0948` | `CRS-M1-00735` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-CONTROL-AFDX-SWITCH-FUNCTIONS-WITH-STATIC-CONFIGURATION-TABLES-CRS-M1-00735` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00736-0949` | `CRS-M1-00736` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-SWITCH-END-SYSTEM-TO-COMPLY-WITH-SECTION-3-EXCEPT-REDUNDANCY-CRS-M1-00736` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00737-0950` | `CRS-M1-00737` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-SWITCH-END-SYSTEM-UNICAST-MAC-AS-SOURCE-ADDRESS-CRS-M1-00737` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00738-0951` | `CRS-M1-00738` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-615A-SESSION-ACROSS-OPS-TO-DL-TRANSITION-CRS-M1-00738` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00739-0952` | `CRS-M1-00739` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-615A-AND-665-TO-UPLOAD-SWITCH-SOFTWARE-AND-CONFIGURATION-CRS-M1-00739` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00740-0953` | `CRS-M1-00740` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-AFDX-SWITCH-PHYSICAL-LAYER-TO-COMPLY-WITH-664P2-CRS-M1-00740` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00741-0954` | `CRS-M1-00741` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-AS-NOT-USED-ON-AFDX-CRS-M1-00741` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00742-0955` | `CRS-M1-00742` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-CHECKSUM-GENERATE-AND-CHECK-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00742` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00743-0956` | `CRS-M1-00743` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-AFDX-END-SYSTEM-INTERNET-LAYER-TO-IMPLEMENT-IP-CRS-M1-00743` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00744-0957` | `CRS-M1-00744` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-AFDX-END-SYSTEM-INTERNET-LAYER-TO-IMPLEMENT-ICMP-CRS-M1-00744` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00745-0958` | `CRS-M1-00745` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SILENTLY-DISCARD-NON-IPV4-DATAGRAMS-CRS-M1-00745` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00746-0959` | `CRS-M1-00746` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-AFDX-UDP-CHECKSUM-UNUSED-COMMENT-CRS-M1-00746` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00747-0960` | `CRS-M1-00747` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-SILENT-BAD-UDP-CHECKSUM-DISCARD-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00747` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00748-0961` | `CRS-M1-00748` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PASS-ICMP-MESSAGES-TO-APPLICATION-LIMITED-TO-ECHO-REQUEST-CRS-M1-00748` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00749-0962` | `CRS-M1-00749` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-PORT-UNREACHABLE-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00749` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00750-0963` | `CRS-M1-00750` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-FORBID-REMOTE-MULTIHOMING-AT-APPLICATION-LAYER-ON-AFDX-CRS-M1-00750` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00751-0964` | `CRS-M1-00751` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-LOCAL-MULTIHOMING-ON-AFDX-CRS-M1-00751` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00752-0965` | `CRS-M1-00752` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-LOG-DISCARDED-DATAGRAMS-ON-AFDX-CRS-M1-00752` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00753-0966` | `CRS-M1-00753` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-DISCARDED-DATAGRAMS-IN-COUNTER-ON-AFDX-CRS-M1-00753` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00754-0967` | `CRS-M1-00754` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENTER-OPS-AFTER-COMPATIBLE-INIT-WHEN-SHOP-INACTIVE-CRS-M1-00754` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00755-0968` | `CRS-M1-00755` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-OPS-MODE-615A-INFORMATION-AND-FIND-CRS-M1-00755` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00756-0969` | `CRS-M1-00756` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENTER-DL-FROM-INIT-ONLY-WHEN-GROUND-AND-COMPATIBILITY-FAIL-OR-EMPTY-CRS-M1-00756` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00757-0970` | `CRS-M1-00757` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENTER-DL-FROM-OPS-ONLY-WHEN-GROUND-UPLOAD-INIT-AND-HEADER-ACCEPTED-CRS-M1-00757` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00758-0971` | `CRS-M1-00758` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-DL-MODE-615A-INFORMATION-UPLOAD-AND-FIND-CRS-M1-00758` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00759-0972` | `CRS-M1-00759` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-SEND-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00759` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00760-0973` | `CRS-M1-00760` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-DOWN-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00760` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00761-0974` | `CRS-M1-00761` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-GATEWAY-FORWARDING-SPEC-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00761` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00762-0975` | `CRS-M1-00762` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-EMBEDDED-GATEWAY-SWITCH-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00762` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00763-0976` | `CRS-M1-00763` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-NON-GATEWAY-DEFAULT-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00763` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00764-0977` | `CRS-M1-00764` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-AFDX-GATEWAY-AUTOCONFIGURATION-ROW-UNMARKED-CRS-M1-00764` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00765-0978` | `CRS-M1-00765` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PERFORM-OPS-FILTERING-POLICING-SWITCHING-FROM-OPS-CONFIG-CRS-M1-00765` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00766-0979` | `CRS-M1-00766` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-OPS-FAULT-HEALTHY-INDICATOR-TO-HEALTHY-CRS-M1-00766` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00767-0980` | `CRS-M1-00767` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-DL-UPLOAD-AS-PREFERABLY-EXCLUSIVE-CRS-M1-00767` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00768-0981` | `CRS-M1-00768` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-DEDICATE-SWITCH-TO-UPLOAD-DURING-DL-UPLOAD-CRS-M1-00768` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00769-0982` | `CRS-M1-00769` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-DEFAULT-RECEPTION-VL-FOR-DATALOADING-CRS-M1-00769` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00770-0983` | `CRS-M1-00770` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-TWELVE-PIN-POSITION-IDENTIFICATION-AS-EXAMPLE-CRS-M1-00770` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00771-0984` | `CRS-M1-00771` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-STATED-TWELVE-PIN-DEFINITIONS-IF-TWELVE-PINS-CHOSEN-CRS-M1-00771` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00772-0985` | `CRS-M1-00772` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-DEFAULT-CONFIGURATION-TABLE-RESIDENT-CRS-M1-00772` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00773-0986` | `CRS-M1-00773` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-DEFAULT-PHYSICAL-PORT-SPEED-100MBPS-WITHOUT-AUTONEG-CRS-M1-00773` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00774-0987` | `CRS-M1-00774` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-DEFAULT-RECEPTION-VL-FIELDS-IN-NONVOLATILE-MEMORY-CRS-M1-00774` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00775-0988` | `CRS-M1-00775` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-DEFAULT-TRANSMISSION-VL-FIELDS-IN-NONVOLATILE-MEMORY-CRS-M1-00775` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00776-0989` | `CRS-M1-00776` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-DEFAULT-TRANSMISSION-VL-FOR-DATALOADING-ACKNOWLEDGE-CRS-M1-00776` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00777-0990` | `CRS-M1-00777` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-OPS-CONFIGURATION-FILE-615A-665-FIELD-LOADABLE-CRS-M1-00777` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00778-0991` | `CRS-M1-00778` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-FILTERING-POLICING-FORWARDING-TABLE-PARAMETER-SET-CRS-M1-00778` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00779-0992` | `CRS-M1-00779` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-LISTED-PARAMETERS-TO-CONFIGURE-FILTER-POLICE-FORWARD-CRS-M1-00779` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00780-0993` | `CRS-M1-00780` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PERFORM-DL-END-SYSTEM-FROM-DEFAULT-CONFIGURATION-TABLE-CRS-M1-00780` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00781-0994` | `CRS-M1-00781` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-DL-FAULT-HEALTHY-INDICATOR-TO-HEALTHY-CRS-M1-00781` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00782-0995` | `CRS-M1-00782` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RETURN-TO-INIT-AT-END-OF-DL-MODE-CRS-M1-00782` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00783-0996` | `CRS-M1-00783` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-DL-MODE-END-AS-615A-DATA-LOADING-FUNCTION-END-CRS-M1-00783` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00784-0997` | `CRS-M1-00784` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-LIMIT-SWITCH-FIELD-LOADABLE-SOFTWARE-TO-OPS-CONFIG-AND-OPS-SOFTWARE-CRS-M1-00784` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00785-0998` | `CRS-M1-00785` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-FIELD-LOADABLE-FILES-IDENTICAL-ACROSS-AIRCRAFT-SWITCHES-CRS-M1-00785` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00786-0999` | `CRS-M1-00786` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MAKE-SWITCH-CONFIGURATION-ACCESSIBLE-VIA-615A-INFORMATION-CRS-M1-00786` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00787-1000` | `CRS-M1-00787` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-LEARN-DATALOADER-IP-FROM-SOURCE-ADDRESS-CRS-M1-00787` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00788-1001` | `CRS-M1-00788` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-PIN-PROGRAMMING-FOR-POSITION-AND-DEFAULT-MAC-IP-CRS-M1-00788` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00789-1002` | `CRS-M1-00789` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-READ-PROGRAM-PINS-IN-INIT-ONLY-WHEN-GROUND-BEFORE-SAFETY-TEST-CRS-M1-00789` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00790-1003` | `CRS-M1-00790` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-DO-NOT-READ-PROGRAM-PINS-WHEN-GROUND-CONDITION-FALSE-CRS-M1-00790` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00791-1004` | `CRS-M1-00791` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-LAST-MEMORIZED-PIN-VALUES-WHEN-NOT-GROUND-CRS-M1-00791` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00792-1005` | `CRS-M1-00792` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-CHECK-TWELVE-PROGRAM-PINS-WITH-PARITY-BIT-CRS-M1-00792` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00793-1006` | `CRS-M1-00793` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MEMORIZE-PROGRAM-PINS-IN-NVM-AFTER-PARITY-PASS-CRS-M1-00793` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00794-1007` | `CRS-M1-00794` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ACQUIRE-SWITCH-POSITION-WITH-TWELVE-PINS-P1-P12-CRS-M1-00794` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00795-1008` | `CRS-M1-00795` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-CODE-PIN-GROUND-AS-ONE-CRS-M1-00795` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00796-1009` | `CRS-M1-00796` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-CODE-PIN-OPEN-AS-ZERO-CRS-M1-00796` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00797-1010` | `CRS-M1-00797` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PROCESS-AT-LEAST-4096-VLS-IN-FILTER-POLICE-FORWARD-CRS-M1-00797` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00798-1011` | `CRS-M1-00798` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-INPUT-PHYSICAL-PORT-CRS-M1-00798` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00799-1012` | `CRS-M1-00799` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-OUTPUT-PHYSICAL-PORTS-CRS-M1-00799` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00800-1013` | `CRS-M1-00800` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-MAC-DESTINATION-CRS-M1-00800` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00801-1014` | `CRS-M1-00801` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-BAG-CRS-M1-00801` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00802-1015` | `CRS-M1-00802` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-MAX-JITTER-CRS-M1-00802` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00803-1016` | `CRS-M1-00803` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-ACCOUNT-CRS-M1-00803` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00804-1017` | `CRS-M1-00804` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-SMAX-CRS-M1-00804` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00805-1018` | `CRS-M1-00805` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-SMIN-CRS-M1-00805` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00806-1019` | `CRS-M1-00806` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-PRIORITIZATION-CRS-M1-00806` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00807-1020` | `CRS-M1-00807` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-MAX-DELAY-CRS-M1-00807` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00808-1021` | `CRS-M1-00808` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-STATE-CRS-M1-00808` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00809-1022` | `CRS-M1-00809` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-SPEED-CRS-M1-00809` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00810-1023` | `CRS-M1-00810` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-LOW-PRIORITY-BUFFER-CRS-M1-00810` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00811-1024` | `CRS-M1-00811` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-HIGH-PRIORITY-BUFFER-CRS-M1-00811` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00812-1025` | `CRS-M1-00812` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-VL-IDENTIFIER-CRS-M1-00812` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00813-1026` | `CRS-M1-00813` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-SMAX-CRS-M1-00813` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00814-1027` | `CRS-M1-00814` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-BAG-CRS-M1-00814` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00815-1028` | `CRS-M1-00815` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-VL-IDENTIFIER-CRS-M1-00815` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00816-1029` | `CRS-M1-00816` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-BAG-CRS-M1-00816` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00817-1030` | `CRS-M1-00817` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-SMAX-CRS-M1-00817` | Supporting-source predicate recorded as a data-object constraint; bound M2 does not widen UPLOAD/INFORMATION execution. |
| `TR-CRS-M1-00818-1031` | `CRS-M1-00818` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00819-1032` | `CRS-M1-00819` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00820-1033` | `CRS-M1-00820` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00821-1034` | `CRS-M1-00821` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00822-1035` | `CRS-M1-00822` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00823-1036` | `CRS-M1-00823` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00824-1037` | `CRS-M1-00824` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00825-1038` | `CRS-M1-00825` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00826-1039` | `CRS-M1-00826` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00827-1040` | `CRS-M1-00827` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00828-1041` | `CRS-M1-00828` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00829-1042` | `CRS-M1-00829` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00830-1043` | `CRS-M1-00830` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00831-1044` | `CRS-M1-00831` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00832-1045` | `CRS-M1-00832` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00833-1046` | `CRS-M1-00833` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00834-1047` | `CRS-M1-00834` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00835-1048` | `CRS-M1-00835` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00836-1049` | `CRS-M1-00836` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00837-1050` | `CRS-M1-00837` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00838-1051` | `CRS-M1-00838` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00839-1052` | `CRS-M1-00839` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00840-1053` | `CRS-M1-00840` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00841-1054` | `CRS-M1-00841` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00842-1055` | `CRS-M1-00842` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00843-1056` | `CRS-M1-00843` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00844-1057` | `CRS-M1-00844` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00845-1058` | `CRS-M1-00845` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00846-1059` | `CRS-M1-00846` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00847-1060` | `CRS-M1-00847` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00848-1061` | `CRS-M1-00848` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00849-1062` | `CRS-M1-00849` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00850-1063` | `CRS-M1-00850` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00851-1064` | `CRS-M1-00851` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00852-1065` | `CRS-M1-00852` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00853-1066` | `CRS-M1-00853` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00854-1067` | `CRS-M1-00854` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00855-1068` | `CRS-M1-00855` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |
| `TR-CRS-M1-00856-1069` | `CRS-M1-00856` | SCOPE | `SCOPE` | 645 semantic leaf is recorded; bound M2 does not execute CRC, check-value or naming algorithms. |

## Infrastructure premises

- `NET-PREMISE-IPV4-UDP` `NOT-ESTABLISHED` — The underlying IPv4/UDP service must satisfy applicable IETF host requirements without P3-specific deviations. Retained as an infrastructure prerequisite; neither implementation compliance nor a complete RFC requirements inventory is claimed. M2 must plan its substantiation before any execution configuration is approved.
- `PREM-RFC-1123` `NOT-ESTABLISHED` — Only host requirements actually triggered by the IPv4/UDP path. RFC 1123 does not replace RFC 1122.

## Actions

| ID | Status | Owner | Gate | Note |
|---|---|---|---|---|
| `A-1` | `EXECUTED-SUCCESSOR-M1-DELTA-PENDING-RG1` | INCREMENTAL-RG1 | PROFILE-MODEL-REFINEMENT-GATE | CR-2026-011 executed the successor identities (6.4.4 LUR, 6.4.5 LUS, LUR write endpoints DL WRQ / TH ACK / DL DATA). Independent RG1 still required. This is a bounded M2 baseline, not a development-ready CRS. |
| `A-2` | `CANDIDATE-PARTIAL` | M2-RG1 | PROFILE-MODEL-REFINEMENT-GATE | RFC-2347 option transfer and RFC-2348 block-size are candidate edges; 1785/2349 remain without an active 615A unit. |
| `A-3` | `CANDIDATE-IN-MODEL` | M2-RG2 | PROFILE-MODEL-REFINEMENT-GATE | Attachment 4 equation restored with retry terms; clocks enable timeout transitions. |
| `A-4` | `DEFERRED` | FUTURE-TAXONOMY-CR | SCOPE-EXPANSION-GATE | requirementKind taxonomy not executed. |
| `F-1` | `DEFERRED` | PRODUCT-SCOPE | SCOPE-EXPANSION-GATE | FIND CRS candidates exist under CR-2026-012; bound M2 still does not model FIND. MODEL-REFINEMENT-PENDING. |
| `F-2` | `DEFERRED` | PRODUCT-SCOPE | SCOPE-EXPANSION-GATE | AFDX CRS candidates exist as conditional deployment; bound M2 remains unselected. MODEL-REFINEMENT-PENDING. |
| `F-3` | `RETAINED-EXCLUSION` | M2-RG0 | SCOPE-EXPANSION-GATE | 665 media-set exclusion retained. |
| `F-4` | `INCOMPLETE-IDENTITY-ONLY` | M2-RG1 | PROFILE-MODEL-REFINEMENT-GATE | P2 identity only; no clause-level model target. |
| `F-5` | `DEFERRED` | EDITORIAL | SCOPE-EXPANSION-GATE | Label harmonization not performed. |
| `NET-ISSUE-EDITION` | `ACCEPTED-CURRENT-EDITION-P3-1-AFDX-DEFERRED` | INDEPENDENT-RG0 | PROFILE-MODEL-REFINEMENT-GATE | Owner accepted 664P3-1 as this M2 input edition; 664P7 remains recorded and AFDX stays unselected. |
| `RFC1122/IPv4/UDP` | `PREMISE-PLANNED` | M6-CONFIGURATION | PROJECT-CONFIGURATION-GATE | IPv4/UDP substantiation planned for Configuration. |
| `RFC1123` | `PREMISE-LIMITED` | M6-CONFIGURATION | PROJECT-CONFIGURATION-GATE | RFC 1123 does not replace RFC 1122. |
| `ARINC645` | `BLOCKED` | SOURCE-ACQUISITION | SOURCE-TECHNICAL-DIRECTION-GATE | Integrity capabilities remain NOT-ESTABLISHED. |
| `P7/AID/address` | `DEFERRED-UNSELECTED-DEPLOYMENT` | PRODUCT-SCOPE | SCOPE-EXPANSION-GATE | Unselected AFDX addressing remains deferred. |
| `README-P2-DISPLAY` | `CLOSED-IN-THIS-PR` | M2-AUTHOR | PROFILE-MODEL-REFINEMENT-GATE | displayGroup rendering remains. |
| `M1-LEDGER` | `RECORDED-IN-INPUT-ACCEPTANCE` | M2-AUTHOR | PROFILE-MODEL-REFINEMENT-GATE | M1 merge facts remain in inputAcceptance. |
| `M1-FILE-IDENTITY-6-4-4` | `CLOSED-BY-SUCCESSOR-M1-DELTA` | INCREMENTAL-RG1 | PROFILE-MODEL-REFINEMENT-GATE | Successor M1 delta executed under CR-2026-011. Frozen merge bytes stay unchanged as a preserved record. Independent RG1 still required. |
| `LUI-FIELD-TABLE-GAP` | `KNOWN-GAP-NO-DEDICATED-TABLE` | M1-EXPANDED | EXECUTABLE-FOUNDATION-GATE | After 6.4.4→LUR there is no dedicated LUI field table. LUI remains a sequence file. Fields are not invented. |

## Sequence endpoint bindings

| CRS | Transition | Event | Actor | Receiver | Action | Objects | Opcode | File | Direction | Layer |
|---|---|---|---|---|---|---|---|---|---|---|
| `CRS-M1-00365` | `T_UPL_LUR_WRQ` | `EV_DL_WRQ_LUR` | `DATA-LOADER` | `TARGET-HARDWARE` | `SEND-TFTP-WRITE-REQUEST` | `LUR` | `WRQ` | `LUR` | `DL-TO-TH` | `NETWORK-VISIBLE` |
| `CRS-M1-00366` | `T_UPL_LUR_ACK` | `EV_TH_ACK_LUR` | `TARGET-HARDWARE` | `DATA-LOADER` | `ACKNOWLEDGE` | `LUR-WRITE-REQUEST` | `ACK` | `LUR` | `TH-TO-DL` | `NETWORK-VISIBLE` |
| `CRS-M1-00367` | `T_UPL_LUR_XFER` | `EV_DL_DATA_LUR` | `DATA-LOADER` | `TARGET-HARDWARE` | `TRANSFER` | `LUR` | `DATA` | `LUR` | `DL-TO-TH` | `NETWORK-VISIBLE` |

## Source refinements

- `REF-A1-00143-BLOCKED-BY-FILE-IDENTITY` — `CANDIDATE-REFINEMENT` — Successor M1 delta (CR-2026-011) records CRS-M1-00143 as 6.4.4 LUR prose with HEADER-FILE. Shared object HEADER-FILE now supports a candidate 665 edge to CRS-M1-00217. Independent RG1 still required. Capability stays NOT-ESTABLISHED. (to `CRS-M1-00217` 2.2.3.1)
- `REF-A1-00315-BLOCKED-BY-FILE-IDENTITY` — `CANDIDATE-REFINEMENT` — Successor M1 delta records Table 6.4.4-1 FIELD-LOAD-PART-NUMBER-NAME as LUR. Shared object LOAD-PART-NUMBER now supports a candidate 665 edge to CRS-M1-00212. Independent RG1 still required. (to `CRS-M1-00212` 2.1.1)
- `REF-SEQ-00365-WRQ-ACTOR` — `CANDIDATE-REFINEMENT` — Successor M1 delta aligns the LUR write triad with §6.3.2 chart A and the TFTP-write machine: DATA-LOADER WRQ to TARGET-HARDWARE, TARGET-HARDWARE ACK to DATA-LOADER, DATA-LOADER DATA to TARGET-HARDWARE. DLA is the loader application layer, not a network WRQ/ACK endpoint. Independent RG1 still required. (to `None` )
- `REF-A2-TFTP-OPTION-2347` — `CANDIDATE-REFINEMENT` — 615A 5.3.2.2 requires transferring TFTP options. RFC 2347 §2 is the option-extension mechanism. The edge uses the public retrieval identity, not a fabricated PDF page. It does not claim complete RFC-2347 conformance. (to `RFC-2347` 2)
- `REF-A2-BLOCKSIZE-2348` — `CANDIDATE-REFINEMENT` — 615A 5.3.2.3.8.1 is the Blocksize Option Implementation unit already in M1 (CRS-M1-00034) with DEP-RFC-2348. A token search for 'blksize' cannot negate that source. RFC 2348 §2 is the candidate encoding. Capability stays NOT-ESTABLISHED. (to `RFC-2348` 2)
- `REF-A2-NO-RFC-1785-ACTIVE-EDGE` — `NOT-ESTABLISHED-NO-ACTIVE-SOURCE-UNIT` — UPLOAD/INFORMATION option units do not name RFC 1785 negotiation-option advertisement. P7 listings stay with unselected AFDX. (to `RFC-1785` )
- `REF-A2-NO-RFC-2349-NAME` — `NOT-ESTABLISHED-NO-ACTIVE-SOURCE-UNIT` — 615A exception and DLP timers are protocol parameters, not an identified RFC-2349 timeout/tsize option unit. (to `RFC-2349` )
- `REF-P2-PHYSICAL-ETHERNET` — `INCOMPLETE-IDENTITY-ONLY` — P2 physical identity is recorded. No clause-level model target is delivered in this candidate. This remains an incomplete task, not a bounded trace. (to `ARINC-664-2` )
- `REF-EDITION-P3-1` — `CONDITIONAL-INPUT-PENDING-RG0` — P3-1 remains a conditional historical input. Independent RG0 still decides edition acceptance. M1 blocksM1Approval snapshot is not flipped. (to `ARINC-664-3` )
- `REF-EDITION-P7-BASE` — `CONDITIONAL-INPUT-PENDING-RG0` — P7 base edition is recorded for deferred AFDX context only. (to `ARINC-664-7` )

## Network relation dispositions

- `NET-REL-001` → `ACTIVE-NORMATIVE-REFINEMENT` (M1 `APPLICABILITY-REVIEW-PENDING`)
- `NET-REL-002` → `INFRASTRUCTURE-PREMISE` (M1 `APPLICABILITY-REVIEW-PENDING`)
- `NET-REL-003` → `INFORMATIONAL-RETAINED` (M1 `NO-NORMATIVE-OVERRIDE`)
- `NET-REL-004` → `ACTIVE-NORMATIVE-REFINEMENT` (M1 `APPLICABILITY-REVIEW-PENDING`)
- `NET-REL-005` → `DEFERRED-UNSELECTED-DEPLOYMENT` (M1 `DEFERRED-FUTURE-SCOPE`)
- `NET-REL-006` → `DEFERRED-UNSELECTED-DEPLOYMENT` (M1 `DEFERRED-FUTURE-SCOPE`)
- `NET-REL-007` → `DEFERRED-UNSELECTED-DEPLOYMENT` (M1 `DEFERRED-FUTURE-SCOPE`)
- `NET-REL-008` → `DEFERRED-UNSELECTED-DEPLOYMENT` (M1 `DEFERRED-FUTURE-SCOPE`)
- `NET-REL-009` → `DEFERRED-UNSELECTED-DEPLOYMENT` (M1 `DEFERRED-FUTURE-SCOPE`)
- `NET-REL-010` → `DEFERRED-UNSELECTED-DEPLOYMENT` (M1 `DEFERRED-FUTURE-SCOPE`)
- `NET-REL-011` → `DEFERRED-UNSELECTED-DEPLOYMENT` (M1 `DEFERRED-FUTURE-SCOPE`)
- `NET-REL-012` → `DEFERRED-UNSELECTED-DEPLOYMENT` (M1 `DEFERRED-FUTURE-SCOPE`)
- `NET-REL-013` → `DEFERRED-UNSELECTED-DEPLOYMENT` (M1 `DEFERRED-FUTURE-SCOPE`)
- `NET-REL-014` → `DEFERRED-UNSELECTED-DEPLOYMENT` (M1 `DEFERRED-FUTURE-SCOPE`)
- `NET-REL-015` → `DEFERRED-UNSELECTED-DEPLOYMENT` (M1 `DEFERRED-FUTURE-SCOPE`)
- `NET-REL-016` → `DEFERRED-UNSELECTED-DEPLOYMENT` (M1 `DEFERRED-FUTURE-SCOPE`)
- `NET-REL-017` → `DEFERRED-UNSELECTED-DEPLOYMENT` (M1 `DEFERRED-FUTURE-SCOPE`)

## Discrete witnesses

- `W-UPL-ACCEPT` UPLOAD init accept: payload.decision=ACCEPT enables the branch; lastDecision is written after the guard. (4 steps)
- `W-UPL-REJECT` UPLOAD init reject from payload.decision=REJECT starting at lastDecision=NONE. (4 steps)
- `W-INF-ACCEPT` INFORMATION init accept uses the same typed payload, not a pre-written lastDecision. (4 steps)
- `W-INF-REJECT` INFORMATION init reject from payload.decision=REJECT. (4 steps)
- `W-LIST-NOT-READY` After init accept the list is not yet offered; LUR WRQ is not enabled. (5 steps)
- `W-LIST-OFFERED-NOT-READY` After the list is offered but before LUS-0001, LUR WRQ stays disabled. (6 steps)
- `W-LUR-AFTER-READY` LUS-0001 establishes session-local list readiness; only then DL WRQ LUR, TH ACK and DL DATA are enabled. (9 steps)
- `W-SESSION-RESET` A later UPLOAD start after INFORMATION completion clears list readiness; offering the list still does not enable LUR WRQ. (16 steps)
- `W-WAIT-NOT-BEFORE` WAIT retry is disabled while CLK_WAIT is below MESSAGE_TIMER_VALUE and enabled at the closed lower bound. (14 steps)
- `W-ACCEPT-WITHOUT-PAYLOAD` Accept is not enabled by lastDecision alone; missing payload.decision leaves the guard false. (4 steps)

## Blocking inputs

- `M1-FILE-IDENTITY-6-4-4` `CLOSED-BY-SUCCESSOR-M1-DELTA` authorization `CR-2026-009` blocksFinalApproval=`False` — Successor M1 delta executed under CR-2026-011. Frozen merge bytes stay unchanged. Independent RG1 still required.
- `SEQ-LUR-WRQ-ACTOR` `CLOSED-BY-SUCCESSOR-M1-DELTA` authorization `CR-2026-009` blocksFinalApproval=`False` — Successor M1 LUR write endpoints are DATA-LOADER→TARGET-HARDWARE WRQ, TARGET-HARDWARE→DATA-LOADER ACK, DATA-LOADER→TARGET-HARDWARE DATA. Frozen merge bytes stay unchanged.
- `NET-ISSUE-EDITION` `ACCEPTED-CURRENT-EDITION-P3-1-AFDX-DEFERRED` authorization `CR-2026-009` blocksFinalApproval=`False` — Owner accepted 664P3-1 as this M2 input edition; 664P7 remains recorded and AFDX stays unselected.

## Analysis boundary

- Untimed: `GRAPH-CONNECTIVITY-ON-DECLARED-TRANSITIONS`
- Timed: `NOT-CHECKED`
- Unproven: timed reachability, implementation conformance, network-stack conformance, LUI field-table predicates

## Review control

- rg0 `PENDING-EXTERNAL-REVIEW`; rg1 `PENDING-EXTERNAL-REVIEW`; rg2 `PENDING-EXTERNAL-REVIEW`
- reviewHead `UNBOUND-DRAFT`; formalApproval `EXTERNAL-JOINT-CONDITION-NOT-YET-SATISFIED`; blocksFinalApproval `True`

# 中文版

# ARINC 615A-3 M2 可观测时序模型——评审视图

> 由 `configs/models/arinc_615a3_m2_model.json` 经 `python scripts/sync_m2_model.py --write` 生成，禁止手改。

## 输入接受

- 批准 Head：`d9d844306acafd99d14ed382d1dc34dedfe837a0`
- 合并：`9bf18124d405b656815bc9eb524ae29bb4f04f56` 父提交 `75e38e08cbcab7c55ad14581e1fc605bc4106bc4` + `d9d844306acafd99d14ed382d1dc34dedfe837a0`
- 树：`2810bcaa76003eef791348607b068d76d91b5103`／批准 Head 树 `2810bcaa76003eef791348607b068d76d91b5103`
- CI：https://github.com/ZhangChi0727/arinc-615a-conformance/actions/runs/34303792744 @ `9bf18124d405b656815bc9eb524ae29bb4f04f56`
- 签署：https://github.com/ZhangChi0727/arinc-615a-conformance/pull/13#issuecomment-5594842302（`COMMENTED`，`APPROVE WITH ACTIONS`）
- 独立性：`NOT-CLAIMED-NAMED-INDEPENDENT-REVIEWER`
- M1 NET-ISSUE-EDITION 快照 blocksM1Approval=`True` — 已合并 M1 树上的历史快照。外部所有者签署与合并绑定了该 Head。该布尔值不重开合并。CR-2026-009 接受 664P3-1 作为本 M2 输入版次；664P7 保持已登记且 AFDX 未选。
- 后继增量 `CR-2026-012` 由 `CR-2026-009` 授权；doesNotTransplantFrozenApproval=`True`
- 前序输入制品提交 `402e8371b0237aec4691bab0b44e502f4ac1a7c4` 树 `26ea73a18fafbd4ba93c9dbb2890eb8453b0ad97`
- 当前输入制品提交 `bcaa4efea6e2695e3063c5a2596e9a0f019c070d` 树 `103cbc1fb5c75dd2efdf6243af0302f2a83d0800`

## 范围

- 服务：UPLOAD, INFORMATION；延期 DOWNLOAD, FIND
- 网络：`COMPLIANT`；AFDX `False`；P3 裁剪 `False`
- 形式：`M=(S,s0,V,C,P,E,T,Inv)`；初态 `S_IDLE`
- 延时时 C 中时钟增长，变量不变，不变量成立。离散步骤先绑定输入事件的有类型 payload，再求值守卫（PAYLOAD 名读取该 payload，不是隐式变量写入），然后更新、复位匹配的时钟实例、输出，进入目标。超时与 WAIT 到期事件仅由 enablingClock 与 enablingBound 之间的 COMPARE(enablingCompare) 使能。输入事件是刺激；输出是额外发射，不得把刺激再计为第二条报文。
- NETWORK-VISIBLE 事件是具名文件角色上的 TFTP 操作码。LUR 是 TFTP 写：数据加载器 WRQ、目标硬件 ACK、数据加载器 DATA。APPLICATION 的 payload.decision 是有类型枚举，在写入 lastDecision 之前参与守卫求值。PARSE-RESULT/LOCAL 事件由已收文件或本地分析导出，不是额外线上操作码。ENVIRONMENT 超时与 WAIT 到期仅由 enablingClock 与 enablingBound 的 COMPARE(enablingCompare) 使能。

## 事件

| ID | 可见性 | 摘要 |
|---|---|---|
| `EV_DL_RRQ_LCI` | NETWORK-VISIBLE | 数据加载器对 LCI 发出 TFTP RRQ |
| `EV_TH_DATA_LCI` | NETWORK-VISIBLE | 目标硬件发送 LCI 数据 |
| `EV_DL_APP_INF_RESPONSE` | APPLICATION | 分析 LCI 后的数据加载器初始化响应 |
| `EV_TH_WRQ_LCL` | NETWORK-VISIBLE | 目标硬件对 LCL 发出 TFTP WRQ |
| `EV_DL_ACK_LCL` | NETWORK-VISIBLE | 数据加载器确认 LCL WRQ |
| `EV_TH_DATA_LCL` | NETWORK-VISIBLE | 目标硬件发送 LCL 数据 |
| `EV_DL_APP_INF` | APPLICATION | 数据加载器应用层消费 LCL |
| `EV_TH_WRQ_LCS` | NETWORK-VISIBLE | 目标硬件对 LCS 发出 TFTP WRQ |
| `EV_TH_DATA_LCS` | NETWORK-VISIBLE | 目标硬件发送 LCS 数据 |
| `EV_DL_APP_INF_STATUS` | APPLICATION | 数据加载器应用层消费 LCS |
| `EV_DL_RRQ_LUI` | NETWORK-VISIBLE | 数据加载器对 LUI 发出 TFTP RRQ |
| `EV_TH_DATA_LUI` | NETWORK-VISIBLE | 目标硬件发送 LUI 数据 |
| `EV_DL_APP_UPL_RESPONSE` | APPLICATION | 分析 LUI 后的数据加载器初始化响应 |
| `EV_DL_OFFER_LIST` | APPLICATION | 初始化接受后数据加载器提交装载列表 |
| `EV_TH_LUS0001` | NETWORK-VISIBLE | 列表未接受时目标硬件发送状态 0001 的 LUS |
| `EV_DL_WRQ_LUR` | NETWORK-VISIBLE | 列表接受后数据加载器对 LUR 发出 TFTP WRQ |
| `EV_TH_ACK_LUR` | NETWORK-VISIBLE | 目标硬件确认 LUR WRQ |
| `EV_DL_DATA_LUR` | NETWORK-VISIBLE | 数据加载器发送 LUR 列表数据 |
| `EV_TH_RRQ_FILE` | NETWORK-VISIBLE | 目标硬件对请求的上载文件发出 TFTP RRQ |
| `EV_DL_FILE_UNAVAIL` | NETWORK-VISIBLE | 数据加载器报告请求文件不可用 |
| `EV_DL_DATA_FILE` | NETWORK-VISIBLE | 数据加载器发送请求的上载文件数据 |
| `EV_TH_FILE_STATUS` | LOCAL | 目标硬件在收妥后记录单文件 LUS 状态 |
| `EV_TH_MORE_FILES` | LOCAL | 目标硬件选择下一文件或转入状态 |
| `EV_TH_WRQ_LUS` | NETWORK-VISIBLE | 目标硬件对 LUS 状态发出 TFTP WRQ |
| `EV_TH_DATA_LUS` | NETWORK-VISIBLE | 目标硬件发送 LUS 数据 |
| `EV_DL_APP_UPL_STATUS` | APPLICATION | 数据加载器应用层消费 LUS |
| `EV_LOCAL_EVAL` | LOCAL | 本地评价，不声称网络可见 |
| `EV_ABORT_DL` | NETWORK-VISIBLE | 数据加载器中止 |
| `EV_ABORT_TH` | NETWORK-VISIBLE | 目标硬件中止 |
| `EV_TFTP_ACK` | NETWORK-VISIBLE | 活动文件通道上的通用 TFTP ACK |
| `EV_TFTP_ERROR` | NETWORK-VISIBLE | TFTP 错误 |
| `EV_TIMEOUT_TFTP` | ENVIRONMENT | TFTP 时钟到期；仅当 CLK_TFTP >= TFTP_TO 时使能 |
| `EV_TIMEOUT_DLP` | ENVIRONMENT | DLP 时钟到期；仅当 CLK_DLP >= DLP_TO 时使能 |
| `EV_TIMEOUT_EXCEPTION` | ENVIRONMENT | 异常时钟到期；仅当 CLK_EXCEPTION >= EXCEPTION_TIMER 时使能 |
| `EV_WAIT_RECEIVED` | PARSE-RESULT | 收到 WAIT 消息；启动不得早于该时延的时钟 |
| `EV_WAIT_ELAPSED` | ENVIRONMENT | WAIT 时延已过；仅当 CLK_WAIT >= MESSAGE_TIMER_VALUE 时使能 |
| `EV_OP_COMPLETE` | PARSE-RESULT | 由 LCS/LUS 状态判定完成，不是伪造成功 |

## 状态

| ID | 终止 | 摘要 |
|---|---|---|
| `S_IDLE` | False | 无活动操作 |
| `S_INF_LCI_RRQ` | False | INFORMATION LCI 读请求未完成 |
| `S_INF_LCI_XFER` | False | LCI TFTP 传输 |
| `S_INF_EVALUATE` | False | 本地分析 LCI，非网络可见 |
| `S_INF_REJECTED` | True | INFORMATION 初始化被拒绝 |
| `S_INF_LCL_WRQ` | False | 初始化接受后目标硬件对 LCL 发出 WRQ |
| `S_INF_LCL_XFER` | False | LCL 列表传输 |
| `S_INF_APP` | False | 应用层消费 LCL |
| `S_INF_LCS_WRQ` | False | 目标硬件对 LCS 状态发出 WRQ |
| `S_INF_LCS_XFER` | False | LCS 状态传输 |
| `S_INF_COMPLETE` | False | INFORMATION 完成，可引导 UPLOAD |
| `S_INF_EXCEPTION` | False | INFORMATION 异常等待 |
| `S_UPL_LUI_RRQ` | False | UPLOAD LUI 读请求未完成 |
| `S_UPL_LUI_XFER` | False | LUI TFTP 传输 |
| `S_UPL_EVALUATE` | False | 本地分析 LUI，非网络可见 |
| `S_UPL_REJECTED` | True | UPLOAD 初始化被拒绝 |
| `S_UPL_LIST_SENT` | False | 初始化接受后数据加载器已提交装载列表 |
| `S_UPL_WAIT_LUS0001` | False | 列表尚未接受时等待 LUS-0001 |
| `S_UPL_LUR_WRQ` | False | 列表接受后数据加载器对 LUR 发出 WRQ（TFTP 写） |
| `S_UPL_LUR_ACK` | False | 目标硬件确认 LUR 写请求 |
| `S_UPL_LUR_XFER` | False | LUR 列表传输，不同于后续文件数据 |
| `S_UPL_FILE_RRQ` | False | 目标硬件对请求的上载文件发出 RRQ |
| `S_UPL_FILE_UNAVAIL` | False | 请求文件不可用 |
| `S_UPL_FILE_XFER` | False | 请求的上载文件传输 |
| `S_UPL_FILE_STATUS` | False | 目标硬件写入单文件 LUS 状态 |
| `S_UPL_MORE_FILES` | False | 仍有文件或应更新状态 |
| `S_UPL_LUS_WRQ` | False | 目标硬件对 LUS 状态更新发出 WRQ |
| `S_UPL_LUS_XFER` | False | LUS 状态传输 |
| `S_UPL_STATUS_APP` | False | 应用层消费 LUS |
| `S_UPL_COMPLETE` | True | UPLOAD 完成，中止不记为成功 |
| `S_UPL_EXCEPTION` | False | UPLOAD 异常等待 |
| `S_WAIT_RETRY` | False | WAIT 消息时延；未到所携定时器不得重试 |
| `S_ABORTING` | False | 正在中止 |
| `S_ABORTED` | True | 中止终止态 |
| `S_FAILED` | True | 失败终止态 |

## 变量

| ID | 类型 | 初值 | 域 |
|---|---|---|---|
| `activeOperation` | ENUM | NONE | NONE, INFORMATION, UPLOAD |
| `lastDecision` | ENUM | NONE | NONE, ACCEPT, REJECT |
| `waitResume` | ENUM | NONE | NONE, UPL_FILE, UPL_LUR, INF_LCI, INF_LCL |
| `listOffered` | ENUM | FALSE | FALSE, TRUE |
| `targetListReady` | ENUM | FALSE | FALSE, TRUE |
| `listAccepted` | ENUM | FALSE | FALSE, TRUE |
| `lciComplete` | ENUM | FALSE | FALSE, TRUE |
| `lclComplete` | ENUM | FALSE | FALSE, TRUE |
| `luiComplete` | ENUM | FALSE | FALSE, TRUE |
| `lurComplete` | ENUM | FALSE | FALSE, TRUE |
| `requestedFileAvailable` | ENUM | TRUE | TRUE, FALSE |
| `moreFilesRequired` | ENUM | FALSE | TRUE, FALSE |
| `statusCode` | ENUM | NONE | NONE, 0X0001, 0X0003, FROM-LCS, FROM-LUS, EXCEPTION |
| `integrityClaim` | ENUM | FALSE | FALSE, TRUE |
| `fileBytes` | INT | 0 | — |
| `tftpRetries` | INT | 0 | — |
| `dlpRetries` | INT | 0 | — |

## 参数

| ID | 单位 | 种类 | 值 | 含义 |
|---|---|---|---|---|
| `TFTP_TO` | s | FIXED-SOURCE-CONSTANT | 2 | 定义 2 秒 TFTP 常量；响应不必恰好发生在 2 秒。 |
| `DLP_TO` | s | FIXED-SOURCE-CONSTANT | 13 | 定义 13 秒 DLP 常量；并不声称每个间隔都持续 13 秒。 |
| `TFTP_RETRY` | 1 | SYMBOLIC-SOURCE-PARAMETER | None | 附件 4 的 TFTP 重试次数。 |
| `DLP_RETRY` | 1 | SYMBOLIC-SOURCE-PARAMETER | None | 附件 4 的 DLP 重试次数。 |
| `DURATION_TIME` | s | SYMBOLIC-SOURCE-PARAMETER | None | 附件 4 不等式中的观测传输间隔。 |
| `EXCEPTION_TIMER` | s | MESSAGE-CARRIED-PARAMETER | None | 由 LCS/LUS 携带的异常定时器。 |
| `MESSAGE_TIMER_VALUE` | s | MESSAGE-CARRIED-PARAMETER | None | 等待消息定时器值。 |
| `MAX_JITTER` | us | SYMBOLIC-SOURCE-PARAMETER | None | 664-7 端系统输出公式中的观测 max_jitter。 |
| `LMAX_I` | 1 | SYMBOLIC-SOURCE-PARAMETER | None | 各 VL 最大帧长 Lmax_i，以八位组计。在已配置 VL 集合上索引，取值可以不同。每个 VL 的 20 八位组开销加在求和内部。 |
| `NBW` | 1 | SYMBOLIC-SOURCE-PARAMETER | None | 为正的介质带宽 Nbw，单位比特每秒。负载项在乘 1000000 换成微秒前是秒。除以零无定义。 |
| `FRAME_DELAY` | us | SYMBOLIC-SOURCE-PARAMETER | None | 加到发送方向 150 微秒技术时延上界上的帧时延。 |
| `TECH_LAT_TX` | us | SYMBOLIC-SOURCE-PARAMETER | None | 在具名端点之间测得的发送方向技术时延。 |
| `TECH_LAT_RX` | us | SYMBOLIC-SOURCE-PARAMETER | None | 在具名端点之间测得的接收方向技术时延。 |

## 时钟

| ID | 范围 | 关联 | 复位 | 含义 |
|---|---|---|---|---|
| `CLK_TFTP` | PER-CORRELATION-KEY | TFTP-PEER-AND-TRANSFER | `T_INF_LCI_RRQ`, `T_UPL_LUI_RRQ`, `T_UPL_LUR_WRQ`, `T_UPL_FILE_RRQ` | 相关传输中上一 TFTP 报文以来的时间。 |
| `CLK_DLP` | PER-CORRELATION-KEY | TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE | `T_INF_ACCEPT_INIT`, `T_UPL_ACCEPT_INIT`, `T_UPL_LUR_WRQ`, `T_UPL_FILE_RRQ` | 操作间／传输间 DLP 时钟。 |
| `CLK_EXCEPTION` | PER-CORRELATION-KEY | STATUS-EXCEPTION-OBJECT | `T_ENTER_UPL_EXC`, `T_ENTER_INF_EXC`, `T_INF_LCS_WRQ` | 异常静默时钟。 |
| `CLK_WAIT` | PER-CORRELATION-KEY | TFTP-PEER-AND-REJECTED-TRANSFER-REQUEST | `T_WAIT_FROM_UPL_FILE`, `T_WAIT_FROM_UPL_LUR`, `T_WAIT_FROM_INF_LCI`, `T_WAIT_FROM_INF_LCL` | 自 WAIT 消息起的时延；在所携定时器到期前禁止重试。 |
| `CLK_FIND` | PER-CORRELATION-KEY | FIND-REQUEST-INSTANCE |  | 观察用 FIND 请求／应答时钟。绑定 M2 迁移不复位该时钟。 |
| `CLK_AFDX_ES` | PER-CORRELATION-KEY | AFDX-END-SYSTEM-MEASUREMENT-INSTANCE |  | 观察用 AFDX 端系统技术时延与抖动时钟。绑定 M2 迁移不复位该时钟。 |

## 不变量

| ID | 状态 | AST | 说明 |
|---|---|---|---|
| `INV-NO-FILE-BEFORE-LUR` | `S_UPL_EVALUATE`, `S_UPL_LIST_SENT`, `S_UPL_WAIT_LUS0001`, `S_UPL_LUR_WRQ`, `S_UPL_LUR_ACK` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"lurComplete"},"right":{"kind":"ENUM","value":"FALSE"}}` | LUR 完成前禁止文件 RRQ。 |
| `INV-INTEGRITY-FALSE` | `S_UPL_COMPLETE` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"integrityClaim"},"right":{"kind":"ENUM","value":"FALSE"}}` | 645 开放时完成不得主张完整性。 |

## 迁移

| ID | 源 | 事件 | 目标 | 守卫 | 更新 | 输出 | 复位 | 需求 |
|---|---|---|---|---|---|---|---|---|
| `T_INF_LCI_RRQ` | `S_IDLE` | `EV_DL_RRQ_LCI` | `S_INF_LCI_RRQ` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"NONE"}}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"INFORMATION"}},{"kind":"ASSIGN","target":"lastDecision","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"waitResume","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"listOffered","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"targetListReady","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"listAccepted","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lurComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"luiComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lciComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lclComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"statusCode","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"integrityClaim","value":{"kind":"ENUM","value":"FALSE"}}]` | — | CLK_TFTP | `CRS-M1-00347` |
| `T_INF_LCI_XFER` | `S_INF_LCI_RRQ` | `EV_TH_DATA_LCI` | `S_INF_LCI_XFER` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | `[{"kind":"ASSIGN","target":"lciComplete","value":{"kind":"ENUM","value":"TRUE"}}]` | — | CLK_TFTP | `CRS-M1-00348` |
| `T_INF_EVAL` | `S_INF_LCI_XFER` | `EV_LOCAL_EVAL` | `S_INF_EVALUATE` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | — | — | — | `CRS-M1-00349` |
| `T_INF_ACCEPT_INIT` | `S_INF_EVALUATE` | `EV_DL_APP_INF_RESPONSE` | `S_INF_LCL_WRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"PAYLOAD","name":"decision"},"right":{"kind":"ENUM","value":"ACCEPT"}}]}` | `[{"kind":"ASSIGN","target":"lastDecision","value":{"kind":"ENUM","value":"ACCEPT"}}]` | — | CLK_DLP | `CRS-M1-00349`, `CRS-M1-00351` |
| `T_INF_REJECT` | `S_INF_EVALUATE` | `EV_DL_APP_INF_RESPONSE` | `S_INF_REJECTED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"PAYLOAD","name":"decision"},"right":{"kind":"ENUM","value":"REJECT"}}]}` | `[{"kind":"ASSIGN","target":"lastDecision","value":{"kind":"ENUM","value":"REJECT"}},{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00350` |
| `T_INF_LCL_WRQ` | `S_INF_LCL_WRQ` | `EV_TH_WRQ_LCL` | `S_INF_LCL_WRQ` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | — | — | CLK_TFTP | `CRS-M1-00351` |
| `T_INF_LCL_ACK` | `S_INF_LCL_WRQ` | `EV_DL_ACK_LCL` | `S_INF_LCL_XFER` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | — | — | CLK_TFTP | `CRS-M1-00352` |
| `T_INF_LCL_XFER` | `S_INF_LCL_XFER` | `EV_TH_DATA_LCL` | `S_INF_APP` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | `[{"kind":"ASSIGN","target":"lclComplete","value":{"kind":"ENUM","value":"TRUE"}}]` | — | CLK_TFTP | `CRS-M1-00353` |
| `T_INF_APP` | `S_INF_APP` | `EV_DL_APP_INF` | `S_INF_LCS_WRQ` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | — | — | — | `CRS-M1-00354` |
| `T_INF_LCS_WRQ` | `S_INF_LCS_WRQ` | `EV_TH_WRQ_LCS` | `S_INF_LCS_XFER` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | — | — | CLK_TFTP, CLK_EXCEPTION | `CRS-M1-00355` |
| `T_INF_LCS_XFER` | `S_INF_LCS_XFER` | `EV_TH_DATA_LCS` | `S_INF_COMPLETE` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | `[{"kind":"ASSIGN","target":"statusCode","value":{"kind":"ENUM","value":"FROM-LCS"}},{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | CLK_TFTP | `CRS-M1-00356`, `CRS-M1-00357`, `CRS-M1-00358` |
| `T_INF_SESSION_END` | `S_INF_COMPLETE` | `EV_OP_COMPLETE` | `S_IDLE` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"NONE"}}` | — | — | — | `CRS-M1-00358` |
| `T_UPL_LUI_RRQ` | `S_IDLE` | `EV_DL_RRQ_LUI` | `S_UPL_LUI_RRQ` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"NONE"}}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"ASSIGN","target":"lastDecision","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"waitResume","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"listOffered","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"targetListReady","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"listAccepted","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lurComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"luiComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lciComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lclComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"statusCode","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"integrityClaim","value":{"kind":"ENUM","value":"FALSE"}}]` | — | CLK_TFTP | `CRS-M1-00359`, `CRS-M1-00360` |
| `T_UPL_LUI_RRQ_AFTER_INF` | `S_INF_COMPLETE` | `EV_DL_RRQ_LUI` | `S_UPL_LUI_RRQ` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"NONE"}}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"ASSIGN","target":"lastDecision","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"waitResume","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"listOffered","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"targetListReady","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"listAccepted","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lurComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"luiComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lciComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"lclComplete","value":{"kind":"ENUM","value":"FALSE"}},{"kind":"ASSIGN","target":"statusCode","value":{"kind":"ENUM","value":"NONE"}},{"kind":"ASSIGN","target":"integrityClaim","value":{"kind":"ENUM","value":"FALSE"}}]` | — | CLK_TFTP | `CRS-M1-00360` |
| `T_UPL_LUI_XFER` | `S_UPL_LUI_RRQ` | `EV_TH_DATA_LUI` | `S_UPL_LUI_XFER` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | `[{"kind":"ASSIGN","target":"luiComplete","value":{"kind":"ENUM","value":"TRUE"}}]` | — | CLK_TFTP | `CRS-M1-00361` |
| `T_UPL_EVAL` | `S_UPL_LUI_XFER` | `EV_LOCAL_EVAL` | `S_UPL_EVALUATE` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | — | — | — | `CRS-M1-00362` |
| `T_UPL_ACCEPT_INIT` | `S_UPL_EVALUATE` | `EV_DL_APP_UPL_RESPONSE` | `S_UPL_LIST_SENT` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"PAYLOAD","name":"decision"},"right":{"kind":"ENUM","value":"ACCEPT"}}]}` | `[{"kind":"ASSIGN","target":"lastDecision","value":{"kind":"ENUM","value":"ACCEPT"}}]` | — | CLK_DLP | `CRS-M1-00362`, `CRS-M1-00363` |
| `T_UPL_REJECT` | `S_UPL_EVALUATE` | `EV_DL_APP_UPL_RESPONSE` | `S_UPL_REJECTED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"PAYLOAD","name":"decision"},"right":{"kind":"ENUM","value":"REJECT"}}]}` | `[{"kind":"ASSIGN","target":"lastDecision","value":{"kind":"ENUM","value":"REJECT"}},{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00362` |
| `T_UPL_LIST_OFFER` | `S_UPL_LIST_SENT` | `EV_DL_OFFER_LIST` | `S_UPL_WAIT_LUS0001` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | `[{"kind":"ASSIGN","target":"listOffered","value":{"kind":"ENUM","value":"TRUE"}}]` | — | CLK_DLP | `CRS-M1-00363`, `CRS-M1-00364` |
| `T_UPL_WAIT_LUS0001` | `S_UPL_WAIT_LUS0001` | `EV_TH_LUS0001` | `S_UPL_WAIT_LUS0001` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"listOffered"},"right":{"kind":"ENUM","value":"TRUE"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"listAccepted"},"right":{"kind":"ENUM","value":"FALSE"}}]}` | `[{"kind":"ASSIGN","target":"statusCode","value":{"kind":"ENUM","value":"0X0001"}},{"kind":"ASSIGN","target":"targetListReady","value":{"kind":"ENUM","value":"TRUE"}}]` | — | CLK_EXCEPTION | `CRS-M1-00364` |
| `T_UPL_LUR_WRQ` | `S_UPL_WAIT_LUS0001` | `EV_DL_WRQ_LUR` | `S_UPL_LUR_WRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"listOffered"},"right":{"kind":"ENUM","value":"TRUE"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"targetListReady"},"right":{"kind":"ENUM","value":"TRUE"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"listAccepted"},"right":{"kind":"ENUM","value":"FALSE"}}]}` | `[{"kind":"ASSIGN","target":"listAccepted","value":{"kind":"ENUM","value":"TRUE"}}]` | — | CLK_TFTP, CLK_DLP | `CRS-M1-00365` |
| `T_UPL_LUR_ACK` | `S_UPL_LUR_WRQ` | `EV_TH_ACK_LUR` | `S_UPL_LUR_ACK` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | — | — | CLK_TFTP | `CRS-M1-00366` |
| `T_UPL_LUR_XFER` | `S_UPL_LUR_ACK` | `EV_DL_DATA_LUR` | `S_UPL_LUR_XFER` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | `[{"kind":"ASSIGN","target":"lurComplete","value":{"kind":"ENUM","value":"TRUE"}}]` | — | CLK_TFTP | `CRS-M1-00367` |
| `T_UPL_FILE_RRQ` | `S_UPL_LUR_XFER` | `EV_TH_RRQ_FILE` | `S_UPL_FILE_RRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"lurComplete"},"right":{"kind":"ENUM","value":"TRUE"}}]}` | — | — | CLK_TFTP, CLK_DLP | `CRS-M1-00368` |
| `T_UPL_FILE_RRQ_MORE` | `S_UPL_MORE_FILES` | `EV_TH_RRQ_FILE` | `S_UPL_FILE_RRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"moreFilesRequired"},"right":{"kind":"ENUM","value":"TRUE"}}]}` | — | — | CLK_TFTP | `CRS-M1-00368`, `CRS-M1-00372` |
| `T_UPL_FILE_UNAVAIL` | `S_UPL_FILE_RRQ` | `EV_DL_FILE_UNAVAIL` | `S_UPL_FILE_UNAVAIL` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"requestedFileAvailable"},"right":{"kind":"ENUM","value":"FALSE"}}]}` | — | — | — | `CRS-M1-00369` |
| `T_UPL_FILE_XFER` | `S_UPL_FILE_RRQ` | `EV_DL_DATA_FILE` | `S_UPL_FILE_XFER` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"requestedFileAvailable"},"right":{"kind":"ENUM","value":"TRUE"}}]}` | `[{"kind":"ASSIGN","target":"fileBytes","value":{"kind":"LITERAL","value":0}}]` | — | CLK_TFTP | `CRS-M1-00370` |
| `T_UPL_FILE_STATUS` | `S_UPL_FILE_XFER` | `EV_TH_FILE_STATUS` | `S_UPL_FILE_STATUS` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | — | — | — | `CRS-M1-00371` |
| `T_UPL_MORE_FILES` | `S_UPL_FILE_STATUS` | `EV_TH_MORE_FILES` | `S_UPL_MORE_FILES` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | — | — | — | `CRS-M1-00372` |
| `T_UPL_TO_LUS` | `S_UPL_MORE_FILES` | `EV_TH_WRQ_LUS` | `S_UPL_LUS_WRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"moreFilesRequired"},"right":{"kind":"ENUM","value":"FALSE"}}]}` | — | — | CLK_TFTP | `CRS-M1-00373` |
| `T_UPL_LUS_XFER` | `S_UPL_LUS_WRQ` | `EV_TH_DATA_LUS` | `S_UPL_LUS_XFER` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | `[{"kind":"ASSIGN","target":"statusCode","value":{"kind":"ENUM","value":"FROM-LUS"}}]` | — | CLK_TFTP, CLK_EXCEPTION | `CRS-M1-00374` |
| `T_UPL_STATUS_APP` | `S_UPL_LUS_XFER` | `EV_DL_APP_UPL_STATUS` | `S_UPL_STATUS_APP` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | — | — | — | `CRS-M1-00375` |
| `T_UPL_COMPLETE` | `S_UPL_STATUS_APP` | `EV_OP_COMPLETE` | `S_UPL_COMPLETE` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"statusCode"},"right":{"kind":"ENUM","value":"0X0003"}},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"integrityClaim"},"right":{"kind":"ENUM","value":"FALSE"}}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00376` |
| `T_UPL_STATUS_REPEAT` | `S_UPL_STATUS_APP` | `EV_TH_MORE_FILES` | `S_UPL_MORE_FILES` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"COMPARE","op":"NE","left":{"kind":"VAR","name":"statusCode"},"right":{"kind":"ENUM","value":"0X0003"}}]}` | — | — | — | `CRS-M1-00376` |
| `T_INF_TFTP_TO` | `S_INF_LCI_RRQ` | `EV_TIMEOUT_TFTP` | `S_FAILED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_TFTP"},"right":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"}}]}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00177` |
| `T_UPL_TFTP_TO` | `S_UPL_LUI_RRQ` | `EV_TIMEOUT_TFTP` | `S_FAILED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_TFTP"},"right":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"}}]}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00177` |
| `T_UPL_LUR_TFTP_TO` | `S_UPL_LUR_WRQ` | `EV_TIMEOUT_TFTP` | `S_FAILED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_TFTP"},"right":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"}}]}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00177` |
| `T_UPL_FILE_TFTP_TO` | `S_UPL_FILE_RRQ` | `EV_TIMEOUT_TFTP` | `S_FAILED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_TFTP"},"right":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"}}]}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00177` |
| `T_UPL_DLP_TO` | `S_UPL_WAIT_LUS0001` | `EV_TIMEOUT_DLP` | `S_FAILED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}]}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00187` |
| `T_UPL_LUR_DLP_TO` | `S_UPL_LUR_XFER` | `EV_TIMEOUT_DLP` | `S_FAILED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}]}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00187`, `CRS-M1-00188` |
| `T_UPL_EXC_TO` | `S_UPL_EXCEPTION` | `EV_TIMEOUT_EXCEPTION` | `S_FAILED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}]}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00101`, `CRS-M1-00108` |
| `T_INF_EXC_TO` | `S_INF_EXCEPTION` | `EV_TIMEOUT_EXCEPTION` | `S_FAILED` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}]}]}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00101` |
| `T_ENTER_UPL_EXC` | `S_UPL_WAIT_LUS0001` | `EV_TH_DATA_LUS` | `S_UPL_EXCEPTION` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | `[{"kind":"ASSIGN","target":"statusCode","value":{"kind":"ENUM","value":"EXCEPTION"}}]` | — | CLK_EXCEPTION | `CRS-M1-00099` |
| `T_ENTER_INF_EXC` | `S_INF_LCS_XFER` | `EV_DL_APP_INF_STATUS` | `S_INF_EXCEPTION` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | `[{"kind":"ASSIGN","target":"statusCode","value":{"kind":"ENUM","value":"EXCEPTION"}}]` | — | CLK_EXCEPTION | `CRS-M1-00099` |
| `T_WAIT_FROM_UPL_FILE` | `S_UPL_FILE_XFER` | `EV_WAIT_RECEIVED` | `S_WAIT_RETRY` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | `[{"kind":"ASSIGN","target":"waitResume","value":{"kind":"ENUM","value":"UPL_FILE"}}]` | — | CLK_WAIT | `CRS-M1-00032` |
| `T_WAIT_FROM_UPL_LUR` | `S_UPL_LUR_XFER` | `EV_WAIT_RECEIVED` | `S_WAIT_RETRY` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | `[{"kind":"ASSIGN","target":"waitResume","value":{"kind":"ENUM","value":"UPL_LUR"}}]` | — | CLK_WAIT | `CRS-M1-00032` |
| `T_WAIT_FROM_INF_LCI` | `S_INF_LCI_XFER` | `EV_WAIT_RECEIVED` | `S_WAIT_RETRY` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | `[{"kind":"ASSIGN","target":"waitResume","value":{"kind":"ENUM","value":"INF_LCI"}}]` | — | CLK_WAIT | `CRS-M1-00032` |
| `T_WAIT_FROM_INF_LCL` | `S_INF_LCL_XFER` | `EV_WAIT_RECEIVED` | `S_WAIT_RETRY` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}}` | `[{"kind":"ASSIGN","target":"waitResume","value":{"kind":"ENUM","value":"INF_LCL"}}]` | — | CLK_WAIT | `CRS-M1-00032` |
| `T_WAIT_RETRY_UPL_FILE` | `S_WAIT_RETRY` | `EV_WAIT_ELAPSED` | `S_UPL_FILE_RRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_WAIT"},"right":{"kind":"SYMBOL","name":"MESSAGE_TIMER_VALUE","unit":"s"}}]},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"waitResume"},"right":{"kind":"ENUM","value":"UPL_FILE"}}]}` | — | — | CLK_TFTP | `CRS-M1-00032` |
| `T_WAIT_RETRY_UPL_LUR` | `S_WAIT_RETRY` | `EV_WAIT_ELAPSED` | `S_UPL_LUR_WRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_WAIT"},"right":{"kind":"SYMBOL","name":"MESSAGE_TIMER_VALUE","unit":"s"}}]},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"waitResume"},"right":{"kind":"ENUM","value":"UPL_LUR"}}]}` | — | — | CLK_TFTP | `CRS-M1-00032` |
| `T_WAIT_RETRY_INF_LCI` | `S_WAIT_RETRY` | `EV_WAIT_ELAPSED` | `S_INF_LCI_RRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_WAIT"},"right":{"kind":"SYMBOL","name":"MESSAGE_TIMER_VALUE","unit":"s"}}]},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"waitResume"},"right":{"kind":"ENUM","value":"INF_LCI"}}]}` | — | — | CLK_TFTP | `CRS-M1-00032` |
| `T_WAIT_RETRY_INF_LCL` | `S_WAIT_RETRY` | `EV_WAIT_ELAPSED` | `S_INF_LCL_WRQ` | `{"kind":"AND","args":[{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"INFORMATION"}},{"kind":"AND","args":[{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_WAIT"},"right":{"kind":"SYMBOL","name":"MESSAGE_TIMER_VALUE","unit":"s"}}]},{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"waitResume"},"right":{"kind":"ENUM","value":"INF_LCL"}}]}` | — | — | CLK_TFTP | `CRS-M1-00032` |
| `T_ABORT_DL` | `S_UPL_FILE_XFER` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_TH` | `S_UPL_FILE_XFER` | `EV_ABORT_TH` | `S_ABORTING` | `{"kind":"COMPARE","op":"EQ","left":{"kind":"VAR","name":"activeOperation"},"right":{"kind":"ENUM","value":"UPLOAD"}}` | — | — | — | `CRS-M1-00340` |
| `T_ABORTED` | `S_ABORTING` | `EV_OP_COMPLETE` | `S_ABORTED` | `{"kind":"TRUE"}` | `[{"kind":"ASSIGN","target":"activeOperation","value":{"kind":"ENUM","value":"NONE"}}]` | — | — | `CRS-M1-00340`, `CRS-M1-00341` |
| `T_ABORT_FROM_S_INF_LCI_RRQ` | `S_INF_LCI_RRQ` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_INF_LCL_XFER` | `S_INF_LCL_XFER` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_INF_LCS_XFER` | `S_INF_LCS_XFER` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_INF_EXCEPTION` | `S_INF_EXCEPTION` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_WAIT_RETRY` | `S_WAIT_RETRY` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_UPL_LUI_XFER` | `S_UPL_LUI_XFER` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_UPL_LIST_SENT` | `S_UPL_LIST_SENT` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_UPL_WAIT_LUS0001` | `S_UPL_WAIT_LUS0001` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_UPL_LUR_XFER` | `S_UPL_LUR_XFER` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |
| `T_ABORT_FROM_S_UPL_LUS_XFER` | `S_UPL_LUS_XFER` | `EV_ABORT_DL` | `S_ABORTING` | `{"kind":"TRUE"}` | — | — | — | `CRS-M1-00341` |

## 顺序约束

- `SEQ-UPL-LIST-BEFORE-FILE` 顺序 `S_UPL_EVALUATE` → `S_UPL_LIST_SENT` → `S_UPL_WAIT_LUS0001` → `S_UPL_LUR_WRQ` → `S_UPL_LUR_ACK` → `S_UPL_LUR_XFER` → `S_UPL_FILE_RRQ`；禁止 [['S_UPL_EVALUATE', 'S_UPL_FILE_RRQ'], ['S_UPL_EVALUATE', 'S_UPL_FILE_XFER'], ['S_UPL_LIST_SENT', 'S_UPL_FILE_RRQ'], ['S_UPL_WAIT_LUS0001', 'S_UPL_FILE_RRQ'], ['S_UPL_WAIT_LUS0001', 'S_UPL_FILE_XFER'], ['S_INF_EVALUATE', 'S_UPL_FILE_XFER']]；图 6.3.2 A 要求在文件 RRQ 之前完成列表接受与 LUR 传输。
- `SEQ-INF-LCL-BEFORE-LCS` 顺序 `S_INF_EVALUATE` → `S_INF_LCL_WRQ` → `S_INF_LCL_XFER` → `S_INF_LCS_WRQ`；禁止 [['S_INF_EVALUATE', 'S_INF_LCS_XFER']]；INFORMATION 的 LCL 列表先于 LCS 状态。

## 字段约束

| ID | 文件 | 字段 | CRS | 检查点 |
|---|---|---|---|---|
| `FC-LCI-FIELD-FILE-LENGTH` | LCI | FIELD-FILE-LENGTH | `CRS-M1-00282` | LCI-FILE-BYTES |
| `FC-LCI-FIELD-PROTOCOL-VERSION` | LCI | FIELD-PROTOCOL-VERSION | `CRS-M1-00283` | LCI-FILE-BYTES |
| `FC-LCI-FIELD-OPERATION-ACCEPTANCE-STATUS-CODE` | LCI | FIELD-OPERATION-ACCEPTANCE-STATUS-CODE | `CRS-M1-00284` | LCI-FILE-BYTES |
| `FC-LCI-FIELD-STATUS-DESCRIPTION-LENGTH` | LCI | FIELD-STATUS-DESCRIPTION-LENGTH | `CRS-M1-00285` | LCI-FILE-BYTES |
| `FC-LCI-FIELD-STATUS-DESCRIPTION` | LCI | FIELD-STATUS-DESCRIPTION | `CRS-M1-00286` | LCI-FILE-BYTES |
| `FC-LCL-FIELD-FILE-LENGTH` | LCL | FIELD-FILE-LENGTH | `CRS-M1-00287` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-PROTOCOL-VERSION` | LCL | FIELD-PROTOCOL-VERSION | `CRS-M1-00288` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-NUMBER-OF-TARGET-HARDWARE` | LCL | FIELD-NUMBER-OF-TARGET-HARDWARE | `CRS-M1-00289` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-LITERAL-NAME-LENGTH` | LCL | FIELD-LITERAL-NAME-LENGTH | `CRS-M1-00290` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-LITERAL-NAME` | LCL | FIELD-LITERAL-NAME | `CRS-M1-00291` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-SERIAL-NUMBER-LENGTH` | LCL | FIELD-SERIAL-NUMBER-LENGTH | `CRS-M1-00292` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-SERIAL-NUMBER` | LCL | FIELD-SERIAL-NUMBER | `CRS-M1-00293` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-NUMBER-OF-PART-NUMBERS` | LCL | FIELD-NUMBER-OF-PART-NUMBERS | `CRS-M1-00294` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-PART-NUMBER-LENGTH` | LCL | FIELD-PART-NUMBER-LENGTH | `CRS-M1-00295` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-PART-NUMBER` | LCL | FIELD-PART-NUMBER | `CRS-M1-00296` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-AMENDMENT-LENGTH` | LCL | FIELD-AMENDMENT-LENGTH | `CRS-M1-00297` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-AMENDMENT` | LCL | FIELD-AMENDMENT | `CRS-M1-00298` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-PART-DESIGNATION-LENGTH` | LCL | FIELD-PART-DESIGNATION-LENGTH | `CRS-M1-00299` | LCL-FILE-BYTES |
| `FC-LCL-FIELD-PART-DESIGNATION-TEXT` | LCL | FIELD-PART-DESIGNATION-TEXT | `CRS-M1-00300` | LCL-FILE-BYTES |
| `FC-LCS-FIELD-FILE-LENGTH` | LCS | FIELD-FILE-LENGTH | `CRS-M1-00301` | LCS-FILE-BYTES |
| `FC-LCS-FIELD-PROTOCOL-VERSION` | LCS | FIELD-PROTOCOL-VERSION | `CRS-M1-00302` | LCS-FILE-BYTES |
| `FC-LCS-FIELD-COUNTER` | LCS | FIELD-COUNTER | `CRS-M1-00303` | LCS-FILE-BYTES |
| `FC-LCS-FIELD-INFORMATION-OPERATION-STATUS-CODE` | LCS | FIELD-INFORMATION-OPERATION-STATUS-CODE | `CRS-M1-00304` | LCS-FILE-BYTES |
| `FC-LCS-FIELD-EXCEPTION-TIMER` | LCS | FIELD-EXCEPTION-TIMER | `CRS-M1-00305` | LCS-FILE-BYTES |
| `FC-LCS-FIELD-ESTIMATED-TIME` | LCS | FIELD-ESTIMATED-TIME | `CRS-M1-00306` | LCS-FILE-BYTES |
| `FC-LCS-FIELD-STATUS-DESCRIPTION-LENGTH` | LCS | FIELD-STATUS-DESCRIPTION-LENGTH | `CRS-M1-00307` | LCS-FILE-BYTES |
| `FC-LCS-FIELD-STATUS-DESCRIPTION` | LCS | FIELD-STATUS-DESCRIPTION | `CRS-M1-00308` | LCS-FILE-BYTES |
| `FC-LUR-FIELD-FILE-LENGTH` | LUR | FIELD-FILE-LENGTH | `CRS-M1-00309` | LUR-FILE-BYTES |
| `FC-LUR-FIELD-PROTOCOL-VERSION` | LUR | FIELD-PROTOCOL-VERSION | `CRS-M1-00310` | LUR-FILE-BYTES |
| `FC-LUR-FIELD-NUMBER-OF-HEADER-FILES` | LUR | FIELD-NUMBER-OF-HEADER-FILES | `CRS-M1-00311` | LUR-FILE-BYTES |
| `FC-LUR-FIELD-HEADER-FILE-NAME-LENGTH` | LUR | FIELD-HEADER-FILE-NAME-LENGTH | `CRS-M1-00312` | LUR-FILE-BYTES |
| `FC-LUR-FIELD-HEADER-FILE-NAME` | LUR | FIELD-HEADER-FILE-NAME | `CRS-M1-00313` | LUR-FILE-BYTES |
| `FC-LUR-FIELD-LOAD-PART-NUMBER-NAME-LENGTH` | LUR | FIELD-LOAD-PART-NUMBER-NAME-LENGTH | `CRS-M1-00314` | LUR-FILE-BYTES |
| `FC-LUR-FIELD-LOAD-PART-NUMBER-NAME` | LUR | FIELD-LOAD-PART-NUMBER-NAME | `CRS-M1-00315` | LUR-FILE-BYTES |
| `FC-LUS-FIELD-FILE-LENGTH` | LUS | FIELD-FILE-LENGTH | `CRS-M1-00316` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-PROTOCOL-VERSION` | LUS | FIELD-PROTOCOL-VERSION | `CRS-M1-00317` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-UPLOAD-OPERATION-STATUS-CODE` | LUS | FIELD-UPLOAD-OPERATION-STATUS-CODE | `CRS-M1-00318` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-UPLOAD-STATUS-DESCRIPTION-LENGTH` | LUS | FIELD-UPLOAD-STATUS-DESCRIPTION-LENGTH | `CRS-M1-00319` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-UPLOAD-STATUS-DESCRIPTION` | LUS | FIELD-UPLOAD-STATUS-DESCRIPTION | `CRS-M1-00320` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-COUNTER` | LUS | FIELD-COUNTER | `CRS-M1-00321` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-EXCEPTION-TIMER` | LUS | FIELD-EXCEPTION-TIMER | `CRS-M1-00322` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-ESTIMATED-TIME` | LUS | FIELD-ESTIMATED-TIME | `CRS-M1-00323` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-LOAD-LIST-RATIO` | LUS | FIELD-LOAD-LIST-RATIO | `CRS-M1-00324` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-NUMBER-OF-HEADER-FILES` | LUS | FIELD-NUMBER-OF-HEADER-FILES | `CRS-M1-00325` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-HEADER-FILE-NAME-LENGTH` | LUS | FIELD-HEADER-FILE-NAME-LENGTH | `CRS-M1-00326` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-HEADER-FILE-NAME` | LUS | FIELD-HEADER-FILE-NAME | `CRS-M1-00327` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-LOAD-PART-NUMBER-NAME-LENGTH` | LUS | FIELD-LOAD-PART-NUMBER-NAME-LENGTH | `CRS-M1-00328` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-LOAD-PART-NUMBER-NAME` | LUS | FIELD-LOAD-PART-NUMBER-NAME | `CRS-M1-00329` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-LOAD-RATIO` | LUS | FIELD-LOAD-RATIO | `CRS-M1-00330` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-LOAD-STATUS` | LUS | FIELD-LOAD-STATUS | `CRS-M1-00331` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-LOAD-STATUS-DESCRIPTION-LENGTH` | LUS | FIELD-LOAD-STATUS-DESCRIPTION-LENGTH | `CRS-M1-00332` | LUS-FILE-BYTES |
| `FC-LUS-FIELD-LOAD-STATUS-DESCRIPTION` | LUS | FIELD-LOAD-STATUS-DESCRIPTION | `CRS-M1-00333` | LUS-FILE-BYTES |
| `FC-LNR-FIELD-FILE-LENGTH` | LNR | FIELD-FILE-LENGTH | `CRS-M1-00459` | LNR-FILE-BYTES |
| `FC-LNR-FIELD-PROTOCOL-VERSION` | LNR | FIELD-PROTOCOL-VERSION | `CRS-M1-00460` | LNR-FILE-BYTES |
| `FC-LNR-FIELD-NUMBER-OF-FILES` | LNR | FIELD-NUMBER-OF-FILES | `CRS-M1-00461` | LNR-FILE-BYTES |
| `FC-LNR-FIELD-FILE-NAME-LENGTH` | LNR | FIELD-FILE-NAME-LENGTH | `CRS-M1-00462` | LNR-FILE-BYTES |
| `FC-LNR-FIELD-FILE-NAME` | LNR | FIELD-FILE-NAME | `CRS-M1-00463` | LNR-FILE-BYTES |
| `FC-LNR-FIELD-USER-DEFINED-DATA-LENGTH` | LNR | FIELD-USER-DEFINED-DATA-LENGTH | `CRS-M1-00464` | LNR-FILE-BYTES |
| `FC-LNR-FIELD-USER-DEFINED-DATA` | LNR | FIELD-USER-DEFINED-DATA | `CRS-M1-00465` | LNR-FILE-BYTES |
| `FC-LNS-FIELD-FILE-LENGTH` | LNS | FIELD-FILE-LENGTH | `CRS-M1-00466` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-PROTOCOL-VERSION` | LNS | FIELD-PROTOCOL-VERSION | `CRS-M1-00467` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-DOWNLOAD-OPERATION-STATUS-CODE` | LNS | FIELD-DOWNLOAD-OPERATION-STATUS-CODE | `CRS-M1-00468` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-DOWNLOAD-STATUS-DESCRIPTION-LENGTH` | LNS | FIELD-DOWNLOAD-STATUS-DESCRIPTION-LENGTH | `CRS-M1-00469` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-DOWNLOAD-STATUS-DESCRIPTION` | LNS | FIELD-DOWNLOAD-STATUS-DESCRIPTION | `CRS-M1-00470` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-COUNTER` | LNS | FIELD-COUNTER | `CRS-M1-00471` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-EXCEPTION-TIMER` | LNS | FIELD-EXCEPTION-TIMER | `CRS-M1-00472` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-ESTIMATED-TIME` | LNS | FIELD-ESTIMATED-TIME | `CRS-M1-00473` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-DOWNLOAD-LIST-RATIO` | LNS | FIELD-DOWNLOAD-LIST-RATIO | `CRS-M1-00474` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-NUMBER-OF-FILES` | LNS | FIELD-NUMBER-OF-FILES | `CRS-M1-00475` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-FILE-NAME-LENGTH` | LNS | FIELD-FILE-NAME-LENGTH | `CRS-M1-00476` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-FILE-NAME` | LNS | FIELD-FILE-NAME | `CRS-M1-00477` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-FILE-STATUS` | LNS | FIELD-FILE-STATUS | `CRS-M1-00478` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-FILE-STATUS-DESCRIPTION-LENGTH` | LNS | FIELD-FILE-STATUS-DESCRIPTION-LENGTH | `CRS-M1-00479` | LNS-FILE-BYTES |
| `FC-LNS-FIELD-FILE-STATUS-DESCRIPTION` | LNS | FIELD-FILE-STATUS-DESCRIPTION | `CRS-M1-00480` | LNS-FILE-BYTES |
| `FC-LNL-FIELD-FILE-LENGTH` | LNL | FIELD-FILE-LENGTH | `CRS-M1-00481` | LNL-FILE-BYTES |
| `FC-LNL-FIELD-PROTOCOL-VERSION` | LNL | FIELD-PROTOCOL-VERSION | `CRS-M1-00482` | LNL-FILE-BYTES |
| `FC-LNL-FIELD-NUMBER-OF-FILES` | LNL | FIELD-NUMBER-OF-FILES | `CRS-M1-00483` | LNL-FILE-BYTES |
| `FC-LNL-FIELD-FILE-NAME-LENGTH` | LNL | FIELD-FILE-NAME-LENGTH | `CRS-M1-00484` | LNL-FILE-BYTES |
| `FC-LNL-FIELD-FILE-NAME` | LNL | FIELD-FILE-NAME | `CRS-M1-00485` | LNL-FILE-BYTES |
| `FC-LNL-FIELD-FILE-DESCRIPTION-LENGTH` | LNL | FIELD-FILE-DESCRIPTION-LENGTH | `CRS-M1-00486` | LNL-FILE-BYTES |
| `FC-LNL-FIELD-FILE-DESCRIPTION` | LNL | FIELD-FILE-DESCRIPTION | `CRS-M1-00487` | LNL-FILE-BYTES |
| `FC-LNA-FIELD-FILE-LENGTH` | LNA | FIELD-FILE-LENGTH | `CRS-M1-00488` | LNA-FILE-BYTES |
| `FC-LNA-FIELD-PROTOCOL-VERSION` | LNA | FIELD-PROTOCOL-VERSION | `CRS-M1-00489` | LNA-FILE-BYTES |
| `FC-LNA-FIELD-NUMBER-OF-FILES` | LNA | FIELD-NUMBER-OF-FILES | `CRS-M1-00490` | LNA-FILE-BYTES |
| `FC-LNA-FIELD-FILE-NAME-LENGTH` | LNA | FIELD-FILE-NAME-LENGTH | `CRS-M1-00491` | LNA-FILE-BYTES |
| `FC-LNA-FIELD-FILE-NAME` | LNA | FIELD-FILE-NAME | `CRS-M1-00492` | LNA-FILE-BYTES |
| `FC-LUB-FIELD-BATCH-FILE-LENGTH` | LUB | FIELD-BATCH-FILE-LENGTH | `CRS-M1-00546` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-BATCH-FILE-FORMAT-VERSION` | LUB | FIELD-BATCH-FILE-FORMAT-VERSION | `CRS-M1-00547` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-SPARE` | LUB | FIELD-SPARE | `CRS-M1-00548` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-POINTER-TO-BATCH-FILE-PN-LENGTH` | LUB | FIELD-POINTER-TO-BATCH-FILE-PN-LENGTH | `CRS-M1-00549` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-POINTER-TO-NUMBER-OF-TARGET-HW-ID-LOAD-LIST-BLOCKS` | LUB | FIELD-POINTER-TO-NUMBER-OF-TARGET-HW-ID-LOAD-LIST-BLOCKS | `CRS-M1-00550` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-EXPANSION-POINT-1` | LUB | FIELD-EXPANSION-POINT-1 | `CRS-M1-00551` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-BATCH-FILE-PN-LENGTH` | LUB | FIELD-BATCH-FILE-PN-LENGTH | `CRS-M1-00552` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-BATCH-FILE-PN` | LUB | FIELD-BATCH-FILE-PN | `CRS-M1-00553` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-COMMENT-LENGTH` | LUB | FIELD-COMMENT-LENGTH | `CRS-M1-00554` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-COMMENT` | LUB | FIELD-COMMENT | `CRS-M1-00555` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-EXPANSION-POINT-2` | LUB | FIELD-EXPANSION-POINT-2 | `CRS-M1-00556` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-NUMBER-OF-TARGET-HW-ID-LOAD-LIST-BLOCKS` | LUB | FIELD-NUMBER-OF-TARGET-HW-ID-LOAD-LIST-BLOCKS | `CRS-M1-00557` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-POINTER-TO-NEXT-TARGET-HW-ID-LOAD-LIST-BLOCK` | LUB | FIELD-POINTER-TO-NEXT-TARGET-HW-ID-LOAD-LIST-BLOCK | `CRS-M1-00558` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-TARGET-HW-ID-POS-LENGTH` | LUB | FIELD-TARGET-HW-ID-POS-LENGTH | `CRS-M1-00559` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-TARGET-HW-ID-POS` | LUB | FIELD-TARGET-HW-ID-POS | `CRS-M1-00560` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-NUMBER-OF-LOADS-FOR-TARGET-HW-ID-POS` | LUB | FIELD-NUMBER-OF-LOADS-FOR-TARGET-HW-ID-POS | `CRS-M1-00561` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-HEADER-FILE-NAME-LENGTH` | LUB | FIELD-HEADER-FILE-NAME-LENGTH | `CRS-M1-00562` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-HEADER-FILE-NAME` | LUB | FIELD-HEADER-FILE-NAME | `CRS-M1-00563` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-LOAD-PN-LENGTH` | LUB | FIELD-LOAD-PN-LENGTH | `CRS-M1-00564` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-LOAD-PN` | LUB | FIELD-LOAD-PN | `CRS-M1-00565` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-EXPANSION-POINT-3` | LUB | FIELD-EXPANSION-POINT-3 | `CRS-M1-00566` | LUB-FILE-BYTES |
| `FC-LUB-FIELD-BATCH-FILE-CRC` | LUB | FIELD-BATCH-FILE-CRC | `CRS-M1-00567` | LUB-FILE-BYTES |

## 状态约束

| ID | CRS | 代码 | 检查点 |
|---|---|---|---|
| `ST-CRS-M1-00334` | `CRS-M1-00334` | 0X0001 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00335` | `CRS-M1-00335` | 0X1000 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00336` | `CRS-M1-00336` | 0X1002 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00337` | `CRS-M1-00337` | 0X0002 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00338` | `CRS-M1-00338` | 0X0003 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00339` | `CRS-M1-00339` | 0X0004 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00340` | `CRS-M1-00340` | 0X1003 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00341` | `CRS-M1-00341` | 0X1004 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00342` | `CRS-M1-00342` | 0X1005 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00343` | `CRS-M1-00343` | 0X1007 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00344` | `CRS-M1-00344` | 0X1007 | STATUS-FILE-AND-DISPLAY |
| `ST-CRS-M1-00345` | `CRS-M1-00345` | DISPLAY-FOOTNOTE | STATUS-FILE-AND-DISPLAY |

## 对象约束

| ID | CRS | 动作 | 检查点 |
|---|---|---|---|
| `OBJ-MINIMUM-ARINC-665-COMPATIBILITY-CAPABILITIES-IMPLEMENT-REQUIRED-ARINC-665-CA-CRS-M1-00191` | `CRS-M1-00191` | IMPLEMENT-REQUIRED-ARINC-665-CAPABILITIES | ARINC-665-DATA-OBJECT |
| `OBJ-ARINC-665-SHOULD-MODALITY-TREAT-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY-CRS-M1-00192` | `CRS-M1-00192` | TREAT-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY | ARINC-665-DATA-OBJECT |
| `OBJ-ARINC-665-MAY-MODALITY-TREAT-MAY-AS-OPTIONAL-CAPABILITY-CRS-M1-00193` | `CRS-M1-00193` | TREAT-MAY-AS-OPTIONAL-CAPABILITY | ARINC-665-DATA-OBJECT |
| `OBJ-OPTIONAL-ARINC-665-CAPABILITY-CONDITIONALLY-IMPLEMENT-OPTIONAL-CAPABILITY-AS-CRS-M1-00194` | `CRS-M1-00194` | CONDITIONALLY-IMPLEMENT-OPTIONAL-CAPABILITY-AS-SPECIFIED | ARINC-665-DATA-OBJECT |
| `OBJ-DATA-FIELD-TYPE-INTERPRET-FIELDS-AS-NUMERIC-BY-DEFAULT-CRS-M1-00195` | `CRS-M1-00195` | INTERPRET-FIELDS-AS-NUMERIC-BY-DEFAULT | ARINC-665-DATA-OBJECT |
| `OBJ-ARINC-665-FILE-PROHIBIT-UNDEFINED-FIELD-INSERTION-CRS-M1-00196` | `CRS-M1-00196` | PROHIBIT-UNDEFINED-FIELD-INSERTION | ARINC-665-DATA-OBJECT |
| `OBJ-FILE-VERSION-COMPATIBILITY-ENCODE-CRS-M1-00197` | `CRS-M1-00197` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-TARGET-HARDWARE-ID-MANUFACTURER-IDENTIFIER-PREFIX-TARGET-HARDWARE-ID-WITH-MA-CRS-M1-00198` | `CRS-M1-00198` | PREFIX-TARGET-HARDWARE-ID-WITH-MANUFACTURER-CODE | ARINC-665-DATA-OBJECT |
| `OBJ-MANUFACTURER-IDENTIFIER-ASSIGN-CRS-M1-00199` | `CRS-M1-00199` | ASSIGN | ARINC-665-DATA-OBJECT |
| `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ASSIGN-GENERIC-TARGET-HARDWARE-ID-CRS-M1-00200` | `CRS-M1-00200` | ASSIGN-GENERIC-TARGET-HARDWARE-ID | ARINC-665-DATA-OBJECT |
| `OBJ-REDUNDANT-CHANNEL-LOADS-DISTRIBUTE-REDUNDANT-LOADS-INTERNALLY-CRS-M1-00201` | `CRS-M1-00201` | DISTRIBUTE-REDUNDANT-LOADS-INTERNALLY | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-ENSURE-CARDINALITY-CRS-M1-00202` | `CRS-M1-00202` | ENSURE-CARDINALITY | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-COORDINATE-CRS-M1-00203` | `CRS-M1-00203` | COORDINATE | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-ASSIGN-CRS-M1-00204` | `CRS-M1-00204` | ASSIGN | ARINC-665-DATA-OBJECT |
| `OBJ-LOADABLE-SOFTWARE-PART-NUMBER-FORMAT-CRS-M1-00205` | `CRS-M1-00205` | FORMAT | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-EXCLUDE-EMBEDDED-BLANKS-CRS-M1-00206` | `CRS-M1-00206` | EXCLUDE-EMBEDDED-BLANKS | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-DO-NOT-ENFORCE-SPECIFIC-PART-NUMBER-FORMAT-CRS-M1-00207` | `CRS-M1-00207` | DO-NOT-ENFORCE-SPECIFIC-PART-NUMBER-FORMAT | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-PROCESS-NONCONFORMING-PART-NUMBER-FORMATS-CRS-M1-00208` | `CRS-M1-00208` | PROCESS-NONCONFORMING-PART-NUMBER-FORMATS | ARINC-665-DATA-OBJECT |
| `OBJ-NETWORK-INTERFACE-DESIGN-CRS-M1-00209` | `CRS-M1-00209` | DESIGN | ARINC-665-DATA-OBJECT |
| `OBJ-NETWORK-INTERFACE-FORMAT-CRS-M1-00210` | `CRS-M1-00210` | FORMAT | ARINC-665-DATA-OBJECT |
| `OBJ-ATA-PART-NUMBER-DELIMITERS-SEPARATE-DELIMITERS-FROM-LETTERS-CRS-M1-00211` | `CRS-M1-00211` | SEPARATE-DELIMITERS-FROM-LETTERS | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-ENCODE-CRS-M1-00212` | `CRS-M1-00212` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-ATA-PART-NUMBER-CHARACTER-SET-EXCLUDE-AMBIGUOUS-LETTER-O-CRS-M1-00213` | `CRS-M1-00213` | EXCLUDE-AMBIGUOUS-LETTER-O | ARINC-665-DATA-OBJECT |
| `OBJ-MMM-CODE-INTERPRET-CONFUSED-MMM-CHARACTERS-AS-ALPHABETIC-CRS-M1-00214` | `CRS-M1-00214` | INTERPRET-CONFUSED-MMM-CHARACTERS-AS-ALPHABETIC | ARINC-665-DATA-OBJECT |
| `OBJ-CHECK-CHARACTERS-COMPUTE-CRS-M1-00215` | `CRS-M1-00215` | COMPUTE | ARINC-665-DATA-OBJECT |
| `OBJ-HEADER-FILE-SOFTWARE-PART-FORMAT-CRS-M1-00216` | `CRS-M1-00216` | FORMAT | ARINC-665-DATA-OBJECT |
| `OBJ-HEADER-FILE-SOFTWARE-PART-ENCODE-CRS-M1-00217` | `CRS-M1-00217` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-HEADER-FILE-DEFINE-CRS-M1-00218` | `CRS-M1-00218` | DEFINE | ARINC-665-DATA-OBJECT |
| `OBJ-BINARY-FIELD-ENCODING-ENCODE-CRS-M1-00219` | `CRS-M1-00219` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-OPERATION-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00220` | `CRS-M1-00220` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-BINARY-FIELD-ENCODING-ENCODE-CRS-M1-00221` | `CRS-M1-00221` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-TARGET-HARDWARE-ID-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00222` | `CRS-M1-00222` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-IMPLEMENT-CRS-M1-00223` | `CRS-M1-00223` | IMPLEMENT | ARINC-665-DATA-OBJECT |
| `OBJ-NETWORK-INTERFACE-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00224` | `CRS-M1-00224` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ENSURE-UNIQUE-CRS-M1-00225` | `CRS-M1-00225` | ENSURE-UNIQUE | ARINC-665-DATA-OBJECT |
| `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ENCODE-CRS-M1-00226` | `CRS-M1-00226` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-TARGET-HARDWARE-ID-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00227` | `CRS-M1-00227` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-DATA-FILE-CONSTRAIN-CRS-M1-00228` | `CRS-M1-00228` | CONSTRAIN | ARINC-665-DATA-OBJECT |
| `OBJ-DATA-FILE-SET-ZERO-CRS-M1-00229` | `CRS-M1-00229` | SET-ZERO | ARINC-665-DATA-OBJECT |
| `OBJ-DATA-FILE-FORMAT-CRS-M1-00230` | `CRS-M1-00230` | FORMAT | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-NETWORK-INTERFACE-DEFINE-CRS-M1-00231` | `CRS-M1-00231` | DEFINE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00232` | `CRS-M1-00232` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00233` | `CRS-M1-00233` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00234` | `CRS-M1-00234` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-NETWORK-INTERFACE-ENCODE-CRS-M1-00235` | `CRS-M1-00235` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-NETWORK-INTERFACE-IMPLEMENT-CRS-M1-00236` | `CRS-M1-00236` | IMPLEMENT | ARINC-665-DATA-OBJECT |
| `OBJ-LOAD-PART-NUMBER-NETWORK-INTERFACE-ENCODE-CRS-M1-00237` | `CRS-M1-00237` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-NETWORK-INTERFACE-DEFINE-CRS-M1-00238` | `CRS-M1-00238` | DEFINE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00239` | `CRS-M1-00239` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-NETWORK-INTERFACE-VALIDATE-CRS-M1-00240` | `CRS-M1-00240` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-HEADER-FILE-VALIDATE-CRS-M1-00241` | `CRS-M1-00241` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00242` | `CRS-M1-00242` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00243` | `CRS-M1-00243` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00244` | `CRS-M1-00244` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00245` | `CRS-M1-00245` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00246` | `CRS-M1-00246` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-VALIDATE-CRS-M1-00247` | `CRS-M1-00247` | VALIDATE | ARINC-665-DATA-OBJECT |
| `OBJ-HEADER-FILE-CRC-DEFINE-CRS-M1-00248` | `CRS-M1-00248` | DEFINE | ARINC-665-DATA-OBJECT |
| `OBJ-HEADER-FILE-CRC-COMPUTE-CRS-M1-00249` | `CRS-M1-00249` | COMPUTE | ARINC-665-DATA-OBJECT |
| `OBJ-CRC-NETWORK-INTERFACE-DEFINE-CRS-M1-00250` | `CRS-M1-00250` | DEFINE | ARINC-665-DATA-OBJECT |
| `OBJ-DATA-FILE-SOFTWARE-PART-ENCODE-CRS-M1-00251` | `CRS-M1-00251` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-SOFTWARE-PART-NETWORK-INTERFACE-ENCODE-CRS-M1-00252` | `CRS-M1-00252` | ENCODE | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-MAY-USE-BATCH-FILE-FORMAT-CRS-M1-00526` | `CRS-M1-00526` | MAY-USE-BATCH-FILE-FORMAT | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-LET-BATCH-FILE-SELECT-LSPS-PER-TARGET-HW-POSITION-CRS-M1-00527` | `CRS-M1-00527` | LET-BATCH-FILE-SELECT-LSPS-PER-TARGET-HW-POSITION | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-IDENTIFY-BATCH-FILE-WITH-LUB-EXTENSION-CRS-M1-00528` | `CRS-M1-00528` | IDENTIFY-BATCH-FILE-WITH-LUB-EXTENSION | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-MATCH-REFERENCED-HEADER-FILE-NAME-CASE-CRS-M1-00529` | `CRS-M1-00529` | MATCH-REFERENCED-HEADER-FILE-NAME-CASE | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-PREFIX-BATCH-FILE-NAME-WITH-MANUFACTURER-CODE-CRS-M1-00530` | `CRS-M1-00530` | PREFIX-BATCH-FILE-NAME-WITH-MANUFACTURER-CODE | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-KEEP-BATCH-FILE-NAME-UNIQUE-PER-MANUFACTURER-CODE-CRS-M1-00531` | `CRS-M1-00531` | KEEP-BATCH-FILE-NAME-UNIQUE-PER-MANUFACTURER-CODE | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-KEEP-BATCH-FILE-PART-NUMBER-UNIQUE-AMONG-LSP-AND-BFP-CRS-M1-00532` | `CRS-M1-00532` | KEEP-BATCH-FILE-PART-NUMBER-UNIQUE-AMONG-LSP-AND-BFP | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-REFERENCE-COMPLETE-HEADER-FILE-NAME-WITHOUT-PATH-CRS-M1-00533` | `CRS-M1-00533` | REFERENCE-COMPLETE-HEADER-FILE-NAME-WITHOUT-PATH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-USE-BATCH-FILE-ONLY-TO-AUTOMATE-MULTI-LSP-SETUP-CRS-M1-00534` | `CRS-M1-00534` | USE-BATCH-FILE-ONLY-TO-AUTOMATE-MULTI-LSP-SETUP | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-DO-NOT-TRANSFER-BATCH-FILE-TO-TARGET-HARDWARE-CRS-M1-00535` | `CRS-M1-00535` | DO-NOT-TRANSFER-BATCH-FILE-TO-TARGET-HARDWARE | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-INCLUDE-BATCH-FILE-CONTENT-DEFINED-BY-TABLE-2-3-1-1-CRS-M1-00536` | `CRS-M1-00536` | INCLUDE-BATCH-FILE-CONTENT-DEFINED-BY-TABLE-2-3-1-1 | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ENCODE-BATCH-FILE-LENGTH-IN-16-BIT-WORDS-CRS-M1-00537` | `CRS-M1-00537` | ENCODE-BATCH-FILE-LENGTH-IN-16-BIT-WORDS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-MAKE-BATCH-FILE-PN-COMPLIANT-WITH-SOFTWARE-LOAD-PN-FORMAT-CRS-M1-00538` | `CRS-M1-00538` | MAKE-BATCH-FILE-PN-COMPLIANT-WITH-SOFTWARE-LOAD-PN-FORMAT | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-KEEP-BATCH-FILE-PN-DISTINCT-FROM-LSP-AND-MSP-CRS-M1-00539` | `CRS-M1-00539` | KEEP-BATCH-FILE-PN-DISTINCT-FROM-LSP-AND-MSP | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-SET-LAST-LOAD-LIST-BLOCK-POINTER-TO-ZERO-CRS-M1-00540` | `CRS-M1-00540` | SET-LAST-LOAD-LIST-BLOCK-POINTER-TO-ZERO | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-MATCH-TARGET-HW-ID-POS-TO-TARGET-HARDWARE-CRS-M1-00541` | `CRS-M1-00541` | MATCH-TARGET-HW-ID-POS-TO-TARGET-HARDWARE | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-MATCH-HEADER-FILE-NAME-TO-LISTED-LSP-CRS-M1-00542` | `CRS-M1-00542` | MATCH-HEADER-FILE-NAME-TO-LISTED-LSP | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-MATCH-LOAD-PN-TO-LSP-FOR-TARGET-HW-ID-POS-CRS-M1-00543` | `CRS-M1-00543` | MATCH-LOAD-PN-TO-LSP-FOR-TARGET-HW-ID-POS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-DEFINE-BATCH-FILE-FORMAT-VERSION-IN-16-BITS-CRS-M1-00568` | `CRS-M1-00568` | DEFINE-BATCH-FILE-FORMAT-VERSION-IN-16-BITS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-TAKE-BATCH-FILE-FORMAT-VERSION-FROM-CLAUSE-1-4-1-CRS-M1-00569` | `CRS-M1-00569` | TAKE-BATCH-FILE-FORMAT-VERSION-FROM-CLAUSE-1-4-1 | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-USE-SPARE-TO-ALIGN-FOLLOWING-POINTERS-ON-4-BYTE-BOUNDARIES-CRS-M1-00570` | `CRS-M1-00570` | USE-SPARE-TO-ALIGN-FOLLOWING-POINTERS-ON-4-BYTE-BOUNDARIES | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-POINT-TO-BATCH-FILE-PN-LENGTH-FROM-START-IN-16-BIT-WORDS-CRS-M1-00571` | `CRS-M1-00571` | POINT-TO-BATCH-FILE-PN-LENGTH-FROM-START-IN-16-BIT-WORDS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-POINT-TO-LOAD-LIST-BLOCK-COUNT-FROM-START-IN-16-BIT-WORDS-CRS-M1-00572` | `CRS-M1-00572` | POINT-TO-LOAD-LIST-BLOCK-COUNT-FROM-START-IN-16-BIT-WORDS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-MAY-GROW-FILE-FORMAT-AT-EXPANSION-POINTS-CRS-M1-00573` | `CRS-M1-00573` | MAY-GROW-FILE-FORMAT-AT-EXPANSION-POINTS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-BATCH-FILE-PN-LENGTH-CRS-M1-00574` | `CRS-M1-00574` | EXCLUDE-NUL-PAD-FROM-BATCH-FILE-PN-LENGTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ENCODE-BATCH-FILE-PN-AS-8-BIT-ASCII-CRS-M1-00575` | `CRS-M1-00575` | ENCODE-BATCH-FILE-PN-AS-8-BIT-ASCII | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ALLOCATE-BATCH-FILE-PN-EVEN-OCTET-WIDTH-CRS-M1-00576` | `CRS-M1-00576` | ALLOCATE-BATCH-FILE-PN-EVEN-OCTET-WIDTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-PAD-ODD-BATCH-FILE-PN-WITH-NUL-CRS-M1-00577` | `CRS-M1-00577` | PAD-ODD-BATCH-FILE-PN-WITH-NUL | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-COMMENT-LENGTH-CRS-M1-00578` | `CRS-M1-00578` | EXCLUDE-NUL-PAD-FROM-COMMENT-LENGTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-SET-COMMENT-LENGTH-ZERO-WHEN-NO-COMMENT-CRS-M1-00579` | `CRS-M1-00579` | SET-COMMENT-LENGTH-ZERO-WHEN-NO-COMMENT | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ENCODE-COMMENT-AS-8-BIT-ASCII-CRS-M1-00580` | `CRS-M1-00580` | ENCODE-COMMENT-AS-8-BIT-ASCII | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ALLOCATE-COMMENT-EVEN-OCTET-WIDTH-CRS-M1-00581` | `CRS-M1-00581` | ALLOCATE-COMMENT-EVEN-OCTET-WIDTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-PAD-ODD-COMMENT-WITH-NUL-CRS-M1-00582` | `CRS-M1-00582` | PAD-ODD-COMMENT-WITH-NUL | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-OMIT-COMMENT-FIELD-WHEN-COMMENT-LENGTH-ZERO-CRS-M1-00583` | `CRS-M1-00583` | OMIT-COMMENT-FIELD-WHEN-COMMENT-LENGTH-ZERO | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-COUNT-TARGET-HW-ID-LOAD-LIST-BLOCKS-IN-BATCH-FILE-CRS-M1-00584` | `CRS-M1-00584` | COUNT-TARGET-HW-ID-LOAD-LIST-BLOCKS-IN-BATCH-FILE | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-POINT-TO-NEXT-LOAD-LIST-BLOCK-IN-RELATIVE-16-BIT-WORDS-CRS-M1-00585` | `CRS-M1-00585` | POINT-TO-NEXT-LOAD-LIST-BLOCK-IN-RELATIVE-16-BIT-WORDS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-TARGET-HW-ID-POS-LENGTH-CRS-M1-00586` | `CRS-M1-00586` | EXCLUDE-NUL-PAD-FROM-TARGET-HW-ID-POS-LENGTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ENCODE-TARGET-HW-ID-POS-AS-8-BIT-ASCII-CRS-M1-00587` | `CRS-M1-00587` | ENCODE-TARGET-HW-ID-POS-AS-8-BIT-ASCII | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ALLOCATE-TARGET-HW-ID-POS-EVEN-OCTET-WIDTH-CRS-M1-00588` | `CRS-M1-00588` | ALLOCATE-TARGET-HW-ID-POS-EVEN-OCTET-WIDTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-PAD-ODD-TARGET-HW-ID-POS-WITH-NUL-CRS-M1-00589` | `CRS-M1-00589` | PAD-ODD-TARGET-HW-ID-POS-WITH-NUL | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-KEEP-TARGET-HW-ID-POS-CONSISTENT-WITH-LISTED-LSP-HEADERS-CRS-M1-00590` | `CRS-M1-00590` | KEEP-TARGET-HW-ID-POS-CONSISTENT-WITH-LISTED-LSP-HEADERS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-COUNT-LOADS-IN-THE-TARGET-HW-ID-LOAD-LIST-BLOCK-CRS-M1-00591` | `CRS-M1-00591` | COUNT-LOADS-IN-THE-TARGET-HW-ID-LOAD-LIST-BLOCK | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-HEADER-FILE-NAME-LENGTH-CRS-M1-00592` | `CRS-M1-00592` | EXCLUDE-NUL-PAD-FROM-HEADER-FILE-NAME-LENGTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ENCODE-HEADER-FILE-NAME-AS-8-BIT-ASCII-CRS-M1-00593` | `CRS-M1-00593` | ENCODE-HEADER-FILE-NAME-AS-8-BIT-ASCII | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ALLOCATE-HEADER-FILE-NAME-EVEN-OCTET-WIDTH-CRS-M1-00594` | `CRS-M1-00594` | ALLOCATE-HEADER-FILE-NAME-EVEN-OCTET-WIDTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-PAD-ODD-HEADER-FILE-NAME-WITH-NUL-CRS-M1-00595` | `CRS-M1-00595` | PAD-ODD-HEADER-FILE-NAME-WITH-NUL | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-USE-HEADER-FILE-NAME-WITHOUT-PATH-CRS-M1-00596` | `CRS-M1-00596` | USE-HEADER-FILE-NAME-WITHOUT-PATH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-KEEP-HEADER-FILE-NAME-FREE-OF-BACKSLASH-CRS-M1-00597` | `CRS-M1-00597` | KEEP-HEADER-FILE-NAME-FREE-OF-BACKSLASH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-INCLUDE-HEADER-FILE-NAME-EXTENSIONS-AND-DELIMITERS-CRS-M1-00598` | `CRS-M1-00598` | INCLUDE-HEADER-FILE-NAME-EXTENSIONS-AND-DELIMITERS | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-DEFINE-LOAD-PN-LENGTH-AS-CHARACTER-COUNT-CRS-M1-00599` | `CRS-M1-00599` | DEFINE-LOAD-PN-LENGTH-AS-CHARACTER-COUNT | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-LOAD-PN-LENGTH-CRS-M1-00600` | `CRS-M1-00600` | EXCLUDE-NUL-PAD-FROM-LOAD-PN-LENGTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ENCODE-LOAD-PN-AS-8-BIT-ASCII-CRS-M1-00601` | `CRS-M1-00601` | ENCODE-LOAD-PN-AS-8-BIT-ASCII | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-ALLOCATE-LOAD-PN-EVEN-OCTET-WIDTH-CRS-M1-00602` | `CRS-M1-00602` | ALLOCATE-LOAD-PN-EVEN-OCTET-WIDTH | ARINC-665-DATA-OBJECT |
| `OBJ-BATCH-FILE-PAD-ODD-LOAD-PN-WITH-NUL-CRS-M1-00603` | `CRS-M1-00603` | PAD-ODD-LOAD-PN-WITH-NUL | ARINC-665-DATA-OBJECT |
| `OBJ-SUPPORTING-GIVE-664P3-PRECEDENCE-OVER-CONFLICTING-RFC-OPTIONS-CRS-M1-00604` | `CRS-M1-00604` | GIVE-664P3-PRECEDENCE-OVER-CONFLICTING-RFC-OPTIONS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-GENERATE-AND-CHECK-UDP-CHECKSUM-CRS-M1-00605` | `CRS-M1-00605` | GENERATE-AND-CHECK-UDP-CHECKSUM | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-IMPLEMENT-IPV4-IN-ACCORDANCE-WITH-P3-FIGURE-3-4-1-1-CRS-M1-00606` | `CRS-M1-00606` | IMPLEMENT-IPV4-IN-ACCORDANCE-WITH-P3-FIGURE-3-4-1-1 | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-FILTER-AND-POLICE-FRAMES-FOR-INTEGRITY-LENGTH-BUDGET-AND-DESTINATION-CRS-M1-00608` | `CRS-M1-00608` | FILTER-AND-POLICE-FRAMES-FOR-INTEGRITY-LENGTH-BUDGET-AND-DESTINATION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-AFDX-NOT-APPLICABLE-PROFILE-ITEMS-AS-MUST-NOT-CRS-M1-00609` | `CRS-M1-00609` | TREAT-AFDX-NOT-APPLICABLE-PROFILE-ITEMS-AS-MUST-NOT | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-UDP-LENGTH-TO-HEADER-PLUS-DATA-OCTETS-CRS-M1-00610` | `CRS-M1-00610` | SET-UDP-LENGTH-TO-HEADER-PLUS-DATA-OCTETS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-COMPUTE-UDP-CHECKSUM-OVER-PSEUDO-HEADER-HEADER-AND-DATA-CRS-M1-00611` | `CRS-M1-00611` | COMPUTE-UDP-CHECKSUM-OVER-PSEUDO-HEADER-HEADER-AND-DATA | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-UDP-LENGTH-AT-LEAST-EIGHT-OCTETS-CRS-M1-00628` | `CRS-M1-00628` | KEEP-UDP-LENGTH-AT-LEAST-EIGHT-OCTETS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-IMPLEMENT-IPV4-FRAGMENTATION-AND-REASSEMBLY-CRS-M1-00613` | `CRS-M1-00613` | IMPLEMENT-IPV4-FRAGMENTATION-AND-REASSEMBLY | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-SILENTLY-DISCARD-NON-IPV4-VERSION-CRS-M1-00614` | `CRS-M1-00614` | SILENTLY-DISCARD-NON-IPV4-VERSION | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-VERIFY-IP-HEADER-CHECKSUM-AND-SILENTLY-DISCARD-BAD-CRS-M1-00629` | `CRS-M1-00629` | VERIFY-IP-HEADER-CHECKSUM-AND-SILENTLY-DISCARD-BAD | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-SUPPORT-IPV4-REASSEMBLY-CRS-M1-00630` | `CRS-M1-00630` | SUPPORT-IPV4-REASSEMBLY | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-GENERATE-AND-VALIDATE-UDP-CHECKSUMS-CRS-M1-00615` | `CRS-M1-00615` | GENERATE-AND-VALIDATE-UDP-CHECKSUMS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-SILENTLY-DISCARD-UDP-DATAGRAM-WITH-INVALID-CHECKSUM-CRS-M1-00631` | `CRS-M1-00631` | SILENTLY-DISCARD-UDP-DATAGRAM-WITH-INVALID-CHECKSUM | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-USE-FIVE-TFTP-PACKET-TYPES-IDENTIFIED-BY-OPCODE-CRS-M1-00617` | `CRS-M1-00617` | USE-FIVE-TFTP-PACKET-TYPES-IDENTIFIED-BY-OPCODE | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ASSIGN-TID-ON-RRQ-OR-WRQ-WITHOUT-MAIL-MODE-CRS-M1-00618` | `CRS-M1-00618` | ASSIGN-TID-ON-RRQ-OR-WRQ-WITHOUT-MAIL-MODE | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-PLACE-OPCODE-IN-TFTP-HEADER-CRS-M1-00619` | `CRS-M1-00619` | PLACE-OPCODE-IN-TFTP-HEADER | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-RRQ-WRQ-AS-OPCODE-FILENAME-AND-MODE-CRS-M1-00632` | `CRS-M1-00632` | ENCODE-RRQ-WRQ-AS-OPCODE-FILENAME-AND-MODE | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-TERMINATE-TFTP-FILENAME-WITH-NUL-CRS-M1-00633` | `CRS-M1-00633` | TERMINATE-TFTP-FILENAME-WITH-NUL | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-DATA-PACKET-WITH-BLOCK-NUMBER-AND-DATA-CRS-M1-00634` | `CRS-M1-00634` | ENCODE-DATA-PACKET-WITH-BLOCK-NUMBER-AND-DATA | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-LIMIT-TFTP-DATA-FIELD-TO-ZERO-THROUGH-512-BYTES-CRS-M1-00635` | `CRS-M1-00635` | LIMIT-TFTP-DATA-FIELD-TO-ZERO-THROUGH-512-BYTES | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-ACK-PACKET-WITH-OPCODE-4-AND-BLOCK-NUMBER-CRS-M1-00636` | `CRS-M1-00636` | ENCODE-ACK-PACKET-WITH-OPCODE-4-AND-BLOCK-NUMBER | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-ERROR-PACKET-AS-OPCODE-ERROR-CODE-AND-MESSAGE-CRS-M1-00637` | `CRS-M1-00637` | ENCODE-ERROR-PACKET-AS-OPCODE-ERROR-CODE-AND-MESSAGE | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-TERMINATE-ON-DATA-PACKET-OF-0-TO-511-BYTES-CRS-M1-00620` | `CRS-M1-00620` | TERMINATE-ON-DATA-PACKET-OF-0-TO-511-BYTES | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-SEND-ERROR-PACKET-OPCODE-5-CRS-M1-00621` | `CRS-M1-00621` | SEND-ERROR-PACKET-OPCODE-5 | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ACKNOWLEDGE-OPTION-NEGOTIATION-WITH-OACK-CRS-M1-00622` | `CRS-M1-00622` | ACKNOWLEDGE-OPTION-NEGOTIATION-WITH-OACK | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-TERMINATE-TRANSFER-WITH-ERROR-CODE-8-CRS-M1-00623` | `CRS-M1-00623` | TERMINATE-TRANSFER-WITH-ERROR-CODE-8 | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-APPEND-OPTIONS-TO-RRQ-OR-WRQ-CRS-M1-00624` | `CRS-M1-00624` | APPEND-OPTIONS-TO-RRQ-OR-WRQ | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-BLKSIZE-AS-ASCII-OCTETS-FROM-8-THROUGH-65464-CRS-M1-00625` | `CRS-M1-00625` | ENCODE-BLKSIZE-AS-ASCII-OCTETS-FROM-8-THROUGH-65464 | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-BLKSIZE-VALUE-IN-ASCII-CRS-M1-00638` | `CRS-M1-00638` | ENCODE-BLKSIZE-VALUE-IN-ASCII | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-NEGOTIATE-BLKSIZE-LESS-OR-EQUAL-TO-CLIENT-VALUE-CRS-M1-00639` | `CRS-M1-00639` | NEGOTIATE-BLKSIZE-LESS-OR-EQUAL-TO-CLIENT-VALUE | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-USE-OACK-BLKSIZE-OR-TERMINATE-WITH-ERROR-8-CRS-M1-00640` | `CRS-M1-00640` | USE-OACK-BLKSIZE-OR-TERMINATE-WITH-ERROR-8 | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-TIMEOUT-AS-ASCII-SECONDS-FROM-1-THROUGH-255-CRS-M1-00626` | `CRS-M1-00626` | ENCODE-TIMEOUT-AS-ASCII-SECONDS-FROM-1-THROUGH-255 | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ECHO-CLIENT-TIMEOUT-VALUE-IN-OACK-CRS-M1-00641` | `CRS-M1-00641` | ECHO-CLIENT-TIMEOUT-VALUE-IN-OACK | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-REQUEST-TSIZE-ZERO-ON-RRQ-AND-RETURN-SIZE-IN-OACK-CRS-M1-00627` | `CRS-M1-00627` | REQUEST-TSIZE-ZERO-ON-RRQ-AND-RETURN-SIZE-IN-OACK | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-SPECIFY-TSIZE-ON-WRQ-AND-ECHO-IN-OACK-CRS-M1-00642` | `CRS-M1-00642` | SPECIFY-TSIZE-ON-WRQ-AND-ECHO-IN-OACK | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-MAY-ABORT-RRQ-WITH-ERROR-CODE-3-CRS-M1-00643` | `CRS-M1-00643` | MAY-ABORT-RRQ-WITH-ERROR-CODE-3 | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-MAY-ABORT-WRQ-WITH-ERROR-CODE-3-CRS-M1-00644` | `CRS-M1-00644` | MAY-ABORT-WRQ-WITH-ERROR-CODE-3 | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-TERMINATE-ON-DATA-SHORTER-THAN-NEGOTIATED-BLKSIZE-CRS-M1-00645` | `CRS-M1-00645` | TERMINATE-ON-DATA-SHORTER-THAN-NEGOTIATED-BLKSIZE | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-SEND-ZERO-LENGTH-FINAL-DATA-WHEN-FILE-IS-INTEGRAL-MULTIPLE-OF-BLKSIZE-CRS-M1-00646` | `CRS-M1-00646` | SEND-ZERO-LENGTH-FINAL-DATA-WHEN-FILE-IS-INTEGRAL-MULTIPLE-OF-BLKSIZE | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-IGNORE-UNACKNOWLEDGED-OPTION-AND-KEEP-DEFAULT-PARAMETERS-CRS-M1-00647` | `CRS-M1-00647` | IGNORE-UNACKNOWLEDGED-OPTION-AND-KEEP-DEFAULT-PARAMETERS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-VERSION-AS-4-BITS-CRS-M1-00648` | `CRS-M1-00648` | ENCODE-VERSION-AS-4-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-IHL-AS-4-BITS-CRS-M1-00649` | `CRS-M1-00649` | ENCODE-IHL-AS-4-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-TOS-AS-8-BITS-CRS-M1-00650` | `CRS-M1-00650` | ENCODE-TOS-AS-8-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-TOTAL-LENGTH-AS-16-BITS-CRS-M1-00651` | `CRS-M1-00651` | ENCODE-TOTAL-LENGTH-AS-16-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-IDENTIFICATION-AS-16-BITS-CRS-M1-00652` | `CRS-M1-00652` | ENCODE-IDENTIFICATION-AS-16-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-FLAGS-AS-3-BITS-CRS-M1-00653` | `CRS-M1-00653` | ENCODE-FLAGS-AS-3-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-FRAGMENT-OFFSET-AS-13-BITS-CRS-M1-00654` | `CRS-M1-00654` | ENCODE-FRAGMENT-OFFSET-AS-13-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-TTL-AS-8-BITS-CRS-M1-00655` | `CRS-M1-00655` | ENCODE-TTL-AS-8-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-PROTOCOL-AS-8-BITS-CRS-M1-00656` | `CRS-M1-00656` | ENCODE-PROTOCOL-AS-8-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-HEADER-CHECKSUM-AS-16-BITS-CRS-M1-00657` | `CRS-M1-00657` | ENCODE-HEADER-CHECKSUM-AS-16-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-SOURCE-ADDRESS-AS-32-BITS-CRS-M1-00658` | `CRS-M1-00658` | ENCODE-SOURCE-ADDRESS-AS-32-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-DESTINATION-ADDRESS-AS-32-BITS-CRS-M1-00659` | `CRS-M1-00659` | ENCODE-DESTINATION-ADDRESS-AS-32-BITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-DO-NOT-SUPPORT-TFTP-MAIL-TRANSFER-MODE-CRS-M1-00660` | `CRS-M1-00660` | DO-NOT-SUPPORT-TFTP-MAIL-TRANSFER-MODE | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-COUNT-UDP-LENGTH-INCLUDING-EIGHT-OCTET-HEADER-CRS-M1-00661` | `CRS-M1-00661` | COUNT-UDP-LENGTH-INCLUDING-EIGHT-OCTET-HEADER | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-NEVER-RESEND-CURRENT-DATA-ON-DUPLICATE-ACK-CRS-M1-00662` | `CRS-M1-00662` | NEVER-RESEND-CURRENT-DATA-ON-DUPLICATE-ACK | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-USE-ADAPTIVE-TFTP-RETRANSMISSION-TIMEOUT-CRS-M1-00663` | `CRS-M1-00663` | USE-ADAPTIVE-TFTP-RETRANSMISSION-TIMEOUT | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-PROVIDE-CONFIGURABLE-TFTP-PATHNAME-ACCESS-CONTROL-CRS-M1-00664` | `CRS-M1-00664` | PROVIDE-CONFIGURABLE-TFTP-PATHNAME-ACCESS-CONTROL | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-SILENTLY-IGNORE-BROADCAST-TFTP-REQUEST-CRS-M1-00665` | `CRS-M1-00665` | SILENTLY-IGNORE-BROADCAST-TFTP-REQUEST | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ALLOW-ONLY-ONE-SOURCE-END-SYSTEM-PER-VL-CRS-M1-00666` | `CRS-M1-00666` | ALLOW-ONLY-ONE-SOURCE-END-SYSTEM-PER-VL | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-VL-AS-UNIDIRECTIONAL-ONE-TO-MANY-CONNECTION-CRS-M1-00667` | `CRS-M1-00667` | TREAT-VL-AS-UNIDIRECTIONAL-ONE-TO-MANY-CONNECTION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-BAG-AS-MINIMUM-INTERVAL-BETWEEN-CONSECUTIVE-VL-FRAMES-CRS-M1-00668` | `CRS-M1-00668` | TREAT-BAG-AS-MINIMUM-INTERVAL-BETWEEN-CONSECUTIVE-VL-FRAMES | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-BOUND-VL-FRAME-ARRIVAL-BY-MAXIMUM-ADMISSIBLE-JITTER-CRS-M1-00669` | `CRS-M1-00669` | BOUND-VL-FRAME-ARRIVAL-BY-MAXIMUM-ADMISSIBLE-JITTER | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-CHARACTERISE-VL-BANDWIDTH-BY-BAG-AND-LMAX-CRS-M1-00670` | `CRS-M1-00670` | CHARACTERISE-VL-BANDWIDTH-BY-BAG-AND-LMAX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ACCOMMODATE-VL-FRAMES-UP-TO-1518-BYTES-CRS-M1-00671` | `CRS-M1-00671` | ACCOMMODATE-VL-FRAMES-UP-TO-1518-BYTES | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-HANDLE-BAG-VALUES-FROM-1-MS-TO-128-MS-CRS-M1-00672` | `CRS-M1-00672` | HANDLE-BAG-VALUES-FROM-1-MS-TO-128-MS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RESTRICT-BAG-TO-POWERS-OF-TWO-MILLISECONDS-CRS-M1-00673` | `CRS-M1-00673` | RESTRICT-BAG-TO-POWERS-OF-TWO-MILLISECONDS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-IDENTIFY-VL-ONLY-BY-MAC-DESTINATION-ADDRESS-CRS-M1-00675` | `CRS-M1-00675` | IDENTIFY-VL-ONLY-BY-MAC-DESTINATION-ADDRESS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-MEASURE-IHL-IN-32-BIT-WORDS-CRS-M1-00676` | `CRS-M1-00676` | MEASURE-IHL-IN-32-BIT-WORDS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-IHL-AT-LEAST-5-CRS-M1-00677` | `CRS-M1-00677` | KEEP-IHL-AT-LEAST-5 | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-MEASURE-IPV4-TOTAL-LENGTH-IN-OCTETS-INCLUDING-HEADER-AND-DATA-CRS-M1-00678` | `CRS-M1-00678` | MEASURE-IPV4-TOTAL-LENGTH-IN-OCTETS-INCLUDING-HEADER-AND-DATA | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-MEASURE-FRAGMENT-OFFSET-IN-8-OCTET-UNITS-CRS-M1-00679` | `CRS-M1-00679` | MEASURE-FRAGMENT-OFFSET-IN-8-OCTET-UNITS | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-ALLOW-IPV4-OPTIONS-TO-BE-PRESENT-OR-ABSENT-CRS-M1-00680` | `CRS-M1-00680` | ALLOW-IPV4-OPTIONS-TO-BE-PRESENT-OR-ABSENT | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-PAD-IPV4-HEADER-TO-32-BIT-BOUNDARY-CRS-M1-00681` | `CRS-M1-00681` | PAD-IPV4-HEADER-TO-32-BIT-BOUNDARY | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-PROVIDE-SECURE-RELIABLE-PARTITION-DATA-EXCHANGE-CRS-M1-00607` | `CRS-M1-00607` | PROVIDE-SECURE-RELIABLE-PARTITION-DATA-EXCHANGE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-IMPLEMENT-IPV4-ADDRESSING-AND-FRAGMENTATION-CRS-M1-00612` | `CRS-M1-00612` | IMPLEMENT-IPV4-ADDRESSING-AND-FRAGMENTATION | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-APPLY-RFC-1123-TFTP-HOST-NOTES-WITHOUT-ADOPTING-MAIL-NETASCII-OR-BROADCAST-RRQ-CRS-M1-00616` | `CRS-M1-00616` | APPLY-RFC-1123-TFTP-HOST-NOTES-WITHOUT-ADOPTING-MAIL-NETASCII-OR-BROADCAST-RRQ | RFC-PUBLIC-TEXT-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-TX-TECHNOLOGICAL-LATENCY-BELOW-150US-PLUS-FRAME-DELAY-CRS-M1-00682` | `CRS-M1-00682` | KEEP-TX-TECHNOLOGICAL-LATENCY-BELOW-150US-PLUS-FRAME-DELAY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-RX-TECHNOLOGICAL-LATENCY-BELOW-150-MICROSECONDS-CRS-M1-00683` | `CRS-M1-00683` | KEEP-RX-TECHNOLOGICAL-LATENCY-BELOW-150-MICROSECONDS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-BOUND-MAX-JITTER-BY-40US-PLUS-VL-LOAD-TERM-CRS-M1-00684` | `CRS-M1-00684` | BOUND-MAX-JITTER-BY-40US-PLUS-VL-LOAD-TERM | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-BOUND-MAX-JITTER-BY-500-MICROSECONDS-EQUATION-CRS-M1-00685` | `CRS-M1-00685` | BOUND-MAX-JITTER-BY-500-MICROSECONDS-EQUATION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-MAC-SOURCE-AS-INDIVIDUAL-AND-LOCALLY-ADMINISTERED-CRS-M1-00686` | `CRS-M1-00686` | ENCODE-MAC-SOURCE-AS-INDIVIDUAL-AND-LOCALLY-ADMINISTERED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-MAC-SOURCE-CONSTANT-FIELD-TO-000000100000000000000000-CRS-M1-00687` | `CRS-M1-00687` | SET-MAC-SOURCE-CONSTANT-FIELD-TO-000000100000000000000000 | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-MAC-SOURCE-INDIVIDUAL-ADDRESS-BIT-TO-ZERO-CRS-M1-00688` | `CRS-M1-00688` | SET-MAC-SOURCE-INDIVIDUAL-ADDRESS-BIT-TO-ZERO | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-MAC-SOURCE-LOCALLY-ADMINISTERED-BIT-TO-ONE-CRS-M1-00689` | `CRS-M1-00689` | SET-MAC-SOURCE-LOCALLY-ADMINISTERED-BIT-TO-ONE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-MAC-SOURCE-USER-DEFINED-ID-AS-16-BITS-CRS-M1-00690` | `CRS-M1-00690` | ENCODE-MAC-SOURCE-USER-DEFINED-ID-AS-16-BITS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-USER-DEFINED-ID-FOR-UNIQUE-MEANINGFUL-HOST-IDENTITY-CRS-M1-00691` | `CRS-M1-00691` | USE-USER-DEFINED-ID-FOR-UNIQUE-MEANINGFUL-HOST-IDENTITY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-INTERFACE-ID-TO-IDENTIFY-REDUNDANT-AFDX-NETWORK-CRS-M1-00692` | `CRS-M1-00692` | USE-INTERFACE-ID-TO-IDENTIFY-REDUNDANT-AFDX-NETWORK | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-INTERFACE-ID-001-AS-NETWORK-A-CRS-M1-00693` | `CRS-M1-00693` | ENCODE-INTERFACE-ID-001-AS-NETWORK-A | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ENCODE-INTERFACE-ID-010-AS-NETWORK-B-CRS-M1-00694` | `CRS-M1-00694` | ENCODE-INTERFACE-ID-010-AS-NETWORK-B | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-VL-JITTER-AT-OR-BELOW-500-MICROSECONDS-CRS-M1-00674` | `CRS-M1-00674` | KEEP-VL-JITTER-AT-OR-BELOW-500-MICROSECONDS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-PROVIDE-ADN-ADDRESS-DETERMINATION-GUIDANCE-CRS-M1-00695` | `CRS-M1-00695` | PROVIDE-ADN-ADDRESS-DETERMINATION-GUIDANCE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-KNOW-DESTINATION-ADDRESSES-AT-CONFIGURATION-TIME-CRS-M1-00696` | `CRS-M1-00696` | KNOW-DESTINATION-ADDRESSES-AT-CONFIGURATION-TIME | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-DEFINE-ADN-ADDRESSING-PLAN-AND-RULES-CRS-M1-00697` | `CRS-M1-00697` | DEFINE-ADN-ADDRESSING-PLAN-AND-RULES | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-IANA-WELL-KNOWN-UDP-PORTS-FOR-STANDARD-SERVICES-INCLUDING-TFTP-CRS-M1-00698` | `CRS-M1-00698` | USE-IANA-WELL-KNOWN-UDP-PORTS-FOR-STANDARD-SERVICES-INCLUDING-TFTP | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ACCESS-PRIVATE-AERO-APPS-VIA-INTEGRATOR-OR-664P4-UDP-PORTS-CRS-M1-00699` | `CRS-M1-00699` | ACCESS-PRIVATE-AERO-APPS-VIA-INTEGRATOR-OR-664P4-UDP-PORTS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-DO-NOT-REASSIGN-WELL-KNOWN-COTS-PORTS-0-1023-CRS-M1-00700` | `CRS-M1-00700` | DO-NOT-REASSIGN-WELL-KNOWN-COTS-PORTS-0-1023 | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-DO-NOT-ROUTE-PRIVATE-ADDRESSES-OUTSIDE-THE-NETWORK-CRS-M1-00701` | `CRS-M1-00701` | DO-NOT-ROUTE-PRIVATE-ADDRESSES-OUTSIDE-THE-NETWORK | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-PROFILED-AERO-NETWORK-AS-IETF-PRIVATE-APPLICATION-CRS-M1-00702` | `CRS-M1-00702` | TREAT-PROFILED-AERO-NETWORK-AS-IETF-PRIVATE-APPLICATION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-PRIVATE-NETWORK-ID-FOR-PROFILED-NETWORKS-CRS-M1-00703` | `CRS-M1-00703` | USE-PRIVATE-NETWORK-ID-FOR-PROFILED-NETWORKS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ASSIGN-MAC-UNICAST-ADDRESSES-AT-CONFIGURATION-TIME-CRS-M1-00704` | `CRS-M1-00704` | ASSIGN-MAC-UNICAST-ADDRESSES-AT-CONFIGURATION-TIME | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-MAC-ADDRESSES-UNIQUE-UNDER-INTEGRATOR-SCHEME-CRS-M1-00705` | `CRS-M1-00705` | KEEP-MAC-ADDRESSES-UNIQUE-UNDER-INTEGRATOR-SCHEME | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-MAC-UL-BIT-WHEN-INTEGRATOR-ASSIGNS-ADDRESSES-CRS-M1-00706` | `CRS-M1-00706` | SET-MAC-UL-BIT-WHEN-INTEGRATOR-ASSIGNS-ADDRESSES | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-ALL-NETWORK-ADDRESSES-UNIQUE-CRS-M1-00707` | `CRS-M1-00707` | KEEP-ALL-NETWORK-ADDRESSES-UNIQUE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RESERVE-UDP-TCP-PORT-59-FOR-615A-DATA-LOADER-TFTP-CRS-M1-00708` | `CRS-M1-00708` | RESERVE-UDP-TCP-PORT-59-FOR-615A-DATA-LOADER-TFTP | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ASSIGN-UDP-PORT-24922-TO-FIND-PROTOCOL-CLIENT-CRS-M1-00709` | `CRS-M1-00709` | ASSIGN-UDP-PORT-24922-TO-FIND-PROTOCOL-CLIENT | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ALLOCATE-TABLE-2-1-ADDRESSES-FROM-RFC1918-PRIVATE-RANGES-CRS-M1-00710` | `CRS-M1-00710` | ALLOCATE-TABLE-2-1-ADDRESSES-FROM-RFC1918-PRIVATE-RANGES | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-MEASURE-TX-TECHNOLOGICAL-LATENCY-BETWEEN-PARTITION-DATA-AND-PHYSICAL-MEDIA-CRS-M1-00711` | `CRS-M1-00711` | MEASURE-TX-TECHNOLOGICAL-LATENCY-BETWEEN-PARTITION-DATA-AND-PHYSICAL-MEDIA | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-START-TX-TECHNOLOGICAL-LATENCY-WHEN-LAST-PARTITION-BIT-IS-AVAILABLE-CRS-M1-00712` | `CRS-M1-00712` | START-TX-TECHNOLOGICAL-LATENCY-WHEN-LAST-PARTITION-BIT-IS-AVAILABLE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-END-TX-TECHNOLOGICAL-LATENCY-WHEN-LAST-FRAME-BIT-IS-ON-MEDIA-CRS-M1-00713` | `CRS-M1-00713` | END-TX-TECHNOLOGICAL-LATENCY-WHEN-LAST-FRAME-BIT-IS-ON-MEDIA | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-MEASURE-TX-TECHNOLOGICAL-LATENCY-WITH-EMPTY-BUFFERS-NO-CONTENTION-AND-NO-IP-FRAGMENTATION-CRS-M1-00714` | `CRS-M1-00714` | MEASURE-TX-TECHNOLOGICAL-LATENCY-WITH-EMPTY-BUFFERS-NO-CONTENTION-AND-NO-IP-FRAGMENTATION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-DISTINGUISH-TECHNOLOGICAL-LATENCY-FROM-CONFIGURATION-LOAD-LATENCY-CRS-M1-00715` | `CRS-M1-00715` | DISTINGUISH-TECHNOLOGICAL-LATENCY-FROM-CONFIGURATION-LOAD-LATENCY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-DEFINE-TECHNOLOGICAL-LATENCY-AS-ACCEPT-PROCESS-AND-BEGIN-TX-WITH-NO-OTHER-TASK-CRS-M1-00716` | `CRS-M1-00716` | DEFINE-TECHNOLOGICAL-LATENCY-AS-ACCEPT-PROCESS-AND-BEGIN-TX-WITH-NO-OTHER-TASK | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ADD-FRAME-DELAY-FOR-PHYSICAL-LAYER-DELIVERY-CRS-M1-00717` | `CRS-M1-00717` | ADD-FRAME-DELAY-FOR-PHYSICAL-LAYER-DELIVERY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-START-RX-TECHNOLOGICAL-LATENCY-WHEN-LAST-FRAME-BIT-IS-RECEIVED-CRS-M1-00718` | `CRS-M1-00718` | START-RX-TECHNOLOGICAL-LATENCY-WHEN-LAST-FRAME-BIT-IS-RECEIVED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-END-RX-TECHNOLOGICAL-LATENCY-WHEN-LAST-DATA-BIT-IS-AVAILABLE-TO-PARTITION-CRS-M1-00719` | `CRS-M1-00719` | END-RX-TECHNOLOGICAL-LATENCY-WHEN-LAST-DATA-BIT-IS-AVAILABLE-TO-PARTITION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-MEASURE-RX-TECHNOLOGICAL-LATENCY-WITH-EMPTY-BUFFERS-AND-NO-CONTENTION-CRS-M1-00720` | `CRS-M1-00720` | MEASURE-RX-TECHNOLOGICAL-LATENCY-WITH-EMPTY-BUFFERS-AND-NO-CONTENTION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SATISFY-BOTH-MAX-JITTER-EQUATIONS-SIMULTANEOUSLY-CRS-M1-00721` | `CRS-M1-00721` | SATISFY-BOTH-MAX-JITTER-EQUATIONS-SIMULTANEOUSLY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-MAX-JITTER-AS-MICROSECONDS-NBW-AS-BITS-PER-SECOND-AND-LMAX-AS-OCTETS-CRS-M1-00722` | `CRS-M1-00722` | TREAT-MAX-JITTER-AS-MICROSECONDS-NBW-AS-BITS-PER-SECOND-AND-LMAX-AS-OCTETS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-COMPOSE-MAC-SOURCE-AS-24-PLUS-16-PLUS-3-PLUS-5-BIT-FIELDS-CRS-M1-00723` | `CRS-M1-00723` | COMPOSE-MAC-SOURCE-AS-24-PLUS-16-PLUS-3-PLUS-5-BIT-FIELDS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-MAC-SOURCE-CONSTANT-TAIL-TO-00000-CRS-M1-00724` | `CRS-M1-00724` | SET-MAC-SOURCE-CONSTANT-TAIL-TO-00000 | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-MAC-SOURCE-CONSTRUCTION-ALGORITHM-AS-NOT-UNIQUELY-RECOMMENDED-CRS-M1-00725` | `CRS-M1-00725` | TREAT-MAC-SOURCE-CONSTRUCTION-ALGORITHM-AS-NOT-UNIQUELY-RECOMMENDED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-INTERFACE-ID-000-AS-NOT-USED-CRS-M1-00726` | `CRS-M1-00726` | RECORD-INTERFACE-ID-000-AS-NOT-USED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-INTERFACE-ID-011-AS-NOT-USED-CRS-M1-00727` | `CRS-M1-00727` | RECORD-INTERFACE-ID-011-AS-NOT-USED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-INTERFACE-ID-100-AS-NOT-USED-CRS-M1-00728` | `CRS-M1-00728` | RECORD-INTERFACE-ID-100-AS-NOT-USED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-INTERFACE-ID-101-AS-NOT-USED-CRS-M1-00729` | `CRS-M1-00729` | RECORD-INTERFACE-ID-101-AS-NOT-USED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-INTERFACE-ID-110-AS-SOURCE-NOR-USED-CRS-M1-00730` | `CRS-M1-00730` | RECORD-INTERFACE-ID-110-AS-SOURCE-NOR-USED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-INTERFACE-ID-111-AS-NOT-USED-CRS-M1-00731` | `CRS-M1-00731` | RECORD-INTERFACE-ID-111-AS-NOT-USED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-P3-RFC-OPTION-RESTRICTION-PHILOSOPHY-CRS-M1-00732` | `CRS-M1-00732` | RECORD-P3-RFC-OPTION-RESTRICTION-PHILOSOPHY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-P3-CONTENTS-LIMITED-TO-RFC-DELTAS-CRS-M1-00733` | `CRS-M1-00733` | RECORD-P3-CONTENTS-LIMITED-TO-RFC-DELTAS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-COMPOSE-AFDX-SWITCH-FROM-FIVE-FUNCTIONAL-BLOCKS-CRS-M1-00734` | `CRS-M1-00734` | COMPOSE-AFDX-SWITCH-FROM-FIVE-FUNCTIONAL-BLOCKS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-CONTROL-AFDX-SWITCH-FUNCTIONS-WITH-STATIC-CONFIGURATION-TABLES-CRS-M1-00735` | `CRS-M1-00735` | CONTROL-AFDX-SWITCH-FUNCTIONS-WITH-STATIC-CONFIGURATION-TABLES | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-SWITCH-END-SYSTEM-TO-COMPLY-WITH-SECTION-3-EXCEPT-REDUNDANCY-CRS-M1-00736` | `CRS-M1-00736` | REQUIRE-SWITCH-END-SYSTEM-TO-COMPLY-WITH-SECTION-3-EXCEPT-REDUNDANCY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-SWITCH-END-SYSTEM-UNICAST-MAC-AS-SOURCE-ADDRESS-CRS-M1-00737` | `CRS-M1-00737` | USE-SWITCH-END-SYSTEM-UNICAST-MAC-AS-SOURCE-ADDRESS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-615A-SESSION-ACROSS-OPS-TO-DL-TRANSITION-CRS-M1-00738` | `CRS-M1-00738` | KEEP-615A-SESSION-ACROSS-OPS-TO-DL-TRANSITION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-615A-AND-665-TO-UPLOAD-SWITCH-SOFTWARE-AND-CONFIGURATION-CRS-M1-00739` | `CRS-M1-00739` | USE-615A-AND-665-TO-UPLOAD-SWITCH-SOFTWARE-AND-CONFIGURATION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-AFDX-SWITCH-PHYSICAL-LAYER-TO-COMPLY-WITH-664P2-CRS-M1-00740` | `CRS-M1-00740` | REQUIRE-AFDX-SWITCH-PHYSICAL-LAYER-TO-COMPLY-WITH-664P2 | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-AS-NOT-USED-ON-AFDX-CRS-M1-00741` | `CRS-M1-00741` | TREAT-UDP-IP-OPTIONS-AS-NOT-USED-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-UDP-CHECKSUM-GENERATE-AND-CHECK-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00742` | `CRS-M1-00742` | TREAT-UDP-CHECKSUM-GENERATE-AND-CHECK-AS-NOT-APPLICABLE-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-AFDX-END-SYSTEM-INTERNET-LAYER-TO-IMPLEMENT-IP-CRS-M1-00743` | `CRS-M1-00743` | REQUIRE-AFDX-END-SYSTEM-INTERNET-LAYER-TO-IMPLEMENT-IP | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-AFDX-END-SYSTEM-INTERNET-LAYER-TO-IMPLEMENT-ICMP-CRS-M1-00744` | `CRS-M1-00744` | REQUIRE-AFDX-END-SYSTEM-INTERNET-LAYER-TO-IMPLEMENT-ICMP | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SILENTLY-DISCARD-NON-IPV4-DATAGRAMS-CRS-M1-00745` | `CRS-M1-00745` | SILENTLY-DISCARD-NON-IPV4-DATAGRAMS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-AFDX-UDP-CHECKSUM-UNUSED-COMMENT-CRS-M1-00746` | `CRS-M1-00746` | RECORD-AFDX-UDP-CHECKSUM-UNUSED-COMMENT | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-SILENT-BAD-UDP-CHECKSUM-DISCARD-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00747` | `CRS-M1-00747` | TREAT-SILENT-BAD-UDP-CHECKSUM-DISCARD-AS-NOT-APPLICABLE-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-PASS-ICMP-MESSAGES-TO-APPLICATION-LIMITED-TO-ECHO-REQUEST-CRS-M1-00748` | `CRS-M1-00748` | PASS-ICMP-MESSAGES-TO-APPLICATION-LIMITED-TO-ECHO-REQUEST | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-UDP-PORT-UNREACHABLE-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00749` | `CRS-M1-00749` | TREAT-UDP-PORT-UNREACHABLE-AS-NOT-APPLICABLE-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-FORBID-REMOTE-MULTIHOMING-AT-APPLICATION-LAYER-ON-AFDX-CRS-M1-00750` | `CRS-M1-00750` | FORBID-REMOTE-MULTIHOMING-AT-APPLICATION-LAYER-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-LOCAL-MULTIHOMING-ON-AFDX-CRS-M1-00751` | `CRS-M1-00751` | REQUIRE-LOCAL-MULTIHOMING-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-LOG-DISCARDED-DATAGRAMS-ON-AFDX-CRS-M1-00752` | `CRS-M1-00752` | LOG-DISCARDED-DATAGRAMS-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-DISCARDED-DATAGRAMS-IN-COUNTER-ON-AFDX-CRS-M1-00753` | `CRS-M1-00753` | RECORD-DISCARDED-DATAGRAMS-IN-COUNTER-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ENTER-OPS-AFTER-COMPATIBLE-INIT-WHEN-SHOP-INACTIVE-CRS-M1-00754` | `CRS-M1-00754` | ENTER-OPS-AFTER-COMPATIBLE-INIT-WHEN-SHOP-INACTIVE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-PROVIDE-OPS-MODE-615A-INFORMATION-AND-FIND-CRS-M1-00755` | `CRS-M1-00755` | PROVIDE-OPS-MODE-615A-INFORMATION-AND-FIND | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ENTER-DL-FROM-INIT-ONLY-WHEN-GROUND-AND-COMPATIBILITY-FAIL-OR-EMPTY-CRS-M1-00756` | `CRS-M1-00756` | ENTER-DL-FROM-INIT-ONLY-WHEN-GROUND-AND-COMPATIBILITY-FAIL-OR-EMPTY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ENTER-DL-FROM-OPS-ONLY-WHEN-GROUND-UPLOAD-INIT-AND-HEADER-ACCEPTED-CRS-M1-00757` | `CRS-M1-00757` | ENTER-DL-FROM-OPS-ONLY-WHEN-GROUND-UPLOAD-INIT-AND-HEADER-ACCEPTED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-PROVIDE-DL-MODE-615A-INFORMATION-UPLOAD-AND-FIND-CRS-M1-00758` | `CRS-M1-00758` | PROVIDE-DL-MODE-615A-INFORMATION-UPLOAD-AND-FIND | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-SEND-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00759` | `CRS-M1-00759` | TREAT-UDP-IP-OPTIONS-SEND-AS-NOT-APPLICABLE-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-DOWN-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00760` | `CRS-M1-00760` | TREAT-UDP-IP-OPTIONS-DOWN-AS-NOT-APPLICABLE-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-GATEWAY-FORWARDING-SPEC-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00761` | `CRS-M1-00761` | TREAT-GATEWAY-FORWARDING-SPEC-AS-NOT-APPLICABLE-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-EMBEDDED-GATEWAY-SWITCH-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00762` | `CRS-M1-00762` | TREAT-EMBEDDED-GATEWAY-SWITCH-AS-NOT-APPLICABLE-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-NON-GATEWAY-DEFAULT-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00763` | `CRS-M1-00763` | TREAT-NON-GATEWAY-DEFAULT-AS-NOT-APPLICABLE-ON-AFDX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-AFDX-GATEWAY-AUTOCONFIGURATION-ROW-UNMARKED-CRS-M1-00764` | `CRS-M1-00764` | RECORD-AFDX-GATEWAY-AUTOCONFIGURATION-ROW-UNMARKED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-PERFORM-OPS-FILTERING-POLICING-SWITCHING-FROM-OPS-CONFIG-CRS-M1-00765` | `CRS-M1-00765` | PERFORM-OPS-FILTERING-POLICING-SWITCHING-FROM-OPS-CONFIG | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-OPS-FAULT-HEALTHY-INDICATOR-TO-HEALTHY-CRS-M1-00766` | `CRS-M1-00766` | SET-OPS-FAULT-HEALTHY-INDICATOR-TO-HEALTHY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-DL-UPLOAD-AS-PREFERABLY-EXCLUSIVE-CRS-M1-00767` | `CRS-M1-00767` | TREAT-DL-UPLOAD-AS-PREFERABLY-EXCLUSIVE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-DEDICATE-SWITCH-TO-UPLOAD-DURING-DL-UPLOAD-CRS-M1-00768` | `CRS-M1-00768` | DEDICATE-SWITCH-TO-UPLOAD-DURING-DL-UPLOAD | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-DEFAULT-RECEPTION-VL-FOR-DATALOADING-CRS-M1-00769` | `CRS-M1-00769` | REQUIRE-DEFAULT-RECEPTION-VL-FOR-DATALOADING | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RECORD-TWELVE-PIN-POSITION-IDENTIFICATION-AS-EXAMPLE-CRS-M1-00770` | `CRS-M1-00770` | RECORD-TWELVE-PIN-POSITION-IDENTIFICATION-AS-EXAMPLE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-STATED-TWELVE-PIN-DEFINITIONS-IF-TWELVE-PINS-CHOSEN-CRS-M1-00771` | `CRS-M1-00771` | USE-STATED-TWELVE-PIN-DEFINITIONS-IF-TWELVE-PINS-CHOSEN | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-KEEP-DEFAULT-CONFIGURATION-TABLE-RESIDENT-CRS-M1-00772` | `CRS-M1-00772` | KEEP-DEFAULT-CONFIGURATION-TABLE-RESIDENT | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-DEFAULT-PHYSICAL-PORT-SPEED-100MBPS-WITHOUT-AUTONEG-CRS-M1-00773` | `CRS-M1-00773` | SET-DEFAULT-PHYSICAL-PORT-SPEED-100MBPS-WITHOUT-AUTONEG | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-DEFAULT-RECEPTION-VL-FIELDS-IN-NONVOLATILE-MEMORY-CRS-M1-00774` | `CRS-M1-00774` | REQUIRE-DEFAULT-RECEPTION-VL-FIELDS-IN-NONVOLATILE-MEMORY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-DEFAULT-TRANSMISSION-VL-FIELDS-IN-NONVOLATILE-MEMORY-CRS-M1-00775` | `CRS-M1-00775` | REQUIRE-DEFAULT-TRANSMISSION-VL-FIELDS-IN-NONVOLATILE-MEMORY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-DEFAULT-TRANSMISSION-VL-FOR-DATALOADING-ACKNOWLEDGE-CRS-M1-00776` | `CRS-M1-00776` | REQUIRE-DEFAULT-TRANSMISSION-VL-FOR-DATALOADING-ACKNOWLEDGE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-OPS-CONFIGURATION-FILE-615A-665-FIELD-LOADABLE-CRS-M1-00777` | `CRS-M1-00777` | REQUIRE-OPS-CONFIGURATION-FILE-615A-665-FIELD-LOADABLE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-FILTERING-POLICING-FORWARDING-TABLE-PARAMETER-SET-CRS-M1-00778` | `CRS-M1-00778` | REQUIRE-FILTERING-POLICING-FORWARDING-TABLE-PARAMETER-SET | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-LISTED-PARAMETERS-TO-CONFIGURE-FILTER-POLICE-FORWARD-CRS-M1-00779` | `CRS-M1-00779` | REQUIRE-LISTED-PARAMETERS-TO-CONFIGURE-FILTER-POLICE-FORWARD | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-PERFORM-DL-END-SYSTEM-FROM-DEFAULT-CONFIGURATION-TABLE-CRS-M1-00780` | `CRS-M1-00780` | PERFORM-DL-END-SYSTEM-FROM-DEFAULT-CONFIGURATION-TABLE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-SET-DL-FAULT-HEALTHY-INDICATOR-TO-HEALTHY-CRS-M1-00781` | `CRS-M1-00781` | SET-DL-FAULT-HEALTHY-INDICATOR-TO-HEALTHY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-RETURN-TO-INIT-AT-END-OF-DL-MODE-CRS-M1-00782` | `CRS-M1-00782` | RETURN-TO-INIT-AT-END-OF-DL-MODE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-TREAT-DL-MODE-END-AS-615A-DATA-LOADING-FUNCTION-END-CRS-M1-00783` | `CRS-M1-00783` | TREAT-DL-MODE-END-AS-615A-DATA-LOADING-FUNCTION-END | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-LIMIT-SWITCH-FIELD-LOADABLE-SOFTWARE-TO-OPS-CONFIG-AND-OPS-SOFTWARE-CRS-M1-00784` | `CRS-M1-00784` | LIMIT-SWITCH-FIELD-LOADABLE-SOFTWARE-TO-OPS-CONFIG-AND-OPS-SOFTWARE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-REQUIRE-FIELD-LOADABLE-FILES-IDENTICAL-ACROSS-AIRCRAFT-SWITCHES-CRS-M1-00785` | `CRS-M1-00785` | REQUIRE-FIELD-LOADABLE-FILES-IDENTICAL-ACROSS-AIRCRAFT-SWITCHES | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-MAKE-SWITCH-CONFIGURATION-ACCESSIBLE-VIA-615A-INFORMATION-CRS-M1-00786` | `CRS-M1-00786` | MAKE-SWITCH-CONFIGURATION-ACCESSIBLE-VIA-615A-INFORMATION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-LEARN-DATALOADER-IP-FROM-SOURCE-ADDRESS-CRS-M1-00787` | `CRS-M1-00787` | LEARN-DATALOADER-IP-FROM-SOURCE-ADDRESS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-PIN-PROGRAMMING-FOR-POSITION-AND-DEFAULT-MAC-IP-CRS-M1-00788` | `CRS-M1-00788` | USE-PIN-PROGRAMMING-FOR-POSITION-AND-DEFAULT-MAC-IP | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-READ-PROGRAM-PINS-IN-INIT-ONLY-WHEN-GROUND-BEFORE-SAFETY-TEST-CRS-M1-00789` | `CRS-M1-00789` | READ-PROGRAM-PINS-IN-INIT-ONLY-WHEN-GROUND-BEFORE-SAFETY-TEST | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-DO-NOT-READ-PROGRAM-PINS-WHEN-GROUND-CONDITION-FALSE-CRS-M1-00790` | `CRS-M1-00790` | DO-NOT-READ-PROGRAM-PINS-WHEN-GROUND-CONDITION-FALSE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-USE-LAST-MEMORIZED-PIN-VALUES-WHEN-NOT-GROUND-CRS-M1-00791` | `CRS-M1-00791` | USE-LAST-MEMORIZED-PIN-VALUES-WHEN-NOT-GROUND | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-CHECK-TWELVE-PROGRAM-PINS-WITH-PARITY-BIT-CRS-M1-00792` | `CRS-M1-00792` | CHECK-TWELVE-PROGRAM-PINS-WITH-PARITY-BIT | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-MEMORIZE-PROGRAM-PINS-IN-NVM-AFTER-PARITY-PASS-CRS-M1-00793` | `CRS-M1-00793` | MEMORIZE-PROGRAM-PINS-IN-NVM-AFTER-PARITY-PASS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-ACQUIRE-SWITCH-POSITION-WITH-TWELVE-PINS-P1-P12-CRS-M1-00794` | `CRS-M1-00794` | ACQUIRE-SWITCH-POSITION-WITH-TWELVE-PINS-P1-P12 | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-CODE-PIN-GROUND-AS-ONE-CRS-M1-00795` | `CRS-M1-00795` | CODE-PIN-GROUND-AS-ONE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-CODE-PIN-OPEN-AS-ZERO-CRS-M1-00796` | `CRS-M1-00796` | CODE-PIN-OPEN-AS-ZERO | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-PROCESS-AT-LEAST-4096-VLS-IN-FILTER-POLICE-FORWARD-CRS-M1-00797` | `CRS-M1-00797` | PROCESS-AT-LEAST-4096-VLS-IN-FILTER-POLICE-FORWARD | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-INPUT-PHYSICAL-PORT-CRS-M1-00798` | `CRS-M1-00798` | INCLUDE-FILTER-TABLE-PER-VL-INPUT-PHYSICAL-PORT | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-OUTPUT-PHYSICAL-PORTS-CRS-M1-00799` | `CRS-M1-00799` | INCLUDE-FILTER-TABLE-PER-VL-OUTPUT-PHYSICAL-PORTS | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-MAC-DESTINATION-CRS-M1-00800` | `CRS-M1-00800` | INCLUDE-FILTER-TABLE-PER-VL-MAC-DESTINATION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-BAG-CRS-M1-00801` | `CRS-M1-00801` | INCLUDE-FILTER-TABLE-PER-VL-BAG | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-MAX-JITTER-CRS-M1-00802` | `CRS-M1-00802` | INCLUDE-FILTER-TABLE-PER-VL-MAX-JITTER | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-ACCOUNT-CRS-M1-00803` | `CRS-M1-00803` | INCLUDE-FILTER-TABLE-PER-VL-ACCOUNT | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-SMAX-CRS-M1-00804` | `CRS-M1-00804` | INCLUDE-FILTER-TABLE-PER-VL-SMAX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-SMIN-CRS-M1-00805` | `CRS-M1-00805` | INCLUDE-FILTER-TABLE-PER-VL-SMIN | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-PRIORITIZATION-CRS-M1-00806` | `CRS-M1-00806` | INCLUDE-FILTER-TABLE-PER-VL-PRIORITIZATION | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-MAX-DELAY-CRS-M1-00807` | `CRS-M1-00807` | INCLUDE-FILTER-TABLE-PER-PORT-MAX-DELAY | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-STATE-CRS-M1-00808` | `CRS-M1-00808` | INCLUDE-FILTER-TABLE-PER-PORT-STATE | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-SPEED-CRS-M1-00809` | `CRS-M1-00809` | INCLUDE-FILTER-TABLE-PER-PORT-SPEED | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-LOW-PRIORITY-BUFFER-CRS-M1-00810` | `CRS-M1-00810` | INCLUDE-FILTER-TABLE-PER-PORT-LOW-PRIORITY-BUFFER | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-HIGH-PRIORITY-BUFFER-CRS-M1-00811` | `CRS-M1-00811` | INCLUDE-FILTER-TABLE-PER-PORT-HIGH-PRIORITY-BUFFER | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-VL-IDENTIFIER-CRS-M1-00812` | `CRS-M1-00812` | INCLUDE-DEFAULT-RX-VL-IDENTIFIER | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-SMAX-CRS-M1-00813` | `CRS-M1-00813` | INCLUDE-DEFAULT-RX-SMAX | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-BAG-CRS-M1-00814` | `CRS-M1-00814` | INCLUDE-DEFAULT-RX-BAG | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-VL-IDENTIFIER-CRS-M1-00815` | `CRS-M1-00815` | INCLUDE-DEFAULT-TX-VL-IDENTIFIER | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-BAG-CRS-M1-00816` | `CRS-M1-00816` | INCLUDE-DEFAULT-TX-BAG | ARINC-664-NETWORK-CONSTRAINT |
| `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-SMAX-CRS-M1-00817` | `CRS-M1-00817` | INCLUDE-DEFAULT-TX-SMAX | ARINC-664-NETWORK-CONSTRAINT |

## 接口

- `IF_TFTP` `ABSTRACT-TRANSPORT` — 不重建完整 TFTP/IPv4 栈。
- `IF_TFTP_BLOCKSIZE` `OPTION-CAPABILITY` — 615A 5.3.2.3.8.1 要求数据加载器具备块大小／网络接口能力。RFC 2348 §2 是候选选项编码。能力仍为未建立。
- `IF_INTEGRITY` `DEPENDENCY-GUARDED` — 不假定完整性成功。
- `IF_NETWORK` `INFRASTRUCTURE-PREMISE` — Compliant IPv4/UDP 主机服务是 Project Configuration 的前提。

## 时序目录

| ID | CRS | 时钟 | 种类 | 边界 | AST | 复位 | 端点 | 检查 | 窗口 |
|---|---|---|---|---|---|---|---|---|---|
| `TIM-CRS-M1-00032` | `CRS-M1-00032` | `CLK_WAIT` | NOT-BEFORE-LOWER-BOUND | MESSAGE_TIMER_VALUE..None s | `{"kind":"COMPARE","op":"GE","left":{"kind":"CLOCK","name":"CLK_WAIT"},"right":{"kind":"SYMBOL","name":"MESSAGE_TIMER_VALUE","unit":"s"}}` | T_WAIT_FROM_UPL_FILE, T_WAIT_FROM_UPL_LUR, T_WAIT_FROM_INF_LCI, T_WAIT_FROM_INF_LCL | CLOSED/UNRESOLVED | `RELATION-BOUND` | RETRY-NOT-BEFORE-CARRIED-TIMER |
| `TIM-CRS-M1-00094` | `CRS-M1-00094` | `CLK_DLP` | DEADLINE-UPPER-BOUND | None..DLP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00097` | `CRS-M1-00097` | `CLK_DLP` | DEADLINE-UPPER-BOUND | None..DLP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00098` | `CRS-M1-00098` | `CLK_DLP` | DEADLINE-UPPER-BOUND | None..DLP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00099` | `CRS-M1-00099` | `CLK_EXCEPTION` | DEADLINE-UPPER-BOUND | None..EXCEPTION_TIMER s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}` | T_ENTER_UPL_EXC, T_ENTER_INF_EXC, T_INF_LCS_WRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00100` | `CRS-M1-00100` | `CLK_EXCEPTION` | DEADLINE-UPPER-BOUND | None..EXCEPTION_TIMER s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}` | T_ENTER_UPL_EXC, T_ENTER_INF_EXC, T_INF_LCS_WRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00101` | `CRS-M1-00101` | `CLK_EXCEPTION` | DEADLINE-UPPER-BOUND | None..EXCEPTION_TIMER s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}` | T_ENTER_UPL_EXC, T_ENTER_INF_EXC, T_INF_LCS_WRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00102` | `CRS-M1-00102` | `CLK_DLP` | DEADLINE-UPPER-BOUND | None..DLP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00106` | `CRS-M1-00106` | `CLK_EXCEPTION` | DEADLINE-UPPER-BOUND | None..EXCEPTION_TIMER s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}` | T_ENTER_UPL_EXC, T_ENTER_INF_EXC, T_INF_LCS_WRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00107` | `CRS-M1-00107` | `CLK_EXCEPTION` | DEADLINE-UPPER-BOUND | None..EXCEPTION_TIMER s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}` | T_ENTER_UPL_EXC, T_ENTER_INF_EXC, T_INF_LCS_WRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00108` | `CRS-M1-00108` | `CLK_EXCEPTION` | DEADLINE-UPPER-BOUND | None..EXCEPTION_TIMER s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}` | T_ENTER_UPL_EXC, T_ENTER_INF_EXC, T_INF_LCS_WRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00168` | `CRS-M1-00168` | `CLK_TFTP` | DEADLINE-UPPER-BOUND | None..TFTP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_TFTP"},"right":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"}}` | T_INF_LCI_RRQ, T_UPL_LUI_RRQ, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00176` | `CRS-M1-00176` | `CLK_DLP` | DEADLINE-UPPER-BOUND | None..DLP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00177` | `CRS-M1-00177` | `CLK_TFTP` | CONSTANT-DEFINITION | 2..2 s | `{"kind":"LITERAL","value":2,"unit":"s"}` | T_INF_LCI_RRQ, T_UPL_LUI_RRQ, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | CLOSED/CLOSED | `CONSTANT-DEFINITION` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00178` | `CRS-M1-00178` | `CLK_TFTP` | SOURCE-EQUATION | 0..TFTP-TO-DIVIDED-BY-4 s | `{"kind":"COMPARE","op":"LE","left":{"kind":"SYMBOL","name":"DURATION_TIME","unit":"s"},"right":{"kind":"BINARY","op":"DIV","left":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"},"right":{"kind":"LITERAL","value":4,"unit":"1"},"unit":"s"}}` | T_INF_LCI_RRQ, T_UPL_LUI_RRQ, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | CLOSED/CLOSED | `EQUATION-STRUCTURAL` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00179` | `CRS-M1-00179` | `CLK_DLP` | SOURCE-EQUATION | 0..TFTP-TO-DIVIDED-BY-2 s | `{"kind":"COMPARE","op":"LE","left":{"kind":"SYMBOL","name":"DURATION_TIME","unit":"s"},"right":{"kind":"BINARY","op":"DIV","left":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"},"right":{"kind":"LITERAL","value":2,"unit":"1"},"unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | CLOSED/CLOSED | `EQUATION-STRUCTURAL` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00184` | `CRS-M1-00184` | `CLK_DLP` | DEADLINE-UPPER-BOUND | None..DLP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00185` | `CRS-M1-00185` | `CLK_DLP` | DEADLINE-UPPER-BOUND | None..DLP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00186` | `CRS-M1-00186` | `CLK_DLP` | PROHIBITION-WINDOW-UPPER-BOUND | None..DLP_TO s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_DLP"},"right":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00187` | `CRS-M1-00187` | `CLK_DLP` | CONSTANT-DEFINITION | 13..13 s | `{"kind":"LITERAL","value":13,"unit":"s"}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | CLOSED/CLOSED | `CONSTANT-DEFINITION` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00188` | `CRS-M1-00188` | `CLK_DLP` | SOURCE-EQUATION | 0..DLP-TO-MINUS-RETRY-AND-NETWORK-TERMS s | `{"kind":"COMPARE","op":"GT","left":{"kind":"SYMBOL","name":"DLP_TO","unit":"s"},"right":{"kind":"BINARY","op":"ADD","left":{"kind":"SYMBOL","name":"DURATION_TIME","unit":"s"},"right":{"kind":"BINARY","op":"ADD","left":{"kind":"BINARY","op":"MUL","left":{"kind":"BINARY","op":"MUL","left":{"kind":"SYMBOL","name":"DLP_RETRY","unit":"1"},"right":{"kind":"BINARY","op":"ADD","left":{"kind":"SYMBOL","name":"TFTP_RETRY","unit":"1"},"right":{"kind":"LITERAL","value":1,"unit":"1"},"unit":"1"},"unit":"1"},"right":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"},"unit":"s"},"right":{"kind":"BINARY","op":"ADD","left":{"kind":"BINARY","op":"MUL","left":{"kind":"SYMBOL","name":"TFTP_RETRY","unit":"1"},"right":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"},"unit":"s"},"right":{"kind":"BINARY","op":"MUL","left":{"kind":"LITERAL","value":2,"unit":"1"},"right":{"kind":"BINARY","op":"DIV","left":{"kind":"SYMBOL","name":"TFTP_TO","unit":"s"},"right":{"kind":"LITERAL","value":4,"unit":"1"},"unit":"s"},"unit":"s"},"unit":"s"},"unit":"s"},"unit":"s"}}` | T_INF_ACCEPT_INIT, T_UPL_ACCEPT_INIT, T_UPL_LUR_WRQ, T_UPL_FILE_RRQ | CLOSED/OPEN | `EQUATION-STRUCTURAL` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00305` | `CRS-M1-00305` | `CLK_EXCEPTION` | DEADLINE-UPPER-BOUND | None..EXCEPTION_TIMER s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}` | T_ENTER_UPL_EXC, T_ENTER_INF_EXC, T_INF_LCS_WRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00322` | `CRS-M1-00322` | `CLK_EXCEPTION` | DEADLINE-UPPER-BOUND | None..EXCEPTION_TIMER s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_EXCEPTION"},"right":{"kind":"SYMBOL","name":"EXCEPTION_TIMER","unit":"s"}}` | T_ENTER_UPL_EXC, T_ENTER_INF_EXC, T_INF_LCS_WRQ | UNRESOLVED/UNRESOLVED | `RELATION-BOUND` | TIMEOUT-ONLY-AT-SOURCE-BOUND-DEADLINE |
| `TIM-CRS-M1-00520` | `CRS-M1-00520` | `CLK_FIND` | CONSTANT-DEFINITION | 3..3 s | `{"kind":"LITERAL","value":3,"unit":"s"}` | — | CLOSED/CLOSED | `CONSTANT-DEFINITION` | FIND-ANSWER-WINDOW-LIFETIME |
| `TIM-CRS-M1-00391` | `CRS-M1-00391` | `CLK_FIND` | DEADLINE-UPPER-BOUND | 0..2 s | `{"kind":"COMPARE","op":"LE","left":{"kind":"CLOCK","name":"CLK_FIND"},"right":{"kind":"LITERAL","value":2,"unit":"s"}}` | — | CLOSED/CLOSED | `RELATION-BOUND` | FIND-HOST-ANSWER-UPPER-BOUND |
| `TIM-CRS-M1-00521` | `CRS-M1-00521` | `CLK_FIND` | CONSTANT-DEFINITION | 3..3 s | `{"kind":"COMPARE","op":"EQ","left":{"kind":"CLOCK","name":"CLK_FIND"},"right":{"kind":"LITERAL","value":3,"unit":"s"}}` | — | CLOSED/CLOSED | `CONSTANT-DEFINITION` | FIND-REGISTRATION-CLOSE-AT-EXPIRY |
| `TIM-CRS-M1-00682` | `CRS-M1-00682` | `CLK_AFDX_ES` | SOURCE-EQUATION | 0..ONE-HUNDRED-FIFTY-MICROSECONDS-PLUS-FRAME-DELAY us | `{"kind":"COMPARE","op":"LT","left":{"kind":"SYMBOL","name":"TECH_LAT_TX","unit":"us"},"right":{"kind":"BINARY","op":"ADD","left":{"kind":"LITERAL","value":150,"unit":"us"},"right":{"kind":"SYMBOL","name":"FRAME_DELAY","unit":"us"},"unit":"us"}}` | — | CLOSED/OPEN | `EQUATION-STRUCTURAL` | AFDX-TX-TECH-LATENCY-STRICT-OPEN-BOUND |
| `TIM-CRS-M1-00683` | `CRS-M1-00683` | `CLK_AFDX_ES` | SOURCE-EQUATION | 0..150 us | `{"kind":"COMPARE","op":"LT","left":{"kind":"SYMBOL","name":"TECH_LAT_RX","unit":"us"},"right":{"kind":"LITERAL","value":150,"unit":"us"}}` | — | CLOSED/OPEN | `EQUATION-STRUCTURAL` | AFDX-RX-TECH-LATENCY-STRICT-OPEN-BOUND |
| `TIM-CRS-M1-00684` | `CRS-M1-00684` | `CLK_AFDX_ES` | SOURCE-EQUATION | 0..FORTY-MICROSECONDS-PLUS-CONVERTED-VL-LOAD-TERM us | `{"kind":"COMPARE","op":"LE","left":{"kind":"SYMBOL","name":"MAX_JITTER","unit":"us"},"right":{"kind":"BINARY","op":"ADD","left":{"kind":"LITERAL","value":40,"unit":"us"},"right":{"kind":"BINARY","op":"MUL","left":{"kind":"BINARY","op":"DIV","left":{"kind":"BINARY","op":"MUL","left":{"kind":"LITERAL","value":8,"unit":"1"},"right":{"kind":"SUM","index":"I","domain":"CONFIGURED-VL-SET","unit":"1","body":{"kind":"BINARY","op":"ADD","left":{"kind":"LITERAL","value":20,"unit":"1"},"right":{"kind":"SYMBOL","name":"LMAX_I","unit":"1"},"unit":"1"}},"unit":"1"},"right":{"kind":"SYMBOL","name":"NBW","unit":"1"},"unit":"s"},"right":{"kind":"LITERAL","value":1000000,"unit":"1"},"unit":"us"},"unit":"us"}}` | — | CLOSED/CLOSED | `EQUATION-STRUCTURAL` | AFDX-MAX-JITTER-LOAD-EQUATION |
| `TIM-CRS-M1-00685` | `CRS-M1-00685` | `CLK_AFDX_ES` | SOURCE-EQUATION | 0..500 us | `{"kind":"COMPARE","op":"LE","left":{"kind":"SYMBOL","name":"MAX_JITTER","unit":"us"},"right":{"kind":"LITERAL","value":500,"unit":"us"}}` | — | CLOSED/CLOSED | `EQUATION-STRUCTURAL` | AFDX-MAX-JITTER-500US-EQUATION |

## 需求处置

| CRS | 种类 | 目标 |
|---|---|---|
| `CRS-M1-00001` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00002` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00003` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00004` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00005` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00006` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00007` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00008` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00009` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00010` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00011` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00012` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00013` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00014` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00015` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00016` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00017` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00018` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00019` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00020` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00021` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00022` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00023` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00024` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00025` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00026` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00027` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00028` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00029` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00030` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00031` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00032` | MODELED-TIMING | `IF_TFTP`, `TIM-CRS-M1-00032`, `CLK_WAIT`, `T_WAIT_FROM_UPL_FILE`, `T_WAIT_FROM_UPL_LUR`, `T_WAIT_FROM_INF_LCI`, `T_WAIT_FROM_INF_LCL`, `T_WAIT_RETRY_UPL_FILE`, `T_WAIT_RETRY_UPL_LUR`, `T_WAIT_RETRY_INF_LCI`, `T_WAIT_RETRY_INF_LCL` |
| `CRS-M1-00033` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00034` | INTERFACE-PREMISE | `IF_TFTP_BLOCKSIZE` |
| `CRS-M1-00035` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00036` | INTERFACE-PREMISE | `IF_TFTP_BLOCKSIZE` |
| `CRS-M1-00037` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00038` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00039` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00040` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00041` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00042` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00043` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00044` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00045` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00046` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00047` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00048` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00049` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00050` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00051` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00052` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00053` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00054` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00055` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00056` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00057` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00058` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00059` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00060` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00061` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00062` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00063` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00064` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00065` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00066` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00067` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00068` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00069` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00070` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00071` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00072` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00073` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00074` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00075` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00076` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00077` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00078` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00079` | MODELED | `T_UPL_LUR_XFER` |
| `CRS-M1-00080` | MODELED | `T_UPL_LUS_XFER` |
| `CRS-M1-00081` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00082` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00083` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00084` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00085` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00086` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00087` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00088` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00089` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00090` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00091` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00092` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00093` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00094` | MODELED-TIMING | `T_INF_LCI_XFER`, `TIM-CRS-M1-00094`, `CLK_DLP` |
| `CRS-M1-00095` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00096` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00097` | MODELED-TIMING | `T_INF_LCI_XFER`, `TIM-CRS-M1-00097`, `CLK_DLP` |
| `CRS-M1-00098` | MODELED-TIMING | `T_INF_LCI_XFER`, `TIM-CRS-M1-00098`, `CLK_DLP` |
| `CRS-M1-00099` | MODELED-TIMING | `T_INF_LCI_XFER`, `TIM-CRS-M1-00099`, `CLK_EXCEPTION`, `T_ENTER_UPL_EXC`, `T_ENTER_INF_EXC` |
| `CRS-M1-00100` | MODELED-TIMING | `T_INF_LCI_XFER`, `TIM-CRS-M1-00100`, `CLK_EXCEPTION` |
| `CRS-M1-00101` | MODELED-TIMING | `T_INF_LCI_XFER`, `TIM-CRS-M1-00101`, `CLK_EXCEPTION`, `T_UPL_EXC_TO`, `T_INF_EXC_TO` |
| `CRS-M1-00102` | MODELED-TIMING | `T_UPL_LUS_XFER`, `TIM-CRS-M1-00102`, `CLK_DLP` |
| `CRS-M1-00103` | MODELED | `T_UPL_LUS_XFER` |
| `CRS-M1-00104` | MODELED | `T_UPL_LUS_XFER` |
| `CRS-M1-00105` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00106` | MODELED-TIMING | `T_UPL_FILE_XFER`, `TIM-CRS-M1-00106`, `CLK_EXCEPTION` |
| `CRS-M1-00107` | MODELED-TIMING | `T_UPL_FILE_XFER`, `TIM-CRS-M1-00107`, `CLK_EXCEPTION` |
| `CRS-M1-00108` | MODELED-TIMING | `T_UPL_LUS_XFER`, `TIM-CRS-M1-00108`, `CLK_EXCEPTION`, `T_UPL_EXC_TO` |
| `CRS-M1-00109` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00110` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00111` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00112` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00113` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00114` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00115` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00116` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00117` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00118` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00119` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00120` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00121` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00122` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00123` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00124` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00125` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00126` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00127` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00128` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00129` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00130` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00131` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00132` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00133` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00134` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00135` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00136` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00137` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00138` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00139` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00140` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00141` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00142` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00143` | MODELED | `T_UPL_LUR_XFER` |
| `CRS-M1-00144` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00145` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00146` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00147` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00148` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00149` | MODELED | `T_UPL_LUS_XFER` |
| `CRS-M1-00150` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00151` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00152` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00153` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00154` | MODELED | `T_UPL_LUS_XFER` |
| `CRS-M1-00155` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00156` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00157` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00158` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00159` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00160` | MODELED | `T_UPL_LUS_XFER` |
| `CRS-M1-00161` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00162` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00163` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00164` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00165` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00166` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00167` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00168` | MODELED-TIMING | `IF_TFTP`, `TIM-CRS-M1-00168`, `CLK_TFTP` |
| `CRS-M1-00169` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00170` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00171` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00172` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00173` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00174` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00175` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00176` | SCOPE-CONSTRAINT | `SCOPE`, `TIM-CRS-M1-00176`, `CLK_DLP` |
| `CRS-M1-00177` | SCOPE-CONSTRAINT | `SCOPE`, `TIM-CRS-M1-00177`, `CLK_TFTP`, `T_INF_TFTP_TO`, `T_UPL_TFTP_TO`, `T_UPL_LUR_TFTP_TO`, `T_UPL_FILE_TFTP_TO` |
| `CRS-M1-00178` | MODELED-TIMING | `IF_TFTP`, `TIM-CRS-M1-00178`, `CLK_TFTP` |
| `CRS-M1-00179` | MODELED-TIMING | `IF_TFTP`, `TIM-CRS-M1-00179`, `CLK_DLP` |
| `CRS-M1-00180` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00181` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00182` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00183` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00184` | MODELED-TIMING | `IF_TFTP`, `TIM-CRS-M1-00184`, `CLK_DLP` |
| `CRS-M1-00185` | SCOPE-CONSTRAINT | `SCOPE`, `TIM-CRS-M1-00185`, `CLK_DLP` |
| `CRS-M1-00186` | SCOPE-CONSTRAINT | `SCOPE`, `TIM-CRS-M1-00186`, `CLK_DLP` |
| `CRS-M1-00187` | SCOPE-CONSTRAINT | `SCOPE`, `TIM-CRS-M1-00187`, `CLK_DLP`, `T_UPL_DLP_TO`, `T_UPL_LUR_DLP_TO` |
| `CRS-M1-00188` | MODELED-TIMING | `IF_TFTP`, `TIM-CRS-M1-00188`, `CLK_DLP`, `T_UPL_LUR_DLP_TO` |
| `CRS-M1-00189` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00190` | INTERFACE-PREMISE | `IF_NETWORK` |
| `CRS-M1-00191` | DATA-CONSTRAINT | `OBJ-MINIMUM-ARINC-665-COMPATIBILITY-CAPABILITIES-IMPLEMENT-REQUIRED-ARINC-665-CA-CRS-M1-00191` |
| `CRS-M1-00192` | DATA-CONSTRAINT | `OBJ-ARINC-665-SHOULD-MODALITY-TREAT-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY-CRS-M1-00192` |
| `CRS-M1-00193` | DATA-CONSTRAINT | `OBJ-ARINC-665-MAY-MODALITY-TREAT-MAY-AS-OPTIONAL-CAPABILITY-CRS-M1-00193` |
| `CRS-M1-00194` | DATA-CONSTRAINT | `OBJ-OPTIONAL-ARINC-665-CAPABILITY-CONDITIONALLY-IMPLEMENT-OPTIONAL-CAPABILITY-AS-CRS-M1-00194` |
| `CRS-M1-00195` | DATA-CONSTRAINT | `OBJ-DATA-FIELD-TYPE-INTERPRET-FIELDS-AS-NUMERIC-BY-DEFAULT-CRS-M1-00195` |
| `CRS-M1-00196` | DATA-CONSTRAINT | `OBJ-ARINC-665-FILE-PROHIBIT-UNDEFINED-FIELD-INSERTION-CRS-M1-00196` |
| `CRS-M1-00197` | DATA-CONSTRAINT | `OBJ-FILE-VERSION-COMPATIBILITY-ENCODE-CRS-M1-00197` |
| `CRS-M1-00198` | DATA-CONSTRAINT | `OBJ-TARGET-HARDWARE-ID-MANUFACTURER-IDENTIFIER-PREFIX-TARGET-HARDWARE-ID-WITH-MA-CRS-M1-00198` |
| `CRS-M1-00199` | DATA-CONSTRAINT | `OBJ-MANUFACTURER-IDENTIFIER-ASSIGN-CRS-M1-00199` |
| `CRS-M1-00200` | DATA-CONSTRAINT | `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ASSIGN-GENERIC-TARGET-HARDWARE-ID-CRS-M1-00200` |
| `CRS-M1-00201` | DATA-CONSTRAINT | `OBJ-REDUNDANT-CHANNEL-LOADS-DISTRIBUTE-REDUNDANT-LOADS-INTERNALLY-CRS-M1-00201` |
| `CRS-M1-00202` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-ENSURE-CARDINALITY-CRS-M1-00202` |
| `CRS-M1-00203` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-COORDINATE-CRS-M1-00203` |
| `CRS-M1-00204` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-ASSIGN-CRS-M1-00204` |
| `CRS-M1-00205` | DATA-CONSTRAINT | `OBJ-LOADABLE-SOFTWARE-PART-NUMBER-FORMAT-CRS-M1-00205` |
| `CRS-M1-00206` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-EXCLUDE-EMBEDDED-BLANKS-CRS-M1-00206` |
| `CRS-M1-00207` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-DO-NOT-ENFORCE-SPECIFIC-PART-NUMBER-FORMAT-CRS-M1-00207` |
| `CRS-M1-00208` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-PROCESS-NONCONFORMING-PART-NUMBER-FORMATS-CRS-M1-00208` |
| `CRS-M1-00209` | DATA-CONSTRAINT | `OBJ-NETWORK-INTERFACE-DESIGN-CRS-M1-00209` |
| `CRS-M1-00210` | DATA-CONSTRAINT | `OBJ-NETWORK-INTERFACE-FORMAT-CRS-M1-00210` |
| `CRS-M1-00211` | DATA-CONSTRAINT | `OBJ-ATA-PART-NUMBER-DELIMITERS-SEPARATE-DELIMITERS-FROM-LETTERS-CRS-M1-00211` |
| `CRS-M1-00212` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-ENCODE-CRS-M1-00212` |
| `CRS-M1-00213` | DATA-CONSTRAINT | `OBJ-ATA-PART-NUMBER-CHARACTER-SET-EXCLUDE-AMBIGUOUS-LETTER-O-CRS-M1-00213` |
| `CRS-M1-00214` | DATA-CONSTRAINT | `OBJ-MMM-CODE-INTERPRET-CONFUSED-MMM-CHARACTERS-AS-ALPHABETIC-CRS-M1-00214` |
| `CRS-M1-00215` | DATA-CONSTRAINT | `OBJ-CHECK-CHARACTERS-COMPUTE-CRS-M1-00215` |
| `CRS-M1-00216` | DATA-CONSTRAINT | `OBJ-HEADER-FILE-SOFTWARE-PART-FORMAT-CRS-M1-00216` |
| `CRS-M1-00217` | DATA-CONSTRAINT | `OBJ-HEADER-FILE-SOFTWARE-PART-ENCODE-CRS-M1-00217` |
| `CRS-M1-00218` | DATA-CONSTRAINT | `OBJ-HEADER-FILE-DEFINE-CRS-M1-00218` |
| `CRS-M1-00219` | DATA-CONSTRAINT | `OBJ-BINARY-FIELD-ENCODING-ENCODE-CRS-M1-00219` |
| `CRS-M1-00220` | DATA-CONSTRAINT | `OBJ-OPERATION-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00220` |
| `CRS-M1-00221` | DATA-CONSTRAINT | `OBJ-BINARY-FIELD-ENCODING-ENCODE-CRS-M1-00221` |
| `CRS-M1-00222` | DATA-CONSTRAINT | `OBJ-TARGET-HARDWARE-ID-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00222` |
| `CRS-M1-00223` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-IMPLEMENT-CRS-M1-00223` |
| `CRS-M1-00224` | DATA-CONSTRAINT | `OBJ-NETWORK-INTERFACE-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00224` |
| `CRS-M1-00225` | DATA-CONSTRAINT | `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ENSURE-UNIQUE-CRS-M1-00225` |
| `CRS-M1-00226` | DATA-CONSTRAINT | `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ENCODE-CRS-M1-00226` |
| `CRS-M1-00227` | DATA-CONSTRAINT | `OBJ-TARGET-HARDWARE-ID-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00227` |
| `CRS-M1-00228` | DATA-CONSTRAINT | `OBJ-DATA-FILE-CONSTRAIN-CRS-M1-00228` |
| `CRS-M1-00229` | DATA-CONSTRAINT | `OBJ-DATA-FILE-SET-ZERO-CRS-M1-00229` |
| `CRS-M1-00230` | DATA-CONSTRAINT | `OBJ-DATA-FILE-FORMAT-CRS-M1-00230` |
| `CRS-M1-00231` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00232` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00233` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00234` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00235` | DATA-CONSTRAINT | `OBJ-NETWORK-INTERFACE-ENCODE-CRS-M1-00235` |
| `CRS-M1-00236` | DATA-CONSTRAINT | `OBJ-NETWORK-INTERFACE-IMPLEMENT-CRS-M1-00236` |
| `CRS-M1-00237` | DATA-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-NETWORK-INTERFACE-ENCODE-CRS-M1-00237` |
| `CRS-M1-00238` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00239` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00240` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00241` | DATA-CONSTRAINT | `OBJ-HEADER-FILE-VALIDATE-CRS-M1-00241` |
| `CRS-M1-00242` | DATA-CONSTRAINT | `OBJ-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00242` |
| `CRS-M1-00243` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00244` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00245` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00246` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00247` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00248` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00249` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00250` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00251` | DATA-CONSTRAINT | `OBJ-DATA-FILE-SOFTWARE-PART-ENCODE-CRS-M1-00251` |
| `CRS-M1-00252` | DATA-CONSTRAINT | `OBJ-SOFTWARE-PART-NETWORK-INTERFACE-ENCODE-CRS-M1-00252` |
| `CRS-M1-00253` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00254` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00255` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00256` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00257` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00258` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00259` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00260` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00261` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00262` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00263` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00264` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00265` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00266` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00267` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00268` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00269` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00270` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00271` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00272` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00273` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00274` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00275` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00276` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00277` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00278` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00279` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00280` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00281` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00282` | DATA-CONSTRAINT | `FC-LCI-FIELD-FILE-LENGTH` |
| `CRS-M1-00283` | DATA-CONSTRAINT | `FC-LCI-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00284` | DATA-CONSTRAINT | `FC-LCI-FIELD-OPERATION-ACCEPTANCE-STATUS-CODE` |
| `CRS-M1-00285` | DATA-CONSTRAINT | `FC-LCI-FIELD-STATUS-DESCRIPTION-LENGTH` |
| `CRS-M1-00286` | DATA-CONSTRAINT | `FC-LCI-FIELD-STATUS-DESCRIPTION` |
| `CRS-M1-00287` | DATA-CONSTRAINT | `FC-LCL-FIELD-FILE-LENGTH` |
| `CRS-M1-00288` | DATA-CONSTRAINT | `FC-LCL-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00289` | DATA-CONSTRAINT | `FC-LCL-FIELD-NUMBER-OF-TARGET-HARDWARE` |
| `CRS-M1-00290` | DATA-CONSTRAINT | `FC-LCL-FIELD-LITERAL-NAME-LENGTH` |
| `CRS-M1-00291` | DATA-CONSTRAINT | `FC-LCL-FIELD-LITERAL-NAME` |
| `CRS-M1-00292` | DATA-CONSTRAINT | `FC-LCL-FIELD-SERIAL-NUMBER-LENGTH` |
| `CRS-M1-00293` | DATA-CONSTRAINT | `FC-LCL-FIELD-SERIAL-NUMBER` |
| `CRS-M1-00294` | DATA-CONSTRAINT | `FC-LCL-FIELD-NUMBER-OF-PART-NUMBERS` |
| `CRS-M1-00295` | DATA-CONSTRAINT | `FC-LCL-FIELD-PART-NUMBER-LENGTH` |
| `CRS-M1-00296` | DATA-CONSTRAINT | `FC-LCL-FIELD-PART-NUMBER` |
| `CRS-M1-00297` | DATA-CONSTRAINT | `FC-LCL-FIELD-AMENDMENT-LENGTH` |
| `CRS-M1-00298` | DATA-CONSTRAINT | `FC-LCL-FIELD-AMENDMENT` |
| `CRS-M1-00299` | DATA-CONSTRAINT | `FC-LCL-FIELD-PART-DESIGNATION-LENGTH` |
| `CRS-M1-00300` | DATA-CONSTRAINT | `FC-LCL-FIELD-PART-DESIGNATION-TEXT` |
| `CRS-M1-00301` | DATA-CONSTRAINT | `FC-LCS-FIELD-FILE-LENGTH` |
| `CRS-M1-00302` | DATA-CONSTRAINT | `FC-LCS-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00303` | DATA-CONSTRAINT | `FC-LCS-FIELD-COUNTER` |
| `CRS-M1-00304` | DATA-CONSTRAINT | `FC-LCS-FIELD-INFORMATION-OPERATION-STATUS-CODE` |
| `CRS-M1-00305` | DATA-CONSTRAINT | `FC-LCS-FIELD-EXCEPTION-TIMER`, `TIM-CRS-M1-00305`, `CLK_EXCEPTION` |
| `CRS-M1-00306` | DATA-CONSTRAINT | `FC-LCS-FIELD-ESTIMATED-TIME` |
| `CRS-M1-00307` | DATA-CONSTRAINT | `FC-LCS-FIELD-STATUS-DESCRIPTION-LENGTH` |
| `CRS-M1-00308` | DATA-CONSTRAINT | `FC-LCS-FIELD-STATUS-DESCRIPTION` |
| `CRS-M1-00309` | DATA-CONSTRAINT | `FC-LUR-FIELD-FILE-LENGTH` |
| `CRS-M1-00310` | DATA-CONSTRAINT | `FC-LUR-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00311` | DATA-CONSTRAINT | `FC-LUR-FIELD-NUMBER-OF-HEADER-FILES` |
| `CRS-M1-00312` | DATA-CONSTRAINT | `FC-LUR-FIELD-HEADER-FILE-NAME-LENGTH` |
| `CRS-M1-00313` | DATA-CONSTRAINT | `FC-LUR-FIELD-HEADER-FILE-NAME` |
| `CRS-M1-00314` | DATA-CONSTRAINT | `FC-LUR-FIELD-LOAD-PART-NUMBER-NAME-LENGTH` |
| `CRS-M1-00315` | DATA-CONSTRAINT | `FC-LUR-FIELD-LOAD-PART-NUMBER-NAME` |
| `CRS-M1-00316` | DATA-CONSTRAINT | `FC-LUS-FIELD-FILE-LENGTH` |
| `CRS-M1-00317` | DATA-CONSTRAINT | `FC-LUS-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00318` | DATA-CONSTRAINT | `FC-LUS-FIELD-UPLOAD-OPERATION-STATUS-CODE` |
| `CRS-M1-00319` | DATA-CONSTRAINT | `FC-LUS-FIELD-UPLOAD-STATUS-DESCRIPTION-LENGTH` |
| `CRS-M1-00320` | DATA-CONSTRAINT | `FC-LUS-FIELD-UPLOAD-STATUS-DESCRIPTION` |
| `CRS-M1-00321` | DATA-CONSTRAINT | `FC-LUS-FIELD-COUNTER` |
| `CRS-M1-00322` | DATA-CONSTRAINT | `FC-LUS-FIELD-EXCEPTION-TIMER`, `TIM-CRS-M1-00322`, `CLK_EXCEPTION` |
| `CRS-M1-00323` | DATA-CONSTRAINT | `FC-LUS-FIELD-ESTIMATED-TIME` |
| `CRS-M1-00324` | DATA-CONSTRAINT | `FC-LUS-FIELD-LOAD-LIST-RATIO` |
| `CRS-M1-00325` | DATA-CONSTRAINT | `FC-LUS-FIELD-NUMBER-OF-HEADER-FILES` |
| `CRS-M1-00326` | DATA-CONSTRAINT | `FC-LUS-FIELD-HEADER-FILE-NAME-LENGTH` |
| `CRS-M1-00327` | DATA-CONSTRAINT | `FC-LUS-FIELD-HEADER-FILE-NAME` |
| `CRS-M1-00328` | DATA-CONSTRAINT | `FC-LUS-FIELD-LOAD-PART-NUMBER-NAME-LENGTH` |
| `CRS-M1-00329` | DATA-CONSTRAINT | `FC-LUS-FIELD-LOAD-PART-NUMBER-NAME` |
| `CRS-M1-00330` | DATA-CONSTRAINT | `FC-LUS-FIELD-LOAD-RATIO` |
| `CRS-M1-00331` | DATA-CONSTRAINT | `FC-LUS-FIELD-LOAD-STATUS` |
| `CRS-M1-00332` | DATA-CONSTRAINT | `FC-LUS-FIELD-LOAD-STATUS-DESCRIPTION-LENGTH` |
| `CRS-M1-00333` | DATA-CONSTRAINT | `FC-LUS-FIELD-LOAD-STATUS-DESCRIPTION` |
| `CRS-M1-00334` | DATA-CONSTRAINT | `ST-CRS-M1-00334` |
| `CRS-M1-00335` | DATA-CONSTRAINT | `ST-CRS-M1-00335` |
| `CRS-M1-00336` | DATA-CONSTRAINT | `ST-CRS-M1-00336` |
| `CRS-M1-00337` | DATA-CONSTRAINT | `ST-CRS-M1-00337` |
| `CRS-M1-00338` | DATA-CONSTRAINT | `ST-CRS-M1-00338` |
| `CRS-M1-00339` | DATA-CONSTRAINT | `ST-CRS-M1-00339` |
| `CRS-M1-00340` | DATA-CONSTRAINT | `ST-CRS-M1-00340`, `T_ABORT_TH`, `T_ABORTED` |
| `CRS-M1-00341` | DATA-CONSTRAINT | `ST-CRS-M1-00341`, `T_ABORT_DL`, `T_ABORTED`, `T_ABORT_FROM_S_INF_LCI_RRQ`, `T_ABORT_FROM_S_INF_LCL_XFER`, `T_ABORT_FROM_S_INF_LCS_XFER`, `T_ABORT_FROM_S_INF_EXCEPTION`, `T_ABORT_FROM_S_WAIT_RETRY`, `T_ABORT_FROM_S_UPL_LUI_XFER`, `T_ABORT_FROM_S_UPL_LIST_SENT`, `T_ABORT_FROM_S_UPL_WAIT_LUS0001`, `T_ABORT_FROM_S_UPL_LUR_XFER`, `T_ABORT_FROM_S_UPL_LUS_XFER` |
| `CRS-M1-00342` | DATA-CONSTRAINT | `ST-CRS-M1-00342` |
| `CRS-M1-00343` | DATA-CONSTRAINT | `ST-CRS-M1-00343` |
| `CRS-M1-00344` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00345` | DATA-CONSTRAINT | `ST-CRS-M1-00345` |
| `CRS-M1-00346` | MODELED | `T_INF_LCI_RRQ` |
| `CRS-M1-00347` | MODELED | `T_INF_LCI_RRQ` |
| `CRS-M1-00348` | MODELED | `T_INF_LCI_XFER` |
| `CRS-M1-00349` | MODELED | `T_INF_EVAL`, `T_INF_ACCEPT_INIT` |
| `CRS-M1-00350` | MODELED | `T_INF_REJECT` |
| `CRS-M1-00351` | MODELED | `T_INF_LCL_WRQ`, `T_INF_ACCEPT_INIT` |
| `CRS-M1-00352` | MODELED | `T_INF_LCL_ACK` |
| `CRS-M1-00353` | MODELED | `T_INF_LCL_XFER` |
| `CRS-M1-00354` | MODELED | `T_INF_APP` |
| `CRS-M1-00355` | MODELED | `T_INF_LCS_WRQ` |
| `CRS-M1-00356` | MODELED | `T_INF_LCS_XFER` |
| `CRS-M1-00357` | MODELED | `T_INF_LCS_XFER` |
| `CRS-M1-00358` | MODELED | `T_INF_LCS_XFER`, `T_INF_SESSION_END` |
| `CRS-M1-00359` | MODELED | `T_UPL_LUI_RRQ` |
| `CRS-M1-00360` | MODELED | `T_UPL_LUI_RRQ`, `T_UPL_LUI_RRQ_AFTER_INF` |
| `CRS-M1-00361` | MODELED | `T_UPL_LUI_XFER` |
| `CRS-M1-00362` | MODELED | `T_UPL_EVAL`, `T_UPL_ACCEPT_INIT`, `T_UPL_REJECT` |
| `CRS-M1-00363` | MODELED | `T_UPL_ACCEPT_INIT`, `T_UPL_LIST_OFFER` |
| `CRS-M1-00364` | MODELED | `T_UPL_LIST_OFFER`, `T_UPL_WAIT_LUS0001` |
| `CRS-M1-00365` | MODELED | `T_UPL_LUR_WRQ` |
| `CRS-M1-00366` | MODELED | `T_UPL_LUR_ACK` |
| `CRS-M1-00367` | MODELED | `T_UPL_LUR_XFER` |
| `CRS-M1-00368` | MODELED | `T_UPL_FILE_RRQ`, `T_UPL_FILE_RRQ_MORE` |
| `CRS-M1-00369` | MODELED | `T_UPL_FILE_UNAVAIL` |
| `CRS-M1-00370` | MODELED | `T_UPL_FILE_XFER` |
| `CRS-M1-00371` | MODELED | `T_UPL_FILE_STATUS` |
| `CRS-M1-00372` | MODELED | `T_UPL_MORE_FILES`, `T_UPL_FILE_RRQ_MORE` |
| `CRS-M1-00373` | MODELED | `T_UPL_TO_LUS` |
| `CRS-M1-00374` | MODELED | `T_UPL_LUS_XFER` |
| `CRS-M1-00375` | MODELED | `T_UPL_STATUS_APP` |
| `CRS-M1-00376` | MODELED | `T_UPL_COMPLETE`, `T_UPL_STATUS_REPEAT` |
| `CRS-M1-00377` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00378` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00379` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00380` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00381` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00382` | INTERFACE-PREMISE | `IF_TFTP` |
| `CRS-M1-00383` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00384` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00385` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00386` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00387` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00388` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00389` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00390` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00391` | SCOPE-CONSTRAINT | `SCOPE`, `TIM-CRS-M1-00391`, `CLK_FIND` |
| `CRS-M1-00392` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00393` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00394` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00395` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00396` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00397` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00398` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00399` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00400` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00401` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00402` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00403` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00404` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00405` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00406` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00407` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00408` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00409` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00410` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00411` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00412` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00413` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00414` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00415` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00416` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00417` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00418` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00419` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00420` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00421` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00422` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00423` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00424` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00426` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00427` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00428` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00429` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00430` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00431` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00432` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00433` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00434` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00435` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00436` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00437` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00438` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00439` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00440` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00441` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00442` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00443` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00444` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00445` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00446` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00447` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00448` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00449` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00450` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00451` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00452` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00453` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00454` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00455` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00456` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00457` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00458` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00459` | DATA-CONSTRAINT | `FC-LNR-FIELD-FILE-LENGTH` |
| `CRS-M1-00460` | DATA-CONSTRAINT | `FC-LNR-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00461` | DATA-CONSTRAINT | `FC-LNR-FIELD-NUMBER-OF-FILES` |
| `CRS-M1-00462` | DATA-CONSTRAINT | `FC-LNR-FIELD-FILE-NAME-LENGTH` |
| `CRS-M1-00463` | DATA-CONSTRAINT | `FC-LNR-FIELD-FILE-NAME` |
| `CRS-M1-00464` | DATA-CONSTRAINT | `FC-LNR-FIELD-USER-DEFINED-DATA-LENGTH` |
| `CRS-M1-00465` | DATA-CONSTRAINT | `FC-LNR-FIELD-USER-DEFINED-DATA` |
| `CRS-M1-00466` | DATA-CONSTRAINT | `FC-LNS-FIELD-FILE-LENGTH` |
| `CRS-M1-00467` | DATA-CONSTRAINT | `FC-LNS-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00468` | DATA-CONSTRAINT | `FC-LNS-FIELD-DOWNLOAD-OPERATION-STATUS-CODE` |
| `CRS-M1-00469` | DATA-CONSTRAINT | `FC-LNS-FIELD-DOWNLOAD-STATUS-DESCRIPTION-LENGTH` |
| `CRS-M1-00470` | DATA-CONSTRAINT | `FC-LNS-FIELD-DOWNLOAD-STATUS-DESCRIPTION` |
| `CRS-M1-00471` | DATA-CONSTRAINT | `FC-LNS-FIELD-COUNTER` |
| `CRS-M1-00472` | DATA-CONSTRAINT | `FC-LNS-FIELD-EXCEPTION-TIMER` |
| `CRS-M1-00473` | DATA-CONSTRAINT | `FC-LNS-FIELD-ESTIMATED-TIME` |
| `CRS-M1-00474` | DATA-CONSTRAINT | `FC-LNS-FIELD-DOWNLOAD-LIST-RATIO` |
| `CRS-M1-00475` | DATA-CONSTRAINT | `FC-LNS-FIELD-NUMBER-OF-FILES` |
| `CRS-M1-00476` | DATA-CONSTRAINT | `FC-LNS-FIELD-FILE-NAME-LENGTH` |
| `CRS-M1-00477` | DATA-CONSTRAINT | `FC-LNS-FIELD-FILE-NAME` |
| `CRS-M1-00478` | DATA-CONSTRAINT | `FC-LNS-FIELD-FILE-STATUS` |
| `CRS-M1-00479` | DATA-CONSTRAINT | `FC-LNS-FIELD-FILE-STATUS-DESCRIPTION-LENGTH` |
| `CRS-M1-00480` | DATA-CONSTRAINT | `FC-LNS-FIELD-FILE-STATUS-DESCRIPTION` |
| `CRS-M1-00481` | DATA-CONSTRAINT | `FC-LNL-FIELD-FILE-LENGTH` |
| `CRS-M1-00482` | DATA-CONSTRAINT | `FC-LNL-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00483` | DATA-CONSTRAINT | `FC-LNL-FIELD-NUMBER-OF-FILES` |
| `CRS-M1-00484` | DATA-CONSTRAINT | `FC-LNL-FIELD-FILE-NAME-LENGTH` |
| `CRS-M1-00485` | DATA-CONSTRAINT | `FC-LNL-FIELD-FILE-NAME` |
| `CRS-M1-00486` | DATA-CONSTRAINT | `FC-LNL-FIELD-FILE-DESCRIPTION-LENGTH` |
| `CRS-M1-00487` | DATA-CONSTRAINT | `FC-LNL-FIELD-FILE-DESCRIPTION` |
| `CRS-M1-00488` | DATA-CONSTRAINT | `FC-LNA-FIELD-FILE-LENGTH` |
| `CRS-M1-00489` | DATA-CONSTRAINT | `FC-LNA-FIELD-PROTOCOL-VERSION` |
| `CRS-M1-00490` | DATA-CONSTRAINT | `FC-LNA-FIELD-NUMBER-OF-FILES` |
| `CRS-M1-00491` | DATA-CONSTRAINT | `FC-LNA-FIELD-FILE-NAME-LENGTH` |
| `CRS-M1-00492` | DATA-CONSTRAINT | `FC-LNA-FIELD-FILE-NAME` |
| `CRS-M1-00493` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00494` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00495` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00496` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00497` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00498` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00499` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00500` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00501` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00502` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00503` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00504` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00505` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00506` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00507` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00508` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00509` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00510` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00511` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00512` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00513` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00514` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00515` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00516` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00517` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00518` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00519` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00520` | SCOPE-CONSTRAINT | `SCOPE`, `TIM-CRS-M1-00520`, `CLK_FIND` |
| `CRS-M1-00521` | SCOPE-CONSTRAINT | `SCOPE`, `TIM-CRS-M1-00521`, `CLK_FIND` |
| `CRS-M1-00522` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00523` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00524` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00525` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00526` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-MAY-USE-BATCH-FILE-FORMAT-CRS-M1-00526` |
| `CRS-M1-00527` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-LET-BATCH-FILE-SELECT-LSPS-PER-TARGET-HW-POSITION-CRS-M1-00527` |
| `CRS-M1-00528` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-IDENTIFY-BATCH-FILE-WITH-LUB-EXTENSION-CRS-M1-00528` |
| `CRS-M1-00529` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-MATCH-REFERENCED-HEADER-FILE-NAME-CASE-CRS-M1-00529` |
| `CRS-M1-00530` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-PREFIX-BATCH-FILE-NAME-WITH-MANUFACTURER-CODE-CRS-M1-00530` |
| `CRS-M1-00531` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-BATCH-FILE-NAME-UNIQUE-PER-MANUFACTURER-CODE-CRS-M1-00531` |
| `CRS-M1-00532` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-BATCH-FILE-PART-NUMBER-UNIQUE-AMONG-LSP-AND-BFP-CRS-M1-00532` |
| `CRS-M1-00533` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-REFERENCE-COMPLETE-HEADER-FILE-NAME-WITHOUT-PATH-CRS-M1-00533` |
| `CRS-M1-00534` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-USE-BATCH-FILE-ONLY-TO-AUTOMATE-MULTI-LSP-SETUP-CRS-M1-00534` |
| `CRS-M1-00535` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-DO-NOT-TRANSFER-BATCH-FILE-TO-TARGET-HARDWARE-CRS-M1-00535` |
| `CRS-M1-00536` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-INCLUDE-BATCH-FILE-CONTENT-DEFINED-BY-TABLE-2-3-1-1-CRS-M1-00536` |
| `CRS-M1-00537` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-BATCH-FILE-LENGTH-IN-16-BIT-WORDS-CRS-M1-00537` |
| `CRS-M1-00538` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-MAKE-BATCH-FILE-PN-COMPLIANT-WITH-SOFTWARE-LOAD-PN-FORMAT-CRS-M1-00538` |
| `CRS-M1-00539` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-BATCH-FILE-PN-DISTINCT-FROM-LSP-AND-MSP-CRS-M1-00539` |
| `CRS-M1-00540` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-SET-LAST-LOAD-LIST-BLOCK-POINTER-TO-ZERO-CRS-M1-00540` |
| `CRS-M1-00541` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-MATCH-TARGET-HW-ID-POS-TO-TARGET-HARDWARE-CRS-M1-00541` |
| `CRS-M1-00542` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-MATCH-HEADER-FILE-NAME-TO-LISTED-LSP-CRS-M1-00542` |
| `CRS-M1-00543` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-MATCH-LOAD-PN-TO-LSP-FOR-TARGET-HW-ID-POS-CRS-M1-00543` |
| `CRS-M1-00544` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00545` | DEPENDENCY-BLOCKED | `IF_INTEGRITY` |
| `CRS-M1-00546` | DATA-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-LENGTH` |
| `CRS-M1-00547` | DATA-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-FORMAT-VERSION` |
| `CRS-M1-00548` | DATA-CONSTRAINT | `FC-LUB-FIELD-SPARE` |
| `CRS-M1-00549` | DATA-CONSTRAINT | `FC-LUB-FIELD-POINTER-TO-BATCH-FILE-PN-LENGTH` |
| `CRS-M1-00550` | DATA-CONSTRAINT | `FC-LUB-FIELD-POINTER-TO-NUMBER-OF-TARGET-HW-ID-LOAD-LIST-BLOCKS` |
| `CRS-M1-00551` | DATA-CONSTRAINT | `FC-LUB-FIELD-EXPANSION-POINT-1` |
| `CRS-M1-00552` | DATA-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-PN-LENGTH` |
| `CRS-M1-00553` | DATA-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-PN` |
| `CRS-M1-00554` | DATA-CONSTRAINT | `FC-LUB-FIELD-COMMENT-LENGTH` |
| `CRS-M1-00555` | DATA-CONSTRAINT | `FC-LUB-FIELD-COMMENT` |
| `CRS-M1-00556` | DATA-CONSTRAINT | `FC-LUB-FIELD-EXPANSION-POINT-2` |
| `CRS-M1-00557` | DATA-CONSTRAINT | `FC-LUB-FIELD-NUMBER-OF-TARGET-HW-ID-LOAD-LIST-BLOCKS` |
| `CRS-M1-00558` | DATA-CONSTRAINT | `FC-LUB-FIELD-POINTER-TO-NEXT-TARGET-HW-ID-LOAD-LIST-BLOCK` |
| `CRS-M1-00559` | DATA-CONSTRAINT | `FC-LUB-FIELD-TARGET-HW-ID-POS-LENGTH` |
| `CRS-M1-00560` | DATA-CONSTRAINT | `FC-LUB-FIELD-TARGET-HW-ID-POS` |
| `CRS-M1-00561` | DATA-CONSTRAINT | `FC-LUB-FIELD-NUMBER-OF-LOADS-FOR-TARGET-HW-ID-POS` |
| `CRS-M1-00562` | DATA-CONSTRAINT | `FC-LUB-FIELD-HEADER-FILE-NAME-LENGTH` |
| `CRS-M1-00563` | DATA-CONSTRAINT | `FC-LUB-FIELD-HEADER-FILE-NAME` |
| `CRS-M1-00564` | DATA-CONSTRAINT | `FC-LUB-FIELD-LOAD-PN-LENGTH` |
| `CRS-M1-00565` | DATA-CONSTRAINT | `FC-LUB-FIELD-LOAD-PN` |
| `CRS-M1-00566` | DATA-CONSTRAINT | `FC-LUB-FIELD-EXPANSION-POINT-3` |
| `CRS-M1-00567` | DEPENDENCY-BLOCKED | `FC-LUB-FIELD-BATCH-FILE-CRC`, `IF_INTEGRITY` |
| `CRS-M1-00568` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-DEFINE-BATCH-FILE-FORMAT-VERSION-IN-16-BITS-CRS-M1-00568` |
| `CRS-M1-00569` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-TAKE-BATCH-FILE-FORMAT-VERSION-FROM-CLAUSE-1-4-1-CRS-M1-00569` |
| `CRS-M1-00570` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-USE-SPARE-TO-ALIGN-FOLLOWING-POINTERS-ON-4-BYTE-BOUNDARIES-CRS-M1-00570` |
| `CRS-M1-00571` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-POINT-TO-BATCH-FILE-PN-LENGTH-FROM-START-IN-16-BIT-WORDS-CRS-M1-00571` |
| `CRS-M1-00572` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-POINT-TO-LOAD-LIST-BLOCK-COUNT-FROM-START-IN-16-BIT-WORDS-CRS-M1-00572` |
| `CRS-M1-00573` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-MAY-GROW-FILE-FORMAT-AT-EXPANSION-POINTS-CRS-M1-00573` |
| `CRS-M1-00574` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-BATCH-FILE-PN-LENGTH-CRS-M1-00574` |
| `CRS-M1-00575` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-BATCH-FILE-PN-AS-8-BIT-ASCII-CRS-M1-00575` |
| `CRS-M1-00576` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-BATCH-FILE-PN-EVEN-OCTET-WIDTH-CRS-M1-00576` |
| `CRS-M1-00577` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-BATCH-FILE-PN-WITH-NUL-CRS-M1-00577` |
| `CRS-M1-00578` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-COMMENT-LENGTH-CRS-M1-00578` |
| `CRS-M1-00579` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-SET-COMMENT-LENGTH-ZERO-WHEN-NO-COMMENT-CRS-M1-00579` |
| `CRS-M1-00580` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-COMMENT-AS-8-BIT-ASCII-CRS-M1-00580` |
| `CRS-M1-00581` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-COMMENT-EVEN-OCTET-WIDTH-CRS-M1-00581` |
| `CRS-M1-00582` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-COMMENT-WITH-NUL-CRS-M1-00582` |
| `CRS-M1-00583` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-OMIT-COMMENT-FIELD-WHEN-COMMENT-LENGTH-ZERO-CRS-M1-00583` |
| `CRS-M1-00584` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-COUNT-TARGET-HW-ID-LOAD-LIST-BLOCKS-IN-BATCH-FILE-CRS-M1-00584` |
| `CRS-M1-00585` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-POINT-TO-NEXT-LOAD-LIST-BLOCK-IN-RELATIVE-16-BIT-WORDS-CRS-M1-00585` |
| `CRS-M1-00586` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-TARGET-HW-ID-POS-LENGTH-CRS-M1-00586` |
| `CRS-M1-00587` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-TARGET-HW-ID-POS-AS-8-BIT-ASCII-CRS-M1-00587` |
| `CRS-M1-00588` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-TARGET-HW-ID-POS-EVEN-OCTET-WIDTH-CRS-M1-00588` |
| `CRS-M1-00589` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-TARGET-HW-ID-POS-WITH-NUL-CRS-M1-00589` |
| `CRS-M1-00590` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-TARGET-HW-ID-POS-CONSISTENT-WITH-LISTED-LSP-HEADERS-CRS-M1-00590` |
| `CRS-M1-00591` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-COUNT-LOADS-IN-THE-TARGET-HW-ID-LOAD-LIST-BLOCK-CRS-M1-00591` |
| `CRS-M1-00592` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-HEADER-FILE-NAME-LENGTH-CRS-M1-00592` |
| `CRS-M1-00593` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-HEADER-FILE-NAME-AS-8-BIT-ASCII-CRS-M1-00593` |
| `CRS-M1-00594` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-HEADER-FILE-NAME-EVEN-OCTET-WIDTH-CRS-M1-00594` |
| `CRS-M1-00595` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-HEADER-FILE-NAME-WITH-NUL-CRS-M1-00595` |
| `CRS-M1-00596` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-USE-HEADER-FILE-NAME-WITHOUT-PATH-CRS-M1-00596` |
| `CRS-M1-00597` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-HEADER-FILE-NAME-FREE-OF-BACKSLASH-CRS-M1-00597` |
| `CRS-M1-00598` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-INCLUDE-HEADER-FILE-NAME-EXTENSIONS-AND-DELIMITERS-CRS-M1-00598` |
| `CRS-M1-00599` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-DEFINE-LOAD-PN-LENGTH-AS-CHARACTER-COUNT-CRS-M1-00599` |
| `CRS-M1-00600` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-LOAD-PN-LENGTH-CRS-M1-00600` |
| `CRS-M1-00601` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-LOAD-PN-AS-8-BIT-ASCII-CRS-M1-00601` |
| `CRS-M1-00602` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-LOAD-PN-EVEN-OCTET-WIDTH-CRS-M1-00602` |
| `CRS-M1-00603` | DATA-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-LOAD-PN-WITH-NUL-CRS-M1-00603` |
| `CRS-M1-00604` | DATA-CONSTRAINT | `OBJ-SUPPORTING-GIVE-664P3-PRECEDENCE-OVER-CONFLICTING-RFC-OPTIONS-CRS-M1-00604` |
| `CRS-M1-00605` | DATA-CONSTRAINT | `OBJ-SUPPORTING-GENERATE-AND-CHECK-UDP-CHECKSUM-CRS-M1-00605` |
| `CRS-M1-00606` | DATA-CONSTRAINT | `OBJ-SUPPORTING-IMPLEMENT-IPV4-IN-ACCORDANCE-WITH-P3-FIGURE-3-4-1-1-CRS-M1-00606` |
| `CRS-M1-00607` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-SECURE-RELIABLE-PARTITION-DATA-EXCHANGE-CRS-M1-00607` |
| `CRS-M1-00608` | DATA-CONSTRAINT | `OBJ-SUPPORTING-FILTER-AND-POLICE-FRAMES-FOR-INTEGRITY-LENGTH-BUDGET-AND-DESTINATION-CRS-M1-00608` |
| `CRS-M1-00609` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-AFDX-NOT-APPLICABLE-PROFILE-ITEMS-AS-MUST-NOT-CRS-M1-00609` |
| `CRS-M1-00610` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-UDP-LENGTH-TO-HEADER-PLUS-DATA-OCTETS-CRS-M1-00610` |
| `CRS-M1-00611` | DATA-CONSTRAINT | `OBJ-SUPPORTING-COMPUTE-UDP-CHECKSUM-OVER-PSEUDO-HEADER-HEADER-AND-DATA-CRS-M1-00611` |
| `CRS-M1-00612` | DATA-CONSTRAINT | `OBJ-SUPPORTING-IMPLEMENT-IPV4-ADDRESSING-AND-FRAGMENTATION-CRS-M1-00612` |
| `CRS-M1-00613` | DATA-CONSTRAINT | `OBJ-SUPPORTING-IMPLEMENT-IPV4-FRAGMENTATION-AND-REASSEMBLY-CRS-M1-00613` |
| `CRS-M1-00614` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SILENTLY-DISCARD-NON-IPV4-VERSION-CRS-M1-00614` |
| `CRS-M1-00615` | DATA-CONSTRAINT | `OBJ-SUPPORTING-GENERATE-AND-VALIDATE-UDP-CHECKSUMS-CRS-M1-00615` |
| `CRS-M1-00616` | DATA-CONSTRAINT | `OBJ-SUPPORTING-APPLY-RFC-1123-TFTP-HOST-NOTES-WITHOUT-ADOPTING-MAIL-NETASCII-OR-BROADCAST-RRQ-CRS-M1-00616` |
| `CRS-M1-00617` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-FIVE-TFTP-PACKET-TYPES-IDENTIFIED-BY-OPCODE-CRS-M1-00617` |
| `CRS-M1-00618` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ASSIGN-TID-ON-RRQ-OR-WRQ-WITHOUT-MAIL-MODE-CRS-M1-00618` |
| `CRS-M1-00619` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PLACE-OPCODE-IN-TFTP-HEADER-CRS-M1-00619` |
| `CRS-M1-00620` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TERMINATE-ON-DATA-PACKET-OF-0-TO-511-BYTES-CRS-M1-00620` |
| `CRS-M1-00621` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SEND-ERROR-PACKET-OPCODE-5-CRS-M1-00621` |
| `CRS-M1-00622` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ACKNOWLEDGE-OPTION-NEGOTIATION-WITH-OACK-CRS-M1-00622` |
| `CRS-M1-00623` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TERMINATE-TRANSFER-WITH-ERROR-CODE-8-CRS-M1-00623` |
| `CRS-M1-00624` | DATA-CONSTRAINT | `OBJ-SUPPORTING-APPEND-OPTIONS-TO-RRQ-OR-WRQ-CRS-M1-00624` |
| `CRS-M1-00625` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-BLKSIZE-AS-ASCII-OCTETS-FROM-8-THROUGH-65464-CRS-M1-00625` |
| `CRS-M1-00626` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-TIMEOUT-AS-ASCII-SECONDS-FROM-1-THROUGH-255-CRS-M1-00626` |
| `CRS-M1-00627` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUEST-TSIZE-ZERO-ON-RRQ-AND-RETURN-SIZE-IN-OACK-CRS-M1-00627` |
| `CRS-M1-00628` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-UDP-LENGTH-AT-LEAST-EIGHT-OCTETS-CRS-M1-00628` |
| `CRS-M1-00629` | DATA-CONSTRAINT | `OBJ-SUPPORTING-VERIFY-IP-HEADER-CHECKSUM-AND-SILENTLY-DISCARD-BAD-CRS-M1-00629` |
| `CRS-M1-00630` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SUPPORT-IPV4-REASSEMBLY-CRS-M1-00630` |
| `CRS-M1-00631` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SILENTLY-DISCARD-UDP-DATAGRAM-WITH-INVALID-CHECKSUM-CRS-M1-00631` |
| `CRS-M1-00632` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-RRQ-WRQ-AS-OPCODE-FILENAME-AND-MODE-CRS-M1-00632` |
| `CRS-M1-00633` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TERMINATE-TFTP-FILENAME-WITH-NUL-CRS-M1-00633` |
| `CRS-M1-00634` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-DATA-PACKET-WITH-BLOCK-NUMBER-AND-DATA-CRS-M1-00634` |
| `CRS-M1-00635` | DATA-CONSTRAINT | `OBJ-SUPPORTING-LIMIT-TFTP-DATA-FIELD-TO-ZERO-THROUGH-512-BYTES-CRS-M1-00635` |
| `CRS-M1-00636` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-ACK-PACKET-WITH-OPCODE-4-AND-BLOCK-NUMBER-CRS-M1-00636` |
| `CRS-M1-00637` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-ERROR-PACKET-AS-OPCODE-ERROR-CODE-AND-MESSAGE-CRS-M1-00637` |
| `CRS-M1-00638` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-BLKSIZE-VALUE-IN-ASCII-CRS-M1-00638` |
| `CRS-M1-00639` | DATA-CONSTRAINT | `OBJ-SUPPORTING-NEGOTIATE-BLKSIZE-LESS-OR-EQUAL-TO-CLIENT-VALUE-CRS-M1-00639` |
| `CRS-M1-00640` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-OACK-BLKSIZE-OR-TERMINATE-WITH-ERROR-8-CRS-M1-00640` |
| `CRS-M1-00641` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ECHO-CLIENT-TIMEOUT-VALUE-IN-OACK-CRS-M1-00641` |
| `CRS-M1-00642` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SPECIFY-TSIZE-ON-WRQ-AND-ECHO-IN-OACK-CRS-M1-00642` |
| `CRS-M1-00643` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MAY-ABORT-RRQ-WITH-ERROR-CODE-3-CRS-M1-00643` |
| `CRS-M1-00644` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MAY-ABORT-WRQ-WITH-ERROR-CODE-3-CRS-M1-00644` |
| `CRS-M1-00645` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TERMINATE-ON-DATA-SHORTER-THAN-NEGOTIATED-BLKSIZE-CRS-M1-00645` |
| `CRS-M1-00646` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SEND-ZERO-LENGTH-FINAL-DATA-WHEN-FILE-IS-INTEGRAL-MULTIPLE-OF-BLKSIZE-CRS-M1-00646` |
| `CRS-M1-00647` | DATA-CONSTRAINT | `OBJ-SUPPORTING-IGNORE-UNACKNOWLEDGED-OPTION-AND-KEEP-DEFAULT-PARAMETERS-CRS-M1-00647` |
| `CRS-M1-00648` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-VERSION-AS-4-BITS-CRS-M1-00648` |
| `CRS-M1-00649` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-IHL-AS-4-BITS-CRS-M1-00649` |
| `CRS-M1-00650` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-TOS-AS-8-BITS-CRS-M1-00650` |
| `CRS-M1-00651` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-TOTAL-LENGTH-AS-16-BITS-CRS-M1-00651` |
| `CRS-M1-00652` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-IDENTIFICATION-AS-16-BITS-CRS-M1-00652` |
| `CRS-M1-00653` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-FLAGS-AS-3-BITS-CRS-M1-00653` |
| `CRS-M1-00654` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-FRAGMENT-OFFSET-AS-13-BITS-CRS-M1-00654` |
| `CRS-M1-00655` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-TTL-AS-8-BITS-CRS-M1-00655` |
| `CRS-M1-00656` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-PROTOCOL-AS-8-BITS-CRS-M1-00656` |
| `CRS-M1-00657` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-HEADER-CHECKSUM-AS-16-BITS-CRS-M1-00657` |
| `CRS-M1-00658` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-SOURCE-ADDRESS-AS-32-BITS-CRS-M1-00658` |
| `CRS-M1-00659` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-DESTINATION-ADDRESS-AS-32-BITS-CRS-M1-00659` |
| `CRS-M1-00660` | DATA-CONSTRAINT | `OBJ-SUPPORTING-DO-NOT-SUPPORT-TFTP-MAIL-TRANSFER-MODE-CRS-M1-00660` |
| `CRS-M1-00661` | DATA-CONSTRAINT | `OBJ-SUPPORTING-COUNT-UDP-LENGTH-INCLUDING-EIGHT-OCTET-HEADER-CRS-M1-00661` |
| `CRS-M1-00662` | DATA-CONSTRAINT | `OBJ-SUPPORTING-NEVER-RESEND-CURRENT-DATA-ON-DUPLICATE-ACK-CRS-M1-00662` |
| `CRS-M1-00663` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-ADAPTIVE-TFTP-RETRANSMISSION-TIMEOUT-CRS-M1-00663` |
| `CRS-M1-00664` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-CONFIGURABLE-TFTP-PATHNAME-ACCESS-CONTROL-CRS-M1-00664` |
| `CRS-M1-00665` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SILENTLY-IGNORE-BROADCAST-TFTP-REQUEST-CRS-M1-00665` |
| `CRS-M1-00666` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ALLOW-ONLY-ONE-SOURCE-END-SYSTEM-PER-VL-CRS-M1-00666` |
| `CRS-M1-00667` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-VL-AS-UNIDIRECTIONAL-ONE-TO-MANY-CONNECTION-CRS-M1-00667` |
| `CRS-M1-00668` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-BAG-AS-MINIMUM-INTERVAL-BETWEEN-CONSECUTIVE-VL-FRAMES-CRS-M1-00668` |
| `CRS-M1-00669` | DATA-CONSTRAINT | `OBJ-SUPPORTING-BOUND-VL-FRAME-ARRIVAL-BY-MAXIMUM-ADMISSIBLE-JITTER-CRS-M1-00669` |
| `CRS-M1-00670` | DATA-CONSTRAINT | `OBJ-SUPPORTING-CHARACTERISE-VL-BANDWIDTH-BY-BAG-AND-LMAX-CRS-M1-00670` |
| `CRS-M1-00671` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ACCOMMODATE-VL-FRAMES-UP-TO-1518-BYTES-CRS-M1-00671` |
| `CRS-M1-00672` | DATA-CONSTRAINT | `OBJ-SUPPORTING-HANDLE-BAG-VALUES-FROM-1-MS-TO-128-MS-CRS-M1-00672` |
| `CRS-M1-00673` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RESTRICT-BAG-TO-POWERS-OF-TWO-MILLISECONDS-CRS-M1-00673` |
| `CRS-M1-00674` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-VL-JITTER-AT-OR-BELOW-500-MICROSECONDS-CRS-M1-00674` |
| `CRS-M1-00675` | DATA-CONSTRAINT | `OBJ-SUPPORTING-IDENTIFY-VL-ONLY-BY-MAC-DESTINATION-ADDRESS-CRS-M1-00675` |
| `CRS-M1-00676` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-IHL-IN-32-BIT-WORDS-CRS-M1-00676` |
| `CRS-M1-00677` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-IHL-AT-LEAST-5-CRS-M1-00677` |
| `CRS-M1-00678` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-IPV4-TOTAL-LENGTH-IN-OCTETS-INCLUDING-HEADER-AND-DATA-CRS-M1-00678` |
| `CRS-M1-00679` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-FRAGMENT-OFFSET-IN-8-OCTET-UNITS-CRS-M1-00679` |
| `CRS-M1-00680` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ALLOW-IPV4-OPTIONS-TO-BE-PRESENT-OR-ABSENT-CRS-M1-00680` |
| `CRS-M1-00681` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PAD-IPV4-HEADER-TO-32-BIT-BOUNDARY-CRS-M1-00681` |
| `CRS-M1-00682` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-TX-TECHNOLOGICAL-LATENCY-BELOW-150US-PLUS-FRAME-DELAY-CRS-M1-00682`, `TIM-CRS-M1-00682`, `CLK_AFDX_ES` |
| `CRS-M1-00683` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-RX-TECHNOLOGICAL-LATENCY-BELOW-150-MICROSECONDS-CRS-M1-00683`, `TIM-CRS-M1-00683`, `CLK_AFDX_ES` |
| `CRS-M1-00684` | DATA-CONSTRAINT | `OBJ-SUPPORTING-BOUND-MAX-JITTER-BY-40US-PLUS-VL-LOAD-TERM-CRS-M1-00684`, `TIM-CRS-M1-00684`, `CLK_AFDX_ES` |
| `CRS-M1-00685` | DATA-CONSTRAINT | `OBJ-SUPPORTING-BOUND-MAX-JITTER-BY-500-MICROSECONDS-EQUATION-CRS-M1-00685`, `TIM-CRS-M1-00685`, `CLK_AFDX_ES` |
| `CRS-M1-00686` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-MAC-SOURCE-AS-INDIVIDUAL-AND-LOCALLY-ADMINISTERED-CRS-M1-00686` |
| `CRS-M1-00687` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-SOURCE-CONSTANT-FIELD-TO-000000100000000000000000-CRS-M1-00687` |
| `CRS-M1-00688` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-SOURCE-INDIVIDUAL-ADDRESS-BIT-TO-ZERO-CRS-M1-00688` |
| `CRS-M1-00689` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-SOURCE-LOCALLY-ADMINISTERED-BIT-TO-ONE-CRS-M1-00689` |
| `CRS-M1-00690` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-MAC-SOURCE-USER-DEFINED-ID-AS-16-BITS-CRS-M1-00690` |
| `CRS-M1-00691` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-USER-DEFINED-ID-FOR-UNIQUE-MEANINGFUL-HOST-IDENTITY-CRS-M1-00691` |
| `CRS-M1-00692` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-INTERFACE-ID-TO-IDENTIFY-REDUNDANT-AFDX-NETWORK-CRS-M1-00692` |
| `CRS-M1-00693` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-INTERFACE-ID-001-AS-NETWORK-A-CRS-M1-00693` |
| `CRS-M1-00694` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-INTERFACE-ID-010-AS-NETWORK-B-CRS-M1-00694` |
| `CRS-M1-00695` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-ADN-ADDRESS-DETERMINATION-GUIDANCE-CRS-M1-00695` |
| `CRS-M1-00696` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KNOW-DESTINATION-ADDRESSES-AT-CONFIGURATION-TIME-CRS-M1-00696` |
| `CRS-M1-00697` | DATA-CONSTRAINT | `OBJ-SUPPORTING-DEFINE-ADN-ADDRESSING-PLAN-AND-RULES-CRS-M1-00697` |
| `CRS-M1-00698` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-IANA-WELL-KNOWN-UDP-PORTS-FOR-STANDARD-SERVICES-INCLUDING-TFTP-CRS-M1-00698` |
| `CRS-M1-00699` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ACCESS-PRIVATE-AERO-APPS-VIA-INTEGRATOR-OR-664P4-UDP-PORTS-CRS-M1-00699` |
| `CRS-M1-00700` | DATA-CONSTRAINT | `OBJ-SUPPORTING-DO-NOT-REASSIGN-WELL-KNOWN-COTS-PORTS-0-1023-CRS-M1-00700` |
| `CRS-M1-00701` | DATA-CONSTRAINT | `OBJ-SUPPORTING-DO-NOT-ROUTE-PRIVATE-ADDRESSES-OUTSIDE-THE-NETWORK-CRS-M1-00701` |
| `CRS-M1-00702` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-PROFILED-AERO-NETWORK-AS-IETF-PRIVATE-APPLICATION-CRS-M1-00702` |
| `CRS-M1-00703` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-PRIVATE-NETWORK-ID-FOR-PROFILED-NETWORKS-CRS-M1-00703` |
| `CRS-M1-00704` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ASSIGN-MAC-UNICAST-ADDRESSES-AT-CONFIGURATION-TIME-CRS-M1-00704` |
| `CRS-M1-00705` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-MAC-ADDRESSES-UNIQUE-UNDER-INTEGRATOR-SCHEME-CRS-M1-00705` |
| `CRS-M1-00706` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-UL-BIT-WHEN-INTEGRATOR-ASSIGNS-ADDRESSES-CRS-M1-00706` |
| `CRS-M1-00707` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-ALL-NETWORK-ADDRESSES-UNIQUE-CRS-M1-00707` |
| `CRS-M1-00708` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RESERVE-UDP-TCP-PORT-59-FOR-615A-DATA-LOADER-TFTP-CRS-M1-00708` |
| `CRS-M1-00709` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ASSIGN-UDP-PORT-24922-TO-FIND-PROTOCOL-CLIENT-CRS-M1-00709` |
| `CRS-M1-00710` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ALLOCATE-TABLE-2-1-ADDRESSES-FROM-RFC1918-PRIVATE-RANGES-CRS-M1-00710` |
| `CRS-M1-00711` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-TX-TECHNOLOGICAL-LATENCY-BETWEEN-PARTITION-DATA-AND-PHYSICAL-MEDIA-CRS-M1-00711` |
| `CRS-M1-00712` | DATA-CONSTRAINT | `OBJ-SUPPORTING-START-TX-TECHNOLOGICAL-LATENCY-WHEN-LAST-PARTITION-BIT-IS-AVAILABLE-CRS-M1-00712` |
| `CRS-M1-00713` | DATA-CONSTRAINT | `OBJ-SUPPORTING-END-TX-TECHNOLOGICAL-LATENCY-WHEN-LAST-FRAME-BIT-IS-ON-MEDIA-CRS-M1-00713` |
| `CRS-M1-00714` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-TX-TECHNOLOGICAL-LATENCY-WITH-EMPTY-BUFFERS-NO-CONTENTION-AND-NO-IP-FRAGMENTATION-CRS-M1-00714` |
| `CRS-M1-00715` | DATA-CONSTRAINT | `OBJ-SUPPORTING-DISTINGUISH-TECHNOLOGICAL-LATENCY-FROM-CONFIGURATION-LOAD-LATENCY-CRS-M1-00715` |
| `CRS-M1-00716` | DATA-CONSTRAINT | `OBJ-SUPPORTING-DEFINE-TECHNOLOGICAL-LATENCY-AS-ACCEPT-PROCESS-AND-BEGIN-TX-WITH-NO-OTHER-TASK-CRS-M1-00716` |
| `CRS-M1-00717` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ADD-FRAME-DELAY-FOR-PHYSICAL-LAYER-DELIVERY-CRS-M1-00717` |
| `CRS-M1-00718` | DATA-CONSTRAINT | `OBJ-SUPPORTING-START-RX-TECHNOLOGICAL-LATENCY-WHEN-LAST-FRAME-BIT-IS-RECEIVED-CRS-M1-00718` |
| `CRS-M1-00719` | DATA-CONSTRAINT | `OBJ-SUPPORTING-END-RX-TECHNOLOGICAL-LATENCY-WHEN-LAST-DATA-BIT-IS-AVAILABLE-TO-PARTITION-CRS-M1-00719` |
| `CRS-M1-00720` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-RX-TECHNOLOGICAL-LATENCY-WITH-EMPTY-BUFFERS-AND-NO-CONTENTION-CRS-M1-00720` |
| `CRS-M1-00721` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SATISFY-BOTH-MAX-JITTER-EQUATIONS-SIMULTANEOUSLY-CRS-M1-00721` |
| `CRS-M1-00722` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-MAX-JITTER-AS-MICROSECONDS-NBW-AS-BITS-PER-SECOND-AND-LMAX-AS-OCTETS-CRS-M1-00722` |
| `CRS-M1-00723` | DATA-CONSTRAINT | `OBJ-SUPPORTING-COMPOSE-MAC-SOURCE-AS-24-PLUS-16-PLUS-3-PLUS-5-BIT-FIELDS-CRS-M1-00723` |
| `CRS-M1-00724` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-SOURCE-CONSTANT-TAIL-TO-00000-CRS-M1-00724` |
| `CRS-M1-00725` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-MAC-SOURCE-CONSTRUCTION-ALGORITHM-AS-NOT-UNIQUELY-RECOMMENDED-CRS-M1-00725` |
| `CRS-M1-00726` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-000-AS-NOT-USED-CRS-M1-00726` |
| `CRS-M1-00727` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-011-AS-NOT-USED-CRS-M1-00727` |
| `CRS-M1-00728` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-100-AS-NOT-USED-CRS-M1-00728` |
| `CRS-M1-00729` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-101-AS-NOT-USED-CRS-M1-00729` |
| `CRS-M1-00730` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-110-AS-SOURCE-NOR-USED-CRS-M1-00730` |
| `CRS-M1-00731` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-111-AS-NOT-USED-CRS-M1-00731` |
| `CRS-M1-00732` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-P3-RFC-OPTION-RESTRICTION-PHILOSOPHY-CRS-M1-00732` |
| `CRS-M1-00733` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-P3-CONTENTS-LIMITED-TO-RFC-DELTAS-CRS-M1-00733` |
| `CRS-M1-00734` | DATA-CONSTRAINT | `OBJ-SUPPORTING-COMPOSE-AFDX-SWITCH-FROM-FIVE-FUNCTIONAL-BLOCKS-CRS-M1-00734` |
| `CRS-M1-00735` | DATA-CONSTRAINT | `OBJ-SUPPORTING-CONTROL-AFDX-SWITCH-FUNCTIONS-WITH-STATIC-CONFIGURATION-TABLES-CRS-M1-00735` |
| `CRS-M1-00736` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-SWITCH-END-SYSTEM-TO-COMPLY-WITH-SECTION-3-EXCEPT-REDUNDANCY-CRS-M1-00736` |
| `CRS-M1-00737` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-SWITCH-END-SYSTEM-UNICAST-MAC-AS-SOURCE-ADDRESS-CRS-M1-00737` |
| `CRS-M1-00738` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-615A-SESSION-ACROSS-OPS-TO-DL-TRANSITION-CRS-M1-00738` |
| `CRS-M1-00739` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-615A-AND-665-TO-UPLOAD-SWITCH-SOFTWARE-AND-CONFIGURATION-CRS-M1-00739` |
| `CRS-M1-00740` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-AFDX-SWITCH-PHYSICAL-LAYER-TO-COMPLY-WITH-664P2-CRS-M1-00740` |
| `CRS-M1-00741` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-AS-NOT-USED-ON-AFDX-CRS-M1-00741` |
| `CRS-M1-00742` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-CHECKSUM-GENERATE-AND-CHECK-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00742` |
| `CRS-M1-00743` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-AFDX-END-SYSTEM-INTERNET-LAYER-TO-IMPLEMENT-IP-CRS-M1-00743` |
| `CRS-M1-00744` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-AFDX-END-SYSTEM-INTERNET-LAYER-TO-IMPLEMENT-ICMP-CRS-M1-00744` |
| `CRS-M1-00745` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SILENTLY-DISCARD-NON-IPV4-DATAGRAMS-CRS-M1-00745` |
| `CRS-M1-00746` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-AFDX-UDP-CHECKSUM-UNUSED-COMMENT-CRS-M1-00746` |
| `CRS-M1-00747` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-SILENT-BAD-UDP-CHECKSUM-DISCARD-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00747` |
| `CRS-M1-00748` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PASS-ICMP-MESSAGES-TO-APPLICATION-LIMITED-TO-ECHO-REQUEST-CRS-M1-00748` |
| `CRS-M1-00749` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-PORT-UNREACHABLE-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00749` |
| `CRS-M1-00750` | DATA-CONSTRAINT | `OBJ-SUPPORTING-FORBID-REMOTE-MULTIHOMING-AT-APPLICATION-LAYER-ON-AFDX-CRS-M1-00750` |
| `CRS-M1-00751` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-LOCAL-MULTIHOMING-ON-AFDX-CRS-M1-00751` |
| `CRS-M1-00752` | DATA-CONSTRAINT | `OBJ-SUPPORTING-LOG-DISCARDED-DATAGRAMS-ON-AFDX-CRS-M1-00752` |
| `CRS-M1-00753` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-DISCARDED-DATAGRAMS-IN-COUNTER-ON-AFDX-CRS-M1-00753` |
| `CRS-M1-00754` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENTER-OPS-AFTER-COMPATIBLE-INIT-WHEN-SHOP-INACTIVE-CRS-M1-00754` |
| `CRS-M1-00755` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-OPS-MODE-615A-INFORMATION-AND-FIND-CRS-M1-00755` |
| `CRS-M1-00756` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENTER-DL-FROM-INIT-ONLY-WHEN-GROUND-AND-COMPATIBILITY-FAIL-OR-EMPTY-CRS-M1-00756` |
| `CRS-M1-00757` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ENTER-DL-FROM-OPS-ONLY-WHEN-GROUND-UPLOAD-INIT-AND-HEADER-ACCEPTED-CRS-M1-00757` |
| `CRS-M1-00758` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-DL-MODE-615A-INFORMATION-UPLOAD-AND-FIND-CRS-M1-00758` |
| `CRS-M1-00759` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-SEND-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00759` |
| `CRS-M1-00760` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-DOWN-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00760` |
| `CRS-M1-00761` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-GATEWAY-FORWARDING-SPEC-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00761` |
| `CRS-M1-00762` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-EMBEDDED-GATEWAY-SWITCH-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00762` |
| `CRS-M1-00763` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-NON-GATEWAY-DEFAULT-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00763` |
| `CRS-M1-00764` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-AFDX-GATEWAY-AUTOCONFIGURATION-ROW-UNMARKED-CRS-M1-00764` |
| `CRS-M1-00765` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PERFORM-OPS-FILTERING-POLICING-SWITCHING-FROM-OPS-CONFIG-CRS-M1-00765` |
| `CRS-M1-00766` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-OPS-FAULT-HEALTHY-INDICATOR-TO-HEALTHY-CRS-M1-00766` |
| `CRS-M1-00767` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-DL-UPLOAD-AS-PREFERABLY-EXCLUSIVE-CRS-M1-00767` |
| `CRS-M1-00768` | DATA-CONSTRAINT | `OBJ-SUPPORTING-DEDICATE-SWITCH-TO-UPLOAD-DURING-DL-UPLOAD-CRS-M1-00768` |
| `CRS-M1-00769` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-DEFAULT-RECEPTION-VL-FOR-DATALOADING-CRS-M1-00769` |
| `CRS-M1-00770` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RECORD-TWELVE-PIN-POSITION-IDENTIFICATION-AS-EXAMPLE-CRS-M1-00770` |
| `CRS-M1-00771` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-STATED-TWELVE-PIN-DEFINITIONS-IF-TWELVE-PINS-CHOSEN-CRS-M1-00771` |
| `CRS-M1-00772` | DATA-CONSTRAINT | `OBJ-SUPPORTING-KEEP-DEFAULT-CONFIGURATION-TABLE-RESIDENT-CRS-M1-00772` |
| `CRS-M1-00773` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-DEFAULT-PHYSICAL-PORT-SPEED-100MBPS-WITHOUT-AUTONEG-CRS-M1-00773` |
| `CRS-M1-00774` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-DEFAULT-RECEPTION-VL-FIELDS-IN-NONVOLATILE-MEMORY-CRS-M1-00774` |
| `CRS-M1-00775` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-DEFAULT-TRANSMISSION-VL-FIELDS-IN-NONVOLATILE-MEMORY-CRS-M1-00775` |
| `CRS-M1-00776` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-DEFAULT-TRANSMISSION-VL-FOR-DATALOADING-ACKNOWLEDGE-CRS-M1-00776` |
| `CRS-M1-00777` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-OPS-CONFIGURATION-FILE-615A-665-FIELD-LOADABLE-CRS-M1-00777` |
| `CRS-M1-00778` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-FILTERING-POLICING-FORWARDING-TABLE-PARAMETER-SET-CRS-M1-00778` |
| `CRS-M1-00779` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-LISTED-PARAMETERS-TO-CONFIGURE-FILTER-POLICE-FORWARD-CRS-M1-00779` |
| `CRS-M1-00780` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PERFORM-DL-END-SYSTEM-FROM-DEFAULT-CONFIGURATION-TABLE-CRS-M1-00780` |
| `CRS-M1-00781` | DATA-CONSTRAINT | `OBJ-SUPPORTING-SET-DL-FAULT-HEALTHY-INDICATOR-TO-HEALTHY-CRS-M1-00781` |
| `CRS-M1-00782` | DATA-CONSTRAINT | `OBJ-SUPPORTING-RETURN-TO-INIT-AT-END-OF-DL-MODE-CRS-M1-00782` |
| `CRS-M1-00783` | DATA-CONSTRAINT | `OBJ-SUPPORTING-TREAT-DL-MODE-END-AS-615A-DATA-LOADING-FUNCTION-END-CRS-M1-00783` |
| `CRS-M1-00784` | DATA-CONSTRAINT | `OBJ-SUPPORTING-LIMIT-SWITCH-FIELD-LOADABLE-SOFTWARE-TO-OPS-CONFIG-AND-OPS-SOFTWARE-CRS-M1-00784` |
| `CRS-M1-00785` | DATA-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-FIELD-LOADABLE-FILES-IDENTICAL-ACROSS-AIRCRAFT-SWITCHES-CRS-M1-00785` |
| `CRS-M1-00786` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MAKE-SWITCH-CONFIGURATION-ACCESSIBLE-VIA-615A-INFORMATION-CRS-M1-00786` |
| `CRS-M1-00787` | DATA-CONSTRAINT | `OBJ-SUPPORTING-LEARN-DATALOADER-IP-FROM-SOURCE-ADDRESS-CRS-M1-00787` |
| `CRS-M1-00788` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-PIN-PROGRAMMING-FOR-POSITION-AND-DEFAULT-MAC-IP-CRS-M1-00788` |
| `CRS-M1-00789` | DATA-CONSTRAINT | `OBJ-SUPPORTING-READ-PROGRAM-PINS-IN-INIT-ONLY-WHEN-GROUND-BEFORE-SAFETY-TEST-CRS-M1-00789` |
| `CRS-M1-00790` | DATA-CONSTRAINT | `OBJ-SUPPORTING-DO-NOT-READ-PROGRAM-PINS-WHEN-GROUND-CONDITION-FALSE-CRS-M1-00790` |
| `CRS-M1-00791` | DATA-CONSTRAINT | `OBJ-SUPPORTING-USE-LAST-MEMORIZED-PIN-VALUES-WHEN-NOT-GROUND-CRS-M1-00791` |
| `CRS-M1-00792` | DATA-CONSTRAINT | `OBJ-SUPPORTING-CHECK-TWELVE-PROGRAM-PINS-WITH-PARITY-BIT-CRS-M1-00792` |
| `CRS-M1-00793` | DATA-CONSTRAINT | `OBJ-SUPPORTING-MEMORIZE-PROGRAM-PINS-IN-NVM-AFTER-PARITY-PASS-CRS-M1-00793` |
| `CRS-M1-00794` | DATA-CONSTRAINT | `OBJ-SUPPORTING-ACQUIRE-SWITCH-POSITION-WITH-TWELVE-PINS-P1-P12-CRS-M1-00794` |
| `CRS-M1-00795` | DATA-CONSTRAINT | `OBJ-SUPPORTING-CODE-PIN-GROUND-AS-ONE-CRS-M1-00795` |
| `CRS-M1-00796` | DATA-CONSTRAINT | `OBJ-SUPPORTING-CODE-PIN-OPEN-AS-ZERO-CRS-M1-00796` |
| `CRS-M1-00797` | DATA-CONSTRAINT | `OBJ-SUPPORTING-PROCESS-AT-LEAST-4096-VLS-IN-FILTER-POLICE-FORWARD-CRS-M1-00797` |
| `CRS-M1-00798` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-INPUT-PHYSICAL-PORT-CRS-M1-00798` |
| `CRS-M1-00799` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-OUTPUT-PHYSICAL-PORTS-CRS-M1-00799` |
| `CRS-M1-00800` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-MAC-DESTINATION-CRS-M1-00800` |
| `CRS-M1-00801` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-BAG-CRS-M1-00801` |
| `CRS-M1-00802` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-MAX-JITTER-CRS-M1-00802` |
| `CRS-M1-00803` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-ACCOUNT-CRS-M1-00803` |
| `CRS-M1-00804` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-SMAX-CRS-M1-00804` |
| `CRS-M1-00805` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-SMIN-CRS-M1-00805` |
| `CRS-M1-00806` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-PRIORITIZATION-CRS-M1-00806` |
| `CRS-M1-00807` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-MAX-DELAY-CRS-M1-00807` |
| `CRS-M1-00808` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-STATE-CRS-M1-00808` |
| `CRS-M1-00809` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-SPEED-CRS-M1-00809` |
| `CRS-M1-00810` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-LOW-PRIORITY-BUFFER-CRS-M1-00810` |
| `CRS-M1-00811` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-HIGH-PRIORITY-BUFFER-CRS-M1-00811` |
| `CRS-M1-00812` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-VL-IDENTIFIER-CRS-M1-00812` |
| `CRS-M1-00813` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-SMAX-CRS-M1-00813` |
| `CRS-M1-00814` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-BAG-CRS-M1-00814` |
| `CRS-M1-00815` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-VL-IDENTIFIER-CRS-M1-00815` |
| `CRS-M1-00816` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-BAG-CRS-M1-00816` |
| `CRS-M1-00817` | DATA-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-SMAX-CRS-M1-00817` |
| `CRS-M1-00818` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00819` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00820` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00821` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00822` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00823` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00824` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00825` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00826` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00827` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00828` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00829` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00830` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00831` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00832` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00833` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00834` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00835` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00836` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00837` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00838` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00839` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00840` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00841` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00842` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00843` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00844` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00845` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00846` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00847` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00848` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00849` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00850` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00851` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00852` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00853` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00854` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00855` | SCOPE-CONSTRAINT | `SCOPE` |
| `CRS-M1-00856` | SCOPE-CONSTRAINT | `SCOPE` |

## 追踪关系

| ID | CRS | 种类 | 目标 | 理由 |
|---|---|---|---|---|
| `TR-CRS-M1-00001-0001` | `CRS-M1-00001` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00002-0002` | `CRS-M1-00002` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00003-0003` | `CRS-M1-00003` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00004-0004` | `CRS-M1-00004` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00005-0005` | `CRS-M1-00005` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00006-0006` | `CRS-M1-00006` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00007-0007` | `CRS-M1-00007` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00008-0008` | `CRS-M1-00008` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00009-0009` | `CRS-M1-00009` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00010-0010` | `CRS-M1-00010` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00011-0011` | `CRS-M1-00011` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00012-0012` | `CRS-M1-00012` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00013-0013` | `CRS-M1-00013` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00014-0014` | `CRS-M1-00014` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00015-0015` | `CRS-M1-00015` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00016-0016` | `CRS-M1-00016` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00017-0017` | `CRS-M1-00017` | SCOPE | `SCOPE` | 非行为／Profile 义务 ENCODE 保持为范围或适用性约束。 |
| `TR-CRS-M1-00018-0018` | `CRS-M1-00018` | INTERFACE | `IF_NETWORK` | 网络基础设施前提；能力未建立。 |
| `TR-CRS-M1-00019-0019` | `CRS-M1-00019` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00020-0020` | `CRS-M1-00020` | INTERFACE | `IF_TFTP` | TRANSFER 的 TFTP 接口前提。 |
| `TR-CRS-M1-00021-0021` | `CRS-M1-00021` | SCOPE | `SCOPE` | 非行为／Profile 义务 USE 保持为范围或适用性约束。 |
| `TR-CRS-M1-00022-0022` | `CRS-M1-00022` | INTERFACE | `IF_TFTP` | DO-NOT-FAIL-TRANSFER-FOR-UNIMPLEMENTED-OPTION 的 TFTP 接口前提。 |
| `TR-CRS-M1-00023-0023` | `CRS-M1-00023` | INTERFACE | `IF_TFTP` | ABSENT-AFTER-BOUNDARY 的 TFTP 接口前提。 |
| `TR-CRS-M1-00024-0024` | `CRS-M1-00024` | INTERFACE | `IF_TFTP` | TRANSFER 的 TFTP 接口前提。 |
| `TR-CRS-M1-00025-0025` | `CRS-M1-00025` | INTERFACE | `IF_TFTP` | USE-WELL-KNOWN-PORT 的 TFTP 接口前提。 |
| `TR-CRS-M1-00026-0026` | `CRS-M1-00026` | SCOPE | `SCOPE` | 非行为／Profile 义务 USE 保持为范围或适用性约束。 |
| `TR-CRS-M1-00027-0027` | `CRS-M1-00027` | SCOPE | `SCOPE` | 非行为／Profile 义务 ENCODE 保持为范围或适用性约束。 |
| `TR-CRS-M1-00028-0028` | `CRS-M1-00028` | SCOPE | `SCOPE` | 非行为／Profile 义务 ENCODE 保持为范围或适用性约束。 |
| `TR-CRS-M1-00029-0029` | `CRS-M1-00029` | INTERFACE | `IF_TFTP` | REPORT-RESOURCE-UNAVAILABLE 的 TFTP 接口前提。 |
| `TR-CRS-M1-00030-0030` | `CRS-M1-00030` | INTERFACE | `IF_TFTP` | REPORT-RESOURCE-UNAVAILABLE 的 TFTP 接口前提。 |
| `TR-CRS-M1-00031-0031` | `CRS-M1-00031` | INTERFACE | `IF_TFTP` | TRANSFER 的 TFTP 接口前提。 |
| `TR-CRS-M1-00032-0032` | `CRS-M1-00032` | INTERFACE | `IF_TFTP` | ABORT-AND-RESTART-AFTER-DELAY 的 TFTP 接口前提。 |
| `TR-CRS-M1-00032-0033` | `CRS-M1-00032` | TIMING | `TIM-CRS-M1-00032` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00032-0034` | `CRS-M1-00032` | CLOCK | `CLK_WAIT` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00032-0454` | `CRS-M1-00032` | TRANSITION | `T_WAIT_FROM_UPL_FILE` | 迁移 T_WAIT_FROM_UPL_FILE 引用此义务。 |
| `TR-CRS-M1-00032-0455` | `CRS-M1-00032` | TRANSITION | `T_WAIT_FROM_UPL_LUR` | 迁移 T_WAIT_FROM_UPL_LUR 引用此义务。 |
| `TR-CRS-M1-00032-0456` | `CRS-M1-00032` | TRANSITION | `T_WAIT_FROM_INF_LCI` | 迁移 T_WAIT_FROM_INF_LCI 引用此义务。 |
| `TR-CRS-M1-00032-0457` | `CRS-M1-00032` | TRANSITION | `T_WAIT_FROM_INF_LCL` | 迁移 T_WAIT_FROM_INF_LCL 引用此义务。 |
| `TR-CRS-M1-00032-0458` | `CRS-M1-00032` | TRANSITION | `T_WAIT_RETRY_UPL_FILE` | 迁移 T_WAIT_RETRY_UPL_FILE 引用此义务。 |
| `TR-CRS-M1-00032-0459` | `CRS-M1-00032` | TRANSITION | `T_WAIT_RETRY_UPL_LUR` | 迁移 T_WAIT_RETRY_UPL_LUR 引用此义务。 |
| `TR-CRS-M1-00032-0460` | `CRS-M1-00032` | TRANSITION | `T_WAIT_RETRY_INF_LCI` | 迁移 T_WAIT_RETRY_INF_LCI 引用此义务。 |
| `TR-CRS-M1-00032-0461` | `CRS-M1-00032` | TRANSITION | `T_WAIT_RETRY_INF_LCL` | 迁移 T_WAIT_RETRY_INF_LCL 引用此义务。 |
| `TR-CRS-M1-00033-0035` | `CRS-M1-00033` | INTERFACE | `IF_NETWORK` | 网络基础设施前提；能力未建立。 |
| `TR-CRS-M1-00034-0036` | `CRS-M1-00034` | INTERFACE | `IF_TFTP_BLOCKSIZE` | 块大小能力前提；RFC 2348 候选边另行记录。 |
| `TR-CRS-M1-00035-0037` | `CRS-M1-00035` | SCOPE | `SCOPE` | 非行为／Profile 义务 IMPLEMENT 保持为范围或适用性约束。 |
| `TR-CRS-M1-00036-0038` | `CRS-M1-00036` | INTERFACE | `IF_TFTP_BLOCKSIZE` | 块大小能力前提；RFC 2348 候选边另行记录。 |
| `TR-CRS-M1-00037-0039` | `CRS-M1-00037` | INTERFACE | `IF_NETWORK` | 网络基础设施前提；能力未建立。 |
| `TR-CRS-M1-00038-0040` | `CRS-M1-00038` | INTERFACE | `IF_TFTP` | COMPARE 的 TFTP 接口前提。 |
| `TR-CRS-M1-00039-0041` | `CRS-M1-00039` | INTERFACE | `IF_NETWORK` | 网络基础设施前提；能力未建立。 |
| `TR-CRS-M1-00040-0042` | `CRS-M1-00040` | INTERFACE | `IF_NETWORK` | 网络基础设施前提；能力未建立。 |
| `TR-CRS-M1-00041-0043` | `CRS-M1-00041` | INTERFACE | `IF_NETWORK` | 网络基础设施前提；能力未建立。 |
| `TR-CRS-M1-00042-0044` | `CRS-M1-00042` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00043-0045` | `CRS-M1-00043` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00044-0046` | `CRS-M1-00044` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00045-0047` | `CRS-M1-00045` | INTERFACE | `IF_NETWORK` | 网络基础设施前提；能力未建立。 |
| `TR-CRS-M1-00046-0048` | `CRS-M1-00046` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00047-0049` | `CRS-M1-00047` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00048-0050` | `CRS-M1-00048` | INTERFACE | `IF_TFTP` | TRANSFER 的 TFTP 接口前提。 |
| `TR-CRS-M1-00049-0051` | `CRS-M1-00049` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00050-0052` | `CRS-M1-00050` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00051-0053` | `CRS-M1-00051` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00052-0054` | `CRS-M1-00052` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00053-0055` | `CRS-M1-00053` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00054-0056` | `CRS-M1-00054` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00055-0057` | `CRS-M1-00055` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00056-0058` | `CRS-M1-00056` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00057-0059` | `CRS-M1-00057` | SCOPE | `SCOPE` | 非行为／Profile 义务 FAIL 保持为范围或适用性约束。 |
| `TR-CRS-M1-00058-0060` | `CRS-M1-00058` | INTERFACE | `IF_NETWORK` | 网络基础设施前提；能力未建立。 |
| `TR-CRS-M1-00059-0061` | `CRS-M1-00059` | INTERFACE | `IF_TFTP` | COMPLY 的 TFTP 接口前提。 |
| `TR-CRS-M1-00060-0062` | `CRS-M1-00060` | INTERFACE | `IF_TFTP` | SEND 的 TFTP 接口前提。 |
| `TR-CRS-M1-00061-0063` | `CRS-M1-00061` | INTERFACE | `IF_NETWORK` | 网络基础设施前提；能力未建立。 |
| `TR-CRS-M1-00062-0064` | `CRS-M1-00062` | SCOPE | `SCOPE` | 非行为／Profile 义务 ALLOW-ANY-ORDER-WHILE-SERIALIZING-PER-TARGET 保持为范围或适用性约束。 |
| `TR-CRS-M1-00063-0065` | `CRS-M1-00063` | SCOPE | `SCOPE` | 非行为／Profile 义务 ABORT 保持为范围或适用性约束。 |
| `TR-CRS-M1-00064-0066` | `CRS-M1-00064` | SCOPE | `SCOPE` | 非行为／Profile 义务 IMPLEMENT 保持为范围或适用性约束。 |
| `TR-CRS-M1-00065-0067` | `CRS-M1-00065` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00066-0068` | `CRS-M1-00066` | INTERFACE | `IF_TFTP` | TRANSFER 的 TFTP 接口前提。 |
| `TR-CRS-M1-00067-0069` | `CRS-M1-00067` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00068-0070` | `CRS-M1-00068` | INTERFACE | `IF_TFTP` | TRANSFER 的 TFTP 接口前提。 |
| `TR-CRS-M1-00069-0071` | `CRS-M1-00069` | INTERFACE | `IF_NETWORK` | 网络基础设施前提；能力未建立。 |
| `TR-CRS-M1-00070-0072` | `CRS-M1-00070` | INTERFACE | `IF_NETWORK` | 网络基础设施前提；能力未建立。 |
| `TR-CRS-M1-00071-0073` | `CRS-M1-00071` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00072-0074` | `CRS-M1-00072` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00073-0075` | `CRS-M1-00073` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00074-0076` | `CRS-M1-00074` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00075-0077` | `CRS-M1-00075` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00076-0078` | `CRS-M1-00076` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00077-0079` | `CRS-M1-00077` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00078-0080` | `CRS-M1-00078` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00079-0081` | `CRS-M1-00079` | TRANSITION | `T_UPL_LUR_XFER` | UPLOAD 列表文件义务落在 LUR 阶段。 |
| `TR-CRS-M1-00080-0082` | `CRS-M1-00080` | TRANSITION | `T_UPL_LUS_XFER` | UPLOAD 状态义务落在 LUS 阶段。 |
| `TR-CRS-M1-00081-0083` | `CRS-M1-00081` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00082-0084` | `CRS-M1-00082` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00083-0085` | `CRS-M1-00083` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00084-0086` | `CRS-M1-00084` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00085-0087` | `CRS-M1-00085` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00086-0088` | `CRS-M1-00086` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00087-0089` | `CRS-M1-00087` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00088-0090` | `CRS-M1-00088` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00089-0091` | `CRS-M1-00089` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00090-0092` | `CRS-M1-00090` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00091-0093` | `CRS-M1-00091` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00092-0094` | `CRS-M1-00092` | SCOPE | `SCOPE` | 非行为／Profile 义务 ABORT 保持为范围或适用性约束。 |
| `TR-CRS-M1-00093-0095` | `CRS-M1-00093` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00094-0096` | `CRS-M1-00094` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00094-0097` | `CRS-M1-00094` | TIMING | `TIM-CRS-M1-00094` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00094-0098` | `CRS-M1-00094` | CLOCK | `CLK_DLP` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00095-0099` | `CRS-M1-00095` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00096-0100` | `CRS-M1-00096` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00097-0101` | `CRS-M1-00097` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00097-0102` | `CRS-M1-00097` | TIMING | `TIM-CRS-M1-00097` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00097-0103` | `CRS-M1-00097` | CLOCK | `CLK_DLP` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00098-0104` | `CRS-M1-00098` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00098-0105` | `CRS-M1-00098` | TIMING | `TIM-CRS-M1-00098` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00098-0106` | `CRS-M1-00098` | CLOCK | `CLK_DLP` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00099-0107` | `CRS-M1-00099` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00099-0108` | `CRS-M1-00099` | TIMING | `TIM-CRS-M1-00099` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00099-0109` | `CRS-M1-00099` | CLOCK | `CLK_EXCEPTION` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00099-0452` | `CRS-M1-00099` | TRANSITION | `T_ENTER_UPL_EXC` | 迁移 T_ENTER_UPL_EXC 引用此义务。 |
| `TR-CRS-M1-00099-0453` | `CRS-M1-00099` | TRANSITION | `T_ENTER_INF_EXC` | 迁移 T_ENTER_INF_EXC 引用此义务。 |
| `TR-CRS-M1-00100-0110` | `CRS-M1-00100` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00100-0111` | `CRS-M1-00100` | TIMING | `TIM-CRS-M1-00100` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00100-0112` | `CRS-M1-00100` | CLOCK | `CLK_EXCEPTION` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00101-0113` | `CRS-M1-00101` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00101-0114` | `CRS-M1-00101` | TIMING | `TIM-CRS-M1-00101` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00101-0115` | `CRS-M1-00101` | CLOCK | `CLK_EXCEPTION` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00101-0449` | `CRS-M1-00101` | TRANSITION | `T_UPL_EXC_TO` | 迁移 T_UPL_EXC_TO 引用此义务。 |
| `TR-CRS-M1-00101-0451` | `CRS-M1-00101` | TRANSITION | `T_INF_EXC_TO` | 迁移 T_INF_EXC_TO 引用此义务。 |
| `TR-CRS-M1-00102-0116` | `CRS-M1-00102` | TRANSITION | `T_UPL_LUS_XFER` | UPLOAD 状态义务落在 LUS 阶段。 |
| `TR-CRS-M1-00102-0117` | `CRS-M1-00102` | TIMING | `TIM-CRS-M1-00102` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00102-0118` | `CRS-M1-00102` | CLOCK | `CLK_DLP` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00103-0119` | `CRS-M1-00103` | TRANSITION | `T_UPL_LUS_XFER` | UPLOAD 状态义务落在 LUS 阶段。 |
| `TR-CRS-M1-00104-0120` | `CRS-M1-00104` | TRANSITION | `T_UPL_LUS_XFER` | UPLOAD 状态义务落在 LUS 阶段。 |
| `TR-CRS-M1-00105-0121` | `CRS-M1-00105` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00106-0122` | `CRS-M1-00106` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00106-0123` | `CRS-M1-00106` | TIMING | `TIM-CRS-M1-00106` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00106-0124` | `CRS-M1-00106` | CLOCK | `CLK_EXCEPTION` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00107-0125` | `CRS-M1-00107` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00107-0126` | `CRS-M1-00107` | TIMING | `TIM-CRS-M1-00107` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00107-0127` | `CRS-M1-00107` | CLOCK | `CLK_EXCEPTION` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00108-0128` | `CRS-M1-00108` | TRANSITION | `T_UPL_LUS_XFER` | UPLOAD 状态义务落在 LUS 阶段。 |
| `TR-CRS-M1-00108-0129` | `CRS-M1-00108` | TIMING | `TIM-CRS-M1-00108` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00108-0130` | `CRS-M1-00108` | CLOCK | `CLK_EXCEPTION` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00108-0450` | `CRS-M1-00108` | TRANSITION | `T_UPL_EXC_TO` | 迁移 T_UPL_EXC_TO 引用此义务。 |
| `TR-CRS-M1-00109-0131` | `CRS-M1-00109` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00110-0132` | `CRS-M1-00110` | SCOPE | `SCOPE` | 非行为／Profile 义务 ABORT 保持为范围或适用性约束。 |
| `TR-CRS-M1-00111-0133` | `CRS-M1-00111` | SCOPE | `SCOPE` | 非行为／Profile 义务 ABORT 保持为范围或适用性约束。 |
| `TR-CRS-M1-00112-0134` | `CRS-M1-00112` | SCOPE | `SCOPE` | 非行为／Profile 义务 ABORT 保持为范围或适用性约束。 |
| `TR-CRS-M1-00113-0135` | `CRS-M1-00113` | SCOPE | `SCOPE` | 非行为／Profile 义务 ABORT 保持为范围或适用性约束。 |
| `TR-CRS-M1-00114-0136` | `CRS-M1-00114` | SCOPE | `SCOPE` | 非行为／Profile 义务 ABORT 保持为范围或适用性约束。 |
| `TR-CRS-M1-00115-0137` | `CRS-M1-00115` | INTERFACE | `IF_NETWORK` | 网络基础设施前提；能力未建立。 |
| `TR-CRS-M1-00116-0138` | `CRS-M1-00116` | SCOPE | `SCOPE` | 非行为／Profile 义务 IMPLEMENT 保持为范围或适用性约束。 |
| `TR-CRS-M1-00117-0139` | `CRS-M1-00117` | INTERFACE | `IF_NETWORK` | 网络基础设施前提；能力未建立。 |
| `TR-CRS-M1-00118-0140` | `CRS-M1-00118` | INTERFACE | `IF_NETWORK` | 网络基础设施前提；能力未建立。 |
| `TR-CRS-M1-00119-0141` | `CRS-M1-00119` | SCOPE | `SCOPE` | 非行为／Profile 义务 ABORT 保持为范围或适用性约束。 |
| `TR-CRS-M1-00120-0142` | `CRS-M1-00120` | SCOPE | `SCOPE` | 非行为／Profile 义务 ABORT 保持为范围或适用性约束。 |
| `TR-CRS-M1-00121-0143` | `CRS-M1-00121` | SCOPE | `SCOPE` | 非行为／Profile 义务 ENCODE 保持为范围或适用性约束。 |
| `TR-CRS-M1-00122-0144` | `CRS-M1-00122` | SCOPE | `SCOPE` | 非行为／Profile 义务 ENCODE 保持为范围或适用性约束。 |
| `TR-CRS-M1-00123-0145` | `CRS-M1-00123` | SCOPE | `SCOPE` | 非行为／Profile 义务 ENCODE 保持为范围或适用性约束。 |
| `TR-CRS-M1-00124-0146` | `CRS-M1-00124` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00125-0147` | `CRS-M1-00125` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00126-0148` | `CRS-M1-00126` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00127-0149` | `CRS-M1-00127` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00128-0150` | `CRS-M1-00128` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00129-0151` | `CRS-M1-00129` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00130-0152` | `CRS-M1-00130` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00131-0153` | `CRS-M1-00131` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00132-0154` | `CRS-M1-00132` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00133-0155` | `CRS-M1-00133` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00134-0156` | `CRS-M1-00134` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00135-0157` | `CRS-M1-00135` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00136-0158` | `CRS-M1-00136` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00137-0159` | `CRS-M1-00137` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00138-0160` | `CRS-M1-00138` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00139-0161` | `CRS-M1-00139` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00140-0162` | `CRS-M1-00140` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00141-0163` | `CRS-M1-00141` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00142-0164` | `CRS-M1-00142` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00143-0165` | `CRS-M1-00143` | TRANSITION | `T_UPL_LUR_XFER` | UPLOAD 列表文件义务落在 LUR 阶段。 |
| `TR-CRS-M1-00144-0166` | `CRS-M1-00144` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00145-0167` | `CRS-M1-00145` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00146-0168` | `CRS-M1-00146` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00147-0169` | `CRS-M1-00147` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00148-0170` | `CRS-M1-00148` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00149-0171` | `CRS-M1-00149` | TRANSITION | `T_UPL_LUS_XFER` | UPLOAD 状态义务落在 LUS 阶段。 |
| `TR-CRS-M1-00150-0172` | `CRS-M1-00150` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00151-0173` | `CRS-M1-00151` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00152-0174` | `CRS-M1-00152` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00153-0175` | `CRS-M1-00153` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00154-0176` | `CRS-M1-00154` | TRANSITION | `T_UPL_LUS_XFER` | UPLOAD 状态义务落在 LUS 阶段。 |
| `TR-CRS-M1-00155-0177` | `CRS-M1-00155` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00156-0178` | `CRS-M1-00156` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00157-0179` | `CRS-M1-00157` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00158-0180` | `CRS-M1-00158` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00159-0181` | `CRS-M1-00159` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00160-0182` | `CRS-M1-00160` | TRANSITION | `T_UPL_LUS_XFER` | UPLOAD 状态义务落在 LUS 阶段。 |
| `TR-CRS-M1-00161-0183` | `CRS-M1-00161` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00162-0184` | `CRS-M1-00162` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00163-0185` | `CRS-M1-00163` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00164-0186` | `CRS-M1-00164` | TRANSITION | `T_UPL_FILE_XFER` | LUR 之后的 UPLOAD 文件线程义务。 |
| `TR-CRS-M1-00165-0187` | `CRS-M1-00165` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00166-0188` | `CRS-M1-00166` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00167-0189` | `CRS-M1-00167` | INTERFACE | `IF_TFTP` | RETRY 的 TFTP 接口前提。 |
| `TR-CRS-M1-00168-0190` | `CRS-M1-00168` | INTERFACE | `IF_TFTP` | TRANSFER 的 TFTP 接口前提。 |
| `TR-CRS-M1-00168-0191` | `CRS-M1-00168` | TIMING | `TIM-CRS-M1-00168` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00168-0192` | `CRS-M1-00168` | CLOCK | `CLK_TFTP` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00169-0193` | `CRS-M1-00169` | SCOPE | `SCOPE` | 非行为／Profile 义务 ACKNOWLEDGE 保持为范围或适用性约束。 |
| `TR-CRS-M1-00170-0194` | `CRS-M1-00170` | INTERFACE | `IF_TFTP` | RETRY 的 TFTP 接口前提。 |
| `TR-CRS-M1-00171-0195` | `CRS-M1-00171` | INTERFACE | `IF_TFTP` | RETRY 的 TFTP 接口前提。 |
| `TR-CRS-M1-00172-0196` | `CRS-M1-00172` | SCOPE | `SCOPE` | 非行为／Profile 义务 PROVIDE 保持为范围或适用性约束。 |
| `TR-CRS-M1-00173-0197` | `CRS-M1-00173` | INTERFACE | `IF_TFTP` | RETRY 的 TFTP 接口前提。 |
| `TR-CRS-M1-00174-0198` | `CRS-M1-00174` | SCOPE | `SCOPE` | 非行为／Profile 义务 DECLARE-FATAL-ERROR 保持为范围或适用性约束。 |
| `TR-CRS-M1-00175-0199` | `CRS-M1-00175` | SCOPE | `SCOPE` | 非行为／Profile 义务 FAIL 保持为范围或适用性约束。 |
| `TR-CRS-M1-00176-0200` | `CRS-M1-00176` | SCOPE | `SCOPE` | 非行为／Profile 义务 ADJUST-UPWARD 保持为范围或适用性约束。 |
| `TR-CRS-M1-00176-0201` | `CRS-M1-00176` | TIMING | `TIM-CRS-M1-00176` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00176-0202` | `CRS-M1-00176` | CLOCK | `CLK_DLP` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00177-0203` | `CRS-M1-00177` | SCOPE | `SCOPE` | 非行为／Profile 义务 SET-CONSTANT 保持为范围或适用性约束。 |
| `TR-CRS-M1-00177-0204` | `CRS-M1-00177` | TIMING | `TIM-CRS-M1-00177` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00177-0205` | `CRS-M1-00177` | CLOCK | `CLK_TFTP` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00177-0442` | `CRS-M1-00177` | TRANSITION | `T_INF_TFTP_TO` | 迁移 T_INF_TFTP_TO 引用此义务。 |
| `TR-CRS-M1-00177-0443` | `CRS-M1-00177` | TRANSITION | `T_UPL_TFTP_TO` | 迁移 T_UPL_TFTP_TO 引用此义务。 |
| `TR-CRS-M1-00177-0444` | `CRS-M1-00177` | TRANSITION | `T_UPL_LUR_TFTP_TO` | 迁移 T_UPL_LUR_TFTP_TO 引用此义务。 |
| `TR-CRS-M1-00177-0445` | `CRS-M1-00177` | TRANSITION | `T_UPL_FILE_TFTP_TO` | 迁移 T_UPL_FILE_TFTP_TO 引用此义务。 |
| `TR-CRS-M1-00178-0206` | `CRS-M1-00178` | INTERFACE | `IF_TFTP` | LIMIT-SINGLE-TFTP-PACKET-TRANSMISSION-DURATION 的 TFTP 接口前提。 |
| `TR-CRS-M1-00178-0207` | `CRS-M1-00178` | TIMING | `TIM-CRS-M1-00178` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00178-0208` | `CRS-M1-00178` | CLOCK | `CLK_TFTP` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00179-0209` | `CRS-M1-00179` | INTERFACE | `IF_TFTP` | LIMIT-TFTP-PACKET-PROCESSING-DURATION 的 TFTP 接口前提。 |
| `TR-CRS-M1-00179-0210` | `CRS-M1-00179` | TIMING | `TIM-CRS-M1-00179` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00179-0211` | `CRS-M1-00179` | CLOCK | `CLK_DLP` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00180-0212` | `CRS-M1-00180` | INTERFACE | `IF_TFTP` | RETRY 的 TFTP 接口前提。 |
| `TR-CRS-M1-00181-0213` | `CRS-M1-00181` | INTERFACE | `IF_TFTP` | RETRY 的 TFTP 接口前提。 |
| `TR-CRS-M1-00182-0214` | `CRS-M1-00182` | SCOPE | `SCOPE` | 非行为／Profile 义务 ENCODE 保持为范围或适用性约束。 |
| `TR-CRS-M1-00183-0215` | `CRS-M1-00183` | INTERFACE | `IF_TFTP` | SEND 的 TFTP 接口前提。 |
| `TR-CRS-M1-00184-0216` | `CRS-M1-00184` | INTERFACE | `IF_TFTP` | TRANSFER 的 TFTP 接口前提。 |
| `TR-CRS-M1-00184-0217` | `CRS-M1-00184` | TIMING | `TIM-CRS-M1-00184` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00184-0218` | `CRS-M1-00184` | CLOCK | `CLK_DLP` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00185-0219` | `CRS-M1-00185` | SCOPE | `SCOPE` | 非行为／Profile 义务 ADJUST-UPWARD 保持为范围或适用性约束。 |
| `TR-CRS-M1-00185-0220` | `CRS-M1-00185` | TIMING | `TIM-CRS-M1-00185` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00185-0221` | `CRS-M1-00185` | CLOCK | `CLK_DLP` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00186-0222` | `CRS-M1-00186` | SCOPE | `SCOPE` | 非行为／Profile 义务 DO-NOT-PRODUCE-LCS-DURING-TIMELY-LCI-LCL-SEQUENCE 保持为范围或适用性约束。 |
| `TR-CRS-M1-00186-0223` | `CRS-M1-00186` | TIMING | `TIM-CRS-M1-00186` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00186-0224` | `CRS-M1-00186` | CLOCK | `CLK_DLP` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00187-0225` | `CRS-M1-00187` | SCOPE | `SCOPE` | 非行为／Profile 义务 PROVIDE 保持为范围或适用性约束。 |
| `TR-CRS-M1-00187-0226` | `CRS-M1-00187` | TIMING | `TIM-CRS-M1-00187` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00187-0227` | `CRS-M1-00187` | CLOCK | `CLK_DLP` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00187-0446` | `CRS-M1-00187` | TRANSITION | `T_UPL_DLP_TO` | 迁移 T_UPL_DLP_TO 引用此义务。 |
| `TR-CRS-M1-00187-0447` | `CRS-M1-00187` | TRANSITION | `T_UPL_LUR_DLP_TO` | 迁移 T_UPL_LUR_DLP_TO 引用此义务。 |
| `TR-CRS-M1-00188-0228` | `CRS-M1-00188` | INTERFACE | `IF_TFTP` | BOUND-INTER-TRANSFER-DURATION-BY-DLP-EQUATION 的 TFTP 接口前提。 |
| `TR-CRS-M1-00188-0229` | `CRS-M1-00188` | TIMING | `TIM-CRS-M1-00188` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00188-0230` | `CRS-M1-00188` | CLOCK | `CLK_DLP` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00188-0448` | `CRS-M1-00188` | TRANSITION | `T_UPL_LUR_DLP_TO` | 迁移 T_UPL_LUR_DLP_TO 引用此义务。 |
| `TR-CRS-M1-00189-0231` | `CRS-M1-00189` | INTERFACE | `IF_TFTP` | RETRY 的 TFTP 接口前提。 |
| `TR-CRS-M1-00190-0232` | `CRS-M1-00190` | INTERFACE | `IF_NETWORK` | 网络基础设施前提；能力未建立。 |
| `TR-CRS-M1-00191-0233` | `CRS-M1-00191` | OBJECT-CONSTRAINT | `OBJ-MINIMUM-ARINC-665-COMPATIBILITY-CAPABILITIES-IMPLEMENT-REQUIRED-ARINC-665-CA-CRS-M1-00191` | 665／数据对象谓词 OBJ-MINIMUM-ARINC-665-COMPATIBILITY-CAPABILITIES-IMPLEMENT-REQUIRED-ARINC-665-CA-CRS-M1-00191。 |
| `TR-CRS-M1-00192-0234` | `CRS-M1-00192` | OBJECT-CONSTRAINT | `OBJ-ARINC-665-SHOULD-MODALITY-TREAT-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY-CRS-M1-00192` | 665／数据对象谓词 OBJ-ARINC-665-SHOULD-MODALITY-TREAT-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY-CRS-M1-00192。 |
| `TR-CRS-M1-00193-0235` | `CRS-M1-00193` | OBJECT-CONSTRAINT | `OBJ-ARINC-665-MAY-MODALITY-TREAT-MAY-AS-OPTIONAL-CAPABILITY-CRS-M1-00193` | 665／数据对象谓词 OBJ-ARINC-665-MAY-MODALITY-TREAT-MAY-AS-OPTIONAL-CAPABILITY-CRS-M1-00193。 |
| `TR-CRS-M1-00194-0236` | `CRS-M1-00194` | OBJECT-CONSTRAINT | `OBJ-OPTIONAL-ARINC-665-CAPABILITY-CONDITIONALLY-IMPLEMENT-OPTIONAL-CAPABILITY-AS-CRS-M1-00194` | 665／数据对象谓词 OBJ-OPTIONAL-ARINC-665-CAPABILITY-CONDITIONALLY-IMPLEMENT-OPTIONAL-CAPABILITY-AS-CRS-M1-00194。 |
| `TR-CRS-M1-00195-0237` | `CRS-M1-00195` | OBJECT-CONSTRAINT | `OBJ-DATA-FIELD-TYPE-INTERPRET-FIELDS-AS-NUMERIC-BY-DEFAULT-CRS-M1-00195` | 665／数据对象谓词 OBJ-DATA-FIELD-TYPE-INTERPRET-FIELDS-AS-NUMERIC-BY-DEFAULT-CRS-M1-00195。 |
| `TR-CRS-M1-00196-0238` | `CRS-M1-00196` | OBJECT-CONSTRAINT | `OBJ-ARINC-665-FILE-PROHIBIT-UNDEFINED-FIELD-INSERTION-CRS-M1-00196` | 665／数据对象谓词 OBJ-ARINC-665-FILE-PROHIBIT-UNDEFINED-FIELD-INSERTION-CRS-M1-00196。 |
| `TR-CRS-M1-00197-0239` | `CRS-M1-00197` | OBJECT-CONSTRAINT | `OBJ-FILE-VERSION-COMPATIBILITY-ENCODE-CRS-M1-00197` | 665／数据对象谓词 OBJ-FILE-VERSION-COMPATIBILITY-ENCODE-CRS-M1-00197。 |
| `TR-CRS-M1-00198-0240` | `CRS-M1-00198` | OBJECT-CONSTRAINT | `OBJ-TARGET-HARDWARE-ID-MANUFACTURER-IDENTIFIER-PREFIX-TARGET-HARDWARE-ID-WITH-MA-CRS-M1-00198` | 665／数据对象谓词 OBJ-TARGET-HARDWARE-ID-MANUFACTURER-IDENTIFIER-PREFIX-TARGET-HARDWARE-ID-WITH-MA-CRS-M1-00198。 |
| `TR-CRS-M1-00199-0241` | `CRS-M1-00199` | OBJECT-CONSTRAINT | `OBJ-MANUFACTURER-IDENTIFIER-ASSIGN-CRS-M1-00199` | 665／数据对象谓词 OBJ-MANUFACTURER-IDENTIFIER-ASSIGN-CRS-M1-00199。 |
| `TR-CRS-M1-00200-0242` | `CRS-M1-00200` | OBJECT-CONSTRAINT | `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ASSIGN-GENERIC-TARGET-HARDWARE-ID-CRS-M1-00200` | 665／数据对象谓词 OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ASSIGN-GENERIC-TARGET-HARDWARE-ID-CRS-M1-00200。 |
| `TR-CRS-M1-00201-0243` | `CRS-M1-00201` | OBJECT-CONSTRAINT | `OBJ-REDUNDANT-CHANNEL-LOADS-DISTRIBUTE-REDUNDANT-LOADS-INTERNALLY-CRS-M1-00201` | 665／数据对象谓词 OBJ-REDUNDANT-CHANNEL-LOADS-DISTRIBUTE-REDUNDANT-LOADS-INTERNALLY-CRS-M1-00201。 |
| `TR-CRS-M1-00202-0244` | `CRS-M1-00202` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-ENSURE-CARDINALITY-CRS-M1-00202` | 665／数据对象谓词 OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-ENSURE-CARDINALITY-CRS-M1-00202。 |
| `TR-CRS-M1-00203-0245` | `CRS-M1-00203` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-COORDINATE-CRS-M1-00203` | 665／数据对象谓词 OBJ-LOAD-PART-NUMBER-COORDINATE-CRS-M1-00203。 |
| `TR-CRS-M1-00204-0246` | `CRS-M1-00204` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-ASSIGN-CRS-M1-00204` | 665／数据对象谓词 OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-ASSIGN-CRS-M1-00204。 |
| `TR-CRS-M1-00205-0247` | `CRS-M1-00205` | OBJECT-CONSTRAINT | `OBJ-LOADABLE-SOFTWARE-PART-NUMBER-FORMAT-CRS-M1-00205` | 665／数据对象谓词 OBJ-LOADABLE-SOFTWARE-PART-NUMBER-FORMAT-CRS-M1-00205。 |
| `TR-CRS-M1-00206-0248` | `CRS-M1-00206` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-EXCLUDE-EMBEDDED-BLANKS-CRS-M1-00206` | 665／数据对象谓词 OBJ-LOAD-PART-NUMBER-EXCLUDE-EMBEDDED-BLANKS-CRS-M1-00206。 |
| `TR-CRS-M1-00207-0249` | `CRS-M1-00207` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-DO-NOT-ENFORCE-SPECIFIC-PART-NUMBER-FORMAT-CRS-M1-00207` | 665／数据对象谓词 OBJ-LOAD-PART-NUMBER-DO-NOT-ENFORCE-SPECIFIC-PART-NUMBER-FORMAT-CRS-M1-00207。 |
| `TR-CRS-M1-00208-0250` | `CRS-M1-00208` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-PROCESS-NONCONFORMING-PART-NUMBER-FORMATS-CRS-M1-00208` | 665／数据对象谓词 OBJ-LOAD-PART-NUMBER-PROCESS-NONCONFORMING-PART-NUMBER-FORMATS-CRS-M1-00208。 |
| `TR-CRS-M1-00209-0251` | `CRS-M1-00209` | OBJECT-CONSTRAINT | `OBJ-NETWORK-INTERFACE-DESIGN-CRS-M1-00209` | 665／数据对象谓词 OBJ-NETWORK-INTERFACE-DESIGN-CRS-M1-00209。 |
| `TR-CRS-M1-00210-0252` | `CRS-M1-00210` | OBJECT-CONSTRAINT | `OBJ-NETWORK-INTERFACE-FORMAT-CRS-M1-00210` | 665／数据对象谓词 OBJ-NETWORK-INTERFACE-FORMAT-CRS-M1-00210。 |
| `TR-CRS-M1-00211-0253` | `CRS-M1-00211` | OBJECT-CONSTRAINT | `OBJ-ATA-PART-NUMBER-DELIMITERS-SEPARATE-DELIMITERS-FROM-LETTERS-CRS-M1-00211` | 665／数据对象谓词 OBJ-ATA-PART-NUMBER-DELIMITERS-SEPARATE-DELIMITERS-FROM-LETTERS-CRS-M1-00211。 |
| `TR-CRS-M1-00212-0254` | `CRS-M1-00212` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-ENCODE-CRS-M1-00212` | 665／数据对象谓词 OBJ-LOAD-PART-NUMBER-ENCODE-CRS-M1-00212。 |
| `TR-CRS-M1-00213-0255` | `CRS-M1-00213` | OBJECT-CONSTRAINT | `OBJ-ATA-PART-NUMBER-CHARACTER-SET-EXCLUDE-AMBIGUOUS-LETTER-O-CRS-M1-00213` | 665／数据对象谓词 OBJ-ATA-PART-NUMBER-CHARACTER-SET-EXCLUDE-AMBIGUOUS-LETTER-O-CRS-M1-00213。 |
| `TR-CRS-M1-00214-0256` | `CRS-M1-00214` | OBJECT-CONSTRAINT | `OBJ-MMM-CODE-INTERPRET-CONFUSED-MMM-CHARACTERS-AS-ALPHABETIC-CRS-M1-00214` | 665／数据对象谓词 OBJ-MMM-CODE-INTERPRET-CONFUSED-MMM-CHARACTERS-AS-ALPHABETIC-CRS-M1-00214。 |
| `TR-CRS-M1-00215-0257` | `CRS-M1-00215` | OBJECT-CONSTRAINT | `OBJ-CHECK-CHARACTERS-COMPUTE-CRS-M1-00215` | 665／数据对象谓词 OBJ-CHECK-CHARACTERS-COMPUTE-CRS-M1-00215。 |
| `TR-CRS-M1-00216-0258` | `CRS-M1-00216` | OBJECT-CONSTRAINT | `OBJ-HEADER-FILE-SOFTWARE-PART-FORMAT-CRS-M1-00216` | 665／数据对象谓词 OBJ-HEADER-FILE-SOFTWARE-PART-FORMAT-CRS-M1-00216。 |
| `TR-CRS-M1-00217-0259` | `CRS-M1-00217` | OBJECT-CONSTRAINT | `OBJ-HEADER-FILE-SOFTWARE-PART-ENCODE-CRS-M1-00217` | 665／数据对象谓词 OBJ-HEADER-FILE-SOFTWARE-PART-ENCODE-CRS-M1-00217。 |
| `TR-CRS-M1-00218-0260` | `CRS-M1-00218` | OBJECT-CONSTRAINT | `OBJ-HEADER-FILE-DEFINE-CRS-M1-00218` | 665／数据对象谓词 OBJ-HEADER-FILE-DEFINE-CRS-M1-00218。 |
| `TR-CRS-M1-00219-0261` | `CRS-M1-00219` | OBJECT-CONSTRAINT | `OBJ-BINARY-FIELD-ENCODING-ENCODE-CRS-M1-00219` | 665／数据对象谓词 OBJ-BINARY-FIELD-ENCODING-ENCODE-CRS-M1-00219。 |
| `TR-CRS-M1-00220-0262` | `CRS-M1-00220` | OBJECT-CONSTRAINT | `OBJ-OPERATION-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00220` | 665／数据对象谓词 OBJ-OPERATION-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00220。 |
| `TR-CRS-M1-00221-0263` | `CRS-M1-00221` | OBJECT-CONSTRAINT | `OBJ-BINARY-FIELD-ENCODING-ENCODE-CRS-M1-00221` | 665／数据对象谓词 OBJ-BINARY-FIELD-ENCODING-ENCODE-CRS-M1-00221。 |
| `TR-CRS-M1-00222-0264` | `CRS-M1-00222` | OBJECT-CONSTRAINT | `OBJ-TARGET-HARDWARE-ID-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00222` | 665／数据对象谓词 OBJ-TARGET-HARDWARE-ID-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00222。 |
| `TR-CRS-M1-00223-0265` | `CRS-M1-00223` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-IMPLEMENT-CRS-M1-00223` | 665／数据对象谓词 OBJ-LOAD-PART-NUMBER-SOFTWARE-PART-IMPLEMENT-CRS-M1-00223。 |
| `TR-CRS-M1-00224-0266` | `CRS-M1-00224` | OBJECT-CONSTRAINT | `OBJ-NETWORK-INTERFACE-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00224` | 665／数据对象谓词 OBJ-NETWORK-INTERFACE-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00224。 |
| `TR-CRS-M1-00225-0267` | `CRS-M1-00225` | OBJECT-CONSTRAINT | `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ENSURE-UNIQUE-CRS-M1-00225` | 665／数据对象谓词 OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ENSURE-UNIQUE-CRS-M1-00225。 |
| `TR-CRS-M1-00226-0268` | `CRS-M1-00226` | OBJECT-CONSTRAINT | `OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ENCODE-CRS-M1-00226` | 665／数据对象谓词 OBJ-SOFTWARE-PART-TARGET-HARDWARE-ID-ENCODE-CRS-M1-00226。 |
| `TR-CRS-M1-00227-0269` | `CRS-M1-00227` | OBJECT-CONSTRAINT | `OBJ-TARGET-HARDWARE-ID-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00227` | 665／数据对象谓词 OBJ-TARGET-HARDWARE-ID-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00227。 |
| `TR-CRS-M1-00228-0270` | `CRS-M1-00228` | OBJECT-CONSTRAINT | `OBJ-DATA-FILE-CONSTRAIN-CRS-M1-00228` | 665／数据对象谓词 OBJ-DATA-FILE-CONSTRAIN-CRS-M1-00228。 |
| `TR-CRS-M1-00229-0271` | `CRS-M1-00229` | OBJECT-CONSTRAINT | `OBJ-DATA-FILE-SET-ZERO-CRS-M1-00229` | 665／数据对象谓词 OBJ-DATA-FILE-SET-ZERO-CRS-M1-00229。 |
| `TR-CRS-M1-00230-0272` | `CRS-M1-00230` | OBJECT-CONSTRAINT | `OBJ-DATA-FILE-FORMAT-CRS-M1-00230` | 665／数据对象谓词 OBJ-DATA-FILE-FORMAT-CRS-M1-00230。 |
| `TR-CRS-M1-00231-0273` | `CRS-M1-00231` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00232-0274` | `CRS-M1-00232` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00233-0275` | `CRS-M1-00233` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00234-0276` | `CRS-M1-00234` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00235-0277` | `CRS-M1-00235` | OBJECT-CONSTRAINT | `OBJ-NETWORK-INTERFACE-ENCODE-CRS-M1-00235` | 665／数据对象谓词 OBJ-NETWORK-INTERFACE-ENCODE-CRS-M1-00235。 |
| `TR-CRS-M1-00236-0278` | `CRS-M1-00236` | OBJECT-CONSTRAINT | `OBJ-NETWORK-INTERFACE-IMPLEMENT-CRS-M1-00236` | 665／数据对象谓词 OBJ-NETWORK-INTERFACE-IMPLEMENT-CRS-M1-00236。 |
| `TR-CRS-M1-00237-0279` | `CRS-M1-00237` | OBJECT-CONSTRAINT | `OBJ-LOAD-PART-NUMBER-NETWORK-INTERFACE-ENCODE-CRS-M1-00237` | 665／数据对象谓词 OBJ-LOAD-PART-NUMBER-NETWORK-INTERFACE-ENCODE-CRS-M1-00237。 |
| `TR-CRS-M1-00238-0280` | `CRS-M1-00238` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00239-0281` | `CRS-M1-00239` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00240-0282` | `CRS-M1-00240` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00241-0283` | `CRS-M1-00241` | OBJECT-CONSTRAINT | `OBJ-HEADER-FILE-VALIDATE-CRS-M1-00241` | 665／数据对象谓词 OBJ-HEADER-FILE-VALIDATE-CRS-M1-00241。 |
| `TR-CRS-M1-00242-0284` | `CRS-M1-00242` | OBJECT-CONSTRAINT | `OBJ-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00242` | 665／数据对象谓词 OBJ-STATUS-CODE-CONDITIONAL-FIELD-ENCODE-CRS-M1-00242。 |
| `TR-CRS-M1-00243-0285` | `CRS-M1-00243` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00244-0286` | `CRS-M1-00244` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00245-0287` | `CRS-M1-00245` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00246-0288` | `CRS-M1-00246` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00247-0289` | `CRS-M1-00247` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00248-0290` | `CRS-M1-00248` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00249-0291` | `CRS-M1-00249` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00250-0292` | `CRS-M1-00250` | INTERFACE | `IF_INTEGRITY` | 完整性接口仍被 ARINC 645 阻塞。 |
| `TR-CRS-M1-00251-0293` | `CRS-M1-00251` | OBJECT-CONSTRAINT | `OBJ-DATA-FILE-SOFTWARE-PART-ENCODE-CRS-M1-00251` | 665／数据对象谓词 OBJ-DATA-FILE-SOFTWARE-PART-ENCODE-CRS-M1-00251。 |
| `TR-CRS-M1-00252-0294` | `CRS-M1-00252` | OBJECT-CONSTRAINT | `OBJ-SOFTWARE-PART-NETWORK-INTERFACE-ENCODE-CRS-M1-00252` | 665／数据对象谓词 OBJ-SOFTWARE-PART-NETWORK-INTERFACE-ENCODE-CRS-M1-00252。 |
| `TR-CRS-M1-00253-0295` | `CRS-M1-00253` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00254-0296` | `CRS-M1-00254` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00255-0297` | `CRS-M1-00255` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00256-0298` | `CRS-M1-00256` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00257-0299` | `CRS-M1-00257` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00258-0300` | `CRS-M1-00258` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00259-0301` | `CRS-M1-00259` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00260-0302` | `CRS-M1-00260` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00261-0303` | `CRS-M1-00261` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00262-0304` | `CRS-M1-00262` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00263-0305` | `CRS-M1-00263` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00264-0306` | `CRS-M1-00264` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00265-0307` | `CRS-M1-00265` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00266-0308` | `CRS-M1-00266` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00267-0309` | `CRS-M1-00267` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00268-0310` | `CRS-M1-00268` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00269-0311` | `CRS-M1-00269` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00270-0312` | `CRS-M1-00270` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00271-0313` | `CRS-M1-00271` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00272-0314` | `CRS-M1-00272` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00273-0315` | `CRS-M1-00273` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00274-0316` | `CRS-M1-00274` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00275-0317` | `CRS-M1-00275` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00276-0318` | `CRS-M1-00276` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00277-0319` | `CRS-M1-00277` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00278-0320` | `CRS-M1-00278` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00279-0321` | `CRS-M1-00279` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00280-0322` | `CRS-M1-00280` | SCOPE | `SCOPE` | 范围／延期服务／Profile 约束，不是文件变量替身。 |
| `TR-CRS-M1-00281-0323` | `CRS-M1-00281` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00282-0324` | `CRS-M1-00282` | FIELD-CONSTRAINT | `FC-LCI-FIELD-FILE-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LCI-FIELD-FILE-LENGTH。 |
| `TR-CRS-M1-00283-0325` | `CRS-M1-00283` | FIELD-CONSTRAINT | `FC-LCI-FIELD-PROTOCOL-VERSION` | 在具名协议文件字节上应用字段谓词 FC-LCI-FIELD-PROTOCOL-VERSION。 |
| `TR-CRS-M1-00284-0326` | `CRS-M1-00284` | FIELD-CONSTRAINT | `FC-LCI-FIELD-OPERATION-ACCEPTANCE-STATUS-CODE` | 在具名协议文件字节上应用字段谓词 FC-LCI-FIELD-OPERATION-ACCEPTANCE-STATUS-CODE。 |
| `TR-CRS-M1-00285-0327` | `CRS-M1-00285` | FIELD-CONSTRAINT | `FC-LCI-FIELD-STATUS-DESCRIPTION-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LCI-FIELD-STATUS-DESCRIPTION-LENGTH。 |
| `TR-CRS-M1-00286-0328` | `CRS-M1-00286` | FIELD-CONSTRAINT | `FC-LCI-FIELD-STATUS-DESCRIPTION` | 在具名协议文件字节上应用字段谓词 FC-LCI-FIELD-STATUS-DESCRIPTION。 |
| `TR-CRS-M1-00287-0329` | `CRS-M1-00287` | FIELD-CONSTRAINT | `FC-LCL-FIELD-FILE-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LCL-FIELD-FILE-LENGTH。 |
| `TR-CRS-M1-00288-0330` | `CRS-M1-00288` | FIELD-CONSTRAINT | `FC-LCL-FIELD-PROTOCOL-VERSION` | 在具名协议文件字节上应用字段谓词 FC-LCL-FIELD-PROTOCOL-VERSION。 |
| `TR-CRS-M1-00289-0331` | `CRS-M1-00289` | FIELD-CONSTRAINT | `FC-LCL-FIELD-NUMBER-OF-TARGET-HARDWARE` | 在具名协议文件字节上应用字段谓词 FC-LCL-FIELD-NUMBER-OF-TARGET-HARDWARE。 |
| `TR-CRS-M1-00290-0332` | `CRS-M1-00290` | FIELD-CONSTRAINT | `FC-LCL-FIELD-LITERAL-NAME-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LCL-FIELD-LITERAL-NAME-LENGTH。 |
| `TR-CRS-M1-00291-0333` | `CRS-M1-00291` | FIELD-CONSTRAINT | `FC-LCL-FIELD-LITERAL-NAME` | 在具名协议文件字节上应用字段谓词 FC-LCL-FIELD-LITERAL-NAME。 |
| `TR-CRS-M1-00292-0334` | `CRS-M1-00292` | FIELD-CONSTRAINT | `FC-LCL-FIELD-SERIAL-NUMBER-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LCL-FIELD-SERIAL-NUMBER-LENGTH。 |
| `TR-CRS-M1-00293-0335` | `CRS-M1-00293` | FIELD-CONSTRAINT | `FC-LCL-FIELD-SERIAL-NUMBER` | 在具名协议文件字节上应用字段谓词 FC-LCL-FIELD-SERIAL-NUMBER。 |
| `TR-CRS-M1-00294-0336` | `CRS-M1-00294` | FIELD-CONSTRAINT | `FC-LCL-FIELD-NUMBER-OF-PART-NUMBERS` | 在具名协议文件字节上应用字段谓词 FC-LCL-FIELD-NUMBER-OF-PART-NUMBERS。 |
| `TR-CRS-M1-00295-0337` | `CRS-M1-00295` | FIELD-CONSTRAINT | `FC-LCL-FIELD-PART-NUMBER-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LCL-FIELD-PART-NUMBER-LENGTH。 |
| `TR-CRS-M1-00296-0338` | `CRS-M1-00296` | FIELD-CONSTRAINT | `FC-LCL-FIELD-PART-NUMBER` | 在具名协议文件字节上应用字段谓词 FC-LCL-FIELD-PART-NUMBER。 |
| `TR-CRS-M1-00297-0339` | `CRS-M1-00297` | FIELD-CONSTRAINT | `FC-LCL-FIELD-AMENDMENT-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LCL-FIELD-AMENDMENT-LENGTH。 |
| `TR-CRS-M1-00298-0340` | `CRS-M1-00298` | FIELD-CONSTRAINT | `FC-LCL-FIELD-AMENDMENT` | 在具名协议文件字节上应用字段谓词 FC-LCL-FIELD-AMENDMENT。 |
| `TR-CRS-M1-00299-0341` | `CRS-M1-00299` | FIELD-CONSTRAINT | `FC-LCL-FIELD-PART-DESIGNATION-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LCL-FIELD-PART-DESIGNATION-LENGTH。 |
| `TR-CRS-M1-00300-0342` | `CRS-M1-00300` | FIELD-CONSTRAINT | `FC-LCL-FIELD-PART-DESIGNATION-TEXT` | 在具名协议文件字节上应用字段谓词 FC-LCL-FIELD-PART-DESIGNATION-TEXT。 |
| `TR-CRS-M1-00301-0343` | `CRS-M1-00301` | FIELD-CONSTRAINT | `FC-LCS-FIELD-FILE-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LCS-FIELD-FILE-LENGTH。 |
| `TR-CRS-M1-00302-0344` | `CRS-M1-00302` | FIELD-CONSTRAINT | `FC-LCS-FIELD-PROTOCOL-VERSION` | 在具名协议文件字节上应用字段谓词 FC-LCS-FIELD-PROTOCOL-VERSION。 |
| `TR-CRS-M1-00303-0345` | `CRS-M1-00303` | FIELD-CONSTRAINT | `FC-LCS-FIELD-COUNTER` | 在具名协议文件字节上应用字段谓词 FC-LCS-FIELD-COUNTER。 |
| `TR-CRS-M1-00304-0346` | `CRS-M1-00304` | FIELD-CONSTRAINT | `FC-LCS-FIELD-INFORMATION-OPERATION-STATUS-CODE` | 在具名协议文件字节上应用字段谓词 FC-LCS-FIELD-INFORMATION-OPERATION-STATUS-CODE。 |
| `TR-CRS-M1-00305-0347` | `CRS-M1-00305` | FIELD-CONSTRAINT | `FC-LCS-FIELD-EXCEPTION-TIMER` | 在具名协议文件字节上应用字段谓词 FC-LCS-FIELD-EXCEPTION-TIMER。 |
| `TR-CRS-M1-00305-0348` | `CRS-M1-00305` | TIMING | `TIM-CRS-M1-00305` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00305-0349` | `CRS-M1-00305` | CLOCK | `CLK_EXCEPTION` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00306-0350` | `CRS-M1-00306` | FIELD-CONSTRAINT | `FC-LCS-FIELD-ESTIMATED-TIME` | 在具名协议文件字节上应用字段谓词 FC-LCS-FIELD-ESTIMATED-TIME。 |
| `TR-CRS-M1-00307-0351` | `CRS-M1-00307` | FIELD-CONSTRAINT | `FC-LCS-FIELD-STATUS-DESCRIPTION-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LCS-FIELD-STATUS-DESCRIPTION-LENGTH。 |
| `TR-CRS-M1-00308-0352` | `CRS-M1-00308` | FIELD-CONSTRAINT | `FC-LCS-FIELD-STATUS-DESCRIPTION` | 在具名协议文件字节上应用字段谓词 FC-LCS-FIELD-STATUS-DESCRIPTION。 |
| `TR-CRS-M1-00309-0353` | `CRS-M1-00309` | FIELD-CONSTRAINT | `FC-LUR-FIELD-FILE-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LUR-FIELD-FILE-LENGTH。 |
| `TR-CRS-M1-00310-0354` | `CRS-M1-00310` | FIELD-CONSTRAINT | `FC-LUR-FIELD-PROTOCOL-VERSION` | 在具名协议文件字节上应用字段谓词 FC-LUR-FIELD-PROTOCOL-VERSION。 |
| `TR-CRS-M1-00311-0355` | `CRS-M1-00311` | FIELD-CONSTRAINT | `FC-LUR-FIELD-NUMBER-OF-HEADER-FILES` | 在具名协议文件字节上应用字段谓词 FC-LUR-FIELD-NUMBER-OF-HEADER-FILES。 |
| `TR-CRS-M1-00312-0356` | `CRS-M1-00312` | FIELD-CONSTRAINT | `FC-LUR-FIELD-HEADER-FILE-NAME-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LUR-FIELD-HEADER-FILE-NAME-LENGTH。 |
| `TR-CRS-M1-00313-0357` | `CRS-M1-00313` | FIELD-CONSTRAINT | `FC-LUR-FIELD-HEADER-FILE-NAME` | 在具名协议文件字节上应用字段谓词 FC-LUR-FIELD-HEADER-FILE-NAME。 |
| `TR-CRS-M1-00314-0358` | `CRS-M1-00314` | FIELD-CONSTRAINT | `FC-LUR-FIELD-LOAD-PART-NUMBER-NAME-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LUR-FIELD-LOAD-PART-NUMBER-NAME-LENGTH。 |
| `TR-CRS-M1-00315-0359` | `CRS-M1-00315` | FIELD-CONSTRAINT | `FC-LUR-FIELD-LOAD-PART-NUMBER-NAME` | 在具名协议文件字节上应用字段谓词 FC-LUR-FIELD-LOAD-PART-NUMBER-NAME。 |
| `TR-CRS-M1-00316-0360` | `CRS-M1-00316` | FIELD-CONSTRAINT | `FC-LUS-FIELD-FILE-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-FILE-LENGTH。 |
| `TR-CRS-M1-00317-0361` | `CRS-M1-00317` | FIELD-CONSTRAINT | `FC-LUS-FIELD-PROTOCOL-VERSION` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-PROTOCOL-VERSION。 |
| `TR-CRS-M1-00318-0362` | `CRS-M1-00318` | FIELD-CONSTRAINT | `FC-LUS-FIELD-UPLOAD-OPERATION-STATUS-CODE` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-UPLOAD-OPERATION-STATUS-CODE。 |
| `TR-CRS-M1-00319-0363` | `CRS-M1-00319` | FIELD-CONSTRAINT | `FC-LUS-FIELD-UPLOAD-STATUS-DESCRIPTION-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-UPLOAD-STATUS-DESCRIPTION-LENGTH。 |
| `TR-CRS-M1-00320-0364` | `CRS-M1-00320` | FIELD-CONSTRAINT | `FC-LUS-FIELD-UPLOAD-STATUS-DESCRIPTION` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-UPLOAD-STATUS-DESCRIPTION。 |
| `TR-CRS-M1-00321-0365` | `CRS-M1-00321` | FIELD-CONSTRAINT | `FC-LUS-FIELD-COUNTER` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-COUNTER。 |
| `TR-CRS-M1-00322-0366` | `CRS-M1-00322` | FIELD-CONSTRAINT | `FC-LUS-FIELD-EXCEPTION-TIMER` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-EXCEPTION-TIMER。 |
| `TR-CRS-M1-00322-0367` | `CRS-M1-00322` | TIMING | `TIM-CRS-M1-00322` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00322-0368` | `CRS-M1-00322` | CLOCK | `CLK_EXCEPTION` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00323-0369` | `CRS-M1-00323` | FIELD-CONSTRAINT | `FC-LUS-FIELD-ESTIMATED-TIME` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-ESTIMATED-TIME。 |
| `TR-CRS-M1-00324-0370` | `CRS-M1-00324` | FIELD-CONSTRAINT | `FC-LUS-FIELD-LOAD-LIST-RATIO` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-LOAD-LIST-RATIO。 |
| `TR-CRS-M1-00325-0371` | `CRS-M1-00325` | FIELD-CONSTRAINT | `FC-LUS-FIELD-NUMBER-OF-HEADER-FILES` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-NUMBER-OF-HEADER-FILES。 |
| `TR-CRS-M1-00326-0372` | `CRS-M1-00326` | FIELD-CONSTRAINT | `FC-LUS-FIELD-HEADER-FILE-NAME-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-HEADER-FILE-NAME-LENGTH。 |
| `TR-CRS-M1-00327-0373` | `CRS-M1-00327` | FIELD-CONSTRAINT | `FC-LUS-FIELD-HEADER-FILE-NAME` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-HEADER-FILE-NAME。 |
| `TR-CRS-M1-00328-0374` | `CRS-M1-00328` | FIELD-CONSTRAINT | `FC-LUS-FIELD-LOAD-PART-NUMBER-NAME-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-LOAD-PART-NUMBER-NAME-LENGTH。 |
| `TR-CRS-M1-00329-0375` | `CRS-M1-00329` | FIELD-CONSTRAINT | `FC-LUS-FIELD-LOAD-PART-NUMBER-NAME` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-LOAD-PART-NUMBER-NAME。 |
| `TR-CRS-M1-00330-0376` | `CRS-M1-00330` | FIELD-CONSTRAINT | `FC-LUS-FIELD-LOAD-RATIO` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-LOAD-RATIO。 |
| `TR-CRS-M1-00331-0377` | `CRS-M1-00331` | FIELD-CONSTRAINT | `FC-LUS-FIELD-LOAD-STATUS` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-LOAD-STATUS。 |
| `TR-CRS-M1-00332-0378` | `CRS-M1-00332` | FIELD-CONSTRAINT | `FC-LUS-FIELD-LOAD-STATUS-DESCRIPTION-LENGTH` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-LOAD-STATUS-DESCRIPTION-LENGTH。 |
| `TR-CRS-M1-00333-0379` | `CRS-M1-00333` | FIELD-CONSTRAINT | `FC-LUS-FIELD-LOAD-STATUS-DESCRIPTION` | 在具名协议文件字节上应用字段谓词 FC-LUS-FIELD-LOAD-STATUS-DESCRIPTION。 |
| `TR-CRS-M1-00334-0380` | `CRS-M1-00334` | STATUS-CONSTRAINT | `ST-CRS-M1-00334` | 状态码谓词 ST-CRS-M1-00334。 |
| `TR-CRS-M1-00335-0381` | `CRS-M1-00335` | STATUS-CONSTRAINT | `ST-CRS-M1-00335` | 状态码谓词 ST-CRS-M1-00335。 |
| `TR-CRS-M1-00336-0382` | `CRS-M1-00336` | STATUS-CONSTRAINT | `ST-CRS-M1-00336` | 状态码谓词 ST-CRS-M1-00336。 |
| `TR-CRS-M1-00337-0383` | `CRS-M1-00337` | STATUS-CONSTRAINT | `ST-CRS-M1-00337` | 状态码谓词 ST-CRS-M1-00337。 |
| `TR-CRS-M1-00338-0384` | `CRS-M1-00338` | STATUS-CONSTRAINT | `ST-CRS-M1-00338` | 状态码谓词 ST-CRS-M1-00338。 |
| `TR-CRS-M1-00339-0385` | `CRS-M1-00339` | STATUS-CONSTRAINT | `ST-CRS-M1-00339` | 状态码谓词 ST-CRS-M1-00339。 |
| `TR-CRS-M1-00340-0386` | `CRS-M1-00340` | STATUS-CONSTRAINT | `ST-CRS-M1-00340` | 状态码谓词 ST-CRS-M1-00340。 |
| `TR-CRS-M1-00340-0463` | `CRS-M1-00340` | TRANSITION | `T_ABORT_TH` | 迁移 T_ABORT_TH 引用此义务。 |
| `TR-CRS-M1-00340-0464` | `CRS-M1-00340` | TRANSITION | `T_ABORTED` | 迁移 T_ABORTED 引用此义务。 |
| `TR-CRS-M1-00341-0387` | `CRS-M1-00341` | STATUS-CONSTRAINT | `ST-CRS-M1-00341` | 状态码谓词 ST-CRS-M1-00341。 |
| `TR-CRS-M1-00341-0462` | `CRS-M1-00341` | TRANSITION | `T_ABORT_DL` | 迁移 T_ABORT_DL 引用此义务。 |
| `TR-CRS-M1-00341-0465` | `CRS-M1-00341` | TRANSITION | `T_ABORTED` | 迁移 T_ABORTED 引用此义务。 |
| `TR-CRS-M1-00341-0466` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_INF_LCI_RRQ` | 迁移 T_ABORT_FROM_S_INF_LCI_RRQ 引用此义务。 |
| `TR-CRS-M1-00341-0467` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_INF_LCL_XFER` | 迁移 T_ABORT_FROM_S_INF_LCL_XFER 引用此义务。 |
| `TR-CRS-M1-00341-0468` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_INF_LCS_XFER` | 迁移 T_ABORT_FROM_S_INF_LCS_XFER 引用此义务。 |
| `TR-CRS-M1-00341-0469` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_INF_EXCEPTION` | 迁移 T_ABORT_FROM_S_INF_EXCEPTION 引用此义务。 |
| `TR-CRS-M1-00341-0470` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_WAIT_RETRY` | 迁移 T_ABORT_FROM_S_WAIT_RETRY 引用此义务。 |
| `TR-CRS-M1-00341-0471` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_UPL_LUI_XFER` | 迁移 T_ABORT_FROM_S_UPL_LUI_XFER 引用此义务。 |
| `TR-CRS-M1-00341-0472` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_UPL_LIST_SENT` | 迁移 T_ABORT_FROM_S_UPL_LIST_SENT 引用此义务。 |
| `TR-CRS-M1-00341-0473` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_UPL_WAIT_LUS0001` | 迁移 T_ABORT_FROM_S_UPL_WAIT_LUS0001 引用此义务。 |
| `TR-CRS-M1-00341-0474` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_UPL_LUR_XFER` | 迁移 T_ABORT_FROM_S_UPL_LUR_XFER 引用此义务。 |
| `TR-CRS-M1-00341-0475` | `CRS-M1-00341` | TRANSITION | `T_ABORT_FROM_S_UPL_LUS_XFER` | 迁移 T_ABORT_FROM_S_UPL_LUS_XFER 引用此义务。 |
| `TR-CRS-M1-00342-0388` | `CRS-M1-00342` | STATUS-CONSTRAINT | `ST-CRS-M1-00342` | 状态码谓词 ST-CRS-M1-00342。 |
| `TR-CRS-M1-00343-0389` | `CRS-M1-00343` | STATUS-CONSTRAINT | `ST-CRS-M1-00343` | 状态码谓词 ST-CRS-M1-00343。 |
| `TR-CRS-M1-00344-0390` | `CRS-M1-00344` | SCOPE | `SCOPE` | 仅 DOWNLOAD 的状态码不进入本 UPLOAD/INFORMATION 候选。 |
| `TR-CRS-M1-00345-0391` | `CRS-M1-00345` | STATUS-CONSTRAINT | `ST-CRS-M1-00345` | 状态码谓词 ST-CRS-M1-00345。 |
| `TR-CRS-M1-00346-0392` | `CRS-M1-00346` | TRANSITION | `T_INF_LCI_RRQ` | 序列图义务映射到 T_INF_LCI_RRQ。 |
| `TR-CRS-M1-00347-0393` | `CRS-M1-00347` | TRANSITION | `T_INF_LCI_RRQ` | 序列图义务映射到 T_INF_LCI_RRQ。 |
| `TR-CRS-M1-00348-0394` | `CRS-M1-00348` | TRANSITION | `T_INF_LCI_XFER` | 序列图义务映射到 T_INF_LCI_XFER。 |
| `TR-CRS-M1-00349-0395` | `CRS-M1-00349` | TRANSITION | `T_INF_EVAL` | 序列图义务映射到 T_INF_EVAL。 |
| `TR-CRS-M1-00349-0396` | `CRS-M1-00349` | TRANSITION | `T_INF_ACCEPT_INIT` | 序列图义务映射到 T_INF_ACCEPT_INIT。 |
| `TR-CRS-M1-00350-0397` | `CRS-M1-00350` | TRANSITION | `T_INF_REJECT` | 序列图义务映射到 T_INF_REJECT。 |
| `TR-CRS-M1-00351-0398` | `CRS-M1-00351` | TRANSITION | `T_INF_LCL_WRQ` | 序列图义务映射到 T_INF_LCL_WRQ。 |
| `TR-CRS-M1-00351-0441` | `CRS-M1-00351` | TRANSITION | `T_INF_ACCEPT_INIT` | 迁移 T_INF_ACCEPT_INIT 引用此义务。 |
| `TR-CRS-M1-00352-0399` | `CRS-M1-00352` | TRANSITION | `T_INF_LCL_ACK` | 序列图义务映射到 T_INF_LCL_ACK。 |
| `TR-CRS-M1-00353-0400` | `CRS-M1-00353` | TRANSITION | `T_INF_LCL_XFER` | 序列图义务映射到 T_INF_LCL_XFER。 |
| `TR-CRS-M1-00354-0401` | `CRS-M1-00354` | TRANSITION | `T_INF_APP` | 序列图义务映射到 T_INF_APP。 |
| `TR-CRS-M1-00355-0402` | `CRS-M1-00355` | TRANSITION | `T_INF_LCS_WRQ` | 序列图义务映射到 T_INF_LCS_WRQ。 |
| `TR-CRS-M1-00356-0403` | `CRS-M1-00356` | TRANSITION | `T_INF_LCS_XFER` | 序列图义务映射到 T_INF_LCS_XFER。 |
| `TR-CRS-M1-00357-0404` | `CRS-M1-00357` | TRANSITION | `T_INF_LCS_XFER` | 序列图义务映射到 T_INF_LCS_XFER。 |
| `TR-CRS-M1-00358-0405` | `CRS-M1-00358` | TRANSITION | `T_INF_LCS_XFER` | 序列图义务映射到 T_INF_LCS_XFER。 |
| `TR-CRS-M1-00358-0406` | `CRS-M1-00358` | TRANSITION | `T_INF_SESSION_END` | 序列图义务映射到 T_INF_SESSION_END。 |
| `TR-CRS-M1-00359-0407` | `CRS-M1-00359` | TRANSITION | `T_UPL_LUI_RRQ` | 序列图义务映射到 T_UPL_LUI_RRQ。 |
| `TR-CRS-M1-00360-0408` | `CRS-M1-00360` | TRANSITION | `T_UPL_LUI_RRQ` | 序列图义务映射到 T_UPL_LUI_RRQ。 |
| `TR-CRS-M1-00360-0409` | `CRS-M1-00360` | TRANSITION | `T_UPL_LUI_RRQ_AFTER_INF` | 序列图义务映射到 T_UPL_LUI_RRQ_AFTER_INF。 |
| `TR-CRS-M1-00361-0410` | `CRS-M1-00361` | TRANSITION | `T_UPL_LUI_XFER` | 序列图义务映射到 T_UPL_LUI_XFER。 |
| `TR-CRS-M1-00362-0411` | `CRS-M1-00362` | TRANSITION | `T_UPL_EVAL` | 序列图义务映射到 T_UPL_EVAL。 |
| `TR-CRS-M1-00362-0412` | `CRS-M1-00362` | TRANSITION | `T_UPL_ACCEPT_INIT` | 序列图义务映射到 T_UPL_ACCEPT_INIT。 |
| `TR-CRS-M1-00362-0413` | `CRS-M1-00362` | TRANSITION | `T_UPL_REJECT` | 序列图义务映射到 T_UPL_REJECT。 |
| `TR-CRS-M1-00363-0414` | `CRS-M1-00363` | TRANSITION | `T_UPL_ACCEPT_INIT` | 序列图义务映射到 T_UPL_ACCEPT_INIT。 |
| `TR-CRS-M1-00363-0415` | `CRS-M1-00363` | TRANSITION | `T_UPL_LIST_OFFER` | 序列图义务映射到 T_UPL_LIST_OFFER。 |
| `TR-CRS-M1-00364-0416` | `CRS-M1-00364` | TRANSITION | `T_UPL_LIST_OFFER` | 序列图义务映射到 T_UPL_LIST_OFFER。 |
| `TR-CRS-M1-00364-0417` | `CRS-M1-00364` | TRANSITION | `T_UPL_WAIT_LUS0001` | 序列图义务映射到 T_UPL_WAIT_LUS0001。 |
| `TR-CRS-M1-00365-0418` | `CRS-M1-00365` | TRANSITION | `T_UPL_LUR_WRQ` | 序列图义务映射到 T_UPL_LUR_WRQ。 |
| `TR-CRS-M1-00366-0419` | `CRS-M1-00366` | TRANSITION | `T_UPL_LUR_ACK` | 序列图义务映射到 T_UPL_LUR_ACK。 |
| `TR-CRS-M1-00367-0420` | `CRS-M1-00367` | TRANSITION | `T_UPL_LUR_XFER` | 序列图义务映射到 T_UPL_LUR_XFER。 |
| `TR-CRS-M1-00368-0421` | `CRS-M1-00368` | TRANSITION | `T_UPL_FILE_RRQ` | 序列图义务映射到 T_UPL_FILE_RRQ。 |
| `TR-CRS-M1-00368-0422` | `CRS-M1-00368` | TRANSITION | `T_UPL_FILE_RRQ_MORE` | 序列图义务映射到 T_UPL_FILE_RRQ_MORE。 |
| `TR-CRS-M1-00369-0423` | `CRS-M1-00369` | TRANSITION | `T_UPL_FILE_UNAVAIL` | 序列图义务映射到 T_UPL_FILE_UNAVAIL。 |
| `TR-CRS-M1-00370-0424` | `CRS-M1-00370` | TRANSITION | `T_UPL_FILE_XFER` | 序列图义务映射到 T_UPL_FILE_XFER。 |
| `TR-CRS-M1-00371-0425` | `CRS-M1-00371` | TRANSITION | `T_UPL_FILE_STATUS` | 序列图义务映射到 T_UPL_FILE_STATUS。 |
| `TR-CRS-M1-00372-0426` | `CRS-M1-00372` | TRANSITION | `T_UPL_MORE_FILES` | 序列图义务映射到 T_UPL_MORE_FILES。 |
| `TR-CRS-M1-00372-0427` | `CRS-M1-00372` | TRANSITION | `T_UPL_FILE_RRQ_MORE` | 序列图义务映射到 T_UPL_FILE_RRQ_MORE。 |
| `TR-CRS-M1-00373-0428` | `CRS-M1-00373` | TRANSITION | `T_UPL_TO_LUS` | 序列图义务映射到 T_UPL_TO_LUS。 |
| `TR-CRS-M1-00374-0429` | `CRS-M1-00374` | TRANSITION | `T_UPL_LUS_XFER` | 序列图义务映射到 T_UPL_LUS_XFER。 |
| `TR-CRS-M1-00375-0430` | `CRS-M1-00375` | TRANSITION | `T_UPL_STATUS_APP` | 序列图义务映射到 T_UPL_STATUS_APP。 |
| `TR-CRS-M1-00376-0431` | `CRS-M1-00376` | TRANSITION | `T_UPL_COMPLETE` | 序列图义务映射到 T_UPL_COMPLETE。 |
| `TR-CRS-M1-00376-0432` | `CRS-M1-00376` | TRANSITION | `T_UPL_STATUS_REPEAT` | 序列图义务映射到 T_UPL_STATUS_REPEAT。 |
| `TR-CRS-M1-00377-0433` | `CRS-M1-00377` | SCOPE | `SCOPE` | 非行为／Profile 义务 RECEIVE 保持为范围或适用性约束。 |
| `TR-CRS-M1-00378-0434` | `CRS-M1-00378` | SCOPE | `SCOPE` | 非行为／Profile 义务 WAIT 保持为范围或适用性约束。 |
| `TR-CRS-M1-00379-0435` | `CRS-M1-00379` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND-TFTP-WRITE-REQUEST 保持为范围或适用性约束。 |
| `TR-CRS-M1-00380-0436` | `CRS-M1-00380` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00381-0437` | `CRS-M1-00381` | SCOPE | `SCOPE` | 非行为／Profile 义务 STOP 保持为范围或适用性约束。 |
| `TR-CRS-M1-00382-0438` | `CRS-M1-00382` | INTERFACE | `IF_TFTP` | TRANSFER 的 TFTP 接口前提。 |
| `TR-CRS-M1-00383-0439` | `CRS-M1-00383` | SCOPE | `SCOPE` | 非行为／Profile 义务 SEND 保持为范围或适用性约束。 |
| `TR-CRS-M1-00384-0440` | `CRS-M1-00384` | SCOPE | `SCOPE` | 非行为／Profile 义务 TERMINATE 保持为范围或适用性约束。 |
| `TR-CRS-M1-00385-0476` | `CRS-M1-00385` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00386-0477` | `CRS-M1-00386` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00387-0478` | `CRS-M1-00387` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00388-0479` | `CRS-M1-00388` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00389-0480` | `CRS-M1-00389` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00390-0481` | `CRS-M1-00390` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00391-0482` | `CRS-M1-00391` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00391-0618` | `CRS-M1-00391` | TIMING | `TIM-CRS-M1-00391` | FIND 时序已编入目录供后续误差区间判定；绑定 M2 不运行 FIND。 |
| `TR-CRS-M1-00391-0619` | `CRS-M1-00391` | CLOCK | `CLK_FIND` | FIND 时钟仅用于目录观察，不进入绑定状态机迁移。 |
| `TR-CRS-M1-00392-0483` | `CRS-M1-00392` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00393-0484` | `CRS-M1-00393` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00394-0485` | `CRS-M1-00394` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00395-0486` | `CRS-M1-00395` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00396-0487` | `CRS-M1-00396` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00397-0488` | `CRS-M1-00397` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00398-0489` | `CRS-M1-00398` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00399-0490` | `CRS-M1-00399` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00400-0491` | `CRS-M1-00400` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00401-0492` | `CRS-M1-00401` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00402-0493` | `CRS-M1-00402` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00403-0494` | `CRS-M1-00403` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00404-0495` | `CRS-M1-00404` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00405-0496` | `CRS-M1-00405` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00406-0497` | `CRS-M1-00406` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00407-0498` | `CRS-M1-00407` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00408-0499` | `CRS-M1-00408` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00409-0500` | `CRS-M1-00409` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00410-0501` | `CRS-M1-00410` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00411-0502` | `CRS-M1-00411` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00412-0503` | `CRS-M1-00412` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00413-0504` | `CRS-M1-00413` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00414-0505` | `CRS-M1-00414` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00415-0506` | `CRS-M1-00415` | SCOPE | `SCOPE` | FIND 义务已记入扩大 CRS；绑定 M2 不建模 FIND 行为。 |
| `TR-CRS-M1-00416-0507` | `CRS-M1-00416` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00417-0508` | `CRS-M1-00417` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00418-0509` | `CRS-M1-00418` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00419-0510` | `CRS-M1-00419` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00420-0511` | `CRS-M1-00420` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00421-0512` | `CRS-M1-00421` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00422-0513` | `CRS-M1-00422` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00423-0514` | `CRS-M1-00423` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00424-0515` | `CRS-M1-00424` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00426-0517` | `CRS-M1-00426` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00427-0518` | `CRS-M1-00427` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00428-0519` | `CRS-M1-00428` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00429-0520` | `CRS-M1-00429` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00430-0521` | `CRS-M1-00430` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00431-0522` | `CRS-M1-00431` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00432-0523` | `CRS-M1-00432` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00433-0524` | `CRS-M1-00433` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00434-0525` | `CRS-M1-00434` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00435-0526` | `CRS-M1-00435` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00436-0527` | `CRS-M1-00436` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00437-0528` | `CRS-M1-00437` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00438-0529` | `CRS-M1-00438` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00439-0530` | `CRS-M1-00439` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00440-0531` | `CRS-M1-00440` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00441-0532` | `CRS-M1-00441` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00442-0533` | `CRS-M1-00442` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00443-0534` | `CRS-M1-00443` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00444-0535` | `CRS-M1-00444` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00445-0536` | `CRS-M1-00445` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00446-0537` | `CRS-M1-00446` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00447-0538` | `CRS-M1-00447` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00448-0539` | `CRS-M1-00448` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00449-0540` | `CRS-M1-00449` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00450-0541` | `CRS-M1-00450` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00451-0542` | `CRS-M1-00451` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00452-0543` | `CRS-M1-00452` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00453-0544` | `CRS-M1-00453` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00454-0545` | `CRS-M1-00454` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00455-0546` | `CRS-M1-00455` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00456-0547` | `CRS-M1-00456` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00457-0548` | `CRS-M1-00457` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00458-0549` | `CRS-M1-00458` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00459-0550` | `CRS-M1-00459` | FIELD-CONSTRAINT | `FC-LNR-FIELD-FILE-LENGTH` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00460-0551` | `CRS-M1-00460` | FIELD-CONSTRAINT | `FC-LNR-FIELD-PROTOCOL-VERSION` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00461-0552` | `CRS-M1-00461` | FIELD-CONSTRAINT | `FC-LNR-FIELD-NUMBER-OF-FILES` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00462-0553` | `CRS-M1-00462` | FIELD-CONSTRAINT | `FC-LNR-FIELD-FILE-NAME-LENGTH` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00463-0554` | `CRS-M1-00463` | FIELD-CONSTRAINT | `FC-LNR-FIELD-FILE-NAME` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00464-0555` | `CRS-M1-00464` | FIELD-CONSTRAINT | `FC-LNR-FIELD-USER-DEFINED-DATA-LENGTH` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00465-0556` | `CRS-M1-00465` | FIELD-CONSTRAINT | `FC-LNR-FIELD-USER-DEFINED-DATA` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00466-0557` | `CRS-M1-00466` | FIELD-CONSTRAINT | `FC-LNS-FIELD-FILE-LENGTH` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00467-0558` | `CRS-M1-00467` | FIELD-CONSTRAINT | `FC-LNS-FIELD-PROTOCOL-VERSION` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00468-0559` | `CRS-M1-00468` | FIELD-CONSTRAINT | `FC-LNS-FIELD-DOWNLOAD-OPERATION-STATUS-CODE` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00469-0560` | `CRS-M1-00469` | FIELD-CONSTRAINT | `FC-LNS-FIELD-DOWNLOAD-STATUS-DESCRIPTION-LENGTH` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00470-0561` | `CRS-M1-00470` | FIELD-CONSTRAINT | `FC-LNS-FIELD-DOWNLOAD-STATUS-DESCRIPTION` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00471-0562` | `CRS-M1-00471` | FIELD-CONSTRAINT | `FC-LNS-FIELD-COUNTER` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00472-0563` | `CRS-M1-00472` | FIELD-CONSTRAINT | `FC-LNS-FIELD-EXCEPTION-TIMER` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00473-0564` | `CRS-M1-00473` | FIELD-CONSTRAINT | `FC-LNS-FIELD-ESTIMATED-TIME` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00474-0565` | `CRS-M1-00474` | FIELD-CONSTRAINT | `FC-LNS-FIELD-DOWNLOAD-LIST-RATIO` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00475-0566` | `CRS-M1-00475` | FIELD-CONSTRAINT | `FC-LNS-FIELD-NUMBER-OF-FILES` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00476-0567` | `CRS-M1-00476` | FIELD-CONSTRAINT | `FC-LNS-FIELD-FILE-NAME-LENGTH` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00477-0568` | `CRS-M1-00477` | FIELD-CONSTRAINT | `FC-LNS-FIELD-FILE-NAME` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00478-0569` | `CRS-M1-00478` | FIELD-CONSTRAINT | `FC-LNS-FIELD-FILE-STATUS` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00479-0570` | `CRS-M1-00479` | FIELD-CONSTRAINT | `FC-LNS-FIELD-FILE-STATUS-DESCRIPTION-LENGTH` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00480-0571` | `CRS-M1-00480` | FIELD-CONSTRAINT | `FC-LNS-FIELD-FILE-STATUS-DESCRIPTION` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00481-0572` | `CRS-M1-00481` | FIELD-CONSTRAINT | `FC-LNL-FIELD-FILE-LENGTH` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00482-0573` | `CRS-M1-00482` | FIELD-CONSTRAINT | `FC-LNL-FIELD-PROTOCOL-VERSION` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00483-0574` | `CRS-M1-00483` | FIELD-CONSTRAINT | `FC-LNL-FIELD-NUMBER-OF-FILES` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00484-0575` | `CRS-M1-00484` | FIELD-CONSTRAINT | `FC-LNL-FIELD-FILE-NAME-LENGTH` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00485-0576` | `CRS-M1-00485` | FIELD-CONSTRAINT | `FC-LNL-FIELD-FILE-NAME` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00486-0577` | `CRS-M1-00486` | FIELD-CONSTRAINT | `FC-LNL-FIELD-FILE-DESCRIPTION-LENGTH` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00487-0578` | `CRS-M1-00487` | FIELD-CONSTRAINT | `FC-LNL-FIELD-FILE-DESCRIPTION` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00488-0579` | `CRS-M1-00488` | FIELD-CONSTRAINT | `FC-LNA-FIELD-FILE-LENGTH` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00489-0580` | `CRS-M1-00489` | FIELD-CONSTRAINT | `FC-LNA-FIELD-PROTOCOL-VERSION` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00490-0581` | `CRS-M1-00490` | FIELD-CONSTRAINT | `FC-LNA-FIELD-NUMBER-OF-FILES` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00491-0582` | `CRS-M1-00491` | FIELD-CONSTRAINT | `FC-LNA-FIELD-FILE-NAME-LENGTH` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00492-0583` | `CRS-M1-00492` | FIELD-CONSTRAINT | `FC-LNA-FIELD-FILE-NAME` | DOWNLOAD 字段约束已记录；绑定 M2 不建模 DOWNLOAD 行为。 |
| `TR-CRS-M1-00493-0584` | `CRS-M1-00493` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00494-0585` | `CRS-M1-00494` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00495-0586` | `CRS-M1-00495` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00496-0587` | `CRS-M1-00496` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00497-0588` | `CRS-M1-00497` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00498-0589` | `CRS-M1-00498` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00499-0590` | `CRS-M1-00499` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00500-0591` | `CRS-M1-00500` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00501-0592` | `CRS-M1-00501` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00502-0593` | `CRS-M1-00502` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00503-0594` | `CRS-M1-00503` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00504-0595` | `CRS-M1-00504` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00505-0596` | `CRS-M1-00505` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00506-0597` | `CRS-M1-00506` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00507-0598` | `CRS-M1-00507` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00508-0599` | `CRS-M1-00508` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00509-0600` | `CRS-M1-00509` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00510-0601` | `CRS-M1-00510` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00511-0602` | `CRS-M1-00511` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00512-0603` | `CRS-M1-00512` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00513-0604` | `CRS-M1-00513` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00514-0605` | `CRS-M1-00514` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00515-0606` | `CRS-M1-00515` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00516-0607` | `CRS-M1-00516` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00517-0608` | `CRS-M1-00517` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00518-0609` | `CRS-M1-00518` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00519-0610` | `CRS-M1-00519` | SCOPE | `SCOPE` | DOWNLOAD／AFDX 义务已记入扩大 CRS；绑定 M2 不建模该行为。 |
| `TR-CRS-M1-00520-0611` | `CRS-M1-00520` | SCOPE | `SCOPE` | 扩大 CRS 已记录；绑定 M2 不执行 FIND／DOWNLOAD。 |
| `TR-CRS-M1-00520-0612` | `CRS-M1-00520` | TIMING | `TIM-CRS-M1-00520` | 扩大 CRS 已记录；绑定 M2 不执行 FIND／DOWNLOAD。 |
| `TR-CRS-M1-00520-0613` | `CRS-M1-00520` | CLOCK | `CLK_FIND` | 扩大 CRS 已记录；绑定 M2 不执行 FIND／DOWNLOAD。 |
| `TR-CRS-M1-00521-0614` | `CRS-M1-00521` | SCOPE | `SCOPE` | 扩大 CRS 已记录；绑定 M2 不执行 FIND／DOWNLOAD。 |
| `TR-CRS-M1-00521-0621` | `CRS-M1-00521` | TIMING | `TIM-CRS-M1-00521` | FIND 时序已编入目录供后续误差区间判定；绑定 M2 不运行 FIND。 |
| `TR-CRS-M1-00521-0622` | `CRS-M1-00521` | CLOCK | `CLK_FIND` | FIND 时钟仅用于目录观察，不进入绑定状态机迁移。 |
| `TR-CRS-M1-00522-0615` | `CRS-M1-00522` | SCOPE | `SCOPE` | 扩大 CRS 已记录；绑定 M2 不执行 FIND／DOWNLOAD。 |
| `TR-CRS-M1-00523-0616` | `CRS-M1-00523` | SCOPE | `SCOPE` | 扩大 CRS 已记录；绑定 M2 不执行 FIND／DOWNLOAD。 |
| `TR-CRS-M1-00524-0617` | `CRS-M1-00524` | SCOPE | `SCOPE` | 扩大 CRS 已记录；绑定 M2 不执行 FIND／DOWNLOAD。 |
| `TR-CRS-M1-00525-0620` | `CRS-M1-00525` | SCOPE | `SCOPE` | 扩大 CRS 已记录；绑定 M2 不执行 FIND／DOWNLOAD。 |
| `TR-CRS-M1-00526-0623` | `CRS-M1-00526` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-MAY-USE-BATCH-FILE-FORMAT-CRS-M1-00526` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00527-0624` | `CRS-M1-00527` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-LET-BATCH-FILE-SELECT-LSPS-PER-TARGET-HW-POSITION-CRS-M1-00527` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00528-0625` | `CRS-M1-00528` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-IDENTIFY-BATCH-FILE-WITH-LUB-EXTENSION-CRS-M1-00528` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00529-0626` | `CRS-M1-00529` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-MATCH-REFERENCED-HEADER-FILE-NAME-CASE-CRS-M1-00529` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00530-0627` | `CRS-M1-00530` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-PREFIX-BATCH-FILE-NAME-WITH-MANUFACTURER-CODE-CRS-M1-00530` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00531-0628` | `CRS-M1-00531` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-BATCH-FILE-NAME-UNIQUE-PER-MANUFACTURER-CODE-CRS-M1-00531` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00532-0629` | `CRS-M1-00532` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-BATCH-FILE-PART-NUMBER-UNIQUE-AMONG-LSP-AND-BFP-CRS-M1-00532` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00533-0630` | `CRS-M1-00533` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-REFERENCE-COMPLETE-HEADER-FILE-NAME-WITHOUT-PATH-CRS-M1-00533` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00534-0631` | `CRS-M1-00534` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-USE-BATCH-FILE-ONLY-TO-AUTOMATE-MULTI-LSP-SETUP-CRS-M1-00534` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00535-0632` | `CRS-M1-00535` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-DO-NOT-TRANSFER-BATCH-FILE-TO-TARGET-HARDWARE-CRS-M1-00535` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00536-0633` | `CRS-M1-00536` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-INCLUDE-BATCH-FILE-CONTENT-DEFINED-BY-TABLE-2-3-1-1-CRS-M1-00536` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00537-0634` | `CRS-M1-00537` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-BATCH-FILE-LENGTH-IN-16-BIT-WORDS-CRS-M1-00537` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00538-0635` | `CRS-M1-00538` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-MAKE-BATCH-FILE-PN-COMPLIANT-WITH-SOFTWARE-LOAD-PN-FORMAT-CRS-M1-00538` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00539-0636` | `CRS-M1-00539` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-BATCH-FILE-PN-DISTINCT-FROM-LSP-AND-MSP-CRS-M1-00539` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00540-0637` | `CRS-M1-00540` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-SET-LAST-LOAD-LIST-BLOCK-POINTER-TO-ZERO-CRS-M1-00540` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00541-0638` | `CRS-M1-00541` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-MATCH-TARGET-HW-ID-POS-TO-TARGET-HARDWARE-CRS-M1-00541` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00542-0639` | `CRS-M1-00542` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-MATCH-HEADER-FILE-NAME-TO-LISTED-LSP-CRS-M1-00542` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00543-0640` | `CRS-M1-00543` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-MATCH-LOAD-PN-TO-LSP-FOR-TARGET-HW-ID-POS-CRS-M1-00543` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00544-0641` | `CRS-M1-00544` | INTERFACE | `IF_INTEGRITY` | CRC 算法身份仍由未绑定的 ARINC 645 阻塞；完整性接口保持未建立。 |
| `TR-CRS-M1-00545-0642` | `CRS-M1-00545` | INTERFACE | `IF_INTEGRITY` | CRC 算法身份仍由未绑定的 ARINC 645 阻塞；完整性接口保持未建立。 |
| `TR-CRS-M1-00546-0643` | `CRS-M1-00546` | FIELD-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-LENGTH` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00547-0644` | `CRS-M1-00547` | FIELD-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-FORMAT-VERSION` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00548-0645` | `CRS-M1-00548` | FIELD-CONSTRAINT | `FC-LUB-FIELD-SPARE` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00549-0646` | `CRS-M1-00549` | FIELD-CONSTRAINT | `FC-LUB-FIELD-POINTER-TO-BATCH-FILE-PN-LENGTH` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00550-0647` | `CRS-M1-00550` | FIELD-CONSTRAINT | `FC-LUB-FIELD-POINTER-TO-NUMBER-OF-TARGET-HW-ID-LOAD-LIST-BLOCKS` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00551-0648` | `CRS-M1-00551` | FIELD-CONSTRAINT | `FC-LUB-FIELD-EXPANSION-POINT-1` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00552-0649` | `CRS-M1-00552` | FIELD-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-PN-LENGTH` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00553-0650` | `CRS-M1-00553` | FIELD-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-PN` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00554-0651` | `CRS-M1-00554` | FIELD-CONSTRAINT | `FC-LUB-FIELD-COMMENT-LENGTH` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00555-0652` | `CRS-M1-00555` | FIELD-CONSTRAINT | `FC-LUB-FIELD-COMMENT` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00556-0653` | `CRS-M1-00556` | FIELD-CONSTRAINT | `FC-LUB-FIELD-EXPANSION-POINT-2` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00557-0654` | `CRS-M1-00557` | FIELD-CONSTRAINT | `FC-LUB-FIELD-NUMBER-OF-TARGET-HW-ID-LOAD-LIST-BLOCKS` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00558-0655` | `CRS-M1-00558` | FIELD-CONSTRAINT | `FC-LUB-FIELD-POINTER-TO-NEXT-TARGET-HW-ID-LOAD-LIST-BLOCK` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00559-0656` | `CRS-M1-00559` | FIELD-CONSTRAINT | `FC-LUB-FIELD-TARGET-HW-ID-POS-LENGTH` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00560-0657` | `CRS-M1-00560` | FIELD-CONSTRAINT | `FC-LUB-FIELD-TARGET-HW-ID-POS` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00561-0658` | `CRS-M1-00561` | FIELD-CONSTRAINT | `FC-LUB-FIELD-NUMBER-OF-LOADS-FOR-TARGET-HW-ID-POS` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00562-0659` | `CRS-M1-00562` | FIELD-CONSTRAINT | `FC-LUB-FIELD-HEADER-FILE-NAME-LENGTH` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00563-0660` | `CRS-M1-00563` | FIELD-CONSTRAINT | `FC-LUB-FIELD-HEADER-FILE-NAME` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00564-0661` | `CRS-M1-00564` | FIELD-CONSTRAINT | `FC-LUB-FIELD-LOAD-PN-LENGTH` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00565-0662` | `CRS-M1-00565` | FIELD-CONSTRAINT | `FC-LUB-FIELD-LOAD-PN` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00566-0663` | `CRS-M1-00566` | FIELD-CONSTRAINT | `FC-LUB-FIELD-EXPANSION-POINT-3` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00567-0664` | `CRS-M1-00567` | FIELD-CONSTRAINT | `FC-LUB-FIELD-BATCH-FILE-CRC` | 665 批处理文件表行记为字段约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00567-0665` | `CRS-M1-00567` | INTERFACE | `IF_INTEGRITY` | CRC 算法身份仍由未绑定的 ARINC 645 阻塞；完整性接口保持未建立。 |
| `TR-CRS-M1-00568-0666` | `CRS-M1-00568` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-DEFINE-BATCH-FILE-FORMAT-VERSION-IN-16-BITS-CRS-M1-00568` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00569-0667` | `CRS-M1-00569` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-TAKE-BATCH-FILE-FORMAT-VERSION-FROM-CLAUSE-1-4-1-CRS-M1-00569` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00570-0668` | `CRS-M1-00570` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-USE-SPARE-TO-ALIGN-FOLLOWING-POINTERS-ON-4-BYTE-BOUNDARIES-CRS-M1-00570` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00571-0669` | `CRS-M1-00571` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-POINT-TO-BATCH-FILE-PN-LENGTH-FROM-START-IN-16-BIT-WORDS-CRS-M1-00571` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00572-0670` | `CRS-M1-00572` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-POINT-TO-LOAD-LIST-BLOCK-COUNT-FROM-START-IN-16-BIT-WORDS-CRS-M1-00572` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00573-0671` | `CRS-M1-00573` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-MAY-GROW-FILE-FORMAT-AT-EXPANSION-POINTS-CRS-M1-00573` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00574-0672` | `CRS-M1-00574` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-BATCH-FILE-PN-LENGTH-CRS-M1-00574` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00575-0673` | `CRS-M1-00575` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-BATCH-FILE-PN-AS-8-BIT-ASCII-CRS-M1-00575` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00576-0674` | `CRS-M1-00576` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-BATCH-FILE-PN-EVEN-OCTET-WIDTH-CRS-M1-00576` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00577-0675` | `CRS-M1-00577` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-BATCH-FILE-PN-WITH-NUL-CRS-M1-00577` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00578-0676` | `CRS-M1-00578` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-COMMENT-LENGTH-CRS-M1-00578` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00579-0677` | `CRS-M1-00579` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-SET-COMMENT-LENGTH-ZERO-WHEN-NO-COMMENT-CRS-M1-00579` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00580-0678` | `CRS-M1-00580` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-COMMENT-AS-8-BIT-ASCII-CRS-M1-00580` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00581-0679` | `CRS-M1-00581` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-COMMENT-EVEN-OCTET-WIDTH-CRS-M1-00581` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00582-0680` | `CRS-M1-00582` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-COMMENT-WITH-NUL-CRS-M1-00582` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00583-0681` | `CRS-M1-00583` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-OMIT-COMMENT-FIELD-WHEN-COMMENT-LENGTH-ZERO-CRS-M1-00583` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00584-0682` | `CRS-M1-00584` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-COUNT-TARGET-HW-ID-LOAD-LIST-BLOCKS-IN-BATCH-FILE-CRS-M1-00584` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00585-0683` | `CRS-M1-00585` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-POINT-TO-NEXT-LOAD-LIST-BLOCK-IN-RELATIVE-16-BIT-WORDS-CRS-M1-00585` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00586-0684` | `CRS-M1-00586` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-TARGET-HW-ID-POS-LENGTH-CRS-M1-00586` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00587-0685` | `CRS-M1-00587` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-TARGET-HW-ID-POS-AS-8-BIT-ASCII-CRS-M1-00587` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00588-0686` | `CRS-M1-00588` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-TARGET-HW-ID-POS-EVEN-OCTET-WIDTH-CRS-M1-00588` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00589-0687` | `CRS-M1-00589` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-TARGET-HW-ID-POS-WITH-NUL-CRS-M1-00589` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00590-0688` | `CRS-M1-00590` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-TARGET-HW-ID-POS-CONSISTENT-WITH-LISTED-LSP-HEADERS-CRS-M1-00590` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00591-0689` | `CRS-M1-00591` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-COUNT-LOADS-IN-THE-TARGET-HW-ID-LOAD-LIST-BLOCK-CRS-M1-00591` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00592-0690` | `CRS-M1-00592` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-HEADER-FILE-NAME-LENGTH-CRS-M1-00592` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00593-0691` | `CRS-M1-00593` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-HEADER-FILE-NAME-AS-8-BIT-ASCII-CRS-M1-00593` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00594-0692` | `CRS-M1-00594` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-HEADER-FILE-NAME-EVEN-OCTET-WIDTH-CRS-M1-00594` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00595-0693` | `CRS-M1-00595` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-HEADER-FILE-NAME-WITH-NUL-CRS-M1-00595` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00596-0694` | `CRS-M1-00596` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-USE-HEADER-FILE-NAME-WITHOUT-PATH-CRS-M1-00596` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00597-0695` | `CRS-M1-00597` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-KEEP-HEADER-FILE-NAME-FREE-OF-BACKSLASH-CRS-M1-00597` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00598-0696` | `CRS-M1-00598` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-INCLUDE-HEADER-FILE-NAME-EXTENSIONS-AND-DELIMITERS-CRS-M1-00598` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00599-0697` | `CRS-M1-00599` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-DEFINE-LOAD-PN-LENGTH-AS-CHARACTER-COUNT-CRS-M1-00599` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00600-0698` | `CRS-M1-00600` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-EXCLUDE-NUL-PAD-FROM-LOAD-PN-LENGTH-CRS-M1-00600` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00601-0699` | `CRS-M1-00601` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ENCODE-LOAD-PN-AS-8-BIT-ASCII-CRS-M1-00601` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00602-0700` | `CRS-M1-00602` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-ALLOCATE-LOAD-PN-EVEN-OCTET-WIDTH-CRS-M1-00602` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00603-0701` | `CRS-M1-00603` | OBJECT-CONSTRAINT | `OBJ-BATCH-FILE-PAD-ODD-LOAD-PN-WITH-NUL-CRS-M1-00603` | 665 批处理文件谓词记为数据对象约束；绑定 M2 不执行批处理加载。 |
| `TR-CRS-M1-00604-0805` | `CRS-M1-00604` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-GIVE-664P3-PRECEDENCE-OVER-CONFLICTING-RFC-OPTIONS-CRS-M1-00604` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00605-0806` | `CRS-M1-00605` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-GENERATE-AND-CHECK-UDP-CHECKSUM-CRS-M1-00605` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00606-0807` | `CRS-M1-00606` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-IMPLEMENT-IPV4-IN-ACCORDANCE-WITH-P3-FIGURE-3-4-1-1-CRS-M1-00606` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00607-0883` | `CRS-M1-00607` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-SECURE-RELIABLE-PARTITION-DATA-EXCHANGE-CRS-M1-00607` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00608-0809` | `CRS-M1-00608` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-FILTER-AND-POLICE-FRAMES-FOR-INTEGRITY-LENGTH-BUDGET-AND-DESTINATION-CRS-M1-00608` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00609-0810` | `CRS-M1-00609` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-AFDX-NOT-APPLICABLE-PROFILE-ITEMS-AS-MUST-NOT-CRS-M1-00609` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00610-0811` | `CRS-M1-00610` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-UDP-LENGTH-TO-HEADER-PLUS-DATA-OCTETS-CRS-M1-00610` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00611-0812` | `CRS-M1-00611` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-COMPUTE-UDP-CHECKSUM-OVER-PSEUDO-HEADER-HEADER-AND-DATA-CRS-M1-00611` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00612-0884` | `CRS-M1-00612` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-IMPLEMENT-IPV4-ADDRESSING-AND-FRAGMENTATION-CRS-M1-00612` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00613-0815` | `CRS-M1-00613` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-IMPLEMENT-IPV4-FRAGMENTATION-AND-REASSEMBLY-CRS-M1-00613` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00614-0816` | `CRS-M1-00614` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SILENTLY-DISCARD-NON-IPV4-VERSION-CRS-M1-00614` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00615-0819` | `CRS-M1-00615` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-GENERATE-AND-VALIDATE-UDP-CHECKSUMS-CRS-M1-00615` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00616-0885` | `CRS-M1-00616` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-APPLY-RFC-1123-TFTP-HOST-NOTES-WITHOUT-ADOPTING-MAIL-NETASCII-OR-BROADCAST-RRQ-CRS-M1-00616` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00617-0822` | `CRS-M1-00617` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-FIVE-TFTP-PACKET-TYPES-IDENTIFIED-BY-OPCODE-CRS-M1-00617` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00618-0823` | `CRS-M1-00618` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ASSIGN-TID-ON-RRQ-OR-WRQ-WITHOUT-MAIL-MODE-CRS-M1-00618` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00619-0824` | `CRS-M1-00619` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PLACE-OPCODE-IN-TFTP-HEADER-CRS-M1-00619` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00620-0831` | `CRS-M1-00620` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TERMINATE-ON-DATA-PACKET-OF-0-TO-511-BYTES-CRS-M1-00620` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00621-0832` | `CRS-M1-00621` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SEND-ERROR-PACKET-OPCODE-5-CRS-M1-00621` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00622-0833` | `CRS-M1-00622` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ACKNOWLEDGE-OPTION-NEGOTIATION-WITH-OACK-CRS-M1-00622` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00623-0834` | `CRS-M1-00623` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TERMINATE-TRANSFER-WITH-ERROR-CODE-8-CRS-M1-00623` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00624-0835` | `CRS-M1-00624` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-APPEND-OPTIONS-TO-RRQ-OR-WRQ-CRS-M1-00624` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00625-0836` | `CRS-M1-00625` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-BLKSIZE-AS-ASCII-OCTETS-FROM-8-THROUGH-65464-CRS-M1-00625` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00626-0840` | `CRS-M1-00626` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-TIMEOUT-AS-ASCII-SECONDS-FROM-1-THROUGH-255-CRS-M1-00626` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00627-0842` | `CRS-M1-00627` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUEST-TSIZE-ZERO-ON-RRQ-AND-RETURN-SIZE-IN-OACK-CRS-M1-00627` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00628-0813` | `CRS-M1-00628` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-UDP-LENGTH-AT-LEAST-EIGHT-OCTETS-CRS-M1-00628` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00629-0817` | `CRS-M1-00629` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-VERIFY-IP-HEADER-CHECKSUM-AND-SILENTLY-DISCARD-BAD-CRS-M1-00629` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00630-0818` | `CRS-M1-00630` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SUPPORT-IPV4-REASSEMBLY-CRS-M1-00630` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00631-0820` | `CRS-M1-00631` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SILENTLY-DISCARD-UDP-DATAGRAM-WITH-INVALID-CHECKSUM-CRS-M1-00631` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00632-0825` | `CRS-M1-00632` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-RRQ-WRQ-AS-OPCODE-FILENAME-AND-MODE-CRS-M1-00632` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00633-0826` | `CRS-M1-00633` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TERMINATE-TFTP-FILENAME-WITH-NUL-CRS-M1-00633` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00634-0827` | `CRS-M1-00634` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-DATA-PACKET-WITH-BLOCK-NUMBER-AND-DATA-CRS-M1-00634` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00635-0828` | `CRS-M1-00635` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-LIMIT-TFTP-DATA-FIELD-TO-ZERO-THROUGH-512-BYTES-CRS-M1-00635` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00636-0829` | `CRS-M1-00636` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-ACK-PACKET-WITH-OPCODE-4-AND-BLOCK-NUMBER-CRS-M1-00636` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00637-0830` | `CRS-M1-00637` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-ERROR-PACKET-AS-OPCODE-ERROR-CODE-AND-MESSAGE-CRS-M1-00637` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00638-0837` | `CRS-M1-00638` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-BLKSIZE-VALUE-IN-ASCII-CRS-M1-00638` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00639-0838` | `CRS-M1-00639` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-NEGOTIATE-BLKSIZE-LESS-OR-EQUAL-TO-CLIENT-VALUE-CRS-M1-00639` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00640-0839` | `CRS-M1-00640` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-OACK-BLKSIZE-OR-TERMINATE-WITH-ERROR-8-CRS-M1-00640` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00641-0841` | `CRS-M1-00641` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ECHO-CLIENT-TIMEOUT-VALUE-IN-OACK-CRS-M1-00641` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00642-0843` | `CRS-M1-00642` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SPECIFY-TSIZE-ON-WRQ-AND-ECHO-IN-OACK-CRS-M1-00642` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00643-0844` | `CRS-M1-00643` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MAY-ABORT-RRQ-WITH-ERROR-CODE-3-CRS-M1-00643` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00644-0845` | `CRS-M1-00644` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MAY-ABORT-WRQ-WITH-ERROR-CODE-3-CRS-M1-00644` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00645-0846` | `CRS-M1-00645` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TERMINATE-ON-DATA-SHORTER-THAN-NEGOTIATED-BLKSIZE-CRS-M1-00645` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00646-0847` | `CRS-M1-00646` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SEND-ZERO-LENGTH-FINAL-DATA-WHEN-FILE-IS-INTEGRAL-MULTIPLE-OF-BLKSIZE-CRS-M1-00646` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00647-0848` | `CRS-M1-00647` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-IGNORE-UNACKNOWLEDGED-OPTION-AND-KEEP-DEFAULT-PARAMETERS-CRS-M1-00647` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00648-0849` | `CRS-M1-00648` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-VERSION-AS-4-BITS-CRS-M1-00648` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00649-0850` | `CRS-M1-00649` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-IHL-AS-4-BITS-CRS-M1-00649` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00650-0851` | `CRS-M1-00650` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-TOS-AS-8-BITS-CRS-M1-00650` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00651-0852` | `CRS-M1-00651` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-TOTAL-LENGTH-AS-16-BITS-CRS-M1-00651` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00652-0853` | `CRS-M1-00652` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-IDENTIFICATION-AS-16-BITS-CRS-M1-00652` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00653-0854` | `CRS-M1-00653` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-FLAGS-AS-3-BITS-CRS-M1-00653` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00654-0855` | `CRS-M1-00654` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-FRAGMENT-OFFSET-AS-13-BITS-CRS-M1-00654` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00655-0856` | `CRS-M1-00655` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-TTL-AS-8-BITS-CRS-M1-00655` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00656-0857` | `CRS-M1-00656` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-PROTOCOL-AS-8-BITS-CRS-M1-00656` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00657-0858` | `CRS-M1-00657` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-HEADER-CHECKSUM-AS-16-BITS-CRS-M1-00657` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00658-0859` | `CRS-M1-00658` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-SOURCE-ADDRESS-AS-32-BITS-CRS-M1-00658` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00659-0860` | `CRS-M1-00659` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-DESTINATION-ADDRESS-AS-32-BITS-CRS-M1-00659` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00660-0861` | `CRS-M1-00660` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-DO-NOT-SUPPORT-TFTP-MAIL-TRANSFER-MODE-CRS-M1-00660` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00661-0862` | `CRS-M1-00661` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-COUNT-UDP-LENGTH-INCLUDING-EIGHT-OCTET-HEADER-CRS-M1-00661` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00662-0863` | `CRS-M1-00662` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-NEVER-RESEND-CURRENT-DATA-ON-DUPLICATE-ACK-CRS-M1-00662` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00663-0864` | `CRS-M1-00663` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-ADAPTIVE-TFTP-RETRANSMISSION-TIMEOUT-CRS-M1-00663` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00664-0865` | `CRS-M1-00664` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-CONFIGURABLE-TFTP-PATHNAME-ACCESS-CONTROL-CRS-M1-00664` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00665-0866` | `CRS-M1-00665` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SILENTLY-IGNORE-BROADCAST-TFTP-REQUEST-CRS-M1-00665` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00666-0867` | `CRS-M1-00666` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ALLOW-ONLY-ONE-SOURCE-END-SYSTEM-PER-VL-CRS-M1-00666` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00667-0868` | `CRS-M1-00667` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-VL-AS-UNIDIRECTIONAL-ONE-TO-MANY-CONNECTION-CRS-M1-00667` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00668-0869` | `CRS-M1-00668` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-BAG-AS-MINIMUM-INTERVAL-BETWEEN-CONSECUTIVE-VL-FRAMES-CRS-M1-00668` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00669-0870` | `CRS-M1-00669` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-BOUND-VL-FRAME-ARRIVAL-BY-MAXIMUM-ADMISSIBLE-JITTER-CRS-M1-00669` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00670-0871` | `CRS-M1-00670` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-CHARACTERISE-VL-BANDWIDTH-BY-BAG-AND-LMAX-CRS-M1-00670` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00671-0872` | `CRS-M1-00671` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ACCOMMODATE-VL-FRAMES-UP-TO-1518-BYTES-CRS-M1-00671` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00672-0873` | `CRS-M1-00672` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-HANDLE-BAG-VALUES-FROM-1-MS-TO-128-MS-CRS-M1-00672` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00673-0874` | `CRS-M1-00673` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RESTRICT-BAG-TO-POWERS-OF-TWO-MILLISECONDS-CRS-M1-00673` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00674-0899` | `CRS-M1-00674` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-VL-JITTER-AT-OR-BELOW-500-MICROSECONDS-CRS-M1-00674` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00675-0876` | `CRS-M1-00675` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-IDENTIFY-VL-ONLY-BY-MAC-DESTINATION-ADDRESS-CRS-M1-00675` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00676-0877` | `CRS-M1-00676` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-IHL-IN-32-BIT-WORDS-CRS-M1-00676` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00677-0878` | `CRS-M1-00677` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-IHL-AT-LEAST-5-CRS-M1-00677` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00678-0879` | `CRS-M1-00678` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-IPV4-TOTAL-LENGTH-IN-OCTETS-INCLUDING-HEADER-AND-DATA-CRS-M1-00678` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00679-0880` | `CRS-M1-00679` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-FRAGMENT-OFFSET-IN-8-OCTET-UNITS-CRS-M1-00679` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00680-0881` | `CRS-M1-00680` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ALLOW-IPV4-OPTIONS-TO-BE-PRESENT-OR-ABSENT-CRS-M1-00680` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00681-0882` | `CRS-M1-00681` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PAD-IPV4-HEADER-TO-32-BIT-BOUNDARY-CRS-M1-00681` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00682-0886` | `CRS-M1-00682` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-TX-TECHNOLOGICAL-LATENCY-BELOW-150US-PLUS-FRAME-DELAY-CRS-M1-00682` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00682-0937` | `CRS-M1-00682` | TIMING | `TIM-CRS-M1-00682` | AFDX 时序作为条件网络约束编入目录；绑定 M2 不执行 AFDX。 |
| `TR-CRS-M1-00682-0938` | `CRS-M1-00682` | CLOCK | `CLK_AFDX_ES` | AFDX 端系统时钟仅用于目录观察，不进入绑定状态机迁移。 |
| `TR-CRS-M1-00683-0887` | `CRS-M1-00683` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-RX-TECHNOLOGICAL-LATENCY-BELOW-150-MICROSECONDS-CRS-M1-00683` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00683-0939` | `CRS-M1-00683` | TIMING | `TIM-CRS-M1-00683` | AFDX 时序作为条件网络约束编入目录；绑定 M2 不执行 AFDX。 |
| `TR-CRS-M1-00683-0940` | `CRS-M1-00683` | CLOCK | `CLK_AFDX_ES` | AFDX 端系统时钟仅用于目录观察，不进入绑定状态机迁移。 |
| `TR-CRS-M1-00684-0888` | `CRS-M1-00684` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-BOUND-MAX-JITTER-BY-40US-PLUS-VL-LOAD-TERM-CRS-M1-00684` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00684-0941` | `CRS-M1-00684` | TIMING | `TIM-CRS-M1-00684` | AFDX 时序作为条件网络约束编入目录；绑定 M2 不执行 AFDX。 |
| `TR-CRS-M1-00684-0942` | `CRS-M1-00684` | CLOCK | `CLK_AFDX_ES` | AFDX 端系统时钟仅用于目录观察，不进入绑定状态机迁移。 |
| `TR-CRS-M1-00685-0889` | `CRS-M1-00685` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-BOUND-MAX-JITTER-BY-500-MICROSECONDS-EQUATION-CRS-M1-00685` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00685-0943` | `CRS-M1-00685` | TIMING | `TIM-CRS-M1-00685` | AFDX 时序作为条件网络约束编入目录；绑定 M2 不执行 AFDX。 |
| `TR-CRS-M1-00685-0944` | `CRS-M1-00685` | CLOCK | `CLK_AFDX_ES` | AFDX 端系统时钟仅用于目录观察，不进入绑定状态机迁移。 |
| `TR-CRS-M1-00686-0890` | `CRS-M1-00686` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-MAC-SOURCE-AS-INDIVIDUAL-AND-LOCALLY-ADMINISTERED-CRS-M1-00686` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00687-0891` | `CRS-M1-00687` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-SOURCE-CONSTANT-FIELD-TO-000000100000000000000000-CRS-M1-00687` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00688-0892` | `CRS-M1-00688` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-SOURCE-INDIVIDUAL-ADDRESS-BIT-TO-ZERO-CRS-M1-00688` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00689-0893` | `CRS-M1-00689` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-SOURCE-LOCALLY-ADMINISTERED-BIT-TO-ONE-CRS-M1-00689` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00690-0894` | `CRS-M1-00690` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-MAC-SOURCE-USER-DEFINED-ID-AS-16-BITS-CRS-M1-00690` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00691-0895` | `CRS-M1-00691` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-USER-DEFINED-ID-FOR-UNIQUE-MEANINGFUL-HOST-IDENTITY-CRS-M1-00691` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00692-0896` | `CRS-M1-00692` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-INTERFACE-ID-TO-IDENTIFY-REDUNDANT-AFDX-NETWORK-CRS-M1-00692` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00693-0897` | `CRS-M1-00693` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-INTERFACE-ID-001-AS-NETWORK-A-CRS-M1-00693` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00694-0898` | `CRS-M1-00694` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENCODE-INTERFACE-ID-010-AS-NETWORK-B-CRS-M1-00694` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00695-0900` | `CRS-M1-00695` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-ADN-ADDRESS-DETERMINATION-GUIDANCE-CRS-M1-00695` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD／INFORMATION 执行，也不激活 AFDX。 |
| `TR-CRS-M1-00696-0901` | `CRS-M1-00696` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KNOW-DESTINATION-ADDRESSES-AT-CONFIGURATION-TIME-CRS-M1-00696` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD／INFORMATION 执行，也不激活 AFDX。 |
| `TR-CRS-M1-00697-0902` | `CRS-M1-00697` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-DEFINE-ADN-ADDRESSING-PLAN-AND-RULES-CRS-M1-00697` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD／INFORMATION 执行，也不激活 AFDX。 |
| `TR-CRS-M1-00698-0903` | `CRS-M1-00698` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-IANA-WELL-KNOWN-UDP-PORTS-FOR-STANDARD-SERVICES-INCLUDING-TFTP-CRS-M1-00698` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD／INFORMATION 执行，也不激活 AFDX。 |
| `TR-CRS-M1-00699-0904` | `CRS-M1-00699` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ACCESS-PRIVATE-AERO-APPS-VIA-INTEGRATOR-OR-664P4-UDP-PORTS-CRS-M1-00699` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD／INFORMATION 执行，也不激活 AFDX。 |
| `TR-CRS-M1-00700-0905` | `CRS-M1-00700` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-DO-NOT-REASSIGN-WELL-KNOWN-COTS-PORTS-0-1023-CRS-M1-00700` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD／INFORMATION 执行，也不激活 AFDX。 |
| `TR-CRS-M1-00701-0906` | `CRS-M1-00701` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-DO-NOT-ROUTE-PRIVATE-ADDRESSES-OUTSIDE-THE-NETWORK-CRS-M1-00701` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD／INFORMATION 执行，也不激活 AFDX。 |
| `TR-CRS-M1-00702-0907` | `CRS-M1-00702` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-PROFILED-AERO-NETWORK-AS-IETF-PRIVATE-APPLICATION-CRS-M1-00702` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD／INFORMATION 执行，也不激活 AFDX。 |
| `TR-CRS-M1-00703-0908` | `CRS-M1-00703` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-PRIVATE-NETWORK-ID-FOR-PROFILED-NETWORKS-CRS-M1-00703` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD／INFORMATION 执行，也不激活 AFDX。 |
| `TR-CRS-M1-00704-0909` | `CRS-M1-00704` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ASSIGN-MAC-UNICAST-ADDRESSES-AT-CONFIGURATION-TIME-CRS-M1-00704` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD／INFORMATION 执行，也不激活 AFDX。 |
| `TR-CRS-M1-00705-0910` | `CRS-M1-00705` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-MAC-ADDRESSES-UNIQUE-UNDER-INTEGRATOR-SCHEME-CRS-M1-00705` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD／INFORMATION 执行，也不激活 AFDX。 |
| `TR-CRS-M1-00706-0911` | `CRS-M1-00706` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-UL-BIT-WHEN-INTEGRATOR-ASSIGNS-ADDRESSES-CRS-M1-00706` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD／INFORMATION 执行，也不激活 AFDX。 |
| `TR-CRS-M1-00707-0912` | `CRS-M1-00707` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-ALL-NETWORK-ADDRESSES-UNIQUE-CRS-M1-00707` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD／INFORMATION 执行，也不激活 AFDX。 |
| `TR-CRS-M1-00708-0913` | `CRS-M1-00708` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RESERVE-UDP-TCP-PORT-59-FOR-615A-DATA-LOADER-TFTP-CRS-M1-00708` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD／INFORMATION 执行，也不激活 AFDX。 |
| `TR-CRS-M1-00709-0914` | `CRS-M1-00709` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ASSIGN-UDP-PORT-24922-TO-FIND-PROTOCOL-CLIENT-CRS-M1-00709` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD／INFORMATION 执行，也不激活 AFDX。 |
| `TR-CRS-M1-00710-0915` | `CRS-M1-00710` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ALLOCATE-TABLE-2-1-ADDRESSES-FROM-RFC1918-PRIVATE-RANGES-CRS-M1-00710` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD／INFORMATION 执行，也不激活 AFDX。 |
| `TR-CRS-M1-00711-0916` | `CRS-M1-00711` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-TX-TECHNOLOGICAL-LATENCY-BETWEEN-PARTITION-DATA-AND-PHYSICAL-MEDIA-CRS-M1-00711` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00712-0917` | `CRS-M1-00712` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-START-TX-TECHNOLOGICAL-LATENCY-WHEN-LAST-PARTITION-BIT-IS-AVAILABLE-CRS-M1-00712` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00713-0918` | `CRS-M1-00713` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-END-TX-TECHNOLOGICAL-LATENCY-WHEN-LAST-FRAME-BIT-IS-ON-MEDIA-CRS-M1-00713` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00714-0919` | `CRS-M1-00714` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-TX-TECHNOLOGICAL-LATENCY-WITH-EMPTY-BUFFERS-NO-CONTENTION-AND-NO-IP-FRAGMENTATION-CRS-M1-00714` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00715-0920` | `CRS-M1-00715` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-DISTINGUISH-TECHNOLOGICAL-LATENCY-FROM-CONFIGURATION-LOAD-LATENCY-CRS-M1-00715` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00716-0921` | `CRS-M1-00716` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-DEFINE-TECHNOLOGICAL-LATENCY-AS-ACCEPT-PROCESS-AND-BEGIN-TX-WITH-NO-OTHER-TASK-CRS-M1-00716` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00717-0922` | `CRS-M1-00717` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ADD-FRAME-DELAY-FOR-PHYSICAL-LAYER-DELIVERY-CRS-M1-00717` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00718-0923` | `CRS-M1-00718` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-START-RX-TECHNOLOGICAL-LATENCY-WHEN-LAST-FRAME-BIT-IS-RECEIVED-CRS-M1-00718` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00719-0924` | `CRS-M1-00719` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-END-RX-TECHNOLOGICAL-LATENCY-WHEN-LAST-DATA-BIT-IS-AVAILABLE-TO-PARTITION-CRS-M1-00719` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00720-0925` | `CRS-M1-00720` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MEASURE-RX-TECHNOLOGICAL-LATENCY-WITH-EMPTY-BUFFERS-AND-NO-CONTENTION-CRS-M1-00720` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00721-0926` | `CRS-M1-00721` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SATISFY-BOTH-MAX-JITTER-EQUATIONS-SIMULTANEOUSLY-CRS-M1-00721` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00722-0927` | `CRS-M1-00722` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-MAX-JITTER-AS-MICROSECONDS-NBW-AS-BITS-PER-SECOND-AND-LMAX-AS-OCTETS-CRS-M1-00722` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00723-0928` | `CRS-M1-00723` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-COMPOSE-MAC-SOURCE-AS-24-PLUS-16-PLUS-3-PLUS-5-BIT-FIELDS-CRS-M1-00723` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00724-0929` | `CRS-M1-00724` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-MAC-SOURCE-CONSTANT-TAIL-TO-00000-CRS-M1-00724` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00725-0930` | `CRS-M1-00725` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-MAC-SOURCE-CONSTRUCTION-ALGORITHM-AS-NOT-UNIQUELY-RECOMMENDED-CRS-M1-00725` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00726-0931` | `CRS-M1-00726` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-000-AS-NOT-USED-CRS-M1-00726` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00727-0932` | `CRS-M1-00727` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-011-AS-NOT-USED-CRS-M1-00727` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00728-0933` | `CRS-M1-00728` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-100-AS-NOT-USED-CRS-M1-00728` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00729-0934` | `CRS-M1-00729` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-101-AS-NOT-USED-CRS-M1-00729` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00730-0935` | `CRS-M1-00730` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-110-AS-SOURCE-NOR-USED-CRS-M1-00730` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00731-0936` | `CRS-M1-00731` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-INTERFACE-ID-111-AS-NOT-USED-CRS-M1-00731` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00732-0945` | `CRS-M1-00732` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-P3-RFC-OPTION-RESTRICTION-PHILOSOPHY-CRS-M1-00732` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00733-0946` | `CRS-M1-00733` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-P3-CONTENTS-LIMITED-TO-RFC-DELTAS-CRS-M1-00733` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00734-0947` | `CRS-M1-00734` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-COMPOSE-AFDX-SWITCH-FROM-FIVE-FUNCTIONAL-BLOCKS-CRS-M1-00734` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00735-0948` | `CRS-M1-00735` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-CONTROL-AFDX-SWITCH-FUNCTIONS-WITH-STATIC-CONFIGURATION-TABLES-CRS-M1-00735` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00736-0949` | `CRS-M1-00736` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-SWITCH-END-SYSTEM-TO-COMPLY-WITH-SECTION-3-EXCEPT-REDUNDANCY-CRS-M1-00736` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00737-0950` | `CRS-M1-00737` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-SWITCH-END-SYSTEM-UNICAST-MAC-AS-SOURCE-ADDRESS-CRS-M1-00737` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00738-0951` | `CRS-M1-00738` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-615A-SESSION-ACROSS-OPS-TO-DL-TRANSITION-CRS-M1-00738` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00739-0952` | `CRS-M1-00739` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-615A-AND-665-TO-UPLOAD-SWITCH-SOFTWARE-AND-CONFIGURATION-CRS-M1-00739` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00740-0953` | `CRS-M1-00740` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-AFDX-SWITCH-PHYSICAL-LAYER-TO-COMPLY-WITH-664P2-CRS-M1-00740` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00741-0954` | `CRS-M1-00741` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-AS-NOT-USED-ON-AFDX-CRS-M1-00741` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00742-0955` | `CRS-M1-00742` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-CHECKSUM-GENERATE-AND-CHECK-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00742` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00743-0956` | `CRS-M1-00743` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-AFDX-END-SYSTEM-INTERNET-LAYER-TO-IMPLEMENT-IP-CRS-M1-00743` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00744-0957` | `CRS-M1-00744` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-AFDX-END-SYSTEM-INTERNET-LAYER-TO-IMPLEMENT-ICMP-CRS-M1-00744` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00745-0958` | `CRS-M1-00745` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SILENTLY-DISCARD-NON-IPV4-DATAGRAMS-CRS-M1-00745` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00746-0959` | `CRS-M1-00746` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-AFDX-UDP-CHECKSUM-UNUSED-COMMENT-CRS-M1-00746` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00747-0960` | `CRS-M1-00747` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-SILENT-BAD-UDP-CHECKSUM-DISCARD-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00747` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00748-0961` | `CRS-M1-00748` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PASS-ICMP-MESSAGES-TO-APPLICATION-LIMITED-TO-ECHO-REQUEST-CRS-M1-00748` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00749-0962` | `CRS-M1-00749` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-PORT-UNREACHABLE-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00749` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00750-0963` | `CRS-M1-00750` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-FORBID-REMOTE-MULTIHOMING-AT-APPLICATION-LAYER-ON-AFDX-CRS-M1-00750` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00751-0964` | `CRS-M1-00751` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-LOCAL-MULTIHOMING-ON-AFDX-CRS-M1-00751` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00752-0965` | `CRS-M1-00752` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-LOG-DISCARDED-DATAGRAMS-ON-AFDX-CRS-M1-00752` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00753-0966` | `CRS-M1-00753` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-DISCARDED-DATAGRAMS-IN-COUNTER-ON-AFDX-CRS-M1-00753` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00754-0967` | `CRS-M1-00754` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENTER-OPS-AFTER-COMPATIBLE-INIT-WHEN-SHOP-INACTIVE-CRS-M1-00754` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00755-0968` | `CRS-M1-00755` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-OPS-MODE-615A-INFORMATION-AND-FIND-CRS-M1-00755` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00756-0969` | `CRS-M1-00756` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENTER-DL-FROM-INIT-ONLY-WHEN-GROUND-AND-COMPATIBILITY-FAIL-OR-EMPTY-CRS-M1-00756` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00757-0970` | `CRS-M1-00757` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ENTER-DL-FROM-OPS-ONLY-WHEN-GROUND-UPLOAD-INIT-AND-HEADER-ACCEPTED-CRS-M1-00757` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00758-0971` | `CRS-M1-00758` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PROVIDE-DL-MODE-615A-INFORMATION-UPLOAD-AND-FIND-CRS-M1-00758` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00759-0972` | `CRS-M1-00759` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-SEND-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00759` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00760-0973` | `CRS-M1-00760` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-UDP-IP-OPTIONS-DOWN-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00760` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00761-0974` | `CRS-M1-00761` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-GATEWAY-FORWARDING-SPEC-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00761` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00762-0975` | `CRS-M1-00762` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-EMBEDDED-GATEWAY-SWITCH-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00762` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00763-0976` | `CRS-M1-00763` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-NON-GATEWAY-DEFAULT-AS-NOT-APPLICABLE-ON-AFDX-CRS-M1-00763` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00764-0977` | `CRS-M1-00764` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-AFDX-GATEWAY-AUTOCONFIGURATION-ROW-UNMARKED-CRS-M1-00764` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00765-0978` | `CRS-M1-00765` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PERFORM-OPS-FILTERING-POLICING-SWITCHING-FROM-OPS-CONFIG-CRS-M1-00765` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00766-0979` | `CRS-M1-00766` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-OPS-FAULT-HEALTHY-INDICATOR-TO-HEALTHY-CRS-M1-00766` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00767-0980` | `CRS-M1-00767` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-DL-UPLOAD-AS-PREFERABLY-EXCLUSIVE-CRS-M1-00767` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00768-0981` | `CRS-M1-00768` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-DEDICATE-SWITCH-TO-UPLOAD-DURING-DL-UPLOAD-CRS-M1-00768` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00769-0982` | `CRS-M1-00769` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-DEFAULT-RECEPTION-VL-FOR-DATALOADING-CRS-M1-00769` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00770-0983` | `CRS-M1-00770` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RECORD-TWELVE-PIN-POSITION-IDENTIFICATION-AS-EXAMPLE-CRS-M1-00770` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00771-0984` | `CRS-M1-00771` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-STATED-TWELVE-PIN-DEFINITIONS-IF-TWELVE-PINS-CHOSEN-CRS-M1-00771` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00772-0985` | `CRS-M1-00772` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-KEEP-DEFAULT-CONFIGURATION-TABLE-RESIDENT-CRS-M1-00772` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00773-0986` | `CRS-M1-00773` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-DEFAULT-PHYSICAL-PORT-SPEED-100MBPS-WITHOUT-AUTONEG-CRS-M1-00773` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00774-0987` | `CRS-M1-00774` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-DEFAULT-RECEPTION-VL-FIELDS-IN-NONVOLATILE-MEMORY-CRS-M1-00774` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00775-0988` | `CRS-M1-00775` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-DEFAULT-TRANSMISSION-VL-FIELDS-IN-NONVOLATILE-MEMORY-CRS-M1-00775` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00776-0989` | `CRS-M1-00776` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-DEFAULT-TRANSMISSION-VL-FOR-DATALOADING-ACKNOWLEDGE-CRS-M1-00776` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00777-0990` | `CRS-M1-00777` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-OPS-CONFIGURATION-FILE-615A-665-FIELD-LOADABLE-CRS-M1-00777` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00778-0991` | `CRS-M1-00778` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-FILTERING-POLICING-FORWARDING-TABLE-PARAMETER-SET-CRS-M1-00778` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00779-0992` | `CRS-M1-00779` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-LISTED-PARAMETERS-TO-CONFIGURE-FILTER-POLICE-FORWARD-CRS-M1-00779` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00780-0993` | `CRS-M1-00780` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PERFORM-DL-END-SYSTEM-FROM-DEFAULT-CONFIGURATION-TABLE-CRS-M1-00780` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00781-0994` | `CRS-M1-00781` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-SET-DL-FAULT-HEALTHY-INDICATOR-TO-HEALTHY-CRS-M1-00781` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00782-0995` | `CRS-M1-00782` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-RETURN-TO-INIT-AT-END-OF-DL-MODE-CRS-M1-00782` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00783-0996` | `CRS-M1-00783` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-TREAT-DL-MODE-END-AS-615A-DATA-LOADING-FUNCTION-END-CRS-M1-00783` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00784-0997` | `CRS-M1-00784` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-LIMIT-SWITCH-FIELD-LOADABLE-SOFTWARE-TO-OPS-CONFIG-AND-OPS-SOFTWARE-CRS-M1-00784` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00785-0998` | `CRS-M1-00785` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-REQUIRE-FIELD-LOADABLE-FILES-IDENTICAL-ACROSS-AIRCRAFT-SWITCHES-CRS-M1-00785` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00786-0999` | `CRS-M1-00786` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MAKE-SWITCH-CONFIGURATION-ACCESSIBLE-VIA-615A-INFORMATION-CRS-M1-00786` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00787-1000` | `CRS-M1-00787` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-LEARN-DATALOADER-IP-FROM-SOURCE-ADDRESS-CRS-M1-00787` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00788-1001` | `CRS-M1-00788` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-PIN-PROGRAMMING-FOR-POSITION-AND-DEFAULT-MAC-IP-CRS-M1-00788` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00789-1002` | `CRS-M1-00789` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-READ-PROGRAM-PINS-IN-INIT-ONLY-WHEN-GROUND-BEFORE-SAFETY-TEST-CRS-M1-00789` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00790-1003` | `CRS-M1-00790` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-DO-NOT-READ-PROGRAM-PINS-WHEN-GROUND-CONDITION-FALSE-CRS-M1-00790` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00791-1004` | `CRS-M1-00791` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-USE-LAST-MEMORIZED-PIN-VALUES-WHEN-NOT-GROUND-CRS-M1-00791` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00792-1005` | `CRS-M1-00792` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-CHECK-TWELVE-PROGRAM-PINS-WITH-PARITY-BIT-CRS-M1-00792` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00793-1006` | `CRS-M1-00793` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-MEMORIZE-PROGRAM-PINS-IN-NVM-AFTER-PARITY-PASS-CRS-M1-00793` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00794-1007` | `CRS-M1-00794` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-ACQUIRE-SWITCH-POSITION-WITH-TWELVE-PINS-P1-P12-CRS-M1-00794` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00795-1008` | `CRS-M1-00795` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-CODE-PIN-GROUND-AS-ONE-CRS-M1-00795` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00796-1009` | `CRS-M1-00796` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-CODE-PIN-OPEN-AS-ZERO-CRS-M1-00796` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00797-1010` | `CRS-M1-00797` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-PROCESS-AT-LEAST-4096-VLS-IN-FILTER-POLICE-FORWARD-CRS-M1-00797` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00798-1011` | `CRS-M1-00798` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-INPUT-PHYSICAL-PORT-CRS-M1-00798` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00799-1012` | `CRS-M1-00799` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-OUTPUT-PHYSICAL-PORTS-CRS-M1-00799` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00800-1013` | `CRS-M1-00800` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-MAC-DESTINATION-CRS-M1-00800` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00801-1014` | `CRS-M1-00801` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-BAG-CRS-M1-00801` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00802-1015` | `CRS-M1-00802` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-MAX-JITTER-CRS-M1-00802` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00803-1016` | `CRS-M1-00803` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-ACCOUNT-CRS-M1-00803` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00804-1017` | `CRS-M1-00804` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-SMAX-CRS-M1-00804` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00805-1018` | `CRS-M1-00805` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-SMIN-CRS-M1-00805` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00806-1019` | `CRS-M1-00806` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-VL-PRIORITIZATION-CRS-M1-00806` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00807-1020` | `CRS-M1-00807` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-MAX-DELAY-CRS-M1-00807` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00808-1021` | `CRS-M1-00808` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-STATE-CRS-M1-00808` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00809-1022` | `CRS-M1-00809` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-SPEED-CRS-M1-00809` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00810-1023` | `CRS-M1-00810` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-LOW-PRIORITY-BUFFER-CRS-M1-00810` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00811-1024` | `CRS-M1-00811` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-FILTER-TABLE-PER-PORT-HIGH-PRIORITY-BUFFER-CRS-M1-00811` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00812-1025` | `CRS-M1-00812` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-VL-IDENTIFIER-CRS-M1-00812` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00813-1026` | `CRS-M1-00813` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-SMAX-CRS-M1-00813` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00814-1027` | `CRS-M1-00814` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-RX-BAG-CRS-M1-00814` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00815-1028` | `CRS-M1-00815` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-VL-IDENTIFIER-CRS-M1-00815` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00816-1029` | `CRS-M1-00816` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-BAG-CRS-M1-00816` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00817-1030` | `CRS-M1-00817` | OBJECT-CONSTRAINT | `OBJ-SUPPORTING-INCLUDE-DEFAULT-TX-SMAX-CRS-M1-00817` | 支持来源谓词记为数据对象约束；绑定 M2 不扩大 UPLOAD/INFORMATION 执行。 |
| `TR-CRS-M1-00818-1031` | `CRS-M1-00818` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00819-1032` | `CRS-M1-00819` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00820-1033` | `CRS-M1-00820` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00821-1034` | `CRS-M1-00821` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00822-1035` | `CRS-M1-00822` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00823-1036` | `CRS-M1-00823` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00824-1037` | `CRS-M1-00824` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00825-1038` | `CRS-M1-00825` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00826-1039` | `CRS-M1-00826` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00827-1040` | `CRS-M1-00827` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00828-1041` | `CRS-M1-00828` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00829-1042` | `CRS-M1-00829` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00830-1043` | `CRS-M1-00830` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00831-1044` | `CRS-M1-00831` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00832-1045` | `CRS-M1-00832` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00833-1046` | `CRS-M1-00833` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00834-1047` | `CRS-M1-00834` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00835-1048` | `CRS-M1-00835` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00836-1049` | `CRS-M1-00836` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00837-1050` | `CRS-M1-00837` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00838-1051` | `CRS-M1-00838` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00839-1052` | `CRS-M1-00839` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00840-1053` | `CRS-M1-00840` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00841-1054` | `CRS-M1-00841` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00842-1055` | `CRS-M1-00842` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00843-1056` | `CRS-M1-00843` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00844-1057` | `CRS-M1-00844` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00845-1058` | `CRS-M1-00845` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00846-1059` | `CRS-M1-00846` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00847-1060` | `CRS-M1-00847` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00848-1061` | `CRS-M1-00848` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00849-1062` | `CRS-M1-00849` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00850-1063` | `CRS-M1-00850` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00851-1064` | `CRS-M1-00851` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00852-1065` | `CRS-M1-00852` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00853-1066` | `CRS-M1-00853` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00854-1067` | `CRS-M1-00854` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00855-1068` | `CRS-M1-00855` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |
| `TR-CRS-M1-00856-1069` | `CRS-M1-00856` | SCOPE | `SCOPE` | 已记录 645 语义叶；绑定 M2 不执行 CRC、校验值或命名算法。 |

## 基础设施前提

- `NET-PREMISE-IPV4-UDP` `NOT-ESTABLISHED` — 底层 IPv4/UDP 服务须遵循适用 IETF 主机要求，不采用 P3 特有偏差。此项作为基础设施前提保留；未声称实现符合性或完整 RFC 需求清单。M2 须规划其验证，之后才可批准任何执行配置。
- `PREM-RFC-1123` `NOT-ESTABLISHED` — 仅纳入当前 IPv4/UDP 路径真实触发的主机要求。RFC 1123 不替代 RFC 1122。

## 行动

| ID | 状态 | 责任 | 门禁 | 说明 |
|---|---|---|---|---|
| `A-1` | `EXECUTED-SUCCESSOR-M1-DELTA-PENDING-RG1` | INCREMENTAL-RG1 | PROFILE-MODEL-REFINEMENT-GATE | CR-2026-011 已执行后继身份（6.4.4 为 LUR、6.4.5 为 LUS、LUR 写端点为 DL WRQ／TH ACK／DL DATA）。仍须独立 RG1。这是有界 M2 基线，不是开发就绪 CRS。 |
| `A-2` | `CANDIDATE-PARTIAL` | M2-RG1 | PROFILE-MODEL-REFINEMENT-GATE | RFC-2347 选项传输与 RFC-2348 块大小为候选边；1785/2349 仍无活动 615A 单元。 |
| `A-3` | `CANDIDATE-IN-MODEL` | M2-RG2 | PROFILE-MODEL-REFINEMENT-GATE | 已恢复带重试项的附件 4 方程；时钟使能超时迁移。 |
| `A-4` | `DEFERRED` | FUTURE-TAXONOMY-CR | SCOPE-EXPANSION-GATE | 未执行 requirementKind 分类扩展。 |
| `F-1` | `DEFERRED` | PRODUCT-SCOPE | SCOPE-EXPANSION-GATE | CR-2026-012 下已有 FIND CRS 候选；绑定 M2 仍不建模 FIND。模型精化待定。 |
| `F-2` | `DEFERRED` | PRODUCT-SCOPE | SCOPE-EXPANSION-GATE | AFDX CRS 候选为条件化部署；绑定 M2 仍未选择 AFDX。模型精化待定。 |
| `F-3` | `RETAINED-EXCLUSION` | M2-RG0 | SCOPE-EXPANSION-GATE | 保留 665 媒体集排除。 |
| `F-4` | `INCOMPLETE-IDENTITY-ONLY` | M2-RG1 | PROFILE-MODEL-REFINEMENT-GATE | 仅有 P2 身份；无条款级模型目标。 |
| `F-5` | `DEFERRED` | EDITORIAL | SCOPE-EXPANSION-GATE | 未做标签统一。 |
| `NET-ISSUE-EDITION` | `ACCEPTED-CURRENT-EDITION-P3-1-AFDX-DEFERRED` | INDEPENDENT-RG0 | PROFILE-MODEL-REFINEMENT-GATE | 所有者接受 664P3-1 作为本 M2 输入版次；664P7 保持已登记且 AFDX 未选。 |
| `RFC1122/IPv4/UDP` | `PREMISE-PLANNED` | M6-CONFIGURATION | PROJECT-CONFIGURATION-GATE | IPv4/UDP 验证计划用于 Configuration。 |
| `RFC1123` | `PREMISE-LIMITED` | M6-CONFIGURATION | PROJECT-CONFIGURATION-GATE | RFC 1123 不替代 RFC 1122。 |
| `ARINC645` | `BLOCKED` | SOURCE-ACQUISITION | SOURCE-TECHNICAL-DIRECTION-GATE | 完整性能力保持未建立。 |
| `P7/AID/address` | `DEFERRED-UNSELECTED-DEPLOYMENT` | PRODUCT-SCOPE | SCOPE-EXPANSION-GATE | 未选择的 AFDX 寻址保持延期。 |
| `README-P2-DISPLAY` | `CLOSED-IN-THIS-PR` | M2-AUTHOR | PROFILE-MODEL-REFINEMENT-GATE | 保留 displayGroup 展示。 |
| `M1-LEDGER` | `RECORDED-IN-INPUT-ACCEPTANCE` | M2-AUTHOR | PROFILE-MODEL-REFINEMENT-GATE | M1 合并事实仍在 inputAcceptance。 |
| `M1-FILE-IDENTITY-6-4-4` | `CLOSED-BY-SUCCESSOR-M1-DELTA` | INCREMENTAL-RG1 | PROFILE-MODEL-REFINEMENT-GATE | 后继 M1 增量已在 CR-2026-011 下执行。冻结合并字节作为保留记录不变。仍须独立 RG1。 |
| `LUI-FIELD-TABLE-GAP` | `KNOWN-GAP-NO-DEDICATED-TABLE` | M1-EXPANDED | EXECUTABLE-FOUNDATION-GATE | 6.4.4 改为 LUR 后没有专用 LUI 字段表。LUI 仍是序列文件。不编造字段。 |

## 序列端点绑定

| CRS | 迁移 | 事件 | 发送者 | 接收者 | 动作 | 对象 | 操作码 | 文件 | 方向 | 层级 |
|---|---|---|---|---|---|---|---|---|---|---|
| `CRS-M1-00365` | `T_UPL_LUR_WRQ` | `EV_DL_WRQ_LUR` | `DATA-LOADER` | `TARGET-HARDWARE` | `SEND-TFTP-WRITE-REQUEST` | `LUR` | `WRQ` | `LUR` | `DL-TO-TH` | `NETWORK-VISIBLE` |
| `CRS-M1-00366` | `T_UPL_LUR_ACK` | `EV_TH_ACK_LUR` | `TARGET-HARDWARE` | `DATA-LOADER` | `ACKNOWLEDGE` | `LUR-WRITE-REQUEST` | `ACK` | `LUR` | `TH-TO-DL` | `NETWORK-VISIBLE` |
| `CRS-M1-00367` | `T_UPL_LUR_XFER` | `EV_DL_DATA_LUR` | `DATA-LOADER` | `TARGET-HARDWARE` | `TRANSFER` | `LUR` | `DATA` | `LUR` | `DL-TO-TH` | `NETWORK-VISIBLE` |

## 来源精化

- `REF-A1-00143-BLOCKED-BY-FILE-IDENTITY` — `CANDIDATE-REFINEMENT` — 后继 M1 增量（CR-2026-011）将 CRS-M1-00143 记为 6.4.4 的 LUR 散文并含 HEADER-FILE。共享对象 HEADER-FILE 现支持到 CRS-M1-00217 的候选 665 边。仍须独立 RG1。能力保持未建立。 （至 `CRS-M1-00217` 2.2.3.1）
- `REF-A1-00315-BLOCKED-BY-FILE-IDENTITY` — `CANDIDATE-REFINEMENT` — 后继 M1 增量将表 6.4.4-1 的 FIELD-LOAD-PART-NUMBER-NAME 记为 LUR。共享对象 LOAD-PART-NUMBER 现支持到 CRS-M1-00212 的候选 665 边。仍须独立 RG1。 （至 `CRS-M1-00212` 2.1.1）
- `REF-SEQ-00365-WRQ-ACTOR` — `CANDIDATE-REFINEMENT` — 后继 M1 增量将 LUR 写三元组对齐到 §6.3.2 图 A 与 TFTP 写机器：DATA-LOADER 向 TARGET-HARDWARE 发 WRQ，TARGET-HARDWARE 向 DATA-LOADER 发 ACK，DATA-LOADER 向 TARGET-HARDWARE 发 DATA。DLA 是加载器应用层，不是网络 WRQ/ACK 端点。仍须独立 RG1。 （至 `None` ）
- `REF-A2-TFTP-OPTION-2347` — `CANDIDATE-REFINEMENT` — 615A 5.3.2.2 要求传输 TFTP 选项。RFC 2347 §2 是选项扩展机制。该边使用公共检索身份，不伪造 PDF 页码。不声称完整 RFC-2347 符合性。 （至 `RFC-2347` 2）
- `REF-A2-BLOCKSIZE-2348` — `CANDIDATE-REFINEMENT` — 615A 5.3.2.3.8.1 是 M1 已纳入的 Blocksize Option Implementation 单元（CRS-M1-00034）并带 DEP-RFC-2348。不能用 blksize 词形搜索否定该来源。RFC 2348 §2 是候选编码。能力保持未建立。 （至 `RFC-2348` 2）
- `REF-A2-NO-RFC-1785-ACTIVE-EDGE` — `NOT-ESTABLISHED-NO-ACTIVE-SOURCE-UNIT` — UPLOAD/INFORMATION 选项单元未点名 RFC 1785 协商选项通告。P7 列举仍随未选择的 AFDX。 （至 `RFC-1785` ）
- `REF-A2-NO-RFC-2349-NAME` — `NOT-ESTABLISHED-NO-ACTIVE-SOURCE-UNIT` — 615A 异常与 DLP 定时器是协议参数，不是已识别的 RFC-2349 timeout/tsize 选项单元。 （至 `RFC-2349` ）
- `REF-P2-PHYSICAL-ETHERNET` — `INCOMPLETE-IDENTITY-ONLY` — 已记录 P2 物理身份。本候选未交付条款级模型目标。这仍是未完成任务，不是有边界追踪。 （至 `ARINC-664-2` ）
- `REF-EDITION-P3-1` — `CONDITIONAL-INPUT-PENDING-RG0` — P3-1 仍为有条件历史输入。独立 RG0 仍决定版次接受。不翻转 M1 blocksM1Approval 快照。 （至 `ARINC-664-3` ）
- `REF-EDITION-P7-BASE` — `CONDITIONAL-INPUT-PENDING-RG0` — P7 初版仅作为延期 AFDX 语境记录。 （至 `ARINC-664-7` ）

## 网络关系处置

- `NET-REL-001` → `ACTIVE-NORMATIVE-REFINEMENT`（M1 `APPLICABILITY-REVIEW-PENDING`）
- `NET-REL-002` → `INFRASTRUCTURE-PREMISE`（M1 `APPLICABILITY-REVIEW-PENDING`）
- `NET-REL-003` → `INFORMATIONAL-RETAINED`（M1 `NO-NORMATIVE-OVERRIDE`）
- `NET-REL-004` → `ACTIVE-NORMATIVE-REFINEMENT`（M1 `APPLICABILITY-REVIEW-PENDING`）
- `NET-REL-005` → `DEFERRED-UNSELECTED-DEPLOYMENT`（M1 `DEFERRED-FUTURE-SCOPE`）
- `NET-REL-006` → `DEFERRED-UNSELECTED-DEPLOYMENT`（M1 `DEFERRED-FUTURE-SCOPE`）
- `NET-REL-007` → `DEFERRED-UNSELECTED-DEPLOYMENT`（M1 `DEFERRED-FUTURE-SCOPE`）
- `NET-REL-008` → `DEFERRED-UNSELECTED-DEPLOYMENT`（M1 `DEFERRED-FUTURE-SCOPE`）
- `NET-REL-009` → `DEFERRED-UNSELECTED-DEPLOYMENT`（M1 `DEFERRED-FUTURE-SCOPE`）
- `NET-REL-010` → `DEFERRED-UNSELECTED-DEPLOYMENT`（M1 `DEFERRED-FUTURE-SCOPE`）
- `NET-REL-011` → `DEFERRED-UNSELECTED-DEPLOYMENT`（M1 `DEFERRED-FUTURE-SCOPE`）
- `NET-REL-012` → `DEFERRED-UNSELECTED-DEPLOYMENT`（M1 `DEFERRED-FUTURE-SCOPE`）
- `NET-REL-013` → `DEFERRED-UNSELECTED-DEPLOYMENT`（M1 `DEFERRED-FUTURE-SCOPE`）
- `NET-REL-014` → `DEFERRED-UNSELECTED-DEPLOYMENT`（M1 `DEFERRED-FUTURE-SCOPE`）
- `NET-REL-015` → `DEFERRED-UNSELECTED-DEPLOYMENT`（M1 `DEFERRED-FUTURE-SCOPE`）
- `NET-REL-016` → `DEFERRED-UNSELECTED-DEPLOYMENT`（M1 `DEFERRED-FUTURE-SCOPE`）
- `NET-REL-017` → `DEFERRED-UNSELECTED-DEPLOYMENT`（M1 `DEFERRED-FUTURE-SCOPE`）

## 离散见证

- `W-UPL-ACCEPT` UPLOAD 初始化接受：payload.decision=ACCEPT 使能该分支；守卫求值后再写入 lastDecision。（4 步）
- `W-UPL-REJECT` 从 lastDecision=NONE 起，payload.decision=REJECT 使能 UPLOAD 初始化拒绝。（4 步）
- `W-INF-ACCEPT` INFORMATION 初始化接受使用同一有类型 payload，而不是预先写好的 lastDecision。（4 步）
- `W-INF-REJECT` INFORMATION 初始化拒绝来自 payload.decision=REJECT。（4 步）
- `W-LIST-NOT-READY` 初始化接受后列表尚未提交；LUR WRQ 不能使能。（5 步）
- `W-LIST-OFFERED-NOT-READY` 列表已提交但尚未收到 LUS-0001 时，LUR WRQ 仍不能使能。（6 步）
- `W-LUR-AFTER-READY` LUS-0001 建立会话内列表就绪；此后才使能数据加载器 LUR WRQ、目标硬件 ACK 与数据加载器 DATA。（9 步）
- `W-SESSION-RESET` INFORMATION 完成后再启动 UPLOAD 时清除列表就绪；提交列表后 LUR WRQ 仍不能使能。（16 步）
- `W-WAIT-NOT-BEFORE` CLK_WAIT 低于 MESSAGE_TIMER_VALUE 时禁止 WAIT 重试；到达闭下界后才使能。（14 步）
- `W-ACCEPT-WITHOUT-PAYLOAD` 仅有 lastDecision 不能使能接受；缺少 payload.decision 时守卫为假。（4 步）

## 阻塞输入

- `M1-FILE-IDENTITY-6-4-4` `CLOSED-BY-SUCCESSOR-M1-DELTA` 授权 `CR-2026-009` blocksFinalApproval=`False` — 后继 M1 增量已在 CR-2026-011 下执行。冻结合并字节不变。仍须独立 RG1。
- `SEQ-LUR-WRQ-ACTOR` `CLOSED-BY-SUCCESSOR-M1-DELTA` 授权 `CR-2026-009` blocksFinalApproval=`False` — 后继 M1 的 LUR 写端点为 DATA-LOADER→TARGET-HARDWARE WRQ、TARGET-HARDWARE→DATA-LOADER ACK、DATA-LOADER→TARGET-HARDWARE DATA。冻结合并字节不变。
- `NET-ISSUE-EDITION` `ACCEPTED-CURRENT-EDITION-P3-1-AFDX-DEFERRED` 授权 `CR-2026-009` blocksFinalApproval=`False` — 所有者接受 664P3-1 作为本 M2 输入版次；664P7 保持已登记且 AFDX 未选。

## 分析边界

- 无时：`GRAPH-CONNECTIVITY-ON-DECLARED-TRANSITIONS`
- 定时：`NOT-CHECKED`
- 未证明：timed reachability, implementation conformance, network-stack conformance, LUI field-table predicates

## 评审控制

- rg0 `PENDING-EXTERNAL-REVIEW`；rg1 `PENDING-EXTERNAL-REVIEW`；rg2 `PENDING-EXTERNAL-REVIEW`
- reviewHead `UNBOUND-DRAFT`；formalApproval `EXTERNAL-JOINT-CONDITION-NOT-YET-SATISFIED`；blocksFinalApproval `True`
