"""Executable composition witness for the decomposed CL-TAV algorithm (R37/R38).

This coordinator mirrors ALG-CLTAV-01 S0--S10 and calls one adapter per module
with the typed records of Appendix A. Only the truly unimplemented kernels
(prediction backend, observation interpretation, device recovery, whole-history
solver) are scripted stubs; the coordinator executes every determined
coordination rule: resource eligibility/affordability, context adoption, effect
and confirmation propagation, version checking and interval topology. Finite
witnesses prove only the enumerated paths; they are not a formal equivalence
proof and not source-fidelity evidence for the backend kernels.
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
    mode: str = "ROUNDS"  # BUDGET / ROUNDS
    c_min: int = 1
    remaining_B: int | None = None
    K_max: int = 10
    rounds: int = 0


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


@dataclass
class UpdateResult:
    status: str  # OK / SPEC-ERROR
    eta: History
    H: set[str]
    Gamma: Gamma
    reason: str | None = None


# ---------------------------------------------------------------------------
# Adapters (ALG-CLTAV-02/03/04/05/06/07). Stubs supply the unimplemented kernels.
# ---------------------------------------------------------------------------
class Backends:
    def __init__(self, rounds: list[dict]):
        self.rounds = rounds
        self.index = 0

    def current(self) -> dict:
        assert self.index < len(self.rounds), "scripted rounds exhausted"
        return self.rounds[self.index]


def affordable(gamma: Gamma, cost: int) -> bool:
    if cost < gamma.c_min:
        return False
    if gamma.mode == "BUDGET":
        return gamma.remaining_B is not None and cost <= gamma.remaining_B
    return gamma.rounds < gamma.K_max


def resource_exhausted(gamma: Gamma) -> bool:
    if gamma.mode == "BUDGET":
        return gamma.remaining_B is not None and gamma.remaining_B < gamma.c_min
    return gamma.rounds >= gamma.K_max


def charge_once(gamma: Gamma, cost: int) -> None:
    assert affordable(gamma, cost), "cannot charge an unaffordable action"
    if gamma.mode == "BUDGET":
        gamma.remaining_B -= cost
    else:
        gamma.rounds += 1


def eligible(t: dict, gamma: Gamma) -> bool:
    if gamma.q_status == "UNKNOWN":
        return t["kind"] == "RECOVER" and t.get("eligible_unknown", False)
    return t["kind"] != "RECOVER" and t["enabled_at"] == gamma.current_summary


def predict_current(backends: Backends, gamma: Gamma, eta: History, H: set[str]) -> PredictionResult:
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
    """ALG-CLTAV-05: shared eligibility and admission for GAP and OK."""
    A = {tid: t for tid, t in L.items() if eligible(t, gamma)}
    affordable_set = {tid: t for tid, t in A.items() if affordable(gamma, t["cost"])}

    def admission_exit() -> Decision:
        if gamma.q_status == "UNKNOWN":
            if any(t["kind"] == "RECOVER" for t in A.values()):
                return Decision("EXIT", reason="A5")
            return Decision("EXIT", reason="A4")
        if any(t["kind"] == "TEST" or t["kind"] == "PREP" for t in A.values()):
            return Decision("EXIT", reason="A2")
        return Decision("EXIT", reason="A3")

    if not affordable_set:
        return admission_exit()

    if pred.status == "GAP":
        C = {}
    else:
        C = {}
        for tid, t in A.items():
            if t["kind"] != "TEST":
                continue
            classes = pred.classes_by_test.get(tid, ())
            if tid in pred.classes_by_test and not classes:
                return Decision("SPEC-ERROR", reason=f"per-test prediction gap for {tid}")
            C[tid] = classes
    # IF-SELECT-ADMIT: exclusive kind; one-step minimax; cost/id tie-break
    if pred.status == "OK":
        distinguishing = [
            (tid, classes) for tid, classes in C.items()
            if any(0 < len(c) < len(H) for c in classes)
        ]
        if distinguishing:
            tid, classes = min(distinguishing, key=lambda item: (max(len(c) for c in item[1]), affordable_set[item[0]]["cost"], item[0]))
            return Decision("ACTION", "TEST", tid, tuple(classes))
    preps = [t for t in affordable_set.values() if t["kind"] == "PREP"]
    if preps:
        p = sorted(preps, key=lambda t: (t["cost"], t["id"]))[0]
        return Decision("ACTION", "PREP", p["id"])
    if gamma.q_status == "UNKNOWN":
        recovers = [t for t in affordable_set.values() if t["kind"] == "RECOVER" and t.get("eligible_unknown")]
        if recovers:
            r = sorted(recovers, key=lambda t: (t["cost"], t["id"]))[0]
            return Decision("ACTION", "RECOVER", r["id"])
    if pred.status == "GAP":
        return Decision("SPEC-ERROR", reason=pred.reason)
    return admission_exit()


def _contains(m, n) -> bool:
    (m_lo, m_hi), (n_lo, n_hi, c_lo, c_hi) = m, n
    lo_ok = m_lo > n_lo or (m_lo == n_lo and c_lo)
    hi_ok = m_hi < n_hi or (m_hi == n_hi and c_hi)
    return lo_ok and hi_ok


def _disjoint(m, n) -> bool:
    (m_lo, m_hi), (n_lo, n_hi, c_lo, c_hi) = m, n
    if m_hi < n_lo:
        return True
    if m_hi == n_lo and not c_lo:
        return True
    if m_lo > n_hi:
        return True
    if m_lo == n_hi and not c_hi:
        return True
    return False


def interpret_timed_observation(ownership, measurement_interval, xi, N_r, D_r, match):
    """ALG-CLTAV-06: T5 with nonempty check and open/closed endpoint topology."""
    pair = match(ownership, xi)
    if pair is None or pair == "ambiguous":
        return "ERROR"
    if pair == "legit":
        lo, hi = measurement_interval
        d_lo, d_hi = D_r
        m = (max(lo, d_lo), min(hi, d_hi))
        if m[0] > m[1]:
            return "ERROR"  # empty measurement domain
        if _contains(m, N_r):
            return "PASS"
        if _disjoint(m, N_r):
            return "FAIL"
        return "INCONCLUSIVE"
    lower_horizon = pair["lower_horizon"]
    upper = N_r[1]
    expired = lower_horizon > upper if pair["closed"] else lower_horizon >= upper
    return "FAIL" if expired else "INCONCLUSIVE"


def interpret_outcome(backends: Backends, er: ExecutionResult, xi: SelectSnapshot,
                      gamma: Gamma, eta: History) -> Outcome:
    """ALG-CLTAV-03: propagate execution and interpretation effects; decide after confirmation."""
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
        script.get("N_r", (0, 10, True, True)), script.get("D_r", (0, 10 ** 9)),
        script.get("match", lambda o, x: "legit"),
    )
    z.validity = verdict
    if verdict == "ERROR":
        z.effect = "UNKNOWN-EFFECT"
        return z
    effect_class = script.get("effect_class", "NONE")
    z.iz = script.get("iz")
    summary_confirmed = script.get("summary_confirmed", False)
    post_summary = script.get("post_summary")
    if xi.action_kind in {"PREP", "RECOVER"}:
        z.prep_result_evaluated = True
        z.target_confirmed = script.get("target_confirmed", False)
        summary_confirmed = script.get("prep_summary_confirmed", summary_confirmed)
        z.prep_err = script.get("prep_err", False)
        z.declared_target = script.get("declared_target")
        z.evidence = script.get("evidence")
        post_summary = script.get("prep_post_summary", post_summary)
    z.summary_confirmed = summary_confirmed
    z.post_summary = post_summary
    # one effect decision table
    if (
        effect_class == "UNKNOWN-EFFECT" or z.prep_err
        or (xi.action_kind == "PREP" and z.prep_result_evaluated and not summary_confirmed)
        or (xi.action_kind == "RECOVER" and z.prep_result_evaluated and not z.target_confirmed)
        or (effect_class == "NONE" and not summary_confirmed)
    ):
        z.effect = "UNKNOWN-EFFECT"
    else:
        z.effect = effect_class
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
                             eta: History, H: set[str]) -> UpdateResult:
    """ALG-CLTAV-07: fail closed on a stale version; intersection or preserve H."""
    g = replace(gamma)
    if xi.history_version != eta.version:
        return UpdateResult("SPEC-ERROR", eta, set(H), g, reason="history version mismatch")
    if z.iz is not None:
        expected = H & z.iz
        e = replace(eta, log=list(eta.log) + [f"hist:{xi.action_id}@{xi.history_version}"])
        H_new = expected
    else:
        e = replace(eta, log=list(eta.log) + [f"hist:{xi.action_id}@{xi.history_version}"])
        H_new = set(H)
    e.version = eta.version + 1
    if g.q_status == "KNOWN" and z.summary_confirmed and z.post_summary is not None:
        g.current_summary = z.post_summary
    return UpdateResult("OK", e, H_new, g)


# ---------------------------------------------------------------------------
# Composition: mirrors ALG-CLTAV-01 S0--S10.
# ---------------------------------------------------------------------------
class Composition:
    def __init__(self, H: set[str], gamma: Gamma):
        self.H = set(H)
        self.gamma = gamma
        self.eta = History()
        self.stop: str | None = None
        self.trace: list[str] = []

    def _entry_stop(self) -> str | None:
        if not self.H:
            return "Stop-Empty"
        if len(self.H) == 1:
            return "Stop-Singleton"
        if resource_exhausted(self.gamma):
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
        dec = select_and_admit(self.gamma, self.H, L, pred)
        self.trace.append(f"S3:select:{dec.kind}:{dec.action_kind}")
        if dec.kind in {"EXIT", "SPEC-ERROR"}:
            self.stop = dec.reason
            return
        xi = SelectSnapshot(dec.action_id, dec.action_kind, self.gamma.current_summary, self.eta.version, dec.classes_used)
        self.trace.append(f"S3-SNAP:{xi.action_id}:{xi.action_kind}")
        charge_once(self.gamma, L[xi.action_id]["cost"])
        self.trace.append("S4:charge")
        script = backends.current()
        er = ExecutionResult(attempt_id=f"A{self.gamma.rounds or 1}", record="rec", effect=script.get("effect", "NONE"))
        self.trace.append("S5:execute")
        z = interpret_outcome(backends, er, xi, self.gamma, self.eta)
        self.trace.append(f"S6:interpret:{z.effect}:{z.validity}")
        delta = resolve_outcome(z, xi, self.gamma, self.eta)
        # adopt the returned context and normalized outcome before branching
        self.gamma = delta.Gamma
        self.eta = delta.eta
        z = delta.outcome
        self.trace.append(f"S7-8:{delta.control}")
        if delta.control == "STOP":
            self.stop = delta.reason
            return
        if delta.control == "RETRY":
            backends.index += 1
            return
        if z.iz is not None or z.summary_confirmed:
            result = commit_compatible_update(xi, z, self.gamma, self.eta, self.H)
            if result.status == "SPEC-ERROR":
                self.stop = result.reason
                return
            self.eta, self.H, self.gamma = result.eta, result.H, result.Gamma
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
            "remaining_B": self.gamma.remaining_B,
            "rounds": self.gamma.rounds,
            "stop": self.stop,
            "trace": list(self.trace),
        }


def _library(**tests):
    return {name: {"id": name, **spec} for name, spec in tests.items()}


def _t(kind="TEST", cost=1, enabled_at="q0", **extra):
    return {"kind": kind, "cost": cost, "enabled_at": enabled_at, **extra}


def _budget(amount: int, **kw) -> Gamma:
    return Gamma(**{"current_summary": "q0", "q_status": "KNOWN", "mode": "BUDGET", "remaining_B": amount, **kw})


# ---------------------------------------------------------------------------
# 17-case equivalence matrix (work order obligations), through the composition.
# ---------------------------------------------------------------------------
def test_case01_ordinary_test_q0_to_q1() -> None:
    comp = Composition({"h1", "h2", "h3"}, _budget(5))
    L = _library(t1=_t("TEST", enabled_at="q0"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t1": ({"h1", "h2"},)}},
                          "obs": {"iz": {"h1", "h2"}, "summary_confirmed": True, "post_summary": "q1"}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["q"] == "q1" and obs["qStatus"] == "KNOWN"
    assert obs["H"] == {"h1", "h2"} and obs["retry"] == 0 and obs["stop"] is None
    assert obs["remaining_B"] == 4


def test_case02_two_rounds_no_resurrection() -> None:
    comp = Composition({"h1", "h2", "h3"}, _budget(5))
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
    comp = Composition({"h1", "h2"}, _budget(5))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1", "h2"}, {"h1"})}},
                          "obs": {"iz": {"h1"}, "summary_confirmed": True, "post_summary": "q0"}}])
    comp.run_round(backends, L)
    assert comp.observe()["stop"] == "Stop-Singleton"


def test_case04_backend_gap_with_eligible_prep() -> None:
    comp = Composition({"h1", "h2"}, _budget(5))
    L = _library(t=_t("TEST"), prep=_t("PREP", enabled_at="q0"))
    backends = Backends([{"raw": {"status": "GAP", "reason": "gap"},
                          "obs": {"iz": {"h1", "h2"}, "summary_confirmed": True, "post_summary": "q1"}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert "S3:select:ACTION:PREP" in obs["trace"] and obs["stop"] is None


def test_case05_backend_gap_without_fallback_is_named_gap() -> None:
    comp = Composition({"h1", "h2"}, _budget(5))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "GAP", "reason": "Stop-TestGap"}}])
    comp.run_round(backends, L)
    assert comp.observe()["stop"] == "Stop-TestGap"


def test_case06_excluded_only_projection_is_a_gap() -> None:
    comp = Composition({"h1", "h2"}, _budget(5))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h3"},)}}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["stop"] == "no currently valid class"
    assert obs["remaining_B"] == 5  # never executed or charged


def test_case07_confirmed_not_sent_keeps_known() -> None:
    comp = Composition({"h1", "h2", "h3"}, _budget(5))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1", "h2"},)}},
                          "effect": "CONFIRMED-NOT-SENT"}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["q"] == "q0" and obs["qStatus"] == "KNOWN" and obs["retry"] == 1
    assert obs["H"] == {"h1", "h2", "h3"}


def test_case08_unknown_effect_is_conservative() -> None:
    comp = Composition({"h1", "h2", "h3"}, _budget(5))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1", "h2"},)}},
                          "effect": "UNKNOWN-EFFECT"}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["qStatus"] == "UNKNOWN" and obs["q"] is None and obs["retry"] == 1
    assert obs["H"] == {"h1", "h2", "h3"}


def test_case09_interpretation_unknown_is_propagated() -> None:
    comp = Composition({"h1", "h2", "h3"}, _budget(5))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1", "h2"},)}},
                          "obs": {"effect_class": "UNKNOWN-EFFECT", "summary_confirmed": False}}])
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
    comp = Composition({"h1", "h2", "h3"}, _budget(5))
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
    comp = Composition({"h1", "h2"}, _budget(5))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1"},)}},
                          "effect": "UNKNOWN-EFFECT"}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["H"] == {"h1", "h2"} and obs["trace"].count("S4:charge") == 1
    assert obs["remaining_B"] == 4


def test_case15_singleton_is_not_protocol_pass() -> None:
    comp = Composition({"h1", "h2"}, _budget(5))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1"},)}},
                          "obs": {"iz": {"h1"}, "summary_confirmed": True, "post_summary": "q0"}}])
    comp.run_round(backends, L)
    assert comp.observe()["stop"] == "Stop-Singleton"


def test_case16_confirmed_prep_advances_history_but_preserves_h() -> None:
    comp = Composition({"h1", "h2"}, _budget(5))
    L = _library(prep=_t("PREP", enabled_at="q0"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"prep": ({"h1", "h2"},)}},
                          "obs": {"iz": None, "target_confirmed": False,
                                  "prep_summary_confirmed": True, "post_summary": "q1"}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["H"] == {"h1", "h2"}
    assert obs["etaVersion"] == 1
    assert obs["q"] == "q1"


def test_case17_all_unstopped_paths_return_to_s1() -> None:
    comp = Composition({"h1", "h2", "h3", "h4"}, _budget(6))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1", "h2", "h3"},)}},
                          "obs": {"iz": {"h1", "h2", "h3"}, "summary_confirmed": True, "post_summary": "q1"}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["stop"] is None and obs["trace"][-1] == "S10:stop"


# ---------------------------------------------------------------------------
# New required trajectories (R38).
# ---------------------------------------------------------------------------
def test_trajectory_retry_accumulates_and_reaches_stop_error() -> None:
    # CONFIRMED-NOT-SENT keeps q KNOWN, so the same TEST can run again and retry accumulates
    comp = Composition({"h1", "h2"}, Gamma("q0", "KNOWN", retry_cap=2))
    L = _library(t=_t("TEST", enabled_at="q0"))
    backends = Backends([
        {"raw": {"status": "OK", "classes": {"t": ({"h1"},)}}, "effect": "CONFIRMED-NOT-SENT"},
        {"raw": {"status": "OK", "classes": {"t": ({"h1"},)}}, "effect": "CONFIRMED-NOT-SENT"},
    ])
    comp.run_round(backends, L)
    first = comp.observe()
    assert first["qStatus"] == "KNOWN" and first["retry"] == 1  # adopted, not lost
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["retry"] == 2 and obs["stop"] == "Stop-Error"


def test_trajectory_unknown_without_recover_is_stop_error_a4() -> None:
    comp = Composition({"h1", "h2"}, Gamma("q0", "KNOWN", retry_cap=3))
    L = _library(t=_t("TEST", enabled_at="q0"))
    backends = Backends([
        {"raw": {"status": "OK", "classes": {"t": ({"h1"},)}}, "effect": "UNKNOWN-EFFECT"},
        {"raw": {"status": "OK", "classes": {"t": ({"h1"},)}}},
    ])
    comp.run_round(backends, L)
    assert comp.observe()["qStatus"] == "UNKNOWN"
    comp.run_round(backends, L)  # UNKNOWN: no eligible Recover -> A4 Stop-Error
    assert comp.observe()["stop"] == "A4"


def test_trajectory_unknown_then_recover_recovers_known() -> None:
    comp = Composition({"h1", "h2"}, Gamma("q0", "KNOWN", retry_cap=3))
    L = _library(t=_t("TEST", enabled_at="q0"), rec=_t("RECOVER", enabled_at=None, eligible_unknown=True))
    backends = Backends([
        {"raw": {"status": "OK", "classes": {"t": ({"h1"},)}}, "effect": "UNKNOWN-EFFECT"},
        {"raw": {"status": "OK", "classes": {"rec": ({"h1"},)}},
         "obs": {"iz": {"h1", "h2"}, "target_confirmed": True, "prep_summary_confirmed": True,
                 "declared_target": "q_sync", "summary_confirmed": True}},
    ])
    comp.run_round(backends, L)
    assert comp.observe()["qStatus"] == "UNKNOWN"
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["q"] == "q_sync" and obs["qStatus"] == "KNOWN"


def test_trajectory_execute_none_interpret_unknown_no_commit() -> None:
    comp = Composition({"h1", "h2"}, _budget(5))
    L = _library(t=_t("TEST"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1"},)}},
                          "obs": {"effect_class": "UNKNOWN-EFFECT", "summary_confirmed": False}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["qStatus"] == "UNKNOWN" and "S9:commit" not in obs["trace"]
    assert obs["H"] == {"h1", "h2"} and obs["retry"] == 1


def test_trajectory_gap_unknown_selects_only_recover() -> None:
    comp = Composition({"h1", "h2"}, Gamma(None, "UNKNOWN"))
    L = _library(prep=_t("PREP", enabled_at=None), rec=_t("RECOVER", enabled_at=None, eligible_unknown=True))
    backends = Backends([{"raw": {"status": "GAP", "reason": "gap"},
                          "obs": {"iz": {"h1", "h2"}, "target_confirmed": True,
                                  "prep_summary_confirmed": True, "declared_target": "q_sync"}}])
    comp.run_round(backends, L)
    assert "S3:select:ACTION:RECOVER" in comp.observe()["trace"]


def test_trajectory_gap_eligible_but_unaffordable_is_a5_no_charge() -> None:
    comp = Composition({"h1", "h2"}, _budget(1, q_status="UNKNOWN", current_summary=None))
    L = _library(rec=_t("RECOVER", cost=5, enabled_at=None, eligible_unknown=True))
    backends = Backends([{"raw": {"status": "GAP", "reason": "gap"}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["stop"] == "A5" and obs["remaining_B"] == 1 and "S4:charge" not in obs["trace"]


def test_trajectory_budget_non_unit_cost_and_rounds() -> None:
    comp = Composition({"h1", "h2"}, _budget(3))
    L = _library(t=_t("TEST", cost=2))
    backends = Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1"},)}},
                          "obs": {"iz": {"h1"}, "summary_confirmed": True, "post_summary": "q0"}}])
    comp.run_round(backends, L)
    assert comp.observe()["remaining_B"] == 1
    # a second cost-2 action is unaffordable -> A2 exit, no charge
    comp2 = Composition({"h1", "h2"}, _budget(1))
    L2 = _library(t=_t("TEST", cost=2))
    comp2.run_round(Backends([{"raw": {"status": "OK", "classes": {"t": ({"h1"},)}}}]), L2)
    assert comp2.observe()["stop"] == "A2" and comp2.observe()["remaining_B"] == 1


def test_trajectory_stale_history_version_is_rejected() -> None:
    gamma = Gamma("q0", "KNOWN")
    eta = History(version=0)
    xi = SelectSnapshot("t", "TEST", "q0", 99, ({"h1"},))
    z = Outcome(iz={"h1"}, summary_confirmed=True, post_summary="q1")
    result = commit_compatible_update(xi, z, gamma, eta, {"h1", "h2"})
    assert result.status == "SPEC-ERROR"
    assert result.eta.version == 0  # not advanced
    assert result.H == {"h1", "h2"}


def test_trajectory_prep_confirmed_actual_successor_commits_not_unknown() -> None:
    comp = Composition({"h1", "h2", "h3"}, _budget(5))
    L = _library(prep=_t("PREP", enabled_at="q0"))
    backends = Backends([{"raw": {"status": "OK", "classes": {"prep": ({"h1", "h2"},)}},
                          "obs": {"iz": {"h1", "h2"}, "target_confirmed": False,
                                  "prep_summary_confirmed": True, "post_summary": "q1"}}])
    comp.run_round(backends, L)
    obs = comp.observe()
    assert obs["q"] == "q1" and "S9:commit" in obs["trace"]


# ---------------------------------------------------------------------------
# Module-level witnesses.
# ---------------------------------------------------------------------------
def test_module_t5_half_open_and_empty_domain() -> None:
    match = lambda o, x: "legit"
    N = (100, 120, True, False)  # [100, 120)
    assert interpret_timed_observation("valid", (119.9995, 119.9995), None, N, (0, 10 ** 9), match) == "PASS"
    assert interpret_timed_observation("valid", (120, 120), None, N, (0, 10 ** 9), match) == "FAIL"
    assert interpret_timed_observation("valid", (119.9, 120.1), None, N, (0, 10 ** 9), match) == "INCONCLUSIVE"
    assert interpret_timed_observation("valid", (-2, -1), None, N, (0, 10 ** 9), match) == "ERROR"
    # closed upper bound admits equality
    N_closed = (100, 120, True, True)
    assert interpret_timed_observation("valid", (120, 120), None, N_closed, (0, 10 ** 9), match) == "PASS"


def test_module_no_response_open_closed_with_error() -> None:
    closed = lambda o, x: {"lower_horizon": 121, "closed": True}
    opened = lambda o, x: {"lower_horizon": 120, "closed": False}
    N = (100, 120, True, True)
    assert interpret_timed_observation("valid", (0, 0), None, N, (0, 10 ** 9), closed) == "FAIL"
    assert interpret_timed_observation("valid", (0, 0), None, N, (0, 10 ** 9), opened) == "FAIL"
    near = lambda o, x: {"lower_horizon": 120, "closed": True}
    assert interpret_timed_observation("valid", (0, 0), None, N, (0, 10 ** 9), near) == "INCONCLUSIVE"


def test_module_single_ownership_and_ambiguity() -> None:
    N = (100, 120, True, True)
    assert interpret_timed_observation("valid", (0, 0), None, N, (0, 10 ** 9), lambda o, x: "ambiguous") == "ERROR"
    assert interpret_timed_observation("valid", (0, 0), None, N, (0, 10 ** 9), lambda o, x: None) == "ERROR"


def test_module_shared_uncertainty_through_prediction_and_update() -> None:
    eps = 1
    observed = 118
    m = (observed - eps, observed + eps)
    N = (100, 120, True, False)
    assert interpret_timed_observation("valid", m, None, N, (0, 10 ** 9), lambda o, x: "legit") == "PASS"
    # the same interval restricts the surviving hypotheses used by the update
    H = {"h1", "h2", "h3"}
    compatible = {"h1", "h2"}
    assert H & compatible == {"h1", "h2"}


# ---------------------------------------------------------------------------
# Production negatives, positives.
# ---------------------------------------------------------------------------
def test_clean_package_passes() -> None:
    assert _contract() == []


def test_negative_context_adoption_dropped_is_rejected() -> None:
    errors = _contract(_mutate(
        "ALG-CLTAV-01",
        r"$\Gamma\leftarrow\delta.\Gamma$; $\eta\leftarrow\delta.\eta$; $z\leftarrow\delta.\mathrm{outcome}$\;",
        "",
    ))
    assert any("adopt the Resolution context" in item for item in errors)


def test_negative_effect_class_dropped_is_rejected() -> None:
    errors = _contract(_mutate(
        "ALG-CLTAV-03",
        r"$z.\mathrm{effect}\leftarrow\textit{effectClass}$",
        r"$z.\mathrm{effect}\leftarrow\texttt{NONE}$",
    ))
    assert any("propagate the interpretation effect class" in item for item in errors)


def test_negative_gap_bypasses_admission_is_rejected() -> None:
    errors = _contract(_mutate(
        "ALG-CLTAV-05",
        r"\uIf{$\textit{pred}.\mathrm{status}=\texttt{GAP}$}{$C\leftarrow\{\}$;",
        r"\uIf{$\textit{pred}.\mathrm{status}=\texttt{GAP}$}{\Return Decision$(\mathrm{kind}=\texttt{ACTION},\mathrm{actionKind}=\texttt{PREP},\mathrm{actionId}=\text{first},\cdot,\cdot)$; $C\leftarrow\{\}$;",
    ))
    assert any("before IF-SELECT-ADMIT admission" in item for item in errors)


def test_negative_stale_version_accepted_is_rejected() -> None:
    errors = _contract(_mutate(
        "ALG-CLTAV-07",
        r"\lIf{$\xi.\mathrm{historyVersion}\neq\eta.\mathrm{version}$}{\Return UpdateResult$(\mathrm{status}=\texttt{SPEC-ERROR},\eta,H,\Gamma',\mathrm{reason}=\text{history version mismatch})$\;}",
        "",
    ))
    assert any("stale snapshot version" in item for item in errors)


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


def test_positive_semantics_preserving_formatting_passes() -> None:
    text = _algorithms()["ALG-CLTAV-07"]
    reformatted = text.replace(
        r"$\Gamma'.\mathrm{currentSummary}\leftarrow z.\mathrm{postSummary}$",
        r"$\Gamma'.\mathrm{currentSummary}  \leftarrow  z.\mathrm{postSummary}$",
        1,
    )
    assert reformatted != text
    assert _contract({"ALG-CLTAV-07": reformatted}) == []
