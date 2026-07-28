"""Export Reply.md Must-execution diffs to docs/review/diffs/."""
from __future__ import annotations

import json
import subprocess
import urllib.parse
from pathlib import Path

gh = r"C:\Program Files\GitHub CLI\gh.exe"
repo = "ZhangChi0727/arinc-615a-conformance"
out_dir = Path(r"E:\Project\protocol-confirmance-verification\docs\review\diffs")
out_dir.mkdir(parents=True, exist_ok=True)


def run(args: list[str], check: bool = True) -> bytes:
    return subprocess.check_output([gh, *args]) if check else subprocess.run(
        [gh, *args], capture_output=True
    ).stdout


def pr_commits(pr: int) -> list[dict]:
    data = json.loads(run(["pr", "view", str(pr), "--json", "commits,headRefOid"]))
    return data["commits"], data["headRefOid"]


def compare_patch(base: str, head: str) -> str:
    # GitHub compare API returns files; use raw compare via gh api + accept patch
    # Prefer: gh api repos/.../compare/base...head -H Accept: application/vnd.github.v3.diff
    url = f"repos/{repo}/compare/{base}...{head}"
    proc = subprocess.run(
        [
            gh,
            "api",
            url,
            "-H",
            "Accept: application/vnd.github.v3.diff",
        ],
        capture_output=True,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout.decode("utf-8", "replace")


commits2, head2 = pr_commits(2)
print("PR2 HEAD", head2[:12])
for c in commits2[-10:]:
    print(" ", c["oid"][:7], c["messageHeadline"])

# Must commits: EN, ZH, gitignore, delete pptx
# Find first Must commit parent = base for Must-only diff
must_msgs = (
    "PR#2 Must",
    "ignore tutorial pptx",
    "remove proprietary training pptx",
)
must = [c for c in commits2 if any(m in c["messageHeadline"] for m in must_msgs)]
if not must:
    # fallback: last 4 commits
    must = commits2[-4:]

first_must = must[0]["oid"]
last_must = must[-1]["oid"]
# parent of first must
meta = json.loads(run(["api", f"repos/{repo}/commits/{first_must}"]))
base_must = meta["parents"][0]["sha"]
print("MUST_RANGE", base_must[:7], "...", last_must[:7], f"({len(must)} commits)")

patch_must = compare_patch(base_must, last_must)
# Binary pptx deletion may produce a note; keep as-is
(out_dir / "Reply_PR2_Must_executed.diff").write_text(patch_must, encoding="utf-8")
print("Wrote", out_dir / "Reply_PR2_Must_executed.diff", "bytes", len(patch_must.encode()))

commits3, head3 = pr_commits(3)
print("PR3 HEAD", head3[:12])
for c in commits3[-10:]:
    print(" ", c["oid"][:7], c["messageHeadline"])

reply_msgs = (
    "Must/Should/Nice",
    "Theory Debt",
    "PR #4 methodology",
    "Reply.md",
)
must3 = [c for c in commits3 if any(m in c["messageHeadline"] for m in reply_msgs)]
if not must3:
    must3 = commits3[-3:]

first3 = must3[0]["oid"]
last3 = must3[-1]["oid"]
meta3 = json.loads(run(["api", f"repos/{repo}/commits/{first3}"]))
base3 = meta3["parents"][0]["sha"]
print("PR3_RANGE", base3[:7], "...", last3[:7], f"({len(must3)} commits)")
patch3 = compare_patch(base3, last3)
(out_dir / "Reply_PR3_process_docs.diff").write_text(patch3, encoding="utf-8")
print("Wrote", out_dir / "Reply_PR3_process_docs.diff", "bytes", len(patch3.encode()))

# Combined for convenience
combined = (
    "# Reply.md execution — combined diff\n"
    f"# PR #2 Must: {base_must[:12]}...{last_must[:12]}\n"
    f"# PR #3 docs: {base3[:12]}...{last3[:12]}\n\n"
    + "##### PR #2 Must #####\n"
    + patch_must
    + "\n##### PR #3 process docs #####\n"
    + patch3
)
(out_dir / "Reply_executed_all.diff").write_text(combined, encoding="utf-8")
print("Wrote", out_dir / "Reply_executed_all.diff")
