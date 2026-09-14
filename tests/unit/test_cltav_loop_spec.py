"""Bounded walk-throughs for first-version CL-TAV admission, ERROR and stops."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("cltav_loop_spec", ROOT / "scripts/cltav_loop_spec.py")
assert SPEC and SPEC.loader
loop = importlib.util.module_from_spec(SPEC)
sys.modules["cltav_loop_spec"] = loop
SPEC.loader.exec_module(loop)


def _hyps(*names: str) -> set[str]:
    return set(names)


def test_affordable_suboptimal_is_admitted_instead_of_stop_budget() -> None:
    library = [
        loop.Action("t_best", loop.ActionKind.TEST, 2.0, frozenset({"q0"}), worst_remaining=1, next_q="q0"),
        loop.Action("t_alt", loop.ActionKind.TEST, 1.0, frozenset({"q0"}), worst_remaining=2, next_q="q0"),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1.0, Hk=_hyps("h1", "h2", "h3"), q="q0",
        B=1.0, remaining_B=1.0,
    )
    chosen = loop.step(session, library, observation=_hyps("h1", "h2"))
    assert chosen is not None and chosen.id == "t_alt"
    assert session.charges == [("t_alt", 1.0)]


def test_test_that_exhausts_budget_cannot_be_followed_by_prep() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1.0, frozenset({"q0"}), worst_remaining=2, next_q="q1"),
        loop.Action("prep", loop.ActionKind.PREP, 1.0, frozenset({"q1"}), next_q="q2"),
        loop.Action("t2", loop.ActionKind.TEST, 1.0, frozenset({"q2"}), worst_remaining=1, next_q="q2"),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1.0, Hk=_hyps("h1", "h2", "h3"), q="q0",
        B=1.0, remaining_B=1.0,
    )
    loop.step(session, library, observation=_hyps("h1", "h2"))
    assert session.stop == "Stop-Budget"
    assert loop.step(session, library, observation=_hyps("h1")) is None
    assert all(item[0] != "prep" for item in session.charges)


def test_kmax_blocks_prep_after_last_round() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1.0, frozenset({"q0"}), worst_remaining=2, next_q="q1"),
        loop.Action("prep", loop.ActionKind.PREP, 1.0, frozenset({"q1"}), next_q="q2"),
    ]
    session = loop.Session(
        loop.ResourceMode.ROUNDS, cmin=1.0, Hk=_hyps("h1", "h2", "h3"), q="q0",
        Kmax=1,
    )
    loop.step(session, library, observation=_hyps("h1", "h2"))
    assert session.stop == "Stop-Budget"
    assert loop.step(session, library, observation=_hyps("h1")) is None


def test_initial_library_with_only_prep_is_admitted() -> None:
    library = [
        loop.Action("prep", loop.ActionKind.PREP, 1.0, frozenset({"q0"}), next_q="q1"),
        loop.Action("t1", loop.ActionKind.TEST, 1.0, frozenset({"q1"}), worst_remaining=1, next_q="q1"),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1.0, Hk=_hyps("h1", "h2"), q="q0",
        B=2.0, remaining_B=2.0,
    )
    chosen = loop.step(session, library, observation=_hyps("h1", "h2"))
    assert chosen is not None and chosen.id == "prep"
    assert session.q == "q1"
    assert session.stop is None


def test_budget_mode_does_not_use_round_or() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1.0, frozenset({"q0"}), worst_remaining=1, next_q="q0"),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1.0, Hk=_hyps("h1", "h2"), q="q0",
        B=0.0, remaining_B=0.0,
    )
    assert loop.step(session, library, observation=_hyps("h1")) is None
    assert session.stop == "Stop-Budget"
    assert session.charges == []


def test_rounds_mode_does_not_use_leftover_budget() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1.0, frozenset({"q0"}), worst_remaining=1, next_q="q0"),
    ]
    session = loop.Session(
        loop.ResourceMode.ROUNDS, cmin=1.0, Hk=_hyps("h1", "h2"), q="q0",
        Kmax=0,
    )
    assert loop.step(session, library, observation=_hyps("h1")) is None
    assert session.stop == "Stop-Budget"


def test_confirmed_not_sent_keeps_q_and_unknown_effect_does_not() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1.0, frozenset({"q0"}), worst_remaining=1, next_q="q1"),
        loop.Action("recover", loop.ActionKind.RECOVER, 1.0, frozenset({"q0"}), next_q="q0"),
    ]
    sent = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1.0, Hk=_hyps("h1", "h2"), q="q0",
        B=4.0, remaining_B=4.0, retry_cap=3,
    )
    loop.step(sent, library, error=loop.ErrorKind.NOT_SENT)
    assert sent.q_status is loop.QStatus.KNOWN
    assert sent.q == "q0"
    assert sent.stop is None
    unknown = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1.0, Hk=_hyps("h1", "h2"), q="q0",
        B=4.0, remaining_B=4.0, retry_cap=3,
    )
    loop.step(unknown, library, error=loop.ErrorKind.UNKNOWN_EFFECT)
    assert unknown.q_status is loop.QStatus.UNKNOWN
    assert unknown.Hk == _hyps("h1", "h2")
    chosen = loop.step(unknown, library, observation=_hyps("h1", "h2"))
    assert chosen is not None and chosen.kind is loop.ActionKind.RECOVER


def test_retry_cap_stops_while_budget_remains() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1.0, frozenset({"q0"}), worst_remaining=1, next_q="q0"),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1.0, Hk=_hyps("h1", "h2"), q="q0",
        B=10.0, remaining_B=10.0, retry_cap=1,
    )
    loop.step(session, library, error=loop.ErrorKind.NOT_SENT)
    assert session.stop == "Stop-Error"
    assert session.remaining_B == 9.0
    assert loop.step(session, library, observation=_hyps("h1")) is None


def test_recover_error_uses_same_gate_and_not_sent_keeps_unknown() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1.0, frozenset({"q0"}), worst_remaining=1, next_q="q1"),
        loop.Action("recover", loop.ActionKind.RECOVER, 1.0, frozenset({"q0"}), next_q="q0"),
    ]
    unknown = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1.0, Hk=_hyps("h1", "h2"), q="q0",
        B=10.0, remaining_B=10.0, retry_cap=3,
    )
    loop.step(unknown, library, error=loop.ErrorKind.UNKNOWN_EFFECT)
    assert unknown.q_status is loop.QStatus.UNKNOWN
    loop.step(unknown, library, error=loop.ErrorKind.NOT_SENT)
    assert unknown.q_status is loop.QStatus.UNKNOWN
    assert unknown.charges[-1][0] == "recover"
    assert unknown.stop is None
    capped = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1.0, Hk=_hyps("h1", "h2"), q="q0",
        B=10.0, remaining_B=10.0, retry_cap=2,
    )
    loop.step(capped, library, error=loop.ErrorKind.UNKNOWN_EFFECT)
    loop.step(capped, library, error=loop.ErrorKind.UNKNOWN_EFFECT)
    assert capped.stop == "Stop-Error"
    assert capped.remaining_B == 8.0
    assert [item[0] for item in capped.charges] == ["t1", "recover"]
