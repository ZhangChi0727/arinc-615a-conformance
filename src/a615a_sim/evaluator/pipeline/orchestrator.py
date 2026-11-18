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
from a615a_sim.evaluator.pipeline.run import replay_run_fixture, run_registered_arm
from a615a_sim.evaluator.pipeline.scene import build_scene_record
from a615a_sim.evaluator.pipeline.truth_stage import write_truth_if_confirmed
from a615a_sim.evaluator.reset import reset_target
from a615a_sim.evaluator.truth import IndependentTruthStore, TruthCapability
from a615a_sim.faults.injector import InjectionAttempt, overlay_declared_fault

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

WF_PATH_KIND = {
    "WF-NORMAL": "LIVE",
    "WF-UNCONFIRMED-INJECT": "LIVE",
    "WF-INVALID-OBS": "LIVE",
    "WF-ABSTAIN": "ACCOUNTING-REPLAY",
    "WF-EQUIVALENT": "ACCOUNTING-REPLAY",
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


COMPARISON_REASONS = {
    ("WF-NORMAL", "finalHypotheses"): (
        "live catalogue hypothesisId uses underscore; SYN-NORMAL uses hyphen"
    ),
    ("WF-NORMAL", "runId"): "deterministic live runId scheme differs from SYN-NORMAL runId",
    ("WF-NORMAL", "attemptId"): "live attemptId is A-WF-*; SYN-NORMAL uses ATT-001",
    ("WF-NORMAL", "truthReference.truthHypothesis"): (
        "live catalogue hypothesisId uses underscore; SYN-NORMAL uses hyphen"
    ),
    ("WF-UNCONFIRMED-INJECT", "injectionStatus"): (
        "unconfirmed live path writes no IF-EXP-TRUTH; SYN-UNCONFIRMED stores UNCONFIRMED"
    ),
    ("WF-UNCONFIRMED-INJECT", "faultDomain"): (
        "unconfirmed live path writes no IF-EXP-TRUTH; SYN-UNCONFIRMED stores UNKNOWN"
    ),
    ("WF-UNCONFIRMED-INJECT", "resourcePolicy"): (
        "live scene still binds a resource mode; SYN-UNCONFIRMED is NOT-RUN"
    ),
    ("WF-UNCONFIRMED-INJECT", "resourceStatus"): (
        "no live collect/run; SYN-UNCONFIRMED records NOT-RUN"
    ),
    ("WF-UNCONFIRMED-INJECT", "attemptId"): "live attemptId is A-WF-*; SYN-UNCONFIRMED uses ATT-004",
    ("WF-INVALID-OBS", "stopClass"): (
        "live CL-LOOP stop is Stop-Singleton; SYN-INVALID-OBS accounts Stop-Error"
    ),
    ("WF-INVALID-OBS", "finalHypotheses"): (
        "live catalogue retains {h_normal}; SYN-INVALID-OBS accounts {h-normal, h1}"
    ),
    ("WF-INVALID-OBS", "injectionStatus"): (
        "live H-INVALID-OBS catalogue is unresolved; SYN-INVALID-OBS stores NORMAL"
    ),
    ("WF-INVALID-OBS", "faultDomain"): (
        "live H-INVALID-OBS catalogue is unknown; SYN-INVALID-OBS stores OUT-OF-DOMAIN"
    ),
    ("WF-INVALID-OBS", "localizationDecisionIssued"): (
        "live singleton stop issues localization; SYN-INVALID-OBS does not"
    ),
    ("WF-INVALID-OBS", "singletonDecisionIssued"): (
        "live singleton stop issues singleton; SYN-INVALID-OBS does not"
    ),
    ("WF-INVALID-OBS", "resourceStatus"): (
        "tester resource log is NORMAL; SYN-INVALID-OBS accounts RESOURCE-ERROR"
    ),
    ("WF-INVALID-OBS", "runId"): "deterministic live runId scheme differs from SYN-INVALID-OBS runId",
    ("WF-INVALID-OBS", "attemptId"): "live attemptId is A-WF-*; SYN-INVALID-OBS uses ATT-005",
    ("WF-ABSTAIN", "injectionStatus"): (
        "catalogue H-RESOURCE-ERROR is unresolved; SYN-STOP-645 stores CONFIRMED"
    ),
    ("WF-ABSTAIN", "faultDomain"): (
        "catalogue H-RESOURCE-ERROR is unknown; SYN-STOP-645 stores IN-DOMAIN-NON-EQUIVALENT"
    ),
    ("WF-ABSTAIN", "truthReference.truthHypothesis"): (
        "catalogue H-RESOURCE-ERROR hypothesisId is null; SYN-STOP-645 stores h645"
    ),
    ("WF-EQUIVALENT", "injectionStatus"): (
        "EVAL reads IF-EXP-TRUTH only; equivalent accounting replay writes no truth"
    ),
    ("WF-EQUIVALENT", "faultDomain"): (
        "EVAL reads IF-EXP-TRUTH only; equivalent accounting replay writes no truth"
    ),
    ("WF-EQUIVALENT", "resourceStatus"): (
        "no RUN/COLLECT on equivalent replay; SYN-EQUIVALENT records NOT-RUN"
    ),
}


def _mismatch_reason(workflow_id: str, field: str, expected: Any, actual: Any) -> str:
    listed = COMPARISON_REASONS.get((workflow_id, field))
    if listed:
        return listed
    return f"{workflow_id} {field} differs from SYN accounting ({expected!r} vs {actual!r})"


def _syn_mismatches(
    actual: Mapping[str, Any], expected: Mapping[str, Any], *, workflow_id: str
) -> list[dict[str, Any]]:
    mismatches = []
    for key in COMPARE_FIELDS:
        got = actual.get(key)
        want = expected.get(key)
        if got != want:
            mismatches.append(
                {
                    "field": key,
                    "expected": want,
                    "actual": got,
                    "reason": _mismatch_reason(workflow_id, key, want, got),
                }
            )
    want_h = (expected.get("truthReference") or {}).get("truthHypothesis")
    got_h = (actual.get("truthReference") or {}).get("truthHypothesis")
    if got_h != want_h:
        mismatches.append(
            {
                "field": "truthReference.truthHypothesis",
                "expected": want_h,
                "actual": got_h,
                "reason": _mismatch_reason(
                    workflow_id, "truthReference.truthHypothesis", want_h, got_h
                ),
            }
        )
    return mismatches


def execute_synthetic_walkthrough(workflow_id: str) -> dict[str, Any]:
    """Execute a registered WF path and compare the produced row with SYN-*."""

    deny_algorithm_truth_access(operation="walkthrough")
    if WF_PATH_KIND[workflow_id] == "ACCOUNTING-REPLAY":
        return execute_accounting_replay(workflow_id)
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
    live["pathKind"] = "LIVE"
    row = live.get("attemptRow") or {}
    live["synComparison"] = _syn_mismatches(row, fixture, workflow_id=workflow_id)
    live["label"] = "SIMULATED-IUT"
    return live


def execute_accounting_replay(workflow_id: str) -> dict[str, Any]:
    """SYN-* may feed RUN and COLLECT inputs only.  FILTER and EVAL compute."""

    deny_algorithm_truth_access(operation="accounting-replay")
    fixture = walkthrough_for_workflow(workflow_id)
    capability = issue_truth_capability()
    store = new_independent_truth_store()
    resource_mode = fixture.get("resourcePolicy") or "NOT-RUN"
    scene = build_scene_record(
        scene_id=fixture["scenarioId"],
        arm_id=fixture["armId"],
        resource_mode=resource_mode,
        fault_plan=SCENE_FAULT[fixture["scenarioId"]],
        pairing_id="PAIR-PHASE-C",
        reset_evidence_ref=fixture.get("resetEvidenceRef"),
    )
    injection = {
        "sceneId": fixture["scenarioId"],
        "attemptId": fixture["attemptId"],
        "faultId": SCENE_FAULT[fixture["scenarioId"]],
        "injectionConfirmed": workflow_id == "WF-ABSTAIN",
        "injectionUnconfirmed": False,
        "producer": "IF-EXP-INJECT",
        "label": "SIMULATED-IUT",
    }
    truth_map = None
    run = None
    collect = None
    if workflow_id == "WF-EQUIVALENT":
        filtered = filter_attempt(variant="pre-run-equivalent", equivalent_fault=True)
        row = assemble_attempt_row(
            scene=scene,
            injection=injection,
            truth=None,
            run=None,
            collect=None,
            filtered=filtered,
        )
    else:
        attempt = InjectionAttempt(
            scene_id=fixture["scenarioId"],
            attempt_id=fixture["attemptId"],
            fault_id=SCENE_FAULT[fixture["scenarioId"]],
            injection_confirmed=True,
            injection_unconfirmed=False,
        )
        truth_map = write_truth_if_confirmed(store, attempt, capability)
        run = replay_run_fixture(fixture)
        collect_mode = resource_mode if resource_mode in {"ROUNDS", "BUDGET"} else "BUDGET"
        collect = collect_from_run(run, resource_mode=collect_mode)
        filtered = filter_attempt(
            variant="run-completed",
            missing_correlation=bool(collect["missingCorrelation"]),
            stop_class=run.get("stopClass"),
            stage=run.get("stage"),
            action_issued=run.get("actionIssued"),
            resource_status=collect["resourceLog"]["statusClass"],
            run_id=run.get("runId"),
        )
        row = evaluate_with_store(
            store,
            fixture["attemptId"],
            capability,
            scene=scene,
            injection=injection,
            run=run,
            collect=collect,
            filtered=filtered,
        )
    result = {
        "path": WF_PATHS[workflow_id],
        "pathKind": "ACCOUNTING-REPLAY",
        "workflowId": workflow_id,
        "synId": WF_TO_SYN[workflow_id],
        "registeredPath": WF_PATHS[workflow_id],
        "sceneRecord": scene,
        "injectionAttempt": injection,
        "truthRecord": truth_map,
        "runRecord": run,
        "collectRecord": collect,
        "filterRecord": filtered,
        "attemptRow": row,
        "metricCells": metric_cells([row]),
        "synComparison": _syn_mismatches(row, fixture, workflow_id=workflow_id),
        "label": "SIMULATED-IUT",
    }
    return result


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
    "WF_PATH_KIND",
    "execute_accounting_replay",
    "execute_live_attempt",
    "execute_synthetic_walkthrough",
    "load_experiment_design",
    "load_synthetic_walkthrough",
    "metric_cells",
]
