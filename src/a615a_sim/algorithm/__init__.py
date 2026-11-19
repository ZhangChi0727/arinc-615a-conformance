"""Algorithm-visible experiment arms.  This package must not import evaluator truth."""

from a615a_sim.algorithm.adapter import REGISTERED_ARMS, run_arm

__all__ = ["REGISTERED_ARMS", "run_arm"]
