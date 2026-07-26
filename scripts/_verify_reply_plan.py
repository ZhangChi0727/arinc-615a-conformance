"""Verify Reply.md Must items landed on PR #2 / #3 branches."""
import json, subprocess, base64, urllib.parse, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
gh = r"C:\Program Files\GitHub CLI\gh.exe"
repo = "ZhangChi0727/arinc-615a-conformance"
b2 = "feature/rr-2026-001-methodology-and-probabilistic-extension"
b3 = "docs/pr0003-repository-refinement"


def api(path):
    return json.loads(subprocess.check_output([gh, "api", path]))


tree2 = api(f"repos/{repo}/git/trees/{b2}?recursive=1")["tree"]
pptx = [t["path"] for t in tree2 if t["path"].endswith(".pptx")]
print("PR2_PPTX", pptx or "NONE")

gi = api(f"repos/{repo}/contents/{urllib.parse.quote('.gitignore')}?ref={b2}")
print("GITIGNORE_PPTX", "*.pptx" in base64.b64decode(gi["content"]).decode())

items = api(f"repos/{repo}/contents/docs/study?ref={b2}")
zh = next(i for i in items if i["name"].endswith("_zh.md") and "RR-2026" in i["name"])
zhmeta = api(f"repos/{repo}/contents/{urllib.parse.quote(zh['path'])}?ref={b2}")
zht = base64.b64decode(zhmeta["content"]).decode("utf-8")
print("ZH_INTERP", "解释性模型" in zht)
print("ZH_ZK", "Z_k" in zht)
print("ZH_SCOPE", "CRS" in zht and "故障" in zht)

en = api(
    f"repos/{repo}/contents/{urllib.parse.quote('docs/study/RR-2026-001_verification_methodology_en.md')}?ref={b2}"
)
ent = base64.b64decode(en["content"]).decode("utf-8")
print("EN_INTERP", "interpretation model" in ent)
print("EN_ZK", "Z_k" in ent)
print("EN_DEF5", "within the scope of CRS" in ent)

have = {t["path"] for t in api(f"repos/{repo}/git/trees/{b3}?recursive=1")["tree"]}
for w in [
    "docs/review/REVIEW_GUIDELINE.md",
    "docs/proposal/PR0004_METHODOLOGY_REFINEMENT.md",
    "docs/review/Reply.md",
]:
    print("PR3", w, w in have)
