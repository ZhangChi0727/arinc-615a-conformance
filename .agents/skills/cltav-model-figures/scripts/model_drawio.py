"""Build and validate controlled CL-TAV Draw.io model candidates."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import stat
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
MANIFEST_RELATIVE = Path("configs/research/cltav_model_figure_manifest.json")
EXPORT_MANIFEST_RELATIVE = Path("configs/research/cltav_model_figure_exports.json")
REVIEW_INDEX_RELATIVE = Path("artifacts/publications/cltav/model-drafts/MODEL_FIGURE_REVIEW_INDEX.md")
CANONICALIZATION = "UTF8-LF-v1"

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
    "boundary": ("#F7F9FB", "#7F8C99", "rounded=1"),
}

EDGE_STYLES = {
    "association": "endArrow=none;", "dependency": "dashed=1;endArrow=open;",
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


def canonical_text(raw: bytes) -> bytes:
    """Apply the named portable text identity policy used by the manifest."""
    return raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(canonical_text(path.read_bytes())).hexdigest()


def raw_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_sha256(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def model_content_sha256(figure: dict[str, Any]) -> str:
    """Identify the complete controlled candidate independently of its review."""
    keys = ("id", "sourcePuml", "sourceSha256", "drawioSource", "drawioSha256",
            "canvas", "typography", "groups", "entities", "notes", "relations",
            "sourceBindings")
    return json_sha256({key: figure.get(key) for key in keys})


def review_bundle_sha256(figure: dict[str, Any], caption: str) -> str:
    revision = figure.get("revision", {})
    return json_sha256({
        "figureId": figure.get("id"),
        "modelVersionId": revision.get("modelVersionId"),
        "modelContentSha256": revision.get("modelContentSha256"),
        "drawioSha256": figure.get("drawioSha256"),
        "caption": caption,
    })


def repository_root(root: Path | None = None) -> Path:
    return (root or ROOT).resolve()


def safe_path(relative: object, *, suffix: str, root: Path | None = None) -> Path:
    """Resolve a repository-relative ordinary file without following link escapes."""
    base = repository_root(root)
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ValueError("path must be a nonempty forward-slash repository-relative string")
    posix, windows = PurePosixPath(relative), PureWindowsPath(relative)
    if posix.is_absolute() or windows.is_absolute() or windows.drive or ":" in relative:
        raise ValueError(f"absolute/drive path is forbidden: {relative}")
    if any(part in {"", ".", ".."} for part in relative.split("/")):
        raise ValueError(f"path traversal is forbidden: {relative}")
    if posix.suffix != suffix:
        raise ValueError(f"expected {suffix} path: {relative}")
    target = base.joinpath(*posix.parts)
    target.resolve(strict=False).relative_to(base)
    cursor = target
    while cursor != base:
        if cursor.exists() or cursor.is_symlink():
            info = cursor.lstat()
            attributes = getattr(info, "st_file_attributes", 0)
            reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 1024)
            if stat.S_ISLNK(info.st_mode) or attributes & reparse:
                raise ValueError(f"link/reparse traversal is forbidden: {relative}")
            if cursor == target and not stat.S_ISREG(info.st_mode):
                raise ValueError(f"target is not an ordinary file: {relative}")
            if cursor != target and not stat.S_ISDIR(info.st_mode):
                raise ValueError(f"parent is not a directory: {relative}")
        cursor = cursor.parent
    return target


def load_manifest(root: Path | None = None) -> dict[str, Any]:
    return json.loads((repository_root(root) / MANIFEST_RELATIVE).read_text(encoding="utf-8"))


def label_value(value: str) -> str:
    text = value.replace("\r\n", "\n").replace("\r", "\n")
    return html.escape(text, quote=False).replace("\n", "<br>")


def normalized_label(value: str | None) -> str:
    text = (value or "").replace("<br/>", "\n").replace("<br />", "\n").replace("<br>", "\n")
    return html.unescape(text)


def _source_units(text: str) -> tuple[list[str], list[str]]:
    """Extract the finite title and note forms used by the nine frozen sources."""
    lines = text.splitlines()
    titles = [line.strip() for line in lines if line.strip().startswith("title ")]
    notes: list[str] = []
    start: int | None = None
    for index, line in enumerate(lines):
        stripped = line.strip()
        if start is None and stripped.startswith("note "):
            start = index
        elif start is not None and stripped == "end note":
            notes.append("\n".join(item.strip() for item in lines[start:index + 1]))
            start = None
    return titles, notes


def _relation_endpoints(anchor: str) -> tuple[str, str] | None:
    annotated = re.search(r"\bfrom=([^\s]+)\s+to=([^\s]+)", anchor)
    if annotated:
        return annotated.group(1), annotated.group(2)
    statement = re.match(r"^\s*([A-Za-z_][\w-]*)\s+(?:-\[[^]]+\])?(?:-->|\.\.>|\.\.|-)\s+([A-Za-z_][\w-]*)", anchor)
    return statement.groups() if statement else None


def node_style(role: str, font_size: float = 12) -> str:
    fill, stroke, shape = ROLE_STYLES[role]
    return (f"{shape};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
            f"strokeWidth=1.25;fontFamily=Helvetica;fontSize={font_size};fontColor=#1F1F1F;"
            "align=center;verticalAlign=middle;spacing=6;shadow=0;glass=0;gradientColor=none;")


def group_style(role: str, font_size: float = 12) -> str:
    fill, stroke, _ = ROLE_STYLES[role]
    return ("swimlane;horizontal=1;startSize=30;rounded=1;whiteSpace=wrap;html=1;"
            f"fillColor={fill};swimlaneFillColor=#FFFFFF;strokeColor={stroke};"
            f"strokeWidth=1.25;fontFamily=Helvetica;fontSize={font_size};fontStyle=1;"
            "fontColor=#1F1F1F;shadow=0;glass=0;gradientColor=none;")


def note_style(font_size: float = 11) -> str:
    return ("shape=note;whiteSpace=wrap;html=1;fillColor=#FAFAFA;strokeColor=#8C8C8C;"
            f"strokeWidth=1;fontFamily=Helvetica;fontSize={font_size};fontColor=#333333;"
            "align=left;verticalAlign=middle;spacing=8;shadow=0;glass=0;gradientColor=none;")


def edge_style(row: dict[str, Any], font_size: float = 11) -> str:
    routing = ""
    for key in ("exitX", "exitY", "entryX", "entryY"):
        if key in row:
            routing += f"{key}={row[key]};"
    if "exitX" in row or "exitY" in row:
        routing += "exitDx=0;exitDy=0;exitPerimeter=1;"
    if "entryX" in row or "entryY" in row:
        routing += "entryDx=0;entryDy=0;entryPerimeter=1;"
    return ("edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;"
            f"html=1;strokeWidth=1.25;fontFamily=Helvetica;fontSize={font_size};"
            "fontColor=#1F1F1F;labelBackgroundColor=#FFFFFF;" + EDGE_STYLES[row["role"]] + routing)


def geometry(parent: ET.Element, row: dict[str, Any], *, relative: bool = False) -> None:
    attrs = {"as": "geometry"}
    if relative:
        attrs["relative"] = "1"
        if "labelX" in row: attrs["x"] = str(row["labelX"])
        if "labelY" in row: attrs["y"] = str(row["labelY"])
    else:
        for key in ("x", "y", "w", "h"):
            attrs[{"w": "width", "h": "height"}.get(key, key)] = str(row[key])
    node = ET.SubElement(parent, "mxGeometry", attrs)
    if relative and row.get("points"):
        points = ET.SubElement(node, "Array", {"as": "points"})
        for point in row["points"]:
            ET.SubElement(points, "mxPoint", {"x": str(point[0]), "y": str(point[1])})


def build_tree(figure: dict[str, Any]) -> ET.ElementTree:
    canvas = figure["canvas"]
    typography = figure.get("typography", {})
    node_font, edge_font, note_font = (typography.get("nodePt", 12), typography.get("edgePt", 11), typography.get("notePt", 11))
    mxfile = ET.Element("mxfile", {"host": "app.diagrams.net", "agent": "cltav-model-figures/1.1", "version": "24.7.17", "type": "device", "compressed": "false"})
    diagram = ET.SubElement(mxfile, "diagram", {"id": figure["id"].lower(), "name": figure["id"]})
    model = ET.SubElement(diagram, "mxGraphModel", {"dx": "0", "dy": "0", "grid": "1", "gridSize": "10", "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1", "fold": "1", "page": "1", "pageScale": "1", "pageWidth": str(canvas["width"]), "pageHeight": str(canvas["height"]), "math": "1", "shadow": "0"})
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})
    group_ids = {row["id"] for row in figure.get("groups", [])}
    entity_ids = {row["id"] for row in figure.get("entities", [])}
    known_ids = group_ids | entity_ids
    for row in figure.get("groups", []):
        cell = ET.SubElement(root, "mxCell", {"id": f"group-{row['id']}", "value": label_value(row["label"]), "style": group_style(row["role"], node_font), "vertex": "1", "parent": "1", "semanticKind": "group", "semanticRole": row["role"], "authorityAlias": row.get("authorityAlias", row["id"])})
        geometry(cell, row)
    for row in figure.get("entities", []):
        parent_id = row.get("parent")
        if parent_id and parent_id not in group_ids: raise ValueError(f"{figure['id']} entity {row['id']} has unknown parent {parent_id}")
        cell = ET.SubElement(root, "mxCell", {"id": f"node-{row['id']}", "value": label_value(row["label"]), "style": node_style(row["role"], node_font), "vertex": "1", "parent": f"group-{parent_id}" if parent_id else "1", "semanticKind": "entity", "semanticRole": row["role"], "authorityAlias": row.get("authorityAlias", row["id"])})
        geometry(cell, row)
    for row in figure.get("notes", []):
        cell = ET.SubElement(root, "mxCell", {"id": f"note-{row['id']}", "value": label_value(row["label"]), "style": note_style(note_font), "vertex": "1", "parent": "1", "semanticKind": "note", "semanticRole": "interpretation-boundary", "sourceNote": row.get("sourceNote", row["id"])})
        geometry(cell, row)
    for row in figure.get("relations", []):
        if row["source"] not in known_ids or row["target"] not in known_ids: raise ValueError(f"{figure['id']} relation {row['id']} has unknown endpoints")
        source_prefix = "group" if row["source"] in group_ids else "node"
        target_prefix = "group" if row["target"] in group_ids else "node"
        attrs = {"id": f"edge-{row['id']}", "value": label_value(row["label"]), "style": edge_style(row, edge_font), "edge": "1", "parent": "1", "source": f"{source_prefix}-{row['source']}", "target": f"{target_prefix}-{row['target']}", "semanticKind": "relation", "semanticRole": row["role"]}
        if row.get("guardRef"): attrs["guardRef"] = row["guardRef"]
        cell = ET.SubElement(root, "mxCell", attrs)
        geometry(cell, row, relative=True)
    ET.indent(mxfile, space="  ")
    return ET.ElementTree(mxfile)


def _valid_hash(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def _binding_anchors(binding: object) -> object:
    if isinstance(binding, dict):
        return binding.get("anchors")
    return binding


def _anchor_map_errors(figure: dict[str, Any], key: str, expected: set[str]) -> list[str]:
    figure_id = figure.get("id", "<unknown>")
    bindings = figure.get("sourceBindings", {}).get(key)
    if not isinstance(bindings, dict): return [f"{figure_id} sourceBindings.{key} must be an object"]
    errors: list[str] = []
    if set(bindings) != expected: errors.append(f"{figure_id} sourceBindings.{key} ids differ from manifest inventory")
    inventory = {str(row["id"]): row for row in figure.get("groups", []) + figure.get("entities", [])} if key == "objects" else {str(row["id"]): row for row in figure.get("relations", [])}
    for row_id, binding in bindings.items():
        if isinstance(binding, dict):
            allowed = {"anchors", "parent"} if key == "objects" else {"anchors", "source", "target"}
            if set(binding) != allowed:
                errors.append(f"{figure_id} sourceBindings.{key}.{row_id} fields must be {sorted(allowed)}")
            row = inventory.get(row_id, {})
            if key == "objects" and binding.get("parent") != row.get("parent"):
                errors.append(f"{figure_id} sourceBindings.objects.{row_id} parent differs from manifest")
            if key == "relations" and (binding.get("source"), binding.get("target")) != (row.get("source"), row.get("target")):
                errors.append(f"{figure_id} sourceBindings.relations.{row_id} endpoints differ from manifest")
        anchors = _binding_anchors(binding)
        values = [anchors] if isinstance(anchors, str) else anchors
        if not isinstance(values, list) or not values or any(not isinstance(v, str) or not v for v in values): errors.append(f"{figure_id} sourceBindings.{key}.{row_id} needs nonempty text anchors")
    return errors


def validate_manifest(data: dict[str, Any], root: Path | None = None) -> list[str]:
    errors: list[str] = []
    if data.get("schemaVersion") != "2.0": errors.append("manifest schemaVersion must be 2.0")
    if data.get("textIdentity") != CANONICALIZATION: errors.append(f"manifest textIdentity must be {CANONICALIZATION}")
    figures = data.get("figures")
    if not isinstance(figures, list) or not figures: return errors + ["manifest must contain at least one registered model candidate"]
    figure_ids: set[str] = set(); paths: set[str] = set(); version_ids: set[str] = set()
    for figure in figures:
        figure_id = figure.get("id")
        if not isinstance(figure_id, str) or figure_id in figure_ids: errors.append(f"duplicate or missing figure id: {figure_id!r}"); continue
        figure_ids.add(figure_id)
        if figure.get("status") != "DRAFT-REDRAW": errors.append(f"{figure_id} must remain DRAFT-REDRAW pending human promotion")
        revision = figure.get("revision")
        if not isinstance(revision, dict):
            errors.append(f"{figure_id} revision record is required")
        else:
            version_id = revision.get("modelVersionId")
            if not isinstance(version_id, str) or not version_id or version_id in version_ids:
                errors.append(f"{figure_id} duplicate or missing modelVersionId")
            else:
                version_ids.add(version_id)
            if revision.get("disposition") not in {"RETAINED-DRAFT-INSTANCE", "REVISED-DRAFT-INSTANCE", "SPLIT-DRAFT-INSTANCE", "MERGED-DRAFT-INSTANCE", "RETIRED"}:
                errors.append(f"{figure_id} invalid revision disposition")
            if revision.get("revisionType") not in {"REFERENCE-REDRAW", "LAYOUT-ONLY", "SEMANTIC-CANDIDATE", "SPLIT", "MERGE", "RETIRE"}:
                errors.append(f"{figure_id} invalid revisionType")
            for field in ("reason", "affectedScope", "relatedContracts", "contractImpact"):
                if not revision.get(field): errors.append(f"{figure_id} revision.{field} is required")
            actual_content = model_content_sha256(figure)
            if revision.get("modelContentSha256") != actual_content:
                errors.append(f"{figure_id} model content identity is stale")
            inputs = revision.get("inputIdentity")
            if not isinstance(inputs, dict) or not all(inputs.get(key) for key in ("startingHead", "sourceSha256", "drawioSha256")):
                errors.append(f"{figure_id} revision.inputIdentity is incomplete")
            elif inputs.get("sourceSha256") != figure.get("sourceSha256") or inputs.get("drawioSha256") != figure.get("drawioSha256"):
                errors.append(f"{figure_id} revision input identity is stale")
            review = revision.get("semanticReview")
            if not isinstance(review, dict) or review.get("status") not in {"PENDING-INDEPENDENT-REVIEW", "ACCEPTED", "REJECTED"}:
                errors.append(f"{figure_id} semanticReview status is invalid")
            elif review.get("modelContentSha256") != actual_content:
                errors.append(f"{figure_id} semantic review is not bound to current content")
            elif review.get("status") == "PENDING-INDEPENDENT-REVIEW" and any(review.get(key) for key in ("reviewedBy", "reviewedAt", "decision")):
                errors.append(f"{figure_id} pending semantic review cannot claim a decision")
            elif review.get("status") in {"ACCEPTED", "REJECTED"} and not all(review.get(key) for key in ("reviewedBy", "reviewedAt", "decision")):
                errors.append(f"{figure_id} completed semantic review requires reviewer, date, and decision")
            if revision.get("promotionStatus") != "DRAFT-NOT-PROMOTED":
                errors.append(f"{figure_id} must remain DRAFT-NOT-PROMOTED")
        for key, suffix in (("sourcePuml", ".puml"), ("drawioSource", ".drawio")):
            value = figure.get(key)
            if not isinstance(value, str) or value in paths: errors.append(f"{figure_id} duplicate or missing {key}")
            else:
                paths.add(value)
                try: safe_path(value, suffix=suffix, root=root)
                except ValueError as exc: errors.append(f"{figure_id} unsafe {key}: {exc}")
        for field in ("sourceSha256", "drawioSha256"):
            if not _valid_hash(figure.get(field)): errors.append(f"{figure_id} has invalid {field}")
        groups, entities, notes, relations = (figure.get("groups", []), figure.get("entities", []), figure.get("notes", []), figure.get("relations", []))
        ids: set[str] = set()
        for collection, roles in ((groups, set(ROLE_STYLES)), (entities, set(ROLE_STYLES)), (notes, None)):
            if not isinstance(collection, list): errors.append(f"{figure_id} semantic collection must be a list"); continue
            for row in collection:
                row_id = row.get("id")
                if not isinstance(row_id, str) or not row_id or row_id in ids: errors.append(f"{figure_id} duplicate or missing semantic id: {row_id!r}")
                ids.add(str(row_id))
                if roles is not None and row.get("role") not in roles: errors.append(f"{figure_id} unknown semantic role in {row_id}: {row.get('role')}")
        group_ids = {row.get("id") for row in groups}; endpoint_ids = group_ids | {row.get("id") for row in entities}; relation_ids: set[str] = set()
        for row in relations:
            row_id = row.get("id")
            if not isinstance(row_id, str) or not row_id or row_id in relation_ids: errors.append(f"{figure_id} duplicate or missing relation id: {row_id!r}")
            relation_ids.add(str(row_id))
            if row.get("role") not in EDGE_STYLES: errors.append(f"{figure_id} unknown relation role in {row_id}: {row.get('role')}")
            if row.get("source") not in endpoint_ids or row.get("target") not in endpoint_ids: errors.append(f"{figure_id} relation {row_id} has unknown endpoints")
        object_ids = {str(row.get("id")) for row in groups + entities}; note_ids = {str(row.get("id")) for row in notes}
        errors.extend(_anchor_map_errors(figure, "objects", object_ids)); errors.extend(_anchor_map_errors(figure, "relations", relation_ids)); errors.extend(_anchor_map_errors(figure, "notes", note_ids))
        title = figure.get("sourceBindings", {}).get("title")
        if not isinstance(title, str) or not title: errors.append(f"{figure_id} sourceBindings.title is required")
        manual = figure.get("sourceBindings", {}).get("manualReview")
        if not isinstance(manual, list) or not manual or any(not isinstance(v, str) or not v for v in manual): errors.append(f"{figure_id} sourceBindings.manualReview must disclose bounded-parser limits")
    return errors


def authority_errors(data: dict[str, Any], root: Path | None = None) -> list[str]:
    errors: list[str] = []; base = repository_root(root)
    for figure in data.get("figures", []):
        figure_id = figure.get("id", "<unknown>")
        try: source = safe_path(figure.get("sourcePuml"), suffix=".puml", root=base)
        except ValueError as exc: errors.append(f"{figure_id}: unsafe PlantUML path: {exc}"); continue
        if not source.is_file(): errors.append(f"{figure_id}: missing PlantUML authority {figure.get('sourcePuml')}"); continue
        actual_hash = sha256(source)
        if actual_hash != figure.get("sourceSha256"): errors.append(f"{figure_id}: PlantUML hash drift {actual_hash}; expected {figure.get('sourceSha256')}")
        text = canonical_text(source.read_bytes()).decode("utf-8"); bindings = figure.get("sourceBindings", {}); title = bindings.get("title")
        titles, note_units = _source_units(text)
        if isinstance(title, str) and title not in titles: errors.append(f"{figure_id}: bound source title is not an extracted complete title unit")
        note_mapping = bindings.get("notes", {})
        note_anchors = []
        if isinstance(note_mapping, dict):
            for binding in note_mapping.values():
                anchors = _binding_anchors(binding)
                note_anchors.extend([anchors] if isinstance(anchors, str) else anchors if isinstance(anchors, list) else [])
        for unit in note_units:
            if not any(isinstance(anchor, str) and anchor.strip() not in {"end note", "}"} and anchor in unit for anchor in note_anchors):
                errors.append(f"{figure_id}: unaccounted complete source note unit: {unit.splitlines()[0]}")
        relation_inventory = {str(row["id"]): row for row in figure.get("relations", [])}
        aliases = {str(row.get("authorityAlias", row["id"])): str(row["id"]) for row in figure.get("groups", []) + figure.get("entities", [])}
        relation_mapping = bindings.get("relations", {})
        relation_anchor_owners: dict[str, list[str]] = {}
        if isinstance(relation_mapping, dict):
            for item_id, binding in relation_mapping.items():
                anchors = _binding_anchors(binding)
                values = [anchors] if isinstance(anchors, str) else anchors if isinstance(anchors, list) else []
                for anchor in values:
                    if isinstance(anchor, str):
                        relation_anchor_owners.setdefault(anchor.strip(), []).append(str(item_id))
        for line in (item.strip() for item in text.splitlines()):
            if line.startswith("'") or not any(token in line for token in ("-->", "..>")):
                continue
            endpoints = _relation_endpoints(line)
            if not endpoints or not all(value in aliases or value in aliases.values() for value in endpoints):
                continue
            owners = relation_anchor_owners.get(line, [])
            if not owners:
                errors.append(f"{figure_id}: unaccounted finite source relation unit: {line}")
            elif len(owners) > 1:
                errors.append(f"{figure_id}: finite source relation unit is bound more than once by {', '.join(owners)}: {line}")
        for key in ("objects", "relations", "notes"):
            mapping = bindings.get(key, {})
            if not isinstance(mapping, dict): continue
            for item_id, binding in mapping.items():
                anchors = _binding_anchors(binding)
                values = [anchors] if isinstance(anchors, str) else anchors
                if isinstance(values, list):
                    for anchor in values:
                        if not isinstance(anchor, str):
                            continue
                        if anchor.strip() in {"end note", "}"}:
                            errors.append(f"{figure_id}: source {key} anchor for {item_id} is a separator, not semantic evidence")
                        elif anchor not in text:
                            errors.append(f"{figure_id}: source {key} anchor missing for {item_id}: {anchor}")
                        elif key == "relations":
                            endpoints = _relation_endpoints(anchor)
                            if endpoints and all(value in aliases or value in aliases.values() for value in endpoints):
                                resolved = tuple(aliases.get(value, value) for value in endpoints)
                                row = relation_inventory.get(str(item_id), {})
                                if resolved != (row.get("source"), row.get("target")):
                                    errors.append(f"{figure_id}: finite source relation endpoints disagree for {item_id}: {resolved}")
    return errors


def _style_map(style: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in style.split(";"):
        if "=" in item:
            key, value = item.split("=", 1); result[key] = value
    return result


def validate_figure(figure: dict[str, Any], root: Path | None = None) -> list[str]:
    errors: list[str] = []; base = repository_root(root); figure_id = figure["id"]
    try:
        source = safe_path(figure["sourcePuml"], suffix=".puml", root=base); output = safe_path(figure["drawioSource"], suffix=".drawio", root=base)
    except ValueError as exc: return [f"{figure_id}: unsafe model path: {exc}"]
    if not source.is_file(): return [f"{figure_id}: missing PlantUML authority {figure['sourcePuml']}"]
    if sha256(source) != figure["sourceSha256"]: errors.append(f"{figure_id}: PlantUML hash drift")
    if not output.is_file(): return errors + [f"{figure_id}: missing Draw.io source {figure['drawioSource']}"]
    if sha256(output) != figure["drawioSha256"]: errors.append(f"{figure_id}: Draw.io hash drift")
    try: xml_root = ET.parse(output).getroot()
    except (OSError, ET.ParseError) as exc: return errors + [f"{figure_id}: unreadable Draw.io XML: {exc}"]
    if xml_root.tag != "mxfile" or xml_root.get("compressed") != "false": errors.append(f"{figure_id}: Draw.io source must be uncompressed mxfile XML")
    all_cells = [cell for cell in xml_root.iter("mxCell") if cell.get("id")]; counts = Counter(cell.get("id") for cell in all_cells); duplicates = sorted(cell_id for cell_id, count in counts.items() if count > 1)
    if duplicates: errors.append(f"{figure_id}: duplicate mxCell ids: {', '.join(duplicates)}")
    cells = {cell.get("id"): cell for cell in all_cells}
    if "0" not in cells or "1" not in cells: errors.append(f"{figure_id}: Draw.io root cells 0 and 1 are required")
    expected: set[str] = set(); groups = {row["id"] for row in figure.get("groups", [])}
    def hidden(cell: ET.Element) -> bool:
        seen: set[str] = set()
        current: ET.Element | None = cell
        while current is not None:
            cell_id = current.get("id") or ""
            if cell_id in seen:
                break
            seen.add(cell_id)
            if current.get("visible") == "0" or current.get("collapsed") == "1":
                return True
            current = cells.get(current.get("parent"))
        return False
    for kind, prefix in (("groups", "group"), ("entities", "node"), ("notes", "note")):
        for row in figure.get(kind, []):
            cell_id = f"{prefix}-{row['id']}"; expected.add(cell_id); cell = cells.get(cell_id)
            if cell is None: errors.append(f"{figure_id}: missing semantic cell {cell_id}"); continue
            expected_parent = f"group-{row['parent']}" if kind == "entities" and row.get("parent") else "1"; expected_role = "interpretation-boundary" if kind == "notes" else row["role"]
            expected_kind = "group" if kind == "groups" else "entity" if kind == "entities" else "note"
            if cell.get("semanticKind") != expected_kind: errors.append(f"{figure_id}: semantic kind drift in {cell_id}")
            if hidden(cell): errors.append(f"{figure_id}: semantic cell hidden or inside collapsed ancestor: {cell_id}")
            if cell.get("vertex") != "1" or cell.get("edge") == "1": errors.append(f"{figure_id}: {cell_id} is not a rendered vertex")
            if cell.get("parent") != expected_parent: errors.append(f"{figure_id}: parent/boundary drift in {cell_id}")
            if normalized_label(cell.get("value")) != row["label"]: errors.append(f"{figure_id}: label drift in {cell_id}")
            if cell.get("semanticRole") != expected_role: errors.append(f"{figure_id}: semantic role drift in {cell_id}")
            style = cell.get("style") or ""
            if "fontFamily=Helvetica" not in style or "shadow=0" not in style: errors.append(f"{figure_id}: style contract missing in {cell_id}")
            if "image=" in style or "gradientColor=none" not in style: errors.append(f"{figure_id}: prohibited image/gradient styling in {cell_id}")
    for row in figure.get("relations", []):
        cell_id = f"edge-{row['id']}"; expected.add(cell_id); cell = cells.get(cell_id)
        if cell is None: errors.append(f"{figure_id}: missing semantic relation {cell_id}"); continue
        source_prefix = "group" if row["source"] in groups else "node"; target_prefix = "group" if row["target"] in groups else "node"
        if cell.get("semanticKind") != "relation" or cell.get("edge") != "1" or cell.get("vertex") == "1": errors.append(f"{figure_id}: {cell_id} is not a rendered semantic edge")
        if hidden(cell): errors.append(f"{figure_id}: semantic relation hidden or inside collapsed ancestor: {cell_id}")
        if cell.get("parent") != "1": errors.append(f"{figure_id}: relation parent drift in {cell_id}")
        if cell.get("source") != f"{source_prefix}-{row['source']}" or cell.get("target") != f"{target_prefix}-{row['target']}": errors.append(f"{figure_id}: endpoint drift in {cell_id}")
        if normalized_label(cell.get("value")) != row["label"]: errors.append(f"{figure_id}: relation label drift in {cell_id}")
        if cell.get("semanticRole") != row["role"]: errors.append(f"{figure_id}: relation role drift in {cell_id}")
        if cell.get("guardRef") != row.get("guardRef"): errors.append(f"{figure_id}: guard reference drift in {cell_id}")
        if row.get("guardRef") and not row.get("label", "").strip(): errors.append(f"{figure_id}: guarded relation lacks a visible guard id in {cell_id}")
        style = _style_map(cell.get("style") or ""); expected_style = _style_map(EDGE_STYLES[row["role"]])
        if any(style.get(key) != value for key, value in expected_style.items()): errors.append(f"{figure_id}: arrow/style polarity drift in {cell_id}")
        if style.get("startArrow", "none") != "none": errors.append(f"{figure_id}: reversed start arrow in {cell_id}")
        geom = cell.find("mxGeometry")
        if geom is None or geom.get("relative") != "1": errors.append(f"{figure_id}: edge geometry missing in {cell_id}")
    graph_cells = {cell.get("id") for cell in all_cells if cell.get("vertex") == "1" or cell.get("edge") == "1" or cell.get("semanticKind")}
    unexpected = sorted(str(cell_id) for cell_id in graph_cells - expected - {"0", "1"})
    if unexpected: errors.append(f"{figure_id}: undeclared rendered/semantic cells: {', '.join(unexpected)}")
    return errors


def validate_package(root: Path | None = None) -> list[str]:
    try: data = load_manifest(root)
    except (OSError, json.JSONDecodeError) as exc: return [f"cannot load {MANIFEST_RELATIVE.as_posix()}: {exc}"]
    errors = validate_manifest(data, root)
    if errors: return errors
    errors.extend(authority_errors(data, root))
    for figure in data["figures"]: errors.extend(validate_figure(figure, root))
    errors.extend(export_errors(data, root))
    return errors


def export_errors(
    data: dict[str, Any],
    root: Path | None = None,
    *,
    exports_override: dict[str, Any] | None = None,
    index_bytes_override: bytes | None = None,
    validate_index: bool = True,
    check_index_freshness: bool = True,
) -> list[str]:
    """Bind review outputs to one candidate, caption, facet, and measured PDF QA."""
    base = repository_root(root)
    if exports_override is None:
        path = base / EXPORT_MANIFEST_RELATIVE
        if not path.is_file():
            return [f"missing model export manifest {EXPORT_MANIFEST_RELATIVE.as_posix()}"]
        try:
            exports = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return [f"cannot load model export manifest: {exc}"]
    else:
        exports = exports_override
    errors: list[str] = []
    rows = exports.get("figures") if isinstance(exports, dict) else None
    if not isinstance(exports, dict) or exports.get("schemaVersion") != "2.0" or not isinstance(rows, list):
        return ["model export manifest requires schemaVersion 2.0 and figures list"]
    figures = {row["id"]: row for row in data.get("figures", [])}
    row_ids = [row.get("figureId") for row in rows]
    if len(set(row_ids)) != len(row_ids):
        errors.append("model export figure ids must be unique")
    if set(row_ids) != set(figures):
        errors.append("model export figure set differs from model manifest")
    output_ids: set[str] = set(); output_paths: set[str] = set()
    for row in rows:
        figure_id = row.get("figureId")
        figure = figures.get(figure_id)
        if not figure:
            continue
        if row.get("drawioSha256") != figure.get("drawioSha256"):
            errors.append(f"{figure_id}: export Draw.io identity is stale")
        revision = figure.get("revision", {})
        if row.get("modelVersionId") != revision.get("modelVersionId") or row.get("modelContentSha256") != revision.get("modelContentSha256"):
            errors.append(f"{figure_id}: export candidate identity is stale")
        caption = row.get("caption")
        if not isinstance(caption, str) or hashlib.sha256(caption.encode("utf-8")).hexdigest() != row.get("captionSha256"):
            errors.append(f"{figure_id}: export caption identity is invalid")
        if isinstance(caption, str) and row.get("reviewBundleSha256") != review_bundle_sha256(figure, caption):
            errors.append(f"{figure_id}: review bundle identity is stale")
        export_status = row.get("exportStatus")
        if export_status not in {"EXPORTED-AND-HASHED", "NEEDS-RENDER"}:
            errors.append(f"{figure_id}: unsupported or missing exportStatus")
        outputs = row.get("outputs")
        if not isinstance(outputs, list):
            errors.append(f"{figure_id}: outputs must be a list")
            continue
        if export_status == "NEEDS-RENDER":
            if outputs:
                errors.append(f"{figure_id}: NEEDS-RENDER cannot claim current outputs")
            if not isinstance(row.get("exportDispositionReason"), str) or not row.get("exportDispositionReason", "").strip():
                errors.append(f"{figure_id}: NEEDS-RENDER requires exportDispositionReason")
        elif export_status == "EXPORTED-AND-HASHED":
            if not outputs:
                errors.append(f"{figure_id}: EXPORTED-AND-HASHED requires declared outputs")
            facets: dict[str, set[str]] = {}
            for item in outputs:
                facet = item.get("facet")
                if isinstance(facet, str) and facet:
                    facets.setdefault(facet, set()).add(str(item.get("format")))
            for facet, formats in facets.items():
                if formats != {"pdf", "svg"}:
                    errors.append(f"{figure_id}: exported facet {facet!r} requires PDF and SVG")
        for item in outputs:
            output_id, output_path = item.get("outputId"), item.get("path")
            if not isinstance(output_id, str) or not output_id or output_id in output_ids:
                errors.append(f"{figure_id}: duplicate or missing outputId")
            else: output_ids.add(output_id)
            if not isinstance(output_path, str) or output_path in output_paths:
                errors.append(f"{figure_id}: duplicate or missing output path")
            else: output_paths.add(output_path)
            if item.get("figureId") != figure_id or item.get("modelVersionId") != revision.get("modelVersionId"):
                errors.append(f"{figure_id}: output is assigned to the wrong candidate")
            if item.get("sourceDrawioSha256") != figure.get("drawioSha256") or item.get("reviewBundleSha256") != row.get("reviewBundleSha256"):
                errors.append(f"{figure_id}: output provenance identity is stale")
            if not isinstance(item.get("facet"), str) or not item.get("facet"):
                errors.append(f"{figure_id}: output facet is required")
            suffix = "." + str(item.get("format", ""))
            try:
                output = safe_path(output_path, suffix=suffix, root=base)
            except ValueError as exc:
                errors.append(f"{figure_id}: unsafe export path: {exc}")
                continue
            if figure_id not in output.name:
                errors.append(f"{figure_id}: export filename must retain the figure id")
            if not output.is_file():
                errors.append(f"{figure_id}: missing declared export {output_path}")
            elif raw_sha256(output) != item.get("rawSha256"):
                errors.append(f"{figure_id}: raw export identity drift in {output_path}")
        qa = row.get("qa")
        if export_status == "EXPORTED-AND-HASHED" and not isinstance(qa, dict):
            errors.append(f"{figure_id}: measured PDF QA record is required")
        elif export_status == "EXPORTED-AND-HASHED":
            measured, page_width, intended, placed = (qa.get("measuredMinimumPdfTextPt"), qa.get("pageWidthPt"), qa.get("intendedWidthMm"), qa.get("placedMinimumTextPt"))
            if not all(isinstance(value, (int, float)) and value > 0 for value in (measured, page_width, intended, placed)):
                errors.append(f"{figure_id}: PDF text QA must use positive measured point values")
            else:
                expected = measured * (intended * 72 / 25.4) / page_width
                if abs(expected - placed) > 0.002:
                    errors.append(f"{figure_id}: placed PDF text point calculation is invalid")
            if qa.get("measurementMethod") != "PDF-TEXT-SPAN-POINT-SIZE":
                errors.append(f"{figure_id}: QA must use rendered PDF text spans, not Draw.io fontSize")
        if row.get("semanticStatus") != revision.get("semanticReview", {}).get("status"):
            errors.append(f"{figure_id}: export semantic status differs from revision review")
        allowed_final = {"TARGET-WIDTH-BELOW-8PT", "NEEDS-LAYOUT-AND-BELOW-8PT", "FINAL-SIZE-PENDING"}
        if row.get("promotionStatus") != "DRAFT-NOT-PROMOTED" or row.get("finalSizeStatus") not in allowed_final:
            errors.append(f"{figure_id}: export status must remain draft with an honest final-size disposition")
    index = exports.get("readerIndex")
    if not validate_index:
        return errors
    if not isinstance(index, dict) or index.get("path") != REVIEW_INDEX_RELATIVE.as_posix():
        errors.append("controlled reader index path is required")
    else:
        try: index_path = safe_path(index.get("path"), suffix=".md", root=base)
        except ValueError as exc: errors.append(f"unsafe reader index path: {exc}")
        else:
            actual_index: bytes | None
            if index_bytes_override is not None:
                actual_index = index_bytes_override
            elif index_path.is_file():
                actual_index = index_path.read_bytes()
            else:
                actual_index = None
            if actual_index is None:
                errors.append("controlled reader index is missing")
            else:
                canonical_index = canonical_text(actual_index)
                if hashlib.sha256(canonical_index).hexdigest() != index.get("textSha256"):
                    errors.append("controlled reader index identity is stale")
                if check_index_freshness:
                    expected_index = canonical_text(render_review_index(data, exports).encode("utf-8"))
                    if canonical_index != expected_index:
                        errors.append("controlled reader index content is stale for current candidates and exports")
    return errors


def render_review_index(data: dict[str, Any], exports: dict[str, Any]) -> str:
    """Create the deterministic reader-facing map without implying scientific approval."""
    models = {row["id"]: row for row in data["figures"]}
    lines = [
        "# CL-TAV model-figure review index", "",
        "> Controlled draft candidates only. Mechanical checks do not establish semantic correctness, publication readiness, or promotion.", "",
        "## Check boundary", "",
        "| Check | Automated | Human decision required |", "| --- | --- | --- |",
        "| File identity, registered topology, visible labels, output assignment and hashes | Yes | No |",
        "| Recorded PDF measurement method, positive point values, and placement formula | Yes | PDF span extraction is performed separately with the named tool |",
        "| Scientific meaning, omissions, downstream contract impact and publication suitability | No | Yes |", "",
        "## Candidate and output map", "",
        "| Figure | Version | Disposition | Editable source | Caption | Review outputs | Semantic review | Final-size status | Promotion |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in exports["figures"]:
        figure = models[row["figureId"]]; rev = figure["revision"]
        source = f"[{Path(figure['drawioSource']).name}](../../../../{figure['drawioSource']})"
        outputs = ", ".join(f"[{item['format'].upper()}](../../../../{item['path']})" for item in row["outputs"])
        if not outputs:
            outputs = "No current export — " + str(row.get("exportDispositionReason", "render pending"))
        caption = str(row["caption"]).replace("|", "\\|")
        lines.append(f"| {row['figureId']} | `{rev['modelVersionId']}` | {rev['disposition']} | {source} | {caption} | {outputs} | {row['semanticStatus']} | {row['finalSizeStatus']} | {row['promotionStatus']} |")
    lines += ["", "## Deferred publication work", "", "Layout refinement, final manuscript placement, independent semantic approval, and promotion remain separate controlled tasks.", ""]
    return "\n".join(lines)


def write_review_index(data: dict[str, Any], root: Path | None = None) -> None:
    base = repository_root(root); registry_path = base / EXPORT_MANIFEST_RELATIVE
    exports = json.loads(registry_path.read_text(encoding="utf-8"))
    preflight = validate_manifest(data, base) + authority_errors(data, base)
    for figure in data.get("figures", []):
        preflight.extend(validate_figure(figure, base))
    preflight.extend(export_errors(data, base, exports_override=exports, validate_index=False))
    if preflight:
        raise ValueError("index publish preflight failed: " + "; ".join(preflight))
    payload = render_review_index(data, exports).encode("utf-8")
    exports["readerIndex"] = {"path": REVIEW_INDEX_RELATIVE.as_posix(), "textSha256": hashlib.sha256(payload).hexdigest()}
    registry_before = registry_path.read_bytes(); index_path = base / REVIEW_INDEX_RELATIVE
    index_before = index_path.read_bytes() if index_path.exists() else None
    candidate_errors = export_errors(data, base, exports_override=exports, index_bytes_override=payload)
    if candidate_errors:
        raise ValueError("index publish candidate is invalid: " + "; ".join(candidate_errors))
    try:
        staging_parent = base / "tmp"; staging_parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="cltav-model-index-", dir=staging_parent) as tmp:
            staged_registry = Path(tmp) / "exports.json"
            staged_index = Path(tmp) / "review-index.md"
            staged_registry.write_text(json.dumps(exports, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            staged_index.write_bytes(payload)
            index_path.parent.mkdir(parents=True, exist_ok=True)
            os.replace(staged_registry, registry_path)
            os.replace(staged_index, index_path)
    except Exception:
        registry_path.write_bytes(registry_before)
        if index_before is None: index_path.unlink(missing_ok=True)
        else: index_path.write_bytes(index_before)
        raise


def _tree_bytes(tree: ET.ElementTree) -> bytes:
    return ET.tostring(tree.getroot(), encoding="utf-8", xml_declaration=True, short_empty_elements=True)


def build(data: dict[str, Any], *, missing_only: bool, force: bool, root: Path | None = None) -> int:
    """Preflight the full batch, stage it, then install with rollback on failure."""
    base = repository_root(root); errors = validate_manifest(data, base) + authority_errors(data, base)
    if errors:
        for error in errors: print(f"  - {error}")
        return 1
    plan: list[tuple[Path, bytes]] = []
    for figure in data["figures"]:
        output = safe_path(figure["drawioSource"], suffix=".drawio", root=base)
        if output.exists() and missing_only:
            current = validate_figure(figure, base)
            if current:
                for error in current: print(f"  - {error}")
                return 1
            continue
        if output.exists() and not force: print(f"refusing to overwrite {output.relative_to(base).as_posix()}; use --force"); return 2
        payload = _tree_bytes(build_tree(figure)); expected = figure.get("drawioSha256"); actual = hashlib.sha256(canonical_text(payload)).hexdigest()
        if expected != actual: print(f"  - {figure['id']}: generated Draw.io identity {actual} does not match manifest {expected}"); return 1
        plan.append((output, payload))
    backups: dict[Path, bytes | None] = {path: path.read_bytes() if path.exists() else None for path, _ in plan}
    try:
        staging_parent = base / "tmp"
        staging_parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="cltav-model-figures-", dir=staging_parent) as tmp:
            staged: list[tuple[Path, Path]] = []
            for index, (output, payload) in enumerate(plan):
                staged_path = Path(tmp) / f"{index:02d}.drawio"; staged_path.write_bytes(payload); staged.append((output, staged_path))
            for output, staged_path in staged:
                output.parent.mkdir(parents=True, exist_ok=True); os.replace(staged_path, output); print(f"wrote {output.relative_to(base).as_posix()}")
    except Exception as exc:  # pragma: no cover
        for output, previous in backups.items():
            if previous is None: output.unlink(missing_ok=True)
            else: output.parent.mkdir(parents=True, exist_ok=True); output.write_bytes(previous)
        print(f"transaction failed and was rolled back: {exc}"); return 1
    print(f"Draw.io build complete: wrote={len(plan)}"); return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-missing", action="store_true"); parser.add_argument("--force", action="store_true"); parser.add_argument("--check", action="store_true"); parser.add_argument("--summary", action="store_true"); parser.add_argument("--write-review-index", action="store_true")
    args = parser.parse_args()
    if not any((args.build_missing, args.force, args.check, args.summary, args.write_review_index)): parser.error("select --build-missing, --force, --check, --summary, or --write-review-index")
    try: data = load_manifest()
    except (OSError, json.JSONDecodeError) as exc: print(f"cannot load {MANIFEST_RELATIVE.as_posix()}: {exc}"); return 1
    errors = validate_manifest(data)
    if errors:
        print("Model figure manifest failed:")
        for error in errors: print(f"  - {error}")
        return 1
    if args.force or args.build_missing:
        result = build(data, missing_only=args.build_missing, force=args.force)
        if result: return result
    if args.write_review_index:
        try: write_review_index(data)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"cannot write controlled review index: {exc}"); return 1
        print(f"wrote {REVIEW_INDEX_RELATIVE.as_posix()}")
    if args.check:
        errors = authority_errors(data)
        for figure in data["figures"]: errors.extend(validate_figure(figure))
        errors.extend(export_errors(data))
        if errors:
            print("Model Draw.io check failed:")
            for error in errors: print(f"  - {error}")
            return 1
        print(f"Model Draw.io check passed: figures={len(data['figures'])}")
    if args.summary:
        print(f"manifest={data['manifestId']} figures={len(data['figures'])} identity={CANONICALIZATION}")
        for figure in data["figures"]: print(f"{figure['id']} {figure['diagramType']} {figure['status']} semantic={figure['revision']['semanticReview']['status']} entities={len(figure['entities'])} relations={len(figure['relations'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
