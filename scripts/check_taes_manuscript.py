"""Mechanical gates for the TAES first-draft manuscript."""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "docs/research/publication/drafts/taes-cltav"
MANIFEST_PATH = DRAFT / "manuscript_manifest.json"
RECORD_PATH = DRAFT / "build_record.json"
PH_RE = re.compile(r"\\phbox(?:high)?\{([^}]+)\}")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
CITE_RE = re.compile(r"\\cite\{([^}]+)\}")
BIB_RE = re.compile(r"@\w+\{([^,]+),")
INPUT_RE = re.compile(r"\\(input|include|bibliography)\{([^}]+)\}")
COMMENT_RE = re.compile(r"(?<!\\)%.*")
DUTY_TOKENS = (
    "Initialize",
    "PredictCurrent",
    "SelectAndAdmit",
    "SelectSnapshot",
    "ChargeOnce",
    "InterpretOutcome",
    "ResolveOutcome",
    "CommitCompatibleUpdate",
    "SPEC-ERROR",
    r"mathrm{control}",
    "actionKind",
)
REQUIRED_REGISTRIES = ("figures", "tables", "algorithms", "placeholders", "sections")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _strip_comments(text: str) -> str:
    return "\n".join(COMMENT_RE.sub("", line) for line in text.splitlines())


def _rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _safe_rel(raw: str, errors: list[str], label: str) -> str | None:
    text = str(raw or "").replace("\\", "/")
    if not text:
        errors.append(f"{label} is empty")
        return None
    if text.startswith("/") or re.match(r"^[A-Za-z]:", text):
        errors.append(f"{label} is not repository-relative: {text}")
        return None
    posix = PurePosixPath(text)
    if ".." in posix.parts:
        errors.append(f"{label} escapes with ..: {text}")
        return None
    return text


def _hash_relative_files(root: Path, files: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(files, key=lambda item: _rel(item, root)):
        digest.update(_rel(path, root).encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return digest.hexdigest()


def source_closure(root: Path | None = None, draft: Path | None = None) -> list[Path]:
    root = ROOT if root is None else root
    draft = DRAFT if draft is None else draft
    files = [
        draft / "main.tex",
        draft / "supplementary.tex",
        draft / "macros.tex",
        draft / "alg_compact_01.tex",
        draft / "references.bib",
        draft / "manuscript_manifest.json",
        root / "scripts/build_taes_manuscript.py",
        root / "scripts/check_taes_manuscript.py",
    ]
    files.extend(sorted((draft / "sections").glob("*.tex")))
    files.extend(sorted((draft / "vendor").glob("IEEEtaes.*")))
    alg = root / "docs/research/publication/algorithms"
    files.extend(
        alg / name
        for name in (
            "ALG-CLTAV-02.tex",
            "ALG-CLTAV-03.tex",
            "ALG-CLTAV-04.tex",
            "ALG-CLTAV-05-selection.tex",
            "ALG-CLTAV-06-timing.tex",
            "ALG-CLTAV-07-history.tex",
        )
    )
    return [path for path in files if path.is_file()]


def source_hash(root: Path | None = None, draft: Path | None = None) -> str:
    root = ROOT if root is None else root
    return _hash_relative_files(root, source_closure(root, draft))


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _pdf_pages(path: Path) -> int:
    data = path.read_bytes()
    return len(re.findall(rb"/Type\s*/Page(?!s)", data))


def _collect_inputs(start: Path, draft: Path, errors: list[str]) -> list[Path]:
    seen: list[Path] = []
    stack = [start]
    while stack:
        current = stack.pop()
        if current in seen or not current.is_file():
            continue
        seen.append(current)
        text = _strip_comments(current.read_text(encoding="utf-8"))
        for command, raw in INPUT_RE.findall(text):
            candidate = raw
            if "." not in Path(raw).name:
                candidate = raw + (".bib" if command == "bibliography" else ".tex")
            rel = _safe_rel(candidate, errors, f"input {raw}")
            if rel is None:
                continue
            target = (current.parent / rel).resolve()
            if not target.is_file():
                alg_hit = (ROOT / "docs/research/publication/algorithms" / Path(rel).name).resolve()
                if alg_hit.is_file():
                    target = alg_hit
            try:
                target.relative_to(draft.resolve())
            except ValueError:
                alg = (ROOT / "docs/research/publication/algorithms").resolve()
                try:
                    target.relative_to(alg)
                except ValueError:
                    errors.append(f"input leaves the manuscript closure: {raw}")
                    continue
            if target.is_symlink():
                errors.append(f"input is a symbolic link: {raw}")
                continue
            stack.append(target)
    return seen


def _duty_errors(compact: str) -> list[str]:
    errors: list[str] = []
    body = _strip_comments(compact)
    if re.search(r"Return\s+SUCCESS", body):
        errors.append("compact algorithm bypasses the accepted loop")
    if "CommitCompatibleUpdate" not in body:
        errors.append("S9 must call CommitCompatibleUpdate, not a bare IF-HIST-UPDATE")
    if "commit via" in body and "IF-HIST-UPDATE" in body and "CommitCompatibleUpdate" not in body:
        errors.append("S9 reduced to a bare history-interface call")
    for token in DUTY_TOKENS:
        if token not in body:
            errors.append(f"compact algorithm is missing duty token {token}")
    if "uncertaintyRef" not in body and ",U)" not in body.replace(" ", ""):
        errors.append("select snapshot must freeze uncertainty reference U")
    return errors


def manuscript_errors(
    manifest: dict | None = None,
    root: Path | None = None,
    draft: Path | None = None,
    record: dict | None = None,
) -> list[str]:
    errors: list[str] = []
    root = ROOT if root is None else root
    draft = DRAFT if draft is None else draft
    manifest_path = draft / "manuscript_manifest.json"
    if manifest is None:
        if not manifest_path.is_file():
            return ["manuscript manifest is missing"]
        try:
            manifest = _load_json(manifest_path)
        except (OSError, json.JSONDecodeError) as exc:
            return [f"manuscript manifest is unreadable: {exc}"]
    if not isinstance(manifest, dict):
        return ["manuscript manifest must be an object"]
    for key in REQUIRED_REGISTRIES:
        if key not in manifest or not isinstance(manifest.get(key), list) or not manifest[key]:
            errors.append(f"manifest registry {key} must be a nonempty list")
    for key in ("main", "supplement", "bibliography", "venueClass"):
        rel = manifest.get(key)
        safe = _safe_rel(str(rel or ""), errors, key)
        if safe and not (draft / safe).is_file():
            errors.append(f"missing {key}: {rel}")
    section_ids = [row.get("id") for row in manifest.get("sections") or [] if isinstance(row, dict)]
    if len(section_ids) != len(set(section_ids)):
        errors.append("duplicate section id")
    tex_index: dict[str, str] = {}
    main_rel = str(manifest.get("main") or "main.tex")
    supp_rel = str(manifest.get("supplement") or "supplementary.tex")

    def _index(path: Path) -> None:
        try:
            key = path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            key = path.name
        tex_index[key] = path.read_text(encoding="utf-8")

    for rel in (main_rel, supp_rel):
        path = draft / rel
        if path.is_file():
            _index(path)
            for dep in _collect_inputs(path, draft, errors):
                _index(dep)
    for row in manifest.get("sections") or []:
        if not isinstance(row, dict):
            errors.append("section row must be an object")
            continue
        rel = row.get("file")
        safe = _safe_rel(str(rel or ""), errors, f"section {row.get('id')}")
        if not safe:
            continue
        path = draft / safe
        if not path.is_file():
            errors.append(f"missing section file {rel}")
            continue
        _index(path)
    compact_path = draft / "alg_compact_01.tex"
    if compact_path.is_file():
        _index(compact_path)
        errors.extend(_duty_errors(compact_path.read_text(encoding="utf-8")))
    executable = {rel: _strip_comments(text) for rel, text in tex_index.items()}
    blob = "\n".join(executable.values())
    for raw in re.findall(r"\\(?:input|include)\{([^}]+)\}", blob):
        _safe_rel(raw if "." in Path(raw).name else raw + ".tex", errors, f"input {raw}")
    if "IEEEexample" in blob or "2020 IEEE" in blob:
        errors.append("template sample identity remains in the manuscript")
    used_ph = PH_RE.findall(blob)
    if len(used_ph) != len(set(used_ph)):
        errors.append("duplicate placeholder invocation")
    declared_ph = [row.get("id") for row in manifest.get("placeholders") or [] if isinstance(row, dict)]
    if len(declared_ph) != len(set(declared_ph)):
        errors.append("duplicate placeholder id")
    for pid in declared_ph:
        if pid not in used_ph:
            errors.append(f"registered placeholder unused: {pid}")
        row = next((item for item in manifest["placeholders"] if item.get("id") == pid), {})
        if not row.get("category") or not row.get("dependsOn") or not row.get("completion"):
            errors.append(f"placeholder {pid} missing category, dependency or completion")
    for pid in sorted(set(used_ph) - set(declared_ph)):
        errors.append(f"used placeholder is not registered: {pid}")
    used_labels = LABEL_RE.findall(blob)
    for row in manifest.get("sections") or []:
        if isinstance(row, dict) and row.get("id") not in used_labels:
            errors.append(f"section label missing: {row.get('id')}")
    for kind, prefix in (("figures", "fig:"), ("tables", "tab:"), ("algorithms", "alg:")):
        declared = [row.get("id") or row.get("paperLabel") for row in manifest.get(kind) or [] if isinstance(row, dict)]
        if not declared:
            continue
        for item in declared:
            if item not in used_labels:
                errors.append(f"registered {kind[:-1]} label unused: {item}")
    fig_src = "".join(
        text for key, text in executable.items() if key.endswith("sec3_arch.tex") or key.endswith("sec5_setup.tex")
    )
    if re.search(r"\(eval[^)]*\)[^\n]*\(sess", fig_src) or "eval.east" in fig_src:
        errors.append("architecture figure routes evaluator truth into the session")
    if "raw rec" not in fig_src and "raw record" not in fig_src:
        errors.append("architecture figure must show a raw-record return path")
    if "(truth)" in fig_src and "(sess)" in fig_src and re.search(r"truth\)[^\n]*sess", fig_src):
        errors.append("truth must not connect to the session node")
    cites: list[str] = []
    for group in CITE_RE.findall(blob):
        cites.extend(item.strip() for item in group.split(","))
    bib_rel = str(manifest.get("bibliography") or "references.bib")
    bib_path = draft / bib_rel
    bib_keys = set(BIB_RE.findall(bib_path.read_text(encoding="utf-8"))) if bib_path.is_file() else set()
    for key in manifest.get("citations") or []:
        if key not in bib_keys:
            errors.append(f"citation key missing from bib: {key}")
        if key not in cites:
            errors.append(f"registered citation unused: {key}")
    for key in sorted(set(cites) - bib_keys):
        if key:
            errors.append(f"unresolved citation: {key}")
    outputs = manifest.get("outputs") if isinstance(manifest.get("outputs"), dict) else {}
    if record is None and RECORD_PATH.is_file() and draft == DRAFT:
        try:
            record = _load_json(RECORD_PATH)
        except (OSError, json.JSONDecodeError):
            record = None
            errors.append("build record is unreadable")
    expected_hash = source_hash(root, draft)
    if not isinstance(record, dict):
        errors.append("build record is missing")
    else:
        if record.get("sourceHash") != expected_hash:
            errors.append("build record source hash does not match the current closure")
        for label, key in (("main", "mainPdf"), ("supplement", "supplementPdf")):
            rel = record.get(key) or outputs.get("main" if label == "main" else "supplement")
            if not rel:
                errors.append(f"{label} PDF path missing")
                continue
            path = root / str(rel)
            if not path.is_file() or path.stat().st_size < 1000:
                errors.append(f"{label} PDF missing or truncated")
                continue
            if not path.read_bytes().startswith(b"%PDF"):
                errors.append(f"{label} PDF is not a PDF")
                continue
            digest = file_sha256(path)
            recorded = (record.get("outputHashes") or {}).get(label)
            if recorded != digest:
                errors.append(f"{label} PDF hash does not match the build record")
            pages = _pdf_pages(path)
            if pages < 1:
                errors.append(f"{label} PDF page count could not be read")
            budget = int(manifest.get("pageBudgetMain") or 10)
            if label == "main" and pages > budget:
                errors.append(f"main PDF exceeds project page budget: {pages}")
            recorded_pages = (record.get("pageCounts") or {}).get(label)
            if recorded_pages not in (None, pages):
                errors.append(f"{label} PDF page count does not match the build record")
    return errors


def main() -> int:
    errors = manuscript_errors()
    if errors:
        print("TAES manuscript check failed:")
        for item in errors:
            print(f"  - {item}")
        return 1
    print("TAES manuscript check passed")
    record = _load_json(RECORD_PATH) if RECORD_PATH.is_file() else {}
    print(f"engine: {record.get('engine', 'unrecorded')}")
    print(f"sourceHash: {record.get('sourceHash', '')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
