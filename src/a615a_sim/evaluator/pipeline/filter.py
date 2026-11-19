"""E5 IF-EXP-FILTER.  Unconfirmed, invalid, equivalent, abstain are not PASS/FAIL."""

from __future__ import annotations

from typing import Any, Mapping

from a615a_sim.evaluator.guard import deny_algorithm_truth_access


def filter_attempt(
    *,
    variant: str,
    injection_unconfirmed: bool = False,
    equivalent_fault: bool = False,
    unresolved: bool = False,
    missing_correlation: bool = False,
    stop_class: str | None = None,
    stage: str | None = None,
    action_issued: bool | None = None,
    resource_status: str | None = None,
    run_id: str | None = None,
) -> dict[str, Any]:
    deny_algorithm_truth_access(operation="e5-filter")
    if variant == "pre-run-exclusion" or injection_unconfirmed:
        return {
            "validityClass": "PRE-RUN-EXCLUDED",
            "filterReason": "unconfirmed-injection",
            "variant": "pre-run-exclusion",
            "producer": "IF-EXP-FILTER",
        }
    if variant == "pre-run-equivalent" or equivalent_fault:
        return {
            "validityClass": "PRE-RUN-EXCLUDED",
            "filterReason": "equivalent-fault",
            "variant": "pre-run-equivalent",
            "producer": "IF-EXP-FILTER",
        }
    if unresolved and run_id is None:
        return {
            "validityClass": "PRE-RUN-EXCLUDED",
            "filterReason": "unresolved-equivalence",
            "variant": "pre-run-exclusion",
            "producer": "IF-EXP-FILTER",
        }
    if missing_correlation:
        return {
            "validityClass": "INVALID",
            "filterReason": "invalid-observation",
            "variant": "run-completed",
            "producer": "IF-EXP-FILTER",
        }
    if stop_class == "Stop-645":
        return {
            "validityClass": "ABSTAIN",
            "filterReason": "abstain",
            "variant": "run-completed",
            "producer": "IF-EXP-FILTER",
        }
    if stop_class == "Stop-Empty":
        return {
            "validityClass": "INVALID",
            "filterReason": "empty-compatible-set",
            "variant": "run-completed",
            "producer": "IF-EXP-FILTER",
        }
    if stop_class == "Stop-Budget" and action_issued is False:
        return {
            "validityClass": "INCOMPLETE",
            "filterReason": "pre-action-budget",
            "variant": "run-completed",
            "producer": "IF-EXP-FILTER",
        }
    if stop_class == "Stop-Budget" or resource_status == "BUDGET-EXHAUSTED":
        return {
            "validityClass": "INCOMPLETE",
            "filterReason": "budget-exhausted",
            "variant": "run-completed",
            "producer": "IF-EXP-FILTER",
        }
    del run_id
    return {
        "validityClass": "VALID",
        "filterReason": "run-completed",
        "variant": "run-completed",
        "producer": "IF-EXP-FILTER",
    }


def filter_from_fixture(row: Mapping[str, Any], collect: Mapping[str, Any]) -> dict[str, Any]:
    status = str(row.get("injectionStatus") or "")
    return filter_attempt(
        variant=(
            "pre-run-exclusion"
            if status == "UNCONFIRMED"
            else "pre-run-equivalent"
            if status == "EQUIVALENT"
            else "run-completed"
        ),
        injection_unconfirmed=status == "UNCONFIRMED",
        equivalent_fault=status == "EQUIVALENT",
        unresolved=status == "UNRESOLVED",
        missing_correlation=bool(collect.get("missingCorrelation")),
        stop_class=row.get("stopClass"),
        stage=row.get("stage"),
        action_issued=row.get("actionIssued"),
        resource_status=row.get("resourceStatus"),
        run_id=row.get("runId"),
    )
