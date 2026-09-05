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
RG0_ANCHOR_PATH = ROOT / "configs/requirements/m1_rg0_source_inventory_anchor.json"
SECTION_SPAN_PATH = ROOT / "configs/requirements/m1_source_section_spans.json"
SEMANTIC_ASSERTION_PATH = ROOT / "configs/requirements/m1_semantic_review_assertions.json"
SUPPLEMENT_DISPOSITION_PATH = ROOT / "configs/requirements/m1_supplement_dispositions.json"
SOURCE_REGISTER_PATH = ROOT / "configs/research/controlled_sources.json"
GENERIC_OBSERVABLE_EFFECTS = {"STATE-OR-ENCODING-OUTCOME-OBSERVABLE"}
REQUIRED_PROFILE_SCOPE_KEYS = {
    "baseOperation",
    "supportingOperation",
    "deferredOperations",
    "configurationStatus",
    "bounded665ProfileScopeTriggerIds",
}


class M1Error(ValueError):
    pass


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def fingerprint(records: list[dict[str, Any]]) -> str:
    return hashlib.sha256(canonical(records)).hexdigest()


def source_inventory_projection(data: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "sourceUnitId": row["sourceUnitId"], "source": row["source"],
            "sourceTextHash": row["sourceTextHash"], "sourceModality": row["sourceModality"],
            "conformanceEffect": row["conformanceEffect"], "applicabilityDecision": row["applicabilityDecision"],
        }
        for row in data["coverageLedger"]
    ]


def timing_provenance_projection(data: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "sourceUnitId": row["sourceUnitId"], "provenanceKind": row["timing"].get("provenanceKind"),
            "sourceParameter": row["timing"].get("sourceParameter"), "lowerBound": row["timing"].get("lowerBound"),
            "upperBound": row["timing"].get("upperBound"), "timingFamily": row["timing"].get("timingFamily"),
            "trigger": row["timing"].get("trigger"), "response": row["timing"].get("response"),
            "cancellation": row["timing"].get("cancellation"), "supersedingTrigger": row["timing"].get("supersedingTrigger"),
            "correlationKey": row["timing"].get("correlationKey"), "pairingPolicy": row["timing"].get("pairingPolicy"),
        }
        for row in data["requirements"] if "timing" in row
    ]


def status_table_projection(data: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"sourceUnitId": row["sourceUnitId"], "constraint": row["statusTableConstraint"]}
        for row in data["requirements"] if "statusTableConstraint" in row
    ]


def field_constraint_projection(data: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"sourceUnitId": row["sourceUnitId"], "constraint": row["fieldConstraint"]}
        for row in data["requirements"] if "fieldConstraint" in row
    ]


def page_account_errors(section_manifest: dict[str, Any], register: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    spans_by_source = {source.get("sourceId"): source.get("spans", []) for source in section_manifest.get("sources", [])}
    exclusions_by_source: dict[str, list[dict[str, Any]]] = {}
    for exclusion in section_manifest.get("excludedRanges", []):
        exclusions_by_source.setdefault(exclusion.get("sourceId"), []).append(exclusion)
    for source in register.get("sources", []):
        source_id = source.get("id")
        page_count = source.get("pageCount")
        if not isinstance(page_count, int) or page_count <= 0:
            errors.append(f"controlled register {source_id} lacks a usable pageCount for the M1 page account")
            continue
        expected = set(range(1, page_count + 1))
        covered: set[int] = set()
        excluded: set[int] = set()
        for span in spans_by_source.get(source_id, []):
            start, end = span["pdfPages"]
            covered.update(range(start, end + 1))
        for exclusion in exclusions_by_source.get(source_id, []):
            start, end = exclusion["pdfPages"]
            excluded.update(range(start, end + 1))
        if covered & excluded:
            errors.append(f"section-span page account for {source_id} overlaps span and exclusion pages")
        accounted = covered | excluded
        if accounted != expected:
            missing = sorted(expected - accounted)
            extra = sorted(accounted - expected)
            errors.append(
                f"section-span page account for {source_id} is incomplete"
                + (f" missing={missing}" if missing else "")
                + (f" extra={extra}" if extra else "")
            )
    return errors


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
    try:
        anchor = json.loads(RG0_ANCHOR_PATH.read_text(encoding="utf-8"))
        section_manifest = json.loads(SECTION_SPAN_PATH.read_text(encoding="utf-8"))
        semantic_assertions = json.loads(SEMANTIC_ASSERTION_PATH.read_text(encoding="utf-8"))
        source_register = json.loads(SOURCE_REGISTER_PATH.read_text(encoding="utf-8"))
        supplement_dispositions = json.loads(SUPPLEMENT_DISPOSITION_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"M1 controlled review input is unavailable: {exc}"]
    errors.extend(page_account_errors(section_manifest, source_register))
    supplement_pages = [row.get("pdfPage") for row in supplement_dispositions.get("pages", [])]
    required_supplement_pages = list(range(155, 158)) + list(range(161, 165)) + list(range(167, 175))
    if supplement_dispositions.get("sourceId") != "ARINC-615A-3" or supplement_pages != required_supplement_pages:
        errors.append("supplement dispositions must cover every change-summary page exactly once and in order")
    for row in supplement_dispositions.get("pages", []):
        if row.get("disposition") != "INCORPORATED-IN-CONSOLIDATED-BODY-CANDIDATE" or not row.get("targetClauseRefs") or row.get("reviewStatus") != "PENDING-EXTERNAL-RG0":
            errors.append(f"supplement page {row.get('pdfPage')} lacks a reviewable candidate disposition")
    review_control = data["reviewControl"]
    supplement_fp = hashlib.sha256(canonical(supplement_dispositions)).hexdigest()
    if review_control.get("supplementDispositionFingerprint") != supplement_fp:
        errors.append("supplement-disposition fingerprint does not match the controlled register")
    if review_control.get("sectionSpanManifestFingerprint") != hashlib.sha256(canonical(section_manifest)).hexdigest():
        errors.append("section-span manifest fingerprint does not match the controlled manifest")
    if review_control.get("semanticAssertionFingerprint") != hashlib.sha256(canonical(semantic_assertions)).hexdigest():
        errors.append("semantic-assertion fingerprint does not match the controlled assertions")
    register_sources = {row.get("id"): row for row in source_register.get("sources", [])}
    for binding in data.get("sourceBindings", []):
        source_id = binding.get("sourceId")
        registered = register_sources.get(source_id)
        if registered is None:
            errors.append(f"source binding {source_id} is not in the controlled register")
            continue
        if binding.get("sha256") != registered.get("sha256"):
            errors.append(f"source binding {source_id} sha256 disagrees with the controlled register")
        if binding.get("role") != registered.get("role"):
            errors.append(f"source binding {source_id} role disagrees with the controlled register")
    scope = data.get("profileScope", {})
    if set(scope) != REQUIRED_PROFILE_SCOPE_KEYS:
        errors.append("profileScope must contain only the controlled M1 scope fields")
    if scope.get("baseOperation") != "UPLOAD":
        errors.append("profileScope.baseOperation must remain UPLOAD")
    if scope.get("supportingOperation") != "INFORMATION":
        errors.append("profileScope.supportingOperation must remain INFORMATION")
    if scope.get("deferredOperations") != ["DOWNLOAD", "FIND"]:
        errors.append("profileScope.deferredOperations must remain DOWNLOAD and FIND")
    if scope.get("configurationStatus") != "NOT YET ESTABLISHED":
        errors.append("profileScope.configurationStatus must remain NOT YET ESTABLISHED")
    spans_by_source: dict[str, list[dict[str, Any]]] = {}
    for source in section_manifest.get("sources", []):
        source_id = source.get("sourceId")
        spans = source.get("spans", [])
        if not source_id or not spans:
            errors.append("section-span manifest sources require non-empty spans")
            continue
        spans_by_source[source_id] = spans
        pdf_pages = [page for span in spans for page in range(span["pdfPages"][0], span["pdfPages"][1] + 1)]
        if len(pdf_pages) != len(set(pdf_pages)):
            errors.append(f"section-span manifest overlaps pages for {source_id}")
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
    source_unit_ids: list[str] = []
    for row in data["coverageLedger"]:
        source = row.get("source", {})
        source_unit_ids.append(str(row.get("sourceUnitId", "")))
        matching_spans = [span for span in spans_by_source.get(source.get("sourceId"), []) if span["pdfPages"][0] <= source.get("pdfPage", 0) <= span["pdfPages"][1]]
        if len(matching_spans) != 1:
            errors.append(f"coverage {row.get('id')} does not resolve to exactly one controlled section span")
        elif source.get("sourceId") == "ARINC-615A-3":
            namespace = matching_spans[0]["namespace"]
            clause = str(source.get("clause", ""))
            valid_namespace = (
                (namespace.startswith("SECTION-") and clause.startswith(namespace.removeprefix("SECTION-") + "."))
                or (namespace.startswith("ATTACHMENT-") and (clause == namespace or clause.startswith(namespace.removeprefix("ATTACHMENT-") + "-")))
                or (namespace.startswith("APPENDIX-") and (clause == namespace or clause.startswith(namespace.removeprefix("APPENDIX-") + "-")))
            )
            if not valid_namespace:
                errors.append(f"coverage {row.get('id')} clause {clause} escapes controlled namespace {namespace}")
            matching_guards = [guard for guard in section_manifest.get("clausePageGuards", []) if guard["sourceId"] == source.get("sourceId") and (clause == guard["clausePrefix"] or clause.startswith(guard["clausePrefix"] + "."))]
            if matching_guards and not any(guard["pdfPages"][0] <= source.get("pdfPage", 0) <= guard["pdfPages"][1] for guard in matching_guards):
                errors.append(f"coverage {row.get('id')} clause {clause} is outside its controlled clause page span")
        atomicity = row.get("atomicity", {})
        if atomicity.get("ownershipKind") != source.get("fragmentKind") or atomicity.get("singleOwner") is not True:
            errors.append(f"coverage {row.get('id')} has inconsistent atomic ownership")
        if source.get("fragmentKind") == "PROSE-SENTENCE" and atomicity.get("sentenceCount") != 1:
            errors.append(f"coverage {row.get('id')} prose unit must contain exactly one sentence")
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
    if len(source_unit_ids) != len(set(source_unit_ids)) or any(not item for item in source_unit_ids):
        errors.append("coverage sourceUnitId values must be non-empty and unique")
    for region in section_manifest.get("exclusiveOwnershipRegions", []):
        collisions = [
            row for row in data["coverageLedger"]
            if row["source"].get("sourceId") == region["sourceId"]
            and row["source"].get("pdfPage") == region["pdfPage"]
            and row["source"].get("fragmentKind") == "PROSE-SENTENCE"
            and row["source"].get("fragmentOrdinal", 0) >= region["proseFragmentOrdinalFrom"]
        ]
        if collisions:
            errors.append(f"exclusive non-prose region {region['tableOrFigure']} has prose co-owners")
    coverage_by_id = {row.get("id"): row for row in data["coverageLedger"]}
    requirement_by_id = {row.get("id"): row for row in data["requirements"]}
    bound_source_ids = {row.get("sourceId") for row in data["sourceBindings"]}
    source_hash_parts: dict[str, list[dict[str, Any]]] = {}
    for row in data["requirements"]:
        source = row.get("source", {})
        semantic = row.get("semantic", {})
        for field in ("actor", "condition", "action", "objects", "observableEffect", "operation", "polarity"):
            if not semantic.get(field):
                errors.append(f"requirement {row.get('id')} lacks semantic.{field}")
        semantic_values = [str(semantic.get("actor", "")), str(semantic.get("condition", "")), str(semantic.get("action", "")), *(str(item) for item in semantic.get("objects", [])), str(semantic.get("observableEffect", ""))]
        if any(re.search(r"^(?:SOURCE-(?:BOUND|DEFINED|IDENTIFIED)|CLAUSE-SPECIFIC|WHEN-CLAUSE-|DURING-.*-SCOPE$)|-$", value) for value in semantic_values):
            errors.append(f"requirement {row.get('id')} retains a non-reviewable semantic fallback")
        if semantic.get("observableEffect") in GENERIC_OBSERVABLE_EFFECTS:
            errors.append(f"requirement {row.get('id')} retains a generic observableEffect")
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
                "timingFamily", "provenanceKind", "sourceParameter", "sourceRelation",
                "trigger", "response", "cancellation", "supersedingTrigger", "correlationKey",
                "pairingPolicy", "concurrencyPolicy", "silenceSemantics", "lowerBound",
                "upperBound", "unit", "lowerBoundary", "upperBoundary", "clockStart",
                "clockResets", "observationState", "errorBudgetState", "ambiguityStatus", "sourceEvidenceUnitIds",
            }
            missing = timing_fields - set(timing)
            if missing:
                errors.append(f"requirement {row.get('id')} timing fields missing: {sorted(missing)}")
            for bound in ("lowerBound", "upperBound"):
                value = timing.get(bound)
                if value is None or (not isinstance(value, (int, float)) and not re.fullmatch(r"(?:UNBOUNDED|UNRESOLVED|[A-Z][A-Z0-9-]+)", str(value))):
                    errors.append(f"requirement {row.get('id')} has invalid {bound}")
            for source_unit_id in timing.get("sourceEvidenceUnitIds", []):
                if source_unit_id not in set(source_unit_ids):
                    errors.append(f"requirement {row.get('id')} timing evidence {source_unit_id} is not in the source inventory")
            for boundary in ("lowerBoundary", "upperBoundary"):
                if timing.get(boundary) not in {"OPEN", "CLOSED", "UNBOUNDED", "UNRESOLVED"}:
                    errors.append(f"requirement {row.get('id')} has invalid {boundary}")
        if source.get("tableOrFigure") and re.fullmatch(r"Table 6\.4\.[1-9]-1", str(source.get("tableOrFigure"))) and "fieldConstraint" not in row:
            errors.append(f"requirement {row.get('id')} table field lacks a structured field constraint")
        if "fieldConstraint" in row and source.get("fragmentKind") != "TABLE-ROW":
            errors.append(f"requirement {row.get('id')} field constraint is not owned by a table row")
        if row.get("roles") != [semantic.get("actor")] or row.get("operations") != [semantic.get("operation")] or row.get("category") != semantic.get("action") or row.get("obligations") != [semantic.get("action")]:
            errors.append(f"requirement {row.get('id')} denormalized semantic fields disagree with semantic")
        for dep_id in row.get("dependencyIds", []):
            if dep_id not in ids.get("dependencies", set()):
                errors.append(f"requirement {row.get('id')} has dangling dependency {dep_id}")
        for gap_id in row.get("gapIds", []):
            if gap_id not in ids.get("gaps", set()):
                errors.append(f"requirement {row.get('id')} has dangling gap {gap_id}")
        if source.get("sourceId") == "ARINC-665-5":
            profile_triggers = row.get("profileScopeTriggerIds", [])
            triggers = row.get("triggeredByRequirementIds", [])
            if profile_triggers != data.get("profileScope", {}).get("bounded665ProfileScopeTriggerIds"):
                errors.append(f"665-5 requirement {row.get('id')} does not preserve the profile-scope trigger set")
            relations = row.get("triggerRelations", [])
            if [item.get("requirementId") for item in relations] != triggers:
                errors.append(f"665-5 requirement {row.get('id')} trigger relations do not match its requirement-level edges")
            for trigger in triggers:
                if trigger not in requirement_by_id or requirement_by_id[trigger].get("source", {}).get("sourceId") != "ARINC-615A-3":
                    errors.append(f"665-5 requirement {row.get('id')} has invalid trigger {trigger}")
            for relation in relations:
                trigger = requirement_by_id.get(relation.get("requirementId"), {})
                rationale = str(relation.get("rationaleCode", ""))
                shared_object = rationale.removeprefix("SHARED-")
                if not rationale.startswith("SHARED-") or shared_object not in row.get("semantic", {}).get("objects", []) or shared_object not in trigger.get("semantic", {}).get("objects", []):
                    errors.append(f"665-5 requirement {row.get('id')} has an unsupported requirement-level trigger rationale")
            if row.get("bounded665Decision") not in {
                "APPLICABLE-AS-BOUNDED-6655-REFERENCE", "NOT-APPLICABLE-TO-CURRENT-PROFILE",
                "DEFERRED-VERSION-GAP", "BLOCKED-BY-ARINC-645", "UNSUPPORTED-BY-CURRENT-SOURCE",
            }:
                errors.append(f"665-5 requirement {row.get('id')} has invalid bounded decision")
            if row.get("refinementDisposition") not in {"PROFILE-SCOPE-ONLY", "DIRECT-DATA-FORMAT-REFINEMENT", "PRODUCER-CONSTRAINT", "CONSUMER-TOLERANCE", "DEPENDENCY-BLOCKED"}:
                errors.append(f"665-5 requirement {row.get('id')} lacks a controlled refinement disposition")
            if not row.get("refinementRationaleEn") or not row.get("refinementRationaleZh"):
                errors.append(f"665-5 requirement {row.get('id')} lacks bilingual refinement rationale")
        hash_key = str(row.get("sourceUnitId"))
        source_hash_parts.setdefault(hash_key, []).append(row)
        relation = row.get("rhoRA", {})
        if set(relation) != {"relation", "sourceCoverageId", "status"} or relation.get("relation") != "refines-reviewed-source-unit" or relation.get("status") != "CANDIDATE":
            errors.append(f"requirement {row.get('id')} rhoRA is not a closed candidate binding")
        coverage_id = relation.get("sourceCoverageId")
        if coverage_id not in coverage_by_id or row.get("id") not in coverage_by_id.get(coverage_id, {}).get("requirementIds", []):
            errors.append(f"requirement {row.get('id')} rho_RA does not close to its coverage row")
        else:
            coverage_row = coverage_by_id[coverage_id]
            identical_fields = (
                "sourceUnitId", "source", "sourceTextHash", "sourceModality",
                "conformanceEffect", "applicabilityDecision", "rationaleCode",
            )
            for field in identical_fields:
                if row.get(field) != coverage_row.get(field):
                    errors.append(f"requirement {row.get('id')} disagrees with coverage {coverage_id} on {field}")
    for rows in source_hash_parts.values():
        if len(rows) > 1 and any(not row.get("atomicPartId") or not row.get("splitRationale") for row in rows):
            errors.append(f"shared source hash requires atomicPartId and splitRationale: {[row.get('id') for row in rows]}")
    timing_rows = [row for row in data["requirements"] if "timing" in row]
    timing_tuples = {
        tuple(row["timing"].get(key) for key in ("timingFamily", "trigger", "response", "cancellation", "supersedingTrigger", "correlationKey", "pairingPolicy"))
        for row in timing_rows
    }
    if len(timing_rows) > 1 and len(timing_tuples) < 3:
        errors.append("timing requirements collapse into generic shared event semantics")
    requirements_by_id = {row.get("id"): row for row in data["requirements"]}
    asserted_ids: list[str] = []
    for assertion in semantic_assertions.get("assertions", []):
        requirement_id = assertion.get("requirementId")
        asserted_ids.append(requirement_id)
        row = requirements_by_id.get(requirement_id)
        if row is None:
            errors.append(f"semantic assertion requirement {requirement_id} is not represented")
            continue
        identity_fields = ("sourceUnitId", "sourceTextHash")
        for field in identity_fields:
            if row.get(field) != assertion.get(field):
                errors.append(f"semantic assertion {requirement_id} disagrees on {field}")
        expected_fields = {
            "semantic": assertion.get("expectedSemantic"),
            "paraphraseEn": assertion.get("expectedParaphraseEn"),
            "paraphraseZh": assertion.get("expectedParaphraseZh"),
            "roles": assertion.get("expectedRoles"),
            "operations": assertion.get("expectedOperations"),
            "category": assertion.get("expectedCategory"),
            "obligations": assertion.get("expectedObligations"),
            "sourceModality": assertion.get("expectedSourceModality"),
            "conformanceEffect": assertion.get("expectedConformanceEffect"),
            "dependencyIds": assertion.get("expectedDependencyIds"),
        }
        if "expectedTiming" in assertion:
            expected_fields["timing"] = assertion["expectedTiming"]
        elif "timing" in row:
            errors.append(f"semantic assertion {requirement_id} omits an existing timing proposition")
        if row.get("source", {}).get("sourceId") == "ARINC-665-5":
            expected_fields["triggerRelations"] = assertion.get("expectedTriggerRelations")
            expected_fields["refinementDisposition"] = assertion.get("expectedRefinementDisposition")
            expected_fields["refinementRationaleEn"] = assertion.get("expectedRefinementRationaleEn")
            expected_fields["refinementRationaleZh"] = assertion.get("expectedRefinementRationaleZh")
        if "fieldConstraint" in row:
            expected_fields["fieldConstraint"] = assertion.get("expectedFieldConstraint")
        for field, value in expected_fields.items():
            if row.get(field) != value:
                errors.append(f"semantic assertion {requirement_id} failed for {field}")
    if len(asserted_ids) != len(set(asserted_ids)) or set(asserted_ids) != set(requirements_by_id):
        errors.append("semantic assertions must cover every requirement exactly once")
    mapped_counts = Counter(
        requirement_id for coverage in data["coverageLedger"] for requirement_id in coverage.get("requirementIds", [])
    )
    for requirement_id in ids.get("requirements", set()):
        if mapped_counts[requirement_id] != 1:
            errors.append(f"requirement {requirement_id} must be mapped by exactly one coverage row")
    gap645 = next((row for row in data["gaps"] if row.get("id") == "GAP-ARINC-645"), None)
    expected_645 = {"CRC-VALIDATION", "CHECK-VALUE-VALIDATION", "NAMING-ALGORITHM-VALIDATION", "COMPLETE-INTEGRITY-VALIDATION"}
    if gap645 is None or gap645.get("status") != "NOT-ESTABLISHED" or set(gap645.get("affectedCapabilityIds", [])) != expected_645:
        errors.append("ARINC 645 gap must retain all four NOT-ESTABLISHED capabilities")
    for dependency in data["dependencies"]:
        if dependency.get("status") == "REGISTERED-SUPPORTING-SOURCE" and dependency.get("sourceId") not in bound_source_ids:
            errors.append(f"registered dependency {dependency.get('id')} lacks a controlled source binding")
        source_id = str(dependency.get("sourceId", ""))
        if re.search(r"RFC-\d+.*RFC-\d+|ARINC-\d+.*ARINC-\d+", source_id):
            errors.append(f"dependency {dependency.get('id')} combines multiple source identities")
    inventory_fp = fingerprint(source_inventory_projection(data))
    timing_fp = fingerprint(timing_provenance_projection(data))
    dependency_fp = fingerprint([row.get("sourceId") for row in data["dependencies"]])
    status_table_fp = fingerprint(status_table_projection(data))
    field_constraint_fp = fingerprint(field_constraint_projection(data))
    if data["reviewControl"].get("sourceInventoryFingerprint") != inventory_fp:
        errors.append("reviewControl.sourceInventoryFingerprint does not match the source-unit projection")
    anchor_expectations = {
        "sourceInventoryFingerprint": inventory_fp,
        "coverageCount": len(data["coverageLedger"]),
        "tableRowCount": sum(row.get("source", {}).get("fragmentKind") == "TABLE-ROW" for row in data["coverageLedger"]),
        "tableFootnoteCount": sum(row.get("source", {}).get("fragmentKind") == "TABLE-FOOTNOTE" for row in data["coverageLedger"]),
        "sequenceEventCount": sum(row.get("source", {}).get("fragmentKind") == "SEQUENCE-EVENT" for row in data["coverageLedger"]),
        "timingProvenanceFingerprint": timing_fp,
        "dependencySourceIdentityFingerprint": dependency_fp,
        "sectionSpanManifestFingerprint": review_control.get("sectionSpanManifestFingerprint"),
        "semanticAssertionFingerprint": review_control.get("semanticAssertionFingerprint"),
        "statusTableFingerprint": status_table_fp,
        "fieldConstraintFingerprint": field_constraint_fp,
        "supplementDispositionFingerprint": supplement_fp,
    }
    for key, value in anchor_expectations.items():
        if anchor.get(key) != value:
            errors.append(f"RG0 anchor {key} does not match the candidate package")
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
    if data["activation"].get("mergeEvidence") != "NOT-YET-PRESENT":
        errors.append("M1 merge evidence must remain absent in the Draft package")
    review_head = data["reviewControl"].get("reviewHead")
    if review_head != "UNBOUND-DRAFT" and not re.fullmatch(r"[0-9a-f]{40}", str(review_head or "")):
        errors.append("reviewHead must be UNBOUND-DRAFT or a complete 40-character SHA")
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
        f"- Source-unit fingerprint: `{data['reviewControl']['sourceInventoryFingerprint']}`",
        "- Automated checks cover structure and cross-record consistency only; proprietary-source completeness and fidelity require external RG0 review.",
    ]
    for title, key in (("Applicability", "applicabilityDecision"), ("Source modality", "sourceModality"), ("Conformance effect", "conformanceEffect")):
        lines += ["", f"## {title}", ""] + [f"- `{name}`: {count}" for name, count in sorted(_counts(requirements, key).items())]
    lines += ["", "## Open dependencies and gaps", ""]
    for row in data["dependencies"] + data["gaps"]:
        lines.append(f"- `{row['id']}` — {row['status']}: {row['summaryEn']} / {row['summaryZh']}")
    lines += ["", "## CRS items", "", "| ID | Source unit | Actor / condition / action / object / observable effect | Modality / effect | Applicability | Bilingual review paraphrase | Timing provenance | Dependencies / gaps |", "|---|---|---|---|---|---|---|---|"]
    for row in requirements:
        src = row["source"]
        sem = row["semantic"]
        semantic_view = f"`{sem['actor']}` / `{sem['condition']}` / `{sem['action']}` / `{', '.join(sem['objects'])}` / `{sem['observableEffect']}`"
        timing_view = "—" if "timing" not in row else f"`{row['timing']['provenanceKind']}` / `{row['timing']['sourceParameter']}` / `{row['timing']['sourceRelation']}` / `{row['timing']['lowerBound']}..{row['timing']['upperBound']} {row['timing']['unit']}` / evidence: {', '.join(row['timing']['sourceEvidenceUnitIds'])}"
        refs = ", ".join(row.get("dependencyIds", []) + row.get("gapIds", [])) or "—"
        lines.append(f"| `{row['id']}` | `{row['sourceUnitId']}`<br>`{src['sourceId']} {src['clause']} p.{src['documentPage']}` | {semantic_view} | `{row['sourceModality']}` / `{row['conformanceEffect']}` | `{row['applicabilityDecision']}` | {row['paraphraseEn']}<br>{row['paraphraseZh']} | {timing_view} | {refs} |")
    lines += ["", "## Observable timing semantics", "", "| CRS | Family | Trigger → response | Cancellation / superseding trigger | Correlation / pairing |", "|---|---|---|---|---|"]
    for row in (item for item in requirements if "timing" in item):
        timing = row["timing"]
        lines.append(f"| `{row['id']}` | `{timing['timingFamily']}` | `{timing['trigger']}` → `{timing['response']}` | `{timing['cancellation']}` / `{timing['supersedingTrigger']}` | `{timing['correlationKey']}` / `{timing['pairingPolicy']}` |")
    lines += ["", "## Requirement-level 615A → 665-5 traceability", "", "| 665-5 CRS | Profile-scope admission | Disposition | Requirement-specific relations |", "|---|---|---|---|"]
    for row in (item for item in requirements if item["source"]["sourceId"] == "ARINC-665-5"):
        relations = ", ".join(f"`{item['requirementId']}` ({item['relation']})" for item in row['triggerRelations']) or "—"
        lines.append(f"| `{row['id']}` | {', '.join(f'`{item}`' for item in row['profileScopeTriggerIds'])} | `{row['refinementDisposition']}` — {row['refinementRationaleEn']} | {relations} |")
    lines += ["", "## Structured protocol-file field constraints", "", "| CRS | File / ordinal | Field | Width | Repetition / presence | Encoding / termination | Notes |", "|---|---|---|---|---|---|---|"]
    for row in (item for item in requirements if "fieldConstraint" in item):
        c = row["fieldConstraint"]
        lines.append(f"| `{row['id']}` | `{c['protocolFile']}` / `{c['ordinal']}` | `{c['fieldId']}` | `{c['widthBitsExpression']}` | `{c['repeatScope']}` / `{c['presenceCondition']}` | `{c['encodingRule']}` / `{c['terminationRule']}` | {', '.join(c['noteRefs']) or '—'} |")
    lines += ["", "## Structured Table 6.4.10-1 constraints", "", "| CRS | Code / kind | Meaning / substitution | Display | Target text | Files / operations |", "|---|---|---|---|---|---|"]
    for row in (item for item in requirements if "statusTableConstraint" in item):
        constraint = row["statusTableConstraint"]
        if constraint["kind"] == "DISPLAY-FOOTNOTE":
            lines.append(f"| `{row['id']}` | `DISPLAY-FOOTNOTE` | `{constraint['substitutionRule']}` | — | — | — |")
        else:
            lines.append(f"| `{row['id']}` | `{constraint['code']}` | `{constraint['meaningCode']}` | `{constraint['displayMode']}` | `{constraint['targetTextRule']}` | `{', '.join(constraint['applicableProtocolFiles'])}` / `{', '.join(constraint['applicableOperations'])}` |")
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
        f"- 来源单元指纹：`{data['reviewControl']['sourceInventoryFingerprint']}`",
        "- 自动检查只覆盖结构与跨记录一致性；专有来源的完整性与忠实度仍须外部 RG0 评审。",
    ]
    for title, key in (("适用性", "applicabilityDecision"), ("来源模态", "sourceModality"), ("符合性效果", "conformanceEffect")):
        lines += ["", f"## {title}", ""] + [f"- `{name}`：{count}" for name, count in sorted(_counts(requirements, key).items())]
    lines += ["", "## 开放依赖与缺口", ""]
    for row in data["dependencies"] + data["gaps"]:
        lines.append(f"- `{row['id']}` — {row['status']}：{row['summaryZh']}")
    lines += ["", "## CRS 项", "", "| ID | 来源单元 | 参与者／条件／行为／对象／可观察结果 | 模态／效果 | 适用性 | 双语评审释义 | 时序溯源 | 依赖／缺口 |", "|---|---|---|---|---|---|---|---|"]
    for row in requirements:
        src = row["source"]; sem = row["semantic"]; refs = ", ".join(row.get("dependencyIds", []) + row.get("gapIds", [])) or "—"
        semantic_view = f"`{sem['actor']}` / `{sem['condition']}` / `{sem['action']}` / `{', '.join(sem['objects'])}` / `{sem['observableEffect']}`"
        timing_view = "—" if "timing" not in row else f"`{row['timing']['provenanceKind']}` / `{row['timing']['sourceParameter']}` / `{row['timing']['sourceRelation']}` / `{row['timing']['lowerBound']}..{row['timing']['upperBound']} {row['timing']['unit']}` / 证据：{', '.join(row['timing']['sourceEvidenceUnitIds'])}"
        lines.append(f"| `{row['id']}` | `{row['sourceUnitId']}`<br>`{src['sourceId']} {src['clause']} p.{src['documentPage']}` | {semantic_view} | `{row['sourceModality']}` / `{row['conformanceEffect']}` | `{row['applicabilityDecision']}` | {row['paraphraseZh']} | {timing_view} | {refs} |")
    lines += ["", "## 可观察时序语义", "", "| CRS | 事件族 | 触发 → 响应 | 取消／替代触发 | 关联／配对 |", "|---|---|---|---|---|"]
    for row in (item for item in requirements if "timing" in item):
        timing = row["timing"]
        lines.append(f"| `{row['id']}` | `{timing['timingFamily']}` | `{timing['trigger']}` → `{timing['response']}` | `{timing['cancellation']}` / `{timing['supersedingTrigger']}` | `{timing['correlationKey']}` / `{timing['pairingPolicy']}` |")
    lines += ["", "## 需求级 615A → 665-5 追溯", "", "| 665-5 CRS | Profile 范围准入 | 处置 | 需求特定关系 |", "|---|---|---|---|"]
    for row in (item for item in requirements if item["source"]["sourceId"] == "ARINC-665-5"):
        relations = ", ".join(f"`{item['requirementId']}` ({item['relation']})" for item in row['triggerRelations']) or "—"
        lines.append(f"| `{row['id']}` | {', '.join(f'`{item}`' for item in row['profileScopeTriggerIds'])} | `{row['refinementDisposition']}` — {row['refinementRationaleZh']} | {relations} |")
    lines += ["", "## 结构化协议文件字段约束", "", "| CRS | 文件／序号 | 字段 | 位宽 | 重复／出现条件 | 编码／终止 | 注释 |", "|---|---|---|---|---|---|---|"]
    for row in (item for item in requirements if "fieldConstraint" in item):
        c = row["fieldConstraint"]
        lines.append(f"| `{row['id']}` | `{c['protocolFile']}` / `{c['ordinal']}` | `{c['fieldId']}` | `{c['widthBitsExpression']}` | `{c['repeatScope']}` / `{c['presenceCondition']}` | `{c['encodingRule']}` / `{c['terminationRule']}` | {', '.join(c['noteRefs']) or '—'} |")
    lines += ["", "## 结构化 Table 6.4.10-1 约束", "", "| CRS | 状态码／类型 | 含义／替换 | 显示 | 目标文本 | 文件／操作 |", "|---|---|---|---|---|---|"]
    for row in (item for item in requirements if "statusTableConstraint" in item):
        constraint = row["statusTableConstraint"]
        if constraint["kind"] == "DISPLAY-FOOTNOTE":
            lines.append(f"| `{row['id']}` | `DISPLAY-FOOTNOTE` | `{constraint['substitutionRule']}` | — | — | — |")
        else:
            lines.append(f"| `{row['id']}` | `{constraint['code']}` | `{constraint['meaningCode']}` | `{constraint['displayMode']}` | `{constraint['targetTextRule']}` | `{', '.join(constraint['applicableProtocolFiles'])}` / `{', '.join(constraint['applicableOperations'])}` |")
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
