import json, base64, subprocess, urllib.parse, pathlib

gh = r"C:\Program Files\GitHub CLI\gh.exe"
repo = "ZhangChi0727/arinc-615a-conformance"
ref = "feature/rr-2026-001-methodology-and-probabilistic-extension"
root = pathlib.Path(r"E:\Project\protocol-confirmance-verification")

items = json.loads(subprocess.check_output([gh, "api", f"repos/{repo}/contents/docs/study?ref={ref}"]))
for it in items:
    name = it["name"]
    safe = name.encode("ascii", "backslashreplace").decode("ascii")
    print("FILE", safe, it["size"])
    if not name.endswith(".md"):
        continue
    enc = urllib.parse.quote(name)
    obj = json.loads(
        subprocess.check_output([gh, "api", f"repos/{repo}/contents/docs/study/{enc}?ref={ref}"])
    )
    data = base64.b64decode(obj["content"])
    out = root / "docs" / "study" / name
    out.write_bytes(data)
    print("WROTE", safe, len(data), obj["sha"][:12])

for path in [".gitignore", "docs/02_thesis_outline.md"]:
    obj = json.loads(subprocess.check_output([gh, "api", f"repos/{repo}/contents/{path}?ref={ref}"]))
    data = base64.b64decode(obj["content"])
    out = root / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    print("WROTE", path, len(data), obj["sha"][:12])
