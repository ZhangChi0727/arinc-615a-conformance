"""Build the pre-registered expected-behaviour table from the design draft."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from a615a_sim.algorithm.hypothesis_model import map_to_parent_hypotheses  # noqa: E402
from a615a_sim.faults.catalogue import entry_by_id, harder_cases  # noqa: E402

DESIGN_PATH = ROOT / "configs/research/cltav_confirmatory_design_draft_v1.json"
OUT_PATH = ROOT / "configs/research/cltav_confirmatory_expected_behaviour_v1.json"
NORMAL_PARENTS = frozenset({"h_normal", "h-normal"})


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _harder_by_id() -> dict[str, Mapping[str, Any]]:
    return {str(case["id"]): case for case in harder_cases()}


def truth_parent_of_fault(fault_id: str) -> str | None:
    entry = entry_by_id(fault_id)
    raw = entry.get("hypothesisId")
    if raw is None or raw == "":
        return None
    mapped = map_to_parent_hypotheses([str(raw)])
    return mapped[0] if mapped else str(raw)


def _secondary_reason(unit: Mapping[str, Any]) -> str:
    harder = unit.get("harderCaseId")
    params = unit.get("parameters") or {}
    if harder == "HC-NORMAL-NEAR-BOUNDARY" or "AX-FIND-NORMAL-NEAR-BOUNDARY" in (unit.get("axisIds") or []):
        return "near-boundary normal; truth parent h_normal"
    if "lurAckAtS" in params or "AX-LUR-ACK-TICK" in (unit.get("axisIds") or []):
        return "LUR-ACK perturbation; truth parent h_normal"
    return "H-NORMAL; truth parent h_normal"


def _late_and_absent_parents(case: Mapping[str, Any]) -> tuple[str, str] | None:
    identifiers = [case.get("parentFaultId"), case.get("pairWith")]
    late = None
    absent = None
    for identifier in identifiers:
        if not identifier:
            continue
        text = str(identifier).upper()
        parent = truth_parent_of_fault(str(identifier))
        if parent is None:
            continue
        if "LATE" in text:
            late = parent
        if "ABSENT" in text or "MISSING" in text:
            absent = parent
    if late and absent and late != absent:
        return late, absent
    return None


def classify_unit(
    unit: Mapping[str, Any],
    *,
    cases: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    fault_id = str(unit["faultId"])
    truth_parent = truth_parent_of_fault(fault_id)
    harder = unit.get("harderCaseId")
    base = {
        "unitId": unit["unitId"],
        "sceneId": unit["sceneId"],
        "faultId": fault_id,
        "harderCaseId": harder,
        "truthParent": truth_parent,
    }
    if truth_parent in NORMAL_PARENTS:
        return {
            "kind": "secondary",
            "reason": _secondary_reason(unit),
            **base,
        }
    if harder == "HC-FIND-ENDPOINT":
        late_fault = (cases.get(str(harder)) or {}).get("parentFaultId") or "F-FIND-ANSWER-LATE"
        late_parent = truth_parent_of_fault(str(late_fault)) or "h_find_answer_late"
        expected_set = sorted(["h_normal", late_parent])
        return {
            "kind": "entry",
            **base,
            "expectedVerdict": "INCONCLUSIVE",
            "expectedCandidateSet": expected_set,
            "rule": "C1 overlap",
        }
    if harder == "HC-LATE-ABSENT-SHORT-WINDOW":
        pair = _late_and_absent_parents(cases.get(str(harder)) or {})
        if pair is None:
            return {
                "kind": "needsDmRuling",
                **base,
                "expectedVerdict": None,
                "expectedCandidateSet": None,
                "rule": None,
                "detail": "could not identify LATE and ABSENT parents from harderCases text",
            }
        late_parent, absent_parent = pair
        return {
            "kind": "entry",
            **base,
            "expectedVerdict": "FAIL",
            "expectedCandidateSet": sorted([late_parent, absent_parent]),
            "rule": "short-window LATE vs ABSENT",
        }
    if harder == "HC-INVALID-OBS-JITTER":
        return {
            "kind": "needsDmRuling",
            **base,
            "expectedVerdict": None,
            "expectedCandidateSet": None,
            "rule": None,
            "detail": "HC-INVALID-OBS-JITTER: evaluator construction; do not guess expected verdict or set",
        }
    if truth_parent is None:
        return {
            "kind": "needsDmRuling",
            **base,
            "expectedVerdict": None,
            "expectedCandidateSet": None,
            "rule": None,
            "detail": "fault has no catalogue hypothesisId; cannot form expectedCandidateSet",
        }
    return {
        "kind": "entry",
        **base,
        "expectedVerdict": "FAIL",
        "expectedCandidateSet": [truth_parent],
        "rule": "ordinary",
    }


def build_expected_behaviour(
    design: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    payload = dict(design) if design is not None else load_json(DESIGN_PATH)
    cases = _harder_by_id()
    entries: list[dict[str, Any]] = []
    secondary: list[dict[str, Any]] = []
    needs: list[dict[str, Any]] = []
    flagged: list[str] = []
    for unit in payload.get("units") or []:
        classified = classify_unit(unit, cases=cases)
        if classified.get("harderCaseId") == "HC-OBS-PERTURB-EPS":
            flagged.append(str(unit["unitId"]))
        kind = classified.pop("kind")
        if kind == "secondary":
            secondary.append(
                {
                    "unitId": classified["unitId"],
                    "sceneId": classified["sceneId"],
                    "faultId": classified["faultId"],
                    "harderCaseId": classified["harderCaseId"],
                    "reason": classified["reason"],
                }
            )
            continue
        if kind == "needsDmRuling":
            needs.append(classified)
            continue
        entries.append(
            {
                "unitId": classified["unitId"],
                "sceneId": classified["sceneId"],
                "faultId": classified["faultId"],
                "harderCaseId": classified["harderCaseId"],
                "truthParent": classified["truthParent"],
                "expectedVerdict": classified["expectedVerdict"],
                "expectedCandidateSet": classified["expectedCandidateSet"],
                "rule": classified["rule"],
            }
        )
    entries.sort(key=lambda item: item["unitId"])
    secondary.sort(key=lambda item: item["unitId"])
    needs.sort(key=lambda item: item["unitId"])
    flagged.sort()
    return {
        "identity": {
            "artifactId": "CLTAV-CONFIRMATORY-EXPECTED-BEHAVIOUR-V1",
            "authority": "CR-2026-032 / DD-056",
            "label": "CONFIRMATORY / SIMULATED-IUT / PRE-REGISTERED-EXPECTED-BEHAVIOUR",
        },
        "units": entries,
        "secondaryOnlyUnits": secondary,
        "needsDmRuling": needs,
        "flaggedForDmReview": flagged,
    }


def rule_counts(payload: Mapping[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for entry in payload.get("units") or []:
        rule = str(entry.get("rule") or "null")
        counts[rule] = counts.get(rule, 0) + 1
    return counts


def write_expected_behaviour(path: Path = OUT_PATH) -> dict[str, Any]:
    payload = build_expected_behaviour()
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


def summary_text(payload: Mapping[str, Any]) -> str:
    lines = [
        "countsPerRule=" + json.dumps(rule_counts(payload), ensure_ascii=False, sort_keys=True),
        "needsDmRuling=" + json.dumps(payload.get("needsDmRuling") or [], ensure_ascii=False, indent=2),
        "flaggedForDmReview=" + json.dumps(payload.get("flaggedForDmReview") or [], ensure_ascii=False, indent=2),
        "hardCaseRows=",
    ]
    hard = [
        entry
        for entry in payload.get("units") or []
        if entry.get("harderCaseId") in {"HC-FIND-ENDPOINT", "HC-LATE-ABSENT-SHORT-WINDOW"}
    ]
    hard.extend(
        item
        for item in (payload.get("needsDmRuling") or [])
        if item.get("harderCaseId") in {"HC-FIND-ENDPOINT", "HC-LATE-ABSENT-SHORT-WINDOW"}
    )
    hard.sort(key=lambda item: item["unitId"])
    lines.append(json.dumps(hard, ensure_ascii=False, indent=2))
    return "\n".join(lines) + "\n"


def main() -> int:
    payload = write_expected_behaviour()
    print(summary_text(payload), end="")
    print("written", OUT_PATH.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
