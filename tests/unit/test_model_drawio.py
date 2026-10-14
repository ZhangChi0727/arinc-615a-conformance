from __future__ import annotations

import copy
import importlib.util
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".agents/skills/cltav-model-figures/scripts/model_drawio.py"


def load_module():
    spec = importlib.util.spec_from_file_location("cltav_model_drawio", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_repository_model_drawio_sources_are_semantically_valid() -> None:
    module = load_module()
    data = module.load_manifest()
    assert module.validate_manifest(data) == []
    errors = [error for figure in data["figures"] for error in module.validate_figure(figure)]
    assert errors == []


def test_validator_rejects_reversed_semantic_edge(tmp_path: Path) -> None:
    module = load_module()
    data = module.load_manifest()
    figure = copy.deepcopy(data["figures"][0])
    source = ROOT / figure["sourcePuml"]
    drawio = ROOT / figure["drawioSource"]
    test_source = tmp_path / figure["sourcePuml"]
    test_drawio = tmp_path / figure["drawioSource"]
    test_source.parent.mkdir(parents=True)
    test_drawio.parent.mkdir(parents=True)
    shutil.copy2(source, test_source)
    tree = ET.parse(drawio)
    edge = next(cell for cell in tree.getroot().iter("mxCell") if cell.get("id") == "edge-request")
    edge.set("source", "node-TestAdapter")
    edge.set("target", "node-Operator")
    tree.write(test_drawio, encoding="utf-8", xml_declaration=True)
    old_root = module.ROOT
    try:
        module.ROOT = tmp_path
        errors = module.validate_figure(figure)
    finally:
        module.ROOT = old_root
    assert any("endpoint drift" in error for error in errors)


def test_generated_drawio_keeps_editable_text_and_semantic_ids() -> None:
    module = load_module()
    figure = module.load_manifest()["figures"][8]
    root = module.build_tree(figure).getroot()
    cells = {cell.get("id"): cell for cell in root.iter("mxCell")}
    assert cells["node-Truth"].get("value") == "Independent truth record<br>evaluator only"
    assert cells["edge-truth-arms"].get("semanticRole") == "forbidden"
    assert cells["edge-truth-arms"].get("source") == "node-Truth"
    assert cells["edge-truth-arms"].get("target") == "node-Arms"


def test_generated_drawio_materializes_nonsemantic_route_controls() -> None:
    module = load_module()
    figure = module.load_manifest()["figures"][4]
    root = module.build_tree(figure).getroot()
    edge = next(
        cell
        for cell in root.iter("mxCell")
        if cell.get("id") == "edge-E-S7-S1"
    )
    assert "exitX=1;" in (edge.get("style") or "")
    geometry = edge.find("mxGeometry")
    assert geometry is not None
    assert geometry.get("relative") == "1"
    assert geometry.get("y") == "-14"
    points = geometry.find("Array")
    assert points is not None
    assert [(point.get("x"), point.get("y")) for point in points] == [
        ("1305", "789"),
        ("1305", "115"),
        ("490", "115"),
    ]
