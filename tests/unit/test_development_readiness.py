import copy
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("development_readiness", ROOT / "scripts" / "check_development_readiness.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
PACKAGE = json.loads((ROOT / "configs" / "engineering" / "cltav_development_contracts.json").read_text(encoding="utf-8"))


def errors(data):
    return MODULE.package_errors(data)


def test_current_candidate_is_blocked_but_valid():
    assert PACKAGE["reviewBoundary"]["readiness"] == "READINESS-BLOCKED"
    assert errors(copy.deepcopy(PACKAGE)) == []


def test_slice_identity_and_edge_rules():
    duplicate_id = copy.deepcopy(PACKAGE)
    duplicate_id["implementationSlices"].append({"id": duplicate_id["implementationSlices"][0]["id"], "scope": "different", "requirementIds": ["CRS-M1-00420"]})
    assert any("repeats a slice ID" in item for item in errors(duplicate_id))

    duplicate_edge = copy.deepcopy(PACKAGE)
    duplicate_edge["implementationSlices"][0]["requirementIds"].append(duplicate_edge["implementationSlices"][0]["requirementIds"][0])
    assert any("repeats a requirement use" in item for item in errors(duplicate_edge))

    shared = copy.deepcopy(PACKAGE)
    shared["implementationSlices"].append({"id": "SLICE-SHARED", "scope": "legal shared consumer", "requirementIds": [shared["implementationSlices"][0]["requirementIds"][0]]})
    assert errors(shared) == []


def test_use_edges_must_resolve_to_m1_and_disposition():
    non_m1 = copy.deepcopy(PACKAGE)
    non_m1["implementationSlices"][0]["requirementIds"].append("CRS-M1-99999")
    assert any("non-M1" in item for item in errors(non_m1))

    required = next(row for row in PACKAGE["protocolInputDispositions"] if row["firstSliceRequired"] and row["disposition"] == "FIRST-SLICE-IMPLEMENTATION")
    downgraded = copy.deepcopy(PACKAGE)
    row = next(item for item in downgraded["protocolInputDispositions"] if item["inputRequirementId"] == required["inputRequirementId"])
    row.update(disposition="NOT-TOOL-OBLIGATION")
    row.pop("moduleId"); row.pop("recordId"); row.pop("acceptanceCaseId")
    assert any("required use has no implementation" in item for item in errors(downgraded))


def test_all_first_slice_references_are_closed_independently():
    row = next(item for item in PACKAGE["protocolInputDispositions"] if item["disposition"] == "FIRST-SLICE-IMPLEMENTATION")
    for field in ("moduleId", "recordId", "acceptanceCaseId"):
        mutated = copy.deepcopy(PACKAGE)
        target = next(item for item in mutated["protocolInputDispositions"] if item["inputRequirementId"] == row["inputRequirementId"])
        target[field] = "MISSING-REFERENCE"
        assert errors(mutated), field


def test_ready_is_stage_locked_even_with_trimmed_relations_or_evidence():
    for evidence in ([], [""], ["   "], ["README.md"]):
        mutated = copy.deepcopy(PACKAGE)
        mutated["reviewBoundary"] = {"readiness": "READY", "claims": "SPECIFICATION-ONLY", "completionEvidence": evidence}
        assert any("READY is prohibited" in item for item in errors(mutated))
