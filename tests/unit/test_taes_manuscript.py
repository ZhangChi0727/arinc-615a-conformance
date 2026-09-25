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
COMPACT = ROOT / "docs/research/publication/drafts/taes-cltav/alg_compact_01.tex"


def test_manifest_placeholders_are_complete() -> None:
    errors = taes.manuscript_errors(copy.deepcopy(MANIFEST))
    assert not any("placeholder" in item for item in errors)


def test_rejects_empty_registries() -> None:
    bad = copy.deepcopy(MANIFEST)
    bad["figures"] = []
    bad["tables"] = []
    bad["algorithms"] = []
    errors = taes.manuscript_errors(bad)
    assert any("figures" in item for item in errors)
    assert any("algorithms" in item for item in errors)


def test_rejects_duplicate_section_and_placeholder() -> None:
    bad = copy.deepcopy(MANIFEST)
    bad["sections"] = list(bad["sections"]) + [bad["sections"][0]]
    errors = taes.manuscript_errors(bad)
    assert any("duplicate section" in item for item in errors)
    text = (ROOT / "docs/research/publication/drafts/taes-cltav/sections/sec1_intro.tex").read_text(
        encoding="utf-8"
    )
    doubled = text + text
    found = taes.PH_RE.findall(doubled)
    assert len(found) > len(set(found))


def test_rejects_unsafe_input() -> None:
    bad = copy.deepcopy(MANIFEST)
    errors = taes.manuscript_errors(bad)
    assert not any("escapes" in item for item in errors)
    fake_errors: list[str] = []
    taes._safe_rel("../../../../../../README.md", fake_errors, "input")
    assert fake_errors


def test_rejects_compact_bypass_and_bare_s9() -> None:
    body = COMPACT.read_text(encoding="utf-8")
    bypass = body.split("Initialize", 1)[0] + "Initialize; \\Return SUCCESS\n\\end{algorithm}\n"
    errors = taes._duty_errors(bypass)
    assert any("bypasses" in item or "CommitCompatibleUpdate" in item for item in errors)
    bare = body.replace("CommitCompatibleUpdate", "IF-HIST-UPDATE").replace(
        "commit via", "commit via"
    )
    # force the reviewed defective phrasing
    bare = "commit via IF-HIST-UPDATE\n"
    errors = taes._duty_errors(bare)
    assert any("CommitCompatibleUpdate" in item or "bare" in item for item in errors)


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


def test_compact_algorithm_keeps_typed_duties() -> None:
    text = COMPACT.read_text(encoding="utf-8")
    assert "ALG-CLTAV-01" in text
    assert "CommitCompatibleUpdate" in text
    assert "SelectSnapshot" in text
    assert taes._duty_errors(text) == []


def test_source_hash_is_relative_and_stable() -> None:
    first = taes.source_hash()
    second = taes.source_hash()
    assert first == second
    assert len(first) == 64
