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


def test_package_a_does_not_self_approve() -> None:
    data = audit()
    assert data["boundPackage"]["artifactVersion"] == "M1-CANDIDATE-9"
    supporting = data["supportingSourceApplicabilityAudit"]
    assert supporting["notIndependentApproval"] is True
    assert all(row["independentApproval"] is False for row in supporting["sources"])
