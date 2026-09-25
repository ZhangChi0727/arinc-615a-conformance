"""Build the TAES first-draft PDFs into an isolated staging directory."""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "docs/research/publication/drafts/taes-cltav"
ALG_DIR = ROOT / "docs/research/publication/algorithms"
STAGE = DRAFT / "build"
VENDOR = DRAFT / "vendor"
OUT_MAIN = ROOT / "artifacts/publications/cltav/CLTAV_TAES_DRAFT.pdf"
OUT_SUPP = ROOT / "artifacts/publications/cltav/CLTAV_TAES_SUPPLEMENT.pdf"

SPEC = importlib.util.spec_from_file_location(
    "check_taes_manuscript", ROOT / "scripts/check_taes_manuscript.py"
)
assert SPEC and SPEC.loader
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


def _which(name: str) -> str | None:
    return shutil.which(name)


def _run(cmd: list[str], cwd: Path, env: dict, log: Path) -> None:
    proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    previous = log.read_text(encoding="utf-8") if log.is_file() else ""
    log.write_text(previous + (proc.stdout or "") + (proc.stderr or ""), encoding="utf-8")
    if proc.returncode != 0:
        raise SystemExit(f"command failed ({proc.returncode}): {' '.join(cmd)}")


def _tex_env(cwd: Path) -> dict:
    env = dict(os.environ)
    parts = os.pathsep.join([str(cwd), str(VENDOR), str(cwd / "sections"), str(ALG_DIR), ""])
    env["TEXINPUTS"] = parts + env.get("TEXINPUTS", "")
    env["BSTINPUTS"] = str(VENDOR) + os.pathsep + env.get("BSTINPUTS", "")
    env["openout_any"] = "p"
    return env


def _compile(job: str, cwd: Path, log: Path) -> None:
    pdflatex = _which("pdflatex")
    bibtex = _which("bibtex")
    if not pdflatex or not bibtex:
        raise SystemExit("TeX capability missing: pdflatex and bibtex are required")
    env = _tex_env(cwd)
    cmd = [pdflatex, "-interaction=nonstopmode", "-halt-on-error", "-no-shell-escape", job]
    _run(cmd, cwd, env, log)
    aux = (cwd / f"{job}.aux").read_text(encoding="utf-8", errors="replace")
    if "\\citation{" in aux:
        _run([bibtex, job], cwd, env, log)
    _run(cmd, cwd, env, log)
    _run(cmd, cwd, env, log)


def _log_has_fatal(log: Path) -> list[str]:
    errors: list[str] = []
    text = log.read_text(encoding="utf-8", errors="replace") if log.is_file() else ""
    if "Output written" not in text:
        errors.append("compile log has no Output written")
    if "LaTeX Error" in text or "Fatal error" in text:
        errors.append("compile log contains a LaTeX error")
    return errors


def main() -> int:
    if not DRAFT.is_dir():
        raise SystemExit("manuscript directory is missing")
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    for name in ("main.tex", "supplementary.tex", "references.bib", "macros.tex", "alg_compact_01.tex"):
        shutil.copy2(DRAFT / name, STAGE / name)
    shutil.copytree(DRAFT / "sections", STAGE / "sections")
    shutil.copy2(VENDOR / "IEEEtaes.cls", STAGE / "IEEEtaes.cls")
    shutil.copy2(VENDOR / "IEEEtaes.bst", STAGE / "IEEEtaes.bst")
    for alg in (
        "ALG-CLTAV-02.tex",
        "ALG-CLTAV-03.tex",
        "ALG-CLTAV-04.tex",
        "ALG-CLTAV-05-selection.tex",
        "ALG-CLTAV-06-timing.tex",
        "ALG-CLTAV-07-history.tex",
    ):
        shutil.copy2(ALG_DIR / alg, STAGE / alg)
    log = STAGE / "compile.log"
    _compile("main", STAGE, log)
    _compile("supplementary", STAGE, log)
    staged_main = STAGE / "main.pdf"
    staged_supp = STAGE / "supplementary.pdf"
    problems = _log_has_fatal(log)
    if staged_main.stat().st_size < 1000 or staged_supp.stat().st_size < 1000:
        problems.append("compiled PDF is empty or truncated")
    if problems:
        raise SystemExit("; ".join(problems))
    engine = subprocess.check_output(["pdflatex", "--version"], text=True).splitlines()[0]
    record = {
        "sourceHash": CHECK.source_hash(),
        "mainPdf": str(OUT_MAIN.relative_to(ROOT)).replace("\\", "/"),
        "supplementPdf": str(OUT_SUPP.relative_to(ROOT)).replace("\\", "/"),
        "outputHashes": {
            "main": CHECK.file_sha256(staged_main),
            "supplement": CHECK.file_sha256(staged_supp),
        },
        "pageCounts": {
            "main": CHECK._pdf_pages(staged_main),
            "supplement": CHECK._pdf_pages(staged_supp),
        },
        "engine": engine,
        "complete": True,
    }
    (STAGE / "build_record.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    preview_errors = CHECK.manuscript_errors(record=record)
    # The published files are not yet copied; ignore missing-published-hash by
    # validating against staged hashes already in the record after copy.
    OUT_MAIN.parent.mkdir(parents=True, exist_ok=True)
    tmp_main = OUT_MAIN.with_suffix(".pdf.staging")
    tmp_supp = OUT_SUPP.with_suffix(".pdf.staging")
    shutil.copy2(staged_main, tmp_main)
    shutil.copy2(staged_supp, tmp_supp)
    tmp_main.replace(OUT_MAIN)
    tmp_supp.replace(OUT_SUPP)
    (DRAFT / "build_record.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    errors = CHECK.manuscript_errors()
    if errors:
        raise SystemExit("post-publish validation failed:\n  - " + "\n  - ".join(errors))
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
