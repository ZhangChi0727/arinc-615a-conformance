"""Execute one named 615A engineering case through the accepted C session."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any
from uuid import uuid4

from cltav_615a.controller import LurStartController
from cltav_615a.objects import EVENT_TH_ACK_LUR
from cltav_615a.types import FaultVariant, PublicEvent
from cltav_615a_adapter.session import LurStartSessionEnvironment, build_lur_start_session
from cltav_runtime.session import ResourceState, SessionResult

from .envelope import UNEVALUATED_OBLIGATIONS, assemble_envelope, utc_now
from .errors import EngineeringError
from .identity import (
    implementation_identities,
    require_repository,
    scenario_identity,
    verify_authority_commit,
)

CASE_NORMAL = "ENG-CASE-NORMAL"
CASE_EARLY_WRQ = "ENG-CASE-EARLY-WRQ"
CASE_EARLY_DATA = "ENG-CASE-EARLY-DATA"
CASE_ACCESS_GAP = "ENG-CASE-ACCESS-UNKNOWN-RECOVER-GAP"
CASE_IDS = (CASE_NORMAL, CASE_EARLY_WRQ, CASE_EARLY_DATA, CASE_ACCESS_GAP)


@dataclass(frozen=True)
class EngineeringRun:
    case_id: str
    repository: Path
    authority_commit: str
    document: dict[str, Any]


def _fraction(value: Fraction | None) -> str | None:
    if value is None:
        return None
    return f"{value.numerator}/{value.denominator}"


def _event(event: PublicEvent) -> dict[str, Any]:
    return {
        "eventId": event.event_id,
        "resetId": event.reset_id,
        "attemptId": event.attempt_id,
        "sessionId": event.session_id,
        "correlationId": event.correlation_id,
        "layer": event.layer,
        "actor": event.actor,
        "receiver": event.receiver,
        "direction": event.direction,
        "kind": event.kind,
        "opcode": event.opcode,
        "fileRole": event.file_role,
        "inReplyToEventId": event.in_reply_to_event_id,
        "tick": event.tick,
        "sequenceNumber": event.sequence_number,
    }


def _round(result: SessionResult) -> dict[str, Any] | None:
    if not result.state.evidence:
        return {
            "actionId": None,
            "actionKind": None,
            "effectClass": None,
            "observable": None,
            "summaryAfter": result.state.context.current_summary,
            "qStatus": result.state.context.q_status,
            "hypotheses": sorted(result.state.history.hypotheses),
            "historyStatuses": dict(result.state.history.status_by_hypothesis),
            "historyVersion": result.state.history.version,
            "resourceMode": result.state.resources.mode,
            "resourceRemaining": result.state.resources.remaining,
            "stopReason": result.stop_reason,
            "diagnostics": [item.code for item in result.diagnostics],
            "uncertaintyIdentity": None,
            "issuedToExecutor": False,
            "chargedOnce": False,
            "detailCharges": {},
        }
    last = result.state.evidence[-1]
    return {
        "actionId": last.snapshot.action_id,
        "actionKind": last.snapshot.action_kind,
        "snapshotId": last.snapshot.snapshot_id,
        "effectClass": last.execution.effect_class,
        "observable": last.execution.observable,
        "summaryConfirmed": last.execution.summary_confirmed,
        "summaryAfter": last.summary_after,
        "qStatus": result.state.context.q_status,
        "hypotheses": sorted(last.snapshot.hypotheses),
        "historyStatuses": dict(result.state.history.status_by_hypothesis),
        "historyVersion": last.history_after.version,
        "resourceMode": result.state.resources.mode,
        "resourceRemaining": result.state.resources.remaining,
        "projectedCost": dict(last.projected_cost),
        "detailCharges": dict(last.detail_charges),
        "chargedOnce": last.charged_once,
        "issuedToExecutor": last.issued_to_executor,
        "stopReason": last.stop_reason or result.stop_reason,
        "resolutionCode": last.resolution_code,
        "uncertaintyIdentity": last.snapshot.uncertainty_identity,
        "measurementTick": _fraction(last.execution.measurement_tick),
        "diagnostics": [item.code for item in result.diagnostics],
        "executionAttemptId": last.execution.execution_attempt_id,
        "evidenceRef": last.execution.evidence_ref,
    }


def _install_variant(controller: LurStartController, case_id: str) -> dict[str, Any]:
    mapping = {
        CASE_EARLY_WRQ: FaultVariant.EARLY_WRQ,
        CASE_EARLY_DATA: FaultVariant.EARLY_DATA,
    }
    variant = mapping.get(case_id)
    if variant is None:
        return {
            "requestedVariant": "NORMAL",
            "installationStatus": "NOT-INSTALLED",
            "confirmed": False,
            "truthLimitation": "NORMAL is the default object; it is not an independently confirmed IUT truth.",
        }
    record = controller.install_fault(variant)
    return {
        "requestedVariant": variant.value,
        "installationStatus": record.status.value,
        "confirmed": record.status.value == "INSTALLED",
        "truthLimitation": (
            "Evaluator-installed surrogate variant is not independent experimental truth "
            "and is not a real-device root cause."
        ),
    }


def _attach_once_ack_withhold(environment: LurStartSessionEnvironment, shared: dict[str, bool]) -> None:
    """Instance-level one-shot tool failure; successors must be re-wrapped.

    The C adapter class is not patched.  The named withhold lives on this
    environment instance and a shared done-flag copied across `_next` results.
    """

    original = LurStartSessionEnvironment._applied_delivery

    def hooked(*, controller, request, expected, adapter_identity):
        if expected.kind == EVENT_TH_ACK_LUR and not shared["done"]:
            shared["done"] = True
            return None
        return original(
            controller=controller,
            request=request,
            expected=expected,
            adapter_identity=adapter_identity,
        )

    object.__setattr__(environment, "_applied_delivery", hooked)


def run_case(
    *,
    repository: Path,
    authority_commit: str,
    case_id: str,
    resource_mode: str,
    resource_remaining: int,
) -> EngineeringRun:
    if case_id not in CASE_IDS:
        raise EngineeringError("CASE-ID-UNKNOWN", f"unknown engineering case {case_id}")
    if resource_mode not in {"ROUNDS", "BUDGET"}:
        raise EngineeringError("RESOURCE-MODE-INVALID", "resource mode must be ROUNDS or BUDGET")
    if type(resource_remaining) is not int or resource_remaining < 1:
        raise EngineeringError("RESOURCE-REMAINING-INVALID", "resource remaining must be a positive integer")
    repo = require_repository(repository)
    commit = verify_authority_commit(repo, authority_commit)
    scenario = scenario_identity(repo)
    controller = LurStartController()
    injection = _install_variant(controller, case_id)
    resources = (
        ResourceState.rounds(resource_remaining)
        if resource_mode == "ROUNDS"
        else ResourceState.budget(resource_remaining)
    )
    built = build_lur_start_session(
        repository=repo,
        controller=controller,
        resources=resources,
        retry_cap=4,
    )
    withheld = case_id == CASE_ACCESS_GAP
    withhold_state = {"done": False}
    rounds: list[dict[str, Any]] = []
    state = built.session.initial_state
    environment = built.environment
    if withheld:
        _attach_once_ack_withhold(environment, withhold_state)
    terminal: SessionResult | None = None
    for _ in range(32):
        terminal = built.session.step(state, environment)
        encoded = _round(terminal)
        if encoded is not None:
            rounds.append(encoded)
        if terminal.stop_reason is not None:
            break
        state = terminal.state
        environment = terminal.environment
        if withheld:
            _attach_once_ack_withhold(environment, withhold_state)
    if terminal is None:
        raise EngineeringError("SESSION-DID-NOT-RUN", "the C session produced no step")
    protocol = terminal.environment.protocol_snapshot
    snapshot = {
        "resetId": protocol.reset_id,
        "attemptId": protocol.attempt_id,
        "sessionId": protocol.session_id,
        "correlationId": protocol.correlation_id,
        "events": [_event(item) for item in protocol.events],
    }
    if not snapshot["events"]:
        raise EngineeringError("JOURNAL-EMPTY", "a valid engineering record requires a public event source")
    stop_reason = terminal.stop_reason
    if case_id == CASE_ACCESS_GAP and stop_reason != "Stop-Prediction-Gap":
        raise EngineeringError(
            "ACCESS-CASE-CONTRACT-MISMATCH",
            "access-exception case must terminate at Stop-Prediction-Gap under DM-C-R01",
        )
    quality = "ENGINEERING-RECORD-VALID"
    algorithm_visible = {
            "identities": {
                "runId": f"eng-run-{uuid4().hex}",
                "sceneId": "ENG-UPLOAD-LUR-START",
                "caseId": case_id,
                "authorityCommit": commit,
                "scenario": scenario,
                "implementation": implementation_identities(),
                "engineeringPurpose": "BOUNDED-615A-CONTROL-SLICE-ENGINEERING-RECORD",
            },
            "configuration": {
                "resourceMode": resource_mode,
                "resourceRemainingInitial": resource_remaining,
                "uncertainty": {
                    "id": rounds[0].get("uncertaintyIdentity") if rounds else None,
                    "timeUnit": "ticks",
                    "maximumErrorTicks": 0,
                    "note": "Virtual engineering ticks; not a calibrated physical clock.",
                },
                "wallClockUtc": utc_now(),
            },
            "journal": snapshot,
            "rounds": rounds,
            "stop": {
                "reason": stop_reason,
                "qStatus": terminal.state.context.q_status,
                "currentSummary": terminal.state.context.current_summary,
                "hypotheses": sorted(terminal.state.history.hypotheses),
                "historyStatuses": dict(terminal.state.history.status_by_hypothesis),
                "diagnostics": [item.code for item in terminal.diagnostics],
                "dmCR01": (
                    "UNKNOWN after a qualified Recover keeps conservative H members; "
                    "the full coordinator stops at Stop-Prediction-Gap. Direct adapter "
                    "FIFO continuation remains available and is not a restored diagnostic."
                    if case_id == CASE_ACCESS_GAP else None
                ),
            },
            "recompute": {
                "rules": [
                    "Recompute source identities from the authority Git objects.",
                    "Recompute fingerprint over algorithm-visible excluding fingerprintSha256.",
                    "Replay compares semantic fields after dropping the named identifier whitelist.",
                ],
                "replayExcludedFields": sorted({
                    "runId", "attemptId", "resetId", "sessionId", "correlationId",
                    "wallClockUtc", "eventId", "executionAttemptId", "snapshotId",
                    "readbackId", "evidenceRef",
                }),
            },
        "unevaluatedObligations": list(UNEVALUATED_OBLIGATIONS),
    }
    evaluator_audit = {
        "faultPlan": {
            "caseId": case_id,
            "requestedVariant": injection["requestedVariant"],
        },
        "reset": {
            "resetId": protocol.reset_id,
            "attemptId": protocol.attempt_id,
        },
        "injection": injection,
        "truthLimitations": [
            injection["truthLimitation"],
            "CRC/check-value/naming/complete-integrity remain NOT-ESTABLISHED.",
            "This is a finite surrogate engineering loop, not IUT detection or four-arm results.",
            "DM-C-R01: full-session recovery does not promote conservative H or continue diagnosis.",
        ],
        "deliveryWithhold": (
            {"kind": EVENT_TH_ACK_LUR, "once": True, "layer": "engineering-runner"}
            if withheld else None
        ),
    }
    document = assemble_envelope(
        algorithm_visible=algorithm_visible,
        evaluator_audit=evaluator_audit,
        quality_status=quality,
    )
    return EngineeringRun(case_id, repo, commit, document)
