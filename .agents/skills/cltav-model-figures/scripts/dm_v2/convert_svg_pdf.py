"""Best-effort SVG->PDF conversion when Draw.io CLI is absent.

This does not produce hashed Draw.io-CLI review exports.
"""
from __future__ import annotations

from pathlib import Path

from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

ROOT = Path(__file__).resolve().parents[5]


def convert(src: Path, dst: Path) -> None:
    drawing = svg2rlg(str(src))
    if drawing is None:
        raise RuntimeError(f"svg2rlg returned None for {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    renderPDF.drawToFile(drawing, str(dst))


def main() -> int:
    jobs: list[tuple[Path, Path]] = []
    drafts = ROOT / "artifacts/publications/cltav/model-drafts"
    jobs.extend((p, p.with_suffix(".pdf")) for p in sorted(drafts.glob("FIG-CL-TAV-*.svg")))
    failed = 0
    for src, dst in jobs:
        try:
            convert(src, dst)
            print(f"wrote {dst.relative_to(ROOT).as_posix()} ({dst.stat().st_size} bytes)")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL {src.relative_to(ROOT).as_posix()}: {type(exc).__name__}: {exc}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
