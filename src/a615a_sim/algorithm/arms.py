"""Four comparison arms.  No evaluator/truth imports."""

from __future__ import annotations

from a615a_sim.algorithm.execute import issue
from a615a_sim.algorithm.library import (
    ACTION_ANALYSIS,
    ArmRun,
    ExclusiveResource,
    predetermined_test_sequence,
)
from a615a_sim.algorithm.target_view import AlgorithmVisibleTarget


def run_cl_t(
    target: AlgorithmVisibleTarget,
    initial: dict[str, str],
    resource: ExclusiveResource,
    *,
    correlation_id: str,
) -> ArmRun:
    """Predetermined TEST sequence.  No analysis feedback into the next test."""

    run = ArmRun("CL-T", resource_mode=resource.mode, resource_remaining=resource.remaining)
    for action_id in predetermined_test_sequence(initial):
        issued = issue(target, run, resource, action_id, correlation_id=correlation_id, initial=initial)
        if issued is None and run.stop_class == "Stop-Budget":
            return run
    run.stop_class = "Stop-NoDistinguisher"
    run.resource_remaining = resource.remaining
    return run


def run_cl_a(
    target: AlgorithmVisibleTarget,
    initial: dict[str, str],
    resource: ExclusiveResource,
    *,
    correlation_id: str,
) -> ArmRun:
    """Analysis only on ALGORITHM-INITIAL fields.  No acquisition."""

    del target, correlation_id
    run = ArmRun("CL-A", resource_mode=resource.mode, resource_remaining=resource.remaining)
    issued = issue(
        None,
        run,
        resource,
        ACTION_ANALYSIS,
        correlation_id="unused",
        initial=initial,
    )
    if issued is None and run.stop_class == "Stop-Budget":
        return run
    run.stop_class = "Stop-NoDistinguisher"
    run.resource_remaining = resource.remaining
    run.analysis_notes["usedOwnObservationCount"] = 0
    return run


def run_cl_ta(
    target: AlgorithmVisibleTarget,
    initial: dict[str, str],
    resource: ExclusiveResource,
    *,
    correlation_id: str,
) -> ArmRun:
    """Frozen collection, then analysis.  No adaptive selection after analysis."""

    run = ArmRun("CL-TA", resource_mode=resource.mode, resource_remaining=resource.remaining)
    for action_id in predetermined_test_sequence(initial):
        issued = issue(target, run, resource, action_id, correlation_id=correlation_id, initial=initial)
        if issued is None and run.stop_class == "Stop-Budget":
            return run
    issued = issue(target, run, resource, ACTION_ANALYSIS, correlation_id=correlation_id, initial=initial)
    if issued is None and run.stop_class == "Stop-Budget":
        return run
    run.stop_class = "Stop-NoDistinguisher"
    run.resource_remaining = resource.remaining
    return run
