"""Bounded reference session coordinator for synthetic engineering validation."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from .bindings import RuntimeAuthorityBinding
from .kernel import FrontierEntry, KernelDiagnostic
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
            return self._step(state, environment)
        except (AttributeError, KeyError, TypeError, ValueError) as exc:
            return SessionResult(
                state, environment, "Stop-Error",
                (KernelDiagnostic("SESSION-TOOL-ERROR", str(exc) or type(exc).__name__),),
            )

    def _step(self, state: SessionState, environment: SyntheticEnvironment) -> SessionResult:
        if state.context.q_status != "KNOWN" or state.context.current_summary is None:
            return SessionResult(
                state, environment, "Stop-Error",
                (KernelDiagnostic("UNRESOLVED-SESSION-SUMMARY", "known summary is required for TEST selection"),),
            )
        candidates: list[tuple[SyntheticAction, ActionPrediction, int]] = []
        diagnostics: list[KernelDiagnostic] = []
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
                candidates.append((action, prediction, worst_case))
            else:
                unaffordable_test_seen = True
        if not candidates:
            prep_candidates: list[tuple[SyntheticAction, ActionPrediction]] = []
            for action in self.model.actions.values():
                if action.kind != "PREP" or state.context.current_summary not in action.enabled_summaries:
                    continue
                prediction = self.model.predict(
                    hypotheses=state.history.hypotheses,
                    frontiers=state.frontiers,
                    status_by_hypothesis=state.history.status_by_hypothesis,
                    action_id=action.action_id,
                )
                diagnostics.extend(prediction.diagnostics)
                if prediction.classes and state.resources.can_afford(action):
                    prep_candidates.append((action, prediction))
            if prep_candidates:
                action, prediction = min(prep_candidates, key=lambda item: (item[0].cost, item[0].action_id))
                candidates.append((action, prediction, 0))
            elif prediction_gap_seen:
                return SessionResult(
                    state, environment, "Stop-Prediction-Gap",
                    tuple(diagnostics + [KernelDiagnostic("PREDICTION-GAP", "no eligible fallback follows the current TEST prediction gap")]),
                )
            elif eligible_test_seen and unaffordable_test_seen:
                return SessionResult(state, environment, "Stop-Budget", tuple(diagnostics))
            else:
                return SessionResult(state, environment, "Stop-No-Action", tuple(diagnostics))
        if not candidates:
            # Defensive totality for future action kinds; all current branches
            # above either construct a candidate or return a named stop.
            return SessionResult(state, environment, "Stop-Error", tuple(diagnostics))
        action, prediction, _score = min(
            candidates, key=lambda item: (item[2], item[0].cost, item[0].action_id),
        )
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
        selected_class = _matching_class(snapshot, execution.record)
        if selected_class is None:
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
                code="OBSERVATION-OUTSIDE-SNAPSHOT",
                message="visible observation is not in the frozen selected prediction",
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


def _matching_class(snapshot: SelectSnapshot, execution: VisibleExecutionRecord) -> PredictionClass | None:
    if execution.action_id != snapshot.action_id or execution.observable is None:
        return None
    matches = [
        value for value in snapshot.classes if value.observable == execution.observable
    ]
    return matches[0] if len(matches) == 1 else None
