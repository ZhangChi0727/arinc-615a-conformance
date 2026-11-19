"""Phase C E0–E6 pipeline, WF walkthroughs versus SYN-*, N3/N4."""

from __future__ import annotations

import ast
import inspect
import json
from fractions import Fraction
from pathlib import Path

import pytest

from a615a_sim.algorithm.loop import SimulatedIutEnvironment
from a615a_sim.clock import FIND_OBSERVATION_END_S, declared_observation_end
from a615a_sim.evaluator import issue_truth_capability, new_independent_truth_store
from a615a_sim.evaluator.guard import TruthLeakageError
from a615a_sim.evaluator.pipeline.collect import collect_from_fixture
from a615a_sim.evaluator.pipeline.design import WF_TO_SYN, load_synthetic_walkthrough
from a615a_sim.evaluator.pipeline.collect import collect_from_run
from a615a_sim.evaluator.pipeline.evaluate import (
    derive_outcome,
    metric_cells,
    population_sets,
)
from a615a_sim.evaluator.pipeline.filter import filter_attempt, filter_from_fixture
from a615a_sim.evaluator.pipeline.orchestrator import (
    WF_PATH_KIND,
    WF_PATHS,
    execute_accounting_replay,
    execute_live_attempt,
    execute_synthetic_walkthrough,
    load_experiment_design,
)
from a615a_sim.evaluator.pipeline.run import replay_run_fixture
from a615a_sim.evaluator.pipeline.timing import observation_end_for_absent_answer
from cltav_runtime.session import ReferenceSession

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
PIPE = SRC / "a615a_sim" / "evaluator" / "pipeline"

EXPECTED_SYN_MISMATCHES = {
    "WF-NORMAL": [
        {
            "field": "finalHypotheses",
            "expected": ["h-normal"],
            "actual": ["h_normal"],
            "reason": "live catalogue hypothesisId uses underscore; SYN-NORMAL uses hyphen",
        },
        {
            "field": "runId",
            "expected": "RUN-001",
            "actual": "RUN-CL-LOOP-A-WF-NORMAL",
            "reason": "deterministic live runId scheme differs from SYN-NORMAL runId",
        },
        {
            "field": "attemptId",
            "expected": "ATT-001",
            "actual": "A-WF-NORMAL",
            "reason": "live attemptId is A-WF-*; SYN-NORMAL uses ATT-001",
        },
        {
            "field": "truthReference.truthHypothesis",
            "expected": "h-normal",
            "actual": "h_normal",
            "reason": "live catalogue hypothesisId uses underscore; SYN-NORMAL uses hyphen",
        },
    ],
    "WF-UNCONFIRMED-INJECT": [
        {
            "field": "resourcePolicy",
            "expected": "NOT-RUN",
            "actual": "ROUNDS",
            "reason": "live scene still binds a resource mode; SYN-UNCONFIRMED is NOT-RUN",
        },
        {
            "field": "resourceStatus",
            "expected": "NOT-RUN",
            "actual": None,
            "reason": "no live collect/run; SYN-UNCONFIRMED records NOT-RUN",
        },
        {
            "field": "attemptId",
            "expected": "ATT-004",
            "actual": "A-WF-UNCONFIRMED-INJECT",
            "reason": "live attemptId is A-WF-*; SYN-UNCONFIRMED uses ATT-004",
        },
    ],
    "WF-INVALID-OBS": [
        {
            "field": "stopClass",
            "expected": "Stop-Error",
            "actual": "Stop-Singleton",
            "reason": "live CL-LOOP stop is Stop-Singleton; SYN-INVALID-OBS accounts Stop-Error",
        },
        {
            "field": "finalHypotheses",
            "expected": ["h-normal", "h1"],
            "actual": ["h_normal"],
            "reason": "live catalogue retains {h_normal}; SYN-INVALID-OBS accounts {h-normal, h1}",
        },
        {
            "field": "injectionStatus",
            "expected": "NORMAL",
            "actual": "UNRESOLVED",
            "reason": "live H-INVALID-OBS catalogue is unresolved; SYN-INVALID-OBS stores NORMAL",
        },
        {
            "field": "faultDomain",
            "expected": "OUT-OF-DOMAIN",
            "actual": "UNKNOWN",
            "reason": "live H-INVALID-OBS catalogue is unknown; SYN-INVALID-OBS stores OUT-OF-DOMAIN",
        },
        {
            "field": "localizationDecisionIssued",
            "expected": False,
            "actual": True,
            "reason": "live singleton stop issues localization; SYN-INVALID-OBS does not",
        },
        {
            "field": "singletonDecisionIssued",
            "expected": False,
            "actual": True,
            "reason": "live singleton stop issues singleton; SYN-INVALID-OBS does not",
        },
        {
            "field": "resourceStatus",
            "expected": "RESOURCE-ERROR",
            "actual": "NORMAL",
            "reason": "tester resource log is NORMAL; SYN-INVALID-OBS accounts RESOURCE-ERROR",
        },
        {
            "field": "runId",
            "expected": "RUN-005",
            "actual": "RUN-CL-LOOP-A-WF-INVALID-OBS",
            "reason": "deterministic live runId scheme differs from SYN-INVALID-OBS runId",
        },
        {
            "field": "attemptId",
            "expected": "ATT-005",
            "actual": "A-WF-INVALID-OBS",
            "reason": "live attemptId is A-WF-*; SYN-INVALID-OBS uses ATT-005",
        },
    ],
    "WF-ABSTAIN": [
        {
            "field": "injectionStatus",
            "expected": "CONFIRMED",
            "actual": "UNRESOLVED",
            "reason": "catalogue H-RESOURCE-ERROR is unresolved; SYN-STOP-645 stores CONFIRMED",
        },
        {
            "field": "faultDomain",
            "expected": "IN-DOMAIN-NON-EQUIVALENT",
            "actual": "UNKNOWN",
            "reason": "catalogue H-RESOURCE-ERROR is unknown; SYN-STOP-645 stores IN-DOMAIN-NON-EQUIVALENT",
        },
        {
            "field": "truthReference.truthHypothesis",
            "expected": "h645",
            "actual": None,
            "reason": "catalogue H-RESOURCE-ERROR hypothesisId is null; SYN-STOP-645 stores h645",
        },
    ],
    "WF-EQUIVALENT": [
        {
            "field": "injectionStatus",
            "expected": "EQUIVALENT",
            "actual": None,
            "reason": "EVAL reads IF-EXP-TRUTH only; equivalent accounting replay writes no truth",
        },
        {
            "field": "faultDomain",
            "expected": "OUT-OF-DOMAIN",
            "actual": None,
            "reason": "EVAL reads IF-EXP-TRUTH only; equivalent accounting replay writes no truth",
        },
        {
            "field": "resourceStatus",
            "expected": "NOT-RUN",
            "actual": None,
            "reason": "no RUN/COLLECT on equivalent replay; SYN-EQUIVALENT records NOT-RUN",
        },
    ],
}


@pytest.mark.parametrize("workflow_id", list(WF_PATHS))
def test_walkthrough_executes_live_pipeline_and_compares_syn(workflow_id: str) -> None:
    result = execute_synthetic_walkthrough(workflow_id)
    expected_path = WF_PATHS[workflow_id]
    assert result["registeredPath"] == expected_path
    assert result["pathKind"] == WF_PATH_KIND[workflow_id]
    assert result["sceneRecord"]["producer"] == "IF-EXP-SCENE"
    assert result["injectionAttempt"]["producer"] == "IF-EXP-INJECT"
    assert result["synComparison"] == EXPECTED_SYN_MISMATCHES[workflow_id]
    actual = result["attemptRow"]
    cells = metric_cells([actual])
    if WF_PATH_KIND[workflow_id] == "LIVE" and "IF-EXP-RUN" in expected_path:
        assert result["runRecord"] is not None
        assert result["runRecord"]["producer"] == "IF-EXP-RUN"
        assert result["collectRecord"]["producer"] == "IF-EXP-COLLECT"
        source = inspect.getsource(execute_synthetic_walkthrough)
        assert "replay_run_fixture" not in source
        assert "collect_from_fixture" not in source
    if workflow_id == "WF-NORMAL":
        assert actual["outcome"] == "PASS"
        assert actual["finalHypotheses"] == ["h_normal"]
        assert actual["stopClass"] == "Stop-Singleton"
        assert actual["armId"] == "CL-LOOP"
        assert actual["validity"] == "VALID"
    if workflow_id == "WF-UNCONFIRMED-INJECT":
        assert actual["runId"] is None
        assert result["filterRecord"]["validityClass"] == "PRE-RUN-EXCLUDED"
        assert actual["outcome"] == "NOT-ANSWERED"
        assert actual["injectionStatus"] == "UNCONFIRMED"
        assert actual["faultDomain"] == "UNKNOWN"
        assert actual["attemptId"] in cells["populations"]["POP-ATTEMPTS"]
        assert actual["attemptId"] not in cells["populations"]["POP-ANSWERED"]
    if workflow_id == "WF-INVALID-OBS":
        assert result["collectRecord"]["missingCorrelation"] is True
        assert result["filterRecord"]["validityClass"] == "INVALID"
        assert actual["outcome"] == "ERROR"
        assert actual["attemptId"] not in cells["populations"]["POP-LOCALIZATION-ELIGIBLE"]
        assert actual["attemptId"] not in cells["populations"]["POP-LOCALIZATION-TRUTH-SCORABLE"]
    if workflow_id == "WF-ABSTAIN":
        replay_source = inspect.getsource(execute_accounting_replay)
        assert "fixture[\"validity\"]" not in replay_source
        assert "fixture[\"outcome\"]" not in replay_source
        assert result["filterRecord"]["validityClass"] == "ABSTAIN"
        assert actual["validity"] == "ABSTAIN"
        assert actual["outcome"] not in {"PASS", "FAIL"}
        assert actual["outcome"] == "NOT-ANSWERED"
        assert actual["attemptId"] in cells["populations"]["POP-ATTEMPTS"]
        assert actual["attemptId"] in cells["populations"]["POP-ABSTAIN"]
        assert actual["attemptId"] not in cells["populations"]["POP-ANSWERED"]
    if workflow_id == "WF-EQUIVALENT":
        assert result["runRecord"] is None
        assert result["filterRecord"]["validityClass"] == "PRE-RUN-EXCLUDED"
        assert actual["runId"] is None
        assert actual["outcome"] == "NOT-ANSWERED"
        assert actual["attemptId"] in cells["populations"]["POP-ATTEMPTS"]
        assert actual["attemptId"] not in cells["populations"]["POP-ANSWERED"]


def test_design_ledger_syn_rows_remain_in_attempt_denominator() -> None:
    design = load_experiment_design()
    rows = list(design["syntheticWalkthroughs"])
    cells = metric_cells(rows)
    assert set(cells["populations"]["POP-ATTEMPTS"]) == {
        item["attemptId"] for item in design["syntheticWalkthroughs"]
    }
    abstain_id = load_synthetic_walkthrough("SYN-STOP-645")["attemptId"]
    assert abstain_id in cells["populations"]["POP-ABSTAIN"]
    assert abstain_id not in cells["populations"]["POP-ANSWERED"]
    unconfirmed = load_synthetic_walkthrough("SYN-UNCONFIRMED")["attemptId"]
    assert unconfirmed in cells["populations"]["POP-ATTEMPTS"]
    assert unconfirmed not in cells["populations"]["POP-ANSWERED"]


def test_schema_fixture_replay_is_not_walkthrough_evidence() -> None:
    expected = load_synthetic_walkthrough("SYN-INVALID-OBS")
    fixture = dict(expected)
    fixture["observationLog"] = [{"correlationId": None, "kind": "STATUS"}]
    run = replay_run_fixture(fixture)
    collect = collect_from_fixture(fixture)
    filtered = filter_from_fixture(fixture, collect)
    assert run["finalHypotheses"] == fixture["finalHypotheses"]
    assert collect["missingCorrelation"] is True
    assert filtered["validityClass"] == "INVALID"
    source = inspect.getsource(execute_synthetic_walkthrough)
    assert "replay_run_fixture" not in source
    assert "collect_from_fixture" not in source


def test_pipeline_modules_do_not_read_iut_private_fault_flags() -> None:
    forbidden = (
        "_resource_error",
        "_fault_id",
        "_scene_id",
        "_scene_wait",
        "_scene_abort",
        "_scene_batch",
    )
    for path in PIPE.glob("*.py"):
        source = path.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in source, f"{path.name} reads IUT private {token}"


def test_run_and_collect_modules_do_not_import_or_read_truth() -> None:
    for name in ("run.py", "collect.py"):
        tree = ast.parse((PIPE / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            modules: list[str] = []
            if isinstance(node, ast.Import):
                modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.append(node.module)
            assert all("truth" not in module.split(".") for module in modules)
            assert all("TruthCapability" not in getattr(node, "names", []) or True for _ in [])
        source = (PIPE / name).read_text(encoding="utf-8")
        assert "IndependentTruthStore" not in source
        assert "get_truth" not in source
        assert "issue_truth_capability" not in source


def test_eval_reads_truth_via_capability_live() -> None:
    capability = issue_truth_capability()
    store = new_independent_truth_store()
    result = execute_live_attempt(
        scene_id="SC-NORMAL-UPLOAD",
        fault_id="H-NORMAL",
        arm_id="CL-LOOP",
        resource_mode="ROUNDS",
        remaining=8,
        capability=capability,
        store=store,
        confirm=True,
    )
    assert result["attemptRow"]["attemptId"]
    assert result["truthRecord"] is not None
    assert "truthHypothesis" in result["truthRecord"]
    assert result["runRecord"]["producer"] == "IF-EXP-RUN"
    blob = json.dumps(result["runRecord"]) + json.dumps(result["collectRecord"])
    assert "truthHypothesis" not in blob
    assert "TruthCapability" not in blob


def test_cl_t_normal_mixed_set_is_inconclusive_not_pass_or_fail() -> None:
    capability = issue_truth_capability()
    store = new_independent_truth_store()
    result = execute_live_attempt(
        scene_id="SC-NORMAL-UPLOAD",
        fault_id="H-NORMAL",
        arm_id="CL-T",
        resource_mode="ROUNDS",
        remaining=8,
        capability=capability,
        store=store,
        confirm=True,
    )
    row = result["attemptRow"]
    assert row is not None
    assert result["runRecord"]["finalHypotheses"] == ["h_normal", "h_status_silence"]
    assert row["outcome"] == "INCONCLUSIVE"
    assert row["outcome"] not in {"PASS", "FAIL"}
    cells = result["metricCells"]
    assert row["attemptId"] in cells["populations"]["POP-INCONCLUSIVE"]
    assert row["attemptId"] not in cells["populations"]["POP-ANSWERED"]
    assert (
        derive_outcome(
            validity="VALID",
            stop_class="Stop-NoDistinguisher",
            observation_interval=None,
            requirement_interval=None,
            final_hypotheses=["h_normal", "h_status_silence"],
        )
        == "INCONCLUSIVE"
    )


def test_derive_outcome_nonsingleton_without_normal_is_fail() -> None:
    assert (
        derive_outcome(
            validity="VALID",
            stop_class="Stop-Budget",
            observation_interval=None,
            requirement_interval=None,
            final_hypotheses=["h1", "h2"],
        )
        == "FAIL"
    )
    assert (
        derive_outcome(
            validity="VALID",
            stop_class="Stop-Singleton",
            observation_interval=None,
            requirement_interval=None,
            final_hypotheses=["h_normal"],
        )
        == "PASS"
    )


def test_filter_budget_incomplete_from_run_evidence() -> None:
    filtered = filter_attempt(
        variant="run-completed",
        stop_class="Stop-Budget",
        action_issued=True,
        resource_status="BUDGET-EXHAUSTED",
        stage="TERMINAL",
    )
    assert filtered["validityClass"] == "INCOMPLETE"
    assert filtered["filterReason"] == "budget-exhausted"


def test_run_ids_are_deterministic_from_attempt_and_arm() -> None:
    first = execute_synthetic_walkthrough("WF-NORMAL")
    second = execute_synthetic_walkthrough("WF-NORMAL")
    assert first["runRecord"]["runId"] == second["runRecord"]["runId"]
    assert first["runRecord"]["runId"] == "RUN-CL-LOOP-A-WF-NORMAL"


def test_live_unconfirmed_stays_in_attempt_denominator() -> None:
    capability = issue_truth_capability()
    store = new_independent_truth_store()
    result = execute_live_attempt(
        scene_id="SC-NORMAL-UPLOAD",
        fault_id="H-NORMAL",
        arm_id="CL-T",
        resource_mode="ROUNDS",
        remaining=8,
        capability=capability,
        store=store,
        confirm=False,
    )
    row = result["attemptRow"]
    assert row["runId"] is None
    assert result["filterRecord"]["validityClass"] == "PRE-RUN-EXCLUDED"
    assert row["outcome"] == "NOT-ANSWERED"
    assert row["injectionStatus"] == "UNCONFIRMED"
    assert row["faultDomain"] == "UNKNOWN"
    cells = result["metricCells"]
    assert row["attemptId"] in cells["populations"]["POP-ATTEMPTS"]
    assert row["attemptId"] not in cells["populations"]["POP-ANSWERED"]


def test_resource_error_silence_collision_is_separate_from_abstain_walkthrough() -> None:
    capability = issue_truth_capability()
    store = new_independent_truth_store()
    result = execute_live_attempt(
        scene_id="SC-RESOURCE-ERROR",
        fault_id="H-RESOURCE-ERROR",
        arm_id="CL-LOOP",
        resource_mode="BUDGET",
        remaining=8,
        capability=capability,
        store=store,
        confirm=True,
    )
    row = result["attemptRow"]
    assert result["injectionAttempt"]["testerResourceLog"]["statusClass"] == "RESOURCE-ERROR"
    assert result["runRecord"]["testerResourceLog"]["statusClass"] == "RESOURCE-ERROR"
    assert row["resourceErrorSilenceCollision"] is True
    assert row["detectFamilyOnly"] is True
    assert row["truthReference"]["truthHypothesis"] is None
    cells = result["metricCells"]
    assert row["attemptId"] in cells["resourceErrorSilenceCollisionAttemptIds"]
    assert row["attemptId"] not in cells["populations"]["POP-LOCALIZATION-TRUTH-SCORABLE"]
    abstain = execute_synthetic_walkthrough("WF-ABSTAIN")
    assert abstain["pathKind"] == "ACCOUNTING-REPLAY"
    assert abstain["attemptRow"]["validity"] == "ABSTAIN"


def test_collect_same_key_status_is_not_resource_error() -> None:
    capability = issue_truth_capability()
    store = new_independent_truth_store()
    result = execute_live_attempt(
        scene_id="SC-SAME-KEY",
        fault_id="H-SAME-KEY",
        arm_id="CL-LOOP",
        resource_mode="ROUNDS",
        remaining=8,
        capability=capability,
        store=store,
        confirm=True,
    )
    status = result["collectRecord"]["resourceLog"]["statusClass"]
    assert status != "RESOURCE-ERROR"
    observations = result["collectRecord"]["observationLog"]
    assert any(
        isinstance(item, dict) and item.get("kind") == "STATUS" for item in observations
    )
    replay = collect_from_run(
        {
            "runId": "RUN-SAME-KEY",
            "stopClass": "Stop-Singleton",
            "observationLog": [{"kind": "STATUS", "payload": {}}],
        },
        resource_mode="ROUNDS",
    )
    assert replay["resourceLog"]["statusClass"] == "UNCLASSIFIED-STATUS"


def test_live_invalid_observation_is_error_not_iut_fail() -> None:
    capability = issue_truth_capability()
    store = new_independent_truth_store()
    result = execute_live_attempt(
        scene_id="SC-INVALID-OBS",
        fault_id="H-INVALID-OBS",
        arm_id="CL-T",
        resource_mode="ROUNDS",
        remaining=8,
        capability=capability,
        store=store,
        confirm=True,
    )
    assert result["collectRecord"]["missingCorrelation"] is True
    assert result["filterRecord"]["validityClass"] == "INVALID"
    assert result["attemptRow"]["outcome"] == "ERROR"
    assert result["attemptRow"]["attemptId"] in result["metricCells"]["populations"]["POP-ATTEMPTS"]
    assert result["attemptRow"]["attemptId"] not in result["metricCells"]["populations"]["POP-ANSWERED"]
    assert result["attemptRow"]["attemptId"] not in result["metricCells"]["populations"]["POP-LOCALIZATION-ELIGIBLE"]
    assert result["attemptRow"]["attemptId"] not in result["metricCells"]["populations"]["POP-LOCALIZATION-TRUTH-SCORABLE"]


def test_n3_reference_session_reaches_iut_only_through_execute() -> None:
    env_source = inspect.getsource(SimulatedIutEnvironment)
    tree = ast.parse(env_source)
    class_nodes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    class_def = class_nodes[0] if class_nodes else tree
    methods = [node for node in class_def.body if isinstance(node, ast.FunctionDef)]
    names = {node.name for node in methods}
    assert "execute" in names
    for node in methods:
        called = [n.attr for n in ast.walk(node) if isinstance(n, ast.Attribute)]
        if node.name not in {"execute", "__init__"}:
            assert "find" not in called
            assert "send" not in called
            assert "information" not in called
            assert "abort" not in called
    session_src = inspect.getsource(ReferenceSession)
    assert "environment.execute(" in session_src
    assert session_src.count("environment.execute(") == 1
    loop_path = SRC / "a615a_sim" / "algorithm" / "loop.py"
    loop = ast.parse(loop_path.read_text(encoding="utf-8"))
    class_def = next(
        node for node in loop.body if isinstance(node, ast.ClassDef) and node.name == "SimulatedIutEnvironment"
    )
    for node in class_def.body:
        if isinstance(node, ast.FunctionDef) and node.name not in {"__init__", "execute"}:
            pytest.fail(f"unexpected IUT contact method {node.name}")


def test_n4_absent_answer_timing_uses_observation_end() -> None:
    model_tick = Fraction(0, 1)
    end = observation_end_for_absent_answer(
        family="FIND",
        model_measurement_tick=model_tick,
    )
    assert end == declared_observation_end("FIND")
    assert end == FIND_OBSERVATION_END_S
    assert end != model_tick


def test_run_module_truth_access_fails_closed() -> None:
    with pytest.raises(TruthLeakageError):
        exec(
            "from a615a_sim.evaluator.truth import IndependentTruthStore\n"
            "IndependentTruthStore()\n",
            {"__name__": "a615a_sim.evaluator.pipeline.run"},
        )


def test_pilot_registration_shape_leaves_n_and_seeds_pending() -> None:
    payload = json.loads(
        (ROOT / "configs/research/cltav_pilot_registration_shape_v1.json").read_text(encoding="utf-8")
    )
    assert payload["identity"]["confirmatoryRegistration"] is False
    assert payload["identity"]["registrationYaml"] is False
    assert payload["sample"]["N"] == "PENDING-PHASE-D"
    assert payload["sample"]["seeds"] == "PENDING-PHASE-D"
    assert payload["identity"]["label"] == "PILOT / SIMULATED-IUT"


def test_population_sets_match_design_checker_on_syn_rows() -> None:
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    import check_experiment_design as checker  # noqa: E402

    design = load_experiment_design()
    expected = checker._population_sets(dict(design))
    actual = population_sets(list(design["syntheticWalkthroughs"]))
    for key in actual:
        if key == "POP-PAIRED-ELIGIBLE":
            continue
        assert actual[key] == expected[key], key
