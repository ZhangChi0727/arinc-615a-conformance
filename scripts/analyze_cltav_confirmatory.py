"""Read-only analysis of confirmatory JSONL.  Pure functions are importable."""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from a615a_sim.algorithm.hypothesis_model import map_to_parent_hypotheses  # noqa: E402

DESIGN_PATH = ROOT / "configs/research/cltav_confirmatory_design_draft_v1.json"
RAW_PATH = ROOT / "artifacts/confirmatory/cltav_confirmatory_attempts_v1.jsonl"
OUT_PATH = ROOT / "artifacts/confirmatory/cltav_confirmatory_analysis_v1.json"
NORMAL_TRUTH = frozenset({"h_normal", "h-normal"})
# Pre-run exclusions documented by CR-2026-031 / RR-PR31-001.
# E3: unresolved LATE vs ABSENT equivalence under a short window.
E3_EXCLUDED = frozenset({"HC-LATE-ABSENT-SHORT-WINDOW"})
# T3: endpoint truth unresolved.
T3_EXCLUDED = frozenset({"HC-FIND-ENDPOINT"})
FAMILYWISE_ALPHA = 0.05


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def pre_run_exclusion_reason(unit: Mapping[str, Any]) -> str | None:
    marked = str(unit.get("preRunExclusion") or "")
    if unit.get("e3Excluded") or unit.get("excludedUnderE3") or marked == "E3":
        return "E3"
    if unit.get("t3Excluded") or unit.get("excludedUnderT3") or marked == "T3":
        return "T3"
    harder = unit.get("harderCaseId")
    if harder in E3_EXCLUDED:
        return "E3"
    if harder in T3_EXCLUDED:
        return "T3"
    return None


def pre_run_excluded_units(design: Mapping[str, Any]) -> dict[str, str]:
    """Map unitId -> reason ('E3' or 'T3') for documented pre-run exclusions."""

    excluded: dict[str, str] = {}
    for unit in design.get("units") or []:
        reason = pre_run_exclusion_reason(unit)
        if reason is not None:
            excluded[str(unit["unitId"])] = reason
    return excluded


def pre_run_excluded_unit_counts(design: Mapping[str, Any]) -> dict[str, int]:
    reasons = list(pre_run_excluded_units(design).values())
    return {"E3": reasons.count("E3"), "T3": reasons.count("T3")}


def binom_cdf(k: int, n: int, p: float) -> float:
    if n < 0:
        raise ValueError("n must be nonnegative")
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    total = 0.0
    q = 1.0 - p
    for i in range(k + 1):
        total += math.comb(n, i) * (p**i) * (q ** (n - i))
    return total


def mcnemar_two_sided(b: int, c: int) -> float:
    discordant = b + c
    if discordant == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2.0 * binom_cdf(k, discordant, 0.5))


def _bisect_p(target_cdf: float, x: int, n: int) -> float:
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2.0
        value = binom_cdf(x, n, mid)
        if value > target_cdf:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def clopper_pearson(x: int, n: int, alpha: float = 0.05) -> tuple[float | None, float | None]:
    if n == 0:
        return None, None
    if x < 0 or x > n:
        raise ValueError("x must lie in [0, n]")
    lower = 0.0 if x == 0 else _bisect_p(1.0 - alpha / 2.0, x - 1, n)
    upper = 1.0 if x == n else _bisect_p(alpha / 2.0, x, n)
    return lower, upper


def holm_adjust(pvalues: Sequence[tuple[str, float]], alpha: float = FAMILYWISE_ALPHA) -> dict[str, float]:
    ordered = sorted(pvalues, key=lambda item: (item[1], item[0]))
    m = len(ordered)
    adjusted: dict[str, float] = {}
    running = 0.0
    for index, (name, pvalue) in enumerate(ordered):
        factor = m - index
        candidate = min(1.0, pvalue * factor)
        running = max(running, candidate)
        adjusted[name] = running
    return adjusted


def m_detect(row: Mapping[str, Any]) -> int:
    truth = str(row.get("truthParentHypothesis") or "")
    if truth in NORMAL_TRUTH:
        raise ValueError("M-DETECT is defined on fault units only")
    return 1 if row.get("verdict") == "FAIL" else 0


def m_localise(row: Mapping[str, Any]) -> int:
    truth = str(row.get("truthParentHypothesis") or "")
    if truth in NORMAL_TRUTH:
        raise ValueError("M-LOCALISE is defined on fault units only")
    candidates = row.get("finalCandidateSet") or []
    mapped = list(map_to_parent_hypotheses([str(item) for item in candidates]))
    return 1 if mapped == [truth] else 0


def _by_unit_arm(rows: Iterable[Mapping[str, Any]]) -> dict[tuple[str, str], Mapping[str, Any]]:
    table: dict[tuple[str, str], Mapping[str, Any]] = {}
    for row in rows:
        table[(str(row["unitId"]), str(row.get("arm") or row.get("armId")))] = row
    return table


def paired_metric(
    rows: Sequence[Mapping[str, Any]],
    *,
    left_arm: str,
    right_arm: str,
    metric,
    excluded_units: Mapping[str, str] | set[str],
) -> dict[str, Any]:
    table = _by_unit_arm(rows)
    units = sorted({row["unitId"] for row in rows})
    excluded = set(excluded_units)
    b = 0
    c = 0
    used = 0
    left_ones = 0
    right_ones = 0
    missing_dropped = 0
    undefined_dropped = 0
    for unit in units:
        if unit in excluded:
            continue
        left = table.get((unit, left_arm))
        right = table.get((unit, right_arm))
        if left is None or right is None:
            continue
        statuses = {left.get("status"), right.get("status")}
        if "UNDEFINED-OUTCOME" in statuses:
            undefined_dropped += 1
            continue
        if "MISSING" in statuses:
            missing_dropped += 1
            continue
        truth = str(left.get("truthParentHypothesis") or "")
        if truth in NORMAL_TRUTH or not truth:
            continue
        left_v = metric(left)
        right_v = metric(right)
        used += 1
        left_ones += left_v
        right_ones += right_v
        if left_v == 1 and right_v == 0:
            b += 1
        elif left_v == 0 and right_v == 1:
            c += 1
    n = used
    discordant = b + c
    pvalue = mcnemar_two_sided(b, c)
    difference = None if n == 0 else (b - c) / n
    ci_low, ci_high = clopper_pearson(b, discordant) if discordant else (None, None)
    return {
        "n": n,
        "b": b,
        "c": c,
        "p": pvalue,
        "pointDifference": difference,
        "clopperPearsonBOverBPlusC": {"lower": ci_low, "upper": ci_high},
        "leftOnes": left_ones,
        "rightOnes": right_ones,
        "undefinedOutcomeDropped": undefined_dropped,
        "missingDropped": missing_dropped,
    }


def _median_min_max(values: Sequence[int]) -> dict[str, Any]:
    if not values:
        return {"median": None, "min": None, "max": None}
    return {
        "median": statistics.median(values),
        "min": min(values),
        "max": max(values),
    }


def secondary_descriptive(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_arm: dict[str, list[Mapping[str, Any]]] = {}
    for row in rows:
        if row.get("status") == "MISSING":
            continue
        arm = str(row.get("arm") or row.get("armId"))
        by_arm.setdefault(arm, []).append(row)
    out: dict[str, Any] = {}
    for arm, items in sorted(by_arm.items()):
        normals = [
            item
            for item in items
            if str(item.get("truthParentHypothesis") or "") in NORMAL_TRUTH
        ]
        false_fails = sum(1 for item in normals if item.get("verdict") == "FAIL")
        inconclusive = sum(1 for item in items if item.get("verdict") == "INCONCLUSIVE")
        rounds = [
            int(item["roundsConsumed"])
            for item in items
            if item.get("roundsConsumed") is not None
        ]
        stops = Counter(str(item.get("stopClass") or "NONE") for item in items)
        out[arm] = {
            "falseFailShare": {
                "numerator": false_fails,
                "denominator": len(normals),
            },
            "inconclusiveShare": {
                "numerator": inconclusive,
                "denominator": len(items),
            },
            "rounds": _median_min_max(rounds),
            "stopClassCounts": dict(stops),
        }
    return out


def analyze_rows(
    rows: Sequence[Mapping[str, Any]],
    *,
    design: Mapping[str, Any],
) -> dict[str, Any]:
    excluded = pre_run_excluded_units(design)
    h1 = paired_metric(
        rows,
        left_arm="CL-LOOP",
        right_arm="CL-T",
        metric=m_detect,
        excluded_units=excluded,
    )
    h2 = paired_metric(
        rows,
        left_arm="CL-LOOP",
        right_arm="CL-TA",
        metric=m_localise,
        excluded_units=excluded,
    )
    adjusted = holm_adjust([("H1", float(h1["p"])), ("H2", float(h2["p"]))])
    contrasts = {
        "H1": {
            **h1,
            "metric": "M-DETECT",
            "comparison": "CL-LOOP vs CL-T",
            "holmAdjustedP": adjusted["H1"],
            "supported": bool(adjusted["H1"] < FAMILYWISE_ALPHA and h1["b"] > h1["c"]),
        },
        "H2": {
            **h2,
            "metric": "M-LOCALISE",
            "comparison": "CL-LOOP vs CL-TA",
            "holmAdjustedP": adjusted["H2"],
            "supported": bool(adjusted["H2"] < FAMILYWISE_ALPHA and h2["b"] > h2["c"]),
        },
    }
    return {
        "label": "CONFIRMATORY / SIMULATED-IUT",
        "preRunExcludedUnitCounts": pre_run_excluded_unit_counts(design),
        "contrasts": contrasts,
        "holm": adjusted,
        "alpha": FAMILYWISE_ALPHA,
        "secondary": secondary_descriptive(rows),
    }


def write_analysis(
    *,
    rows: Sequence[Mapping[str, Any]],
    design: Mapping[str, Any],
    out_path: Path = OUT_PATH,
) -> dict[str, Any]:
    if out_path.exists():
        print(f"{out_path} already exists", file=sys.stderr)
        raise SystemExit(2)
    payload = analyze_rows(rows, design=design)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only confirmatory analysis.")
    parser.add_argument("--jsonl", type=Path, default=RAW_PATH)
    parser.add_argument("--design", type=Path, default=DESIGN_PATH)
    parser.add_argument("--out", type=Path, default=OUT_PATH)
    args = parser.parse_args(argv)
    design = load_json(args.design)
    rows = load_jsonl(args.jsonl)
    payload = write_analysis(rows=rows, design=design, out_path=args.out)
    print(json.dumps({"written": str(args.out), "contrasts": list(payload["contrasts"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
