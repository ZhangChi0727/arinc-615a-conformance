"""Independent in-process synthetic execution environment.

The environment owns a private finite state and turns an admitted action into a
visible record.  It does not accept a hypothesis set, a prediction class,
selection score, evaluator truth or an expected outcome.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from types import MappingProxyType
from typing import Any, Mapping


@dataclass(frozen=True)
class ExecutionRequest:
    """The intentionally narrow algorithm-to-environment execution request."""

    session_id: str
    execution_attempt_id: str
    action_id: str
    action_kind: str


@dataclass(frozen=True)
class VisibleExecutionRecord:
    """Visible execution evidence; it contains no evaluator truth."""

    execution_attempt_id: str
    action_id: str
    effect_class: str
    observable: str | None
    summary_confirmed: bool
    post_summary: str | None
    measurement_tick: Fraction | None
    uncertainty_identity: str | None
    evidence_ref: str


@dataclass(frozen=True)
class EnvironmentExecution:
    record: VisibleExecutionRecord
    successor: "SyntheticEnvironment"


@dataclass(frozen=True)
class SyntheticEnvironment:
    """A finite deterministic environment with private state transitions."""

    _state: str
    _uncertainty_identity: str
    _states: Mapping[str, Mapping[str, Mapping[str, Any]]]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SyntheticEnvironment":
        if not isinstance(value, Mapping) or set(value) != {"initialPrivateState", "uncertaintyIdentity", "states"}:
            raise ValueError("synthetic environment uses unknown or missing fields")
        initial = value.get("initialPrivateState")
        uncertainty_identity = value.get("uncertaintyIdentity")
        states = value.get("states")
        if (
            not isinstance(initial, str) or not initial
            or not isinstance(uncertainty_identity, str) or not uncertainty_identity
            or not isinstance(states, Mapping) or not states
        ):
            raise ValueError("synthetic environment declaration is invalid")
        parsed: dict[str, Mapping[str, Mapping[str, Any]]] = {}
        for state_id, actions in states.items():
            if not isinstance(state_id, str) or not state_id or not isinstance(actions, Mapping) or not actions:
                raise ValueError("synthetic environment state declaration is invalid")
            parsed_actions: dict[str, Mapping[str, Any]] = {}
            for action_id, outcome in actions.items():
                if not isinstance(action_id, str) or not action_id or not isinstance(outcome, Mapping):
                    raise ValueError("synthetic environment action declaration is invalid")
                if set(outcome) != {"effectClass", "observable", "summaryConfirmed", "measurementTick", "nextPrivateState"}:
                    raise ValueError("synthetic environment outcome uses unknown or missing fields")
                effect = outcome.get("effectClass")
                observable = outcome.get("observable")
                confirmed = outcome.get("summaryConfirmed")
                measurement_tick = outcome.get("measurementTick")
                successor = outcome.get("nextPrivateState")
                if effect not in {"NONE", "CONFIRMED-NOT-SENT", "UNKNOWN-EFFECT"}:
                    raise ValueError("synthetic environment effect class is invalid")
                if observable is not None and (not isinstance(observable, str) or not observable):
                    raise ValueError("synthetic environment observable is invalid")
                if not isinstance(confirmed, bool) or not isinstance(successor, str) or not successor:
                    raise ValueError("synthetic environment outcome is invalid")
                if effect == "NONE" and (observable is None or not confirmed):
                    raise ValueError("normal synthetic outcome requires visible confirmed evidence")
                if effect == "NONE":
                    _exact_tick(measurement_tick)
                if effect != "NONE" and (observable is not None or confirmed or measurement_tick is not None):
                    raise ValueError("non-normal synthetic outcome cannot manufacture an observation")
                # Detach and normalize the actual consumer configuration.
                # A shallow proxy still aliases an input rational mapping,
                # allowing a post-construction caller mutation to change the
                # visible execution record without constructing a new
                # environment instance.
                parsed_actions[action_id] = MappingProxyType(
                    {
                        "effectClass": effect,
                        "observable": observable,
                        "summaryConfirmed": confirmed,
                        "measurementTick": _exact_tick(measurement_tick) if effect == "NONE" else None,
                        "nextPrivateState": successor,
                    },
                )
            parsed[state_id] = MappingProxyType(parsed_actions)
        if initial not in parsed:
            raise ValueError("synthetic environment initial state is undeclared")
        for actions in parsed.values():
            for outcome in actions.values():
                if outcome["nextPrivateState"] not in parsed:
                    raise ValueError("synthetic environment successor state is undeclared")
        return cls(initial, uncertainty_identity, MappingProxyType(parsed))

    def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
        """Execute an admitted request without access to algorithm internals."""

        if not isinstance(request, ExecutionRequest):
            raise ValueError("synthetic environment requires an execution request")
        if (
            not request.session_id
            or not request.execution_attempt_id
            or not request.action_id
            or request.action_kind not in {"TEST", "PREP", "RECOVER"}
        ):
            raise ValueError("synthetic execution request is invalid")
        outcome = self._states[self._state].get(request.action_id)
        if outcome is None:
            record = VisibleExecutionRecord(
                execution_attempt_id=request.execution_attempt_id,
                action_id=request.action_id,
                effect_class="CONFIRMED-NOT-SENT",
                observable=None,
                summary_confirmed=False,
                post_summary=None,
                measurement_tick=None,
                uncertainty_identity=self._uncertainty_identity,
                evidence_ref=f"synthetic:{request.execution_attempt_id}:not-sent",
            )
            return EnvironmentExecution(record, self)
        successor = SyntheticEnvironment(outcome["nextPrivateState"], self._uncertainty_identity, self._states)
        observable = outcome["observable"]
        record = VisibleExecutionRecord(
            execution_attempt_id=request.execution_attempt_id,
            action_id=request.action_id,
            effect_class=outcome["effectClass"],
            observable=observable,
            summary_confirmed=outcome["summaryConfirmed"],
            post_summary=observable if outcome["summaryConfirmed"] else None,
            measurement_tick=outcome["measurementTick"],
            uncertainty_identity=self._uncertainty_identity,
            evidence_ref=f"synthetic:{request.execution_attempt_id}:{outcome['effectClass'].lower()}",
        )
        return EnvironmentExecution(record, successor)


def _exact_tick(value: object) -> Fraction:
    if isinstance(value, int) and not isinstance(value, bool):
        return Fraction(value)
    if isinstance(value, Mapping) and set(value) == {"numerator", "positiveDenominator"}:
        numerator = value.get("numerator")
        denominator = value.get("positiveDenominator")
        if (
            isinstance(numerator, int) and not isinstance(numerator, bool)
            and isinstance(denominator, int) and not isinstance(denominator, bool)
            and denominator > 0
        ):
            return Fraction(numerator, denominator)
    raise ValueError("synthetic measurement tick must be an exact integer or rational mapping")
