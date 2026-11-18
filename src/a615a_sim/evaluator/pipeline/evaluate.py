"""E6 IF-EXP-EVAL.  Sole reader of IF-EXP-TRUTH via TruthCapability."""

from __future__ import annotations

from typing import Any, Mapping

from a615a_sim.algorithm.library import EMPTY_DETAIL, project_cost
from a615a_sim.evaluator.guard import deny_algorithm_truth_access
from a615a_sim.evaluator.pipeline.timing import interval_outcome
from a615a_sim.evaluator.truth import IndependentTruthStore, TruthCapability, TruthRecord

ANSWERED_OUTCOMES = frozenset({"PASS", "FAIL"})
NOT_ANSWERED_VALIDITY = frozenset({"PRE-RUN-EXCLUDED", "ABSTAIN", "INCOMPLETE"})


def _truth_fields(
    truth: Mapping[str, Any] | TruthRecord | None,
) -> dict[str, Any]:
    if truth is None:
        return {
            "truthHypothesis": None,
            "injectionStatus": None,
            "faultDomain": None,
            "equivalenceDisposition": None,
        }
    if isinstance(truth, TruthRecord):
        return {
            "truthHypothesis": truth.truth_hypothesis,
            "injectionStatus": truth.injection_status,
            "faultDomain": truth.fault_domain_class,
            "equivalenceDisposition": truth.equivalence_disposition,
        }
    return {
        "truthHypothesis": truth.get("truthHypothesis")
        or (truth.get("truthReference") or {}).get("truthHypothesis"),
        "injectionStatus": truth.get("injectionStatus"),
        "faultDomain": truth.get("faultDomain") or truth.get("faultDomainClass"),
        "equivalenceDisposition": truth.get("equivalenceDisposition"),
    }


def derive_outcome(
    *,
    validity: str,
    stop_class: str | None,
    observation_interval: Mapping[str, Any] | None,
    requirement_interval: Mapping[str, Any] | None,
    final_hypotheses: list[str],
    t5_verdicts: list[str] | None = None,
) -> str:
    if validity in NOT_ANSWERED_VALIDITY:
        return "NOT-ANSWERED"
    if validity == "INVALID":
        return "ERROR"
    timed = interval_outcome(observation_interval, requirement_interval)
    if timed:
        return timed
    if t5_verdicts and "INCONCLUSIVE" in t5_verdicts:
        return "INCONCLUSIVE"
    if stop_class in {"Stop-Error", "Stop-Empty"}:
        return "ERROR"
    if len(final_hypotheses) == 1 and final_hypotheses[0] in {"h-normal", "h_normal"}:
        return "PASS"
    if final_hypotheses:
        return "FAIL"
    return "NOT-ANSWERED"


def assemble_attempt_row(
    *,
    fixture: Mapping[str, Any] | None = None,
    scene: Mapping[str, Any],
    injection: Mapping[str, Any],
    truth: Mapping[str, Any] | None,
    run: Mapping[str, Any] | None,
    collect: Mapping[str, Any] | None,
    filtered: Mapping[str, Any],
) -> dict[str, Any]:
    deny_algorithm_truth_access(operation="e6-eval")
    source = dict(fixture or {})
    truth_fields = _truth_fields(truth if truth is not None else source.get("truthReference"))
    if source.get("truthReference"):
        truth_fields["truthHypothesis"] = source["truthReference"].get("truthHypothesis")
        if source.get("injectionStatus"):
            truth_fields["injectionStatus"] = source["injectionStatus"]
        if source.get("faultDomain"):
            truth_fields["faultDomain"] = source["faultDomain"]
    validity = filtered["validityClass"]
    hypotheses = list(
        (run or {}).get("finalHypotheses")
        or source.get("finalHypotheses")
        or []
    )
    observation_interval = source.get("observationInterval")
    requirement_interval = source.get("requirementInterval") or scene.get("requirementInterval")
    outcome = derive_outcome(
        validity=validity,
        stop_class=(run or {}).get("stopClass") or source.get("stopClass"),
        observation_interval=observation_interval,
        requirement_interval=requirement_interval,
        final_hypotheses=hypotheses,
        t5_verdicts=(run or {}).get("t5Verdicts"),
    )
    charged = dict(
        (collect or {}).get("resourceLog", {}).get("detailCharges")
        or source.get("chargedCost")
        or EMPTY_DETAIL
    )
    row = {
        "id": source.get("id"),
        "label": source.get("label", "SIMULATED-IUT"),
        "scenarioId": source.get("scenarioId") or scene.get("sceneId"),
        "attemptId": source.get("attemptId") or injection.get("attemptId"),
        "runId": None if run is None else (run.get("runId") if run else source.get("runId")),
        "armId": source.get("armId") or scene.get("algorithmVisibleFields", {}).get("registeredArm"),
        "baseSceneId": source.get("baseSceneId"),
        "sceneSeed": source.get("sceneSeed"),
        "constructionId": source.get("constructionId"),
        "contrastId": source.get("contrastId"),
        "pairingId": source.get("pairingId") or scene.get("pairingId"),
        "pairedArmId": source.get("pairedArmId"),
        "resetEvidenceRef": source.get("resetEvidenceRef") or scene.get("resetEvidenceRef"),
        "resetConfirmed": source.get("resetConfirmed"),
        "pairParentMetricIds": list(source.get("pairParentMetricIds") or []),
        "updateStatus": source.get("updateStatus"),
        "truthReference": {
            "ref": "IF-EXP-TRUTH.truthRecord",
            "visibility": "EVALUATOR-ONLY",
            "truthHypothesis": truth_fields["truthHypothesis"],
        },
        "injectionStatus": source.get("injectionStatus") or truth_fields["injectionStatus"],
        "faultDomain": source.get("faultDomain") or truth_fields["faultDomain"],
        "validity": validity,
        "outcome": outcome,
        "stopClass": None if run is None and source.get("runId") is None else (
            (run or {}).get("stopClass") if run else source.get("stopClass")
        ),
        "stage": source.get("stage") or ((run or {}).get("stage") if run else None),
        "observationInterval": observation_interval,
        "requirementInterval": requirement_interval,
        "endpointTopology": source.get("endpointTopology"),
        "historyBefore": list(source.get("historyBefore") or []),
        "compatibleState": list(source.get("compatibleState") or (run or {}).get("compatibleState") or []),
        "finalHypotheses": hypotheses,
        "localizationDecisionIssued": bool(
            source.get("localizationDecisionIssued")
            if fixture is not None
            else (run or {}).get("localizationDecisionIssued")
        ),
        "singletonDecisionIssued": bool(
            source.get("singletonDecisionIssued")
            if fixture is not None
            else (run or {}).get("singletonDecisionIssued")
        ),
        "resourcePolicy": source.get("resourcePolicy")
        or (collect or {}).get("resourceLog", {}).get("mode")
        or scene.get("resourceMode"),
        "resourceStatus": source.get("resourceStatus")
        or (collect or {}).get("resourceLog", {}).get("statusClass"),
        "actionIssued": bool(
            source.get("actionIssued") if fixture is not None else (run or {}).get("actionIssued")
        ),
        "chargedCost": charged,
        "reviewSetupEffort": source.get("reviewSetupEffort", 0),
        "producer": "IF-EXP-EVAL",
    }
    if run is None and (fixture or {}).get("runId") is None:
        row["runId"] = None
        row["stopClass"] = None
    return row


def population_sets(rows: list[Mapping[str, Any]]) -> dict[str, set[str]]:
    """Metric-dictionary populations.  Excluded attempts remain in POP-ATTEMPTS."""

    by_id = {str(row.get("attemptId", "")): row for row in rows if row.get("attemptId")}
    attempts = set(by_id)
    answered = {
        aid
        for aid, row in by_id.items()
        if row.get("runId") is not None
        and row.get("validity") == "VALID"
        and row.get("outcome") in ANSWERED_OUTCOMES
    }
    normal = {
        aid
        for aid, row in by_id.items()
        if row.get("runId") is not None
        and row.get("injectionStatus") == "NORMAL"
        and row.get("faultDomain") == "NORMAL"
        and row.get("validity") == "VALID"
    }
    faults = {
        aid
        for aid, row in by_id.items()
        if row.get("injectionStatus") == "CONFIRMED"
        and row.get("faultDomain") == "IN-DOMAIN-NON-EQUIVALENT"
        and row.get("runId") is not None
    }
    misses = {aid for aid in faults if by_id[aid].get("outcome") == "PASS"}
    false_fails = {aid for aid in normal if by_id[aid].get("outcome") == "FAIL"}
    answered_truth_scorable = {
        aid
        for aid in answered
        if by_id[aid].get("truthReference", {}).get("truthHypothesis") is not None
    }
    conditional_error = (misses | false_fails) & answered_truth_scorable
    abstain = {aid for aid, row in by_id.items() if row.get("validity") == "ABSTAIN"}
    inconclusive = {aid for aid, row in by_id.items() if row.get("outcome") == "INCONCLUSIVE"}
    error = {
        aid
        for aid, row in by_id.items()
        if row.get("outcome") == "ERROR" or row.get("validity") == "INVALID"
    }
    incomplete = {
        aid
        for aid, row in by_id.items()
        if row.get("validity") == "INCOMPLETE" or row.get("resourceStatus") == "BUDGET-EXHAUSTED"
    }
    loc_eligible = set(faults)
    loc_decision = {
        aid for aid in loc_eligible if by_id[aid].get("localizationDecisionIssued") is True
    }
    loc_truth_scorable = {
        aid
        for aid in loc_decision
        if by_id[aid].get("validity") == "VALID"
        and by_id[aid].get("truthReference", {}).get("truthHypothesis") is not None
    }
    retained = {
        aid
        for aid in loc_decision
        if aid in loc_truth_scorable
        and by_id[aid].get("truthReference", {}).get("truthHypothesis")
        in by_id[aid].get("finalHypotheses", [])
    }
    excluded = loc_truth_scorable - retained
    singleton = {
        aid
        for aid in loc_decision
        if by_id[aid].get("singletonDecisionIssued") is True
        and len(by_id[aid].get("finalHypotheses", [])) == 1
    }
    singleton_truth_scorable = {aid for aid in singleton if aid in loc_truth_scorable}
    singleton_correct = {
        aid
        for aid in singleton_truth_scorable
        if by_id[aid].get("truthReference", {}).get("truthHypothesis")
        == by_id[aid].get("finalHypotheses", [None])[0]
    }
    truth_missing = {
        aid
        for aid in attempts
        if by_id[aid].get("truthReference", {}).get("truthHypothesis") is None
        and (aid in answered or aid in loc_decision or aid in singleton)
    }
    rounds = {
        aid
        for aid, row in by_id.items()
        if row.get("runId") is not None and row.get("resourcePolicy") == "ROUNDS"
    }
    return {
        "POP-ATTEMPTS": attempts,
        "POP-ANSWERED": answered,
        "POP-ANSWERED-TRUTH-SCORABLE": answered_truth_scorable,
        "POP-TRUTH-MISSING": truth_missing,
        "POP-QUALIFIED-NORMAL": normal,
        "POP-CONFIRMED-FAULT": faults,
        "POP-MISSES": misses,
        "POP-FALSE-FAILS": false_fails,
        "POP-CONDITIONAL-ERROR": conditional_error,
        "POP-ABSTAIN": abstain,
        "POP-INCONCLUSIVE": inconclusive,
        "POP-ERROR": error,
        "POP-INCOMPLETE": incomplete,
        "POP-LOCALIZATION-ELIGIBLE": loc_eligible,
        "POP-LOCALIZATION-DECISION": loc_decision,
        "POP-LOCALIZATION-TRUTH-SCORABLE": loc_truth_scorable,
        "POP-TRUE-RETAINED": retained,
        "POP-TRUE-EXCLUDED": excluded,
        "POP-SINGLETON-DECISION": singleton,
        "POP-SINGLETON-TRUTH-SCORABLE": singleton_truth_scorable,
        "POP-SINGLETON-CORRECT": singleton_correct,
        "POP-ROUNDS": rounds,
    }


def metric_cells(rows: list[Mapping[str, Any]]) -> dict[str, Any]:
    pops = population_sets(rows)
    n = len(pops["POP-ATTEMPTS"])

    def proportion(num: str, den: str) -> Any:
        denom = len(pops[den])
        if denom == 0:
            return "N/A"
        return len(pops[num]) / denom

    four_vectors = []
    for row in rows:
        charged = row.get("chargedCost") or {}
        four_vectors.append(
            project_cost(
                {
                    "acquisition": int(charged.get("acquisition") or 0),
                    "computation": int(charged.get("computation") or 0),
                    "preparation": int(charged.get("preparation") or 0),
                    "recovery": int(charged.get("recovery") or 0),
                    "retry": int(charged.get("retry") or 0),
                }
            )
        )
    return {
        "MET-ATTEMPTS": n,
        "MET-ANSWERED-COVERAGE": proportion("POP-ANSWERED", "POP-ATTEMPTS"),
        "MET-CONDITIONAL-DETECTION-ERROR": proportion(
            "POP-CONDITIONAL-ERROR", "POP-ANSWERED-TRUTH-SCORABLE"
        ),
        "MET-TRUTH-SCORABLE-COVERAGE": proportion(
            "POP-ANSWERED-TRUTH-SCORABLE", "POP-ANSWERED"
        ),
        "MET-TRUTH-MISSING": proportion("POP-TRUTH-MISSING", "POP-ATTEMPTS"),
        "MET-MISS": proportion("POP-MISSES", "POP-CONFIRMED-FAULT"),
        "MET-FALSE-FAIL": proportion("POP-FALSE-FAILS", "POP-QUALIFIED-NORMAL"),
        "MET-ABSTAIN": proportion("POP-ABSTAIN", "POP-ATTEMPTS"),
        "MET-INCONCLUSIVE": proportion("POP-INCONCLUSIVE", "POP-ATTEMPTS"),
        "MET-ERROR": proportion("POP-ERROR", "POP-ATTEMPTS"),
        "MET-INCOMPLETE": proportion("POP-INCOMPLETE", "POP-ATTEMPTS"),
        "MET-LOCALIZATION-COVERAGE": proportion(
            "POP-LOCALIZATION-DECISION", "POP-LOCALIZATION-ELIGIBLE"
        ),
        "MET-TRUE-RETAINED": proportion("POP-TRUE-RETAINED", "POP-LOCALIZATION-TRUTH-SCORABLE"),
        "MET-TRUE-EXCLUDED": proportion("POP-TRUE-EXCLUDED", "POP-LOCALIZATION-TRUTH-SCORABLE"),
        "MET-SINGLETON-CORRECT": proportion(
            "POP-SINGLETON-CORRECT", "POP-SINGLETON-TRUTH-SCORABLE"
        ),
        "MET-FINAL-CANDIDATES": [
            len(row.get("finalHypotheses") or [])
            for row in rows
            if str(row.get("attemptId")) in pops["POP-LOCALIZATION-ELIGIBLE"]
        ],
        "MET-COST-VECTOR": four_vectors,
        "MET-ROUNDS": [
            1 if row.get("actionIssued") else 0
            for row in rows
            if str(row.get("attemptId")) in pops["POP-ROUNDS"]
        ],
        "attemptDenominator": n,
        "answeredSubsetDenominator": len(pops["POP-ANSWERED"]),
        "populations": {key: sorted(value) for key, value in pops.items()},
        "label": "SIMULATED-IUT / PILOT-ACCOUNTING",
    }


def evaluate_with_store(
    store: IndependentTruthStore,
    attempt_id: str,
    capability: TruthCapability,
    **parts: Any,
) -> dict[str, Any]:
    deny_algorithm_truth_access(operation="e6-eval-store")
    truth = store.get(attempt_id, capability)
    return assemble_attempt_row(truth=truth.as_mapping(capability), **parts)
