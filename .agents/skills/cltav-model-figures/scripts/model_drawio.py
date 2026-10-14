"""Build and validate semantic-preserving CL-TAV Draw.io redraw sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
MANIFEST = ROOT / "configs/research/cltav_model_figure_manifest.json"

ROLE_STYLES = {
    "core": ("#DCE6F1", "#315A7D", "rounded=1"),
    "external": ("#F2F2F2", "#666666", "rounded=1"),
    "evidence": ("#FFF2CC", "#9A7B1F", "rounded=1"),
    "planned": ("#FFF2CC", "#9A7B1F", "rounded=1;dashed=1"),
    "risk": ("#FCE8E6", "#B85450", "rounded=1"),
    "stop": ("#FCE8E6", "#B85450", "rounded=1"),
    "retry": ("#FCE5CD", "#C47A1B", "rounded=1;dashed=1"),
    "truth": ("#EDE7F6", "#6A4C93", "rounded=1"),
    "decision": ("#E2F0D9", "#548235", "rhombus"),
    "constraint": ("#E8EDF3", "#486581", "rounded=1"),
    "port": ("#FFFFFF", "#315A7D", "rounded=0"),
    "state": ("#DCE6F1", "#315A7D", "rounded=1"),
}

EDGE_STYLES = {
    "association": "endArrow=none;",
    "dependency": "dashed=1;endArrow=open;",
    "evidence-only": "dashed=1;endArrow=open;strokeColor=#9A7B1F;",
    "evaluation": "endArrow=block;strokeColor=#6A4C93;",
    "feedback": "dashed=1;endArrow=block;strokeColor=#315A7D;",
    "forbidden": "dashed=1;endArrow=block;strokeColor=#B85450;fontColor=#9C0006;",
    "observation": "dashed=1;endArrow=block;strokeColor=#315A7D;",
    "planned": "dashed=1;endArrow=open;strokeColor=#9A7B1F;",
    "retry": "dashed=1;endArrow=block;strokeColor=#C47A1B;",
    "risk": "dashed=1;endArrow=block;strokeColor=#B85450;",
    "stop": "endArrow=block;strokeColor=#B85450;",
    "trace": "endArrow=open;strokeColor=#9A7B1F;",
    "constraint-link": "endArrow=none;strokeColor=#486581;",
    "continue": "dashed=1;endArrow=block;strokeColor=#315A7D;",
    "transition": "endArrow=block;strokeColor=#315A7D;",
    "sequence": "endArrow=block;strokeColor=#315A7D;",
    "flow": "endArrow=block;strokeColor=#315A7D;",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def label_value(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")


def normalized_label(value: str | None) -> str:
    text = value or ""
    return text.replace("<br/>", "\n").replace("<br />", "\n").replace("<br>", "\n")


def node_style(role: str) -> str:
    fill, stroke, shape = ROLE_STYLES.get(role, ROLE_STYLES["core"])
    return (
        f"{shape};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
        "strokeWidth=1.25;fontFamily=Helvetica;fontSize=12;fontColor=#1F1F1F;"
        "align=center;verticalAlign=middle;spacing=6;shadow=0;glass=0;gradientColor=none;"
    )


def group_style(role: str) -> str:
    fill, stroke, _ = ROLE_STYLES.get(role, ("#F7F9FB", "#7F8C99", ""))
    return (
        "swimlane;horizontal=1;startSize=30;rounded=1;whiteSpace=wrap;html=1;"
        f"fillColor={fill};swimlaneFillColor=#FFFFFF;strokeColor={stroke};"
        "strokeWidth=1.25;fontFamily=Helvetica;fontSize=12;fontStyle=1;"
        "fontColor=#1F1F1F;shadow=0;glass=0;gradientColor=none;"
    )


def note_style() -> str:
    return (
        "shape=note;whiteSpace=wrap;html=1;fillColor=#FAFAFA;strokeColor=#8C8C8C;"
        "strokeWidth=1;fontFamily=Helvetica;fontSize=11;fontColor=#333333;"
        "align=left;verticalAlign=middle;spacing=8;shadow=0;glass=0;gradientColor=none;"
    )


def edge_style(row: dict[str, Any]) -> str:
    semantic = EDGE_STYLES.get(row["role"], EDGE_STYLES["flow"])
    routing = ""
    for key in ("exitX", "exitY", "entryX", "entryY"):
        if key in row:
            routing += f"{key}={row[key]};"
    if "exitX" in row or "exitY" in row:
        routing += "exitDx=0;exitDy=0;exitPerimeter=1;"
    if "entryX" in row or "entryY" in row:
        routing += "entryDx=0;entryDy=0;entryPerimeter=1;"
    return (
        "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;"
        "html=1;strokeWidth=1.25;fontFamily=Helvetica;fontSize=11;"
        "fontColor=#1F1F1F;labelBackgroundColor=#FFFFFF;" + semantic + routing
    )


def geometry(parent: ET.Element, row: dict[str, Any], *, relative: bool = False) -> None:
    attrs = {"as": "geometry"}
    if relative:
        attrs["relative"] = "1"
        if "labelX" in row:
            attrs["x"] = str(row["labelX"])
        if "labelY" in row:
            attrs["y"] = str(row["labelY"])
    else:
        for key in ("x", "y", "w", "h"):
            attrs[{"w": "width", "h": "height"}.get(key, key)] = str(row[key])
    geometry_node = ET.SubElement(parent, "mxGeometry", attrs)
    if relative and row.get("points"):
        points = ET.SubElement(geometry_node, "Array", {"as": "points"})
        for point in row["points"]:
            ET.SubElement(points, "mxPoint", {"x": str(point[0]), "y": str(point[1])})


def build_tree(figure: dict[str, Any]) -> ET.ElementTree:
    canvas = figure["canvas"]
    mxfile = ET.Element(
        "mxfile",
        {
            "host": "app.diagrams.net",
            "agent": "cltav-model-figures/1.0",
            "version": "24.7.17",
            "type": "device",
            "compressed": "false",
        },
    )
    diagram = ET.SubElement(
        mxfile,
        "diagram",
        {"id": figure["id"].lower(), "name": figure["id"]},
    )
    model = ET.SubElement(
        diagram,
        "mxGraphModel",
        {
            "dx": "0",
            "dy": "0",
            "grid": "1",
            "gridSize": "10",
            "guides": "1",
            "tooltips": "1",
            "connect": "1",
            "arrows": "1",
            "fold": "1",
            "page": "1",
            "pageScale": "1",
            "pageWidth": str(canvas["width"]),
            "pageHeight": str(canvas["height"]),
            "math": "1",
            "shadow": "0",
        },
    )
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    group_ids = {row["id"] for row in figure.get("groups", [])}
    entity_ids = {row["id"] for row in figure.get("entities", [])}
    known_ids = group_ids | entity_ids

    for row in figure.get("groups", []):
        cell = ET.SubElement(
            root,
            "mxCell",
            {
                "id": f"group-{row['id']}",
                "value": label_value(row["label"]),
                "style": group_style(row["role"]),
                "vertex": "1",
                "parent": "1",
                "semanticKind": "group",
                "semanticRole": row["role"],
            },
        )
        geometry(cell, row)

    for row in figure.get("entities", []):
        parent_id = row.get("parent")
        if parent_id and parent_id not in group_ids:
            raise ValueError(f"{figure['id']} entity {row['id']} has unknown parent {parent_id}")
        cell = ET.SubElement(
            root,
            "mxCell",
            {
                "id": f"node-{row['id']}",
                "value": label_value(row["label"]),
                "style": node_style(row["role"]),
                "vertex": "1",
                "parent": f"group-{parent_id}" if parent_id else "1",
                "semanticKind": "entity",
                "semanticRole": row["role"],
            },
        )
        geometry(cell, row)

    for row in figure.get("notes", []):
        cell = ET.SubElement(
            root,
            "mxCell",
            {
                "id": f"note-{row['id']}",
                "value": label_value(row["label"]),
                "style": note_style(),
                "vertex": "1",
                "parent": "1",
                "semanticKind": "note",
                "semanticRole": "interpretation-boundary",
            },
        )
        geometry(cell, row)

    for row in figure.get("relations", []):
        if row["source"] not in known_ids or row["target"] not in known_ids:
            raise ValueError(
                f"{figure['id']} relation {row['id']} has unknown endpoints "
                f"{row['source']}->{row['target']}"
            )
        source_prefix = "group" if row["source"] in group_ids else "node"
        target_prefix = "group" if row["target"] in group_ids else "node"
        cell = ET.SubElement(
            root,
            "mxCell",
            {
                "id": f"edge-{row['id']}",
                "value": label_value(row["label"]),
                "style": edge_style(row),
                "edge": "1",
                "parent": "1",
                "source": f"{source_prefix}-{row['source']}",
                "target": f"{target_prefix}-{row['target']}",
                "semanticKind": "relation",
                "semanticRole": row["role"],
            },
        )
        geometry(cell, row, relative=True)

    ET.indent(mxfile, space="  ")
    return ET.ElementTree(mxfile)


def validate_manifest(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schemaVersion") != "1.0":
        errors.append("manifest schemaVersion must be 1.0")
    figures = data.get("figures")
    if not isinstance(figures, list) or len(figures) != 9:
        errors.append("manifest must contain the nine FIG-CL-TAV redraws")
        return errors
    figure_ids: set[str] = set()
    drawio_paths: set[str] = set()
    for figure in figures:
        figure_id = figure.get("id")
        if not isinstance(figure_id, str) or figure_id in figure_ids:
            errors.append(f"duplicate or missing figure id: {figure_id!r}")
            continue
        figure_ids.add(figure_id)
        drawio = figure.get("drawioSource")
        if not isinstance(drawio, str) or drawio in drawio_paths:
            errors.append(f"{figure_id} duplicate or missing drawioSource")
        else:
            drawio_paths.add(drawio)
        for hash_field in ("sourceSha256", "drawioSha256"):
            hash_value = figure.get(hash_field)
            if (
                not isinstance(hash_value, str)
                or len(hash_value) != 64
                or any(character not in "0123456789abcdef" for character in hash_value)
            ):
                errors.append(f"{figure_id} has invalid {hash_field}")
        semantic_ids: set[str] = set()
        for collection in ("groups", "entities", "notes"):
            for row in figure.get(collection, []):
                row_id = row.get("id")
                if not isinstance(row_id, str) or not row_id or row_id in semantic_ids:
                    errors.append(f"{figure_id} duplicate or missing {collection} id: {row_id!r}")
                semantic_ids.add(str(row_id))
        relation_ids: set[str] = set()
        endpoint_ids = {
            row.get("id")
            for collection in ("groups", "entities")
            for row in figure.get(collection, [])
        }
        for row in figure.get("relations", []):
            row_id = row.get("id")
            if not isinstance(row_id, str) or not row_id or row_id in relation_ids:
                errors.append(f"{figure_id} duplicate or missing relation id: {row_id!r}")
            relation_ids.add(str(row_id))
            if row.get("source") not in endpoint_ids or row.get("target") not in endpoint_ids:
                errors.append(
                    f"{figure_id} relation {row_id} has unknown endpoints "
                    f"{row.get('source')}->{row.get('target')}"
                )
            for key in ("exitX", "exitY", "entryX", "entryY", "labelX", "labelY"):
                value = row.get(key)
                if value is not None and (
                    isinstance(value, bool) or not isinstance(value, (int, float))
                ):
                    errors.append(f"{figure_id} relation {row_id} has nonnumeric {key}")
            points = row.get("points")
            if points is not None and (
                not isinstance(points, list)
                or any(
                    not isinstance(point, list)
                    or len(point) != 2
                    or any(
                        isinstance(value, bool) or not isinstance(value, (int, float))
                        for value in point
                    )
                    for point in points
                )
            ):
                errors.append(f"{figure_id} relation {row_id} has invalid route points")
    expected = {f"FIG-CL-TAV-{index:02d}" for index in range(1, 10)}
    if figure_ids != expected:
        errors.append(f"figure id set mismatch: {sorted(figure_ids)}")
    return errors


def validate_figure(figure: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    figure_id = figure["id"]
    source = ROOT / figure["sourcePuml"]
    output = ROOT / figure["drawioSource"]
    if not source.is_file():
        return [f"{figure_id}: missing PlantUML authority {figure['sourcePuml']}"]
    actual_hash = sha256(source)
    if actual_hash != figure["sourceSha256"]:
        errors.append(
            f"{figure_id}: PlantUML hash drift {actual_hash}; "
            f"expected {figure['sourceSha256']}"
        )
    if not output.is_file():
        return errors + [f"{figure_id}: missing Draw.io source {figure['drawioSource']}"]
    actual_output_hash = sha256(output)
    if actual_output_hash != figure["drawioSha256"]:
        errors.append(
            f"{figure_id}: Draw.io hash drift {actual_output_hash}; "
            f"expected {figure['drawioSha256']}"
        )
    try:
        root = ET.parse(output).getroot()
    except (OSError, ET.ParseError) as exc:
        return errors + [f"{figure_id}: unreadable Draw.io XML: {exc}"]
    if root.tag != "mxfile" or root.get("compressed") != "false":
        errors.append(f"{figure_id}: Draw.io source must be uncompressed mxfile XML")
    cells = {cell.get("id"): cell for cell in root.iter("mxCell") if cell.get("id")}
    if "0" not in cells or "1" not in cells:
        errors.append(f"{figure_id}: Draw.io root cells 0 and 1 are required")

    expected_semantic: set[str] = set()
    groups = {row["id"] for row in figure.get("groups", [])}
    for kind, prefix in (("groups", "group"), ("entities", "node"), ("notes", "note")):
        for row in figure.get(kind, []):
            cell_id = f"{prefix}-{row['id']}"
            expected_semantic.add(cell_id)
            cell = cells.get(cell_id)
            if cell is None:
                errors.append(f"{figure_id}: missing semantic cell {cell_id}")
                continue
            if normalized_label(cell.get("value")) != row["label"]:
                errors.append(f"{figure_id}: label drift in {cell_id}")
            expected_role = row.get("role", "interpretation-boundary")
            if kind == "notes":
                expected_role = "interpretation-boundary"
            if cell.get("semanticRole") != expected_role:
                errors.append(f"{figure_id}: semantic role drift in {cell_id}")
            style = cell.get("style") or ""
            if "fontFamily=Helvetica" not in style or "shadow=0" not in style:
                errors.append(f"{figure_id}: style contract missing in {cell_id}")
            if "image=" in style or "gradientColor=none" not in style:
                errors.append(f"{figure_id}: prohibited image/gradient styling in {cell_id}")

    for row in figure.get("relations", []):
        cell_id = f"edge-{row['id']}"
        expected_semantic.add(cell_id)
        cell = cells.get(cell_id)
        if cell is None:
            errors.append(f"{figure_id}: missing semantic relation {cell_id}")
            continue
        source_prefix = "group" if row["source"] in groups else "node"
        target_prefix = "group" if row["target"] in groups else "node"
        expected_source = f"{source_prefix}-{row['source']}"
        expected_target = f"{target_prefix}-{row['target']}"
        if cell.get("source") != expected_source or cell.get("target") != expected_target:
            errors.append(
                f"{figure_id}: endpoint drift in {cell_id}: "
                f"{cell.get('source')}->{cell.get('target')}"
            )
        if normalized_label(cell.get("value")) != row["label"]:
            errors.append(f"{figure_id}: relation label drift in {cell_id}")
        if cell.get("semanticRole") != row["role"]:
            errors.append(f"{figure_id}: relation role drift in {cell_id}")
        geometry_node = cell.find("mxGeometry")
        if geometry_node is None or geometry_node.get("relative") != "1":
            errors.append(f"{figure_id}: edge geometry missing in {cell_id}")

    actual_semantic = {
        cell_id
        for cell_id, cell in cells.items()
        if cell.get("semanticKind") in {"group", "entity", "note", "relation"}
    }
    unexpected = sorted(actual_semantic - expected_semantic)
    if unexpected:
        errors.append(f"{figure_id}: undeclared semantic cells: {', '.join(unexpected)}")
    return errors


def build(data: dict[str, Any], *, missing_only: bool, force: bool) -> int:
    wrote = 0
    for figure in data["figures"]:
        output = ROOT / figure["drawioSource"]
        if output.exists() and missing_only:
            continue
        if output.exists() and not force:
            print(f"refusing to overwrite {output.relative_to(ROOT).as_posix()}; use --force")
            return 2
        output.parent.mkdir(parents=True, exist_ok=True)
        tree = build_tree(figure)
        tree.write(output, encoding="utf-8", xml_declaration=True, short_empty_elements=True)
        wrote += 1
        print(f"wrote {output.relative_to(ROOT).as_posix()}")
    print(f"Draw.io build complete: wrote={wrote}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-missing", action="store_true", help="create only absent Draw.io drafts")
    parser.add_argument("--force", action="store_true", help="replace all Draw.io drafts from the manifest")
    parser.add_argument("--check", action="store_true", help="validate source hashes and semantic equality")
    parser.add_argument("--summary", action="store_true", help="print compact figure inventory")
    args = parser.parse_args()
    if not any((args.build_missing, args.force, args.check, args.summary)):
        parser.error("select --build-missing, --force, --check, or --summary")

    try:
        data = load_manifest()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot load {MANIFEST.relative_to(ROOT).as_posix()}: {exc}")
        return 1
    errors = validate_manifest(data)
    if errors:
        print("Model figure manifest failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    if args.force or args.build_missing:
        result = build(data, missing_only=args.build_missing, force=args.force)
        if result:
            return result
    if args.check:
        for figure in data["figures"]:
            errors.extend(validate_figure(figure))
        if errors:
            print("Model Draw.io check failed:")
            for error in errors:
                print(f"  - {error}")
            return 1
        print(f"Model Draw.io check passed: figures={len(data['figures'])}")
    if args.summary:
        print(f"manifest={data['manifestId']} figures={len(data['figures'])}")
        for figure in data["figures"]:
            print(
                f"{figure['id']} {figure['diagramType']} {figure['status']} "
                f"entities={len(figure['entities'])} relations={len(figure['relations'])} "
                f"drawio={figure['drawioSource']}"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
