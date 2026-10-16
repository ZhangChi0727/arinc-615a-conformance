from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".agents/skills/cltav-model-figures/scripts/model_drawio.py"


def load_module():
    spec = importlib.util.spec_from_file_location("cltav_model_drawio", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_package(tmp_path: Path, module):
    data = copy.deepcopy(module.load_manifest())
    manifest = tmp_path / module.MANIFEST_RELATIVE
    manifest.parent.mkdir(parents=True)
    for figure in data["figures"]:
        for key in ("sourcePuml", "drawioSource"):
            source, target = ROOT / figure[key], tmp_path / figure[key]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data


def copy_exports(tmp_path: Path, module):
    source = ROOT / module.EXPORT_MANIFEST_RELATIVE
    exports = json.loads(source.read_text(encoding="utf-8"))
    target = tmp_path / module.EXPORT_MANIFEST_RELATIVE
    target.parent.mkdir(parents=True, exist_ok=True)
    for figure in exports["figures"]:
        for output in figure["outputs"]:
            source_output, target_output = ROOT / output["path"], tmp_path / output["path"]
            target_output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_output, target_output)
    target.write_text(json.dumps(exports, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return exports


def rewrite_tree(path: Path, mutate) -> None:
    tree = ET.parse(path)
    mutate(tree)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def cell(tree: ET.ElementTree, cell_id: str):
    return next(item for item in tree.getroot().iter("mxCell") if item.get("id") == cell_id)


def test_repository_package_is_valid() -> None:
    assert load_module().validate_package() == []


def test_all_nine_redraws_are_draft_and_source_bound() -> None:
    data = load_module().load_manifest()
    assert len(data["figures"]) == 9
    assert {f["status"] for f in data["figures"]} == {"DRAFT-REDRAW"}
    for figure in data["figures"]:
        bindings = figure["sourceBindings"]
        assert set(bindings["objects"]) == {r["id"] for r in figure["groups"] + figure["entities"]}
        assert set(bindings["relations"]) == {r["id"] for r in figure["relations"]}
        assert set(bindings["notes"]) == {r["id"] for r in figure["notes"]}


def test_fig05_preserves_effect_and_update_partition() -> None:
    figure = load_module().load_manifest()["figures"][4]
    edges = {r["id"]: (r["source"], r["target"], r.get("guardRef")) for r in figure["relations"]}
    assert edges["E-S6-S7"] == ("S6", "S7", "G-EFFECT")
    assert edges["E-CONFIRM-S8"] == ("RecoverConfirmed", "S8", "G-RECOVER")
    assert edges["E-CONFIRM-S9"] == ("RecoverConfirmed", "S9", "G-TEST-PREP")
    assert "Unconfirmed" not in {r["id"] for r in figure["entities"]}
    assert ("S3", "SpecError") in {(r["source"], r["target"]) for r in figure["relations"]}
    labels = {r["id"]: r["label"] for r in figure["relations"]}
    assert labels["E-S2-S3"] == "not G-GAP"
    assert "unless effect class already returned" in next(r["label"] for r in figure["entities"] if r["id"] == "S6")


def test_fig06_routes_protocol_observation_through_session() -> None:
    figure = load_module().load_manifest()["figures"][5]
    edges = {(r["source"], r["target"]) for r in figure["relations"]}
    assert ("Observation", "ReceiveObservation") in edges
    assert ("ReceiveObservation", "Analyse") in edges
    assert ("Observation", "Analyse") not in edges


def test_fig07_records_error_guard_order_and_four_witnesses() -> None:
    figure = load_module().load_manifest()["figures"][6]
    refs = [r.get("guardRef") for r in figure["relations"] if r["source"] == "ErrorHandle"]
    assert refs == ["CAP", "E-A4", "E-A5", "NOT-SENT", "E-RETRY"]
    notes = "\n".join(r["label"] for r in figure["notes"])
    for witness in ("E-A4", "E-A5", "NOT-SENT", "E-RETRY"):
        assert witness in notes
    for relation in figure["relations"]:
        if relation.get("guardRef"):
            assert relation["label"].strip()


def test_fig09_preserves_truth_validity_denominators_and_interface_boundary() -> None:
    figure = load_module().load_manifest()["figures"][8]
    entities = {row["id"]: row["label"] for row in figure["entities"]}
    relations = {row["id"]: row["label"] for row in figure["relations"]}
    notes = {row["id"]: row["label"] for row in figure["notes"]}
    assert "missing" in entities["Valid"]
    assert relations["scene-truth"] == "INJECT-CONFIRM"
    assert relations["valid-metrics"] == "ATTEMPT/ANSWERED DENOM."
    assert "INJECT-CONFIRM = injection plan + execution confirmation" in notes["relation-legend"]
    assert "ATTEMPT/ANSWERED DENOM. = attempt and answered-subset denominators" in notes["relation-legend"]
    for interface in ("IF-OBS-INTERPRET", "IF-PREP-RECOVER", "IF-EQUIV", "IF-RESOURCE-STOP", "IF-EXP-EVAL"):
        assert interface in notes["truth-boundary"]


def test_generated_drawio_keeps_editable_text_and_semantic_ids() -> None:
    module = load_module()
    root = module.build_tree(module.load_manifest()["figures"][8]).getroot()
    cells = {item.get("id"): item for item in root.iter("mxCell")}
    assert cells["node-Truth"].get("value") == "Independent truth record<br>evaluator only"
    assert cells["edge-truth-arms"].get("semanticRole") == "forbidden"
    assert cells["edge-truth-arms"].get("source") == "node-Truth"
    assert cells["edge-truth-arms"].get("target") == "node-Arms"


def test_html_label_round_trip_preserves_literal_constraints_and_entities() -> None:
    module = load_module()
    for label in ("<<constraint>>", "a < b & c > d", "line one\nline <two>"):
        encoded = module.label_value(label)
        assert module.normalized_label(encoded) == label
        assert "<constraint>" not in encoded


def test_crlf_and_lf_have_same_canonical_identity(tmp_path: Path) -> None:
    module = load_module()
    lf, crlf = tmp_path / "lf.puml", tmp_path / "crlf.puml"
    lf.write_bytes(b"alpha\nbeta\n")
    crlf.write_bytes(b"alpha\r\nbeta\r\n")
    assert module.sha256(lf) == module.sha256(crlf)


def test_content_drift_changes_canonical_identity(tmp_path: Path) -> None:
    module = load_module()
    path = tmp_path / "source.puml"
    path.write_text("alpha\n", encoding="utf-8")
    before = module.sha256(path)
    path.write_text("beta\n", encoding="utf-8")
    assert module.sha256(path) != before


@pytest.mark.parametrize("value", ["../escape.puml", "/absolute/escape.puml", "C" + ":/escape.puml", "dir\\escape.puml", "dir/./escape.puml"])
def test_safe_path_rejects_nonportable_or_escaping_paths(value: str) -> None:
    with pytest.raises(ValueError):
        load_module().safe_path(value, suffix=".puml")


def test_safe_path_rejects_wrong_suffix() -> None:
    with pytest.raises(ValueError):
        load_module().safe_path("docs/source.svg", suffix=".puml")


def test_safe_path_rejects_symlink_escape(tmp_path: Path) -> None:
    module = load_module()
    outside = tmp_path.parent / (tmp_path.name + "-outside")
    outside.mkdir()
    link = tmp_path / "linked"
    try:
        os.symlink(outside, link, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation is unavailable")
    with pytest.raises(ValueError):
        module.safe_path("linked/file.puml", suffix=".puml", root=tmp_path)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda f: f["sourceBindings"].pop("title"), "title is required"),
        (lambda f: f["sourceBindings"]["notes"].pop(next(iter(f["sourceBindings"]["notes"]))), "notes ids differ"),
        (lambda f: f["sourceBindings"].pop("manualReview"), "manualReview"),
        (lambda f: f["sourceBindings"]["objects"].pop(next(iter(f["sourceBindings"]["objects"]))), "objects ids differ"),
        (lambda f: f["sourceBindings"]["relations"].pop(next(iter(f["sourceBindings"]["relations"]))), "relations ids differ"),
    ],
)
def test_manifest_rejects_incomplete_source_bindings(mutation, message: str) -> None:
    module = load_module()
    data = copy.deepcopy(module.load_manifest())
    mutation(data["figures"][0])
    assert any(message in error for error in module.validate_manifest(data))


def test_authority_rejects_missing_title_anchor(tmp_path: Path) -> None:
    module = load_module()
    data = copy_package(tmp_path, module)
    data["figures"][0]["sourceBindings"]["title"] = "title not present"
    assert any("complete title unit" in error for error in module.authority_errors(data, tmp_path))


def test_authority_rejects_missing_note_anchor(tmp_path: Path) -> None:
    module = load_module()
    data = copy_package(tmp_path, module)
    figure = data["figures"][0]
    note = next(iter(figure["sourceBindings"]["notes"]))
    figure["sourceBindings"]["notes"][note] = ["not present in PlantUML"]
    assert any("source notes anchor missing" in error for error in module.authority_errors(data, tmp_path))


def test_coordinated_note_inventory_binding_and_xml_deletion_is_rejected(tmp_path: Path) -> None:
    module = load_module()
    data = copy_package(tmp_path, module)
    figure = data["figures"][0]
    figure["notes"] = []
    figure["sourceBindings"]["notes"] = {}
    path = tmp_path / figure["drawioSource"]
    def mutate(tree):
        graph_root = next(node for node in tree.getroot().iter("root"))
        for item in list(graph_root):
            if (item.get("id") or "").startswith("note-"):
                graph_root.remove(item)
    rewrite_tree(path, mutate)
    figure["drawioSha256"] = module.sha256(path)
    assert any("unaccounted complete source note unit" in error for error in module.authority_errors(data, tmp_path))


def test_coordinated_manifest_xml_endpoint_drift_fails_source_binding() -> None:
    module = load_module()
    data = copy.deepcopy(module.load_manifest())
    relation = data["figures"][0]["relations"][0]
    relation["source"], relation["target"] = relation["target"], relation["source"]
    assert any("endpoints differ from manifest" in error for error in module.validate_manifest(data))


def test_coordinated_manifest_xml_parent_drift_fails_source_binding() -> None:
    module = load_module()
    data = copy.deepcopy(module.load_manifest())
    data["figures"][1]["entities"][0]["parent"] = "PCRS"
    assert any("parent differs from manifest" in error for error in module.validate_manifest(data))


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda tree: (cell(tree, "edge-request").set("source", "node-TestAdapter"), cell(tree, "edge-request").set("target", "node-Operator")), "endpoint drift"),
        (lambda tree: cell(tree, "edge-request").set("style", (cell(tree, "edge-request").get("style") or "") + "startArrow=block;"), "reversed start arrow"),
        (lambda tree: cell(tree, "edge-request").set("parent", "node-Operator"), "relation parent drift"),
        (lambda tree: cell(tree, "node-Operator").set("parent", "node-TestAdapter"), "parent/boundary drift"),
        (lambda tree: cell(tree, "node-Operator").set("semanticRole", "core"), "semantic role drift"),
        (lambda tree: cell(tree, "edge-request").set("semanticRole", "stop"), "relation role drift"),
        (lambda tree: cell(tree, "node-Operator").set("value", "changed"), "label drift"),
        (lambda tree: cell(tree, "edge-request").set("value", "changed"), "relation label drift"),
    ],
)
def test_xml_semantic_mutations_are_rejected(tmp_path: Path, mutation, message: str) -> None:
    module = load_module()
    data = copy_package(tmp_path, module)
    figure = data["figures"][0]
    path = tmp_path / figure["drawioSource"]
    rewrite_tree(path, mutation)
    figure["drawioSha256"] = module.sha256(path)
    assert any(message in error for error in module.validate_figure(figure, tmp_path))


@pytest.mark.parametrize("mutation", ["cell", "ancestor"])
def test_hidden_semantic_cells_and_collapsed_ancestors_are_rejected(tmp_path: Path, mutation: str) -> None:
    module = load_module()
    data = copy_package(tmp_path, module)
    figure = data["figures"][1]
    path = tmp_path / figure["drawioSource"]
    def change(tree):
        if mutation == "cell":
            cell(tree, "edge-goals-to-crs").set("visible", "0")
        else:
            cell(tree, "group-MG").set("collapsed", "1")
    rewrite_tree(path, change)
    figure["drawioSha256"] = module.sha256(path)
    assert any("hidden or inside collapsed ancestor" in error for error in module.validate_figure(figure, tmp_path))


def test_missing_relation_is_rejected(tmp_path: Path) -> None:
    module = load_module()
    data = copy_package(tmp_path, module)
    figure = data["figures"][0]
    path = tmp_path / figure["drawioSource"]
    def mutate(tree):
        edge = cell(tree, "edge-request")
        next(parent for parent in tree.getroot().iter() if edge in list(parent)).remove(edge)
    rewrite_tree(path, mutate)
    figure["drawioSha256"] = module.sha256(path)
    assert any("missing semantic relation edge-request" in e for e in module.validate_figure(figure, tmp_path))


def test_undeclared_rendered_cell_is_rejected(tmp_path: Path) -> None:
    module = load_module()
    data = copy_package(tmp_path, module)
    figure = data["figures"][0]
    path = tmp_path / figure["drawioSource"]
    def mutate(tree):
        graph_root = next(node for node in tree.getroot().iter("root"))
        ET.SubElement(graph_root, "mxCell", {"id": "rogue", "vertex": "1", "parent": "1"})
    rewrite_tree(path, mutate)
    figure["drawioSha256"] = module.sha256(path)
    assert any("undeclared rendered/semantic cells" in e for e in module.validate_figure(figure, tmp_path))


def test_duplicate_xml_id_is_rejected(tmp_path: Path) -> None:
    module = load_module()
    data = copy_package(tmp_path, module)
    figure = data["figures"][0]
    path = tmp_path / figure["drawioSource"]
    def mutate(tree):
        graph_root = next(node for node in tree.getroot().iter("root"))
        ET.SubElement(graph_root, "mxCell", {"id": "node-Operator", "vertex": "1", "parent": "1"})
    rewrite_tree(path, mutate)
    figure["drawioSha256"] = module.sha256(path)
    assert any("duplicate mxCell ids" in e for e in module.validate_figure(figure, tmp_path))


def test_build_preflight_missing_authority_writes_nothing(tmp_path: Path) -> None:
    module = load_module()
    data = copy_package(tmp_path, module)
    (tmp_path / data["figures"][0]["sourcePuml"]).unlink()
    before = {(tmp_path / f["drawioSource"]): (tmp_path / f["drawioSource"]).read_bytes() for f in data["figures"]}
    assert module.build(data, missing_only=False, force=True, root=tmp_path) == 1
    assert all(path.read_bytes() == payload for path, payload in before.items())


def test_build_preflight_generated_hash_mismatch_writes_nothing(tmp_path: Path) -> None:
    module = load_module()
    data = copy_package(tmp_path, module)
    data["figures"][4]["drawioSha256"] = "0" * 64
    before = {(tmp_path / f["drawioSource"]): (tmp_path / f["drawioSource"]).read_bytes() for f in data["figures"]}
    assert module.build(data, missing_only=False, force=True, root=tmp_path) == 1
    assert all(path.read_bytes() == payload for path, payload in before.items())


def test_build_rolls_back_after_install_failure(tmp_path: Path, monkeypatch) -> None:
    module = load_module()
    data = copy_package(tmp_path, module)
    before = {(tmp_path / f["drawioSource"]): (tmp_path / f["drawioSource"]).read_bytes() for f in data["figures"]}
    real_replace, calls = module.os.replace, 0
    def flaky(source, target):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("injected install failure")
        return real_replace(source, target)
    monkeypatch.setattr(module.os, "replace", flaky)
    assert module.build(data, missing_only=False, force=True, root=tmp_path) == 1
    assert all(path.read_bytes() == payload for path, payload in before.items())


def test_generated_payload_hashes_match_manifest() -> None:
    module = load_module()
    for figure in module.load_manifest()["figures"]:
        payload = module._tree_bytes(module.build_tree(figure))
        assert hashlib.sha256(module.canonical_text(payload)).hexdigest() == figure["drawioSha256"]


def test_export_registry_rejects_stale_drawio_identity(tmp_path: Path) -> None:
    module = load_module()
    data = copy_package(tmp_path, module)
    copy_exports(tmp_path, module)
    data["figures"][0]["drawioSha256"] = "0" * 64
    assert any("export Draw.io identity is stale" in error for error in module.export_errors(data, tmp_path))


@pytest.mark.parametrize("mutation", ["missing", "changed"])
def test_export_registry_rejects_missing_or_changed_output(tmp_path: Path, mutation: str) -> None:
    module = load_module()
    data = copy_package(tmp_path, module)
    exports = copy_exports(tmp_path, module)
    output = tmp_path / exports["figures"][0]["outputs"][0]["path"]
    if mutation == "missing":
        output.unlink()
    else:
        output.write_bytes(output.read_bytes() + b"drift")
    errors = module.export_errors(data, tmp_path)
    assert any(("missing declared export" if mutation == "missing" else "raw export identity drift") in error for error in errors)


def test_export_registry_rejects_caption_change_without_identity_refresh(tmp_path: Path) -> None:
    module = load_module()
    data = copy_package(tmp_path, module)
    exports = copy_exports(tmp_path, module)
    exports["figures"][0]["caption"] += " changed"
    path = tmp_path / module.EXPORT_MANIFEST_RELATIVE
    path.write_text(json.dumps(exports, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert any("export caption identity is invalid" in error for error in module.export_errors(data, tmp_path))
