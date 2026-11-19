"""Phase A simulated-IUT harness: faults, truth isolation, reset, clock."""

from __future__ import annotations

import ast
import sys
import types
from fractions import Fraction
from pathlib import Path

import pytest

from a615a_sim.bound_iut.protocol import PROTOCOL_EVENT_WHITELIST, SimulatedTarget
from a615a_sim.clock import (
    ClosedInterval,
    DECLARED_OBSERVATION_END_S,
    FIND_ANSWER_LATE_AT_S,
    FIND_ANSWER_NORMAL_AT_S,
    FIND_HOST_ANSWER_S,
    FIND_OBSERVATION_END_S,
    INFORMATION_OBSERVATION_END_S,
    SIMULATED_EPSILON,
    STATUS_EXCEPTION_DELAY_S,
    SimulatedClock,
    declared_observation_end,
    find_host_requirement,
    t5_interval_verdict,
)
from a615a_sim.algorithm.hypothesis_model import public_hypothesis_ids
from a615a_sim.algorithm.library import STOP_CLASSES
from a615a_sim.evaluator import (
    evaluator_fault_record,
    get_truth,
    invoke_callable,
    issue_truth_capability,
    new_independent_truth_store,
    write_confirmed_truth,
)
from a615a_sim.evaluator.harness import confirm_then_overlay, run_registered_arms
from a615a_sim.evaluator.guard import TruthLeakageError
from a615a_sim.evaluator.reset import reset_target
from a615a_sim.faults.catalogue import (
    entry_by_id,
    evaluator_fault_plan,
    h_single_entries,
    in_domain_hypotheses_for_scene,
    load_catalogue,
    locate_scenes,
)
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
    assert found["kind"] == "FIND-ANSWER" and found["label"] == "SIMULATED-IUT"
    assert found["tick"] == str(FIND_ANSWER_NORMAL_AT_S)
    assert sent["kind"] == "COMPLETED"
    assert aborted["kind"] == "ABORT"
    assert info["kind"] == "COMPLETED"
    assert found["observationInterval"]["unit"] == "second"


def test_catalogue_declares_h_single_and_normal() -> None:
    catalogue = load_catalogue()
    ids = {entry["id"] for entry in h_single_entries()}
    assert catalogue["normal"]["id"] == "H-NORMAL"
    assert catalogue["normal"]["hypothesisId"] == "h_normal"
    assert catalogue["normal"]["inHSingle"] is False
    assert "sceneId" not in catalogue["normal"]
    assert ids == {
        "F-FIND-ANSWER-LATE",
        "F-FIND-ANSWER-ABSENT",
        "F-LUR-ACK-MISSING",
        "F-LUR-ACK-WITHOUT-WRQ",
        "F-STATUS-SILENCE",
    }
    tokens = [entry["confirmationToken"] for entry in h_single_entries()]
    assert len(tokens) == len(set(tokens))
    pair = catalogue["decEquivCandidates"][0]["pair"]
    assert pair == ["F-FIND-ANSWER-LATE", "F-FIND-ANSWER-ABSENT"]
    assert catalogue["decEquivCandidates"][0]["status"] == "OPEN"
    for entry in h_single_entries():
        assert entry["observableSignature"]
        assert entry["mechanism"]
        assert entry["confirmationToken"]
        assert entry["basisIds"]
        assert entry["expectedT5OrHalt"]
        assert entry["applicableScenes"]
        assert "sceneId" not in entry
        assert entry["inHSingle"] is True
    assert catalogue["normal"]["confirmationToken"] == "H-NORMAL"


@pytest.mark.parametrize(("scene_id", "fault_id"), list(evaluator_fault_plan()))
def test_confirmed_injection_writes_truth_before_any_arm(scene_id: str, fault_id: str) -> None:
    target = _target()
    reset = reset_target(target, pairing_id="PAIR-PHASE-A")
    assert reset.confirmed
    capability = issue_truth_capability()
    store = new_independent_truth_store()
    attempt = inject(
        target,
        scene_id=scene_id,
        fault_id=fault_id,
        truth_store=store,
        truth_capability=capability,
    )
    assert attempt.injection_confirmed is True
    assert attempt.injection_unconfirmed is False
    record = get_truth(store, attempt.attempt_id, capability)
    assert record.attempt_id == attempt.attempt_id
    assert record.confirmation_ref == f"INJ-{attempt.attempt_id}"


def test_unconfirmed_injection_cannot_become_truth() -> None:
    target = _target()
    reset_target(target)
    attempt = inject(
        target, scene_id="SC-NORMAL-UPLOAD", fault_id="F-LUR-ACK-MISSING", confirm=False
    )
    assert attempt.injection_confirmed is False
    assert attempt.injection_unconfirmed is True
    store = new_independent_truth_store()
    capability = issue_truth_capability()
    with pytest.raises(ValueError, match="unconfirmed"):
        write_confirmed_truth(store, attempt, capability)


def test_reset_evidence_is_distinct_per_attempt() -> None:
    target = _target()
    first = reset_target(target, pairing_id="PAIR-1")
    inject(target, scene_id="SC-NORMAL-UPLOAD", fault_id="F-LUR-ACK-MISSING")
    second = reset_target(target, pairing_id="PAIR-1")
    assert first.pairing_id == second.pairing_id
    assert first.reset_id != second.reset_id
    assert first.reset_evidence_ref != second.reset_evidence_ref
    assert second.confirmed
    assert second.snapshot["state"] == "IDLE"
    assert "faultId" not in second.snapshot


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
    assert host.lower == Fraction(0)
    assert host.upper == FIND_HOST_ANSWER_S == Fraction(2)
    assert t5_interval_verdict(ClosedInterval(Fraction(0), Fraction(2)), host) == "PASS"
    end = declared_observation_end()
    assert end == DECLARED_OBSERVATION_END_S == FIND_OBSERVATION_END_S
    assert end > FIND_HOST_ANSWER_S + SIMULATED_EPSILON
    info_end = declared_observation_end("INFORMATION")
    assert info_end == INFORMATION_OBSERVATION_END_S
    assert info_end > STATUS_EXCEPTION_DELAY_S + SIMULATED_EPSILON
    import a615a_sim.clock as clock_mod

    assert not hasattr(clock_mod, "find_registration_requirement")
    assert not hasattr(clock_mod, "FIND_REGISTRATION_S")


def test_algorithm_module_read_fails_closed() -> None:
    store = new_independent_truth_store()
    capability = issue_truth_capability()
    probe = types.ModuleType("cltav_runtime.fake_arm")
    probe.__name__ = "cltav_runtime.fake_arm"
    exec(
        "def steal(store, capability):\n    return store.get('missing', capability)\n",
        probe.__dict__,
    )
    sys.modules["cltav_runtime.fake_arm"] = probe
    try:
        with pytest.raises(TruthLeakageError, match="algorithm/arm"):
            probe.steal(store, capability)
    finally:
        del sys.modules["cltav_runtime.fake_arm"]


def test_unclassified_caller_fails_closed() -> None:
    store = new_independent_truth_store()
    capability = issue_truth_capability()
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
        from a615a_sim.evaluator import guard as guard_mod

        original = guard_mod.inspect.stack

        def _empty_stack(*_args, **_kwargs):
            return []

        guard_mod.inspect.stack = _empty_stack
        try:
            with pytest.raises(TruthLeakageError, match="not an evaluator"):
                store.get("missing", capability)
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


def test_no_module_outside_allowlist_imports_truth() -> None:
    src_root = Path(__file__).resolve().parents[2] / "src"
    offenders: list[str] = []
    for path in src_root.rglob("*.py"):
        relative = path.relative_to(src_root)
        parts = relative.parts
        if len(parts) >= 2 and parts[0] == "a615a_sim" and parts[1] in {"evaluator", "faults"}:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            modules: list[str] = []
            if isinstance(node, ast.Import):
                modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.append(node.module)
            if any(
                module == "a615a_sim.evaluator.truth"
                or module.startswith("a615a_sim.evaluator.truth.")
                for module in modules
            ):
                offenders.append(relative.as_posix())
                break
    assert offenders == []


def test_unlisted_module_called_from_evaluator_frame_is_denied() -> None:
    store = new_independent_truth_store()
    capability = issue_truth_capability()
    probe = types.ModuleType("experiment_arms.fake")
    probe.__name__ = "experiment_arms.fake"
    exec(
        "def read_truth(store, capability):\n    return store.get('missing', capability)\n",
        probe.__dict__,
    )
    sys.modules["experiment_arms.fake"] = probe
    try:
        with pytest.raises(TruthLeakageError):
            invoke_callable(probe.read_truth, store, capability)
    finally:
        del sys.modules["experiment_arms.fake"]


def test_arm_holding_target_cannot_call_evaluator_fault_record() -> None:
    target = _target()
    reset_target(target)
    inject(target, scene_id="SC-NORMAL-UPLOAD", fault_id="F-FIND-ANSWER-LATE")
    capability = issue_truth_capability()
    probe = types.ModuleType("a615a_sim.algorithm.fake_arm")
    probe.__name__ = "a615a_sim.algorithm.fake_arm"
    exec(
        "def steal(fn, target, capability):\n    return fn(target, capability)\n",
        probe.__dict__,
    )
    sys.modules["a615a_sim.algorithm.fake_arm"] = probe
    try:
        with pytest.raises(TruthLeakageError, match="algorithm/arm"):
            invoke_callable(probe.steal, evaluator_fault_record, target, capability)
    finally:
        del sys.modules["a615a_sim.algorithm.fake_arm"]


def test_access_without_capability_is_denied() -> None:
    store = new_independent_truth_store()
    with pytest.raises(TruthLeakageError, match="capability"):
        get_truth(store, "missing")
    target = _target()
    reset_target(target)
    attempt = inject(target, scene_id="SC-NORMAL-UPLOAD", fault_id="F-LUR-ACK-MISSING")
    with pytest.raises(TruthLeakageError, match="capability"):
        write_confirmed_truth(store, attempt)
    with pytest.raises(TruthLeakageError, match="capability"):
        evaluator_fault_record(target)


def test_locate_scenes_have_at_least_two_in_domain_hypotheses() -> None:
    for scene_id in locate_scenes():
        hypotheses = in_domain_hypotheses_for_scene(scene_id)
        assert "H-NORMAL" in hypotheses
        assert len(hypotheses) >= 2, scene_id


def test_inapplicable_scene_fault_pair_is_rejected() -> None:
    target = _target()
    reset_target(target)
    with pytest.raises(ValueError, match="inapplicable"):
        inject(target, scene_id="SC-NO-RESPONSE", fault_id="F-FIND-ANSWER-LATE")
    with pytest.raises(ValueError, match="inapplicable"):
        inject(target, scene_id="SC-NORMAL-UPLOAD", fault_id="F-STATUS-SILENCE")
    with pytest.raises(ValueError, match="inapplicable"):
        inject(target, scene_id="SC-SAME-KEY", fault_id="F-LUR-ACK-MISSING")


def test_scene_id_does_not_uniquely_determine_truth() -> None:
    scene_id = "SC-NORMAL-UPLOAD"
    capability = issue_truth_capability()
    store = new_independent_truth_store()
    first = inject(
        _target(),
        scene_id=scene_id,
        fault_id="h_normal",
        truth_store=store,
        truth_capability=capability,
    )
    second = inject(
        _target(),
        scene_id=scene_id,
        fault_id="F-FIND-ANSWER-LATE",
        truth_store=store,
        truth_capability=capability,
    )
    assert get_truth(store, first.attempt_id, capability).truth_hypothesis == "h_normal"
    assert (
        get_truth(store, second.attempt_id, capability).truth_hypothesis
        == "h_find_answer_late"
    )


def test_late_and_absent_signatures_differ_under_declared_observation_window() -> None:
    assert FIND_ANSWER_LATE_AT_S > FIND_HOST_ANSWER_S
    assert FIND_ANSWER_LATE_AT_S < declared_observation_end()
    late = inject(_target(), scene_id="SC-NORMAL-UPLOAD", fault_id="F-FIND-ANSWER-LATE")
    absent = inject(_target(), scene_id="SC-NORMAL-UPLOAD", fault_id="F-FIND-ANSWER-ABSENT")
    assert late.observed_signature == "FIND-ANSWER-LATE"
    assert absent.observed_signature == "FIND-ANSWER-ABSENT"
    assert late.observed_signature != absent.observed_signature
    late_target = _target()
    inject(late_target, scene_id="SC-WAIT-CONTINUE", fault_id="F-FIND-ANSWER-LATE")
    late_event = next(event for event in late_target.events if event.kind == "FIND-ANSWER")
    late_obs = late_target.clock.observation_interval(late_event.tick)
    assert t5_interval_verdict(late_obs, find_host_requirement()) == "FAIL"
    absent_target = _target()
    inject(absent_target, scene_id="SC-ABORT", fault_id="F-FIND-ANSWER-ABSENT")
    assert all(event.kind != "FIND-ANSWER" for event in absent_target.events)
    assert absent_target.clock.now == declared_observation_end("FIND")


def test_wait_abort_and_batch_are_h_normal_trajectories() -> None:
    wait = _target()
    inject(wait, scene_id="SC-WAIT-CONTINUE", fault_id="H-NORMAL")
    kinds = {event.kind for event in wait.events}
    assert {"WAIT", "CONTINUE"} <= kinds
    abort = _target()
    inject(abort, scene_id="SC-ABORT", fault_id="h_normal")
    assert any(event.kind == "ABORT" for event in abort.events)
    batch = _target()
    inject(batch, scene_id="SC-SINGLE-BATCH", fault_id="H-NORMAL")
    assert batch.configuration == "BATCH"


def test_status_silence_does_not_suppress_abort_fallback() -> None:
    target = _target()
    inject(target, scene_id="SC-NO-RESPONSE", fault_id="F-STATUS-SILENCE")
    kinds = [event.kind for event in target.events]
    assert "STATUS" in kinds
    assert "STATUS-SILENCE" not in kinds
    assert kinds[-1] == "ABORT"
    assert all("abortFallback" not in event.payload for event in target.events)
    assert target.clock.now >= INFORMATION_OBSERVATION_END_S


VERDICT_FIELD_DENYLIST = frozenset(
    {
        "afterHostDeadline",
        "hostAnswerInWindow",
        "thAck",
        "matchingWrqReceived",
        "invariant",
        "haltedAtObservationEnd",
        "abortFallback",
        "faultId",
        "hostAnswer",
        "beforeObservationEnd",
        "owned",
    }
)

FAULT_OR_HYPOTHESIS_IDS = frozenset(
    {
        "F-FIND-ANSWER-LATE",
        "F-FIND-ANSWER-ABSENT",
        "F-LUR-ACK-MISSING",
        "F-LUR-ACK-WITHOUT-WRQ",
        "F-STATUS-SILENCE",
        "H-NORMAL",
        "h_normal",
        "h_find_answer_late",
        "h_find_answer_absent",
        "h_lur_ack_missing",
        "h_lur_ack_without_wrq",
        "h_status_silence",
        "FIND-ANSWER-LATE",
        "FIND-ANSWER-ABSENT",
        "LUR-ACK-MISSING",
        "LUR-ACK-WITHOUT-WRQ",
        "STATUS-SILENCE",
        "STATUS-WITH-DELAY",
    }
)


def _flatten(value: object) -> str:
    return repr(value)


@pytest.mark.parametrize(("scene_id", "fault_id"), list(evaluator_fault_plan()))
def test_algorithm_visible_stream_has_no_truth_or_verdict_fields(scene_id: str, fault_id: str) -> None:
    target = _target()
    reset_target(target)
    inject(target, scene_id=scene_id, fault_id=fault_id)
    records = target.algorithm_visible_records()
    snapshot = target.snapshot()
    assert "faultId" not in snapshot
    kinds = {record["kind"] for record in records}
    assert kinds <= PROTOCOL_EVENT_WHITELIST
    blob = _flatten(records) + _flatten(snapshot)
    for forbidden in FAULT_OR_HYPOTHESIS_IDS:
        assert forbidden not in blob
    for record in records:
        assert "state" not in record
        assert not (VERDICT_FIELD_DENYLIST & set(record.keys()))
        assert not (VERDICT_FIELD_DENYLIST & set(record["payload"].keys()))
    capability = issue_truth_capability()
    evaluator = evaluator_fault_record(target, capability)
    if fault_id not in {"H-NORMAL", "h_normal"}:
        assert evaluator["faultId"] == fault_id
    assert not hasattr(target, "evaluator_fault_record")


def test_two_faults_in_one_scene_differ_only_by_timing_presence_or_order() -> None:
    scene_id = "SC-NORMAL-UPLOAD"
    streams: dict[str, list[tuple[str, str]]] = {}
    payloads: dict[str, list[frozenset[str]]] = {}
    for fault_id in ("H-NORMAL", "F-FIND-ANSWER-LATE", "F-FIND-ANSWER-ABSENT"):
        target = _target()
        reset_target(target)
        inject(target, scene_id=scene_id, fault_id=fault_id)
        records = target.algorithm_visible_records()
        streams[fault_id] = [(record["kind"], record["tick"]) for record in records]
        payloads[fault_id] = [frozenset(record["payload"].keys()) for record in records]
        assert {kind for kind, _tick in streams[fault_id]} <= PROTOCOL_EVENT_WHITELIST
    assert streams["H-NORMAL"] != streams["F-FIND-ANSWER-LATE"]
    assert streams["F-FIND-ANSWER-LATE"] != streams["F-FIND-ANSWER-ABSENT"]
    normal_kinds = [kind for kind, _tick in streams["H-NORMAL"] if kind.startswith("FIND")]
    late_kinds = [kind for kind, _tick in streams["F-FIND-ANSWER-LATE"] if kind.startswith("FIND")]
    assert normal_kinds == late_kinds == ["FIND-REQUEST-RECEIVED", "FIND-ANSWER"]
    normal_answer = next(tick for kind, tick in streams["H-NORMAL"] if kind == "FIND-ANSWER")
    late_answer = next(tick for kind, tick in streams["F-FIND-ANSWER-LATE"] if kind == "FIND-ANSWER")
    assert normal_answer != late_answer
    assert "FIND-ANSWER" not in {kind for kind, _tick in streams["F-FIND-ANSWER-ABSENT"]}
    lur_missing = _target()
    lur_unmatched = _target()
    inject(lur_missing, scene_id=scene_id, fault_id="F-LUR-ACK-MISSING")
    inject(lur_unmatched, scene_id=scene_id, fault_id="F-LUR-ACK-WITHOUT-WRQ")
    missing_kinds = [event.kind for event in lur_missing.events]
    unmatched_kinds = [event.kind for event in lur_unmatched.events]
    assert "LUR-WRQ" in missing_kinds and "LUR-ACK" not in missing_kinds
    assert "LUR-ACK" in unmatched_kinds and "LUR-WRQ" not in unmatched_kinds


def test_catalogue_declares_observation_ends_per_scene_family() -> None:
    catalogue = load_catalogue()
    find_end = catalogue["identity"]["observationEnds"]["FIND"]
    info_end = catalogue["identity"]["observationEnds"]["INFORMATION"]
    assert find_end["endS"] == str(FIND_OBSERVATION_END_S)
    assert info_end["endS"] == str(INFORMATION_OBSERVATION_END_S)
    assert "2 s" in find_end["justification"]
    assert "10 s" in info_end["justification"]


def test_normal_find_answer_tick_differs_from_late_only() -> None:
    normal = _target()
    late = _target()
    inject(normal, scene_id="SC-NORMAL-UPLOAD", fault_id="H-NORMAL")
    inject(late, scene_id="SC-NORMAL-UPLOAD", fault_id="F-FIND-ANSWER-LATE")
    normal_answer = next(event for event in normal.events if event.kind == "FIND-ANSWER")
    late_answer = next(event for event in late.events if event.kind == "FIND-ANSWER")
    assert normal_answer.tick == FIND_ANSWER_NORMAL_AT_S
    assert late_answer.tick == FIND_ANSWER_LATE_AT_S
    assert normal_answer.tick < FIND_HOST_ANSWER_S < late_answer.tick


def test_confirmation_traces_never_reach_algorithm_visible_records() -> None:
    target = _target()
    capability = issue_truth_capability()
    store = new_independent_truth_store()
    confirm_then_overlay(
        target,
        scene_id="SC-NORMAL-UPLOAD",
        fault_id="F-FIND-ANSWER-LATE",
        truth_store=store,
        capability=capability,
        pairing_id="PAIR-TRACE",
    )
    assert target.algorithm_visible_records() == []
    assert target.events == ()
    ledgers = run_registered_arms(
        target,
        scene_id="SC-NORMAL-UPLOAD",
        fault_id="F-FIND-ANSWER-LATE",
        truth_store=store,
        capability=capability,
        pairing_id="PAIR-TRACE-RUN",
    )
    for run in ledgers.values():
        blob = repr(run.as_mapping())
        assert "corr-" not in blob
        for record in run.observation_log:
            correlation = record.get("correlationId") or ""
            assert not str(correlation).startswith("corr-")


def _in_domain_plan() -> list[tuple[str, str, str]]:
    rows = []
    for scene_id, fault_id in evaluator_fault_plan():
        hypothesis = entry_by_id(fault_id).get("hypothesisId")
        if hypothesis in public_hypothesis_ids():
            rows.append((scene_id, fault_id, str(hypothesis)))
    return rows


@pytest.mark.parametrize(("scene_id", "fault_id", "truth_hypothesis"), _in_domain_plan())
def test_cl_loop_and_cl_ta_retain_evaluator_truth(scene_id: str, fault_id: str, truth_hypothesis: str) -> None:
    target = _target()
    capability = issue_truth_capability()
    store = new_independent_truth_store()
    ledgers = run_registered_arms(
        target,
        scene_id=scene_id,
        fault_id=fault_id,
        truth_store=store,
        capability=capability,
        resource_mode="ROUNDS",
        remaining=8,
    )
    for arm_id in ("CL-LOOP", "CL-TA"):
        run = ledgers[arm_id]
        assert truth_hypothesis in run.candidate_hypotheses
        assert run.stop_class in STOP_CLASSES
        assert "faultId" not in repr(run.as_mapping())


def test_cl_loop_shrinks_candidate_set_on_h_single() -> None:
    target = _target()
    capability = issue_truth_capability()
    store = new_independent_truth_store()
    ledgers = run_registered_arms(
        target,
        scene_id="SC-NORMAL-UPLOAD",
        fault_id="F-FIND-ANSWER-LATE",
        truth_store=store,
        capability=capability,
    )
    initial = public_hypothesis_ids()
    loop = ledgers["CL-LOOP"].candidate_hypotheses
    assert "h_find_answer_late" in loop
    assert len(loop) < len(initial)
    assert set(loop) < set(initial)
