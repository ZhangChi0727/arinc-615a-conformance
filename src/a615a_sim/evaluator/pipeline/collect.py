"""E4 IF-EXP-COLLECT.  Algorithm-visible only; no IF-EXP-TRUTH access."""

from __future__ import annotations

from typing import Any, Mapping

from a615a_sim.algorithm.library import EMPTY_DETAIL, project_cost


def collect_from_run(run_record: Mapping[str, Any], *, resource_mode: str) -> dict[str, Any]:
    """Project observation and resource logs.  Missing correlation is invalid-observation."""

    observations = list(run_record.get("observationLog") or [])
    detail = dict(run_record.get("detailCharges") or EMPTY_DETAIL)
    missing = any(
        isinstance(item, Mapping) and item.get("correlationId") in {None, ""}
        for item in observations
    )
    if run_record.get("traceRef", {}).get("observationLog"):
        extra = run_record["traceRef"]["observationLog"]
        if isinstance(extra, list):
            observations = observations or extra
            missing = missing or any(
                isinstance(item, Mapping) and item.get("correlationId") in {None, ""}
                for item in extra
            )
    status = "NORMAL"
    if not run_record.get("runId"):
        status = "NOT-RUN"
    return {
        "observationLog": observations,
        "resourceLog": {
            "mode": resource_mode,
            "statusClass": status,
            "detailCharges": detail,
            "chargedCost": project_cost(detail) if detail else dict(EMPTY_DETAIL),
        },
        "missingCorrelation": missing,
        "producer": "IF-EXP-COLLECT",
        "label": "SIMULATED-IUT",
    }


def collect_from_fixture(row: Mapping[str, Any]) -> dict[str, Any]:
    """Collect declared walkthrough resource/observation fields.  No truth read."""

    charged = dict(row.get("chargedCost") or EMPTY_DETAIL)
    missing = row.get("scenarioId") == "SC-INVALID-OBS"
    return {
        "observationLog": [
            {
                "correlationId": None if missing else "X-SYN",
                "kind": "FIXTURE",
            }
        ],
        "resourceLog": {
            "mode": row.get("resourcePolicy"),
            "statusClass": row.get("resourceStatus"),
            "detailCharges": charged,
            "chargedCost": charged,
        },
        "missingCorrelation": missing,
        "producer": "IF-EXP-COLLECT",
        "label": "SIMULATED-IUT",
    }
