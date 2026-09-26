"""Mechanical gates for the TAES first-draft manuscript."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
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
    without_percent = "\n".join(COMMENT_RE.sub("", line) for line in text.splitlines())
    result: list[str] = []
    cursor = 0
    while cursor < len(without_percent):
        match = re.search(r"\\tcp\*?\{", without_percent[cursor:])
        if not match:
            result.append(without_percent[cursor:])
            break
        start = cursor + match.start()
        brace = cursor + match.end() - 1
        result.append(without_percent[cursor:start])
        depth, end = 0, brace
        while end < len(without_percent):
            depth += without_percent[end] == "{"
            depth -= without_percent[end] == "}"
            end += 1
            if depth == 0:
                break
        cursor = end
    return "".join(result)


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


def _dependency_errors(root: Path, files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        if not path.is_file() or path.is_symlink():
            errors.append(f"dependency is not an ordinary file: {path}")
            continue
        try:
            rel = path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            errors.append(f"dependency leaves repository: {path}")
            continue
        tracked = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--error-unmatch", rel],
            capture_output=True, text=True, check=False,
        )
        if tracked.returncode:
            errors.append(f"dependency is not tracked: {rel}")
    return errors


def _hash_relative_files(root: Path, files: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(files, key=lambda item: _rel(item, root)):
        digest.update(_rel(path, root).encode("utf-8"))
        digest.update(b"\0")
        data = path.read_bytes()
        if path.suffix.lower() in {".tex", ".bib", ".cls", ".bst", ".json", ".py"}:
            data = data.replace(b"\r\n", b"\n")
        digest.update(data)
    return digest.hexdigest()


def source_closure(root: Path | None = None, draft: Path | None = None) -> list[Path]:
    root = ROOT if root is None else root
    draft = DRAFT if draft is None else draft
    files = [
        draft / "main.tex",
        draft / "supplementary.tex",
        draft / "macros.tex",
        draft / "alg_compact_01.tex",
        draft / "supp_alg03_display.tex",
        draft / "supp_alg07_display.tex",
        draft / "references.bib",
        draft / "manuscript_manifest.json",
        root / "scripts/build_taes_manuscript.py",
        root / "scripts/check_taes_manuscript.py",
    ]
    files.extend(sorted((draft / "vendor").glob("IEEEtaes.*")))
    closure_errors: list[str] = []
    for entry in (draft / "main.tex", draft / "supplementary.tex"):
        files.extend(_collect_inputs(entry, draft, closure_errors, root))
    for tex in tuple(files):
        if tex.suffix != ".tex" or not tex.is_file():
            continue
        for raw in re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", _strip_comments(tex.read_text(encoding="utf-8"))):
            for candidate in _graphic_candidates(raw, tex.parent, draft):
                if candidate.is_file():
                    files.append(candidate)
                    break
    # Missing dependencies are reported by manuscript_errors; do not silently
    # discard successfully resolved nested dependencies from the identity.
    return list(dict.fromkeys(path for path in files if path.is_file()))


def source_hash(root: Path | None = None, draft: Path | None = None) -> str:
    root = ROOT if root is None else root
    return _hash_relative_files(root, source_closure(root, draft))


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _pdf_pages(path: Path) -> int:
    pdfinfo = shutil.which("pdfinfo")
    if not pdfinfo:
        return 0
    result = subprocess.run(
        [pdfinfo, str(path)], capture_output=True, text=True, check=False
    )
    match = re.search(r"^Pages:\s+(\d+)\s*$", result.stdout, re.MULTILINE)
    return int(match.group(1)) if result.returncode == 0 and match else 0


def _collect_inputs(start: Path, draft: Path, errors: list[str], root: Path = ROOT) -> list[Path]:
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
                target = (draft / rel).resolve()
            if not target.is_file():
                alg_hit = (root / "docs/research/publication/algorithms" / Path(rel).name).resolve()
                if alg_hit.is_file():
                    target = alg_hit
            if not target.is_file():
                errors.append(f"input is missing: {raw}")
                continue
            try:
                target.relative_to(draft.resolve())
            except ValueError:
                alg = (root / "docs/research/publication/algorithms").resolve()
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
    normalized = re.sub(r"\s+", "", body)
    required_guard = r"\lIf{$\textit{status}=\texttt{SPEC-ERROR}$}{\Return\texttt{Stop-SpecError}}"
    if required_guard not in normalized:
        errors.append("S9 must stop on CommitCompatibleUpdate SPEC-ERROR")
    for token in DUTY_TOKENS:
        if token not in body:
            errors.append(f"compact algorithm is missing duty token {token}")
    if "uncertaintyRef" not in body and ",U)" not in body.replace(" ", ""):
        errors.append("select snapshot must freeze uncertainty reference U")
    return errors


def _graphic_errors(blob: str, draft: Path | None = None) -> list[str]:
    errors: list[str] = []
    for raw in re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", blob):
        _safe_rel(raw, errors, f"graphic {raw}")
        if draft is not None:
            candidates = _graphic_candidates(raw, draft, draft)
            if not any(candidate.is_file() for candidate in candidates):
                errors.append(f"graphic is missing: {raw}")
    return errors


def _graphic_candidates(raw: str, parent: Path, draft: Path) -> list[Path]:
    candidates = [parent / raw, draft / raw]
    if not Path(raw).suffix:
        candidates.extend(parent / f"{raw}{suffix}" for suffix in (".pdf", ".png", ".jpg", ".jpeg"))
        candidates.extend(draft / f"{raw}{suffix}" for suffix in (".pdf", ".png", ".jpg", ".jpeg"))
    return list(dict.fromkeys(candidates))


def _eif_branches(text: str) -> tuple[str, str, str] | None:
    start = text.find(r"\eIf")
    if start < 0:
        return None
    groups: list[str] = []
    cursor = start + 4
    while len(groups) < 3:
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1
        if cursor >= len(text) or text[cursor] != "{":
            return None
        depth, end = 0, cursor
        while end < len(text):
            depth += text[end] == "{"
            depth -= text[end] == "}"
            end += 1
            if depth == 0:
                groups.append(text[cursor + 1:end - 1])
                cursor = end
                break
        else:
            return None
    return tuple(groups)  # type: ignore[return-value]


def _if_branch(text: str, required_condition: str) -> str | None:
    start = text.find(r"\If")
    while start >= 0:
        cursor, groups = start + 3, []
        for _ in range(2):
            while cursor < len(text) and text[cursor].isspace():
                cursor += 1
            if cursor >= len(text) or text[cursor] != "{":
                break
            depth, end = 0, cursor
            while end < len(text):
                depth += text[end] == "{"
                depth -= text[end] == "}"
                end += 1
                if depth == 0:
                    groups.append(text[cursor + 1:end - 1])
                    cursor = end
                    break
            else:
                break
        if len(groups) == 2 and required_condition in groups[0]:
            return groups[1]
        start = text.find(r"\If", start + 3)
    return None


def _display_errors(s2: str, s6: str) -> list[str]:
    errors: list[str] = []
    raw_s2 = _strip_comments(s2)
    s2_branch = _if_branch(raw_s2, r"\xi.\mathrm{actionKind}\in")
    s2 = re.sub(r"\s+", "", raw_s2)
    raw_s6 = _strip_comments(s6)
    branches = _eif_branches(raw_s6)
    s6 = re.sub(r"\s+", "", raw_s6)
    if not branches or "$z.I_z$ is a valid compatible class" not in branches[0]:
        errors.append("derived S6 must preserve explicit valid/identity branches")
        return errors
    valid, identity = (re.sub(r"\s+", "", part) for part in branches[1:])
    if valid.count("\\IFhist") != 1 or identity.count("\\IFhist") != 1:
        errors.append("derived S6 must invoke exactly one history update per branch")
    if "$\\eta'\\leftarrow\\eta_c$;$H'\\leftarrowH_c$" not in valid:
        errors.append("derived S6 valid branch must adopt the narrowed history and candidate set")
    if "NONE,and$z.\\mathrm{postSummary}$" not in identity or "$H'\\leftarrowH$" not in identity:
        errors.append("derived S6 identity branch must preserve H with the NONE update")
    required_s2 = (
        "z.\\mathrm{effect}\\leftarrower.\\mathrm{effect}",
        "z.\\mathrm{kind}\\leftarrow\\xi.\\mathrm{actionKind}",
        "z.\\mathrm{actionId}\\leftarrow\\xi.\\mathrm{actionId}",
        "z.\\mathrm{prepResultEvaluated}\\leftarrow\\textbf{true}",
        "(z.\\mathrm{targetConfirmed},s,z.\\mathrm{prepErr},z.\\mathrm{declaredTarget},z.\\mathrm{evidence},p)\\leftarrow",
        "z.\\mathrm{summaryConfirmed}\\leftarrows",
        "z.\\mathrm{postSummary}\\leftarrowp",
    )
    branch_s2 = re.sub(r"\s+", "", s2_branch or "")
    if any(token not in s2 for token in required_s2) or any(token not in branch_s2 for token in required_s2[3:5]):
        errors.append("derived S2 must preserve the evaluated confirmation assignment tuple")
    return errors


def manuscript_errors(
    manifest: dict | None = None,
    root: Path | None = None,
    draft: Path | None = None,
    record: dict | None = None,
    artifact_paths: dict[str, Path] | None = None,
    allow_incomplete_record: bool = False,
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
            for dep in _collect_inputs(path, draft, errors, root):
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
        if len(declared) != len(set(declared)):
            errors.append(f"duplicate {kind[:-1]} registry entry")
        for item in declared:
            if item not in used_labels:
                errors.append(f"registered {kind[:-1]} label unused: {item}")
        for item in (label for label in used_labels if label.startswith(prefix)):
            if item not in declared:
                errors.append(f"used {kind[:-1]} label is not registered: {item}")
    errors.extend(_graphic_errors(blob, draft))
    s2_path = draft / "supp_alg03_display.tex"
    s6_path = draft / "supp_alg07_display.tex"
    if not s2_path.is_file() or not s6_path.is_file():
        errors.append("derived display module is missing")
    else:
        errors.extend(_display_errors(s2_path.read_text(encoding="utf-8"), s6_path.read_text(encoding="utf-8")))
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
    errors.extend(_dependency_errors(root, source_closure(root, draft)))
    if not isinstance(record, dict):
        errors.append("build record is missing")
    else:
        if record.get("complete") is not True and not allow_incomplete_record:
            errors.append("build record is not complete")
        if record.get("sourceHash") != expected_hash:
            errors.append("build record source hash does not match the current closure")
        for label, key in (("main", "mainPdf"), ("supplement", "supplementPdf")):
            manifest_rel = outputs.get("main" if label == "main" else "supplement")
            rel = record.get(key) or manifest_rel
            if manifest_rel and record.get(key) and record.get(key) != manifest_rel:
                errors.append(f"{label} PDF path disagrees with the manifest")
            if not rel:
                errors.append(f"{label} PDF path missing")
                continue
            path = (artifact_paths or {}).get(label, root / str(rel))
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
            if recorded_pages != pages:
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
