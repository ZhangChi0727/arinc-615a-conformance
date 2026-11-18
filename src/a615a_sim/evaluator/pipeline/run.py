"""E3 IF-EXP-RUN.  No IF-EXP-TRUTH access."""

from __future__ import annotations

from typing import Any, Mapping

from a615a_sim.algorithm.adapter import run_arm
from a615a_sim.algorithm.library import ArmRun
from a615a_sim.bound_iut.protocol import SimulatedTarget


def run_registered_arm(
    target: SimulatedTarget,
    *,
    scene_id: str,
    arm_id: str,
    resource_mode: str,
    remaining: int,
    correlation_id: str,
    run_id: str | None = None,
) -> dict[str, Any]:
    """Execute one arm.  Evaluator truth tokens are not parameters."""

    arm_run: ArmRun = run_arm(
        arm_id,
        target,
        scene_id=scene_id,
        resource_mode=resource_mode,
        remaining=remaining,
        correlation_id=correlation_id,
    )
    mapping = arm_run.as_mapping()
    issued = list(arm_run.issued_actions)
    hypotheses = list(arm_run.candidate_hypotheses)
    localization = bool(hypotheses) and arm_run.stop_class not in {
        "Stop-Error",
        "Stop-Empty",
        "Stop-645",
        "Stop-Budget",
    }
    singleton = localization and len(hypotheses) == 1 and arm_run.stop_class == "Stop-Singleton"
    if not issued and arm_run.stop_class == "Stop-Budget":
        stage = "PRE-ACTION"
    elif arm_run.stop_class in {"Stop-Empty", "Stop-645"}:
        stage = "POST-UPDATE"
    else:
        stage = "TERMINAL"
    return {
        "runId": run_id or f"RUN-{correlation_id}",
        "sceneId": scene_id,
        "armId": arm_id,
        "stopClass": arm_run.stop_class,
        "stage": stage,
        "traceRef": mapping,
        "finalHypotheses": hypotheses,
        "localizationDecisionIssued": localization,
        "singletonDecisionIssued": singleton,
        "actionIssued": bool(issued),
        "issuedActions": issued,
        "t5Verdicts": list(arm_run.t5_verdicts),
        "observationLog": list(arm_run.observation_log),
        "detailCharges": dict(arm_run.detail_charges),
        "chargedCost": arm_run.projected_cost(),
        "resourceMode": arm_run.resource_mode,
        "producer": "IF-EXP-RUN",
        "label": "SIMULATED-IUT",
    }


def replay_run_fixture(row: Mapping[str, Any]) -> dict[str, Any]:
    """Replay a synthetic walkthrough RUN record.  Does not read truth."""

    return {
        "runId": row.get("runId"),
        "sceneId": row.get("scenarioId"),
        "armId": row.get("armId"),
        "stopClass": row.get("stopClass"),
        "traceRef": {
            "finalHypotheses": list(row.get("finalHypotheses") or []),
            "stopClass": row.get("stopClass"),
            "stage": row.get("stage"),
        },
        "finalHypotheses": list(row.get("finalHypotheses") or []),
        "localizationDecisionIssued": bool(row.get("localizationDecisionIssued")),
        "singletonDecisionIssued": bool(row.get("singletonDecisionIssued")),
        "actionIssued": bool(row.get("actionIssued")),
        "historyBefore": list(row.get("historyBefore") or []),
        "compatibleState": list(row.get("compatibleState") or []),
        "stage": row.get("stage"),
        "producer": "IF-EXP-RUN",
        "label": "SIMULATED-IUT",
    }
