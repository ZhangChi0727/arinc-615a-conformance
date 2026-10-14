"""Validate the bounded CL-TAV experiment implementation design.

The checker establishes snapshot provenance, structural closure, semantic gates,
and synthetic finite-population accounting.  It does not approve novelty,
mathematical arguments, protocol interpretation, or confirmatory execution.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
DESIGN_PATH = Path("configs/research/cltav_experiment_design.json")
SCHEMA_PATH = Path("configs/research/cltav_experiment_design.schema.json")

REQUIRED_BINDINGS = {
    "configs/research/cltav_interface_registry.json": "ACCEPTED-AUTHORITY",
    "configs/engineering/cltav_development_contracts.json": "ACCEPTED-AUTHORITY",
    "docs/research/CLAIM_EVIDENCE_MATRIX.md": "SUCCESSOR-BASELINE",
    "docs/research/EXPERIMENT_PLAN.md": "SUCCESSOR-BASELINE",
    "docs/research/methodology/RR-2026-001_test_analysis_conformance_methodology.md": "ACCEPTED-AUTHORITY",
    "docs/research/publication/drafts/taes-cltav/manuscript_manifest.json": "SUCCESSOR-BASELINE",
    "configs/requirements/arinc_615a3_m1_crs.json": "ACCEPTED-AUTHORITY",
    "configs/models/arinc_615a3_m2_model.json": "ACCEPTED-AUTHORITY",
    "configs/research/literature/evidence_ledger.csv": "ACCEPTED-AUTHORITY",
}
REQUIRED_DECISIONS = {
    "DEC-MATH-REVIEW", "DEC-IUT", "DEC-TRUTH", "DEC-EQUIV",
    "DEC-SAMPLE", "DEC-RESOURCE", "DEC-CLOCK", "DEC-DISCLOSURE",
}
REQUIRED_DEPENDENCIES = {
    "DEP-IUT", "DEP-TRUTH", "DEP-CLOCK", "DEP-RESET", "DEP-OBS-QUAL",
    "DEP-RESOURCE", "DEP-REGISTRATION", "DEP-EQUIV", "DEP-SAMPLE",
    "DEP-645-RUNTIME",
}
REQUIRED_METRICS = {
    "MET-ATTEMPTS", "MET-ANSWERED-COVERAGE", "MET-CONDITIONAL-DETECTION-ERROR",
    "MET-MISS", "MET-FALSE-FAIL", "MET-ABSTAIN", "MET-INCONCLUSIVE",
    "MET-ERROR", "MET-INCOMPLETE", "MET-LOCALIZATION-COVERAGE",
    "MET-TRUE-RETAINED", "MET-TRUE-EXCLUDED", "MET-SINGLETON-CORRECT",
    "MET-FINAL-CANDIDATES", "MET-COST-VECTOR", "MET-ROUNDS",
    "MET-ABLATION-DELTA",
}
REQUIRED_ANALYSES = {"AN-FLOW", "AN-PROPORTION", "AN-DISTRIBUTION", "AN-PAIRED"}
REQUIRED_POPULATIONS = {
    "POP-ATTEMPTS", "POP-ANSWERED", "POP-QUALIFIED-NORMAL",
    "POP-CONFIRMED-FAULT", "POP-MISSES", "POP-FALSE-FAILS",
    "POP-CONDITIONAL-ERROR", "POP-ABSTAIN", "POP-INCONCLUSIVE", "POP-ERROR",
    "POP-INCOMPLETE", "POP-LOCALIZATION-ELIGIBLE", "POP-LOCALIZATION-DECISION",
    "POP-TRUE-RETAINED", "POP-TRUE-EXCLUDED", "POP-SINGLETON-DECISION",
    "POP-SINGLETON-CORRECT", "POP-PAIRED-ELIGIBLE", "POP-ROUNDS",
}
ROW_FIELDS = {
    "attemptId", "runId", "pairingId", "injectionStatus", "faultDomain", "validity",
    "outcome", "stopClass", "stage", "observationInterval", "requirementInterval",
    "historyBefore", "compatibleState", "finalHypotheses", "localizationDecisionIssued",
    "singletonDecisionIssued", "resourcePolicy", "resourceStatus", "actionIssued", "chargedCost",
}
NESTED_ROW_FIELDS = {
    "truthReference.ref", "truthReference.visibility", "truthReference.truthHypothesis",
    "chargedCost.acquisition", "chargedCost.computation", "chargedCost.preparation",
    "chargedCost.recovery", "chargedCost.retry",
}


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _json_bytes(blob: bytes, label: str, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(blob.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"bound authority {label} is not valid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"bound authority {label} must be a JSON object")
        return {}
    return value


def _duplicates(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if value and count > 1)


def _git_output(root: Path, *args: str, text: bool = False) -> bytes | str:
    return subprocess.check_output(
        ["git", *args], cwd=root, text=text, stderr=subprocess.STDOUT
    )


def _safe_relative(path: str) -> bool:
    candidate = Path(path)
    return bool(path) and not candidate.is_absolute() and ".." not in candidate.parts


def _ids(rows: Any, label: str, errors: list[str]) -> set[str]:
    if not isinstance(rows, list):
        errors.append(f"{label} must be an array")
        return set()
    values = [str(row.get("id", "")) for row in rows if isinstance(row, dict)]
    for value in _duplicates(values):
        errors.append(f"duplicate {label} id {value}")
    return {value for value in values if value}


def _rows(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = data.get(key, [])
    if not isinstance(value, list):
        return []
    return [row for row in value if isinstance(row, dict)]


def _refs(values: Any, allowed: set[str], label: str) -> list[str]:
    if not isinstance(values, list):
        return [f"{label} references must be an array"]
    return [f"unknown {label} reference {value}" for value in values if value not in allowed]


def _schema_errors(schema: dict[str, Any], data: Any) -> list[str]:
    try:
        Draft202012Validator.check_schema(schema)
        issues = Draft202012Validator(schema).iter_errors(data)
        rendered = []
        for issue in issues:
            location = ".".join(str(part) for part in issue.absolute_path) or "<root>"
            rendered.append(f"schema {location}: {issue.message}")
        return sorted(rendered)
    except Exception as exc:  # jsonschema emits several documented subclasses
        return [f"schema validation unavailable: {type(exc).__name__}: {exc}"]


def _snapshot_from_bindings(
    root: Path, data: dict[str, Any], errors: list[str]
) -> dict[str, bytes]:
    bindings = _rows(data, "inputBindings")
    paths = [str(row.get("path", "")) for row in bindings]
    for value in _duplicates(paths):
        errors.append(f"duplicate input binding {value}")

    by_path = {str(row.get("path", "")): row for row in bindings}
    missing = sorted(set(REQUIRED_BINDINGS) - set(by_path))
    extra = sorted(set(by_path) - set(REQUIRED_BINDINGS))
    for path in missing:
        errors.append(f"required input binding missing: {path}")
    for path in extra:
        errors.append(f"unexpected input binding: {path}")

    base = data.get("identity", {}).get("baseCommit", "") if isinstance(data.get("identity"), dict) else ""
    snapshot: dict[str, bytes] = {}
    for path, expected_role in REQUIRED_BINDINGS.items():
        row = by_path.get(path)
        if row is None:
            continue
        if row.get("role") != expected_role:
            errors.append(f"input binding role mismatch for {path}: expected {expected_role}")
        if not _safe_relative(path):
            errors.append(f"unsafe input binding path {path!r}")
            continue
        oid = row.get("gitBlobOid", "")
        try:
            resolved = str(_git_output(root, "rev-parse", f"{base}:{path}", text=True)).strip()
            blob = bytes(_git_output(root, "cat-file", "blob", str(oid)))
        except (subprocess.CalledProcessError, OSError) as exc:
            errors.append(f"cannot resolve bound Git blob {path}: {exc}")
            continue
        if resolved != oid:
            errors.append(f"input binding OID mismatch for {path}: {oid} != {resolved}")
        digest = hashlib.sha256(blob).hexdigest()
        if digest != row.get("sha256"):
            errors.append(f"input binding SHA-256 mismatch for {path}")
        if resolved == oid and digest == row.get("sha256"):
            snapshot[path] = blob
    return snapshot


def _authority_models(snapshot: dict[str, bytes], errors: list[str]) -> dict[str, Any]:
    required_json = [
        "configs/research/cltav_interface_registry.json",
        "configs/engineering/cltav_development_contracts.json",
        "configs/requirements/arinc_615a3_m1_crs.json",
        "configs/models/arinc_615a3_m2_model.json",
    ]
    models: dict[str, Any] = {}
    for path in required_json:
        blob = snapshot.get(path)
        models[path] = _json_bytes(blob, path, errors) if blob is not None else {}
    models["claimText"] = snapshot.get(
        "docs/research/CLAIM_EVIDENCE_MATRIX.md", b""
    ).decode("utf-8-sig", errors="replace")
    evidence_blob = snapshot.get("configs/research/literature/evidence_ledger.csv", b"")
    try:
        evidence_rows = list(csv.DictReader(io.StringIO(evidence_blob.decode("utf-8-sig"))))
    except (UnicodeDecodeError, csv.Error) as exc:
        errors.append(f"bound evidence ledger is not parseable: {exc}")
        evidence_rows = []
    models["evidenceIds"] = {row.get("evidence_id", "") or row.get("evidenceId", "") for row in evidence_rows}
    if not models["evidenceIds"] and evidence_rows:
        models["evidenceIds"] = {next(iter(row.values()), "") for row in evidence_rows}
    return models


def _field_reference_errors(
    references: Any, records: dict[str, set[str]], interfaces: dict[str, set[str]]
) -> list[str]:
    errors: list[str] = []
    if not isinstance(references, list):
        return ["requiredFields must be an array"]
    for reference in references:
        if reference in ROW_FIELDS or reference in NESTED_ROW_FIELDS:
            continue
        if not isinstance(reference, str):
            errors.append(f"field reference must be text: {reference!r}")
            continue
        owner, separator, field = reference.partition(".")
        if not separator or not field:
            errors.append(f"unknown synthetic or authority field {reference}")
        elif owner in records and field not in records[owner]:
            errors.append(f"unknown record field {reference}")
        elif owner in interfaces and field not in interfaces[owner]:
            errors.append(f"unknown interface output {reference}")
        elif owner not in records and owner not in interfaces:
            errors.append(f"unknown field-reference owner {owner}")
    return errors


def _population_sets(data: dict[str, Any]) -> dict[str, set[str]]:
    rows = _rows(data, "syntheticWalkthroughs")
    by_id = {str(row.get("attemptId", "")): row for row in rows if row.get("attemptId")}
    attempts = set(by_id)
    answered = {aid for aid, row in by_id.items() if row.get("validity") == "VALID" and row.get("outcome") in {"PASS", "FAIL"}}
    normal = {aid for aid, row in by_id.items() if row.get("injectionStatus") == "NORMAL" and row.get("faultDomain") == "NORMAL" and row.get("validity") == "VALID"}
    faults = {aid for aid, row in by_id.items() if row.get("injectionStatus") == "CONFIRMED" and row.get("faultDomain") == "IN-DOMAIN-NON-EQUIVALENT" and row.get("runId") is not None}
    misses = {aid for aid in faults if by_id[aid].get("outcome") == "PASS"}
    false_fails = {aid for aid in normal if by_id[aid].get("outcome") == "FAIL"}
    conditional_error = (misses | false_fails) & answered
    abstain = {aid for aid, row in by_id.items() if row.get("validity") == "ABSTAIN"}
    inconclusive = {aid for aid, row in by_id.items() if row.get("outcome") == "INCONCLUSIVE"}
    error = {aid for aid, row in by_id.items() if row.get("outcome") == "ERROR" or row.get("validity") == "INVALID"}
    incomplete = {aid for aid, row in by_id.items() if row.get("validity") == "INCOMPLETE" or row.get("resourceStatus") == "BUDGET-EXHAUSTED"}
    loc_eligible = set(faults)
    loc_decision = {aid for aid in loc_eligible if by_id[aid].get("localizationDecisionIssued") is True}
    retained = {
        aid for aid in loc_decision
        if by_id[aid].get("truthReference", {}).get("truthHypothesis") in by_id[aid].get("finalHypotheses", [])
    }
    excluded = loc_decision - retained
    singleton = {
        aid for aid in loc_decision
        if by_id[aid].get("singletonDecisionIssued") is True
        and len(by_id[aid].get("finalHypotheses", [])) == 1
    }
    singleton_correct = {
        aid for aid in singleton
        if by_id[aid].get("truthReference", {}).get("truthHypothesis") == by_id[aid].get("finalHypotheses", [None])[0]
    }
    pairing_counts = Counter(
        str(row.get("pairingId")) for row in rows if row.get("pairingId") is not None
    )
    paired = {pair_id for pair_id, count in pairing_counts.items() if count == 2}
    rounds = {
        aid for aid, row in by_id.items()
        if row.get("runId") is not None and row.get("resourcePolicy") == "ROUNDS"
    }
    return {
        "POP-ATTEMPTS": attempts, "POP-ANSWERED": answered,
        "POP-QUALIFIED-NORMAL": normal, "POP-CONFIRMED-FAULT": faults,
        "POP-MISSES": misses, "POP-FALSE-FAILS": false_fails,
        "POP-CONDITIONAL-ERROR": conditional_error, "POP-ABSTAIN": abstain,
        "POP-INCONCLUSIVE": inconclusive, "POP-ERROR": error,
        "POP-INCOMPLETE": incomplete, "POP-LOCALIZATION-ELIGIBLE": loc_eligible,
        "POP-LOCALIZATION-DECISION": loc_decision, "POP-TRUE-RETAINED": retained,
        "POP-TRUE-EXCLUDED": excluded, "POP-SINGLETON-DECISION": singleton,
        "POP-SINGLETON-CORRECT": singleton_correct, "POP-PAIRED-ELIGIBLE": paired,
        "POP-ROUNDS": rounds,
    }


def _validate_walkthroughs(data: dict[str, Any], scenario_ids: set[str]) -> list[str]:
    errors: list[str] = []
    rows = _rows(data, "syntheticWalkthroughs")
    attempt_ids = [str(row.get("attemptId", "")) for row in rows]
    for duplicate in _duplicates(attempt_ids):
        errors.append(f"duplicate synthetic attempt {duplicate}")
    for row in rows:
        row_id = row.get("id", "<unknown>")
        if row.get("label") != "SYNTHETIC-DESIGN-WALKTHROUGH":
            errors.append(f"walkthrough {row_id} is not explicitly synthetic")
        if row.get("scenarioId") not in scenario_ids:
            errors.append(f"walkthrough {row_id} has unknown scenario {row.get('scenarioId')}")
        truth = row.get("truthReference")
        if not isinstance(truth, dict) or truth.get("ref") != "IF-EXP-TRUTH.truthRecord" or truth.get("visibility") != "EVALUATOR-ONLY":
            errors.append(f"walkthrough {row_id} lacks typed evaluator-only truth")
        if row.get("injectionStatus") in {"UNCONFIRMED", "EQUIVALENT", "UNRESOLVED"} and row.get("runId") is not None:
            errors.append(f"walkthrough {row_id} invents a run for a pre-run excluded injection")
        if row.get("runId") is None and (row.get("resourcePolicy") != "NOT-RUN" or row.get("resourceStatus") != "NOT-RUN"):
            errors.append(f"walkthrough {row_id} assigns a resource policy/status to a non-run")
        if row.get("runId") is not None and row.get("resourcePolicy") == "NOT-RUN":
            errors.append(f"walkthrough {row_id} hides the resource policy of an admitted run")
        if row.get("resourceStatus") == "BUDGET-EXHAUSTED" and row.get("stopClass") != "Stop-Budget":
            errors.append(f"walkthrough {row_id} has budget exhaustion without Stop-Budget")
        if row.get("outcome") in {"PASS", "FAIL"} and row.get("validity") != "VALID":
            errors.append(f"walkthrough {row_id} assigns PASS/FAIL to invalid evidence")
        if row.get("outcome") == "ERROR" and row.get("localizationDecisionIssued"):
            errors.append(f"walkthrough {row_id} cannot count ERROR as a localization decision")
        final = row.get("finalHypotheses", [])
        if row.get("singletonDecisionIssued") and (not row.get("localizationDecisionIssued") or len(final) != 1):
            errors.append(f"walkthrough {row_id} has an invalid singleton decision")
        if row.get("stopClass") in {"Stop-645", "Stop-Budget"} and row.get("singletonDecisionIssued"):
            errors.append(f"walkthrough {row_id} lets {row.get('stopClass')} masquerade as a singleton decision")
        if row.get("stopClass") == "Stop-Empty":
            if final or row.get("stage") != "POST-UPDATE" or row.get("outcome") != "ERROR":
                errors.append(f"walkthrough {row_id} violates Stop-Empty stage/outcome priority")
        if row.get("stopClass") == "Stop-645" and row.get("stage") != "POST-UPDATE":
            errors.append(f"walkthrough {row_id} violates Stop-645 stage priority")
        if row.get("stage") == "PRE-ACTION" and (row.get("actionIssued") or any(row.get("chargedCost", {}).values())):
            errors.append(f"walkthrough {row_id} charges or issues an action before admission")
        if row.get("stopClass") in {"Stop-645", "Stop-Budget"} and row.get("actionIssued") and sum(row.get("chargedCost", {}).values()) <= 0:
            errors.append(f"walkthrough {row_id} hides spent cost at {row.get('stopClass')}")
        if row_id == "SYN-T5-OVERLAP":
            observed = row.get("observationInterval")
            required = row.get("requirementInterval")
            if not isinstance(observed, dict) or not isinstance(required, dict):
                errors.append("SYN-T5-OVERLAP lacks a real measurement/requirement interval witness")
            else:
                if observed.get("unit") != required.get("unit"):
                    errors.append("SYN-T5-OVERLAP interval units do not match")
                try:
                    valid_order = observed["lower"] <= observed["upper"] and required["lower"] <= required["upper"]
                    overlaps = max(observed["lower"], required["lower"]) <= min(observed["upper"], required["upper"])
                except (KeyError, TypeError):
                    valid_order = overlaps = False
                if not valid_order or not overlaps or row.get("outcome") != "INCONCLUSIVE":
                    errors.append("SYN-T5-OVERLAP does not witness an inconclusive interval overlap")
    return errors


def validate_design(root: Path = ROOT, design: dict[str, Any] | None = None) -> list[str]:
    try:
        data = design if design is not None else _read_json(root / DESIGN_PATH)
        schema = _read_json(root / SCHEMA_PATH)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read experiment-design input: {exc}"]
    if not isinstance(data, dict) or not isinstance(schema, dict):
        return ["experiment design and schema must be JSON objects"]

    errors = _schema_errors(schema, data)
    # Semantic routines assume the versioned shape.  Returning structured
    # schema diagnostics here is deliberate: malformed nested rows must never
    # reach ad-hoc access paths or surface as a traceback.
    if errors:
        return errors
    snapshot = _snapshot_from_bindings(root, data, errors)
    authorities = _authority_models(snapshot, errors)
    registry = authorities.get("configs/research/cltav_interface_registry.json", {})
    development = authorities.get("configs/engineering/cltav_development_contracts.json", {})
    m1 = authorities.get("configs/requirements/arinc_615a3_m1_crs.json", {})

    registry_arms = set(registry.get("arms", []))
    registry_families = set(registry.get("experimentIds", []))
    algorithm_rows = [row for row in registry.get("interfaces", []) if isinstance(row, dict)]
    experiment_rows = [row for row in registry.get("experimentInterfaces", []) if isinstance(row, dict)]
    registry_algorithm = {row.get("id") for row in algorithm_rows}
    registry_experiment = {row.get("id") for row in experiment_rows}
    development_scenario_rows = {
        row.get("id"): row for row in development.get("experimentScenarios", []) if isinstance(row, dict)
    }
    development_scenarios = set(development_scenario_rows)
    development_matrix = {
        row.get("id") for row in development.get("acceptanceMatrix", []) if isinstance(row, dict)
    }
    acceptance_cases = {
        row.get("id") for row in development.get("acceptanceCases", []) if isinstance(row, dict)
    }
    development_records = {
        row.get("id"): set(row.get("fields", []))
        for row in development.get("recordContracts", []) if isinstance(row, dict)
    }
    interface_outputs = {
        row.get("id"): set(row.get("outputs", [])) for row in [*algorithm_rows, *experiment_rows]
    }
    crs_ids = {row.get("id") for row in m1.get("requirements", []) if isinstance(row, dict)}

    refs = data.get("references", {}) if isinstance(data.get("references"), dict) else {}
    expected_refs = (
        ("arms", registry_arms), ("families", registry_families),
        ("scenarios", development_scenarios), ("acceptanceMatrix", development_matrix),
        ("algorithmInterfaces", registry_algorithm), ("experimentInterfaces", registry_experiment),
        ("records", set(development_records)),
    )
    for key, expected in expected_refs:
        actual = set(refs.get(key, [])) if isinstance(refs.get(key, []), list) else set()
        if actual != expected:
            errors.append(f"references.{key} must equal its bound Git authority: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}")
    for claim_id in refs.get("claims", []) if isinstance(refs.get("claims"), list) else []:
        if not re.search(rf"\|\s*{re.escape(str(claim_id))}\s*\|", authorities.get("claimText", "")):
            errors.append(f"unknown claim reference {claim_id} in bound Git claim matrix")
    evidence_ids = authorities.get("evidenceIds", set())
    for evidence_id in refs.get("evidenceIds", []) if isinstance(refs.get("evidenceIds"), list) else []:
        if evidence_id not in evidence_ids:
            errors.append(f"unknown evidence reference {evidence_id} in bound Git evidence ledger")

    argument_rows = _rows(data, "claimArguments")
    argument_values = [str(row.get("claimId", "")) for row in argument_rows]
    for duplicate in _duplicates(argument_values):
        errors.append(f"duplicate claim argument id {duplicate}")
    argument_ids = {value for value in argument_values if value}
    if argument_ids != {"CL-C1", "CL-C2"}:
        errors.append("claimArguments must contain exactly CL-C1 and CL-C2")

    arm_ids = _ids(data.get("arms"), "arm", errors)
    if arm_ids != registry_arms:
        errors.append(f"arm design must contain exactly {sorted(registry_arms)}")
    expected_arm_costs = {
        "CL-T": {"acquisition", "preparation", "retry"},
        "CL-A": {"computation"},
        "CL-TA": {"acquisition", "computation", "preparation", "retry"},
        "CL-LOOP": {"acquisition", "computation", "preparation", "retry"},
    }
    for arm in _rows(data, "arms"):
        for item in arm.get("visibleInputs", []) if isinstance(arm.get("visibleInputs"), list) else []:
            if not isinstance(item, dict):
                continue
            reference = item.get("ref", "")
            if reference.startswith("IF-EXP-TRUTH.") or item.get("role") not in {"ALGORITHM-INITIAL", "ALGORITHM-OWN-ACTION"}:
                errors.append(f"typed truth leakage or invalid visibility in arm {arm.get('id')}: {reference}")
            errors.extend(_field_reference_errors([reference], development_records, interface_outputs))
        if arm.get("id") in {"CL-T", "CL-A", "CL-TA"} and arm.get("feedback"):
            errors.append(f"non-loop arm {arm.get('id')} cannot receive feedback")
        if arm.get("id") == "CL-A" and any(item.get("role") == "ALGORITHM-OWN-ACTION" for item in arm.get("visibleInputs", []) if isinstance(item, dict)):
            errors.append("CL-A cannot receive records from an action it did not execute")
        arm_id = arm.get("id")
        if arm_id in expected_arm_costs and set(arm.get("costComponents", [])) != expected_arm_costs[arm_id]:
            errors.append(f"arm {arm_id} cost projection disagrees with the registered fair-comparison contract")

    decision_ids = _ids(data.get("pendingDecisions"), "pending decision", errors)
    if decision_ids != REQUIRED_DECISIONS:
        errors.append(f"pending decisions must remain complete: missing={sorted(REQUIRED_DECISIONS-decision_ids)}, extra={sorted(decision_ids-REQUIRED_DECISIONS)}")
    for decision in _rows(data, "pendingDecisions"):
        if decision.get("status") != "OPEN":
            errors.append(f"pending decision {decision.get('id')} cannot be marked complete by this design")
        for field in ("ownerRole", "inputEvidence", "selectionProcedure", "freezeBy", "closureWitness"):
            if not decision.get(field):
                errors.append(f"pending decision {decision.get('id')} lacks {field}")

    dependency_ids = _ids(data.get("dependencies"), "dependency", errors)
    if dependency_ids != REQUIRED_DEPENDENCIES:
        errors.append(f"dependencies must remain complete: missing={sorted(REQUIRED_DEPENDENCIES-dependency_ids)}, extra={sorted(dependency_ids-REQUIRED_DEPENDENCIES)}")
    scenario_ids = _ids(data.get("scenarios"), "scenario", errors)
    if scenario_ids != development_scenarios:
        errors.append(f"scenario design must contain exactly {sorted(development_scenarios)}")
    for scenario in _rows(data, "scenarios"):
        scenario_id = scenario.get("id")
        errors.extend(_refs(scenario.get("familyIds"), registry_families, "experiment family"))
        errors.extend(_refs(scenario.get("acceptanceMatrixRefs"), development_matrix, "acceptance-matrix"))
        errors.extend(_refs(scenario.get("acceptanceCaseRefs"), acceptance_cases, "acceptance-case"))
        errors.extend(_refs(scenario.get("dependencyIds"), dependency_ids, "dependency"))
        errors.extend(_refs(scenario.get("crsRefs"), crs_ids, "CRS"))
        if scenario.get("developmentScenarioRef") != scenario_id:
            errors.append(f"scenario {scenario_id} must bind its exact development scenario")
        accepted = development_scenario_rows.get(scenario_id, {})
        if accepted and scenario.get("serviceScope") != accepted.get("serviceScope"):
            errors.append(f"scenario {scenario_id} service scope disagrees with bound Git development authority")
        if scenario.get("crsDisposition") == "TOOL-OR-EXPERIMENT-N/A" and scenario.get("crsRefs"):
            errors.append(f"scenario {scenario_id} cannot combine N/A CRS disposition with CRS references")
        if scenario.get("crsDisposition") == "APPLICABLE" and not scenario.get("crsRefs"):
            errors.append(f"scenario {scenario_id} lacks applicable CRS references")

    disposition_ids = _ids(data.get("acceptanceMatrixDispositions"), "acceptance-matrix disposition", errors)
    if disposition_ids != development_matrix:
        errors.append(f"all 14 acceptance-matrix rows require disposition: missing={sorted(development_matrix-disposition_ids)}, extra={sorted(disposition_ids-development_matrix)}")
    disposition_consumers = scenario_ids | dependency_ids | registry_families
    for row in _rows(data, "acceptanceMatrixDispositions"):
        errors.extend(_refs(row.get("consumerRefs"), disposition_consumers, "AM consumer"))

    population_ids = _ids(data.get("populations"), "population", errors)
    if population_ids != REQUIRED_POPULATIONS:
        errors.append(f"population definitions must remain complete: missing={sorted(REQUIRED_POPULATIONS-population_ids)}, extra={sorted(population_ids-REQUIRED_POPULATIONS)}")
    analysis_ids = _ids(data.get("analysisPlans"), "analysis plan", errors)
    if analysis_ids != REQUIRED_ANALYSES:
        errors.append(f"analysis plans must remain complete: missing={sorted(REQUIRED_ANALYSES-analysis_ids)}, extra={sorted(analysis_ids-REQUIRED_ANALYSES)}")
    for analysis in _rows(data, "analysisPlans"):
        errors.extend(_refs(analysis.get("methodEvidenceIds"), evidence_ids, "method evidence"))
        if analysis.get("freezeDecisionId") not in decision_ids:
            errors.append(f"analysis plan {analysis.get('id')} has unknown freeze decision")

    metric_ids = _ids(data.get("metrics"), "metric", errors)
    if metric_ids != REQUIRED_METRICS:
        errors.append(f"metric set must remain complete: missing={sorted(REQUIRED_METRICS-metric_ids)}, extra={sorted(metric_ids-REQUIRED_METRICS)}")
    for metric in _rows(data, "metrics"):
        metric_id = metric.get("id")
        errors.extend(_refs(metric.get("familyIds"), registry_families, "experiment family"))
        if metric.get("populationId") not in population_ids:
            errors.append(f"metric {metric_id} has unknown denominator population")
        numerator = metric.get("numeratorPopulationId")
        if numerator is not None and numerator not in population_ids:
            errors.append(f"metric {metric_id} has unknown numerator population")
        errors.extend(_refs(metric.get("parentMetricIds"), metric_ids, "parent metric"))
        if metric.get("analysisPlanId") not in analysis_ids:
            errors.append(f"metric {metric_id} lacks a valid analysis plan")
        if not metric.get("missingRule") or not metric.get("censoringRule"):
            errors.append(f"metric {metric_id} lacks missing/censoring rules")
        errors.extend(_field_reference_errors(metric.get("requiredFields"), development_records, interface_outputs))

    primary_metric_ids = {row.get("id") for row in _rows(data, "metrics") if row.get("primary") is True}
    family_metric_ids: set[str] = set()
    for family in _rows(data, "comparisonFamilies"):
        errors.extend(_refs(family.get("metricIds"), metric_ids, "comparison metric"))
        family_metric_ids.update(family.get("metricIds", []))
    if not primary_metric_ids <= family_metric_ids:
        errors.append(f"primary metrics lack comparison-family assignment: {sorted(primary_metric_ids-family_metric_ids)}")

    dependency_consumers = scenario_ids | registry_families | metric_ids
    for dependency in _rows(data, "dependencies"):
        dep_id = dependency.get("id")
        errors.extend(_refs(dependency.get("consumers"), dependency_consumers, "dependency consumer"))
        errors.extend(_refs(dependency.get("decisionIds"), decision_ids, "dependency decision"))
        if not dependency.get("closureTest"):
            errors.append(f"dependency {dep_id} lacks closure evidence")
        if dependency.get("state") == "PROPOSED-CONTRACT-DELTA" and not dependency.get("proposalFields"):
            errors.append(f"proposed dependency {dep_id} lacks concrete proposal fields")
        current = dependency.get("currentReference", {})
        if isinstance(current, dict) and current.get("kind") in {"algorithm-interface", "experiment-interface", "record-field"}:
            errors.extend(_field_reference_errors([current.get("ref", "")], development_records, interface_outputs))
    equiv = next((row for row in _rows(data, "dependencies") if row.get("id") == "DEP-EQUIV"), {})
    if any(field.get("path", "").startswith("IF-EQUIV") for field in equiv.get("proposalFields", []) if isinstance(field, dict)):
        errors.append("evaluator mutation equivalence must not redefine runtime IF-EQUIV")

    admission = data.get("designAdmission", {}) if isinstance(data.get("designAdmission"), dict) else {}
    if admission.get("confirmatoryRunStatus") != "BLOCKED":
        errors.append("candidate design cannot mark confirmatory execution ready")
    blocking = set(admission.get("blockingDecisionIds", [])) if isinstance(admission.get("blockingDecisionIds"), list) else set()
    required_blocking = REQUIRED_DECISIONS - {"DEC-DISCLOSURE"}
    if blocking != required_blocking:
        errors.append(f"blocking decisions must remain complete: missing={sorted(required_blocking-blocking)}, extra={sorted(blocking-required_blocking)}")
    if admission.get("historicalCaptureUse") != "EXPLORATORY-OFFLINE-ONLY":
        errors.append("historical captures cannot become interactive truth-bearing scenarios")

    if data.get("costAccounting", {}).get("detailToProjection", {}).get("recovery") != "preparation":
        errors.append("recovery detail must project to preparation")
    if data.get("costAccounting", {}).get("acceptedProjection") != ["acquisition", "computation", "preparation", "retry"]:
        errors.append("accepted cost projection must remain four-dimensional")
    errors.extend(_validate_walkthroughs(data, development_scenarios))

    # Exercise the derived sets so malformed nested values become diagnostics, never exceptions.
    try:
        derived_populations = _population_sets(data)
        for metric in _rows(data, "metrics"):
            numerator_id = metric.get("numeratorPopulationId")
            denominator_id = metric.get("populationId")
            if numerator_id is not None and numerator_id in derived_populations and denominator_id in derived_populations:
                outside = derived_populations[numerator_id] - derived_populations[denominator_id]
                if outside:
                    errors.append(
                        f"metric {metric.get('id')} numerator population is outside its denominator: {sorted(outside)}"
                    )
    except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
        errors.append(f"synthetic population derivation failed: {type(exc).__name__}: {exc}")
    return sorted(set(errors))


def _fraction(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "N/A"
    return f"{numerator}/{denominator}"


def accounting_summary(data: dict[str, Any]) -> dict[str, object]:
    rows = _rows(data, "syntheticWalkthroughs")
    populations = _population_sets(data)
    answered = populations["POP-ANSWERED"]
    attempts = populations["POP-ATTEMPTS"]
    conditional_errors = populations["POP-CONDITIONAL-ERROR"]
    projected = {"acquisition": 0.0, "computation": 0.0, "preparation": 0.0, "retry": 0.0}
    for row in rows:
        charged = row.get("chargedCost", {})
        projected["acquisition"] += float(charged.get("acquisition", 0))
        projected["computation"] += float(charged.get("computation", 0))
        projected["preparation"] += float(charged.get("preparation", 0)) + float(charged.get("recovery", 0))
        projected["retry"] += float(charged.get("retry", 0))
    projected_clean = {key: int(value) if value.is_integer() else value for key, value in projected.items()}
    return {
        "attempts": len(attempts),
        "answered": len(answered),
        "fails": sum(row.get("attemptId") in answered and row.get("outcome") == "FAIL" for row in rows),
        "pass": sum(row.get("attemptId") in answered and row.get("outcome") == "PASS" for row in rows),
        "answeredCoverage": _fraction(len(answered), len(attempts)),
        "conditionalDetectionError": _fraction(len(conditional_errors), len(answered)),
        "localizationDecisionCoverage": _fraction(len(populations["POP-LOCALIZATION-DECISION"]), len(populations["POP-LOCALIZATION-ELIGIBLE"])),
        "singletonLocalizationDecisions": len(populations["POP-SINGLETON-DECISION"]),
        "abstain": len(populations["POP-ABSTAIN"]),
        "unconfirmedInjection": sum(row.get("injectionStatus") == "UNCONFIRMED" for row in rows),
        "invalidObservation": sum(row.get("scenarioId") == "SC-INVALID-OBS" and row.get("validity") == "INVALID" for row in rows),
        "equivalentFault": sum(row.get("injectionStatus") == "EQUIVALENT" for row in rows),
        "unresolvedFault": sum(row.get("injectionStatus") == "UNRESOLVED" for row in rows),
        "projectedCostTotals": projected_clean,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", action="store_true", help="print the synthetic finite-population summary")
    args = parser.parse_args()
    errors = validate_design()
    if errors:
        print("Experiment design check failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Experiment design check passed")
    if args.summary:
        print(json.dumps(accounting_summary(_read_json(ROOT / DESIGN_PATH)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
