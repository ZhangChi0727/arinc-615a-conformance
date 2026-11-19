"""Evaluator-side four-arm runner.  Holds truth capability; never passes it to arms."""

from __future__ import annotations

from typing import Any, Mapping

from a615a_sim.algorithm.adapter import REGISTERED_ARMS, run_arm
from a615a_sim.algorithm.library import ArmRun
from a615a_sim.bound_iut.protocol import SimulatedTarget
from a615a_sim.evaluator.guard import deny_algorithm_truth_access
from a615a_sim.evaluator.reset import reset_target
from a615a_sim.evaluator.truth import TruthCapability, _require_capability
from a615a_sim.faults.injector import inject, overlay_declared_fault


def confirm_then_overlay(
    target: SimulatedTarget,
    *,
    scene_id: str,
    fault_id: str,
    truth_store: Any,
    capability: object,
    pairing_id: str,
) -> Mapping[str, Any]:
    """Write IF-EXP-TRUTH, then reset and re-overlay so arms do not see confirmation traces."""

    deny_algorithm_truth_access(operation="confirm-then-overlay")
    _require_capability(capability)
    reset_target(target, pairing_id=pairing_id)
    attempt = inject(
        target,
        scene_id=scene_id,
        fault_id=fault_id,
        truth_store=truth_store,
        truth_capability=capability,
    )
    reset_target(target, pairing_id=pairing_id)
    overlay_declared_fault(target, scene_id=scene_id, fault_id=fault_id)
    return attempt.as_mapping()


def run_registered_arms(
    target: SimulatedTarget,
    *,
    scene_id: str,
    fault_id: str,
    truth_store: Any,
    capability: TruthCapability,
    resource_mode: str = "ROUNDS",
    remaining: int = 8,
    pairing_id: str = "PAIR-PHASE-B",
) -> dict[str, ArmRun]:
    """Run each arm on a fresh overlay of the same (scene, fault).  Isolated ledgers."""

    deny_algorithm_truth_access(operation="run-registered-arms")
    _require_capability(capability)
    confirm_then_overlay(
        target,
        scene_id=scene_id,
        fault_id=fault_id,
        truth_store=truth_store,
        capability=capability,
        pairing_id=pairing_id,
    )
    ledgers: dict[str, ArmRun] = {}
    for arm_id in REGISTERED_ARMS:
        reset_target(target, pairing_id=pairing_id)
        overlay_declared_fault(target, scene_id=scene_id, fault_id=fault_id)
        ledgers[arm_id] = run_arm(
            arm_id,
            target,
            scene_id=scene_id,
            resource_mode=resource_mode,
            remaining=remaining,
            correlation_id=f"{arm_id}-{scene_id}",
        )
    return ledgers
