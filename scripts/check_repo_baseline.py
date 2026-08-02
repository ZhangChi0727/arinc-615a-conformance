"""Validate repository documentation against RB-2026-001-v4.2."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METHODOLOGY_DIR = ROOT / "docs/methodology"
REPORT = METHODOLOGY_DIR / "RR-2026-001_test_analysis_conformance_methodology.md"
ZH_MARKER = "\n# 中文版\n"
APPENDED_ZH_RE = re.compile(r"^# 中文版$", re.MULTILINE)

REQUIRED = [
    ROOT / "README.md",
    ROOT / "PROJECT_PLAN.md",
    ROOT / "RESEARCH_OUTLINE.md",
    ROOT / "TRACKS.md",
    ROOT / "docs/BASELINE.md",
    ROOT / "docs/README.md",
    ROOT / "docs/02_thesis_outline.md",
    ROOT / "docs/architecture.md",
    ROOT / "docs/terminology.md",
    REPORT,
    ROOT / "docs/research/RESEARCH_PLAN.md",
    ROOT / "docs/research/EXPERIMENT_PLAN.md",
    ROOT / "docs/research/CLAIM_EVIDENCE_MATRIX.md",
    ROOT / "docs/engineering/IMPLEMENTATION_PLAN.md",
    ROOT / "docs/requirements/CRS_SCHEMA.md",
    ROOT / "docs/requirements/README.md",
    ROOT / "docs/requirements/TRACEABILITY_SCHEMA.md",
    ROOT / "docs/requirements/APPLICABILITY_TEMPLATE.md",
    ROOT / "docs/design/EVIDENCE_MANIFEST.md",
    ROOT / "docs/design/README.md",
    ROOT / "docs/review/REVIEW_GUIDELINE.md",
    ROOT / "docs/review/DESIGN_DECISIONS.md",
    ROOT / "docs/review/GATE_RECORD_TEMPLATE.md",
    ROOT / "docs/review/PR6_BASELINE_REVIEW_CHECKLIST.md",
    ROOT / "docs/management/CHANGE_CONTROL.md",
    ROOT / "docs/management/RISK_REGISTER.md",
    ROOT / "docs/management/changes/CR-2026-001.md",
    ROOT / "docs/management/changes/CR-2026-002.md",
    METHODOLOGY_DIR / "00_INDEX.md",
    ROOT / "thesis/README.md",
    ROOT / "tutorial/README.md",
    ROOT / "tutorial/common/README.md",
    ROOT / "tutorial/arinc615a/README.md",
    ROOT / "scripts/README.md",
]

BILINGUAL = REQUIRED

LEGACY_FILENAMES = {
    "RR-2026-001_test_analysis_conformance_methodology_en.md",
    "RR-2026-001_测试分析符合性验证方法论_zh.md",
    "RR-2026-001_verification_methodology_en.md",
    "RR-2026-001_验证用例生成方法论_zh.md",
}

LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
H2_RE = re.compile(r"^## ", re.MULTILINE)
H3_RE = re.compile(r"^### ", re.MULTILINE)
MATH_OPEN_RE = re.compile(r"^\\\[$", re.MULTILINE)
MATH_CLOSE_RE = re.compile(r"^\\\]$", re.MULTILINE)
NUMERIC_TAG_RE = re.compile(r"\\tag\{(\d+)}")
TIMED_TAG_RE = re.compile(r"\\tag\{(T\d+)}")
FENCE_RE = re.compile(r"^```", re.MULTILINE)
JSON_FENCE_RE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)

REQUIRED_ARCHITECTURE_TERMS = {
    ROOT / "TRACKS.md": {
        "Boundary contracts",
        "evidence_manifest_id",
        "gate_record_id",
        "tutorial/common/",
        "tutorial/arinc615a/",
    },
    ROOT / "docs/architecture.md": {
        "Domain boundaries and traceable dependencies",
        "This controlled feedback is not a direct reverse dependency.",
    },
    ROOT / "tutorial/README.md": {
        "explains_baseline",
        "explains_tool_release",
        "normative: false",
    },
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def document_shape(text: str) -> tuple[int, int, int, int, list[str], list[str], int]:
    return (
        len(H2_RE.findall(text)),
        len(H3_RE.findall(text)),
        len(MATH_OPEN_RE.findall(text)),
        len(MATH_CLOSE_RE.findall(text)),
        NUMERIC_TAG_RE.findall(text),
        TIMED_TAG_RE.findall(text),
        len(FENCE_RE.findall(text)),
    )


def local_link_errors() -> list[str]:
    errors: list[str] = []
    for source in ROOT.rglob("*.md"):
        if ".git" in source.parts or "local-references" in source.parts:
            continue
        text = read(source)
        for match in LINK_RE.finditer(text):
            link = match.group(1).strip().strip("<>")
            if link.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = link.split("#", 1)[0]
            if not path_part:
                continue
            target = (source.parent / path_part).resolve()
            if not target.exists():
                errors.append(
                    f"{source.relative_to(ROOT)} -> {link} "
                    f"(missing {target.relative_to(ROOT)})"
                )
    return errors


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED:
        if not path.exists():
            errors.append(f"missing required baseline file: {path.relative_to(ROOT)}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    baseline = read(ROOT / "docs/BASELINE.md")
    if "RB-2026-001-v4.2" not in baseline:
        errors.append("docs/BASELINE.md does not declare RB-2026-001-v4.2")

    bilingual_shapes: dict[Path, tuple[tuple, tuple]] = {}
    for path in BILINGUAL:
        text = read(path)
        markers = APPENDED_ZH_RE.findall(text)
        if len(markers) != 1 or text.count(ZH_MARKER) != 1:
            errors.append(
                f"key document must contain exactly one H1 '# 中文版' boundary: "
                f"{path.relative_to(ROOT)}"
            )
            en_text, zh_text = text, ""
        else:
            en_text, zh_text = text.split(ZH_MARKER, 1)

        en_document_shape = document_shape(en_text)
        zh_document_shape = document_shape(zh_text)
        bilingual_shapes[path] = (en_document_shape, zh_document_shape)
        if en_document_shape != zh_document_shape:
            errors.append(
                f"EN/ZH controlled structure differs in {path.relative_to(ROOT)}: "
                f"EN={en_document_shape}, ZH={zh_document_shape}"
            )

    en_shape, zh_shape = bilingual_shapes[REPORT]

    expected_numeric = [str(number) for number in range(1, 15)]
    expected_timed = [f"T{number}" for number in range(1, 6)]
    if en_shape[4] != expected_numeric:
        errors.append(f"numeric equation tags are not 1..14: {en_shape[4]}")
    if en_shape[5] != expected_timed:
        errors.append(f"timed equation tags are not T1..T5: {en_shape[5]}")
    if en_shape[2] != en_shape[3]:
        errors.append("English display-math delimiters are unbalanced")
    if zh_shape[2] != zh_shape[3]:
        errors.append("Chinese display-math delimiters are unbalanced")
    if en_shape[6] % 2 or zh_shape[6] % 2:
        errors.append("code fences are unbalanced in one or both report sections")

    required_report_terms = {
        "clock-augmented observable EFSM",
        "measurement-error budget",
        "Robust timing verdict",
        "逻辑序列",
        "测量误差预算",
        "稳健时序判定",
    }
    report = read(REPORT)
    for term in required_report_terms:
        if term not in report:
            errors.append(f"methodology report is missing required v4.2 term: {term}")

    for legacy in LEGACY_FILENAMES:
        if (METHODOLOGY_DIR / legacy).exists():
            errors.append(f"legacy/parallel report filename still exists: {legacy}")

    parallel_reports = list(METHODOLOGY_DIR.glob("RR-2026*_zh.md"))
    for path in parallel_reports:
        errors.append(
            f"parallel Chinese report is prohibited; append it in the source file: "
            f"{path.relative_to(ROOT)}"
        )

    legacy_study_dir = ROOT / "docs/study"
    if legacy_study_dir.exists():
        legacy_study_files = [path for path in legacy_study_dir.rglob("*") if path.is_file()]
        for path in legacy_study_files:
            errors.append(
                f"legacy docs/study artifact still exists; use docs/methodology or "
                f"tutorial/: {path.relative_to(ROOT)}"
            )

    for path, terms in REQUIRED_ARCHITECTURE_TERMS.items():
        text = read(path)
        for term in terms:
            if term not in text:
                errors.append(
                    f"architecture contract term missing from "
                    f"{path.relative_to(ROOT)}: {term}"
                )

    manifest_text = read(ROOT / "docs/design/EVIDENCE_MANIFEST.md")
    manifest_examples = JSON_FENCE_RE.findall(manifest_text)
    if len(manifest_examples) != 2:
        errors.append("evidence manifest must contain exactly two JSON examples")
    else:
        parsed_manifests: list[dict] = []
        for language, example in zip(("English", "Chinese"), manifest_examples):
            try:
                parsed_manifests.append(json.loads(example))
            except json.JSONDecodeError as exc:
                errors.append(f"{language} evidence-manifest JSON is invalid: {exc}")
        if len(parsed_manifests) == 2:
            if parsed_manifests[0] != parsed_manifests[1]:
                errors.append("English/Chinese evidence-manifest examples differ")
            required_manifest_fields = {
                "manifestId",
                "baselineId",
                "sourceCommit",
                "requirementSetId",
                "crsVersion",
                "modelId",
                "modelVersion",
                "verificationCaseSetId",
                "vcsVersion",
                "verificationCaseId",
                "toolVersion",
                "environmentId",
                "upstreamArtifactRefs",
                "executionStatus",
                "clock",
                "rawEvidenceRefs",
                "derivedEvidenceRefs",
                "gateRecordRefs",
                "verdict",
            }
            missing = required_manifest_fields - parsed_manifests[0].keys()
            if missing:
                errors.append(
                    "evidence manifest is missing required fields: "
                    + ", ".join(sorted(missing))
                )
            error_budget = parsed_manifests[0].get("clock", {}).get("errorBudget", {})
            required_budget_fields = {
                "id",
                "version",
                "environmentId",
                "boundNs",
                "combinationRule",
                "commonBiasTreatment",
                "components",
            }
            missing_budget = required_budget_fields - error_budget.keys()
            if missing_budget:
                errors.append(
                    "evidence error budget is missing required fields: "
                    + ", ".join(sorted(missing_budget))
                )

    errors.extend(local_link_errors())

    if errors:
        print("Baseline validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "RB-2026-001-v4.2 validation passed: "
        f"per-language H2={en_shape[0]}, H3={en_shape[1]}, "
        f"math_blocks={en_shape[2]}, equation_tags=1..14,T1..T5, "
        f"bilingual_docs={len(BILINGUAL)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
