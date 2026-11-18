"""Phase B four-arm adapter: behaviour, cost, visibility, ReferenceSession."""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

import pytest

from a615a_sim.algorithm.adapter import REGISTERED_ARMS, run_arm
from a615a_sim.algorithm.library import (
    ACTION_ANALYSIS,
    ACTION_LIBRARY,
    ACTION_TEST_FIND,
    ACTION_TEST_INFORMATION,
    ACTION_TEST_SEND,
    STOP_CLASSES,
    predetermined_test_sequence,
)
from a615a_sim.bound_iut.protocol import SimulatedTarget
from a615a_sim.clock import SimulatedClock
from a615a_sim.evaluator import (
    issue_truth_capability,
    new_independent_truth_store,
    run_registered_arms,
)
from a615a_sim.evaluator.guard import TruthLeakageError
from a615a_sim.evaluator.reset import reset_target
from a615a_sim.faults.catalogue import evaluator_fault_plan
from a615a_sim.faults.injector import overlay_declared_fault
from cltav_runtime.session import ReferenceSession


SRC = Path(__file__).resolve().parents[2] / "src"
ARM_ROOT = SRC / "a615a_sim" / "algorithm"


def _target() -> SimulatedTarget:
    return SimulatedTarget(SimulatedClock())


def test_arm_modules_do_not_import_evaluator_or_truth() -> None:
    offenders: list[str] = []
    for path in ARM_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            modules: list[str] = []
            if isinstance(node, ast.Import):
                modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.append(node.module)
            if any(
                module == "a615a_sim.evaluator"
                or module.startswith("a615a_sim.evaluator.")
                or "truth" in module.split(".")
                or module.endswith("fault_view")
                for module in modules
            ):
                offenders.append(path.relative_to(SRC).as_posix())
                break
    assert offenders == []


def test_arm_source_has_no_fault_plan_or_capability() -> None:
    blob = "\n".join(path.read_text(encoding="utf-8") for path in ARM_ROOT.rglob("*.py"))
    for forbidden in ("faultPlan", "TruthCapability", "issue_truth_capability", "evaluator_fault_record"):
        assert forbidden not in blob


def test_cl_loop_source_constructs_reference_session() -> None:
    source = (ARM_ROOT / "loop.py").read_text(encoding="utf-8")
    assert "from cltav_runtime.session import ReferenceSession" in source
    assert "ReferenceSession(" in source


@pytest.mark.parametrize(("scene_id", "fault_id"), [("SC-NORMAL-UPLOAD", "H-NORMAL"), ("SC-NO-RESPONSE", "F-STATUS-SILENCE")])
def test_four_arms_run_on_same_scene_fault(scene_id: str, fault_id: str) -> None:
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
    assert set(ledgers) == set(REGISTERED_ARMS)
    for arm_id, run in ledgers.items():
        assert run.arm_id == arm_id
        assert run.stop_class in STOP_CLASSES
        assert run.resource_mode == "ROUNDS"
        assert set(run.issued_actions) <= set(ACTION_LIBRARY)
        blob = repr(run.as_mapping())
        assert "faultPlan" not in blob
        assert "faultId" not in blob
        assert "TruthCapability" not in blob
        for record in run.observation_log:
            assert "state" not in record
            assert "faultId" not in record


def test_cl_t_predetermined_tests_charge_acquisition_only() -> None:
    target = _target()
    overlay_declared_fault(target, scene_id="SC-NORMAL-UPLOAD", fault_id="H-NORMAL")
    run = run_arm(
        "CL-T",
        target,
        scene_id="SC-NORMAL-UPLOAD",
        resource_mode="ROUNDS",
        remaining=8,
        correlation_id="t-normal",
    )
    assert run.issued_actions == [ACTION_TEST_FIND, ACTION_TEST_SEND]
    assert run.projected_cost()["acquisition"] == 2
    assert run.projected_cost()["computation"] == 0
    assert ACTION_ANALYSIS not in run.issued_actions
    assert run.observation_log[0]["kind"] in {"FIND-ANSWER", "FIND-REQUEST-RECEIVED"}


def test_cl_a_analysis_only_no_invented_acquisition() -> None:
    target = _target()
    overlay_declared_fault(target, scene_id="SC-NORMAL-UPLOAD", fault_id="H-NORMAL")
    before = list(target.algorithm_visible_records())
    run = run_arm(
        "CL-A",
        target,
        scene_id="SC-NORMAL-UPLOAD",
        resource_mode="BUDGET",
        remaining=8,
        correlation_id="a-normal",
    )
    assert run.issued_actions == [ACTION_ANALYSIS]
    assert run.projected_cost() == {
        "acquisition": 0,
        "computation": 1,
        "preparation": 0,
        "retry": 0,
    }
    assert run.observation_log == []
    assert target.algorithm_visible_records() == before
    assert run.analysis_notes["usedOwnObservationCount"] == 0
    assert "sceneId" in run.analysis_notes["usedInitialFields"]


def test_cl_ta_collect_then_analyse_no_adaptive_test() -> None:
    target = _target()
    overlay_declared_fault(target, scene_id="SC-NO-RESPONSE", fault_id="H-NORMAL")
    run = run_arm(
        "CL-TA",
        target,
        scene_id="SC-NO-RESPONSE",
        resource_mode="ROUNDS",
        remaining=8,
        correlation_id="ta-info",
    )
    assert run.issued_actions == [ACTION_TEST_INFORMATION, ACTION_ANALYSIS]
    assert run.projected_cost()["acquisition"] == 1
    assert run.projected_cost()["computation"] == 1
    tests_after_analysis = [
        action for action in run.issued_actions[run.issued_actions.index(ACTION_ANALYSIS) + 1 :]
        if action.startswith("TEST-")
    ]
    assert tests_after_analysis == []


def test_cl_loop_uses_reference_session() -> None:
    target = _target()
    overlay_declared_fault(target, scene_id="SC-NORMAL-UPLOAD", fault_id="H-NORMAL")
    run = run_arm(
        "CL-LOOP",
        target,
        scene_id="SC-NORMAL-UPLOAD",
        resource_mode="ROUNDS",
        remaining=8,
        correlation_id="loop-normal",
    )
    assert run.runtime_session_type == "ReferenceSession"
    assert run.runtime_session_type == ReferenceSession.__qualname__
    assert inspect.isclass(ReferenceSession)
    assert any(action in ACTION_LIBRARY for action in run.issued_actions) or run.stop_class in STOP_CLASSES
    assert run.stop_class in STOP_CLASSES


def test_other_arms_do_not_see_cl_loop_records() -> None:
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
    loop_log = ledgers["CL-LOOP"].observation_log
    for arm_id in ("CL-T", "CL-A", "CL-TA"):
        other = ledgers[arm_id].observation_log
        assert other is not loop_log
        if arm_id == "CL-A":
            assert other == []
        assert ledgers[arm_id].runtime_session_type is None


def test_arm_cannot_hold_truth_capability_from_harness() -> None:
    source = inspect.getsource(run_registered_arms)
    assert "run_arm(" in source
    assert "capability" not in inspect.getsource(run_arm)


def test_unaffordable_predetermined_test_is_stop_budget() -> None:
    target = _target()
    overlay_declared_fault(target, scene_id="SC-NORMAL-UPLOAD", fault_id="H-NORMAL")
    run = run_arm(
        "CL-T",
        target,
        scene_id="SC-NORMAL-UPLOAD",
        resource_mode="ROUNDS",
        remaining=0,
        correlation_id="t-broke",
    )
    assert run.stop_class == "Stop-Budget"
    assert run.issued_actions == []
    assert run.projected_cost()["acquisition"] == 0


def test_single_resource_mode_per_run() -> None:
    target = _target()
    overlay_declared_fault(target, scene_id="SC-WAIT-CONTINUE", fault_id="H-NORMAL")
    rounds = run_arm("CL-T", target, scene_id="SC-WAIT-CONTINUE", resource_mode="ROUNDS", remaining=8, correlation_id="r")
    reset_target(target)
    overlay_declared_fault(target, scene_id="SC-WAIT-CONTINUE", fault_id="H-NORMAL")
    budget = run_arm("CL-T", target, scene_id="SC-WAIT-CONTINUE", resource_mode="BUDGET", remaining=8, correlation_id="b")
    assert rounds.resource_mode == "ROUNDS"
    assert budget.resource_mode == "BUDGET"
    assert rounds.issued_actions == budget.issued_actions == list(predetermined_test_sequence({"serviceScope": "UPLOAD"}))


def test_evaluator_fault_plan_not_passed_to_adapter() -> None:
    source = inspect.getsource(run_arm)
    assert "fault_id" not in source
    assert "faultPlan" not in source
    plan = evaluator_fault_plan()
    assert plan


def test_algorithm_arm_cannot_import_evaluator_at_runtime() -> None:
    import sys
    import types

    probe = types.ModuleType("a615a_sim.algorithm.import_probe")
    probe.__name__ = "a615a_sim.algorithm.import_probe"
    sys.modules[probe.__name__] = probe
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
            exec("from a615a_sim.evaluator.truth import IndependentTruthStore\n", probe.__dict__)
        assert caught.value.__class__.__name__ == "TruthLeakageError" or isinstance(caught.value, TruthLeakageError)
    finally:
        sys.modules.update(saved)
        del sys.modules[probe.__name__]
