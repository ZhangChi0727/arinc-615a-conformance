"""Pilot hypothesis model and consistency filter.  Public catalogue fields only."""

from __future__ import annotations

import json
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

from a615a_sim.algorithm.library import (
    ACTION_TEST_ABORT,
    ACTION_TEST_FIND,
    ACTION_TEST_INFORMATION,
    ACTION_TEST_SEND,
    FAIR_DETAIL_CHARGES,
    STOP_CLASSES,
    TEST_ACTIONS,
    ArmRun,
)
from a615a_sim.clock import (
    ClosedInterval,
    find_host_requirement,
    t5_interval_verdict,
)

_ROOT = Path(__file__).resolve().parents[3]
MODEL_PATH = _ROOT / "configs/research/cltav_pilot_hypothesis_model_v1.json"
MODEL_V2_PATH = _ROOT / "configs/research/cltav_confirmatory_hypothesis_model_v2.json"
IDENTIFICATION_STOP = "Stop-Singleton"  # RR-006 N5.5: identification stop; no alias.
SCENE_TERMINAL_SEND = frozenset({"COMPLETED", "WAIT", "CONTINUE", "ABORT"})  # N5.1 LUR-COMPLETE.
FIND_ANSWER_BOUNDARY = "FIND-ANSWER-BOUNDARY"


def _require_hypothesis_ids(payload: Mapping[str, Any]) -> None:
    ids = tuple(payload["hypothesisIds"])
    if ids[0] != "h_normal":
        raise ValueError("h_normal must be the first registered hypothesis")
    if "h_find_answer_late" not in ids or "h_find_answer_absent" not in ids:
        raise ValueError("LATE and ABSENT must remain two hypotheses")


@lru_cache(maxsize=1)
def load_pilot_hypothesis_model() -> Mapping[str, Any]:
    payload = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    if payload["identity"]["version"] != "1":
        raise ValueError("pilot hypothesis model version is not 1")
    _require_hypothesis_ids(payload)
    return payload


@lru_cache(maxsize=1)
def load_confirmatory_hypothesis_model_v2() -> Mapping[str, Any]:
    payload = json.loads(MODEL_V2_PATH.read_text(encoding="utf-8"))
    if payload["identity"]["version"] != "2":
        raise ValueError("confirmatory hypothesis model version is not 2")
    _require_hypothesis_ids(payload)
    return payload


def public_hypothesis_ids() -> tuple[str, ...]:
    return tuple(load_pilot_hypothesis_model()["hypothesisIds"])


def _observation_interval(record: Mapping[str, Any]) -> ClosedInterval:
    interval = record["observationInterval"]
    return ClosedInterval(Fraction(str(interval["lower"])), Fraction(str(interval["upper"])))


def classify_observable(action_id: str, record: Mapping[str, Any]) -> str:
    """Map one algorithm-visible record onto a registered observation class.

    FIND-ANSWER uses the T5 interval rule on the visible observationInterval
    versus CRS-M1-00391 [0, 2].  FIND-ANSWER-BOUNDARY is an observation class,
    not a protocol event name.
    """

    kind = str(record["kind"])
    if action_id == ACTION_TEST_FIND and kind == "FIND-ANSWER":
        verdict = t5_interval_verdict(_observation_interval(record), find_host_requirement())
        if verdict == "PASS":
            return "FIND-ANSWER"
        if verdict == "FAIL":
            return "FIND-ANSWER-LATE"
        return FIND_ANSWER_BOUNDARY
    if action_id == ACTION_TEST_SEND:
        if kind in SCENE_TERMINAL_SEND:
            return "LUR-COMPLETE"
        return kind
    return kind


def consistent_hypotheses(
    issued_actions: list[str],
    observation_log: list[Mapping[str, Any]],
) -> tuple[str, ...]:
    """Retain hypotheses compatible with this arm's visible TEST records only."""

    model = load_confirmatory_hypothesis_model_v2()
    remaining = list(model["hypothesisIds"])
    records = iter(observation_log)
    table = model["actions"]
    for action_id in issued_actions:
        if action_id not in TEST_ACTIONS:
            continue
        try:
            record = next(records)
        except StopIteration:
            break
        observed = classify_observable(action_id, record)
        action_table = table[action_id]
        remaining = [
            hypothesis
            for hypothesis in remaining
            if action_table[hypothesis]["observable"] == observed
        ]
    return tuple(remaining)


def declare_arm_result(run: ArmRun, *, session_stop: str | None = None) -> ArmRun:
    """Attach the candidate set and a registered stop class."""

    run.candidate_hypotheses = list(consistent_hypotheses(run.issued_actions, run.observation_log))
    budgeted = run.stop_class == "Stop-Budget"
    if budgeted:
        return run
    if session_stop and session_stop not in STOP_CLASSES:
        raise ValueError(f"unregistered stop class {session_stop}")
    if len(run.candidate_hypotheses) == 1:
        run.stop_class = IDENTIFICATION_STOP
        return run
    if run.arm_id == "CL-LOOP" and session_stop in STOP_CLASSES:
        run.stop_class = session_stop
        return run
    run.stop_class = "Stop-NoDistinguisher"
    return run


def _hypothesis_row(identifier: str) -> dict[str, object]:
    return {
        "id": identifier,
        "controlStateId": "q0",
        "clockConstraint": {
            "x": {
                "lower": {"numerator": 0, "positiveDenominator": 1},
                "upper": {"numerator": 0, "positiveDenominator": 1},
                "lowerClosed": True,
                "upperClosed": True,
            }
        },
        "typedStore": {"mode": "normal"},
    }


def _test_action(action_id: str, emissions: dict[str, str], ticks: dict[str, Mapping[str, int]]) -> dict[str, object]:
    detail = dict(FAIR_DETAIL_CHARGES[action_id])
    return {
        "id": action_id,
        "kind": "TEST",
        "cost": max(1, sum(detail.values())),
        "detailCharges": detail,
        "enabledSummaries": ["q0"],
        "transition": {
            "id": f"tr-{action_id}",
            "source": "q0",
            "target": "q0",
            "guardAst": {"tag": "TRUE"},
            "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q0"}],
        },
        "observableByHypothesis": emissions,
        "measurementTicksByHypothesis": ticks,
    }


def experiment_session_model() -> dict[str, object]:
    payload = load_confirmatory_hypothesis_model_v2()
    hyps = tuple(payload["hypothesisIds"])
    actions = []
    for action_id in (
        ACTION_TEST_FIND,
        ACTION_TEST_SEND,
        ACTION_TEST_ABORT,
        ACTION_TEST_INFORMATION,
    ):
        table = payload["actions"][action_id]
        emissions = {hyp: table[hyp]["observable"] for hyp in hyps}
        ticks = {hyp: table[hyp]["measurementTick"] for hyp in hyps}
        actions.append(_test_action(action_id, emissions, ticks))
    return {
        "model": {
            "stateIds": ["q0"],
            "clockIds": ["x"],
            "typedDomains": {"mode": ["normal"]},
        },
        "hypotheses": [_hypothesis_row(hyp) for hyp in hyps],
        "actions": actions,
        "limits": {
            "pathLength": 4,
            "frontierStates": 8,
            "hypotheses": len(hyps),
            "actions": 4,
            "observationClasses": 10,
        },
        "uncertainty": {
            "id": "sim-iut-u-1",
            "clockId": "x",
            "timeUnit": "ticks",
            "maximumErrorTicks": 12,
        },
    }
