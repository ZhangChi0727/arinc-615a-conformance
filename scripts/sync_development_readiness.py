"""Render the single-authority CL-TAV development review view."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import check_development_readiness as readiness

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "configs/engineering/cltav_development_contracts.json"
VIEW = ROOT / "docs/engineering/CLTAV_DEVELOPMENT_REVIEW_VIEW.md"


def render(data: dict) -> str:
    rows = data["protocolInputDispositions"]
    counts = {name: sum(row["disposition"] == name for row in rows) for name in (
        "FIRST-SLICE-IMPLEMENTATION", "DEPENDENCY-BLOCKED", "LATER-SERVICE", "NOT-TOOL-OBLIGATION")}
    lines = [
        "# CL-TAV Development Readiness Review View", "",
        "> Generated from `configs/engineering/cltav_development_contracts.json`; do not edit.", "",
        f"- Control: `{data['control']['changeRequest']}`; decisions {', '.join(data['control']['decisions'])}",
        f"- Bound M1 requirements: {len(rows)}; readiness: `{data['reviewBoundary']['readiness']}`; claim: `{data['reviewBoundary']['claims']}`",
        "", "## Disposition summary", "",
        "| Disposition | Count |", "|---|---:|",
    ]
    lines += [f"| `{name}` | {count} |" for name, count in counts.items()]
    lines += ["", "## First-slice uses", "", "| Requirement | Module | Record | Acceptance |", "|---|---|---|---|"]
    lines += [f"| `{row['inputRequirementId']}` | `{row.get('moduleId','—')}` | `{row.get('recordId','—')}` | `{row.get('acceptanceCaseId','—')}` |" for row in rows if row["firstSliceRequired"]]
    lines += ["", "# 中文版", "", "# CL-TAV 开发就绪评审视图", "", "> 由同一权威 JSON 生成，禁止手工修改。", "", f"- 绑定 M1 需求：{len(rows)}；就绪状态：`{data['reviewBoundary']['readiness']}`；主张边界：`{data['reviewBoundary']['claims']}`", "", "## 处置摘要", "", "| 处置 | 数量 |", "|---|---:|"]
    lines += [f"| `{name}` | {count} |" for name, count in counts.items()]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.loads(PACKAGE.read_text(encoding="utf-8"))
    errors = readiness.package_errors(data)
    if errors:
        print("development review view refused: " + "; ".join(errors), file=sys.stderr)
        return 1
    expected = render(data)
    actual = VIEW.read_text(encoding="utf-8") if VIEW.exists() else ""
    if args.write:
        VIEW.write_text(expected, encoding="utf-8", newline="\n")
        return 0
    if actual != expected:
        print("development review view is stale; run sync_development_readiness.py --write", file=sys.stderr)
        return 1
    print("development review view is synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
