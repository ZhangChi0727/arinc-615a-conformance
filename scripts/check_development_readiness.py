"""Validate the authoritative CL-TAV first-slice development contract."""
from __future__ import annotations

import copy
import json
import hashlib
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


def _acceptance_relation_errors(case: dict) -> list[str]:
    """Evaluate the closed deterministic relation declared by a specification witness."""
    relation = case.get("relationId", "")
    inputs = case.get("inputFixture", {}).get("values", {})
    outputs = case.get("expectedOutputFixture", {}).get("values", {})
    errors: list[str] = []
    if relation == "RC-TRANSFER-TERMINAL":
        if not isinstance(inputs.get("terminal"), dict) or outputs.get("terminalConfirmed") is not True:
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
        affordable = [a for a in actions if a.get("id") in inputs.get("eligibleActions", []) and a.get("cost", 10**9) <= resource.get("remaining", -1)]
        expected = min(affordable, key=lambda a: (a["worstClass"], a["cost"], a["id"]))["id"] if affordable else None
        if len(affordable) < 2 or outputs.get("selectedActionId") != expected:
            errors.append("RC-SELECT-STABLE-ID at expectedOutputFixture.values.selectedActionId")
    elif relation == "RC-VERDICT-WHOLE-INTERVAL":
        interval = inputs.get("interval", {})
        window = inputs.get("requirementWindow", {})
        try:
            for candidate in (interval, window):
                if not isinstance(candidate, dict) or set(candidate) != {"lower", "upper", "lowerClosed", "upperClosed"} or not isinstance(candidate["lower"], (int, float)) or isinstance(candidate["lower"], bool) or not isinstance(candidate["upper"], (int, float)) or isinstance(candidate["upper"], bool) or candidate["lower"] > candidate["upper"] or candidate["lower"] == candidate["upper"] and not (candidate["lowerClosed"] and candidate["upperClosed"]):
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
        compatible = set(inputs.get("compatibleObservationHypotheses", []))
        if set(new.get("H", [])) != set(old.get("H", [])) & compatible or new.get("version") != old.get("version", -1) + 1:
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
        if outputs.get("attemptDenominator") != len(inputs.get("attempts", [])):
            errors.append("RC-DENOMINATOR-ATTEMPTS at expectedOutputFixture.values.attemptDenominator")
        if outputs.get("answeredDenominator") != sum(item in {"PASS", "FAIL"} for item in inputs.get("attempts", [])):
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
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        integrity_by_requirement = {}
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
                "IF-HIST-UPDATE": {"status","compatibleStateByHypothesis","Hprime","historyHandlePrime","historyVersion","summaryEffect"},
                "IF-EQUIV": {"status","proofBasis"},
                "IF-RESOURCE-STOP": {"stopClass","finalH","trace"},
            }.get(row["interfaceId"], set()) if row["reachable"] else set()
            if row["interfaceId"] == "IF-PRED-OBS" and row["reachable"] and row["internalResult"] != "FEASIBLE":
                required_contract_fields = required_contract_fields - {"classesByTest"}
            if set(contract.get("requiredFields", [])) != required_contract_fields:
                errors.append(f"{refinement['id']} return contract is incomplete for {row['interfaceId']}/{row['internalResult']}")
            expected_record = {"IF-PRED-OBS": "PredictionResult", "IF-SELECT-ADMIT": "Decision", "IF-HIST-UPDATE": "HistoryUpdateBackendResult", "IF-EQUIV": "EquivalenceResult", "IF-RESOURCE-STOP": "StopResult"}.get(row["interfaceId"])
            if row["reachable"] and contract.get("recordType") != expected_record:
                errors.append(f"{refinement['id']} return record type is not the controlled {expected_record} for {row['interfaceId']}/{row['internalResult']}")
            if row["interfaceId"] == "IF-HIST-UPDATE" and row["reachable"] and ("eta_c" not in contract.get("adapter", "") or "H_c" not in contract.get("adapter", "") or "S9" not in contract.get("adapter", "")):
                errors.append(f"{refinement['id']} history backend adapter does not preserve eta_c/H_c through S9")
            if row["interfaceId"] == "IF-PRED-OBS" and row["reachable"]:
                expects_classes = row["internalResult"] == "FEASIBLE"
                if ("classesByTest" in contract.get("requiredFields", [])) != expects_classes:
                    errors.append(f"{refinement['id']} prediction return payload does not distinguish OK from GAP")
            if row["interfaceId"] == "IF-SELECT-ADMIT" and row["reachable"] and "TEST-scoped" not in contract.get("adapter", ""):
                errors.append(f"{refinement['id']} selection adapter loses TEST-scoped GAP semantics")
        model_schema = finite["modelInstanceSchema"]
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
            return lo is not None and hi is not None and lo <= hi and (lo != hi or value["lowerClosed"] and value["upperClosed"]) and isinstance(value["lowerClosed"], bool) and isinstance(value["upperClosed"], bool)
        def intersection(left: dict, right: dict) -> dict | None:
            left_lower, left_upper = rational(left["lower"]), rational(left["upper"])
            right_lower, right_upper = rational(right["lower"]), rational(right["upper"])
            assert left_lower is not None and left_upper is not None and right_lower is not None and right_upper is not None
            lower, upper = max(left_lower, right_lower), min(left_upper, right_upper)
            if lower > upper:
                return None
            lower_closed = (left["lowerClosed"] if left_lower == lower else left["upperClosed"]) and (right["lowerClosed"] if right_lower == lower else right["upperClosed"])
            upper_closed = (left["upperClosed"] if left_upper == upper else left["lowerClosed"]) and (right["upperClosed"] if right_upper == upper else right["lowerClosed"])
            if lower == upper and not (lower_closed and upper_closed):
                return None
            def fraction_object(value: Fraction) -> dict[str, int]:
                return {"numerator": value.numerator, "positiveDenominator": value.denominator}
            return {"lower": fraction_object(lower), "upper": fraction_object(upper), "lowerClosed": lower_closed, "upperClosed": upper_closed}
        def advanced(interval: dict, delta: Fraction) -> dict:
            def fraction_object(value: Fraction) -> dict[str, int]:
                return {"numerator": value.numerator, "positiveDenominator": value.denominator}
            return {"lower": fraction_object(rational(interval["lower"]) + delta), "upper": fraction_object(rational(interval["upper"]) + delta), "lowerClosed": interval["lowerClosed"], "upperClosed": interval["upperClosed"]}
        declared_states = set(model_schema.get("stateIds", []))
        declared_clocks = set(model_schema.get("clockIds", []))
        declared_variables = model_schema.get("typedVariables", {})
        if not declared_states or not declared_clocks or not isinstance(declared_variables, dict):
            errors.append(f"{refinement['id']} model instance lacks finite state/clock/variable declarations")
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
                return [] if set(ast) == {"tag", "state"} and ast.get("state") in declared_states else ["STATE-EQUALS lacks a declared state"]
            if tag == "RATIONAL-INTERVAL-CONTAINS":
                return [] if set(ast) == {"tag", "clock", "interval"} and ast.get("clock") in declared_clocks and valid_interval(ast.get("interval")) else ["RATIONAL-INTERVAL-CONTAINS is malformed"]
            if tag == "TYPED-FIELD-EQUALS":
                domain = declared_variables.get(ast.get("field")) if isinstance(declared_variables, dict) else None
                return [] if set(ast) == {"tag", "field", "value"} and isinstance(domain, list) and ast.get("value") in domain else ["TYPED-FIELD-EQUALS is malformed"]
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
                return current if isinstance(store, dict) and store.get(ast["field"]) == ast["value"] else None
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
                if tag == "CLOCK-RESET-TO-ZERO" and set(update) == {"tag", "clock"} and update.get("clock") in declared_clocks:
                    target = ("clock", update["clock"])
                elif tag == "TYPED-FIELD-ASSIGN" and set(update) == {"tag", "field", "value"} and update.get("field") in declared_variables and update.get("value") in declared_variables[update["field"]]:
                    target = ("field", update["field"])
                elif tag == "STATE-ASSIGN" and set(update) == {"tag", "state"} and update.get("state") in declared_states:
                    target = ("state", "control")
                else:
                    results.append(f"unsupported or malformed update {tag}"); continue
                if target in targets:
                    results.append(f"conflicting simultaneous update {target[0]}:{target[1]}")
                targets.add(target)
            return results
        for witness_id in ("FK-W1-FEASIBLE", "FK-W2-INFEASIBLE"):
            witness = next(row for row in finite["witnessVectors"] if row["id"] == witness_id)
            if not valid_interval(witness["input"].get("clockConstraint")) or not valid_interval(witness["input"].get("guard")):
                errors.append(f"{refinement['id']} {witness_id} has a noncanonical or reversed interval")
            transition = witness["input"].get("transition", {})
            actual_guard = guard_interval(transition.get("guardAst", {})) if isinstance(transition.get("guardAst"), dict) else None
            if transition.get("source") != witness["input"].get("state") or not isinstance(transition.get("target"), str) or not transition["target"]:
                errors.append(f"{refinement['id']} {witness_id} transition endpoints are malformed")
            if guard_errors(transition.get("guardAst")) or update_errors(transition.get("simultaneousUpdates")):
                errors.append(f"{refinement['id']} {witness_id} has an unsupported guard or update")
            if not valid_interval(actual_guard) or actual_guard != witness["input"].get("guard"):
                errors.append(f"{refinement['id']} {witness_id} transition guard differs from the authoritative guard")
            delta = rational(witness["input"].get("delta"))
            if delta is None or delta < 0 or witness["input"].get("quantifier") != "EXISTS-DELTA":
                errors.append(f"{refinement['id']} {witness_id} has an invalid time-advance witness")
            elif valid_interval(witness["input"].get("clockConstraint")) and valid_interval(actual_guard):
                successor = guard_constraint(transition["guardAst"], advanced(witness["input"]["clockConstraint"], delta), witness["input"].get("state"), witness["input"].get("typedStore", {}))
                computed = "FEASIBLE" if successor is not None else "INFEASIBLE"
                if witness.get("expected", {}).get("result") != computed:
                    errors.append(f"{refinement['id']} {witness_id} result does not follow its clock/guard constraint")
                reset = any(update.get("tag") == "CLOCK-RESET-TO-ZERO" and update.get("clock") == "x" for update in transition["simultaneousUpdates"])
                if reset and successor is not None:
                    successor = {"lower": {"numerator": 0, "positiveDenominator": 1}, "upper": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": True, "upperClosed": True}
                if computed == "FEASIBLE" and (witness["expected"].get("state") != transition.get("target") or witness["expected"].get("clockConstraint") != successor):
                    errors.append(f"{refinement['id']} {witness_id} successor does not follow its transition/time advance")
        w3 = next(row for row in finite["witnessVectors"] if row["id"] == "FK-W3-UNKNOWN")
        w3_guard = w3.get("input", {}).get("transition", {}).get("guardAst")
        if not guard_errors(w3_guard) or w3.get("expected", {}).get("result") != "UNSUPPORTED-SYNTAX":
            errors.append(f"{refinement['id']} unsupported syntax witness is not a typed unsupported guard")
        clock_witness = next(row for row in finite["witnessVectors"] if row["id"] == "FK-W5-CLOCK")
        if clock_witness.get("expected", {}).get("merge") is not False or not all(valid_interval(value) for value in clock_witness.get("input", {}).get("clockConstraints", [])):
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
        if not isinstance(old, dict) or not isinstance(new, dict) or not isinstance(old.get("H"), list) or not isinstance(new.get("H"), list) or not isinstance(compatible_raw, list) or not isinstance(old.get("version"), int) or not isinstance(new.get("version"), int):
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
        sv=select_case["inputFixture"]["values"]; affordable=[a for a in sv["actions"] if a["id"] in sv["eligibleActions"] and a["cost"] <= sv["resource"]["remaining"]]
        chosen=select_case["expectedOutputFixture"]["values"].get("selectedActionId")
        if len(affordable) < 2 or chosen != min(affordable,key=lambda a:(a["worstClass"],a["cost"],a["id"]))["id"]:
            errors.append("AC-SYN-SELECT does not exercise the controlled affordable stable-ID tie")
    required_matrix_categories = {"corpus identity", "label boundary", "capture format", "IP reassembly", "TFTP reconstruction", "field contracts", "matching and no response", "timing and U", "prediction and admission", "history update", "state and return", "resource accounting", "experiment boundary", "controlled drift"}
    matrix_ids = [item["id"] for item in data["acceptanceMatrix"]]
    if len(matrix_ids) != len(set(matrix_ids)) or {item["category"] for item in data["acceptanceMatrix"]} != required_matrix_categories:
        errors.append("acceptanceMatrix must cover each controlled category exactly once")
    if any(not item[field].strip() for item in data["acceptanceMatrix"] for field in ("category", "categoryZh", "positiveInput", "positiveInputZh", "expectedOutput", "expectedOutputZh", "negativeMutation", "negativeMutationZh", "expectedRejection", "expectedRejectionZh")):
        errors.append("acceptanceMatrix contains a blank executable specification")
    for item in data["acceptanceMatrix"]:
        if not item["caseIds"] or not set(item["caseIds"]).issubset(case_by_id):
            errors.append(f"{item['id']} has an unknown or empty acceptance-vector reference")
        required_axes = {
            "corpus identity":{"captureId","relativePath","byteCount","sha256","resolvedFileIdentity"}, "IP reassembly":{"fragmentOffsets","coverageRanges","overlapPolicy","gapPolicy"},
            "TFTP reconstruction":{"tidPair","blockNumbers","terminalBlock","optionState"}, "timing and U":{"measurementInterval","requirementWindow","clockValidity","boundaryClosure"},
            "history update":{"H","compatibleObservationHypotheses","historyVersion","summaryConfirmed"}, "controlled drift":{"authorityHash","viewHash","publicationMode","failurePreservesOldView"},
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
            "corpus identity": "AC-EXP-TRUTH", "label boundary": "AC-EXP-TRUTH", "capture format": "AC-SYN-TRANSFER",
            "IP reassembly": "AC-SYN-TRANSFER", "TFTP reconstruction": "AC-SYN-TRANSFER", "field contracts": "AC-SYN-TRANSFER",
            "matching and no response": "AC-SYN-OBSERVATION", "timing and U": "AC-SYN-OBSERVATION", "prediction and admission": "AC-SYN-PREDICTION",
            "history update": "AC-SYN-HISTORY", "state and return": "AC-SYN-RESOURCE-STOP", "resource accounting": "AC-SYN-RESOURCE-STOP",
            "experiment boundary": "AC-EXP-SCENE", "controlled drift": "AC-EXP-CAUSAL",
        }[item["category"]]
        if expected_case not in item["caseIds"]:
            errors.append(f"{item['id']} is not bound to its controlled acceptance consumer")
        if item["category"] == "state and return" and item["coverageValues"] != {"internalResult": "EMPTY-HISTORY", "interfaceId": "IF-RESOURCE-STOP", "returnRecord": "StopResult", "sideEffects": "PRESERVE"}:
            errors.append(f"{item['id']} has an unbound state/return coverage vector")
        if item["category"] == "corpus identity":
            vector = item["coverageValues"]
            capture = capture_by_id.get(vector.get("captureId"))
            if capture is None or any(vector.get(key) != capture.get(key) for key in ("relativePath", "byteCount", "sha256")) or vector.get("resolvedFileIdentity") != "git-tracked-regular-file":
                errors.append(f"{item['id']} does not consume a bound capture-manifest identity")
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
            "SC-INVALID-OBS":{"clockValid","expectedVerdict"}, "SC-SAME-KEY":{"key","policy","expectedOwner"},
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
            owner = {"FIFO": "REQUEST-A", "MOST-RECENT": "REQUEST-B", "UNIQUE-KEY": "AMBIGUOUS"}.get(values.get("policy"))
            if values.get("expectedOwner") != owner:
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
                if not (option_inputs.get("receiverSupport") is True and option_inputs.get("optionSelected") is True and isinstance(option_inputs.get("optionIdentity"), str) and option_inputs["optionIdentity"] and isinstance(option_inputs.get("protectedBytesRef"), str) and option_inputs["protectedBytesRef"] and option_expected == {"receiverSupportsSelectedOption": True, "protectedBytesBound": True}):
                    errors.append(f"{dependency['id']} {requirement_id} witness lacks selected-option support/protected-byte relation")
            same_part = witnesses.get("CRS-M1-00087", {}).get("inputs", {})
            if not (witnesses.get("CRS-M1-00087", {}).get("expected") == {"samePartNumberCheckValueRelation": "EQUALS"} and same_part.get("fileAId") != same_part.get("fileBId") and same_part.get("partNumberA") == same_part.get("partNumberB") and same_part.get("crcA") == same_part.get("crcB")):
                errors.append(f"{dependency['id']} 00087 witness must compare CRCs of two same-part-number files")
            image = witnesses.get("CRS-M1-00085", {}).get("inputs", {})
            image_values = (image.get("finalImageCheckValue"), image.get("lspCheckValue"))
            if not (image.get("orderedBytesPresent") and image.get("checkValuePresent") and image.get("relation") == "EQUALS" and witnesses.get("CRS-M1-00085", {}).get("expected") == {"checkValueRelation": "EQUALS"} and all(isinstance(value, str) and value for value in image_values) and image_values[0] == image_values[1]):
                errors.append(f"{dependency['id']} 00085 witness lacks final-image/LSP check-value relation")
            comparison = witnesses.get("CRS-M1-00086", {}).get("inputs", {})
            comparison_values = (comparison.get("oldCheckValue"), comparison.get("newCheckValue"))
            if not (comparison.get("comparisonSelected") and witnesses.get("CRS-M1-00086", {}).get("expected") == {"comparisonSelected": True, "comparisonResult": "DIFFERENT"} and isinstance(comparison.get("oldFileId"), str) and isinstance(comparison.get("newFileId"), str) and comparison.get("oldFileId") and comparison.get("newFileId") and comparison.get("oldFileId") != comparison.get("newFileId") and all(isinstance(value, str) and value for value in comparison_values) and comparison.get("comparisonResult") == ("EQUAL" if comparison_values[0] == comparison_values[1] else "DIFFERENT")):
                errors.append(f"{dependency['id']} 00086 witness lacks declared old/new comparison result")
            status = witnesses.get("CRS-M1-00109", {}).get("inputs", {})
            events = status.get("events", [])
            start, end = status.get("calculationStartAt"), status.get("calculationEndAt")
            typed_events = isinstance(events, list) and all(isinstance(event, dict) and event.get("kind") in {"FINAL-DATA", "STATUS"} and isinstance(event.get("at"), int) and not isinstance(event.get("at"), bool) for event in events)
            ordered = typed_events and all(events[index]["at"] < events[index + 1]["at"] for index in range(len(events) - 1))
            final_indices = [index for index, event in enumerate(events) if event.get("kind") == "FINAL-DATA"] if typed_events else []
            final_index = final_indices[-1] if final_indices else -1
            points = status.get("statusObservationPoints")
            status_times = {event["at"] for event in events[final_index + 1:] if event["kind"] == "STATUS"} if final_index >= 0 and typed_events else set()
            continued = isinstance(points, list) and points and all(isinstance(point, int) and start <= point <= end and point in status_times for point in points) if isinstance(start, int) and isinstance(end, int) else False
            if not (status.get("finalDataSeen") and status.get("calculationInProgress") and witnesses.get("CRS-M1-00109", {}).get("expected") == {"statusContinuation": "AT-EACH-OBSERVATION-POINT"} and isinstance(start, int) and isinstance(end, int) and start <= end and typed_events and ordered and final_index >= 0 and events[final_index]["at"] <= end and continued):
                errors.append(f"{dependency['id']} 00109 witness lacks post-DATA status continuation")
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
