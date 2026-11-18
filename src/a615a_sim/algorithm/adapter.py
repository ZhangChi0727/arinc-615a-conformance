"""One adapter for the four registered arms.  Arms never see truth or injector plans."""

from __future__ import annotations

from a615a_sim.algorithm.arms import run_cl_a, run_cl_t, run_cl_ta
from a615a_sim.algorithm.library import (
    REGISTERED_ARMS,
    ArmRun,
    ExclusiveResource,
    algorithm_visible_initial,
)
from a615a_sim.algorithm.loop import run_cl_loop
from a615a_sim.algorithm.target_view import AlgorithmVisibleTarget
from a615a_sim.bound_iut.protocol import SimulatedTarget

_DISPATCH = {
    "CL-T": run_cl_t,
    "CL-A": run_cl_a,
    "CL-TA": run_cl_ta,
    "CL-LOOP": run_cl_loop,
}


def run_arm(
    arm_id: str,
    target: SimulatedTarget,
    *,
    scene_id: str,
    resource_mode: str,
    remaining: int,
    correlation_id: str,
) -> ArmRun:
    if arm_id not in REGISTERED_ARMS:
        raise ValueError(f"unknown arm {arm_id}")
    initial = algorithm_visible_initial(
        scene_id=scene_id,
        registered_arm=arm_id,
        resource_mode=resource_mode,
    )
    visible_target = AlgorithmVisibleTarget(target)
    resource = ExclusiveResource(resource_mode, remaining)
    return _DISPATCH[arm_id](
        visible_target,
        initial,
        resource,
        correlation_id=correlation_id,
    )
