"""Upload PR #3 review/guideline docs via GitHub Contents API."""
import json, base64, subprocess, urllib.parse, pathlib, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

gh = r"C:\Program Files\GitHub CLI\gh.exe"
repo = "ZhangChi0727/arinc-615a-conformance"
branch = "docs/pr0003-repository-refinement"
root = pathlib.Path(r"E:\Project\protocol-confirmance-verification")

FILES = [
    (
        "docs/review/REVIEW_GUIDELINE.md",
        "docs: add Must/Should/Nice bands and Theory Debt check",
    ),
    (
        "docs/proposal/PR0004_METHODOLOGY_REFINEMENT.md",
        "docs: add PR #4 methodology refinement backlog proposal",
    ),
    (
        "docs/review/Reply.md",
        "docs: record agreed Reply.md execution plan for PR #2/#4",
    ),
]


def api(args, input_bytes=None):
    return subprocess.check_output([gh, "api", *args], input=input_bytes)


def put_file(rel: str, message: str):
    path = root / rel
    if not path.exists():
        raise SystemExit(f"missing {rel}")
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    enc = urllib.parse.quote(rel)
    sha = None
    try:
        meta = json.loads(api([f"repos/{repo}/contents/{enc}?ref={branch}"]))
        sha = meta.get("sha")
    except subprocess.CalledProcessError:
        sha = None
    payload = {"message": message, "content": b64, "branch": branch}
    if sha:
        payload["sha"] = sha
    body = json.dumps(payload).encode("utf-8")
    api(
        ["--method", "PUT", f"repos/{repo}/contents/{enc}", "--input", "-"],
        input_bytes=body,
    )
    print("PUT", rel, "ok")


for rel, msg in FILES:
    put_file(rel, msg)
print("DONE")
