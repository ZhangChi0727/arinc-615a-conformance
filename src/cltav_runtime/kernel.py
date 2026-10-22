"""Finite, explicit CL-TAV path propagation.

The implementation follows the bounded ``AR-FINITE`` contract.  It handles
only its declared AST/update vocabulary and exact rational one-clock witness
projection.  Unsupported syntax and resource exhaustion deliberately retain
the caller's hypothesis rather than treating a failure to compute as proof of
incompatibility.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import subprocess
from types import MappingProxyType
from typing import Any, Mapping, Sequence


_MODEL_CONTEXT_TOKEN = object()
_CONTRACT_SNAPSHOT_TOKEN = object()
_PROVENANCE_WRITE_TOKEN = object()
_SUPPORTED_GUARD_TAGS = (
    "TRUE", "AND", "STATE-EQUALS", "RATIONAL-INTERVAL-CONTAINS",
    "TYPED-FIELD-EQUALS",
)
_SUPPORTED_UPDATE_TAGS = (
    "STATE-ASSIGN", "CLOCK-RESET-TO-ZERO", "TYPED-FIELD-ASSIGN",
)
_AUTHORITY_MERGE_FIELDS = (
    "hypothesisId", "controlStateId", "clockConstraint", "typedStore",
    "historyProvenance",
)
_SUPPORTED_LIMIT_BEHAVIOR = {
    "pathLength": "CONSERVATIVE-UNKNOWN",
    "frontierStates": "CONSERVATIVE-UNKNOWN",
    "hypotheses": "SPEC-ERROR",
    "actions": "ADMIT-REFUSED",
    "observationClasses": "PredictionGapError",
}
_SUPPORTED_INTERNAL_RESULTS = (
    "FEASIBLE", "INFEASIBLE", "COMPUTATION-UNKNOWN", "UNSUPPORTED-SYNTAX",
    "LIMIT-REACHED", "EMPTY-HISTORY",
)
# This is the bounded runtime's interface projection, not a claim to execute
# every interface in the development contract.  It pins the return conventions
# consumed at the finite-kernel boundary while allowing unrelated interfaces to
# evolve in their own controlled release.
_SUPPORTED_RESULT_MAPPING = {
    "IF-HIST-UPDATE": {
        "success": ("HistoryHandlePrime", "Hprime", "Stop-Empty"),
        "failure": ("Stop-Empty", "RESOURCE-UNKNOWN", "CONSERVATIVE-UNKNOWN"),
    },
    "IF-EQUIV": {
        "success": ("established", "notEstablished", "unknown"),
        "failure": ("UNKNOWN", "RESOURCE-UNKNOWN"),
    },
    "IF-RESOURCE-STOP": {
        "success": ("stopClass", "finalH", "trace"),
        "failure": ("Stop-Budget", "Stop-Error", "Stop-645"),
    },
}
_SUPPORTED_CLOCK_CONSTRAINT = {
    "type": "canonical-difference-bounds",
    "boundType": "rational",
    "finiteWitnessProjection": "one declared clock ID plus its rational interval; W1/W2 have exact one-clock semantics",
    "unsupportedProjection": "multi-clock or cross-clock relation without a named DBM projection is SPEC-ERROR, never a computed successor",
    "timeAdvance": "one shared nonnegative rational delta",
    "reset": "substitute exact zero before canonicalization",
    "feasibility": ("FEASIBLE", "INFEASIBLE", "COMPUTATION-UNKNOWN"),
}


@dataclass(frozen=True)
class KernelDiagnostic:
    """A controlled diagnostic; never an IUT verdict."""

    code: str
    message: str


@dataclass(frozen=True)
class ContractSnapshot:
    """A Git-object snapshot of the controlled contract actually consumed.

    The factory reads the requested ``commit:path`` object directly.  It never
    falls back to a mutable worktree file, and callers cannot manufacture a
    verified snapshot by supplying matching arbitrary bytes and a digest.
    """

    contract_commit: str
    contract_path: str
    contract_blob_sha256: str
    _content: bytes = field(default=b"", init=False, compare=False, repr=False)
    _verification_token: object | None = field(default=None, init=False, compare=False, repr=False)

    @classmethod
    def from_git_object(
        cls, *, repository: Path | str, contract_commit: str, contract_path: str,
    ) -> "ContractSnapshot":
        path = _safe_contract_path(contract_path)
        if not isinstance(contract_commit, str) or len(contract_commit) != 40 or any(character not in "0123456789abcdef" for character in contract_commit):
            raise ValueError("contract commit identity is invalid")
        repository_path = Path(repository).resolve()
        if not repository_path.is_dir():
            raise ValueError("contract repository is not an existing directory")
        try:
            resolved_commit = subprocess.run(
                ["git", "-C", str(repository_path), "rev-parse", "--verify", f"{contract_commit}^{{commit}}"],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            ).stdout.strip()
            if resolved_commit != contract_commit:
                raise ValueError("contract commit does not resolve to the declared identity")
            content = subprocess.run(
                ["git", "-C", str(repository_path), "show", f"{resolved_commit}:{path}"],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            ).stdout
        except subprocess.CalledProcessError as exc:
            raise ValueError("controlled contract Git object cannot be loaded") from exc
        try:
            parsed = json.loads(content.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("controlled contract object must be UTF-8 JSON") from exc
        if not isinstance(parsed, Mapping):
            raise ValueError("controlled contract root must be an object")
        snapshot = cls(resolved_commit, path, sha256(content).hexdigest())
        object.__setattr__(snapshot, "_content", content)
        object.__setattr__(snapshot, "_verification_token", _CONTRACT_SNAPSHOT_TOKEN)
        return snapshot

    def _parsed_contract(self) -> Mapping[str, Any]:
        if not _verified_snapshot(self):
            raise ValueError("contract snapshot is not verified")
        parsed = json.loads(self._content.decode("utf-8"))
        if not isinstance(parsed, Mapping):
            raise ValueError("controlled contract root must be an object")
        return parsed


@dataclass(frozen=True)
class ModelContext:
    """Verified, immutable inputs for one finite-model projection.

    The caller first obtains a :class:`ContractSnapshot` from an exact Git
    ``commit:path`` object.  The factory validates the bounded runtime's
    compatibility projection before freezing the model declaration, so a
    mutable worktree edit or an incompatible controlled-contract revision
    cannot be silently substituted.  Snapshot/factory failures raise
    ``ValueError``; propagation and merge failures use ``KernelResult``
    diagnostics and retain their public input paths.
    """

    contract_commit: str
    contract_path: str
    contract_blob_sha256: str
    model_sha256: str
    projection_clock: str
    state_ids: frozenset[str]
    clock_ids: frozenset[str]
    typed_domains: Mapping[str, frozenset[Any]]
    supported_guard_tags: tuple[str, ...]
    supported_update_tags: tuple[str, ...]
    authority_merge_fields: tuple[str, ...]
    identity: str
    provenance_store: "ProvenanceStore" = field(
        default_factory=lambda: ProvenanceStore(), compare=False, repr=False,
    )
    _binding_sha256: str = field(default="", init=False, compare=False, repr=False)
    _verification_token: object | None = field(default=None, init=False, compare=False, repr=False)

    @classmethod
    def build(
        cls, *, snapshot: ContractSnapshot, model: Mapping[str, Any], projection_clock: str,
    ) -> "ModelContext":
        if not _verified_snapshot(snapshot):
            raise ValueError("model context requires a verified controlled contract snapshot")
        guard_tags, update_tags, merge_fields = _finite_contract_vocabulary(snapshot._parsed_contract())
        if set(model) != {"stateIds", "clockIds", "typedDomains"}:
            raise ValueError("finite runtime model must use exactly the declared model fields")
        states, clocks, domains = model.get("stateIds"), model.get("clockIds"), model.get("typedDomains")
        error = _validate_model_domain(states, clocks, domains)
        if error is not None or not isinstance(projection_clock, str) or projection_clock not in clocks or len(clocks) != 1:
            raise ValueError("finite model declaration is outside the supported projection")
        frozen_domains = MappingProxyType({key: frozenset(value) for key, value in domains.items()})
        model_bytes = json.dumps(_canonical_model(model), sort_keys=True, separators=(",", ":")).encode("utf-8")
        model_sha = sha256(model_bytes).hexdigest()
        identity = _model_context_identity(
            snapshot.contract_commit, snapshot.contract_path, snapshot.contract_blob_sha256, model_sha,
            projection_clock,
        )
        context = cls(
            contract_commit=snapshot.contract_commit,
            contract_path=snapshot.contract_path,
            contract_blob_sha256=snapshot.contract_blob_sha256,
            model_sha256=model_sha,
            projection_clock=projection_clock,
            state_ids=frozenset(states),
            clock_ids=frozenset(clocks),
            typed_domains=frozen_domains,
            supported_guard_tags=guard_tags,
            supported_update_tags=update_tags,
            authority_merge_fields=merge_fields,
            identity=identity,
        )
        object.__setattr__(context, "_binding_sha256", _context_binding_digest(context))
        object.__setattr__(context, "_verification_token", _MODEL_CONTEXT_TOKEN)
        return context

    def read_only_replay_context(self) -> "ModelContext":
        """Return an equally verified context with an isolated evidence store.

        Finite propagation appends content-addressed step records as it derives
        successors. A caller that only replays an already retained public
        ledger must therefore not use this context's shared store: replay is a
        validation operation, not a new source of runtime provenance. The
        immutable model authority and all existing records are retained, while
        deterministic replay records are inserted only in the copy.
        """

        if not _verified_context(self):
            raise ValueError("read-only replay requires a verified model context")
        replay = ModelContext(
            contract_commit=self.contract_commit,
            contract_path=self.contract_path,
            contract_blob_sha256=self.contract_blob_sha256,
            model_sha256=self.model_sha256,
            projection_clock=self.projection_clock,
            state_ids=self.state_ids,
            clock_ids=self.clock_ids,
            typed_domains=self.typed_domains,
            supported_guard_tags=self.supported_guard_tags,
            supported_update_tags=self.supported_update_tags,
            authority_merge_fields=self.authority_merge_fields,
            identity=self.identity,
            provenance_store=self.provenance_store.copy(),
        )
        object.__setattr__(replay, "_binding_sha256", self._binding_sha256)
        object.__setattr__(replay, "_verification_token", _MODEL_CONTEXT_TOKEN)
        return replay


@dataclass(frozen=True)
class Interval:
    """Exact rational interval with preserved endpoint topology."""

    lower: Fraction
    upper: Fraction
    lower_closed: bool
    upper_closed: bool

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "Interval":
        if set(value) != {"lower", "upper", "lowerClosed", "upperClosed"}:
            raise ValueError("interval fields are not canonical")
        try:
            lower = _fraction(value["lower"])
            upper = _fraction(value["upper"])
            lower_closed = value["lowerClosed"]
            upper_closed = value["upperClosed"]
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("invalid rational interval") from exc
        if not isinstance(lower_closed, bool) or not isinstance(upper_closed, bool):
            raise ValueError("interval endpoint closure must be boolean")
        if lower > upper or (lower == upper and not (lower_closed and upper_closed)):
            raise ValueError("interval is empty")
        return cls(lower, upper, lower_closed, upper_closed)

    def shifted(self, delta: Fraction) -> "Interval":
        return Interval(self.lower + delta, self.upper + delta, self.lower_closed, self.upper_closed)

    def intersect(self, other: "Interval") -> "Interval | None":
        lower = max(self.lower, other.lower)
        upper = min(self.upper, other.upper)
        lower_closed = (
            self.lower_closed if self.lower > other.lower
            else other.lower_closed if other.lower > self.lower
            else self.lower_closed and other.lower_closed
        )
        upper_closed = (
            self.upper_closed if self.upper < other.upper
            else other.upper_closed if other.upper < self.upper
            else self.upper_closed and other.upper_closed
        )
        if lower > upper or (lower == upper and not (lower_closed and upper_closed)):
            return None
        return Interval(lower, upper, lower_closed, upper_closed)

    def as_mapping(self) -> dict[str, Any]:
        return {
            "lower": _fraction_mapping(self.lower),
            "upper": _fraction_mapping(self.upper),
            "lowerClosed": self.lower_closed,
            "upperClosed": self.upper_closed,
        }


@dataclass(frozen=True)
class FrontierEntry:
    """One explicit path in a finite, versioned history frontier."""

    hypothesis_id: str
    control_state_id: str
    clocks: Mapping[str, Interval]
    typed_store: Mapping[str, Any]
    path_length: int
    history_provenance: tuple[str, ...]
    status: str = "KNOWN"
    model_identity: str = ""

    def __post_init__(self) -> None:
        """Take immutable snapshots so later caller mutation cannot rewrite history."""
        object.__setattr__(self, "clocks", MappingProxyType(dict(self.clocks)))
        object.__setattr__(self, "typed_store", MappingProxyType(dict(self.typed_store)))
        object.__setattr__(self, "history_provenance", tuple(self.history_provenance))

    def merge_key(self) -> tuple[Any, ...]:
        """Return the five authority fields used by production merging.

        ``path_length`` and ``status`` are metadata checked separately so a
        caller never mistakes this key for a complete entry snapshot.
        """
        return _authority_merge_key(self)


@dataclass(frozen=True)
class ProvenanceRecord:
    """One compact, content-addressed root or finite transition record.

    Records point only to their immediate parent.  A frontier retains the
    reference chain for transparent merge identity, while the records share
    the payloads instead of nesting a growing display trace at every step.
    """

    reference: str
    kind: str
    context_identity: str
    parent_reference: str | None
    root_id: str | None
    transition_id: str | None
    transition_identity: str | None
    transition: tuple[Any, ...] | None
    delta: Fraction | None
    pre_update_clocks: tuple[tuple[str, Interval], ...]
    observations: tuple[tuple[str, Interval], ...]
    result_identity: tuple[Any, ...]

    def as_mapping(self) -> dict[str, Any]:
        """Return a serialisable, inspectable source record."""
        return {
            "reference": self.reference,
            "kind": self.kind,
            "contextIdentity": self.context_identity,
            "parentReference": self.parent_reference,
            "rootId": self.root_id,
            "transitionId": self.transition_id,
            "transitionIdentity": self.transition_identity,
            "transition": None if self.transition is None else _json_safe(_transition_from_canonical(self.transition)),
            "delta": None if self.delta is None else _fraction_mapping(self.delta),
            "preUpdateClockConstraints": {
                name: interval.as_mapping() for name, interval in self.pre_update_clocks
            },
            "observationConstraints": {
                name: interval.as_mapping() for name, interval in self.observations
            },
            "resultIdentity": _result_identity_mapping(self.result_identity),
        }


class ProvenanceStore:
    """Append-only, in-process storage for verifiable compact source records."""

    def __init__(self) -> None:
        self._records: dict[str, ProvenanceRecord] = {}

    def records(self) -> Mapping[str, ProvenanceRecord]:
        """Return an immutable snapshot; callers cannot rewrite history."""
        return MappingProxyType(dict(self._records))

    def resolve(self, reference: str) -> ProvenanceRecord | None:
        return self._records.get(reference)

    def copy(self) -> "ProvenanceStore":
        """Copy immutable records for deterministic, side-effect-free replay."""

        copied = ProvenanceStore()
        copied._records = dict(self._records)
        return copied

    def _register_root(
        self, context: ModelContext, root_id: str, entry: FrontierEntry, *, token: object,
    ) -> str:
        if token is not _PROVENANCE_WRITE_TOKEN:
            raise ValueError("root records may be created only by the verified runtime")
        if not isinstance(root_id, str) or not root_id:
            raise ValueError("root ID must be a nonempty string")
        candidate = ProvenanceRecord(
            reference="", kind="ROOT", context_identity=context.identity,
            parent_reference=None, root_id=root_id, transition_id=None,
            transition_identity=None, transition=None, delta=None, pre_update_clocks=(),
            observations=(),
            result_identity=_entry_result_identity(entry),
        )
        reference = _record_reference(candidate)
        record = ProvenanceRecord(reference=reference, **_record_fields(candidate))
        self._insert(record)
        return reference

    def _append_step(
        self, context: ModelContext, parent: FrontierEntry,
        transition: Mapping[str, Any], pre_update_clocks: Mapping[str, Interval],
        delta: Fraction, observations: Mapping[str, Interval] | None,
        successor: FrontierEntry, *, token: object,
    ) -> ProvenanceRecord:
        if token is not _PROVENANCE_WRITE_TOKEN:
            raise ValueError("step records may be created only by verified propagation")
        parent_reference = parent.history_provenance[-1]
        candidate = ProvenanceRecord(
            reference="", kind="STEP", context_identity=context.identity,
            parent_reference=parent_reference, root_id=None,
            transition_id=transition["id"],
            transition_identity=sha256(repr(_canonical_transition(transition)).encode("utf-8")).hexdigest(),
            transition=_canonical_transition(transition),
            delta=delta,
            pre_update_clocks=tuple(sorted(pre_update_clocks.items())),
            observations=tuple(sorted((observations or {}).items())),
            result_identity=_entry_result_identity(successor),
        )
        reference = _record_reference(candidate)
        record = ProvenanceRecord(reference=reference, **_record_fields(candidate))
        self._insert(record)
        return record

    def verify_entry(self, context: ModelContext, entry: FrontierEntry) -> KernelDiagnostic | None:
        """Return a controlled provenance diagnostic for every malformed record."""
        try:
            return self._verify_entry(context, entry)
        except (AttributeError, KeyError, OverflowError, TypeError, ValueError) as exc:
            return KernelDiagnostic(
                "MALFORMED-PROVENANCE-RECORD", str(exc) or type(exc).__name__,
            )

    def _verify_entry(self, context: ModelContext, entry: FrontierEntry) -> KernelDiagnostic | None:
        refs = entry.history_provenance
        if not refs:
            return KernelDiagnostic("INVALID-PROVENANCE-CLOSURE", "frontier has no root source record")
        if len(refs) != entry.path_length + 1:
            return KernelDiagnostic("INVALID-PROVENANCE-CLOSURE", "path length and source-reference chain disagree")
        previous: str | None = None
        replayed_parent: FrontierEntry | None = None
        for index, reference in enumerate(refs):
            record = self._records.get(reference)
            if record is None:
                return KernelDiagnostic("MISSING-PROVENANCE-RECORD", "frontier references a source record that is not available")
            shape_error = _source_record_shape_error(record)
            if shape_error is not None:
                return shape_error
            if record.reference != reference or _record_reference(record) != reference:
                return KernelDiagnostic("TAMPERED-PROVENANCE-RECORD", "source record does not match its content address")
            if record.context_identity != context.identity:
                return KernelDiagnostic("PROVENANCE-CONTEXT-MISMATCH", "source record belongs to a different model context")
            if index == 0:
                if record.kind != "ROOT" or record.parent_reference is not None:
                    return KernelDiagnostic("INVALID-PROVENANCE-CLOSURE", "first source record is not a root")
                root_error, replayed_parent = _verify_root_record(context, record)
                if root_error is not None:
                    return root_error
            elif record.kind != "STEP" or record.parent_reference != previous:
                return KernelDiagnostic("INVALID-PROVENANCE-CLOSURE", "step source record does not reference its immediate parent")
            else:
                assert replayed_parent is not None
                semantic_error, replayed_parent = _verify_step_record(context, replayed_parent, record)
                if semantic_error is not None:
                    return semantic_error
            previous = reference
        if replayed_parent is None or _entry_result_identity(replayed_parent) != _entry_result_identity(entry):
            return KernelDiagnostic("PROVENANCE-RESULT-MISMATCH", "source record does not describe the returned frontier entry")
        return None

    def _insert(self, record: ProvenanceRecord) -> None:
        existing = self._records.get(record.reference)
        if existing is not None and existing != record:
            raise ValueError("content-address collision has incompatible payload")
        self._records[record.reference] = record


def initial_entry(
    context: ModelContext, *, hypothesis_id: str, control_state_id: str,
    clocks: Mapping[str, Interval], typed_store: Mapping[str, Any], root_id: str,
    status: str = "KNOWN",
) -> FrontierEntry:
    """Create the only supported public initial path for a model context."""
    if not _verified_context(context):
        raise ValueError("initial entry requires a verified model context")
    provisional = FrontierEntry(
        hypothesis_id, control_state_id, clocks, typed_store, 0, (root_id,), status,
        context.identity,
    )
    diagnostics: list[KernelDiagnostic] = []
    if not _valid_entry(provisional, set(context.state_ids), set(context.clock_ids), context.typed_domains, diagnostics):
        raise ValueError("invalid initial frontier entry")
    reference = context.provenance_store._register_root(
        context, root_id, provisional, token=_PROVENANCE_WRITE_TOKEN,
    )
    return FrontierEntry(
        hypothesis_id, control_state_id, clocks, typed_store, 0, (reference,), status,
        context.identity,
    )


@dataclass(frozen=True)
class KernelResult:
    """The typed, conservative result of a single finite transition step."""

    kind: str
    entries: tuple[FrontierEntry, ...]
    diagnostics: tuple[KernelDiagnostic, ...] = field(default_factory=tuple)
    source_records: tuple[ProvenanceRecord, ...] = field(default_factory=tuple)

    @property
    def feasible(self) -> bool:
        return self.kind == "FEASIBLE"


def propagate_transition(
    entry: FrontierEntry | object,
    transition: Mapping[str, Any] | object,
    *,
    state_ids: set[str],
    clock_ids: set[str],
    typed_domains: Mapping[str, set[Any]],
    context: ModelContext | None = None,
    observation_intervals: Mapping[str, Interval] | None = None,
    delta: Fraction | None = None,
    path_limit: int,
    frontier_limit: int,
) -> KernelResult:
    """Apply one declared transition without implicit discretisation.

    ``INFEASIBLE`` is the only result that represents a proven lack of this
    successor.  Invalid models, unsupported syntax, and configured limits are
    controlled returns that preserve the incoming path/hypothesis.
    """
    try:
        return _propagate_transition(
            entry, transition, state_ids=state_ids, clock_ids=clock_ids,
            typed_domains=typed_domains, context=context, observation_intervals=observation_intervals,
            delta=delta, path_limit=path_limit, frontier_limit=frontier_limit,
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        retained = (entry,) if isinstance(entry, FrontierEntry) else ()
        return KernelResult(
            "SPEC-ERROR", retained,
            (KernelDiagnostic("MALFORMED-KERNEL-INPUT", str(exc) or type(exc).__name__),),
        )


def _propagate_transition(
    entry: FrontierEntry | object,
    transition: Mapping[str, Any] | object,
    *,
    state_ids: set[str],
    clock_ids: set[str],
    typed_domains: Mapping[str, set[Any]],
    context: ModelContext | None,
    observation_intervals: Mapping[str, Interval] | None,
    delta: Fraction | None,
    path_limit: int,
    frontier_limit: int,
) -> KernelResult:
    """Implementation body protected by :func:`propagate_transition`."""
    if not isinstance(entry, FrontierEntry):
        return KernelResult("SPEC-ERROR", (), (KernelDiagnostic("MALFORMED-KERNEL-INPUT", "frontier entry is not a FrontierEntry"),))
    if not isinstance(transition, Mapping):
        return KernelResult("SPEC-ERROR", (entry,), (KernelDiagnostic("MALFORMED-KERNEL-INPUT", "transition is not an object"),))
    model_error = _validate_model_domain(state_ids, clock_ids, typed_domains)
    if model_error is not None:
        return KernelResult("SPEC-ERROR", (entry,), (model_error,))
    if not _verified_context(context):
        return KernelResult("SPEC-ERROR", (entry,), (KernelDiagnostic("UNVERIFIED-MODEL-CONTEXT", "finite propagation requires a verified model context"),))
    if (
        context.state_ids != frozenset(state_ids)
        or context.clock_ids != frozenset(clock_ids)
        or dict(context.typed_domains) != {key: frozenset(value) for key, value in typed_domains.items()}
    ):
        return KernelResult("SPEC-ERROR", (entry,), (KernelDiagnostic("MODEL-CONTEXT-MISMATCH", "consumed model inputs differ from the verified context"),))
    if entry.model_identity != context.identity:
        return KernelResult("SPEC-ERROR", (entry,), (KernelDiagnostic("MODEL-IDENTITY-MISMATCH", "frontier entry does not belong to this model context"),))
    if len(clock_ids) != 1:
        return KernelResult("SPEC-ERROR", (entry,), (KernelDiagnostic("UNPROJECTED-MULTI-CLOCK", "this finite witness implementation accepts exactly one declared clock"),))
    diagnostics: list[KernelDiagnostic] = []
    if not _valid_entry(entry, state_ids, clock_ids, typed_domains, diagnostics):
        return KernelResult("SPEC-ERROR", (entry,), tuple(diagnostics))
    provenance_error = context.provenance_store.verify_entry(context, entry)
    if provenance_error is not None:
        return KernelResult("SPEC-ERROR", (entry,), (provenance_error,))
    if not _valid_limit(path_limit, minimum=0) or not _valid_limit(frontier_limit, minimum=1):
        return KernelResult("SPEC-ERROR", (entry,), (KernelDiagnostic("INVALID-LIMIT", "path and frontier limits must be finite nonnegative integers"),))
    delta_error, normalized_delta = _normalize_delta(delta)
    if delta_error is not None:
        return KernelResult("SPEC-ERROR", (entry,), (delta_error,))
    transition_error = _validate_transition(transition, state_ids, clock_ids, typed_domains)
    if transition_error is not None:
        if transition_error.code in {"AST-DEPTH-LIMIT", "AST-NODE-LIMIT"}:
            return KernelResult("CONSERVATIVE-UNKNOWN", (entry,), (transition_error,))
        return KernelResult("SPEC-ERROR", (entry,), (transition_error,))
    observation_error = _validate_observation_constraints(observation_intervals, clock_ids)
    if observation_error is not None:
        return KernelResult("SPEC-ERROR", (entry,), (observation_error,))
    if entry.path_length >= path_limit:
        return KernelResult("CONSERVATIVE-UNKNOWN", (entry,), (KernelDiagnostic("PATH-LIMIT", "declared path bound reached; hypothesis retained"),))
    if transition.get("source") != entry.control_state_id:
        if entry.status == "CONSERVATIVE-UNKNOWN":
            return KernelResult("CONSERVATIVE-UNKNOWN", (entry,), (KernelDiagnostic("CONSERVATIVE-PATH", "unknown effect prevents path exclusion"),))
        return KernelResult("INFEASIBLE", ())
    updates = transition.get("simultaneousUpdates")
    guard = transition.get("guardAst")
    assert normalized_delta is not None
    delta = normalized_delta

    advanced = {name: interval.shifted(delta) for name, interval in entry.clocks.items()}
    guarded, guard_error = _apply_guard(entry.control_state_id, entry.typed_store, advanced, guard, clock_ids)
    if guard_error is not None:
        return KernelResult("SPEC-ERROR", (entry,), (guard_error,))
    if guarded is None:
        if entry.status == "CONSERVATIVE-UNKNOWN":
            return KernelResult("CONSERVATIVE-UNKNOWN", (entry,), (KernelDiagnostic("CONSERVATIVE-PATH", "unknown effect prevents path exclusion"),))
        return KernelResult("INFEASIBLE", ())
    if observation_intervals:
        guarded = dict(guarded)
        for clock, observation in observation_intervals.items():
            intersection = guarded[clock].intersect(observation)
            if intersection is None:
                if entry.status == "CONSERVATIVE-UNKNOWN":
                    return KernelResult("CONSERVATIVE-UNKNOWN", (entry,), (KernelDiagnostic("CONSERVATIVE-PATH", "unknown effect prevents path exclusion"),))
                return KernelResult("INFEASIBLE", ())
            guarded[clock] = intersection

    successor, source_record, update_error = _apply_updates(
        entry, transition, guarded, state_ids, clock_ids, typed_domains, delta,
        observation_intervals, context,
    )
    if update_error is not None:
        return KernelResult("SPEC-ERROR", (entry,), (update_error,))
    assert successor is not None and source_record is not None
    return KernelResult("FEASIBLE", (successor,), source_records=(source_record,))


def merge_frontier(entries: Sequence[FrontierEntry], *, frontier_limit: int, context: ModelContext | None = None) -> KernelResult:
    """Merge only fully identical, whole-history frontiers."""
    retained: tuple[FrontierEntry, ...] = ()
    try:
        retained = tuple(entries)
        if not _verified_context(context):
            return KernelResult("SPEC-ERROR", retained, (KernelDiagnostic("UNVERIFIED-MODEL-CONTEXT", "finite merge requires a verified model context"),))
        if not _valid_limit(frontier_limit, minimum=1):
            return KernelResult("SPEC-ERROR", retained, (KernelDiagnostic("INVALID-LIMIT", "frontier limit must be a positive integer"),))
        for entry in retained:
            if not _valid_merge_entry(entry, context):
                return KernelResult("SPEC-ERROR", retained, (KernelDiagnostic("MALFORMED-FRONTIER", "frontier contains an invalid entry"),))
            provenance_error = context.provenance_store.verify_entry(context, entry)
            if provenance_error is not None:
                return KernelResult("SPEC-ERROR", retained, (provenance_error,))
        merged: dict[tuple[Any, ...], FrontierEntry] = {}
        for entry in retained:
            authority_key = _authority_merge_key(entry)
            existing = merged.get(authority_key)
            if existing is not None and (existing.status != entry.status or existing.path_length != entry.path_length):
                return KernelResult("CONSERVATIVE-UNKNOWN", retained, (KernelDiagnostic("MERGE-METADATA-CONFLICT", "same authority merge key has incompatible status or pathLength"),))
            merged.setdefault(authority_key, entry)
        values = tuple(merged.values())
        if len(values) > frontier_limit:
            return KernelResult("CONSERVATIVE-UNKNOWN", retained, (KernelDiagnostic("FRONTIER-LIMIT", "frontier state limit reached; no hypothesis removed"),))
        return KernelResult("FEASIBLE", values)
    except (AttributeError, TypeError, ValueError) as exc:
        return KernelResult("SPEC-ERROR", retained, (KernelDiagnostic("MALFORMED-FRONTIER", str(exc) or type(exc).__name__),))


_MAX_GUARD_DEPTH = 64
_MAX_GUARD_NODES = 256


def _validate_guard_ast(
    ast: Mapping[str, Any],
    state_ids: set[str],
    clock_ids: set[str],
    typed_domains: Mapping[str, set[Any]],
) -> KernelDiagnostic | None:
    """Boundedly validate every node before recursive evaluation begins."""
    pending: list[tuple[object, int, frozenset[int]]] = [(ast, 1, frozenset())]
    count = 0
    while pending:
        node, depth, ancestors = pending.pop()
        count += 1
        if count > _MAX_GUARD_NODES:
            return KernelDiagnostic("AST-NODE-LIMIT", "guard exceeds the declared finite node limit")
        if depth > _MAX_GUARD_DEPTH:
            return KernelDiagnostic("AST-DEPTH-LIMIT", "guard exceeds the declared finite depth limit")
        if not isinstance(node, Mapping):
            return KernelDiagnostic("INVALID-GUARD-AST", "guard node is not a tagged object")
        identity = id(node)
        if identity in ancestors:
            return KernelDiagnostic("CYCLIC-GUARD-AST", "guard contains a cyclic reference")
        tag = node.get("tag")
        if tag == "TRUE":
            if set(node) != {"tag"}:
                return KernelDiagnostic("INVALID-GUARD-AST", "TRUE guard has unknown fields")
        elif tag == "AND":
            operands = node.get("operands")
            if set(node) != {"tag", "operands"} or not isinstance(operands, list) or not operands:
                return KernelDiagnostic("INVALID-GUARD-AST", "AND requires exactly a nonempty operands list")
            if len(operands) > _MAX_GUARD_NODES - count:
                return KernelDiagnostic("AST-NODE-LIMIT", "guard exceeds the declared finite node limit")
            next_ancestors = ancestors | {identity}
            pending.extend((operand, depth + 1, next_ancestors) for operand in operands)
        elif tag == "STATE-EQUALS":
            state = node.get("state")
            if set(node) != {"tag", "state"} or not isinstance(state, str) or state not in state_ids:
                return KernelDiagnostic("INVALID-GUARD-AST", "state guard uses an undeclared control state")
        elif tag == "TYPED-FIELD-EQUALS":
            field = node.get("field")
            if set(node) != {"tag", "field", "value"} or not isinstance(field, str) or field not in typed_domains or not _domain_contains(typed_domains[field], node.get("value")):
                return KernelDiagnostic("INVALID-GUARD-AST", "typed field guard is outside the declared domain")
        elif tag == "RATIONAL-INTERVAL-CONTAINS":
            if set(node) != {"tag", "clock", "interval"} or not isinstance(node.get("clock"), str) or node["clock"] not in clock_ids:
                return KernelDiagnostic("INVALID-GUARD-AST", "interval guard uses an undeclared clock")
            try:
                Interval.from_mapping(node["interval"])
            except (KeyError, TypeError, ValueError):
                return KernelDiagnostic("INVALID-GUARD-AST", "interval guard requires a canonical rational interval")
        else:
            return KernelDiagnostic("UNSUPPORTED-GUARD-AST", f"unsupported guard AST tag: {tag!r}")
    return None


def _validate_transition(
    transition: Mapping[str, Any], state_ids: set[str], clock_ids: set[str], typed_domains: Mapping[str, set[Any]],
) -> KernelDiagnostic | None:
    required = {"id", "source", "target", "guardAst", "simultaneousUpdates"}
    if set(transition) != required:
        return KernelDiagnostic("INVALID-TRANSITION", "transition must use exactly the declared finite transition fields")
    if any(not isinstance(transition[key], str) for key in ("id", "source", "target")):
        return KernelDiagnostic("INVALID-TRANSITION", "transition id/source/target must be strings")
    if transition["source"] not in state_ids or transition["target"] not in state_ids:
        return KernelDiagnostic("INVALID-TRANSITION", "transition source or target is undeclared")
    guard = transition["guardAst"]
    if not isinstance(guard, Mapping):
        return KernelDiagnostic("INVALID-TRANSITION", "guardAst is not a tagged object")
    diagnostic = _validate_guard_ast(guard, state_ids, clock_ids, typed_domains)
    if diagnostic is not None:
        return diagnostic
    updates = transition["simultaneousUpdates"]
    if not isinstance(updates, list):
        return KernelDiagnostic("INVALID-TRANSITION", "simultaneousUpdates must be a list")
    targets: set[tuple[str, str]] = set()
    for update in updates:
        diagnostic, target = _validate_update(update, state_ids, clock_ids, typed_domains)
        if diagnostic is not None:
            return diagnostic
        assert target is not None
        if target in targets:
            return KernelDiagnostic("CONFLICTING-UPDATE", "simultaneous updates write the same target")
        targets.add(target)
        if target[0] == "state" and update["state"] != transition["target"]:
            return KernelDiagnostic("CONFLICTING-UPDATE", "STATE-ASSIGN must agree with transition target")
    return None


def _validate_update(
    update: object, state_ids: set[str], clock_ids: set[str], typed_domains: Mapping[str, set[Any]],
) -> tuple[KernelDiagnostic | None, tuple[str, str] | None]:
    if not isinstance(update, Mapping):
        return KernelDiagnostic("INVALID-UPDATE", "update is not a tagged object"), None
    tag = update.get("tag")
    if tag == "STATE-ASSIGN":
        if set(update) != {"tag", "state"} or update.get("state") not in state_ids:
            return KernelDiagnostic("INVALID-UPDATE", "state update uses an undeclared control state"), None
        return None, ("state", "")
    if tag == "CLOCK-RESET-TO-ZERO":
        if set(update) != {"tag", "clock"} or not isinstance(update.get("clock"), str) or update["clock"] not in clock_ids:
            return KernelDiagnostic("INVALID-UPDATE", "clock reset uses an undeclared clock"), None
        return None, ("clock", update["clock"])
    if tag == "TYPED-FIELD-ASSIGN":
        field = update.get("field")
        if set(update) != {"tag", "field", "value"} or not isinstance(field, str) or field not in typed_domains or not _domain_contains(typed_domains[field], update.get("value")):
            return KernelDiagnostic("INVALID-UPDATE", "typed field update is outside its declared domain"), None
        return None, ("field", field)
    return KernelDiagnostic("UNSUPPORTED-UPDATE", f"unsupported update tag: {tag!r}"), None


def _validate_observation_constraints(
    observations: Mapping[str, Interval] | None, clock_ids: set[str],
) -> KernelDiagnostic | None:
    if observations is None:
        return None
    if not isinstance(observations, Mapping):
        return KernelDiagnostic("INVALID-OBSERVATION-CONSTRAINT", "observation constraints must be a mapping")
    for clock, observation in observations.items():
        if not isinstance(clock, str) or clock not in clock_ids or not _valid_interval(observation):
            return KernelDiagnostic("INVALID-OBSERVATION-CONSTRAINT", "observation uses an undeclared clock or non-interval value")
    return None


def _apply_guard(
    state: str,
    store: Mapping[str, Any],
    clocks: Mapping[str, Interval],
    ast: Mapping[str, Any],
    clock_ids: set[str],
) -> tuple[Mapping[str, Interval] | None, KernelDiagnostic | None]:
    tag = ast.get("tag")
    if tag == "TRUE":
        return clocks, None
    if tag == "AND":
        operands = ast.get("operands")
        if not isinstance(operands, list) or not operands:
            return None, KernelDiagnostic("INVALID-GUARD-AST", "AND requires a nonempty operands list")
        current: Mapping[str, Interval] | None = clocks
        for operand in operands:
            if not isinstance(operand, Mapping):
                return None, KernelDiagnostic("INVALID-GUARD-AST", "AND operand is not a tagged guard")
            current, error = _apply_guard(state, store, current or {}, operand, clock_ids)
            if error is not None or current is None:
                return current, error
        return current, None
    if tag == "STATE-EQUALS":
        expected = ast.get("state")
        return (clocks if isinstance(expected, str) and state == expected else None), None
    if tag == "TYPED-FIELD-EQUALS":
        field = ast.get("field")
        if not isinstance(field, str) or "value" not in ast:
            return None, KernelDiagnostic("INVALID-GUARD-AST", "typed field guard requires field and value")
        return (clocks if store.get(field) == ast["value"] else None), None
    if tag == "RATIONAL-INTERVAL-CONTAINS":
        clock = ast.get("clock")
        if not isinstance(clock, str) or clock not in clock_ids or clock not in clocks:
            return None, KernelDiagnostic("INVALID-GUARD-AST", "interval guard uses an undeclared clock")
        try:
            interval = Interval.from_mapping(ast["interval"])
        except (KeyError, TypeError, ValueError):
            return None, KernelDiagnostic("INVALID-GUARD-AST", "interval guard requires a canonical rational interval")
        intersection = clocks[clock].intersect(interval)
        if intersection is None:
            return None, None
        updated = dict(clocks)
        updated[clock] = intersection
        return updated, None
    return None, KernelDiagnostic("UNSUPPORTED-GUARD-AST", f"unsupported guard AST tag: {tag!r}")


def _apply_updates(
    entry: FrontierEntry,
    transition: Mapping[str, Any],
    clocks: Mapping[str, Interval],
    state_ids: set[str],
    clock_ids: set[str],
    typed_domains: Mapping[str, set[Any]],
    delta: Fraction,
    observations: Mapping[str, Interval] | None,
    context: ModelContext,
) -> tuple[FrontierEntry | None, ProvenanceRecord | None, KernelDiagnostic | None]:
    provisional = _successor_after_updates(entry, transition, clocks)
    try:
        record = context.provenance_store._append_step(
            context, entry, transition, clocks, delta, observations, provisional,
            token=_PROVENANCE_WRITE_TOKEN,
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        return None, None, KernelDiagnostic("PROVENANCE-RECORD-ERROR", str(exc) or type(exc).__name__)
    return FrontierEntry(
        hypothesis_id=provisional.hypothesis_id,
        control_state_id=provisional.control_state_id,
        clocks=provisional.clocks,
        typed_store=provisional.typed_store,
        path_length=provisional.path_length,
        history_provenance=entry.history_provenance + (record.reference,),
        status=provisional.status,
        model_identity=provisional.model_identity,
    ), record, None


def _successor_after_updates(
    entry: FrontierEntry, transition: Mapping[str, Any], clocks: Mapping[str, Interval],
) -> FrontierEntry:
    """Apply already-validated simultaneous updates without creating evidence."""
    next_state = transition["target"]
    next_clocks = dict(clocks)
    next_store = dict(entry.typed_store)
    for update in transition["simultaneousUpdates"]:
        tag = update["tag"]
        if tag == "STATE-ASSIGN":
            next_state = update["state"]
        elif tag == "CLOCK-RESET-TO-ZERO":
            next_clocks[update["clock"]] = Interval(Fraction(0), Fraction(0), True, True)
        else:
            next_store[update["field"]] = update["value"]
    return FrontierEntry(
        hypothesis_id=entry.hypothesis_id,
        control_state_id=next_state,
        clocks=next_clocks,
        typed_store=next_store,
        path_length=entry.path_length + 1,
        history_provenance=entry.history_provenance,
        status=entry.status,
        model_identity=entry.model_identity,
    )


def _verify_root_record(
    context: ModelContext, record: ProvenanceRecord,
) -> tuple[KernelDiagnostic | None, FrontierEntry | None]:
    """Replay a root before a later update can hide an invalid initial state."""
    if (
        not isinstance(record.root_id, str) or not record.root_id
        or record.transition_id is not None or record.transition_identity is not None
        or record.transition is not None or record.delta is not None
        or record.pre_update_clocks or record.observations
    ):
        return KernelDiagnostic(
            "INVALID-PROVENANCE-SEMANTICS", "root record has non-root transition or time fields",
        ), None
    try:
        root = _replay_entry_from_result_identity(record.result_identity, context, expected_path_length=0)
    except (AttributeError, KeyError, TypeError, ValueError):
        return KernelDiagnostic(
            "INVALID-PROVENANCE-SEMANTICS", "root record is outside the verified model domain",
        ), None
    return None, root


def _verify_step_record(
    context: ModelContext, parent: FrontierEntry, record: ProvenanceRecord,
) -> tuple[KernelDiagnostic | None, FrontierEntry | None]:
    """Replay one compact record; a refreshed hash cannot bless false semantics."""
    if (
        record.transition is None or record.transition_id is None
        or record.transition_identity is None or record.delta is None
        or record.root_id is not None
    ):
        return KernelDiagnostic("INVALID-PROVENANCE-SEMANTICS", "step record is missing transition or time evidence"), None
    if record.transition_identity != sha256(repr(record.transition).encode("utf-8")).hexdigest():
        return KernelDiagnostic("INVALID-PROVENANCE-SEMANTICS", "step transition identity does not match its definition"), None
    try:
        transition = _transition_from_canonical(record.transition)
    except (TypeError, ValueError, KeyError):
        return KernelDiagnostic("INVALID-PROVENANCE-SEMANTICS", "step record has an unreadable transition"), None
    if transition["id"] != record.transition_id:
        return KernelDiagnostic("INVALID-PROVENANCE-SEMANTICS", "step transition ID does not match its definition"), None
    transition_error = _validate_transition(
        transition, set(context.state_ids), set(context.clock_ids), context.typed_domains,
    )
    if transition_error is not None:
        return KernelDiagnostic("INVALID-PROVENANCE-SEMANTICS", "step transition is outside the verified finite model"), None
    delta_error, delta = _normalize_delta(record.delta)
    if delta_error is not None or delta is None:
        return KernelDiagnostic("INVALID-PROVENANCE-SEMANTICS", "step time advance is invalid"), None
    try:
        observations = dict(record.observations)
    except (TypeError, ValueError):
        return KernelDiagnostic("INVALID-PROVENANCE-SEMANTICS", "step observation constraints are invalid"), None
    if len(observations) != len(record.observations):
        return KernelDiagnostic("INVALID-PROVENANCE-SEMANTICS", "step observation constraints duplicate a clock"), None
    observation_error = _validate_observation_constraints(observations, set(context.clock_ids))
    if observation_error is not None:
        return KernelDiagnostic("INVALID-PROVENANCE-SEMANTICS", "step observation constraints are outside the verified model"), None
    if transition["source"] != parent.control_state_id:
        return KernelDiagnostic("INVALID-PROVENANCE-SEMANTICS", "step source state does not match its parent"), None
    advanced = {name: interval.shifted(delta) for name, interval in parent.clocks.items()}
    guarded, guard_error = _apply_guard(
        parent.control_state_id, parent.typed_store, advanced, transition["guardAst"],
        set(context.clock_ids),
    )
    if guard_error is not None or guarded is None:
        return KernelDiagnostic("INVALID-PROVENANCE-SEMANTICS", "step guard has no feasible verified successor"), None
    guarded = dict(guarded)
    for clock, observation in observations.items():
        intersection = guarded[clock].intersect(observation)
        if intersection is None:
            return KernelDiagnostic("INVALID-PROVENANCE-SEMANTICS", "step observation has no feasible verified successor"), None
        guarded[clock] = intersection
    if tuple(sorted(guarded.items())) != record.pre_update_clocks:
        return KernelDiagnostic("INVALID-PROVENANCE-SEMANTICS", "step pre-update clock constraints do not replay"), None
    expected = _successor_after_updates(parent, transition, guarded)
    if _entry_result_identity(expected) != record.result_identity:
        return KernelDiagnostic("INVALID-PROVENANCE-SEMANTICS", "step result does not follow from its verified parent and transition"), None
    try:
        result = _replay_entry_from_result_identity(
            record.result_identity, context, expected_path_length=parent.path_length + 1,
        )
    except (AttributeError, KeyError, TypeError, ValueError):
        return KernelDiagnostic("INVALID-PROVENANCE-SEMANTICS", "step result is outside the verified model domain"), None
    if (
        result.hypothesis_id != parent.hypothesis_id
        or result.status != parent.status
        or result.model_identity != parent.model_identity
    ):
        return KernelDiagnostic("INVALID-PROVENANCE-SEMANTICS", "step changes protected frontier identity fields"), None
    return None, result


def _valid_entry(
    entry: FrontierEntry,
    state_ids: set[str],
    clock_ids: set[str],
    typed_domains: Mapping[str, set[Any]],
    diagnostics: list[KernelDiagnostic],
) -> bool:
    valid = True
    if not isinstance(entry.hypothesis_id, str) or not entry.hypothesis_id:
        diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "hypothesisId must be a stable nonempty ID")); valid = False
    if entry.control_state_id not in state_ids:
        diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "frontier control state is undeclared")); valid = False
    if not isinstance(entry.clocks, Mapping) or set(entry.clocks) != clock_ids:
        diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "frontier clocks must exactly match declared clock IDs")); valid = False
    elif any(not _valid_interval(value) for value in entry.clocks.values()):
        diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "frontier clock constraints must be exact intervals")); valid = False
    if not isinstance(entry.typed_store, Mapping):
        diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "frontier typedStore must be a mapping")); valid = False
    for field, value in entry.typed_store.items() if isinstance(entry.typed_store, Mapping) else ():
        if field not in typed_domains or not _domain_contains(typed_domains[field], value):
            diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "frontier typedStore is outside the declared domain")); valid = False
    if isinstance(entry.typed_store, Mapping) and set(entry.typed_store) != set(typed_domains):
        diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "frontier typedStore must contain every declared field")); valid = False
    if not isinstance(entry.path_length, int) or isinstance(entry.path_length, bool) or entry.path_length < 0:
        diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "pathLength must be a nonnegative integer")); valid = False
    if not isinstance(entry.history_provenance, tuple) or not entry.history_provenance or any(not isinstance(item, str) for item in entry.history_provenance):
        diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "history provenance must be immutable")); valid = False
    if entry.status not in {"KNOWN", "CONSERVATIVE-UNKNOWN"}:
        diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "frontier status is not declared")); valid = False
    if not isinstance(entry.model_identity, str) or len(entry.model_identity) != 64:
        diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "frontier model identity is not bound")); valid = False
    return valid


def _validate_model_domain(
    state_ids: object, clock_ids: object, typed_domains: object,
) -> KernelDiagnostic | None:
    if not isinstance(state_ids, set) or not state_ids or any(not isinstance(value, str) or not value for value in state_ids):
        return KernelDiagnostic("INVALID-MODEL-DOMAIN", "state IDs must be a nonempty finite string set")
    if not isinstance(clock_ids, set) or any(not isinstance(value, str) or not value for value in clock_ids):
        return KernelDiagnostic("INVALID-MODEL-DOMAIN", "clock IDs must be a finite string set")
    if not isinstance(typed_domains, Mapping) or not typed_domains:
        return KernelDiagnostic("INVALID-MODEL-DOMAIN", "typed domains must be a nonempty mapping")
    for field, domain in typed_domains.items():
        if not isinstance(field, str) or not field or not isinstance(domain, (set, frozenset)) or not domain:
            return KernelDiagnostic("INVALID-MODEL-DOMAIN", "each typed domain must be a nonempty finite set")
        if any(not _scalar(value) for value in domain):
            return KernelDiagnostic("INVALID-MODEL-DOMAIN", "typed domains support declared finite scalar values only")
        if len({type(value) for value in domain}) != 1:
            return KernelDiagnostic("INVALID-MODEL-DOMAIN", "a typed domain may not mix scalar runtime types")
    return None


def _valid_merge_entry(value: object, context: ModelContext) -> bool:
    """Validate a public merge operand without assuming a prior propagation."""
    if not isinstance(value, FrontierEntry):
        return False
    if value.model_identity != context.identity:
        return False
    diagnostics: list[KernelDiagnostic] = []
    return _valid_entry(
        value, set(context.state_ids), set(context.clock_ids), context.typed_domains,
        diagnostics,
    )


def _authority_merge_key(entry: FrontierEntry) -> tuple[Any, ...]:
    """The five authority fields, separate from metadata-conflict policy."""
    return (
        entry.hypothesis_id,
        entry.control_state_id,
        tuple(sorted((key, _interval_key(value)) for key, value in entry.clocks.items())),
        tuple(sorted((key, _typed_key(value)) for key, value in entry.typed_store.items())),
        entry.history_provenance,
    )


def _fraction(value: Any) -> Fraction:
    if not isinstance(value, Mapping):
        raise ValueError("rational must be an object")
    if set(value) != {"numerator", "positiveDenominator"}:
        raise ValueError("rational fields are not canonical")
    numerator, denominator = value.get("numerator"), value.get("positiveDenominator")
    if not isinstance(numerator, int) or not isinstance(denominator, int) or isinstance(numerator, bool) or isinstance(denominator, bool) or denominator <= 0:
        raise ValueError("invalid rational fields")
    fraction = Fraction(numerator, denominator)
    if fraction.numerator != numerator or fraction.denominator != denominator:
        raise ValueError("rational is not canonical")
    return fraction


def _fraction_mapping(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "positiveDenominator": value.denominator}


def _interval_key(value: Interval) -> tuple[Any, ...]:
    return (value.lower, value.upper, value.lower_closed, value.upper_closed)


def _typed_key(value: object) -> tuple[str, object]:
    """A type-preserving scalar identity (``True`` is never integer ``1``)."""
    return (type(value).__qualname__, value)


def _entry_result_identity(entry: FrontierEntry) -> tuple[Any, ...]:
    """The result portion recorded at each root/step, excluding trace links."""
    return (
        entry.hypothesis_id,
        entry.control_state_id,
        tuple(sorted((key, _interval_key(value)) for key, value in entry.clocks.items())),
        tuple(sorted((key, _typed_key(value)) for key, value in entry.typed_store.items())),
        entry.path_length,
        entry.status,
        entry.model_identity,
    )


def _result_identity_mapping(identity: tuple[Any, ...]) -> dict[str, Any]:
    """Expose the compact result identity without relying on Python repr()."""
    (
        hypothesis_id, control_state_id, clocks, typed_store, path_length,
        status, model_identity,
    ) = identity
    return {
        "hypothesisId": hypothesis_id,
        "controlStateId": control_state_id,
        "clockConstraints": {
            name: {
                "lower": _fraction_mapping(bounds[0]),
                "upper": _fraction_mapping(bounds[1]),
                "lowerClosed": bounds[2],
                "upperClosed": bounds[3],
            }
            for name, bounds in clocks
        },
        "typedStore": {
            name: _source_typed_value(value) for name, value in typed_store
        },
        "pathLength": path_length,
        "status": status,
        "modelIdentity": model_identity,
    }


def _source_typed_value(value: tuple[str, object]) -> dict[str, Any]:
    """Encode a finite scalar with its runtime type preserved."""
    type_name, scalar = value
    if isinstance(scalar, Fraction):
        encoded: object = _fraction_mapping(scalar)
    else:
        encoded = scalar
    return {"type": type_name, "value": encoded}


def _json_safe(value: Any) -> Any:
    """Encode internal exact scalars in the emitted source-record view."""
    if isinstance(value, Fraction):
        return {"type": "Fraction", "value": _fraction_mapping(value)}
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if value is None or isinstance(value, (str, int, bool)):
        return value
    raise ValueError("source record contains a non-serialisable value")


def _entry_from_result_identity(identity: tuple[Any, ...]) -> FrontierEntry:
    if not isinstance(identity, tuple) or len(identity) != 7:
        raise ValueError("invalid result identity")
    hypothesis_id, control_state_id, clocks, typed_store, path_length, status, model_identity = identity
    if not isinstance(clocks, tuple) or not isinstance(typed_store, tuple):
        raise ValueError("invalid result identity fields")
    clock_mapping: dict[str, Interval] = {}
    for name, bounds in clocks:
        if not isinstance(name, str) or not isinstance(bounds, tuple) or len(bounds) != 4:
            raise ValueError("invalid result clock")
        if name in clock_mapping:
            raise ValueError("duplicate result clock")
        lower, upper, lower_closed, upper_closed = bounds
        if (
            not isinstance(lower, Fraction) or not isinstance(upper, Fraction)
            or not isinstance(lower_closed, bool) or not isinstance(upper_closed, bool)
        ):
            raise ValueError("invalid result clock bounds")
        interval = Interval(lower, upper, lower_closed, upper_closed)
        if not _valid_interval(interval):
            raise ValueError("invalid result interval")
        clock_mapping[name] = interval
    store_mapping: dict[str, Any] = {}
    for name, typed_value in typed_store:
        if not isinstance(name, str) or not isinstance(typed_value, tuple) or len(typed_value) != 2:
            raise ValueError("invalid result typed store")
        if name in store_mapping:
            raise ValueError("duplicate result typed field")
        type_name, scalar = typed_value
        if not isinstance(type_name, str) or type(scalar).__qualname__ != type_name:
            raise ValueError("invalid result typed scalar")
        store_mapping[name] = scalar
    return FrontierEntry(
        hypothesis_id, control_state_id, clock_mapping, store_mapping, path_length,
        ("replay",), status, model_identity,
    )


def _replay_entry_from_result_identity(
    identity: tuple[Any, ...], context: ModelContext, *, expected_path_length: int,
) -> FrontierEntry:
    """Decode a source record only after enforcing the bound model contract."""
    entry = _entry_from_result_identity(identity)
    diagnostics: list[KernelDiagnostic] = []
    if not _valid_entry(
        entry, set(context.state_ids), set(context.clock_ids), context.typed_domains, diagnostics,
    ):
        raise ValueError("replayed entry is outside the verified model domain")
    if entry.model_identity != context.identity:
        raise ValueError("replayed entry has a different model identity")
    if entry.path_length != expected_path_length:
        raise ValueError("replayed entry has an invalid path length")
    return entry


def _record_fields(record: ProvenanceRecord) -> dict[str, Any]:
    """Return all record fields other than its content address."""
    return {
        "kind": record.kind,
        "context_identity": record.context_identity,
        "parent_reference": record.parent_reference,
        "root_id": record.root_id,
        "transition_id": record.transition_id,
        "transition_identity": record.transition_identity,
        "transition": record.transition,
        "delta": record.delta,
        "pre_update_clocks": record.pre_update_clocks,
        "observations": record.observations,
        "result_identity": record.result_identity,
    }


def _source_record_shape_error(record: object) -> KernelDiagnostic | None:
    """Reject malformed stored payloads before canonical hashing or replay.

    ProvenanceStore is intentionally inspectable for evidence export, so this
    guard treats a damaged in-process record as untrusted input.  It checks
    only the safely inspectable carrier shape here; root/step semantics and
    model-domain membership remain the replay checks below.
    """
    if not isinstance(record, ProvenanceRecord):
        return KernelDiagnostic("MALFORMED-PROVENANCE-RECORD", "stored source record has an invalid carrier type")
    if not isinstance(record.reference, str) or record.kind not in {"ROOT", "STEP"}:
        return KernelDiagnostic("MALFORMED-PROVENANCE-RECORD", "stored source record has an invalid identity or kind")
    if not isinstance(record.context_identity, str):
        return KernelDiagnostic("MALFORMED-PROVENANCE-RECORD", "stored source record has an invalid context identity")
    if record.parent_reference is not None and not isinstance(record.parent_reference, str):
        return KernelDiagnostic("MALFORMED-PROVENANCE-RECORD", "stored source record has an invalid parent reference")
    if record.root_id is not None and not isinstance(record.root_id, str):
        return KernelDiagnostic("MALFORMED-PROVENANCE-RECORD", "stored source record has an invalid root ID")
    if record.transition_id is not None and not isinstance(record.transition_id, str):
        return KernelDiagnostic("MALFORMED-PROVENANCE-RECORD", "stored source record has an invalid transition ID")
    if record.transition_identity is not None and not isinstance(record.transition_identity, str):
        return KernelDiagnostic("MALFORMED-PROVENANCE-RECORD", "stored source record has an invalid transition identity")
    if record.transition is not None and not isinstance(record.transition, tuple):
        return KernelDiagnostic("MALFORMED-PROVENANCE-RECORD", "stored source record has an invalid transition payload")
    if record.delta is not None and not isinstance(record.delta, Fraction):
        return KernelDiagnostic("MALFORMED-PROVENANCE-RECORD", "stored source record has an invalid time delta")
    if not isinstance(record.result_identity, tuple):
        return KernelDiagnostic("MALFORMED-PROVENANCE-RECORD", "stored source record has an invalid result payload")
    for label, constraints in (
        ("pre-update clocks", record.pre_update_clocks),
        ("observations", record.observations),
    ):
        if not isinstance(constraints, tuple):
            return KernelDiagnostic("MALFORMED-PROVENANCE-RECORD", f"stored source record has invalid {label}")
        for item in constraints:
            if (
                not isinstance(item, tuple) or len(item) != 2
                or not isinstance(item[0], str) or not _valid_interval(item[1])
            ):
                return KernelDiagnostic("MALFORMED-PROVENANCE-RECORD", f"stored source record has invalid {label}")
    return None


def _record_reference(record: ProvenanceRecord) -> str:
    """Calculate the stable address for a compact provenance payload."""
    payload = repr((
        record.kind, record.context_identity, record.parent_reference,
        record.root_id, record.transition_id, record.transition_identity,
        record.transition, record.delta,
        tuple((name, _interval_key(interval)) for name, interval in record.pre_update_clocks),
        tuple((name, _interval_key(interval)) for name, interval in record.observations),
        record.result_identity,
    )).encode("utf-8")
    return f"{record.kind.lower()}:" + sha256(payload).hexdigest()


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str) and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _safe_contract_path(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("contract path must be a nonempty repository-relative path")
    normalized = value.replace("\\", "/")
    posix = PurePosixPath(normalized)
    windows = PureWindowsPath(value)
    if posix.is_absolute() or windows.is_absolute() or windows.drive or ".." in posix.parts:
        raise ValueError("contract path is not a safe repository-relative path")
    return posix.as_posix()


def _verified_snapshot(value: object) -> bool:
    if not isinstance(value, ContractSnapshot) or value._verification_token is not _CONTRACT_SNAPSHOT_TOKEN:
        return False
    try:
        path = _safe_contract_path(value.contract_path)
    except ValueError:
        return False
    return (
        path == value.contract_path
        and isinstance(value.contract_commit, str)
        and len(value.contract_commit) == 40
        and all(character in "0123456789abcdef" for character in value.contract_commit)
        and _is_sha256(value.contract_blob_sha256)
        and isinstance(value._content, bytes)
        and sha256(value._content).hexdigest() == value.contract_blob_sha256
    )


def _finite_contract_vocabulary(contract: Mapping[str, Any]) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    """Validate the exact AR-FINITE compatibility projection this runtime consumes.

    Git identity says which controlled object was read.  This function answers
    the separate question of whether that object's finite-kernel boundary is
    one this deliberately bounded implementation can execute.  It therefore
    checks the declared AST/update/merge vocabulary *and* the result, limit and
    one-clock projection contracts, without treating unrelated prose or other
    interface mappings as executable runtime input.
    """
    refinements = contract.get("algorithmRefinements")
    if not isinstance(refinements, list):
        raise ValueError("controlled contract is missing algorithmRefinements")
    matches = [item for item in refinements if isinstance(item, Mapping) and item.get("id") == "AR-FINITE"]
    if len(matches) != 1:
        raise ValueError("controlled contract must contain exactly one AR-FINITE refinement")
    finite = matches[0].get("finiteKernelContract")
    if not isinstance(finite, Mapping):
        raise ValueError("AR-FINITE is missing finiteKernelContract")
    guard_tags, update_tags, merge_fields = (
        finite.get("guardSyntax"), finite.get("updateSyntax"), finite.get("mergeKey"),
    )
    internal_results = finite.get("internalResults")
    if (
        not isinstance(guard_tags, list) or tuple(guard_tags) != _SUPPORTED_GUARD_TAGS
        or not isinstance(update_tags, list) or tuple(update_tags) != _SUPPORTED_UPDATE_TAGS
        or not isinstance(merge_fields, list) or tuple(merge_fields) != _AUTHORITY_MERGE_FIELDS
        or not isinstance(internal_results, list) or tuple(internal_results) != _SUPPORTED_INTERNAL_RESULTS
        or finite.get("limitBehavior") != _SUPPORTED_LIMIT_BEHAVIOR
        or not _supported_result_mapping(finite.get("resultMapping"))
        or not _supported_clock_projection(finite.get("modelInstanceSchema"))
    ):
        raise ValueError("AR-FINITE vocabulary is unsupported by this finite runtime")
    return tuple(guard_tags), tuple(update_tags), tuple(merge_fields)


def _supported_result_mapping(value: object) -> bool:
    """Check only the finite kernel's declared interface-return projection."""
    if not isinstance(value, Mapping):
        return False
    for interface_id, expected in _SUPPORTED_RESULT_MAPPING.items():
        candidate = value.get(interface_id)
        if not isinstance(candidate, Mapping) or set(candidate) != {"success", "failure"}:
            return False
        if (
            not isinstance(candidate["success"], list) or not isinstance(candidate["failure"], list)
            or tuple(candidate["success"]) != expected["success"]
            or tuple(candidate["failure"]) != expected["failure"]
        ):
            return False
    return True


def _supported_clock_projection(value: object) -> bool:
    """Check the single-clock rational projection that the runtime implements."""
    if not isinstance(value, Mapping):
        return False
    clock = value.get("clockConstraint")
    if not isinstance(clock, Mapping):
        return False
    normalized = dict(clock)
    if isinstance(normalized.get("feasibility"), list):
        normalized["feasibility"] = tuple(normalized["feasibility"])
    return normalized == _SUPPORTED_CLOCK_CONSTRAINT


def _model_context_identity(
    contract_commit: str, contract_path: str, contract_blob_sha256: str,
    model_sha256: str, projection_clock: str,
) -> str:
    return sha256((
        contract_commit + "\0" + contract_path + "\0" + contract_blob_sha256
        + "\0" + model_sha256 + "\0" + projection_clock
    ).encode("utf-8")).hexdigest()


def _context_binding_digest(context: ModelContext) -> str:
    """Bind every public context field to the factory-issued context token."""
    payload = repr((
        context.contract_commit, context.contract_path, context.contract_blob_sha256,
        context.model_sha256, context.projection_clock,
        tuple(sorted(context.state_ids)), tuple(sorted(context.clock_ids)),
        tuple(
            (name, tuple(sorted((_typed_key(value) for value in domain), key=repr)))
            for name, domain in sorted(context.typed_domains.items())
        ),
        context.supported_guard_tags, context.supported_update_tags,
        context.authority_merge_fields,
        context.identity,
    )).encode("utf-8")
    return sha256(payload).hexdigest()


def _verified_context(value: object) -> bool:
    """Reject direct/fabricated contexts before they can seed a frontier."""
    if not isinstance(value, ModelContext) or value._verification_token is not _MODEL_CONTEXT_TOKEN:
        return False
    if not (
        _is_sha256(value.contract_blob_sha256)
        and _is_sha256(value.model_sha256)
        and _is_sha256(value.identity)
        and _is_sha256(value._binding_sha256)
        and isinstance(value.contract_commit, str)
        and len(value.contract_commit) == 40
        and all(character in "0123456789abcdef" for character in value.contract_commit)
        and isinstance(value.contract_path, str)
        and value.contract_path
        and not value.contract_path.startswith(("/", "\\"))
        and ".." not in value.contract_path.replace("\\", "/").split("/")
        and isinstance(value.projection_clock, str)
        and value.supported_guard_tags == _SUPPORTED_GUARD_TAGS
        and value.supported_update_tags == _SUPPORTED_UPDATE_TAGS
        and value.authority_merge_fields == _AUTHORITY_MERGE_FIELDS
    ):
        return False
    try:
        domain_error = _validate_model_domain(
            set(value.state_ids), set(value.clock_ids),
            {name: set(domain) for name, domain in value.typed_domains.items()},
        )
    except (AttributeError, TypeError, ValueError):
        return False
    expected_identity = _model_context_identity(
        value.contract_commit, value.contract_path, value.contract_blob_sha256,
        value.model_sha256, value.projection_clock,
    )
    return (
        domain_error is None
        and value.projection_clock in value.clock_ids
        and len(value.clock_ids) == 1
        and value.identity == expected_identity
        and value._binding_sha256 == _context_binding_digest(value)
    )


def _canonical_model(model: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stateIds": sorted(model["stateIds"]),
        "clockIds": sorted(model["clockIds"]),
        "typedDomains": {
            key: sorted((_canonical_scalar(value) for value in domain), key=repr)
            for key, domain in sorted(model["typedDomains"].items())
        },
    }


def _canonical_scalar(value: object) -> dict[str, Any]:
    """Type-preserving, JSON-safe finite-domain scalar representation."""
    if not _scalar(value):
        raise ValueError("finite model domain contains an unsupported scalar")
    if isinstance(value, Fraction):
        encoded: object = _fraction_mapping(value)
    else:
        encoded = value
    return {"type": type(value).__qualname__, "value": encoded}


def _valid_limit(value: object, *, minimum: int) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= minimum


def _domain_contains(domain: set[Any], value: object) -> bool:
    try:
        return any(type(value) is type(candidate) and value == candidate for candidate in domain)
    except TypeError:
        return False


def _scalar(value: object) -> bool:
    return isinstance(value, (str, int, Fraction, bool)) and not isinstance(value, float)


def _normalize_delta(value: object) -> tuple[KernelDiagnostic | None, Fraction | None]:
    if value is None:
        return None, Fraction(0)
    if isinstance(value, int) and not isinstance(value, bool):
        value = Fraction(value)
    if not isinstance(value, Fraction):
        return KernelDiagnostic("INVALID-DELTA", "time advance must be an exact integer or Fraction"), None
    if value < 0:
        return KernelDiagnostic("INVALID-DELTA", "time advance must be nonnegative"), None
    return None, value


def _valid_interval(value: object) -> bool:
    return (
        isinstance(value, Interval)
        and isinstance(value.lower, Fraction)
        and isinstance(value.upper, Fraction)
        and isinstance(value.lower_closed, bool)
        and isinstance(value.upper_closed, bool)
        and not (value.lower > value.upper or (value.lower == value.upper and not (value.lower_closed and value.upper_closed)))
    )


def _canonical_transition(transition: Mapping[str, Any]) -> tuple[Any, ...]:
    return (
        transition["id"], transition["source"], transition["target"],
        _canonical_guard(transition["guardAst"]),
        tuple(sorted(_canonical_update(update) for update in transition["simultaneousUpdates"])),
    )


def _transition_from_canonical(value: tuple[Any, ...]) -> dict[str, Any]:
    if not isinstance(value, tuple) or len(value) != 5:
        raise ValueError("invalid canonical transition")
    identifier, source, target, guard, updates = value
    if not all(isinstance(item, str) for item in (identifier, source, target)) or not isinstance(updates, tuple):
        raise ValueError("invalid canonical transition header")
    return {
        "id": identifier,
        "source": source,
        "target": target,
        "guardAst": _guard_from_canonical(guard),
        "simultaneousUpdates": [_update_from_canonical(update) for update in updates],
    }


def _canonical_guard(ast: Mapping[str, Any]) -> tuple[Any, ...]:
    tag = ast["tag"]
    if tag == "TRUE":
        return (tag,)
    if tag == "AND":
        return (tag, tuple(sorted(_canonical_guard(child) for child in ast["operands"])))
    if tag == "STATE-EQUALS":
        return (tag, ast["state"])
    if tag == "TYPED-FIELD-EQUALS":
        return (tag, ast["field"], ast["value"])
    interval = Interval.from_mapping(ast["interval"])
    return (tag, ast["clock"], _interval_key(interval))


def _guard_from_canonical(value: Any) -> dict[str, Any]:
    if not isinstance(value, tuple) or not value or not isinstance(value[0], str):
        raise ValueError("invalid canonical guard")
    tag = value[0]
    if tag == "TRUE" and len(value) == 1:
        return {"tag": tag}
    if tag == "AND" and len(value) == 2 and isinstance(value[1], tuple):
        return {"tag": tag, "operands": [_guard_from_canonical(child) for child in value[1]]}
    if tag == "STATE-EQUALS" and len(value) == 2 and isinstance(value[1], str):
        return {"tag": tag, "state": value[1]}
    if tag == "TYPED-FIELD-EQUALS" and len(value) == 3 and isinstance(value[1], str):
        return {"tag": tag, "field": value[1], "value": value[2]}
    if tag == "RATIONAL-INTERVAL-CONTAINS" and len(value) == 3 and isinstance(value[1], str):
        bounds = value[2]
        if not isinstance(bounds, tuple) or len(bounds) != 4:
            raise ValueError("invalid canonical interval guard")
        lower, upper, lower_closed, upper_closed = bounds
        if not isinstance(lower, Fraction) or not isinstance(upper, Fraction):
            raise ValueError("invalid canonical interval bounds")
        return {
            "tag": tag,
            "clock": value[1],
            "interval": {
                "lower": _fraction_mapping(lower),
                "upper": _fraction_mapping(upper),
                "lowerClosed": lower_closed,
                "upperClosed": upper_closed,
            },
        }
    raise ValueError("invalid canonical guard")


def _canonical_update(update: Mapping[str, Any]) -> tuple[Any, ...]:
    tag = update["tag"]
    if tag == "STATE-ASSIGN":
        return (tag, update["state"])
    if tag == "CLOCK-RESET-TO-ZERO":
        return (tag, update["clock"])
    return (tag, update["field"], update["value"])


def _update_from_canonical(value: Any) -> dict[str, Any]:
    if not isinstance(value, tuple) or not value or not isinstance(value[0], str):
        raise ValueError("invalid canonical update")
    tag = value[0]
    if tag == "STATE-ASSIGN" and len(value) == 2 and isinstance(value[1], str):
        return {"tag": tag, "state": value[1]}
    if tag == "CLOCK-RESET-TO-ZERO" and len(value) == 2 and isinstance(value[1], str):
        return {"tag": tag, "clock": value[1]}
    if tag == "TYPED-FIELD-ASSIGN" and len(value) == 3 and isinstance(value[1], str):
        return {"tag": tag, "field": value[1], "value": value[2]}
    raise ValueError("invalid canonical update")
