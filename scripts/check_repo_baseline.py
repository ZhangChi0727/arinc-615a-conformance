"""Validate the repository baseline against discovered artifacts.

Version-sensitive artifacts (baselines, release records, change requests, gate
records, reader reports) are discovered by directory scan and pattern match,
not by hardcoded file names. Project invariants (root Markdown, equation tags,
bilingual structure, evidence-manifest schema, required terms) are enforced from
named constants so baseline evolution does not require editing this file.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# Directory roots for discovered artifacts.
CONTROL = ROOT / "docs/control"
BASELINES_DIR = CONTROL / "baselines"
CHANGES_DIR = CONTROL / "changes"
GATES_DIR = CONTROL / "gates"
CONTRACTS_DIR = CONTROL / "contracts"
RESEARCH = ROOT / "docs/research"
METHODOLOGY_DIR = RESEARCH / "methodology"
CURRENT_REPORT_DIR = ROOT / "artifacts/reports/current"

# Discovery patterns (version-sensitive artifacts are not hard-coded).
BASELINE_RE = re.compile(r"^RB-\d{4}-\d{3}-v[\d.]+\.md$")
RELEASE_RECORD_RE = re.compile(r"^BRR-RB-\d{4}-\d{3}-v[\d.]+\.md$")
CHANGE_RE = re.compile(r"^CR-\d{4}-\d{3}\.md$")
GATE_RECORD_RE = re.compile(r"^GR-.*\.md$")
READER_REPORT_RE = re.compile(r"^RPT-\d{4}-\d{3}.*\.md$")
METHODOLOGY_REPORT_RE = re.compile(r"^RR-\d{4}-\d{3}.*_.*methodology.*\.md$")

# Fixed invariant anchors.
ZH_MARKER = "\n# 中文版\n"
APPENDED_ZH_RE = re.compile(r"^# 中文版$", re.MULTILINE)
ZH_BOUNDARY_HEADER = "# 中文版"

REPORT_PATH = METHODOLOGY_DIR / "RR-2026-001_test_analysis_conformance_methodology.md"
EVIDENCE_MANIFEST_PATH = ROOT / "docs/engineering/design/EVIDENCE_MANIFEST.md"
TRACEABILITY_PATH = CONTRACTS_DIR / "TRACEABILITY_SCHEMA.md"
CLAIMS_PATH = RESEARCH / "CLAIM_EVIDENCE_MATRIX.md"
REFERENCE_CATALOG_PATH = RESEARCH / "reference_catalog.yaml"

# Structural invariant directories (content checked by presence, not version).
REQUIRED_FIXED_FILES = [
    ROOT / "README.md",
    CONTROL / "PROJECT_CONTROL.md",
    CONTROL / "CHANGE_CONTROL.md",
    CONTRACTS_DIR / "ARCHITECTURE.md",
    CONTRACTS_DIR / "DOMAIN_BOUNDARIES.md",
    CONTRACTS_DIR / "TERMINOLOGY.md",
    CONTRACTS_DIR / "APPLICABILITY_TEMPLATE.md",
    CONTRACTS_DIR / "CRS_SCHEMA.md",
    CONTRACTS_DIR / "TRACEABILITY_SCHEMA.md",
    CONTRACTS_DIR / "REQUIREMENTS_GUIDE.md",
    CONTROL / "decisions" / "DESIGN_DECISIONS.md",
    GATES_DIR / "GATE_RECORD_TEMPLATE.md",
    GATES_DIR / "REVIEW_GUIDELINE.md",
    GATES_DIR / "PR6_BASELINE_REVIEW_CHECKLIST.md",
    CONTROL / "risks" / "RISK_REGISTER.md",
    RESEARCH / "RESEARCH_CONTROL.md",
    RESEARCH / "EXPERIMENT_PLAN.md",
    RESEARCH / "CLAIM_EVIDENCE_MATRIX.md",
    METHODOLOGY_DIR / "METHODOLOGY_CATALOG.md",
    RESEARCH / "publication" / "RESEARCH_OUTLINE.md",
    RESEARCH / "publication" / "PUBLICATION_GUIDE.md",
    ROOT / "docs/engineering/ENGINEERING_CONTROL.md",
    ROOT / "docs/engineering/design/EVIDENCE_MANIFEST.md",
    ROOT / "docs/engineering/design/DESIGN_GUIDE.md",
    ROOT / "docs/engineering/SCRIPT_CATALOG.md",
    ROOT / "docs/engineering/EXAMPLE_CONFIG_GUIDE.md",
    ROOT / "docs/engineering/increments/IAR_TEMPLATE.md",
    ROOT / "docs/tutorial/TUTORIAL_CONTROL.md",
    ROOT / "docs/tutorial/sources/COMMON_TUTORIAL_PLAN.md",
    ROOT / "docs/tutorial/sources/ARINC615A_TUTORIAL_PLAN.md",
    REPORT_PATH,
]

# Bilingual exemption: gate records are historical control artifacts that may
# remain monolingual; discovered dynamically.
BILINGUAL_EXEMPT_RE = re.compile(r"^GR-PR\d+-.*\.md$")

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

# Mathematical invariants of the methodology report.
NUMERIC_EQUATION_RANGE = range(1, 15)
TIMED_EQUATION_RANGE = range(1, 6)

REQUIRED_ARCHITECTURE_TERMS = {
    CONTRACTS_DIR / "DOMAIN_BOUNDARIES.md": {
        "Boundary contracts",
        "evidence_manifest_id",
        "gate_record_id",
        "Common Verification Tutorial",
        "ARINC 615A Tutorial",
    },
    CONTRACTS_DIR / "ARCHITECTURE.md": {
        "Domain boundaries and traceable dependencies",
        "This controlled feedback is not a direct reverse dependency.",
    },
    ROOT / "docs/tutorial/TUTORIAL_CONTROL.md": {
        "explains_baseline",
        "explains_tool_release",
        "normative: false",
    },
    CONTROL / "PROJECT_CONTROL.md": {
        "reader release surface",
        "developer control plane",
        "artifacts/reports/current/",
    },
}

REQUIRED_REPORT_TERMS = {
    "clock-augmented observable EFSM",
    "measurement-error budget",
    "Robust timing verdict",
    "逻辑序列",
    "测量误差预算",
    "稳健时序判定",
}

EVIDENCE_MANIFEST_REQUIRED_FIELDS = {
    "manifestId", "baselineId", "sourceCommit", "requirementSetId",
    "crsVersion", "modelId", "modelVersion", "verificationCaseSetId",
    "vcsVersion", "verificationCaseId", "toolVersion", "environmentId",
    "upstreamArtifactRefs", "executionStatus", "clock", "rawEvidenceRefs",
    "derivedEvidenceRefs", "gateRecordRefs", "verdict",
    "verificationObjectiveRefs", "testArticleConformityRef",
    "testSetupConformityRef", "procedureConformityRef",
    "problemRefs", "deviationRefs", "tool",
}
EVIDENCE_MANIFEST_VERSION = "1.3"
EVIDENCE_BUDGET_REQUIRED_FIELDS = {
    "id", "version", "environmentId", "boundNs",
    "combinationRule", "commonBiasTreatment", "components",
}

# v4.3 architecture anchors discovered by content, not path.
REQUIRED_V43_TRACEABILITY_TERMS = (
    "rho_BR", "rho_RO", "rho_OM", "rho_EO", "rho_OC",
    "NOT_INSTANTIATED_IN_PROTOCOL_ONLY_STUDY",
)
REQUIRED_V43_CLAIMS = ("A-BASIS", "A-COMP", "A-OBJ", "E-TIME", "R-MUT", "R-XFER")
V43_BASELINE_PREFIX = "RB-2026-001-v4.3"
V43_NONCLAIM_PHRASE = "certification-oriented does not mean certification-approved"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def discover(pattern: re.Pattern[str], directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted(path for path in directory.iterdir() if pattern.match(path.name))


def discover_exactly_one(pattern: re.PathLike, directory: Path, label: str, errors: list[str]) -> Path | None:
    matches = discover(pattern, directory)
    if len(matches) != 1:
        errors.append(
            f"{label}: expected exactly one match in {directory.relative_to(ROOT)}, "
            f"found {len(matches)}"
        )
        return None
    return matches[0]


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


def collect_required(errors: list[str]) -> tuple[list[Path], Path | None, Path | None, list[Path]]:
    """Build the required-file list from fixed files plus discovered artifacts."""
    required = list(REQUIRED_FIXED_FILES)
    discovered_baseline = None
    reader_report = None

    for baseline in discover(BASELINE_RE, BASELINES_DIR):
        required.append(baseline)
    for release in discover(RELEASE_RECORD_RE, BASELINES_DIR):
        required.append(release)
    for change in discover(CHANGE_RE, CHANGES_DIR):
        required.append(change)
    for gate in discover(GATE_RECORD_RE, GATES_DIR):
        required.append(gate)

    reader_report = discover_exactly_one(
        re.compile(r"^.*\.md$"), CURRENT_REPORT_DIR,
        "reader report", errors,
    )
    if reader_report is not None:
        required.append(reader_report)

    return required, None, reader_report, []


def main() -> int:
    errors: list[str] = []

    required, _, reader_report, _ = collect_required(errors)

    for path in required:
        if not path.exists():
            errors.append(f"missing required baseline file: {path.relative_to(ROOT)}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    baselines = discover(BASELINE_RE, BASELINES_DIR)
    if baselines:
        latest_text = read(baselines[-1])
        latest_id = baselines[-1].stem
        if latest_id not in latest_text:
            errors.append(
                f"{baselines[-1].relative_to(ROOT)} does not declare {latest_id}"
            )

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

    current_files = sorted(
        path for path in CURRENT_REPORT_DIR.glob("*") if path.is_file()
    )
    if reader_report is None:
        pass
    elif current_files != [reader_report]:
        errors.append(
            "artifacts/reports/current must contain exactly the declared reader report"
        )

    bilingual = [path for path in required if not BILINGUAL_EXEMPT_RE.match(path.name)]
    bilingual_shapes: dict[Path, tuple[tuple, tuple]] = {}
    for path in bilingual:
        text = read(path)
        markers = APPENDED_ZH_RE.findall(text)
        if len(markers) != 1 or text.count(ZH_MARKER) != 1:
            errors.append(
                f"key document must contain exactly one H1 '{ZH_BOUNDARY_HEADER}' boundary: "
                f"{path.relative_to(ROOT)}"
            )
            en_text, zh_text = text, ""
        else:
            en_text, zh_text = text.split(ZH_MARKER, 1)

        en_shape = document_shape(en_text)
        zh_shape = document_shape(zh_text)
        bilingual_shapes[path] = (en_shape, zh_shape)
        if en_shape != zh_shape:
            errors.append(
                f"EN/ZH controlled structure differs in {path.relative_to(ROOT)}: "
                f"EN={en_shape}, ZH={zh_shape}"
            )

    if REPORT_PATH in bilingual_shapes:
        en_shape, zh_shape = bilingual_shapes[REPORT_PATH]
        expected_numeric = [str(n) for n in NUMERIC_EQUATION_RANGE]
        expected_timed = [f"T{n}" for n in TIMED_EQUATION_RANGE]
        if en_shape[4] != expected_numeric:
            errors.append(f"numeric equation tags are not {expected_numeric[0]}..{expected_numeric[-1]}: {en_shape[4]}")
        if en_shape[5] != expected_timed:
            errors.append(f"timed equation tags are not {expected_timed[0]}..{expected_timed[-1]}: {en_shape[5]}")
        if en_shape[2] != en_shape[3]:
            errors.append("English display-math delimiters are unbalanced")
        if zh_shape[2] != zh_shape[3]:
            errors.append("Chinese display-math delimiters are unbalanced")
        if en_shape[6] % 2 or zh_shape[6] % 2:
            errors.append("code fences are unbalanced in one or both report sections")

    report_text = read(REPORT_PATH)
    for term in REQUIRED_REPORT_TERMS:
        if term not in report_text:
            errors.append(f"methodology report is missing required term: {term}")

    for legacy in LEGACY_FILENAMES:
        if (METHODOLOGY_DIR / legacy).exists():
            errors.append(f"legacy/parallel report filename still exists: {legacy}")

    for path in METHODOLOGY_DIR.glob("RR-2026*_zh.md"):
        errors.append(
            f"parallel Chinese report is prohibited; append it in the source file: "
            f"{path.relative_to(ROOT)}"
        )

    legacy_study_dir = ROOT / "docs/study"
    if legacy_study_dir.exists():
        for path in legacy_study_dir.rglob("*"):
            if path.is_file():
                errors.append(
                    f"legacy docs/study artifact still exists; use "
                    f"docs/research/methodology or docs/tutorial: {path.relative_to(ROOT)}"
                )

    for path, terms in REQUIRED_ARCHITECTURE_TERMS.items():
        if not path.exists():
            errors.append(f"architecture contract missing: {path.relative_to(ROOT)}")
            continue
        text = read(path)
        for term in terms:
            if term not in text:
                errors.append(
                    f"architecture contract term missing from "
                    f"{path.relative_to(ROOT)}: {term}"
                )

    for baseline in discover(BASELINE_RE, BASELINES_DIR):
        if not baseline.exists():
            continue
        text = read(baseline)
        if "[`docs/research/methodology/RR-2026-001_test_analysis_conformance_methodology.md`](../../research/methodology/RR-2026-001_test_analysis_conformance_methodology.md)" not in text:
            errors.append(f"baseline missing methodology link: {baseline.relative_to(ROOT)}")
        if "[`docs/control/CHANGE_CONTROL.md`](../CHANGE_CONTROL.md)" not in text:
            errors.append(f"baseline missing change-control link: {baseline.relative_to(ROOT)}")

    manifest_text = read(EVIDENCE_MANIFEST_PATH)
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
            missing = EVIDENCE_MANIFEST_REQUIRED_FIELDS - parsed_manifests[0].keys()
            if missing:
                errors.append(
                    "evidence manifest is missing required fields: "
                    + ", ".join(sorted(missing))
                )
            if parsed_manifests[0].get("manifestVersion") != EVIDENCE_MANIFEST_VERSION:
                errors.append(
                    f"evidence manifest manifestVersion must be {EVIDENCE_MANIFEST_VERSION}"
                )
            tool = parsed_manifests[0].get("tool", {})
            if "qualificationStatus" not in tool:
                errors.append("evidence manifest tool block requires qualificationStatus")
            error_budget = parsed_manifests[0].get("clock", {}).get("errorBudget", {})
            missing_budget = EVIDENCE_BUDGET_REQUIRED_FIELDS - error_budget.keys()
            if missing_budget:
                errors.append(
                    "evidence error budget is missing required fields: "
                    + ", ".join(sorted(missing_budget))
                )

    errors.extend(local_link_errors())

    if not REFERENCE_CATALOG_PATH.exists():
        errors.append("missing optional reference catalog (recommended for v4.3)")

    traceability = read(TRACEABILITY_PATH)
    for term in REQUIRED_V43_TRACEABILITY_TERMS:
        if term not in traceability:
            errors.append(f"v4.3 traceability relation missing: {term}")

    claims = read(CLAIMS_PATH)
    for term in REQUIRED_V43_CLAIMS:
        if term not in claims:
            errors.append(f"v4.3 claim-evidence matrix missing claim: {term}")

    v43_baselines = [b for b in discover(BASELINE_RE, BASELINES_DIR)
                     if b.name.startswith("RB-2026-001-v4.3")]
    if not v43_baselines:
        errors.append("v4.3 candidate baseline missing")
    else:
        v43_text = read(v43_baselines[0])
        if V43_BASELINE_PREFIX not in v43_text:
            errors.append("v4.3 baseline does not declare RB-2026-001-v4.3")
        if V43_NONCLAIM_PHRASE not in v43_text:
            errors.append("v4.3 baseline is missing a required non-claim")

    cr_files = discover(CHANGE_RE, CHANGES_DIR)
    cr_prefixes = {f.stem for f in cr_files}
    if "CR-2026-004" not in cr_prefixes:
        errors.append("CR-2026-004 not found among discovered change requests")

    if errors:
        print("Baseline validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Repository baseline validation passed: "
        f"baselines={len(discover(BASELINE_RE, BASELINES_DIR))}, "
        f"changes={len(cr_files)}, "
        f"gates={len(discover(GATE_RECORD_RE, GATES_DIR))}, "
        f"equation_tags=1..{max(NUMERIC_EQUATION_RANGE)},T1..T{max(TIMED_EQUATION_RANGE)}, "
        f"bilingual_docs={len(bilingual)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())