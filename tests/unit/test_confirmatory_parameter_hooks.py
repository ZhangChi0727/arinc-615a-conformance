"""Feasibility of parameterized faults: timing/presence/order only."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from a615a_sim.bound_iut.protocol import PROTOCOL_EVENT_WHITELIST, SimulatedTarget
from a615a_sim.clock import FIND_ANSWER_LATE_AT_S, FIND_HOST_ANSWER_S, SimulatedClock
from a615a_sim.evaluator import (
    get_truth,
    issue_truth_capability,
    new_independent_truth_store,
)
from a615a_sim.evaluator.reset import reset_target
from a615a_sim.faults.catalogue import harder_cases, parameter_axes
from a615a_sim.faults.injector import inject
from a615a_sim.faults.parameters import expand_arm_cells, expand_independent_units

ROOT = Path(__file__).resolve().parents[2]
DRAFT_CONFIG = ROOT / "configs/research/cltav_confirmatory_design_draft_v1.json"


def _target() -> SimulatedTarget:
    return SimulatedTarget(SimulatedClock())


def test_catalogue_declares_parameter_axes_and_harder_cases() -> None:
    axes = {axis["axisId"] for axis in parameter_axes()}
    assert axes == {
        "AX-BASE-SCENE",
        "AX-FIND-ANSWER-TICK",
        "AX-FIND-NORMAL-NEAR-BOUNDARY",
        "AX-STATUS-SILENCE-UNTIL",
        "AX-LUR-ACK-TICK",
        "AX-OBS-JITTER",
        "AX-FIND-OBS-END",
    }
    cases = {case["id"] for case in harder_cases()}
    assert "HC-FIND-ENDPOINT" in cases
    assert "HC-OBS-PERTURB-EPS" in cases
    for case in harder_cases():
        assert case["statementClass"] == "HYPOTHESIS-NOT-RESULT"
        assert case["visibleThrough"]


def test_parameterized_late_find_keeps_event_names_and_changes_tick() -> None:
    default = _target()
    reset_target(default)
    inject(default, scene_id="SC-NORMAL-UPLOAD", fault_id="F-FIND-ANSWER-LATE")
    parameterized = _target()
    reset_target(parameterized)
    inject(
        parameterized,
        scene_id="SC-NORMAL-UPLOAD",
        fault_id="F-FIND-ANSWER-LATE",
        parameters={"findAnswerAtS": "2002/1000"},
    )
    default_kinds = {event.kind for event in default.events}
    param_kinds = {event.kind for event in parameterized.events}
    assert default_kinds == param_kinds <= PROTOCOL_EVENT_WHITELIST
    default_answer = next(event for event in default.events if event.kind == "FIND-ANSWER")
    param_answer = next(event for event in parameterized.events if event.kind == "FIND-ANSWER")
    assert default_answer.tick == FIND_ANSWER_LATE_AT_S
    assert param_answer.tick == Fraction("2002/1000")
    assert param_answer.tick > FIND_HOST_ANSWER_S


def test_observation_jitter_shifts_interval_only() -> None:
    target = _target()
    reset_target(target)
    inject(
        target,
        scene_id="SC-NORMAL-UPLOAD",
        fault_id="F-FIND-ANSWER-LATE",
        parameters={"observationJitterS": "1/500"},
    )
    visible = target.algorithm_visible_records()
    assert {row["kind"] for row in visible} <= PROTOCOL_EVENT_WHITELIST
    answer = next(row for row in visible if row["kind"] == "FIND-ANSWER")
    assert "tick" not in answer
    raw = next(event for event in target.events if event.kind == "FIND-ANSWER")
    interval = target.clock.observation_interval(raw.tick)
    assert answer["observationInterval"]["lower"] == str(interval.lower + Fraction(1, 500))
    assert answer["observationInterval"]["upper"] == str(interval.upper + Fraction(1, 500))
    assert answer["kind"] == "FIND-ANSWER"


def test_visible_records_omit_exact_tick() -> None:
    target = _target()
    reset_target(target)
    inject(target, scene_id="SC-NORMAL-UPLOAD", fault_id="H-NORMAL")
    for record in target.algorithm_visible_records():
        assert "tick" not in record
        assert "observationInterval" in record
    timed = target.evaluator_timed_records()
    assert timed
    assert all("tick" in row for row in timed)


def test_jitter_changes_arm_visible_interval() -> None:
    def _answer_interval(jitter: str) -> tuple[str, str]:
        target = _target()
        reset_target(target)
        inject(
            target,
            scene_id="SC-NORMAL-UPLOAD",
            fault_id="F-FIND-ANSWER-LATE",
            parameters={"observationJitterS": jitter},
        )
        answer = next(
            row for row in target.algorithm_visible_records() if row["kind"] == "FIND-ANSWER"
        )
        assert "tick" not in answer
        interval = answer["observationInterval"]
        return interval["lower"], interval["upper"]

    minus = _answer_interval("-1/500")
    plus = _answer_interval("1/500")
    none = _answer_interval("0")
    assert minus != plus
    assert minus != none
    assert plus != none


def test_absent_short_window_omits_find_answer_without_new_kind() -> None:
    target = _target()
    reset_target(target)
    attempt = inject(
        target,
        scene_id="SC-NORMAL-UPLOAD",
        fault_id="F-FIND-ANSWER-ABSENT",
        parameters={"findObservationEndS": "2"},
    )
    kinds = [event.kind for event in target.events]
    assert kinds == ["FIND-REQUEST-RECEIVED"]
    assert "FIND-ANSWER-ABSENT" not in kinds
    assert attempt.injection_confirmed is True


def test_delayed_lur_ack_remains_present() -> None:
    target = _target()
    reset_target(target)
    inject(
        target,
        scene_id="SC-NORMAL-UPLOAD",
        fault_id="H-NORMAL",
        parameters={"lurAckAtS": "1"},
    )
    kinds = [event.kind for event in target.events]
    assert "LUR-WRQ" in kinds and "LUR-ACK" in kinds
    ack = next(event for event in target.events if event.kind == "LUR-ACK")
    assert ack.tick == Fraction(1)


def test_truth_access_unchanged_with_parameters() -> None:
    capability = issue_truth_capability()
    store = new_independent_truth_store()
    target = _target()
    reset_target(target)
    attempt = inject(
        target,
        scene_id="SC-NORMAL-UPLOAD",
        fault_id="F-FIND-ANSWER-LATE",
        parameters={"findAnswerAtS": "41/20"},
        truth_store=store,
        truth_capability=capability,
    )
    assert attempt.injection_confirmed is True
    record = get_truth(store, attempt.attempt_id, capability)
    assert record.attempt_id == attempt.attempt_id
    assert record.confirmation_ref == f"INJ-{attempt.attempt_id}"


def test_injector_rejects_parameters_that_do_not_match_fault() -> None:
    target = _target()
    reset_target(target)
    with pytest.raises(ValueError, match="do not match fault H-NORMAL"):
        inject(
            target,
            scene_id="SC-NORMAL-UPLOAD",
            fault_id="H-NORMAL",
            parameters={"findAnswerAtS": "41/20"},
        )


def test_draft_units_are_labelled_and_do_not_run() -> None:
    units = expand_independent_units()
    assert units
    assert all(unit["label"].startswith("DRAFT") for unit in units)
    assert all("/CL-" not in unit["unitId"] for unit in units)


def test_draft_config_is_marked_draft_and_matches_expander() -> None:
    payload = json.loads(DRAFT_CONFIG.read_text(encoding="utf-8"))
    assert payload["identity"]["status"] == "DRAFT"
    assert payload["identity"]["confirmatoryRegistration"] is False
    assert payload["identity"]["registrationYaml"] is False
    assert payload["sample"]["decSample"] == "OPEN"
    assert payload["openDecisions"] == [
        "DEC-TRUTH",
        "DEC-CLOCK",
        "DEC-EQUIV",
        "DEC-SAMPLE",
        "DEC-RESOURCE",
    ]
    cells = expand_arm_cells()
    assert payload["cellCount"] == len(cells) == len(payload["cells"])
    assert payload["unitCount"] == len(expand_independent_units())
    assert payload["cells"][0]["label"].startswith("DRAFT")
