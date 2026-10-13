"""Small runtime validation for the versioned offline-evidence envelope."""

from __future__ import annotations

import re
from typing import Any


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SOURCE_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
ABSOLUTE_PATH_RE = re.compile(r"(?:^|[\s\"'])((?:[A-Za-z]:[\\/])|/(?:[^\s\"']+))")


def evidence_errors(data: object) -> list[str]:
    """Validate the implementation output shape without a runtime dependency.

    The canonical JSON Schema is stored beside engineering contracts.  This
    lightweight equivalent protects the production publication path in a clean
    installation where the optional development ``jsonschema`` extra is absent.
    """
    if not isinstance(data, dict):
        return ["evidence must be an object"]
    errors: list[str] = []
    required = {
        "artifactType", "schemaVersion", "evidenceBoundary", "tool", "input",
        "runParameters", "executionStatus", "counts", "packetRefs", "datagrams",
        "transfers", "events", "diagnostics",
    }
    missing = required - set(data)
    if missing:
        errors.append("evidence is missing " + ", ".join(sorted(missing)))
    if data.get("artifactType") != "CLTAV-OFFLINE-INTAKE-EVIDENCE":
        errors.append("artifactType is invalid")
    if data.get("schemaVersion") != "1.0":
        errors.append("schemaVersion is invalid")
    boundary = data.get("evidenceBoundary")
    if not isinstance(boundary, dict) or boundary.get("conformanceVerdict") != "NOT-EVALUATED":
        errors.append("evidenceBoundary must keep conformanceVerdict NOT-EVALUATED")
    tool = data.get("tool")
    if not isinstance(tool, dict) or tool.get("name") != "cltav-offline":
        errors.append("tool identity is invalid")
    elif not isinstance(tool.get("sourceCommit"), str) or not SOURCE_COMMIT_RE.fullmatch(tool["sourceCommit"]):
        errors.append("tool.sourceCommit must be a lowercase 40-character Git object ID")
    input_data = data.get("input")
    if not isinstance(input_data, dict):
        errors.append("input must be an object")
    else:
        if not isinstance(input_data.get("captureId"), str) or not input_data["captureId"].strip():
            errors.append("input.captureId is invalid")
        if not isinstance(input_data.get("byteCount"), int) or input_data["byteCount"] < 0:
            errors.append("input.byteCount is invalid")
        if not isinstance(input_data.get("sha256"), str) or not SHA256_RE.fullmatch(input_data["sha256"]):
            errors.append("input.sha256 is invalid")
    if data.get("executionStatus") not in {"COMPLETE", "COMPLETE-WITH-CONTROLLED-ISSUES", "FATAL-INPUT-ERROR"}:
        errors.append("executionStatus is invalid")
    for key in ("packetRefs", "datagrams", "transfers", "events", "diagnostics"):
        if not isinstance(data.get(key), list):
            errors.append(f"{key} must be an array")
    _check_counts(data, errors)
    _check_provenance(data, errors)
    for event in _objects(data.get("events")):
        if not isinstance(event, dict) or event.get("conformanceVerdict") != "NOT-EVALUATED":
            errors.append("events must retain NOT-EVALUATED conformanceVerdict")
            break
    for transfer in _objects(data.get("transfers")):
        if not isinstance(transfer, dict) or transfer.get("integrity") != "NOT-EVALUATED":
            errors.append("transfers must retain NOT-EVALUATED integrity")
            break
    rendered = _rendered_strings(data)
    if ABSOLUTE_PATH_RE.search(rendered):
        errors.append("evidence must not contain an absolute machine path")
    forbidden = {"rawPayload", "payloadBytes", "completePayloadBytes", "capturePath", "corpusRoot"}
    found = _find_forbidden_keys(data, forbidden)
    if found:
        errors.append("evidence contains forbidden payload/path field " + found[0])
    return errors


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


def _check_provenance(data: dict[str, Any], errors: list[str]) -> None:
    packet_ids = _ids(data.get("packetRefs"), "packetRefId", "packetRefs", errors)
    datagram_ids = _ids(data.get("datagrams"), "datagramId", "datagrams", errors)
    transfer_ids = _ids(data.get("transfers"), "transferId", "transfers", errors)
    _ids(data.get("events"), "eventId", "events", errors)
    for item in _objects(data.get("datagrams")):
        if not isinstance(item, dict):
            continue
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
