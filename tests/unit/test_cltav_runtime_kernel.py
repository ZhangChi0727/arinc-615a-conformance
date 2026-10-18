from fractions import Fraction

from cltav_runtime.kernel import FrontierEntry, Interval, merge_frontier, propagate_transition


STATE_IDS = {"q0", "q1", "q2"}
CLOCK_IDS = {"x", "y"}
DOMAINS = {"mode": {"normal", "recovery"}}


def rational(value: int) -> dict[str, int]:
    return {"numerator": value, "positiveDenominator": 1}


def interval(lower: int, upper: int, lower_closed: bool = True, upper_closed: bool = True) -> dict[str, object]:
    return {"lower": rational(lower), "upper": rational(upper), "lowerClosed": lower_closed, "upperClosed": upper_closed}


def entry(*, provenance: tuple[str, ...] = ("S0",), x: Interval | None = None) -> FrontierEntry:
    return FrontierEntry(
        hypothesis_id="h0",
        control_state_id="q0",
        clocks={"x": x or Interval(Fraction(0), Fraction(1), True, True), "y": Interval(Fraction(2), Fraction(2), True, True)},
        typed_store={"mode": "normal"},
        path_length=0,
        history_provenance=provenance,
    )


def transition(guard: dict[str, object], updates: list[dict[str, object]] | None = None) -> dict[str, object]:
    return {"id": "t01", "source": "q0", "target": "q1", "guardAst": guard, "simultaneousUpdates": updates or []}


def invoke(current: FrontierEntry, spec: dict[str, object], **kwargs: object):
    return propagate_transition(
        current,
        spec,
        state_ids=STATE_IDS,
        clock_ids=CLOCK_IDS,
        typed_domains=DOMAINS,
        path_limit=kwargs.pop("path_limit", 3),
        frontier_limit=kwargs.pop("frontier_limit", 4),
        **kwargs,
    )


def test_feasible_interval_guard_preserves_exact_endpoint_and_history() -> None:
    result = invoke(entry(), transition({"tag": "RATIONAL-INTERVAL-CONTAINS", "clock": "x", "interval": interval(0, 2)}))
    assert result.kind == "FEASIBLE"
    successor = result.entries[0]
    assert successor.control_state_id == "q1"
    assert successor.clocks["x"] == Interval(Fraction(0), Fraction(1), True, True)
    assert successor.history_provenance == ("S0", "t01")


def test_open_endpoint_intersection_is_not_silently_closed() -> None:
    result = invoke(entry(x=Interval(Fraction(0), Fraction(1), True, True)), transition({"tag": "RATIONAL-INTERVAL-CONTAINS", "clock": "x", "interval": interval(1, 2, False, True)}))
    assert result.kind == "INFEASIBLE"


def test_unsupported_guard_is_controlled_and_retains_path() -> None:
    current = entry()
    result = invoke(current, transition({"tag": "CALL", "name": "not-supported"}))
    assert result.kind == "SPEC-ERROR"
    assert result.entries == (current,)
    assert result.diagnostics[0].code == "UNSUPPORTED-GUARD-AST"


def test_clock_advance_intersection_and_reset_are_exact_and_simultaneous() -> None:
    result = invoke(
        entry(),
        transition(
            {"tag": "AND", "operands": [{"tag": "STATE-EQUALS", "state": "q0"}, {"tag": "RATIONAL-INTERVAL-CONTAINS", "clock": "x", "interval": interval(1, 2)}]},
            [{"tag": "CLOCK-RESET-TO-ZERO", "clock": "x"}, {"tag": "TYPED-FIELD-ASSIGN", "field": "mode", "value": "recovery"}],
        ),
        delta=Fraction(1),
    )
    assert result.kind == "FEASIBLE"
    successor = result.entries[0]
    assert successor.clocks["x"] == Interval(Fraction(0), Fraction(0), True, True)
    assert successor.clocks["y"] == Interval(Fraction(3), Fraction(3), True, True)
    assert successor.typed_store == {"mode": "recovery"}


def test_invalid_update_is_controlled_and_cannot_publish_successor() -> None:
    current = entry()
    result = invoke(current, transition({"tag": "TRUE"}, [{"tag": "TYPED-FIELD-ASSIGN", "field": "mode", "value": "unsupported"}]))
    assert result.kind == "SPEC-ERROR"
    assert result.entries == (current,)
    assert result.diagnostics[0].code == "INVALID-UPDATE"


def test_limit_is_conservative_not_empty_or_equivalence() -> None:
    current = entry()
    result = invoke(current, transition({"tag": "TRUE"}), path_limit=0)
    assert result.kind == "CONSERVATIVE-UNKNOWN"
    assert result.entries == (current,)
    assert result.diagnostics[0].code == "PATH-LIMIT"


def test_merge_requires_full_history_not_only_hypothesis() -> None:
    first = entry(provenance=("S0", "a"))
    second = entry(provenance=("S0", "b"))
    result = merge_frontier([first, second], frontier_limit=4)
    assert result.kind == "FEASIBLE"
    assert result.entries == (first, second)
