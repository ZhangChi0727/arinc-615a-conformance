"""Evaluator-only fault identity.  Arm code holding the IUT cannot call this."""

from __future__ import annotations

from typing import Any

from a615a_sim.bound_iut.protocol import SimulatedTarget
from a615a_sim.evaluator.guard import deny_algorithm_truth_access
from a615a_sim.evaluator.truth import _require_capability


def evaluator_fault_record(target: SimulatedTarget, capability: object = None) -> dict[str, Any]:
    """Return evaluator-only fault identity.  Requires a truth capability."""

    deny_algorithm_truth_access(operation="evaluator-fault-record")
    _require_capability(capability)
    return {
        "faultId": target._fault_id,
        "sceneId": target._scene_id,
        "label": "EVALUATOR-ONLY",
    }
