"""E0 IF-EXP-SCENE."""

from __future__ import annotations

from typing import Any, Mapping

from a615a_sim.algorithm.library import INITIAL_VISIBLE_FIELDS, algorithm_visible_initial
from a615a_sim.evaluator.guard import deny_algorithm_truth_access

FORBIDDEN_VISIBLE = frozenset(
    {
        "faultPlan",
        "truthSource",
        "injectionConfirmed",
        "validityClass",
        "equivalenceDisposition",
        "posthocAdjudication",
    }
)


def build_scene_record(
    *,
    scene_id: str,
    arm_id: str,
    resource_mode: str,
    config_id: str = "SIMULATED-IUT-BOUND-MODEL",
    iut: str = "SIMULATED-IUT",
    fault_plan: str | None = None,
    pairing_id: str | None = None,
    reset_id: str | None = None,
    reset_evidence_ref: str | None = None,
    requirement_interval: Mapping[str, Any] | None = None,
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluator/operator sceneRecord.  Algorithm sees only the typed projection."""

    deny_algorithm_truth_access(operation="e0-scene")
    visible = algorithm_visible_initial(
        scene_id=scene_id,
        registered_arm=arm_id,
        resource_mode=resource_mode if resource_mode in {"ROUNDS", "BUDGET"} else "ROUNDS",
        public_configuration_ref=config_id,
    )
    if set(visible) != set(INITIAL_VISIBLE_FIELDS):
        raise ValueError("algorithm-visible initial fields drifted from the allowlist")
    if FORBIDDEN_VISIBLE & set(visible):
        raise ValueError("algorithm-visible projection contains evaluator-only members")
    record = {
        "sceneId": scene_id,
        "configId": config_id,
        "IUT": iut,
        "faultPlan": fault_plan,
        "resourceMode": resource_mode,
        "pairingId": pairing_id,
        "resetId": reset_id,
        "resetEvidenceRef": reset_evidence_ref,
        "requirementInterval": dict(requirement_interval) if requirement_interval else None,
        "algorithmVisibleFields": dict(visible),
        "producer": "IF-EXP-SCENE",
        "label": "SIMULATED-IUT",
    }
    if extra:
        for key, value in extra.items():
            if key not in record:
                record[key] = value
    return record
