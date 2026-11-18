"""Evaluator-only experiment records.  Not imported by a615a_sim public API."""

from a615a_sim.evaluator.guard import (
    TruthLeakageError,
    deny_algorithm_import,
    deny_algorithm_truth_access,
)

deny_algorithm_import(operation="import-evaluator")

from a615a_sim.evaluator.fault_view import evaluator_fault_record
from a615a_sim.evaluator.reset import reset_target
from a615a_sim.evaluator.truth import IndependentTruthStore, TruthCapability
from a615a_sim.faults.injector import InjectionAttempt

__all__ = [
    "IndependentTruthStore",
    "TruthCapability",
    "TruthLeakageError",
    "deny_algorithm_import",
    "deny_algorithm_truth_access",
    "evaluator_fault_record",
    "get_truth",
    "invoke_callable",
    "issue_truth_capability",
    "new_independent_truth_store",
    "reset_target",
    "write_confirmed_truth",
]


def issue_truth_capability() -> TruthCapability:
    return TruthCapability()


def new_independent_truth_store() -> IndependentTruthStore:
    return IndependentTruthStore()


def write_confirmed_truth(
    store: IndependentTruthStore,
    attempt: InjectionAttempt,
    capability: object = None,
):
    return store.write_from_confirmed_injection(attempt, capability)


def get_truth(
    store: IndependentTruthStore,
    attempt_id: str,
    capability: object = None,
):
    return store.get(attempt_id, capability)


def invoke_callable(fn, *args, **kwargs):
    return fn(*args, **kwargs)
