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
RECORD_PATH = DRAFT / "build_record.json"
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
    # TeX engines can emit UTF-8 diagnostics even when the Windows console
    # default is cp1252.  Build logging must not turn a successful/failed TeX
    # invocation into an unrelated decoder crash.
    proc = subprocess.run(
        cmd, cwd=cwd, env=env, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
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


def _final_layout_errors(cwd: Path, jobs: tuple[str, ...]) -> list[str]:
    """Reject layout and reference diagnostics from the final TeX pass.

    The combined command log contains expected first-pass citation work, so it
    is not suitable for this check.  Each final ``<job>.log`` is overwritten by
    its final pdflatex pass and is therefore the artifact-relevant diagnostic.
    """
    errors: list[str] = []
    for job in jobs:
        path = cwd / f"{job}.log"
        text = path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""
        if not text:
            errors.append(f"final {job} TeX log is missing")
            continue
        if "Overfull \\hbox" in text or "Overfull \\vbox" in text:
            errors.append(f"final {job} TeX log reports an overfull box")
        if "There were undefined references" in text or "undefined citations" in text:
            errors.append(f"final {job} TeX log reports unresolved references")
    return errors


def _stage_closure(stage: Path) -> None:
    """Copy the checker-resolved closure using the paths TeX resolves in stage."""
    for source in CHECK.source_closure():
        try:
            relative = source.relative_to(DRAFT)
            target = stage / (source.name if relative.parts[0] == "vendor" else relative)
        except ValueError:
            try:
                source.relative_to(ALG_DIR)
                target = stage / source.name
            except ValueError:
                continue  # build-control files are hashed but not TeX inputs
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def _publish(targets: tuple[tuple[Path, Path], ...], replace: object | None = None) -> None:
    """Install a complete artifact set or restore every prior target byte-for-byte."""
    mover = replace or (lambda staged, target: staged.replace(target))
    backups: list[tuple[Path, Path]] = []
    installed: list[tuple[Path, bool]] = []
    try:
        for _, target in targets:
            existed = target.exists()
            installed.append((target, existed))
            if existed:
                backup = target.with_suffix(target.suffix + ".previous")
                shutil.copy2(target, backup)
                backups.append((target, backup))
        for staged, target in targets:
            mover(staged, target)
    except OSError as exc:
        for target, backup in backups:
            if backup.exists():
                backup.replace(target)
        for target, existed in installed:
            if not existed and target.exists():
                target.unlink()
        raise SystemExit(f"publication transaction failed; prior outputs restored: {exc}") from exc
    finally:
        for _, backup in backups:
            if backup.exists():
                backup.unlink()


def main() -> int:
    if not DRAFT.is_dir():
        raise SystemExit("manuscript directory is missing")
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    _stage_closure(STAGE)
    log = STAGE / "compile.log"
    _compile("main", STAGE, log)
    _compile("supplementary", STAGE, log)
    staged_main = STAGE / "main.pdf"
    staged_supp = STAGE / "supplementary.pdf"
    problems = _log_has_fatal(log) + _final_layout_errors(STAGE, ("main", "supplementary"))
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
        # This state is deliberately not publishable.  It becomes complete
        # only after the staged artifacts pass the same checker used in CI.
        "complete": False,
    }
    (STAGE / "build_record.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    preview_errors = CHECK.manuscript_errors(
        record=record,
        artifact_paths={"main": staged_main, "supplement": staged_supp},
        allow_incomplete_record=True,
    )
    if preview_errors:
        raise SystemExit("staged validation failed:\n  - " + "\n  - ".join(preview_errors))
    record["complete"] = True
    complete_errors = CHECK.manuscript_errors(
        record=record, artifact_paths={"main": staged_main, "supplement": staged_supp}
    )
    if complete_errors:
        raise SystemExit("completed staged validation failed:\n  - " + "\n  - ".join(complete_errors))
    # Only a fully validated pair is eligible for publication.
    OUT_MAIN.parent.mkdir(parents=True, exist_ok=True)
    tmp_main = OUT_MAIN.with_suffix(".pdf.staging")
    tmp_supp = OUT_SUPP.with_suffix(".pdf.staging")
    tmp_record = RECORD_PATH.with_suffix(".json.staging")
    shutil.copy2(staged_main, tmp_main)
    shutil.copy2(staged_supp, tmp_supp)
    tmp_record.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    targets = ((tmp_main, OUT_MAIN), (tmp_supp, OUT_SUPP), (tmp_record, RECORD_PATH))
    _publish(targets)
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
