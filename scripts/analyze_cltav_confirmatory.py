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
EXPECTED_PATH = ROOT / "configs/research/cltav_confirmatory_expected_behaviour_v1.json"
REGISTRATION_PATH = ROOT / "configs/research/cltav_confirmatory_registration_v3.json"
RAW_PATH = ROOT / "artifacts/confirmatory/cltav_confirmatory_attempts_v1.jsonl"
OUT_PATH = ROOT / "artifacts/confirmatory/cltav_confirmatory_analysis_v1.json"
NORMAL_TRUTH = frozenset({"h_normal", "h-normal"})
FAMILYWISE_ALPHA = 0.05


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def load_expected_behaviour(path: Path = EXPECTED_PATH) -> dict[str, Any]:
    return load_json(path)


def expected_by_unit_id(expected: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(entry["unitId"]): dict(entry) for entry in expected.get("units") or []}


def eligible_unit_ids(expected: Mapping[str, Any]) -> set[str]:
    return {str(entry["unitId"]) for entry in expected.get("units") or []}


def null_expectation_count(expected: Mapping[str, Any]) -> int:
    return len(list(expected.get("needsDmRuling") or []))


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


def _acceptable_verdicts(expected: Mapping[str, Any]) -> list[str]:
    if expected.get("acceptableVerdicts") is not None:
        return [str(item) for item in expected["acceptableVerdicts"]]
    single = expected.get("expectedVerdict")
    return [] if single is None else [str(single)]


def _excludes_fail_and_pass(expected: Mapping[str, Any]) -> bool:
    acceptable = set(_acceptable_verdicts(expected))
    return "FAIL" not in acceptable and "PASS" not in acceptable


def scored_verdict(row: Mapping[str, Any]) -> str | None:
    if row.get("status") == "UNDEFINED-OUTCOME":
        return None
    value = row.get("verdict")
    return None if value is None else str(value)


def mapped_candidate_set(row: Mapping[str, Any]) -> list[str]:
    if row.get("status") == "UNDEFINED-OUTCOME":
        run = row.get("runRecord") or {}
        hypotheses = [str(item) for item in (run.get("finalHypotheses") or [])]
        if hypotheses:
            return sorted(map_to_parent_hypotheses(hypotheses))
    candidates = [str(item) for item in (row.get("finalCandidateSet") or [])]
    return sorted(map_to_parent_hypotheses(candidates))


def candidate_rule_holds(mapped: Sequence[str], rule: Mapping[str, Any] | None) -> bool:
    if not rule:
        return False
    kind = str(rule.get("kind") or "")
    values = list(mapped)
    if kind == "equals":
        want = sorted(str(item) for item in (rule.get("set") or []))
        return values == want
    if kind == "contains":
        return str(rule.get("member")) in values
    if kind == "notSingletonFault":
        return not (len(values) == 1 and values[0] not in NORMAL_TRUTH)
    return False


def m_detect_correct(row: Mapping[str, Any], expected: Mapping[str, Any]) -> int:
    verdict = scored_verdict(row)
    acceptable = _acceptable_verdicts(expected)
    if verdict is None:
        return 1 if _excludes_fail_and_pass(expected) else 0
    return 1 if verdict in acceptable else 0


def m_localise_correct(row: Mapping[str, Any], expected: Mapping[str, Any]) -> int:
    mapped = mapped_candidate_set(row)
    rule = expected.get("candidateRule")
    if rule is None and expected.get("expectedCandidateSet") is not None:
        rule = {"kind": "equals", "set": list(expected["expectedCandidateSet"])}
    return 1 if candidate_rule_holds(mapped, rule) else 0


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
    eligible_units: Mapping[str, Any] | set[str],
) -> dict[str, Any]:
    table = _by_unit_arm(rows)
    units = sorted({row["unitId"] for row in rows})
    eligible = set(eligible_units)
    b = 0
    c = 0
    used = 0
    left_ones = 0
    right_ones = 0
    missing_dropped = 0
    undefined_scored = 0
    for unit in units:
        if unit not in eligible:
            continue
        left = table.get((unit, left_arm))
        right = table.get((unit, right_arm))
        if left is None or right is None:
            continue
        statuses = {left.get("status"), right.get("status")}
        if "MISSING" in statuses:
            missing_dropped += 1
            continue
        if "UNDEFINED-OUTCOME" in statuses:
            undefined_scored += 1
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
        "undefinedOutcomeScored": undefined_scored,
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
    expected: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    del design  # cells/units come from the expected-behaviour table for H1/H2.
    table = expected if expected is not None else load_expected_behaviour()
    by_unit = expected_by_unit_id(table)
    eligible = eligible_unit_ids(table)

    def detect(row: Mapping[str, Any]) -> int:
        return m_detect_correct(row, by_unit[str(row["unitId"])])

    def localise(row: Mapping[str, Any]) -> int:
        return m_localise_correct(row, by_unit[str(row["unitId"])])

    h1 = paired_metric(
        rows,
        left_arm="CL-LOOP",
        right_arm="CL-T",
        metric=detect,
        eligible_units=eligible,
    )
    h2 = paired_metric(
        rows,
        left_arm="CL-LOOP",
        right_arm="CL-TA",
        metric=localise,
        eligible_units=eligible,
    )
    adjusted = holm_adjust([("H1", float(h1["p"])), ("H2", float(h2["p"]))])
    contrasts = {
        "H1": {
            **h1,
            "metric": "M-DETECT-CORRECT",
            "comparison": "CL-LOOP vs CL-T",
            "holmAdjustedP": adjusted["H1"],
            "supported": bool(adjusted["H1"] < FAMILYWISE_ALPHA and h1["b"] > h1["c"]),
        },
        "H2": {
            **h2,
            "metric": "M-LOCALISE-CORRECT",
            "comparison": "CL-LOOP vs CL-TA",
            "holmAdjustedP": adjusted["H2"],
            "supported": bool(adjusted["H2"] < FAMILYWISE_ALPHA and h2["b"] > h2["c"]),
        },
    }
    return {
        "label": "CONFIRMATORY / SIMULATED-IUT",
        "eligibleUnitCount": len(eligible),
        "nullExpectationUnitCount": null_expectation_count(table),
        "contrasts": contrasts,
        "holm": adjusted,
        "alpha": FAMILYWISE_ALPHA,
        "secondary": secondary_descriptive(rows),
    }


def write_analysis(
    *,
    rows: Sequence[Mapping[str, Any]],
    design: Mapping[str, Any],
    expected: Mapping[str, Any] | None = None,
    out_path: Path = OUT_PATH,
) -> dict[str, Any]:
    if out_path.exists():
        print(f"{out_path} already exists", file=sys.stderr)
        raise SystemExit(2)
    payload = analyze_rows(rows, design=design, expected=expected)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only confirmatory analysis.")
    parser.add_argument("--jsonl", type=Path, default=RAW_PATH)
    parser.add_argument("--design", type=Path, default=DESIGN_PATH)
    parser.add_argument("--out", type=Path, default=OUT_PATH)
    parser.add_argument("--registration", type=Path, default=REGISTRATION_PATH)
    args = parser.parse_args(argv)
    registration = load_json(args.registration)
    if registration.get("identity", {}).get("artifactId") != "CLTAV-CONFIRMATORY-REGISTRATION-V3":
        print("analysis requires confirmatory registration v3", file=sys.stderr)
        raise SystemExit(2)
    design = load_json(args.design)
    rows = load_jsonl(args.jsonl)
    payload = write_analysis(rows=rows, design=design, out_path=args.out)
    print(json.dumps({"written": str(args.out), "contrasts": list(payload["contrasts"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
