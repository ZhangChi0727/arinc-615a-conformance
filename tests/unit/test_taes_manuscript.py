from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
from shutil import copytree

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
DRAFT = ROOT / "docs/research/publication/drafts/taes-cltav"


def _fixture_record(tmp_path: Path, mutate: str) -> tuple[Path, dict]:
    fixture_root = tmp_path / "repo"
    fixture_draft = fixture_root / "docs/research/publication/drafts/taes-cltav"
    fixture_draft.parent.mkdir(parents=True, exist_ok=True)
    copytree(DRAFT, fixture_draft, dirs_exist_ok=True)
    main = fixture_draft / "main.tex"
    main.write_text(main.read_text(encoding="utf-8") + "\n" + mutate + "\n", encoding="utf-8")
    record = json.loads((DRAFT / "build_record.json").read_text(encoding="utf-8"))
    record["sourceHash"] = taes.source_hash(fixture_root, fixture_draft)
    return fixture_draft, record


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


def test_rejects_removed_s9_error_handler() -> None:
    body = COMPACT.read_text(encoding="utf-8")
    defective = body.replace(
        "\\lIf{$\\textit{status}=\\texttt{SPEC-ERROR}$}{\\Return \\texttt{Stop-SpecError}}", ""
    )
    errors = taes._duty_errors(defective)
    assert "S9 must stop on CommitCompatibleUpdate SPEC-ERROR" in errors


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


def test_source_hash_normalizes_checkout_line_endings(tmp_path: Path) -> None:
    source = tmp_path / "source.tex"
    source.write_bytes(b"alpha\nbeta\n")
    lf_hash = taes._hash_relative_files(tmp_path, [source])
    source.write_bytes(b"alpha\r\nbeta\r\n")
    assert taes._hash_relative_files(tmp_path, [source]) == lf_hash


def test_rejects_duplicate_and_pruned_registered_figures() -> None:
    duplicate = copy.deepcopy(MANIFEST)
    duplicate["figures"].append(dict(duplicate["figures"][0]))
    errors = taes.manuscript_errors(duplicate)
    assert "duplicate figure registry entry" in errors
    pruned = copy.deepcopy(MANIFEST)
    pruned["figures"] = pruned["figures"][1:]
    errors = taes.manuscript_errors(pruned)
    assert any("used figure label is not registered: fig:arch" == item for item in errors)


def test_rejects_incomplete_or_conflicting_build_record() -> None:
    record = json.loads((ROOT / "docs/research/publication/drafts/taes-cltav/build_record.json").read_text(encoding="utf-8"))
    incomplete = dict(record)
    incomplete["complete"] = False
    errors = taes.manuscript_errors(copy.deepcopy(MANIFEST), record=incomplete)
    assert "build record is not complete" in errors
    conflict = dict(record)
    conflict["mainPdf"] = "README.md"
    errors = taes.manuscript_errors(copy.deepcopy(MANIFEST), record=conflict)
    assert "main PDF path disagrees with the manifest" in errors


def test_rejects_unsafe_graphic_dependency() -> None:
    errors = taes._graphic_errors(r"\includegraphics{../../outside.pdf}")
    assert "graphic ../../outside.pdf escapes with ..: ../../outside.pdf" in errors


def test_pdf_page_parser_capability_failure(monkeypatch: object, tmp_path: Path) -> None:
    pdf = tmp_path / "document.pdf"
    pdf.write_bytes(b"%PDF-1.4\n/Type /Page\n")
    monkeypatch.setattr(taes.shutil, "which", lambda _: None)  # type: ignore[attr-defined]
    assert taes._pdf_pages(pdf) == 0


def test_production_entry_rejects_missing_input_and_graphic_after_hash_refresh(tmp_path: Path) -> None:
    fixture_draft, record = _fixture_record(tmp_path, r"\input{r44_missing_input}")
    errors = taes.manuscript_errors(root=tmp_path / "repo", draft=fixture_draft, record=record)
    assert "input is missing: r44_missing_input" in errors
    fixture_draft, record = _fixture_record(tmp_path, r"\includegraphics{r44_missing.pdf}")
    errors = taes.manuscript_errors(root=tmp_path / "repo", draft=fixture_draft, record=record)
    assert "graphic is missing: r44_missing.pdf" in errors


def test_recursive_input_is_hashed_and_detects_its_own_change(tmp_path: Path) -> None:
    fixture_draft, record = _fixture_record(tmp_path, r"\input{r45_extra}")
    extra = fixture_draft / "r45_extra.tex"
    extra.write_text("First included text.\n", encoding="utf-8")
    fixture_root = tmp_path / "repo"
    first = taes.source_hash(fixture_root, fixture_draft)
    assert extra in taes.source_closure(fixture_root, fixture_draft)
    record["sourceHash"] = first
    assert not any("source hash" in item for item in taes.manuscript_errors(root=fixture_root, draft=fixture_draft, record=record))
    extra.write_text("Changed included text.\n", encoding="utf-8")
    assert taes.source_hash(fixture_root, fixture_draft) != first


def test_rejects_s9_guard_inversion_and_display_contract_mutations() -> None:
    inverted = COMPACT.read_text(encoding="utf-8").replace(
        "\\textit{status}=\\texttt{SPEC-ERROR}", "\\textit{status}\\neq\\texttt{SPEC-ERROR}"
    )
    assert "S9 must stop on CommitCompatibleUpdate SPEC-ERROR" in taes._duty_errors(inverted)
    s2 = (DRAFT / "supp_alg03_display.tex").read_text(encoding="utf-8")
    s6 = (DRAFT / "supp_alg07_display.tex").read_text(encoding="utf-8")
    assert "derived S2 must preserve the evaluated confirmation assignment tuple" in taes._display_errors(
        s2.replace("z.\\mathrm{prepResultEvaluated}\\leftarrow\\textbf{true}", "z.\\mathrm{prepResultEvaluated}\\leftarrow\\textbf{false}"), s6
    )
    assert "derived S6 must preserve explicit valid/identity branches" in taes._display_errors(s2, s6.replace("\\eIf", "\\uIf"))
    assert "derived S6 valid branch must adopt the narrowed history and candidate set" in taes._display_errors(
        s2, s6.replace("H'\\leftarrow H_c", "H'\\leftarrow H")
    )
    assert "derived S6 must preserve explicit valid/identity branches" in taes._display_errors(
        s2, s6.replace("is a valid compatible class", "is NOT a valid compatible class")
    )
