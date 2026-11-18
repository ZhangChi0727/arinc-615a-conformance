"""Fault injector driven by a declared single-fault plan (IF-EXP-INJECT)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping
from uuid import uuid4

from a615a_sim.bound_iut.protocol import SimulatedTarget
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


_H_SINGLE_TOKENS = frozenset(
    {
        "FIND-ANSWER-LATE",
        "FIND-ANSWER-ABSENT",
        "LUR-ACK-MISSING",
        "LUR-ACK-WITHOUT-WRQ",
        "STATUS-SILENCE",
    }
)


def _observe_signature(target: SimulatedTarget, fault_id: str) -> str | None:
    kinds = {event.kind for event in target.events}
    visible = target._last_visible or {}
    canonical = canonical_fault_id(fault_id)
    if canonical in {"H-NORMAL"}:
        if kinds & _H_SINGLE_TOKENS:
            return None
        return "H-NORMAL"
    if canonical == "F-FIND-ANSWER-LATE":
        late = [event for event in target.events if event.kind == "FIND-ANSWER-LATE"]
        return "FIND-ANSWER-LATE" if late else None
    if canonical == "F-FIND-ANSWER-ABSENT":
        absent = [event for event in target.events if event.kind == "FIND-ANSWER-ABSENT"]
        host = [event for event in target.events if event.kind in {"FIND", "FIND-ANSWER-LATE"}]
        return "FIND-ANSWER-ABSENT" if absent and not host else None
    if canonical == "F-LUR-ACK-MISSING":
        wrq = any(event.kind == "LUR-WRQ" for event in target.events)
        ack = any(event.kind in {"LUR-ACK", "LUR-ACK-WITHOUT-WRQ"} for event in target.events)
        return "LUR-ACK-MISSING" if wrq and not ack and "LUR-ACK-MISSING" in kinds else None
    if canonical == "F-LUR-ACK-WITHOUT-WRQ":
        wrq = any(event.kind == "LUR-WRQ" for event in target.events)
        unmatched = any(event.kind == "LUR-ACK-WITHOUT-WRQ" for event in target.events)
        return "LUR-ACK-WITHOUT-WRQ" if unmatched and not wrq else None
    if canonical == "F-STATUS-SILENCE":
        silenced = [
            event
            for event in target.events
            if event.kind == "STATUS-SILENCE" and event.payload.get("abortFallback") == "AVAILABLE"
        ]
        delayed = "STATUS-WITH-DELAY" in kinds
        suppressed = any(
            event.payload.get("abortFallback") == "SUPPRESSED" for event in target.events
        )
        return "STATUS-SILENCE" if silenced and delayed and not suppressed else None
    if canonical == "H-SAME-KEY":
        reused = [event for event in target.events if event.payload.get("reusedKey")]
        return "REUSED-KEY" if reused else None
    if canonical == "H-INVALID-OBS":
        return "MISSING-CORRELATION" if visible.get("correlationId") is None else None
    if canonical == "H-RESOURCE-ERROR":
        return "RESOURCE-ERROR" if "RESOURCE-ERROR" in kinds else None
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
        return
    if canonical == "H-SAME-KEY":
        target.information(correlation_id)
        target.information(correlation_id + "-b")
        return
    if canonical in {"H-INVALID-OBS", "H-RESOURCE-ERROR"}:
        target.information(correlation_id)
        return
    raise KeyError(canonical)


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
    overlay = None if canonical == "H-NORMAL" else canonical
    target.install_scene(scene_id)
    target.install_fault(overlay)
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
