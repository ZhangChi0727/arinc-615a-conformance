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
)


def audit() -> dict:
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_package_a_sources_are_first_class_tasks_with_denominators() -> None:
    data = audit()
    assert data["applicabilityAuditPending"] == []
    supporting = data["supportingSourceApplicabilityAudit"]
    assert supporting["notIndependentApproval"] is True
    assert supporting["645BindingThisPr"] is False
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
    assert all(row["refinementDisposition"] in {"PROFILE-SCOPE-ONLY", "DEPENDENCY-BLOCKED"} for row in batch_reqs)
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


def test_rfc_identities_stay_unmerged_and_645_is_acquired_not_bound() -> None:
    data = audit()
    source_ids = [row["sourceId"] for row in data["supportingSourceApplicabilityAudit"]["sources"]]
    assert "RFC-1350-RFC-2347" not in source_ids
    blocked = data["blockedSource"]
    assert blocked["status"] == "BLOCKED-SOURCE-645"
    assert blocked["localFileAcquired"] is True
    assert blocked["boundThisPr"] is False
    abort = data["supportingSourceApplicabilityAudit"]["findAbortAdjudication"]
    assert abort["status"] == "APPLIED-IN-CRS"
    assert abort["code"] == "FIND-ABORT-DOES-NOT-WAIVE-WINDOWS"
    assert abort["crsCancellation"] == "FIND-ABORT-DOES-NOT-WAIVE-WINDOWS"
    part4 = data["supportingSourceApplicabilityAudit"]["arinc664Part4"]
    assert part4["status"] == "NOT-IN-THIS-PR-SOURCE-SET"
    assert part4["affectedRequirementId"] == "CRS-M1-00519"
    assert part4["unboundDispositionId"] == "UD-664-4-NOT-IN-SOURCE-SET"
    dispositions = data["supportingSourceApplicabilityAudit"]["unboundDispositions"]
    assert len(dispositions) == 1
    unbound = dispositions[0]
    assert unbound["id"] == part4["unboundDispositionId"]
    assert unbound["auditUnitId"] == "SAU-P7-P4"
    assert unbound["affectedRequirementId"] == part4["affectedRequirementId"]
    assert unbound["notIndependentApproval"] is True


def test_package_a_does_not_self_approve() -> None:
    data = audit()
    assert data["boundPackage"]["artifactVersion"] == "M1-CANDIDATE-11"
    supporting = data["supportingSourceApplicabilityAudit"]
    assert supporting["notIndependentApproval"] is True
    assert all(row["independentApproval"] is False for row in supporting["sources"])


ALLOWED_LEAF_STATUS = {
    "NOT-REQUIRED",
    "LEAF-CRS-EMITTED",
    "EXISTING-351-TRIGGERED-ROWS",
    "EXISTING-LEAF-VIA-2-1-2",
    "EXISTING-615A-LEAF",
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
    p7_rows = [row for row in crs["requirements"] if row["source"]["sourceId"] == "ARINC-664-7"]
    assert rfc_rows
    assert p3_rows
    assert p7_rows
    assert all(row["reviewStatus"] == "PENDING-EXTERNAL-INDEPENDENT-REVIEW" for row in rfc_rows + p3_rows + p7_rows)
    deps = {row["id"]: row for row in crs["dependencies"]}
    for dep_id in ("DEP-RFC-1350", "DEP-RFC-768", "DEP-ARINC-664-3", "DEP-ARINC-664-7"):
        assert deps[dep_id]["status"] == "OPEN-DEPENDENCY"
    spans = json.loads(SPANS.read_text(encoding="utf-8"))
    by_id = {row["sourceId"]: row for row in spans["sources"]}
    assert by_id["ARINC-664-2"]["spans"][0]["pdfPages"] == [8, 28]
    assert any(row["pdfPages"] == [8, 36] for row in by_id["ARINC-664-3"]["spans"])
    assert "RFC-1350" in by_id
    assert "RFC-768" in by_id
    remaining = {}
    unbound = next(
        row
        for row in data["supportingSourceApplicabilityAudit"]["unboundDispositions"]
        if row["id"] == part4["unboundDispositionId"]
    )
    for source in data["supportingSourceApplicabilityAudit"]["sources"]:
        for unit in source["units"]:
            if unit["leafCrsStatus"] == "LEAF-CRS-EMITTED":
                assert unit["leafCoverageIds"]
                assert "leafRequirementIds" in unit
            if unit["leafCrsStatus"] == "CRS-M1-00519-REMAINS-NOT-YET-BOUND":
                assert unit["unboundDispositionId"]
                assert unit["id"] == unbound["auditUnitId"]
            for item in unit.get("remainingSubunits") or []:
                remaining[item["id"]] = item
    for remaining_id in (
        "SAU-1123-4-2-REMAINING-HOST-NOTE-ATOMS",
        "SAU-P7-3-REMAINING-VL-BAG-JITTER",
        "SAU-791-3-1-REMAINING-FIELD-WIDTHS",
    ):
        assert remaining[remaining_id]["disposition"] == "NOT-YET-BOUND"


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

