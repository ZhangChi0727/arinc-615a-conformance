#!/usr/bin/env python3
"""Validate the authoritative M1 package and render its review-only view."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any
import re

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PATH = ROOT / "configs/requirements/arinc_615a3_m1_crs.json"
SCHEMA_PATH = ROOT / "configs/requirements/m1_crs_package.schema.json"
VIEW_PATH = ROOT / "docs/control/requirements/ARINC615A3_M1_CRS_REVIEW_VIEW.md"


class M1Error(ValueError):
    pass


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def fingerprint(records: list[dict[str, Any]]) -> str:
    return hashlib.sha256(canonical(records)).hexdigest()


def load_package(path: Path = PACKAGE_PATH) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        jsonschema.Draft202012Validator(schema).validate(data)
    except jsonschema.ValidationError as exc:
        raise M1Error(f"schema violation at {list(exc.absolute_path)}: {exc.message}") from exc
    errors = package_errors(data)
    if errors:
        raise M1Error("; ".join(errors))
    return data


def package_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = ("sourceBindings", "coverageLedger", "requirements", "dependencies", "gaps", "reviewControl", "inventorySummary", "activation")
    for key in required:
        if key not in data:
            errors.append(f"missing top-level field {key}")
    if errors:
        return errors
    collections = {key: data[key] for key in ("coverageLedger", "requirements", "dependencies", "gaps")}
    ids: dict[str, set[str]] = {}
    for name, rows in collections.items():
        if not isinstance(rows, list):
            errors.append(f"{name} must be an array")
            continue
        row_ids = [row.get("id") for row in rows if isinstance(row, dict)]
        if len(row_ids) != len(rows) or any(not isinstance(item, str) or not item for item in row_ids):
            errors.append(f"{name} contains a missing/invalid id")
        if len(row_ids) != len(set(row_ids)):
            errors.append(f"{name} contains duplicate ids")
        if row_ids != sorted(row_ids):
            errors.append(f"{name} ids must be sorted")
        ids[name] = set(row_ids)
    locators: list[str] = []
    for row in data["coverageLedger"]:
        source = row.get("source", {})
        locator_key = json.dumps(source, sort_keys=True, ensure_ascii=False)
        locators.append(locator_key)
        requirement_ids = row.get("requirementIds", [])
        if (
            row.get("conformanceEffect") in {"REQUIRED", "CONDITIONAL-REQUIRED", "PROHIBITED"}
            and row.get("applicabilityDecision") in {"APPLICABLE-BASE", "APPLICABLE-SUPPORTING", "CONDITIONAL", "BLOCKED-BY-DEPENDENCY"}
            and not requirement_ids
        ):
            errors.append(f"normative coverage {row.get('id')} has no CRS mapping")
        for requirement_id in requirement_ids:
            if requirement_id not in ids.get("requirements", set()):
                errors.append(f"coverage {row.get('id')} has dangling requirement {requirement_id}")
    if len(locators) != len(set(locators)):
        errors.append("coverage locators must be unique")
    coverage_by_id = {row.get("id"): row for row in data["coverageLedger"]}
    bound_source_ids = {row.get("sourceId") for row in data["sourceBindings"]}
    source_hash_parts: dict[tuple[str, str, int, str], list[dict[str, Any]]] = {}
    for row in data["requirements"]:
        source = row.get("source", {})
        if row.get("paraphraseEn") == row.get("paraphraseZh"):
            errors.append(f"requirement {row.get('id')} bilingual paraphrases must differ")
        if any(token in row.get("paraphraseEn", "") for token in ("CLAUSE-SPECIFIC-BEHAVIOR", "SOURCE-DEFINED-NORMATIVE-BEHAVIOR")):
            errors.append(f"requirement {row.get('id')} retains an uninformative paraphrase fallback")
        if not row.get("obligations"):
            errors.append(f"requirement {row.get('id')} has no obligation")
        if len(row.get("obligations", [])) > 1 and not row.get("inseparableRationale"):
            errors.append(f"compound requirement {row.get('id')} lacks an inseparable rationale")
        if row.get("sourceModality") == "SHOULD" and row.get("conformanceEffect") not in {"REQUIRED", "CONDITIONAL-REQUIRED", "PROHIBITED"}:
            errors.append(f"requirement {row.get('id')} downgrades source SHOULD")
        if row.get("sourceModality") == "MAY" and row.get("conformanceEffect") == "REQUIRED":
            errors.append(f"requirement {row.get('id')} upgrades source MAY without a condition")
        timing = row.get("timing")
        if timing is not None:
            timing_fields = {
                "trigger", "response", "cancellation", "supersedingTrigger", "correlationKey",
                "pairingPolicy", "concurrencyPolicy", "silenceSemantics", "lowerBound",
                "upperBound", "unit", "lowerBoundary", "upperBoundary", "clockStart",
                "clockResets", "observationState", "errorBudgetState",
            }
            missing = timing_fields - set(timing)
            if missing:
                errors.append(f"requirement {row.get('id')} timing fields missing: {sorted(missing)}")
            for bound in ("lowerBound", "upperBound"):
                value = timing.get(bound)
                if value is None or (not isinstance(value, (int, float)) and value not in {"UNBOUNDED", "UNRESOLVED"}):
                    errors.append(f"requirement {row.get('id')} has invalid {bound}")
            for boundary in ("lowerBoundary", "upperBoundary"):
                if timing.get(boundary) not in {"OPEN", "CLOSED", "UNBOUNDED", "UNRESOLVED"}:
                    errors.append(f"requirement {row.get('id')} has invalid {boundary}")
        for dep_id in row.get("dependencyIds", []):
            if dep_id not in ids.get("dependencies", set()):
                errors.append(f"requirement {row.get('id')} has dangling dependency {dep_id}")
        for gap_id in row.get("gapIds", []):
            if gap_id not in ids.get("gaps", set()):
                errors.append(f"requirement {row.get('id')} has dangling gap {gap_id}")
        if source.get("sourceId") == "ARINC-665-5":
            triggers = row.get("triggeredByRequirementIds", [])
            if not triggers:
                errors.append(f"665-5 requirement {row.get('id')} lacks a 615A-3 trigger")
            for trigger in triggers:
                if trigger not in ids.get("requirements", set()) or not trigger.startswith("CRS-615A3-"):
                    errors.append(f"665-5 requirement {row.get('id')} has invalid trigger {trigger}")
            if row.get("bounded665Decision") not in {
                "APPLICABLE-AS-BOUNDED-6655-REFERENCE", "NOT-APPLICABLE-TO-CURRENT-PROFILE",
                "DEFERRED-VERSION-GAP", "BLOCKED-BY-ARINC-645", "UNSUPPORTED-BY-CURRENT-SOURCE",
            }:
                errors.append(f"665-5 requirement {row.get('id')} has invalid bounded decision")
        hash_key = (str(source.get("sourceId")), str(source.get("clause")), int(source.get("pdfPage", 0)), str(row.get("sourceTextHash")))
        source_hash_parts.setdefault(hash_key, []).append(row)
        relation = row.get("rhoRA", {})
        coverage_id = relation.get("sourceCoverageId")
        if coverage_id not in coverage_by_id or row.get("id") not in coverage_by_id.get(coverage_id, {}).get("requirementIds", []):
            errors.append(f"requirement {row.get('id')} rho_RA does not close to its coverage row")
    for rows in source_hash_parts.values():
        if len(rows) > 1 and any(not row.get("atomicPartId") or not row.get("splitRationale") for row in rows):
            errors.append(f"shared source hash requires atomicPartId and splitRationale: {[row.get('id') for row in rows]}")
    gap645 = next((row for row in data["gaps"] if row.get("id") == "GAP-ARINC-645"), None)
    expected_645 = {"CRC-VALIDATION", "CHECK-VALUE-VALIDATION", "NAMING-ALGORITHM-VALIDATION", "COMPLETE-INTEGRITY-VALIDATION"}
    if gap645 is None or gap645.get("status") != "NOT-ESTABLISHED" or set(gap645.get("affectedCapabilityIds", [])) != expected_645:
        errors.append("ARINC 645 gap must retain all four NOT-ESTABLISHED capabilities")
    for dependency in data["dependencies"]:
        if dependency.get("status") == "REGISTERED-SUPPORTING-SOURCE" and dependency.get("sourceId") not in bound_source_ids:
            errors.append(f"registered dependency {dependency.get('id')} lacks a controlled source binding")
    summary = data["inventorySummary"]
    expected = {
        "coverageCount": len(data["coverageLedger"]),
        "requirementCount": len(data["requirements"]),
        "dependencyCount": len(data["dependencies"]),
        "gapCount": len(data["gaps"]),
        "coverageFingerprint": fingerprint(data["coverageLedger"]),
        "requirementsFingerprint": fingerprint(data["requirements"]),
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            errors.append(f"inventorySummary.{key} does not match governed records")
    if data["reviewControl"].get("rg0") != "PENDING-EXTERNAL-INDEPENDENT-REVIEW" or data["reviewControl"].get("rg1") != "PENDING-EXTERNAL-INDEPENDENT-REVIEW":
        errors.append("RG0/RG1 must remain pending in the Draft package")
    if data["activation"].get("formalApproval") != "EXTERNAL-JOINT-CONDITION-NOT-YET-SATISFIED":
        errors.append("M1 formal approval must remain external and unsatisfied")
    forbidden_keys = {"rawSourceText", "sourceText", "quote", "excerpt", "screenshot", "payload", "pdfPath"}
    machine_path = re.compile(r"(?i)(?:[a-z]:[\\/]|file://|/(?:home|Users)/[^/]+/)")  # STABLE_INVARIANT
    reversible = re.compile(r"^(?:[A-Za-z0-9+/]{160,}={0,2}|[0-9a-fA-F]{256,})$")
    def scan(value: Any, path: str = "$") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in forbidden_keys:
                    errors.append(f"proprietary-source field is prohibited at {path}.{key}")
                scan(child, f"{path}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value): scan(child, f"{path}[{index}]")
        elif isinstance(value, str):
            if machine_path.search(value): errors.append(f"machine-local path is prohibited at {path}")
            if reversible.fullmatch(value): errors.append(f"reversible source payload is prohibited at {path}")
    scan(data)
    return errors


def _counts(rows: list[dict[str, Any]], key: str) -> Counter[str]:
    return Counter(str(row.get(key, "UNSPECIFIED")) for row in rows)


def render(data: dict[str, Any]) -> str:
    coverage = data["coverageLedger"]
    requirements = data["requirements"]
    lines = [
        "# ARINC 615A-3 M1 CRS and Applicability — Generated Review View",
        "",
        "> Generated from `configs/requirements/arinc_615a3_m1_crs.json` by `python scripts/sync_m1_crs.py --write`. Do not edit this view.",
        "",
        "## Candidate state",
        "",
        f"- Disposition: `{data['candidateDisposition']}`",
        f"- RG0: `{data['reviewControl']['rg0']}`",
        f"- RG1: `{data['reviewControl']['rg1']}`",
        f"- Formal approval: `{data['activation']['formalApproval']}`",
        "- This package establishes neither Project Configuration nor protocol conformance.",
        "",
        "## Inventory",
        "",
        f"- Coverage rows: {len(coverage)}",
        f"- CRS items: {len(requirements)}",
        f"- Dependencies: {len(data['dependencies'])}",
        f"- Gaps: {len(data['gaps'])}",
        f"- Coverage fingerprint: `{data['inventorySummary']['coverageFingerprint']}`",
        f"- Requirements fingerprint: `{data['inventorySummary']['requirementsFingerprint']}`",
    ]
    for title, key in (("Applicability", "applicabilityDecision"), ("Source modality", "sourceModality"), ("Conformance effect", "conformanceEffect")):
        lines += ["", f"## {title}", ""] + [f"- `{name}`: {count}" for name, count in sorted(_counts(requirements, key).items())]
    lines += ["", "## Open dependencies and gaps", ""]
    for row in data["dependencies"] + data["gaps"]:
        lines.append(f"- `{row['id']}` — {row['status']}: {row['summaryEn']} / {row['summaryZh']}")
    lines += ["", "## CRS items", "", "| ID | Source | Modality / effect | Applicability | Review paraphrase | Dependencies / gaps |", "|---|---|---|---|---|---|"]
    for row in requirements:
        src = row["source"]
        refs = ", ".join(row.get("dependencyIds", []) + row.get("gapIds", [])) or "—"
        lines.append(f"| `{row['id']}` | `{src['sourceId']} {src['clause']} p.{src['documentPage']}` | `{row['sourceModality']}` / `{row['conformanceEffect']}` | `{row['applicabilityDecision']}` | {row['paraphraseEn']}<br>{row['paraphraseZh']} | {refs} |")
    lines += ["", "## Non-base and unresolved inventory", ""]
    for row in coverage:
        if row["applicabilityDecision"] not in {"APPLICABLE-BASE", "APPLICABLE-SUPPORTING"}:
            lines.append(f"- `{row['id']}` — `{row['applicabilityDecision']}` — {row['rationaleCode']}")
    lines += [
        "", "# 中文版", "",
        "本文件由 `configs/requirements/arinc_615a3_m1_crs.json` 生成；请勿手工编辑。", "",
        "## 候选状态", "",
        f"- 处置：`{data['candidateDisposition']}`",
        f"- RG0：`{data['reviewControl']['rg0']}`",
        f"- RG1：`{data['reviewControl']['rg1']}`",
        f"- 正式批准：`{data['activation']['formalApproval']}`",
        "- 本数据包不建立 Project Configuration 或协议符合性。", "",
        "## 清单", "",
        f"- 覆盖行：{len(coverage)}", f"- CRS 项：{len(requirements)}",
        f"- 依赖：{len(data['dependencies'])}", f"- 缺口：{len(data['gaps'])}",
        f"- 覆盖指纹：`{data['inventorySummary']['coverageFingerprint']}`",
        f"- 需求指纹：`{data['inventorySummary']['requirementsFingerprint']}`",
    ]
    for title, key in (("适用性", "applicabilityDecision"), ("来源模态", "sourceModality"), ("符合性效果", "conformanceEffect")):
        lines += ["", f"## {title}", ""] + [f"- `{name}`：{count}" for name, count in sorted(_counts(requirements, key).items())]
    lines += ["", "## 开放依赖与缺口", ""]
    for row in data["dependencies"] + data["gaps"]:
        lines.append(f"- `{row['id']}` — {row['status']}：{row['summaryZh']}")
    lines += ["", "## CRS 项", "", "| ID | 来源 | 模态／效果 | 适用性 | 评审释义 | 依赖／缺口 |", "|---|---|---|---|---|---|"]
    for row in requirements:
        src = row["source"]; refs = ", ".join(row.get("dependencyIds", []) + row.get("gapIds", [])) or "—"
        lines.append(f"| `{row['id']}` | `{src['sourceId']} {src['clause']} p.{src['documentPage']}` | `{row['sourceModality']}` / `{row['conformanceEffect']}` | `{row['applicabilityDecision']}` | {row['paraphraseZh']} | {refs} |")
    lines += ["", "## 非基础范围及未决清单", ""]
    for row in coverage:
        if row["applicabilityDecision"] not in {"APPLICABLE-BASE", "APPLICABLE-SUPPORTING"}:
            lines.append(f"- `{row['id']}` — `{row['applicabilityDecision']}` — {row['rationaleCode']}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        data = load_package()
        expected = render(data)
    except (OSError, json.JSONDecodeError, M1Error) as exc:
        print(f"M1 CRS validation failed: {exc}", file=sys.stderr)
        return 1
    if args.write:
        VIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
        VIEW_PATH.write_text(expected, encoding="utf-8", newline="\n")
        return 0
    actual = VIEW_PATH.read_text(encoding="utf-8") if VIEW_PATH.exists() else ""
    if actual != expected:
        print("generated M1 review view is stale; run sync_m1_crs.py --write", file=sys.stderr)
        return 1
    print(f"M1 CRS validation passed: coverage={len(data['coverageLedger'])}, requirements={len(data['requirements'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
