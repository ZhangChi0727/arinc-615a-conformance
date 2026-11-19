"""Load the experiment design JSON.  Does not close DEC-* gates."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

_ROOT = Path(__file__).resolve().parents[4]
DESIGN_PATH = _ROOT / "configs" / "research" / "cltav_experiment_design.json"
WF_TO_SYN = {
    "WF-NORMAL": "SYN-NORMAL",
    "WF-UNCONFIRMED-INJECT": "SYN-UNCONFIRMED",
    "WF-INVALID-OBS": "SYN-INVALID-OBS",
    "WF-ABSTAIN": "SYN-STOP-645",
    "WF-EQUIVALENT": "SYN-EQUIVALENT",
}


@lru_cache(maxsize=1)
def load_experiment_design() -> Mapping[str, Any]:
    return json.loads(DESIGN_PATH.read_text(encoding="utf-8"))


def load_synthetic_walkthrough(walkthrough_id: str) -> dict[str, Any]:
    rows = load_experiment_design()["syntheticWalkthroughs"]
    for row in rows:
        if row["id"] == walkthrough_id:
            return dict(row)
    raise KeyError(walkthrough_id)


def walkthrough_for_workflow(workflow_id: str) -> dict[str, Any]:
    return load_synthetic_walkthrough(WF_TO_SYN[workflow_id])
