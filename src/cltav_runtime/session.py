"""Bounded reference session coordinator for synthetic engineering validation."""

from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass, replace
from fractions import Fraction
from hashlib import sha256
from types import MappingProxyType
from typing import Mapping

from .bindings import RuntimeAuthorityBinding
from .kernel import FrontierEntry, Interval, KernelDiagnostic
from .interpretation import (
    InterpretationContract,
    ObservationAssessment,
    ObservationInput,
    OwnershipEvent,
    OwnershipOrderBoundary,
    OwnershipReplay,
    OwnershipResolution,
    assess_observation,
    interpretation_contract_identity,
    _parse_contract,
    _retained_ownership_order_boundary,
    strict_observation_assessment_equal,
    strict_observation_input_equal,
)
from .model import (
    ActionPrediction,
    FiniteSessionModel,
    PredictionClass,
    SyntheticAction,
    rebuild_verified_finite_session_model,
    verified_finite_session_model,
)
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
    "OBSERVATION-INTERPRETATION-ERROR",
    "OBSERVATION-UNCERTAINTY-WINDOW-MISMATCH",
    "OBSERVATION-NO-RESPONSE",
    "DUPLICATE-OBSERVATION-RESPONSE",
    "DUPLICATE-OBSERVATION-TRIGGER",
    "OBSERVATION-EVENT-IDENTITY-CONFLICT",
})
_OBSERVATION_QUARANTINE_CODES = frozenset({
    "DUPLICATE-OBSERVATION-RESPONSE",
    "DUPLICATE-OBSERVATION-TRIGGER",
    "OBSERVATION-EVENT-IDENTITY-CONFLICT",
})
_OBSERVATION_ORDER_REJECTION_CODES = frozenset({
    "INSUFFICIENT-OWNERSHIP-CONTEXT",
    "INVALID-OWNERSHIP-ORDER-BOUNDARY",
})
_MAPPING_PROXY_TYPE = type(MappingProxyType({}))


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
    interpretation_contract_identity: str | None = None


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
    # The session, not the environment, derives this immutable assessment from
    # ``execution.observation_input``.  It stays separate from the model's
    # observable class so T5 FAIL/INCONCLUSIVE never becomes an implicit
    # all-candidate history mutation.
    observation_assessment: ObservationAssessment | None = None


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
    # A response identity is consumed at most once for this session.  This is
    # separate from execution-attempt idempotence because one received record
    # must not be replayed under a later attempt or a different policy.
    consumed_response_ids: frozenset[str] = frozenset()
    # A request instance becomes terminal as soon as checked ownership says it
    # is uniquely claimed or ambiguous.  This is distinct from a seen response
    # token: a later trace cannot repair, reallocate, or re-score an already
    # observed request/response relation by narrowing its candidate set.
    terminal_trigger_event_ids: frozenset[str] = frozenset()
    # The public event ledger is separate from response/request outcome sets:
    # exact active requests may legitimately recur in a later cumulative
    # trace, while every other seen event identity is immutable and terminal.
    event_identity_refs: Mapping[str, OwnershipEvent] = field(
        default_factory=lambda: MappingProxyType({}),
    )
    active_trigger_event_ids: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        """Detach public top-level ledgers from caller-owned backing maps.

        ``MappingProxyType`` prevents writes *through the proxy* but does not
        freeze a dictionary held by its creator. A state may cross a public
        checkpoint/adapter boundary between S0 and S4, so retaining such a
        proxy directly would let an adapter rewrite a ledger after the
        pre-dispatch validation. Preserve invalid non-mapping values for the
        named state validator; valid mapping inputs are copied into fresh
        private proxies before the state can be dispatched.
        """

        if isinstance(self.frontiers, Mapping):
            object.__setattr__(self, "frontiers", MappingProxyType(dict(self.frontiers)))
        if type(self.event_identity_refs) is _MAPPING_PROXY_TYPE:
            object.__setattr__(
                self,
                "event_identity_refs",
                MappingProxyType({
                    identifier: (
                        OwnershipEvent(
                            event.event_id,
                            event.sequence,
                            event.kind,
                            event.key,
                            event.event_type,
                            event.timestamp,
                            event.target_request_id,
                        )
                        if type(event) is OwnershipEvent else event
                    )
                    for identifier, event in self.event_identity_refs.items()
                }),
            )


@dataclass(frozen=True)
class _ObservationLedgerDelta:
    """Terminal facts obtained from one complete checked ownership replay."""

    response_ids: frozenset[str]
    terminal_trigger_ids: frozenset[str]
    replayed_request_ids: frozenset[str]
    event_refs: Mapping[str, OwnershipEvent]
    active_trigger_ids: frozenset[str]


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


def _detached_dispatch_value(value: object) -> object:
    """Recursively rebuild the finite public checkpoint held across S4.

    Public checkpoint values are frozen dataclasses and immutable proxies in
    ordinary use.  That prevents accidental mutation but not a deliberately
    hostile adapter which retained an object reference and invokes
    ``object.__setattr__`` while ``execute`` is active.  The S4 boundary is
    finite and has only dataclass/mapping/sequence public values, so rebuild
    that closure rather than trusting aliases retained by the caller.

    Unknown scalar objects are intentionally returned as-is: normal S0
    validation has already closed the public checkpoint domain before this
    function is reached, while copying arbitrary adapter objects would extend
    the runtime's declared data model.
    """

    # ``Fraction`` is normally immutable at the language level, but it is a
    # finite public value and a hostile adapter can still rewrite its private
    # numerator/denominator with ``object.__setattr__``.  Rebuild it just as
    # we rebuild the frozen dataclasses that contain it; retaining the same
    # scalar instance would leave a mutable alias inside an otherwise detached
    # Interval, ownership event, or checkpoint seed.
    if type(value) is Fraction:
        return Fraction(value.numerator, value.denominator)
    if isinstance(value, Mapping):
        return {
            _detached_dispatch_value(key): _detached_dispatch_value(item)
            for key, item in value.items()
        } if type(value) is dict else MappingProxyType({
            _detached_dispatch_value(key): _detached_dispatch_value(item)
            for key, item in value.items()
        })
    if type(value) is tuple:
        return tuple(_detached_dispatch_value(item) for item in value)
    if type(value) is frozenset:
        return frozenset(_detached_dispatch_value(item) for item in value)
    if type(value) is set:
        return {_detached_dispatch_value(item) for item in value}
    if is_dataclass(value) and not isinstance(value, type):
        return type(value)(**{
            item.name: _detached_dispatch_value(getattr(value, item.name))
            for item in fields(value)
            if item.init
        })
    return value


def _detached_dispatch_checkpoint(state: SessionState) -> SessionState:
    """Return an S4-private reconstruction of one already validated state."""

    detached = _detached_dispatch_value(state)
    if type(detached) is not SessionState:  # defensive; `state` was validated at S0
        raise TypeError("dispatch checkpoint reconstruction did not return SessionState")
    return detached


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
        interpretation_contract: InterpretationContract | None = None,
    ) -> None:
        try:
            # Selection, charging, evidence and causal replay must all consume
            # one private finite authority projection.  A caller may retain
            # the model/binding objects it supplied, and an S4 adapter may
            # likewise retain those references; neither may rewrite the
            # action cost, finite AST, uncertainty or authority identities
            # after the S0/S3 checks have completed.
            if type(binding) is not RuntimeAuthorityBinding:
                raise TypeError("runtime authority binding is not exact")
            private_model = _frozen_model_snapshot(model)
            private_authority_identities = _frozen_authority_identities(binding.identities())
        except (AttributeError, TypeError, ValueError) as exc:
            raise ValueError("session runtime authority is invalid") from exc
        model_development_identity = {
            "commit": private_model.context.contract_commit,
            "path": private_model.context.contract_path,
            "blobSha256": private_model.context.contract_blob_sha256,
        }
        if private_authority_identities["development"] != model_development_identity:
            raise ValueError("runtime model and authority binding use different development snapshots")
        context = SessionContext.create(
            session_id=session_id,
            run_id=run_id,
            experiment_attempt_id=experiment_attempt_id,
            model_identity=private_model.identity,
            current_summary=initial_summary,
            q_status="KNOWN",
            resource_remainder=resources.remaining,
            retry_count=0,
            retry_cap=retry_cap,
        )
        seed_frontiers = _session_seed_frontiers(private_model, initial_path_bundles)
        history = HistoryHandle.initial(
            hypotheses=set(seed_frontiers),
            compatible_state_by_hypothesis={
                hypothesis: tuple(frontier.history_provenance[-1] for frontier in bundle)
                for hypothesis, bundle in seed_frontiers.items()
            },
        )
        # Keep legacy inspection of the caller's binding non-authoritative.
        # No S3/S4/S9 operation below reads it after the frozen identity
        # projection is created above.
        self.binding = binding
        self._authority_identities = private_authority_identities
        self._model = private_model
        if interpretation_contract is not None:
            try:
                detached_contract = _detached_dispatch_value(interpretation_contract)
                if type(detached_contract) is not InterpretationContract:
                    raise TypeError("interpretation contract reconstruction changed its public type")
                # Identity validation normalizes the typed contract, but the
                # session must consume that same normalized value rather than
                # the caller-shaped preimage.  This removes string subclasses
                # and other parser-normalized aliases before the private S4
                # authority snapshot is retained.
                normalized_contract, contract_errors = _parse_contract(detached_contract)
                if normalized_contract is None or contract_errors:
                    raise ValueError("interpretation contract is invalid")
                detached_contract = _detached_dispatch_value(normalized_contract)
                if type(detached_contract) is not InterpretationContract:
                    raise TypeError("canonical interpretation contract reconstruction changed its public type")
                contract_identity = interpretation_contract_identity(detached_contract)
            except (TypeError, ValueError) as exc:
                raise ValueError("session interpretation contract is invalid") from exc
            if detached_contract.deadline_authority == "REVIEWED":
                raise ValueError("bounded runtime has no controlled reviewed-deadline registry")
            # The session, rather than a fixture, owns the timing basis.  Bind
            # every identity that selects the model uncertainty snapshot so a
            # raw material declaration cannot silently choose a different
            # clock/unit/error budget from the frozen S3 model.
            if (
                detached_contract.clock_identity != self._model.uncertainty.clock_id
                or detached_contract.unit != self._model.uncertainty.time_unit
                or detached_contract.uncertainty_identity != self._model.uncertainty.uncertainty_id
                or detached_contract.error_budget_identity != self._model.uncertainty.identity
            ):
                raise ValueError("session interpretation contract does not bind the frozen model uncertainty snapshot")
        else:
            detached_contract = None
            contract_identity = None
        # Keep the object actually consumed by S4--S9 private.  The public
        # compatibility accessor below returns a fresh finite reconstruction,
        # so a caller cannot mutate the same contract object that this session
        # uses after its construction-time identity check.
        self._interpretation_contract = detached_contract
        self._interpretation_contract_identity = contract_identity
        self._authority_identity = _session_authority_identity(
            self._authority_identities,
            self._model,
            contract_identity,
        )
        self._seed_identity = _session_seed_identity(
            context=context,
            history=history,
            frontiers=seed_frontiers,
            resources=resources,
            authority_identity=self._authority_identity,
        )
        seed_state = SessionState(
            context=context,
            history=history,
            frontiers=seed_frontiers,
            resources=resources,
            attempts=0,
            processed_execution_attempt_ids=frozenset(),
            evidence=(),
            authority_identity=self._authority_identity,
            seed_identity=self._seed_identity,
            consumed_response_ids=frozenset(),
            terminal_trigger_event_ids=frozenset(),
            event_identity_refs=MappingProxyType({}),
            active_trigger_event_ids=frozenset(),
        )
        # The externally inspectable S0 checkpoint and the internal causal
        # replay seed intentionally do not share any finite nested object.
        # A hostile S4 adapter may retain the caller-visible state and use
        # object-level mutation; later same-session lineage checks must still
        # start from the frozen private seed, just as a fresh coordinator does.
        self._initial_seed_state = _detached_dispatch_checkpoint(seed_state)
        self.initial_state = _detached_dispatch_checkpoint(seed_state)

    @property
    def interpretation_contract(self) -> InterpretationContract | None:
        """Return a detached inspection copy, never the consumed authority."""

        if self._interpretation_contract is None:
            return None
        detached = _detached_dispatch_value(self._interpretation_contract)
        if type(detached) is not InterpretationContract:  # pragma: no cover - defensive invariant
            raise TypeError("interpretation contract reconstruction changed its public type")
        return detached

    @property
    def model(self) -> FiniteSessionModel:
        """Return an inspection copy, never the model consumed by a session."""

        return _frozen_model_snapshot(self._model)

    def run(self, environment: SyntheticEnvironment, *, maximum_rounds: int) -> SessionResult:
        if isinstance(maximum_rounds, bool) or not isinstance(maximum_rounds, int) or maximum_rounds < 1:
            return SessionResult(
                self.initial_state, environment, "Stop-Error",
                (KernelDiagnostic("INVALID-ROUND-LIMIT", "maximum rounds must be a positive integer"),),
            )
        state = _detached_dispatch_checkpoint(self._initial_seed_state)
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
            action = self._model.actions.get(canonical.snapshot.action_id)
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
            ingress_error = _incoming_record_error(
                record, action=action, interpretation_contract=self._interpretation_contract,
            )
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
        initial_context = self._initial_seed_state.context
        context = state.context
        if not isinstance(context, SessionContext) or (
            context.session_id != initial_context.session_id
            or context.run_id != initial_context.run_id
            or context.model_identity != self._model.identity
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
        if type(state.processed_execution_attempt_ids) is not frozenset or any(
            type(value) is not str or not value for value in state.processed_execution_attempt_ids
        ):
            return KernelDiagnostic("INVALID-EXECUTION-IDENTITIES", "processed execution identities are invalid")
        if type(state.consumed_response_ids) is not frozenset or any(
            type(value) is not str or not value for value in state.consumed_response_ids
        ):
            return KernelDiagnostic("INVALID-RESPONSE-IDENTITIES", "consumed response identities are invalid")
        if type(state.terminal_trigger_event_ids) is not frozenset or any(
            type(value) is not str or not value for value in state.terminal_trigger_event_ids
        ):
            return KernelDiagnostic("INVALID-TRIGGER-IDENTITIES", "discharged trigger identities are invalid")
        event_ledger_error = _event_identity_ledger_error(
            state.event_identity_refs,
            state.active_trigger_event_ids,
            state.terminal_trigger_event_ids,
            state.consumed_response_ids,
        )
        if event_ledger_error is not None:
            return event_ledger_error
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
            if len(paths) > self._model.frontier_limit:
                return KernelDiagnostic("FRONTIER-BUNDLE-LIMIT", "frontier path bundle exceeds the declared bound")
            for frontier in paths:
                if frontier.model_identity != self._model.context.identity:
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
            self._model.context.provenance_store.verify_entry(self._model.context, frontier) is None
            for paths in frontier_bundles.values()
            for frontier in paths
        )
        if local_closure:
            return self._model, None
        replay_model = _replay_model(self._model)
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

        replay_model = _replay_model(self._model) if replay_model is None else replay_model
        context = self._initial_seed_state.context
        history = self._initial_seed_state.history
        frontiers: Mapping[str, tuple[FrontierEntry, ...]] = self._initial_seed_state.frontiers
        resources = self._initial_seed_state.resources
        processed_ids: frozenset[str] = frozenset()
        consumed_response_ids: frozenset[str] = frozenset()
        terminal_trigger_event_ids: frozenset[str] = frozenset()
        seen_ownership_events: Mapping[str, OwnershipEvent] = MappingProxyType({})
        active_trigger_event_ids: frozenset[str] = frozenset()

        def apply_observation_ledger(
            assessment: ObservationAssessment | None, *, mode: str = "FULL",
        ) -> None:
            """Mirror one live accepted/rejected replay in this causal audit."""

            nonlocal consumed_response_ids, terminal_trigger_event_ids, active_trigger_event_ids, seen_ownership_events
            if mode == "FULL":
                (
                    consumed_response_ids,
                    terminal_trigger_event_ids,
                    seen_ownership_events,
                    active_trigger_event_ids,
                ) = _advance_observation_ledger(
                    consumed_response_ids,
                    terminal_trigger_event_ids,
                    active_trigger_event_ids,
                    seen_ownership_events,
                    assessment,
                )
            elif mode == "QUARANTINE":
                (
                    consumed_response_ids,
                    terminal_trigger_event_ids,
                    seen_ownership_events,
                    active_trigger_event_ids,
                ) = _quarantine_conflicted_observation_ledger(
                    consumed_response_ids,
                    terminal_trigger_event_ids,
                    seen_ownership_events,
                    active_trigger_event_ids,
                    assessment,
                )
            elif mode == "NONE":
                # An order-invalid delta is not admitted as a newly observed
                # public fact.  The retained ledger stays the sole source of
                # the next global high-water boundary.
                return
            else:
                raise ValueError("observation ledger mode is outside the controlled vocabulary")

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
                or not isinstance(item.observation_assessment, (ObservationAssessment, type(None)))
                or not isinstance(item.resolution_code, str)
                or not item.resolution_code
            ):
                return KernelDiagnostic("INVALID-EVIDENCE-RECORD", "evidence ledger item has an invalid public field type")
            action = replay_model.actions.get(item.snapshot.action_id)
            if action is None or item.snapshot.action_kind != action.kind:
                return KernelDiagnostic("EVIDENCE-ACTION-MISMATCH", "evidence snapshot does not name a current model action")
            prefix = SessionState(
                context, history, frontiers, resources, index - 1, processed_ids, (),
                self._authority_identity, self._seed_identity, consumed_response_ids,
                terminal_trigger_event_ids, seen_ownership_events, active_trigger_event_ids,
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
                authority_identities=self._authority_identities,
                interpretation_contract_identity=self._interpretation_contract_identity,
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
                assessment = item.observation_assessment
                expected_code = item.resolution_code
                if assessment is not None:
                    if type(item.rejected_response) is not VisibleExecutionRecord:
                        return KernelDiagnostic("EVIDENCE-ERROR-MISMATCH", "observation-bearing canonical error has no retained visible record")
                    expected_assessment = _bound_rejected_observation_assessment(
                        item.rejected_response,
                        action=action,
                        interpretation_contract=self._interpretation_contract,
                        model=replay_model,
                        execution_attempt_id=expected_execution_id,
                        prior_active_requests=_active_ownership_seed(
                            seen_ownership_events,
                            active_trigger_event_ids,
                        ),
                        prior_order_boundary=_ownership_order_boundary(
                            seen_ownership_events,
                            self._interpretation_contract,
                        ),
                    )
                    if (
                        expected_assessment is None
                        or not _strict_observation_assessment_equal(assessment, expected_assessment)
                    ):
                        return KernelDiagnostic("EVIDENCE-ERROR-MISMATCH", "canonical error assessment is not the bound rejected TEST material")
                    rejected_record_error = _incoming_record_error(
                        item.rejected_response,
                        action=action,
                        interpretation_contract=self._interpretation_contract,
                    )
                    if rejected_record_error is None:
                        return KernelDiagnostic("EVIDENCE-ERROR-MISMATCH", "canonical error retains a normal observation record")
                    conflict = _observation_replay_conflict(
                        seen_ownership_events,
                        active_trigger_event_ids,
                        terminal_trigger_event_ids,
                        consumed_response_ids,
                        assessment,
                    )
                    expected_code = conflict.code if conflict is not None else rejected_record_error.code
                if (
                    expected_code not in _CHARGED_ERROR_CODES
                    or item.resolution_code != expected_code
                ):
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
                apply_observation_ledger(
                    assessment,
                    mode=_observation_ledger_mode(
                        assessment,
                        conflict_code=(
                            item.resolution_code
                            if item.resolution_code in _OBSERVATION_QUARANTINE_CODES
                            else None
                        ),
                    ),
                )
                if expected_stop is not None and index != len(state.evidence):
                    return KernelDiagnostic("EVIDENCE-TERMINAL-MISMATCH", "a retry-cap error evidence item cannot have a later causal round")
                continue

            record_error = _incoming_record_error(
                item.execution, action=action, interpretation_contract=self._interpretation_contract,
            )
            if record_error is not None:
                return KernelDiagnostic("EVIDENCE-RECORD-MISMATCH", record_error.message)
            if item.execution.action_id != action.action_id:
                return KernelDiagnostic("EVIDENCE-ACTION-MISMATCH", "visible execution action differs from the admitted action")
            binding_error: KernelDiagnostic | None = None
            if self._interpretation_contract is None:
                if item.execution.observation_input is not None or item.observation_assessment is not None:
                    return KernelDiagnostic("EVIDENCE-INTERPRETATION-MISMATCH", "unbound session cannot retain ownership/timing evidence")
                assessment: ObservationAssessment | None = None
            elif item.execution.effect_class == "NONE" and action.kind == "TEST":
                assert isinstance(item.execution.observation_input, ObservationInput)
                assessment = assess_observation(
                    item.execution.observation_input,
                    self._interpretation_contract,
                    prior_active_requests=_active_ownership_seed(
                        seen_ownership_events,
                        active_trigger_event_ids,
                    ),
                    prior_order_boundary=_ownership_order_boundary(
                        seen_ownership_events,
                        self._interpretation_contract,
                    ),
                )
                binding_error = _observation_record_binding_error(item.execution, replay_model)
                assessment = _assessment_with_binding_error(assessment, binding_error)
                if not _strict_observation_assessment_equal(item.observation_assessment, assessment):
                    return KernelDiagnostic("EVIDENCE-INTERPRETATION-MISMATCH", "evidence assessment does not match its raw ownership/timing replay")
                # Interpret the complete typed material before comparing its
                # execution binding.  A binding failure still retains the
                # causal ownership result: an owned or ambiguous response
                # token cannot be replayed later under a friendlier record.
            else:
                if item.execution.observation_input is not None or item.observation_assessment is not None:
                    return KernelDiagnostic("EVIDENCE-INTERPRETATION-MISMATCH", "non-TEST or non-observation effect cannot retain ownership/timing evidence")
                assessment = None
                binding_error = None
            # Event IDs name immutable public facts across rounds.  Apply the
            # same complete identity/terminality conflict decision as live
            # execution before binding, timing, or silence classification.
            replay_conflict = _observation_replay_conflict(
                seen_ownership_events,
                active_trigger_event_ids,
                terminal_trigger_event_ids,
                consumed_response_ids,
                assessment,
            )
            if replay_conflict is not None:
                conflict_code = replay_conflict.code
                expected_history, expected_context, expected_stop = s7_expected(
                    conflict_code, item.execution,
                )
                if (
                    item.resolution_code != conflict_code
                    or not _strict_visible_execution_record_equal(item.rejected_response, item.execution)
                    or item.committed
                    or item.history_after != expected_history
                    or item.summary_after is not None
                    or item.stop_reason != expected_stop
                ):
                    return KernelDiagnostic("EVIDENCE-EVENT-IDENTITY-MISMATCH", "event-identity conflict does not close over the conservative S7 transition")
                context = expected_context
                history = expected_history
                resources = charged_resources
                processed_ids = processed_ids | {expected_execution_id}
                apply_observation_ledger(
                    assessment,
                    mode=_observation_ledger_mode(
                        assessment,
                        conflict_code=conflict_code,
                    ),
                )
                if expected_stop is not None and index != len(state.evidence):
                    return KernelDiagnostic("EVIDENCE-TERMINAL-MISMATCH", "a retry-cap ownership replay conflict cannot have a later causal round")
                continue

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

            if binding_error is not None:
                binding_code = _binding_resolution_code(binding_error)
                expected_history, expected_context, expected_stop = s7_expected(
                    binding_code, item.execution,
                )
                if (
                    item.resolution_code != binding_code
                    or not _strict_visible_execution_record_equal(item.rejected_response, item.execution)
                    or item.committed
                    or item.history_after != expected_history
                    or item.summary_after is not None
                    or item.stop_reason != expected_stop
                ):
                    return KernelDiagnostic("EVIDENCE-INTERPRETATION-MISMATCH", "binding-invalid observation does not close over the S7 retry transition")
                context = expected_context
                history = expected_history
                resources = charged_resources
                processed_ids = processed_ids | {expected_execution_id}
                apply_observation_ledger(
                    assessment,
                    mode=_observation_ledger_mode(assessment),
                )
                if expected_stop is not None and index != len(state.evidence):
                    return KernelDiagnostic("EVIDENCE-TERMINAL-MISMATCH", "a retry-cap binding error cannot have a later causal round")
                continue

            if assessment is not None and assessment.verdict == "ERROR":
                expected_history, expected_context, expected_stop = s7_expected(
                    "OBSERVATION-INTERPRETATION-ERROR", item.execution,
                )
                if (
                    item.resolution_code != "OBSERVATION-INTERPRETATION-ERROR"
                    or not _strict_visible_execution_record_equal(item.rejected_response, item.execution)
                    or item.committed
                    or item.history_after != expected_history
                    or item.summary_after is not None
                    or item.stop_reason != expected_stop
                ):
                    return KernelDiagnostic("EVIDENCE-INTERPRETATION-MISMATCH", "invalid ownership/timing evidence does not close over the S7 retry transition")
                context = expected_context
                history = expected_history
                resources = charged_resources
                processed_ids = processed_ids | {expected_execution_id}
                apply_observation_ledger(
                    assessment,
                    mode=_observation_ledger_mode(assessment),
                )
                if expected_stop is not None and index != len(state.evidence):
                    return KernelDiagnostic("EVIDENCE-TERMINAL-MISMATCH", "a retry-cap interpretation error cannot have a later causal round")
                continue

            if assessment is not None and assessment.kind == "NO-RESPONSE":
                expected_history, expected_context, expected_stop = s7_expected(
                    "OBSERVATION-NO-RESPONSE", item.execution,
                )
                if (
                    item.resolution_code != "OBSERVATION-NO-RESPONSE"
                    or item.rejected_response is not None
                    or item.committed
                    or item.history_after != expected_history
                    or item.summary_after is not None
                    or item.stop_reason != expected_stop
                ):
                    return KernelDiagnostic(
                        "EVIDENCE-NO-RESPONSE-MISMATCH",
                        "no-response evidence does not close over the conservative S7 transition",
                    )
                context = expected_context
                history = expected_history
                resources = charged_resources
                processed_ids = processed_ids | {expected_execution_id}
                apply_observation_ledger(
                    assessment,
                    mode=_observation_ledger_mode(assessment),
                )
                if expected_stop is not None and index != len(state.evidence):
                    return KernelDiagnostic("EVIDENCE-TERMINAL-MISMATCH", "a retry-cap no-response item cannot have a later causal round")
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
                        or not _strict_visible_execution_record_equal(item.rejected_response, item.execution)
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
                    apply_observation_ledger(
                        assessment,
                        mode=_observation_ledger_mode(assessment),
                    )
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
            apply_observation_ledger(assessment)
            if expected_stop is not None and index != len(state.evidence):
                return KernelDiagnostic("EVIDENCE-TERMINAL-MISMATCH", "a terminal committed evidence item cannot have a later causal round")

        if (
            state.context != context
            or state.history != history
            or dict(current_frontiers) != dict(frontiers)
            or state.resources != resources
            or state.processed_execution_attempt_ids != processed_ids
            or state.consumed_response_ids != consumed_response_ids
            or state.terminal_trigger_event_ids != terminal_trigger_event_ids
            or state.active_trigger_event_ids != active_trigger_event_ids
            or not _strict_ownership_event_mapping_equal(
                state.event_identity_refs, seen_ownership_events,
            )
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
            authority_identities=_detached_dispatch_value(self._authority_identities),
            interpretation_contract_identity=self._interpretation_contract_identity,
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
        # S4 is the only point at which an environment adapter runs.  It
        # receives no state argument, but a hostile adapter can still retain a
        # reference to the caller-owned checkpoint.  Take a recursively
        # detached state boundary snapshot before dispatch, including retained
        # evidence and its ownership replay.  A frozen dataclass alone cannot
        # stop an adapter from using ``object.__setattr__`` on an old nested
        # value; no S7/S8/S9 operation may consume that mutable alias.
        dispatch_state = _detached_dispatch_checkpoint(state)
        try:
            execution = environment.execute(request)
        except Exception as exc:
            return self._charged_execution_error(
                state=dispatch_state,
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
            state=dispatch_state,
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
        record_error = _incoming_record_error(
            execution.record, action=action, interpretation_contract=self._interpretation_contract,
        )
        if record_error is not None:
            # A malformed visible S4 record is still not entitled to erase a
            # correctly bound raw ownership/timing observation.  Preserve the
            # assessment only when the raw material names this *issued*
            # execution and passes the bidirectional binding check; arbitrary
            # malformed adapter objects never acquire ledger authority here.
            rejected_assessment = _bound_rejected_observation_assessment(
                execution.record,
                action=action,
                interpretation_contract=self._interpretation_contract,
                model=model,
                execution_attempt_id=execution_attempt_id,
                prior_active_requests=_active_ownership_seed(
                    state.event_identity_refs,
                    state.active_trigger_event_ids,
                ),
                prior_order_boundary=_ownership_order_boundary(
                    state.event_identity_refs,
                    self._interpretation_contract,
                ),
            )
            rejected_code = record_error.code
            rejected_replay_conflict = False
            if rejected_assessment is not None:
                rejected_conflict = _observation_replay_conflict(
                    state.event_identity_refs,
                    state.active_trigger_event_ids,
                    state.terminal_trigger_event_ids,
                    state.consumed_response_ids,
                    rejected_assessment,
                )
                if rejected_conflict is not None:
                    rejected_code = rejected_conflict.code
                    rejected_replay_conflict = rejected_code in _OBSERVATION_QUARANTINE_CODES
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
                code=rejected_code,
                message=record_error.message,
                execution_record=execution.record,
                environment_after_execution=execution.successor,
                observation_assessment=rejected_assessment,
                observation_ledger_mode=_observation_ledger_mode(
                    rejected_assessment,
                    conflict_code=(rejected_code if rejected_replay_conflict else None),
                ),
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

        # A contract-bound TEST may formally record the exclusive
        # no-response material shape.  It has no S9 summary by design; route
        # it to the interpreter before the ordinary confirmed-summary guard so
        # it can preserve history through the named S7 no-response branch.
        if (
            action.kind == "TEST"
            and self._interpretation_contract is not None
            and type(execution.record.observation_input) is ObservationInput
            and execution.record.observation_input.response_id is None
        ):
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
            self._authority_identity, self._seed_identity, state.consumed_response_ids,
            state.terminal_trigger_event_ids, state.event_identity_refs,
            state.active_trigger_event_ids,
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
        observation_assessment: ObservationAssessment | None = None,
        observation_ledger_mode: str = "FULL",
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
            None, False, stop_reason, rejected_response, code, observation_assessment,
        )
        # Ordinary rejected S7 routes apply the same complete typed replay
        # delta as a normal S9 commit. A cross-round identity/duplicate
        # conflict instead quarantines immutable receipt facts: a later trace
        # cannot repair a seen response or terminal request by changing its
        # pairing material, nor can it use that rejected trace to advance a
        # request disposition.
        if observation_ledger_mode == "FULL":
            (
                next_consumed_response_ids,
                next_terminal_trigger_event_ids,
                next_event_identity_refs,
                next_active_trigger_event_ids,
            ) = _advance_observation_ledger(
                state.consumed_response_ids,
                state.terminal_trigger_event_ids,
                state.active_trigger_event_ids,
                state.event_identity_refs,
                observation_assessment,
            )
        elif observation_ledger_mode == "QUARANTINE":
            (
                next_consumed_response_ids,
                next_terminal_trigger_event_ids,
                next_event_identity_refs,
                next_active_trigger_event_ids,
            ) = _quarantine_conflicted_observation_ledger(
                state.consumed_response_ids,
                state.terminal_trigger_event_ids,
                state.event_identity_refs,
                state.active_trigger_event_ids,
                observation_assessment,
            )
        elif observation_ledger_mode == "NONE":
            (
                next_consumed_response_ids,
                next_terminal_trigger_event_ids,
                next_event_identity_refs,
                next_active_trigger_event_ids,
            ) = (
                state.consumed_response_ids,
                state.terminal_trigger_event_ids,
                state.event_identity_refs,
                state.active_trigger_event_ids,
            )
        else:
            raise ValueError("observation ledger mode is outside the controlled vocabulary")
        next_state = SessionState(
            next_context, next_history, state.frontiers, charged_resources,
            state.attempts + 1, state.processed_execution_attempt_ids | {execution_attempt_id}, state.evidence + (evidence,),
            self._authority_identity, self._seed_identity, next_consumed_response_ids,
            next_terminal_trigger_event_ids, next_event_identity_refs,
            next_active_trigger_event_ids,
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

        assessment: ObservationAssessment | None = None
        if self._interpretation_contract is not None and action.kind == "TEST":
            assert isinstance(execution_record.observation_input, ObservationInput)
            assessment = assess_observation(
                execution_record.observation_input,
                self._interpretation_contract,
                prior_active_requests=_active_ownership_seed(
                    state.event_identity_refs,
                    state.active_trigger_event_ids,
                ),
                prior_order_boundary=_ownership_order_boundary(
                    state.event_identity_refs,
                    self._interpretation_contract,
                ),
            )
            binding_error = _observation_record_binding_error(execution_record, model)
            assessment = _assessment_with_binding_error(assessment, binding_error)
            replay_conflict = _observation_replay_conflict(
                state.event_identity_refs,
                state.active_trigger_event_ids,
                state.terminal_trigger_event_ids,
                state.consumed_response_ids,
                assessment,
            )
            if replay_conflict is not None:
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
                    code=replay_conflict.code,
                    message=replay_conflict.message,
                    rejected_response=execution_record,
                    observation_assessment=assessment,
                    observation_ledger_mode=_observation_ledger_mode(
                        assessment,
                        conflict_code=replay_conflict.code,
                    ),
                )
            if binding_error is not None:
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
                    code=_binding_resolution_code(binding_error),
                    message=binding_error.message,
                    rejected_response=execution_record,
                    observation_assessment=assessment,
                    observation_ledger_mode=_observation_ledger_mode(assessment),
                )
            if assessment.verdict == "ERROR":
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
                    code="OBSERVATION-INTERPRETATION-ERROR",
                    message=assessment.reason,
                    rejected_response=execution_record,
                    observation_assessment=assessment,
                    observation_ledger_mode=_observation_ledger_mode(assessment),
                )
            if assessment.kind == "NO-RESPONSE":
                # The record proves an issued execution with no normal public
                # response.  It is neither CONFIRMED-NOT-SENT nor a normal
                # class commit: retain the assessment, preserve H through the
                # conservative S7 route, and never smuggle it into S9.
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
                    code="OBSERVATION-NO-RESPONSE",
                    message=assessment.reason,
                    observation_assessment=assessment,
                    observation_ledger_mode=_observation_ledger_mode(assessment),
                )
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
                    observation_assessment=assessment,
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
            resolution_code="COMMIT", observation_assessment=assessment,
        )
        next_state = SessionState(
            next_context, next_history, next_frontiers, charged_resources,
            state.attempts + 1, state.processed_execution_attempt_ids | {execution_attempt_id}, state.evidence + (evidence,),
            self._authority_identity, self._seed_identity,
            *_advance_observation_ledger(
                state.consumed_response_ids,
                state.terminal_trigger_event_ids,
                state.active_trigger_event_ids,
                state.event_identity_refs,
                assessment,
            ),
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

        current_model = self._model if model is None else model
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
        observation_assessment: ObservationAssessment | None = None,
        observation_ledger_mode: str = "FULL",
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
            observation_assessment=observation_assessment,
            observation_ledger_mode=observation_ledger_mode,
        )


def _has_distinguishing_value(prediction: ActionPrediction, hypotheses: frozenset[str]) -> bool:
    return any(0 < len(value.hypotheses) < len(hypotheses) for value in prediction.classes)


def _frozen_model_snapshot(model: FiniteSessionModel) -> FiniteSessionModel:
    """Return one private finite-model authority projection for a session.

    The model's ordinary public dataclasses are intentionally inspectable, but
    Python's frozen dataclasses do not prevent a hostile S4 adapter from using
    ``object.__setattr__`` on an alias retained by the caller.  S3 admission,
    resource charging, evidence replay and later propagation must therefore
    use a distinct finite model.  The verified ``ModelContext`` is copied via
    its dedicated replay constructor: it preserves the authoritative Git
    token, context identity and existing provenance roots.  Its field
    authority is private; the normal append-only live provenance publication
    store remains shared for compatibility, while causal replay copies that
    store before validating a retained ledger.
    """

    # Rebuild from the factory-held canonical JSON rather than copying the
    # caller's public mappings after validation.  This closes a construction
    # TOCTOU in which an action map could change between a digest check and a
    # subsequent deep copy.
    private = rebuild_verified_finite_session_model(model)
    # A normal pre-S0 rewrite is still a malformed caller authority and is
    # rejected.  If a side-effecting mapping changes only while this check is
    # traversing it, the already rebuilt private projection remains the
    # factory-source semantics rather than the changed caller value.
    if not verified_finite_session_model(model):
        raise ValueError("runtime model is not a typed finite model")
    # Keep the established live-session provenance publication behaviour: new
    # deterministic records remain visible through the caller's declared model
    # context.  The private context's authority fields and all finite model
    # semantics above are rebuilt from the verified source; only this
    # append-only publication channel remains shared.  Causal validation calls
    # ``_replay_model`` and receives a copied store, so replay never writes it.
    object.__setattr__(private.context, "provenance_store", model.context.provenance_store)
    if not verified_finite_session_model(private):  # pragma: no cover - defensive closure check
        raise ValueError("runtime model private authority projection is invalid")
    return private


def _frozen_authority_identities(value: object) -> Mapping[str, Mapping[str, str]]:
    """Detach and validate the only binding fields consumed after S0.

    The runtime needs stable raw-Git identities, not a live caller-held
    ``RuntimeAuthorityBinding`` object.  Snapshot the two identity triples at
    construction so a later object-level mutation cannot change S3 evidence
    or make same-session and fresh coordinator replay disagree.
    """

    if not isinstance(value, Mapping) or set(value) != {"development", "interfaceRegistry"}:
        raise ValueError("runtime authority identities are incomplete")
    detached: dict[str, Mapping[str, str]] = {}
    for source in ("development", "interfaceRegistry"):
        identity = value.get(source)
        if not isinstance(identity, Mapping) or set(identity) != {"commit", "path", "blobSha256"}:
            raise ValueError("runtime authority identity is malformed")
        fields = {name: identity.get(name) for name in ("commit", "path", "blobSha256")}
        if any(type(item) is not str or not item for item in fields.values()):
            raise ValueError("runtime authority identity must use nonblank exact strings")
        detached[source] = MappingProxyType({name: fields[name] for name in ("commit", "path", "blobSha256")})
    return MappingProxyType(detached)


def _replay_model(model: FiniteSessionModel) -> FiniteSessionModel:
    """Freeze replay writes in a detached verified model context.

    Prediction may append deterministic source records for new runtime paths.
    Causal-ledger validation instead recreates an existing prefix; it needs
    the same authority and record closure, but must not mutate the session's
    shared provenance store.
    """

    return replace(model, context=model.context.read_only_replay_context())


def _session_authority_identity(
    identities: Mapping[str, Mapping[str, str]],
    model: FiniteSessionModel,
    interpretation_contract_identity: str | None = None,
) -> str:
    """Bind S0 to the exact controlled snapshots consumed by this session."""

    payload = (
        model.identity,
        model.context.identity,
        interpretation_contract_identity,
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
    interpretation_contract: InterpretationContract | None = None,
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
            or record.observation_input is not None
            or record.response_id is not None
        ):
            return KernelDiagnostic(
                "INVALID-EXECUTION-RECORD",
                "non-normal execution cannot manufacture an observation, confirmation, summary, measurement, uncertainty, or recovery result",
            )
        return None

    if action.kind == "TEST":
        if record.prep_recover is not None:
            return KernelDiagnostic("INVALID-EXECUTION-RECORD", "TEST cannot carry a Prep/Recover result")
        if (
            interpretation_contract is not None
            and type(record.observation_input) is ObservationInput
            and record.observation_input.response_id is None
        ):
            if (
                record.observable is not None or record.summary_confirmed or record.post_summary is not None
                or record.measurement_tick is not None or record.uncertainty_identity is not None
                or record.response_id is not None
            ):
                return KernelDiagnostic("INVALID-EXECUTION-RECORD", "response-free TEST material cannot coexist with a normal response or S9 summary")
            return None
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
        if interpretation_contract is None:
            if record.observation_input is not None or record.response_id is not None:
                return KernelDiagnostic("INVALID-EXECUTION-RECORD", "unbound TEST cannot carry ownership/timing material")
        elif type(record.observation_input) is not ObservationInput or not isinstance(record.response_id, str) or not record.response_id:
            return KernelDiagnostic("INVALID-EXECUTION-RECORD", "bound normal TEST requires one typed response-linked ownership/timing material")
        return None

    if action.kind not in {"PREP", "RECOVER"}:
        return KernelDiagnostic("INVALID-EXECUTION-RECORD", "execution action kind is outside the controlled vocabulary")
    result = record.prep_recover
    if record.observation_input is not None or record.response_id is not None:
        return KernelDiagnostic("INVALID-EXECUTION-RECORD", "Prep/Recover cannot manufacture a TEST ownership/timing input")
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


def _observation_record_binding_error(
    record: VisibleExecutionRecord,
    model: FiniteSessionModel,
) -> KernelDiagnostic | None:
    """Bind raw public material bidirectionally to its returned record.

    This check closes the raw/visible binding before an interpretation result
    can affect a session.  A trace with a valid ownership result is still
    unusable if it belongs to another execution, action, measurement,
    uncertainty snapshot, response, or public evidence record.
    """

    provenance_error = _observation_record_provenance_error(record)
    if provenance_error is not None:
        return provenance_error
    material = record.observation_input
    assert type(material) is ObservationInput
    if material.response_id is not None:
        expected_window = model.uncertainty.window(record.measurement_tick) if type(record.measurement_tick) is Fraction else None
        if not _strict_interval_equal(material.measurement_interval, expected_window):
            return KernelDiagnostic(
                "OBSERVATION-UNCERTAINTY-WINDOW-MISMATCH",
                "raw measurement interval is not the exact frozen model uncertainty window",
            )
    return None


def _observation_record_provenance_error(
    record: VisibleExecutionRecord,
) -> KernelDiagnostic | None:
    """Check identity binding independently of the frozen uncertainty window.

    This smaller relation is enough to retain an already issued public trace
    in an S7 ledger when another structural or U-window error rejects the
    visible record.  The full binding function above still rejects that record
    for normal interpretation/commit.
    """

    material = record.observation_input
    if type(material) is not ObservationInput:
        return KernelDiagnostic("OBSERVATION-BINDING-MISMATCH", "bound TEST record has no typed raw observation material")
    if not all((
        _strict_scalar_equal(material.execution_attempt_id, record.execution_attempt_id),
        _strict_scalar_equal(material.action_id, record.action_id),
        _strict_scalar_equal(material.evidence_ref, record.evidence_ref),
        _strict_scalar_equal(material.measurement_tick, record.measurement_tick),
        _strict_scalar_equal(material.uncertainty_identity, record.uncertainty_identity),
        _strict_scalar_equal(material.response_id, record.response_id),
    )):
        return KernelDiagnostic("OBSERVATION-BINDING-MISMATCH", "raw ownership/timing material does not describe this execution record")
    return None


def _bound_rejected_observation_assessment(
    record: VisibleExecutionRecord,
    *,
    action: SyntheticAction,
    interpretation_contract: InterpretationContract | None,
    model: FiniteSessionModel,
    execution_attempt_id: str,
    prior_active_requests: Mapping[str, OwnershipEvent] | None = None,
    prior_order_boundary: OwnershipOrderBoundary | None = None,
) -> ObservationAssessment | None:
    """Preserve only a safely bound raw TEST observation rejected at S4.

    A visible-record shape failure must not erase public response ownership.
    Conversely, a malformed adapter object must not manufacture a session
    ledger update.  This narrow helper accepts material only when it names the
    currently issued TEST exactly and its raw/visible provenance binding
    closes.  The returned assessment then retains a separate frozen-window
    diagnostic when applicable, rather than losing ownership facts.
    """

    if (
        interpretation_contract is None
        or action.kind != "TEST"
        or type(record.observation_input) is not ObservationInput
        or record.execution_attempt_id != execution_attempt_id
        or record.action_id != action.action_id
    ):
        return None
    if _observation_record_provenance_error(record) is not None:
        return None
    assessment = assess_observation(
        record.observation_input,
        interpretation_contract,
        prior_active_requests=prior_active_requests,
        prior_order_boundary=prior_order_boundary,
    )
    return _assessment_with_binding_error(
        assessment,
        _observation_record_binding_error(record, model),
    )


def _assessment_with_binding_error(
    assessment: ObservationAssessment,
    binding_error: KernelDiagnostic | None,
) -> ObservationAssessment:
    """Make a frozen-U mismatch a typed measurement ERROR, not a bare S7.

    Provenance/identity binding errors remain outside the observation verdict:
    they say the returned record is not its claimed public material.  The
    exact frozen uncertainty-window mismatch instead invalidates the measured
    interval itself, so retain the ownership replay and publish a named ERROR
    assessment that both live execution and checkpoint replay recompute.
    """

    if (
        binding_error is None
        or binding_error.code != "OBSERVATION-UNCERTAINTY-WINDOW-MISMATCH"
    ):
        return assessment
    diagnostics = assessment.diagnostics
    if not any(
        diagnostic.code == binding_error.code and diagnostic.message == binding_error.message
        for diagnostic in diagnostics
    ):
        diagnostics = diagnostics + (binding_error,)
    return replace(
        assessment,
        verdict="ERROR",
        score_disposition="ERROR",
        answered=False,
        reason=binding_error.message,
        diagnostics=diagnostics,
    )


def _binding_resolution_code(binding_error: KernelDiagnostic) -> str:
    """Expose measurement-window rejection without conflating identity faults."""

    return (
        "OBSERVATION-UNCERTAINTY-WINDOW-MISMATCH"
        if binding_error.code == "OBSERVATION-UNCERTAINTY-WINDOW-MISMATCH"
        else "OBSERVATION-INTERPRETATION-ERROR"
    )


def _observation_ledger_mode(
    assessment: ObservationAssessment | None,
    *,
    conflict_code: str | None = None,
) -> str:
    """Choose the only ledger effect permitted for a rejected observation.

    An event that falls before the retained global order frontier is not a
    newly observed public fact for this session.  Retaining it through the
    ordinary FULL/error path would advance the next frontier with material we
    explicitly rejected and could make a later valid delta unrecoverable.
    Identity conflicts retain uncontested facts through their established
    quarantine path; all other checked replays keep the existing FULL path.
    """

    if (
        type(assessment) is ObservationAssessment
        and any(
            diagnostic.code in _OBSERVATION_ORDER_REJECTION_CODES
            for diagnostic in assessment.diagnostics
        )
    ):
        return "NONE"
    if conflict_code in _OBSERVATION_QUARANTINE_CODES:
        return "QUARANTINE"
    return "FULL"


def _strict_interval_equal(actual: object, expected: object) -> bool:
    if actual is None or expected is None:
        return actual is None and expected is None
    if type(actual) is not Interval or type(expected) is not Interval:
        return False
    return all(
        _strict_scalar_equal(getattr(actual, field), getattr(expected, field))
        for field in ("lower", "upper", "lower_closed", "upper_closed")
    )


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
        _strict_scalar_equal(actual.response_id, expected.response_id),
        _strict_observation_input_equal(actual.observation_input, expected.observation_input),
        _strict_prep_recover_result_equal(actual.prep_recover, expected.prep_recover)
        if actual.prep_recover is not None or expected.prep_recover is not None
        else True,
    ))


def _strict_observation_input_equal(actual: object, expected: object) -> bool:
    """Compare raw interpretation material only as a type-exact value."""

    return strict_observation_input_equal(actual, expected)


def _strict_observation_assessment_equal(actual: object, expected: object) -> bool:
    """Assessment equality is meaningful only when both values are typed."""

    return strict_observation_assessment_equal(actual, expected)


def _terminal_trigger_ids(assessment: ObservationAssessment | None) -> frozenset[str]:
    """Backward-sized projection of the complete replay ledger delta."""

    return _observation_ledger_delta(assessment).terminal_trigger_ids


def _observation_ledger_delta(assessment: ObservationAssessment | None) -> _ObservationLedgerDelta:
    """Derive the session's terminal facts from one typed ownership replay.

    The selected ``response_id`` is not the extent of an observation trace.
    A FIFO/MOST-RECENT replay may discharge several requests and may contain
    unmatched/wrong-key response tokens which are still public facts.  The
    session consumes every typed response token from that replay, terminalises
    every non-active contract request, and records every replayed request ID
    so a later round cannot reintroduce an already terminal instance under a
    different response or pairing policy.
    """

    if type(assessment) is not ObservationAssessment:
        return _ObservationLedgerDelta(
            frozenset(), frozenset(), frozenset(), MappingProxyType({}), frozenset(),
        )
    response_ids: set[str] = set()
    terminal_trigger_ids: set[str] = set()
    replayed_request_ids: set[str] = set()
    active_trigger_ids: set[str] = set()
    event_refs: dict[str, OwnershipEvent] = {}
    replay = assessment.replay
    if type(replay) is OwnershipReplay:
        for identifier, event in replay.event_refs.items():
            if type(identifier) is str and identifier and type(event) is OwnershipEvent:
                event_refs[identifier] = event
                if event.kind == "RESPONSE":
                    response_ids.add(identifier)
        for identifier, disposition in replay.request_dispositions.items():
            if type(identifier) is not str or not identifier or type(disposition) is not str:
                continue
            replayed_request_ids.add(identifier)
            if disposition in {"DISCHARGED", "AMBIGUOUS", "CANCELLED", "SUPERSEDED"}:
                terminal_trigger_ids.add(identifier)
            elif disposition == "ACTIVE":
                active_trigger_ids.add(identifier)
    # A syntactically typed selected response with no event object is itself a
    # sparse public terminal token.  If that identifier names a typed event in
    # this replay, the event controls its role: a request/cancellation ID must
    # not be reclassified as a consumed response merely because malformed
    # material placed it in ``responseId``.
    if type(assessment.response_id) is str and assessment.response_id:
        selected_event = event_refs.get(assessment.response_id)
        if selected_event is None or selected_event.kind == "RESPONSE":
            response_ids.add(assessment.response_id)
    if type(assessment.ownership) is OwnershipResolution:
        ownership = assessment.ownership
        if ownership.status == "UNIQUE" and type(ownership.owner_request_id) is str and ownership.owner_request_id:
            terminal_trigger_ids.add(ownership.owner_request_id)
            replayed_request_ids.add(ownership.owner_request_id)
        elif ownership.status == "AMBIGUOUS":
            terminal_trigger_ids.update(
                identifier for identifier in ownership.candidate_request_ids
                if type(identifier) is str and identifier
            )
            replayed_request_ids.update(
                identifier for identifier in ownership.candidate_request_ids
                if type(identifier) is str and identifier
            )
    return _ObservationLedgerDelta(
        frozenset(response_ids), frozenset(terminal_trigger_ids), frozenset(replayed_request_ids),
        MappingProxyType(dict(event_refs)), frozenset(active_trigger_ids),
    )


def _active_ownership_seed(
    event_identity_refs: Mapping[str, OwnershipEvent],
    active_trigger_event_ids: frozenset[str],
) -> Mapping[str, OwnershipEvent]:
    """Project only validated retained ACTIVE requests into one new replay.

    Terminal responses/requests are immutable receipts, not a required raw
    prefix for the next incremental observation.  The selected ownership
    policy nevertheless needs every still-ACTIVE request and its original
    global order.  This helper is used symmetrically by live execution and
    causal-ledger replay; it never receives adapter-owned raw material.
    """

    return MappingProxyType({
        identifier: event_identity_refs[identifier]
        for identifier in active_trigger_event_ids
        if identifier in event_identity_refs
    })


def _ownership_order_boundary(
    event_identity_refs: Mapping[str, OwnershipEvent],
    interpretation_contract: InterpretationContract | None,
) -> OwnershipOrderBoundary | None:
    """Project the checked ledger's controlled global order high-water mark.

    ACTIVE requests are a narrow ownership seed: they decide the candidates
    for a newly observed response.  The full verified ledger separately
    establishes the global sequence/timestamp prefix, including terminal
    requests and consumed responses.  Never derive this boundary from raw
    S4 material or a caller-supplied summary; live execution and causal
    replay both call this helper over their independently reconstructed
    ledger.
    """

    if interpretation_contract is None:
        return None
    return _retained_ownership_order_boundary(
        event_identity_refs,
        interpretation_contract,
    )


def _strict_ownership_event_equal(actual: object, expected: object) -> bool:
    """Compare one public ownership event without scalar subclass coercion."""

    if type(actual) is not OwnershipEvent or type(expected) is not OwnershipEvent:
        return False
    return all(
        _strict_scalar_equal(getattr(actual, field), getattr(expected, field))
        for field in (
            "event_id", "sequence", "kind", "key", "event_type", "timestamp", "target_request_id",
        )
    )


def _observation_replay_conflict(
    seen_event_refs: Mapping[str, OwnershipEvent],
    active_trigger_event_ids: frozenset[str],
    terminal_trigger_event_ids: frozenset[str],
    consumed_response_ids: frozenset[str],
    assessment: ObservationAssessment | None,
) -> KernelDiagnostic | None:
    """Apply one closed cross-round ownership identity/terminality policy.

    An exact ACTIVE request may appear again in a later cumulative trace.  No
    other already seen event can be replayed as fresh material: responses and
    terminal requests retain their specific duplicate diagnostics, while a
    changed field/kind or a non-obligation event identity is an immutable
    event-identity conflict.  This helper is intentionally shared by live
    execution and causal-ledger replay before any timing/binding verdict.
    """

    delta = _observation_ledger_delta(assessment)
    # First scan every immutable/cross-role conflict.  A trace may also carry
    # a duplicate response; that lower-severity duplicate must not mask a
    # changed event identity and accidentally choose the FULL ledger path.
    # Sorting prevents diagnostics from depending on a frozenset iteration.
    if delta.response_ids & delta.replayed_request_ids:
        return KernelDiagnostic(
            "OBSERVATION-EVENT-IDENTITY-CONFLICT",
            "one replay assigns an identifier both response and request roles",
        )
    if (
        active_trigger_event_ids & delta.response_ids
        or terminal_trigger_event_ids & delta.response_ids
        or consumed_response_ids & delta.replayed_request_ids
    ):
        return KernelDiagnostic(
            "OBSERVATION-EVENT-IDENTITY-CONFLICT",
            "an observation identifier conflicts with an already retained response/request role",
        )
    for identifier in sorted(delta.response_ids):
        prior = seen_event_refs.get(identifier)
        if prior is not None and prior.kind != "RESPONSE":
            return KernelDiagnostic(
                "OBSERVATION-EVENT-IDENTITY-CONFLICT",
                "a selected response identity was previously retained under a different event kind",
            )
    for identifier in sorted(delta.replayed_request_ids):
        prior = seen_event_refs.get(identifier)
        if prior is not None and prior.kind != "REQUEST":
            return KernelDiagnostic(
                "OBSERVATION-EVENT-IDENTITY-CONFLICT",
                "a replayed request identity was previously retained under a different event kind",
            )
    for identifier in sorted(delta.event_refs):
        event = delta.event_refs[identifier]
        prior = seen_event_refs.get(identifier)
        if prior is not None and not _strict_ownership_event_equal(prior, event):
            return KernelDiagnostic(
                "OBSERVATION-EVENT-IDENTITY-CONFLICT",
                "ownership event identity was reused with different typed public fields",
            )
        if prior is None and identifier in consumed_response_ids and event.kind != "RESPONSE":
            return KernelDiagnostic(
                "OBSERVATION-EVENT-IDENTITY-CONFLICT",
                "a consumed response identity was reused under a different event kind",
            )
        if prior is None and identifier in terminal_trigger_event_ids and event.kind != "REQUEST":
            return KernelDiagnostic(
                "OBSERVATION-EVENT-IDENTITY-CONFLICT",
                "a terminal trigger identity was reused under a different event kind",
            )

    # The immutable scan is clear.  Retain only deterministic duplicate
    # candidates now: all exact response duplicates take precedence over an
    # exact terminal-request duplicate, and one exact ACTIVE request is the
    # sole event identity allowed to recur without an error.
    duplicate_response = False
    duplicate_trigger = False
    for identifier in sorted(delta.response_ids):
        if identifier in consumed_response_ids:
            duplicate_response = True
        elif (prior := seen_event_refs.get(identifier)) is not None and prior.kind == "RESPONSE":
            duplicate_response = True
    for identifier in sorted(delta.replayed_request_ids):
        if identifier in terminal_trigger_event_ids:
            duplicate_trigger = True
    for identifier in sorted(delta.event_refs):
        event = delta.event_refs[identifier]
        prior = seen_event_refs.get(identifier)
        if prior is None:
            continue
        if event.kind == "RESPONSE":
            duplicate_response = True
        elif event.kind == "REQUEST":
            if identifier in terminal_trigger_event_ids:
                duplicate_trigger = True
            elif identifier in active_trigger_event_ids:
                continue
            else:
                return KernelDiagnostic(
                    "OBSERVATION-EVENT-IDENTITY-CONFLICT",
                    "only an exactly replayed active contract request may recur across rounds",
                )
        else:
            return KernelDiagnostic(
                "OBSERVATION-EVENT-IDENTITY-CONFLICT",
                "only an exactly replayed active contract request may recur across rounds",
            )
    if duplicate_response:
        return KernelDiagnostic(
            "DUPLICATE-OBSERVATION-RESPONSE",
            "response identity was already consumed by this session",
        )
    if duplicate_trigger:
        return KernelDiagnostic(
            "DUPLICATE-OBSERVATION-TRIGGER",
            "trigger instance was already terminal in this session",
        )
    return None


def _merged_observation_event_refs(
    seen_event_refs: Mapping[str, OwnershipEvent],
    assessment: ObservationAssessment | None,
) -> Mapping[str, OwnershipEvent]:
    """Extend an already checked event ledger with one typed replay."""

    merged = dict(seen_event_refs)
    for identifier, event in _observation_ledger_delta(assessment).event_refs.items():
        merged.setdefault(identifier, event)
    return MappingProxyType(merged)


def _strict_ownership_event_mapping_equal(
    actual: object,
    expected: object,
) -> bool:
    if not isinstance(actual, Mapping) or not isinstance(expected, Mapping):
        return False
    if (
        len(actual) != len(expected)
        or any(type(identifier) is not str for identifier in actual)
        or any(type(identifier) is not str for identifier in expected)
        or set(actual) != set(expected)
    ):
        return False
    return all(_strict_ownership_event_equal(actual[identifier], expected[identifier]) for identifier in actual)


def _advance_observation_ledger(
    consumed_response_ids: frozenset[str],
    terminal_trigger_event_ids: frozenset[str],
    active_trigger_event_ids: frozenset[str],
    event_identity_refs: Mapping[str, OwnershipEvent],
    assessment: ObservationAssessment | None,
) -> tuple[
    frozenset[str], frozenset[str], Mapping[str, OwnershipEvent], frozenset[str],
]:
    """Apply the same complete-replay delta in live and lineage paths."""

    delta = _observation_ledger_delta(assessment)
    next_terminal = terminal_trigger_event_ids | delta.terminal_trigger_ids
    return (
        consumed_response_ids | delta.response_ids,
        next_terminal,
        _merged_observation_event_refs(event_identity_refs, assessment),
        (active_trigger_event_ids | delta.active_trigger_ids) - next_terminal,
    )


def _quarantine_conflicted_observation_ledger(
    consumed_response_ids: frozenset[str],
    terminal_trigger_event_ids: frozenset[str],
    event_identity_refs: Mapping[str, OwnershipEvent],
    active_trigger_event_ids: frozenset[str],
    assessment: ObservationAssessment | None,
) -> tuple[
    frozenset[str], frozenset[str], Mapping[str, OwnershipEvent], frozenset[str],
]:
    """Seal uncontested public facts from a trace with an identity conflict.

    A conflicting request must not mutate its established ownership state, but
    a new response token in that same public trace cannot be made available
    for a later, friendlier pairing.  Retain only previously unseen event IDs
    and consume newly observed response IDs; leave active/terminal request
    dispositions unchanged.  Causal replay uses this same quarantine path.
    """

    delta = _observation_ledger_delta(assessment)
    merged = dict(event_identity_refs)
    response_ids: set[str] = set()
    for identifier, event in delta.event_refs.items():
        # A scalar ledger may deliberately retain a malformed selected
        # response which had no typed event object.  If a later conflict trace
        # supplies that identifier under any event kind, the old role wins:
        # do not create a contradictory map entry while quarantining other
        # uncontested facts from the same trace.
        if (
            identifier in merged
            or identifier in consumed_response_ids
            or identifier in terminal_trigger_event_ids
            or identifier in active_trigger_event_ids
        ):
            continue
        merged[identifier] = event
        if event.kind == "RESPONSE":
            response_ids.add(identifier)
    if type(assessment) is ObservationAssessment and type(assessment.response_id) is str and assessment.response_id:
        selected_event = delta.event_refs.get(assessment.response_id)
        if (
            (selected_event is None or selected_event.kind == "RESPONSE")
            and assessment.response_id not in event_identity_refs
            and assessment.response_id not in consumed_response_ids
            and assessment.response_id not in terminal_trigger_event_ids
            and assessment.response_id not in active_trigger_event_ids
        ):
            response_ids.add(assessment.response_id)
    return (
        consumed_response_ids | frozenset(response_ids),
        terminal_trigger_event_ids,
        MappingProxyType(merged),
        active_trigger_event_ids,
    )


def _event_identity_ledger_error(
    event_identity_refs: object,
    active_trigger_event_ids: object,
    terminal_trigger_event_ids: frozenset[str],
    consumed_response_ids: frozenset[str],
) -> KernelDiagnostic | None:
    """Validate the persistent canonical ledger before a resumed dispatch."""

    if type(event_identity_refs) is not _MAPPING_PROXY_TYPE:
        return KernelDiagnostic("INVALID-OBSERVATION-EVENT-LEDGER", "event identity ledger is not an immutable mapping")
    if type(terminal_trigger_event_ids) is not frozenset or any(
        type(identifier) is not str or not identifier for identifier in terminal_trigger_event_ids
    ):
        return KernelDiagnostic("INVALID-OBSERVATION-EVENT-LEDGER", "terminal trigger identities are invalid")
    if type(consumed_response_ids) is not frozenset or any(
        type(identifier) is not str or not identifier for identifier in consumed_response_ids
    ):
        return KernelDiagnostic("INVALID-OBSERVATION-EVENT-LEDGER", "consumed response identities are invalid")
    if type(active_trigger_event_ids) is not frozenset or any(
        type(identifier) is not str or not identifier for identifier in active_trigger_event_ids
    ):
        return KernelDiagnostic("INVALID-OBSERVATION-EVENT-LEDGER", "active trigger identities are invalid")
    if active_trigger_event_ids & terminal_trigger_event_ids:
        return KernelDiagnostic("INVALID-OBSERVATION-EVENT-LEDGER", "active and terminal trigger identities overlap")
    if active_trigger_event_ids & consumed_response_ids:
        return KernelDiagnostic("INVALID-OBSERVATION-EVENT-LEDGER", "active trigger and consumed response identities overlap")
    if consumed_response_ids & terminal_trigger_event_ids:
        return KernelDiagnostic("INVALID-OBSERVATION-EVENT-LEDGER", "response and terminal-trigger identities overlap")
    for identifier, event in event_identity_refs.items():
        if (
            type(identifier) is not str
            or not identifier
            or type(event) is not OwnershipEvent
            or not _strict_scalar_equal(identifier, event.event_id)
            or type(event.sequence) is not int
            or event.sequence < 0
            or type(event.kind) is not str
            or event.kind not in {"REQUEST", "RESPONSE", "CANCEL", "SUPERSEDE"}
            or type(event.key) is not str
            or not event.key
            or type(event.event_type) is not str
            or not event.event_type
            or type(event.timestamp) is not Fraction
            or (
                event.kind in {"CANCEL", "SUPERSEDE"}
                and (type(event.target_request_id) is not str or not event.target_request_id)
            )
            or (
                event.kind not in {"CANCEL", "SUPERSEDE"}
                and event.target_request_id is not None
                and (event.kind != "REQUEST" or type(event.target_request_id) is not str or not event.target_request_id)
            )
        ):
            return KernelDiagnostic("INVALID-OBSERVATION-EVENT-LEDGER", "event identity ledger contains an invalid typed event")
        if identifier in consumed_response_ids and event.kind != "RESPONSE":
            return KernelDiagnostic("INVALID-OBSERVATION-EVENT-LEDGER", "a consumed response identity does not name a response event")
        if identifier in terminal_trigger_event_ids and event.kind != "REQUEST":
            return KernelDiagnostic("INVALID-OBSERVATION-EVENT-LEDGER", "a terminal trigger identity does not name a request event")
        if event.kind == "RESPONSE" and identifier not in consumed_response_ids:
            return KernelDiagnostic("INVALID-OBSERVATION-EVENT-LEDGER", "a retained response event was not consumed")
    for identifier in active_trigger_event_ids | terminal_trigger_event_ids:
        event = event_identity_refs.get(identifier)
        if type(event) is not OwnershipEvent or event.kind != "REQUEST":
            return KernelDiagnostic("INVALID-OBSERVATION-EVENT-LEDGER", "active/terminal trigger identity does not name a retained request event")
    return None


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
    authority_identities: Mapping[str, Mapping[str, str]],
    interpretation_contract_identity: str | None,
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
        or not _strict_authority_identities_equal(snapshot.authority_identities, authority_identities)
        or snapshot.interpretation_contract_identity != interpretation_contract_identity
    ):
        return KernelDiagnostic("SNAPSHOT-IDENTITY-MISMATCH", "evidence snapshot is not the expected causal selection snapshot")
    return None


def _strict_authority_identities_equal(
    actual: object,
    expected: Mapping[str, Mapping[str, str]],
) -> bool:
    """Compare the finite identity projection without Mapping equality tricks."""

    if not isinstance(actual, Mapping) or set(actual) != set(expected):
        return False
    for source, expected_identity in expected.items():
        received = actual.get(source)
        if not isinstance(received, Mapping) or set(received) != set(expected_identity):
            return False
        for field, expected_value in expected_identity.items():
            if type(received.get(field)) is not str or received.get(field) != expected_value:
                return False
    return True


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
