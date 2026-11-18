"""Drive E0–E6 in the registered walkthrough order."""

from __future__ import annotations

from typing import Any, Mapping

from a615a_sim.bound_iut.protocol import SimulatedTarget
from a615a_sim.clock import SimulatedClock
from a615a_sim.evaluator.guard import deny_algorithm_truth_access
from a615a_sim.evaluator.pipeline.collect import collect_from_run
from a615a_sim.evaluator.pipeline.design import (
    WF_TO_SYN,
    load_experiment_design,
    load_synthetic_walkthrough,
    walkthrough_for_workflow,
)
from a615a_sim.evaluator import issue_truth_capability, new_independent_truth_store
from a615a_sim.evaluator.pipeline.evaluate import (
    UndefinedDetectionOutcome,
    assemble_attempt_row,
    evaluate_with_store,
    metric_cells,
)
from a615a_sim.evaluator.pipeline.filter import filter_attempt
from a615a_sim.evaluator.pipeline.inject_stage import inject_mapping, run_inject
from a615a_sim.evaluator.pipeline.run import run_registered_arm
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

SCENE_FAULT = {
    "SC-NORMAL-UPLOAD": "H-NORMAL",
    "SC-WAIT-CONTINUE": "H-NORMAL",
    "SC-ABORT": "H-NORMAL",
    "SC-SINGLE-BATCH": "H-NORMAL",
    "SC-INVALID-OBS": "H-INVALID-OBS",
    "SC-RESOURCE-ERROR": "H-RESOURCE-ERROR",
    "SC-SAME-KEY": "H-SAME-KEY",
    "SC-NO-RESPONSE": "F-STATUS-SILENCE",
}

COMPARE_FIELDS = (
    "scenarioId",
    "armId",
    "validity",
    "outcome",
    "stopClass",
    "finalHypotheses",
    "injectionStatus",
    "faultDomain",
    "localizationDecisionIssued",
    "singletonDecisionIssued",
    "resourcePolicy",
    "resourceStatus",
    "actionIssued",
    "runId",
    "attemptId",
    "stage",
)


def _syn_mismatches(actual: Mapping[str, Any], expected: Mapping[str, Any]) -> list[dict[str, Any]]:
    mismatches = []
    for key in COMPARE_FIELDS:
        got = actual.get(key)
        want = expected.get(key)
        if key == "finalHypotheses" and got != want:
            mismatches.append({"field": key, "expected": want, "produced": got})
        elif key != "finalHypotheses" and got != want:
            mismatches.append({"field": key, "expected": want, "produced": got})
    want_h = (expected.get("truthReference") or {}).get("truthHypothesis")
    got_h = (actual.get("truthReference") or {}).get("truthHypothesis")
    if got_h != want_h:
        mismatches.append(
            {
                "field": "truthReference.truthHypothesis",
                "expected": want_h,
                "produced": got_h,
            }
        )
    return mismatches


def execute_synthetic_walkthrough(workflow_id: str) -> dict[str, Any]:
    """Live SCENE→INJECT/TRUTH→RUN→COLLECT→FILTER→EVAL compared with SYN-*."""

    deny_algorithm_truth_access(operation="walkthrough")
    fixture = walkthrough_for_workflow(workflow_id)
    confirm = fixture["injectionStatus"] != "UNCONFIRMED"
    resource_mode = fixture.get("resourcePolicy") or "ROUNDS"
    if resource_mode not in {"ROUNDS", "BUDGET"}:
        resource_mode = "ROUNDS"
    capability = issue_truth_capability()
    store = new_independent_truth_store()
    live = execute_live_attempt(
        scene_id=fixture["scenarioId"],
        fault_id=SCENE_FAULT[fixture["scenarioId"]],
        arm_id=fixture["armId"],
        resource_mode=resource_mode,
        remaining=8,
        capability=capability,
        store=store,
        confirm=confirm,
        pairing_id="PAIR-PHASE-C",
        attempt_id=f"A-{workflow_id}",
    )
    live["workflowId"] = workflow_id
    live["synId"] = WF_TO_SYN[workflow_id]
    live["registeredPath"] = WF_PATHS[workflow_id]
    row = live.get("attemptRow") or {}
    live["synComparison"] = _syn_mismatches(row, fixture)
    if live.get("undefinedDetectionOutcome"):
        live["synComparison"].insert(
            0,
            {
                "field": "outcome",
                "expected": fixture.get("outcome"),
                "produced": None,
                "undefinedDetectionOutcome": live["undefinedDetectionOutcome"],
            },
        )
    live["label"] = "SIMULATED-IUT"
    return live


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
    attempt_id: str | None = None,
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
        attempt_id=attempt_id,
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
        stage=run.get("stage"),
        action_issued=run["actionIssued"],
        resource_status=collect["resourceLog"]["statusClass"],
        run_id=run["runId"],
    )
    try:
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
    except UndefinedDetectionOutcome as exc:
        return {
            "path": WF_PATHS["WF-NORMAL"],
            "sceneRecord": scene,
            "injectionAttempt": injection,
            "truthRecord": truth_map,
            "runRecord": run,
            "collectRecord": collect,
            "filterRecord": filtered,
            "attemptRow": None,
            "undefinedDetectionOutcome": str(exc),
            "label": "SIMULATED-IUT",
        }
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
