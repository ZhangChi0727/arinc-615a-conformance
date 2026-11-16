"""Recompute source, code, journal, cost and history relations."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .envelope import compute_fingerprint, semantic_projection, validate_envelope
from .errors import EngineeringError
from .identity import implementation_identities, require_repository, scenario_identity, verify_authority_commit
from .jsonutil import load_json_mapping


def load_evidence_directory(path: Path) -> dict[str, Any]:
    envelope = path / "envelope.json"
    if not envelope.is_file():
        raise EngineeringError("EVIDENCE-READ-ERROR", "evidence envelope.json is missing")
    document = load_json_mapping(envelope.read_bytes(), code="EVIDENCE-READ-ERROR")
    visible_dir = path / "algorithm-visible"
    audit_dir = path / "evaluator-audit"
    if visible_dir.exists():
        leaked = _scan_for_evaluator(load_json_mapping((visible_dir / "identities.json").read_bytes(), code="EVIDENCE-READ-ERROR") if (visible_dir / "identities.json").is_file() else {})
        if leaked:
            raise EngineeringError("EVALUATOR-FIELD-IN-ALGORITHM-VISIBLE", leaked)
    if not audit_dir.is_dir() or not visible_dir.is_dir():
        raise EngineeringError("EVIDENCE-LAYOUT-INVALID", "algorithm-visible and evaluator-audit directories are required")
    return document


def _scan_for_evaluator(value: Mapping[str, Any]) -> str | None:
    from .envelope import EVALUATOR_KEYS

    for key in value:
        if key in EVALUATOR_KEYS:
            return key
    return None


def verify_document(
    document: Mapping[str, Any],
    *,
    repository: Path,
    authority_commit: str,
) -> dict[str, Any]:
    validate_envelope(document)
    repo = require_repository(repository)
    commit = verify_authority_commit(repo, authority_commit)
    recorded_commit = document["algorithmVisible"]["identities"].get("authorityCommit")
    if recorded_commit != commit:
        raise EngineeringError("AUTHORITY-COMMIT-MISMATCH", "evidence authority commit does not match the CLI argument")
    expected_scenario = scenario_identity(repo)
    recorded_scenario = document["algorithmVisible"]["identities"].get("scenario")
    if recorded_scenario != expected_scenario:
        raise EngineeringError("SCENARIO-IDENTITY-MISMATCH", "H-B scenario identity does not recompute")
    recorded_impl = document["algorithmVisible"]["identities"].get("implementation")
    live_impl = implementation_identities()
    if recorded_impl.get("adapterSource") != live_impl["adapterSource"]:
        raise EngineeringError("ADAPTER-IDENTITY-MISMATCH", "loaded adapter identity does not match the evidence")
    if recorded_impl.get("objectSource") != live_impl["objectSource"]:
        raise EngineeringError("OBJECT-IDENTITY-MISMATCH", "loaded object identity does not match the evidence")
    visible = document["algorithmVisible"]
    if compute_fingerprint(visible) != visible.get("fingerprintSha256"):
        raise EngineeringError("FINGERPRINT-MISMATCH", "refreshed fingerprint still does not match a tampered payload")
    rounds = visible.get("rounds")
    if not isinstance(rounds, list) or not rounds:
        raise EngineeringError("ROUNDS-MISSING", "ordered runtime rounds are required")
    journal = visible["journal"]["events"]
    if not journal:
        raise EngineeringError("JOURNAL-EMPTY", "public journal events are required")
    _assert_event_directions(journal)
    versions = [item.get("historyVersion") for item in rounds if isinstance(item, Mapping)]
    if versions != sorted(versions):
        raise EngineeringError("HISTORY-VERSION-ORDER", "history versions are not nondecreasing")
    remaining = [item.get("resourceRemaining") for item in rounds if isinstance(item, Mapping)]
    if any(not isinstance(value, int) or value < 0 for value in remaining):
        raise EngineeringError("RESOURCE-RECOMPUTE-INVALID", "resource remaining cannot be recomputed as a nonnegative integer")
    audit = document.get("evaluatorAudit")
    if not isinstance(audit, Mapping):
        raise EngineeringError("EVALUATOR-AUDIT-MISSING", "evaluator audit is required")
    reset = audit.get("reset")
    if not isinstance(reset, Mapping) or reset.get("resetId") != journal[0].get("resetId"):
        raise EngineeringError("RESET-EVIDENCE-MISMATCH", "reset identity does not match the public journal")
    _assert_variant_journal(document)
    return dict(document)


_KIND_DIRECTIONS = {
    "EV_DL_WRQ_LUR": "DL-TO-TH",
    "EV_DL_DATA_LUR": "DL-TO-TH",
    "EV_TH_ACK_LUR": "TH-TO-DL",
    "EV_TH_LUS_READY": "TH-TO-DL",
    "EV_TH_LUS0001": "TH-TO-DL",
}


def _assert_event_directions(events: list[Any]) -> None:
    for event in events:
        if not isinstance(event, Mapping):
            raise EngineeringError("JOURNAL-EVENT-MALFORMED", "journal event must be a mapping")
        expected = _KIND_DIRECTIONS.get(event.get("kind"))
        if expected is not None and event.get("direction") != expected:
            raise EngineeringError("EVENT-DIRECTION-MISMATCH", "public event direction does not match its kind")


def _assert_variant_journal(document: Mapping[str, Any]) -> None:
    kinds = [item.get("kind") for item in document["algorithmVisible"]["journal"]["events"]]
    injection = document["evaluatorAudit"].get("injection")
    if not isinstance(injection, Mapping):
        raise EngineeringError("INJECTION-EVIDENCE-MISSING", "injection evidence is required")
    variant = injection.get("requestedVariant")
    if variant == "EARLY-WRQ" and injection.get("confirmed") is True:
        wrq = next((index for index, kind in enumerate(kinds) if kind == "EV_DL_WRQ_LUR"), None)
        ready = next((index for index, kind in enumerate(kinds) if kind in {"EV_TH_LUS_READY", "EV_TH_LUS0001"}), None)
        if wrq is None or (ready is not None and wrq > ready):
            raise EngineeringError("FAULT-READBACK-MISMATCH", "EARLY-WRQ injection is not supported by the public journal")
    if variant == "EARLY-DATA" and injection.get("confirmed") is True:
        data = next((index for index, kind in enumerate(kinds) if kind == "EV_DL_DATA_LUR"), None)
        ack = next((index for index, kind in enumerate(kinds) if kind == "EV_TH_ACK_LUR"), None)
        if data is None or (ack is not None and data > ack):
            raise EngineeringError("FAULT-READBACK-MISMATCH", "EARLY-DATA injection is not supported by the public journal")


def compare_semantic(expected: Mapping[str, Any], actual: Mapping[str, Any]) -> None:
    left = semantic_projection(expected["algorithmVisible"])
    right = semantic_projection(actual["algorithmVisible"])
    if left["stop"]["reason"] != right["stop"]["reason"]:
        raise EngineeringError("REPLAY-STOP-MISMATCH", "replayed stop reason differs")
    if [item.get("actionId") for item in left["rounds"]] != [item.get("actionId") for item in right["rounds"]]:
        raise EngineeringError("REPLAY-ACTION-MISMATCH", "replayed action sequence differs")
    if [item.get("kind") for item in left["journal"]["events"]] != [item.get("kind") for item in right["journal"]["events"]]:
        raise EngineeringError("REPLAY-JOURNAL-MISMATCH", "replayed public event kinds differ")
    if left["stop"]["historyStatuses"] != right["stop"]["historyStatuses"]:
        raise EngineeringError("REPLAY-HISTORY-MISMATCH", "replayed conservative history statuses differ")
    if semantic_projection(left["rounds"]) != semantic_projection(right["rounds"]):
        raise EngineeringError("REPLAY-ROUND-MISMATCH", "replayed semantic round fields differ")
