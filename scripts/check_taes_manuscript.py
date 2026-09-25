"""Mechanical gates for the TAES first-draft manuscript."""
from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "docs/research/publication/drafts/taes-cltav"
MANIFEST_PATH = DRAFT / "manuscript_manifest.json"
PH_RE = re.compile(r"\\phbox(?:high)?\{([^}]+)\}")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
CITE_RE = re.compile(r"\\cite\{([^}]+)\}")
BIB_RE = re.compile(r"@\w+\{([^,]+),")


def _load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _read(rel: str) -> str:
    return (DRAFT / rel).read_text(encoding="utf-8")


def _safe(rel: str, errors: list[str], label: str) -> None:
    raw = str(rel).replace("\\", "/")
    if raw.startswith("/") or re.match(r"^[A-Za-z]:", raw):
        errors.append(f"{label} is not repository-relative: {raw}")
        return
    posix = PurePosixPath(raw)
    if ".." in posix.parts:
        errors.append(f"{label} escapes with ..: {raw}")


def manuscript_errors(manifest: dict | None = None) -> list[str]:
    errors: list[str] = []
    if manifest is None:
        if not MANIFEST_PATH.is_file():
            return ["manuscript manifest is missing"]
        manifest = _load_manifest()
    for key in ("main", "supplement", "bibliography", "venueClass"):
        rel = manifest.get(key) if key != "venueClass" else manifest.get("venueClass")
        if key == "venueClass":
            rel = manifest.get("venueClass")
        if not rel:
            errors.append(f"manifest missing {key}")
            continue
        _safe(str(rel), errors, key)
        path = DRAFT / str(rel)
        if not path.is_file():
            errors.append(f"missing {key}: {rel}")
    used_ph: set[str] = set()
    used_labels: set[str] = set()
    used_cites: set[str] = set()
    tex_files = [manifest["main"], manifest["supplement"], "macros.tex", "alg_compact_01.tex"]
    tex_files.extend(row["file"] for row in manifest.get("sections") or [])
    blob = ""
    for rel in tex_files:
        path = DRAFT / rel
        if not path.is_file():
            errors.append(f"missing tex {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        blob += text + "\n"
        used_ph.update(PH_RE.findall(text))
        used_labels.update(LABEL_RE.findall(text))
        for group in CITE_RE.findall(text):
            used_cites.update(item.strip() for item in group.split(","))
    if "IEEEexample" in blob or "2020 IEEE" in blob:
        errors.append("template sample identity remains in the manuscript")
    declared_ph = [row["id"] for row in manifest.get("placeholders") or [] if isinstance(row, dict)]
    if len(declared_ph) != len(set(declared_ph)):
        errors.append("duplicate placeholder id")
    for pid in declared_ph:
        if pid not in used_ph:
            errors.append(f"registered placeholder unused: {pid}")
        row = next(r for r in manifest["placeholders"] if r["id"] == pid)
        if not row.get("category") or not row.get("dependsOn") or not row.get("completion"):
            errors.append(f"placeholder {pid} missing category, dependency or completion")
    for pid in sorted(used_ph - set(declared_ph)):
        errors.append(f"used placeholder is not registered: {pid}")
    for row in manifest.get("sections") or []:
        if row.get("id") not in used_labels:
            errors.append(f"section label missing: {row.get('id')}")
    bib = (DRAFT / manifest["bibliography"]).read_text(encoding="utf-8") if (DRAFT / manifest.get("bibliography", "")).is_file() else ""
    bib_keys = set(BIB_RE.findall(bib))
    for key in manifest.get("citations") or []:
        if key not in bib_keys:
            errors.append(f"citation key missing from bib: {key}")
        if key not in used_cites:
            errors.append(f"registered citation unused: {key}")
    for key in sorted(used_cites - bib_keys):
        if key:
            errors.append(f"unresolved citation: {key}")
    for row in manifest.get("algorithms") or []:
        source = ROOT / row["source"] if not str(row["source"]).startswith("docs/") and (DRAFT / row["source"]).is_file() else ROOT / row.get("authority", row["source"])
        if row["source"].endswith(".tex"):
            cand = DRAFT / row["source"]
            if cand.is_file():
                source = cand
            elif (ROOT / row["source"]).is_file():
                source = ROOT / row["source"]
            else:
                errors.append(f"algorithm source missing: {row['source']}")
                continue
        text = source.read_text(encoding="utf-8")
        if row["stableId"] not in text and row["stableId"] not in (DRAFT / "alg_compact_01.tex").read_text(encoding="utf-8"):
            errors.append(f"stable algorithm id not in source: {row['stableId']}")
    main_pdf = ROOT / (manifest.get("outputs") or {}).get("main", "")
    if main_pdf.is_file() and main_pdf.stat().st_size >= 1000:
        data = main_pdf.read_bytes()
        if not data.startswith(b"%PDF"):
            errors.append("main PDF is not a PDF")
        pages = len(re.findall(rb"/Type\s*/Page(?!s)", data))
        if pages < 1:
            errors.append("main PDF page count could not be read")
        if pages > int(manifest.get("pageBudgetMain") or 10):
            errors.append(f"main PDF exceeds project page budget: {pages}")
        extracted = data.decode("latin-1", errors="ignore")
        if "??" in extracted and re.search(r"\[\s*\?\?\s*\]", extracted):
            errors.append("main PDF contains unresolved ??")
    else:
        errors.append("main manuscript PDF has not been built")
    return errors


def main() -> int:
    errors = manuscript_errors()
    if errors:
        print("TAES manuscript check failed:")
        for item in errors:
            print(f"  - {item}")
        return 1
    print("TAES manuscript check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
