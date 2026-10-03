"""Validate the authoritative CL-TAV first-slice development contract."""
from __future__ import annotations

import json
import hashlib
import subprocess
import sys
from pathlib import Path, PureWindowsPath

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PATH = ROOT / "configs/engineering/cltav_development_contracts.json"
SCHEMA_PATH = ROOT / "configs/engineering/cltav_development_contracts.schema.json"
M1_PATH = ROOT / "configs/requirements/arinc_615a3_m1_crs.json"



def _git_blob_sha256(relative: str) -> str:
    raw = subprocess.check_output(["git", "show", f"HEAD:{relative}"], cwd=ROOT)
    return hashlib.sha256(raw).hexdigest()


def _git_blob_json(relative: str, blobs: dict[str, bytes]) -> dict:
    raw = blobs[relative]
    return json.loads(raw.decode("utf-8"))


def package_errors(data: dict) -> list[str]:
    errors: list[str] = []
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors.extend(f"schema: {item.message}" for item in Draft202012Validator(schema).iter_errors(data))
    if errors:
        return errors
    binding_rows = data["inputBindings"]
    if len({row["artifactId"] for row in binding_rows}) != len(binding_rows):
        errors.append("inputBindings repeats an artifactId")
    if len({row["path"] for row in binding_rows}) != len(binding_rows):
        errors.append("inputBindings repeats a path")
    bindings = {row["artifactId"]: row for row in binding_rows}
    required_bindings = {
        "ARINC615A3-M1-CRS": "configs/requirements/arinc_615a3_m1_crs.json",
        "CLTAV-INTERFACE-REGISTRY": "configs/research/cltav_interface_registry.json",
    }
    if {key: row["path"] for key, row in bindings.items()} != required_bindings:
        errors.append("inputBindings must exactly bind M1 CRS and CL-TAV interface registry")
    blobs: dict[str, bytes] = {}
    for artifact_id, binding in bindings.items():
        relative = binding["path"]
        target = ROOT / relative
        windows = PureWindowsPath(relative)
        if Path(relative).is_absolute() or windows.is_absolute() or windows.drive or ".." in Path(relative).parts:
            errors.append(f"input binding path is unsafe: {artifact_id}")
            continue
        try:
            target.resolve(strict=True).relative_to(ROOT.resolve())
            tracked = subprocess.run(["git", "ls-files", "--error-unmatch", relative], cwd=ROOT, capture_output=True).returncode == 0
        except OSError:
            tracked = False
        if not target.is_file() or not tracked or target.is_symlink():
            errors.append(f"input binding is missing: {artifact_id}")
        else:
            raw = subprocess.check_output(["git", "show", f"HEAD:{relative}"], cwd=ROOT)
            blobs[relative] = raw
            if binding["sha256"] != hashlib.sha256(raw).hexdigest():
                errors.append(f"input binding content identity differs: {artifact_id}")
    if errors:
        return errors
    try:
        registry = _git_blob_json(required_bindings["CLTAV-INTERFACE-REGISTRY"], blobs)
        if not isinstance(registry.get("interfaces"), list) or not registry["interfaces"]:
            errors.append("CL-TAV interface registry lacks interfaces")
    except (OSError, json.JSONDecodeError):
        errors.append("CL-TAV interface registry is unreadable")
    try:
        m1 = _git_blob_json(required_bindings["ARINC615A3-M1-CRS"], blobs)
    except (OSError, json.JSONDecodeError):
        return errors + ["bound M1 CRS is unreadable"]
    expected = {row["id"] for row in m1["requirements"]}
    source_by_id = {row["id"]: row for row in m1["requirements"]}
    slice_ids = [slice_["id"] for slice_ in data["implementationSlices"]]
    if len(slice_ids) != len(set(slice_ids)):
        errors.append("implementationSlices repeats a slice ID")
    first_slice_ids = {item for slice_ in data["implementationSlices"] for item in slice_.get("requirementIds", [])}
    for slice_ in data["implementationSlices"]:
        used = slice_["requirementIds"]
        if len(used) != len(set(used)):
            errors.append(f"{slice_['id']} repeats a requirement use")
    if not first_slice_ids.issubset(expected):
        errors.append("implementationSlices contains a non-M1 requirement ID")
    rows = data["protocolInputDispositions"]
    actual = [row["inputRequirementId"] for row in rows]
    if len(actual) != len(set(actual)):
        errors.append("protocolInputDispositions repeats a requirement ID")
    if set(actual) != expected:
        errors.append("protocolInputDispositions must equal the bound M1 requirement set")
    modules = {row["id"] for row in data["moduleContracts"]}
    records = {row["id"] for row in data["recordContracts"]}
    cases = {row["id"] for row in data["acceptanceCases"]}
    for label, items in (("moduleContracts", data["moduleContracts"]), ("recordContracts", data["recordContracts"]), ("acceptanceCases", data["acceptanceCases"])):
        values = [row["id"] for row in items]
        if len(values) != len(set(values)):
            errors.append(f"{label} repeats an ID")
    tool_ids = [row["id"] for row in data["toolRequirements"]]
    if len(tool_ids) != len(set(tool_ids)):
        errors.append("toolRequirements repeats an ID")
    interface_ids = {row.get("id") for row in registry["interfaces"]}
    control_docs = {
        "DD": (ROOT / "docs/control/decisions/DESIGN_DECISIONS.md").read_text(encoding="utf-8"),
        "CR": (ROOT / "docs/control/changes/CR-2026-016.md").read_text(encoding="utf-8"),
        "T5": (ROOT / "docs/research/methodology/RR-2026-001_test_analysis_conformance_methodology.md").read_text(encoding="utf-8"),
    }
    for tool in data["toolRequirements"]:
        for field in ("title", "titleZh", "trigger", "triggerZh", "action", "actionZh", "errorUnknown", "errorUnknownZh", "evidence", "evidenceZh"):
            if not tool[field].strip():
                errors.append(f"{tool['id']} has blank {field}")
        if any(not item.strip() for field in ("preconditions", "preconditionsZh") for item in tool[field]):
            errors.append(f"{tool['id']} has a blank precondition")
        if tool["ownerModuleId"] not in modules:
            errors.append(f"{tool['id']} has an unknown owner module")
        for record_id in [*tool["inputRecordIds"], *tool["outputRecordIds"]]:
            if record_id not in records:
                errors.append(f"{tool['id']} has an unknown record reference")
        if tool["acceptanceCaseId"] not in cases:
            errors.append(f"{tool['id']} has an unknown acceptance case")
        if any(interface_id not in interface_ids for interface_id in tool.get("interfaceIds", [])):
            errors.append(f"{tool['id']} has an unknown interface reference")
        if any(requirement_id not in expected for requirement_id in tool["protocolRequirementIds"]):
            errors.append(f"{tool['id']} has an unknown protocol requirement reference")
        if tool["sourceRelationship"] == "PROTOCOL-DERIVED" and not tool["protocolRequirementIds"]:
            errors.append(f"{tool['id']} protocol-derived contract lacks protocol evidence")
        for reference in tool["traceability"]:
            if reference.startswith("DD-") and reference not in control_docs["DD"]:
                errors.append(f"{tool['id']} has an unknown DD traceability reference")
            elif reference.startswith("CR-") and reference.split(" ", 1)[0] not in control_docs["CR"]:
                errors.append(f"{tool['id']} has an unknown CR traceability reference")
            elif reference == "T5" and "\\tag{T5}" not in control_docs["T5"]:
                errors.append(f"{tool['id']} has an unknown method traceability reference")
            elif reference.startswith("IF-") and reference not in interface_ids:
                errors.append(f"{tool['id']} has an unknown interface traceability reference")
    for row in rows:
        source = source_by_id.get(row["inputRequirementId"])
        if source and row["firstSliceRequired"] != (row["inputRequirementId"] in first_slice_ids):
            errors.append(f"{row['inputRequirementId']} has an incorrect firstSliceRequired classification")
        if source and row["inputRequirementId"] in first_slice_ids and "CRC" in set(source["semantic"].get("objects") or []) and row["disposition"] != "DEPENDENCY-BLOCKED":
            errors.append(f"{row['inputRequirementId']} must remain dependency-blocked")
        if row["firstSliceRequired"] and row["disposition"] not in {"FIRST-SLICE-IMPLEMENTATION", "DEPENDENCY-BLOCKED"}:
            errors.append(f"{row['inputRequirementId']} required use has no implementation or dependency disposition")
        if row["disposition"] == "FIRST-SLICE-IMPLEMENTATION":
            for key, known, label in (("moduleId", modules, "module"), ("recordId", records, "record"), ("acceptanceCaseId", cases, "acceptance case")):
                if row.get(key) not in known:
                    errors.append(f"{row['inputRequirementId']} lacks a valid first-slice {label}")
        if row["firstSliceRequired"] and row["disposition"] == "FIRST-SLICE-IMPLEMENTATION":
            if not all(row.get(key) for key in ("moduleId", "recordId", "acceptanceCaseId")):
                errors.append(f"{row['inputRequirementId']} lacks a consumer/acceptance closure")
    blocked = [row for row in rows if row["disposition"] == "DEPENDENCY-BLOCKED" and row.get("firstSliceRequired")]
    if blocked and data["reviewBoundary"]["readiness"] != "READINESS-BLOCKED":
        errors.append("required blocked input requires READINESS-BLOCKED")
    if data["reviewBoundary"]["readiness"] == "READY":
        errors.append("READY is prohibited until the complete readiness gate is implemented")
        if blocked or not all(isinstance(item, str) and item.strip() for item in data["reviewBoundary"]["completionEvidence"]):
            errors.append("READY requires no required blocks and nonempty completion evidence")
        if any(row["disposition"] != "FIRST-SLICE-IMPLEMENTATION" and row["firstSliceRequired"] for row in rows):
            errors.append("READY cannot retain a required non-implementation disposition")
    if data["reviewBoundary"]["claims"] != "SPECIFICATION-ONLY":
        errors.append("review boundary must remain SPECIFICATION-ONLY")
    return errors


def main() -> int:
    try:
        data = json.loads(PACKAGE_PATH.read_text(encoding="utf-8"))
        errors = package_errors(data)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"development-readiness validation failed: {exc}", file=sys.stderr)
        return 1
    if errors:
        print("development-readiness validation failed:", file=sys.stderr)
        print("\n".join(f"- {item}" for item in errors), file=sys.stderr)
        return 1
    print(f"development-readiness validation passed: requirements={len(data['protocolInputDispositions'])}; readiness={data['reviewBoundary']['readiness']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
