"""Map approved figlib figures onto controlled Draw.io identities.

The committed ``.drawio`` bytes are exactly ``model_drawio.build_tree`` output.
Figlib cell ids are renamed here; nothing is hand-edited in the XML.
Discarded candidates (closed-loop v2/v3/v4a/v4b and experiment v2) are not selected.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(HERE))

from build_all import FIGS  # noqa: E402
from figlib import ERR, ERR_FILL, GREY, KEY, svg as figlib_svg  # noqa: E402

SPEC = importlib.util.spec_from_file_location(
    "cltav_model_drawio",
    ROOT / ".agents/skills/cltav-model-figures/scripts/model_drawio.py",
)
drawio = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = drawio
SPEC.loader.exec_module(drawio)

MANIFEST_PATH = ROOT / "configs/research/cltav_model_figure_manifest.json"
EXPORT_PATH = ROOT / "configs/research/cltav_model_figure_exports.json"
STARTING_HEAD = "1901742d9a9f1ddf0ef2868d40d4ca40fd9496bb"
SYSML = "SysML 1.6 notation-based views; executable/metamodel conformance is not claimed"
ID_RE_OK = __import__("re").compile(r"^[A-Za-z_][\w-]*$")

# Figlib id -> controlled manifest id. Unlisted ids stay unchanged.
RENAME = {
    "01": {"OP": "Operator", "AD": "TestAdapter", "MS": "Session", "e1": "request"},
    "02": {"L1": "MG", "L2": "PCRS", "d1": "goals-to-crs"},
    "07": {"EH": "ErrorHandle", "t8": "error-recover", "t11": "error-cap"},
    "09": {"x1": "truth-arms"},
}
RETARGET = {"04": {"PT": "PTL", "PC": "PCL", "PH": "PHL", "PS": "PSL", "PB": "PBL"}}
SKIP = {"04": {"PT", "PC", "PH", "PS", "PB"}}
GUARD = {"07": {"error-cap": "CAP", "error-recover": "UNCONFIRMED"}}
VERSION = {
    "01": "v2", "02": "v2", "03": "v2", "04": "v2", "05": "v4",
    "06": "v2", "07": "v2", "08": "v2", "09": "v3",
}
ROLE_BY_STYLE = {
    "main": {"end": "flow", "open": "dependency", "none": "association"},
    "dep": {"end": "observation", "open": "dependency", "none": "dependency"},
    "forbid": {"end": "forbidden", "open": "forbidden", "none": "forbidden"},
    "err": {"end": "risk", "open": "risk", "none": "risk"},
    "loop": {"end": "continue", "open": "continue", "none": "continue"},
    "stop": {"end": "stop", "open": "stop", "none": "stop"},
    "bind": {"end": "constraint-link", "open": "constraint-link", "none": "constraint-link"},
}
ROLE_OVERRIDE = {
    "01": {"Operator": "external", "CLK": "external", "IB": "risk", "IUT": "core"},
    "02": {"TR": "planned", "VC": "planned", "TM": "planned", "EV": "planned"},
    "03": {"EV": "evidence"},
    "08": {
        "IA": "constraint", "EP": "constraint", "JM": "constraint", "UP": "constraint",
        "CM": "constraint", "BU": "constraint", "SC": "constraint",
    },
}
ARROW = {"dependency": "..>", "forbidden": "..>", "planned": "..>", "evidence-only": "..>"}
EXTRA_NOTES = {
    "05": [{
        "id": "s7-wording",
        "x": 16, "y": 640, "w": 768, "h": 72,
        "label": (
            "S7 is drawn as keep or invalidate q. CONFIRMED-NOT-SENT keeps q; "
            "UNKNOWN-EFFECT invalidates q. Only RECOVER is admissible after unknown-effect. "
            "confirmed not sent remains the method and Algorithm 1 wording. "
            "Two columns: left S0-S3 and S10 aligned with Terminal; right S4-S9."
        ),
    }],
    "09": [{
        "id": "truth-boundary",
        "x": 16, "y": 748, "w": 768, "h": 108,
        "label": (
            "Registered interfaces remain constraints on this view. "
            "Algorithm calls: IF-PRED-OBS, IF-SELECT-ADMIT, IF-EXECUTE-RECORD, "
            "IF-OBS-INTERPRET, IF-PREP-RECOVER, IF-HIST-UPDATE, IF-EQUIV, IF-RESOURCE-STOP. "
            "Experiment I/O: IF-EXP-SCENE, IF-EXP-INJECT, IF-EXP-TRUTH, IF-EXP-COLLECT, "
            "IF-EXP-RUN, IF-EXP-FILTER, IF-EXP-EVAL. "
            "Campaigns: EXP-CLTAV-DETECT, EXP-CLTAV-LOCATE, EXP-CLTAV-ABLATION. "
            "Arms: CL-T / CL-A / CL-TA / CL-LOOP. "
            "Truth is evaluator-only and is never an algorithm input. "
            "The truth-to-run edge is forbidden leakage. "
            "This note records the interface boundary; it is not a measured result."
        ),
    }],
}
CANVAS_EXTRA = {"05": 90, "09": 140}
GRAPHS_PATH = ROOT / "configs/research/cltav_figure_graphs.json"
READER_SVG_DIRS = (
    ROOT / "artifacts/publications/cltav/model-drafts",
    ROOT / "artifacts/publications/cltav/figures",
)
SVG_NAME = {
    "01": "FIG-CL-TAV-01-context.svg",
    "02": "FIG-CL-TAV-02-requirement-layers.svg",
    "03": "FIG-CL-TAV-03-bdd.svg",
    "04": "FIG-CL-TAV-04-ibd.svg",
    "05": "FIG-CL-TAV-05-closed-loop-activity.svg",
    "06": "FIG-CL-TAV-06-diagnostic-sequence.svg",
    "07": "FIG-CL-TAV-07-two-state-machines.svg",
    "08": "FIG-CL-TAV-08-parametric.svg",
    "09": "FIG-CL-TAV-09-experiment-architecture.svg",
}
GRAPH_POLARITY = {
    "05": {
        "eloop": "continue",
        "e910": "advance",
        "s-TPG": "stop",
        "e7loop": "retry",
        "e7stop": "stop",
    },
}
STYLE_POLARITY = {"loop": "continue", "stop": "stop"}
BRIDGES = {
    "05": [
        "XOR exclusive action kinds remain TEST, PREP and RECOVER on S3.",
        "Hk is the survivor set after S9: H <- H intersect I_z.",
        "Prep is named PREP on S3; ERROR and unconfirmed effects enter S7.",
        "ErrorHandle is the FIG-07 witness of S7 containment; it is not a second box on this v4 layout.",
        "Charge cost once is drawn as Charge declared cost once.",
        "strictly-reducing overlapping classes remain the FIG-06 and Algorithm 1 admission contract.",
        "empty S is not selectable; S=empty is Spec. error.",
        "Admit guards A1 and A5 remain in Algorithm 1 and FIG-07; A2/5 here shares Stop-Budget.",
        "resource bounds cmin and Kmax are FIG-08 constraints; they terminate via Stop-Budget.",
    ],
    "06": [
        "Message 10 is Izk of tb, drawn as I_k of t_b.",
        "PREP names the Prep action.",
    ],
    "07": [
        "bound M2 is the approved model identity drawn as Bound M2.",
        "Ports belong to FIG-CL-TAV-04.",
        "retry remaining is drawn as retry left.",
    ],
    "08": [
        "Displayed constraints include cmin, Kmax and Hk.",
    ],
}
REASONS = {
    "01": "Operator reaches the session, not the adapter; action and observation are bidirectional through the adapter; the clock is t_k with error bound epsilon.",
    "02": "Regroup method goals, protocol CRS, deferred tool requirements and the representative trace as drawn.",
    "03": "Regroup the logical classifiers and trace edges as drawn.",
    "04": "Show Msess ports and the adapter as the only Mprot connection, as drawn.",
    "05": "Adopt the approved two-column v4 loop. S7 is drawn as keep or invalidate q; CONFIRMED-NOT-SENT keeps q and UNKNOWN-EFFECT invalidates q in the method text and Algorithm 1.",
    "06": "Redraw the diagnostic sequence, including overlapping admission and the second observation to analysis.",
    "07": "Show guards A1-A5 and priorities P1-P5, shared Stop-Budget for A2/A5 and P5, and ErrorHandle stop routing. No cross-machine transition.",
    "08": "Redraw the displayed timing, cost and history constraints. They are not claimed solved.",
    "09": (
        "Adopt experiment architecture v3 from the DM 2026-11 redraw source: "
        "truth recorded before any arm runs (IF-EXP-TRUTH on E1), IF-EXP-RUN on E2, "
        "E6 is the CL-RQ1-CL-RQ3 reporting step, and exclusions include unconfirmed injection and abstain."
    ),
}


def readable(text: str) -> str:
    """Keep subscripts as ASCII so labels stay editable plain text."""
    if not text:
        return ""
    parts: list[str] = []
    for part in __import__("re").split(r"(\$[^$]*\$)", text):
        if not part:
            continue
        if part.startswith("$") and part.endswith("$") and len(part) > 1:
            parts.append(part[1:-1].lstrip("!"))
        else:
            parts.append(part)
    return "".join(parts).replace("\r\n", "\n").replace("\r", "\n")


def num(value: float) -> int | float:
    value = round(float(value), 2)
    if abs(value - round(value)) < 1e-9:
        return int(round(value))
    return value


def node_label(node) -> str:
    parts = [readable(node.stereo), readable(node.title), readable(node.detail)]
    text = "\n".join(part.strip() for part in parts if part and part.strip())
    return text or node.id


def default_role(node, manifest_id: str, key: str) -> str:
    override = ROLE_OVERRIDE.get(key, {}).get(manifest_id)
    if override:
        return override
    if node.shape == "diamond":
        return "decision"
    if node.shape in {"dot", "lifeline"}:
        return "state" if node.shape == "dot" else "boundary"
    if node.shape == "port":
        return "port"
    if node.dash or node.fill == GREY and node.shape in {"round", "pill", "rect"}:
        if node.fill == ERR_FILL or node.stroke == ERR:
            return "risk"
        if "stop" in readable(node.title).lower() or node.shape == "pill":
            return "stop"
        return "planned"
    if node.fill == ERR_FILL or node.stroke == ERR:
        return "risk"
    if node.fill == KEY:
        return "core"
    title = readable(node.title).lower()
    if title.startswith("stop"):
        return "stop"
    if node.shape == "pill":
        return "external"
    if node.shape == "text":
        return "constraint"
    return "core"


def group_role(node) -> str:
    if node.fill == GREY:
        return "boundary"
    if node.fill == KEY:
        return "core"
    return "boundary"


def smallest_frame(node, frames) -> str | None:
    cx, cy = node.x + node.w / 2, node.y + node.h / 2
    hits = [
        frame for frame in frames
        if frame.id != node.id and frame.x <= cx <= frame.x + frame.w and frame.y <= cy <= frame.y + frame.h
    ]
    if not hits:
        return None
    hits.sort(key=lambda frame: frame.w * frame.h)
    return hits[0].id


def edge_role(edge) -> str:
    return ROLE_BY_STYLE[edge.style][edge.arrow]


def fraction(point: float, origin: float, size: float) -> int | float:
    if size <= 0:
        return 0.5
    value = (point - origin) / size
    value = min(1.0, max(0.0, value))
    return num(round(value, 4))


def one_line(text: str) -> str:
    return " / ".join(part.strip() for part in text.splitlines() if part.strip())


def build_figure(key: str, previous: dict) -> tuple[dict, list[dict]]:
    figure = FIGS[key]()
    rename = RENAME.get(key, {})
    retarget = RETARGET.get(key, {})
    skip = set(SKIP.get(key, set()))
    frames = [node for node in figure.nodes if node.shape == "frame" and node.id not in skip]
    mapping: list[dict] = []

    def mid(figlib_id: str) -> str:
        return rename.get(figlib_id, figlib_id)

    groups, entities, notes = [], [], []
    for node in figure.nodes:
        if node.id in skip:
            mapping.append({"figlib": node.id, "manifest": None, "kind": "skipped", "reason": "absorbed or non-semantic port square"})
            continue
        manifest_id = mid(node.id)
        if not ID_RE_OK.match(manifest_id):
            raise SystemExit(f"FIG-{key} id {manifest_id} is not a controlled identifier")
        label = node_label(node)
        if node.shape == "frame":
            groups.append({
                "id": manifest_id, "label": label, "role": group_role(node),
                "x": num(node.x), "y": num(node.y), "w": num(node.w), "h": num(node.h),
            })
            mapping.append({"figlib": node.id, "manifest": f"group-{manifest_id}", "kind": "group", "label": label})
            continue
        is_note = node.shape == "note" or (node.shape == "text" and not readable(node.title).strip() and readable(node.detail).strip())
        if is_note:
            notes.append({"id": manifest_id, "label": label, "x": num(node.x), "y": num(node.y), "w": num(node.w), "h": num(node.h)})
            mapping.append({"figlib": node.id, "manifest": f"note-{manifest_id}", "kind": "note", "label": label})
            continue
        parent_figlib = smallest_frame(node, frames)
        parent = mid(parent_figlib) if parent_figlib else None
        x, y = node.x, node.y
        if parent_figlib:
            host = next(frame for frame in frames if frame.id == parent_figlib)
            x, y = node.x - host.x, node.y - host.y
        row = {
            "id": manifest_id, "label": label, "role": default_role(node, manifest_id, key),
            "x": num(x), "y": num(y), "w": num(node.w), "h": num(node.h),
        }
        if parent:
            row["parent"] = parent
        entities.append(row)
        mapping.append({
            "figlib": node.id, "manifest": f"node-{manifest_id}", "kind": "entity",
            "parent": f"group-{parent}" if parent else "1", "label": label,
        })

    if figure.legend:
        legend = "Legend: " + "; ".join(readable(text) for _, text in figure.legend)
        ly = figure.legend_y if figure.legend_y is not None else figure.h - 16
        notes.append({
            "id": "legend", "label": legend,
            "x": num(figure.legend_x), "y": num(ly), "w": num(max(120, figure.w - figure.legend_x - 16)), "h": 28,
        })
        mapping.append({"figlib": "legend", "manifest": "note-legend", "kind": "note", "label": legend})

    for extra in EXTRA_NOTES.get(key, []):
        notes.append({k: extra[k] for k in ("id", "label", "x", "y", "w", "h")})
        mapping.append({"figlib": None, "manifest": f"note-{extra['id']}", "kind": "note", "label": extra["label"]})

    relations = []
    seen_lines: set[str] = set()
    for edge in figure.edges:
        src = retarget.get(edge.src, edge.src)
        dst = retarget.get(edge.dst, edge.dst)
        if src in skip or dst in skip:
            raise SystemExit(f"FIG-{key} edge {edge.id} still points at a skipped cell")
        manifest_id = mid(edge.id)
        role = edge_role(edge)
        label = readable(edge.label)
        source, target = mid(src), mid(dst)
        src_node = figure.get(src)
        dst_node = figure.get(dst)
        row = {"id": manifest_id, "source": source, "target": target, "label": label, "role": role}
        if edge.pts:
            row["exitX"] = fraction(edge.pts[0][0], src_node.x, src_node.w)
            row["exitY"] = fraction(edge.pts[0][1], src_node.y, src_node.h)
            row["entryX"] = fraction(edge.pts[-1][0], dst_node.x, dst_node.w)
            row["entryY"] = fraction(edge.pts[-1][1], dst_node.y, dst_node.h)
            points = [[num(x), num(y)] for x, y in edge.pts[1:-1]]
            if points:
                row["points"] = points
        guard = GUARD.get(key, {}).get(manifest_id)
        if guard:
            if not label.strip():
                raise SystemExit(f"FIG-{key} guard {guard} has an empty label")
            row["guardRef"] = guard
        arrow = ARROW.get(role, "-->")
        line = f"{source} {arrow} {target} : {manifest_id} {one_line(label)}".rstrip()
        if line in seen_lines:
            raise SystemExit(f"duplicate PlantUML relation line: {line}")
        seen_lines.add(line)
        row["_line"] = line
        relations.append(row)
        mapping.append({
            "figlib": edge.id, "manifest": f"edge-{manifest_id}", "kind": "relation",
            "source": source, "target": target, "role": role, "label": label,
            "droppedLabelCell": f"{edge.id}-lbl" if edge.label else None,
        })

    puml = render_puml(key, previous["id"], groups, entities, notes, relations)
    puml_path = ROOT / previous["sourcePuml"]
    puml_path.write_bytes(puml.encode("utf-8"))
    source_hash = drawio.sha256(puml_path)

    record = {
        "id": previous["id"],
        "topic": previous["topic"],
        "diagramType": previous["diagramType"],
        "status": "DRAFT-REDRAW",
        "sourcePuml": previous["sourcePuml"],
        "sourceSha256": source_hash,
        "drawioSource": previous["drawioSource"],
        "drawioSha256": "",
        "canvas": {
            "width": num(figure.w),
            "height": num(figure.h + CANVAS_EXTRA.get(key, 0)),
            "publicationWidth": previous.get("canvas", {}).get("publicationWidth", "double-column"),
        },
        "groups": groups,
        "entities": entities,
        "relations": [{k: v for k, v in row.items() if k != "_line"} for row in relations],
        "notes": notes,
        "typography": {"nodePt": 12, "edgePt": 11, "notePt": 11},
        "sourceBindings": bind(previous["id"], groups, entities, notes, relations),
    }
    payload = drawio._tree_bytes(drawio.build_tree(record))
    record["drawioSha256"] = hashlib.sha256(drawio.canonical_text(payload)).hexdigest()
    content = drawio.model_content_sha256(record)
    version = VERSION[key]
    record["revision"] = {
        "modelVersionId": f"{previous['id']}@{version}-1901742",
        "disposition": "REVISED-DRAFT-INSTANCE",
        "revisionType": "SEMANTIC-CANDIDATE",
        "reason": REASONS[key],
        "affectedScope": ["MODEL-FIGURE", previous["id"]] + (["MANUSCRIPT"] if key in {"01", "05", "09"} else []),
        "relatedContracts": ["CR-2026-023", "CR-2026-020", "DD-044", "DD-047"],
        "contractImpact": (
            "No algorithm, interface, runtime, CRS/M2 or experiment-contract change is made. "
            "This is a semantic figure candidate. Independent review of this head remains pending. "
            "User acceptance on 2026-11-17 covers the approved figlib preview, not this commit."
        ),
        "inputIdentity": {
            "startingHead": STARTING_HEAD,
            "sourceSha256": source_hash,
            "drawioSha256": record["drawioSha256"],
        },
        "promotionStatus": "DRAFT-NOT-PROMOTED",
        "modelContentSha256": content,
        "semanticReview": {
            "status": "PENDING-INDEPENDENT-REVIEW",
            "modelContentSha256": content,
            "reviewedBy": None,
            "reviewedAt": None,
            "decision": None,
        },
    }
    return record, mapping


def render_puml(key: str, figure_id: str, groups, entities, notes, relations) -> str:
    lines = [
        f"@startuml {figure_id}",
        "skinparam shadowing false",
        f"title {figure_id} {VERSION[key]}. {SYSML}",
        f"' Approved figlib candidate {VERSION[key]} mapped to controlled ids. Not a proof of equivalence.",
    ]
    for bridge in BRIDGES.get(key, []):
        lines.append(f"' {bridge}")
    for row in groups:
        lines.append(f"rectangle {row['id']}")
        lines.append(f"' group {row['id']}: {one_line(row['label'])}")
    for row in entities:
        lines.append(f"component {row['id']}")
        lines.append(f"' entity {row['id']}: {one_line(row['label'])}")
    for row in relations:
        lines.append(row["_line"])
    for row in notes:
        lines.append(f"note as {row['id']}")
        for part in row["label"].splitlines() or [row["label"]]:
            lines.append(f"  {part}")
        lines.append("end note")
    lines.append("@enduml")
    lines.append("")
    return "\n".join(lines)


def bind(figure_id: str, groups, entities, notes, relations) -> dict:
    objects = {}
    for row in groups:
        objects[row["id"]] = {"parent": None, "anchors": [f"rectangle {row['id']}"]}
    for row in entities:
        objects[row["id"]] = {"parent": row.get("parent"), "anchors": [f"component {row['id']}"]}
    note_map = {}
    for row in notes:
        anchor = row["label"].splitlines()[0].strip()
        note_map[row["id"]] = [anchor]
    relation_map = {}
    for row in relations:
        relation_map[row["id"]] = {"source": row["source"], "target": row["target"], "anchors": [row["_line"]]}
    return {
        "title": f"title {figure_id} {VERSION[figure_id[-2:]]}. {SYSML}",
        "objects": objects,
        "relations": relation_map,
        "notes": note_map,
        "manualReview": [
            "Bindings prove finite source-location identity and topology, not full PlantUML semantic equivalence.",
            "The controlled Draw.io uses the shipped role styles and orthogonal edges. Figlib preview styling is not reproduced.",
            "Human promotion remains required for interpretation, guard completeness, and publication layout.",
        ],
    }


def mapped_id(key: str, figlib_id: str | None) -> str | None:
    if not figlib_id:
        return figlib_id
    fid = RETARGET.get(key, {}).get(figlib_id, figlib_id)
    return RENAME.get(key, {}).get(fid, fid)


def remap_svg_endpoints(text: str, key: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return f'{match.group(1)}="{mapped_id(key, match.group(2))}"'

    return re.sub(r'(data-from|data-to)="([^"]*)"', replace, text)


def graph_label(node) -> str:
    """Use a contiguous SVG-visible fragment. Math tspans are not reconstructed."""
    title = node.title or ""
    if "$" in title:
        return title.split("$", 1)[0].strip()
    title = readable(title).strip()
    if title:
        return title
    detail = node.detail or ""
    if "$" in detail:
        return detail.split("$", 1)[0].strip()
    return readable(detail).split("\n")[0].strip()


def graph_polarity(key: str, manifest_id: str, edge) -> str | None:
    override = GRAPH_POLARITY.get(key, {}).get(manifest_id)
    if override:
        return override
    return STYLE_POLARITY.get(edge.style)


def graph_entry(key: str, figure) -> dict:
    skip = set(SKIP.get(key, set()))
    nodes: dict[str, dict] = {}
    for node in figure.nodes:
        if node.id in skip or node.shape == "note":
            continue
        mid = mapped_id(key, node.id)
        if not mid:
            continue
        row: dict = {"x": num(node.x), "y": num(node.y), "w": num(node.w), "h": num(node.h)}
        label = graph_label(node)
        if label:
            row["label"] = label
        nodes[mid] = row
    edges = []
    for edge in figure.edges:
        src = mapped_id(key, edge.src)
        dst = mapped_id(key, edge.dst)
        if src in skip or dst in skip:
            raise SystemExit(f"FIG-{key} graph edge {edge.id} still points at a skipped cell")
        mid = mapped_id(key, edge.id)
        row = {"id": mid, "from": src, "to": dst}
        polarity = graph_polarity(key, mid, edge)
        if polarity:
            row["polarity"] = polarity
        guard = readable(edge.label).replace("\n", " ").strip()
        if guard:
            row["guard"] = guard
        edges.append(row)
    return {"width": num(figure.w), "height": num(figure.h), "nodes": nodes, "edges": edges}


def write_reader_svgs_and_graphs(graphs: dict[str, dict]) -> None:
    for directory in READER_SVG_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
    for key, figure in ((item, FIGS[item]()) for item in SVG_NAME):
        name = SVG_NAME[key]
        text = remap_svg_endpoints(figlib_svg(figure), key)
        if not text.endswith("\n"):
            text += "\n"
        payload = text.encode("utf-8")
        for directory in READER_SVG_DIRS:
            (directory / name).write_bytes(payload)
        graphs[name] = graph_entry(key, figure)
    GRAPHS_PATH.write_text(
        json.dumps({
            "schemaVersion": "1.0",
            "id": "CLTAV-FIGURE-GRAPHS",
            "authority": (
                "Bounded control edges for reader SVG reconciliation of the nine revised "
                "FIG-CL-TAV candidates. ALG-CLTAV-01 and the named PlantUML edge ids are the "
                "control narrative. This file is not a second algorithm."
            ),
            "figures": graphs,
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def caption_for(figure: dict) -> str:
    title = figure["sourceBindings"]["title"].removeprefix("title ")
    return (
        f"{title} Current editable candidate; input PlantUML identity is recorded, "
        "semantic review of this head is pending, and promotion is not authorized. "
        "No full 615A behaviour, real IUT, 645 capability, or experimental result is claimed."
    )


def refresh_exports(data: dict) -> None:
    exports = json.loads(EXPORT_PATH.read_text(encoding="utf-8"))
    by_id = {row["id"]: row for row in data["figures"]}
    refreshed = []
    for old in exports["figures"]:
        figure = by_id[old["figureId"]]
        caption = caption_for(figure)
        bundle = drawio.review_bundle_sha256(figure, caption)
        refreshed.append({
            "figureId": figure["id"],
            "drawioPath": figure["drawioSource"],
            "drawioSha256": figure["drawioSha256"],
            "caption": caption,
            "captionSha256": hashlib.sha256(caption.encode("utf-8")).hexdigest(),
            "exporter": {
                "name": "unavailable",
                "version": "NEEDS-RENDER",
                "parameters": "Draw.io CLI is not installed; no SVG or PDF was rendered from the revised Draw.io source",
            },
            "outputs": [],
            "checkedAt": "2026-11-17",
            "semanticStatus": "PENDING-INDEPENDENT-REVIEW",
            "exportStatus": "NEEDS-RENDER",
            "exportDispositionReason": (
                "Draw.io CLI is not installed. The previous model-draft PDF and SVG are not renders of this "
                "revised Draw.io identity and are not current review outputs."
            ),
            "finalSizeStatus": "FINAL-SIZE-PENDING",
            "promotionStatus": "DRAFT-NOT-PROMOTED",
            "modelVersionId": figure["revision"]["modelVersionId"],
            "modelContentSha256": figure["revision"]["modelContentSha256"],
            "reviewBundleSha256": bundle,
        })
    exports["figures"] = refreshed
    EXPORT_PATH.write_text(json.dumps(exports, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    previous = {row["id"]: row for row in manifest["figures"]}
    records = []
    report = []
    for key in ("01", "02", "03", "04", "05", "06", "07", "08", "09"):
        figure_id = f"FIG-CL-TAV-{key}"
        record, mapping = build_figure(key, previous[figure_id])
        records.append(record)
        report.append({"figure": figure_id, "version": VERSION[key], "cells": mapping})
        print(
            f"{figure_id} {VERSION[key]} groups={len(record['groups'])} "
            f"entities={len(record['entities'])} notes={len(record['notes'])} "
            f"relations={len(record['relations'])} drawio={record['drawioSha256'][:12]}"
        )
    manifest["figures"] = records
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_reader_svgs_and_graphs({})
    loaded = drawio.load_manifest(ROOT)
    code = drawio.build(loaded, missing_only=False, force=True, root=ROOT)
    if code:
        return code
    refresh_exports(loaded)
    loaded = drawio.load_manifest(ROOT)
    drawio.write_review_index(loaded, ROOT)
    map_path = ROOT / "configs/research/cltav_model_figure_id_map.json"
    map_path.write_text(json.dumps({
        "schemaVersion": "1.0",
        "generator": ".agents/skills/cltav-model-figures/scripts/dm_v2/promote_controlled.py",
        "selected": {
            "01-04,06-08": "figlib v2",
            "05": "FIG-CL-TAV-05-closed-loop-v4 (fig05b, two columns, 800x630)",
            "09": "FIG-CL-TAV-09-experiment-architecture-v3",
        },
        "notSelected": [
            "FIG-CL-TAV-05-closed-loop-v2",
            "FIG-CL-TAV-05-closed-loop-v3",
            "FIG-CL-TAV-05-closed-loop-v4a",
            "FIG-CL-TAV-05-closed-loop-v4b",
            "FIG-CL-TAV-09-experiment-architecture-v2",
        ],
        "figures": report,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    errors = drawio.validate_package(ROOT)
    if errors:
        print("CHECK FAILED")
        for error in errors:
            print(" -", error)
        return 1
    print("Model Draw.io check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
