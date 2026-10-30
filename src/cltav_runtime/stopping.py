"""Frozen stop and conservative-equivalence values for the finite runtime.

The bounded reference runtime deliberately has no equivalence proof backend and
does not implement ARINC 645 integrity capability.  This module therefore
models only the controlled *return* contract: it records why a finite session
stops, retains any currently applicable named residual, and makes abstention
explicit rather than turning a lack of a one-step distinguisher into proof.

It has no dependency on :mod:`cltav_runtime.session` so the relation can be
shared by live execution and causal replay without a circular import.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Mapping, Protocol


class _HistoryLike(Protocol):
    hypotheses: frozenset[str]
    status_by_hypothesis: Mapping[str, str]
    version: int
    processed: bool


class _ContextLike(Protocol):
    q_status: str
    retry_count: int
    retry_cap: int


class _ResourceLike(Protocol):
    mode: str
    remaining: int


class _FrontierLike(Protocol):
    path_length: int
    status: str


def _nonblank(value: object, *, label: str) -> str:
    if type(value) is not str or not value.strip():
        raise ValueError(f"{label} must be a nonblank exact string")
    return value


def _digest(value: object) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Named645Residual:
    """One source-bound unresolved 645 runtime obligation for one frozen input."""

    requirement_id: str
    dependency_id: str
    source_unit_id: str
    contract_id: str
    context_id: str
    input_identity: str

    def __post_init__(self) -> None:
        for name, value in (
            ("645 residual requirement identity", self.requirement_id),
            ("645 residual dependency identity", self.dependency_id),
            ("645 residual source identity", self.source_unit_id),
            ("645 residual contract identity", self.contract_id),
            ("645 residual applicability context", self.context_id),
            ("645 residual input identity", self.input_identity),
        ):
            _nonblank(value, label=name)

    @property
    def identity(self) -> str:
        return _digest(
            (
                self.requirement_id,
                self.dependency_id,
                self.source_unit_id,
                self.contract_id,
                self.context_id,
                self.input_identity,
            ),
        )


@dataclass(frozen=True)
class StopInputs:
    """Detached S0 inputs used by the controlled stop relation.

    A ``context_id`` names a validated public finite-runtime context, not an
    editable applicability flag.  The binding has already derived the exact
    residual tuple for it from Git-bound bytes before this value exists.
    """

    applicability_status: str
    context_id: str | None
    applicability_input_identity: str | None
    named_645_residuals: tuple[Named645Residual, ...]

    def __post_init__(self) -> None:
        if self.applicability_status not in {
            "P3-UNAVAILABLE", "P3-ACTIVE", "P3-EXPLICIT-INACTIVE", "P3-METHOD-ONLY",
        }:
            raise ValueError("finite applicability status is outside the controlled vocabulary")
        if self.context_id is not None:
            _nonblank(self.context_id, label="finite applicability context identity")
        if self.applicability_input_identity is not None:
            _nonblank(self.applicability_input_identity, label="finite applicability input identity")
        if type(self.named_645_residuals) is not tuple or any(
            type(item) is not Named645Residual for item in self.named_645_residuals
        ):
            raise ValueError("named 645 residuals must be an exact frozen tuple")
        if (self.context_id is None) != (self.applicability_input_identity is None):
            raise ValueError("finite applicability context and input identity must occur together")
        if self.applicability_status == "P3-UNAVAILABLE" and (
            self.context_id is not None
            or self.applicability_input_identity is not None
            or self.named_645_residuals
        ):
            raise ValueError("unavailable P3 inputs cannot carry an evaluated context or residual")
        if self.applicability_status != "P3-UNAVAILABLE" and (
            self.context_id is None or self.applicability_input_identity is None
        ):
            raise ValueError("evaluated P3 inputs require a frozen applicability context")
        if self.applicability_status == "P3-ACTIVE" and not self.named_645_residuals:
            raise ValueError("active P3 inputs require a named residual")
        if self.applicability_status in {"P3-EXPLICIT-INACTIVE", "P3-METHOD-ONLY"} and self.named_645_residuals:
            raise ValueError("non-active P3 inputs cannot carry a named residual")
        if self.named_645_residuals and self.context_id is None:
            raise ValueError("named 645 residuals require a finite applicability context")
        if any(
            item.context_id != self.context_id or item.input_identity != self.applicability_input_identity
            for item in self.named_645_residuals
        ):
            raise ValueError("named 645 residuals do not match the frozen applicability input")
        identities = tuple(item.identity for item in self.named_645_residuals)
        if len(identities) != len(set(identities)):
            raise ValueError("named 645 residuals must not repeat an exact obligation")

    @property
    def active_residuals(self) -> tuple[Named645Residual, ...]:
        return self.named_645_residuals

    @property
    def identity(self) -> str:
        return _digest(
            (
                self.applicability_status,
                self.context_id,
                self.applicability_input_identity,
                tuple(item.identity for item in self.named_645_residuals),
            ),
        )


@dataclass(frozen=True)
class EquivalenceStatus:
    """A conservative IF-EQUIV return without a proof-producing backend."""

    tag: str
    reason: str
    hypotheses: tuple[str, ...]
    history_version: int
    action_domain_identity: str
    path_limit: int
    frontier_limit: int
    observation_class_limit: int
    calculation_diagnostic_codes: tuple[str, ...]


@dataclass(frozen=True)
class StopTrace:
    """Typed in-memory IF-RESOURCE-STOP evidence for one checked state."""

    phase: str
    stop_class: str | None
    reason: str
    final_hypotheses: tuple[str, ...]
    history_version: int
    resource_mode: str
    resource_remaining: int
    retry_count: int
    retry_cap: int
    applicability_status: str
    applicability_context_id: str | None
    applicability_input_identity: str | None
    active_named_645_residuals: tuple[Named645Residual, ...]
    equivalence: EquivalenceStatus
    model_identity: str
    authority_identity: str
    trace_identity: str


@dataclass(frozen=True)
class StopDecision:
    """The one pure stop-relation result consumed by live/replay paths."""

    stop_class: str | None
    trace: StopTrace


def action_domain_identity(actions: Mapping[str, object]) -> str:
    """Return a stable identity for the finite action/observation domain.

    IF-EQUIV is scoped not merely by a transition AST but by the selections
    and observations the bounded coordinator is actually allowed to consider.
    Keep every such consumed finite field in this explicit projection even
    though the enclosing model identity also cryptographically binds it.
    """

    if not isinstance(actions, Mapping):
        raise ValueError("finite action domain is not a mapping")
    def fraction_key(value: object) -> tuple[int, int]:
        numerator = getattr(value, "numerator", None)
        denominator = getattr(value, "denominator", None)
        if type(numerator) is not int or type(denominator) is not int or denominator <= 0:
            raise ValueError("finite action domain has an invalid exact measurement tick")
        return numerator, denominator

    items: list[tuple[object, ...]] = []
    for action_id, action in actions.items():
        if type(action_id) is not str or not action_id:
            raise ValueError("finite action domain has an invalid action identity")
        kind = getattr(action, "kind", None)
        transition_json = getattr(action, "transition_json", None)
        action_value_id = getattr(action, "action_id", None)
        cost = getattr(action, "cost", None)
        detail_charges = getattr(action, "detail_charges", None)
        enabled_summaries = getattr(action, "enabled_summaries", None)
        observable_by_hypothesis = getattr(action, "observable_by_hypothesis", None)
        measurement_ticks_by_hypothesis = getattr(action, "measurement_ticks_by_hypothesis", None)
        declared_empty_observable_ticks = getattr(action, "declared_empty_observable_ticks", None)
        declared_target = getattr(action, "declared_target", None)
        recover_when_unknown = getattr(action, "recover_when_unknown", None)
        if (
            type(action_value_id) is not str
            or action_value_id != action_id
            or type(kind) is not str
            or type(transition_json) is not str
            or type(cost) is not int
            or not isinstance(detail_charges, Mapping)
            or type(enabled_summaries) is not frozenset
            or not isinstance(observable_by_hypothesis, Mapping)
            or not isinstance(measurement_ticks_by_hypothesis, Mapping)
            or not isinstance(declared_empty_observable_ticks, Mapping)
            or (declared_target is not None and type(declared_target) is not str)
            or type(recover_when_unknown) is not bool
        ):
            raise ValueError("finite action domain has an invalid declared action")
        charges = tuple(sorted(detail_charges.items()))
        if any(type(name) is not str or type(amount) is not int for name, amount in charges):
            raise ValueError("finite action domain has an invalid charge projection")
        summaries = tuple(sorted(enabled_summaries))
        if any(type(item) is not str for item in summaries):
            raise ValueError("finite action domain has an invalid summary projection")
        emissions: list[tuple[str, tuple[str, ...]]] = []
        for hypothesis, values in sorted(observable_by_hypothesis.items()):
            if type(hypothesis) is not str or type(values) is not tuple or any(type(item) is not str for item in values):
                raise ValueError("finite action domain has an invalid observable projection")
            emissions.append((hypothesis, values))
        ticks: list[tuple[str, tuple[int, int]]] = []
        for hypothesis, tick in sorted(measurement_ticks_by_hypothesis.items()):
            if type(hypothesis) is not str:
                raise ValueError("finite action domain has an invalid measurement key")
            ticks.append((hypothesis, fraction_key(tick)))
        declared_empty: list[tuple[str, tuple[int, int]]] = []
        for observable, tick in sorted(declared_empty_observable_ticks.items()):
            if type(observable) is not str or not observable:
                raise ValueError("finite action domain has an invalid declared empty observable")
            declared_empty.append((observable, fraction_key(tick)))
        items.append((
            action_id,
            kind,
            cost,
            charges,
            summaries,
            transition_json,
            tuple(emissions),
            tuple(ticks),
            declared_target,
            recover_when_unknown,
            tuple(declared_empty),
        ))
    return _digest(tuple(sorted(items)))


def conservative_equivalence_status(
    *,
    context: _ContextLike,
    history: _HistoryLike,
    frontiers: Mapping[str, tuple[_FrontierLike, ...]],
    action_domain_identity_value: str,
    path_limit: int,
    frontier_limit: int,
    observation_class_limit: int,
    calculation_diagnostic_codes: tuple[str, ...] = (),
) -> EquivalenceStatus:
    """Return only ``notEstablished`` or ``unknown`` for this bounded slice.

    A lack of a currently useful TEST, an empty finite search, or a missing
    proof backend never produces ``established``.  Unknown/conservative input
    and reached finite bounds are made visible to callers instead of being
    silently recast as an equivalence result.
    """

    if (
        type(calculation_diagnostic_codes) is not tuple
        or any(type(code) is not str or not code for code in calculation_diagnostic_codes)
    ):
        raise ValueError("calculation diagnostics must be an exact nonblank-string tuple")
    diagnostic_codes = tuple(sorted(set(calculation_diagnostic_codes)))
    # These are controlled finite-calculation outcomes, not proof outcomes.
    # Preserve them in the trace instead of allowing a later caller to
    # collapse an unsupported AST or a reached bound into the generic
    # "no proof backend" explanation.
    specific_calculation_unknown = tuple(
        code
        for code in diagnostic_codes
        if (
            code == "COMPUTATION-UNKNOWN"
            or code.startswith("UNSUPPORTED-")
            or code.endswith("-LIMIT")
            or code.endswith("-LIMIT-REACHED")
        )
    )
    calculation_unknown = specific_calculation_unknown or tuple(
        code for code in diagnostic_codes
        if code == "CONSERVATIVE-PREDICTION-GAP"
    )
    hypotheses = tuple(sorted(history.hypotheses))
    if context.q_status != "KNOWN":
        tag, reason = "unknown", "SESSION-UNKNOWN"
    elif (
        any(status == "CONSERVATIVE-UNKNOWN" for status in history.status_by_hypothesis.values())
        or any(
            path.status == "CONSERVATIVE-UNKNOWN"
            for paths in frontiers.values()
            for path in paths
        )
    ):
        tag, reason = "unknown", "CONSERVATIVE-UNKNOWN"
    elif any(
        len(paths) >= frontier_limit
        for paths in frontiers.values()
    ):
        tag, reason = "unknown", "FRONTIER-LIMIT-REACHED"
    elif any(
        path.path_length >= path_limit
        for paths in frontiers.values()
        for path in paths
    ):
        tag, reason = "unknown", "PATH-LIMIT-REACHED"
    elif calculation_unknown:
        tag, reason = "unknown", f"CALCULATION-{calculation_unknown[0]}"
    else:
        tag, reason = "notEstablished", "NO-VERIFIED-PROOF-BACKEND"
    return EquivalenceStatus(
        tag=tag,
        reason=reason,
        hypotheses=hypotheses,
        history_version=history.version,
        action_domain_identity=action_domain_identity_value,
        path_limit=path_limit,
        frontier_limit=frontier_limit,
        observation_class_limit=observation_class_limit,
        calculation_diagnostic_codes=diagnostic_codes,
    )


def evaluate_stop(
    *,
    phase: str,
    context: _ContextLike,
    history: _HistoryLike,
    frontiers: Mapping[str, tuple[_FrontierLike, ...]],
    resources: _ResourceLike,
    stop_inputs: StopInputs,
    model_identity: str,
    authority_identity: str,
    action_domain_identity_value: str,
    path_limit: int,
    frontier_limit: int,
    observation_class_limit: int,
    forced_stop_class: str | None = None,
    forced_reason: str | None = None,
    admission_exit: tuple[str, str] | None = None,
    calculation_diagnostic_codes: tuple[str, ...] = (),
) -> StopDecision:
    """Apply the finite P1--P5 priority relation to one validated state.

    ``forced_stop_class`` is reserved for the already-charged S7 retry-cap
    terminal.  It is intentionally evaluated outside P1--P5 so a retry error
    cannot be overwritten by the normal resource branch.
    """

    if phase not in {"ENTRY", "POST-UPDATE", "RETRY"}:
        raise ValueError("stop phase is outside the controlled vocabulary")
    equivalence = conservative_equivalence_status(
        context=context,
        history=history,
        frontiers=frontiers,
        action_domain_identity_value=action_domain_identity_value,
        path_limit=path_limit,
        frontier_limit=frontier_limit,
        observation_class_limit=observation_class_limit,
        calculation_diagnostic_codes=calculation_diagnostic_codes,
    )
    residuals = stop_inputs.active_residuals
    if admission_exit is not None and (
        type(admission_exit) is not tuple
        or len(admission_exit) != 2
        or admission_exit[0] not in {
            "Stop-Budget",
            "Stop-Error",
            "Stop-NoDistinguisher",
            "Stop-Prediction-Gap",
        }
        or type(admission_exit[1]) is not str
        or not admission_exit[1]
    ):
        raise ValueError("admission stop exit is outside the controlled vocabulary")
    if forced_stop_class is not None:
        if forced_stop_class != "Stop-Error" or forced_reason != "RETRY-CAP-EXHAUSTED":
            raise ValueError("forced stop is reserved for retry-cap exhaustion")
        stop_class, reason = forced_stop_class, forced_reason
    elif history.processed and not history.hypotheses:
        stop_class, reason = "Stop-Empty", "PROCESSED-EMPTY-HISTORY"
    elif len(history.hypotheses) == 1:
        stop_class, reason = "Stop-Singleton", "SINGLETON-HISTORY"
    elif residuals:
        stop_class, reason = "Stop-645", "CURRENT-NAMED-645-RESIDUAL"
    # No current branch can emit ``established``: the optional proof backend
    # is deliberately outside B/C-2C.  Keep this guarded clause so a future
    # verified backend must explicitly extend this type rather than changing
    # a no-distinguisher or unknown result into proof by accident.
    elif equivalence.tag == "established":  # pragma: no cover - no producer in this slice
        stop_class, reason = "Stop-Equivalent", "VERIFIED-FINITE-PROOF"
    elif resources.remaining == 0:
        stop_class, reason = "Stop-Budget", "RESOURCE-EXHAUSTED"
    elif admission_exit is not None:
        stop_class, reason = admission_exit
    else:
        stop_class, reason = None, equivalence.reason
    # The trace is an evidence snapshot, not an alias to the S0 stop input.
    # Frozen dataclasses are still vulnerable to a hostile ``object.__setattr__``
    # caller, so a trace must not share a residual object with the session's
    # authoritative stop inputs.  A later live/replay evaluation then always
    # reads the original frozen input; mutation of retained evidence is caught
    # by normal trace recomputation instead of changing the next stop class.
    trace_residuals = tuple(
        Named645Residual(
            requirement_id=item.requirement_id,
            dependency_id=item.dependency_id,
            source_unit_id=item.source_unit_id,
            contract_id=item.contract_id,
            context_id=item.context_id,
            input_identity=item.input_identity,
        )
        for item in residuals
    )
    trace_payload = (
        phase,
        stop_class,
        reason,
        tuple(sorted(history.hypotheses)),
        history.version,
        resources.mode,
        resources.remaining,
        context.retry_count,
        context.retry_cap,
        stop_inputs.applicability_status,
        stop_inputs.context_id,
        stop_inputs.applicability_input_identity,
        tuple(item.identity for item in residuals),
        equivalence,
        model_identity,
        authority_identity,
    )
    trace = StopTrace(
        phase=phase,
        stop_class=stop_class,
        reason=reason,
        final_hypotheses=tuple(sorted(history.hypotheses)),
        history_version=history.version,
        resource_mode=resources.mode,
        resource_remaining=resources.remaining,
        retry_count=context.retry_count,
        retry_cap=context.retry_cap,
        applicability_status=stop_inputs.applicability_status,
        applicability_context_id=stop_inputs.context_id,
        applicability_input_identity=stop_inputs.applicability_input_identity,
        active_named_645_residuals=trace_residuals,
        equivalence=equivalence,
        model_identity=model_identity,
        authority_identity=authority_identity,
        trace_identity=_digest(trace_payload),
    )
    return StopDecision(stop_class=stop_class, trace=trace)
