"""Small runtime validation for the versioned offline-evidence envelope."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from typing import Any

from jsonschema import Draft202012Validator

from .contracts import evidence_projection_errors
from .controlled_resources import ControlledResourceError, controlled_resource_json


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SOURCE_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
ABSOLUTE_PATH_RE = re.compile(r"(?:^|[\s\"'])((?:[A-Za-z]:[\\/])|/(?:[^\s\"']+))")


def evidence_errors(data: object) -> list[str]:
    """Validate published evidence against the controlled schema and relations.

    JSON Schema is a runtime dependency rather than a best-effort developer
    extra: a publisher must never claim to validate a shape it does not execute.
    The semantic pass below deliberately covers cross-record parentage that a
    local JSON Schema cannot express succinctly.
    """
    schema_errors = _schema_errors(data)
    if schema_errors:
        return schema_errors
    if not isinstance(data, dict):
        return ["evidence must be an object"]
    errors: list[str] = []
    _check_counts(data, errors)
    _check_provenance(data, errors)
    _check_execution_shape(data, errors)
    errors.extend(evidence_projection_errors(data))
    rendered = _rendered_strings(data)
    if ABSOLUTE_PATH_RE.search(rendered):
        errors.append("evidence must not contain an absolute machine path")
    forbidden = {"rawPayload", "payloadBytes", "completePayloadBytes", "capturePath", "corpusRoot"}
    found = _find_forbidden_keys(data, forbidden)
    if found:
        errors.append("evidence contains forbidden payload/path field " + found[0])
    return errors


def evidence_failure_code(errors: list[str]) -> str:
    """Return a stable tool code when validation failed before interpretation."""
    for error in errors:
        code = error.split(":", 1)[0]
        if code.startswith("CONTROLLED-RESOURCE-") or code.startswith("DEVELOPMENT-CONTRACT-"):
            return code
    return "EVIDENCE-SCHEMA-ERROR"


@lru_cache(maxsize=1)
def _validator() -> Draft202012Validator:
    try:
        schema = controlled_resource_json("evidence-schema")
    except ControlledResourceError as exc:  # pragma: no cover - package/install failure boundary
        raise RuntimeError(f"{exc.code}: {exc}") from exc
    return Draft202012Validator(schema)


def _schema_errors(data: object) -> list[str]:
    try:
        errors = sorted(_validator().iter_errors(data), key=lambda item: list(item.absolute_path))
    except RuntimeError as exc:
        return [str(exc)]
    return [
        "schema " + (".".join(str(part) for part in error.absolute_path) or "$") + f": {error.message}"
        for error in errors
    ]


def _check_counts(data: dict[str, Any], errors: list[str]) -> None:
    counts = data.get("counts")
    expected = {
        "evidencePacketRefs": "packetRefs",
        "datagrams": "datagrams",
        "transfers": "transfers",
        "events": "events",
        "diagnostics": "diagnostics",
    }
    if not isinstance(counts, dict):
        errors.append("counts must be an object")
        return
    for count_name, list_name in expected.items():
        value = counts.get(count_name)
        records = data.get(list_name)
        if not isinstance(value, int) or value < 0:
            errors.append(f"counts.{count_name} is invalid")
        elif isinstance(records, list) and value != len(records):
            errors.append(f"counts.{count_name} differs from {list_name} length")
    container_packets = counts.get("containerPackets")
    if not isinstance(container_packets, int) or container_packets < 0:
        errors.append("counts.containerPackets is invalid")


def _check_execution_shape(data: dict[str, Any], errors: list[str]) -> None:
    """Tie declared execution status to observable evidence, without verdicts."""
    execution = data["executionStatus"]
    diagnostics = data["diagnostics"]
    non_complete = any(item.get("status") != "COMPLETE" for item in _objects(data["datagrams"])) or any(
        item.get("reconstructionStatus") != "COMPLETE" for item in _objects(data["transfers"])
    )
    parse_issue = any(
        item.get("layer") == "PARSE-RESULT"
        and isinstance(item.get("fields"), dict)
        and item["fields"].get("parseStatus") != "PARSED"
        for item in _objects(data["events"])
        if isinstance(item, dict)
    )
    if execution == "COMPLETE" and (diagnostics or non_complete or parse_issue):
        errors.append("COMPLETE execution cannot contain controlled issues")
    if execution == "COMPLETE-WITH-CONTROLLED-ISSUES" and not (diagnostics or non_complete or parse_issue):
        errors.append("controlled-issues execution must retain a controlled issue")
    if execution == "FATAL-INPUT-ERROR":
        if any(data[key] for key in ("packetRefs", "datagrams", "transfers", "events")):
            errors.append("fatal input evidence must not publish partial reconstruction records")
        if len(diagnostics) != 1 or diagnostics[0].get("severity") != "ERROR":
            errors.append("fatal input evidence must contain exactly one ERROR diagnostic")


def _check_provenance(data: dict[str, Any], errors: list[str]) -> None:
    input_capture_id = data["input"]["captureId"]
    packet_ids = _ids(data.get("packetRefs"), "packetRefId", "packetRefs", errors)
    datagram_ids = _ids(data.get("datagrams"), "datagramId", "datagrams", errors)
    transfer_ids = _ids(data.get("transfers"), "transferId", "transfers", errors)
    _ids(data.get("events"), "eventId", "events", errors)
    for item in _objects(data.get("datagrams")):
        if not isinstance(item, dict):
            continue
        if item.get("captureId") != input_capture_id:
            errors.append("datagram captureId differs from input captureId")
        _require_known_ids(item.get("packetRefIds"), packet_ids, "datagram packetRefIds", errors)
        status = item.get("status")
        payload_length = item.get("payloadLength")
        if status == "COMPLETE" and (not isinstance(payload_length, int) or payload_length < 0):
            errors.append("complete datagram must declare a nonnegative payloadLength")
        if status != "COMPLETE" and payload_length is not None:
            errors.append("non-complete datagram must not publish a payloadLength")
    for item in _objects(data.get("transfers")):
        if not isinstance(item, dict):
            continue
        if item.get("captureId") != input_capture_id:
            errors.append("transfer captureId differs from input captureId")
        _require_known_ids(item.get("packetRefIds"), packet_ids, "transfer packetRefIds", errors)
        _require_known_ids(item.get("datagramIds"), datagram_ids, "transfer datagramIds", errors)
        block = item.get("blockSize")
        if not isinstance(block, dict):
            errors.append("transfer blockSize must be an object")
            continue
        option_status = block.get("status")
        value = block.get("value")
        if option_status == "DEFAULTED" and value != 512:
            errors.append("DEFAULTED transfer blockSize must be 512")
        if option_status == "UNKNOWN" and value is not None:
            errors.append("UNKNOWN transfer blockSize must be null")
        if option_status == "ACCEPTED" and (not isinstance(value, int) or value < 1):
            errors.append("ACCEPTED transfer blockSize must be a positive integer")
        complete_length = item.get("completePayloadLength")
        if item.get("reconstructionStatus") == "COMPLETE" and (
            not isinstance(complete_length, int) or complete_length < 0
        ):
            errors.append("complete transfer must declare a nonnegative completePayloadLength")
        if item.get("reconstructionStatus") != "COMPLETE" and complete_length is not None:
            errors.append("non-complete transfer must not publish completePayloadLength")
    for item in _objects(data.get("events")):
        if not isinstance(item, dict):
            continue
        transfer_id = item.get("transferId")
        if not isinstance(transfer_id, str) or transfer_id not in transfer_ids:
            errors.append("event transferId does not reference a known transfer")
        _require_known_ids(item.get("sourceDatagramIds"), datagram_ids, "event sourceDatagramIds", errors)
        _require_known_ids(item.get("sourcePacketRefIds"), packet_ids, "event sourcePacketRefIds", errors)
        if isinstance(transfer_id, str) and transfer_id in transfer_ids:
            parent = next(candidate for candidate in _objects(data.get("transfers")) if candidate.get("transferId") == transfer_id)
            if not set(item.get("sourceDatagramIds", [])).issubset(set(parent.get("datagramIds", []))):
                errors.append("event sourceDatagramIds are not owned by its transfer")
            if not set(item.get("sourcePacketRefIds", [])).issubset(set(parent.get("packetRefIds", []))):
                errors.append("event sourcePacketRefIds are not owned by its transfer")
    for item in _objects(data.get("packetRefs")):
        if isinstance(item, dict) and item.get("captureId") != input_capture_id:
            errors.append("packetRef captureId differs from input captureId")
    for item in _objects(data.get("diagnostics")):
        if not isinstance(item, dict):
            continue
        packet_ref_id = item.get("packetRefId")
        if packet_ref_id is not None and packet_ref_id not in packet_ids:
            errors.append("diagnostic packetRefId does not reference a known packetRef")


def _ids(value: object, key: str, label: str, errors: list[str]) -> set[str]:
    if not isinstance(value, list):
        return set()
    result: set[str] = set()
    for item in value:
        if not isinstance(item, dict) or not isinstance(item.get(key), str) or not item[key]:
            errors.append(f"{label} contains an item without {key}")
            continue
        if item[key] in result:
            errors.append(f"{label} has repeated {key}")
            continue
        result.add(item[key])
    return result


def _require_known_ids(value: object, known: set[str], label: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{label} must be an array")
        return
    for item in value:
        if not isinstance(item, str) or item not in known:
            errors.append(f"{label} contains an unknown reference")
            return


def _objects(value: object) -> list[object]:
    return value if isinstance(value, list) else []


def _rendered_strings(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(_rendered_strings(item) for item in value.values())
    if isinstance(value, list):
        return "\n".join(_rendered_strings(item) for item in value)
    return ""


def _find_forbidden_keys(value: object, forbidden: set[str]) -> list[str]:
    if isinstance(value, dict):
        result = [key for key in value if key in forbidden]
        for child in value.values():
            result.extend(_find_forbidden_keys(child, forbidden))
        return result
    if isinstance(value, list):
        result: list[str] = []
        for child in value:
            result.extend(_find_forbidden_keys(child, forbidden))
        return result
    return []
