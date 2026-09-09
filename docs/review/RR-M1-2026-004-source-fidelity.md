# RR-M1-2026-004 — Source-fidelity audit against local reference PDFs

**Auditor role.** Assistant-driven cross-check against the three local reference PDFs made available by the user in `local-references/`. Not an independent external RG0/RG1 review; the WO Section 7 sign-off template still applies for formal approval.

- Candidate Head: `557946ba87c3f22aaa1b8f24a8ccfded069abb87`
- Reference PDFs consulted (proprietary; **no verbatim text has been copied into Git**):
  - `local-references/ARINC615A-3.pdf` — 174 pages, `sha256=918eff7afd7e88a312f07c5a0cefea1c70e31e95dc727716e92005bc96f02511` (matches `controlled_sources.json`)
  - `local-references/ARINC 665-5.pdf` — 139 pages, `sha256=340cfbac1788ee3409d4b5f58f715fa37b19c69c105d311ed4d540f9350da9d8` (matches `controlled_sources.json`)
  - `local-references/ARINC664P2.pdf` — 53 pages, `sha256=177594eed4cb8a13f370a1a3ded88baf881816f83ab0528eb435acad621063d5` (**not yet in `controlled_sources.json`**)

## 1. Bounded scope reminder

The candidate M1 CRS covers only what the current `profileScope` admits:

- `baseOperation = UPLOAD`, `supportingOperation = INFORMATION`, `deferredOperations = [DOWNLOAD, FIND]`.
- ARINC 615A-3 is the sole active protocol authority (`CURRENT-PROTOCOL-AUTHORITY`).
- ARINC 665-5 is admitted only as bounded data-format reference for the LSP header/data/support file structure that UPLOAD carries; `bounded665EdgePolicy` defers any 615A-to-665 requirement-level refinement to M2.
- ARINC 645, ARINC 664 Parts 2 and 3, and RFC 768/791/1123/1350/1785/2347/2348/2349 are open dependencies. Their capabilities remain `NOT-ESTABLISHED`.

Anything outside that bounded scope is expected to be `OUT-OF-PROFILE`, `DEFERRED-FUTURE-SCOPE`, or in `openDependencies`, not a CRS requirement.

## 2. Structural coverage against the actual PDFs

### 615A-3

| PDF area | Leaf units | CRS items | Assessment |
|---|---|---|---|
| Front matter (PDF 1-12) | excluded | 0 | ✅ correctly excluded by `m1_source_section_spans.excludedRanges` |
| §1 Introduction (PDF 13-18) | 90 | 16 | ✅ 16 items promoted are the interpretation and modality-related rules |
| §2 Interchangeability (PDF 19-25) | 107 | 0 | ✅ hardware form-factor / environmental; correctly `OUT-OF-PROFILE` with `NON-PROTOCOL-PRODUCT-OR-INFORMATIVE` |
| §3 Unit Design (PDF 26-28) | 73 | 0 | ✅ controls/self-load/UX; correctly `OUT-OF-PROFILE` |
| §4 Software Transport Media (PDF 29-33) | 85 | 0 | ✅ legacy floppy/PC-card/USB/optical; correctly `OUT-OF-PROFILE` for Ethernet-only 615A-3 |
| §5 Load Protocol (PDF 34-53) | 404 | 76 | ✅ every §5.x subclause represented (5.1, 5.2, 5.3.1, 5.3.2 through 5.3.2.3.9, 5.3.3 FIND deferred, 5.3.4, 5.4.1-5.4.5.x) |
| §6 Load Protocol Definition (PDF 54-97) | 863 | 206 | ✅ every §6.x subclause represented; §6.4.1-6.4.10 protocol-file tables all present |
| Attachment 1 Connector (PDF 98-99) | 38 | 10 | ✅ connector signal assignments |
| Attachment 2 Load Scenarios (PDF 100-106) | 25 | 0 | ✅ narrative scenarios; correctly informative |
| Attachment 3 FIND (PDF 107-110) | 18 (as `ATTACHMENT-3`) + 20 (as `A-3.*`) | 7 | ⚠️ mixed — §5.3.3 FIND is `DEFERRED-FIND-M9` (5 leaves) but Attachment 3 body is currently `NON-PROTOCOL-PRODUCT-OR-INFORMATIVE`; inconsistent classification (see Finding F-1) |
| Attachment 4 Time-Out and Retry (PDF 111-121) | 49 | 7 (CRS) + 23 (timing rows) | ✅ 23 timing objects cover the numerical / symbolic constants (DLP-TO, TFTP-TO, DLP-RETRY, TFTP-RETRY, EXCEPTION-DELAY, MESSAGE-TIMER-VALUE); 3 EQUATION units added under WO-M1-2026-003 |
| Attachment 5 Environmental Test (PDF 122-133) | 24 | 0 | ✅ environmental categories; correctly informative |
| Appendix A Human Interface (PDF 123) | 6 | 0 | ✅ informative |
| Appendix B Reference Guide (PDF 125) | 13 | 0 | ✅ informative |
| Appendix C Acronyms (PDF 127) | 4 | 0 | ✅ informative |
| Appendix D Glossary (PDF 129-133) | 72 | 0 | ✅ informative |
| Appendix E Data Loading Over AFDX (PDF 134) | 13 | 0 | ⚠️ currently entirely `NON-PROTOCOL-PRODUCT-OR-INFORMATIVE`; AFDX deployment carries deployment-normative constraints — see Finding F-2 |
| Appendix F Protocol File Examples (PDF 135-136) | 17 | 0 | ✅ examples — informative |
| Appendix G TFTP Examples (PDF 137-145) | 183 | 0 | ✅ examples — informative |
| Supplement change-summaries (PDF 155-157, 161-164, 167-174) | leaf inventory + supplement register | 0 CRS (register only) | ✅ page-by-page dispositions in `m1_supplement_dispositions.json` |
| Non-normative front/back matter (PDF 146-154, 158-160, 165-166) | excluded | 0 | ✅ correctly excluded |

Every 615A-3 PDF page is accounted by a controlled section span or an explicit exclusion range (`page_account_errors` returns empty).

### 665-5

| PDF area | Leaf units | CRS items | Assessment |
|---|---|---|---|
| Front matter (PDF 1-10) | excluded | 0 | ✅ excluded |
| §1 Introduction (PDF 11-14) | 88 | 5 | ✅ purpose, applicability, terminology, target hardware ID, electronic distribution |
| §2 Loadable Software Parts (PDF 15-31) | 322 | 57 | ✅ software load PN, header file with all 63 pointer fields, data file, support file, batch file part |
| §3 Loadable Media Set Parts (PDF 32-45) | not in inventory | 0 | ⚠️ excluded by page range but rationale is only "back matter"; should be an explicit `BOUNDED-6655-SCOPE-EXCLUSION-MEDIA-SET-NOT-USED-BY-ETHERNET-UPLOAD` — see Finding F-3 |
| §4 Media Set File Format (PDF 46-?) | not in inventory | 0 | ⚠️ same as F-3 |
| §5 onward (PDF ?-139) | not in inventory | 0 | ⚠️ same as F-3 |
| Back matter / supplement summaries | excluded | 0 | ✅ excluded |

The bounded scope excludes 665-5 pages 32-139 by page range. That is defensible under the current `UPLOAD + INFORMATION` Profile because Ethernet-only 615A-3 does not deliver via physical media, but the CRS should record **why** those pages are out-of-scope, not just **that** they are outside the page range.

### 664 Part 2 (Ethernet Physical + Data Link Layer)

- PDF present, `sha256=177594eed4cb8a13f370a1a3ded88baf881816f83ab0528eb435acad621063d5`, 53 pages, publication date 2003-06-10.
- Not yet registered in `configs/research/controlled_sources.json` — still shown as `openDependencies` entry with `ETHERNET-PHYSICAL-LINK-SEMANTICS` capability blocked.
- Now available to bind: 615A-3 Ethernet transport (§5, Attachment 4 timing, Appendix E AFDX) can be sourced against 664 P2 §2 (General Description), §3 (Physical Layer Specification), and the MAC-frame / addressing subsections — see Finding F-4.

## 3. Findings

### F-1 — Attachment 3 (FIND) inconsistent classification (Must, before M2)

Main-body §5.3.3 references to FIND are `DEFERRED-FUTURE-SCOPE` with rationale `DEFERRED-FIND-M9`. Attachment 3 provides the full FIND definition (message flow, discovery semantics, timeout behaviour) — currently classified `NON-PROTOCOL-PRODUCT-OR-INFORMATIVE`. This is inconsistent: an informative appendix cannot supply the definition of a deferred normative behaviour.

**Required correction:** reclassify all Attachment 3 leaf units that carry normative FIND obligations from `NON-PROTOCOL-PRODUCT-OR-INFORMATIVE` to `DEFERRED-FUTURE-SCOPE` with rationale `DEFERRED-FIND-M9`. Purely narrative sentences (e.g., "This attachment describes…") can remain informative.

### F-2 — Appendix E (AFDX) has no explicit deferral or dependency binding (Must, before M2)

Appendix E "Data Loading Over AFDX" — 13 leaf units, all `NON-PROTOCOL-PRODUCT-OR-INFORMATIVE`. This appendix specifies AFDX-specific configuration constraints for 615A-3 deployments over AFDX networks. Two problems:

1. The appendix is not purely informative — its rules constrain any implementation that chooses AFDX transport.
2. AFDX is defined by ARINC 664 Part 7 (not yet acquired) resting on ARINC 664 Part 2 physical/link layer (now available).

**Required correction:** replace the informative classification with either

- `DEFERRED-FUTURE-SCOPE` + rationale `DEFERRED-AFDX-DEPLOYMENT-M2-INFRASTRUCTURE-BINDING`, OR
- `APPLICABLE-CONDITIONAL` with a new `deploymentCondition = "IF-AFDX-TRANSPORT-CHOSEN"` and dependencies `DEP-ARINC-664-2` (bound after F-4) + a new `DEP-ARINC-664-7` (open until acquired).

The second option is preferable because it preserves the normative status while making the AFDX condition explicit.

### F-3 — 665-5 pages 32-139 excluded by range without a bounded-scope rationale (Should)

`m1_source_section_spans.json` excludes 665-5 pages 32-139 as trailing "back matter". In truth, that page range contains normative material (§3 Loadable Media Set Parts, §4 Media Set File Format, batch/media file structures) that is simply outside the Ethernet-only UPLOAD Profile. External RG0 should see an explicit scope-exclusion note.

**Required correction:** add a `boundedSourceScopeExclusion` array to the section-span manifest (or an equivalent record) that lists each excluded 665-5 clause with rationale `BOUNDED-6655-SCOPE-EXCLUSION-MEDIA-SET-NOT-USED-BY-ETHERNET-UPLOAD`. If M9 later activates media-based delivery, the exclusion can be lifted with a controlled CR.

### F-4 — 664 P2 is available and should be bound (Should)

The PDF is present with a stable `sha256=177594eed4cb8a13f370a1a3ded88baf881816f83ab0528eb435acad621063d5`. Currently 615A-3 §5 (Ethernet transport) has open `ETHERNET-PHYSICAL-LINK-SEMANTICS`; two 615A-3 CRS items that presume Ethernet frame semantics (part of the `DEP-ARINC-664-2` dependency set) remain unbound.

**Required correction:** register 664 P2 in `configs/research/controlled_sources.json` under `sources[]` with role `BOUNDED-PHYSICAL-LINK-REFERENCE`, remove it from `openDependencies`, and update `capabilities[ETHERNET-PHYSICAL-LINK-SEMANTICS].status` from `NOT-ESTABLISHED` to `BOUNDED-BY-ARINC-664-2`. Add a `DEP-ARINC-664-2` binding to any CRS requirement that in fact references Ethernet frame semantics.

Do **not** change 615A-3 CRS content on the strength of 664 P2 alone — bindings are additive metadata, not new requirements.

### F-5 — Attachment clause label inconsistency (Nice)

Coverage ledger uses `"A-1.1"`, `"A-2.1"`, `"A-3"`, `"A-4.1"` (alphabetic-prefix Attachment labels) alongside `"4-1"`, `"4-3.1"`, `"4-4.1"` (numeric-prefix labels) that appear in both coverage and requirements. Both notations resolve to Attachment content but the mixing is confusing for reviewers and complicates cross-referencing to the PDF TOC (which uses `ATTACHMENTS 1..5`).

**Required correction (optional, low priority):** harmonize to one convention — recommend `"ATTACHMENT-3"`, `"ATTACHMENT-3.SECTION-1"`, `"ATTACHMENT-4.4.1"` — via a mechanical relabeling pass in `sync_m1_crs.py`. This is purely a display-fidelity fix.

## 4. Standards still needed

The following standards are not yet available in `local-references/` and their absence bounds what M1 (and later stages) can claim. None of these is a M1 approval blocker under the current bounded Profile; they become blockers for specific capabilities and for M2 attachment reconciliation.

| Standard | Blocks | Where needed | Availability |
|---|---|---|---|
| **ARINC 664 Part 7** (AFDX / Deterministic Ethernet) | AFDX deployment binding (F-2), Appendix E of 615A-3 | If AFDX deployment is in scope | Proprietary (SAE ITC) |
| **ARINC 664 Part 3** (Internet-Based Protocols and Services) | `AIRCRAFT-INTERNET-NETWORK-SEMANTICS` capability (`DEP-ARINC-664-3`) | Any claim about IP/UDP over avionics network | Proprietary (SAE ITC) |
| **ARINC 645** (Common Terminology for Data Loading) | `CRC-VALIDATION`, `CHECK-VALUE-VALIDATION`, `NAMING-ALGORITHM-VALIDATION`, `COMPLETE-INTEGRITY-VALIDATION` — 4 capabilities blocked | Any CRC / check-value verdict; already flagged as `GAP-ARINC-645` | Proprietary (SAE ITC) |
| **IETF RFC 768** (UDP) | `UDP-IDENTITY-AND-APPLICABILITY` | Every UDP-relative statement | Public (`https://www.rfc-editor.org/rfc/rfc768.txt`) |
| **IETF RFC 791** (IP) | `IP-IDENTITY-AND-APPLICABILITY` | Every IP-relative statement | Public (`https://www.rfc-editor.org/rfc/rfc791.txt`) |
| **IETF RFC 1123** (Host Requirements) | `HOST-REQUIREMENT-IDENTITY` | Host behaviour claims | Public |
| **IETF RFC 1350** (TFTP v2) | `TFTP-BASE-IDENTITY-AND-APPLICABILITY` | TFTP base protocol | Public |
| **IETF RFC 1785, 2347, 2348, 2349** (TFTP options) | TFTP option-negotiation, option-extension, block-size, timeout / transfer-size | Every TFTP-option statement | Public |

The four IETF RFCs can be added to the controlled sources today (download from `rfc-editor.org`, compute SHA-256, register). The three ARINC parts require acquisition through the SAE ITC store or an equivalent authorized channel.

## 5. What is **not** missing

- Under `bounded scope = UPLOAD + INFORMATION`, no §5 or §6 normative subclause is unrepresented. The 322 615A-3 items correctly project every applicable normative sentence.
- 23 timing objects with 3 independent `EQUATION` evidence units close the Attachment 4 timing surface for the currently-active operations.
- The 62 665-5 items correctly represent the §2 LSP file-format surface. §3 media-set content is outside Profile.
- Every registered PDF page is accounted (`page_account_errors` empty). Every anchor fingerprint recomputes.

If DOWNLOAD or FIND were to be activated (currently M9 in the roadmap), roughly 15 additional CRS items would need to be promoted from `DEFERRED-FUTURE-SCOPE`; they are already in the coverage inventory and would not require new source acquisition.

## 6. Recommendation

- Findings **F-1, F-2** are Must corrections and should be applied before external RG0/RG1 signs off, or at latest before entering M2. They are pure reclassification + new dependency identity; no proprietary text is written to Git.
- Finding **F-3, F-4** are Should corrections. **F-4** unlocks the 664 P2 dependency (available now).
- Finding **F-5** is Nice.
- Standards acquisition: proceed with the four IETF RFCs (public) as an unblocking step; the three ARINC parts remain acquisition tasks with visible impact on M2 attachment reconciliation and AFDX deployment.

Executing F-1..F-4 changes the CRS Head and resets the RG0/RG1 clock on `557946ba…`. A separate work order (WO-M1-2026-004) is recommended; the pre-M2 baseline sequence is in `docs/review/WO-PRE-M2-2026-001.md`.

*Prepared 6 Sep 2026. No proprietary source text has been included in this file.*
