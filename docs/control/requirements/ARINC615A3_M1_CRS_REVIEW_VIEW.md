# ARINC 615A-3 M1 CRS and Applicability — Generated Review View

> Generated from `configs/requirements/arinc_615a3_m1_crs.json` by `python scripts/sync_m1_crs.py --write`. Do not edit this view.

## Candidate state

- Disposition: `ADOPT`
- RG0: `PENDING-EXTERNAL-INDEPENDENT-REVIEW`
- RG1: `PENDING-EXTERNAL-INDEPENDENT-REVIEW`
- Formal approval: `EXTERNAL-JOINT-CONDITION-NOT-YET-SATISFIED`
- This package establishes neither Project Configuration nor protocol conformance.

## Inventory

- Coverage rows: 523
- CRS items: 300
- Dependencies: 4
- Gaps: 1
- Coverage fingerprint: `f4f885b52a6b7f7597abffd775bc8aa1ef681c34adf9940ec3b5fed3ff26af50`
- Requirements fingerprint: `3eb61c6f5db277b3273e8d2436a85db9b99ce142e66a80c0da99b9cd496dd8eb`

## Applicability

- `APPLICABLE-BASE`: 41
- `APPLICABLE-SUPPORTING`: 237
- `BLOCKED-BY-DEPENDENCY`: 22

## Source modality

- `FIGURE-CONSTRAINT`: 4
- `MAY`: 76
- `MUST`: 18
- `SHOULD`: 200
- `TABLE-CONSTRAINT`: 2

## Conformance effect

- `OPTIONAL`: 76
- `REQUIRED`: 224

## Open dependencies and gaps

- `DEP-ARINC-645` — OPEN-DEPENDENCY: Integrity and naming algorithms remain unavailable. / 完整性与命名算法来源仍未取得。
- `DEP-ARINC-6655` — REGISTERED-SUPPORTING-SOURCE: Bounded data-format survey; not an edition substitute. / 有界数据格式调查，不构成版次替代。
- `DEP-IP-UDP-664` — OPEN-DEPENDENCY: IP, UDP and ARINC 664 network semantics require controlled source closure. / IP、UDP 与 ARINC 664 网络语义仍需受控来源闭合。
- `DEP-RFC-TFTP` — OPEN-DEPENDENCY: TFTP base and option RFC identities and applicability remain open. / TFTP 基础及选项 RFC 的身份与适用性仍开放。
- `GAP-ARINC-645` — NOT-ESTABLISHED: CRC, check-value, naming and complete-integrity validation are blocked. / CRC、校验值、命名及完整完整性验证仍受阻。

## CRS items

| ID | Source | Modality / effect | Applicability | Review paraphrase | Dependencies / gaps |
|---|---|---|---|---|---|
| `CRS-615A3-0001` | `ARINC-615A-3 1.1 p.1` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.1.<br>对 SCOPE，执行条款 1.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0002` | `ARINC-615A-3 1.3 p.2` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.3.<br>对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0003` | `ARINC-615A-3 1.3 p.2` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.3.<br>对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子transport规则。 | — |
| `CRS-615A3-0004` | `ARINC-615A-3 1.3 p.2` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic protocol behavior rule 3 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.3.<br>对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子protocol behavior规则。 | — |
| `CRS-615A3-0005` | `ARINC-615A-3 1.3 p.2` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic protocol behavior rule 4 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.3.<br>对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子protocol behavior规则。 | — |
| `CRS-615A3-0006` | `ARINC-615A-3 1.3 p.2` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 5 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.3.<br>对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0007` | `ARINC-615A-3 1.3 p.2` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic protocol behavior rule 6 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.3.<br>对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子protocol behavior规则。 | — |
| `CRS-615A3-0008` | `ARINC-615A-3 1.3 p.2` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 7 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.3.<br>对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 7 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0009` | `ARINC-615A-3 1.3 p.2` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 8 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.3.<br>对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 8 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0010` | `ARINC-615A-3 1.3 p.2` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic protocol behavior rule 9 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.3.<br>对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 9 项原子protocol behavior规则。 | — |
| `CRS-615A3-0011` | `ARINC-615A-3 1.4.1 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic protocol behavior rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.1.<br>对 SCOPE，执行条款 1.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | — |
| `CRS-615A3-0012` | `ARINC-615A-3 1.4.1 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.1.<br>对 SCOPE，执行条款 1.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0013` | `ARINC-615A-3 1.4.1 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 3 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.1.<br>对 SCOPE，执行条款 1.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0014` | `ARINC-615A-3 1.4.1 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic human interface rule 4 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.1.<br>对 SCOPE，执行条款 1.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子human interface规则。 | — |
| `CRS-615A3-0015` | `ARINC-615A-3 1.4.1 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic data format rule 5 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.1.<br>对 SCOPE，执行条款 1.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子data format规则。 | DEP-ARINC-6655, DEP-IP-UDP-664 |
| `CRS-615A3-0016` | `ARINC-615A-3 1.4.1 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic error status rule 6 governing STATUS at clause 1.4.1.<br>对 SCOPE，执行条款 1.4.1 中治理 STATUS 的第 6 项原子error status规则。 | — |
| `CRS-615A3-0017` | `ARINC-615A-3 1.4.3 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.3.<br>对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | — |
| `CRS-615A3-0018` | `ARINC-615A-3 1.4.3 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic protocol behavior rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.3.<br>对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | — |
| `CRS-615A3-0019` | `ARINC-615A-3 1.4.3 p.4` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 3 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.3.<br>对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子transport规则。 | — |
| `CRS-615A3-0020` | `ARINC-615A-3 1.4.3 p.4` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic error status rule 4 governing STATUS at clause 1.4.3.<br>对 SCOPE，执行条款 1.4.3 中治理 STATUS 的第 4 项原子error status规则。 | — |
| `CRS-615A3-0021` | `ARINC-615A-3 1.4.3 p.4` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 5 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.3.<br>对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0022` | `ARINC-615A-3 1.4.3 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic human interface rule 6 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.3.<br>对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子human interface规则。 | — |
| `CRS-615A3-0023` | `ARINC-615A-3 1.4.3 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 7 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.3.<br>对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 7 项原子transport规则。 | — |
| `CRS-615A3-0024` | `ARINC-615A-3 1.4.3 p.4` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 8 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.3.<br>对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 8 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0025` | `ARINC-615A-3 1.4.3 p.4` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 9 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.3.<br>对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 9 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0026` | `ARINC-615A-3 1.4.3 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 10 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.3.<br>对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 10 项原子transport规则。 | — |
| `CRS-615A3-0027` | `ARINC-615A-3 1.4.3 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic protocol behavior rule 11 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.3.<br>对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 11 项原子protocol behavior规则。 | — |
| `CRS-615A3-0028` | `ARINC-615A-3 1.4.3 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 12 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.3.<br>对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 12 项原子transport规则。 | — |
| `CRS-615A3-0029` | `ARINC-615A-3 1.8 p.5` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic data format rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.8.<br>对 SCOPE，执行条款 1.8 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子data format规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0030` | `ARINC-615A-3 1.8 p.5` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.8.<br>对 SCOPE，执行条款 1.8 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0031` | `ARINC-615A-3 1.8 p.5` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 3 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.8.<br>对 SCOPE，执行条款 1.8 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0032` | `ARINC-615A-3 1.8 p.5` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 4 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.8.<br>对 SCOPE，执行条款 1.8 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子transport规则。 | — |
| `CRS-615A3-0033` | `ARINC-615A-3 1.8 p.5` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 5 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.8.<br>对 SCOPE，执行条款 1.8 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子transport规则。 | DEP-ARINC-6655, DEP-IP-UDP-664 |
| `CRS-615A3-0034` | `ARINC-615A-3 1.8 p.5` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic protocol behavior rule 6 governing FIND at clause 1.8.<br>对 SCOPE，执行条款 1.8 中治理 FIND 的第 6 项原子protocol behavior规则。 | — |
| `CRS-615A3-0035` | `ARINC-615A-3 1.8 p.5` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 7 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.8.<br>对 SCOPE，执行条款 1.8 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 7 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0036` | `ARINC-615A-3 1.8 p.5` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 8 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.8.<br>对 SCOPE，执行条款 1.8 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 8 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0037` | `ARINC-615A-3 1.10 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For SCOPE, enforce atomic transport rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.10.<br>对 SCOPE，执行条款 1.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | — |
| `CRS-615A3-0038` | `ARINC-615A-3 5.2 p.22` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 1 governing FILE-NAME at clause 5.2.<br>对 COMMON，执行条款 5.2 中治理 FILE-NAME 的第 1 项原子data format规则。 | — |
| `CRS-615A3-0039` | `ARINC-615A-3 5.2 p.22` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic transport rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.2.<br>对 COMMON，执行条款 5.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子transport规则。 | DEP-ARINC-6655 |
| `CRS-615A3-0040` | `ARINC-615A-3 5.3.1 p.23` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 1 governing FIND at clause 5.3.1.<br>对 COMMON，执行条款 5.3.1 中治理 FIND 的第 1 项原子data format规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0041` | `ARINC-615A-3 5.3.2 p.24` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic transport rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.3.2.<br>对 COMMON，执行条款 5.3.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0042` | `ARINC-615A-3 5.3.2.3.2 p.25` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 1 governing TFTP-OPTION at clause 5.3.2.3.2.<br>对 COMMON，执行条款 5.3.2.3.2 中治理 TFTP-OPTION 的第 1 项原子data format规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0043` | `ARINC-615A-3 5.3.2.3.2 p.25` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic protocol behavior rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.3.2.3.2.<br>对 COMMON，执行条款 5.3.2.3.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | — |
| `CRS-615A3-0044` | `ARINC-615A-3 5.3.2.3.2 p.25` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic error status rule 3 governing ERROR at clause 5.3.2.3.2.<br>对 COMMON，执行条款 5.3.2.3.2 中治理 ERROR 的第 3 项原子error status规则。 | — |
| `CRS-615A3-0045` | `ARINC-615A-3 5.3.2.3.2 p.25` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic transport rule 4 governing TFTP-OPTION at clause 5.3.2.3.2.<br>对 COMMON，执行条款 5.3.2.3.2 中治理 TFTP-OPTION 的第 4 项原子transport规则。 | DEP-IP-UDP-664, DEP-RFC-TFTP |
| `CRS-615A3-0046` | `ARINC-615A-3 5.3.2.3.2 p.25` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 5 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.3.2.3.2.<br>对 COMMON，执行条款 5.3.2.3.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子data format规则。 | — |
| `CRS-615A3-0047` | `ARINC-615A-3 5.3.2.3.2 p.25` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 6 governing PORT at clause 5.3.2.3.2.<br>对 COMMON，执行条款 5.3.2.3.2 中治理 PORT 的第 6 项原子data format规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0048` | `ARINC-615A-3 5.3.2.3.4 p.26` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic error status rule 1 governing ERROR at clause 5.3.2.3.4.<br>对 COMMON，执行条款 5.3.2.3.4 中治理 ERROR 的第 1 项原子error status规则。 | — |
| `CRS-615A3-0049` | `ARINC-615A-3 5.3.2.3.4 p.26` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 2 governing ERROR at clause 5.3.2.3.4.<br>对 COMMON，执行条款 5.3.2.3.4 中治理 ERROR 的第 2 项原子data format规则。 | — |
| `CRS-615A3-0050` | `ARINC-615A-3 5.3.2.3.4 p.26` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 3 governing ERROR at clause 5.3.2.3.4.<br>对 COMMON，执行条款 5.3.2.3.4 中治理 ERROR 的第 3 项原子data format规则。 | — |
| `CRS-615A3-0051` | `ARINC-615A-3 5.3.2.3.4 p.26` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 4 governing WAIT / ERROR at clause 5.3.2.3.4.<br>对 COMMON，执行条款 5.3.2.3.4 中治理 WAIT / ERROR 的第 4 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0052` | `ARINC-615A-3 5.3.2.3.4 p.26` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic transport rule 5 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.3.2.3.4.<br>对 COMMON，执行条款 5.3.2.3.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子transport规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0053` | `ARINC-615A-3 5.3.2.3.4 p.26` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 6 governing WAIT / ABORT at clause 5.3.2.3.4.<br>对 COMMON，执行条款 5.3.2.3.4 中治理 WAIT / ABORT 的第 6 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0054` | `ARINC-615A-3 5.3.2.3.8.1 p.28` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic transport rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.3.2.3.8.1.<br>对 COMMON，执行条款 5.3.2.3.8.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0055` | `ARINC-615A-3 5.3.2.3.8.1 p.28` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic transport rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.3.2.3.8.1.<br>对 COMMON，执行条款 5.3.2.3.8.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0056` | `ARINC-615A-3 5.3.2.3.8.1 p.28` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic transport rule 3 governing BLOCK-SIZE at clause 5.3.2.3.8.1.<br>对 COMMON，执行条款 5.3.2.3.8.1 中治理 BLOCK-SIZE 的第 3 项原子transport规则。 | DEP-IP-UDP-664, DEP-RFC-TFTP |
| `CRS-615A3-0057` | `ARINC-615A-3 5.3.2.3.8.1 p.28` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic protocol behavior rule 4 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.3.2.3.8.1.<br>对 COMMON，执行条款 5.3.2.3.8.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子protocol behavior规则。 | — |
| `CRS-615A3-0058` | `ARINC-615A-3 5.3.2.3.8.5 p.29` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic transport rule 1 governing BLOCK-SIZE at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 BLOCK-SIZE 的第 1 项原子transport规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0059` | `ARINC-615A-3 5.3.2.3.8.5 p.29` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 2 governing BLOCK-SIZE / TRANSFER-SIZE at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 BLOCK-SIZE / TRANSFER-SIZE 的第 2 项原子data format规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0060` | `ARINC-615A-3 5.3.2.3.8.5 p.29` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic error status rule 3 governing TRANSFER-SIZE / ERROR at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 TRANSFER-SIZE / ERROR 的第 3 项原子error status规则。 | — |
| `CRS-615A3-0061` | `ARINC-615A-3 5.3.2.3.8.5 p.29` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 4 governing TRANSFER-SIZE / TIMEOUT at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 TRANSFER-SIZE / TIMEOUT 的第 4 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0062` | `ARINC-615A-3 5.3.2.3.8.5 p.29` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 5 governing TIMEOUT at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 TIMEOUT 的第 5 项原子timing规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0063` | `ARINC-615A-3 5.3.2.3.8.5 p.29` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 6 governing TIMEOUT / PART-NUMBER at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 TIMEOUT / PART-NUMBER 的第 6 项原子timing规则。 | — |
| `CRS-615A3-0064` | `ARINC-615A-3 5.3.2.3.8.5 p.29` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 7 governing TIMEOUT / CHECKSUM at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 TIMEOUT / CHECKSUM 的第 7 项原子timing规则。 | GAP-ARINC-645 |
| `CRS-615A3-0065` | `ARINC-615A-3 5.3.2.3.8.5 p.30` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 8 governing CHECKSUM / CRC / FILE-NAME / HEADER-FILE at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 CHECKSUM / CRC / FILE-NAME / HEADER-FILE 的第 8 项原子data format规则。 | DEP-ARINC-6655, DEP-RFC-TFTP, GAP-ARINC-645 |
| `CRS-615A3-0066` | `ARINC-615A-3 5.3.2.3.8.5 p.30` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 9 governing CRC at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 CRC 的第 9 项原子data format规则。 | GAP-ARINC-645 |
| `CRS-615A3-0067` | `ARINC-615A-3 5.3.2.3.8.5 p.30` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic transport rule 10 governing TFTP-OPTION / CHECKSUM at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 TFTP-OPTION / CHECKSUM 的第 10 项原子transport规则。 | DEP-RFC-TFTP, GAP-ARINC-645 |
| `CRS-615A3-0068` | `ARINC-615A-3 5.3.2.3.8.5 p.31` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 11 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 11 项原子data format规则。 | — |
| `CRS-615A3-0069` | `ARINC-615A-3 5.3.2.3.8.5 p.31` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 12 governing CHECKSUM / CRC / FILE-NAME / HEADER-FILE at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 CHECKSUM / CRC / FILE-NAME / HEADER-FILE 的第 12 项原子data format规则。 | DEP-ARINC-6655, GAP-ARINC-645 |
| `CRS-615A3-0070` | `ARINC-615A-3 5.3.2.3.8.5 p.31` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 13 governing DOWNLOAD at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 DOWNLOAD 的第 13 项原子data format规则。 | — |
| `CRS-615A3-0071` | `ARINC-615A-3 5.3.2.3.8.5 p.31` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic transport rule 14 governing CHECKSUM at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 CHECKSUM 的第 14 项原子transport规则。 | GAP-ARINC-645 |
| `CRS-615A3-0072` | `ARINC-615A-3 5.3.2.3.8.5 p.31` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 15 governing CHECKSUM / DATA-FILE / ERROR at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 CHECKSUM / DATA-FILE / ERROR 的第 15 项原子data format规则。 | DEP-RFC-TFTP, GAP-ARINC-645 |
| `CRS-615A3-0073` | `ARINC-615A-3 5.3.2.3.8.5 p.31` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 16 governing CHECKSUM / DOWNLOAD / ERROR at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 CHECKSUM / DOWNLOAD / ERROR 的第 16 项原子data format规则。 | GAP-ARINC-645 |
| `CRS-615A3-0074` | `ARINC-615A-3 5.3.2.3.8.5 p.31` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 17 governing CHECKSUM / DOWNLOAD at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 CHECKSUM / DOWNLOAD 的第 17 项原子data format规则。 | GAP-ARINC-645 |
| `CRS-615A3-0075` | `ARINC-615A-3 5.3.2.3.8.5 p.31` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic protocol behavior rule 18 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.3.2.3.8.5.<br>对 COMMON，执行条款 5.3.2.3.8.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 18 项原子protocol behavior规则。 | — |
| `CRS-615A3-0076` | `ARINC-615A-3 5.4.1 p.33` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic transport rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.4.1.<br>对 COMMON，执行条款 5.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0077` | `ARINC-615A-3 5.4.1 p.33` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic transport rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.4.1.<br>对 COMMON，执行条款 5.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0078` | `ARINC-615A-3 5.4.1 p.33` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 3 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.4.1.<br>对 COMMON，执行条款 5.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子data format规则。 | — |
| `CRS-615A3-0079` | `ARINC-615A-3 5.4.1 p.34` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic protocol behavior rule 4 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.4.1.<br>对 COMMON，执行条款 5.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子protocol behavior规则。 | — |
| `CRS-615A3-0080` | `ARINC-615A-3 5.4.1 p.34` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic error status rule 5 governing ABORT at clause 5.4.1.<br>对 COMMON，执行条款 5.4.1 中治理 ABORT 的第 5 项原子error status规则。 | — |
| `CRS-615A3-0081` | `ARINC-615A-3 5.4.1 p.34` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic protocol behavior rule 6 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.4.1.<br>对 COMMON，执行条款 5.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子protocol behavior规则。 | — |
| `CRS-615A3-0082` | `ARINC-615A-3 5.4.1 p.34` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 7 governing UPLOAD / DOWNLOAD / FIND at clause 5.4.1.<br>对 COMMON，执行条款 5.4.1 中治理 UPLOAD / DOWNLOAD / FIND 的第 7 项原子data format规则。 | — |
| `CRS-615A3-0083` | `ARINC-615A-3 5.4.1 p.34` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic protocol behavior rule 8 governing FIND at clause 5.4.1.<br>对 COMMON，执行条款 5.4.1 中治理 FIND 的第 8 项原子protocol behavior规则。 | — |
| `CRS-615A3-0084` | `ARINC-615A-3 5.4.1 p.34` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 9 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.4.1.<br>对 COMMON，执行条款 5.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 9 项原子data format规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0085` | `ARINC-615A-3 5.4.1 p.34` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 10 governing STATUS at clause 5.4.1.<br>对 COMMON，执行条款 5.4.1 中治理 STATUS 的第 10 项原子data format规则。 | — |
| `CRS-615A3-0086` | `ARINC-615A-3 5.4.3 p.35` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic transport rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.4.3.<br>对 UPLOAD，执行条款 5.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | — |
| `CRS-615A3-0087` | `ARINC-615A-3 5.4.3 p.35` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic protocol behavior rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.4.3.<br>对 UPLOAD，执行条款 5.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | — |
| `CRS-615A3-0088` | `ARINC-615A-3 5.4.3 p.35` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic protocol behavior rule 3 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.4.3.<br>对 UPLOAD，执行条款 5.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子protocol behavior规则。 | — |
| `CRS-615A3-0089` | `ARINC-615A-3 5.4.3 p.35` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic timing rule 4 governing WAIT / STATUS at clause 5.4.3.<br>对 UPLOAD，执行条款 5.4.3 中治理 WAIT / STATUS 的第 4 项原子timing规则。 | — |
| `CRS-615A3-0090` | `ARINC-615A-3 5.4.3 p.35` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic transport rule 5 governing TFTP-OPTION at clause 5.4.3.<br>对 UPLOAD，执行条款 5.4.3 中治理 TFTP-OPTION 的第 5 项原子transport规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0091` | `ARINC-615A-3 5.4.3 p.35` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic transport rule 6 governing TFTP-OPTION at clause 5.4.3.<br>对 UPLOAD，执行条款 5.4.3 中治理 TFTP-OPTION 的第 6 项原子transport规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0092` | `ARINC-615A-3 5.4.3 p.35` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic data format rule 7 governing UPLOAD at clause 5.4.3.<br>对 UPLOAD，执行条款 5.4.3 中治理 UPLOAD 的第 7 项原子data format规则。 | GAP-ARINC-645 |
| `CRS-615A3-0093` | `ARINC-615A-3 5.4.3.1 p.36` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic protocol behavior rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.4.3.1.<br>对 UPLOAD，执行条款 5.4.3.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | — |
| `CRS-615A3-0094` | `ARINC-615A-3 5.4.3.1 p.36` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic error status rule 2 governing STATUS at clause 5.4.3.1.<br>对 UPLOAD，执行条款 5.4.3.1 中治理 STATUS 的第 2 项原子error status规则。 | — |
| `CRS-615A3-0095` | `ARINC-615A-3 5.4.3.1 p.36` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic transport rule 3 governing TFTP-OPTION at clause 5.4.3.1.<br>对 UPLOAD，执行条款 5.4.3.1 中治理 TFTP-OPTION 的第 3 项原子transport规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0096` | `ARINC-615A-3 5.4.3.1 p.36` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic data format rule 4 governing FILE-NAME at clause 5.4.3.1.<br>对 UPLOAD，执行条款 5.4.3.1 中治理 FILE-NAME 的第 4 项原子data format规则。 | GAP-ARINC-645 |
| `CRS-615A3-0097` | `ARINC-615A-3 5.4.3.1 p.36` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic timing rule 5 governing TFTP-OPTION at clause 5.4.3.1.<br>对 UPLOAD，执行条款 5.4.3.1 中治理 TFTP-OPTION 的第 5 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0098` | `ARINC-615A-3 5.4.3.1 p.36` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic data format rule 6 governing PART-NUMBER / HEADER-FILE / DATA-FILE at clause 5.4.3.1.<br>对 UPLOAD，执行条款 5.4.3.1 中治理 PART-NUMBER / HEADER-FILE / DATA-FILE 的第 6 项原子data format规则。 | — |
| `CRS-615A3-0099` | `ARINC-615A-3 5.4.3.2 p.37` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic protocol behavior rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.4.3.2.<br>对 UPLOAD，执行条款 5.4.3.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | GAP-ARINC-645 |
| `CRS-615A3-0100` | `ARINC-615A-3 5.4.3.2 p.37` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic data format rule 2 governing CRC at clause 5.4.3.2.<br>对 UPLOAD，执行条款 5.4.3.2 中治理 CRC 的第 2 项原子data format规则。 | GAP-ARINC-645 |
| `CRS-615A3-0101` | `ARINC-615A-3 5.4.3.2 p.37` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic data format rule 3 governing CRC / PART-NUMBER at clause 5.4.3.2.<br>对 UPLOAD，执行条款 5.4.3.2 中治理 CRC / PART-NUMBER 的第 3 项原子data format规则。 | GAP-ARINC-645 |
| `CRS-615A3-0102` | `ARINC-615A-3 5.4.3.2 p.37` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic data format rule 4 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.4.3.2.<br>对 UPLOAD，执行条款 5.4.3.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子data format规则。 | — |
| `CRS-615A3-0103` | `ARINC-615A-3 5.4.3.2 p.37` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic timing rule 5 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.4.3.2.<br>对 UPLOAD，执行条款 5.4.3.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子timing规则。 | — |
| `CRS-615A3-0104` | `ARINC-615A-3 5.4.3.2 p.37` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic data format rule 6 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.4.3.2.<br>对 UPLOAD，执行条款 5.4.3.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子data format规则。 | — |
| `CRS-615A3-0105` | `ARINC-615A-3 5.4.5.1 p.40` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 1 governing DOWNLOAD at clause 5.4.5.1.<br>对 COMMON，执行条款 5.4.5.1 中治理 DOWNLOAD 的第 1 项原子data format规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0106` | `ARINC-615A-3 5.4.5.1 p.40` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic human interface rule 2 governing DOWNLOAD at clause 5.4.5.1.<br>对 COMMON，执行条款 5.4.5.1 中治理 DOWNLOAD 的第 2 项原子human interface规则。 | — |
| `CRS-615A3-0107` | `ARINC-615A-3 5.4.5.1 p.40` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic error status rule 3 governing DOWNLOAD / ERROR at clause 5.4.5.1.<br>对 COMMON，执行条款 5.4.5.1 中治理 DOWNLOAD / ERROR 的第 3 项原子error status规则。 | — |
| `CRS-615A3-0108` | `ARINC-615A-3 5.4.5.1 p.40` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 4 governing DOWNLOAD at clause 5.4.5.1.<br>对 COMMON，执行条款 5.4.5.1 中治理 DOWNLOAD 的第 4 项原子timing规则。 | — |
| `CRS-615A3-0109` | `ARINC-615A-3 5.4.5.1 p.40` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 5 governing DOWNLOAD at clause 5.4.5.1.<br>对 COMMON，执行条款 5.4.5.1 中治理 DOWNLOAD 的第 5 项原子timing规则。 | — |
| `CRS-615A3-0110` | `ARINC-615A-3 5.4.5.2 p.41` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 1 governing ABORT / STATUS at clause 5.4.5.2.<br>对 COMMON，执行条款 5.4.5.2 中治理 ABORT / STATUS 的第 1 项原子data format规则。 | — |
| `CRS-615A3-0111` | `ARINC-615A-3 6.2.8.2 p.45` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic timing rule 1 governing WAIT at clause 6.2.8.2.<br>对 UPLOAD，执行条款 6.2.8.2 中治理 WAIT 的第 1 项原子timing规则。 | DEP-IP-UDP-664, DEP-RFC-TFTP |
| `CRS-615A3-0112` | `ARINC-615A-3 6.3.1 p.51` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic timing rule 1 governing TIMEOUT at clause 6.3.1.<br>对 INFORMATION，执行条款 6.3.1 中治理 TIMEOUT 的第 1 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0113` | `ARINC-615A-3 6.3.1 p.51` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic timing rule 2 governing TIMEOUT at clause 6.3.1.<br>对 INFORMATION，执行条款 6.3.1 中治理 TIMEOUT 的第 2 项原子timing规则。 | — |
| `CRS-615A3-0114` | `ARINC-615A-3 6.3.1 p.51` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic timing rule 3 governing STATUS / TIMEOUT at clause 6.3.1.<br>对 INFORMATION，执行条款 6.3.1 中治理 STATUS / TIMEOUT 的第 3 项原子timing规则。 | — |
| `CRS-615A3-0115` | `ARINC-615A-3 6.3.1 p.51` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic timing rule 4 governing ABORT / STATUS / TIMEOUT / INFORMATION at clause 6.3.1.<br>对 INFORMATION，执行条款 6.3.1 中治理 ABORT / STATUS / TIMEOUT / INFORMATION 的第 4 项原子timing规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0116` | `ARINC-615A-3 6.3.1 p.51` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic timing rule 5 governing STATUS / TIMEOUT at clause 6.3.1.<br>对 INFORMATION，执行条款 6.3.1 中治理 STATUS / TIMEOUT 的第 5 项原子timing规则。 | — |
| `CRS-615A3-0117` | `ARINC-615A-3 6.3.1 p.51` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic timing rule 6 governing STATUS / TIMEOUT at clause 6.3.1.<br>对 INFORMATION，执行条款 6.3.1 中治理 STATUS / TIMEOUT 的第 6 项原子timing规则。 | — |
| `CRS-615A3-0118` | `ARINC-615A-3 6.3.1 p.52` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic timing rule 7 governing WAIT at clause 6.3.1.<br>对 INFORMATION，执行条款 6.3.1 中治理 WAIT 的第 7 项原子timing规则。 | — |
| `CRS-615A3-0119` | `ARINC-615A-3 6.3.1 p.52` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic timing rule 8 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.3.1.<br>对 INFORMATION，执行条款 6.3.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 8 项原子timing规则。 | — |
| `CRS-615A3-0120` | `ARINC-615A-3 6.3.1 p.52` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic timing rule 9 governing ABORT / STATUS / UPLOAD / DOWNLOAD at clause 6.3.1.<br>对 INFORMATION，执行条款 6.3.1 中治理 ABORT / STATUS / UPLOAD / DOWNLOAD 的第 9 项原子timing规则。 | — |
| `CRS-615A3-0121` | `ARINC-615A-3 5.3.2.3.4 p.55` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 7 governing TIMEOUT at clause 5.3.2.3.4.<br>对 COMMON，执行条款 5.3.2.3.4 中治理 TIMEOUT 的第 7 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0122` | `ARINC-615A-3 5.3.2.3.4 p.55` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 8 governing TIMEOUT at clause 5.3.2.3.4.<br>对 COMMON，执行条款 5.3.2.3.4 中治理 TIMEOUT 的第 8 项原子timing规则。 | — |
| `CRS-615A3-0123` | `ARINC-615A-3 5.3.2.3.4 p.55` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 9 governing STATUS / TIMEOUT at clause 5.3.2.3.4.<br>对 COMMON，执行条款 5.3.2.3.4 中治理 STATUS / TIMEOUT 的第 9 项原子timing规则。 | — |
| `CRS-615A3-0124` | `ARINC-615A-3 5.3.2.3.4 p.55` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 10 governing ABORT / STATUS / TIMEOUT / ERROR at clause 5.3.2.3.4.<br>对 COMMON，执行条款 5.3.2.3.4 中治理 ABORT / STATUS / TIMEOUT / ERROR 的第 10 项原子timing规则。 | DEP-IP-UDP-664, DEP-RFC-TFTP |
| `CRS-615A3-0125` | `ARINC-615A-3 5.3.2.3.4 p.55` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 11 governing HEADER-FILE / DATA-FILE / UPLOAD at clause 5.3.2.3.4.<br>对 COMMON，执行条款 5.3.2.3.4 中治理 HEADER-FILE / DATA-FILE / UPLOAD 的第 11 项原子data format规则。 | — |
| `CRS-615A3-0126` | `ARINC-615A-3 5.3.2.3.4 p.56` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 12 governing WAIT at clause 5.3.2.3.4.<br>对 COMMON，执行条款 5.3.2.3.4 中治理 WAIT 的第 12 项原子timing规则。 | — |
| `CRS-615A3-0127` | `ARINC-615A-3 5.3.2.3.4 p.56` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 13 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 5.3.2.3.4.<br>对 COMMON，执行条款 5.3.2.3.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 13 项原子timing规则。 | — |
| `CRS-615A3-0128` | `ARINC-615A-3 5.3.2.3.4 p.56` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 14 governing ABORT / STATUS / UPLOAD / DOWNLOAD at clause 5.3.2.3.4.<br>对 COMMON，执行条款 5.3.2.3.4 中治理 ABORT / STATUS / UPLOAD / DOWNLOAD 的第 14 项原子timing规则。 | — |
| `CRS-615A3-0129` | `ARINC-615A-3 5.3.2.3.4 p.56` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 15 governing STATUS / CHECKSUM / CRC / DATA-FILE at clause 5.3.2.3.4.<br>对 COMMON，执行条款 5.3.2.3.4 中治理 STATUS / CHECKSUM / CRC / DATA-FILE 的第 15 项原子data format规则。 | GAP-ARINC-645 |
| `CRS-615A3-0130` | `ARINC-615A-3 6.3.5 p.64` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 1 governing TIMEOUT at clause 6.3.5.<br>对 COMMON，执行条款 6.3.5 中治理 TIMEOUT 的第 1 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0131` | `ARINC-615A-3 6.3.5 p.64` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 2 governing ABORT / STATUS at clause 6.3.5.<br>对 COMMON，执行条款 6.3.5 中治理 ABORT / STATUS 的第 2 项原子data format规则。 | — |
| `CRS-615A3-0132` | `ARINC-615A-3 6.3.5 p.64` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 3 governing ABORT / STATUS / ERROR at clause 6.3.5.<br>对 COMMON，执行条款 6.3.5 中治理 ABORT / STATUS / ERROR 的第 3 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0133` | `ARINC-615A-3 6.3.5 p.64` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 4 governing ABORT / STATUS at clause 6.3.5.<br>对 COMMON，执行条款 6.3.5 中治理 ABORT / STATUS 的第 4 项原子data format规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0134` | `ARINC-615A-3 6.4 p.65` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 1 governing PROTOCOL-VERSION at clause 6.4.<br>对 COMMON，执行条款 6.4 中治理 PROTOCOL-VERSION 的第 1 项原子data format规则。 | — |
| `CRS-615A3-0135` | `ARINC-615A-3 6.4 p.65` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic protocol behavior rule 2 governing PROTOCOL-VERSION at clause 6.4.<br>对 COMMON，执行条款 6.4 中治理 PROTOCOL-VERSION 的第 2 项原子protocol behavior规则。 | — |
| `CRS-615A3-0136` | `ARINC-615A-3 6.4 p.65` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 3 governing PROTOCOL-VERSION at clause 6.4.<br>对 COMMON，执行条款 6.4 中治理 PROTOCOL-VERSION 的第 3 项原子data format规则。 | — |
| `CRS-615A3-0137` | `ARINC-615A-3 6.4 p.65` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 4 governing PROTOCOL-VERSION at clause 6.4.<br>对 COMMON，执行条款 6.4 中治理 PROTOCOL-VERSION 的第 4 项原子data format规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0138` | `ARINC-615A-3 6.4 p.65` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic error status rule 5 governing PROTOCOL-VERSION / ABORT at clause 6.4.<br>对 COMMON，执行条款 6.4 中治理 PROTOCOL-VERSION / ABORT 的第 5 项原子error status规则。 | — |
| `CRS-615A3-0139` | `ARINC-615A-3 6.4 p.65` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 6 governing PROTOCOL-VERSION / ABORT / STATUS at clause 6.4.<br>对 COMMON，执行条款 6.4 中治理 PROTOCOL-VERSION / ABORT / STATUS 的第 6 项原子data format规则。 | — |
| `CRS-615A3-0140` | `ARINC-615A-3 6.4 p.65` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 7 governing PROTOCOL-VERSION at clause 6.4.<br>对 COMMON，执行条款 6.4 中治理 PROTOCOL-VERSION 的第 7 项原子data format规则。 | — |
| `CRS-615A3-0141` | `ARINC-615A-3 6.4 p.65` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 8 governing PART-NUMBER / ZERO-TERMINATION at clause 6.4.<br>对 COMMON，执行条款 6.4 中治理 PART-NUMBER / ZERO-TERMINATION 的第 8 项原子data format规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0142` | `ARINC-615A-3 6.4 p.65` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 9 governing ZERO-TERMINATION at clause 6.4.<br>对 COMMON，执行条款 6.4 中治理 ZERO-TERMINATION 的第 9 项原子data format规则。 | — |
| `CRS-615A3-0143` | `ARINC-615A-3 6.4 p.66` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 10 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.<br>对 COMMON，执行条款 6.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 10 项原子data format规则。 | — |
| `CRS-615A3-0144` | `ARINC-615A-3 6.4.2 p.68` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic protocol behavior rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.2.<br>对 INFORMATION，执行条款 6.4.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | — |
| `CRS-615A3-0145` | `ARINC-615A-3 6.4.2 p.68` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic data format rule 2 governing PROTOCOL-VERSION / PART-NUMBER / ZERO-TERMINATION at clause 6.4.2.<br>对 INFORMATION，执行条款 6.4.2 中治理 PROTOCOL-VERSION / PART-NUMBER / ZERO-TERMINATION 的第 2 项原子data format规则。 | — |
| `CRS-615A3-0146` | `ARINC-615A-3 6.4.2 p.69` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic protocol behavior rule 3 governing ZERO-TERMINATION at clause 6.4.2.<br>对 INFORMATION，执行条款 6.4.2 中治理 ZERO-TERMINATION 的第 3 项原子protocol behavior规则。 | — |
| `CRS-615A3-0147` | `ARINC-615A-3 6.4.2 p.69` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic protocol behavior rule 4 governing ZERO-TERMINATION at clause 6.4.2.<br>对 INFORMATION，执行条款 6.4.2 中治理 ZERO-TERMINATION 的第 4 项原子protocol behavior规则。 | — |
| `CRS-615A3-0148` | `ARINC-615A-3 6.4.3 p.70` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic protocol behavior rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.3.<br>对 INFORMATION，执行条款 6.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | — |
| `CRS-615A3-0149` | `ARINC-615A-3 6.4.3 p.70` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic timing rule 2 governing PROTOCOL-VERSION / STATUS / INFORMATION / ZERO-TERMINATION at clause 6.4.3.<br>对 INFORMATION，执行条款 6.4.3 中治理 PROTOCOL-VERSION / STATUS / INFORMATION / ZERO-TERMINATION 的第 2 项原子timing规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0150` | `ARINC-615A-3 6.4.4 p.72` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic data format rule 1 governing STATUS at clause 6.4.4.<br>对 UPLOAD，执行条款 6.4.4 中治理 STATUS 的第 1 项原子data format规则。 | — |
| `CRS-615A3-0151` | `ARINC-615A-3 6.4.4 p.72` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic timing rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.4.<br>对 UPLOAD，执行条款 6.4.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子timing规则。 | — |
| `CRS-615A3-0152` | `ARINC-615A-3 6.4.4 p.72` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic timing rule 3 governing STATUS at clause 6.4.4.<br>对 UPLOAD，执行条款 6.4.4 中治理 STATUS 的第 3 项原子timing规则。 | — |
| `CRS-615A3-0153` | `ARINC-615A-3 6.4.4 p.72` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic data format rule 4 governing STATUS at clause 6.4.4.<br>对 UPLOAD，执行条款 6.4.4 中治理 STATUS 的第 4 项原子data format规则。 | — |
| `CRS-615A3-0154` | `ARINC-615A-3 6.4.4 p.72` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic protocol behavior rule 5 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.4.<br>对 UPLOAD，执行条款 6.4.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子protocol behavior规则。 | — |
| `CRS-615A3-0155` | `ARINC-615A-3 6.4.4 p.72` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic data format rule 6 governing PROTOCOL-VERSION / FILE-NAME / PART-NUMBER / HEADER-FILE at clause 6.4.4.<br>对 UPLOAD，执行条款 6.4.4 中治理 PROTOCOL-VERSION / FILE-NAME / PART-NUMBER / HEADER-FILE 的第 6 项原子data format规则。 | — |
| `CRS-615A3-0156` | `ARINC-615A-3 6.4.4 p.73` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic data format rule 7 governing HEADER-FILE at clause 6.4.4.<br>对 UPLOAD，执行条款 6.4.4 中治理 HEADER-FILE 的第 7 项原子data format规则。 | — |
| `CRS-615A3-0157` | `ARINC-615A-3 6.4.4 p.73` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic protocol behavior rule 8 governing ZERO-TERMINATION at clause 6.4.4.<br>对 UPLOAD，执行条款 6.4.4 中治理 ZERO-TERMINATION 的第 8 项原子protocol behavior规则。 | — |
| `CRS-615A3-0158` | `ARINC-615A-3 6.4.4 p.73` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic protocol behavior rule 9 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.4.<br>对 UPLOAD，执行条款 6.4.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 9 项原子protocol behavior规则。 | — |
| `CRS-615A3-0159` | `ARINC-615A-3 6.4.5 p.75` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic data format rule 1 governing STATUS at clause 6.4.5.<br>对 UPLOAD，执行条款 6.4.5 中治理 STATUS 的第 1 项原子data format规则。 | — |
| `CRS-615A3-0160` | `ARINC-615A-3 6.4.5 p.75` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic protocol behavior rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.5.<br>对 UPLOAD，执行条款 6.4.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | — |
| `CRS-615A3-0161` | `ARINC-615A-3 6.4.5 p.75` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic protocol behavior rule 3 governing ZERO-TERMINATION at clause 6.4.5.<br>对 UPLOAD，执行条款 6.4.5 中治理 ZERO-TERMINATION 的第 3 项原子protocol behavior规则。 | — |
| `CRS-615A3-0162` | `ARINC-615A-3 6.4.5 p.76` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic data format rule 4 governing STATUS at clause 6.4.5.<br>对 UPLOAD，执行条款 6.4.5 中治理 STATUS 的第 4 项原子data format规则。 | — |
| `CRS-615A3-0163` | `ARINC-615A-3 6.4.5 p.76` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic timing rule 5 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.5.<br>对 UPLOAD，执行条款 6.4.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子timing规则。 | — |
| `CRS-615A3-0164` | `ARINC-615A-3 6.4.5 p.76` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic timing rule 6 governing STATUS at clause 6.4.5.<br>对 UPLOAD，执行条款 6.4.5 中治理 STATUS 的第 6 项原子timing规则。 | — |
| `CRS-615A3-0165` | `ARINC-615A-3 6.4.5 p.76` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic data format rule 7 governing HEADER-FILE at clause 6.4.5.<br>对 UPLOAD，执行条款 6.4.5 中治理 HEADER-FILE 的第 7 项原子data format规则。 | — |
| `CRS-615A3-0166` | `ARINC-615A-3 6.4.5 p.76` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic protocol behavior rule 8 governing ZERO-TERMINATION at clause 6.4.5.<br>对 UPLOAD，执行条款 6.4.5 中治理 ZERO-TERMINATION 的第 8 项原子protocol behavior规则。 | — |
| `CRS-615A3-0167` | `ARINC-615A-3 6.4.5 p.77` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | For UPLOAD, enforce atomic protocol behavior rule 9 governing ZERO-TERMINATION at clause 6.4.5.<br>对 UPLOAD，执行条款 6.4.5 中治理 ZERO-TERMINATION 的第 9 项原子protocol behavior规则。 | — |
| `CRS-615A3-0168` | `ARINC-615A-3 6.4.10 p.82` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic data format rule 1 governing STATUS at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 STATUS 的第 1 项原子data format规则。 | — |
| `CRS-615A3-0169` | `ARINC-615A-3 6.4.10 p.82` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic protocol behavior rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | — |
| `CRS-615A3-0170` | `ARINC-615A-3 6.4.10 p.82` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic protocol behavior rule 3 governing ZERO-TERMINATION at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 ZERO-TERMINATION 的第 3 项原子protocol behavior规则。 | — |
| `CRS-615A3-0171` | `ARINC-615A-3 6.4.10 p.84` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic protocol behavior rule 4 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子protocol behavior规则。 | — |
| `CRS-615A3-0172` | `ARINC-615A-3 6.4.10 p.84` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic data format rule 5 governing PROTOCOL-VERSION / FILE-NAME / DOWNLOAD / ZERO-TERMINATION at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 PROTOCOL-VERSION / FILE-NAME / DOWNLOAD / ZERO-TERMINATION 的第 5 项原子data format规则。 | — |
| `CRS-615A3-0173` | `ARINC-615A-3 6.4.10 p.84` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic data format rule 6 governing STATUS / ZERO-TERMINATION at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 STATUS / ZERO-TERMINATION 的第 6 项原子data format规则。 | — |
| `CRS-615A3-0174` | `ARINC-615A-3 6.4.10 p.85` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic timing rule 7 governing STATUS / UPLOAD / DOWNLOAD at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 STATUS / UPLOAD / DOWNLOAD 的第 7 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0175` | `ARINC-615A-3 6.4.10 p.85` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic data format rule 8 governing ABORT / STATUS / FILE-NAME / PART-NUMBER at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 ABORT / STATUS / FILE-NAME / PART-NUMBER 的第 8 项原子data format规则。 | — |
| `CRS-615A3-0176` | `ARINC-615A-3 6.4.10 p.87` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic transport rule 9 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 9 项原子transport规则。 | — |
| `CRS-615A3-0177` | `ARINC-615A-3 6.4.10 p.87` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic transport rule 10 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 10 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0178` | `ARINC-615A-3 6.4.10 p.87` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic transport rule 11 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 11 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0179` | `ARINC-615A-3 6.4.10 p.87` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic transport rule 12 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 12 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0180` | `ARINC-615A-3 6.4.10 p.87` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic protocol behavior rule 13 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 13 项原子protocol behavior规则。 | — |
| `CRS-615A3-0181` | `ARINC-615A-3 6.4.10 p.87` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic protocol behavior rule 14 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 14 项原子protocol behavior规则。 | — |
| `CRS-615A3-0182` | `ARINC-615A-3 6.4.10 p.87` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic protocol behavior rule 15 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 15 项原子protocol behavior规则。 | — |
| `CRS-615A3-0183` | `ARINC-615A-3 6.4.10 p.87` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic protocol behavior rule 16 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 16 项原子protocol behavior规则。 | — |
| `CRS-615A3-0184` | `ARINC-615A-3 6.4.10 p.87` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic protocol behavior rule 17 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 17 项原子protocol behavior规则。 | — |
| `CRS-615A3-0185` | `ARINC-615A-3 6.4.10 p.87` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic protocol behavior rule 18 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 18 项原子protocol behavior规则。 | — |
| `CRS-615A3-0186` | `ARINC-615A-3 6.4.10 p.87` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For INFORMATION, enforce atomic protocol behavior rule 19 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 6.4.10.<br>对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 19 项原子protocol behavior规则。 | — |
| `CRS-615A3-0187` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 1 governing TIMEOUT / RETRY at clause 4-1.<br>对 COMMON，执行条款 4-1 中治理 TIMEOUT / RETRY 的第 1 项原子timing规则。 | — |
| `CRS-615A3-0188` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 2 governing TIMEOUT at clause 4-1.<br>对 COMMON，执行条款 4-1 中治理 TIMEOUT 的第 2 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0189` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 3 governing TIMEOUT / ERROR at clause 4-1.<br>对 COMMON，执行条款 4-1 中治理 TIMEOUT / ERROR 的第 3 项原子timing规则。 | — |
| `CRS-615A3-0190` | `ARINC-615A-3 4-1 p.99` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 4 governing TIMEOUT / RETRY / CRC / ERROR at clause 4-1.<br>对 COMMON，执行条款 4-1 中治理 TIMEOUT / RETRY / CRC / ERROR 的第 4 项原子timing规则。 | DEP-RFC-TFTP, GAP-ARINC-645 |
| `CRS-615A3-0191` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic retry policy rule 5 governing RETRY / ERROR at clause 4-1.<br>对 COMMON，执行条款 4-1 中治理 RETRY / ERROR 的第 5 项原子retry policy规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0192` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic error status rule 6 governing ERROR at clause 4-1.<br>对 COMMON，执行条款 4-1 中治理 ERROR 的第 6 项原子error status规则。 | — |
| `CRS-615A3-0193` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic retry policy rule 7 governing RETRY / UPLOAD / DOWNLOAD / ERROR at clause 4-1.<br>对 COMMON，执行条款 4-1 中治理 RETRY / UPLOAD / DOWNLOAD / ERROR 的第 7 项原子retry policy规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0194` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic retry policy rule 8 governing RETRY / ERROR at clause 4-1.<br>对 COMMON，执行条款 4-1 中治理 RETRY / ERROR 的第 8 项原子retry policy规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0195` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic error status rule 9 governing ERROR at clause 4-1.<br>对 COMMON，执行条款 4-1 中治理 ERROR 的第 9 项原子error status规则。 | — |
| `CRS-615A3-0196` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 10 governing TIMEOUT at clause 4-1.<br>对 COMMON，执行条款 4-1 中治理 TIMEOUT 的第 10 项原子timing规则。 | — |
| `CRS-615A3-0197` | `ARINC-615A-3 4-3 p.100` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 1 governing TIMEOUT at clause 4-3.<br>对 COMMON，执行条款 4-3 中治理 TIMEOUT 的第 1 项原子timing规则。 | — |
| `CRS-615A3-0198` | `ARINC-615A-3 4-3 p.100` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic transport rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 4-3.<br>对 COMMON，执行条款 4-3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子transport规则。 | DEP-IP-UDP-664, DEP-RFC-TFTP |
| `CRS-615A3-0199` | `ARINC-615A-3 4-3 p.100` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic transport rule 3 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 4-3.<br>对 COMMON，执行条款 4-3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子transport规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0200` | `ARINC-615A-3 4-3 p.101` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 4 governing RETRY / ERROR at clause 4-3.<br>对 COMMON，执行条款 4-3 中治理 RETRY / ERROR 的第 4 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0201` | `ARINC-615A-3 4-3 p.101` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic retry policy rule 5 governing RETRY at clause 4-3.<br>对 COMMON，执行条款 4-3 中治理 RETRY 的第 5 项原子retry policy规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0202` | `ARINC-615A-3 4-4 p.102` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 1 governing TIMEOUT / RETRY at clause 4-4.<br>对 COMMON，执行条款 4-4 中治理 TIMEOUT / RETRY 的第 1 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0203` | `ARINC-615A-3 4-4 p.102` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 2 governing TIMEOUT at clause 4-4.<br>对 COMMON，执行条款 4-4 中治理 TIMEOUT 的第 2 项原子timing规则。 | DEP-IP-UDP-664, DEP-RFC-TFTP |
| `CRS-615A3-0204` | `ARINC-615A-3 4-4 p.102` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 3 governing TIMEOUT at clause 4-4.<br>对 COMMON，执行条款 4-4 中治理 TIMEOUT 的第 3 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0205` | `ARINC-615A-3 4-4 p.102` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 4 governing TIMEOUT at clause 4-4.<br>对 COMMON，执行条款 4-4 中治理 TIMEOUT 的第 4 项原子timing规则。 | — |
| `CRS-615A3-0206` | `ARINC-615A-3 4-4 p.102` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 5 governing STATUS at clause 4-4.<br>对 COMMON，执行条款 4-4 中治理 STATUS 的第 5 项原子data format规则。 | — |
| `CRS-615A3-0207` | `ARINC-615A-3 4-4 p.102` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 6 governing TIMEOUT at clause 4-4.<br>对 COMMON，执行条款 4-4 中治理 TIMEOUT 的第 6 项原子timing规则。 | — |
| `CRS-615A3-0208` | `ARINC-615A-3 4-4 p.102` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 7 governing TIMEOUT at clause 4-4.<br>对 COMMON，执行条款 4-4 中治理 TIMEOUT 的第 7 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0209` | `ARINC-615A-3 4-4 p.103` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 8 governing RETRY / ERROR at clause 4-4.<br>对 COMMON，执行条款 4-4 中治理 RETRY / ERROR 的第 8 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0210` | `ARINC-615A-3 4-4 p.104` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic timing rule 9 governing TIMEOUT / RETRY at clause 4-4.<br>对 COMMON，执行条款 4-4 中治理 TIMEOUT / RETRY 的第 9 项原子timing规则。 | — |
| `CRS-615A3-0211` | `ARINC-615A-3 4-4 p.104` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic data format rule 10 governing ERROR at clause 4-4.<br>对 COMMON，执行条款 4-4 中治理 ERROR 的第 10 项原子data format规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0212` | `ARINC-615A-3 4-4 p.106` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic protocol behavior rule 11 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 4-4.<br>对 COMMON，执行条款 4-4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 11 项原子protocol behavior规则。 | — |
| `CRS-615A3-0213` | `ARINC-615A-3 4-4 p.106` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For COMMON, enforce atomic error status rule 12 governing UPLOAD / DOWNLOAD / ERROR at clause 4-4.<br>对 COMMON，执行条款 4-4 中治理 UPLOAD / DOWNLOAD / ERROR 的第 12 项原子error status规则。 | — |
| `CRS-615A3-0214` | `ARINC-615A-3 6.1 p.42` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Table 6-1 fixes Information message direction between DLA and DLP.<br>表 6-1 固定 Information 消息在 DLA 与 DLP 间的方向。 | — |
| `CRS-615A3-0215` | `ARINC-615A-3 6.1 p.42` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Table 6-1 fixes Upload message direction between DLA and DLP.<br>表 6-1 固定 Upload 消息在 DLA 与 DLP 间的方向。 | — |
| `CRS-615A3-0216` | `ARINC-615A-3 6.3.1 p.50` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Information follows the initialization, LCI, LCL, status and completion ordering shown by the chart.<br>Information 遵循图示初始化、LCI、LCL、状态及完成顺序。 | DEP-RFC-TFTP |
| `CRS-615A3-0217` | `ARINC-615A-3 6.3.2 p.53` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Upload initialization and list transfer follow the first chart segment.<br>Upload 初始化及清单传输遵循序列图第一段。 | DEP-RFC-TFTP |
| `CRS-615A3-0218` | `ARINC-615A-3 6.3.2 p.54` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Upload file transfer, unavailable-file handling and completion status follow the second chart segment.<br>Upload 文件传输、文件不可用处理及完成状态遵循序列图第二段。 | DEP-RFC-TFTP |
| `CRS-615A3-0219` | `ARINC-615A-3 6.3.5 p.63` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Interruption follows the charted abort request, stop, confirmation and termination sequence.<br>中断遵循图示中止请求、停止、确认及终止顺序。 | DEP-RFC-TFTP |
| `CRS-6655-0001` | `ARINC-665-5 1.3.3 p.1` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic protocol behavior rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.3.3.<br>对 DATA-OBJECT，执行条款 1.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0002` | `ARINC-665-5 1.3.3 p.1` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic transport rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.3.3.<br>对 DATA-OBJECT，执行条款 1.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子transport规则。 | DEP-ARINC-6655 |
| `CRS-6655-0003` | `ARINC-665-5 1.3.3 p.1` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic protocol behavior rule 3 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.3.3.<br>对 DATA-OBJECT，执行条款 1.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0004` | `ARINC-665-5 1.3.3 p.1` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic protocol behavior rule 4 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.3.3.<br>对 DATA-OBJECT，执行条款 1.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0005` | `ARINC-665-5 1.3.3 p.1` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 5 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.3.3.<br>对 DATA-OBJECT，执行条款 1.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0006` | `ARINC-665-5 1.3.3 p.1` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 6 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.3.3.<br>对 DATA-OBJECT，执行条款 1.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0007` | `ARINC-665-5 1.4.2 p.2` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic protocol behavior rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.2.<br>对 DATA-OBJECT，执行条款 1.4.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0008` | `ARINC-665-5 1.4.2 p.2` | `MAY` / `OPTIONAL` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic data format rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.2.<br>对 DATA-OBJECT，执行条款 1.4.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0009` | `ARINC-665-5 1.4.2 p.2` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 3 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.2.<br>对 DATA-OBJECT，执行条款 1.4.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0010` | `ARINC-665-5 1.4.4 p.3` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.4.<br>对 DATA-OBJECT，执行条款 1.4.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0011` | `ARINC-665-5 1.4.4 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.4.<br>对 DATA-OBJECT，执行条款 1.4.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0012` | `ARINC-665-5 1.4.4 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 3 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.4.4.<br>对 DATA-OBJECT，执行条款 1.4.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0013` | `ARINC-665-5 1.4.4 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 4 governing PART-NUMBER / HEADER-FILE at clause 1.4.4.<br>对 DATA-OBJECT，执行条款 1.4.4 中治理 PART-NUMBER / HEADER-FILE 的第 4 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0014` | `ARINC-665-5 1.5 p.4` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic transport rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.5.<br>对 DATA-OBJECT，执行条款 1.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | DEP-ARINC-6655 |
| `CRS-6655-0015` | `ARINC-665-5 1.5 p.4` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic protocol behavior rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.5.<br>对 DATA-OBJECT，执行条款 1.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0016` | `ARINC-665-5 1.5 p.4` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 3 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.5.<br>对 DATA-OBJECT，执行条款 1.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0017` | `ARINC-665-5 1.5 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic protocol behavior rule 4 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.5.<br>对 DATA-OBJECT，执行条款 1.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0018` | `ARINC-665-5 1.5 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic transport rule 5 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 1.5.<br>对 DATA-OBJECT，执行条款 1.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子transport规则。 | DEP-ARINC-6655 |
| `CRS-6655-0019` | `ARINC-665-5 2.1.1 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic protocol behavior rule 1 governing PART-NUMBER at clause 2.1.1.<br>对 DATA-OBJECT，执行条款 2.1.1 中治理 PART-NUMBER 的第 1 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0020` | `ARINC-665-5 2.1.1 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic protocol behavior rule 2 governing PART-NUMBER at clause 2.1.1.<br>对 DATA-OBJECT，执行条款 2.1.1 中治理 PART-NUMBER 的第 2 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0021` | `ARINC-665-5 2.1.1 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic timing rule 3 governing PART-NUMBER at clause 2.1.1.<br>对 DATA-OBJECT，执行条款 2.1.1 中治理 PART-NUMBER 的第 3 项原子timing规则。 | DEP-ARINC-6655 |
| `CRS-6655-0022` | `ARINC-665-5 2.1.1 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 4 governing PART-NUMBER / FIND at clause 2.1.1.<br>对 DATA-OBJECT，执行条款 2.1.1 中治理 PART-NUMBER / FIND 的第 4 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0023` | `ARINC-665-5 2.1.1 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 5 governing PART-NUMBER at clause 2.1.1.<br>对 DATA-OBJECT，执行条款 2.1.1 中治理 PART-NUMBER 的第 5 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0024` | `ARINC-665-5 2.1.1 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 6 governing PART-NUMBER at clause 2.1.1.<br>对 DATA-OBJECT，执行条款 2.1.1 中治理 PART-NUMBER 的第 6 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0025` | `ARINC-665-5 2.1.1 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 7 governing PART-NUMBER at clause 2.1.1.<br>对 DATA-OBJECT，执行条款 2.1.1 中治理 PART-NUMBER 的第 7 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0026` | `ARINC-665-5 2.1.1 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic protocol behavior rule 8 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.1.1.<br>对 DATA-OBJECT，执行条款 2.1.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 8 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0027` | `ARINC-665-5 2.1.1 p.6` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic protocol behavior rule 9 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.1.1.<br>对 DATA-OBJECT，执行条款 2.1.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 9 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0028` | `ARINC-665-5 2.1.4 p.7` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic transport rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.1.4.<br>对 DATA-OBJECT，执行条款 2.1.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | DEP-ARINC-6655 |
| `CRS-6655-0029` | `ARINC-665-5 2.1.4 p.7` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 2 governing PART-NUMBER at clause 2.1.4.<br>对 DATA-OBJECT，执行条款 2.1.4 中治理 PART-NUMBER 的第 2 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0030` | `ARINC-665-5 2.1.4 p.7` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic protocol behavior rule 3 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.1.4.<br>对 DATA-OBJECT，执行条款 2.1.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0031` | `ARINC-665-5 2.1.4 p.7` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 4 governing PART-NUMBER / ERROR at clause 2.1.4.<br>对 DATA-OBJECT，执行条款 2.1.4 中治理 PART-NUMBER / ERROR 的第 4 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0032` | `ARINC-665-5 2.1.4 p.7` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic protocol behavior rule 5 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.1.4.<br>对 DATA-OBJECT，执行条款 2.1.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0033` | `ARINC-665-5 2.1.4 p.7` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic transport rule 6 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.1.4.<br>对 DATA-OBJECT，执行条款 2.1.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子transport规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0034` | `ARINC-665-5 2.2.3.1 p.8` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.<br>对 DATA-OBJECT，执行条款 2.2.3.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0035` | `ARINC-665-5 2.2.3.1 p.8` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 2 governing FILE-NAME at clause 2.2.3.1.<br>对 DATA-OBJECT，执行条款 2.2.3.1 中治理 FILE-NAME 的第 2 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0036` | `ARINC-665-5 2.2.3.1 p.8` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 3 governing FILE-NAME / HEADER-FILE at clause 2.2.3.1.<br>对 DATA-OBJECT，执行条款 2.2.3.1 中治理 FILE-NAME / HEADER-FILE 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0037` | `ARINC-665-5 2.2.3.1 p.8` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 4 governing HEADER-FILE / DATA-FILE at clause 2.2.3.1.<br>对 DATA-OBJECT，执行条款 2.2.3.1 中治理 HEADER-FILE / DATA-FILE 的第 4 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0038` | `ARINC-665-5 2.2.3.1 p.8` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic protocol behavior rule 5 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.<br>对 DATA-OBJECT，执行条款 2.2.3.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0039` | `ARINC-665-5 2.2.3.1 p.8` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 6 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.<br>对 DATA-OBJECT，执行条款 2.2.3.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0040` | `ARINC-665-5 2.2.3.1 p.8` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 7 governing FILE-NAME / HEADER-FILE / DATA-FILE at clause 2.2.3.1.<br>对 DATA-OBJECT，执行条款 2.2.3.1 中治理 FILE-NAME / HEADER-FILE / DATA-FILE 的第 7 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0041` | `ARINC-665-5 2.2.3.1.7 p.11` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 1 governing UPLOAD / DOWNLOAD at clause 2.2.3.1.7.<br>对 DATA-OBJECT，执行条款 2.2.3.1.7 中治理 UPLOAD / DOWNLOAD 的第 1 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0042` | `ARINC-665-5 2.2.3.1.7 p.11` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 2 governing PART-NUMBER / DATA-FILE / DOWNLOAD at clause 2.2.3.1.7.<br>对 DATA-OBJECT，执行条款 2.2.3.1.7 中治理 PART-NUMBER / DATA-FILE / DOWNLOAD 的第 2 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0043` | `ARINC-665-5 2.2.3.1.16 p.12` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.16.<br>对 DATA-OBJECT，执行条款 2.2.3.1.16 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0044` | `ARINC-665-5 2.2.3.1.16 p.12` | `MAY` / `OPTIONAL` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic data format rule 2 governing PART-NUMBER at clause 2.2.3.1.16.<br>对 DATA-OBJECT，执行条款 2.2.3.1.16 中治理 PART-NUMBER 的第 2 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0045` | `ARINC-665-5 2.2.3.1.16 p.12` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 3 governing PART-NUMBER at clause 2.2.3.1.16.<br>对 DATA-OBJECT，执行条款 2.2.3.1.16 中治理 PART-NUMBER 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0046` | `ARINC-665-5 2.2.3.1.20 p.13` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.20.<br>对 DATA-OBJECT，执行条款 2.2.3.1.20 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0047` | `ARINC-665-5 2.2.3.1.20 p.13` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic protocol behavior rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.20.<br>对 DATA-OBJECT，执行条款 2.2.3.1.20 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0048` | `ARINC-665-5 2.2.3.1.20 p.13` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 3 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.20.<br>对 DATA-OBJECT，执行条款 2.2.3.1.20 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0049` | `ARINC-665-5 2.2.3.1.28 p.14` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.28.<br>对 DATA-OBJECT，执行条款 2.2.3.1.28 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0050` | `ARINC-665-5 2.2.3.1.28 p.14` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.28.<br>对 DATA-OBJECT，执行条款 2.2.3.1.28 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0051` | `ARINC-665-5 2.2.3.1.28 p.14` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 3 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.28.<br>对 DATA-OBJECT，执行条款 2.2.3.1.28 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0052` | `ARINC-665-5 2.2.3.1.36 p.15` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 1 governing DATA-FILE at clause 2.2.3.1.36.<br>对 DATA-OBJECT，执行条款 2.2.3.1.36 中治理 DATA-FILE 的第 1 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0053` | `ARINC-665-5 2.2.3.1.36 p.15` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 2 governing DATA-FILE at clause 2.2.3.1.36.<br>对 DATA-OBJECT，执行条款 2.2.3.1.36 中治理 DATA-FILE 的第 2 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0054` | `ARINC-665-5 2.2.3.1.36 p.15` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 3 governing FILE-NAME / DATA-FILE at clause 2.2.3.1.36.<br>对 DATA-OBJECT，执行条款 2.2.3.1.36 中治理 FILE-NAME / DATA-FILE 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0055` | `ARINC-665-5 2.2.3.1.43 p.16` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic data format rule 1 governing CRC / DATA-FILE at clause 2.2.3.1.43.<br>对 DATA-OBJECT，执行条款 2.2.3.1.43 中治理 CRC / DATA-FILE 的第 1 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0056` | `ARINC-665-5 2.2.3.1.43 p.16` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic data format rule 2 governing CRC / DATA-FILE at clause 2.2.3.1.43.<br>对 DATA-OBJECT，执行条款 2.2.3.1.43 中治理 CRC / DATA-FILE 的第 2 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0057` | `ARINC-665-5 2.2.3.1.43 p.16` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic data format rule 3 governing DATA-FILE at clause 2.2.3.1.43.<br>对 DATA-OBJECT，执行条款 2.2.3.1.43 中治理 DATA-FILE 的第 3 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0058` | `ARINC-665-5 2.2.3.1.43 p.16` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic protocol behavior rule 4 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.43.<br>对 DATA-OBJECT，执行条款 2.2.3.1.43 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子protocol behavior规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0059` | `ARINC-665-5 2.2.3.1.43 p.16` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic protocol behavior rule 5 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.43.<br>对 DATA-OBJECT，执行条款 2.2.3.1.43 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子protocol behavior规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0060` | `ARINC-665-5 2.2.3.1.43 p.16` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic data format rule 6 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.43.<br>对 DATA-OBJECT，执行条款 2.2.3.1.43 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0061` | `ARINC-665-5 2.2.3.1.43 p.16` | `MAY` / `OPTIONAL` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic data format rule 7 governing DATA-FILE at clause 2.2.3.1.43.<br>对 DATA-OBJECT，执行条款 2.2.3.1.43 中治理 DATA-FILE 的第 7 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0062` | `ARINC-665-5 2.2.3.1.51 p.17` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.51.<br>对 DATA-OBJECT，执行条款 2.2.3.1.51 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0063` | `ARINC-665-5 2.2.3.1.51 p.17` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 2 governing FILE-NAME at clause 2.2.3.1.51.<br>对 DATA-OBJECT，执行条款 2.2.3.1.51 中治理 FILE-NAME 的第 2 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0064` | `ARINC-665-5 2.2.3.1.51 p.17` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 3 governing PART-NUMBER at clause 2.2.3.1.51.<br>对 DATA-OBJECT，执行条款 2.2.3.1.51 中治理 PART-NUMBER 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0065` | `ARINC-665-5 2.2.3.1.51 p.17` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 4 governing PART-NUMBER at clause 2.2.3.1.51.<br>对 DATA-OBJECT，执行条款 2.2.3.1.51 中治理 PART-NUMBER 的第 4 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0066` | `ARINC-665-5 2.2.3.1.51 p.17` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic transport rule 5 governing CRC at clause 2.2.3.1.51.<br>对 DATA-OBJECT，执行条款 2.2.3.1.51 中治理 CRC 的第 5 项原子transport规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0067` | `ARINC-665-5 2.2.3.1.60 p.18` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic protocol behavior rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.60.<br>对 DATA-OBJECT，执行条款 2.2.3.1.60 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0068` | `ARINC-665-5 2.2.3.1.60 p.18` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic protocol behavior rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.60.<br>对 DATA-OBJECT，执行条款 2.2.3.1.60 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0069` | `ARINC-665-5 2.2.3.1.60 p.18` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic data format rule 3 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.60.<br>对 DATA-OBJECT，执行条款 2.2.3.1.60 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0070` | `ARINC-665-5 2.2.3.1.60 p.18` | `MAY` / `OPTIONAL` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic data format rule 4 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.60.<br>对 DATA-OBJECT，执行条款 2.2.3.1.60 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0071` | `ARINC-665-5 2.2.3.1.60 p.18` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 5 governing HEADER-FILE at clause 2.2.3.1.60.<br>对 DATA-OBJECT，执行条款 2.2.3.1.60 中治理 HEADER-FILE 的第 5 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0072` | `ARINC-665-5 2.2.3.1.60 p.18` | `MAY` / `OPTIONAL` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic data format rule 6 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.1.60.<br>对 DATA-OBJECT，执行条款 2.2.3.1.60 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0073` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic protocol behavior rule 1 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.3.<br>对 DATA-OBJECT，执行条款 2.2.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0074` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic protocol behavior rule 2 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.3.<br>对 DATA-OBJECT，执行条款 2.2.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0075` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic protocol behavior rule 3 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.3.<br>对 DATA-OBJECT，执行条款 2.2.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子protocol behavior规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0076` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic data format rule 4 governing CRC / HEADER-FILE / DATA-FILE at clause 2.2.3.3.<br>对 DATA-OBJECT，执行条款 2.2.3.3 中治理 CRC / HEADER-FILE / DATA-FILE 的第 4 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0077` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic data format rule 5 governing CRC / HEADER-FILE at clause 2.2.3.3.<br>对 DATA-OBJECT，执行条款 2.2.3.3 中治理 CRC / HEADER-FILE 的第 5 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0078` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | For DATA-OBJECT, enforce atomic transport rule 6 governing CRC at clause 2.2.3.3.<br>对 DATA-OBJECT，执行条款 2.2.3.3 中治理 CRC 的第 6 项原子transport规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0079` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 7 governing DATA-FILE at clause 2.2.3.3.<br>对 DATA-OBJECT，执行条款 2.2.3.3 中治理 DATA-FILE 的第 7 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0080` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 8 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.3.<br>对 DATA-OBJECT，执行条款 2.2.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 8 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0081` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | For DATA-OBJECT, enforce atomic data format rule 9 governing CLAUSE-SPECIFIC-BEHAVIOR at clause 2.2.3.3.<br>对 DATA-OBJECT，执行条款 2.2.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 9 项原子data format规则。 | DEP-ARINC-6655 |

## Non-base and unresolved inventory

- `COV-615A3-0038` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0039` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0040` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0041` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0042` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0043` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0044` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0045` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0046` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0047` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0048` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0049` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0050` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0051` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0052` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0053` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0054` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0055` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0056` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0057` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0058` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0059` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0060` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0061` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0062` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0063` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0064` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0065` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0066` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0067` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0068` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0069` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0070` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0071` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0072` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0073` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0074` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0075` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0076` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0077` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0078` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0079` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0080` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0081` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0082` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0083` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0084` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0085` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0086` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0087` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0088` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0089` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0090` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0091` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0092` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0093` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0094` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0095` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0096` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0097` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0098` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0099` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0100` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0101` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0102` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0103` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0104` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0105` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0106` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0107` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0108` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0109` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0110` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0111` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0112` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0113` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0114` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0115` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0116` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0117` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0118` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0119` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0120` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0121` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0122` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0123` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0124` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0125` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0126` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0127` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0128` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0129` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0130` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0131` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0132` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0133` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0134` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0135` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0136` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0137` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0138` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0139` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0140` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0141` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0142` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0143` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0144` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0145` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0146` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0147` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0148` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0187` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0188` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0189` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0190` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0220` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0221` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0222` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0223` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0224` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0225` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0226` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0227` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0228` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0254` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0255` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0256` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0257` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0258` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0259` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0260` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0261` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0262` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0263` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0264` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0265` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0266` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0267` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0306` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0307` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0308` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0309` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0310` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0311` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0312` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0313` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0314` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0315` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0316` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0320` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0337` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0338` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0339` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0340` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0341` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0342` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0343` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0344` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0345` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0346` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0347` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0348` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0349` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0350` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0351` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0352` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0353` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0354` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0355` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0356` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0357` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0358` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0359` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0360` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0361` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0362` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0363` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0364` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0365` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0366` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0367` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0368` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0369` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0370` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0371` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0372` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0373` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0374` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0375` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0376` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0377` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0378` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0406` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0407` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0408` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0409` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0410` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0411` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0412` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0413` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0414` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0415` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0416` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0417` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0418` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0419` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0420` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0421` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0422` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0423` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0424` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0425` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0426` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0427` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0428` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0429` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0430` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0431` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0432` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0435` — `DEFERRED-FUTURE-SCOPE` — MANUALLY-BOUND-NONPROSE-CONSTRAINT
- `COV-615A3-0436` — `DEFERRED-FUTURE-SCOPE` — MANUALLY-BOUND-NONPROSE-CONSTRAINT
- `COV-615A3-0440` — `DEFERRED-FUTURE-SCOPE` — MANUALLY-BOUND-NONPROSE-CONSTRAINT
- `COV-615A3-0441` — `DEFERRED-FUTURE-SCOPE` — MANUALLY-BOUND-NONPROSE-CONSTRAINT
- `COV-6655-0008` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0033` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0044` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0055` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0056` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0057` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0058` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0059` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0060` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0061` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0066` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0067` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0068` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0069` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0070` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0072` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0073` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0074` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0075` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0076` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0077` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0078` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT

# 中文版

本文件由 `configs/requirements/arinc_615a3_m1_crs.json` 生成；请勿手工编辑。

## 候选状态

- 处置：`ADOPT`
- RG0：`PENDING-EXTERNAL-INDEPENDENT-REVIEW`
- RG1：`PENDING-EXTERNAL-INDEPENDENT-REVIEW`
- 正式批准：`EXTERNAL-JOINT-CONDITION-NOT-YET-SATISFIED`
- 本数据包不建立 Project Configuration 或协议符合性。

## 清单

- 覆盖行：523
- CRS 项：300
- 依赖：4
- 缺口：1
- 覆盖指纹：`f4f885b52a6b7f7597abffd775bc8aa1ef681c34adf9940ec3b5fed3ff26af50`
- 需求指纹：`3eb61c6f5db277b3273e8d2436a85db9b99ce142e66a80c0da99b9cd496dd8eb`

## 适用性

- `APPLICABLE-BASE`：41
- `APPLICABLE-SUPPORTING`：237
- `BLOCKED-BY-DEPENDENCY`：22

## 来源模态

- `FIGURE-CONSTRAINT`：4
- `MAY`：76
- `MUST`：18
- `SHOULD`：200
- `TABLE-CONSTRAINT`：2

## 符合性效果

- `OPTIONAL`：76
- `REQUIRED`：224

## 开放依赖与缺口

- `DEP-ARINC-645` — OPEN-DEPENDENCY：完整性与命名算法来源仍未取得。
- `DEP-ARINC-6655` — REGISTERED-SUPPORTING-SOURCE：有界数据格式调查，不构成版次替代。
- `DEP-IP-UDP-664` — OPEN-DEPENDENCY：IP、UDP 与 ARINC 664 网络语义仍需受控来源闭合。
- `DEP-RFC-TFTP` — OPEN-DEPENDENCY：TFTP 基础及选项 RFC 的身份与适用性仍开放。
- `GAP-ARINC-645` — NOT-ESTABLISHED：CRC、校验值、命名及完整完整性验证仍受阻。

## CRS 项

| ID | 来源 | 模态／效果 | 适用性 | 评审释义 | 依赖／缺口 |
|---|---|---|---|---|---|
| `CRS-615A3-0001` | `ARINC-615A-3 1.1 p.1` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0002` | `ARINC-615A-3 1.3 p.2` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0003` | `ARINC-615A-3 1.3 p.2` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子transport规则。 | — |
| `CRS-615A3-0004` | `ARINC-615A-3 1.3 p.2` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子protocol behavior规则。 | — |
| `CRS-615A3-0005` | `ARINC-615A-3 1.3 p.2` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子protocol behavior规则。 | — |
| `CRS-615A3-0006` | `ARINC-615A-3 1.3 p.2` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0007` | `ARINC-615A-3 1.3 p.2` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子protocol behavior规则。 | — |
| `CRS-615A3-0008` | `ARINC-615A-3 1.3 p.2` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 7 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0009` | `ARINC-615A-3 1.3 p.2` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 8 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0010` | `ARINC-615A-3 1.3 p.2` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 9 项原子protocol behavior规则。 | — |
| `CRS-615A3-0011` | `ARINC-615A-3 1.4.1 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | — |
| `CRS-615A3-0012` | `ARINC-615A-3 1.4.1 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0013` | `ARINC-615A-3 1.4.1 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0014` | `ARINC-615A-3 1.4.1 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子human interface规则。 | — |
| `CRS-615A3-0015` | `ARINC-615A-3 1.4.1 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子data format规则。 | DEP-ARINC-6655, DEP-IP-UDP-664 |
| `CRS-615A3-0016` | `ARINC-615A-3 1.4.1 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.1 中治理 STATUS 的第 6 项原子error status规则。 | — |
| `CRS-615A3-0017` | `ARINC-615A-3 1.4.3 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | — |
| `CRS-615A3-0018` | `ARINC-615A-3 1.4.3 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | — |
| `CRS-615A3-0019` | `ARINC-615A-3 1.4.3 p.4` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子transport规则。 | — |
| `CRS-615A3-0020` | `ARINC-615A-3 1.4.3 p.4` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.3 中治理 STATUS 的第 4 项原子error status规则。 | — |
| `CRS-615A3-0021` | `ARINC-615A-3 1.4.3 p.4` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0022` | `ARINC-615A-3 1.4.3 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子human interface规则。 | — |
| `CRS-615A3-0023` | `ARINC-615A-3 1.4.3 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 7 项原子transport规则。 | — |
| `CRS-615A3-0024` | `ARINC-615A-3 1.4.3 p.4` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 8 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0025` | `ARINC-615A-3 1.4.3 p.4` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 9 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0026` | `ARINC-615A-3 1.4.3 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 10 项原子transport规则。 | — |
| `CRS-615A3-0027` | `ARINC-615A-3 1.4.3 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 11 项原子protocol behavior规则。 | — |
| `CRS-615A3-0028` | `ARINC-615A-3 1.4.3 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 12 项原子transport规则。 | — |
| `CRS-615A3-0029` | `ARINC-615A-3 1.8 p.5` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.8 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子data format规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0030` | `ARINC-615A-3 1.8 p.5` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.8 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0031` | `ARINC-615A-3 1.8 p.5` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.8 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0032` | `ARINC-615A-3 1.8 p.5` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.8 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子transport规则。 | — |
| `CRS-615A3-0033` | `ARINC-615A-3 1.8 p.5` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.8 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子transport规则。 | DEP-ARINC-6655, DEP-IP-UDP-664 |
| `CRS-615A3-0034` | `ARINC-615A-3 1.8 p.5` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.8 中治理 FIND 的第 6 项原子protocol behavior规则。 | — |
| `CRS-615A3-0035` | `ARINC-615A-3 1.8 p.5` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.8 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 7 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0036` | `ARINC-615A-3 1.8 p.5` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.8 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 8 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0037` | `ARINC-615A-3 1.10 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 SCOPE，执行条款 1.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | — |
| `CRS-615A3-0038` | `ARINC-615A-3 5.2 p.22` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.2 中治理 FILE-NAME 的第 1 项原子data format规则。 | — |
| `CRS-615A3-0039` | `ARINC-615A-3 5.2 p.22` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子transport规则。 | DEP-ARINC-6655 |
| `CRS-615A3-0040` | `ARINC-615A-3 5.3.1 p.23` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.1 中治理 FIND 的第 1 项原子data format规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0041` | `ARINC-615A-3 5.3.2 p.24` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0042` | `ARINC-615A-3 5.3.2.3.2 p.25` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.2 中治理 TFTP-OPTION 的第 1 项原子data format规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0043` | `ARINC-615A-3 5.3.2.3.2 p.25` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | — |
| `CRS-615A3-0044` | `ARINC-615A-3 5.3.2.3.2 p.25` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.2 中治理 ERROR 的第 3 项原子error status规则。 | — |
| `CRS-615A3-0045` | `ARINC-615A-3 5.3.2.3.2 p.25` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.2 中治理 TFTP-OPTION 的第 4 项原子transport规则。 | DEP-IP-UDP-664, DEP-RFC-TFTP |
| `CRS-615A3-0046` | `ARINC-615A-3 5.3.2.3.2 p.25` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子data format规则。 | — |
| `CRS-615A3-0047` | `ARINC-615A-3 5.3.2.3.2 p.25` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.2 中治理 PORT 的第 6 项原子data format规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0048` | `ARINC-615A-3 5.3.2.3.4 p.26` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.4 中治理 ERROR 的第 1 项原子error status规则。 | — |
| `CRS-615A3-0049` | `ARINC-615A-3 5.3.2.3.4 p.26` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.4 中治理 ERROR 的第 2 项原子data format规则。 | — |
| `CRS-615A3-0050` | `ARINC-615A-3 5.3.2.3.4 p.26` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.4 中治理 ERROR 的第 3 项原子data format规则。 | — |
| `CRS-615A3-0051` | `ARINC-615A-3 5.3.2.3.4 p.26` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.4 中治理 WAIT / ERROR 的第 4 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0052` | `ARINC-615A-3 5.3.2.3.4 p.26` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子transport规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0053` | `ARINC-615A-3 5.3.2.3.4 p.26` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.4 中治理 WAIT / ABORT 的第 6 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0054` | `ARINC-615A-3 5.3.2.3.8.1 p.28` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0055` | `ARINC-615A-3 5.3.2.3.8.1 p.28` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0056` | `ARINC-615A-3 5.3.2.3.8.1 p.28` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.1 中治理 BLOCK-SIZE 的第 3 项原子transport规则。 | DEP-IP-UDP-664, DEP-RFC-TFTP |
| `CRS-615A3-0057` | `ARINC-615A-3 5.3.2.3.8.1 p.28` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子protocol behavior规则。 | — |
| `CRS-615A3-0058` | `ARINC-615A-3 5.3.2.3.8.5 p.29` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 BLOCK-SIZE 的第 1 项原子transport规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0059` | `ARINC-615A-3 5.3.2.3.8.5 p.29` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 BLOCK-SIZE / TRANSFER-SIZE 的第 2 项原子data format规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0060` | `ARINC-615A-3 5.3.2.3.8.5 p.29` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 TRANSFER-SIZE / ERROR 的第 3 项原子error status规则。 | — |
| `CRS-615A3-0061` | `ARINC-615A-3 5.3.2.3.8.5 p.29` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 TRANSFER-SIZE / TIMEOUT 的第 4 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0062` | `ARINC-615A-3 5.3.2.3.8.5 p.29` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 TIMEOUT 的第 5 项原子timing规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0063` | `ARINC-615A-3 5.3.2.3.8.5 p.29` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 TIMEOUT / PART-NUMBER 的第 6 项原子timing规则。 | — |
| `CRS-615A3-0064` | `ARINC-615A-3 5.3.2.3.8.5 p.29` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 TIMEOUT / CHECKSUM 的第 7 项原子timing规则。 | GAP-ARINC-645 |
| `CRS-615A3-0065` | `ARINC-615A-3 5.3.2.3.8.5 p.30` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 CHECKSUM / CRC / FILE-NAME / HEADER-FILE 的第 8 项原子data format规则。 | DEP-ARINC-6655, DEP-RFC-TFTP, GAP-ARINC-645 |
| `CRS-615A3-0066` | `ARINC-615A-3 5.3.2.3.8.5 p.30` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 CRC 的第 9 项原子data format规则。 | GAP-ARINC-645 |
| `CRS-615A3-0067` | `ARINC-615A-3 5.3.2.3.8.5 p.30` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 TFTP-OPTION / CHECKSUM 的第 10 项原子transport规则。 | DEP-RFC-TFTP, GAP-ARINC-645 |
| `CRS-615A3-0068` | `ARINC-615A-3 5.3.2.3.8.5 p.31` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 11 项原子data format规则。 | — |
| `CRS-615A3-0069` | `ARINC-615A-3 5.3.2.3.8.5 p.31` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 CHECKSUM / CRC / FILE-NAME / HEADER-FILE 的第 12 项原子data format规则。 | DEP-ARINC-6655, GAP-ARINC-645 |
| `CRS-615A3-0070` | `ARINC-615A-3 5.3.2.3.8.5 p.31` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 DOWNLOAD 的第 13 项原子data format规则。 | — |
| `CRS-615A3-0071` | `ARINC-615A-3 5.3.2.3.8.5 p.31` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 CHECKSUM 的第 14 项原子transport规则。 | GAP-ARINC-645 |
| `CRS-615A3-0072` | `ARINC-615A-3 5.3.2.3.8.5 p.31` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 CHECKSUM / DATA-FILE / ERROR 的第 15 项原子data format规则。 | DEP-RFC-TFTP, GAP-ARINC-645 |
| `CRS-615A3-0073` | `ARINC-615A-3 5.3.2.3.8.5 p.31` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 CHECKSUM / DOWNLOAD / ERROR 的第 16 项原子data format规则。 | GAP-ARINC-645 |
| `CRS-615A3-0074` | `ARINC-615A-3 5.3.2.3.8.5 p.31` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 CHECKSUM / DOWNLOAD 的第 17 项原子data format规则。 | GAP-ARINC-645 |
| `CRS-615A3-0075` | `ARINC-615A-3 5.3.2.3.8.5 p.31` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.8.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 18 项原子protocol behavior规则。 | — |
| `CRS-615A3-0076` | `ARINC-615A-3 5.4.1 p.33` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0077` | `ARINC-615A-3 5.4.1 p.33` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0078` | `ARINC-615A-3 5.4.1 p.33` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子data format规则。 | — |
| `CRS-615A3-0079` | `ARINC-615A-3 5.4.1 p.34` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子protocol behavior规则。 | — |
| `CRS-615A3-0080` | `ARINC-615A-3 5.4.1 p.34` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.4.1 中治理 ABORT 的第 5 项原子error status规则。 | — |
| `CRS-615A3-0081` | `ARINC-615A-3 5.4.1 p.34` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子protocol behavior规则。 | — |
| `CRS-615A3-0082` | `ARINC-615A-3 5.4.1 p.34` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.4.1 中治理 UPLOAD / DOWNLOAD / FIND 的第 7 项原子data format规则。 | — |
| `CRS-615A3-0083` | `ARINC-615A-3 5.4.1 p.34` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.4.1 中治理 FIND 的第 8 项原子protocol behavior规则。 | — |
| `CRS-615A3-0084` | `ARINC-615A-3 5.4.1 p.34` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.4.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 9 项原子data format规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0085` | `ARINC-615A-3 5.4.1 p.34` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.4.1 中治理 STATUS 的第 10 项原子data format规则。 | — |
| `CRS-615A3-0086` | `ARINC-615A-3 5.4.3 p.35` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | — |
| `CRS-615A3-0087` | `ARINC-615A-3 5.4.3 p.35` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | — |
| `CRS-615A3-0088` | `ARINC-615A-3 5.4.3 p.35` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子protocol behavior规则。 | — |
| `CRS-615A3-0089` | `ARINC-615A-3 5.4.3 p.35` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3 中治理 WAIT / STATUS 的第 4 项原子timing规则。 | — |
| `CRS-615A3-0090` | `ARINC-615A-3 5.4.3 p.35` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3 中治理 TFTP-OPTION 的第 5 项原子transport规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0091` | `ARINC-615A-3 5.4.3 p.35` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3 中治理 TFTP-OPTION 的第 6 项原子transport规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0092` | `ARINC-615A-3 5.4.3 p.35` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3 中治理 UPLOAD 的第 7 项原子data format规则。 | GAP-ARINC-645 |
| `CRS-615A3-0093` | `ARINC-615A-3 5.4.3.1 p.36` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | — |
| `CRS-615A3-0094` | `ARINC-615A-3 5.4.3.1 p.36` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3.1 中治理 STATUS 的第 2 项原子error status规则。 | — |
| `CRS-615A3-0095` | `ARINC-615A-3 5.4.3.1 p.36` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3.1 中治理 TFTP-OPTION 的第 3 项原子transport规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0096` | `ARINC-615A-3 5.4.3.1 p.36` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3.1 中治理 FILE-NAME 的第 4 项原子data format规则。 | GAP-ARINC-645 |
| `CRS-615A3-0097` | `ARINC-615A-3 5.4.3.1 p.36` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3.1 中治理 TFTP-OPTION 的第 5 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0098` | `ARINC-615A-3 5.4.3.1 p.36` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3.1 中治理 PART-NUMBER / HEADER-FILE / DATA-FILE 的第 6 项原子data format规则。 | — |
| `CRS-615A3-0099` | `ARINC-615A-3 5.4.3.2 p.37` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | GAP-ARINC-645 |
| `CRS-615A3-0100` | `ARINC-615A-3 5.4.3.2 p.37` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3.2 中治理 CRC 的第 2 项原子data format规则。 | GAP-ARINC-645 |
| `CRS-615A3-0101` | `ARINC-615A-3 5.4.3.2 p.37` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3.2 中治理 CRC / PART-NUMBER 的第 3 项原子data format规则。 | GAP-ARINC-645 |
| `CRS-615A3-0102` | `ARINC-615A-3 5.4.3.2 p.37` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子data format规则。 | — |
| `CRS-615A3-0103` | `ARINC-615A-3 5.4.3.2 p.37` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子timing规则。 | — |
| `CRS-615A3-0104` | `ARINC-615A-3 5.4.3.2 p.37` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 5.4.3.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子data format规则。 | — |
| `CRS-615A3-0105` | `ARINC-615A-3 5.4.5.1 p.40` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.4.5.1 中治理 DOWNLOAD 的第 1 项原子data format规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0106` | `ARINC-615A-3 5.4.5.1 p.40` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.4.5.1 中治理 DOWNLOAD 的第 2 项原子human interface规则。 | — |
| `CRS-615A3-0107` | `ARINC-615A-3 5.4.5.1 p.40` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.4.5.1 中治理 DOWNLOAD / ERROR 的第 3 项原子error status规则。 | — |
| `CRS-615A3-0108` | `ARINC-615A-3 5.4.5.1 p.40` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.4.5.1 中治理 DOWNLOAD 的第 4 项原子timing规则。 | — |
| `CRS-615A3-0109` | `ARINC-615A-3 5.4.5.1 p.40` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.4.5.1 中治理 DOWNLOAD 的第 5 项原子timing规则。 | — |
| `CRS-615A3-0110` | `ARINC-615A-3 5.4.5.2 p.41` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.4.5.2 中治理 ABORT / STATUS 的第 1 项原子data format规则。 | — |
| `CRS-615A3-0111` | `ARINC-615A-3 6.2.8.2 p.45` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.2.8.2 中治理 WAIT 的第 1 项原子timing规则。 | DEP-IP-UDP-664, DEP-RFC-TFTP |
| `CRS-615A3-0112` | `ARINC-615A-3 6.3.1 p.51` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.3.1 中治理 TIMEOUT 的第 1 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0113` | `ARINC-615A-3 6.3.1 p.51` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.3.1 中治理 TIMEOUT 的第 2 项原子timing规则。 | — |
| `CRS-615A3-0114` | `ARINC-615A-3 6.3.1 p.51` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.3.1 中治理 STATUS / TIMEOUT 的第 3 项原子timing规则。 | — |
| `CRS-615A3-0115` | `ARINC-615A-3 6.3.1 p.51` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.3.1 中治理 ABORT / STATUS / TIMEOUT / INFORMATION 的第 4 项原子timing规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0116` | `ARINC-615A-3 6.3.1 p.51` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.3.1 中治理 STATUS / TIMEOUT 的第 5 项原子timing规则。 | — |
| `CRS-615A3-0117` | `ARINC-615A-3 6.3.1 p.51` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.3.1 中治理 STATUS / TIMEOUT 的第 6 项原子timing规则。 | — |
| `CRS-615A3-0118` | `ARINC-615A-3 6.3.1 p.52` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.3.1 中治理 WAIT 的第 7 项原子timing规则。 | — |
| `CRS-615A3-0119` | `ARINC-615A-3 6.3.1 p.52` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.3.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 8 项原子timing规则。 | — |
| `CRS-615A3-0120` | `ARINC-615A-3 6.3.1 p.52` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.3.1 中治理 ABORT / STATUS / UPLOAD / DOWNLOAD 的第 9 项原子timing规则。 | — |
| `CRS-615A3-0121` | `ARINC-615A-3 5.3.2.3.4 p.55` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.4 中治理 TIMEOUT 的第 7 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0122` | `ARINC-615A-3 5.3.2.3.4 p.55` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.4 中治理 TIMEOUT 的第 8 项原子timing规则。 | — |
| `CRS-615A3-0123` | `ARINC-615A-3 5.3.2.3.4 p.55` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.4 中治理 STATUS / TIMEOUT 的第 9 项原子timing规则。 | — |
| `CRS-615A3-0124` | `ARINC-615A-3 5.3.2.3.4 p.55` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.4 中治理 ABORT / STATUS / TIMEOUT / ERROR 的第 10 项原子timing规则。 | DEP-IP-UDP-664, DEP-RFC-TFTP |
| `CRS-615A3-0125` | `ARINC-615A-3 5.3.2.3.4 p.55` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.4 中治理 HEADER-FILE / DATA-FILE / UPLOAD 的第 11 项原子data format规则。 | — |
| `CRS-615A3-0126` | `ARINC-615A-3 5.3.2.3.4 p.56` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.4 中治理 WAIT 的第 12 项原子timing规则。 | — |
| `CRS-615A3-0127` | `ARINC-615A-3 5.3.2.3.4 p.56` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 13 项原子timing规则。 | — |
| `CRS-615A3-0128` | `ARINC-615A-3 5.3.2.3.4 p.56` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.4 中治理 ABORT / STATUS / UPLOAD / DOWNLOAD 的第 14 项原子timing规则。 | — |
| `CRS-615A3-0129` | `ARINC-615A-3 5.3.2.3.4 p.56` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 5.3.2.3.4 中治理 STATUS / CHECKSUM / CRC / DATA-FILE 的第 15 项原子data format规则。 | GAP-ARINC-645 |
| `CRS-615A3-0130` | `ARINC-615A-3 6.3.5 p.64` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 6.3.5 中治理 TIMEOUT 的第 1 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0131` | `ARINC-615A-3 6.3.5 p.64` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 6.3.5 中治理 ABORT / STATUS 的第 2 项原子data format规则。 | — |
| `CRS-615A3-0132` | `ARINC-615A-3 6.3.5 p.64` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 6.3.5 中治理 ABORT / STATUS / ERROR 的第 3 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0133` | `ARINC-615A-3 6.3.5 p.64` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 6.3.5 中治理 ABORT / STATUS 的第 4 项原子data format规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0134` | `ARINC-615A-3 6.4 p.65` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 6.4 中治理 PROTOCOL-VERSION 的第 1 项原子data format规则。 | — |
| `CRS-615A3-0135` | `ARINC-615A-3 6.4 p.65` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 6.4 中治理 PROTOCOL-VERSION 的第 2 项原子protocol behavior规则。 | — |
| `CRS-615A3-0136` | `ARINC-615A-3 6.4 p.65` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 6.4 中治理 PROTOCOL-VERSION 的第 3 项原子data format规则。 | — |
| `CRS-615A3-0137` | `ARINC-615A-3 6.4 p.65` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 6.4 中治理 PROTOCOL-VERSION 的第 4 项原子data format规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0138` | `ARINC-615A-3 6.4 p.65` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 6.4 中治理 PROTOCOL-VERSION / ABORT 的第 5 项原子error status规则。 | — |
| `CRS-615A3-0139` | `ARINC-615A-3 6.4 p.65` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 6.4 中治理 PROTOCOL-VERSION / ABORT / STATUS 的第 6 项原子data format规则。 | — |
| `CRS-615A3-0140` | `ARINC-615A-3 6.4 p.65` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 6.4 中治理 PROTOCOL-VERSION 的第 7 项原子data format规则。 | — |
| `CRS-615A3-0141` | `ARINC-615A-3 6.4 p.65` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 6.4 中治理 PART-NUMBER / ZERO-TERMINATION 的第 8 项原子data format规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0142` | `ARINC-615A-3 6.4 p.65` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 6.4 中治理 ZERO-TERMINATION 的第 9 项原子data format规则。 | — |
| `CRS-615A3-0143` | `ARINC-615A-3 6.4 p.66` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 6.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 10 项原子data format规则。 | — |
| `CRS-615A3-0144` | `ARINC-615A-3 6.4.2 p.68` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | — |
| `CRS-615A3-0145` | `ARINC-615A-3 6.4.2 p.68` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.2 中治理 PROTOCOL-VERSION / PART-NUMBER / ZERO-TERMINATION 的第 2 项原子data format规则。 | — |
| `CRS-615A3-0146` | `ARINC-615A-3 6.4.2 p.69` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.2 中治理 ZERO-TERMINATION 的第 3 项原子protocol behavior规则。 | — |
| `CRS-615A3-0147` | `ARINC-615A-3 6.4.2 p.69` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.2 中治理 ZERO-TERMINATION 的第 4 项原子protocol behavior规则。 | — |
| `CRS-615A3-0148` | `ARINC-615A-3 6.4.3 p.70` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | — |
| `CRS-615A3-0149` | `ARINC-615A-3 6.4.3 p.70` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.3 中治理 PROTOCOL-VERSION / STATUS / INFORMATION / ZERO-TERMINATION 的第 2 项原子timing规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0150` | `ARINC-615A-3 6.4.4 p.72` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.4 中治理 STATUS 的第 1 项原子data format规则。 | — |
| `CRS-615A3-0151` | `ARINC-615A-3 6.4.4 p.72` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子timing规则。 | — |
| `CRS-615A3-0152` | `ARINC-615A-3 6.4.4 p.72` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.4 中治理 STATUS 的第 3 项原子timing规则。 | — |
| `CRS-615A3-0153` | `ARINC-615A-3 6.4.4 p.72` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.4 中治理 STATUS 的第 4 项原子data format规则。 | — |
| `CRS-615A3-0154` | `ARINC-615A-3 6.4.4 p.72` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子protocol behavior规则。 | — |
| `CRS-615A3-0155` | `ARINC-615A-3 6.4.4 p.72` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.4 中治理 PROTOCOL-VERSION / FILE-NAME / PART-NUMBER / HEADER-FILE 的第 6 项原子data format规则。 | — |
| `CRS-615A3-0156` | `ARINC-615A-3 6.4.4 p.73` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.4 中治理 HEADER-FILE 的第 7 项原子data format规则。 | — |
| `CRS-615A3-0157` | `ARINC-615A-3 6.4.4 p.73` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.4 中治理 ZERO-TERMINATION 的第 8 项原子protocol behavior规则。 | — |
| `CRS-615A3-0158` | `ARINC-615A-3 6.4.4 p.73` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 9 项原子protocol behavior规则。 | — |
| `CRS-615A3-0159` | `ARINC-615A-3 6.4.5 p.75` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.5 中治理 STATUS 的第 1 项原子data format规则。 | — |
| `CRS-615A3-0160` | `ARINC-615A-3 6.4.5 p.75` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | — |
| `CRS-615A3-0161` | `ARINC-615A-3 6.4.5 p.75` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.5 中治理 ZERO-TERMINATION 的第 3 项原子protocol behavior规则。 | — |
| `CRS-615A3-0162` | `ARINC-615A-3 6.4.5 p.76` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.5 中治理 STATUS 的第 4 项原子data format规则。 | — |
| `CRS-615A3-0163` | `ARINC-615A-3 6.4.5 p.76` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子timing规则。 | — |
| `CRS-615A3-0164` | `ARINC-615A-3 6.4.5 p.76` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.5 中治理 STATUS 的第 6 项原子timing规则。 | — |
| `CRS-615A3-0165` | `ARINC-615A-3 6.4.5 p.76` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.5 中治理 HEADER-FILE 的第 7 项原子data format规则。 | — |
| `CRS-615A3-0166` | `ARINC-615A-3 6.4.5 p.76` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.5 中治理 ZERO-TERMINATION 的第 8 项原子protocol behavior规则。 | — |
| `CRS-615A3-0167` | `ARINC-615A-3 6.4.5 p.77` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 对 UPLOAD，执行条款 6.4.5 中治理 ZERO-TERMINATION 的第 9 项原子protocol behavior规则。 | — |
| `CRS-615A3-0168` | `ARINC-615A-3 6.4.10 p.82` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 STATUS 的第 1 项原子data format规则。 | — |
| `CRS-615A3-0169` | `ARINC-615A-3 6.4.10 p.82` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | — |
| `CRS-615A3-0170` | `ARINC-615A-3 6.4.10 p.82` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 ZERO-TERMINATION 的第 3 项原子protocol behavior规则。 | — |
| `CRS-615A3-0171` | `ARINC-615A-3 6.4.10 p.84` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子protocol behavior规则。 | — |
| `CRS-615A3-0172` | `ARINC-615A-3 6.4.10 p.84` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 PROTOCOL-VERSION / FILE-NAME / DOWNLOAD / ZERO-TERMINATION 的第 5 项原子data format规则。 | — |
| `CRS-615A3-0173` | `ARINC-615A-3 6.4.10 p.84` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 STATUS / ZERO-TERMINATION 的第 6 项原子data format规则。 | — |
| `CRS-615A3-0174` | `ARINC-615A-3 6.4.10 p.85` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 STATUS / UPLOAD / DOWNLOAD 的第 7 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0175` | `ARINC-615A-3 6.4.10 p.85` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 ABORT / STATUS / FILE-NAME / PART-NUMBER 的第 8 项原子data format规则。 | — |
| `CRS-615A3-0176` | `ARINC-615A-3 6.4.10 p.87` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 9 项原子transport规则。 | — |
| `CRS-615A3-0177` | `ARINC-615A-3 6.4.10 p.87` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 10 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0178` | `ARINC-615A-3 6.4.10 p.87` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 11 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0179` | `ARINC-615A-3 6.4.10 p.87` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 12 项原子transport规则。 | DEP-IP-UDP-664 |
| `CRS-615A3-0180` | `ARINC-615A-3 6.4.10 p.87` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 13 项原子protocol behavior规则。 | — |
| `CRS-615A3-0181` | `ARINC-615A-3 6.4.10 p.87` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 14 项原子protocol behavior规则。 | — |
| `CRS-615A3-0182` | `ARINC-615A-3 6.4.10 p.87` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 15 项原子protocol behavior规则。 | — |
| `CRS-615A3-0183` | `ARINC-615A-3 6.4.10 p.87` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 16 项原子protocol behavior规则。 | — |
| `CRS-615A3-0184` | `ARINC-615A-3 6.4.10 p.87` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 17 项原子protocol behavior规则。 | — |
| `CRS-615A3-0185` | `ARINC-615A-3 6.4.10 p.87` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 18 项原子protocol behavior规则。 | — |
| `CRS-615A3-0186` | `ARINC-615A-3 6.4.10 p.87` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 INFORMATION，执行条款 6.4.10 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 19 项原子protocol behavior规则。 | — |
| `CRS-615A3-0187` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-1 中治理 TIMEOUT / RETRY 的第 1 项原子timing规则。 | — |
| `CRS-615A3-0188` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-1 中治理 TIMEOUT 的第 2 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0189` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-1 中治理 TIMEOUT / ERROR 的第 3 项原子timing规则。 | — |
| `CRS-615A3-0190` | `ARINC-615A-3 4-1 p.99` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-1 中治理 TIMEOUT / RETRY / CRC / ERROR 的第 4 项原子timing规则。 | DEP-RFC-TFTP, GAP-ARINC-645 |
| `CRS-615A3-0191` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-1 中治理 RETRY / ERROR 的第 5 项原子retry policy规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0192` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-1 中治理 ERROR 的第 6 项原子error status规则。 | — |
| `CRS-615A3-0193` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-1 中治理 RETRY / UPLOAD / DOWNLOAD / ERROR 的第 7 项原子retry policy规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0194` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-1 中治理 RETRY / ERROR 的第 8 项原子retry policy规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0195` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-1 中治理 ERROR 的第 9 项原子error status规则。 | — |
| `CRS-615A3-0196` | `ARINC-615A-3 4-1 p.99` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-1 中治理 TIMEOUT 的第 10 项原子timing规则。 | — |
| `CRS-615A3-0197` | `ARINC-615A-3 4-3 p.100` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-3 中治理 TIMEOUT 的第 1 项原子timing规则。 | — |
| `CRS-615A3-0198` | `ARINC-615A-3 4-3 p.100` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子transport规则。 | DEP-IP-UDP-664, DEP-RFC-TFTP |
| `CRS-615A3-0199` | `ARINC-615A-3 4-3 p.100` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子transport规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0200` | `ARINC-615A-3 4-3 p.101` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-3 中治理 RETRY / ERROR 的第 4 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0201` | `ARINC-615A-3 4-3 p.101` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-3 中治理 RETRY 的第 5 项原子retry policy规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0202` | `ARINC-615A-3 4-4 p.102` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-4 中治理 TIMEOUT / RETRY 的第 1 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0203` | `ARINC-615A-3 4-4 p.102` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-4 中治理 TIMEOUT 的第 2 项原子timing规则。 | DEP-IP-UDP-664, DEP-RFC-TFTP |
| `CRS-615A3-0204` | `ARINC-615A-3 4-4 p.102` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-4 中治理 TIMEOUT 的第 3 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0205` | `ARINC-615A-3 4-4 p.102` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-4 中治理 TIMEOUT 的第 4 项原子timing规则。 | — |
| `CRS-615A3-0206` | `ARINC-615A-3 4-4 p.102` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-4 中治理 STATUS 的第 5 项原子data format规则。 | — |
| `CRS-615A3-0207` | `ARINC-615A-3 4-4 p.102` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-4 中治理 TIMEOUT 的第 6 项原子timing规则。 | — |
| `CRS-615A3-0208` | `ARINC-615A-3 4-4 p.102` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-4 中治理 TIMEOUT 的第 7 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0209` | `ARINC-615A-3 4-4 p.103` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-4 中治理 RETRY / ERROR 的第 8 项原子timing规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0210` | `ARINC-615A-3 4-4 p.104` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-4 中治理 TIMEOUT / RETRY 的第 9 项原子timing规则。 | — |
| `CRS-615A3-0211` | `ARINC-615A-3 4-4 p.104` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-4 中治理 ERROR 的第 10 项原子data format规则。 | DEP-RFC-TFTP |
| `CRS-615A3-0212` | `ARINC-615A-3 4-4 p.106` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 11 项原子protocol behavior规则。 | — |
| `CRS-615A3-0213` | `ARINC-615A-3 4-4 p.106` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 COMMON，执行条款 4-4 中治理 UPLOAD / DOWNLOAD / ERROR 的第 12 项原子error status规则。 | — |
| `CRS-615A3-0214` | `ARINC-615A-3 6.1 p.42` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 表 6-1 固定 Information 消息在 DLA 与 DLP 间的方向。 | — |
| `CRS-615A3-0215` | `ARINC-615A-3 6.1 p.42` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 表 6-1 固定 Upload 消息在 DLA 与 DLP 间的方向。 | — |
| `CRS-615A3-0216` | `ARINC-615A-3 6.3.1 p.50` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Information 遵循图示初始化、LCI、LCL、状态及完成顺序。 | DEP-RFC-TFTP |
| `CRS-615A3-0217` | `ARINC-615A-3 6.3.2 p.53` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Upload 初始化及清单传输遵循序列图第一段。 | DEP-RFC-TFTP |
| `CRS-615A3-0218` | `ARINC-615A-3 6.3.2 p.54` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Upload 文件传输、文件不可用处理及完成状态遵循序列图第二段。 | DEP-RFC-TFTP |
| `CRS-615A3-0219` | `ARINC-615A-3 6.3.5 p.63` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 中断遵循图示中止请求、停止、确认及终止顺序。 | DEP-RFC-TFTP |
| `CRS-6655-0001` | `ARINC-665-5 1.3.3 p.1` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 1.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0002` | `ARINC-665-5 1.3.3 p.1` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 1.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子transport规则。 | DEP-ARINC-6655 |
| `CRS-6655-0003` | `ARINC-665-5 1.3.3 p.1` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 1.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0004` | `ARINC-665-5 1.3.3 p.1` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 1.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0005` | `ARINC-665-5 1.3.3 p.1` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 1.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0006` | `ARINC-665-5 1.3.3 p.1` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 1.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0007` | `ARINC-665-5 1.4.2 p.2` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 1.4.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0008` | `ARINC-665-5 1.4.2 p.2` | `MAY` / `OPTIONAL` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 1.4.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0009` | `ARINC-665-5 1.4.2 p.2` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 1.4.2 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0010` | `ARINC-665-5 1.4.4 p.3` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 1.4.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0011` | `ARINC-665-5 1.4.4 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 1.4.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0012` | `ARINC-665-5 1.4.4 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 1.4.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0013` | `ARINC-665-5 1.4.4 p.3` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 1.4.4 中治理 PART-NUMBER / HEADER-FILE 的第 4 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0014` | `ARINC-665-5 1.5 p.4` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 1.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | DEP-ARINC-6655 |
| `CRS-6655-0015` | `ARINC-665-5 1.5 p.4` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 1.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0016` | `ARINC-665-5 1.5 p.4` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 1.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0017` | `ARINC-665-5 1.5 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 1.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0018` | `ARINC-665-5 1.5 p.4` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 1.5 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子transport规则。 | DEP-ARINC-6655 |
| `CRS-6655-0019` | `ARINC-665-5 2.1.1 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.1.1 中治理 PART-NUMBER 的第 1 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0020` | `ARINC-665-5 2.1.1 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.1.1 中治理 PART-NUMBER 的第 2 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0021` | `ARINC-665-5 2.1.1 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.1.1 中治理 PART-NUMBER 的第 3 项原子timing规则。 | DEP-ARINC-6655 |
| `CRS-6655-0022` | `ARINC-665-5 2.1.1 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.1.1 中治理 PART-NUMBER / FIND 的第 4 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0023` | `ARINC-665-5 2.1.1 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.1.1 中治理 PART-NUMBER 的第 5 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0024` | `ARINC-665-5 2.1.1 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.1.1 中治理 PART-NUMBER 的第 6 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0025` | `ARINC-665-5 2.1.1 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.1.1 中治理 PART-NUMBER 的第 7 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0026` | `ARINC-665-5 2.1.1 p.6` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.1.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 8 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0027` | `ARINC-665-5 2.1.1 p.6` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.1.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 9 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0028` | `ARINC-665-5 2.1.4 p.7` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.1.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子transport规则。 | DEP-ARINC-6655 |
| `CRS-6655-0029` | `ARINC-665-5 2.1.4 p.7` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.1.4 中治理 PART-NUMBER 的第 2 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0030` | `ARINC-665-5 2.1.4 p.7` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.1.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0031` | `ARINC-665-5 2.1.4 p.7` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.1.4 中治理 PART-NUMBER / ERROR 的第 4 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0032` | `ARINC-665-5 2.1.4 p.7` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.1.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0033` | `ARINC-665-5 2.1.4 p.7` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.1.4 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子transport规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0034` | `ARINC-665-5 2.2.3.1 p.8` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0035` | `ARINC-665-5 2.2.3.1 p.8` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1 中治理 FILE-NAME 的第 2 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0036` | `ARINC-665-5 2.2.3.1 p.8` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1 中治理 FILE-NAME / HEADER-FILE 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0037` | `ARINC-665-5 2.2.3.1 p.8` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1 中治理 HEADER-FILE / DATA-FILE 的第 4 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0038` | `ARINC-665-5 2.2.3.1 p.8` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0039` | `ARINC-665-5 2.2.3.1 p.8` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0040` | `ARINC-665-5 2.2.3.1 p.8` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1 中治理 FILE-NAME / HEADER-FILE / DATA-FILE 的第 7 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0041` | `ARINC-665-5 2.2.3.1.7 p.11` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.7 中治理 UPLOAD / DOWNLOAD 的第 1 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0042` | `ARINC-665-5 2.2.3.1.7 p.11` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.7 中治理 PART-NUMBER / DATA-FILE / DOWNLOAD 的第 2 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0043` | `ARINC-665-5 2.2.3.1.16 p.12` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.16 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0044` | `ARINC-665-5 2.2.3.1.16 p.12` | `MAY` / `OPTIONAL` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.1.16 中治理 PART-NUMBER 的第 2 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0045` | `ARINC-665-5 2.2.3.1.16 p.12` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.16 中治理 PART-NUMBER 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0046` | `ARINC-665-5 2.2.3.1.20 p.13` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.20 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0047` | `ARINC-665-5 2.2.3.1.20 p.13` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.20 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | DEP-ARINC-6655 |
| `CRS-6655-0048` | `ARINC-665-5 2.2.3.1.20 p.13` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.20 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0049` | `ARINC-665-5 2.2.3.1.28 p.14` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.28 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0050` | `ARINC-665-5 2.2.3.1.28 p.14` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.28 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0051` | `ARINC-665-5 2.2.3.1.28 p.14` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.28 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0052` | `ARINC-665-5 2.2.3.1.36 p.15` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.36 中治理 DATA-FILE 的第 1 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0053` | `ARINC-665-5 2.2.3.1.36 p.15` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.36 中治理 DATA-FILE 的第 2 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0054` | `ARINC-665-5 2.2.3.1.36 p.15` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.36 中治理 FILE-NAME / DATA-FILE 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0055` | `ARINC-665-5 2.2.3.1.43 p.16` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.1.43 中治理 CRC / DATA-FILE 的第 1 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0056` | `ARINC-665-5 2.2.3.1.43 p.16` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.1.43 中治理 CRC / DATA-FILE 的第 2 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0057` | `ARINC-665-5 2.2.3.1.43 p.16` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.1.43 中治理 DATA-FILE 的第 3 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0058` | `ARINC-665-5 2.2.3.1.43 p.16` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.1.43 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子protocol behavior规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0059` | `ARINC-665-5 2.2.3.1.43 p.16` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.1.43 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 5 项原子protocol behavior规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0060` | `ARINC-665-5 2.2.3.1.43 p.16` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.1.43 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0061` | `ARINC-665-5 2.2.3.1.43 p.16` | `MAY` / `OPTIONAL` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.1.43 中治理 DATA-FILE 的第 7 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0062` | `ARINC-665-5 2.2.3.1.51 p.17` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.51 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0063` | `ARINC-665-5 2.2.3.1.51 p.17` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.51 中治理 FILE-NAME 的第 2 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0064` | `ARINC-665-5 2.2.3.1.51 p.17` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.51 中治理 PART-NUMBER 的第 3 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0065` | `ARINC-665-5 2.2.3.1.51 p.17` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.51 中治理 PART-NUMBER 的第 4 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0066` | `ARINC-665-5 2.2.3.1.51 p.17` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.1.51 中治理 CRC 的第 5 项原子transport规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0067` | `ARINC-665-5 2.2.3.1.60 p.18` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.1.60 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0068` | `ARINC-665-5 2.2.3.1.60 p.18` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.1.60 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0069` | `ARINC-665-5 2.2.3.1.60 p.18` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.1.60 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0070` | `ARINC-665-5 2.2.3.1.60 p.18` | `MAY` / `OPTIONAL` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.1.60 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 4 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0071` | `ARINC-665-5 2.2.3.1.60 p.18` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.1.60 中治理 HEADER-FILE 的第 5 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0072` | `ARINC-665-5 2.2.3.1.60 p.18` | `MAY` / `OPTIONAL` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.1.60 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 6 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0073` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 1 项原子protocol behavior规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0074` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 2 项原子protocol behavior规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0075` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 3 项原子protocol behavior规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0076` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.3 中治理 CRC / HEADER-FILE / DATA-FILE 的第 4 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0077` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.3 中治理 CRC / HEADER-FILE 的第 5 项原子data format规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0078` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `BLOCKED-BY-DEPENDENCY` | 对 DATA-OBJECT，执行条款 2.2.3.3 中治理 CRC 的第 6 项原子transport规则。 | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-6655-0079` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.3 中治理 DATA-FILE 的第 7 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0080` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 8 项原子data format规则。 | DEP-ARINC-6655 |
| `CRS-6655-0081` | `ARINC-665-5 2.2.3.3 p.19` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对 DATA-OBJECT，执行条款 2.2.3.3 中治理 CLAUSE-SPECIFIC-BEHAVIOR 的第 9 项原子data format规则。 | DEP-ARINC-6655 |

## 非基础范围及未决清单

- `COV-615A3-0038` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0039` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0040` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0041` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0042` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0043` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0044` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0045` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0046` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0047` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0048` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0049` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0050` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0051` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0052` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0053` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0054` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0055` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0056` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0057` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0058` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0059` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0060` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0061` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0062` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0063` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0064` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0065` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0066` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0067` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0068` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0069` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0070` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0071` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0072` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0073` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0074` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0075` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0076` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0077` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0078` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0079` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0080` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0081` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0082` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0083` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0084` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0085` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0086` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0087` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0088` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0089` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0090` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0091` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0092` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0093` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0094` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0095` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0096` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0097` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0098` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0099` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0100` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0101` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0102` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0103` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0104` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0105` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0106` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0107` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0108` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0109` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0110` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0111` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0112` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0113` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0114` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0115` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0116` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0117` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0118` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0119` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0120` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0121` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0122` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0123` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0124` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0125` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0126` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0127` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0128` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0129` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0130` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0131` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0132` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0133` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0134` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0135` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0136` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0137` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0138` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0139` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0140` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0141` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0142` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0143` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0144` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0145` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0146` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0147` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0148` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0187` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0188` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0189` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0190` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0220` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0221` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0222` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0223` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0224` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0225` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0226` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0227` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0228` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0254` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0255` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0256` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0257` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0258` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0259` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0260` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0261` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0262` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0263` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0264` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0265` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0266` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0267` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0306` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0307` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0308` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0309` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0310` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0311` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0312` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0313` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0314` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0315` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0316` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0320` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-DOWNLOAD-M9
- `COV-615A3-0337` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0338` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0339` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0340` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0341` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0342` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0343` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0344` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0345` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0346` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0347` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0348` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0349` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0350` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0351` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0352` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0353` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0354` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0355` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0356` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0357` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0358` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0359` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0360` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0361` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0362` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0363` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0364` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0365` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0366` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0367` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0368` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0369` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0370` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0371` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0372` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0373` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0374` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0375` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0376` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0377` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0378` — `DEFERRED-FUTURE-SCOPE` — DEFERRED-FIND-M9
- `COV-615A3-0406` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0407` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0408` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0409` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0410` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0411` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0412` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0413` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0414` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0415` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0416` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0417` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0418` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0419` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0420` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0421` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0422` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0423` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0424` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0425` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0426` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0427` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0428` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0429` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0430` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0431` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0432` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-615A3-0435` — `DEFERRED-FUTURE-SCOPE` — MANUALLY-BOUND-NONPROSE-CONSTRAINT
- `COV-615A3-0436` — `DEFERRED-FUTURE-SCOPE` — MANUALLY-BOUND-NONPROSE-CONSTRAINT
- `COV-615A3-0440` — `DEFERRED-FUTURE-SCOPE` — MANUALLY-BOUND-NONPROSE-CONSTRAINT
- `COV-615A3-0441` — `DEFERRED-FUTURE-SCOPE` — MANUALLY-BOUND-NONPROSE-CONSTRAINT
- `COV-6655-0008` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0033` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0044` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0055` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0056` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0057` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0058` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0059` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0060` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0061` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0066` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0067` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0068` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0069` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0070` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0072` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0073` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0074` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0075` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0076` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0077` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
- `COV-6655-0078` — `BLOCKED-BY-DEPENDENCY` — TRIGGERED-BY-615A3-DATA-OBJECT
