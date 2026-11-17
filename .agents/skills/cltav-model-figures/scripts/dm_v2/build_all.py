"""FIG-CL-TAV-01..09 redraw candidates (DRAFT-REDRAW, not promoted)."""

from __future__ import annotations

import sys
from pathlib import Path

from figlib import ACCENT, ERR, ERR_FILL, GREY, KEY, MUTED, WHITE, Figure, write

OUT = Path(__file__).resolve().parent


def fig01() -> Figure:
    f = Figure("FIG-CL-TAV-01-context-v2", 780, 410)
    f.n("FS", 16, 16, 270, 250, "Msess", "verification session domain", shape="frame", fill="none", stroke=MUTED)
    f.n("FP", 572, 16, 196, 250, "Mprot", "protocol domain", shape="frame", fill="none", stroke=MUTED)
    f.n("OP", 66, 56, 170, 40, "Operator", shape="pill")
    f.n("MS", 36, 140, 210, 90, "CL-TAV session", "candidate set $!H$, resource state;\none admitted action per round", fill=KEY)
    f.n("AD", 330, 140, 180, 90, "Test adapter", "encodes stimuli;\ncaptures raw records")
    f.n("IUT", 590, 130, 160, 110, "IUT", "loader target; protocol\nmessages and operation\nstates live here")
    f.n("CLK", 330, 290, 180, 54, "Network clock", "timestamps, error bound $\u03b5$")
    f.n("IB", 584, 302, 172, 70, "645 integrity boundary", "identity bound; capability\nNOT-ESTABLISHED", fill=GREY, dash=True, shape="round", title_size=11.5)
    f.n("NT", 36, 300, 250, 44, "", "Msess sees protocol state only\nthrough the adapter.", shape="note", fill=WHITE, stroke=MUTED, align="left", bold=False)
    f.link("e1", "OP", "b", "MS", "t", style="main", label="test request", lpos=(157, 124))
    f.link("e2", "MS", "r@168", "AD", "l@168", label="action $a_k$", lpos=(288, 162), lanchor="middle")
    f.link("e3", "AD", "l@204", "MS", "r@204", label="obs. $!I_k$", lpos=(288, 222), lanchor="middle")
    f.link("e4", "AD", "r@168", "IUT", "l@168", label="stimulus", lpos=(550, 162), lanchor="middle")
    f.link("e5", "IUT", "l@204", "AD", "r@204", label="raw records", lpos=(550, 222), lanchor="middle")
    f.link("e6", "AD", "b", "CLK", "t", label="$t_k$ \u00b1 $\u03b5$", lpos=(426, 266))
    f.link("e7", "IUT", "b", "IB", "t", style="dep", arrow="open", label="call and state only;\nnot algorithm evidence", lpos=(664, 282), lanchor="end")
    f.legend = [("main", "information flow"), ("dep", "non-evidential dependency")]
    f.legend_y = 398
    return f


def fig02() -> Figure:
    f = Figure("FIG-CL-TAV-02-requirement-layers-v2", 780, 500)
    f.n("L1", 16, 16, 372, 116, "Method goals", "", shape="frame", fill="none", stroke=MUTED)
    for i, t in enumerate(["CL-RQ1  loop consistency", "CL-RQ2  comparative effect", "CL-RQ3  uncertainty and stopping"]):
        f.n(f"G{i}", 36, 40 + i * 30, 332, 24, t, fill=KEY, title_size=11.5, bold=False)
    f.n("L2", 16, 170, 372, 166, "Protocol CRS", "", shape="frame", fill="none", stroke=MUTED)
    crs = ["INFORMATION", "UPLOAD", "Media-defined DOWNLOAD", "Operator-defined DOWNLOAD", "FIND", "abort / reject / retry"]
    for i, t in enumerate(crs):
        f.n(f"C{i}", 28 + (i % 2) * 180, 198 + (i // 2) * 44, 170, 32, t, title_size=11, bold=(t == "UPLOAD"),
            fill=WHITE if t != "UPLOAD" else KEY)
    f.n("L3", 16, 376, 372, 74, "Tool requirements", "", shape="frame", fill="none", stroke=MUTED)
    f.n("TR", 36, 402, 332, 36, "deferred to a later development-ready PR", "", dash=True, fill=GREY, title_size=11, bold=False)
    f.link("d1", "L1", "b", "L2", "t", style="dep", arrow="open", label="uses protocol obligations", lpos=(208, 155))
    f.link("d2", "L2", "b", "L3", "t", style="dep", arrow="open", label="may later implement", lpos=(208, 361))
    f.n("FT", 416, 16, 354, 434, "Representative trace", "E1 subset", shape="frame", fill="none", stroke=MUTED)
    chain = [
        ("SU", "Source unit: 615A-3 \u00a76.3.2, chart A, E007", False, KEY),
        ("R1", "CRS-M1-00365", False, WHITE),
        ("R2", "CRS-M1-00366", False, WHITE),
        ("R3", "CRS-M1-00367", False, WHITE),
        ("CO", "Constraint: LUR write order", False, WHITE),
        ("VC", "Test / Analysis verification case", True, WHITE),
        ("TM", "Tool module (later PR)", True, GREY),
        ("EV", "Evidence (not executed)", True, GREY),
    ]
    for i, (nid, t, planned, fill) in enumerate(chain):
        f.n(nid, 432, 46 + i * 50, 310, 30, t, fill=fill, dash=planned, title_size=11, bold=(i == 0))
    for i in range(len(chain) - 1):
        a, b = chain[i][0], chain[i + 1][0]
        planned = chain[i + 1][2]
        f.link(f"t{i}", a, "b", b, "t", style="dep" if planned else "main", arrow="open" if planned else "end",
               )
    f.link("x", "C1", "r", "SU", "l", via=[(400, 214), (400, 61)], style="dep", arrow="open", label="traced\nexample", lpos=(396, 152), lanchor="end")
    f.n("NT", 16, 462, 748, 30, "", "Bound M1 identifiers. DOWNLOAD and FIND traces await source-unit audit; satisfy/verify are model relations, no executed verification is claimed.",
        shape="text", align="left", bold=False)
    f.legend = []
    return f


def fig03() -> Figure:
    f = Figure("FIG-CL-TAV-03-bdd-v2", 780, 440)
    B = dict(stereo="\u00abblock\u00bb", h=78)
    def blk(nid, x, y, t, d, fill=WHITE, dash=False):
        f.n(nid, x, y, 210, B["h"], t, d, stereo=B["stereo"], fill=fill, dash=dash)
    blk("TE", 30, 30, "Test", "$t$ \u2208 $!T$($q_k$);  cost($t$) \u2265 $c_{min}$")
    blk("OB", 285, 30, "Observation", "$!I_k$, observable summary $q_k$;\nERROR if instrument invalid", KEY)
    blk("AN", 540, 30, "Analysis", "constraint verdict;\nsame partitions as scoring", KEY)
    blk("DI", 540, 280, "Diagnosis", "candidate set $!H_k$;\ncompatibility update", KEY)
    blk("SE", 30, 280, "Selection", "one-step min-max $s$($t$);\nPREP / RECOVER actions")
    blk("EV", 285, 158, "Evidence", "traces, stop class,\nresource remainder", GREY)
    f.link("a1", "TE", "r", "OB", "l", label="execute", lpos=(262, 62), lanchor="middle")
    f.link("a2", "OB", "r", "AN", "l", label="$!I_k$", lpos=(517, 62), lanchor="middle")
    f.link("a3", "AN", "b", "DI", "t", label="compatible /\ninconsistent", lpos=(651, 186))
    f.link("a4", "DI", "l", "SE", "r", label="remaining $!H_k$", lpos=(390, 312), lanchor="middle")
    f.link("a5", "SE", "t", "TE", "b", label="next TEST,\nPREP or stop", lpos=(129, 186), lanchor="end")
    f.link("d1", "EV", "t", "OB", "b", style="dep", arrow="open")
    f.link("d2", "EV", "l", "SE", "t@190", via=[(190, 197)], style="dep", arrow="open")
    f.link("d3", "EV", "r", "DI", "t@580", via=[(580, 197)], style="dep", arrow="open")
    f.n("NT", 30, 384, 720, 22, "", "Blocks are logical classifiers, not implemented modules.", shape="text", align="left", bold=False)
    f.legend = [("main", "directed association"), ("dep", "\u00abtrace\u00bb dependency"), ("fill:" + KEY, "analysis core")]
    f.legend_y = 428
    return f


def fig04() -> Figure:
    f = Figure("FIG-CL-TAV-04-ibd-v2", 780, 410)
    f.n("C", 290, 85, 200, 220, "ibd", "controller", shape="frame", fill="#F7FAFE", stroke="#333333")
    f.n("CT", 320, 165, 140, 60, "Msess", "holds $!H$, $q$, journal", shape="text")
    ports = {"PT": (284, 124, "trace"), "PC": (284, 244, "constraint"), "PH": (484, 124, "candidate-set"),
             "PS": (484, 244, "test-selection"), "PB": (384, 299, "")}
    for pid, (x, y, t) in ports.items():
        f.n(pid, x, y, 12, 12, "", shape="port", fill=WHITE)
        if t:
            f.n(pid + "L", x + 16 if x < 400 else x - 92, y - 4, 88, 20, t, shape="text", title_size=10.5, bold=False)
    f.n("PBL", 366, 276, 60, 16, "budget", shape="text", title_size=10.5, bold=False)
    f.n("AD", 40, 100, 150, 60, "Protocol adapter", "connects to Mprot")
    f.n("CE", 40, 220, 150, 60, "Constraint evaluator", "", title_size=11.5)
    f.n("CS", 590, 100, 150, 60, "Candidate store", "$!H_k$")
    f.n("TL", 590, 220, 150, 60, "Test library", "$!T$($q_k$): TEST, PREP,\nRECOVER")
    f.n("BC", 315, 345, 150, 44, "Budget / $K_{max}$ clock", "", title_size=11.5)
    f.link("c1", "AD", "r", "PT", "l", arrow="none", label="$!I_k$, records", lpos=(237, 124), lanchor="middle")
    f.link("c2", "CE", "r", "PC", "l", arrow="none", label="verdict", lpos=(237, 244), lanchor="middle")
    f.link("c3", "PH", "r", "CS", "l", arrow="none", label="$!H_k$", lpos=(539, 124), lanchor="middle")
    f.link("c4", "PS", "r", "TL", "l", arrow="none", label="$!T$($q_k$)", lpos=(539, 244), lanchor="middle")
    f.link("c5", "PB", "b", "BC", "t", arrow="none", label="cost, rounds", lpos=(396, 332))
    f.n("N1", 30, 330, 240, 44, "", "Only the adapter talks to Mprot;\nMsess never holds protocol state.", shape="note", fill=WHITE, stroke=MUTED, align="left", bold=False)
    f.n("N2", 510, 330, 250, 44, "", "Each action or ERROR costs at least\n$c_{min}$ or one $K_{max}$ round.", shape="note", fill=WHITE, stroke=MUTED, align="left", bold=False)
    f.legend = []
    f.shift(-70)
    return f


def fig05a() -> Figure:
    return fig05("FIG-CL-TAV-05-closed-loop-v4a", [70, 128, 186, 244, 302, 360, 470, 570, 670, 770, 872])


def fig05b() -> Figure:
    f = Figure("FIG-CL-TAV-05-closed-loop-v4", 800, 630)
    LX, LW, RX, RW = 236, 210, 486, 286
    f.n("S0", LX, 14, LW, 52, "S0  Initialise session", "$!H_0$, resource mode,\nretry counter")
    f.n("S1", LX, 100, LW, 44, "S1  Resource / stop gate", "IF-RESOURCE-STOP")
    f.n("S2", LX, 176, LW, 62, "S2  Predict observation\nclasses", "IF-PRED-OBS", fill=KEY)
    f.n("S3", LX, 270, LW, 70, "S3  Select and admit\none action", "IF-SELECT-ADMIT:\nTEST | PREP | RECOVER", fill=KEY)
    f.n("S10", LX, 486, LW, 50, "S10  Stop rules P1\u2013P5", "IF-RESOURCE-STOP, IF-EQUIV")
    f.n("S4", RX, 100, RW, 36, "S4  Charge declared cost once")
    f.n("S5", RX, 166, RW, 44, "S5  Execute and record effect", "IF-EXECUTE-RECORD")
    f.n("S6", RX, 240, RW, 44, "S6  Interpret observation", "IF-OBS-INTERPRET", fill=KEY)
    f.n("D1", 554, 314, 150, 60, "record valid?", shape="diamond", title_size=11.5)
    f.n("S8", 506, 410, 128, 44, "S8  Confirm RECOVER", "sole KNOWN writer", title_size=11)
    f.n("S7", 646, 410, 126, 48, "S7  Contain effect", "keep or invalidate $q$", fill=ERR_FILL, stroke=ERR)
    f.n("S9", RX, 486, 150, 50, "S9  Update history", "$!H$ \u2190 $!H$ \u2229 $!I_z$", fill=KEY)
    f.n("SE", 650, 494, 118, 30, "Stop-Error", shape="pill", fill=GREY, stroke=MUTED)
    f.n("T", 8, 50, 150, 552, "Terminal", "", shape="frame", fill=GREY, stroke=MUTED)
    term = [
        ("TA3", "Stop-NoDistinguisher", 79, "A3", "S1"), ("TA25", "Stop-Budget", 109, "A2/5", "S1"),
        ("TA4", "Stop-Error", 139, "A4", "S1"),
        ("TPG", "Stop-Prediction-Gap", 194, "", "S2"),
        ("TAD", "ADMIT", 262, "", "S3"), ("TSE", "Spec. error", 296, "$!S$=\u2205", "S3"),
        ("TP1", "Stop-Empty", 434, "P1", "S10"), ("TP2", "Stop-Singleton", 466, "P2", "S10"),
        ("TP3", "Stop-645", 498, "P3", "S10"), ("TP4", "Stop-Equivalent", 530, "P4", "S10"),
        ("TP5", "Stop-Budget", 562, "P5", "S10"),
    ]
    for tid, t, ty, _, _ in term:
        f.n(tid, 14, ty, 136, 26, t, shape="round", title_size=10.5)
    f.link("e01", "S0", "b", "S1", "t")
    f.link("e12", "S1", "b", "S2", "t")
    f.link("e23", "S2", "b", "S3", "t")
    f.link("e34", "S3", "r", "S4", "l", via=[(466, 305), (466, 118)])
    f.link("e45", "S4", "b", "S5", "t")
    f.link("e56", "S5", "b", "S6", "t")
    f.link("e6d", "S6", "b", "D1", "t")
    f.link("ed8", "D1", "b", "S8", "t@570", via=[(629, 392), (570, 392)], label="RECOVER", lpos=(624, 405), lanchor="end")
    f.link("ed9", "D1", "l", "S9", "t@496", via=[(496, 344)], label="TEST /\nPREP", lpos=(452, 380))
    f.link("e89", "S8", "b", "S9", "t@570")
    f.link("e910", "S9", "l", "S10", "r")
    f.link("ed7", "D1", "r", "S7", "t@722", via=[(722, 344)], style="err",
           label="invalid or\nunconfirmed", lpos=(716, 384), lanchor="end")
    f.link("e7loop", "S7", "r@424", "S1", "t@430", via=[(784, 424), (784, 86), (430, 86)], style="err",
           label="retry < cap", lpos=(780, 404), lanchor="end")
    f.link("e7stop", "S7", "b", "SE", "t", style="err", label="cap", lpos=(715, 478))
    f.link("eloop", "S10", "b", "S1", "t@400", via=[(341, 562), (792, 562), (792, 78), (400, 78)], style="loop",
           label="continue", lpos=(560, 576))
    BUS = 202
    for tid, _, ty, guard, src in term:
        sy = f.a(src, "l")[1]
        cy = ty + 13
        f.link("s-" + tid, src, "l", tid, "r", via=[(BUS, sy), (BUS, cy)] if abs(sy - cy) > 0.5 else [], style="stop",
               label=guard, lpos=(166, cy - 4))
    for lid, src, t in (("LS1", "S1", "decided"), ("LS2", "S2", "gap"), ("LS3", "S3", "select"), ("LS10", "S10", "P1\u2013P5")):
        f.n(lid, 208, f.a(src, "l")[1] - 15, 32, 14, t, shape="text", title_size=10, bold=False)
    f.legend = [("main", "control flow"), ("loop", "next round"), ("err", "error containment"), ("stop", "termination"), ("fill:" + KEY, "analysis core")]
    f.legend_y = 614
    f.legend_x = 180
    f.h = 630
    return f


def fig05(name: str = "FIG-CL-TAV-05-closed-loop-v3", ys: list[int] | None = None) -> Figure:
    f = Figure(name, 800, 900)
    MX, MW = 250, 270
    f.n("S0", MX, 20, MW, 52, "S0  Initialise session", "$!H_0$, resource mode, retry counter")
    f.n("S1", MX, 102, MW, 44, "S1  Resource / stop gate", "IF-RESOURCE-STOP")
    f.n("S2", MX, 176, MW, 62, "S2  Predict observation classes", "IF-PRED-OBS", fill=KEY)
    f.n("S3", MX, 268, MW, 62, "S3  Select and admit one action", "IF-SELECT-ADMIT: TEST | PREP | RECOVER", fill=KEY)
    f.n("S4", MX, 360, MW, 36, "S4  Charge declared cost once")
    f.n("S5", MX, 426, MW, 44, "S5  Execute and record effect", "IF-EXECUTE-RECORD")
    f.n("S6", MX, 500, MW, 44, "S6  Interpret observation", "IF-OBS-INTERPRET", fill=KEY)
    f.n("D1", MX + 60, 574, MW - 120, 60, "record valid?", shape="diamond", title_size=11.5)
    f.n("S8", MX + 60, 670, 150, 44, "S8  Confirm RECOVER", "sole KNOWN writer", title_size=11.5)
    f.n("S9", MX, 744, MW, 50, "S9  Update history", "$!H$ \u2190 $!H$ \u2229 $!I_z$", fill=KEY)
    f.n("S10", MX, 824, MW, 50, "S10  Stop rules P1\u2013P5", "IF-RESOURCE-STOP, IF-EQUIV")
    f.n("S7", 568, 500, 218, 64, "S7  Contain effect",
        "CONFIRMED-NOT-SENT keeps $q$;\nUNKNOWN-EFFECT invalidates $q$", fill=ERR_FILL, stroke=ERR)
    f.n("SE", 612, 700, 130, 34, "Stop-Error", shape="pill", fill=GREY, stroke=MUTED)
    f.n("T", 8, 50, 150, 856, "Terminal", "", shape="frame", fill=GREY, stroke=MUTED)
    # (id, label, top y, guard on the branch, source step)
    term = [
        ("TA3", "Stop-NoDistinguisher", 80, "A3", "S1"), ("TA25", "Stop-Budget", 110, "A2/5", "S1"),
        ("TA4", "Stop-Error", 140, "A4", "S1"),
        ("TPG", "Stop-Prediction-Gap", 194, "", "S2"),
        ("TAD", "ADMIT", 270, "", "S3"), ("TSE", "Spec. error", 302, "$!S$=∅", "S3"),
        ("TP1", "Stop-Empty", 752, "P1", "S10"), ("TP2", "Stop-Singleton", 782, "P2", "S10"),
        ("TP3", "Stop-645", 812, "P3", "S10"), ("TP4", "Stop-Equivalent", 842, "P4", "S10"),
        ("TP5", "Stop-Budget", 872, "P5", "S10"),
    ]
    if ys:
        term = [(a, b, y, c, d) for (a, b, _, c, d), y in zip(term, ys)]
    for tid, t, ty, _, _ in term:
        f.n(tid, 14, ty, 136, 26, t, shape="round", title_size=10.5)
    f.link("e01", "S0", "b", "S1", "t")
    f.link("e12", "S1", "b", "S2", "t")
    f.link("e23", "S2", "b", "S3", "t")
    f.link("e34", "S3", "b", "S4", "t")
    f.link("e45", "S4", "b", "S5", "t")
    f.link("e56", "S5", "b", "S6", "t")
    f.link("e6d", "S6", "b", "D1", "t")
    f.link("ed8", "D1", "b", "S8", "t", label="RECOVER", lpos=(380, 660), lanchor="end")
    f.link("ed9", "D1", "b", "S9", "t@482", via=[(385, 652), (482, 652)], label="TEST / PREP", lpos=(488, 700))
    f.link("e89", "S8", "b", "S9", "t@385")
    f.link("e910", "S9", "b", "S10", "t")
    f.link("eloop", "S10", "r", "S1", "r", via=[(545, 849), (545, 124)], style="loop", label="continue", lpos=(551, 330))
    f.link("ed7", "D1", "r", "S7", "l@550", via=[(552, 604), (552, 550)], style="err",
           label="invalid or\nunconfirmed", lpos=(560, 618))
    f.link("e7loop", "S7", "t", "S1", "r@116", via=[(677, 116)], style="err", label="retry < cap", lpos=(683, 330))
    f.link("e7stop", "S7", "b", "SE", "t", style="err", label="cap reached", lpos=(683, 690))
    BUS = 202
    for tid, _, ty, guard, src in term:
        sy = f.a(src, "l")[1]
        cy = ty + 13
        f.link("s-" + tid, src, "l", tid, "r", via=[(BUS, sy), (BUS, cy)] if abs(sy - cy) > 0.5 else [], style="stop",
               label=guard, lpos=(166, cy - 4))
    f.n("LS1", 204, 108, 50, 14, "decided", shape="text", title_size=10, bold=False)
    f.n("LS2", 204, 191, 50, 14, "gap", shape="text", title_size=10, bold=False)
    f.n("LS3", 204, 283, 50, 14, "select", shape="text", title_size=10, bold=False)
    f.n("LS10", 204, 833, 50, 14, "P1\u2013P5", shape="text", title_size=10, bold=False)
    f.legend = [("main", "control flow"), ("loop", "next round"), ("err", "error containment"), ("stop", "termination"), ("fill:" + KEY, "analysis core")]
    f.legend_y = 922
    f.legend_x = 180
    f.h = 936
    return f


def fig06() -> Figure:
    f = Figure("FIG-CL-TAV-06-diagnostic-sequence-v2", 780, 610)
    L = {"OP": (10, 100, "Operator", ""), "MS": (140, 120, "Msess", "session"), "MP": (500, 120, "Mprot", "protocol"),
         "AN": (650, 120, "Analysis", "and diagnosis")}
    for k, (x, w, t, d) in L.items():
        f.n(k, x, 16, w, 410, t, d, shape="lifeline", fill=KEY if k == "MS" else WHITE)
    cx = {k: x + w / 2 for k, (x, w, _, _) in L.items()}

    def msg(i, a, b, y, text, reply=False):
        f.e(f"m{i}", a, b, [(cx[a], y), (cx[b], y)], style="dep" if reply else "main", arrow="open" if reply else "end",
            label=text, lpos=((cx[a] + cx[b]) / 2, y - 5), lanchor="middle")

    def self_(i, y, text):
        x = cx["MS"]
        f.e(f"m{i}", "MS", "MS", [(x, y), (x + 26, y), (x + 26, y + 16), (x + 4, y + 16)], label=text, lpos=(x + 34, y + 4))

    msg(1, "OP", "MS", 76, "1  start ($!H_0$)")
    self_(2, 96, "2  Admit: overlapping classes stay strictly reducing")
    self_(3, 128, "3  uninformative TEST is not admitted")
    self_(4, 160, "4  select PREP from $!A$")
    msg(5, "MS", "MP", 206, "5  PREP action")
    msg(6, "MP", "MS", 238, "6  $q_{k+1}$", reply=True)
    self_(7, 258, "7  select distinguishing TEST $t_b$")
    msg(8, "MS", "MP", 304, "8  execute $t_b$")
    msg(9, "MP", "MS", 336, "9  observation separating $h_1$ / $h_2$", reply=True)
    msg(10, "MS", "AN", 372, "10  $!I_k$ of $t_b$")
    msg(11, "AN", "MS", 404, "11  $!H_k$ singleton, or still indistinguishable", reply=True)
    f.n("NT", 150, 440, 620, 30, "", "$!H_0$ = {$h_{normal}$} \u222a $!H_{single}$; admission, resource and recovery rules as in Alg. 1.",
        shape="note", fill=WHITE, stroke=MUTED, align="left", bold=False)
    f.legend = [("main", "message"), ("dep", "reply")]
    f.legend_y = 492
    f.legend_x = 150
    f.h = 506
    return f


def fig07() -> Figure:
    f = Figure("FIG-CL-TAV-07-two-state-machines-v2", 800, 640)
    f.n("FM", 10, 10, 590, 620, "stm Msess", "", shape="frame", fill="none", stroke="#333333")
    stops = {"SN": (90, "Stop-NoDistinguisher"), "SR": (129, "Stop-Error"), "SB": (250, "Stop-Budget"),
             "SM": (400, "Stop-Empty"), "SS": (440, "Stop-Singleton"), "S6": (480, "Stop-645"), "SQ": (520, "Stop-Equivalent")}
    for k, (y, t) in stops.items():
        f.n(k, 30, y, 140, 28, t, shape="pill", fill=GREY, stroke=MUTED, title_size=11)
    f.n("I0", 309, 46, 12, 12, shape="dot")
    f.n("ID", 250, 70, 130, 30, "Idle", title_size=12)
    f.n("AM", 250, 125, 130, 36, "Admit", fill=KEY)
    f.n("SL", 250, 210, 130, 30, "Select")
    f.n("EX", 250, 290, 130, 30, "Execute")
    f.n("UP", 250, 440, 130, 36, "Update", fill=KEY)
    f.n("EH", 430, 210, 140, 36, "ErrorHandle", fill=ERR_FILL, stroke=ERR)
    f.n("RC", 430, 360, 140, 36, "RecoverConfirm")
    f.link("t0", "I0", "b", "ID", "t@315")
    f.link("t1", "ID", "b", "AM", "t@315")
    f.link("t2", "AM", "b@315", "SL", "t@315", label="A1", lpos=(309, 190), lanchor="end")
    f.link("t3", "SL", "b@315", "EX", "t@315", label="chosen from $!S$", lpos=(321, 270))
    f.link("t4", "EX", "b@315", "UP", "t@315", label="TEST / PREP,\nvalid $!I_k$", lpos=(321, 345))
    f.link("t5", "EX", "r@298", "EH", "b@440", via=[(440, 298)], style="err", label="ERROR", lpos=(446, 272))
    f.link("t6", "EX", "r@314", "RC", "t@470", via=[(470, 314)], label="RECOVER\nrecord", lpos=(466, 336), lanchor="end")
    f.link("t7", "RC", "b@500", "UP", "r@458", via=[(500, 458)], label="target\nconfirmed", lpos=(494, 424), lanchor="end")
    f.link("t8", "RC", "r", "AM", "r@133", via=[(585, 378), (585, 133)], style="err", label="unconfirmed;\n$q$ UNKNOWN", lpos=(579, 336), lanchor="end")
    f.link("t9", "EH", "t@470", "AM", "r@151", via=[(470, 151)], style="err",
           label="CNS, or\nUNKNOWN with\nRECOVER \u2208 $!S$;\nretry left", lpos=(476, 164))
    f.link("t10", "EH", "t@566", "SR", "l", via=[(566, 36), (20, 36), (20, 143)], style="err")
    f.link("t11", "EH", "t@566", "SB", "l", via=[(566, 36), (20, 36), (20, 264)], style="err",
           label="ErrorHandle: retry cap or A4\n\u2192 Stop-Error;  A5 \u2192 Stop-Budget", lpos=(30, 54))
    f.link("a3", "AM", "l@135", "SN", "r", via=[(230, 135), (230, 104)], style="stop", label="A3", lpos=(176, 100))
    f.link("a4", "AM", "l@143", "SR", "r", style="stop", label="A4", lpos=(176, 139))
    f.link("a25", "AM", "l@151", "SB", "r", via=[(230, 151), (230, 264)], style="stop", label="A2, A5", lpos=(176, 260))
    f.link("p5", "UP", "l@444", "SB", "r", via=[(240, 444), (240, 264)], style="stop", label="P5", lpos=(246, 360))
    f.link("p1", "UP", "l@450", "SM", "r", via=[(215, 450), (215, 414)], style="stop", label="P1", lpos=(176, 410))
    f.link("p2", "UP", "l@456", "SS", "r@454", style="stop", label="P2", lpos=(176, 450))
    f.link("p3", "UP", "l@462", "S6", "r", via=[(215, 462), (215, 494)], style="stop", label="P3", lpos=(176, 490))
    f.link("p4", "UP", "l@470", "SQ", "r", via=[(230, 470), (230, 534)], style="stop", label="P4", lpos=(176, 530))
    f.link("lp", "UP", "r@470", "AM", "b@345", via=[(400, 470), (400, 192), (345, 192)], style="loop",
           label="else: |$!H$| > 1,\nresource left", lpos=(394, 398), lanchor="end")
    f.n("FP", 612, 10, 180, 280, "stm Mprot", "", shape="frame", fill="none", stroke="#333333")
    f.n("BM", 622, 44, 162, 92, "Bound M2", "INFORMATION / UPLOAD;\napproved model identity;\nno new behaviour edges", title_size=12)
    f.n("PL", 622, 156, 162, 120, "Planned CRS scope", "Media-defined and\nOperator-defined\nDOWNLOAD, FIND;\nno behaviour edges", dash=True, fill=GREY, title_size=12)
    f.n("GT", 612, 302, 180, 76, "", "Guards A1\u2013A5 and update\npriority P1\u2013P5 as in Alg. 1.\nNo cross-machine transition;\nports of Fig. 4 only.",
        shape="note", fill=WHITE, stroke=MUTED, align="left", bold=False)
    f.legend = [("main", "transition"), ("loop", "next round"), ("err", "error path"), ("stop", "to final state")]
    f.legend_y = 612
    f.legend_x = 24
    return f


def fig08() -> Figure:
    f = Figure("FIG-CL-TAV-08-parametric-v2", 780, 428)
    S = "\u00abconstraint\u00bb"
    f.n("IA", 30, 40, 180, 72, "Allowed interval", "$!I$: allowed timing interval", stereo=S, shape="round")
    f.n("EP", 30, 150, 180, 72, "Error bound", "$\u03b5$: measurement error", stereo=S, shape="round")
    f.n("JM", 270, 95, 190, 72, "Measured interval", "$!J$: feasible interval from\nmeasurement and $\u03b5$", stereo=S, shape="round", fill=KEY)
    f.n("UP", 540, 95, 220, 72, "History update", "$!H_{k+1}$ = {$h$ \u2208 $!H_k$ |\n$O$($h$, $t$, $q_k$) \u2229 $!I_k$ \u2260 \u2205}", stereo=S, shape="round", fill=KEY)
    f.n("CM", 30, 290, 200, 72, "Positive cost", "$c_{min}$ > 0; cost($t$) \u2265 $c_{min}$;\ncost(ERROR) \u2265 $c_{min}$", stereo=S, shape="round")
    f.n("BU", 270, 290, 190, 72, "Resource mode", "$B$ finite \u2295 $K_{max}$ finite", stereo=S, shape="round")
    f.n("SC", 540, 290, 220, 72, "Selection score", "$s$($t$) = worst remaining |$!H_k$|\nover Obs($t$, $q_k$)", stereo=S, shape="round")
    f.link("b1", "IA", "r", "JM", "l@120", via=[(235, 76), (235, 120)], style="bind", arrow="none", label="$!I$", lpos=(220, 71), lanchor="middle")
    f.link("b2", "EP", "r", "JM", "l@142", via=[(245, 186), (245, 142)], style="bind", arrow="none", label="$\u03b5$", lpos=(225, 181), lanchor="middle")
    f.link("b3", "JM", "r", "UP", "l", style="bind", arrow="none", label="$!J$", lpos=(500, 126), lanchor="middle")
    f.link("b4", "SC", "t", "UP", "b", style="bind", arrow="none", label="$!H_k$, Obs($t$, $q_k$)", lpos=(656, 232))
    f.link("b5", "BU", "r", "SC", "l", style="bind", arrow="none", label="mode", lpos=(500, 321), lanchor="middle")
    f.link("b6", "CM", "r", "BU", "l", style="bind", arrow="none", label="$c_{min}$", lpos=(250, 321), lanchor="middle")
    f.n("NT", 30, 384, 730, 30, "", "Constraints are displayed, not claimed solved; vanishing positive costs do not prove termination.",
        shape="note", fill=WHITE, stroke=MUTED, align="left", bold=False)
    f.legend = []
    return f


def fig09() -> Figure:
    f = Figure("FIG-CL-TAV-09-experiment-architecture-v2", 800, 430)
    f.n("LE", 180, 16, 610, 130, "Evaluator only", "", shape="frame", fill="#FAFAFA", stroke=MUTED)
    f.n("LA", 180, 186, 610, 130, "Algorithm visible", "", shape="frame", fill="#F7FAFE", stroke=MUTED)
    f.n("SC", 20, 46, 140, 250, "Controlled\nscenario", "IUT configuration,\nfault plan,\nresource mode\n\nfeeds the truth record\nand every arm from\nthe same declared\npool and action library", fill=WHITE)
    f.n("TR", 195, 46, 125, 80, "Truth record", "injection plan and\nexecution confirmation", title_size=12)
    f.n("VA", 360, 46, 115, 80, "Validity check", "invalid, equivalent,\nmissing runs", title_size=12)
    f.n("ME", 515, 46, 130, 80, "Metrics", "DETECT / LOCATE /\nABLATION; attempt and\nanswered denominators", title_size=12)
    f.n("CL", 680, 46, 100, 80, "RQ claims", "comparable\nprojections;\nno unrun numbers", title_size=12)
    f.n("AR", 195, 216, 125, 80, "Comparison arms", "CL-T, CL-A,\nCL-TA, CL-LOOP", fill=KEY, title_size=12)
    f.n("OB", 360, 216, 115, 80, "Observations", "I\u2096, q, cost;\nresource log", title_size=12)
    f.link("f1", "SC", "r@86", "TR", "l@86")
    f.link("f2", "SC", "r@256", "AR", "l@256")
    f.link("f3", "TR", "r", "VA", "l")
    f.link("f4", "VA", "r", "ME", "l")
    f.link("f5", "ME", "r", "CL", "l")
    f.link("f6", "AR", "r", "OB", "l")
    f.link("f7", "OB", "t", "VA", "b", label="records", lpos=(424, 170))
    f.link("x1", "TR", "b", "AR", "t", style="forbid", label="never an\nalgorithm input", lpos=(264, 160))
    f.n("NT", 180, 330, 610, 70, "", "Evaluator truth never enters IF-SELECT-ADMIT, IF-PRED-OBS, IF-HIST-UPDATE or IF-EXECUTE-RECORD;\n"
        "IF-OBS-INTERPRET, IF-PREP-RECOVER, IF-EQUIV and IF-RESOURCE-STOP see algorithm-visible data only.\n"
        "A shared pool does not give CL-LOOP records to other arms, nor charge CL-A a fictional sampling cost.\n"
        "Experiment I/O: IF-EXP-SCENE, -INJECT, -TRUTH, -COLLECT, -RUN, -FILTER, -EVAL.",
        shape="note", fill=WHITE, stroke=MUTED, align="left", bold=False)
    f.legend = [("main", "data flow"), ("forbid", "forbidden leakage"), ("fill:" + KEY, "method under test")]
    f.legend_y = 418
    f.legend_x = 180
    f.h = 430
    return f


def fig09v3() -> Figure:
    f = Figure("FIG-CL-TAV-09-experiment-architecture-v3", 800, 760)
    MX, MW = 250, 300
    f.n("EV", 12, 102, 200, 548, "Evaluator only", "", shape="frame", fill=GREY, stroke=MUTED)
    f.n("AV", 236, 176, 328, 220, "Algorithm visible", "", shape="frame", fill="#F7FAFE", stroke=ACCENT)
    f.n("XO", 600, 404, 188, 246, "Excluded, still counted", "", shape="frame", fill=GREY, stroke=MUTED)

    f.n("E0", MX, 20, MW, 56, "E0  Declare scenario pool", "IUT configuration, fault plan, resource mode;\nfixed before any run  (IF-EXP-SCENE)")
    f.n("E1", MX, 100, MW, 62, "E1  Inject fault, confirm execution", "truth recorded before any arm runs\n(IF-EXP-INJECT, IF-EXP-TRUTH)")
    f.n("E2", MX, 206, MW, 112, "E2  Run arms", "same pool and action library  (IF-EXP-RUN)", shape="frame", fill=WHITE, stroke="#333333")
    arms = [("CL-T", "test\nonly"), ("CL-A", "analysis\nonly"), ("CL-TA", "test +\nanalysis"), ("CL-LOOP", "closed\nloop")]
    for i, (t, d) in enumerate(arms):
        f.n(f"A{i}", MX + 10 + i * 72, 240, 66, 64, t, d, title_size=11, fill=KEY if t == "CL-LOOP" else WHITE)
    f.n("E3", MX, 340, MW, 44, "E3  Collect records", "$!I_k$, $q$, cost, resource log  (IF-EXP-COLLECT)")
    f.n("E4", MX, 420, MW, 52, "E4  Validity filter", "invalid, equivalent or missing runs leave\nthe answered subset  (IF-EXP-FILTER)")
    f.n("E5", MX, 502, MW, 62, "E5  Evaluate against truth", "DETECT / LOCATE / ABLATION with attempt\nand answered-subset denominators  (IF-EXP-EVAL)", fill=KEY)
    f.n("E6", MX, 594, MW, 56, "E6  Answer CL-RQ1\u2013CL-RQ3", "reporting step only; comparable\nprojections, no unrun numbers")

    f.n("TR", 24, 130, 176, 96, "Truth record", "injection plan and\nexecution confirmation\n(IF-EXP-TRUTH)", fill=WHITE)
    f.n("TN", 18, 596, 188, 44, "", "Truth is never an\nalgorithm input.",
        shape="note", fill=WHITE, stroke=MUTED, align="left", bold=False)
    outs = [("invalid run", "unconfirmed injection\nor setup fault"), ("equivalent fault", "observationally\nindistinguishable"), ("missing record", "collection gap"), ("unanswered", "abstain; still counted")]
    y = 432
    for i, (t, d) in enumerate(outs):
        h = 26 + 13.5 * (d.count("\n") + 1)
        f.n(f"X{i}", 612, y, 164, h, t, d, shape="round", title_size=11)
        y += h + 6

    f.link("m0", "E0", "b", "E1", "t")
    f.link("m1", "E1", "b", "E2", "t")
    f.link("m2", "E2", "b", "E3", "t")
    f.link("m3", "E3", "b", "E4", "t")
    f.link("m4", "E4", "b", "E5", "t")
    f.link("m5", "E5", "b", "E6", "t")
    f.link("t1", "E1", "l", "TR", "r@131", via=[(226, 131)], label="truth first", lpos=(242, 125), lanchor="end")
    f.link("t2", "TR", "b@60", "E4", "l", via=[(60, 446)], label="evaluator-only check", lpos=(126, 440))
    f.link("t3", "TR", "b@120", "E5", "l", via=[(120, 533)], label="ground truth", lpos=(126, 527))
    f.link("x1", "TR", "r@200", "E2", "l@262", via=[(226, 200), (226, 262)], style="forbid", label="never an\nalgorithm input", lpos=(220, 252), lanchor="end")
    f.link("lp", "E3", "r", "E1", "r", via=[(580, 362), (580, 131)], style="loop", label="next scenario\n\u00d7 arm", lpos=(586, 240))
    f.link("ex", "E4", "r", "XO", "l@446", style="err", label="excluded", lpos=(575, 440), lanchor="middle")
    f.n("NT", 236, 666, 552, 30, "", "Shared pool: no arm sees CL-LOOP records; excluded runs stay in the attempt denominator.",
        shape="note", fill=WHITE, stroke=MUTED, align="left", bold=False)
    f.legend = [("main", "experiment flow"), ("loop", "repeat"), ("forbid", "forbidden leakage"), ("err", "exclusion"), ("fill:" + KEY, "method under test")]
    f.legend_y = 716
    f.legend_x = 24
    f.h = 730
    return f


FIGS = {"01": fig01, "02": fig02, "03": fig03, "04": fig04, "05": fig05b, "06": fig06, "07": fig07, "08": fig08, "09": fig09v3}

if __name__ == "__main__":
    for key in sys.argv[1:] or FIGS:
        fig = FIGS[key]()
        write(fig, OUT)
        print(fig.name, fig.w, fig.h)
