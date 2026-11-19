"""Simulated clock with a declared error bound epsilon (DEP-CLOCK, simulated).

This is not physical metrology and does not close DEC-CLOCK.  T5 uses the
experiment-plan interval rule: I_obs subseteq I_r is PASS; disjoint is FAIL;
intersect-but-not-contained is INCONCLUSIVE.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

CLOCK_IDENTITY = "SIMULATED-CLOCK-CLTAV-EXP-A"
CLOCK_UNIT = "second"
# Declared simulated error bound.  DEC-CLOCK remains OPEN; this is not a
# calibrated laboratory budget.
SIMULATED_EPSILON = Fraction(1, 1000)
FIND_HOST_ANSWER_S = Fraction(2, 1)
STATUS_EXCEPTION_DELAY_S = Fraction(10, 1)
# Observation end > governing deadline + epsilon + margin so presence versus
# absence (and late versus absent FIND answers) remain distinguishable.
OBSERVATION_END_MARGIN_S = Fraction(1, 10)
OBSERVATION_END_EXTRA_S = Fraction(1, 10)
FIND_OBSERVATION_END_S = (
    FIND_HOST_ANSWER_S + SIMULATED_EPSILON + OBSERVATION_END_MARGIN_S + OBSERVATION_END_EXTRA_S
)
INFORMATION_OBSERVATION_END_S = (
    STATUS_EXCEPTION_DELAY_S
    + SIMULATED_EPSILON
    + OBSERVATION_END_MARGIN_S
    + OBSERVATION_END_EXTRA_S
)
# Alias retained for FIND-family callers.
DECLARED_OBSERVATION_END_S = FIND_OBSERVATION_END_S
FIND_ANSWER_NORMAL_AT_S = Fraction(1, 100)
FIND_ANSWER_LATE_AT_S = FIND_HOST_ANSWER_S + Fraction(5, 100)
SCENE_FAMILY_FIND = "FIND"
SCENE_FAMILY_INFORMATION = "INFORMATION"

FIND_OBSERVATION_END_JUSTIFICATION = (
    "FIND-family observation end is strictly greater than CRS-M1-00391 host-answer "
    "deadline 2 s plus SIMULATED_EPSILON plus margin so a late FIND-ANSWER tick in "
    "(2, end) is distinct from a missing FIND-ANSWER observed only when the window ends."
)
INFORMATION_OBSERVATION_END_JUSTIFICATION = (
    "INFORMATION-family observation end is strictly greater than the STATUS "
    "exceptionDelaySeconds=10 s obligation plus SIMULATED_EPSILON plus margin so "
    "omitted follow-on STATUS is observed as window end rather than as a named silence event."
)


@dataclass(frozen=True)
class ClosedInterval:
    lower: Fraction
    upper: Fraction
    unit: str = CLOCK_UNIT

    def __post_init__(self) -> None:
        if self.upper < self.lower:
            raise ValueError("interval upper is below lower")

    def contains(self, other: "ClosedInterval") -> bool:
        return self.lower <= other.lower and other.upper <= self.upper

    def disjoint(self, other: "ClosedInterval") -> bool:
        return self.upper < other.lower or other.upper < self.lower

    def intersect(self, other: "ClosedInterval") -> "ClosedInterval | None":
        lower = max(self.lower, other.lower)
        upper = min(self.upper, other.upper)
        if upper < lower:
            return None
        return ClosedInterval(lower, upper, self.unit)


class SimulatedClock:
    """Monotonic process-local clock used for FIND/SEND/ABORT/INFORMATION timing."""

    def __init__(self, *, epsilon: Fraction = SIMULATED_EPSILON) -> None:
        if epsilon <= 0:
            raise ValueError("epsilon must be a positive Fraction")
        self._tick = Fraction(0, 1)
        self.epsilon = epsilon
        self.identity = CLOCK_IDENTITY
        self.unit = CLOCK_UNIT

    @property
    def now(self) -> Fraction:
        return self._tick

    def advance(self, delta: Fraction | int) -> Fraction:
        step = delta if isinstance(delta, Fraction) else Fraction(delta, 1)
        if step < 0:
            raise ValueError("clock cannot run backwards")
        self._tick += step
        return self._tick

    def observation_interval(self, tick: Fraction | None = None) -> ClosedInterval:
        instant = self._tick if tick is None else tick
        return ClosedInterval(instant - self.epsilon, instant + self.epsilon, self.unit)

    def reset(self) -> None:
        self._tick = Fraction(0, 1)


def t5_interval_verdict(observation: ClosedInterval, requirement: ClosedInterval) -> str:
    """Apply EXP-PLAN-2026-001 T5 on closed intervals.  Not a runtime rewrite."""

    if requirement.contains(observation):
        return "PASS"
    if observation.disjoint(requirement):
        return "FAIL"
    return "INCONCLUSIVE"


def find_host_requirement() -> ClosedInterval:
    """CRS-M1-00391 2 s host-answer closed interval [0, 2]."""

    return ClosedInterval(Fraction(0, 1), FIND_HOST_ANSWER_S)


def declared_observation_end(family: str = SCENE_FAMILY_FIND) -> Fraction:
    """Evaluator observation end for a scene family; each exceeds deadline + ε + margin."""

    if family == SCENE_FAMILY_INFORMATION:
        minimum = STATUS_EXCEPTION_DELAY_S + SIMULATED_EPSILON + OBSERVATION_END_MARGIN_S
        if INFORMATION_OBSERVATION_END_S <= minimum:
            raise ValueError("INFORMATION observation end must exceed 10 s + epsilon + margin")
        return INFORMATION_OBSERVATION_END_S
    if family != SCENE_FAMILY_FIND:
        raise ValueError(f"unknown scene family {family}")
    minimum = FIND_HOST_ANSWER_S + SIMULATED_EPSILON + OBSERVATION_END_MARGIN_S
    if FIND_OBSERVATION_END_S <= minimum:
        raise ValueError("FIND observation end must exceed 2 s + epsilon + margin")
    return FIND_OBSERVATION_END_S
