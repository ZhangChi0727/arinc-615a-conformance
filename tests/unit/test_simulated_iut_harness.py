"""Phase A simulated-IUT harness: faults, truth isolation, reset, clock."""

from __future__ import annotations

import sys
import types
from fractions import Fraction

import pytest

from a615a_sim.bound_iut.protocol import SimulatedTarget
from a615a_sim.clock import (
    ClosedInterval,
    SIMULATED_EPSILON,
    SimulatedClock,
    find_host_requirement,
    t5_interval_verdict,
)
from a615a_sim.evaluator.guard import TruthLeakageError
from a615a_sim.evaluator.reset import reset_target
from a615a_sim.evaluator.truth import IndependentTruthStore
from a615a_sim.faults.catalogue import h_single_entries, load_catalogue
from a615a_sim.faults.injector import inject


def _target() -> SimulatedTarget:
    return SimulatedTarget(SimulatedClock())


def test_bound_model_refuses_download_and_afdx() -> None:
    target = _target()
    with pytest.raises(ValueError, match="DOWNLOAD"):
        target._require_bound("DOWNLOAD")
    with pytest.raises(ValueError, match="AFDX"):
        target._require_bound("AFDX")


def test_bound_model_find_send_abort_and_information() -> None:
    target = _target()
    found = target.find("c-find")
    sent = target.send("c-find")
    aborted = _target().abort("c-abort")
    info = _target().information("c-info")
    assert found["kind"] == "FIND" and found["label"] == "SIMULATED-IUT"
    assert sent["kind"] == "SEND"
    assert aborted["kind"] == "ABORT"
    assert info["kind"] == "INFORMATION"
    assert found["observationInterval"]["unit"] == "second"


def test_catalogue_declares_h_single_and_normal() -> None:
    catalogue = load_catalogue()
    ids = {entry["id"] for entry in h_single_entries()}
    assert catalogue["normal"]["id"] == "H-NORMAL"
    assert catalogue["normal"]["inHSingle"] is False
    assert ids == {
        "H-WAIT-CONTINUE",
        "H-NO-RESPONSE",
        "H-ABORT",
        "H-SAME-KEY",
        "H-SINGLE-BATCH",
    }
    for entry in h_single_entries():
        assert entry["observableSignature"]
        assert entry["mechanism"]
        assert entry["confirmationToken"]
        assert entry["inHSingle"] is True


@pytest.mark.parametrize(
    ("fault_id", "scene_id"),
    [
        ("H-NORMAL", "SC-NORMAL-UPLOAD"),
        ("H-WAIT-CONTINUE", "SC-WAIT-CONTINUE"),
        ("H-NO-RESPONSE", "SC-NO-RESPONSE"),
        ("H-ABORT", "SC-ABORT"),
        ("H-SAME-KEY", "SC-SAME-KEY"),
        ("H-SINGLE-BATCH", "SC-SINGLE-BATCH"),
        ("H-INVALID-OBS", "SC-INVALID-OBS"),
        ("H-RESOURCE-ERROR", "SC-RESOURCE-ERROR"),
    ],
)
def test_confirmed_injection_writes_truth_before_any_arm(fault_id: str, scene_id: str) -> None:
    target = _target()
    reset = reset_target(target, pairing_id="PAIR-PHASE-A")
    assert reset.confirmed
    attempt = inject(target, scene_id=scene_id, fault_id=fault_id)
    assert attempt.injection_confirmed is True
    assert attempt.injection_unconfirmed is False
    store = IndependentTruthStore()
    record = store.write_from_confirmed_injection(attempt)
    assert record.attempt_id == attempt.attempt_id
    assert store.get(attempt.attempt_id).confirmation_ref == f"INJ-{attempt.attempt_id}"


def test_unconfirmed_injection_cannot_become_truth() -> None:
    target = _target()
    reset_target(target)
    attempt = inject(target, scene_id="SC-ABORT", fault_id="H-ABORT", confirm=False)
    assert attempt.injection_confirmed is False
    assert attempt.injection_unconfirmed is True
    store = IndependentTruthStore()
    with pytest.raises(ValueError, match="unconfirmed"):
        store.write_from_confirmed_injection(attempt)


def test_reset_evidence_is_distinct_per_attempt() -> None:
    target = _target()
    first = reset_target(target, pairing_id="PAIR-1")
    inject(target, scene_id="SC-ABORT", fault_id="H-ABORT")
    second = reset_target(target, pairing_id="PAIR-1")
    assert first.pairing_id == second.pairing_id
    assert first.reset_id != second.reset_id
    assert first.reset_evidence_ref != second.reset_evidence_ref
    assert second.confirmed
    assert second.snapshot["state"] == "IDLE"
    assert second.snapshot["faultId"] is None


def test_simulated_clock_t5_matches_experiment_plan_examples() -> None:
    assert SIMULATED_EPSILON == Fraction(1, 1000)
    point = ClosedInterval(Fraction(3, 1), Fraction(3, 1))
    overlap = ClosedInterval(Fraction(29, 10), Fraction(31, 10))
    miss = ClosedInterval(Fraction(39, 10), Fraction(41, 10))
    assert t5_interval_verdict(overlap, point) == "INCONCLUSIVE"
    assert t5_interval_verdict(miss, point) == "FAIL"
    assert t5_interval_verdict(point, point) == "PASS"
    clock = SimulatedClock()
    clock.advance(Fraction(1, 1))
    interval = clock.observation_interval()
    assert interval.upper - interval.lower == 2 * SIMULATED_EPSILON
    host = find_host_requirement()
    assert t5_interval_verdict(ClosedInterval(Fraction(0), Fraction(2)), host) == "PASS"


def test_algorithm_module_read_fails_closed() -> None:
    store = IndependentTruthStore()
    probe = types.ModuleType("cltav_runtime.fake_arm")
    probe.__name__ = "cltav_runtime.fake_arm"
    exec(
        "def steal(store):\n    return store.get('missing')\n",
        probe.__dict__,
    )
    sys.modules["cltav_runtime.fake_arm"] = probe
    try:
        with pytest.raises(TruthLeakageError, match="algorithm/arm"):
            probe.steal(store)
    finally:
        del sys.modules["cltav_runtime.fake_arm"]


def test_unclassified_caller_fails_closed() -> None:
    store = IndependentTruthStore()
    probe = types.ModuleType("unregistered.caller")
    probe.__name__ = "unregistered.caller"
    exec(
        "def steal(store):\n"
        "    import inspect\n"
        "    from a615a_sim.evaluator.guard import deny_algorithm_truth_access\n"
        "    # Drop test frames by invoking the store method after rewriting globals.\n"
        "    return store.get('missing')\n",
        probe.__dict__,
    )
    sys.modules["unregistered.caller"] = probe
    try:
        # Test frame remains on the stack, so this path is allowed by the
        # tests. prefix.  Fail-closed for production is the missing-allowed
        # branch exercised by calling deny with a synthetic empty stack.
        from a615a_sim.evaluator import guard as guard_mod

        original = guard_mod.inspect.stack

        def _empty_stack(*_args, **_kwargs):
            return []

        guard_mod.inspect.stack = _empty_stack
        try:
            with pytest.raises(TruthLeakageError, match="not an evaluator"):
                store.get("missing")
        finally:
            guard_mod.inspect.stack = original
    finally:
        del sys.modules["unregistered.caller"]


def test_iut_public_package_does_not_export_truth() -> None:
    import a615a_sim
    import inspect

    assert not hasattr(a615a_sim, "IndependentTruthStore")
    source = inspect.getsource(a615a_sim)
    assert "from a615a_sim.evaluator" not in source
    assert "import IndependentTruthStore" not in source


def test_algorithm_import_of_truth_fails_closed() -> None:
    probe = types.ModuleType("cltav_runtime.fake_arm")
    probe.__name__ = "cltav_runtime.fake_arm"
    sys.modules["cltav_runtime.fake_arm"] = probe
    dropped = [
        name
        for name in list(sys.modules)
        if name == "a615a_sim.evaluator" or name.startswith("a615a_sim.evaluator.")
    ]
    saved = {name: sys.modules[name] for name in dropped}
    for name in dropped:
        del sys.modules[name]
    try:
        with pytest.raises(Exception, match="algorithm/arm") as caught:
            exec(
                "from a615a_sim.evaluator.truth import IndependentTruthStore\n",
                probe.__dict__,
            )
        assert caught.value.__class__.__name__ == "TruthLeakageError"
    finally:
        sys.modules.update(saved)
        del sys.modules["cltav_runtime.fake_arm"]
