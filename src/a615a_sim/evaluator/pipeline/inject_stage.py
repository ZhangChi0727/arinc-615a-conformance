"""E1 IF-EXP-INJECT.  Planned is not confirmed."""

from __future__ import annotations

from typing import Any

from a615a_sim.bound_iut.protocol import SimulatedTarget
from a615a_sim.evaluator.guard import deny_algorithm_truth_access
from a615a_sim.faults.injector import InjectionAttempt, inject


def run_inject(
    target: SimulatedTarget,
    *,
    scene_id: str,
    fault_id: str,
    attempt_id: str | None = None,
    confirm: bool = True,
) -> InjectionAttempt:
    deny_algorithm_truth_access(operation="e1-inject")
    return inject(
        target,
        scene_id=scene_id,
        fault_id=fault_id,
        attempt_id=attempt_id,
        confirm=confirm,
        truth_store=None,
        truth_capability=None,
    )


def inject_mapping(attempt: InjectionAttempt) -> dict[str, Any]:
    return dict(attempt.as_mapping())
