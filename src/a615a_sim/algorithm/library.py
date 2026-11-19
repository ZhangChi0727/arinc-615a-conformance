"""Shared action library, fair cost table, stop names, and predetermined sequences.

Authority: EXP-PLAN-2026-001 fair-cost table; experiment design arms[];
EXPERIMENT_IMPLEMENTATION_SPEC arm visibility table and T5 oracle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Mapping

from a615a_sim.clock import ClosedInterval, find_host_requirement, t5_interval_verdict

REGISTERED_ARMS = ("CL-T", "CL-A", "CL-TA", "CL-LOOP")
RESOURCE_MODES = frozenset({"ROUNDS", "BUDGET"})
STOP_CLASSES = frozenset(
    {
        "Stop-Empty",
        "Stop-Singleton",
        "Stop-645",
        "Stop-Equivalent",
        "Stop-Budget",
        "Stop-Error",
        "Stop-NoDistinguisher",
        "Stop-Round-Limit",
        "Stop-Prediction-Gap",
        "Stop-SpecError",
    }
)

ACTION_TEST_FIND = "TEST-FIND"
ACTION_TEST_SEND = "TEST-SEND"
ACTION_TEST_ABORT = "TEST-ABORT"
ACTION_TEST_INFORMATION = "TEST-INFORMATION"
ACTION_ANALYSIS = "ANALYSIS"
ACTION_PREP = "PREP"
ACTION_RECOVER = "RECOVER"

ACTION_LIBRARY = (
    ACTION_TEST_FIND,
    ACTION_TEST_SEND,
    ACTION_TEST_ABORT,
    ACTION_TEST_INFORMATION,
    ACTION_ANALYSIS,
    ACTION_PREP,
    ACTION_RECOVER,
)

TEST_ACTIONS = frozenset(
    {ACTION_TEST_FIND, ACTION_TEST_SEND, ACTION_TEST_ABORT, ACTION_TEST_INFORMATION}
)

# Same action type has the same price on every arm.  Unexecuted actions are not
# charged.  Recovery folds into preparation once at projection time.
FAIR_DETAIL_CHARGES: Mapping[str, Mapping[str, int]] = {
    ACTION_TEST_FIND: {
        "acquisition": 1,
        "computation": 0,
        "preparation": 0,
        "recovery": 0,
        "retry": 0,
    },
    ACTION_TEST_SEND: {
        "acquisition": 1,
        "computation": 0,
        "preparation": 0,
        "recovery": 0,
        "retry": 0,
    },
    ACTION_TEST_ABORT: {
        "acquisition": 1,
        "computation": 0,
        "preparation": 0,
        "recovery": 0,
        "retry": 0,
    },
    ACTION_TEST_INFORMATION: {
        "acquisition": 1,
        "computation": 0,
        "preparation": 0,
        "recovery": 0,
        "retry": 0,
    },
    ACTION_ANALYSIS: {
        "acquisition": 0,
        "computation": 1,
        "preparation": 0,
        "recovery": 0,
        "retry": 0,
    },
    ACTION_PREP: {
        "acquisition": 0,
        "computation": 0,
        "preparation": 1,
        "recovery": 0,
        "retry": 0,
    },
    ACTION_RECOVER: {
        "acquisition": 0,
        "computation": 0,
        "preparation": 0,
        "recovery": 1,
        "retry": 0,
    },
}

ARM_COST_COMPONENTS = {
    "CL-T": frozenset({"acquisition", "preparation", "retry"}),
    "CL-A": frozenset({"computation"}),
    "CL-TA": frozenset({"acquisition", "computation", "preparation", "retry"}),
    "CL-LOOP": frozenset({"acquisition", "computation", "preparation", "retry"}),
}

EMPTY_DETAIL = {
    "acquisition": 0,
    "computation": 0,
    "preparation": 0,
    "recovery": 0,
    "retry": 0,
}

INITIAL_VISIBLE_FIELDS = (
    "sceneId",
    "serviceScope",
    "registeredArm",
    "resourceMode",
    "publicConfigurationRef",
)

UPLOAD_SCENES = frozenset(
    {"SC-NORMAL-UPLOAD", "SC-WAIT-CONTINUE", "SC-ABORT", "SC-SINGLE-BATCH"}
)
INFORMATION_SCENES = frozenset(
    {"SC-NO-RESPONSE", "SC-INVALID-OBS", "SC-SAME-KEY", "SC-RESOURCE-ERROR"}
)


def service_scope_for_scene(scene_id: str) -> str:
    if scene_id in UPLOAD_SCENES:
        return "UPLOAD"
    if scene_id in INFORMATION_SCENES:
        return "INFORMATION"
    raise KeyError(scene_id)


def algorithm_visible_initial(
    *,
    scene_id: str,
    registered_arm: str,
    resource_mode: str,
    public_configuration_ref: str = "SIMULATED-IUT-BOUND-MODEL",
) -> dict[str, str]:
    if registered_arm not in REGISTERED_ARMS:
        raise ValueError(f"unknown arm {registered_arm}")
    if resource_mode not in RESOURCE_MODES:
        raise ValueError(f"unknown resource mode {resource_mode}")
    return {
        "sceneId": scene_id,
        "serviceScope": service_scope_for_scene(scene_id),
        "registeredArm": registered_arm,
        "resourceMode": resource_mode,
        "publicConfigurationRef": public_configuration_ref,
    }


def predetermined_test_sequence(initial: Mapping[str, str]) -> tuple[str, ...]:
    """Frozen TEST sequence from ALGORITHM-INITIAL fields only."""

    scope = initial["serviceScope"]
    if scope == "UPLOAD":
        return (ACTION_TEST_FIND, ACTION_TEST_SEND)
    if scope == "INFORMATION":
        return (ACTION_TEST_INFORMATION,)
    raise ValueError(f"unknown serviceScope {scope}")


def action_cost(action_id: str) -> int:
    detail = FAIR_DETAIL_CHARGES[action_id]
    return max(1, sum(detail.values()))


def project_cost(detail: Mapping[str, int]) -> dict[str, int]:
    return {
        "acquisition": detail["acquisition"],
        "computation": detail["computation"],
        "preparation": detail["preparation"] + detail["recovery"],
        "retry": detail["retry"],
    }


def t5_on_visible(record: Mapping[str, Any]) -> str | None:
    """T5 oracle on algorithm-visible FIND-ANSWER intervals.  Not a truth read."""

    if record.get("kind") != "FIND-ANSWER":
        return None
    interval = record["observationInterval"]
    observation = ClosedInterval(_as_fraction(interval["lower"]), _as_fraction(interval["upper"]))
    return t5_interval_verdict(observation, find_host_requirement())


def _as_fraction(value: object) -> Fraction:
    return Fraction(str(value))


@dataclass
class ExclusiveResource:
    mode: str
    remaining: int

    def __post_init__(self) -> None:
        if self.mode not in RESOURCE_MODES:
            raise ValueError("one exclusive resource mode per run")
        if self.remaining < 0:
            raise ValueError("resource remaining must be nonnegative")

    def need(self, action_id: str) -> int:
        return 1 if self.mode == "ROUNDS" else action_cost(action_id)

    def can_afford(self, action_id: str) -> bool:
        return self.remaining >= self.need(action_id)

    def charge(self, action_id: str) -> None:
        if not self.can_afford(action_id):
            raise ValueError("unaffordable action cannot be charged")
        self.remaining -= self.need(action_id)


@dataclass
class ArmRun:
    arm_id: str
    issued_actions: list[str] = field(default_factory=list)
    observation_log: list[dict[str, Any]] = field(default_factory=list)
    detail_charges: dict[str, int] = field(default_factory=lambda: dict(EMPTY_DETAIL))
    stop_class: str = "Stop-Error"
    resource_mode: str = "ROUNDS"
    resource_remaining: int = 0
    t5_verdicts: list[str] = field(default_factory=list)
    runtime_session_type: str | None = None
    runtime_binding_sha: str | None = None
    candidate_hypotheses: list[str] = field(default_factory=list)
    analysis_notes: dict[str, Any] = field(default_factory=dict)

    def charge_action(self, action_id: str) -> None:
        if action_id not in ACTION_LIBRARY:
            raise ValueError(f"action {action_id} is not in the shared library")
        for key, amount in FAIR_DETAIL_CHARGES[action_id].items():
            self.detail_charges[key] += amount
        self.issued_actions.append(action_id)

    def projected_cost(self) -> dict[str, int]:
        return project_cost(self.detail_charges)

    def as_mapping(self) -> dict[str, Any]:
        return {
            "armId": self.arm_id,
            "issuedActions": list(self.issued_actions),
            "observationLog": list(self.observation_log),
            "chargedCost": self.projected_cost(),
            "detailCharges": dict(self.detail_charges),
            "stopClass": self.stop_class,
            "resourceMode": self.resource_mode,
            "resourceRemaining": self.resource_remaining,
            "t5Verdicts": list(self.t5_verdicts),
            "runtimeSessionType": self.runtime_session_type,
            "runtimeBindingSha": self.runtime_binding_sha,
            "candidateHypotheses": list(self.candidate_hypotheses),
            "analysisNotes": dict(self.analysis_notes),
            "label": "SIMULATED-IUT",
        }
