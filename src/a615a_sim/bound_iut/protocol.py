"""Deterministic bound-model 615A target: UPLOAD FIND/SEND/ABORT and INFORMATION.

DOWNLOAD and AFDX behaviour are refused.  This object is a SIMULATED-IUT, not a
conformance oracle or a real target.  IUT = TH / FIND-HOST; data-loader paths
are tester infrastructure.  Algorithm-visible events are protocol-layer only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Mapping

from a615a_sim.clock import (
    FIND_ANSWER_LATE_AT_S,
    FIND_ANSWER_NORMAL_AT_S,
    FIND_OBSERVATION_END_S,
    INFORMATION_OBSERVATION_END_S,
    STATUS_EXCEPTION_DELAY_S,
    SimulatedClock,
)

ALLOWED_OPERATIONS = frozenset({"FIND", "SEND", "ABORT", "INFORMATION"})
FORBIDDEN_OPERATIONS = frozenset({"DOWNLOAD", "AFDX"})

PROTOCOL_EVENT_WHITELIST = frozenset(
    {
        "FIND-REQUEST-RECEIVED",
        "FIND-ANSWER",
        "LUR-WRQ",
        "LUR-ACK",
        "STATUS",
        "WAIT",
        "CONTINUE",
        "ABORT",
        "COMPLETED",
    }
)

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
    _find_answer_at: Fraction | None = None
    _status_until: Fraction | None = None
    _lur_ack_at: Fraction | None = None
    _observation_jitter: Fraction = Fraction(0, 1)
    _find_observation_end: Fraction | None = None

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
        self.install_parameters(None)

    def install_parameters(self, parameters: Mapping[str, Any] | None) -> None:
        """Timing/presence/order hooks only.  No new protocol event names."""

        params = dict(parameters or {})

        def _frac(key: str) -> Fraction | None:
            if key not in params or params[key] is None:
                return None
            value = params[key]
            return value if isinstance(value, Fraction) else Fraction(str(value))

        self._find_answer_at = _frac("findAnswerAtS")
        self._status_until = _frac("statusSilenceUntilS")
        self._lur_ack_at = _frac("lurAckAtS")
        self._find_observation_end = _frac("findObservationEndS")
        jitter = _frac("observationJitterS")
        self._observation_jitter = jitter if jitter is not None else Fraction(0, 1)

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
        if kind not in PROTOCOL_EVENT_WHITELIST:
            raise ValueError(f"non-protocol event kind {kind}")
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
        received = self._record("FIND-REQUEST-RECEIVED", correlation_id)
        if self._fault_id == H_SINGLE_FIND_ABSENT:
            self._advance_to(self._find_observation_end or FIND_OBSERVATION_END_S)
            self._state = "FIND_ACTIVE"
            return self._visible(received)
        if self._find_answer_at is not None:
            answer_at = self._find_answer_at
        elif self._fault_id == H_SINGLE_FIND_LATE:
            answer_at = FIND_ANSWER_LATE_AT_S
        else:
            answer_at = FIND_ANSWER_NORMAL_AT_S
        self._advance_to(answer_at)
        event = self._record("FIND-ANSWER", correlation_id)
        return self._visible(event)

    def send(self, correlation_id: str) -> dict[str, Any]:
        self._require_bound("SEND")
        self.clock.advance(Fraction(1, 50))
        if self._fault_id == H_SINGLE_LUR_WITHOUT_WRQ:
            self._state = "UPLOAD_ACTIVE"
            event = self._record("LUR-ACK", correlation_id)
            return self._visible(event)
        if self._fault_id == H_SINGLE_LUR_MISSING:
            wrq = self._record("LUR-WRQ", correlation_id)
            self._state = "UPLOAD_ACTIVE"
            return self._visible(wrq)
        self._record("LUR-WRQ", correlation_id)
        if self._lur_ack_at is not None:
            self._advance_to(max(self.clock.now, self._lur_ack_at))
        self._record("LUR-ACK", correlation_id)
        if self._scene_abort:
            self._state = "ABORTED"
            event = self._record("ABORT", correlation_id)
            return self._visible(event)
        if self._scene_wait:
            self._state = "WAIT"
            self._record("WAIT", correlation_id)
            self.clock.advance(Fraction(1, 10))
            self._state = "UPLOAD_ACTIVE"
            cont = self._record("CONTINUE", correlation_id)
            return self._visible(cont)
        self._state = "UPLOAD_ACTIVE"
        self._correlation = correlation_id
        self._state = "COMPLETED"
        event = self._record("COMPLETED", correlation_id)
        return self._visible(event)

    def abort(self, correlation_id: str) -> dict[str, Any]:
        self._require_bound("ABORT")
        self.clock.advance(Fraction(1, 100))
        self._state = "ABORTED"
        event = self._record("ABORT", correlation_id)
        return self._visible(event)

    def tester_abort(self, correlation_id: str) -> dict[str, Any]:
        """Data-loader abort fallback as a tester-issued ABORT event (R1)."""

        self._advance_to(max(self.clock.now, INFORMATION_OBSERVATION_END_S))
        self._state = "ABORTED"
        event = self._record("ABORT", correlation_id)
        return self._visible(event)

    def information(self, correlation_id: str) -> dict[str, Any]:
        self._require_bound("INFORMATION")
        if self._resource_error:
            self.clock.advance(Fraction(1, 100))
            event = self._record("STATUS", correlation_id)
            return self._visible(event)
        key = self._correlation if (self._reuse_key and self._correlation) else correlation_id
        if self._reuse_key and self._correlation and key == self._correlation:
            self.clock.advance(Fraction(1, 100))
            event = self._record("STATUS", key)
            return self._visible(event)
        self.clock.advance(Fraction(1, 100))
        delay = self._record(
            "STATUS",
            correlation_id,
            exceptionDelaySeconds=str(STATUS_EXCEPTION_DELAY_S),
        )
        self._state = "INFORMATION_ACTIVE"
        self._correlation = correlation_id
        if self._fault_id == H_SINGLE_STATUS_SILENCE:
            self._advance_to(self._status_until or INFORMATION_OBSERVATION_END_S)
            return self._visible(delay)
        event = self._record("COMPLETED", correlation_id)
        return self._visible(event)

    def algorithm_visible_records(self) -> list[dict[str, Any]]:
        return [self._visible_dict(event) for event in self._events]

    def evaluator_timed_records(self) -> list[dict[str, Any]]:
        """Exact ticks for the evaluator store.  Not algorithm-visible."""

        return [
            {
                "kind": event.kind,
                "correlationId": event.correlation_id,
                "tick": str(event.tick),
                "payload": dict(event.payload),
                "label": "EVALUATOR-ONLY",
            }
            for event in self._events
        ]

    def _visible(self, event: ProtocolEvent) -> dict[str, Any]:
        record = self._visible_dict(event)
        self._last_visible = record
        return record

    def _visible_dict(self, event: ProtocolEvent) -> dict[str, Any]:
        interval = self.clock.observation_interval(event.tick)
        return {
            "kind": event.kind,
            "correlationId": None if self._corrupt_observation else event.correlation_id,
            "observationInterval": {
                "lower": str(interval.lower + self._observation_jitter),
                "upper": str(interval.upper + self._observation_jitter),
                "unit": self.clock.unit,
            },
            "payload": dict(event.payload),
            "label": "SIMULATED-IUT",
        }
