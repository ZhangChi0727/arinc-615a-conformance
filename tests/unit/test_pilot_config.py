"""Phase D pre-declaration: cells, N, seeds exist before any census."""

from __future__ import annotations

import json
from pathlib import Path

from a615a_sim.algorithm.library import REGISTERED_ARMS
from a615a_sim.evaluator.pipeline.pilot_config import (
    CONFIG_PATH,
    catalogue_cells,
    load_pilot_config,
)

ROOT = Path(__file__).resolve().parents[2]


def test_pilot_config_is_predeclared_and_not_confirmatory() -> None:
    payload = load_pilot_config()
    assert payload["identity"]["confirmatoryRegistration"] is False
    assert payload["identity"]["registrationYaml"] is False
    assert payload["identity"]["label"] == "PILOT / SIMULATED-IUT"
    assert payload["sample"]["attemptsPerCell"] == 3
    assert payload["sample"]["seeds"] == [1001, 1002, 1003]
    assert payload["sample"]["decSample"] == "OPEN"
    assert payload["resourceMode"]["mode"] == "ROUNDS"
    assert payload["resourceMode"]["remainingPerCell"] == 8
    assert payload["resourceMode"]["decResource"] == "OPEN"
    assert payload["iut"]["decIut"] == "CLOSED"
    assert payload["iut"]["class"] == "SIMULATED-IUT"
    assert "DEC-SAMPLE" in payload["openDecisions"]
    assert "DEC-IUT" not in payload["openDecisions"]
    assert payload["closedDecisions"] == ["DEC-IUT"]
    assert "inferential statistics" in payload["analysis"]["forbidden"]


def test_pilot_cells_match_catalogue_applicable_scenes_times_four_arms() -> None:
    payload = load_pilot_config()
    expected = catalogue_cells()
    assert payload["cellCount"] == len(expected) == 120
    assert payload["attemptCount"] == 360
    observed = [
        (cell["sceneId"], cell["faultId"], cell["armId"]) for cell in payload["cells"]
    ]
    wanted = [(row["sceneId"], row["faultId"], row["armId"]) for row in expected]
    assert observed == wanted
    for cell in payload["cells"]:
        assert cell["N"] == 3
        assert cell["seeds"] == [1001, 1002, 1003]
        assert cell["armId"] in REGISTERED_ARMS
        assert cell["resourceMode"] == "ROUNDS"
        assert cell["resourceRemaining"] == 8


def test_phase_c_shape_file_still_leaves_n_pending() -> None:
    payload = json.loads(
        (ROOT / "configs/research/cltav_pilot_registration_shape_v1.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["sample"]["N"] == "PENDING-PHASE-D"
    assert CONFIG_PATH.name == "cltav_pilot_config_v1.json"
