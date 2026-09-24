"""F-C: decomposed CL-TAV control-flow equivalence witnesses and production negatives.

The bounded walk-through spec ``scripts/cltav_loop_spec.py`` is the executable
reference for admission, charging, ERROR, retry and stop classification. The
typeset package is the reference for the S6/S7-S8 contracts. This file checks
that the decomposition preserves the specified call order and that deleting a
key call from an actual TeX sub-module fails the production governance entry
(``check_repo_baseline.cltav_algorithm_contract_errors``), not just a registry field.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


loop = _load("cltav_loop_spec", ROOT / "scripts/cltav_loop_spec.py")
baseline = _load("check_repo_baseline", ROOT / "scripts/check_repo_baseline.py")

ALG_DIR = ROOT / "docs/research/publication/algorithms"
ALG_MODULE_FILES = {
    "ALG-CLTAV-01": "ALG-CLTAV-01.tex",
    "ALG-CLTAV-05": "ALG-CLTAV-05-selection.tex",
    "ALG-CLTAV-06": "ALG-CLTAV-06-timing.tex",
    "ALG-CLTAV-07": "ALG-CLTAV-07-history.tex",
    "ALG-CLTAV-02": "ALG-CLTAV-02.tex",
    "ALG-CLTAV-03": "ALG-CLTAV-03.tex",
    "ALG-CLTAV-04": "ALG-CLTAV-04.tex",
    "ALG-CLTAV-APPENDIX": "CLTAV_ALGORITHM_APPENDIX.tex",
}
PUML_PATH = ROOT / "docs/research/publication/models/FIG-CL-TAV-09-experiment-architecture.puml"
EXP_PLAN = ROOT / "docs/research/EXPERIMENT_PLAN.md"


def _algorithms(overrides: dict[str, str] | None = None) -> dict[str, str]:
    overrides = overrides or {}
    return {
        module: overrides.get(module, (ALG_DIR / name).read_text(encoding="utf-8"))
        for module, name in ALG_MODULE_FILES.items()
    }


def _contract(overrides: dict[str, str] | None = None) -> list[str]:
    return baseline.cltav_algorithm_contract_errors(
        _algorithms(overrides),
        PUML_PATH.read_text(encoding="utf-8"),
        EXP_PLAN.read_text(encoding="utf-8"),
    )


def _mutate(module: str, old: str, new: str) -> dict[str, str]:
    text = _algorithms()[module]
    assert old in text, f"expected anchor missing from {module}: {old!r}"
    return {module: text.replace(old, new)}


def _hyps(*names: str) -> set[str]:
    return set(names)


def _session(H=("h1", "h2"), q="q0", *, B=10, retry_cap=3):
    return loop.Session(
        loop.ResourceMode.BUDGET, cmin=1, Hk=_hyps(*H), q=q,
        B=B, remaining_B=B, retry_cap=retry_cap,
    )


# ---------------------------------------------------------------------------
# Equivalence witness matrix (work order section 11). Each witness fixes the
# abstract backend outputs and checks the resulting (H, resource, retry, stop).
# ---------------------------------------------------------------------------
def test_case_valid_test_commits_q1_and_stops_on_singleton() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), next_q="q1",
                    obs_classes=(frozenset({"h1", "h2"}), frozenset({"h2", "h3"}),
                                 frozenset({"h1", "h3"}))),
        loop.Action("t2", loop.ActionKind.TEST, 1, frozenset({"q1"}), next_q="q1",
                    obs_classes=(frozenset({"h1"}), frozenset({"h2"}))),
    ]
    session = _session(H=("h1", "h2", "h3"), q="q0")
    assert loop.step(session, library, observation=_hyps("h1", "h2")).id == "t1"
    assert session.q == "q1"
    assert session.charges == [("t1", 1)]
    assert loop.step(session, library, observation=_hyps("h1")).id == "t2"
    assert session.stop == "Stop-Singleton"


def test_case03_uninformative_test_not_charged_and_prep_chosen() -> None:
    library = [
        loop.Action("uninformative", loop.ActionKind.TEST, 1, frozenset({"q0"}),
                    obs_classes=(frozenset({"h1", "h2"}),)),
        loop.Action("prep", loop.ActionKind.PREP, 1, frozenset({"q0"}), next_q="q1"),
    ]
    session = _session()
    assert loop.step(session, library, observation=_hyps("h1", "h2")).id == "prep"
    assert session.charges == [("prep", 1)]


def test_case04_overlapping_classes_remain_distinguishing() -> None:
    overlap = loop.Action("overlap", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=2,
                          obs_classes=(frozenset({"h1", "h2"}), frozenset({"h1"}), frozenset({"h2"})))
    assert loop.can_strictly_reduce(overlap, _hyps("h1", "h2"))
    session = _session()
    assert loop.step(session, [overlap], observation=_hyps("h1", "h2")).id == "overlap"


def test_case06_distinguishing_but_unaffordable_is_stop_budget() -> None:
    costly = loop.Action("costly", loop.ActionKind.TEST, 5, frozenset({"q0"}), worst_remaining=1)
    session = _session(B=1)
    assert loop.step(session, [costly], observation=_hyps("h1")) is None
    assert session.stop == "Stop-Budget"
    assert session.charges == []


def test_case07_unknown_without_recover_is_a4_with_eligible_unaffordable_a5() -> None:
    no_recover = loop.Action("t", loop.ActionKind.TEST, 1, frozenset({"q0"}), worst_remaining=1)
    session = _session()
    loop.step(session, [no_recover], error=loop.ErrorKind.UNKNOWN_EFFECT)
    assert loop.admit_decision(session, [no_recover]) == "A4"
    costly_recover = loop.Action("recover", loop.ActionKind.RECOVER, 9, frozenset({"x"}),
                                 next_q="q_sync", recover_when_unknown=True)
    session2 = _session(B=2, retry_cap=5)
    loop.step(session2, [no_recover, costly_recover], error=loop.ErrorKind.UNKNOWN_EFFECT)
    assert loop.admit_decision(session2, [no_recover, costly_recover]) == "A5"


def test_case08_unknown_effect_keeps_h_clears_summary_one_charge_counts_retry() -> None:
    library = [loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), next_q="q1", worst_remaining=1)]
    session = _session(retry_cap=5)
    loop.step(session, library, error=loop.ErrorKind.UNKNOWN_EFFECT)
    assert session.Hk == _hyps("h1", "h2")
    assert session.q_status is loop.QStatus.UNKNOWN
    assert session.retries == 1
    assert session.charges == [("t1", 1)]


def test_case09_confirmed_not_sent_keeps_known_and_counts_retry() -> None:
    library = [loop.Action("prep", loop.ActionKind.PREP, 1, frozenset({"q0"}), next_q="q1")]
    session = _session(retry_cap=5)
    loop.step(session, library, error=loop.ErrorKind.NOT_SENT)
    assert session.q_status is loop.QStatus.KNOWN
    assert session.q == "q0"
    assert session.retries == 1
    assert session.stop is None


def test_case12_unconfirmed_recover_stays_unknown_confirmed_reads_new_summary() -> None:
    library = [
        loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), next_q="q1", worst_remaining=1),
        loop.Action("recover", loop.ActionKind.RECOVER, 1, frozenset({"x"}),
                    next_q="q_sync", recover_when_unknown=True),
    ]
    session = _session(retry_cap=5)
    loop.step(session, library, error=loop.ErrorKind.UNKNOWN_EFFECT)
    loop.step(session, library, observation=_hyps("h1", "h2"))
    assert session.q_status is loop.QStatus.UNKNOWN
    assert session.q == "q0"
    confirmed = _session(retry_cap=5)
    loop.step(confirmed, library, error=loop.ErrorKind.UNKNOWN_EFFECT)
    loop.step(confirmed, library, observation=_hyps("h1", "h2"), confirmed_q="q_sync")
    assert confirmed.q == "q_sync"
    assert confirmed.q_status is loop.QStatus.KNOWN


def test_case13_retry_cap_reached_is_stop_error_not_budget() -> None:
    library = [loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), next_q="q0", worst_remaining=1)]
    session = _session(B=10, retry_cap=1)
    loop.step(session, library, error=loop.ErrorKind.UNKNOWN_EFFECT)
    assert session.stop == "Stop-Error"
    assert session.remaining_B == 9


def test_case14_error_does_not_delete_candidates_or_double_charge() -> None:
    library = [loop.Action("t1", loop.ActionKind.TEST, 1, frozenset({"q0"}), next_q="q0", worst_remaining=1)]
    session = _session(B=4)
    loop.step(session, library, error=loop.ErrorKind.NOT_SENT)
    assert session.Hk == _hyps("h1", "h2")
    assert session.charges == [("t1", 1)]


def test_case15_stop_priority_is_exclusive_and_unknown_is_not_equivalent() -> None:
    assert loop.UPDATE_STOP_PRIORITY == (
        "Stop-Empty", "Stop-Singleton", "Stop-645", "Stop-Equivalent", "Stop-Budget",
    )
    singleton = _session(B=5)
    loop.step(singleton, [loop.Action("t", loop.ActionKind.TEST, 1, frozenset({"q0"}), next_q="q0", worst_remaining=1)],
              observation=_hyps("h1"))
    assert singleton.stop == "Stop-Singleton"  # not protocol PASS


# ---------------------------------------------------------------------------
# Production negatives: deleting a key call from an actual TeX sub-module must
# fail the production governance entry, not just a registry field.
# ---------------------------------------------------------------------------
def test_clean_package_passes_the_production_entry() -> None:
    assert _contract() == []


def test_deleting_predict_call_from_submodule_is_rejected() -> None:
    errors = _contract(_mutate("ALG-CLTAV-02", r"\IFpred", r"\IFUNDECLARED"))
    assert any("IF-PRED-OBS" in item or "IFUNDECLARED" in item for item in errors)


def test_deleting_predictcurrent_definition_is_rejected() -> None:
    errors = _contract(_mutate("ALG-CLTAV-02", "PredictCurrent", "SomethingElse"))
    assert any("ALG-CLTAV-02 does not define PredictCurrent" in item for item in errors)


def test_reordering_actionid_before_select_is_rejected() -> None:
    errors = _contract(_mutate("ALG-CLTAV-01", "SelectAndAdmit", "actionId SelectAndAdmit"))
    assert any("actionId" in item for item in errors)


def test_deleting_s9_commit_is_rejected() -> None:
    errors = _contract(_mutate(
        "ALG-CLTAV-07",
        r"\Gamma'.\mathrm{currentSummary}\leftarrow z.\mathrm{postSummary}",
        "",
    ))
    assert any("S9 must commit currentSummary" in item for item in errors)


def test_deleting_prep_interpretation_call_is_rejected() -> None:
    errors = _contract(_mutate("ALG-CLTAV-03", r"\IFprep", r"\IFUNDECLARED"))
    assert any("IF-PREP-RECOVER" in item or "IFUNDECLARED" in item for item in errors)


def test_deleting_known_sole_writer_is_rejected() -> None:
    errors = _contract(_mutate("ALG-CLTAV-04", "sole writer", "not the writer"))
    assert any("sole writer" in item for item in errors)


def test_deleting_history_call_is_rejected() -> None:
    errors = _contract(_mutate(
        "ALG-CLTAV-07",
        r"\IFhist$(\eta,H,\xi.\mathrm{actionId},\xi.\mathrm{qUsedAtSelect},\xi.\mathrm{classesUsedAtSelect},z.I_z,z.\mathrm{postSummary})$",
        "noop",
    ))
    assert any("IF-HIST-UPDATE" in item for item in errors)


def test_missing_submodule_is_rejected() -> None:
    algorithms = _algorithms()
    del algorithms["ALG-CLTAV-04"]
    errors = baseline.cltav_algorithm_contract_errors(
        algorithms, PUML_PATH.read_text(encoding="utf-8"), EXP_PLAN.read_text(encoding="utf-8"),
    )
    assert any("presentationModules" in item for item in errors)


def test_deleting_one_step_minimax_is_rejected() -> None:
    errors = _contract(_mutate("ALG-CLTAV-05", "one-step minimax", "some selection"))
    assert any("minimax" in item for item in errors)


def test_undeclared_interface_call_in_submodule_is_rejected() -> None:
    errors = _contract(_mutate("ALG-CLTAV-02", r"\end{algorithm}", r"% IF-UNDECLARED" + "\n" + r"\end{algorithm}"))
    assert any("undeclared interface call IF-UNDECLARED" in item for item in errors)


def test_top_level_procedure_order_is_preserved() -> None:
    main = _algorithms()["ALG-CLTAV-01"]
    positions = [main.find(name) for name in baseline.CLTAV_MAIN_PROCEDURES]
    assert all(pos >= 0 for pos in positions)
    assert positions == sorted(positions)
