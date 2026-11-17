"""Shared geometry model: one figure description -> editable .drawio (bound edges) + identical SVG preview.

Units are px; figures are designed at <= 800 px width for a 7.16 in TAES double column,
so 11 px text is about 7 pt after scaling.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from pathlib import Path

FONT = "Helvetica"
INK = "#1A1A1A"
MUTED = "#555555"
LINE = "#333333"
WHITE = "#FFFFFF"
KEY = "#EAF1FB"
ACCENT = "#1F5AA6"
ERR = "#B4541A"
ERR_FILL = "#FBF0E8"
GREY = "#F2F2F2"

T_SIZE, D_SIZE, L_SIZE = 12.5, 11, 11
EDGE_STYLES = {
    "main": (LINE, 1.2, ""),
    "loop": (ACCENT, 1.6, ""),
    "err": (ERR, 1.3, "5 3"),
    "stop": (MUTED, 1.0, "2 2"),
    "dep": (MUTED, 1.0, "5 3"),
    "forbid": (ERR, 1.6, "6 3"),
    "bind": (LINE, 1.0, ""),
}


@dataclass
class Node:
    id: str
    x: float
    y: float
    w: float
    h: float
    title: str = ""
    detail: str = ""
    fill: str = WHITE
    stroke: str = LINE
    shape: str = "rect"  # rect | round | pill | diamond | frame | text | note | port | dot | lifeline
    align: str = "center"
    stereo: str = ""
    dash: bool = False
    title_size: float = T_SIZE
    bold: bool = True


@dataclass
class Edge:
    id: str
    src: str | None
    dst: str | None
    pts: list[tuple[float, float]]
    style: str = "main"
    label: str = ""
    lpos: tuple[float, float] | None = None
    lanchor: str = "start"
    arrow: str = "end"  # end | none | open


@dataclass
class Figure:
    name: str
    w: float
    h: float
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    legend: list[tuple[str, str]] = field(default_factory=list)
    legend_y: float | None = None
    legend_x: float = 20

    def n(self, *a, **k) -> Node:
        node = Node(*a, **k)
        self.nodes.append(node)
        return node

    def e(self, *a, **k) -> Edge:
        edge = Edge(*a, **k)
        self.edges.append(edge)
        return edge

    def shift(self, dy: float) -> None:
        for n in self.nodes:
            n.y += dy
        for e in self.edges:
            e.pts = [(x, y + dy) for x, y in e.pts]
            if e.lpos:
                e.lpos = (e.lpos[0], e.lpos[1] + dy)
        if self.legend_y is not None:
            self.legend_y += dy
        self.h += dy

    def get(self, nid):
        return next(n for n in self.nodes if n.id == nid)

    # anchors: "t", "b", "l", "r" or "t@x", "b@x", "l@y", "r@y"
    def a(self, nid: str, side: str) -> tuple[float, float]:
        n = self.get(nid)
        s, _, v = side.partition("@")
        if s == "t":
            return (float(v) if v else n.x + n.w / 2, n.y)
        if s == "b":
            return (float(v) if v else n.x + n.w / 2, n.y + n.h)
        if s == "l":
            return (n.x, float(v) if v else n.y + n.h / 2)
        return (n.x + n.w, float(v) if v else n.y + n.h / 2)

    def link(self, eid, src, ss, dst, ds, via=(), **k) -> Edge:
        return self.e(eid, src, dst, [self.a(src, ss), *via, self.a(dst, ds)], **k)


# ---------------------------------------------------------------- math markup
# "$q_k$" -> italic serif; "$!H_k$" -> bold italic serif (sets); "_k" italic subscript, "_{min}" upright subscript.
MATH_FONT = "Times New Roman"
_MATH = re.compile(r"(\$[^$]*\$)")
_SUB = re.compile(r"_(\{[^}]*\}|.)")


def _segments(line: str):
    """Yield (text, kind, bold) with kind in n | m | s (italic sub) | su (upright sub)."""
    for part in _MATH.split(line):
        if not part:
            continue
        if not (part.startswith("$") and part.endswith("$") and len(part) > 1):
            yield part, "n", False
            continue
        body = part[1:-1]
        bold = body.startswith("!")
        body = body.lstrip("!")
        pos = 0
        for m in _SUB.finditer(body):
            if m.start() > pos:
                yield body[pos:m.start()], "m", bold
            sub = m.group(1).strip("{}")
            yield sub, "s" if len(sub) == 1 or not sub.isalpha() else "su", bold
            pos = m.end()
        if pos < len(body):
            yield body[pos:], "m", bold


def plain(s: str) -> str:
    return "".join(t for t, _, _ in _segments(s))


# ---------------------------------------------------------------- SVG
def _t(x, y, text, size, weight="normal", color=INK, anchor="middle", italic=False):
    out = []
    for i, line in enumerate(text.split("\n")):
        it = ' font-style="italic"' if italic else ""
        spans, shift = [], 0.0
        for seg, kind, bold in _segments(line):
            esc = html.escape(seg)
            if kind == "n":
                attrs = ""
                target = 0.0
            elif kind == "m":
                attrs = f' font-family="{MATH_FONT}" font-style="italic" font-size="{size * 1.12:.1f}"' + (' font-weight="bold"' if bold else ' font-weight="normal"')
                target = 0.0
            else:
                style = "italic" if kind == "s" else "normal"
                attrs = f' font-family="{MATH_FONT}" font-style="{style}" font-size="{size * 0.78:.1f}" font-weight="normal"'
                target = size * 0.3
            dy = target - shift
            shift = target
            spans.append(f'<tspan{attrs}{f" dy={chr(34)}{dy:.1f}{chr(34)}" if dy else ""}>{esc}</tspan>')
        out.append(f'<text x="{x:.1f}" y="{y + i * (size + 2.5):.1f}" font-family="{FONT}" font-size="{size}" '
                   f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}"{it}>{"".join(spans)}</text>')
    return "\n".join(out)


def _lines(s):
    return s.count("\n") + 1 if s else 0


def svg(fig: Figure) -> str:
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{fig.w}" height="{fig.h}" viewBox="0 0 {fig.w} {fig.h}">',
         '<rect width="100%" height="100%" fill="white"/>', "<defs>"]
    for k, (c, _, _) in EDGE_STYLES.items():
        p.append(f'<marker id="a-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                 f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
        p.append(f'<marker id="o-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
                 f'<path d="M0,0 L10,5 L0,10" fill="none" stroke="{c}" stroke-width="1.4"/></marker>')
    p.append("</defs>")
    for n in fig.nodes:
        dash = ' stroke-dasharray="5 3"' if n.dash else ""
        if n.shape == "lifeline":
            cx = n.x + n.w / 2
            p.append(f'<line x1="{cx}" y1="{n.y + 34}" x2="{cx}" y2="{n.y + n.h}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="4 3"/>')
            p.append(f'<rect x="{n.x}" y="{n.y}" width="{n.w}" height="34" rx="3" fill="{n.fill}" stroke="{n.stroke}" stroke-width="1.2"/>')
            p.append(_t(cx, n.y + 15 if n.detail else n.y + 21, n.title, T_SIZE, "bold"))
            if n.detail:
                p.append(_t(cx, n.y + 28, n.detail, D_SIZE - 1, color=MUTED))
            continue
        if n.shape == "dot":
            p.append(f'<circle cx="{n.x + n.w / 2}" cy="{n.y + n.h / 2}" r="{n.w / 2}" fill="{INK}"/>')
            continue
        if n.shape == "diamond":
            cx, cy = n.x + n.w / 2, n.y + n.h / 2
            p.append(f'<polygon points="{cx},{n.y} {n.x + n.w},{cy} {cx},{n.y + n.h} {n.x},{cy}" fill="{n.fill}" stroke="{n.stroke}" stroke-width="1.2"/>')
        elif n.shape == "note":
            f = 10
            p.append(f'<path d="M{n.x},{n.y} H{n.x + n.w - f} L{n.x + n.w},{n.y + f} V{n.y + n.h} H{n.x} Z" fill="{n.fill}" stroke="{n.stroke}" stroke-width="0.9"/>')
            p.append(f'<path d="M{n.x + n.w - f},{n.y} V{n.y + f} H{n.x + n.w}" fill="none" stroke="{n.stroke}" stroke-width="0.9"/>')
        elif n.shape != "text":
            rx = {"rect": 3, "round": 8, "pill": min(n.h / 2, 16), "frame": 0, "port": 0}.get(n.shape, 3)
            sw = 0.9 if n.shape == "frame" else 1.2
            p.append(f'<rect x="{n.x}" y="{n.y}" width="{n.w}" height="{n.h}" rx="{rx}" fill="{n.fill}" stroke="{n.stroke}" stroke-width="{sw}"{dash}/>')
        if n.shape == "frame":
            tw = len(n.title) * 6.6 + 16
            p.append(f'<path d="M{n.x},{n.y + 20} H{n.x + tw - 8} L{n.x + tw},{n.y + 12} V{n.y}" fill="none" stroke="{n.stroke}" stroke-width="0.9"/>')
            p.append(_t(n.x + 7, n.y + 14.5, n.title, D_SIZE, "bold", anchor="start"))
            if n.detail:
                p.append(_t(n.x + tw + 8, n.y + 14.5, n.detail, D_SIZE - 0.5, color=MUTED, anchor="start", italic=True))
            continue
        if n.shape == "port":
            if n.title:
                p.append(_t(n.x + n.w / 2, n.y - 4, n.title, D_SIZE - 0.5, color=MUTED))
            continue
        lines = _lines(n.stereo) + _lines(n.title) + _lines(n.detail)
        block = _lines(n.stereo) * (D_SIZE + 2.5) + _lines(n.title) * (n.title_size + 2.5) + _lines(n.detail) * (D_SIZE + 2.5)
        top = n.y + n.h / 2 - block / 2 + n.title_size * 0.8 if lines else 0
        if n.align == "left":
            x, anc = n.x + 8, "start"
            top = n.y + 6 + n.title_size * 0.8
        else:
            x, anc = n.x + n.w / 2, "middle"
        if n.stereo:
            p.append(_t(x, top, n.stereo, D_SIZE - 0.5, color=MUTED, anchor=anc))
            top += _lines(n.stereo) * (D_SIZE + 2.5)
        if n.title:
            p.append(_t(x, top, n.title, n.title_size, "bold" if n.bold else "normal", anchor=anc))
            top += _lines(n.title) * (n.title_size + 2.5)
        if n.detail:
            p.append(_t(x, top, n.detail, D_SIZE, color=MUTED if n.bold else INK, anchor=anc))
    for e in fig.edges:
        c, wdt, dash = EDGE_STYLES[e.style]
        da = f' stroke-dasharray="{dash}"' if dash else ""
        mk = {"end": f' marker-end="url(#a-{e.style})"', "open": f' marker-end="url(#o-{e.style})"', "none": ""}[e.arrow]
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in e.pts)
        p.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="{wdt}"{da}{mk}/>')
        if e.style == "forbid":
            mx, my = e.pts[len(e.pts) // 2 - 1]
            nx, ny = e.pts[len(e.pts) // 2]
            cx, cy = (mx + nx) / 2, (my + ny) / 2
            p.append(f'<path d="M{cx - 6},{cy - 6} L{cx + 6},{cy + 6} M{cx + 6},{cy - 6} L{cx - 6},{cy + 6}" stroke="{ERR}" stroke-width="2.2"/>')
        if e.label:
            p.append(_t(e.lpos[0], e.lpos[1], e.label, L_SIZE, color=c if e.style not in ("main", "bind") else INK,
                        anchor=e.lanchor, italic=True))
    if fig.legend:
        lx, ly = fig.legend_x, fig.legend_y or fig.h - 14
        for kind, text in fig.legend:
            if kind.startswith("fill:"):
                p.append(f'<rect x="{lx}" y="{ly - 7}" width="16" height="12" fill="{kind[5:]}" stroke="{LINE}" stroke-width="0.8"/>')
                p.append(_t(lx + 22, ly + 4, text, L_SIZE - 0.5, color=MUTED, anchor="start"))
            else:
                c, wdt, dash = EDGE_STYLES[kind]
                da = f' stroke-dasharray="{dash}"' if dash else ""
                p.append(f'<line x1="{lx}" y1="{ly}" x2="{lx + 26}" y2="{ly}" stroke="{c}" stroke-width="{wdt}"{da} marker-end="url(#a-{kind})"/>')
                p.append(_t(lx + 32, ly + 4, text, L_SIZE - 0.5, color=MUTED, anchor="start"))
            lx += 32 + len(text) * 5.6 + 22
    p.append("</svg>")
    return "\n".join(p)


# ---------------------------------------------------------------- draw.io
def _e(s):
    return html.escape(s, quote=True)


def _br(s):
    lines = []
    for line in s.split("\n"):
        out = []
        for seg, kind, bold in _segments(line):
            esc = html.escape(seg, quote=True)
            if kind == "n":
                out.append(esc)
            elif kind == "m":
                inner = f"<b>{esc}</b>" if bold else esc
                out.append(f'<font face="{MATH_FONT}"><i>{inner}</i></font>')
            elif kind == "s":
                out.append(f'<sub><font face="{MATH_FONT}"><i>{esc}</i></font></sub>')
            else:
                out.append(f'<sub><font face="{MATH_FONT}">{esc}</font></sub>')
        lines.append("".join(out))
    return "<br>".join(lines)


def _val(n: Node) -> str:
    parts = []
    if n.stereo:
        parts.append(f'<font style="font-size:{D_SIZE - 0.5}px" color="{MUTED}">{_br(n.stereo)}</font>')
    if n.title:
        parts.append(f"<b>{_br(n.title)}</b>" if n.bold else _br(n.title))
    if n.detail:
        parts.append(f'<font style="font-size:{D_SIZE}px" color="{MUTED if n.bold else INK}">{_br(n.detail)}</font>')
    return "<br>".join(parts)


def drawio(fig: Figure) -> str:
    c = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    base = f"html=1;whiteSpace=wrap;fontFamily={FONT};fontSize={T_SIZE};fontColor={INK};"
    for n in fig.nodes:
        dash = "dashed=1;" if n.dash else ""
        align = "align=left;verticalAlign=top;spacingLeft=6;" if n.align == "left" else ""
        sty = {
            "rect": "rounded=1;arcSize=4;",
            "round": "rounded=1;arcSize=12;",
            "pill": "rounded=1;arcSize=50;",
            "diamond": "rhombus;",
            "frame": "shape=umlFrame;width=" + str(int(len(n.title) * 6.6 + 16)) + ";height=20;verticalAlign=top;align=left;spacingLeft=6;fontSize=11;",
            "text": "text;strokeColor=none;fillColor=none;",
            "note": "shape=note;size=10;",
            "port": "",
            "dot": "ellipse;",
            "lifeline": "shape=umlLifeline;perimeter=lifelinePerimeter;size=34;",
        }[n.shape]
        val = _val(n) if n.shape not in ("frame", "port", "dot") else (f"<b>{_e(n.title)}</b>" if n.shape == "frame" else "")
        if n.shape == "frame" and n.detail:
            val += f' <i><font color="{MUTED}">{_e(n.detail)}</font></i>'
        fill = INK if n.shape == "dot" else n.fill
        c.append(f'<mxCell id="{n.id}" value="{_e(val)}" style="{sty}{base}{align}{dash}fillColor={fill};strokeColor={n.stroke};" vertex="1" parent="1">'
                 f'<mxGeometry x="{n.x}" y="{n.y}" width="{n.w}" height="{n.h}" as="geometry"/></mxCell>')
        if n.shape == "port" and n.title:
            c.append(f'<mxCell id="{n.id}-lbl" value="{_e(n.title)}" style="text;html=1;align=center;fontFamily={FONT};fontSize={D_SIZE - 0.5};fontColor={MUTED};" vertex="1" parent="1">'
                     f'<mxGeometry x="{n.x + n.w / 2 - 50}" y="{n.y - 18}" width="100" height="16" as="geometry"/></mxCell>')
    for e in fig.edges:
        col, wdt, dash = EDGE_STYLES[e.style]
        ds = f"dashed=1;dashPattern={dash};" if dash else ""
        arrow = {"end": "endArrow=block;endFill=1;", "open": "endArrow=open;endFill=0;", "none": "endArrow=none;"}[e.arrow]
        con = ""
        for key, nid, pt in (("exit", e.src, e.pts[0]), ("entry", e.dst, e.pts[-1])):
            if nid:
                n = fig.get(nid)
                rx = min(max((pt[0] - n.x) / n.w, 0), 1) if n.w else 0.5
                ry = min(max((pt[1] - n.y) / n.h, 0), 1) if n.h else 0.5
                con += f"{key}X={rx:.4f};{key}Y={ry:.4f};{key}Dx=0;{key}Dy=0;{key}Perimeter=0;"
        st = f"edgeStyle=none;html=1;rounded=0;{arrow}endSize=6;strokeColor={col};strokeWidth={wdt};{ds}{con}"
        src = f' source="{e.src}"' if e.src else ""
        dst = f' target="{e.dst}"' if e.dst else ""
        wp = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in e.pts[1:-1])
        (sx, sy), (tx, ty) = e.pts[0], e.pts[-1]
        c.append(f'<mxCell id="{e.id}" value="" style="{st}" edge="1" parent="1"{src}{dst}>'
                 f'<mxGeometry relative="1" as="geometry"><mxPoint x="{sx}" y="{sy}" as="sourcePoint"/>'
                 f'<mxPoint x="{tx}" y="{ty}" as="targetPoint"/><Array as="points">{wp}</Array></mxGeometry></mxCell>')
        if e.label:
            lw = max(len(plain(l)) for l in e.label.split("\n")) * 6.0 + 8
            lh = _lines(e.label) * (L_SIZE + 2.5) + 4
            gx = {"start": e.lpos[0] - 4, "end": e.lpos[0] - lw + 4, "middle": e.lpos[0] - lw / 2}[e.lanchor]
            al = {"start": "left", "end": "right", "middle": "center"}[e.lanchor]
            lc = col if e.style not in ("main", "bind") else INK
            c.append(f'<mxCell id="{e.id}-lbl" value="{_br(e.label)}" style="text;html=1;align={al};verticalAlign=top;spacing=0;fontFamily={FONT};fontSize={L_SIZE};fontStyle=2;fontColor={lc};" vertex="1" parent="1">'
                     f'<mxGeometry x="{gx:.1f}" y="{e.lpos[1] - L_SIZE:.1f}" width="{lw:.1f}" height="{lh:.1f}" as="geometry"/></mxCell>')
    if fig.legend:
        c.append(f'<mxCell id="legend" value="{_e("Legend: " + "; ".join(t for _, t in fig.legend))}" style="text;html=1;align=left;fontFamily={FONT};fontSize={L_SIZE - 0.5};fontColor={MUTED};" vertex="1" parent="1">'
                 f'<mxGeometry x="{fig.legend_x}" y="{(fig.legend_y or fig.h - 14) - 8}" width="{fig.w - 40}" height="16" as="geometry"/></mxCell>')
    return (f'<mxfile host="cltav-build" version="24.0.0"><diagram id="{fig.name}" name="{fig.name}">'
            f'<mxGraphModel dx="{fig.w}" dy="{fig.h}" grid="1" gridSize="2" guides="1" page="1" pageWidth="{fig.w}" pageHeight="{fig.h}" math="0" shadow="0">'
            f'<root>{"".join(c)}</root></mxGraphModel></diagram></mxfile>\n')


def write(fig: Figure, out: Path) -> None:
    (out / f"{fig.name}.svg").write_text(svg(fig), encoding="utf-8", newline="\n")
    (out / f"{fig.name}.drawio").write_text(drawio(fig), encoding="utf-8", newline="\n")
