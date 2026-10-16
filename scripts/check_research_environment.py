"""Validate the repository's reusable research-environment contracts."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import shutil
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
ENVIRONMENT = Path("configs/research/research_environment.json")

CSV_CONTRACTS = {
    "searchLog": (
        "search_id",
        "executed_at",
        "database",
        "query",
        "filters",
        "result_count",
        "export_ref",
        "operator",
        "notes",
    ),
    "screeningLedger": (
        "candidate_id",
        "source_id",
        "title",
        "year",
        "doi",
        "database",
        "search_ids",
        "stage",
        "decision",
        "reason",
        "decided_by",
        "decided_at",
        "full_text_status",
        "notes",
    ),
    "evidenceLedger": (
        "evidence_id",
        "source_id",
        "locator",
        "evidence_type",
        "proposition",
        "private_note_ref",
        "access_level",
        "support_status",
        "quality_notes",
        "extracted_by",
        "verified_by",
        "verified_at",
    ),
    "claimCitationLedger": (
        "mapping_id",
        "claim_id",
        "source_id",
        "evidence_id",
        "relationship",
        "status",
        "scope_limit",
        "reviewed_by",
        "reviewed_at",
    ),
}

ID_FIELDS = {
    "searchLog": "search_id",
    "screeningLedger": "candidate_id",
    "evidenceLedger": "evidence_id",
    "claimCitationLedger": "mapping_id",
}

TOOLS = (
    ("python", True),
    ("pdflatex", True),
    ("bibtex", True),
    ("latexmk", False),
    ("pandoc", False),
    ("java", False),
    ("plantuml", False),
    ("dot", False),
    ("inkscape", False),
    ("drawio", False),
)


def _load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"unreadable JSON {path.as_posix()}: {exc}")
        return None


def duplicate_values(rows: Iterable[dict[str, str]], field: str) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for row in rows:
        value = (row.get(field) or "").strip()
        if not value:
            continue
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def _validate_csv(path: Path, expected: tuple[str, ...], id_field: str) -> list[str]:
    errors: list[str] = []
    try:
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            actual = tuple(reader.fieldnames or ())
            rows = list(reader)
    except OSError as exc:
        return [f"unreadable CSV {path.as_posix()}: {exc}"]
    if actual != expected:
        errors.append(
            f"CSV header mismatch for {path.as_posix()}: expected {expected}, got {actual}"
        )
        return errors
    for row_number, row in enumerate(rows, start=2):
        if not any((value or "").strip() for value in row.values()):
            errors.append(f"blank data row in {path.as_posix()}:{row_number}")
        elif not (row.get(id_field) or "").strip():
            errors.append(f"missing {id_field} in {path.as_posix()}:{row_number}")
    for value in duplicate_values(rows, id_field):
        errors.append(f"duplicate {id_field} {value!r} in {path.as_posix()}")
    return errors


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def _ledger_link_errors(root: Path, registries: dict[str, object]) -> list[str]:
    """Validate source/evidence references without upgrading review status."""
    errors: list[str] = []
    try:
        screening = _read_csv(root / str(registries["screeningLedger"]))
        evidence = _read_csv(root / str(registries["evidenceLedger"]))
        mappings = _read_csv(root / str(registries["claimCitationLedger"]))
    except (OSError, KeyError) as exc:
        return [f"cannot cross-check literature ledgers: {exc}"]
    screened_sources = {row.get("source_id", "") for row in screening}
    evidence_by_id = {row.get("evidence_id", ""): row for row in evidence}
    for row in evidence:
        if row.get("source_id") not in screened_sources:
            errors.append(
                f"evidence {row.get('evidence_id')} source is absent from screening ledger: "
                f"{row.get('source_id')}"
            )
    for row in mappings:
        mapping_id = row.get("mapping_id")
        evidence_id = row.get("evidence_id")
        source_id = row.get("source_id")
        linked = evidence_by_id.get(evidence_id or "")
        if linked is None:
            errors.append(f"mapping {mapping_id} has unknown evidence id {evidence_id}")
        elif linked.get("source_id") != source_id:
            errors.append(
                f"mapping {mapping_id} source does not match {evidence_id}: "
                f"{source_id} != {linked.get('source_id')}"
            )
        if row.get("status") != "DRAFT" or row.get("reviewed_by") or row.get("reviewed_at"):
            errors.append(f"mapping {mapping_id} improperly records human review or promotion")
    return errors


def _frontmatter_name(path: Path) -> str | None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return None


def validate_environment(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    environment_path = root / ENVIRONMENT
    data = _load_json(environment_path, errors)
    if not isinstance(data, dict):
        return errors or ["research environment must be a JSON object"]

    review = data.get("review")
    if not isinstance(review, dict) or review.get("mode") != "LIVING-EVIDENCE-MAP":
        errors.append("review.mode must be LIVING-EVIDENCE-MAP")
    if isinstance(review, dict) and review.get("fixedCutoffDate") is not None:
        errors.append("living evidence map must not claim a permanent fixed cutoff date")
    databases = review.get("databases") if isinstance(review, dict) else None
    names = {
        row.get("name")
        for row in databases or []
        if isinstance(row, dict) and isinstance(row.get("name"), str)
    }
    required_databases = {
        "IEEE Xplore",
        "ACM Digital Library",
        "Scopus",
        "Web of Science",
        "Crossref",
        "OpenAlex",
    }
    missing_databases = sorted(required_databases - names)
    if missing_databases:
        errors.append(f"missing declared research databases: {', '.join(missing_databases)}")

    registries = data.get("registries")
    if not isinstance(registries, dict):
        return errors + ["registries must be an object"]
    for key, expected in CSV_CONTRACTS.items():
        relative = registries.get(key)
        if not isinstance(relative, str) or not relative:
            errors.append(f"missing registry path {key}")
            continue
        path = root / relative
        if not path.is_file():
            errors.append(f"missing registry file {relative}")
            continue
        errors.extend(_validate_csv(path, expected, ID_FIELDS[key]))
    errors.extend(_ledger_link_errors(root, registries))

    figure_relative = registries.get("quantitativeFigureManifest")
    if not isinstance(figure_relative, str) or not figure_relative:
        errors.append("missing quantitativeFigureManifest path")
    else:
        figure_data = _load_json(root / figure_relative, errors)
        if isinstance(figure_data, dict) and not isinstance(figure_data.get("figures"), list):
            errors.append("quantitative figure manifest figures must be a list")

    model_figure_relative = registries.get("modelFigureManifest")
    if not isinstance(model_figure_relative, str) or not model_figure_relative:
        errors.append("missing modelFigureManifest path")
    else:
        model_figure_data = _load_json(root / model_figure_relative, errors)
        if isinstance(model_figure_data, dict):
            model_figures = model_figure_data.get("figures")
            if not isinstance(model_figures, list) or len(model_figures) != 9:
                errors.append("model figure manifest must contain nine figures")
            model_script = root / ".agents/skills/cltav-model-figures/scripts/model_drawio.py"
            try:
                spec = importlib.util.spec_from_file_location("cltav_model_drawio_environment", model_script)
                if spec is None or spec.loader is None:
                    raise ImportError("cannot create model-figure validator module")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                errors.extend(f"model figure: {item}" for item in module.validate_package(root))
            except (OSError, ImportError, ValueError) as exc:
                errors.append(f"cannot run model-figure validator: {exc}")

    model_export_relative = registries.get("modelFigureExports")
    if not isinstance(model_export_relative, str) or not model_export_relative:
        errors.append("missing modelFigureExports path")
    elif model_export_relative != "configs/research/cltav_model_figure_exports.json":
        errors.append("modelFigureExports must use the controlled registry path")
    elif not (root / model_export_relative).is_file():
        errors.append(f"missing registry file {model_export_relative}")

    skills = data.get("skills")
    if not isinstance(skills, list) or not skills:
        errors.append("skills must be a nonempty list")
    else:
        for relative in skills:
            if not isinstance(relative, str):
                errors.append("skill path must be a string")
                continue
            path = root / relative
            if not path.is_file():
                errors.append(f"missing skill entrypoint {relative}")
                continue
            name = _frontmatter_name(path)
            if name != path.parent.name:
                errors.append(
                    f"skill name {name!r} does not match folder {path.parent.name!r}"
                )

    human_gates = data.get("humanGates")
    if not isinstance(human_gates, list) or "FINAL-SCIENTIFIC-APPROVAL" not in human_gates:
        errors.append("FINAL-SCIENTIFIC-APPROVAL human gate is required")
    return errors


def tool_report() -> list[str]:
    rows: list[str] = []
    for name, required_for_manuscript in TOOLS:
        candidates = (name, "draw.io") if name == "drawio" else (name,)
        location = None
        for candidate in candidates:
            location = shutil.which(candidate)
            if location:
                break
        if name == "drawio" and location is None:
            windows_app = Path.home() / "AppData/Local/Programs/draw.io/draw.io.exe"
            if windows_app.is_file():
                location = str(windows_app)
        role = "manuscript-required" if required_for_manuscript else "optional-workflow"
        rows.append(f"{name}: {location or 'MISSING'} [{role}]")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tools", action="store_true", help="also report local tool capabilities")
    args = parser.parse_args()
    errors = validate_environment()
    if errors:
        print("Research environment check failed:")
        for item in errors:
            print(f"  - {item}")
        return 1
    print("Research environment check passed")
    if args.tools:
        print("Local tool capabilities:")
        for row in tool_report():
            print(f"  - {row}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
