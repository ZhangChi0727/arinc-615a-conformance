"""Load the Phase D pre-declared pilot config.  Does not run attempts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from a615a_sim.algorithm.library import REGISTERED_ARMS
from a615a_sim.faults.catalogue import evaluator_fault_plan, locate_scenes

_ROOT = Path(__file__).resolve().parents[4]
CONFIG_PATH = _ROOT / "configs/research/cltav_pilot_config_v1.json"


def load_pilot_config() -> Mapping[str, Any]:
    payload = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("pilot config must be an object")
    return payload


def declared_cells() -> tuple[dict[str, Any], ...]:
    payload = load_pilot_config()
    cells = payload["cells"]
    return tuple(dict(cell) for cell in cells)


def catalogue_cells() -> tuple[dict[str, str], ...]:
    locate = locate_scenes()
    rows: list[dict[str, str]] = []
    for scene_id, fault_id in evaluator_fault_plan():
        for arm_id in REGISTERED_ARMS:
            rows.append(
                {
                    "sceneId": scene_id,
                    "faultId": fault_id,
                    "armId": arm_id,
                    "locateFamily": scene_id in locate,
                }
            )
    return tuple(rows)


__all__ = [
    "CONFIG_PATH",
    "catalogue_cells",
    "declared_cells",
    "load_pilot_config",
]
