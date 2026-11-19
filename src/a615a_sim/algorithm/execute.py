"""Issue one library action against the algorithm-visible target."""

from __future__ import annotations

from typing import Any

from a615a_sim.algorithm.library import (
    ACTION_ANALYSIS,
    ACTION_PREP,
    ACTION_RECOVER,
    ACTION_TEST_ABORT,
    ACTION_TEST_FIND,
    ACTION_TEST_INFORMATION,
    ACTION_TEST_SEND,
    ArmRun,
    ExclusiveResource,
    t5_on_visible,
)
from a615a_sim.algorithm.target_view import AlgorithmVisibleTarget


def issue(
    target: AlgorithmVisibleTarget | None,
    run: ArmRun,
    resource: ExclusiveResource,
    action_id: str,
    *,
    correlation_id: str,
    initial: dict[str, str] | None = None,
) -> dict[str, Any] | None:
    if not resource.can_afford(action_id):
        run.stop_class = "Stop-Budget"
        run.resource_remaining = resource.remaining
        return None
    resource.charge(action_id)
    run.charge_action(action_id)
    visible: dict[str, Any] | None = None
    if action_id in {
        ACTION_TEST_FIND,
        ACTION_TEST_SEND,
        ACTION_TEST_ABORT,
        ACTION_TEST_INFORMATION,
        ACTION_PREP,
        ACTION_RECOVER,
    } and target is None:
        raise ValueError("TEST/Prep/Recover require an algorithm-visible target")
    if action_id == ACTION_TEST_FIND:
        visible = target.find(correlation_id)
    elif action_id == ACTION_TEST_SEND:
        visible = target.send(correlation_id)
    elif action_id == ACTION_TEST_ABORT:
        visible = target.abort(correlation_id)
    elif action_id == ACTION_TEST_INFORMATION:
        visible = target.information(correlation_id)
    elif action_id == ACTION_ANALYSIS:
        run.analysis_notes = {
            "usedInitialFields": sorted((initial or {}).keys()),
            "usedOwnObservationCount": len(run.observation_log),
        }
    elif action_id in {ACTION_PREP, ACTION_RECOVER}:
        visible = None
    else:
        raise ValueError(f"undeclared action {action_id}")
    if visible is not None:
        run.observation_log.append(visible)
        verdict = t5_on_visible(visible)
        if verdict is not None:
            run.t5_verdicts.append(verdict)
    run.resource_remaining = resource.remaining
    return visible
