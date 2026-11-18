"""Deterministic bound-model 615A target: UPLOAD FIND/SEND/ABORT and INFORMATION.

DOWNLOAD and AFDX behaviour are refused.  This object is a SIMULATED-IUT, not a
conformance oracle or a real target.  IUT = TH / FIND-HOST; data-loader paths
are tester infrastructure.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any

from a615a_sim.clock import (
    DECLARED_OBSERVATION_END_S,
    FIND_ANSWER_LATE_AT_S,
    SimulatedClock,
)

ALLOWED_OPERATIONS = frozenset({"FIND", "SEND", "ABORT", "INFORMATION"})
FORBIDDEN_OPERATIONS = frozenset({"DOWNLOAD", "AFDX"})

H_SINGLE_FIND_LATE = "F-FIND-ANSWER-LATE"
H_SINGLE_FIND_ABSENT = "F-FIND-ANSWER-ABSENT"
H_SINGLE_LUR_MISSING = "F-LUR-ACK-MISSING"
H_SINGLE_LUR_WITHOUT_WRQ = "F-LUR-ACK-WITHOUT-WRQ"
H_SINGLE_STATUS_SILENCE = "F-STATUS-SILENCE"


@dataclass
class ProtocolEvent:
    kind: str
    correlation_id: str
    tick: Fraction
    payload: dict[str, Any]


@dataclass
class SimulatedTarget:
    """Process-local bound-model IUT with a single active correlation."""

    clock: SimulatedClock
    configuration: str = "SINGLE"
    _state: str = "IDLE"
    _correlation: str | None = None
    _fault_id: str | None = None
    _scene_id: str | None = None
    _events: list[ProtocolEvent] = field(default_factory=list)
    _generation: int = 0
    _corrupt_observation: bool = False
    _reuse_key: bool = False
    _resource_error: bool = False
    _scene_wait: bool = False
    _scene_abort: bool = False
    _scene_batch: bool = False
    _last_visible: dict[str, Any] | None = None

    @property
    def state(self) -> str:
        return self._state

    @property
    def events(self) -> tuple[ProtocolEvent, ...]:
        return tuple(self._events)

    def snapshot(self) -> dict[str, Any]:
        return {
            "generation": self._generation,
            "state": self._state,
            "correlation": self._correlation,
            "configuration": "BATCH" if self._scene_batch else self.configuration,
            "faultId": self._fault_id,
            "sceneId": self._scene_id,
            "clockTick": str(self.clock.now),
        }

    def install_scene(self, scene_id: str | None) -> None:
        self._scene_id = scene_id
        self._scene_wait = scene_id == "SC-WAIT-CONTINUE"
        self._scene_abort = scene_id == "SC-ABORT"
        self._scene_batch = scene_id == "SC-SINGLE-BATCH"
        if self._scene_batch:
            self.configuration = "BATCH"

    def install_fault(self, fault_id: str | None) -> None:
        self._fault_id = fault_id
        self._corrupt_observation = fault_id == "H-INVALID-OBS"
        self._reuse_key = fault_id == "H-SAME-KEY"
        self._resource_error = fault_id == "H-RESOURCE-ERROR"

    def reset(self) -> dict[str, Any]:
        self._generation += 1
        self._state = "IDLE"
        self._correlation = None
        self._events.clear()
        self._last_visible = None
        self.install_fault(None)
        self.install_scene(None)
        self.configuration = "SINGLE"
        self.clock.reset()
        return self.snapshot()

    def _record(self, kind: str, correlation_id: str, **payload: Any) -> ProtocolEvent:
        event = ProtocolEvent(kind, correlation_id, self.clock.now, payload)
        self._events.append(event)
        return event

    def _require_bound(self, operation: str) -> None:
        if operation in FORBIDDEN_OPERATIONS:
            raise ValueError(f"{operation} is outside the bound simulated IUT")
        if operation not in ALLOWED_OPERATIONS:
            raise ValueError(f"unknown operation {operation}")

    def _advance_to(self, tick: Fraction) -> None:
        if tick < self.clock.now:
            raise ValueError("clock cannot run backwards")
        delta = tick - self.clock.now
        if delta > 0:
            self.clock.advance(delta)

    def find(self, correlation_id: str) -> dict[str, Any]:
        self._require_bound("FIND")
        self._state = "FIND_ACTIVE"
        self._correlation = correlation_id
        if self._fault_id == H_SINGLE_FIND_LATE:
            self._advance_to(FIND_ANSWER_LATE_AT_S)
            event = self._record(
                "FIND-ANSWER-LATE",
                correlation_id,
                hostAnswerInWindow=False,
                afterHostDeadline=True,
                beforeObservationEnd=FIND_ANSWER_LATE_AT_S < DECLARED_OBSERVATION_END_S,
            )
            return self._visible(event)
        if self._fault_id == H_SINGLE_FIND_ABSENT:
            self._advance_to(DECLARED_OBSERVATION_END_S)
            event = self._record(
                "FIND-ANSWER-ABSENT",
                correlation_id,
                hostAnswer=False,
                haltedAtObservationEnd=True,
            )
            self._state = "HALTED"
            return self._visible(event)
        self.clock.advance(Fraction(1, 100))
        event = self._record(
            "FIND",
            correlation_id,
            hostAnswerInWindow=True,
            hostAnswerS="2",
        )
        return self._visible(event)

    def send(self, correlation_id: str) -> dict[str, Any]:
        self._require_bound("SEND")
        self.clock.advance(Fraction(1, 50))
        if self._fault_id == H_SINGLE_LUR_WITHOUT_WRQ:
            self._state = "HALTED"
            event = self._record(
                "LUR-ACK-WITHOUT-WRQ",
                correlation_id,
                matchingWrqReceived=False,
                invariant="TH-MATCHING-LUR-WRQ-RECEIVED",
            )
            return self._visible(event)
        if self._fault_id == H_SINGLE_LUR_MISSING:
            wrq = self._record("LUR-WRQ", correlation_id, matchingWrqReceived=True)
            self._state = "HALTED"
            event = self._record(
                "LUR-ACK-MISSING",
                correlation_id,
                afterWrq=wrq.kind,
                thAck=False,
            )
            return self._visible(event)
        self._record("LUR-WRQ", correlation_id, matchingWrqReceived=True)
        self._record("LUR-ACK", correlation_id, matchingWrqReceived=True)
        if self._scene_abort:
            self._state = "ABORTED"
            event = self._record("ABORT", correlation_id, owned=True, during="SEND")
            return self._visible(event)
        if self._scene_wait:
            self._state = "WAIT"
            wait = self._record("WAIT", correlation_id)
            self.clock.advance(Fraction(1, 10))
            self._state = "UPLOAD_ACTIVE"
            cont = self._record("CONTINUE", correlation_id, after=str(wait.tick))
            return self._visible(cont)
        self._state = "UPLOAD_ACTIVE"
        self._correlation = correlation_id
        event = self._record("SEND", correlation_id)
        self._state = "COMPLETED"
        self._record("COMPLETED", correlation_id)
        return self._visible(event)

    def abort(self, correlation_id: str) -> dict[str, Any]:
        self._require_bound("ABORT")
        self.clock.advance(Fraction(1, 100))
        self._state = "ABORTED"
        event = self._record("ABORT", correlation_id, owned=True)
        return self._visible(event)

    def information(self, correlation_id: str) -> dict[str, Any]:
        self._require_bound("INFORMATION")
        if self._resource_error:
            self.clock.advance(Fraction(1, 100))
            event = self._record("RESOURCE-ERROR", correlation_id, resourceStatus="RESOURCE-ERROR")
            return self._visible(event)
        key = self._correlation if (self._reuse_key and self._correlation) else correlation_id
        if self._reuse_key and self._correlation and key == self._correlation:
            self.clock.advance(Fraction(1, 100))
            event = self._record("INFORMATION", key, reusedKey=True, secondRequest=True)
            return self._visible(event)
        self.clock.advance(Fraction(1, 100))
        delay = self._record(
            "STATUS-WITH-DELAY",
            correlation_id,
            exceptionDelaySeconds="10",
            operationKey=correlation_id,
        )
        if self._fault_id == H_SINGLE_STATUS_SILENCE:
            self.clock.advance(Fraction(11, 1))
            event = self._record(
                "STATUS-SILENCE",
                correlation_id,
                afterDelay=True,
                abortFallback="AVAILABLE",
                trigger=delay.kind,
            )
            self._state = "INFORMATION_ACTIVE"
            self._correlation = correlation_id
            return self._visible(event)
        self._state = "INFORMATION_ACTIVE"
        self._correlation = correlation_id
        event = self._record("INFORMATION", correlation_id, afterDelay=True, abortFallback="AVAILABLE")
        return self._visible(event)

    def _visible(self, event: ProtocolEvent) -> dict[str, Any]:
        record = {
            "kind": event.kind,
            "correlationId": None if self._corrupt_observation else event.correlation_id,
            "tick": str(event.tick),
            "observationInterval": {
                "lower": str(self.clock.observation_interval(event.tick).lower),
                "upper": str(self.clock.observation_interval(event.tick).upper),
                "unit": self.clock.unit,
            },
            "payload": dict(event.payload),
            "state": self._state,
            "label": "SIMULATED-IUT",
        }
        self._last_visible = record
        return record
