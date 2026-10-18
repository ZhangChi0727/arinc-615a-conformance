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

    def merge_key(self) -> tuple[Any, ...]:
        return (
            self.hypothesis_id,
            self.control_state_id,
            tuple(sorted((key, _interval_key(value)) for key, value in self.clocks.items())),
            tuple(sorted(self.typed_store.items())),
            self.history_provenance,
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
    entry: FrontierEntry,
    transition: Mapping[str, Any],
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
    diagnostics: list[KernelDiagnostic] = []
    if not _valid_entry(entry, state_ids, clock_ids, typed_domains, diagnostics):
        return KernelResult("SPEC-ERROR", (entry,), tuple(diagnostics))
    if not isinstance(path_limit, int) or path_limit < 0 or not isinstance(frontier_limit, int) or frontier_limit < 1:
        return KernelResult("SPEC-ERROR", (entry,), (KernelDiagnostic("INVALID-LIMIT", "path and frontier limits must be finite nonnegative integers"),))
    if entry.path_length >= path_limit:
        return KernelResult("CONSERVATIVE-UNKNOWN", (entry,), (KernelDiagnostic("PATH-LIMIT", "declared path bound reached; hypothesis retained"),))
    if transition.get("source") != entry.control_state_id:
        return KernelResult("INFEASIBLE", ())
    if transition.get("target") not in state_ids or not isinstance(transition.get("id"), str):
        return KernelResult("SPEC-ERROR", (entry,), (KernelDiagnostic("INVALID-TRANSITION", "transition identity or target is undeclared"),))
    updates = transition.get("simultaneousUpdates")
    guard = transition.get("guardAst")
    if not isinstance(updates, list) or not isinstance(guard, Mapping):
        return KernelResult("SPEC-ERROR", (entry,), (KernelDiagnostic("INVALID-TRANSITION", "guardAst and simultaneousUpdates are required"),))
    if delta is None:
        delta = Fraction(0)
    if delta < 0:
        return KernelResult("SPEC-ERROR", (entry,), (KernelDiagnostic("INVALID-DELTA", "time advance must be nonnegative"),))

    advanced = {name: interval.shifted(delta) for name, interval in entry.clocks.items()}
    guarded, guard_error = _apply_guard(entry.control_state_id, entry.typed_store, advanced, guard, clock_ids)
    if guard_error is not None:
        return KernelResult("SPEC-ERROR", (entry,), (guard_error,))
    if guarded is None:
        return KernelResult("INFEASIBLE", ())
    if observation_intervals:
        guarded = dict(guarded)
        for clock, observation in observation_intervals.items():
            if clock not in clock_ids or clock not in guarded:
                return KernelResult("SPEC-ERROR", (entry,), (KernelDiagnostic("INVALID-OBSERVATION-CONSTRAINT", "observation uses an undeclared clock"),))
            intersection = guarded[clock].intersect(observation)
            if intersection is None:
                return KernelResult("INFEASIBLE", ())
            guarded[clock] = intersection

    successor, update_error = _apply_updates(entry, transition, guarded, state_ids, clock_ids, typed_domains)
    if update_error is not None:
        return KernelResult("SPEC-ERROR", (entry,), (update_error,))
    if frontier_limit < 1:
        return KernelResult("CONSERVATIVE-UNKNOWN", (entry,), (KernelDiagnostic("FRONTIER-LIMIT", "declared frontier bound reached; hypothesis retained"),))
    return KernelResult("FEASIBLE", (successor,))


def merge_frontier(entries: Sequence[FrontierEntry], *, frontier_limit: int) -> KernelResult:
    """Merge only fully identical, whole-history frontiers."""
    if not isinstance(frontier_limit, int) or frontier_limit < 1:
        return KernelResult("SPEC-ERROR", tuple(entries), (KernelDiagnostic("INVALID-LIMIT", "frontier limit must be a positive integer"),))
    merged: dict[tuple[Any, ...], FrontierEntry] = {}
    for entry in entries:
        merged.setdefault(entry.merge_key(), entry)
    values = tuple(merged.values())
    if len(values) > frontier_limit:
        return KernelResult("CONSERVATIVE-UNKNOWN", tuple(entries), (KernelDiagnostic("FRONTIER-LIMIT", "frontier state limit reached; no hypothesis removed"),))
    return KernelResult("FEASIBLE", values)


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
) -> tuple[FrontierEntry, KernelDiagnostic | None]:
    next_state = transition["target"]
    next_clocks = dict(clocks)
    next_store = dict(entry.typed_store)
    # All update operands are validated before any successor is published.
    for update in transition["simultaneousUpdates"]:
        if not isinstance(update, Mapping):
            return entry, KernelDiagnostic("INVALID-UPDATE", "update is not a tagged object")
        tag = update.get("tag")
        if tag == "STATE-ASSIGN":
            value = update.get("state")
            if not isinstance(value, str) or value not in state_ids:
                return entry, KernelDiagnostic("INVALID-UPDATE", "state update uses an undeclared control state")
            next_state = value
        elif tag == "CLOCK-RESET-TO-ZERO":
            clock = update.get("clock")
            if not isinstance(clock, str) or clock not in clock_ids:
                return entry, KernelDiagnostic("INVALID-UPDATE", "clock reset uses an undeclared clock")
            next_clocks[clock] = Interval(Fraction(0), Fraction(0), True, True)
        elif tag == "TYPED-FIELD-ASSIGN":
            field = update.get("field")
            if not isinstance(field, str) or field not in typed_domains or update.get("value") not in typed_domains[field]:
                return entry, KernelDiagnostic("INVALID-UPDATE", "typed field update is outside its declared domain")
            next_store[field] = update["value"]
        else:
            return entry, KernelDiagnostic("UNSUPPORTED-UPDATE", f"unsupported update tag: {tag!r}")
    return FrontierEntry(
        hypothesis_id=entry.hypothesis_id,
        control_state_id=next_state,
        clocks=next_clocks,
        typed_store=next_store,
        path_length=entry.path_length + 1,
        history_provenance=entry.history_provenance + (str(transition["id"]),),
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
    if set(entry.clocks) != clock_ids:
        diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "frontier clocks must exactly match declared clock IDs")); valid = False
    for field, value in entry.typed_store.items():
        if field not in typed_domains or value not in typed_domains[field]:
            diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "frontier typedStore is outside the declared domain")); valid = False
    if set(entry.typed_store) != set(typed_domains):
        diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "frontier typedStore must contain every declared field")); valid = False
    if not isinstance(entry.path_length, int) or entry.path_length < 0:
        diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "pathLength must be a nonnegative integer")); valid = False
    if not isinstance(entry.history_provenance, tuple):
        diagnostics.append(KernelDiagnostic("INVALID-ENTRY", "history provenance must be immutable")); valid = False
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
