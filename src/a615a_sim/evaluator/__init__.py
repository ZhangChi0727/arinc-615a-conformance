"""Evaluator-only experiment records.  Not imported by a615a_sim public API."""

from a615a_sim.evaluator.guard import (
    TruthLeakageError,
    deny_algorithm_import,
    deny_algorithm_truth_access,
)

deny_algorithm_import(operation="import-evaluator")

from a615a_sim.evaluator.reset import reset_target
from a615a_sim.evaluator.truth import IndependentTruthStore

__all__ = [
    "IndependentTruthStore",
    "TruthLeakageError",
    "deny_algorithm_import",
    "deny_algorithm_truth_access",
    "reset_target",
]
