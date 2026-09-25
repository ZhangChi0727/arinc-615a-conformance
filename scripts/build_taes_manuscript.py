"""Build the TAES first-draft PDFs into an isolated directory."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "docs/research/publication/drafts/taes-cltav"
ALG_DIR = ROOT / "docs/research/publication/algorithms"
BUILD = DRAFT / "build"
VENDOR = DRAFT / "vendor"
OUT_MAIN = ROOT / "artifacts/publications/cltav/CLTAV_TAES_DRAFT.pdf"
OUT_SUPP = ROOT / "artifacts/publications/cltav/CLTAV_TAES_SUPPLEMENT.pdf"


def _which(name: str) -> str | None:
    return shutil.which(name)


def _run(cmd: list[str], cwd: Path, env: dict) -> None:
    proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    log = BUILD / "compile.log"
    log.write_text((proc.stdout or "") + (proc.stderr or ""), encoding="utf-8")
    if proc.returncode != 0:
        raise SystemExit(f"command failed ({proc.returncode}): {' '.join(cmd)}")


def _source_hash() -> str:
    digest = hashlib.sha256()
    paths = sorted(
        [
            *DRAFT.glob("*.tex"),
            *DRAFT.glob("*.bib"),
            *DRAFT.glob("sections/*.tex"),
            DRAFT / "manuscript_manifest.json",
            VENDOR / "IEEEtaes.cls",
            VENDOR / "IEEEtaes.bst",
            ALG_DIR / "ALG-CLTAV-05-selection.tex",
            ALG_DIR / "ALG-CLTAV-06-timing.tex",
            ALG_DIR / "ALG-CLTAV-07-history.tex",
        ]
    )
    for path in paths:
        digest.update(path.as_posix().encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _compile(job: str) -> None:
    env = dict(**{k: v for k, v in __import__("os").environ.items()})
    texinputs = str(DRAFT) + ";" + str(VENDOR) + ";" + str(DRAFT / "sections") + ";" + str(ALG_DIR) + ";"
    env["TEXINPUTS"] = texinputs + env.get("TEXINPUTS", "")
    env["BSTINPUTS"] = str(VENDOR) + ";" + env.get("BSTINPUTS", "")
    env["openout_any"] = "p"
    pdflatex = _which("pdflatex")
    bibtex = _which("bibtex")
    if not pdflatex or not bibtex:
        raise SystemExit("TeX capability missing: pdflatex and bibtex are required")
    _run([pdflatex, "-interaction=nonstopmode", "-halt-on-error", job], BUILD, env)
    aux = (BUILD / f"{job}.aux").read_text(encoding="utf-8", errors="replace")
    if "\\citation{" in aux:
        _run([bibtex, job], BUILD, env)
    _run([pdflatex, "-interaction=nonstopmode", "-halt-on-error", job], BUILD, env)
    _run([pdflatex, "-interaction=nonstopmode", "-halt-on-error", job], BUILD, env)


def main() -> int:
    if not DRAFT.is_dir():
        raise SystemExit("manuscript directory is missing")
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)
    for name in ("main.tex", "supplementary.tex", "references.bib", "macros.tex", "alg_compact_01.tex"):
        shutil.copy2(DRAFT / name, BUILD / name)
    shutil.copytree(DRAFT / "sections", BUILD / "sections")
    shutil.copy2(VENDOR / "IEEEtaes.cls", BUILD / "IEEEtaes.cls")
    shutil.copy2(VENDOR / "IEEEtaes.bst", BUILD / "IEEEtaes.bst")
    for alg in (
        "ALG-CLTAV-05-selection.tex",
        "ALG-CLTAV-06-timing.tex",
        "ALG-CLTAV-07-history.tex",
    ):
        shutil.copy2(ALG_DIR / alg, BUILD / alg)
    _compile("main")
    _compile("supplementary")
    main_pdf = BUILD / "main.pdf"
    supp_pdf = BUILD / "supplementary.pdf"
    if main_pdf.stat().st_size < 1000 or supp_pdf.stat().st_size < 1000:
        raise SystemExit("compiled PDF is empty or truncated")
    OUT_MAIN.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(main_pdf, OUT_MAIN)
    shutil.copy2(supp_pdf, OUT_SUPP)
    record = {
        "sourceHash": _source_hash(),
        "mainPdf": str(OUT_MAIN.relative_to(ROOT)).replace("\\", "/"),
        "supplementPdf": str(OUT_SUPP.relative_to(ROOT)).replace("\\", "/"),
        "engine": subprocess.check_output(["pdflatex", "--version"], text=True).splitlines()[0],
    }
    (BUILD / "build_record.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    (DRAFT / "build_record.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
