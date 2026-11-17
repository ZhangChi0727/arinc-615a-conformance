"""Fault injector driven by a declared single-fault plan (IF-EXP-INJECT)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping
from uuid import uuid4

from a615a_sim.bound_iut.protocol import SimulatedTarget
from a615a_sim.faults.catalogue import declared_signature, entry_by_id


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


def _observe_signature(target: SimulatedTarget, fault_id: str) -> str | None:
    kinds = {event.kind for event in target.events}
    visible = target._last_visible or {}
    if fault_id == "H-NORMAL":
        return "COMPLETED" if "COMPLETED" in kinds and "FIND" in kinds else None
    if fault_id == "H-WAIT-CONTINUE":
        return "WAIT+CONTINUE" if {"WAIT", "CONTINUE"} <= kinds else None
    if fault_id == "H-NO-RESPONSE":
        return "NO-RESPONSE" if "NO-RESPONSE" in kinds and "STATUS-WITH-DELAY" in kinds else None
    if fault_id == "H-ABORT":
        return "ABORT" if "ABORT" in kinds else None
    if fault_id == "H-SAME-KEY":
        reused = [event for event in target.events if event.payload.get("reusedKey")]
        return "REUSED-KEY" if reused else None
    if fault_id == "H-SINGLE-BATCH":
        return "BATCH" if target.configuration == "BATCH" else None
    if fault_id == "H-INVALID-OBS":
        return "MISSING-CORRELATION" if visible.get("correlationId") is None else None
    if fault_id == "H-RESOURCE-ERROR":
        return "RESOURCE-ERROR" if "RESOURCE-ERROR" in kinds else None
    return None


def _drive_for_confirmation(target: SimulatedTarget, fault_id: str, correlation_id: str) -> None:
    if fault_id in {"H-NORMAL", "H-WAIT-CONTINUE", "H-ABORT", "H-SINGLE-BATCH"}:
        target.find(correlation_id)
        target.send(correlation_id)
        return
    if fault_id == "H-NO-RESPONSE":
        target.information(correlation_id)
        return
    if fault_id == "H-SAME-KEY":
        target.information(correlation_id)
        target.information(correlation_id + "-b")
        return
    if fault_id == "H-INVALID-OBS":
        target.information(correlation_id)
        return
    if fault_id == "H-RESOURCE-ERROR":
        target.information(correlation_id)
        return
    raise KeyError(fault_id)


def inject(
    target: SimulatedTarget,
    *,
    scene_id: str,
    fault_id: str,
    attempt_id: str | None = None,
    confirm: bool = True,
) -> InjectionAttempt:
    """Install one declared fault.  Planned is not confirmed until the signature is seen."""

    entry_by_id(fault_id)
    attempt = attempt_id or f"A-{uuid4().hex[:12]}"
    target.install_fault(fault_id)
    observed = None
    if confirm:
        _drive_for_confirmation(target, fault_id, correlation_id=f"corr-{attempt}")
        observed = _observe_signature(target, fault_id)
    declared = declared_signature(fault_id)
    token = str(entry_by_id(fault_id)["confirmationToken"])
    confirmed = bool(confirm and observed == token)
    return InjectionAttempt(
        scene_id=scene_id,
        attempt_id=attempt,
        fault_id=fault_id,
        injection_confirmed=confirmed,
        injection_unconfirmed=not confirmed,
        observed_signature=observed,
        declared_signature=declared,
    )
