"""Render the single-authority CL-TAV development review view."""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

import check_development_readiness as readiness

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "configs/engineering/cltav_development_contracts.json"
VIEW = ROOT / "docs/engineering/CLTAV_DEVELOPMENT_REVIEW_VIEW.md"


def plain_text(value: object) -> str:
    """Render controlled free text without allowing it to alter Markdown structure."""
    text = str(value).replace("\r\n", "\n").replace("\r", "\n")
    return html.escape(text, quote=False).replace("\\", "\\\\").replace("`", "\\`").replace("|", "\\|").replace("\n", "<br>")


def render(data: dict) -> str:
    rows = data["protocolInputDispositions"]
    counts = {name: sum(row["disposition"] == name for row in rows) for name in sorted({row["disposition"] for row in rows})}
    lines = [
        "# CL-TAV Development Readiness Review View", "",
        "> Generated from `configs/engineering/cltav_development_contracts.json`; do not edit.", "",
        f"- Control: `{data['control']['changeRequest']}`; decisions {', '.join(data['control']['decisions'])}",
        f"- Bound M1 requirements: {len(rows)}; disposition total: {sum(counts.values())}; readiness: `{data['reviewBoundary']['readiness']}`; claim: `{data['reviewBoundary']['claims']}`",
        "", "## Inputs", "",
    ]
    lines += [f"- `{item['artifactId']}` — `{item['path']}` — SHA-256 `{item['sha256']}` — {plain_text(item['purpose'])}" for item in data["inputBindings"]]
    lines += ["", "## Slices and dependencies", ""]
    lines += [f"- `{item['id']}` — {plain_text(item['scope'])} — {len(item['requirementIds'])} requirement uses" for item in data["implementationSlices"]]
    lines += [f"- dependency `{item['id']}`: `{item['status']}`" for item in data["implementationDependencies"]]
    lines += ["", "## Slice membership relations", "", "| Slice | Requirement |", "|---|---|"]
    lines += [f"| `{item['id']}` | `{requirement_id}` |" for item in data["implementationSlices"] for requirement_id in item["requirementIds"]]
    lines += [
        "", "## Disposition summary", "",
        "| Disposition | Count |", "|---|---:|",
    ]
    lines += [f"| `{name}` | {count} |" for name, count in counts.items()]
    lines += ["", "## All requirement dispositions", "", "| Requirement | Disposition | First slice | Module | Record | Acceptance | Rationale |", "|---|---|---|---|---|---|---|"]
    lines += [f"| `{row['inputRequirementId']}` | `{row['disposition']}` | `{row['firstSliceRequired']}` | `{row.get('moduleId','—')}` | `{row.get('recordId','—')}` | `{row.get('acceptanceCaseId','—')}` | {plain_text(row['rationale'])} |" for row in rows]
    lines += ["", "# 中文版", "", "# CL-TAV 开发就绪评审视图", "", "> 由同一权威 JSON 生成，禁止手工修改。", "", f"- 控制：`{data['control']['changeRequest']}`；设计决策：{', '.join(f'`{decision}`' for decision in data['control']['decisions'])}", f"- 绑定 M1 需求：{len(rows)}；处置合计：{sum(counts.values())}；就绪状态：`{data['reviewBoundary']['readiness']}`；主张边界：`{data['reviewBoundary']['claims']}`", "", "## 输入身份", ""]
    lines += [f"- `{item['artifactId']}` — `{item['path']}` — SHA-256 `{item['sha256']}` — {plain_text(item['purposeZh'])}" for item in data["inputBindings"]]
    lines += ["", "## 切片与依赖", ""]
    lines += [f"- `{item['id']}` — {plain_text(item['scopeZh'])} — {len(item['requirementIds'])} 条需求用途" for item in data["implementationSlices"]]
    lines += [f"- 依赖 `{item['id']}`：`{item['status']}`" for item in data["implementationDependencies"]]
    lines += ["", "## 切片成员关系", "", "| 切片 | 需求 |", "|---|---|"]
    lines += [f"| `{item['id']}` | `{requirement_id}` |" for item in data["implementationSlices"] for requirement_id in item["requirementIds"]]
    lines += ["", "## 处置摘要", "", "| 处置 | 数量 |", "|---|---:|"]
    lines += [f"| `{name}` | {count} |" for name, count in counts.items()]
    lines += ["", "## 全部需求处置", "", "| 需求 | 处置 | 首轮 | 模块 | 记录 | 验收 | 理由 |", "|---|---|---|---|---|---|---|"]
    lines += [f"| `{row['inputRequirementId']}` | `{row['disposition']}` | `{row['firstSliceRequired']}` | `{row.get('moduleId','—')}` | `{row.get('recordId','—')}` | `{row.get('acceptanceCaseId','—')}` | {plain_text(row['rationaleZh'])} |" for row in rows]
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
