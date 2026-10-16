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
    "MET-ABLATION-DELTA", "MET-TRUTH-SCORABLE-COVERAGE", "MET-TRUTH-MISSING",
}
REQUIRED_ANALYSES = {"AN-FLOW", "AN-PROPORTION", "AN-DISTRIBUTION", "AN-PAIRED"}
REQUIRED_METRIC_CONTRACTS = {
    "MET-ATTEMPTS": (None, "POP-ATTEMPTS", {"attemptId"}),
    "MET-ANSWERED-COVERAGE": ("POP-ANSWERED", "POP-ATTEMPTS", {"attemptId", "validity", "outcome"}),
    "MET-CONDITIONAL-DETECTION-ERROR": ("POP-CONDITIONAL-ERROR", "POP-ANSWERED-TRUTH-SCORABLE", {"validity", "outcome", "truthReference.truthHypothesis"}),
    "MET-TRUTH-SCORABLE-COVERAGE": ("POP-ANSWERED-TRUTH-SCORABLE", "POP-ANSWERED", {"outcome", "validity", "truthReference.truthHypothesis"}),
    "MET-TRUTH-MISSING": ("POP-TRUTH-MISSING", "POP-ATTEMPTS", {"truthReference.truthHypothesis", "outcome", "localizationDecisionIssued"}),
    "MET-MISS": ("POP-MISSES", "POP-CONFIRMED-FAULT", {"injectionStatus", "faultDomain", "outcome", "truthReference.truthHypothesis"}),
    "MET-FALSE-FAIL": ("POP-FALSE-FAILS", "POP-QUALIFIED-NORMAL", {"injectionStatus", "faultDomain", "validity", "outcome"}),
    "MET-ABSTAIN": ("POP-ABSTAIN", "POP-ATTEMPTS", {"validity"}),
    "MET-INCONCLUSIVE": ("POP-INCONCLUSIVE", "POP-ATTEMPTS", {"outcome", "observationInterval", "requirementInterval"}),
    "MET-ERROR": ("POP-ERROR", "POP-ATTEMPTS", {"validity", "outcome"}),
    "MET-INCOMPLETE": ("POP-INCOMPLETE", "POP-ATTEMPTS", {"validity", "resourceStatus", "chargedCost"}),
    "MET-LOCALIZATION-COVERAGE": ("POP-LOCALIZATION-DECISION", "POP-LOCALIZATION-ELIGIBLE", {"localizationDecisionIssued", "injectionStatus", "faultDomain"}),
    "MET-TRUE-RETAINED": ("POP-TRUE-RETAINED", "POP-LOCALIZATION-TRUTH-SCORABLE", {"truthReference.truthHypothesis", "finalHypotheses", "localizationDecisionIssued"}),
    "MET-TRUE-EXCLUDED": ("POP-TRUE-EXCLUDED", "POP-LOCALIZATION-TRUTH-SCORABLE", {"truthReference.truthHypothesis", "finalHypotheses", "localizationDecisionIssued"}),
    "MET-SINGLETON-CORRECT": ("POP-SINGLETON-CORRECT", "POP-SINGLETON-TRUTH-SCORABLE", {"singletonDecisionIssued", "finalHypotheses", "truthReference.truthHypothesis"}),
    "MET-FINAL-CANDIDATES": (None, "POP-LOCALIZATION-ELIGIBLE", {"finalHypotheses", "stopClass"}),
    "MET-COST-VECTOR": (None, "POP-ATTEMPTS", {"chargedCost.acquisition", "chargedCost.computation", "chargedCost.preparation", "chargedCost.recovery", "chargedCost.retry"}),
    "MET-ROUNDS": (None, "POP-ROUNDS", {"runId", "actionIssued", "resourcePolicy"}),
    "MET-ABLATION-DELTA": (None, "POP-PAIRED-ELIGIBLE", {"pairingId", "outcome", "chargedCost"}),
}
REQUIRED_UPDATE_RELATIONS = {
    ("ACCEPTED", "CURRENT-QUALIFIED-INTERPRETATION", "VALID-UPDATE", False, True),
    ("REJECTED", "NO-CURRENT-UPDATE", "NOT-APPLIED-ERROR", True, False),
    ("NOT-EVALUATED", "NO-CURRENT-UPDATE", "NO-UPDATE", True, False),
}
REQUIRED_DIRECT_SOURCE_ANCHORS = {
    "SRC-ANCHOR-BERNOULLI-EXACT-INTERVAL": (
        "docs/research/methodology/RR-2026-001_test_analysis_conformance_methodology.md",
        995,
        1019,
        "55215e23ca1ae18f01ed40dd8bc68c6c9e02cb0b3a521569c28368bf35e13dc2",
    ),
}
MILESTONE_ORDER = {
    "design-review": 0,
    "pilot": 1,
    "confirmatory-registration": 2,
    "confirmatory-run": 3,
    "submission": 4,
    "645-specific-run": 4,
}
REQUIRED_FIELD_SOURCE_SEMANTICS = {
    "outcome": (
        "DERIVED", "IF-EXP-RUN.traceRef",
        {"IF-EXP-RUN.traceRef", "IF-EXP-FILTER.validityClass", "OBSERVATION-ASSESSMENT.verdict"},
        None,
    ),
    "truthReference.truthHypothesis": (
        "PROPOSED", "IF-EXP-TRUTH.truthRecord", {"IF-EXP-TRUTH.truthRecord"},
        "truthRecord.truthHypothesis",
    ),
    "injectionStatus": (
        "PROPOSED", "IF-EXP-TRUTH.truthRecord", {"IF-EXP-TRUTH.truthRecord"},
        "truthRecord.injectionStatus",
    ),
    "faultDomain": (
        "PROPOSED", "IF-EXP-TRUTH.truthRecord", {"IF-EXP-TRUTH.truthRecord"},
        "truthRecord.equivalenceDisposition",
    ),
    "observationInterval": (
        "DIRECT", "OBSERVATION-ASSESSMENT.measurementInterval",
        {"OBSERVATION-ASSESSMENT.measurementInterval"}, None,
    ),
    "requirementInterval": (
        "PROPOSED", "IF-EXP-SCENE.sceneRecord", {"IF-EXP-SCENE.sceneRecord"},
        "sceneRecord.requirementInterval",
    ),
    "pairingId": (
        "PROPOSED", "IF-EXP-SCENE.sceneRecord", {"IF-EXP-SCENE.sceneRecord"},
        "sceneRecord.pairingId",
    ),
}
REQUIRED_POPULATIONS = {
    "POP-ATTEMPTS", "POP-ANSWERED", "POP-QUALIFIED-NORMAL",
    "POP-CONFIRMED-FAULT", "POP-MISSES", "POP-FALSE-FAILS",
    "POP-CONDITIONAL-ERROR", "POP-ABSTAIN", "POP-INCONCLUSIVE", "POP-ERROR",
    "POP-INCOMPLETE", "POP-LOCALIZATION-ELIGIBLE", "POP-LOCALIZATION-DECISION",
    "POP-TRUE-RETAINED", "POP-TRUE-EXCLUDED", "POP-SINGLETON-DECISION",
    "POP-SINGLETON-CORRECT", "POP-PAIRED-ELIGIBLE", "POP-ROUNDS",
    "POP-ANSWERED-TRUTH-SCORABLE", "POP-TRUTH-MISSING",
    "POP-LOCALIZATION-TRUTH-SCORABLE", "POP-SINGLETON-TRUTH-SCORABLE",
}
REQUIRED_SCENARIO_CRS = {
    "SC-NORMAL-UPLOAD": {"CRS-M1-00077"},
    "SC-WAIT-CONTINUE": {"CRS-M1-00106", "CRS-M1-00107"},
    "SC-NO-RESPONSE": {"CRS-M1-00101"},
    "SC-ABORT": {"CRS-M1-00104", "CRS-M1-00108"},
    "SC-INVALID-OBS": set(), "SC-SAME-KEY": set(),
    "SC-SINGLE-BATCH": set(), "SC-RESOURCE-ERROR": set(),
}
REQUIRED_DEPENDENCY_EDGES = {
    "DEP-TRUTH": {
        "MET-MISS", "MET-FALSE-FAIL", "MET-CONDITIONAL-DETECTION-ERROR",
        "MET-TRUE-RETAINED", "MET-TRUE-EXCLUDED", "MET-SINGLETON-CORRECT",
        "MET-TRUTH-SCORABLE-COVERAGE", "MET-TRUTH-MISSING",
    },
    "DEP-CLOCK": {"SC-WAIT-CONTINUE", "SC-NO-RESPONSE", "SC-INVALID-OBS"},
    "DEP-RESOURCE": {"SC-RESOURCE-ERROR", "MET-COST-VECTOR", "MET-ROUNDS"},
    "DEP-EQUIV": {"MET-MISS", "MET-ABLATION-DELTA"},
}
ROW_FIELDS = {
    "attemptId", "runId", "armId", "baseSceneId", "pairingId", "pairedArmId",
    "resetEvidenceRef", "resetConfirmed", "sceneSeed", "constructionId",
    "contrastId", "pairParentMetricIds", "updateStatus",
    "injectionStatus", "faultDomain", "validity",
    "outcome", "stopClass", "stage", "observationInterval", "requirementInterval",
    "historyBefore", "compatibleState", "finalHypotheses", "localizationDecisionIssued",
    "singletonDecisionIssued", "resourcePolicy", "resourceStatus", "actionIssued", "chargedCost",
    "endpointTopology", "reviewSetupEffort",
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
    answered = {
        aid for aid, row in by_id.items()
        if row.get("runId") is not None
        and row.get("validity") == "VALID"
        and row.get("outcome") in {"PASS", "FAIL"}
    }
    normal = {
        aid for aid, row in by_id.items()
        if row.get("runId") is not None
        and row.get("injectionStatus") == "NORMAL"
        and row.get("faultDomain") == "NORMAL"
        and row.get("validity") == "VALID"
    }
    faults = {aid for aid, row in by_id.items() if row.get("injectionStatus") == "CONFIRMED" and row.get("faultDomain") == "IN-DOMAIN-NON-EQUIVALENT" and row.get("runId") is not None}
    misses = {aid for aid in faults if by_id[aid].get("outcome") == "PASS"}
    false_fails = {aid for aid in normal if by_id[aid].get("outcome") == "FAIL"}
    answered_truth_scorable = {
        aid for aid in answered
        if by_id[aid].get("truthReference", {}).get("truthHypothesis") is not None
    }
    conditional_error = (misses | false_fails) & answered_truth_scorable
    abstain = {aid for aid, row in by_id.items() if row.get("validity") == "ABSTAIN"}
    inconclusive = {aid for aid, row in by_id.items() if row.get("outcome") == "INCONCLUSIVE"}
    error = {aid for aid, row in by_id.items() if row.get("outcome") == "ERROR" or row.get("validity") == "INVALID"}
    incomplete = {aid for aid, row in by_id.items() if row.get("validity") == "INCOMPLETE" or row.get("resourceStatus") == "BUDGET-EXHAUSTED"}
    loc_eligible = set(faults)
    loc_decision = {aid for aid in loc_eligible if by_id[aid].get("localizationDecisionIssued") is True}
    loc_truth_scorable = {
        aid for aid in loc_decision
        if by_id[aid].get("validity") == "VALID"
        and by_id[aid].get("truthReference", {}).get("truthHypothesis") is not None
    }
    retained = {
        aid for aid in loc_decision
        if aid in loc_truth_scorable and by_id[aid].get("truthReference", {}).get("truthHypothesis") in by_id[aid].get("finalHypotheses", [])
    }
    excluded = loc_truth_scorable - retained
    singleton = {
        aid for aid in loc_decision
        if by_id[aid].get("singletonDecisionIssued") is True
        and len(by_id[aid].get("finalHypotheses", [])) == 1
    }
    singleton_truth_scorable = {
        aid for aid in singleton
        if aid in loc_truth_scorable
    }
    singleton_correct = {
        aid for aid in singleton_truth_scorable
        if by_id[aid].get("truthReference", {}).get("truthHypothesis") == by_id[aid].get("finalHypotheses", [None])[0]
    }
    truth_missing = {
        aid for aid in attempts
        if by_id[aid].get("truthReference", {}).get("truthHypothesis") is None
        and (aid in answered or aid in loc_decision or aid in singleton)
    }
    pair_groups: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if row.get("pairingId") is not None:
            pair_groups.setdefault(str(row["pairingId"]), []).append(row)
    paired: set[str] = set()
    contrasts = {
        str(row.get("id")): row for row in _rows(data, "registeredContrasts")
    }
    parent_metrics = {
        "MET-ANSWERED-COVERAGE", "MET-TRUE-RETAINED", "MET-COST-VECTOR"
    }

    def eligible_parents(row: dict[str, Any]) -> set[str]:
        aid = str(row.get("attemptId", ""))
        result = {"MET-ANSWERED-COVERAGE"} if aid in attempts else set()
        if aid in loc_truth_scorable:
            result.add("MET-TRUE-RETAINED")
        charged = row.get("chargedCost", {})
        if isinstance(charged, dict) and all(
            isinstance(charged.get(key), (int, float))
            for key in ("acquisition", "computation", "preparation", "recovery", "retry")
        ):
            result.add("MET-COST-VECTOR")
        return result

    for pair_id, members in pair_groups.items():
        if len(members) != 2:
            continue
        left, right = members
        contrast = contrasts.get(str(left.get("contrastId")), {})
        structural = (
            left.get("baseSceneId") == right.get("baseSceneId")
            and left.get("sceneSeed") == right.get("sceneSeed")
            and left.get("constructionId") == right.get("constructionId")
            and left.get("contrastId") == right.get("contrastId")
            and left.get("armId") != right.get("armId")
            and left.get("pairedArmId") == right.get("armId")
            and right.get("pairedArmId") == left.get("armId")
            and set(contrast.get("armIds", [])) == {left.get("armId"), right.get("armId")}
            and left.get("resetEvidenceRef")
            and right.get("resetEvidenceRef")
            and left.get("resetEvidenceRef") != right.get("resetEvidenceRef")
            and left.get("resetConfirmed") is True
            and right.get("resetConfirmed") is True
        )
        if structural:
            for parent_id in parent_metrics & set(contrast.get("parentMetricIds", [])):
                if parent_id in eligible_parents(left) and parent_id in eligible_parents(right):
                    paired.add(f"{pair_id}::{parent_id}")
    rounds = {
        aid for aid, row in by_id.items()
        if row.get("runId") is not None and row.get("resourcePolicy") == "ROUNDS"
    }
    return {
        "POP-ATTEMPTS": attempts, "POP-ANSWERED": answered,
        "POP-ANSWERED-TRUTH-SCORABLE": answered_truth_scorable,
        "POP-TRUTH-MISSING": truth_missing,
        "POP-QUALIFIED-NORMAL": normal, "POP-CONFIRMED-FAULT": faults,
        "POP-MISSES": misses, "POP-FALSE-FAILS": false_fails,
        "POP-CONDITIONAL-ERROR": conditional_error, "POP-ABSTAIN": abstain,
        "POP-INCONCLUSIVE": inconclusive, "POP-ERROR": error,
        "POP-INCOMPLETE": incomplete, "POP-LOCALIZATION-ELIGIBLE": loc_eligible,
        "POP-LOCALIZATION-DECISION": loc_decision,
        "POP-LOCALIZATION-TRUTH-SCORABLE": loc_truth_scorable,
        "POP-TRUE-RETAINED": retained,
        "POP-TRUE-EXCLUDED": excluded, "POP-SINGLETON-DECISION": singleton,
        "POP-SINGLETON-TRUTH-SCORABLE": singleton_truth_scorable,
        "POP-SINGLETON-CORRECT": singleton_correct, "POP-PAIRED-ELIGIBLE": paired,
        "POP-ROUNDS": rounds,
    }


def _validate_walkthroughs(data: dict[str, Any], scenario_ids: set[str]) -> list[str]:
    errors: list[str] = []
    rows = _rows(data, "syntheticWalkthroughs")
    attempt_ids = [str(row.get("attemptId", "")) for row in rows]
    row_ids = {str(row.get("id", "")) for row in rows}
    relation_rows = _rows(data, "updateDecisionRelations")
    actual_relations = {
        (
            row.get("interpretationDisposition"), row.get("updateSource"), row.get("updateStatus"),
            row.get("preserveHistory"), row.get("currentDecisionPermitted"),
        )
        for row in relation_rows
    }
    if actual_relations != REQUIRED_UPDATE_RELATIONS or len(relation_rows) != len(REQUIRED_UPDATE_RELATIONS):
        errors.append("update decision relation must retain the reviewed interpretation/source/update truth table")
    relation_by_input = {
        (row.get("interpretationDisposition"), row.get("updateSource")): row
        for row in relation_rows
    }
    interpretation_rows = _rows(data, "walkthroughInterpretationContracts")
    interpretation_ids = [str(row.get("walkthroughId", "")) for row in interpretation_rows]
    if set(interpretation_ids) != row_ids or len(interpretation_ids) != len(row_ids):
        errors.append("every synthetic walkthrough requires exactly one interpretation/update-source contract")
    interpretation_by_id = {
        str(row.get("walkthroughId", "")): row for row in interpretation_rows
    }
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
        if row.get("runId") is None:
            non_run_ok = (
                row.get("stage") == "PRE-RUN"
                and row.get("validity") == "PRE-RUN-EXCLUDED"
                and row.get("outcome") == "NOT-ANSWERED"
                and row.get("updateStatus") == "NO-UPDATE"
                and row.get("stopClass") is None
                and row.get("resourcePolicy") == "NOT-RUN"
                and row.get("resourceStatus") == "NOT-RUN"
                and row.get("actionIssued") is False
                and row.get("localizationDecisionIssued") is False
                and row.get("singletonDecisionIssued") is False
                and not any(row.get("chargedCost", {}).values())
            )
            if not non_run_ok:
                errors.append(
                    f"walkthrough {row_id} non-run record must remain PRE-RUN/PRE-RUN-EXCLUDED/NOT-ANSWERED with no update, decision, action, stop or charge"
                )
        elif row.get("resourcePolicy") == "NOT-RUN" or row.get("stage") == "PRE-RUN" or row.get("validity") == "PRE-RUN-EXCLUDED":
            errors.append(f"walkthrough {row_id} hides or mislabels an admitted run")
        if row.get("resourceStatus") == "BUDGET-EXHAUSTED" and row.get("stopClass") != "Stop-Budget":
            errors.append(f"walkthrough {row_id} has budget exhaustion without Stop-Budget")
        if row.get("outcome") in {"PASS", "FAIL"} and row.get("validity") != "VALID":
            errors.append(f"walkthrough {row_id} assigns PASS/FAIL to invalid evidence")
        if row.get("outcome") == "ERROR" and row.get("localizationDecisionIssued"):
            errors.append(f"walkthrough {row_id} cannot count ERROR as a localization decision")
        final = row.get("finalHypotheses", [])
        history = row.get("historyBefore", [])
        compatible = row.get("compatibleState", [])
        update_status = row.get("updateStatus")
        interpretation = interpretation_by_id.get(str(row_id), {})
        relation = relation_by_input.get(
            (interpretation.get("interpretationDisposition"), interpretation.get("updateSource")),
            {},
        )
        if not relation or update_status != relation.get("updateStatus"):
            errors.append(
                f"walkthrough {row_id} violates the common interpretation/update-source decision relation"
            )
        if relation.get("preserveHistory") is True and set(final) != set(history):
            errors.append(f"walkthrough {row_id} non-applied current step must preserve preceding H/history")
        if relation.get("currentDecisionPermitted") is False and (
            row.get("localizationDecisionIssued") or row.get("singletonDecisionIssued")
        ):
            errors.append(f"walkthrough {row_id} non-applied current step cannot issue a current localization decision")
        if interpretation.get("interpretationDisposition") == "REJECTED" and (
            update_status != "NOT-APPLIED-ERROR" or row.get("outcome") != "ERROR"
        ):
            errors.append(f"walkthrough {row_id} rejected interpretation must remain a non-applied ERROR")
        if update_status == "NOT-APPLIED-ERROR":
            if set(final) != set(history) or row.get("outcome") != "ERROR":
                errors.append(
                    f"walkthrough {row_id} rejected update must preserve H and remain ERROR independent of the stop label"
                )
        elif update_status == "VALID-UPDATE":
            if set(final) != set(compatible) or not set(final) <= set(history):
                errors.append(
                    f"walkthrough {row_id} valid successor must equal compatibility intersection and be a subset of H"
                )
            if not final and (
                row.get("stopClass") != "Stop-Empty"
                or row.get("stage") != "POST-UPDATE"
                or row.get("outcome") != "ERROR"
            ):
                errors.append(f"walkthrough {row_id} empty valid update has mandatory Stop-Empty priority")
            if len(final) == 1 and row.get("stopClass") != "Stop-Singleton":
                errors.append(f"walkthrough {row_id} singleton valid update has mandatory Stop-Singleton priority")
        elif update_status == "NO-UPDATE" and set(final) != set(history):
            errors.append(f"walkthrough {row_id} no-update exit must preserve H")
        if row.get("singletonDecisionIssued") and (not row.get("localizationDecisionIssued") or len(final) != 1):
            errors.append(f"walkthrough {row_id} has an invalid singleton decision")
        if row.get("stopClass") in {"Stop-645", "Stop-Budget"} and row.get("singletonDecisionIssued"):
            errors.append(f"walkthrough {row_id} lets {row.get('stopClass')} masquerade as a singleton decision")
        if row.get("stopClass") == "Stop-Empty":
            if update_status != "VALID-UPDATE" or final or row.get("stage") != "POST-UPDATE" or row.get("outcome") != "ERROR":
                errors.append(f"walkthrough {row_id} violates Stop-Empty stage/outcome priority")
        if row.get("stopClass") == "Stop-645" and row.get("stage") != "POST-UPDATE":
            errors.append(f"walkthrough {row_id} violates Stop-645 stage priority")
        if row.get("stage") == "POST-UPDATE" and len(final) == 1 and row.get("stopClass") != "Stop-Singleton":
            errors.append(f"walkthrough {row_id} bypasses Stop-Singleton priority")
        if row.get("stage") == "POST-UPDATE" and not final and row.get("stopClass") != "Stop-Empty":
            errors.append(f"walkthrough {row_id} bypasses Stop-Empty priority")
        if row.get("stage") == "PRE-ACTION" and (row.get("actionIssued") or any(row.get("chargedCost", {}).values())):
            errors.append(f"walkthrough {row_id} charges or issues an action before admission")
        if not row.get("actionIssued") and any(row.get("chargedCost", {}).values()):
            errors.append(f"walkthrough {row_id} charges an unissued arm action")
        if row.get("stopClass") in {"Stop-645", "Stop-Budget"} and row.get("actionIssued") and sum(row.get("chargedCost", {}).values()) <= 0:
            errors.append(f"walkthrough {row_id} hides spent cost at {row.get('stopClass')}")
        allowed_costs = {
            arm.get("id"): set(arm.get("costComponents", []))
            for arm in _rows(data, "arms")
        }.get(row.get("armId"), set())
        charged = row.get("chargedCost", {})
        for detail, amount in charged.items() if isinstance(charged, dict) else []:
            projected = "preparation" if detail == "recovery" else detail
            if amount and projected not in allowed_costs:
                errors.append(
                    f"walkthrough {row_id} charges {detail} outside arm {row.get('armId')} cost contract"
                )
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
                    contained = required["lower"] <= observed["lower"] and observed["upper"] <= required["upper"]
                    disjoint = observed["upper"] < required["lower"] or required["upper"] < observed["lower"]
                except (KeyError, TypeError):
                    valid_order = contained = disjoint = False
                expected = "PASS" if contained else "FAIL" if disjoint else "INCONCLUSIVE"
                if row.get("endpointTopology") != "CLOSED" or not valid_order or row.get("outcome") != expected:
                    errors.append(f"SYN-T5-OVERLAP violates closed-interval T5 classification; expected {expected}")
    populations = _population_sets(data)
    derived_pairs = populations["POP-PAIRED-ELIGIBLE"]
    for row in rows:
        declared = set(row.get("pairParentMetricIds", []))
        prefix = f"{row.get('pairingId')}::"
        expected = {
            item.split("::", 1)[1]
            for item in derived_pairs if row.get("pairingId") is not None and item.startswith(prefix)
        }
        if declared != expected:
            errors.append(
                f"walkthrough {row.get('id')} pairing eligibility and parent metrics disagree with derived finite evidence"
            )
    return errors


def _analysis_choice(row: dict[str, Any]) -> tuple[str, str]:
    if row.get("domainEnumeration") == "COMPLETE":
        return "DETERMINISTIC-EXHAUSTIVE", "CANDIDATE-METHOD"
    if (
        row.get("domainEnumeration") == "INCOMPLETE"
        and row.get("randomAssignment") == "INDEPENDENT"
        and row.get("dependence") == "NONE"
        and row.get("independentUnit") == "ATTEMPT"
    ):
        return "INDEPENDENT-RANDOMIZED", "CANDIDATE-METHOD"
    if (
        row.get("domainEnumeration") == "INCOMPLETE"
        and row.get("randomAssignment") == "NOT-INDEPENDENT"
        and row.get("dependence") == "PAIRED"
        and row.get("pairingEvidence") is True
        and row.get("independentUnit") == "PAIR"
    ):
        return "PAIRED-OR-CLUSTERED", "CANDIDATE-METHOD"
    if (
        row.get("domainEnumeration") == "INCOMPLETE"
        and row.get("randomAssignment") == "NOT-INDEPENDENT"
        and row.get("dependence") == "CLUSTERED"
        and row.get("clusterEvidence") is True
        and row.get("independentUnit") == "CLUSTER"
    ):
        return "PAIRED-OR-CLUSTERED", "CANDIDATE-METHOD"
    return "NONE", "WAIT-DEC-SAMPLE"


def _translation_keys(data: dict[str, Any]) -> set[str]:
    groups = {
        "claimArguments": "claimId", "arms": "id", "scenarios": "id",
        "metrics": "id", "analysisPlans": "id", "dependencies": "id",
        "pendingDecisions": "id", "comparisonFamilies": "id",
    }
    result: set[str] = set()
    for group, id_field in groups.items():
        for row in _rows(data, group):
            result.add(f"{group}.{row.get(id_field)}.summary")
    return result


def _validate_protocol_timelines(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for row in _rows(data, "protocolTimelineWalkthroughs"):
        row_id = row.get("id")
        if row.get("scenarioId") != "SC-NO-RESPONSE" or row.get("crsRef") != "CRS-M1-00101":
            errors.append(f"protocol timeline {row_id} must bind SC-NO-RESPONSE and CRS-M1-00101")
            continue
        trigger = row.get("trigger", {})
        received = row.get("receivedEvent", {})
        elapsed = row.get("elapsedSeconds")
        delay = trigger.get("exceptionDelaySeconds")
        boundary = row.get("timerExpiryBoundary")
        abort_obligation = row.get("abortObligation")
        abort_bound = row.get("abortCompletionBoundSeconds")
        observation_end = row.get("observationEndSeconds")
        horizon_qualified = row.get("observationEndQualified") is True
        same_operation = (
            trigger.get("actor") == "DATA-LOADER"
            and trigger.get("event") == "RECEIVED-STATUS-WITH-EXCEPTION-DELAY"
            and trigger.get("operationKey")
            and trigger.get("operationKey") == received.get("operationKey")
        )
        expected = "NOT-SCORED"
        if abort_bound is not None:
            errors.append(
                f"protocol timeline {row_id} supplies an unreviewed abort completion bound while DEC-CLOCK is OPEN"
            )
        timing_values = all(
            isinstance(value, (int, float)) for value in (elapsed, delay, observation_end)
        )
        horizon_valid = timing_values and observation_end >= elapsed
        if same_operation and horizon_valid and horizon_qualified:
            if abort_obligation != "REQUIRED-IF-NO-TIMELY-STATUS":
                errors.append(f"protocol timeline {row_id} drops the required abort fallback obligation")
            event = received.get("event")
            if event == "NEW-STATUS":
                if elapsed < delay:
                    expected = "PASS"
                elif elapsed == delay and boundary == "CLOSED":
                    expected = "PASS"
            elif (
                event == "ABORT"
                and received.get("requiredFallback") is True
                and elapsed > delay
                and abort_obligation == "REQUIRED-IF-NO-TIMELY-STATUS"
            ):
                expected = "PASS"
        elif not same_operation and abort_obligation != "NOT-APPLICABLE":
            errors.append(f"protocol timeline {row_id} assigns the CRS abort obligation to an unbound trigger")
        if boundary != "UNRESOLVED":
            errors.append(f"protocol timeline {row_id} must retain the bound authority's unresolved timer endpoint until DEC-CLOCK closes")
        if not horizon_valid:
            errors.append(f"protocol timeline {row_id} lacks a finite qualified observation endpoint covering its event")
        if row.get("outcome") != expected:
            errors.append(f"protocol timeline {row_id} expected {expected}, got {row.get('outcome')}")
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
    proposed_interface_outputs: dict[str, set[str]] = {}
    for dependency in _rows(data, "dependencies"):
        for field in dependency.get("proposalFields", []):
            if not isinstance(field, dict):
                continue
            owner, separator, name = str(field.get("path", "")).partition(".")
            if separator and owner.startswith("IF-"):
                proposed_interface_outputs.setdefault(owner, set()).add(name)
    reference_outputs = {key: set(value) for key, value in interface_outputs.items()}
    for owner, fields in proposed_interface_outputs.items():
        reference_outputs.setdefault(owner, set()).update(fields)
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

    contrast_ids = _ids(data.get("registeredContrasts"), "registered contrast", errors)
    expected_contrasts = {
        "CONTRAST-DETECT-LOOP-T", "CONTRAST-LOCATE-LOOP-T",
        "CONTRAST-LOCATE-LOOP-TA",
    }
    if contrast_ids != expected_contrasts:
        errors.append("registered contrasts must remain complete")
    for contrast in _rows(data, "registeredContrasts"):
        errors.extend(_refs(contrast.get("armIds"), registry_arms, "contrast arm"))
        errors.extend(_refs(contrast.get("parentMetricIds"), REQUIRED_METRICS, "contrast parent metric"))

    arm_ids = _ids(data.get("arms"), "arm", errors)
    if arm_ids != registry_arms:
        errors.append(f"arm design must contain exactly {sorted(registry_arms)}")
    expected_arm_costs = {
        "CL-T": {"acquisition", "preparation", "retry"},
        "CL-A": {"computation"},
        "CL-TA": {"acquisition", "computation", "preparation", "retry"},
        "CL-LOOP": {"acquisition", "computation", "preparation", "retry"},
    }
    expected_arm_inputs = {
        "CL-T": {("IF-EXP-SCENE.algorithmVisibleFields", "ALGORITHM-INITIAL"), ("IF-EXP-COLLECT.observationLog", "ALGORITHM-OWN-ACTION")},
        "CL-A": {("IF-EXP-SCENE.algorithmVisibleFields", "ALGORITHM-INITIAL")},
        "CL-TA": {("IF-EXP-SCENE.algorithmVisibleFields", "ALGORITHM-INITIAL"), ("IF-EXP-COLLECT.observationLog", "ALGORITHM-OWN-ACTION")},
        "CL-LOOP": {("IF-EXP-SCENE.algorithmVisibleFields", "ALGORITHM-INITIAL"), ("IF-EXP-COLLECT.observationLog", "ALGORITHM-OWN-ACTION"), ("IF-EXP-COLLECT.resourceLog", "ALGORITHM-OWN-ACTION")},
    }
    for arm in _rows(data, "arms"):
        for item in arm.get("visibleInputs", []) if isinstance(arm.get("visibleInputs"), list) else []:
            if not isinstance(item, dict):
                continue
            reference = item.get("ref", "")
            evaluator_only = (
                reference.startswith("IF-EXP-TRUTH.")
                or reference.startswith("truthReference.")
                or reference in {"IF-EXP-INJECT.injectionConfirmed", "IF-EXP-FILTER.validityClass"}
            )
            if evaluator_only or item.get("role") not in {"ALGORITHM-INITIAL", "ALGORITHM-OWN-ACTION"}:
                errors.append(f"typed truth leakage or invalid visibility in arm {arm.get('id')}: {reference}")
            errors.extend(_field_reference_errors([reference], development_records, reference_outputs))
        if arm.get("id") in {"CL-T", "CL-A", "CL-TA"} and arm.get("feedback"):
            errors.append(f"non-loop arm {arm.get('id')} cannot receive feedback")
        if arm.get("id") == "CL-A" and any(item.get("role") == "ALGORITHM-OWN-ACTION" for item in arm.get("visibleInputs", []) if isinstance(item, dict)):
            errors.append("CL-A cannot receive records from an action it did not execute")
        arm_id = arm.get("id")
        actual_inputs = {(item.get("ref"), item.get("role")) for item in arm.get("visibleInputs", []) if isinstance(item, dict)}
        if arm_id in expected_arm_inputs and actual_inputs != expected_arm_inputs[arm_id]:
            errors.append(f"arm {arm_id} visible inputs must equal the reviewed fixed allowlist")
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
        errors.extend(_refs(scenario.get("requiredRecords"), set(development_records), "required record"))
        if scenario.get("developmentScenarioRef") != scenario_id:
            errors.append(f"scenario {scenario_id} must bind its exact development scenario")
        accepted = development_scenario_rows.get(scenario_id, {})
        if accepted and scenario.get("serviceScope") != accepted.get("serviceScope"):
            errors.append(f"scenario {scenario_id} service scope disagrees with bound Git development authority")
        if scenario.get("crsDisposition") == "TOOL-OR-EXPERIMENT-N/A" and scenario.get("crsRefs"):
            errors.append(f"scenario {scenario_id} cannot combine N/A CRS disposition with CRS references")
        if scenario.get("crsDisposition") == "APPLICABLE" and not scenario.get("crsRefs"):
            errors.append(f"scenario {scenario_id} lacks applicable CRS references")
        if set(scenario.get("crsRefs", [])) != REQUIRED_SCENARIO_CRS.get(str(scenario_id), set()):
            errors.append(f"scenario {scenario_id} CRS references disagree with the reviewed proposition binding")

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
        if analysis.get("missingInputResult") != "WAIT-DEC-SAMPLE" or not analysis.get("sourceLocators"):
            errors.append(f"analysis plan {analysis.get('id')} lacks a bounded missing-input wait or source locator")
        status = analysis.get("methodStatus")
        locators = analysis.get("sourceLocators", [])
        for locator in locators if isinstance(locators, list) else []:
            path = locator.get("path", "") if isinstance(locator, dict) else ""
            start = locator.get("lineStart") if isinstance(locator, dict) else None
            end = locator.get("lineEnd") if isinstance(locator, dict) else None
            role = locator.get("role") if isinstance(locator, dict) else None
            if path not in snapshot:
                errors.append(f"analysis plan {analysis.get('id')} source locator is not a bound path: {path}")
                continue
            line_count = len(snapshot[path].decode("utf-8-sig", errors="replace").splitlines())
            if not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start or end > line_count:
                errors.append(f"analysis plan {analysis.get('id')} source locator has an invalid line range")
            if role not in {"DIRECT", "CONTEXT-ONLY"}:
                errors.append(f"analysis plan {analysis.get('id')} source locator has an invalid role")
            if role == "DIRECT":
                anchor_id = locator.get("anchorId")
                excerpt_sha = locator.get("excerptSha256")
                expected_anchor = REQUIRED_DIRECT_SOURCE_ANCHORS.get(str(anchor_id))
                if expected_anchor is None:
                    errors.append(f"analysis plan {analysis.get('id')} DIRECT source lacks a reviewed stable proposition anchor")
                elif (path, start, end, excerpt_sha) != expected_anchor:
                    errors.append(f"analysis plan {analysis.get('id')} DIRECT source locator drifted from its reviewed proposition anchor")
                elif isinstance(start, int) and isinstance(end, int) and 1 <= start <= end <= line_count:
                    source_lines = snapshot[path].decode("utf-8-sig", errors="replace").splitlines()
                    actual_excerpt_sha = hashlib.sha256("\n".join(source_lines[start - 1:end]).encode("utf-8")).hexdigest()
                    if actual_excerpt_sha != excerpt_sha:
                        errors.append(f"analysis plan {analysis.get('id')} DIRECT proposition excerpt identity does not match its anchor")
        direct = [item for item in locators if isinstance(item, dict) and item.get("role") == "DIRECT"]
        if status == "NAMED-CANDIDATE" and not direct:
            errors.append(f"analysis plan {analysis.get('id')} names a method without a direct source")
        if status in {"DESCRIPTIVE-ONLY", "METHOD-WAIT"} and direct:
            errors.append(f"analysis plan {analysis.get('id')} overstates context as a direct method source")

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
        if metric_id in REQUIRED_METRIC_CONTRACTS:
            expected_numerator, expected_denominator, expected_fields = REQUIRED_METRIC_CONTRACTS[metric_id]
            if (
                metric.get("numeratorPopulationId") != expected_numerator
                or metric.get("populationId") != expected_denominator
                or set(metric.get("requiredFields", [])) != expected_fields
            ):
                errors.append(f"metric {metric_id} disagrees with its reviewed finite computation contract")

    metric_consumers_by_field: dict[str, set[str]] = {}
    for metric in _rows(data, "metrics"):
        for field in metric.get("requiredFields", []):
            metric_consumers_by_field.setdefault(str(field), set()).add(str(metric.get("id")))
    field_contract_rows = _rows(data, "metricFieldContracts")
    field_contracts = {str(row.get("field", "")): row for row in field_contract_rows}
    if len(field_contracts) != len(field_contract_rows):
        errors.append("metric field handoff contracts contain duplicate field identities")
    if set(field_contracts) != set(metric_consumers_by_field):
        errors.append(
            "metric field handoff contracts must cover exactly every registered metric required field"
        )
    dependencies_by_id = {str(row.get("id", "")): row for row in _rows(data, "dependencies")}
    for field, consumers in metric_consumers_by_field.items():
        contract = field_contracts.get(field, {})
        if set(contract.get("consumerMetricIds", [])) != consumers:
            errors.append(f"metric field {field} has stale or incomplete consumer relationships")
        source_path = contract.get("sourcePath", "")
        errors.extend(_field_reference_errors([source_path], development_records, interface_outputs))
        source_inputs = contract.get("sourceInputPaths", [])
        errors.extend(_field_reference_errors(source_inputs, development_records, interface_outputs))
        source_kind = contract.get("sourceKind")
        proposal_path = contract.get("proposalFieldPath")
        if source_kind == "DIRECT" and (source_inputs != [source_path] or proposal_path is not None):
            errors.append(f"metric field {field} DIRECT source must be one exact existing leaf and no proposal")
        if source_kind == "DERIVED" and (not source_inputs or proposal_path is not None):
            errors.append(f"metric field {field} DERIVED source requires declared inputs and no proposal")
        if source_kind == "PROPOSED" and proposal_path is None:
            errors.append(f"metric field {field} PROPOSED source requires a registered proposal")
        if not str(contract.get("derivationRule", "")).strip():
            errors.append(f"metric field {field} lacks a bounded value derivation rule")
        dependency_id = str(contract.get("dependencyId", ""))
        dependency = dependencies_by_id.get(dependency_id)
        if dependency is None:
            errors.append(f"metric field {field} has unknown dependency {dependency_id}")
            continue
        closure = contract.get("closureMilestone")
        blocking = dependency.get("blockingMilestone")
        if closure not in MILESTONE_ORDER or blocking not in MILESTONE_ORDER or MILESTONE_ORDER[closure] > MILESTONE_ORDER[blocking]:
            errors.append(f"metric field {field} closes after its dependency blocking milestone")
        if proposal_path is not None:
            proposal = next(
                (item for item in dependency.get("proposalFields", []) if item.get("path") == proposal_path),
                None,
            )
            if proposal is None:
                errors.append(f"metric field {field} lacks required proposal {proposal_path} in {dependency_id}")
            elif (
                proposal.get("producer") != contract.get("producerRole")
                or proposal.get("visibility") != contract.get("visibility")
                or proposal.get("backwardCompatibility") != contract.get("backwardCompatibility")
                or proposal.get("closureMilestone") != closure
            ):
                errors.append(f"metric field {field} disagrees with its producer/visibility/compatibility/milestone proposal")

    for field, expected in REQUIRED_FIELD_SOURCE_SEMANTICS.items():
        contract = field_contracts.get(field, {})
        actual = (
            contract.get("sourceKind"), contract.get("sourcePath"),
            set(contract.get("sourceInputPaths", [])), contract.get("proposalFieldPath"),
        )
        if actual != expected:
            errors.append(f"metric field {field} violates its reviewed value-source semantics")

    if field_contracts.get("pairingId", {}).get("proposalFieldPath") == "sceneRecord.resetEvidenceRef":
        errors.append("metric field pairingId must remain distinct from per-arm resetEvidenceRef")

    critical_truth_contracts = {
        "truthReference.truthHypothesis": ("truthRecord.truthHypothesis", "independent evaluator", "DEP-TRUTH", "pilot"),
        "injectionStatus": ("truthRecord.injectionStatus", "independent evaluator", "DEP-TRUTH", "pilot"),
        "faultDomain": ("truthRecord.equivalenceDisposition", "fault adjudicator", "DEP-EQUIV", "confirmatory-registration"),
    }
    truth_proposals = {
        str(item.get("path", ""))
        for item in dependencies_by_id.get("DEP-TRUTH", {}).get("proposalFields", [])
        if isinstance(item, dict)
    }
    required_truth_proposals = {
        "truthRecord.confirmationRef", "truthRecord.truthHypothesis",
        "truthRecord.injectionStatus", "truthRecord.equivalenceDisposition",
    }
    if not required_truth_proposals <= truth_proposals:
        errors.append("DEP-TRUTH must keep separate truth identity, injection status, equivalence, and confirmation evidence proposals")
    confirmation = next(
        (
            item for item in dependencies_by_id.get("DEP-TRUTH", {}).get("proposalFields", [])
            if isinstance(item, dict) and item.get("path") == "truthRecord.confirmationRef"
        ),
        {},
    )
    if (
        confirmation.get("producer"), confirmation.get("visibility"),
        confirmation.get("backwardCompatibility"), confirmation.get("closureMilestone"),
    ) != ("independent evaluator", "evaluator-only", "additive field", "pilot"):
        errors.append("metric truth confirmation evidence disagrees with its producer/visibility/compatibility/milestone proposal")
    for field, expected in critical_truth_contracts.items():
        contract = field_contracts.get(field, {})
        actual = (
            contract.get("proposalFieldPath"), contract.get("producerRole"),
            contract.get("dependencyId"), contract.get("closureMilestone"),
        )
        if actual != expected or contract.get("visibility") != "evaluator-only":
            errors.append(f"metric field {field} must retain its reviewed independent evaluator handoff")

    proposal_signatures: dict[str, set[tuple[Any, ...]]] = {}
    for dependency in _rows(data, "dependencies"):
        for proposal in dependency.get("proposalFields", []):
            path = str(proposal.get("path", ""))
            proposal_signatures.setdefault(path, set()).add(
                (
                    proposal.get("type"), proposal.get("producer"), proposal.get("visibility"),
                    proposal.get("backwardCompatibility"), proposal.get("closureMilestone"),
                )
            )
    for path, signatures in proposal_signatures.items():
        if len(signatures) > 1:
            errors.append(f"proposal field {path} has inconsistent cross-dependency handoff semantics")

    primary_metric_ids = {row.get("id") for row in _rows(data, "metrics") if row.get("primary") is True}
    family_metric_ids: set[str] = set()
    for family in _rows(data, "comparisonFamilies"):
        errors.extend(_refs(family.get("metricIds"), metric_ids, "comparison metric"))
        family_metric_ids.update(family.get("metricIds", []))
        if not family.get("contrasts") or not family.get("jointConclusion"):
            errors.append(f"comparison family {family.get('id')} lacks explicit contrasts or joint conclusion")
    if not primary_metric_ids <= family_metric_ids:
        errors.append(f"primary metrics lack comparison-family assignment: {sorted(primary_metric_ids-family_metric_ids)}")

    dependency_consumers = scenario_ids | registry_families | metric_ids
    for dependency in _rows(data, "dependencies"):
        dep_id = dependency.get("id")
        errors.extend(_refs(dependency.get("consumers"), dependency_consumers, "dependency consumer"))
        errors.extend(_refs(dependency.get("decisionIds"), decision_ids, "dependency decision"))
        missing_edges = REQUIRED_DEPENDENCY_EDGES.get(str(dep_id), set()) - set(dependency.get("consumers", []))
        if missing_edges:
            errors.append(f"dependency {dep_id} is missing required consumers {sorted(missing_edges)}")
        if not dependency.get("closureTest"):
            errors.append(f"dependency {dep_id} lacks closure evidence")
        if dependency.get("state") == "PROPOSED-CONTRACT-DELTA" and not dependency.get("proposalFields"):
            errors.append(f"proposed dependency {dep_id} lacks concrete proposal fields")
        for field in dependency.get("proposalFields", []):
            if not isinstance(field, dict):
                continue
            if str(field.get("path", "")).startswith("truthRecord.") and field.get("visibility") != "evaluator-only":
                errors.append(f"dependency {dep_id} exposes evaluator truth proposal outside evaluator-only visibility")
            if str(field.get("type", "")).endswith("[]"):
                errors.append(f"dependency {dep_id} proposal field has an empty type domain")
        current = dependency.get("currentReference", {})
        allowed_reference_kinds = {
            "algorithm-interface", "contrast-only-algorithm-interface", "experiment-interface",
            "record-field", "experiment-plan", "experiment-plan-section", "placeholder", "authority-binding",
        }
        if not isinstance(current, dict) or current.get("kind") not in allowed_reference_kinds:
            errors.append(f"dependency {dep_id} has unknown currentReference kind")
        elif current.get("kind") in {"algorithm-interface", "contrast-only-algorithm-interface", "experiment-interface", "record-field"}:
            errors.extend(_field_reference_errors([current.get("ref", "")], development_records, interface_outputs))
    equiv = next((row for row in _rows(data, "dependencies") if row.get("id") == "DEP-EQUIV"), {})
    if any(field.get("path", "").startswith("IF-EQUIV") for field in equiv.get("proposalFields", []) if isinstance(field, dict)):
        errors.append("evaluator mutation equivalence must not redefine runtime IF-EQUIV")
    truth_dependency = next((row for row in _rows(data, "dependencies") if row.get("id") == "DEP-TRUTH"), {})
    if set(truth_dependency.get("decisionIds", [])) != {"DEC-TRUTH", "DEC-EQUIV"}:
        errors.append("DEP-TRUTH must retain exactly the truth and equivalence decisions")
    if truth_dependency.get("blockingMilestone") != "pilot":
        errors.append("DEP-TRUTH blocking milestone must remain pilot")
    safe_projection = next(
        (
            field for field in next(
                (row for row in _rows(data, "dependencies") if row.get("id") == "DEP-IUT"), {}
            ).get("proposalFields", [])
            if isinstance(field, dict) and field.get("path") == "IF-EXP-SCENE.algorithmVisibleFields"
        ),
        {},
    )
    expected_safe_members = {
        ("sceneId", "string", "ALGORITHM-INITIAL"),
        ("serviceScope", "enum", "ALGORITHM-INITIAL"),
        ("registeredArm", "enum", "ALGORITHM-INITIAL"),
        ("resourceMode", "enum", "ALGORITHM-INITIAL"),
        ("publicConfigurationRef", "reference", "ALGORITHM-INITIAL"),
    }
    actual_safe_members = {
        (item.get("name"), item.get("type"), item.get("role"))
        for item in safe_projection.get("members", []) if isinstance(item, dict)
    }
    forbidden_safe_members = {
        "faultPlan", "truthSource", "injectionConfirmed", "validityClass",
        "equivalenceDisposition", "posthocAdjudication",
    }
    if actual_safe_members != expected_safe_members:
        errors.append("safe projection must retain the exact typed algorithm-visible member allowlist")
    if set(safe_projection.get("limits", {}).get("forbiddenMembers", [])) != forbidden_safe_members:
        errors.append("safe projection must retain the exact evaluator-only member denylist")
    if any(item[0] in forbidden_safe_members for item in actual_safe_members):
        errors.append("safe projection leaks evaluator-only truth or adjudication members")

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
    resource_decision = next((row for row in _rows(data, "pendingDecisions") if row.get("id") == "DEC-RESOURCE"), {})
    resource_text = " ".join(str(resource_decision.get(key, "")) for key in ("options", "recommendation", "selectionProcedure"))
    if "dual stop" in resource_text.lower() or "exactly one" not in resource_text.lower():
        errors.append("DEC-RESOURCE must select exactly one BUDGET or ROUNDS mode; retry cap remains separate")
    choice_rows = _rows(data, "analysisChoiceWalkthroughs")
    required_choice_results = {
        ("DETERMINISTIC-EXHAUSTIVE", "CANDIDATE-METHOD"),
        ("INDEPENDENT-RANDOMIZED", "CANDIDATE-METHOD"),
        ("PAIRED-OR-CLUSTERED", "CANDIDATE-METHOD"),
        ("NONE", "WAIT-DEC-SAMPLE"),
    }
    actual_choice_results = {(row.get("selectedBranch"), row.get("result")) for row in choice_rows}
    if not required_choice_results <= actual_choice_results:
        errors.append("analysis choice walkthroughs must cover census, independent, paired/clustered and missing-input WAIT branches")
    if not any(row.get("dependence") == "CLUSTERED" for row in choice_rows):
        errors.append("analysis choice walkthroughs must distinguish clustered evidence from paired evidence")
    for row in choice_rows:
        derived = _analysis_choice(row)
        actual = (row.get("selectedBranch"), row.get("result"))
        if derived != actual:
            errors.append(f"analysis choice {row.get('id')} disagrees with its independence/pairing inputs")
    translations = data.get("translationsZh", {})
    required_translation_keys = _translation_keys(data)
    if not isinstance(translations, dict):
        errors.append("translationsZh must be an object")
    else:
        missing_translations = required_translation_keys - set(translations)
        for key in sorted(missing_translations):
            errors.append(f"missing controlled Chinese translation {key}")
        for key in required_translation_keys & set(translations):
            value = translations.get(key)
            if not isinstance(value, str) or not value.strip() or not re.search(r"[\u3400-\u9fff]", value):
                errors.append(f"controlled Chinese translation is not substantive: {key}")
    errors.extend(_validate_protocol_timelines(data))
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
    metric_rows = {row.get("id"): row for row in _rows(data, "metrics")}

    def metric_fraction(metric_id: str) -> str:
        metric = metric_rows[metric_id]
        numerator = populations[str(metric["numeratorPopulationId"])]
        denominator = populations[str(metric["populationId"])]
        return _fraction(len(numerator), len(denominator))

    answered = populations["POP-ANSWERED"]
    attempts = populations["POP-ATTEMPTS"]
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
        "answeredCoverage": metric_fraction("MET-ANSWERED-COVERAGE"),
        "conditionalDetectionError": metric_fraction("MET-CONDITIONAL-DETECTION-ERROR"),
        "localizationDecisionCoverage": metric_fraction("MET-LOCALIZATION-COVERAGE"),
        "singletonLocalizationDecisions": len(populations["POP-SINGLETON-DECISION"]),
        "abstain": len(populations["POP-ABSTAIN"]),
        "unconfirmedInjection": sum(row.get("injectionStatus") == "UNCONFIRMED" for row in rows),
        "invalidObservation": sum(row.get("scenarioId") == "SC-INVALID-OBS" and row.get("validity") == "INVALID" for row in rows),
        "equivalentFault": sum(row.get("injectionStatus") == "EQUIVALENT" for row in rows),
        "unresolvedFault": sum(row.get("injectionStatus") == "UNRESOLVED" for row in rows),
        "projectedCostTotals": projected_clean,
        "reviewSetupEffort": sum(float(row.get("reviewSetupEffort", 0)) for row in rows),
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
