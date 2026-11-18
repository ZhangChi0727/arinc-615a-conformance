"""Run the pre-declared SIMULATED-IUT / PILOT census.  Does not edit the config."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from a615a_sim.evaluator import issue_truth_capability, new_independent_truth_store  # noqa: E402
from a615a_sim.evaluator.pipeline.evaluate import metric_cells, population_sets  # noqa: E402
from a615a_sim.evaluator.pipeline.orchestrator import execute_live_attempt  # noqa: E402
from a615a_sim.evaluator.pipeline.pilot_config import CONFIG_PATH, load_pilot_config  # noqa: E402

OUT_DIR = ROOT / "artifacts" / "pilot"
RAW_PATH = OUT_DIR / "cltav_pilot_attempts_v1.jsonl"
SUMMARY_PATH = OUT_DIR / "cltav_pilot_summary_v1.json"

METRIC_NUM_DEN = (
    ("MET-ATTEMPTS", "POP-ATTEMPTS", None),
    ("MET-ANSWERED-COVERAGE", "POP-ANSWERED", "POP-ATTEMPTS"),
    ("MET-CONDITIONAL-DETECTION-ERROR", "POP-CONDITIONAL-ERROR", "POP-ANSWERED-TRUTH-SCORABLE"),
    ("MET-TRUTH-SCORABLE-COVERAGE", "POP-ANSWERED-TRUTH-SCORABLE", "POP-ANSWERED"),
    ("MET-TRUTH-MISSING", "POP-TRUTH-MISSING", "POP-ATTEMPTS"),
    ("MET-MISS", "POP-MISSES", "POP-CONFIRMED-FAULT"),
    ("MET-FALSE-FAIL", "POP-FALSE-FAILS", "POP-QUALIFIED-NORMAL"),
    ("MET-ABSTAIN", "POP-ABSTAIN", "POP-ATTEMPTS"),
    ("MET-INCONCLUSIVE", "POP-INCONCLUSIVE", "POP-ATTEMPTS"),
    ("MET-ERROR", "POP-ERROR", "POP-ATTEMPTS"),
    ("MET-INCOMPLETE", "POP-INCOMPLETE", "POP-ATTEMPTS"),
    ("MET-LOCALIZATION-COVERAGE", "POP-LOCALIZATION-DECISION", "POP-LOCALIZATION-ELIGIBLE"),
    ("MET-TRUE-RETAINED", "POP-TRUE-RETAINED", "POP-LOCALIZATION-TRUTH-SCORABLE"),
    ("MET-TRUE-EXCLUDED", "POP-TRUE-EXCLUDED", "POP-LOCALIZATION-TRUTH-SCORABLE"),
    ("MET-SINGLETON-CORRECT", "POP-SINGLETON-CORRECT", "POP-SINGLETON-TRUTH-SCORABLE"),
)

COMPARE_IGNORE = {
    "attemptId",
    "runId",
    "pairingId",
    "resetEvidenceRef",
}


def _git_head() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def counts_with_denominators(rows: list[Mapping[str, Any]]) -> dict[str, Any]:
    pops = population_sets(rows)
    out: dict[str, Any] = {}
    for metric_id, num_pop, den_pop in METRIC_NUM_DEN:
        numerator = len(pops[num_pop])
        if den_pop is None:
            out[metric_id] = {
                "numerator": numerator,
                "denominator": numerator,
                "display": f"{numerator}/{numerator}",
            }
            continue
        denominator = len(pops[den_pop])
        display = "N/A" if denominator == 0 else f"{numerator}/{denominator}"
        out[metric_id] = {
            "numerator": numerator,
            "denominator": denominator,
            "display": display,
            "numeratorPopulation": num_pop,
            "denominatorPopulation": den_pop,
        }
    finals = [
        len(row.get("finalHypotheses") or [])
        for row in rows
        if str(row.get("attemptId")) in pops["POP-LOCALIZATION-ELIGIBLE"]
    ]
    out["MET-FINAL-CANDIDATES"] = {
        "eligibleN": len(pops["POP-LOCALIZATION-ELIGIBLE"]),
        "lengths": finals,
    }
    out["MET-COST-VECTOR"] = metric_cells(rows)["MET-COST-VECTOR"]
    out["MET-ROUNDS"] = metric_cells(rows)["MET-ROUNDS"]
    return out


def _comparable(row: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key not in COMPARE_IGNORE}


def variance_report(rows: list[Mapping[str, Any]]) -> dict[str, Any]:
    comparable = [_comparable(row) for row in rows]
    unique = []
    for item in comparable:
        if item not in unique:
            unique.append(item)
    return {
        "attemptN": len(rows),
        "distinctComparableRows": len(unique),
        "identicalRepeats": len(unique) <= 1,
    }


def run_census() -> dict[str, Any]:
    config_bytes = CONFIG_PATH.read_bytes()
    config_sha = hashlib.sha256(config_bytes).hexdigest()
    payload = load_pilot_config()
    if payload["identity"]["confirmatoryRegistration"]:
        raise SystemExit("pilot config must not be confirmatory")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    raw_rows: list[dict[str, Any]] = []
    problems: list[dict[str, Any]] = []
    with RAW_PATH.open("w", encoding="utf-8") as handle:
        for cell in payload["cells"]:
            for seed in cell["seeds"]:
                attempt_id = f"A-{cell['cellId']}-S{seed}"
                store = new_independent_truth_store()
                capability = issue_truth_capability()
                live = execute_live_attempt(
                    scene_id=cell["sceneId"],
                    fault_id=cell["faultId"],
                    arm_id=cell["armId"],
                    resource_mode=cell["resourceMode"],
                    remaining=int(cell["resourceRemaining"]),
                    capability=capability,
                    store=store,
                    confirm=True,
                    pairing_id=f"PAIR-{cell['cellId']}-S{seed}",
                    attempt_id=attempt_id,
                )
                row = live.get("attemptRow")
                record = {
                    "label": "PILOT / SIMULATED-IUT",
                    "developmentLineage": True,
                    "confirmatory": False,
                    "cellId": cell["cellId"],
                    "sceneId": cell["sceneId"],
                    "faultId": cell["faultId"],
                    "armId": cell["armId"],
                    "seed": seed,
                    "resourceMode": cell["resourceMode"],
                    "resourceRemaining": cell["resourceRemaining"],
                    "locateFamily": cell["locateFamily"],
                    "configSha256": config_sha,
                    "attemptRow": row,
                    "undefinedDetectionOutcome": live.get("undefinedDetectionOutcome"),
                    "injectionAttempt": live.get("injectionAttempt"),
                    "filterRecord": live.get("filterRecord"),
                    "runStopClass": (live.get("runRecord") or {}).get("stopClass"),
                    "runFinalHypotheses": (live.get("runRecord") or {}).get("finalHypotheses"),
                }
                if row is None:
                    problems.append(
                        {
                            "attemptId": attempt_id,
                            "cellId": cell["cellId"],
                            "kind": "undefined-detection-outcome",
                            "detail": live.get("undefinedDetectionOutcome"),
                        }
                    )
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
                raw_rows.append(record)

    by_cell: dict[str, list[dict[str, Any]]] = {}
    for record in raw_rows:
        by_cell.setdefault(record["cellId"], []).append(record)

    cell_summaries = []
    for cell in payload["cells"]:
        records = by_cell[cell["cellId"]]
        rows = [item["attemptRow"] for item in records if item["attemptRow"] is not None]
        cell_summaries.append(
            {
                "cellId": cell["cellId"],
                "sceneId": cell["sceneId"],
                "faultId": cell["faultId"],
                "armId": cell["armId"],
                "N": cell["N"],
                "seeds": cell["seeds"],
                "locateFamily": cell["locateFamily"],
                "scoredAttempts": len(rows),
                "metrics": counts_with_denominators(rows) if rows else None,
                "variance": variance_report(rows) if rows else None,
            }
        )

    scored = [item["attemptRow"] for item in raw_rows if item["attemptRow"] is not None]
    summary = {
        "label": "PILOT / SIMULATED-IUT",
        "confirmatory": False,
        "developmentLineage": True,
        "reuseAsConfirmatoryForbidden": True,
        "configPath": str(CONFIG_PATH.relative_to(ROOT)).replace("\\", "/"),
        "configSha256": config_sha,
        "predeclarationHead": _git_head(),
        "cellCount": payload["cellCount"],
        "declaredAttemptCount": payload["attemptCount"],
        "writtenAttemptCount": len(raw_rows),
        "scoredAttemptCount": len(scored),
        "overallMetrics": counts_with_denominators(scored) if scored else None,
        "cells": cell_summaries,
        "operationalProblems": problems,
        "knownStructuralEffects": [
            "CL-T reports the observation-implied candidate set without ANALYSIS credit; CL-TA may shrink further after frozen TEST then ANALYSIS.",
            "TEST-ABORT is not on the predetermined TEST path; SC-ABORT ABORT is IUT trajectory.",
            "RESOURCE-ERROR constructions can collide with h_status_silence localisation accounting.",
            "Mixed VALID {h_normal, ...} with no T5 interval is INCONCLUSIVE.",
            "SC-SAME-KEY, SC-RESOURCE-ERROR, SC-INVALID-OBS are DETECT/ABLATION accounting only (not LOCATE).",
        ],
        "analysis": payload["analysis"],
        "openDecisions": payload["openDecisions"],
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    summary = run_census()
    print(
        json.dumps(
            {
                "writtenAttemptCount": summary["writtenAttemptCount"],
                "scoredAttemptCount": summary["scoredAttemptCount"],
                "operationalProblems": len(summary["operationalProblems"]),
                "raw": str(RAW_PATH),
                "summary": str(SUMMARY_PATH),
            }
        )
    )


if __name__ == "__main__":
    main()
