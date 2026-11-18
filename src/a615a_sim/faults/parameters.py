"""Expand DRAFT confirmatory parameter cells.  Not a census runner."""

from __future__ import annotations

from typing import Any, Mapping

from a615a_sim.faults.catalogue import (
    applicable_scenes,
    locate_scenes,
    parameter_axes,
)

FIND_SCENES = (
    "SC-NORMAL-UPLOAD",
    "SC-WAIT-CONTINUE",
    "SC-ABORT",
    "SC-SINGLE-BATCH",
)
STATUS_SCENES = ("SC-NO-RESPONSE", "SC-WAIT-CONTINUE", "SC-ABORT")
ARMS = ("CL-T", "CL-A", "CL-TA", "CL-LOOP")


def _axis(axis_id: str) -> Mapping[str, Any]:
    for axis in parameter_axes():
        if axis["axisId"] == axis_id:
            return axis
    raise KeyError(axis_id)


def expand_independent_units() -> tuple[dict[str, Any], ...]:
    """One unit is (base scene × fault × parameter vector).  Arms are paired later."""

    units: list[dict[str, Any]] = []
    find_ticks = _axis("AX-FIND-ANSWER-TICK")["values"]
    silence = _axis("AX-STATUS-SILENCE-UNTIL")["values"]
    lur_ack = _axis("AX-LUR-ACK-TICK")["values"]
    jitter = _axis("AX-OBS-JITTER")["values"]
    find_ends = _axis("AX-FIND-OBS-END")["values"]

    for scene in sorted(applicable_scenes("H-NORMAL")):
        units.append(
            {
                "unitId": f"{scene}/H-NORMAL/DEFAULT",
                "sceneId": scene,
                "faultId": "H-NORMAL",
                "parameters": {},
                "axisIds": ["AX-BASE-SCENE"],
                "harderCaseId": None,
            }
        )

    for scene in FIND_SCENES:
        for value in find_ticks:
            units.append(
                {
                    "unitId": f"{scene}/F-FIND-ANSWER-LATE/{value['id']}",
                    "sceneId": scene,
                    "faultId": "F-FIND-ANSWER-LATE",
                    "parameters": {"findAnswerAtS": value["findAnswerAtS"]},
                    "axisIds": ["AX-BASE-SCENE", "AX-FIND-ANSWER-TICK"],
                    "harderCaseId": None,
                }
            )
        units.append(
            {
                "unitId": f"{scene}/F-FIND-ANSWER-ABSENT/DEFAULT",
                "sceneId": scene,
                "faultId": "F-FIND-ANSWER-ABSENT",
                "parameters": {},
                "axisIds": ["AX-BASE-SCENE"],
                "harderCaseId": None,
            }
        )
        units.append(
            {
                "unitId": f"{scene}/F-LUR-ACK-MISSING/DEFAULT",
                "sceneId": scene,
                "faultId": "F-LUR-ACK-MISSING",
                "parameters": {},
                "axisIds": ["AX-BASE-SCENE"],
                "harderCaseId": None,
            }
        )
        units.append(
            {
                "unitId": f"{scene}/F-LUR-ACK-WITHOUT-WRQ/DEFAULT",
                "sceneId": scene,
                "faultId": "F-LUR-ACK-WITHOUT-WRQ",
                "parameters": {},
                "axisIds": ["AX-BASE-SCENE"],
                "harderCaseId": None,
            }
        )
        for value in lur_ack:
            units.append(
                {
                    "unitId": f"{scene}/H-NORMAL/{value['id']}",
                    "sceneId": scene,
                    "faultId": "H-NORMAL",
                    "parameters": {"lurAckAtS": value["lurAckAtS"]},
                    "axisIds": ["AX-BASE-SCENE", "AX-LUR-ACK-TICK"],
                    "harderCaseId": None,
                }
            )

    for scene in STATUS_SCENES:
        for value in silence:
            units.append(
                {
                    "unitId": f"{scene}/F-STATUS-SILENCE/{value['id']}",
                    "sceneId": scene,
                    "faultId": "F-STATUS-SILENCE",
                    "parameters": {"statusSilenceUntilS": value["statusSilenceUntilS"]},
                    "axisIds": ["AX-BASE-SCENE", "AX-STATUS-SILENCE-UNTIL"],
                    "harderCaseId": None,
                }
            )

    for scene in FIND_SCENES:
        units.append(
            {
                "unitId": f"{scene}/HC-FIND-ENDPOINT/findAnswerAtS=2",
                "sceneId": scene,
                "faultId": "F-FIND-ANSWER-LATE",
                "parameters": {"findAnswerAtS": "2"},
                "axisIds": ["AX-BASE-SCENE", "AX-FIND-ANSWER-TICK"],
                "harderCaseId": "HC-FIND-ENDPOINT",
            }
        )
    units.append(
        {
            "unitId": "SC-INVALID-OBS/HC-INVALID-OBS-JITTER/observationJitterS=-1/500",
            "sceneId": "SC-INVALID-OBS",
            "faultId": "H-INVALID-OBS",
            "parameters": {"observationJitterS": "-1/500"},
            "axisIds": ["AX-OBS-JITTER"],
            "harderCaseId": "HC-INVALID-OBS-JITTER",
        }
    )

    for scene in FIND_SCENES:
        for value in jitter:
            units.append(
                {
                    "unitId": f"{scene}/F-FIND-ANSWER-LATE/{value['id']}",
                    "sceneId": scene,
                    "faultId": "F-FIND-ANSWER-LATE",
                    "parameters": {"observationJitterS": value["observationJitterS"]},
                    "axisIds": ["AX-BASE-SCENE", "AX-OBS-JITTER"],
                    "harderCaseId": "HC-OBS-PERTURB-EPS",
                }
            )
        for value in find_ends:
            if value["id"] == "FIND-END-DEFAULT":
                continue
            units.append(
                {
                    "unitId": f"{scene}/F-FIND-ANSWER-ABSENT/{value['id']}",
                    "sceneId": scene,
                    "faultId": "F-FIND-ANSWER-ABSENT",
                    "parameters": {"findObservationEndS": value["findObservationEndS"]},
                    "axisIds": ["AX-BASE-SCENE", "AX-FIND-OBS-END"],
                    "harderCaseId": "HC-LATE-ABSENT-SHORT-WINDOW",
                }
            )

    locate = locate_scenes()
    for unit in units:
        unit["locateFamily"] = unit["sceneId"] in locate
        unit["label"] = "DRAFT / SIMULATED-IUT / HYPOTHETICAL-NOT-RESULT"
    return tuple(units)


def expand_arm_cells() -> tuple[dict[str, Any], ...]:
    cells: list[dict[str, Any]] = []
    for unit in expand_independent_units():
        for arm in ARMS:
            cell = dict(unit)
            cell["armId"] = arm
            cell["cellId"] = f"{unit['unitId']}/{arm}"
            cells.append(cell)
    return tuple(cells)
