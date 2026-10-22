"""Bounded reference session coordinator for synthetic engineering validation."""

from __future__ import annotations

from dataclasses import dataclass, replace
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

    def __post_init__(self) -> None:
        if self.mode not in {"ROUNDS", "BUDGET"}:
            raise ValueError("resource mode must be exactly ROUNDS or BUDGET")
        if isinstance(self.remaining, bool) or not isinstance(self.remaining, int) or self.remaining < 0:
            raise ValueError("resource remaining must be a nonnegative integer")

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
    rejected_response: VisibleExecutionRecord | None = None


@dataclass(frozen=True)
class SessionState:
    context: SessionContext
    history: HistoryHandle
    frontiers: Mapping[str, tuple[FrontierEntry, ...]]
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
        initial_path_bundles: Mapping[str, tuple[FrontierEntry, ...]] | None = None,
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
        seed_frontiers = _session_seed_frontiers(model, initial_path_bundles)
        history = HistoryHandle.initial(
            hypotheses=set(seed_frontiers),
            compatible_state_by_hypothesis={
                hypothesis: tuple(frontier.history_provenance[-1] for frontier in bundle)
                for hypothesis, bundle in seed_frontiers.items()
            },
        )
        self.binding = binding
        self.model = model
        self.initial_state = SessionState(
            context=context,
            history=history,
            frontiers=seed_frontiers,
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
        except Exception as exc:
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
        if not isinstance(state.evidence, tuple) or len(state.evidence) != state.attempts:
            return KernelDiagnostic("ATTEMPT-EVIDENCE-MISMATCH", "every issued attempt requires exactly one evidence record")
        if not isinstance(state.history, HistoryHandle) or not isinstance(state.frontiers, Mapping):
            return KernelDiagnostic("HISTORY-FRONTIER-MISMATCH", "history and frontier hypothesis sets differ")
        history_error = _history_handle_error(state.history)
        if history_error is not None:
            return history_error
        try:
            frontier_bundles = {
                hypothesis: _frontier_bundle(bundle)
                for hypothesis, bundle in state.frontiers.items()
            }
        except (AttributeError, TypeError, ValueError) as exc:
            return KernelDiagnostic("INVALID-FRONTIER-BUNDLE", str(exc) or type(exc).__name__)
        if set(frontier_bundles) != set(state.history.hypotheses):
            return KernelDiagnostic("HISTORY-FRONTIER-MISMATCH", "history and frontier hypothesis sets differ")
        try:
            history_matches_frontier = all(
                state.history.compatible_state_by_hypothesis.get(hypothesis)
                == tuple(path.history_provenance[-1] for path in paths)
                for hypothesis, paths in frontier_bundles.items()
            )
        except (AttributeError, IndexError, TypeError) as exc:
            return KernelDiagnostic("HISTORY-PROVENANCE-MISMATCH", str(exc) or type(exc).__name__)
        if not history_matches_frontier:
            return KernelDiagnostic("HISTORY-PROVENANCE-MISMATCH", "history does not name each current frontier source")
        for paths in frontier_bundles.values():
            if len(paths) > self.model.frontier_limit:
                return KernelDiagnostic("FRONTIER-BUNDLE-LIMIT", "frontier path bundle exceeds the declared bound")
            for frontier in paths:
                if frontier.model_identity != self.model.context.identity:
                    return KernelDiagnostic("FRONTIER-MODEL-MISMATCH", "frontier does not belong to this verified model")
                provenance_error = self.model.context.provenance_store.verify_entry(self.model.context, frontier)
                if provenance_error is not None:
                    return provenance_error
        return self._evidence_lineage_error(state, frontier_bundles)

    def _evidence_lineage_error(
        self,
        state: SessionState,
        current_frontiers: Mapping[str, tuple[FrontierEntry, ...]],
    ) -> KernelDiagnostic | None:
        """Replay the public causal prefix before accepting a resumed state.

        A current frontier that belongs to the model is insufficient: it must
        be the successor of this session's retained evidence.  Replaying the
        bounded, public evidence ledger binds summary, resources, snapshots,
        actions, history and frontier provenance without pretending to create
        a cryptographic tamper-proof store.
        """

        replay_model = _replay_model(self.model)
        context = self.initial_state.context
        history = self.initial_state.history
        frontiers: Mapping[str, tuple[FrontierEntry, ...]] = self.initial_state.frontiers
        resources = self.initial_state.resources
        processed_ids: frozenset[str] = frozenset()
        for index, item in enumerate(state.evidence, start=1):
            if not isinstance(item, RoundEvidence):
                return KernelDiagnostic("INVALID-EVIDENCE-RECORD", "evidence ledger contains a non-RoundEvidence value")
            if (
                not isinstance(item.snapshot, SelectSnapshot)
                or not isinstance(item.prediction, ActionPrediction)
                or not isinstance(item.execution, VisibleExecutionRecord)
                or not isinstance(item.resource_before, AlgorithmResourceView)
                or not isinstance(item.resource_after, AlgorithmResourceView)
                or not isinstance(item.detail_charges, Mapping)
                or not isinstance(item.projected_cost, Mapping)
                or not isinstance(item.history_before, HistoryHandle)
                or not isinstance(item.history_after, HistoryHandle)
                or not isinstance(item.issued_to_executor, bool)
                or not isinstance(item.charged_once, bool)
                or not isinstance(item.committed, bool)
                or not isinstance(item.stop_reason, (str, type(None)))
                or not isinstance(item.summary_after, (str, type(None)))
                or not isinstance(item.rejected_response, (VisibleExecutionRecord, type(None)))
            ):
                return KernelDiagnostic("INVALID-EVIDENCE-RECORD", "evidence ledger item has an invalid public field type")
            action = replay_model.actions.get(item.snapshot.action_id)
            if action is None or item.snapshot.action_kind != action.kind:
                return KernelDiagnostic("EVIDENCE-ACTION-MISMATCH", "evidence snapshot does not name a current model action")
            prefix = SessionState(context, history, frontiers, resources, index - 1, processed_ids, ())
            admission = self._admit(prefix, model=replay_model)
            if admission.action is None or admission.prediction is None or admission.action.action_id != action.action_id:
                return KernelDiagnostic("EVIDENCE-ADMISSION-MISMATCH", "evidence action was not admitted by its causal prefix")
            if item.prediction != admission.prediction:
                return KernelDiagnostic("EVIDENCE-PREDICTION-MISMATCH", "evidence prediction does not match the admitted action calculation")
            snapshot_error = _snapshot_error(
                item.snapshot,
                context=context,
                history=history,
                attempt=index,
                action=action,
                prediction=admission.prediction,
                model=replay_model,
                binding=self.binding,
            )
            if snapshot_error is not None:
                return snapshot_error
            if not item.issued_to_executor or not item.charged_once:
                return KernelDiagnostic("EVIDENCE-ISSUE-MISMATCH", "every ledger item must represent one issued charged execution")
            if item.resource_before != resources.algorithm_view(action):
                return KernelDiagnostic("EVIDENCE-RESOURCE-MISMATCH", "evidence resource-before view does not match its causal prefix")
            if not resources.can_afford(action):
                return KernelDiagnostic("EVIDENCE-RESOURCE-MISMATCH", "evidence action was not affordable in its causal prefix")
            charged_resources = resources.charge(action)
            if item.resource_after != charged_resources.algorithm_view(action):
                return KernelDiagnostic("EVIDENCE-RESOURCE-MISMATCH", "evidence resource-after view does not close over the charge")
            if dict(item.detail_charges) != dict(action.detail_charges) or dict(item.projected_cost) != dict(action.projected_cost()):
                return KernelDiagnostic("EVIDENCE-CHARGE-MISMATCH", "evidence charges do not match the admitted action")
            if item.history_before != history:
                return KernelDiagnostic("EVIDENCE-HISTORY-MISMATCH", "evidence history-before does not match its causal prefix")
            expected_execution_id = f"{context.run_id}:{context.session_id}:execution:{index}"
            if item.execution.execution_attempt_id != expected_execution_id or expected_execution_id in processed_ids:
                return KernelDiagnostic("EXECUTION-EVIDENCE-MISMATCH", "evidence execution identity is not the expected causal attempt")

            if _is_expected_error_record(item.execution, item.snapshot, expected_execution_id):
                if item.committed or item.history_after != history or item.summary_after is not None or item.stop_reason != "Stop-Error":
                    return KernelDiagnostic("EVIDENCE-ERROR-MISMATCH", "rejected execution evidence must preserve history and stop with error")
                if item.rejected_response is not None and not isinstance(item.rejected_response, VisibleExecutionRecord):
                    return KernelDiagnostic("EVIDENCE-REJECTED-RESPONSE", "rejected response must be a visible execution record when retained")
                context = _conservative_context(context)
                resources = charged_resources
                processed_ids = processed_ids | {expected_execution_id}
                if index != len(state.evidence):
                    return KernelDiagnostic("EVIDENCE-TERMINAL-MISMATCH", "an error evidence item cannot have a later causal round")
                continue

            record_error = _incoming_record_error(item.execution)
            if record_error is not None:
                return KernelDiagnostic("EVIDENCE-RECORD-MISMATCH", record_error.message)
            if item.execution.action_id != action.action_id:
                return KernelDiagnostic("EVIDENCE-ACTION-MISMATCH", "visible execution action differs from the admitted action")
            if item.rejected_response is not None:
                return KernelDiagnostic("EVIDENCE-REJECTED-RESPONSE", "accepted execution evidence cannot also retain a rejected response")
            if item.execution.effect_class == "CONFIRMED-NOT-SENT":
                if item.committed or item.history_after != history or item.summary_after != context.current_summary or item.stop_reason != "Stop-Error":
                    return KernelDiagnostic("EVIDENCE-NOT-SENT-MISMATCH", "confirmed-not-sent evidence must preserve the known history and summary")
                resources = charged_resources
                processed_ids = processed_ids | {expected_execution_id}
                if index != len(state.evidence):
                    return KernelDiagnostic("EVIDENCE-TERMINAL-MISMATCH", "confirmed-not-sent evidence cannot have a later causal round")
                continue
            if item.execution.effect_class == "UNKNOWN-EFFECT":
                if item.committed or item.history_after != history or item.summary_after is not None or item.stop_reason != "Stop-Error":
                    return KernelDiagnostic("EVIDENCE-UNKNOWN-MISMATCH", "unknown effect evidence must preserve history and stop with error")
                context = _conservative_context(context)
                resources = charged_resources
                processed_ids = processed_ids | {expected_execution_id}
                if index != len(state.evidence):
                    return KernelDiagnostic("EVIDENCE-TERMINAL-MISMATCH", "unknown-effect evidence cannot have a later causal round")
                continue

            selected_class, interpretation_error = _matching_class(item.snapshot, item.execution)
            if selected_class is None or interpretation_error is not None:
                return KernelDiagnostic("EVIDENCE-INTERPRETATION-MISMATCH", "committed evidence is outside its frozen prediction")
            next_history = HistoryHandle.committed(
                hypotheses=selected_class.hypotheses,
                compatible_state_by_hypothesis={
                    hypothesis: tuple(entry.history_provenance[-1] for entry in entries)
                    for hypothesis, entries in selected_class.successors.items()
                },
                status_by_hypothesis={
                    hypothesis: "CONSERVATIVE-UNKNOWN" if hypothesis in selected_class.conservative_hypotheses else "KNOWN"
                    for hypothesis in selected_class.hypotheses
                },
                version=history.version + 1,
            )
            next_context = SessionContext.create(
                session_id=context.session_id,
                run_id=context.run_id,
                experiment_attempt_id=context.experiment_attempt_id,
                model_identity=context.model_identity,
                current_summary=item.execution.post_summary,
                q_status="KNOWN",
            )
            expected_stop = "Stop-Empty" if not next_history.hypotheses else (
                "Stop-Singleton" if len(next_history.hypotheses) == 1 else None
            )
            if (
                not item.committed
                or item.history_after != next_history
                or item.summary_after != next_context.current_summary
                or item.stop_reason != expected_stop
            ):
                return KernelDiagnostic("EVIDENCE-COMMIT-MISMATCH", "committed evidence does not match its derived history update")
            context = next_context
            history = next_history
            frontiers = MappingProxyType(dict(selected_class.successors))
            resources = charged_resources
            processed_ids = processed_ids | {expected_execution_id}

        if (
            state.context != context
            or state.history != history
            or dict(current_frontiers) != dict(frontiers)
            or state.resources != resources
            or state.processed_execution_attempt_ids != processed_ids
        ):
            return KernelDiagnostic("SESSION-LINEAGE-MISMATCH", "resumed state is not the terminal state of its evidence lineage")
        return None

    def _step(self, state: SessionState, environment: SyntheticEnvironment) -> SessionResult:
        if state.evidence and state.evidence[-1].stop_reason is not None:
            return SessionResult(
                state,
                environment,
                state.evidence[-1].stop_reason,
                (KernelDiagnostic("TERMINAL-SESSION-STATE", "the retained evidence ledger already records a terminal stop"),),
            )
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
        except Exception as exc:
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
                execution_record=(
                    execution.record
                    if isinstance(execution.record, VisibleExecutionRecord)
                    else None
                ),
                environment_after_execution=(
                    execution.successor if isinstance(execution.successor, SyntheticEnvironment) else None
                ),
            )
        record_error = _incoming_record_error(execution.record)
        if record_error is not None:
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
                code=record_error.code,
                message=record_error.message,
                execution_record=execution.record,
                environment_after_execution=execution.successor,
            )
        if (
            execution.record.execution_attempt_id != execution_attempt_id
            or execution.record.action_id != snapshot.action_id
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
                message="execution result attempt/action identity is invalid or already processed",
                execution_record=execution.record,
                environment_after_execution=execution.successor,
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
        if not isinstance(execution.record.post_summary, str) or not execution.record.post_summary:
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
                code="SUMMARY-CONFIRMATION-ERROR",
                message="confirmed normal execution did not return a nonempty successor summary",
                execution_record=execution.record,
                environment_after_execution=execution.successor,
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
                environment_after_execution=execution.successor,
            )
        next_history = HistoryHandle.committed(
            hypotheses=selected_class.hypotheses,
            compatible_state_by_hypothesis={
                hypothesis: tuple(entry.history_provenance[-1] for entry in entries)
                for hypothesis, entries in selected_class.successors.items()
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

    def _admit(
        self, state: SessionState, *, model: FiniteSessionModel | None = None,
    ) -> AdmissionDecision:
        """Apply the B/C-1 TEST/GAP/PREP table without side effects."""

        current_model = self.model if model is None else model
        diagnostics: list[KernelDiagnostic] = []
        test_candidates: list[tuple[SyntheticAction, ActionPrediction, int]] = []
        eligible_test_seen = False
        unaffordable_test_seen = False
        prediction_gap_seen = False
        for action in current_model.actions.values():
            if action.kind != "TEST" or state.context.current_summary not in action.enabled_summaries:
                continue
            eligible_test_seen = True
            prediction = current_model.predict(
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

        # A current GAP revokes the complete TEST scoring set, including an
        # affordability conclusion derived from a TEST which is no longer a
        # candidate.  Only a subsequently eligible PREP may establish A2.
        if prediction_gap_seen:
            test_candidates.clear()
            unaffordable_test_seen = False

        prep_candidates: list[tuple[SyntheticAction, ActionPrediction]] = []
        eligible_prep_seen = False
        unaffordable_prep_seen = False
        for action in current_model.actions.values():
            if action.kind != "PREP" or state.context.current_summary not in action.enabled_summaries:
                continue
            eligible_prep_seen = True
            prediction = current_model.predict(
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
        environment_after_execution: SyntheticEnvironment | None = None,
    ) -> SessionResult:
        """Record an error after S4 without returning the pre-charge state.

        Once a request is issued, it owns an attempt identity and consumes the
        declared resource unit.  A malformed execution result cannot undo that
        fact; it instead transitions the session to a controlled, conservative
        unknown state without invoking S9.
        """

        expected_record = VisibleExecutionRecord(
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
            expected_record,
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
            execution_record,
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
            environment_after_execution or environment,
            "Stop-Error",
            tuple(diagnostics + [KernelDiagnostic(code, message)]),
        )


def _has_distinguishing_value(prediction: ActionPrediction, hypotheses: frozenset[str]) -> bool:
    return any(0 < len(value.hypotheses) < len(hypotheses) for value in prediction.classes)


def _replay_model(model: FiniteSessionModel) -> FiniteSessionModel:
    """Freeze replay writes in a detached verified model context.

    Prediction may append deterministic source records for new runtime paths.
    Causal-ledger validation instead recreates an existing prefix; it needs
    the same authority and record closure, but must not mutate the session's
    shared provenance store.
    """

    return replace(model, context=model.context.read_only_replay_context())


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


def _incoming_record_error(record: VisibleExecutionRecord) -> KernelDiagnostic | None:
    """Check the closed, visible execution-record combinations at S4/S8.

    The synthetic environment validates its own declarative outcomes, but an
    execution adapter is a public session boundary and may construct this
    dataclass directly.  Validate the same field and effect combinations here
    before any branch can treat a malformed record as a confirmed observation,
    a confirmed non-send, or a conservative unknown.
    """

    if any(
        not isinstance(value, str) or not value
        for value in (record.execution_attempt_id, record.action_id, record.evidence_ref)
    ):
        return KernelDiagnostic("INVALID-EXECUTION-RECORD", "execution identity, action identity, and evidence reference must be nonempty strings")
    if (
        not isinstance(record.effect_class, str)
        or record.effect_class not in {"NONE", "CONFIRMED-NOT-SENT", "UNKNOWN-EFFECT"}
    ):
        return KernelDiagnostic("INVALID-EXECUTION-RECORD", "execution effect class is outside the controlled vocabulary")
    if not isinstance(record.summary_confirmed, bool):
        return KernelDiagnostic("INVALID-EXECUTION-RECORD", "summary confirmation must be Boolean")
    if not isinstance(record.uncertainty_identity, str) or not record.uncertainty_identity:
        return KernelDiagnostic("INVALID-EXECUTION-RECORD", "incoming execution record must name a nonempty uncertainty identity")
    if record.effect_class == "NONE":
        if not isinstance(record.observable, str) or not record.observable:
            return KernelDiagnostic("INVALID-EXECUTION-RECORD", "normal execution requires a nonempty visible observation")
        if not record.summary_confirmed:
            return KernelDiagnostic("INVALID-EXECUTION-RECORD", "normal execution requires summary confirmation")
        if not isinstance(record.post_summary, str) or not record.post_summary:
            return KernelDiagnostic("SUMMARY-CONFIRMATION-ERROR", "confirmed normal execution did not return a nonempty successor summary")
        if not isinstance(record.measurement_tick, Fraction):
            return KernelDiagnostic("INVALID-EXECUTION-RECORD", "normal execution requires an exact measurement tick")
        return None
    if (
        record.observable is not None
        or record.summary_confirmed
        or record.post_summary is not None
        or record.measurement_tick is not None
    ):
        return KernelDiagnostic(
            "INVALID-EXECUTION-RECORD",
            "non-normal execution cannot manufacture an observation, confirmation, summary, or measurement",
        )
    return None


def _history_handle_error(history: HistoryHandle) -> KernelDiagnostic | None:
    """Validate a public HistoryHandle even when its factory was bypassed."""

    if not isinstance(history.hypotheses, frozenset) or any(
        not isinstance(item, str) or not item for item in history.hypotheses
    ):
        return KernelDiagnostic("INVALID-HISTORY-HANDLE", "history hypotheses must be a finite set of nonempty strings")
    if (
        isinstance(history.version, bool)
        or not isinstance(history.version, int)
        or history.version < 0
        or not isinstance(history.processed, bool)
        or not isinstance(history.compatible_state_by_hypothesis, Mapping)
        or not isinstance(history.status_by_hypothesis, Mapping)
    ):
        return KernelDiagnostic("INVALID-HISTORY-HANDLE", "history version, processed flag, or mappings are invalid")
    if set(history.compatible_state_by_hypothesis) != set(history.hypotheses):
        return KernelDiagnostic("INVALID-HISTORY-HANDLE", "history frontier references must cover exactly the hypotheses")
    for hypothesis, references in history.compatible_state_by_hypothesis.items():
        if (
            not isinstance(hypothesis, str)
            or not isinstance(references, tuple)
            or not references
            or any(not isinstance(reference, str) or not reference for reference in references)
            or len(references) != len(set(references))
        ):
            return KernelDiagnostic("INVALID-HISTORY-HANDLE", "history frontier references are invalid")
    if not set(history.status_by_hypothesis) <= set(history.hypotheses) or any(
        value not in {"KNOWN", "CONSERVATIVE-UNKNOWN"}
        for value in history.status_by_hypothesis.values()
    ):
        return KernelDiagnostic("INVALID-HISTORY-HANDLE", "history status map is outside the controlled vocabulary")
    if history.processed:
        if history.version < 1 or set(history.status_by_hypothesis) != set(history.hypotheses):
            return KernelDiagnostic("INVALID-HISTORY-HANDLE", "processed history must have positive version and complete statuses")
    elif history.version != 0:
        return KernelDiagnostic("INVALID-HISTORY-HANDLE", "unprocessed history must be the S0 version")
    return None


def _snapshot_error(
    snapshot: object,
    *,
    context: SessionContext,
    history: HistoryHandle,
    attempt: int,
    action: SyntheticAction,
    prediction: ActionPrediction,
    model: FiniteSessionModel,
    binding: RuntimeAuthorityBinding,
) -> KernelDiagnostic | None:
    if not isinstance(snapshot, SelectSnapshot):
        return KernelDiagnostic("SNAPSHOT-IDENTITY-MISMATCH", "evidence snapshot has an invalid type")
    if (
        snapshot.session_id != context.session_id
        or snapshot.snapshot_id != f"{context.session_id}:snapshot:{history.version}:{attempt}"
        or snapshot.action_id != action.action_id
        or snapshot.action_kind != action.kind
        or snapshot.q_used_at_select != context.current_summary
        or snapshot.history_version != history.version
        or snapshot.hypotheses != history.hypotheses
        or snapshot.classes != prediction.classes
        or snapshot.model_identity != model.identity
        or snapshot.uncertainty_identity != model.uncertainty_identity
        or snapshot.uncertainty_digest != model.uncertainty_digest
        or dict(snapshot.authority_identities) != dict(binding.identities())
    ):
        return KernelDiagnostic("SNAPSHOT-IDENTITY-MISMATCH", "evidence snapshot is not the expected causal selection snapshot")
    return None


def _is_expected_error_record(
    record: object, snapshot: SelectSnapshot, execution_attempt_id: str,
) -> bool:
    return record == VisibleExecutionRecord(
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


def _conservative_context(context: SessionContext) -> SessionContext:
    return SessionContext.create(
        session_id=context.session_id,
        run_id=context.run_id,
        experiment_attempt_id=context.experiment_attempt_id,
        model_identity=context.model_identity,
        current_summary=None,
        q_status="CONSERVATIVE-UNKNOWN",
    )


def _interval_contains(interval: object, tick: object) -> bool:
    if not isinstance(interval, Interval) or not isinstance(tick, Fraction):
        return False
    return (
        (tick > interval.lower or (tick == interval.lower and interval.lower_closed))
        and (tick < interval.upper or (tick == interval.upper and interval.upper_closed))
    )


def _frontier_bundle(value: object) -> tuple[FrontierEntry, ...]:
    if (
        not isinstance(value, tuple)
        or not value
        or any(not isinstance(path, FrontierEntry) for path in value)
    ):
        raise ValueError("frontier bundle must be a nonempty tuple of FrontierEntry values")
    return value


def _session_seed_frontiers(
    model: FiniteSessionModel,
    declared: Mapping[str, tuple[FrontierEntry, ...]] | None,
) -> Mapping[str, tuple[FrontierEntry, ...]]:
    """Accept an explicit finite S0 path seed and freeze it for one session."""

    source: Mapping[str, object]
    if declared is None:
        source = {hypothesis: (frontier,) for hypothesis, frontier in model.initial_frontiers.items()}
    else:
        source = declared
    if not isinstance(source, Mapping) or set(source) != set(model.initial_frontiers):
        raise ValueError("session seed must cover exactly the declared model hypotheses")
    normalized: dict[str, tuple[FrontierEntry, ...]] = {}
    for hypothesis, raw_bundle in source.items():
        try:
            bundle = _frontier_bundle(raw_bundle)
        except ValueError as exc:
            raise ValueError(f"session seed for {hypothesis!r} is invalid: {exc}") from exc
        if len(bundle) > model.frontier_limit:
            raise ValueError("session seed exceeds the declared frontier bound")
        for frontier in bundle:
            if (
                frontier.hypothesis_id != hypothesis
                or frontier.model_identity != model.context.identity
            ):
                raise ValueError("session seed path is not a model-owned frontier for its hypothesis")
            provenance_error = model.context.provenance_store.verify_entry(model.context, frontier)
            if provenance_error is not None:
                raise ValueError(f"session seed provenance is invalid: {provenance_error.code}")
        normalized[hypothesis] = bundle
    return MappingProxyType(normalized)
