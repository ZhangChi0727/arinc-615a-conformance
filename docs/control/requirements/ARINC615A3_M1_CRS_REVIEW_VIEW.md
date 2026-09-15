# ARINC 615A-3 M1 CRS and Applicability — Generated Review View

> Generated from `configs/requirements/arinc_615a3_m1_crs.json` by `python scripts/sync_m1_crs.py --write`. Do not edit this view.

## Candidate state

- Disposition: `ADOPT`
- RG0: `PENDING-EXTERNAL-INDEPENDENT-REVIEW`
- RG1: `PENDING-EXTERNAL-INDEPENDENT-REVIEW`
- Formal approval: `EXTERNAL-JOINT-CONDITION-NOT-YET-SATISFIED`
- This package establishes neither Project Configuration nor protocol conformance.

## Inventory

- Coverage rows: 2796
- CRS items: 524
- Dependencies: 14
- Gaps: 1
- Coverage fingerprint: `806a197c7ec644f55d05dd8a6a31f80390ece5ccfe2e7d55a6816da6e2c04dfd`
- Requirements fingerprint: `d9e4f22496734c5635f518b881f6c7ce9d8bd1a4fdea1f296b225f4422eacd3b`
- Source-unit fingerprint: `6de712854823ea8ebf7040306ae6c76540f9dc6356acf3fff75c108c53e55241`
- Automated checks cover structure and cross-record consistency only; proprietary-source completeness and fidelity require external RG0 review.
- `generatedSemanticProjectionEn/Zh` are assertion-bound drift projections, not independent RG1 evidence.
- 665 edge policy: `REQUIREMENT-LEVEL-615A-TO-665-EDGES-DEFERRED-TO-M2-ATTACHMENT-RECONCILIATION`

## Applicability

- `APPLICABLE-BASE`: 89
- `APPLICABLE-SUPPORTING`: 325
- `CONDITIONAL`: 110

## Source modality

- `FACT`: 18
- `FIGURE-CONSTRAINT`: 63
- `MAY`: 55
- `MUST`: 15
- `SHOULD`: 246
- `TABLE-CONSTRAINT`: 127

## Conformance effect

- `CONDITIONAL-REQUIRED`: 99
- `OPTIONAL`: 54
- `REQUIRED`: 371

## Open dependencies and gaps

- `DEP-ARINC-645` — OPEN-DEPENDENCY: ARINC 645 algorithms remain unavailable. / ARINC 645 算法来源仍未取得。
- `DEP-ARINC-664-2` — OPEN-DEPENDENCY: Ethernet physical and link semantics remain open. / 以太网物理层与链路层语义仍开放。
- `DEP-ARINC-664-3` — OPEN-DEPENDENCY: Received P3-1 identity; edition and network applicability review remain open. / 已接收 P3-1 身份；版次与网络适用性评审仍开放。
- `DEP-ARINC-664-7` — OPEN-DEPENDENCY: Received P7 base edition; AFDX is deferred and AID future-supplement applicability remains open. / 已接收 P7 初版；AFDX 延期，AID 未来补充版适用性仍开放。
- `DEP-ARINC-6655` — REGISTERED-SUPPORTING-SOURCE: Bounded data-object source. / 有界数据对象来源。
- `DEP-RFC-1122` — OPEN-DEPENDENCY: RFC 1122 communication-layer identity retrieved; infrastructure conformance and applicability of subsequent updates remain unestablished. / 已取得 RFC 1122 通信层来源身份；基础设施符合性及后续更新适用性尚未建立。
- `DEP-RFC-1123` — OPEN-DEPENDENCY: Host requirement identity and applicability remain open. / 主机要求身份与适用性仍开放。
- `DEP-RFC-1350` — OPEN-DEPENDENCY: TFTP base identity and applicability remain open. / TFTP 基础身份与适用性仍开放。
- `DEP-RFC-1785` — OPEN-DEPENDENCY: TFTP option-negotiation identity remains open. / TFTP 选项协商身份仍开放。
- `DEP-RFC-2347` — OPEN-DEPENDENCY: TFTP option-extension identity remains open. / TFTP 选项扩展身份仍开放。
- `DEP-RFC-2348` — OPEN-DEPENDENCY: TFTP block-size option identity remains open. / TFTP 块大小选项身份仍开放。
- `DEP-RFC-2349` — OPEN-DEPENDENCY: TFTP timeout and transfer-size option identity remains open. / TFTP 超时与传输大小选项身份仍开放。
- `DEP-RFC-768` — OPEN-DEPENDENCY: UDP identity and applicability remain open. / UDP 身份与适用性仍开放。
- `DEP-RFC-791` — OPEN-DEPENDENCY: IP identity and applicability remain open. / IP 身份与适用性仍开放。
- `GAP-ARINC-645` — NOT-ESTABLISHED: ARINC 645-dependent validation remains blocked. / 依赖 ARINC 645 的验证仍受阻。

## Network reference inspection and approval blockers

M1 selects Compliant IPv4/UDP network services. P3 profiled exceptions and AFDX remain deferred. Reference-region inspection is not full network-stack conformance evidence; applicable RFC service behavior is an explicit, unverified infrastructure prerequisite.

- Network mode: `COMPLIANT`; AFDX selected: `False`.

| ID | Source / edition | Clause / PDF page | Inspection boundary | Summary |
|---|---|---|---|---|
| `NET-P3-SCOPE` | `ARINC-664-3` / `664P3-1` | 1.2 / 8 | `INSPECTION-REGION` | P3 distinguishes compliant and profiled networks; interoperability across these choices is not automatic. |
| `NET-P3-PRECEDENCE` | `ARINC-664-3` / `664P3-1` | 1.5 / 13 | `INSPECTION-REGION` | P3 restricts RFC options and establishes its precedence within its applicable network profile. |
| `NET-P3-TFTP` | `ARINC-664-3` / `664P3-1` | 3.2.2-3.2.3 / 21 | `INSPECTION-REGION` | Base TFTP references option RFCs; DL-TFTP implementation details refer back to 615A. |
| `NET-P3-UDP-RULE` | `ARINC-664-3` / `664P3-1` | 3.3.2 / 29 | `INSPECTION-REGION` | UDP is the minimum transport; profiled table X/E markings govern conformity and permitted exceptions, not a blanket recommendation. |
| `NET-P3-UDP-TABLE` | `ARINC-664-3` / `664P3-1` | Table 3.3.2-1 / 30 | `DEFERRED-PROFILED-TABLE-REGION` | The profiled UDP table differentiates checksum, source-address and interface obligations. Its deviations are unselected; applicable RFC behavior remains an unverified infrastructure prerequisite. |
| `NET-P3-IP-RULE` | `ARINC-664-3` / `664P3-1` | 3.4.1 / 31 | `INSPECTION-REGION` | IPv4 profiling uses a distinct requirement table and explicit exception rules. |
| `NET-P3-IP-TABLE` | `ARINC-664-3` / `664P3-1` | Table 3.4.1-1 / first page / 32 | `DEFERRED-PROFILED-TABLE-REGION` | Mandatory profiled rows include IPv4 version and header checks; the table is not yet an admitted leaf-level CRS inventory. |
| `NET-P3-FRAGMENT` | `ARINC-664-3` / `664P3-1` | Table 3.4.1-2 / 36 | `INSPECTION-REGION` | P3 permits specific reassembly deviations in profiled networks; these cannot erase the 615A Data Loader fragmentation/reassembly obligation. |
| `NET-P3-MTU` | `ARINC-664-3` / `664P3-1` | 3.4.1.2 / 36 | `INSPECTION-REGION` | MTU availability and respecting frame size concern network configuration and packet sizing, not a 615A operation deadline. |
| `NET-P3-ARP` | `ARINC-664-3` / `664P3-1` | 3.5.1 / 58 | `INSPECTION-REGION` | Dynamic ARP cache admission and static-map failure behavior are conditional network obligations requiring deployment selection. |
| `NET-P7-SCOPE` | `ARINC-664-7` / `664P7` | 1.2 / 9 | `INSPECTION-REGION` | AFDX defines a particular network profile and references P2 for physical links. |
| `NET-P7-TFTP` | `ARINC-664-7` / `664P7` | 3.3.1.2.3 / 40 | `INSPECTION-REGION` | AFDX file service lists TFTP RFCs and a block handling capacity; applicability is conditional on AFDX deployment. |
| `NET-P7-EXAMPLE` | `ARINC-664-7` / `664P7` | 3.3.2 / 42 | `INSPECTION-REGION` | Example ports and VLs do not replace the 615A control-port rule. |
| `NET-P7-IP` | `ARINC-664-7` / `664P7` | 3.3.3.2 / 44 | `INSPECTION-REGION` | AFDX IPv4 sizing accounts for its sequence number and refers to Attachment 2; it is not a global TFTP blocksize or timeout constraint. |
| `NET-P7-ADDRESS` | `ARINC-664-7` / `664P7` | 3.4.1.3.1-3.4.1.3.2 / 50 | `INSPECTION-REGION` | Intra/extra AFDX addressing and bidirectional SAP/queuing choices need system integration decisions. |
| `NET-P7-SWITCH` | `ARINC-664-7` / `664P7` | 4.9.1 / 75 | `INSPECTION-REGION` | Switch software loading refers to 615A/665, without making an AFDX switch the selected target of this Profile. |
| `NET-P7-PERFORMANCE` | `ARINC-664-7` / `664P7` | 5.1 / 80 | `INSPECTION-REGION` | AFDX burst-processing performance uses its own measurement conditions; it does not establish a 615A transfer timeout. |

| Relation | Owner | Target regions | Condition / disposition | Rationale / issues |
|---|---|---|---|---|
| `NET-REL-001` | `CRS-M1-00006` | NET-P3-SCOPE, NET-P3-PRECEDENCE, NET-P3-UDP-RULE, NET-P3-IP-RULE | `CURRENT-ETHERNET-PROFILE` / `APPLICABILITY-REVIEW-PENDING` | 615A 1.3 invokes P3. DD-023 selects its Compliant Network route; P3 exception tables do not replace applicable RFC behavior. Exact-edition acceptance remains an external review decision. / NET-ISSUE-EDITION, NET-ISSUE-PROFILE |
| `NET-REL-002` | `CRS-M1-00034` | NET-P3-FRAGMENT, NET-P3-MTU | `CURRENT-ETHERNET-PROFILE` / `APPLICABILITY-REVIEW-PENDING` | The current 615A loader fragmentation/reassembly obligation is retained. DD-023 excludes P3 no-reassembly deviations; MTU is a network-size constraint, not an operation deadline. / NET-ISSUE-PROFILE, NET-ISSUE-RFC1122 |
| `NET-REL-003` | `CRS-M1-00025` | NET-P3-TFTP, NET-P7-EXAMPLE | `CURRENT-ETHERNET-PROFILE` / `NO-NORMATIVE-OVERRIDE` | DL-TFTP refers back to 615A; the AFDX example using port 69 does not override 615A port 59. /  |
| `NET-REL-004` | `CRS-M1-00020` | NET-P3-TFTP | `CURRENT-ETHERNET-PROFILE` / `APPLICABILITY-REVIEW-PENDING` | P3 names RFC 2347 for base TFTP options; the precise 615A port-option source unit still needs review before a direct RFC edge is emitted. / NET-ISSUE-OPTION-EDGE |
| `NET-REL-005` | `COV-M1-01960` | NET-P7-SCOPE | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | This Appendix E source unit is inspected only for conditional AFDX context; target regions are review pointers, not proof of an equivalent atomic obligation. / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-006` | `COV-M1-01961` | NET-P7-SCOPE | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | This Appendix E source unit is inspected only for conditional AFDX context; target regions are review pointers, not proof of an equivalent atomic obligation. / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-007` | `COV-M1-01962` | NET-P7-SCOPE | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | This Appendix E source unit is inspected only for conditional AFDX context; target regions are review pointers, not proof of an equivalent atomic obligation. / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-008` | `COV-M1-01963` | NET-P7-ADDRESS | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | This Appendix E source unit is inspected only for conditional AFDX context; target regions are review pointers, not proof of an equivalent atomic obligation. / NET-ISSUE-AFDX-DETAIL, NET-ISSUE-AID |
| `NET-REL-009` | `COV-M1-01964` | NET-P7-ADDRESS | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | This Appendix E source unit is inspected only for conditional AFDX context; target regions are review pointers, not proof of an equivalent atomic obligation. / NET-ISSUE-AFDX-DETAIL, NET-ISSUE-AID |
| `NET-REL-010` | `COV-M1-01965` | NET-P7-ADDRESS | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | This Appendix E source unit is inspected only for conditional AFDX context; target regions are review pointers, not proof of an equivalent atomic obligation. / NET-ISSUE-AFDX-DETAIL, NET-ISSUE-AID |
| `NET-REL-011` | `COV-M1-01966` | NET-P7-SCOPE | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | This Appendix E source unit is inspected only for conditional AFDX context; target regions are review pointers, not proof of an equivalent atomic obligation. / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-012` | `COV-M1-01967` | NET-P7-ADDRESS | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | This Appendix E source unit is inspected only for conditional AFDX context; target regions are review pointers, not proof of an equivalent atomic obligation. / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-013` | `COV-M1-01968` | NET-P7-ADDRESS | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | This Appendix E source unit is inspected only for conditional AFDX context; target regions are review pointers, not proof of an equivalent atomic obligation. / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-014` | `COV-M1-01969` | NET-P7-ADDRESS | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | This Appendix E source unit is inspected only for conditional AFDX context; target regions are review pointers, not proof of an equivalent atomic obligation. / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-015` | `COV-M1-01970` | NET-P7-TFTP, NET-P7-EXAMPLE | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | This Appendix E source unit is inspected only for conditional AFDX context; target regions are review pointers, not proof of an equivalent atomic obligation. / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-016` | `COV-M1-01971` | NET-P7-IP, NET-P7-PERFORMANCE | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | This Appendix E source unit is inspected only for conditional AFDX context; target regions are review pointers, not proof of an equivalent atomic obligation. / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-017` | `COV-M1-01972` | NET-P7-ADDRESS | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | This Appendix E source unit is inspected only for conditional AFDX context; target regions are review pointers, not proof of an equivalent atomic obligation. / NET-ISSUE-AFDX-DETAIL, NET-ISSUE-ADDRESS |

| Issue | Blocks M1 approval | Status | Required resolution |
|---|---|---|---|
| `NET-ISSUE-EDITION` | `True` | `OPEN` | The exact historical editions are pinned for this candidate; independent RG0 must confirm this edition-bounded interpretation, not latest-edition compliance. P3 Supplement 1 describes continued IPv4 support; the P7 AID future-supplement issue remains separately deferred. |
| `NET-ISSUE-PROFILE` | `False` | `RESOLVED-BY-SCOPE-DECISION` | User selected Compliant Network under DD-023. P3 exception columns are not selected. RFC-conforming IPv4/UDP behavior remains an unverified infrastructure prerequisite. |
| `NET-ISSUE-RFC1122` | `False` | `SOURCE-ACQUIRED-REVIEW-PENDING` | RFC 1122 was retrieved from RFC Editor with an immutable content hash. Its applicable obligations and updates remain part of the infrastructure prerequisite; retrieval is not conformance evidence. |
| `NET-ISSUE-OPTION-EDGE` | `False` | `OPEN` | A-2 remains deferred: P3 3.2.2 names RFC 2347 and P7 lists RFC 1785, but this does not prove an exact active 615A atomic trigger edge. |
| `NET-ISSUE-AFDX-DETAIL` | `False` | `OPEN` | AFDX remains unselected; P7 Attachment 2, IEEE 802.3 (2000), and configuration-dependent latency/MTU need a later admitted deployment audit. |
| `NET-ISSUE-AID` | `False` | `OPEN` | 615A Appendix E names an AID defined in a future P7 supplement; the supplied base edition cannot close that future supplement reference. |
| `NET-ISSUE-ADDRESS` | `False` | `OPEN` | Appendix E allows P4 address rules or integrator-defined requirements; record the choice before AFDX activation. P4 is not automatically a procurement mandate. |

### Infrastructure premises and public sources

`DD-023`

- `NET-PREMISE-IPV4-UDP` / `NOT-ESTABLISHED` / `PROJECT-CONFIGURATION-GATE`: The underlying IPv4/UDP service must satisfy applicable IETF host requirements without P3-specific deviations. Retained as an infrastructure prerequisite; neither implementation compliance nor a complete RFC requirements inventory is claimed. M2 must plan its substantiation before any execution configuration is approved.
- `RFC-1122`: https://www.rfc-editor.org/rfc/rfc1122.txt / SHA-256 `9f526e6bebc868324fedb90aebbcf6e5b15c53fd373ca5d5ce1c2cdcd264e04f`

## CRS items

| ID | Source unit | Actor / condition / action / object / observable effect | Modality / effect | Applicability | Generated semantic projection (assertion-bound) | Timing provenance | Dependencies / gaps |
|---|---|---|---|---|---|---|---|
| `CRS-M1-00001` | `SU-ARINC-615A-3-1-2-P014-PROSE-SENTENCE-002-8D3CB7C14FBD`<br>`ARINC-615A-3 1.2 p.2` | `ARINC-615A-CONFORMING-IMPLEMENTATION` / `UNCONDITIONAL` / `IMPLEMENT-REQUIRED-STANDARD-FUNCTIONS` / `MINIMUM-COMPATIBILITY-FUNCTION-SET` / `COMPATIBILITY-CAPABILITY-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-CONFORMING-IMPLEMENTATION shall perform IMPLEMENT-REQUIRED-STANDARD-FUNCTIONS on MINIMUM-COMPATIBILITY-FUNCTION-SET under UNCONDITIONAL; evidence is the resulting COMPATIBILITY-CAPABILITY-OBSERVABLE.<br>参与者“ARINC-615A-CONFORMING-IMPLEMENTATION”在“UNCONDITIONAL”下必须对“MINIMUM-COMPATIBILITY-FUNCTION-SET”执行“IMPLEMENT-REQUIRED-STANDARD-FUNCTIONS”；证据是“COMPATIBILITY-CAPABILITY-OBSERVABLE”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00002` | `SU-ARINC-615A-3-1-2-P014-PROSE-SENTENCE-003-8280DDEE506E`<br>`ARINC-615A-3 1.2 p.2` | `ARINC-615A-REQUIREMENT-INTERPRETER` / `WHEN-INTERPRETING-ARINC-615A-NORMATIVE-LANGUAGE` / `TREAT-615A-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY` / `ARINC-615A-SHOULD-MODALITY` / `MODALITY-INTERPRETATION-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-REQUIREMENT-INTERPRETER shall perform TREAT-615A-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY on ARINC-615A-SHOULD-MODALITY under WHEN-INTERPRETING-ARINC-615A-NORMATIVE-LANGUAGE; evidence is the resulting MODALITY-INTERPRETATION-OBSERVABLE.<br>参与者“ARINC-615A-REQUIREMENT-INTERPRETER”在“WHEN-INTERPRETING-ARINC-615A-NORMATIVE-LANGUAGE”下必须对“ARINC-615A-SHOULD-MODALITY”执行“TREAT-615A-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY”；证据是“MODALITY-INTERPRETATION-OBSERVABLE”。 | — | — |
| `CRS-M1-00003` | `SU-ARINC-615A-3-1-2-P014-PROSE-SENTENCE-004-9B5A3832A655`<br>`ARINC-615A-3 1.2 p.2` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `USE` / `CONFORMANCE-MODALITY` / `USE-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION may perform USE on CONFORMANCE-MODALITY under UNCONDITIONAL; evidence is the resulting USE-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下可以对“CONFORMANCE-MODALITY”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00004` | `SU-ARINC-615A-3-1-2-P014-PROSE-SENTENCE-005-7D9A4E2DA48E`<br>`ARINC-615A-3 1.2 p.2` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `WHEN-OPTIONAL-CAPABILITY-IMPLEMENTED` / `IMPLEMENT` / `CONFORMANCE-MODALITY` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform IMPLEMENT on CONFORMANCE-MODALITY under WHEN-OPTIONAL-CAPABILITY-IMPLEMENTED; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“实现可选能力时”下必须对“CONFORMANCE-MODALITY”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00005` | `SU-ARINC-615A-3-1-3-P014-PROSE-SENTENCE-001-2FA34C046AFB`<br>`ARINC-615A-3 1.3 p.2` | `DATA-LOADER` / `UNCONDITIONAL` / `TRANSFER` / `SOFTWARE-PART` / `TRANSFER-OUTCOME-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform TRANSFER on SOFTWARE-PART under UNCONDITIONAL; evidence is the resulting TRANSFER-OUTCOME-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下必须对“软件加载件”执行“传输”；证据是“传输结果可被观察”。 | — | — |
| `CRS-M1-00006` | `SU-ARINC-615A-3-1-3-P014-PROSE-SENTENCE-002-873AFAE35C45`<br>`ARINC-615A-3 1.3 p.2` | `DATA-LOADER-AND-TARGET-HARDWARE` / `UNCONDITIONAL` / `TRANSFER-VIA-ETHERNET` / `DATA-TRANSFER` / `ETHERNET-TRANSFER-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER-AND-TARGET-HARDWARE shall perform TRANSFER-VIA-ETHERNET on DATA-TRANSFER under UNCONDITIONAL; evidence is the resulting ETHERNET-TRANSFER-OBSERVABLE.<br>参与者“DATA-LOADER-AND-TARGET-HARDWARE”在“UNCONDITIONAL”下必须对“DATA-TRANSFER”执行“TRANSFER-VIA-ETHERNET”；证据是“ETHERNET-TRANSFER-OBSERVABLE”。 | — | DEP-ARINC-664-2, DEP-ARINC-664-3 |
| `CRS-M1-00007` | `SU-ARINC-615A-3-1-3-P014-PROSE-SENTENCE-007-EC7965CC3D31`<br>`ARINC-615A-3 1.3 p.2` | `DATA-LOADER` / `UNCONDITIONAL` / `IMPLEMENT` / `OPERATION, NETWORK-INTERFACE` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform IMPLEMENT on OPERATION, NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下必须对“协议操作、网络接口”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00008` | `SU-ARINC-615A-3-1-3-P014-PROSE-SENTENCE-009-00560ACC8ACC`<br>`ARINC-615A-3 1.3 p.2` | `ARINC-615A-DEFINITION` / `UNCONDITIONAL` / `ALLOW-COMBINATION` / `DATA-LOADING-TYPES` / `COMBINED-LOADING-CAPABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-DEFINITION shall perform ALLOW-COMBINATION on DATA-LOADING-TYPES under UNCONDITIONAL; evidence is the resulting COMBINED-LOADING-CAPABILITY-OBSERVABLE.<br>参与者“ARINC-615A-DEFINITION”在“UNCONDITIONAL”下必须对“DATA-LOADING-TYPES”执行“ALLOW-COMBINATION”；证据是“COMBINED-LOADING-CAPABILITY-OBSERVABLE”。 | — | — |
| `CRS-M1-00009` | `SU-ARINC-615A-3-1-3-P015-PROSE-SENTENCE-011-06D3CBD76B0F`<br>`ARINC-615A-3 1.3 p.3` | `ARINC-615A-TRANSPORT-INTEGRATOR` / `WHEN-TRANSPORTING-ARINC-615A-OVER-AN-ALTERNATE-NETWORK` / `PRESERVE-PROTOCOL-SEMANTICS-OVER-ALTERNATE-NETWORK` / `ALTERNATE-NETWORK-TRANSPORT` / `TRANSPORT-COMPATIBILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-TRANSPORT-INTEGRATOR shall perform PRESERVE-PROTOCOL-SEMANTICS-OVER-ALTERNATE-NETWORK on ALTERNATE-NETWORK-TRANSPORT under WHEN-TRANSPORTING-ARINC-615A-OVER-AN-ALTERNATE-NETWORK; evidence is the resulting TRANSPORT-COMPATIBILITY-OBSERVABLE.<br>参与者“ARINC-615A-TRANSPORT-INTEGRATOR”在“WHEN-TRANSPORTING-ARINC-615A-OVER-AN-ALTERNATE-NETWORK”下必须对“ALTERNATE-NETWORK-TRANSPORT”执行“PRESERVE-PROTOCOL-SEMANTICS-OVER-ALTERNATE-NETWORK”；证据是“TRANSPORT-COMPATIBILITY-OBSERVABLE”。 | — | — |
| `CRS-M1-00010` | `SU-ARINC-615A-3-1-3-P015-PROSE-SENTENCE-014-ACDCC666CD78`<br>`ARINC-615A-3 1.3 p.3` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `IMPLEMENT` / `NETWORK-INTERFACE` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform IMPLEMENT on NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“网络接口”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00011` | `SU-ARINC-615A-3-1-3-P015-PROSE-SENTENCE-015-C47A9C5EA9CF`<br>`ARINC-615A-3 1.3 p.3` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `SELECT` / `SOFTWARE-PART, OPERATION, TARGET-HARDWARE-ID` / `SELECT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform SELECT on SOFTWARE-PART, OPERATION, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting SELECT-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“软件加载件、协议操作、TARGET-HARDWARE-ID”执行“选择”；证据是“SELECT-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00012` | `SU-ARINC-615A-3-1-6-P017-PROSE-SENTENCE-001-6E91C83C11CE`<br>`ARINC-615A-3 1.6 p.5` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `DESIGN` / `NETWORK-INTERFACE` / `DESIGN-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform DESIGN on NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting DESIGN-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“网络接口”执行“设计”；证据是“DESIGN-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00013` | `SU-ARINC-615A-3-1-6-P017-PROSE-SENTENCE-003-817EC6E68797`<br>`ARINC-615A-3 1.6 p.5` | `DATA-LOADER` / `UNCONDITIONAL` / `IMPLEMENT` / `NETWORK-INTERFACE` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform IMPLEMENT on NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下必须对“网络接口”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00014` | `SU-ARINC-615A-3-1-6-P017-PROSE-SENTENCE-004-1768AAB8F452`<br>`ARINC-615A-3 1.6 p.5` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ENCODE` / `NETWORK-INTERFACE` / `ENCODED-FIELD-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION may perform ENCODE on NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下可以对“网络接口”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00015` | `SU-ARINC-615A-3-1-6-P017-PROSE-SENTENCE-005-358B4BAB3D69`<br>`ARINC-615A-3 1.6 p.5` | `PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ENCODE` / `NETWORK-INTERFACE` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-IMPLEMENTATION shall perform ENCODE on NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议实现”在“UNCONDITIONAL”下必须对“网络接口”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00016` | `SU-ARINC-615A-3-1-6-P017-PROSE-SENTENCE-006-711482ED9B24`<br>`ARINC-615A-3 1.6 p.5` | `SOFTWARE-PACKAGE-PRODUCER` / `UNCONDITIONAL` / `COMPLY` / `SOFTWARE-PART, NETWORK-INTERFACE` / `COMPLY-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor SOFTWARE-PACKAGE-PRODUCER shall perform COMPLY on SOFTWARE-PART, NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting COMPLY-RESULT-OBSERVABLE.<br>参与者“软件包生成方”在“UNCONDITIONAL”下必须对“软件加载件、网络接口”执行“符合”；证据是“COMPLY-RESULT-OBSERVABLE”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00017` | `SU-ARINC-615A-3-5-1-P034-PROSE-SENTENCE-015-441CC925118B`<br>`ARINC-615A-3 5.1 p.22` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `PROTOCOL-FILE-NAME` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER shall perform ENCODE on PROTOCOL-FILE-NAME under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议文件生成方”在“UNCONDITIONAL”下必须对“PROTOCOL-FILE-NAME”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00018` | `SU-ARINC-615A-3-5-1-P034-PROSE-SENTENCE-016-EE8EBA5E1E47`<br>`ARINC-615A-3 5.1 p.22` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `COMPLY` / `NETWORK-INTERFACE` / `COMPLY-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform COMPLY on NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting COMPLY-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“网络接口”执行“符合”；证据是“COMPLY-RESULT-OBSERVABLE”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00019` | `SU-ARINC-615A-3-5-2-P035-PROSE-SENTENCE-017-D07026646B5D`<br>`ARINC-615A-3 5.2 p.23` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `USE` / `FIND-SERVICE, TARGET-HARDWARE-ID` / `USE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform USE on FIND-SERVICE, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting USE-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“FIND-SERVICE、TARGET-HARDWARE-ID”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00020` | `SU-ARINC-615A-3-5-3-2-2-P037-PROSE-SENTENCE-001-5DE45B64D498`<br>`ARINC-615A-3 5.3.2.2 p.25` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `TRANSFER` / `TFTP-OPTION` / `TRANSFER-OUTCOME-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION may perform TRANSFER on TFTP-OPTION under UNCONDITIONAL; evidence is the resulting TRANSFER-OUTCOME-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下可以对“TFTP 选项”执行“传输”；证据是“传输结果可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00021` | `SU-ARINC-615A-3-5-3-2-2-P037-PROSE-SENTENCE-003-DE334C18716C`<br>`ARINC-615A-3 5.3.2.2 p.25` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `USE` / `DEFAULT-OPTION-VALUES` / `USE-RESULT-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform USE on DEFAULT-OPTION-VALUES under UNCONDITIONAL; evidence is the resulting USE-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“DEFAULT-OPTION-VALUES”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00022` | `SU-ARINC-615A-3-5-3-2-2-P037-PROSE-SENTENCE-004-FC7D3B3729A1`<br>`ARINC-615A-3 5.3.2.2 p.25` | `ARINC-615A-TFTP-IMPLEMENTATION` / `WHEN-A-TFTP-OPTION-IS-NOT-IMPLEMENTED` / `DO-NOT-FAIL-TRANSFER-FOR-UNIMPLEMENTED-OPTION` / `TFTP-TRANSFER, UNIMPLEMENTED-TFTP-OPTION` / `ABSENCE-OF-OPTION-CAUSED-TRANSFER-FAILURE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-TFTP-IMPLEMENTATION shall perform DO-NOT-FAIL-TRANSFER-FOR-UNIMPLEMENTED-OPTION on TFTP-TRANSFER, UNIMPLEMENTED-TFTP-OPTION under WHEN-A-TFTP-OPTION-IS-NOT-IMPLEMENTED; evidence is the resulting ABSENCE-OF-OPTION-CAUSED-TRANSFER-FAILURE-OBSERVABLE.<br>参与者“ARINC-615A-TFTP-IMPLEMENTATION”在“WHEN-A-TFTP-OPTION-IS-NOT-IMPLEMENTED”下必须对“TFTP-TRANSFER、UNIMPLEMENTED-TFTP-OPTION”执行“DO-NOT-FAIL-TRANSFER-FOR-UNIMPLEMENTED-OPTION”；证据是“ABSENCE-OF-OPTION-CAUSED-TRANSFER-FAILURE-OBSERVABLE”。 | — | — |
| `CRS-M1-00023` | `SU-ARINC-615A-3-5-3-2-2-P037-PROSE-SENTENCE-005-C966C11D19B8`<br>`ARINC-615A-3 5.3.2.2 p.25` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `AFTER-LAST-TFTP-OPTION` / `ABSENT-AFTER-BOUNDARY` / `TFTP-OPTION, NETWORK-INTERFACE` / `ABSENT-AFTER-BOUNDARY-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform ABSENT-AFTER-BOUNDARY on TFTP-OPTION, NETWORK-INTERFACE under AFTER-LAST-TFTP-OPTION; evidence is the resulting ABSENT-AFTER-BOUNDARY-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“最后一个 TFTP 选项结束后”下必须对“TFTP 选项、网络接口”执行“确保边界后不存在数据”；证据是“ABSENT-AFTER-BOUNDARY-RESULT-OBSERVABLE”。 | — | DEP-RFC-768, DEP-RFC-791, DEP-RFC-1350 |
| `CRS-M1-00024` | `SU-ARINC-615A-3-5-3-2-3-2-P037-PROSE-SENTENCE-002-1E0F8D921559`<br>`ARINC-615A-3 5.3.2.3.2 p.25` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `TRANSFER` / `TARGET-HARDWARE-ID` / `TRANSFER-OUTCOME-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE may perform TRANSFER on TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting TRANSFER-OUTCOME-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下可以对“TARGET-HARDWARE-ID”执行“传输”；证据是“传输结果可被观察”。 | — | — |
| `CRS-M1-00025` | `SU-ARINC-615A-3-5-3-2-3-2-P037-PROSE-SENTENCE-004-F3852739104C`<br>`ARINC-615A-3 5.3.2.3.2 p.25` | `ARINC-615A-TFTP-IMPLEMENTATION` / `UNCONDITIONAL` / `USE-WELL-KNOWN-PORT` / `TFTP-PORT-59` / `TFTP-PORT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-TFTP-IMPLEMENTATION shall perform USE-WELL-KNOWN-PORT on TFTP-PORT-59 under UNCONDITIONAL; evidence is the resulting TFTP-PORT-OBSERVABLE.<br>参与者“ARINC-615A-TFTP-IMPLEMENTATION”在“UNCONDITIONAL”下必须对“TFTP-PORT-59”执行“USE-WELL-KNOWN-PORT”；证据是“TFTP-PORT-OBSERVABLE”。 | — | DEP-RFC-1350 |
| `CRS-M1-00026` | `SU-ARINC-615A-3-5-3-2-3-3-P038-PROSE-SENTENCE-004-15DBABB1142A`<br>`ARINC-615A-3 5.3.2.3.3 p.26` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `USE` / `ERROR-CODE` / `USE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform USE on ERROR-CODE under UNCONDITIONAL; evidence is the resulting USE-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“错误码”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00027` | `SU-ARINC-615A-3-5-3-2-3-3-P038-PROSE-SENTENCE-005-A1C528A5F702`<br>`ARINC-615A-3 5.3.2.3.3 p.26` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `ERROR-CODE, ERROR-MESSAGE` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER shall perform ENCODE on ERROR-CODE, ERROR-MESSAGE under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议文件生成方”在“UNCONDITIONAL”下必须对“错误码、错误消息”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00028` | `SU-ARINC-615A-3-5-3-2-3-3-P038-PROSE-SENTENCE-006-06665FE11D6E`<br>`ARINC-615A-3 5.3.2.3.3 p.26` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `ERROR-CODE, ERROR-MESSAGE` / `ENCODED-FIELD-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER may perform ENCODE on ERROR-CODE, ERROR-MESSAGE under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议文件生成方”在“UNCONDITIONAL”下可以对“错误码、错误消息”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00029` | `SU-ARINC-615A-3-5-3-2-3-3-P038-PROSE-SENTENCE-007-2560DF2DBBD3`<br>`ARINC-615A-3 5.3.2.3.3 p.26` | `DATA-LOADER` / `UNCONDITIONAL` / `REPORT-RESOURCE-UNAVAILABLE` / `TFTP-ERROR-CODE-3` / `ERROR-PACKET-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform REPORT-RESOURCE-UNAVAILABLE on TFTP-ERROR-CODE-3 under UNCONDITIONAL; evidence is the resulting ERROR-PACKET-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下必须对“TFTP-ERROR-CODE-3”执行“REPORT-RESOURCE-UNAVAILABLE”；证据是“ERROR-PACKET-OBSERVABLE”。 | — | DEP-RFC-1350 |
| `CRS-M1-00030` | `SU-ARINC-615A-3-5-3-2-3-3-P038-PROSE-SENTENCE-008-B72528E71CC2`<br>`ARINC-615A-3 5.3.2.3.3 p.26` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `REPORT-RESOURCE-UNAVAILABLE` / `TFTP-ERROR-CODE-3` / `ERROR-PACKET-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform REPORT-RESOURCE-UNAVAILABLE on TFTP-ERROR-CODE-3 under UNCONDITIONAL; evidence is the resulting ERROR-PACKET-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“TFTP-ERROR-CODE-3”执行“REPORT-RESOURCE-UNAVAILABLE”；证据是“ERROR-PACKET-OBSERVABLE”。 | — | DEP-RFC-1350 |
| `CRS-M1-00031` | `SU-ARINC-615A-3-5-3-2-3-4-P038-PROSE-SENTENCE-004-1F95516BE886`<br>`ARINC-615A-3 5.3.2.3.4 p.26` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `TRANSFER` / `PROTOCOL-MESSAGE` / `TRANSFER-OUTCOME-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION may perform TRANSFER on PROTOCOL-MESSAGE under UNCONDITIONAL; evidence is the resulting TRANSFER-OUTCOME-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下可以对“PROTOCOL-MESSAGE”执行“传输”；证据是“传输结果可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00032` | `SU-ARINC-615A-3-5-3-2-3-4-P038-PROSE-SENTENCE-006-D6FEB985BBBB`<br>`ARINC-615A-3 5.3.2.3.4 p.26` | `TFTP-WAIT-RECEIVER` / `WHEN-A-WAIT-MESSAGE-IS-RECEIVED` / `ABORT-AND-RESTART-AFTER-DELAY` / `CURRENT-TFTP-TRANSFER, WAIT-DELAY` / `ABORT-THEN-RETRY-SEQUENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TFTP-WAIT-RECEIVER shall perform ABORT-AND-RESTART-AFTER-DELAY on CURRENT-TFTP-TRANSFER, WAIT-DELAY under WHEN-A-WAIT-MESSAGE-IS-RECEIVED; evidence is the resulting ABORT-THEN-RETRY-SEQUENCE-OBSERVABLE.<br>参与者“TFTP-WAIT-RECEIVER”在“WHEN-A-WAIT-MESSAGE-IS-RECEIVED”下必须对“CURRENT-TFTP-TRANSFER、WAIT-DELAY”执行“ABORT-AND-RESTART-AFTER-DELAY”；证据是“ABORT-THEN-RETRY-SEQUENCE-OBSERVABLE”。 | `MESSAGE-CARRIED-PARAMETER` / `MESSAGE-TIMER-VALUE` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-TABLE-6_4_3-1-R006 | DEP-RFC-1350 |
| `CRS-M1-00033` | `SU-ARINC-615A-3-5-3-2-3-8-P040-PROSE-SENTENCE-002-ADF7BE206185`<br>`ARINC-615A-3 5.3.2.3.8 p.28` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ENCODE` / `NETWORK-INTERFACE` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform ENCODE on NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“网络接口”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00034` | `SU-ARINC-615A-3-5-3-2-3-8-1-P040-PROSE-SENTENCE-001-28CC7C395DC9`<br>`ARINC-615A-3 5.3.2.3.8.1 p.28` | `DATA-LOADER` / `UNCONDITIONAL` / `IMPLEMENT` / `TFTP-BLOCK-SIZE, NETWORK-INTERFACE` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform IMPLEMENT on TFTP-BLOCK-SIZE, NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下必须对“TFTP 块大小、网络接口”执行“提供能力”；证据是“能力可用性可被观察”。 | — | DEP-RFC-791, DEP-RFC-1350, DEP-RFC-2348 |
| `CRS-M1-00035` | `SU-ARINC-615A-3-5-3-2-3-8-1-P040-PROSE-SENTENCE-002-A3F954863D43`<br>`ARINC-615A-3 5.3.2.3.8.1 p.28` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `IMPLEMENT` / `CONFORMANCE-MODALITY, TARGET-HARDWARE-ID` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform IMPLEMENT on CONFORMANCE-MODALITY, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“CONFORMANCE-MODALITY、TARGET-HARDWARE-ID”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00036` | `SU-ARINC-615A-3-5-3-2-3-8-1-P041-PROSE-SENTENCE-003-C74E9B3EC0A0`<br>`ARINC-615A-3 5.3.2.3.8.1 p.29` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `USE` / `TFTP-BLOCK-SIZE, TARGET-HARDWARE-ID` / `USE-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE may perform USE on TFTP-BLOCK-SIZE, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting USE-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下可以对“TFTP 块大小、TARGET-HARDWARE-ID”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | DEP-RFC-1350, DEP-RFC-2348 |
| `CRS-M1-00037` | `SU-ARINC-615A-3-5-3-2-3-8-2-P041-PROSE-SENTENCE-001-700C898C606C`<br>`ARINC-615A-3 5.3.2.3.8.2 p.29` | `PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `USE` / `NETWORK-INTERFACE` / `USE-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-IMPLEMENTATION may perform USE on NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting USE-RESULT-OBSERVABLE.<br>参与者“协议实现”在“UNCONDITIONAL”下可以对“网络接口”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00038` | `SU-ARINC-615A-3-5-3-2-3-8-2-P041-PROSE-SENTENCE-002-A12EC6F8831E`<br>`ARINC-615A-3 5.3.2.3.8.2 p.29` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `WHEN-TRANSFER-SIZE-MISMATCHES` / `COMPARE` / `TFTP-TRANSFER-SIZE, TFTP-FILE-TRANSFER` / `COMPARISON-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform COMPARE on TFTP-TRANSFER-SIZE, TFTP-FILE-TRANSFER under WHEN-TRANSFER-SIZE-MISMATCHES; evidence is the resulting COMPARISON-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“声明传输大小与实际数据不一致时”下必须对“TFTP 传输大小、TFTP 文件传输”执行“比较”；证据是“比较结果可被观察”。 | — | DEP-RFC-2349 |
| `CRS-M1-00039` | `SU-ARINC-615A-3-5-3-2-3-8-3-P041-PROSE-SENTENCE-001-700C898C606C`<br>`ARINC-615A-3 5.3.2.3.8.3 p.29` | `PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `USE` / `NETWORK-INTERFACE` / `USE-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-IMPLEMENTATION may perform USE on NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting USE-RESULT-OBSERVABLE.<br>参与者“协议实现”在“UNCONDITIONAL”下可以对“网络接口”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00040` | `SU-ARINC-615A-3-5-3-2-3-8-4-P041-PROSE-SENTENCE-001-700C898C606C`<br>`ARINC-615A-3 5.3.2.3.8.4 p.29` | `PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `USE` / `NETWORK-INTERFACE` / `USE-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-IMPLEMENTATION may perform USE on NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting USE-RESULT-OBSERVABLE.<br>参与者“协议实现”在“UNCONDITIONAL”下可以对“网络接口”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00041` | `SU-ARINC-615A-3-5-3-2-3-8-5-P041-PROSE-SENTENCE-001-700C898C606C`<br>`ARINC-615A-3 5.3.2.3.8.5 p.29` | `PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `USE` / `NETWORK-INTERFACE` / `USE-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-IMPLEMENTATION may perform USE on NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting USE-RESULT-OBSERVABLE.<br>参与者“协议实现”在“UNCONDITIONAL”下可以对“网络接口”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00042` | `SU-ARINC-615A-3-5-3-2-3-8-5-P042-PROSE-SENTENCE-009-89192D1CA807`<br>`ARINC-615A-3 5.3.2.3.8.5 p.30` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ENCODE` / `HEADER-FILE, CRC, SOFTWARE-PART, TARGET-HARDWARE-ID` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform ENCODE on HEADER-FILE, CRC, SOFTWARE-PART, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“头文件、CRC／校验值、软件加载件、TARGET-HARDWARE-ID”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | DEP-RFC-1350, DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00043` | `SU-ARINC-615A-3-5-3-2-3-8-5-P042-PROSE-SENTENCE-010-B47966431472`<br>`ARINC-615A-3 5.3.2.3.8.5 p.30` | `DATA-LOADER` / `WHEN-THE-CHECKSUM-OPTION-IS-PRESENT` / `LOCATE-REQUESTED-FILE-USING-INCLUDED-CRC` / `REQUESTED-FILE, INCLUDED-CRC` / `REQUESTED-FILE-SELECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform LOCATE-REQUESTED-FILE-USING-INCLUDED-CRC on REQUESTED-FILE, INCLUDED-CRC under WHEN-THE-CHECKSUM-OPTION-IS-PRESENT; evidence is the resulting REQUESTED-FILE-SELECTION-OBSERVABLE.<br>参与者“数据加载器”在“WHEN-THE-CHECKSUM-OPTION-IS-PRESENT”下必须对“REQUESTED-FILE、INCLUDED-CRC”执行“LOCATE-REQUESTED-FILE-USING-INCLUDED-CRC”；证据是“REQUESTED-FILE-SELECTION-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00044` | `SU-ARINC-615A-3-5-3-2-3-8-5-P042-PROSE-SENTENCE-018-7A289A4F990C`<br>`ARINC-615A-3 5.3.2.3.8.5 p.30` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `USE` / `CRC` / `USE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform USE on CRC under UNCONDITIONAL; evidence is the resulting USE-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“CRC／校验值”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00045` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-022-12774BEEEE8C`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `IMPLEMENT` / `NETWORK-INTERFACE, TARGET-HARDWARE-ID` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE may perform IMPLEMENT on NETWORK-INTERFACE, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下可以对“网络接口、TARGET-HARDWARE-ID”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00046` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-023-5321224DBF5C`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `SOFTWARE-PACKAGE-PRODUCER` / `UNCONDITIONAL` / `IMPLEMENT` / `HEADER-FILE, CRC, SOFTWARE-PART, NETWORK-INTERFACE` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor SOFTWARE-PACKAGE-PRODUCER shall perform IMPLEMENT on HEADER-FILE, CRC, SOFTWARE-PART, NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“软件包生成方”在“UNCONDITIONAL”下必须对“头文件、CRC／校验值、软件加载件、网络接口”执行“提供能力”；证据是“能力可用性可被观察”。 | — | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00047` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-024-04F65EF5ECB7`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `DATA-LOADER` / `UNCONDITIONAL` / `SEND` / `CRC` / `MESSAGE-OR-FILE-DIRECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform SEND on CRC under UNCONDITIONAL; evidence is the resulting MESSAGE-OR-FILE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下必须对“CRC／校验值”执行“发送”；证据是“消息或文件及其方向可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00048` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-026-443ABAEE9FB5`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `TRANSFER` / `NETWORK-INTERFACE, TARGET-HARDWARE-ID, LCL-TRANSFER` / `TRANSFER-OUTCOME-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE may perform TRANSFER on NETWORK-INTERFACE, TARGET-HARDWARE-ID, LCL-TRANSFER under UNCONDITIONAL; evidence is the resulting TRANSFER-OUTCOME-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下可以对“网络接口、TARGET-HARDWARE-ID、LCL-TRANSFER”执行“传输”；证据是“传输结果可被观察”。 | — | — |
| `CRS-M1-00049` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-027-6937C2561848`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `SEND` / `CRC, NETWORK-INTERFACE` / `MESSAGE-OR-FILE-DIRECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform SEND on CRC, NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting MESSAGE-OR-FILE-DIRECTION-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“CRC／校验值、网络接口”执行“发送”；证据是“消息或文件及其方向可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00050` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-029-CCAB139B0370`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `TARGET-HARDWARE` / `WHEN-RESPONDING-TO-A-SUPPORTED-CHECKSUM-OPTION` / `RETURN-FILE-CHECKSUM-COMPUTED-BY-INDICATED-ALGORITHM` / `ENTIRE-FILE, INDICATED-CHECKSUM-ALGORITHM, CHECKSUM-VALUE` / `RETURNED-CHECKSUM-VALUE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform RETURN-FILE-CHECKSUM-COMPUTED-BY-INDICATED-ALGORITHM on ENTIRE-FILE, INDICATED-CHECKSUM-ALGORITHM, CHECKSUM-VALUE under WHEN-RESPONDING-TO-A-SUPPORTED-CHECKSUM-OPTION; evidence is the resulting RETURNED-CHECKSUM-VALUE-OBSERVABLE.<br>参与者“目标硬件”在“WHEN-RESPONDING-TO-A-SUPPORTED-CHECKSUM-OPTION”下必须对“ENTIRE-FILE、INDICATED-CHECKSUM-ALGORITHM、CHECKSUM-VALUE”执行“RETURN-FILE-CHECKSUM-COMPUTED-BY-INDICATED-ALGORITHM”；证据是“RETURNED-CHECKSUM-VALUE-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00051` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-030-15DD7CD59677`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `TARGET-HARDWARE` / `WHEN-CHECKSUM-OPTION-IS-GIVEN-AND-ALGORITHM-IS-SUPPORTED` / `ACKNOWLEDGE-CHECKSUM-OPTION-IF-ALGORITHM-SUPPORTED` / `CHECKSUM-OPTION, SPECIFIED-CHECKSUM-ALGORITHM` / `CHECKSUM-OPTION-ACKNOWLEDGEMENT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform ACKNOWLEDGE-CHECKSUM-OPTION-IF-ALGORITHM-SUPPORTED on CHECKSUM-OPTION, SPECIFIED-CHECKSUM-ALGORITHM under WHEN-CHECKSUM-OPTION-IS-GIVEN-AND-ALGORITHM-IS-SUPPORTED; evidence is the resulting CHECKSUM-OPTION-ACKNOWLEDGEMENT-OBSERVABLE.<br>参与者“目标硬件”在“WHEN-CHECKSUM-OPTION-IS-GIVEN-AND-ALGORITHM-IS-SUPPORTED”下必须对“CHECKSUM-OPTION、SPECIFIED-CHECKSUM-ALGORITHM”执行“ACKNOWLEDGE-CHECKSUM-OPTION-IF-ALGORITHM-SUPPORTED”；证据是“CHECKSUM-OPTION-ACKNOWLEDGEMENT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00052` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-030-15DD7CD59677`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `DATA-LOADER` / `AFTER-CHECKSUM-OPTION-ACKNOWLEDGEMENT-AND-FILE-TRANSFER-COMPLETION` / `CALCULATE-AND-VALIDATE-RECEIVED-FILE-CHECKSUM` / `ENTIRE-RECEIVED-DATA-FILE, ACKNOWLEDGED-CHECKSUM-ALGORITHM` / `POST-TRANSFER-INTEGRITY-VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform CALCULATE-AND-VALIDATE-RECEIVED-FILE-CHECKSUM on ENTIRE-RECEIVED-DATA-FILE, ACKNOWLEDGED-CHECKSUM-ALGORITHM under AFTER-CHECKSUM-OPTION-ACKNOWLEDGEMENT-AND-FILE-TRANSFER-COMPLETION; evidence is the resulting POST-TRANSFER-INTEGRITY-VALIDATION-RESULT-OBSERVABLE.<br>参与者“数据加载器”在“AFTER-CHECKSUM-OPTION-ACKNOWLEDGEMENT-AND-FILE-TRANSFER-COMPLETION”下必须对“ENTIRE-RECEIVED-DATA-FILE、ACKNOWLEDGED-CHECKSUM-ALGORITHM”执行“CALCULATE-AND-VALIDATE-RECEIVED-FILE-CHECKSUM”；证据是“POST-TRANSFER-INTEGRITY-VALIDATION-RESULT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00053` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-031-CDCCDED52C40`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `DATA-LOADER` / `WHEN-CHECKSUM-VALIDATION-FAILS` / `DO-NOT-FAIL-TFTP-TRANSFER-ON-CHECKSUM-VALIDATION-FAILURE` / `TFTP-TRANSFER, CHECKSUM-VALIDATION-FAILURE` / `ABSENCE-OF-CHECKSUM-CAUSED-TFTP-FAILURE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform DO-NOT-FAIL-TFTP-TRANSFER-ON-CHECKSUM-VALIDATION-FAILURE on TFTP-TRANSFER, CHECKSUM-VALIDATION-FAILURE under WHEN-CHECKSUM-VALIDATION-FAILS; evidence is the resulting ABSENCE-OF-CHECKSUM-CAUSED-TFTP-FAILURE-OBSERVABLE.<br>参与者“数据加载器”在“WHEN-CHECKSUM-VALIDATION-FAILS”下必须对“TFTP-TRANSFER、CHECKSUM-VALIDATION-FAILURE”执行“DO-NOT-FAIL-TFTP-TRANSFER-ON-CHECKSUM-VALIDATION-FAILURE”；证据是“ABSENCE-OF-CHECKSUM-CAUSED-TFTP-FAILURE-OBSERVABLE”。 | — | DEP-RFC-1350, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00054` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-032-C495B27D5E7B`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `DATA-LOADER` / `UNCONDITIONAL` / `VALIDATE` / `CRC, OPERATION` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform VALIDATE on CRC, OPERATION under UNCONDITIONAL; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下必须对“CRC／校验值、协议操作”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00055` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-033-54C31853DBBA`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `DATA-LOADER` / `UNCONDITIONAL` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform VALIDATE on CRC under UNCONDITIONAL; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00056` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-034-6BD83C2FA204`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `DATA-LOADER` / `UNCONDITIONAL` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER may perform VALIDATE on CRC under UNCONDITIONAL; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下可以对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00057` | `SU-ARINC-615A-3-5-3-2-3-8-6-P044-PROSE-SENTENCE-005-F74AC5B7AE1C`<br>`ARINC-615A-3 5.3.2.3.8.6 p.32` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `FAIL` / `OPERATION, TARGET-HARDWARE-ID` / `FAILURE-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE may perform FAIL on OPERATION, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting FAILURE-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下可以对“协议操作、TARGET-HARDWARE-ID”执行“判定失败”；证据是“失败结果可被观察”。 | — | — |
| `CRS-M1-00058` | `SU-ARINC-615A-3-5-3-2-3-8-6-P044-PROSE-SENTENCE-006-1813D605F404`<br>`ARINC-615A-3 5.3.2.3.8.6 p.32` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ASSIGN` / `NETWORK-INTERFACE` / `ASSIGN-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform ASSIGN on NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting ASSIGN-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“网络接口”执行“分配或管理”；证据是“ASSIGN-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00059` | `SU-ARINC-615A-3-5-3-2-3-9-P044-PROSE-SENTENCE-001-04EEB77FBE9B`<br>`ARINC-615A-3 5.3.2.3.9 p.32` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `COMPLY` / `TFTP-BLOCK-NUMBER` / `COMPLY-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform COMPLY on TFTP-BLOCK-NUMBER under UNCONDITIONAL; evidence is the resulting COMPLY-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“TFTP 块号”执行“符合”；证据是“COMPLY-RESULT-OBSERVABLE”。 | — | DEP-RFC-1350 |
| `CRS-M1-00060` | `SU-ARINC-615A-3-5-3-2-3-9-P044-PROSE-SENTENCE-003-17BB6DF8AFB6`<br>`ARINC-615A-3 5.3.2.3.9 p.32` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `ON-TFTP-BLOCK-NUMBER-OVERFLOW` / `SEND` / `TFTP-BLOCK-NUMBER` / `MESSAGE-OR-FILE-DIRECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform SEND on TFTP-BLOCK-NUMBER under ON-TFTP-BLOCK-NUMBER-OVERFLOW; evidence is the resulting MESSAGE-OR-FILE-DIRECTION-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“TFTP 块号溢出时”下必须对“TFTP 块号”执行“发送”；证据是“消息或文件及其方向可被观察”。 | — | — |
| `CRS-M1-00061` | `SU-ARINC-615A-3-5-4-1-P045-PROSE-SENTENCE-008-B50B97990D87`<br>`ARINC-615A-3 5.4.1 p.33` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `IMPLEMENT` / `NETWORK-INTERFACE, TARGET-HARDWARE-ID` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE may perform IMPLEMENT on NETWORK-INTERFACE, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下可以对“网络接口、TARGET-HARDWARE-ID”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00062` | `SU-ARINC-615A-3-5-4-1-P046-PROSE-SENTENCE-018-975659D827AD`<br>`ARINC-615A-3 5.4.1 p.34` | `DATA-LOADING-SYSTEM` / `FOR-OPERATIONS-ON-THE-SAME-TARGET-HARDWARE` / `ALLOW-ANY-ORDER-WHILE-SERIALIZING-PER-TARGET` / `OPERATIONS-PER-TARGET-HARDWARE` / `PER-TARGET-OPERATION-ORDER-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADING-SYSTEM shall perform ALLOW-ANY-ORDER-WHILE-SERIALIZING-PER-TARGET on OPERATIONS-PER-TARGET-HARDWARE under FOR-OPERATIONS-ON-THE-SAME-TARGET-HARDWARE; evidence is the resulting PER-TARGET-OPERATION-ORDER-OBSERVABLE.<br>参与者“DATA-LOADING-SYSTEM”在“FOR-OPERATIONS-ON-THE-SAME-TARGET-HARDWARE”下必须对“OPERATIONS-PER-TARGET-HARDWARE”执行“ALLOW-ANY-ORDER-WHILE-SERIALIZING-PER-TARGET”；证据是“PER-TARGET-OPERATION-ORDER-OBSERVABLE”。 | — | — |
| `CRS-M1-00063` | `SU-ARINC-615A-3-5-4-1-P046-PROSE-SENTENCE-019-E420E9678873`<br>`ARINC-615A-3 5.4.1 p.34` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ABORT` / `OPERATION` / `ABORT-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION may perform ABORT on OPERATION under UNCONDITIONAL; evidence is the resulting ABORT-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下可以对“协议操作”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00064` | `SU-ARINC-615A-3-5-4-1-P046-PROSE-SENTENCE-020-EB49BE04DB5C`<br>`ARINC-615A-3 5.4.1 p.34` | `DATA-LOADER` / `UNCONDITIONAL` / `IMPLEMENT` / `OPERATION` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform IMPLEMENT on OPERATION under UNCONDITIONAL; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下必须对“协议操作”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00065` | `SU-ARINC-615A-3-5-4-1-P046-PROSE-SENTENCE-021-B970B2F9D719`<br>`ARINC-615A-3 5.4.1 p.34` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `TRANSFER` / `OPERATION, FIND-SERVICE, TARGET-HARDWARE-ID` / `TRANSFER-OUTCOME-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform TRANSFER on OPERATION, FIND-SERVICE, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting TRANSFER-OUTCOME-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“协议操作、FIND-SERVICE、TARGET-HARDWARE-ID”执行“传输”；证据是“传输结果可被观察”。 | — | — |
| `CRS-M1-00066` | `SU-ARINC-615A-3-5-4-1-P046-PROSE-SENTENCE-021-B970B2F9D719`<br>`ARINC-615A-3 5.4.1 p.34` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `TRANSFER` / `OPERATION` / `TRANSFER-OUTCOME-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform TRANSFER on OPERATION under UNCONDITIONAL; evidence is the resulting TRANSFER-OUTCOME-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“协议操作”执行“传输”；证据是“传输结果可被观察”。 | — | — |
| `CRS-M1-00067` | `SU-ARINC-615A-3-5-4-1-P046-PROSE-SENTENCE-022-FC38D80A0B56`<br>`ARINC-615A-3 5.4.1 p.34` | `DATA-LOADER` / `UNCONDITIONAL` / `LOCATE` / `OPERATION, FIND-SERVICE` / `LOCATE-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER may perform LOCATE on OPERATION, FIND-SERVICE under UNCONDITIONAL; evidence is the resulting LOCATE-RESULT-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下可以对“协议操作、FIND-SERVICE”执行“定位”；证据是“LOCATE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00068` | `SU-ARINC-615A-3-5-4-1-P046-PROSE-SENTENCE-023-ED7AFF26DD5C`<br>`ARINC-615A-3 5.4.1 p.34` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `TRANSFER` / `OPERATION, NETWORK-INTERFACE` / `TRANSFER-OUTCOME-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform TRANSFER on OPERATION, NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting TRANSFER-OUTCOME-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“协议操作、网络接口”执行“传输”；证据是“传输结果可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00069` | `SU-ARINC-615A-3-5-4-1-P046-PROSE-SENTENCE-024-6B0F5F41DA4C`<br>`ARINC-615A-3 5.4.1 p.34` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ENCODE` / `OPERATION, NETWORK-INTERFACE` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform ENCODE on OPERATION, NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“协议操作、网络接口”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00070` | `SU-ARINC-615A-3-5-4-1-P047-PROSE-SENTENCE-025-9C4E3C2DEF6F`<br>`ARINC-615A-3 5.4.1 p.35` | `TARGET-HARDWARE` / `WHEN-OPTIONAL-CAPABILITY-IMPLEMENTED` / `IMPLEMENT` / `OPERATION, NETWORK-INTERFACE, TARGET-HARDWARE-ID` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform IMPLEMENT on OPERATION, NETWORK-INTERFACE, TARGET-HARDWARE-ID under WHEN-OPTIONAL-CAPABILITY-IMPLEMENTED; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“目标硬件”在“实现可选能力时”下必须对“协议操作、网络接口、TARGET-HARDWARE-ID”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00071` | `SU-ARINC-615A-3-5-4-2-P047-PROSE-SENTENCE-002-ECE0CBAF4A74`<br>`ARINC-615A-3 5.4.2 p.35` | `DATA-LOADER` / `UNCONDITIONAL` / `IMPLEMENT` / `OPERATION` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform IMPLEMENT on OPERATION under UNCONDITIONAL; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下必须对“协议操作”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00072` | `SU-ARINC-615A-3-5-4-2-P047-PROSE-SENTENCE-003-78F447EDB430`<br>`ARINC-615A-3 5.4.2 p.35` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `IMPLEMENT` / `OPERATION, TARGET-HARDWARE-ID` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform IMPLEMENT on OPERATION, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“协议操作、TARGET-HARDWARE-ID”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00073` | `SU-ARINC-615A-3-5-4-2-P047-PROSE-SENTENCE-021-2733DF1A1970`<br>`ARINC-615A-3 5.4.2 p.35` | `DATA-LOADER` / `UNCONDITIONAL` / `WAIT` / `CURRENT-STATUS` / `WAIT-BEHAVIOR-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform WAIT on CURRENT-STATUS under UNCONDITIONAL; evidence is the resulting WAIT-BEHAVIOR-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下必须对“CURRENT-STATUS”执行“等待”；证据是“等待行为可被观察”。 | — | — |
| `CRS-M1-00074` | `SU-ARINC-615A-3-5-4-2-P047-PROSE-SENTENCE-023-DD0255D27FB0`<br>`ARINC-615A-3 5.4.2 p.35` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `VALIDATE` / `TFTP-OPTION` / `VALIDATION-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-PARTICIPANT may perform VALIDATE on TFTP-OPTION under UNCONDITIONAL; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下可以对“TFTP 选项”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00075` | `SU-ARINC-615A-3-5-4-2-P047-PROSE-SENTENCE-024-12B60035E133`<br>`ARINC-615A-3 5.4.2 p.35` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `IMPLEMENT` / `TFTP-OPTION` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE may perform IMPLEMENT on TFTP-OPTION under UNCONDITIONAL; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下可以对“TFTP 选项”执行“提供能力”；证据是“能力可用性可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00076` | `SU-ARINC-615A-3-5-4-2-P047-PROSE-SENTENCE-025-3CF28DC21423`<br>`ARINC-615A-3 5.4.2 p.35` | `DATA-LOADER` / `UNCONDITIONAL` / `VALIDATE` / `CRC, NETWORK-INTERFACE` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform VALIDATE on CRC, NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下必须对“CRC／校验值、网络接口”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00077` | `SU-ARINC-615A-3-5-4-3-P047-PROSE-SENTENCE-002-ECE0CBAF4A74`<br>`ARINC-615A-3 5.4.3 p.35` | `DATA-LOADER` / `UNCONDITIONAL` / `IMPLEMENT` / `OPERATION` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor DATA-LOADER shall perform IMPLEMENT on OPERATION under UNCONDITIONAL; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下必须对“协议操作”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00078` | `SU-ARINC-615A-3-5-4-3-P047-PROSE-SENTENCE-003-78F447EDB430`<br>`ARINC-615A-3 5.4.3 p.35` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `IMPLEMENT` / `OPERATION, TARGET-HARDWARE-ID` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE shall perform IMPLEMENT on OPERATION, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“协议操作、TARGET-HARDWARE-ID”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00079` | `SU-ARINC-615A-3-5-4-3-P048-PROSE-SENTENCE-015-A6329164790D`<br>`ARINC-615A-3 5.4.3 p.36` | `TARGET-HARDWARE` / `WHEN-LOAD-LIST-ITEM-REJECTED` / `REJECT` / `LOAD-LIST, TARGET-HARDWARE-ID` / `REJECTION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE shall perform REJECT on LOAD-LIST, TARGET-HARDWARE-ID under WHEN-LOAD-LIST-ITEM-REJECTED; evidence is the resulting REJECTION-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“加载清单中任一项被拒绝时”下必须对“LOAD-LIST、TARGET-HARDWARE-ID”执行“拒绝”；证据是“拒绝结果可被观察”。 | — | — |
| `CRS-M1-00080` | `SU-ARINC-615A-3-5-4-3-P048-PROSE-SENTENCE-018-3233B1CC77D5`<br>`ARINC-615A-3 5.4.3 p.36` | `DATA-LOADER` / `UNCONDITIONAL` / `DISPLAY` / `CURRENT-STATUS` / `USER-INDICATION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor DATA-LOADER shall perform DISPLAY on CURRENT-STATUS under UNCONDITIONAL; evidence is the resulting USER-INDICATION-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下必须对“CURRENT-STATUS”执行“显示或通知”；证据是“用户提示可被观察”。 | — | — |
| `CRS-M1-00081` | `SU-ARINC-615A-3-5-4-3-P048-PROSE-SENTENCE-024-D550F67EB586`<br>`ARINC-615A-3 5.4.3 p.36` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `VALIDATE` / `TFTP-OPTION, NETWORK-INTERFACE` / `VALIDATION-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE may perform VALIDATE on TFTP-OPTION, NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下可以对“TFTP 选项、网络接口”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00082` | `SU-ARINC-615A-3-5-4-3-P048-PROSE-SENTENCE-026-F38D018C4499`<br>`ARINC-615A-3 5.4.3 p.36` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE shall perform VALIDATE on CRC under UNCONDITIONAL; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00083` | `SU-ARINC-615A-3-5-4-3-P048-PROSE-SENTENCE-027-E777A6D3DAC7`<br>`ARINC-615A-3 5.4.3 p.36` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `VALIDATE` / `TFTP-OPTION` / `VALIDATION-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE may perform VALIDATE on TFTP-OPTION under UNCONDITIONAL; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下可以对“TFTP 选项”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00084` | `SU-ARINC-615A-3-5-4-3-1-P048-PROSE-SENTENCE-004-AF732D243056`<br>`ARINC-615A-3 5.4.3.1 p.36` | `TARGET-HARDWARE` / `WHEN-EVALUATING-A-NEW-LOAD` / `RETAIN-CURRENT-DATA-FILE-PART-NUMBERS-FOR-NEW-LOAD-COMPARISON` / `CURRENT-INSTALLED-LOAD-PART-NUMBERS, NEW-LOAD-HEADER-PART-NUMBERS` / `RETAINED-PART-NUMBER-COMPARISON-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE shall perform RETAIN-CURRENT-DATA-FILE-PART-NUMBERS-FOR-NEW-LOAD-COMPARISON on CURRENT-INSTALLED-LOAD-PART-NUMBERS, NEW-LOAD-HEADER-PART-NUMBERS under WHEN-EVALUATING-A-NEW-LOAD; evidence is the resulting RETAINED-PART-NUMBER-COMPARISON-OBSERVABLE.<br>参与者“目标硬件”在“WHEN-EVALUATING-A-NEW-LOAD”下必须对“CURRENT-INSTALLED-LOAD-PART-NUMBERS、NEW-LOAD-HEADER-PART-NUMBERS”执行“RETAIN-CURRENT-DATA-FILE-PART-NUMBERS-FOR-NEW-LOAD-COMPARISON”；证据是“RETAINED-PART-NUMBER-COMPARISON-OBSERVABLE”。 | — | — |
| `CRS-M1-00085` | `SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-007-F209ABE1376B`<br>`ARINC-615A-3 5.4.3.1 p.37` | `SOFTWARE-PACKAGE-PRODUCER` / `UNCONDITIONAL` / `VALIDATE` / `CRC, SOFTWARE-PART` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor SOFTWARE-PACKAGE-PRODUCER shall perform VALIDATE on CRC, SOFTWARE-PART under UNCONDITIONAL; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“软件包生成方”在“UNCONDITIONAL”下必须对“CRC／校验值、软件加载件”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00086` | `SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-008-CDA43D6568CC`<br>`ARINC-615A-3 5.4.3.1 p.37` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `VALIDATE` / `CRC, FILE-CONTENT, TARGET-HARDWARE-ID` / `VALIDATION-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE may perform VALIDATE on CRC, FILE-CONTENT, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下可以对“CRC／校验值、FILE-CONTENT、TARGET-HARDWARE-ID”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00087` | `SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-010-F4624AC8DCB4`<br>`ARINC-615A-3 5.4.3.1 p.37` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENSURE-EQUALITY` / `LOAD-PART-NUMBER, CRC` / `ENSURE-EQUALITY-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ENSURE-EQUALITY on LOAD-PART-NUMBER, CRC under UNCONDITIONAL; evidence is the resulting ENSURE-EQUALITY-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“加载件号、CRC／校验值”执行“确保取值相等”；证据是“ENSURE-EQUALITY-RESULT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00088` | `SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-012-B2655A4BD5D6`<br>`ARINC-615A-3 5.4.3.1 p.37` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `FORMAT` / `FILE-CONTENT` / `ENCODED-FORMAT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform FORMAT on FILE-CONTENT under UNCONDITIONAL; evidence is the resulting ENCODED-FORMAT-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“FILE-CONTENT”执行“按规定格式化”；证据是“编码格式可被观察”。 | — | — |
| `CRS-M1-00089` | `SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-015-1FD87B87894F`<br>`ARINC-615A-3 5.4.3.1 p.37` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `SELECT` / `FILE-CONTENT` / `SELECT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform SELECT on FILE-CONTENT under UNCONDITIONAL; evidence is the resulting SELECT-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“FILE-CONTENT”执行“选择”；证据是“SELECT-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00090` | `SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-017-D6D20C0AE6D8`<br>`ARINC-615A-3 5.4.3.1 p.37` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `COMPILE-AND-LINK` / `FILE-CONTENT` / `COMPILE-AND-LINK-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform COMPILE-AND-LINK on FILE-CONTENT under UNCONDITIONAL; evidence is the resulting COMPILE-AND-LINK-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“FILE-CONTENT”执行“独立编译并链接”；证据是“COMPILE-AND-LINK-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00091` | `SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-018-7D1A5B42A8F9`<br>`ARINC-615A-3 5.4.3.1 p.37` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `DEFINE` / `FILE-CONTENT, PROGRAM-MEMORY-MAP` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform DEFINE on FILE-CONTENT, PROGRAM-MEMORY-MAP under UNCONDITIONAL; evidence is the resulting DEFINE-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“FILE-CONTENT、PROGRAM-MEMORY-MAP”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00092` | `SU-ARINC-615A-3-5-4-5-2-P053-PROSE-SENTENCE-008-6BD76320C0DE`<br>`ARINC-615A-3 5.4.5.2 p.41` | `DATA-LOADER` / `UNCONDITIONAL` / `ABORT` / `STATUS-FILE, TEXT-FIELD, OPERATION` / `ABORT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform ABORT on STATUS-FILE, TEXT-FIELD, OPERATION under UNCONDITIONAL; evidence is the resulting ABORT-RESULT-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下必须对“状态文件、文本字段、协议操作”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00093` | `SU-ARINC-615A-3-6-2-8-1-P057-PROSE-SENTENCE-001-B9AF73779529`<br>`ARINC-615A-3 6.2.8.1 p.45` | `TARGET-HARDWARE` / `ON-WAIT-MESSAGE-RECEIPT` / `RETRY` / `TARGET-HARDWARE-ID, PROTOCOL-MESSAGE` / `RETRY-ATTEMPT-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE shall perform RETRY on TARGET-HARDWARE-ID, PROTOCOL-MESSAGE under ON-WAIT-MESSAGE-RECEIPT; evidence is the resulting RETRY-ATTEMPT-OBSERVABLE.<br>参与者“目标硬件”在“收到 WAIT 消息时”下必须对“TARGET-HARDWARE-ID、PROTOCOL-MESSAGE”执行“重试”；证据是“重试尝试可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00094` | `SU-ARINC-615A-3-6-3-1-P063-PROSE-SENTENCE-010-EF2C1FAB94E9`<br>`ARINC-615A-3 6.3.1 p.51` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `DEFINE` / `STATUS-FILE` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform DEFINE on STATUS-FILE under UNCONDITIONAL; evidence is the resulting DEFINE-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“状态文件”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | `SYMBOLIC-SOURCE-PARAMETER` / `DLP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-001-E20DEE6A28B4, SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-002-68A6807BC6D8 | — |
| `CRS-M1-00095` | `SU-ARINC-615A-3-6-3-1-P063-PROSE-SENTENCE-014-46E366631127`<br>`ARINC-615A-3 6.3.1 p.51` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ENCODE` / `STATUS-FILE, NETWORK-INTERFACE, PROTOCOL-ERROR` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform ENCODE on STATUS-FILE, NETWORK-INTERFACE, PROTOCOL-ERROR under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“状态文件、网络接口、PROTOCOL-ERROR”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00096` | `SU-ARINC-615A-3-6-3-1-P063-PROSE-SENTENCE-015-FFB177F65B0A`<br>`ARINC-615A-3 6.3.1 p.51` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ABORT` / `ABORT-MESSAGE, STATUS-FILE, NETWORK-INTERFACE, TARGET-HARDWARE-ID` / `ABORT-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE may perform ABORT on ABORT-MESSAGE, STATUS-FILE, NETWORK-INTERFACE, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting ABORT-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下可以对“中止消息、状态文件、网络接口、TARGET-HARDWARE-ID”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00097` | `SU-ARINC-615A-3-6-3-1-P063-PROSE-SENTENCE-018-33F16CA0556B`<br>`ARINC-615A-3 6.3.1 p.51` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `SEND` / `STATUS-FILE, TIMEOUT-EXPIRY, LCL-TRANSFER` / `MESSAGE-OR-FILE-DIRECTION-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE may perform SEND on STATUS-FILE, TIMEOUT-EXPIRY, LCL-TRANSFER under UNCONDITIONAL; evidence is the resulting MESSAGE-OR-FILE-DIRECTION-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下可以对“状态文件、TIMEOUT-EXPIRY、LCL-TRANSFER”执行“发送”；证据是“消息或文件及其方向可被观察”。 | `SYMBOLIC-SOURCE-PARAMETER` / `DLP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-001-E20DEE6A28B4, SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-002-68A6807BC6D8 | — |
| `CRS-M1-00098` | `SU-ARINC-615A-3-6-3-1-P063-PROSE-SENTENCE-020-D27F9DB819AB`<br>`ARINC-615A-3 6.3.1 p.51` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `SEND` / `STATUS-FILE, TARGET-HARDWARE-ID` / `MESSAGE-OR-FILE-DIRECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform SEND on STATUS-FILE, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting MESSAGE-OR-FILE-DIRECTION-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“状态文件、TARGET-HARDWARE-ID”执行“发送”；证据是“消息或文件及其方向可被观察”。 | `SYMBOLIC-SOURCE-PARAMETER` / `DLP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-001-E20DEE6A28B4, SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-002-68A6807BC6D8 | — |
| `CRS-M1-00099` | `SU-ARINC-615A-3-6-3-1-P064-PROSE-SENTENCE-031-D8862D88C46E`<br>`ARINC-615A-3 6.3.1 p.52` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `WAIT` / `EXCEPTION-TIMER, OPERATION, TARGET-HARDWARE-ID` / `WAIT-BEHAVIOR-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform WAIT on EXCEPTION-TIMER, OPERATION, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting WAIT-BEHAVIOR-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“异常计时器、协议操作、TARGET-HARDWARE-ID”执行“等待”；证据是“等待行为可被观察”。 | `MESSAGE-CARRIED-PARAMETER` / `MESSAGE-TIMER-VALUE` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-TABLE-6_4_3-1-R006 | — |
| `CRS-M1-00100` | `SU-ARINC-615A-3-6-3-1-P064-PROSE-SENTENCE-032-E812AC346D09`<br>`ARINC-615A-3 6.3.1 p.52` | `TARGET-HARDWARE-SUPPLIER` / `UNCONDITIONAL` / `WAIT` / `EXCEPTION-TIMER, TARGET-HARDWARE-ID` / `WAIT-BEHAVIOR-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE-SUPPLIER shall perform WAIT on EXCEPTION-TIMER, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting WAIT-BEHAVIOR-OBSERVABLE.<br>参与者“目标硬件供应商”在“UNCONDITIONAL”下必须对“异常计时器、TARGET-HARDWARE-ID”执行“等待”；证据是“等待行为可被观察”。 | `MESSAGE-CARRIED-PARAMETER` / `MESSAGE-TIMER-VALUE` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-TABLE-6_4_3-1-R006 | — |
| `CRS-M1-00101` | `SU-ARINC-615A-3-6-3-1-P064-PROSE-SENTENCE-033-2765B9535D98`<br>`ARINC-615A-3 6.3.1 p.52` | `DATA-LOADER` / `AFTER-A-STATUS-FILE-DECLARES-AN-EXCEPTION-DELAY` / `RECEIVE-STATUS-BEFORE-DELAY-OR-ABORT-OPERATION` / `NEW-STATUS-FILE, EXCEPTION-DELAY, ACTIVE-OPERATION` / `STATUS-BEFORE-DEADLINE-OR-ABORT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform RECEIVE-STATUS-BEFORE-DELAY-OR-ABORT-OPERATION on NEW-STATUS-FILE, EXCEPTION-DELAY, ACTIVE-OPERATION under AFTER-A-STATUS-FILE-DECLARES-AN-EXCEPTION-DELAY; evidence is the resulting STATUS-BEFORE-DEADLINE-OR-ABORT-OBSERVABLE.<br>参与者“数据加载器”在“AFTER-A-STATUS-FILE-DECLARES-AN-EXCEPTION-DELAY”下必须对“NEW-STATUS-FILE、EXCEPTION-DELAY、ACTIVE-OPERATION”执行“RECEIVE-STATUS-BEFORE-DELAY-OR-ABORT-OPERATION”；证据是“STATUS-BEFORE-DEADLINE-OR-ABORT-OBSERVABLE”。 | `MESSAGE-CARRIED-PARAMETER` / `EXCEPTION-DELAY` / `STATUS-RECEIVED-BEFORE-EXCEPTION-DELAY-ELSE-OPERATION-ABORT` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-028-9597EE244FD7 | — |
| `CRS-M1-00102` | `SU-ARINC-615A-3-6-3-2-P067-PROSE-SENTENCE-020-43C35127F07F`<br>`ARINC-615A-3 6.3.2 p.55` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `DEFINE` / `STATUS-FILE` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform DEFINE on STATUS-FILE under UNCONDITIONAL; evidence is the resulting DEFINE-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“状态文件”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | `SYMBOLIC-SOURCE-PARAMETER` / `DLP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-001-E20DEE6A28B4, SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-002-68A6807BC6D8 | — |
| `CRS-M1-00103` | `SU-ARINC-615A-3-6-3-2-P067-PROSE-SENTENCE-022-9B7AA17CBAF6`<br>`ARINC-615A-3 6.3.2 p.55` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ENCODE` / `STATUS-FILE, NETWORK-INTERFACE, PROTOCOL-ERROR` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE shall perform ENCODE on STATUS-FILE, NETWORK-INTERFACE, PROTOCOL-ERROR under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“状态文件、网络接口、PROTOCOL-ERROR”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00104` | `SU-ARINC-615A-3-6-3-2-P067-PROSE-SENTENCE-023-AEFFB70E9596`<br>`ARINC-615A-3 6.3.2 p.55` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ABORT` / `ABORT-MESSAGE, STATUS-FILE, NETWORK-INTERFACE, TARGET-HARDWARE-ID` / `ABORT-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE may perform ABORT on ABORT-MESSAGE, STATUS-FILE, NETWORK-INTERFACE, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting ABORT-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下可以对“中止消息、状态文件、网络接口、TARGET-HARDWARE-ID”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00105` | `SU-ARINC-615A-3-6-3-2-P067-PROSE-SENTENCE-026-3B69FEC8B73B`<br>`ARINC-615A-3 6.3.2 p.55` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `TRANSFER` / `UPLOAD-THREAD` / `TRANSFER-OUTCOME-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE may perform TRANSFER on UPLOAD-THREAD under UNCONDITIONAL; evidence is the resulting TRANSFER-OUTCOME-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下可以对“UPLOAD-THREAD”执行“传输”；证据是“传输结果可被观察”。 | — | — |
| `CRS-M1-00106` | `SU-ARINC-615A-3-6-3-2-P068-PROSE-SENTENCE-038-D8862D88C46E`<br>`ARINC-615A-3 6.3.2 p.56` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `WAIT` / `EXCEPTION-TIMER, OPERATION, TARGET-HARDWARE-ID` / `WAIT-BEHAVIOR-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE shall perform WAIT on EXCEPTION-TIMER, OPERATION, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting WAIT-BEHAVIOR-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“异常计时器、协议操作、TARGET-HARDWARE-ID”执行“等待”；证据是“等待行为可被观察”。 | `MESSAGE-CARRIED-PARAMETER` / `MESSAGE-TIMER-VALUE` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-TABLE-6_4_3-1-R006 | — |
| `CRS-M1-00107` | `SU-ARINC-615A-3-6-3-2-P068-PROSE-SENTENCE-039-E812AC346D09`<br>`ARINC-615A-3 6.3.2 p.56` | `TARGET-HARDWARE-SUPPLIER` / `UNCONDITIONAL` / `WAIT` / `EXCEPTION-TIMER, TARGET-HARDWARE-ID` / `WAIT-BEHAVIOR-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE-SUPPLIER shall perform WAIT on EXCEPTION-TIMER, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting WAIT-BEHAVIOR-OBSERVABLE.<br>参与者“目标硬件供应商”在“UNCONDITIONAL”下必须对“异常计时器、TARGET-HARDWARE-ID”执行“等待”；证据是“等待行为可被观察”。 | `MESSAGE-CARRIED-PARAMETER` / `MESSAGE-TIMER-VALUE` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-TABLE-6_4_3-1-R006 | — |
| `CRS-M1-00108` | `SU-ARINC-615A-3-6-3-2-P068-PROSE-SENTENCE-040-2765B9535D98`<br>`ARINC-615A-3 6.3.2 p.56` | `DATA-LOADER` / `AFTER-A-STATUS-FILE-DECLARES-AN-EXCEPTION-DELAY` / `RECEIVE-STATUS-BEFORE-DELAY-OR-ABORT-OPERATION` / `NEW-STATUS-FILE, EXCEPTION-DELAY, ACTIVE-OPERATION` / `STATUS-BEFORE-DEADLINE-OR-ABORT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor DATA-LOADER shall perform RECEIVE-STATUS-BEFORE-DELAY-OR-ABORT-OPERATION on NEW-STATUS-FILE, EXCEPTION-DELAY, ACTIVE-OPERATION under AFTER-A-STATUS-FILE-DECLARES-AN-EXCEPTION-DELAY; evidence is the resulting STATUS-BEFORE-DEADLINE-OR-ABORT-OBSERVABLE.<br>参与者“数据加载器”在“AFTER-A-STATUS-FILE-DECLARES-AN-EXCEPTION-DELAY”下必须对“NEW-STATUS-FILE、EXCEPTION-DELAY、ACTIVE-OPERATION”执行“RECEIVE-STATUS-BEFORE-DELAY-OR-ABORT-OPERATION”；证据是“STATUS-BEFORE-DEADLINE-OR-ABORT-OBSERVABLE”。 | `MESSAGE-CARRIED-PARAMETER` / `EXCEPTION-DELAY` / `STATUS-RECEIVED-BEFORE-EXCEPTION-DELAY-ELSE-OPERATION-ABORT` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-028-9597EE244FD7 | — |
| `CRS-M1-00109` | `SU-ARINC-615A-3-6-3-2-P068-PROSE-SENTENCE-042-4C1D759A6B9A`<br>`ARINC-615A-3 6.3.2 p.56` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `SEND` / `STATUS-FILE, DATA-FILE, CRC` / `MESSAGE-OR-FILE-DIRECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform SEND on STATUS-FILE, DATA-FILE, CRC under UNCONDITIONAL; evidence is the resulting MESSAGE-OR-FILE-DIRECTION-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“状态文件、数据文件、CRC／校验值”执行“发送”；证据是“消息或文件及其方向可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00110` | `SU-ARINC-615A-3-6-3-5-P076-PROSE-SENTENCE-009-BF2F613AC35B`<br>`ARINC-615A-3 6.3.5 p.64` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ABORT` / `STATUS-FILE, TARGET-HARDWARE-ID` / `ABORT-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE may perform ABORT on STATUS-FILE, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting ABORT-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下可以对“状态文件、TARGET-HARDWARE-ID”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00111` | `SU-ARINC-615A-3-6-3-5-P076-PROSE-SENTENCE-011-5B38B1E3DBEF`<br>`ARINC-615A-3 6.3.5 p.64` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ABORT` / `STATUS-FILE, OPERATION, TARGET-HARDWARE-ID` / `ABORT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform ABORT on STATUS-FILE, OPERATION, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting ABORT-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“状态文件、协议操作、TARGET-HARDWARE-ID”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00112` | `SU-ARINC-615A-3-6-3-5-P076-PROSE-SENTENCE-012-EED68957A0BC`<br>`ARINC-615A-3 6.3.5 p.64` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ABORT` / `ABORT-MESSAGE, OPERATION, TARGET-HARDWARE-ID` / `ABORT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform ABORT on ABORT-MESSAGE, OPERATION, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting ABORT-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“中止消息、协议操作、TARGET-HARDWARE-ID”执行“中止”；证据是“中止结果可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00113` | `SU-ARINC-615A-3-6-3-5-P076-PROSE-SENTENCE-013-DEDC03B64B0A`<br>`ARINC-615A-3 6.3.5 p.64` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ABORT` / `STATUS-FILE, ERROR-MESSAGE, TARGET-HARDWARE-ID` / `ABORT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform ABORT on STATUS-FILE, ERROR-MESSAGE, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting ABORT-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“状态文件、错误消息、TARGET-HARDWARE-ID”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00114` | `SU-ARINC-615A-3-6-3-5-P076-PROSE-SENTENCE-015-DCA535962C3D`<br>`ARINC-615A-3 6.3.5 p.64` | `DATA-LOADER` / `UNCONDITIONAL` / `ABORT` / `ABORT-MESSAGE, OPERATION` / `ABORT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform ABORT on ABORT-MESSAGE, OPERATION under UNCONDITIONAL; evidence is the resulting ABORT-RESULT-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下必须对“中止消息、协议操作”执行“中止”；证据是“中止结果可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00115` | `SU-ARINC-615A-3-6-4-P077-PROSE-SENTENCE-005-1B24BCFF8198`<br>`ARINC-615A-3 6.4 p.65` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `SEND` / `PROTOCOL-VERSION, OPERATION, NETWORK-INTERFACE, TARGET-HARDWARE-ID` / `MESSAGE-OR-FILE-DIRECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform SEND on PROTOCOL-VERSION, OPERATION, NETWORK-INTERFACE, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting MESSAGE-OR-FILE-DIRECTION-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“协议版本、协议操作、网络接口、TARGET-HARDWARE-ID”执行“发送”；证据是“消息或文件及其方向可被观察”。 | — | — |
| `CRS-M1-00116` | `SU-ARINC-615A-3-6-4-P077-PROSE-SENTENCE-007-20EF70E6EF8B`<br>`ARINC-615A-3 6.4 p.65` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `IMPLEMENT` / `PROTOCOL-VERSION, OPERATION, TARGET-HARDWARE-ID` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform IMPLEMENT on PROTOCOL-VERSION, OPERATION, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“协议版本、协议操作、TARGET-HARDWARE-ID”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00117` | `SU-ARINC-615A-3-6-4-P077-PROSE-SENTENCE-010-5F21110D7E4B`<br>`ARINC-615A-3 6.4 p.65` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `DEFINE` / `PROTOCOL-VERSION, NETWORK-INTERFACE` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER shall perform DEFINE on PROTOCOL-VERSION, NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting DEFINE-RESULT-OBSERVABLE.<br>参与者“协议文件生成方”在“UNCONDITIONAL”下必须对“协议版本、网络接口”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00118` | `SU-ARINC-615A-3-6-4-P077-PROSE-SENTENCE-011-5625CA7DF2D3`<br>`ARINC-615A-3 6.4 p.65` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPTIONAL-CAPABILITY-IMPLEMENTED` / `IMPLEMENT` / `PROTOCOL-VERSION, NETWORK-INTERFACE` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER shall perform IMPLEMENT on PROTOCOL-VERSION, NETWORK-INTERFACE under WHEN-OPTIONAL-CAPABILITY-IMPLEMENTED; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“协议文件生成方”在“实现可选能力时”下必须对“协议版本、网络接口”执行“提供能力”；证据是“能力可用性可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00119` | `SU-ARINC-615A-3-6-4-P077-PROSE-SENTENCE-013-2FCCE7C4573B`<br>`ARINC-615A-3 6.4 p.65` | `DATA-LOADER` / `WHEN-OPTIONAL-CAPABILITY-IMPLEMENTED` / `ABORT` / `PROTOCOL-VERSION` / `ABORT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform ABORT on PROTOCOL-VERSION under WHEN-OPTIONAL-CAPABILITY-IMPLEMENTED; evidence is the resulting ABORT-RESULT-OBSERVABLE.<br>参与者“数据加载器”在“实现可选能力时”下必须对“协议版本”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00120` | `SU-ARINC-615A-3-6-4-P077-PROSE-SENTENCE-014-569F14A5E296`<br>`ARINC-615A-3 6.4 p.65` | `DATA-LOADER` / `WHEN-PROTOCOL-VERSIONS-DIFFER` / `ABORT` / `ABORT-MESSAGE, STATUS-FILE, PROTOCOL-VERSION, OPERATION` / `ABORT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform ABORT on ABORT-MESSAGE, STATUS-FILE, PROTOCOL-VERSION, OPERATION under WHEN-PROTOCOL-VERSIONS-DIFFER; evidence is the resulting ABORT-RESULT-OBSERVABLE.<br>参与者“数据加载器”在“协议版本不兼容时”下必须对“中止消息、状态文件、协议版本、协议操作”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00121` | `SU-ARINC-615A-3-6-4-P077-PROSE-SENTENCE-015-425EEC39D73C`<br>`ARINC-615A-3 6.4 p.65` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `PROTOCOL-VERSION` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER shall perform ENCODE on PROTOCOL-VERSION under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议文件生成方”在“UNCONDITIONAL”下必须对“协议版本”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00122` | `SU-ARINC-615A-3-6-4-P077-PROSE-SENTENCE-017-280B7BBBB75A`<br>`ARINC-615A-3 6.4 p.65` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform ENCODE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00123` | `SU-ARINC-615A-3-6-4-P078-PROSE-SENTENCE-019-70F6AB842538`<br>`ARINC-615A-3 6.4 p.66` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER may perform ENCODE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议文件生成方”在“UNCONDITIONAL”下可以对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00124` | `SU-ARINC-615A-3-6-4-1-P080-PROSE-SENTENCE-023-B30093B748E5`<br>`ARINC-615A-3 6.4.1 p.68` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ALLOW-PRINTABLE` / `TEXT-FIELD` / `ALLOW-PRINTABLE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ALLOW-PRINTABLE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ALLOW-PRINTABLE-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“仅允许可打印字符”；证据是“ALLOW-PRINTABLE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00125` | `SU-ARINC-615A-3-6-4-1-P080-PROSE-SENTENCE-023-B30093B748E5`<br>`ARINC-615A-3 6.4.1 p.68` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `EXCLUDE-CONTROL-CHARACTERS` / `TEXT-FIELD, CONTROL-CHARACTERS` / `CONTROL-CHARACTER-ABSENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER shall perform EXCLUDE-CONTROL-CHARACTERS on TEXT-FIELD, CONTROL-CHARACTERS under WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD; evidence is the resulting CONTROL-CHARACTER-ABSENCE-OBSERVABLE.<br>参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、CONTROL-CHARACTERS”执行“EXCLUDE-CONTROL-CHARACTERS”；证据是“CONTROL-CHARACTER-ABSENCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00126` | `SU-ARINC-615A-3-6-4-1-P080-PROSE-SENTENCE-023-B30093B748E5`<br>`ARINC-615A-3 6.4.1 p.68` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `LIMIT-TEXT-LENGTH-TO-255-CHARACTERS` / `TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS` / `TEXT-LENGTH-BOUND-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER shall perform LIMIT-TEXT-LENGTH-TO-255-CHARACTERS on TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS under WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD; evidence is the resulting TEXT-LENGTH-BOUND-OBSERVABLE.<br>参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、MAXIMUM-255-CHARACTERS、MAXIMUM-2040-BITS”执行“LIMIT-TEXT-LENGTH-TO-255-CHARACTERS”；证据是“TEXT-LENGTH-BOUND-OBSERVABLE”。 | — | — |
| `CRS-M1-00127` | `SU-ARINC-615A-3-6-4-1-P080-PROSE-SENTENCE-024-1532165AA3AE`<br>`ARINC-615A-3 6.4.1 p.68` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ENCODE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00128` | `SU-ARINC-615A-3-6-4-2-P081-PROSE-SENTENCE-018-7650772794FC`<br>`ARINC-615A-3 6.4.2 p.69` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ENCODE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00129` | `SU-ARINC-615A-3-6-4-2-P081-PROSE-SENTENCE-023-B016CF154BFD`<br>`ARINC-615A-3 6.4.2 p.69` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ENCODE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00130` | `SU-ARINC-615A-3-6-4-2-P081-PROSE-SENTENCE-030-B016CF154BFD`<br>`ARINC-615A-3 6.4.2 p.69` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ENCODE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00131` | `SU-ARINC-615A-3-6-4-2-P082-PROSE-SENTENCE-042-0D59A327A7CC`<br>`ARINC-615A-3 6.4.2 p.70` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ALLOW-PRINTABLE` / `TEXT-FIELD` / `ALLOW-PRINTABLE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ALLOW-PRINTABLE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ALLOW-PRINTABLE-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“仅允许可打印字符”；证据是“ALLOW-PRINTABLE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00132` | `SU-ARINC-615A-3-6-4-2-P082-PROSE-SENTENCE-042-0D59A327A7CC`<br>`ARINC-615A-3 6.4.2 p.70` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `EXCLUDE-CONTROL-CHARACTERS` / `TEXT-FIELD, CONTROL-CHARACTERS` / `CONTROL-CHARACTER-ABSENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER shall perform EXCLUDE-CONTROL-CHARACTERS on TEXT-FIELD, CONTROL-CHARACTERS under WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD; evidence is the resulting CONTROL-CHARACTER-ABSENCE-OBSERVABLE.<br>参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、CONTROL-CHARACTERS”执行“EXCLUDE-CONTROL-CHARACTERS”；证据是“CONTROL-CHARACTER-ABSENCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00133` | `SU-ARINC-615A-3-6-4-2-P082-PROSE-SENTENCE-042-0D59A327A7CC`<br>`ARINC-615A-3 6.4.2 p.70` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `LIMIT-TEXT-LENGTH-TO-255-CHARACTERS` / `TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS` / `TEXT-LENGTH-BOUND-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER shall perform LIMIT-TEXT-LENGTH-TO-255-CHARACTERS on TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS under WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD; evidence is the resulting TEXT-LENGTH-BOUND-OBSERVABLE.<br>参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、MAXIMUM-255-CHARACTERS、MAXIMUM-2040-BITS”执行“LIMIT-TEXT-LENGTH-TO-255-CHARACTERS”；证据是“TEXT-LENGTH-BOUND-OBSERVABLE”。 | — | — |
| `CRS-M1-00134` | `SU-ARINC-615A-3-6-4-2-P082-PROSE-SENTENCE-043-1532165AA3AE`<br>`ARINC-615A-3 6.4.2 p.70` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ENCODE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00135` | `SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-029-C2788AA6D18A`<br>`ARINC-615A-3 6.4.3 p.72` | `PROTOCOL-FILE-PRODUCER` / `WHEN-STATUS-CODE-IS-0002-OR-0004` / `ENCODE` / `STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER shall perform ENCODE on STATUS-CODE-CONDITIONAL-FIELD under WHEN-STATUS-CODE-IS-0002-OR-0004; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议文件生成方”在“状态码为 0x0002 或 0x0004 时”下必须对“STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00136` | `SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-034-65EBA86ACA77`<br>`ARINC-615A-3 6.4.3 p.72` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `PROVIDE` / `ESTIMATED-TIME, OPERATION` / `PROVIDE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform PROVIDE on ESTIMATED-TIME, OPERATION under UNCONDITIONAL; evidence is the resulting PROVIDE-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“预计时间、协议操作”执行“提供”；证据是“PROVIDE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00137` | `SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-037-98AB79F99A7B`<br>`ARINC-615A-3 6.4.3 p.72` | `TARGET-HARDWARE` / `WHEN-TIMER-VALUE-IS-NOT-PROVIDED` / `ENCODE` / `ESTIMATED-TIME, TARGET-HARDWARE-ID` / `ENCODED-FIELD-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform ENCODE on ESTIMATED-TIME, TARGET-HARDWARE-ID under WHEN-TIMER-VALUE-IS-NOT-PROVIDED; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“目标硬件”在“目标未提供计时值时”下必须对“预计时间、TARGET-HARDWARE-ID”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00138` | `SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-043-83077CACF0DC`<br>`ARINC-615A-3 6.4.3 p.72` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER may perform ENCODE on STATUS-CODE-CONDITIONAL-FIELD under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议文件生成方”在“UNCONDITIONAL”下可以对“STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00139` | `SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-045-1B483243E195`<br>`ARINC-615A-3 6.4.3 p.72` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ALLOW-PRINTABLE` / `TEXT-FIELD` / `ALLOW-PRINTABLE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ALLOW-PRINTABLE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ALLOW-PRINTABLE-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“仅允许可打印字符”；证据是“ALLOW-PRINTABLE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00140` | `SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-045-1B483243E195`<br>`ARINC-615A-3 6.4.3 p.72` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `EXCLUDE-CONTROL-CHARACTERS` / `TEXT-FIELD, CONTROL-CHARACTERS` / `CONTROL-CHARACTER-ABSENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER shall perform EXCLUDE-CONTROL-CHARACTERS on TEXT-FIELD, CONTROL-CHARACTERS under WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD; evidence is the resulting CONTROL-CHARACTER-ABSENCE-OBSERVABLE.<br>参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、CONTROL-CHARACTERS”执行“EXCLUDE-CONTROL-CHARACTERS”；证据是“CONTROL-CHARACTER-ABSENCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00141` | `SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-045-1B483243E195`<br>`ARINC-615A-3 6.4.3 p.72` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `LIMIT-TEXT-LENGTH-TO-255-CHARACTERS` / `TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS` / `TEXT-LENGTH-BOUND-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER shall perform LIMIT-TEXT-LENGTH-TO-255-CHARACTERS on TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS under WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD; evidence is the resulting TEXT-LENGTH-BOUND-OBSERVABLE.<br>参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、MAXIMUM-255-CHARACTERS、MAXIMUM-2040-BITS”执行“LIMIT-TEXT-LENGTH-TO-255-CHARACTERS”；证据是“TEXT-LENGTH-BOUND-OBSERVABLE”。 | — | — |
| `CRS-M1-00142` | `SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-046-1532165AA3AE`<br>`ARINC-615A-3 6.4.3 p.72` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ENCODE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00143` | `SU-ARINC-615A-3-6-4-4-P085-PROSE-SENTENCE-013-D5E44774D202`<br>`ARINC-615A-3 6.4.4 p.73` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `HEADER-FILE, LUR` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor PROTOCOL-FILE-PRODUCER shall perform ENCODE on HEADER-FILE, LUR under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议文件生成方”在“UNCONDITIONAL”下必须对“头文件、LUR”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00144` | `SU-ARINC-615A-3-6-4-4-P085-PROSE-SENTENCE-018-1532165AA3AE`<br>`ARINC-615A-3 6.4.4 p.73` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ENCODE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00145` | `SU-ARINC-615A-3-6-4-4-P085-PROSE-SENTENCE-023-53AAFA003A8B`<br>`ARINC-615A-3 6.4.4 p.73` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ALLOW-PRINTABLE` / `TEXT-FIELD` / `ALLOW-PRINTABLE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ALLOW-PRINTABLE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ALLOW-PRINTABLE-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“仅允许可打印字符”；证据是“ALLOW-PRINTABLE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00146` | `SU-ARINC-615A-3-6-4-4-P085-PROSE-SENTENCE-023-53AAFA003A8B`<br>`ARINC-615A-3 6.4.4 p.73` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `EXCLUDE-CONTROL-CHARACTERS` / `TEXT-FIELD, CONTROL-CHARACTERS` / `CONTROL-CHARACTER-ABSENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor PROTOCOL-FILE-PRODUCER shall perform EXCLUDE-CONTROL-CHARACTERS on TEXT-FIELD, CONTROL-CHARACTERS under WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD; evidence is the resulting CONTROL-CHARACTER-ABSENCE-OBSERVABLE.<br>参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、CONTROL-CHARACTERS”执行“EXCLUDE-CONTROL-CHARACTERS”；证据是“CONTROL-CHARACTER-ABSENCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00147` | `SU-ARINC-615A-3-6-4-4-P085-PROSE-SENTENCE-023-53AAFA003A8B`<br>`ARINC-615A-3 6.4.4 p.73` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `LIMIT-TEXT-LENGTH-TO-255-CHARACTERS` / `TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS` / `TEXT-LENGTH-BOUND-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor PROTOCOL-FILE-PRODUCER shall perform LIMIT-TEXT-LENGTH-TO-255-CHARACTERS on TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS under WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD; evidence is the resulting TEXT-LENGTH-BOUND-OBSERVABLE.<br>参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、MAXIMUM-255-CHARACTERS、MAXIMUM-2040-BITS”执行“LIMIT-TEXT-LENGTH-TO-255-CHARACTERS”；证据是“TEXT-LENGTH-BOUND-OBSERVABLE”。 | — | — |
| `CRS-M1-00148` | `SU-ARINC-615A-3-6-4-4-P085-PROSE-SENTENCE-024-1532165AA3AE`<br>`ARINC-615A-3 6.4.4 p.73` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ENCODE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00149` | `SU-ARINC-615A-3-6-4-5-P087-PROSE-SENTENCE-028-44AE34DB0ED5`<br>`ARINC-615A-3 6.4.5 p.75` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | Actor PROTOCOL-FILE-PRODUCER may perform ENCODE on STATUS-CODE-CONDITIONAL-FIELD under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议文件生成方”在“UNCONDITIONAL”下可以对“STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00150` | `SU-ARINC-615A-3-6-4-5-P087-PROSE-SENTENCE-030-1B483243E195`<br>`ARINC-615A-3 6.4.5 p.75` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ALLOW-PRINTABLE` / `TEXT-FIELD` / `ALLOW-PRINTABLE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ALLOW-PRINTABLE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ALLOW-PRINTABLE-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“仅允许可打印字符”；证据是“ALLOW-PRINTABLE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00151` | `SU-ARINC-615A-3-6-4-5-P087-PROSE-SENTENCE-030-1B483243E195`<br>`ARINC-615A-3 6.4.5 p.75` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `EXCLUDE-CONTROL-CHARACTERS` / `TEXT-FIELD, CONTROL-CHARACTERS` / `CONTROL-CHARACTER-ABSENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor PROTOCOL-FILE-PRODUCER shall perform EXCLUDE-CONTROL-CHARACTERS on TEXT-FIELD, CONTROL-CHARACTERS under WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD; evidence is the resulting CONTROL-CHARACTER-ABSENCE-OBSERVABLE.<br>参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、CONTROL-CHARACTERS”执行“EXCLUDE-CONTROL-CHARACTERS”；证据是“CONTROL-CHARACTER-ABSENCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00152` | `SU-ARINC-615A-3-6-4-5-P087-PROSE-SENTENCE-030-1B483243E195`<br>`ARINC-615A-3 6.4.5 p.75` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `LIMIT-TEXT-LENGTH-TO-255-CHARACTERS` / `TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS` / `TEXT-LENGTH-BOUND-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor PROTOCOL-FILE-PRODUCER shall perform LIMIT-TEXT-LENGTH-TO-255-CHARACTERS on TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS under WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD; evidence is the resulting TEXT-LENGTH-BOUND-OBSERVABLE.<br>参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、MAXIMUM-255-CHARACTERS、MAXIMUM-2040-BITS”执行“LIMIT-TEXT-LENGTH-TO-255-CHARACTERS”；证据是“TEXT-LENGTH-BOUND-OBSERVABLE”。 | — | — |
| `CRS-M1-00153` | `SU-ARINC-615A-3-6-4-5-P087-PROSE-SENTENCE-031-1532165AA3AE`<br>`ARINC-615A-3 6.4.5 p.75` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ENCODE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00154` | `SU-ARINC-615A-3-6-4-5-P088-PROSE-SENTENCE-040-B5C9724D1870`<br>`ARINC-615A-3 6.4.5 p.76` | `PROTOCOL-FILE-PRODUCER` / `WHEN-STATUS-CODE-IS-0002-OR-0004` / `ENCODE` / `STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | Actor PROTOCOL-FILE-PRODUCER shall perform ENCODE on STATUS-CODE-CONDITIONAL-FIELD under WHEN-STATUS-CODE-IS-0002-OR-0004; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议文件生成方”在“状态码为 0x0002 或 0x0004 时”下必须对“STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00155` | `SU-ARINC-615A-3-6-4-5-P088-PROSE-SENTENCE-045-19508B8A4FBD`<br>`ARINC-615A-3 6.4.5 p.76` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `PROVIDE` / `ESTIMATED-TIME, OPERATION, TARGET-HARDWARE-ID` / `PROVIDE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE shall perform PROVIDE on ESTIMATED-TIME, OPERATION, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting PROVIDE-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“预计时间、协议操作、TARGET-HARDWARE-ID”执行“提供”；证据是“PROVIDE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00156` | `SU-ARINC-615A-3-6-4-5-P088-PROSE-SENTENCE-048-394FB8F92672`<br>`ARINC-615A-3 6.4.5 p.76` | `TARGET-HARDWARE` / `WHEN-TIMER-VALUE-IS-NOT-PROVIDED` / `ENCODE` / `ESTIMATED-TIME, TARGET-HARDWARE-ID` / `ENCODED-FIELD-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE shall perform ENCODE on ESTIMATED-TIME, TARGET-HARDWARE-ID under WHEN-TIMER-VALUE-IS-NOT-PROVIDED; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“目标硬件”在“目标未提供计时值时”下必须对“预计时间、TARGET-HARDWARE-ID”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00157` | `SU-ARINC-615A-3-6-4-5-P088-PROSE-SENTENCE-054-628FD5E1362E`<br>`ARINC-615A-3 6.4.5 p.76` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `HEADER-FILE` / `ENCODED-FIELD-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | Actor PROTOCOL-FILE-PRODUCER shall perform ENCODE on HEADER-FILE under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议文件生成方”在“UNCONDITIONAL”下必须对“头文件”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00158` | `SU-ARINC-615A-3-6-4-5-P088-PROSE-SENTENCE-059-1532165AA3AE`<br>`ARINC-615A-3 6.4.5 p.76` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ENCODE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00159` | `SU-ARINC-615A-3-6-4-5-P089-PROSE-SENTENCE-064-1532165AA3AE`<br>`ARINC-615A-3 6.4.5 p.77` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ENCODE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00160` | `SU-ARINC-615A-3-6-4-5-P090-PROSE-SENTENCE-089-19FE3D2863DD`<br>`ARINC-615A-3 6.4.5 p.78` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | Actor PROTOCOL-FILE-PRODUCER may perform ENCODE on STATUS-CODE-CONDITIONAL-FIELD under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议文件生成方”在“UNCONDITIONAL”下可以对“STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00161` | `SU-ARINC-615A-3-6-4-5-P090-PROSE-SENTENCE-091-B30093B748E5`<br>`ARINC-615A-3 6.4.5 p.78` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ALLOW-PRINTABLE` / `TEXT-FIELD` / `ALLOW-PRINTABLE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ALLOW-PRINTABLE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ALLOW-PRINTABLE-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“仅允许可打印字符”；证据是“ALLOW-PRINTABLE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00162` | `SU-ARINC-615A-3-6-4-5-P090-PROSE-SENTENCE-091-B30093B748E5`<br>`ARINC-615A-3 6.4.5 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `EXCLUDE-CONTROL-CHARACTERS` / `TEXT-FIELD, CONTROL-CHARACTERS` / `CONTROL-CHARACTER-ABSENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor PROTOCOL-FILE-PRODUCER shall perform EXCLUDE-CONTROL-CHARACTERS on TEXT-FIELD, CONTROL-CHARACTERS under WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD; evidence is the resulting CONTROL-CHARACTER-ABSENCE-OBSERVABLE.<br>参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、CONTROL-CHARACTERS”执行“EXCLUDE-CONTROL-CHARACTERS”；证据是“CONTROL-CHARACTER-ABSENCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00163` | `SU-ARINC-615A-3-6-4-5-P090-PROSE-SENTENCE-091-B30093B748E5`<br>`ARINC-615A-3 6.4.5 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `LIMIT-TEXT-LENGTH-TO-255-CHARACTERS` / `TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS` / `TEXT-LENGTH-BOUND-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor PROTOCOL-FILE-PRODUCER shall perform LIMIT-TEXT-LENGTH-TO-255-CHARACTERS on TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS under WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD; evidence is the resulting TEXT-LENGTH-BOUND-OBSERVABLE.<br>参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、MAXIMUM-255-CHARACTERS、MAXIMUM-2040-BITS”执行“LIMIT-TEXT-LENGTH-TO-255-CHARACTERS”；证据是“TEXT-LENGTH-BOUND-OBSERVABLE”。 | — | — |
| `CRS-M1-00164` | `SU-ARINC-615A-3-6-4-5-P090-PROSE-SENTENCE-092-1532165AA3AE`<br>`ARINC-615A-3 6.4.5 p.78` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | Actor ARINC-615A-PROTOCOL-PARTICIPANT shall perform ENCODE on TEXT-FIELD under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00165` | `SU-ARINC-615A-3-6-4-10-P096-PROSE-SENTENCE-001-2C9653D1AE20`<br>`ARINC-615A-3 6.4.10 p.84` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `DISPLAY` / `TEXT-FIELD, TARGET-HARDWARE-ID` / `USER-INDICATION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform DISPLAY on TEXT-FIELD, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting USER-INDICATION-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“文本字段、TARGET-HARDWARE-ID”执行“显示或通知”；证据是“用户提示可被观察”。 | — | — |
| `CRS-M1-00166` | `SU-ARINC-615A-3-6-4-10-P097-PROSE-SENTENCE-002-5D81ED14D19B`<br>`ARINC-615A-3 6.4.10 p.85` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `WAIT` / `NETWORK-INTERFACE, TARGET-HARDWARE-ID` / `WAIT-BEHAVIOR-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform WAIT on NETWORK-INTERFACE, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting WAIT-BEHAVIOR-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“网络接口、TARGET-HARDWARE-ID”执行“等待”；证据是“等待行为可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00167` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-005-D75104E5A8FF`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `RETRY` / `TIMEOUT-AND-RETRY-LAYERS` / `RETRY-ATTEMPT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform RETRY on TIMEOUT-AND-RETRY-LAYERS under UNCONDITIONAL; evidence is the resulting RETRY-ATTEMPT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“TIMEOUT-AND-RETRY-LAYERS”执行“重试”；证据是“重试尝试可被观察”。 | — | — |
| `CRS-M1-00168` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-009-F320813241E5`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `TRANSFER` / `TFTP-FILE-TRANSFER` / `TRANSFER-OUTCOME-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform TRANSFER on TFTP-FILE-TRANSFER under UNCONDITIONAL; evidence is the resulting TRANSFER-OUTCOME-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“TFTP 文件传输”执行“传输”；证据是“传输结果可被观察”。 | `SYMBOLIC-SOURCE-PARAMETER` / `TFTP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-4-3-1-P112-PROSE-SENTENCE-001-97BE648C2E96, SU-ARINC-615A-3-4-3-1-P112-PROSE-SENTENCE-002-E2A9490FA667 | DEP-RFC-1350 |
| `CRS-M1-00169` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-010-414439744FBA`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ACKNOWLEDGE` / `TIMEOUT-EXPIRY` / `ACKNOWLEDGE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform ACKNOWLEDGE on TIMEOUT-EXPIRY under UNCONDITIONAL; evidence is the resulting ACKNOWLEDGE-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“TIMEOUT-EXPIRY”执行“确认”；证据是“ACKNOWLEDGE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00170` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-012-D951F3C8D8DC`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `RETRY` / `TFTP-FILE-TRANSFER` / `RETRY-ATTEMPT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION may perform RETRY on TFTP-FILE-TRANSFER under UNCONDITIONAL; evidence is the resulting RETRY-ATTEMPT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下可以对“TFTP 文件传输”执行“重试”；证据是“重试尝试可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00171` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-013-DCEA052A12C5`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `AFTER-RETRY-LIMIT-EXHAUSTION` / `RETRY` / `TFTP-FILE-TRANSFER, RETRY-NUMBER` / `RETRY-ATTEMPT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform RETRY on TFTP-FILE-TRANSFER, RETRY-NUMBER under AFTER-RETRY-LIMIT-EXHAUSTION; evidence is the resulting RETRY-ATTEMPT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“重试限额耗尽后”下必须对“TFTP 文件传输、RETRY-NUMBER”执行“重试”；证据是“重试尝试可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00172` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-014-0E511BD5A2AE`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `PROVIDE` / `PROTOCOL-ERROR` / `PROVIDE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform PROVIDE on PROTOCOL-ERROR under UNCONDITIONAL; evidence is the resulting PROVIDE-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“PROTOCOL-ERROR”执行“提供”；证据是“PROVIDE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00173` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-017-7C1E9A3C2D05`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `ON-TFTP-ERROR` / `RETRY` / `TFTP-FILE-TRANSFER` / `RETRY-ATTEMPT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform RETRY on TFTP-FILE-TRANSFER under ON-TFTP-ERROR; evidence is the resulting RETRY-ATTEMPT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“TFTP 层报告错误时”下必须对“TFTP 文件传输”执行“重试”；证据是“重试尝试可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00174` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-019-F7B55A457FA5`<br>`ARINC-615A-3 4-1 p.99` | `DLP-CLIENT` / `AFTER-DLP-RETRY-LIMIT-IS-EXCEEDED-AND-ERROR-PERSISTS` / `DECLARE-FATAL-ERROR` / `DLP-FILE-TRANSFER` / `FATAL-ERROR-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLP-CLIENT shall perform DECLARE-FATAL-ERROR on DLP-FILE-TRANSFER under AFTER-DLP-RETRY-LIMIT-IS-EXCEEDED-AND-ERROR-PERSISTS; evidence is the resulting FATAL-ERROR-RESULT-OBSERVABLE.<br>参与者“DLP-CLIENT”在“AFTER-DLP-RETRY-LIMIT-IS-EXCEEDED-AND-ERROR-PERSISTS”下必须对“DLP-FILE-TRANSFER”执行“DECLARE-FATAL-ERROR”；证据是“FATAL-ERROR-RESULT-OBSERVABLE”。 | — | DEP-RFC-1350 |
| `CRS-M1-00175` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-020-C80348B18729`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `FAIL` / `PROTOCOL-ERROR` / `FAILURE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform FAIL on PROTOCOL-ERROR under UNCONDITIONAL; evidence is the resulting FAILURE-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“PROTOCOL-ERROR”执行“判定失败”；证据是“失败结果可被观察”。 | — | — |
| `CRS-M1-00176` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-028-35890C54B368`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ADJUST-UPWARD` / `TIMEOUT-VALUE` / `ADJUST-UPWARD-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform ADJUST-UPWARD on TIMEOUT-VALUE under UNCONDITIONAL; evidence is the resulting ADJUST-UPWARD-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“TIMEOUT-VALUE”执行“向上调整”；证据是“ADJUST-UPWARD-RESULT-OBSERVABLE”。 | `SYMBOLIC-SOURCE-PARAMETER` / `DLP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-001-E20DEE6A28B4, SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-002-68A6807BC6D8 | — |
| `CRS-M1-00177` | `SU-ARINC-615A-3-4-3-1-P112-PROSE-SENTENCE-004-4C05C3174D37`<br>`ARINC-615A-3 4-3.1 p.100` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `SET-CONSTANT` / `TIMEOUT-VALUE` / `CONSTANT-VALUE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform SET-CONSTANT on TIMEOUT-VALUE under UNCONDITIONAL; evidence is the resulting CONSTANT-VALUE-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“TIMEOUT-VALUE”执行“设置固定常数”；证据是“固定取值可被观察”。 | `FIXED-SOURCE-CONSTANT` / `TFTP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `2..2 s` / evidence: SU-ARINC-615A-3-4-3-1-P112-PROSE-SENTENCE-004-4C05C3174D37 | — |
| `CRS-M1-00178` | `SU-ARINC-615A-3-4-3-1-P112-PROSE-SENTENCE-005-88F51ABD3389`<br>`ARINC-615A-3 4-3.1 p.100` | `NETWORK-PATH` / `DURING-ONE-TFTP-PACKET-NETWORK-TRANSFER` / `LIMIT-SINGLE-TFTP-PACKET-TRANSMISSION-DURATION` / `SINGLE-TFTP-PACKET, TFTP-TO-DIVIDED-BY-4` / `PACKET-TRANSMISSION-DURATION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor NETWORK-PATH shall perform LIMIT-SINGLE-TFTP-PACKET-TRANSMISSION-DURATION on SINGLE-TFTP-PACKET, TFTP-TO-DIVIDED-BY-4 under DURING-ONE-TFTP-PACKET-NETWORK-TRANSFER; evidence is the resulting PACKET-TRANSMISSION-DURATION-OBSERVABLE.<br>参与者“NETWORK-PATH”在“DURING-ONE-TFTP-PACKET-NETWORK-TRANSFER”下必须对“SINGLE-TFTP-PACKET、TFTP-TO-DIVIDED-BY-4”执行“LIMIT-SINGLE-TFTP-PACKET-TRANSMISSION-DURATION”；证据是“PACKET-TRANSMISSION-DURATION-OBSERVABLE”。 | `SYMBOLIC-SOURCE-EQUATION` / `TFTP-TO-DIVIDED-BY-4` / `PACKET-TRANSMISSION-DURATION<=TFTP-TO/4` / `0..TFTP-TO-DIVIDED-BY-4 s` / evidence: SU-ARINC-615A-3-A4-3-1-P112-EQUATION-001 | DEP-RFC-1350 |
| `CRS-M1-00179` | `SU-ARINC-615A-3-4-3-1-P112-PROSE-SENTENCE-007-69549032F30B`<br>`ARINC-615A-3 4-3.1 p.100` | `TFTP-SUBSCRIBER` / `BETWEEN-TFTP-PACKET-RECEPTION-AND-ASSOCIATED-PACKET-EMISSION` / `LIMIT-TFTP-PACKET-PROCESSING-DURATION` / `RECEIVED-TFTP-PACKET, ASSOCIATED-EMITTED-PACKET, TFTP-TO-DIVIDED-BY-2` / `SUBSCRIBER-PROCESSING-DURATION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TFTP-SUBSCRIBER shall perform LIMIT-TFTP-PACKET-PROCESSING-DURATION on RECEIVED-TFTP-PACKET, ASSOCIATED-EMITTED-PACKET, TFTP-TO-DIVIDED-BY-2 under BETWEEN-TFTP-PACKET-RECEPTION-AND-ASSOCIATED-PACKET-EMISSION; evidence is the resulting SUBSCRIBER-PROCESSING-DURATION-OBSERVABLE.<br>参与者“TFTP-SUBSCRIBER”在“BETWEEN-TFTP-PACKET-RECEPTION-AND-ASSOCIATED-PACKET-EMISSION”下必须对“RECEIVED-TFTP-PACKET、ASSOCIATED-EMITTED-PACKET、TFTP-TO-DIVIDED-BY-2”执行“LIMIT-TFTP-PACKET-PROCESSING-DURATION”；证据是“SUBSCRIBER-PROCESSING-DURATION-OBSERVABLE”。 | `SYMBOLIC-SOURCE-EQUATION` / `TFTP-TO-DIVIDED-BY-2` / `SUBSCRIBER-PROCESSING-DURATION<=TFTP-TO/2` / `0..TFTP-TO-DIVIDED-BY-2 s` / evidence: SU-ARINC-615A-3-A4-3-1-P112-EQUATION-002 | DEP-RFC-1350 |
| `CRS-M1-00180` | `SU-ARINC-615A-3-4-3-2-P113-PROSE-SENTENCE-001-205BD6EF24F3`<br>`ARINC-615A-3 4-3.2 p.101` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `RETRY` / `TFTP-EXCHANGE, RETRY-NUMBER, TARGET-HARDWARE-ID` / `RETRY-ATTEMPT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE may perform RETRY on TFTP-EXCHANGE, RETRY-NUMBER, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting RETRY-ATTEMPT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下可以对“TFTP 交换、RETRY-NUMBER、TARGET-HARDWARE-ID”执行“重试”；证据是“重试尝试可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00181` | `SU-ARINC-615A-3-4-3-2-P113-PROSE-SENTENCE-011-A604F56F9739`<br>`ARINC-615A-3 4-3.2 p.101` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `RETRY` / `RETRY-NUMBER` / `RETRY-ATTEMPT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform RETRY on RETRY-NUMBER under UNCONDITIONAL; evidence is the resulting RETRY-ATTEMPT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“RETRY-NUMBER”执行“重试”；证据是“重试尝试可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00182` | `SU-ARINC-615A-3-4-3-3-P114-PROSE-SENTENCE-001-5174295F548B`<br>`ARINC-615A-3 4-3.3 p.102` | `PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ENCODE` / `SORCERERS-APPRENTICE-FIX` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-IMPLEMENTATION shall perform ENCODE on SORCERERS-APPRENTICE-FIX under UNCONDITIONAL; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议实现”在“UNCONDITIONAL”下必须对“SORCERERS-APPRENTICE-FIX”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | DEP-RFC-1123, DEP-RFC-1350 |
| `CRS-M1-00183` | `SU-ARINC-615A-3-4-3-3-P114-PROSE-SENTENCE-002-889533B1AA3F`<br>`ARINC-615A-3 4-3.3 p.102` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `ON-DUPLICATE-ACKNOWLEDGEMENT` / `SEND` / `TFTP-EXCHANGE, NETWORK-INTERFACE` / `MESSAGE-OR-FILE-DIRECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform SEND on TFTP-EXCHANGE, NETWORK-INTERFACE under ON-DUPLICATE-ACKNOWLEDGEMENT; evidence is the resulting MESSAGE-OR-FILE-DIRECTION-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“收到重复确认时”下必须对“TFTP 交换、网络接口”执行“发送”；证据是“消息或文件及其方向可被观察”。 | — | — |
| `CRS-M1-00184` | `SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-003-7C29399D1DAB`<br>`ARINC-615A-3 4-4.1 p.102` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `TRANSFER` / `TFTP-FILE-TRANSFER` / `TRANSFER-OUTCOME-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform TRANSFER on TFTP-FILE-TRANSFER under UNCONDITIONAL; evidence is the resulting TRANSFER-OUTCOME-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“TFTP 文件传输”执行“传输”；证据是“传输结果可被观察”。 | `SYMBOLIC-SOURCE-PARAMETER` / `DLP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-001-E20DEE6A28B4, SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-002-68A6807BC6D8 | DEP-RFC-1350 |
| `CRS-M1-00185` | `SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-006-02C6AA3F66A1`<br>`ARINC-615A-3 4-4.1 p.102` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ADJUST-UPWARD` / `TIMEOUT-VALUE` / `ADJUST-UPWARD-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-PROTOCOL-IMPLEMENTATION shall perform ADJUST-UPWARD on TIMEOUT-VALUE under UNCONDITIONAL; evidence is the resulting ADJUST-UPWARD-RESULT-OBSERVABLE.<br>参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“TIMEOUT-VALUE”执行“向上调整”；证据是“ADJUST-UPWARD-RESULT-OBSERVABLE”。 | `SYMBOLIC-SOURCE-PARAMETER` / `DLP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-001-E20DEE6A28B4, SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-002-68A6807BC6D8 | — |
| `CRS-M1-00186` | `SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-008-4848608477C0`<br>`ARINC-615A-3 4-4.1 p.102` | `TARGET-HARDWARE` / `WHEN-LCI-LCL-STARTS-BEFORE-DLP-TO-EXPIRY` / `DO-NOT-PRODUCE-LCS-DURING-TIMELY-LCI-LCL-SEQUENCE` / `LCI-LCL-SEQUENCE, DLP-TO, LCS-STATUS-FILE` / `ABSENCE-OF-LCS-BEFORE-DLP-DEADLINE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform DO-NOT-PRODUCE-LCS-DURING-TIMELY-LCI-LCL-SEQUENCE on LCI-LCL-SEQUENCE, DLP-TO, LCS-STATUS-FILE under WHEN-LCI-LCL-STARTS-BEFORE-DLP-TO-EXPIRY; evidence is the resulting ABSENCE-OF-LCS-BEFORE-DLP-DEADLINE-OBSERVABLE.<br>参与者“目标硬件”在“WHEN-LCI-LCL-STARTS-BEFORE-DLP-TO-EXPIRY”下必须对“LCI-LCL-SEQUENCE、DLP-TO、LCS-STATUS-FILE”执行“DO-NOT-PRODUCE-LCS-DURING-TIMELY-LCI-LCL-SEQUENCE”；证据是“ABSENCE-OF-LCS-BEFORE-DLP-DEADLINE-OBSERVABLE”。 | `SYMBOLIC-SOURCE-PARAMETER` / `DLP-TO` / `LCI-LCL-START<DLP-TO-EXPIRY=>ABSENT(LCS)` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-001-E20DEE6A28B4, SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-002-68A6807BC6D8 | — |
| `CRS-M1-00187` | `SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-011-BD0CBB7058D1`<br>`ARINC-615A-3 4-4.1 p.102` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `PROVIDE` / `TIMEOUT-VALUE, TARGET-HARDWARE-ID` / `PROVIDE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform PROVIDE on TIMEOUT-VALUE, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting PROVIDE-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下必须对“TIMEOUT-VALUE、TARGET-HARDWARE-ID”执行“提供”；证据是“PROVIDE-RESULT-OBSERVABLE”。 | `FIXED-SOURCE-CONSTANT` / `DLP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `13..13 s` / evidence: SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-011-BD0CBB7058D1 | — |
| `CRS-M1-00188` | `SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-012-FB8820DE2238`<br>`ARINC-615A-3 4-4.1 p.102` | `TARGET-HARDWARE` / `BETWEEN-CONSECUTIVE-TFTP-FILE-TRANSFERS` / `BOUND-INTER-TRANSFER-DURATION-BY-DLP-EQUATION` / `DURATION-TIME, DLP-TO, DLP-RETRY, TFTP-RETRY, TFTP-TO` / `INTER-TRANSFER-DURATION-AND-EQUATION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform BOUND-INTER-TRANSFER-DURATION-BY-DLP-EQUATION on DURATION-TIME, DLP-TO, DLP-RETRY, TFTP-RETRY, TFTP-TO under BETWEEN-CONSECUTIVE-TFTP-FILE-TRANSFERS; evidence is the resulting INTER-TRANSFER-DURATION-AND-EQUATION-OBSERVABLE.<br>参与者“目标硬件”在“BETWEEN-CONSECUTIVE-TFTP-FILE-TRANSFERS”下必须对“DURATION-TIME、DLP-TO、DLP-RETRY、TFTP-RETRY、TFTP-TO”执行“BOUND-INTER-TRANSFER-DURATION-BY-DLP-EQUATION”；证据是“INTER-TRANSFER-DURATION-AND-EQUATION-OBSERVABLE”。 | `SYMBOLIC-SOURCE-EQUATION` / `DLP-TO-EQUATION` / `DLP-TO>DURATION-TIME+DLP-RETRY*(TFTP-RETRY+1)*TFTP-TO+TFTP-RETRY*TFTP-TO+2*(TFTP-TO/4)` / `0..DLP-TO-MINUS-RETRY-AND-NETWORK-TERMS s` / evidence: SU-ARINC-615A-3-A4-4-1-P115-EQUATION-001 | DEP-RFC-1350 |
| `CRS-M1-00189` | `SU-ARINC-615A-3-4-4-2-1-P115-PROSE-SENTENCE-001-46D0EBEB4FDD`<br>`ARINC-615A-3 4-4.2.1 p.103` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `RETRY` / `TFTP-FILE-TRANSFER, RETRY-NUMBER, TARGET-HARDWARE-ID` / `RETRY-ATTEMPT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE may perform RETRY on TFTP-FILE-TRANSFER, RETRY-NUMBER, TARGET-HARDWARE-ID under UNCONDITIONAL; evidence is the resulting RETRY-ATTEMPT-OBSERVABLE.<br>参与者“目标硬件”在“UNCONDITIONAL”下可以对“TFTP 文件传输、RETRY-NUMBER、TARGET-HARDWARE-ID”执行“重试”；证据是“重试尝试可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00190` | `SU-ARINC-615A-3-4-4-2-3-P116-PROSE-SENTENCE-003-546D677F3BB9`<br>`ARINC-615A-3 4-4.2.3 p.104` | `DATA-LOADER` / `UNCONDITIONAL` / `IMPLEMENT` / `NETWORK-INTERFACE` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER may perform IMPLEMENT on NETWORK-INTERFACE under UNCONDITIONAL; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“数据加载器”在“UNCONDITIONAL”下可以对“网络接口”执行“提供能力”；证据是“能力可用性可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00191` | `SU-ARINC-665-5-1-3-1-P011-PROSE-SENTENCE-002-93AC8751234E`<br>`ARINC-665-5 1.3.1 p.1` | `ARINC-665-CONFORMING-PRODUCT` / `UNCONDITIONAL` / `IMPLEMENT-REQUIRED-ARINC-665-CAPABILITIES` / `MINIMUM-ARINC-665-COMPATIBILITY-CAPABILITIES` / `ARINC-665-COMPATIBILITY-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-CONFORMING-PRODUCT shall perform IMPLEMENT-REQUIRED-ARINC-665-CAPABILITIES on MINIMUM-ARINC-665-COMPATIBILITY-CAPABILITIES under UNCONDITIONAL; evidence is the resulting ARINC-665-COMPATIBILITY-OBSERVABLE.<br>参与者“ARINC-665-CONFORMING-PRODUCT”在“UNCONDITIONAL”下必须对“MINIMUM-ARINC-665-COMPATIBILITY-CAPABILITIES”执行“IMPLEMENT-REQUIRED-ARINC-665-CAPABILITIES”；证据是“ARINC-665-COMPATIBILITY-OBSERVABLE”。 | — | — |
| `CRS-M1-00192` | `SU-ARINC-665-5-1-3-1-P011-PROSE-SENTENCE-003-F4F4BC419A09`<br>`ARINC-665-5 1.3.1 p.1` | `ARINC-665-REQUIREMENT-INTERPRETER` / `UNCONDITIONAL` / `TREAT-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY` / `ARINC-665-SHOULD-MODALITY` / `MODALITY-INTERPRETATION-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-REQUIREMENT-INTERPRETER shall perform TREAT-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY on ARINC-665-SHOULD-MODALITY under UNCONDITIONAL; evidence is the resulting MODALITY-INTERPRETATION-OBSERVABLE.<br>参与者“ARINC-665-REQUIREMENT-INTERPRETER”在“UNCONDITIONAL”下必须对“ARINC-665-SHOULD-MODALITY”执行“TREAT-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY”；证据是“MODALITY-INTERPRETATION-OBSERVABLE”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00193` | `SU-ARINC-665-5-1-3-1-P011-PROSE-SENTENCE-005-BC73FE29F0AF`<br>`ARINC-665-5 1.3.1 p.1` | `ARINC-665-REQUIREMENT-INTERPRETER` / `UNCONDITIONAL` / `TREAT-MAY-AS-OPTIONAL-CAPABILITY` / `ARINC-665-MAY-MODALITY` / `MODALITY-INTERPRETATION-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-REQUIREMENT-INTERPRETER may perform TREAT-MAY-AS-OPTIONAL-CAPABILITY on ARINC-665-MAY-MODALITY under UNCONDITIONAL; evidence is the resulting MODALITY-INTERPRETATION-OBSERVABLE.<br>参与者“ARINC-665-REQUIREMENT-INTERPRETER”在“UNCONDITIONAL”下可以对“ARINC-665-MAY-MODALITY”执行“TREAT-MAY-AS-OPTIONAL-CAPABILITY”；证据是“MODALITY-INTERPRETATION-OBSERVABLE”。 | — | — |
| `CRS-M1-00194` | `SU-ARINC-665-5-1-3-1-P011-PROSE-SENTENCE-006-3F3CB7AE6B26`<br>`ARINC-665-5 1.3.1 p.1` | `ARINC-665-CONFORMING-PRODUCT` / `WHEN-A-MAY-CAPABILITY-IS-IMPLEMENTED` / `CONDITIONALLY-IMPLEMENT-OPTIONAL-CAPABILITY-AS-SPECIFIED` / `OPTIONAL-ARINC-665-CAPABILITY` / `CONDITIONAL-CAPABILITY-CONFORMANCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-CONFORMING-PRODUCT shall perform CONDITIONALLY-IMPLEMENT-OPTIONAL-CAPABILITY-AS-SPECIFIED on OPTIONAL-ARINC-665-CAPABILITY under WHEN-A-MAY-CAPABILITY-IS-IMPLEMENTED; evidence is the resulting CONDITIONAL-CAPABILITY-CONFORMANCE-OBSERVABLE.<br>参与者“ARINC-665-CONFORMING-PRODUCT”在“WHEN-A-MAY-CAPABILITY-IS-IMPLEMENTED”下必须对“OPTIONAL-ARINC-665-CAPABILITY”执行“CONDITIONALLY-IMPLEMENT-OPTIONAL-CAPABILITY-AS-SPECIFIED”；证据是“CONDITIONAL-CAPABILITY-CONFORMANCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00195` | `SU-ARINC-665-5-1-3-3-P011-PROSE-SENTENCE-001-E0CA338A51EE`<br>`ARINC-665-5 1.3.3 p.1` | `ARINC-665-DATA-OBJECT-CONSUMER` / `UNCONDITIONAL` / `INTERPRET-FIELDS-AS-NUMERIC-BY-DEFAULT` / `DATA-FIELD-TYPE` / `DATA-TYPE-INTERPRETATION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-CONSUMER shall perform INTERPRET-FIELDS-AS-NUMERIC-BY-DEFAULT on DATA-FIELD-TYPE under UNCONDITIONAL; evidence is the resulting DATA-TYPE-INTERPRETATION-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-CONSUMER”在“UNCONDITIONAL”下必须对“DATA-FIELD-TYPE”执行“INTERPRET-FIELDS-AS-NUMERIC-BY-DEFAULT”；证据是“DATA-TYPE-INTERPRETATION-OBSERVABLE”。 | — | — |
| `CRS-M1-00196` | `SU-ARINC-665-5-1-4-2-P012-PROSE-SENTENCE-002-D07F6C2D4DAC`<br>`ARINC-665-5 1.4.2 p.2` | `LSP-OR-MEDIA-SET-CREATOR` / `UNCONDITIONAL` / `PROHIBIT-UNDEFINED-FIELD-INSERTION` / `ARINC-665-FILE` / `UNDEFINED-FIELD-ABSENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor LSP-OR-MEDIA-SET-CREATOR shall perform PROHIBIT-UNDEFINED-FIELD-INSERTION on ARINC-665-FILE under UNCONDITIONAL; evidence is the resulting UNDEFINED-FIELD-ABSENCE-OBSERVABLE.<br>参与者“LSP-OR-MEDIA-SET-CREATOR”在“UNCONDITIONAL”下必须对“ARINC-665-FILE”执行“PROHIBIT-UNDEFINED-FIELD-INSERTION”；证据是“UNDEFINED-FIELD-ABSENCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00197` | `SU-ARINC-665-5-1-4-3-P013-PROSE-SENTENCE-004-C23C95885017`<br>`ARINC-665-5 1.4.3 p.3` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `FILE-VERSION-COMPATIBILITY` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform ENCODE on FILE-VERSION-COMPATIBILITY under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“FILE-VERSION-COMPATIBILITY”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00198` | `SU-ARINC-665-5-1-5-P014-PROSE-SENTENCE-002-DBF83061338F`<br>`ARINC-665-5 1.5 p.4` | `SOFTWARE-PACKAGE-PRODUCER` / `UNCONDITIONAL` / `PREFIX-TARGET-HARDWARE-ID-WITH-MANUFACTURER-CODE` / `TARGET-HARDWARE-ID, MANUFACTURER-IDENTIFIER` / `TARGET-HARDWARE-ID-PREFIX-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor SOFTWARE-PACKAGE-PRODUCER shall perform PREFIX-TARGET-HARDWARE-ID-WITH-MANUFACTURER-CODE on TARGET-HARDWARE-ID, MANUFACTURER-IDENTIFIER under UNCONDITIONAL; evidence is the resulting TARGET-HARDWARE-ID-PREFIX-OBSERVABLE.<br>参与者“软件包生成方”在“UNCONDITIONAL”下必须对“TARGET-HARDWARE-ID、MANUFACTURER-IDENTIFIER”执行“PREFIX-TARGET-HARDWARE-ID-WITH-MANUFACTURER-CODE”；证据是“TARGET-HARDWARE-ID-PREFIX-OBSERVABLE”。 | — | — |
| `CRS-M1-00199` | `SU-ARINC-665-5-1-5-P014-PROSE-SENTENCE-003-35251417E277`<br>`ARINC-665-5 1.5 p.4` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ASSIGN` / `MANUFACTURER-IDENTIFIER` / `ASSIGN-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform ASSIGN on MANUFACTURER-IDENTIFIER under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ASSIGN-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“MANUFACTURER-IDENTIFIER”执行“分配或管理”；证据是“ASSIGN-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00200` | `SU-ARINC-665-5-1-5-P015-PROSE-SENTENCE-005-8F3C7190D1E7`<br>`ARINC-665-5 1.5 p.5` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-A-SOFTWARE-PART-IS-ACCEPTED-BY-MULTIPLE-TARGET-TYPES` / `ASSIGN-GENERIC-TARGET-HARDWARE-ID` / `SOFTWARE-PART-TARGET-HARDWARE-ID` / `TARGET-HARDWARE-ID-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor SOFTWARE-PACKAGE-PRODUCER shall perform ASSIGN-GENERIC-TARGET-HARDWARE-ID on SOFTWARE-PART-TARGET-HARDWARE-ID under WHEN-A-SOFTWARE-PART-IS-ACCEPTED-BY-MULTIPLE-TARGET-TYPES; evidence is the resulting TARGET-HARDWARE-ID-FIELD-OBSERVABLE.<br>参与者“软件包生成方”在“WHEN-A-SOFTWARE-PART-IS-ACCEPTED-BY-MULTIPLE-TARGET-TYPES”下必须对“SOFTWARE-PART-TARGET-HARDWARE-ID”执行“ASSIGN-GENERIC-TARGET-HARDWARE-ID”；证据是“TARGET-HARDWARE-ID-FIELD-OBSERVABLE”。 | — | — |
| `CRS-M1-00201` | `SU-ARINC-665-5-1-5-P015-PROSE-SENTENCE-007-6D740BC1EA66`<br>`ARINC-665-5 1.5 p.5` | `MULTI-CHANNEL-TARGET-SYSTEM` / `UNCONDITIONAL` / `DISTRIBUTE-REDUNDANT-LOADS-INTERNALLY` / `REDUNDANT-CHANNEL-LOADS` / `SINGLE-EXTERNAL-LOAD-REQUEST-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor MULTI-CHANNEL-TARGET-SYSTEM shall perform DISTRIBUTE-REDUNDANT-LOADS-INTERNALLY on REDUNDANT-CHANNEL-LOADS under UNCONDITIONAL; evidence is the resulting SINGLE-EXTERNAL-LOAD-REQUEST-OBSERVABLE.<br>参与者“MULTI-CHANNEL-TARGET-SYSTEM”在“UNCONDITIONAL”下必须对“REDUNDANT-CHANNEL-LOADS”执行“DISTRIBUTE-REDUNDANT-LOADS-INTERNALLY”；证据是“SINGLE-EXTERNAL-LOAD-REQUEST-OBSERVABLE”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00202` | `SU-ARINC-665-5-2-1-P016-PROSE-SENTENCE-001-A7E185845C31`<br>`ARINC-665-5 2.1 p.6` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENSURE-CARDINALITY` / `LOAD-PART-NUMBER, SOFTWARE-PART, LOADABLE-SOFTWARE-PART-NUMBER` / `ENSURE-CARDINALITY-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor SOFTWARE-PACKAGE-PRODUCER shall perform ENSURE-CARDINALITY on LOAD-PART-NUMBER, SOFTWARE-PART, LOADABLE-SOFTWARE-PART-NUMBER under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENSURE-CARDINALITY-RESULT-OBSERVABLE.<br>参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“加载件号、软件加载件、LOADABLE-SOFTWARE-PART-NUMBER”执行“保证基数约束”；证据是“ENSURE-CARDINALITY-RESULT-OBSERVABLE”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00203` | `SU-ARINC-665-5-2-1-P016-PROSE-SENTENCE-002-C9B7C44AE544`<br>`ARINC-665-5 2.1 p.6` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `COORDINATE` / `LOAD-PART-NUMBER` / `COORDINATE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform COORDINATE on LOAD-PART-NUMBER under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting COORDINATE-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“加载件号”执行“协调并批准”；证据是“COORDINATE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00204` | `SU-ARINC-665-5-2-1-P016-PROSE-SENTENCE-003-D2A78669BC58`<br>`ARINC-665-5 2.1 p.6` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ASSIGN` / `LOAD-PART-NUMBER, SOFTWARE-PART` / `ASSIGN-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor SOFTWARE-PACKAGE-PRODUCER shall perform ASSIGN on LOAD-PART-NUMBER, SOFTWARE-PART under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ASSIGN-RESULT-OBSERVABLE.<br>参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“加载件号、软件加载件”执行“分配或管理”；证据是“ASSIGN-RESULT-OBSERVABLE”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00205` | `SU-ARINC-665-5-2-1-1-P016-PROSE-SENTENCE-001-79D9D9285B09`<br>`ARINC-665-5 2.1.1 p.6` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `FORMAT` / `LOADABLE-SOFTWARE-PART-NUMBER` / `ENCODED-FORMAT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor SOFTWARE-PACKAGE-PRODUCER shall perform FORMAT on LOADABLE-SOFTWARE-PART-NUMBER under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FORMAT-OBSERVABLE.<br>参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“LOADABLE-SOFTWARE-PART-NUMBER”执行“按规定格式化”；证据是“编码格式可被观察”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00206` | `SU-ARINC-665-5-2-1-1-P016-PROSE-SENTENCE-005-9401791D8DFE`<br>`ARINC-665-5 2.1.1 p.6` | `ARINC-665-DATA-OBJECT-PRODUCER` / `UNCONDITIONAL` / `EXCLUDE-EMBEDDED-BLANKS` / `LOAD-PART-NUMBER` / `LOAD-PART-NUMBER-ENCODING-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform EXCLUDE-EMBEDDED-BLANKS on LOAD-PART-NUMBER under UNCONDITIONAL; evidence is the resulting LOAD-PART-NUMBER-ENCODING-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“UNCONDITIONAL”下必须对“加载件号”执行“EXCLUDE-EMBEDDED-BLANKS”；证据是“LOAD-PART-NUMBER-ENCODING-OBSERVABLE”。 | — | — |
| `CRS-M1-00207` | `SU-ARINC-665-5-2-1-1-P016-PROSE-SENTENCE-008-6FB26843CBD8`<br>`ARINC-665-5 2.1.1 p.6` | `ARINC-615A-DATA-LOADER` / `UNCONDITIONAL` / `DO-NOT-ENFORCE-SPECIFIC-PART-NUMBER-FORMAT` / `LOAD-PART-NUMBER` / `ABSENCE-OF-PN-FORMAT-REJECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-DATA-LOADER shall perform DO-NOT-ENFORCE-SPECIFIC-PART-NUMBER-FORMAT on LOAD-PART-NUMBER under UNCONDITIONAL; evidence is the resulting ABSENCE-OF-PN-FORMAT-REJECTION-OBSERVABLE.<br>参与者“ARINC-615A-DATA-LOADER”在“UNCONDITIONAL”下必须对“加载件号”执行“DO-NOT-ENFORCE-SPECIFIC-PART-NUMBER-FORMAT”；证据是“ABSENCE-OF-PN-FORMAT-REJECTION-OBSERVABLE”。 | — | — |
| `CRS-M1-00208` | `SU-ARINC-665-5-2-1-1-P016-PROSE-SENTENCE-009-63B5D84BC565`<br>`ARINC-665-5 2.1.1 p.6` | `ARINC-615A-DATA-LOADER` / `UNCONDITIONAL` / `PROCESS-NONCONFORMING-PART-NUMBER-FORMATS` / `LOAD-PART-NUMBER` / `LOAD-ACCEPTANCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-615A-DATA-LOADER shall perform PROCESS-NONCONFORMING-PART-NUMBER-FORMATS on LOAD-PART-NUMBER under UNCONDITIONAL; evidence is the resulting LOAD-ACCEPTANCE-OBSERVABLE.<br>参与者“ARINC-615A-DATA-LOADER”在“UNCONDITIONAL”下必须对“加载件号”执行“PROCESS-NONCONFORMING-PART-NUMBER-FORMATS”；证据是“LOAD-ACCEPTANCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00209` | `SU-ARINC-665-5-2-1-1-P017-PROSE-SENTENCE-014-4EC0F7886DBA`<br>`ARINC-665-5 2.1.1 p.7` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `DESIGN` / `NETWORK-INTERFACE` / `DESIGN-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER may perform DESIGN on NETWORK-INTERFACE under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting DESIGN-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下可以对“网络接口”执行“设计”；证据是“DESIGN-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00210` | `SU-ARINC-665-5-2-1-1-P017-PROSE-SENTENCE-015-3EE2B6181AC8`<br>`ARINC-665-5 2.1.1 p.7` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `FORMAT` / `NETWORK-INTERFACE` / `ENCODED-FORMAT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER may perform FORMAT on NETWORK-INTERFACE under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FORMAT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下可以对“网络接口”执行“按规定格式化”；证据是“编码格式可被观察”。 | — | — |
| `CRS-M1-00211` | `SU-ARINC-665-5-2-1-1-P017-PROSE-SENTENCE-018-ED171884907D`<br>`ARINC-665-5 2.1.1 p.7` | `ARINC-665-DATA-OBJECT-PRODUCER` / `UNCONDITIONAL` / `SEPARATE-DELIMITERS-FROM-LETTERS` / `ATA-PART-NUMBER-DELIMITERS` / `DELIMITER-PLACEMENT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform SEPARATE-DELIMITERS-FROM-LETTERS on ATA-PART-NUMBER-DELIMITERS under UNCONDITIONAL; evidence is the resulting DELIMITER-PLACEMENT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“UNCONDITIONAL”下必须对“ATA-PART-NUMBER-DELIMITERS”执行“SEPARATE-DELIMITERS-FROM-LETTERS”；证据是“DELIMITER-PLACEMENT-OBSERVABLE”。 | — | — |
| `CRS-M1-00212` | `SU-ARINC-665-5-2-1-1-P017-PROSE-SENTENCE-021-CBAD881793E5`<br>`ARINC-665-5 2.1.1 p.7` | `PROTOCOL-FILE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `LOAD-PART-NUMBER` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER shall perform ENCODE on LOAD-PART-NUMBER under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议文件生成方”在“生成 ARINC 665 数据对象时”下必须对“加载件号”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00213` | `SU-ARINC-665-5-2-1-1-P017-PROSE-SENTENCE-022-1D9E17675A1C`<br>`ARINC-665-5 2.1.1 p.7` | `ARINC-665-DATA-OBJECT-PRODUCER` / `UNCONDITIONAL` / `EXCLUDE-AMBIGUOUS-LETTER-O` / `ATA-PART-NUMBER-CHARACTER-SET` / `PART-NUMBER-CHARACTER-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform EXCLUDE-AMBIGUOUS-LETTER-O on ATA-PART-NUMBER-CHARACTER-SET under UNCONDITIONAL; evidence is the resulting PART-NUMBER-CHARACTER-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“UNCONDITIONAL”下必须对“ATA-PART-NUMBER-CHARACTER-SET”执行“EXCLUDE-AMBIGUOUS-LETTER-O”；证据是“PART-NUMBER-CHARACTER-OBSERVABLE”。 | — | — |
| `CRS-M1-00214` | `SU-ARINC-665-5-2-1-1-P017-PROSE-SENTENCE-024-481F25AD55F2`<br>`ARINC-665-5 2.1.1 p.7` | `ARINC-665-DATA-OBJECT-CONSUMER` / `UNCONDITIONAL` / `INTERPRET-CONFUSED-MMM-CHARACTERS-AS-ALPHABETIC` / `MMM-CODE` / `MMM-CHARACTER-INTERPRETATION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-CONSUMER shall perform INTERPRET-CONFUSED-MMM-CHARACTERS-AS-ALPHABETIC on MMM-CODE under UNCONDITIONAL; evidence is the resulting MMM-CHARACTER-INTERPRETATION-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-CONSUMER”在“UNCONDITIONAL”下必须对“MMM-CODE”执行“INTERPRET-CONFUSED-MMM-CHARACTERS-AS-ALPHABETIC”；证据是“MMM-CHARACTER-INTERPRETATION-OBSERVABLE”。 | — | — |
| `CRS-M1-00215` | `SU-ARINC-665-5-2-1-3-P017-PROSE-SENTENCE-003-41F8723AEC8B`<br>`ARINC-665-5 2.1.3 p.7` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `COMPUTE` / `CHECK-CHARACTERS` / `COMPUTE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform COMPUTE on CHECK-CHARACTERS under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting COMPUTE-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CHECK-CHARACTERS”执行“计算”；证据是“COMPUTE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00216` | `SU-ARINC-665-5-2-2-2-1-P018-PROSE-SENTENCE-001-84EA4A3113C8`<br>`ARINC-665-5 2.2.2.1 p.8` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `FORMAT` / `HEADER-FILE, SOFTWARE-PART` / `ENCODED-FORMAT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor SOFTWARE-PACKAGE-PRODUCER shall perform FORMAT on HEADER-FILE, SOFTWARE-PART under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FORMAT-OBSERVABLE.<br>参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“头文件、软件加载件”执行“按规定格式化”；证据是“编码格式可被观察”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00217` | `SU-ARINC-665-5-2-2-3-1-P018-PROSE-SENTENCE-001-7A7C6DE1A7A7`<br>`ARINC-665-5 2.2.3.1 p.8` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `HEADER-FILE, SOFTWARE-PART` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor SOFTWARE-PACKAGE-PRODUCER shall perform ENCODE on HEADER-FILE, SOFTWARE-PART under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“头文件、软件加载件”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00218` | `SU-ARINC-665-5-2-2-3-1-P019-PROSE-SENTENCE-003-D19D48006847`<br>`ARINC-665-5 2.2.3.1 p.9` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `DEFINE` / `HEADER-FILE` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor SOFTWARE-PACKAGE-PRODUCER shall perform DEFINE on HEADER-FILE under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting DEFINE-RESULT-OBSERVABLE.<br>参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“头文件”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00219` | `SU-ARINC-665-5-2-2-3-1-P019-PROSE-SENTENCE-004-A761BB0130D9`<br>`ARINC-665-5 2.2.3.1 p.9` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `BINARY-FIELD-ENCODING` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform ENCODE on BINARY-FIELD-ENCODING under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“BINARY-FIELD-ENCODING”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00220` | `SU-ARINC-665-5-2-2-3-1-3-1-P021-PROSE-SENTENCE-004-EF7E6FF4663B`<br>`ARINC-665-5 2.2.3.1.3.1 p.11` | `DATA-LOADER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `OPERATION, STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER may perform ENCODE on OPERATION, STATUS-CODE-CONDITIONAL-FIELD under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“数据加载器”在“生成 ARINC 665 数据对象时”下可以对“协议操作、STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00221` | `SU-ARINC-665-5-2-2-3-1-3-2-P021-PROSE-SENTENCE-001-641A8CBC9145`<br>`ARINC-665-5 2.2.3.1.3.2 p.11` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `BINARY-FIELD-ENCODING` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform ENCODE on BINARY-FIELD-ENCODING under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“BINARY-FIELD-ENCODING”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00222` | `SU-ARINC-665-5-2-2-3-1-10-P022-PROSE-SENTENCE-003-BCEBB784B407`<br>`ARINC-665-5 2.2.3.1.10 p.12` | `TARGET-HARDWARE` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `TARGET-HARDWARE-ID, STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform ENCODE on TARGET-HARDWARE-ID, STATUS-CODE-CONDITIONAL-FIELD under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“目标硬件”在“生成 ARINC 665 数据对象时”下必须对“TARGET-HARDWARE-ID、STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00223` | `SU-ARINC-665-5-2-2-3-1-14-P022-PROSE-SENTENCE-004-4114C0816C51`<br>`ARINC-665-5 2.2.3.1.14 p.12` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `IMPLEMENT` / `LOAD-PART-NUMBER, SOFTWARE-PART` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor SOFTWARE-PACKAGE-PRODUCER shall perform IMPLEMENT on LOAD-PART-NUMBER, SOFTWARE-PART under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“加载件号、软件加载件”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00224` | `SU-ARINC-665-5-2-2-3-1-18-P023-PROSE-SENTENCE-002-E664B245877E`<br>`ARINC-665-5 2.2.3.1.18 p.13` | `PROTOCOL-FILE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `NETWORK-INTERFACE, STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER shall perform ENCODE on NETWORK-INTERFACE, STATUS-CODE-CONDITIONAL-FIELD under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议文件生成方”在“生成 ARINC 665 数据对象时”下必须对“网络接口、STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00225` | `SU-ARINC-665-5-2-2-3-1-18-P023-PROSE-SENTENCE-004-C2CE75F23520`<br>`ARINC-665-5 2.2.3.1.18 p.13` | `TARGET-HARDWARE` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENSURE-UNIQUE` / `SOFTWARE-PART, TARGET-HARDWARE-ID` / `ENSURE-UNIQUE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform ENSURE-UNIQUE on SOFTWARE-PART, TARGET-HARDWARE-ID under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENSURE-UNIQUE-RESULT-OBSERVABLE.<br>参与者“目标硬件”在“生成 ARINC 665 数据对象时”下必须对“软件加载件、TARGET-HARDWARE-ID”执行“保证唯一性”；证据是“ENSURE-UNIQUE-RESULT-OBSERVABLE”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00226` | `SU-ARINC-665-5-2-2-3-1-24-P024-PROSE-SENTENCE-002-C100FC8EE4E9`<br>`ARINC-665-5 2.2.3.1.24 p.14` | `TARGET-HARDWARE` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `SOFTWARE-PART, TARGET-HARDWARE-ID` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform ENCODE on SOFTWARE-PART, TARGET-HARDWARE-ID under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“目标硬件”在“生成 ARINC 665 数据对象时”下必须对“软件加载件、TARGET-HARDWARE-ID”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00227` | `SU-ARINC-665-5-2-2-3-1-26-P024-PROSE-SENTENCE-005-38372C2FA366`<br>`ARINC-665-5 2.2.3.1.26 p.14` | `TARGET-HARDWARE` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `TARGET-HARDWARE-ID, STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform ENCODE on TARGET-HARDWARE-ID, STATUS-CODE-CONDITIONAL-FIELD under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“目标硬件”在“生成 ARINC 665 数据对象时”下必须对“TARGET-HARDWARE-ID、STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00228` | `SU-ARINC-665-5-2-2-3-1-31-P025-PROSE-SENTENCE-002-0374CB53F0AB`<br>`ARINC-665-5 2.2.3.1.31 p.15` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `CONSTRAIN` / `DATA-FILE` / `CONSTRAIN-RESULT-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform CONSTRAIN on DATA-FILE under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting CONSTRAIN-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“数据文件”执行“施加边界约束”；证据是“CONSTRAIN-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00229` | `SU-ARINC-665-5-2-2-3-1-32-P025-PROSE-SENTENCE-002-F6BCEFFF8371`<br>`ARINC-665-5 2.2.3.1.32 p.15` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `SET-ZERO` / `DATA-FILE` / `ZERO-VALUE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform SET-ZERO on DATA-FILE under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ZERO-VALUE-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“数据文件”执行“置零”；证据是“零值可被观察”。 | — | — |
| `CRS-M1-00230` | `SU-ARINC-665-5-2-2-3-1-37-P026-PROSE-SENTENCE-002-05AC99F08A26`<br>`ARINC-665-5 2.2.3.1.37 p.16` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `FORMAT` / `DATA-FILE` / `ENCODED-FORMAT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform FORMAT on DATA-FILE under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FORMAT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“数据文件”执行“按规定格式化”；证据是“编码格式可被观察”。 | — | — |
| `CRS-M1-00231` | `SU-ARINC-665-5-2-2-3-1-38-P026-PROSE-SENTENCE-002-E3FF88E1EDA0`<br>`ARINC-665-5 2.2.3.1.38 p.16` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `DEFINE` / `CRC, NETWORK-INTERFACE` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform DEFINE on CRC, NETWORK-INTERFACE under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting DEFINE-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值、网络接口”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00232` | `SU-ARINC-665-5-2-2-3-1-40-P026-PROSE-SENTENCE-002-FCF47A272C90`<br>`ARINC-665-5 2.2.3.1.40 p.16` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform VALIDATE on CRC under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00233` | `SU-ARINC-665-5-2-2-3-1-41-P026-PROSE-SENTENCE-002-3F17CFA7FF3B`<br>`ARINC-665-5 2.2.3.1.41 p.16` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform VALIDATE on CRC under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00234` | `SU-ARINC-665-5-2-2-3-1-42-P026-PROSE-SENTENCE-002-5E94CB4814AF`<br>`ARINC-665-5 2.2.3.1.42 p.16` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform VALIDATE on CRC under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00235` | `SU-ARINC-665-5-2-2-3-1-44-P027-PROSE-SENTENCE-002-AF1722AA2C2B`<br>`ARINC-665-5 2.2.3.1.44 p.17` | `PROTOCOL-FILE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `NETWORK-INTERFACE` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER shall perform ENCODE on NETWORK-INTERFACE under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议文件生成方”在“生成 ARINC 665 数据对象时”下必须对“网络接口”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00236` | `SU-ARINC-665-5-2-2-3-1-45-P027-PROSE-SENTENCE-002-3B48FE46115E`<br>`ARINC-665-5 2.2.3.1.45 p.17` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `IMPLEMENT` / `NETWORK-INTERFACE` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform IMPLEMENT on NETWORK-INTERFACE under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting CAPABILITY-AVAILABILITY-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“网络接口”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00237` | `SU-ARINC-665-5-2-2-3-1-49-P027-PROSE-SENTENCE-004-5EFD86A600D8`<br>`ARINC-665-5 2.2.3.1.49 p.17` | `PROTOCOL-FILE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `LOAD-PART-NUMBER, NETWORK-INTERFACE, STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER shall perform ENCODE on LOAD-PART-NUMBER, NETWORK-INTERFACE, STATUS-CODE-CONDITIONAL-FIELD under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议文件生成方”在“生成 ARINC 665 数据对象时”下必须对“加载件号、网络接口、STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00238` | `SU-ARINC-665-5-2-2-3-1-51-P027-PROSE-SENTENCE-002-E3FF88E1EDA0`<br>`ARINC-665-5 2.2.3.1.51 p.17` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `DEFINE` / `CRC, NETWORK-INTERFACE` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform DEFINE on CRC, NETWORK-INTERFACE under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting DEFINE-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值、网络接口”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00239` | `SU-ARINC-665-5-2-2-3-1-53-P028-PROSE-SENTENCE-002-EE1E5830AB09`<br>`ARINC-665-5 2.2.3.1.53 p.18` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform VALIDATE on CRC under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00240` | `SU-ARINC-665-5-2-2-3-1-54-P028-PROSE-SENTENCE-002-02BC06547867`<br>`ARINC-665-5 2.2.3.1.54 p.18` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC, NETWORK-INTERFACE` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform VALIDATE on CRC, NETWORK-INTERFACE under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值、网络接口”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00241` | `SU-ARINC-665-5-2-2-3-1-57-P028-PROSE-SENTENCE-002-284196C6B3D0`<br>`ARINC-665-5 2.2.3.1.57 p.18` | `OPERATOR` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `HEADER-FILE` / `VALIDATION-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor OPERATOR may perform VALIDATE on HEADER-FILE under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“操作员”在“生成 ARINC 665 数据对象时”下可以对“头文件”执行“验证”；证据是“验证结果可被观察”。 | — | — |
| `CRS-M1-00242` | `SU-ARINC-665-5-2-2-3-1-57-P028-PROSE-SENTENCE-003-E6ACA86FDF43`<br>`ARINC-665-5 2.2.3.1.57 p.18` | `PROTOCOL-FILE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | Actor PROTOCOL-FILE-PRODUCER may perform ENCODE on STATUS-CODE-CONDITIONAL-FIELD under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“协议文件生成方”在“生成 ARINC 665 数据对象时”下可以对“STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00243` | `SU-ARINC-665-5-2-2-3-1-59-P028-PROSE-SENTENCE-002-6672CA36E154`<br>`ARINC-665-5 2.2.3.1.59 p.18` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform VALIDATE on CRC under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00244` | `SU-ARINC-665-5-2-2-3-1-60-P028-PROSE-SENTENCE-002-3F17CFA7FF3B`<br>`ARINC-665-5 2.2.3.1.60 p.18` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform VALIDATE on CRC under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00245` | `SU-ARINC-665-5-2-2-3-1-61-P029-PROSE-SENTENCE-002-6F1B40878C6B`<br>`ARINC-665-5 2.2.3.1.61 p.19` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform VALIDATE on CRC under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00246` | `SU-ARINC-665-5-2-2-3-1-61-P029-PROSE-SENTENCE-003-6155DCD79C06`<br>`ARINC-665-5 2.2.3.1.61 p.19` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform VALIDATE on CRC under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00247` | `SU-ARINC-665-5-2-2-3-1-61-P029-PROSE-SENTENCE-004-9A509D9AE4E2`<br>`ARINC-665-5 2.2.3.1.61 p.19` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform VALIDATE on CRC under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting VALIDATION-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00248` | `SU-ARINC-665-5-2-2-3-1-62-P029-PROSE-SENTENCE-002-136B2E7764B0`<br>`ARINC-665-5 2.2.3.1.62 p.19` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `DEFINE` / `HEADER-FILE, CRC, NETWORK-INTERFACE` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor SOFTWARE-PACKAGE-PRODUCER shall perform DEFINE on HEADER-FILE, CRC, NETWORK-INTERFACE under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting DEFINE-RESULT-OBSERVABLE.<br>参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“头文件、CRC／校验值、网络接口”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00249` | `SU-ARINC-665-5-2-2-3-1-63-P029-PROSE-SENTENCE-002-8F49EC0CB8C3`<br>`ARINC-665-5 2.2.3.1.63 p.19` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `COMPUTE` / `HEADER-FILE, CRC` / `COMPUTE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor SOFTWARE-PACKAGE-PRODUCER shall perform COMPUTE on HEADER-FILE, CRC under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting COMPUTE-RESULT-OBSERVABLE.<br>参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“头文件、CRC／校验值”执行“计算”；证据是“COMPUTE-RESULT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00250` | `SU-ARINC-665-5-2-2-3-1-63-P029-PROSE-SENTENCE-003-5A9C8CDFFDEB`<br>`ARINC-665-5 2.2.3.1.63 p.19` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `DEFINE` / `CRC, NETWORK-INTERFACE` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor ARINC-665-DATA-OBJECT-PRODUCER shall perform DEFINE on CRC, NETWORK-INTERFACE under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting DEFINE-RESULT-OBSERVABLE.<br>参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值、网络接口”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00251` | `SU-ARINC-665-5-2-2-3-2-P029-PROSE-SENTENCE-002-25AC959A1D2A`<br>`ARINC-665-5 2.2.3.2 p.19` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `DATA-FILE, SOFTWARE-PART, FILE-CONTENT` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor SOFTWARE-PACKAGE-PRODUCER shall perform ENCODE on DATA-FILE, SOFTWARE-PART, FILE-CONTENT under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“数据文件、软件加载件、FILE-CONTENT”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00252` | `SU-ARINC-665-5-2-2-3-3-P029-PROSE-SENTENCE-002-BC8C7608516E`<br>`ARINC-665-5 2.2.3.3 p.19` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `SOFTWARE-PART, NETWORK-INTERFACE, FILE-CONTENT` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor SOFTWARE-PACKAGE-PRODUCER shall perform ENCODE on SOFTWARE-PART, NETWORK-INTERFACE, FILE-CONTENT under WHEN-PRODUCING-ARINC-665-DATA-OBJECT; evidence is the resulting ENCODED-FIELD-OBSERVABLE.<br>参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“软件加载件、网络接口、FILE-CONTENT”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00253` | `SU-ARINC-615A-3-TABLE-6-1-R002`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `TH_INFORMATION_INITIALIZATION` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on TH_INFORMATION_INITIALIZATION under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“TH_INFORMATION_INITIALIZATION”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00254` | `SU-ARINC-615A-3-TABLE-6-1-R003`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `INFORMATION_INITIALIZATION_RESPONSE` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLP shall perform SEND on INFORMATION_INITIALIZATION_RESPONSE under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“INFORMATION_INITIALIZATION_RESPONSE”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00255` | `SU-ARINC-615A-3-TABLE-6-1-R005`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `TH_INFORMATION` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLP shall perform SEND on TH_INFORMATION under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“TH_INFORMATION”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00256` | `SU-ARINC-615A-3-TABLE-6-1-R006`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `INFORMATION_STATUS` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLP shall perform SEND on INFORMATION_STATUS under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“INFORMATION_STATUS”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00257` | `SU-ARINC-615A-3-TABLE-6-1-R007`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `ABORT_REQUEST` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on ABORT_REQUEST under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“ABORT_REQUEST”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00258` | `SU-ARINC-615A-3-TABLE-6-1-R009`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `TH_UPLOADING_INITIALIZATION` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on TH_UPLOADING_INITIALIZATION under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“TH_UPLOADING_INITIALIZATION”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00259` | `SU-ARINC-615A-3-TABLE-6-1-R010`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `UPLOADING_INITIALIZATION_RESPONSE` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLP shall perform SEND on UPLOADING_INITIALIZATION_RESPONSE under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“UPLOADING_INITIALIZATION_RESPONSE”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00260` | `SU-ARINC-615A-3-TABLE-6-1-R012`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `LOAD_LIST` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on LOAD_LIST under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“LOAD_LIST”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00261` | `SU-ARINC-615A-3-TABLE-6-1-R013`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `UPLOAD_INFORMATION_STATUS` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLP shall perform SEND on UPLOAD_INFORMATION_STATUS under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“UPLOAD_INFORMATION_STATUS”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00262` | `SU-ARINC-615A-3-TABLE-6-1-R014`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `ABORT_REQUEST` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on ABORT_REQUEST under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“ABORT_REQUEST”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00263` | `SU-ARINC-615A-3-TABLE-6-1-R016`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `FILE_NOT_AVAILABLE` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLP shall perform SEND on FILE_NOT_AVAILABLE under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“FILE_NOT_AVAILABLE”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00264` | `SU-ARINC-615A-3-TABLE-6-1-R017`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `UPLOAD_INFORMATION_STATUS` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLP shall perform SEND on UPLOAD_INFORMATION_STATUS under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“UPLOAD_INFORMATION_STATUS”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00265` | `SU-ARINC-615A-3-TABLE-6-1-R018`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `ABORT_REQUEST` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on ABORT_REQUEST under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“ABORT_REQUEST”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00266` | `SU-ARINC-615A-3-TABLE-6-1-R020`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_MEDIA_INITIALIZATION` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on DOWNLOADING_MEDIA_INITIALIZATION under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“DOWNLOADING_MEDIA_INITIALIZATION”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00267` | `SU-ARINC-615A-3-TABLE-6-1-R021`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_INITIALIZATION_RESPONSE` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLP shall perform SEND on DOWNLOADING_INITIALIZATION_RESPONSE under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_INITIALIZATION_RESPONSE”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00268` | `SU-ARINC-615A-3-TABLE-6-1-R023`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_INFORMATION_STATUS` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLP shall perform SEND on DOWNLOADING_INFORMATION_STATUS under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_INFORMATION_STATUS”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00269` | `SU-ARINC-615A-3-TABLE-6-1-R024`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `ABORT_REQUEST` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on ABORT_REQUEST under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“ABORT_REQUEST”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00270` | `SU-ARINC-615A-3-TABLE-6-1-R026`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_FILE_RECEIPT` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLP shall perform SEND on DOWNLOADING_FILE_RECEIPT under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_FILE_RECEIPT”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00271` | `SU-ARINC-615A-3-TABLE-6-1-R027`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_INFORMATION_STATUS` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLP shall perform SEND on DOWNLOADING_INFORMATION_STATUS under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_INFORMATION_STATUS”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00272` | `SU-ARINC-615A-3-TABLE-6-1-R028`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `ABORT_REQUEST` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on ABORT_REQUEST under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“ABORT_REQUEST”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00273` | `SU-ARINC-615A-3-TABLE-6-1-R030`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_OPERATOR_INITIALIZATION` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on DOWNLOADING_OPERATOR_INITIALIZATION under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“DOWNLOADING_OPERATOR_INITIALIZATION”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00274` | `SU-ARINC-615A-3-TABLE-6-1-R031`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_INITIALIZATION_RESPONSE` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLP shall perform SEND on DOWNLOADING_INITIALIZATION_RESPONSE under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_INITIALIZATION_RESPONSE”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00275` | `SU-ARINC-615A-3-TABLE-6-1-R033`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_FILE_LIST_RECEIPT` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLP shall perform SEND on DOWNLOADING_FILE_LIST_RECEIPT under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_FILE_LIST_RECEIPT”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00276` | `SU-ARINC-615A-3-TABLE-6-1-R034`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `FILE_SELECTION` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on FILE_SELECTION under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“FILE_SELECTION”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00277` | `SU-ARINC-615A-3-TABLE-6-1-R035`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_INFORMATION_STATUS` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLP shall perform SEND on DOWNLOADING_INFORMATION_STATUS under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_INFORMATION_STATUS”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00278` | `SU-ARINC-615A-3-TABLE-6-1-R036`<br>`ARINC-615A-3 6.1 p.43` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `ABORT-REQUEST` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on ABORT-REQUEST under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“ABORT-REQUEST”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00279` | `SU-ARINC-615A-3-TABLE-6-1-R038`<br>`ARINC-615A-3 6.1 p.43` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_FILE_RECEIPT` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLP shall perform SEND on DOWNLOADING_FILE_RECEIPT under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_FILE_RECEIPT”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00280` | `SU-ARINC-615A-3-TABLE-6-1-R039`<br>`ARINC-615A-3 6.1 p.43` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_INFORMATION_STATUS` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLP shall perform SEND on DOWNLOADING_INFORMATION_STATUS under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_INFORMATION_STATUS”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00281` | `SU-ARINC-615A-3-TABLE-6-1-R040`<br>`ARINC-615A-3 6.1 p.43` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `ABORT_REQUEST` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on ABORT_REQUEST under TABLE-DEFINED-OPERATION-STEP; evidence is the resulting MESSAGE-DIRECTION-OBSERVABLE.<br>参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“ABORT_REQUEST”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00282` | `SU-ARINC-615A-3-TABLE-6_4_1-1-R002`<br>`ARINC-615A-3 6.4.1 p.67` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-FILE-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-FILE-LENGTH in position 1 with 32 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 1 个字段位置编码 FIELD-FILE-LENGTH，位宽为 32 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00283` | `SU-ARINC-615A-3-TABLE-6_4_1-1-R003`<br>`ARINC-615A-3 6.4.1 p.67` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PROTOCOL-VERSION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-PROTOCOL-VERSION in position 2 with 16 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 2 个字段位置编码 FIELD-PROTOCOL-VERSION，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00284` | `SU-ARINC-615A-3-TABLE-6_4_1-1-R004`<br>`ARINC-615A-3 6.4.1 p.67` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-OPERATION-ACCEPTANCE-STATUS-CODE` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-OPERATION-ACCEPTANCE-STATUS-CODE in position 3 with 16 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 3 个字段位置编码 FIELD-OPERATION-ACCEPTANCE-STATUS-CODE，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00285` | `SU-ARINC-615A-3-TABLE-6_4_1-1-R005`<br>`ARINC-615A-3 6.4.1 p.67` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-STATUS-DESCRIPTION-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-STATUS-DESCRIPTION-LENGTH in position 4 with 8 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 4 个字段位置编码 FIELD-STATUS-DESCRIPTION-LENGTH，位宽为 8 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00286` | `SU-ARINC-615A-3-TABLE-6_4_1-1-R006`<br>`ARINC-615A-3 6.4.1 p.67` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-STATUS-DESCRIPTION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-STATUS-DESCRIPTION in position 5 with 0 to 2040 bits, repeated once; termination is ZERO-TERMINATED-PER-SECTION-6.4.<br>协议文件生成方必须在第 5 个字段位置编码 FIELD-STATUS-DESCRIPTION，位宽为 0..2040 bit，重复范围为 ONCE；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00287` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R002`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-FILE-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-FILE-LENGTH in position 1 with 32 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 1 个字段位置编码 FIELD-FILE-LENGTH，位宽为 32 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00288` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R003`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PROTOCOL-VERSION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-PROTOCOL-VERSION in position 2 with 16 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 2 个字段位置编码 FIELD-PROTOCOL-VERSION，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00289` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R004`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-NUMBER-OF-TARGET-HARDWARE` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-NUMBER-OF-TARGET-HARDWARE in position 3 with 16 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 3 个字段位置编码 FIELD-NUMBER-OF-TARGET-HARDWARE，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00290` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R005`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LITERAL-NAME-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-LITERAL-NAME-LENGTH in position 4 with 8 bits, repeated per literal name; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 4 个字段位置编码 FIELD-LITERAL-NAME-LENGTH，位宽为 8 bit，重复范围为 PER-LITERAL-NAME；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00291` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R006`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LITERAL-NAME` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-LITERAL-NAME in position 5 with 8 to 2040 bits, repeated per literal name; termination is ZERO-TERMINATED-PER-SECTION-6.4.<br>协议文件生成方必须在第 5 个字段位置编码 FIELD-LITERAL-NAME，位宽为 8..2040 bit，重复范围为 PER-LITERAL-NAME；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00292` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R007`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-SERIAL-NUMBER-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-SERIAL-NUMBER-LENGTH in position 6 with 8 bits, repeated per literal name; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 6 个字段位置编码 FIELD-SERIAL-NUMBER-LENGTH，位宽为 8 bit，重复范围为 PER-LITERAL-NAME；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00293` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R008`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-SERIAL-NUMBER` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-SERIAL-NUMBER in position 7 with 8 to 2040 bits, repeated per literal name; termination is ZERO-TERMINATED-PER-SECTION-6.4.<br>协议文件生成方必须在第 7 个字段位置编码 FIELD-SERIAL-NUMBER，位宽为 8..2040 bit，重复范围为 PER-LITERAL-NAME；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00294` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R009`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-NUMBER-OF-PART-NUMBERS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-NUMBER-OF-PART-NUMBERS in position 8 with 16 bits, repeated per literal name; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 8 个字段位置编码 FIELD-NUMBER-OF-PART-NUMBERS，位宽为 16 bit，重复范围为 PER-LITERAL-NAME；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00295` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R010`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PART-NUMBER-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-PART-NUMBER-LENGTH in position 9 with 8 bits, repeated per part number within literal name; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 9 个字段位置编码 FIELD-PART-NUMBER-LENGTH，位宽为 8 bit，重复范围为 PER-PART-NUMBER-WITHIN-LITERAL-NAME；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00296` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R011`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PART-NUMBER` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-PART-NUMBER in position 10 with 8 to 2040 bits, repeated per part number within literal name; termination is ZERO-TERMINATED-PER-SECTION-6.4.<br>协议文件生成方必须在第 10 个字段位置编码 FIELD-PART-NUMBER，位宽为 8..2040 bit，重复范围为 PER-PART-NUMBER-WITHIN-LITERAL-NAME；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00297` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R012`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-AMENDMENT-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-AMENDMENT-LENGTH in position 11 with 8 bits, repeated per part number within literal name; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 11 个字段位置编码 FIELD-AMENDMENT-LENGTH，位宽为 8 bit，重复范围为 PER-PART-NUMBER-WITHIN-LITERAL-NAME；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00298` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R013`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-AMENDMENT` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-AMENDMENT in position 12 with 0 to 2040 bits, repeated per part number within literal name; termination is ZERO-TERMINATED-PER-SECTION-6.4.<br>协议文件生成方必须在第 12 个字段位置编码 FIELD-AMENDMENT，位宽为 0..2040 bit，重复范围为 PER-PART-NUMBER-WITHIN-LITERAL-NAME；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00299` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R014`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PART-DESIGNATION-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-PART-DESIGNATION-LENGTH in position 13 with 8 bits, repeated per part number within literal name; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 13 个字段位置编码 FIELD-PART-DESIGNATION-LENGTH，位宽为 8 bit，重复范围为 PER-PART-NUMBER-WITHIN-LITERAL-NAME；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00300` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R015`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PART-DESIGNATION-TEXT` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-PART-DESIGNATION-TEXT in position 14 with 8 to 2040 bits, repeated per part number within literal name; termination is ZERO-TERMINATED-PER-SECTION-6.4.<br>协议文件生成方必须在第 14 个字段位置编码 FIELD-PART-DESIGNATION-TEXT，位宽为 8..2040 bit，重复范围为 PER-PART-NUMBER-WITHIN-LITERAL-NAME；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00301` | `SU-ARINC-615A-3-TABLE-6_4_3-1-R002`<br>`ARINC-615A-3 6.4.3 p.70` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-FILE-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-FILE-LENGTH in position 1 with 32 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 1 个字段位置编码 FIELD-FILE-LENGTH，位宽为 32 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00302` | `SU-ARINC-615A-3-TABLE-6_4_3-1-R003`<br>`ARINC-615A-3 6.4.3 p.70` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PROTOCOL-VERSION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-PROTOCOL-VERSION in position 2 with 16 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 2 个字段位置编码 FIELD-PROTOCOL-VERSION，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00303` | `SU-ARINC-615A-3-TABLE-6_4_3-1-R004`<br>`ARINC-615A-3 6.4.3 p.70` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-COUNTER` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-COUNTER in position 3 with 16 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 3 个字段位置编码 FIELD-COUNTER，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00304` | `SU-ARINC-615A-3-TABLE-6_4_3-1-R005`<br>`ARINC-615A-3 6.4.3 p.70` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-INFORMATION-OPERATION-STATUS-CODE` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-INFORMATION-OPERATION-STATUS-CODE in position 4 with 16 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 4 个字段位置编码 FIELD-INFORMATION-OPERATION-STATUS-CODE，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00305` | `SU-ARINC-615A-3-TABLE-6_4_3-1-R006`<br>`ARINC-615A-3 6.4.3 p.70` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-EXCEPTION-TIMER` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-EXCEPTION-TIMER in position 5 with 16 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 5 个字段位置编码 FIELD-EXCEPTION-TIMER，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | `MESSAGE-CARRIED-PARAMETER` / `MESSAGE-TIMER-VALUE` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-TABLE-6_4_3-1-R006 | — |
| `CRS-M1-00306` | `SU-ARINC-615A-3-TABLE-6_4_3-1-R007`<br>`ARINC-615A-3 6.4.3 p.70` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-ESTIMATED-TIME` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-ESTIMATED-TIME in position 6 with 16 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 6 个字段位置编码 FIELD-ESTIMATED-TIME，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00307` | `SU-ARINC-615A-3-TABLE-6_4_3-1-R008`<br>`ARINC-615A-3 6.4.3 p.70` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-STATUS-DESCRIPTION-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-STATUS-DESCRIPTION-LENGTH in position 7 with 8 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 7 个字段位置编码 FIELD-STATUS-DESCRIPTION-LENGTH，位宽为 8 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00308` | `SU-ARINC-615A-3-TABLE-6_4_3-1-R009`<br>`ARINC-615A-3 6.4.3 p.70` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-STATUS-DESCRIPTION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The protocol-file producer shall encode FIELD-STATUS-DESCRIPTION in position 8 with 0 to 2040 bits, repeated once; termination is ZERO-TERMINATED-PER-SECTION-6.4.<br>协议文件生成方必须在第 8 个字段位置编码 FIELD-STATUS-DESCRIPTION，位宽为 0..2040 bit，重复范围为 ONCE；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00309` | `SU-ARINC-615A-3-TABLE-6_4_4-1-R002`<br>`ARINC-615A-3 6.4.4 p.72` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-FILE-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-FILE-LENGTH in position 1 with 32 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 1 个字段位置编码 FIELD-FILE-LENGTH，位宽为 32 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00310` | `SU-ARINC-615A-3-TABLE-6_4_4-1-R003`<br>`ARINC-615A-3 6.4.4 p.72` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PROTOCOL-VERSION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-PROTOCOL-VERSION in position 2 with 16 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 2 个字段位置编码 FIELD-PROTOCOL-VERSION，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00311` | `SU-ARINC-615A-3-TABLE-6_4_4-1-R004`<br>`ARINC-615A-3 6.4.4 p.72` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-NUMBER-OF-HEADER-FILES` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-NUMBER-OF-HEADER-FILES in position 3 with 16 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 3 个字段位置编码 FIELD-NUMBER-OF-HEADER-FILES，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00312` | `SU-ARINC-615A-3-TABLE-6_4_4-1-R005`<br>`ARINC-615A-3 6.4.4 p.72` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-HEADER-FILE-NAME-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-HEADER-FILE-NAME-LENGTH in position 4 with 8 bits, repeated per preceding count field; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 4 个字段位置编码 FIELD-HEADER-FILE-NAME-LENGTH，位宽为 8 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00313` | `SU-ARINC-615A-3-TABLE-6_4_4-1-R006`<br>`ARINC-615A-3 6.4.4 p.72` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-HEADER-FILE-NAME` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-HEADER-FILE-NAME in position 5 with 8 to 2040 bits, repeated per preceding count field; termination is ZERO-TERMINATED-PER-SECTION-6.4.<br>协议文件生成方必须在第 5 个字段位置编码 FIELD-HEADER-FILE-NAME，位宽为 8..2040 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00314` | `SU-ARINC-615A-3-TABLE-6_4_4-1-R007`<br>`ARINC-615A-3 6.4.4 p.72` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-PART-NUMBER-NAME-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-LOAD-PART-NUMBER-NAME-LENGTH in position 6 with 8 bits, repeated per preceding count field; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 6 个字段位置编码 FIELD-LOAD-PART-NUMBER-NAME-LENGTH，位宽为 8 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00315` | `SU-ARINC-615A-3-TABLE-6_4_4-1-R008`<br>`ARINC-615A-3 6.4.4 p.72` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-PART-NUMBER-NAME` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-LOAD-PART-NUMBER-NAME in position 7 with 8 to 2040 bits, repeated per preceding count field; termination is ZERO-TERMINATED-PER-SECTION-6.4.<br>协议文件生成方必须在第 7 个字段位置编码 FIELD-LOAD-PART-NUMBER-NAME，位宽为 8..2040 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00316` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R002`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-FILE-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-FILE-LENGTH in position 1 with 32 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 1 个字段位置编码 FIELD-FILE-LENGTH，位宽为 32 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00317` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R003`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PROTOCOL-VERSION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-PROTOCOL-VERSION in position 2 with 16 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 2 个字段位置编码 FIELD-PROTOCOL-VERSION，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00318` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R004`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-UPLOAD-OPERATION-STATUS-CODE` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-UPLOAD-OPERATION-STATUS-CODE in position 3 with 16 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 3 个字段位置编码 FIELD-UPLOAD-OPERATION-STATUS-CODE，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00319` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R005`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-UPLOAD-STATUS-DESCRIPTION-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-UPLOAD-STATUS-DESCRIPTION-LENGTH in position 4 with 8 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 4 个字段位置编码 FIELD-UPLOAD-STATUS-DESCRIPTION-LENGTH，位宽为 8 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00320` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R006`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-UPLOAD-STATUS-DESCRIPTION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-UPLOAD-STATUS-DESCRIPTION in position 5 with 0 to 2040 bits, repeated once; termination is ZERO-TERMINATED-PER-SECTION-6.4.<br>协议文件生成方必须在第 5 个字段位置编码 FIELD-UPLOAD-STATUS-DESCRIPTION，位宽为 0..2040 bit，重复范围为 ONCE；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00321` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R007`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-COUNTER` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-COUNTER in position 6 with 16 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 6 个字段位置编码 FIELD-COUNTER，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00322` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R008`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-EXCEPTION-TIMER` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-EXCEPTION-TIMER in position 7 with 16 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 7 个字段位置编码 FIELD-EXCEPTION-TIMER，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | `MESSAGE-CARRIED-PARAMETER` / `MESSAGE-TIMER-VALUE` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / evidence: SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-TABLE-6_4_3-1-R006 | — |
| `CRS-M1-00323` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R009`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-ESTIMATED-TIME` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-ESTIMATED-TIME in position 8 with 16 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 8 个字段位置编码 FIELD-ESTIMATED-TIME，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00324` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R010`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-LIST-RATIO` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-LOAD-LIST-RATIO in position 9 with 24 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 9 个字段位置编码 FIELD-LOAD-LIST-RATIO，位宽为 24 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00325` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R011`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-NUMBER-OF-HEADER-FILES` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-NUMBER-OF-HEADER-FILES in position 10 with 16 bits, repeated once; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 10 个字段位置编码 FIELD-NUMBER-OF-HEADER-FILES，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00326` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R012`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-HEADER-FILE-NAME-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-HEADER-FILE-NAME-LENGTH in position 11 with 8 bits, repeated per preceding count field; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 11 个字段位置编码 FIELD-HEADER-FILE-NAME-LENGTH，位宽为 8 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00327` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R013`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-HEADER-FILE-NAME` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-HEADER-FILE-NAME in position 12 with 8 to 2040 bits, repeated per preceding count field; termination is ZERO-TERMINATED-PER-SECTION-6.4.<br>协议文件生成方必须在第 12 个字段位置编码 FIELD-HEADER-FILE-NAME，位宽为 8..2040 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00328` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R014`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-PART-NUMBER-NAME-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-LOAD-PART-NUMBER-NAME-LENGTH in position 13 with 8 bits, repeated per preceding count field; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 13 个字段位置编码 FIELD-LOAD-PART-NUMBER-NAME-LENGTH，位宽为 8 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00329` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R015`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-PART-NUMBER-NAME` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-LOAD-PART-NUMBER-NAME in position 14 with 8 to 2040 bits, repeated per preceding count field; termination is ZERO-TERMINATED-PER-SECTION-6.4.<br>协议文件生成方必须在第 14 个字段位置编码 FIELD-LOAD-PART-NUMBER-NAME，位宽为 8..2040 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00330` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R016`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-RATIO` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-LOAD-RATIO in position 15 with 24 bits, repeated per preceding count field; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 15 个字段位置编码 FIELD-LOAD-RATIO，位宽为 24 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00331` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R017`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-STATUS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-LOAD-STATUS in position 16 with 16 bits, repeated per preceding count field; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 16 个字段位置编码 FIELD-LOAD-STATUS，位宽为 16 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00332` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R018`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-STATUS-DESCRIPTION-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-LOAD-STATUS-DESCRIPTION-LENGTH in position 17 with 8 bits, repeated per preceding count field; termination is NOT-APPLICABLE-OR-PROSE-DEFINED.<br>协议文件生成方必须在第 17 个字段位置编码 FIELD-LOAD-STATUS-DESCRIPTION-LENGTH，位宽为 8 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00333` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R019`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-STATUS-DESCRIPTION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | The protocol-file producer shall encode FIELD-LOAD-STATUS-DESCRIPTION in position 18 with 0 to 2040 bits, repeated per preceding count field; termination is ZERO-TERMINATED-PER-SECTION-6.4.<br>协议文件生成方必须在第 18 个字段位置编码 FIELD-LOAD-STATUS-DESCRIPTION，位宽为 0..2040 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00334` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R001`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X0001-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X0001` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform INTERPRET-AND-DISPLAY-STATUS on STATUS-CODE-0X0001 under WHEN-STATUS-CODE-0X0001-IS-RECEIVED; evidence is the resulting STATUS-MEANING-AND-DISPLAY-OBSERVABLE.<br>参与者“数据加载器”在“WHEN-STATUS-CODE-0X0001-IS-RECEIVED”下必须对“STATUS-CODE-0X0001”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00335` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R002`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X1000-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X1000` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform INTERPRET-AND-DISPLAY-STATUS on STATUS-CODE-0X1000 under WHEN-STATUS-CODE-0X1000-IS-RECEIVED; evidence is the resulting STATUS-MEANING-AND-DISPLAY-OBSERVABLE.<br>参与者“数据加载器”在“WHEN-STATUS-CODE-0X1000-IS-RECEIVED”下必须对“STATUS-CODE-0X1000”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00336` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R003`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X1002-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X1002` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform INTERPRET-AND-DISPLAY-STATUS on STATUS-CODE-0X1002 under WHEN-STATUS-CODE-0X1002-IS-RECEIVED; evidence is the resulting STATUS-MEANING-AND-DISPLAY-OBSERVABLE.<br>参与者“数据加载器”在“WHEN-STATUS-CODE-0X1002-IS-RECEIVED”下必须对“STATUS-CODE-0X1002”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00337` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R004`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X0002-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X0002` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform INTERPRET-AND-DISPLAY-STATUS on STATUS-CODE-0X0002 under WHEN-STATUS-CODE-0X0002-IS-RECEIVED; evidence is the resulting STATUS-MEANING-AND-DISPLAY-OBSERVABLE.<br>参与者“数据加载器”在“WHEN-STATUS-CODE-0X0002-IS-RECEIVED”下必须对“STATUS-CODE-0X0002”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00338` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R005`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X0003-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X0003` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform INTERPRET-AND-DISPLAY-STATUS on STATUS-CODE-0X0003 under WHEN-STATUS-CODE-0X0003-IS-RECEIVED; evidence is the resulting STATUS-MEANING-AND-DISPLAY-OBSERVABLE.<br>参与者“数据加载器”在“WHEN-STATUS-CODE-0X0003-IS-RECEIVED”下必须对“STATUS-CODE-0X0003”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00339` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R006`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X0004-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X0004` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform INTERPRET-AND-DISPLAY-STATUS on STATUS-CODE-0X0004 under WHEN-STATUS-CODE-0X0004-IS-RECEIVED; evidence is the resulting STATUS-MEANING-AND-DISPLAY-OBSERVABLE.<br>参与者“数据加载器”在“WHEN-STATUS-CODE-0X0004-IS-RECEIVED”下必须对“STATUS-CODE-0X0004”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00340` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R007`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X1003-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X1003` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform INTERPRET-AND-DISPLAY-STATUS on STATUS-CODE-0X1003 under WHEN-STATUS-CODE-0X1003-IS-RECEIVED; evidence is the resulting STATUS-MEANING-AND-DISPLAY-OBSERVABLE.<br>参与者“数据加载器”在“WHEN-STATUS-CODE-0X1003-IS-RECEIVED”下必须对“STATUS-CODE-0X1003”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00341` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R008`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X1004-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X1004` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform INTERPRET-AND-DISPLAY-STATUS on STATUS-CODE-0X1004 under WHEN-STATUS-CODE-0X1004-IS-RECEIVED; evidence is the resulting STATUS-MEANING-AND-DISPLAY-OBSERVABLE.<br>参与者“数据加载器”在“WHEN-STATUS-CODE-0X1004-IS-RECEIVED”下必须对“STATUS-CODE-0X1004”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00342` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R009`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X1005-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X1005` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform INTERPRET-AND-DISPLAY-STATUS on STATUS-CODE-0X1005 under WHEN-STATUS-CODE-0X1005-IS-RECEIVED; evidence is the resulting STATUS-MEANING-AND-DISPLAY-OBSERVABLE.<br>参与者“数据加载器”在“WHEN-STATUS-CODE-0X1005-IS-RECEIVED”下必须对“STATUS-CODE-0X1005”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00343` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R010`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X1007-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X1007` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform INTERPRET-AND-DISPLAY-STATUS on STATUS-CODE-0X1007 under WHEN-STATUS-CODE-0X1007-IS-RECEIVED; evidence is the resulting STATUS-MEANING-AND-DISPLAY-OBSERVABLE.<br>参与者“数据加载器”在“WHEN-STATUS-CODE-0X1007-IS-RECEIVED”下必须对“STATUS-CODE-0X1007”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00344` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R011`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X1007-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X1007` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER shall perform INTERPRET-AND-DISPLAY-STATUS on STATUS-CODE-0X1007 under WHEN-STATUS-CODE-0X1007-IS-RECEIVED; evidence is the resulting STATUS-MEANING-AND-DISPLAY-OBSERVABLE.<br>参与者“数据加载器”在“WHEN-STATUS-CODE-0X1007-IS-RECEIVED”下必须对“STATUS-CODE-0X1007”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00345` | `SU-ARINC-615A-3-TABLE-6_4_10-1-FOOTNOTE-001`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER-DISPLAY` / `WHEN-RENDERING-TABLE-6.4.10-STATUS` / `SUBSTITUTE-OPERATION-NAME` / `STATUS-DISPLAY-TEXT` / `DISPLAY-TEXT-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DATA-LOADER-DISPLAY shall perform SUBSTITUTE-OPERATION-NAME on STATUS-DISPLAY-TEXT under WHEN-RENDERING-TABLE-6.4.10-STATUS; evidence is the resulting DISPLAY-TEXT-OBSERVABLE.<br>参与者“DATA-LOADER-DISPLAY”在“WHEN-RENDERING-TABLE-6.4.10-STATUS”下必须对“STATUS-DISPLAY-TEXT”执行“SUBSTITUTE-OPERATION-NAME”；证据是“DISPLAY-TEXT-OBSERVABLE”。 | — | — |
| `CRS-M1-00346` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E001-6BBD8FA395EF`<br>`ARINC-615A-3 6.3.1 p.50` | `DLA` / `OPERATION-START` / `RECEIVE` / `TH-INFORMATION-INITIALIZATION` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform RECEIVE on TH-INFORMATION-INITIALIZATION toward APPLICATION under OPERATION-START; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“OPERATION-START”下必须对“TH-INFORMATION-INITIALIZATION”执行“接收”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00347` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E002-C4C83C8F67F8`<br>`ARINC-615A-3 6.3.1 p.50` | `DLA` / `INITIALIZATION` / `SEND-TFTP-READ-REQUEST` / `LCI` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND-TFTP-READ-REQUEST on LCI toward TARGET-HARDWARE under INITIALIZATION; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“INITIALIZATION”下必须对“LCI”执行“SEND-TFTP-READ-REQUEST”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00348` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E003-86B1F4D69CC7`<br>`ARINC-615A-3 6.3.1 p.50` | `TARGET-HARDWARE` / `READ-REQUEST-ACCEPTED` / `TRANSFER` / `LCI` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform TRANSFER on LCI toward DLA under READ-REQUEST-ACCEPTED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“目标硬件”在“READ-REQUEST-ACCEPTED”下必须对“LCI”执行“传输”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00349` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E004-7D245D52CBFE`<br>`ARINC-615A-3 6.3.1 p.50` | `DLA` / `LCI-ANALYSED` / `SEND` / `INFORMATION-INITIALIZATION-RESPONSE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on INFORMATION-INITIALIZATION-RESPONSE toward APPLICATION under LCI-ANALYSED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“LCI-ANALYSED”下必须对“INFORMATION-INITIALIZATION-RESPONSE”执行“发送”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00350` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E005-432DDCB05AC3`<br>`ARINC-615A-3 6.3.1 p.50` | `DLA` / `INITIALIZATION-REJECTED` / `TERMINATE` / `INFORMATION-OPERATION` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform TERMINATE on INFORMATION-OPERATION toward APPLICATION under INITIALIZATION-REJECTED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“INITIALIZATION-REJECTED”下必须对“INFORMATION-OPERATION”执行“TERMINATE”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00351` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E006-ACD86B335E4E`<br>`ARINC-615A-3 6.3.1 p.50` | `TARGET-HARDWARE` / `INITIALIZATION-ACCEPTED` / `SEND-TFTP-WRITE-REQUEST` / `LCL` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform SEND-TFTP-WRITE-REQUEST on LCL toward DLA under INITIALIZATION-ACCEPTED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“目标硬件”在“INITIALIZATION-ACCEPTED”下必须对“LCL”执行“SEND-TFTP-WRITE-REQUEST”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00352` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E007-BABEAA841AA6`<br>`ARINC-615A-3 6.3.1 p.50` | `DLA` / `REQUEST-RECEIVED` / `ACKNOWLEDGE` / `LCL-WRITE-REQUEST` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform ACKNOWLEDGE on LCL-WRITE-REQUEST toward TARGET-HARDWARE under REQUEST-RECEIVED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“REQUEST-RECEIVED”下必须对“LCL-WRITE-REQUEST”执行“确认”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00353` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E008-C31F4710028B`<br>`ARINC-615A-3 6.3.1 p.50` | `TARGET-HARDWARE` / `ACKNOWLEDGED` / `TRANSFER` / `LCL` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform TRANSFER on LCL toward DLA under ACKNOWLEDGED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“目标硬件”在“ACKNOWLEDGED”下必须对“LCL”执行“传输”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00354` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E009-CA2FDC811E4A`<br>`ARINC-615A-3 6.3.1 p.50` | `DLA` / `LCL-RECEIVED` / `SEND` / `TH-INFORMATION` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on TH-INFORMATION toward APPLICATION under LCL-RECEIVED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“LCL-RECEIVED”下必须对“TH-INFORMATION”执行“发送”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00355` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E010-B9802EF2D3EA`<br>`ARINC-615A-3 6.3.1 p.50` | `TARGET-HARDWARE` / `STATUS-UPDATE-DUE` / `SEND-TFTP-WRITE-REQUEST` / `LCS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform SEND-TFTP-WRITE-REQUEST on LCS toward DLA under STATUS-UPDATE-DUE; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“目标硬件”在“STATUS-UPDATE-DUE”下必须对“LCS”执行“SEND-TFTP-WRITE-REQUEST”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00356` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E011-1AC058091969`<br>`ARINC-615A-3 6.3.1 p.50` | `TARGET-HARDWARE` / `WRITE-REQUEST-ACKNOWLEDGED` / `TRANSFER` / `LCS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform TRANSFER on LCS toward DLA under WRITE-REQUEST-ACKNOWLEDGED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“目标硬件”在“WRITE-REQUEST-ACKNOWLEDGED”下必须对“LCS”执行“传输”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00357` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E012-641E73AF20EF`<br>`ARINC-615A-3 6.3.1 p.50` | `DLA` / `LCS-RECEIVED` / `SEND` / `INFORMATION-STATUS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on INFORMATION-STATUS toward APPLICATION under LCS-RECEIVED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“LCS-RECEIVED”下必须对“INFORMATION-STATUS”执行“发送”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00358` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E013-73850A1986EF`<br>`ARINC-615A-3 6.3.1 p.50` | `TARGET-HARDWARE` / `OPERATION-COMPLETION-STATE` / `REPEAT-OR-TERMINATE` / `LCS-STATUS-CYCLE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform REPEAT-OR-TERMINATE on LCS-STATUS-CYCLE toward DLA under OPERATION-COMPLETION-STATE; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“目标硬件”在“OPERATION-COMPLETION-STATE”下必须对“LCS-STATUS-CYCLE”执行“REPEAT-OR-TERMINATE”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00359` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E001-C4F05B5E63B6`<br>`ARINC-615A-3 6.3.2 p.53` | `DLA` / `OPERATION-START` / `RECEIVE` / `TH-UPLOADING-INITIALIZATION` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor DLA shall perform RECEIVE on TH-UPLOADING-INITIALIZATION toward APPLICATION under OPERATION-START; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“OPERATION-START”下必须对“TH-UPLOADING-INITIALIZATION”执行“接收”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00360` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E002-77866A816D15`<br>`ARINC-615A-3 6.3.2 p.53` | `DLA` / `INITIALIZATION` / `SEND-TFTP-READ-REQUEST` / `LUI` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor DLA shall perform SEND-TFTP-READ-REQUEST on LUI toward TARGET-HARDWARE under INITIALIZATION; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“INITIALIZATION”下必须对“LUI”执行“SEND-TFTP-READ-REQUEST”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00361` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E003-23D0F1A6F303`<br>`ARINC-615A-3 6.3.2 p.53` | `TARGET-HARDWARE` / `READ-REQUEST-ACCEPTED` / `TRANSFER` / `LUI` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE shall perform TRANSFER on LUI toward DLA under READ-REQUEST-ACCEPTED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“目标硬件”在“READ-REQUEST-ACCEPTED”下必须对“LUI”执行“传输”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00362` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E004-30A7E36B1CAC`<br>`ARINC-615A-3 6.3.2 p.53` | `DLA` / `LUI-ANALYSED` / `SEND` / `UPLOADING-INITIALIZATION-RESPONSE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor DLA shall perform SEND on UPLOADING-INITIALIZATION-RESPONSE toward APPLICATION under LUI-ANALYSED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“LUI-ANALYSED”下必须对“UPLOADING-INITIALIZATION-RESPONSE”执行“发送”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00363` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E005-1CC34400D27E`<br>`ARINC-615A-3 6.3.2 p.53` | `DLA` / `INITIALIZATION-ACCEPTED` / `SEND` / `LOAD-LIST` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor DLA shall perform SEND on LOAD-LIST toward TARGET-HARDWARE under INITIALIZATION-ACCEPTED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“INITIALIZATION-ACCEPTED”下必须对“LOAD-LIST”执行“发送”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00364` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E006-298771587D83`<br>`ARINC-615A-3 6.3.2 p.53` | `DLA` / `LIST-NOT-YET-ACCEPTED` / `WAIT` / `LUS-0001` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor DLA shall perform WAIT on LUS-0001 toward TARGET-HARDWARE under LIST-NOT-YET-ACCEPTED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“LIST-NOT-YET-ACCEPTED”下必须对“LUS-0001”执行“等待”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00365` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E007-7726A816FFE7`<br>`ARINC-615A-3 6.3.2 p.53` | `DATA-LOADER` / `LIST-ACCEPTED` / `SEND-TFTP-WRITE-REQUEST` / `LUR` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor DATA-LOADER shall perform SEND-TFTP-WRITE-REQUEST on LUR toward TARGET-HARDWARE under LIST-ACCEPTED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器”在“LIST-ACCEPTED”下必须对“LUR”执行“SEND-TFTP-WRITE-REQUEST”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00366` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E008-F1D3B51077A3`<br>`ARINC-615A-3 6.3.2 p.53` | `TARGET-HARDWARE` / `REQUEST-RECEIVED` / `ACKNOWLEDGE` / `LUR-WRITE-REQUEST` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE shall perform ACKNOWLEDGE on LUR-WRITE-REQUEST toward DATA-LOADER under REQUEST-RECEIVED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“目标硬件”在“REQUEST-RECEIVED”下必须对“LUR-WRITE-REQUEST”执行“确认”，接收方为“数据加载器”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00367` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E009-9A7CD75981CB`<br>`ARINC-615A-3 6.3.2 p.53` | `DATA-LOADER` / `ACKNOWLEDGED` / `TRANSFER` / `LUR` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor DATA-LOADER shall perform TRANSFER on LUR toward TARGET-HARDWARE under ACKNOWLEDGED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器”在“ACKNOWLEDGED”下必须对“LUR”执行“传输”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00368` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E001-0056C38BAE97`<br>`ARINC-615A-3 6.3.2 p.54` | `TARGET-HARDWARE` / `FILE-SELECTED` / `SEND-TFTP-READ-REQUEST` / `REQUESTED-UPLOAD-FILE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE shall perform SEND-TFTP-READ-REQUEST on REQUESTED-UPLOAD-FILE toward DLA under FILE-SELECTED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“目标硬件”在“FILE-SELECTED”下必须对“REQUESTED-UPLOAD-FILE”执行“SEND-TFTP-READ-REQUEST”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00369` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E002-9E4B69ABC6C0`<br>`ARINC-615A-3 6.3.2 p.54` | `DLA` / `REQUESTED-FILE-UNAVAILABLE` / `SEND` / `FILE-NOT-AVAILABLE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor DLA shall perform SEND on FILE-NOT-AVAILABLE toward TARGET-HARDWARE under REQUESTED-FILE-UNAVAILABLE; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“REQUESTED-FILE-UNAVAILABLE”下必须对“FILE-NOT-AVAILABLE”执行“发送”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00370` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E003-4CF8C989BD2D`<br>`ARINC-615A-3 6.3.2 p.54` | `DLA` / `REQUESTED-FILE-AVAILABLE` / `TRANSFER` / `REQUESTED-UPLOAD-FILE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor DLA shall perform TRANSFER on REQUESTED-UPLOAD-FILE toward TARGET-HARDWARE under REQUESTED-FILE-AVAILABLE; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“REQUESTED-FILE-AVAILABLE”下必须对“REQUESTED-UPLOAD-FILE”执行“传输”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00371` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E004-FA670B42C1F5`<br>`ARINC-615A-3 6.3.2 p.54` | `TARGET-HARDWARE` / `FILE-RECEIVED` / `WRITE` / `LUS-FILE-STATUS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE shall perform WRITE on LUS-FILE-STATUS toward TARGET-MEMORY under FILE-RECEIVED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“目标硬件”在“FILE-RECEIVED”下必须对“LUS-FILE-STATUS”执行“WRITE”，接收方为“TARGET-MEMORY”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00372` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E005-B45D394BBCF7`<br>`ARINC-615A-3 6.3.2 p.54` | `TARGET-HARDWARE` / `MORE-FILES-REQUIRED` / `REPEAT` / `UPLOAD-FILE-THREAD` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE shall perform REPEAT on UPLOAD-FILE-THREAD toward DLA under MORE-FILES-REQUIRED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“目标硬件”在“MORE-FILES-REQUIRED”下必须对“UPLOAD-FILE-THREAD”执行“REPEAT”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00373` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E006-5AECD60FFEA3`<br>`ARINC-615A-3 6.3.2 p.54` | `TARGET-HARDWARE` / `STATUS-UPDATE-DUE` / `SEND-TFTP-WRITE-REQUEST` / `LUS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE shall perform SEND-TFTP-WRITE-REQUEST on LUS toward DLA under STATUS-UPDATE-DUE; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“目标硬件”在“STATUS-UPDATE-DUE”下必须对“LUS”执行“SEND-TFTP-WRITE-REQUEST”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00374` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E007-1C729672C57C`<br>`ARINC-615A-3 6.3.2 p.54` | `TARGET-HARDWARE` / `WRITE-REQUEST-ACKNOWLEDGED` / `TRANSFER` / `LUS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor TARGET-HARDWARE shall perform TRANSFER on LUS toward DLA under WRITE-REQUEST-ACKNOWLEDGED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“目标硬件”在“WRITE-REQUEST-ACKNOWLEDGED”下必须对“LUS”执行“传输”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00375` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E008-772971415EE7`<br>`ARINC-615A-3 6.3.2 p.54` | `DLA` / `LUS-RECEIVED` / `SEND` / `UPLOAD-INFORMATION-STATUS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor DLA shall perform SEND on UPLOAD-INFORMATION-STATUS toward APPLICATION under LUS-RECEIVED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“LUS-RECEIVED”下必须对“UPLOAD-INFORMATION-STATUS”执行“发送”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00376` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E009-0243DF6FD28F`<br>`ARINC-615A-3 6.3.2 p.54` | `DLA` / `UPLOAD-COMPLETION-STATE` / `REPEAT-OR-TERMINATE` / `UPLOAD-STATUS-CYCLE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | Actor DLA shall perform REPEAT-OR-TERMINATE on UPLOAD-STATUS-CYCLE toward APPLICATION under UPLOAD-COMPLETION-STATE; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“UPLOAD-COMPLETION-STATE”下必须对“UPLOAD-STATUS-CYCLE”执行“REPEAT-OR-TERMINATE”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00377` | `SU-ARINC-615A-3-SECTION-6-3-5-SEQUENCE-CHART-E001-9F14C8F561CB`<br>`ARINC-615A-3 6.3.5 p.63` | `DLA` / `INTERRUPTION-START` / `RECEIVE` / `ABORT-REQUEST` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform RECEIVE on ABORT-REQUEST toward APPLICATION under INTERRUPTION-START; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“INTERRUPTION-START”下必须对“ABORT-REQUEST”执行“接收”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00378` | `SU-ARINC-615A-3-SECTION-6-3-5-SEQUENCE-CHART-E002-ADCFF3068CA9`<br>`ARINC-615A-3 6.3.5 p.63` | `DLA` / `ABORT-REQUESTED` / `WAIT` / `STATUS-FILE-WRITE-REQUEST` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform WAIT on STATUS-FILE-WRITE-REQUEST toward TARGET-HARDWARE under ABORT-REQUESTED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“ABORT-REQUESTED”下必须对“STATUS-FILE-WRITE-REQUEST”执行“等待”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00379` | `SU-ARINC-615A-3-SECTION-6-3-5-SEQUENCE-CHART-E003-F48598C39EB0`<br>`ARINC-615A-3 6.3.5 p.63` | `TARGET-HARDWARE` / `STATUS-AVAILABLE` / `SEND-TFTP-WRITE-REQUEST` / `LCS-LUS-OR-LNS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform SEND-TFTP-WRITE-REQUEST on LCS-LUS-OR-LNS toward DLA under STATUS-AVAILABLE; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“目标硬件”在“STATUS-AVAILABLE”下必须对“LCS-LUS-OR-LNS”执行“SEND-TFTP-WRITE-REQUEST”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00380` | `SU-ARINC-615A-3-SECTION-6-3-5-SEQUENCE-CHART-E004-CE12F9C3643D`<br>`ARINC-615A-3 6.3.5 p.63` | `DLA` / `WRITE-REQUEST-RECEIVED` / `SEND` / `ABORT-ERROR` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on ABORT-ERROR toward TARGET-HARDWARE under WRITE-REQUEST-RECEIVED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“WRITE-REQUEST-RECEIVED”下必须对“ABORT-ERROR”执行“发送”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00381` | `SU-ARINC-615A-3-SECTION-6-3-5-SEQUENCE-CHART-E005-62BABD65DCA2`<br>`ARINC-615A-3 6.3.5 p.63` | `TARGET-HARDWARE` / `ABORT-ERROR-RECEIVED` / `STOP` / `NONSTATUS-FILE-TRANSFERS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform STOP on NONSTATUS-FILE-TRANSFERS toward DLA under ABORT-ERROR-RECEIVED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“目标硬件”在“ABORT-ERROR-RECEIVED”下必须对“NONSTATUS-FILE-TRANSFERS”执行“STOP”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00382` | `SU-ARINC-615A-3-SECTION-6-3-5-SEQUENCE-CHART-E006-697ED629B1F1`<br>`ARINC-615A-3 6.3.5 p.63` | `TARGET-HARDWARE` / `ACTIVITIES-STOPPED` / `TRANSFER` / `ABORT-CONFIRMATION-STATUS-FILE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor TARGET-HARDWARE shall perform TRANSFER on ABORT-CONFIRMATION-STATUS-FILE toward DLA under ACTIVITIES-STOPPED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“目标硬件”在“ACTIVITIES-STOPPED”下必须对“ABORT-CONFIRMATION-STATUS-FILE”执行“传输”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00383` | `SU-ARINC-615A-3-SECTION-6-3-5-SEQUENCE-CHART-E007-0E8514BE5C06`<br>`ARINC-615A-3 6.3.5 p.63` | `DLA` / `ABORT-STATUS-RECEIVED` / `SEND` / `INFORMATION-OR-UPLOAD-OR-DOWNLOAD-STATUS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform SEND on INFORMATION-OR-UPLOAD-OR-DOWNLOAD-STATUS toward APPLICATION under ABORT-STATUS-RECEIVED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“ABORT-STATUS-RECEIVED”下必须对“INFORMATION-OR-UPLOAD-OR-DOWNLOAD-STATUS”执行“发送”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00384` | `SU-ARINC-615A-3-SECTION-6-3-5-SEQUENCE-CHART-E008-F805E5E804BC`<br>`ARINC-615A-3 6.3.5 p.63` | `DLA` / `ABORT-CONFIRMED` / `TERMINATE` / `INTERRUPTION-MODE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | Actor DLA shall perform TERMINATE on INTERRUPTION-MODE toward APPLICATION under ABORT-CONFIRMED; evidence is the resulting ORDER-DIRECTION-BRANCH-OBSERVABLE.<br>参与者“数据加载器应用层”在“ABORT-CONFIRMED”下必须对“INTERRUPTION-MODE”执行“TERMINATE”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00385` | `SU-ARINC-615A-3-5-3-3-P044-PROSE-SENTENCE-005-36878C1F8E7E`<br>`ARINC-615A-3 5.3.3 p.32` | `FIND-PROTOCOL` / `WHEN-FIND-IMPLEMENTED` / `USE-UDP-PORT-1001` / `UDP-PORT-1001` / `FIND-PORT-1001-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | When a FIND initiator or FIND host is implemented, FIND shall use UDP port 1001 decimal.<br>在实现 FIND 发起方或 FIND 主机时，FIND 必须使用十进制 UDP 端口 1001。 | — | — |
| `CRS-M1-00386` | `SU-ARINC-615A-3-3-1-P107-PROSE-SENTENCE-006-B1ED10DE43C7`<br>`ARINC-615A-3 3-1 p.95` | `DATA-LOADER` / `WHEN-FIND-PATH-CARRIES-TRAFFIC-AND-BEFORE-DATA-LOAD` / `RUN-FIND-AT-LEAST-ONCE` / `FIND-REQUEST` / `FIND-PRELOAD-RUN-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When the path can carry FIND traffic, the data loader shall run FIND at least once before data-load operations.<br>在路径能够承载 FIND 业务时，数据加载器必须在数据加载操作前至少运行一次 FIND。 | — | — |
| `CRS-M1-00387` | `SU-ARINC-615A-3-3-1-P107-PROSE-SENTENCE-007-9166DCC81508`<br>`ARINC-615A-3 3-1 p.95` | `DATA-LOADER` / `WHEN-FIND-PATH-CARRIES-TRAFFIC-AND-BEFORE-LATER-OPERATION` / `MAY-RERUN-FIND-AND-REGISTER-ANSWERS` / `FIND-REQUEST, FIND-ANSWER` / `FIND-OPTIONAL-RERUN-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | On a FIND-capable path, the data loader may run FIND again and register answers before each later operation.<br>在能够承载 FIND 的路径上，数据加载器可以在后续每次操作前再次运行 FIND 并登记应答。 | — | — |
| `CRS-M1-00388` | `SU-ARINC-615A-3-3-1-P107-PROSE-SENTENCE-011-AD843D1C9EDF`<br>`ARINC-615A-3 3-1 p.95` | `FIND-PROTOCOL` / `WHEN-FIND-IMPLEMENTED` / `USE-WELL-KNOWN-UDP-PORT-1001` / `UDP-PORT-1001` / `FIND-ATTACHMENT-PORT-1001-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | FIND request and answer packets shall use the well-known UDP port 1001 decimal.<br>FIND 请求与应答分组必须使用众所周知的十进制 UDP 端口 1001。 | — | — |
| `CRS-M1-00389` | `SU-ARINC-615A-3-3-1-P107-PROSE-SENTENCE-012-AEB96A80314F`<br>`ARINC-615A-3 3-1 p.95` | `FIND-PROTOCOL` / `WHEN-FIND-IMPLEMENTED` / `USE-SAME-PORT-FOR-REQUEST-AND-ANSWER` / `FIND-REQUEST, FIND-ANSWER, UDP-PORT-1001` / `FIND-SHARED-PORT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The FIND request packet and the FIND answer packet shall use the same UDP port number.<br>FIND 请求分组与 FIND 应答分组必须使用同一 UDP 端口号。 | — | — |
| `CRS-M1-00390` | `SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-003-1E8680AD6287`<br>`ARINC-615A-3 3-2 p.96` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `REGISTER-VALID-FIND-ANSWERS-AS-LOAD-TARGETS` / `VALID-FIND-ANSWERS, LOAD-TARGET-REGISTRATION` / `VALID-FIND-ANSWER-REGISTRATION-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | When FIND is implemented, the data loader shall register all valid FIND answers as possible load targets.<br>在实现 FIND 时，数据加载器必须把所有有效 FIND 应答登记为可能的加载目标。 | — | — |
| `CRS-M1-00391` | `SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-005-3CE166EDA700`<br>`ARINC-615A-3 3-2 p.96` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `ANSWER-FIND-REQUEST-WITHIN-TWO-SECOND-UPPER-BOUND` / `FIND-ANSWER, FIND-HOST-TIMEOUT-UPPER-BOUND-2-S` / `FIND-HOST-ANSWER-WITHIN-TWO-SECOND-UPPER-BOUND-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | When FIND is implemented, a FIND host shall send its FIND answer within a two-second upper bound of receiving a legal request. An earlier answer satisfies the deadline; the three-second registration window does not extend this host bound.<br>在实现 FIND 时，FIND 主机必须在收到合法请求后的两秒上界内发出 FIND 应答。更早的应答满足该期限；三秒登记窗口不能延长该主机上界。 | `FIXED-SOURCE-CONSTANT` / `FIND-HOST-TIMEOUT-2-S` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `0..2 s` / evidence: SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-005-3CE166EDA700 | — |
| `CRS-M1-00392` | `SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-006-E98F49FBFBDF`<br>`ARINC-615A-3 3-2 p.96` | `FIND-INITIATOR` / `WHEN-FIND-IMPLEMENTED` / `TAKE-NEEDED-INFORMATION-FROM-MESSAGE-STRUCTURE-OR-FIND-PACKET-DATA` / `MESSAGE-STRUCTURE, FIND-PACKET-DATA` / `FIND-INFORMATION-LOCATION-ALTERNATIVE-OBSERVABLE` | `MAY` / `CONDITIONAL-REQUIRED` | `APPLICABLE-SUPPORTING` | When FIND is implemented, the initiator shall take needed information from the message structure or from FIND packet data. This records the alternative locations; it does not activate AFDX and does not permit omitting needed information.<br>在实现 FIND 时，发起方必须从报文结构或 FIND 分组数据中取得所需信息。这记录两种承载位置，不激活 AFDX，也不允许省略所需信息。 | — | — |
| `CRS-M1-00393` | `SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-010-76E6AE59C360`<br>`ARINC-615A-3 3-2 p.96` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `SEND-NO-ANSWER-TO-ILLEGAL-FIND-REQUEST` / `ILLEGAL-FIND-REQUEST` / `FIND-ILLEGAL-REQUEST-SILENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | A FIND host shall send no answer to an illegal or invalid FIND request.<br>对于非法或无效的 FIND 请求，FIND 主机不得发出应答。 | — | — |
| `CRS-M1-00394` | `SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-011-A1CA1EF64C11`<br>`ARINC-615A-3 3-2 p.96` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `IGNORE-INVALID-FIND-ANSWER` / `INVALID-FIND-ANSWER` / `FIND-INVALID-ANSWER-IGNORE-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The data loader shall ignore an invalid FIND answer.<br>数据加载器必须忽略无效的 FIND 应答。 | — | — |
| `CRS-M1-00395` | `SU-ARINC-615A-3-3-4-P108-PROSE-SENTENCE-001-DB0FEBBE9664`<br>`ARINC-615A-3 3-4 p.96` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `SET-IRQ-SOURCE-MAC-TO-DATA-LOADER` / `IRQ-SOURCE-MAC` / `IRQ-SOURCE-MAC-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | In an Information Request, the data loader shall set the source MAC address to its own MAC address.<br>在信息请求中，数据加载器必须把源 MAC 地址设为自己的 MAC 地址。 | — | — |
| `CRS-M1-00396` | `SU-ARINC-615A-3-3-4-P108-PROSE-SENTENCE-002-412B0FD7B45D`<br>`ARINC-615A-3 3-4 p.96` | `DATA-LOADER` / `WHEN-FIND-PATH-CARRIES-TRAFFIC` / `SET-IRQ-DESTINATION-MAC-TO-UNICAST-MULTICAST-OR-BROADCAST` / `IRQ-DESTINATION-MAC` / `IRQ-DESTINATION-MAC-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When the path can carry FIND, the data loader shall set the Information Request destination MAC to a unicast, multicast or broadcast MAC.<br>在路径能够承载 FIND 时，数据加载器必须把信息请求的目的 MAC 设为单播、组播或广播 MAC。 | — | — |
| `CRS-M1-00397` | `SU-ARINC-615A-3-ATTACHMENT-3-P109-PROSE-SENTENCE-003-B443A5630F89`<br>`ARINC-615A-3 ATTACHMENT-3 p.97` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `SET-IRQ-SOURCE-IP-TO-DATA-LOADER` / `IRQ-SOURCE-IP` / `IRQ-SOURCE-IP-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | In an Information Request, the data loader shall set the source IP address to its own IP address.<br>在信息请求中，数据加载器必须把源 IP 地址设为自己的 IP 地址。 | — | — |
| `CRS-M1-00398` | `SU-ARINC-615A-3-ATTACHMENT-3-P109-PROSE-SENTENCE-004-0BFE8D84B7A9`<br>`ARINC-615A-3 ATTACHMENT-3 p.97` | `DATA-LOADER` / `WHEN-FIND-PATH-CARRIES-TRAFFIC` / `SET-IRQ-DESTINATION-IP-TO-UNICAST-MULTICAST-OR-BROADCAST` / `IRQ-DESTINATION-IP` / `IRQ-DESTINATION-IP-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When the path can carry FIND, the data loader shall set the Information Request destination IP to a unicast, multicast or broadcast IP, including limited or all-ones broadcast.<br>在路径能够承载 FIND 时，数据加载器必须把信息请求的目的 IP 设为单播、组播或广播 IP，包括有限广播或全 1 广播。 | — | — |
| `CRS-M1-00399` | `SU-ARINC-615A-3-ATTACHMENT-3-P109-PROSE-SENTENCE-005-DC8D7B76A7B9`<br>`ARINC-615A-3 ATTACHMENT-3 p.97` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `SET-IRQ-OPCODE-TO-0001` / `IRQ-OPCODE-0001` / `IRQ-OPCODE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The data loader shall set the Information Request opcode to 0x0001.<br>数据加载器必须把信息请求操作码设为 0x0001。 | — | — |
| `CRS-M1-00400` | `SU-ARINC-615A-3-ATTACHMENT-3-P109-PROSE-SENTENCE-006-FC8DA6118FFF`<br>`ARINC-615A-3 ATTACHMENT-3 p.97` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `SET-IRQ-DATA-LIST-TO-ASCII-NUL` / `IRQ-DATA-LIST, ASCII-NUL` / `IRQ-DATA-LIST-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The data loader shall set the Information Request data list to a single ASCII NUL terminator.<br>数据加载器必须把信息请求数据表设为单个 ASCII 空字符终止符。 | — | — |
| `CRS-M1-00401` | `SU-ARINC-615A-3-ATTACHMENT-3-P109-PROSE-SENTENCE-007-99F468D5D311`<br>`ARINC-615A-3 ATTACHMENT-3 p.97` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `TERMINATE-IRQ-PACKET-WITH-DLE` / `IRQ-PACKET-TERMINATOR-DLE` / `IRQ-TERMINATOR-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The data loader shall terminate the Information Request packet with 0x10.<br>数据加载器必须以 0x10 结束信息请求分组。 | — | — |
| `CRS-M1-00402` | `SU-ARINC-615A-3-3-5-P109-PROSE-SENTENCE-001-D2A70FEFE065`<br>`ARINC-615A-3 3-5 p.97` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `SET-IAN-SOURCE-MAC-TO-FIND-HOST` / `IAN-SOURCE-MAC` / `IAN-SOURCE-MAC-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | In an Information Answer, the FIND host shall set the source MAC address to the target-hardware MAC address.<br>在信息应答中，FIND 主机必须把源 MAC 地址设为目标硬件 MAC 地址。 | — | — |
| `CRS-M1-00403` | `SU-ARINC-615A-3-3-5-P109-PROSE-SENTENCE-002-21D8C06816D1`<br>`ARINC-615A-3 3-5 p.97` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `SET-IAN-DESTINATION-MAC-TO-ASSOCIATED-IRQ-SOURCE-MAC` / `IAN-DESTINATION-MAC` / `IAN-DESTINATION-MAC-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The FIND host shall set the Information Answer destination MAC to the source MAC of the associated Information Request.<br>FIND 主机必须把信息应答的目的 MAC 设为对应信息请求的源 MAC。 | — | — |
| `CRS-M1-00404` | `SU-ARINC-615A-3-3-5-P109-PROSE-SENTENCE-003-E5DBDB9636E9`<br>`ARINC-615A-3 3-5 p.97` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `SET-IAN-SOURCE-IP-TO-FIND-HOST` / `IAN-SOURCE-IP` / `IAN-SOURCE-IP-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | In an Information Answer, the FIND host shall set the source IP address to the target-hardware IP address.<br>在信息应答中，FIND 主机必须把源 IP 地址设为目标硬件 IP 地址。 | — | — |
| `CRS-M1-00405` | `SU-ARINC-615A-3-3-5-P109-PROSE-SENTENCE-004-98DCC47DCB2B`<br>`ARINC-615A-3 3-5 p.97` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `SET-IAN-DESTINATION-IP-TO-ASSOCIATED-IRQ-SOURCE-IP` / `IAN-DESTINATION-IP` / `IAN-DESTINATION-IP-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The FIND host shall set the Information Answer destination IP to the source IP of the associated Information Request.<br>FIND 主机必须把信息应答的目的 IP 设为对应信息请求的源 IP。 | — | — |
| `CRS-M1-00406` | `SU-ARINC-615A-3-3-5-P109-PROSE-SENTENCE-005-4D7FB8BC839C`<br>`ARINC-615A-3 3-5 p.97` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `SET-IAN-OPCODE-TO-0002` / `IAN-OPCODE-0002` / `IAN-OPCODE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The FIND host shall set the Information Answer opcode to 0x0002.<br>FIND 主机必须把信息应答操作码设为 0x0002。 | — | — |
| `CRS-M1-00407` | `SU-ARINC-615A-3-3-5-P109-PROSE-SENTENCE-007-0F2D63CA1D3E`<br>`ARINC-615A-3 3-5 p.97` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `ENCODE-EMPTY-IAN-PARAMETER-AS-SINGLE-NUL` / `EMPTY-IAN-PARAMETER, ASCII-NUL` / `IAN-EMPTY-FIELD-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The FIND host shall encode an empty Information Answer parameter as a single ASCII NUL byte.<br>FIND 主机必须把空的信息应答参数编码为单个 ASCII 空字节。 | — | — |
| `CRS-M1-00408` | `SU-ARINC-615A-3-3-5-P109-PROSE-SENTENCE-008-D8483D058800`<br>`ARINC-615A-3 3-5 p.97` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `OMIT-EMBEDDED-NUL-FROM-IAN-STRINGS` / `IAN-PARAMETER-STRING` / `IAN-NO-EMBEDDED-NUL-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The FIND host shall omit embedded NUL bytes from available Information Answer parameter strings.<br>FIND 主机必须从已提供的信息应答参数字符串中省略内嵌空字节。 | — | — |
| `CRS-M1-00409` | `SU-ARINC-615A-3-3-5-P109-PROSE-SENTENCE-009-2DD2663EB0A1`<br>`ARINC-615A-3 3-5 p.97` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `TERMINATE-IAN-PACKET-WITH-DLE` / `IAN-PACKET-TERMINATOR-DLE` / `IAN-TERMINATOR-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The FIND host shall terminate the Information Answer packet with 0x10.<br>FIND 主机必须以 0x10 结束信息应答分组。 | — | — |
| `CRS-M1-00410` | `SU-ARINC-615A-3-ATTACHMENT-3-P110-PROSE-SENTENCE-012-DB234DB803F9`<br>`ARINC-615A-3 ATTACHMENT-3 p.98` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `ENCODE-IAN-PARAMETERS-AS-NUL-TERMINATED-STRINGS-IN-SECTION-3-6-ORDER` / `IAN-PARAMETER-STRINGS` / `IAN-PARAMETER-ORDER-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The FIND host shall encode Information Answer parameter values as NUL-terminated strings in Attachment 3 section 6 order.<br>FIND 主机必须按附件 3 第 6 节顺序，把信息应答参数值编码为空字符终止字符串。 | — | — |
| `CRS-M1-00411` | `SU-ARINC-615A-3-ATTACHMENT-3-P110-PROSE-SENTENCE-013-48CB9FF4518D`<br>`ARINC-615A-3 ATTACHMENT-3 p.98` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `LIMIT-TARGET-HARDWARE-IDENTIFIER-TO-15-CHARACTERS-EXCLUDING-TERMINATOR` / `TARGET-HARDWARE-IDENTIFIER, LENGTH-15` / `THW-ID-LENGTH-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The FIND host shall limit Target Hardware Identifier to 15 characters excluding the terminator.<br>FIND 主机必须把目标硬件标识符限制为不含终止符的 15 个字符。 | — | — |
| `CRS-M1-00412` | `SU-ARINC-615A-3-ATTACHMENT-3-P110-PROSE-SENTENCE-014-913B305AF452`<br>`ARINC-615A-3 ATTACHMENT-3 p.98` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `LIMIT-TARGET-TYPE-NAME-TO-8-CHARACTERS-EXCLUDING-TERMINATOR` / `TARGET-TYPE-NAME, LENGTH-8` / `TARGET-TYPE-NAME-LENGTH-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The FIND host shall limit Target Type Name to 8 characters excluding the terminator.<br>FIND 主机必须把目标类型名限制为不含终止符的 8 个字符。 | — | — |
| `CRS-M1-00413` | `SU-ARINC-615A-3-ATTACHMENT-3-P110-PROSE-SENTENCE-015-14EF51A05AEA`<br>`ARINC-615A-3 ATTACHMENT-3 p.98` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `LIMIT-TARGET-POSITION-TO-8-CHARACTERS-EXCLUDING-TERMINATOR` / `TARGET-POSITION, LENGTH-8` / `TARGET-POSITION-LENGTH-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The FIND host shall limit Target Position to 8 characters excluding the terminator.<br>FIND 主机必须把目标位置限制为不含终止符的 8 个字符。 | — | — |
| `CRS-M1-00414` | `SU-ARINC-615A-3-ATTACHMENT-3-P110-PROSE-SENTENCE-016-22BA44DB74A6`<br>`ARINC-615A-3 ATTACHMENT-3 p.98` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `LIMIT-LITERAL-NAME-TO-20-CHARACTERS-EXCLUDING-TERMINATOR` / `LITERAL-NAME, LENGTH-20` / `LITERAL-NAME-LENGTH-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The FIND host shall limit Literal Name to 20 characters excluding the terminator.<br>FIND 主机必须把字面名限制为不含终止符的 20 个字符。 | — | — |
| `CRS-M1-00415` | `SU-ARINC-615A-3-ATTACHMENT-3-P110-PROSE-SENTENCE-017-4A05E0BB2809`<br>`ARINC-615A-3 ATTACHMENT-3 p.98` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `ENCODE-MANUFACTURER-CODE-AS-3-CHARACTERS-EXCLUDING-TERMINATOR` / `MANUFACTURER-CODE, LENGTH-3` / `MANUFACTURER-CODE-LENGTH-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | The FIND host shall encode Manufacturer Code as 3 characters excluding the terminator.<br>FIND 主机必须把制造商代码编码为不含终止符的 3 个字符。 | — | — |
| `CRS-M1-00416` | `SU-ARINC-615A-3-5-4-4-P050-PROSE-SENTENCE-007-CA89CD0344A9`<br>`ARINC-615A-3 5.4.4 p.38` | `DATA-LOADER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `IMPLEMENT-BOTH-MEDIA-DEFINED-OPERATOR-DEFINED-DOWNLOAD` / `MEDIA-DEFINED, OPERATOR-DEFINED` / `IMPLEMENT-BOTH-MEDIA-DEFINED-OPERATOR-DEFINED-DOWNLOAD-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the data loader shall implement both Media Defined and Operator Defined DOWNLOAD.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，数据加载器必须实现 both 媒体定义 and 操作员定义 DOWNLOAD。 | — | — |
| `CRS-M1-00417` | `SU-ARINC-615A-3-5-4-4-P050-PROSE-SENTENCE-008-EB64770DFDD9`<br>`ARINC-615A-3 5.4.4 p.38` | `TARGET-HARDWARE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `IMPLEMENT-NONE-ONE-BOTH-DOWNLOAD-MODES` / `MEDIA-DEFINED, OPERATOR-DEFINED` / `IMPLEMENT-NONE-ONE-BOTH-DOWNLOAD-MODES-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the target hardware may implement none, one, or both DOWNLOAD modes.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，目标硬件可以实现 none, one, or both DOWNLOAD modes。 | — | — |
| `CRS-M1-00418` | `SU-ARINC-615A-3-5-4-4-P050-PROSE-SENTENCE-009-DD0255D27FB0`<br>`ARINC-615A-3 5.4.4 p.38` | `DATA-LOADER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `SPECIFY-TFTP-OPTIONS-SUPPLY-DATA-INTEGRITY-CHECK-TRANSFER` / `TFTP-OPTIONS` / `SPECIFY-TFTP-OPTIONS-SUPPLY-DATA-INTEGRITY-CHECK-TRANSFER-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the data loader may specify TFTP options that supply a data-integrity check for the transfer.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，数据加载器可以规定 TFTP options that supply a data-integrity check for the transfer。 | — | — |
| `CRS-M1-00419` | `SU-ARINC-615A-3-5-4-4-P050-PROSE-SENTENCE-010-12B60035E133`<br>`ARINC-615A-3 5.4.4 p.38` | `TARGET-HARDWARE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `IMPLEMENT-TFTP-INTEGRITY-OPTION` / `TFTP-OPTION` / `IMPLEMENT-TFTP-INTEGRITY-OPTION-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the target hardware may implement that TFTP integrity option.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，目标硬件可以实现 that TFTP integrity option。 | — | — |
| `CRS-M1-00420` | `SU-ARINC-615A-3-5-4-4-P050-PROSE-SENTENCE-011-3CF28DC21423`<br>`ARINC-615A-3 5.4.4 p.38` | `DATA-LOADER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `IT-SUPPORTS-OFFERED-CHECK-VALUE-VALIDATE-DATA-TRANSFER` / `CHECK-VALUE` / `IT-SUPPORTS-OFFERED-CHECK-VALUE-VALIDATE-DATA-TRANSFER-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the data loader shall if it supports the offered check value, validate the data transfer.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，数据加载器必须if it supports the offered check value, 校验 the data transfer。 | — | — |
| `CRS-M1-00421` | `SU-ARINC-615A-3-5-4-4-P050-PROSE-SENTENCE-012-D9C78F1A4E4C`<br>`ARINC-615A-3 5.4.4 p.38` | `DATA-LOADER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `TREAT-CHECKSUM-VALIDATION-INFORMATION-ONLY-STILL-EXPORT-FILE` / `CHECKSUM, EXPORT` / `TREAT-CHECKSUM-VALIDATION-INFORMATION-ONLY-STILL-EXPORT-FILE-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the data loader shall treat checksum validation as information only and still export the file.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，数据加载器必须把 校验和 validation as information only and still export the file。 | — | — |
| `CRS-M1-00422` | `SU-ARINC-615A-3-5-4-4-1-P050-PROSE-SENTENCE-004-E7A9E12EDE22`<br>`ARINC-615A-3 5.4.4.1 p.38` | `DATA-LOADER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `USE-LNR-ALREADY-STORED-ARINC-665-PART-MEDIA` / `LNR, ARINC-665-PART` / `USE-LNR-ALREADY-STORED-ARINC-665-PART-MEDIA-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the data loader may use an LNR already stored in an ARINC 665 part on the media.<br>在实现并使用媒体定义 DOWNLOAD 时，数据加载器可以使用 an LNR already stored in an ARINC 665 part on the media。 | — | — |
| `CRS-M1-00423` | `SU-ARINC-615A-3-5-4-4-1-P050-PROSE-SENTENCE-006-F3361F00DCE2`<br>`ARINC-615A-3 5.4.4.1 p.38` | `DATA-LOADER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `EXAMINE-EACH-PART-HEADER-OFFER-HEADERS-WHOSE-DOWNLOAD-BIT-SET` / `DOWNLOAD-BIT, HEADER-FILE` / `EXAMINE-EACH-PART-HEADER-OFFER-HEADERS-WHOSE-DOWNLOAD-BIT-SE-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the data loader shall examine each part header and offer headers whose download bit is set.<br>在实现并使用媒体定义 DOWNLOAD 时，数据加载器必须检查 each part header and 提供 headers whose download bit is set。 | — | — |
| `CRS-M1-00424` | `SU-ARINC-615A-3-5-4-4-1-P050-PROSE-SENTENCE-007-A88849FBE53E`<br>`ARINC-615A-3 5.4.4.1 p.38` | `OPERATOR` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `MORE-THAN-ONE-DOWNLOAD-BIT-HEADER-EXISTS-SELECT-ONE` / `HEADER-FILE` / `MORE-THAN-ONE-DOWNLOAD-BIT-HEADER-EXISTS-SELECT-ONE-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the operator may if more than one download-bit header exists, select one.<br>在实现并使用媒体定义 DOWNLOAD 时，操作员可以if more than one download-bit header exists, 选择 one。 | — | — |
| `CRS-M1-00426` | `SU-ARINC-615A-3-5-4-4-3-P052-PROSE-SENTENCE-002-1036539E638B`<br>`ARINC-615A-3 5.4.4.3 p.40` | `DATA-LOADER` / `WHEN-REMOVABLE-MEDIA-IS-LNR-SOURCE-AND-DOWNLOAD-DESTINATION` / `PROMPT-OPERATOR-REPLACE-SELECT-WRITABLE-MEDIA-BEFORE-STARTING-DOWNLOAD` / `WRITABLE-MEDIA` / `PROMPT-OPERATOR-REPLACE-SELECT-WRITABLE-MEDIA-BEFORE-STARTIN-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When removable media is the LNR source and the destination of downloaded data, the data loader shall prompt the operator to replace or select writable media before starting DOWNLOAD.<br>在可移动媒体既是 LNR 来源又是下载数据目的地时，数据加载器必须在开始 DOWNLOAD 前提示操作员更换或选择可写媒体。 | — | — |
| `CRS-M1-00427` | `SU-ARINC-615A-3-5-4-4-3-P052-PROSE-SENTENCE-003-3B9221D5DF13`<br>`ARINC-615A-3 5.4.4.3 p.40` | `DATA-LOADER` / `WHEN-REMOVABLE-MEDIA-IS-LNR-SOURCE-AND-DOWNLOAD-DESTINATION` / `FAIL-DOWNLOAD-WRITE-STILL-FAILS-AFTER-ASKING-WRITABLE-MEDIA` / `WRITABLE-MEDIA` / `FAIL-DOWNLOAD-WRITE-STILL-FAILS-AFTER-ASKING-WRITABLE-MEDIA-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When removable media is the LNR source and the destination of downloaded data, the data loader shall fail DOWNLOAD if the write still fails after asking for writable media.<br>在可移动媒体既是 LNR 来源又是下载数据目的地时，若在要求可写媒体之后写入仍然失败，数据加载器必须使 DOWNLOAD 失败。 | — | — |
| `CRS-M1-00428` | `SU-ARINC-615A-3-5-4-4-3-P052-PROSE-SENTENCE-004-C40353394C94`<br>`ARINC-615A-3 5.4.4.3 p.40` | `DATA-LOADER` / `WHEN-REMOVABLE-MEDIA-IS-LNR-SOURCE-AND-DOWNLOAD-DESTINATION` / `CREATE-NEW-DNLD-DATA-THW-ID-POS-NUMBER-DIRECTORY-EACH` / `DNLD-DATA` / `CREATE-NEW-DNLD-DATA-THW-ID-POS-NUMBER-DIRECTORY-EACH-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When removable media is the LNR source and the destination of downloaded data, the data loader shall create a new DNLD_DATA_<THW_ID_POS>_<number> directory for each download.<br>在可移动媒体既是 LNR 来源又是下载数据目的地时，数据加载器必须为每次下载新建 DNLD_DATA_<THW_ID_POS>_<number> 目录。 | — | — |
| `CRS-M1-00429` | `SU-ARINC-615A-3-5-4-4-3-P052-PROSE-SENTENCE-008-4B56712D118C`<br>`ARINC-615A-3 5.4.4.3 p.40` | `DATA-LOADER` / `WHEN-REMOVABLE-MEDIA-IS-LNR-SOURCE-AND-DOWNLOAD-DESTINATION` / `CREATE-DNLD-INFO-THW-ID-POS-NUMBER-MANUFACTURER-SPECIFIC-DOWNLOAD` / `DNLD-INFO` / `CREATE-DNLD-INFO-THW-ID-POS-NUMBER-MANUFACTURER-SPECIFIC-DOW-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | When removable media is the LNR source and the destination of downloaded data, the data loader may create DNLD_INFO_<THW_ID_POS>_<number> for manufacturer-specific download information.<br>在可移动媒体既是 LNR 来源又是下载数据目的地时，数据加载器可以为制造商专用下载信息创建 DNLD_INFO_<THW_ID_POS>_<number> 文件。 | — | — |
| `CRS-M1-00430` | `SU-ARINC-615A-3-6-3-3-P070-PROSE-SENTENCE-033-EC6A3B3AFA4A`<br>`ARINC-615A-3 6.3.3 p.58` | `OPERATOR` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `SELECT-MEDIA-TYPE-MEDIA-DEFINED-DOWNLOAD` / `MEDIA-TYPE` / `SELECT-MEDIA-TYPE-MEDIA-DEFINED-DOWNLOAD-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the operator shall select the media type for Media Defined DOWNLOAD.<br>在实现并使用媒体定义 DOWNLOAD 时，操作员必须选择 the media type for 媒体定义 DOWNLOAD。 | — | — |
| `CRS-M1-00431` | `SU-ARINC-615A-3-6-3-3-P070-PROSE-SENTENCE-038-2ED4ABAC4193`<br>`ARINC-615A-3 6.3.3 p.58` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `SEND-STATUS-FILES-WITHIN-ATTACHMENT-4-DLP-MAXIMUM-DELAY` / `LNS, ATTACHMENT-4` / `SEND-STATUS-FILES-WITHIN-ATTACHMENT-4-DLP-MAXIMUM-DELAY-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the target hardware shall send status files within the Attachment 4 DLP maximum delay.<br>在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须发送 状态文件s within the 附件 4 DLP maximum delay。 | — | — |
| `CRS-M1-00432` | `SU-ARINC-615A-3-6-3-3-P070-PROSE-SENTENCE-040-18B50A8E503C`<br>`ARINC-615A-3 6.3.3 p.58` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `FATAL-ERROR-EMIT-STATUS-FILE-MATCHING-CODE-DESCRIPTION-INSIDE-TIMEOUT` / `LNS, STATUS-CODE, STATUS-DESCRIPTION` / `FATAL-ERROR-EMIT-STATUS-FILE-MATCHING-CODE-DESCRIPTION-INSID-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the target hardware shall on fatal error emit a status file with matching code and description inside the timeout.<br>在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须on fatal error emit a 状态文件 with matching code and description inside the timeout。 | — | — |
| `CRS-M1-00433` | `SU-ARINC-615A-3-6-3-3-P070-PROSE-SENTENCE-041-7AC0400C9DB1`<br>`ARINC-615A-3 6.3.3 p.58` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `SEND-STATUS-FILE-IMMEDIATELY-CARRY-ABORT-INTERRUPT` / `ABORT-5-3-2-3-6, INTERRUPT-6-3-6` / `SEND-STATUS-FILE-IMMEDIATELY-CARRY-ABORT-INTERRUPT-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the target hardware may send a status file immediately to carry an abort or interrupt.<br>在实现并使用媒体定义 DOWNLOAD 时，目标硬件可以发送 a 状态文件 immediately to carry an 中止 or interrupt。 | — | — |
| `CRS-M1-00434` | `SU-ARINC-615A-3-6-3-3-P070-PROSE-SENTENCE-050-D8862D88C46E`<br>`ARINC-615A-3 6.3.3 p.58` | `DATA-LOADER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `TARGET-ANSWERS-BEFORE-EXCEPTION-TIMER-ELAPSES-CONTINUE-WITHOUT-WAITING-IT` / `EXCEPTION-TIMER` / `TARGET-ANSWERS-BEFORE-EXCEPTION-TIMER-ELAPSES-CONTINUE-WITHO-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the data loader shall if the target answers before Exception Timer elapses, continue without waiting it out.<br>在实现并使用媒体定义 DOWNLOAD 时，若目标在 Exception Timer 到期前应答，数据加载器必须继续而不把该定时器等待完毕。 | — | — |
| `CRS-M1-00435` | `SU-ARINC-615A-3-6-3-3-P070-PROSE-SENTENCE-051-E812AC346D09`<br>`ARINC-615A-3 6.3.3 p.58` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `MINIMIZE-EXCEPTION-TIMER-SO-SILENT-PHASE-STAYS-SHORT` / `EXCEPTION-TIMER` / `MINIMIZE-EXCEPTION-TIMER-SO-SILENT-PHASE-STAYS-SHORT-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the target hardware shall minimize Exception Timer so the silent phase stays short.<br>在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须尽量缩短 Exception Timer so the silent phase stays short。 | — | — |
| `CRS-M1-00436` | `SU-ARINC-615A-3-6-3-3-P070-PROSE-SENTENCE-052-91F9A68124BD`<br>`ARINC-615A-3 6.3.3 p.58` | `DATA-LOADER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ABORT-DOWNLOAD-NO-NEW-STATUS-FILE-ARRIVES-BEFORE-EXCEPTION-TIMER` / `EXCEPTION-TIMER, LNS` / `ABORT-DOWNLOAD-NO-NEW-STATUS-FILE-ARRIVES-BEFORE-EXCEPTION-T-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the data loader shall abort DOWNLOAD if no new status file arrives before Exception Timer expires.<br>在实现并使用媒体定义 DOWNLOAD 时，数据加载器必须中止 DOWNLOAD if no new 状态文件 arrives before Exception Timer expires。 | — | — |
| `CRS-M1-00437` | `SU-ARINC-615A-3-6-3-4-P073-PROSE-SENTENCE-007-18AB4BEB6990`<br>`ARINC-615A-3 6.3.4 p.61` | `OPERATOR` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ABLE-SELECT-MEDIA-TYPE-OPERATOR-DEFINED-DOWNLOAD` / `MEDIA-TYPE` / `ABLE-SELECT-MEDIA-TYPE-OPERATOR-DEFINED-DOWNLOAD-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the operator shall be able to select the media type for Operator Defined DOWNLOAD.<br>在实现并使用操作员定义 DOWNLOAD 时，操作员必须be able to 选择 the media type for 操作员定义 DOWNLOAD。 | — | — |
| `CRS-M1-00438` | `SU-ARINC-615A-3-6-3-4-P073-PROSE-SENTENCE-012-2ED4ABAC4193`<br>`ARINC-615A-3 6.3.4 p.61` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `SEND-STATUS-FILES-WITHIN-ATTACHMENT-4-DLP-MAXIMUM-DELAY--00981` / `LNS, ATTACHMENT-4` / `SEND-STATUS-FILES-WITHIN-ATTACHMENT-4-DLP-MAXIMUM-DELAY-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the target hardware shall send status files within the Attachment 4 DLP maximum delay.<br>在实现并使用操作员定义 DOWNLOAD 时，目标硬件必须发送 状态文件s within the 附件 4 DLP maximum delay。 | — | — |
| `CRS-M1-00439` | `SU-ARINC-615A-3-6-3-4-P073-PROSE-SENTENCE-014-9F2F8E73FD5D`<br>`ARINC-615A-3 6.3.4 p.61` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `FATAL-ERROR-EMIT-STATUS-FILE-MATCHING-CODE-DESCRIPTION-INSIDE-TIMEOUT--00983` / `LNS, STATUS-CODE, STATUS-DESCRIPTION` / `FATAL-ERROR-EMIT-STATUS-FILE-MATCHING-CODE-DESCRIPTION-INSID-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the target hardware shall on fatal error emit a status file with matching code and description inside the timeout.<br>在实现并使用操作员定义 DOWNLOAD 时，目标硬件必须on fatal error emit a 状态文件 with matching code and description inside the timeout。 | — | — |
| `CRS-M1-00440` | `SU-ARINC-615A-3-6-3-4-P073-PROSE-SENTENCE-015-7AC0400C9DB1`<br>`ARINC-615A-3 6.3.4 p.61` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `SEND-STATUS-FILE-IMMEDIATELY-CARRY-ABORT-INTERRUPT--00984` / `ABORT-5-3-2-3-6, INTERRUPT-6-3-6` / `SEND-STATUS-FILE-IMMEDIATELY-CARRY-ABORT-INTERRUPT-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the target hardware may send a status file immediately to carry an abort or interrupt.<br>在实现并使用操作员定义 DOWNLOAD 时，目标硬件可以发送 a 状态文件 immediately to carry an 中止 or interrupt。 | — | — |
| `CRS-M1-00441` | `SU-ARINC-615A-3-6-3-4-P073-PROSE-SENTENCE-024-D8862D88C46E`<br>`ARINC-615A-3 6.3.4 p.61` | `DATA-LOADER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `TARGET-ANSWERS-BEFORE-EXCEPTION-TIMER-ELAPSES-CONTINUE-WITHOUT-WAITING-IT--00993` / `EXCEPTION-TIMER` / `TARGET-ANSWERS-BEFORE-EXCEPTION-TIMER-ELAPSES-CONTINUE-WITHO-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the data loader shall if the target answers before Exception Timer elapses, continue without waiting it out.<br>在实现并使用操作员定义 DOWNLOAD 时，若目标在 Exception Timer 到期前应答，数据加载器必须继续而不把该定时器等待完毕。 | — | — |
| `CRS-M1-00442` | `SU-ARINC-615A-3-6-3-4-P073-PROSE-SENTENCE-025-E812AC346D09`<br>`ARINC-615A-3 6.3.4 p.61` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `MINIMIZE-EXCEPTION-TIMER-SO-SILENT-PHASE-STAYS-SHORT--00994` / `EXCEPTION-TIMER` / `MINIMIZE-EXCEPTION-TIMER-SO-SILENT-PHASE-STAYS-SHORT-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the target hardware shall minimize Exception Timer so the silent phase stays short.<br>在实现并使用操作员定义 DOWNLOAD 时，目标硬件必须尽量缩短 Exception Timer so the silent phase stays short。 | — | — |
| `CRS-M1-00443` | `SU-ARINC-615A-3-6-3-4-P073-PROSE-SENTENCE-026-464E9E6694A8`<br>`ARINC-615A-3 6.3.4 p.61` | `DATA-LOADER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ABORT-DOWNLOAD-NO-NEW-STATUS-FILE-ARRIVES-BEFORE-EXCEPTION-TIMER--00995` / `EXCEPTION-TIMER, LNS` / `ABORT-DOWNLOAD-NO-NEW-STATUS-FILE-ARRIVES-BEFORE-EXCEPTION-T-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the data loader shall abort DOWNLOAD if no new status file arrives before Exception Timer expires.<br>在实现并使用操作员定义 DOWNLOAD 时，数据加载器必须中止 DOWNLOAD if no new 状态文件 arrives before Exception Timer expires。 | — | — |
| `CRS-M1-00444` | `SU-ARINC-615A-3-6-4-6-P091-PROSE-SENTENCE-016-1532165AA3AE`<br>`ARINC-615A-3 6.4.6 p.79` | `PROTOCOL-FILE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ZERO-TERMINATE-LNR-FILE-NAME-0X00` / `OBJ-0X00` / `ZERO-TERMINATE-LNR-FILE-NAME-0X00-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the protocol-file producer shall zero-terminate LNR File Name with 0x00.<br>在实现并使用媒体定义 DOWNLOAD 时，协议文件生成方必须用 0x00 作为 LNR File Name 的零终止。 | — | — |
| `CRS-M1-00445` | `SU-ARINC-615A-3-6-4-7-P092-PROSE-SENTENCE-028-83077CACF0DC`<br>`ARINC-615A-3 6.4.7 p.80` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `OTHER-STATUS-CODES-IGNORE-DESCRIPTION-CONTENT-WHICH-MAY-HOLD-LEFTOVER` / `DOWNLOAD-STATUS-DESCRIPTION` / `OTHER-STATUS-CODES-IGNORE-DESCRIPTION-CONTENT-WHICH-MAY-HOLD-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer may for other status codes ignore description content, which may hold leftover data.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方对其他状态码可以忽略描述字段内容，其中可能残留数据。 | — | — |
| `CRS-M1-00446` | `SU-ARINC-615A-3-6-4-7-P092-PROSE-SENTENCE-030-B1FB47BD2E90`<br>`ARINC-615A-3 6.4.7 p.80` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `USE-ONLY-PRINTABLE-CHARACTERS-DOWNLOAD-STATUS-DESCRIPTION-NO-CONTROL-CHARACTERS` / `DOWNLOAD-STATUS-DESCRIPTION` / `USE-ONLY-PRINTABLE-CHARACTERS-DOWNLOAD-STATUS-DESCRIPTION-NO-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall use only printable characters in Download Status Description, with no control characters, max 255.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须使用 only printable characters in Download Status Description, with no control characters, max 255。 | — | — |
| `CRS-M1-00447` | `SU-ARINC-615A-3-6-4-7-P092-PROSE-SENTENCE-031-1532165AA3AE`<br>`ARINC-615A-3 6.4.7 p.80` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ZERO-TERMINATE-DOWNLOAD-STATUS-DESCRIPTION-0X00` / `OBJ-0X00` / `ZERO-TERMINATE-DOWNLOAD-STATUS-DESCRIPTION-0X00-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall zero-terminate Download Status Description with 0x00.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须用 0x00 作为 Download Status Description 的零终止。 | — | — |
| `CRS-M1-00448` | `SU-ARINC-615A-3-6-4-7-P093-PROSE-SENTENCE-040-BFA9E163247A`<br>`ARINC-615A-3 6.4.7 p.81` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `SET-EXCEPTION-TIMER-0X0000-EVERY-OTHER-STATUS-CODE` / `EXCEPTION-TIMER, OBJ-0X0000` / `SET-EXCEPTION-TIMER-0X0000-EVERY-OTHER-STATUS-CODE-OBSERVABLE` | `MUST` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall set Exception Timer to 0x0000 for every other status code.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须把其他状态码的 Exception Timer 置为 0x0000。 | — | — |
| `CRS-M1-00449` | `SU-ARINC-615A-3-6-4-7-P093-PROSE-SENTENCE-045-16B3A57C8CEC`<br>`ARINC-615A-3 6.4.7 p.81` | `TARGET-HARDWARE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `PROVIDE-ESTIMATED-TIME-SOON-POSSIBLE-DURING-OPERATION` / `ESTIMATED-TIME` / `PROVIDE-ESTIMATED-TIME-SOON-POSSIBLE-DURING-OPERATION-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the target hardware shall provide Estimated Time as soon as possible during the operation.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，目标硬件必须在操作过程中尽快提供 Estimated Time。 | — | — |
| `CRS-M1-00450` | `SU-ARINC-615A-3-6-4-7-P093-PROSE-SENTENCE-048-581419285745`<br>`ARINC-615A-3 6.4.7 p.81` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `TARGET-DOES-NOT-GIVE-ESTIMATED-TIME-SET-FIELD-0XFFFF` / `ESTIMATED-TIME, OBJ-0XFFFF` / `TARGET-DOES-NOT-GIVE-ESTIMATED-TIME-SET-FIELD-0XFFFF-OBSERVABLE` | `MUST` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall if the target does not give Estimated Time, set the field to 0xFFFF.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，若目标未给出 Estimated Time，协议文件生成方必须把该字段置为 0xFFFF。 | — | — |
| `CRS-M1-00451` | `SU-ARINC-615A-3-6-4-7-P093-PROSE-SENTENCE-058-1532165AA3AE`<br>`ARINC-615A-3 6.4.7 p.81` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ZERO-TERMINATE-LNS-FILE-NAME-0X00` / `OBJ-0X00` / `ZERO-TERMINATE-LNS-FILE-NAME-0X00-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall zero-terminate LNS File Name with 0x00.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须用 0x00 作为 LNS File Name 的零终止。 | — | — |
| `CRS-M1-00452` | `SU-ARINC-615A-3-6-4-7-P094-PROSE-SENTENCE-077-6BCAB56CC15C`<br>`ARINC-615A-3 6.4.7 p.82` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `OTHER-FILE-STATUS-CODES-IGNORE-DESCRIPTION-CONTENT-WHICH-MAY-HOLD` / `FILE-STATUS-DESCRIPTION` / `OTHER-FILE-STATUS-CODES-IGNORE-DESCRIPTION-CONTENT-WHICH-MAY-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer may for other file status codes ignore description content, which may hold leftover data.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方对其他文件状态码可以忽略描述字段内容，其中可能残留数据。 | — | — |
| `CRS-M1-00453` | `SU-ARINC-615A-3-6-4-7-P094-PROSE-SENTENCE-079-53AAFA003A8B`<br>`ARINC-615A-3 6.4.7 p.82` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `USE-ONLY-PRINTABLE-CHARACTERS-FILE-STATUS-DESCRIPTION-NO-CONTROL-CHARACTERS` / `FILE-STATUS-DESCRIPTION` / `USE-ONLY-PRINTABLE-CHARACTERS-FILE-STATUS-DESCRIPTION-NO-CON-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall use only printable characters in File Status Description, with no control characters, max 255.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须使用 only printable characters in File Status Description, with no control characters, max 255。 | — | — |
| `CRS-M1-00454` | `SU-ARINC-615A-3-6-4-7-P094-PROSE-SENTENCE-080-1532165AA3AE`<br>`ARINC-615A-3 6.4.7 p.82` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ZERO-TERMINATE-FILE-STATUS-DESCRIPTION-0X00` / `OBJ-0X00` / `ZERO-TERMINATE-FILE-STATUS-DESCRIPTION-0X00-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall zero-terminate File Status Description with 0x00.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须用 0x00 作为 File Status Description 的零终止。 | — | — |
| `CRS-M1-00455` | `SU-ARINC-615A-3-6-4-8-P095-PROSE-SENTENCE-015-1532165AA3AE`<br>`ARINC-615A-3 6.4.8 p.83` | `PROTOCOL-FILE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ZERO-TERMINATE-LNL-FILE-NAME-0X00` / `OBJ-0X00` / `ZERO-TERMINATE-LNL-FILE-NAME-0X00-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall zero-terminate LNL File Name with 0x00.<br>在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须用 0x00 作为 LNL File Name 的零终止。 | — | — |
| `CRS-M1-00456` | `SU-ARINC-615A-3-6-4-8-P096-PROSE-SENTENCE-020-53AAFA003A8B`<br>`ARINC-615A-3 6.4.8 p.84` | `PROTOCOL-FILE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `USE-ONLY-PRINTABLE-CHARACTERS-LNL-FILE-DESCRIPTION-NO-CONTROL-CHARACTERS` / `FILE-DESCRIPTION` / `USE-ONLY-PRINTABLE-CHARACTERS-LNL-FILE-DESCRIPTION-NO-CONTRO-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall use only printable characters in LNL File Description, with no control characters, max 255.<br>在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须使用 only printable characters in LNL File Description, with no control characters, max 255。 | — | — |
| `CRS-M1-00457` | `SU-ARINC-615A-3-6-4-8-P096-PROSE-SENTENCE-021-1532165AA3AE`<br>`ARINC-615A-3 6.4.8 p.84` | `PROTOCOL-FILE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ZERO-TERMINATE-LNL-FILE-DESCRIPTION-0X00` / `OBJ-0X00` / `ZERO-TERMINATE-LNL-FILE-DESCRIPTION-0X00-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall zero-terminate LNL File Description with 0x00.<br>在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须用 0x00 作为 LNL File Description 的零终止。 | — | — |
| `CRS-M1-00458` | `SU-ARINC-615A-3-6-4-9-P096-PROSE-SENTENCE-016-1532165AA3AE`<br>`ARINC-615A-3 6.4.9 p.84` | `PROTOCOL-FILE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ZERO-TERMINATE-LNA-FILE-NAME-0X00` / `OBJ-0X00` / `ZERO-TERMINATE-LNA-FILE-NAME-0X00-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall zero-terminate LNA File Name with 0x00.<br>在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须用 0x00 作为 LNA File Name 的零终止。 | — | — |
| `CRS-M1-00459` | `SU-ARINC-615A-3-TABLE-6_4_6-1-R002`<br>`ARINC-615A-3 6.4.6 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-LENGTH, LNR` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-FILE-LENGTH of LNR at the tabulated width and table ordinal 1.<br>在实现并使用媒体定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 1 个字段位置编码 LNR 的 FIELD-FILE-LENGTH。 | — | — |
| `CRS-M1-00460` | `SU-ARINC-615A-3-TABLE-6_4_6-1-R003`<br>`ARINC-615A-3 6.4.6 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-PROTOCOL-VERSION, LNR` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When the corresponding DOWNLOAD mode is used, the protocol-file producer shall encode FIELD-PROTOCOL-VERSION of LNR as two ASCII characters at table ordinal 2.<br>在使用对应 DOWNLOAD 模式时，协议文件生成方必须把 LNR 的 FIELD-PROTOCOL-VERSION 按表序号 2 编码为两个 ASCII 字符。 | — | — |
| `CRS-M1-00461` | `SU-ARINC-615A-3-TABLE-6_4_6-1-R004`<br>`ARINC-615A-3 6.4.6 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-NUMBER-OF-FILES, LNR` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-NUMBER-OF-FILES of LNR at the tabulated width and table ordinal 3.<br>在实现并使用媒体定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 3 个字段位置编码 LNR 的 FIELD-NUMBER-OF-FILES。 | — | — |
| `CRS-M1-00462` | `SU-ARINC-615A-3-TABLE-6_4_6-1-R005`<br>`ARINC-615A-3 6.4.6 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-NAME-LENGTH, LNR` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-FILE-NAME-LENGTH of LNR at the tabulated width and table ordinal 4.<br>在实现并使用媒体定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 4 个字段位置编码 LNR 的 FIELD-FILE-NAME-LENGTH。 | — | — |
| `CRS-M1-00463` | `SU-ARINC-615A-3-TABLE-6_4_6-1-R006`<br>`ARINC-615A-3 6.4.6 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-NAME, LNR` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-FILE-NAME of LNR at the tabulated width and table ordinal 5.<br>在实现并使用媒体定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 5 个字段位置编码 LNR 的 FIELD-FILE-NAME。 | — | — |
| `CRS-M1-00464` | `SU-ARINC-615A-3-TABLE-6_4_6-1-R007`<br>`ARINC-615A-3 6.4.6 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-USER-DEFINED-DATA-LENGTH, LNR` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-USER-DEFINED-DATA-LENGTH of LNR at the tabulated width and table ordinal 6.<br>在实现并使用媒体定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 6 个字段位置编码 LNR 的 FIELD-USER-DEFINED-DATA-LENGTH。 | — | — |
| `CRS-M1-00465` | `SU-ARINC-615A-3-TABLE-6_4_6-1-R008`<br>`ARINC-615A-3 6.4.6 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-USER-DEFINED-DATA, LNR` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-USER-DEFINED-DATA of LNR at the tabulated width and table ordinal 7.<br>在实现并使用媒体定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 7 个字段位置编码 LNR 的 FIELD-USER-DEFINED-DATA。 | — | — |
| `CRS-M1-00466` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R002`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-LENGTH, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-FILE-LENGTH of LNS at the tabulated width and table ordinal 1.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 1 个字段位置编码 LNS 的 FIELD-FILE-LENGTH。 | — | — |
| `CRS-M1-00467` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R003`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-PROTOCOL-VERSION, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When the corresponding DOWNLOAD mode is used, the protocol-file producer shall encode FIELD-PROTOCOL-VERSION of LNS as two ASCII characters at table ordinal 2.<br>在使用对应 DOWNLOAD 模式时，协议文件生成方必须把 LNS 的 FIELD-PROTOCOL-VERSION 按表序号 2 编码为两个 ASCII 字符。 | — | — |
| `CRS-M1-00468` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R004`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-DOWNLOAD-OPERATION-STATUS-CODE, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-DOWNLOAD-OPERATION-STATUS-CODE of LNS at the tabulated width and table ordinal 3.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 3 个字段位置编码 LNS 的 FIELD-DOWNLOAD-OPERATION-STATUS-CODE。 | — | — |
| `CRS-M1-00469` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R005`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-DOWNLOAD-STATUS-DESCRIPTION-LENGTH, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-DOWNLOAD-STATUS-DESCRIPTION-LENGTH of LNS at the tabulated width and table ordinal 4.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 4 个字段位置编码 LNS 的 FIELD-DOWNLOAD-STATUS-DESCRIPTION-LENGTH。 | — | — |
| `CRS-M1-00470` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R006`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-DOWNLOAD-STATUS-DESCRIPTION, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-DOWNLOAD-STATUS-DESCRIPTION of LNS at the tabulated width and table ordinal 5.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 5 个字段位置编码 LNS 的 FIELD-DOWNLOAD-STATUS-DESCRIPTION。 | — | — |
| `CRS-M1-00471` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R007`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-COUNTER, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-COUNTER of LNS at the tabulated width and table ordinal 6.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 6 个字段位置编码 LNS 的 FIELD-COUNTER。 | — | — |
| `CRS-M1-00472` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R008`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-EXCEPTION-TIMER, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode LNS Exception Timer as a physically present 16-bit field at table ordinal 7. The field is used on status 0x0002 or 0x0004 as remaining seconds in 0..65535; other statuses keep the field and store 0x0000.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须把 LNS Exception Timer 编为表序 7 的固定 16 位字段。该字段在状态 0x0002 或 0x0004 用作 0..65535 的剩余秒数；其他状态仍保留该字段并置 0x0000。 | — | — |
| `CRS-M1-00473` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R009`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-ESTIMATED-TIME, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is used, the protocol-file producer shall encode LNS Estimated Time as a physically present 16-bit field at table ordinal 8. Status 0x0002 or 0x0004 carry remaining seconds in 0..32767, with 0xFFFF meaning not given; other statuses keep the field and store 0x0000. Inactive 0x0000 is unused filler, not a not-given sentinel.<br>在使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须把 LNS Estimated Time 编为表序 8 的固定 16 位字段。状态 0x0002 或 0x0004 携带 0..32767 的剩余秒数，0xFFFF 表示未给出；其他状态仍保留该字段并置 0x0000。非活动的 0x0000 是未使用填充，不是未给出哨兵。 | — | — |
| `CRS-M1-00474` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R010`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-DOWNLOAD-LIST-RATIO, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is used, the protocol-file producer shall encode LNS Download List Ratio as three right-adjusted ASCII characters with leading blanks, not as an integer.<br>在使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须把 LNS Download List Ratio 编为三个右对齐、前导空白的 ASCII 字符，而不是整数。 | — | — |
| `CRS-M1-00475` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R011`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-NUMBER-OF-FILES, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-NUMBER-OF-FILES of LNS at the tabulated width and table ordinal 10.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 10 个字段位置编码 LNS 的 FIELD-NUMBER-OF-FILES。 | — | — |
| `CRS-M1-00476` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R012`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-NAME-LENGTH, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-FILE-NAME-LENGTH of LNS at the tabulated width and table ordinal 11.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 11 个字段位置编码 LNS 的 FIELD-FILE-NAME-LENGTH。 | — | — |
| `CRS-M1-00477` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R013`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-NAME, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-FILE-NAME of LNS at the tabulated width and table ordinal 12.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 12 个字段位置编码 LNS 的 FIELD-FILE-NAME。 | — | — |
| `CRS-M1-00478` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R014`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-STATUS, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-FILE-STATUS of LNS at the tabulated width and table ordinal 13.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 13 个字段位置编码 LNS 的 FIELD-FILE-STATUS。 | — | — |
| `CRS-M1-00479` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R015`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-STATUS-DESCRIPTION-LENGTH, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-FILE-STATUS-DESCRIPTION-LENGTH of LNS at the tabulated width and table ordinal 14.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 14 个字段位置编码 LNS 的 FIELD-FILE-STATUS-DESCRIPTION-LENGTH。 | — | — |
| `CRS-M1-00480` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R016`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-STATUS-DESCRIPTION, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined or Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-FILE-STATUS-DESCRIPTION of LNS at the tabulated width and table ordinal 15.<br>在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 15 个字段位置编码 LNS 的 FIELD-FILE-STATUS-DESCRIPTION。 | — | — |
| `CRS-M1-00481` | `SU-ARINC-615A-3-TABLE-6_4_8-1-R002`<br>`ARINC-615A-3 6.4.8 p.83` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-LENGTH, LNL` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-FILE-LENGTH of LNL at the tabulated width and table ordinal 1.<br>在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 1 个字段位置编码 LNL 的 FIELD-FILE-LENGTH。 | — | — |
| `CRS-M1-00482` | `SU-ARINC-615A-3-TABLE-6_4_8-1-R003`<br>`ARINC-615A-3 6.4.8 p.83` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-PROTOCOL-VERSION, LNL` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When the corresponding DOWNLOAD mode is used, the protocol-file producer shall encode FIELD-PROTOCOL-VERSION of LNL as two ASCII characters at table ordinal 2.<br>在使用对应 DOWNLOAD 模式时，协议文件生成方必须把 LNL 的 FIELD-PROTOCOL-VERSION 按表序号 2 编码为两个 ASCII 字符。 | — | — |
| `CRS-M1-00483` | `SU-ARINC-615A-3-TABLE-6_4_8-1-R004`<br>`ARINC-615A-3 6.4.8 p.83` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-NUMBER-OF-FILES, LNL` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-NUMBER-OF-FILES of LNL at the tabulated width and table ordinal 3.<br>在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 3 个字段位置编码 LNL 的 FIELD-NUMBER-OF-FILES。 | — | — |
| `CRS-M1-00484` | `SU-ARINC-615A-3-TABLE-6_4_8-1-R005`<br>`ARINC-615A-3 6.4.8 p.83` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-NAME-LENGTH, LNL` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-FILE-NAME-LENGTH of LNL at the tabulated width and table ordinal 4.<br>在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 4 个字段位置编码 LNL 的 FIELD-FILE-NAME-LENGTH。 | — | — |
| `CRS-M1-00485` | `SU-ARINC-615A-3-TABLE-6_4_8-1-R006`<br>`ARINC-615A-3 6.4.8 p.83` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-NAME, LNL` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-FILE-NAME of LNL at the tabulated width and table ordinal 5.<br>在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 5 个字段位置编码 LNL 的 FIELD-FILE-NAME。 | — | — |
| `CRS-M1-00486` | `SU-ARINC-615A-3-TABLE-6_4_8-1-R007`<br>`ARINC-615A-3 6.4.8 p.83` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-DESCRIPTION-LENGTH, LNL` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-FILE-DESCRIPTION-LENGTH of LNL at the tabulated width and table ordinal 6.<br>在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 6 个字段位置编码 LNL 的 FIELD-FILE-DESCRIPTION-LENGTH。 | — | — |
| `CRS-M1-00487` | `SU-ARINC-615A-3-TABLE-6_4_8-1-R008`<br>`ARINC-615A-3 6.4.8 p.83` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-DESCRIPTION, LNL` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-FILE-DESCRIPTION of LNL at the tabulated width and table ordinal 7.<br>在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 7 个字段位置编码 LNL 的 FIELD-FILE-DESCRIPTION。 | — | — |
| `CRS-M1-00488` | `SU-ARINC-615A-3-TABLE-6_4_9-1-R002`<br>`ARINC-615A-3 6.4.9 p.84` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-LENGTH, LNA` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-FILE-LENGTH of LNA at the tabulated width and table ordinal 1.<br>在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 1 个字段位置编码 LNA 的 FIELD-FILE-LENGTH。 | — | — |
| `CRS-M1-00489` | `SU-ARINC-615A-3-TABLE-6_4_9-1-R003`<br>`ARINC-615A-3 6.4.9 p.84` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-PROTOCOL-VERSION, LNA` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When the corresponding DOWNLOAD mode is used, the protocol-file producer shall encode FIELD-PROTOCOL-VERSION of LNA as two ASCII characters at table ordinal 2.<br>在使用对应 DOWNLOAD 模式时，协议文件生成方必须把 LNA 的 FIELD-PROTOCOL-VERSION 按表序号 2 编码为两个 ASCII 字符。 | — | — |
| `CRS-M1-00490` | `SU-ARINC-615A-3-TABLE-6_4_9-1-R004`<br>`ARINC-615A-3 6.4.9 p.84` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-NUMBER-OF-FILES, LNA` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-NUMBER-OF-FILES of LNA at the tabulated width and table ordinal 3.<br>在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 3 个字段位置编码 LNA 的 FIELD-NUMBER-OF-FILES。 | — | — |
| `CRS-M1-00491` | `SU-ARINC-615A-3-TABLE-6_4_9-1-R005`<br>`ARINC-615A-3 6.4.9 p.84` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-NAME-LENGTH, LNA` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-FILE-NAME-LENGTH of LNA at the tabulated width and table ordinal 4.<br>在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 4 个字段位置编码 LNA 的 FIELD-FILE-NAME-LENGTH。 | — | — |
| `CRS-M1-00492` | `SU-ARINC-615A-3-TABLE-6_4_9-1-R006`<br>`ARINC-615A-3 6.4.9 p.84` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-NAME, LNA` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the protocol-file producer shall encode FIELD-FILE-NAME of LNA at the tabulated width and table ordinal 5.<br>在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 5 个字段位置编码 LNA 的 FIELD-FILE-NAME。 | — | — |
| `CRS-M1-00493` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E001-93E2E1579D6F`<br>`ARINC-615A-3 6.3.3 p.57` | `DATA-LOADER-APPLICATION` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ISSUE-DOWNLOADING-MEDIA-INITIALIZATION-START-MEDIA-MODE-CHART` / `DOWNLOADING-MEDIA-INITIALIZATION` / `ISSUE-DOWNLOADING-MEDIA-INITIALIZATION-START-MEDIA-MODE-CHAR-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the data-loader application shall issue Downloading_Media_Initialization to start the media-mode chart.<br>在实现并使用媒体定义 DOWNLOAD 时，数据加载器应用层必须发出 Downloading_Media_Initialization to start the media-mode chart。 | — | — |
| `CRS-M1-00494` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E002-56059C7FBCE3`<br>`ARINC-615A-3 6.3.3 p.57` | `DATA-LOADER-PROTOCOL` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `TFTP-READ-LND-TARGET` / `LND` / `TFTP-READ-LND-TARGET-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the data-loader protocol layer shall TFTP-read LND from the target.<br>在实现并使用媒体定义 DOWNLOAD 时，数据加载器协议层必须用 TFTP 从目标读取 LND。 | — | — |
| `CRS-M1-00495` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E003-7572FB4A7D49`<br>`ARINC-615A-3 6.3.3 p.57` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `TRANSFER-LND-ANSWER-WAIT-RETRY` / `LND, WAIT` / `TRANSFER-LND-ANSWER-WAIT-RETRY-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the target hardware shall transfer LND or answer WAIT for retry.<br>在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须传送 LND or answer WAIT for retry。 | — | — |
| `CRS-M1-00496` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E004-F7FB3AED0BF8`<br>`ARINC-615A-3 6.3.3 p.57` | `DATA-LOADER-PROTOCOL` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `EMIT-DOWNLOADING-INITIALIZATION-RESPONSE-LND-OUTCOME` / `DOWNLOADING-INITIALIZATION-RESPONSE` / `EMIT-DOWNLOADING-INITIALIZATION-RESPONSE-LND-OUTCOME-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the data-loader protocol layer shall emit Downloading_Initialization_Response from the LND outcome.<br>在实现并使用媒体定义 DOWNLOAD 时，数据加载器协议层必须根据 LND 结果发出 Downloading_Initialization_Response。 | — | — |
| `CRS-M1-00497` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E005-DDC22BBE77AD`<br>`ARINC-615A-3 6.3.3 p.57` | `DATA-LOADER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `END-MEDIA-DEFINED-DOWNLOAD-DENY` / `DENY` / `END-MEDIA-DEFINED-DOWNLOAD-DENY-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the data loader shall end Media Defined DOWNLOAD on deny.<br>在实现并使用媒体定义 DOWNLOAD 时，数据加载器必须结束 媒体定义 DOWNLOAD on deny。 | — | — |
| `CRS-M1-00498` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E006-FFDAE5BD327A`<br>`ARINC-615A-3 6.3.3 p.57` | `DATA-LOADER-PROTOCOL` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `AFTER-ACCEPT-WRITE-LNR-TO-TARGET-BY-TFTP` / `LNR, TARGET-HARDWARE, TFTP` / `ACCEPT-TFTP-WRITE-LNR-TARGET-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the data-loader protocol layer shall, after accept, write LNR to the target hardware using TFTP.<br>在实现并使用媒体定义 DOWNLOAD 时，数据加载器协议层必须在接受之后用 TFTP 把 LNR 写到目标硬件。 | — | — |
| `CRS-M1-00499` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E007-465C743F7A74`<br>`ARINC-615A-3 6.3.3 p.57` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `RECEIVE-ANALYZE-LNR` / `LNR` / `RECEIVE-ANALYZE-LNR-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the target hardware shall receive and analyze LNR.<br>在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须接收 and analyze LNR。 | — | — |
| `CRS-M1-00500` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E008-4F5A7B67B142`<br>`ARINC-615A-3 6.3.3 p.57` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `TFTP-WRITE-LNS-INCLUDING-ACCEPTED-NOT-STARTED-0X0001` / `LNS, OBJ-0X0001` / `TFTP-WRITE-LNS-INCLUDING-ACCEPTED-NOT-STARTED-0X0001-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the target hardware shall TFTP-write LNS, including accepted-not-started 0x0001.<br>在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须用 TFTP 写 LNS，并包含已接受但未开始的 0x0001。 | — | — |
| `CRS-M1-00501` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E009-0C4A2E52223E`<br>`ARINC-615A-3 6.3.3 p.57` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `TFTP-SEND-EACH-LNR-LISTED-DATA-FILE` / `DATA-FILES` / `TFTP-SEND-EACH-LNR-LISTED-DATA-FILE-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the target hardware shall TFTP-send each LNR-listed data file.<br>在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须TFTP-发送 each LNR-listed data file。 | — | — |
| `CRS-M1-00502` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E010-C4CF6F527181`<br>`ARINC-615A-3 6.3.3 p.57` | `DATA-LOADER-PROTOCOL` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ISSUE-DOWNLOADING-FILE-RECEIPT-EACH-RECEIVED-FILE` / `DOWNLOADING-FILE-RECEIPT` / `ISSUE-DOWNLOADING-FILE-RECEIPT-EACH-RECEIVED-FILE-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the data-loader protocol layer shall issue Downloading_File_Receipt for each received file.<br>在实现并使用媒体定义 DOWNLOAD 时，数据加载器协议层必须发出 Downloading_File_Receipt for each 接收d file。 | — | — |
| `CRS-M1-00503` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E011-86839F050632`<br>`ARINC-615A-3 6.3.3 p.57` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `REPEAT-REMAINING-FILES-LNS-PROGRESS` / `LNS` / `REPEAT-REMAINING-FILES-LNS-PROGRESS-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the target hardware shall repeat remaining files with LNS progress.<br>在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须重复 remaining files with LNS progress。 | — | — |
| `CRS-M1-00504` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E012-9EC73921C558`<br>`ARINC-615A-3 6.3.3 p.57` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `END-AFTER-FINAL-LNS-COMPLETE-FATAL-HONOUR-ATTACHMENT-4-CHRONO` / `LNS, ATTACHMENT-4` / `END-AFTER-FINAL-LNS-COMPLETE-FATAL-HONOUR-ATTACHMENT-4-CHRON-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Media Defined DOWNLOAD is implemented and used, the target hardware shall end after final LNS complete or fatal; honour Attachment 4 chrono timeouts.<br>在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须结束 after final LNS 完成 or fatal; honour 附件 4 chrono timeouts。 | — | — |
| `CRS-M1-00505` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E001-D20446C4AA87`<br>`ARINC-615A-3 6.3.4 p.60` | `DATA-LOADER-APPLICATION` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ISSUE-DOWNLOADING-OPERATOR-INITIALIZATION-START-OPERATOR-MODE-CHART` / `DOWNLOADING-OPERATOR-INITIALIZATION` / `ISSUE-DOWNLOADING-OPERATOR-INITIALIZATION-START-OPERATOR-MOD-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the data-loader application shall issue Downloading_Operator_Initialization to start the operator-mode chart.<br>在实现并使用操作员定义 DOWNLOAD 时，数据加载器应用层必须发出 Downloading_Operator_Initialization to start the operator-mode chart。 | — | — |
| `CRS-M1-00506` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E002-FA62BFEC08D9`<br>`ARINC-615A-3 6.3.4 p.60` | `DATA-LOADER-PROTOCOL` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `TFTP-READ-LNO-TARGET` / `LNO` / `TFTP-READ-LNO-TARGET-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the data-loader protocol layer shall TFTP-read LNO from the target.<br>在实现并使用操作员定义 DOWNLOAD 时，数据加载器协议层必须用 TFTP 从目标读取 LNO。 | — | — |
| `CRS-M1-00507` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E003-4E7C61B06179`<br>`ARINC-615A-3 6.3.4 p.60` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `TRANSFER-LNO-ANSWER-WAIT-RETRY` / `LNO, WAIT` / `TRANSFER-LNO-ANSWER-WAIT-RETRY-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the target hardware shall transfer LNO or answer WAIT for retry.<br>在实现并使用操作员定义 DOWNLOAD 时，目标硬件必须传送 LNO or answer WAIT for retry。 | — | — |
| `CRS-M1-00508` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E004-4DD6ECF8E15C`<br>`ARINC-615A-3 6.3.4 p.60` | `DATA-LOADER-PROTOCOL` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `EMIT-DOWNLOADING-INITIALIZATION-RESPONSE-LNO-OUTCOME` / `DOWNLOADING-INITIALIZATION-RESPONSE` / `EMIT-DOWNLOADING-INITIALIZATION-RESPONSE-LNO-OUTCOME-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the data-loader protocol layer shall emit Downloading_Initialization_Response from the LNO outcome.<br>在实现并使用操作员定义 DOWNLOAD 时，数据加载器协议层必须根据 LNO 结果发出 Downloading_Initialization_Response。 | — | — |
| `CRS-M1-00509` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E005-22221ABB2116`<br>`ARINC-615A-3 6.3.4 p.60` | `DATA-LOADER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `END-OPERATOR-DEFINED-DOWNLOAD-DENY` / `DENY` / `END-OPERATOR-DEFINED-DOWNLOAD-DENY-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the data loader shall end Operator Defined DOWNLOAD on deny.<br>在实现并使用操作员定义 DOWNLOAD 时，数据加载器必须结束 操作员定义 DOWNLOAD on deny。 | — | — |
| `CRS-M1-00510` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E006-145A7178D4F7`<br>`ARINC-615A-3 6.3.4 p.60` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `AFTER-ACCEPT-WRITE-LNL-TO-LOADER-BY-TFTP` / `LNL, DATA-LOADER, TFTP` / `ACCEPT-TFTP-WRITE-LNL-LOADER-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the target hardware shall, after accept, write LNL to the data loader using TFTP.<br>在实现并使用操作员定义 DOWNLOAD 时，目标硬件必须在接受之后用 TFTP 把 LNL 写到加载器。 | — | — |
| `CRS-M1-00511` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E007-BB90540A19D7`<br>`ARINC-615A-3 6.3.4 p.60` | `DATA-LOADER-PROTOCOL` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ISSUE-DOWNLOADING-FILE-LIST-RECEIPT` / `DOWNLOADING-FILE-LIST-RECEIPT` / `ISSUE-DOWNLOADING-FILE-LIST-RECEIPT-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the data-loader protocol layer shall issue Downloading_File_List_Receipt.<br>在实现并使用操作员定义 DOWNLOAD 时，数据加载器协议层必须发出 Downloading_File_List_Receipt。 | — | — |
| `CRS-M1-00512` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E008-1FFC2020C9F9`<br>`ARINC-615A-3 6.3.4 p.60` | `OPERATOR` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `SELECT-FILES-LOADER-TFTP-WRITES-LNA-FILE-SELECTION` / `LNA, FILE-SELECTION` / `SELECT-FILES-LOADER-TFTP-WRITES-LNA-FILE-SELECTION-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the operator shall select files; loader TFTP-writes LNA as File_Selection.<br>在实现并使用操作员定义 DOWNLOAD 时，操作员必须选择 files; loader TFTP-writes LNA as File_Selection。 | — | — |
| `CRS-M1-00513` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E009-0C4A2E52223E`<br>`ARINC-615A-3 6.3.4 p.60` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `TFTP-SEND-EACH-LNA-LISTED-DATA-FILE` / `DATA-FILES` / `TFTP-SEND-EACH-LNA-LISTED-DATA-FILE-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the target hardware shall TFTP-send each LNA-listed data file.<br>在实现并使用操作员定义 DOWNLOAD 时，目标硬件必须TFTP-发送 each LNA-listed data file。 | — | — |
| `CRS-M1-00514` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E010-C4CF6F527181`<br>`ARINC-615A-3 6.3.4 p.60` | `DATA-LOADER-PROTOCOL` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ISSUE-DOWNLOADING-FILE-RECEIPT-EACH-RECEIVED-FILE--02783` / `DOWNLOADING-FILE-RECEIPT` / `ISSUE-DOWNLOADING-FILE-RECEIPT-EACH-RECEIVED-FILE-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the data-loader protocol layer shall issue Downloading_File_Receipt for each received file.<br>在实现并使用操作员定义 DOWNLOAD 时，数据加载器协议层必须发出 Downloading_File_Receipt for each 接收d file。 | — | — |
| `CRS-M1-00515` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E011-86839F050632`<br>`ARINC-615A-3 6.3.4 p.60` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `REPEAT-REMAINING-FILES-LNS-PROGRESS--02784` / `LNS` / `REPEAT-REMAINING-FILES-LNS-PROGRESS-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the target hardware shall repeat remaining files with LNS progress.<br>在实现并使用操作员定义 DOWNLOAD 时，目标硬件必须重复 remaining files with LNS progress。 | — | — |
| `CRS-M1-00516` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E012-9EC73921C558`<br>`ARINC-615A-3 6.3.4 p.60` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `END-AFTER-FINAL-LNS-COMPLETE-FATAL-HONOUR-ATTACHMENT-4-CHRONO--02785` / `LNS, ATTACHMENT-4` / `END-AFTER-FINAL-LNS-COMPLETE-FATAL-HONOUR-ATTACHMENT-4-CHRON-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When Operator Defined DOWNLOAD is implemented and used, the target hardware shall end after final LNS complete or fatal; honour Attachment 4 chrono timeouts.<br>在实现并使用操作员定义 DOWNLOAD 时，目标硬件必须结束 after final LNS 完成 or fatal; honour 附件 4 chrono timeouts。 | — | — |
| `CRS-M1-00517` | `SU-ARINC-615A-3-APPENDIX-E-P134-PROSE-SENTENCE-008-123ADFD1F0A0`<br>`ARINC-615A-3 APPENDIX-E p.122` | `DATA-LOADER` / `WHEN-615A-IS-CARRIED-OVER-AFDX` / `USE-FIND-NETWORK-CONFIGURATION-FILE-IDENTIFY-TARGETS-AFDX-NETWORK` / `FIND, NETWORK-CONFIGURATION-FILE` / `USE-FIND-NETWORK-CONFIGURATION-FILE-IDENTIFY-TARGETS-AFDX-NE-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | When the configured deployment carries 615A over AFDX rather than ordinary Ethernet, the data loader may use FIND or a network configuration file to identify targets on the AFDX network. This does not activate the current Compliant Ethernet instance.<br>在配置的部署把 615A 承载于 AFDX 而非普通以太网时，数据加载器可以使用 FIND or a network configuration file to identify targets on the AFDX network。这不激活当前 Compliant 以太网实例。 | — | — |
| `CRS-M1-00518` | `SU-ARINC-615A-3-APPENDIX-E-P134-PROSE-SENTENCE-011-E6FB447853B2`<br>`ARINC-615A-3 APPENDIX-E p.122` | `DATA-LOADER` / `WHEN-615A-IS-CARRIED-OVER-AFDX` / `USE-TFTP-PROTOCOL-DESCRIBED-615A-3-615A-OPERATIONS-OVER-AFDX` / `TFTP` / `USE-TFTP-PROTOCOL-DESCRIBED-615A-3-615A-OPERATIONS-OVER-AFDX-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When the configured deployment carries 615A over AFDX rather than ordinary Ethernet, the data loader shall use the TFTP protocol described in 615A-3 for 615A operations over AFDX. This does not activate the current Compliant Ethernet instance.<br>在配置的部署把 615A 承载于 AFDX 而非普通以太网时，数据加载器必须使用 the TFTP protocol described in 615A-3 for 615A operations over AFDX。这不激活当前 Compliant 以太网实例。 | — | — |
| `CRS-M1-00519` | `SU-ARINC-615A-3-APPENDIX-E-P134-PROSE-SENTENCE-013-B5690D59EDBF`<br>`ARINC-615A-3 APPENDIX-E p.122` | `SYSTEM-INTEGRATOR` / `WHEN-615A-IS-CARRIED-OVER-AFDX` / `APPLY-664P4-ADDRESS-RULES-OR-INTEGRATOR-IDENTIFIED-REQUIREMENTS` / `ARINC-664-4-ADDRESS-RULES, INTEGRATOR-IDENTIFIED-ADDRESS-REQUIREMENTS` / `AFDX-ADDRESS-RULE-ALTERNATIVE-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When the configured deployment carries 615A over AFDX rather than ordinary Ethernet, the system integrator shall apply aviation data-network address rules from 664 Part 4, or identify integrator-specified address requirements. The alternative remains open; this does not select Part 4 automatically and does not activate the current Compliant Ethernet instance.<br>在配置的部署把 615A 承载于 AFDX 而非普通以太网时，系统集成商必须适用 664 Part 4 的航空数据网络地址规则，或指出集成商识别的地址要求。这两条路径保持可选择，不自动选定 Part 4，也不激活当前 Compliant 以太网实例。 | — | — |
| `CRS-M1-00520` | `SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-002-F178271163DF`<br>`ARINC-615A-3 3-2 p.96` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `KEEP-THREE-SECOND-FIND-ANSWER-WINDOW` / `FIND-ANSWER-WINDOW-3-S` / `FIND-ANSWER-WINDOW-LIFETIME-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | When FIND is implemented, the data loader shall keep a three-second FIND-answer registration window after sending a FIND request. That three-second value is the window lifetime, not a host-answer deadline and not a permission to close registration early.<br>在实现 FIND 时，数据加载器必须在发出 FIND 请求后保持三秒 FIND 应答登记窗口。该三秒是窗口寿命，不是主机应答期限，也不是可以提前关闭登记的许可。 | `FIXED-SOURCE-CONSTANT` / `FIND-ANSWER-WINDOW-3-S` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `3..3 s` / evidence: SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-002-F178271163DF | — |
| `CRS-M1-00521` | `SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-004-30FC1BCEB891`<br>`ARINC-615A-3 3-2 p.96` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `CLOSE-FIND-ANSWER-REGISTRATION-WHEN-WINDOW-EXPIRES` / `FIND-ANSWER-REGISTRATION, FIND-ANSWER-WINDOW-3-S` / `FIND-REGISTRATION-CLOSE-AT-WINDOW-END-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | When FIND is implemented, the data loader shall close FIND-answer registration three seconds after the FIND request is sent. That close is the same logical instant as the three-second window lifetime elapsing; it is not a second three-second delay after expiry.<br>在实现 FIND 时，数据加载器必须在发出 FIND 请求后三秒关闭 FIND 应答登记。该关闭与三秒窗口寿命到期是同一逻辑时刻，而不是到期后再延迟三秒。 | `FIXED-SOURCE-CONSTANT` / `FIND-ANSWER-WINDOW-3-S` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `3..3 s` / evidence: SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-004-30FC1BCEB891 | — |
| `CRS-M1-00522` | `SU-ARINC-615A-3-5-4-4-3-P052-PROSE-SENTENCE-005-D462FF831585`<br>`ARINC-615A-3 5.4.4.3 p.40` | `DATA-LOADER` / `WHEN-REMOVABLE-MEDIA-IS-LNR-SOURCE-AND-DOWNLOAD-DESTINATION` / `CREATE-DNLD-DATA-DIRECTORY-IN-DOWNLOAD-MEDIA-ROOT` / `DNLD-DATA-DIRECTORY, DOWNLOAD-MEDIA-ROOT` / `DNLD-DATA-DIRECTORY-IN-ROOT-OBSERVABLE` | `FACT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When removable media is the LNR source and the destination of downloaded data, the data loader shall create the DNLD_DATA directory in the root directory of the download media.<br>在可移动媒体既是 LNR 来源又是下载数据目的地时，数据加载器必须在下载媒体的根目录下创建 DNLD_DATA 目录。 | — | — |
| `CRS-M1-00523` | `SU-ARINC-615A-3-5-4-4-3-P052-PROSE-SENTENCE-006-ED9F856333F8`<br>`ARINC-615A-3 5.4.4.3 p.40` | `DATA-LOADER` / `WHEN-REMOVABLE-MEDIA-IS-LNR-SOURCE-AND-DOWNLOAD-DESTINATION` / `INCREMENT-DNLD-DATA-NUMBER-EACH-DOWNLOAD` / `DNLD-DATA-NUMBER, DNLD-DATA-DIRECTORY` / `DNLD-DATA-NUMBER-INCREMENTS-OBSERVABLE` | `FACT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When removable media is the LNR source and the destination of downloaded data, the data loader shall increment <number> on each download so successive DNLD_DATA directory names stay unique.<br>在可移动媒体既是 LNR 来源又是下载数据目的地时，数据加载器必须在每次下载时递增 <number>，以使相继 DNLD_DATA 目录名保持唯一。 | — | — |
| `CRS-M1-00524` | `SU-ARINC-615A-3-3-3-P108-PROSE-SENTENCE-003-9C92144E4252`<br>`ARINC-615A-3 3-3 p.96` | `FIND-PROTOCOL` / `WHEN-FIND-IMPLEMENTED` / `ENCODE-FIND-PACKET-AS-TWO-BYTE-HEADER-PLUS-VARIABLE-DATA` / `FIND-HEADER-2-BYTE, FIND-VARIABLE-LENGTH-DATA, FIND-OPCODE` / `FIND-HEADER-AND-DATA-LAYOUT-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | When FIND is implemented, each FIND packet shall contain a header plus a variable-length data portion. The header is two bytes and carries the opcode.<br>在实现 FIND 时，每个 FIND 分组必须包含报头和可变长度数据区。报头为两字节并承载操作码。 | — | — |
| `CRS-M1-00525` | `SU-ARINC-615A-3-5-4-4-3-P052-PROSE-SENTENCE-007-FF9E1B1FACD7`<br>`ARINC-615A-3 5.4.4.3 p.40` | `DATA-LOADER` / `WHEN-REMOVABLE-MEDIA-IS-LNR-SOURCE-AND-DOWNLOAD-DESTINATION` / `START-DNLD-DATA-NUMBER-AT-ONE` / `DNLD-DATA-NUMBER` / `DNLD-DATA-NUMBER-STARTS-AT-ONE-OBSERVABLE` | `FACT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | When removable media is the LNR source and the destination of downloaded data, the data loader shall start <number> at 1.<br>在可移动媒体既是 LNR 来源又是下载数据目的地时，数据加载器必须把 <number> 从 1 开始。 | — | — |

## Observable timing semantics

| CRS | Family | Trigger → response | Cancellation / superseding trigger | Correlation / pairing |
|---|---|---|---|---|
| `CRS-M1-00032` | `WAIT-MESSAGE-RETRY-NOT-BEFORE-DEADLINE` | `WAIT-MESSAGE-WITH-DELAY-RECEIVED` → `NEW-TFTP-TRANSFER-INITIATED-AFTER-DELAY` | `OPERATION-ABORTED-OR-FATAL` / `NEWER-WAIT-MESSAGE-FOR-SAME-REQUEST-RECEIVED` | `TFTP-PEER-AND-REJECTED-TRANSFER-REQUEST` / `PAIR-WAIT-DELAY-WITH-REPLACEMENT-TFTP-TRANSFER` |
| `CRS-M1-00094` | `DLP-CONSECUTIVE-TFTP-TRANSFER-DEADLINE` | `FINAL-PACKET-OF-INITIATING-TFTP-TRANSFER` → `FIRST-PACKET-OF-NEXT-DLP-TFTP-TRANSFER` | `DLP-OPERATION-ABORTED-OR-FATAL` / `AUTHORIZED-DLP-RETRY-START` | `TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-CONSECUTIVE-TFTP-TRANSFERS-IN-SAME-OPERATION` |
| `CRS-M1-00097` | `DLP-CONSECUTIVE-TFTP-TRANSFER-DEADLINE` | `FINAL-PACKET-OF-INITIATING-TFTP-TRANSFER` → `FIRST-PACKET-OF-NEXT-DLP-TFTP-TRANSFER` | `DLP-OPERATION-ABORTED-OR-FATAL` / `AUTHORIZED-DLP-RETRY-START` | `TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-CONSECUTIVE-TFTP-TRANSFERS-IN-SAME-OPERATION` |
| `CRS-M1-00098` | `DLP-CONSECUTIVE-TFTP-TRANSFER-DEADLINE` | `FINAL-PACKET-OF-INITIATING-TFTP-TRANSFER` → `FIRST-PACKET-OF-NEXT-DLP-TFTP-TRANSFER` | `DLP-OPERATION-ABORTED-OR-FATAL` / `AUTHORIZED-DLP-RETRY-START` | `TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-CONSECUTIVE-TFTP-TRANSFERS-IN-SAME-OPERATION` |
| `CRS-M1-00099` | `STATUS-EXCEPTION-SILENCE-DEADLINE` | `STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` → `FIRST-TARGET-STATUS-OR-RESPONSE-AFTER-SILENCE` | `OPERATION-ABORTED-OR-FATAL` / `NEWER-STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` | `TARGET-OPERATION-AND-STATUS-FILE-INSTANCE` / `PAIR-EXCEPTION-TIMER-WITH-TARGET-SILENCE-INTERVAL` |
| `CRS-M1-00100` | `STATUS-EXCEPTION-SILENCE-DEADLINE` | `STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` → `FIRST-TARGET-STATUS-OR-RESPONSE-AFTER-SILENCE` | `OPERATION-ABORTED-OR-FATAL` / `NEWER-STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` | `TARGET-OPERATION-AND-STATUS-FILE-INSTANCE` / `PAIR-EXCEPTION-TIMER-WITH-TARGET-SILENCE-INTERVAL` |
| `CRS-M1-00101` | `STATUS-BEFORE-EXCEPTION-DELAY-OR-ABORT` | `STATUS-FILE-WITH-EXCEPTION-DELAY-RECEIVED` → `NEW-STATUS-FILE-RECEIVED-OR-OPERATION-ABORTED` | `OPERATION-TERMINATED` / `NEWER-STATUS-FILE-RECEIVED` | `TARGET-AND-ACTIVE-OPERATION` / `PAIR-EXCEPTION-DELAY-WITH-NEXT-STATUS-OR-ABORT` |
| `CRS-M1-00102` | `DLP-CONSECUTIVE-TFTP-TRANSFER-DEADLINE` | `FINAL-PACKET-OF-INITIATING-TFTP-TRANSFER` → `FIRST-PACKET-OF-NEXT-DLP-TFTP-TRANSFER` | `DLP-OPERATION-ABORTED-OR-FATAL` / `AUTHORIZED-DLP-RETRY-START` | `TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-CONSECUTIVE-TFTP-TRANSFERS-IN-SAME-OPERATION` |
| `CRS-M1-00106` | `STATUS-EXCEPTION-SILENCE-DEADLINE` | `STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` → `FIRST-TARGET-STATUS-OR-RESPONSE-AFTER-SILENCE` | `OPERATION-ABORTED-OR-FATAL` / `NEWER-STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` | `TARGET-OPERATION-AND-STATUS-FILE-INSTANCE` / `PAIR-EXCEPTION-TIMER-WITH-TARGET-SILENCE-INTERVAL` |
| `CRS-M1-00107` | `STATUS-EXCEPTION-SILENCE-DEADLINE` | `STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` → `FIRST-TARGET-STATUS-OR-RESPONSE-AFTER-SILENCE` | `OPERATION-ABORTED-OR-FATAL` / `NEWER-STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` | `TARGET-OPERATION-AND-STATUS-FILE-INSTANCE` / `PAIR-EXCEPTION-TIMER-WITH-TARGET-SILENCE-INTERVAL` |
| `CRS-M1-00108` | `STATUS-BEFORE-EXCEPTION-DELAY-OR-ABORT` | `STATUS-FILE-WITH-EXCEPTION-DELAY-RECEIVED` → `NEW-STATUS-FILE-RECEIVED-OR-OPERATION-ABORTED` | `OPERATION-TERMINATED` / `NEWER-STATUS-FILE-RECEIVED` | `TARGET-AND-ACTIVE-OPERATION` / `PAIR-EXCEPTION-DELAY-WITH-NEXT-STATUS-OR-ABORT` |
| `CRS-M1-00168` | `TFTP-PACKET-ANSWER-DEADLINE` | `TFTP-PACKET-SENT` → `CORRESPONDING-TFTP-ANSWER-RECEIVED` | `TFTP-TRANSFER-TERMINATED` / `AUTHORIZED-RETRANSMISSION-OF-SAME-EXCHANGE` | `TFTP-TRANSFER-ID-AND-EXCHANGE-NUMBER` / `PAIR-PACKET-WITH-ITS-ANSWER` |
| `CRS-M1-00176` | `DLP-CONSECUTIVE-TFTP-TRANSFER-DEADLINE` | `FINAL-PACKET-OF-INITIATING-TFTP-TRANSFER` → `FIRST-PACKET-OF-NEXT-DLP-TFTP-TRANSFER` | `DLP-OPERATION-ABORTED-OR-FATAL` / `AUTHORIZED-DLP-RETRY-START` | `TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-CONSECUTIVE-TFTP-TRANSFERS-IN-SAME-OPERATION` |
| `CRS-M1-00177` | `TFTP-PACKET-ANSWER-DEADLINE` | `TFTP-PACKET-SENT` → `CORRESPONDING-TFTP-ANSWER-RECEIVED` | `TFTP-TRANSFER-TERMINATED` / `AUTHORIZED-RETRANSMISSION-OF-SAME-EXCHANGE` | `TFTP-TRANSFER-ID-AND-EXCHANGE-NUMBER` / `PAIR-PACKET-WITH-ITS-ANSWER` |
| `CRS-M1-00178` | `TFTP-PACKET-TRANSMISSION-DURATION-BOUND` | `TFTP-PACKET-EMISSION` → `SAME-TFTP-PACKET-RECEPTION` | `PACKET-TRANSFER-CANCELLED` / `NONE` | `TFTP-PACKET-IDENTITY` / `PAIR-EMISSION-WITH-RECEPTION-OF-SAME-PACKET` |
| `CRS-M1-00179` | `TFTP-SUBSCRIBER-PROCESSING-DURATION-BOUND` | `TFTP-PACKET-RECEPTION` → `ASSOCIATED-TFTP-PACKET-EMISSION` | `TFTP-EXCHANGE-TERMINATED` / `NONE` | `TFTP-EXCHANGE-AND-SUBSCRIBER` / `PAIR-RECEIVED-PACKET-WITH-ASSOCIATED-EMITTED-PACKET` |
| `CRS-M1-00184` | `DLP-CONSECUTIVE-TFTP-TRANSFER-DEADLINE` | `FINAL-PACKET-OF-INITIATING-TFTP-TRANSFER` → `FIRST-PACKET-OF-NEXT-DLP-TFTP-TRANSFER` | `DLP-OPERATION-ABORTED-OR-FATAL` / `AUTHORIZED-DLP-RETRY-START` | `TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-CONSECUTIVE-TFTP-TRANSFERS-IN-SAME-OPERATION` |
| `CRS-M1-00185` | `DLP-CONSECUTIVE-TFTP-TRANSFER-DEADLINE` | `FINAL-PACKET-OF-INITIATING-TFTP-TRANSFER` → `FIRST-PACKET-OF-NEXT-DLP-TFTP-TRANSFER` | `DLP-OPERATION-ABORTED-OR-FATAL` / `AUTHORIZED-DLP-RETRY-START` | `TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-CONSECUTIVE-TFTP-TRANSFERS-IN-SAME-OPERATION` |
| `CRS-M1-00186` | `LCS-PRODUCTION-PROHIBITION-WINDOW` | `LCI-LCL-SEQUENCE-INITIATED-BEFORE-DLP-TO-EXPIRY` → `LCS-MUST-NOT-BE-PRODUCED` | `DLP-TO-EXPIRES-OR-SEQUENCE-TERMINATES` / `NEW-LCI-LCL-SEQUENCE` | `TARGET-AND-LCI-LCL-SEQUENCE` / `PAIR-TIMELY-LCI-LCL-SEQUENCE-WITH-LCS-ABSENCE` |
| `CRS-M1-00187` | `DLP-CONSECUTIVE-TFTP-TRANSFER-DEADLINE` | `FINAL-PACKET-OF-INITIATING-TFTP-TRANSFER` → `FIRST-PACKET-OF-NEXT-DLP-TFTP-TRANSFER` | `DLP-OPERATION-ABORTED-OR-FATAL` / `AUTHORIZED-DLP-RETRY-START` | `TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-CONSECUTIVE-TFTP-TRANSFERS-IN-SAME-OPERATION` |
| `CRS-M1-00188` | `DLP-CONSECUTIVE-TFTP-TRANSFER-EQUATION` | `LAST-PACKET-OF-PREVIOUS-TFTP-RECEIVED` → `FIRST-PACKET-OF-NEXT-TFTP-EMITTED` | `DLP-OPERATION-TERMINATED` / `NEW-DLP-SEQUENCE-STARTED` | `TARGET-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-PREVIOUS-LAST-RECEPTION-WITH-NEXT-FIRST-EMISSION` |
| `CRS-M1-00305` | `STATUS-EXCEPTION-SILENCE-DEADLINE` | `STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` → `FIRST-TARGET-STATUS-OR-RESPONSE-AFTER-SILENCE` | `OPERATION-ABORTED-OR-FATAL` / `NEWER-STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` | `TARGET-OPERATION-AND-STATUS-FILE-INSTANCE` / `PAIR-EXCEPTION-TIMER-WITH-TARGET-SILENCE-INTERVAL` |
| `CRS-M1-00322` | `STATUS-EXCEPTION-SILENCE-DEADLINE` | `STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` → `FIRST-TARGET-STATUS-OR-RESPONSE-AFTER-SILENCE` | `OPERATION-ABORTED-OR-FATAL` / `NEWER-STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` | `TARGET-OPERATION-AND-STATUS-FILE-INSTANCE` / `PAIR-EXCEPTION-TIMER-WITH-TARGET-SILENCE-INTERVAL` |
| `CRS-M1-00391` | `FIND-HOST-ANSWER-DEADLINE` | `FIND-REQUEST-RECEIVED-BY-HOST` → `FIND-ANSWER-SENT-BY-HOST` | `PROJECT-ASSUMPTION-UNRESOLVED-FIND-ABORT` / `NONE` | `FIND-REQUEST-INSTANCE` / `PAIR-FIND-REQUEST-WITH-HOST-ANSWER` |
| `CRS-M1-00520` | `FIND-ANSWER-REGISTRATION-WINDOW` | `FIND-REQUEST-SENT` → `FIND-ANSWER-WINDOW-LIFETIME-ELAPSED` | `PROJECT-ASSUMPTION-UNRESOLVED-FIND-ABORT` / `NONE` | `FIND-REQUEST-INSTANCE` / `PAIR-FIND-REQUEST-WITH-REGISTRATION-WINDOW` |
| `CRS-M1-00521` | `FIND-REGISTRATION-CLOSE-AT-EXPIRY` | `FIND-REQUEST-SENT` → `FIND-ANSWER-REGISTRATION-CLOSED` | `PROJECT-ASSUMPTION-UNRESOLVED-FIND-ABORT` / `NONE` | `FIND-REQUEST-INSTANCE` / `PAIR-FIND-REQUEST-WITH-REGISTRATION-CLOSE` |

## Requirement-level 615A → 665-5 traceability

| 665-5 CRS | Profile-scope admission | Disposition | Requirement-specific relations |
|---|---|---|---|
| `CRS-M1-00191` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00192` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00193` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00194` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00195` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00196` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00197` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00198` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00199` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00200` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00201` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00202` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00203` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00204` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00205` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00206` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00207` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00208` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00209` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00210` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00211` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00212` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00213` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00214` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00215` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00216` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00217` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00218` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00219` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00220` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00221` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00222` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00223` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00224` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00225` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00226` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00227` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00228` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00229` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00230` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00231` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00232` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00233` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00234` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00235` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00236` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00237` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00238` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00239` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00240` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00241` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00242` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00243` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00244` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00245` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00246` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00247` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00248` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00249` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00250` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00251` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |
| `CRS-M1-00252` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 is admitted by the bounded profile scope; this source proposition does not by itself establish a direct implication from a specific ARINC 615A-3 requirement. | — |

## Structured protocol-file field constraints

| CRS | File / ordinal | Field | Width | Repetition / presence / use | Encoding / termination | Notes |
|---|---|---|---|---|---|---|
| `CRS-M1-00282` | `LCI` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00283` | `LCI` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00284` | `LCI` / `3` | `FIELD-OPERATION-ACCEPTANCE-STATUS-CODE` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00285` | `LCI` / `4` | `FIELD-STATUS-DESCRIPTION-LENGTH` | `8` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00286` | `LCI` / `5` | `FIELD-STATUS-DESCRIPTION` | `0..2040` | `ONCE` / `WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00287` | `LCL` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00288` | `LCL` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00289` | `LCL` / `3` | `FIELD-NUMBER-OF-TARGET-HARDWARE` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00290` | `LCL` / `4` | `FIELD-LITERAL-NAME-LENGTH` | `8` | `PER-LITERAL-NAME` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00291` | `LCL` / `5` | `FIELD-LITERAL-NAME` | `8..2040` | `PER-LITERAL-NAME` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00292` | `LCL` / `6` | `FIELD-SERIAL-NUMBER-LENGTH` | `8` | `PER-LITERAL-NAME` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00293` | `LCL` / `7` | `FIELD-SERIAL-NUMBER` | `8..2040` | `PER-LITERAL-NAME` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00294` | `LCL` / `8` | `FIELD-NUMBER-OF-PART-NUMBERS` | `16` | `PER-LITERAL-NAME` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00295` | `LCL` / `9` | `FIELD-PART-NUMBER-LENGTH` | `8` | `PER-PART-NUMBER-WITHIN-LITERAL-NAME` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00296` | `LCL` / `10` | `FIELD-PART-NUMBER` | `8..2040` | `PER-PART-NUMBER-WITHIN-LITERAL-NAME` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00297` | `LCL` / `11` | `FIELD-AMENDMENT-LENGTH` | `8` | `PER-PART-NUMBER-WITHIN-LITERAL-NAME` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00298` | `LCL` / `12` | `FIELD-AMENDMENT` | `0..2040` | `PER-PART-NUMBER-WITHIN-LITERAL-NAME` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00299` | `LCL` / `13` | `FIELD-PART-DESIGNATION-LENGTH` | `8` | `PER-PART-NUMBER-WITHIN-LITERAL-NAME` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00300` | `LCL` / `14` | `FIELD-PART-DESIGNATION-TEXT` | `8..2040` | `PER-PART-NUMBER-WITHIN-LITERAL-NAME` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00301` | `LCS` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00302` | `LCS` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00303` | `LCS` / `3` | `FIELD-COUNTER` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00304` | `LCS` / `4` | `FIELD-INFORMATION-OPERATION-STATUS-CODE` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00305` | `LCS` / `5` | `FIELD-EXCEPTION-TIMER` | `16` | `ONCE` / `WHEN-STATUS-CODE-0002-OR-0004` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00306` | `LCS` / `6` | `FIELD-ESTIMATED-TIME` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00307` | `LCS` / `7` | `FIELD-STATUS-DESCRIPTION-LENGTH` | `8` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00308` | `LCS` / `8` | `FIELD-STATUS-DESCRIPTION` | `0..2040` | `ONCE` / `WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00309` | `LUR` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00310` | `LUR` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00311` | `LUR` / `3` | `FIELD-NUMBER-OF-HEADER-FILES` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00312` | `LUR` / `4` | `FIELD-HEADER-FILE-NAME-LENGTH` | `8` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00313` | `LUR` / `5` | `FIELD-HEADER-FILE-NAME` | `8..2040` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00314` | `LUR` / `6` | `FIELD-LOAD-PART-NUMBER-NAME-LENGTH` | `8` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00315` | `LUR` / `7` | `FIELD-LOAD-PART-NUMBER-NAME` | `8..2040` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00316` | `LUS` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00317` | `LUS` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00318` | `LUS` / `3` | `FIELD-UPLOAD-OPERATION-STATUS-CODE` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00319` | `LUS` / `4` | `FIELD-UPLOAD-STATUS-DESCRIPTION-LENGTH` | `8` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00320` | `LUS` / `5` | `FIELD-UPLOAD-STATUS-DESCRIPTION` | `0..2040` | `ONCE` / `WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00321` | `LUS` / `6` | `FIELD-COUNTER` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00322` | `LUS` / `7` | `FIELD-EXCEPTION-TIMER` | `16` | `ONCE` / `WHEN-STATUS-CODE-0002-OR-0004` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00323` | `LUS` / `8` | `FIELD-ESTIMATED-TIME` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00324` | `LUS` / `9` | `FIELD-LOAD-LIST-RATIO` | `24` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00325` | `LUS` / `10` | `FIELD-NUMBER-OF-HEADER-FILES` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00326` | `LUS` / `11` | `FIELD-HEADER-FILE-NAME-LENGTH` | `8` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00327` | `LUS` / `12` | `FIELD-HEADER-FILE-NAME` | `8..2040` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00328` | `LUS` / `13` | `FIELD-LOAD-PART-NUMBER-NAME-LENGTH` | `8` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00329` | `LUS` / `14` | `FIELD-LOAD-PART-NUMBER-NAME` | `8..2040` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00330` | `LUS` / `15` | `FIELD-LOAD-RATIO` | `24` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00331` | `LUS` / `16` | `FIELD-LOAD-STATUS` | `16` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00332` | `LUS` / `17` | `FIELD-LOAD-STATUS-DESCRIPTION-LENGTH` | `8` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00333` | `LUS` / `18` | `FIELD-LOAD-STATUS-DESCRIPTION` | `0..2040` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00459` | `LNR` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNR-FILE-LENGTH-32 |
| `CRS-M1-00460` | `LNR` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `FIXED-WIDTH-ASCII` / `FIXED-TWO-ASCII-CHARACTERS` | PROTOCOL-VERSION-TWO-ASCII-CHARACTERS |
| `CRS-M1-00461` | `LNR` / `3` | `FIELD-NUMBER-OF-FILES` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNR-NUMBER-OF-FILES-16 |
| `CRS-M1-00462` | `LNR` / `4` | `FIELD-FILE-NAME-LENGTH` | `8` | `PER-FILE-RECORD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNR-FILE-NAME-LENGTH-REPEAT |
| `CRS-M1-00463` | `LNR` / `5` | `FIELD-FILE-NAME` | `8-TO-2040` | `PER-FILE-RECORD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | LNR-FILE-NAME-REPEAT |
| `CRS-M1-00464` | `LNR` / `6` | `FIELD-USER-DEFINED-DATA-LENGTH` | `8` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNR-USER-DATA-LENGTH-ONCE |
| `CRS-M1-00465` | `LNR` / `7` | `FIELD-USER-DEFINED-DATA` | `0-TO-2040` | `ONCE` / `WHEN-LENGTH-FIELD-POSITIVE` / `—` | `LENGTH-PREFIXED-BINARY` / `LENGTH-PREFIXED-PER-TABLE` | LNR-USER-DATA-ONCE-NOT-PER-FILE |
| `CRS-M1-00466` | `LNS` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-FIELD-FILE-LENGTH-TABLE-WIDTH |
| `CRS-M1-00467` | `LNS` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `FIXED-WIDTH-ASCII` / `FIXED-TWO-ASCII-CHARACTERS` | PROTOCOL-VERSION-TWO-ASCII-CHARACTERS |
| `CRS-M1-00468` | `LNS` / `3` | `FIELD-DOWNLOAD-OPERATION-STATUS-CODE` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-FIELD-DOWNLOAD-OPERATION-STATUS-CODE-TABLE-WIDTH |
| `CRS-M1-00469` | `LNS` / `4` | `FIELD-DOWNLOAD-STATUS-DESCRIPTION-LENGTH` | `8` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-FIELD-DOWNLOAD-STATUS-DESCRIPTION-LENGTH-TABLE-WIDTH |
| `CRS-M1-00470` | `LNS` / `5` | `FIELD-DOWNLOAD-STATUS-DESCRIPTION` | `0-TO-2040` | `ONCE` / `WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | LNS-FIELD-DOWNLOAD-STATUS-DESCRIPTION-TABLE-WIDTH |
| `CRS-M1-00471` | `LNS` / `6` | `FIELD-COUNTER` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-FIELD-COUNTER-TABLE-WIDTH |
| `CRS-M1-00472` | `LNS` / `7` | `FIELD-EXCEPTION-TIMER` | `16` | `ONCE` / `ALWAYS` / `WHEN-STATUS-CODE-0002-OR-0004` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-EXCEPTION-TIMER-WHEN-STATUS-0002-OR-0004 |
| `CRS-M1-00473` | `LNS` / `8` | `FIELD-ESTIMATED-TIME` | `16` | `ONCE` / `ALWAYS` / `WHEN-STATUS-CODE-0002-OR-0004` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-ESTIMATED-TIME-WHEN-STATUS-0002-OR-0004, LNS-ESTIMATED-TIME-UNKNOWN-IS-0xFFFF |
| `CRS-M1-00474` | `LNS` / `9` | `FIELD-DOWNLOAD-LIST-RATIO` | `24` | `ONCE` / `ALWAYS` / `—` | `FIXED-WIDTH-ASCII` / `RIGHT-ADJUSTED-LEADING-BLANKS` | LNS-DOWNLOAD-LIST-RATIO-THREE-ASCII-PERCENT |
| `CRS-M1-00475` | `LNS` / `10` | `FIELD-NUMBER-OF-FILES` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-FIELD-NUMBER-OF-FILES-TABLE-WIDTH |
| `CRS-M1-00476` | `LNS` / `11` | `FIELD-FILE-NAME-LENGTH` | `8` | `PER-FILE-RECORD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-FIELD-FILE-NAME-LENGTH-TABLE-WIDTH |
| `CRS-M1-00477` | `LNS` / `12` | `FIELD-FILE-NAME` | `8-TO-2040` | `PER-FILE-RECORD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | LNS-FIELD-FILE-NAME-TABLE-WIDTH |
| `CRS-M1-00478` | `LNS` / `13` | `FIELD-FILE-STATUS` | `16` | `PER-FILE-RECORD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-FIELD-FILE-STATUS-TABLE-WIDTH |
| `CRS-M1-00479` | `LNS` / `14` | `FIELD-FILE-STATUS-DESCRIPTION-LENGTH` | `8` | `PER-FILE-RECORD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-FIELD-FILE-STATUS-DESCRIPTION-LENGTH-TABLE-WIDTH |
| `CRS-M1-00480` | `LNS` / `15` | `FIELD-FILE-STATUS-DESCRIPTION` | `0-TO-2040` | `PER-FILE-RECORD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | LNS-FIELD-FILE-STATUS-DESCRIPTION-TABLE-WIDTH |
| `CRS-M1-00481` | `LNL` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNL-FIELD-FILE-LENGTH-TABLE-WIDTH |
| `CRS-M1-00482` | `LNL` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `FIXED-WIDTH-ASCII` / `FIXED-TWO-ASCII-CHARACTERS` | PROTOCOL-VERSION-TWO-ASCII-CHARACTERS |
| `CRS-M1-00483` | `LNL` / `3` | `FIELD-NUMBER-OF-FILES` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNL-FIELD-NUMBER-OF-FILES-TABLE-WIDTH |
| `CRS-M1-00484` | `LNL` / `4` | `FIELD-FILE-NAME-LENGTH` | `8` | `PER-FILE-RECORD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNL-FIELD-FILE-NAME-LENGTH-TABLE-WIDTH |
| `CRS-M1-00485` | `LNL` / `5` | `FIELD-FILE-NAME` | `8-TO-2040` | `PER-FILE-RECORD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | LNL-FIELD-FILE-NAME-TABLE-WIDTH |
| `CRS-M1-00486` | `LNL` / `6` | `FIELD-FILE-DESCRIPTION-LENGTH` | `8` | `PER-FILE-RECORD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNL-FIELD-FILE-DESCRIPTION-LENGTH-TABLE-WIDTH |
| `CRS-M1-00487` | `LNL` / `7` | `FIELD-FILE-DESCRIPTION` | `0-TO-2040` | `PER-FILE-RECORD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | LNL-FIELD-FILE-DESCRIPTION-TABLE-WIDTH |
| `CRS-M1-00488` | `LNA` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNA-FIELD-FILE-LENGTH-TABLE-WIDTH |
| `CRS-M1-00489` | `LNA` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `FIXED-WIDTH-ASCII` / `FIXED-TWO-ASCII-CHARACTERS` | PROTOCOL-VERSION-TWO-ASCII-CHARACTERS |
| `CRS-M1-00490` | `LNA` / `3` | `FIELD-NUMBER-OF-FILES` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNA-FIELD-NUMBER-OF-FILES-TABLE-WIDTH |
| `CRS-M1-00491` | `LNA` / `4` | `FIELD-FILE-NAME-LENGTH` | `8` | `PER-FILE-RECORD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNA-FIELD-FILE-NAME-LENGTH-TABLE-WIDTH |
| `CRS-M1-00492` | `LNA` / `5` | `FIELD-FILE-NAME` | `8-TO-2040` | `PER-FILE-RECORD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | LNA-FIELD-FILE-NAME-TABLE-WIDTH |

## Structured Table 6.4.10-1 constraints

| CRS | Code / kind | Meaning / substitution | Display | Target text | Files / operations |
|---|---|---|---|---|---|
| `CRS-M1-00334` | `0X0001` | `ACCEPTED-NOT-STARTED` | `NO-DISPLAY` | `NOT-SPECIFIED` | `.LCI, .LCS, .LUI, .LUS, .LND, .LNO, .LNS` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00335` | `0X1000` | `OPERATION-DENIED` | `DISPLAY-CONTROLLED-TEMPLATE-AND-TARGET-TEXT` | `REQUIRED` | `.LCI, .LUI, .LND, .LNO` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00336` | `0X1002` | `OPERATION-NOT-SUPPORTED` | `DISPLAY-CONTROLLED-TEMPLATE` | `FORBIDDEN` | `.LCI, .LUI, .LND, .LNO` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00337` | `0X0002` | `IN-PROGRESS` | `ENTERTAIN-USER-WITHOUT-STATUS-TEXT` | `NOT-SPECIFIED` | `.LCS, .LUS, .LNS` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00338` | `0X0003` | `COMPLETED-WITHOUT-ERROR` | `DISPLAY-CONTROLLED-TEMPLATE` | `FORBIDDEN` | `.LCS, .LUS, .LNS` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00339` | `0X0004` | `IN-PROGRESS-WITH-TARGET-DETAIL` | `DISPLAY-TARGET-TEXT` | `REQUIRED` | `.LCS, .LUS, .LNS` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00340` | `0X1003` | `ABORTED-BY-TARGET` | `DISPLAY-CONTROLLED-TEMPLATE-AND-TARGET-TEXT` | `REQUIRED` | `.LCS, .LUS, .LNS` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00341` | `0X1004` | `ABORTED-BY-DATA-LOADER` | `DISPLAY-CONTROLLED-TEMPLATE` | `FORBIDDEN` | `.LCS, .LUS, .LNS` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00342` | `0X1005` | `ABORTED-BY-OPERATOR` | `DISPLAY-CONTROLLED-TEMPLATE` | `FORBIDDEN` | `.LCS, .LUS, .LNS` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00343` | `0X1007` | `LOAD-PART-FAILED` | `DISPLAY-IDENTIFIER-AND-FAILURE-TEMPLATE-AND-TARGET-TEXT` | `REQUIRED` | `.LUS` / `UPLOAD` |
| `CRS-M1-00344` | `0X1007` | `DOWNLOAD-FILE-FAILED` | `DISPLAY-IDENTIFIER-AND-FAILURE-TEMPLATE-AND-TARGET-TEXT` | `REQUIRED` | `.LNS` / `DOWNLOAD` |
| `CRS-M1-00345` | `DISPLAY-FOOTNOTE` | `SUBSTITUTE-ACTIVE-OPERATION-NAME` | — | — | — |

## Non-base and unresolved inventory

- `COV-M1-00001` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00002` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00003` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00004` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00005` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00006` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00007` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00008` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00009` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00010` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00011` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00012` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00013` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00014` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00015` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00016` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00017` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00018` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00019` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00051` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00052` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00053` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00054` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00055` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00056` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00057` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00058` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00059` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00060` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00061` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00062` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00063` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00064` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00065` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00066` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00067` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00068` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00069` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00070` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00071` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00072` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00073` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00074` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00075` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00076` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00083` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00084` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00085` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00086` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00087` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00088` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00089` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00090` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00091` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00092` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00093` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00094` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00095` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00096` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00097` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00098` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00099` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00100` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00101` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00102` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00103` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00104` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00105` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00106` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00107` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00108` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00109` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00110` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00111` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00112` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00113` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00114` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00115` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00116` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00117` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00118` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00119` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00120` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00121` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00122` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00123` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00124` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00125` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00126` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00127` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00128` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00129` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00130` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00131` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00132` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00133` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00134` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00135` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00136` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00137` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00138` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00139` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00140` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00141` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00142` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00143` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00144` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00145` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00146` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00147` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00148` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00149` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00150` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00151` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00152` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00153` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00154` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00155` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00156` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00157` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00158` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00159` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00160` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00161` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00162` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00163` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00164` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00165` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00166` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00167` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00168` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00169` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00170` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00171` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00172` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00173` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00174` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00175` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00176` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00177` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00178` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00179` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00180` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00181` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00182` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00183` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00184` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00185` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00186` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00187` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00188` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00189` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00190` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00191` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00192` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00193` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00194` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00195` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00196` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00197` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00198` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00199` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00200` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00201` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00202` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00203` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00204` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00205` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00206` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00207` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00208` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00209` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00210` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00211` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00212` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00213` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00214` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00215` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00216` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00217` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00218` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00219` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00220` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00221` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00222` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00223` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00224` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00225` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00226` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00227` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00228` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00229` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00230` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00231` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00232` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00233` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00234` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00235` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00236` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00237` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00238` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00239` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00240` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00241` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00242` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00243` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00244` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00245` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00246` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00247` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00248` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00249` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00250` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00251` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00252` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00253` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00254` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00255` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00256` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00257` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00258` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00259` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00260` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00261` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00262` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00263` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00264` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00265` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00266` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00267` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00268` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00269` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00270` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00271` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00272` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00273` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00274` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00275` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00276` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00277` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00278` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00279` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00280` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00281` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00282` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00283` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00284` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00285` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00286` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00287` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00288` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00289` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00290` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00291` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00292` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00293` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00294` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00295` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00296` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00297` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00298` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00299` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00300` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00301` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00302` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00303` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00304` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00305` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00306` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00307` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00308` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00309` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00310` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00311` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00312` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00313` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00314` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00315` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00316` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00317` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00318` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00319` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00320` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00321` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00322` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00323` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00324` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00325` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00326` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00327` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00328` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00329` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00330` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00331` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00332` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00333` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00334` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00335` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00336` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00337` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00338` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00339` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00340` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00341` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00342` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00343` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00344` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00345` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00346` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00347` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00348` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00349` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00350` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00351` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00352` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00353` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00354` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00355` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00692` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00693` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00694` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00696` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-00697` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-00698` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-00699` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-00700` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-00701` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-00702` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00703` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00704` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00705` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00706` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00707` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00708` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00709` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00710` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00711` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00712` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00713` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00714` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00715` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00716` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00717` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00718` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00719` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00720` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00721` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00722` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00723` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00724` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00725` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00726` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00727` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00728` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00729` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00730` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00731` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00732` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00733` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00734` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00735` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION-DESCRIPTION
- `COV-M1-00736` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION
- `COV-M1-00737` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION
- `COV-M1-00738` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION
- `COV-M1-00739` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION
- `COV-M1-00740` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION
- `COV-M1-00741` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION
- `COV-M1-00742` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION
- `COV-M1-00743` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION-DESCRIPTION
- `COV-M1-00744` — `OUT-OF-PROFILE` — NON-NORMATIVE-DOWNLOAD-EXAMPLE
- `COV-M1-00745` — `OUT-OF-PROFILE` — NON-NORMATIVE-DOWNLOAD-EXAMPLE
- `COV-M1-00746` — `OUT-OF-PROFILE` — NON-NORMATIVE-DOWNLOAD-EXAMPLE
- `COV-M1-00804` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00805` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00806` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00807` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00808` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00809` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00810` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00811` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00812` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00813` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00814` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00815` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00816` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00817` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00818` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00819` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00820` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00821` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00822` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00823` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00824` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00825` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00826` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00827` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00828` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00829` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00830` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00916` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00917` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00918` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00919` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00920` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00921` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00922` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00923` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00924` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00925` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00926` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00927` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00928` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00929` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00930` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00931` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00932` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00933` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00934` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00935` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00936` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00937` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00938` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00939` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00940` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00941` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00942` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00943` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00944` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00945` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00946` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00947` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00948` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00949` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00950` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00951` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00952` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00953` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00954` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00955` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00956` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00957` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00958` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00959` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00960` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00961` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00962` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00963` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00964` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00965` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00966` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00967` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00968` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00969` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00970` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00971` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00972` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00973` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00974` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00975` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00976` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-00977` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00978` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00979` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00980` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00981` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-00982` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00983` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-00984` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-00985` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00986` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00987` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00988` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00989` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00990` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00991` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00992` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00993` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-00994` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-00995` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-00996` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00997` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01273` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01274` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01275` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01276` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01277` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01278` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01279` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01280` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01281` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01282` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01283` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01284` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01285` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01286` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01287` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01288` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-01289` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01290` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01291` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01292` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01293` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01294` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01295` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01296` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01297` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01298` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01299` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01300` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01301` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01302` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01303` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01304` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01305` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01306` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01307` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01308` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01309` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01310` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01311` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01312` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01313` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01314` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01315` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01316` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01317` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01318` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01319` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01320` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01321` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01322` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01323` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01324` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01325` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01326` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01327` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01328` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01329` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01330` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01331` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01332` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01333` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01334` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01335` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01336` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01337` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01338` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01339` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01340` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01341` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01342` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01343` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01344` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01345` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01346` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01347` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01348` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01349` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01350` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01351` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01352` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01353` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01354` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01355` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01356` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01357` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01358` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01359` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01360` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01361` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01362` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01363` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01364` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01365` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01366` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01367` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01368` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01369` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01370` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01371` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01372` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01373` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01374` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01375` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01376` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01377` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01378` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01379` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01380` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01381` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01382` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01383` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01384` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01385` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01386` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01387` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-01388` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01389` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01390` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01391` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01392` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-01393` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-01394` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01395` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01396` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01397` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01398` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01399` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01400` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01401` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01402` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01403` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01404` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01405` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01406` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01407` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01408` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01409` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-01413` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01414` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01415` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01416` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01417` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01418` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01419` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01420` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01421` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01422` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01423` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01424` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01425` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01426` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01427` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01428` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01429` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01430` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01431` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01432` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01433` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01434` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01435` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01436` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01437` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01438` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01439` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01440` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01441` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01442` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01443` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01444` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01445` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01446` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01447` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01448` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01449` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01450` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01451` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01452` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01453` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01454` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01455` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01456` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01457` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01458` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01459` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01460` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01461` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01462` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01463` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01464` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01465` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01466` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01467` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01468` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01469` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01470` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01471` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01472` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01473` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01474` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01475` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01476` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01477` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01478` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01479` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01480` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01481` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01482` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01483` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01484` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01485` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01486` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01487` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01488` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01489` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01490` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01491` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01492` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01493` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01494` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01495` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01496` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01497` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01498` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01499` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01500` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01501` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01502` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01503` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01504` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01505` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01506` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01507` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01508` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01509` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01510` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01511` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01512` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01513` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01514` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01515` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01516` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01517` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01518` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01519` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01520` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01521` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01522` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01523` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01524` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01525` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01526` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01527` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01528` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01529` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01530` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01531` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01532` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01533` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01534` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01535` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01536` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01537` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01538` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01539` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01540` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01541` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01542` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01543` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01544` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01545` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01546` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01547` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01548` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01549` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01550` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01551` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01552` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01553` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01554` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01555` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01556` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01557` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01558` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01559` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01560` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01561` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01562` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01563` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01564` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01565` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01566` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01567` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01568` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01569` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01570` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01571` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01572` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01573` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01574` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01575` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01576` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01577` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01578` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01579` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01580` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01581` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01586` — `CONDITIONAL` — FIND-CONDITIONAL-DESCRIPTION
- `COV-M1-01587` — `CONDITIONAL` — FIND-CONDITIONAL-NETWORK-OR-PRELOAD
- `COV-M1-01588` — `CONDITIONAL` — FIND-CONDITIONAL-NETWORK-OR-PRELOAD
- `COV-M1-01589` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01590` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01591` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01592` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01593` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01596` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01597` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01598` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01599` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01604` — `CONDITIONAL` — FIND-CONDITIONAL-DESCRIPTION
- `COV-M1-01612` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01622` — `CONDITIONAL` — FIND-CONDITIONAL-NETWORK-OR-PRELOAD
- `COV-M1-01624` — `CONDITIONAL` — FIND-CONDITIONAL-NETWORK-OR-PRELOAD
- `COV-M1-01632` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01645` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01652` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-EXAMPLE
- `COV-M1-01653` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-EXAMPLE
- `COV-M1-01654` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01684` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01685` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01686` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01701` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01702` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01720` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01735` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01736` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01737` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01747` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01748` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01756` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01757` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01758` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01759` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01760` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01761` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01762` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01763` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01764` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01765` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01766` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01767` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01768` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01769` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01770` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01771` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01772` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01773` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01774` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01775` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01776` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01777` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01778` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01779` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01780` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01781` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01782` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01783` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01784` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01785` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01786` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01787` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01788` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01789` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01790` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01791` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01792` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01793` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01794` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01795` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01796` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01797` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01798` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01799` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01800` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01801` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01802` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01803` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01804` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01805` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01806` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01807` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01808` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01809` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01810` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01811` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01812` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01813` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01814` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01815` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01816` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01817` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01818` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01819` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01820` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01821` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01822` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01823` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01824` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01825` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01826` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01827` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01828` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01829` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01830` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01831` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01832` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01833` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01834` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01835` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01836` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01837` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01838` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01839` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01840` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01841` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01842` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01843` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01844` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01845` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01846` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01847` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01848` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01849` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01850` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01851` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01852` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01853` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01854` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01855` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01856` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01857` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01858` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01859` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01860` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01861` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01862` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01863` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01864` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01865` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01866` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01867` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01868` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01869` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01870` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01871` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01872` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01873` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01874` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01875` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01876` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01877` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01878` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01879` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01880` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01881` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01882` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01883` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01884` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01885` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01886` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01887` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01888` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01889` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01890` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01891` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01892` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01893` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01894` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01895` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01896` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01897` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01898` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01899` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01900` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01901` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01902` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01903` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01904` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01905` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01906` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01907` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01908` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01909` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01910` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01911` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01912` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01913` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01914` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01915` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01916` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01917` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01918` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01919` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01920` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01921` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01922` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01923` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01924` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01925` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01926` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01927` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01928` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01929` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01930` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01931` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01932` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01933` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01934` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01935` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01936` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01937` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01938` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01939` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01940` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01941` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01942` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01943` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01944` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01945` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01946` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01947` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01948` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01949` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01950` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01951` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01952` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01953` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01954` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01955` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01956` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01957` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01958` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01959` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01960` — `OUT-OF-PROFILE` — NON-NORMATIVE-AFDX-EXAMPLE
- `COV-M1-01961` — `OUT-OF-PROFILE` — NON-NORMATIVE-AFDX-EXAMPLE
- `COV-M1-01962` — `CONDITIONAL` — AFDX-CONDITIONAL-DESCRIPTION
- `COV-M1-01963` — `CONDITIONAL` — AFDX-CONDITIONAL-DESCRIPTION
- `COV-M1-01964` — `OUT-OF-PROFILE` — NON-NORMATIVE-AFDX-EXAMPLE
- `COV-M1-01965` — `OUT-OF-PROFILE` — NON-NORMATIVE-AFDX-EXAMPLE
- `COV-M1-01966` — `OUT-OF-PROFILE` — NON-NORMATIVE-AFDX-EXAMPLE
- `COV-M1-01967` — `CONDITIONAL` — AFDX-CONDITIONAL-DEPLOYMENT
- `COV-M1-01968` — `CONDITIONAL` — AFDX-CONDITIONAL-DESCRIPTION
- `COV-M1-01969` — `CONDITIONAL` — AFDX-CONDITIONAL-DESCRIPTION
- `COV-M1-01970` — `CONDITIONAL` — AFDX-CONDITIONAL-DEPLOYMENT
- `COV-M1-01971` — `CONDITIONAL` — AFDX-CONDITIONAL-DESCRIPTION
- `COV-M1-01972` — `CONDITIONAL` — AFDX-CONDITIONAL-DEPLOYMENT
- `COV-M1-01973` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01974` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01975` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01976` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01977` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01978` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01979` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01980` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01981` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01982` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01983` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01984` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01985` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01986` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01987` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01988` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01989` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01990` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01991` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01992` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01993` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01994` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01995` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01996` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01997` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01998` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01999` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02000` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02001` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02002` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02003` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02004` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02005` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02006` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02007` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02008` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02009` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02010` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02011` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02012` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02013` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02014` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02015` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02016` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02017` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02018` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02019` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02020` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02021` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02022` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02023` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02024` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02025` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02026` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02027` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02028` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02029` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02030` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02031` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02032` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02033` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02034` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02035` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02036` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02037` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02038` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02039` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02040` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02041` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02042` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02043` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02044` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02045` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02046` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02047` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02048` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02049` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02050` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02051` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02052` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02053` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02054` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02055` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02056` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02057` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02058` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02059` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02060` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02061` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02062` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02063` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02064` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02065` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02066` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02067` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02068` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02069` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02070` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02071` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02072` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02073` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02074` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02075` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02076` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02077` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02078` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02079` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02080` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02081` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02082` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02083` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02084` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02085` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02086` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02087` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02088` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02089` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02090` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02091` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02092` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02093` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02094` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02095` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02096` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02097` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02098` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02099` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02100` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02101` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02102` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02103` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02104` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02105` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02106` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02107` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02108` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02109` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02110` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02111` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02112` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02113` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02114` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02115` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02116` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02117` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02118` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02119` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02120` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02121` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02122` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02123` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02124` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02125` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02126` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02127` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02128` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02129` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02130` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02131` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02132` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02133` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02134` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02135` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02136` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02137` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02138` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02139` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02140` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02141` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02142` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02143` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02144` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02145` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02146` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02147` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02148` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02149` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02150` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02151` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02152` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02153` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02154` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02155` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02156` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02157` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02158` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02159` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02160` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02161` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02162` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02163` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02164` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02165` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02166` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02167` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02168` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02169` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02170` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02171` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02172` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02173` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02174` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02175` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02176` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02177` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02178` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02179` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02180` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02181` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02182` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02183` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02255` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02256` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02257` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02258` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02259` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02260` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02261` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02308` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02309` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02310` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02311` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02312` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02313` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02314` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02315` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02316` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02317` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02318` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02553` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02554` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02555` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02556` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02557` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02558` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02559` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02560` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02561` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02562` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02563` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02564` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02565` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02566` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02567` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02568` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02569` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02570` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02571` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02572` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02573` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02574` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02575` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02576` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02577` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02578` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02579` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02580` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02581` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02582` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02583` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02681` — `OUT-OF-PROFILE` — NON-NORMATIVE-DOWNLOAD-COMMENTARY
- `COV-M1-02682` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02683` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02684` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02685` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02686` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02687` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02688` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02689` — `OUT-OF-PROFILE` — NON-NORMATIVE-DOWNLOAD-COMMENTARY
- `COV-M1-02690` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02691` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02692` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02693` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02694` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02695` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02696` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02697` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02698` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02699` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02700` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02701` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02702` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02703` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02704` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02705` — `OUT-OF-PROFILE` — NON-NORMATIVE-DOWNLOAD-COMMENTARY
- `COV-M1-02706` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02707` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02708` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02709` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02710` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02711` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02712` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02713` — `OUT-OF-PROFILE` — NON-NORMATIVE-DOWNLOAD-COMMENTARY
- `COV-M1-02714` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02715` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02716` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02717` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02718` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02762` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02763` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02764` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02765` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02766` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02767` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02768` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02769` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02770` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02771` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02772` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02773` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02774` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02775` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02776` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02777` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02778` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02779` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02780` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02781` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02782` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02783` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02784` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02785` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED

# 中文版

本文件由 `configs/requirements/arinc_615a3_m1_crs.json` 生成；请勿手工编辑。

## 候选状态

- 处置：`ADOPT`
- RG0：`PENDING-EXTERNAL-INDEPENDENT-REVIEW`
- RG1：`PENDING-EXTERNAL-INDEPENDENT-REVIEW`
- 正式批准：`EXTERNAL-JOINT-CONDITION-NOT-YET-SATISFIED`
- 本数据包不建立 Project Configuration 或协议符合性。

## 清单

- 覆盖行：2796
- CRS 项：524
- 依赖：14
- 缺口：1
- 覆盖指纹：`806a197c7ec644f55d05dd8a6a31f80390ece5ccfe2e7d55a6816da6e2c04dfd`
- 需求指纹：`d9e4f22496734c5635f518b881f6c7ce9d8bd1a4fdea1f296b225f4422eacd3b`
- 来源单元指纹：`6de712854823ea8ebf7040306ae6c76540f9dc6356acf3fff75c108c53e55241`
- 自动检查只覆盖结构与跨记录一致性；专有来源的完整性与忠实度仍须外部 RG0 评审。
- `generatedSemanticProjectionEn/Zh` 是受断言约束的漂移投影，不是独立 RG1 证据。
- 665 边政策：`REQUIREMENT-LEVEL-615A-TO-665-EDGES-DEFERRED-TO-M2-ATTACHMENT-RECONCILIATION`

## 适用性

- `APPLICABLE-BASE`：89
- `APPLICABLE-SUPPORTING`：325
- `CONDITIONAL`：110

## 来源模态

- `FACT`：18
- `FIGURE-CONSTRAINT`：63
- `MAY`：55
- `MUST`：15
- `SHOULD`：246
- `TABLE-CONSTRAINT`：127

## 符合性效果

- `CONDITIONAL-REQUIRED`：99
- `OPTIONAL`：54
- `REQUIRED`：371

## 开放依赖与缺口

- `DEP-ARINC-645` — OPEN-DEPENDENCY：ARINC 645 算法来源仍未取得。
- `DEP-ARINC-664-2` — OPEN-DEPENDENCY：以太网物理层与链路层语义仍开放。
- `DEP-ARINC-664-3` — OPEN-DEPENDENCY：已接收 P3-1 身份；版次与网络适用性评审仍开放。
- `DEP-ARINC-664-7` — OPEN-DEPENDENCY：已接收 P7 初版；AFDX 延期，AID 未来补充版适用性仍开放。
- `DEP-ARINC-6655` — REGISTERED-SUPPORTING-SOURCE：有界数据对象来源。
- `DEP-RFC-1122` — OPEN-DEPENDENCY：已取得 RFC 1122 通信层来源身份；基础设施符合性及后续更新适用性尚未建立。
- `DEP-RFC-1123` — OPEN-DEPENDENCY：主机要求身份与适用性仍开放。
- `DEP-RFC-1350` — OPEN-DEPENDENCY：TFTP 基础身份与适用性仍开放。
- `DEP-RFC-1785` — OPEN-DEPENDENCY：TFTP 选项协商身份仍开放。
- `DEP-RFC-2347` — OPEN-DEPENDENCY：TFTP 选项扩展身份仍开放。
- `DEP-RFC-2348` — OPEN-DEPENDENCY：TFTP 块大小选项身份仍开放。
- `DEP-RFC-2349` — OPEN-DEPENDENCY：TFTP 超时与传输大小选项身份仍开放。
- `DEP-RFC-768` — OPEN-DEPENDENCY：UDP 身份与适用性仍开放。
- `DEP-RFC-791` — OPEN-DEPENDENCY：IP 身份与适用性仍开放。
- `GAP-ARINC-645` — NOT-ESTABLISHED：依赖 ARINC 645 的验证仍受阻。

## 网络引用审计与批准阻塞项

M1 选择 Compliant IPv4/UDP 网络服务。P3 裁剪例外与 AFDX 继续延期。引用区域检查不构成完整网络栈符合性证据；适用 RFC 服务行为属于显式、尚未验证的基础设施前提。

- Network mode: `COMPLIANT`; AFDX selected: `False`.

| ID | Source / edition | Clause / PDF page | Inspection boundary | Summary |
|---|---|---|---|---|
| `NET-P3-SCOPE` | `ARINC-664-3` / `664P3-1` | 1.2 / 8 | `INSPECTION-REGION` | P3 区分 Compliant 与 Profiled 网络；不同选择间的互操作性并不自动成立。 |
| `NET-P3-PRECEDENCE` | `ARINC-664-3` / `664P3-1` | 1.5 / 13 | `INSPECTION-REGION` | P3 在其适用的网络 profile 内限制 RFC 选项并规定优先级。 |
| `NET-P3-TFTP` | `ARINC-664-3` / `664P3-1` | 3.2.2-3.2.3 / 21 | `INSPECTION-REGION` | 基础 TFTP 引用选项 RFC；DL-TFTP 实现细节回引 615A。 |
| `NET-P3-UDP-RULE` | `ARINC-664-3` / `664P3-1` | 3.3.2 / 29 | `INSPECTION-REGION` | UDP 是最低传输要求；Profiled 表 X/E 标记决定遵循与可允许例外，不能统一降为建议。 |
| `NET-P3-UDP-TABLE` | `ARINC-664-3` / `664P3-1` | Table 3.3.2-1 / 30 | `DEFERRED-PROFILED-TABLE-REGION` | Profiled UDP 表区分校验和、源地址与接口义务。其偏差未选择；适用 RFC 行为仍是尚未验证的基础设施前提。 |
| `NET-P3-IP-RULE` | `ARINC-664-3` / `664P3-1` | 3.4.1 / 31 | `INSPECTION-REGION` | IPv4 裁剪使用独立要求表及明确的例外规则。 |
| `NET-P3-IP-TABLE` | `ARINC-664-3` / `664P3-1` | Table 3.4.1-1 / first page / 32 | `DEFERRED-PROFILED-TABLE-REGION` | Profiled 必选行包括 IPv4 版本和报头检查；该表尚未构成已纳入的叶级 CRS 清单。 |
| `NET-P3-FRAGMENT` | `ARINC-664-3` / `664P3-1` | Table 3.4.1-2 / 36 | `INSPECTION-REGION` | P3 允许 Profiled 网络采用特定重组偏差；这不能抹去 615A Data Loader 的分片／重组义务。 |
| `NET-P3-MTU` | `ARINC-664-3` / `664P3-1` | 3.4.1.2 / 36 | `INSPECTION-REGION` | MTU 可获知性与帧大小限制涉及网络配置及报文尺寸，并非 615A 操作时限。 |
| `NET-P3-ARP` | `ARINC-664-3` / `664P3-1` | 3.5.1 / 58 | `INSPECTION-REGION` | 动态 ARP 缓存接纳和静态映射失败处理属于需要选择部署条件的网络义务。 |
| `NET-P7-SCOPE` | `ARINC-664-7` / `664P7` | 1.2 / 9 | `INSPECTION-REGION` | AFDX 定义特定网络 profile，物理链路引用 P2。 |
| `NET-P7-TFTP` | `ARINC-664-7` / `664P7` | 3.3.1.2.3 / 40 | `INSPECTION-REGION` | AFDX 文件服务列出 TFTP RFC 与块处理能力；适用性以选择 AFDX 部署为条件。 |
| `NET-P7-EXAMPLE` | `ARINC-664-7` / `664P7` | 3.3.2 / 42 | `INSPECTION-REGION` | 示例端口和 VL 不能替代 615A 控制端口规则。 |
| `NET-P7-IP` | `ARINC-664-7` / `664P7` | 3.3.3.2 / 44 | `INSPECTION-REGION` | AFDX IPv4 尺寸考虑其序号并引用附件 2；它不是全局 TFTP 块大小或超时限制。 |
| `NET-P7-ADDRESS` | `ARINC-664-7` / `664P7` | 3.4.1.3.1-3.4.1.3.2 / 50 | `INSPECTION-REGION` | AFDX 内外寻址及双向 SAP／队列选择需要系统集成决策。 |
| `NET-P7-SWITCH` | `ARINC-664-7` / `664P7` | 4.9.1 / 75 | `INSPECTION-REGION` | 交换机软件加载引用 615A/665，但不能据此将 AFDX 交换机选为本 Profile 的目标。 |
| `NET-P7-PERFORMANCE` | `ARINC-664-7` / `664P7` | 5.1 / 80 | `INSPECTION-REGION` | AFDX 突发处理性能使用自身测量条件；它不建立 615A 传输超时。 |

| Relation | Owner | Target regions | Condition / disposition | Rationale / issues |
|---|---|---|---|---|
| `NET-REL-001` | `CRS-M1-00006` | NET-P3-SCOPE, NET-P3-PRECEDENCE, NET-P3-UDP-RULE, NET-P3-IP-RULE | `CURRENT-ETHERNET-PROFILE` / `APPLICABILITY-REVIEW-PENDING` | 615A 1.3 引用 P3。DD-023 选择其 Compliant Network 路径；P3 例外表不替代适用 RFC 行为。精确版次接受仍由外部评审决定。 / NET-ISSUE-EDITION, NET-ISSUE-PROFILE |
| `NET-REL-002` | `CRS-M1-00034` | NET-P3-FRAGMENT, NET-P3-MTU | `CURRENT-ETHERNET-PROFILE` / `APPLICABILITY-REVIEW-PENDING` | 保留当前 615A 加载器分片／重组义务。DD-023 排除 P3 不重组偏差；MTU 属于网络尺寸约束，并非操作时限。 / NET-ISSUE-PROFILE, NET-ISSUE-RFC1122 |
| `NET-REL-003` | `CRS-M1-00025` | NET-P3-TFTP, NET-P7-EXAMPLE | `CURRENT-ETHERNET-PROFILE` / `NO-NORMATIVE-OVERRIDE` | DL-TFTP 回引 615A；使用端口 69 的 AFDX 示例不覆盖 615A 端口 59。 /  |
| `NET-REL-004` | `CRS-M1-00020` | NET-P3-TFTP | `CURRENT-ETHERNET-PROFILE` / `APPLICABILITY-REVIEW-PENDING` | P3 为基础 TFTP 选项列出 RFC 2347；615A 端口选项的精确来源单元仍需评审，之后才可建立直接 RFC 边。 / NET-ISSUE-OPTION-EDGE |
| `NET-REL-005` | `COV-M1-01960` | NET-P7-SCOPE | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | 此附录 E 来源单元仅按条件 AFDX 语境检查；目标区域是评审定位，不证明存在等价的原子义务。 / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-006` | `COV-M1-01961` | NET-P7-SCOPE | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | 此附录 E 来源单元仅按条件 AFDX 语境检查；目标区域是评审定位，不证明存在等价的原子义务。 / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-007` | `COV-M1-01962` | NET-P7-SCOPE | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | 此附录 E 来源单元仅按条件 AFDX 语境检查；目标区域是评审定位，不证明存在等价的原子义务。 / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-008` | `COV-M1-01963` | NET-P7-ADDRESS | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | 此附录 E 来源单元仅按条件 AFDX 语境检查；目标区域是评审定位，不证明存在等价的原子义务。 / NET-ISSUE-AFDX-DETAIL, NET-ISSUE-AID |
| `NET-REL-009` | `COV-M1-01964` | NET-P7-ADDRESS | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | 此附录 E 来源单元仅按条件 AFDX 语境检查；目标区域是评审定位，不证明存在等价的原子义务。 / NET-ISSUE-AFDX-DETAIL, NET-ISSUE-AID |
| `NET-REL-010` | `COV-M1-01965` | NET-P7-ADDRESS | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | 此附录 E 来源单元仅按条件 AFDX 语境检查；目标区域是评审定位，不证明存在等价的原子义务。 / NET-ISSUE-AFDX-DETAIL, NET-ISSUE-AID |
| `NET-REL-011` | `COV-M1-01966` | NET-P7-SCOPE | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | 此附录 E 来源单元仅按条件 AFDX 语境检查；目标区域是评审定位，不证明存在等价的原子义务。 / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-012` | `COV-M1-01967` | NET-P7-ADDRESS | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | 此附录 E 来源单元仅按条件 AFDX 语境检查；目标区域是评审定位，不证明存在等价的原子义务。 / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-013` | `COV-M1-01968` | NET-P7-ADDRESS | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | 此附录 E 来源单元仅按条件 AFDX 语境检查；目标区域是评审定位，不证明存在等价的原子义务。 / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-014` | `COV-M1-01969` | NET-P7-ADDRESS | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | 此附录 E 来源单元仅按条件 AFDX 语境检查；目标区域是评审定位，不证明存在等价的原子义务。 / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-015` | `COV-M1-01970` | NET-P7-TFTP, NET-P7-EXAMPLE | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | 此附录 E 来源单元仅按条件 AFDX 语境检查；目标区域是评审定位，不证明存在等价的原子义务。 / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-016` | `COV-M1-01971` | NET-P7-IP, NET-P7-PERFORMANCE | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | 此附录 E 来源单元仅按条件 AFDX 语境检查；目标区域是评审定位，不证明存在等价的原子义务。 / NET-ISSUE-AFDX-DETAIL |
| `NET-REL-017` | `COV-M1-01972` | NET-P7-ADDRESS | `IF-AFDX-TRANSPORT-CHOSEN` / `DEFERRED-FUTURE-SCOPE` | 此附录 E 来源单元仅按条件 AFDX 语境检查；目标区域是评审定位，不证明存在等价的原子义务。 / NET-ISSUE-AFDX-DETAIL, NET-ISSUE-ADDRESS |

| Issue | Blocks M1 approval | Status | Required resolution |
|---|---|---|---|
| `NET-ISSUE-EDITION` | `True` | `OPEN` | 本候选固定精确历史版次；独立 RG0 须确认此版次边界解释，不是最新版符合性。P3 补充 1 描述继续支持 IPv4；P7 AID 未来补充版问题单独延期。 |
| `NET-ISSUE-PROFILE` | `False` | `RESOLVED-BY-SCOPE-DECISION` | 用户按 DD-023 选择 Compliant Network；不采用 P3 例外列。遵循 RFC 的 IPv4/UDP 行为仍是尚未验证的基础设施前提。 |
| `NET-ISSUE-RFC1122` | `False` | `SOURCE-ACQUIRED-REVIEW-PENDING` | 已从 RFC Editor 取得 RFC 1122 并记录不可变内容哈希。其适用义务与更新仍属于基础设施前提；取得原文不是符合性证据。 |
| `NET-ISSUE-OPTION-EDGE` | `False` | `OPEN` | A-2 继续延期：P3 3.2.2 列出 RFC 2347 且 P7 列出 RFC 1785，但这不证明精确的活动 615A 原子触发边。 |
| `NET-ISSUE-AFDX-DETAIL` | `False` | `OPEN` | AFDX 尚未选择；P7 附件 2、IEEE 802.3（2000）及配置相关延迟／MTU 须在后续纳入部署时审计。 |
| `NET-ISSUE-AID` | `False` | `OPEN` | 615A 附录 E 将 AID 指向未来 P7 补充版；所提供初版不能关闭该未来补充版引用。 |
| `NET-ISSUE-ADDRESS` | `False` | `OPEN` | 附录 E 允许 P4 寻址规则或集成商规定要求；须在 AFDX 激活前记录选择，不能自动将 P4 变为采购要求。 |

### 基础设施前提与公共来源

`DD-023`

- `NET-PREMISE-IPV4-UDP` / `NOT-ESTABLISHED` / `PROJECT-CONFIGURATION-GATE`: 底层 IPv4/UDP 服务须遵循适用 IETF 主机要求，不采用 P3 特有偏差。此项作为基础设施前提保留；未声称实现符合性或完整 RFC 需求清单。M2 须规划其验证，之后才可批准任何执行配置。
- `RFC-1122`: https://www.rfc-editor.org/rfc/rfc1122.txt / SHA-256 `9f526e6bebc868324fedb90aebbcf6e5b15c53fd373ca5d5ce1c2cdcd264e04f`

## CRS 项

| ID | 来源单元 | 参与者／条件／行为／对象／可观察结果 | 模态／效果 | 适用性 | 生成语义投影（受断言约束） | 时序溯源 | 依赖／缺口 |
|---|---|---|---|---|---|---|---|
| `CRS-M1-00001` | `SU-ARINC-615A-3-1-2-P014-PROSE-SENTENCE-002-8D3CB7C14FBD`<br>`ARINC-615A-3 1.2 p.2` | `ARINC-615A-CONFORMING-IMPLEMENTATION` / `UNCONDITIONAL` / `IMPLEMENT-REQUIRED-STANDARD-FUNCTIONS` / `MINIMUM-COMPATIBILITY-FUNCTION-SET` / `COMPATIBILITY-CAPABILITY-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-615A-CONFORMING-IMPLEMENTATION”在“UNCONDITIONAL”下必须对“MINIMUM-COMPATIBILITY-FUNCTION-SET”执行“IMPLEMENT-REQUIRED-STANDARD-FUNCTIONS”；证据是“COMPATIBILITY-CAPABILITY-OBSERVABLE”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00002` | `SU-ARINC-615A-3-1-2-P014-PROSE-SENTENCE-003-8280DDEE506E`<br>`ARINC-615A-3 1.2 p.2` | `ARINC-615A-REQUIREMENT-INTERPRETER` / `WHEN-INTERPRETING-ARINC-615A-NORMATIVE-LANGUAGE` / `TREAT-615A-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY` / `ARINC-615A-SHOULD-MODALITY` / `MODALITY-INTERPRETATION-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-615A-REQUIREMENT-INTERPRETER”在“WHEN-INTERPRETING-ARINC-615A-NORMATIVE-LANGUAGE”下必须对“ARINC-615A-SHOULD-MODALITY”执行“TREAT-615A-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY”；证据是“MODALITY-INTERPRETATION-OBSERVABLE”。 | — | — |
| `CRS-M1-00003` | `SU-ARINC-615A-3-1-2-P014-PROSE-SENTENCE-004-9B5A3832A655`<br>`ARINC-615A-3 1.2 p.2` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `USE` / `CONFORMANCE-MODALITY` / `USE-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下可以对“CONFORMANCE-MODALITY”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00004` | `SU-ARINC-615A-3-1-2-P014-PROSE-SENTENCE-005-7D9A4E2DA48E`<br>`ARINC-615A-3 1.2 p.2` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `WHEN-OPTIONAL-CAPABILITY-IMPLEMENTED` / `IMPLEMENT` / `CONFORMANCE-MODALITY` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“实现可选能力时”下必须对“CONFORMANCE-MODALITY”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00005` | `SU-ARINC-615A-3-1-3-P014-PROSE-SENTENCE-001-2FA34C046AFB`<br>`ARINC-615A-3 1.3 p.2` | `DATA-LOADER` / `UNCONDITIONAL` / `TRANSFER` / `SOFTWARE-PART` / `TRANSFER-OUTCOME-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“UNCONDITIONAL”下必须对“软件加载件”执行“传输”；证据是“传输结果可被观察”。 | — | — |
| `CRS-M1-00006` | `SU-ARINC-615A-3-1-3-P014-PROSE-SENTENCE-002-873AFAE35C45`<br>`ARINC-615A-3 1.3 p.2` | `DATA-LOADER-AND-TARGET-HARDWARE` / `UNCONDITIONAL` / `TRANSFER-VIA-ETHERNET` / `DATA-TRANSFER` / `ETHERNET-TRANSFER-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“DATA-LOADER-AND-TARGET-HARDWARE”在“UNCONDITIONAL”下必须对“DATA-TRANSFER”执行“TRANSFER-VIA-ETHERNET”；证据是“ETHERNET-TRANSFER-OBSERVABLE”。 | — | DEP-ARINC-664-2, DEP-ARINC-664-3 |
| `CRS-M1-00007` | `SU-ARINC-615A-3-1-3-P014-PROSE-SENTENCE-007-EC7965CC3D31`<br>`ARINC-615A-3 1.3 p.2` | `DATA-LOADER` / `UNCONDITIONAL` / `IMPLEMENT` / `OPERATION, NETWORK-INTERFACE` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“UNCONDITIONAL”下必须对“协议操作、网络接口”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00008` | `SU-ARINC-615A-3-1-3-P014-PROSE-SENTENCE-009-00560ACC8ACC`<br>`ARINC-615A-3 1.3 p.2` | `ARINC-615A-DEFINITION` / `UNCONDITIONAL` / `ALLOW-COMBINATION` / `DATA-LOADING-TYPES` / `COMBINED-LOADING-CAPABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-615A-DEFINITION”在“UNCONDITIONAL”下必须对“DATA-LOADING-TYPES”执行“ALLOW-COMBINATION”；证据是“COMBINED-LOADING-CAPABILITY-OBSERVABLE”。 | — | — |
| `CRS-M1-00009` | `SU-ARINC-615A-3-1-3-P015-PROSE-SENTENCE-011-06D3CBD76B0F`<br>`ARINC-615A-3 1.3 p.3` | `ARINC-615A-TRANSPORT-INTEGRATOR` / `WHEN-TRANSPORTING-ARINC-615A-OVER-AN-ALTERNATE-NETWORK` / `PRESERVE-PROTOCOL-SEMANTICS-OVER-ALTERNATE-NETWORK` / `ALTERNATE-NETWORK-TRANSPORT` / `TRANSPORT-COMPATIBILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-615A-TRANSPORT-INTEGRATOR”在“WHEN-TRANSPORTING-ARINC-615A-OVER-AN-ALTERNATE-NETWORK”下必须对“ALTERNATE-NETWORK-TRANSPORT”执行“PRESERVE-PROTOCOL-SEMANTICS-OVER-ALTERNATE-NETWORK”；证据是“TRANSPORT-COMPATIBILITY-OBSERVABLE”。 | — | — |
| `CRS-M1-00010` | `SU-ARINC-615A-3-1-3-P015-PROSE-SENTENCE-014-ACDCC666CD78`<br>`ARINC-615A-3 1.3 p.3` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `IMPLEMENT` / `NETWORK-INTERFACE` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“网络接口”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00011` | `SU-ARINC-615A-3-1-3-P015-PROSE-SENTENCE-015-C47A9C5EA9CF`<br>`ARINC-615A-3 1.3 p.3` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `SELECT` / `SOFTWARE-PART, OPERATION, TARGET-HARDWARE-ID` / `SELECT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“软件加载件、协议操作、TARGET-HARDWARE-ID”执行“选择”；证据是“SELECT-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00012` | `SU-ARINC-615A-3-1-6-P017-PROSE-SENTENCE-001-6E91C83C11CE`<br>`ARINC-615A-3 1.6 p.5` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `DESIGN` / `NETWORK-INTERFACE` / `DESIGN-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“网络接口”执行“设计”；证据是“DESIGN-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00013` | `SU-ARINC-615A-3-1-6-P017-PROSE-SENTENCE-003-817EC6E68797`<br>`ARINC-615A-3 1.6 p.5` | `DATA-LOADER` / `UNCONDITIONAL` / `IMPLEMENT` / `NETWORK-INTERFACE` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“UNCONDITIONAL”下必须对“网络接口”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00014` | `SU-ARINC-615A-3-1-6-P017-PROSE-SENTENCE-004-1768AAB8F452`<br>`ARINC-615A-3 1.6 p.5` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ENCODE` / `NETWORK-INTERFACE` / `ENCODED-FIELD-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下可以对“网络接口”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00015` | `SU-ARINC-615A-3-1-6-P017-PROSE-SENTENCE-005-358B4BAB3D69`<br>`ARINC-615A-3 1.6 p.5` | `PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ENCODE` / `NETWORK-INTERFACE` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议实现”在“UNCONDITIONAL”下必须对“网络接口”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00016` | `SU-ARINC-615A-3-1-6-P017-PROSE-SENTENCE-006-711482ED9B24`<br>`ARINC-615A-3 1.6 p.5` | `SOFTWARE-PACKAGE-PRODUCER` / `UNCONDITIONAL` / `COMPLY` / `SOFTWARE-PART, NETWORK-INTERFACE` / `COMPLY-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“软件包生成方”在“UNCONDITIONAL”下必须对“软件加载件、网络接口”执行“符合”；证据是“COMPLY-RESULT-OBSERVABLE”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00017` | `SU-ARINC-615A-3-5-1-P034-PROSE-SENTENCE-015-441CC925118B`<br>`ARINC-615A-3 5.1 p.22` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `PROTOCOL-FILE-NAME` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“UNCONDITIONAL”下必须对“PROTOCOL-FILE-NAME”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00018` | `SU-ARINC-615A-3-5-1-P034-PROSE-SENTENCE-016-EE8EBA5E1E47`<br>`ARINC-615A-3 5.1 p.22` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `COMPLY` / `NETWORK-INTERFACE` / `COMPLY-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“网络接口”执行“符合”；证据是“COMPLY-RESULT-OBSERVABLE”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00019` | `SU-ARINC-615A-3-5-2-P035-PROSE-SENTENCE-017-D07026646B5D`<br>`ARINC-615A-3 5.2 p.23` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `USE` / `FIND-SERVICE, TARGET-HARDWARE-ID` / `USE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“FIND-SERVICE、TARGET-HARDWARE-ID”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00020` | `SU-ARINC-615A-3-5-3-2-2-P037-PROSE-SENTENCE-001-5DE45B64D498`<br>`ARINC-615A-3 5.3.2.2 p.25` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `TRANSFER` / `TFTP-OPTION` / `TRANSFER-OUTCOME-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下可以对“TFTP 选项”执行“传输”；证据是“传输结果可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00021` | `SU-ARINC-615A-3-5-3-2-2-P037-PROSE-SENTENCE-003-DE334C18716C`<br>`ARINC-615A-3 5.3.2.2 p.25` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `USE` / `DEFAULT-OPTION-VALUES` / `USE-RESULT-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“DEFAULT-OPTION-VALUES”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00022` | `SU-ARINC-615A-3-5-3-2-2-P037-PROSE-SENTENCE-004-FC7D3B3729A1`<br>`ARINC-615A-3 5.3.2.2 p.25` | `ARINC-615A-TFTP-IMPLEMENTATION` / `WHEN-A-TFTP-OPTION-IS-NOT-IMPLEMENTED` / `DO-NOT-FAIL-TRANSFER-FOR-UNIMPLEMENTED-OPTION` / `TFTP-TRANSFER, UNIMPLEMENTED-TFTP-OPTION` / `ABSENCE-OF-OPTION-CAUSED-TRANSFER-FAILURE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-615A-TFTP-IMPLEMENTATION”在“WHEN-A-TFTP-OPTION-IS-NOT-IMPLEMENTED”下必须对“TFTP-TRANSFER、UNIMPLEMENTED-TFTP-OPTION”执行“DO-NOT-FAIL-TRANSFER-FOR-UNIMPLEMENTED-OPTION”；证据是“ABSENCE-OF-OPTION-CAUSED-TRANSFER-FAILURE-OBSERVABLE”。 | — | — |
| `CRS-M1-00023` | `SU-ARINC-615A-3-5-3-2-2-P037-PROSE-SENTENCE-005-C966C11D19B8`<br>`ARINC-615A-3 5.3.2.2 p.25` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `AFTER-LAST-TFTP-OPTION` / `ABSENT-AFTER-BOUNDARY` / `TFTP-OPTION, NETWORK-INTERFACE` / `ABSENT-AFTER-BOUNDARY-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“最后一个 TFTP 选项结束后”下必须对“TFTP 选项、网络接口”执行“确保边界后不存在数据”；证据是“ABSENT-AFTER-BOUNDARY-RESULT-OBSERVABLE”。 | — | DEP-RFC-768, DEP-RFC-791, DEP-RFC-1350 |
| `CRS-M1-00024` | `SU-ARINC-615A-3-5-3-2-3-2-P037-PROSE-SENTENCE-002-1E0F8D921559`<br>`ARINC-615A-3 5.3.2.3.2 p.25` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `TRANSFER` / `TARGET-HARDWARE-ID` / `TRANSFER-OUTCOME-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下可以对“TARGET-HARDWARE-ID”执行“传输”；证据是“传输结果可被观察”。 | — | — |
| `CRS-M1-00025` | `SU-ARINC-615A-3-5-3-2-3-2-P037-PROSE-SENTENCE-004-F3852739104C`<br>`ARINC-615A-3 5.3.2.3.2 p.25` | `ARINC-615A-TFTP-IMPLEMENTATION` / `UNCONDITIONAL` / `USE-WELL-KNOWN-PORT` / `TFTP-PORT-59` / `TFTP-PORT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-615A-TFTP-IMPLEMENTATION”在“UNCONDITIONAL”下必须对“TFTP-PORT-59”执行“USE-WELL-KNOWN-PORT”；证据是“TFTP-PORT-OBSERVABLE”。 | — | DEP-RFC-1350 |
| `CRS-M1-00026` | `SU-ARINC-615A-3-5-3-2-3-3-P038-PROSE-SENTENCE-004-15DBABB1142A`<br>`ARINC-615A-3 5.3.2.3.3 p.26` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `USE` / `ERROR-CODE` / `USE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“错误码”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00027` | `SU-ARINC-615A-3-5-3-2-3-3-P038-PROSE-SENTENCE-005-A1C528A5F702`<br>`ARINC-615A-3 5.3.2.3.3 p.26` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `ERROR-CODE, ERROR-MESSAGE` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“UNCONDITIONAL”下必须对“错误码、错误消息”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00028` | `SU-ARINC-615A-3-5-3-2-3-3-P038-PROSE-SENTENCE-006-06665FE11D6E`<br>`ARINC-615A-3 5.3.2.3.3 p.26` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `ERROR-CODE, ERROR-MESSAGE` / `ENCODED-FIELD-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“UNCONDITIONAL”下可以对“错误码、错误消息”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00029` | `SU-ARINC-615A-3-5-3-2-3-3-P038-PROSE-SENTENCE-007-2560DF2DBBD3`<br>`ARINC-615A-3 5.3.2.3.3 p.26` | `DATA-LOADER` / `UNCONDITIONAL` / `REPORT-RESOURCE-UNAVAILABLE` / `TFTP-ERROR-CODE-3` / `ERROR-PACKET-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“UNCONDITIONAL”下必须对“TFTP-ERROR-CODE-3”执行“REPORT-RESOURCE-UNAVAILABLE”；证据是“ERROR-PACKET-OBSERVABLE”。 | — | DEP-RFC-1350 |
| `CRS-M1-00030` | `SU-ARINC-615A-3-5-3-2-3-3-P038-PROSE-SENTENCE-008-B72528E71CC2`<br>`ARINC-615A-3 5.3.2.3.3 p.26` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `REPORT-RESOURCE-UNAVAILABLE` / `TFTP-ERROR-CODE-3` / `ERROR-PACKET-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“TFTP-ERROR-CODE-3”执行“REPORT-RESOURCE-UNAVAILABLE”；证据是“ERROR-PACKET-OBSERVABLE”。 | — | DEP-RFC-1350 |
| `CRS-M1-00031` | `SU-ARINC-615A-3-5-3-2-3-4-P038-PROSE-SENTENCE-004-1F95516BE886`<br>`ARINC-615A-3 5.3.2.3.4 p.26` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `TRANSFER` / `PROTOCOL-MESSAGE` / `TRANSFER-OUTCOME-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下可以对“PROTOCOL-MESSAGE”执行“传输”；证据是“传输结果可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00032` | `SU-ARINC-615A-3-5-3-2-3-4-P038-PROSE-SENTENCE-006-D6FEB985BBBB`<br>`ARINC-615A-3 5.3.2.3.4 p.26` | `TFTP-WAIT-RECEIVER` / `WHEN-A-WAIT-MESSAGE-IS-RECEIVED` / `ABORT-AND-RESTART-AFTER-DELAY` / `CURRENT-TFTP-TRANSFER, WAIT-DELAY` / `ABORT-THEN-RETRY-SEQUENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“TFTP-WAIT-RECEIVER”在“WHEN-A-WAIT-MESSAGE-IS-RECEIVED”下必须对“CURRENT-TFTP-TRANSFER、WAIT-DELAY”执行“ABORT-AND-RESTART-AFTER-DELAY”；证据是“ABORT-THEN-RETRY-SEQUENCE-OBSERVABLE”。 | `MESSAGE-CARRIED-PARAMETER` / `MESSAGE-TIMER-VALUE` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-TABLE-6_4_3-1-R006 | DEP-RFC-1350 |
| `CRS-M1-00033` | `SU-ARINC-615A-3-5-3-2-3-8-P040-PROSE-SENTENCE-002-ADF7BE206185`<br>`ARINC-615A-3 5.3.2.3.8 p.28` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ENCODE` / `NETWORK-INTERFACE` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“网络接口”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00034` | `SU-ARINC-615A-3-5-3-2-3-8-1-P040-PROSE-SENTENCE-001-28CC7C395DC9`<br>`ARINC-615A-3 5.3.2.3.8.1 p.28` | `DATA-LOADER` / `UNCONDITIONAL` / `IMPLEMENT` / `TFTP-BLOCK-SIZE, NETWORK-INTERFACE` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“UNCONDITIONAL”下必须对“TFTP 块大小、网络接口”执行“提供能力”；证据是“能力可用性可被观察”。 | — | DEP-RFC-791, DEP-RFC-1350, DEP-RFC-2348 |
| `CRS-M1-00035` | `SU-ARINC-615A-3-5-3-2-3-8-1-P040-PROSE-SENTENCE-002-A3F954863D43`<br>`ARINC-615A-3 5.3.2.3.8.1 p.28` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `IMPLEMENT` / `CONFORMANCE-MODALITY, TARGET-HARDWARE-ID` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“CONFORMANCE-MODALITY、TARGET-HARDWARE-ID”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00036` | `SU-ARINC-615A-3-5-3-2-3-8-1-P041-PROSE-SENTENCE-003-C74E9B3EC0A0`<br>`ARINC-615A-3 5.3.2.3.8.1 p.29` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `USE` / `TFTP-BLOCK-SIZE, TARGET-HARDWARE-ID` / `USE-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下可以对“TFTP 块大小、TARGET-HARDWARE-ID”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | DEP-RFC-1350, DEP-RFC-2348 |
| `CRS-M1-00037` | `SU-ARINC-615A-3-5-3-2-3-8-2-P041-PROSE-SENTENCE-001-700C898C606C`<br>`ARINC-615A-3 5.3.2.3.8.2 p.29` | `PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `USE` / `NETWORK-INTERFACE` / `USE-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“协议实现”在“UNCONDITIONAL”下可以对“网络接口”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00038` | `SU-ARINC-615A-3-5-3-2-3-8-2-P041-PROSE-SENTENCE-002-A12EC6F8831E`<br>`ARINC-615A-3 5.3.2.3.8.2 p.29` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `WHEN-TRANSFER-SIZE-MISMATCHES` / `COMPARE` / `TFTP-TRANSFER-SIZE, TFTP-FILE-TRANSFER` / `COMPARISON-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“声明传输大小与实际数据不一致时”下必须对“TFTP 传输大小、TFTP 文件传输”执行“比较”；证据是“比较结果可被观察”。 | — | DEP-RFC-2349 |
| `CRS-M1-00039` | `SU-ARINC-615A-3-5-3-2-3-8-3-P041-PROSE-SENTENCE-001-700C898C606C`<br>`ARINC-615A-3 5.3.2.3.8.3 p.29` | `PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `USE` / `NETWORK-INTERFACE` / `USE-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“协议实现”在“UNCONDITIONAL”下可以对“网络接口”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00040` | `SU-ARINC-615A-3-5-3-2-3-8-4-P041-PROSE-SENTENCE-001-700C898C606C`<br>`ARINC-615A-3 5.3.2.3.8.4 p.29` | `PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `USE` / `NETWORK-INTERFACE` / `USE-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“协议实现”在“UNCONDITIONAL”下可以对“网络接口”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00041` | `SU-ARINC-615A-3-5-3-2-3-8-5-P041-PROSE-SENTENCE-001-700C898C606C`<br>`ARINC-615A-3 5.3.2.3.8.5 p.29` | `PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `USE` / `NETWORK-INTERFACE` / `USE-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“协议实现”在“UNCONDITIONAL”下可以对“网络接口”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00042` | `SU-ARINC-615A-3-5-3-2-3-8-5-P042-PROSE-SENTENCE-009-89192D1CA807`<br>`ARINC-615A-3 5.3.2.3.8.5 p.30` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ENCODE` / `HEADER-FILE, CRC, SOFTWARE-PART, TARGET-HARDWARE-ID` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“头文件、CRC／校验值、软件加载件、TARGET-HARDWARE-ID”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | DEP-RFC-1350, DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00043` | `SU-ARINC-615A-3-5-3-2-3-8-5-P042-PROSE-SENTENCE-010-B47966431472`<br>`ARINC-615A-3 5.3.2.3.8.5 p.30` | `DATA-LOADER` / `WHEN-THE-CHECKSUM-OPTION-IS-PRESENT` / `LOCATE-REQUESTED-FILE-USING-INCLUDED-CRC` / `REQUESTED-FILE, INCLUDED-CRC` / `REQUESTED-FILE-SELECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“WHEN-THE-CHECKSUM-OPTION-IS-PRESENT”下必须对“REQUESTED-FILE、INCLUDED-CRC”执行“LOCATE-REQUESTED-FILE-USING-INCLUDED-CRC”；证据是“REQUESTED-FILE-SELECTION-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00044` | `SU-ARINC-615A-3-5-3-2-3-8-5-P042-PROSE-SENTENCE-018-7A289A4F990C`<br>`ARINC-615A-3 5.3.2.3.8.5 p.30` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `USE` / `CRC` / `USE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“CRC／校验值”执行“使用”；证据是“USE-RESULT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00045` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-022-12774BEEEE8C`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `IMPLEMENT` / `NETWORK-INTERFACE, TARGET-HARDWARE-ID` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下可以对“网络接口、TARGET-HARDWARE-ID”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00046` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-023-5321224DBF5C`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `SOFTWARE-PACKAGE-PRODUCER` / `UNCONDITIONAL` / `IMPLEMENT` / `HEADER-FILE, CRC, SOFTWARE-PART, NETWORK-INTERFACE` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“软件包生成方”在“UNCONDITIONAL”下必须对“头文件、CRC／校验值、软件加载件、网络接口”执行“提供能力”；证据是“能力可用性可被观察”。 | — | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00047` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-024-04F65EF5ECB7`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `DATA-LOADER` / `UNCONDITIONAL` / `SEND` / `CRC` / `MESSAGE-OR-FILE-DIRECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“UNCONDITIONAL”下必须对“CRC／校验值”执行“发送”；证据是“消息或文件及其方向可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00048` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-026-443ABAEE9FB5`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `TRANSFER` / `NETWORK-INTERFACE, TARGET-HARDWARE-ID, LCL-TRANSFER` / `TRANSFER-OUTCOME-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下可以对“网络接口、TARGET-HARDWARE-ID、LCL-TRANSFER”执行“传输”；证据是“传输结果可被观察”。 | — | — |
| `CRS-M1-00049` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-027-6937C2561848`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `SEND` / `CRC, NETWORK-INTERFACE` / `MESSAGE-OR-FILE-DIRECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“CRC／校验值、网络接口”执行“发送”；证据是“消息或文件及其方向可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00050` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-029-CCAB139B0370`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `TARGET-HARDWARE` / `WHEN-RESPONDING-TO-A-SUPPORTED-CHECKSUM-OPTION` / `RETURN-FILE-CHECKSUM-COMPUTED-BY-INDICATED-ALGORITHM` / `ENTIRE-FILE, INDICATED-CHECKSUM-ALGORITHM, CHECKSUM-VALUE` / `RETURNED-CHECKSUM-VALUE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“WHEN-RESPONDING-TO-A-SUPPORTED-CHECKSUM-OPTION”下必须对“ENTIRE-FILE、INDICATED-CHECKSUM-ALGORITHM、CHECKSUM-VALUE”执行“RETURN-FILE-CHECKSUM-COMPUTED-BY-INDICATED-ALGORITHM”；证据是“RETURNED-CHECKSUM-VALUE-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00051` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-030-15DD7CD59677`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `TARGET-HARDWARE` / `WHEN-CHECKSUM-OPTION-IS-GIVEN-AND-ALGORITHM-IS-SUPPORTED` / `ACKNOWLEDGE-CHECKSUM-OPTION-IF-ALGORITHM-SUPPORTED` / `CHECKSUM-OPTION, SPECIFIED-CHECKSUM-ALGORITHM` / `CHECKSUM-OPTION-ACKNOWLEDGEMENT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“WHEN-CHECKSUM-OPTION-IS-GIVEN-AND-ALGORITHM-IS-SUPPORTED”下必须对“CHECKSUM-OPTION、SPECIFIED-CHECKSUM-ALGORITHM”执行“ACKNOWLEDGE-CHECKSUM-OPTION-IF-ALGORITHM-SUPPORTED”；证据是“CHECKSUM-OPTION-ACKNOWLEDGEMENT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00052` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-030-15DD7CD59677`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `DATA-LOADER` / `AFTER-CHECKSUM-OPTION-ACKNOWLEDGEMENT-AND-FILE-TRANSFER-COMPLETION` / `CALCULATE-AND-VALIDATE-RECEIVED-FILE-CHECKSUM` / `ENTIRE-RECEIVED-DATA-FILE, ACKNOWLEDGED-CHECKSUM-ALGORITHM` / `POST-TRANSFER-INTEGRITY-VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“AFTER-CHECKSUM-OPTION-ACKNOWLEDGEMENT-AND-FILE-TRANSFER-COMPLETION”下必须对“ENTIRE-RECEIVED-DATA-FILE、ACKNOWLEDGED-CHECKSUM-ALGORITHM”执行“CALCULATE-AND-VALIDATE-RECEIVED-FILE-CHECKSUM”；证据是“POST-TRANSFER-INTEGRITY-VALIDATION-RESULT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00053` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-031-CDCCDED52C40`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `DATA-LOADER` / `WHEN-CHECKSUM-VALIDATION-FAILS` / `DO-NOT-FAIL-TFTP-TRANSFER-ON-CHECKSUM-VALIDATION-FAILURE` / `TFTP-TRANSFER, CHECKSUM-VALIDATION-FAILURE` / `ABSENCE-OF-CHECKSUM-CAUSED-TFTP-FAILURE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“WHEN-CHECKSUM-VALIDATION-FAILS”下必须对“TFTP-TRANSFER、CHECKSUM-VALIDATION-FAILURE”执行“DO-NOT-FAIL-TFTP-TRANSFER-ON-CHECKSUM-VALIDATION-FAILURE”；证据是“ABSENCE-OF-CHECKSUM-CAUSED-TFTP-FAILURE-OBSERVABLE”。 | — | DEP-RFC-1350, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00054` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-032-C495B27D5E7B`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `DATA-LOADER` / `UNCONDITIONAL` / `VALIDATE` / `CRC, OPERATION` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“UNCONDITIONAL”下必须对“CRC／校验值、协议操作”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00055` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-033-54C31853DBBA`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `DATA-LOADER` / `UNCONDITIONAL` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“UNCONDITIONAL”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00056` | `SU-ARINC-615A-3-5-3-2-3-8-5-P043-PROSE-SENTENCE-034-6BD83C2FA204`<br>`ARINC-615A-3 5.3.2.3.8.5 p.31` | `DATA-LOADER` / `UNCONDITIONAL` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“UNCONDITIONAL”下可以对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00057` | `SU-ARINC-615A-3-5-3-2-3-8-6-P044-PROSE-SENTENCE-005-F74AC5B7AE1C`<br>`ARINC-615A-3 5.3.2.3.8.6 p.32` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `FAIL` / `OPERATION, TARGET-HARDWARE-ID` / `FAILURE-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下可以对“协议操作、TARGET-HARDWARE-ID”执行“判定失败”；证据是“失败结果可被观察”。 | — | — |
| `CRS-M1-00058` | `SU-ARINC-615A-3-5-3-2-3-8-6-P044-PROSE-SENTENCE-006-1813D605F404`<br>`ARINC-615A-3 5.3.2.3.8.6 p.32` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ASSIGN` / `NETWORK-INTERFACE` / `ASSIGN-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“网络接口”执行“分配或管理”；证据是“ASSIGN-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00059` | `SU-ARINC-615A-3-5-3-2-3-9-P044-PROSE-SENTENCE-001-04EEB77FBE9B`<br>`ARINC-615A-3 5.3.2.3.9 p.32` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `COMPLY` / `TFTP-BLOCK-NUMBER` / `COMPLY-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“TFTP 块号”执行“符合”；证据是“COMPLY-RESULT-OBSERVABLE”。 | — | DEP-RFC-1350 |
| `CRS-M1-00060` | `SU-ARINC-615A-3-5-3-2-3-9-P044-PROSE-SENTENCE-003-17BB6DF8AFB6`<br>`ARINC-615A-3 5.3.2.3.9 p.32` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `ON-TFTP-BLOCK-NUMBER-OVERFLOW` / `SEND` / `TFTP-BLOCK-NUMBER` / `MESSAGE-OR-FILE-DIRECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“TFTP 块号溢出时”下必须对“TFTP 块号”执行“发送”；证据是“消息或文件及其方向可被观察”。 | — | — |
| `CRS-M1-00061` | `SU-ARINC-615A-3-5-4-1-P045-PROSE-SENTENCE-008-B50B97990D87`<br>`ARINC-615A-3 5.4.1 p.33` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `IMPLEMENT` / `NETWORK-INTERFACE, TARGET-HARDWARE-ID` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下可以对“网络接口、TARGET-HARDWARE-ID”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00062` | `SU-ARINC-615A-3-5-4-1-P046-PROSE-SENTENCE-018-975659D827AD`<br>`ARINC-615A-3 5.4.1 p.34` | `DATA-LOADING-SYSTEM` / `FOR-OPERATIONS-ON-THE-SAME-TARGET-HARDWARE` / `ALLOW-ANY-ORDER-WHILE-SERIALIZING-PER-TARGET` / `OPERATIONS-PER-TARGET-HARDWARE` / `PER-TARGET-OPERATION-ORDER-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“DATA-LOADING-SYSTEM”在“FOR-OPERATIONS-ON-THE-SAME-TARGET-HARDWARE”下必须对“OPERATIONS-PER-TARGET-HARDWARE”执行“ALLOW-ANY-ORDER-WHILE-SERIALIZING-PER-TARGET”；证据是“PER-TARGET-OPERATION-ORDER-OBSERVABLE”。 | — | — |
| `CRS-M1-00063` | `SU-ARINC-615A-3-5-4-1-P046-PROSE-SENTENCE-019-E420E9678873`<br>`ARINC-615A-3 5.4.1 p.34` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ABORT` / `OPERATION` / `ABORT-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下可以对“协议操作”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00064` | `SU-ARINC-615A-3-5-4-1-P046-PROSE-SENTENCE-020-EB49BE04DB5C`<br>`ARINC-615A-3 5.4.1 p.34` | `DATA-LOADER` / `UNCONDITIONAL` / `IMPLEMENT` / `OPERATION` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“UNCONDITIONAL”下必须对“协议操作”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00065` | `SU-ARINC-615A-3-5-4-1-P046-PROSE-SENTENCE-021-B970B2F9D719`<br>`ARINC-615A-3 5.4.1 p.34` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `TRANSFER` / `OPERATION, FIND-SERVICE, TARGET-HARDWARE-ID` / `TRANSFER-OUTCOME-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“协议操作、FIND-SERVICE、TARGET-HARDWARE-ID”执行“传输”；证据是“传输结果可被观察”。 | — | — |
| `CRS-M1-00066` | `SU-ARINC-615A-3-5-4-1-P046-PROSE-SENTENCE-021-B970B2F9D719`<br>`ARINC-615A-3 5.4.1 p.34` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `TRANSFER` / `OPERATION` / `TRANSFER-OUTCOME-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“协议操作”执行“传输”；证据是“传输结果可被观察”。 | — | — |
| `CRS-M1-00067` | `SU-ARINC-615A-3-5-4-1-P046-PROSE-SENTENCE-022-FC38D80A0B56`<br>`ARINC-615A-3 5.4.1 p.34` | `DATA-LOADER` / `UNCONDITIONAL` / `LOCATE` / `OPERATION, FIND-SERVICE` / `LOCATE-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“UNCONDITIONAL”下可以对“协议操作、FIND-SERVICE”执行“定位”；证据是“LOCATE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00068` | `SU-ARINC-615A-3-5-4-1-P046-PROSE-SENTENCE-023-ED7AFF26DD5C`<br>`ARINC-615A-3 5.4.1 p.34` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `TRANSFER` / `OPERATION, NETWORK-INTERFACE` / `TRANSFER-OUTCOME-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“协议操作、网络接口”执行“传输”；证据是“传输结果可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00069` | `SU-ARINC-615A-3-5-4-1-P046-PROSE-SENTENCE-024-6B0F5F41DA4C`<br>`ARINC-615A-3 5.4.1 p.34` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ENCODE` / `OPERATION, NETWORK-INTERFACE` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“协议操作、网络接口”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00070` | `SU-ARINC-615A-3-5-4-1-P047-PROSE-SENTENCE-025-9C4E3C2DEF6F`<br>`ARINC-615A-3 5.4.1 p.35` | `TARGET-HARDWARE` / `WHEN-OPTIONAL-CAPABILITY-IMPLEMENTED` / `IMPLEMENT` / `OPERATION, NETWORK-INTERFACE, TARGET-HARDWARE-ID` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“实现可选能力时”下必须对“协议操作、网络接口、TARGET-HARDWARE-ID”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00071` | `SU-ARINC-615A-3-5-4-2-P047-PROSE-SENTENCE-002-ECE0CBAF4A74`<br>`ARINC-615A-3 5.4.2 p.35` | `DATA-LOADER` / `UNCONDITIONAL` / `IMPLEMENT` / `OPERATION` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“UNCONDITIONAL”下必须对“协议操作”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00072` | `SU-ARINC-615A-3-5-4-2-P047-PROSE-SENTENCE-003-78F447EDB430`<br>`ARINC-615A-3 5.4.2 p.35` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `IMPLEMENT` / `OPERATION, TARGET-HARDWARE-ID` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“协议操作、TARGET-HARDWARE-ID”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00073` | `SU-ARINC-615A-3-5-4-2-P047-PROSE-SENTENCE-021-2733DF1A1970`<br>`ARINC-615A-3 5.4.2 p.35` | `DATA-LOADER` / `UNCONDITIONAL` / `WAIT` / `CURRENT-STATUS` / `WAIT-BEHAVIOR-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“UNCONDITIONAL”下必须对“CURRENT-STATUS”执行“等待”；证据是“等待行为可被观察”。 | — | — |
| `CRS-M1-00074` | `SU-ARINC-615A-3-5-4-2-P047-PROSE-SENTENCE-023-DD0255D27FB0`<br>`ARINC-615A-3 5.4.2 p.35` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `VALIDATE` / `TFTP-OPTION` / `VALIDATION-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下可以对“TFTP 选项”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00075` | `SU-ARINC-615A-3-5-4-2-P047-PROSE-SENTENCE-024-12B60035E133`<br>`ARINC-615A-3 5.4.2 p.35` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `IMPLEMENT` / `TFTP-OPTION` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下可以对“TFTP 选项”执行“提供能力”；证据是“能力可用性可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00076` | `SU-ARINC-615A-3-5-4-2-P047-PROSE-SENTENCE-025-3CF28DC21423`<br>`ARINC-615A-3 5.4.2 p.35` | `DATA-LOADER` / `UNCONDITIONAL` / `VALIDATE` / `CRC, NETWORK-INTERFACE` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“UNCONDITIONAL”下必须对“CRC／校验值、网络接口”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00077` | `SU-ARINC-615A-3-5-4-3-P047-PROSE-SENTENCE-002-ECE0CBAF4A74`<br>`ARINC-615A-3 5.4.3 p.35` | `DATA-LOADER` / `UNCONDITIONAL` / `IMPLEMENT` / `OPERATION` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“数据加载器”在“UNCONDITIONAL”下必须对“协议操作”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00078` | `SU-ARINC-615A-3-5-4-3-P047-PROSE-SENTENCE-003-78F447EDB430`<br>`ARINC-615A-3 5.4.3 p.35` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `IMPLEMENT` / `OPERATION, TARGET-HARDWARE-ID` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“协议操作、TARGET-HARDWARE-ID”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00079` | `SU-ARINC-615A-3-5-4-3-P048-PROSE-SENTENCE-015-A6329164790D`<br>`ARINC-615A-3 5.4.3 p.36` | `TARGET-HARDWARE` / `WHEN-LOAD-LIST-ITEM-REJECTED` / `REJECT` / `LOAD-LIST, TARGET-HARDWARE-ID` / `REJECTION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“目标硬件”在“加载清单中任一项被拒绝时”下必须对“LOAD-LIST、TARGET-HARDWARE-ID”执行“拒绝”；证据是“拒绝结果可被观察”。 | — | — |
| `CRS-M1-00080` | `SU-ARINC-615A-3-5-4-3-P048-PROSE-SENTENCE-018-3233B1CC77D5`<br>`ARINC-615A-3 5.4.3 p.36` | `DATA-LOADER` / `UNCONDITIONAL` / `DISPLAY` / `CURRENT-STATUS` / `USER-INDICATION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“数据加载器”在“UNCONDITIONAL”下必须对“CURRENT-STATUS”执行“显示或通知”；证据是“用户提示可被观察”。 | — | — |
| `CRS-M1-00081` | `SU-ARINC-615A-3-5-4-3-P048-PROSE-SENTENCE-024-D550F67EB586`<br>`ARINC-615A-3 5.4.3 p.36` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `VALIDATE` / `TFTP-OPTION, NETWORK-INTERFACE` / `VALIDATION-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | 参与者“目标硬件”在“UNCONDITIONAL”下可以对“TFTP 选项、网络接口”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00082` | `SU-ARINC-615A-3-5-4-3-P048-PROSE-SENTENCE-026-F38D018C4499`<br>`ARINC-615A-3 5.4.3 p.36` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00083` | `SU-ARINC-615A-3-5-4-3-P048-PROSE-SENTENCE-027-E777A6D3DAC7`<br>`ARINC-615A-3 5.4.3 p.36` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `VALIDATE` / `TFTP-OPTION` / `VALIDATION-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | 参与者“目标硬件”在“UNCONDITIONAL”下可以对“TFTP 选项”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00084` | `SU-ARINC-615A-3-5-4-3-1-P048-PROSE-SENTENCE-004-AF732D243056`<br>`ARINC-615A-3 5.4.3.1 p.36` | `TARGET-HARDWARE` / `WHEN-EVALUATING-A-NEW-LOAD` / `RETAIN-CURRENT-DATA-FILE-PART-NUMBERS-FOR-NEW-LOAD-COMPARISON` / `CURRENT-INSTALLED-LOAD-PART-NUMBERS, NEW-LOAD-HEADER-PART-NUMBERS` / `RETAINED-PART-NUMBER-COMPARISON-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“目标硬件”在“WHEN-EVALUATING-A-NEW-LOAD”下必须对“CURRENT-INSTALLED-LOAD-PART-NUMBERS、NEW-LOAD-HEADER-PART-NUMBERS”执行“RETAIN-CURRENT-DATA-FILE-PART-NUMBERS-FOR-NEW-LOAD-COMPARISON”；证据是“RETAINED-PART-NUMBER-COMPARISON-OBSERVABLE”。 | — | — |
| `CRS-M1-00085` | `SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-007-F209ABE1376B`<br>`ARINC-615A-3 5.4.3.1 p.37` | `SOFTWARE-PACKAGE-PRODUCER` / `UNCONDITIONAL` / `VALIDATE` / `CRC, SOFTWARE-PART` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“软件包生成方”在“UNCONDITIONAL”下必须对“CRC／校验值、软件加载件”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-6655, DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00086` | `SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-008-CDA43D6568CC`<br>`ARINC-615A-3 5.4.3.1 p.37` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `VALIDATE` / `CRC, FILE-CONTENT, TARGET-HARDWARE-ID` / `VALIDATION-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | 参与者“目标硬件”在“UNCONDITIONAL”下可以对“CRC／校验值、FILE-CONTENT、TARGET-HARDWARE-ID”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00087` | `SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-010-F4624AC8DCB4`<br>`ARINC-615A-3 5.4.3.1 p.37` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENSURE-EQUALITY` / `LOAD-PART-NUMBER, CRC` / `ENSURE-EQUALITY-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“加载件号、CRC／校验值”执行“确保取值相等”；证据是“ENSURE-EQUALITY-RESULT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00088` | `SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-012-B2655A4BD5D6`<br>`ARINC-615A-3 5.4.3.1 p.37` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `FORMAT` / `FILE-CONTENT` / `ENCODED-FORMAT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“FILE-CONTENT”执行“按规定格式化”；证据是“编码格式可被观察”。 | — | — |
| `CRS-M1-00089` | `SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-015-1FD87B87894F`<br>`ARINC-615A-3 5.4.3.1 p.37` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `SELECT` / `FILE-CONTENT` / `SELECT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“FILE-CONTENT”执行“选择”；证据是“SELECT-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00090` | `SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-017-D6D20C0AE6D8`<br>`ARINC-615A-3 5.4.3.1 p.37` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `COMPILE-AND-LINK` / `FILE-CONTENT` / `COMPILE-AND-LINK-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“FILE-CONTENT”执行“独立编译并链接”；证据是“COMPILE-AND-LINK-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00091` | `SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-018-7D1A5B42A8F9`<br>`ARINC-615A-3 5.4.3.1 p.37` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `DEFINE` / `FILE-CONTENT, PROGRAM-MEMORY-MAP` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“FILE-CONTENT、PROGRAM-MEMORY-MAP”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00092` | `SU-ARINC-615A-3-5-4-5-2-P053-PROSE-SENTENCE-008-6BD76320C0DE`<br>`ARINC-615A-3 5.4.5.2 p.41` | `DATA-LOADER` / `UNCONDITIONAL` / `ABORT` / `STATUS-FILE, TEXT-FIELD, OPERATION` / `ABORT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“UNCONDITIONAL”下必须对“状态文件、文本字段、协议操作”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00093` | `SU-ARINC-615A-3-6-2-8-1-P057-PROSE-SENTENCE-001-B9AF73779529`<br>`ARINC-615A-3 6.2.8.1 p.45` | `TARGET-HARDWARE` / `ON-WAIT-MESSAGE-RECEIPT` / `RETRY` / `TARGET-HARDWARE-ID, PROTOCOL-MESSAGE` / `RETRY-ATTEMPT-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“目标硬件”在“收到 WAIT 消息时”下必须对“TARGET-HARDWARE-ID、PROTOCOL-MESSAGE”执行“重试”；证据是“重试尝试可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00094` | `SU-ARINC-615A-3-6-3-1-P063-PROSE-SENTENCE-010-EF2C1FAB94E9`<br>`ARINC-615A-3 6.3.1 p.51` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `DEFINE` / `STATUS-FILE` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“状态文件”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | `SYMBOLIC-SOURCE-PARAMETER` / `DLP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-001-E20DEE6A28B4, SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-002-68A6807BC6D8 | — |
| `CRS-M1-00095` | `SU-ARINC-615A-3-6-3-1-P063-PROSE-SENTENCE-014-46E366631127`<br>`ARINC-615A-3 6.3.1 p.51` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ENCODE` / `STATUS-FILE, NETWORK-INTERFACE, PROTOCOL-ERROR` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“状态文件、网络接口、PROTOCOL-ERROR”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00096` | `SU-ARINC-615A-3-6-3-1-P063-PROSE-SENTENCE-015-FFB177F65B0A`<br>`ARINC-615A-3 6.3.1 p.51` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ABORT` / `ABORT-MESSAGE, STATUS-FILE, NETWORK-INTERFACE, TARGET-HARDWARE-ID` / `ABORT-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下可以对“中止消息、状态文件、网络接口、TARGET-HARDWARE-ID”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00097` | `SU-ARINC-615A-3-6-3-1-P063-PROSE-SENTENCE-018-33F16CA0556B`<br>`ARINC-615A-3 6.3.1 p.51` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `SEND` / `STATUS-FILE, TIMEOUT-EXPIRY, LCL-TRANSFER` / `MESSAGE-OR-FILE-DIRECTION-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下可以对“状态文件、TIMEOUT-EXPIRY、LCL-TRANSFER”执行“发送”；证据是“消息或文件及其方向可被观察”。 | `SYMBOLIC-SOURCE-PARAMETER` / `DLP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-001-E20DEE6A28B4, SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-002-68A6807BC6D8 | — |
| `CRS-M1-00098` | `SU-ARINC-615A-3-6-3-1-P063-PROSE-SENTENCE-020-D27F9DB819AB`<br>`ARINC-615A-3 6.3.1 p.51` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `SEND` / `STATUS-FILE, TARGET-HARDWARE-ID` / `MESSAGE-OR-FILE-DIRECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“状态文件、TARGET-HARDWARE-ID”执行“发送”；证据是“消息或文件及其方向可被观察”。 | `SYMBOLIC-SOURCE-PARAMETER` / `DLP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-001-E20DEE6A28B4, SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-002-68A6807BC6D8 | — |
| `CRS-M1-00099` | `SU-ARINC-615A-3-6-3-1-P064-PROSE-SENTENCE-031-D8862D88C46E`<br>`ARINC-615A-3 6.3.1 p.52` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `WAIT` / `EXCEPTION-TIMER, OPERATION, TARGET-HARDWARE-ID` / `WAIT-BEHAVIOR-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“异常计时器、协议操作、TARGET-HARDWARE-ID”执行“等待”；证据是“等待行为可被观察”。 | `MESSAGE-CARRIED-PARAMETER` / `MESSAGE-TIMER-VALUE` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-TABLE-6_4_3-1-R006 | — |
| `CRS-M1-00100` | `SU-ARINC-615A-3-6-3-1-P064-PROSE-SENTENCE-032-E812AC346D09`<br>`ARINC-615A-3 6.3.1 p.52` | `TARGET-HARDWARE-SUPPLIER` / `UNCONDITIONAL` / `WAIT` / `EXCEPTION-TIMER, TARGET-HARDWARE-ID` / `WAIT-BEHAVIOR-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件供应商”在“UNCONDITIONAL”下必须对“异常计时器、TARGET-HARDWARE-ID”执行“等待”；证据是“等待行为可被观察”。 | `MESSAGE-CARRIED-PARAMETER` / `MESSAGE-TIMER-VALUE` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-TABLE-6_4_3-1-R006 | — |
| `CRS-M1-00101` | `SU-ARINC-615A-3-6-3-1-P064-PROSE-SENTENCE-033-2765B9535D98`<br>`ARINC-615A-3 6.3.1 p.52` | `DATA-LOADER` / `AFTER-A-STATUS-FILE-DECLARES-AN-EXCEPTION-DELAY` / `RECEIVE-STATUS-BEFORE-DELAY-OR-ABORT-OPERATION` / `NEW-STATUS-FILE, EXCEPTION-DELAY, ACTIVE-OPERATION` / `STATUS-BEFORE-DEADLINE-OR-ABORT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“AFTER-A-STATUS-FILE-DECLARES-AN-EXCEPTION-DELAY”下必须对“NEW-STATUS-FILE、EXCEPTION-DELAY、ACTIVE-OPERATION”执行“RECEIVE-STATUS-BEFORE-DELAY-OR-ABORT-OPERATION”；证据是“STATUS-BEFORE-DEADLINE-OR-ABORT-OBSERVABLE”。 | `MESSAGE-CARRIED-PARAMETER` / `EXCEPTION-DELAY` / `STATUS-RECEIVED-BEFORE-EXCEPTION-DELAY-ELSE-OPERATION-ABORT` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-028-9597EE244FD7 | — |
| `CRS-M1-00102` | `SU-ARINC-615A-3-6-3-2-P067-PROSE-SENTENCE-020-43C35127F07F`<br>`ARINC-615A-3 6.3.2 p.55` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `DEFINE` / `STATUS-FILE` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“状态文件”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | `SYMBOLIC-SOURCE-PARAMETER` / `DLP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-001-E20DEE6A28B4, SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-002-68A6807BC6D8 | — |
| `CRS-M1-00103` | `SU-ARINC-615A-3-6-3-2-P067-PROSE-SENTENCE-022-9B7AA17CBAF6`<br>`ARINC-615A-3 6.3.2 p.55` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ENCODE` / `STATUS-FILE, NETWORK-INTERFACE, PROTOCOL-ERROR` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“状态文件、网络接口、PROTOCOL-ERROR”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00104` | `SU-ARINC-615A-3-6-3-2-P067-PROSE-SENTENCE-023-AEFFB70E9596`<br>`ARINC-615A-3 6.3.2 p.55` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ABORT` / `ABORT-MESSAGE, STATUS-FILE, NETWORK-INTERFACE, TARGET-HARDWARE-ID` / `ABORT-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | 参与者“目标硬件”在“UNCONDITIONAL”下可以对“中止消息、状态文件、网络接口、TARGET-HARDWARE-ID”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00105` | `SU-ARINC-615A-3-6-3-2-P067-PROSE-SENTENCE-026-3B69FEC8B73B`<br>`ARINC-615A-3 6.3.2 p.55` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `TRANSFER` / `UPLOAD-THREAD` / `TRANSFER-OUTCOME-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | 参与者“目标硬件”在“UNCONDITIONAL”下可以对“UPLOAD-THREAD”执行“传输”；证据是“传输结果可被观察”。 | — | — |
| `CRS-M1-00106` | `SU-ARINC-615A-3-6-3-2-P068-PROSE-SENTENCE-038-D8862D88C46E`<br>`ARINC-615A-3 6.3.2 p.56` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `WAIT` / `EXCEPTION-TIMER, OPERATION, TARGET-HARDWARE-ID` / `WAIT-BEHAVIOR-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“异常计时器、协议操作、TARGET-HARDWARE-ID”执行“等待”；证据是“等待行为可被观察”。 | `MESSAGE-CARRIED-PARAMETER` / `MESSAGE-TIMER-VALUE` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-TABLE-6_4_3-1-R006 | — |
| `CRS-M1-00107` | `SU-ARINC-615A-3-6-3-2-P068-PROSE-SENTENCE-039-E812AC346D09`<br>`ARINC-615A-3 6.3.2 p.56` | `TARGET-HARDWARE-SUPPLIER` / `UNCONDITIONAL` / `WAIT` / `EXCEPTION-TIMER, TARGET-HARDWARE-ID` / `WAIT-BEHAVIOR-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“目标硬件供应商”在“UNCONDITIONAL”下必须对“异常计时器、TARGET-HARDWARE-ID”执行“等待”；证据是“等待行为可被观察”。 | `MESSAGE-CARRIED-PARAMETER` / `MESSAGE-TIMER-VALUE` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-TABLE-6_4_3-1-R006 | — |
| `CRS-M1-00108` | `SU-ARINC-615A-3-6-3-2-P068-PROSE-SENTENCE-040-2765B9535D98`<br>`ARINC-615A-3 6.3.2 p.56` | `DATA-LOADER` / `AFTER-A-STATUS-FILE-DECLARES-AN-EXCEPTION-DELAY` / `RECEIVE-STATUS-BEFORE-DELAY-OR-ABORT-OPERATION` / `NEW-STATUS-FILE, EXCEPTION-DELAY, ACTIVE-OPERATION` / `STATUS-BEFORE-DEADLINE-OR-ABORT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“数据加载器”在“AFTER-A-STATUS-FILE-DECLARES-AN-EXCEPTION-DELAY”下必须对“NEW-STATUS-FILE、EXCEPTION-DELAY、ACTIVE-OPERATION”执行“RECEIVE-STATUS-BEFORE-DELAY-OR-ABORT-OPERATION”；证据是“STATUS-BEFORE-DEADLINE-OR-ABORT-OBSERVABLE”。 | `MESSAGE-CARRIED-PARAMETER` / `EXCEPTION-DELAY` / `STATUS-RECEIVED-BEFORE-EXCEPTION-DELAY-ELSE-OPERATION-ABORT` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-028-9597EE244FD7 | — |
| `CRS-M1-00109` | `SU-ARINC-615A-3-6-3-2-P068-PROSE-SENTENCE-042-4C1D759A6B9A`<br>`ARINC-615A-3 6.3.2 p.56` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `SEND` / `STATUS-FILE, DATA-FILE, CRC` / `MESSAGE-OR-FILE-DIRECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“状态文件、数据文件、CRC／校验值”执行“发送”；证据是“消息或文件及其方向可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00110` | `SU-ARINC-615A-3-6-3-5-P076-PROSE-SENTENCE-009-BF2F613AC35B`<br>`ARINC-615A-3 6.3.5 p.64` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ABORT` / `STATUS-FILE, TARGET-HARDWARE-ID` / `ABORT-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下可以对“状态文件、TARGET-HARDWARE-ID”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00111` | `SU-ARINC-615A-3-6-3-5-P076-PROSE-SENTENCE-011-5B38B1E3DBEF`<br>`ARINC-615A-3 6.3.5 p.64` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ABORT` / `STATUS-FILE, OPERATION, TARGET-HARDWARE-ID` / `ABORT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“状态文件、协议操作、TARGET-HARDWARE-ID”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00112` | `SU-ARINC-615A-3-6-3-5-P076-PROSE-SENTENCE-012-EED68957A0BC`<br>`ARINC-615A-3 6.3.5 p.64` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ABORT` / `ABORT-MESSAGE, OPERATION, TARGET-HARDWARE-ID` / `ABORT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“中止消息、协议操作、TARGET-HARDWARE-ID”执行“中止”；证据是“中止结果可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00113` | `SU-ARINC-615A-3-6-3-5-P076-PROSE-SENTENCE-013-DEDC03B64B0A`<br>`ARINC-615A-3 6.3.5 p.64` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `ABORT` / `STATUS-FILE, ERROR-MESSAGE, TARGET-HARDWARE-ID` / `ABORT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“状态文件、错误消息、TARGET-HARDWARE-ID”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00114` | `SU-ARINC-615A-3-6-3-5-P076-PROSE-SENTENCE-015-DCA535962C3D`<br>`ARINC-615A-3 6.3.5 p.64` | `DATA-LOADER` / `UNCONDITIONAL` / `ABORT` / `ABORT-MESSAGE, OPERATION` / `ABORT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“UNCONDITIONAL”下必须对“中止消息、协议操作”执行“中止”；证据是“中止结果可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00115` | `SU-ARINC-615A-3-6-4-P077-PROSE-SENTENCE-005-1B24BCFF8198`<br>`ARINC-615A-3 6.4 p.65` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `SEND` / `PROTOCOL-VERSION, OPERATION, NETWORK-INTERFACE, TARGET-HARDWARE-ID` / `MESSAGE-OR-FILE-DIRECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“协议版本、协议操作、网络接口、TARGET-HARDWARE-ID”执行“发送”；证据是“消息或文件及其方向可被观察”。 | — | — |
| `CRS-M1-00116` | `SU-ARINC-615A-3-6-4-P077-PROSE-SENTENCE-007-20EF70E6EF8B`<br>`ARINC-615A-3 6.4 p.65` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `IMPLEMENT` / `PROTOCOL-VERSION, OPERATION, TARGET-HARDWARE-ID` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“协议版本、协议操作、TARGET-HARDWARE-ID”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00117` | `SU-ARINC-615A-3-6-4-P077-PROSE-SENTENCE-010-5F21110D7E4B`<br>`ARINC-615A-3 6.4 p.65` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `DEFINE` / `PROTOCOL-VERSION, NETWORK-INTERFACE` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“UNCONDITIONAL”下必须对“协议版本、网络接口”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00118` | `SU-ARINC-615A-3-6-4-P077-PROSE-SENTENCE-011-5625CA7DF2D3`<br>`ARINC-615A-3 6.4 p.65` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPTIONAL-CAPABILITY-IMPLEMENTED` / `IMPLEMENT` / `PROTOCOL-VERSION, NETWORK-INTERFACE` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“实现可选能力时”下必须对“协议版本、网络接口”执行“提供能力”；证据是“能力可用性可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00119` | `SU-ARINC-615A-3-6-4-P077-PROSE-SENTENCE-013-2FCCE7C4573B`<br>`ARINC-615A-3 6.4 p.65` | `DATA-LOADER` / `WHEN-OPTIONAL-CAPABILITY-IMPLEMENTED` / `ABORT` / `PROTOCOL-VERSION` / `ABORT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“实现可选能力时”下必须对“协议版本”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00120` | `SU-ARINC-615A-3-6-4-P077-PROSE-SENTENCE-014-569F14A5E296`<br>`ARINC-615A-3 6.4 p.65` | `DATA-LOADER` / `WHEN-PROTOCOL-VERSIONS-DIFFER` / `ABORT` / `ABORT-MESSAGE, STATUS-FILE, PROTOCOL-VERSION, OPERATION` / `ABORT-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“协议版本不兼容时”下必须对“中止消息、状态文件、协议版本、协议操作”执行“中止”；证据是“中止结果可被观察”。 | — | — |
| `CRS-M1-00121` | `SU-ARINC-615A-3-6-4-P077-PROSE-SENTENCE-015-425EEC39D73C`<br>`ARINC-615A-3 6.4 p.65` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `PROTOCOL-VERSION` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“UNCONDITIONAL”下必须对“协议版本”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00122` | `SU-ARINC-615A-3-6-4-P077-PROSE-SENTENCE-017-280B7BBBB75A`<br>`ARINC-615A-3 6.4 p.65` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00123` | `SU-ARINC-615A-3-6-4-P078-PROSE-SENTENCE-019-70F6AB842538`<br>`ARINC-615A-3 6.4 p.66` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“UNCONDITIONAL”下可以对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00124` | `SU-ARINC-615A-3-6-4-1-P080-PROSE-SENTENCE-023-B30093B748E5`<br>`ARINC-615A-3 6.4.1 p.68` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ALLOW-PRINTABLE` / `TEXT-FIELD` / `ALLOW-PRINTABLE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“仅允许可打印字符”；证据是“ALLOW-PRINTABLE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00125` | `SU-ARINC-615A-3-6-4-1-P080-PROSE-SENTENCE-023-B30093B748E5`<br>`ARINC-615A-3 6.4.1 p.68` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `EXCLUDE-CONTROL-CHARACTERS` / `TEXT-FIELD, CONTROL-CHARACTERS` / `CONTROL-CHARACTER-ABSENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、CONTROL-CHARACTERS”执行“EXCLUDE-CONTROL-CHARACTERS”；证据是“CONTROL-CHARACTER-ABSENCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00126` | `SU-ARINC-615A-3-6-4-1-P080-PROSE-SENTENCE-023-B30093B748E5`<br>`ARINC-615A-3 6.4.1 p.68` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `LIMIT-TEXT-LENGTH-TO-255-CHARACTERS` / `TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS` / `TEXT-LENGTH-BOUND-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、MAXIMUM-255-CHARACTERS、MAXIMUM-2040-BITS”执行“LIMIT-TEXT-LENGTH-TO-255-CHARACTERS”；证据是“TEXT-LENGTH-BOUND-OBSERVABLE”。 | — | — |
| `CRS-M1-00127` | `SU-ARINC-615A-3-6-4-1-P080-PROSE-SENTENCE-024-1532165AA3AE`<br>`ARINC-615A-3 6.4.1 p.68` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00128` | `SU-ARINC-615A-3-6-4-2-P081-PROSE-SENTENCE-018-7650772794FC`<br>`ARINC-615A-3 6.4.2 p.69` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00129` | `SU-ARINC-615A-3-6-4-2-P081-PROSE-SENTENCE-023-B016CF154BFD`<br>`ARINC-615A-3 6.4.2 p.69` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00130` | `SU-ARINC-615A-3-6-4-2-P081-PROSE-SENTENCE-030-B016CF154BFD`<br>`ARINC-615A-3 6.4.2 p.69` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00131` | `SU-ARINC-615A-3-6-4-2-P082-PROSE-SENTENCE-042-0D59A327A7CC`<br>`ARINC-615A-3 6.4.2 p.70` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ALLOW-PRINTABLE` / `TEXT-FIELD` / `ALLOW-PRINTABLE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“仅允许可打印字符”；证据是“ALLOW-PRINTABLE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00132` | `SU-ARINC-615A-3-6-4-2-P082-PROSE-SENTENCE-042-0D59A327A7CC`<br>`ARINC-615A-3 6.4.2 p.70` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `EXCLUDE-CONTROL-CHARACTERS` / `TEXT-FIELD, CONTROL-CHARACTERS` / `CONTROL-CHARACTER-ABSENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、CONTROL-CHARACTERS”执行“EXCLUDE-CONTROL-CHARACTERS”；证据是“CONTROL-CHARACTER-ABSENCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00133` | `SU-ARINC-615A-3-6-4-2-P082-PROSE-SENTENCE-042-0D59A327A7CC`<br>`ARINC-615A-3 6.4.2 p.70` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `LIMIT-TEXT-LENGTH-TO-255-CHARACTERS` / `TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS` / `TEXT-LENGTH-BOUND-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、MAXIMUM-255-CHARACTERS、MAXIMUM-2040-BITS”执行“LIMIT-TEXT-LENGTH-TO-255-CHARACTERS”；证据是“TEXT-LENGTH-BOUND-OBSERVABLE”。 | — | — |
| `CRS-M1-00134` | `SU-ARINC-615A-3-6-4-2-P082-PROSE-SENTENCE-043-1532165AA3AE`<br>`ARINC-615A-3 6.4.2 p.70` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00135` | `SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-029-C2788AA6D18A`<br>`ARINC-615A-3 6.4.3 p.72` | `PROTOCOL-FILE-PRODUCER` / `WHEN-STATUS-CODE-IS-0002-OR-0004` / `ENCODE` / `STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“状态码为 0x0002 或 0x0004 时”下必须对“STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00136` | `SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-034-65EBA86ACA77`<br>`ARINC-615A-3 6.4.3 p.72` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `PROVIDE` / `ESTIMATED-TIME, OPERATION` / `PROVIDE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“预计时间、协议操作”执行“提供”；证据是“PROVIDE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00137` | `SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-037-98AB79F99A7B`<br>`ARINC-615A-3 6.4.3 p.72` | `TARGET-HARDWARE` / `WHEN-TIMER-VALUE-IS-NOT-PROVIDED` / `ENCODE` / `ESTIMATED-TIME, TARGET-HARDWARE-ID` / `ENCODED-FIELD-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“目标未提供计时值时”下必须对“预计时间、TARGET-HARDWARE-ID”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00138` | `SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-043-83077CACF0DC`<br>`ARINC-615A-3 6.4.3 p.72` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“UNCONDITIONAL”下可以对“STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00139` | `SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-045-1B483243E195`<br>`ARINC-615A-3 6.4.3 p.72` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ALLOW-PRINTABLE` / `TEXT-FIELD` / `ALLOW-PRINTABLE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“仅允许可打印字符”；证据是“ALLOW-PRINTABLE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00140` | `SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-045-1B483243E195`<br>`ARINC-615A-3 6.4.3 p.72` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `EXCLUDE-CONTROL-CHARACTERS` / `TEXT-FIELD, CONTROL-CHARACTERS` / `CONTROL-CHARACTER-ABSENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、CONTROL-CHARACTERS”执行“EXCLUDE-CONTROL-CHARACTERS”；证据是“CONTROL-CHARACTER-ABSENCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00141` | `SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-045-1B483243E195`<br>`ARINC-615A-3 6.4.3 p.72` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `LIMIT-TEXT-LENGTH-TO-255-CHARACTERS` / `TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS` / `TEXT-LENGTH-BOUND-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、MAXIMUM-255-CHARACTERS、MAXIMUM-2040-BITS”执行“LIMIT-TEXT-LENGTH-TO-255-CHARACTERS”；证据是“TEXT-LENGTH-BOUND-OBSERVABLE”。 | — | — |
| `CRS-M1-00142` | `SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-046-1532165AA3AE`<br>`ARINC-615A-3 6.4.3 p.72` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00143` | `SU-ARINC-615A-3-6-4-4-P085-PROSE-SENTENCE-013-D5E44774D202`<br>`ARINC-615A-3 6.4.4 p.73` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `HEADER-FILE, LUR` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“协议文件生成方”在“UNCONDITIONAL”下必须对“头文件、LUR”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00144` | `SU-ARINC-615A-3-6-4-4-P085-PROSE-SENTENCE-018-1532165AA3AE`<br>`ARINC-615A-3 6.4.4 p.73` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00145` | `SU-ARINC-615A-3-6-4-4-P085-PROSE-SENTENCE-023-53AAFA003A8B`<br>`ARINC-615A-3 6.4.4 p.73` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ALLOW-PRINTABLE` / `TEXT-FIELD` / `ALLOW-PRINTABLE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“仅允许可打印字符”；证据是“ALLOW-PRINTABLE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00146` | `SU-ARINC-615A-3-6-4-4-P085-PROSE-SENTENCE-023-53AAFA003A8B`<br>`ARINC-615A-3 6.4.4 p.73` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `EXCLUDE-CONTROL-CHARACTERS` / `TEXT-FIELD, CONTROL-CHARACTERS` / `CONTROL-CHARACTER-ABSENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、CONTROL-CHARACTERS”执行“EXCLUDE-CONTROL-CHARACTERS”；证据是“CONTROL-CHARACTER-ABSENCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00147` | `SU-ARINC-615A-3-6-4-4-P085-PROSE-SENTENCE-023-53AAFA003A8B`<br>`ARINC-615A-3 6.4.4 p.73` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `LIMIT-TEXT-LENGTH-TO-255-CHARACTERS` / `TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS` / `TEXT-LENGTH-BOUND-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、MAXIMUM-255-CHARACTERS、MAXIMUM-2040-BITS”执行“LIMIT-TEXT-LENGTH-TO-255-CHARACTERS”；证据是“TEXT-LENGTH-BOUND-OBSERVABLE”。 | — | — |
| `CRS-M1-00148` | `SU-ARINC-615A-3-6-4-4-P085-PROSE-SENTENCE-024-1532165AA3AE`<br>`ARINC-615A-3 6.4.4 p.73` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00149` | `SU-ARINC-615A-3-6-4-5-P087-PROSE-SENTENCE-028-44AE34DB0ED5`<br>`ARINC-615A-3 6.4.5 p.75` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | 参与者“协议文件生成方”在“UNCONDITIONAL”下可以对“STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00150` | `SU-ARINC-615A-3-6-4-5-P087-PROSE-SENTENCE-030-1B483243E195`<br>`ARINC-615A-3 6.4.5 p.75` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ALLOW-PRINTABLE` / `TEXT-FIELD` / `ALLOW-PRINTABLE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“仅允许可打印字符”；证据是“ALLOW-PRINTABLE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00151` | `SU-ARINC-615A-3-6-4-5-P087-PROSE-SENTENCE-030-1B483243E195`<br>`ARINC-615A-3 6.4.5 p.75` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `EXCLUDE-CONTROL-CHARACTERS` / `TEXT-FIELD, CONTROL-CHARACTERS` / `CONTROL-CHARACTER-ABSENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、CONTROL-CHARACTERS”执行“EXCLUDE-CONTROL-CHARACTERS”；证据是“CONTROL-CHARACTER-ABSENCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00152` | `SU-ARINC-615A-3-6-4-5-P087-PROSE-SENTENCE-030-1B483243E195`<br>`ARINC-615A-3 6.4.5 p.75` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `LIMIT-TEXT-LENGTH-TO-255-CHARACTERS` / `TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS` / `TEXT-LENGTH-BOUND-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、MAXIMUM-255-CHARACTERS、MAXIMUM-2040-BITS”执行“LIMIT-TEXT-LENGTH-TO-255-CHARACTERS”；证据是“TEXT-LENGTH-BOUND-OBSERVABLE”。 | — | — |
| `CRS-M1-00153` | `SU-ARINC-615A-3-6-4-5-P087-PROSE-SENTENCE-031-1532165AA3AE`<br>`ARINC-615A-3 6.4.5 p.75` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00154` | `SU-ARINC-615A-3-6-4-5-P088-PROSE-SENTENCE-040-B5C9724D1870`<br>`ARINC-615A-3 6.4.5 p.76` | `PROTOCOL-FILE-PRODUCER` / `WHEN-STATUS-CODE-IS-0002-OR-0004` / `ENCODE` / `STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“协议文件生成方”在“状态码为 0x0002 或 0x0004 时”下必须对“STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00155` | `SU-ARINC-615A-3-6-4-5-P088-PROSE-SENTENCE-045-19508B8A4FBD`<br>`ARINC-615A-3 6.4.5 p.76` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `PROVIDE` / `ESTIMATED-TIME, OPERATION, TARGET-HARDWARE-ID` / `PROVIDE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“预计时间、协议操作、TARGET-HARDWARE-ID”执行“提供”；证据是“PROVIDE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00156` | `SU-ARINC-615A-3-6-4-5-P088-PROSE-SENTENCE-048-394FB8F92672`<br>`ARINC-615A-3 6.4.5 p.76` | `TARGET-HARDWARE` / `WHEN-TIMER-VALUE-IS-NOT-PROVIDED` / `ENCODE` / `ESTIMATED-TIME, TARGET-HARDWARE-ID` / `ENCODED-FIELD-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“目标硬件”在“目标未提供计时值时”下必须对“预计时间、TARGET-HARDWARE-ID”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00157` | `SU-ARINC-615A-3-6-4-5-P088-PROSE-SENTENCE-054-628FD5E1362E`<br>`ARINC-615A-3 6.4.5 p.76` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `HEADER-FILE` / `ENCODED-FIELD-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“协议文件生成方”在“UNCONDITIONAL”下必须对“头文件”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00158` | `SU-ARINC-615A-3-6-4-5-P088-PROSE-SENTENCE-059-1532165AA3AE`<br>`ARINC-615A-3 6.4.5 p.76` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00159` | `SU-ARINC-615A-3-6-4-5-P089-PROSE-SENTENCE-064-1532165AA3AE`<br>`ARINC-615A-3 6.4.5 p.77` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00160` | `SU-ARINC-615A-3-6-4-5-P090-PROSE-SENTENCE-089-19FE3D2863DD`<br>`ARINC-615A-3 6.4.5 p.78` | `PROTOCOL-FILE-PRODUCER` / `UNCONDITIONAL` / `ENCODE` / `STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-BASE` | 参与者“协议文件生成方”在“UNCONDITIONAL”下可以对“STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00161` | `SU-ARINC-615A-3-6-4-5-P090-PROSE-SENTENCE-091-B30093B748E5`<br>`ARINC-615A-3 6.4.5 p.78` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ALLOW-PRINTABLE` / `TEXT-FIELD` / `ALLOW-PRINTABLE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“仅允许可打印字符”；证据是“ALLOW-PRINTABLE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00162` | `SU-ARINC-615A-3-6-4-5-P090-PROSE-SENTENCE-091-B30093B748E5`<br>`ARINC-615A-3 6.4.5 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `EXCLUDE-CONTROL-CHARACTERS` / `TEXT-FIELD, CONTROL-CHARACTERS` / `CONTROL-CHARACTER-ABSENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、CONTROL-CHARACTERS”执行“EXCLUDE-CONTROL-CHARACTERS”；证据是“CONTROL-CHARACTER-ABSENCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00163` | `SU-ARINC-615A-3-6-4-5-P090-PROSE-SENTENCE-091-B30093B748E5`<br>`ARINC-615A-3 6.4.5 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD` / `LIMIT-TEXT-LENGTH-TO-255-CHARACTERS` / `TEXT-FIELD, MAXIMUM-255-CHARACTERS, MAXIMUM-2040-BITS` / `TEXT-LENGTH-BOUND-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“协议文件生成方”在“WHEN-ENCODING-A-PROTOCOL-TEXT-FIELD”下必须对“文本字段、MAXIMUM-255-CHARACTERS、MAXIMUM-2040-BITS”执行“LIMIT-TEXT-LENGTH-TO-255-CHARACTERS”；证据是“TEXT-LENGTH-BOUND-OBSERVABLE”。 | — | — |
| `CRS-M1-00164` | `SU-ARINC-615A-3-6-4-5-P090-PROSE-SENTENCE-092-1532165AA3AE`<br>`ARINC-615A-3 6.4.5 p.78` | `ARINC-615A-PROTOCOL-PARTICIPANT` / `UNCONDITIONAL` / `ENCODE` / `TEXT-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“ARINC 615A 协议参与方”在“UNCONDITIONAL”下必须对“文本字段”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00165` | `SU-ARINC-615A-3-6-4-10-P096-PROSE-SENTENCE-001-2C9653D1AE20`<br>`ARINC-615A-3 6.4.10 p.84` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `DISPLAY` / `TEXT-FIELD, TARGET-HARDWARE-ID` / `USER-INDICATION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“文本字段、TARGET-HARDWARE-ID”执行“显示或通知”；证据是“用户提示可被观察”。 | — | — |
| `CRS-M1-00166` | `SU-ARINC-615A-3-6-4-10-P097-PROSE-SENTENCE-002-5D81ED14D19B`<br>`ARINC-615A-3 6.4.10 p.85` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `WAIT` / `NETWORK-INTERFACE, TARGET-HARDWARE-ID` / `WAIT-BEHAVIOR-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“网络接口、TARGET-HARDWARE-ID”执行“等待”；证据是“等待行为可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00167` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-005-D75104E5A8FF`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `RETRY` / `TIMEOUT-AND-RETRY-LAYERS` / `RETRY-ATTEMPT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“TIMEOUT-AND-RETRY-LAYERS”执行“重试”；证据是“重试尝试可被观察”。 | — | — |
| `CRS-M1-00168` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-009-F320813241E5`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `TRANSFER` / `TFTP-FILE-TRANSFER` / `TRANSFER-OUTCOME-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“TFTP 文件传输”执行“传输”；证据是“传输结果可被观察”。 | `SYMBOLIC-SOURCE-PARAMETER` / `TFTP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-4-3-1-P112-PROSE-SENTENCE-001-97BE648C2E96, SU-ARINC-615A-3-4-3-1-P112-PROSE-SENTENCE-002-E2A9490FA667 | DEP-RFC-1350 |
| `CRS-M1-00169` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-010-414439744FBA`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ACKNOWLEDGE` / `TIMEOUT-EXPIRY` / `ACKNOWLEDGE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“TIMEOUT-EXPIRY”执行“确认”；证据是“ACKNOWLEDGE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00170` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-012-D951F3C8D8DC`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `RETRY` / `TFTP-FILE-TRANSFER` / `RETRY-ATTEMPT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下可以对“TFTP 文件传输”执行“重试”；证据是“重试尝试可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00171` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-013-DCEA052A12C5`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `AFTER-RETRY-LIMIT-EXHAUSTION` / `RETRY` / `TFTP-FILE-TRANSFER, RETRY-NUMBER` / `RETRY-ATTEMPT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“重试限额耗尽后”下必须对“TFTP 文件传输、RETRY-NUMBER”执行“重试”；证据是“重试尝试可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00172` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-014-0E511BD5A2AE`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `PROVIDE` / `PROTOCOL-ERROR` / `PROVIDE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“PROTOCOL-ERROR”执行“提供”；证据是“PROVIDE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00173` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-017-7C1E9A3C2D05`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `ON-TFTP-ERROR` / `RETRY` / `TFTP-FILE-TRANSFER` / `RETRY-ATTEMPT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“TFTP 层报告错误时”下必须对“TFTP 文件传输”执行“重试”；证据是“重试尝试可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00174` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-019-F7B55A457FA5`<br>`ARINC-615A-3 4-1 p.99` | `DLP-CLIENT` / `AFTER-DLP-RETRY-LIMIT-IS-EXCEEDED-AND-ERROR-PERSISTS` / `DECLARE-FATAL-ERROR` / `DLP-FILE-TRANSFER` / `FATAL-ERROR-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“DLP-CLIENT”在“AFTER-DLP-RETRY-LIMIT-IS-EXCEEDED-AND-ERROR-PERSISTS”下必须对“DLP-FILE-TRANSFER”执行“DECLARE-FATAL-ERROR”；证据是“FATAL-ERROR-RESULT-OBSERVABLE”。 | — | DEP-RFC-1350 |
| `CRS-M1-00175` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-020-C80348B18729`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `FAIL` / `PROTOCOL-ERROR` / `FAILURE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“PROTOCOL-ERROR”执行“判定失败”；证据是“失败结果可被观察”。 | — | — |
| `CRS-M1-00176` | `SU-ARINC-615A-3-4-1-P111-PROSE-SENTENCE-028-35890C54B368`<br>`ARINC-615A-3 4-1 p.99` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ADJUST-UPWARD` / `TIMEOUT-VALUE` / `ADJUST-UPWARD-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“TIMEOUT-VALUE”执行“向上调整”；证据是“ADJUST-UPWARD-RESULT-OBSERVABLE”。 | `SYMBOLIC-SOURCE-PARAMETER` / `DLP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-001-E20DEE6A28B4, SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-002-68A6807BC6D8 | — |
| `CRS-M1-00177` | `SU-ARINC-615A-3-4-3-1-P112-PROSE-SENTENCE-004-4C05C3174D37`<br>`ARINC-615A-3 4-3.1 p.100` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `SET-CONSTANT` / `TIMEOUT-VALUE` / `CONSTANT-VALUE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“TIMEOUT-VALUE”执行“设置固定常数”；证据是“固定取值可被观察”。 | `FIXED-SOURCE-CONSTANT` / `TFTP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `2..2 s` / 证据：SU-ARINC-615A-3-4-3-1-P112-PROSE-SENTENCE-004-4C05C3174D37 | — |
| `CRS-M1-00178` | `SU-ARINC-615A-3-4-3-1-P112-PROSE-SENTENCE-005-88F51ABD3389`<br>`ARINC-615A-3 4-3.1 p.100` | `NETWORK-PATH` / `DURING-ONE-TFTP-PACKET-NETWORK-TRANSFER` / `LIMIT-SINGLE-TFTP-PACKET-TRANSMISSION-DURATION` / `SINGLE-TFTP-PACKET, TFTP-TO-DIVIDED-BY-4` / `PACKET-TRANSMISSION-DURATION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“NETWORK-PATH”在“DURING-ONE-TFTP-PACKET-NETWORK-TRANSFER”下必须对“SINGLE-TFTP-PACKET、TFTP-TO-DIVIDED-BY-4”执行“LIMIT-SINGLE-TFTP-PACKET-TRANSMISSION-DURATION”；证据是“PACKET-TRANSMISSION-DURATION-OBSERVABLE”。 | `SYMBOLIC-SOURCE-EQUATION` / `TFTP-TO-DIVIDED-BY-4` / `PACKET-TRANSMISSION-DURATION<=TFTP-TO/4` / `0..TFTP-TO-DIVIDED-BY-4 s` / 证据：SU-ARINC-615A-3-A4-3-1-P112-EQUATION-001 | DEP-RFC-1350 |
| `CRS-M1-00179` | `SU-ARINC-615A-3-4-3-1-P112-PROSE-SENTENCE-007-69549032F30B`<br>`ARINC-615A-3 4-3.1 p.100` | `TFTP-SUBSCRIBER` / `BETWEEN-TFTP-PACKET-RECEPTION-AND-ASSOCIATED-PACKET-EMISSION` / `LIMIT-TFTP-PACKET-PROCESSING-DURATION` / `RECEIVED-TFTP-PACKET, ASSOCIATED-EMITTED-PACKET, TFTP-TO-DIVIDED-BY-2` / `SUBSCRIBER-PROCESSING-DURATION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“TFTP-SUBSCRIBER”在“BETWEEN-TFTP-PACKET-RECEPTION-AND-ASSOCIATED-PACKET-EMISSION”下必须对“RECEIVED-TFTP-PACKET、ASSOCIATED-EMITTED-PACKET、TFTP-TO-DIVIDED-BY-2”执行“LIMIT-TFTP-PACKET-PROCESSING-DURATION”；证据是“SUBSCRIBER-PROCESSING-DURATION-OBSERVABLE”。 | `SYMBOLIC-SOURCE-EQUATION` / `TFTP-TO-DIVIDED-BY-2` / `SUBSCRIBER-PROCESSING-DURATION<=TFTP-TO/2` / `0..TFTP-TO-DIVIDED-BY-2 s` / 证据：SU-ARINC-615A-3-A4-3-1-P112-EQUATION-002 | DEP-RFC-1350 |
| `CRS-M1-00180` | `SU-ARINC-615A-3-4-3-2-P113-PROSE-SENTENCE-001-205BD6EF24F3`<br>`ARINC-615A-3 4-3.2 p.101` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `RETRY` / `TFTP-EXCHANGE, RETRY-NUMBER, TARGET-HARDWARE-ID` / `RETRY-ATTEMPT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下可以对“TFTP 交换、RETRY-NUMBER、TARGET-HARDWARE-ID”执行“重试”；证据是“重试尝试可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00181` | `SU-ARINC-615A-3-4-3-2-P113-PROSE-SENTENCE-011-A604F56F9739`<br>`ARINC-615A-3 4-3.2 p.101` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `RETRY` / `RETRY-NUMBER` / `RETRY-ATTEMPT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“RETRY-NUMBER”执行“重试”；证据是“重试尝试可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00182` | `SU-ARINC-615A-3-4-3-3-P114-PROSE-SENTENCE-001-5174295F548B`<br>`ARINC-615A-3 4-3.3 p.102` | `PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ENCODE` / `SORCERERS-APPRENTICE-FIX` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议实现”在“UNCONDITIONAL”下必须对“SORCERERS-APPRENTICE-FIX”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | DEP-RFC-1123, DEP-RFC-1350 |
| `CRS-M1-00183` | `SU-ARINC-615A-3-4-3-3-P114-PROSE-SENTENCE-002-889533B1AA3F`<br>`ARINC-615A-3 4-3.3 p.102` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `ON-DUPLICATE-ACKNOWLEDGEMENT` / `SEND` / `TFTP-EXCHANGE, NETWORK-INTERFACE` / `MESSAGE-OR-FILE-DIRECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“收到重复确认时”下必须对“TFTP 交换、网络接口”执行“发送”；证据是“消息或文件及其方向可被观察”。 | — | — |
| `CRS-M1-00184` | `SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-003-7C29399D1DAB`<br>`ARINC-615A-3 4-4.1 p.102` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `TRANSFER` / `TFTP-FILE-TRANSFER` / `TRANSFER-OUTCOME-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“TFTP 文件传输”执行“传输”；证据是“传输结果可被观察”。 | `SYMBOLIC-SOURCE-PARAMETER` / `DLP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-001-E20DEE6A28B4, SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-002-68A6807BC6D8 | DEP-RFC-1350 |
| `CRS-M1-00185` | `SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-006-02C6AA3F66A1`<br>`ARINC-615A-3 4-4.1 p.102` | `ARINC-615A-PROTOCOL-IMPLEMENTATION` / `UNCONDITIONAL` / `ADJUST-UPWARD` / `TIMEOUT-VALUE` / `ADJUST-UPWARD-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC 615A 协议实现”在“UNCONDITIONAL”下必须对“TIMEOUT-VALUE”执行“向上调整”；证据是“ADJUST-UPWARD-RESULT-OBSERVABLE”。 | `SYMBOLIC-SOURCE-PARAMETER` / `DLP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-001-E20DEE6A28B4, SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-002-68A6807BC6D8 | — |
| `CRS-M1-00186` | `SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-008-4848608477C0`<br>`ARINC-615A-3 4-4.1 p.102` | `TARGET-HARDWARE` / `WHEN-LCI-LCL-STARTS-BEFORE-DLP-TO-EXPIRY` / `DO-NOT-PRODUCE-LCS-DURING-TIMELY-LCI-LCL-SEQUENCE` / `LCI-LCL-SEQUENCE, DLP-TO, LCS-STATUS-FILE` / `ABSENCE-OF-LCS-BEFORE-DLP-DEADLINE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“WHEN-LCI-LCL-STARTS-BEFORE-DLP-TO-EXPIRY”下必须对“LCI-LCL-SEQUENCE、DLP-TO、LCS-STATUS-FILE”执行“DO-NOT-PRODUCE-LCS-DURING-TIMELY-LCI-LCL-SEQUENCE”；证据是“ABSENCE-OF-LCS-BEFORE-DLP-DEADLINE-OBSERVABLE”。 | `SYMBOLIC-SOURCE-PARAMETER` / `DLP-TO` / `LCI-LCL-START<DLP-TO-EXPIRY=>ABSENT(LCS)` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-001-E20DEE6A28B4, SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-002-68A6807BC6D8 | — |
| `CRS-M1-00187` | `SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-011-BD0CBB7058D1`<br>`ARINC-615A-3 4-4.1 p.102` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `PROVIDE` / `TIMEOUT-VALUE, TARGET-HARDWARE-ID` / `PROVIDE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下必须对“TIMEOUT-VALUE、TARGET-HARDWARE-ID”执行“提供”；证据是“PROVIDE-RESULT-OBSERVABLE”。 | `FIXED-SOURCE-CONSTANT` / `DLP-TO` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `13..13 s` / 证据：SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-011-BD0CBB7058D1 | — |
| `CRS-M1-00188` | `SU-ARINC-615A-3-4-4-1-P114-PROSE-SENTENCE-012-FB8820DE2238`<br>`ARINC-615A-3 4-4.1 p.102` | `TARGET-HARDWARE` / `BETWEEN-CONSECUTIVE-TFTP-FILE-TRANSFERS` / `BOUND-INTER-TRANSFER-DURATION-BY-DLP-EQUATION` / `DURATION-TIME, DLP-TO, DLP-RETRY, TFTP-RETRY, TFTP-TO` / `INTER-TRANSFER-DURATION-AND-EQUATION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“BETWEEN-CONSECUTIVE-TFTP-FILE-TRANSFERS”下必须对“DURATION-TIME、DLP-TO、DLP-RETRY、TFTP-RETRY、TFTP-TO”执行“BOUND-INTER-TRANSFER-DURATION-BY-DLP-EQUATION”；证据是“INTER-TRANSFER-DURATION-AND-EQUATION-OBSERVABLE”。 | `SYMBOLIC-SOURCE-EQUATION` / `DLP-TO-EQUATION` / `DLP-TO>DURATION-TIME+DLP-RETRY*(TFTP-RETRY+1)*TFTP-TO+TFTP-RETRY*TFTP-TO+2*(TFTP-TO/4)` / `0..DLP-TO-MINUS-RETRY-AND-NETWORK-TERMS s` / 证据：SU-ARINC-615A-3-A4-4-1-P115-EQUATION-001 | DEP-RFC-1350 |
| `CRS-M1-00189` | `SU-ARINC-615A-3-4-4-2-1-P115-PROSE-SENTENCE-001-46D0EBEB4FDD`<br>`ARINC-615A-3 4-4.2.1 p.103` | `TARGET-HARDWARE` / `UNCONDITIONAL` / `RETRY` / `TFTP-FILE-TRANSFER, RETRY-NUMBER, TARGET-HARDWARE-ID` / `RETRY-ATTEMPT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“UNCONDITIONAL”下可以对“TFTP 文件传输、RETRY-NUMBER、TARGET-HARDWARE-ID”执行“重试”；证据是“重试尝试可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00190` | `SU-ARINC-615A-3-4-4-2-3-P116-PROSE-SENTENCE-003-546D677F3BB9`<br>`ARINC-615A-3 4-4.2.3 p.104` | `DATA-LOADER` / `UNCONDITIONAL` / `IMPLEMENT` / `NETWORK-INTERFACE` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“UNCONDITIONAL”下可以对“网络接口”执行“提供能力”；证据是“能力可用性可被观察”。 | — | DEP-RFC-1350 |
| `CRS-M1-00191` | `SU-ARINC-665-5-1-3-1-P011-PROSE-SENTENCE-002-93AC8751234E`<br>`ARINC-665-5 1.3.1 p.1` | `ARINC-665-CONFORMING-PRODUCT` / `UNCONDITIONAL` / `IMPLEMENT-REQUIRED-ARINC-665-CAPABILITIES` / `MINIMUM-ARINC-665-COMPATIBILITY-CAPABILITIES` / `ARINC-665-COMPATIBILITY-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-CONFORMING-PRODUCT”在“UNCONDITIONAL”下必须对“MINIMUM-ARINC-665-COMPATIBILITY-CAPABILITIES”执行“IMPLEMENT-REQUIRED-ARINC-665-CAPABILITIES”；证据是“ARINC-665-COMPATIBILITY-OBSERVABLE”。 | — | — |
| `CRS-M1-00192` | `SU-ARINC-665-5-1-3-1-P011-PROSE-SENTENCE-003-F4F4BC419A09`<br>`ARINC-665-5 1.3.1 p.1` | `ARINC-665-REQUIREMENT-INTERPRETER` / `UNCONDITIONAL` / `TREAT-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY` / `ARINC-665-SHOULD-MODALITY` / `MODALITY-INTERPRETATION-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-REQUIREMENT-INTERPRETER”在“UNCONDITIONAL”下必须对“ARINC-665-SHOULD-MODALITY”执行“TREAT-SHOULD-AS-REQUIRED-FOR-MINIMUM-COMPATIBILITY”；证据是“MODALITY-INTERPRETATION-OBSERVABLE”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00193` | `SU-ARINC-665-5-1-3-1-P011-PROSE-SENTENCE-005-BC73FE29F0AF`<br>`ARINC-665-5 1.3.1 p.1` | `ARINC-665-REQUIREMENT-INTERPRETER` / `UNCONDITIONAL` / `TREAT-MAY-AS-OPTIONAL-CAPABILITY` / `ARINC-665-MAY-MODALITY` / `MODALITY-INTERPRETATION-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-REQUIREMENT-INTERPRETER”在“UNCONDITIONAL”下可以对“ARINC-665-MAY-MODALITY”执行“TREAT-MAY-AS-OPTIONAL-CAPABILITY”；证据是“MODALITY-INTERPRETATION-OBSERVABLE”。 | — | — |
| `CRS-M1-00194` | `SU-ARINC-665-5-1-3-1-P011-PROSE-SENTENCE-006-3F3CB7AE6B26`<br>`ARINC-665-5 1.3.1 p.1` | `ARINC-665-CONFORMING-PRODUCT` / `WHEN-A-MAY-CAPABILITY-IS-IMPLEMENTED` / `CONDITIONALLY-IMPLEMENT-OPTIONAL-CAPABILITY-AS-SPECIFIED` / `OPTIONAL-ARINC-665-CAPABILITY` / `CONDITIONAL-CAPABILITY-CONFORMANCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-CONFORMING-PRODUCT”在“WHEN-A-MAY-CAPABILITY-IS-IMPLEMENTED”下必须对“OPTIONAL-ARINC-665-CAPABILITY”执行“CONDITIONALLY-IMPLEMENT-OPTIONAL-CAPABILITY-AS-SPECIFIED”；证据是“CONDITIONAL-CAPABILITY-CONFORMANCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00195` | `SU-ARINC-665-5-1-3-3-P011-PROSE-SENTENCE-001-E0CA338A51EE`<br>`ARINC-665-5 1.3.3 p.1` | `ARINC-665-DATA-OBJECT-CONSUMER` / `UNCONDITIONAL` / `INTERPRET-FIELDS-AS-NUMERIC-BY-DEFAULT` / `DATA-FIELD-TYPE` / `DATA-TYPE-INTERPRETATION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-CONSUMER”在“UNCONDITIONAL”下必须对“DATA-FIELD-TYPE”执行“INTERPRET-FIELDS-AS-NUMERIC-BY-DEFAULT”；证据是“DATA-TYPE-INTERPRETATION-OBSERVABLE”。 | — | — |
| `CRS-M1-00196` | `SU-ARINC-665-5-1-4-2-P012-PROSE-SENTENCE-002-D07F6C2D4DAC`<br>`ARINC-665-5 1.4.2 p.2` | `LSP-OR-MEDIA-SET-CREATOR` / `UNCONDITIONAL` / `PROHIBIT-UNDEFINED-FIELD-INSERTION` / `ARINC-665-FILE` / `UNDEFINED-FIELD-ABSENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“LSP-OR-MEDIA-SET-CREATOR”在“UNCONDITIONAL”下必须对“ARINC-665-FILE”执行“PROHIBIT-UNDEFINED-FIELD-INSERTION”；证据是“UNDEFINED-FIELD-ABSENCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00197` | `SU-ARINC-665-5-1-4-3-P013-PROSE-SENTENCE-004-C23C95885017`<br>`ARINC-665-5 1.4.3 p.3` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `FILE-VERSION-COMPATIBILITY` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“FILE-VERSION-COMPATIBILITY”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00198` | `SU-ARINC-665-5-1-5-P014-PROSE-SENTENCE-002-DBF83061338F`<br>`ARINC-665-5 1.5 p.4` | `SOFTWARE-PACKAGE-PRODUCER` / `UNCONDITIONAL` / `PREFIX-TARGET-HARDWARE-ID-WITH-MANUFACTURER-CODE` / `TARGET-HARDWARE-ID, MANUFACTURER-IDENTIFIER` / `TARGET-HARDWARE-ID-PREFIX-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“软件包生成方”在“UNCONDITIONAL”下必须对“TARGET-HARDWARE-ID、MANUFACTURER-IDENTIFIER”执行“PREFIX-TARGET-HARDWARE-ID-WITH-MANUFACTURER-CODE”；证据是“TARGET-HARDWARE-ID-PREFIX-OBSERVABLE”。 | — | — |
| `CRS-M1-00199` | `SU-ARINC-665-5-1-5-P014-PROSE-SENTENCE-003-35251417E277`<br>`ARINC-665-5 1.5 p.4` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ASSIGN` / `MANUFACTURER-IDENTIFIER` / `ASSIGN-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“MANUFACTURER-IDENTIFIER”执行“分配或管理”；证据是“ASSIGN-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00200` | `SU-ARINC-665-5-1-5-P015-PROSE-SENTENCE-005-8F3C7190D1E7`<br>`ARINC-665-5 1.5 p.5` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-A-SOFTWARE-PART-IS-ACCEPTED-BY-MULTIPLE-TARGET-TYPES` / `ASSIGN-GENERIC-TARGET-HARDWARE-ID` / `SOFTWARE-PART-TARGET-HARDWARE-ID` / `TARGET-HARDWARE-ID-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“软件包生成方”在“WHEN-A-SOFTWARE-PART-IS-ACCEPTED-BY-MULTIPLE-TARGET-TYPES”下必须对“SOFTWARE-PART-TARGET-HARDWARE-ID”执行“ASSIGN-GENERIC-TARGET-HARDWARE-ID”；证据是“TARGET-HARDWARE-ID-FIELD-OBSERVABLE”。 | — | — |
| `CRS-M1-00201` | `SU-ARINC-665-5-1-5-P015-PROSE-SENTENCE-007-6D740BC1EA66`<br>`ARINC-665-5 1.5 p.5` | `MULTI-CHANNEL-TARGET-SYSTEM` / `UNCONDITIONAL` / `DISTRIBUTE-REDUNDANT-LOADS-INTERNALLY` / `REDUNDANT-CHANNEL-LOADS` / `SINGLE-EXTERNAL-LOAD-REQUEST-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“MULTI-CHANNEL-TARGET-SYSTEM”在“UNCONDITIONAL”下必须对“REDUNDANT-CHANNEL-LOADS”执行“DISTRIBUTE-REDUNDANT-LOADS-INTERNALLY”；证据是“SINGLE-EXTERNAL-LOAD-REQUEST-OBSERVABLE”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00202` | `SU-ARINC-665-5-2-1-P016-PROSE-SENTENCE-001-A7E185845C31`<br>`ARINC-665-5 2.1 p.6` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENSURE-CARDINALITY` / `LOAD-PART-NUMBER, SOFTWARE-PART, LOADABLE-SOFTWARE-PART-NUMBER` / `ENSURE-CARDINALITY-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“加载件号、软件加载件、LOADABLE-SOFTWARE-PART-NUMBER”执行“保证基数约束”；证据是“ENSURE-CARDINALITY-RESULT-OBSERVABLE”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00203` | `SU-ARINC-665-5-2-1-P016-PROSE-SENTENCE-002-C9B7C44AE544`<br>`ARINC-665-5 2.1 p.6` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `COORDINATE` / `LOAD-PART-NUMBER` / `COORDINATE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“加载件号”执行“协调并批准”；证据是“COORDINATE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00204` | `SU-ARINC-665-5-2-1-P016-PROSE-SENTENCE-003-D2A78669BC58`<br>`ARINC-665-5 2.1 p.6` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ASSIGN` / `LOAD-PART-NUMBER, SOFTWARE-PART` / `ASSIGN-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“加载件号、软件加载件”执行“分配或管理”；证据是“ASSIGN-RESULT-OBSERVABLE”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00205` | `SU-ARINC-665-5-2-1-1-P016-PROSE-SENTENCE-001-79D9D9285B09`<br>`ARINC-665-5 2.1.1 p.6` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `FORMAT` / `LOADABLE-SOFTWARE-PART-NUMBER` / `ENCODED-FORMAT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“LOADABLE-SOFTWARE-PART-NUMBER”执行“按规定格式化”；证据是“编码格式可被观察”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00206` | `SU-ARINC-665-5-2-1-1-P016-PROSE-SENTENCE-005-9401791D8DFE`<br>`ARINC-665-5 2.1.1 p.6` | `ARINC-665-DATA-OBJECT-PRODUCER` / `UNCONDITIONAL` / `EXCLUDE-EMBEDDED-BLANKS` / `LOAD-PART-NUMBER` / `LOAD-PART-NUMBER-ENCODING-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“UNCONDITIONAL”下必须对“加载件号”执行“EXCLUDE-EMBEDDED-BLANKS”；证据是“LOAD-PART-NUMBER-ENCODING-OBSERVABLE”。 | — | — |
| `CRS-M1-00207` | `SU-ARINC-665-5-2-1-1-P016-PROSE-SENTENCE-008-6FB26843CBD8`<br>`ARINC-665-5 2.1.1 p.6` | `ARINC-615A-DATA-LOADER` / `UNCONDITIONAL` / `DO-NOT-ENFORCE-SPECIFIC-PART-NUMBER-FORMAT` / `LOAD-PART-NUMBER` / `ABSENCE-OF-PN-FORMAT-REJECTION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-615A-DATA-LOADER”在“UNCONDITIONAL”下必须对“加载件号”执行“DO-NOT-ENFORCE-SPECIFIC-PART-NUMBER-FORMAT”；证据是“ABSENCE-OF-PN-FORMAT-REJECTION-OBSERVABLE”。 | — | — |
| `CRS-M1-00208` | `SU-ARINC-665-5-2-1-1-P016-PROSE-SENTENCE-009-63B5D84BC565`<br>`ARINC-665-5 2.1.1 p.6` | `ARINC-615A-DATA-LOADER` / `UNCONDITIONAL` / `PROCESS-NONCONFORMING-PART-NUMBER-FORMATS` / `LOAD-PART-NUMBER` / `LOAD-ACCEPTANCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-615A-DATA-LOADER”在“UNCONDITIONAL”下必须对“加载件号”执行“PROCESS-NONCONFORMING-PART-NUMBER-FORMATS”；证据是“LOAD-ACCEPTANCE-OBSERVABLE”。 | — | — |
| `CRS-M1-00209` | `SU-ARINC-665-5-2-1-1-P017-PROSE-SENTENCE-014-4EC0F7886DBA`<br>`ARINC-665-5 2.1.1 p.7` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `DESIGN` / `NETWORK-INTERFACE` / `DESIGN-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下可以对“网络接口”执行“设计”；证据是“DESIGN-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00210` | `SU-ARINC-665-5-2-1-1-P017-PROSE-SENTENCE-015-3EE2B6181AC8`<br>`ARINC-665-5 2.1.1 p.7` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `FORMAT` / `NETWORK-INTERFACE` / `ENCODED-FORMAT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下可以对“网络接口”执行“按规定格式化”；证据是“编码格式可被观察”。 | — | — |
| `CRS-M1-00211` | `SU-ARINC-665-5-2-1-1-P017-PROSE-SENTENCE-018-ED171884907D`<br>`ARINC-665-5 2.1.1 p.7` | `ARINC-665-DATA-OBJECT-PRODUCER` / `UNCONDITIONAL` / `SEPARATE-DELIMITERS-FROM-LETTERS` / `ATA-PART-NUMBER-DELIMITERS` / `DELIMITER-PLACEMENT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“UNCONDITIONAL”下必须对“ATA-PART-NUMBER-DELIMITERS”执行“SEPARATE-DELIMITERS-FROM-LETTERS”；证据是“DELIMITER-PLACEMENT-OBSERVABLE”。 | — | — |
| `CRS-M1-00212` | `SU-ARINC-665-5-2-1-1-P017-PROSE-SENTENCE-021-CBAD881793E5`<br>`ARINC-665-5 2.1.1 p.7` | `PROTOCOL-FILE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `LOAD-PART-NUMBER` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“生成 ARINC 665 数据对象时”下必须对“加载件号”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00213` | `SU-ARINC-665-5-2-1-1-P017-PROSE-SENTENCE-022-1D9E17675A1C`<br>`ARINC-665-5 2.1.1 p.7` | `ARINC-665-DATA-OBJECT-PRODUCER` / `UNCONDITIONAL` / `EXCLUDE-AMBIGUOUS-LETTER-O` / `ATA-PART-NUMBER-CHARACTER-SET` / `PART-NUMBER-CHARACTER-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“UNCONDITIONAL”下必须对“ATA-PART-NUMBER-CHARACTER-SET”执行“EXCLUDE-AMBIGUOUS-LETTER-O”；证据是“PART-NUMBER-CHARACTER-OBSERVABLE”。 | — | — |
| `CRS-M1-00214` | `SU-ARINC-665-5-2-1-1-P017-PROSE-SENTENCE-024-481F25AD55F2`<br>`ARINC-665-5 2.1.1 p.7` | `ARINC-665-DATA-OBJECT-CONSUMER` / `UNCONDITIONAL` / `INTERPRET-CONFUSED-MMM-CHARACTERS-AS-ALPHABETIC` / `MMM-CODE` / `MMM-CHARACTER-INTERPRETATION-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-CONSUMER”在“UNCONDITIONAL”下必须对“MMM-CODE”执行“INTERPRET-CONFUSED-MMM-CHARACTERS-AS-ALPHABETIC”；证据是“MMM-CHARACTER-INTERPRETATION-OBSERVABLE”。 | — | — |
| `CRS-M1-00215` | `SU-ARINC-665-5-2-1-3-P017-PROSE-SENTENCE-003-41F8723AEC8B`<br>`ARINC-665-5 2.1.3 p.7` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `COMPUTE` / `CHECK-CHARACTERS` / `COMPUTE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CHECK-CHARACTERS”执行“计算”；证据是“COMPUTE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00216` | `SU-ARINC-665-5-2-2-2-1-P018-PROSE-SENTENCE-001-84EA4A3113C8`<br>`ARINC-665-5 2.2.2.1 p.8` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `FORMAT` / `HEADER-FILE, SOFTWARE-PART` / `ENCODED-FORMAT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“头文件、软件加载件”执行“按规定格式化”；证据是“编码格式可被观察”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00217` | `SU-ARINC-665-5-2-2-3-1-P018-PROSE-SENTENCE-001-7A7C6DE1A7A7`<br>`ARINC-665-5 2.2.3.1 p.8` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `HEADER-FILE, SOFTWARE-PART` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“头文件、软件加载件”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00218` | `SU-ARINC-665-5-2-2-3-1-P019-PROSE-SENTENCE-003-D19D48006847`<br>`ARINC-665-5 2.2.3.1 p.9` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `DEFINE` / `HEADER-FILE` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“头文件”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00219` | `SU-ARINC-665-5-2-2-3-1-P019-PROSE-SENTENCE-004-A761BB0130D9`<br>`ARINC-665-5 2.2.3.1 p.9` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `BINARY-FIELD-ENCODING` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“BINARY-FIELD-ENCODING”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00220` | `SU-ARINC-665-5-2-2-3-1-3-1-P021-PROSE-SENTENCE-004-EF7E6FF4663B`<br>`ARINC-665-5 2.2.3.1.3.1 p.11` | `DATA-LOADER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `OPERATION, STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“生成 ARINC 665 数据对象时”下可以对“协议操作、STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00221` | `SU-ARINC-665-5-2-2-3-1-3-2-P021-PROSE-SENTENCE-001-641A8CBC9145`<br>`ARINC-665-5 2.2.3.1.3.2 p.11` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `BINARY-FIELD-ENCODING` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“BINARY-FIELD-ENCODING”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00222` | `SU-ARINC-665-5-2-2-3-1-10-P022-PROSE-SENTENCE-003-BCEBB784B407`<br>`ARINC-665-5 2.2.3.1.10 p.12` | `TARGET-HARDWARE` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `TARGET-HARDWARE-ID, STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“生成 ARINC 665 数据对象时”下必须对“TARGET-HARDWARE-ID、STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00223` | `SU-ARINC-665-5-2-2-3-1-14-P022-PROSE-SENTENCE-004-4114C0816C51`<br>`ARINC-665-5 2.2.3.1.14 p.12` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `IMPLEMENT` / `LOAD-PART-NUMBER, SOFTWARE-PART` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“加载件号、软件加载件”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00224` | `SU-ARINC-665-5-2-2-3-1-18-P023-PROSE-SENTENCE-002-E664B245877E`<br>`ARINC-665-5 2.2.3.1.18 p.13` | `PROTOCOL-FILE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `NETWORK-INTERFACE, STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“生成 ARINC 665 数据对象时”下必须对“网络接口、STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00225` | `SU-ARINC-665-5-2-2-3-1-18-P023-PROSE-SENTENCE-004-C2CE75F23520`<br>`ARINC-665-5 2.2.3.1.18 p.13` | `TARGET-HARDWARE` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENSURE-UNIQUE` / `SOFTWARE-PART, TARGET-HARDWARE-ID` / `ENSURE-UNIQUE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“生成 ARINC 665 数据对象时”下必须对“软件加载件、TARGET-HARDWARE-ID”执行“保证唯一性”；证据是“ENSURE-UNIQUE-RESULT-OBSERVABLE”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00226` | `SU-ARINC-665-5-2-2-3-1-24-P024-PROSE-SENTENCE-002-C100FC8EE4E9`<br>`ARINC-665-5 2.2.3.1.24 p.14` | `TARGET-HARDWARE` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `SOFTWARE-PART, TARGET-HARDWARE-ID` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“生成 ARINC 665 数据对象时”下必须对“软件加载件、TARGET-HARDWARE-ID”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | DEP-ARINC-6655 |
| `CRS-M1-00227` | `SU-ARINC-665-5-2-2-3-1-26-P024-PROSE-SENTENCE-005-38372C2FA366`<br>`ARINC-665-5 2.2.3.1.26 p.14` | `TARGET-HARDWARE` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `TARGET-HARDWARE-ID, STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“生成 ARINC 665 数据对象时”下必须对“TARGET-HARDWARE-ID、STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00228` | `SU-ARINC-665-5-2-2-3-1-31-P025-PROSE-SENTENCE-002-0374CB53F0AB`<br>`ARINC-665-5 2.2.3.1.31 p.15` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `CONSTRAIN` / `DATA-FILE` / `CONSTRAIN-RESULT-OBSERVABLE` | `MUST` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“数据文件”执行“施加边界约束”；证据是“CONSTRAIN-RESULT-OBSERVABLE”。 | — | — |
| `CRS-M1-00229` | `SU-ARINC-665-5-2-2-3-1-32-P025-PROSE-SENTENCE-002-F6BCEFFF8371`<br>`ARINC-665-5 2.2.3.1.32 p.15` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `SET-ZERO` / `DATA-FILE` / `ZERO-VALUE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“数据文件”执行“置零”；证据是“零值可被观察”。 | — | — |
| `CRS-M1-00230` | `SU-ARINC-665-5-2-2-3-1-37-P026-PROSE-SENTENCE-002-05AC99F08A26`<br>`ARINC-665-5 2.2.3.1.37 p.16` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `FORMAT` / `DATA-FILE` / `ENCODED-FORMAT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“数据文件”执行“按规定格式化”；证据是“编码格式可被观察”。 | — | — |
| `CRS-M1-00231` | `SU-ARINC-665-5-2-2-3-1-38-P026-PROSE-SENTENCE-002-E3FF88E1EDA0`<br>`ARINC-665-5 2.2.3.1.38 p.16` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `DEFINE` / `CRC, NETWORK-INTERFACE` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值、网络接口”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00232` | `SU-ARINC-665-5-2-2-3-1-40-P026-PROSE-SENTENCE-002-FCF47A272C90`<br>`ARINC-665-5 2.2.3.1.40 p.16` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00233` | `SU-ARINC-665-5-2-2-3-1-41-P026-PROSE-SENTENCE-002-3F17CFA7FF3B`<br>`ARINC-665-5 2.2.3.1.41 p.16` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00234` | `SU-ARINC-665-5-2-2-3-1-42-P026-PROSE-SENTENCE-002-5E94CB4814AF`<br>`ARINC-665-5 2.2.3.1.42 p.16` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00235` | `SU-ARINC-665-5-2-2-3-1-44-P027-PROSE-SENTENCE-002-AF1722AA2C2B`<br>`ARINC-665-5 2.2.3.1.44 p.17` | `PROTOCOL-FILE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `NETWORK-INTERFACE` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“生成 ARINC 665 数据对象时”下必须对“网络接口”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00236` | `SU-ARINC-665-5-2-2-3-1-45-P027-PROSE-SENTENCE-002-3B48FE46115E`<br>`ARINC-665-5 2.2.3.1.45 p.17` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `IMPLEMENT` / `NETWORK-INTERFACE` / `CAPABILITY-AVAILABILITY-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“网络接口”执行“提供能力”；证据是“能力可用性可被观察”。 | — | — |
| `CRS-M1-00237` | `SU-ARINC-665-5-2-2-3-1-49-P027-PROSE-SENTENCE-004-5EFD86A600D8`<br>`ARINC-665-5 2.2.3.1.49 p.17` | `PROTOCOL-FILE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `LOAD-PART-NUMBER, NETWORK-INTERFACE, STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“生成 ARINC 665 数据对象时”下必须对“加载件号、网络接口、STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00238` | `SU-ARINC-665-5-2-2-3-1-51-P027-PROSE-SENTENCE-002-E3FF88E1EDA0`<br>`ARINC-665-5 2.2.3.1.51 p.17` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `DEFINE` / `CRC, NETWORK-INTERFACE` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值、网络接口”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00239` | `SU-ARINC-665-5-2-2-3-1-53-P028-PROSE-SENTENCE-002-EE1E5830AB09`<br>`ARINC-665-5 2.2.3.1.53 p.18` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00240` | `SU-ARINC-665-5-2-2-3-1-54-P028-PROSE-SENTENCE-002-02BC06547867`<br>`ARINC-665-5 2.2.3.1.54 p.18` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC, NETWORK-INTERFACE` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值、网络接口”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00241` | `SU-ARINC-665-5-2-2-3-1-57-P028-PROSE-SENTENCE-002-284196C6B3D0`<br>`ARINC-665-5 2.2.3.1.57 p.18` | `OPERATOR` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `HEADER-FILE` / `VALIDATION-RESULT-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“操作员”在“生成 ARINC 665 数据对象时”下可以对“头文件”执行“验证”；证据是“验证结果可被观察”。 | — | — |
| `CRS-M1-00242` | `SU-ARINC-665-5-2-2-3-1-57-P028-PROSE-SENTENCE-003-E6ACA86FDF43`<br>`ARINC-665-5 2.2.3.1.57 p.18` | `PROTOCOL-FILE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `STATUS-CODE-CONDITIONAL-FIELD` / `ENCODED-FIELD-OBSERVABLE` | `MAY` / `OPTIONAL` | `APPLICABLE-SUPPORTING` | 参与者“协议文件生成方”在“生成 ARINC 665 数据对象时”下可以对“STATUS-CODE-CONDITIONAL-FIELD”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00243` | `SU-ARINC-665-5-2-2-3-1-59-P028-PROSE-SENTENCE-002-6672CA36E154`<br>`ARINC-665-5 2.2.3.1.59 p.18` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00244` | `SU-ARINC-665-5-2-2-3-1-60-P028-PROSE-SENTENCE-002-3F17CFA7FF3B`<br>`ARINC-665-5 2.2.3.1.60 p.18` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00245` | `SU-ARINC-665-5-2-2-3-1-61-P029-PROSE-SENTENCE-002-6F1B40878C6B`<br>`ARINC-665-5 2.2.3.1.61 p.19` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00246` | `SU-ARINC-665-5-2-2-3-1-61-P029-PROSE-SENTENCE-003-6155DCD79C06`<br>`ARINC-665-5 2.2.3.1.61 p.19` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00247` | `SU-ARINC-665-5-2-2-3-1-61-P029-PROSE-SENTENCE-004-9A509D9AE4E2`<br>`ARINC-665-5 2.2.3.1.61 p.19` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `VALIDATE` / `CRC` / `VALIDATION-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值”执行“验证”；证据是“验证结果可被观察”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00248` | `SU-ARINC-665-5-2-2-3-1-62-P029-PROSE-SENTENCE-002-136B2E7764B0`<br>`ARINC-665-5 2.2.3.1.62 p.19` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `DEFINE` / `HEADER-FILE, CRC, NETWORK-INTERFACE` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“头文件、CRC／校验值、网络接口”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00249` | `SU-ARINC-665-5-2-2-3-1-63-P029-PROSE-SENTENCE-002-8F49EC0CB8C3`<br>`ARINC-665-5 2.2.3.1.63 p.19` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `COMPUTE` / `HEADER-FILE, CRC` / `COMPUTE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“头文件、CRC／校验值”执行“计算”；证据是“COMPUTE-RESULT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00250` | `SU-ARINC-665-5-2-2-3-1-63-P029-PROSE-SENTENCE-003-5A9C8CDFFDEB`<br>`ARINC-665-5 2.2.3.1.63 p.19` | `ARINC-665-DATA-OBJECT-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `DEFINE` / `CRC, NETWORK-INTERFACE` / `DEFINE-RESULT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“ARINC-665-DATA-OBJECT-PRODUCER”在“生成 ARINC 665 数据对象时”下必须对“CRC／校验值、网络接口”执行“定义”；证据是“DEFINE-RESULT-OBSERVABLE”。 | — | DEP-ARINC-645, GAP-ARINC-645 |
| `CRS-M1-00251` | `SU-ARINC-665-5-2-2-3-2-P029-PROSE-SENTENCE-002-25AC959A1D2A`<br>`ARINC-665-5 2.2.3.2 p.19` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `DATA-FILE, SOFTWARE-PART, FILE-CONTENT` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“数据文件、软件加载件、FILE-CONTENT”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00252` | `SU-ARINC-665-5-2-2-3-3-P029-PROSE-SENTENCE-002-BC8C7608516E`<br>`ARINC-665-5 2.2.3.3 p.19` | `SOFTWARE-PACKAGE-PRODUCER` / `WHEN-PRODUCING-ARINC-665-DATA-OBJECT` / `ENCODE` / `SOFTWARE-PART, NETWORK-INTERFACE, FILE-CONTENT` / `ENCODED-FIELD-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“软件包生成方”在“生成 ARINC 665 数据对象时”下必须对“软件加载件、网络接口、FILE-CONTENT”执行“编码或赋值”；证据是“编码字段可被观察”。 | — | — |
| `CRS-M1-00253` | `SU-ARINC-615A-3-TABLE-6-1-R002`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `TH_INFORMATION_INITIALIZATION` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“TH_INFORMATION_INITIALIZATION”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00254` | `SU-ARINC-615A-3-TABLE-6-1-R003`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `INFORMATION_INITIALIZATION_RESPONSE` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“INFORMATION_INITIALIZATION_RESPONSE”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00255` | `SU-ARINC-615A-3-TABLE-6-1-R005`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `TH_INFORMATION` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“TH_INFORMATION”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00256` | `SU-ARINC-615A-3-TABLE-6-1-R006`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `INFORMATION_STATUS` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“INFORMATION_STATUS”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00257` | `SU-ARINC-615A-3-TABLE-6-1-R007`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `ABORT_REQUEST` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“ABORT_REQUEST”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00258` | `SU-ARINC-615A-3-TABLE-6-1-R009`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `TH_UPLOADING_INITIALIZATION` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“TH_UPLOADING_INITIALIZATION”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00259` | `SU-ARINC-615A-3-TABLE-6-1-R010`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `UPLOADING_INITIALIZATION_RESPONSE` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“UPLOADING_INITIALIZATION_RESPONSE”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00260` | `SU-ARINC-615A-3-TABLE-6-1-R012`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `LOAD_LIST` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“LOAD_LIST”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00261` | `SU-ARINC-615A-3-TABLE-6-1-R013`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `UPLOAD_INFORMATION_STATUS` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“UPLOAD_INFORMATION_STATUS”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00262` | `SU-ARINC-615A-3-TABLE-6-1-R014`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `ABORT_REQUEST` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“ABORT_REQUEST”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00263` | `SU-ARINC-615A-3-TABLE-6-1-R016`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `FILE_NOT_AVAILABLE` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“FILE_NOT_AVAILABLE”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00264` | `SU-ARINC-615A-3-TABLE-6-1-R017`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `UPLOAD_INFORMATION_STATUS` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“UPLOAD_INFORMATION_STATUS”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00265` | `SU-ARINC-615A-3-TABLE-6-1-R018`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `ABORT_REQUEST` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“ABORT_REQUEST”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00266` | `SU-ARINC-615A-3-TABLE-6-1-R020`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_MEDIA_INITIALIZATION` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“DOWNLOADING_MEDIA_INITIALIZATION”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00267` | `SU-ARINC-615A-3-TABLE-6-1-R021`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_INITIALIZATION_RESPONSE` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_INITIALIZATION_RESPONSE”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00268` | `SU-ARINC-615A-3-TABLE-6-1-R023`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_INFORMATION_STATUS` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_INFORMATION_STATUS”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00269` | `SU-ARINC-615A-3-TABLE-6-1-R024`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `ABORT_REQUEST` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“ABORT_REQUEST”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00270` | `SU-ARINC-615A-3-TABLE-6-1-R026`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_FILE_RECEIPT` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_FILE_RECEIPT”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00271` | `SU-ARINC-615A-3-TABLE-6-1-R027`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_INFORMATION_STATUS` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_INFORMATION_STATUS”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00272` | `SU-ARINC-615A-3-TABLE-6-1-R028`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `ABORT_REQUEST` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“ABORT_REQUEST”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00273` | `SU-ARINC-615A-3-TABLE-6-1-R030`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_OPERATOR_INITIALIZATION` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“DOWNLOADING_OPERATOR_INITIALIZATION”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00274` | `SU-ARINC-615A-3-TABLE-6-1-R031`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_INITIALIZATION_RESPONSE` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_INITIALIZATION_RESPONSE”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00275` | `SU-ARINC-615A-3-TABLE-6-1-R033`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_FILE_LIST_RECEIPT` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_FILE_LIST_RECEIPT”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00276` | `SU-ARINC-615A-3-TABLE-6-1-R034`<br>`ARINC-615A-3 6.1 p.42` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `FILE_SELECTION` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“FILE_SELECTION”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00277` | `SU-ARINC-615A-3-TABLE-6-1-R035`<br>`ARINC-615A-3 6.1 p.42` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_INFORMATION_STATUS` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_INFORMATION_STATUS”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00278` | `SU-ARINC-615A-3-TABLE-6-1-R036`<br>`ARINC-615A-3 6.1 p.43` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `ABORT-REQUEST` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“ABORT-REQUEST”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00279` | `SU-ARINC-615A-3-TABLE-6-1-R038`<br>`ARINC-615A-3 6.1 p.43` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_FILE_RECEIPT` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_FILE_RECEIPT”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00280` | `SU-ARINC-615A-3-TABLE-6-1-R039`<br>`ARINC-615A-3 6.1 p.43` | `DLP` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `DOWNLOADING_INFORMATION_STATUS` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器协议层”在“表中规定的操作步骤”下必须对“DOWNLOADING_INFORMATION_STATUS”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00281` | `SU-ARINC-615A-3-TABLE-6-1-R040`<br>`ARINC-615A-3 6.1 p.43` | `DLA` / `TABLE-DEFINED-OPERATION-STEP` / `SEND` / `ABORT_REQUEST` / `MESSAGE-DIRECTION-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“表中规定的操作步骤”下必须对“ABORT_REQUEST”执行“发送”；证据是“消息名称与传输方向可被观察”。 | — | — |
| `CRS-M1-00282` | `SU-ARINC-615A-3-TABLE-6_4_1-1-R002`<br>`ARINC-615A-3 6.4.1 p.67` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-FILE-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 1 个字段位置编码 FIELD-FILE-LENGTH，位宽为 32 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00283` | `SU-ARINC-615A-3-TABLE-6_4_1-1-R003`<br>`ARINC-615A-3 6.4.1 p.67` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PROTOCOL-VERSION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 2 个字段位置编码 FIELD-PROTOCOL-VERSION，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00284` | `SU-ARINC-615A-3-TABLE-6_4_1-1-R004`<br>`ARINC-615A-3 6.4.1 p.67` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-OPERATION-ACCEPTANCE-STATUS-CODE` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 3 个字段位置编码 FIELD-OPERATION-ACCEPTANCE-STATUS-CODE，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00285` | `SU-ARINC-615A-3-TABLE-6_4_1-1-R005`<br>`ARINC-615A-3 6.4.1 p.67` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-STATUS-DESCRIPTION-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 4 个字段位置编码 FIELD-STATUS-DESCRIPTION-LENGTH，位宽为 8 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00286` | `SU-ARINC-615A-3-TABLE-6_4_1-1-R006`<br>`ARINC-615A-3 6.4.1 p.67` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-STATUS-DESCRIPTION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 5 个字段位置编码 FIELD-STATUS-DESCRIPTION，位宽为 0..2040 bit，重复范围为 ONCE；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00287` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R002`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-FILE-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 1 个字段位置编码 FIELD-FILE-LENGTH，位宽为 32 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00288` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R003`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PROTOCOL-VERSION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 2 个字段位置编码 FIELD-PROTOCOL-VERSION，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00289` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R004`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-NUMBER-OF-TARGET-HARDWARE` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 3 个字段位置编码 FIELD-NUMBER-OF-TARGET-HARDWARE，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00290` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R005`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LITERAL-NAME-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 4 个字段位置编码 FIELD-LITERAL-NAME-LENGTH，位宽为 8 bit，重复范围为 PER-LITERAL-NAME；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00291` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R006`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LITERAL-NAME` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 5 个字段位置编码 FIELD-LITERAL-NAME，位宽为 8..2040 bit，重复范围为 PER-LITERAL-NAME；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00292` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R007`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-SERIAL-NUMBER-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 6 个字段位置编码 FIELD-SERIAL-NUMBER-LENGTH，位宽为 8 bit，重复范围为 PER-LITERAL-NAME；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00293` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R008`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-SERIAL-NUMBER` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 7 个字段位置编码 FIELD-SERIAL-NUMBER，位宽为 8..2040 bit，重复范围为 PER-LITERAL-NAME；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00294` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R009`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-NUMBER-OF-PART-NUMBERS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 8 个字段位置编码 FIELD-NUMBER-OF-PART-NUMBERS，位宽为 16 bit，重复范围为 PER-LITERAL-NAME；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00295` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R010`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PART-NUMBER-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 9 个字段位置编码 FIELD-PART-NUMBER-LENGTH，位宽为 8 bit，重复范围为 PER-PART-NUMBER-WITHIN-LITERAL-NAME；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00296` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R011`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PART-NUMBER` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 10 个字段位置编码 FIELD-PART-NUMBER，位宽为 8..2040 bit，重复范围为 PER-PART-NUMBER-WITHIN-LITERAL-NAME；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00297` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R012`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-AMENDMENT-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 11 个字段位置编码 FIELD-AMENDMENT-LENGTH，位宽为 8 bit，重复范围为 PER-PART-NUMBER-WITHIN-LITERAL-NAME；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00298` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R013`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-AMENDMENT` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 12 个字段位置编码 FIELD-AMENDMENT，位宽为 0..2040 bit，重复范围为 PER-PART-NUMBER-WITHIN-LITERAL-NAME；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00299` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R014`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PART-DESIGNATION-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 13 个字段位置编码 FIELD-PART-DESIGNATION-LENGTH，位宽为 8 bit，重复范围为 PER-PART-NUMBER-WITHIN-LITERAL-NAME；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00300` | `SU-ARINC-615A-3-TABLE-6_4_2-1-R015`<br>`ARINC-615A-3 6.4.2 p.68` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PART-DESIGNATION-TEXT` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 14 个字段位置编码 FIELD-PART-DESIGNATION-TEXT，位宽为 8..2040 bit，重复范围为 PER-PART-NUMBER-WITHIN-LITERAL-NAME；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00301` | `SU-ARINC-615A-3-TABLE-6_4_3-1-R002`<br>`ARINC-615A-3 6.4.3 p.70` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-FILE-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 1 个字段位置编码 FIELD-FILE-LENGTH，位宽为 32 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00302` | `SU-ARINC-615A-3-TABLE-6_4_3-1-R003`<br>`ARINC-615A-3 6.4.3 p.70` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PROTOCOL-VERSION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 2 个字段位置编码 FIELD-PROTOCOL-VERSION，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00303` | `SU-ARINC-615A-3-TABLE-6_4_3-1-R004`<br>`ARINC-615A-3 6.4.3 p.70` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-COUNTER` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 3 个字段位置编码 FIELD-COUNTER，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00304` | `SU-ARINC-615A-3-TABLE-6_4_3-1-R005`<br>`ARINC-615A-3 6.4.3 p.70` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-INFORMATION-OPERATION-STATUS-CODE` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 4 个字段位置编码 FIELD-INFORMATION-OPERATION-STATUS-CODE，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00305` | `SU-ARINC-615A-3-TABLE-6_4_3-1-R006`<br>`ARINC-615A-3 6.4.3 p.70` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-EXCEPTION-TIMER` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 5 个字段位置编码 FIELD-EXCEPTION-TIMER，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | `MESSAGE-CARRIED-PARAMETER` / `MESSAGE-TIMER-VALUE` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-TABLE-6_4_3-1-R006 | — |
| `CRS-M1-00306` | `SU-ARINC-615A-3-TABLE-6_4_3-1-R007`<br>`ARINC-615A-3 6.4.3 p.70` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-ESTIMATED-TIME` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 6 个字段位置编码 FIELD-ESTIMATED-TIME，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00307` | `SU-ARINC-615A-3-TABLE-6_4_3-1-R008`<br>`ARINC-615A-3 6.4.3 p.70` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-STATUS-DESCRIPTION-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 7 个字段位置编码 FIELD-STATUS-DESCRIPTION-LENGTH，位宽为 8 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00308` | `SU-ARINC-615A-3-TABLE-6_4_3-1-R009`<br>`ARINC-615A-3 6.4.3 p.70` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-STATUS-DESCRIPTION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 协议文件生成方必须在第 8 个字段位置编码 FIELD-STATUS-DESCRIPTION，位宽为 0..2040 bit，重复范围为 ONCE；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00309` | `SU-ARINC-615A-3-TABLE-6_4_4-1-R002`<br>`ARINC-615A-3 6.4.4 p.72` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-FILE-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 1 个字段位置编码 FIELD-FILE-LENGTH，位宽为 32 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00310` | `SU-ARINC-615A-3-TABLE-6_4_4-1-R003`<br>`ARINC-615A-3 6.4.4 p.72` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PROTOCOL-VERSION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 2 个字段位置编码 FIELD-PROTOCOL-VERSION，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00311` | `SU-ARINC-615A-3-TABLE-6_4_4-1-R004`<br>`ARINC-615A-3 6.4.4 p.72` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-NUMBER-OF-HEADER-FILES` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 3 个字段位置编码 FIELD-NUMBER-OF-HEADER-FILES，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00312` | `SU-ARINC-615A-3-TABLE-6_4_4-1-R005`<br>`ARINC-615A-3 6.4.4 p.72` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-HEADER-FILE-NAME-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 4 个字段位置编码 FIELD-HEADER-FILE-NAME-LENGTH，位宽为 8 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00313` | `SU-ARINC-615A-3-TABLE-6_4_4-1-R006`<br>`ARINC-615A-3 6.4.4 p.72` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-HEADER-FILE-NAME` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 5 个字段位置编码 FIELD-HEADER-FILE-NAME，位宽为 8..2040 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00314` | `SU-ARINC-615A-3-TABLE-6_4_4-1-R007`<br>`ARINC-615A-3 6.4.4 p.72` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-PART-NUMBER-NAME-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 6 个字段位置编码 FIELD-LOAD-PART-NUMBER-NAME-LENGTH，位宽为 8 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00315` | `SU-ARINC-615A-3-TABLE-6_4_4-1-R008`<br>`ARINC-615A-3 6.4.4 p.72` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-PART-NUMBER-NAME` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 7 个字段位置编码 FIELD-LOAD-PART-NUMBER-NAME，位宽为 8..2040 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00316` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R002`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-FILE-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 1 个字段位置编码 FIELD-FILE-LENGTH，位宽为 32 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00317` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R003`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-PROTOCOL-VERSION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 2 个字段位置编码 FIELD-PROTOCOL-VERSION，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00318` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R004`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-UPLOAD-OPERATION-STATUS-CODE` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 3 个字段位置编码 FIELD-UPLOAD-OPERATION-STATUS-CODE，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00319` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R005`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-UPLOAD-STATUS-DESCRIPTION-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 4 个字段位置编码 FIELD-UPLOAD-STATUS-DESCRIPTION-LENGTH，位宽为 8 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00320` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R006`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-UPLOAD-STATUS-DESCRIPTION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 5 个字段位置编码 FIELD-UPLOAD-STATUS-DESCRIPTION，位宽为 0..2040 bit，重复范围为 ONCE；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00321` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R007`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-COUNTER` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 6 个字段位置编码 FIELD-COUNTER，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00322` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R008`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-EXCEPTION-TIMER` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 7 个字段位置编码 FIELD-EXCEPTION-TIMER，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | `MESSAGE-CARRIED-PARAMETER` / `MESSAGE-TIMER-VALUE` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `UNRESOLVED..UNRESOLVED s` / 证据：SU-ARINC-615A-3-6-4-3-P084-PROSE-SENTENCE-027-B0D6862E1D67, SU-ARINC-615A-3-TABLE-6_4_3-1-R006 | — |
| `CRS-M1-00323` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R009`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-ESTIMATED-TIME` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 8 个字段位置编码 FIELD-ESTIMATED-TIME，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00324` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R010`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-LIST-RATIO` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 9 个字段位置编码 FIELD-LOAD-LIST-RATIO，位宽为 24 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00325` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R011`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-NUMBER-OF-HEADER-FILES` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 10 个字段位置编码 FIELD-NUMBER-OF-HEADER-FILES，位宽为 16 bit，重复范围为 ONCE；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00326` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R012`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-HEADER-FILE-NAME-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 11 个字段位置编码 FIELD-HEADER-FILE-NAME-LENGTH，位宽为 8 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00327` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R013`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-HEADER-FILE-NAME` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 12 个字段位置编码 FIELD-HEADER-FILE-NAME，位宽为 8..2040 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00328` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R014`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-PART-NUMBER-NAME-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 13 个字段位置编码 FIELD-LOAD-PART-NUMBER-NAME-LENGTH，位宽为 8 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00329` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R015`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-PART-NUMBER-NAME` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 14 个字段位置编码 FIELD-LOAD-PART-NUMBER-NAME，位宽为 8..2040 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00330` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R016`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-RATIO` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 15 个字段位置编码 FIELD-LOAD-RATIO，位宽为 24 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00331` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R017`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-STATUS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 16 个字段位置编码 FIELD-LOAD-STATUS，位宽为 16 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00332` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R018`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-STATUS-DESCRIPTION-LENGTH` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 17 个字段位置编码 FIELD-LOAD-STATUS-DESCRIPTION-LENGTH，位宽为 8 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 NOT-APPLICABLE-OR-PROSE-DEFINED。 | — | — |
| `CRS-M1-00333` | `SU-ARINC-615A-3-TABLE-6_4_5-1-R019`<br>`ARINC-615A-3 6.4.5 p.74` | `PROTOCOL-FILE-PRODUCER` / `TABLE-DEFINED-FILE-STRUCTURE` / `ENCODE` / `FIELD-LOAD-STATUS-DESCRIPTION` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 协议文件生成方必须在第 18 个字段位置编码 FIELD-LOAD-STATUS-DESCRIPTION，位宽为 0..2040 bit，重复范围为 PER-PRECEDING-COUNT-FIELD；终止规则为 ZERO-TERMINATED-PER-SECTION-6.4。 | — | — |
| `CRS-M1-00334` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R001`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X0001-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X0001` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“WHEN-STATUS-CODE-0X0001-IS-RECEIVED”下必须对“STATUS-CODE-0X0001”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00335` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R002`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X1000-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X1000` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“WHEN-STATUS-CODE-0X1000-IS-RECEIVED”下必须对“STATUS-CODE-0X1000”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00336` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R003`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X1002-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X1002` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“WHEN-STATUS-CODE-0X1002-IS-RECEIVED”下必须对“STATUS-CODE-0X1002”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00337` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R004`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X0002-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X0002` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“WHEN-STATUS-CODE-0X0002-IS-RECEIVED”下必须对“STATUS-CODE-0X0002”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00338` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R005`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X0003-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X0003` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“WHEN-STATUS-CODE-0X0003-IS-RECEIVED”下必须对“STATUS-CODE-0X0003”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00339` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R006`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X0004-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X0004` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“WHEN-STATUS-CODE-0X0004-IS-RECEIVED”下必须对“STATUS-CODE-0X0004”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00340` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R007`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X1003-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X1003` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“WHEN-STATUS-CODE-0X1003-IS-RECEIVED”下必须对“STATUS-CODE-0X1003”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00341` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R008`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X1004-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X1004` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“WHEN-STATUS-CODE-0X1004-IS-RECEIVED”下必须对“STATUS-CODE-0X1004”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00342` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R009`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X1005-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X1005` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“WHEN-STATUS-CODE-0X1005-IS-RECEIVED”下必须对“STATUS-CODE-0X1005”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00343` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R010`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X1007-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X1007` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“WHEN-STATUS-CODE-0X1007-IS-RECEIVED”下必须对“STATUS-CODE-0X1007”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00344` | `SU-ARINC-615A-3-TABLE-6_4_10-1-R011`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER` / `WHEN-STATUS-CODE-0X1007-IS-RECEIVED` / `INTERPRET-AND-DISPLAY-STATUS` / `STATUS-CODE-0X1007` / `STATUS-MEANING-AND-DISPLAY-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器”在“WHEN-STATUS-CODE-0X1007-IS-RECEIVED”下必须对“STATUS-CODE-0X1007”执行“INTERPRET-AND-DISPLAY-STATUS”；证据是“STATUS-MEANING-AND-DISPLAY-OBSERVABLE”。 | — | — |
| `CRS-M1-00345` | `SU-ARINC-615A-3-TABLE-6_4_10-1-FOOTNOTE-001`<br>`ARINC-615A-3 6.4.10 p.85` | `DATA-LOADER-DISPLAY` / `WHEN-RENDERING-TABLE-6.4.10-STATUS` / `SUBSTITUTE-OPERATION-NAME` / `STATUS-DISPLAY-TEXT` / `DISPLAY-TEXT-OBSERVABLE` | `TABLE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“DATA-LOADER-DISPLAY”在“WHEN-RENDERING-TABLE-6.4.10-STATUS”下必须对“STATUS-DISPLAY-TEXT”执行“SUBSTITUTE-OPERATION-NAME”；证据是“DISPLAY-TEXT-OBSERVABLE”。 | — | — |
| `CRS-M1-00346` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E001-6BBD8FA395EF`<br>`ARINC-615A-3 6.3.1 p.50` | `DLA` / `OPERATION-START` / `RECEIVE` / `TH-INFORMATION-INITIALIZATION` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“OPERATION-START”下必须对“TH-INFORMATION-INITIALIZATION”执行“接收”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00347` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E002-C4C83C8F67F8`<br>`ARINC-615A-3 6.3.1 p.50` | `DLA` / `INITIALIZATION` / `SEND-TFTP-READ-REQUEST` / `LCI` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“INITIALIZATION”下必须对“LCI”执行“SEND-TFTP-READ-REQUEST”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00348` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E003-86B1F4D69CC7`<br>`ARINC-615A-3 6.3.1 p.50` | `TARGET-HARDWARE` / `READ-REQUEST-ACCEPTED` / `TRANSFER` / `LCI` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“READ-REQUEST-ACCEPTED”下必须对“LCI”执行“传输”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00349` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E004-7D245D52CBFE`<br>`ARINC-615A-3 6.3.1 p.50` | `DLA` / `LCI-ANALYSED` / `SEND` / `INFORMATION-INITIALIZATION-RESPONSE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“LCI-ANALYSED”下必须对“INFORMATION-INITIALIZATION-RESPONSE”执行“发送”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00350` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E005-432DDCB05AC3`<br>`ARINC-615A-3 6.3.1 p.50` | `DLA` / `INITIALIZATION-REJECTED` / `TERMINATE` / `INFORMATION-OPERATION` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“INITIALIZATION-REJECTED”下必须对“INFORMATION-OPERATION”执行“TERMINATE”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00351` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E006-ACD86B335E4E`<br>`ARINC-615A-3 6.3.1 p.50` | `TARGET-HARDWARE` / `INITIALIZATION-ACCEPTED` / `SEND-TFTP-WRITE-REQUEST` / `LCL` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“INITIALIZATION-ACCEPTED”下必须对“LCL”执行“SEND-TFTP-WRITE-REQUEST”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00352` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E007-BABEAA841AA6`<br>`ARINC-615A-3 6.3.1 p.50` | `DLA` / `REQUEST-RECEIVED` / `ACKNOWLEDGE` / `LCL-WRITE-REQUEST` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“REQUEST-RECEIVED”下必须对“LCL-WRITE-REQUEST”执行“确认”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00353` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E008-C31F4710028B`<br>`ARINC-615A-3 6.3.1 p.50` | `TARGET-HARDWARE` / `ACKNOWLEDGED` / `TRANSFER` / `LCL` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“ACKNOWLEDGED”下必须对“LCL”执行“传输”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00354` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E009-CA2FDC811E4A`<br>`ARINC-615A-3 6.3.1 p.50` | `DLA` / `LCL-RECEIVED` / `SEND` / `TH-INFORMATION` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“LCL-RECEIVED”下必须对“TH-INFORMATION”执行“发送”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00355` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E010-B9802EF2D3EA`<br>`ARINC-615A-3 6.3.1 p.50` | `TARGET-HARDWARE` / `STATUS-UPDATE-DUE` / `SEND-TFTP-WRITE-REQUEST` / `LCS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“STATUS-UPDATE-DUE”下必须对“LCS”执行“SEND-TFTP-WRITE-REQUEST”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00356` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E011-1AC058091969`<br>`ARINC-615A-3 6.3.1 p.50` | `TARGET-HARDWARE` / `WRITE-REQUEST-ACKNOWLEDGED` / `TRANSFER` / `LCS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“WRITE-REQUEST-ACKNOWLEDGED”下必须对“LCS”执行“传输”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00357` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E012-641E73AF20EF`<br>`ARINC-615A-3 6.3.1 p.50` | `DLA` / `LCS-RECEIVED` / `SEND` / `INFORMATION-STATUS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“LCS-RECEIVED”下必须对“INFORMATION-STATUS”执行“发送”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00358` | `SU-ARINC-615A-3-SECTION-6-3-1-SEQUENCE-CHART-E013-73850A1986EF`<br>`ARINC-615A-3 6.3.1 p.50` | `TARGET-HARDWARE` / `OPERATION-COMPLETION-STATE` / `REPEAT-OR-TERMINATE` / `LCS-STATUS-CYCLE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“OPERATION-COMPLETION-STATE”下必须对“LCS-STATUS-CYCLE”执行“REPEAT-OR-TERMINATE”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00359` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E001-C4F05B5E63B6`<br>`ARINC-615A-3 6.3.2 p.53` | `DLA` / `OPERATION-START` / `RECEIVE` / `TH-UPLOADING-INITIALIZATION` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“数据加载器应用层”在“OPERATION-START”下必须对“TH-UPLOADING-INITIALIZATION”执行“接收”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00360` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E002-77866A816D15`<br>`ARINC-615A-3 6.3.2 p.53` | `DLA` / `INITIALIZATION` / `SEND-TFTP-READ-REQUEST` / `LUI` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“数据加载器应用层”在“INITIALIZATION”下必须对“LUI”执行“SEND-TFTP-READ-REQUEST”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00361` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E003-23D0F1A6F303`<br>`ARINC-615A-3 6.3.2 p.53` | `TARGET-HARDWARE` / `READ-REQUEST-ACCEPTED` / `TRANSFER` / `LUI` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“目标硬件”在“READ-REQUEST-ACCEPTED”下必须对“LUI”执行“传输”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00362` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E004-30A7E36B1CAC`<br>`ARINC-615A-3 6.3.2 p.53` | `DLA` / `LUI-ANALYSED` / `SEND` / `UPLOADING-INITIALIZATION-RESPONSE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“数据加载器应用层”在“LUI-ANALYSED”下必须对“UPLOADING-INITIALIZATION-RESPONSE”执行“发送”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00363` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E005-1CC34400D27E`<br>`ARINC-615A-3 6.3.2 p.53` | `DLA` / `INITIALIZATION-ACCEPTED` / `SEND` / `LOAD-LIST` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“数据加载器应用层”在“INITIALIZATION-ACCEPTED”下必须对“LOAD-LIST”执行“发送”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00364` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E006-298771587D83`<br>`ARINC-615A-3 6.3.2 p.53` | `DLA` / `LIST-NOT-YET-ACCEPTED` / `WAIT` / `LUS-0001` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“数据加载器应用层”在“LIST-NOT-YET-ACCEPTED”下必须对“LUS-0001”执行“等待”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00365` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E007-7726A816FFE7`<br>`ARINC-615A-3 6.3.2 p.53` | `DATA-LOADER` / `LIST-ACCEPTED` / `SEND-TFTP-WRITE-REQUEST` / `LUR` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“数据加载器”在“LIST-ACCEPTED”下必须对“LUR”执行“SEND-TFTP-WRITE-REQUEST”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00366` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E008-F1D3B51077A3`<br>`ARINC-615A-3 6.3.2 p.53` | `TARGET-HARDWARE` / `REQUEST-RECEIVED` / `ACKNOWLEDGE` / `LUR-WRITE-REQUEST` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“目标硬件”在“REQUEST-RECEIVED”下必须对“LUR-WRITE-REQUEST”执行“确认”，接收方为“数据加载器”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00367` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-A-E009-9A7CD75981CB`<br>`ARINC-615A-3 6.3.2 p.53` | `DATA-LOADER` / `ACKNOWLEDGED` / `TRANSFER` / `LUR` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“数据加载器”在“ACKNOWLEDGED”下必须对“LUR”执行“传输”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00368` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E001-0056C38BAE97`<br>`ARINC-615A-3 6.3.2 p.54` | `TARGET-HARDWARE` / `FILE-SELECTED` / `SEND-TFTP-READ-REQUEST` / `REQUESTED-UPLOAD-FILE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“目标硬件”在“FILE-SELECTED”下必须对“REQUESTED-UPLOAD-FILE”执行“SEND-TFTP-READ-REQUEST”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00369` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E002-9E4B69ABC6C0`<br>`ARINC-615A-3 6.3.2 p.54` | `DLA` / `REQUESTED-FILE-UNAVAILABLE` / `SEND` / `FILE-NOT-AVAILABLE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“数据加载器应用层”在“REQUESTED-FILE-UNAVAILABLE”下必须对“FILE-NOT-AVAILABLE”执行“发送”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00370` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E003-4CF8C989BD2D`<br>`ARINC-615A-3 6.3.2 p.54` | `DLA` / `REQUESTED-FILE-AVAILABLE` / `TRANSFER` / `REQUESTED-UPLOAD-FILE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“数据加载器应用层”在“REQUESTED-FILE-AVAILABLE”下必须对“REQUESTED-UPLOAD-FILE”执行“传输”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00371` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E004-FA670B42C1F5`<br>`ARINC-615A-3 6.3.2 p.54` | `TARGET-HARDWARE` / `FILE-RECEIVED` / `WRITE` / `LUS-FILE-STATUS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“目标硬件”在“FILE-RECEIVED”下必须对“LUS-FILE-STATUS”执行“WRITE”，接收方为“TARGET-MEMORY”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00372` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E005-B45D394BBCF7`<br>`ARINC-615A-3 6.3.2 p.54` | `TARGET-HARDWARE` / `MORE-FILES-REQUIRED` / `REPEAT` / `UPLOAD-FILE-THREAD` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“目标硬件”在“MORE-FILES-REQUIRED”下必须对“UPLOAD-FILE-THREAD”执行“REPEAT”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00373` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E006-5AECD60FFEA3`<br>`ARINC-615A-3 6.3.2 p.54` | `TARGET-HARDWARE` / `STATUS-UPDATE-DUE` / `SEND-TFTP-WRITE-REQUEST` / `LUS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“目标硬件”在“STATUS-UPDATE-DUE”下必须对“LUS”执行“SEND-TFTP-WRITE-REQUEST”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00374` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E007-1C729672C57C`<br>`ARINC-615A-3 6.3.2 p.54` | `TARGET-HARDWARE` / `WRITE-REQUEST-ACKNOWLEDGED` / `TRANSFER` / `LUS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“目标硬件”在“WRITE-REQUEST-ACKNOWLEDGED”下必须对“LUS”执行“传输”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00375` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E008-772971415EE7`<br>`ARINC-615A-3 6.3.2 p.54` | `DLA` / `LUS-RECEIVED` / `SEND` / `UPLOAD-INFORMATION-STATUS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“数据加载器应用层”在“LUS-RECEIVED”下必须对“UPLOAD-INFORMATION-STATUS”执行“发送”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00376` | `SU-ARINC-615A-3-SECTION-6-3-2-SEQUENCE-CHART-B-E009-0243DF6FD28F`<br>`ARINC-615A-3 6.3.2 p.54` | `DLA` / `UPLOAD-COMPLETION-STATE` / `REPEAT-OR-TERMINATE` / `UPLOAD-STATUS-CYCLE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-BASE` | 参与者“数据加载器应用层”在“UPLOAD-COMPLETION-STATE”下必须对“UPLOAD-STATUS-CYCLE”执行“REPEAT-OR-TERMINATE”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00377` | `SU-ARINC-615A-3-SECTION-6-3-5-SEQUENCE-CHART-E001-9F14C8F561CB`<br>`ARINC-615A-3 6.3.5 p.63` | `DLA` / `INTERRUPTION-START` / `RECEIVE` / `ABORT-REQUEST` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“INTERRUPTION-START”下必须对“ABORT-REQUEST”执行“接收”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00378` | `SU-ARINC-615A-3-SECTION-6-3-5-SEQUENCE-CHART-E002-ADCFF3068CA9`<br>`ARINC-615A-3 6.3.5 p.63` | `DLA` / `ABORT-REQUESTED` / `WAIT` / `STATUS-FILE-WRITE-REQUEST` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“ABORT-REQUESTED”下必须对“STATUS-FILE-WRITE-REQUEST”执行“等待”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00379` | `SU-ARINC-615A-3-SECTION-6-3-5-SEQUENCE-CHART-E003-F48598C39EB0`<br>`ARINC-615A-3 6.3.5 p.63` | `TARGET-HARDWARE` / `STATUS-AVAILABLE` / `SEND-TFTP-WRITE-REQUEST` / `LCS-LUS-OR-LNS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“STATUS-AVAILABLE”下必须对“LCS-LUS-OR-LNS”执行“SEND-TFTP-WRITE-REQUEST”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00380` | `SU-ARINC-615A-3-SECTION-6-3-5-SEQUENCE-CHART-E004-CE12F9C3643D`<br>`ARINC-615A-3 6.3.5 p.63` | `DLA` / `WRITE-REQUEST-RECEIVED` / `SEND` / `ABORT-ERROR` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“WRITE-REQUEST-RECEIVED”下必须对“ABORT-ERROR”执行“发送”，接收方为“目标硬件”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00381` | `SU-ARINC-615A-3-SECTION-6-3-5-SEQUENCE-CHART-E005-62BABD65DCA2`<br>`ARINC-615A-3 6.3.5 p.63` | `TARGET-HARDWARE` / `ABORT-ERROR-RECEIVED` / `STOP` / `NONSTATUS-FILE-TRANSFERS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“ABORT-ERROR-RECEIVED”下必须对“NONSTATUS-FILE-TRANSFERS”执行“STOP”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00382` | `SU-ARINC-615A-3-SECTION-6-3-5-SEQUENCE-CHART-E006-697ED629B1F1`<br>`ARINC-615A-3 6.3.5 p.63` | `TARGET-HARDWARE` / `ACTIVITIES-STOPPED` / `TRANSFER` / `ABORT-CONFIRMATION-STATUS-FILE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“目标硬件”在“ACTIVITIES-STOPPED”下必须对“ABORT-CONFIRMATION-STATUS-FILE”执行“传输”，接收方为“数据加载器应用层”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00383` | `SU-ARINC-615A-3-SECTION-6-3-5-SEQUENCE-CHART-E007-0E8514BE5C06`<br>`ARINC-615A-3 6.3.5 p.63` | `DLA` / `ABORT-STATUS-RECEIVED` / `SEND` / `INFORMATION-OR-UPLOAD-OR-DOWNLOAD-STATUS` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“ABORT-STATUS-RECEIVED”下必须对“INFORMATION-OR-UPLOAD-OR-DOWNLOAD-STATUS”执行“发送”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00384` | `SU-ARINC-615A-3-SECTION-6-3-5-SEQUENCE-CHART-E008-F805E5E804BC`<br>`ARINC-615A-3 6.3.5 p.63` | `DLA` / `ABORT-CONFIRMED` / `TERMINATE` / `INTERRUPTION-MODE` / `ORDER-DIRECTION-BRANCH-OBSERVABLE` | `FIGURE-CONSTRAINT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 参与者“数据加载器应用层”在“ABORT-CONFIRMED”下必须对“INTERRUPTION-MODE”执行“TERMINATE”，接收方为“APPLICATION”；证据是“ORDER-DIRECTION-BRANCH-OBSERVABLE”。 | — | — |
| `CRS-M1-00385` | `SU-ARINC-615A-3-5-3-3-P044-PROSE-SENTENCE-005-36878C1F8E7E`<br>`ARINC-615A-3 5.3.3 p.32` | `FIND-PROTOCOL` / `WHEN-FIND-IMPLEMENTED` / `USE-UDP-PORT-1001` / `UDP-PORT-1001` / `FIND-PORT-1001-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 在实现 FIND 发起方或 FIND 主机时，FIND 必须使用十进制 UDP 端口 1001。 | — | — |
| `CRS-M1-00386` | `SU-ARINC-615A-3-3-1-P107-PROSE-SENTENCE-006-B1ED10DE43C7`<br>`ARINC-615A-3 3-1 p.95` | `DATA-LOADER` / `WHEN-FIND-PATH-CARRIES-TRAFFIC-AND-BEFORE-DATA-LOAD` / `RUN-FIND-AT-LEAST-ONCE` / `FIND-REQUEST` / `FIND-PRELOAD-RUN-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在路径能够承载 FIND 业务时，数据加载器必须在数据加载操作前至少运行一次 FIND。 | — | — |
| `CRS-M1-00387` | `SU-ARINC-615A-3-3-1-P107-PROSE-SENTENCE-007-9166DCC81508`<br>`ARINC-615A-3 3-1 p.95` | `DATA-LOADER` / `WHEN-FIND-PATH-CARRIES-TRAFFIC-AND-BEFORE-LATER-OPERATION` / `MAY-RERUN-FIND-AND-REGISTER-ANSWERS` / `FIND-REQUEST, FIND-ANSWER` / `FIND-OPTIONAL-RERUN-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | 在能够承载 FIND 的路径上，数据加载器可以在后续每次操作前再次运行 FIND 并登记应答。 | — | — |
| `CRS-M1-00388` | `SU-ARINC-615A-3-3-1-P107-PROSE-SENTENCE-011-AD843D1C9EDF`<br>`ARINC-615A-3 3-1 p.95` | `FIND-PROTOCOL` / `WHEN-FIND-IMPLEMENTED` / `USE-WELL-KNOWN-UDP-PORT-1001` / `UDP-PORT-1001` / `FIND-ATTACHMENT-PORT-1001-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | FIND 请求与应答分组必须使用众所周知的十进制 UDP 端口 1001。 | — | — |
| `CRS-M1-00389` | `SU-ARINC-615A-3-3-1-P107-PROSE-SENTENCE-012-AEB96A80314F`<br>`ARINC-615A-3 3-1 p.95` | `FIND-PROTOCOL` / `WHEN-FIND-IMPLEMENTED` / `USE-SAME-PORT-FOR-REQUEST-AND-ANSWER` / `FIND-REQUEST, FIND-ANSWER, UDP-PORT-1001` / `FIND-SHARED-PORT-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | FIND 请求分组与 FIND 应答分组必须使用同一 UDP 端口号。 | — | — |
| `CRS-M1-00390` | `SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-003-1E8680AD6287`<br>`ARINC-615A-3 3-2 p.96` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `REGISTER-VALID-FIND-ANSWERS-AS-LOAD-TARGETS` / `VALID-FIND-ANSWERS, LOAD-TARGET-REGISTRATION` / `VALID-FIND-ANSWER-REGISTRATION-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 在实现 FIND 时，数据加载器必须把所有有效 FIND 应答登记为可能的加载目标。 | — | — |
| `CRS-M1-00391` | `SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-005-3CE166EDA700`<br>`ARINC-615A-3 3-2 p.96` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `ANSWER-FIND-REQUEST-WITHIN-TWO-SECOND-UPPER-BOUND` / `FIND-ANSWER, FIND-HOST-TIMEOUT-UPPER-BOUND-2-S` / `FIND-HOST-ANSWER-WITHIN-TWO-SECOND-UPPER-BOUND-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 在实现 FIND 时，FIND 主机必须在收到合法请求后的两秒上界内发出 FIND 应答。更早的应答满足该期限；三秒登记窗口不能延长该主机上界。 | `FIXED-SOURCE-CONSTANT` / `FIND-HOST-TIMEOUT-2-S` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `0..2 s` / 证据：SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-005-3CE166EDA700 | — |
| `CRS-M1-00392` | `SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-006-E98F49FBFBDF`<br>`ARINC-615A-3 3-2 p.96` | `FIND-INITIATOR` / `WHEN-FIND-IMPLEMENTED` / `TAKE-NEEDED-INFORMATION-FROM-MESSAGE-STRUCTURE-OR-FIND-PACKET-DATA` / `MESSAGE-STRUCTURE, FIND-PACKET-DATA` / `FIND-INFORMATION-LOCATION-ALTERNATIVE-OBSERVABLE` | `MAY` / `CONDITIONAL-REQUIRED` | `APPLICABLE-SUPPORTING` | 在实现 FIND 时，发起方必须从报文结构或 FIND 分组数据中取得所需信息。这记录两种承载位置，不激活 AFDX，也不允许省略所需信息。 | — | — |
| `CRS-M1-00393` | `SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-010-76E6AE59C360`<br>`ARINC-615A-3 3-2 p.96` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `SEND-NO-ANSWER-TO-ILLEGAL-FIND-REQUEST` / `ILLEGAL-FIND-REQUEST` / `FIND-ILLEGAL-REQUEST-SILENCE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 对于非法或无效的 FIND 请求，FIND 主机不得发出应答。 | — | — |
| `CRS-M1-00394` | `SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-011-A1CA1EF64C11`<br>`ARINC-615A-3 3-2 p.96` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `IGNORE-INVALID-FIND-ANSWER` / `INVALID-FIND-ANSWER` / `FIND-INVALID-ANSWER-IGNORE-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 数据加载器必须忽略无效的 FIND 应答。 | — | — |
| `CRS-M1-00395` | `SU-ARINC-615A-3-3-4-P108-PROSE-SENTENCE-001-DB0FEBBE9664`<br>`ARINC-615A-3 3-4 p.96` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `SET-IRQ-SOURCE-MAC-TO-DATA-LOADER` / `IRQ-SOURCE-MAC` / `IRQ-SOURCE-MAC-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 在信息请求中，数据加载器必须把源 MAC 地址设为自己的 MAC 地址。 | — | — |
| `CRS-M1-00396` | `SU-ARINC-615A-3-3-4-P108-PROSE-SENTENCE-002-412B0FD7B45D`<br>`ARINC-615A-3 3-4 p.96` | `DATA-LOADER` / `WHEN-FIND-PATH-CARRIES-TRAFFIC` / `SET-IRQ-DESTINATION-MAC-TO-UNICAST-MULTICAST-OR-BROADCAST` / `IRQ-DESTINATION-MAC` / `IRQ-DESTINATION-MAC-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在路径能够承载 FIND 时，数据加载器必须把信息请求的目的 MAC 设为单播、组播或广播 MAC。 | — | — |
| `CRS-M1-00397` | `SU-ARINC-615A-3-ATTACHMENT-3-P109-PROSE-SENTENCE-003-B443A5630F89`<br>`ARINC-615A-3 ATTACHMENT-3 p.97` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `SET-IRQ-SOURCE-IP-TO-DATA-LOADER` / `IRQ-SOURCE-IP` / `IRQ-SOURCE-IP-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 在信息请求中，数据加载器必须把源 IP 地址设为自己的 IP 地址。 | — | — |
| `CRS-M1-00398` | `SU-ARINC-615A-3-ATTACHMENT-3-P109-PROSE-SENTENCE-004-0BFE8D84B7A9`<br>`ARINC-615A-3 ATTACHMENT-3 p.97` | `DATA-LOADER` / `WHEN-FIND-PATH-CARRIES-TRAFFIC` / `SET-IRQ-DESTINATION-IP-TO-UNICAST-MULTICAST-OR-BROADCAST` / `IRQ-DESTINATION-IP` / `IRQ-DESTINATION-IP-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在路径能够承载 FIND 时，数据加载器必须把信息请求的目的 IP 设为单播、组播或广播 IP，包括有限广播或全 1 广播。 | — | — |
| `CRS-M1-00399` | `SU-ARINC-615A-3-ATTACHMENT-3-P109-PROSE-SENTENCE-005-DC8D7B76A7B9`<br>`ARINC-615A-3 ATTACHMENT-3 p.97` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `SET-IRQ-OPCODE-TO-0001` / `IRQ-OPCODE-0001` / `IRQ-OPCODE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 数据加载器必须把信息请求操作码设为 0x0001。 | — | — |
| `CRS-M1-00400` | `SU-ARINC-615A-3-ATTACHMENT-3-P109-PROSE-SENTENCE-006-FC8DA6118FFF`<br>`ARINC-615A-3 ATTACHMENT-3 p.97` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `SET-IRQ-DATA-LIST-TO-ASCII-NUL` / `IRQ-DATA-LIST, ASCII-NUL` / `IRQ-DATA-LIST-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 数据加载器必须把信息请求数据表设为单个 ASCII 空字符终止符。 | — | — |
| `CRS-M1-00401` | `SU-ARINC-615A-3-ATTACHMENT-3-P109-PROSE-SENTENCE-007-99F468D5D311`<br>`ARINC-615A-3 ATTACHMENT-3 p.97` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `TERMINATE-IRQ-PACKET-WITH-DLE` / `IRQ-PACKET-TERMINATOR-DLE` / `IRQ-TERMINATOR-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 数据加载器必须以 0x10 结束信息请求分组。 | — | — |
| `CRS-M1-00402` | `SU-ARINC-615A-3-3-5-P109-PROSE-SENTENCE-001-D2A70FEFE065`<br>`ARINC-615A-3 3-5 p.97` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `SET-IAN-SOURCE-MAC-TO-FIND-HOST` / `IAN-SOURCE-MAC` / `IAN-SOURCE-MAC-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 在信息应答中，FIND 主机必须把源 MAC 地址设为目标硬件 MAC 地址。 | — | — |
| `CRS-M1-00403` | `SU-ARINC-615A-3-3-5-P109-PROSE-SENTENCE-002-21D8C06816D1`<br>`ARINC-615A-3 3-5 p.97` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `SET-IAN-DESTINATION-MAC-TO-ASSOCIATED-IRQ-SOURCE-MAC` / `IAN-DESTINATION-MAC` / `IAN-DESTINATION-MAC-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | FIND 主机必须把信息应答的目的 MAC 设为对应信息请求的源 MAC。 | — | — |
| `CRS-M1-00404` | `SU-ARINC-615A-3-3-5-P109-PROSE-SENTENCE-003-E5DBDB9636E9`<br>`ARINC-615A-3 3-5 p.97` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `SET-IAN-SOURCE-IP-TO-FIND-HOST` / `IAN-SOURCE-IP` / `IAN-SOURCE-IP-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 在信息应答中，FIND 主机必须把源 IP 地址设为目标硬件 IP 地址。 | — | — |
| `CRS-M1-00405` | `SU-ARINC-615A-3-3-5-P109-PROSE-SENTENCE-004-98DCC47DCB2B`<br>`ARINC-615A-3 3-5 p.97` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `SET-IAN-DESTINATION-IP-TO-ASSOCIATED-IRQ-SOURCE-IP` / `IAN-DESTINATION-IP` / `IAN-DESTINATION-IP-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | FIND 主机必须把信息应答的目的 IP 设为对应信息请求的源 IP。 | — | — |
| `CRS-M1-00406` | `SU-ARINC-615A-3-3-5-P109-PROSE-SENTENCE-005-4D7FB8BC839C`<br>`ARINC-615A-3 3-5 p.97` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `SET-IAN-OPCODE-TO-0002` / `IAN-OPCODE-0002` / `IAN-OPCODE-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | FIND 主机必须把信息应答操作码设为 0x0002。 | — | — |
| `CRS-M1-00407` | `SU-ARINC-615A-3-3-5-P109-PROSE-SENTENCE-007-0F2D63CA1D3E`<br>`ARINC-615A-3 3-5 p.97` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `ENCODE-EMPTY-IAN-PARAMETER-AS-SINGLE-NUL` / `EMPTY-IAN-PARAMETER, ASCII-NUL` / `IAN-EMPTY-FIELD-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | FIND 主机必须把空的信息应答参数编码为单个 ASCII 空字节。 | — | — |
| `CRS-M1-00408` | `SU-ARINC-615A-3-3-5-P109-PROSE-SENTENCE-008-D8483D058800`<br>`ARINC-615A-3 3-5 p.97` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `OMIT-EMBEDDED-NUL-FROM-IAN-STRINGS` / `IAN-PARAMETER-STRING` / `IAN-NO-EMBEDDED-NUL-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | FIND 主机必须从已提供的信息应答参数字符串中省略内嵌空字节。 | — | — |
| `CRS-M1-00409` | `SU-ARINC-615A-3-3-5-P109-PROSE-SENTENCE-009-2DD2663EB0A1`<br>`ARINC-615A-3 3-5 p.97` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `TERMINATE-IAN-PACKET-WITH-DLE` / `IAN-PACKET-TERMINATOR-DLE` / `IAN-TERMINATOR-OBSERVABLE` | `SHOULD` / `REQUIRED` | `APPLICABLE-SUPPORTING` | FIND 主机必须以 0x10 结束信息应答分组。 | — | — |
| `CRS-M1-00410` | `SU-ARINC-615A-3-ATTACHMENT-3-P110-PROSE-SENTENCE-012-DB234DB803F9`<br>`ARINC-615A-3 ATTACHMENT-3 p.98` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `ENCODE-IAN-PARAMETERS-AS-NUL-TERMINATED-STRINGS-IN-SECTION-3-6-ORDER` / `IAN-PARAMETER-STRINGS` / `IAN-PARAMETER-ORDER-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | FIND 主机必须按附件 3 第 6 节顺序，把信息应答参数值编码为空字符终止字符串。 | — | — |
| `CRS-M1-00411` | `SU-ARINC-615A-3-ATTACHMENT-3-P110-PROSE-SENTENCE-013-48CB9FF4518D`<br>`ARINC-615A-3 ATTACHMENT-3 p.98` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `LIMIT-TARGET-HARDWARE-IDENTIFIER-TO-15-CHARACTERS-EXCLUDING-TERMINATOR` / `TARGET-HARDWARE-IDENTIFIER, LENGTH-15` / `THW-ID-LENGTH-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | FIND 主机必须把目标硬件标识符限制为不含终止符的 15 个字符。 | — | — |
| `CRS-M1-00412` | `SU-ARINC-615A-3-ATTACHMENT-3-P110-PROSE-SENTENCE-014-913B305AF452`<br>`ARINC-615A-3 ATTACHMENT-3 p.98` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `LIMIT-TARGET-TYPE-NAME-TO-8-CHARACTERS-EXCLUDING-TERMINATOR` / `TARGET-TYPE-NAME, LENGTH-8` / `TARGET-TYPE-NAME-LENGTH-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | FIND 主机必须把目标类型名限制为不含终止符的 8 个字符。 | — | — |
| `CRS-M1-00413` | `SU-ARINC-615A-3-ATTACHMENT-3-P110-PROSE-SENTENCE-015-14EF51A05AEA`<br>`ARINC-615A-3 ATTACHMENT-3 p.98` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `LIMIT-TARGET-POSITION-TO-8-CHARACTERS-EXCLUDING-TERMINATOR` / `TARGET-POSITION, LENGTH-8` / `TARGET-POSITION-LENGTH-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | FIND 主机必须把目标位置限制为不含终止符的 8 个字符。 | — | — |
| `CRS-M1-00414` | `SU-ARINC-615A-3-ATTACHMENT-3-P110-PROSE-SENTENCE-016-22BA44DB74A6`<br>`ARINC-615A-3 ATTACHMENT-3 p.98` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `LIMIT-LITERAL-NAME-TO-20-CHARACTERS-EXCLUDING-TERMINATOR` / `LITERAL-NAME, LENGTH-20` / `LITERAL-NAME-LENGTH-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | FIND 主机必须把字面名限制为不含终止符的 20 个字符。 | — | — |
| `CRS-M1-00415` | `SU-ARINC-615A-3-ATTACHMENT-3-P110-PROSE-SENTENCE-017-4A05E0BB2809`<br>`ARINC-615A-3 ATTACHMENT-3 p.98` | `FIND-HOST` / `WHEN-FIND-IMPLEMENTED` / `ENCODE-MANUFACTURER-CODE-AS-3-CHARACTERS-EXCLUDING-TERMINATOR` / `MANUFACTURER-CODE, LENGTH-3` / `MANUFACTURER-CODE-LENGTH-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | FIND 主机必须把制造商代码编码为不含终止符的 3 个字符。 | — | — |
| `CRS-M1-00416` | `SU-ARINC-615A-3-5-4-4-P050-PROSE-SENTENCE-007-CA89CD0344A9`<br>`ARINC-615A-3 5.4.4 p.38` | `DATA-LOADER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `IMPLEMENT-BOTH-MEDIA-DEFINED-OPERATOR-DEFINED-DOWNLOAD` / `MEDIA-DEFINED, OPERATOR-DEFINED` / `IMPLEMENT-BOTH-MEDIA-DEFINED-OPERATOR-DEFINED-DOWNLOAD-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，数据加载器必须实现 both 媒体定义 and 操作员定义 DOWNLOAD。 | — | — |
| `CRS-M1-00417` | `SU-ARINC-615A-3-5-4-4-P050-PROSE-SENTENCE-008-EB64770DFDD9`<br>`ARINC-615A-3 5.4.4 p.38` | `TARGET-HARDWARE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `IMPLEMENT-NONE-ONE-BOTH-DOWNLOAD-MODES` / `MEDIA-DEFINED, OPERATOR-DEFINED` / `IMPLEMENT-NONE-ONE-BOTH-DOWNLOAD-MODES-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，目标硬件可以实现 none, one, or both DOWNLOAD modes。 | — | — |
| `CRS-M1-00418` | `SU-ARINC-615A-3-5-4-4-P050-PROSE-SENTENCE-009-DD0255D27FB0`<br>`ARINC-615A-3 5.4.4 p.38` | `DATA-LOADER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `SPECIFY-TFTP-OPTIONS-SUPPLY-DATA-INTEGRITY-CHECK-TRANSFER` / `TFTP-OPTIONS` / `SPECIFY-TFTP-OPTIONS-SUPPLY-DATA-INTEGRITY-CHECK-TRANSFER-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，数据加载器可以规定 TFTP options that supply a data-integrity check for the transfer。 | — | — |
| `CRS-M1-00419` | `SU-ARINC-615A-3-5-4-4-P050-PROSE-SENTENCE-010-12B60035E133`<br>`ARINC-615A-3 5.4.4 p.38` | `TARGET-HARDWARE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `IMPLEMENT-TFTP-INTEGRITY-OPTION` / `TFTP-OPTION` / `IMPLEMENT-TFTP-INTEGRITY-OPTION-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，目标硬件可以实现 that TFTP integrity option。 | — | — |
| `CRS-M1-00420` | `SU-ARINC-615A-3-5-4-4-P050-PROSE-SENTENCE-011-3CF28DC21423`<br>`ARINC-615A-3 5.4.4 p.38` | `DATA-LOADER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `IT-SUPPORTS-OFFERED-CHECK-VALUE-VALIDATE-DATA-TRANSFER` / `CHECK-VALUE` / `IT-SUPPORTS-OFFERED-CHECK-VALUE-VALIDATE-DATA-TRANSFER-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，数据加载器必须if it supports the offered check value, 校验 the data transfer。 | — | — |
| `CRS-M1-00421` | `SU-ARINC-615A-3-5-4-4-P050-PROSE-SENTENCE-012-D9C78F1A4E4C`<br>`ARINC-615A-3 5.4.4 p.38` | `DATA-LOADER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `TREAT-CHECKSUM-VALIDATION-INFORMATION-ONLY-STILL-EXPORT-FILE` / `CHECKSUM, EXPORT` / `TREAT-CHECKSUM-VALIDATION-INFORMATION-ONLY-STILL-EXPORT-FILE-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，数据加载器必须把 校验和 validation as information only and still export the file。 | — | — |
| `CRS-M1-00422` | `SU-ARINC-615A-3-5-4-4-1-P050-PROSE-SENTENCE-004-E7A9E12EDE22`<br>`ARINC-615A-3 5.4.4.1 p.38` | `DATA-LOADER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `USE-LNR-ALREADY-STORED-ARINC-665-PART-MEDIA` / `LNR, ARINC-665-PART` / `USE-LNR-ALREADY-STORED-ARINC-665-PART-MEDIA-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，数据加载器可以使用 an LNR already stored in an ARINC 665 part on the media。 | — | — |
| `CRS-M1-00423` | `SU-ARINC-615A-3-5-4-4-1-P050-PROSE-SENTENCE-006-F3361F00DCE2`<br>`ARINC-615A-3 5.4.4.1 p.38` | `DATA-LOADER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `EXAMINE-EACH-PART-HEADER-OFFER-HEADERS-WHOSE-DOWNLOAD-BIT-SET` / `DOWNLOAD-BIT, HEADER-FILE` / `EXAMINE-EACH-PART-HEADER-OFFER-HEADERS-WHOSE-DOWNLOAD-BIT-SE-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，数据加载器必须检查 each part header and 提供 headers whose download bit is set。 | — | — |
| `CRS-M1-00424` | `SU-ARINC-615A-3-5-4-4-1-P050-PROSE-SENTENCE-007-A88849FBE53E`<br>`ARINC-615A-3 5.4.4.1 p.38` | `OPERATOR` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `MORE-THAN-ONE-DOWNLOAD-BIT-HEADER-EXISTS-SELECT-ONE` / `HEADER-FILE` / `MORE-THAN-ONE-DOWNLOAD-BIT-HEADER-EXISTS-SELECT-ONE-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，操作员可以if more than one download-bit header exists, 选择 one。 | — | — |
| `CRS-M1-00426` | `SU-ARINC-615A-3-5-4-4-3-P052-PROSE-SENTENCE-002-1036539E638B`<br>`ARINC-615A-3 5.4.4.3 p.40` | `DATA-LOADER` / `WHEN-REMOVABLE-MEDIA-IS-LNR-SOURCE-AND-DOWNLOAD-DESTINATION` / `PROMPT-OPERATOR-REPLACE-SELECT-WRITABLE-MEDIA-BEFORE-STARTING-DOWNLOAD` / `WRITABLE-MEDIA` / `PROMPT-OPERATOR-REPLACE-SELECT-WRITABLE-MEDIA-BEFORE-STARTIN-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在可移动媒体既是 LNR 来源又是下载数据目的地时，数据加载器必须在开始 DOWNLOAD 前提示操作员更换或选择可写媒体。 | — | — |
| `CRS-M1-00427` | `SU-ARINC-615A-3-5-4-4-3-P052-PROSE-SENTENCE-003-3B9221D5DF13`<br>`ARINC-615A-3 5.4.4.3 p.40` | `DATA-LOADER` / `WHEN-REMOVABLE-MEDIA-IS-LNR-SOURCE-AND-DOWNLOAD-DESTINATION` / `FAIL-DOWNLOAD-WRITE-STILL-FAILS-AFTER-ASKING-WRITABLE-MEDIA` / `WRITABLE-MEDIA` / `FAIL-DOWNLOAD-WRITE-STILL-FAILS-AFTER-ASKING-WRITABLE-MEDIA-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在可移动媒体既是 LNR 来源又是下载数据目的地时，若在要求可写媒体之后写入仍然失败，数据加载器必须使 DOWNLOAD 失败。 | — | — |
| `CRS-M1-00428` | `SU-ARINC-615A-3-5-4-4-3-P052-PROSE-SENTENCE-004-C40353394C94`<br>`ARINC-615A-3 5.4.4.3 p.40` | `DATA-LOADER` / `WHEN-REMOVABLE-MEDIA-IS-LNR-SOURCE-AND-DOWNLOAD-DESTINATION` / `CREATE-NEW-DNLD-DATA-THW-ID-POS-NUMBER-DIRECTORY-EACH` / `DNLD-DATA` / `CREATE-NEW-DNLD-DATA-THW-ID-POS-NUMBER-DIRECTORY-EACH-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在可移动媒体既是 LNR 来源又是下载数据目的地时，数据加载器必须为每次下载新建 DNLD_DATA_<THW_ID_POS>_<number> 目录。 | — | — |
| `CRS-M1-00429` | `SU-ARINC-615A-3-5-4-4-3-P052-PROSE-SENTENCE-008-4B56712D118C`<br>`ARINC-615A-3 5.4.4.3 p.40` | `DATA-LOADER` / `WHEN-REMOVABLE-MEDIA-IS-LNR-SOURCE-AND-DOWNLOAD-DESTINATION` / `CREATE-DNLD-INFO-THW-ID-POS-NUMBER-MANUFACTURER-SPECIFIC-DOWNLOAD` / `DNLD-INFO` / `CREATE-DNLD-INFO-THW-ID-POS-NUMBER-MANUFACTURER-SPECIFIC-DOW-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | 在可移动媒体既是 LNR 来源又是下载数据目的地时，数据加载器可以为制造商专用下载信息创建 DNLD_INFO_<THW_ID_POS>_<number> 文件。 | — | — |
| `CRS-M1-00430` | `SU-ARINC-615A-3-6-3-3-P070-PROSE-SENTENCE-033-EC6A3B3AFA4A`<br>`ARINC-615A-3 6.3.3 p.58` | `OPERATOR` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `SELECT-MEDIA-TYPE-MEDIA-DEFINED-DOWNLOAD` / `MEDIA-TYPE` / `SELECT-MEDIA-TYPE-MEDIA-DEFINED-DOWNLOAD-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，操作员必须选择 the media type for 媒体定义 DOWNLOAD。 | — | — |
| `CRS-M1-00431` | `SU-ARINC-615A-3-6-3-3-P070-PROSE-SENTENCE-038-2ED4ABAC4193`<br>`ARINC-615A-3 6.3.3 p.58` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `SEND-STATUS-FILES-WITHIN-ATTACHMENT-4-DLP-MAXIMUM-DELAY` / `LNS, ATTACHMENT-4` / `SEND-STATUS-FILES-WITHIN-ATTACHMENT-4-DLP-MAXIMUM-DELAY-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须发送 状态文件s within the 附件 4 DLP maximum delay。 | — | — |
| `CRS-M1-00432` | `SU-ARINC-615A-3-6-3-3-P070-PROSE-SENTENCE-040-18B50A8E503C`<br>`ARINC-615A-3 6.3.3 p.58` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `FATAL-ERROR-EMIT-STATUS-FILE-MATCHING-CODE-DESCRIPTION-INSIDE-TIMEOUT` / `LNS, STATUS-CODE, STATUS-DESCRIPTION` / `FATAL-ERROR-EMIT-STATUS-FILE-MATCHING-CODE-DESCRIPTION-INSID-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须on fatal error emit a 状态文件 with matching code and description inside the timeout。 | — | — |
| `CRS-M1-00433` | `SU-ARINC-615A-3-6-3-3-P070-PROSE-SENTENCE-041-7AC0400C9DB1`<br>`ARINC-615A-3 6.3.3 p.58` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `SEND-STATUS-FILE-IMMEDIATELY-CARRY-ABORT-INTERRUPT` / `ABORT-5-3-2-3-6, INTERRUPT-6-3-6` / `SEND-STATUS-FILE-IMMEDIATELY-CARRY-ABORT-INTERRUPT-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，目标硬件可以发送 a 状态文件 immediately to carry an 中止 or interrupt。 | — | — |
| `CRS-M1-00434` | `SU-ARINC-615A-3-6-3-3-P070-PROSE-SENTENCE-050-D8862D88C46E`<br>`ARINC-615A-3 6.3.3 p.58` | `DATA-LOADER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `TARGET-ANSWERS-BEFORE-EXCEPTION-TIMER-ELAPSES-CONTINUE-WITHOUT-WAITING-IT` / `EXCEPTION-TIMER` / `TARGET-ANSWERS-BEFORE-EXCEPTION-TIMER-ELAPSES-CONTINUE-WITHO-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，若目标在 Exception Timer 到期前应答，数据加载器必须继续而不把该定时器等待完毕。 | — | — |
| `CRS-M1-00435` | `SU-ARINC-615A-3-6-3-3-P070-PROSE-SENTENCE-051-E812AC346D09`<br>`ARINC-615A-3 6.3.3 p.58` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `MINIMIZE-EXCEPTION-TIMER-SO-SILENT-PHASE-STAYS-SHORT` / `EXCEPTION-TIMER` / `MINIMIZE-EXCEPTION-TIMER-SO-SILENT-PHASE-STAYS-SHORT-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须尽量缩短 Exception Timer so the silent phase stays short。 | — | — |
| `CRS-M1-00436` | `SU-ARINC-615A-3-6-3-3-P070-PROSE-SENTENCE-052-91F9A68124BD`<br>`ARINC-615A-3 6.3.3 p.58` | `DATA-LOADER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ABORT-DOWNLOAD-NO-NEW-STATUS-FILE-ARRIVES-BEFORE-EXCEPTION-TIMER` / `EXCEPTION-TIMER, LNS` / `ABORT-DOWNLOAD-NO-NEW-STATUS-FILE-ARRIVES-BEFORE-EXCEPTION-T-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，数据加载器必须中止 DOWNLOAD if no new 状态文件 arrives before Exception Timer expires。 | — | — |
| `CRS-M1-00437` | `SU-ARINC-615A-3-6-3-4-P073-PROSE-SENTENCE-007-18AB4BEB6990`<br>`ARINC-615A-3 6.3.4 p.61` | `OPERATOR` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ABLE-SELECT-MEDIA-TYPE-OPERATOR-DEFINED-DOWNLOAD` / `MEDIA-TYPE` / `ABLE-SELECT-MEDIA-TYPE-OPERATOR-DEFINED-DOWNLOAD-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，操作员必须be able to 选择 the media type for 操作员定义 DOWNLOAD。 | — | — |
| `CRS-M1-00438` | `SU-ARINC-615A-3-6-3-4-P073-PROSE-SENTENCE-012-2ED4ABAC4193`<br>`ARINC-615A-3 6.3.4 p.61` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `SEND-STATUS-FILES-WITHIN-ATTACHMENT-4-DLP-MAXIMUM-DELAY--00981` / `LNS, ATTACHMENT-4` / `SEND-STATUS-FILES-WITHIN-ATTACHMENT-4-DLP-MAXIMUM-DELAY-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，目标硬件必须发送 状态文件s within the 附件 4 DLP maximum delay。 | — | — |
| `CRS-M1-00439` | `SU-ARINC-615A-3-6-3-4-P073-PROSE-SENTENCE-014-9F2F8E73FD5D`<br>`ARINC-615A-3 6.3.4 p.61` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `FATAL-ERROR-EMIT-STATUS-FILE-MATCHING-CODE-DESCRIPTION-INSIDE-TIMEOUT--00983` / `LNS, STATUS-CODE, STATUS-DESCRIPTION` / `FATAL-ERROR-EMIT-STATUS-FILE-MATCHING-CODE-DESCRIPTION-INSID-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，目标硬件必须on fatal error emit a 状态文件 with matching code and description inside the timeout。 | — | — |
| `CRS-M1-00440` | `SU-ARINC-615A-3-6-3-4-P073-PROSE-SENTENCE-015-7AC0400C9DB1`<br>`ARINC-615A-3 6.3.4 p.61` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `SEND-STATUS-FILE-IMMEDIATELY-CARRY-ABORT-INTERRUPT--00984` / `ABORT-5-3-2-3-6, INTERRUPT-6-3-6` / `SEND-STATUS-FILE-IMMEDIATELY-CARRY-ABORT-INTERRUPT-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，目标硬件可以发送 a 状态文件 immediately to carry an 中止 or interrupt。 | — | — |
| `CRS-M1-00441` | `SU-ARINC-615A-3-6-3-4-P073-PROSE-SENTENCE-024-D8862D88C46E`<br>`ARINC-615A-3 6.3.4 p.61` | `DATA-LOADER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `TARGET-ANSWERS-BEFORE-EXCEPTION-TIMER-ELAPSES-CONTINUE-WITHOUT-WAITING-IT--00993` / `EXCEPTION-TIMER` / `TARGET-ANSWERS-BEFORE-EXCEPTION-TIMER-ELAPSES-CONTINUE-WITHO-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，若目标在 Exception Timer 到期前应答，数据加载器必须继续而不把该定时器等待完毕。 | — | — |
| `CRS-M1-00442` | `SU-ARINC-615A-3-6-3-4-P073-PROSE-SENTENCE-025-E812AC346D09`<br>`ARINC-615A-3 6.3.4 p.61` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `MINIMIZE-EXCEPTION-TIMER-SO-SILENT-PHASE-STAYS-SHORT--00994` / `EXCEPTION-TIMER` / `MINIMIZE-EXCEPTION-TIMER-SO-SILENT-PHASE-STAYS-SHORT-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，目标硬件必须尽量缩短 Exception Timer so the silent phase stays short。 | — | — |
| `CRS-M1-00443` | `SU-ARINC-615A-3-6-3-4-P073-PROSE-SENTENCE-026-464E9E6694A8`<br>`ARINC-615A-3 6.3.4 p.61` | `DATA-LOADER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ABORT-DOWNLOAD-NO-NEW-STATUS-FILE-ARRIVES-BEFORE-EXCEPTION-TIMER--00995` / `EXCEPTION-TIMER, LNS` / `ABORT-DOWNLOAD-NO-NEW-STATUS-FILE-ARRIVES-BEFORE-EXCEPTION-T-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，数据加载器必须中止 DOWNLOAD if no new 状态文件 arrives before Exception Timer expires。 | — | — |
| `CRS-M1-00444` | `SU-ARINC-615A-3-6-4-6-P091-PROSE-SENTENCE-016-1532165AA3AE`<br>`ARINC-615A-3 6.4.6 p.79` | `PROTOCOL-FILE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ZERO-TERMINATE-LNR-FILE-NAME-0X00` / `OBJ-0X00` / `ZERO-TERMINATE-LNR-FILE-NAME-0X00-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，协议文件生成方必须用 0x00 作为 LNR File Name 的零终止。 | — | — |
| `CRS-M1-00445` | `SU-ARINC-615A-3-6-4-7-P092-PROSE-SENTENCE-028-83077CACF0DC`<br>`ARINC-615A-3 6.4.7 p.80` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `OTHER-STATUS-CODES-IGNORE-DESCRIPTION-CONTENT-WHICH-MAY-HOLD-LEFTOVER` / `DOWNLOAD-STATUS-DESCRIPTION` / `OTHER-STATUS-CODES-IGNORE-DESCRIPTION-CONTENT-WHICH-MAY-HOLD-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方对其他状态码可以忽略描述字段内容，其中可能残留数据。 | — | — |
| `CRS-M1-00446` | `SU-ARINC-615A-3-6-4-7-P092-PROSE-SENTENCE-030-B1FB47BD2E90`<br>`ARINC-615A-3 6.4.7 p.80` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `USE-ONLY-PRINTABLE-CHARACTERS-DOWNLOAD-STATUS-DESCRIPTION-NO-CONTROL-CHARACTERS` / `DOWNLOAD-STATUS-DESCRIPTION` / `USE-ONLY-PRINTABLE-CHARACTERS-DOWNLOAD-STATUS-DESCRIPTION-NO-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须使用 only printable characters in Download Status Description, with no control characters, max 255。 | — | — |
| `CRS-M1-00447` | `SU-ARINC-615A-3-6-4-7-P092-PROSE-SENTENCE-031-1532165AA3AE`<br>`ARINC-615A-3 6.4.7 p.80` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ZERO-TERMINATE-DOWNLOAD-STATUS-DESCRIPTION-0X00` / `OBJ-0X00` / `ZERO-TERMINATE-DOWNLOAD-STATUS-DESCRIPTION-0X00-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须用 0x00 作为 Download Status Description 的零终止。 | — | — |
| `CRS-M1-00448` | `SU-ARINC-615A-3-6-4-7-P093-PROSE-SENTENCE-040-BFA9E163247A`<br>`ARINC-615A-3 6.4.7 p.81` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `SET-EXCEPTION-TIMER-0X0000-EVERY-OTHER-STATUS-CODE` / `EXCEPTION-TIMER, OBJ-0X0000` / `SET-EXCEPTION-TIMER-0X0000-EVERY-OTHER-STATUS-CODE-OBSERVABLE` | `MUST` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须把其他状态码的 Exception Timer 置为 0x0000。 | — | — |
| `CRS-M1-00449` | `SU-ARINC-615A-3-6-4-7-P093-PROSE-SENTENCE-045-16B3A57C8CEC`<br>`ARINC-615A-3 6.4.7 p.81` | `TARGET-HARDWARE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `PROVIDE-ESTIMATED-TIME-SOON-POSSIBLE-DURING-OPERATION` / `ESTIMATED-TIME` / `PROVIDE-ESTIMATED-TIME-SOON-POSSIBLE-DURING-OPERATION-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，目标硬件必须在操作过程中尽快提供 Estimated Time。 | — | — |
| `CRS-M1-00450` | `SU-ARINC-615A-3-6-4-7-P093-PROSE-SENTENCE-048-581419285745`<br>`ARINC-615A-3 6.4.7 p.81` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `TARGET-DOES-NOT-GIVE-ESTIMATED-TIME-SET-FIELD-0XFFFF` / `ESTIMATED-TIME, OBJ-0XFFFF` / `TARGET-DOES-NOT-GIVE-ESTIMATED-TIME-SET-FIELD-0XFFFF-OBSERVABLE` | `MUST` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，若目标未给出 Estimated Time，协议文件生成方必须把该字段置为 0xFFFF。 | — | — |
| `CRS-M1-00451` | `SU-ARINC-615A-3-6-4-7-P093-PROSE-SENTENCE-058-1532165AA3AE`<br>`ARINC-615A-3 6.4.7 p.81` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ZERO-TERMINATE-LNS-FILE-NAME-0X00` / `OBJ-0X00` / `ZERO-TERMINATE-LNS-FILE-NAME-0X00-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须用 0x00 作为 LNS File Name 的零终止。 | — | — |
| `CRS-M1-00452` | `SU-ARINC-615A-3-6-4-7-P094-PROSE-SENTENCE-077-6BCAB56CC15C`<br>`ARINC-615A-3 6.4.7 p.82` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `OTHER-FILE-STATUS-CODES-IGNORE-DESCRIPTION-CONTENT-WHICH-MAY-HOLD` / `FILE-STATUS-DESCRIPTION` / `OTHER-FILE-STATUS-CODES-IGNORE-DESCRIPTION-CONTENT-WHICH-MAY-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方对其他文件状态码可以忽略描述字段内容，其中可能残留数据。 | — | — |
| `CRS-M1-00453` | `SU-ARINC-615A-3-6-4-7-P094-PROSE-SENTENCE-079-53AAFA003A8B`<br>`ARINC-615A-3 6.4.7 p.82` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `USE-ONLY-PRINTABLE-CHARACTERS-FILE-STATUS-DESCRIPTION-NO-CONTROL-CHARACTERS` / `FILE-STATUS-DESCRIPTION` / `USE-ONLY-PRINTABLE-CHARACTERS-FILE-STATUS-DESCRIPTION-NO-CON-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须使用 only printable characters in File Status Description, with no control characters, max 255。 | — | — |
| `CRS-M1-00454` | `SU-ARINC-615A-3-6-4-7-P094-PROSE-SENTENCE-080-1532165AA3AE`<br>`ARINC-615A-3 6.4.7 p.82` | `PROTOCOL-FILE` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ZERO-TERMINATE-FILE-STATUS-DESCRIPTION-0X00` / `OBJ-0X00` / `ZERO-TERMINATE-FILE-STATUS-DESCRIPTION-0X00-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须用 0x00 作为 File Status Description 的零终止。 | — | — |
| `CRS-M1-00455` | `SU-ARINC-615A-3-6-4-8-P095-PROSE-SENTENCE-015-1532165AA3AE`<br>`ARINC-615A-3 6.4.8 p.83` | `PROTOCOL-FILE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ZERO-TERMINATE-LNL-FILE-NAME-0X00` / `OBJ-0X00` / `ZERO-TERMINATE-LNL-FILE-NAME-0X00-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须用 0x00 作为 LNL File Name 的零终止。 | — | — |
| `CRS-M1-00456` | `SU-ARINC-615A-3-6-4-8-P096-PROSE-SENTENCE-020-53AAFA003A8B`<br>`ARINC-615A-3 6.4.8 p.84` | `PROTOCOL-FILE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `USE-ONLY-PRINTABLE-CHARACTERS-LNL-FILE-DESCRIPTION-NO-CONTROL-CHARACTERS` / `FILE-DESCRIPTION` / `USE-ONLY-PRINTABLE-CHARACTERS-LNL-FILE-DESCRIPTION-NO-CONTRO-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须使用 only printable characters in LNL File Description, with no control characters, max 255。 | — | — |
| `CRS-M1-00457` | `SU-ARINC-615A-3-6-4-8-P096-PROSE-SENTENCE-021-1532165AA3AE`<br>`ARINC-615A-3 6.4.8 p.84` | `PROTOCOL-FILE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ZERO-TERMINATE-LNL-FILE-DESCRIPTION-0X00` / `OBJ-0X00` / `ZERO-TERMINATE-LNL-FILE-DESCRIPTION-0X00-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须用 0x00 作为 LNL File Description 的零终止。 | — | — |
| `CRS-M1-00458` | `SU-ARINC-615A-3-6-4-9-P096-PROSE-SENTENCE-016-1532165AA3AE`<br>`ARINC-615A-3 6.4.9 p.84` | `PROTOCOL-FILE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ZERO-TERMINATE-LNA-FILE-NAME-0X00` / `OBJ-0X00` / `ZERO-TERMINATE-LNA-FILE-NAME-0X00-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须用 0x00 作为 LNA File Name 的零终止。 | — | — |
| `CRS-M1-00459` | `SU-ARINC-615A-3-TABLE-6_4_6-1-R002`<br>`ARINC-615A-3 6.4.6 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-LENGTH, LNR` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 1 个字段位置编码 LNR 的 FIELD-FILE-LENGTH。 | — | — |
| `CRS-M1-00460` | `SU-ARINC-615A-3-TABLE-6_4_6-1-R003`<br>`ARINC-615A-3 6.4.6 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-PROTOCOL-VERSION, LNR` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在使用对应 DOWNLOAD 模式时，协议文件生成方必须把 LNR 的 FIELD-PROTOCOL-VERSION 按表序号 2 编码为两个 ASCII 字符。 | — | — |
| `CRS-M1-00461` | `SU-ARINC-615A-3-TABLE-6_4_6-1-R004`<br>`ARINC-615A-3 6.4.6 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-NUMBER-OF-FILES, LNR` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 3 个字段位置编码 LNR 的 FIELD-NUMBER-OF-FILES。 | — | — |
| `CRS-M1-00462` | `SU-ARINC-615A-3-TABLE-6_4_6-1-R005`<br>`ARINC-615A-3 6.4.6 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-NAME-LENGTH, LNR` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 4 个字段位置编码 LNR 的 FIELD-FILE-NAME-LENGTH。 | — | — |
| `CRS-M1-00463` | `SU-ARINC-615A-3-TABLE-6_4_6-1-R006`<br>`ARINC-615A-3 6.4.6 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-NAME, LNR` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 5 个字段位置编码 LNR 的 FIELD-FILE-NAME。 | — | — |
| `CRS-M1-00464` | `SU-ARINC-615A-3-TABLE-6_4_6-1-R007`<br>`ARINC-615A-3 6.4.6 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-USER-DEFINED-DATA-LENGTH, LNR` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 6 个字段位置编码 LNR 的 FIELD-USER-DEFINED-DATA-LENGTH。 | — | — |
| `CRS-M1-00465` | `SU-ARINC-615A-3-TABLE-6_4_6-1-R008`<br>`ARINC-615A-3 6.4.6 p.78` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-USER-DEFINED-DATA, LNR` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 7 个字段位置编码 LNR 的 FIELD-USER-DEFINED-DATA。 | — | — |
| `CRS-M1-00466` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R002`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-LENGTH, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 1 个字段位置编码 LNS 的 FIELD-FILE-LENGTH。 | — | — |
| `CRS-M1-00467` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R003`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-PROTOCOL-VERSION, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在使用对应 DOWNLOAD 模式时，协议文件生成方必须把 LNS 的 FIELD-PROTOCOL-VERSION 按表序号 2 编码为两个 ASCII 字符。 | — | — |
| `CRS-M1-00468` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R004`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-DOWNLOAD-OPERATION-STATUS-CODE, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 3 个字段位置编码 LNS 的 FIELD-DOWNLOAD-OPERATION-STATUS-CODE。 | — | — |
| `CRS-M1-00469` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R005`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-DOWNLOAD-STATUS-DESCRIPTION-LENGTH, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 4 个字段位置编码 LNS 的 FIELD-DOWNLOAD-STATUS-DESCRIPTION-LENGTH。 | — | — |
| `CRS-M1-00470` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R006`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-DOWNLOAD-STATUS-DESCRIPTION, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 5 个字段位置编码 LNS 的 FIELD-DOWNLOAD-STATUS-DESCRIPTION。 | — | — |
| `CRS-M1-00471` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R007`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-COUNTER, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 6 个字段位置编码 LNS 的 FIELD-COUNTER。 | — | — |
| `CRS-M1-00472` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R008`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-EXCEPTION-TIMER, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须把 LNS Exception Timer 编为表序 7 的固定 16 位字段。该字段在状态 0x0002 或 0x0004 用作 0..65535 的剩余秒数；其他状态仍保留该字段并置 0x0000。 | — | — |
| `CRS-M1-00473` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R009`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-ESTIMATED-TIME, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须把 LNS Estimated Time 编为表序 8 的固定 16 位字段。状态 0x0002 或 0x0004 携带 0..32767 的剩余秒数，0xFFFF 表示未给出；其他状态仍保留该字段并置 0x0000。非活动的 0x0000 是未使用填充，不是未给出哨兵。 | — | — |
| `CRS-M1-00474` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R010`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-DOWNLOAD-LIST-RATIO, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须把 LNS Download List Ratio 编为三个右对齐、前导空白的 ASCII 字符，而不是整数。 | — | — |
| `CRS-M1-00475` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R011`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-NUMBER-OF-FILES, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 10 个字段位置编码 LNS 的 FIELD-NUMBER-OF-FILES。 | — | — |
| `CRS-M1-00476` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R012`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-NAME-LENGTH, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 11 个字段位置编码 LNS 的 FIELD-FILE-NAME-LENGTH。 | — | — |
| `CRS-M1-00477` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R013`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-NAME, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 12 个字段位置编码 LNS 的 FIELD-FILE-NAME。 | — | — |
| `CRS-M1-00478` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R014`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-STATUS, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 13 个字段位置编码 LNS 的 FIELD-FILE-STATUS。 | — | — |
| `CRS-M1-00479` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R015`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-STATUS-DESCRIPTION-LENGTH, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 14 个字段位置编码 LNS 的 FIELD-FILE-STATUS-DESCRIPTION-LENGTH。 | — | — |
| `CRS-M1-00480` | `SU-ARINC-615A-3-TABLE-6_4_7-1-R016`<br>`ARINC-615A-3 6.4.7 p.79` | `PROTOCOL-FILE-PRODUCER` / `WHEN-MEDIA-OR-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-STATUS-DESCRIPTION, LNS` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义或操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 15 个字段位置编码 LNS 的 FIELD-FILE-STATUS-DESCRIPTION。 | — | — |
| `CRS-M1-00481` | `SU-ARINC-615A-3-TABLE-6_4_8-1-R002`<br>`ARINC-615A-3 6.4.8 p.83` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-LENGTH, LNL` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 1 个字段位置编码 LNL 的 FIELD-FILE-LENGTH。 | — | — |
| `CRS-M1-00482` | `SU-ARINC-615A-3-TABLE-6_4_8-1-R003`<br>`ARINC-615A-3 6.4.8 p.83` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-PROTOCOL-VERSION, LNL` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在使用对应 DOWNLOAD 模式时，协议文件生成方必须把 LNL 的 FIELD-PROTOCOL-VERSION 按表序号 2 编码为两个 ASCII 字符。 | — | — |
| `CRS-M1-00483` | `SU-ARINC-615A-3-TABLE-6_4_8-1-R004`<br>`ARINC-615A-3 6.4.8 p.83` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-NUMBER-OF-FILES, LNL` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 3 个字段位置编码 LNL 的 FIELD-NUMBER-OF-FILES。 | — | — |
| `CRS-M1-00484` | `SU-ARINC-615A-3-TABLE-6_4_8-1-R005`<br>`ARINC-615A-3 6.4.8 p.83` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-NAME-LENGTH, LNL` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 4 个字段位置编码 LNL 的 FIELD-FILE-NAME-LENGTH。 | — | — |
| `CRS-M1-00485` | `SU-ARINC-615A-3-TABLE-6_4_8-1-R006`<br>`ARINC-615A-3 6.4.8 p.83` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-NAME, LNL` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 5 个字段位置编码 LNL 的 FIELD-FILE-NAME。 | — | — |
| `CRS-M1-00486` | `SU-ARINC-615A-3-TABLE-6_4_8-1-R007`<br>`ARINC-615A-3 6.4.8 p.83` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-DESCRIPTION-LENGTH, LNL` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 6 个字段位置编码 LNL 的 FIELD-FILE-DESCRIPTION-LENGTH。 | — | — |
| `CRS-M1-00487` | `SU-ARINC-615A-3-TABLE-6_4_8-1-R008`<br>`ARINC-615A-3 6.4.8 p.83` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-DESCRIPTION, LNL` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 7 个字段位置编码 LNL 的 FIELD-FILE-DESCRIPTION。 | — | — |
| `CRS-M1-00488` | `SU-ARINC-615A-3-TABLE-6_4_9-1-R002`<br>`ARINC-615A-3 6.4.9 p.84` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-LENGTH, LNA` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 1 个字段位置编码 LNA 的 FIELD-FILE-LENGTH。 | — | — |
| `CRS-M1-00489` | `SU-ARINC-615A-3-TABLE-6_4_9-1-R003`<br>`ARINC-615A-3 6.4.9 p.84` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-PROTOCOL-VERSION, LNA` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在使用对应 DOWNLOAD 模式时，协议文件生成方必须把 LNA 的 FIELD-PROTOCOL-VERSION 按表序号 2 编码为两个 ASCII 字符。 | — | — |
| `CRS-M1-00490` | `SU-ARINC-615A-3-TABLE-6_4_9-1-R004`<br>`ARINC-615A-3 6.4.9 p.84` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-NUMBER-OF-FILES, LNA` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 3 个字段位置编码 LNA 的 FIELD-NUMBER-OF-FILES。 | — | — |
| `CRS-M1-00491` | `SU-ARINC-615A-3-TABLE-6_4_9-1-R005`<br>`ARINC-615A-3 6.4.9 p.84` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-NAME-LENGTH, LNA` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 4 个字段位置编码 LNA 的 FIELD-FILE-NAME-LENGTH。 | — | — |
| `CRS-M1-00492` | `SU-ARINC-615A-3-TABLE-6_4_9-1-R006`<br>`ARINC-615A-3 6.4.9 p.84` | `PROTOCOL-FILE-PRODUCER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ENCODE-TABULATED-FIELD` / `FIELD-FILE-NAME, LNA` / `FIELD-PRESENCE-SIZE-AND-VALUE-OBSERVABLE` | `TABLE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，协议文件生成方必须按表定宽度和第 5 个字段位置编码 LNA 的 FIELD-FILE-NAME。 | — | — |
| `CRS-M1-00493` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E001-93E2E1579D6F`<br>`ARINC-615A-3 6.3.3 p.57` | `DATA-LOADER-APPLICATION` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ISSUE-DOWNLOADING-MEDIA-INITIALIZATION-START-MEDIA-MODE-CHART` / `DOWNLOADING-MEDIA-INITIALIZATION` / `ISSUE-DOWNLOADING-MEDIA-INITIALIZATION-START-MEDIA-MODE-CHAR-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，数据加载器应用层必须发出 Downloading_Media_Initialization to start the media-mode chart。 | — | — |
| `CRS-M1-00494` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E002-56059C7FBCE3`<br>`ARINC-615A-3 6.3.3 p.57` | `DATA-LOADER-PROTOCOL` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `TFTP-READ-LND-TARGET` / `LND` / `TFTP-READ-LND-TARGET-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，数据加载器协议层必须用 TFTP 从目标读取 LND。 | — | — |
| `CRS-M1-00495` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E003-7572FB4A7D49`<br>`ARINC-615A-3 6.3.3 p.57` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `TRANSFER-LND-ANSWER-WAIT-RETRY` / `LND, WAIT` / `TRANSFER-LND-ANSWER-WAIT-RETRY-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须传送 LND or answer WAIT for retry。 | — | — |
| `CRS-M1-00496` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E004-F7FB3AED0BF8`<br>`ARINC-615A-3 6.3.3 p.57` | `DATA-LOADER-PROTOCOL` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `EMIT-DOWNLOADING-INITIALIZATION-RESPONSE-LND-OUTCOME` / `DOWNLOADING-INITIALIZATION-RESPONSE` / `EMIT-DOWNLOADING-INITIALIZATION-RESPONSE-LND-OUTCOME-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，数据加载器协议层必须根据 LND 结果发出 Downloading_Initialization_Response。 | — | — |
| `CRS-M1-00497` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E005-DDC22BBE77AD`<br>`ARINC-615A-3 6.3.3 p.57` | `DATA-LOADER` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `END-MEDIA-DEFINED-DOWNLOAD-DENY` / `DENY` / `END-MEDIA-DEFINED-DOWNLOAD-DENY-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，数据加载器必须结束 媒体定义 DOWNLOAD on deny。 | — | — |
| `CRS-M1-00498` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E006-FFDAE5BD327A`<br>`ARINC-615A-3 6.3.3 p.57` | `DATA-LOADER-PROTOCOL` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `AFTER-ACCEPT-WRITE-LNR-TO-TARGET-BY-TFTP` / `LNR, TARGET-HARDWARE, TFTP` / `ACCEPT-TFTP-WRITE-LNR-TARGET-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，数据加载器协议层必须在接受之后用 TFTP 把 LNR 写到目标硬件。 | — | — |
| `CRS-M1-00499` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E007-465C743F7A74`<br>`ARINC-615A-3 6.3.3 p.57` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `RECEIVE-ANALYZE-LNR` / `LNR` / `RECEIVE-ANALYZE-LNR-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须接收 and analyze LNR。 | — | — |
| `CRS-M1-00500` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E008-4F5A7B67B142`<br>`ARINC-615A-3 6.3.3 p.57` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `TFTP-WRITE-LNS-INCLUDING-ACCEPTED-NOT-STARTED-0X0001` / `LNS, OBJ-0X0001` / `TFTP-WRITE-LNS-INCLUDING-ACCEPTED-NOT-STARTED-0X0001-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须用 TFTP 写 LNS，并包含已接受但未开始的 0x0001。 | — | — |
| `CRS-M1-00501` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E009-0C4A2E52223E`<br>`ARINC-615A-3 6.3.3 p.57` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `TFTP-SEND-EACH-LNR-LISTED-DATA-FILE` / `DATA-FILES` / `TFTP-SEND-EACH-LNR-LISTED-DATA-FILE-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须TFTP-发送 each LNR-listed data file。 | — | — |
| `CRS-M1-00502` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E010-C4CF6F527181`<br>`ARINC-615A-3 6.3.3 p.57` | `DATA-LOADER-PROTOCOL` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `ISSUE-DOWNLOADING-FILE-RECEIPT-EACH-RECEIVED-FILE` / `DOWNLOADING-FILE-RECEIPT` / `ISSUE-DOWNLOADING-FILE-RECEIPT-EACH-RECEIVED-FILE-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，数据加载器协议层必须发出 Downloading_File_Receipt for each 接收d file。 | — | — |
| `CRS-M1-00503` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E011-86839F050632`<br>`ARINC-615A-3 6.3.3 p.57` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `REPEAT-REMAINING-FILES-LNS-PROGRESS` / `LNS` / `REPEAT-REMAINING-FILES-LNS-PROGRESS-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须重复 remaining files with LNS progress。 | — | — |
| `CRS-M1-00504` | `SU-ARINC-615A-3-SECTION-6-3-3-SEQUENCE-CHART-E012-9EC73921C558`<br>`ARINC-615A-3 6.3.3 p.57` | `TARGET-HARDWARE` / `WHEN-MEDIA-DEFINED-DOWNLOAD-IS-USED` / `END-AFTER-FINAL-LNS-COMPLETE-FATAL-HONOUR-ATTACHMENT-4-CHRONO` / `LNS, ATTACHMENT-4` / `END-AFTER-FINAL-LNS-COMPLETE-FATAL-HONOUR-ATTACHMENT-4-CHRON-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用媒体定义 DOWNLOAD 时，目标硬件必须结束 after final LNS 完成 or fatal; honour 附件 4 chrono timeouts。 | — | — |
| `CRS-M1-00505` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E001-D20446C4AA87`<br>`ARINC-615A-3 6.3.4 p.60` | `DATA-LOADER-APPLICATION` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ISSUE-DOWNLOADING-OPERATOR-INITIALIZATION-START-OPERATOR-MODE-CHART` / `DOWNLOADING-OPERATOR-INITIALIZATION` / `ISSUE-DOWNLOADING-OPERATOR-INITIALIZATION-START-OPERATOR-MOD-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，数据加载器应用层必须发出 Downloading_Operator_Initialization to start the operator-mode chart。 | — | — |
| `CRS-M1-00506` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E002-FA62BFEC08D9`<br>`ARINC-615A-3 6.3.4 p.60` | `DATA-LOADER-PROTOCOL` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `TFTP-READ-LNO-TARGET` / `LNO` / `TFTP-READ-LNO-TARGET-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，数据加载器协议层必须用 TFTP 从目标读取 LNO。 | — | — |
| `CRS-M1-00507` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E003-4E7C61B06179`<br>`ARINC-615A-3 6.3.4 p.60` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `TRANSFER-LNO-ANSWER-WAIT-RETRY` / `LNO, WAIT` / `TRANSFER-LNO-ANSWER-WAIT-RETRY-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，目标硬件必须传送 LNO or answer WAIT for retry。 | — | — |
| `CRS-M1-00508` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E004-4DD6ECF8E15C`<br>`ARINC-615A-3 6.3.4 p.60` | `DATA-LOADER-PROTOCOL` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `EMIT-DOWNLOADING-INITIALIZATION-RESPONSE-LNO-OUTCOME` / `DOWNLOADING-INITIALIZATION-RESPONSE` / `EMIT-DOWNLOADING-INITIALIZATION-RESPONSE-LNO-OUTCOME-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，数据加载器协议层必须根据 LNO 结果发出 Downloading_Initialization_Response。 | — | — |
| `CRS-M1-00509` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E005-22221ABB2116`<br>`ARINC-615A-3 6.3.4 p.60` | `DATA-LOADER` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `END-OPERATOR-DEFINED-DOWNLOAD-DENY` / `DENY` / `END-OPERATOR-DEFINED-DOWNLOAD-DENY-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，数据加载器必须结束 操作员定义 DOWNLOAD on deny。 | — | — |
| `CRS-M1-00510` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E006-145A7178D4F7`<br>`ARINC-615A-3 6.3.4 p.60` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `AFTER-ACCEPT-WRITE-LNL-TO-LOADER-BY-TFTP` / `LNL, DATA-LOADER, TFTP` / `ACCEPT-TFTP-WRITE-LNL-LOADER-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，目标硬件必须在接受之后用 TFTP 把 LNL 写到加载器。 | — | — |
| `CRS-M1-00511` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E007-BB90540A19D7`<br>`ARINC-615A-3 6.3.4 p.60` | `DATA-LOADER-PROTOCOL` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ISSUE-DOWNLOADING-FILE-LIST-RECEIPT` / `DOWNLOADING-FILE-LIST-RECEIPT` / `ISSUE-DOWNLOADING-FILE-LIST-RECEIPT-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，数据加载器协议层必须发出 Downloading_File_List_Receipt。 | — | — |
| `CRS-M1-00512` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E008-1FFC2020C9F9`<br>`ARINC-615A-3 6.3.4 p.60` | `OPERATOR` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `SELECT-FILES-LOADER-TFTP-WRITES-LNA-FILE-SELECTION` / `LNA, FILE-SELECTION` / `SELECT-FILES-LOADER-TFTP-WRITES-LNA-FILE-SELECTION-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，操作员必须选择 files; loader TFTP-writes LNA as File_Selection。 | — | — |
| `CRS-M1-00513` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E009-0C4A2E52223E`<br>`ARINC-615A-3 6.3.4 p.60` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `TFTP-SEND-EACH-LNA-LISTED-DATA-FILE` / `DATA-FILES` / `TFTP-SEND-EACH-LNA-LISTED-DATA-FILE-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，目标硬件必须TFTP-发送 each LNA-listed data file。 | — | — |
| `CRS-M1-00514` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E010-C4CF6F527181`<br>`ARINC-615A-3 6.3.4 p.60` | `DATA-LOADER-PROTOCOL` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `ISSUE-DOWNLOADING-FILE-RECEIPT-EACH-RECEIVED-FILE--02783` / `DOWNLOADING-FILE-RECEIPT` / `ISSUE-DOWNLOADING-FILE-RECEIPT-EACH-RECEIVED-FILE-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，数据加载器协议层必须发出 Downloading_File_Receipt for each 接收d file。 | — | — |
| `CRS-M1-00515` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E011-86839F050632`<br>`ARINC-615A-3 6.3.4 p.60` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `REPEAT-REMAINING-FILES-LNS-PROGRESS--02784` / `LNS` / `REPEAT-REMAINING-FILES-LNS-PROGRESS-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，目标硬件必须重复 remaining files with LNS progress。 | — | — |
| `CRS-M1-00516` | `SU-ARINC-615A-3-SECTION-6-3-4-SEQUENCE-CHART-E012-9EC73921C558`<br>`ARINC-615A-3 6.3.4 p.60` | `TARGET-HARDWARE` / `WHEN-OPERATOR-DEFINED-DOWNLOAD-IS-USED` / `END-AFTER-FINAL-LNS-COMPLETE-FATAL-HONOUR-ATTACHMENT-4-CHRONO--02785` / `LNS, ATTACHMENT-4` / `END-AFTER-FINAL-LNS-COMPLETE-FATAL-HONOUR-ATTACHMENT-4-CHRON-OBSERVABLE` | `FIGURE-CONSTRAINT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在实现并使用操作员定义 DOWNLOAD 时，目标硬件必须结束 after final LNS 完成 or fatal; honour 附件 4 chrono timeouts。 | — | — |
| `CRS-M1-00517` | `SU-ARINC-615A-3-APPENDIX-E-P134-PROSE-SENTENCE-008-123ADFD1F0A0`<br>`ARINC-615A-3 APPENDIX-E p.122` | `DATA-LOADER` / `WHEN-615A-IS-CARRIED-OVER-AFDX` / `USE-FIND-NETWORK-CONFIGURATION-FILE-IDENTIFY-TARGETS-AFDX-NETWORK` / `FIND, NETWORK-CONFIGURATION-FILE` / `USE-FIND-NETWORK-CONFIGURATION-FILE-IDENTIFY-TARGETS-AFDX-NE-OBSERVABLE` | `MAY` / `OPTIONAL` | `CONDITIONAL` | 在配置的部署把 615A 承载于 AFDX 而非普通以太网时，数据加载器可以使用 FIND or a network configuration file to identify targets on the AFDX network。这不激活当前 Compliant 以太网实例。 | — | — |
| `CRS-M1-00518` | `SU-ARINC-615A-3-APPENDIX-E-P134-PROSE-SENTENCE-011-E6FB447853B2`<br>`ARINC-615A-3 APPENDIX-E p.122` | `DATA-LOADER` / `WHEN-615A-IS-CARRIED-OVER-AFDX` / `USE-TFTP-PROTOCOL-DESCRIBED-615A-3-615A-OPERATIONS-OVER-AFDX` / `TFTP` / `USE-TFTP-PROTOCOL-DESCRIBED-615A-3-615A-OPERATIONS-OVER-AFDX-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在配置的部署把 615A 承载于 AFDX 而非普通以太网时，数据加载器必须使用 the TFTP protocol described in 615A-3 for 615A operations over AFDX。这不激活当前 Compliant 以太网实例。 | — | — |
| `CRS-M1-00519` | `SU-ARINC-615A-3-APPENDIX-E-P134-PROSE-SENTENCE-013-B5690D59EDBF`<br>`ARINC-615A-3 APPENDIX-E p.122` | `SYSTEM-INTEGRATOR` / `WHEN-615A-IS-CARRIED-OVER-AFDX` / `APPLY-664P4-ADDRESS-RULES-OR-INTEGRATOR-IDENTIFIED-REQUIREMENTS` / `ARINC-664-4-ADDRESS-RULES, INTEGRATOR-IDENTIFIED-ADDRESS-REQUIREMENTS` / `AFDX-ADDRESS-RULE-ALTERNATIVE-OBSERVABLE` | `SHOULD` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在配置的部署把 615A 承载于 AFDX 而非普通以太网时，系统集成商必须适用 664 Part 4 的航空数据网络地址规则，或指出集成商识别的地址要求。这两条路径保持可选择，不自动选定 Part 4，也不激活当前 Compliant 以太网实例。 | — | — |
| `CRS-M1-00520` | `SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-002-F178271163DF`<br>`ARINC-615A-3 3-2 p.96` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `KEEP-THREE-SECOND-FIND-ANSWER-WINDOW` / `FIND-ANSWER-WINDOW-3-S` / `FIND-ANSWER-WINDOW-LIFETIME-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 在实现 FIND 时，数据加载器必须在发出 FIND 请求后保持三秒 FIND 应答登记窗口。该三秒是窗口寿命，不是主机应答期限，也不是可以提前关闭登记的许可。 | `FIXED-SOURCE-CONSTANT` / `FIND-ANSWER-WINDOW-3-S` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `3..3 s` / 证据：SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-002-F178271163DF | — |
| `CRS-M1-00521` | `SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-004-30FC1BCEB891`<br>`ARINC-615A-3 3-2 p.96` | `DATA-LOADER` / `WHEN-FIND-IMPLEMENTED` / `CLOSE-FIND-ANSWER-REGISTRATION-WHEN-WINDOW-EXPIRES` / `FIND-ANSWER-REGISTRATION, FIND-ANSWER-WINDOW-3-S` / `FIND-REGISTRATION-CLOSE-AT-WINDOW-END-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 在实现 FIND 时，数据加载器必须在发出 FIND 请求后三秒关闭 FIND 应答登记。该关闭与三秒窗口寿命到期是同一逻辑时刻，而不是到期后再延迟三秒。 | `FIXED-SOURCE-CONSTANT` / `FIND-ANSWER-WINDOW-3-S` / `SOURCE-DEFINES-DEADLINE-OR-DURATION` / `3..3 s` / 证据：SU-ARINC-615A-3-3-2-P108-PROSE-SENTENCE-004-30FC1BCEB891 | — |
| `CRS-M1-00522` | `SU-ARINC-615A-3-5-4-4-3-P052-PROSE-SENTENCE-005-D462FF831585`<br>`ARINC-615A-3 5.4.4.3 p.40` | `DATA-LOADER` / `WHEN-REMOVABLE-MEDIA-IS-LNR-SOURCE-AND-DOWNLOAD-DESTINATION` / `CREATE-DNLD-DATA-DIRECTORY-IN-DOWNLOAD-MEDIA-ROOT` / `DNLD-DATA-DIRECTORY, DOWNLOAD-MEDIA-ROOT` / `DNLD-DATA-DIRECTORY-IN-ROOT-OBSERVABLE` | `FACT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在可移动媒体既是 LNR 来源又是下载数据目的地时，数据加载器必须在下载媒体的根目录下创建 DNLD_DATA 目录。 | — | — |
| `CRS-M1-00523` | `SU-ARINC-615A-3-5-4-4-3-P052-PROSE-SENTENCE-006-ED9F856333F8`<br>`ARINC-615A-3 5.4.4.3 p.40` | `DATA-LOADER` / `WHEN-REMOVABLE-MEDIA-IS-LNR-SOURCE-AND-DOWNLOAD-DESTINATION` / `INCREMENT-DNLD-DATA-NUMBER-EACH-DOWNLOAD` / `DNLD-DATA-NUMBER, DNLD-DATA-DIRECTORY` / `DNLD-DATA-NUMBER-INCREMENTS-OBSERVABLE` | `FACT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在可移动媒体既是 LNR 来源又是下载数据目的地时，数据加载器必须在每次下载时递增 <number>，以使相继 DNLD_DATA 目录名保持唯一。 | — | — |
| `CRS-M1-00524` | `SU-ARINC-615A-3-3-3-P108-PROSE-SENTENCE-003-9C92144E4252`<br>`ARINC-615A-3 3-3 p.96` | `FIND-PROTOCOL` / `WHEN-FIND-IMPLEMENTED` / `ENCODE-FIND-PACKET-AS-TWO-BYTE-HEADER-PLUS-VARIABLE-DATA` / `FIND-HEADER-2-BYTE, FIND-VARIABLE-LENGTH-DATA, FIND-OPCODE` / `FIND-HEADER-AND-DATA-LAYOUT-OBSERVABLE` | `FACT` / `REQUIRED` | `APPLICABLE-SUPPORTING` | 在实现 FIND 时，每个 FIND 分组必须包含报头和可变长度数据区。报头为两字节并承载操作码。 | — | — |
| `CRS-M1-00525` | `SU-ARINC-615A-3-5-4-4-3-P052-PROSE-SENTENCE-007-FF9E1B1FACD7`<br>`ARINC-615A-3 5.4.4.3 p.40` | `DATA-LOADER` / `WHEN-REMOVABLE-MEDIA-IS-LNR-SOURCE-AND-DOWNLOAD-DESTINATION` / `START-DNLD-DATA-NUMBER-AT-ONE` / `DNLD-DATA-NUMBER` / `DNLD-DATA-NUMBER-STARTS-AT-ONE-OBSERVABLE` | `FACT` / `CONDITIONAL-REQUIRED` | `CONDITIONAL` | 在可移动媒体既是 LNR 来源又是下载数据目的地时，数据加载器必须把 <number> 从 1 开始。 | — | — |

## 可观察时序语义

| CRS | 事件族 | 触发 → 响应 | 取消／替代触发 | 关联／配对 |
|---|---|---|---|---|
| `CRS-M1-00032` | `WAIT-MESSAGE-RETRY-NOT-BEFORE-DEADLINE` | `WAIT-MESSAGE-WITH-DELAY-RECEIVED` → `NEW-TFTP-TRANSFER-INITIATED-AFTER-DELAY` | `OPERATION-ABORTED-OR-FATAL` / `NEWER-WAIT-MESSAGE-FOR-SAME-REQUEST-RECEIVED` | `TFTP-PEER-AND-REJECTED-TRANSFER-REQUEST` / `PAIR-WAIT-DELAY-WITH-REPLACEMENT-TFTP-TRANSFER` |
| `CRS-M1-00094` | `DLP-CONSECUTIVE-TFTP-TRANSFER-DEADLINE` | `FINAL-PACKET-OF-INITIATING-TFTP-TRANSFER` → `FIRST-PACKET-OF-NEXT-DLP-TFTP-TRANSFER` | `DLP-OPERATION-ABORTED-OR-FATAL` / `AUTHORIZED-DLP-RETRY-START` | `TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-CONSECUTIVE-TFTP-TRANSFERS-IN-SAME-OPERATION` |
| `CRS-M1-00097` | `DLP-CONSECUTIVE-TFTP-TRANSFER-DEADLINE` | `FINAL-PACKET-OF-INITIATING-TFTP-TRANSFER` → `FIRST-PACKET-OF-NEXT-DLP-TFTP-TRANSFER` | `DLP-OPERATION-ABORTED-OR-FATAL` / `AUTHORIZED-DLP-RETRY-START` | `TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-CONSECUTIVE-TFTP-TRANSFERS-IN-SAME-OPERATION` |
| `CRS-M1-00098` | `DLP-CONSECUTIVE-TFTP-TRANSFER-DEADLINE` | `FINAL-PACKET-OF-INITIATING-TFTP-TRANSFER` → `FIRST-PACKET-OF-NEXT-DLP-TFTP-TRANSFER` | `DLP-OPERATION-ABORTED-OR-FATAL` / `AUTHORIZED-DLP-RETRY-START` | `TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-CONSECUTIVE-TFTP-TRANSFERS-IN-SAME-OPERATION` |
| `CRS-M1-00099` | `STATUS-EXCEPTION-SILENCE-DEADLINE` | `STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` → `FIRST-TARGET-STATUS-OR-RESPONSE-AFTER-SILENCE` | `OPERATION-ABORTED-OR-FATAL` / `NEWER-STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` | `TARGET-OPERATION-AND-STATUS-FILE-INSTANCE` / `PAIR-EXCEPTION-TIMER-WITH-TARGET-SILENCE-INTERVAL` |
| `CRS-M1-00100` | `STATUS-EXCEPTION-SILENCE-DEADLINE` | `STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` → `FIRST-TARGET-STATUS-OR-RESPONSE-AFTER-SILENCE` | `OPERATION-ABORTED-OR-FATAL` / `NEWER-STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` | `TARGET-OPERATION-AND-STATUS-FILE-INSTANCE` / `PAIR-EXCEPTION-TIMER-WITH-TARGET-SILENCE-INTERVAL` |
| `CRS-M1-00101` | `STATUS-BEFORE-EXCEPTION-DELAY-OR-ABORT` | `STATUS-FILE-WITH-EXCEPTION-DELAY-RECEIVED` → `NEW-STATUS-FILE-RECEIVED-OR-OPERATION-ABORTED` | `OPERATION-TERMINATED` / `NEWER-STATUS-FILE-RECEIVED` | `TARGET-AND-ACTIVE-OPERATION` / `PAIR-EXCEPTION-DELAY-WITH-NEXT-STATUS-OR-ABORT` |
| `CRS-M1-00102` | `DLP-CONSECUTIVE-TFTP-TRANSFER-DEADLINE` | `FINAL-PACKET-OF-INITIATING-TFTP-TRANSFER` → `FIRST-PACKET-OF-NEXT-DLP-TFTP-TRANSFER` | `DLP-OPERATION-ABORTED-OR-FATAL` / `AUTHORIZED-DLP-RETRY-START` | `TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-CONSECUTIVE-TFTP-TRANSFERS-IN-SAME-OPERATION` |
| `CRS-M1-00106` | `STATUS-EXCEPTION-SILENCE-DEADLINE` | `STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` → `FIRST-TARGET-STATUS-OR-RESPONSE-AFTER-SILENCE` | `OPERATION-ABORTED-OR-FATAL` / `NEWER-STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` | `TARGET-OPERATION-AND-STATUS-FILE-INSTANCE` / `PAIR-EXCEPTION-TIMER-WITH-TARGET-SILENCE-INTERVAL` |
| `CRS-M1-00107` | `STATUS-EXCEPTION-SILENCE-DEADLINE` | `STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` → `FIRST-TARGET-STATUS-OR-RESPONSE-AFTER-SILENCE` | `OPERATION-ABORTED-OR-FATAL` / `NEWER-STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` | `TARGET-OPERATION-AND-STATUS-FILE-INSTANCE` / `PAIR-EXCEPTION-TIMER-WITH-TARGET-SILENCE-INTERVAL` |
| `CRS-M1-00108` | `STATUS-BEFORE-EXCEPTION-DELAY-OR-ABORT` | `STATUS-FILE-WITH-EXCEPTION-DELAY-RECEIVED` → `NEW-STATUS-FILE-RECEIVED-OR-OPERATION-ABORTED` | `OPERATION-TERMINATED` / `NEWER-STATUS-FILE-RECEIVED` | `TARGET-AND-ACTIVE-OPERATION` / `PAIR-EXCEPTION-DELAY-WITH-NEXT-STATUS-OR-ABORT` |
| `CRS-M1-00168` | `TFTP-PACKET-ANSWER-DEADLINE` | `TFTP-PACKET-SENT` → `CORRESPONDING-TFTP-ANSWER-RECEIVED` | `TFTP-TRANSFER-TERMINATED` / `AUTHORIZED-RETRANSMISSION-OF-SAME-EXCHANGE` | `TFTP-TRANSFER-ID-AND-EXCHANGE-NUMBER` / `PAIR-PACKET-WITH-ITS-ANSWER` |
| `CRS-M1-00176` | `DLP-CONSECUTIVE-TFTP-TRANSFER-DEADLINE` | `FINAL-PACKET-OF-INITIATING-TFTP-TRANSFER` → `FIRST-PACKET-OF-NEXT-DLP-TFTP-TRANSFER` | `DLP-OPERATION-ABORTED-OR-FATAL` / `AUTHORIZED-DLP-RETRY-START` | `TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-CONSECUTIVE-TFTP-TRANSFERS-IN-SAME-OPERATION` |
| `CRS-M1-00177` | `TFTP-PACKET-ANSWER-DEADLINE` | `TFTP-PACKET-SENT` → `CORRESPONDING-TFTP-ANSWER-RECEIVED` | `TFTP-TRANSFER-TERMINATED` / `AUTHORIZED-RETRANSMISSION-OF-SAME-EXCHANGE` | `TFTP-TRANSFER-ID-AND-EXCHANGE-NUMBER` / `PAIR-PACKET-WITH-ITS-ANSWER` |
| `CRS-M1-00178` | `TFTP-PACKET-TRANSMISSION-DURATION-BOUND` | `TFTP-PACKET-EMISSION` → `SAME-TFTP-PACKET-RECEPTION` | `PACKET-TRANSFER-CANCELLED` / `NONE` | `TFTP-PACKET-IDENTITY` / `PAIR-EMISSION-WITH-RECEPTION-OF-SAME-PACKET` |
| `CRS-M1-00179` | `TFTP-SUBSCRIBER-PROCESSING-DURATION-BOUND` | `TFTP-PACKET-RECEPTION` → `ASSOCIATED-TFTP-PACKET-EMISSION` | `TFTP-EXCHANGE-TERMINATED` / `NONE` | `TFTP-EXCHANGE-AND-SUBSCRIBER` / `PAIR-RECEIVED-PACKET-WITH-ASSOCIATED-EMITTED-PACKET` |
| `CRS-M1-00184` | `DLP-CONSECUTIVE-TFTP-TRANSFER-DEADLINE` | `FINAL-PACKET-OF-INITIATING-TFTP-TRANSFER` → `FIRST-PACKET-OF-NEXT-DLP-TFTP-TRANSFER` | `DLP-OPERATION-ABORTED-OR-FATAL` / `AUTHORIZED-DLP-RETRY-START` | `TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-CONSECUTIVE-TFTP-TRANSFERS-IN-SAME-OPERATION` |
| `CRS-M1-00185` | `DLP-CONSECUTIVE-TFTP-TRANSFER-DEADLINE` | `FINAL-PACKET-OF-INITIATING-TFTP-TRANSFER` → `FIRST-PACKET-OF-NEXT-DLP-TFTP-TRANSFER` | `DLP-OPERATION-ABORTED-OR-FATAL` / `AUTHORIZED-DLP-RETRY-START` | `TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-CONSECUTIVE-TFTP-TRANSFERS-IN-SAME-OPERATION` |
| `CRS-M1-00186` | `LCS-PRODUCTION-PROHIBITION-WINDOW` | `LCI-LCL-SEQUENCE-INITIATED-BEFORE-DLP-TO-EXPIRY` → `LCS-MUST-NOT-BE-PRODUCED` | `DLP-TO-EXPIRES-OR-SEQUENCE-TERMINATES` / `NEW-LCI-LCL-SEQUENCE` | `TARGET-AND-LCI-LCL-SEQUENCE` / `PAIR-TIMELY-LCI-LCL-SEQUENCE-WITH-LCS-ABSENCE` |
| `CRS-M1-00187` | `DLP-CONSECUTIVE-TFTP-TRANSFER-DEADLINE` | `FINAL-PACKET-OF-INITIATING-TFTP-TRANSFER` → `FIRST-PACKET-OF-NEXT-DLP-TFTP-TRANSFER` | `DLP-OPERATION-ABORTED-OR-FATAL` / `AUTHORIZED-DLP-RETRY-START` | `TARGET-OPERATION-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-CONSECUTIVE-TFTP-TRANSFERS-IN-SAME-OPERATION` |
| `CRS-M1-00188` | `DLP-CONSECUTIVE-TFTP-TRANSFER-EQUATION` | `LAST-PACKET-OF-PREVIOUS-TFTP-RECEIVED` → `FIRST-PACKET-OF-NEXT-TFTP-EMITTED` | `DLP-OPERATION-TERMINATED` / `NEW-DLP-SEQUENCE-STARTED` | `TARGET-AND-DLP-TRANSFER-SEQUENCE` / `PAIR-PREVIOUS-LAST-RECEPTION-WITH-NEXT-FIRST-EMISSION` |
| `CRS-M1-00305` | `STATUS-EXCEPTION-SILENCE-DEADLINE` | `STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` → `FIRST-TARGET-STATUS-OR-RESPONSE-AFTER-SILENCE` | `OPERATION-ABORTED-OR-FATAL` / `NEWER-STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` | `TARGET-OPERATION-AND-STATUS-FILE-INSTANCE` / `PAIR-EXCEPTION-TIMER-WITH-TARGET-SILENCE-INTERVAL` |
| `CRS-M1-00322` | `STATUS-EXCEPTION-SILENCE-DEADLINE` | `STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` → `FIRST-TARGET-STATUS-OR-RESPONSE-AFTER-SILENCE` | `OPERATION-ABORTED-OR-FATAL` / `NEWER-STATUS-FILE-WITH-EXCEPTION-TIMER-RECEIVED` | `TARGET-OPERATION-AND-STATUS-FILE-INSTANCE` / `PAIR-EXCEPTION-TIMER-WITH-TARGET-SILENCE-INTERVAL` |
| `CRS-M1-00391` | `FIND-HOST-ANSWER-DEADLINE` | `FIND-REQUEST-RECEIVED-BY-HOST` → `FIND-ANSWER-SENT-BY-HOST` | `PROJECT-ASSUMPTION-UNRESOLVED-FIND-ABORT` / `NONE` | `FIND-REQUEST-INSTANCE` / `PAIR-FIND-REQUEST-WITH-HOST-ANSWER` |
| `CRS-M1-00520` | `FIND-ANSWER-REGISTRATION-WINDOW` | `FIND-REQUEST-SENT` → `FIND-ANSWER-WINDOW-LIFETIME-ELAPSED` | `PROJECT-ASSUMPTION-UNRESOLVED-FIND-ABORT` / `NONE` | `FIND-REQUEST-INSTANCE` / `PAIR-FIND-REQUEST-WITH-REGISTRATION-WINDOW` |
| `CRS-M1-00521` | `FIND-REGISTRATION-CLOSE-AT-EXPIRY` | `FIND-REQUEST-SENT` → `FIND-ANSWER-REGISTRATION-CLOSED` | `PROJECT-ASSUMPTION-UNRESOLVED-FIND-ABORT` / `NONE` | `FIND-REQUEST-INSTANCE` / `PAIR-FIND-REQUEST-WITH-REGISTRATION-CLOSE` |

## 需求级 615A → 665-5 追溯

| 665-5 CRS | Profile 范围准入 | 处置 | 需求特定关系 |
|---|---|---|---|
| `CRS-M1-00191` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00192` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00193` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00194` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00195` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00196` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00197` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00198` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00199` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00200` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00201` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00202` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00203` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00204` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00205` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00206` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00207` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00208` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00209` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00210` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00211` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00212` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00213` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00214` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00215` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00216` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00217` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00218` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00219` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00220` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00221` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00222` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00223` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00224` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00225` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00226` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00227` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00228` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00229` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00230` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00231` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00232` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00233` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00234` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00235` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00236` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00237` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00238` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00239` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00240` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00241` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00242` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00243` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00244` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00245` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00246` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00247` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00248` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00249` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00250` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `DEPENDENCY-BLOCKED` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00251` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |
| `CRS-M1-00252` | `CRS-M1-00001`, `CRS-M1-00016`, `CRS-M1-00018`, `CRS-M1-00042`, `CRS-M1-00046`, `CRS-M1-00085` | `PROFILE-SCOPE-ONLY` — ARINC 665-5 由有界 Profile 范围准入；该来源命题本身不建立来自某一特定 ARINC 615A-3 需求的直接蕴含关系。 | — |

## 结构化协议文件字段约束

| CRS | 文件／序号 | 字段 | 位宽 | 重复／出现／使用 | 编码／终止 | 注释 |
|---|---|---|---|---|---|---|
| `CRS-M1-00282` | `LCI` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00283` | `LCI` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00284` | `LCI` / `3` | `FIELD-OPERATION-ACCEPTANCE-STATUS-CODE` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00285` | `LCI` / `4` | `FIELD-STATUS-DESCRIPTION-LENGTH` | `8` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00286` | `LCI` / `5` | `FIELD-STATUS-DESCRIPTION` | `0..2040` | `ONCE` / `WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00287` | `LCL` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00288` | `LCL` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00289` | `LCL` / `3` | `FIELD-NUMBER-OF-TARGET-HARDWARE` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00290` | `LCL` / `4` | `FIELD-LITERAL-NAME-LENGTH` | `8` | `PER-LITERAL-NAME` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00291` | `LCL` / `5` | `FIELD-LITERAL-NAME` | `8..2040` | `PER-LITERAL-NAME` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00292` | `LCL` / `6` | `FIELD-SERIAL-NUMBER-LENGTH` | `8` | `PER-LITERAL-NAME` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00293` | `LCL` / `7` | `FIELD-SERIAL-NUMBER` | `8..2040` | `PER-LITERAL-NAME` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00294` | `LCL` / `8` | `FIELD-NUMBER-OF-PART-NUMBERS` | `16` | `PER-LITERAL-NAME` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00295` | `LCL` / `9` | `FIELD-PART-NUMBER-LENGTH` | `8` | `PER-PART-NUMBER-WITHIN-LITERAL-NAME` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00296` | `LCL` / `10` | `FIELD-PART-NUMBER` | `8..2040` | `PER-PART-NUMBER-WITHIN-LITERAL-NAME` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00297` | `LCL` / `11` | `FIELD-AMENDMENT-LENGTH` | `8` | `PER-PART-NUMBER-WITHIN-LITERAL-NAME` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00298` | `LCL` / `12` | `FIELD-AMENDMENT` | `0..2040` | `PER-PART-NUMBER-WITHIN-LITERAL-NAME` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00299` | `LCL` / `13` | `FIELD-PART-DESIGNATION-LENGTH` | `8` | `PER-PART-NUMBER-WITHIN-LITERAL-NAME` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00300` | `LCL` / `14` | `FIELD-PART-DESIGNATION-TEXT` | `8..2040` | `PER-PART-NUMBER-WITHIN-LITERAL-NAME` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00301` | `LCS` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00302` | `LCS` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00303` | `LCS` / `3` | `FIELD-COUNTER` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00304` | `LCS` / `4` | `FIELD-INFORMATION-OPERATION-STATUS-CODE` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00305` | `LCS` / `5` | `FIELD-EXCEPTION-TIMER` | `16` | `ONCE` / `WHEN-STATUS-CODE-0002-OR-0004` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00306` | `LCS` / `6` | `FIELD-ESTIMATED-TIME` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00307` | `LCS` / `7` | `FIELD-STATUS-DESCRIPTION-LENGTH` | `8` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00308` | `LCS` / `8` | `FIELD-STATUS-DESCRIPTION` | `0..2040` | `ONCE` / `WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00309` | `LUR` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00310` | `LUR` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00311` | `LUR` / `3` | `FIELD-NUMBER-OF-HEADER-FILES` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00312` | `LUR` / `4` | `FIELD-HEADER-FILE-NAME-LENGTH` | `8` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00313` | `LUR` / `5` | `FIELD-HEADER-FILE-NAME` | `8..2040` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00314` | `LUR` / `6` | `FIELD-LOAD-PART-NUMBER-NAME-LENGTH` | `8` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00315` | `LUR` / `7` | `FIELD-LOAD-PART-NUMBER-NAME` | `8..2040` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00316` | `LUS` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00317` | `LUS` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00318` | `LUS` / `3` | `FIELD-UPLOAD-OPERATION-STATUS-CODE` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00319` | `LUS` / `4` | `FIELD-UPLOAD-STATUS-DESCRIPTION-LENGTH` | `8` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00320` | `LUS` / `5` | `FIELD-UPLOAD-STATUS-DESCRIPTION` | `0..2040` | `ONCE` / `WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00321` | `LUS` / `6` | `FIELD-COUNTER` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00322` | `LUS` / `7` | `FIELD-EXCEPTION-TIMER` | `16` | `ONCE` / `WHEN-STATUS-CODE-0002-OR-0004` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00323` | `LUS` / `8` | `FIELD-ESTIMATED-TIME` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00324` | `LUS` / `9` | `FIELD-LOAD-LIST-RATIO` | `24` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00325` | `LUS` / `10` | `FIELD-NUMBER-OF-HEADER-FILES` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00326` | `LUS` / `11` | `FIELD-HEADER-FILE-NAME-LENGTH` | `8` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00327` | `LUS` / `12` | `FIELD-HEADER-FILE-NAME` | `8..2040` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00328` | `LUS` / `13` | `FIELD-LOAD-PART-NUMBER-NAME-LENGTH` | `8` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00329` | `LUS` / `14` | `FIELD-LOAD-PART-NUMBER-NAME` | `8..2040` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00330` | `LUS` / `15` | `FIELD-LOAD-RATIO` | `24` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00331` | `LUS` / `16` | `FIELD-LOAD-STATUS` | `16` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00332` | `LUS` / `17` | `FIELD-LOAD-STATUS-DESCRIPTION-LENGTH` | `8` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | — |
| `CRS-M1-00333` | `LUS` / `18` | `FIELD-LOAD-STATUS-DESCRIPTION` | `0..2040` | `PER-PRECEDING-COUNT-FIELD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | NOTE-1 |
| `CRS-M1-00459` | `LNR` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNR-FILE-LENGTH-32 |
| `CRS-M1-00460` | `LNR` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `FIXED-WIDTH-ASCII` / `FIXED-TWO-ASCII-CHARACTERS` | PROTOCOL-VERSION-TWO-ASCII-CHARACTERS |
| `CRS-M1-00461` | `LNR` / `3` | `FIELD-NUMBER-OF-FILES` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNR-NUMBER-OF-FILES-16 |
| `CRS-M1-00462` | `LNR` / `4` | `FIELD-FILE-NAME-LENGTH` | `8` | `PER-FILE-RECORD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNR-FILE-NAME-LENGTH-REPEAT |
| `CRS-M1-00463` | `LNR` / `5` | `FIELD-FILE-NAME` | `8-TO-2040` | `PER-FILE-RECORD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | LNR-FILE-NAME-REPEAT |
| `CRS-M1-00464` | `LNR` / `6` | `FIELD-USER-DEFINED-DATA-LENGTH` | `8` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNR-USER-DATA-LENGTH-ONCE |
| `CRS-M1-00465` | `LNR` / `7` | `FIELD-USER-DEFINED-DATA` | `0-TO-2040` | `ONCE` / `WHEN-LENGTH-FIELD-POSITIVE` / `—` | `LENGTH-PREFIXED-BINARY` / `LENGTH-PREFIXED-PER-TABLE` | LNR-USER-DATA-ONCE-NOT-PER-FILE |
| `CRS-M1-00466` | `LNS` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-FIELD-FILE-LENGTH-TABLE-WIDTH |
| `CRS-M1-00467` | `LNS` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `FIXED-WIDTH-ASCII` / `FIXED-TWO-ASCII-CHARACTERS` | PROTOCOL-VERSION-TWO-ASCII-CHARACTERS |
| `CRS-M1-00468` | `LNS` / `3` | `FIELD-DOWNLOAD-OPERATION-STATUS-CODE` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-FIELD-DOWNLOAD-OPERATION-STATUS-CODE-TABLE-WIDTH |
| `CRS-M1-00469` | `LNS` / `4` | `FIELD-DOWNLOAD-STATUS-DESCRIPTION-LENGTH` | `8` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-FIELD-DOWNLOAD-STATUS-DESCRIPTION-LENGTH-TABLE-WIDTH |
| `CRS-M1-00470` | `LNS` / `5` | `FIELD-DOWNLOAD-STATUS-DESCRIPTION` | `0-TO-2040` | `ONCE` / `WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | LNS-FIELD-DOWNLOAD-STATUS-DESCRIPTION-TABLE-WIDTH |
| `CRS-M1-00471` | `LNS` / `6` | `FIELD-COUNTER` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-FIELD-COUNTER-TABLE-WIDTH |
| `CRS-M1-00472` | `LNS` / `7` | `FIELD-EXCEPTION-TIMER` | `16` | `ONCE` / `ALWAYS` / `WHEN-STATUS-CODE-0002-OR-0004` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-EXCEPTION-TIMER-WHEN-STATUS-0002-OR-0004 |
| `CRS-M1-00473` | `LNS` / `8` | `FIELD-ESTIMATED-TIME` | `16` | `ONCE` / `ALWAYS` / `WHEN-STATUS-CODE-0002-OR-0004` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-ESTIMATED-TIME-WHEN-STATUS-0002-OR-0004, LNS-ESTIMATED-TIME-UNKNOWN-IS-0xFFFF |
| `CRS-M1-00474` | `LNS` / `9` | `FIELD-DOWNLOAD-LIST-RATIO` | `24` | `ONCE` / `ALWAYS` / `—` | `FIXED-WIDTH-ASCII` / `RIGHT-ADJUSTED-LEADING-BLANKS` | LNS-DOWNLOAD-LIST-RATIO-THREE-ASCII-PERCENT |
| `CRS-M1-00475` | `LNS` / `10` | `FIELD-NUMBER-OF-FILES` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-FIELD-NUMBER-OF-FILES-TABLE-WIDTH |
| `CRS-M1-00476` | `LNS` / `11` | `FIELD-FILE-NAME-LENGTH` | `8` | `PER-FILE-RECORD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-FIELD-FILE-NAME-LENGTH-TABLE-WIDTH |
| `CRS-M1-00477` | `LNS` / `12` | `FIELD-FILE-NAME` | `8-TO-2040` | `PER-FILE-RECORD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | LNS-FIELD-FILE-NAME-TABLE-WIDTH |
| `CRS-M1-00478` | `LNS` / `13` | `FIELD-FILE-STATUS` | `16` | `PER-FILE-RECORD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-FIELD-FILE-STATUS-TABLE-WIDTH |
| `CRS-M1-00479` | `LNS` / `14` | `FIELD-FILE-STATUS-DESCRIPTION-LENGTH` | `8` | `PER-FILE-RECORD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNS-FIELD-FILE-STATUS-DESCRIPTION-LENGTH-TABLE-WIDTH |
| `CRS-M1-00480` | `LNS` / `15` | `FIELD-FILE-STATUS-DESCRIPTION` | `0-TO-2040` | `PER-FILE-RECORD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | LNS-FIELD-FILE-STATUS-DESCRIPTION-TABLE-WIDTH |
| `CRS-M1-00481` | `LNL` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNL-FIELD-FILE-LENGTH-TABLE-WIDTH |
| `CRS-M1-00482` | `LNL` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `FIXED-WIDTH-ASCII` / `FIXED-TWO-ASCII-CHARACTERS` | PROTOCOL-VERSION-TWO-ASCII-CHARACTERS |
| `CRS-M1-00483` | `LNL` / `3` | `FIELD-NUMBER-OF-FILES` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNL-FIELD-NUMBER-OF-FILES-TABLE-WIDTH |
| `CRS-M1-00484` | `LNL` / `4` | `FIELD-FILE-NAME-LENGTH` | `8` | `PER-FILE-RECORD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNL-FIELD-FILE-NAME-LENGTH-TABLE-WIDTH |
| `CRS-M1-00485` | `LNL` / `5` | `FIELD-FILE-NAME` | `8-TO-2040` | `PER-FILE-RECORD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | LNL-FIELD-FILE-NAME-TABLE-WIDTH |
| `CRS-M1-00486` | `LNL` / `6` | `FIELD-FILE-DESCRIPTION-LENGTH` | `8` | `PER-FILE-RECORD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNL-FIELD-FILE-DESCRIPTION-LENGTH-TABLE-WIDTH |
| `CRS-M1-00487` | `LNL` / `7` | `FIELD-FILE-DESCRIPTION` | `0-TO-2040` | `PER-FILE-RECORD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | LNL-FIELD-FILE-DESCRIPTION-TABLE-WIDTH |
| `CRS-M1-00488` | `LNA` / `1` | `FIELD-FILE-LENGTH` | `32` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNA-FIELD-FILE-LENGTH-TABLE-WIDTH |
| `CRS-M1-00489` | `LNA` / `2` | `FIELD-PROTOCOL-VERSION` | `16` | `ONCE` / `ALWAYS` / `—` | `FIXED-WIDTH-ASCII` / `FIXED-TWO-ASCII-CHARACTERS` | PROTOCOL-VERSION-TWO-ASCII-CHARACTERS |
| `CRS-M1-00490` | `LNA` / `3` | `FIELD-NUMBER-OF-FILES` | `16` | `ONCE` / `ALWAYS` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNA-FIELD-NUMBER-OF-FILES-TABLE-WIDTH |
| `CRS-M1-00491` | `LNA` / `4` | `FIELD-FILE-NAME-LENGTH` | `8` | `PER-FILE-RECORD` / `PER-REPETITION-OF-ENCLOSING-BLOCK` / `—` | `UNSIGNED-INT-BIG-ENDIAN` / `NOT-APPLICABLE-OR-PROSE-DEFINED` | LNA-FIELD-FILE-NAME-LENGTH-TABLE-WIDTH |
| `CRS-M1-00492` | `LNA` / `5` | `FIELD-FILE-NAME` | `8-TO-2040` | `PER-FILE-RECORD` / `PER-REPETITION-AND-WHEN-LENGTH-FIELD-POSITIVE` / `—` | `ZERO-TERMINATED-ASCII` / `ZERO-TERMINATED-PER-SECTION-6.4` | LNA-FIELD-FILE-NAME-TABLE-WIDTH |

## 结构化 Table 6.4.10-1 约束

| CRS | 状态码／类型 | 含义／替换 | 显示 | 目标文本 | 文件／操作 |
|---|---|---|---|---|---|
| `CRS-M1-00334` | `0X0001` | `ACCEPTED-NOT-STARTED` | `NO-DISPLAY` | `NOT-SPECIFIED` | `.LCI, .LCS, .LUI, .LUS, .LND, .LNO, .LNS` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00335` | `0X1000` | `OPERATION-DENIED` | `DISPLAY-CONTROLLED-TEMPLATE-AND-TARGET-TEXT` | `REQUIRED` | `.LCI, .LUI, .LND, .LNO` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00336` | `0X1002` | `OPERATION-NOT-SUPPORTED` | `DISPLAY-CONTROLLED-TEMPLATE` | `FORBIDDEN` | `.LCI, .LUI, .LND, .LNO` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00337` | `0X0002` | `IN-PROGRESS` | `ENTERTAIN-USER-WITHOUT-STATUS-TEXT` | `NOT-SPECIFIED` | `.LCS, .LUS, .LNS` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00338` | `0X0003` | `COMPLETED-WITHOUT-ERROR` | `DISPLAY-CONTROLLED-TEMPLATE` | `FORBIDDEN` | `.LCS, .LUS, .LNS` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00339` | `0X0004` | `IN-PROGRESS-WITH-TARGET-DETAIL` | `DISPLAY-TARGET-TEXT` | `REQUIRED` | `.LCS, .LUS, .LNS` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00340` | `0X1003` | `ABORTED-BY-TARGET` | `DISPLAY-CONTROLLED-TEMPLATE-AND-TARGET-TEXT` | `REQUIRED` | `.LCS, .LUS, .LNS` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00341` | `0X1004` | `ABORTED-BY-DATA-LOADER` | `DISPLAY-CONTROLLED-TEMPLATE` | `FORBIDDEN` | `.LCS, .LUS, .LNS` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00342` | `0X1005` | `ABORTED-BY-OPERATOR` | `DISPLAY-CONTROLLED-TEMPLATE` | `FORBIDDEN` | `.LCS, .LUS, .LNS` / `INFORMATION, UPLOAD, DOWNLOAD` |
| `CRS-M1-00343` | `0X1007` | `LOAD-PART-FAILED` | `DISPLAY-IDENTIFIER-AND-FAILURE-TEMPLATE-AND-TARGET-TEXT` | `REQUIRED` | `.LUS` / `UPLOAD` |
| `CRS-M1-00344` | `0X1007` | `DOWNLOAD-FILE-FAILED` | `DISPLAY-IDENTIFIER-AND-FAILURE-TEMPLATE-AND-TARGET-TEXT` | `REQUIRED` | `.LNS` / `DOWNLOAD` |
| `CRS-M1-00345` | `DISPLAY-FOOTNOTE` | `SUBSTITUTE-ACTIVE-OPERATION-NAME` | — | — | — |

## 非基础范围及未决清单

- `COV-M1-00001` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00002` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00003` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00004` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00005` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00006` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00007` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00008` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00009` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00010` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00011` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00012` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00013` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00014` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00015` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00016` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00017` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00018` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00019` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00051` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00052` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00053` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00054` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00055` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00056` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00057` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00058` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00059` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00060` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00061` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00062` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00063` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00064` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00065` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00066` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00067` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00068` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00069` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00070` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00071` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00072` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00073` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00074` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00075` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00076` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00083` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00084` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00085` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00086` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00087` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00088` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00089` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00090` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00091` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00092` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00093` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00094` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00095` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00096` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00097` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00098` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00099` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00100` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00101` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00102` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00103` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00104` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00105` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00106` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00107` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00108` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00109` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00110` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00111` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00112` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00113` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00114` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00115` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00116` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00117` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00118` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00119` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00120` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00121` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00122` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00123` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00124` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00125` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00126` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00127` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00128` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00129` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00130` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00131` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00132` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00133` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00134` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00135` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00136` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00137` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00138` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00139` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00140` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00141` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00142` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00143` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00144` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00145` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00146` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00147` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00148` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00149` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00150` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00151` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00152` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00153` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00154` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00155` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00156` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00157` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00158` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00159` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00160` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00161` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00162` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00163` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00164` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00165` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00166` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00167` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00168` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00169` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00170` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00171` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00172` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00173` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00174` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00175` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00176` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00177` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00178` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00179` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00180` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00181` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00182` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00183` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00184` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00185` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00186` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00187` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00188` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00189` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00190` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00191` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00192` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00193` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00194` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00195` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00196` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00197` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00198` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00199` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00200` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00201` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00202` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00203` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00204` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00205` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00206` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00207` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00208` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00209` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00210` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00211` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00212` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00213` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00214` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00215` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00216` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00217` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00218` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00219` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00220` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00221` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00222` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00223` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00224` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00225` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00226` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00227` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00228` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00229` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00230` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00231` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00232` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00233` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00234` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00235` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00236` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00237` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00238` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00239` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00240` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00241` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00242` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00243` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00244` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00245` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00246` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00247` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00248` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00249` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00250` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00251` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00252` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00253` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00254` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00255` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00256` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00257` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00258` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00259` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00260` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00261` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00262` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00263` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00264` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00265` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00266` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00267` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00268` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00269` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00270` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00271` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00272` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00273` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00274` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00275` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00276` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00277` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00278` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00279` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00280` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00281` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00282` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00283` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00284` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00285` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00286` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00287` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00288` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00289` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00290` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00291` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00292` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00293` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00294` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00295` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00296` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00297` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00298` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00299` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00300` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00301` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00302` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00303` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00304` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00305` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00306` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00307` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00308` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00309` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00310` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00311` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00312` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00313` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00314` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00315` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00316` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00317` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00318` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00319` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00320` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00321` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00322` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00323` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00324` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00325` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00326` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00327` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00328` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00329` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00330` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00331` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00332` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00333` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00334` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00335` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00336` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00337` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00338` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00339` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00340` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00341` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00342` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00343` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00344` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00345` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00346` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00347` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00348` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00349` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00350` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00351` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00352` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00353` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00354` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00355` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-00692` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00693` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00694` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00696` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-00697` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-00698` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-00699` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-00700` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-00701` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-00702` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00703` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00704` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00705` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00706` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00707` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00708` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00709` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00710` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00711` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00712` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00713` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00714` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00715` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00716` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00717` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00718` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00719` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00720` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00721` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00722` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00723` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00724` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00725` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00726` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00727` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00728` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00729` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00730` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00731` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00732` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00733` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00734` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00735` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION-DESCRIPTION
- `COV-M1-00736` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION
- `COV-M1-00737` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION
- `COV-M1-00738` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION
- `COV-M1-00739` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION
- `COV-M1-00740` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION
- `COV-M1-00741` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION
- `COV-M1-00742` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION
- `COV-M1-00743` — `CONDITIONAL` — DOWNLOAD-MEDIA-ORGANIZATION-DESCRIPTION
- `COV-M1-00744` — `OUT-OF-PROFILE` — NON-NORMATIVE-DOWNLOAD-EXAMPLE
- `COV-M1-00745` — `OUT-OF-PROFILE` — NON-NORMATIVE-DOWNLOAD-EXAMPLE
- `COV-M1-00746` — `OUT-OF-PROFILE` — NON-NORMATIVE-DOWNLOAD-EXAMPLE
- `COV-M1-00804` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00805` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00806` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00807` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00808` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00809` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00810` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00811` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00812` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00813` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00814` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00815` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00816` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00817` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00818` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-00819` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00820` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00821` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00822` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00823` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00824` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00825` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00826` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00827` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00828` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00829` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00830` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00916` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00917` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00918` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00919` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00920` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00921` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00922` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00923` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00924` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00925` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00926` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00927` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00928` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00929` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00930` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00931` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00932` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00933` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00934` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00935` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00936` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00937` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00938` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00939` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00940` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00941` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00942` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00943` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00944` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00945` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00946` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00947` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00948` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00949` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00950` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00951` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00952` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00953` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00954` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00955` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00956` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00957` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00958` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00959` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00960` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00961` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00962` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00963` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00964` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00965` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00966` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00967` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-00968` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00969` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-00970` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00971` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00972` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00973` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00974` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00975` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00976` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-00977` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00978` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00979` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00980` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00981` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-00982` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00983` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-00984` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-00985` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00986` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00987` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00988` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00989` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00990` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00991` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00992` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00993` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-00994` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-00995` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-00996` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-00997` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01273` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01274` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01275` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01276` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01277` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01278` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01279` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01280` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01281` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01282` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01283` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01284` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01285` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01286` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01287` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01288` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-01289` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01290` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01291` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01292` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED-DESCRIPTION
- `COV-M1-01293` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01294` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01295` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01296` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01297` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01298` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01299` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01300` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01301` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01302` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01303` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01304` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01305` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01306` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01307` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01308` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01309` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01310` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01311` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01312` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01313` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01314` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01315` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01316` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01317` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01318` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01319` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01320` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01321` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01322` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01323` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01324` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01325` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01326` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01327` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01328` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01329` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01330` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01331` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01332` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01333` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01334` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01335` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01336` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01337` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01338` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01339` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01340` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01341` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01342` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01343` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01344` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01345` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01346` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01347` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01348` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01349` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01350` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01351` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01352` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01353` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01354` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01355` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01356` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01357` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01358` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01359` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01360` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01361` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01362` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01363` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01364` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01365` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01366` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01367` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01368` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01369` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01370` — `CONDITIONAL` — DOWNLOAD-SHARED-DESCRIPTION
- `COV-M1-01371` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01372` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-01373` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01374` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01375` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01376` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01377` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01378` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01379` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01380` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01381` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01382` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01383` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01384` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01385` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01386` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01387` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-01388` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01389` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01390` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01391` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01392` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-01393` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-01394` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01395` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01396` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01397` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01398` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01399` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01400` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01401` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01402` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01403` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01404` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01405` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01406` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01407` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01408` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED-DESCRIPTION
- `COV-M1-01409` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-01413` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01414` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01415` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01416` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01417` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01418` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01419` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01420` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01421` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01422` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01423` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01424` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01425` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01426` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01427` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01428` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01429` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01430` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01431` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01432` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01433` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01434` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01435` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01436` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01437` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01438` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01439` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01440` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01441` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01442` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01443` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01444` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01445` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01446` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01447` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01448` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01449` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01450` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01451` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01452` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01453` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01454` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01455` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01456` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01457` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01458` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01459` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01460` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01461` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01462` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01463` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01464` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01465` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01466` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01467` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01468` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01469` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01470` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01471` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01472` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01473` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01474` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01475` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01476` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01477` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01478` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01479` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01480` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01481` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01482` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01483` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01484` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01485` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01486` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01487` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01488` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01489` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01490` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01491` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01492` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01493` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01494` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01495` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01496` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01497` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01498` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01499` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01500` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01501` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01502` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01503` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01504` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01505` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01506` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01507` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01508` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01509` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01510` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01511` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01512` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01513` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01514` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01515` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01516` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01517` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01518` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01519` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01520` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01521` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01522` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01523` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01524` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01525` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01526` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01527` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01528` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01529` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01530` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01531` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01532` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01533` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01534` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01535` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01536` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01537` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01538` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01539` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01540` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01541` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01542` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01543` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01544` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01545` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01546` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01547` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01548` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01549` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01550` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01551` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01552` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01553` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01554` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01555` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01556` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01557` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01558` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01559` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01560` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01561` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01562` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01563` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01564` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01565` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01566` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01567` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01568` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01569` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01570` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01571` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01572` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01573` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01574` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01575` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01576` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01577` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01578` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01579` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01580` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01581` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01586` — `CONDITIONAL` — FIND-CONDITIONAL-DESCRIPTION
- `COV-M1-01587` — `CONDITIONAL` — FIND-CONDITIONAL-NETWORK-OR-PRELOAD
- `COV-M1-01588` — `CONDITIONAL` — FIND-CONDITIONAL-NETWORK-OR-PRELOAD
- `COV-M1-01589` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01590` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01591` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01592` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01593` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01596` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01597` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01598` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01599` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01604` — `CONDITIONAL` — FIND-CONDITIONAL-DESCRIPTION
- `COV-M1-01612` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01622` — `CONDITIONAL` — FIND-CONDITIONAL-NETWORK-OR-PRELOAD
- `COV-M1-01624` — `CONDITIONAL` — FIND-CONDITIONAL-NETWORK-OR-PRELOAD
- `COV-M1-01632` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01645` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-COMMENTARY
- `COV-M1-01652` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-EXAMPLE
- `COV-M1-01653` — `OUT-OF-PROFILE` — NON-NORMATIVE-FIND-EXAMPLE
- `COV-M1-01654` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01684` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01685` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01686` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01701` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01702` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01720` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01735` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01736` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01737` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01747` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01748` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01756` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01757` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01758` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01759` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01760` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01761` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01762` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01763` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01764` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01765` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01766` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01767` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01768` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01769` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01770` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01771` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01772` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01773` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01774` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01775` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01776` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01777` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01778` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01779` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01780` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01781` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01782` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01783` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01784` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01785` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01786` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01787` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01788` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01789` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01790` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01791` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01792` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01793` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01794` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01795` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01796` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01797` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01798` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01799` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01800` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01801` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01802` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01803` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01804` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01805` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01806` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01807` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01808` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01809` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01810` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01811` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01812` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01813` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01814` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01815` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01816` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01817` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01818` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01819` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01820` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01821` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01822` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01823` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01824` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01825` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01826` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01827` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01828` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01829` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01830` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01831` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01832` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01833` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01834` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01835` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01836` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01837` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01838` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01839` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01840` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01841` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01842` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01843` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01844` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01845` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01846` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01847` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01848` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01849` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01850` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01851` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01852` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01853` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01854` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01855` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01856` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01857` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01858` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01859` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01860` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01861` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01862` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01863` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01864` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01865` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01866` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01867` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01868` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01869` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01870` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01871` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01872` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01873` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01874` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01875` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01876` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01877` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01878` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01879` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01880` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01881` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01882` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01883` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01884` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01885` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01886` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01887` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01888` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01889` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01890` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01891` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01892` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01893` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01894` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01895` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01896` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01897` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01898` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01899` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01900` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01901` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01902` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01903` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01904` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01905` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01906` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01907` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01908` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01909` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01910` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01911` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01912` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01913` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01914` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01915` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01916` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01917` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01918` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01919` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01920` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01921` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01922` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01923` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01924` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01925` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01926` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01927` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01928` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01929` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01930` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01931` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01932` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01933` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01934` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01935` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01936` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01937` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01938` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01939` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01940` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01941` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01942` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01943` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01944` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01945` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01946` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01947` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01948` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01949` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01950` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01951` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01952` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01953` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01954` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01955` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01956` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01957` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01958` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01959` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01960` — `OUT-OF-PROFILE` — NON-NORMATIVE-AFDX-EXAMPLE
- `COV-M1-01961` — `OUT-OF-PROFILE` — NON-NORMATIVE-AFDX-EXAMPLE
- `COV-M1-01962` — `CONDITIONAL` — AFDX-CONDITIONAL-DESCRIPTION
- `COV-M1-01963` — `CONDITIONAL` — AFDX-CONDITIONAL-DESCRIPTION
- `COV-M1-01964` — `OUT-OF-PROFILE` — NON-NORMATIVE-AFDX-EXAMPLE
- `COV-M1-01965` — `OUT-OF-PROFILE` — NON-NORMATIVE-AFDX-EXAMPLE
- `COV-M1-01966` — `OUT-OF-PROFILE` — NON-NORMATIVE-AFDX-EXAMPLE
- `COV-M1-01967` — `CONDITIONAL` — AFDX-CONDITIONAL-DEPLOYMENT
- `COV-M1-01968` — `CONDITIONAL` — AFDX-CONDITIONAL-DESCRIPTION
- `COV-M1-01969` — `CONDITIONAL` — AFDX-CONDITIONAL-DESCRIPTION
- `COV-M1-01970` — `CONDITIONAL` — AFDX-CONDITIONAL-DEPLOYMENT
- `COV-M1-01971` — `CONDITIONAL` — AFDX-CONDITIONAL-DESCRIPTION
- `COV-M1-01972` — `CONDITIONAL` — AFDX-CONDITIONAL-DEPLOYMENT
- `COV-M1-01973` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01974` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01975` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01976` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01977` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01978` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01979` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01980` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01981` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01982` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01983` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01984` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01985` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01986` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01987` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01988` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01989` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01990` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01991` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01992` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01993` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01994` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01995` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01996` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01997` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01998` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-01999` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02000` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02001` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02002` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02003` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02004` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02005` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02006` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02007` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02008` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02009` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02010` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02011` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02012` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02013` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02014` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02015` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02016` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02017` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02018` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02019` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02020` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02021` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02022` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02023` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02024` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02025` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02026` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02027` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02028` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02029` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02030` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02031` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02032` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02033` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02034` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02035` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02036` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02037` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02038` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02039` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02040` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02041` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02042` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02043` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02044` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02045` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02046` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02047` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02048` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02049` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02050` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02051` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02052` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02053` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02054` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02055` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02056` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02057` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02058` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02059` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02060` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02061` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02062` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02063` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02064` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02065` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02066` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02067` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02068` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02069` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02070` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02071` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02072` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02073` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02074` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02075` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02076` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02077` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02078` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02079` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02080` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02081` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02082` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02083` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02084` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02085` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02086` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02087` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02088` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02089` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02090` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02091` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02092` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02093` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02094` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02095` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02096` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02097` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02098` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02099` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02100` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02101` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02102` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02103` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02104` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02105` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02106` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02107` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02108` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02109` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02110` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02111` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02112` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02113` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02114` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02115` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02116` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02117` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02118` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02119` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02120` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02121` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02122` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02123` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02124` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02125` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02126` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02127` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02128` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02129` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02130` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02131` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02132` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02133` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02134` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02135` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02136` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02137` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02138` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02139` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02140` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02141` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02142` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02143` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02144` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02145` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02146` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02147` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02148` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02149` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02150` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02151` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02152` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02153` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02154` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02155` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02156` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02157` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02158` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02159` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02160` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02161` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02162` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02163` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02164` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02165` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02166` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02167` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02168` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02169` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02170` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02171` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02172` — `OUT-OF-PROFILE` — NON-PROTOCOL-PRODUCT-OR-INFORMATIVE
- `COV-M1-02173` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02174` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02175` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02176` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02177` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02178` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02179` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02180` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02181` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02182` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02183` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02255` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02256` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02257` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02258` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02259` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02260` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02261` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02308` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02309` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02310` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02311` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02312` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02313` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02314` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02315` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02316` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02317` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02318` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02553` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02554` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02555` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02556` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02557` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02558` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02559` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02560` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02561` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02562` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02563` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02564` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02565` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02566` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02567` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02568` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02569` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02570` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02571` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02572` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02573` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02574` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02575` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02576` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02577` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02578` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02579` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02580` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02581` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02582` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02583` — `OUT-OF-PROFILE` — NOT-TRIGGERED-BY-CURRENT-SERVICE
- `COV-M1-02681` — `OUT-OF-PROFILE` — NON-NORMATIVE-DOWNLOAD-COMMENTARY
- `COV-M1-02682` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02683` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02684` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02685` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02686` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02687` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02688` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02689` — `OUT-OF-PROFILE` — NON-NORMATIVE-DOWNLOAD-COMMENTARY
- `COV-M1-02690` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02691` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02692` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02693` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02694` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02695` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02696` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02697` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02698` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02699` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02700` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02701` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02702` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02703` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02704` — `CONDITIONAL` — DOWNLOAD-SHARED
- `COV-M1-02705` — `OUT-OF-PROFILE` — NON-NORMATIVE-DOWNLOAD-COMMENTARY
- `COV-M1-02706` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02707` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02708` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02709` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02710` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02711` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02712` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02713` — `OUT-OF-PROFILE` — NON-NORMATIVE-DOWNLOAD-COMMENTARY
- `COV-M1-02714` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02715` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02716` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02717` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02718` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02762` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02763` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02764` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02765` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02766` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02767` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02768` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02769` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02770` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02771` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02772` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02773` — `CONDITIONAL` — DOWNLOAD-MEDIA-DEFINED
- `COV-M1-02774` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02775` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02776` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02777` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02778` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02779` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02780` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02781` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02782` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02783` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02784` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
- `COV-M1-02785` — `CONDITIONAL` — DOWNLOAD-OPERATOR-DEFINED
