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


def _git_blob_json(relative: str) -> dict:
    raw = subprocess.check_output(["git", "show", f"HEAD:{relative}"], cwd=ROOT)
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
        elif binding["sha256"] != _git_blob_sha256(relative):
            errors.append(f"input binding content identity differs: {artifact_id}")
    try:
        registry = _git_blob_json(required_bindings["CLTAV-INTERFACE-REGISTRY"])
        if not isinstance(registry.get("interfaces"), list) or not registry["interfaces"]:
            errors.append("CL-TAV interface registry lacks interfaces")
    except (OSError, json.JSONDecodeError):
        errors.append("CL-TAV interface registry is unreadable")
    try:
        m1 = _git_blob_json(required_bindings["ARINC615A3-M1-CRS"])
    except (OSError, json.JSONDecodeError):
        return errors + ["bound M1 CRS is unreadable"]
    expected = {row["id"] for row in m1["requirements"]}
    source_by_id = {row["id"]: row for row in m1["requirements"]}
    first_slice_ids = {item for slice_ in data["implementationSlices"] for item in slice_.get("requirementIds", [])}
    flattened = [item for slice_ in data["implementationSlices"] for item in slice_.get("requirementIds", [])]
    if len(flattened) != len(set(flattened)):
        errors.append("implementationSlices repeats a requirement use")
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
    for row in rows:
        source = source_by_id.get(row["inputRequirementId"])
        if source and row["firstSliceRequired"] != (row["inputRequirementId"] in first_slice_ids):
            errors.append(f"{row['inputRequirementId']} has an incorrect firstSliceRequired classification")
        if source and row["inputRequirementId"] in first_slice_ids and "CRC" in set(source["semantic"].get("objects") or []) and row["disposition"] != "DEPENDENCY-BLOCKED":
            errors.append(f"{row['inputRequirementId']} must remain dependency-blocked")
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
