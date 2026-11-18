"""Feasibility tests for the DRAFT confirmatory design parameter hooks.

These tests do not run a census or confirmatory experiment.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from a615a_sim.bound_iut.protocol import PROTOCOL_EVENT_WHITELIST, SimulatedTarget
from a615a_sim.clock import (
    FIND_HOST_ANSWER_S,
    SIMULATED_EPSILON,
    SimulatedClock,
    find_host_requirement,
    t5_interval_verdict,
)
from a615a_sim.faults.catalogue import harder_cases, h_single_entries, parameter_axes
from a615a_sim.faults.injector import inject
from a615a_sim.faults.parameters import ARMS, expand_arm_cells, expand_independent_units


ROOT = Path(__file__).resolve().parents[2]
DESIGN_PATH = ROOT / "configs" / "research" / "cltav_confirmatory_design_draft_v1.json"


def _target() -> SimulatedTarget:
    return SimulatedTarget(SimulatedClock())


def test_h_single_identities_unchanged() -> None:
    assert {entry["id"] for entry in h_single_entries()} == {
        "F-FIND-ANSWER-LATE",
        "F-FIND-ANSWER-ABSENT",
        "F-LUR-ACK-MISSING",
        "F-LUR-ACK-WITHOUT-WRQ",
        "F-STATUS-SILENCE",
    }


def test_parameter_axes_and_harder_cases_are_declared() -> None:
    axis_ids = {axis["axisId"] for axis in parameter_axes()}
    assert axis_ids == {
        "AX-BASE-SCENE",
        "AX-FIND-ANSWER-TICK",
        "AX-FIND-NORMAL-NEAR-BOUNDARY",
        "AX-STATUS-SILENCE-UNTIL",
        "AX-LUR-ACK-TICK",
        "AX-OBS-JITTER",
        "AX-FIND-OBS-END",
    }
    case_ids = {case["id"] for case in harder_cases()}
    assert "HC-FIND-ENDPOINT" in case_ids
    assert "HC-LATE-ABSENT-SHORT-WINDOW" in case_ids
    for case in harder_cases():
        assert case["statementClass"] == "HYPOTHESIS-NOT-RESULT"
        assert set(case["hypothesisStress"]) == set(ARMS)


def test_parameterized_late_answer_keeps_find_answer_event() -> None:
    tick = Fraction(2002, 1000)
    attempt = inject(
        _target(),
        scene_id="SC-NORMAL-UPLOAD",
        fault_id="F-FIND-ANSWER-LATE",
        parameters={"findAnswerAtS": tick},
    )
    assert attempt.injection_confirmed
    assert attempt.observed_signature == "FIND-ANSWER-LATE"
    target = _target()
    inject(
        target,
        scene_id="SC-NORMAL-UPLOAD",
        fault_id="F-FIND-ANSWER-LATE",
        parameters={"findAnswerAtS": tick},
    )
    kinds = {event.kind for event in target.events}
    assert kinds <= PROTOCOL_EVENT_WHITELIST
    assert "FIND-ANSWER" in kinds
    answer = next(event for event in target.events if event.kind == "FIND-ANSWER")
    assert answer.tick == tick
    interval = target.clock.observation_interval(answer.tick)
    assert t5_interval_verdict(interval, find_host_requirement()) == "FAIL"


def test_endpoint_tick_is_not_a_confirmed_late_signature() -> None:
    attempt = inject(
        _target(),
        scene_id="SC-NORMAL-UPLOAD",
        fault_id="F-FIND-ANSWER-LATE",
        parameters={"findAnswerAtS": Fraction(2, 1)},
    )
    assert attempt.injection_unconfirmed
    target = _target()
    inject(
        target,
        scene_id="SC-NORMAL-UPLOAD",
        fault_id="F-FIND-ANSWER-LATE",
        parameters={"findAnswerAtS": Fraction(2, 1)},
    )
    answer = next(event for event in target.events if event.kind == "FIND-ANSWER")
    verdict = t5_interval_verdict(
        target.clock.observation_interval(answer.tick), find_host_requirement()
    )
    assert verdict == "INCONCLUSIVE"
    assert answer.tick == FIND_HOST_ANSWER_S


def test_observation_jitter_is_visible_only_as_interval_shift() -> None:
    jitter = 2 * SIMULATED_EPSILON
    target = _target()
    inject(
        target,
        scene_id="SC-NORMAL-UPLOAD",
        fault_id="F-FIND-ANSWER-LATE",
        parameters={"observationJitterS": jitter},
    )
    visible = target.algorithm_visible_records()
    answer = next(row for row in visible if row["kind"] == "FIND-ANSWER")
    raw = next(event for event in target.events if event.kind == "FIND-ANSWER")
    unshifted = target.clock.observation_interval(raw.tick)
    assert "tick" not in answer
    assert answer["kind"] == "FIND-ANSWER"
    assert Fraction(answer["observationInterval"]["lower"]) == unshifted.lower + jitter
    assert Fraction(answer["observationInterval"]["upper"]) == unshifted.upper + jitter


def test_delayed_ack_preserves_lur_ack_event() -> None:
    target = _target()
    inject(
        target,
        scene_id="SC-NORMAL-UPLOAD",
        fault_id="H-NORMAL",
        parameters={"lurAckAtS": Fraction(1, 5)},
    )
    kinds = [event.kind for event in target.events]
    assert "LUR-WRQ" in kinds and "LUR-ACK" in kinds
    ack = next(event for event in target.events if event.kind == "LUR-ACK")
    assert ack.tick >= Fraction(1, 5)


def test_short_observation_end_absent_uses_existing_kinds() -> None:
    target = _target()
    attempt = inject(
        target,
        scene_id="SC-ABORT",
        fault_id="F-FIND-ANSWER-ABSENT",
        parameters={"findObservationEndS": Fraction(2, 1)},
    )
    assert attempt.injection_confirmed
    assert {event.kind for event in target.events} <= PROTOCOL_EVENT_WHITELIST
    assert not any(event.kind == "FIND-ANSWER" for event in target.events)
    assert target.clock.now == Fraction(2, 1)


def test_draft_design_json_matches_expander_and_stays_draft() -> None:
    payload = json.loads(DESIGN_PATH.read_text(encoding="utf-8"))
    assert payload["identity"]["status"] == "DRAFT"
    assert payload["identity"]["confirmatoryRegistration"] is False
    assert payload["identity"]["label"] == "DRAFT / SIMULATED-IUT / HYPOTHETICAL-NOT-RESULT"
    assert payload["identity"]["userDecisionS1"]["decClock"] == "OPEN"
    assert payload["identity"]["userDecisionS1"]["implements"].startswith("C1")
    units = expand_independent_units()
    cells = expand_arm_cells()
    assert payload["cellCount"] == len(cells) == len(payload["cells"])
    assert payload["unitCount"] == len(units)
    assert {cell["cellId"] for cell in payload["cells"]} == {cell["cellId"] for cell in cells}
    assert all(cell["armId"] in ARMS for cell in cells)
    assert payload["openDecisions"] == [
        "DEC-TRUTH",
        "DEC-CLOCK",
        "DEC-EQUIV",
        "DEC-SAMPLE",
        "DEC-RESOURCE",
    ]


def test_visible_find_answer_has_no_tick() -> None:
    target = _target()
    inject(target, scene_id="SC-NORMAL-UPLOAD", fault_id="H-NORMAL")
    for record in target.algorithm_visible_records():
        assert "tick" not in record
        assert "observationInterval" in record


def test_injector_rejects_late_answer_parameter_under_h_normal() -> None:
    with pytest.raises(ValueError, match="do not match fault H-NORMAL"):
        inject(
            _target(),
            scene_id="SC-NORMAL-UPLOAD",
            fault_id="H-NORMAL",
            parameters={"findAnswerAtS": "41/20"},
        )
