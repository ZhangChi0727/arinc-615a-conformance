"""Drive E0–E6 in the registered walkthrough order."""

from __future__ import annotations

from typing import Any, Mapping

from a615a_sim.bound_iut.protocol import SimulatedTarget
from a615a_sim.clock import SimulatedClock
from a615a_sim.evaluator.guard import deny_algorithm_truth_access
from a615a_sim.evaluator.pipeline.collect import collect_from_fixture, collect_from_run
from a615a_sim.evaluator.pipeline.design import (
    load_experiment_design,
    load_synthetic_walkthrough,
    walkthrough_for_workflow,
)
from a615a_sim.evaluator.pipeline.evaluate import assemble_attempt_row, evaluate_with_store, metric_cells
from a615a_sim.evaluator.pipeline.filter import filter_attempt, filter_from_fixture
from a615a_sim.evaluator.pipeline.inject_stage import inject_mapping, run_inject
from a615a_sim.evaluator.pipeline.run import replay_run_fixture, run_registered_arm
from a615a_sim.evaluator.pipeline.scene import build_scene_record
from a615a_sim.evaluator.pipeline.truth_stage import write_truth_if_confirmed
from a615a_sim.evaluator.reset import reset_target
from a615a_sim.evaluator.truth import IndependentTruthStore, TruthCapability
from a615a_sim.faults.injector import overlay_declared_fault

WF_PATHS = {
    "WF-NORMAL": [
        "IF-EXP-SCENE",
        "IF-EXP-INJECT",
        "IF-EXP-TRUTH",
        "IF-EXP-RUN",
        "IF-EXP-COLLECT",
        "IF-EXP-FILTER",
        "IF-EXP-EVAL",
    ],
    "WF-UNCONFIRMED-INJECT": ["IF-EXP-SCENE", "IF-EXP-INJECT", "IF-EXP-FILTER", "IF-EXP-EVAL"],
    "WF-INVALID-OBS": [
        "IF-EXP-SCENE",
        "IF-EXP-INJECT",
        "IF-EXP-TRUTH",
        "IF-EXP-RUN",
        "IF-EXP-COLLECT",
        "IF-EXP-FILTER",
        "IF-EXP-EVAL",
    ],
    "WF-ABSTAIN": [
        "IF-EXP-SCENE",
        "IF-EXP-INJECT",
        "IF-EXP-TRUTH",
        "IF-EXP-RUN",
        "IF-EXP-COLLECT",
        "IF-EXP-FILTER",
        "IF-EXP-EVAL",
    ],
    "WF-EQUIVALENT": [
        "IF-EXP-SCENE",
        "IF-EXP-INJECT",
        "IF-EXP-TRUTH",
        "IF-EXP-FILTER",
        "IF-EXP-EVAL",
    ],
}


def execute_synthetic_walkthrough(workflow_id: str) -> dict[str, Any]:
    """Replay one WF-* path against the mapped SYN-* fixture.  Not a live result."""

    deny_algorithm_truth_access(operation="walkthrough")
    fixture = walkthrough_for_workflow(workflow_id)
    path = WF_PATHS[workflow_id]
    resource_mode = fixture.get("resourcePolicy") or "ROUNDS"
    if resource_mode == "NOT-RUN":
        resource_mode = "BUDGET"
    scene = build_scene_record(
        scene_id=fixture["scenarioId"],
        arm_id=fixture["armId"],
        resource_mode=resource_mode,
        pairing_id=fixture.get("pairingId"),
        reset_evidence_ref=fixture.get("resetEvidenceRef"),
        requirement_interval=fixture.get("requirementInterval"),
        extra={"baseSceneId": fixture.get("baseSceneId"), "sceneSeed": fixture.get("sceneSeed")},
    )
    injection = {
        "sceneId": fixture["scenarioId"],
        "attemptId": fixture["attemptId"],
        "injectionConfirmed": fixture["injectionStatus"] not in {"UNCONFIRMED"},
        "injectionUnconfirmed": fixture["injectionStatus"] == "UNCONFIRMED",
        "producer": "IF-EXP-INJECT",
    }
    truth = None
    run = None
    collect = None
    if "IF-EXP-TRUTH" in path:
        truth = {
            "truthHypothesis": fixture["truthReference"]["truthHypothesis"],
            "injectionStatus": fixture["injectionStatus"],
            "faultDomain": fixture["faultDomain"],
            "equivalentFault": fixture["injectionStatus"] == "EQUIVALENT",
            "producer": "IF-EXP-TRUTH",
        }
    if "IF-EXP-RUN" in path:
        run = replay_run_fixture(fixture)
    if "IF-EXP-COLLECT" in path:
        collect = collect_from_fixture(fixture)
    filtered = filter_from_fixture(fixture, collect or {})
    row = assemble_attempt_row(
        fixture=fixture,
        scene=scene,
        injection=injection,
        truth=truth,
        run=run,
        collect=collect,
        filtered=filtered,
    )
    return {
        "workflowId": workflow_id,
        "path": path,
        "sceneRecord": scene,
        "injectionAttempt": injection,
        "truthRecord": truth,
        "runRecord": run,
        "collectRecord": collect,
        "filterRecord": filtered,
        "attemptRow": row,
        "label": "SYNTHETIC-DESIGN-WALKTHROUGH",
    }


def execute_live_attempt(
    *,
    scene_id: str,
    fault_id: str,
    arm_id: str,
    resource_mode: str,
    remaining: int,
    capability: TruthCapability,
    store: IndependentTruthStore,
    confirm: bool = True,
    pairing_id: str = "PAIR-PHASE-C",
) -> dict[str, Any]:
    """Live SCENE→INJECT/TRUTH→RUN→COLLECT→FILTER→EVAL on the simulated IUT."""

    deny_algorithm_truth_access(operation="live-pipeline")
    target = SimulatedTarget(SimulatedClock())
    scene = build_scene_record(
        scene_id=scene_id,
        arm_id=arm_id,
        resource_mode=resource_mode,
        fault_plan=fault_id,
        pairing_id=pairing_id,
    )
    reset_target(target, pairing_id=pairing_id)
    attempt = run_inject(
        target,
        scene_id=scene_id,
        fault_id=fault_id,
        confirm=confirm,
    )
    injection = inject_mapping(attempt)
    truth_map = None
    if attempt.injection_confirmed:
        truth_map = write_truth_if_confirmed(store, attempt, capability)
        reset_target(target, pairing_id=pairing_id)
        overlay_declared_fault(target, scene_id=scene_id, fault_id=fault_id)
    else:
        filtered = filter_attempt(
            variant="pre-run-exclusion",
            injection_unconfirmed=True,
        )
        row = assemble_attempt_row(
            scene=scene,
            injection=injection,
            truth=None,
            run=None,
            collect=None,
            filtered=filtered,
        )
        return {
            "path": WF_PATHS["WF-UNCONFIRMED-INJECT"],
            "sceneRecord": scene,
            "injectionAttempt": injection,
            "filterRecord": filtered,
            "attemptRow": row,
            "metricCells": metric_cells([row]),
            "label": "SIMULATED-IUT",
        }
    run = run_registered_arm(
        target,
        scene_id=scene_id,
        arm_id=arm_id,
        resource_mode=resource_mode,
        remaining=remaining,
        correlation_id=f"{arm_id}-{attempt.attempt_id}",
    )
    collect = collect_from_run(run, resource_mode=resource_mode)
    filtered = filter_attempt(
        variant="run-completed",
        missing_correlation=bool(collect["missingCorrelation"]),
        stop_class=run["stopClass"],
        action_issued=run["actionIssued"],
        resource_status=collect["resourceLog"]["statusClass"],
        run_id=run["runId"],
    )
    row = evaluate_with_store(
        store,
        attempt.attempt_id,
        capability,
        scene=scene,
        injection=injection,
        run=run,
        collect=collect,
        filtered=filtered,
    )
    return {
        "path": WF_PATHS["WF-NORMAL"],
        "sceneRecord": scene,
        "injectionAttempt": injection,
        "truthRecord": truth_map,
        "runRecord": run,
        "collectRecord": collect,
        "filterRecord": filtered,
        "attemptRow": row,
        "metricCells": metric_cells([row]),
        "label": "SIMULATED-IUT",
    }


__all__ = [
    "WF_PATHS",
    "execute_live_attempt",
    "execute_synthetic_walkthrough",
    "load_experiment_design",
    "load_synthetic_walkthrough",
    "metric_cells",
]
