"""Validate the effective RB-2026-001-v4.2.1 baseline and the v4.3 candidate."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METHODOLOGY_DIR = ROOT / "docs/research/methodology"
REPORT = METHODOLOGY_DIR / "RR-2026-001_test_analysis_conformance_methodology.md"
BASELINE = ROOT / "docs/control/baselines/RB-2026-001-v4.2.1.md"
RELEASE_RECORD = ROOT / "docs/control/baselines/BRR-RB-2026-001-v4.2.1.md"
CURRENT_REPORT_DIR = ROOT / "artifacts/reports/current"
READER_REPORT = CURRENT_REPORT_DIR / "RPT-2026-002_information_architecture_v4.2.1.md"
PR7_GATE = ROOT / "docs/control/gates/GR-PR7-RB-2026-001-v4.2.1.md"
V43_BASELINE = ROOT / "docs/control/baselines/RB-2026-001-v4.3.md"
V43_CR = ROOT / "docs/control/changes/CR-2026-004.md"
V43_CONTRACTS = [
    ROOT / "docs/control/contracts/VERIFICATION_OBJECTIVE.md",
    ROOT / "docs/control/contracts/OBJECTIVE_SATISFACTION_RECORD.md",
    ROOT / "docs/control/contracts/COMPLIANCE_EVIDENCE_INDEX.md",
    ROOT / "docs/control/contracts/TEST_CONFORMITY_RECORD.md",
    ROOT / "docs/control/contracts/PROBLEM_CLOSURE_RECORD.md",
]
V43_LITERATURE = ROOT / "docs/research/methodology/CERTIFICATION_EVIDENCE_BASIS.md"
REFERENCE_CATALOG = ROOT / "docs/research/reference_catalog.yaml"
ZH_MARKER = "\n# 中文版\n"
APPENDED_ZH_RE = re.compile(r"^# 中文版$", re.MULTILINE)

REQUIRED = [
    ROOT / "README.md",
    ROOT / "docs/control/PROJECT_CONTROL.md",
    ROOT / "docs/control/CHANGE_CONTROL.md",
    ROOT / "docs/control/baselines/RB-2026-001-v4.2.md",
    ROOT / "docs/control/baselines/BRR-RB-2026-001-v4.2.md",
    BASELINE,
    RELEASE_RECORD,
    ROOT / "docs/control/contracts/ARCHITECTURE.md",
    ROOT / "docs/control/contracts/DOMAIN_BOUNDARIES.md",
    ROOT / "docs/control/contracts/TERMINOLOGY.md",
    ROOT / "docs/control/contracts/APPLICABILITY_TEMPLATE.md",
    ROOT / "docs/control/contracts/CRS_SCHEMA.md",
    ROOT / "docs/control/contracts/TRACEABILITY_SCHEMA.md",
    ROOT / "docs/control/contracts/REQUIREMENTS_GUIDE.md",
    ROOT / "docs/control/decisions/DESIGN_DECISIONS.md",
    ROOT / "docs/control/gates/GATE_RECORD_TEMPLATE.md",
    ROOT / "docs/control/gates/REVIEW_GUIDELINE.md",
    ROOT / "docs/control/gates/PR6_BASELINE_REVIEW_CHECKLIST.md",
    ROOT / "docs/control/gates/GR-PR6-RB-2026-001-v4.2.md",
    PR7_GATE,
    ROOT / "docs/control/risks/RISK_REGISTER.md",
    ROOT / "docs/control/changes/CR-2026-001.md",
    ROOT / "docs/control/changes/CR-2026-002.md",
    ROOT / "docs/control/changes/CR-2026-003.md",
    V43_CR,
    V43_BASELINE,
    V43_LITERATURE,
    *V43_CONTRACTS,
    REPORT,
    ROOT / "docs/research/RESEARCH_CONTROL.md",
    ROOT / "docs/research/EXPERIMENT_PLAN.md",
    ROOT / "docs/research/CLAIM_EVIDENCE_MATRIX.md",
    METHODOLOGY_DIR / "METHODOLOGY_CATALOG.md",
    ROOT / "docs/research/publication/RESEARCH_OUTLINE.md",
    ROOT / "docs/research/publication/PUBLICATION_GUIDE.md",
    ROOT / "docs/engineering/ENGINEERING_CONTROL.md",
    ROOT / "docs/engineering/design/EVIDENCE_MANIFEST.md",
    ROOT / "docs/engineering/design/DESIGN_GUIDE.md",
    ROOT / "docs/engineering/SCRIPT_CATALOG.md",
    ROOT / "docs/engineering/EXAMPLE_CONFIG_GUIDE.md",
    ROOT / "docs/engineering/increments/IAR_TEMPLATE.md",
    ROOT / "docs/tutorial/TUTORIAL_CONTROL.md",
    ROOT / "docs/tutorial/sources/COMMON_TUTORIAL_PLAN.md",
    ROOT / "docs/tutorial/sources/ARINC615A_TUTORIAL_PLAN.md",
    READER_REPORT,
]

BILINGUAL_EXEMPT = {
    ROOT / "docs/control/gates/GR-PR6-RB-2026-001-v4.2.md",
    PR7_GATE,
}
BILINGUAL = [path for path in REQUIRED if path not in BILINGUAL_EXEMPT]

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
    ROOT / "docs/control/contracts/DOMAIN_BOUNDARIES.md": {
        "Boundary contracts",
        "evidence_manifest_id",
        "gate_record_id",
        "Common Verification Tutorial",
        "ARINC 615A Tutorial",
    },
    ROOT / "docs/control/contracts/ARCHITECTURE.md": {
        "Domain boundaries and traceable dependencies",
        "This controlled feedback is not a direct reverse dependency.",
    },
    ROOT / "docs/tutorial/TUTORIAL_CONTROL.md": {
        "explains_baseline",
        "explains_tool_release",
        "normative: false",
    },
    ROOT / "docs/control/PROJECT_CONTROL.md": {
        "reader release surface",
        "developer control plane",
        "artifacts/reports/current/",
    },
}

REQUIRED_BASELINE_LINKS = {
    ROOT / "docs/control/baselines/RB-2026-001-v4.2.md": {
        "[`docs/research/methodology/RR-2026-001_test_analysis_conformance_methodology.md`](../../research/methodology/RR-2026-001_test_analysis_conformance_methodology.md)",
        "[`docs/control/CHANGE_CONTROL.md`](../CHANGE_CONTROL.md)",
    },
    BASELINE: {
        "[`docs/research/methodology/RR-2026-001_test_analysis_conformance_methodology.md`](../../research/methodology/RR-2026-001_test_analysis_conformance_methodology.md)",
        "[`docs/control/CHANGE_CONTROL.md`](../CHANGE_CONTROL.md)",
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
        if "local-references" in source.parts:
            continue
        if any(part.startswith(".") for part in source.relative_to(ROOT).parts):
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
            try:
                relative_target = target.relative_to(ROOT)
            except ValueError:
                errors.append(
                    f"{source.relative_to(ROOT)} -> {link} "
                    f"(target escapes repository root: {target})"
                )
                continue
            if not target.exists():
                errors.append(
                    f"{source.relative_to(ROOT)} -> {link} "
                    f"(missing {relative_target})"
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

    baseline = read(BASELINE)
    if "RB-2026-001-v4.2.1" not in baseline:
        errors.append(f"{BASELINE.relative_to(ROOT)} does not declare RB-2026-001-v4.2.1")

    root_markdown = sorted(ROOT.glob("*.md"))
    if root_markdown != [ROOT / "README.md"]:
        errors.append(
            "README.md must be the only root Markdown document: "
            + ", ".join(path.name for path in root_markdown)
        )

    nested_readmes = sorted(
        path for path in ROOT.rglob("README.md")
        if path != ROOT / "README.md"
        and "local-references" not in path.parts
        and not any(part.startswith(".") for part in path.relative_to(ROOT).parts)
    )
    for path in nested_readmes:
        errors.append(f"subdirectory README is prohibited: {path.relative_to(ROOT)}")

    current_reader_reports = sorted(CURRENT_REPORT_DIR.glob("*"))
    current_reader_reports = [path for path in current_reader_reports if path.is_file()]
    if current_reader_reports != [READER_REPORT]:
        errors.append(
            "artifacts/reports/current must contain exactly the declared reader report"
        )

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
                f"legacy docs/study artifact still exists; use "
                f"docs/research/methodology or docs/tutorial: {path.relative_to(ROOT)}"
            )

    for path, terms in REQUIRED_ARCHITECTURE_TERMS.items():
        text = read(path)
        for term in terms:
            if term not in text:
                errors.append(
                    f"architecture contract term missing from "
                    f"{path.relative_to(ROOT)}: {term}"
                )

    for path, links in REQUIRED_BASELINE_LINKS.items():
        text = read(path)
        for link in links:
            if link not in text:
                errors.append(
                    f"canonical baseline link missing from {path.relative_to(ROOT)}: "
                    f"{link}"
                )

    manifest_text = read(ROOT / "docs/engineering/design/EVIDENCE_MANIFEST.md")
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
                "verificationObjectiveRefs",
                "testArticleConformityRef",
                "testSetupConformityRef",
                "procedureConformityRef",
                "problemRefs",
                "deviationRefs",
                "tool",
            }
            missing = required_manifest_fields - parsed_manifests[0].keys()
            if missing:
                errors.append(
                    "evidence manifest is missing required fields: "
                    + ", ".join(sorted(missing))
                )
            if parsed_manifests[0].get("manifestVersion") != "1.3":
                errors.append("evidence manifest manifestVersion must be 1.3")
            tool = parsed_manifests[0].get("tool", {})
            if "qualificationStatus" not in tool:
                errors.append("evidence manifest tool block requires qualificationStatus")
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

    if not REFERENCE_CATALOG.exists():
        errors.append("missing optional reference catalog (recommended for v4.3)")

    traceability = read(ROOT / "docs/control/contracts/TRACEABILITY_SCHEMA.md")
    for term in (
        "rho_BR",
        "rho_RO",
        "rho_OM",
        "rho_EO",
        "rho_OC",
        "NOT_INSTANTIATED_IN_PROTOCOL_ONLY_STUDY",
    ):
        if term not in traceability:
            errors.append(f"v4.3 traceability relation missing: {term}")

    claims = read(ROOT / "docs/research/CLAIM_EVIDENCE_MATRIX.md")
    for term in ("A-BASIS", "A-COMP", "A-OBJ", "E-TIME", "R-MUT", "R-XFER"):
        if term not in claims:
            errors.append(f"v4.3 claim-evidence matrix missing claim: {term}")

    v43_baseline_text = read(V43_BASELINE)
    if "RB-2026-001-v4.3" not in v43_baseline_text:
        errors.append("v4.3 baseline does not declare RB-2026-001-v4.3")
    if "certification-oriented does not mean certification-approved" not in v43_baseline_text:
        errors.append("v4.3 baseline is missing a required non-claim")

    v43_cr_text = read(V43_CR)
    if "CR-2026-004" not in v43_cr_text:
        errors.append("CR-2026-004 does not declare CR-2026-004")

    if errors:
        print("Baseline validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "RB-2026-001-v4.2.1 validation passed: "
        f"per-language H2={en_shape[0]}, H3={en_shape[1]}, "
        f"math_blocks={en_shape[2]}, equation_tags=1..14,T1..T5, "
        f"bilingual_docs={len(BILINGUAL)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
