"""Synthetic-data tests for confirmatory runner/analysis.  No real cell is run."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runner = _load("run_cltav_confirmatory", ROOT / "scripts/run_cltav_confirmatory.py")
analyze = _load("analyze_cltav_confirmatory", ROOT / "scripts/analyze_cltav_confirmatory.py")


def test_mcnemar_zero_discordant_is_one() -> None:
    assert analyze.mcnemar_two_sided(0, 0) == 1.0


def test_mcnemar_five_versus_zero() -> None:
    assert analyze.mcnemar_two_sided(5, 0) == 0.0625


def test_mcnemar_ten_versus_two_matches_comb_sum() -> None:
    n = 12
    k = 2
    cdf = sum(math.comb(n, i) for i in range(k + 1)) / (2**n)
    assert analyze.mcnemar_two_sided(10, 2) == pytest.approx(min(1.0, 2 * cdf))


def test_holm_orders_and_multiplies() -> None:
    adjusted = analyze.holm_adjust([("H1", 0.04), ("H2", 0.01)])
    assert adjusted["H2"] == pytest.approx(0.02)
    assert adjusted["H1"] == pytest.approx(0.04)


def test_clopper_pearson_bounds() -> None:
    low_zero, _ = analyze.clopper_pearson(0, 10)
    _, high_all = analyze.clopper_pearson(10, 10)
    low, high = analyze.clopper_pearson(5, 10)
    assert low_zero == 0.0
    assert high_all == 1.0
    assert low == pytest.approx(0.187, abs=0.005)
    assert high == pytest.approx(0.813, abs=0.005)


def _row(
    unit_id: str,
    arm: str,
    *,
    truth: str,
    verdict: str,
    candidates: list[str],
    status: str = "OK",
    stop: str = "Stop-Singleton",
    rounds: int = 2,
) -> dict:
    return {
        "label": "CONFIRMATORY / SIMULATED-IUT",
        "cellId": f"{unit_id}/{arm}",
        "unitId": unit_id,
        "arm": arm,
        "truthParentHypothesis": truth,
        "verdict": verdict,
        "finalCandidateSet": candidates,
        "stopClass": stop,
        "roundsConsumed": rounds,
        "status": status,
    }


def test_metric_definitions_on_hand_built_rows() -> None:
    fail_true = _row("U-F", "CL-LOOP", truth="h_find_answer_late", verdict="FAIL", candidates=["h_find_answer_late"])
    miss = _row("U-F", "CL-T", truth="h_find_answer_late", verdict="INCONCLUSIVE", candidates=["h_normal", "h_find_answer_late"])
    assert analyze.m_detect(fail_true) == 1
    assert analyze.m_detect(miss) == 0
    assert analyze.m_localise(fail_true) == 1
    assert analyze.m_localise(miss) == 0
    with pytest.raises(ValueError):
        analyze.m_detect(_row("U-N", "CL-T", truth="h_normal", verdict="FAIL", candidates=["h_find_answer_late"]))


def test_missing_pair_is_excluded_from_contrast() -> None:
    rows = [
        _row("U1", "CL-LOOP", truth="h_find_answer_late", verdict="FAIL", candidates=["h_find_answer_late"]),
        _row("U1", "CL-T", truth="h_find_answer_late", verdict="PASS", candidates=["h_normal"], status="MISSING"),
        _row("U2", "CL-LOOP", truth="h_find_answer_late", verdict="FAIL", candidates=["h_find_answer_late"]),
        _row("U2", "CL-T", truth="h_find_answer_late", verdict="PASS", candidates=["h_normal"]),
    ]
    design = {"units": [{"unitId": "U1", "harderCaseId": None}, {"unitId": "U2", "harderCaseId": None}]}
    result = analyze.paired_metric(
        rows,
        left_arm="CL-LOOP",
        right_arm="CL-T",
        metric=analyze.m_detect,
        excluded_units=analyze.pre_run_excluded_units(design),
    )
    assert result["n"] == 1
    assert result["b"] == 1
    assert result["c"] == 0
    assert result["missingDropped"] == 1
    assert result["undefinedOutcomeDropped"] == 0


def test_e3_and_t3_reason_mapping_and_dropped_counts() -> None:
    rows = [
        _row("U-E3", "CL-LOOP", truth="h_find_answer_late", verdict="FAIL", candidates=["h_find_answer_late"]),
        _row("U-E3", "CL-T", truth="h_find_answer_late", verdict="PASS", candidates=["h_normal"]),
        _row("U-T3", "CL-LOOP", truth="h_find_answer_late", verdict="FAIL", candidates=["h_find_answer_late"]),
        _row("U-T3", "CL-T", truth="h_find_answer_late", verdict="PASS", candidates=["h_normal"]),
        _row("U-OK", "CL-LOOP", truth="h_find_answer_late", verdict="FAIL", candidates=["h_find_answer_late"]),
        _row("U-OK", "CL-T", truth="h_find_answer_late", verdict="PASS", candidates=["h_normal"]),
        _row("U-MISS", "CL-LOOP", truth="h_find_answer_late", verdict="FAIL", candidates=["h_find_answer_late"], status="MISSING"),
        _row("U-MISS", "CL-T", truth="h_find_answer_late", verdict="PASS", candidates=["h_normal"]),
        _row("U-UNDEF", "CL-LOOP", truth="h_find_answer_late", verdict="FAIL", candidates=["h_find_answer_late"], status="UNDEFINED-OUTCOME"),
        _row("U-UNDEF", "CL-T", truth="h_find_answer_late", verdict="PASS", candidates=["h_normal"]),
    ]
    design = {
        "units": [
            {"unitId": "U-E3", "harderCaseId": "HC-LATE-ABSENT-SHORT-WINDOW"},
            {"unitId": "U-T3", "harderCaseId": "HC-FIND-ENDPOINT"},
            {"unitId": "U-OK", "harderCaseId": None},
            {"unitId": "U-MISS", "harderCaseId": None},
            {"unitId": "U-UNDEF", "harderCaseId": None},
        ]
    }
    mapping = analyze.pre_run_excluded_units(design)
    assert mapping == {"U-E3": "E3", "U-T3": "T3"}
    assert analyze.pre_run_excluded_unit_counts(design) == {"E3": 1, "T3": 1}
    result = analyze.paired_metric(
        rows,
        left_arm="CL-LOOP",
        right_arm="CL-T",
        metric=analyze.m_detect,
        excluded_units=mapping,
    )
    assert result["n"] == 1
    assert result["b"] == 1
    assert result["missingDropped"] == 1
    assert result["undefinedOutcomeDropped"] == 1
    payload = analyze.analyze_rows(rows, design=design)
    assert payload["preRunExcludedUnitCounts"] == {"E3": 1, "T3": 1}
    assert payload["contrasts"]["H1"]["missingDropped"] == 1
    assert payload["contrasts"]["H1"]["undefinedOutcomeDropped"] == 1
    secondary = payload["secondary"]["CL-LOOP"]
    assert secondary["inconclusiveShare"]["denominator"] >= 3


def test_pre_run_excluded_units_remain_in_secondary() -> None:
    rows = [
        _row("U-E3", "CL-LOOP", truth="h_find_answer_late", verdict="INCONCLUSIVE", candidates=["h_normal", "h_find_answer_late"]),
        _row("U-E3", "CL-T", truth="h_find_answer_late", verdict="INCONCLUSIVE", candidates=["h_normal", "h_find_answer_late"]),
    ]
    design = {"units": [{"unitId": "U-E3", "harderCaseId": "HC-LATE-ABSENT-SHORT-WINDOW"}]}
    payload = analyze.analyze_rows(rows, design=design)
    assert payload["preRunExcludedUnitCounts"] == {"E3": 1, "T3": 0}
    assert payload["secondary"]["CL-LOOP"]["inconclusiveShare"] == {"numerator": 1, "denominator": 1}
    assert payload["contrasts"]["H1"]["n"] == 0


def test_dry_run_preflight_passes_with_monkeypatched_clean_tree(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(runner, "git_porcelain", lambda cwd=None: "")
    monkeypatch.setattr(runner, "RAW_PATH", tmp_path / "missing.jsonl")
    runner.run_preflight()
    assert runner.planned_cell_count() == 312
    code = runner.main(["--dry-run"])
    assert code == 0


def test_tampered_hash_fails_preflight(tmp_path) -> None:
    source = ROOT / "configs/research/cltav_confirmatory_registration_v1.json"
    payload = json.loads(source.read_text(encoding="utf-8"))
    first = payload["hashedFiles"][0]
    payload["configHashes"][first] = hashlib.sha256(b"tampered").hexdigest()
    copy_path = tmp_path / "registration.json"
    copy_path.write_text(json.dumps(payload), encoding="utf-8")
    errors = runner.preflight_errors(
        registration=payload,
        porcelain="",
        raw_path=tmp_path / "absent.jsonl",
    )
    assert any("hash mismatch" in item for item in errors)
    with pytest.raises(SystemExit) as caught:
        runner.run_preflight(
            registration=payload,
            porcelain="",
            raw_path=tmp_path / "absent.jsonl",
        )
    assert caught.value.code == 2
    original = json.loads(source.read_text(encoding="utf-8"))
    assert original["configHashes"][first] != payload["configHashes"][first]


def _synthetic_cell() -> dict[str, str]:
    return {
        "cellId": "SC-ABORT/H-NORMAL/DEFAULT/CL-T",
        "unitId": "SC-ABORT/H-NORMAL/DEFAULT",
        "sceneId": "SC-ABORT",
        "faultId": "H-NORMAL",
        "armId": "CL-T",
        "parameters": {},
    }


def test_undefined_detection_outcome_is_not_retried(monkeypatch) -> None:
    calls: list[int] = []

    def fake_live(**kwargs):
        calls.append(1)
        return {
            "attemptRow": None,
            "undefinedDetectionOutcome": "metric dictionary does not define PASS/FAIL",
            "runRecord": {
                "stopClass": "Stop-NoDistinguisher",
                "finalHypotheses": ["h_normal", "h_find_answer_late"],
                "traceRef": {"resourceRemaining": 6},
            },
        }

    monkeypatch.setattr(runner, "execute_live_attempt", fake_live)
    record = runner.execute_one_cell(
        _synthetic_cell(), remaining=8, git_sha="deadbeef", config_hashes={}
    )
    assert len(calls) == 1
    assert record["status"] == "UNDEFINED-OUTCOME"
    assert record["verdict"] is None
    assert record["undefinedDetectionOutcome"] == "metric dictionary does not define PASS/FAIL"
    assert record["stopClass"] == "Stop-NoDistinguisher"
    assert record["finalCandidateSet"] == ["h_normal", "h_find_answer_late"]
    assert record["roundsConsumed"] == 2


def test_infrastructure_exception_retries_once_then_missing(monkeypatch) -> None:
    calls: list[int] = []

    def fake_live(**kwargs):
        calls.append(1)
        raise RuntimeError("pipeline exploded")

    monkeypatch.setattr(runner, "execute_live_attempt", fake_live)
    record = runner.execute_one_cell(
        _synthetic_cell(), remaining=8, git_sha="deadbeef", config_hashes={}
    )
    assert len(calls) == 2
    assert record["status"] == "MISSING"
    assert record["verdict"] is None
