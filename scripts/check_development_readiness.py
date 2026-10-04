"""Validate the authoritative CL-TAV first-slice development contract."""
from __future__ import annotations

import json
import hashlib
import re
import subprocess
import sys
from pathlib import Path, PureWindowsPath

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PATH = ROOT / "configs/engineering/cltav_development_contracts.json"
SCHEMA_PATH = ROOT / "configs/engineering/cltav_development_contracts.schema.json"
M1_PATH = ROOT / "configs/requirements/arinc_615a3_m1_crs.json"

FIELD_SCHEMA_KEYS = {
    "type", "constraintId", "required", "enum", "const", "pattern", "minLength",
    "minimum", "maximum", "minItems", "maxItems", "uniqueItems", "items",
    "properties", "requiredProperties", "additionalProperties", "oneOf",
}
FIELD_SCHEMA_TYPES = {"string", "integer", "number", "boolean", "array", "object", "null"}


def _field_definition_errors(definition: object, path: str) -> list[str]:
    if not isinstance(definition, dict) or not definition:
        return [f"{path} field definition must be a nonempty object"]
    errors: list[str] = []
    unknown = set(definition) - FIELD_SCHEMA_KEYS
    if unknown:
        errors.append(f"{path} field definition has unsupported keywords: {sorted(unknown)}")
    if definition.get("type") not in FIELD_SCHEMA_TYPES and "oneOf" not in definition:
        errors.append(f"{path} field definition has unsupported type")
    if not isinstance(definition.get("constraintId"), str) or not re.fullmatch(r"RC-[A-Z0-9-]+", definition.get("constraintId", "")):
        errors.append(f"{path} field definition lacks a valid constraintId")
    if "required" in definition and not isinstance(definition["required"], bool):
        errors.append(f"{path} field definition required must be boolean")
    if "requiredProperties" in definition and (
        not isinstance(definition["requiredProperties"], list)
        or not all(isinstance(item, str) and item for item in definition["requiredProperties"])
    ):
        errors.append(f"{path} requiredProperties must be a string array")
    if "properties" in definition:
        if not isinstance(definition["properties"], dict):
            errors.append(f"{path} properties must be an object")
        else:
            for key, child in definition["properties"].items():
                errors.extend(_field_definition_errors(child, f"{path}.{key}"))
    for key in ("items", "additionalProperties"):
        value = definition.get(key)
        if isinstance(value, dict):
            errors.extend(_field_definition_errors(value, f"{path}.{key}"))
        elif key in definition and key == "items":
            errors.append(f"{path} items must be a field definition")
        elif key in definition and not isinstance(value, bool):
            errors.append(f"{path} additionalProperties must be boolean or a field definition")
    if "oneOf" in definition:
        if not isinstance(definition["oneOf"], list) or not definition["oneOf"]:
            errors.append(f"{path} oneOf must be a nonempty array")
        else:
            for index, child in enumerate(definition["oneOf"]):
                errors.extend(_field_definition_errors(child, f"{path}.oneOf[{index}]"))
    return errors


def _json_schema(definition: dict) -> dict:
    schema = {key: value for key, value in definition.items() if key not in {"required", "constraintId", "requiredProperties"}}
    if "items" in schema:
        schema["items"] = _json_schema(schema["items"])
    if isinstance(schema.get("additionalProperties"), dict):
        schema["additionalProperties"] = _json_schema(schema["additionalProperties"])
    if "properties" in schema:
        schema["properties"] = {key: _json_schema(value) for key, value in schema["properties"].items()}
    if "oneOf" in schema:
        schema["oneOf"] = [_json_schema(value) for value in schema["oneOf"]]
    if "requiredProperties" in definition:
        schema["required"] = definition["requiredProperties"]
    return schema


def validate_record_instance(record: dict, payload: object) -> list[tuple[str, str, str]]:
    """Return stable (constraint ID, field path, diagnostic) tuples."""
    if not isinstance(payload, dict):
        return [("RC-RECORD-TYPE", "$", "record must be an object")]
    schema = {
        "type": "object",
        "properties": {field: _json_schema(record["fieldDefinitions"][field]) for field in record["fields"]},
        "required": [field for field in record["fields"] if record["fieldDefinitions"][field].get("required")],
        "additionalProperties": False,
    }
    results: list[tuple[str, str, str]] = []
    for error in Draft202012Validator(schema).iter_errors(payload):
        parts = [str(item) for item in error.absolute_path]
        if error.validator == "required":
            missing = re.search(r"'([^']+)' is a required property", error.message)
            field = missing.group(1) if missing else "?"
            path = field
        elif error.validator == "additionalProperties":
            field = "?"
            path = "$"
        else:
            field = parts[0] if parts else "?"
            path = ".".join(parts) or "$"
        definition = record["fieldDefinitions"].get(field, {})
        results.append((definition.get("constraintId", "RC-UNKNOWN-FIELD"), path, error.message))
    if record["id"] == "PACKET-REF" and isinstance(payload.get("caplen"), int) and isinstance(payload.get("origlen"), int) and payload["caplen"] > payload["origlen"]:
        results.append(("RC-PACKET-CAPLEN", "caplen", "captured length exceeds original length"))
    if record["id"] == "OBSERVATION-ASSESSMENT" and isinstance(payload.get("measurementInterval"), dict):
        interval = payload["measurementInterval"]
        if isinstance(interval.get("lower"), int) and isinstance(interval.get("upper"), int) and interval["lower"] > interval["upper"]:
            results.append(("RC-OBS-INTERVAL", "measurementInterval", "lower endpoint exceeds upper endpoint"))
    if record["id"] == "INTAKE-METADATA" and isinstance(payload.get("clockAccuracy"), dict):
        clock = payload["clockAccuracy"]
        if clock.get("state") == "DECLARED" and "boundNs" not in clock:
            results.append(("RC-INTAKE-CLOCK", "clockAccuracy", "declared clock accuracy lacks boundNs"))
        if clock.get("state") == "UNKNOWN" and "boundNs" in clock:
            results.append(("RC-INTAKE-CLOCK", "clockAccuracy", "unknown clock accuracy must not invent boundNs"))
    if record["id"] == "TRANSFER-RECORD" and isinstance(payload.get("optionState"), dict):
        option_state = payload["optionState"]
        if option_state.get("mode") == "UNKNOWN" and option_state.get("values"):
            results.append(("RC-TRANSFER-OPTION-STATE", "optionState", "unknown option state must not claim negotiated values"))
    if record["id"] == "HISTORY-HANDLE" and isinstance(payload.get("H"), list):
        hypotheses = set(payload["H"])
        compatible = payload.get("compatibleStateByHypothesis")
        statuses = payload.get("statusByHypothesis", {})
        if isinstance(compatible, dict) and set(compatible) != hypotheses:
            results.append(("RC-HISTORY-COMPATIBLE", "compatibleStateByHypothesis", "compatible histories must exactly cover H"))
        if isinstance(statuses, dict) and not set(statuses).issubset(hypotheses):
            results.append(("RC-HISTORY-STATUS", "statusByHypothesis", "status refers to a hypothesis outside H"))
    return results



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
    for record in data["recordContracts"]:
        if record["ownerModuleId"] not in modules:
            errors.append(f"{record['id']} has an unknown owner module")
        if len(record["fields"]) != len(set(record["fields"])):
            errors.append(f"{record['id']} repeats a field")
        if set(record["fieldDefinitions"]) != set(record["fields"]):
            errors.append(f"{record['id']} field definitions do not match fields")
            if record.get("interfaceHandle") == "HistoryHandle":
                handle = registry.get("sessionHandles", {}).get("HistoryHandle", {})
                if record["fields"] != handle.get("fields"):
                    errors.append("HISTORY-HANDLE fields differ from interface HistoryHandle")
            continue
        definition_errors = [
            item
            for field, definition in record["fieldDefinitions"].items()
            for item in _field_definition_errors(definition, f"{record['id']}.{field}")
        ]
        if definition_errors:
            errors.extend(definition_errors)
            continue
        example_errors = validate_record_instance(record, record["example"])
        if example_errors:
            errors.append(f"{record['id']} example is invalid: {example_errors}")
        invalid_errors = validate_record_instance(record, record["invalidExample"])
        if not invalid_errors:
            errors.append(f"{record['id']} invalid example violates no field constraint")
        expected_error = record["invalidExpected"]
        if not any(code == expected_error["constraintId"] and path == expected_error["path"] for code, path, _ in invalid_errors):
            errors.append(f"{record['id']} invalid example does not match invalidExpected")
        if record["example"] == record["invalidExample"]:
            errors.append(f"{record['id']} invalid example equals example")
        if record.get("interfaceHandle") == "HistoryHandle":
            handle = registry.get("sessionHandles", {}).get("HistoryHandle", {})
            if record["fields"] != handle.get("fields"):
                errors.append("HISTORY-HANDLE fields differ from interface HistoryHandle")
            status_definition = record["fieldDefinitions"]["statusByHypothesis"].get("additionalProperties", {})
            if status_definition.get("enum") != handle.get("statusByHypothesisValues"):
                errors.append("HISTORY-HANDLE statuses differ from interface HistoryHandle")
        elif record["id"] == "HISTORY-HANDLE":
            errors.append("HISTORY-HANDLE lacks interfaceHandle binding")
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
            if re.fullmatch(r"DD-\d{3}", reference):
                if f"## {reference} " not in control_docs["DD"]:
                    errors.append(f"{tool['id']} has an unknown DD traceability reference")
            elif match := re.fullmatch(r"(CR-\d{4}-\d{3}) (AC-\d{2})", reference):
                change_id, acceptance_id = match.groups()
                if f"# {change_id} " not in control_docs["CR"] or f"| {acceptance_id} |" not in control_docs["CR"]:
                    errors.append(f"{tool['id']} has an unknown CR traceability reference")
            elif re.fullmatch(r"T\d+", reference):
                if f"\\tag{{{reference}}}" not in control_docs["T5"]:
                    errors.append(f"{tool['id']} has an unknown method traceability reference")
            elif re.fullmatch(r"IF-[A-Z-]+", reference):
                if reference not in interface_ids:
                    errors.append(f"{tool['id']} has an unknown interface traceability reference")
            elif re.fullmatch(r"CRS-M1-\d{5}", reference):
                if reference not in expected:
                    errors.append(f"{tool['id']} has an unknown protocol traceability reference")
            else:
                errors.append(f"{tool['id']} has an unsupported traceability reference")
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
