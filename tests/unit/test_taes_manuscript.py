from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load():
    spec = importlib.util.spec_from_file_location(
        "check_taes_manuscript", ROOT / "scripts/check_taes_manuscript.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


taes = _load()
MANIFEST = json.loads(
    (ROOT / "docs/research/publication/drafts/taes-cltav/manuscript_manifest.json").read_text(
        encoding="utf-8"
    )
)


def test_manifest_placeholders_are_complete() -> None:
    errors = taes.manuscript_errors(copy.deepcopy(MANIFEST))
    assert not any("placeholder" in item for item in errors)


def test_rejects_unregistered_and_empty_placeholders() -> None:
    bad = copy.deepcopy(MANIFEST)
    bad["placeholders"][0]["dependsOn"] = []
    errors = taes.manuscript_errors(bad)
    assert any("missing category, dependency or completion" in item for item in errors)
    dropped = copy.deepcopy(MANIFEST)
    dropped["placeholders"] = dropped["placeholders"][1:]
    errors = taes.manuscript_errors(dropped)
    assert any("not registered" in item for item in errors)


def test_rejects_missing_citation_key() -> None:
    bad = copy.deepcopy(MANIFEST)
    bad["citations"] = list(bad["citations"]) + ["not-a-real-paper-1999"]
    errors = taes.manuscript_errors(bad)
    assert any("missing from bib" in item for item in errors)


def test_rejects_path_escape() -> None:
    bad = copy.deepcopy(MANIFEST)
    bad["main"] = "../secret.tex"
    errors = taes.manuscript_errors(bad)
    assert any("escapes" in item or "missing" in item for item in errors)


def test_compact_algorithm_keeps_stable_id() -> None:
    text = (ROOT / "docs/research/publication/drafts/taes-cltav/alg_compact_01.tex").read_text(
        encoding="utf-8"
    )
    assert "ALG-CLTAV-01" in text
    assert "qUsedAtSelect" in text or "q_{\\mathrm{used}}" in text
