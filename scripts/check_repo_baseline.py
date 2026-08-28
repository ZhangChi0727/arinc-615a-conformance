"""Validate the repository baseline against discovered artifacts.

Version-sensitive artifacts (baselines, release records, change requests, gate
records, reader reports) are discovered by directory scan and pattern match,
not by hardcoded file names. Project invariants (root Markdown, equation tags,
bilingual structure, evidence-manifest schema, required terms) are enforced from
named constants so baseline evolution does not require editing this file.
"""

from __future__ import annotations

import json
import hashlib
import re
import subprocess
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
EXTERNAL_BINDING_PATH = CONTRACTS_DIR / "EXTERNAL_GVS_BINDING.md"
INSTANCE_MAPPING_PATH = CONTRACTS_DIR / "GVS_INSTANCE_MAPPING.md"
PROFILE_BINDING_PATH = CONTRACTS_DIR / "ARINC615A_PROFILE_BINDING_CONFIGURATION.md"
MIGRATION_HANDOFF_PATH = CONTROL / "reviews" / "PR9_GVS_MIGRATION_REVIEW_HANDOFF.md"
ACK_HANDOFF_PATH = CONTROL / "reviews" / "PR10_GVS_DISPOSITION_ACK_REVIEW_HANDOFF.md"

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
    EXTERNAL_BINDING_PATH,
    INSTANCE_MAPPING_PATH,
    PROFILE_BINDING_PATH,
    CONTROL / "decisions" / "DESIGN_DECISIONS.md",
    GATES_DIR / "GATE_RECORD_TEMPLATE.md",
    GATES_DIR / "REVIEW_GUIDELINE.md",
    GATES_DIR / "PR6_BASELINE_REVIEW_CHECKLIST.md",
    CONTROL / "risks" / "RISK_REGISTER.md",
    MIGRATION_HANDOFF_PATH,
    ACK_HANDOFF_PATH,
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

# Immutable GVS/instance identities for the reviewed migration candidate.
METHOD_DEFINITION_COMMIT = "48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b"
METHOD_DISPOSITION_COMMIT = "c02330d21fe2d3e89e7e2d6352872d52461a6dda"
METHOD_APPROVED_HEAD = "37fb88329abaea8f7127da96a66c0ac5d7525543"
ARINC_V43_RELEASE_COMMIT = "523d42bf03a1135b3d63a00bfb47d3b879d3927e"
ARINC_V43_RELEASE_TAG = "v4.3"
ACK_BASELINE_ID = "RB-2026-001-v4.3.1"
ACK_DISPOSITION = "REVIEWED-COMPATIBLE-WITH-QUALIFICATION"
ACK_QUALIFICATION_IDS = {f"Q-{number:02d}" for number in range(1, 10)}
ACK_BASELINE_PATH = BASELINES_DIR / "RB-2026-001-v4.3.1.md"
ACK_CHANGE_PATH = CHANGES_DIR / "CR-2026-005.md"
LEGACY_RELEASE_TAG = "RB-2026-001-v4.2.1"
LEGACY_RELEASE_COMMIT = "3299e6dae83424862f75a4c1d09b91b80d9d8b00"
CONTROL_STATE_COMMIT = "0ce96f701159fd4156d5e5e9889360f53977a61b"
PR9_STARTING_HEAD = "53a98447bcfa862f082ce443d69115067d3ff2f1"
ALLOWED_MAPPING_STATUSES = {
    "NOT-DETERMINED", "CANDIDATE", "PARTIAL", "CONFLICT", "OUT-OF-SCOPE",
}
METHOD_MAPPING_EXPECTED = {
    "R01": ("Applicability/Profile Declaration", "PICS-like declaration", "active v4.2.1", "realizes", "CANDIDATE"),
    "R02": ("VerificationBasisElement", "applicable CRS item", "active v4.2.1", "candidate-correspondence", "CANDIDATE"),
    "R03": ("VerificationObligation", "current ARINC requirement-obligation aspect", "active v4.2.1", "no-direct-correspondence", "NOT-DETERMINED"),
    "R04": ("VerificationObligation", "PR #9 Verification Objective", "PR #9 / v4.3 candidate", "candidate-correspondence", "NOT-DETERMINED"),
    "R05": ("Obligation/Coverage aspect", "functional/state/timing and related classifications", "active v4.2.1", "classifies", "CANDIDATE"),
    "R06": ("VerificationStrategy", "Test-and-Analysis allocation", "active v4.2.1", "realizes", "PARTIAL"),
    "R07": ("VerificationCase", "VC", "active v4.2.1", "instantiates", "CANDIDATE"),
    "R08": ("VerificationProcedure", "procedure", "active v4.2.1", "instantiates", "CANDIDATE"),
    "R09": ("Observation", "packet trace/timestamp/log", "active v4.2.1", "instantiates", "CANDIDATE"),
    "R10": ("Result", "verdict", "active v4.2.1", "instantiates", "CANDIDATE"),
    "R11": ("Oracle", "discrete/robust timing rule", "active v4.2.1", "implements", "CANDIDATE"),
    "R12": ("Evidence", "characterized execution/analysis record", "active v4.2.1", "candidate-correspondence", "NOT-DETERMINED"),
    "R13": ("Argument", "scoped assurance reasoning", "active v4.2.1", "realizes", "PARTIAL"),
    "R14": ("Claim", "PR #9 CEI claim entry candidate", "PR #9 / v4.3 candidate", "indexes", "NOT-DETERMINED"),
    "R15": ("CompositeGate", "RG/G gate package", "PR #9 / v4.3 candidate", "specializes", "NOT-DETERMINED"),
    "R16": ("Configuration", "IUT/setup/procedure identity", "active v4.2.1", "instantiates", "CANDIDATE"),
    "R17": ("Anomaly/Change/Impact", "Problem Closure plus CR/DD", "active v4.2.1", "candidate-correspondence", "NOT-DETERMINED"),
    "R18": ("SufficiencyAssessment", "PR #9 OSR/claim-review candidate", "PR #9 / v4.3 candidate", "candidate-correspondence", "NOT-DETERMINED"),
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
REPORT_DISPLAY_MATH_BLOCKS = 94
REPORT_DISPLAY_MATH_SHA256 = "2050040b3d2572f5eca3b9b7b93fed472e7e236e1951f8c88702534dbe3a24cb"


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


def display_math_fingerprint(text: str) -> tuple[int, str]:
    blocks = re.findall(r"(?ms)^\\\[$.*?^\\\]$", text)
    payload = "\n".join(blocks).encode("utf-8")
    return len(blocks), hashlib.sha256(payload).hexdigest()


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
        "NOT-EXERCISED",
        "NOT YET ESTABLISHED",
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
    if re.search(r"(?:^|[\s`'\"(])(?:[A-Za-z]:[\\/]|file://)", binding, re.MULTILINE):
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
    source_rows: dict[str, tuple[str, str, str, str, str]] = {}
    additional_rows: dict[str, tuple[str, str]] = {}

    for line in english.splitlines():
        if re.match(r"^\| R\d{2} \|", line):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) != 10:
                errors.append(f"method reconciliation row must have 10 columns: {line}")
                continue
            row_id, role, local_object, source, relation, status, *_ = cells
            value = (
                role.strip("`"), local_object, source,
                relation.strip("`"), status.strip("`"),
            )
            if row_id in source_rows:
                errors.append(f"duplicate method reconciliation row: {row_id}")
            source_rows[row_id] = value
            if value[4] not in ALLOWED_MAPPING_STATUSES:
                errors.append(f"method row {row_id} has prohibited status: {value[4]}")
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
    if source_rows.get("R03", (None, None, None))[2] == source_rows.get("R04", (None, None, None))[2]:
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
        "candidate baseline": (("RB-2026-001-v4.3",), ("RB-2026-001-v4.3",)),
        "prior baseline": (("RB-2026-001-v4.2.1",), ("RB-2026-001-v4.2.1",)),
        "method semantics": (("1–14", "T1–T5", "unchanged"), ("1–14", "T1–T5", "不变")),
        "status": (("Migration candidate", "Draft", "independent migration review"), ("迁移候选", "Draft", "独立迁移评审")),
        "trigger": (("PR #14", "pre-framework PR #9", "Candidate GVS Core"), ("PR #14", "pre-framework PR #9", "Candidate GVS Core")),
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
        "NOT-EXERCISED",
        "NOT YET ESTABLISHED",
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
        "Instance evaluation": "NOT-EXERCISED",
        "Project Configuration": "NOT YET ESTABLISHED",
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
        for value in (ACK_DISPOSITION, "NOT-EXERCISED", "NOT YET ESTABLISHED"):
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
        read(BASELINES_DIR / "RB-2026-001-v4.3.md"),
        read(CHANGES_DIR / "CR-2026-004.md"),
    ))
    errors.extend(cr_bilingual_metadata_errors(read(CHANGES_DIR / "CR-2026-004.md")))
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
        BASELINES_DIR / "RB-2026-001-v4.3.md", CHANGES_DIR / "CR-2026-004.md",
        CONTRACTS_DIR / "ARCHITECTURE.md", CONTRACTS_DIR / "TRACEABILITY_SCHEMA.md",
        INSTANCE_MAPPING_PATH, PROFILE_BINDING_PATH, MIGRATION_HANDOFF_PATH,
        RESEARCH / "CLAIM_EVIDENCE_MATRIX.md", REPORT_PATH,
        ROOT / "docs/engineering/design/EVIDENCE_MANIFEST.md",
    ]
    combined = "\n".join(read(path) for path in candidate_paths)
    if re.search(r"certification-grounded", combined, re.IGNORECASE):
        errors.append("active v4.3 candidate surfaces still use certification-grounded")

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
        "instance evaluation is `NOT-EXERCISED`",
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
        if path.suffix.lower() not in {".md", ".py", ".yaml", ".yml", ".json", ".toml"}:
            continue
        try:
            text = read(path)
        except UnicodeDecodeError:
            continue
        if relative != Path("scripts/check_repo_baseline.py") and re.search(
            r"(?:C:\\Users\\|/home/[^/]+/|file://)", text
        ):
            errors.append(f"tracked text exposes a machine/private path: {relative}")
        for pattern in credential_patterns:
            if pattern.search(text):
                errors.append(f"possible credential/private key in tracked text: {relative}")


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
    math_count, math_digest = display_math_fingerprint(report_text)
    if math_count != REPORT_DISPLAY_MATH_BLOCKS or math_digest != REPORT_DISPLAY_MATH_SHA256:
        errors.append(
            "methodology display mathematics changed from the frozen v4.2.1 payload: "
            f"blocks={math_count}, sha256={math_digest}"
        )

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
    else:
        validate_reference_catalog(errors)

    validate_gvs_binding(errors)
    validate_third_handshake_acknowledgement(errors)
    validate_instance_mapping(errors)
    validate_cross_repository_semantics(errors)
    validate_candidate_semantics(errors)
    validate_tracked_hygiene(errors)

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
        v43_text = read(BASELINES_DIR / "RB-2026-001-v4.3.md")
        if V43_BASELINE_PREFIX not in v43_text:
            errors.append("v4.3 baseline does not declare RB-2026-001-v4.3")
        if V43_NONCLAIM_PHRASE not in v43_text:
            errors.append("v4.3 baseline is missing a required non-claim")

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
