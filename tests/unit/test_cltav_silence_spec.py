"""R21-F02 specification witnesses: instance-paired silence, not a timeout engine."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "cltav_silence_spec", ROOT / "scripts/cltav_silence_spec.py"
)
assert SPEC and SPEC.loader
silence = importlib.util.module_from_spec(SPEC)
sys.modules["cltav_silence_spec"] = silence
SPEC.loader.exec_module(silence)

CRS = ROOT / "configs/requirements/arinc_615a3_m1_crs.json"
IDENTITY = ROOT / "docs/research/methodology/rr_2026_001_revision_identity.json"


def _ob(
    trigger: silence.Event,
    *,
    upper: float = 3.0,
    closed: bool = True,
    pairing: silence.PairingPolicy = silence.PairingPolicy.UNIQUE_KEY,
    concurrent: bool = False,
) -> silence.TimedObligation:
    return silence.TimedObligation(
        trigger,
        upper_bound=upper,
        upper_closed=closed,
        pairing=pairing,
        concurrent_same_key=concurrent,
    )


def test_wrong_key_response_does_not_suppress_unmatched_timeout() -> None:
    a = silence.Event(0, 0.0, silence.EventKind.TRIG, "A")
    b_resp = silence.Event(1, 1.0, silence.EventKind.RESP, "B")
    trace = (a, b_resp)
    obligation = _ob(a)
    assert silence.displayed_global_resp_no_response(obligation, trace, 4.0) is False
    assert silence.no_response(obligation, trace, 4.0) is True
    assert silence.t2_holds(obligation, trace) is False


def test_matching_response_discharges_instance() -> None:
    a = silence.Event(0, 0.0, silence.EventKind.TRIG, "A")
    resp = silence.Event(1, 1.0, silence.EventKind.RESP, "A")
    obligation = _ob(a)
    assert silence.no_response(obligation, (a, resp), 4.0) is False
    assert silence.instance_disposition(obligation, (a, resp), 4.0) is silence.Disposition.DISCHARGED
    assert silence.t2_holds(obligation, (a, resp)) is True


def test_equal_time_later_index_response_is_processed() -> None:
    trig = silence.Event(0, 1.0, silence.EventKind.TRIG, "A")
    resp = silence.Event(1, 1.0, silence.EventKind.RESP, "A")
    obligation = _ob(trig)
    assert silence.match_r(obligation, trig, resp, (trig,)) == "MATCH"
    assert silence.no_response(obligation, (trig, resp), 4.0) is False
    assert silence.displayed_global_resp_no_response(obligation, (trig, resp), 4.0) is False


def test_cancellation_does_not_produce_later_timeout() -> None:
    trig = silence.Event(0, 0.0, silence.EventKind.TRIG, "A")
    cancel = silence.Event(1, 1.0, silence.EventKind.CANCEL, "A")
    obligation = _ob(trig)
    assert silence.no_response(obligation, (trig, cancel), 4.0) is False
    assert silence.instance_disposition(obligation, (trig, cancel), 4.0) is silence.Disposition.CANCELLED


def test_supersession_does_not_timeout_the_old_instance() -> None:
    first = silence.Event(0, 0.0, silence.EventKind.TRIG, "A")
    second = silence.Event(1, 1.0, silence.EventKind.TRIG, "A")
    obligation = _ob(first)
    trace = (first, second)
    assert silence.instance_disposition(obligation, trace, 5.0) is silence.Disposition.SUPERSEDED
    assert silence.no_response(obligation, trace, 5.0) is False
    successor = _ob(second)
    assert silence.no_response(successor, trace, 5.0) is True


def test_ambiguous_unique_key_pairing_is_error_not_fail() -> None:
    first = silence.Event(0, 0.0, silence.EventKind.TRIG, "A")
    second = silence.Event(1, 0.5, silence.EventKind.TRIG, "A")
    resp = silence.Event(2, 1.0, silence.EventKind.RESP, "A")
    obligation = _ob(first, concurrent=True)
    trace = (first, second, resp)
    assert silence.no_response(obligation, trace, 4.0) is silence.Disposition.ERROR
    assert silence.no_response(_ob(second, concurrent=True), trace, 4.0) is silence.Disposition.ERROR


def test_closed_upper_bound_admits_response_exactly_at_deadline() -> None:
    trig = silence.Event(0, 0.0, silence.EventKind.TRIG, "A")
    obligation = _ob(trig, upper=3.0, closed=True)
    assert silence.no_response(obligation, (trig,), 3.0) is False
    assert silence.no_response(obligation, (trig,), 4.0) is True
    on_time = silence.Event(1, 3.0, silence.EventKind.RESP, "A")
    assert silence.t2_holds(obligation, (trig, on_time)) is True
    assert silence.no_response(obligation, (trig, on_time), 4.0) is False


def test_open_upper_bound_expires_at_deadline_and_keeps_find_constants() -> None:
    trig = silence.Event(0, 0.0, silence.EventKind.TRIG, "A")
    obligation = _ob(trig, upper=3.0, closed=False)
    assert silence.no_response(obligation, (trig,), 3.0) is True
    late = silence.Event(1, 3.0, silence.EventKind.RESP, "A")
    assert silence.t2_holds(obligation, (trig, late)) is False
    assert silence.no_response(obligation, (trig, late), 4.0) is False
    crs = json.loads(CRS.read_text(encoding="utf-8"))
    find = {
        row["id"]: row["timing"]
        for row in crs["requirements"]
        if row.get("timing", {}).get("timingFamily") in {
            "FIND-ANSWER-REGISTRATION-WINDOW",
            "FIND-HOST-ANSWER-DEADLINE",
        }
    }
    assert find["CRS-M1-00391"]["upperBound"] == 2
    assert find["CRS-M1-00520"]["upperBound"] == 3
    identity = json.loads(IDENTITY.read_text(encoding="utf-8"))
    freeze = identity["historicalFreeze"]
    assert freeze["displayMathBlocks"] == 94
    assert identity["successor"]["independentMathematicalApproval"] is False
    assert identity["successor"]["independentReviewApproval"] is False
    assert identity["successor"]["historicalMathCheckDoesNotProveSuccessorMath"] is True
