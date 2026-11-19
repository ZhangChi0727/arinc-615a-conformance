"""Timing fields for EVAL.  Absent answers use the observation end (N4)."""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Mapping

from a615a_sim.clock import (
    FIND_OBSERVATION_END_S,
    SCENE_FAMILY_FIND,
    SCENE_FAMILY_INFORMATION,
    declared_observation_end,
    t5_interval_verdict,
    ClosedInterval,
    find_host_requirement,
)


def observation_end_for_absent_answer(
    *,
    family: str = SCENE_FAMILY_FIND,
    model_measurement_tick: Fraction | None = None,
) -> Fraction:
    """N4: FIND/INFORMATION absence is scored at the observation end, not tick 0."""

    del model_measurement_tick
    return declared_observation_end(family)


def interval_outcome(
    observation: Mapping[str, Any] | None,
    requirement: Mapping[str, Any] | None,
) -> str | None:
    if not observation or not requirement:
        return None
    obs = ClosedInterval(
        Fraction(str(observation["lower"])),
        Fraction(str(observation["upper"])),
        str(observation.get("unit", "s")),
    )
    req = ClosedInterval(
        Fraction(str(requirement["lower"])),
        Fraction(str(requirement["upper"])),
        str(requirement.get("unit", "s")),
    )
    if obs.unit != req.unit:
        raise ValueError("observation and requirement interval units differ")
    return t5_interval_verdict(obs, req)


def find_absent_requirement() -> ClosedInterval:
    return find_host_requirement()


ABSENT_FIND_END = FIND_OBSERVATION_END_S
INFORMATION_FAMILY = SCENE_FAMILY_INFORMATION
