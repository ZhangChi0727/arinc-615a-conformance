"""Validate the bounded CL-TAV experiment implementation design.

This checker proves structural closure and synthetic accounting only.  It does
not approve novelty, mathematical arguments, fairness, protocol interpretation,
or confirmatory execution.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
DESIGN_PATH = Path("configs/research/cltav_experiment_design.json")
SCHEMA_PATH = Path("configs/research/cltav_experiment_design.schema.json")
REGISTRY_PATH = Path("configs/research/cltav_interface_registry.json")
DEVELOPMENT_PATH = Path("configs/engineering/cltav_development_contracts.json")
CLAIM_PATH = Path("docs/research/CLAIM_EVIDENCE_MATRIX.md")


def _load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _duplicates(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if count > 1)


def _git_blob_bytes(root: Path, oid: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", oid], cwd=root)


def _safe_relative(path: str) -> bool:
    candidate = Path(path)
    return bool(path) and not candidate.is_absolute() and ".." not in candidate.parts


def _ids(rows: object, label: str, errors: list[str]) -> set[str]:
    if not isinstance(rows, list):
        errors.append(f"{label} must be an array")
        return set()
    values = [row.get("id", "") for row in rows if isinstance(row, dict)]
    for value in _duplicates(values):
        errors.append(f"duplicate {label} id {value}")
    return set(values)


def _ref_errors(values: list[str], allowed: set[str], label: str) -> list[str]:
    return [f"unknown {label} reference {value}" for value in values if value not in allowed]


def _field_reference_errors(
    references: list[str], records: dict[str, set[str]], interfaces: dict[str, set[str]]
) -> list[str]:
    errors: list[str] = []
    for reference in references:
        owner, separator, field = reference.partition(".")
        if not separator or not field:
            errors.append(f"field reference must use OWNER.member: {reference}")
        elif owner in records and field not in records[owner]:
            errors.append(f"unknown record field {reference}")
        elif owner in interfaces and field not in interfaces[owner]:
            errors.append(f"unknown interface output {reference}")
        elif owner not in records and owner not in interfaces:
            errors.append(f"unknown field-reference owner {owner}")
    return errors


def validate_design(root: Path = ROOT, design: dict | None = None) -> list[str]:
    errors: list[str] = []
    try:
        data = design if design is not None else _load(root / DESIGN_PATH)
        schema = _load(root / SCHEMA_PATH)
        registry = _load(root / REGISTRY_PATH)
        development = _load(root / DEVELOPMENT_PATH)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read experiment-design input: {exc}"]
    if not all(isinstance(item, dict) for item in (data, schema, registry, development)):
        return ["experiment-design inputs must be JSON objects"]

    for issue in Draft202012Validator(schema).iter_errors(data):
        location = ".".join(str(part) for part in issue.absolute_path) or "<root>"
        errors.append(f"schema {location}: {issue.message}")

    bindings = data.get("inputBindings", [])
    binding_paths = [row.get("path", "") for row in bindings if isinstance(row, dict)]
    for value in _duplicates(binding_paths):
        errors.append(f"duplicate input binding {value}")
    for row in bindings:
        if not isinstance(row, dict):
            continue
        relative = row.get("path", "")
        oid = row.get("gitBlobOid", "")
        if not _safe_relative(relative):
            errors.append(f"unsafe input binding path {relative!r}")
            continue
        try:
            resolved_oid = subprocess.check_output(
                ["git", "rev-parse", f"{data['identity']['baseCommit']}:{relative}"],
                cwd=root,
                text=True,
            ).strip()
            blob = _git_blob_bytes(root, oid)
        except (subprocess.CalledProcessError, OSError, KeyError) as exc:
            errors.append(f"cannot resolve bound Git blob {relative}: {exc}")
            continue
        if resolved_oid != oid:
            errors.append(f"input binding OID mismatch for {relative}: {oid} != {resolved_oid}")
        digest = hashlib.sha256(blob).hexdigest()
        if digest != row.get("sha256"):
            errors.append(f"input binding SHA-256 mismatch for {relative}")

    refs = data.get("references", {})
    registry_arms = set(registry.get("arms", []))
    registry_families = set(registry.get("experimentIds", []))
    registry_algorithm = {row.get("id") for row in registry.get("interfaces", [])}
    registry_experiment = {row.get("id") for row in registry.get("experimentInterfaces", [])}
    development_scenarios = {row.get("id") for row in development.get("experimentScenarios", [])}
    development_matrix = {row.get("id") for row in development.get("acceptanceMatrix", [])}
    development_records = {
        row.get("id"): set(row.get("fields", []))
        for row in development.get("recordContracts", [])
        if isinstance(row, dict)
    }
    interface_outputs = {
        row.get("id"): set(row.get("outputs", []))
        for row in [*registry.get("interfaces", []), *registry.get("experimentInterfaces", [])]
        if isinstance(row, dict)
    }
    expected_refs = (
        ("arms", registry_arms),
        ("families", registry_families),
        ("scenarios", development_scenarios),
        ("acceptanceMatrix", development_matrix),
        ("algorithmInterfaces", registry_algorithm),
        ("experimentInterfaces", registry_experiment),
        ("records", set(development_records)),
    )
    for key, expected in expected_refs:
        actual = set(refs.get(key, []))
        if actual != expected:
            errors.append(f"references.{key} must equal its bound authority: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}")

    try:
        claim_text = (root / CLAIM_PATH).read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read claim matrix: {exc}")
        claim_text = ""
    for claim_id in refs.get("claims", []):
        if not re.search(rf"\|\s*{re.escape(claim_id)}\s*\|", claim_text):
            errors.append(f"unknown claim reference {claim_id}")

    argument_ids: set[str] = set()
    for argument in data.get("claimArguments", []):
        claim_id = argument.get("claimId", "")
        if claim_id in argument_ids:
            errors.append(f"duplicate claim argument id {claim_id}")
        argument_ids.add(claim_id)
    if argument_ids != {"CL-C1", "CL-C2"}:
        errors.append("claimArguments must contain exactly CL-C1 and CL-C2")

    arm_ids = _ids(data.get("arms"), "arm", errors)
    if arm_ids != registry_arms:
        errors.append(f"arm design must contain exactly {sorted(registry_arms)}")
    for arm in data.get("arms", []):
        text = " ".join([*arm.get("visibleInputs", []), *arm.get("actions", [])]).lower()
        if "evaluator truth" in text:
            errors.append(f"truth leakage into arm {arm.get('id')}")
        if arm.get("id") in {"CL-T", "CL-A", "CL-TA"} and arm.get("feedback"):
            errors.append(f"non-loop arm {arm.get('id')} cannot receive feedback")
        if arm.get("id") == "CL-A" and ("adaptive" in text or "acquisition" in arm.get("costComponents", [])):
            errors.append("CL-A cannot receive adaptive future records or invented acquisition cost")

    dependency_ids = _ids(data.get("dependencies"), "dependency", errors)
    scenario_ids = _ids(data.get("scenarios"), "scenario", errors)
    if scenario_ids != development_scenarios:
        errors.append(f"scenario design must contain exactly {sorted(development_scenarios)}")
    for scenario in data.get("scenarios", []):
        errors.extend(_ref_errors(scenario.get("familyIds", []), registry_families, "experiment family"))
        errors.extend(_ref_errors(scenario.get("acceptanceMatrixRefs", []), development_matrix, "acceptance-matrix"))
        errors.extend(_ref_errors(scenario.get("dependencyIds", []), dependency_ids, "dependency"))
        if scenario.get("serviceScope") not in {"UPLOAD", "INFORMATION"}:
            errors.append(f"scenario {scenario.get('id')} silently activates service {scenario.get('serviceScope')}")

    metric_ids = _ids(data.get("metrics"), "metric", errors)
    for metric in data.get("metrics", []):
        if not metric.get("denominator"):
            errors.append(f"metric {metric.get('id')} lacks a denominator")
        if metric.get("zeroDenominator") != "N/A":
            errors.append(f"metric {metric.get('id')} must report an empty denominator as N/A")
        errors.extend(_ref_errors(metric.get("familyIds", []), registry_families, "experiment family"))
        errors.extend(_field_reference_errors(metric.get("requiredFields", []), development_records, interface_outputs))

    consumers = set(refs.get("scenarios", [])) | set(refs.get("families", [])) | metric_ids
    for dependency in data.get("dependencies", []):
        errors.extend(_ref_errors(dependency.get("consumers", []), consumers, "dependency consumer"))
        if dependency.get("state") != "EXISTING-REFERENCE" and not dependency.get("closureTest"):
            errors.append(f"pending dependency {dependency.get('id')} lacks closure evidence")

    decision_ids = _ids(data.get("pendingDecisions"), "pending decision", errors)
    for decision in data.get("pendingDecisions", []):
        if decision.get("status") != "OPEN":
            errors.append(f"pending decision {decision.get('id')} cannot be marked complete by this design")
        for field in ("ownerRole", "evidenceNeeded", "freezeBy"):
            if not decision.get(field):
                errors.append(f"pending decision {decision.get('id')} lacks {field}")
    admission = data.get("designAdmission", {})
    if admission.get("confirmatoryRunStatus") != "BLOCKED":
        errors.append("candidate design cannot mark confirmatory execution ready")
    errors.extend(_ref_errors(admission.get("blockingDecisionIds", []), decision_ids, "blocking decision"))
    if admission.get("historicalCaptureUse") != "EXPLORATORY-OFFLINE-ONLY":
        errors.append("historical captures cannot become interactive truth-bearing scenarios")

    attempts: list[str] = []
    for row in data.get("syntheticWalkthroughs", []):
        attempts.append(row.get("attemptId", ""))
        if row.get("label") != "SYNTHETIC-DESIGN-WALKTHROUGH":
            errors.append(f"walkthrough {row.get('id')} is not explicitly synthetic")
        if row.get("scenarioId") not in development_scenarios:
            errors.append(f"walkthrough {row.get('id')} has unknown scenario {row.get('scenarioId')}")
        if "attempt" not in row.get("denominators", []):
            errors.append(f"walkthrough {row.get('id')} is missing the all-attempt denominator")
        if row.get("validity") == "UNCONFIRMED-INJECTION" and row.get("runId") is not None:
            errors.append(f"walkthrough {row.get('id')} invents a run for an unconfirmed injection")
        if row.get("validity") == "EQUIVALENT-FAULT" and row.get("runId") is not None:
            errors.append(f"walkthrough {row.get('id')} runs a pre-run equivalent case")
        if row.get("outcome") in {"PASS", "FAIL"} and row.get("validity") != "VALID":
            errors.append(f"walkthrough {row.get('id')} assigns PASS/FAIL to invalid evidence")
        if row.get("stopClass") in {"Stop-645", "Stop-Budget"} and sum(row.get("chargedCost", {}).values()) <= 0:
            errors.append(f"walkthrough {row.get('id')} hides spent cost at {row.get('stopClass')}")
    for value in _duplicates(attempts):
        errors.append(f"duplicate synthetic attempt {value}")

    artifact_ids = _ids(data.get("artifactMap"), "artifact", errors)
    if len(artifact_ids) < 4:
        errors.append("artifactMap must retain the design, claims, plan and checker authorities")
    return errors


def accounting_summary(data: dict) -> dict[str, object]:
    rows = data["syntheticWalkthroughs"]
    answered = [row for row in rows if row["outcome"] in {"PASS", "FAIL"}]
    singleton = [row for row in rows if len(row["finalHypotheses"]) == 1 and "localization-decision" in row["denominators"]]
    return {
        "attempts": len({row["attemptId"] for row in rows}),
        "answered": len(answered),
        "fails": sum(row["outcome"] == "FAIL" for row in answered),
        "pass": sum(row["outcome"] == "PASS" for row in answered),
        "singletonLocalizationDecisions": len(singleton),
        "abstain": sum("abstain" in row["denominators"] for row in rows),
        "unconfirmedInjection": sum("unconfirmed-injection" in row["denominators"] for row in rows),
        "invalidObservation": sum("invalid-observation" in row["denominators"] for row in rows),
        "equivalentFault": sum("equivalent-fault" in row["denominators"] for row in rows),
        "emptyAnsweredRate": "N/A" if not answered else f"{len(answered)}/{len(rows)}",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", action="store_true", help="print the synthetic design ledger summary")
    args = parser.parse_args()
    errors = validate_design()
    if errors:
        print("Experiment design check failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Experiment design check passed")
    if args.summary:
        print(json.dumps(accounting_summary(_load(ROOT / DESIGN_PATH)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
