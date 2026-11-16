"""Recompute source, code, journal, cost and history relations."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from cltav_615a_adapter.contract import ACTION_IDS, load_hb_session_contract

from .envelope import compute_fingerprint, semantic_projection, validate_envelope
from .errors import EngineeringError
from .identity import implementation_identities, require_repository, scenario_identity, verify_authority_commit
from .jsonutil import canonical_json_bytes, load_json_mapping

ALGORITHM_DIR = "algorithm-visible"
EVALUATOR_DIR = "evaluator-audit"
SPLIT_FILES = {
    Path(ALGORITHM_DIR) / "identities.json": ("algorithmVisible", "identities"),
    Path(ALGORITHM_DIR) / "configuration.json": ("algorithmVisible", "configuration"),
    Path(ALGORITHM_DIR) / "journal.json": ("algorithmVisible", "journal"),
    Path(ALGORITHM_DIR) / "rounds.json": ("algorithmVisible", "rounds"),
    Path(ALGORITHM_DIR) / "stop.json": ("algorithmVisible", "stop"),
    Path(ALGORITHM_DIR) / "recompute.json": ("algorithmVisible", "recompute"),
    Path(ALGORITHM_DIR) / "unevaluated.json": ("algorithmVisible", "unevaluatedObligations"),
    Path(ALGORITHM_DIR) / "fingerprint.json": None,
    Path(EVALUATOR_DIR) / "fault.json": ("evaluatorAudit", "faultPlan"),
    Path(EVALUATOR_DIR) / "reset.json": ("evaluatorAudit", "reset"),
    Path(EVALUATOR_DIR) / "injection.json": ("evaluatorAudit", "injection"),
    Path(EVALUATOR_DIR) / "limitations.json": ("evaluatorAudit", "limitations"),
    Path(EVALUATOR_DIR) / "delivery-withhold.json": ("evaluatorAudit", "deliveryWithhold"),
}
ALLOWED_ROOT_FILES = frozenset({"envelope.json", "manifest.json"})


def load_evidence_directory(path: Path) -> dict[str, Any]:
    envelope = path / "envelope.json"
    if not envelope.is_file():
        raise EngineeringError("EVIDENCE-READ-ERROR", "evidence envelope.json is missing")
    document = load_json_mapping(envelope.read_bytes(), code="EVIDENCE-READ-ERROR")
    visible_dir = path / ALGORITHM_DIR
    audit_dir = path / EVALUATOR_DIR
    if not audit_dir.is_dir() or not visible_dir.is_dir():
        raise EngineeringError("EVIDENCE-LAYOUT-INVALID", "algorithm-visible and evaluator-audit directories are required")
    if (visible_dir / "identities.json").is_file():
        leaked = _scan_for_evaluator(load_json_mapping((visible_dir / "identities.json").read_bytes(), code="EVIDENCE-READ-ERROR"))
        if leaked:
            raise EngineeringError("EVALUATOR-FIELD-IN-ALGORITHM-VISIBLE", leaked)
    return document


def _scan_for_evaluator(value: Mapping[str, Any]) -> str | None:
    from .envelope import EVALUATOR_KEYS

    for key in value:
        if key in EVALUATOR_KEYS:
            return key
    return None


def verify_evidence_directory(
    path: Path,
    *,
    repository: Path,
    authority_commit: str,
) -> dict[str, Any]:
    document = load_evidence_directory(path)
    verified = verify_document(
        document,
        repository=repository,
        authority_commit=authority_commit,
        rerun=True,
    )
    _assert_directory_closure(path, document)
    return verified


def verify_document(
    document: Mapping[str, Any],
    *,
    repository: Path,
    authority_commit: str,
    rerun: bool = True,
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
    if recorded_impl != live_impl:
        raise EngineeringError("IMPLEMENTATION-IDENTITY-MISMATCH", "loaded object/adapter/runtime/engineering identity does not recompute")
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
    _assert_event_identities_and_order(visible["journal"])
    _assert_resource_recompute(document, repository=repo)
    _assert_hypothesis_monotone(rounds, visible["stop"])
    _assert_actions_and_terminal(rounds, visible["stop"])
    audit = document.get("evaluatorAudit")
    if not isinstance(audit, Mapping):
        raise EngineeringError("EVALUATOR-AUDIT-MISSING", "evaluator audit is required")
    reset = audit.get("reset")
    if not isinstance(reset, Mapping) or reset.get("resetId") != journal[0].get("resetId"):
        raise EngineeringError("RESET-EVIDENCE-MISMATCH", "reset identity does not match the public journal")
    _assert_reset_attempt_binding(visible["journal"], reset)
    _assert_variant_journal(document)
    if rerun:
        _assert_rereun_semantic(document, repository=repo, authority_commit=commit)
    return dict(document)


def _assert_directory_closure(root: Path, document: Mapping[str, Any]) -> None:
    expected = {root / path for path in SPLIT_FILES} | {root / name for name in ALLOWED_ROOT_FILES}
    actual = {path for path in root.rglob("*") if path.is_file()}
    extra = actual - expected
    missing = expected - actual
    if extra or missing:
        raise EngineeringError("EVIDENCE-LAYOUT-INVALID", "evidence directory files do not match the closed layout")
    visible = document["algorithmVisible"]
    audit = document["evaluatorAudit"]
    for relative, locator in SPLIT_FILES.items():
        raw = (root / relative).read_bytes()
        if locator is None:
            expected_bytes = canonical_json_bytes({"fingerprintSha256": visible["fingerprintSha256"]})
        elif locator[0] == "algorithmVisible":
            expected_bytes = canonical_json_bytes(visible[locator[1]])
        elif locator[1] == "limitations":
            expected_bytes = canonical_json_bytes(audit["truthLimitations"])
        else:
            expected_bytes = canonical_json_bytes(audit[locator[1]])
        if raw != expected_bytes:
            raise EngineeringError("EVIDENCE-SPLIT-MISMATCH", f"{relative.as_posix()} does not match the envelope")


def _library_charges(action: Mapping[str, Any]) -> dict[str, int]:
    declared = action["cost"]
    return {
        "acquisition": int(declared["acquisition"]),
        "computation": int(declared["computation"]),
        "preparation": int(declared["preparation"]),
        "retry": int(declared["retry"]),
        "recovery": 0,
    }


def _assert_resource_recompute(document: Mapping[str, Any], *, repository: Path) -> None:
    contract = load_hb_session_contract(repository)
    visible = document["algorithmVisible"]
    mode = visible["configuration"]["resourceMode"]
    remaining = visible["configuration"]["resourceRemainingInitial"]
    if mode not in {"ROUNDS", "BUDGET"}:
        raise EngineeringError("RESOURCE-MODE-INVALID", "resource mode must be ROUNDS or BUDGET")
    for item in visible["rounds"]:
        if not isinstance(item, Mapping):
            raise EngineeringError("ROUNDS-MISSING", "each round must be a mapping")
        action_id = item.get("actionId")
        if action_id not in ACTION_IDS:
            raise EngineeringError("ACTION-ID-INVALID", "round action is not in the H-B action library")
        declared = _library_charges(contract.action(action_id))
        kind = contract.action(action_id)["kind"]
        if item.get("actionKind") not in {None, kind}:
            raise EngineeringError("ACTION-KIND-MISMATCH", "round action kind does not match the H-B library")
        expected_charges = {key: value for key, value in declared.items() if key != "recovery"}
        recorded_remaining = item.get("resourceRemaining")
        consumed = 1 if mode == "ROUNDS" else max(1, sum(declared.values()))
        charged = recorded_remaining == remaining - consumed
        uncharged = recorded_remaining == remaining
        if not charged and not uncharged:
            raise EngineeringError("RESOURCE-RECOMPUTE-MISMATCH", "resource remaining does not recompute from charged library costs")
        if charged:
            projected = dict(item.get("projectedCost") or {})
            details = dict(item.get("detailCharges") or {})
            projected_view = {key: projected.get(key, 0) for key in expected_charges}
            details_view = {key: details.get(key, 0) for key in expected_charges} if details else expected_charges
            if projected_view != expected_charges or details_view != expected_charges:
                raise EngineeringError("COST-LIBRARY-MISMATCH", "round cost does not recompute from the H-B action library")
            remaining = recorded_remaining
        elif item.get("chargedOnce") and item.get("stopReason") is None:
            raise EngineeringError("RESOURCE-RECOMPUTE-MISMATCH", "a charged non-terminal round did not consume library cost")


def _assert_hypothesis_monotone(rounds: list[Any], stop: Mapping[str, Any]) -> None:
    previous: set[str] | None = None
    for item in rounds:
        current = set((item.get("historyStatuses") or {}).keys()) or set(item.get("hypotheses") or ())
        if not current:
            raise EngineeringError("HYPOTHESIS-EMPTY", "a round cannot drop the hypothesis set to empty except by a named stop")
        if previous is not None and not current <= previous:
            raise EngineeringError("HYPOTHESIS-MONOTONE-VIOLATION", "H must contract by intersection and cannot gain members")
        previous = current
    if previous is None or set(stop.get("hypotheses") or ()) != previous:
        raise EngineeringError("HYPOTHESIS-STOP-MISMATCH", "stop hypotheses must equal the final round set")
    reason = stop.get("reason")
    if reason == "Stop-Singleton" and len(previous) != 1:
        raise EngineeringError("STOP-HYPOTHESIS-INCOMPATIBLE", "Stop-Singleton requires a singleton H")
    if reason == "Stop-Prediction-Gap":
        statuses = set((stop.get("historyStatuses") or {}).values())
        if statuses != {"CONSERVATIVE-UNKNOWN"}:
            raise EngineeringError("STOP-HYPOTHESIS-INCOMPATIBLE", "Stop-Prediction-Gap must retain conservative members")


def _assert_actions_and_terminal(rounds: list[Any], stop: Mapping[str, Any]) -> None:
    versions = [item.get("historyVersion") for item in rounds if isinstance(item, Mapping)]
    if versions != sorted(versions):
        raise EngineeringError("HISTORY-VERSION-ORDER", "history versions are not nondecreasing")
    stopped = False
    for index, item in enumerate(rounds):
        if stopped:
            raise EngineeringError("POST-STOP-ROUND", "a round was recorded after a terminal stop")
        if item.get("stopReason"):
            stopped = True
            if index != len(rounds) - 1:
                raise EngineeringError("POST-STOP-ROUND", "a round was recorded after a terminal stop")
    if stop.get("reason") and rounds[-1].get("stopReason") not in {stop.get("reason"), None}:
        raise EngineeringError("STOP-REASON-ROUND-MISMATCH", "final round stop does not match the envelope stop")


def _assert_event_identities_and_order(journal: Mapping[str, Any]) -> None:
    events = journal["events"]
    if events[0].get("kind") != "LIST-SUBMISSION-PRECONDITION-RECORDED":
        raise EngineeringError("JOURNAL-PRECONDITION-MISSING", "the public journal must begin at the list-submission preparation boundary")
    reset_id = journal.get("resetId") or events[0].get("resetId")
    attempt_id = journal.get("attemptId") or events[0].get("attemptId")
    session_id = journal.get("sessionId") or events[0].get("sessionId")
    previous_tick = -1
    previous_sequence = None
    for index, event in enumerate(events):
        if event.get("resetId") != reset_id or event.get("attemptId") != attempt_id or event.get("sessionId") != session_id:
            raise EngineeringError("JOURNAL-IDENTITY-DRIFT", "reset/attempt/session identities are not constant in the journal")
        sequence = event.get("sequenceNumber")
        if type(sequence) is not int:
            raise EngineeringError("JOURNAL-SEQUENCE-INVALID", "event sequenceNumber must be an integer")
        if previous_sequence is None:
            if sequence not in {0, 1}:
                raise EngineeringError("JOURNAL-SEQUENCE-INVALID", "event sequenceNumber must start at 0 or 1")
        elif sequence != previous_sequence + 1:
            raise EngineeringError("JOURNAL-SEQUENCE-GAP", "event sequenceNumber must increase by one")
        previous_sequence = sequence
        tick = event.get("tick")
        if type(tick) is not int or tick < previous_tick:
            raise EngineeringError("JOURNAL-TICK-ORDER", "event ticks must be nondecreasing integers")
        previous_tick = tick
        if index != sequence and not (events[0].get("sequenceNumber") == 1 and sequence == index + 1):
            if sequence != index and sequence != index + events[0].get("sequenceNumber", 0):
                pass


def _assert_reset_attempt_binding(journal: Mapping[str, Any], reset: Mapping[str, Any]) -> None:
    events = journal["events"]
    reset_id = events[0]["resetId"]
    attempt_id = events[0]["attemptId"]
    if reset.get("resetId") != reset_id or reset.get("attemptId") != attempt_id:
        raise EngineeringError("RESET-EVIDENCE-MISMATCH", "audit reset/attempt does not match the journal")
    reset_prefix = str(reset_id).split(":")[0]
    attempt_prefix = str(attempt_id).split(":")[0]
    if not reset_prefix or reset_prefix != attempt_prefix:
        raise EngineeringError("RESET-IDENTITY-INCONSISTENT", "reset and attempt identities do not share a run prefix")
    if ":reset-" not in str(reset_id) or ":attempt-" not in str(attempt_id):
        raise EngineeringError("RESET-IDENTITY-INCONSISTENT", "reset/attempt identities are not the controller epoch form")


def _assert_rereun_semantic(
    document: Mapping[str, Any],
    *,
    repository: Path,
    authority_commit: str,
) -> None:
    from .runner import run_case

    visible = document["algorithmVisible"]
    replayed = run_case(
        repository=repository,
        authority_commit=authority_commit,
        case_id=visible["identities"]["caseId"],
        resource_mode=visible["configuration"]["resourceMode"],
        resource_remaining=visible["configuration"]["resourceRemainingInitial"],
    )
    compare_semantic(document, replayed.document)

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
    if set(left["stop"]["hypotheses"]) != set(right["stop"]["hypotheses"]):
        raise EngineeringError("REPLAY-HYPOTHESIS-MISMATCH", "replayed hypothesis set differs")
    if semantic_projection(left["rounds"]) != semantic_projection(right["rounds"]):
        raise EngineeringError("REPLAY-ROUND-MISMATCH", "replayed semantic round fields differ")
