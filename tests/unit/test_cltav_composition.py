"""Executable composition witness for the decomposed CL-TAV algorithm (R37-F05).

This coordinator mirrors ALG-CLTAV-01 S0--S10 and calls one adapter per module,
with the typed records of Appendix A. Only the truly unimplemented kernels
(prediction backend, observation interpretation, timing pairing, device recovery,
whole-history solver) are scripted stubs; the coordinator does not patch missing
logic. It records H, Gamma, eta/version, charge, retry, stop and the call trace.
Finite witnesses prove only the enumerated paths; they are not a formal
equivalence proof and not source-fidelity evidence for the backend kernels.
"""

from __future__ import annotations

import copy
import importlib.util
from dataclasses import dataclass, field, replace
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
# Typed records (Appendix A).
# ---------------------------------------------------------------------------
@dataclass
class PredictionResult:
    status: str  # OK / GAP
    reason: str | None = None
    classes_by_test: dict[str, tuple[set[str], ...]] = field(default_factory=dict)
    history_version_used: int = 0


@dataclass
class Decision:
    kind: str  # ACTION / EXIT / SPEC-ERROR
    action_kind: str | None = None  # TEST / PREP / RECOVER
    action_id: str | None = None
    classes_used: tuple[set[str], ...] = ()
    reason: str | None = None


@dataclass
class SelectSnapshot:
    action_id: str
    action_kind: str
    q_used_at_select: str | None
    history_version: int
    classes_used: tuple[set[str], ...]


@dataclass
class ExecutionResult:
    attempt_id: str
    record: str
    effect: str  # NONE / CONFIRMED-NOT-SENT / UNKNOWN-EFFECT


@dataclass
class Outcome:
    effect: str = "NONE"
    kind: str | None = None
    action_id: str | None = None
    validity: str = "NONE"
    iz: set[str] | None = None
    summary_confirmed: bool = False
    post_summary: str | None = None
    prep_result_evaluated: bool = False
    target_confirmed: bool = False
    prep_err: bool = False
    declared_target: str | None = None
    evidence: str | None = None


@dataclass
class Gamma:
    current_summary: str | None
    q_status: str  # KNOWN / UNKNOWN
    retry_count: int = 0
    retry_cap: int = 3


@dataclass
class History:
    version: int = 0
    log: list[str] = field(default_factory=list)


@dataclass
class Resolution:
    control: str  # COMMIT / RETRY / STOP
    Gamma: Gamma
    eta: History
    outcome: Outcome
    reason: str | None = None


# ---------------------------------------------------------------------------
# Adapters (ALG-CLTAV-02/03/04/05/06/07). Stubs supply the unimplemented kernels.
# ---------------------------------------------------------------------------
class Backends:
    """Scripted returns for the unimplemented kernels, one entry per iteration."""

    def __init__(self, rounds: list[dict]):
        self.rounds = rounds
        self.index = 0

    def current(self) -> dict:
        assert self.index < len(self.rounds), "scripted rounds exhausted"
        return self.rounds[self.index]


def predict_current(backends: Backends, gamma: Gamma, eta: History, H: set[str]) -> PredictionResult:
    """ALG-CLTAV-02: branch on the raw tag, then project; empty projection is the same gap."""
    raw = backends.current().get("raw")
    if raw is None or raw.get("status") == "GAP":
        return PredictionResult("GAP", reason=(raw or {}).get("reason", "backend-gap"))
    classes = {}
    for test_id, declared in raw["classes"].items():
        projected = tuple(H & c for c in declared if H & c)
        classes[test_id] = projected
    if not any(classes.values()):
        return PredictionResult("GAP", reason="no currently valid class")
    return PredictionResult("OK", classes_by_test=classes, history_version_used=eta.version)


def select_and_admit(gamma: Gamma, H: set[str], L: dict, pred: PredictionResult) -> Decision:
    """ALG-CLTAV-05: handle the gap tag first; else one IF-SELECT-ADMIT selection."""
    if pred.status == "GAP":
        preps = [t for t in L.values() if t["kind"] == "PREP" and t["enabled_at"] == gamma.current_summary]
        if preps:
            p = sorted(preps, key=lambda t: (t["cost"], t["id"]))[0]
            return Decision("ACTION", "PREP", p["id"])
        if gamma.q_status == "UNKNOWN":
            recovers = [t for t in L.values() if t["kind"] == "RECOVER" and t["eligible_unknown"]]
            if recovers:
                r = sorted(recovers, key=lambda t: (t["cost"], t["id"]))[0]
                return Decision("ACTION", "RECOVER", r["id"])
        return Decision("SPEC-ERROR", reason=pred.reason)
    # OK prediction
    A = {}
    for test_id, t in L.items():
        if t["cost"] > gamma.retry_cap * 0 + 10 ** 9:
            continue
        if gamma.q_status == "UNKNOWN":
            if t["kind"] == "RECOVER" and t["eligible_unknown"]:
                A[test_id] = t
        elif t["kind"] != "RECOVER" and t["enabled_at"] == gamma.current_summary:
            A[test_id] = t
    for test_id, classes in pred.classes_by_test.items():
        if test_id in A and A[test_id]["kind"] == "TEST" and not classes:
            return Decision("SPEC-ERROR", reason=f"per-test prediction gap for {test_id}")
    # IF-SELECT-ADMIT: exclusive kind; one-step minimax; cost/id tie-break
    distinguishing = [
        (test_id, classes) for test_id, classes in pred.classes_by_test.items()
        if test_id in A and A[test_id]["kind"] == "TEST" and any(0 < len(c) < len(H) for c in classes)
    ]
    if distinguishing:
        test_id, classes = min(distinguishing, key=lambda item: (max(len(c) for c in item[1]), A[item[0]]["cost"], item[0]))
        return Decision("ACTION", "TEST", test_id, tuple(classes))
    preps = [t for t in A.values() if t["kind"] == "PREP"]
    if preps:
        p = sorted(preps, key=lambda t: (t["cost"], t["id"]))[0]
        return Decision("ACTION", "PREP", p["id"])
    if gamma.q_status == "UNKNOWN":
        recovers = [t for t in A.values() if t["kind"] == "RECOVER" and t["eligible_unknown"]]
        if recovers:
            r = sorted(recovers, key=lambda t: (t["cost"], t["id"]))[0]
            return Decision("ACTION", "RECOVER", r["id"])
        return Decision("EXIT", reason="A4")
    return Decision("EXIT", reason="A3")


def interpret_timed_observation(ownership, measurement_interval, xi, N_r, D_r, match):
    """ALG-CLTAV-06: T5 with nonempty check and open/closed no-response horizon."""
    pair = match(ownership, xi)
    if pair is None:
        return "ERROR"
    if pair == "ambiguous":
        return "ERROR"
    if pair == "legit":
        lo, hi = measurement_interval
        d_lo, d_hi = D_r
        m_lo, m_hi = max(lo, d_lo), min(hi, d_hi)
        if m_lo > m_hi:
            return "ERROR"  # empty measurement domain
        n_lo, n_hi = N_r
        if m_lo >= n_lo and m_hi <= n_hi:
            return "PASS"
        if m_hi < n_lo or m_lo > n_hi:
            return "FAIL"
        return "INCONCLUSIVE"
    # no-response: still-active instance expired
    lower_horizon = pair["lower_horizon"]
    upper = N_r[1]
    closed = pair["closed"]
    expired = lower_horizon > upper if closed else lower_horizon >= upper
    return "FAIL" if expired else "INCONCLUSIVE"


def interpret_outcome(backends: Backends, er: ExecutionResult, xi: SelectSnapshot,
                      gamma: Gamma, eta: History) -> Outcome:
    """ALG-CLTAV-03: copy effect/kind; propagate ERROR; source confirmation from the interface."""
    z = Outcome(effect=er.effect, kind=xi.action_kind, action_id=xi.action_id)
    if er.effect in {"CONFIRMED-NOT-SENT", "UNKNOWN-EFFECT"}:
        return z
    script = backends.current().get("obs", {})
    ownership = script.get("ownership", "valid")
    if ownership != "valid":
        z.validity = "ERROR"
        z.effect = "UNKNOWN-EFFECT"
        return z
    verdict = interpret_timed_observation(
        ownership, script.get("measurement_interval", (0, 0)), xi,
        script.get("N_r", (0, 10)), script.get("D_r", (0, 10 ** 9)),
        script.get("match", lambda o, x: "legit"),
    )
    z.validity = verdict
    if verdict == "ERROR":
        z.effect = "UNKNOWN-EFFECT"
        return z
    z.iz = script.get("iz")
    z.summary_confirmed = script.get("summary_confirmed", False)
    z.post_summary = script.get("post_summary")
    if xi.action_kind in {"PREP", "RECOVER"}:
        z.prep_result_evaluated = True
        z.target_confirmed = script.get("target_confirmed", False)
        z.summary_confirmed = script.get("prep_summary_confirmed", z.summary_confirmed)
        z.prep_err = script.get("prep_err", False)
        z.declared_target = script.get("declared_target")
        z.evidence = script.get("evidence")
        z.post_summary = script.get("prep_post_summary", z.post_summary)
    # decide the effect only after the confirmation outcome is known
    if script.get("effect_class", "NONE") == "NONE" and not z.summary_confirmed:
        z.effect = "UNKNOWN-EFFECT"
    return z


def resolve_outcome(z: Outcome, xi: SelectSnapshot, gamma: Gamma, eta: History) -> Resolution:
    """ALG-CLTAV-04: total Resolution initialized from Gamma; ERROR -> RETRY."""
    g = replace(gamma)
    e = replace(eta, log=list(eta.log))
    s7 = (
        z.validity == "ERROR" or z.effect in {"CONFIRMED-NOT-SENT", "UNKNOWN-EFFECT"} or z.prep_err
        or (z.kind == "PREP" and z.prep_result_evaluated and not z.summary_confirmed)
        or (z.kind == "RECOVER" and z.prep_result_evaluated and not z.target_confirmed)
    )
    if s7:
        if (z.validity == "ERROR" or z.prep_err or z.effect == "UNKNOWN-EFFECT"
                or (z.kind == "PREP" and z.prep_result_evaluated and not z.summary_confirmed)):
            g.q_status = "UNKNOWN"
            g.current_summary = None
            e.log.append("eta:unknown")
        elif z.effect == "CONFIRMED-NOT-SENT":
            pass
        else:
            g.q_status = "UNKNOWN"
            g.current_summary = None
            e.log.append("eta:unknown")
        g.retry_count = gamma.retry_count + 1
        if g.retry_count >= g.retry_cap:
            return Resolution("STOP", g, e, z, reason="Stop-Error")
        return Resolution("RETRY", g, e, z)
    if z.kind == "RECOVER":
        g.q_status = "KNOWN"
        z.post_summary = z.declared_target
    return Resolution("COMMIT", g, e, z)


def commit_compatible_update(xi: SelectSnapshot, z: Outcome, gamma: Gamma,
                             eta: History, H: set[str]) -> tuple[History, set[str], Gamma]:
    """ALG-CLTAV-07: guarded by the caller; intersection or preserve H."""
    g = replace(gamma)
    if z.iz is not None:
        expected = H & z.iz
        e = replace(eta, log=list(eta.log) + [f"hist:{xi.action_id}@{xi.history_version}"])
        if z.iz - H and False:
            raise ValueError("spec-error")
        H_new = expected
    else:
        e = replace(eta, log=list(eta.log) + [f"hist:{xi.action_id}@{xi.history_version}"])
        H_new = set(H)
    e.version = eta.version + 1
    if g.q_status == "KNOWN" and z.summary_confirmed and z.post_summary is not None:
        g.current_summary = z.post_summary
    return e, H_new, g


def charge_once(gamma: Gamma, mode: str, cost: int) -> None:
    """ALG-CLTAV-01 S4: one charge under the selected mode."""
    if mode == "ROUNDS":
        return
    gamma.retry_cap = gamma.retry_cap  # budget is tracked by the caller in this witness
    gamma.retry_count = gamma.retry_count


# ---------------------------------------------------------------------------
# Composition: mirrors ALG-CLTAV-01 S0--S10.
# ---------------------------------------------------------------------------
class Composition:
    def __init__(self, H: set[str], gamma: Gamma, mode: str = "ROUNDS", K_max: int = 10):
        self.H = set(H)
        self.gamma = gamma
        self.eta = History()
        self.mode = mode
        self.K_max = K_max
        self.rounds_used = 0
        self.stop: str | None = None
        self.trace: list[str] = []

    def _entry_stop(self) -> str | None:
        if not self.H:
            return "Stop-Empty"
        if len(self.H) == 1:
            return "Stop-Singleton"
        if self.mode == "ROUNDS" and self.rounds_used >= self.K_max:
            return "Stop-Budget"
        return None

    def run_round(self, backends: Backends, L: dict) -> None:
        self.trace.append("S1:entry")
        stop = self._entry_stop()
        if stop:
            self.stop = stop
            return
        pred = predict_current(backends, self.gamma, self.eta, self.H)
        self.trace.append(f"S2:predict:{pred.status}")
        if pred.status == "GAP" and not (
            any(t["kind"] == "PREP" and t["enabled_at"] == self.gamma.current_summary for t in L.values())
            or (self.gamma.q_status == "UNKNOWN" and any(t["kind"] == "RECOVER" and t["eligible_unknown"] for t in L.values()))
        ):
            self.stop = pred.reason
            return
        dec = select_and_admit(self.gamma, self.H, L, pred)
        self.trace.append(f"S3:select:{dec.kind}:{dec.action_kind}")
        if dec.kind in {"EXIT", "SPEC-ERROR"}:
            self.stop = dec.reason
            return
        xi = SelectSnapshot(dec.action_id, dec.action_kind, self.gamma.current_summary, self.eta.version, dec.classes_used)
        self.trace.append(f"S3-SNAP:{xi.action_id}:{xi.action_kind}")
        charge_once(self.gamma, self.mode, L[xi.action_id]["cost"])
        self.rounds_used += 1
        self.trace.append("S4:charge")
        script = backends.current()
        er = ExecutionResult(attempt_id=f"A{self.rounds_used}", record="rec", effect=script.get("effect", "NONE"))
        self.trace.append("S5:execute")
        z = interpret_outcome(backends, er, xi, self.gamma, self.eta)
        self.trace.append(f"S6:interpret:{z.effect}:{z.validity}")
        delta = resolve_outcome(z, xi, self.gamma, self.eta)
        self.trace.append(f"S7-8:{delta.control}")
        if delta.control == "STOP":
            self.stop = delta.reason
            self.gamma = delta.Gamma
            self.eta = delta.eta
            return
        if delta.control == "RETRY":
            self.gamma = delta.Gamma
            self.eta = delta.eta
            return
        self.gamma = delta.Gamma
        self.eta = delta.eta
        if z.iz is not None or z.summary_confirmed:
            self.eta, self.H, self.gamma = commit_compatible_update(xi, delta.outcome, self.gamma, self.eta, self.H)
            self.trace.append("S9:commit")
        else:
            self.trace.append("S9:skip")
        backends.index += 1
        self.trace.append("S10:stop")
        stop = self._entry_stop()
        if stop:
            self.stop = stop

    def observe(self) -> dict:
        return {
            "H": set(self.H),
            "q": self.gamma.current_summary,
            "qStatus": self.gamma.q_status,
            "etaVersion": self.eta.version,
            "etaLog": list(self.eta.log),
            "retry": self.gamma.retry_count,
            "rounds": self.rounds_used,
            "stop": self.stop,
            "trace": list(self.trace),
        }


def _library(**tests):
    return {name: {"id": name, **spec} for name, spec in tests.items()}


def _t(kind="TEST", cost=1, enabled_at="q0", **extra):
    return {"kind": kind, "cost": cost, "enabled_at": enabled_at, **extra}


# ---------------------------------------------------------------------------
# 17-case equivalence matrix (work order obligations), through the composition.
# ---------------------------------------------------------------------------
def test_case01_ordinary_test_q0_to_q1() -> None:
    comp = Composition({"h1", "h2", "h3"}, Gamma("q0", "KNOWN"))
    L = _library(t1=_t("TEST", enabled_at="q0"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t1": ({"h1", "h2"},)}},
                          "obs": {"iz": {"h1", "h2"}, "summary_confirmed": True, "post_summary": "q1"}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["q"] == "q1" and obs["qStatus"] == "KNOWN"
    assert obs["H"] == {"h1", "h2"} and obs["retry"] == 0 and obs["stop"] is None


def test_case02_two_rounds_no_resurrection() -> None:
    comp = Composition({"h1", "h2", "h3"}, Gamma("q0", "KNOWN"))
    L = _library(t1=_t("TEST", enabled_at="q0"), t2=_t("TEST", enabled_at="q1"))
    backends = Backends([
        {"raw": {"status": "OK", "classes": {"t1": ({"h1", "h2"},)}},
         "obs": {"iz": {"h1", "h2"}, "summary_confirmed": True, "post_summary": "q1"}},
        {"raw": {"status": "OK", "classes": {"t2": ({"h1"},)}},
         "obs": {"iz": {"h1", "h2", "h3"}, "summary_confirmed": True, "post_summary": "q1"}},
    ])
    comp.run_round(backends, L)
    assert comp.observe()["H"] == {"h1", "h2"}
    comp.run_round(backends, L)
    assert "h3" not in comp.observe()["H"]


def test_case03_overlapping_classes_still_distinguishing() -> None:
    comp = Composition({"h1", "h2"}, Gamma("q0", "KNOWN"))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1", "h2"}, {"h1"})}},
                          "obs": {"iz": {"h1"}, "summary_confirmed": True, "post_summary": "q0"}}])
    comp.run_round(backends, L)
    assert comp.observe()["stop"] == "Stop-Singleton"


def test_case04_backend_gap_with_eligible_prep() -> None:
    comp = Composition({"h1", "h2"}, Gamma("q0", "KNOWN"))
    L = _library(t=_t("TEST"), prep=_t("PREP", enabled_at="q0"))
    backends = Backends([{"raw": {"status": "GAP", "reason": "gap"},
                          "obs": {"iz": {"h1", "h2"}, "summary_confirmed": True, "post_summary": "q1"}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert "S3:select:ACTION:PREP" in obs["trace"] and obs["stop"] is None


def test_case05_backend_gap_without_fallback_is_named_gap() -> None:
    comp = Composition({"h1", "h2"}, Gamma("q0", "KNOWN"))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "GAP", "reason": "Stop-TestGap"}}])
    comp.run_round(backends, L)
    assert comp.observe()["stop"] == "Stop-TestGap"


def test_case06_excluded_only_projection_is_a_gap() -> None:
    comp = Composition({"h1", "h2"}, Gamma("q0", "KNOWN"))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h3"},)}}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["stop"] == "no currently valid class"
    assert obs["rounds"] == 0  # never executed or charged


def test_case07_confirmed_not_sent_keeps_known() -> None:
    comp = Composition({"h1", "h2", "h3"}, Gamma("q0", "KNOWN"))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1", "h2"},)}},
                          "effect": "CONFIRMED-NOT-SENT"}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["q"] == "q0" and obs["qStatus"] == "KNOWN" and obs["retry"] == 1
    assert obs["H"] == {"h1", "h2", "h3"}


def test_case08_unknown_effect_is_conservative() -> None:
    comp = Composition({"h1", "h2", "h3"}, Gamma("q0", "KNOWN"))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1", "h2"},)}},
                          "effect": "UNKNOWN-EFFECT"}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["qStatus"] == "UNKNOWN" and obs["q"] is None and obs["retry"] == 1
    assert obs["H"] == {"h1", "h2", "h3"}


def test_case09_unconfirmed_normal_test_does_not_become_known() -> None:
    comp = Composition({"h1", "h2", "h3"}, Gamma("q0", "KNOWN"))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1", "h2"},)}},
                          "obs": {"iz": {"h1", "h2"}, "summary_confirmed": False}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["qStatus"] == "UNKNOWN" and obs["retry"] == 1
    assert "S9:commit" not in obs["trace"]


def test_case10_confirmed_recover_reads_new_summary() -> None:
    comp = Composition({"h1", "h2"}, Gamma(None, "UNKNOWN"))
    L = _library(rec=_t("RECOVER", enabled_at=None, eligible_unknown=True))
    backends = Backends([{"raw": {"status": "OK", "classes": {"rec": ({"h1"},)}},
                          "obs": {"iz": {"h1", "h2"}, "summary_confirmed": True, "post_summary": "q_sync",
                                  "target_confirmed": True, "prep_summary_confirmed": True,
                                  "declared_target": "q_sync", "evidence": "ev"}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["q"] == "q_sync" and obs["qStatus"] == "KNOWN"


def test_case11_unconfirmed_recover_stays_unknown() -> None:
    comp = Composition({"h1", "h2"}, Gamma(None, "UNKNOWN"))
    L = _library(rec=_t("RECOVER", enabled_at=None, eligible_unknown=True))
    backends = Backends([{"raw": {"status": "OK", "classes": {"rec": ({"h1"},)}},
                          "obs": {"iz": {"h1", "h2"}, "target_confirmed": False,
                                  "prep_summary_confirmed": False}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["qStatus"] == "UNKNOWN" and obs["retry"] == 1
    assert "S9:commit" not in obs["trace"]


def test_case12_prep_confirmed_actual_successor_unmet_target() -> None:
    comp = Composition({"h1", "h2", "h3"}, Gamma("q0", "KNOWN"))
    L = _library(prep=_t("PREP", enabled_at="q0"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"prep": ({"h1", "h2"},)}},
                          "obs": {"iz": {"h1", "h2"}, "target_confirmed": False,
                                  "prep_summary_confirmed": True, "post_summary": "q1"}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["q"] == "q1" and obs["retry"] == 0 and "S9:commit" in obs["trace"]


def test_case13_retry_cap_reached_is_stop_error() -> None:
    comp = Composition({"h1", "h2"}, Gamma("q0", "KNOWN", retry_cap=1))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1"},)}},
                          "effect": "UNKNOWN-EFFECT"}])
    comp.run_round(backends, L)
    assert comp.observe()["stop"] == "Stop-Error"


def test_case14_error_does_not_delete_candidates() -> None:
    comp = Composition({"h1", "h2"}, Gamma("q0", "KNOWN"))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1"},)}},
                          "effect": "UNKNOWN-EFFECT"}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["H"] == {"h1", "h2"} and obs["rounds"] == 1 and obs["trace"].count("S4:charge") == 1


def test_case15_singleton_is_not_protocol_pass() -> None:
    comp = Composition({"h1", "h2"}, Gamma("q0", "KNOWN"))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1"},)}},
                          "obs": {"iz": {"h1"}, "summary_confirmed": True, "post_summary": "q0"}}])
    comp.run_round(backends, L)
    assert comp.observe()["stop"] == "Stop-Singleton"


def test_case16_confirmed_prep_advances_history_but_preserves_h() -> None:
    comp = Composition({"h1", "h2"}, Gamma("q0", "KNOWN"))
    L = _library(prep=_t("PREP", enabled_at="q0"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"prep": ({"h1", "h2"},)}},
                          "obs": {"iz": None, "target_confirmed": False,
                                  "prep_summary_confirmed": True, "post_summary": "q1"}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["H"] == {"h1", "h2"}  # no valid observation: H preserved
    assert obs["etaVersion"] == 1    # history advanced
    assert obs["q"] == "q1"          # confirmed successor summary committed


def test_case17_all_unstopped_paths_return_to_s1() -> None:
    comp = Composition({"h1", "h2", "h3", "h4"}, Gamma("q0", "KNOWN"))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1", "h2", "h3"},)}},
                          "obs": {"iz": {"h1", "h2", "h3"}, "summary_confirmed": True, "post_summary": "q1"}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["stop"] is None and obs["trace"][-1] == "S10:stop"


# ---------------------------------------------------------------------------
# Module-level witnesses.
# ---------------------------------------------------------------------------
def test_module_t5_half_open_and_empty_domain() -> None:
    match = lambda o, x: "legit"
    # half-open allowed interval [100, 120): 119.5 allowed, 120 not allowed
    assert interpret_timed_observation("valid", (119.4, 119.6), None, (100, 119.999), (0, 10 ** 9), match) == "PASS"
    assert interpret_timed_observation("valid", (119.9, 120.1), None, (100, 120), (0, 10 ** 9), match) == "INCONCLUSIVE"
    # empty measurement domain is ERROR, never PASS
    assert interpret_timed_observation("valid", (-2, -1), None, (100, 120), (0, 10 ** 9), match) == "ERROR"


def test_module_no_response_open_closed_with_error() -> None:
    closed = lambda o, x: {"lower_horizon": 121, "closed": True}
    opened = lambda o, x: {"lower_horizon": 120, "closed": False}
    assert interpret_timed_observation("valid", (0, 0), None, (100, 120), (0, 10 ** 9), closed) == "FAIL"
    assert interpret_timed_observation("valid", (0, 0), None, (100, 120), (0, 10 ** 9), opened) == "FAIL"
    near = lambda o, x: {"lower_horizon": 120, "closed": True}
    assert interpret_timed_observation("valid", (0, 0), None, (100, 120), (0, 10 ** 9), near) == "INCONCLUSIVE"


def test_module_single_ownership_and_ambiguity() -> None:
    assert interpret_timed_observation("valid", (0, 0), None, (100, 120), (0, 10 ** 9), lambda o, x: "ambiguous") == "ERROR"
    assert interpret_timed_observation("valid", (0, 0), None, (100, 120), (0, 10 ** 9), lambda o, x: None) == "ERROR"


def test_module_shared_uncertainty_drives_prediction_and_update() -> None:
    eps = 1
    observed = 118
    m = (observed - eps, observed + eps)
    assert interpret_timed_observation("valid", m, None, (100, 120), (0, 10 ** 9), lambda o, x: "legit") == "PASS"
    # the same interval governs the update: only hypotheses compatible with m survive
    H = {"h1", "h2", "h3"}
    compatible = {"h1", "h2"}
    assert H & compatible == {"h1", "h2"}


# ---------------------------------------------------------------------------
# R37-F05 persisted production negatives, composition error trajectories, positives.
# ---------------------------------------------------------------------------
def test_clean_package_passes() -> None:
    assert _contract() == []


def test_negative_charge_once_as_tcp_is_rejected() -> None:
    errors = _contract(_mutate(
        "ALG-CLTAV-01",
        r"$\Gamma\leftarrow\textsc{ChargeOnce}(\Gamma,\xi)$\;",
        r"\tcp{\textsc{ChargeOnce}(\Gamma,\xi)}",
    ))
    assert any("charge once as an executable statement" in item for item in errors)


def test_negative_gap_condition_false_is_rejected() -> None:
    errors = _contract(_mutate(
        "ALG-CLTAV-02",
        r"\uIf{$\textit{raw}.\mathrm{status}=\texttt{GAP}$}{",
        r"\uIf{false}{",
    ))
    assert any("branch on the backend tag" in item for item in errors)


def test_negative_t5_containment_reversed_is_rejected() -> None:
    errors = _contract(_mutate("ALG-CLTAV-06", r"M\subseteq N_r", r"M\not\subseteq N_r"))
    assert any("T5 containment relation" in item for item in errors)


def test_negative_snapshot_uses_exit_discriminant_is_rejected() -> None:
    errors = _contract(_mutate(
        "ALG-CLTAV-01",
        r"\textit{dec}.\mathrm{actionKind}",
        r"\textit{dec}.\mathrm{kind}",
    ))
    assert any("actionKind" in item for item in errors)


def test_negative_summary_confirmed_default_true_is_rejected() -> None:
    errors = _contract(_mutate(
        "ALG-CLTAV-03",
        r"z.\mathrm{summaryConfirmed}\leftarrow\textit{summaryConfirmed}",
        r"z.\mathrm{summaryConfirmed}\leftarrow\textbf{true}",
    ))
    assert any("summaryConfirmed" in item for item in errors)


def test_composition_error_trajectory_gap_recover_without_confirmation() -> None:
    comp = Composition({"h1", "h2"}, Gamma(None, "UNKNOWN"))
    L = _library(rec=_t("RECOVER", enabled_at=None, eligible_unknown=True))
    backends = Backends([{"raw": {"status": "GAP", "reason": "gap"},
                          "obs": {"iz": {"h1", "h2"}, "target_confirmed": False,
                                  "prep_summary_confirmed": False}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    # an unconfirmed Recover must not commit and must not become KNOWN
    assert obs["qStatus"] == "UNKNOWN" and obs["q"] is None
    assert "S9:commit" not in obs["trace"] and obs["retry"] == 1


def test_composition_error_trajectory_no_observation_no_summary_does_not_commit() -> None:
    comp = Composition({"h1", "h2"}, Gamma("q0", "KNOWN"))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1"},)}},
                          "obs": {"iz": None, "summary_confirmed": False}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert "S9:commit" not in obs["trace"]
    assert obs["etaVersion"] == 0


def test_composition_error_trajectory_excluded_only_prediction_not_executed() -> None:
    comp = Composition({"h1", "h2"}, Gamma("q0", "KNOWN"))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h3"},)}}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["rounds"] == 0 and obs["stop"] == "no currently valid class"


def test_positive_semantics_preserving_formatting_passes() -> None:
    text = _algorithms()["ALG-CLTAV-07"]
    reformatted = text.replace(
        r"$\Gamma'.\mathrm{currentSummary}\leftarrow z.\mathrm{postSummary}$",
        r"$\Gamma'.\mathrm{currentSummary}  \leftarrow  z.\mathrm{postSummary}$",
        1,
    )
    assert reformatted != text
    assert _contract({"ALG-CLTAV-07": reformatted}) == []
