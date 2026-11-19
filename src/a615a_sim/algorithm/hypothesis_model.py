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
    FIND_ANSWER_NORMAL_AT_S,
    SIMULATED_EPSILON,
    find_host_requirement,
    t5_interval_verdict,
)
from a615a_sim.faults.catalogue import harder_cases, parameter_axes

_ROOT = Path(__file__).resolve().parents[3]
MODEL_PATH = _ROOT / "configs/research/cltav_pilot_hypothesis_model_v1.json"
MODEL_V2_PATH = _ROOT / "configs/research/cltav_confirmatory_hypothesis_model_v2.json"
IDENTIFICATION_STOP = "Stop-Singleton"  # RR-006 N5.5: identification stop; no alias.
SCENE_TERMINAL_SEND = frozenset({"COMPLETED", "WAIT", "CONTINUE", "ABORT"})  # N5.1 LUR-COMPLETE.
FIND_ANSWER_BOUNDARY = "FIND-ANSWER-BOUNDARY"
VARIANT_NORMAL_NEAR_BOUNDARY = "h_normal@near-boundary"
VARIANT_LATE_BOUNDARY = "h_find_answer_late@boundary"
VARIANT_LATE_CLEAR = "h_find_answer_late@clear"


def _require_hypothesis_ids(payload: Mapping[str, Any], *, version: str) -> None:
    ids = tuple(payload["hypothesisIds"])
    if ids[0] != "h_normal":
        raise ValueError("h_normal must be the first registered hypothesis")
    if "h_find_answer_late" not in ids or "h_find_answer_absent" not in ids:
        raise ValueError("LATE and ABSENT must remain two hypotheses")
    if version == "2":
        if VARIANT_NORMAL_NEAR_BOUNDARY not in ids or VARIANT_LATE_BOUNDARY not in ids:
            raise ValueError("v2 must split FIND boundary variants from the catalogue grid")


def find_interval_class(tick: Fraction, jitter: Fraction = Fraction(0, 1)) -> str:
    """T5 class of tick ± ε + jitter versus CRS-M1-00391 [0, 2]."""

    interval = ClosedInterval(
        tick - SIMULATED_EPSILON + jitter, tick + SIMULATED_EPSILON + jitter
    )
    verdict = t5_interval_verdict(interval, find_host_requirement())
    if verdict == "PASS":
        return "FIND-ANSWER"
    if verdict == "FAIL":
        return "FIND-ANSWER-LATE"
    return FIND_ANSWER_BOUNDARY


def _axis_values(axis_id: str) -> tuple[Mapping[str, Any], ...]:
    for axis in parameter_axes():
        if axis["axisId"] == axis_id:
            return tuple(axis["values"])
    raise KeyError(axis_id)


def _tick_from_mapping(value: Mapping[str, Any], key: str) -> Fraction | None:
    raw = value.get(key)
    if raw is None:
        return None
    return Fraction(str(raw))


def grid_find_parameter_classes() -> dict[str, dict[str, Any]]:
    """Group catalogue FIND ticks by T5 class.  One class per parent fault."""

    classes: dict[str, dict[str, Any]] = {
        "h_normal:FIND-ANSWER": {
            "parent": "h_normal",
            "variant": "h_normal",
            "observable": "FIND-ANSWER",
            "tick": FIND_ANSWER_NORMAL_AT_S,
            "source": "default-normal",
        }
    }
    for value in _axis_values("AX-FIND-NORMAL-NEAR-BOUNDARY"):
        tick = _tick_from_mapping(value, "findAnswerAtS")
        if tick is None:
            continue
        observed = find_interval_class(tick)
        key = f"h_normal:{observed}"
        classes.setdefault(
            key,
            {
                "parent": "h_normal",
                "variant": VARIANT_NORMAL_NEAR_BOUNDARY if observed == FIND_ANSWER_BOUNDARY else "h_normal",
                "observable": observed,
                "tick": tick,
                "source": value["id"],
            },
        )
    for value in _axis_values("AX-FIND-ANSWER-TICK"):
        tick = _tick_from_mapping(value, "findAnswerAtS")
        if tick is None:
            continue
        observed = find_interval_class(tick)
        variant = VARIANT_LATE_CLEAR if observed == "FIND-ANSWER-LATE" else VARIANT_LATE_BOUNDARY
        if observed == "FIND-ANSWER":
            variant = "h_find_answer_late"
        key = f"h_find_answer_late:{observed}"
        classes.setdefault(
            key,
            {
                "parent": "h_find_answer_late",
                "variant": "h_find_answer_late" if observed == "FIND-ANSWER-LATE" else variant,
                "observable": observed,
                "tick": tick,
                "source": value["id"],
            },
        )
    for case in harder_cases():
        tick = _tick_from_mapping(case.get("parameters") or {}, "findAnswerAtS")
        if tick is None:
            continue
        parent_fault = str(case.get("parentFaultId") or "")
        parent = "h_find_answer_late" if parent_fault == "F-FIND-ANSWER-LATE" else "h_normal"
        if parent_fault not in {"F-FIND-ANSWER-LATE", "H-NORMAL"}:
            continue
        observed = find_interval_class(tick)
        if parent == "h_find_answer_late" and observed == FIND_ANSWER_BOUNDARY:
            variant = VARIANT_LATE_BOUNDARY
        elif parent == "h_normal" and observed == FIND_ANSWER_BOUNDARY:
            variant = VARIANT_NORMAL_NEAR_BOUNDARY
        elif parent == "h_find_answer_late":
            variant = "h_find_answer_late"
        else:
            variant = "h_normal"
        key = f"{parent}:{observed}"
        classes.setdefault(
            key,
            {
                "parent": parent,
                "variant": variant,
                "observable": observed,
                "tick": tick,
                "source": case["id"],
            },
        )
    return classes


def parent_hypothesis(hypothesis_id: str) -> str:
    table = load_confirmatory_hypothesis_model_v2()["parentByVariant"]
    return str(table.get(hypothesis_id, hypothesis_id))


def map_to_parent_hypotheses(hypothesis_ids: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    """Evaluator mapping: variants collapse to catalogue parent hypotheses."""

    parents: list[str] = []
    for identifier in hypothesis_ids:
        parent = parent_hypothesis(identifier)
        if parent not in parents:
            parents.append(parent)
    return tuple(parents)


@lru_cache(maxsize=1)
def load_pilot_hypothesis_model() -> Mapping[str, Any]:
    payload = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    if payload["identity"]["version"] != "1":
        raise ValueError("pilot hypothesis model version is not 1")
    _require_hypothesis_ids(payload, version="1")
    return payload


@lru_cache(maxsize=1)
def load_confirmatory_hypothesis_model_v2() -> Mapping[str, Any]:
    payload = json.loads(MODEL_V2_PATH.read_text(encoding="utf-8"))
    if payload["identity"]["version"] != "2":
        raise ValueError("confirmatory hypothesis model version is not 2")
    _require_hypothesis_ids(payload, version="2")
    return payload


def public_hypothesis_ids() -> tuple[str, ...]:
    return tuple(load_pilot_hypothesis_model()["hypothesisIds"])


def confirmatory_hypothesis_ids() -> tuple[str, ...]:
    return tuple(load_confirmatory_hypothesis_model_v2()["hypothesisIds"])


def _fraction_tick(tick: Fraction) -> dict[str, int]:
    return {"numerator": int(tick.numerator), "positiveDenominator": int(tick.denominator)}


def _copy_action_row(source: Mapping[str, Any], *, observable: str | None = None, tick: Fraction | None = None) -> dict[str, Any]:
    row = dict(source)
    if observable is not None:
        row["observable"] = observable
        row["present"] = observable != "FIND-REQUEST-RECEIVED"
    if tick is not None:
        row["measurementTick"] = _fraction_tick(tick)
    return row


def build_confirmatory_hypothesis_model_v2() -> dict[str, Any]:
    """Split v1 parents by catalogue FIND parameter class.  v1 file is not written."""

    v1 = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    classes = grid_find_parameter_classes()
    parent_ids = list(v1["hypothesisIds"])
    hypothesis_ids: list[str] = []
    for parent in parent_ids:
        hypothesis_ids.append(parent)
        for item in classes.values():
            variant = str(item["variant"])
            if item["parent"] == parent and variant != parent and variant not in hypothesis_ids:
                hypothesis_ids.append(variant)
    parent_by_variant = {identifier: identifier for identifier in hypothesis_ids}
    for item in classes.values():
        parent_by_variant[str(item["variant"])] = str(item["parent"])

    actions: dict[str, Any] = {}
    for action_id, table in v1["actions"].items():
        action_table: dict[str, Any] = {}
        for hypothesis in hypothesis_ids:
            parent = parent_by_variant[hypothesis]
            base = dict(table[parent])
            if action_id == ACTION_TEST_FIND and hypothesis in {VARIANT_NORMAL_NEAR_BOUNDARY, VARIANT_LATE_BOUNDARY}:
                item = next(row for row in classes.values() if row["variant"] == hypothesis)
                action_table[hypothesis] = _copy_action_row(
                    base, observable=str(item["observable"]), tick=item["tick"]
                )
            else:
                action_table[hypothesis] = _copy_action_row(base)
        actions[action_id] = action_table

    return {
        "identity": {
            "artifactId": "CLTAV-CONFIRMATORY-HYPOTHESIS-MODEL",
            "version": "2",
            "status": "DRAFT",
            "changeRequest": "CR-2026-028",
            "authority": "RR-PR29-2026-002 B1: split hypotheses by fault x parameter class from the catalogue grid. S1 interval classification retained. Pilot v1 unchanged.",
            "catalogueId": "CLTAV-H-SINGLE-SIMULATED-2026-010-B1",
            "label": "SIMULATED-IUT",
            "pilotInterfaceNote": "Pilot census artefacts were produced against the v1 tick-classified interface and are not regenerated here.",
        },
        "hypothesisIds": hypothesis_ids,
        "parentByVariant": parent_by_variant,
        "observationClasses": list(v1.get("observationClasses") or []) or [
            "FIND-ANSWER",
            "FIND-ANSWER-LATE",
            FIND_ANSWER_BOUNDARY,
            "FIND-REQUEST-RECEIVED",
            "LUR-COMPLETE",
            "LUR-WRQ",
            "LUR-ACK",
            "ABORT",
            "COMPLETED",
            "STATUS",
        ],
        "intervalRule": {
            "source": "EXP-PLAN-2026-001 T5; clock.t5_interval_verdict; CRS-M1-00391 closed [0, 2]",
            "contained": "FIND-ANSWER (in window)",
            "disjoint": "FIND-ANSWER-LATE",
            "partialOverlap": FIND_ANSWER_BOUNDARY,
            "note": "FIND-ANSWER-BOUNDARY is an observation class, not a protocol event name. Variants are generated from the catalogue grid.",
        },
        "parameterClasses": {
            key: {
                "parent": item["parent"],
                "variant": item["variant"],
                "observable": item["observable"],
                "measurementTick": str(item["tick"]),
                "source": item["source"],
            }
            for key, item in classes.items()
        },
        "actions": actions,
        "notes": [
            "Pilot hypothesis model v1 is unmodified.",
            "v2 splits FIND hypotheses by T5 interval class on the catalogue grid.",
            "h_normal@near-boundary and h_find_answer_late@boundary both emit FIND-ANSWER-BOUNDARY so a boundary observation retains both parents after evaluator mapping.",
            "The evaluator table parentByVariant maps variants to catalogue parents for truth retention, singleton scoring, and R1.",
            "LATE and ABSENT remain two parent hypotheses (DEC-EQUIV OPEN).",
        ],
    }


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
            "frontierStates": 16,
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
