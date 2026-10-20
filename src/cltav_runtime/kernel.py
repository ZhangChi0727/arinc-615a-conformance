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
from types import MappingProxyType
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class KernelDiagnostic:
    """A controlled diagnostic; never an IUT verdict."""

    code: str
    message: str


@dataclass(frozen=True)
class Interval:
    """Exact rational interval with preserved endpoint topology."""

    lower: Fraction
    upper: Fraction
    lower_closed: bool
    upper_closed: bool

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "Interval":
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

    def __post_init__(self) -> None:
        """Take immutable snapshots so later caller mutation cannot rewrite history."""
        object.__setattr__(self, "clocks", MappingProxyType(dict(self.clocks)))
        object.__setattr__(self, "typed_store", MappingProxyType(dict(self.typed_store)))
        object.__setattr__(self, "history_provenance", tuple(self.history_provenance))

    def merge_key(self) -> tuple[Any, ...]:
        return (
            self.hypothesis_id,
            self.control_state_id,
            tuple(sorted((key, _interval_key(value)) for key, value in self.clocks.items())),
            tuple(sorted(self.typed_store.items())),
            self.history_provenance,
            self.path_length,
            self.status,
        )


@dataclass(frozen=True)
class KernelResult:
    """The typed, conservative result of a single finite transition step."""

    kind: str
    entries: tuple[FrontierEntry, ...]
    diagnostics: tuple[KernelDiagnostic, ...] = field(default_factory=tuple)

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
            typed_domains=typed_domains, observation_intervals=observation_intervals,
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
    if len(clock_ids) != 1:
        return KernelResult("SPEC-ERROR", (entry,), (KernelDiagnostic("UNPROJECTED-MULTI-CLOCK", "this finite witness implementation accepts exactly one declared clock"),))
    diagnostics: list[KernelDiagnostic] = []
    if not _valid_entry(entry, state_ids, clock_ids, typed_domains, diagnostics):
        return KernelResult("SPEC-ERROR", (entry,), tuple(diagnostics))
    if not _valid_limit(path_limit, minimum=0) or not _valid_limit(frontier_limit, minimum=1):
        return KernelResult("SPEC-ERROR", (entry,), (KernelDiagnostic("INVALID-LIMIT", "path and frontier limits must be finite nonnegative integers"),))
    transition_error = _validate_transition(transition, state_ids, clock_ids, typed_domains)
    if transition_error is not None:
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
    if delta is None:
        delta = Fraction(0)
    elif isinstance(delta, int) and not isinstance(delta, bool):
        delta = Fraction(delta)
    elif not isinstance(delta, Fraction):
        return KernelResult("SPEC-ERROR", (entry,), (KernelDiagnostic("INVALID-DELTA", "time advance must be an exact integer or Fraction"),))
    if delta < 0:
        return KernelResult("SPEC-ERROR", (entry,), (KernelDiagnostic("INVALID-DELTA", "time advance must be nonnegative"),))

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

    successor, update_error = _apply_updates(entry, transition, guarded, state_ids, clock_ids, typed_domains, delta, observation_intervals)
    if update_error is not None:
        return KernelResult("SPEC-ERROR", (entry,), (update_error,))
    if frontier_limit < 1:
        return KernelResult("CONSERVATIVE-UNKNOWN", (entry,), (KernelDiagnostic("FRONTIER-LIMIT", "declared frontier bound reached; hypothesis retained"),))
    return KernelResult("FEASIBLE", (successor,))


def merge_frontier(entries: Sequence[FrontierEntry], *, frontier_limit: int) -> KernelResult:
    """Merge only fully identical, whole-history frontiers."""
    try:
        retained = tuple(entries)
        if not _valid_limit(frontier_limit, minimum=1):
            return KernelResult("SPEC-ERROR", retained, (KernelDiagnostic("INVALID-LIMIT", "frontier limit must be a positive integer"),))
        if any(not isinstance(entry, FrontierEntry) for entry in retained):
            return KernelResult("SPEC-ERROR", (), (KernelDiagnostic("MALFORMED-FRONTIER", "frontier contains a non-entry value"),))
        merged: dict[tuple[Any, ...], FrontierEntry] = {}
        for entry in retained:
            merged.setdefault(entry.merge_key(), entry)
        values = tuple(merged.values())
        if len(values) > frontier_limit:
            return KernelResult("CONSERVATIVE-UNKNOWN", retained, (KernelDiagnostic("FRONTIER-LIMIT", "frontier state limit reached; no hypothesis removed"),))
        return KernelResult("FEASIBLE", values)
    except (AttributeError, TypeError, ValueError) as exc:
        return KernelResult("SPEC-ERROR", (), (KernelDiagnostic("MALFORMED-FRONTIER", str(exc) or type(exc).__name__),))


def _validate_guard_ast(
    ast: Mapping[str, Any],
    state_ids: set[str],
    clock_ids: set[str],
    typed_domains: Mapping[str, set[Any]],
) -> KernelDiagnostic | None:
    """Validate every branch before evaluating any branch.

    This is deliberately separate from guard evaluation.  A false first
    operand cannot make an unsupported later operand disappear into an
    ``INFEASIBLE`` result.
    """
    tag = ast.get("tag")
    if tag == "TRUE":
        return None
    if tag == "AND":
        operands = ast.get("operands")
        if not isinstance(operands, list) or not operands:
            return KernelDiagnostic("INVALID-GUARD-AST", "AND requires a nonempty operands list")
        for operand in operands:
            if not isinstance(operand, Mapping):
                return KernelDiagnostic("INVALID-GUARD-AST", "AND operand is not a tagged guard")
            diagnostic = _validate_guard_ast(operand, state_ids, clock_ids, typed_domains)
            if diagnostic is not None:
                return diagnostic
        return None
    if tag == "STATE-EQUALS":
        state = ast.get("state")
        if not isinstance(state, str) or state not in state_ids:
            return KernelDiagnostic("INVALID-GUARD-AST", "state guard uses an undeclared control state")
        return None
    if tag == "TYPED-FIELD-EQUALS":
        field = ast.get("field")
        if not isinstance(field, str) or field not in typed_domains or ast.get("value") not in typed_domains[field]:
            return KernelDiagnostic("INVALID-GUARD-AST", "typed field guard is outside the declared domain")
        return None
    if tag == "RATIONAL-INTERVAL-CONTAINS":
        if not isinstance(ast.get("clock"), str) or ast["clock"] not in clock_ids:
            return KernelDiagnostic("INVALID-GUARD-AST", "interval guard uses an undeclared clock")
        try:
            Interval.from_mapping(ast["interval"])
        except (KeyError, TypeError, ValueError):
            return KernelDiagnostic("INVALID-GUARD-AST", "interval guard requires a canonical rational interval")
        return None
    return KernelDiagnostic("UNSUPPORTED-GUARD-AST", f"unsupported guard AST tag: {tag!r}")


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
) -> tuple[FrontierEntry, KernelDiagnostic | None]:
    updates = transition["simultaneousUpdates"]
    next_state = transition["target"]
    next_clocks = dict(clocks)
    next_store = dict(entry.typed_store)
    for update in updates:
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
        history_provenance=entry.history_provenance + (_step_provenance(transition["id"], clocks, delta, observations),),
        status=entry.status,
    ), None


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
    if not isinstance(entry.history_provenance, tuple) or any(not isinstance(item, str) for item in entry.history_provenance):
        diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "history provenance must be immutable")); valid = False
    if entry.status not in {"KNOWN", "CONSERVATIVE-UNKNOWN"}:
        diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "frontier status is not declared")); valid = False
    return valid


def _fraction(value: Any) -> Fraction:
    if not isinstance(value, Mapping):
        raise ValueError("rational must be an object")
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


def _valid_limit(value: object, *, minimum: int) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= minimum


def _domain_contains(domain: set[Any], value: object) -> bool:
    try:
        return value in domain
    except TypeError:
        return False


def _valid_interval(value: object) -> bool:
    return (
        isinstance(value, Interval)
        and isinstance(value.lower, Fraction)
        and isinstance(value.upper, Fraction)
        and isinstance(value.lower_closed, bool)
        and isinstance(value.upper_closed, bool)
        and not (value.lower > value.upper or (value.lower == value.upper and not (value.lower_closed and value.upper_closed)))
    )


def _step_provenance(
    transition_id: str,
    pre_update_clocks: Mapping[str, Interval],
    delta: Fraction,
    observations: Mapping[str, Interval] | None,
) -> str:
    """A stable identity for the actual path input, including time evidence.

    It is intentionally not a display trace.  Its only purpose is preventing a
    clock reset from erasing the distinct pre-reset time/observation history
    that the finite merge contract requires us to retain.
    """
    clock_part = tuple(sorted((name, _interval_key(interval)) for name, interval in pre_update_clocks.items()))
    observation_part = tuple(sorted((name, _interval_key(interval)) for name, interval in (observations or {}).items()))
    return repr((transition_id, delta, clock_part, observation_part))
