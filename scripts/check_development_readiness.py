"""Validate the authoritative CL-TAV first-slice development contract."""
from __future__ import annotations

import copy
import json
import hashlib
import math
import re
import subprocess
import sys
from fractions import Fraction
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

# A relation is selected by the typed consumer contract, never by a case ID or
# by a free-text negative expectation.  This leaves room for new legal cases
# while preventing an equivalence witness from claiming a resource relation.
RELATION_CONTRACT_BINDINGS = {
    "RC-TRANSFER-TERMINAL": ({"IF-EXECUTE-RECORD", "IF-OBS-INTERPRET", "IF-HIST-UPDATE"}, {"TR-CAPTURE-INTAKE", "TR-DATAGRAM-REASSEMBLY", "TR-TRANSFER-RECONSTRUCTION", "TR-PROTOCOL-EVENT", "TR-OWNERSHIP", "TR-OBSERVATION-ASSESSMENT", "TR-HISTORY-COMPATIBILITY", "TR-TRACEABLE-FINDING"}),
    "RC-PREDICTION-NONEMPTY": ({"IF-PRED-OBS"}, {"TR-HISTORY-COMPATIBILITY"}),
    "RC-SELECT-STABLE-ID": ({"IF-SELECT-ADMIT"}, {"TR-HISTORY-COMPATIBILITY"}),
    "RC-VERDICT-WHOLE-INTERVAL": ({"IF-OBS-INTERPRET"}, {"TR-OBSERVATION-ASSESSMENT"}),
    "RC-SUMMARY-CONFIRMATION": ({"IF-PREP-RECOVER"}, {"TR-HISTORY-COMPATIBILITY"}),
    "RC-HISTORY-NO-RESURRECTION": ({"IF-HIST-UPDATE"}, {"TR-HISTORY-COMPATIBILITY"}),
    "RC-EQUIV-EVIDENCE": ({"IF-EQUIV"}, {"TR-HISTORY-COMPATIBILITY"}),
    "RC-RESOURCE-ONCE": ({"IF-RESOURCE-STOP"}, {"TR-HISTORY-COMPATIBILITY", "TR-TRACEABLE-FINDING"}),
    "RC-INTEGRITY-RUNTIME": ({"IF-OBS-INTERPRET"}, {"TR-PROTOCOL-EVENT"}),
    "RC-SCENE-RESET-ID": ({"IF-EXECUTE-RECORD"}, {"TR-CAPTURE-INTAKE"}),
    "RC-TRUTH-ISOLATION": ({"IF-OBS-INTERPRET"}, {"TR-TRACEABLE-FINDING"}),
    "RC-CAUSAL-PREFIX": ({"IF-EXECUTE-RECORD"}, {"TR-OBSERVATION-ASSESSMENT"}),
    "RC-DENOMINATOR-ATTEMPTS": ({"IF-RESOURCE-STOP"}, {"TR-TRACEABLE-FINDING"}),
}


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


def _ip_reassembly_status(vector: object) -> str | None:
    if not isinstance(vector, dict):
        return None
    length, ranges, conflict = vector.get("datagramLengthBytes"), vector.get("coverageRanges"), vector.get("overlapConflict")
    fragments = vector.get("fragments")
    if (type(length) is not int or length <= 0 or not isinstance(ranges, list) or not ranges
            or not isinstance(fragments, list) or not fragments
            or type(conflict) is not bool or any(not isinstance(pair, list) or len(pair) != 2
                                                 or any(type(bound) is not int for bound in pair)
                                                 or pair[0] < 0 or pair[0] > pair[1] or pair[1] >= length for pair in ranges)):
        return None
    observed: dict[int, int] = {}
    derived_conflict = False
    offsets: list[int] = []
    for fragment in fragments:
        if (not isinstance(fragment, dict) or set(fragment) != {"offset", "bytesHex"}
                or type(fragment.get("offset")) is not int or fragment["offset"] < 0
                or not isinstance(fragment.get("bytesHex"), str)):
            return None
        try:
            payload = bytes.fromhex(fragment["bytesHex"])
        except ValueError:
            return None
        if not payload or fragment["offset"] + len(payload) > length:
            return None
        offsets.append(fragment["offset"])
        for index, byte in enumerate(payload, fragment["offset"]):
            if index in observed and observed[index] != byte:
                derived_conflict = True
            observed[index] = byte
    if offsets != vector.get("fragmentOffsets") or conflict is not derived_conflict:
        return None
    actual_ranges: list[list[int]] = []
    for index in sorted(observed):
        if not actual_ranges or index > actual_ranges[-1][1] + 1:
            actual_ranges.append([index, index])
        else:
            actual_ranges[-1][1] = index
    if ranges != actual_ranges:
        return None
    if derived_conflict:
        return "CONFLICT"
    merged_end = -1
    for start, end in sorted(ranges):
        if start > merged_end + 1:
            return "GAPPED"
        merged_end = max(merged_end, end)
    return "COMPLETE" if merged_end == length - 1 else "GAPPED"


def _replay_ownership(values: dict) -> tuple[str | None, dict[str, str], dict[str, str]]:
    """One finite event replay supplies both response owners and request states."""
    if (not isinstance(values, dict) or not isinstance(values.get("policy"), str)
            or values["policy"] not in {"FIFO", "MOST-RECENT", "UNIQUE-KEY"}):
        return "untyped ownership policy", {}, {}
    events = values.get("ownershipEvents")
    if (not isinstance(events, list) or not events
            or not all(isinstance(event, dict)
                       and isinstance(event.get("kind"), str)
                       and set(event) == ({"id", "kind", "key", "sequence", "targetRequestId"} if event.get("kind") in {"CANCEL", "SUPERSEDE"} else {"id", "kind", "key", "sequence"})
                       and event.get("kind") in {"REQUEST", "RESPONSE", "CANCEL", "SUPERSEDE"}
                       and isinstance(event.get("id"), str) and bool(event["id"])
                       and isinstance(event.get("key"), str) and bool(event["key"])
                       and isinstance(event.get("sequence"), int) and not isinstance(event["sequence"], bool)
                       and event["sequence"] >= 0
                       and (event["kind"] not in {"CANCEL", "SUPERSEDE"}
                            or (isinstance(event.get("targetRequestId"), str) and bool(event["targetRequestId"])))
                       for event in events)):
        return "untyped ownership event schedule", {}, {}
    requests = {event["id"]: event for event in events if event["kind"] == "REQUEST"}
    if (len({event["sequence"] for event in events}) != len(events)
            or len({event["id"] for event in events}) != len(events)
            or any(event["targetRequestId"] not in requests
                   or requests[event["targetRequestId"]]["sequence"] >= event["sequence"]
                   or requests[event["targetRequestId"]]["key"] != event["key"]
                   for event in events if event["kind"] in {"CANCEL", "SUPERSEDE"})):
        return "invalid ownership event schedule", {}, {}
    policy = values.get("policy")
    active: dict[str, dict] = {}
    states: dict[str, str] = {}
    owners: dict[str, str] = {}
    for event in sorted(events, key=lambda item: item["sequence"]):
        if event["kind"] == "REQUEST":
            active[event["id"]] = event
            states[event["id"]] = "ACTIVE"
        elif event["kind"] in {"CANCEL", "SUPERSEDE"}:
            target = event["targetRequestId"]
            if target in active:
                active.pop(target)
                states[target] = "CANCELLED" if event["kind"] == "CANCEL" else "SUPERSEDED"
        else:
            candidates = sorted((request for request in active.values() if request["key"] == event["key"]),
                                key=lambda request: request["sequence"])
            owner = ("UNMATCHED" if not candidates else
                     "AMBIGUOUS" if policy == "UNIQUE-KEY" and len(candidates) != 1 else
                     candidates[-1]["id"] if policy == "MOST-RECENT" else candidates[0]["id"])
            owners[event["id"]] = owner
            if owner == "AMBIGUOUS":
                for request in candidates:
                    states[request["id"]] = "AMBIGUOUS"
                    active.pop(request["id"])
            elif owner != "UNMATCHED":
                states[owner] = "DISCHARGED"
                active.pop(owner)
    return None, owners, states


def _resolve_ownership(values: dict) -> tuple[str | None, str | None]:
    """Resolve one response from the same replay used by T2 and no-response."""
    if (not isinstance(values, dict) or not isinstance(values.get("key"), str) or not values["key"]
            or not isinstance(values.get("responseId"), str) or not values["responseId"]):
        return "untyped ownership key or response", None
    error, owners, _ = _replay_ownership(values)
    if error:
        return error, None
    response = next((event for event in values["ownershipEvents"] if event["id"] == values["responseId"]
                     and event["kind"] == "RESPONSE"), None)
    if response is None:
        return "response absent from event schedule", None
    return None, owners[response["id"]] if response["key"] == values["key"] else "UNMATCHED"


def _request_lifecycle(values: dict) -> dict[str, str] | None:
    error, _, states = _replay_ownership(values)
    return None if error else states


def _remaining_request_ids(values: dict) -> set[str] | None:
    states = _request_lifecycle(values)
    return {request_id for request_id, state in states.items() if state == "ACTIVE"} if states is not None else None


def _acceptance_relation_errors(case: dict) -> list[str]:
    """Evaluate the closed deterministic relation declared by a specification witness."""
    relation = case.get("relationId", "")
    inputs = case.get("inputFixture", {}).get("values", {})
    outputs = case.get("expectedOutputFixture", {}).get("values", {})
    errors: list[str] = []
    if not isinstance(inputs, dict) or not isinstance(outputs, dict):
        return [f"{relation or 'acceptance relation'} requires object fixture values"]
    if relation == "RC-TRANSFER-TERMINAL":
        terminal = inputs.get("terminal")
        option = inputs.get("optionState")
        accepted = inputs.get("acceptedBlockBytes")
        block_size = 512 if option == "DEFAULTED" else accepted if option == "ACCEPTED" else None
        typed_terminal = (isinstance(terminal, dict) and set(terminal) == {"block", "payloadBytes", "nextZeroBlock", "nextZeroPayloadBytes"}
                          and type(terminal.get("block")) is int and terminal["block"] >= 0
                          and type(terminal.get("payloadBytes")) is int and terminal["payloadBytes"] >= 0
                          and (terminal.get("nextZeroBlock") is None or type(terminal["nextZeroBlock"]) is int)
                          and (terminal.get("nextZeroPayloadBytes") is None or type(terminal["nextZeroPayloadBytes"]) is int)
                          and isinstance(inputs.get("blocks"), list)
                          and all(type(block) is int and block >= 0 for block in inputs["blocks"])
                          and terminal["block"] in inputs["blocks"]
                          and (terminal["nextZeroBlock"] is None and terminal["nextZeroPayloadBytes"] is None
                               or terminal["nextZeroBlock"] is not None and terminal["nextZeroPayloadBytes"] == 0
                               and terminal["nextZeroBlock"] in inputs.get("blocks", []))
                          and isinstance(option, str) and option in {"DEFAULTED", "ACCEPTED", "UNKNOWN"}
                          and (accepted is None if option != "ACCEPTED" else type(accepted) is int and accepted > 0)
                          and (block_size is None or terminal["payloadBytes"] <= block_size))
        derived = (typed_terminal and block_size is not None and terminal["payloadBytes"] <= block_size
                   and (terminal["payloadBytes"] < block_size or terminal["nextZeroBlock"] == terminal["block"] + 1))
        if not typed_terminal or outputs.get("terminalConfirmed") is not bool(derived):
            errors.append("RC-TRANSFER-TERMINAL at inputFixture.values.terminal")
    elif relation == "RC-PREDICTION-NONEMPTY":
        if outputs.get("predictionStatus") == "OK":
            frontiers = inputs.get("frontiers", [])
            states = {item.get("state") for item in frontiers if isinstance(item, dict) and item.get("hypothesisId") in set(inputs.get("H", []))}
            derived = {item.get("observationClass") for item in inputs.get("model", {}).get("transitions", []) if isinstance(item, dict) and item.get("source") in states and item.get("actionId") == inputs.get("actionId") and isinstance(item.get("observationClass"), str)}
            if not derived or set(outputs.get("classes", [])) != derived:
                errors.append("RC-PREDICTION-NONEMPTY at expectedOutputFixture.values.classes")
    elif relation == "RC-SELECT-STABLE-ID":
        actions = inputs.get("actions", [])
        resource = inputs.get("resource", {})
        if (not isinstance(actions, list) or not isinstance(resource, dict)
                or not isinstance(inputs.get("eligibleActions"), list)
                or any(not isinstance(value, str) or not value for value in inputs["eligibleActions"])
                or len(set(inputs["eligibleActions"])) != len(inputs["eligibleActions"])
                or not isinstance(resource.get("mode"), str)
                or resource["mode"] not in {"BUDGET", "ROUNDS"}
                or type(resource.get("remaining")) is not int or resource["remaining"] < 0):
            return ["RC-SELECT-STABLE-ID requires typed actions, eligibleActions, and resource"]
        hypotheses = inputs.get("H")
        classes = inputs.get("distinguishingClasses")
        if (not isinstance(hypotheses, list) or not hypotheses
                or any(not isinstance(h, str) or not h for h in hypotheses)
                or len(set(hypotheses)) != len(hypotheses)
                or not isinstance(classes, list) or len(classes) < 2
                or any(not isinstance(value, str) or not value for value in classes)
                or len(set(classes)) != len(classes)
                or any(not isinstance(a, dict)
                       or not isinstance(a.get("id"), str) or not a["id"]
                       or not isinstance(a.get("kind"), str) or a["kind"] not in {"TEST", "PREP", "RECOVER"}
                       or type(a.get("cost")) is not int or a["cost"] < 0
                       or a["kind"] == "TEST" and a["cost"] == 0
                       or (a["kind"] == "TEST" and (set(a) != {"id", "kind", "cost", "worstClass", "classesByHypothesis"}
                           or not isinstance(a.get("classesByHypothesis"), dict)
                           or set(a["classesByHypothesis"]) != set(hypotheses)
                           or any(not isinstance(value, str) or not value for value in a["classesByHypothesis"].values())
                           or set(a["classesByHypothesis"].values()) != set(classes)
                           or type(a.get("worstClass")) is not int
                           or a["worstClass"] != max(list(a["classesByHypothesis"].values()).count(value) for value in classes)))
                       or (a["kind"] != "TEST" and set(a) != {"id", "kind", "cost"})
                       for a in actions)):
            return ["RC-SELECT-STABLE-ID requires typed distinguishing TEST scores"]
        if len({a["id"] for a in actions}) != len(actions) or not set(inputs["eligibleActions"]).issubset({a["id"] for a in actions}):
            return ["RC-SELECT-STABLE-ID requires unique declared eligible TEST IDs"]
        affordable = [a for a in actions if a["kind"] == "TEST" and a["id"] in inputs["eligibleActions"]
                      and (resource["remaining"] > 0 if resource["mode"] == "ROUNDS" else a["cost"] <= resource["remaining"])]
        expected = min(affordable, key=lambda a: (a["worstClass"], a["cost"], a["id"]))["id"] if affordable else None
        eligible_tests = [a for a in actions if a["kind"] == "TEST" and a["id"] in inputs["eligibleActions"]]
        if len(eligible_tests) < 2 or outputs.get("selectedActionId") != expected:
            errors.append("RC-SELECT-STABLE-ID at expectedOutputFixture.values.selectedActionId")
    elif relation == "RC-VERDICT-WHOLE-INTERVAL":
        interval = inputs.get("interval", {})
        window = inputs.get("requirementWindow", {})
        try:
            for candidate in (interval, window):
                if not isinstance(candidate, dict) or set(candidate) != {"lower", "upper", "lowerClosed", "upperClosed"} or not isinstance(candidate["lower"], (int, float)) or isinstance(candidate["lower"], bool) or not isinstance(candidate["upper"], (int, float)) or isinstance(candidate["upper"], bool) or not isinstance(candidate["lowerClosed"], bool) or not isinstance(candidate["upperClosed"], bool) or candidate["lower"] > candidate["upper"] or candidate["lower"] == candidate["upper"] and not (candidate["lowerClosed"] and candidate["upperClosed"]):
                    raise ValueError("malformed interval")
            if inputs.get("clockValid") is not True:
                expected = "ERROR"
            else:
                within_lower = interval["lower"] > window["lower"] or interval["lower"] == window["lower"] and (not interval["lowerClosed"] or window["lowerClosed"])
                within_upper = interval["upper"] < window["upper"] or interval["upper"] == window["upper"] and (not interval["upperClosed"] or window["upperClosed"])
                disjoint = interval["upper"] < window["lower"] or interval["lower"] > window["upper"] or interval["upper"] == window["lower"] and not (interval["upperClosed"] and window["lowerClosed"]) or interval["lower"] == window["upper"] and not (interval["lowerClosed"] and window["upperClosed"])
                expected = "PASS" if within_lower and within_upper else "FAIL" if disjoint else "INCONCLUSIVE"
        except (KeyError, TypeError, ValueError):
            expected = None
            errors.append("RC-VERDICT-WHOLE-INTERVAL at inputFixture.values.interval: malformed interval")
        if outputs.get("verdict") != expected:
            errors.append("RC-VERDICT-WHOLE-INTERVAL at expectedOutputFixture.values.verdict")
    elif relation == "RC-SUMMARY-CONFIRMATION":
        if outputs.get("commitSummary") and not inputs.get("summaryConfirmed"):
            errors.append("RC-SUMMARY-CONFIRMATION at inputFixture.values.summaryConfirmed")
        elif outputs.get("commitSummary") != inputs.get("postSummary"):
            errors.append("RC-SUMMARY-CONFIRMATION at expectedOutputFixture.values.commitSummary")
    elif relation == "RC-HISTORY-NO-RESURRECTION":
        old = inputs.get("history", {})
        new = outputs.get("history", {})
        compatible_raw = inputs.get("compatibleObservationHypotheses")
        typed_lists = (isinstance(old, dict) and isinstance(new, dict)
                       and all(isinstance(value, list) and all(isinstance(item, str) for item in value)
                               for value in (old.get("H"), new.get("H"), compatible_raw)))
        if (not typed_lists or not isinstance(old.get("version"), int) or isinstance(old.get("version"), bool)
                or not isinstance(new.get("version"), int) or isinstance(new.get("version"), bool)
                or set(new["H"]) != set(old["H"]) & set(compatible_raw) or new["version"] != old["version"] + 1):
            errors.append("RC-HISTORY-NO-RESURRECTION at expectedOutputFixture.values.history.H")
    elif relation == "RC-EQUIV-EVIDENCE":
        if outputs.get("result") == "established" and inputs.get("finiteDomainProof") != "present":
            errors.append("RC-EQUIV-EVIDENCE at expectedOutputFixture.values.result")
    elif relation == "RC-RESOURCE-ONCE":
        if outputs.get("charges") != inputs.get("attemptsIssued"):
            errors.append("RC-RESOURCE-ONCE at expectedOutputFixture.values.charges")
    elif relation == "RC-INTEGRITY-RUNTIME":
        if outputs.get("judgment") != "NOT-EVALUATED" and inputs.get("runtimeEvidence") != "ESTABLISHED":
            errors.append("RC-INTEGRITY-RUNTIME at expectedOutputFixture.values.judgment")
    elif relation == "RC-SCENE-RESET-ID":
        if not inputs.get("resetId"):
            errors.append("RC-SCENE-RESET-ID at inputFixture.values.resetId")
    elif relation == "RC-TRUTH-ISOLATION":
        if inputs.get("algorithmVisible") is not False:
            errors.append("RC-TRUTH-ISOLATION at inputFixture.values.algorithmVisible")
    elif relation == "RC-CAUSAL-PREFIX":
        if any("truth" in str(item).lower() for item in inputs.get("visiblePrefix", [])):
            errors.append("RC-CAUSAL-PREFIX at inputFixture.values.visiblePrefix")
    elif relation == "RC-DENOMINATOR-ATTEMPTS":
        attempts = inputs.get("attempts")
        if not isinstance(attempts, list) or any(not isinstance(item, str) for item in attempts):
            return ["RC-DENOMINATOR-ATTEMPTS requires a string attempt sequence"]
        if outputs.get("attemptDenominator") != len(attempts):
            errors.append("RC-DENOMINATOR-ATTEMPTS at expectedOutputFixture.values.attemptDenominator")
        if outputs.get("answeredDenominator") != sum(item in {"PASS", "FAIL"} for item in attempts):
            errors.append("RC-DENOMINATOR-ATTEMPTS at expectedOutputFixture.values.answeredDenominator")
    return errors


def _apply_acceptance_variant(case: dict, variant: dict) -> dict:
    mutated = copy.deepcopy(case)
    target: object = mutated
    path = variant["path"]
    for part in path[:-1]:
        target = target[part]
    leaf = path[-1]
    if variant["operation"] == "remove":
        del target[leaf]
    else:
        target[leaf] = copy.deepcopy(variant.get("value"))
    return mutated


def package_errors(data: dict) -> list[str]:
    errors: list[str] = []
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        return [f"schema is invalid: {exc.message}"]
    errors.extend(f"schema at {item.json_path}: {item.message}" for item in Draft202012Validator(schema).iter_errors(data))
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
        "CLTAV-INTEGRITY-OBLIGATION-BASELINE": "configs/engineering/cltav_integrity_obligation_baseline.json",
        "CLTAV-HISTORICAL-CAPTURE-MANIFEST": "configs/research/cltav_historical_capture_manifest.json",
    }
    if {key: row["path"] for key, row in bindings.items()} != required_bindings:
        errors.append("inputBindings must exactly bind M1 CRS, CL-TAV registry, integrity baseline, and capture manifest")
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
        capture_manifest = _git_blob_json(required_bindings["CLTAV-HISTORICAL-CAPTURE-MANIFEST"], blobs)
        capture_by_id = {item["captureId"]: item for item in capture_manifest.get("captures", [])}
        if not capture_by_id:
            errors.append("historical capture manifest lacks captures")
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        capture_by_id = {}
        errors.append("historical capture manifest is unreadable")
    try:
        m1 = _git_blob_json(required_bindings["ARINC615A3-M1-CRS"], blobs)
    except (OSError, json.JSONDecodeError):
        return errors + ["bound M1 CRS is unreadable"]
    expected = {row["id"] for row in m1["requirements"]}
    source_by_id = {row["id"]: row for row in m1["requirements"]}
    try:
        integrity_baseline = _git_blob_json(required_bindings["CLTAV-INTEGRITY-OBLIGATION-BASELINE"], blobs)
        integrity_rows = integrity_baseline["obligations"]
        integrity_by_requirement = {row["requirementId"]: row for row in integrity_rows}
        if len(integrity_by_requirement) != len(integrity_rows):
            errors.append("integrity obligation baseline repeats a requirement")
        required_integrity_fields = {"requirementId", "service", "sourceUnitId", "contractId", "subject", "condition", "requiredObservation", "acceptanceCaseId"}
        if any(set(row) != required_integrity_fields or any(not str(value).strip() for value in row.values()) for row in integrity_rows):
            errors.append("integrity obligation baseline has an incomplete obligation contract")
        entities = integrity_baseline.get("symbolicEntities")
        if (not isinstance(entities, list) or not entities
                or any(not isinstance(row, dict) or set(row) != {"id", "kind", "service"}
                       or not all(isinstance(value, str) and value for value in row.values())
                       or row["kind"] not in {"OPTION", "PROTECTED-BYTES", "FILE", "ALGORITHM"}
                       or row["service"] not in {"INFORMATION", "UPLOAD"} for row in entities)
                or len({row["id"] for row in entities if isinstance(row, dict) and isinstance(row.get("id"), str)}) != len(entities)):
            errors.append("integrity symbolic entity catalog is invalid")
            symbolic_entities = {}
        else:
            symbolic_entities = {row["id"]: row for row in entities}
        status_schedule = integrity_baseline.get("syntheticStatusSchedule")
        if (not isinstance(status_schedule, dict)
                or status_schedule.get("contractId") != "INT-POST-DATA-STATUS-CONTINUATION"
                or status_schedule.get("scope") != "FINITE-SPECIFICATION-WITNESS-NOT-PROTOCOL-FREQUENCY"):
            errors.append("integrity finite status schedule is missing or unbounded")
            status_schedule = {}
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        integrity_by_requirement = {}
        symbolic_entities = {}
        status_schedule = {}
        errors.append("bound integrity obligation baseline is unreadable")
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
            example = record["example"]
            if not example.get("H"):
                errors.append("HISTORY-HANDLE initialization example must retain a nonempty H0")
            for label, instance in (("example", record["example"]), ("invalidExample", record["invalidExample"])):
                raw_hypotheses = instance.get("H", [])
                if not all(isinstance(item, str) for item in raw_hypotheses):
                    continue
                hypotheses = set(raw_hypotheses)
                compatible = set(instance.get("compatibleStateByHypothesis", {}))
                statuses = set(instance.get("statusByHypothesis", {}))
                if compatible != hypotheses or (statuses and statuses != hypotheses):
                    errors.append(f"HISTORY-HANDLE {label} maps must exactly cover H")
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
        required_merge = {"hypothesisId", "controlStateId", "clockConstraint", "typedStore", "historyProvenance"}
        if set(finite["mergeKey"]) != required_merge:
            errors.append(f"{refinement['id']} merge key must preserve state, clock, store, and whole-history provenance")
        expected_limits = {"pathLength":"CONSERVATIVE-UNKNOWN", "frontierStates":"CONSERVATIVE-UNKNOWN", "hypotheses":"SPEC-ERROR", "actions":"ADMIT-REFUSED", "observationClasses":"PredictionGapError"}
        if finite["limitBehavior"] != expected_limits:
            errors.append(f"{refinement['id']} finite limit behavior differs from the controlled conservative mapping")
        expected_internal = {"FEASIBLE","INFEASIBLE","COMPUTATION-UNKNOWN","UNSUPPORTED-SYNTAX","LIMIT-REACHED","EMPTY-HISTORY"}
        if set(finite["internalResults"]) != expected_internal:
            errors.append(f"{refinement['id']} finite internal result vocabulary is incomplete")
        expected_mapping = {binding["interfaceId"] for binding in refinement["interfaceBindings"]}
        if set(finite["resultMapping"]) != expected_mapping:
            errors.append(f"{refinement['id']} result mapping differs from its algorithm interfaces")
        for binding in refinement["interfaceBindings"]:
            mapping = finite["resultMapping"].get(binding["interfaceId"], {})
            if mapping.get("success") != binding["outputTypes"] or mapping.get("failure") != binding["failureTags"]:
                errors.append(f"{refinement['id']} result mapping is stale for {binding['interfaceId']}")
        total = finite["totalReturnMapping"]
        total_keys = [(row["interfaceId"], row["internalResult"]) for row in total]
        expected_total = {(binding["interfaceId"], result) for binding in refinement["interfaceBindings"] for result in expected_internal}
        if len(total_keys) != len(set(total_keys)) or set(total_keys) != expected_total:
            errors.append(f"{refinement['id']} total finite-result return mapping is incomplete or duplicated")
        controlled_outputs = {
            "IF-PRED-OBS": {"FEASIBLE":"currentlyValidNonemptyClasses","INFEASIBLE":"PredictionGapError","COMPUTATION-UNKNOWN":"RESOURCE-UNKNOWN","UNSUPPORTED-SYNTAX":"PredictionGapError","LIMIT-REACHED":"RESOURCE-UNKNOWN","EMPTY-HISTORY":"PredictionGapError"},
            "IF-SELECT-ADMIT": {"FEASIBLE":"admitA2A5","INFEASIBLE":"PredictionGapError","COMPUTATION-UNKNOWN":"ADMIT-REFUSED","UNSUPPORTED-SYNTAX":"SPEC-ERROR","LIMIT-REACHED":"ADMIT-REFUSED","EMPTY-HISTORY":"PredictionGapError"},
            "IF-HIST-UPDATE": {"FEASIBLE":"Hprime","INFEASIBLE":"Hprime","COMPUTATION-UNKNOWN":"CONSERVATIVE-UNKNOWN","UNSUPPORTED-SYNTAX":"CONSERVATIVE-UNKNOWN","LIMIT-REACHED":"CONSERVATIVE-UNKNOWN","EMPTY-HISTORY":"Stop-Empty"},
            "IF-EQUIV": {"FEASIBLE":"notEstablished","INFEASIBLE":"notEstablished","COMPUTATION-UNKNOWN":"unknown","UNSUPPORTED-SYNTAX":"unknown","LIMIT-REACHED":"unknown","EMPTY-HISTORY":"notEstablished"},
            "IF-RESOURCE-STOP": {"EMPTY-HISTORY":"stopClass=Stop-Empty"},
        }
        for row in total:
            expected_output = controlled_outputs.get(row["interfaceId"], {}).get(row["internalResult"])
            if row["reachable"] != (expected_output is not None):
                errors.append(f"{refinement['id']} has an incorrect reachable result for {row['interfaceId']}/{row['internalResult']}")
            if expected_output is not None and row.get("output") != expected_output:
                errors.append(f"{refinement['id']} has an unsafe output for {row['interfaceId']}/{row['internalResult']}")
            if expected_output is None and (row.get("output") is not None or row.get("rejectionReason") != "UNREACHABLE-IN-THIS-INTERFACE"):
                errors.append(f"{refinement['id']} must mark {row['interfaceId']}/{row['internalResult']} unreachable")
            expected_history = "EMPTY-PROVEN" if row["interfaceId"] == "IF-HIST-UPDATE" and row["internalResult"] == "EMPTY-HISTORY" else "INTERSECT-PROVEN" if row["interfaceId"] == "IF-HIST-UPDATE" and row["internalResult"] in {"FEASIBLE", "INFEASIBLE"} else "PRESERVE"
            if row["historyEffect"] != expected_history or row["summaryEffect"] != "PRESERVE" or row["chargeEffect"] != "NONE":
                errors.append(f"{refinement['id']} has unsafe side effects for {row['interfaceId']}/{row['internalResult']}")
            contract = row.get("returnContract", {})
            required_contract_fields = {
                "IF-PRED-OBS": {"status","reason","classesByTest","historyVersionUsed","uncertaintyRef"},
                "IF-SELECT-ADMIT": {"kind","actionKind","actionId","classesUsed","reason"},
                "IF-HIST-UPDATE": {"status","compatibleStateByHypothesis","Hprime","HistoryHandlePrime","historyVersion","summaryEffect"},
                "IF-EQUIV": {"status","proofBasis"},
                "IF-RESOURCE-STOP": {"stopClass","finalH","trace"},
            }.get(row["interfaceId"], set()) if row["reachable"] else set()
            if row["interfaceId"] == "IF-PRED-OBS" and row["reachable"] and row["internalResult"] != "FEASIBLE":
                required_contract_fields = required_contract_fields - {"classesByTest"}
            if set(contract.get("requiredFields", [])) != required_contract_fields:
                errors.append(f"{refinement['id']} return contract is incomplete for {row['interfaceId']}/{row['internalResult']}")
            if contract.get("branchTag") != row["internalResult"] or set(contract.get("fieldSources", {})) != required_contract_fields:
                errors.append(f"{refinement['id']} return payload lacks a closed branch/source mapping for {row['interfaceId']}/{row['internalResult']}")
            expected_sources = {field: "KERNEL" for field in required_contract_fields}
            if row["interfaceId"] == "IF-HIST-UPDATE":
                expected_sources["Hprime"] = "BACKEND-ALIAS"
                expected_sources["HistoryHandlePrime"] = "INTERFACE-ADAPTER"
            if contract.get("fieldSources") != expected_sources:
                errors.append(f"{refinement['id']} return payload sources are not controlled for {row['interfaceId']}/{row['internalResult']}")
            expected_record = {"IF-PRED-OBS": "PredictionResult", "IF-SELECT-ADMIT": "Decision", "IF-HIST-UPDATE": "HistoryUpdateResult", "IF-EQUIV": "EquivalenceResult", "IF-RESOURCE-STOP": "StopResult"}.get(row["interfaceId"])
            if row["reachable"] and contract.get("recordType") != expected_record:
                errors.append(f"{refinement['id']} return record type is not the controlled {expected_record} for {row['interfaceId']}/{row['internalResult']}")
            if row["interfaceId"] == "IF-HIST-UPDATE" and row["reachable"] and contract.get("adapter") != "Backend returns eta_c and H_c; IF-HIST-UPDATE exposes their typed aliases; S9 alone constructs GammaPrime and commits a confirmed summary.":
                errors.append(f"{refinement['id']} history backend adapter does not preserve eta_c/H_c through S9")
            if row["interfaceId"] == "IF-PRED-OBS" and row["reachable"]:
                expects_classes = row["internalResult"] == "FEASIBLE"
                if ("classesByTest" in contract.get("requiredFields", [])) != expects_classes:
                    errors.append(f"{refinement['id']} prediction return payload does not distinguish OK from GAP")
            if row["interfaceId"] == "IF-SELECT-ADMIT" and row["reachable"] and "TEST-scoped" not in contract.get("adapter", ""):
                errors.append(f"{refinement['id']} selection adapter loses TEST-scoped GAP semantics")
        flow = finite["historyReturnFlow"]
        backend, interface, s9 = flow.get("backend"), flow.get("interface"), flow.get("s9")
        source_map = {
            "interface.Hprime": "backend.H_c",
            "interface.HistoryHandlePrime.compatibleStateByHypothesis": "backend.eta_c",
            "interface.HistoryHandlePrime.version": "backend.historyVersion",
            "s9.etaPrime": "interface.HistoryHandlePrime",
            "s9.Hprime": "interface.Hprime",
            "s9.GammaPrime.qStatus": "inputGamma.qStatus",
            "s9.GammaPrime.currentSummary": "normalizedOutcome.postSummary when the S9 guard holds; otherwise inputGamma.currentSummary",
            "s9.GammaPrime.otherSessionFields": "inputGamma unchanged; S7/S8 effects are upstream of S9",
        }
        input_gamma, outcome = flow.get("inputGamma"), flow.get("normalizedOutcome")
        session_fields = set(registry["sessionHandles"]["SessionContext"]["fields"])
        gamma_typed = (isinstance(input_gamma, dict) and set(input_gamma) == session_fields
                       and isinstance(input_gamma.get("sessionId"), str) and bool(input_gamma["sessionId"])
                       and all(type(input_gamma.get(field)) is int and input_gamma[field] >= 0 for field in ("resourceRemainder", "retryCount", "retryCap"))
                       and input_gamma["retryCap"] > 0 and input_gamma["retryCount"] <= input_gamma["retryCap"]
                       and isinstance(input_gamma.get("qStatus"), str)
                       and input_gamma["qStatus"] in {"KNOWN", "UNKNOWN"}
                       and isinstance(input_gamma.get("currentSummary"), str)
                       and (input_gamma.get("knownTarget") is None or isinstance(input_gamma.get("knownTarget"), str))
                       and all(isinstance(input_gamma.get(field), list) for field in ("knownEvidence", "errorHistory", "unknownHistory"))
                       and isinstance(outcome, dict) and set(outcome) == {"summaryConfirmed", "postSummary"}
                       and isinstance(outcome.get("summaryConfirmed"), bool)
                       and (outcome.get("postSummary") is None or isinstance(outcome.get("postSummary"), str)))
        should_commit = (gamma_typed and input_gamma["qStatus"] == "KNOWN"
                         and outcome["summaryConfirmed"] and isinstance(outcome["postSummary"], str)
                         and bool(outcome["postSummary"]))
        gamma_expected = dict(input_gamma) if gamma_typed else {}
        if should_commit:
            gamma_expected["currentSummary"] = outcome["postSummary"]
        history_record = next((record for record in data["recordContracts"] if record["id"] == "HISTORY-HANDLE"), None)
        handle = interface.get("HistoryHandlePrime") if isinstance(interface, dict) else None
        gamma = s9.get("GammaPrime") if isinstance(s9, dict) else None
        if (not isinstance(backend, dict) or set(backend) != {"eta_c", "H_c", "historyVersion"}
                or not isinstance(backend.get("eta_c"), dict) or not isinstance(backend.get("H_c"), list)
                or not backend["H_c"] or any(not isinstance(hypothesis, str) for hypothesis in backend["H_c"])
                or len(set(backend["H_c"])) != len(backend["H_c"])
                or set(backend["eta_c"]) != set(backend["H_c"])
                or not all(isinstance(frontier, str) and frontier.startswith("frontier-") for frontier in backend["eta_c"].values())
                or not isinstance(backend.get("historyVersion"), int) or isinstance(backend.get("historyVersion"), bool)
                or not isinstance(interface, dict) or set(interface) != {"status", "Hprime", "HistoryHandlePrime"}
                or not isinstance(interface.get("status"), str) or interface["status"] not in {"KNOWN", "CONSERVATIVE-UNKNOWN"}
                or interface.get("Hprime") != backend["H_c"] or not isinstance(handle, dict)
                or history_record is None or validate_record_instance(history_record, handle)
                or handle.get("compatibleStateByHypothesis") != backend["eta_c"]
                or handle.get("version") != backend["historyVersion"]
                or not isinstance(s9, dict) or set(s9) != {"status", "etaPrime", "Hprime", "GammaPrime", "summaryConfirmed", "summaryCommitted"}
                or s9.get("status") != "OK" or s9.get("etaPrime") != handle
                or s9.get("Hprime") != interface["Hprime"] or not isinstance(gamma, dict)
                or not gamma_typed or set(gamma) != session_fields
                or {field: gamma[field] for field in session_fields} != gamma_expected
                or s9.get("summaryConfirmed") is not outcome["summaryConfirmed"]
                or s9.get("summaryCommitted") is not should_commit
                or flow.get("sourceMap") != source_map):
            errors.append(f"{refinement['id']} history backend/interface/S9 payload flow is invalid")
        branch_rows = flow.get("branchWitnesses")
        required_branches = {"HR-NO-COMMIT", "HR-STOP-EMPTY", "HR-CONSERVATIVE", "HR-VERSION-MISMATCH"}
        if (not isinstance(branch_rows, list) or len(branch_rows) != len(required_branches)
                or any(not isinstance(row, dict) or row.get("id") not in required_branches for row in branch_rows)
                or {row["id"] for row in branch_rows} != required_branches):
            errors.append(f"{refinement['id']} history return branch witnesses are incomplete")
        else:
            for branch in branch_rows:
                branch_id = branch["id"]
                g, z, b, i, result = (branch.get(key) for key in ("inputGamma", "outcome", "backend", "interface", "s9"))
                input_h = branch.get("inputH")
                input_handle = branch.get("inputHistoryHandle")
                affected = branch.get("affectedHypothesisIds")
                versions = (branch.get("snapshotVersion"), branch.get("historyInputVersion"))
                typed = (set(branch) == {"id", "effectKnowledge", "inputGamma", "outcome", "affectedHypothesisIds", "snapshotVersion", "historyInputVersion", "inputH", "inputHistoryHandle", "backend", "interface", "s9"}
                         and isinstance(g, dict) and set(g) == session_fields
                         and all(g.get(field) == input_gamma.get(field) for field in session_fields - {"qStatus", "currentSummary"})
                         and isinstance(g.get("qStatus"), str) and g["qStatus"] in {"KNOWN", "UNKNOWN"}
                         and isinstance(g.get("currentSummary"), str)
                         and isinstance(z, dict) and set(z) == {"summaryConfirmed", "postSummary"}
                         and type(z.get("summaryConfirmed")) is bool
                         and (z.get("postSummary") is None or isinstance(z.get("postSummary"), str))
                         and all(type(version) is int and version >= 0 for version in versions)
                         and isinstance(input_h, list) and all(isinstance(h, str) and h for h in input_h)
                         and len(set(input_h)) == len(input_h)
                         and isinstance(affected, list) and all(isinstance(h, str) and h for h in affected)
                         and len(set(affected)) == len(affected) and set(affected).issubset(input_h)
                         and isinstance(input_handle, dict) and history_record is not None
                         and not validate_record_instance(history_record, input_handle)
                         and input_handle.get("H") == input_h and input_handle.get("version") == versions[1]
                         and ((isinstance(input_handle.get("statusByHypothesis"), dict)
                               and set(input_handle["statusByHypothesis"]) == set(input_h))
                              or (versions[1] == 0 and input_handle.get("statusByHypothesis", {}) == {}))
                         and isinstance(result, dict)
                         and set(result) == ({"status", "reason", "etaPrime", "Hprime", "GammaPrime", "summaryCommitted", "outerDisposition"}
                                             if branch_id == "HR-VERSION-MISMATCH" else
                                             {"status", "etaPrime", "Hprime", "GammaPrime", "summaryCommitted", "outerDisposition"})
                         and isinstance(result.get("GammaPrime"), dict)
                         and set(result["GammaPrime"]) == session_fields
                         and isinstance(result.get("Hprime"), list)
                         and type(result.get("summaryCommitted")) is bool)
                if not typed:
                    errors.append(f"{refinement['id']} {branch_id} has malformed history return payload")
                    continue
                stale = versions[0] != versions[1]
                effect = branch["effectKnowledge"]
                expected_effect = {"HR-NO-COMMIT": "COMPATIBLE", "HR-STOP-EMPTY": "PROVEN-INCOMPATIBLE",
                                   "HR-CONSERVATIVE": "UNKNOWN-EFFECT", "HR-VERSION-MISMATCH": "VERSION-MISMATCH"}[branch_id]
                if effect != expected_effect or stale is not (effect == "VERSION-MISMATCH"):
                    errors.append(f"{refinement['id']} {branch_id} effect evidence and version premise disagree")
                if (effect == "UNKNOWN-EFFECT") is not bool(affected):
                    errors.append(f"{refinement['id']} {branch_id} affected history members do not match effect knowledge")
                commit = (not stale and g["qStatus"] == "KNOWN" and z["summaryConfirmed"]
                          and isinstance(z["postSummary"], str) and bool(z["postSummary"]))
                expected_summary = z["postSummary"] if commit else g["currentSummary"]
                expected_gamma = dict(g)
                expected_gamma["currentSummary"] = expected_summary
                if (result["GammaPrime"] != expected_gamma
                        or result["summaryCommitted"] is not commit):
                    errors.append(f"{refinement['id']} {branch_id} violates S9 summary commit guard")
                if stale:
                    if (b is not None or i is not None or result["status"] != "SPEC-ERROR"
                            or result.get("reason") != "history version mismatch"
                            or result["etaPrime"] != input_handle
                            or result["Hprime"] != input_h or result["outerDisposition"] != "Stop-Error"):
                        errors.append(f"{refinement['id']} {branch_id} version mismatch did not preserve input history")
                    continue
                if (branch_id == "HR-NO-COMMIT" and z["summaryConfirmed"]
                        or effect == "PROVEN-INCOMPATIBLE" and (g["qStatus"] != "KNOWN" or not input_h)
                        or effect == "UNKNOWN-EFFECT" and (z["summaryConfirmed"]
                            or isinstance(b, dict) and b.get("H_c") != input_h)):
                    errors.append(f"{refinement['id']} {branch_id} input/effect does not witness its history branch")
                handle = i.get("HistoryHandlePrime") if isinstance(i, dict) else None
                input_status = input_handle.get("statusByHypothesis", {})
                valid_members = (isinstance(b, dict) and isinstance(b.get("H_c"), list)
                                 and all(isinstance(h, str) and h in input_h for h in b["H_c"]))
                expected_member_status = None
                if valid_members:
                    # S0 may leave member status unset. A processed return must
                    # establish every surviving member's status; only a proved
                    # compatible effect can establish KNOWN without an old value.
                    expected_member_status = {h: input_status.get(h, "KNOWN") for h in b["H_c"]}
                    if effect == "UNKNOWN-EFFECT":
                        for h in affected:
                            if h in expected_member_status:
                                expected_member_status[h] = "CONSERVATIVE-UNKNOWN"
                        if any(h not in input_status and h not in affected for h in b["H_c"]):
                            expected_member_status = None
                if (not isinstance(b, dict) or set(b) != {"eta_c", "H_c", "historyVersion"}
                        or not isinstance(b.get("H_c"), list)
                        or any(not isinstance(h, str) or not h for h in b["H_c"])
                        or len(set(b["H_c"])) != len(b["H_c"])
                        or not set(b["H_c"]).issubset(input_h) or not isinstance(b.get("eta_c"), dict)
                        or effect == "UNKNOWN-EFFECT" and b["H_c"] != input_h
                        or effect == "PROVEN-INCOMPATIBLE" and b["H_c"] != []
                        or set(b["eta_c"]) != set(b["H_c"]) or b.get("historyVersion") != versions[1] + 1
                        or not isinstance(i, dict) or set(i) != {"status", "Hprime", "HistoryHandlePrime"}
                        or i.get("Hprime") != b["H_c"] or not isinstance(handle, dict)
                        or history_record is None or validate_record_instance(history_record, handle)
                        or handle.get("compatibleStateByHypothesis") != b["eta_c"]
                        or expected_member_status is None
                        or handle.get("statusByHypothesis") != expected_member_status
                        or handle.get("version") != b["historyVersion"]
                        or result["etaPrime"] != handle or result["Hprime"] != i["Hprime"] or result["status"] != "OK"
                        or result["outerDisposition"] != ("Stop-Empty" if not b["H_c"] else "CONTINUE")
                        or i.get("status") != ("Stop-Empty" if effect == "PROVEN-INCOMPATIBLE" else "CONSERVATIVE-UNKNOWN" if effect == "UNKNOWN-EFFECT" else "KNOWN")):
                    errors.append(f"{refinement['id']} {branch_id} backend/interface/S9 branch mapping is invalid")
        model_schema = finite["modelInstanceSchema"]
        clock_contract = model_schema.get("clockConstraint", {})
        if (not isinstance(clock_contract, dict)
                or clock_contract.get("finiteWitnessProjection") != "one declared clock ID plus its rational interval; W1/W2 have exact one-clock semantics"
                or clock_contract.get("unsupportedProjection") != "multi-clock or cross-clock relation without a named DBM projection is SPEC-ERROR, never a computed successor"):
            errors.append(f"{refinement['id']} finite clock projection boundary is not explicit")
        if set(model_schema.get("guardAst", {}).get("supported", [])) != {"TRUE", "AND", "STATE-EQUALS", "RATIONAL-INTERVAL-CONTAINS", "TYPED-FIELD-EQUALS"} or set(model_schema.get("guardAst", {}).get("unsupported", [])) != {"OR", "NOT", "CALL"}:
            errors.append(f"{refinement['id']} finite guard AST support boundary is ambiguous")
        def rational(value: object) -> Fraction | None:
            if not isinstance(value, dict) or set(value) != {"numerator", "positiveDenominator"}:
                return None
            n, q = value.get("numerator"), value.get("positiveDenominator")
            if not isinstance(n, int) or isinstance(n, bool) or not isinstance(q, int) or isinstance(q, bool) or q <= 0:
                return None
            return Fraction(n, q)
        def valid_interval(value: object) -> bool:
            if not isinstance(value, dict) or set(value) != {"lower","upper","lowerClosed","upperClosed"}:
                return False
            lo, hi = rational(value["lower"]), rational(value["upper"])
            return (isinstance(value["lowerClosed"], bool) and isinstance(value["upperClosed"], bool)
                    and lo is not None and hi is not None and lo <= hi
                    and (lo != hi or value["lowerClosed"] and value["upperClosed"]))
        def intersection(left: dict, right: dict) -> dict | None:
            left_lower, left_upper = rational(left["lower"]), rational(left["upper"])
            right_lower, right_upper = rational(right["lower"]), rational(right["upper"])
            assert left_lower is not None and left_upper is not None and right_lower is not None and right_upper is not None
            lower, upper = max(left_lower, right_lower), min(left_upper, right_upper)
            if lower > upper:
                return None
            # An endpoint that lies strictly inside an input interval is included by
            # that interval.  Only an input which contributes the endpoint may open
            # it.  Do not borrow the opposite endpoint's closure flag here.
            lower_closed = (left["lowerClosed"] if left_lower == lower else True) and (right["lowerClosed"] if right_lower == lower else True)
            upper_closed = (left["upperClosed"] if left_upper == upper else True) and (right["upperClosed"] if right_upper == upper else True)
            if lower == upper and not (lower_closed and upper_closed):
                return None
            def fraction_object(value: Fraction) -> dict[str, int]:
                return {"numerator": value.numerator, "positiveDenominator": value.denominator}
            return {"lower": fraction_object(lower), "upper": fraction_object(upper), "lowerClosed": lower_closed, "upperClosed": upper_closed}
        def advanced(interval: dict, delta: Fraction) -> dict:
            def fraction_object(value: Fraction) -> dict[str, int]:
                return {"numerator": value.numerator, "positiveDenominator": value.denominator}
            return {"lower": fraction_object(rational(interval["lower"]) + delta), "upper": fraction_object(rational(interval["upper"]) + delta), "lowerClosed": interval["lowerClosed"], "upperClosed": interval["upperClosed"]}
        def declared_ids(value: object) -> set[str] | None:
            if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item for item in value):
                return None
            result = set(value)
            return result if len(result) == len(value) else None
        declared_states = declared_ids(model_schema.get("stateIds"))
        declared_clocks = declared_ids(model_schema.get("clockIds"))
        declared_variables = model_schema.get("typedVariables", {})
        def finite_scalar(member: object) -> bool:
            return (isinstance(member, (str, int, bool))
                    or isinstance(member, float) and member == member and member not in (float("inf"), float("-inf")))
        declarations_valid = (
            declared_states is not None and declared_clocks is not None
            and isinstance(declared_variables, dict)
            and bool(declared_variables)
            and all(isinstance(field, str) and field and isinstance(domain, list) and domain
                    and all(finite_scalar(member) for member in domain)
                    and len({(type(member).__name__, member) for member in domain}) == len(domain)
                    for field, domain in declared_variables.items())
        )
        if not declarations_valid:
            errors.append(f"{refinement['id']} model instance lacks finite state/clock/variable declarations")
            declared_states = declared_states or set()
            declared_clocks = declared_clocks or set()
            declared_variables = declared_variables if isinstance(declared_variables, dict) else {}
        def guard_errors(ast: object) -> list[str]:
            if not isinstance(ast, dict) or not isinstance(ast.get("tag"), str):
                return ["guard is not a typed AST"]
            tag = ast["tag"]
            if tag in {"OR", "NOT", "CALL"}:
                return [f"unsupported guard tag {tag}"]
            if tag == "TRUE":
                return [] if set(ast) == {"tag"} else ["TRUE has unexpected operands"]
            if tag == "AND":
                children = ast.get("children")
                if set(ast) != {"tag", "children"} or not isinstance(children, list) or not children:
                    return ["AND lacks children"]
                return [error for child in children for error in guard_errors(child)]
            if tag == "STATE-EQUALS":
                return [] if set(ast) == {"tag", "state"} and isinstance(ast.get("state"), str) and ast["state"] in declared_states else ["STATE-EQUALS lacks a declared state"]
            if tag == "RATIONAL-INTERVAL-CONTAINS":
                return [] if set(ast) == {"tag", "clock", "interval"} and isinstance(ast.get("clock"), str) and ast["clock"] in declared_clocks and valid_interval(ast.get("interval")) else ["RATIONAL-INTERVAL-CONTAINS is malformed"]
            if tag == "TYPED-FIELD-EQUALS":
                domain = declared_variables.get(ast.get("field")) if isinstance(ast.get("field"), str) else None
                return [] if set(ast) == {"tag", "field", "value"} and isinstance(domain, list) and any(type(ast.get("value")) is type(member) and ast.get("value") == member for member in domain) else ["TYPED-FIELD-EQUALS is malformed"]
            return [f"unknown guard tag {tag}"]
        def guard_constraint(ast: dict, current: dict, state: object, store: object) -> dict | None:
            tag = ast["tag"]
            if tag == "TRUE":
                return current
            if tag == "STATE-EQUALS":
                return current if state == ast["state"] else None
            if tag == "RATIONAL-INTERVAL-CONTAINS":
                return intersection(current, ast["interval"])
            if tag == "TYPED-FIELD-EQUALS":
                return current if isinstance(store, dict) and type(store.get(ast["field"])) is type(ast["value"]) and store.get(ast["field"]) == ast["value"] else None
            if tag == "AND":
                result = current
                for child in ast["children"]:
                    result = guard_constraint(child, result, state, store) if result is not None else None
                return result
            return None
        def guard_interval(ast: dict) -> dict | None:
            if ast.get("tag") == "RATIONAL-INTERVAL-CONTAINS":
                return ast["interval"]
            if ast.get("tag") == "TRUE":
                return None
            if ast.get("tag") == "AND":
                result: dict | None = None
                for child in ast["children"]:
                    child_interval = guard_interval(child)
                    if child_interval is not None:
                        result = child_interval if result is None else intersection(result, child_interval)
                return result
            return None
        def update_errors(updates: object) -> list[str]:
            if not isinstance(updates, list):
                return ["simultaneousUpdates is not a list"]
            targets: set[tuple[str, str]] = set()
            results: list[str] = []
            for update in updates:
                if not isinstance(update, dict):
                    results.append("update is not an object"); continue
                tag = update.get("tag")
                if tag == "CLOCK-RESET-TO-ZERO" and set(update) == {"tag", "clock"} and isinstance(update.get("clock"), str) and update["clock"] in declared_clocks:
                    target = ("clock", update["clock"])
                elif tag == "TYPED-FIELD-ASSIGN" and set(update) == {"tag", "field", "value"} and isinstance(update.get("field"), str) and update["field"] in declared_variables and any(type(update.get("value")) is type(member) and update.get("value") == member for member in declared_variables[update["field"]]):
                    target = ("field", update["field"])
                elif tag == "STATE-ASSIGN" and set(update) == {"tag", "state"} and isinstance(update.get("state"), str) and update["state"] in declared_states:
                    target = ("state", "control")
                else:
                    results.append(f"unsupported or malformed update {tag}"); continue
                if target in targets:
                    results.append(f"conflicting simultaneous update {target[0]}:{target[1]}")
                targets.add(target)
            return results
        witness_ids = [row["id"] for row in finite["witnessVectors"]]
        if (len(witness_ids) != 5 or set(witness_ids) !=
                {"FK-W1-FEASIBLE", "FK-W2-INFEASIBLE", "FK-W3-UNKNOWN", "FK-W4-HISTORY", "FK-W5-CLOCK"}):
            errors.append(f"{refinement['id']} finite-kernel witness set is incomplete")
            continue
        for witness_id in ("FK-W1-FEASIBLE", "FK-W2-INFEASIBLE"):
            witness = next(row for row in finite["witnessVectors"] if row["id"] == witness_id)
            witness_input = witness.get("input")
            required_input = {"state", "projectionClock", "typedStore", "clockConstraint", "guard", "observation", "transition", "quantifier", "delta"}
            if not isinstance(witness_input, dict) or set(witness_input) != required_input:
                errors.append(f"{refinement['id']} {witness_id} input has missing, extra, or untyped fields")
                continue
            if not isinstance(witness_input.get("state"), str) or witness_input["state"] not in declared_states:
                errors.append(f"{refinement['id']} {witness_id} input.state is outside the declared model")
                continue
            if not valid_interval(witness["input"].get("clockConstraint")) or not valid_interval(witness["input"].get("guard")):
                errors.append(f"{refinement['id']} {witness_id} has a noncanonical or reversed interval")
            transition = witness["input"].get("transition", {})
            if (not isinstance(transition, dict) or set(transition) != {"id", "source", "target", "guardAst", "simultaneousUpdates"}
                    or not isinstance(transition.get("id"), str) or not transition["id"]
                    or transition.get("source") != witness["input"].get("state")
                    or not isinstance(transition.get("target"), str) or not transition["target"]):
                errors.append(f"{refinement['id']} {witness_id} transition endpoints are malformed")
                continue
            guard_ast = transition.get("guardAst")
            updates = transition.get("simultaneousUpdates")
            if guard_errors(guard_ast) or update_errors(updates):
                errors.append(f"{refinement['id']} {witness_id} input.transition.guardAst or simultaneousUpdates has an unsupported guard or update")
                # A malformed negative witness is a validation result, never an
                # excuse to execute below with missing AST/update members.
                continue
            actual_guard = guard_interval(guard_ast)
            # `guard` is a compatibility projection: TRUE and state/store guards do
            # not have an interval projection.  When the AST has one, it must agree.
            if actual_guard is not None and (not valid_interval(actual_guard) or actual_guard != witness["input"].get("guard")):
                errors.append(f"{refinement['id']} {witness_id} transition guard differs from the authoritative guard")
            delta = rational(witness["input"].get("delta"))
            if delta is None or delta < 0 or witness["input"].get("quantifier") != "EXISTS-DELTA":
                errors.append(f"{refinement['id']} {witness_id} has an invalid time-advance witness")
            elif valid_interval(witness["input"].get("clockConstraint")):
                if not isinstance(witness["input"].get("state"), str) or witness["input"]["state"] not in declared_states:
                    errors.append(f"{refinement['id']} {witness_id} input.state is outside the declared model")
                    continue
                if not isinstance(transition.get("target"), str) or transition["target"] not in declared_states:
                    errors.append(f"{refinement['id']} {witness_id} input.transition.target is outside the declared model")
                    continue
                store = witness["input"].get("typedStore")
                if (not isinstance(store, dict) or set(store) != set(declared_variables)
                    or any(not any(type(store[field]) is type(member) and store[field] == member for member in domain)
                           for field, domain in declared_variables.items())):
                    errors.append(f"{refinement['id']} {witness_id} input.typedStore is outside the declared model")
                    continue
                expected_payload = witness.get("expected", {})
                expected_keys = ({"result", "state", "typedStore", "clockConstraint"}
                                 if witness_id == "FK-W1-FEASIBLE" else {"result", "successorCount"})
                if not isinstance(expected_payload, dict) or set(expected_payload) != expected_keys:
                    errors.append(f"{refinement['id']} {witness_id} expected successor branch has invalid fields")
                    continue
                if witness_id == "FK-W2-INFEASIBLE" and (type(expected_payload["successorCount"]) is not int
                                                        or expected_payload["successorCount"] != 0):
                    errors.append(f"{refinement['id']} {witness_id} INFEASIBLE must have zero successors")
                if "state" in expected_payload:
                    computed_state = expected_payload["state"]
                    if not isinstance(computed_state, str) or computed_state not in declared_states:
                        errors.append(f"{refinement['id']} {witness_id} expected.state is outside the declared model")
                        continue
                if "typedStore" in expected_payload:
                    expected_store_payload = expected_payload["typedStore"]
                    if (not isinstance(expected_store_payload, dict) or set(expected_store_payload) != set(declared_variables)
                            or any(not any(type(expected_store_payload[field]) is type(member) and expected_store_payload[field] == member for member in domain)
                                   for field, domain in declared_variables.items())):
                        errors.append(f"{refinement['id']} {witness_id} expected.typedStore is outside the declared model")
                        continue
                if len(declared_clocks) != 1 or next(iter(declared_clocks)) != witness["input"].get("projectionClock"):
                    errors.append(f"{refinement['id']} {witness_id} anonymous interval requires an explicit single-clock projection")
                    continue
                successor = guard_constraint(guard_ast, advanced(witness["input"]["clockConstraint"], delta), witness["input"].get("state"), witness["input"].get("typedStore", {}))
                computed = "FEASIBLE" if successor is not None else "INFEASIBLE"
                if witness.get("expected", {}).get("result") != computed:
                    errors.append(f"{refinement['id']} {witness_id} result does not follow its clock/guard constraint")
                reset = any(update.get("tag") == "CLOCK-RESET-TO-ZERO" and update.get("clock") == witness["input"]["projectionClock"] for update in updates)
                if reset and successor is not None:
                    successor = {"lower": {"numerator": 0, "positiveDenominator": 1}, "upper": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": True, "upperClosed": True}
                expected_store = dict(witness["input"].get("typedStore", {}))
                for update in updates:
                    if update.get("tag") == "TYPED-FIELD-ASSIGN":
                        expected_store[update["field"]] = update["value"]
                state_updates = [update["state"] for update in updates if update.get("tag") == "STATE-ASSIGN"]
                expected_state = state_updates[0] if state_updates else transition.get("target")
                if state_updates and expected_state != transition.get("target"):
                    errors.append(f"{refinement['id']} {witness_id} state update conflicts with transition target")
                if computed == "FEASIBLE" and (witness["expected"].get("state") != expected_state or witness["expected"].get("clockConstraint") != successor or witness["expected"].get("typedStore") != expected_store):
                    errors.append(f"{refinement['id']} {witness_id} successor does not follow its transition/time advance")
        w3 = next(row for row in finite["witnessVectors"] if row["id"] == "FK-W3-UNKNOWN")
        w3_transition = w3.get("input", {}).get("transition")
        w3_guard = w3_transition.get("guardAst") if isinstance(w3_transition, dict) else None
        if (not isinstance(w3_transition, dict)
                or set(w3_transition) != {"id", "source", "target", "guardAst", "simultaneousUpdates"}
                or not isinstance(w3_transition.get("id"), str) or not w3_transition["id"]
                or not isinstance(w3_guard, dict) or w3_guard.get("tag") != "CALL"
                or not guard_errors(w3_guard) or w3.get("expected", {}).get("result") != "UNSUPPORTED-SYNTAX"):
            errors.append(f"{refinement['id']} unsupported syntax witness is not a typed unsupported guard")
        clock_witness = next(row for row in finite["witnessVectors"] if row["id"] == "FK-W5-CLOCK")
        clock_constraints = clock_witness.get("input", {}).get("clockConstraints", [])
        if (clock_witness.get("expected", {}).get("merge") is not False
                or not isinstance(clock_witness.get("input", {}).get("clockId"), str)
                or clock_witness["input"]["clockId"] not in declared_clocks
                or not isinstance(clock_constraints, list) or len(clock_constraints) != 2
                or not all(valid_interval(value) for value in clock_constraints)
                or clock_constraints[0] == clock_constraints[1]):
            errors.append(f"{refinement['id']} clock-correlation witness must remain separate")
        witness_ids = {row["id"] for row in finite["witnessVectors"]}
        if witness_ids != {"FK-W1-FEASIBLE","FK-W2-INFEASIBLE","FK-W3-UNKNOWN","FK-W4-HISTORY","FK-W5-CLOCK"}:
            errors.append(f"{refinement['id']} finite-kernel witness set is incomplete")
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
        for case_id in binding["acceptanceCaseIds"]:
            case = case_by_id.get(case_id)
            if case is not None and binding["interfaceId"] not in case.get("experimentInterfaceIds", []):
                errors.append(f"{binding['interfaceId']} acceptance case {case_id} omits that experiment interface")
    for parameter in data["runtimeParameterContracts"]:
        if not set(parameter["acceptanceCaseIds"]).issubset(cases):
            errors.append(f"{parameter['id']} has an unknown acceptance case")
        for field in ("title", "titleZh", "unit", "configurationRequirement", "configurationRequirementZh", "exhaustionBehavior", "exhaustionBehaviorZh", "ownerScope", "ownerScopeZh"):
            if not parameter[field].strip():
                errors.append(f"{parameter['id']} has blank {field}")
    for case in data["acceptanceCases"]:
        relation_contract = RELATION_CONTRACT_BINDINGS.get(case.get("relationId"))
        if relation_contract is None:
            errors.append(f"{case['id']} has an unknown deterministic relation")
        else:
            required_interfaces, required_tools = relation_contract
            if set(case["algorithmInterfaceIds"]) != required_interfaces or set(case["toolRequirementIds"]) != required_tools:
                errors.append(f"{case['id']} relationId is incompatible with its typed consumer contract")
        if not set(case["inputRecordIds"]).issubset(records):
            errors.append(f"{case['id']} has an unknown input record")
        if not set(case["toolRequirementIds"]).issubset(tool_by_id):
            errors.append(f"{case['id']} has an unknown tool requirement")
        if not set(case["moduleIds"]).issubset(modules):
            errors.append(f"{case['id']} has an unknown module")
        if not set(case["algorithmInterfaceIds"]).issubset(interface_ids):
            errors.append(f"{case['id']} has an unknown algorithm interface")
        if not set(case.get("experimentInterfaceIds", [])).issubset(experiment_registry):
            errors.append(f"{case['id']} has an unknown experiment interface")
        for field in ("title", "titleZh", "expectedContractOutput", "expectedContractOutputZh", "prohibitedOutput", "prohibitedOutputZh", "basis", "basisZh"):
            if not case[field].strip():
                errors.append(f"{case['id']} has blank {field}")
        if case["inputFixture"].get("recordIds") != case["inputRecordIds"]:
            errors.append(f"{case['id']} fixture record identities differ from the case inputs")
        if case["inputFixture"].get("caseId") != case["id"]:
            errors.append(f"{case['id']} fixture case identity differs from the controlled case")
        if case["expectedOutputFixture"].get("statement") != case["expectedContractOutput"]:
            errors.append(f"{case['id']} expected fixture differs from the controlled expected output")
        if not case["prohibitedOutputPaths"] or not case["negativeVariants"]:
            errors.append(f"{case['id']} lacks concrete prohibited outputs or negative variants")
        if case["inputFixture"].get("values") in (None, {}, []) or case["expectedOutputFixture"].get("values") in (None, {}, []):
            errors.append(f"{case['id']} lacks concrete typed input or expected output values")
        for variant in case["negativeVariants"]:
            if variant["mutation"] in {"violate the named precondition", "remove required identity or precondition", "NO-MUTATION"} or variant["expectedRejection"] == "ACCEPT":
                errors.append(f"{case['id']} has a non-executable negative variant")
                continue
            try:
                variant_errors = _acceptance_relation_errors(_apply_acceptance_variant(case, variant))
            except (KeyError, IndexError, TypeError):
                errors.append(f"{case['id']} negative variant {variant['id']} has an invalid executable path")
                continue
            if variant["expectedRejection"] not in variant_errors:
                errors.append(f"{case['id']} negative variant {variant['id']} does not hit its named relation")
        for tool_id in case["toolRequirementIds"]:
            tool = tool_by_id.get(tool_id)
            if tool is not None and tool["ownerModuleId"] not in case["moduleIds"]:
                errors.append(f"{case['id']} tool {tool_id} omits owner module {tool['ownerModuleId']}")
        errors.extend(_acceptance_relation_errors(case))
    case_values = {case["id"]: case["inputFixture"]["values"] for case in data["acceptanceCases"]}
    prediction = case_values.get("AC-SYN-PREDICTION", {})
    if not prediction.get("model", {}).get("transitions") or not prediction.get("H") or not prediction.get("eligibleActions") or not prediction.get("resource"):
        errors.append("AC-SYN-PREDICTION lacks model, H, eligibility, or resource inputs")
    selection = case_values.get("AC-SYN-SELECT", {})
    if not selection.get("H") or not selection.get("eligibleActions") or not selection.get("distinguishingClasses") or not selection.get("resource"):
        errors.append("AC-SYN-SELECT lacks H, eligibility, distinguishing classes, or resource inputs")
    stop_case = next((case for case in data["acceptanceCases"] if case["id"] == "AC-SYN-RESOURCE-STOP"), None)
    if stop_case is not None:
        values = stop_case["inputFixture"]["values"]
        expected_values = stop_case["expectedOutputFixture"]["values"]
        if expected_values.get("stop") == "Stop-Error" and not (values.get("lastOutcome") == "ADAPTER-ERROR" and values.get("consecutiveErrorCount") == values.get("retryCap")):
            errors.append("AC-SYN-RESOURCE-STOP expects Stop-Error without an exhausted error premise")
        if expected_values.get("charges") != values.get("attemptsIssued"):
            errors.append("AC-SYN-RESOURCE-STOP charges must equal issued attempts exactly once")
    scene_case = case_values.get("AC-EXP-SCENE", {})
    if not {"sceneId","configurationId","iutId","resetId","resourceMode","faultPlan","armId","sessionContext"}.issubset(scene_case):
        errors.append("AC-EXP-SCENE lacks a runnable scene or run-interface input")
    causal = case_values.get("AC-EXP-CAUSAL", {})
    if causal.get("arm") not in {"CL-T", "CL-A", "CL-TA", "CL-LOOP"}:
        errors.append("AC-EXP-CAUSAL uses an uncontrolled experiment arm")
    if any("truth" in str(item).lower() for item in causal.get("visiblePrefix", [])):
        errors.append("AC-EXP-CAUSAL exposes evaluator truth")
    observation_case = next((case for case in data["acceptanceCases"] if case["id"] == "AC-SYN-OBSERVATION"), None)
    if observation_case and _acceptance_relation_errors(observation_case):
        errors.append("AC-SYN-OBSERVATION verdict differs from the controlled whole-interval relation")
    history_case = next((case for case in data["acceptanceCases"] if case["id"] == "AC-SYN-HISTORY"), None)
    if history_case:
        old = history_case["inputFixture"].get("values", {}).get("history")
        compatible_raw = history_case["inputFixture"].get("values", {}).get("compatibleObservationHypotheses")
        new = history_case["expectedOutputFixture"].get("values", {}).get("history")
        if (not isinstance(old, dict) or not isinstance(new, dict)
                or any(not isinstance(value, list) or any(not isinstance(item, str) for item in value)
                       for value in (old.get("H"), new.get("H"), compatible_raw))
                or not isinstance(old.get("version"), int) or isinstance(old.get("version"), bool)
                or not isinstance(new.get("version"), int) or isinstance(new.get("version"), bool)):
            errors.append("AC-SYN-HISTORY lacks a typed history fixture")
        elif set(new["H"]) != set(old["H"]) & set(compatible_raw) or new["version"] != old["version"] + 1:
            errors.append("AC-SYN-HISTORY violates intersection, no-resurrection, or version advancement")
    prep_case = next((case for case in data["acceptanceCases"] if case["id"] == "AC-SYN-PREP-RECOVER"), None)
    if prep_case:
        pv = prep_case["inputFixture"]["values"]; po = prep_case["expectedOutputFixture"]["values"]
        if po.get("commitSummary") and not pv.get("summaryConfirmed"):
            errors.append("AC-SYN-PREP-RECOVER commits an unconfirmed summary")
    truth_case = case_values.get("AC-EXP-TRUTH", {})
    if truth_case.get("algorithmVisible") is not False:
        errors.append("AC-EXP-TRUTH leaks evaluator truth to the algorithm")
    if selection.get("expectedOutputFixture"):
        pass
    select_case = next((case for case in data["acceptanceCases"] if case["id"] == "AC-SYN-SELECT"), None)
    if select_case:
        if _acceptance_relation_errors(select_case):
            errors.append("AC-SYN-SELECT does not exercise the controlled affordable stable-ID tie")
    required_matrix_categories = {"corpus identity", "label boundary", "capture format", "IP reassembly", "TFTP reconstruction", "field contracts", "matching and no response", "timing and U", "prediction and admission", "history update", "state and return", "resource accounting", "experiment boundary", "controlled drift"}
    matrix_ids = [item["id"] for item in data["acceptanceMatrix"]]
    if len(matrix_ids) != len(set(matrix_ids)) or {item["category"] for item in data["acceptanceMatrix"]} != required_matrix_categories:
        errors.append("acceptanceMatrix must cover each controlled category exactly once")
    if any(not item[field].strip() for item in data["acceptanceMatrix"] for field in ("category", "categoryZh", "positiveInput", "positiveInputZh", "expectedOutput", "expectedOutputZh", "negativeMutation", "negativeMutationZh", "expectedRejection", "expectedRejectionZh")):
        errors.append("acceptanceMatrix contains a blank executable specification")
    for item in data["acceptanceMatrix"]:
        if (not item["caseIds"] and item["category"] != "controlled drift") or not set(item["caseIds"]).issubset(case_by_id):
            errors.append(f"{item['id']} has an unknown or empty acceptance-vector reference")
        required_axes = {
            "corpus identity":{"captureId","relativePath","byteCount","sha256","resolvedFileIdentity"}, "IP reassembly":{"fragmentOffsets","fragments","coverageRanges","datagramLengthBytes","overlapConflict","overlapPolicy","gapPolicy"},
            "TFTP reconstruction":{"tidPair","blockNumbers","terminalBlock","optionState"}, "timing and U":{"measurementInterval","requirementWindow","clockValidity","boundaryClosure"},
            "history update":{"H","compatibleObservationHypotheses","historyVersion","summaryConfirmed"}, "controlled drift":{"sourceMutation","viewMarker","publicationMode","failurePreservesOldView"},
        }.get(item["category"])
        if required_axes and set(item.get("coverageAxes", [])) != required_axes:
            errors.append(f"{item['id']} lacks category-specific coverage axes")
        if set(item.get("coverageValues", {})) != set(item.get("coverageAxes", [])):
            errors.append(f"{item['id']} coverage axes lack concrete values")
        def has_missing(value: object) -> bool:
            if value is None:
                return True
            if isinstance(value, dict):
                return any(has_missing(child) for child in value.values())
            if isinstance(value, list):
                return any(has_missing(child) for child in value)
            return False
        if has_missing(item.get("coverageValues", {})):
            errors.append(f"{item['id']} coverage axes contain an unconsumable null value")
        expected_case = {
            "corpus identity": "AC-SYN-TRANSFER", "label boundary": "AC-SYN-TRANSFER", "capture format": "AC-SYN-TRANSFER",
            "IP reassembly": "AC-SYN-TRANSFER", "TFTP reconstruction": "AC-SYN-TRANSFER", "field contracts": "AC-SYN-TRANSFER",
            "matching and no response": "AC-SYN-OBSERVATION", "timing and U": "AC-SYN-OBSERVATION", "prediction and admission": "AC-SYN-SELECT",
            "history update": "AC-SYN-HISTORY", "state and return": "AC-SYN-HISTORY", "resource accounting": "AC-SYN-RESOURCE-STOP",
            "experiment boundary": "AC-EXP-SCENE", "controlled drift": None,
        }[item["category"]]
        if expected_case is not None and expected_case not in item["caseIds"]:
            errors.append(f"{item['id']} is not bound to its controlled acceptance consumer")
        consumer = case_by_id.get(expected_case)
        consumer_input = consumer.get("inputFixture", {}).get("values", {}) if consumer else {}
        consumer_output = consumer.get("expectedOutputFixture", {}).get("values", {}) if consumer else {}
        if item["category"] == "state and return" and item["coverageValues"] != {"internalResult": "EMPTY-HISTORY", "interfaceId": "IF-RESOURCE-STOP", "returnRecord": "StopResult", "sideEffects": "PRESERVE"}:
            errors.append(f"{item['id']} has an unbound state/return coverage vector")
        if item["category"] == "state and return":
            finite_rows = data["algorithmRefinements"][0]["finiteKernelContract"]["totalReturnMapping"]
            vector = item["coverageValues"]
            mapped = next((row for row in finite_rows if row["interfaceId"] == vector.get("interfaceId")
                           and row["internalResult"] == vector.get("internalResult")), None)
            if (mapped is None or mapped.get("returnContract", {}).get("recordType") != vector.get("returnRecord")
                    or mapped.get("historyEffect") != vector.get("sideEffects")
                    or consumer_output.get("stop") != "Stop-Empty"):
                errors.append(f"{item['id']} state/return vector has no finite-kernel and Stop-Empty consumer")
        if item["category"] == "corpus identity":
            vector = item["coverageValues"]
            capture = capture_by_id.get(vector.get("captureId"))
            if capture is None or any(vector.get(key) != capture.get(key) for key in ("relativePath", "byteCount", "sha256")) or vector.get("resolvedFileIdentity") != "externally-inventoried-regular-file":
                errors.append(f"{item['id']} does not consume a bound capture-manifest identity")
            if consumer_input.get("captureId") != vector.get("captureId"):
                errors.append(f"{item['id']} consumer does not use the inventoried capture")
        if item["category"] == "capture format" and consumer_input.get("captureFormat") != item["coverageValues"]:
            errors.append(f"{item['id']} capture format differs from its case fixture")
        if item["category"] == "label boundary" and (consumer_input.get("labelBoundary") != item["coverageValues"]
                                                      or item["coverageValues"].get("independentTruth") != "not-claimed"
                                                      or any("truth" in key.lower() for key in consumer_output)):
            errors.append(f"{item['id']} exploratory label boundary is not consumed without truth leakage")
        if item["category"] == "IP reassembly":
            vector = item["coverageValues"]
            policy = module_by_id.get("MOD-REASSEMBLY", {}).get("reassemblyPolicy", {})
            offsets, ranges = vector.get("fragmentOffsets"), vector.get("coverageRanges")
            typed_offsets = isinstance(offsets, list) and offsets and all(isinstance(value, int) and not isinstance(value, bool) and value >= 0 for value in offsets)
            typed_ranges = isinstance(ranges, list) and ranges and all(isinstance(value, list) and len(value) == 2 and all(isinstance(bound, int) and not isinstance(bound, bool) and bound >= 0 for bound in value) and value[0] <= value[1] for value in ranges)
            derived_status = _ip_reassembly_status(vector)
            if not (typed_offsets and typed_ranges and derived_status is not None and isinstance(policy, dict)
                    and vector.get("overlapPolicy") == policy.get("overlapPolicy")
                    and vector.get("gapPolicy") == policy.get("gapStatus")):
                errors.append(f"{item['id']} has an unexecutable IP reassembly vector")
            if consumer_input.get("ipFragments") != vector or consumer_output.get("datagramStatus") != derived_status:
                errors.append(f"{item['id']} IP vector is not consumed by its transfer case")
        if item["category"] == "TFTP reconstruction":
            vector = item["coverageValues"]
            blocks = vector.get("blockNumbers")
            tid_pair = vector.get("tidPair") if isinstance(vector.get("tidPair"), list) and len(vector["tidPair"]) == 2 else [None, None]
            if not (isinstance(vector.get("tidPair"), list) and len(vector["tidPair"]) == 2 and all(isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 65535 for value in vector["tidPair"]) and isinstance(blocks, list) and blocks and all(isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 65535 for value in blocks) and isinstance(vector.get("terminalBlock"), int) and not isinstance(vector.get("terminalBlock"), bool) and vector["terminalBlock"] in blocks and vector.get("optionState") in {"ACCEPTED", "DEFAULTED", "UNKNOWN"}):
                errors.append(f"{item['id']} has an unexecutable TFTP reconstruction vector")
            if (consumer_input.get("tid") != {"client": tid_pair[0], "server": tid_pair[1]}
                    or consumer_input.get("blocks") != blocks or consumer_input.get("terminal", {}).get("block") != vector.get("terminalBlock")
                    or consumer_input.get("optionState") != vector.get("optionState")
                    or consumer_output.get("orderedBlocks") != blocks):
                errors.append(f"{item['id']} TFTP vector is not consumed by its transfer case")
        if item["category"] == "field contracts":
            vector = item["coverageValues"]
            source = source_by_id.get(vector.get("sourceRequirementId"), {}) if isinstance(vector.get("sourceRequirementId"), str) else {}
            field_constraint = source.get("fieldConstraint") if isinstance(source, dict) else None
            source_width = field_constraint.get("widthBitsExpression") if isinstance(field_constraint, dict) else None
            width = int(source_width) if isinstance(source_width, str) and source_width.isdecimal() else None
            source_encoding = field_constraint.get("encodingRule") if isinstance(field_constraint, dict) else None
            expected_encoding = (f"ASCII-{width // 8}" if source_encoding == "FIXED-WIDTH-ASCII" and width is not None and width % 8 == 0 else
                                 "UNSIGNED-BE" if source_encoding == "UNSIGNED-INT-BIG-ENDIAN" else None)
            if (not isinstance(vector.get("ordinal"), int) or isinstance(vector.get("ordinal"), bool) or vector["ordinal"] < 0
                    or not isinstance(vector.get("widthBits"), int) or isinstance(vector.get("widthBits"), bool) or vector["widthBits"] <= 0
                    or not isinstance(vector.get("fieldId"), str) or not vector["fieldId"]
                    or vector.get("encodingRule") not in {"ASCII-2", "ASCII-4", "UNSIGNED-BE", "OPAQUE-BYTES"}):
                errors.append(f"{item['id']} has an unexecutable field-layout vector")
            if (not isinstance(field_constraint, dict) or width is None or expected_encoding is None
                    or any(vector.get(field) != field_constraint.get(field) for field in ("protocolFile", "fieldId", "ordinal"))
                    or vector.get("widthBits") != width or vector.get("encodingRule") != expected_encoding):
                errors.append(f"{item['id']} field layout does not match its bound CRS fieldConstraint")
            if consumer_input.get("fieldLayout") != vector:
                errors.append(f"{item['id']} field layout is not consumed by its transfer case")
        if item["category"] == "timing and U":
            vector = item["coverageValues"]
            timing_fixture = consumer_input.get("matrixTimingFixture", {})
            pseudo_case = {"relationId": "RC-VERDICT-WHOLE-INTERVAL",
                           "inputFixture": {"values": {"interval": timing_fixture.get("interval"),
                                                       "requirementWindow": timing_fixture.get("requirementWindow"),
                                                       "clockValid": timing_fixture.get("clockValid")}},
                           "expectedOutputFixture": {"values": {"verdict": timing_fixture.get("expectedVerdict")}}} if isinstance(timing_fixture, dict) else {}
            if (not isinstance(timing_fixture, dict)
                    or vector.get("measurementInterval") != timing_fixture.get("interval")
                    or vector.get("requirementWindow") != timing_fixture.get("requirementWindow")
                    or vector.get("clockValidity") != timing_fixture.get("clockValid")
                    or vector.get("boundaryClosure") != "UPPER-CLOSED"
                    or timing_fixture.get("expectedVerdict") != "INCONCLUSIVE"
                    or _acceptance_relation_errors(pseudo_case)):
                errors.append(f"{item['id']} timing vector is not consumed by the observation relation")
        if item["category"] == "prediction and admission":
            vector = item["coverageValues"]
            if (any(vector.get(key) != consumer_input.get(key) for key in ("H", "eligibleActions", "distinguishingClasses"))
                    or vector.get("resource") != consumer_input.get("resource")
                    or consumer_output.get("selectedActionId") is not None
                    and consumer_output.get("selectedActionId") not in vector.get("eligibleActions", [])):
                errors.append(f"{item['id']} admission vector is not consumed by the select case")
        if item["category"] == "history update":
            vector = item["coverageValues"]
            history = consumer_input.get("history", {})
            if (vector.get("H") != history.get("H")
                    or vector.get("compatibleObservationHypotheses") != consumer_input.get("compatibleObservationHypotheses")
                    or vector.get("historyVersion") != history.get("version")
                    or vector.get("summaryConfirmed") is not consumer_input.get("summaryConfirmed")
                    or consumer_output.get("history", {}).get("H") != []):
                errors.append(f"{item['id']} history vector is not consumed by the intersection case")
        if item["category"] == "matching and no response":
            vector = item["coverageValues"]
            transfer_input = case_by_id.get("AC-SYN-TRANSFER", {}).get("inputFixture", {}).get("values", {})
            owner_fixture = transfer_input.get("ownershipFixture", {})
            no_response = transfer_input.get("noResponseFixture", {})
            schedule_error, owner = _resolve_ownership(owner_fixture) if isinstance(owner_fixture, dict) else ("untyped fixture", None)
            request_states = _request_lifecycle(owner_fixture) if not schedule_error else None
            request_state = request_states.get(no_response.get("requestId")) if isinstance(no_response, dict) and isinstance(request_states, dict) else None
            request_active = request_state == "ACTIVE"
            no_response_disposition = ("ERROR" if request_state == "AMBIGUOUS" else
                                       "FAIL-NO-RESPONSE" if request_active
                                       and type(no_response.get("earliestElapsed")) in (int, float)
                                       and type(no_response.get("deadline")) in (int, float)
                                       and type(no_response.get("upperClosed")) is bool
                                       and (no_response["earliestElapsed"] > no_response["deadline"]
                                            if no_response["upperClosed"] else no_response["earliestElapsed"] >= no_response["deadline"]) else
                                       "INCONCLUSIVE" if request_active else "NO-ACTIVE-OBLIGATION")
            if (set(item["caseIds"]) != {"AC-SYN-OBSERVATION", "AC-SYN-TRANSFER"}
                    or schedule_error or owner_fixture.get("expectedOwner") != owner
                    or any(vector.get(field) != owner_fixture.get(field) for field in ("responseId", "key", "policy", "expectedOwner"))
                    or not isinstance(no_response, dict)
                    or not isinstance(no_response.get("requestId"), str)
                    or no_response["requestId"] not in {event["id"] for event in owner_fixture.get("ownershipEvents", []) if isinstance(event, dict) and event.get("kind") == "REQUEST"}
                    or type(no_response.get("cancelled")) is not bool
                    or type(no_response.get("upperClosed")) is not bool
                    or no_response["cancelled"] is not (request_state == "CANCELLED")
                    or no_response.get("expectedDisposition") != no_response_disposition
                    or vector.get("earliestElapsed") != no_response.get("earliestElapsed")
                    or vector.get("deadline") != no_response.get("deadline")
                    or type(no_response.get("earliestElapsed")) not in (int, float)
                    or type(no_response.get("deadline")) not in (int, float)
                    or not math.isfinite(no_response["earliestElapsed"]) or no_response["earliestElapsed"] < 0
                    or not math.isfinite(no_response["deadline"]) or no_response["deadline"] < 0):
                errors.append(f"{item['id']} ownership/no-response vector lacks its case fixture consumers")
        if item["category"] == "resource accounting":
            vector = item["coverageValues"]
            if (vector.get("resourceMode") != consumer_input.get("mode")
                    or vector.get("remaining") != consumer_input.get("remaining")
                    or vector.get("attemptsIssued") != consumer_input.get("attemptsIssued")
                    or vector.get("retryCount") != consumer_input.get("consecutiveErrorCount")
                    or consumer_output.get("charges") != vector.get("attemptsIssued")):
                errors.append(f"{item['id']} resource vector is not consumed by the charge case")
        if item["category"] == "experiment boundary":
            vector = item["coverageValues"]
            if (any(vector.get(key) != consumer_input.get(key) for key in ("armId", "algorithmVisibleFields", "truthSource", "resetId"))
                    or vector.get("truthSource") != "evaluator-only"
                    or any("truth" in str(field).lower() for field in vector.get("algorithmVisibleFields", []))
                    or consumer_output.get("executionStatus") != "NOT-EXECUTED"):
                errors.append(f"{item['id']} experiment vector is not consumed by the registered scene")
        if item["category"] == "controlled drift":
            vector = item["coverageValues"]
            expected_drift = {"sourceMutation": "remove protocolInputDispositions[0].rationaleZh",
                              "viewMarker": "preserve this failed-publication marker\n",
                              "publicationMode": "--write", "failurePreservesOldView": True}
            if (vector != expected_drift or item["caseIds"]
                    or item.get("testConsumer") != "test_review_generator_refuses_invalid_authority_and_detects_stale_view"):
                errors.append(f"{item['id']} drift vector is not the generator failure-preservation fixture")
        if item["category"] == "controlled drift":
            vector = item["coverageValues"]
            if not (isinstance(vector.get("sourceMutation"), str) and isinstance(vector.get("viewMarker"), str)
                    and vector.get("publicationMode") == "--write" and vector.get("failurePreservesOldView") is True):
                errors.append(f"{item['id']} has an unexecutable controlled-drift vector")
    scenario_ids = [item["id"] for item in data["experimentScenarios"]]
    if len(scenario_ids) != len(set(scenario_ids)) or len(scenario_ids) < 8:
        errors.append("experimentScenarios must contain eight unique first-batch scenes")
    prerequisite_ids = [item["id"] for item in data["experimentPrerequisites"]]
    if len(prerequisite_ids) != len(set(prerequisite_ids)) or any(not item["responsibility"].strip() or not item["closureCondition"].strip() for item in data["experimentPrerequisites"]):
        errors.append("experiment prerequisites are duplicated or incomplete")
    for scenario in data["experimentScenarios"]:
        for field in ("title", "titleZh", "serviceScope", "controllableAction", "faultConfirmation", "independentTruthSource", "resetContract", "timingContract", "resourceContract"):
            if not scenario[field].strip():
                errors.append(f"{scenario['id']} has blank {field}")
        visible = " ".join(scenario["algorithmVisibleFields"]).lower()
        if "truth" in visible or "injection plan" in visible:
            errors.append(f"{scenario['id']} leaks evaluator truth into algorithm-visible fields")
        if scenario["serviceScope"] not in {"UPLOAD", "INFORMATION"}:
            errors.append(f"{scenario['id']} uses an uncontrolled service")
        if not scenario["dependencyIds"] or not scenario["acceptanceCaseIds"] or not set(scenario["acceptanceCaseIds"]).issubset(case_by_id):
            errors.append(f"{scenario['id']} lacks controlled dependency or acceptance bindings")
        if not set(scenario["dependencyIds"]).issubset(prerequisite_ids) or len(scenario.get("scenarioValues", {}).get("eventSequence", [])) < 2:
            errors.append(f"{scenario['id']} has unresolved prerequisites or an incomplete scenario vector")
        values = scenario.get("scenarioValues", {})
        required_scene = {
            "SC-NORMAL-UPLOAD":{"sessionId","terminalStatus"}, "SC-WAIT-CONTINUE":{"obligationId","waitActive"},
            "SC-NO-RESPONSE":{"triggerAt","earliestElapsed","deadline","upperClosed","cancelled"}, "SC-ABORT":{"obligationId","cancelled"},
            "SC-INVALID-OBS":{"clockValid","expectedVerdict"}, "SC-SAME-KEY":{"key","policy","expectedOwner","responseId","ownershipEvents"},
            "SC-SINGLE-BATCH":{"firstContext","secondContext","resetId"}, "SC-RESOURCE-ERROR":{"retryCap","consecutiveErrors","expectedStop"},
        }.get(scenario["id"], set())
        if not required_scene.issubset(values):
            errors.append(f"{scenario['id']} lacks its behavior-specific scenario values")
        if scenario["id"] == "SC-NO-RESPONSE" and not (values.get("cancelled") is False and values.get("earliestElapsed", 0) > values.get("deadline", 0)):
            errors.append("SC-NO-RESPONSE does not establish the controlled elapsed-horizon relation")
        if scenario["id"] == "SC-SAME-KEY" and values.get("policy") not in {"UNIQUE-KEY","FIFO","MOST-RECENT"}:
            errors.append("SC-SAME-KEY has an uncontrolled ownership policy")
        if scenario["id"] == "SC-NORMAL-UPLOAD" and values.get("eventSequence") != ["LUI", "LUR", "DATA", "LUS"]:
            errors.append("SC-NORMAL-UPLOAD lacks the controlled UPLOAD event sequence")
        if scenario["id"] == "SC-INVALID-OBS" and not (values.get("clockValid") is False and values.get("expectedVerdict") == "ERROR"):
            errors.append("SC-INVALID-OBS does not preserve the invalid-clock ERROR relation")
        if scenario["id"] == "SC-SAME-KEY":
            schedule_error, owner = _resolve_ownership(values)
            if schedule_error:
                errors.append(f"SC-SAME-KEY {schedule_error}")
            elif values.get("expectedOwner") != owner:
                errors.append("SC-SAME-KEY ownership result does not follow its declared policy")
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
        if module["id"] == "MOD-REASSEMBLY" and module.get("reassemblyPolicy") != {
            "overlapPolicy": "IDENTICAL-ONLY", "identicalOverlap": "DUPLICATE",
            "differentOverlap": "CONFLICT", "gapStatus": "GAPPED", "overwriteEarlierBytes": False,
        }:
            errors.append("MOD-REASSEMBLY structured overlap/gap policy is missing or unsafe")
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
    integrity_dependencies = [dependency for dependency in data["implementationDependencies"] if set(dependency.get("requirementIds", [])) & set(integrity_by_requirement)]
    if len(integrity_dependencies) != 1:
        errors.append("exactly one dependency must cover the independently bound integrity obligations")
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
        if dependency["runtimeStatus"] == "ESTABLISHED":
            errors.append(f"{dependency['id']} runtime capability cannot be established by this specification-only package")
        source_bindings = {row.get("requirementId"): row for row in dependency["sourceBindings"]}
        if len(source_bindings) != len(dependency["sourceBindings"]) or set(source_bindings) != set(dependency["requirementIds"]):
            errors.append(f"{dependency['id']} source bindings must exactly cover its requirements")
        is_integrity_dependency = dependency in integrity_dependencies
        if is_integrity_dependency and set(dependency["requirementIds"]) != set(integrity_by_requirement):
            errors.append(f"{dependency['id']} requirements differ from the independent obligation baseline")
        if is_integrity_dependency:
            witnesses = {row.get("requirementId"): row for row in dependency.get("obligationWitnesses", [])}
            if len(witnesses) != len(dependency.get("obligationWitnesses", [])) or set(witnesses) != set(integrity_by_requirement):
                errors.append(f"{dependency['id']} obligation witnesses must exactly cover the independent baseline")
            for requirement_id, witness in witnesses.items():
                if not isinstance(witness.get("expected"), dict) or not witness["expected"]:
                    errors.append(f"{dependency['id']} {requirement_id} witness lacks a structured expected relation")
                expected_text = {
                    "CRS-M1-00076": "receiver supports selected INFORMATION integrity option",
                    "CRS-M1-00082": "receiver supports selected UPLOAD integrity option",
                    "CRS-M1-00085": "final-image check value equals the LSP check value",
                    "CRS-M1-00086": "optional old/new comparison retains both identities and its declared result",
                    "CRS-M1-00087": "same part number implies crcA equals crcB",
                    "CRS-M1-00109": "STATUS continues after FINAL-DATA while calculation is in progress",
                }.get(requirement_id)
                if witness.get("expectedRelation") != expected_text:
                    errors.append(f"{dependency['id']} {requirement_id} expectedRelation does not match its controlled structured contract")
            for requirement_id in ("CRS-M1-00076", "CRS-M1-00082"):
                option = witnesses.get(requirement_id, {})
                option_inputs, option_expected = option.get("inputs", {}), option.get("expected", {})
                service = integrity_by_requirement.get(requirement_id, {}).get("service")
                option_entity = symbolic_entities.get(option_inputs.get("optionIdentity")) if isinstance(option_inputs.get("optionIdentity"), str) else None
                bytes_entity = symbolic_entities.get(option_inputs.get("protectedBytesRef")) if isinstance(option_inputs.get("protectedBytesRef"), str) else None
                if not (option_inputs.get("service") == service
                        and option_entity == {"id": option_inputs.get("optionIdentity"), "kind": "OPTION", "service": service}
                        and bytes_entity == {"id": option_inputs.get("protectedBytesRef"), "kind": "PROTECTED-BYTES", "service": service}
                        and option_inputs.get("receiverSupport") is True and option_inputs.get("optionSelected") is True
                        and option_expected == {"receiverSupportsSelectedOption": True, "protectedBytesBound": True}):
                    errors.append(f"{dependency['id']} {requirement_id} witness lacks selected-option support/protected-byte relation")
            same_part = witnesses.get("CRS-M1-00087", {}).get("inputs", {})
            crc_a, crc_b = same_part.get("crcA"), same_part.get("crcB")
            def upload_entity(reference: object, kind: str) -> bool:
                return (isinstance(reference, str) and symbolic_entities.get(reference)
                        == {"id": reference, "kind": kind, "service": "UPLOAD"})
            if not (witnesses.get("CRS-M1-00087", {}).get("expected") == {"samePartNumberCheckValueRelation": "EQUALS"} and upload_entity(same_part.get("fileAId"), "FILE") and upload_entity(same_part.get("fileBId"), "FILE") and same_part.get("fileAId") != same_part.get("fileBId") and isinstance(same_part.get("partNumberA"), str) and same_part.get("partNumberA") and same_part.get("partNumberA") == same_part.get("partNumberB") and all(isinstance(value, str) and value for value in (crc_a, crc_b)) and crc_a == crc_b):
                errors.append(f"{dependency['id']} 00087 witness must compare CRCs of two same-part-number files")
            image = witnesses.get("CRS-M1-00085", {}).get("inputs", {})
            image_values = (image.get("finalImageCheckValue"), image.get("lspCheckValue"))
            if not (upload_entity(image.get("finalImageId"), "FILE") and upload_entity(image.get("lspId"), "FILE") and image.get("orderedBytesPresent") and image.get("checkValuePresent") and image.get("relation") == "EQUALS" and witnesses.get("CRS-M1-00085", {}).get("expected") == {"checkValueRelation": "EQUALS"} and all(isinstance(value, str) and value for value in image_values) and image_values[0] == image_values[1]):
                errors.append(f"{dependency['id']} 00085 witness lacks final-image/LSP check-value relation")
            comparison = witnesses.get("CRS-M1-00086", {}).get("inputs", {})
            comparison_values = (comparison.get("oldCheckValue"), comparison.get("newCheckValue"))
            comparison_selected = comparison.get("comparisonSelected")
            if comparison_selected is False:
                comparison_valid = (comparison == {"comparisonSelected": False}
                                    and witnesses.get("CRS-M1-00086", {}).get("expected") == {"comparisonSelected": False, "comparisonResult": "NOT-APPLICABLE"})
            else:
                computed_comparison = "EQUAL" if comparison_values[0] == comparison_values[1] else "DIFFERENT"
                comparison_valid = (comparison_selected is True
                                    and witnesses.get("CRS-M1-00086", {}).get("expected") == {"comparisonSelected": True, "comparisonResult": computed_comparison}
                                    and upload_entity(comparison.get("oldFileId"), "FILE") and upload_entity(comparison.get("newFileId"), "FILE")
                                    and comparison.get("oldFileId") != comparison.get("newFileId")
                                    and all(isinstance(value, str) and value for value in comparison_values)
                                    and comparison.get("comparisonResult") == computed_comparison)
            if not comparison_valid:
                errors.append(f"{dependency['id']} 00086 witness lacks declared old/new comparison result")
            status = witnesses.get("CRS-M1-00109", {}).get("inputs", {})
            events = status.get("events", [])
            start, end = status.get("calculationStartAt"), status.get("calculationEndAt")
            typed_events = isinstance(events, list) and all(isinstance(event, dict) and isinstance(event.get("kind"), str) and event["kind"] in {"FINAL-DATA", "STATUS"} and isinstance(event.get("at"), int) and not isinstance(event.get("at"), bool) for event in events)
            ordered = typed_events and all(events[index]["at"] < events[index + 1]["at"] for index in range(len(events) - 1))
            final_indices = [index for index, event in enumerate(events) if event.get("kind") == "FINAL-DATA"] if typed_events else []
            final_index = final_indices[-1] if final_indices else -1
            # The required observation schedule is a controlled witness input.  It
            # must not be derived from, or silently reduced to, the STATUS events
            # being used to prove continuation.
            points = status.get("requiredStatusObservationPoints")
            status_times = {event["at"] for event in events[final_index + 1:] if event["kind"] == "STATUS"} if final_index >= 0 and typed_events else set()
            windows = status_schedule.get("observationWindows")
            origin = status_schedule.get("calculationStartAt")
            shift = start - origin if isinstance(start, int) and not isinstance(start, bool) and isinstance(origin, int) and not isinstance(origin, bool) else None
            schedule_valid = (isinstance(start, int) and not isinstance(start, bool) and isinstance(end, int) and not isinstance(end, bool)
                              and shift is not None and end == status_schedule.get("calculationEndAt", -1) + shift
                              and isinstance(windows, list) and bool(windows)
                              and all(isinstance(window, dict) and set(window) == {"from", "through", "statusRequiredAt"}
                                      and all(isinstance(window[key], int) and not isinstance(window[key], bool) for key in window)
                                      and window["from"] < window["statusRequiredAt"] <= window["through"] for window in windows))
            scheduled_points = [window["statusRequiredAt"] + shift for window in windows] if schedule_valid else []
            continued = (schedule_valid and windows[0]["from"] + shift == start and windows[-1]["through"] + shift == end
                         and all(windows[index]["through"] == windows[index + 1]["from"] for index in range(len(windows) - 1))
                         and points == scheduled_points and all(point in status_times for point in scheduled_points))
            if not (status.get("finalDataSeen") is True and status.get("calculationInProgress") is True
                    and status.get("observationComplete") is True
                    and witnesses.get("CRS-M1-00109", {}).get("expected") == {"statusContinuation": "AT-EACH-OBSERVATION-POINT"}
                    and isinstance(start, int) and isinstance(end, int) and start <= end and typed_events and ordered
                    and final_index >= 0 and events[final_index]["at"] <= end and continued):
                errors.append(f"{dependency['id']} 00109 witness lacks post-DATA status continuation")
            def classify_integrity_evidence(requirement_id: str, values: dict) -> str:
                """One finite evidence relation for the baseline and its variants."""
                if requirement_id in {"CRS-M1-00076", "CRS-M1-00082"}:
                    service = integrity_by_requirement.get(requirement_id, {}).get("service")
                    option_ref, bytes_ref = values.get("optionIdentity"), values.get("protectedBytesRef")
                    if not (values.get("service") == service and isinstance(option_ref, str) and isinstance(bytes_ref, str)
                            and symbolic_entities.get(option_ref) == {"id": option_ref, "kind": "OPTION", "service": service}
                            and symbolic_entities.get(bytes_ref) == {"id": bytes_ref, "kind": "PROTECTED-BYTES", "service": service}):
                        return "INVALID-SPEC"
                    if values.get("optionSelected") is None:
                        return "NOT-EVALUATED"
                    if values.get("optionSelected") is False:
                        return "NOT-APPLICABLE"
                    if values.get("receiverSupport") is None:
                        return "NOT-EVALUATED"
                    return "SATISFIED" if values.get("receiverSupport") is True else "VIOLATED"
                if requirement_id == "CRS-M1-00085":
                    if not upload_entity(values.get("finalImageId"), "FILE") or not upload_entity(values.get("lspId"), "FILE"):
                        return "INVALID-SPEC"
                    if values.get("checkValuePresent") is False and any(values.get(key) is not None for key in ("finalImageCheckValue", "lspCheckValue")):
                        return "INVALID-SPEC"
                    if values.get("checkValuePresent") is not True or values.get("orderedBytesPresent") is not True:
                        return "NOT-EVALUATED"
                    if not all(isinstance(values.get(key), str) and values[key] for key in ("finalImageCheckValue", "lspCheckValue")):
                        return "NOT-EVALUATED"
                    return "SATISFIED" if values["finalImageCheckValue"] == values["lspCheckValue"] else "VIOLATED"
                if requirement_id == "CRS-M1-00086":
                    if values.get("comparisonSelected") is False:
                        return "NOT-APPLICABLE"
                    if values.get("comparisonSelected") is None:
                        return "NOT-EVALUATED"
                    if not (upload_entity(values.get("oldFileId"), "FILE") and upload_entity(values.get("newFileId"), "FILE")):
                        return "INVALID-SPEC"
                    old, new = values.get("oldCheckValue"), values.get("newCheckValue")
                    if not all(isinstance(value, str) and value for value in (old, new)) or values.get("comparisonResult") is None:
                        return "NOT-EVALUATED"
                    actual = "EQUAL" if old == new else "DIFFERENT"
                    return "SATISFIED" if values.get("comparisonResult") == actual else "VIOLATED"
                if requirement_id == "CRS-M1-00087":
                    if not (upload_entity(values.get("fileAId"), "FILE") and upload_entity(values.get("fileBId"), "FILE")):
                        return "INVALID-SPEC"
                    if not all(isinstance(values.get(key), str) and values[key] for key in ("partNumberA", "partNumberB")):
                        return "NOT-EVALUATED"
                    if values["partNumberA"] != values["partNumberB"]:
                        return "NOT-APPLICABLE"
                    if not all(isinstance(values.get(key), str) and values[key] for key in ("crcA", "crcB")):
                        return "NOT-EVALUATED"
                    return "SATISFIED" if values["crcA"] == values["crcB"] else "VIOLATED"
                if requirement_id == "CRS-M1-00109":
                    variant_events = values.get("events", [])
                    if (not isinstance(variant_events, list)
                            or any(not isinstance(event, dict) or set(event) != {"kind", "at"}
                                   or not isinstance(event.get("kind"), str)
                                   or event["kind"] not in {"FINAL-DATA", "STATUS"}
                                   or type(event.get("at")) is not int for event in variant_events)):
                        return "INVALID-SPEC"
                    variant_ordered = all(variant_events[index]["at"] < variant_events[index + 1]["at"] for index in range(len(variant_events) - 1))
                    variant_final_indices = [index for index, event in enumerate(variant_events) if event["kind"] == "FINAL-DATA"]
                    if values.get("finalDataSeen") is False and variant_final_indices:
                        return "INVALID-SPEC"
                    if values.get("calculationInProgress") is False:
                        return "NOT-APPLICABLE"
                    if values.get("finalDataSeen") is False or values.get("observationComplete") is False:
                        return "NOT-EVALUATED"
                    if not (values.get("calculationStartAt") == start and values.get("calculationEndAt") == end
                            and values.get("requiredStatusObservationPoints") == scheduled_points
                            and schedule_valid and variant_ordered and len(variant_final_indices) == 1
                            and variant_events[variant_final_indices[0]]["at"] <= end
                            and windows[0]["from"] + shift == start and windows[-1]["through"] + shift == end
                            and all(windows[index]["through"] == windows[index + 1]["from"] for index in range(len(windows) - 1))):
                        return "INVALID-SPEC"
                    observed = {event["at"] for event in variant_events[variant_final_indices[0] + 1:] if event["kind"] == "STATUS"}
                    return "SATISFIED" if all(point in observed for point in scheduled_points) else "VIOLATED"
                return "INVALID-SPEC"
            for requirement_id in integrity_by_requirement:
                if classify_integrity_evidence(requirement_id, witnesses.get(requirement_id, {}).get("inputs", {})) != "SATISFIED":
                    errors.append(f"{dependency['id']} {requirement_id} baseline does not satisfy its shared evidence relation")
            variant_rows = dependency.get("obligationVariants", [])
            required_variants = {
                (requirement_id, branch)
                for requirement_id in ("CRS-M1-00076", "CRS-M1-00082", "CRS-M1-00086", "CRS-M1-00087", "CRS-M1-00109")
                for branch in ("VIOLATED", "NOT-EVALUATED", "NOT-APPLICABLE")
            } | {("CRS-M1-00085", "VIOLATED"), ("CRS-M1-00085", "NOT-EVALUATED")}
            if (not isinstance(variant_rows, list) or len(variant_rows) != len(required_variants)
                    or {(row.get("requirementId"), row.get("branch")) for row in variant_rows if isinstance(row, dict)} != required_variants):
                errors.append(f"{dependency['id']} integrity variant classification matrix is incomplete")
            for variant in variant_rows if isinstance(variant_rows, list) else []:
                if not isinstance(variant, dict):
                    continue
                requirement_id = variant.get("requirementId")
                base = witnesses.get(requirement_id, {}).get("inputs", {})
                changes = variant.get("changes")
                if not isinstance(base, dict) or not isinstance(changes, dict) or not changes or not set(changes).issubset(base):
                    errors.append(f"{dependency['id']} {requirement_id} variant has unbound inputs")
                    continue
                values = dict(base)
                values.update(changes)
                def known_text(value: object) -> bool:
                    return isinstance(value, str) and bool(value)
                nullable_text = lambda value: value is None or known_text(value)
                nullable_bool = lambda value: type(value) in (bool, type(None))
                if requirement_id in {"CRS-M1-00076", "CRS-M1-00082"}:
                    shape_ok = (set(values) == {"service", "receiverSupport", "optionSelected", "optionIdentity", "protectedBytesRef"}
                                and all(known_text(values.get(key)) for key in ("service", "optionIdentity", "protectedBytesRef"))
                                and nullable_bool(values.get("receiverSupport")) and nullable_bool(values.get("optionSelected")))
                elif requirement_id == "CRS-M1-00085":
                    shape_ok = (set(values) == {"finalImageId", "lspId", "orderedBytesPresent", "checkValuePresent", "finalImageCheckValue", "lspCheckValue", "relation"}
                                and upload_entity(values.get("finalImageId"), "FILE") and upload_entity(values.get("lspId"), "FILE")
                                and all(type(values.get(key)) is bool for key in ("orderedBytesPresent", "checkValuePresent"))
                                and all(nullable_text(values.get(key)) for key in ("finalImageCheckValue", "lspCheckValue"))
                                and values.get("relation") == "EQUALS")
                elif requirement_id == "CRS-M1-00086":
                    shape_ok = (set(values) == {"comparisonSelected", "oldFileId", "newFileId", "oldCheckValue", "newCheckValue", "comparisonResult"}
                                and nullable_bool(values.get("comparisonSelected"))
                                and upload_entity(values.get("oldFileId"), "FILE") and upload_entity(values.get("newFileId"), "FILE")
                                and all(nullable_text(values.get(key)) for key in ("oldCheckValue", "newCheckValue"))
                                and (values.get("comparisonResult") is None or isinstance(values.get("comparisonResult"), str)
                                     and values["comparisonResult"] in {"EQUAL", "DIFFERENT"}))
                elif requirement_id == "CRS-M1-00087":
                    shape_ok = (set(values) == {"fileAId", "fileBId", "partNumberA", "partNumberB", "crcA", "crcB"}
                                and upload_entity(values.get("fileAId"), "FILE") and upload_entity(values.get("fileBId"), "FILE")
                                and all(nullable_text(values.get(key)) for key in ("partNumberA", "partNumberB", "crcA", "crcB")))
                else:
                    shape_ok = (set(values) == {"finalDataSeen", "calculationInProgress", "observationComplete", "events", "calculationStartAt", "calculationEndAt", "requiredStatusObservationPoints"}
                                and all(type(values.get(key)) is bool for key in ("finalDataSeen", "calculationInProgress", "observationComplete"))
                                and all(type(values.get(key)) is int for key in ("calculationStartAt", "calculationEndAt"))
                                and isinstance(values.get("requiredStatusObservationPoints"), list)
                                and all(type(point) is int for point in values["requiredStatusObservationPoints"])
                                and isinstance(values.get("events"), list)
                                and all(isinstance(event, dict) and set(event) == {"kind", "at"}
                                        and isinstance(event.get("kind"), str)
                                        and event["kind"] in {"FINAL-DATA", "STATUS"} and type(event.get("at")) is int
                                        for event in values["events"]))
                if not shape_ok:
                    errors.append(f"{dependency['id']} {requirement_id} variant has invalid typed inputs")
                    continue
                classification = classify_integrity_evidence(requirement_id, values)
                if classification != variant.get("branch"):
                    errors.append(f"{dependency['id']} {requirement_id} variant expected {variant.get('branch')} but derives {classification}")
        for requirement_id, binding in source_bindings.items():
            source = source_by_id.get(requirement_id, {})
            if binding.get("sourceUnitId") != source.get("sourceUnitId"):
                errors.append(f"{dependency['id']} has a forged source binding for {requirement_id}")
            baseline = integrity_by_requirement.get(requirement_id)
            if is_integrity_dependency and (baseline is None or binding.get("sourceUnitId") != baseline.get("sourceUnitId") or binding.get("contractId") != baseline.get("contractId")):
                errors.append(f"{dependency['id']} has a forged obligation contract for {requirement_id}")
            if not binding.get("contract", "").strip() or (baseline and baseline["requiredObservation"] not in binding["contract"]):
                errors.append(f"{dependency['id']} lacks concrete obligation semantics for {requirement_id}")
        for evidence in dependency["closureEvidence"]:
            evidence_path = ROOT / evidence
            if Path(evidence).is_absolute() or ".." in Path(evidence).parts or not evidence_path.is_file():
                errors.append(f"{dependency['id']} has unsafe or missing closure evidence {evidence}")
        if is_integrity_dependency and set(dependency["closureEvidence"]) != {
            "configs/engineering/cltav_integrity_obligation_baseline.json",
            "configs/requirements/arinc_615a3_m1_crs.json",
        }:
            errors.append(f"{dependency['id']} closure evidence is not content-bound and relevant")
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
    required_relations = data["requiredDependencyRelations"]
    relation_ids = [row["dependencyId"] for row in required_relations]
    if len(relation_ids) != len(set(relation_ids)):
        errors.append("requiredDependencyRelations repeats a dependency")
    for relation in required_relations:
        dependency = dependency_by_id.get(relation["dependencyId"])
        if dependency is None or set(dependency["requirementIds"]) != set(relation["requirementIds"]):
            errors.append(f"required dependency relation {relation['dependencyId']} was pruned or changed")
            continue
        for requirement_id in relation["requirementIds"]:
            disposition = next((row for row in rows if row["inputRequirementId"] == requirement_id), None)
            if disposition is None or relation["dependencyId"] not in disposition.get("dependencyIds", []):
                errors.append(f"required dependency relation {relation['dependencyId']} lost {requirement_id}")
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
        errors.append("READY activation is outside this Draft specification package and requires an independent acceptance gate")
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
