"""Bounded reference session coordinator for synthetic engineering validation."""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from hashlib import sha256
from types import MappingProxyType
from typing import Mapping

from .bindings import RuntimeAuthorityBinding
from .kernel import FrontierEntry, Interval, KernelDiagnostic
from .model import ActionPrediction, FiniteSessionModel, PredictionClass, SyntheticAction
from .synthetic import (
    EnvironmentExecution,
    ExecutionRequest,
    PrepRecoverResult,
    SyntheticEnvironment,
    VisibleExecutionRecord,
)
from .types import HistoryHandle, SessionContext


_CHARGED_ERROR_CODES = frozenset({
    "EXECUTION-TOOL-ERROR",
    "POST-DISPATCH-ERROR",
    "EXECUTION-RESULT-TYPE-ERROR",
    "EXECUTION-IDENTITY-ERROR",
    "INVALID-EXECUTION-RECORD",
    "SUMMARY-CONFIRMATION-ERROR",
    "RECOVERY-TARGET-MISMATCH",
})


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

    The finite B/C-2A slice implements TEST, the shared prediction-gap/Prep
    route, and the separate UNKNOWN-session Recover route.  It deliberately
    represents refusal explicitly rather than folding an incomplete TEST
    prediction, an unaffordable Prep, or an unavailable Recover into an empty
    action list.
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
    q_used_at_select: str | None
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
    # Name the controlled S7/S8/S9 branch which produced this record.  The
    # causal ledger must replay the exact error branch rather than infer it
    # from a shared ``UNKNOWN-EFFECT`` shape.
    resolution_code: str | None = None


@dataclass(frozen=True)
class SessionState:
    context: SessionContext
    history: HistoryHandle
    frontiers: Mapping[str, tuple[FrontierEntry, ...]]
    resources: ResourceState
    attempts: int
    processed_execution_attempt_ids: frozenset[str]
    evidence: tuple[RoundEvidence, ...]
    authority_identity: str
    seed_identity: str


@dataclass(frozen=True)
class SessionResult:
    state: SessionState
    environment: SyntheticEnvironment
    stop_reason: str | None
    diagnostics: tuple[KernelDiagnostic, ...]


@dataclass(frozen=True)
class _S8RecoveryAdoption:
    """Internal S8 output, consumed by S9 before it becomes SessionContext."""

    q_status: str
    known_target: str
    known_evidence: tuple[str, ...]


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
        retry_cap: int = 1,
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
            resource_remainder=resources.remaining,
            retry_count=0,
            retry_cap=retry_cap,
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
        self._authority_identity = _session_authority_identity(binding, model)
        self._seed_identity = _session_seed_identity(
            context=context,
            history=history,
            frontiers=seed_frontiers,
            resources=resources,
            authority_identity=self._authority_identity,
        )
        self.initial_state = SessionState(
            context=context,
            history=history,
            frontiers=seed_frontiers,
            resources=resources,
            attempts=0,
            processed_execution_attempt_ids=frozenset(),
            evidence=(),
            authority_identity=self._authority_identity,
            seed_identity=self._seed_identity,
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
            assert isinstance(state, SessionState)
            terminal = self._retained_terminal_result(state, environment)
            if terminal is not None:
                return terminal
            # Receive transport deliveries before S3/S4.  A repeated record is
            # therefore an idempotent receive event, not a reason to issue a
            # new action and discover the duplication only after charging it.
            if isinstance(environment, SyntheticEnvironment):
                pending = environment.take_pending_delivery()
                if pending is not None:
                    record, environment_after_delivery = pending
                    return self._consume_pending_delivery(state, environment_after_delivery, record)
            execution_model, execution_error = self._execution_model(state)
            if execution_error is not None:
                return SessionResult(state, environment, "Stop-Error", (execution_error,))
            assert execution_model is not None
            return self._step(state, environment, model=execution_model)
        except Exception as exc:
            return SessionResult(
                state, environment, "Stop-Error",
                (KernelDiagnostic("SESSION-TOOL-ERROR", str(exc) or type(exc).__name__),),
            )

    @staticmethod
    def _retained_terminal_result(
        state: SessionState,
        environment: SyntheticEnvironment,
    ) -> SessionResult | None:
        """Preserve a recorded terminal stop before accepting any delivery."""

        if not state.evidence or state.evidence[-1].stop_reason is None:
            return None
        return SessionResult(
            state,
            environment,
            state.evidence[-1].stop_reason,
            (KernelDiagnostic(
                "TERMINAL-SESSION-STATE",
                "the retained evidence ledger already records a terminal stop",
            ),),
        )

    def _consume_pending_delivery(
        self,
        state: SessionState,
        environment_after_delivery: SyntheticEnvironment,
        record: VisibleExecutionRecord,
    ) -> SessionResult:
        """Handle one inbound delivery without admitting or charging an action."""

        execution_id = record.execution_attempt_id
        if (
            isinstance(execution_id, str)
            and execution_id
            and execution_id in state.processed_execution_attempt_ids
        ):
            canonical_evidence = tuple(
                item
                for item in state.evidence
                if item.execution.execution_attempt_id == execution_id
            )
            # State validation establishes a one-to-one ledger of processed
            # identities to issued evidence.  Still fail closed here rather
            # than silently accepting a malformed public checkpoint.
            if len(canonical_evidence) != 1:
                return SessionResult(
                    state,
                    environment_after_delivery,
                    "Stop-Error",
                    (KernelDiagnostic(
                        "EXECUTION-DELIVERY-LEDGER-MISMATCH",
                        "processed execution identity has no unique canonical evidence record",
                    ),),
                )
            canonical = canonical_evidence[0]
            action = self.model.actions.get(canonical.snapshot.action_id)
            if action is None:
                return SessionResult(
                    state,
                    environment_after_delivery,
                    "Stop-Error",
                    (KernelDiagnostic(
                        "EXECUTION-DELIVERY-LEDGER-MISMATCH",
                        "canonical processed evidence does not name a current model action",
                    ),),
                )
            ingress_error = _incoming_record_error(record, action=action)
            if (
                ingress_error is not None
                or not _strict_visible_execution_record_equal(record, canonical.execution)
            ):
                return SessionResult(
                    state,
                    environment_after_delivery,
                    "Stop-Error",
                    (KernelDiagnostic(
                        "CONFLICTING-EXECUTION-DELIVERY",
                        "inbound execution delivery is not a type-exact canonical processed record",
                    ),),
                )
            return SessionResult(
                state,
                environment_after_delivery,
                None,
                (KernelDiagnostic(
                    "DUPLICATE-EXECUTION-EVIDENCE",
                    "already processed execution delivery was discarded before admission",
                ),),
            )
        return SessionResult(
            state,
            environment_after_delivery,
            "Stop-Error",
            (KernelDiagnostic(
                "UNEXPECTED-EXECUTION-DELIVERY",
                "inbound delivery does not match an already processed execution identity",
            ),),
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
        if not isinstance(state.authority_identity, str) or state.authority_identity != self._authority_identity:
            return KernelDiagnostic("SESSION-AUTHORITY-MISMATCH", "state does not retain this session's exact authority binding")
        if not isinstance(state.seed_identity, str) or state.seed_identity != self._seed_identity:
            return KernelDiagnostic("SESSION-SEED-MISMATCH", "state does not retain this session's frozen S0 seed identity")
        if not isinstance(state.resources, ResourceState) or state.resources.mode not in {"ROUNDS", "BUDGET"} or (
            isinstance(state.resources.remaining, bool)
            or not isinstance(state.resources.remaining, int)
            or state.resources.remaining < 0
        ):
            return KernelDiagnostic("INVALID-RESOURCE-STATE", "state resource mode or remainder is invalid")
        try:
            normalized_context = SessionContext.create(
                session_id=context.session_id,
                run_id=context.run_id,
                experiment_attempt_id=context.experiment_attempt_id,
                model_identity=context.model_identity,
                current_summary=context.current_summary,
                q_status=context.q_status,
                resource_remainder=context.resource_remainder,
                retry_count=context.retry_count,
                retry_cap=context.retry_cap,
                known_target=context.known_target,
                known_evidence=context.known_evidence,
                error_history=context.error_history,
                unknown_history=context.unknown_history,
            )
        except (AttributeError, TypeError, ValueError) as exc:
            return KernelDiagnostic("INVALID-SESSION-CONTEXT", str(exc) or type(exc).__name__)
        if normalized_context != context:
            return KernelDiagnostic("INVALID-SESSION-CONTEXT", "state context is not an immutable normalized session context")
        if context.resource_remainder != state.resources.remaining:
            return KernelDiagnostic("RESOURCE-CONTEXT-MISMATCH", "session context does not retain the charged resource remainder")
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
        # The target context may deliberately be a fresh, equivalent verified
        # model whose local provenance cache contains only S0.  A resumed
        # public checkpoint must therefore be verified against the detached
        # causal replay below, rather than requiring its derived source
        # records to have been written to this target's mutable cache first.
        return self._evidence_lineage_error(state, frontier_bundles)

    def _execution_model(
        self, state: SessionState,
    ) -> tuple[FiniteSessionModel | None, KernelDiagnostic | None]:
        """Select the verified context used to propagate a public state.

        A locally produced state retains its already verified source-record
        closure in this session's model context.  A portable public checkpoint
        may instead carry derived records that were causally verified in an
        isolated replay but must never be copied into a fresh target's mutable
        cache.  The latter continues with that detached verified context.
        """

        try:
            frontier_bundles = {
                hypothesis: _frontier_bundle(bundle)
                for hypothesis, bundle in state.frontiers.items()
            }
        except (AttributeError, TypeError, ValueError) as exc:
            return None, KernelDiagnostic("INVALID-FRONTIER-BUNDLE", str(exc) or type(exc).__name__)
        local_closure = all(
            self.model.context.provenance_store.verify_entry(self.model.context, frontier) is None
            for paths in frontier_bundles.values()
            for frontier in paths
        )
        if local_closure:
            return self.model, None
        replay_model = _replay_model(self.model)
        replay_error = self._evidence_lineage_error(
            state, frontier_bundles, replay_model=replay_model,
        )
        if replay_error is not None:
            return None, replay_error
        return replay_model, None

    def _evidence_lineage_error(
        self,
        state: SessionState,
        current_frontiers: Mapping[str, tuple[FrontierEntry, ...]],
        *,
        replay_model: FiniteSessionModel | None = None,
    ) -> KernelDiagnostic | None:
        """Replay the public causal prefix before accepting a resumed state.

        A current frontier that belongs to the model is insufficient: it must
        be the successor of this session's retained evidence.  Replaying the
        bounded, public evidence ledger binds summary, resources, snapshots,
        actions, history and frontier provenance without pretending to create
        a cryptographic tamper-proof store.
        """

        replay_model = _replay_model(self.model) if replay_model is None else replay_model
        context = self.initial_state.context
        history = self.initial_state.history
        frontiers: Mapping[str, tuple[FrontierEntry, ...]] = self.initial_state.frontiers
        resources = self.initial_state.resources
        processed_ids: frozenset[str] = frozenset()

        def s7_expected(code: str, record: VisibleExecutionRecord) -> tuple[HistoryHandle, SessionContext, str | None]:
            expected_history = self._conservative_history(history)
            expected_context = self._context_after_retry(
                context,
                charged_resources,
                error_entry=f"{code}:{record.evidence_ref}",
                make_unknown=True,
            )
            expected_stop = (
                "Stop-Error"
                if expected_context.retry_count >= expected_context.retry_cap
                else None
            )
            return expected_history, expected_context, expected_stop

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
                or not isinstance(item.resolution_code, str)
                or not item.resolution_code
            ):
                return KernelDiagnostic("INVALID-EVIDENCE-RECORD", "evidence ledger item has an invalid public field type")
            action = replay_model.actions.get(item.snapshot.action_id)
            if action is None or item.snapshot.action_kind != action.kind:
                return KernelDiagnostic("EVIDENCE-ACTION-MISMATCH", "evidence snapshot does not name a current model action")
            prefix = SessionState(
                context, history, frontiers, resources, index - 1, processed_ids, (),
                self._authority_identity, self._seed_identity,
            )
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

            # An adapter/tool failure is represented by a deliberately narrow
            # placeholder record.  It is still charged and must replay the
            # exact named S7 branch, not the pre-B/C-2 terminal shortcut.
            if _is_expected_error_record(item.execution, item.snapshot, expected_execution_id):
                if item.resolution_code not in _CHARGED_ERROR_CODES:
                    return KernelDiagnostic("EVIDENCE-ERROR-MISMATCH", "canonical charged error record uses an uncontrolled resolution code")
                expected_history, expected_context, expected_stop = s7_expected(item.resolution_code, item.execution)
                if (
                    item.committed
                    or item.history_after != expected_history
                    or item.summary_after is not None
                    or item.stop_reason != expected_stop
                ):
                    return KernelDiagnostic("EVIDENCE-ERROR-MISMATCH", "rejected execution evidence does not close over its S7 retry transition")
                context = expected_context
                history = expected_history
                resources = charged_resources
                processed_ids = processed_ids | {expected_execution_id}
                if expected_stop is not None and index != len(state.evidence):
                    return KernelDiagnostic("EVIDENCE-TERMINAL-MISMATCH", "a retry-cap error evidence item cannot have a later causal round")
                continue

            record_error = _incoming_record_error(item.execution, action=action)
            if record_error is not None:
                return KernelDiagnostic("EVIDENCE-RECORD-MISMATCH", record_error.message)
            if item.execution.action_id != action.action_id:
                return KernelDiagnostic("EVIDENCE-ACTION-MISMATCH", "visible execution action differs from the admitted action")

            if item.execution.effect_class == "CONFIRMED-NOT-SENT":
                expected_context = self._context_after_retry(
                    context,
                    charged_resources,
                    error_entry=f"CONFIRMED-NOT-SENT:{item.execution.evidence_ref}",
                    make_unknown=False,
                )
                expected_stop = (
                    "Stop-Error"
                    if expected_context.retry_count >= expected_context.retry_cap
                    else None
                )
                if (
                    item.resolution_code != "CONFIRMED-NOT-SENT"
                    or item.rejected_response is not None
                    or item.committed
                    or item.history_after != history
                    or item.summary_after != expected_context.current_summary
                    or item.stop_reason != expected_stop
                ):
                    return KernelDiagnostic("EVIDENCE-NOT-SENT-MISMATCH", "confirmed-not-sent evidence does not preserve its summary/history retry contract")
                context = expected_context
                resources = charged_resources
                processed_ids = processed_ids | {expected_execution_id}
                if expected_stop is not None and index != len(state.evidence):
                    return KernelDiagnostic("EVIDENCE-TERMINAL-MISMATCH", "a retry-cap non-send evidence item cannot have a later causal round")
                continue

            if item.execution.effect_class == "UNKNOWN-EFFECT":
                expected_history, expected_context, expected_stop = s7_expected("UNKNOWN-EFFECT", item.execution)
                if (
                    item.resolution_code != "UNKNOWN-EFFECT"
                    or item.rejected_response is not None
                    or item.committed
                    or item.history_after != expected_history
                    or item.summary_after is not None
                    or item.stop_reason != expected_stop
                ):
                    return KernelDiagnostic("EVIDENCE-UNKNOWN-MISMATCH", "unknown-effect evidence does not close over its S7 retry transition")
                context = expected_context
                history = expected_history
                resources = charged_resources
                processed_ids = processed_ids | {expected_execution_id}
                if expected_stop is not None and index != len(state.evidence):
                    return KernelDiagnostic("EVIDENCE-TERMINAL-MISMATCH", "a retry-cap unknown-effect evidence item cannot have a later causal round")
                continue

            recovery = item.execution.prep_recover
            recovery_error_code: str | None = None
            if action.kind in {"PREP", "RECOVER"}:
                assert isinstance(recovery, PrepRecoverResult)
                if recovery.prep_error or recovery.ineligible:
                    recovery_error_code = "PREP-RECOVER-ERROR"
                elif action.kind == "PREP" and not recovery.summary_confirmed:
                    recovery_error_code = "PREP-SUMMARY-UNCONFIRMED"
                elif action.kind == "RECOVER" and (
                    not recovery.target_confirmed or not recovery.summary_confirmed
                ):
                    recovery_error_code = "RECOVER-TARGET-UNCONFIRMED"
            if recovery_error_code is not None:
                expected_history, expected_context, expected_stop = s7_expected(recovery_error_code, item.execution)
                if (
                    item.resolution_code != recovery_error_code
                    or item.rejected_response is not None
                    or item.committed
                    or item.history_after != expected_history
                    or item.summary_after is not None
                    or item.stop_reason != expected_stop
                ):
                    return KernelDiagnostic("EVIDENCE-RECOVERY-MISMATCH", "Prep/Recover evidence does not close over its S7 retry transition")
                context = expected_context
                history = expected_history
                resources = charged_resources
                processed_ids = processed_ids | {expected_execution_id}
                if expected_stop is not None and index != len(state.evidence):
                    return KernelDiagnostic("EVIDENCE-TERMINAL-MISMATCH", "a retry-cap recovery evidence item cannot have a later causal round")
                continue

            if item.execution.observable is None:
                try:
                    next_history, next_frontiers, _summary_diagnostics = self._summary_only_transition(
                        model=replay_model,
                        history=history,
                        frontiers=frontiers,
                        action=action,
                        snapshot=item.snapshot,
                        prediction=admission.prediction,
                    )
                except (TypeError, ValueError) as exc:
                    return KernelDiagnostic(
                        "EVIDENCE-SUMMARY-ONLY-MISMATCH",
                        str(exc) or type(exc).__name__,
                    )
            else:
                selected_class, interpretation_error = _matching_class(item.snapshot, item.execution)
                if selected_class is None:
                    assert interpretation_error is not None
                    expected_history, expected_context, expected_stop = s7_expected(
                        interpretation_error.code, item.execution,
                    )
                    if (
                        item.resolution_code != interpretation_error.code
                        or item.rejected_response != item.execution
                        or item.committed
                        or item.history_after != expected_history
                        or item.summary_after is not None
                        or item.stop_reason != expected_stop
                    ):
                        return KernelDiagnostic("EVIDENCE-INTERPRETATION-MISMATCH", "rejected observation does not close over its S7 retry transition")
                    context = expected_context
                    history = expected_history
                    resources = charged_resources
                    processed_ids = processed_ids | {expected_execution_id}
                    if expected_stop is not None and index != len(state.evidence):
                        return KernelDiagnostic("EVIDENCE-TERMINAL-MISMATCH", "a retry-cap rejected-observation item cannot have a later causal round")
                    continue
                next_history = self._history_for_class(history, selected_class)
                next_frontiers = MappingProxyType(dict(selected_class.successors))

            if item.rejected_response is not None:
                return KernelDiagnostic("EVIDENCE-REJECTED-RESPONSE", "accepted execution evidence cannot also retain a rejected response")
            context_before_s9 = self._context_with_resource(context, charged_resources)
            s8_adoption = (
                self._s8_recover_known(recovery)
                if action.kind == "RECOVER"
                else None
            )
            try:
                next_context = self._s9_commit_summary(
                    context_before_s9,
                    item.execution.post_summary,
                    s8_adoption=s8_adoption,
                )
            except (TypeError, ValueError) as exc:
                return KernelDiagnostic("EVIDENCE-COMMIT-MISMATCH", str(exc) or type(exc).__name__)
            expected_stop = self._normal_stop_reason(next_history)
            if (
                item.resolution_code != "COMMIT"
                or not item.committed
                or item.history_after != next_history
                or item.summary_after != next_context.current_summary
                or item.stop_reason != expected_stop
            ):
                return KernelDiagnostic("EVIDENCE-COMMIT-MISMATCH", "committed evidence does not match its derived S8/S9 history update")
            context = next_context
            history = next_history
            frontiers = next_frontiers
            resources = charged_resources
            processed_ids = processed_ids | {expected_execution_id}
            if expected_stop is not None and index != len(state.evidence):
                return KernelDiagnostic("EVIDENCE-TERMINAL-MISMATCH", "a terminal committed evidence item cannot have a later causal round")

        if (
            state.context != context
            or state.history != history
            or dict(current_frontiers) != dict(frontiers)
            or state.resources != resources
            or state.processed_execution_attempt_ids != processed_ids
        ):
            return KernelDiagnostic("SESSION-LINEAGE-MISMATCH", "resumed state is not the terminal state of its evidence lineage")
        # Keep full provenance verification, but perform it over the
        # canonical frontier records rebuilt in the detached replay context.
        # This accepts a valid portable public checkpoint without mutating or
        # depending on the target session's local cache.
        for paths in frontiers.values():
            for frontier in paths:
                provenance_error = replay_model.context.provenance_store.verify_entry(
                    replay_model.context, frontier,
                )
                if provenance_error is not None:
                    return provenance_error
        return None

    def _step(
        self,
        state: SessionState,
        environment: SyntheticEnvironment,
        *,
        model: FiniteSessionModel,
    ) -> SessionResult:
        terminal = self._retained_terminal_result(state, environment)
        if terminal is not None:
            return terminal
        if state.context.q_status == "KNOWN" and state.context.current_summary is None:
            return SessionResult(
                state, environment, "Stop-Error",
                (KernelDiagnostic("UNRESOLVED-SESSION-SUMMARY", "known summary is required for TEST selection"),),
            )
        admission = self._admit(state, model=model)
        if admission.action is None or admission.prediction is None:
            stop_reason = {
                "PREDICTION-GAP": "Stop-Prediction-Gap",
                "A2-UNAFFORDABLE": "Stop-Budget",
                "A5-UNAFFORDABLE-RECOVER": "Stop-Budget",
                "A4-NO-ELIGIBLE-RECOVER": "Stop-Error",
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
            model_identity=model.identity,
            uncertainty_identity=model.uncertainty_identity,
            uncertainty_digest=model.uncertainty_digest,
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

        return self._post_dispatch(
            state=state,
            environment=environment,
            model=model,
            snapshot=snapshot,
            prediction=prediction,
            action=action,
            resource_before=resource_before,
            resource_after=resource_after,
            charged_resources=charged_resources,
            execution_attempt_id=execution_attempt_id,
            diagnostics=diagnostics,
            execution=execution,
        )

    def _post_dispatch(
        self,
        *,
        state: SessionState,
        environment: SyntheticEnvironment,
        model: FiniteSessionModel,
        snapshot: SelectSnapshot,
        prediction: ActionPrediction,
        action: SyntheticAction,
        resource_before: AlgorithmResourceView,
        resource_after: AlgorithmResourceView,
        charged_resources: ResourceState,
        execution_attempt_id: str,
        diagnostics: list[KernelDiagnostic],
        execution: object,
    ) -> SessionResult:
        """Close every ordinary failure after S4 over the issued attempt."""

        try:
            return self._consume_execution(
                state=state,
                environment=environment,
                model=model,
                snapshot=snapshot,
                prediction=prediction,
                action=action,
                resource_before=resource_before,
                resource_after=resource_after,
                charged_resources=charged_resources,
                execution_attempt_id=execution_attempt_id,
                diagnostics=diagnostics,
                execution=execution,
            )
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
                code="POST-DISPATCH-ERROR",
                message=str(exc) or type(exc).__name__,
                execution_record=_visible_execution_record(execution),
                environment_after_execution=_returned_environment(execution),
            )

    def _consume_execution(
        self,
        *,
        state: SessionState,
        environment: SyntheticEnvironment,
        model: FiniteSessionModel,
        snapshot: SelectSnapshot,
        prediction: ActionPrediction,
        action: SyntheticAction,
        resource_before: AlgorithmResourceView,
        resource_after: AlgorithmResourceView,
        charged_resources: ResourceState,
        execution_attempt_id: str,
        diagnostics: list[KernelDiagnostic],
        execution: object,
    ) -> SessionResult:
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
        record_error = _incoming_record_error(execution.record, action=action)
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
                message="execution result attempt/action identity is invalid",
                execution_record=execution.record,
                environment_after_execution=execution.successor,
            )
        if execution.record.effect_class == "CONFIRMED-NOT-SENT":
            return self._retry_after_not_sent(
                state=state,
                environment_after_execution=execution.successor,
                snapshot=snapshot,
                prediction=prediction,
                action=action,
                resource_before=resource_before,
                resource_after=resource_after,
                charged_resources=charged_resources,
                execution_attempt_id=execution_attempt_id,
                diagnostics=diagnostics,
                execution_record=execution.record,
            )

        if execution.record.effect_class == "UNKNOWN-EFFECT":
            return self._s7_retry(
                state=state,
                environment_after_execution=execution.successor,
                snapshot=snapshot,
                prediction=prediction,
                action=action,
                resource_before=resource_before,
                resource_after=resource_after,
                charged_resources=charged_resources,
                execution_attempt_id=execution_attempt_id,
                diagnostics=diagnostics,
                execution_record=execution.record,
                code="UNKNOWN-EFFECT",
                message="synthetic execution did not confirm a successor summary",
            )

        if action.kind in {"PREP", "RECOVER"}:
            recovery = execution.record.prep_recover
            assert isinstance(recovery, PrepRecoverResult)
            if recovery.prep_error or recovery.ineligible:
                return self._s7_retry(
                    state=state,
                    environment_after_execution=execution.successor,
                    snapshot=snapshot,
                    prediction=prediction,
                    action=action,
                    resource_before=resource_before,
                    resource_after=resource_after,
                    charged_resources=charged_resources,
                    execution_attempt_id=execution_attempt_id,
                    diagnostics=diagnostics,
                    execution_record=execution.record,
                    code="PREP-RECOVER-ERROR",
                    message="Prep/Recover returned a declared error or ineligible result",
                )
            if action.kind == "PREP" and not recovery.summary_confirmed:
                return self._s7_retry(
                    state=state,
                    environment_after_execution=execution.successor,
                    snapshot=snapshot,
                    prediction=prediction,
                    action=action,
                    resource_before=resource_before,
                    resource_after=resource_after,
                    charged_resources=charged_resources,
                    execution_attempt_id=execution_attempt_id,
                    diagnostics=diagnostics,
                    execution_record=execution.record,
                    code="PREP-SUMMARY-UNCONFIRMED",
                    message="Prep did not confirm its actual successor summary",
                )
            if action.kind == "RECOVER" and (
                not recovery.target_confirmed or not recovery.summary_confirmed
            ):
                return self._s7_retry(
                    state=state,
                    environment_after_execution=execution.successor,
                    snapshot=snapshot,
                    prediction=prediction,
                    action=action,
                    resource_before=resource_before,
                    resource_after=resource_after,
                    charged_resources=charged_resources,
                    execution_attempt_id=execution_attempt_id,
                    diagnostics=diagnostics,
                    execution_record=execution.record,
                    code="RECOVER-TARGET-UNCONFIRMED",
                    message="Recover did not confirm both its target and successor summary",
                )

        if not execution.record.summary_confirmed or not isinstance(execution.record.post_summary, str) or not execution.record.post_summary:
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
                message="confirmed execution did not return a nonempty successor summary",
                execution_record=execution.record,
                environment_after_execution=execution.successor,
            )
        return self._commit_confirmed_execution(
            state=state,
            environment_after_execution=execution.successor,
            model=model,
            snapshot=snapshot,
            prediction=prediction,
            action=action,
            resource_before=resource_before,
            resource_after=resource_after,
            charged_resources=charged_resources,
            execution_attempt_id=execution_attempt_id,
            diagnostics=diagnostics,
            execution_record=execution.record,
        )

    def _retry_after_not_sent(
        self,
        *,
        state: SessionState,
        environment_after_execution: SyntheticEnvironment,
        snapshot: SelectSnapshot,
        prediction: ActionPrediction,
        action: SyntheticAction,
        resource_before: AlgorithmResourceView,
        resource_after: AlgorithmResourceView,
        charged_resources: ResourceState,
        execution_attempt_id: str,
        diagnostics: list[KernelDiagnostic],
        execution_record: VisibleExecutionRecord,
    ) -> SessionResult:
        """Apply the narrow CONFIRMED-NOT-SENT branch without invoking recovery.

        This is intentionally distinct from S7.  The returned record proves
        that no action was sent, so it cannot turn an already known summary or
        compatible history into an UNKNOWN result.  It nevertheless consumes
        the issued attempt's one charge and retry allowance.
        """

        next_context = self._context_after_retry(
            state.context,
            charged_resources,
            error_entry=f"CONFIRMED-NOT-SENT:{execution_record.evidence_ref}",
            make_unknown=False,
        )
        stop_reason = "Stop-Error" if next_context.retry_count >= next_context.retry_cap else None
        evidence = RoundEvidence(
            snapshot, prediction, execution_record, True, True, resource_before, resource_after,
            action.detail_charges, action.projected_cost(), state.history, state.history,
            next_context.current_summary, False, stop_reason,
            resolution_code="CONFIRMED-NOT-SENT",
        )
        next_state = SessionState(
            next_context, state.history, state.frontiers, charged_resources,
            state.attempts + 1, state.processed_execution_attempt_ids | {execution_attempt_id}, state.evidence + (evidence,),
            self._authority_identity, self._seed_identity,
        )
        return SessionResult(
            next_state,
            environment_after_execution,
            stop_reason,
            tuple(diagnostics + [KernelDiagnostic(
                "CONFIRMED-NOT-SENT", "environment confirmed that no action was sent",
            )]),
        )

    def _s7_retry(
        self,
        *,
        state: SessionState,
        environment_after_execution: SyntheticEnvironment,
        snapshot: SelectSnapshot,
        prediction: ActionPrediction,
        action: SyntheticAction,
        resource_before: AlgorithmResourceView,
        resource_after: AlgorithmResourceView,
        charged_resources: ResourceState,
        execution_attempt_id: str,
        diagnostics: list[KernelDiagnostic],
        execution_record: VisibleExecutionRecord,
        code: str,
        message: str,
        rejected_response: VisibleExecutionRecord | None = None,
    ) -> SessionResult:
        """Apply the single S7 path after an issued but unresolved action."""

        next_history = self._conservative_history(state.history)
        next_context = self._context_after_retry(
            state.context,
            charged_resources,
            error_entry=f"{code}:{execution_record.evidence_ref}",
            make_unknown=True,
        )
        stop_reason = "Stop-Error" if next_context.retry_count >= next_context.retry_cap else None
        evidence = RoundEvidence(
            snapshot, prediction, execution_record, True, True, resource_before, resource_after,
            action.detail_charges, action.projected_cost(), state.history, next_history,
            None, False, stop_reason, rejected_response, code,
        )
        next_state = SessionState(
            next_context, next_history, state.frontiers, charged_resources,
            state.attempts + 1, state.processed_execution_attempt_ids | {execution_attempt_id}, state.evidence + (evidence,),
            self._authority_identity, self._seed_identity,
        )
        return SessionResult(
            next_state,
            environment_after_execution,
            stop_reason,
            tuple(diagnostics + [KernelDiagnostic(code, message)]),
        )

    def _commit_confirmed_execution(
        self,
        *,
        state: SessionState,
        environment_after_execution: SyntheticEnvironment,
        model: FiniteSessionModel,
        snapshot: SelectSnapshot,
        prediction: ActionPrediction,
        action: SyntheticAction,
        resource_before: AlgorithmResourceView,
        resource_after: AlgorithmResourceView,
        charged_resources: ResourceState,
        execution_attempt_id: str,
        diagnostics: list[KernelDiagnostic],
        execution_record: VisibleExecutionRecord,
    ) -> SessionResult:
        """Apply S8 (when needed) and S9 from a confirmed normalized outcome."""

        if execution_record.observable is None:
            next_history, next_frontiers, summary_diagnostics = self._summary_only_transition(
                model=model,
                history=state.history,
                frontiers=state.frontiers,
                action=action,
                snapshot=snapshot,
                prediction=prediction,
            )
            diagnostics.extend(summary_diagnostics)
        else:
            selected_class, interpretation_error = _matching_class(snapshot, execution_record)
            if selected_class is None:
                assert interpretation_error is not None
                return self._s7_retry(
                    state=state,
                    environment_after_execution=environment_after_execution,
                    snapshot=snapshot,
                    prediction=prediction,
                    action=action,
                    resource_before=resource_before,
                    resource_after=resource_after,
                    charged_resources=charged_resources,
                    execution_attempt_id=execution_attempt_id,
                    diagnostics=diagnostics,
                    execution_record=execution_record,
                    code=interpretation_error.code,
                    message=interpretation_error.message,
                    rejected_response=execution_record,
                )
            next_history = self._history_for_class(state.history, selected_class)
            next_frontiers = MappingProxyType(dict(selected_class.successors))

        context_before_s9 = self._context_with_resource(state.context, charged_resources)
        s8_adoption: _S8RecoveryAdoption | None = None
        if action.kind == "RECOVER":
            recovery = execution_record.prep_recover
            assert isinstance(recovery, PrepRecoverResult)
            # S8 is the only recovery branch permitted to restore KNOWN and
            # consume the declared target/evidence.  It deliberately does not
            # write current_summary; S9 below remains that sole writer.
            s8_adoption = self._s8_recover_known(recovery)
        next_context = self._s9_commit_summary(
            context_before_s9, execution_record.post_summary, s8_adoption=s8_adoption,
        )
        stop_reason = self._normal_stop_reason(next_history)
        evidence = RoundEvidence(
            snapshot, prediction, execution_record, True, True, resource_before, resource_after,
            action.detail_charges, action.projected_cost(), state.history, next_history,
            next_context.current_summary, True, stop_reason,
            resolution_code="COMMIT",
        )
        next_state = SessionState(
            next_context, next_history, next_frontiers, charged_resources,
            state.attempts + 1, state.processed_execution_attempt_ids | {execution_attempt_id}, state.evidence + (evidence,),
            self._authority_identity, self._seed_identity,
        )
        return SessionResult(next_state, environment_after_execution, stop_reason, tuple(diagnostics))

    @staticmethod
    def _normal_stop_reason(history: HistoryHandle) -> str | None:
        return "Stop-Empty" if not history.hypotheses else (
            "Stop-Singleton" if len(history.hypotheses) == 1 else None
        )

    @staticmethod
    def _history_for_class(history: HistoryHandle, selected_class: PredictionClass) -> HistoryHandle:
        return HistoryHandle.committed(
            hypotheses=selected_class.hypotheses,
            compatible_state_by_hypothesis={
                hypothesis: tuple(entry.history_provenance[-1] for entry in entries)
                for hypothesis, entries in selected_class.successors.items()
            },
            status_by_hypothesis={
                hypothesis: (
                    "CONSERVATIVE-UNKNOWN"
                    if (
                        hypothesis in selected_class.conservative_hypotheses
                        or history.status_by_hypothesis.get(hypothesis) == "CONSERVATIVE-UNKNOWN"
                        or any(
                            entry.status == "CONSERVATIVE-UNKNOWN"
                            for entry in selected_class.successors[hypothesis]
                        )
                    )
                    else "KNOWN"
                )
                for hypothesis in selected_class.hypotheses
            },
            version=history.version + 1,
        )

    @staticmethod
    def _summary_only_transition(
        *,
        model: FiniteSessionModel,
        history: HistoryHandle,
        frontiers: Mapping[str, tuple[FrontierEntry, ...]],
        action: SyntheticAction,
        snapshot: SelectSnapshot,
        prediction: ActionPrediction,
    ) -> tuple[
        HistoryHandle,
        Mapping[str, tuple[FrontierEntry, ...]],
        tuple[KernelDiagnostic, ...],
    ]:
        """Commit an executed Prep/Recover transition without an ``I_z`` class.

        The summary belongs solely to S9.  This helper instead consumes the
        selected action's frozen finite transition for every current path,
        preserving ``H`` while making an unresolved member conservative.  It
        is used by both the live S9 branch and public-ledger replay.
        """

        if (
            action.kind not in {"PREP", "RECOVER"}
            or snapshot.action_id != action.action_id
            or snapshot.action_kind != action.kind
            or prediction.action_id != action.action_id
            or snapshot.classes != prediction.classes
            or snapshot.hypotheses != history.hypotheses
        ):
            raise ValueError("summary-only transition does not match its frozen admitted action")
        propagated = model.summary_only_successors(
            hypotheses=history.hypotheses,
            frontiers=frontiers,
            status_by_hypothesis=history.status_by_hypothesis,
            action_id=action.action_id,
        )
        if propagated.action_id != action.action_id or set(propagated.successors) != set(history.hypotheses):
            raise ValueError("summary-only transition did not retain every current hypothesis")
        if any(not paths for paths in propagated.successors.values()):
            raise ValueError("summary-only transition produced an empty frontier bundle")

        next_frontiers = MappingProxyType({
            hypothesis: tuple(propagated.successors[hypothesis])
            for hypothesis in sorted(history.hypotheses)
        })
        next_history = HistoryHandle.committed(
            hypotheses=history.hypotheses,
            compatible_state_by_hypothesis={
                hypothesis: tuple(entry.history_provenance[-1] for entry in next_frontiers[hypothesis])
                for hypothesis in history.hypotheses
            },
            status_by_hypothesis={
                hypothesis: (
                    "CONSERVATIVE-UNKNOWN"
                    if hypothesis in propagated.conservative_hypotheses
                    else "KNOWN"
                )
                for hypothesis in history.hypotheses
            },
            version=history.version + 1,
        )
        return next_history, next_frontiers, propagated.diagnostics

    @staticmethod
    def _conservative_history(history: HistoryHandle) -> HistoryHandle:
        """Preserve H/frontiers while marking every retained member uncertain."""

        # S7 is the error-containment path.  It must remain available even if
        # a later normal-commit helper fails while constructing a derived
        # HistoryHandle (for example an adapter regression during S9
        # preparation).  The input history was already validated at S0/S6;
        # build the simple, lossless conservative successor directly instead
        # of re-entering the fallible normal-commit factory.
        return HistoryHandle(
            hypotheses=history.hypotheses,
            compatible_state_by_hypothesis=history.compatible_state_by_hypothesis,
            status_by_hypothesis=MappingProxyType({
                hypothesis: "CONSERVATIVE-UNKNOWN" for hypothesis in history.hypotheses
            }),
            version=history.version + 1,
            processed=True,
        )

    @staticmethod
    def _context_with_resource(context: SessionContext, resources: ResourceState) -> SessionContext:
        return SessionContext.create(
            session_id=context.session_id,
            run_id=context.run_id,
            experiment_attempt_id=context.experiment_attempt_id,
            model_identity=context.model_identity,
            current_summary=context.current_summary,
            q_status=context.q_status,
            resource_remainder=resources.remaining,
            retry_count=context.retry_count,
            retry_cap=context.retry_cap,
            known_target=context.known_target,
            known_evidence=context.known_evidence,
            error_history=context.error_history,
            unknown_history=context.unknown_history,
        )

    @staticmethod
    def _context_after_retry(
        context: SessionContext,
        resources: ResourceState,
        *,
        error_entry: str,
        make_unknown: bool,
    ) -> SessionContext:
        return SessionContext.create(
            session_id=context.session_id,
            run_id=context.run_id,
            experiment_attempt_id=context.experiment_attempt_id,
            model_identity=context.model_identity,
            current_summary=None if make_unknown else context.current_summary,
            q_status="UNKNOWN" if make_unknown else context.q_status,
            resource_remainder=resources.remaining,
            retry_count=context.retry_count + 1,
            retry_cap=context.retry_cap,
            known_target=None if make_unknown else context.known_target,
            known_evidence=() if make_unknown else context.known_evidence,
            error_history=context.error_history + (error_entry,),
            unknown_history=(
                context.unknown_history + (error_entry,)
                if make_unknown else context.unknown_history
            ),
        )

    @staticmethod
    def _s8_recover_known(recovery: PrepRecoverResult) -> _S8RecoveryAdoption:
        return _S8RecoveryAdoption(
            q_status="KNOWN",
            known_target=recovery.declared_target,
            known_evidence=(recovery.evidence,),
        )

    @staticmethod
    def _s9_commit_summary(
        context: SessionContext,
        post_summary: str | None,
        *,
        s8_adoption: _S8RecoveryAdoption | None = None,
    ) -> SessionContext:
        q_status = context.q_status if s8_adoption is None else s8_adoption.q_status
        known_target = context.known_target if s8_adoption is None else s8_adoption.known_target
        known_evidence = context.known_evidence if s8_adoption is None else s8_adoption.known_evidence
        if q_status != "KNOWN" or not isinstance(post_summary, str) or not post_summary:
            raise ValueError("S9 requires a KNOWN context and a confirmed successor summary")
        return SessionContext.create(
            session_id=context.session_id,
            run_id=context.run_id,
            experiment_attempt_id=context.experiment_attempt_id,
            model_identity=context.model_identity,
            current_summary=post_summary,
            q_status=q_status,
            resource_remainder=context.resource_remainder,
            retry_count=context.retry_count,
            retry_cap=context.retry_cap,
            known_target=known_target,
            known_evidence=known_evidence,
            error_history=context.error_history,
            unknown_history=context.unknown_history,
        )

    def _admit(
        self, state: SessionState, *, model: FiniteSessionModel | None = None,
    ) -> AdmissionDecision:
        """Apply the shared A1--A5 table without mutating a session.

        A known session can select a scored TEST or an unscored PREP fallback.
        An unknown session deliberately takes the separate Recover branch: its
        action is declared eligible, never inferred from a stale summary, and
        it is not scored as an observation-minimax TEST.
        """

        current_model = self.model if model is None else model
        diagnostics: list[KernelDiagnostic] = []

        if state.context.q_status == "UNKNOWN":
            recover_candidates: list[tuple[SyntheticAction, ActionPrediction]] = []
            declared_recover_seen = False
            eligible_recover_seen = False
            unaffordable_recover_seen = False
            for action in current_model.actions.values():
                if action.kind != "RECOVER":
                    continue
                declared_recover_seen = True
                if not action.recover_when_unknown:
                    continue
                eligible_recover_seen = True
                prediction = current_model.predict(
                    hypotheses=state.history.hypotheses,
                    frontiers=state.frontiers,
                    status_by_hypothesis=state.history.status_by_hypothesis,
                    action_id=action.action_id,
                )
                diagnostics.extend(prediction.diagnostics)
                if state.resources.can_afford(action):
                    recover_candidates.append((action, prediction))
                else:
                    unaffordable_recover_seen = True
            if recover_candidates:
                action, prediction = min(
                    recover_candidates, key=lambda item: (item[0].cost, item[0].action_id),
                )
                return AdmissionDecision("RECOVER", action, prediction, "RECOVER-ADMITTED", tuple(diagnostics))
            if eligible_recover_seen and unaffordable_recover_seen:
                return AdmissionDecision(
                    "ADMIT", None, None, "A5-UNAFFORDABLE-RECOVER",
                    tuple(diagnostics + [KernelDiagnostic(
                        "ADMISSION-A5-UNAFFORDABLE-RECOVER",
                        "an UNKNOWN session has an eligible but unaffordable Recover action",
                    )]),
                )
            reason = "A4-NO-ELIGIBLE-RECOVER"
            detail = (
                "UNKNOWN session has only ineligible declared Recover actions"
                if declared_recover_seen else "UNKNOWN session has no declared Recover action"
            )
            return AdmissionDecision(
                "ADMIT", None, None, reason,
                tuple(diagnostics + [KernelDiagnostic("ADMISSION-A4-NO-ELIGIBLE-RECOVER", detail)]),
            )

        if state.context.q_status != "KNOWN" or state.context.current_summary is None:
            return AdmissionDecision(
                "ADMIT", None, None, "INVALID-SESSION-STATUS",
                tuple(diagnostics + [KernelDiagnostic("INVALID-SESSION-STATUS", "session is neither KNOWN nor UNKNOWN")]),
            )

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
        return self._s7_retry(
            state=state,
            environment_after_execution=environment_after_execution or environment,
            snapshot=snapshot,
            prediction=prediction,
            action=action,
            resource_before=resource_before,
            resource_after=resource_after,
            charged_resources=charged_resources,
            execution_attempt_id=execution_attempt_id,
            diagnostics=diagnostics,
            execution_record=expected_record,
            code=code,
            message=message,
            rejected_response=execution_record,
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


def _session_authority_identity(
    binding: RuntimeAuthorityBinding, model: FiniteSessionModel,
) -> str:
    """Bind S0 to the exact controlled snapshots consumed by this session."""

    identities = binding.identities()
    payload = (
        model.identity,
        model.context.identity,
        tuple(
            (source, tuple(sorted(identity.items())))
            for source, identity in sorted(identities.items())
        ),
    )
    return sha256(repr(payload).encode("utf-8")).hexdigest()


def _session_seed_identity(
    *,
    context: SessionContext,
    history: HistoryHandle,
    frontiers: Mapping[str, tuple[FrontierEntry, ...]],
    resources: ResourceState,
    authority_identity: str,
) -> str:
    """Freeze the declared public S0 seed without re-signing resumed state."""

    def path_key(path: FrontierEntry) -> tuple[object, ...]:
        return (
            path.hypothesis_id,
            path.control_state_id,
            tuple(
                (
                    name,
                    interval.lower.numerator,
                    interval.lower.denominator,
                    interval.upper.numerator,
                    interval.upper.denominator,
                    interval.lower_closed,
                    interval.upper_closed,
                )
                for name, interval in sorted(path.clocks.items())
            ),
            tuple(sorted((name, repr(value)) for name, value in path.typed_store.items())),
            path.path_length,
            path.history_provenance,
            path.status,
            path.model_identity,
        )

    payload = (
        authority_identity,
        context.session_id,
        context.run_id,
        context.experiment_attempt_id,
        context.model_identity,
        context.current_summary,
        context.q_status,
        context.resource_remainder,
        context.retry_count,
        context.retry_cap,
        context.known_target,
        context.known_evidence,
        context.error_history,
        context.unknown_history,
        tuple(sorted(history.hypotheses)),
        tuple(sorted(history.compatible_state_by_hypothesis.items())),
        tuple(sorted(history.status_by_hypothesis.items())),
        history.version,
        history.processed,
        tuple(
            (hypothesis, tuple(path_key(path) for path in bundle))
            for hypothesis, bundle in sorted(frontiers.items())
        ),
        resources.mode,
        resources.remaining,
    )
    return sha256(repr(payload).encode("utf-8")).hexdigest()


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


def _incoming_record_error(
    record: VisibleExecutionRecord, *, action: SyntheticAction,
) -> KernelDiagnostic | None:
    """Check the closed, visible execution-record combinations at S4/S8.

    The synthetic environment validates its own declarative outcomes, but an
    execution adapter is a public session boundary and may construct this
    dataclass directly.  Validate the same field and effect combinations here
    before any branch can treat a malformed record as a confirmed observation,
    a confirmed non-send, or a conservative unknown.
    """

    if any(
        not isinstance(value, str) or not value.strip()
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
    if record.effect_class != "NONE":
        if (
            record.observable is not None
            or record.summary_confirmed
            or record.post_summary is not None
            or record.measurement_tick is not None
            or record.uncertainty_identity is not None
            or record.prep_recover is not None
        ):
            return KernelDiagnostic(
                "INVALID-EXECUTION-RECORD",
                "non-normal execution cannot manufacture an observation, confirmation, summary, measurement, uncertainty, or recovery result",
            )
        return None

    if action.kind == "TEST":
        if record.prep_recover is not None:
            return KernelDiagnostic("INVALID-EXECUTION-RECORD", "TEST cannot carry a Prep/Recover result")
        if not isinstance(record.observable, str) or not record.observable:
            return KernelDiagnostic("INVALID-EXECUTION-RECORD", "normal TEST execution requires a nonempty visible observation")
        if not record.summary_confirmed:
            return KernelDiagnostic("INVALID-EXECUTION-RECORD", "normal TEST execution requires summary confirmation")
        if not isinstance(record.post_summary, str) or not record.post_summary:
            return KernelDiagnostic("SUMMARY-CONFIRMATION-ERROR", "confirmed normal TEST execution did not return a nonempty successor summary")
        if not isinstance(record.measurement_tick, Fraction):
            return KernelDiagnostic("INVALID-EXECUTION-RECORD", "normal TEST execution requires an exact measurement tick")
        if not isinstance(record.uncertainty_identity, str) or not record.uncertainty_identity.strip():
            return KernelDiagnostic("INVALID-EXECUTION-RECORD", "observed TEST execution must name a nonempty uncertainty identity")
        return None

    if action.kind not in {"PREP", "RECOVER"}:
        return KernelDiagnostic("INVALID-EXECUTION-RECORD", "execution action kind is outside the controlled vocabulary")
    result = record.prep_recover
    if not isinstance(result, PrepRecoverResult):
        return KernelDiagnostic("INVALID-EXECUTION-RECORD", "normal Prep/Recover execution requires a typed recovery result")
    if (
        not isinstance(result.target_confirmed, bool)
        or not isinstance(result.summary_confirmed, bool)
        or not isinstance(result.prep_error, bool)
        or not isinstance(result.ineligible, bool)
        or not isinstance(result.declared_target, str)
        or not result.declared_target.strip()
        or not isinstance(result.evidence, str)
        or not result.evidence.strip()
    ):
        return KernelDiagnostic("INVALID-EXECUTION-RECORD", "Prep/Recover result has an invalid confirmation, target, or evidence field")
    if result.declared_target != action.declared_target:
        return KernelDiagnostic("RECOVERY-TARGET-MISMATCH", "Prep/Recover result does not name the admitted action's declared target")
    if record.summary_confirmed != result.summary_confirmed or record.post_summary != result.post_summary:
        return KernelDiagnostic("INVALID-EXECUTION-RECORD", "visible and Prep/Recover summary fields disagree")
    if result.summary_confirmed:
        if not isinstance(result.post_summary, str) or not result.post_summary:
            return KernelDiagnostic("SUMMARY-CONFIRMATION-ERROR", "confirmed Prep/Recover result did not return a nonempty successor summary")
    elif result.post_summary is not None:
        return KernelDiagnostic("INVALID-EXECUTION-RECORD", "unconfirmed Prep/Recover result cannot carry a successor summary")
    if (result.prep_error or result.ineligible) and (result.target_confirmed or result.summary_confirmed):
        return KernelDiagnostic("INVALID-EXECUTION-RECORD", "failed Prep/Recover result cannot claim a confirmation")
    if record.observable is None:
        if record.measurement_tick is not None or record.uncertainty_identity is not None:
            return KernelDiagnostic(
                "INVALID-EXECUTION-RECORD",
                "summary-only Prep/Recover result cannot carry a measurement tick or uncertainty identity",
            )
    elif (
        not isinstance(record.observable, str)
        or not record.observable
        or not isinstance(record.measurement_tick, Fraction)
        or not isinstance(record.uncertainty_identity, str)
        or not record.uncertainty_identity.strip()
    ):
        return KernelDiagnostic(
            "INVALID-EXECUTION-RECORD",
            "Prep/Recover observation must pair a nonempty label, exact measurement tick, and uncertainty identity",
        )
    return None


def _strict_scalar_equal(actual: object, expected: object) -> bool:
    """Compare a closed scalar only after requiring its exact runtime type.

    Python deliberately equates ``True == 1`` and ``Fraction(0) == 0``.  That
    is useful arithmetic behavior, but it is not a safe identity relation for
    an already processed public execution record.
    """

    return type(actual) is type(expected) and actual == expected


def _strict_prep_recover_result_equal(actual: object, expected: object) -> bool:
    """Compare the nested recovery return without bool/int coercion."""

    if type(actual) is not PrepRecoverResult or type(expected) is not PrepRecoverResult:
        return False
    return all((
        _strict_scalar_equal(actual.target_confirmed, expected.target_confirmed),
        _strict_scalar_equal(actual.summary_confirmed, expected.summary_confirmed),
        _strict_scalar_equal(actual.prep_error, expected.prep_error),
        _strict_scalar_equal(actual.ineligible, expected.ineligible),
        _strict_scalar_equal(actual.declared_target, expected.declared_target),
        _strict_scalar_equal(actual.evidence, expected.evidence),
        _strict_scalar_equal(actual.post_summary, expected.post_summary),
    ))


def _strict_visible_execution_record_equal(actual: object, expected: object) -> bool:
    """Return true only for a type-exact closed visible-record copy."""

    if type(actual) is not VisibleExecutionRecord or type(expected) is not VisibleExecutionRecord:
        return False
    return all((
        _strict_scalar_equal(actual.execution_attempt_id, expected.execution_attempt_id),
        _strict_scalar_equal(actual.action_id, expected.action_id),
        _strict_scalar_equal(actual.effect_class, expected.effect_class),
        _strict_scalar_equal(actual.observable, expected.observable),
        _strict_scalar_equal(actual.summary_confirmed, expected.summary_confirmed),
        _strict_scalar_equal(actual.post_summary, expected.post_summary),
        _strict_scalar_equal(actual.measurement_tick, expected.measurement_tick),
        _strict_scalar_equal(actual.uncertainty_identity, expected.uncertainty_identity),
        _strict_scalar_equal(actual.evidence_ref, expected.evidence_ref),
        _strict_prep_recover_result_equal(actual.prep_recover, expected.prep_recover)
        if actual.prep_recover is not None or expected.prep_recover is not None
        else True,
    ))


def _visible_execution_record(value: object) -> VisibleExecutionRecord | None:
    """Retain only a typed raw S4 record in a post-dispatch error ledger."""

    if isinstance(value, EnvironmentExecution) and isinstance(value.record, VisibleExecutionRecord):
        return value.record
    return None


def _returned_environment(value: object) -> SyntheticEnvironment | None:
    """Retain an actually returned typed successor without fabricating one."""

    if isinstance(value, EnvironmentExecution) and isinstance(value.successor, SyntheticEnvironment):
        return value.successor
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
    return _strict_visible_execution_record_equal(record, VisibleExecutionRecord(
        execution_attempt_id=execution_attempt_id,
        action_id=snapshot.action_id,
        effect_class="UNKNOWN-EFFECT",
        observable=None,
        summary_confirmed=False,
        post_summary=None,
        measurement_tick=None,
        uncertainty_identity=None,
        evidence_ref=f"synthetic:{execution_attempt_id}:tool-error",
    ))


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
