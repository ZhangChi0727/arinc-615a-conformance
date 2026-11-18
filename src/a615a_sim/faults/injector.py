"""Fault injector driven by a declared single-fault plan (IF-EXP-INJECT)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping
from uuid import uuid4

from a615a_sim.bound_iut.protocol import SimulatedTarget
from a615a_sim.clock import (
    FIND_ANSWER_LATE_AT_S,
    FIND_HOST_ANSWER_S,
    FIND_OBSERVATION_END_S,
    INFORMATION_OBSERVATION_END_S,
    declared_observation_end,
)
from a615a_sim.faults.catalogue import (
    canonical_fault_id,
    declared_signature,
    entry_by_id,
    require_applicable,
)


@dataclass(frozen=True)
class InjectionAttempt:
    scene_id: str
    attempt_id: str
    fault_id: str
    injection_confirmed: bool
    injection_unconfirmed: bool
    producer: str = "IF-EXP-INJECT"
    observed_signature: str | None = None
    declared_signature: str | None = None

    def as_mapping(self) -> Mapping[str, Any]:
        return {
            "sceneId": self.scene_id,
            "attemptId": self.attempt_id,
            "faultId": self.fault_id,
            "injectionConfirmed": self.injection_confirmed,
            "injectionUnconfirmed": self.injection_unconfirmed,
            "producer": self.producer,
            "observedSignature": self.observed_signature,
            "declaredSignature": self.declared_signature,
            "label": "SIMULATED-IUT",
        }


def _kinds(target: SimulatedTarget) -> set[str]:
    return {event.kind for event in target.events}


def _observe_signature(target: SimulatedTarget, fault_id: str) -> str | None:
    kinds = _kinds(target)
    visible = target._last_visible or {}
    canonical = canonical_fault_id(fault_id)
    answers = [event for event in target.events if event.kind == "FIND-ANSWER"]
    wrq = any(event.kind == "LUR-WRQ" for event in target.events)
    ack = any(event.kind == "LUR-ACK" for event in target.events)
    statuses = [event for event in target.events if event.kind == "STATUS"]
    if canonical in {"H-NORMAL"}:
        late_answer = any(
            event.tick > FIND_HOST_ANSWER_S for event in answers
        )
        silence = (
            statuses
            and target.clock.now >= INFORMATION_OBSERVATION_END_S
            and not any(event.kind == "COMPLETED" for event in target.events)
        )
        if late_answer or (not answers and any(event.kind == "FIND-REQUEST-RECEIVED" for event in target.events) and target.clock.now >= FIND_OBSERVATION_END_S):
            return None
        if wrq and not ack:
            return None
        if ack and not wrq:
            return None
        if silence:
            return None
        return "H-NORMAL"
    if canonical == "F-FIND-ANSWER-LATE":
        late = [
            event
            for event in answers
            if FIND_HOST_ANSWER_S < event.tick < FIND_OBSERVATION_END_S
            and event.tick == FIND_ANSWER_LATE_AT_S
        ]
        return "FIND-ANSWER-LATE" if late else None
    if canonical == "F-FIND-ANSWER-ABSENT":
        requested = any(event.kind == "FIND-REQUEST-RECEIVED" for event in target.events)
        halted = target.clock.now == declared_observation_end("FIND")
        return "FIND-ANSWER-ABSENT" if requested and not answers and halted else None
    if canonical == "F-LUR-ACK-MISSING":
        return "LUR-ACK-MISSING" if wrq and not ack else None
    if canonical == "F-LUR-ACK-WITHOUT-WRQ":
        return "LUR-ACK-WITHOUT-WRQ" if ack and not wrq else None
    if canonical == "F-STATUS-SILENCE":
        delayed = any(event.payload.get("exceptionDelaySeconds") == "10" for event in statuses)
        follow_on_status = len(statuses) > 1
        tester_abort = any(event.kind == "ABORT" for event in target.events)
        at_end = target.clock.now >= INFORMATION_OBSERVATION_END_S
        return "STATUS-SILENCE" if delayed and not follow_on_status and tester_abort and at_end else None
    if canonical == "H-SAME-KEY":
        ids = [event.correlation_id for event in target.events if event.kind == "STATUS"]
        return "REUSED-KEY" if len(ids) >= 2 and len(set(ids)) == 1 else None
    if canonical == "H-INVALID-OBS":
        return "MISSING-CORRELATION" if visible.get("correlationId") is None else None
    if canonical == "H-RESOURCE-ERROR":
        only_status = kinds <= {"STATUS"} and "STATUS" in kinds
        return "RESOURCE-ERROR" if only_status and not any(
            event.payload.get("exceptionDelaySeconds") for event in statuses
        ) else None
    return None


def _drive_for_confirmation(
    target: SimulatedTarget, fault_id: str, scene_id: str, correlation_id: str
) -> None:
    canonical = canonical_fault_id(fault_id)
    information_scenes = {
        "SC-NO-RESPONSE",
        "SC-SAME-KEY",
        "SC-INVALID-OBS",
        "SC-RESOURCE-ERROR",
    }
    if canonical == "H-NORMAL":
        if scene_id in information_scenes:
            target.information(correlation_id)
            return
        target.find(correlation_id)
        target.send(correlation_id)
        return
    if canonical in {
        "F-FIND-ANSWER-LATE",
        "F-FIND-ANSWER-ABSENT",
        "F-LUR-ACK-MISSING",
        "F-LUR-ACK-WITHOUT-WRQ",
    }:
        target.find(correlation_id)
        if canonical in {"F-LUR-ACK-MISSING", "F-LUR-ACK-WITHOUT-WRQ"}:
            target.send(correlation_id)
        return
    if canonical == "F-STATUS-SILENCE":
        target.information(correlation_id)
        target.tester_abort(correlation_id)
        return
    if canonical == "H-SAME-KEY":
        target.information(correlation_id)
        target.information(correlation_id + "-b")
        return
    if canonical in {"H-INVALID-OBS", "H-RESOURCE-ERROR"}:
        target.information(correlation_id)
        return
    raise KeyError(canonical)


def overlay_declared_fault(
    target: SimulatedTarget, *, scene_id: str, fault_id: str
) -> None:
    """Install scene and fault overlay without driving confirmation traces."""

    canonical = canonical_fault_id(fault_id)
    require_applicable(scene_id, canonical)
    overlay = None if canonical == "H-NORMAL" else canonical
    target.install_scene(scene_id)
    target.install_fault(overlay)


def inject(
    target: SimulatedTarget,
    *,
    scene_id: str,
    fault_id: str,
    attempt_id: str | None = None,
    confirm: bool = True,
    truth_store: Any | None = None,
    truth_capability: Any | None = None,
) -> InjectionAttempt:
    """Overlay one declared fault on an applicable scene.  Planned is not confirmed."""

    require_applicable(scene_id, fault_id)
    canonical = canonical_fault_id(fault_id)
    attempt = attempt_id or f"A-{uuid4().hex[:12]}"
    overlay_declared_fault(target, scene_id=scene_id, fault_id=canonical)
    observed = None
    if confirm:
        _drive_for_confirmation(
            target, canonical, scene_id, correlation_id=f"corr-{attempt}"
        )
        observed = _observe_signature(target, canonical)
    declared = declared_signature(canonical)
    token = str(entry_by_id(canonical)["confirmationToken"])
    confirmed = bool(confirm and observed == token)
    record = InjectionAttempt(
        scene_id=scene_id,
        attempt_id=attempt,
        fault_id=canonical,
        injection_confirmed=confirmed,
        injection_unconfirmed=not confirmed,
        observed_signature=observed,
        declared_signature=declared,
    )
    if truth_store is not None:
        truth_store.write_from_confirmed_injection(record, truth_capability)
    return record
