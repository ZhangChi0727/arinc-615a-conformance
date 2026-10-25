"""Finite public model parsing and prediction for the reference session.

The model declares per-hypothesis *observable emissions*.  Prediction groups
those public emissions after actual finite-kernel propagation.  The synthetic
environment holds a separate private state and is never asked for a candidate
set or a predicted class.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from hashlib import sha256
import json
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from .kernel import (
    FrontierEntry,
    Interval,
    KernelDiagnostic,
    ModelContext,
    initial_entry,
    propagate_transition,
)


_ACTION_KINDS = frozenset({"TEST", "PREP", "RECOVER"})
_FINITE_SESSION_MODEL_TOKEN = object()


def _canonical_digest(value: Mapping[str, Any]) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8"),
    ).hexdigest()


@dataclass(frozen=True)
class SyntheticAction:
    """One public action declared by a finite reference model."""

    action_id: str
    kind: str
    cost: int
    detail_charges: Mapping[str, int]
    enabled_summaries: frozenset[str]
    transition_json: str
    observable_by_hypothesis: Mapping[str, tuple[str, ...]]
    measurement_ticks_by_hypothesis: Mapping[str, Fraction]
    declared_target: str | None = None
    recover_when_unknown: bool = False

    def transition_for_kernel(self) -> Mapping[str, Any]:
        """Return a fresh mutable decoding of this action's frozen AST.

        The finite kernel consumes ordinary mapping/list JSON values.  Keeping
        only canonical JSON inside the action makes it impossible for a caller
        to mutate the nested AST that was used to calculate ``identity``.
        """

        value = json.loads(self.transition_json)
        if not isinstance(value, Mapping):  # defensive; construction verifies it
            raise ValueError("frozen finite-session transition is invalid")
        return value

    def projected_cost(self) -> Mapping[str, int]:
        """Return the declared four-component projection without recharging."""

        return MappingProxyType(
            {
                "acquisition": self.detail_charges["acquisition"],
                "computation": self.detail_charges["computation"],
                "preparation": self.detail_charges["preparation"] + self.detail_charges["recovery"],
                "retry": self.detail_charges["retry"],
            },
        )


@dataclass(frozen=True)
class PredictionClass:
    """A nonempty current observation class, produced by model calculation."""

    action_id: str
    observable: str
    hypotheses: frozenset[str]
    successors: Mapping[str, tuple[FrontierEntry, ...]]
    conservative_hypotheses: frozenset[str] = frozenset()
    measurement_windows: Mapping[str, Interval] = field(
        default_factory=lambda: MappingProxyType({}),
    )


@dataclass(frozen=True)
class MeasurementUncertainty:
    """Finite shared timing uncertainty used by prediction and interpretation."""

    uncertainty_id: str
    clock_id: str
    time_unit: str
    maximum_error: Fraction
    identity: str

    def window(self, tick: Fraction) -> Interval:
        return Interval(
            tick - self.maximum_error,
            tick + self.maximum_error,
            True,
            True,
        )


@dataclass(frozen=True)
class ActionPrediction:
    """Finite prediction for exactly one action and one history version."""

    action_id: str
    classes: tuple[PredictionClass, ...]
    diagnostics: tuple[KernelDiagnostic, ...]

    @property
    def has_distinguishing_value(self) -> bool:
        universe = frozenset().union(*(value.hypotheses for value in self.classes))
        return any(0 < len(value.hypotheses) < len(universe) for value in self.classes)


@dataclass(frozen=True)
class SummaryOnlySuccessor:
    """Whole-history successor of one confirmed result without ``I_z``.

    A summary confirmation establishes a public successor summary, but it is
    not an observation class.  The action has still been executed, so its
    declared transition is applied independently to every retained model path.
    A path which cannot be propagated is retained as a named conservative
    continuation rather than silently deleting its hypothesis or pretending
    that the predecessor state was a known successor.
    """

    action_id: str
    successors: Mapping[str, tuple[FrontierEntry, ...]]
    conservative_hypotheses: frozenset[str]
    diagnostics: tuple[KernelDiagnostic, ...]


@dataclass(frozen=True)
class FiniteSessionModel:
    """Validated public model data for the bounded reference session."""

    context: ModelContext
    actions: Mapping[str, SyntheticAction]
    initial_frontiers: Mapping[str, FrontierEntry]
    path_limit: int
    frontier_limit: int
    hypothesis_limit: int
    action_limit: int
    observation_class_limit: int
    identity: str
    uncertainty: MeasurementUncertainty
    _source_json: bytes = field(default=b"", init=False, compare=False, repr=False)
    _binding_sha256: str = field(default="", init=False, compare=False, repr=False)
    _verification_token: object | None = field(default=None, init=False, compare=False, repr=False)

    @property
    def uncertainty_identity(self) -> str:
        return self.uncertainty.uncertainty_id

    @property
    def uncertainty_digest(self) -> str:
        return self.uncertainty.identity

    @classmethod
    def from_mapping(
        cls, *, context: ModelContext, value: Mapping[str, Any],
    ) -> "FiniteSessionModel":
        if not isinstance(value, Mapping):
            raise ValueError("finite session model must be an object")
        # The fixture/model is a JSON contract.  Detach it before parsing so a
        # caller cannot change a nested guard/update after this construction
        # while retaining the original model identity.
        value = _json_clone(value)
        required = {
            "model", "hypotheses", "actions", "limits", "uncertainty",
        }
        if set(value) != required:
            raise ValueError("finite session model uses unknown or missing fields")
        model = value["model"]
        if not isinstance(model, Mapping):
            raise ValueError("finite session model declaration is invalid")
        expected_model = {
            "stateIds": sorted(context.state_ids),
            "clockIds": sorted(context.clock_ids),
            "typedDomains": {
                key: sorted(domain) for key, domain in sorted(context.typed_domains.items())
            },
        }
        if _canonical_model(model) != expected_model:
            raise ValueError("finite session model differs from its verified context")
        hypotheses = value["hypotheses"]
        actions = value["actions"]
        limits = value["limits"]
        uncertainty = _parse_uncertainty(value["uncertainty"], context.projection_clock)
        if not isinstance(hypotheses, list) or not hypotheses:
            raise ValueError("finite session model needs at least one hypothesis")
        if not isinstance(actions, list) or not actions:
            raise ValueError("finite session model needs at least one action")
        if not isinstance(limits, Mapping) or set(limits) != {
            "pathLength", "frontierStates", "hypotheses", "actions", "observationClasses",
        }:
            raise ValueError("finite session model limits are invalid")
        path_limit = _positive_int(limits["pathLength"], "path length")
        frontier_limit = _positive_int(limits["frontierStates"], "frontier limit")
        hypothesis_limit = _positive_int(limits["hypotheses"], "hypothesis limit")
        action_limit = _positive_int(limits["actions"], "action limit")
        observation_class_limit = _positive_int(limits["observationClasses"], "observation-class limit")
        hypothesis_ids: list[str] = []
        frontiers: dict[str, FrontierEntry] = {}
        for item in hypotheses:
            identifier, entry = _initial_frontier(context, item)
            if identifier in frontiers:
                raise ValueError("finite session model has duplicate hypothesis IDs")
            hypothesis_ids.append(identifier)
            frontiers[identifier] = entry
        parsed_actions: dict[str, SyntheticAction] = {}
        for item in actions:
            action = _parse_action(item, frozenset(hypothesis_ids))
            if action.action_id in parsed_actions:
                raise ValueError("finite session model has duplicate action IDs")
            parsed_actions[action.action_id] = action
        if len(parsed_actions) > action_limit:
            raise ValueError("finite session action count exceeds its declared bound")
        if len(frontiers) > hypothesis_limit:
            raise ValueError("finite session hypothesis count exceeds its declared bound")
        identity = _canonical_digest(value)
        result = cls(
            context=context,
            actions=MappingProxyType(parsed_actions),
            initial_frontiers=MappingProxyType(frontiers),
            path_limit=path_limit,
            frontier_limit=frontier_limit,
            hypothesis_limit=hypothesis_limit,
            action_limit=action_limit,
            observation_class_limit=observation_class_limit,
            identity=identity,
            uncertainty=uncertainty,
        )
        # Keep the exact canonical JSON that produced ``identity`` and bind
        # every finite value actually consumed by S3--S9.  Frozen dataclasses
        # can still be rewritten through ``object.__setattr__`` by an adapter
        # retaining a caller alias, so a digest of the original JSON alone is
        # not enough to establish a construction-time authority boundary.
        source_json = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
        object.__setattr__(result, "_source_json", source_json)
        object.__setattr__(result, "_binding_sha256", _finite_model_binding_digest(result))
        object.__setattr__(result, "_verification_token", _FINITE_SESSION_MODEL_TOKEN)
        return result

    def predict(
        self, *, hypotheses: frozenset[str], frontiers: Mapping[str, FrontierEntry | tuple[FrontierEntry, ...]],
        status_by_hypothesis: Mapping[str, str], action_id: str,
    ) -> ActionPrediction:
        """Compute current classes by propagating each current public path."""

        action = self.actions.get(action_id)
        if action is None:
            return ActionPrediction(
                action_id, (), (KernelDiagnostic("UNKNOWN-ACTION", "action is not in the declared finite model"),),
            )
        if not hypotheses or not hypotheses <= set(frontiers):
            return ActionPrediction(
                action_id, (), (KernelDiagnostic("INVALID-HISTORY", "current hypotheses/frontiers are inconsistent"),),
            )
        grouped: dict[str, dict[str, tuple[FrontierEntry, ...]]] = {}
        measurement_windows: dict[str, dict[str, Interval]] = {}
        conservative: dict[str, tuple[FrontierEntry, ...]] = {}
        diagnostics: list[KernelDiagnostic] = []
        for hypothesis in sorted(hypotheses):
            try:
                paths = _frontier_paths(frontiers[hypothesis])
            except (KeyError, TypeError, ValueError) as exc:
                return ActionPrediction(
                    action_id,
                    (),
                    tuple(diagnostics + [KernelDiagnostic("INVALID-HISTORY", str(exc) or type(exc).__name__)]),
                )
            # The S0 member-status map may legitimately omit a member.  A
            # conservative status carried by any retained public frontier is
            # nevertheless authoritative for prediction: a normal observation
            # cannot exclude that unresolved member merely because S0 did not
            # duplicate its status in the optional map.  This is a membership
            # rule, *not* permission to skip its finite transition.  An
            # admitted non-self-loop TEST still advances every retained path
            # (including its state, clocks, store and provenance); only the
            # resulting member remains in every completed visible class.
            member_conservative = (
                status_by_hypothesis.get(hypothesis) == "CONSERVATIVE-UNKNOWN"
                or any(path.status == "CONSERVATIVE-UNKNOWN" for path in paths)
            )
            feasible: list[FrontierEntry] = []
            retained: list[FrontierEntry] = []
            for path in paths:
                result = propagate_transition(
                    path,
                    action.transition_for_kernel(),
                    state_ids=set(self.context.state_ids),
                    clock_ids=set(self.context.clock_ids),
                    typed_domains={key: set(domain) for key, domain in self.context.typed_domains.items()},
                    context=self.context,
                    path_limit=self.path_limit,
                    frontier_limit=self.frontier_limit,
                )
                diagnostics.extend(result.diagnostics)
                if result.kind == "FEASIBLE":
                    feasible.extend(result.entries)
                elif result.kind != "INFEASIBLE" or member_conservative:
                    # The incoming path, not a fabricated observation class,
                    # remains the conservative witness for a calculation that
                    # did not prove compatibility or incompatibility.  A
                    # member that was already conservative also retains an
                    # otherwise infeasible source path: its historic unknown
                    # effect cannot be converted into a proved exclusion.
                    if result.kind == "INFEASIBLE":
                        diagnostics.append(KernelDiagnostic(
                            "CONSERVATIVE-MEMBER-PATH",
                            "an existing conservative member retains an infeasible source witness",
                        ))
                    retained.extend(result.entries or (path,))

            if member_conservative:
                try:
                    conservative[hypothesis] = _bounded_paths(
                        feasible + retained, self.frontier_limit,
                    )
                except ValueError as exc:
                    diagnostics.append(KernelDiagnostic("FRONTIER-BUNDLE-LIMIT", str(exc)))
                    # Do not erase a compatible conservative member merely
                    # because all exact successors cannot fit the declared
                    # finite bundle.  Withhold a visible class for this
                    # member and retain its verified source witness.
                    conservative[hypothesis] = paths
                # A conservative member never supplies a completed normal
                # observation class of its own.  If another completed member
                # supplies one below, this calculated continuation is injected
                # into it; if none does, the named prediction gap remains.
                continue

            if feasible:
                try:
                    successors = _bounded_paths(feasible + retained, self.frontier_limit)
                except ValueError as exc:
                    diagnostics.append(KernelDiagnostic("FRONTIER-BUNDLE-LIMIT", str(exc)))
                    # A finite bound cannot erase paths merely because their
                    # successor bundle would be too large to retain.  Keep
                    # the source bundle as a conservative continuation and
                    # withhold any unproved visible class for this member.
                    conservative[hypothesis] = paths
                    continue
                for observable in action.observable_by_hypothesis[hypothesis]:
                    grouped.setdefault(observable, {})[hypothesis] = successors
                    measurement_windows.setdefault(observable, {})[hypothesis] = self.uncertainty.window(
                        action.measurement_ticks_by_hypothesis[hypothesis],
                    )
            if retained:
                # A bounded/unsupported computation keeps its hypothesis in a
                # conservative continuation.  It is included in every normal
                # class below, so a visible normal observation cannot exclude
                # a hypothesis whose applicable computation was not completed.
                conservative[hypothesis] = _bounded_paths(retained, self.frontier_limit)
        if conservative:
            if grouped:
                for successors in grouped.values():
                    for hypothesis, paths in conservative.items():
                        successors[hypothesis] = _bounded_paths(
                            list(successors.get(hypothesis, ())) + list(paths), self.frontier_limit,
                        )
            else:
                # No completed calculation produced a visible class.  Keeping
                # a synthetic ``unknown`` class here would make an incomplete
                # calculation look like an admissible, distinguishing TEST
                # outcome.  The coordinator must instead treat this as the
                # named prediction gap and may consider an admitted PREP.
                return ActionPrediction(
                    action_id,
                    (),
                    tuple(
                        diagnostics
                        + [
                            KernelDiagnostic(
                                "CONSERVATIVE-PREDICTION-GAP",
                                "no completed visible class exists; conservative hypotheses are retained",
                            ),
                        ]
                    ),
                )
        if len(grouped) > self.observation_class_limit:
            return ActionPrediction(
                action_id,
                (),
                tuple(diagnostics + [KernelDiagnostic("OBSERVATION-CLASS-LIMIT", "declared observation-class bound reached; TEST scoring is withheld")]),
            )
        classes = tuple(
            PredictionClass(
                action_id=action_id,
                observable=observable,
                hypotheses=frozenset(successors),
                successors=MappingProxyType(dict(successors)),
                conservative_hypotheses=frozenset(conservative),
                measurement_windows=MappingProxyType(dict(measurement_windows[observable])),
            )
            for observable, successors in sorted(grouped.items())
        )
        return ActionPrediction(action_id, classes, tuple(diagnostics))

    def summary_only_successors(
        self,
        *,
        hypotheses: frozenset[str],
        frontiers: Mapping[str, FrontierEntry | tuple[FrontierEntry, ...]],
        status_by_hypothesis: Mapping[str, str],
        action_id: str,
    ) -> SummaryOnlySuccessor:
        """Propagate an executed action without intersecting an observation class.

        ``predict`` is intentionally observation-class oriented: it groups
        paths by visible emissions and may withhold normal TEST scoring.  A
        confirmed summary-only Prep/Recover result is different.  It retains
        the current ``H`` while applying the admitted action's finite
        transition to every current path, preserving all applicable
        successors.  A bounded, unsupported, or infeasible path stays as a
        conservative source witness; this helper never manufactures a known
        successor from ``postSummary`` and never erases a member merely because
        no ``I_z`` was supplied.
        """

        action = self.actions.get(action_id)
        if action is None:
            return SummaryOnlySuccessor(
                action_id,
                MappingProxyType({}),
                frozenset(),
                (KernelDiagnostic("UNKNOWN-ACTION", "action is not in the declared finite model"),),
            )
        if not hypotheses or not hypotheses <= set(frontiers):
            return SummaryOnlySuccessor(
                action_id,
                MappingProxyType({}),
                frozenset(),
                (KernelDiagnostic("INVALID-HISTORY", "current hypotheses/frontiers are inconsistent"),),
            )

        successors: dict[str, tuple[FrontierEntry, ...]] = {}
        conservative: set[str] = set()
        diagnostics: list[KernelDiagnostic] = []
        for hypothesis in sorted(hypotheses):
            try:
                paths = _frontier_paths(frontiers[hypothesis])
            except (KeyError, TypeError, ValueError) as exc:
                return SummaryOnlySuccessor(
                    action_id,
                    MappingProxyType({}),
                    frozenset(),
                    tuple(diagnostics + [KernelDiagnostic("INVALID-HISTORY", str(exc) or type(exc).__name__)]),
                )

            # A previous S7 result is still a retained model path.  The
            # subsequently admitted action must therefore advance it just as
            # it advances a known member; otherwise a confirmed q0->q1
            # action could leave a conservative q0 member stale forever.  Its
            # status remains conservative, because this propagation does not
            # retroactively prove the earlier uncertain effect.
            # S0 is allowed to omit the member-status map.  That omission is
            # not a positive KNOWN assertion: a retained frontier can itself
            # carry the conservative status.  The committed result therefore
            # derives member conservatism from both representations, and later
            # also from the propagation result below.  Otherwise an S0 seed
            # with a genuine C-U path could be silently promoted merely
            # because its optional S0 status-map entry was absent.
            history_conservative = (
                status_by_hypothesis.get(hypothesis) == "CONSERVATIVE-UNKNOWN"
            )
            source_conservative = any(
                path.status == "CONSERVATIVE-UNKNOWN" for path in paths
            )
            already_conservative = history_conservative or source_conservative
            advanced: list[FrontierEntry] = []
            retained: list[FrontierEntry] = []
            unresolved = already_conservative
            for path in paths:
                result = propagate_transition(
                    path,
                    action.transition_for_kernel(),
                    state_ids=set(self.context.state_ids),
                    clock_ids=set(self.context.clock_ids),
                    typed_domains={key: set(domain) for key, domain in self.context.typed_domains.items()},
                    context=self.context,
                    path_limit=self.path_limit,
                    frontier_limit=self.frontier_limit,
                )
                diagnostics.extend(result.diagnostics)
                if result.kind == "FEASIBLE":
                    advanced.extend(result.entries)
                    continue

                # No summary-only observation may exclude a current member.
                # Preserve the finite source/result witness and make the
                # uncertainty explicit instead of retaining a stale KNOWN
                # predecessor or inventing a successor from the summary name.
                unresolved = True
                retained.extend(result.entries or (path,))
                diagnostics.append(KernelDiagnostic(
                    "SUMMARY-ONLY-CONSERVATIVE-PATH",
                    f"{result.kind} action propagation retained a conservative path for {hypothesis}",
                ))

            try:
                successors[hypothesis] = _bounded_paths(
                    advanced + retained,
                    self.frontier_limit,
                )
            except ValueError as exc:
                # The current source bundle has already passed the session
                # bound.  Retaining it is the only conservative finite result
                # when the attempted successor union would exceed that bound.
                successors[hypothesis] = paths
                unresolved = True
                diagnostics.append(KernelDiagnostic("SUMMARY-ONLY-FRONTIER-LIMIT", str(exc)))

            result_conservative = any(
                path.status == "CONSERVATIVE-UNKNOWN"
                for path in successors[hypothesis]
            )
            if unresolved or result_conservative:
                conservative.add(hypothesis)
                if already_conservative:
                    diagnostics.append(KernelDiagnostic(
                        "SUMMARY-ONLY-CONSERVATIVE-PATH",
                        f"existing conservative history propagated without promotion for {hypothesis}",
                    ))

        return SummaryOnlySuccessor(
            action_id,
            MappingProxyType(dict(successors)),
            frozenset(conservative),
            tuple(diagnostics),
        )


def verified_finite_session_model(value: object) -> bool:
    """Return whether a factory-issued finite model still matches its source.

    ``FiniteSessionModel`` is intentionally inspectable.  This check is the
    narrower authority boundary needed by the coordinator: it rejects a model
    whose action costs, AST, frontier, uncertainty, or limits were rewritten
    after ``from_mapping`` while its old public ``identity`` was retained.
    It is not a general object sandbox.
    """

    if not _verified_finite_model_source(value):
        return False
    assert isinstance(value, FiniteSessionModel)
    try:
        return (
            type(value._binding_sha256) is str
            and value._binding_sha256 == _finite_model_binding_digest(value)
        )
    except (AttributeError, KeyError, TypeError, ValueError, OverflowError):
        return False


def rebuild_verified_finite_session_model(value: object) -> FiniteSessionModel:
    """Rebuild an S0 model only from its factory-held canonical source JSON.

    This deliberately does *not* copy public ``actions`` or ``frontiers`` from
    the caller object after checking it.  A side-effecting mapping could change
    between such a check and a later copy.  The retained canonical JSON and a
    verified replay context instead provide one atomic finite authority source
    for the private session projection.
    """

    if not _verified_finite_model_source(value):
        raise ValueError("finite model source is not verified")
    assert isinstance(value, FiniteSessionModel)
    try:
        source = json.loads(value._source_json.decode("utf-8"))
        if not isinstance(source, Mapping):
            raise ValueError("finite model source root is invalid")
        context = value.context.read_only_replay_context()
        rebuilt = FiniteSessionModel.from_mapping(context=context, value=source)
    except (AttributeError, TypeError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        raise ValueError("finite model source is not verified") from exc
    if rebuilt.identity != value.identity:
        raise ValueError("finite model source identity is inconsistent")
    return rebuilt


def _verified_finite_model_source(value: object) -> bool:
    """Check the immutable factory source without rereading mutable fields."""

    if type(value) is not FiniteSessionModel or value._verification_token is not _FINITE_SESSION_MODEL_TOKEN:
        return False
    try:
        return (
            type(value._source_json) is bytes
            and type(value.identity) is str
            and sha256(value._source_json).hexdigest() == value.identity
            and type(value.context) is ModelContext
            and value.context.read_only_replay_context() is not None
        )
    except (AttributeError, TypeError, ValueError):
        return False


def _finite_model_binding_digest(value: FiniteSessionModel) -> str:
    """Content-address every finite model value consumed by the coordinator."""

    def fraction_key(item: object) -> tuple[int, int]:
        if type(item) is not Fraction:
            raise TypeError("finite model rational leaf is not exact")
        return item.numerator, item.denominator

    def interval_key(item: object) -> tuple[object, ...]:
        if type(item) is not Interval:
            raise TypeError("finite model interval is not typed")
        return (*fraction_key(item.lower), *fraction_key(item.upper), item.lower_closed, item.upper_closed)

    def mapping_key(item: object) -> tuple[tuple[str, object], ...]:
        if not isinstance(item, Mapping):
            raise TypeError("finite model mapping is invalid")
        # JSON round-tripping rejects hostile non-contract leaves while giving
        # the exact normalised value used when the factory parsed the model.
        rendered = json.dumps(dict(item), sort_keys=True, separators=(",", ":"))
        decoded = json.loads(rendered)
        if not isinstance(decoded, dict) or any(type(key) is not str for key in decoded):
            raise TypeError("finite model mapping is not a JSON object")
        return tuple(sorted(decoded.items()))

    def action_key(identifier: object, action: object) -> tuple[object, ...]:
        if type(identifier) is not str or type(action) is not SyntheticAction:
            raise TypeError("finite model action is invalid")
        if (
            type(action.action_id) is not str
            or type(action.kind) is not str
            or type(action.cost) is not int
            or type(action.transition_json) is not str
            or type(action.recover_when_unknown) is not bool
            or (action.declared_target is not None and type(action.declared_target) is not str)
        ):
            raise TypeError("finite model action scalar is invalid")
        if not isinstance(action.detail_charges, Mapping):
            raise TypeError("finite model action charges are invalid")
        charges = tuple(sorted(action.detail_charges.items()))
        if any(type(name) is not str or type(amount) is not int for name, amount in charges):
            raise TypeError("finite model action charge leaf is invalid")
        if type(action.enabled_summaries) is not frozenset or any(type(item) is not str for item in action.enabled_summaries):
            raise TypeError("finite model action summary is invalid")
        emissions: list[tuple[str, tuple[str, ...]]] = []
        if not isinstance(action.observable_by_hypothesis, Mapping):
            raise TypeError("finite model action emissions are invalid")
        for hypothesis, values in sorted(action.observable_by_hypothesis.items()):
            if type(hypothesis) is not str or type(values) is not tuple or any(type(item) is not str for item in values):
                raise TypeError("finite model action emission leaf is invalid")
            emissions.append((hypothesis, values))
        ticks: list[tuple[str, tuple[int, int]]] = []
        if not isinstance(action.measurement_ticks_by_hypothesis, Mapping):
            raise TypeError("finite model action ticks are invalid")
        for hypothesis, tick in sorted(action.measurement_ticks_by_hypothesis.items()):
            if type(hypothesis) is not str:
                raise TypeError("finite model action tick key is invalid")
            ticks.append((hypothesis, fraction_key(tick)))
        return (
            identifier,
            action.action_id,
            action.kind,
            action.cost,
            charges,
            tuple(sorted(action.enabled_summaries)),
            action.transition_json,
            tuple(emissions),
            tuple(ticks),
            action.declared_target,
            action.recover_when_unknown,
        )

    def frontier_key(identifier: object, frontier: object) -> tuple[object, ...]:
        if type(identifier) is not str or type(frontier) is not FrontierEntry:
            raise TypeError("finite model initial frontier is invalid")
        if (
            type(frontier.hypothesis_id) is not str
            or type(frontier.control_state_id) is not str
            or type(frontier.path_length) is not int
            or type(frontier.history_provenance) is not tuple
            or any(type(reference) is not str for reference in frontier.history_provenance)
            or type(frontier.status) is not str
            or type(frontier.model_identity) is not str
        ):
            raise TypeError("finite model initial frontier scalar is invalid")
        if not isinstance(frontier.clocks, Mapping) or not isinstance(frontier.typed_store, Mapping):
            raise TypeError("finite model initial frontier fields are invalid")
        clocks = tuple(
            (name, interval_key(interval))
            for name, interval in sorted(frontier.clocks.items())
            if type(name) is str
        )
        if len(clocks) != len(frontier.clocks):
            raise TypeError("finite model initial frontier clock key is invalid")
        return (
            identifier,
            frontier.hypothesis_id,
            frontier.control_state_id,
            clocks,
            mapping_key(frontier.typed_store),
            frontier.path_length,
            frontier.history_provenance,
            frontier.status,
            frontier.model_identity,
        )

    if not isinstance(value.actions, Mapping) or not isinstance(value.initial_frontiers, Mapping):
        raise TypeError("finite model collections are invalid")
    if type(value.uncertainty) is not MeasurementUncertainty:
        raise TypeError("finite model uncertainty is invalid")
    if (
        any(type(limit) is not int for limit in (
            value.path_limit,
            value.frontier_limit,
            value.hypothesis_limit,
            value.action_limit,
            value.observation_class_limit,
        ))
        or type(value.identity) is not str
        or type(value.uncertainty.uncertainty_id) is not str
        or type(value.uncertainty.clock_id) is not str
        or type(value.uncertainty.time_unit) is not str
        or type(value.uncertainty.identity) is not str
    ):
        raise TypeError("finite model scalar is invalid")
    payload = (
        value.context.identity,
        tuple(action_key(identifier, action) for identifier, action in sorted(value.actions.items())),
        tuple(frontier_key(identifier, frontier) for identifier, frontier in sorted(value.initial_frontiers.items())),
        value.path_limit,
        value.frontier_limit,
        value.hypothesis_limit,
        value.action_limit,
        value.observation_class_limit,
        value.identity,
        (
            value.uncertainty.uncertainty_id,
            value.uncertainty.clock_id,
            value.uncertainty.time_unit,
            fraction_key(value.uncertainty.maximum_error),
            value.uncertainty.identity,
        ),
    )
    return sha256(repr(payload).encode("utf-8")).hexdigest()


def _canonical_model(value: Mapping[str, Any]) -> dict[str, Any]:
    if set(value) != {"stateIds", "clockIds", "typedDomains"}:
        raise ValueError("finite session model declaration is invalid")
    states, clocks, domains = value.get("stateIds"), value.get("clockIds"), value.get("typedDomains")
    if not isinstance(states, list) or not isinstance(clocks, list) or not isinstance(domains, Mapping):
        raise ValueError("finite session model declaration is invalid")
    if any(not isinstance(item, str) for item in states + clocks):
        raise ValueError("finite session model identifiers are invalid")
    normalized_domains: dict[str, list[Any]] = {}
    for key, domain in domains.items():
        if not isinstance(key, str) or not isinstance(domain, list):
            raise ValueError("finite session model typed domains are invalid")
        normalized_domains[key] = sorted(domain)
    return {"stateIds": sorted(states), "clockIds": sorted(clocks), "typedDomains": normalized_domains}


def _initial_frontier(context: ModelContext, item: Any) -> tuple[str, FrontierEntry]:
    if not isinstance(item, Mapping):
        raise ValueError("finite session hypothesis is invalid")
    required = {"id", "controlStateId", "clockConstraint", "typedStore"}
    if set(item) != required:
        raise ValueError("finite session hypothesis uses unknown or missing fields")
    identifier = item.get("id")
    state = item.get("controlStateId")
    clocks = item.get("clockConstraint")
    store = item.get("typedStore")
    if not isinstance(identifier, str) or not identifier or not isinstance(state, str):
        raise ValueError("finite session hypothesis identity is invalid")
    if not isinstance(clocks, Mapping) or set(clocks) != set(context.clock_ids):
        raise ValueError("finite session hypothesis clock constraint is invalid")
    parsed_clocks = {name: Interval.from_mapping(interval) for name, interval in clocks.items()}
    if not isinstance(store, Mapping):
        raise ValueError("finite session hypothesis typed store is invalid")
    return identifier, initial_entry(
        context,
        hypothesis_id=identifier,
        control_state_id=state,
        clocks=parsed_clocks,
        typed_store=store,
        root_id=f"root:{identifier}",
    )


def _parse_action(item: Any, hypothesis_ids: frozenset[str]) -> SyntheticAction:
    if not isinstance(item, Mapping):
        raise ValueError("finite session action is invalid")
    required = {
        "id", "kind", "cost", "detailCharges", "enabledSummaries", "transition", "observableByHypothesis", "measurementTicksByHypothesis",
    }
    allowed = required | {"declaredTarget", "recoverWhenUnknown"}
    if not set(item) <= allowed or not required <= set(item):
        raise ValueError("finite session action uses unknown or missing fields")
    identifier = item.get("id")
    kind = item.get("kind")
    cost = item.get("cost")
    detail_charges = item.get("detailCharges")
    summaries = item.get("enabledSummaries")
    transition = item.get("transition")
    emissions = item.get("observableByHypothesis")
    measurement_ticks = item.get("measurementTicksByHypothesis")
    declared_target = item.get("declaredTarget")
    recover_when_unknown = item.get("recoverWhenUnknown", False)
    if not isinstance(identifier, str) or not identifier or kind not in _ACTION_KINDS:
        raise ValueError("finite session action identity or kind is invalid")
    if kind in {"PREP", "RECOVER"}:
        if not isinstance(declared_target, str) or not declared_target.strip():
            raise ValueError("Prep/Recover action requires a nonblank declared target")
        if not isinstance(recover_when_unknown, bool):
            raise ValueError("Prep/Recover unknown eligibility must be Boolean")
        if kind == "PREP" and recover_when_unknown:
            raise ValueError("Prep cannot be eligible from an UNKNOWN session")
    elif "declaredTarget" in item or "recoverWhenUnknown" in item:
        raise ValueError("TEST action cannot declare a recovery target or UNKNOWN eligibility")
    if isinstance(cost, bool) or not isinstance(cost, int) or cost < 1:
        raise ValueError("finite session action cost must be a positive integer")
    if not isinstance(detail_charges, Mapping) or set(detail_charges) != {
        "acquisition", "computation", "preparation", "recovery", "retry",
    }:
        raise ValueError("finite session action detail charges are invalid")
    if any(isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in detail_charges.values()):
        raise ValueError("finite session action detail charge is invalid")
    if not isinstance(summaries, list) or not summaries or any(not isinstance(value, str) or not value for value in summaries):
        raise ValueError("finite session action enabled summaries are invalid")
    if not isinstance(transition, Mapping):
        raise ValueError("finite session action transition is invalid")
    if not isinstance(emissions, Mapping) or set(emissions) != hypothesis_ids:
        raise ValueError("finite session action emissions must cover exactly the declared hypotheses")
    if not isinstance(measurement_ticks, Mapping) or set(measurement_ticks) != hypothesis_ids:
        raise ValueError("finite session action measurement ticks must cover exactly the declared hypotheses")
    parsed_emissions: dict[str, tuple[str, ...]] = {}
    parsed_ticks: dict[str, Fraction] = {}
    for hypothesis, emission in emissions.items():
        values = (emission,) if isinstance(emission, str) else tuple(emission) if isinstance(emission, list) else ()
        if not values or any(not isinstance(item, str) or not item for item in values) or len(values) != len(set(values)):
            raise ValueError("finite session action observable emission is invalid")
        parsed_emissions[hypothesis] = values
        parsed_ticks[hypothesis] = _exact_tick(measurement_ticks[hypothesis], "finite session action measurement tick")
    transition_json = json.dumps(transition, sort_keys=True, separators=(",", ":"))
    return SyntheticAction(
        identifier,
        kind,
        cost,
        MappingProxyType(dict(detail_charges)),
        frozenset(summaries),
        transition_json,
        MappingProxyType(parsed_emissions),
        MappingProxyType(parsed_ticks),
        declared_target,
        recover_when_unknown,
    )


def _json_clone(value: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return a detached, JSON-only model contract or a named input error."""

    try:
        cloned = json.loads(json.dumps(value, sort_keys=True, separators=(",", ":")))
    except (TypeError, ValueError) as exc:
        raise ValueError("finite session model must contain only JSON contract values") from exc
    if not isinstance(cloned, Mapping):
        raise ValueError("finite session model must be an object")
    return cloned


def _parse_uncertainty(value: Any, projection_clock: str) -> MeasurementUncertainty:
    if not isinstance(value, Mapping) or set(value) != {
        "id", "clockId", "timeUnit", "maximumErrorTicks",
    }:
        raise ValueError("finite session uncertainty contract is invalid")
    uncertainty_id = value.get("id")
    clock_id = value.get("clockId")
    time_unit = value.get("timeUnit")
    if (
        not isinstance(uncertainty_id, str) or not uncertainty_id
        or clock_id != projection_clock
        or time_unit != "ticks"
    ):
        raise ValueError("finite session uncertainty identity, clock, or unit is invalid")
    maximum_error = _exact_tick(value.get("maximumErrorTicks"), "finite session maximum uncertainty")
    if maximum_error < 0:
        raise ValueError("finite session maximum uncertainty must be nonnegative")
    canonical = {
        "id": uncertainty_id,
        "clockId": clock_id,
        "timeUnit": time_unit,
        "maximumErrorTicks": {
            "numerator": maximum_error.numerator,
            "positiveDenominator": maximum_error.denominator,
        },
    }
    identity = sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8"),
    ).hexdigest()
    return MeasurementUncertainty(uncertainty_id, clock_id, time_unit, maximum_error, identity)


def _exact_tick(value: Any, label: str) -> Fraction:
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
    raise ValueError(f"{label} must be an exact integer or rational mapping")


def _frontier_paths(value: FrontierEntry | tuple[FrontierEntry, ...]) -> tuple[FrontierEntry, ...]:
    """Normalize one public hypothesis frontier into its finite path bundle."""

    paths = (value,) if isinstance(value, FrontierEntry) else value
    if (
        not isinstance(paths, tuple)
        or not paths
        or any(not isinstance(path, FrontierEntry) for path in paths)
    ):
        raise ValueError("hypothesis frontier must be a nonempty finite path tuple")
    return paths


def _bounded_paths(paths: list[FrontierEntry], limit: int) -> tuple[FrontierEntry, ...]:
    """Deduplicate exact paths while retaining a conservative finite bundle."""

    unique: list[FrontierEntry] = []
    identities: set[tuple[object, ...]] = set()
    for path in paths:
        identity = (
            path.hypothesis_id, path.control_state_id, tuple(sorted(path.clocks.items())),
            tuple(sorted(path.typed_store.items())), path.path_length,
            path.history_provenance, path.status, path.model_identity,
        )
        if identity not in identities:
            identities.add(identity)
            unique.append(path)
    if len(unique) > limit:
        # This branch cannot claim that omitted paths are infeasible.  The
        # caller receives the first finite bundle only when its declared bound
        # was respected; otherwise construction is invalid rather than silently
        # erasing a compatible path.
        raise ValueError("finite hypothesis path bundle exceeds the declared frontier bound")
    return tuple(unique)


def _positive_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"finite session {label} must be a positive integer")
    return value
