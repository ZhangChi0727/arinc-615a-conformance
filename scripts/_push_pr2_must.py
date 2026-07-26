"""Upload PR #2 Must fixes to feature branch via GitHub Contents API."""
import json, base64, subprocess, urllib.parse, pathlib, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

gh = r"C:\Program Files\GitHub CLI\gh.exe"
repo = "ZhangChi0727/arinc-615a-conformance"
branch = "feature/rr-2026-001-methodology-and-probabilistic-extension"
root = pathlib.Path(r"E:\Project\protocol-confirmance-verification")


def api(args, input_bytes=None):
    cmd = [gh, "api", *args]
    return subprocess.check_output(cmd, input=input_bytes)


def put_file(rel: str, message: str, local_rel: str | None = None):
    path = root / (local_rel or rel)
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
    out = api(
        ["--method", "PUT", f"repos/{repo}/contents/{enc}", "--input", "-"],
        input_bytes=body,
    )
    obj = json.loads(out)
    print("PUT", rel.encode("ascii", "backslashreplace").decode("ascii"), "ok")


def delete_file(rel: str, message: str):
    enc = urllib.parse.quote(rel)
    meta = json.loads(api([f"repos/{repo}/contents/{enc}?ref={branch}"]))
    sha = meta["sha"]
    payload = {"message": message, "sha": sha, "branch": branch}
    body = json.dumps(payload).encode("utf-8")
    api(
        ["--method", "DELETE", f"repos/{repo}/contents/{enc}", "--input", "-"],
        input_bytes=body,
    )
    print("DELETE", rel.encode("ascii", "backslashreplace").decode("ascii"), "ok")


# Chinese RR (discover remote name)
zh_name = None
items = json.loads(api([f"repos/{repo}/contents/docs/study?ref={branch}"]))
for it in items:
    if it["name"].endswith("_zh.md") and "RR-2026" in it["name"]:
        zh_name = "docs/study/" + it["name"]
        break
if not zh_name:
    raise SystemExit("ZH RR not found on remote")

local_zh = None
for p in (root / "docs" / "study").glob("RR-2026*_zh.md"):
    local_zh = str(p.relative_to(root)).replace("\\", "/")
    break
if not local_zh:
    raise SystemExit("ZH RR not found locally")

print("ZH remote:", zh_name.encode("ascii", "backslashreplace").decode("ascii"))
print("ZH local:", local_zh.encode("ascii", "backslashreplace").decode("ascii"))
put_file(
    zh_name,
    "fix(research): PR#2 Must — HMM Z_k, path confidence, weakest-link, Def.5 scope (ZH)",
    local_rel=local_zh,
)
put_file(".gitignore", "chore: ignore tutorial pptx / large slides on public repo")

# C0 delete pptx
pptx = None
tree = json.loads(api([f"repos/{repo}/git/trees/{branch}?recursive=1"]))
for t in tree.get("tree", []):
    if t["path"].endswith(".pptx") and t["path"].startswith("tutorial/"):
        pptx = t["path"]
        break
if pptx:
    delete_file(pptx, "chore: remove proprietary training pptx from public branch (C0)")
else:
    print("NO_PPTX_FOUND")

print("DONE")
