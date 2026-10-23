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
class PrepRecoverResult:
    """Visible, typed return from ``IF-PREP-RECOVER``.

    The environment may report publicly observable confirmation and evidence,
    but this value is deliberately only a return record.  It has no reference
    to a session context, candidate hypotheses, score, or evaluator truth; the
    session's S7/S8/S9 code remains the sole owner of state changes.
    """

    target_confirmed: bool
    summary_confirmed: bool
    prep_error: bool
    ineligible: bool
    declared_target: str
    evidence: str
    post_summary: str | None


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
    prep_recover: PrepRecoverResult | None = None


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
    _pending_delivery: VisibleExecutionRecord | None = None

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
                allowed = {
                    "effectClass", "observable", "summaryConfirmed", "postSummary", "measurementTick",
                    "nextPrivateState", "prepRecover",
                }
                required = {
                    "effectClass", "observable", "summaryConfirmed", "postSummary", "measurementTick", "nextPrivateState",
                }
                if not set(outcome) <= allowed:
                    raise ValueError("synthetic environment outcome uses unknown or missing fields")
                if not required <= set(outcome):
                    if "postSummary" not in outcome:
                        raise ValueError("synthetic environment outcome requires an explicit successor summary field")
                    raise ValueError("synthetic environment outcome uses unknown or missing fields")
                effect = outcome.get("effectClass")
                observable = outcome.get("observable")
                confirmed = outcome.get("summaryConfirmed")
                post_summary = outcome.get("postSummary")
                measurement_tick = outcome.get("measurementTick")
                successor = outcome.get("nextPrivateState")
                prep_recover = _prep_recover_result(outcome.get("prepRecover")) if "prepRecover" in outcome else None
                if effect not in {"NONE", "CONFIRMED-NOT-SENT", "UNKNOWN-EFFECT"}:
                    raise ValueError("synthetic environment effect class is invalid")
                if observable is not None and (not isinstance(observable, str) or not observable):
                    raise ValueError("synthetic environment observable is invalid")
                if not isinstance(confirmed, bool) or not isinstance(successor, str) or not successor:
                    raise ValueError("synthetic environment outcome is invalid")
                if effect != "NONE" and (
                    observable is not None or confirmed or post_summary is not None
                    or measurement_tick is not None or prep_recover is not None
                ):
                    raise ValueError("non-normal synthetic outcome cannot manufacture observation or successor fields")
                if effect == "NONE" and prep_recover is None:
                    if (
                        observable is None or not confirmed
                        or not isinstance(post_summary, str) or not post_summary
                    ):
                        raise ValueError("normal TEST outcome requires visible confirmed evidence and an explicit successor summary")
                    _exact_tick(measurement_tick)
                if effect == "NONE" and prep_recover is not None:
                    if (
                        confirmed != prep_recover.summary_confirmed
                        or post_summary != prep_recover.post_summary
                    ):
                        raise ValueError("Prep/Recover confirmation must agree with the visible outcome")
                    if observable is None:
                        if measurement_tick is not None:
                            raise ValueError("summary-only Prep/Recover outcome cannot carry a measurement tick")
                    else:
                        _exact_tick(measurement_tick)
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
                        "postSummary": post_summary,
                        "measurementTick": _exact_tick(measurement_tick) if effect == "NONE" and measurement_tick is not None else None,
                        "nextPrivateState": successor,
                        "prepRecover": prep_recover,
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

    def with_pending_delivery(self, record: VisibleExecutionRecord) -> "SyntheticEnvironment":
        """Return a bounded environment with one inbound, not-yet-consumed record.

        A pending delivery models transport reception, not a fresh admitted
        action.  ``ReferenceSession.step`` consumes it before S3/S4, so a
        duplicate record can be discarded idempotently without creating a new
        request, charge, or history record.  The one-record bound keeps this
        synthetic engineering seam finite; an adapter with a real queue must
        expose the same receive-before-issue ordering.
        """

        if not isinstance(record, VisibleExecutionRecord):
            raise ValueError("synthetic pending delivery must be a visible execution record")
        if self._pending_delivery is not None:
            raise ValueError("synthetic environment already has an unconsumed pending delivery")
        return SyntheticEnvironment(self._state, self._uncertainty_identity, self._states, record)

    def take_pending_delivery(self) -> tuple[VisibleExecutionRecord, "SyntheticEnvironment"] | None:
        """Consume the one inbound delivery before any new action is issued."""

        if self._pending_delivery is None:
            return None
        return self._pending_delivery, SyntheticEnvironment(
            self._state, self._uncertainty_identity, self._states,
        )

    def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
        """Execute an admitted request without access to algorithm internals."""

        if self._pending_delivery is not None:
            raise ValueError("synthetic environment has an unconsumed pending delivery")
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
                uncertainty_identity=None,
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
            post_summary=outcome["postSummary"],
            measurement_tick=outcome["measurementTick"],
            uncertainty_identity=(
                self._uncertainty_identity
                if outcome["effectClass"] == "NONE" and observable is not None
                else None
            ),
            evidence_ref=f"synthetic:{request.execution_attempt_id}:{outcome['effectClass'].lower()}",
            prep_recover=outcome["prepRecover"],
        )
        return EnvironmentExecution(record, successor)


def _prep_recover_result(value: object) -> PrepRecoverResult:
    """Decode a narrow public recovery return, never a session mutation."""

    required = {
        "targetConfirmed", "summaryConfirmed", "prepError", "ineligible",
        "declaredTarget", "evidence", "postSummary",
    }
    if not isinstance(value, Mapping) or set(value) != required:
        raise ValueError("synthetic Prep/Recover result uses unknown or missing fields")
    target_confirmed = value.get("targetConfirmed")
    summary_confirmed = value.get("summaryConfirmed")
    prep_error = value.get("prepError")
    ineligible = value.get("ineligible")
    declared_target = value.get("declaredTarget")
    evidence = value.get("evidence")
    post_summary = value.get("postSummary")
    if not all(isinstance(flag, bool) for flag in (
        target_confirmed, summary_confirmed, prep_error, ineligible,
    )):
        raise ValueError("synthetic Prep/Recover confirmations must be Boolean")
    if not isinstance(declared_target, str) or not declared_target:
        raise ValueError("synthetic Prep/Recover target must be a nonempty string")
    if not isinstance(evidence, str) or not evidence.strip():
        raise ValueError("synthetic Prep/Recover evidence must be a nonblank string")
    if summary_confirmed:
        if not isinstance(post_summary, str) or not post_summary:
            raise ValueError("confirmed Prep/Recover result requires a successor summary")
    elif post_summary is not None:
        raise ValueError("unconfirmed Prep/Recover result cannot carry a successor summary")
    if (prep_error or ineligible) and (target_confirmed or summary_confirmed):
        raise ValueError("failed Prep/Recover result cannot claim a confirmation")
    return PrepRecoverResult(
        target_confirmed=target_confirmed,
        summary_confirmed=summary_confirmed,
        prep_error=prep_error,
        ineligible=ineligible,
        declared_target=declared_target,
        evidence=evidence,
        post_summary=post_summary,
    )


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
