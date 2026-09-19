"""Bounded walk-throughs for first-version CL-TAV admission, ERROR and stops."""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

import pytest

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
        loop.Action("t_best", loop.ActionKind.TEST, 2, frozenset({"q0"}), worst_remaining=1, next_q="q0"),
        loop.Action("t_alt", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=2, next_q="q0"),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2", "h3"), q="q0",
        B=1, remaining_B=1,
    )
    chosen = loop.step(session, library, observation=_hyps("h1", "h2"))
    assert chosen is not None and chosen.id == "t_alt"
    assert session.charges == [("t_alt", 1)]


def test_test_that_exhausts_budget_cannot_be_followed_by_prep() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=2, next_q="q1"),
        loop.Action("prep", loop.ActionKind.PREP, 1, frozenset({"q1"}), next_q="q2"),
        loop.Action("t2", loop.ActionKind.TEST, 1, frozenset({"q2"}), worst_remaining=1, next_q="q2"),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2", "h3"), q="q0",
        B=1, remaining_B=1,
    )
    loop.step(session, library, observation=_hyps("h1", "h2"))
    assert session.stop == "Stop-Budget"
    assert loop.step(session, library, observation=_hyps("h1")) is None
    assert all(item[0] != "prep" for item in session.charges)


def test_kmax_blocks_prep_after_last_round() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=2, next_q="q1"),
        loop.Action("prep", loop.ActionKind.PREP, 1, frozenset({"q1"}), next_q="q2"),
    ]
    session = loop.Session(
        loop.ResourceMode.ROUNDS, cmin=1, Hk=_hyps("h1", "h2", "h3"), q="q0",
        Kmax=1,
    )
    loop.step(session, library, observation=_hyps("h1", "h2"))
    assert session.stop == "Stop-Budget"
    assert loop.step(session, library, observation=_hyps("h1")) is None


def test_initial_library_with_only_prep_is_admitted() -> None:
    library = [
        loop.Action("prep", loop.ActionKind.PREP, 1, frozenset({"q0"}), next_q="q1"),
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q1"}), worst_remaining=1, next_q="q1"),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=2, remaining_B=2,
    )
    chosen = loop.step(session, library, observation=_hyps("h1", "h2"))
    assert chosen is not None and chosen.id == "prep"
    assert session.q == "q1"
    assert session.stop is None


def test_budget_mode_does_not_use_round_or() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q0"),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=0, remaining_B=0,
    )
    assert loop.step(session, library, observation=_hyps("h1")) is None
    assert session.stop == "Stop-Budget"
    assert session.charges == []


def test_rounds_mode_does_not_use_leftover_budget() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q0"),
    ]
    session = loop.Session(
        loop.ResourceMode.ROUNDS, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        Kmax=0,
    )
    assert loop.step(session, library, observation=_hyps("h1")) is None
    assert session.stop == "Stop-Budget"


def test_uninformative_test_does_not_block_prep() -> None:
    library = [
        loop.Action(
            "uninformative",
            loop.ActionKind.TEST,
            1,
            frozenset({"q0"}),
            worst_remaining=2,
            next_q="q0",
            obs_classes=(frozenset({"h1", "h2"}),),
        ),
        loop.Action("prep", loop.ActionKind.PREP, 1, frozenset({"q0"}), next_q="q1"),
        loop.Action(
            "split",
            loop.ActionKind.TEST,
            1,
            frozenset({"q1"}),
            worst_remaining=1,
            next_q="q1",
            obs_classes=(frozenset({"h1"}), frozenset({"h2"})),
        ),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=3, remaining_B=3,
    )
    first = loop.step(session, library, observation=_hyps("h1", "h2"))
    assert first is not None and first.id == "prep"
    assert session.q == "q1"
    second = loop.step(session, library, observation=_hyps("h1"))
    assert second is not None and second.id == "split"
    assert session.stop == "Stop-Singleton"
    assert [item[0] for item in session.charges] == ["prep", "split"]


def test_overlapping_observation_is_still_distinguishing_valuable() -> None:
    overlapping = loop.Action(
        "overlap",
        loop.ActionKind.TEST,
        1,
        frozenset({"q0"}),
        worst_remaining=2,
        next_q="q0",
        obs_classes=(frozenset({"h1", "h2"}), frozenset({"h1"}), frozenset({"h2"})),
    )
    library = [
        overlapping,
        loop.Action("prep", loop.ActionKind.PREP, 1, frozenset({"q0"}), next_q="q1"),
    ]
    hk = _hyps("h1", "h2")
    assert loop.can_strictly_reduce(overlapping, hk)
    assert loop.worst_remaining_count(overlapping, hk) == 2
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=hk, q="q0",
        B=3, remaining_B=3,
    )
    chosen = loop.step(session, library, observation=_hyps("h1", "h2"))
    assert chosen is not None and chosen.id == "overlap"
    assert session.stop is None
    assert session.charges[0][0] != "prep"


def test_valuable_but_unaffordable_is_stop_budget() -> None:
    library = [
        loop.Action("costly", loop.ActionKind.TEST, 2, frozenset({"q0"}), worst_remaining=1, next_q="q0"),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=1, remaining_B=1,
    )
    assert loop.step(session, library, observation=_hyps("h1")) is None
    assert session.stop == "Stop-Budget"
    assert session.charges == []


def test_no_strictly_reducing_test_and_no_prep_is_stop_nodistinguisher() -> None:
    library = [
        loop.Action(
            "uninformative",
            loop.ActionKind.TEST,
            1,
            frozenset({"q0"}),
            worst_remaining=2,
            next_q="q0",
            obs_classes=(frozenset({"h1", "h2"}),),
        ),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=3, remaining_B=3,
    )
    assert loop.step(session, library, observation=_hyps("h1", "h2")) is None
    assert session.stop == "Stop-NoDistinguisher"
    assert session.charges == []


def test_confirmed_not_sent_keeps_q_and_unknown_effect_does_not() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q1"),
        loop.Action(
            "recover",
            loop.ActionKind.RECOVER,
            1,
            frozenset({"unreachable"}),
            next_q="q_sync",
            recover_when_unknown=True,
        ),
    ]
    sent = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=4, remaining_B=4, retry_cap=3,
    )
    loop.step(sent, library, error=loop.ErrorKind.NOT_SENT)
    assert sent.q_status is loop.QStatus.KNOWN
    assert sent.q == "q0"
    assert sent.stop is None
    unknown = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=4, remaining_B=4, retry_cap=3,
    )
    loop.step(unknown, library, error=loop.ErrorKind.UNKNOWN_EFFECT)
    assert unknown.q_status is loop.QStatus.UNKNOWN
    assert unknown.Hk == _hyps("h1", "h2")
    chosen = loop.step(unknown, library, confirmed_q="q_sync")
    assert chosen is not None and chosen.kind is loop.ActionKind.RECOVER
    assert unknown.q == "q_sync"
    assert unknown.q_status is loop.QStatus.KNOWN


def test_retry_cap_stops_while_budget_remains() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q0"),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=10, remaining_B=10, retry_cap=1,
    )
    loop.step(session, library, error=loop.ErrorKind.NOT_SENT)
    assert session.stop == "Stop-Error"
    assert session.remaining_B == 9
    assert loop.step(session, library, observation=_hyps("h1")) is None


def test_ineligible_recover_is_not_admitted_or_charged() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q1"),
        loop.Action("recover", loop.ActionKind.RECOVER, 1, frozenset({"unreachable"})),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=10, remaining_B=10, retry_cap=3,
    )
    loop.step(session, library, error=loop.ErrorKind.UNKNOWN_EFFECT)
    assert session.q_status is loop.QStatus.UNKNOWN
    assert loop.step(session, library, observation=_hyps("h1", "h2")) is None
    assert session.stop == "Stop-Error"
    assert [item[0] for item in session.charges] == ["t1"]


def test_recover_without_confirmation_does_not_restore_old_q() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q1"),
        loop.Action(
            "recover",
            loop.ActionKind.RECOVER,
            1,
            frozenset({"unreachable"}),
            next_q="q_sync",
            recover_when_unknown=True,
        ),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=10, remaining_B=10, retry_cap=3,
    )
    loop.step(session, library, error=loop.ErrorKind.UNKNOWN_EFFECT)
    chosen = loop.step(session, library, observation=_hyps("h1", "h2"))
    assert chosen is not None and chosen.id == "recover"
    assert session.q_status is loop.QStatus.UNKNOWN
    assert session.q == "q0"
    assert session.Hk == _hyps("h1", "h2")


def test_recover_error_uses_same_gate_and_not_sent_keeps_unknown() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q1"),
        loop.Action(
            "recover",
            loop.ActionKind.RECOVER,
            1,
            frozenset({"unreachable"}),
            next_q="q_sync",
            recover_when_unknown=True,
        ),
    ]
    unknown = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=10, remaining_B=10, retry_cap=3,
    )
    loop.step(unknown, library, error=loop.ErrorKind.UNKNOWN_EFFECT)
    assert unknown.q_status is loop.QStatus.UNKNOWN
    loop.step(unknown, library, error=loop.ErrorKind.NOT_SENT)
    assert unknown.q_status is loop.QStatus.UNKNOWN
    assert unknown.charges[-1][0] == "recover"
    assert unknown.stop is None
    capped = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=10, remaining_B=10, retry_cap=2,
    )
    loop.step(capped, library, error=loop.ErrorKind.UNKNOWN_EFFECT)
    loop.step(capped, library, error=loop.ErrorKind.UNKNOWN_EFFECT)
    assert capped.stop == "Stop-Error"
    assert capped.remaining_B == 8
    assert [item[0] for item in capped.charges] == ["t1", "recover"]


def test_not_sent_without_recover_retries_when_cap_remains() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q0"),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=10, remaining_B=10, retry_cap=3,
    )
    loop.step(session, library, error=loop.ErrorKind.NOT_SENT)
    assert session.stop is None
    assert session.q_status is loop.QStatus.KNOWN
    chosen = loop.step(session, library, observation=_hyps("h1"))
    assert chosen is not None and chosen.id == "t1"


def test_singleton_on_last_round_beats_stop_budget() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q0"),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=1, remaining_B=1,
    )
    loop.step(session, library, observation=_hyps("h1"))
    assert session.stop == "Stop-Singleton"
    assert session.remaining_B == 0


def test_empty_on_last_round_beats_stop_budget() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q0"),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=1, remaining_B=1,
    )
    loop.step(session, library, observation=set())
    assert session.stop == "Stop-Empty"


def test_equivalent_with_resource_remaining_is_stop_equivalent() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q0"),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=5, remaining_B=5,
    )
    loop.step(session, library, observation=_hyps("h1", "h2"), equivalent=True)
    assert session.stop == "Stop-Equivalent"
    assert session.remaining_B == 4


def test_named_645_beats_continue() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q0"),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=5, remaining_B=5,
    )
    loop.step(session, library, observation=_hyps("h1", "h2"), named_645=True)
    assert session.stop == "Stop-645"


def test_update_stop_priority_table_matches_figures() -> None:
    assert loop.UPDATE_STOP_PRIORITY == (
        "Stop-Empty",
        "Stop-Singleton",
        "Stop-645",
        "Stop-Equivalent",
        "Stop-Budget",
    )
    assert set(loop.ADMIT_SELECT_TABLE) == {"A1", "A2", "A3", "A4", "A5"}


def test_excluded_hypothesis_class_is_not_distinguishing_value() -> None:
    test = loop.Action(
        "t",
        loop.ActionKind.TEST,
        1,
        frozenset({"q0"}),
        next_q="q0",
        obs_classes=(frozenset({"h1", "h2"}), frozenset({"h3"})),
    )
    prep = loop.Action("prep", loop.ActionKind.PREP, 1, frozenset({"q0"}), next_q="q1")
    hk = _hyps("h1", "h2")
    assert loop.current_valid_classes(test, hk) == ({"h1", "h2"},)
    assert loop.can_strictly_reduce(test, hk) is False
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=hk, q="q0",
        B=2, remaining_B=2,
    )
    library = [test, prep]
    assert loop.admit_decision(session, library) == "A1"
    chosen = loop.step(session, library, observation=_hyps("h1", "h2"))
    assert chosen is not None and chosen.id == "prep"


def test_explicit_empty_class_does_not_make_a_test_valuable() -> None:
    empty_only = loop.Action(
        "empty",
        loop.ActionKind.TEST,
        1,
        frozenset({"q0"}),
        obs_classes=(frozenset(),),
    )
    gap = loop.Action(
        "gap",
        loop.ActionKind.TEST,
        1,
        frozenset({"q0"}),
        obs_classes=(frozenset({"h3"}),),
    )
    hk = _hyps("h1", "h2")
    with pytest.raises(loop.PredictionGapError, match="empty") as empty_exc:
        loop.can_strictly_reduce(empty_only, hk)
    assert empty_exc.value.action_id == "empty"
    with pytest.raises(loop.PredictionGapError, match="gap") as gap_exc:
        loop.worst_remaining_count(gap, hk)
    assert gap_exc.value.action_id == "gap"
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=hk, q="q0",
        B=2, remaining_B=2,
    )
    with pytest.raises(loop.PredictionGapError, match="gap"):
        loop.step(session, [gap], observation=_hyps("h1"))
    assert session.stop is None
    assert session.charges == []
    assert session.history == []
    with pytest.raises(loop.PredictionGapError, match="gap"):
        loop.admit_decision(
            loop.Session(loop.ResourceMode.BUDGET, cmin=1, Hk=hk, q="q0", B=2, remaining_B=2),
            [gap],
        )


def test_prediction_gap_is_not_silent_a3() -> None:
    gap = loop.Action(
        "t",
        loop.ActionKind.TEST,
        1,
        frozenset({"q0"}),
        obs_classes=(frozenset({"h3"}),),
    )
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=2, remaining_B=2,
    )
    with pytest.raises(loop.PredictionGapError) as exc:
        loop.admit_decision(session, [gap])
    assert exc.value.action_id == "t"
    with pytest.raises(loop.PredictionGapError):
        loop.step(session, [gap], observation=_hyps("h1"))
    assert session.stop is None
    assert session.history == []
    assert session.charges == []


def test_unknown_eligible_recover_unaffordable_is_stop_budget() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q1"),
        loop.Action(
            "recover",
            loop.ActionKind.RECOVER,
            2,
            frozenset({"unreachable"}),
            next_q="q_sync",
            recover_when_unknown=True,
        ),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=1, remaining_B=1, retry_cap=3,
    )
    loop.step(session, library, error=loop.ErrorKind.UNKNOWN_EFFECT)
    assert session.stop == "Stop-Budget"
    assert session.q_status is loop.QStatus.UNKNOWN
    assert session.history[0].startswith("ERROR:UNKNOWN_EFFECT")
    assert session.charges == [("t1", 1)]
    assert loop.admit_decision(session, library) == "A5"


def test_uninformative_only_is_a3_not_execute() -> None:
    library = [
        loop.Action(
            "uninformative",
            loop.ActionKind.TEST,
            1,
            frozenset({"q0"}),
            obs_classes=(frozenset({"h1", "h2"}),),
        ),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=3, remaining_B=3,
    )
    assert loop.admit_decision(session, library) == "A3"
    assert loop.admissible(session, library)
    assert loop.select(session, loop.admissible(session, library)) is None
    assert loop.step(session, library, observation=_hyps("h1", "h2")) is None
    assert session.stop == "Stop-NoDistinguisher"
    assert session.charges == []


def test_unconfirmed_recover_then_unaffordable_stays_unknown() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q1"),
        loop.Action(
            "recover",
            loop.ActionKind.RECOVER,
            1,
            frozenset({"unreachable"}),
            next_q="q_sync",
            recover_when_unknown=True,
        ),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=2, remaining_B=2, retry_cap=3,
    )
    loop.step(session, library, error=loop.ErrorKind.UNKNOWN_EFFECT)
    chosen = loop.step(session, library, observation=_hyps("h1", "h2"))
    assert chosen is not None and chosen.id == "recover"
    assert session.q_status is loop.QStatus.UNKNOWN
    assert session.q == "q0"
    assert session.stop == "Stop-Budget"
    assert session.charges == [("t1", 1), ("recover", 1)]


def test_retry_cap_preempts_recover_in_s_and_a5() -> None:
    recover = loop.Action(
        "recover",
        loop.ActionKind.RECOVER,
        1,
        frozenset({"unreachable"}),
        next_q="q_sync",
        recover_when_unknown=True,
    )
    costly = loop.Action(
        "recover",
        loop.ActionKind.RECOVER,
        2,
        frozenset({"unreachable"}),
        next_q="q_sync",
        recover_when_unknown=True,
    )
    test = loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q1")
    available = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=10, remaining_B=10, retry_cap=1,
    )
    loop.step(available, [test, recover], error=loop.ErrorKind.UNKNOWN_EFFECT)
    assert available.stop == "Stop-Error"
    assert available.q_status is loop.QStatus.UNKNOWN
    assert available.history[0].startswith("ERROR:UNKNOWN_EFFECT")
    assert available.charges == [("t1", 1)]
    unaffordable = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=1, remaining_B=1, retry_cap=1,
    )
    loop.step(unaffordable, [test, costly], error=loop.ErrorKind.UNKNOWN_EFFECT)
    assert unaffordable.stop == "Stop-Error"
    assert unaffordable.q_status is loop.QStatus.UNKNOWN
    assert unaffordable.history[0].startswith("ERROR:UNKNOWN_EFFECT")
    assert unaffordable.charges == [("t1", 1)]
    assert unaffordable.remaining_B == 0


def test_resource_domain_rejects_non_finite_and_non_integer_inputs() -> None:
    hk = _hyps("h1", "h2")
    with pytest.raises(ValueError):
        loop.Session(loop.ResourceMode.BUDGET, cmin=1, Hk=hk, q="q0", B=math.inf, remaining_B=math.inf)
    with pytest.raises(ValueError):
        loop.Session(loop.ResourceMode.BUDGET, cmin=1, Hk=hk, q="q0", B=math.nan, remaining_B=1)
    with pytest.raises(ValueError):
        loop.Session(loop.ResourceMode.ROUNDS, cmin=1, Hk=hk, q="q0", Kmax=1.5)
    with pytest.raises(ValueError):
        loop.Session(loop.ResourceMode.BUDGET, cmin=1, Hk=hk, q="q0", B=2, remaining_B=3)
    with pytest.raises(ValueError):
        loop.Session(loop.ResourceMode.BUDGET, cmin=1, Hk=hk, q="q0", B=1, remaining_B=1, retry_cap=0)
    with pytest.raises(ValueError):
        loop.Action("t1", loop.ActionKind.TEST, math.inf, frozenset({"q0"}))
    with pytest.raises(ValueError):
        loop.Action("t1", loop.ActionKind.TEST, 1.5, frozenset({"q0"}))
    with pytest.raises(ValueError):
        loop.Action(
            "recover",
            loop.ActionKind.RECOVER,
            1,
            frozenset({"q0"}),
            recover_when_unknown=True,
        )


def _one_test_library() -> list:
    return [
        loop.Action(
            "t",
            loop.ActionKind.TEST,
            1,
            frozenset({"q"}),
            obs_classes=(frozenset({"normal"}), frozenset({"h1"})),
        )
    ]


def test_outside_singleton_does_not_resurrect_or_localize() -> None:
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("normal", "h1"), q="q",
        B=5, remaining_B=5,
    )
    chosen = loop.step(session, _one_test_library(), observation=_hyps("h2"))
    assert chosen is not None and chosen.id == "t"
    assert session.Hk == set()
    assert session.stop == "Stop-Empty"
    assert session.charges == [("t", 1)]
    assert "h2" not in session.Hk


def test_removed_hypothesis_cannot_reenter() -> None:
    library = [
        loop.Action(
            "t1",
            loop.ActionKind.TEST,
            1,
            frozenset({"q0"}),
            obs_classes=(frozenset({"h1", "h2"}),),
            next_q="q1",
        ),
        loop.Action(
            "t2",
            loop.ActionKind.TEST,
            1,
            frozenset({"q1"}),
            obs_classes=(frozenset({"h1"}), frozenset({"h2"})),
            next_q="q1",
        ),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2", "h3"), q="q0",
        B=5, remaining_B=5,
    )
    first = loop.step(session, library, observation=_hyps("h1", "h2"))
    assert first is not None and first.id == "t1"
    assert session.Hk == _hyps("h1", "h2")
    assert session.stop is None
    assert session.charges == [("t1", 1)]
    assert session.q == "q1"
    second = loop.step(session, library, observation=_hyps("h1", "h2", "h3"))
    assert second is not None and second.id == "t2"
    assert session.charges == [("t1", 1), ("t2", 1)]
    assert session.Hk == _hyps("h1", "h2")
    assert "h3" not in session.Hk
    assert session.stop is None


def test_valid_observation_subset_is_intersected() -> None:
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("normal", "h1", "h2"), q="q",
        B=5, remaining_B=5,
    )
    library = [
        loop.Action("t", loop.ActionKind.TEST, 1, frozenset({"q"}), worst_remaining=2, next_q="q"),
    ]
    loop.step(session, library, observation=_hyps("normal", "h1"))
    assert session.Hk == _hyps("normal", "h1")
    assert session.stop is None
    assert session.Hk <= _hyps("normal", "h1", "h2")


def test_legitimate_empty_class_is_inconsistency_not_input_error() -> None:
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=2, remaining_B=2,
    )
    library = [loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q0")]
    loop.step(session, library, observation=set())
    assert session.stop == "Stop-Empty"
    assert session.Hk == set()
    assert session.charges == [("t1", 1)]


def test_error_leaves_candidate_set_unchanged() -> None:
    library = [loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q0")]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("h1", "h2"), q="q0",
        B=4, remaining_B=4, retry_cap=3,
    )
    loop.step(session, library, error=loop.ErrorKind.NOT_SENT)
    assert session.Hk == _hyps("h1", "h2")
    assert session.stop is None


def test_recover_observation_class_is_also_intersected() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1, next_q="q1"),
        loop.Action(
            "recover",
            loop.ActionKind.RECOVER,
            1,
            frozenset({"unreachable"}),
            next_q="q_sync",
            recover_when_unknown=True,
        ),
    ]
    session = loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps("normal", "h1"), q="q0",
        B=10, remaining_B=10, retry_cap=3,
    )
    loop.step(session, library, error=loop.ErrorKind.UNKNOWN_EFFECT)
    assert session.Hk == _hyps("normal", "h1")
    loop.step(session, library, observation=_hyps("h2"), confirmed_q="q_sync")
    assert session.Hk == set()
    assert session.stop == "Stop-Empty"
