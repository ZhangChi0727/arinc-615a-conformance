#!/usr/bin/env python3
"""Write configs/research/cltav_confirmatory_hypothesis_model_v2.json from the builder."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from a615a_sim.algorithm.hypothesis_model import (  # noqa: E402
    MODEL_V2_PATH,
    build_confirmatory_hypothesis_model_v2,
)


def main() -> int:
    payload = build_confirmatory_hypothesis_model_v2()
    MODEL_V2_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
