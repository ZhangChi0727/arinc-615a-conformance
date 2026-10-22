"""Bounded reference session coordinator for synthetic engineering validation."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from types import MappingProxyType
from typing import Mapping

from .bindings import RuntimeAuthorityBinding
from .kernel import FrontierEntry, Interval, KernelDiagnostic
from .model import ActionPrediction, FiniteSessionModel, PredictionClass, SyntheticAction
from .synthetic import (
    EnvironmentExecution,
    ExecutionRequest,
    SyntheticEnvironment,
    VisibleExecutionRecord,
)
from .types import HistoryHandle, SessionContext


@dataclass(frozen=True)
class ResourceState:
    """One exclusive bounded session resource mode."""

    mode: str
    remaining: int

    @classmethod
    def rounds(cls, remaining: int) -> "ResourceState":
        if isinstance(remaining, bool) or not isinstance(remaining, int) or remaining < 0:
            raise ValueError("round resource remaining must be a nonnegative integer")
        return cls("ROUNDS", remaining)

    @classmethod
    def budget(cls, remaining: int) -> "ResourceState":
        if isinstance(remaining, bool) or not isinstance(remaining, int) or remaining < 0:
            raise ValueError("budget resource remaining must be a nonnegative integer")
        return cls("BUDGET", remaining)

    def can_afford(self, action: SyntheticAction) -> bool:
        return self.remaining >= 1 if self.mode == "ROUNDS" else self.remaining >= action.cost

    def charge(self, action: SyntheticAction) -> "ResourceState":
        if not self.can_afford(action):
            raise ValueError("unaffordable action cannot be charged")
        consumed = 1 if self.mode == "ROUNDS" else action.cost
        return ResourceState(self.mode, self.remaining - consumed)

    def algorithm_view(self, action: SyntheticAction) -> "AlgorithmResourceView":
        """Expose only causal resource fields required for admission."""

        return AlgorithmResourceView(self.mode, self.remaining, action.cost)


@dataclass(frozen=True)
class AlgorithmResourceView:
    """Closed resource projection; audit-only cost/status fields stay outside."""

    mode: str
    remaining: int
    declared_action_cost: int


@dataclass(frozen=True)
class AdmissionDecision:
    """One read-only A1–A3 decision before S3/S4 can mutate a session.

    The finite B/C-1 slice implements TEST, the shared prediction-gap route,
    and PREP fallback.  It deliberately represents refusal explicitly rather
    than folding an incomplete TEST prediction or an unaffordable PREP into an
    empty action list.
    """

    kind: str
    action: SyntheticAction | None
    prediction: ActionPrediction | None
    reason: str
    diagnostics: tuple[KernelDiagnostic, ...]


@dataclass(frozen=True)
class SelectSnapshot:
    """Frozen S3 selection inputs and final action identity."""

    session_id: str
    snapshot_id: str
    action_id: str
    action_kind: str
    q_used_at_select: str
    history_version: int
    hypotheses: frozenset[str]
    classes: tuple[PredictionClass, ...]
    model_identity: str
    uncertainty_identity: str
    uncertainty_digest: str
    authority_identities: Mapping[str, Mapping[str, str]]


@dataclass(frozen=True)
class RoundEvidence:
    """One observable engineering round, not a protocol verdict."""

    snapshot: SelectSnapshot
    prediction: ActionPrediction
    execution: VisibleExecutionRecord
    issued_to_executor: bool
    charged_once: bool
    resource_before: AlgorithmResourceView
    resource_after: AlgorithmResourceView
    detail_charges: Mapping[str, int]
    projected_cost: Mapping[str, int]
    history_before: HistoryHandle
    history_after: HistoryHandle
    summary_after: str | None
    committed: bool
    stop_reason: str | None


@dataclass(frozen=True)
class SessionState:
    context: SessionContext
    history: HistoryHandle
    frontiers: Mapping[str, FrontierEntry]
    resources: ResourceState
    attempts: int
    processed_execution_attempt_ids: frozenset[str]
    evidence: tuple[RoundEvidence, ...]


@dataclass(frozen=True)
class SessionResult:
    state: SessionState
    environment: SyntheticEnvironment
    stop_reason: str | None
    diagnostics: tuple[KernelDiagnostic, ...]


class ReferenceSession:
    """Composes prediction, S3 snapshot, execution, interpretation and S9.

    Its environment dependency is deliberately limited to
    :meth:`SyntheticEnvironment.execute`; the coordinator has no API to query
    private state or evaluator truth.
    """

    def __init__(
        self, *, binding: RuntimeAuthorityBinding, model: FiniteSessionModel,
        session_id: str, run_id: str, initial_summary: str, resources: ResourceState,
        experiment_attempt_id: str | None = None,
    ) -> None:
        if binding.development.contract_commit != model.context.contract_commit:
            raise ValueError("runtime model and authority binding use different development snapshots")
        context = SessionContext.create(
            session_id=session_id,
            run_id=run_id,
            experiment_attempt_id=experiment_attempt_id,
            model_identity=model.identity,
            current_summary=initial_summary,
            q_status="KNOWN",
        )
        history = HistoryHandle.initial(
            hypotheses=set(model.initial_frontiers),
            compatible_state_by_hypothesis={
                hypothesis: frontier.history_provenance[-1]
                for hypothesis, frontier in model.initial_frontiers.items()
            },
        )
        self.binding = binding
        self.model = model
        self.initial_state = SessionState(
            context=context,
            history=history,
            frontiers=MappingProxyType(dict(model.initial_frontiers)),
            resources=resources,
            attempts=0,
            processed_execution_attempt_ids=frozenset(),
            evidence=(),
        )

    def run(self, environment: SyntheticEnvironment, *, maximum_rounds: int) -> SessionResult:
        if isinstance(maximum_rounds, bool) or not isinstance(maximum_rounds, int) or maximum_rounds < 1:
            return SessionResult(
                self.initial_state, environment, "Stop-Error",
                (KernelDiagnostic("INVALID-ROUND-LIMIT", "maximum rounds must be a positive integer"),),
            )
        state = self.initial_state
        current_environment = environment
        for _ in range(maximum_rounds):
            step = self.step(state, current_environment)
            state, current_environment = step.state, step.environment
            if step.stop_reason is not None:
                return step
        return SessionResult(
            state, current_environment, "Stop-Round-Limit",
            (KernelDiagnostic("ROUND-LIMIT", "declared synthetic round limit reached"),),
        )

    def step(self, state: SessionState, environment: SyntheticEnvironment) -> SessionResult:
        """Run one S0–S10 reference iteration with controlled failures."""

        try:
            state_error = self._state_error(state)
            if state_error is not None:
                return SessionResult(state, environment, "Stop-Error", (state_error,))
            return self._step(state, environment)
        except (AttributeError, KeyError, TypeError, ValueError) as exc:
            return SessionResult(
                state, environment, "Stop-Error",
                (KernelDiagnostic("SESSION-TOOL-ERROR", str(exc) or type(exc).__name__),),
            )

    def _state_error(self, state: object) -> KernelDiagnostic | None:
        """Validate a resumed public state before admission or charging.

        ``SessionState`` is deliberately inspectable, so callers may attempt
        to resume with a state from another model/session or with a rewritten
        compatible-history map.  Validate the full provenance closure here;
        matching only ``H`` or incrementing a supplied version is not enough.
        """

        if not isinstance(state, SessionState):
            return KernelDiagnostic("INVALID-SESSION-STATE", "state is not a SessionState")
        initial_context = self.initial_state.context
        context = state.context
        if not isinstance(context, SessionContext) or (
            context.session_id != initial_context.session_id
            or context.run_id != initial_context.run_id
            or context.model_identity != self.model.identity
        ):
            return KernelDiagnostic("SESSION-IDENTITY-MISMATCH", "state does not belong to this session/run/model")
        if context.experiment_attempt_id != initial_context.experiment_attempt_id:
            return KernelDiagnostic("EXPERIMENT-IDENTITY-MISMATCH", "state changes the declared experiment identity")
        if not isinstance(state.resources, ResourceState) or state.resources.mode not in {"ROUNDS", "BUDGET"} or (
            isinstance(state.resources.remaining, bool)
            or not isinstance(state.resources.remaining, int)
            or state.resources.remaining < 0
        ):
            return KernelDiagnostic("INVALID-RESOURCE-STATE", "state resource mode or remainder is invalid")
        if isinstance(state.attempts, bool) or not isinstance(state.attempts, int) or state.attempts < 0:
            return KernelDiagnostic("INVALID-ATTEMPT-COUNT", "state attempt count is invalid")
        if not isinstance(state.processed_execution_attempt_ids, frozenset) or any(
            not isinstance(value, str) or not value for value in state.processed_execution_attempt_ids
        ):
            return KernelDiagnostic("INVALID-EXECUTION-IDENTITIES", "processed execution identities are invalid")
        if len(state.evidence) != state.attempts:
            return KernelDiagnostic("ATTEMPT-EVIDENCE-MISMATCH", "every issued attempt requires exactly one evidence record")
        if not isinstance(state.history, HistoryHandle) or set(state.frontiers) != set(state.history.hypotheses):
            return KernelDiagnostic("HISTORY-FRONTIER-MISMATCH", "history and frontier hypothesis sets differ")
        if any(
            state.history.compatible_state_by_hypothesis.get(hypothesis)
            != frontier.history_provenance[-1]
            for hypothesis, frontier in state.frontiers.items()
        ):
            return KernelDiagnostic("HISTORY-PROVENANCE-MISMATCH", "history does not name each current frontier source")
        if state.history.processed:
            if set(state.history.status_by_hypothesis) != set(state.history.hypotheses):
                return KernelDiagnostic("INCOMPLETE-PROCESSED-HISTORY", "processed history must status every current hypothesis")
        elif state.history.version != 0:
            return KernelDiagnostic("INVALID-INITIAL-HISTORY", "unprocessed history must be the S0 version")
        for frontier in state.frontiers.values():
            if not isinstance(frontier, FrontierEntry) or frontier.model_identity != self.model.context.identity:
                return KernelDiagnostic("FRONTIER-MODEL-MISMATCH", "frontier does not belong to this verified model")
            provenance_error = self.model.context.provenance_store.verify_entry(self.model.context, frontier)
            if provenance_error is not None:
                return provenance_error
        committed_count = sum(1 for item in state.evidence if item.committed)
        if state.history.version != committed_count:
            return KernelDiagnostic("HISTORY-VERSION-MISMATCH", "history version does not equal committed evidence count")
        evidence_ids = frozenset(item.execution.execution_attempt_id for item in state.evidence)
        if evidence_ids != state.processed_execution_attempt_ids or len(evidence_ids) != len(state.evidence):
            return KernelDiagnostic("EXECUTION-EVIDENCE-MISMATCH", "execution identities do not close over the evidence ledger")
        for item in state.evidence:
            if (
                item.snapshot.session_id != context.session_id
                or item.snapshot.model_identity != self.model.identity
                or item.snapshot.uncertainty_identity != self.model.uncertainty_identity
                or item.snapshot.uncertainty_digest != self.model.uncertainty_digest
                or dict(item.snapshot.authority_identities) != dict(self.binding.identities())
            ):
                return KernelDiagnostic("SNAPSHOT-IDENTITY-MISMATCH", "evidence snapshot identity is not owned by this session")
        return None

    def _step(self, state: SessionState, environment: SyntheticEnvironment) -> SessionResult:
        if state.context.q_status != "KNOWN" or state.context.current_summary is None:
            return SessionResult(
                state, environment, "Stop-Error",
                (KernelDiagnostic("UNRESOLVED-SESSION-SUMMARY", "known summary is required for TEST selection"),),
            )
        admission = self._admit(state)
        if admission.action is None or admission.prediction is None:
            stop_reason = {
                "PREDICTION-GAP": "Stop-Prediction-Gap",
                "A2-UNAFFORDABLE": "Stop-Budget",
                "NO-ADMITTED-ACTION": "Stop-No-Action",
            }.get(admission.reason, "Stop-Error")
            return SessionResult(state, environment, stop_reason, admission.diagnostics)
        action, prediction = admission.action, admission.prediction
        diagnostics = list(admission.diagnostics)
        snapshot = SelectSnapshot(
            session_id=state.context.session_id,
            snapshot_id=f"{state.context.session_id}:snapshot:{state.history.version}:{state.attempts + 1}",
            action_id=action.action_id,
            action_kind=action.kind,
            q_used_at_select=state.context.current_summary,
            history_version=state.history.version,
            hypotheses=state.history.hypotheses,
            classes=prediction.classes,
            model_identity=self.model.identity,
            uncertainty_identity=self.model.uncertainty_identity,
            uncertainty_digest=self.model.uncertainty_digest,
            authority_identities=self.binding.identities(),
        )
        resource_before = state.resources.algorithm_view(action)
        charged_resources = state.resources.charge(action)
        resource_after = charged_resources.algorithm_view(action)
        execution_attempt_id = (
            f"{state.context.run_id}:{state.context.session_id}:execution:{state.attempts + 1}"
        )
        request = ExecutionRequest(
            session_id=state.context.session_id,
            execution_attempt_id=execution_attempt_id,
            action_id=snapshot.action_id,
            action_kind=snapshot.action_kind,
        )
        try:
            execution = environment.execute(request)
        except (AttributeError, KeyError, TypeError, ValueError) as exc:
            return self._charged_execution_error(
                state=state,
                environment=environment,
                snapshot=snapshot,
                prediction=prediction,
                action=action,
                resource_before=resource_before,
                resource_after=resource_after,
                charged_resources=charged_resources,
                execution_attempt_id=execution_attempt_id,
                diagnostics=diagnostics,
                code="EXECUTION-TOOL-ERROR",
                message=str(exc) or type(exc).__name__,
            )
        if not isinstance(execution, EnvironmentExecution):
            return self._charged_execution_error(
                state=state,
                environment=environment,
                snapshot=snapshot,
                prediction=prediction,
                action=action,
                resource_before=resource_before,
                resource_after=resource_after,
                charged_resources=charged_resources,
                execution_attempt_id=execution_attempt_id,
                diagnostics=diagnostics,
                code="EXECUTION-RESULT-TYPE-ERROR",
                message="environment did not return an EnvironmentExecution",
            )
        if not isinstance(execution.record, VisibleExecutionRecord) or not isinstance(execution.successor, SyntheticEnvironment):
            return self._charged_execution_error(
                state=state,
                environment=environment,
                snapshot=snapshot,
                prediction=prediction,
                action=action,
                resource_before=resource_before,
                resource_after=resource_after,
                charged_resources=charged_resources,
                execution_attempt_id=execution_attempt_id,
                diagnostics=diagnostics,
                code="EXECUTION-RESULT-TYPE-ERROR",
                message="environment execution has an invalid record or successor",
            )
        if (
            execution.record.execution_attempt_id != execution_attempt_id
            or execution_attempt_id in state.processed_execution_attempt_ids
        ):
            return self._charged_execution_error(
                state=state,
                environment=environment,
                snapshot=snapshot,
                prediction=prediction,
                action=action,
                resource_before=resource_before,
                resource_after=resource_after,
                charged_resources=charged_resources,
                execution_attempt_id=execution_attempt_id,
                diagnostics=diagnostics,
                code="EXECUTION-IDENTITY-ERROR",
                message="execution result identity is invalid or already processed",
            )
        if execution.record.effect_class == "CONFIRMED-NOT-SENT":
            evidence = RoundEvidence(
                snapshot, prediction, execution.record, True, True, resource_before, resource_after,
                action.detail_charges, action.projected_cost(), state.history, state.history,
                state.context.current_summary, False, "Stop-Error",
            )
            next_state = SessionState(
                state.context, state.history, state.frontiers, charged_resources,
                state.attempts + 1, state.processed_execution_attempt_ids | {execution_attempt_id}, state.evidence + (evidence,),
            )
            return SessionResult(
                next_state, execution.successor, "Stop-Error",
                tuple(diagnostics + [KernelDiagnostic("CONFIRMED-NOT-SENT", "environment confirmed that no action was sent")]),
            )
        if execution.record.effect_class != "NONE" or not execution.record.summary_confirmed:
            unknown_context = SessionContext.create(
                session_id=state.context.session_id,
                run_id=state.context.run_id,
                experiment_attempt_id=state.context.experiment_attempt_id,
                model_identity=state.context.model_identity,
                current_summary=None,
                q_status="CONSERVATIVE-UNKNOWN",
            )
            evidence = RoundEvidence(
                snapshot, prediction, execution.record, True, True, resource_before, resource_after,
                action.detail_charges, action.projected_cost(), state.history, state.history,
                None, False, "Stop-Error",
            )
            next_state = SessionState(
                unknown_context, state.history, state.frontiers, charged_resources,
                state.attempts + 1, state.processed_execution_attempt_ids | {execution_attempt_id}, state.evidence + (evidence,),
            )
            return SessionResult(
                next_state, execution.successor, "Stop-Error",
                tuple(diagnostics + [KernelDiagnostic("UNKNOWN-EFFECT", "synthetic execution did not confirm a successor summary")]),
            )
        selected_class, interpretation_error = _matching_class(snapshot, execution.record)
        if selected_class is None:
            assert interpretation_error is not None
            return self._charged_execution_error(
                state=state,
                environment=environment,
                snapshot=snapshot,
                prediction=prediction,
                action=action,
                resource_before=resource_before,
                resource_after=resource_after,
                charged_resources=charged_resources,
                execution_attempt_id=execution_attempt_id,
                diagnostics=diagnostics,
                code=interpretation_error.code,
                message=interpretation_error.message,
                execution_record=execution.record,
            )
        next_history = HistoryHandle.committed(
            hypotheses=selected_class.hypotheses,
            compatible_state_by_hypothesis={
                hypothesis: entry.history_provenance[-1]
                for hypothesis, entry in selected_class.successors.items()
            },
            status_by_hypothesis={
                hypothesis: "CONSERVATIVE-UNKNOWN" if hypothesis in selected_class.conservative_hypotheses else "KNOWN"
                for hypothesis in selected_class.hypotheses
            },
            version=state.history.version + 1,
        )
        next_context = SessionContext.create(
            session_id=state.context.session_id,
            run_id=state.context.run_id,
            experiment_attempt_id=state.context.experiment_attempt_id,
            model_identity=state.context.model_identity,
            current_summary=execution.record.post_summary,
            q_status="KNOWN",
        )
        stop_reason = "Stop-Empty" if not next_history.hypotheses else (
            "Stop-Singleton" if len(next_history.hypotheses) == 1 else None
        )
        evidence = RoundEvidence(
            snapshot, prediction, execution.record, True, True, resource_before, resource_after,
            action.detail_charges, action.projected_cost(), state.history, next_history,
            next_context.current_summary, True, stop_reason,
        )
        next_state = SessionState(
            next_context,
            next_history,
            MappingProxyType(dict(selected_class.successors)),
            charged_resources,
            state.attempts + 1,
            state.processed_execution_attempt_ids | {execution_attempt_id},
            state.evidence + (evidence,),
        )
        return SessionResult(next_state, execution.successor, stop_reason, tuple(diagnostics))

    def _admit(self, state: SessionState) -> AdmissionDecision:
        """Apply the B/C-1 TEST/GAP/PREP table without side effects."""

        diagnostics: list[KernelDiagnostic] = []
        test_candidates: list[tuple[SyntheticAction, ActionPrediction, int]] = []
        eligible_test_seen = False
        unaffordable_test_seen = False
        prediction_gap_seen = False
        for action in self.model.actions.values():
            if action.kind != "TEST" or state.context.current_summary not in action.enabled_summaries:
                continue
            eligible_test_seen = True
            prediction = self.model.predict(
                hypotheses=state.history.hypotheses,
                frontiers=state.frontiers,
                status_by_hypothesis=state.history.status_by_hypothesis,
                action_id=action.action_id,
            )
            diagnostics.extend(prediction.diagnostics)
            if not prediction.classes:
                prediction_gap_seen = True
                continue
            if not _has_distinguishing_value(prediction, state.history.hypotheses):
                continue
            worst_case = max(len(item.hypotheses) for item in prediction.classes)
            if state.resources.can_afford(action):
                test_candidates.append((action, prediction, worst_case))
            else:
                unaffordable_test_seen = True
        if not prediction_gap_seen and test_candidates:
            action, prediction, _score = min(
                test_candidates, key=lambda item: (item[2], item[0].cost, item[0].action_id),
            )
            return AdmissionDecision("TEST", action, prediction, "TEST-ADMITTED", tuple(diagnostics))

        prep_candidates: list[tuple[SyntheticAction, ActionPrediction]] = []
        eligible_prep_seen = False
        unaffordable_prep_seen = False
        for action in self.model.actions.values():
            if action.kind != "PREP" or state.context.current_summary not in action.enabled_summaries:
                continue
            eligible_prep_seen = True
            prediction = self.model.predict(
                hypotheses=state.history.hypotheses,
                frontiers=state.frontiers,
                status_by_hypothesis=state.history.status_by_hypothesis,
                action_id=action.action_id,
            )
            diagnostics.extend(prediction.diagnostics)
            if not prediction.classes:
                continue
            if state.resources.can_afford(action):
                prep_candidates.append((action, prediction))
            else:
                unaffordable_prep_seen = True
        if prep_candidates:
            action, prediction = min(prep_candidates, key=lambda item: (item[0].cost, item[0].action_id))
            return AdmissionDecision("PREP", action, prediction, "PREP-ADMITTED", tuple(diagnostics))
        if unaffordable_test_seen or unaffordable_prep_seen:
            return AdmissionDecision(
                "ADMIT", None, None, "A2-UNAFFORDABLE",
                tuple(diagnostics + [KernelDiagnostic("ADMISSION-A2-UNAFFORDABLE", "eligible action is not affordable in the declared resource mode")]),
            )
        if prediction_gap_seen:
            return AdmissionDecision(
                "ADMIT", None, None, "PREDICTION-GAP",
                tuple(diagnostics + [KernelDiagnostic("PREDICTION-GAP", "current TEST prediction is incomplete and no eligible PREP fallback was admitted")]),
            )
        reason = "NO-ADMITTED-ACTION"
        if eligible_test_seen or eligible_prep_seen:
            diagnostics.append(KernelDiagnostic("NO-ADMITTED-ACTION", "known session has no affordable distinguishing TEST or usable PREP"))
        return AdmissionDecision("ADMIT", None, None, reason, tuple(diagnostics))

    def _charged_execution_error(
        self,
        *,
        state: SessionState,
        environment: SyntheticEnvironment,
        snapshot: SelectSnapshot,
        prediction: ActionPrediction,
        action: SyntheticAction,
        resource_before: AlgorithmResourceView,
        resource_after: AlgorithmResourceView,
        charged_resources: ResourceState,
        execution_attempt_id: str,
        diagnostics: list[KernelDiagnostic],
        code: str,
        message: str,
        execution_record: VisibleExecutionRecord | None = None,
    ) -> SessionResult:
        """Record an error after S4 without returning the pre-charge state.

        Once a request is issued, it owns an attempt identity and consumes the
        declared resource unit.  A malformed execution result cannot undo that
        fact; it instead transitions the session to a controlled, conservative
        unknown state without invoking S9.
        """

        record = execution_record or VisibleExecutionRecord(
            execution_attempt_id=execution_attempt_id,
            action_id=snapshot.action_id,
            effect_class="UNKNOWN-EFFECT",
            observable=None,
            summary_confirmed=False,
            post_summary=None,
            measurement_tick=None,
            uncertainty_identity=None,
            evidence_ref=f"synthetic:{execution_attempt_id}:tool-error",
        )
        unknown_context = SessionContext.create(
            session_id=state.context.session_id,
            run_id=state.context.run_id,
            experiment_attempt_id=state.context.experiment_attempt_id,
            model_identity=state.context.model_identity,
            current_summary=None,
            q_status="CONSERVATIVE-UNKNOWN",
        )
        evidence = RoundEvidence(
            snapshot,
            prediction,
            record,
            True,
            True,
            resource_before,
            resource_after,
            action.detail_charges,
            action.projected_cost(),
            state.history,
            state.history,
            None,
            False,
            "Stop-Error",
        )
        charged_state = SessionState(
            unknown_context,
            state.history,
            state.frontiers,
            charged_resources,
            state.attempts + 1,
            state.processed_execution_attempt_ids | {execution_attempt_id},
            state.evidence + (evidence,),
        )
        return SessionResult(
            charged_state,
            environment,
            "Stop-Error",
            tuple(diagnostics + [KernelDiagnostic(code, message)]),
        )


def _has_distinguishing_value(prediction: ActionPrediction, hypotheses: frozenset[str]) -> bool:
    return any(0 < len(value.hypotheses) < len(hypotheses) for value in prediction.classes)


def _matching_class(
    snapshot: SelectSnapshot, execution: VisibleExecutionRecord,
) -> tuple[PredictionClass | None, KernelDiagnostic | None]:
    if execution.action_id != snapshot.action_id or execution.observable is None:
        return None, KernelDiagnostic(
            "OBSERVATION-OUTSIDE-SNAPSHOT",
            "visible action or observation is not in the frozen selected prediction",
        )
    if execution.uncertainty_identity != snapshot.uncertainty_identity:
        return None, KernelDiagnostic(
            "UNCERTAINTY-SNAPSHOT-MISMATCH",
            "interpretation record does not name the uncertainty snapshot used at selection",
        )
    if execution.measurement_tick is None:
        return None, KernelDiagnostic(
            "OBSERVATION-MEASUREMENT-ERROR",
            "normal visible observation has no exact measurement tick",
        )
    matches = [
        value for value in snapshot.classes if value.observable == execution.observable
    ]
    if len(matches) != 1:
        return None, KernelDiagnostic(
            "OBSERVATION-OUTSIDE-SNAPSHOT",
            "visible observation is not in the frozen selected prediction",
        )
    candidate = matches[0]
    if not any(_interval_contains(window, execution.measurement_tick) for window in candidate.measurement_windows.values()):
        return None, KernelDiagnostic(
            "OBSERVATION-MEASUREMENT-OUTSIDE-UNCERTAINTY",
            "visible measurement tick is outside every selected uncertainty window",
        )
    return candidate, None


def _interval_contains(interval: object, tick: object) -> bool:
    if not isinstance(interval, Interval) or not isinstance(tick, Fraction):
        return False
    return (
        (tick > interval.lower or (tick == interval.lower and interval.lower_closed))
        and (tick < interval.upper or (tick == interval.upper and interval.upper_closed))
    )
