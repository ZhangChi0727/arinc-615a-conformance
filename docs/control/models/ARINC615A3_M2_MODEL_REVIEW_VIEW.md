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
- Successor delta `CR-2026-011` authorized by `CR-2026-009`; doesNotTransplantFrozenApproval=`True`
- Predecessor input artifact commit `402e8371b0237aec4691bab0b44e502f4ac1a7c4` tree `26ea73a18fafbd4ba93c9dbb2890eb8453b0ad97`

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

## Clocks

| ID | Scope | Correlation | Reset on | Meaning |
|---|---|---|---|---|
| `CLK_TFTP` | PER-CORRELATION-KEY | TFTP-PEER-AND-TRANSFER | `T_INF_LCI_RRQ`, `T_UPL_LUI_RRQ`, `T_UPL_LUR_WRQ`, `T_UPL_FILE_RRQ` | Time since last TFTP packet of the correlated transfer. |
| `CLK_DLP` | PER-CORRELATION-KEY | TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE | `T_INF_ACCEPT_INIT`, `T_UPL_ACCEPT_INIT`, `T_UPL_LUR_WRQ`, `T_UPL_FILE_RRQ` | Inter-operation / inter-transfer DLP clock. |
| `CLK_EXCEPTION` | PER-CORRELATION-KEY | STATUS-EXCEPTION-OBJECT | `T_ENTER_UPL_EXC`, `T_ENTER_INF_EXC`, `T_INF_LCS_WRQ` | Exception silence clock. |
| `CLK_WAIT` | PER-CORRELATION-KEY | TFTP-PEER-AND-REJECTED-TRANSFER-REQUEST | `T_WAIT_FROM_UPL_FILE`, `T_WAIT_FROM_UPL_LUR`, `T_WAIT_FROM_INF_LCI`, `T_WAIT_FROM_INF_LCL` | Delay since the WAIT message that forbids retry until the carried timer elapses. |

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
| `TR-CRS-M1-00100-0110` | `CRS-M1-00100` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00100-0111` | `CRS-M1-00100` | TIMING | `TIM-CRS-M1-00100` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00100-0112` | `CRS-M1-00100` | CLOCK | `CLK_EXCEPTION` | Clock used by this timing obligation. |
| `TR-CRS-M1-00101-0113` | `CRS-M1-00101` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION supporting obligation on the LCI/LCL/LCS machine. |
| `TR-CRS-M1-00101-0114` | `CRS-M1-00101` | TIMING | `TIM-CRS-M1-00101` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00101-0115` | `CRS-M1-00101` | CLOCK | `CLK_EXCEPTION` | Clock used by this timing obligation. |
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
| `TR-CRS-M1-00188-0228` | `CRS-M1-00188` | INTERFACE | `IF_TFTP` | TFTP interface premise for BOUND-INTER-TRANSFER-DURATION-BY-DLP-EQUATION. |
| `TR-CRS-M1-00188-0229` | `CRS-M1-00188` | TIMING | `TIM-CRS-M1-00188` | Timing catalog row with source relation and clock enablement. |
| `TR-CRS-M1-00188-0230` | `CRS-M1-00188` | CLOCK | `CLK_DLP` | Clock used by this timing obligation. |
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
| `TR-CRS-M1-00341-0387` | `CRS-M1-00341` | STATUS-CONSTRAINT | `ST-CRS-M1-00341` | Status-code predicate ST-CRS-M1-00341. |
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
| `TR-CRS-M1-00351-0441` | `CRS-M1-00351` | TRANSITION | `T_INF_ACCEPT_INIT` | Transition T_INF_ACCEPT_INIT cites this obligation. |
| `TR-CRS-M1-00177-0442` | `CRS-M1-00177` | TRANSITION | `T_INF_TFTP_TO` | Transition T_INF_TFTP_TO cites this obligation. |
| `TR-CRS-M1-00177-0443` | `CRS-M1-00177` | TRANSITION | `T_UPL_TFTP_TO` | Transition T_UPL_TFTP_TO cites this obligation. |
| `TR-CRS-M1-00177-0444` | `CRS-M1-00177` | TRANSITION | `T_UPL_LUR_TFTP_TO` | Transition T_UPL_LUR_TFTP_TO cites this obligation. |
| `TR-CRS-M1-00177-0445` | `CRS-M1-00177` | TRANSITION | `T_UPL_FILE_TFTP_TO` | Transition T_UPL_FILE_TFTP_TO cites this obligation. |
| `TR-CRS-M1-00187-0446` | `CRS-M1-00187` | TRANSITION | `T_UPL_DLP_TO` | Transition T_UPL_DLP_TO cites this obligation. |
| `TR-CRS-M1-00187-0447` | `CRS-M1-00187` | TRANSITION | `T_UPL_LUR_DLP_TO` | Transition T_UPL_LUR_DLP_TO cites this obligation. |
| `TR-CRS-M1-00188-0448` | `CRS-M1-00188` | TRANSITION | `T_UPL_LUR_DLP_TO` | Transition T_UPL_LUR_DLP_TO cites this obligation. |
| `TR-CRS-M1-00101-0449` | `CRS-M1-00101` | TRANSITION | `T_UPL_EXC_TO` | Transition T_UPL_EXC_TO cites this obligation. |
| `TR-CRS-M1-00108-0450` | `CRS-M1-00108` | TRANSITION | `T_UPL_EXC_TO` | Transition T_UPL_EXC_TO cites this obligation. |
| `TR-CRS-M1-00101-0451` | `CRS-M1-00101` | TRANSITION | `T_INF_EXC_TO` | Transition T_INF_EXC_TO cites this obligation. |
| `TR-CRS-M1-00099-0452` | `CRS-M1-00099` | TRANSITION | `T_ENTER_UPL_EXC` | Transition T_ENTER_UPL_EXC cites this obligation. |
| `TR-CRS-M1-00099-0453` | `CRS-M1-00099` | TRANSITION | `T_ENTER_INF_EXC` | Transition T_ENTER_INF_EXC cites this obligation. |
| `TR-CRS-M1-00032-0454` | `CRS-M1-00032` | TRANSITION | `T_WAIT_FROM_UPL_FILE` | Transition T_WAIT_FROM_UPL_FILE cites this obligation. |
| `TR-CRS-M1-00032-0455` | `CRS-M1-00032` | TRANSITION | `T_WAIT_FROM_UPL_LUR` | Transition T_WAIT_FROM_UPL_LUR cites this obligation. |
| `TR-CRS-M1-00032-0456` | `CRS-M1-00032` | TRANSITION | `T_WAIT_FROM_INF_LCI` | Transition T_WAIT_FROM_INF_LCI cites this obligation. |
| `TR-CRS-M1-00032-0457` | `CRS-M1-00032` | TRANSITION | `T_WAIT_FROM_INF_LCL` | Transition T_WAIT_FROM_INF_LCL cites this obligation. |
| `TR-CRS-M1-00032-0458` | `CRS-M1-00032` | TRANSITION | `T_WAIT_RETRY_UPL_FILE` | Transition T_WAIT_RETRY_UPL_FILE cites this obligation. |
| `TR-CRS-M1-00032-0459` | `CRS-M1-00032` | TRANSITION | `T_WAIT_RETRY_UPL_LUR` | Transition T_WAIT_RETRY_UPL_LUR cites this obligation. |
| `TR-CRS-M1-00032-0460` | `CRS-M1-00032` | TRANSITION | `T_WAIT_RETRY_INF_LCI` | Transition T_WAIT_RETRY_INF_LCI cites this obligation. |
| `TR-CRS-M1-00032-0461` | `CRS-M1-00032` | TRANSITION | `T_WAIT_RETRY_INF_LCL` | Transition T_WAIT_RETRY_INF_LCL cites this obligation. |
| `TR-CRS-M1-00341-0462` | `CRS-M1-00341` | TRANSITION | `T_ABORT_DL` | Transition T_ABORT_DL cites this obligation. |
| `TR-CRS-M1-00340-0463` | `CRS-M1-00340` | TRANSITION | `T_ABORT_TH` | Transition T_ABORT_TH cites this obligation. |
| `TR-CRS-M1-00340-0464` | `CRS-M1-00340` | TRANSITION | `T_ABORTED` | Transition T_ABORTED cites this obligation. |
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
| `F-1` | `DEFERRED` | PRODUCT-SCOPE | SCOPE-EXPANSION-GATE | FIND remains deferred. |
| `F-2` | `DEFERRED` | PRODUCT-SCOPE | SCOPE-EXPANSION-GATE | AFDX remains unselected. |
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

| CRS | Transition | Event | Actor | Receiver | Direction | Layer |
|---|---|---|---|---|---|---|
| `CRS-M1-00365` | `T_UPL_LUR_WRQ` | `EV_DL_WRQ_LUR` | `DATA-LOADER` | `TARGET-HARDWARE` | `DL-TO-TH` | `NETWORK-VISIBLE` |
| `CRS-M1-00366` | `T_UPL_LUR_ACK` | `EV_TH_ACK_LUR` | `TARGET-HARDWARE` | `DATA-LOADER` | `TH-TO-DL` | `NETWORK-VISIBLE` |
| `CRS-M1-00367` | `T_UPL_LUR_XFER` | `EV_DL_DATA_LUR` | `DATA-LOADER` | `TARGET-HARDWARE` | `DL-TO-TH` | `NETWORK-VISIBLE` |

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
- 后继增量 `CR-2026-011` 由 `CR-2026-009` 授权；doesNotTransplantFrozenApproval=`True`
- 前序输入制品提交 `402e8371b0237aec4691bab0b44e502f4ac1a7c4` 树 `26ea73a18fafbd4ba93c9dbb2890eb8453b0ad97`

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

## 时钟

| ID | 范围 | 关联 | 复位 | 含义 |
|---|---|---|---|---|
| `CLK_TFTP` | PER-CORRELATION-KEY | TFTP-PEER-AND-TRANSFER | `T_INF_LCI_RRQ`, `T_UPL_LUI_RRQ`, `T_UPL_LUR_WRQ`, `T_UPL_FILE_RRQ` | 相关传输中上一 TFTP 报文以来的时间。 |
| `CLK_DLP` | PER-CORRELATION-KEY | TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE | `T_INF_ACCEPT_INIT`, `T_UPL_ACCEPT_INIT`, `T_UPL_LUR_WRQ`, `T_UPL_FILE_RRQ` | 操作间／传输间 DLP 时钟。 |
| `CLK_EXCEPTION` | PER-CORRELATION-KEY | STATUS-EXCEPTION-OBJECT | `T_ENTER_UPL_EXC`, `T_ENTER_INF_EXC`, `T_INF_LCS_WRQ` | 异常静默时钟。 |
| `CLK_WAIT` | PER-CORRELATION-KEY | TFTP-PEER-AND-REJECTED-TRANSFER-REQUEST | `T_WAIT_FROM_UPL_FILE`, `T_WAIT_FROM_UPL_LUR`, `T_WAIT_FROM_INF_LCI`, `T_WAIT_FROM_INF_LCL` | 自 WAIT 消息起的时延；在所携定时器到期前禁止重试。 |

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
| `TR-CRS-M1-00100-0110` | `CRS-M1-00100` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00100-0111` | `CRS-M1-00100` | TIMING | `TIM-CRS-M1-00100` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00100-0112` | `CRS-M1-00100` | CLOCK | `CLK_EXCEPTION` | 此时序义务使用的时钟。 |
| `TR-CRS-M1-00101-0113` | `CRS-M1-00101` | TRANSITION | `T_INF_LCI_XFER` | INFORMATION 支持义务落在 LCI/LCL/LCS 机器上。 |
| `TR-CRS-M1-00101-0114` | `CRS-M1-00101` | TIMING | `TIM-CRS-M1-00101` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00101-0115` | `CRS-M1-00101` | CLOCK | `CLK_EXCEPTION` | 此时序义务使用的时钟。 |
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
| `TR-CRS-M1-00188-0228` | `CRS-M1-00188` | INTERFACE | `IF_TFTP` | BOUND-INTER-TRANSFER-DURATION-BY-DLP-EQUATION 的 TFTP 接口前提。 |
| `TR-CRS-M1-00188-0229` | `CRS-M1-00188` | TIMING | `TIM-CRS-M1-00188` | 带来源关系与时钟使能的时序目录行。 |
| `TR-CRS-M1-00188-0230` | `CRS-M1-00188` | CLOCK | `CLK_DLP` | 此时序义务使用的时钟。 |
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
| `TR-CRS-M1-00341-0387` | `CRS-M1-00341` | STATUS-CONSTRAINT | `ST-CRS-M1-00341` | 状态码谓词 ST-CRS-M1-00341。 |
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
| `TR-CRS-M1-00351-0441` | `CRS-M1-00351` | TRANSITION | `T_INF_ACCEPT_INIT` | 迁移 T_INF_ACCEPT_INIT 引用此义务。 |
| `TR-CRS-M1-00177-0442` | `CRS-M1-00177` | TRANSITION | `T_INF_TFTP_TO` | 迁移 T_INF_TFTP_TO 引用此义务。 |
| `TR-CRS-M1-00177-0443` | `CRS-M1-00177` | TRANSITION | `T_UPL_TFTP_TO` | 迁移 T_UPL_TFTP_TO 引用此义务。 |
| `TR-CRS-M1-00177-0444` | `CRS-M1-00177` | TRANSITION | `T_UPL_LUR_TFTP_TO` | 迁移 T_UPL_LUR_TFTP_TO 引用此义务。 |
| `TR-CRS-M1-00177-0445` | `CRS-M1-00177` | TRANSITION | `T_UPL_FILE_TFTP_TO` | 迁移 T_UPL_FILE_TFTP_TO 引用此义务。 |
| `TR-CRS-M1-00187-0446` | `CRS-M1-00187` | TRANSITION | `T_UPL_DLP_TO` | 迁移 T_UPL_DLP_TO 引用此义务。 |
| `TR-CRS-M1-00187-0447` | `CRS-M1-00187` | TRANSITION | `T_UPL_LUR_DLP_TO` | 迁移 T_UPL_LUR_DLP_TO 引用此义务。 |
| `TR-CRS-M1-00188-0448` | `CRS-M1-00188` | TRANSITION | `T_UPL_LUR_DLP_TO` | 迁移 T_UPL_LUR_DLP_TO 引用此义务。 |
| `TR-CRS-M1-00101-0449` | `CRS-M1-00101` | TRANSITION | `T_UPL_EXC_TO` | 迁移 T_UPL_EXC_TO 引用此义务。 |
| `TR-CRS-M1-00108-0450` | `CRS-M1-00108` | TRANSITION | `T_UPL_EXC_TO` | 迁移 T_UPL_EXC_TO 引用此义务。 |
| `TR-CRS-M1-00101-0451` | `CRS-M1-00101` | TRANSITION | `T_INF_EXC_TO` | 迁移 T_INF_EXC_TO 引用此义务。 |
| `TR-CRS-M1-00099-0452` | `CRS-M1-00099` | TRANSITION | `T_ENTER_UPL_EXC` | 迁移 T_ENTER_UPL_EXC 引用此义务。 |
| `TR-CRS-M1-00099-0453` | `CRS-M1-00099` | TRANSITION | `T_ENTER_INF_EXC` | 迁移 T_ENTER_INF_EXC 引用此义务。 |
| `TR-CRS-M1-00032-0454` | `CRS-M1-00032` | TRANSITION | `T_WAIT_FROM_UPL_FILE` | 迁移 T_WAIT_FROM_UPL_FILE 引用此义务。 |
| `TR-CRS-M1-00032-0455` | `CRS-M1-00032` | TRANSITION | `T_WAIT_FROM_UPL_LUR` | 迁移 T_WAIT_FROM_UPL_LUR 引用此义务。 |
| `TR-CRS-M1-00032-0456` | `CRS-M1-00032` | TRANSITION | `T_WAIT_FROM_INF_LCI` | 迁移 T_WAIT_FROM_INF_LCI 引用此义务。 |
| `TR-CRS-M1-00032-0457` | `CRS-M1-00032` | TRANSITION | `T_WAIT_FROM_INF_LCL` | 迁移 T_WAIT_FROM_INF_LCL 引用此义务。 |
| `TR-CRS-M1-00032-0458` | `CRS-M1-00032` | TRANSITION | `T_WAIT_RETRY_UPL_FILE` | 迁移 T_WAIT_RETRY_UPL_FILE 引用此义务。 |
| `TR-CRS-M1-00032-0459` | `CRS-M1-00032` | TRANSITION | `T_WAIT_RETRY_UPL_LUR` | 迁移 T_WAIT_RETRY_UPL_LUR 引用此义务。 |
| `TR-CRS-M1-00032-0460` | `CRS-M1-00032` | TRANSITION | `T_WAIT_RETRY_INF_LCI` | 迁移 T_WAIT_RETRY_INF_LCI 引用此义务。 |
| `TR-CRS-M1-00032-0461` | `CRS-M1-00032` | TRANSITION | `T_WAIT_RETRY_INF_LCL` | 迁移 T_WAIT_RETRY_INF_LCL 引用此义务。 |
| `TR-CRS-M1-00341-0462` | `CRS-M1-00341` | TRANSITION | `T_ABORT_DL` | 迁移 T_ABORT_DL 引用此义务。 |
| `TR-CRS-M1-00340-0463` | `CRS-M1-00340` | TRANSITION | `T_ABORT_TH` | 迁移 T_ABORT_TH 引用此义务。 |
| `TR-CRS-M1-00340-0464` | `CRS-M1-00340` | TRANSITION | `T_ABORTED` | 迁移 T_ABORTED 引用此义务。 |
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
| `F-1` | `DEFERRED` | PRODUCT-SCOPE | SCOPE-EXPANSION-GATE | FIND 保持延期。 |
| `F-2` | `DEFERRED` | PRODUCT-SCOPE | SCOPE-EXPANSION-GATE | AFDX 保持未选择。 |
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

| CRS | 迁移 | 事件 | 发送者 | 接收者 | 方向 | 层级 |
|---|---|---|---|---|---|---|
| `CRS-M1-00365` | `T_UPL_LUR_WRQ` | `EV_DL_WRQ_LUR` | `DATA-LOADER` | `TARGET-HARDWARE` | `DL-TO-TH` | `NETWORK-VISIBLE` |
| `CRS-M1-00366` | `T_UPL_LUR_ACK` | `EV_TH_ACK_LUR` | `TARGET-HARDWARE` | `DATA-LOADER` | `TH-TO-DL` | `NETWORK-VISIBLE` |
| `CRS-M1-00367` | `T_UPL_LUR_XFER` | `EV_DL_DATA_LUR` | `DATA-LOADER` | `TARGET-HARDWARE` | `DL-TO-TH` | `NETWORK-VISIBLE` |

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
