"""Shared validation for typed development-record contracts.

The repository readiness gate and the installed offline intake adapter consume
the same bounded record vocabulary.  Keeping the validator here prevents a
wheel from silently accepting a record that the controlled readiness gate
would reject (or vice versa).
"""

from __future__ import annotations

import re
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


FIELD_SCHEMA_KEYS = {
    "type", "constraintId", "required", "enum", "const", "pattern", "minLength",
    "minimum", "maximum", "minItems", "maxItems", "uniqueItems", "items",
    "properties", "requiredProperties", "additionalProperties", "oneOf",
}
FIELD_SCHEMA_TYPES = {"string", "integer", "number", "boolean", "array", "object", "null"}


def field_definition_errors(definition: object, path: str, *, allow_required: bool = True) -> list[str]:
    """Validate the small controlled field-definition dialect."""
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
    for key in ("minLength", "minItems", "maxItems"):
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
                errors.extend(field_definition_errors(child, f"{path}.{key}", allow_required=False))
    for key in ("items", "additionalProperties"):
        value = definition.get(key)
        if isinstance(value, dict):
            errors.extend(field_definition_errors(value, f"{path}.{key}", allow_required=False))
        elif key in definition and key == "items":
            errors.append(f"{path} items must be a field definition")
        elif key in definition and not isinstance(value, bool):
            errors.append(f"{path} additionalProperties must be boolean or a field definition")
    if "oneOf" in definition:
        if not isinstance(definition["oneOf"], list) or not definition["oneOf"]:
            errors.append(f"{path} oneOf must be a nonempty array")
        else:
            for index, child in enumerate(definition["oneOf"]):
                errors.extend(field_definition_errors(child, f"{path}.oneOf[{index}]", allow_required=False))
    if isinstance(definition.get("requiredProperties"), list) and all(isinstance(item, str) for item in definition["requiredProperties"]) and isinstance(definition.get("properties"), dict):
        missing = set(definition["requiredProperties"]) - set(definition["properties"])
        if missing:
            errors.append(f"{path} requiredProperties names unknown properties: {sorted(missing)}")
    return errors


def json_schema(definition: dict[str, Any]) -> dict[str, Any]:
    """Translate the controlled field dialect into a JSON Schema fragment."""
    schema = {key: value for key, value in definition.items() if key not in {"required", "constraintId", "requiredProperties"}}
    if "items" in schema:
        schema["items"] = json_schema(schema["items"])
    if isinstance(schema.get("additionalProperties"), dict):
        schema["additionalProperties"] = json_schema(schema["additionalProperties"])
    if "properties" in schema:
        schema["properties"] = {key: json_schema(value) for key, value in schema["properties"].items()}
    if "oneOf" in schema:
        schema["oneOf"] = [json_schema(value) for value in schema["oneOf"]]
    if "requiredProperties" in definition:
        schema["required"] = definition["requiredProperties"]
    return schema


def _oneof_leaves(definition: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = definition.get("oneOf")
    if not candidates:
        return [definition]
    return [leaf for candidate in candidates for leaf in _oneof_leaves(candidate)]


def _type_compatible(definition: dict[str, Any], value: object) -> bool:
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


def _definitions_for_path(record: dict[str, Any], parts: list[object]) -> list[dict[str, Any]]:
    if not parts or not isinstance(parts[0], str):
        return []
    definitions = [record["fieldDefinitions"].get(parts[0], {})]
    for part in parts[1:]:
        advanced: list[dict[str, Any]] = []
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


def _definition_for_path(record: dict[str, Any], parts: list[object]) -> dict[str, Any]:
    definitions = _definitions_for_path(record, parts)
    return definitions[0] if len(definitions) == 1 else {}


def _required_instance_errors(
    record: dict[str, Any], definition: dict[str, Any], value: object, parts: list[object],
) -> list[tuple[str, tuple[object, ...], str]]:
    results: list[tuple[str, tuple[object, ...], str]] = []
    candidates = definition.get("oneOf", [])
    if candidates:
        valid = [item for item in candidates if Draft202012Validator(json_schema(item)).is_valid(value)]
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


def validate_record_instance(record: dict[str, Any], payload: object) -> list[tuple[str, tuple[object, ...], str]]:
    """Return stable ``(constraint ID, field path, diagnostic)`` tuples."""
    if not isinstance(payload, dict):
        return [("RC-RECORD-TYPE", (), "record must be an object")]
    try:
        schema = {
            "type": "object",
            "properties": {field: json_schema(record["fieldDefinitions"][field]) for field in record["fields"]},
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
        if error.validator == "additionalProperties":
            known = set(error.schema.get("properties", {}))
            extra = sorted(set(error.instance) - known)[0] if isinstance(error.instance, dict) and set(error.instance) - known else "?"
            parts.append(extra)
            definition: dict[str, Any] = {}
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


# Compatibility aliases preserve the controlled checker module's established
# internal helper names while making its implementation the runtime one.
_field_definition_errors = field_definition_errors
_json_schema = json_schema

