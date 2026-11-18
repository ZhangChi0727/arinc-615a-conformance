"""E2 IF-EXP-TRUTH.  Unconfirmed injection cannot default to valid truth."""

from __future__ import annotations

from typing import Any, Mapping

from a615a_sim.evaluator.guard import deny_algorithm_truth_access
from a615a_sim.evaluator.truth import IndependentTruthStore, TruthCapability
from a615a_sim.faults.injector import InjectionAttempt


def write_truth_if_confirmed(
    store: IndependentTruthStore,
    attempt: InjectionAttempt,
    capability: TruthCapability,
) -> Mapping[str, Any] | None:
    deny_algorithm_truth_access(operation="e2-truth")
    if attempt.injection_unconfirmed or not attempt.injection_confirmed:
        return None
    record = store.write_from_confirmed_injection(attempt, capability)
    return record.as_mapping(capability)
