"""Validate the authoritative CL-TAV first-slice development contract."""
from __future__ import annotations

import copy
import json
import hashlib
import re
import subprocess
import sys
from pathlib import Path, PureWindowsPath

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

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


def _field_definition_errors(definition: object, path: str, *, allow_required: bool = True) -> list[str]:
    if not isinstance(definition, dict) or not definition:
        return [f"{path} field definition must be a nonempty object"]
    errors: list[str] = []
    unknown = set(definition) - FIELD_SCHEMA_KEYS
    if unknown:
        errors.append(f"{path} field definition has unsupported keywords: {sorted(unknown)}")
    declared_type = definition.get("type")
    if "type" in definition and (not isinstance(declared_type, str) or declared_type not in FIELD_SCHEMA_TYPES):
        errors.append(f"{path} field definition has unsupported type")
    if "type" not in definition and "oneOf" not in definition:
        errors.append(f"{path} field definition requires type or oneOf")
    if "type" in definition and "oneOf" in definition:
        errors.append(f"{path} field definition cannot combine type and oneOf")
    if not isinstance(definition.get("constraintId"), str) or not re.fullmatch(r"RC-[A-Z0-9-]+", definition.get("constraintId", "")):
        errors.append(f"{path} field definition lacks a valid constraintId")
    if "required" in definition:
        if not allow_required:
            errors.append(f"{path} nested required is unsupported; use parent requiredProperties")
        elif not isinstance(definition["required"], bool):
            errors.append(f"{path} field definition required must be boolean")
    integer_keywords = ("minLength", "minItems", "maxItems")
    for key in integer_keywords:
        if key in definition and (not isinstance(definition[key], int) or isinstance(definition[key], bool) or definition[key] < 0):
            errors.append(f"{path} {key} must be a non-negative integer")
    if isinstance(definition.get("minItems"), int) and isinstance(definition.get("maxItems"), int) and definition["minItems"] > definition["maxItems"]:
        errors.append(f"{path} minItems exceeds maxItems")
    for key in ("minimum", "maximum"):
        if key in definition and (not isinstance(definition[key], (int, float)) or isinstance(definition[key], bool)):
            errors.append(f"{path} {key} must be a number")
    if "minimum" in definition and "maximum" in definition and isinstance(definition["minimum"], (int, float)) and isinstance(definition["maximum"], (int, float)) and definition["minimum"] > definition["maximum"]:
        errors.append(f"{path} minimum exceeds maximum")
    if "uniqueItems" in definition and not isinstance(definition["uniqueItems"], bool):
        errors.append(f"{path} uniqueItems must be boolean")
    if "enum" in definition and (not isinstance(definition["enum"], list) or not definition["enum"]):
        errors.append(f"{path} enum must be a nonempty array")
    if "pattern" in definition:
        if not isinstance(definition["pattern"], str):
            errors.append(f"{path} pattern must be a string")
        else:
            try:
                re.compile(definition["pattern"])
            except (re.error, OverflowError):
                errors.append(f"{path} pattern is not a valid regular expression")
    keyword_types = {
        "minLength": {"string"}, "pattern": {"string"},
        "minimum": {"integer", "number"}, "maximum": {"integer", "number"},
        "minItems": {"array"}, "maxItems": {"array"}, "uniqueItems": {"array"}, "items": {"array"},
        "properties": {"object"}, "requiredProperties": {"object"}, "additionalProperties": {"object"},
    }
    for key, allowed_types in keyword_types.items():
        if key in definition and (not isinstance(declared_type, str) or declared_type not in allowed_types):
            errors.append(f"{path} {key} is not valid for type {declared_type!r}")
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
                errors.extend(_field_definition_errors(child, f"{path}.{key}", allow_required=False))
    for key in ("items", "additionalProperties"):
        value = definition.get(key)
        if isinstance(value, dict):
            errors.extend(_field_definition_errors(value, f"{path}.{key}", allow_required=False))
        elif key in definition and key == "items":
            errors.append(f"{path} items must be a field definition")
        elif key in definition and not isinstance(value, bool):
            errors.append(f"{path} additionalProperties must be boolean or a field definition")
    if "oneOf" in definition:
        if not isinstance(definition["oneOf"], list) or not definition["oneOf"]:
            errors.append(f"{path} oneOf must be a nonempty array")
        else:
            for index, child in enumerate(definition["oneOf"]):
                errors.extend(_field_definition_errors(child, f"{path}.oneOf[{index}]", allow_required=False))
    if isinstance(definition.get("requiredProperties"), list) and all(isinstance(item, str) for item in definition["requiredProperties"]) and isinstance(definition.get("properties"), dict):
        missing = set(definition["requiredProperties"]) - set(definition["properties"])
        if missing:
            errors.append(f"{path} requiredProperties names unknown properties: {sorted(missing)}")
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


def _oneof_leaves(definition: dict) -> list[dict]:
    candidates = definition.get("oneOf")
    if not candidates:
        return [definition]
    return [leaf for candidate in candidates for leaf in _oneof_leaves(candidate)]


def _type_compatible(definition: dict, value: object) -> bool:
    candidates = definition.get("oneOf")
    if candidates:
        return any(_type_compatible(candidate, value) for candidate in candidates)
    expected = definition.get("type")
    if expected == "null":
        return value is None
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return False


def _definitions_for_path(record: dict, parts: list[object]) -> list[dict]:
    if not parts or not isinstance(parts[0], str):
        return []
    definitions = [record["fieldDefinitions"].get(parts[0], {})]
    for part in parts[1:]:
        advanced: list[dict] = []
        for definition in definitions:
            for candidate in _oneof_leaves(definition):
                if candidate.get("type") == "array" and isinstance(part, int):
                    advanced.append(candidate.get("items", {}))
                elif candidate.get("type") == "object" and isinstance(part, str) and part in candidate.get("properties", {}):
                    advanced.append(candidate["properties"][part])
                elif candidate.get("type") == "object" and isinstance(part, str) and isinstance(candidate.get("additionalProperties"), dict):
                    advanced.append(candidate["additionalProperties"])
        definitions = [definition for definition in advanced if definition]
        if not definitions:
            break
    return definitions


def _definition_for_path(record: dict, parts: list[object]) -> dict:
    definitions = _definitions_for_path(record, parts)
    return definitions[0] if len(definitions) == 1 else {}


def _required_instance_errors(record: dict, definition: dict, value: object, parts: list[object]) -> list[tuple[str, tuple[object, ...], str]]:
    results: list[tuple[str, tuple[object, ...], str]] = []
    candidates = definition.get("oneOf", [])
    if candidates:
        valid = [item for item in candidates if Draft202012Validator(_json_schema(item)).is_valid(value)]
        type_compatible = [item for item in candidates if _type_compatible(item, value)]
        selected = valid if len(valid) == 1 else type_compatible if not valid and len(type_compatible) == 1 else []
        for item in selected:
            results.extend(_required_instance_errors(record, item, value, parts))
        return results
    if definition.get("type") == "object" and isinstance(value, dict):
        for name in definition.get("requiredProperties", []):
            if name not in value:
                child = definition.get("properties", {}).get(name, {})
                results.append((child.get("constraintId", "RC-UNKNOWN-FIELD"), tuple([*parts, name]), f"required property {name!r} is missing"))
        for name, child_value in value.items():
            child = definition.get("properties", {}).get(name)
            if child is None and isinstance(definition.get("additionalProperties"), dict):
                child = definition["additionalProperties"]
            if child is not None:
                results.extend(_required_instance_errors(record, child, child_value, [*parts, name]))
    elif definition.get("type") == "array" and isinstance(value, list) and isinstance(definition.get("items"), dict):
        for index, child_value in enumerate(value):
            results.extend(_required_instance_errors(record, definition["items"], child_value, [*parts, index]))
    return results


def validate_record_instance(record: dict, payload: object) -> list[tuple[str, tuple[object, ...], str]]:
    """Return stable (constraint ID, field path, diagnostic) tuples."""
    if not isinstance(payload, dict):
        return [("RC-RECORD-TYPE", (), "record must be an object")]
    try:
        schema = {
            "type": "object",
            "properties": {field: _json_schema(record["fieldDefinitions"][field]) for field in record["fields"]},
            "required": [field for field in record["fields"] if record["fieldDefinitions"][field].get("required")],
            "additionalProperties": False,
        }
        Draft202012Validator.check_schema(schema)
    except (AttributeError, KeyError, TypeError, SchemaError, re.error, OverflowError) as exc:
        return [("RC-DEFINITION-INVALID", (), f"record definition is invalid: {exc}")]
    results: list[tuple[str, tuple[object, ...], str]] = []
    for field in schema["required"]:
        if field not in payload:
            results.append((record["fieldDefinitions"][field]["constraintId"], (field,), f"required property {field!r} is missing"))
    for field, value in payload.items():
        if field in record["fieldDefinitions"]:
            results.extend(_required_instance_errors(record, record["fieldDefinitions"][field], value, [field]))
    for error in Draft202012Validator(schema).iter_errors(payload):
        parts: list[object] = list(error.absolute_path)
        if error.validator == "required":
            continue
        elif error.validator == "additionalProperties":
            known = set(error.schema.get("properties", {}))
            extra = sorted(set(error.instance) - known)[0] if isinstance(error.instance, dict) and set(error.instance) - known else "?"
            parts.append(extra)
            definition = {}
        else:
            definition = _definition_for_path(record, parts)
        results.append((definition.get("constraintId", "RC-UNKNOWN-FIELD"), tuple(parts), error.message))
    if results:
        return results
    if record["id"] == "PACKET-REF" and payload["caplen"] > payload["origlen"]:
        results.append(("RC-PACKET-CAPLEN", ("caplen",), "captured length exceeds original length"))
    if record["id"] == "OBSERVATION-ASSESSMENT" and isinstance(payload.get("measurementInterval"), dict):
        interval = payload["measurementInterval"]
        if interval["lower"] > interval["upper"]:
            results.append(("RC-OBS-INTERVAL", ("measurementInterval",), "lower endpoint exceeds upper endpoint"))
        if interval["lower"] == interval["upper"] and not (interval["lowerClosed"] and interval["upperClosed"]):
            results.append(("RC-OBS-INTERVAL", ("measurementInterval",), "equal endpoints require a closed point interval"))
    if record["id"] == "OBSERVATION-ASSESSMENT" and payload.get("measurementInterval") is None and payload.get("verdict") != "ERROR":
        results.append(("RC-OBS-INTERVAL", ("measurementInterval",), "an absent measurement interval requires ERROR"))
    if record["id"] == "DATAGRAM-RECORD":
        for index, coverage in enumerate(payload["coverage"]):
            if coverage["start"] >= coverage["endExclusive"]:
                results.append(("RC-DATAGRAM-RANGE", ("coverage", index), "coverage requires start < endExclusive"))
    if record["id"] == "INTAKE-METADATA" and isinstance(payload.get("clockAccuracy"), dict):
        clock = payload["clockAccuracy"]
        if clock.get("state") == "DECLARED" and "boundNs" not in clock:
            results.append(("RC-INTAKE-CLOCK", ("clockAccuracy",), "declared clock accuracy lacks boundNs"))
        if clock.get("state") == "UNKNOWN" and "boundNs" in clock:
            results.append(("RC-INTAKE-CLOCK", ("clockAccuracy",), "unknown clock accuracy must not invent boundNs"))
    if record["id"] == "TRANSFER-RECORD" and isinstance(payload.get("optionState"), dict):
        option_state = payload["optionState"]
        if option_state.get("mode") == "UNKNOWN" and option_state.get("values"):
            results.append(("RC-TRANSFER-OPTION-STATE", ("optionState",), "unknown option state must not claim negotiated values"))
        if option_state.get("mode") in {"ACCEPTED", "DEFAULTED"} and not option_state.get("values"):
            results.append(("RC-TRANSFER-OPTION-STATE", ("optionState",), "accepted or defaulted option state requires effective values"))
        if option_state.get("mode") == "DEFAULTED" and "blksize" in option_state.get("values", {}) and option_state["values"]["blksize"] != 512:
            results.append(("RC-OPTION-BLKSIZE", ("optionState", "values", "blksize"), "DEFAULTED blksize must equal the bound default 512"))
        for block_id in payload["blockMap"]:
            if not re.fullmatch(r"(?:0|[1-9][0-9]{0,4})", block_id) or int(block_id) > 65535:
                results.append(("RC-TRANSFER-BLOCK-MAP", ("blockMap", block_id), "block identity must be decimal 0..65535"))
    if record["id"] == "HISTORY-HANDLE":
        hypotheses = set(payload["H"])
        compatible = payload.get("compatibleStateByHypothesis")
        statuses = payload.get("statusByHypothesis", {})
        if isinstance(compatible, dict) and set(compatible) != hypotheses:
            results.append(("RC-HISTORY-COMPATIBLE", ("compatibleStateByHypothesis",), "compatible histories must exactly cover H"))
        if isinstance(statuses, dict) and not set(statuses).issubset(hypotheses):
            results.append(("RC-HISTORY-STATUS", ("statusByHypothesis",), "status refers to a hypothesis outside H"))
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
    valid_record_definitions: set[str] = set()
    for record in data["recordContracts"]:
        if record["ownerModuleId"] not in modules:
            errors.append(f"{record['id']} has an unknown owner module")
        if any(requirement_id not in expected for requirement_id in record.get("sourceRequirementIds", [])):
            errors.append(f"{record['id']} has an unknown source requirement")
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
        valid_record_definitions.add(record["id"])
        example_errors = validate_record_instance(record, record["example"])
        if example_errors:
            errors.append(f"{record['id']} example is invalid: {example_errors}")
        invalid_errors = validate_record_instance(record, record["invalidExample"])
        if not invalid_errors:
            errors.append(f"{record['id']} invalid example violates no field constraint")
        expected_error = record["invalidExpected"]
        expected_parts: list[object] = expected_error["path"]
        expected_definitions = _definitions_for_path(record, expected_parts)
        if expected_error["constraintId"] not in {definition.get("constraintId") for definition in expected_definitions}:
            errors.append(f"{record['id']} invalidExpected does not resolve to its declared constraint")
        if not any(code == expected_error["constraintId"] and list(path) == expected_error["path"] for code, path, _ in invalid_errors):
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
    tool_by_id = {row["id"]: row for row in data["toolRequirements"]}
    record_by_id = {row["id"]: row for row in data["recordContracts"]}
    runtime_parameter_ids = {row["id"] for row in data["runtimeParameterContracts"]}
    module_by_id = {row["id"]: row for row in data["moduleContracts"]}
    parameter_ids = [row["id"] for row in data["runtimeParameterContracts"]]
    if len(parameter_ids) != len(set(parameter_ids)):
        errors.append("runtimeParameterContracts repeats an ID")
    case_by_id = {row["id"]: row for row in data["acceptanceCases"]}
    registry_by_id = {row["id"]: row for row in registry["interfaces"]}
    bound_interface_ids: list[str] = []
    for refinement in data["algorithmRefinements"]:
        binding_ids = [binding["interfaceId"] for binding in refinement["interfaceBindings"]]
        if len(binding_ids) != len(set(binding_ids)):
            errors.append(f"{refinement['id']} repeats an interface binding")
        bound_interface_ids.extend(binding_ids)
        for binding in refinement["interfaceBindings"]:
            source = registry_by_id.get(binding["interfaceId"])
            if source is None:
                errors.append(f"{refinement['id']} has an unknown algorithm interface binding")
                continue
            if binding["inputTypes"] != source["inputs"]:
                errors.append(f"{binding['interfaceId']} input types differ from interface registry")
            if binding["outputTypes"] != source["outputs"]:
                errors.append(f"{binding['interfaceId']} output types differ from interface registry")
            if binding["interfaceId"] == "IF-SELECT-ADMIT":
                if binding["writeOwnership"] != "Read-only; S3-SNAP constructs the immutable final SelectSnapshot after this interface returns.":
                    errors.append("IF-SELECT-ADMIT must remain read-only; S3-SNAP constructs the final SelectSnapshot")
            if not set(binding["runtimeParameterIds"]).issubset(runtime_parameter_ids):
                errors.append(f"{binding['interfaceId']} has an unknown runtime parameter")
            if not set(binding["acceptanceCaseIds"]).issubset(cases):
                errors.append(f"{binding['interfaceId']} has an unknown acceptance case")
            for field in ("readOwnership", "writeOwnership", "timeContract", "timeContractZh", "implementationLocation"):
                if not binding[field].strip():
                    errors.append(f"{binding['interfaceId']} has blank {field}")
            for field in ("readOwnershipZh", "writeOwnershipZh"):
                if not binding[field].strip():
                    errors.append(f"{binding['interfaceId']} has blank {field}")
    if set(bound_interface_ids) != interface_ids:
        errors.append("algorithm interface bindings must equal the interface registry")
    for refinement in data["algorithmRefinements"]:
        finite = refinement["finiteKernelContract"]
        required_frontier = {"hypothesisId", "controlStateId", "clockConstraint", "typedStore", "pathLength", "historyProvenance", "status"}
        if set(finite["frontierEntryFields"]) != required_frontier:
            errors.append(f"{refinement['id']} finite frontier fields are incomplete")
        if not set(finite["mergeKey"]).issubset(required_frontier) or "historyProvenance" not in finite["mergeKey"]:
            errors.append(f"{refinement['id']} merge key may lose whole-history provenance")
        expected_mapping = {binding["interfaceId"] for binding in refinement["interfaceBindings"]}
        if set(finite["resultMapping"]) != expected_mapping:
            errors.append(f"{refinement['id']} result mapping differs from its algorithm interfaces")
        for binding in refinement["interfaceBindings"]:
            mapping = finite["resultMapping"].get(binding["interfaceId"], {})
            if mapping.get("success") != binding["outputTypes"] or mapping.get("failure") != binding["failureTags"]:
                errors.append(f"{refinement['id']} result mapping is stale for {binding['interfaceId']}")
    experiment_registry = {item["id"]: item for item in registry.get("experimentInterfaces", [])}
    experiment_bindings = data["experimentInterfaceBindings"]
    experiment_binding_ids = [item["interfaceId"] for item in experiment_bindings]
    if len(experiment_binding_ids) != len(set(experiment_binding_ids)) or set(experiment_binding_ids) != set(experiment_registry):
        errors.append("experiment interface bindings must equal the controlled registry")
    for binding in experiment_bindings:
        source = experiment_registry.get(binding["interfaceId"])
        if source is None:
            continue
        if binding["inputTypes"] != source["inputs"] or binding["outputTypes"] != source["outputs"]:
            errors.append(f"{binding['interfaceId']} experiment I/O differs from the registry")
        if binding["failureBehavior"] != source["failure"] or binding["resourceContract"] != source["resourceBasis"]:
            errors.append(f"{binding['interfaceId']} experiment failure/resource contract differs from the registry")
        if not set(binding["acceptanceCaseIds"]).issubset(cases):
            errors.append(f"{binding['interfaceId']} has an unknown experiment acceptance case")
        for field in ("readOwnership", "readOwnershipZh", "writeOwnership", "writeOwnershipZh", "failureBehaviorZh", "resourceContractZh", "implementationLocation"):
            if not binding[field].strip():
                errors.append(f"{binding['interfaceId']} has blank {field}")
    for parameter in data["runtimeParameterContracts"]:
        if not set(parameter["acceptanceCaseIds"]).issubset(cases):
            errors.append(f"{parameter['id']} has an unknown acceptance case")
        for field in ("title", "titleZh", "unit", "configurationRequirement", "configurationRequirementZh", "exhaustionBehavior", "exhaustionBehaviorZh", "ownerScope", "ownerScopeZh"):
            if not parameter[field].strip():
                errors.append(f"{parameter['id']} has blank {field}")
    for case in data["acceptanceCases"]:
        if not set(case["inputRecordIds"]).issubset(records):
            errors.append(f"{case['id']} has an unknown input record")
        if not set(case["toolRequirementIds"]).issubset(tool_by_id):
            errors.append(f"{case['id']} has an unknown tool requirement")
        if not set(case["moduleIds"]).issubset(modules):
            errors.append(f"{case['id']} has an unknown module")
        if not set(case["algorithmInterfaceIds"]).issubset(interface_ids):
            errors.append(f"{case['id']} has an unknown algorithm interface")
        for field in ("title", "titleZh", "expectedContractOutput", "expectedContractOutputZh", "prohibitedOutput", "prohibitedOutputZh", "basis", "basisZh"):
            if not case[field].strip():
                errors.append(f"{case['id']} has blank {field}")
        if case["inputFixture"].get("recordIds") != case["inputRecordIds"]:
            errors.append(f"{case['id']} fixture record identities differ from the case inputs")
        if case["expectedOutputFixture"].get("statement") != case["expectedContractOutput"]:
            errors.append(f"{case['id']} expected fixture differs from the controlled expected output")
        if not case["prohibitedOutputPaths"] or not case["negativeVariants"]:
            errors.append(f"{case['id']} lacks concrete prohibited outputs or negative variants")
        for tool_id in case["toolRequirementIds"]:
            tool = tool_by_id.get(tool_id)
            if tool is not None and tool["ownerModuleId"] not in case["moduleIds"]:
                errors.append(f"{case['id']} tool {tool_id} omits owner module {tool['ownerModuleId']}")
    required_matrix_categories = {"corpus identity", "label boundary", "capture format", "IP reassembly", "TFTP reconstruction", "field contracts", "matching and no response", "timing and U", "prediction and admission", "history update", "state and return", "resource accounting", "experiment boundary", "controlled drift"}
    matrix_ids = [item["id"] for item in data["acceptanceMatrix"]]
    if len(matrix_ids) != len(set(matrix_ids)) or {item["category"] for item in data["acceptanceMatrix"]} != required_matrix_categories:
        errors.append("acceptanceMatrix must cover each controlled category exactly once")
    if any(not item[field].strip() for item in data["acceptanceMatrix"] for field in ("category", "categoryZh", "positiveInput", "positiveInputZh", "expectedOutput", "expectedOutputZh", "negativeMutation", "negativeMutationZh", "expectedRejection", "expectedRejectionZh")):
        errors.append("acceptanceMatrix contains a blank executable specification")
    scenario_ids = [item["id"] for item in data["experimentScenarios"]]
    if len(scenario_ids) != len(set(scenario_ids)) or len(scenario_ids) < 8:
        errors.append("experimentScenarios must contain eight unique first-batch scenes")
    for scenario in data["experimentScenarios"]:
        for field in ("title", "titleZh", "serviceScope", "controllableAction", "faultConfirmation", "independentTruthSource", "resetContract", "timingContract", "resourceContract"):
            if not scenario[field].strip():
                errors.append(f"{scenario['id']} has blank {field}")
        visible = " ".join(scenario["algorithmVisibleFields"]).lower()
        if "truth" in visible or "injection plan" in visible:
            errors.append(f"{scenario['id']} leaks evaluator truth into algorithm-visible fields")
    for tool in data["toolRequirements"]:
        case = case_by_id.get(tool["acceptanceCaseId"])
        if case is not None:
            if tool["id"] not in case["toolRequirementIds"]:
                errors.append(f"{tool['id']} is absent from its acceptance case")
            if tool["ownerModuleId"] not in case["moduleIds"]:
                errors.append(f"{tool['id']} acceptance case omits its owner module")
            if not set(tool["interfaceIds"]).intersection(case["algorithmInterfaceIds"]):
                errors.append(f"{tool['id']} acceptance case omits its interface")
    for refinement in data["algorithmRefinements"]:
        for binding in refinement["interfaceBindings"]:
            for case_id in binding["acceptanceCaseIds"]:
                case = case_by_id.get(case_id)
                if case is not None and binding["interfaceId"] not in case["algorithmInterfaceIds"]:
                    errors.append(f"{binding['interfaceId']} acceptance case {case_id} omits that interface")
    parameter_consumers: dict[str, set[tuple[str, str]]] = {parameter_id: set() for parameter_id in runtime_parameter_ids}
    for refinement in data["algorithmRefinements"]:
        for binding in refinement["interfaceBindings"]:
            for parameter_id in binding["runtimeParameterIds"]:
                parameter_consumers.setdefault(parameter_id, set()).add(("interface", binding["interfaceId"]))
    for module in data["moduleContracts"]:
        for parameter_id in module["runtimeParameterIds"]:
            parameter_consumers.setdefault(parameter_id, set()).add(("module", module["id"]))
    for parameter in data["runtimeParameterContracts"]:
        for case_id in parameter["acceptanceCaseIds"]:
            case = case_by_id.get(case_id)
            if case is None:
                continue
            consumers = parameter_consumers.get(parameter["id"], set())
            covered = (("interface", interface_id) in consumers for interface_id in case["algorithmInterfaceIds"])
            covered_module = (("module", module_id) in consumers for module_id in case["moduleIds"])
            if not any(covered) and not any(covered_module):
                errors.append(f"{parameter['id']} acceptance case {case_id} has no parameter consumer")
    retry_cap = next((parameter for parameter in data["runtimeParameterContracts"] if parameter["id"] == "RP-RETRY-CAP"), None)
    if retry_cap is not None and retry_cap["domain"] != "POSITIVE-INTEGER":
        errors.append("RP-RETRY-CAP must retain the existing positive-integer domain")
    upstream_graph: dict[str, set[str]] = {}
    for module in data["moduleContracts"]:
        for field in ("title", "titleZh", "responsibility", "responsibilityZh"):
            if not module[field].strip():
                errors.append(f"{module['id']} has blank {field}")
        for field in ("preconditions", "preconditionsZh", "invariants", "invariantsZh"):
            if any(not item.strip() for item in module[field]):
                errors.append(f"{module['id']} has blank {field}")
        if len(module["steps"]) != len({step["id"] for step in module["steps"]}):
            errors.append(f"{module['id']} repeats a step ID")
        for step in module["steps"]:
            if not step["action"].strip() or not step["actionZh"].strip():
                errors.append(f"{module['id']} has a blank step action")
        if len(module["failureOutcomes"]) != len({outcome["code"] for outcome in module["failureOutcomes"]}):
            errors.append(f"{module['id']} repeats a failure outcome code")
        for outcome in module["failureOutcomes"]:
            if any(not outcome[field].strip() for field in ("condition", "conditionZh", "result", "resultZh")):
                errors.append(f"{module['id']} has a blank failure outcome")
        referenced_records = set(module["inputRecordIds"]) | set(module["outputRecordIds"])
        if not referenced_records.issubset(records):
            errors.append(f"{module['id']} has an unknown record reference")
        if any(record_by_id[record_id]["ownerModuleId"] != module["id"] for record_id in module["outputRecordIds"] if record_id in record_by_id):
            errors.append(f"{module['id']} claims an output owned by another module")
        if not set(module["toolRequirementIds"]).issubset(tool_by_id):
            errors.append(f"{module['id']} has an unknown tool requirement")
        owned_tools = {tool_id for tool_id, tool in tool_by_id.items() if tool["ownerModuleId"] == module["id"]}
        if set(module["toolRequirementIds"]) != owned_tools:
            errors.append(f"{module['id']} tool requirements differ from owned requirements")
        for tool_id in set(module["toolRequirementIds"]) & set(tool_by_id):
            tool = tool_by_id[tool_id]
            if not set(tool["inputRecordIds"]).issubset(module["inputRecordIds"]):
                errors.append(f"{module['id']} omits an owned requirement input")
            if not set(tool["outputRecordIds"]).issubset(module["outputRecordIds"]):
                errors.append(f"{module['id']} omits an owned requirement output")
            if not set(tool["interfaceIds"]).issubset(module["interfaceIds"]):
                errors.append(f"{module['id']} omits an owned requirement interface")
        if not set(module["interfaceIds"]).issubset(interface_ids):
            errors.append(f"{module['id']} has an unknown interface reference")
        if not set(module["acceptanceCaseIds"]).issubset(cases):
            errors.append(f"{module['id']} has an unknown acceptance case")
        required_cases = {tool_by_id[tool_id]["acceptanceCaseId"] for tool_id in module["toolRequirementIds"] if tool_id in tool_by_id}
        for missing_case in sorted(required_cases - set(module["acceptanceCaseIds"])):
            requiring_tools = sorted(tool_id for tool_id in module["toolRequirementIds"] if tool_id in tool_by_id and tool_by_id[tool_id]["acceptanceCaseId"] == missing_case)
            errors.append(f"{module['id']} omits acceptance case {missing_case} required by {requiring_tools}")
        if not set(module["runtimeParameterIds"]).issubset(runtime_parameter_ids):
            errors.append(f"{module['id']} has an unknown runtime parameter")
        mapping_keys = [(mapping["recordId"], mapping["field"]) for mapping in module["outputValueMappings"]]
        if len(mapping_keys) != len(set(mapping_keys)):
            errors.append(f"{module['id']} repeats an output value mapping")
        for mapping in module["outputValueMappings"]:
            record = record_by_id.get(mapping["recordId"])
            if mapping["recordId"] not in module["outputRecordIds"] or record is None:
                errors.append(f"{module['id']} output mapping references a non-output record")
                continue
            if mapping["field"] not in record["fieldDefinitions"]:
                errors.append(f"{module['id']} output mapping references an unknown field")
                continue
            if not mapping["meaning"].strip() or not mapping["meaningZh"].strip():
                errors.append(f"{module['id']} has a blank output mapping meaning")
            # A malformed record contract already has a named definition
            # diagnostic above.  Do not re-enter instance validation here:
            # mapping checks must remain deterministic and must not turn that
            # contract error into an AttributeError.
            if mapping["recordId"] not in valid_record_definitions:
                continue
            for value in mapping["emittedValues"]:
                witness = copy.deepcopy(record["example"])
                witness[mapping["field"]] = value
                if validate_record_instance(record, witness):
                    errors.append(f"{module['id']} output mapping emits invalid {mapping['recordId']}.{mapping['field']} value {value!r}")
        upstream = set(module["upstreamModuleIds"])
        if module["id"] in upstream or not upstream.issubset(modules):
            errors.append(f"{module['id']} has an invalid upstream module")
        upstream_graph[module["id"]] = upstream
    for record in data["recordContracts"]:
        owner = module_by_id.get(record["ownerModuleId"])
        if owner and record["id"] not in set(owner["inputRecordIds"]) | set(owner["outputRecordIds"]):
            errors.append(f"{record['id']} is absent from its owner module boundary")
    for start in modules:
        pending = list(upstream_graph.get(start, set()))
        visited: set[str] = set()
        while pending:
            current = pending.pop()
            if current == start:
                errors.append(f"{start} participates in an upstream dependency cycle")
                break
            if current not in visited:
                visited.add(current)
                pending.extend(upstream_graph.get(current, set()))
    for consumer_id, module in module_by_id.items():
        reachable: set[str] = set()
        pending = list(upstream_graph.get(consumer_id, set()))
        while pending:
            current = pending.pop()
            if current not in reachable:
                reachable.add(current)
                pending.extend(upstream_graph.get(current, set()))
        for record_id in module["inputRecordIds"]:
            producers = {producer_id for producer_id, producer in module_by_id.items() if producer_id != consumer_id and record_id in producer["outputRecordIds"]}
            for producer_id in sorted(producers - reachable):
                errors.append(f"{consumer_id} input {record_id} lacks producer dependency on {producer_id}")
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
    dependency_by_id = {item["id"]: item for item in data["implementationDependencies"]}
    if len(dependency_by_id) != len(data["implementationDependencies"]):
        errors.append("implementationDependencies repeats an ID")
    for dependency in data["implementationDependencies"]:
        if not set(dependency["requirementIds"]).issubset(expected):
            errors.append(f"{dependency['id']} has an unknown requirement")
        if not set(dependency["moduleIds"]).issubset(modules) or not set(dependency["recordIds"]).issubset(records) or not set(dependency["acceptanceCaseIds"]).issubset(cases):
            errors.append(f"{dependency['id']} has an unknown contract closure reference")
        for field in ("title", "titleZh", "affectedJudgments", "affectedJudgmentsZh", "specificationContract", "specificationContractZh", "failureBehavior", "failureBehaviorZh"):
            if not dependency[field].strip():
                errors.append(f"{dependency['id']} has blank {field}")
        if dependency["specificationStatus"] == "CLOSED" and (not dependency["closureEvidence"] or dependency["affectsSpecificationReadiness"]):
            errors.append(f"{dependency['id']} closed specification status is inconsistent")
        if dependency["runtimeStatus"] == "NOT-ESTABLISHED" and "NOT-EVALUATED" not in dependency["failureBehavior"]:
            errors.append(f"{dependency['id']} must preserve the runtime not-evaluated boundary")
        for requirement_id in dependency["requirementIds"]:
            row = next((item for item in rows if item["inputRequirementId"] == requirement_id), None)
            if row is None or dependency["id"] not in row.get("dependencyIds", []):
                errors.append(f"{dependency['id']} requirement {requirement_id} lacks its dependency relation")
    for row in rows:
        source = source_by_id.get(row["inputRequirementId"])
        if source and row["firstSliceRequired"] != (row["inputRequirementId"] in first_slice_ids):
            errors.append(f"{row['inputRequirementId']} has an incorrect firstSliceRequired classification")
        for dependency_id in row.get("dependencyIds", []):
            dependency = dependency_by_id.get(dependency_id)
            if dependency is None or row["inputRequirementId"] not in dependency["requirementIds"]:
                errors.append(f"{row['inputRequirementId']} has an invalid dependency relation")
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
    open_spec_dependencies = [item for item in data["implementationDependencies"] if item["specificationStatus"] != "CLOSED" or item["affectsSpecificationReadiness"]]
    if open_spec_dependencies and data["reviewBoundary"]["readiness"] != "READINESS-BLOCKED":
        errors.append("open specification dependency requires READINESS-BLOCKED")
    if data["reviewBoundary"]["readiness"] in {"CANDIDATE", "READY"}:
        evidence = data["reviewBoundary"]["completionEvidence"]
        if blocked or open_spec_dependencies or not evidence or not all(isinstance(item, str) and item.strip() for item in evidence):
            errors.append("candidate readiness requires closed specification dependencies and completion evidence")
        if any(row["disposition"] != "FIRST-SLICE-IMPLEMENTATION" and row["firstSliceRequired"] for row in rows):
            errors.append("candidate readiness cannot retain a required non-implementation disposition")
    if data["reviewBoundary"]["readiness"] == "READY":
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
