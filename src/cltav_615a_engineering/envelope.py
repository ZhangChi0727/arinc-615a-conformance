"""Closed 615A engineering evidence envelope.  Not a G3 producer document."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Mapping

from jsonschema import Draft202012Validator

from .errors import EngineeringError
from .identity import ARTIFACT_TYPE, FORBIDDEN_G3_MODES, PRODUCER_MODE, SCHEMA_ID, schema_bytes
from .jsonutil import canonical_json_bytes, sha256_hex

UNEVALUATED_OBLIGATIONS = (
    "FULL-UPLOAD-COMPLETION",
    "LUR-PAYLOAD-INTEGRITY",
    "CRC-CHECK-VALUE-NAMING-CAPABILITY",
    "PROTOCOL-NO-RESPONSE-DEADLINE",
    "REAL-NETWORK-OR-IUT",
    "FOUR-ARM-EXPERIMENT",
    "POST-RECOVER-FULL-SESSION-H-DISCRIMINATION",
)

EVALUATOR_KEYS = frozenset({
    "faultPlan", "faultId", "activeFault", "evaluatorTruth", "injection",
    "privateLoaderState", "bypassReason",
})

REPLAY_EXCLUDED_FIELDS = frozenset({
    "runId",
    "attemptId",
    "resetId",
    "sessionId",
    "correlationId",
    "wallClockUtc",
    "eventId",
    "executionAttemptId",
    "snapshotId",
    "readbackId",
    "evidenceRef",
})


def _validator() -> Draft202012Validator:
    import json

    schema = json.loads(schema_bytes().decode("utf-8"))
    return Draft202012Validator(schema)


def fingerprint_payload(algorithm_visible: Mapping[str, Any]) -> dict[str, Any]:
    payload = {key: value for key, value in algorithm_visible.items() if key != "fingerprintSha256"}
    return payload


def compute_fingerprint(algorithm_visible: Mapping[str, Any]) -> str:
    return sha256_hex(canonical_json_bytes(fingerprint_payload(algorithm_visible)))


def assemble_envelope(
    *,
    algorithm_visible: dict[str, Any],
    evaluator_audit: dict[str, Any],
    quality_status: str,
) -> dict[str, Any]:
    visible = deepcopy(algorithm_visible)
    visible["fingerprintSha256"] = compute_fingerprint(visible)
    document = {
        "artifactType": ARTIFACT_TYPE,
        "producerMode": PRODUCER_MODE,
        "schemaId": SCHEMA_ID,
        "cliExitMeaning": "ZERO-MEANS-VALID-ENGINEERING-RECORD-NOT-IUT-PASS",
        "qualityStatus": quality_status,
        "algorithmVisible": visible,
        "evaluatorAudit": deepcopy(evaluator_audit),
    }
    validate_envelope(document)
    return document


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate_envelope(document: Mapping[str, Any]) -> None:
    if document.get("producerMode") in FORBIDDEN_G3_MODES or document.get("artifactType") in FORBIDDEN_G3_MODES:
        raise EngineeringError("G3-PRODUCER-IMPERSONATION", "615A engineering evidence must not claim the G3 producer mode")
    if document.get("producerMode") != PRODUCER_MODE or document.get("artifactType") != ARTIFACT_TYPE:
        raise EngineeringError("ENVELOPE-PRODUCER-INVALID", "envelope producer/artifact identity is not the 615A engineering mode")
    visible = document.get("algorithmVisible")
    if not isinstance(visible, Mapping):
        raise EngineeringError("ENVELOPE-VISIBLE-MISSING", "algorithm-visible mapping is required")
    leaked = EVALUATOR_KEYS.intersection(visible)
    if leaked:
        raise EngineeringError("EVALUATOR-FIELD-IN-ALGORITHM-VISIBLE", f"evaluator field leaked into algorithm-visible: {sorted(leaked)[0]}")
    _reject_evaluator_nested(visible)
    errors = sorted(_validator().iter_errors(document), key=lambda item: list(item.path))
    if errors:
        raise EngineeringError("ENVELOPE-SCHEMA-INVALID", errors[0].message)
    expected = compute_fingerprint(visible)
    if visible.get("fingerprintSha256") != expected:
        raise EngineeringError("FINGERPRINT-MISMATCH", "algorithm-visible fingerprint does not match the canonical payload")
    identities = visible.get("identities")
    if not isinstance(identities, Mapping):
        raise EngineeringError("ENVELOPE-IDENTITY-MISSING", "identities are required")
    for key in ("scenario", "implementation", "authorityCommit", "runId"):
        if not identities.get(key):
            raise EngineeringError("ENVELOPE-IDENTITY-INCOMPLETE", f"missing identity field {key}")
    journal = visible.get("journal")
    if not isinstance(journal, Mapping) or "events" not in journal:
        raise EngineeringError("ENVELOPE-JOURNAL-MISSING", "ordered public journal is required")
    reset = document.get("evaluatorAudit", {}).get("reset") if isinstance(document.get("evaluatorAudit"), Mapping) else None
    if not isinstance(reset, Mapping) or not reset.get("resetId"):
        raise EngineeringError("ENVELOPE-RESET-IDENTITY-MISSING", "reset identity is required")
    injection = document.get("evaluatorAudit", {}).get("injection") if isinstance(document.get("evaluatorAudit"), Mapping) else None
    if isinstance(injection, Mapping) and injection.get("confirmed") is not True:
        if document.get("qualityStatus") == "VERIFIED-NORMAL":
            raise EngineeringError("UNCONFIRMED-INJECTION-NOT-NORMAL", "unconfirmed injection cannot produce verified-normal")
    if document.get("qualityStatus") not in {"ENGINEERING-RECORD-VALID", "ENGINEERING-RECORD-INCOMPLETE"}:
        raise EngineeringError("QUALITY-STATUS-INVALID", "quality status is not an engineering record grade")


def _reject_evaluator_nested(value: object) -> None:
    if isinstance(value, Mapping):
        leaked = EVALUATOR_KEYS.intersection(value)
        if leaked:
            raise EngineeringError("EVALUATOR-FIELD-IN-ALGORITHM-VISIBLE", f"evaluator field leaked into algorithm-visible: {sorted(leaked)[0]}")
        for nested in value.values():
            _reject_evaluator_nested(nested)
    elif isinstance(value, list):
        for nested in value:
            _reject_evaluator_nested(nested)


def semantic_projection(value: object) -> object:
    """Drop named replay-volatile identifiers while preserving causal fields."""

    if isinstance(value, Mapping):
        return {
            key: semantic_projection(item)
            for key, item in value.items()
            if key not in REPLAY_EXCLUDED_FIELDS
        }
    if isinstance(value, list):
        return [semantic_projection(item) for item in value]
    return value
