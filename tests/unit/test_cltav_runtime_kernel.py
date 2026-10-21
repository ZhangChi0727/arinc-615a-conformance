from fractions import Fraction

from cltav_runtime.kernel import FrontierEntry, Interval, merge_frontier, propagate_transition


STATE_IDS = {"q0", "q1", "q2"}
CLOCK_IDS = {"x"}
DOMAINS = {"mode": {"normal", "recovery"}}


def rational(value: int) -> dict[str, int]:
    return {"numerator": value, "positiveDenominator": 1}


def interval(lower: int, upper: int, lower_closed: bool = True, upper_closed: bool = True) -> dict[str, object]:
    return {"lower": rational(lower), "upper": rational(upper), "lowerClosed": lower_closed, "upperClosed": upper_closed}


def entry(*, provenance: tuple[str, ...] = ("S0",), x: Interval | None = None) -> FrontierEntry:
    return FrontierEntry(
        hypothesis_id="h0",
        control_state_id="q0",
        clocks={"x": x or Interval(Fraction(0), Fraction(1), True, True)},
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
    assert successor.history_provenance[0] == "S0"
    assert successor.history_provenance[1].startswith("step:")


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


def test_all_guard_branches_are_validated_before_false_branch_can_short_circuit() -> None:
    result = invoke(
        entry(),
        transition({"tag": "AND", "operands": [
            {"tag": "STATE-EQUALS", "state": "q2"},
            {"tag": "CALL", "name": "unsupported"},
        ]}),
    )
    assert result.kind == "SPEC-ERROR"
    assert result.diagnostics[0].code == "UNSUPPORTED-GUARD-AST"


def test_unprojected_multi_clock_and_float_advance_are_controlled_errors() -> None:
    current = entry()
    multi = propagate_transition(
        current, transition({"tag": "TRUE"}), state_ids=STATE_IDS,
        clock_ids={"x", "y"}, typed_domains=DOMAINS, path_limit=3, frontier_limit=4,
    )
    floating = invoke(current, transition({"tag": "TRUE"}), delta=0.5)
    assert multi.kind == "SPEC-ERROR"
    assert multi.diagnostics[0].code == "UNPROJECTED-MULTI-CLOCK"
    assert floating.kind == "SPEC-ERROR"
    assert floating.diagnostics[0].code == "INVALID-DELTA"


def test_conflicting_simultaneous_updates_are_not_list_ordered() -> None:
    result = invoke(
        entry(), transition({"tag": "TRUE"}, [
            {"tag": "TYPED-FIELD-ASSIGN", "field": "mode", "value": "normal"},
            {"tag": "TYPED-FIELD-ASSIGN", "field": "mode", "value": "recovery"},
        ]),
    )
    assert result.kind == "SPEC-ERROR"
    assert result.diagnostics[0].code == "CONFLICTING-UPDATE"


def test_merge_does_not_drop_conservative_status_or_path_limit_evidence() -> None:
    known = entry(provenance=("S0", "t01"))
    unknown = FrontierEntry(
        hypothesis_id=known.hypothesis_id, control_state_id=known.control_state_id,
        clocks=known.clocks, typed_store=known.typed_store, path_length=known.path_length,
        history_provenance=known.history_provenance, status="CONSERVATIVE-UNKNOWN",
    )
    result = merge_frontier([known, unknown], frontier_limit=4)
    assert result.entries == (known, unknown)


def test_malformed_top_level_input_returns_named_diagnostic() -> None:
    result = propagate_transition(
        object(), {"id": "t", "source": "q0", "target": "q1", "guardAst": {"tag": "TRUE"}, "simultaneousUpdates": []},
        state_ids=STATE_IDS, clock_ids=CLOCK_IDS, typed_domains=DOMAINS,
        path_limit=3, frontier_limit=4,
    )
    assert result.kind == "SPEC-ERROR"
    assert result.diagnostics[0].code == "MALFORMED-KERNEL-INPUT"


def test_conservative_path_is_never_excluded_by_a_false_guard() -> None:
    current = FrontierEntry(
        hypothesis_id="h0", control_state_id="q0", clocks=entry().clocks,
        typed_store={"mode": "normal"}, path_length=0,
        history_provenance=("S0",), status="CONSERVATIVE-UNKNOWN",
    )
    result = invoke(current, transition({"tag": "STATE-EQUALS", "state": "q2"}))
    assert result.kind == "CONSERVATIVE-UNKNOWN"
    assert result.entries == (current,)


def test_callers_cannot_mutate_a_published_frontier_snapshot() -> None:
    clock_data = {"x": Interval(Fraction(0), Fraction(1), True, True)}
    store_data = {"mode": "normal"}
    current = FrontierEntry("h0", "q0", clock_data, store_data, 0, ("S0",))
    clock_data["x"] = Interval(Fraction(9), Fraction(9), True, True)
    store_data["mode"] = "recovery"
    assert current.clocks["x"] == Interval(Fraction(0), Fraction(1), True, True)
    assert current.typed_store == {"mode": "normal"}


def test_transition_validation_precedes_source_feasibility_shortcut() -> None:
    spec = transition({"tag": "TRUE"}, [{"tag": "CALL"}])
    spec["source"] = "q2"
    result = invoke(entry(), spec)
    assert result.kind == "SPEC-ERROR"
    assert result.diagnostics[0].code == "UNSUPPORTED-UPDATE"


def test_frontier_capacity_limit_retains_every_input_path() -> None:
    first = entry(provenance=("S0", "a"))
    second = entry(provenance=("S0", "b"))
    result = merge_frontier([first, second], frontier_limit=1)
    assert result.kind == "CONSERVATIVE-UNKNOWN"
    assert result.entries == (first, second)


def test_all_input_validation_precedes_source_and_limit_shortcuts() -> None:
    bad_guard = invoke(entry(), transition({"tag": "TRUE", "extra": "forbidden"}))
    source_mismatch = transition({"tag": "TRUE"})
    source_mismatch["source"] = "q2"
    bad_delta = invoke(entry(), source_mismatch, delta="not-rational")
    path_limited_bad_delta = invoke(entry(), transition({"tag": "TRUE"}), path_limit=0, delta="not-rational")
    assert bad_guard.diagnostics[0].code == "INVALID-GUARD-AST"
    assert bad_delta.diagnostics[0].code == "INVALID-DELTA"
    assert path_limited_bad_delta.diagnostics[0].code == "INVALID-DELTA"


def test_bool_is_not_an_integer_domain_member() -> None:
    numeric_domains = {"count": {1}}
    numeric_entry = FrontierEntry("h0", "q0", {"x": Interval(Fraction(0), Fraction(1), True, True)}, {"count": True}, 0, ("S0",))
    result = propagate_transition(
        numeric_entry, transition({"tag": "TRUE"}), state_ids=STATE_IDS,
        clock_ids=CLOCK_IDS, typed_domains=numeric_domains, path_limit=3, frontier_limit=4,
    )
    assert result.kind == "SPEC-ERROR"
    assert result.diagnostics[0].code == "INVALID-ENTRY"


def test_merge_rejects_invalid_public_operands_without_losing_them() -> None:
    invalid = FrontierEntry("h0", "q0", {"x": Interval(Fraction(3), Fraction(1), True, True)}, {"mode": "normal"}, True, ("S0",), "INVALID")
    result = merge_frontier([entry(), invalid], frontier_limit=4)
    assert result.kind == "SPEC-ERROR"
    assert result.entries == (entry(), invalid)
    assert result.diagnostics[0].code == "MALFORMED-FRONTIER"


def test_provenance_keeps_distinct_parent_store_after_overwrite() -> None:
    normal = entry()
    recovery = FrontierEntry("h0", "q0", normal.clocks, {"mode": "recovery"}, 0, ("S0",))
    spec = transition({"tag": "TRUE"}, [{"tag": "TYPED-FIELD-ASSIGN", "field": "mode", "value": "normal"}])
    first = invoke(normal, spec).entries[0]
    second = invoke(recovery, spec).entries[0]
    result = merge_frontier([first, second], frontier_limit=4)
    assert result.kind == "FEASIBLE"
    assert len(result.entries) == 2


def test_guard_depth_and_cycle_are_named_controlled_errors() -> None:
    deep: dict[str, object] = {"tag": "TRUE"}
    for _ in range(64):
        deep = {"tag": "AND", "operands": [deep]}
    cyclic: dict[str, object] = {"tag": "AND", "operands": []}
    cyclic["operands"].append(cyclic)  # type: ignore[index]
    depth_result = invoke(entry(), transition(deep))
    cycle_result = invoke(entry(), transition(cyclic))
    assert depth_result.kind == "CONSERVATIVE-UNKNOWN"
    assert depth_result.diagnostics[0].code == "AST-DEPTH-LIMIT"
    assert cycle_result.kind == "SPEC-ERROR"
    assert cycle_result.diagnostics[0].code == "CYCLIC-GUARD-AST"


def test_model_domains_are_finite_scalar_and_type_homogeneous() -> None:
    for bad_domains in ({"mode": "normal"}, {"mode": {"normal", 1.5}}, {"mode": [[1]]}):
        result = propagate_transition(
            entry(), transition({"tag": "TRUE"}), state_ids=STATE_IDS,
            clock_ids=CLOCK_IDS, typed_domains=bad_domains, path_limit=3, frontier_limit=4,
        )
        assert result.kind == "SPEC-ERROR"
        assert result.diagnostics[0].code == "INVALID-MODEL-DOMAIN"


def test_type_preserving_merge_key_does_not_equate_true_and_one() -> None:
    truth = FrontierEntry("h0", "q0", entry().clocks, {"mode": True}, 0, ("S0",))
    one = FrontierEntry("h0", "q0", entry().clocks, {"mode": 1}, 0, ("S0",))
    result = merge_frontier([truth, one], frontier_limit=4)
    assert result.kind == "FEASIBLE"
    assert len(result.entries) == 2


def test_history_provenance_is_a_bounded_hash_chain_over_many_steps() -> None:
    current = entry()
    loop = transition({"tag": "TRUE"})
    loop["target"] = "q0"
    for _ in range(30):
        current = invoke(current, loop, path_limit=31).entries[0]
    assert len(current.history_provenance) == 31
    assert max(map(len, current.history_provenance[1:])) <= 69
