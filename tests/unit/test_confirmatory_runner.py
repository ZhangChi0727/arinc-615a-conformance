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
builder = _load(
    "build_confirmatory_expected_behaviour_v1",
    ROOT / "scripts/build_confirmatory_expected_behaviour_v1.py",
)


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


ENDPOINT_EXPECTED = {
    "unitId": "U-EP",
    "acceptableVerdicts": ["INCONCLUSIVE"],
    "candidateRule": {"kind": "equals", "set": ["h_find_answer_late", "h_normal"]},
}
SHORT_WINDOW_EXPECTED = {
    "unitId": "U-SW",
    "acceptableVerdicts": ["FAIL"],
    "candidateRule": {"kind": "equals", "set": ["h_find_answer_absent", "h_find_answer_late"]},
}
INVALID_OBS_EXPECTED = {
    "unitId": "U-INV",
    "acceptableVerdicts": ["ERROR", "INCONCLUSIVE", "NOT-ANSWERED"],
    "candidateRule": {"kind": "notSingletonFault"},
}
NORMAL_EXPECTED = {
    "unitId": "U-N",
    "acceptableVerdicts": ["INCONCLUSIVE", "PASS"],
    "candidateRule": {"kind": "contains", "member": "h_normal"},
}


def test_v2_metrics_on_endpoint_and_short_window_rows() -> None:
    endpoint_ok = _row(
        "U-EP",
        "CL-LOOP",
        truth="h_find_answer_late",
        verdict="INCONCLUSIVE",
        candidates=["h_normal", "h_find_answer_late"],
    )
    endpoint_fail = _row(
        "U-EP",
        "CL-T",
        truth="h_find_answer_late",
        verdict="FAIL",
        candidates=["h_find_answer_late"],
    )
    assert analyze.m_detect_correct(endpoint_ok, ENDPOINT_EXPECTED) == 1
    assert analyze.m_detect_correct(endpoint_fail, ENDPOINT_EXPECTED) == 0
    short_both = _row(
        "U-SW",
        "CL-LOOP",
        truth="h_find_answer_absent",
        verdict="FAIL",
        candidates=["h_find_answer_late", "h_find_answer_absent"],
    )
    short_singleton = _row(
        "U-SW",
        "CL-TA",
        truth="h_find_answer_absent",
        verdict="FAIL",
        candidates=["h_find_answer_absent"],
    )
    assert analyze.m_localise_correct(short_both, SHORT_WINDOW_EXPECTED) == 1
    assert analyze.m_localise_correct(short_singleton, SHORT_WINDOW_EXPECTED) == 0


def test_invalid_observation_class_scores_non_pass_fail() -> None:
    ok = _row("U-INV", "CL-LOOP", truth="", verdict="INCONCLUSIVE", candidates=["h_normal", "h_invalid"])
    fail = _row("U-INV", "CL-T", truth="", verdict="FAIL", candidates=["h_find_answer_late"])
    singleton = _row("U-INV", "CL-TA", truth="", verdict="ERROR", candidates=["h_find_answer_late"])
    assert analyze.m_detect_correct(ok, INVALID_OBS_EXPECTED) == 1
    assert analyze.m_detect_correct(fail, INVALID_OBS_EXPECTED) == 0
    assert analyze.m_localise_correct(ok, INVALID_OBS_EXPECTED) == 1
    assert analyze.m_localise_correct(singleton, INVALID_OBS_EXPECTED) == 0


def test_h_normal_units_accept_pass_or_inconclusive() -> None:
    passed = _row("U-N", "CL-LOOP", truth="h_normal", verdict="PASS", candidates=["h_normal"])
    mixed = _row("U-N", "CL-T", truth="h_normal", verdict="INCONCLUSIVE", candidates=["h_normal", "h_find_answer_late"])
    failed = _row("U-N", "CL-TA", truth="h_normal", verdict="FAIL", candidates=["h_find_answer_late"])
    assert analyze.m_detect_correct(passed, NORMAL_EXPECTED) == 1
    assert analyze.m_detect_correct(mixed, NORMAL_EXPECTED) == 1
    assert analyze.m_detect_correct(failed, NORMAL_EXPECTED) == 0
    assert analyze.m_localise_correct(passed, NORMAL_EXPECTED) == 1
    assert analyze.m_localise_correct(mixed, NORMAL_EXPECTED) == 1
    assert analyze.m_localise_correct(failed, NORMAL_EXPECTED) == 0


def test_undefined_outcome_is_scored_not_dropped() -> None:
    ordinary = {
        "unitId": "U3",
        "acceptableVerdicts": ["FAIL"],
        "candidateRule": {"kind": "equals", "set": ["h_find_answer_late"]},
    }
    invalid = dict(INVALID_OBS_EXPECTED)
    undef_ordinary = _row(
        "U3",
        "CL-LOOP",
        truth="h_find_answer_late",
        verdict="FAIL",
        candidates=["h_find_answer_late"],
        status="UNDEFINED-OUTCOME",
    )
    undef_invalid = _row(
        "U-INV",
        "CL-LOOP",
        truth="",
        verdict="FAIL",
        candidates=["h_normal", "h_find_answer_late"],
        status="UNDEFINED-OUTCOME",
    )
    assert analyze.m_detect_correct(undef_ordinary, ordinary) == 0
    assert analyze.m_detect_correct(undef_invalid, invalid) == 1
    assert analyze.m_localise_correct(undef_ordinary, ordinary) == 1
    from_run_record = {
        "unitId": "U3",
        "arm": "CL-TA",
        "status": "UNDEFINED-OUTCOME",
        "verdict": None,
        "finalCandidateSet": [],
        "runRecord": {
            "stopClass": "Stop-NoDistinguisher",
            "finalHypotheses": ["h_find_answer_late"],
        },
    }
    assert analyze.m_localise_correct(from_run_record, ordinary) == 1
    rows = [
        _row("U1", "CL-LOOP", truth="h_find_answer_late", verdict="FAIL", candidates=["h_find_answer_late"]),
        _row("U1", "CL-T", truth="h_find_answer_late", verdict="PASS", candidates=["h_normal"], status="MISSING"),
        _row("U2", "CL-LOOP", truth="h_find_answer_late", verdict="FAIL", candidates=["h_find_answer_late"]),
        _row("U2", "CL-T", truth="h_find_answer_late", verdict="PASS", candidates=["h_normal"]),
        undef_ordinary,
        _row("U3", "CL-T", truth="h_find_answer_late", verdict="PASS", candidates=["h_normal"]),
    ]
    expected = {
        "units": [
            {"unitId": "U1", "acceptableVerdicts": ["FAIL"], "candidateRule": {"kind": "equals", "set": ["h_find_answer_late"]}},
            {"unitId": "U2", "acceptableVerdicts": ["FAIL"], "candidateRule": {"kind": "equals", "set": ["h_find_answer_late"]}},
            ordinary,
        ],
        "needsDmRuling": [],
    }
    payload = analyze.analyze_rows(rows, design={"units": []}, expected=expected)
    assert payload["contrasts"]["H1"]["missingDropped"] == 1
    assert payload["contrasts"]["H1"]["undefinedOutcomeScored"] == 1
    assert payload["contrasts"]["H1"]["n"] == 2


def test_missing_pair_is_dropped_from_contrast() -> None:
    rows = [
        _row("U1", "CL-LOOP", truth="h_find_answer_late", verdict="FAIL", candidates=["h_find_answer_late"]),
        _row("U1", "CL-T", truth="h_find_answer_late", verdict="PASS", candidates=["h_normal"], status="MISSING"),
        _row("U2", "CL-LOOP", truth="h_find_answer_late", verdict="FAIL", candidates=["h_find_answer_late"]),
        _row("U2", "CL-T", truth="h_find_answer_late", verdict="PASS", candidates=["h_normal"]),
    ]
    expected = {
        "units": [
            {"unitId": "U1", "acceptableVerdicts": ["FAIL"], "candidateRule": {"kind": "equals", "set": ["h_find_answer_late"]}},
            {"unitId": "U2", "acceptableVerdicts": ["FAIL"], "candidateRule": {"kind": "equals", "set": ["h_find_answer_late"]}},
        ]
    }
    payload = analyze.analyze_rows(rows, design={"units": []}, expected=expected)
    assert payload["contrasts"]["H1"]["n"] == 1
    assert payload["contrasts"]["H1"]["b"] == 1
    assert payload["contrasts"]["H1"]["missingDropped"] == 1
    assert payload["contrasts"]["H1"]["undefinedOutcomeScored"] == 0
    assert payload["eligibleUnitCount"] == 2


def test_endpoint_and_short_window_units_are_eligible() -> None:
    rows = [
        _row(
            "U-EP",
            "CL-LOOP",
            truth="h_find_answer_late",
            verdict="INCONCLUSIVE",
            candidates=["h_normal", "h_find_answer_late"],
        ),
        _row(
            "U-EP",
            "CL-T",
            truth="h_find_answer_late",
            verdict="FAIL",
            candidates=["h_find_answer_late"],
        ),
        _row(
            "U-SW",
            "CL-LOOP",
            truth="h_find_answer_absent",
            verdict="FAIL",
            candidates=["h_find_answer_absent", "h_find_answer_late"],
        ),
        _row(
            "U-SW",
            "CL-TA",
            truth="h_find_answer_absent",
            verdict="FAIL",
            candidates=["h_find_answer_absent"],
        ),
    ]
    expected = {"units": [ENDPOINT_EXPECTED, SHORT_WINDOW_EXPECTED], "needsDmRuling": []}
    payload = analyze.analyze_rows(rows, design={"units": []}, expected=expected)
    assert payload["eligibleUnitCount"] == 2
    assert payload["nullExpectationUnitCount"] == 0
    assert payload["contrasts"]["H1"]["n"] == 1
    assert payload["contrasts"]["H2"]["n"] == 1
    assert payload["secondary"]["CL-LOOP"]["inconclusiveShare"]["denominator"] == 2


def test_expected_behaviour_table_is_reproducible() -> None:
    committed = json.loads(
        (ROOT / "configs/research/cltav_confirmatory_expected_behaviour_v1.json").read_text(encoding="utf-8")
    )
    rebuilt = builder.build_expected_behaviour()
    assert rebuilt == committed
    assert len(committed["units"]) == 78
    assert committed["needsDmRuling"] == []
    assert "secondaryOnlyUnits" not in committed


def test_dry_run_preflight_passes_with_monkeypatched_clean_tree(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(runner, "git_porcelain", lambda cwd=None: "")
    monkeypatch.setattr(runner, "RAW_PATH", tmp_path / "missing.jsonl")
    runner.run_preflight()
    assert runner.planned_cell_count() == 312
    code = runner.main(["--dry-run"])
    assert code == 0


def test_tampered_hash_fails_preflight(tmp_path) -> None:
    source = ROOT / "configs/research/cltav_confirmatory_registration_v2.json"
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
    assert record["runRecord"]["stopClass"] == "Stop-NoDistinguisher"
    assert record["runRecord"]["finalHypotheses"] == ["h_normal", "h_find_answer_late"]
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
