"""E6 IF-EXP-EVAL.  Sole reader of IF-EXP-TRUTH via TruthCapability."""

from __future__ import annotations

from typing import Any, Mapping

from a615a_sim.algorithm.library import EMPTY_DETAIL, project_cost
from a615a_sim.evaluator.guard import deny_algorithm_truth_access
from a615a_sim.evaluator.pipeline.timing import interval_outcome
from a615a_sim.evaluator.truth import IndependentTruthStore, TruthCapability, TruthRecord

ANSWERED_OUTCOMES = frozenset({"PASS", "FAIL"})
NOT_ANSWERED_VALIDITY = frozenset({"PRE-RUN-EXCLUDED", "ABSTAIN", "INCOMPLETE"})
NORMAL_HYPOTHESES = frozenset({"h_normal", "h-normal"})
DETECT_ONLY_SCENES = frozenset({"SC-INVALID-OBS", "SC-RESOURCE-ERROR", "SC-SAME-KEY"})
# metricFieldContracts.injectionStatus / faultDomain: design enums from IF-EXP-TRUTH.
INJECTION_STATUS_ENUM = {
    "normal": "NORMAL",
    "confirmed": "CONFIRMED",
    "unconfirmed": "UNCONFIRMED",
    "equivalent": "EQUIVALENT",
    "unresolved": "UNRESOLVED",
}
FAULT_DOMAIN_ENUM = {
    "normal": "NORMAL",
    "in-domain-non-equivalent": "IN-DOMAIN-NON-EQUIVALENT",
    "out-of-domain": "OUT-OF-DOMAIN",
    "unknown": "UNKNOWN",
}


class UndefinedDetectionOutcome(ValueError):
    """Raised when the metric dictionary / design JSON does not define PASS/FAIL."""


def _map_enum(raw: Any, table: Mapping[str, str]) -> Any:
    if raw is None:
        return None
    text = str(raw)
    if text in table.values():
        return text
    return table.get(text.lower(), text)


def _truth_fields(truth: Mapping[str, Any] | TruthRecord | None) -> dict[str, Any]:
    """Project IF-EXP-TRUTH only.  Fixture rows are never a truth source."""

    if truth is None:
        return {
            "truthHypothesis": None,
            "injectionStatus": None,
            "faultDomain": None,
            "equivalenceDisposition": None,
        }
    if isinstance(truth, TruthRecord):
        hypothesis = truth.truth_hypothesis
        status = truth.injection_status
        domain = truth.fault_domain_class
        disposition = truth.equivalence_disposition
    else:
        hypothesis = truth.get("truthHypothesis")
        status = truth.get("injectionStatus")
        domain = truth.get("faultDomain") or truth.get("faultDomainClass")
        disposition = truth.get("equivalenceDisposition")
    return {
        "truthHypothesis": hypothesis,
        "injectionStatus": _map_enum(status, INJECTION_STATUS_ENUM),
        "faultDomain": _map_enum(domain, FAULT_DOMAIN_ENUM),
        "equivalenceDisposition": disposition,
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
    """Detection outcome from the metric dictionary and design JSON only.

    Citations:
    - populations.POP-ANSWERED.retentionRule: ERROR / INCONCLUSIVE / NOT-ANSWERED
      are not answered; PRE-RUN-EXCLUDED, ABSTAIN, INCOMPLETE → NOT-ANSWERED.
    - populations.POP-ERROR: validity INVALID or outcome ERROR (SYN-INVALID-OBS,
      SYN-STOP-EMPTY / Stop-Empty, Stop-Error).
    - metrics.MET-INCONCLUSIVE.censoringRule and EXPERIMENT_PLAN T5: interval
      containment PASS, disjoint FAIL, overlap INCONCLUSIVE.  No timing claim
      when either interval is absent (DEC-CLOCK OPEN / RR-006 N5.4).
    - syntheticWalkthroughs.SYN-NORMAL: singleton {h_normal} → PASS.
    - syntheticWalkthroughs.SYN-FAIL-NONSINGLETON and EXPERIMENT_PLAN: a valid
      detection FAIL may be a non-singleton set that does not retain h_normal.
    - Mixed sets that still contain h_normal, with no T5 interval, are not
      defined (SYN-T5-OVERLAP is interval INCONCLUSIVE; SYN-PRE-ACTION is
      INCOMPLETE).  Do not treat them as FAIL (that would be a false fail on a
      qualified normal, POP-FALSE-FAILS / MET-FALSE-FAIL).
    """

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
    retained_normal = [item for item in final_hypotheses if item in NORMAL_HYPOTHESES]
    if len(final_hypotheses) == 1 and retained_normal:
        return "PASS"
    if final_hypotheses and not retained_normal:
        return "FAIL"
    if final_hypotheses:
        raise UndefinedDetectionOutcome(
            "design JSON does not define detection PASS/FAIL for a VALID "
            "candidate set that still contains h_normal together with other "
            "hypotheses when no T5 observation/requirement interval is present "
            "(metricFieldContracts.outcome; POP-FALSE-FAILS; SYN-T5-OVERLAP is "
            "interval-only INCONCLUSIVE)"
        )
    return "NOT-ANSWERED"


def assemble_attempt_row(
    *,
    scene: Mapping[str, Any],
    injection: Mapping[str, Any],
    truth: Mapping[str, Any] | None,
    run: Mapping[str, Any] | None,
    collect: Mapping[str, Any] | None,
    filtered: Mapping[str, Any],
) -> dict[str, Any]:
    deny_algorithm_truth_access(operation="e6-eval")
    truth_fields = _truth_fields(truth)
    validity = filtered["validityClass"]
    hypotheses = list((run or {}).get("finalHypotheses") or [])
    observation_interval = (run or {}).get("observationInterval")
    requirement_interval = scene.get("requirementInterval")
    outcome = derive_outcome(
        validity=validity,
        stop_class=None if run is None else run.get("stopClass"),
        observation_interval=observation_interval,
        requirement_interval=requirement_interval,
        final_hypotheses=hypotheses,
        t5_verdicts=None if run is None else run.get("t5Verdicts"),
    )
    charged = dict(
        (collect or {}).get("resourceLog", {}).get("detailCharges") or EMPTY_DETAIL
    )
    run_id = None if run is None else run.get("runId")
    scene_id = scene.get("sceneId")
    collision = (
        scene_id == "SC-RESOURCE-ERROR"
        and "h_status_silence" in hypotheses
    )
    row = {
        "id": injection.get("attemptId"),
        "label": "SIMULATED-IUT",
        "scenarioId": scene_id,
        "attemptId": injection.get("attemptId"),
        "runId": run_id,
        "armId": scene.get("algorithmVisibleFields", {}).get("registeredArm"),
        "baseSceneId": scene.get("baseSceneId"),
        "sceneSeed": scene.get("sceneSeed"),
        "constructionId": scene.get("constructionId"),
        "contrastId": scene.get("contrastId"),
        "pairingId": scene.get("pairingId"),
        "pairedArmId": None,
        "resetEvidenceRef": scene.get("resetEvidenceRef"),
        "resetConfirmed": bool(injection.get("injectionConfirmed")),
        "pairParentMetricIds": [],
        "updateStatus": None,
        "truthReference": {
            "ref": "IF-EXP-TRUTH.truthRecord",
            "visibility": "EVALUATOR-ONLY",
            "truthHypothesis": truth_fields["truthHypothesis"],
        },
        "injectionStatus": truth_fields["injectionStatus"],
        "faultDomain": truth_fields["faultDomain"],
        "validity": validity,
        "outcome": outcome,
        "stopClass": None if run is None else run.get("stopClass"),
        "stage": "PRE-RUN" if run is None else run.get("stage"),
        "observationInterval": observation_interval,
        "requirementInterval": requirement_interval,
        "endpointTopology": "NOT-APPLICABLE",
        "historyBefore": [],
        "compatibleState": list((run or {}).get("compatibleState") or hypotheses),
        "finalHypotheses": hypotheses,
        "localizationDecisionIssued": bool((run or {}).get("localizationDecisionIssued")),
        "singletonDecisionIssued": bool((run or {}).get("singletonDecisionIssued")),
        "resourcePolicy": (collect or {}).get("resourceLog", {}).get("mode")
        or scene.get("resourceMode"),
        "resourceStatus": None
        if run is None
        else (collect or {}).get("resourceLog", {}).get("statusClass"),
        "actionIssued": bool((run or {}).get("actionIssued")),
        "chargedCost": charged,
        "reviewSetupEffort": 0,
        "detectFamilyOnly": scene_id in DETECT_ONLY_SCENES,
        "resourceErrorSilenceCollision": collision,
        "producer": "IF-EXP-EVAL",
    }
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
        # RR-006 N5.3: INVALID-OBS / RESOURCE-ERROR / SAME-KEY (hypothesisId null)
        # are DETECT/abstain accounting only.  They never enter MET-TRUE-RETAINED
        # because loc_truth_scorable requires a non-null truth hypothesis.
        # RESOURCE-ERROR → h_status_silence is a wrong localisation collision.
        "detectFamilyOnlyAttemptIds": [
            str(row.get("attemptId"))
            for row in rows
            if row.get("detectFamilyOnly")
        ],
        "resourceErrorSilenceCollisionAttemptIds": [
            str(row.get("attemptId"))
            for row in rows
            if row.get("resourceErrorSilenceCollision")
        ],
        "clockClaims": "none-DEC-CLOCK-OPEN",
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
