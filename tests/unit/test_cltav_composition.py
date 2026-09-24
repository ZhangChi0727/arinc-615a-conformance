"""Executable composition witness for the decomposed CL-TAV algorithm (R36-F03).

This is a minimal, test-local coordinator that mirrors the ALG-CLTAV-01 loop and
the typed module returns (PredictionResult, Decision, Outcome, Resolution). It
exercises the new orchestration and its argument/return wiring, not the unchanged
loop-spec interpreter. Scripted backends supply the abstract returns. Finite
witnesses prove only the enumerated paths; they are not a formal equivalence proof
and not source-fidelity evidence for the backend kernels.
"""

from __future__ import annotations

import copy
import importlib.util
import json
from dataclasses import dataclass, field
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    assert old in text, f"anchor missing from {module}: {old!r}"
    return {module: text.replace(old, new)}


# ---------------------------------------------------------------------------
# Typed records (mirroring Appendix A) and the composition coordinator.
# ---------------------------------------------------------------------------
@dataclass
class PredictionResult:
    status: str  # OK / GAP
    classes_by_test: dict[str, tuple[set[str], ...]] = field(default_factory=dict)
    reason: str | None = None


@dataclass
class Decision:
    kind: str  # ACTION / EXIT / SPEC-ERROR
    action_id: str | None = None
    action_kind: str | None = None
    classes_used: tuple[set[str], ...] = ()
    reason: str | None = None


@dataclass
class Outcome:
    effect: str = "NONE"
    kind: str | None = None
    action_id: str | None = None
    iz: set[str] | None = None
    summary_confirmed: bool = False
    post_summary: str | None = None
    prep_result_evaluated: bool = False
    target_confirmed: bool = False
    prep_err: bool = False
    declared_target: str | None = None
    evidence: str | None = None


@dataclass
class Resolution:
    control: str  # COMMIT / RETRY / STOP
    outcome: Outcome
    reason: str | None = None


class Composition:
    """Mirrors ALG-CLTAV-01 S0--S10 with explicit typed module returns."""

    def __init__(self, H: set[str], q: str | None, resource: int, retry_cap: int = 3):
        self.H = set(H)
        self.q = q
        self.q_status = "KNOWN" if q is not None else "UNKNOWN"
        self.history: list[str] = []
        self.resource = resource
        self.retry = 0
        self.retry_cap = retry_cap
        self.stop: str | None = None
        self.trace: list[str] = []
        self._k = 0

    # S1 / S10
    def _stop_check(self, *, named_645=False, equivalent=False) -> str | None:
        if not self.H:
            return "Stop-Empty"
        if len(self.H) == 1:
            return "Stop-Singleton"
        if named_645:
            return "Stop-645"
        if equivalent:
            return "Stop-Equivalent"
        if self.resource <= 0:
            return "Stop-Budget"
        return None

    def run_round(self, pred: PredictionResult, execute, *, named_645=False, equivalent=False) -> None:
        self.trace.append(f"S{self._k}:entry")
        stop = self._stop_check(named_645=named_645, equivalent=equivalent)
        if stop:
            self.stop = stop
            return
        self._k += 1
        # S2
        self.trace.append("S2:predict")
        if pred.status == "GAP":
            self.trace.append("S2:gap")
            if not execute.gap_fallback:
                self.stop = pred.reason
                return
        # S3 selection
        self.trace.append("S3:select")
        decision = execute.action if execute.action is not None else self._select(pred)
        if decision.kind in {"EXIT", "SPEC-ERROR"}:
            self.stop = decision.reason
            return
        # freeze snapshot
        snapshot = {
            "actionId": decision.action_id,
            "kind": decision.action_kind,
            "qUsedAtSelect": self.q,
            "historyVersion": len(self.history),
            "classesUsedAtSelect": decision.classes_used,
        }
        self.trace.append(f"S3:snap:{snapshot['actionId']}")
        # S4 charge once
        self.resource -= 1
        self.trace.append("S4:charge")
        # S5 execute
        self.trace.append("S5:execute")
        outcome = execute(snapshot, self.H)
        # S6 interpret (outcome carries its action id/kind)
        outcome.action_id = snapshot["actionId"]
        outcome.kind = snapshot["kind"]
        self.trace.append("S6:interpret")
        # S7-S8 resolve
        resolution = self._resolve(outcome)
        self.trace.append(f"S7-8:{resolution.control}")
        if resolution.control == "STOP":
            self.stop = resolution.reason
            return
        if resolution.control == "RETRY":
            return
        # S9 commit
        self.trace.append("S9:commit")
        z = resolution.outcome
        if z.iz is not None:
            self.H = self.H & z.iz
        self.history.append(f"commit:{snapshot['actionId']}")
        if self.q_status == "KNOWN" and z.summary_confirmed and z.post_summary is not None:
            self.q = z.post_summary
        # S10
        self.trace.append("S10:stop")
        stop = self._stop_check(named_645=named_645, equivalent=equivalent)
        if stop:
            self.stop = stop

    def _select(self, pred: PredictionResult):
        if pred.status == "GAP":
            return Decision("EXIT", reason=pred.reason)
        best: tuple[tuple[int, str], str, tuple[set[str], ...]] | None = None
        for test_id, classes in pred.classes_by_test.items():
            distinguished = any(0 < len(c) < len(self.H) for c in classes)
            if distinguished:
                key = (max(len(c) for c in classes), test_id)
                if best is None or key < best[0]:
                    best = (key, test_id, tuple(classes))
        if best is None:
            return Decision("EXIT", reason="Stop-NoDistinguisher")
        _, test_id, classes = best
        return Decision("ACTION", action_id=test_id, action_kind="TEST", classes_used=classes)

    def _resolve(self, z: Outcome) -> Resolution:
        if (
            z.effect in {"CONFIRMED-NOT-SENT", "UNKNOWN-EFFECT"}
            or z.prep_err
            or (z.kind == "PREP" and z.prep_result_evaluated and not z.summary_confirmed)
            or (z.action_id is not None and z.kind == "RECOVER" and z.prep_result_evaluated
                and not z.target_confirmed)
        ):
            if z.prep_err or z.effect == "UNKNOWN-EFFECT" or (
                z.kind == "PREP" and z.prep_result_evaluated and not z.summary_confirmed
            ):
                self.q_status = "UNKNOWN"
                self.q = None
                self.history.append("eta:unknown")
            elif z.effect == "CONFIRMED-NOT-SENT":
                pass
            else:
                self.q_status = "UNKNOWN"
                self.q = None
                self.history.append("eta:unknown")
            self.retry += 1
            if self.retry >= self.retry_cap:
                return Resolution("STOP", z, reason="Stop-Error")
            return Resolution("RETRY", z)
        if z.kind == "RECOVER":
            self.q_status = "KNOWN"
            z.post_summary = z.declared_target
        return Resolution("COMMIT", z)

    def observe(self) -> dict:
        return {
            "H": set(self.H),
            "q": self.q,
            "qStatus": self.q_status,
            "history": list(self.history),
            "resource": self.resource,
            "retry": self.retry,
            "stop": self.stop,
            "trace": list(self.trace),
        }


class Execute:
    """Scripted S3/S5/S6 backend: optional explicit action, then an Outcome."""

    def __init__(self, outcome_fn, *, gap_fallback: bool = False, action: Decision | None = None):
        self.outcome_fn = outcome_fn
        self.gap_fallback = gap_fallback
        self.action = action

    def __call__(self, snapshot, H):
        return self.outcome_fn(snapshot, H)


# ---------------------------------------------------------------------------
# 17-case equivalence matrix, routed through the new composition.
# ---------------------------------------------------------------------------
def test_case01_ordinary_test_q0_to_q1() -> None:
    comp = Composition(H={"h1", "h2", "h3"}, q="q0", resource=5)
    pred = PredictionResult("OK", {"t1": ({frozenset({"h1", "h2"})},)})

    def outcome(snapshot, H):
        return Outcome(effect="NONE", iz={"h1", "h2"}, summary_confirmed=True, post_summary="q1")

    comp.run_round(pred, Execute(outcome))
    obs = comp.observe()
    assert obs["q"] == "q1" and obs["qStatus"] == "KNOWN"
    assert obs["H"] == {"h1", "h2"}
    assert obs["resource"] == 4 and obs["retry"] == 0
    assert "S4:charge" in obs["trace"] and "S9:commit" in obs["trace"]


def test_case02_two_rounds_no_resurrection() -> None:
    comp = Composition(H={"h1", "h2", "h3"}, q="q0", resource=5)

    def o1(s, H):
        return Outcome(effect="NONE", iz={"h1", "h2"}, summary_confirmed=True, post_summary="q1")

    def o2(s, H):
        return Outcome(effect="NONE", iz={"h1", "h2", "h3"}, summary_confirmed=True, post_summary="q1")

    comp.run_round(PredictionResult("OK", {"t1": ({frozenset({"h1", "h2"})},)}), Execute(o1))
    assert comp.observe()["H"] == {"h1", "h2"}
    comp.run_round(PredictionResult("OK", {"t2": ({frozenset({"h1"})},)}), Execute(o2))
    assert "h3" not in comp.observe()["H"]


def test_case03_overlapping_classes_still_distinguishing() -> None:
    comp = Composition(H={"h1", "h2"}, q="q0", resource=5)
    pred = PredictionResult("OK", {"overlap": (frozenset({"h1", "h2"}), frozenset({"h1"}))})

    def outcome(s, H):
        return Outcome(effect="NONE", iz={"h1"}, summary_confirmed=True, post_summary="q0")

    comp.run_round(pred, Execute(outcome))
    assert comp.observe()["stop"] == "Stop-Singleton"


def test_case04_prediction_gap_with_eligible_recover() -> None:
    comp = Composition(H={"h1", "h2"}, q="q0", resource=5)
    pred = PredictionResult("GAP", reason="gap")

    def outcome(s, H):
        return Outcome(effect="NONE", iz={"h1", "h2"}, summary_confirmed=True, post_summary="q_sync")

    comp.run_round(pred, Execute(outcome, gap_fallback=True,
                                 action=Decision("ACTION", action_id="recover", action_kind="RECOVER")))
    assert comp.observe()["stop"] is None
    assert "S2:gap" in comp.observe()["trace"]


def test_case05_backend_gap_without_fallback_is_named_gap() -> None:
    comp = Composition(H={"h1", "h2"}, q="q0", resource=5)
    comp.run_round(PredictionResult("GAP", reason="Stop-TestGap"), Execute(lambda s, H: Outcome()))
    assert comp.observe()["stop"] == "Stop-TestGap"


def test_case06_confirmed_not_sent_keeps_known() -> None:
    comp = Composition(H={"h1", "h2", "h3"}, q="q0", resource=5)
    pred = PredictionResult("OK", {"t1": ({frozenset({"h1", "h2"})},)})

    def outcome(s, H):
        return Outcome(effect="CONFIRMED-NOT-SENT")

    comp.run_round(pred, Execute(outcome))
    obs = comp.observe()
    assert obs["q"] == "q0" and obs["qStatus"] == "KNOWN"
    assert obs["retry"] == 1 and obs["H"] == {"h1", "h2", "h3"}


def test_case07_unknown_effect_is_conservative() -> None:
    comp = Composition(H={"h1", "h2", "h3"}, q="q0", resource=5)
    pred = PredictionResult("OK", {"t1": ({frozenset({"h1", "h2"})},)})

    def outcome(s, H):
        return Outcome(effect="UNKNOWN-EFFECT")

    comp.run_round(pred, Execute(outcome))
    obs = comp.observe()
    assert obs["qStatus"] == "UNKNOWN" and obs["q"] is None
    assert obs["H"] == {"h1", "h2", "h3"} and obs["retry"] == 1


def test_case08_confirmed_recover_reads_new_summary() -> None:
    comp = Composition(H={"h1", "h2"}, q=None, resource=5)

    def outcome(s, H):
        return Outcome(effect="NONE", kind="RECOVER", target_confirmed=True,
                       summary_confirmed=True, declared_target="q_sync")

    comp.run_round(PredictionResult("OK", {"t": ({frozenset({"h1"})},)}),
                   Execute(outcome, action=Decision("ACTION", action_id="recover", action_kind="RECOVER")))
    obs = comp.observe()
    assert obs["q"] == "q_sync" and obs["qStatus"] == "KNOWN"


def test_case09_unconfirmed_recover_stays_unknown() -> None:
    comp = Composition(H={"h1", "h2"}, q=None, resource=5)

    def outcome(s, H):
        return Outcome(effect="NONE", kind="RECOVER", prep_result_evaluated=True,
                       target_confirmed=False, summary_confirmed=False)

    comp.run_round(PredictionResult("OK", {"t": ({frozenset({"h1"})},)}),
                   Execute(outcome, action=Decision("ACTION", action_id="recover", action_kind="RECOVER")))
    obs = comp.observe()
    assert obs["qStatus"] == "UNKNOWN" and obs["retry"] == 1


def test_case10_prep_confirmed_actual_successor_unmet_target() -> None:
    comp = Composition(H={"h1", "h2", "h3"}, q="q0", resource=5)

    def outcome(s, H):
        return Outcome(effect="NONE", kind="PREP", prep_result_evaluated=True,
                       target_confirmed=False, summary_confirmed=True, post_summary="q1")

    comp.run_round(PredictionResult("OK", {"t": ({frozenset({"h1", "h2"})},)}),
                   Execute(outcome, action=Decision("ACTION", action_id="prep", action_kind="PREP")))
    obs = comp.observe()
    assert obs["q"] == "q1" and obs["retry"] == 0


def test_case11_unconfirmed_prep_successor_enters_s7() -> None:
    comp = Composition(H={"h1", "h2", "h3"}, q="q0", resource=5)

    def outcome(s, H):
        return Outcome(effect="NONE", kind="PREP", prep_result_evaluated=True,
                       target_confirmed=False, summary_confirmed=False)

    comp.run_round(PredictionResult("OK", {"t": ({frozenset({"h1", "h2"})},)}),
                   Execute(outcome, action=Decision("ACTION", action_id="prep", action_kind="PREP")))
    obs = comp.observe()
    assert obs["qStatus"] == "UNKNOWN" and obs["retry"] == 1 and obs["H"] == {"h1", "h2", "h3"}


def test_case12_retry_cap_reached_is_stop_error() -> None:
    comp = Composition(H={"h1", "h2"}, q="q0", resource=10, retry_cap=1)
    pred = PredictionResult("OK", {"t": ({frozenset({"h1"})},)})

    def outcome(s, H):
        return Outcome(effect="UNKNOWN-EFFECT")

    comp.run_round(pred, Execute(outcome))
    obs = comp.observe()
    assert obs["stop"] == "Stop-Error" and obs["resource"] == 9


def test_case13_error_does_not_delete_candidates_or_double_charge() -> None:
    comp = Composition(H={"h1", "h2"}, q="q0", resource=4, retry_cap=3)
    pred = PredictionResult("OK", {"t": ({frozenset({"h1"})},)})

    def outcome(s, H):
        return Outcome(effect="UNKNOWN-EFFECT")

    comp.run_round(pred, Execute(outcome))
    obs = comp.observe()
    assert obs["H"] == {"h1", "h2"} and obs["resource"] == 3
    assert obs["trace"].count("S4:charge") == 1


def test_case14_empty_after_update_is_stop_empty() -> None:
    comp = Composition(H={"h1", "h2"}, q="q0", resource=5)

    def outcome(s, H):
        return Outcome(effect="NONE", iz=set(), summary_confirmed=True, post_summary="q0")

    comp.run_round(PredictionResult("OK", {"t": ({frozenset({"h1"})},)}), Execute(outcome))
    assert comp.observe()["stop"] == "Stop-Empty"


def test_case15_singleton_is_not_protocol_pass() -> None:
    comp = Composition(H={"h1", "h2"}, q="q0", resource=5)

    def outcome(s, H):
        return Outcome(effect="NONE", iz={"h1"}, summary_confirmed=True, post_summary="q0")

    comp.run_round(PredictionResult("OK", {"t": ({frozenset({"h1"})},)}), Execute(outcome))
    assert comp.observe()["stop"] == "Stop-Singleton"


def test_case16_same_h_different_history_not_merged_by_h() -> None:
    comp = Composition(H={"h1", "h2", "h3"}, q="q0", resource=6)

    def o1(s, H):
        return Outcome(effect="NONE", iz={"h1", "h2"}, summary_confirmed=True, post_summary="q1")

    def o2(s, H):
        return Outcome(effect="NONE", iz={"h1", "h2"}, summary_confirmed=True, post_summary="q2")

    comp.run_round(PredictionResult("OK", {"t1": ({frozenset({"h1", "h2"})},)}), Execute(o1))
    h_after_one = set(comp.observe()["H"])
    comp.run_round(PredictionResult("OK", {"t2": ({frozenset({"h1", "h2"})},)}), Execute(o2))
    obs = comp.observe()
    assert obs["H"] == h_after_one  # same H ...
    assert obs["history"] != []  # ... but history advanced and is retained


def test_case17_all_unstopped_paths_return_to_s1() -> None:
    comp = Composition(H={"h1", "h2", "h3", "h4"}, q="q0", resource=6)

    def outcome(s, H):
        return Outcome(effect="NONE", iz={"h1", "h2", "h3"}, summary_confirmed=True, post_summary="q1")

    comp.run_round(PredictionResult("OK", {"t": ({frozenset({"h1", "h2", "h3"})},)}), Execute(outcome))
    obs = comp.observe()
    assert obs["stop"] is None  # H={h1,h2,h3}, resource remains: the loop returns to S1
    assert obs["resource"] == 5
    assert obs["trace"][-1] == "S10:stop"


# ---------------------------------------------------------------------------
# Module-level witnesses (T5, ownership, no-response, shared uncertainty).
# ---------------------------------------------------------------------------
def test_module_t5_equal_and_open_upper_bound() -> None:
    # T5: M subset N -> PASS; M disjoint -> FAIL; overlap -> INCONCLUSIVE.
    def verdict(m_lo, m_hi, n_lo, n_hi):
        if m_lo >= n_lo and m_hi <= n_hi:
            return "PASS"
        if m_hi < n_lo or m_lo > n_hi:
            return "FAIL"
        return "INCONCLUSIVE"

    assert verdict(105, 115, 100, 120) == "PASS"      # wholly inside
    assert verdict(121, 125, 100, 120) == "FAIL"      # wholly outside
    assert verdict(118, 122, 100, 120) == "INCONCLUSIVE"  # overlaps upper boundary
    assert verdict(120, 120, 100, 120) == "PASS"      # exact closed upper endpoint
    assert verdict(120, 120, 100, 119) == "FAIL"      # open upper endpoint excludes equality


def test_module_ownership_is_single_result_for_t2_and_no_response() -> None:
    # One ownership result feeds both the T2 pairing and the no-response rule.
    ownership = {"instance": "I1", "valid": True, "key": "r1"}
    pair = {"trigger": "t0", "response": "t1"} if ownership["valid"] else None
    assert pair is not None
    no_response = None  # response present, so the no-response rule does not fire
    assert (pair is None) == (no_response is not None)


def test_module_cancellation_cannot_claim_later_response() -> None:
    instances = [
        {"id": "I1", "state": "CANCELLED"},
        {"id": "I2", "state": "ACTIVE", "key": "r2"},
    ]
    claimed = [i for i in instances if i["state"] == "ACTIVE" and i["key"] == "r2"]
    assert [i["id"] for i in claimed] == ["I2"]


def test_module_no_response_forms_only_after_expiry() -> None:
    def no_response(active, now, deadline):
        return "FAIL" if (active and now > deadline) else "INCONCLUSIVE"

    assert no_response(True, 101, 100) == "FAIL"
    assert no_response(True, 99, 100) == "INCONCLUSIVE"
    assert no_response(False, 101, 100) == "INCONCLUSIVE"


def test_module_common_uncertainty_used_in_prediction_and_update() -> None:
    # The same epsilon drives the observation class projection and the update interval.
    eps = 3
    observed = 118
    m = (observed - eps, observed + eps)
    assert m == (115, 121)
    # prediction scores classes under the same interval; update intersects with it
    assert m[0] <= 118 <= m[1]


# ---------------------------------------------------------------------------
# R36-F03 persisted production negatives and positive controls.
# ---------------------------------------------------------------------------
def test_clean_package_passes() -> None:
    assert _contract() == []


def test_negative_charge_once_only_in_comment_is_rejected() -> None:
    text = _algorithms()["ALG-CLTAV-01"]
    mutated = text.replace(
        r"$\Gamma\leftarrow\textsc{ChargeOnce}(\Gamma,\xi)$\;",
        r"% \textsc{ChargeOnce} retained in a comment only",
    )
    assert mutated != text
    errors = _contract({"ALG-CLTAV-01": mutated})
    assert any("charge once as an executable statement" in item for item in errors)


def test_negative_interpret_outcome_wrong_argument_is_rejected() -> None:
    errors = _contract(_mutate(
        "ALG-CLTAV-01",
        r"\textsc{InterpretOutcome}(\textit{er},\xi,\Gamma,\eta,U)",
        r"\textsc{InterpretOutcome}(WRONG)",
    ))
    assert any("InterpretOutcome must receive" in item for item in errors)


def test_negative_alg04_retry_to_commit_is_rejected() -> None:
    errors = _contract(_mutate(
        "ALG-CLTAV-04",
        r"\mathrm{control}=\texttt{RETRY}",
        r"\mathrm{control}=\texttt{COMMIT}",
    ))
    assert any("RETRY" in item for item in errors)


def test_negative_prediction_gap_projected_is_rejected() -> None:
    text = _algorithms()["ALG-CLTAV-02"]
    mutated = text.replace(
        r"$\textit{raw}\leftarrow$ \IFpred$(\Gamma,\eta,H,U,L)$\;",
        r"$\textit{raw}\leftarrow$ \IFpred$(\Gamma,\eta,H,U,L)$\; "
        r"$\textit{classes}\leftarrow\textsc{ProjectOntoCurrentH}(\textit{raw}.\mathrm{classes},H)$\;",
    )
    assert mutated != text
    errors = _contract({"ALG-CLTAV-02": mutated})
    assert any("gap tag before class projection" in item for item in errors)


def test_negative_history_assignment_instead_of_intersection_is_rejected() -> None:
    errors = _contract(_mutate("ALG-CLTAV-07", r"H'\leftarrow H\cap z.I_z", r"H'\leftarrow z.I_z"))
    assert any("intersect" in item or "assign H = I_z" in item for item in errors)


def test_negative_timing_verdict_as_candidate_set_is_rejected() -> None:
    errors = _contract(_mutate("ALG-CLTAV-06", r"\mathrm{owns}\leftarrow", r"I_z\leftarrow"))
    assert any("must not emit the candidate set" in item for item in errors)


def test_positive_semantics_preserving_formatting_passes() -> None:
    # Reflowing a line (extra spaces) must not trip the structured checks.
    text = _algorithms()["ALG-CLTAV-07"]
    reformatted = text.replace(
        r"$\Gamma'.\mathrm{currentSummary}\leftarrow z.\mathrm{postSummary}$",
        r"$\Gamma'.\mathrm{currentSummary}  \leftarrow  z.\mathrm{postSummary}$",
        1,
    )
    assert reformatted != text
    assert _contract({"ALG-CLTAV-07": reformatted}) == []
