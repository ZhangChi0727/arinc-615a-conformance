"""Refresh units/cells of the DRAFT confirmatory design from the catalogue expander."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from a615a_sim.faults.parameters import expand_arm_cells, expand_independent_units  # noqa: E402

PATH = ROOT / "configs/research/cltav_confirmatory_design_draft_v1.json"


def main() -> None:
    payload = json.loads(PATH.read_text(encoding="utf-8"))
    units = [dict(unit) for unit in expand_independent_units()]
    cells = [dict(cell) for cell in expand_arm_cells()]
    payload["units"] = units
    payload["cells"] = cells
    payload["unitCount"] = len(units)
    payload["cellCount"] = len(cells)
    payload["attemptCountIfN1"] = len(cells)
    PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print(len(units), len(cells))


if __name__ == "__main__":
    main()
