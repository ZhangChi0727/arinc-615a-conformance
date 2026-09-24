"""Validate the repository baseline against discovered artifacts.

Version-sensitive artifacts (baselines, release records, change requests, gate
records, reader reports) are discovered by directory scan and pattern match,
not by hardcoded file names. Project invariants (root Markdown, equation tags,
bilingual structure, evidence-manifest schema, required terms) are enforced from
named constants so baseline evolution does not require editing this file.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath, PureWindowsPath


ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "project-status.json"

SYNC_SPEC = importlib.util.spec_from_file_location(
    "sync_project_overview", ROOT / "scripts/sync_project_overview.py"
)
assert SYNC_SPEC and SYNC_SPEC.loader
sync = importlib.util.module_from_spec(SYNC_SPEC)
SYNC_SPEC.loader.exec_module(sync)
M1_SYNC_SPEC = importlib.util.spec_from_file_location(
    "sync_m1_crs", ROOT / "scripts/sync_m1_crs.py"
)
assert M1_SYNC_SPEC and M1_SYNC_SPEC.loader
m1_sync = importlib.util.module_from_spec(M1_SYNC_SPEC)
M1_SYNC_SPEC.loader.exec_module(m1_sync)
M2_SYNC_SPEC = importlib.util.spec_from_file_location(
    "sync_m2_model", ROOT / "scripts/sync_m2_model.py"
)
assert M2_SYNC_SPEC and M2_SYNC_SPEC.loader
m2_sync = importlib.util.module_from_spec(M2_SYNC_SPEC)
M2_SYNC_SPEC.loader.exec_module(m2_sync)
STATUS = sync.load_status(STATUS_PATH)
SOURCE_REGISTER_PATH = ROOT / STATUS["technicalDirection"]["sourceRegisterPath"]
CONTROLLED_SOURCES = sync.load_source_register(SOURCE_REGISTER_PATH)
ACQUISITION_RECORD_PATH = ROOT / CONTROLLED_SOURCES["acquisitionRecordPath"]
ACQUISITION_RECORD = json.loads(ACQUISITION_RECORD_PATH.read_text(encoding="utf-8"))

# Directory roots for discovered artifacts.
CONTROL = ROOT / "docs/control"
BASELINES_DIR = CONTROL / "baselines"
CHANGES_DIR = CONTROL / "changes"
GATES_DIR = CONTROL / "gates"
CONTRACTS_DIR = CONTROL / "contracts"
RESEARCH = ROOT / "docs/research"
METHODOLOGY_DIR = RESEARCH / "methodology"

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
METHOD_MATH_IDENTITY_PATH = METHODOLOGY_DIR / "rr_2026_001_revision_identity.json"
SOURCE_AUDIT_PATH = ROOT / "configs/research/cltav_protocol_source_audit.json"
CLTAV_PUML_DIR = RESEARCH / "publication" / "models"
CLTAV_ALGORITHM_DIR = RESEARCH / "publication" / "algorithms"
CLTAV_ALGORITHM_FILES = {
    "ALG-CLTAV-01": "ALG-CLTAV-01.tex",
    "ALG-CLTAV-05": "ALG-CLTAV-05-selection.tex",
    "ALG-CLTAV-06": "ALG-CLTAV-06-timing.tex",
    "ALG-CLTAV-07": "ALG-CLTAV-07-history.tex",
    "ALG-CLTAV-02": "ALG-CLTAV-02.tex",
    "ALG-CLTAV-03": "ALG-CLTAV-03.tex",
    "ALG-CLTAV-04": "ALG-CLTAV-04.tex",
    "ALG-CLTAV-APPENDIX": "CLTAV_ALGORITHM_APPENDIX.tex",
}
CLTAV_PUML_FILES = (
    "FIG-CL-TAV-01-context.puml",
    "FIG-CL-TAV-02-requirement-layers.puml",
    "FIG-CL-TAV-03-bdd.puml",
    "FIG-CL-TAV-04-ibd.puml",
    "FIG-CL-TAV-05-closed-loop-activity.puml",
    "FIG-CL-TAV-06-diagnostic-sequence.puml",
    "FIG-CL-TAV-07-two-state-machines.puml",
    "FIG-CL-TAV-08-parametric.puml",
    "FIG-CL-TAV-09-experiment-architecture.puml",
)
CLTAV_SVG_DIR = ROOT / "artifacts/publications/cltav/figures"
CLTAV_SVG_FILES = tuple(name.replace(".puml", ".svg") for name in CLTAV_PUML_FILES)
AUDIT_STATUS_GENERATION = {
    "AUDIT-BEFORE-REQUIREMENT-GENERATION": False,
    "SOURCE-UNIT-AUDIT-IN-PROGRESS": False,
    "PARTIAL-CRS-GENERATION-IN-PROGRESS": True,
    "AUDIT-COMPLETE-REQUIREMENT-GENERATION-ALLOWED": True,
}
DEFERRED_AUDIT_CODES = (
    "DEFERRED-FIND-M9",
    "DEFERRED-DOWNLOAD-M9",
    "DEFERRED-AFDX-DEPLOYMENT-M2-INFRASTRUCTURE-BINDING",
)
AUDIT_UNIT_FIELDS = (
    "id",
    "sourceUnitId",
    "clause",
    "tableOrFigure",
    "documentPage",
    "pdfPage",
    "fragmentKind",
    "fragmentOrdinal",
    "applicabilityDecision",
    "requirementIds",
)
SOURCE_REREAD_APPLICABILITY = (
    "APPLICABLE",
    "CONDITIONALLY-APPLICABLE",
    "JUSTIFIED-NOT-APPLICABLE",
    "NON-NORMATIVE",
    "SOURCE-BLOCKED",
)
SOURCE_REREAD_DOWNLOAD_MODES = (
    "MEDIA-DEFINED",
    "OPERATOR-DEFINED",
    "SHARED",
    "MEDIA-ORGANIZATION",
)
AFDX_RATIONALE = "DEFERRED-AFDX-DEPLOYMENT-M2-INFRASTRUCTURE-BINDING"
AFDX_UNCONDITIONAL_APPLICABILITY = "APPLICABLE"
SOURCE_REREAD_UNIT_FIELDS = (
    "id",
    "sourceUnitId",
    "clause",
    "pdfPage",
    "frozenSourceModality",
    "frozenConformanceEffect",
    "frozenApplicabilityDecision",
    "frozenRationaleCode",
    "candidateApplicability",
    "candidateConformanceEffect",
    "actor",
    "condition",
    "action",
    "objects",
    "notes",
)
SYSML_NOTATION_MARK = "SysML 1.6 notation-based views; executable/metamodel conformance is not claimed"
EVIDENCE_MANIFEST_PATH = ROOT / "docs/engineering/design/EVIDENCE_MANIFEST.md"
TRACEABILITY_PATH = CONTRACTS_DIR / "TRACEABILITY_SCHEMA.md"
CLAIMS_PATH = RESEARCH / "CLAIM_EVIDENCE_MATRIX.md"
REFERENCE_CATALOG_PATH = RESEARCH / "reference_catalog.yaml"
EXTERNAL_BINDING_PATH = CONTRACTS_DIR / "EXTERNAL_GVS_BINDING.md"
INSTANCE_MAPPING_PATH = CONTRACTS_DIR / "GVS_INSTANCE_MAPPING.md"
PROFILE_BINDING_PATH = CONTRACTS_DIR / "ARINC615A_PROFILE_BINDING_CONFIGURATION.md"
MIGRATION_HANDOFF_PATH = ROOT / STATUS["release"]["records"]["migrationReviewPath"]
ACK_HANDOFF_PATH = ROOT / STATUS["release"]["records"]["acknowledgementReviewPath"]
ARCHIVED_READER_REPORT_PATH = ROOT / STATUS["release"]["records"]["historicalReaderReportPath"]

# Structural invariant directories (content checked by presence, not version).
REQUIRED_FIXED_FILES = [
    ROOT / "README.md",
    STATUS_PATH,
    SOURCE_REGISTER_PATH,
    ACQUISITION_RECORD_PATH,
    ROOT / "scripts/sync_project_overview.py",
    ROOT / "scripts/sync_m1_crs.py",
    ROOT / "scripts/sync_m2_model.py",
    ROOT / "configs/requirements/m1_crs_package.schema.json",
    ROOT / "configs/requirements/arinc_615a3_m1_crs.json",
    CONTROL / "requirements" / "ARINC615A3_M1_CRS_REVIEW_VIEW.md",
    ROOT / "configs/models/m2_model_package.schema.json",
    ROOT / "configs/models/arinc_615a3_m2_model.json",
    CONTROL / "models" / "ARINC615A3_M2_MODEL_REVIEW_VIEW.md",
    CONTROL / "PROJECT_CONTROL.md",
    CONTROL / "CHANGE_CONTROL.md",
    CONTRACTS_DIR / "ARCHITECTURE.md",
    CONTRACTS_DIR / "DOMAIN_BOUNDARIES.md",
    CONTRACTS_DIR / "TERMINOLOGY.md",
    CONTRACTS_DIR / "APPLICABILITY_TEMPLATE.md",
    CONTRACTS_DIR / "CRS_SCHEMA.md",
    CONTRACTS_DIR / "MODEL_SCHEMA.md",
    CONTRACTS_DIR / "TRACEABILITY_SCHEMA.md",
    CONTRACTS_DIR / "REQUIREMENTS_GUIDE.md",
    EXTERNAL_BINDING_PATH,
    INSTANCE_MAPPING_PATH,
    PROFILE_BINDING_PATH,
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
    ROOT / "artifacts/publications/cltav/CLTAV_RESEARCH_PLAN.md",
    ROOT / "configs/research/cltav_protocol_source_audit.json",
    ROOT / "configs/research/cltav_interface_registry.json",
    ROOT / "configs/research/cltav_figure_graphs.json",
    ROOT / "configs/research/cltav_owned_generated_artifacts.json",
    ROOT / "artifacts/publications/cltav/ALG-CLTAV-01.pdf",
    ROOT / "scripts/cltav_loop_spec.py",
    *[CLTAV_PUML_DIR / name for name in CLTAV_PUML_FILES],
    *[CLTAV_SVG_DIR / name for name in CLTAV_SVG_FILES],
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
    METHODOLOGY_DIR / "rr_2026_001_revision_identity.json",
    ARCHIVED_READER_REPORT_PATH,
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
CODE_FENCE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`]+`")
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
        "CL-TAV two machines and SysML views",
    },
    ROOT / "docs/tutorial/TUTORIAL_CONTROL.md": {
        "explains_baseline",
        "explains_tool_release",
        "normative: false",
    },
    CONTROL / "PROJECT_CONTROL.md": {
        "sole human-readable current-status surface",
        "atomic records",
        "Every pull request updates both",
    },
    CONTROL / "CHANGE_CONTROL.md": {
        "Changes to standard interpretation, applicability, mathematical/timing or",
        "ownership or migration semantics are baseline changes requiring independent",
        "对标准解释、适用性、数学／时序或 oracle／verdict 语义",
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

# STABLE_INVARIANT: profile traceability and claim vocabulary.
REQUIRED_V43_TRACEABILITY_TERMS = (
    "rho_BR", "rho_RO", "rho_OM", "rho_EO", "rho_OC",
    "NOT_INSTANTIATED_IN_PROTOCOL_ONLY_STUDY",
)
REQUIRED_V43_CLAIMS = ("A-BASIS", "A-COMP", "A-OBJ", "E-TIME", "R-MUT", "R-XFER")
V43_BASELINE_PREFIX = STATUS["release"]["assessedSource"]["baselineId"]
V43_NONCLAIM_PHRASE = "certification-oriented does not mean certification-approved"

# Lifecycle identities are governed data. No current SHA, tag, PR or branch is
# duplicated in executable code.
METHOD_DEFINITION_COMMIT = STATUS["methodInputs"]["methodDefinition"]["commit"]
METHOD_DISPOSITION_COMMIT = STATUS["methodInputs"]["compatibilityDisposition"]["commit"]
METHOD_APPROVED_HEAD = STATUS["release"]["historicalProvenance"]["methodApprovedHead"]
ARINC_V43_RELEASE_COMMIT = STATUS["release"]["assessedSource"]["commit"]
ARINC_V43_RELEASE_TAG = STATUS["release"]["assessedSource"]["tag"]
ACK_BASELINE_ID = STATUS["release"]["currentBaselineId"]
ACK_DISPOSITION = STATUS["methodInputs"]["compatibilityDisposition"]["status"]
CONFIGURATION_STATUS = STATUS["claimsBoundary"]["projectConfigurationStatus"]
EVALUATION_STATUS = STATUS["claimsBoundary"]["instanceEvaluation"]
RQ8_STATUS = STATUS["claimsBoundary"]["rq8"]
ACK_QUALIFICATION_IDS = {f"Q-{number:02d}" for number in range(1, 10)}
ACK_BASELINE_PATH = ROOT / STATUS["release"]["records"]["baselinePath"]
ACK_CHANGE_PATH = ROOT / STATUS["release"]["records"]["changePath"]
ASSESSED_BASELINE_PATH = ROOT / STATUS["release"]["assessedSource"]["baselinePath"]
ASSESSED_CHANGE_PATH = ROOT / STATUS["release"]["assessedSource"]["changePath"]
LEGACY_RELEASE_TAG = STATUS["release"]["historicalProvenance"]["legacyReleaseTag"]
LEGACY_RELEASE_COMMIT = STATUS["release"]["historicalProvenance"]["legacyReleaseCommit"]
CONTROL_STATE_COMMIT = STATUS["release"]["historicalProvenance"]["controlStateCommit"]
PR9_STARTING_HEAD = STATUS["release"]["historicalProvenance"]["migrationStartingHead"]
ALLOWED_MAPPING_STATUSES = {
    "NOT-DETERMINED", "CANDIDATE", "PARTIAL", "CONFLICT", "OUT-OF-SCOPE",
}
METHOD_MAPPING_EXPECTED = {
    # STABLE_INVARIANT: external role, ARINC object, relation and status.
    "R01": ("Applicability/Profile Declaration", "PICS-like declaration", "realizes", "CANDIDATE"),
    "R02": ("VerificationBasisElement", "applicable CRS item", "candidate-correspondence", "CANDIDATE"),
    "R03": ("VerificationObligation", "current ARINC requirement-obligation aspect", "no-direct-correspondence", "NOT-DETERMINED"),
    "R04": ("VerificationObligation", "Verification Objective", "candidate-correspondence", "NOT-DETERMINED"),
    "R05": ("Obligation/Coverage aspect", "functional/state/timing and related classifications", "classifies", "CANDIDATE"),
    "R06": ("VerificationStrategy", "Test-and-Analysis allocation", "realizes", "PARTIAL"),
    "R07": ("VerificationCase", "VC", "instantiates", "CANDIDATE"),
    "R08": ("VerificationProcedure", "procedure", "instantiates", "CANDIDATE"),
    "R09": ("Observation", "packet trace/timestamp/log", "instantiates", "CANDIDATE"),
    "R10": ("Result", "verdict", "instantiates", "CANDIDATE"),
    "R11": ("Oracle", "discrete/robust timing rule", "implements", "CANDIDATE"),
    "R12": ("Evidence", "characterized execution/analysis record", "candidate-correspondence", "NOT-DETERMINED"),
    "R13": ("Argument", "scoped assurance reasoning", "realizes", "PARTIAL"),
    "R14": ("Claim", "CEI claim entry candidate", "indexes", "NOT-DETERMINED"),
    "R15": ("CompositeGate", "RG/G gate package", "specializes", "NOT-DETERMINED"),
    "R16": ("Configuration", "IUT/setup/procedure identity", "instantiates", "CANDIDATE"),
    "R17": ("Anomaly/Change/Impact", "Problem Closure plus CR/DD", "candidate-correspondence", "NOT-DETERMINED"),
    "R18": ("SufficiencyAssessment", "OSR/claim-review candidate", "candidate-correspondence", "NOT-DETERMINED"),
}
INSTANCE_ADDITIONAL_EXPECTED = {
    "A01": ("VerificationCase", "Test Purpose"),
    "A02": ("Evidence", "Execution Evidence Manifest"),
    "A03": ("Configuration", "Test Conformity Record"),
    "A04": ("Argument", "L0–L7 ARINC evidence view"),
    "A05": ("SufficiencyAssessment", "A0–A4 ARINC assurance states"),
    "A06": ("SufficiencyAssessment", "R0–R5 instance research maturity"),
    "A07": ("Configuration", "future Project Configuration `TMP-PC-ARINC615A-01`"),
}
EXTERNAL_ROLE_LOCATORS = {row[0] for row in METHOD_MAPPING_EXPECTED.values()}
ACCEPTANCE_IDS = {f"AC-{number:02d}" for number in range(1, 13)}
METHOD_MATH_IDENTITY_PATH = METHODOLOGY_DIR / "rr_2026_001_revision_identity.json"


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


def _markdown_code_ranges(text: str) -> list[tuple[int, int]]:
    ranges = [(match.start(), match.end()) for match in CODE_FENCE_BLOCK_RE.finditer(text)]
    covered = list(ranges)
    for match in INLINE_CODE_RE.finditer(text):
        start, end = match.start(), match.end()
        if any(lo <= start < hi for lo, hi in covered):
            continue
        ranges.append((start, end))
    return ranges


def _inside_range(index: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start <= index < end for start, end in ranges)


def local_link_errors() -> list[str]:
    errors: list[str] = []
    for source in ROOT.rglob("*.md"):
        if "local-references" in source.parts:
            continue
        if any(part.startswith(".") for part in source.relative_to(ROOT).parts):
            continue
        text = read(source)
        skip = _markdown_code_ranges(text)
        for match in LINK_RE.finditer(text):
            if _inside_range(match.start(), skip):
                continue
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

    for baseline in discover(BASELINE_RE, BASELINES_DIR):
        required.append(baseline)
    for release in discover(RELEASE_RECORD_RE, BASELINES_DIR):
        required.append(release)
    for change in discover(CHANGE_RE, CHANGES_DIR):
        required.append(change)
    for gate in discover(GATE_RECORD_RE, GATES_DIR):
        required.append(gate)

    return required, None, None, []


def display_math_fingerprint(text: str) -> tuple[int, str]:
    blocks = re.findall(r"(?ms)^\\\[$.*?^\\\]$", text)
    payload = "\n".join(blocks).encode("utf-8")
    return len(blocks), hashlib.sha256(payload).hexdigest()


def git_show_file(commit: str, rel_path: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"{commit}:{rel_path.replace(chr(92), '/')}"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.decode("utf-8")


def load_method_math_identity() -> dict:
    return json.loads(METHOD_MATH_IDENTITY_PATH.read_text(encoding="utf-8"))


def historical_methodology_math_errors() -> list[str]:
    """Historical commit objects keep the frozen math identity; the worktree successor does not."""
    errors: list[str] = []
    try:
        identity = load_method_math_identity()
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load methodology math identity: {exc}"]
    freeze = identity.get("historicalFreeze") or {}
    report_path = identity.get("reportPath")
    commit = freeze.get("commit")
    if not isinstance(report_path, str) or not isinstance(commit, str):
        return ["methodology math identity is missing reportPath or historicalFreeze.commit"]
    text = git_show_file(commit, report_path)
    if text is None:
        return [f"cannot read historical methodology object {commit}:{report_path}"]
    count, digest = display_math_fingerprint(text)
    if count != freeze.get("displayMathBlocks") or digest != freeze.get("displayMathSha256"):
        errors.append(
            "historical methodology display mathematics drifted from the recorded freeze identity: "
            f"blocks={count}, sha256={digest}"
        )
    successor = identity.get("successor") or {}
    if successor.get("independentMathematicalApproval") is True:
        errors.append("successor methodology identity must not self-assert independent mathematical approval")
    if successor.get("independentReviewApproval") is True:
        errors.append("successor methodology identity must not self-assert independent review approval")
    if successor.get("historicalMathCheckDoesNotProveSuccessorMath") is not True:
        errors.append("successor identity must state that the historical math check does not prove successor mathematics")
    return errors


def _audit_locator_from_crs(row: dict) -> dict:
    source = row.get("source") or {}
    return {
        "id": row.get("id"),
        "sourceUnitId": row.get("sourceUnitId"),
        "clause": source.get("clause"),
        "tableOrFigure": source.get("tableOrFigure"),
        "documentPage": source.get("documentPage"),
        "pdfPage": source.get("pdfPage"),
        "fragmentKind": source.get("fragmentKind"),
        "fragmentOrdinal": source.get("fragmentOrdinal"),
        "applicabilityDecision": row.get("applicabilityDecision"),
        "requirementIds": list(row.get("requirementIds") or []),
    }


def _expected_clause_groups(units: list[dict]) -> list[dict]:
    groups: dict[tuple[object, object], dict] = {}
    for item in units:
        key = (item.get("clause"), item.get("tableOrFigure"))
        group = groups.setdefault(
            key,
            {"clause": key[0], "tableOrFigure": key[1], "count": 0, "coverageIds": []},
        )
        group["count"] += 1
        group["coverageIds"].append(item.get("id"))
    out = []
    for group in groups.values():
        out.append(
            {
                "clause": group["clause"],
                "tableOrFigure": group["tableOrFigure"],
                "count": group["count"],
                "coverageIds": sorted(group["coverageIds"]),
            }
        )
    return sorted(out, key=lambda row: (-row["count"], str(row["clause"]), str(row["tableOrFigure"] or "")))


def _count_field(rows, key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = row.get(key)
        if value is None:
            continue
        name = str(value)
        counts[name] = counts.get(name, 0) + 1
    return counts


def leaf_unit_hash(text: str) -> str:
    """ARINC-LEAF-UNIT-NFC-LF-HWS-v2: NFC, LF, collapse horizontal whitespace, SHA-256."""
    canon = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    canon = re.sub(r"[ \t]+", " ", canon).strip()
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def is_complete_prose_sentence(text: str) -> bool:
    """True for a finished prose sentence. Truncated lead-ins and heading fragments fail."""
    compact = re.sub(r"\s+", " ", str(text or "")).strip()
    if len(compact) < 40:
        return False
    stripped = compact.rstrip('"').rstrip("'")
    if stripped.endswith("to include") or stripped.endswith("as follows"):
        return False
    if stripped.endswith(":"):
        return False
    return bool(re.search(r"[.!?]$", stripped))


SUPPORTING_SOURCE_STATUSES = {"BOUNDED-AUDIT-COMPLETE"}
SUPPORTING_LEAF_STATUSES = {
    "NOT-REQUIRED",
    "LEAF-CRS-EMITTED",
    "EXISTING-351-TRIGGERED-ROWS",
    "EXISTING-LEAF-VIA-2-1-2",
    "EXISTING-615A-LEAF",
    "EXISTING-LEAF-VIA-645",
    "CRS-M1-00519-REMAINS-NOT-YET-BOUND",
}
SUPPORTING_LEAF_BOUND_STATUSES = {
    "LEAF-CRS-EMITTED",
    "EXISTING-351-TRIGGERED-ROWS",
    "EXISTING-LEAF-VIA-2-1-2",
    "EXISTING-615A-LEAF",
    "EXISTING-LEAF-VIA-645",
}
# Historical enum retained for migration. Authorization comes from unboundDispositions, not from this name.
SUPPORTING_UNBOUND_LEAF_STATUSES = {
    "CRS-M1-00519-REMAINS-NOT-YET-BOUND",
}
SUPPORTING_NOT_REQUIRED_APPLICABILITY = {"OUT-OF-PROFILE", "DEPENDENCY-BLOCKED"}
SUPPORTING_REQUIRED_EFFECTS = {"REQUIRED", "CONDITIONAL-REQUIRED"}
SUPPORTING_APPLICABLE_DECISIONS = {"APPLICABLE-SUPPORTING", "CONDITIONAL"}


def supporting_scope_source_ids(register: dict | None = None) -> set[str]:
    """Supporting-source scope from the controlled register, not a counted whitelist."""
    register = CONTROLLED_SOURCES if register is None else register
    ids: set[str] = set()
    for row in register.get("sources") or []:
        if not isinstance(row, dict):
            continue
        if row.get("role") == "CURRENT-PROTOCOL-AUTHORITY":
            continue
        source_id = row.get("id")
        if isinstance(source_id, str) and source_id:
            ids.add(source_id)
    for row in register.get("openDependencies") or []:
        if not isinstance(row, dict):
            continue
        source_id = row.get("id")
        if isinstance(source_id, str) and source_id.startswith("RFC-"):
            ids.add(source_id)
    return ids


def supporting_unit_clause_prefixes(unit: dict) -> list[str]:
    """Locator prefixes for an audit unit. Composite numeric ranges split; titles stay whole."""
    locator = unit.get("leafLocator") if isinstance(unit.get("leafLocator"), dict) else {}
    recorded = locator.get("clausePrefixes")
    if isinstance(recorded, list) and recorded:
        return [str(item) for item in recorded if isinstance(item, str) and item]
    clause = str(unit.get("clause") or "")
    if re.fullmatch(r"[0-9]+(?:\.[0-9]+)*-[0-9]+(?:\.[0-9]+)*", clause):
        return clause.split("-")
    return [clause] if clause else []


def supporting_unit_source_ids(source_id: str, unit: dict) -> set[str]:
    locator = unit.get("leafLocator") if isinstance(unit.get("leafLocator"), dict) else {}
    recorded = locator.get("sourceIds")
    if isinstance(recorded, list) and recorded:
        return {str(item) for item in recorded if isinstance(item, str) and item}
    return {source_id} if source_id else set()


def supporting_unit_excluded_prefixes(unit: dict) -> list[str]:
    locator = unit.get("leafLocator") if isinstance(unit.get("leafLocator"), dict) else {}
    recorded = locator.get("excludedClausePrefixes")
    if isinstance(recorded, list):
        return [str(item) for item in recorded if isinstance(item, str) and item]
    return []


def clause_in_supporting_unit_scope(clause: str, unit: dict) -> bool:
    """True when a leaf clause is in the unit scope. Prefix+dot is allowed; exact unit clause also matches composites such as 3.2.2-3.2.3."""
    text = str(clause or "")
    excluded = supporting_unit_excluded_prefixes(unit)
    if any(text == prefix or text.startswith(prefix + ".") for prefix in excluded):
        return False
    if not unit.get("leafLocator") and text == str(unit.get("clause") or ""):
        return True
    for prefix in supporting_unit_clause_prefixes(unit):
        if text == prefix or text.startswith(prefix + "."):
            return True
    return False


def _register_source_digest(register: dict, source_id: str) -> str | None:
    for row in register.get("sources") or []:
        if isinstance(row, dict) and row.get("id") == source_id:
            digest = row.get("sha256")
            return str(digest) if digest else None
    for row in register.get("openDependencies") or []:
        if not isinstance(row, dict) or row.get("id") != source_id:
            continue
        retrieval = row.get("publicRetrieval") or {}
        digest = retrieval.get("retrievedSha256")
        return str(digest) if digest else None
    return None


def supporting_unbound_disposition_map(supporting: dict) -> tuple[dict[str, dict], list[str]]:
    """Index unbound dispositions by id. Does not authorize by historical status name."""
    errors: list[str] = []
    rows = supporting.get("unboundDispositions")
    if rows is None:
        return {}, ["supporting-source audit unboundDispositions is required"]
    if not isinstance(rows, list):
        return {}, ["supporting-source audit unboundDispositions must be a list"]
    by_id: dict[str, dict] = {}
    seen_units: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"supporting-source unboundDispositions[{index}] must be an object")
            continue
        disp_id = row.get("id")
        if not isinstance(disp_id, str) or not disp_id:
            errors.append(f"supporting-source unboundDispositions[{index}] is missing id")
            continue
        if disp_id in by_id:
            errors.append(f"supporting-source audit contains duplicate unbound disposition {disp_id}")
        by_id[disp_id] = row
        unit_id = row.get("auditUnitId")
        if not isinstance(unit_id, str) or not unit_id:
            errors.append(f"supporting-source unbound disposition {disp_id} is missing auditUnitId")
        elif unit_id in seen_units:
            errors.append(f"supporting-source unbound disposition repeats audit unit {unit_id}")
        else:
            seen_units.add(unit_id)
        if row.get("notIndependentApproval") is not True:
            errors.append(f"supporting-source unbound disposition {disp_id} must not claim independent approval")
        if not row.get("affectedRequirementId"):
            errors.append(f"supporting-source unbound disposition {disp_id} is missing affectedRequirementId")
        if not row.get("affectedCoverageId"):
            errors.append(f"supporting-source unbound disposition {disp_id} is missing affectedCoverageId")
        if not row.get("unfinishedScopeEn") or not row.get("unfinishedScopeZh"):
            errors.append(f"supporting-source unbound disposition {disp_id} is missing unfinished scope")
        if not row.get("sourceId") or not row.get("clause") or not row.get("rationaleCode"):
            errors.append(f"supporting-source unbound disposition {disp_id} is missing source, locator or rationale")
    return by_id, errors


def _unbound_unit_errors(
    unit: dict,
    source_id: str,
    dispositions: dict[str, dict],
    req_by_id: dict,
    coverage_by_id: dict,
    part4: dict,
) -> list[str]:
    """Unbound is a recorded gap. It still has source, effect, and affected-identity checks."""
    errors: list[str] = []
    unit_id = unit.get("id")
    applicability = unit.get("applicabilityDecision")
    effect = unit.get("conformanceEffect")
    if applicability in SUPPORTING_APPLICABLE_DECISIONS and effect in SUPPORTING_REQUIRED_EFFECTS:
        errors.append(
            f"supporting-source unit {unit_id} has applicable required obligations and cannot use an unbound leaf status"
        )
        return errors
    disp_id = unit.get("unboundDispositionId")
    if not isinstance(disp_id, str) or not disp_id:
        errors.append(f"supporting-source unit {unit_id} unbound status is missing unboundDispositionId")
        return errors
    disposition = dispositions.get(disp_id)
    if disposition is None:
        errors.append(f"supporting-source unit {unit_id} unboundDispositionId is not a recorded unbound disposition")
        return errors
    if disposition.get("auditUnitId") != unit_id:
        errors.append(f"supporting-source unit {unit_id} unbound disposition does not name this audit unit")
    if disposition.get("sourceId") != source_id:
        errors.append(f"supporting-source unit {unit_id} unbound disposition sourceId does not match the parent source")
    if disposition.get("clause") != unit.get("clause"):
        errors.append(f"supporting-source unit {unit_id} unbound disposition clause does not match the unit locator")
    if disposition.get("rationaleCode") != unit.get("rationaleCode"):
        errors.append(f"supporting-source unit {unit_id} unbound disposition rationaleCode does not match the unit")
    req_id = disposition.get("affectedRequirementId")
    if not isinstance(req_id, str) or req_id not in req_by_id:
        errors.append(f"supporting-source unit {unit_id} unbound affected requirement is absent from the bound CRS package")
        return errors
    req = req_by_id[req_id]
    cov_id = disposition.get("affectedCoverageId")
    expected_cov = (req.get("rhoRA") or {}).get("sourceCoverageId")
    if not isinstance(cov_id, str) or cov_id not in coverage_by_id:
        errors.append(f"supporting-source unit {unit_id} unbound affected coverage is absent from the bound CRS ledger")
    elif expected_cov and cov_id != expected_cov:
        errors.append(f"supporting-source unit {unit_id} unbound affected coverage does not match the bound requirement")
    if part4:
        if part4.get("unboundDispositionId") == disp_id:
            if part4.get("affectedRequirementId") != req_id:
                errors.append("supporting-source Part-4 record does not match the unbound affected requirement")
            if part4.get("status") and part4.get("status") != disposition.get("status"):
                errors.append("supporting-source Part-4 status does not match the unbound disposition")
    return errors


def supporting_source_audit_errors(
    audit: dict,
    crs: dict,
    register: dict | None = None,
) -> list[str]:
    """Structural supporting-source audit gate. Does not prove source-text completeness."""
    errors: list[str] = []
    register = CONTROLLED_SOURCES if register is None else register
    supporting = audit.get("supportingSourceApplicabilityAudit")
    if supporting is None:
        errors.append("supportingSourceApplicabilityAudit is required")
        return errors
    if not isinstance(supporting, dict):
        errors.append("supportingSourceApplicabilityAudit must be an object")
        return errors
    if supporting.get("notIndependentApproval") is not True:
        errors.append("supporting-source audit must not claim independent approval")
    blocked = audit.get("blockedSource") or {}
    if "645BindingThisPr" in supporting and supporting.get("645BindingThisPr") is not False:
        if blocked.get("boundThisPr") is not True:
            errors.append("claimed 645 binding must also set blockedSource.boundThisPr")
    dispositions, disposition_errors = supporting_unbound_disposition_map(supporting)
    errors.extend(disposition_errors)
    part4 = supporting.get("arinc664Part4") if isinstance(supporting.get("arinc664Part4"), dict) else {}
    if part4.get("unboundDispositionId"):
        if part4["unboundDispositionId"] not in dispositions:
            errors.append("supporting-source Part-4 record does not name a recorded unbound disposition")
    sources = supporting.get("sources")
    if not isinstance(sources, list):
        errors.append("supporting-source audit sources must be a list")
        return errors
    if not sources:
        errors.append("supporting-source audit sources must be non-empty")
        return errors
    expected_ids = supporting_scope_source_ids(register)
    recorded_ids: list[str] = []
    seen_source: set[str] = set()
    seen_units: set[str] = set()
    unbound_refs: dict[str, str] = {}
    coverage_by_id = {row["id"]: row for row in crs.get("coverageLedger") or [] if isinstance(row, dict) and row.get("id")}
    req_by_id = {row["id"]: row for row in crs.get("requirements") or [] if isinstance(row, dict) and row.get("id")}
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            errors.append(f"supporting-source audit sources[{index}] must be an object")
            continue
        source_id = source.get("sourceId")
        if not isinstance(source_id, str) or not source_id:
            errors.append(f"supporting-source audit sources[{index}] is missing sourceId")
            continue
        if source_id in seen_source:
            errors.append(f"supporting-source audit contains duplicate sourceId {source_id}")
        seen_source.add(source_id)
        recorded_ids.append(source_id)
        if source.get("status") not in SUPPORTING_SOURCE_STATUSES:
            errors.append(f"supporting-source {source_id} status is not a declared supporting-audit value")
        if source.get("independentApproval") is not False:
            errors.append(f"supporting-source {source_id} must not claim independent approval")
        expected_digest = _register_source_digest(register, source_id)
        recorded_digest = source.get("sha256")
        if expected_digest and recorded_digest and recorded_digest != expected_digest:
            errors.append(f"supporting-source {source_id} sha256 does not match the controlled register")
        units = source.get("units")
        if not isinstance(units, list) or not units:
            errors.append(f"supporting-source {source_id} units must be a non-empty list")
            continue
        denom = source.get("coverageDenominator") or {}
        if denom.get("count") != len(units):
            errors.append(f"supporting-source {source_id} coverageDenominator.count does not match units")
        unit_ids: list[str] = []
        seen_clauses: set[str] = set()
        allowed_sources_for_unit = lambda unit: supporting_unit_source_ids(source_id, unit)
        for unit_index, unit in enumerate(units):
            if not isinstance(unit, dict):
                errors.append(f"supporting-source {source_id} units[{unit_index}] must be an object")
                continue
            unit_id = unit.get("id")
            if not isinstance(unit_id, str) or not unit_id:
                errors.append(f"supporting-source {source_id} contains a unit without id")
                continue
            if unit_id in seen_units or unit_id in unit_ids:
                errors.append(f"supporting-source audit contains duplicate unit id {unit_id}")
            seen_units.add(unit_id)
            unit_ids.append(unit_id)
            clause = str(unit.get("clause") or "")
            if clause:
                if clause in seen_clauses:
                    errors.append(f"supporting-source {source_id} contains duplicate unit clause {clause}")
                seen_clauses.add(clause)
            applicability = unit.get("applicabilityDecision")
            effect = unit.get("conformanceEffect")
            leaf_status = unit.get("leafCrsStatus")
            if leaf_status not in SUPPORTING_LEAF_STATUSES:
                errors.append(f"supporting-source unit {unit_id} has undeclared leafCrsStatus")
                continue
            not_required_allowed = applicability in SUPPORTING_NOT_REQUIRED_APPLICABILITY or (
                applicability == "CONDITIONAL" and effect == "INFORMATIVE"
            )
            if leaf_status == "NOT-REQUIRED":
                if applicability in SUPPORTING_APPLICABLE_DECISIONS and effect in SUPPORTING_REQUIRED_EFFECTS:
                    errors.append(
                        f"supporting-source unit {unit_id} has applicable required obligations and cannot be NOT-REQUIRED"
                    )
                elif not not_required_allowed:
                    errors.append(
                        f"supporting-source unit {unit_id} NOT-REQUIRED is not supported by its applicability/effect disposition"
                    )
                continue
            if leaf_status in SUPPORTING_UNBOUND_LEAF_STATUSES:
                errors.extend(
                    _unbound_unit_errors(unit, source_id, dispositions, req_by_id, coverage_by_id, part4)
                )
                disp_id = unit.get("unboundDispositionId")
                if isinstance(disp_id, str) and disp_id:
                    unbound_refs[unit_id] = disp_id
                continue
            if leaf_status not in SUPPORTING_LEAF_BOUND_STATUSES:
                continue
            leaf_cov = unit.get("leafCoverageIds")
            leaf_req = unit.get("leafRequirementIds")
            admitted = unit.get("admittedLeafUnits")
            if not isinstance(leaf_cov, list) or not leaf_cov:
                errors.append(f"supporting-source unit {unit_id} {leaf_status} is missing leafCoverageIds")
                continue
            if not isinstance(admitted, list) or not admitted:
                errors.append(f"supporting-source unit {unit_id} {leaf_status} is missing admittedLeafUnits")
                continue
            if len(leaf_cov) != len(set(leaf_cov)):
                errors.append(f"supporting-source unit {unit_id} leafCoverageIds contains duplicates")
            admitted_cov: list[str] = []
            admitted_req: list[str] = []
            for item_index, item in enumerate(admitted):
                if not isinstance(item, dict):
                    errors.append(f"supporting-source unit {unit_id} admittedLeafUnits[{item_index}] must be an object")
                    continue
                cov_id = item.get("coverageId")
                source_unit = item.get("sourceUnitId")
                admitted_clause = item.get("clause")
                if not isinstance(cov_id, str) or cov_id not in coverage_by_id:
                    errors.append(f"supporting-source unit {unit_id} admitted coverage {cov_id} is absent from the bound CRS ledger")
                    continue
                if cov_id in admitted_cov:
                    errors.append(f"supporting-source unit {unit_id} admittedLeafUnits contains duplicate coverage {cov_id}")
                admitted_cov.append(cov_id)
                coverage = coverage_by_id[cov_id]
                cov_source = (coverage.get("source") or {}).get("sourceId")
                allowed_sources = allowed_sources_for_unit(unit)
                if cov_source not in allowed_sources:
                    errors.append(f"supporting-source unit {unit_id} admitted coverage {cov_id} is from {cov_source}")
                if source_unit and coverage.get("sourceUnitId") != source_unit:
                    errors.append(f"supporting-source unit {unit_id} admitted coverage {cov_id} sourceUnitId does not match the bound CRS ledger")
                leaf_clause = (coverage.get("source") or {}).get("clause")
                if admitted_clause and admitted_clause != leaf_clause:
                    errors.append(f"supporting-source unit {unit_id} admitted coverage {cov_id} clause does not match the bound CRS ledger")
                if not clause_in_supporting_unit_scope(str(leaf_clause or ""), unit):
                    errors.append(f"supporting-source unit {unit_id} admitted coverage {cov_id} is outside the unit locator scope")
                for req_id in item.get("requirementIds") or []:
                    if isinstance(req_id, str) and req_id not in admitted_req:
                        admitted_req.append(req_id)
            if set(leaf_cov) != set(admitted_cov):
                errors.append(
                    f"supporting-source unit {unit_id} leafCoverageIds do not match the admitted leaf-unit set"
                )
            expected_req: list[str] = []
            for cov_id in leaf_cov:
                if not isinstance(cov_id, str) or cov_id not in coverage_by_id:
                    errors.append(f"supporting-source unit {unit_id} leaf coverage {cov_id} is absent from the bound CRS ledger")
                    continue
                coverage = coverage_by_id[cov_id]
                cov_source = (coverage.get("source") or {}).get("sourceId")
                allowed_sources = allowed_sources_for_unit(unit)
                if cov_source not in allowed_sources:
                    errors.append(f"supporting-source unit {unit_id} leaf coverage {cov_id} is from {cov_source}")
                if not clause_in_supporting_unit_scope(str((coverage.get("source") or {}).get("clause") or ""), unit):
                    errors.append(f"supporting-source unit {unit_id} leaf coverage {cov_id} is outside the unit locator scope")
                for req_id in coverage.get("requirementIds") or []:
                    if req_id not in expected_req:
                        expected_req.append(req_id)
            if not isinstance(leaf_req, list):
                errors.append(f"supporting-source unit {unit_id} {leaf_status} is missing leafRequirementIds")
                continue
            if len(leaf_req) != len(set(leaf_req)):
                errors.append(f"supporting-source unit {unit_id} leafRequirementIds contains duplicates")
            if set(leaf_req) != set(expected_req):
                errors.append(
                    f"supporting-source unit {unit_id} leafRequirementIds do not match the bound coverage requirement set"
                )
            if admitted_req and set(leaf_req) != set(admitted_req):
                errors.append(
                    f"supporting-source unit {unit_id} leafRequirementIds do not match the admitted leaf-unit set"
                )
            for req_id in leaf_req:
                if req_id not in req_by_id:
                    errors.append(f"supporting-source unit {unit_id} leaf requirement {req_id} is absent from the bound CRS package")
                    continue
                req = req_by_id[req_id]
                req_source = (req.get("source") or {}).get("sourceId")
                if req_source not in allowed_sources_for_unit(unit):
                    errors.append(f"supporting-source unit {unit_id} leaf requirement {req_id} is from {req_source}")
                if not clause_in_supporting_unit_scope(str((req.get("source") or {}).get("clause") or ""), unit):
                    errors.append(f"supporting-source unit {unit_id} leaf requirement {req_id} is outside the unit locator scope")
    extra = set(recorded_ids) - expected_ids
    missing = expected_ids - set(recorded_ids)
    if extra:
        errors.append("supporting-source audit contains sources outside the controlled supporting scope")
    if missing:
        errors.append("supporting-source audit is missing sources from the controlled supporting scope")
    for disp_id, disposition in dispositions.items():
        unit_id = disposition.get("auditUnitId")
        if unit_id not in unbound_refs:
            errors.append(f"supporting-source unbound disposition {disp_id} is not used by an unbound audit unit")
        elif unbound_refs.get(unit_id) != disp_id:
            errors.append(f"supporting-source unbound disposition {disp_id} does not match the unit unboundDispositionId")
    return errors


def protocol_source_audit_errors(audit: dict, crs: dict, register: dict | None = None) -> list[str]:
    """Row-level navigation identity of the deferred ledger. Not a source-semantics proof."""
    errors: list[str] = []
    status = audit.get("status")
    if status not in AUDIT_STATUS_GENERATION:
        errors.append("protocol source audit status is not a declared audit-phase value")
    expected_generation = AUDIT_STATUS_GENERATION.get(status)
    if audit.get("requirementGenerationAllowed") is not expected_generation:
        errors.append("protocol source audit requirementGenerationAllowed must match the declared status")
    if audit.get("notBatchStatusRename") is not True:
        errors.append("protocol source audit must forbid batch status rename")
    bound = audit.get("boundPackage") or {}
    inventory = crs.get("inventorySummary") or {}
    if bound.get("coverageFingerprint") != inventory.get("coverageFingerprint"):
        errors.append("protocol source audit coverage fingerprint does not match the bound CRS package")
    if bound.get("requirementsFingerprint") != inventory.get("requirementsFingerprint"):
        errors.append("protocol source audit requirements fingerprint does not match the bound CRS package")
    if bound.get("artifactVersion") != crs.get("artifactVersion"):
        errors.append("protocol source audit artifactVersion does not match the bound CRS package")
    if bound.get("coverageCount") != inventory.get("coverageCount"):
        errors.append("protocol source audit boundPackage.coverageCount does not match the bound CRS package")
    if bound.get("requirementCount") != inventory.get("requirementCount"):
        errors.append("protocol source audit boundPackage.requirementCount does not match the bound CRS package")
    ledger = {row["id"]: row for row in crs.get("coverageLedger") or []}
    deferred_units = audit.get("deferredUnits") or {}
    summary = audit.get("summary") or {}
    rationale_counts = summary.get("rationaleCodes") or {}
    by_rationale = ((summary.get("deferredFutureScope") or {}).get("byRationale") or {})
    clause_groups = audit.get("clauseGroups") or {}
    for code in DEFERRED_AUDIT_CODES:
        expected_rows = {
            row_id: _audit_locator_from_crs(row)
            for row_id, row in ledger.items()
            if row.get("rationaleCode") == code
        }
        recorded = deferred_units.get(code)
        if not isinstance(recorded, list):
            errors.append(f"protocol source audit deferredUnits.{code} must be a list")
            continue
        recorded_ids = [item.get("id") if isinstance(item, dict) else None for item in recorded]
        if None in recorded_ids or "" in recorded_ids:
            errors.append(f"protocol source audit {code} contains a row without id")
        if len(recorded_ids) != len(set(recorded_ids)):
            errors.append(f"protocol source audit {code} contains duplicate coverage ids")
        if set(recorded_ids) - {None, ""} != set(expected_rows):
            errors.append(f"protocol source audit IDs for {code} do not match the bound CRS ledger")
        if by_rationale.get(code, 0) != len(expected_rows):
            errors.append(f"protocol source audit summary count for {code} does not match the bound CRS ledger")
        if rationale_counts.get(code, 0) != len(expected_rows):
            errors.append(f"protocol source audit rationaleCodes.{code} does not match the bound CRS ledger")
        locators: list[dict] = []
        for item in recorded:
            if not isinstance(item, dict):
                errors.append(f"protocol source audit {code} contains a non-object row")
                continue
            missing = [field for field in AUDIT_UNIT_FIELDS if field not in item]
            if missing:
                errors.append(f"protocol source audit row {item.get('id')} is missing {missing[0]}")
                continue
            if item.get("requirementIds") is None:
                errors.append(f"protocol source audit row {item.get('id')} must make requirementIds explicit")
                continue
            row_id = item.get("id")
            expected = expected_rows.get(row_id)
            if expected is None:
                continue
            for field in AUDIT_UNIT_FIELDS:
                left = item.get(field)
                right = expected.get(field)
                if field == "requirementIds":
                    left = list(left or [])
                    right = list(right or [])
                if left != right:
                    errors.append(
                        f"protocol source audit row {row_id} {field} does not match the bound CRS locator"
                    )
            locators.append(item)
        expected_groups = _expected_clause_groups(list(expected_rows.values()))
        recorded_groups = clause_groups.get(code) or []
        normalized = []
        if not isinstance(recorded_groups, list):
            errors.append(f"protocol source audit clauseGroups.{code} must be a list")
        else:
            for group in recorded_groups:
                if not isinstance(group, dict):
                    errors.append(f"protocol source audit clauseGroups.{code} contains a non-object group")
                    continue
                normalized.append(
                    {
                        "clause": group.get("clause"),
                        "tableOrFigure": group.get("tableOrFigure"),
                        "count": group.get("count"),
                        "coverageIds": sorted(group.get("coverageIds") or []),
                    }
                )
            normalized = sorted(
                normalized,
                key=lambda row: (-int(row["count"] or 0), str(row["clause"]), str(row["tableOrFigure"] or "")),
            )
            if normalized != expected_groups:
                errors.append(f"protocol source audit clauseGroups.{code} drifted from deferredUnits")
    if summary.get("coverageCount") != inventory.get("coverageCount"):
        errors.append("protocol source audit summary.coverageCount does not match the bound CRS package")
    if summary.get("requirementCount") != inventory.get("requirementCount"):
        errors.append("protocol source audit summary.requirementCount does not match the bound CRS package")
    expected_app = _count_field(ledger.values(), "applicabilityDecision")
    if (summary.get("applicabilityDecisions") or {}) != expected_app:
        errors.append("protocol source audit summary.applicabilityDecisions drifted from the bound CRS ledger")
    expected_rat = _count_field(ledger.values(), "rationaleCode")
    if (summary.get("rationaleCodes") or {}) != expected_rat:
        errors.append("protocol source audit summary.rationaleCodes drifted from the bound CRS ledger")
    deferred_total = expected_app.get("DEFERRED-FUTURE-SCOPE", 0)
    future = summary.get("deferredFutureScope") or {}
    if future.get("total") != deferred_total:
        errors.append("protocol source audit summary.deferredFutureScope.total does not match the bound CRS ledger")
    errors.extend(source_reread_errors(audit))
    reread = audit.get("sourceReread") or {}
    generated_ids_by_code = reread.get("generatedUnitIdsByCode") or {}
    for code in reread.get("generatedCodes") or []:
        if not isinstance(code, str):
            continue
        for row_id in generated_ids_by_code.get(code) or []:
            if row_id not in ledger:
                errors.append(f"{code} generated inventory id {row_id} is absent from the bound CRS ledger")
    errors.extend(supporting_source_audit_errors(audit, crs, register))
    return errors


CLTAV_INTERFACE_REGISTRY_PATH = ROOT / "configs/research/cltav_interface_registry.json"
CLTAV_FIGURE_GRAPHS_PATH = ROOT / "configs/research/cltav_figure_graphs.json"
CLTAV_OWNED_ARTIFACTS_PATH = ROOT / "configs/research/cltav_owned_generated_artifacts.json"
CLTAV_INTERFACE_IDS = (
    "IF-PRED-OBS",
    "IF-HIST-UPDATE",
    "IF-OBS-INTERPRET",
    "IF-SELECT-ADMIT",
    "IF-EXECUTE-RECORD",
    "IF-PREP-RECOVER",
    "IF-EQUIV",
    "IF-RESOURCE-STOP",
)
CLTAV_EXPERIMENT_IDS = ("EXP-CLTAV-DETECT", "EXP-CLTAV-LOCATE", "EXP-CLTAV-ABLATION")
READER_ALG_PDF = ROOT / "artifacts/publications/cltav/ALG-CLTAV-01.pdf"


def arinc_645_closure_errors(audit: dict, crs: dict, model: dict | None = None) -> list[str]:
    """SOURCE/SEMANTIC bind is not CAPABILITY establishment. Not a source-faithfulness proof."""
    errors: list[str] = []
    supporting = audit.get("supportingSourceApplicabilityAudit") or {}
    if supporting.get("645BindingThisPr") is not True:
        return errors
    remaining = audit.get("remainingSourceWork")
    if not isinstance(remaining, dict):
        errors.append("645 remaining work is missing after source bind")
        return errors
    if remaining.get("arinc645CapabilityEstablishmentThisPr") is not False:
        errors.append("645 source bind must not establish capabilities")
    for key in (
        "crcValidationEstablishedThisPr",
        "checkValueValidationEstablishedThisPr",
        "namingAlgorithmValidationEstablishedThisPr",
        "completeIntegrityValidationEstablishedThisPr",
    ):
        if remaining.get(key) is not False:
            errors.append(f"645 source bind must not establish {key}")
    gap = remaining.get("arinc645RemainingWorkAfterThisPr") or {}
    if gap.get("id") != "GAP-ARINC-645" or gap.get("status") != "NOT-ESTABLISHED":
        errors.append("GAP-ARINC-645 must remain NOT-ESTABLISHED after source bind")
    for key in (
        "crcValidation",
        "checkValueValidation",
        "namingAlgorithmValidation",
        "completeIntegrityValidation",
    ):
        item = gap.get(key) or {}
        if item.get("status") != "CAPABILITY-NOT-ESTABLISHED" or item.get("establishedThisPr") is not False:
            errors.append(f"645 source bind must not establish {key}")
    if model is not None:
        blocked = (((model.get("model") or {}).get("interfaces") or {}).get("IF_INTEGRITY") or {}).get("blockedBy")
        if not isinstance(blocked, list) or "ARINC-645" not in blocked:
            errors.append("bound M2 IF_INTEGRITY must remain blocked by ARINC-645")
    reqs = [row for row in crs.get("requirements") or [] if (row.get("source") or {}).get("sourceId") == "ARINC-645"]
    if not reqs:
        errors.append("645 source bind must emit in-scope semantic leaves")
        return errors
    for row in reqs:
        action = str((row.get("semantic") or {}).get("action") or "")
        objects = list((row.get("semantic") or {}).get("objects") or [])
        en = str(row.get("generatedSemanticProjectionEn") or "")
        zh = str(row.get("generatedSemanticProjectionZh") or "")
        page = (row.get("source") or {}).get("pdfPage")
        if "PREFIX-HEADER-FILENAME" in action and (
            "DATA-FILE-NAME" in objects or "SUPPORT-FILE-NAME" in objects
        ):
            errors.append("645 manufacturer prefix must not apply to Data or Support filenames")
        if "not distinct LSPs" in en or "不是不同 LSP" in zh:
            errors.append("645 case rule must not be rewritten as a different-LSP identity rule")
        if "BIND-CRC-64-CHECK" in action and page == 34:
            errors.append("645 CRC-64 Check is not located on PDF 34")
        if "BIND-CRC-64-REFIN" in action and page == 34:
            errors.append("645 CRC-64 RefIn/RefOut/XorOut are not located on PDF 34")
    type_rows = [
        row
        for row in reqs
        if (row.get("source") or {}).get("tableOrFigure") == "Table 4-5"
        and (row.get("source") or {}).get("fragmentKind") == "TABLE-ROW"
    ]
    if len(type_rows) < 8:
        errors.append("645 Table 4-5 type/method/length rows must be split per type")
    footnotes = [
        row
        for row in reqs
        if (row.get("source") or {}).get("tableOrFigure") == "Table 4-5"
        and (row.get("source") or {}).get("fragmentKind") == "TABLE-FOOTNOTE"
    ]
    if len(footnotes) < 2:
        errors.append("645 Table 4-5 footnotes must be separate leaves")
    for action in (
        "BIND-CRC-8-CHECK-TO-256-BYTE-VECTOR",
        "BIND-CRC-16-CHECK-TO-256-BYTE-VECTOR",
        "BIND-CRC-32-CHECK-TO-256-BYTE-VECTOR",
        "BIND-CRC-64-CHECK-TO-256-BYTE-VECTOR",
    ):
        if not any((row.get("semantic") or {}).get("action") == action for row in reqs):
            errors.append(f"645 missing check-vector association {action}")
    source_645 = next(
        (
            row
            for row in (supporting.get("sources") or [])
            if isinstance(row, dict) and row.get("sourceId") == "ARINC-645"
        ),
        None,
    )
    if isinstance(source_645, dict):
        front = ((source_645.get("pageAccount") or {}).get("frontMatterPdfPages") or [0, 0])
        if len(front) >= 2 and int(front[1]) >= 31:
            errors.append("645 PDF 31 CRC body must not be classified as front matter")
        units = {row.get("id"): row for row in (source_645.get("units") or []) if isinstance(row, dict)}
        front_unit = units.get("SAU-645-FRONT") or {}
        front_pages = front_unit.get("pdfPages") or []
        if front_pages and int(front_pages[-1]) >= 31:
            errors.append("645 front-matter unit must not include CRC body page 31")
        if "SAU-645-BODY-PRE" not in units:
            errors.append("645 untriggered body before CRC must be classified, not absorbed into front matter")
        pre = units.get("SAU-645-BODY-PRE") or {}
        if pre.get("clause") != "1-4.2" or pre.get("pdfPages") != [7, 29]:
            errors.append("645 untriggered pre-body must end at §4.2 / PDF 29; §4.3.1 is on PDF 30")
        byte_order_unit = units.get("SAU-645-4-3-2-FILE-BYTE-ORDER") or {}
        if byte_order_unit.get("applicabilityDecision") != "APPLICABLE-SUPPORTING":
            errors.append("645 §4.3.2 file-byte order must be classified as applicable supporting source")
        if byte_order_unit.get("leafRequirementIds") != ["CRS-M1-00864"]:
            errors.append("645 §4.3.2 file-byte order must map to its dedicated CRS leaf")
        expected_pdf30_dispositions = {
            "SAU-645-4-3-1-CRC-DEFINITION": (
                "4.3.1", "CRC-FORMAL-DEFINITION-INTERPRETED-BY-SELECTED-PARAMETERS"
            ),
            "SAU-645-4-3-2-1-BIT-ORDERING": (
                "4.3.2.1", "CRC-BIT-ORDER-INTERPRETED-BY-SELECTED-REFLECTION-PARAMETERS"
            ),
            "SAU-645-4-3-2-2-BIT-SHIFTING": (
                "4.3.2.2", "CRC-IMPLEMENTATION-RESOURCE-NOT-PROTOCOL-FRAMING-OBLIGATION"
            ),
        }
        for unit_id, (clause, rationale) in expected_pdf30_dispositions.items():
            unit = units.get(unit_id) or {}
            if (
                unit.get("clause") != clause
                or unit.get("pdfPages") != [30, 30]
                or unit.get("applicabilityDecision") != "OUT-OF-PROFILE"
                or unit.get("conformanceEffect") != "INFORMATIVE"
                or unit.get("leafCrsStatus") != "NOT-REQUIRED"
                or unit.get("rationaleCode") != rationale
            ):
                errors.append(f"645 {clause} on PDF 30 must retain its explicit non-obligation disposition")
        bit_order = units.get("SAU-645-4-3-2-1-BIT-ORDERING") or {}
        if "unreflected" not in str(bit_order.get("summaryEn") or "").lower() or "不反射" not in str(bit_order.get("summaryZh") or ""):
            errors.append("645 §4.3.2.1 disposition must not imply all CRC algorithms are unreflected")
        bit_shift = units.get("SAU-645-4-3-2-2-BIT-SHIFTING") or {}
        if "segmentation" not in str(bit_shift.get("summaryEn") or "").lower() or "分段" not in str(bit_shift.get("summaryZh") or ""):
            errors.append("645 §4.3.2.2 disposition must reject a protocol-segmentation interpretation")
        hash_unit = units.get("SAU-645-4-6-HASH") or {}
        hash_pages = [int(item) for item in (hash_unit.get("pdfPages") or []) if str(item).isdigit()]
        if 36 not in hash_pages:
            errors.append("645 §4.6 exclusion must include PDF 36 where the hash body starts")
        if units.get("SAU-645-4-3-2-EFF", {}).get("applicabilityDecision") != "OUT-OF-PROFILE":
            errors.append("645 4.3.2.8 process efficiency must receive an applicability disposition")
        if units.get("SAU-645-4-3-2-EX", {}).get("applicabilityDecision") != "OUT-OF-PROFILE":
            errors.append("645 4.3.2.9 CRC examples must receive an applicability disposition")
        relations = source_645.get("triggerRelationsThisPr") or []
        req_by_id = {row.get("id"): row for row in crs.get("requirements") or [] if isinstance(row, dict)}
        actions_645 = {
            str((row.get("semantic") or {}).get("action") or "")
            for row in reqs
        }
        if len(relations) < 3:
            errors.append("645 trigger relations must cover CRC, check-value and naming groups")
        for relation in relations:
            if not isinstance(relation, dict):
                errors.append("645 trigger relation must be an object")
                continue
            for req_id in relation.get("fromRequirementIds") or []:
                if req_id not in req_by_id:
                    errors.append(f"645 trigger relation cites missing requirement {req_id}")
            for action in relation.get("to645Actions") or []:
                if action not in actions_645:
                    errors.append(f"645 trigger relation cites missing leaf action {action}")
    actions = {str((row.get("semantic") or {}).get("action") or "") for row in reqs}
    for action in (
        "BIND-CRC-TRANSMISSION-BIT-REFLECTION",
        "BIND-CRC-PROCESS-BIT-REFLECTION",
        "BIND-CRC-POST-PROCESS-BIT-REFLECTION",
        "RECORD-CRC-ALL-ONES-INITIALIZATION-VARIANT",
        "PAD-SHORT-INPUT-TO-CRC-REGISTER-SIZE",
        "RECORD-CRC-FINAL-ONES-COMPLEMENT-VARIANT",
        "PROCESS-CRC-FILE-BYTES-IN-OCCURRENCE-ORDER",
        "INCLUDE-NECESSARY-DATA-FOR-EACH-LOADING-INTERFACE",
    ):
        if action not in actions:
            errors.append(f"645 missing PDF31 or §7.1 residual leaf {action}")
    crc_by_action = {
        str((row.get("semantic") or {}).get("action") or ""): row
        for row in reqs
    }
    file_order = crc_by_action.get("PROCESS-CRC-FILE-BYTES-IN-OCCURRENCE-ORDER") or {}
    if file_order.get("source", {}).get("pdfPage") != 30 or file_order.get("source", {}).get("clause") != "4.3.2":
        errors.append("645 CRC file-byte-order leaf must be anchored at §4.3.2 PDF 30")
    if set((file_order.get("semantic") or {}).get("objects") or []) != {"CRC", "FILE-BYTE-SEQUENCE"}:
        errors.append("645 CRC file-byte-order leaf must not conflate input order with check-value storage")
    for action in (
        "RECORD-CRC-ALL-ONES-INITIALIZATION-VARIANT",
        "RECORD-CRC-FINAL-ONES-COMPLEMENT-VARIANT",
    ):
        variant = crc_by_action.get(action) or {}
        if variant.get("conformanceEffect") != "INFORMATIVE":
            errors.append(f"645 {action} must remain a variant explanation, not a universal requirement")
        if (variant.get("semantic") or {}).get("condition") == "WHEN-615A-INTEGRITY-REQUIRES-A-645-CRC":
            errors.append(f"645 {action} must not be universal across 615A CRC algorithms")
    row_544 = next((row for row in crs.get("requirements") or [] if row.get("id") == "CRS-M1-00544"), None)
    row_545 = next((row for row in crs.get("requirements") or [] if row.get("id") == "CRS-M1-00545"), None)
    if row_544 and row_545:
        en_544 = str(row_544.get("generatedSemanticProjectionEn") or "")
        if "blocked by ARINC 645" in en_544.lower():
            errors.append("CRS-M1-00544 must not call algorithm identity blocked after the 645 source bind")
        if "CRS-M1-00819" not in en_544:
            errors.append("CRS-M1-00544 must bind algorithm identity to the 645 CRC-16 leaf")
    remaining_reason = str(remaining.get("remainingReasonEn") or "") + str(audit.get("blockedSource") or {})
    if "file is missing" in remaining_reason.lower() or "未取得文件" in remaining_reason:
        errors.append("645 remaining work must not be explained as a missing file")
    return errors


def governed_source_errors(audit: dict, crs: dict, model: dict | None = None) -> list[str]:
    """Governance aggregation for the controlled source package.

    This is the single entry the baseline validator uses for the source audit and
    the 615A-triggered 645 closure, so a persistence test can prove that a mutated
    controlled input is collected by the normal governance path rather than by an
    isolated helper.
    """
    return protocol_source_audit_errors(audit, crs) + arinc_645_closure_errors(audit, crs, model)


def _load_cltav_registry(registry: dict | None = None) -> dict:
    if registry is not None:
        return registry
    return json.loads(CLTAV_INTERFACE_REGISTRY_PATH.read_text(encoding="utf-8"))


def _algorithm_body(algorithm: str) -> str:
    match = re.search(r"\\begin\{algorithm\}.*?\\end\{algorithm\}", algorithm, re.S)
    return match.group(0) if match else ""


def _puml_edges(text: str) -> list[tuple[str, str, str]]:
    edges: list[tuple[str, str, str]] = []
    for raw in text.splitlines():
        line = raw.strip()
        match = re.match(r"^(\w+)\s+(-+\S*->)\s+(\w+)(.*)$", line)
        if match:
            edges.append((match.group(1), match.group(3), line))
    return edges


# STABLE_INVARIANT: presentation layers and top-level control-flow relations of
# the CL-TAV algorithm package (DD-036). These are structural, not lifecycle data.
CLTAV_MODULE_IDS = (
    "ALG-CLTAV-01",
    "ALG-CLTAV-05",
    "ALG-CLTAV-06",
    "ALG-CLTAV-07",
    "ALG-CLTAV-02",
    "ALG-CLTAV-03",
    "ALG-CLTAV-04",
    "ALG-CLTAV-APPENDIX",
)
CLTAV_MAIN_PROCEDURES = (
    "Initialize",
    "EntryStop",
    "PredictCurrent",
    "SelectAndAdmit",
    "SelectSnapshot",
    "ChargeOnce",
    "ExecuteAndRecord",
    "InterpretOutcome",
    "ResolveOutcome",
    "CommitCompatibleUpdate",
    "PostUpdateStop",
)
CLTAV_MODULE_PROCEDURES = {
    "ALG-CLTAV-02": ("PredictCurrent",),
    "ALG-CLTAV-03": ("InterpretOutcome",),
    "ALG-CLTAV-04": ("ResolveOutcome",),
    "ALG-CLTAV-05": ("SelectAndAdmit",),
    "ALG-CLTAV-06": ("InterpretTimedObservation",),
    "ALG-CLTAV-07": ("CommitCompatibleUpdate",),
}


def _algorithm_bodies(algorithm: str) -> str:
    """Return every algorithm environment, so a decomposed package is checked as a whole."""
    return "\n".join(
        re.findall(r"\\begin\{algorithm\}.*?\\end\{algorithm\}", algorithm, re.S)
    )


def _cltav_presentation_errors(
    algorithms: dict[str, str], main_body: str,
) -> list[str]:
    """Cross-file control-flow relations for the decomposed CL-TAV algorithm package."""
    errors: list[str] = []
    positions: list[tuple[int, str]] = []
    for name in CLTAV_MAIN_PROCEDURES:
        at = main_body.find(name)
        if at < 0:
            errors.append(f"top-level algorithm is missing procedure {name}")
        else:
            positions.append((at, name))
    ordered = [name for _, name in sorted(positions)]
    if ordered != [name for name in CLTAV_MAIN_PROCEDURES if name in ordered]:
        errors.append("top-level procedure order differs from the specified control flow")
    if "Finish" not in main_body:
        errors.append("top-level algorithm is missing its Finish return")
    predict = main_body.find("PredictCurrent")
    select = main_body.find("SelectAndAdmit")
    if predict < 0 or select < 0 or predict > select:
        errors.append("PredictCurrent (IF-PRED-OBS) must be called before SelectAndAdmit (IF-SELECT-ADMIT)")
    for module, procedures in CLTAV_MODULE_PROCEDURES.items():
        text = algorithms.get(module, "")
        for procedure in procedures:
            if procedure not in text:
                errors.append(f"{module} does not define {procedure}")
    return errors


def _strip_tex_comments(text: str) -> str:
    """Remove TeX and algorithm2e comments so a name kept only in a comment is not a call."""
    text = re.sub(r"(?<!\\)%.*", "", text)
    pattern = re.compile(r"\\tcp\*?|\\tcc\*?")
    out: list[str] = []
    index = 0
    while index < len(text):
        match = pattern.search(text, index)
        if not match:
            out.append(text[index:])
            break
        out.append(text[index:match.start()])
        cursor = match.end()
        while cursor < len(text) and text[cursor] in " \t":
            cursor += 1
        if cursor < len(text) and text[cursor] == "{":
            depth = 0
            while cursor < len(text):
                if text[cursor] == "{":
                    depth += 1
                elif text[cursor] == "}":
                    depth -= 1
                cursor += 1
                if depth == 0:
                    break
        index = cursor
    return "".join(out)


def _cltav_executable_errors(algorithms: dict[str, str]) -> list[str]:
    """Bounded executable-call model: statements, signatures, data flow and return branches.

    Comment-only names (TeX percent comments and algorithm2e tcp/tcc), macro
    definitions and captions do not satisfy these checks. Relations are checked,
    not just keywords.
    """
    errors: list[str] = []
    bodies = {
        module: _strip_tex_comments(_algorithm_bodies(text))
        for module, text in algorithms.items()
    }
    main = bodies.get("ALG-CLTAV-01", "")

    if r"\textsc{ChargeOnce}(" not in main:
        errors.append("top-level must charge once as an executable statement, not only a name in a comment")
    obs_call = re.search(r"\\textsc\{InterpretOutcome\}\(([^)]*)\)", main)
    if not obs_call or not all(
        token in obs_call.group(1) for token in (r"\textit{er}", r"\xi", r"\Gamma", r"\eta")
    ):
        errors.append("InterpretOutcome must receive ExecutionResult, snapshot xi, Gamma and eta")
    if r"\textit{dec}.\mathrm{actionId}" not in main:
        errors.append("top-level must project the selected actionId from the Decision record")
    if r"\textit{dec}.\mathrm{actionKind}" not in main:
        errors.append("the snapshot action kind must come from the Decision actionKind")
    if re.search(r"SelectSnapshot\}\(\s*\\textit\{dec\}\.\\mathrm\{kind\}", main):
        errors.append("the snapshot must not use the ACTION/EXIT discriminant as the action kind")
    if "is a valid observation class or $z.\\mathrm{summaryConfirmed}$ is true" not in main:
        errors.append("the S9 guard must be an executable condition, not a comment")

    alg02 = bodies.get("ALG-CLTAV-02", "")
    if r"\textit{raw}.\mathrm{status}=\texttt{GAP}" not in alg02:
        errors.append("PredictCurrent must branch on the backend tag before projection")
    gap_at = alg02.find(r"\mathrm{status}=\texttt{GAP}")
    proj_at = alg02.find("ProjectOntoCurrentH")
    if gap_at < 0 or proj_at < 0 or gap_at > proj_at:
        errors.append("PredictCurrent must branch on the gap tag before class projection")
    if r"\Return PredictionResult$(\mathrm{status}=\texttt{GAP}" not in alg02:
        errors.append("PredictCurrent must return a tagged gap result instead of projecting an error")

    alg03 = bodies.get("ALG-CLTAV-03", "")
    if r"z.\mathrm{effect}\leftarrow\textit{er}.\mathrm{effect}" not in alg03:
        errors.append("InterpretOutcome must copy the executed effect into the Outcome")
    if r"z.\mathrm{kind}\leftarrow\xi.\mathrm{actionKind}" not in alg03:
        errors.append("InterpretOutcome must copy the snapshot action kind into the Outcome")
    if r"z.\mathrm{summaryConfirmed}\leftarrow\textit{summaryConfirmed}" not in alg03:
        errors.append("InterpretOutcome must take summaryConfirmed from the interpretation interface")
    if re.search(r"\\mathrm\{summaryConfirmed\}\s*\\leftarrow\s*\\textbf\{true\}", alg03):
        errors.append("InterpretOutcome must not default summaryConfirmed to true")
    if r"\IFobs" not in alg03:
        errors.append("InterpretOutcome must call IF-OBS-INTERPRET")
    if r"\IFprep" not in alg03:
        errors.append("InterpretOutcome must call IF-PREP-RECOVER for Prep and Recover")

    alg04 = bodies.get("ALG-CLTAV-04", "")
    if r"\mathrm{control}=\texttt{RETRY}" not in alg04:
        errors.append("ResolveOutcome must return RETRY on the ERROR or unknown path")
    if r"\Gamma'\leftarrow\Gamma" not in alg04:
        errors.append("ResolveOutcome must initialize the returned context from Gamma")

    alg05 = bodies.get("ALG-CLTAV-05", "")
    if r"\IFsel" not in alg05:
        errors.append("SelectAndAdmit must call IF-SELECT-ADMIT")

    alg06 = bodies.get("ALG-CLTAV-06", "")
    if r"M\subseteq N_r" not in alg06 or r"\not\subseteq" in alg06:
        errors.append("timed observation must apply the T5 containment relation")
    if r"M=\varnothing" not in alg06:
        errors.append("timed observation must reject an empty measurement domain as ERROR")
    if r"\mathrm{lowerHorizon}>U_r" not in alg06 or r"\mathrm{lowerHorizon}\ge U_r" not in alg06:
        errors.append("no-response must distinguish the closed and open upper bound")
    if re.search(r"I_z\s*\\leftarrow", alg06):
        errors.append("timed observation must not emit the candidate set as a timing verdict")

    alg07 = bodies.get("ALG-CLTAV-07", "")
    if r"H\cap z.I_z" not in alg07:
        errors.append("history update must intersect H with the compatible set")
    if re.search(r"H'?\s*\\leftarrow\s*z\.I_z", alg07):
        errors.append("history update must not assign H = I_z")
    if r"\Gamma'\leftarrow\Gamma" not in alg07:
        errors.append("history update must initialize the returned context from Gamma")
    if "precondition" not in alg07.lower():
        errors.append("history update must declare the S9 guard as a precondition")
    if "$z.\\mathrm{summaryConfirmed}$ is true" not in alg07:
        errors.append("S9 must commit currentSummary only under the confirmed successor guard")
    return errors


def cltav_algorithm_contract_errors(
    algorithms: "dict[str, str] | str",
    experiment_puml: str,
    experiment_plan: str,
    registry: dict | None = None,
) -> list[str]:
    """Registry, cross-file interface calls, top-level control flow and experiment record edges."""
    errors: list[str] = []
    if isinstance(algorithms, str):
        algorithms = {"ALG-CLTAV-01": algorithms}
    corpus = "\n".join(algorithms.values())
    main_text = algorithms.get("ALG-CLTAV-01", "")
    main_body = _algorithm_bodies(main_text)
    corpus_bodies = _algorithm_bodies(corpus)
    spec = _load_cltav_registry(registry)
    declared_modules = spec.get("presentationModules")
    if declared_modules and set(algorithms) != set(declared_modules):
        errors.append("algorithm package modules differ from the registry presentationModules")
    interfaces = spec.get("interfaces") or []
    experiment_ifs = spec.get("experimentInterfaces") or []
    if not isinstance(interfaces, list) or not interfaces:
        errors.append("CL-TAV interface registry is missing interfaces")
        return errors
    ids = [row.get("id") for row in interfaces if isinstance(row, dict)]
    if None in ids or "" in ids:
        errors.append("CL-TAV interface registry contains an interface without id")
    if len(list(filter(None, ids))) != len(set(filter(None, ids))):
        errors.append("CL-TAV interface registry contains duplicate interface ids")
    required_fields = ("id", "inputs", "outputs", "pre", "guarantee", "failure", "stateEffect")
    for row in interfaces:
        if not isinstance(row, dict):
            errors.append("CL-TAV interface registry contains a non-object interface")
            continue
        missing = [field for field in required_fields if not row.get(field)]
        if missing:
            errors.append(f"{row.get('id')} is missing {missing[0]}")
        if row.get("id") == "IF-HIST-UPDATE":
            joined = " ".join(str(item) for item in (row.get("inputs") or []) + (row.get("outputs") or []))
            if "HistoryHandle" not in joined:
                errors.append("IF-HIST-UPDATE is missing a HistoryHandle carrier")
        if row.get("id") == "IF-PREP-RECOVER" and not {"targetConfirmed", "summaryConfirmed"}.issubset(set(row.get("outputs") or [])):
            errors.append("IF-PREP-RECOVER is missing target or successor confirmation output")
        if row.get("id") == "IF-PRED-OBS" and "currentlyValidNonemptyClasses" not in " ".join(str(item) for item in (row.get("outputs") or [])):
            errors.append("IF-PRED-OBS is missing currently valid classes")
        if row.get("id") == "IF-SELECT-ADMIT" and "currentlyValidNonemptyClasses" not in " ".join(str(item) for item in (row.get("inputs") or [])):
            errors.append("IF-SELECT-ADMIT is missing predicted classes as input")
    handles = spec.get("sessionHandles") or {}
    if "HistoryHandle" not in handles or "SessionContext" not in handles:
        errors.append("CL-TAV registry is missing SessionContext or HistoryHandle")
    macros = {row.get("macro"): row.get("id") for row in interfaces if isinstance(row, dict) and row.get("macro")}
    called = set(re.findall(r"\\(IF[a-z]+)", corpus_bodies))
    for row in interfaces:
        if not isinstance(row, dict) or row.get("calledInAlgorithm") is not True:
            continue
        contract_id = row.get("id")
        macro = row.get("macro")
        if macro and macro not in called:
            errors.append(f"presentation algorithms do not call {contract_id}")
        if contract_id and contract_id not in corpus:
            errors.append(f"algorithm package is missing {contract_id}")
        if contract_id and contract_id not in experiment_puml:
            errors.append(f"experiment architecture view is missing {contract_id}")
        if contract_id and contract_id not in experiment_plan:
            errors.append(f"experiment plan is missing {contract_id}")
    declared = {row.get("id") for row in interfaces if isinstance(row, dict)} | {
        row.get("id") for row in experiment_ifs if isinstance(row, dict)
    }
    for token in sorted(set(re.findall(r"IF-[A-Z0-9-]+", corpus + "\n" + experiment_puml + "\n" + experiment_plan))):
        if token not in declared:
            errors.append(f"undeclared interface call {token}")
    for token in sorted(set(re.findall(r"IF-[A-Z0-9-]+", corpus_bodies))):
        if token not in declared:
            errors.append(f"undeclared interface call {token}")
    if "HistoryHandle" not in corpus and r"\eta" not in corpus:
        errors.append("algorithm package is missing HistoryHandle")
    errors.extend(_cltav_presentation_errors(algorithms, main_body))
    errors.extend(_cltav_executable_errors(algorithms))
    dataflow = spec.get("dataflow") or []
    if not any(row.get("from") == "IF-PRED-OBS" and row.get("to") == "IF-SELECT-ADMIT" for row in dataflow):
        errors.append("registry is missing predict-to-select dataflow")
    if not any(row.get("from") == "IF-HIST-UPDATE" and row.get("nextIteration") for row in dataflow):
        errors.append("registry is missing history-to-next-prediction dataflow")
    for exp_id in spec.get("experimentIds") or CLTAV_EXPERIMENT_IDS:
        if exp_id not in experiment_puml:
            errors.append(f"experiment architecture view is missing {exp_id}")
        if exp_id not in experiment_plan:
            errors.append(f"experiment plan is missing {exp_id}")
    for exp_if in experiment_ifs:
        if not isinstance(exp_if, dict):
            continue
        exp_id = exp_if.get("id")
        missing = [field for field in ("id", "inputs", "outputs", "failure") if not exp_if.get(field)]
        if missing:
            errors.append(f"{exp_id} is missing {missing[0]}")
        if exp_id and exp_id not in experiment_plan:
            errors.append(f"experiment plan is missing {exp_id}")
    denominators = spec.get("denominators") or []
    if not denominators:
        errors.append("registry is missing denominator definitions")
    for name in denominators:
        if name not in experiment_plan:
            errors.append(f"experiment plan is missing denominator {name}")
    if "evaluator-only" not in experiment_puml:
        errors.append("experiment architecture view is missing evaluator-only")
    if "forbidden leakage" not in experiment_puml:
        errors.append("experiment architecture view is missing forbidden leakage")
    for source, target, line in _puml_edges(experiment_puml):
        if source == "Truth" and target == "Arms" and "forbidden" not in line:
            errors.append("experiment architecture view must not give evaluator truth to comparison arms")
        if source == "Truth" and any(item in line for item in (spec.get("forbiddenTruthInputs") or [])):
            if "forbidden" not in line and "never" not in line:
                errors.append("evaluator truth must not enter a select/predict/history/execute input")
    if "Truth --> Arms" in experiment_puml and "forbidden" not in experiment_puml:
        errors.append("experiment architecture view must not give evaluator truth to comparison arms")
    walks = spec.get("recordFlowWalkthroughs") or []
    if len(walks) < 5:
        errors.append("registry is missing experiment record-flow walkthroughs")
    all_ids = [row.get("id") for row in list(interfaces) + list(experiment_ifs) if isinstance(row, dict)]
    if None in all_ids or "" in all_ids:
        errors.append("CL-TAV interface registry contains an interface without id")
    if len(list(filter(None, all_ids))) != len(set(filter(None, all_ids))):
        errors.append("CL-TAV interface registry contains duplicate interface ids")
    endpoints = _registry_endpoints(spec)
    for edge in dataflow:
        if not isinstance(edge, dict):
            continue
        src, dst = edge.get("from"), edge.get("to")
        output, incoming = edge.get("output"), edge.get("input")
        if src not in endpoints:
            errors.append(f"dataflow source {src} is not a declared interface or session handle")
            continue
        if dst not in endpoints:
            errors.append(f"dataflow destination {dst} is not a declared interface or session handle")
            continue
        if output not in endpoints[src]["outputs"]:
            errors.append(f"dataflow output {output} is not a port of {src}")
        if incoming not in endpoints[dst]["inputs"]:
            errors.append(f"dataflow input {incoming} is not a port of {dst}")
    exp_by_id = {row.get("id"): row for row in experiment_ifs if isinstance(row, dict)}
    for walk in walks:
        if not isinstance(walk, dict):
            continue
        walk_id = walk.get("id")
        if walk.get("truthToSelect") is True:
            errors.append(f"{walk_id} must not mark truthToSelect")
        for token in walk.get("path") or []:
            if token not in declared:
                errors.append(f"{walk_id} walk path cites undeclared interface {token}")
        records = walk.get("records")
        if not isinstance(records, dict) or not records:
            errors.append(f"{walk_id} is missing required typed records")
            continue
        filter_needed = _variant_inputs(exp_by_id.get("IF-EXP-FILTER") or {}, walk.get("filterVariant") or "run-completed")
        eval_needed = _variant_inputs(exp_by_id.get("IF-EXP-EVAL") or {}, walk.get("evalVariant") or "run-completed")
        filter_rec = records.get("filterInput") or {}
        eval_rec = records.get("evalInput") or {}
        for field in filter_needed:
            if field not in filter_rec:
                errors.append(f"{walk_id} filter record is missing {field}")
        for field in eval_needed:
            if field not in eval_rec:
                errors.append(f"{walk_id} eval record is missing {field}")
        dens = walk.get("denominators")
        if not isinstance(dens, list) or "attempt" not in dens:
            errors.append(f"{walk_id} must record attempt plus membership denominators")
    errors.extend(_algorithm_effect_errors(
        corpus, dataflow, interfaces, handles.get("SessionContext") or {},
        main_algorithm=main_text,
    ))
    return errors


def _algorithm_effect_errors(
    algorithm: str, dataflow: list, interfaces: list, session_context: dict | None = None,
    main_algorithm: str | None = None,
) -> list[str]:
    """Select-time snapshot, successor summaries, and effect classes match the delivered S steps.

    ``algorithm`` is the whole decomposed package; ``main_algorithm`` is the
    top-level file whose body carries the loop order.
    """
    errors: list[str] = []
    body = _algorithm_bodies(algorithm)
    main_body = _algorithm_bodies(main_algorithm) if main_algorithm is not None else body
    if "CONFIRMED-NOT-SENT" not in body or "UNKNOWN-EFFECT" not in body:
        errors.append("main algorithm must distinguish CONFIRMED-NOT-SENT from UNKNOWN-EFFECT")
    if "sole writer" not in body:
        errors.append("main algorithm must name the sole writer of KNOWN")
    if "qUsedAtSelect" not in main_body:
        errors.append("top-level algorithm must freeze qUsedAtSelect in the select snapshot")
    if "\\IFexec" not in body:
        errors.append("algorithm package must call IF-EXECUTE-RECORD")
    freeze_at = main_body.find("SelectSnapshot")
    exec_at = main_body.find("ExecuteAndRecord")
    if freeze_at < 0 or exec_at < 0 or freeze_at > exec_at:
        errors.append("select snapshot must be frozen before IF-EXECUTE-RECORD")
    if "one-step minimax" not in body:
        errors.append("the selection contract must name the one-step minimax rule")
    select_at = main_body.find("SelectAndAdmit")
    action_at = main_body.find("actionId")
    if select_at < 0 or action_at < 0 or select_at > action_at:
        errors.append("SelectSnapshot.actionId must be frozen only after final TEST minimax selection")
    if "t^\\star\\leftarrow" in main_body:
        errors.append("main algorithm must not replace tStar after IF-SELECT-ADMIT")
    match = re.search(r"\\IFhist\$\((.*?)\)\$", body, re.S)
    hist_call = match.group(1) if match else ""
    if "qUsedAtSelect" not in hist_call or "postSummary" not in hist_call:
        errors.append("IF-HIST-UPDATE must receive qUsedAtSelect and postSummary")
    if "qStatus" in hist_call:
        errors.append("IF-HIST-UPDATE must not receive live qStatus")
    marker = "\\texttt{CONFIRMED-NOT-SENT}$}"
    at = body.find(marker)
    window = body[at:at + 220] if at >= 0 else ""
    if "unchanged" not in window:
        errors.append("CONFIRMED-NOT-SENT must leave q unchanged")
    if any(
        isinstance(row, dict) and row.get("from") == "SessionContext" and row.get("input") == "qUsedAtSelect"
        for row in dataflow
    ):
        errors.append("qUsedAtSelect must not be wired from live SessionContext")
    if not any(
        isinstance(row, dict)
        and row.get("from") == "SelectSnapshot"
        and row.get("output") == "qUsedAtSelect"
        and row.get("to") == "IF-HIST-UPDATE"
        for row in dataflow
    ):
        errors.append("registry must pass SelectSnapshot.qUsedAtSelect into IF-HIST-UPDATE")
    if not any(
        isinstance(row, dict)
        and row.get("from") == "IF-SELECT-ADMIT"
        and row.get("output") == "tStar"
        and row.get("to") == "SelectSnapshot"
        and row.get("input") == "actionId"
        for row in dataflow
    ):
        errors.append("registry must freeze IF-SELECT-ADMIT final tStar as SelectSnapshot.actionId")
    if not any(
        isinstance(row, dict)
        and row.get("from") == "SelectSnapshot"
        and row.get("output") == "actionId"
        and row.get("to") == "IF-EXECUTE-RECORD"
        for row in dataflow
    ):
        errors.append("registry must execute SelectSnapshot.actionId")
    fields = set((session_context or {}).get("fields") or [])
    if not {"qStatus", "currentSummary"}.issubset(fields):
        errors.append("SessionContext must distinguish qStatus from currentSummary")
    if "\\Gamma.\\mathrm{currentSummary}" not in body:
        errors.append("main algorithm must read and commit currentSummary")
    if not any(
        isinstance(row, dict)
        and row.get("from") == "SessionContext"
        and row.get("output") == "currentSummary"
        and row.get("to") == "IF-SELECT-ADMIT"
        and row.get("input") == "q"
        for row in dataflow
    ):
        errors.append("registry must feed currentSummary to IF-SELECT-ADMIT")
    for producer in ("IF-OBS-INTERPRET", "IF-PREP-RECOVER"):
        if not any(
            isinstance(row, dict)
            and row.get("from") == producer
            and row.get("output") == "postSummary"
            and row.get("to") == "SessionContext"
            and row.get("input") == "currentSummary"
            and row.get("appliedBy") == "S9-sole-commit"
            for row in dataflow
        ):
            errors.append(f"registry must commit {producer} postSummary through S9")
    obs = next((row for row in interfaces if isinstance(row, dict) and row.get("id") == "IF-OBS-INTERPRET"), {})
    if not {"summaryConfirmed", "postSummary"}.issubset(set(obs.get("outputs") or [])):
        errors.append("IF-OBS-INTERPRET must return summaryConfirmed and postSummary")
    if "\\IFobs" not in body or "\\mathrm{verdict}=\\mathrm{INCONCLUSIVE}" not in body:
        errors.append("the timed-observation contract must call IF-OBS-INTERPRET and apply the T5 interval verdict")
    prep = next((row for row in interfaces if isinstance(row, dict) and row.get("id") == "IF-PREP-RECOVER"), {})
    prep_outputs = set(prep.get("outputs") or [])
    if not {"targetConfirmed", "summaryConfirmed", "postSummary"}.issubset(prep_outputs):
        errors.append("IF-PREP-RECOVER must distinguish targetConfirmed from summaryConfirmed")
    if "summaryConfirmed=false" not in str(prep.get("failure") or ""):
        errors.append("IF-PREP-RECOVER must classify an unconfirmed Prep successor summary")
    prep_escape = "($z.\\mathrm{kind}$ is Prep and $z.\\mathrm{prepResultEvaluated}$ and $z.\\mathrm{summaryConfirmed}$ is false)"
    if body.count(prep_escape) < 2:
        errors.append("unconfirmed Prep successor summary must enter S7")
    if "CONFIRMED-NOT-SENT" not in body or "prepResultEvaluated" not in body:
        errors.append("CONFIRMED-NOT-SENT must bypass unevaluated Prep confirmation")
    compact = re.sub(r"\s+", "", body)
    commit_guard = r"$z.\mathrm{summaryConfirmed}$istrue"
    commit_assign = r"\Gamma'.\mathrm{currentSummary}\leftarrowz.\mathrm{postSummary}"
    if commit_guard not in compact or commit_assign not in compact:
        errors.append("S9 must commit currentSummary only under the confirmed KNOWN successor guard")
    if "does not write" not in str(prep.get("stateEffect") or ""):
        errors.append("IF-PREP-RECOVER must not write session state")
    return errors


def _registry_endpoints(spec: dict) -> dict[str, dict[str, list[str]]]:
    endpoints: dict[str, dict[str, list[str]]] = {}
    for key, row in (spec.get("sessionHandles") or {}).items():
        if not isinstance(row, dict):
            continue
        fields = [str(item) for item in (row.get("fields") or [])]
        endpoints[str(row.get("id") or key)] = {"inputs": fields, "outputs": fields}
    for row in list(spec.get("interfaces") or []) + list(spec.get("experimentInterfaces") or []):
        if not isinstance(row, dict) or not row.get("id"):
            continue
        endpoints[str(row["id"])] = {
            "inputs": [str(item) for item in (row.get("inputs") or [])],
            "outputs": [str(item) for item in (row.get("outputs") or [])],
        }
    return endpoints


def _variant_inputs(iface: dict, when: str) -> list[str]:
    for variant in iface.get("inputVariants") or []:
        if isinstance(variant, dict) and variant.get("when") == when:
            return [str(item) for item in (variant.get("inputs") or [])]
    return [str(item) for item in (iface.get("inputs") or [])]


def expected_download_mode(clause: str) -> str:
    """Media Defined and Operator Defined DOWNLOAD stay separate after reread."""
    if clause.startswith(("5.4.4.1", "6.2.10", "6.4.6")) or clause == "6.3.3":
        return "MEDIA-DEFINED"
    if clause.startswith(("5.4.4.2", "6.2.14", "6.2.15", "6.2.16", "6.4.8", "6.4.9")) or clause == "6.3.4":
        return "OPERATOR-DEFINED"
    if clause.startswith("5.4.4.3"):
        return "MEDIA-ORGANIZATION"
    return "SHARED"


def source_reread_errors(audit: dict) -> list[str]:
    """FIND/DOWNLOAD/AFDX reread candidates. Generated codes may rewrite the bound package."""
    errors: list[str] = []
    reread = audit.get("sourceReread")
    status = audit.get("status")
    if status in {"SOURCE-UNIT-AUDIT-IN-PROGRESS", "PARTIAL-CRS-GENERATION-IN-PROGRESS"} and not isinstance(reread, dict):
        errors.append("source-unit audit in progress must record sourceReread")
        return errors
    if reread is None:
        return errors
    if not isinstance(reread, dict):
        errors.append("sourceReread must be an object")
        return errors
    if reread.get("requirementGenerationAllowed") is not False:
        errors.append("sourceReread must not allow requirement generation")
    generated_codes = {code for code in (reread.get("generatedCodes") or []) if isinstance(code, str)}
    unknown_generated = generated_codes - set(DEFERRED_AUDIT_CODES)
    if unknown_generated:
        errors.append("sourceReread generatedCodes contains an undeclared deferred rationale")
    if generated_codes:
        if reread.get("doesNotRewriteBoundPackage") is not False:
            errors.append("sourceReread must record bound-package rewrite after generated codes")
    elif reread.get("doesNotRewriteBoundPackage") is not True:
        errors.append("sourceReread must not rewrite the bound package")
    if reread.get("proprietaryTextExcluded") is not True:
        errors.append("sourceReread must exclude proprietary source text")
    deferred = audit.get("deferredUnits") or {}
    generated_ids_by_code = reread.get("generatedUnitIdsByCode") or {}
    units = reread.get("units")
    if not isinstance(units, list):
        errors.append("sourceReread units must be a list")
        return errors
    recorded_ids = [item.get("id") if isinstance(item, dict) else None for item in units]
    if None in recorded_ids or "" in recorded_ids:
        errors.append("sourceReread contains a row without id")
    if len(list(filter(None, recorded_ids))) != len(set(filter(None, recorded_ids))):
        errors.append("sourceReread contains duplicate coverage ids")
    if reread.get("unitsRead") != len(units):
        errors.append("sourceReread unitsRead does not match recorded units")
    completed = [code for code in (reread.get("completedCodes") or []) if isinstance(code, str)]
    current = reread.get("scopeThisIncrement")
    active = [
        code
        for code in completed + [current]
        if isinstance(code, str) and code and code in DEFERRED_AUDIT_CODES
    ]
    pending = set(reread.get("pendingCodes") or [])
    recorded_codes = {
        item.get("frozenRationaleCode")
        for item in units
        if isinstance(item, dict) and item.get("frozenRationaleCode")
    }
    if set(active) != recorded_codes:
        errors.append("sourceReread completed/current codes do not match recorded rationale codes")
    if pending & recorded_codes:
        errors.append("sourceReread pendingCodes must not include recorded codes")
    if generated_codes - recorded_codes:
        errors.append("sourceReread generatedCodes must be a subset of recorded rationale codes")
    for code in sorted(recorded_codes):
        got_ids = [
            item.get("id")
            for item in units
            if isinstance(item, dict) and item.get("frozenRationaleCode") == code
        ]
        if code in generated_codes:
            expected_ids = generated_ids_by_code.get(code) or []
            if not isinstance(expected_ids, list):
                errors.append(f"{code} generated inventory must be a list")
                continue
            if set(filter(None, got_ids)) != set(filter(None, expected_ids)):
                errors.append(f"{code} sourceReread IDs do not match generated inventory")
            if len(got_ids) != len(expected_ids):
                errors.append(f"{code} sourceReread unit count does not match generated inventory")
            continue
        expected_ids = [row.get("id") for row in deferred.get(code) or [] if isinstance(row, dict)]
        if set(filter(None, got_ids)) != set(filter(None, expected_ids)):
            errors.append(f"{code} sourceReread IDs do not match deferred units")
        if len(got_ids) != len(expected_ids):
            errors.append(f"{code} sourceReread unit count does not match deferred units")
    for item in units:
        if not isinstance(item, dict):
            errors.append("sourceReread contains a non-object row")
            continue
        missing = [field for field in SOURCE_REREAD_UNIT_FIELDS if field not in item]
        if missing:
            errors.append(f"sourceReread row {item.get('id')} is missing {missing[0]}")
            continue
        if item.get("frozenApplicabilityDecision") != "DEFERRED-FUTURE-SCOPE":
            errors.append(f"sourceReread row {item.get('id')} must keep frozen DEFERRED-FUTURE-SCOPE")
        if item.get("candidateApplicability") not in SOURCE_REREAD_APPLICABILITY:
            errors.append(f"sourceReread row {item.get('id')} has an undeclared candidateApplicability")
        if item.get("frozenSourceModality") == "COMMENTARY" and item.get("candidateApplicability") != "NON-NORMATIVE":
            errors.append(f"sourceReread row {item.get('id')} must not promote commentary")
        if not isinstance(item.get("objects"), list) or not item.get("objects"):
            errors.append(f"sourceReread row {item.get('id')} must list objects")
        if not item.get("actor") or not item.get("action"):
            errors.append(f"sourceReread row {item.get('id')} must record actor and action")
        if item.get("frozenRationaleCode") == "DEFERRED-DOWNLOAD-M9":
            mode = item.get("downloadMode")
            if mode not in SOURCE_REREAD_DOWNLOAD_MODES:
                errors.append(f"sourceReread row {item.get('id')} must declare a DOWNLOAD mode")
            elif mode != expected_download_mode(str(item.get("clause") or "")):
                errors.append(f"sourceReread row {item.get('id')} must not mix Media Defined and Operator Defined DOWNLOAD")
        if item.get("frozenRationaleCode") == AFDX_RATIONALE:
            if item.get("deploymentVariant") != "AFDX":
                errors.append(f"sourceReread row {item.get('id')} must declare the AFDX deployment variant")
            if item.get("candidateApplicability") == AFDX_UNCONDITIONAL_APPLICABILITY:
                errors.append(
                    f"sourceReread row {item.get('id')} must not treat AFDX appendix as the current Compliant instance"
                )
    return errors


def cltav_sysml_errors(models: dict[str, str]) -> list[str]:
    """File and marker completeness for notation-based views.

    Semantic admission, ERROR and stop-class behavior is checked by
    scripts/cltav_loop_spec.py walk-throughs, not by natural-language regex.
    """
    errors: list[str] = []
    for name in CLTAV_PUML_FILES:
        text = models.get(name, "")
        if not text:
            errors.append(f"missing CL-TAV SysML source: {name}")
            continue
        if SYSML_NOTATION_MARK not in text:
            errors.append(f"{name} must declare SysML 1.6 notation-based views")
    activity = models.get("FIG-CL-TAV-05-closed-loop-activity.puml", "")
    for token in (
        "admissible",
        "XOR",
        "Hk",
        "Prep",
        "ERROR",
        "ErrorHandle",
        "unknown-effect",
        "confirmed not sent",
        "Charge cost once",
        "strictly-reducing",
        "selectable",
        "A1",
        "A5",
        "unconfirmed",
        "P1",
        "P5",
        "Stop-Budget",
        "Stop-NoDistinguisher",
        "Stop-Equivalent",
        "Stop-Singleton",
        "Stop-Empty",
        "Stop-Error",
        "Stop-645",
        "cmin",
        "Kmax",
    ):
        if token not in activity:
            errors.append(f"closed-loop activity view is missing {token}")
    if "if (A empty?)" in activity and "S empty" not in activity:
        errors.append("closed-loop activity view must not Execute from nonempty A without selectable S")
    machines = models.get("FIG-CL-TAV-07-two-state-machines.puml", "")
    for token in ("Msess", "Mprot", "Admit", "ErrorHandle", "bound M2", "FIG-CL-TAV-04", "FIND", "P1", "P5", "A1", "A5", "unconfirmed", "retry remaining"):
        if token not in machines:
            errors.append(f"two-machine view is missing {token}")
    if "Information -->" in machines:
        errors.append("two-machine view must not draw unaudited Information to other-operation edges")
    if re.search(r"Msess\s+-->\s+Mprot", machines):
        errors.append("two-machine view must not use a cross-machine state transition")
    if "Execute --> StopError" in machines:
        errors.append("two-machine view must not stop immediately on every ERROR")
    if "retry cap or Recover not admissible" in machines:
        errors.append("two-machine view must not stop on Recover-not-admissible except under unknown-effect")
    if "ErrorHandle --> Admit : unknown-effect and Recover in S" in machines:
        errors.append("two-machine view must not Admit unknown-effect Recover without retry remaining")
    if "RecoverConfirm --> StopBudget : unconfirmed A5" in machines or "RecoverConfirm --> StopError : unconfirmed A4" in machines:
        errors.append("two-machine view must not overlap unconfirmed Recover stop with return to Admit")
    parametric = models.get("FIG-CL-TAV-08-parametric.puml", "")
    for token in ("cmin", "Kmax", "Hk"):
        if token not in parametric:
            errors.append(f"parametric view is missing {token}")
    sequence = models.get("FIG-CL-TAV-06-diagnostic-sequence.puml", "")
    if "Prep" not in sequence or "overlapping" not in sequence:
        errors.append("diagnostic sequence view must show overlapping observation and Prep")
    experiment = models.get("FIG-CL-TAV-09-experiment-architecture.puml", "")
    for token in (
        "evaluator-only",
        "forbidden leakage",
        "IF-SELECT-ADMIT",
        "CL-T / CL-A / CL-TA / CL-LOOP",
        "DETECT / LOCATE / ABLATION",
    ):
        if token not in experiment:
            errors.append(f"experiment architecture view is missing {token}")
    if "Truth --> Arms" in experiment and "forbidden" not in experiment:
        errors.append("experiment architecture view must not give evaluator truth to comparison arms")
    if "Izk of tb" not in sequence:
        errors.append("diagnostic sequence view must send the second observation to Analysis")
    layers = models.get("FIG-CL-TAV-02-requirement-layers.puml", "")
    if "CRS-M1-00365" not in layers:
        errors.append("requirement-layer view must include the representative source-to-CRS trace")
    return errors


def _load_figure_graphs() -> dict:
    if not CLTAV_FIGURE_GRAPHS_PATH.is_file():
        return {}
    try:
        return json.loads(CLTAV_FIGURE_GRAPHS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _svg_labeled_edges(root: ET.Element) -> list[tuple[str, str, float, float, float, float]]:
    edges: list[tuple[str, str, float, float, float, float]] = []
    for elem in root.iter():
        if elem.tag.split("}")[-1] != "line":
            continue
        src, dst = elem.get("data-from"), elem.get("data-to")
        if not src or not dst:
            continue
        try:
            edges.append((
                src,
                dst,
                float(elem.get("x1") or 0),
                float(elem.get("y1") or 0),
                float(elem.get("x2") or 0),
                float(elem.get("y2") or 0),
            ))
        except ValueError:
            continue
    return edges


def _point_in_node(x: float, y: float, node: dict, pad: float = 8) -> bool:
    left = float(node.get("x") or 0) - pad
    top = float(node.get("y") or 0) - pad
    right = float(node.get("x") or 0) + float(node.get("w") or 0) + pad
    bottom = float(node.get("y") or 0) + float(node.get("h") or 0) + pad
    return left <= x <= right and top <= y <= bottom


def _figure_graph_errors(name: str, root: ET.Element) -> list[str]:
    graphs = (_load_figure_graphs().get("figures") or {}).get(name)
    if not isinstance(graphs, dict):
        return []
    errors: list[str] = []
    nodes = graphs.get("nodes") or {}
    required = {(row.get("from"), row.get("to")) for row in (graphs.get("edges") or []) if isinstance(row, dict)}
    found = _svg_labeled_edges(root)
    found_pairs = {(src, dst) for src, dst, *_ in found}
    for pair in sorted(required):
        if pair not in found_pairs:
            errors.append(f"{name} is missing structural edge {pair[0]}->{pair[1]}")
    if name == "FIG-CL-TAV-09-experiment-architecture.svg":
        if ("Valid", "Metrics") not in found_pairs:
            errors.append(f"{name} must connect Valid to Metrics")
        if ("Obs", "Metrics") in found_pairs:
            errors.append(f"{name} must not bypass validity: Obs must not connect directly to Metrics")
        valid = nodes.get("Valid") or {}
        for src, dst, x1, y1, _x2, _y2 in found:
            if dst == "Metrics" and valid and not _point_in_node(x1, y1, valid):
                errors.append(f"{name} Metrics inbound edge does not start in the Valid box")
        visible = _svg_visible_text(root)
        for key, node in nodes.items():
            label = str((node or {}).get("label") or "")
            if label and label not in visible:
                errors.append(f"{name} node {key} label is truncated or missing")
    if name == "FIG-CL-TAV-05-closed-loop-activity.svg":
        for pair in (("Unconfirmed", "S7"), ("S7", "LoopS1"), ("LoopS1", "S1")):
            if pair not in found_pairs:
                errors.append(f"{name} is missing retry/unconfirmed back-edge {pair[0]}->{pair[1]}")
        errors.extend(_figure05_control_errors(graphs, found_pairs, root))
    return errors


FIG05_CONTROL_EDGES = (
    {"id": "E-S10-S1", "from": "S10", "to": "S1", "polarity": "continue", "guard": "no stop"},
    {"id": "E-S9-S10", "from": "S9", "to": "S10", "polarity": "advance"},
    {"id": "E-S1-STOP", "from": "S1", "to": "StopGate", "polarity": "stop", "guard": "already decided"},
    {"id": "E-S2-GAP", "from": "S2", "to": "PredictionGap", "polarity": "stop", "guard": "Recover and Prep ineligible"},
    {"id": "E-S7-S1", "from": "S7", "to": "S1", "polarity": "retry", "via": ("LoopS1",)},
)


def _svg_visible_text(root: ET.Element) -> str:
    chunks: list[str] = []
    for elem in root.iter():
        if elem.tag.split("}")[-1] != "text":
            continue
        parts = [elem.text or ""]
        parts.extend((child.text or "") for child in list(elem))
        chunks.append(" ".join(part.strip() for part in parts if part and part.strip()))
    return "\n".join(chunks)


def _figure05_control_errors(graphs: dict, found_pairs: set[tuple[str, str]], root: ET.Element) -> list[str]:
    """Bounded decision table. JSON/SVG agreement alone is not the control authority."""
    errors: list[str] = []
    edges = [row for row in (graphs.get("edges") or []) if isinstance(row, dict)]
    by_id = {row.get("id"): row for row in edges}
    by_pair = {(row.get("from"), row.get("to")): row for row in edges}
    puml_path = RESEARCH / "publication" / "models" / "FIG-CL-TAV-05-closed-loop-activity.puml"
    puml = puml_path.read_text(encoding="utf-8") if puml_path.is_file() else ""
    visible = _svg_visible_text(root)
    for spec in FIG05_CONTROL_EDGES:
        edge_id = spec["id"]
        if edge_id not in puml:
            errors.append(f"FIG-05 PlantUML is missing control id {edge_id}")
        row = by_id.get(edge_id)
        via = spec.get("via") or ()
        if via:
            hops = [spec["from"], *via, spec["to"]]
            for src, dst in zip(hops, hops[1:]):
                if (src, dst) not in by_pair:
                    errors.append(f"FIG-05 is missing retry hop {src}->{dst}")
                if (src, dst) not in found_pairs:
                    errors.append(f"FIG-05 SVG is missing retry hop {src}->{dst}")
            if row is None:
                errors.append(f"FIG-05 control table is missing {edge_id}")
            elif row.get("polarity") != spec["polarity"]:
                errors.append(f"{edge_id} polarity inverted")
        else:
            pair = (spec["from"], spec["to"])
            if row is None or (row.get("from"), row.get("to")) != pair:
                errors.append(f"FIG-05 control edge {edge_id} must be {pair[0]}->{pair[1]}")
            elif row.get("polarity") != spec["polarity"]:
                errors.append(f"{edge_id} polarity inverted")
            if pair not in found_pairs:
                errors.append(f"FIG-05 SVG is missing {pair[0]}->{pair[1]}")
        guard = spec.get("guard")
        if guard and guard not in visible:
            errors.append(f"FIG-05 visible text is missing guard {guard}")
    if ("S10", "S1") not in by_pair:
        errors.append("FIG-05 is missing the normal S10->S1 continue edge")
    if ("S9", "S10") not in by_pair or ("S10", "S1") not in by_pair:
        errors.append("FIG-05 S9 without a stop must be able to reach the next S1")
    for key, node in (graphs.get("nodes") or {}).items():
        label = str(node.get("label") or "")
        if label and label not in visible:
            errors.append(f"FIG-05 node {key} label is truncated or missing")
    return errors


def cltav_figure_errors() -> list[str]:
    """Reader SVG completeness, labeled structural edges, and XML-valid edges."""
    errors: list[str] = []
    critical = {
        "FIG-CL-TAV-01-context.svg",
        "FIG-CL-TAV-05-closed-loop-activity.svg",
        "FIG-CL-TAV-09-experiment-architecture.svg",
    }
    for name in CLTAV_SVG_FILES:
        path = CLTAV_SVG_DIR / name
        if not path.is_file():
            errors.append(f"missing CL-TAV reader figure: {name}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        head = text[:400].lstrip().lower()
        if "<svg" not in head:
            errors.append(f"{name} is not an SVG document")
        if "bad url" in text.lower() or "huffman" in text.lower():
            errors.append(f"{name} is a renderer error page, not a figure")
        for comment in re.findall(r"<!--(.*?)-->", text, re.S):
            if "--" in comment:
                errors.append(f"{name} XML comment contains '--'")
                break
        if name not in critical:
            continue
        try:
            root = ET.fromstring(text)
        except ET.ParseError as exc:
            errors.append(f"{name} is not well-formed XML: {exc}")
            continue
        tags = {elem.tag.split("}")[-1] for elem in root.iter()}
        if not (tags & {"line", "polyline", "path", "polygon"}):
            errors.append(f"{name} has no visible connecting edges")
        if name == "FIG-CL-TAV-05-closed-loop-activity.svg":
            blob = ET.tostring(root, encoding="unicode").lower()
            for token in ("error", "recover", "predict", "select"):
                if token not in blob:
                    errors.append(f"{name} is missing visible {token} control-flow")
        errors.extend(_figure_graph_errors(name, root))
    if not READER_ALG_PDF.is_file():
        errors.append("missing reader typeset algorithm PDF")
    wrapper = (RESEARCH / "publication" / "algorithms" / "ALG-CLTAV-01-wrapper.tex").read_text(encoding="utf-8")
    if "Lines 27--29" in wrapper or "Lines 15--18" in wrapper:
        errors.append("algorithm Chinese mapping still cites stale typeset line numbers")
    if "S0" not in wrapper or "S10" not in wrapper:
        errors.append("algorithm Chinese mapping must use stable step labels")
    return errors


def cltav_outline_errors(outline_text: str) -> list[str]:
    """Each thesis chapter must carry claim, question, algorithm/architecture, and evidence."""
    errors: list[str] = []
    if ZH_MARKER not in outline_text:
        return ["research outline is missing the Chinese boundary"]
    english, chinese = outline_text.split(ZH_MARKER, 1)
    if english.count("- **Claim:**") != 8 or chinese.count("- **论点：**") != 8:
        errors.append("research outline must state a claim for each of the eight chapters")
    if english.count("- **Answers:**") != 8 or chinese.count("- **回答：**") != 8:
        errors.append("research outline must map each chapter to a research question")
    if english.count("- **Uses:**") != 8 or chinese.count("- **使用：**") != 8:
        errors.append("research outline must name the algorithm or architecture each chapter uses")
    if english.count("- **Needs:**") != 8 or chinese.count("- **需要：**") != 8:
        errors.append("research outline must name the experiment or evidence each chapter needs")
    for fig in range(1, 9):
        fig_id = f"FIG-CL-TAV-0{fig}"
        if fig_id not in english or fig_id not in chinese:
            errors.append(f"research outline is missing {fig_id}")
    if "M_{\\mathrm{sess}}" not in english or "M_{\\mathrm{prot}}" not in english:
        errors.append("research outline must distinguish the verification-session and protocol-operation machines")
    if "c_{\\min}" not in english or "K_{\\max}" not in english:
        errors.append("research outline must state the finite-termination rule")
    outline_dir = RESEARCH / "publication"
    for raw in LINK_RE.findall(outline_text):
        href = raw.split()[0]
        if href.startswith("#") or "://" in href:
            continue
        target = (outline_dir / href).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"research outline link escapes the repository: {href}")
            continue
        if not target.exists():
            errors.append(f"research outline link is missing: {href}")
    return errors


def validate_gvs_binding(errors: list[str]) -> None:
    binding = read(EXTERNAL_BINDING_PATH)
    required_binding_values = (
        "TMP-XRB-ARINC615A-01",
        "TMP-ARINC615A-01",
        "TMP-CTP-ARINC615A-01",
        "TMP-PB-ARINC615A-01",
        "TMP-PC-ARINC615A-01",
        METHOD_DEFINITION_COMMIT,
        METHOD_DISPOSITION_COMMIT,
        METHOD_APPROVED_HEAD,
        ARINC_V43_RELEASE_COMMIT,
        ARINC_V43_RELEASE_TAG,
        ACK_BASELINE_ID,
        ACK_DISPOSITION,
        EVALUATION_STATUS,
        CONFIGURATION_STATUS,
    )
    for value in required_binding_values:
        if value not in binding:
            errors.append(f"external GVS binding is missing controlled value: {value}")

    if re.search(
        r"complex-system-verification-assurance/(?:blob|tree)/(?:main|master|latest)(?:/|$)",
        binding,
        re.IGNORECASE,
    ):
        errors.append("external GVS binding uses a mutable method-repository locator")
    if MACHINE_LOCAL_RE.search(binding):
        errors.append("external GVS binding contains a machine-local path")
    if "196cfc" in binding:
        errors.append("external GVS binding uses the pre-merge method parent 196cfc")

    # Every occurrence of the method SHA in controlled documentation must sit
    # in an explicit external method-definition/binding context.
    context_terms = (
        "methoddefinitioncommit", "candidate gvs core", "external method",
        "method commit", "method merge", "method pr", "method object", "methodology baseline",
        "commit-bound locator", "instance registry", "instance_registry", "方法提交", "方法合并", "方法 pr", "方法对象", "外部 core",
        "外部方法", "candidate gvs core", "methoddefinitioncommit",
    )
    for source in ROOT.rglob("*.md"):
        if "local-references" in source.parts:
            continue
        lines = read(source).splitlines()
        for index, line in enumerate(lines):
            if METHOD_DEFINITION_COMMIT not in line:
                continue
            window = " ".join(lines[max(0, index - 2): index + 3]).lower()
            if not any(term in window for term in context_terms):
                errors.append(
                    "method SHA lacks explicit method-definition context: "
                    f"{source.relative_to(ROOT)}:{index + 1}"
                )


def _mapping_language_review_rows(
    section: str, language: str, errors: list[str],
) -> dict[str, tuple[str, str, str]]:
    """Parse relation, status, and Review for every controlled mapping row."""
    rows: dict[str, tuple[str, str, str]] = {}
    expected_ids = set(METHOD_MAPPING_EXPECTED) | set(INSTANCE_ADDITIONAL_EXPECTED)
    for line in section.splitlines():
        match = re.match(r"^\| ([RA]\d{2}) \|", line)
        if not match:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        row_id = match.group(1)
        expected_columns = 10 if row_id.startswith("R") else 11
        if len(cells) != expected_columns:
            errors.append(
                f"{language} mapping row {row_id} must have {expected_columns} columns"
            )
            continue
        relation_index, status_index = ((4, 5) if row_id.startswith("R") else (5, 6))
        relation = cells[relation_index].strip("`")
        status = cells[status_index].strip("`")
        review = cells[-1]
        if row_id in rows:
            errors.append(f"duplicate {language} mapping review row: {row_id}")
        rows[row_id] = (relation, status, review)

        normalized_review = review.replace("～", "–")
        if review.strip().lower() == "pending" or review.strip() == "待审":
            errors.append(f"{language} mapping row {row_id} Review is still bare pending")
        required_fragments = (
            (METHOD_DISPOSITION_COMMIT, "Q-01–Q-09", "relation/status unchanged",
             "local acknowledgement review pending")
            if language == "English"
            else (METHOD_DISPOSITION_COMMIT, "Q-01–Q-09", "关系/状态不变",
                  "本地确认评审待完成")
        )
        for fragment in required_fragments:
            if fragment not in normalized_review:
                errors.append(
                    f"{language} mapping row {row_id} Review lacks controlled reference: "
                    f"{fragment}"
                )
        if language == "English":
            prematurely_approved = re.search(
                r"local acknowledgement(?: review)? (?:approved|complete|closed)",
                review,
                re.IGNORECASE,
            )
        else:
            prematurely_approved = re.search(
                r"本地确认(?:评审)?(?:已批准|已通过|已完成|已关闭)", review,
            )
        if prematurely_approved:
            errors.append(
                f"{language} mapping row {row_id} prematurely approves local acknowledgement"
            )

    if set(rows) != expected_ids:
        errors.append(
            f"{language} mapping Review row IDs differ: expected {sorted(expected_ids)}, "
            f"found {sorted(rows)}"
        )
    return rows


def mapping_reconciliation_errors(text: str) -> list[str]:
    """Validate source-row closure, bilingual Review, and local additions."""
    errors: list[str] = []
    if ZH_MARKER not in text:
        return ["mapping bilingual boundary is missing"]
    english, chinese = text.split(ZH_MARKER, 1)
    english_review_rows = _mapping_language_review_rows(english, "English", errors)
    chinese_review_rows = _mapping_language_review_rows(chinese, "Chinese", errors)
    source_rows: dict[str, tuple[str, str, str, str]] = {}
    source_provenance: dict[str, str] = {}
    additional_rows: dict[str, tuple[str, str]] = {}

    for line in english.splitlines():
        if re.match(r"^\| R\d{2} \|", line):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) != 10:
                errors.append(f"method reconciliation row must have 10 columns: {line}")
                continue
            row_id, role, local_object, source, relation, status, *_ = cells
            normalized_object = re.sub(r"^PR\s*#\d+\s+", "", local_object)
            value = (
                role.strip("`"), normalized_object,
                relation.strip("`"), status.strip("`"),
            )
            if row_id in source_rows:
                errors.append(f"duplicate method reconciliation row: {row_id}")
            source_rows[row_id] = value
            source_provenance[row_id] = source
            if value[3] not in ALLOWED_MAPPING_STATUSES:
                errors.append(f"method row {row_id} has prohibited status: {value[3]}")
        elif re.match(r"^\| A\d{2} \|", line):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) != 11:
                errors.append(f"instance-only mapping row must have 11 columns: {line}")
                continue
            row_id, row_class, role, local_object, _, relation, status, *_ = cells
            role = role.strip("`")
            relation = relation.strip("`")
            status = status.strip("`")
            if row_id in additional_rows:
                errors.append(f"duplicate instance-only mapping row: {row_id}")
            additional_rows[row_id] = (role, local_object)
            if row_class.strip("`") != "INSTANCE-ONLY-ADDITIONAL":
                errors.append(f"additional row {row_id} lacks INSTANCE-ONLY-ADDITIONAL class")
            if role not in EXTERNAL_ROLE_LOCATORS:
                errors.append(f"additional row {row_id} uses unknown external role locator: {role}")
            if (relation, status) != ("no-direct-correspondence", "NOT-DETERMINED"):
                errors.append(
                    f"additional row {row_id} must remain no-direct-correspondence / "
                    f"NOT-DETERMINED, found {relation} / {status}"
                )

    for row_id, expected in METHOD_MAPPING_EXPECTED.items():
        if source_rows.get(row_id) != expected:
            errors.append(
                f"method source row {row_id} is missing or strengthened: "
                f"expected {expected}, found {source_rows.get(row_id)}"
            )
    unexpected_source = set(source_rows) - set(METHOD_MAPPING_EXPECTED)
    if unexpected_source:
        errors.append(f"unexpected method source rows: {sorted(unexpected_source)}")

    for row_id, expected in INSTANCE_ADDITIONAL_EXPECTED.items():
        if additional_rows.get(row_id) != expected:
            errors.append(
                f"instance-only row {row_id} differs: expected {expected}, "
                f"found {additional_rows.get(row_id)}"
            )
    unexpected_additional = set(additional_rows) - set(INSTANCE_ADDITIONAL_EXPECTED)
    if unexpected_additional:
        errors.append(f"unexpected instance-only rows: {sorted(unexpected_additional)}")

    if source_rows.get("R07", (None,))[0] == source_rows.get("R08", (None,))[0]:
        errors.append("VerificationCase and VerificationProcedure are not independent rows")
    if source_provenance.get("R03") == source_provenance.get("R04"):
        errors.append("legacy and candidate VerificationObligation sources are not separated")
    for row_id in sorted(set(english_review_rows) & set(chinese_review_rows)):
        english_relation_status = english_review_rows[row_id][:2]
        chinese_relation_status = chinese_review_rows[row_id][:2]
        if english_relation_status != chinese_relation_status:
            errors.append(
                f"bilingual mapping row {row_id} relation/status differs: "
                f"English {english_relation_status}, Chinese {chinese_relation_status}"
            )
    return errors


def acceptance_criteria_errors(baseline_text: str, cr_text: str) -> list[str]:
    errors: list[str] = []
    cr_english = cr_text.split(ZH_MARKER, 1)[0]
    ids = set(re.findall(r"(?m)^\| (AC-\d{2}) \|", cr_english))
    if ids != ACCEPTANCE_IDS:
        errors.append(f"controlled acceptance IDs differ: expected {sorted(ACCEPTANCE_IDS)}, found {sorted(ids)}")
    if "## Controlled acceptance criteria" not in cr_text or "## 受控接受准则" not in cr_text:
        errors.append("controlled acceptance section/anchor is missing in one language")
    if "CR-2026-004.md#controlled-acceptance-criteria" not in baseline_text:
        errors.append("English baseline does not link the authoritative acceptance anchor")
    if "CR-2026-004.md#受控接受准则" not in baseline_text:
        errors.append("Chinese baseline does not link the authoritative acceptance anchor")
    stale_reference = re.compile(
        r"(?:section\s+2" + "1" + r"|第\s*2" + "1" + r"\s*节)",
        re.IGNORECASE,
    )
    if stale_reference.search(baseline_text + "\n" + cr_text):
        errors.append("stale nonexistent numbered acceptance-section reference remains")
    return errors


def cr_bilingual_metadata_errors(text: str) -> list[str]:
    errors: list[str] = []
    if ZH_MARKER not in text:
        return ["CR bilingual boundary is missing"]
    english, chinese = text.split(ZH_MARKER, 1)
    english_meta = english.split("## Problem", 1)[0]
    chinese_meta = chinese.split("## 问题", 1)[0]
    checks = {
        "change class": (
            ("external method binding", "ownership", "migration", "traceability"),
            ("外部方法绑定", "所有权", "迁移", "追踪"),
        ),
        "candidate baseline": ((V43_BASELINE_PREFIX,), (V43_BASELINE_PREFIX,)),
        "prior baseline": (("RB-2026-001-v4.2.1",), ("RB-2026-001-v4.2.1",)),
        "method semantics": (("1–14", "T1–T5", "unchanged"), ("1–14", "T1–T5", "不变")),
        "status": (("Migration candidate", "Draft", "independent migration review"), ("迁移候选", "Draft", "独立迁移评审")),
        "trigger": (("Candidate GVS Core",), ("Candidate GVS Core",)),
        "method commit": ((METHOD_DEFINITION_COMMIT,), (METHOD_DEFINITION_COMMIT,)),
    }
    for label, (english_terms, chinese_terms) in checks.items():
        if not all(term.lower() in english_meta.lower() for term in english_terms):
            errors.append(f"English CR metadata differs for {label}")
        if not all(term.lower() in chinese_meta.lower() for term in chinese_terms):
            errors.append(f"Chinese CR metadata differs for {label}")
    return errors


def observation_result_errors(pbc_text: str, handoff_text: str) -> list[str]:
    errors: list[str] = []
    normalized_pbc = re.sub(r"\s+", " ", pbc_text)
    required = (
        "applying it to controlled Observation(s) produces a Result/verdict",
        "A Result is not an Observation",
        "应用于受控 Observation 后产生 Result/verdict",
        "Result 不是 Observation",
    )
    for phrase in required:
        if phrase not in normalized_pbc:
            errors.append(f"PBC is missing Observation/Oracle/Result rule: {phrase}")
    if "Observation → Oracle evaluation → Result" not in handoff_text:
        errors.append("review handoff lacks Observation → Oracle evaluation → Result")
    prohibited = (
        re.compile(r"verdict/result\s+is\s+an\s+observation", re.IGNORECASE),
        re.compile(r"verdict/result\s+是[^。\n]*观测", re.IGNORECASE),
    )
    if any(pattern.search(pbc_text) for pattern in prohibited):
        errors.append("PBC incorrectly defines Result/verdict as Observation")
    return errors


def evidence_chain_errors(
    architecture_text: str, osr_text: str, cei_text: str, manifest_text: str,
) -> list[str]:
    errors: list[str] = []
    required_by_artifact = {
        "Architecture": (
            "| Observation / raw record |", "| Result |", "| Evidence Item |",
            "| Argument / SufficiencyAssessment |", "| Claim / Decision |",
        ),
        "OSR": (
            "supportingResultRefs", "supportingEvidenceItems", "admissionDecisionRef",
            "credibilityAssessmentRef", "sufficiencyAssessmentRef", "argumentRef",
            "decisionRef", "decisionVersion", "provenance only; never direct satisfaction",
        ),
        "CEI": (
            "claimRef", "claimVersion", "argumentRef", "statusDecisionRef",
            "asOfVersion", "evidenceItemRefs", "resultRefs", "statusSnapshot",
            "never decides it",
        ),
        "Evidence Manifest": (
            "provenance container/execution record", "automatically admitted Evidence Item",
            "does not by itself satisfy an objective",
        ),
    }
    texts = {
        "Architecture": architecture_text,
        "OSR": osr_text,
        "CEI": cei_text,
        "Evidence Manifest": manifest_text,
    }
    for artifact, terms in required_by_artifact.items():
        for term in terms:
            if term not in texts[artifact]:
                errors.append(f"{artifact} is missing evidence-chain control: {term}")
    bilingual_schema_fields = {
        "OSR": (
            "supportingResultRefs", "supportingEvidenceItems", "admissionDecisionRef",
            "credibilityAssessmentRef", "sufficiencyAssessmentRef", "argumentRef",
            "decisionRef", "decisionVersion",
        ),
        "CEI": (
            "claimRef", "claimVersion", "argumentRef", "statusDecisionRef",
            "asOfVersion", "evidenceItemRefs", "resultRefs", "statusSnapshot",
        ),
    }
    for artifact, fields in bilingual_schema_fields.items():
        schema_blocks = re.findall(r"```yaml\s*\n(.*?)\n```", texts[artifact], re.DOTALL)
        if len(schema_blocks) != 2:
            errors.append(f"{artifact} must contain exactly two bilingual YAML schemas")
            continue
        for language, schema in zip(("English", "Chinese"), schema_blocks):
            for field in fields:
                if field not in schema:
                    errors.append(
                        f"{artifact} {language} schema is missing evidence-chain field: {field}"
                    )
    prohibited = (
        "| Evidence | Immutable run and analysis datasets |",
        "a claim becomes `SUPPORTED`",
    )
    combined = architecture_text + "\n" + cei_text
    for phrase in prohibited:
        if phrase in combined:
            errors.append(f"evidence/claim shortcut remains: {phrase}")
    return errors


def controlled_table_value(text: str, field: str) -> str | None:
    """Return one English control-table value; duplicates are an error upstream."""
    english = text.split(ZH_MARKER, 1)[0]
    matches = re.findall(
        rf"(?m)^\| \*\*{re.escape(field)}\*\* \| (.*?) \|$", english,
    )
    return matches[0] if len(matches) == 1 else None


def _without_fenced_code(text: str) -> str:
    """Remove fenced code before checking prose for literal Markdown damage."""
    return re.sub(r"(?ms)^```[^\n]*\n.*?^```[ \t]*$", "", text)


def _controlled_content_link_targets(text: str, heading: str) -> set[str]:
    if heading not in text:
        return set()
    section = text.split(heading, 1)[1]
    section = re.split(r"(?m)^## ", section, maxsplit=1)[0]
    return set(re.findall(r"\]\(([^)]+)\)", section))


def third_handshake_acknowledgement_errors(
    binding_text: str,
    mapping_text: str,
    pbc_text: str,
    baseline_text: str,
    change_text: str,
    handoff_text: str,
) -> list[str]:
    """Validate the cross-repository acknowledgement without awarding approval."""
    errors: list[str] = []
    documents = {
        "binding": binding_text,
        "mapping": mapping_text,
        "PBC": pbc_text,
        "baseline": baseline_text,
        "change": change_text,
        "handoff": handoff_text,
    }

    for document_name, text in documents.items():
        prose = _without_fenced_code(text)
        damage = re.search(
            r"`([nr])(?=(?:`|[ \t]*(?:[-#*>]|$)))",
            prose,
            re.MULTILINE,
        )
        if damage:
            errors.append(
                f"{document_name} contains literal Markdown line-break damage: "
                f"`{damage.group(1)}"
            )

    bilingual_documents = {
        name: text for name, text in documents.items()
        if name in {"binding", "mapping", "baseline", "change", "handoff"}
    }
    bilingual_parts: dict[str, tuple[str, str]] = {}
    for document_name, text in bilingual_documents.items():
        if ZH_MARKER not in text:
            errors.append(f"{document_name} acknowledgement bilingual boundary is missing")
            continue
        bilingual_parts[document_name] = tuple(text.split(ZH_MARKER, 1))  # type: ignore[assignment]

    bilingual_common_values = (
        METHOD_DEFINITION_COMMIT,
        METHOD_DISPOSITION_COMMIT,
        ACK_DISPOSITION,
        "Q-01–Q-09",
        EVALUATION_STATUS,
        CONFIGURATION_STATUS,
    )
    for document_name, parts in bilingual_parts.items():
        for language, section in zip(("English", "Chinese"), parts):
            for value in bilingual_common_values:
                if value not in section:
                    errors.append(
                        f"{document_name} {language} controlled acknowledgement value "
                        f"is missing: {value}"
                    )

    for document_name in ("binding", "handoff"):
        if document_name not in bilingual_parts:
            continue
        for language, section in zip(("English", "Chinese"), bilingual_parts[document_name]):
            for value, required_token in (
                (METHOD_APPROVED_HEAD, METHOD_APPROVED_HEAD),
                ("COMMENTED", "`COMMENTED`"),
                ("APPROVE", "`APPROVE`"),
            ):
                if required_token not in section:
                    errors.append(
                        f"{document_name} {language} method review truth is missing: {value}"
                    )

    if "baseline" in bilingual_parts:
        baseline_english, baseline_chinese = bilingual_parts["baseline"]
        english_links = _controlled_content_link_targets(
            baseline_english, "## Controlled content",
        )
        chinese_links = _controlled_content_link_targets(
            baseline_chinese, "## 受控内容",
        )
        normalized_chinese_links = {
            target.replace("#强制限定", "#mandatory-qualifications")
            for target in chinese_links
        }
        if len(english_links) != 7 or len(chinese_links) != 7:
            errors.append(
                "baseline bilingual Controlled content must contain exactly seven links: "
                f"English={len(english_links)}, Chinese={len(chinese_links)}"
            )
        if english_links != normalized_chinese_links:
            errors.append(
                "baseline bilingual Controlled content link targets differ: "
                f"English={sorted(english_links)}, Chinese={sorted(chinese_links)}"
            )

    expected_fields = {
        "MethodDefinitionCommit": METHOD_DEFINITION_COMMIT,
        "MethodCompatibilityDispositionCommit": METHOD_DISPOSITION_COMMIT,
    }
    for document_name in ("binding", "mapping", "baseline", "change"):
        for field, expected in expected_fields.items():
            actual = controlled_table_value(documents[document_name], field)
            expected_rendered = f"`{expected}`"
            if actual != expected_rendered:
                errors.append(
                    f"{document_name} {field} identity differs: "
                    f"expected {expected_rendered}, found {actual}"
                )

    if METHOD_DEFINITION_COMMIT == METHOD_DISPOSITION_COMMIT:
        errors.append("method definition and disposition identities are conflated")

    identity_requirements = {
        "binding": (
            METHOD_DEFINITION_COMMIT, METHOD_DISPOSITION_COMMIT,
            METHOD_APPROVED_HEAD, ARINC_V43_RELEASE_COMMIT,
            ARINC_V43_RELEASE_TAG, ACK_BASELINE_ID,
        ),
        "baseline": (
            METHOD_DEFINITION_COMMIT, METHOD_DISPOSITION_COMMIT,
            ARINC_V43_RELEASE_COMMIT, ARINC_V43_RELEASE_TAG, ACK_BASELINE_ID,
        ),
        "change": (
            METHOD_DEFINITION_COMMIT, METHOD_DISPOSITION_COMMIT,
            METHOD_APPROVED_HEAD, ARINC_V43_RELEASE_COMMIT,
            ARINC_V43_RELEASE_TAG, ACK_BASELINE_ID,
        ),
        "handoff": (
            METHOD_DEFINITION_COMMIT, METHOD_DISPOSITION_COMMIT,
            METHOD_APPROVED_HEAD, ARINC_V43_RELEASE_COMMIT,
            ARINC_V43_RELEASE_TAG, ACK_BASELINE_ID,
        ),
    }
    for document_name, values in identity_requirements.items():
        for value in values:
            if value not in documents[document_name]:
                errors.append(f"{document_name} is missing controlled identity: {value}")

    controlled_status_fields = {
        "Compatibility": ACK_DISPOSITION + " — Q-01–Q-09",
        "Instance evaluation": EVALUATION_STATUS,
        "Project Configuration": CONFIGURATION_STATUS,
    }
    for document_name in ("binding", "mapping", "PBC"):
        for field, expected in controlled_status_fields.items():
            actual = controlled_table_value(documents[document_name], field)
            if actual != expected:
                errors.append(
                    f"{document_name} controlled {field} differs: "
                    f"expected {expected}, found {actual}"
                )
    for document_name in ("binding", "mapping", "PBC", "baseline", "change", "handoff"):
        text = documents[document_name]
        for value in (ACK_DISPOSITION, EVALUATION_STATUS, CONFIGURATION_STATUS):
            if value not in text:
                errors.append(f"{document_name} is missing controlled status: {value}")
        if "Q-01–Q-09" not in text:
            errors.append(f"{document_name} is missing the Q-01–Q-09 qualification set")

    if ZH_MARKER in change_text:
        change_english, change_chinese = change_text.split(ZH_MARKER, 1)
        for language, section in (("English", change_english), ("Chinese", change_chinese)):
            change_ids = set(re.findall(r"(?m)^\| (Q-\d{2}) \|", section))
            if change_ids != ACK_QUALIFICATION_IDS:
                errors.append(
                    f"change request {language} qualification IDs differ: "
                    f"expected {sorted(ACK_QUALIFICATION_IDS)}, found {sorted(change_ids)}"
                )

    # Commit-bound locators must associate definition artifacts only with the
    # definition SHA and disposition artifacts only with the disposition SHA.
    wrong_locator_patterns = (
        rf"blob/{METHOD_DISPOSITION_COMMIT}/[^)\n]*generic_verification_suite_core\.md",
        rf"blob/{METHOD_DEFINITION_COMMIT}/[^)\n]*third_handshake_compatibility_disposition\.md",
        r"complex-system-verification-assurance/(?:blob|tree)/(?:main|master|latest)(?:/|$)",
    )
    for pattern in wrong_locator_patterns:
        if re.search(pattern, binding_text, re.IGNORECASE):
            errors.append(f"binding contains a wrong or mutable commit-bound association: {pattern}")

    prohibited_promotions = (
        "INSTANCE-EXERCISED", "VALIDATED-BASELINE", "RQ8 CLOSED",
        "Project Configuration is ESTABLISHED", "protocol conformance established",
    )
    combined = "\n".join(documents.values())
    for phrase in prohibited_promotions:
        if phrase in combined:
            errors.append(f"acknowledgement contains a prohibited promotion: {phrase}")

    required_nonclaims = (
        "no method-repository baseline or tag",
        "no protocol-conformance",
        "RQ8-closure",
    )
    for phrase in required_nonclaims:
        if phrase.lower() not in combined.lower():
            errors.append(f"acknowledgement non-claim is missing: {phrase}")

    return errors


def validate_third_handshake_acknowledgement(errors: list[str]) -> None:
    errors.extend(third_handshake_acknowledgement_errors(
        read(EXTERNAL_BINDING_PATH),
        read(INSTANCE_MAPPING_PATH),
        read(PROFILE_BINDING_PATH),
        read(ACK_BASELINE_PATH),
        read(ACK_CHANGE_PATH),
        read(ACK_HANDOFF_PATH),
    ))

def validate_instance_mapping(errors: list[str]) -> None:
    errors.extend(mapping_reconciliation_errors(read(INSTANCE_MAPPING_PATH)))


def validate_cross_repository_semantics(errors: list[str]) -> None:
    errors.extend(acceptance_criteria_errors(
        read(ASSESSED_BASELINE_PATH),
        read(ASSESSED_CHANGE_PATH),
    ))
    errors.extend(cr_bilingual_metadata_errors(read(ASSESSED_CHANGE_PATH)))
    errors.extend(observation_result_errors(
        read(PROFILE_BINDING_PATH), read(MIGRATION_HANDOFF_PATH),
    ))
    errors.extend(evidence_chain_errors(
        read(CONTRACTS_DIR / "ARCHITECTURE.md"),
        read(CONTRACTS_DIR / "OBJECTIVE_SATISFACTION_RECORD.md"),
        read(CONTRACTS_DIR / "COMPLIANCE_EVIDENCE_INDEX.md"),
        read(EVIDENCE_MANIFEST_PATH),
    ))


def validate_candidate_semantics(errors: list[str]) -> None:
    candidate_paths = [
        ROOT / "README.md", CONTROL / "PROJECT_CONTROL.md", CONTROL / "CHANGE_CONTROL.md",
        ASSESSED_BASELINE_PATH, ASSESSED_CHANGE_PATH,
        CONTRACTS_DIR / "ARCHITECTURE.md", CONTRACTS_DIR / "TRACEABILITY_SCHEMA.md",
        INSTANCE_MAPPING_PATH, PROFILE_BINDING_PATH, MIGRATION_HANDOFF_PATH,
        RESEARCH / "CLAIM_EVIDENCE_MATRIX.md", REPORT_PATH,
        ROOT / "docs/engineering/design/EVIDENCE_MANIFEST.md",
    ]
    combined = "\n".join(read(path) for path in candidate_paths)
    if re.search(r"certification-grounded", combined, re.IGNORECASE):
        errors.append("active assessed-source surfaces still use certification-grounded")

    scoped_terms = {
        "L0–L7": ("ARINC", "Profile", "not Generic"),
        "A0–A4": ("ARINC", "Profile", "not Generic"),
        "R0–R5": ("ARINC", "Profile", "not Generic"),
        "RG0–RG6": ("ARINC", "Profile", "non-Generic"),
        "G0–G7": ("ARINC", "Profile", "non-Generic"),
    }
    mapping_and_handoff = read(INSTANCE_MAPPING_PATH) + read(MIGRATION_HANDOFF_PATH)
    for taxonomy, qualifiers in scoped_terms.items():
        if taxonomy not in mapping_and_handoff:
            errors.append(f"candidate taxonomy is missing: {taxonomy}")
        for qualifier in qualifiers:
            if qualifier.lower() not in mapping_and_handoff.lower():
                errors.append(f"candidate taxonomy scope is missing qualifier: {qualifier}")

    required_nonpromotion = (
        "CEI is an index and not Claim, Argument, Evidence Item, or Evidence Architecture",
        "PASS cannot automatically promote Evidence, Objective Satisfaction, Claim support, compliance, or authority acceptance",
        "compatibility is `NOT-DETERMINED`",
        f"instance evaluation is `{EVALUATION_STATUS}`",
    )
    handoff = read(MIGRATION_HANDOFF_PATH)
    for phrase in required_nonpromotion:
        if phrase.lower() not in handoff.lower():
            errors.append(f"migration handoff is missing non-promotion rule: {phrase}")


def validate_reference_catalog(errors: list[str]) -> None:
    text = read(REFERENCE_CATALOG_PATH)
    entries = re.split(r"(?m)^- referenceId: ", text)[1:]
    identifiers: set[str] = set()
    allowed_authorities = {
        "regulatory_guidance", "standard", "academic", "engineering_practice",
    }
    for entry in entries:
        identifier = entry.splitlines()[0].strip()
        if identifier in identifiers:
            errors.append(f"duplicate reference catalog ID: {identifier}")
        identifiers.add(identifier)
        for field in ("title:", "authorityLevel:", "roles:", "supports:", "projectUsage:"):
            if not re.search(rf"(?m)^  {re.escape(field)}", entry):
                errors.append(f"reference {identifier} is missing YAML field {field}")
        authority = re.search(r"(?m)^  authorityLevel: ([^\s]+)$", entry)
        if authority and authority.group(1) not in allowed_authorities:
            errors.append(
                f"reference {identifier} has invalid authorityLevel: {authority.group(1)}"
            )
    if not entries:
        errors.append("reference catalog contains no YAML entries")


def validate_tracked_hygiene(errors: list[str]) -> None:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"], cwd=ROOT, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        errors.append(f"cannot enumerate tracked artifacts: {exc}")
        return
    tracked = [Path(item.decode("utf-8")) for item in result.stdout.split(b"\0") if item]
    prohibited_parts = {"__pycache__", ".pytest_cache", "local-references"}
    credential_patterns = (
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    )
    for relative in tracked:
        if prohibited_parts.intersection(relative.parts) or relative.suffix in {".pyc", ".pyo"}:
            errors.append(f"prohibited generated/private artifact is tracked: {relative}")
            continue
        path = ROOT / relative
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".py", ".yaml", ".yml", ".json", ".toml"}:
            continue
        try:
            text = read(path)
        except UnicodeDecodeError:
            continue
        if TRACKED_MACHINE_LOCAL_RE.search(_without_stable_invariant_lines(text)):
            errors.append(f"tracked text exposes a machine/private path: {relative}")
        for pattern in credential_patterns:
            if pattern.search(text):
                errors.append(f"possible credential/private key in tracked text: {relative}")


# STABLE_INVARIANT: lifecycle facts belong in project-status.json, while these
# patterns describe prohibited executable-code shapes.
FULL_SHA_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
NUMBERED_PR_RE = re.compile(r"\bPR\s*#\d+\b", re.IGNORECASE)
MUTABLE_IDENTITY_RE = re.compile(
    r"(?:refs/heads/|origin/|blob/)(?:main|master|latest)(?![\w.-])"
    r"|(?:BRANCH|REF|IDENTITY|COMMIT|TAG|BASELINE)[A-Z0-9_]*\s*=\s*[\"'](?:main|master|latest)[\"']",
    re.IGNORECASE,
)
MACHINE_LOCAL_RE = re.compile(
    r"(?<![\w:])[A-Za-z]:[\\/](?![\\/])|file://|/(?:home|Users)/[^/\s]+/",  # STABLE_INVARIANT
    re.IGNORECASE,
)  # STABLE_INVARIANT
TRACKED_MACHINE_LOCAL_RE = re.compile(
    r"(?<!\w)[A-Za-z]:[\\/](?:Users|Project|Program Files)(?:[\\/]|$)"  # STABLE_INVARIANT
    r"|file://|/(?:home|Users)/[^/\s]+/",  # STABLE_INVARIANT
    re.IGNORECASE,
)  # STABLE_INVARIANT


def _without_stable_invariant_lines(text: str) -> str:
    return "\n".join(
        line for line in text.splitlines() if "# STABLE_INVARIANT" not in line
    )


def governance_code_paths(root: Path = ROOT) -> list[Path]:
    """Dynamically discover production scripts and all regression tests."""
    paths = list((root / "scripts").rglob("*.py"))
    paths.extend((root / "tests").rglob("test_*.py"))
    return sorted(
        path for path in paths
        if path.is_file() and "__pycache__" not in path.parts
    )


def lifecycle_literal_errors(status: dict, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    current_tags = {
        status["release"]["tag"],
        status["release"]["assessedSource"]["tag"],
    }
    for path in governance_code_paths(root):
        text = path.read_text(encoding="utf-8")
        errors.extend(lifecycle_literal_text_errors(text, path.name, current_tags))
    return errors


def lifecycle_literal_text_errors(
    text: str, name: str, current_tags: set[str],
) -> list[str]:
    errors: list[str] = []
    if FULL_SHA_RE.search(text):
        errors.append(f"lifecycle SHA literal in executable governance code: {name}")
    if NUMBERED_PR_RE.search(text):
        errors.append(f"PR-number literal in executable governance code: {name}")
    if MUTABLE_IDENTITY_RE.search(text):
        errors.append(f"mutable branch used as lifecycle identity: {name}")
    if MACHINE_LOCAL_RE.search(_without_stable_invariant_lines(text)):
        errors.append(f"machine-local path in executable governance code: {name}")
    for tag in current_tags:
        if re.search(rf"(?<![\w.-]){re.escape(tag)}(?![\w.-])", text):
            errors.append(f"current release-tag literal in executable governance code: {name}")
    return errors


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def changed_files_for_event(changed: set[str] | None = None) -> set[str]:
    if changed is not None:
        return {item.replace("\\", "/") for item in changed}
    if os.getenv("GITHUB_EVENT_NAME") != "pull_request":
        return set()
    base = os.getenv("GITHUB_BASE_REF")
    if not base:
        return set()
    output = _git("diff", "--name-only", f"origin/{base}...HEAD")
    return {line for line in output.splitlines() if line}


def pr_required_file_errors(status: dict, changed: set[str] | None = None) -> list[str]:
    if os.getenv("GITHUB_EVENT_NAME") != "pull_request" and changed is None:
        return []
    changed = changed_files_for_event() if changed is None else changed
    required = set(status["governance"]["requiredPullRequestFiles"])
    return [
        f"pull request must update {path}"
        for path in sorted(required - changed)
    ]


def retired_surface_errors(status: dict) -> list[str]:
    errors: list[str] = []
    current_dir = ROOT / "artifacts/reports/current"
    historical_report = ROOT / status["release"]["records"]["historicalReaderReportPath"]
    current_files = {
        path.resolve() for path in current_dir.iterdir() if path.is_file()
    } if current_dir.is_dir() else set()
    # The sole legacy path remains only because an atomic baseline references
    # it. It is historical evidence, not a current-status owner.
    if current_files != {historical_report.resolve()}:
        errors.append("legacy reader-report path differs from the single immutable historical record")
    allowed_handoffs = {
        Path(status["release"]["records"]["migrationReviewPath"]),
        Path(status["release"]["records"]["acknowledgementReviewPath"]),
    }
    found_handoffs = {
        path.relative_to(ROOT)
        for path in ROOT.rglob("*HANDOFF*.md")
        if "local-references" not in path.parts
    }
    if found_handoffs != allowed_handoffs:
        errors.append("HANDOFF population differs from the two immutable historical reviews")
    active_paths = (
        ROOT / "README.md", CONTROL / "PROJECT_CONTROL.md", CONTROL / "CHANGE_CONTROL.md",
        RESEARCH / "RESEARCH_CONTROL.md", ROOT / "docs/engineering/ENGINEERING_CONTROL.md",
        ROOT / "docs/tutorial/TUTORIAL_CONTROL.md",
        ROOT / "docs/engineering/increments/IAR_TEMPLATE.md",
    )
    for path in active_paths:
        text = read(path)
        for target in allowed_handoffs:
            if target.name in text:
                errors.append(f"active control surface references retired HANDOFF: {path.relative_to(ROOT)}")
        errors.extend(reader_handoff_text_errors(text, str(path.relative_to(ROOT))))
    return errors


def reader_handoff_text_errors(text: str, label: str) -> list[str]:
    if re.search(r"Reader-report handoff|向读者报告交接", text, re.IGNORECASE):
        return [f"active template retains reader-report handoff: {label}"]
    return []


def research_ownership_errors(text: str) -> list[str]:
    required = (
        "Method Inputs → ARINC Domain/Product Refinement → Instance Evidence → Controlled Feedback",
        "ARINC research is conducted under, not in place of, the Candidate GVS Core",
        "may not reverse-define the Generic Core",
        "Framework Change Proposal",
        "Cross-instance generalization and RQ8 closure remain the method repository's",
        "方法输入 → ARINC 领域／产品精化 → 实例证据 → 受控反馈",
        "不能反向定义 Generic Core",
        "跨实例推广和 RQ8 关闭仍由方法仓库综合",
    )
    return [f"research ownership control is missing: {phrase}" for phrase in required if phrase not in text]


def _controlled_tracked_path_error(
    raw: object, root: Path, tracked_paths: set[str], label: str,
) -> tuple[Path | None, str | None]:
    if not isinstance(raw, str) or not raw:
        return None, f"{label} must be a non-empty repository-relative path"
    normalized = raw.replace("\\", "/")
    posix = PurePosixPath(normalized)
    windows = PureWindowsPath(raw)
    if posix.is_absolute() or windows.is_absolute() or windows.drive or ".." in posix.parts:
        return None, f"{label} must be repository-relative without traversal"
    resolved_root = root.resolve()
    candidate = resolved_root / Path(*posix.parts)
    if candidate.is_symlink():
        return None, f"{label} must not be a symbolic link"
    target = candidate.resolve()
    try:
        target.relative_to(resolved_root)
    except ValueError:
        return None, f"{label} resolves outside the repository"
    if not target.is_file():
        return None, f"{label} must be an ordinary file"
    if posix.as_posix() not in tracked_paths:
        return None, f"{label} must name a Git-tracked file"
    return target, None


def _unique_rows(rows: object, label: str) -> tuple[dict[str, dict], list[str]]:
    if not isinstance(rows, list):
        return {}, [f"{label} must be a list"]
    result: dict[str, dict] = {}
    errors: list[str] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
            errors.append(f"{label}[{index}] must have a non-empty id")
            continue
        if row["id"] in result:
            errors.append(f"{label} contains duplicate id {row['id']}")
        else:
            result[row["id"]] = row
    return result, errors


def _git_blob_bytes(root: Path, relative: str, commit: str | None = None) -> tuple[bytes | None, str | None]:
    locator = f"{commit}:{relative}" if commit else f"HEAD:{relative}"
    result = subprocess.run(
        ["git", "show", locator], cwd=root,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode != 0:
        return None, f"cannot read committed Git blob {locator}"
    return result.stdout, None


def _head_blob_bytes(root: Path, relative: str) -> tuple[bytes | None, str | None]:
    return _git_blob_bytes(root, relative)


def frozen_record_errors(
    records: object, root: Path, tracked_paths: set[str], label: str = "frozenRecords",
) -> list[str]:
    """Compare registered identities with committed Git blob bytes, never checkout text.

    An optional record-level commit pins historical bytes after the same path
    later carries a successor revision. HEAD is used only when no commit is named.
    """
    errors: list[str] = []
    if not isinstance(records, list) or not records:
        return [f"{label} must be a non-empty list"]
    for index, record in enumerate(records):
        item_label = f"{label}[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{item_label} must be an object")
            continue
        target, path_error = _controlled_tracked_path_error(
            record.get("path"), root, tracked_paths, f"{item_label}.path",
        )
        if path_error:
            errors.append(path_error)
            continue
        assert target is not None
        commit = record.get("commit")
        if commit is not None:
            if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
                errors.append(f"{item_label}.commit must be a 40-character lowercase SHA")
                continue
        payload, blob_error = _git_blob_bytes(root, record["path"], commit)
        if blob_error:
            errors.append(blob_error)
            continue
        assert payload is not None
        if record.get("byteCount") != len(payload):
            errors.append(f"{item_label} byteCount differs from committed Git blob")
        if record.get("sha256") != hashlib.sha256(payload).hexdigest():
            errors.append(f"{item_label} sha256 differs from committed Git blob")
        if record.get("path") == "docs/research/methodology/RR-2026-001_test_analysis_conformance_methodology.md":
            freeze_commit = load_method_math_identity().get("historicalFreeze", {}).get("commit")
            if commit != freeze_commit:
                errors.append(
                    f"{item_label} must pin the methodology report to the historical freeze commit, "
                    "not to successor HEAD bytes"
                )
    return errors


def _required_historical_aliases(source_id: str) -> tuple[set[str], str | None]:
    """Derive the minimum normalized alias family from a canonical source ID."""
    if not isinstance(source_id, str):
        return set(), "canonical id must be a string"
    canonical = unicodedata.normalize("NFKC", source_id).strip()
    prefix, separator, designation = canonical.partition("-")
    if not separator or not prefix.strip() or not designation.strip():
        return set(), "canonical id must use prefix-designation form"
    prefix = prefix.strip()
    designation = designation.strip()
    return {
        unicodedata.normalize("NFKC", alias).strip().casefold()
        for alias in (canonical, f"{prefix} {designation}", designation)
    }, None


def _active_authority_text_errors(register: dict, root: Path, tracked_paths: set[str]) -> list[str]:
    errors: list[str] = []
    historical_aliases: list[tuple[str, str]] = []
    history = register.get("historicalAssumptions")
    if not isinstance(history, list) or not history:
        return ["historicalAssumptions must be a non-empty list"]
    for history_index, item in enumerate(history):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"].strip():
            errors.append(f"historicalAssumptions[{history_index}] must have a non-empty canonical id")
            continue
        required_aliases, canonical_error = _required_historical_aliases(item["id"])
        if canonical_error:
            errors.append(f"historical assumption {item['id']} has an invalid canonical id: {canonical_error}")
        aliases = item.get("textAliases")
        if not isinstance(aliases, list) or not aliases:
            errors.append(f"historical assumption {item['id']} must define non-empty textAliases")
            aliases = []
        non_strings = [alias for alias in aliases if not isinstance(alias, str)]
        if non_strings:
            errors.append(f"historical assumption {item['id']} textAliases must contain only strings")
        string_aliases = [alias for alias in aliases if isinstance(alias, str)]
        normalized = [unicodedata.normalize("NFKC", alias).strip().casefold() for alias in string_aliases]
        if any(not alias for alias in normalized):
            errors.append(f"historical assumption {item['id']} contains blank textAliases")
        if len(normalized) != len(set(normalized)):
            errors.append(f"historical assumption {item['id']} contains duplicate textAliases")
        missing_aliases = required_aliases - set(normalized)
        if missing_aliases:
            errors.append(
                f"historical assumption {item['id']} textAliases lacks required forms: "
                + ", ".join(sorted(missing_aliases))
            )
        scan_aliases = required_aliases | {alias for alias in normalized if alias}
        historical_aliases.extend((item["id"], alias) for alias in scan_aliases)
    surfaces = register.get("activeControlSurfacePaths")
    required_surfaces = {
        "docs/research/RESEARCH_CONTROL.md",
        "docs/engineering/ENGINEERING_CONTROL.md",
        "docs/control/contracts/ARINC615A_PROFILE_BINDING_CONFIGURATION.md",
        "docs/control/contracts/ARCHITECTURE.md",
    }
    if not isinstance(surfaces, list) or not surfaces:
        return ["activeControlSurfacePaths must be a non-empty list"]
    normalized_surfaces = [raw.replace("\\", "/") for raw in surfaces if isinstance(raw, str)]
    if len(normalized_surfaces) != len(surfaces):
        errors.append("activeControlSurfacePaths entries must be paths")
    if len(normalized_surfaces) != len(set(normalized_surfaces)):
        errors.append("activeControlSurfacePaths contains duplicate paths")
    missing = required_surfaces - set(normalized_surfaces)
    if missing:
        errors.append("activeControlSurfacePaths lacks required control surfaces: " + ", ".join(sorted(missing)))
    for index, raw in enumerate(surfaces):
        target, path_error = _controlled_tracked_path_error(
            raw, root, tracked_paths, f"activeControlSurfacePaths[{index}]",
        )
        if path_error:
            errors.append(path_error)
            continue
        assert target is not None
        control_text = target.read_text(encoding="utf-8")
        folded_text = unicodedata.normalize("NFKC", control_text).casefold()
        for source_id, alias in historical_aliases:
            offset = folded_text.find(alias)
            if offset >= 0:
                line_number = control_text.count("\n", 0, offset) + 1
                errors.append(
                    f"active control surface names historical source {source_id}: "
                    f"{raw}:{line_number}"
                )
                break
    return errors


def controlled_source_errors(
    status: dict,
    register: dict,
    acquisition: dict | None = None,
    root: Path = ROOT,
    tracked_paths: set[str] | None = None,
) -> list[str]:
    """Validate generic source, control-reference and serial-roadmap invariants."""
    errors: list[str] = []
    if tracked_paths is None:
        try:
            result = subprocess.run(
                ["git", "ls-files", "-z"], cwd=root, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            tracked_paths = {
                item.decode("utf-8").replace("\\", "/")
                for item in result.stdout.split(b"\0") if item
            }
        except (OSError, subprocess.CalledProcessError) as exc:
            return [f"cannot enumerate tracked source-control files: {exc}"]

    if not isinstance(register.get("schemaVersion"), str):
        errors.append("controlled source schemaVersion must be a string")
    by_id, unique_errors = _unique_rows(register.get("sources"), "sources")
    errors.extend(unique_errors)
    dependency_by_id, dependency_errors = _unique_rows(register.get("openDependencies"), "openDependencies")
    errors.extend(dependency_errors)
    history_by_id, history_errors = _unique_rows(register.get("historicalAssumptions"), "historicalAssumptions")
    errors.extend(history_errors)
    roadmap_by_id, roadmap_errors = _unique_rows(register.get("roadmap"), "roadmap")
    errors.extend(roadmap_errors)
    capability_by_id, capability_errors = _unique_rows(register.get("capabilities"), "capabilities")
    errors.extend(capability_errors)
    if unique_errors:
        return errors

    authority_id = register.get("currentProtocolAuthorityId")
    authorities = [item for item in by_id.values() if item.get("role") == "CURRENT-PROTOCOL-AUTHORITY"]
    if authority_id not in by_id or len(authorities) != 1 or authorities[0].get("id") != authority_id:
        errors.append("currentProtocolAuthorityId must reference the single current protocol authority")
    for item in by_id.values():
        if item.get("role") == "CURRENT-PROTOCOL-AUTHORITY":
            continue
        if not isinstance(item.get("displayGroup"), str) or not item["displayGroup"].strip():
            errors.append(f"source {item.get('id')} must declare displayGroup for README rendering")

    acquisition_path_raw = register.get("acquisitionRecordPath")
    acquisition_path, acquisition_path_error = _controlled_tracked_path_error(
        acquisition_path_raw, root, tracked_paths, "acquisitionRecordPath",
    )
    if acquisition_path_error:
        errors.append(acquisition_path_error)
    if acquisition is None and acquisition_path is not None:
        try:
            acquisition = json.loads(acquisition_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"cannot parse acquisition record: {exc}")
    acquisition = {} if acquisition is None else acquisition
    acquired_by_id, acquired_errors = _unique_rows(acquisition.get("sources"), "acquisition.sources")
    errors.extend(acquired_errors)
    acquisition_id = acquisition.get("recordId")
    identity_fields = ("id", "edition", "publicationDate", "pageCount", "byteCount", "sha256")

    for source_id, source in by_id.items():
        if not isinstance(source.get("edition"), str) or not source["edition"]:
            errors.append(f"{source_id} edition must be a non-empty string")
        if not isinstance(source.get("pageCount"), int) or source["pageCount"] <= 0:
            errors.append(f"{source_id} pageCount must be a positive integer")
        if not isinstance(source.get("byteCount"), int) or source["byteCount"] <= 0:
            errors.append(f"{source_id} byteCount must be a positive integer")
        if not re.fullmatch(r"[0-9a-f]{64}", str(source.get("sha256", ""))):
            errors.append(f"{source_id} sha256 must be a complete lowercase SHA-256")
        if source.get("sourceHandling") != "LOCAL-PROPRIETARY-NO-REPOSITORY-COPY":
            errors.append(f"{source_id} has an invalid source-handling policy")
        acquired = acquired_by_id.get(source_id)
        if acquired is None or any(source.get(field) != acquired.get(field) for field in identity_fields):
            errors.append(f"{source_id} differs from its independent acquisition record")
        if source.get("acquisitionRecordId") != acquisition_id:
            errors.append(f"{source_id} acquisitionRecordId does not resolve")
        wire_version = source.get("wireVersion")
        if wire_version is not None and (not isinstance(wire_version, str) or wire_version == source.get("edition")):
            errors.append(f"{source_id} wire version must remain distinct from edition")
        if source.get("role") == "BOUNDED-DATA-FORMAT-REFERENCE":
            if source.get("equivalentReplacementFor") != [] or not source.get("limitations"):
                errors.append(f"{source_id} bounded applicability/equivalence policy is invalid")

    for dependency_id, dependency in dependency_by_id.items():
        if dependency.get("status") != "OPEN-DEPENDENCY":
            errors.append(f"open dependency {dependency_id} has an invalid status")
        affected = dependency.get("affectedCapabilityIds")
        if not isinstance(affected, list) or not affected:
            errors.append(f"open dependency {dependency_id} must identify affected capabilities")
            continue
        for capability_id in affected:
            capability = capability_by_id.get(capability_id)
            if capability is None:
                errors.append(f"open dependency {dependency_id} references unknown capability {capability_id}")
            elif capability.get("status") == "ESTABLISHED" or dependency_id not in capability.get("blockedBy", []):
                errors.append(f"capability {capability_id} cannot be established while {dependency_id} is open")

    for history_id, item in history_by_id.items():
        if item.get("status") != "HISTORICAL-SUPERSEDED" or item.get("activeDependency") is not False:
            errors.append(f"historical assumption {history_id} must remain superseded and inactive")
        errors.extend(frozen_record_errors(
            item.get("frozenRecords"), root, tracked_paths,
            f"historicalAssumptions[{history_id}].frozenRecords",
        ))

    migration = register.get("futureSourceMigration", {})
    migration_status = migration.get("status")
    if migration_status not in {"IDLE", "ACTIVE"}:
        errors.append("future source migration status is invalid")
    if migration_status == "IDLE" and migration.get("target") is not None:
        errors.append("idle future source migration cannot name a target")
    if migration_status == "ACTIVE" and not isinstance(migration.get("target"), str):
        errors.append("active future source migration must name a target")
    if not isinstance(migration.get("requiredGates"), list) or not migration["requiredGates"]:
        errors.append("future source migration gate is incomplete")

    direction = register.get("technicalDirection", {})
    for field in ("behaviorModel", "verificationMethod"):
        if not isinstance(direction.get(field), str) or not direction[field]:
            errors.append(f"technicalDirection.{field} must be a non-empty controlled value")
    if not isinstance(direction.get("deferredModels"), list):
        errors.append("technicalDirection.deferredModels must be a list")
    platform = direction.get("executionPlatform", {})
    if platform.get("selected") is not None or platform.get("dependencies") != []:
        errors.append("an execution platform cannot be selected without its separate control gate")
    if not isinstance(platform.get("deferredCandidates"), list) or not platform.get("selectionGate"):
        errors.append("execution-platform deferral and selection gate must be controlled")
    reuse = direction.get("openSourceReuse", {})
    if set(reuse) != {"L1", "L2", "L3"} or any(not isinstance(value, str) or not value for value in reuse.values()):
        errors.append("open-source reuse policy must define non-empty L1/L2/L3 controls")

    decision_path, decision_error = _controlled_tracked_path_error(
        direction.get("decisionRecordPath"), root, tracked_paths, "technicalDirection.decisionRecordPath",
    )
    if decision_error:
        errors.append(decision_error)
    elif decision_path is not None:
        decision_text = decision_path.read_text(encoding="utf-8")
        decision_ids = direction.get("decisionIds")
        if not isinstance(decision_ids, list) or not decision_ids:
            errors.append("technicalDirection.decisionIds must be a non-empty list")
            decision_ids = []
        for decision_id in decision_ids:
            if not isinstance(decision_id, str) or decision_id not in decision_text:
                errors.append(f"technical decision record does not resolve decision {decision_id}")

    roadmap_order = list(roadmap_by_id)
    index_by_id = {stage_id: index for index, stage_id in enumerate(roadmap_order)}
    gate_ids: list[str] = []
    for stage_index, (stage_id, stage) in enumerate(roadmap_by_id.items()):
        dependencies = stage.get("dependsOn")
        if not isinstance(dependencies, list) or len(dependencies) != len(set(dependencies)):
            errors.append(f"roadmap stage {stage_id} has invalid or duplicate dependencies")
            continue
        expected_dependencies = [] if stage_index == 0 else [roadmap_order[stage_index - 1]]
        if dependencies != expected_dependencies:
            errors.append(f"roadmap stage {stage_id} must depend only on its immediate predecessor")
        gate_id = stage.get("gateId")
        if not isinstance(gate_id, str) or not gate_id:
            errors.append(f"roadmap stage {stage_id} lacks gateId")
        else:
            gate_ids.append(gate_id)
    if len(gate_ids) != len(set(gate_ids)):
        errors.append("roadmap gateId values must be unique")
    lifecycle = register.get("lifecycle", {})
    current_id, next_id = lifecycle.get("currentStageId"), lifecycle.get("nextStageId")
    if current_id not in roadmap_by_id or next_id not in roadmap_by_id or current_id == next_id:
        errors.append("lifecycle current/next stage references are invalid")
    else:
        current_index = index_by_id[current_id]
        next_index = index_by_id[next_id]
        if next_index != current_index + 1:
            errors.append("lifecycle next stage must immediately follow current stage")
        disposition = lifecycle.get("candidateDisposition")
        for stage_index, (stage_id, stage) in enumerate(roadmap_by_id.items()):
            if stage_index < current_index:
                expected_status = "COMPLETED-EXTERNALLY-VERIFIED"
                expected_gate_status = "COMPLETED-EXTERNALLY-VERIFIED"
            elif stage_index == current_index:
                expected_status = f"DISPOSITION-{disposition}"
                expected_gate_status = "EXTERNAL-VERIFICATION-REQUIRED"
            elif stage_index == next_index:
                expected_status = "NEXT-BLOCKED-BY-FINAL-GATE"
                expected_gate_status = "NOT YET ESTABLISHED"
            else:
                expected_status = "BLOCKED-BY-PREDECESSOR"
                expected_gate_status = "BLOCKED"
            if stage.get("status") != expected_status:
                errors.append(f"roadmap stage {stage_id} status must be {expected_status}")
            gate_id = stage.get("gateId")
            governed_gates = status.get("development", {}).get("gates", {})
            if isinstance(gate_id, str) and governed_gates.get(gate_id) != expected_gate_status:
                errors.append(f"roadmap gate {gate_id} status must be {expected_gate_status}")
        stop = status.get("development", {}).get("currentStop", {})
        expected_gate = roadmap_by_id[next_id].get("gateId")
        expected_path = f"development.gates.{expected_gate}"
        if stop.get("id") != expected_gate or stop.get("statusPath") != expected_path:
            errors.append("current stop does not resolve the next roadmap stage gate")
    governed_gates = status.get("development", {}).get("gates")
    if not isinstance(governed_gates, dict) or set(governed_gates) != set(gate_ids):
        errors.append("development.gates must match all and only roadmap gateId values")
    if lifecycle.get("repositoryMergeEvidence") != "EXTERNAL-VERIFICATION-REQUIRED" or lifecycle.get("independentApproval") != "NOT-AUTOMATED":
        errors.append("approval and merge evidence must remain externally verified conditions")
    if lifecycle.get("nextStageEntryRule") != "PROHIBITED-UNTIL-APPROVAL-AND-ORDINARY-MERGE-VERIFIED":
        errors.append("next-stage entry rule is not controlled")
    activation_path, activation_error = _controlled_tracked_path_error(
        lifecycle.get("formalActivationControlPath"), root, tracked_paths,
        "lifecycle.formalActivationControlPath",
    )
    if activation_error:
        errors.append(activation_error)
    elif activation_path is not None:
        activation_text = activation_path.read_text(encoding="utf-8")
        if str(lifecycle.get("candidateDisposition", "")).upper() not in activation_text.upper():
            errors.append("activation control does not identify the lifecycle disposition")

    direction_pointer = status.get("technicalDirection", {})
    register_path, register_path_error = _controlled_tracked_path_error(
        direction_pointer.get("sourceRegisterPath"), root, tracked_paths,
        "technicalDirection.sourceRegisterPath",
    )
    if register_path_error:
        errors.append(register_path_error)
    for pointer_name, expected in (
        ("currentStageIdPath", current_id), ("nextStageIdPath", next_id),
        ("formalActivationControlPath", lifecycle.get("formalActivationControlPath")),
        ("technicalDecisionPath", direction.get("decisionRecordPath")),
    ):
        pointer = direction_pointer.get(pointer_name)
        try:
            actual = sync._get(register, pointer) if isinstance(pointer, str) else None
        except KeyError:
            actual = None
        if actual != expected:
            errors.append(f"technicalDirection.{pointer_name} does not resolve controlled data")

    for constraint in register.get("protectedStateConstraints", []):
        if not isinstance(constraint, dict) or not isinstance(constraint.get("path"), str):
            errors.append("protectedStateConstraints entries require path and equals")
            continue
        try:
            actual = sync._get(status, constraint["path"])
        except KeyError:
            errors.append(f"protected state path does not resolve: {constraint['path']}")
        else:
            if actual != constraint.get("equals"):
                errors.append(f"protected state changed before its controlling stage: {constraint['path']}")

    errors.extend(_active_authority_text_errors(register, root, tracked_paths))
    return errors


def overview_semantic_errors(readme: str) -> list[str]:
    errors: list[str] = []
    if re.search(r"(?im)^\| Current release \|[^\n]*(?:Draft|candidate)", readme):
        errors.append("README still presents the current release as Draft/candidate")
    if re.search(r"(?im)^\| 当前发布 \|[^\n]*(?:Draft|候选)", readme):
        errors.append("README 中文当前发布仍被标为 Draft/候选")
    return errors


def governed_status_errors(
    status: dict,
    readme: str,
    register: dict | None = None,
    root: Path = ROOT,
    tracked_paths: set[str] | None = None,
) -> list[str]:
    """Validate governed state and the README produced from that exact state."""
    register = CONTROLLED_SOURCES if register is None else register
    errors = list(sync.status_errors(status, root))
    errors.extend(
        controlled_source_errors(
            status, register, root=root, tracked_paths=tracked_paths,
        )
    )
    try:
        expected = sync.replace_status_block(readme, status, register)
    except (sync.StatusError, KeyError, TypeError, IndexError) as exc:
        errors.append(f"README status integration failed: {exc}")
    else:
        if readme != expected:
            errors.append("README governed block differs from project-status.json")
    return errors


OWNED_PUBLICATION_PREFIX = "artifacts/publications/"
OWNED_ARTIFACT_KIND = "OWNED-GENERATED-PUBLICATION"
OWNED_SOURCE_SUFFIXES = {".tex", ".md", ".puml", ".svg", ".json"}
OWNED_FORBIDDEN_PARTS = {"local-references", "tmp"}
OWNED_DANGEROUS_SUFFIXES = {".pdf", ".patch", ".diff", ".exe", ".dll", ".bin", ".zip"}


def _tracked_repo_paths(root: Path) -> set[str] | None:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"], cwd=root, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return {item.decode("utf-8").replace("\\", "/") for item in result.stdout.split(b"\0") if item}


def _owned_registration_errors(
    registry: dict,
    root: Path,
    tracked_paths: set[str],
) -> tuple[list[str], set[str]]:
    """Validate owned-artifact rows. A self-reported boolean is not an exemption."""
    errors: list[str] = []
    allowed: set[str] = set()
    rows = registry.get("artifacts") if isinstance(registry, dict) else None
    if not isinstance(rows, list):
        return ["owned generated artifact registry is missing artifacts"], set()
    seen: set[str] = set()
    for index, row in enumerate(rows):
        label = f"ownedArtifacts[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{label} must be an object")
            continue
        raw = row.get("path")
        target, path_error = _controlled_tracked_path_error(raw, root, tracked_paths, label)
        normalized = str(raw or "").replace("\\", "/")
        if path_error:
            errors.append(path_error)
        if normalized in seen:
            errors.append(f"{label} duplicates target {normalized}")
        elif normalized:
            seen.add(normalized)
        publication_pdf = normalized.startswith(OWNED_PUBLICATION_PREFIX) and normalized.lower().endswith(".pdf")
        if not publication_pdf:
            errors.append(f"{label} must be a PDF under {OWNED_PUBLICATION_PREFIX}")
        kind_ok = row.get("kind") == OWNED_ARTIFACT_KIND
        if not kind_ok:
            errors.append(f"{label} is missing kind {OWNED_ARTIFACT_KIND}")
        generator_ok = isinstance(row.get("generator"), str) and bool(row.get("generator").strip())
        if not generator_ok:
            errors.append(f"{label} is missing generator")
        if not isinstance(row.get("safetyCheck"), str) or not row.get("safetyCheck").strip():
            errors.append(f"{label} is missing safetyCheck")
        declared = row.get("notProprietarySource") is True
        if not declared:
            errors.append(f"{label} must declare notProprietarySource")
        sources = row.get("trackedSources")
        if not isinstance(sources, list) or not sources:
            errors.append(f"{label} is missing trackedSources")
            sources = []
        source_ok = bool(sources)
        for source in sources:
            source_label = f"{label}.trackedSources"
            _source_path, source_error = _controlled_tracked_path_error(
                source, root, tracked_paths, source_label,
            )
            if source_error:
                errors.append(source_error)
                source_ok = False
                continue
            source_posix = PurePosixPath(str(source).replace("\\", "/"))
            if OWNED_FORBIDDEN_PARTS.intersection(source_posix.parts):
                errors.append(f"{source_label} points at a prohibited directory")
                source_ok = False
            suffix = source_posix.suffix.lower()
            if suffix not in OWNED_SOURCE_SUFFIXES or suffix in OWNED_DANGEROUS_SUFFIXES:
                errors.append(f"{source_label} must be an owned text or figure source")
                source_ok = False
        if target is not None and target.is_symlink():
            errors.append(f"{label} must not be a symbolic link")
            source_ok = False
        if path_error or not source_ok or not kind_ok or not generator_ok or not declared or not publication_pdf:
            continue
        allowed.add(normalized)
    return errors, allowed


def prohibited_source_artifact_errors(
    changed: set[str],
    registry: dict | None = None,
    root: Path | None = None,
    tracked_paths: set[str] | None = None,
) -> list[str]:
    """Reject protected-source payloads. Owned PDFs are exempt only when the registration proves its sources."""
    errors: list[str] = []
    root = ROOT if root is None else root
    if registry is None:
        if not CLTAV_OWNED_ARTIFACTS_PATH.is_file():
            registry = {}
            errors.append("owned generated artifact registry is missing")
        else:
            try:
                registry = json.loads(CLTAV_OWNED_ARTIFACTS_PATH.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                registry = {}
                errors.append("owned generated artifact registry is unreadable")
    if tracked_paths is None:
        tracked_paths = _tracked_repo_paths(root)
        if tracked_paths is None:
            errors.append("cannot enumerate tracked files for owned artifacts")
            tracked_paths = set()
    structural, owned = _owned_registration_errors(registry, root, tracked_paths)
    errors.extend(structural)
    for raw in changed:
        path = PurePosixPath(str(raw).replace("\\", "/"))
        lowered = path.name.lower()
        if "local-references" in path.parts:
            errors.append(f"private source directory cannot be tracked: {path}")
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            if str(path) not in owned:
                errors.append(f"protected or transient source artifact cannot be added: {path}")
        elif suffix in {".patch", ".diff"}:
            errors.append(f"protected or transient source artifact cannot be added: {path}")
        if any(token in lowered for token in ("standard_extract", "standard-extract", "clause_extract", "clause-extract")):
            errors.append(f"standard extraction cannot be added: {path}")
    return errors


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

    errors.extend(governed_status_errors(STATUS, read(ROOT / "README.md"), CONTROLLED_SOURCES))
    try:
        m1_package = m1_sync.load_package()
    except (OSError, json.JSONDecodeError, m1_sync.M1Error) as exc:
        errors.append(f"M1 CRS package validation failed: {exc}")
    else:
        if read(m1_sync.VIEW_PATH) != m1_sync.render(m1_package):
            errors.append("generated M1 CRS review view differs from authoritative package")
        control = CONTROLLED_SOURCES.get("requirementsControl", {})
        expected_paths = {
            "packagePath": m1_sync.PACKAGE_PATH.relative_to(ROOT).as_posix(),
            "schemaPath": "configs/requirements/m1_crs_package.schema.json",
            "reviewViewPath": m1_sync.VIEW_PATH.relative_to(ROOT).as_posix(),
            "generatorPath": "scripts/sync_m1_crs.py",
        }
        for key, expected_path in expected_paths.items():
            if control.get(key) != expected_path:
                errors.append(f"requirementsControl.{key} must be {expected_path}")
    model_control = CONTROLLED_SOURCES.get("modelControl")
    if not isinstance(model_control, dict):
        errors.append("modelControl is missing from the source register")
    else:
        try:
            m2_package = m2_sync.load_package()
        except (OSError, json.JSONDecodeError, m2_sync.M2Error) as exc:
            errors.append(f"M2 model package validation failed: {exc}")
        else:
            if read(m2_sync.VIEW_PATH) != m2_sync.render(m2_package):
                errors.append("generated M2 model review view differs from authoritative package")
            expected_m2 = {
                "packagePath": m2_sync.PACKAGE_PATH.relative_to(ROOT).as_posix(),
                "schemaPath": m2_sync.SCHEMA_PATH.relative_to(ROOT).as_posix(),
                "reviewViewPath": m2_sync.VIEW_PATH.relative_to(ROOT).as_posix(),
                "generatorPath": "scripts/sync_m2_model.py",
            }
            for key, expected_path in expected_m2.items():
                if model_control.get(key) != expected_path:
                    errors.append(f"modelControl.{key} must match the M2 generator paths")
    errors.extend(prohibited_source_artifact_errors(changed_files_for_event()))

    bilingual = [
        path for path in required
        if path.suffix == ".md"
        and path != ROOT / "README.md"
        and not BILINGUAL_EXEMPT_RE.match(path.name)
    ]
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
    errors.extend(historical_methodology_math_errors())
    crs_package = json.loads(read(ROOT / "configs/requirements/arinc_615a3_m1_crs.json"))
    audit_package = json.loads(read(SOURCE_AUDIT_PATH))
    m2_package = json.loads(read(ROOT / "configs/models/arinc_615a3_m2_model.json"))
    errors.extend(governed_source_errors(audit_package, crs_package, m2_package))
    errors.extend(
        cltav_algorithm_contract_errors(
            {module: read(CLTAV_ALGORITHM_DIR / name) for module, name in CLTAV_ALGORITHM_FILES.items()},
            read(CLTAV_PUML_DIR / "FIG-CL-TAV-09-experiment-architecture.puml"),
            read(RESEARCH / "EXPERIMENT_PLAN.md"),
        )
    )
    errors.extend(cltav_outline_errors(read(RESEARCH / "publication" / "RESEARCH_OUTLINE.md")))
    errors.extend(
        cltav_sysml_errors(
            {name: read(CLTAV_PUML_DIR / name) for name in CLTAV_PUML_FILES}
        )
    )
    errors.extend(cltav_figure_errors())

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
        errors.append("missing optional reference catalog for the active profile")
    else:
        validate_reference_catalog(errors)

    validate_gvs_binding(errors)
    validate_third_handshake_acknowledgement(errors)
    validate_instance_mapping(errors)
    validate_cross_repository_semantics(errors)
    validate_candidate_semantics(errors)
    validate_tracked_hygiene(errors)
    errors.extend(lifecycle_literal_errors(STATUS))
    errors.extend(pr_required_file_errors(STATUS))
    errors.extend(retired_surface_errors(STATUS))
    errors.extend(research_ownership_errors(read(RESEARCH / "RESEARCH_CONTROL.md")))
    errors.extend(overview_semantic_errors(read(ROOT / "README.md")))

    traceability = read(TRACEABILITY_PATH)
    for term in REQUIRED_V43_TRACEABILITY_TERMS:
        if term not in traceability:
            errors.append(f"profile traceability relation missing: {term}")

    claims = read(CLAIMS_PATH)
    for term in REQUIRED_V43_CLAIMS:
        if term not in claims:
            errors.append(f"profile claim-evidence matrix missing claim: {term}")

    v43_baselines = [b for b in discover(BASELINE_RE, BASELINES_DIR)
                     if b.stem.startswith(V43_BASELINE_PREFIX)]
    if not v43_baselines:
        errors.append("assessed-source baseline missing")
    else:
        v43_text = read(ASSESSED_BASELINE_PATH)
        if V43_BASELINE_PREFIX not in v43_text:
            errors.append("assessed-source baseline does not declare its governed identity")
        if V43_NONCLAIM_PHRASE not in v43_text:
            errors.append("assessed-source baseline is missing a required non-claim")

    cr_files = discover(CHANGE_RE, CHANGES_DIR)
    cr_prefixes = {f.stem for f in cr_files}
    if "CR-2026-004" not in cr_prefixes:
        errors.append("CR-2026-004 not found among discovered change requests")
    if "CR-2026-005" not in cr_prefixes:
        errors.append("CR-2026-005 not found among discovered change requests")

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
