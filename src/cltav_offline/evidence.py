"""Small runtime validation for the versioned offline-evidence envelope."""

from __future__ import annotations

import re
from typing import Any


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ABSOLUTE_PATH_RE = re.compile(r"(?:^|[\"'])((?:[A-Za-z]:[\\/])|/)")


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
    for event in data.get("events", []):
        if not isinstance(event, dict) or event.get("conformanceVerdict") != "NOT-EVALUATED":
            errors.append("events must retain NOT-EVALUATED conformanceVerdict")
            break
    for transfer in data.get("transfers", []):
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
