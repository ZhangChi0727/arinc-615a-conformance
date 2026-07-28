"""Validate repository documentation against RB-2026-001-v4.1."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EN_REPORT = ROOT / "docs/study/RR-2026-001_test_analysis_conformance_methodology_en.md"
ZH_REPORT = ROOT / "docs/study/RR-2026-001_测试分析符合性验证方法论_zh.md"

REQUIRED = [
    ROOT / "docs/BASELINE.md",
    ROOT / "docs/README.md",
    EN_REPORT,
    ZH_REPORT,
    ROOT / "PROJECT_PLAN.md",
    ROOT / "docs/research/RESEARCH_PLAN.md",
    ROOT / "docs/research/EXPERIMENT_PLAN.md",
    ROOT / "docs/research/CLAIM_EVIDENCE_MATRIX.md",
    ROOT / "docs/engineering/IMPLEMENTATION_PLAN.md",
    ROOT / "docs/management/CHANGE_CONTROL.md",
    ROOT / "docs/management/RISK_REGISTER.md",
]

LEGACY_FILENAMES = {
    "RR-2026-001_verification_methodology_en.md",
    "RR-2026-001_验证用例生成方法论_zh.md",
}

LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
H2_RE = re.compile(r"^## ", re.MULTILINE)
H3_RE = re.compile(r"^### ", re.MULTILINE)
MATH_OPEN_RE = re.compile(r"^\\\[$", re.MULTILINE)
MATH_CLOSE_RE = re.compile(r"^\\\]$", re.MULTILINE)
TAG_RE = re.compile(r"\\tag\{(\d+)}")
FENCE_RE = re.compile(r"^```", re.MULTILINE)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def report_shape(path: Path) -> tuple[int, int, int, int, list[str], int]:
    text = read(path)
    return (
        len(H2_RE.findall(text)),
        len(H3_RE.findall(text)),
        len(MATH_OPEN_RE.findall(text)),
        len(MATH_CLOSE_RE.findall(text)),
        TAG_RE.findall(text),
        len(FENCE_RE.findall(text)),
    )


def local_link_errors() -> list[str]:
    errors: list[str] = []
    for source in ROOT.rglob("*.md"):
        if ".git" in source.parts:
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
    if "RB-2026-001-v4.1" not in baseline:
        errors.append("docs/BASELINE.md does not declare RB-2026-001-v4.1")

    en_shape = report_shape(EN_REPORT)
    zh_shape = report_shape(ZH_REPORT)
    if en_shape != zh_shape:
        errors.append(f"EN/ZH report structure differs: EN={en_shape}, ZH={zh_shape}")

    expected_tags = [str(number) for number in range(1, 15)]
    if en_shape[4] != expected_tags:
        errors.append(f"equation tags are not 1..14: {en_shape[4]}")
    if en_shape[2] != en_shape[3]:
        errors.append("display-math delimiters are unbalanced")
    if en_shape[5] % 2:
        errors.append("code fences are unbalanced")

    for legacy in LEGACY_FILENAMES:
        if (ROOT / "docs/study" / legacy).exists():
            errors.append(f"legacy report filename still exists: {legacy}")

    errors.extend(local_link_errors())

    if errors:
        print("Baseline validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "RB-2026-001-v4.1 validation passed: "
        f"H2={en_shape[0]}, H3={en_shape[1]}, "
        f"math_blocks={en_shape[2]}, equation_tags=1..14"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
