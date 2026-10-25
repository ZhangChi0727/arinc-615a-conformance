"""Public-contract regressions for bounded observation interpretation.

These tests deliberately exercise the public material/contract boundary rather
than session helpers.  In particular, a synthetic declaration may supply a
trace but never its own ownership policy, clock validity, requirement interval,
or deadline authority.
"""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction

import pytest

from cltav_runtime.interpretation import (
    InterpretationContract,
    ObservationInput,
    OwnershipEvent,
    OwnershipOrderBoundary,
    assess_observation,
    bind_observation_input,
    observation_input_from_mapping,
    replay_ownership,
    interpretation_contract_identity,
)
from cltav_runtime.kernel import Interval


def _interval(
    lower: int,
    upper: int,
    *,
    lower_closed: bool = True,
    upper_closed: bool = True,
) -> Interval:
    return Interval(Fraction(lower), Fraction(upper), lower_closed, upper_closed)


def _event(
    event_id: str,
    sequence: int,
    kind: str,
    key: str,
    event_type: str,
    timestamp: int,
    target: str | None = None,
) -> OwnershipEvent:
    return OwnershipEvent(
        event_id,
        sequence,
        kind,
        key,
        event_type,
        Fraction(timestamp),
        target,
    )


def _contract(
    *,
    policy: str = "UNIQUE-KEY",
    concurrent: bool = False,
    physical: Interval | None = None,
    requirement: Interval | None = None,
    clock_valid: bool = True,
    budget_valid: bool = True,
    authority: str = "REVIEWED",
    upper: int | None = 5,
    upper_closed: bool = True,
) -> InterpretationContract:
    effective_requirement = requirement or _interval(1, 5, upper_closed=upper_closed)
    if authority == "REVIEWED":
        deadline_identity: str | None = "reviewed:deadline:v1"
    elif authority == "METHOD-ONLY" and upper is not None:
        deadline_identity = "method:teaching-bound:v1"
    else:
        deadline_identity = None
    return InterpretationContract(
        contract_id="IC-TEST-V1",
        trigger_event_type="REQ",
        response_event_type="RESP",
        key="k",
        policy=policy,
        concurrent_same_key=concurrent,
        cancellation_event_type="CANCEL",
        supersession_event_type="SUPERSEDE",
        physical_domain=physical or _interval(-10, 10),
        requirement_window=effective_requirement,
        clock_identity="clock:test:v1",
        uncertainty_identity="uncertainty:test:v1",
        error_budget_identity="budget:test:v1",
        unit="tick",
        clock_valid=clock_valid,
        error_budget_valid=budget_valid,
        deadline_authority=authority,
        deadline_identity=deadline_identity,
        upper_bound=effective_requirement.upper if upper is not None else None,
        upper_closed=effective_requirement.upper_closed,
    )


def _input(
    events: tuple[OwnershipEvent, ...],
    *,
    trigger: str = "A",
    response: str | None = "R",
    measurement: Interval | None = None,
    tick: int | None = None,
    qualified: bool = True,
    earliest: int | None = 6,
    clock: str = "clock:test:v1",
    unit: str = "tick",
    uncertainty: str | None = "uncertainty:test:v1",
) -> ObservationInput:
    if response is None:
        raw = ObservationInput(
            events,
            trigger,
            None,
            None,
            qualified,
            None if earliest is None else Fraction(earliest),
            clock,
            unit,
        )
        return bind_observation_input(
            raw,
            execution_attempt_id="attempt:1",
            action_id="TEST",
            evidence_ref="evidence:1",
            measurement_tick=None,
            uncertainty_identity=None,
        )

    measurement = measurement or _interval(2, 3)
    if tick is None:
        assert measurement.lower_closed
        measurement_tick = measurement.lower
    else:
        measurement_tick = Fraction(tick)
    raw = ObservationInput(
        events,
        trigger,
        response,
        measurement,
        qualified,
        None if earliest is None else Fraction(earliest),
        clock,
        unit,
    )
    return bind_observation_input(
        raw,
        execution_attempt_id="attempt:1",
        action_id="TEST",
        evidence_ref="evidence:1",
        measurement_tick=measurement_tick,
        uncertainty_identity=uncertainty,
    )


def _normal_events() -> tuple[OwnershipEvent, ...]:
    return (
        _event("A", 1, "REQUEST", "k", "REQ", 0),
        _event("R", 2, "RESPONSE", "k", "RESP", 2),
    )


def _events_with_response_elapsed(elapsed: int) -> tuple[OwnershipEvent, ...]:
    """One owned response whose public event delta is ``elapsed`` ticks."""

    return (
        _event("A", 1, "REQUEST", "k", "REQ", 0),
        _event("R", 2, "RESPONSE", "k", "RESP", elapsed),
    )


def _raw_material_mapping() -> dict[str, object]:
    return {
        "events": [
            {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
            {"id": "R", "sequence": 2, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 2},
        ],
        "triggerEventId": "A",
        "responseId": "R",
        "measurementInterval": {"lower": 2, "upper": 3, "lowerClosed": True, "upperClosed": True},
        "observationEndQualified": True,
        "earliestElapsed": 6,
        "clockIdentity": "clock:test:v1",
        "unit": "tick",
    }


def _error_codes(result: object) -> set[str]:
    diagnostics = getattr(result, "diagnostics")
    return {item.code for item in diagnostics}


def test_raw_material_parser_rejects_injected_interpretation_fields() -> None:
    parsed = observation_input_from_mapping(_raw_material_mapping())
    assert parsed.execution_attempt_id is None
    assert parsed.action_id is None
    assert parsed.evidence_ref is None

    for injected in (
        "policy",
        "deadlineAuthority",
        "physicalDomain",
        "requirementWindow",
        "clockValid",
        "errorBudgetValid",
        "expectedVerdict",
    ):
        declaration = _raw_material_mapping()
        declaration[injected] = "fixture-must-not-control-this"
        with pytest.raises(ValueError, match="unknown or missing fields"):
            observation_input_from_mapping(declaration)


def test_bound_raw_material_and_controlled_contract_drive_matching_t5_pass() -> None:
    raw = observation_input_from_mapping(_raw_material_mapping())
    bound = bind_observation_input(
        raw,
        execution_attempt_id="attempt:1",
        action_id="TEST",
        evidence_ref="evidence:1",
        measurement_tick=Fraction(2),
        uncertainty_identity="uncertainty:test:v1",
    )
    result = assess_observation(bound, _contract())

    assert result.kind == "T5"
    assert result.verdict == "PASS"
    assert result.score_disposition == "ANSWERED"
    assert result.answered is True
    assert result.ownership is not None
    assert result.ownership.status == "UNIQUE"
    assert result.ownership.owner_request_id == "A"
    assert result.evidence_refs == ("R", "A")


def test_wrong_trigger_or_response_encoding_is_never_matched() -> None:
    wrong_trigger = _input(_normal_events(), trigger="R")
    trigger_result = assess_observation(wrong_trigger, _contract())
    assert trigger_result.verdict == "ERROR"
    assert "UNKNOWN-TRIGGER" in _error_codes(trigger_result)

    wrong_response_events = (
        _event("A", 1, "REQUEST", "k", "REQ", 0),
        _event("R", 2, "RESPONSE", "k", "OTHER", 2),
    )
    response_result = assess_observation(_input(wrong_response_events), _contract())
    assert response_result.verdict == "ERROR"
    assert "OWNERSHIP-ERROR" in _error_codes(response_result)


@pytest.mark.parametrize(
    ("policy", "first_owner", "second_owner"),
    (
        ("FIFO", "A", "B"),
        ("MOST-RECENT", "B", "A"),
    ),
)
def test_fifo_and_most_recent_assign_each_response_once(
    policy: str,
    first_owner: str,
    second_owner: str,
) -> None:
    events = (
        _event("A", 1, "REQUEST", "k", "REQ", 0),
        _event("B", 2, "REQUEST", "k", "REQ", 1),
        _event("R1", 3, "RESPONSE", "k", "RESP", 2),
        _event("R2", 4, "RESPONSE", "k", "RESP", 3),
    )
    replay = replay_ownership(events, _contract(policy=policy, concurrent=True))

    assert replay.diagnostics == ()
    assert replay.response_resolutions["R1"].owner_request_id == first_owner
    assert replay.response_resolutions["R2"].owner_request_id == second_owner
    assert replay.request_dispositions == {"A": "DISCHARGED", "B": "DISCHARGED"}


@pytest.mark.parametrize(
    ("policy", "expected_status", "expected_owner"),
    (
        ("FIFO", "UNIQUE", "B"),
        ("MOST-RECENT", "UNIQUE", "C"),
        ("UNIQUE-KEY", "AMBIGUOUS", None),
    ),
)
def test_incremental_replay_seeds_every_retained_active_request_for_ownership(
    policy: str,
    expected_status: str,
    expected_owner: str | None,
) -> None:
    """An incremental delta cannot select an owner by omitting B's receipt."""

    retained_b = _event("B", 2, "REQUEST", "k", "REQ", 0)
    delta = (
        _event("C", 4, "REQUEST", "k", "REQ", 0),
        _event("R2", 5, "RESPONSE", "k", "RESP", 0),
    )
    replay = replay_ownership(
        delta,
        _contract(policy=policy, concurrent=True, authority="METHOD-ONLY"),
        prior_active_requests={"B": retained_b},
    )
    resolution = replay.response_resolutions["R2"]
    assert replay.diagnostics == ()
    assert set(replay.event_refs) == {"C", "R2"}
    assert resolution.status == expected_status
    assert resolution.owner_request_id == expected_owner
    assert resolution.candidate_request_ids == ("B", "C")


def test_incremental_replay_accepts_an_exact_retained_request_reappearance_and_seed_cancellation() -> None:
    retained_b = _event("B", 2, "REQUEST", "k", "REQ", 0)
    contract = _contract(policy="FIFO", concurrent=True, authority="METHOD-ONLY")
    cumulative = replay_ownership(
        (
            _event("B", 2, "REQUEST", "k", "REQ", 0),
            _event("R2", 3, "RESPONSE", "k", "RESP", 0),
        ),
        contract,
        prior_active_requests={"B": retained_b},
    )
    assert cumulative.diagnostics == ()
    assert cumulative.response_resolutions["R2"].owner_request_id == "B"

    cancelled = replay_ownership(
        (_event("T", 3, "CANCEL", "k", "CANCEL", 0, "B"),),
        contract,
        prior_active_requests={"B": retained_b},
    )
    assert cancelled.diagnostics == ()
    assert cancelled.request_dispositions == {"B": "CANCELLED"}


def test_incremental_replay_rejects_changed_seed_identity_and_unordered_new_request() -> None:
    retained_b = _event("B", 2, "REQUEST", "k", "REQ", 0)
    contract = _contract(policy="FIFO", concurrent=True, authority="METHOD-ONLY")
    changed = replay_ownership(
        (_event("B", 2, "REQUEST", "k", "REQ", 1),),
        contract,
        prior_active_requests={"B": retained_b},
    )
    assert any(item.code == "OWNERSHIP-SEED-EVENT-CONFLICT" for item in changed.diagnostics)

    unordered = replay_ownership(
        (
            _event("C", 1, "REQUEST", "k", "REQ", 0),
            _event("R2", 3, "RESPONSE", "k", "RESP", 0),
        ),
        contract,
        prior_active_requests={"B": retained_b},
    )
    assert any(item.code == "INSUFFICIENT-OWNERSHIP-CONTEXT" for item in unordered.diagnostics)


@pytest.mark.parametrize(
    ("prior", "active"),
    (
        (
            (
                _event("A", 1, "REQUEST", "k", "REQ", 0),
                _event("B", 2, "REQUEST", "k", "REQ", 0),
                _event("R1", 10, "RESPONSE", "k", "RESP", 0),
            ),
            {"A": _event("A", 1, "REQUEST", "k", "REQ", 0)},
        ),
        (
            (
                _event("A", 1, "REQUEST", "k", "REQ", 0),
                _event("R1", 10, "RESPONSE", "k", "RESP", 0),
            ),
            {},
        ),
    ),
    ids=("retained-active", "no-retained-active"),
)
def test_incremental_replay_rejects_a_new_request_backfilled_before_the_processed_frontier(
    prior: tuple[OwnershipEvent, ...],
    active: dict[str, OwnershipEvent],
) -> None:
    """A later delta cannot revise an already processed response owner."""

    replay = replay_ownership(
        (
            _event("C", 3, "REQUEST", "k", "REQ", 0),
            _event("R2", 11, "RESPONSE", "k", "RESP", 0),
        ),
        _contract(policy="MOST-RECENT", concurrent=True, authority="METHOD-ONLY"),
        prior_active_requests=active,
        prior_order_boundary=OwnershipOrderBoundary(
            10,
            Fraction(0),
            frozenset(event.event_id for event in prior),
        ),
    )

    assert {item.code for item in replay.diagnostics} == {"INSUFFICIENT-OWNERSHIP-CONTEXT"}
    assert replay.request_dispositions == {}
    assert replay.response_resolutions == {}


@pytest.mark.parametrize(
    ("tail_sequence", "tail_kind", "tail_event_type"),
    (
        (12, "NOT-A-KIND", "INVALID"),
        (11, "REQUEST", "REQ"),
    ),
    ids=("invalid-kind", "duplicate-sequence"),
)
def test_incremental_replay_checks_a_valid_prefix_before_rejecting_a_malformed_tail(
    tail_sequence: int,
    tail_kind: str,
    tail_event_type: str,
) -> None:
    """A malformed later item cannot mask an earlier controlled backfill."""

    replay = replay_ownership(
        (
            _event("C", 3, "REQUEST", "k", "REQ", 0),
            _event("R2", 11, "RESPONSE", "k", "RESP", 0),
            _event("invalid-tail", tail_sequence, tail_kind, "k", tail_event_type, 0),
        ),
        _contract(policy="MOST-RECENT", concurrent=True, authority="METHOD-ONLY"),
        prior_order_boundary=OwnershipOrderBoundary(10, Fraction(0), frozenset({"A", "R1"})),
    )

    assert {item.code for item in replay.diagnostics} == {
        "INVALID-OWNERSHIP-EVENT",
        "INSUFFICIENT-OWNERSHIP-CONTEXT",
    }
    assert set(replay.event_refs) == {"C", "R2"}
    assert replay.request_dispositions == {}
    assert replay.response_resolutions == {}


def test_incremental_replay_enforces_global_sequence_timestamp_and_exact_active_rules() -> None:
    """The retained prefix has strict sequence but nondecreasing time order."""

    active_a = _event("A", 1, "REQUEST", "k", "REQ", 10)
    boundary = OwnershipOrderBoundary(10, Fraction(10), frozenset({"A", "R1"}))
    contract = _contract(policy="MOST-RECENT", concurrent=True, authority="METHOD-ONLY")

    equal_sequence = replay_ownership(
        (
            _event("C", 10, "REQUEST", "k", "REQ", 10),
            _event("R2", 11, "RESPONSE", "k", "RESP", 10),
        ),
        contract,
        prior_active_requests={"A": active_a},
        prior_order_boundary=boundary,
    )
    timestamp_backfill = replay_ownership(
        (
            _event("C", 11, "REQUEST", "k", "REQ", 9),
            _event("R2", 12, "RESPONSE", "k", "RESP", 9),
        ),
        contract,
        prior_active_requests={"A": active_a},
        prior_order_boundary=boundary,
    )
    legal_equal_timestamp = replay_ownership(
        (
            _event("C", 11, "REQUEST", "k", "REQ", 10),
            _event("R2", 12, "RESPONSE", "k", "RESP", 10),
        ),
        contract,
        prior_active_requests={"A": active_a},
        prior_order_boundary=boundary,
    )
    exact_active = replay_ownership(
        (
            _event("A", 1, "REQUEST", "k", "REQ", 10),
            _event("R3", 11, "RESPONSE", "k", "RESP", 10),
        ),
        contract,
        prior_active_requests={"A": active_a},
        prior_order_boundary=boundary,
    )

    assert all(
        {item.code for item in replay.diagnostics} == {"INSUFFICIENT-OWNERSHIP-CONTEXT"}
        for replay in (equal_sequence, timestamp_backfill)
    )
    assert legal_equal_timestamp.diagnostics == ()
    assert legal_equal_timestamp.response_resolutions["R2"].owner_request_id == "C"
    assert exact_active.diagnostics == ()
    assert exact_active.response_resolutions["R3"].owner_request_id == "A"


@pytest.mark.parametrize(
    ("kind", "event_type"),
    (("RESPONSE", "RESP"), ("CANCEL", "CANCEL"), ("SUPERSEDE", "SUPERSEDE")),
)
def test_incremental_replay_cannot_bypass_the_frontier_with_response_or_termination_kind(
    kind: str,
    event_type: str,
) -> None:
    active_a = _event("A", 1, "REQUEST", "k", "REQ", 0)
    boundary = OwnershipOrderBoundary(10, Fraction(0), frozenset({"A", "R1"}))
    target = None if kind == "RESPONSE" else "A"
    replay = replay_ownership(
        (_event("late", 9, kind, "k", event_type, 0, target),),
        _contract(policy="FIFO", concurrent=True, authority="METHOD-ONLY"),
        prior_active_requests={"A": active_a},
        prior_order_boundary=boundary,
    )

    assert {item.code for item in replay.diagnostics} == {"INSUFFICIENT-OWNERSHIP-CONTEXT"}


def test_incremental_replay_keeps_terminal_replay_distinct_from_an_active_confirmation() -> None:
    active_a = _event("A", 1, "REQUEST", "k", "REQ", 0)
    replay = replay_ownership(
        (_event("R1", 10, "RESPONSE", "k", "RESP", 0),),
        _contract(policy="FIFO", concurrent=True, authority="METHOD-ONLY"),
        prior_active_requests={"A": active_a},
        prior_order_boundary=OwnershipOrderBoundary(10, Fraction(0), frozenset({"A", "R1"})),
    )

    assert {item.code for item in replay.diagnostics} == {"RETAINED-OWNERSHIP-EVENT-REPLAY"}


@pytest.mark.parametrize(
    "boundary",
    (
        OwnershipOrderBoundary(0, Fraction(0), frozenset({"A"})),
        OwnershipOrderBoundary(1, Fraction(0), frozenset({""})),
    ),
    ids=("precedes-active-seed", "empty-retained-identity"),
)
def test_incremental_replay_rejects_an_invalid_order_boundary_without_throwing(
    boundary: OwnershipOrderBoundary,
) -> None:
    """Caller-supplied summaries cannot lower or fabricate the checked frontier."""

    replay = replay_ownership(
        (_event("R2", 2, "RESPONSE", "k", "RESP", 0),),
        _contract(policy="FIFO", concurrent=True, authority="METHOD-ONLY"),
        prior_active_requests={"A": _event("A", 1, "REQUEST", "k", "REQ", 0)},
        prior_order_boundary=boundary,
    )

    assert {item.code for item in replay.diagnostics} == {"INVALID-OWNERSHIP-ORDER-BOUNDARY"}
    assert replay.request_dispositions == {}
    assert replay.response_resolutions == {}


def test_assessment_uses_a_retained_incremental_trigger_for_the_measurement_delta() -> None:
    retained_b = _event("B", 2, "REQUEST", "k", "REQ", 0)
    result = assess_observation(
        _input(
            (_event("R2", 3, "RESPONSE", "k", "RESP", 2),),
            trigger="B", response="R2", measurement=_interval(2, 2), tick=2,
        ),
        _contract(policy="FIFO", concurrent=True, authority="METHOD-ONLY"),
        prior_active_requests={"B": retained_b},
    )
    assert result.verdict == "PASS"
    assert result.ownership is not None
    assert result.ownership.owner_request_id == "B"


@pytest.mark.parametrize(
    ("termination_kind", "termination_type"),
    (("CANCEL", "CANCEL"), ("SUPERSEDE", "SUPERSEDE")),
)
def test_incremental_no_response_uses_the_retained_trigger_for_a_timely_termination(
    termination_kind: str,
    termination_type: str,
) -> None:
    """A delta-only administrative event can close a retained reviewed obligation."""

    retained_b = _event("B", 2, "REQUEST", "k", "REQ", 0)
    result = assess_observation(
        _input(
            (_event("T", 3, termination_kind, "k", termination_type, 1, "B"),),
            trigger="B",
            response=None,
            earliest=6,
        ),
        _contract(policy="FIFO", concurrent=True, authority="REVIEWED"),
        prior_active_requests={"B": retained_b},
    )

    assert result.verdict == "INCONCLUSIVE"
    assert result.score_disposition == "NOT-APPLICABLE"
    assert result.answered is False
    assert result.diagnostics == ()
    assert result.evidence_refs == ("B", "T")


def test_unique_key_ambiguity_is_an_error_not_an_arbitrary_owner() -> None:
    events = (
        _event("A", 1, "REQUEST", "k", "REQ", 0),
        _event("B", 2, "REQUEST", "k", "REQ", 1),
        _event("R", 3, "RESPONSE", "k", "RESP", 2),
    )
    contract = _contract(concurrent=True)
    replay = replay_ownership(events, contract)
    assert replay.response_resolutions["R"].status == "AMBIGUOUS"
    assert replay.response_resolutions["R"].candidate_request_ids == ("A", "B")

    result = assess_observation(_input(events), contract)
    assert result.verdict == "ERROR"
    assert result.answered is False
    assert "OWNERSHIP-ERROR" in _error_codes(result)


def test_nonconcurrent_same_key_requires_an_explicit_supersession_target() -> None:
    events = (
        _event("A", 1, "REQUEST", "k", "REQ", 0),
        _event("B", 2, "REQUEST", "k", "REQ", 1),
        _event("R", 3, "RESPONSE", "k", "RESP", 2),
    )
    contract = _contract(concurrent=False)

    replay = replay_ownership(events, contract)
    assert {item.code for item in replay.diagnostics} == {"IMPLICIT-OWNERSHIP-SUPERSESSION"}

    result = assess_observation(_input(events), contract)
    assert result.verdict == "ERROR"
    assert "IMPLICIT-OWNERSHIP-SUPERSESSION" in _error_codes(result)


def test_nonconcurrent_replacement_must_target_a_currently_active_request() -> None:
    """A stale target cannot admit a second non-concurrent obligation."""

    stale = (
        _event("A", 1, "REQUEST", "k", "REQ", 0),
        _event("B", 2, "REQUEST", "k", "REQ", 1, "A"),
        _event("C", 3, "REQUEST", "k", "REQ", 2, "A"),
        _event("R", 4, "RESPONSE", "k", "RESP", 3),
    )
    contract = _contract(concurrent=False, authority="METHOD-ONLY")
    replay = replay_ownership(stale, contract)
    assert any(item.code == "INVALID-OWNERSHIP-TERMINATION" for item in replay.diagnostics)
    assert replay.request_dispositions == {"A": "SUPERSEDED", "B": "DISCHARGED"}
    assert "C" not in replay.request_dispositions

    rejected = assess_observation(
        _input(stale, trigger="B", measurement=_interval(2, 2), tick=2),
        contract,
    )
    assert rejected.verdict == "ERROR"
    assert "INVALID-OWNERSHIP-TERMINATION" in _error_codes(rejected)

    valid = (
        _event("A", 1, "REQUEST", "k", "REQ", 0),
        _event("B", 2, "REQUEST", "k", "REQ", 1, "A"),
        _event("C", 3, "REQUEST", "k", "REQ", 2, "B"),
        _event("R", 4, "RESPONSE", "k", "RESP", 3),
    )
    accepted = assess_observation(
        _input(valid, trigger="C", measurement=_interval(1, 1), tick=1),
        contract,
    )
    assert accepted.verdict == "PASS"
    assert accepted.ownership is not None
    assert accepted.ownership.owner_request_id == "C"


@pytest.mark.parametrize(
    ("termination_kind", "termination_type"),
    (("CANCEL", "CANCEL"), ("SUPERSEDE", "SUPERSEDE")),
)
def test_complete_foreign_key_termination_does_not_pollute_the_selected_contract(
    termination_kind: str,
    termination_type: str,
) -> None:
    """An unrelated complete transaction is not a malformed local one."""

    clean = (
        _event("A", 1, "REQUEST", "k", "REQ", 0),
        _event("R", 4, "RESPONSE", "k", "RESP", 2),
    )
    foreign = (
        _event("A", 1, "REQUEST", "k", "REQ", 0),
        _event("X", 2, "REQUEST", "other", "REQ", 1),
        _event("T", 3, termination_kind, "other", termination_type, 1, "X"),
        _event("R", 4, "RESPONSE", "k", "RESP", 2),
    )
    contract = _contract(authority="METHOD-ONLY")
    baseline = assess_observation(_input(clean, measurement=_interval(2, 2), tick=2), contract)
    result = assess_observation(_input(foreign, measurement=_interval(2, 2), tick=2), contract)

    assert baseline.verdict == result.verdict == "PASS"
    assert baseline.ownership is not None and result.ownership is not None
    assert result.ownership.owner_request_id == baseline.ownership.owner_request_id == "A"
    assert result.replay is not None
    assert result.replay.request_dispositions == {"A": "DISCHARGED"}
    assert result.replay.diagnostics == ()


@pytest.mark.parametrize(
    "events",
    (
        (
            _event("A", 1, "REQUEST", "k", "REQ", 0),
            _event("T", 2, "CANCEL", "other", "CANCEL", 1, "A"),
            _event("R", 3, "RESPONSE", "k", "RESP", 2),
        ),
        (
            _event("A", 1, "REQUEST", "k", "REQ", 0),
            _event("X", 2, "REQUEST", "other", "REQ", 1),
            _event("T", 3, "CANCEL", "k", "CANCEL", 2, "X"),
            _event("R", 4, "RESPONSE", "k", "RESP", 3),
        ),
        (
            _event("A", 1, "REQUEST", "k", "REQ", 0),
            _event("T", 2, "SUPERSEDE", "k", "WRONG", 1, "A"),
            _event("R", 3, "RESPONSE", "k", "RESP", 2),
        ),
    ),
)
def test_wrong_or_current_key_termination_still_rejects_the_contract_trace(
    events: tuple[OwnershipEvent, ...],
) -> None:
    result = assess_observation(
        _input(events, measurement=_interval(2, 2), tick=2),
        _contract(authority="METHOD-ONLY"),
    )
    assert result.verdict == "ERROR"
    assert "INVALID-OWNERSHIP-TERMINATION" in _error_codes(result)


@pytest.mark.parametrize(
    ("termination_kind", "termination_type"),
    (("CANCEL", "CANCEL"), ("SUPERSEDE", "SUPERSEDE")),
)
def test_foreign_key_termination_cannot_precede_its_future_controlled_target(
    termination_kind: str,
    termination_type: str,
) -> None:
    """A target is controlled even when its request appears later in the trace."""

    events = (
        _event("T", 1, termination_kind, "other", termination_type, 0, "A"),
        _event("A", 2, "REQUEST", "k", "REQ", 0),
        _event("R", 3, "RESPONSE", "k", "RESP", 0),
    )
    result = assess_observation(
        _input(events, measurement=_interval(0, 0), tick=0),
        _contract(authority="METHOD-ONLY"),
    )

    assert result.verdict == "ERROR"
    assert result.answered is False
    assert "INVALID-OWNERSHIP-TERMINATION" in _error_codes(result)


@pytest.mark.parametrize(
    "events",
    (
        (
            _event("A", 1, "REQUEST", "k", "REQ", 0),
            _event("A", 2, "REQUEST", "k", "REQ", 1),
        ),
        (
            _event("C", 1, "CANCEL", "k", "CANCEL", 0, "A"),
            _event("A", 2, "REQUEST", "k", "REQ", 1),
            _event("R", 3, "RESPONSE", "k", "RESP", 2),
        ),
        (
            _event("S", 1, "SUPERSEDE", "k", "SUPERSEDE", 0, "A"),
            _event("A", 2, "REQUEST", "k", "REQ", 1),
            _event("R", 3, "RESPONSE", "k", "RESP", 2),
        ),
    ),
)
def test_duplicate_trigger_or_future_termination_is_a_named_error(
    events: tuple[OwnershipEvent, ...],
) -> None:
    response = "R" if any(event.event_id == "R" for event in events) else None
    result = assess_observation(_input(events, response=response), _contract())
    assert result.verdict == "ERROR"
    assert result.answered is False
    assert result.diagnostics


@pytest.mark.parametrize(
    ("measurement", "requirement", "expected"),
    (
        (_interval(2, 3), _interval(1, 5), "PASS"),
        (_interval(6, 7), _interval(1, 5), "FAIL"),
        (_interval(4, 6), _interval(1, 5), "INCONCLUSIVE"),
        (_interval(5, 5), _interval(0, 5), "PASS"),
        (_interval(5, 5), _interval(0, 5, upper_closed=False), "FAIL"),
    ),
)
def test_t5_uses_entire_interval_with_closed_and_open_boundaries(
    measurement: Interval,
    requirement: Interval,
    expected: str,
) -> None:
    result = assess_observation(
        _input(
            _events_with_response_elapsed(
                measurement.lower.numerator // measurement.lower.denominator,
            ),
            measurement=measurement,
            tick=measurement.lower.numerator // measurement.lower.denominator,
        ),
        _contract(requirement=requirement),
    )
    assert result.verdict == expected
    assert result.answered is (expected in {"PASS", "FAIL"})
    if expected == "INCONCLUSIVE":
        assert result.score_disposition != "ANSWERED"


def test_t5_intersects_the_physical_domain_and_rejects_an_empty_one() -> None:
    result = assess_observation(
        _input(_events_with_response_elapsed(3), measurement=_interval(2, 4), tick=3),
        _contract(physical=_interval(3, 4), requirement=_interval(3, 5)),
    )
    assert result.verdict == "PASS"
    assert result.physical_interval == _interval(3, 4)

    empty = assess_observation(
        _input(_events_with_response_elapsed(3), measurement=_interval(2, 4), tick=3),
        _contract(physical=_interval(8, 9)),
    )
    assert empty.verdict == "ERROR"
    assert "EMPTY-PHYSICAL-MEASUREMENT-DOMAIN" in _error_codes(empty)


@pytest.mark.parametrize(
    "input_value,contract",
    (
        (_input(_normal_events(), clock="other-clock"), _contract()),
        (_input(_normal_events(), unit="ms"), _contract()),
        (_input(_normal_events(), uncertainty="other-uncertainty"), _contract()),
        (_input(_normal_events()), _contract(clock_valid=False)),
        (_input(_normal_events()), _contract(budget_valid=False)),
        (replace(_input(_normal_events()), measurement_interval=_interval(3, 2)), _contract()),
        (replace(_input(_normal_events()), measurement_tick=Fraction(99)), _contract()),
    ),
)
def test_t5_invalid_clock_unit_error_budget_or_measurement_is_error(
    input_value: ObservationInput,
    contract: InterpretationContract,
) -> None:
    result = assess_observation(input_value, contract)
    assert result.verdict == "ERROR"
    assert result.score_disposition == "ERROR"
    assert result.answered is False


@pytest.mark.parametrize(
    ("upper_closed", "earliest", "expected"),
    (
        (True, 5, "INCONCLUSIVE"),
        (True, 6, "FAIL"),
        (False, 5, "FAIL"),
    ),
)
def test_reviewed_no_response_requires_proven_expiry_and_respects_boundary_topology(
    upper_closed: bool,
    earliest: int,
    expected: str,
) -> None:
    events = (_event("A", 1, "REQUEST", "k", "REQ", 0),)
    result = assess_observation(
        _input(events, response=None, earliest=earliest),
        _contract(upper_closed=upper_closed),
    )
    assert result.kind == "NO-RESPONSE"
    assert result.verdict == expected
    assert result.answered is (expected == "FAIL")
    assert result.score_disposition == (
        "ANSWERED" if expected == "FAIL" else "PENDING-HORIZON"
    )


def test_no_response_requires_elapsed_only_after_the_horizon_is_needed() -> None:
    active = (_event("A", 1, "REQUEST", "k", "REQ", 0),)
    pending = assess_observation(
        _input(active, response=None, qualified=False, earliest=None),
        _contract(),
    )
    assert pending.verdict == "INCONCLUSIVE"
    assert pending.score_disposition == "PENDING-HORIZON"
    assert pending.answered is False

    cancelled = (
        _event("A", 1, "REQUEST", "k", "REQ", 0),
        _event("C", 2, "CANCEL", "k", "CANCEL", 1, "A"),
    )
    not_applicable = assess_observation(
        _input(cancelled, response=None, earliest=None),
        _contract(),
    )
    assert not_applicable.verdict == "INCONCLUSIVE"
    assert not_applicable.score_disposition == "NOT-APPLICABLE"
    assert not_applicable.answered is False

    missing_qualified_horizon = assess_observation(
        _input(active, response=None, qualified=True, earliest=None),
        _contract(),
    )
    assert missing_qualified_horizon.verdict == "ERROR"
    assert "INVALID-ELAPSED-HORIZON" in _error_codes(missing_qualified_horizon)


@pytest.mark.parametrize(
    ("termination_kind", "termination_type", "at_elapsed", "upper_closed", "earliest"),
    (
        ("CANCEL", "CANCEL", 6, True, 6),
        ("SUPERSEDE", "SUPERSEDE", 6, True, 6),
        # At an open upper boundary, cancellation is already too late to
        # suppress the established no-response failure.
        ("CANCEL", "CANCEL", 5, False, 5),
    ),
)
def test_postdeadline_termination_cannot_mask_reviewed_no_response_failure(
    termination_kind: str,
    termination_type: str,
    at_elapsed: int,
    upper_closed: bool,
    earliest: int,
) -> None:
    events = (
        _event("A", 1, "REQUEST", "k", "REQ", 0),
        _event("T", 2, termination_kind, "k", termination_type, at_elapsed, "A"),
    )
    requirement = _interval(1, 5, upper_closed=upper_closed)
    result = assess_observation(
        _input(events, response=None, earliest=earliest),
        _contract(requirement=requirement, upper_closed=upper_closed),
    )

    assert result.kind == "NO-RESPONSE"
    assert result.verdict == "FAIL"
    assert result.score_disposition == "ANSWERED"
    assert result.answered is True


def test_cancelled_or_superseded_obligation_cannot_receive_a_no_response_failure() -> None:
    cancelled = (
        _event("A", 1, "REQUEST", "k", "REQ", 0),
        _event("C", 2, "CANCEL", "k", "CANCEL", 1, "A"),
    )
    cancelled_result = assess_observation(
        _input(cancelled, response=None),
        _contract(),
    )
    assert cancelled_result.verdict == "INCONCLUSIVE"
    assert cancelled_result.score_disposition == "NOT-APPLICABLE"
    assert cancelled_result.answered is False

    superseded = (
        _event("A", 1, "REQUEST", "k", "REQ", 0),
        _event("B", 2, "REQUEST", "k", "REQ", 1, "A"),
    )
    superseded_result = assess_observation(
        _input(superseded, response=None),
        _contract(),
    )
    assert superseded_result.verdict == "INCONCLUSIVE"
    assert superseded_result.score_disposition == "NOT-APPLICABLE"


@pytest.mark.parametrize(
    ("termination_kind", "termination_type", "contract_kwargs", "expected_code"),
    (
        ("CANCEL", "CANCEL", {"clock_valid": False}, "INVALID-CLOCK-CHAIN"),
        ("CANCEL", "CANCEL", {"budget_valid": False}, "INVALID-ERROR-BUDGET"),
        ("SUPERSEDE", "SUPERSEDE", {"clock_valid": False}, "INVALID-CLOCK-CHAIN"),
        ("SUPERSEDE", "SUPERSEDE", {"budget_valid": False}, "INVALID-ERROR-BUDGET"),
    ),
)
def test_timestamped_termination_cannot_bypass_invalid_time_or_error_basis(
    termination_kind: str,
    termination_type: str,
    contract_kwargs: dict[str, bool],
    expected_code: str,
) -> None:
    events = (
        _event("A", 1, "REQUEST", "k", "REQ", 0),
        _event("T", 2, termination_kind, "k", termination_type, 1, "A"),
    )
    result = assess_observation(
        _input(events, response=None, earliest=6),
        _contract(**contract_kwargs),
    )
    assert result.verdict == "ERROR"
    assert result.score_disposition == "ERROR"
    assert expected_code in _error_codes(result)


@pytest.mark.parametrize(
    "contract",
    (
        replace(_contract(), upper_bound=Fraction(4)),
        replace(_contract(), upper_closed=False),
        replace(
            _contract(requirement=_interval(1, 5, upper_closed=False)),
            upper_bound=Fraction(4),
        ),
    ),
)
def test_deadline_boundary_must_match_the_requirement_window_upper_endpoint_and_closure(
    contract: InterpretationContract,
) -> None:
    result = assess_observation(_input(_normal_events()), contract)
    assert result.verdict == "ERROR"
    assert result.score_disposition == "ERROR"
    assert "INVALID-INTERPRETATION-CONTRACT" in _error_codes(result)


def test_method_only_silence_is_an_engineering_witness_and_does_not_hide_errors() -> None:
    events = (_event("A", 1, "REQUEST", "k", "REQ", 0),)
    result = assess_observation(
        _input(events, response=None, earliest=99),
        _contract(authority="METHOD-ONLY"),
    )
    assert result.verdict == "INCONCLUSIVE"
    assert result.score_disposition == "PENDING-DEADLINE"
    assert result.answered is False

    invalid_horizon = assess_observation(
        _input(events, response=None, earliest=-1),
        _contract(authority="METHOD-ONLY"),
    )
    assert invalid_horizon.verdict == "ERROR"
    assert "INVALID-ELAPSED-HORIZON" in _error_codes(invalid_horizon)

    invalid_clock = assess_observation(
        _input(events, response=None, earliest=99),
        _contract(authority="METHOD-ONLY", clock_valid=False),
    )
    assert invalid_clock.verdict == "ERROR"
    assert "INVALID-CLOCK-CHAIN" in _error_codes(invalid_clock)

    t5_witness = assess_observation(_input(_normal_events()), _contract(authority="METHOD-ONLY"))
    assert t5_witness.verdict == "PASS"
    assert t5_witness.score_disposition == "ENGINEERING-WITNESS"
    assert t5_witness.answered is False


def test_present_response_cannot_be_declared_as_silence() -> None:
    result = assess_observation(_input(_normal_events(), response=None), _contract())
    assert result.verdict == "ERROR"
    assert result.answered is False


def test_owned_measurement_tick_is_the_public_response_minus_trigger_delta() -> None:
    nonzero_origin = (
        _event("A", 1, "REQUEST", "k", "REQ", 7),
        _event("R", 2, "RESPONSE", "k", "RESP", 11),
    )
    equal_timestamp = (
        _event("A", 1, "REQUEST", "k", "REQ", 4),
        _event("R", 2, "RESPONSE", "k", "RESP", 4),
    )
    assert assess_observation(
        _input(nonzero_origin, measurement=_interval(4, 4), tick=4), _contract(requirement=_interval(0, 5)),
    ).verdict == "PASS"
    assert assess_observation(
        _input(equal_timestamp, measurement=_interval(0, 0), tick=0), _contract(requirement=_interval(0, 5)),
    ).verdict == "PASS"

    mismatch = assess_observation(
        _input(nonzero_origin, measurement=_interval(0, 0), tick=0), _contract(requirement=_interval(0, 5)),
    )
    assert mismatch.verdict == "ERROR"
    assert "MEASUREMENT-EVENT-DELTA-MISMATCH" in _error_codes(mismatch)


@pytest.mark.parametrize(
    ("policy", "trigger", "measurement_tick"),
    (("FIFO", "A", 2), ("MOST-RECENT", "B", 1)),
)
def test_measurement_event_delta_uses_the_owner_selected_by_the_controlled_policy(
    policy: str,
    trigger: str,
    measurement_tick: int,
) -> None:
    events = (
        _event("A", 1, "REQUEST", "k", "REQ", 0),
        _event("B", 2, "REQUEST", "k", "REQ", 1),
        _event("R", 3, "RESPONSE", "k", "RESP", 2),
    )
    contract = _contract(policy=policy, concurrent=True, requirement=_interval(0, 5))
    result = assess_observation(
        _input(events, trigger=trigger, measurement=_interval(measurement_tick, measurement_tick), tick=measurement_tick),
        contract,
    )
    assert result.verdict == "PASS"
    wrong = assess_observation(
        _input(events, trigger=trigger, measurement=_interval(0, 0), tick=0),
        contract,
    )
    assert wrong.verdict == "ERROR"
    assert "MEASUREMENT-EVENT-DELTA-MISMATCH" in _error_codes(wrong)


@pytest.mark.parametrize("bad_identity", (1, True, " ", object()))
def test_optional_deadline_identity_is_absent_or_a_nonblank_exact_string(
    bad_identity: object,
) -> None:
    contract = replace(_contract(authority="METHOD-ONLY", upper=None), deadline_identity=bad_identity)
    result = assess_observation(_input(_normal_events()), contract)
    assert result.verdict == "ERROR"
    assert "INVALID-INTERPRETATION-CONTRACT" in _error_codes(result)
    with pytest.raises(ValueError, match="invalid"):
        interpretation_contract_identity(contract)


@pytest.mark.parametrize(
    "malformed",
    (
        lambda value: replace(value, events=(value.events[0], object())),
        lambda value: replace(value, measurement_interval=object()),
        lambda value: replace(value, observation_end_qualified=1),
        lambda value: replace(value, earliest_elapsed=True),
    ),
)
def test_malformed_public_input_returns_a_named_error_not_an_exception(malformed) -> None:
    result = assess_observation(malformed(_input(_normal_events())), _contract())
    assert result.verdict == "ERROR"
    assert result.score_disposition == "ERROR"
    assert result.diagnostics


def test_every_public_result_uses_four_valued_verdict_and_derived_answered_invariant() -> None:
    normal = _normal_events()
    no_response = (_event("A", 1, "REQUEST", "k", "REQ", 0),)
    outcomes = (
        assess_observation(_input(normal), _contract()),
        assess_observation(_input(normal, measurement=_interval(6, 7), tick=6), _contract()),
        assess_observation(_input(normal, measurement=_interval(4, 6), tick=4), _contract()),
        assess_observation(_input(no_response, response=None, earliest=6), _contract()),
        assess_observation(_input(no_response, response=None, earliest=5), _contract()),
        assess_observation(replace(_input(normal), unit="bad"), _contract()),
        assess_observation(_input(normal), _contract(authority="METHOD-ONLY")),
    )
    for result in outcomes:
        assert result.verdict in {"PASS", "FAIL", "INCONCLUSIVE", "ERROR"}
        assert result.answered is (
            result.score_disposition == "ANSWERED" and result.verdict in {"PASS", "FAIL"}
        )
        if result.verdict == "INCONCLUSIVE":
            assert result.answered is False
