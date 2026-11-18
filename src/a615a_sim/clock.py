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
# Observation end > 2 s + epsilon + margin so LATE versus ABSENT differ.
OBSERVATION_END_MARGIN_S = Fraction(1, 10)
DECLARED_OBSERVATION_END_S = FIND_HOST_ANSWER_S + SIMULATED_EPSILON + OBSERVATION_END_MARGIN_S + Fraction(1, 10)
FIND_ANSWER_LATE_AT_S = FIND_HOST_ANSWER_S + Fraction(5, 100)


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


def declared_observation_end() -> Fraction:
    """Evaluator observation end; strictly after 2 s + epsilon + margin."""

    minimum = FIND_HOST_ANSWER_S + SIMULATED_EPSILON + OBSERVATION_END_MARGIN_S
    if DECLARED_OBSERVATION_END_S <= minimum:
        raise ValueError("declared observation end must exceed 2 s + epsilon + margin")
    return DECLARED_OBSERVATION_END_S
