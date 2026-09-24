"""Structural checks for the Package A supporting-source applicability audit."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "configs/research/cltav_protocol_source_audit.json"
SPANS = ROOT / "configs/requirements/m1_source_section_spans.json"

REQUIRED_SOURCES = (
    "ARINC-665-5",
    "ARINC-664-2",
    "ARINC-664-3",
    "ARINC-664-4",
    "ARINC-664-7",
    "RFC-768",
    "RFC-791",
    "RFC-1122",
    "RFC-1123",
    "RFC-1350",
    "RFC-1785",
    "RFC-2347",
    "RFC-2348",
    "RFC-2349",
    "ARINC-645",
)


def audit() -> dict:
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_package_a_sources_are_first_class_tasks_with_denominators() -> None:
    data = audit()
    assert data["applicabilityAuditPending"] == []
    supporting = data["supportingSourceApplicabilityAudit"]
    assert supporting["notIndependentApproval"] is True
    assert supporting["645BindingThisPr"] is True
    head = supporting["boundHead"]
    assert isinstance(head, str) and len(head) == 40
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", head, "HEAD"],
        cwd=ROOT,
        check=False,
    )
    assert ancestor.returncode == 0
    source_ids = [row["sourceId"] for row in supporting["sources"]]
    assert len(source_ids) == len(set(source_ids))
    by_id = {row["sourceId"]: row for row in supporting["sources"]}
    assert list(by_id) == list(REQUIRED_SOURCES)
    for source_id in REQUIRED_SOURCES:
        source = by_id[source_id]
        assert source["status"] == "BOUNDED-AUDIT-COMPLETE"
        assert source["independentApproval"] is False
        denom = source["coverageDenominator"]
        units = source["units"]
        assert denom["count"] == len(units) >= 2
        ids = [row["id"] for row in units]
        assert len(ids) == len(set(ids))
        for row in units:
            assert row["applicabilityDecision"]
            assert row["rationaleCode"]
            assert row["summaryEn"]
            assert row["summaryZh"]
            if row["applicabilityDecision"] == "OUT-OF-PROFILE":
                assert row["leafCrsStatus"] == "NOT-REQUIRED"


def test_665_batch_file_is_inside_survey_and_media_set_was_readjudicated() -> None:
    data = audit()
    source = next(row for row in data["supportingSourceApplicabilityAudit"]["sources"] if row["sourceId"] == "ARINC-665-5")
    batch = next(row for row in source["units"] if row["id"] == "SAU-665-2-3")
    media = next(row for row in source["units"] if row["id"] == "SAU-665-3")
    assert batch["pdfPages"] == [30, 35]
    assert batch["leafCrsStatus"] == "LEAF-CRS-EMITTED"
    assert batch["leafCrsStatus"] != "LEAF-CRS-CLOSED"
    assert batch["applicabilityDecision"] == "APPLICABLE-SUPPORTING"
    crs = json.loads((ROOT / "configs/requirements/arinc_615a3_m1_crs.json").read_text(encoding="utf-8"))
    batch_reqs = [
        row for row in crs["requirements"]
        if row["source"]["sourceId"] == "ARINC-665-5" and str(row["source"].get("clause") or "").startswith("2.3")
    ]
    assert any(row["semantic"]["action"] == "DO-NOT-TRANSFER-BATCH-FILE-TO-TARGET-HARDWARE" for row in batch_reqs)
    assert any(row["semantic"]["action"] == "IDENTIFY-BATCH-FILE-WITH-LUB-EXTENSION" for row in batch_reqs)
    assert any(row["semantic"]["action"] == "POINT-TO-BATCH-FILE-PN-LENGTH-FROM-START-IN-16-BIT-WORDS" for row in batch_reqs)
    assert any(row["semantic"]["action"] == "OMIT-COMMENT-FIELD-WHEN-COMMENT-LENGTH-ZERO" for row in batch_reqs)
    assert any(row["semantic"]["action"] == "KEEP-HEADER-FILE-NAME-FREE-OF-BACKSLASH" for row in batch_reqs)
    assert all(row["reviewStatus"] == "PENDING-EXTERNAL-INDEPENDENT-REVIEW" for row in batch_reqs)
    assert all(row["refinementDisposition"] in {"PROFILE-SCOPE-ONLY", "DEPENDENCY-BLOCKED", "POINTS-TO-BOUND-645-LEAF"} for row in batch_reqs)
    table_rows = [
        row for row in batch_reqs
        if row["source"].get("tableOrFigure") == "Table 2.3.1-1" and row["source"].get("fragmentKind") == "TABLE-ROW"
    ]
    assert len(table_rows) == 22
    for row in table_rows:
        constraint = row["fieldConstraint"]
        assert constraint["protocolFile"] == "LUB"
        assert "TABLE-DEFINED" not in constraint["widthBitsExpression"]
        assert constraint["widthBitsExpression"]
        if "CEILING" in constraint["widthBitsExpression"]:
            assert "LENGTH" in constraint["widthBitsExpression"]
    assert media["pdfPages"] == [36, 54]
    assert media["applicabilityDecision"] == "OUT-OF-PROFILE"
    assert "ETHERNET-UPLOAD" not in media["rationaleCode"]
    spans = json.loads(SPANS.read_text(encoding="utf-8"))
    survey = next(row for row in spans["sources"] if row["sourceId"] == "ARINC-665-5")["spans"][0]
    assert survey["pdfPages"] == [11, 35]
    outside = next(
        row for row in spans["excludedRanges"]
        if row["sourceId"] == "ARINC-665-5" and row["kind"] == "OUTSIDE-BOUNDED-SURVEY"
    )
    assert outside["pdfPages"] == [36, 139]


def test_rfc_identities_stay_unmerged_and_645_is_bound_without_capability() -> None:
    data = audit()
    source_ids = [row["sourceId"] for row in data["supportingSourceApplicabilityAudit"]["sources"]]
    assert "RFC-1350-RFC-2347" not in source_ids
    blocked = data["blockedSource"]
    assert blocked["status"] == "BLOCKED-SOURCE-645"
    assert blocked["localFileAcquired"] is True
    assert blocked["boundThisPr"] is True
    abort = data["supportingSourceApplicabilityAudit"]["findAbortAdjudication"]
    assert abort["status"] == "APPLIED-IN-CRS"
    assert abort["code"] == "FIND-ABORT-DOES-NOT-WAIVE-WINDOWS"
    assert abort["crsCancellation"] == "FIND-ABORT-DOES-NOT-WAIVE-WINDOWS"
    part4 = data["supportingSourceApplicabilityAudit"]["arinc664Part4"]
    assert part4["status"] == "ACQUIRED-IDENTITY-RECORDED"
    assert part4["affectedRequirementId"] == "CRS-M1-00519"
    assert not part4.get("unboundDispositionId")
    dispositions = data["supportingSourceApplicabilityAudit"]["unboundDispositions"]
    assert dispositions == []
    p4_unit = next(
        unit
        for source in data["supportingSourceApplicabilityAudit"]["sources"]
        if source["sourceId"] == "ARINC-664-4"
        for unit in source["units"]
        if unit["id"] == "SAU-P4-ATT-1"
    )
    assert p4_unit["leafCrsStatus"] == "LEAF-CRS-EMITTED"
    assert p4_unit["leafCrsStatus"] != "LEAF-CRS-CLOSED"
    cross = next(
        unit
        for source in data["supportingSourceApplicabilityAudit"]["sources"]
        if source["sourceId"] == "ARINC-664-7"
        for unit in source["units"]
        if unit["id"] == "SAU-P7-P4"
    )
    assert cross["leafCrsStatus"] == "EXISTING-615A-LEAF"
    assert cross["leafRequirementIds"] == ["CRS-M1-00519"]


def test_package_a_does_not_self_approve() -> None:
    data = audit()
    assert data["boundPackage"]["artifactVersion"].startswith("M1-CANDIDATE-")
    supporting = data["supportingSourceApplicabilityAudit"]
    assert supporting["notIndependentApproval"] is True
    assert all(row["independentApproval"] is False for row in supporting["sources"])


ALLOWED_LEAF_STATUS = {
    "NOT-REQUIRED",
    "LEAF-CRS-EMITTED",
    "EXISTING-351-TRIGGERED-ROWS",
    "EXISTING-LEAF-VIA-2-1-2",
    "EXISTING-615A-LEAF",
    "EXISTING-LEAF-VIA-645",
    "CRS-M1-00519-REMAINS-NOT-YET-BOUND",
}


def test_triggered_664_and_rfc_leaves_are_emitted() -> None:
    data = audit()
    leftover = []
    for source in data["supportingSourceApplicabilityAudit"]["sources"]:
        for unit in source["units"]:
            status = unit["leafCrsStatus"]
            if status not in ALLOWED_LEAF_STATUS:
                leftover.append((source["sourceId"], unit["id"], status))
            if (
                source["sourceId"] not in {"ARINC-615A-3", "ARINC-665-5"}
                and unit["conformanceEffect"] == "REQUIRED"
                and unit["applicabilityDecision"] != "OUT-OF-PROFILE"
            ):
                assert status == "LEAF-CRS-EMITTED", (unit["id"], status)
    assert leftover == []
    part4 = data["supportingSourceApplicabilityAudit"]["arinc664Part4"]
    assert part4["affectedRequirementId"] == "CRS-M1-00519"
    crs = json.loads((ROOT / "configs/requirements/arinc_615a3_m1_crs.json").read_text(encoding="utf-8"))
    rfc_rows = [row for row in crs["requirements"] if str(row["source"]["sourceId"]).startswith("RFC-")]
    p3_rows = [row for row in crs["requirements"] if row["source"]["sourceId"] == "ARINC-664-3"]
    p4_rows = [row for row in crs["requirements"] if row["source"]["sourceId"] == "ARINC-664-4"]
    p7_rows = [row for row in crs["requirements"] if row["source"]["sourceId"] == "ARINC-664-7"]
    assert rfc_rows
    assert p3_rows
    assert p4_rows
    assert p7_rows
    assert all(row["reviewStatus"] == "PENDING-EXTERNAL-INDEPENDENT-REVIEW" for row in rfc_rows + p3_rows + p4_rows + p7_rows)
    assert all(row["applicabilityDecision"] == "CONDITIONAL" for row in p4_rows)
    assert all("DEP-ARINC-664-4" in row["dependencyIds"] for row in p4_rows)
    deps = {row["id"]: row for row in crs["dependencies"]}
    for dep_id in ("DEP-RFC-1350", "DEP-RFC-768", "DEP-ARINC-664-3", "DEP-ARINC-664-4", "DEP-ARINC-664-7"):
        assert deps[dep_id]["status"] == "OPEN-DEPENDENCY"
    spans = json.loads(SPANS.read_text(encoding="utf-8"))
    by_id = {row["sourceId"]: row for row in spans["sources"]}
    assert by_id["ARINC-664-2"]["spans"][0]["pdfPages"] == [8, 28]
    assert any(row["pdfPages"] == [8, 36] for row in by_id["ARINC-664-3"]["spans"])
    assert any(row["pdfPages"] == [7, 18] for row in by_id["ARINC-664-4"]["spans"])
    assert "RFC-1350" in by_id
    assert "RFC-768" in by_id
    remaining = {}
    for source in data["supportingSourceApplicabilityAudit"]["sources"]:
        for unit in source["units"]:
            if unit["leafCrsStatus"] == "LEAF-CRS-EMITTED":
                assert unit["leafCoverageIds"]
                assert "leafRequirementIds" in unit
            assert unit["leafCrsStatus"] != "CRS-M1-00519-REMAINS-NOT-YET-BOUND"
            for item in unit.get("remainingSubunits") or []:
                remaining[item["id"]] = item
    assert "SAU-1123-4-2-REMAINING-HOST-NOTE-ATOMS" not in remaining
    assert "SAU-P7-3-REMAINING-VL-BAG-JITTER" not in remaining
    assert "SAU-791-3-1-REMAINING-FIELD-WIDTHS" not in remaining
    assert remaining["SAU-1123-4-2-REMAINING-NETASCII-AND-NONSTANDARD-EXTENSIONS"]["disposition"] == "OUT-OF-PROFILE"
    assert remaining["SAU-1123-4-2-REMAINING-IMPLEMENTATION-EXPONENTIAL-BACKOFF"]["disposition"] == "INFORMATIVE"
    assert "SAU-P7-3-REMAINING-MAX-JITTER-EQUATION-AND-MAC-SOURCE" not in remaining
    assert remaining["SAU-665-2-3-REMAINING-CRC-ALGORITHM-IDENTITY"]["disposition"] == "CAPABILITY-NOT-ESTABLISHED"
    assert remaining["SAU-665-2-3-REMAINING-INFORMATIVE-NOTES-AND-LOCATORS"]["disposition"] == "INFORMATIVE"
    assert "SAU-P3-1-5-REMAINING-RFC-BODY" not in remaining
    assert "SAU-P7-4-REMAINING-SWITCH-BLOCKS" not in remaining
    assert "SAU-P7-ATT2-REMAINING-TABLE-ROWS" not in remaining
    assert remaining["SAU-P7-4-REMAINING-SHOP-OPTIONAL"]["disposition"] == "OUT-OF-PROFILE"
    assert remaining["SAU-P7-4-REMAINING-MIB-SNMP-AND-PERIODIC-STATUS"]["disposition"] == "OUT-OF-PROFILE"
    assert remaining["SAU-P7-4-REMAINING-MIB-SNMP-AND-PERIODIC-STATUS"]["clause"] == "4.6"
    assert remaining["SAU-P7-4-REMAINING-MIB-SNMP-AND-PERIODIC-STATUS"]["pdfPages"] == [65]
    assert "SAU-P7-4-REMAINING-CONFIG-AND-PIN-TABLE-FIELDS" not in remaining
    assert remaining["SAU-P7-4-REMAINING-INTEGRATOR-DEFINED-INIT-AND-PORT-COUNTS"]["disposition"] == "INFORMATIVE"
    assert remaining["SAU-P7-ATT2-REMAINING-TCP-TABLE-2-1"]["disposition"] == "OUT-OF-PROFILE"
    assert "SAU-P7-4-REMAINING-CONFIG-PIN-AND-INTERNAL-DETAILS" not in remaining
    assert "SAU-P7-ATT2-REMAINING-GATEWAY-AND-UNMARKED-ROWS" not in remaining
    assert "SAU-P7-4-REMAINING-CONFIG-PIN-AND-MIB-DETAILS" not in remaining
    assert "SAU-P7-ATT2-REMAINING-TABLE-MARK-LOCATORS" not in remaining
    assert all(
        item["disposition"]
        in {
            "OUT-OF-PROFILE",
            "INFORMATIVE",
            "DEPENDENCY-BLOCKED",
            "CAPABILITY-NOT-ESTABLISHED",
        }
        for item in remaining.values()
    )
    p3 = next(
        unit
        for source in data["supportingSourceApplicabilityAudit"]["sources"]
        if source["sourceId"] == "ARINC-664-3"
        for unit in source["units"]
        if unit["id"] == "SAU-P3-1-5"
    )
    assert len(p3["leafRequirementIds"]) >= 3
    session = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "KEEP-615A-SESSION-ACROSS-OPS-TO-DL-TRANSITION"
    )
    assert session["source"]["clause"] == "4.8.4"
    ip_row = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "REQUIRE-AFDX-END-SYSTEM-INTERNET-LAYER-TO-IMPLEMENT-IP"
    )
    assert ip_row["source"]["clause"] == "ATT-2"
    checksum = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "TREAT-UDP-CHECKSUM-GENERATE-AND-CHECK-AS-NOT-APPLICABLE-ON-AFDX"
    )
    assert checksum["id"] == "CRS-M1-00742"
    assert "NOT APPLICABLE" in checksum["generatedSemanticProjectionEn"]
    assert "CRS-M1-00609" in checksum["generatedSemanticProjectionEn"]
    assert checksum["ambiguityStatus"] == "NONE-OBSERVED"
    assert checksum["gapIds"] == []
    discard = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "TREAT-SILENT-BAD-UDP-CHECKSUM-DISCARD-AS-NOT-APPLICABLE-ON-AFDX"
    )
    assert discard["id"] != checksum["id"]
    assert discard["source"]["clause"] == "ATT-2"
    assert "NOT APPLICABLE" in discard["generatedSemanticProjectionEn"]
    icmp = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "PASS-ICMP-MESSAGES-TO-APPLICATION-LIMITED-TO-ECHO-REQUEST"
    )
    assert "MUST" in icmp["generatedSemanticProjectionEn"]
    assert "NOT APPLICABLE" not in icmp["generatedSemanticProjectionEn"]
    ip_send = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "TREAT-UDP-IP-OPTIONS-SEND-AS-NOT-APPLICABLE-ON-AFDX"
    )
    assert "NOT APPLICABLE" in ip_send["generatedSemanticProjectionEn"]
    assert "CRS-M1-00609" in ip_send["generatedSemanticProjectionEn"]
    gateway = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "TREAT-GATEWAY-FORWARDING-SPEC-AS-NOT-APPLICABLE-ON-AFDX"
    )
    assert "NOT APPLICABLE" in gateway["generatedSemanticProjectionEn"]
    unmarked = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "RECORD-AFDX-GATEWAY-AUTOCONFIGURATION-ROW-UNMARKED"
    )
    assert unmarked["conformanceEffect"] == "INFORMATIVE"
    assert "unmarked" in unmarked["generatedSemanticProjectionEn"]
    assert "CRS-M1-00609 is not applied" in unmarked["generatedSemanticProjectionEn"]
    assert any(
        row["semantic"]["action"] == "PERFORM-OPS-FILTERING-POLICING-SWITCHING-FROM-OPS-CONFIG"
        for row in crs["requirements"]
    )
    assert any(
        row["semantic"]["action"] == "TREAT-DL-UPLOAD-AS-PREFERABLY-EXCLUSIVE" for row in crs["requirements"]
    )
    init_dl = next(row for row in crs["requirements"] if row["id"] == "CRS-M1-00756")
    assert "AND (compatibility checks fail OR no software is loaded)" in init_dl["generatedSemanticProjectionEn"]
    assert "且（兼容性检查失败或无已加载软件）" in init_dl["generatedSemanticProjectionZh"]
    assert any(
        row["semantic"]["action"] == "PROVIDE-OPS-MODE-615A-INFORMATION-AND-FIND" for row in crs["requirements"]
    )
    assert any(
        row["semantic"]["action"] == "PROVIDE-DL-MODE-615A-INFORMATION-UPLOAD-AND-FIND" for row in crs["requirements"]
    )
    assert any(
        row["semantic"]["action"] == "ENTER-DL-FROM-OPS-ONLY-WHEN-GROUND-UPLOAD-INIT-AND-HEADER-ACCEPTED"
        for row in crs["requirements"]
    )
    assert any(
        row["semantic"]["action"] == "REQUIRE-DEFAULT-RECEPTION-VL-FIELDS-IN-NONVOLATILE-MEMORY"
        for row in crs["requirements"]
    )
    assert any(
        row["semantic"]["action"] == "CHECK-TWELVE-PROGRAM-PINS-WITH-PARITY-BIT" for row in crs["requirements"]
    )
    assert any(
        row["semantic"]["action"] == "MAKE-SWITCH-CONFIGURATION-ACCESSIBLE-VIA-615A-INFORMATION"
        for row in crs["requirements"]
    )
    assert any(
        row["semantic"]["action"] == "PROCESS-AT-LEAST-4096-VLS-IN-FILTER-POLICE-FORWARD"
        for row in crs["requirements"]
    )
    intro = next(row for row in crs["requirements"] if row["id"] == "CRS-M1-00778")
    closing = next(row for row in crs["requirements"] if row["id"] == "CRS-M1-00779")
    membership = intro["listMembership"]
    assert membership["listId"] == "P7-4.7.3.2-FILTER-POLICE-FORWARD-PARAMETERS"
    assert membership["role"] == "INTRODUCER"
    assert intro["id"] not in membership["memberRequirementIds"]
    assert closing["id"] not in membership["memberRequirementIds"]
    assert closing["listMembership"]["memberRequirementIds"] == membership["memberRequirementIds"]
    assert "listed per-VL" not in intro["generatedSemanticProjectionEn"]
    members = [row for row in crs["requirements"] if row["id"] in membership["memberRequirementIds"]]
    assert len(members) == 14
    assert {row["source"]["fragmentKind"] for row in members} == {"LIST-ITEM"}
    assert {row["listMembership"]["scope"] for row in members} == {"PER-VL", "PER-PORT"}
    assert {row["listMembership"]["priorityClass"] for row in members if row["listMembership"]["priorityClass"] in {"HIGH", "LOW"}} == {"HIGH", "LOW"}
    assert any(row["semantic"]["action"] == "INCLUDE-FILTER-TABLE-PER-VL-INPUT-PHYSICAL-PORT" for row in members)
    assert any(row["semantic"]["action"] == "INCLUDE-FILTER-TABLE-PER-PORT-HIGH-PRIORITY-BUFFER" for row in members)
    rx = next(row for row in crs["requirements"] if row["id"] == "CRS-M1-00769")
    pin = next(row for row in crs["requirements"] if row["id"] == "CRS-M1-00771")
    assert "named open" not in rx["generatedSemanticProjectionEn"]
    assert "named open" not in pin["generatedSemanticProjectionEn"]
    assert "具名未决" not in rx["generatedSemanticProjectionZh"]
    assert "具名未决" not in pin["generatedSemanticProjectionZh"]
    philosophy = next(row for row in crs["requirements"] if row["id"] == "CRS-M1-00732")
    contents = next(row for row in crs["requirements"] if row["id"] == "CRS-M1-00733")
    precedence = next(row for row in crs["requirements"] if row["id"] == "CRS-M1-00604")
    assert philosophy["conformanceEffect"] == "INFORMATIVE"
    assert contents["conformanceEffect"] == "INFORMATIVE"
    assert philosophy["semantic"]["actor"] == "ARINC-664P3-DOCUMENT-CONTROL"
    assert "user/regulatory" in philosophy["generatedSemanticProjectionEn"]
    assert precedence["conformanceEffect"] == "CONDITIONAL-REQUIRED"
    assert precedence["semantic"]["action"] == "GIVE-664P3-PRECEDENCE-OVER-CONFLICTING-RFC-OPTIONS"


TRUNCATED_LEAD_IN = "The TFTP Read Request or Write Request packet is modified to include"
BLKSIZE_RANGE = 'Valid values range between "8" and "65464" octets, inclusive.'
TIMEOUT_RANGE = 'Valid values range between "1" and "255" seconds, inclusive.'
TSIZE_RRQ = (
    'In Read Request packets, a size of "0" is specified in the request '
    "and the size of the file, in octets, is returned in the OACK."
)
CHECKSUM_CROSS_PAGE = (
    "Checksum is the 16-bit one's complement of the one's complement sum of a "
    "pseudo header of information from the IP header, the UDP header, and the "
    "data, padded with zero octets at the end (if necessary) to make a multiple "
    "of two octets."
)


def test_rfc_option_leaves_bind_complete_distinct_sentences() -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "check_repo_baseline", ROOT / "scripts/check_repo_baseline.py"
    )
    assert spec and spec.loader
    baseline = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(baseline)
    crs = json.loads((ROOT / "configs/requirements/arinc_615a3_m1_crs.json").read_text(encoding="utf-8"))
    by_id = {row["id"]: row for row in crs["requirements"]}
    truncated = baseline.leaf_unit_hash(TRUNCATED_LEAD_IN)
    assert not baseline.is_complete_prose_sentence(TRUNCATED_LEAD_IN)
    assert baseline.is_complete_prose_sentence(BLKSIZE_RANGE)
    assert baseline.is_complete_prose_sentence(CHECKSUM_CROSS_PAGE)
    blksize = by_id["CRS-M1-00625"]
    timeout = by_id["CRS-M1-00626"]
    tsize = by_id["CRS-M1-00627"]
    assert blksize["sourceTextHash"] == baseline.leaf_unit_hash(BLKSIZE_RANGE)
    assert timeout["sourceTextHash"] == baseline.leaf_unit_hash(TIMEOUT_RANGE)
    assert tsize["sourceTextHash"] == baseline.leaf_unit_hash(TSIZE_RRQ)
    assert len({blksize["sourceTextHash"], timeout["sourceTextHash"], tsize["sourceTextHash"]}) == 3
    assert truncated not in {blksize["sourceTextHash"], timeout["sourceTextHash"], tsize["sourceTextHash"]}
    assert "UNESTABLISHED" not in by_id["CRS-M1-00614"]["semantic"]["action"]
    assert "UNESTABLISHED" not in by_id["CRS-M1-00615"]["semantic"]["action"]
    assert by_id["CRS-M1-00614"]["sourceModality"] == "MUST"
    assert by_id["CRS-M1-00625"]["sourceModality"] == "FACT"
    abort = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "MAY-ABORT-RRQ-WITH-ERROR-CODE-3"
    )
    assert abort["sourceModality"] == "MAY"
    assert abort["conformanceEffect"] == "OPTIONAL"
    assert any(row["semantic"]["action"] == "ENCODE-RRQ-WRQ-AS-OPCODE-FILENAME-AND-MODE" for row in crs["requirements"])
    assert any(row["semantic"]["action"] == "ECHO-CLIENT-TIMEOUT-VALUE-IN-OACK" for row in crs["requirements"])
    assert any(row["semantic"]["action"] == "SPECIFY-TSIZE-ON-WRQ-AND-ECHO-IN-OACK" for row in crs["requirements"])
    checksum = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "COMPUTE-UDP-CHECKSUM-OVER-PSEUDO-HEADER-HEADER-AND-DATA"
    )
    assert checksum["sourceTextHash"] == baseline.leaf_unit_hash(CHECKSUM_CROSS_PAGE)
    sas = next(row for row in crs["requirements"] if row["semantic"]["action"] == "NEVER-RESEND-CURRENT-DATA-ON-DUPLICATE-ACK")
    assert sas["source"]["sourceId"] == "RFC-1123"
    assert sas["sourceModality"] == "MUST"
    mail = next(row for row in crs["requirements"] if row["semantic"]["action"] == "DO-NOT-SUPPORT-TFTP-MAIL-TRANSFER-MODE")
    assert mail["conformanceEffect"] == "PROHIBITED"
    assert mail["semantic"]["polarity"] == "NEGATIVE"
    version_width = next(row for row in crs["requirements"] if row["semantic"]["action"] == "ENCODE-VERSION-AS-4-BITS")
    assert version_width["sourceTextHash"] == baseline.leaf_unit_hash("Version: 4 bits")
    bag = next(row for row in crs["requirements"] if row["semantic"]["action"] == "RESTRICT-BAG-TO-POWERS-OF-TWO-MILLISECONDS")
    assert bag["source"]["sourceId"] == "ARINC-664-7"
    port59 = next(
        row for row in crs["requirements"] if row["semantic"]["action"] == "RESERVE-UDP-TCP-PORT-59-FOR-615A-DATA-LOADER-TFTP"
    )
    assert port59["source"]["sourceId"] == "ARINC-664-4"
    assert port59["source"]["clause"] == "ATT-1"
    assert "remaining" not in by_id["CRS-M1-00612"]["generatedSemanticProjectionEn"].lower()
    jitter_cap = next(
        row for row in crs["requirements"] if row["semantic"]["action"] == "KEEP-VL-JITTER-AT-OR-BELOW-500-MICROSECONDS"
    )
    assert "500" in jitter_cap["generatedSemanticProjectionEn"]
    assert "hashed-equation gap" not in jitter_cap["generatedSemanticProjectionEn"]
    eq1 = next(
        row for row in crs["requirements"] if row["semantic"]["action"] == "BOUND-MAX-JITTER-BY-40US-PLUS-VL-LOAD-TERM"
    )
    eq2 = next(
        row for row in crs["requirements"] if row["semantic"]["action"] == "BOUND-MAX-JITTER-BY-500-MICROSECONDS-EQUATION"
    )
    assert eq1["source"]["fragmentKind"] == "EQUATION"
    assert eq2["source"]["fragmentKind"] == "EQUATION"
    assert eq1["ambiguityStatus"] == "SOURCE-EQUATION-OPERATORS-RECOVERED-FROM-PDF-LAYOUT"
    mac = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "ENCODE-MAC-SOURCE-AS-INDIVIDUAL-AND-LOCALLY-ADMINISTERED"
    )
    assert mac["source"]["clause"] == "3.2.5.2"


def test_tftp_end_condition_combines_default_and_negotiated_blksize() -> None:
    crs = json.loads((ROOT / "configs/requirements/arinc_615a3_m1_crs.json").read_text(encoding="utf-8"))
    by_id = {row["id"]: row for row in crs["requirements"]}
    default_end = by_id["CRS-M1-00620"]
    default_width = by_id["CRS-M1-00635"]
    assert "BLKSIZE-WAS-NOT-SUCCESSFULLY-NEGOTIATED" in default_end["semantic"]["condition"]
    assert "BLKSIZE-WAS-NOT-SUCCESSFULLY-NEGOTIATED" in default_width["semantic"]["condition"]
    negotiated = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "TERMINATE-ON-DATA-SHORTER-THAN-NEGOTIATED-BLKSIZE"
    )
    zero = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "SEND-ZERO-LENGTH-FINAL-DATA-WHEN-FILE-IS-INTEGRAL-MULTIPLE-OF-BLKSIZE"
    )
    fallback = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "IGNORE-UNACKNOWLEDGED-OPTION-AND-KEEP-DEFAULT-PARAMETERS"
    )
    assert negotiated["source"]["sourceId"] == "RFC-2348"
    assert zero["source"]["sourceId"] == "RFC-2348"
    assert fallback["source"]["sourceId"] == "RFC-2347"
    assert any(
        rel["requirementId"] == "CRS-M1-00620" and rel["relation"] == "REFINES-WHEN-OPTION-NEGOTIATED"
        for rel in negotiated["supportingRequirementRelations"]
    )
    assert any(
        rel["relation"] == "FALLBACK-WHEN-OPTION-NOT-ACCEPTED"
        for rel in fallback["supportingRequirementRelations"]
    )

    def effective_blksize(requested: int | None, accepted: int | None) -> int:
        if accepted is None:
            return 512
        return accepted

    def is_final_data(length: int, blksize: int) -> bool:
        return length < blksize

    assert is_final_data(700, effective_blksize(1024, 1024)) is True
    assert is_final_data(256, effective_blksize(256, 256)) is False
    assert is_final_data(511, effective_blksize(None, None)) is True
    assert is_final_data(512, effective_blksize(None, None)) is False
    assert is_final_data(0, effective_blksize(1024, 1024)) is True
    assert "1024" in negotiated["generatedSemanticProjectionEn"]
    assert "700" in negotiated["generatedSemanticProjectionEn"]
    assert "256" in negotiated["generatedSemanticProjectionEn"]
    assert "integral multiple" in zero["generatedSemanticProjectionEn"]
    assert "never requested" in fallback["generatedSemanticProjectionEn"]


P7_PRINT_PAGES = {18: 10, 19: 11, 21: 13, 22: 14, 23: 15, 24: 16, 25: 17, 26: 18, 27: 19}
MAC_FIELDS = (("CONSTANT", 24), ("USER-DEFINED-ID", 16), ("INTERFACE-ID", 3), ("CONSTANT-TAIL", 5))


def _crs() -> dict:
    return json.loads((ROOT / "configs/requirements/arinc_615a3_m1_crs.json").read_text(encoding="utf-8"))


def test_p7_print_pages_are_not_pdf_indexes() -> None:
    crs = _crs()
    this_round = [
        row
        for row in crs["requirements"]
        if row["source"]["sourceId"] == "ARINC-664-7" and 666 <= int(row["id"].rsplit("-", 1)[1]) <= 694
    ]
    assert this_round
    for row in this_round:
        pdf_page = row["source"]["pdfPage"]
        document_page = row["source"]["documentPage"]
        assert pdf_page in P7_PRINT_PAGES
        assert document_page == P7_PRINT_PAGES[pdf_page]
        assert document_page != pdf_page
    coverage = [
        row
        for row in crs["coverageLedger"]
        if row["source"]["sourceId"] == "ARINC-664-7"
        and row["source"]["pdfPage"] in P7_PRINT_PAGES
        and any(666 <= int(req_id.rsplit("-", 1)[1]) for req_id in row.get("requirementIds") or [])
    ]
    assert coverage
    for row in coverage:
        assert row["source"]["documentPage"] == P7_PRINT_PAGES[row["source"]["pdfPage"]]
    p4 = next(row for row in crs["requirements"] if row["id"] == "CRS-M1-00710")
    assert p4["source"]["documentPage"] == 19
    assert p4["source"]["pdfPage"] == 25


def _ideal_value_latency_verdict(value: float, bound: float, premises_met: bool, *, strict: bool) -> str:
    """Exact-value source-algebra check. Not a deployed measurement PASS."""
    if not premises_met:
        return "INCONCLUSIVE"
    if strict:
        return "PASS" if value < bound else "FAIL"
    return "PASS" if value <= bound else "FAIL"


def _t5_interval_verdict(obs_lo: float, obs_hi: float, req_lo: float, req_hi: float, *, req_upper_open: bool) -> str:
    """T5 interval treatment for deployed measurements with a Configuration error budget."""
    req_contains = (
        lambda x: req_lo <= x < req_hi if req_upper_open else req_lo <= x <= req_hi
    )
    if obs_lo > obs_hi:
        raise ValueError("observation interval is reversed")
    if req_contains(obs_lo) and req_contains(obs_hi):
        return "PASS"
    disjoint = obs_hi < req_lo or (obs_lo >= req_hi if req_upper_open else obs_lo > req_hi)
    if disjoint:
        return "FAIL"
    return "INCONCLUSIVE"


def _jitter_env(max_jitter: float, lmax_values: list[float], nbw: float) -> dict:
    return {
        "vars": {},
        "clocks": {},
        "params": {"MAX_JITTER": max_jitter, "NBW": nbw, "LMAX_I": None},
        "payload": {},
        "sum_domains": {"CONFIGURED-VL-SET": list(lmax_values)},
    }


def _eval_both_jitter(m2sync, load_expr, cap_expr, max_jitter: float, lmax_values: list[float], nbw: float) -> bool:
    env = _jitter_env(max_jitter, lmax_values, nbw)
    return m2sync.eval_ast(load_expr, env) is True and m2sync.eval_ast(cap_expr, env) is True


def _scalar_lmax_expr() -> dict:
    return {
        "kind": "COMPARE",
        "op": "LE",
        "left": {"kind": "SYMBOL", "name": "MAX_JITTER"},
        "right": {
            "kind": "BINARY",
            "op": "ADD",
            "left": {"kind": "LITERAL", "value": 40},
            "right": {
                "kind": "BINARY",
                "op": "MUL",
                "left": {
                    "kind": "BINARY",
                    "op": "DIV",
                    "left": {
                        "kind": "BINARY",
                        "op": "MUL",
                        "left": {
                            "kind": "BINARY",
                            "op": "ADD",
                            "left": {"kind": "LITERAL", "value": 20},
                            "right": {"kind": "SYMBOL", "name": "LMAX_I"},
                        },
                        "right": {"kind": "LITERAL", "value": 8},
                    },
                    "right": {"kind": "SYMBOL", "name": "NBW"},
                },
                "right": {"kind": "LITERAL", "value": 1000000},
            },
        },
    }


def _overhead_once_expr() -> dict:
    return {
        "kind": "COMPARE",
        "op": "LE",
        "left": {"kind": "SYMBOL", "name": "MAX_JITTER"},
        "right": {
            "kind": "BINARY",
            "op": "ADD",
            "left": {"kind": "LITERAL", "value": 40},
            "right": {
                "kind": "BINARY",
                "op": "MUL",
                "left": {
                    "kind": "BINARY",
                    "op": "DIV",
                    "left": {
                        "kind": "BINARY",
                        "op": "MUL",
                        "left": {"kind": "LITERAL", "value": 8},
                        "right": {
                            "kind": "BINARY",
                            "op": "ADD",
                            "left": {"kind": "LITERAL", "value": 20},
                            "right": {
                                "kind": "SUM",
                                "index": "I",
                                "domain": "CONFIGURED-VL-SET",
                                "body": {"kind": "SYMBOL", "name": "LMAX_I"},
                            },
                        },
                    },
                    "right": {"kind": "SYMBOL", "name": "NBW"},
                },
                "right": {"kind": "LITERAL", "value": 1000000},
            },
        },
    }


def test_p7_technological_latency_and_jitter_contracts() -> None:
    import copy
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    import sync_m2_model as m2sync

    crs = _crs()
    by_id = {row["id"]: row for row in crs["requirements"]}
    tx = by_id["CRS-M1-00682"]
    rx = by_id["CRS-M1-00683"]
    eq1 = by_id["CRS-M1-00684"]
    eq2 = by_id["CRS-M1-00685"]
    both = next(
        row for row in crs["requirements"] if row["semantic"]["action"] == "SATISFY-BOTH-MAX-JITTER-EQUATIONS-SIMULTANEOUSLY"
    )
    units = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "TREAT-MAX-JITTER-AS-MICROSECONDS-NBW-AS-BITS-PER-SECOND-AND-LMAX-AS-OCTETS"
    )
    assert tx["source"]["documentPage"] == 15 and tx["source"]["pdfPage"] == 23
    assert rx["source"]["documentPage"] == 16 and rx["source"]["pdfPage"] == 24
    assert eq1["source"]["documentPage"] == 17 and eq1["source"]["pdfPage"] == 25
    assert "EMPTY-BUFFERS" in tx["semantic"]["objects"]
    assert tx["timing"]["upperBoundary"] == "OPEN"
    assert rx["timing"]["upperBoundary"] == "OPEN"
    assert tx["timing"]["observationState"] == "CONFIGURATION-DEPENDENT"
    assert rx["timing"]["cancellation"] == "MEASUREMENT-PREMISES-NOT-MET"
    assert tx["timing"]["errorBudgetState"] == "FUTURE-CONFIGURATION-DEPENDENT"
    assert rx["timing"]["errorBudgetState"] == "FUTURE-CONFIGURATION-DEPENDENT"
    assert tx["timing"]["sourceRelation"] == "TECH-LAT-TX < 150 + FRAME-DELAY"
    assert rx["timing"]["sourceRelation"] == "TECH-LAT-RX < 150"
    assert _ideal_value_latency_verdict(150, 150, True, strict=True) == "FAIL"
    assert _ideal_value_latency_verdict(149.9, 150, True, strict=True) == "PASS"
    assert _ideal_value_latency_verdict(200, 150, False, strict=True) == "INCONCLUSIVE"
    assert _ideal_value_latency_verdict(150, 150, True, strict=False) == "PASS"
    assert _t5_interval_verdict(149, 151, 0, 150, req_upper_open=True) == "INCONCLUSIVE"
    assert _t5_interval_verdict(148, 149, 0, 150, req_upper_open=True) == "PASS"
    assert _t5_interval_verdict(150, 151, 0, 150, req_upper_open=True) == "FAIL"
    assert eq1["timing"]["sourceRelation"] == (
        "MAX-JITTER <= 40 + (8 * SUM{I-IN-CONFIGURED-VL-SET}(20 + LMAX-I) / NBW) * 1000000"
    )
    assert eq2["timing"]["sourceRelation"] == "MAX-JITTER <= 500"
    assert eq1["timing"]["silenceSemantics"] == "BOTH-MAX-JITTER-EQUATIONS-MUST-HOLD"
    assert eq1["timing"]["errorBudgetState"] == "NOT-REQUIRED"
    assert "SUM" in units["generatedSemanticProjectionEn"]
    assert "bits/s" in units["generatedSemanticProjectionEn"]
    assert "octets" in units["generatedSemanticProjectionEn"]
    assert "positive" in units["generatedSemanticProjectionEn"]
    assert both["semantic"]["action"] == "SATISFY-BOTH-MAX-JITTER-EQUATIONS-SIMULTANEOUSLY"
    m2 = json.loads((ROOT / "configs/models/arinc_615a3_m2_model.json").read_text(encoding="utf-8"))
    load_row = next(row for row in m2["timingCatalog"] if row["requirementId"] == "CRS-M1-00684")
    cap_row = next(row for row in m2["timingCatalog"] if row["requirementId"] == "CRS-M1-00685")
    assert load_row["expression"]["op"] == "LE"
    assert any(node.get("kind") == "SUM" for node in m2sync.walk_nodes(load_row["expression"]))
    assert m2sync.source_equation_structure_errors(load_row, eq1["timing"]["sourceRelation"], load_row["expression"]) == []
    assert m2sync.parse_source_equation(eq1["timing"]["sourceRelation"]) is not None
    nbw = 100_000_000
    assert _eval_both_jitter(m2sync, load_row["expression"], cap_row["expression"], 45, [64], nbw) is True
    assert _eval_both_jitter(m2sync, load_row["expression"], cap_row["expression"], 160, [1000, 1000], nbw) is True
    assert _eval_both_jitter(m2sync, load_row["expression"], cap_row["expression"], 160, [1000], nbw) is False
    assert _eval_both_jitter(m2sync, load_row["expression"], cap_row["expression"], 202, [1000, 1000], nbw) is True
    two_unequal = _eval_both_jitter(m2sync, load_row["expression"], cap_row["expression"], 160, [64, 1518], nbw)
    assert two_unequal is True
    assert _eval_both_jitter(m2sync, load_row["expression"], cap_row["expression"], 510, [1518, 1518, 1518, 1518], nbw) is False
    assert _eval_both_jitter(m2sync, load_row["expression"], cap_row["expression"], 490, [1518, 1518, 1518, 1518], nbw) is True
    zero_bw = _jitter_env(40, [64], 0)
    assert m2sync.eval_ast(load_row["expression"], zero_bw) is not True
    broken = copy.deepcopy(load_row)
    broken["expression"]["op"] = "GE"
    assert m2sync.source_equation_structure_errors(broken, eq1["timing"]["sourceRelation"], broken["expression"])
    no_sum = copy.deepcopy(load_row)
    no_sum["expression"] = _scalar_lmax_expr()
    assert m2sync.source_equation_structure_errors(no_sum, eq1["timing"]["sourceRelation"], no_sum["expression"])
    overhead_once = copy.deepcopy(load_row)
    overhead_once["expression"] = _overhead_once_expr()
    assert m2sync.source_equation_structure_errors(
        overhead_once, eq1["timing"]["sourceRelation"], overhead_once["expression"]
    )
    dropped_vl_body = copy.deepcopy(load_row)
    dropped_vl_body["expression"] = {
        "kind": "COMPARE",
        "op": "LE",
        "left": {"kind": "SYMBOL", "name": "MAX_JITTER"},
        "right": {
            "kind": "BINARY",
            "op": "ADD",
            "left": {"kind": "LITERAL", "value": 40},
            "right": {
                "kind": "BINARY",
                "op": "MUL",
                "left": {
                    "kind": "BINARY",
                    "op": "DIV",
                    "left": {
                        "kind": "BINARY",
                        "op": "MUL",
                        "left": {"kind": "LITERAL", "value": 8},
                        "right": {
                            "kind": "SUM",
                            "index": "I",
                            "domain": "CONFIGURED-VL-SET",
                            "body": {"kind": "LITERAL", "value": 20},
                        },
                    },
                    "right": {"kind": "SYMBOL", "name": "NBW"},
                },
                "right": {"kind": "LITERAL", "value": 1000000},
            },
        },
    }
    assert m2sync.source_equation_structure_errors(
        dropped_vl_body, eq1["timing"]["sourceRelation"], dropped_vl_body["expression"]
    )
    one_only = copy.deepcopy(load_row)
    one_only["expression"] = {
        "kind": "COMPARE",
        "op": "LE",
        "left": {"kind": "SYMBOL", "name": "MAX_JITTER"},
        "right": {"kind": "LITERAL", "value": 500},
    }
    assert m2sync.source_equation_structure_errors(one_only, eq1["timing"]["sourceRelation"], one_only["expression"])
    no_units = copy.deepcopy(load_row)
    no_units["expression"]["right"]["right"] = {
        "kind": "BINARY",
        "op": "DIV",
        "left": {
            "kind": "BINARY",
            "op": "MUL",
            "left": {"kind": "LITERAL", "value": 8},
            "right": {
                "kind": "SUM",
                "index": "I",
                "domain": "CONFIGURED-VL-SET",
                "body": {
                    "kind": "BINARY",
                    "op": "ADD",
                    "left": {"kind": "LITERAL", "value": 20},
                    "right": {"kind": "SYMBOL", "name": "LMAX_I"},
                },
            },
        },
        "right": {"kind": "SYMBOL", "name": "NBW"},
    }
    assert m2sync.source_equation_structure_errors(no_units, eq1["timing"]["sourceRelation"], no_units["expression"])
    cap_broken = copy.deepcopy(cap_row)
    cap_broken["expression"]["op"] = "LT"
    assert m2sync.source_equation_structure_errors(cap_broken, eq2["timing"]["sourceRelation"], cap_broken["expression"])
    data = copy.deepcopy(m2)
    dest = next(row for row in data["timingCatalog"] if row["requirementId"] == "CRS-M1-00684")
    dest["expression"] = _scalar_lmax_expr()
    data["inventorySummary"]["timingFingerprint"] = m2sync.fingerprint(data["timingCatalog"])
    assert any("equation structure" in item or "indexed SUM" in item for item in m2sync.package_errors(data))
    assert m2["scope"]["afdxSelected"] is False
    assert list(m2["scope"]["services"]) == ["UPLOAD", "INFORMATION"]
    assert any(row["id"] == "CLK_AFDX_ES" for row in m2["model"]["clocks"])
    assert not any("CLK_AFDX_ES" in (row.get("resets") or []) for row in m2["model"]["transitions"])
    assert len(m2["model"]["transitions"]) == 65


def test_p7_mac_source_is_complete_48_bit_binding() -> None:
    crs = _crs()
    composition = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "COMPOSE-MAC-SOURCE-AS-24-PLUS-16-PLUS-3-PLUS-5-BIT-FIELDS"
    )
    tail = next(row for row in crs["requirements"] if row["semantic"]["action"] == "SET-MAC-SOURCE-CONSTANT-TAIL-TO-00000")
    commentary = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "TREAT-MAC-SOURCE-CONSTRUCTION-ALGORITHM-AS-NOT-UNIQUELY-RECOMMENDED"
    )
    ieee = next(
        row
        for row in crs["requirements"]
        if row["semantic"]["action"] == "ENCODE-MAC-SOURCE-AS-INDIVIDUAL-AND-LOCALLY-ADMINISTERED"
    )
    assert composition["source"]["documentPage"] == 19
    assert composition["source"]["pdfPage"] == 27
    assert tail["source"]["tableOrFigure"] == "Figure 3-11"
    widths = [width for _name, width in MAC_FIELDS]
    assert sum(widths) == 48
    starts = []
    cursor = 0
    for width in widths:
        starts.append(cursor)
        cursor += width
    assert cursor == 48
    assert starts == [0, 24, 40, 43]
    overlapping = any(
        start < other_start + other_width and other_start < start + width
        for (start, width) in zip(starts, widths)
        for (other_start, other_width) in zip(starts, widths)
        if (start, width) != (other_start, other_width)
    )
    assert overlapping is False
    assert 24 + 16 + 3 != 48
    assert "00000" in tail["generatedSemanticProjectionEn"] or "0 0000" in tail["generatedSemanticProjectionEn"]
    assert commentary["sourceModality"] == "COMMENTARY"
    assert commentary["conformanceEffect"] == "INFORMATIVE"
    assert "No unique" not in ieee["generatedSemanticProjectionEn"]
    encodings = {}
    for row in crs["requirements"]:
        action = row["semantic"]["action"]
        if action == "ENCODE-INTERFACE-ID-001-AS-NETWORK-A":
            encodings["001"] = row
        elif action == "ENCODE-INTERFACE-ID-010-AS-NETWORK-B":
            encodings["010"] = row
        elif action.startswith("RECORD-INTERFACE-ID-") and action.endswith("-AS-NOT-USED"):
            encodings[action.split("-")[3]] = row
        elif action == "RECORD-INTERFACE-ID-110-AS-SOURCE-NOR-USED":
            encodings["110"] = row
    assert set(encodings) == {"000", "001", "010", "011", "100", "101", "110", "111"}
    assert encodings["001"]["conformanceEffect"] == "CONDITIONAL-REQUIRED"
    assert encodings["010"]["conformanceEffect"] == "CONDITIONAL-REQUIRED"
    for code in ("000", "011", "100", "101", "110", "111"):
        assert encodings[code]["conformanceEffect"] == "INFORMATIVE"
        assert encodings[code]["conformanceEffect"] != "PROHIBITED"
    assert encodings["001"]["semantic"]["action"] != encodings["010"]["semantic"]["action"]
    wrong_tail = "11111"
    assert wrong_tail not in tail["generatedSemanticProjectionEn"]


def test_udp_checksum_afdx_must_fabrication_fails_after_fingerprint_refresh() -> None:
    import copy
    import importlib.util

    spec = importlib.util.spec_from_file_location("sync_m1_crs", ROOT / "scripts/sync_m1_crs.py")
    assert spec and spec.loader
    m1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m1)
    data = json.loads((ROOT / "configs/requirements/arinc_615a3_m1_crs.json").read_text(encoding="utf-8"))
    row = next(
        item
        for item in data["requirements"]
        if item["semantic"]["action"] == "TREAT-UDP-CHECKSUM-GENERATE-AND-CHECK-AS-NOT-APPLICABLE-ON-AFDX"
    )
    assert "NOT APPLICABLE" in row["generatedSemanticProjectionEn"]
    mutated = copy.deepcopy(data)
    target = next(item for item in mutated["requirements"] if item["id"] == row["id"])
    target["semantic"]["action"] = "IMPLEMENT-UDP-CHECKSUM-GENERATE-AND-CHECK-FACILITY"
    target["generatedSemanticProjectionEn"] = (
        "If AFDX is chosen, Table 2-2 marks UDP checksum generation/checking AFDX MUST. "
        "That generate/check capability is retained and CRS-M1-00609 is not applied."
    )
    target["ambiguityStatus"] = "SOURCE-AFDX-TABLE-MARK-AND-UNUSED-COMMENT-UNRESOLVED"
    target["gapIds"] = ["GAP-UDP-CHECKSUM-USE-POLICY"]
    summary = mutated["inventorySummary"]
    summary["coverageFingerprint"] = m1.fingerprint(mutated["coverageLedger"])
    summary["requirementsFingerprint"] = m1.fingerprint(mutated["requirements"])
    mutated["reviewControl"]["sourceInventoryFingerprint"] = m1.fingerprint(m1.source_inventory_projection(mutated))
    found = m1.package_errors(mutated)
    assert any("semantic assertion" in item or "CRS-M1-00742" in item for item in found)


def test_informative_laundering_of_named_remainders_fails() -> None:
    data = audit()
    remaining = {}
    for source in data["supportingSourceApplicabilityAudit"]["sources"]:
        for unit in source["units"]:
            for item in unit.get("remainingSubunits") or []:
                remaining[item["id"]] = item
    mib = remaining["SAU-P7-4-REMAINING-MIB-SNMP-AND-PERIODIC-STATUS"]
    shop = remaining["SAU-P7-4-REMAINING-SHOP-OPTIONAL"]
    integrator = remaining["SAU-P7-4-REMAINING-INTEGRATOR-DEFINED-INIT-AND-PORT-COUNTS"]
    assert "SAU-P7-4-REMAINING-CONFIG-AND-PIN-TABLE-FIELDS" not in remaining
    assert mib["disposition"] != "INFORMATIVE"
    assert shop["disposition"] != "INFORMATIVE"
    assert mib["disposition"] == "OUT-OF-PROFILE"
    assert shop["disposition"] == "OUT-OF-PROFILE"
    assert integrator["disposition"] == "INFORMATIVE"


def test_filter_table_list_membership_mutations_fail_after_fingerprint_refresh() -> None:
    import copy
    import importlib.util

    spec = importlib.util.spec_from_file_location("sync_m1_crs", ROOT / "scripts/sync_m1_crs.py")
    assert spec and spec.loader
    m1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m1)
    data = json.loads((ROOT / "configs/requirements/arinc_615a3_m1_crs.json").read_text(encoding="utf-8"))

    def refresh(package: dict) -> None:
        package["inventorySummary"]["coverageFingerprint"] = m1.fingerprint(package["coverageLedger"])
        package["inventorySummary"]["requirementsFingerprint"] = m1.fingerprint(package["requirements"])
        package["reviewControl"]["sourceInventoryFingerprint"] = m1.fingerprint(m1.source_inventory_projection(package))

    legal = copy.deepcopy(data)
    refresh(legal)
    assert not any("list " in item and "P7-4.7.3.2" in item for item in m1.package_errors(legal))

    dropped = copy.deepcopy(data)
    intro = next(row for row in dropped["requirements"] if row["id"] == "CRS-M1-00778")
    intro["listMembership"]["memberRequirementIds"] = intro["listMembership"]["memberRequirementIds"][1:]
    refresh(dropped)
    found = m1.package_errors(dropped)
    assert any("introducer members do not match MEMBER rows" in item or "must own the 14" in item for item in found)

    swapped = copy.deepcopy(data)
    member = next(
        row
        for row in swapped["requirements"]
        if row.get("listMembership", {}).get("listId") == "P7-4.7.3.2-FILTER-POLICE-FORWARD-PARAMETERS"
        and row.get("listMembership", {}).get("scope") == "PER-VL"
    )
    member["listMembership"]["scope"] = "PER-PORT"
    refresh(swapped)
    found = m1.package_errors(swapped)
    assert any("nine per-VL and five per-port members" in item for item in found)


def test_lub_spare_is_not_zero_fill_and_keeps_width_alignment() -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("sync_m1_crs", ROOT / "scripts/sync_m1_crs.py")
    assert spec and spec.loader
    m1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m1)
    crs = json.loads((ROOT / "configs/requirements/arinc_615a3_m1_crs.json").read_text(encoding="utf-8"))
    spare = next(row for row in crs["requirements"] if row["id"] == "CRS-M1-00548")
    constraint = spare["fieldConstraint"]
    assert constraint["widthBitsExpression"] == "16"
    assert constraint["encodingRule"] == "ALIGNMENT-FIELD-VALUE-NOT-CONSTRAINED"
    assert constraint["encodingRule"] != "RESERVED-ZERO-FILL"
    assert "align" in spare["generatedSemanticProjectionEn"].lower()
    assert "对齐" in spare["generatedSemanticProjectionZh"]
    assert "reserved zero" not in spare["generatedSemanticProjectionEn"].lower()
    assert "填零" not in spare["generatedSemanticProjectionZh"]
    assert not m1.encoding_rejects_integer_value(constraint["encodingRule"], 0xABCD)
    alignment = next(row for row in crs["requirements"] if row["id"] == "CRS-M1-00570")
    assert alignment["semantic"]["action"] == "USE-SPARE-TO-ALIGN-FOLLOWING-POINTERS-ON-4-BYTE-BOUNDARIES"
    last_ptr = next(row for row in crs["requirements"] if row["id"] == "CRS-M1-00540")
    comment = next(row for row in crs["requirements"] if row["id"] == "CRS-M1-00579")
    assert last_ptr["semantic"]["action"] == "SET-LAST-LOAD-LIST-BLOCK-POINTER-TO-ZERO"
    assert comment["semantic"]["action"] == "SET-COMMENT-LENGTH-ZERO-WHEN-NO-COMMENT"
    for req_id in ("CRS-M1-00551", "CRS-M1-00556", "CRS-M1-00566"):
        expansion = next(row for row in crs["requirements"] if row["id"] == req_id)
        assert expansion["fieldConstraint"]["widthBitsExpression"] == "0"
        assert expansion["fieldConstraint"]["encodingRule"] == "ZERO-WIDTH-NO-EMITTED-BYTES"


def test_lub_spare_zero_fill_reintroduction_fails_after_fingerprint_refresh() -> None:
    import copy
    import importlib.util

    spec = importlib.util.spec_from_file_location("sync_m1_crs", ROOT / "scripts/sync_m1_crs.py")
    assert spec and spec.loader
    m1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m1)
    data = json.loads((ROOT / "configs/requirements/arinc_615a3_m1_crs.json").read_text(encoding="utf-8"))

    def refresh(package: dict) -> None:
        package["inventorySummary"]["coverageFingerprint"] = m1.fingerprint(package["coverageLedger"])
        package["inventorySummary"]["requirementsFingerprint"] = m1.fingerprint(package["requirements"])
        package["reviewControl"]["sourceInventoryFingerprint"] = m1.fingerprint(m1.source_inventory_projection(package))

    legal = copy.deepcopy(data)
    refresh(legal)
    assert not any("CRS-M1-00548" in item and "zero" in item for item in m1.package_errors(legal))

    restored = copy.deepcopy(data)
    spare = next(row for row in restored["requirements"] if row["id"] == "CRS-M1-00548")
    spare["fieldConstraint"]["encodingRule"] = "RESERVED-ZERO-FILL"
    spare["generatedSemanticProjectionEn"] = (
        "Encode the Spare field of LUB as 16 reserved zero bits used to align the following pointers."
    )
    refresh(restored)
    found = m1.package_errors(restored)
    assert any("must not treat LUB Spare as reserved-zero-fill" in item for item in found)
    assert m1.encoding_rejects_integer_value("RESERVED-ZERO-FILL", 1)
