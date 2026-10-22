"""Two-round bounded session integration checks without an IUT or network."""

from __future__ import annotations

import copy
from dataclasses import FrozenInstanceError, replace
import json
from pathlib import Path
import subprocess

import pytest

from cltav_runtime.bindings import RuntimeAuthorityBinding
from cltav_runtime.kernel import ContractSnapshot, ModelContext
from cltav_runtime.model import FiniteSessionModel
from cltav_runtime.session import ReferenceSession, ResourceState, SessionState
from cltav_runtime.synthetic import (
    EnvironmentExecution,
    ExecutionRequest,
    SyntheticEnvironment,
    VisibleExecutionRecord,
)
from cltav_runtime.types import HistoryHandle


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "fixtures" / "cltav_runtime" / "two_round_scenarios.json"
DEVELOPMENT_PATH = "configs/engineering/cltav_development_contracts.json"
INTERFACE_PATH = "configs/research/cltav_interface_registry.json"


def _head_commit() -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()


def _runtime_parts() -> tuple[RuntimeAuthorityBinding, FiniteSessionModel, dict[str, object]]:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    head = _head_commit()
    binding = RuntimeAuthorityBinding.from_git_objects(
        repository=ROOT,
        development_commit=head,
        development_path=DEVELOPMENT_PATH,
        interface_commit=head,
        interface_path=INTERFACE_PATH,
    )
    snapshot = ContractSnapshot.from_git_object(
        repository=ROOT, contract_commit=head, contract_path=DEVELOPMENT_PATH,
    )
    public_model = fixture["algorithmModel"]["model"]
    context = ModelContext.build(
        snapshot=snapshot,
        model={
            "stateIds": set(public_model["stateIds"]),
            "clockIds": set(public_model["clockIds"]),
            "typedDomains": {
                name: set(domain) for name, domain in public_model["typedDomains"].items()
            },
        },
        projection_clock="x",
    )
    return binding, FiniteSessionModel.from_mapping(context=context, value=fixture["algorithmModel"]), fixture


@pytest.mark.parametrize(
    ("environment_name", "second_action", "remaining_hypothesis"),
    [("alpha", "test-left", "h0"), ("beta", "test-right", "h2")],
)
def test_two_round_feedback_consumes_committed_summary_and_changes_selection(
    environment_name: str, second_action: str, remaining_hypothesis: str,
) -> None:
    binding, model, fixture = _runtime_parts()
    result = ReferenceSession(
        binding=binding,
        model=model,
        session_id=f"session-{environment_name}",
        run_id=f"run-{environment_name}",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
    ).run(SyntheticEnvironment.from_mapping(fixture["environments"][environment_name]), maximum_rounds=2)

    assert result.stop_reason == "Stop-Singleton"
    assert [item.snapshot.action_id for item in result.state.evidence] == ["test-router", second_action]
    assert result.state.evidence[1].snapshot.q_used_at_select == result.state.evidence[0].summary_after
    assert result.state.evidence[1].snapshot.history_version == 1
    assert result.state.history.hypotheses == {remaining_hypothesis}
    assert result.state.resources.remaining == 0
    assert all(item.committed for item in result.state.evidence)
    assert result.state.context.experiment_attempt_id is None
    assert [item.execution.execution_attempt_id for item in result.state.evidence] == [
        f"run-{environment_name}:session-{environment_name}:execution:1",
        f"run-{environment_name}:session-{environment_name}:execution:2",
    ]
    assert all(item.issued_to_executor and item.charged_once for item in result.state.evidence)
    assert result.state.evidence[0].detail_charges == {
        "acquisition": 0, "computation": 1, "preparation": 0, "recovery": 0, "retry": 0,
    }
    assert result.state.evidence[0].projected_cost == {
        "acquisition": 0, "computation": 1, "preparation": 0, "retry": 0,
    }


def test_evaluator_truth_is_not_an_algorithm_input() -> None:
    binding, model, fixture = _runtime_parts()
    environment = SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"])
    first = ReferenceSession(
        binding=binding, model=model, session_id="session-a", run_id="run-a", initial_summary="q0", resources=ResourceState.rounds(2),
    ).run(environment, maximum_rounds=2)
    # These labels live only in the evaluator fixture.  Altering them does not
    # change any algorithm-facing input or the resulting action trajectory.
    evaluator_truth = fixture["evaluatorTruth"]
    evaluator_truth["alpha"]["injectedCondition"] = "different-evaluator-label"
    second = ReferenceSession(
        binding=binding, model=model, session_id="session-a", run_id="run-a", initial_summary="q0", resources=ResourceState.rounds(2),
    ).run(SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]), maximum_rounds=2)

    assert [item.snapshot.action_id for item in first.state.evidence] == [
        item.snapshot.action_id for item in second.state.evidence
    ]
    assert first.state.history.hypotheses == second.state.history.hypotheses


def test_algorithm_model_rejects_an_extra_truth_field() -> None:
    _binding, model, fixture = _runtime_parts()
    altered = dict(fixture["algorithmModel"])
    altered["nestedTruth"] = {"evaluator": "not-visible"}

    with pytest.raises(ValueError, match="unknown or missing"):
        FiniteSessionModel.from_mapping(context=model.context, value=altered)


def test_prediction_keeps_overlapping_classes_and_names_a_current_gap() -> None:
    _binding, model, _fixture = _runtime_parts()
    overlap = model.predict(
        hypotheses=frozenset(model.initial_frontiers),
        frontiers=model.initial_frontiers,
        status_by_hypothesis={},
        action_id="test-overlap",
    )
    gap = model.predict(
        hypotheses=frozenset(model.initial_frontiers),
        frontiers=model.initial_frontiers,
        status_by_hypothesis={},
        action_id="test-gap",
    )

    assert {item.observable: item.hypotheses for item in overlap.classes}["overlap-shared"] == {"h0", "h2"}
    assert overlap.has_distinguishing_value is True
    assert gap.classes == ()


def test_model_detaches_nested_ast_inputs_and_exposes_no_mutable_transition() -> None:
    _binding, model, fixture = _runtime_parts()
    source = copy.deepcopy(fixture["algorithmModel"])
    frozen = FiniteSessionModel.from_mapping(context=model.context, value=source)
    before = frozen.predict(
        hypotheses=frozenset(frozen.initial_frontiers),
        frontiers=frozen.initial_frontiers,
        status_by_hypothesis={},
        action_id="test-router",
    )
    source_router = next(item for item in source["actions"] if item["id"] == "test-router")
    source_router["transition"]["guardAst"] = {"tag": "STATE-EQUALS", "state": "q1"}
    detached = frozen.actions["test-router"].transition_for_kernel()
    detached["guardAst"] = {"tag": "STATE-EQUALS", "state": "q1"}
    after = frozen.predict(
        hypotheses=frozenset(frozen.initial_frontiers),
        frontiers=frozen.initial_frontiers,
        status_by_hypothesis={},
        action_id="test-router",
    )

    assert [(item.observable, item.hypotheses) for item in after.classes] == [
        (item.observable, item.hypotheses) for item in before.classes
    ]
    with pytest.raises(FrozenInstanceError):
        frozen.actions["test-router"].transition_json = "{}"  # type: ignore[misc]


def test_unaffordable_best_test_and_no_information_test_do_not_displace_router() -> None:
    binding, model, fixture = _runtime_parts()
    budget_model_data = copy.deepcopy(fixture["algorithmModel"])
    for action in budget_model_data["actions"]:
        if action["id"] in {"test-router", "test-expensive-optimal"}:
            action["enabledSummaries"] = ["budget-q0"]
    budget_model = FiniteSessionModel.from_mapping(context=model.context, value=budget_model_data)
    result = ReferenceSession(
        binding=binding,
        model=budget_model,
        session_id="session-affordability",
        run_id="run-affordability",
        initial_summary="budget-q0",
        resources=ResourceState.budget(2),
    ).run(SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]), maximum_rounds=1)

    assert result.state.evidence[0].snapshot.action_id == "test-router"
    assert result.state.evidence[0].snapshot.action_id != "test-no-information"


def test_rounds_mode_consumes_one_issued_action_not_declared_action_cost() -> None:
    binding, model, fixture = _runtime_parts()
    rounds_model_data = copy.deepcopy(fixture["algorithmModel"])
    for action in rounds_model_data["actions"]:
        if action["id"] == "test-expensive-optimal":
            action["enabledSummaries"] = ["q0"]
    rounds_model = FiniteSessionModel.from_mapping(context=model.context, value=rounds_model_data)
    environment = SyntheticEnvironment.from_mapping(
        {
            "initialPrivateState": "private-rounds",
            "uncertaintyIdentity": "synthetic-u-1",
            "states": {
                "private-rounds": {
                    "test-expensive-optimal": {"effectClass": "NONE", "observable": "e0", "summaryConfirmed": True, "measurementTick": 0, "nextPrivateState": "private-rounds"}
                }
            },
        },
    )
    result = ReferenceSession(
        binding=binding, model=rounds_model, session_id="session-rounds", run_id="run-rounds",
        initial_summary="q0", resources=ResourceState.rounds(1),
    ).run(environment, maximum_rounds=1)

    assert result.state.evidence[0].snapshot.action_id == "test-expensive-optimal"
    assert result.state.evidence[0].resource_before.remaining == 1
    assert result.state.evidence[0].resource_after.remaining == 0


def test_current_test_gap_is_named_and_eligible_prep_uses_the_same_admission_entry() -> None:
    binding, model, fixture = _runtime_parts()
    gap_and_router = copy.deepcopy(fixture["algorithmModel"])
    gap_and_router["actions"] = [
        item for item in gap_and_router["actions"]
        if item["id"] in {"test-gap", "test-router"}
    ]
    for action in gap_and_router["actions"]:
        if action["id"] == "test-gap":
            action["enabledSummaries"] = ["q0"]
    gap_and_router["limits"]["actions"] = 2
    gap_model = FiniteSessionModel.from_mapping(context=model.context, value=gap_and_router)
    gap_result = ReferenceSession(
        binding=binding, model=gap_model, session_id="session-gap", run_id="run-gap",
        initial_summary="q0", resources=ResourceState.rounds(1),
    ).run(SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]), maximum_rounds=1)
    assert gap_result.stop_reason == "Stop-Prediction-Gap"

    with_prep = copy.deepcopy(gap_and_router)
    with_prep["actions"].append(
        {
            "id": "prep-after-gap",
            "kind": "PREP",
            "cost": 1,
            "detailCharges": {"acquisition": 0, "computation": 0, "preparation": 1, "recovery": 0, "retry": 0},
            "enabledSummaries": ["q0"],
            "transition": {"id": "tr-prep", "source": "q0", "target": "q0", "guardAst": {"tag": "TRUE"}, "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q0"}]},
            "observableByHypothesis": {"h0": "prep-summary", "h1": "prep-summary", "h2": "prep-summary", "h3": "prep-summary"},
            "measurementTicksByHypothesis": {"h0": 0, "h1": 0, "h2": 0, "h3": 0},
        },
    )
    with_prep["limits"]["actions"] = 3
    prep_model = FiniteSessionModel.from_mapping(context=model.context, value=with_prep)
    prep_environment = SyntheticEnvironment.from_mapping(
        {
            "initialPrivateState": "private-prep",
            "uncertaintyIdentity": "synthetic-u-1",
            "states": {
                "private-prep": {
                    "prep-after-gap": {"effectClass": "NONE", "observable": "prep-summary", "summaryConfirmed": True, "measurementTick": 0, "nextPrivateState": "private-prep"}
                }
            },
        },
    )
    prep_result = ReferenceSession(
        binding=binding, model=prep_model, session_id="session-prep", run_id="run-prep",
        initial_summary="q0", resources=ResourceState.rounds(1),
    ).run(prep_environment, maximum_rounds=1)
    assert prep_result.state.evidence[0].snapshot.action_id == "prep-after-gap"
    assert prep_result.stop_reason == "Stop-Round-Limit"

    refused = ReferenceSession(
        binding=binding, model=prep_model, session_id="session-prep-refused", run_id="run-prep-refused",
        initial_summary="q0", resources=ResourceState.rounds(0),
    ).run(prep_environment, maximum_rounds=1)
    assert refused.stop_reason == "Stop-Budget"
    assert refused.state.evidence == ()
    assert refused.diagnostics[-1].code == "ADMISSION-A2-UNAFFORDABLE"


def test_environment_execution_request_has_no_hypothesis_or_truth_argument() -> None:
    with pytest.raises(TypeError):
        ExecutionRequest(
            session_id="session-a", execution_attempt_id="run-a:session-a:execution:1", action_id="test-router", action_kind="TEST",
            hypotheses={"h0"},  # type: ignore[call-arg]
        )


def test_confirmed_not_sent_is_issued_and_charged_once_but_preserves_history() -> None:
    binding, model, fixture = _runtime_parts()
    result = ReferenceSession(
        binding=binding,
        model=model,
        session_id="session-not-sent",
        run_id="run-not-sent",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
    ).run(SyntheticEnvironment.from_mapping(fixture["environments"]["notSent"]), maximum_rounds=1)

    assert result.stop_reason == "Stop-Error"
    evidence = result.state.evidence[0]
    assert evidence.execution.effect_class == "CONFIRMED-NOT-SENT"
    assert evidence.issued_to_executor is True
    assert evidence.charged_once is True
    assert evidence.resource_before.remaining == 2
    assert evidence.resource_after.remaining == 1
    assert evidence.history_before is evidence.history_after
    assert evidence.summary_after == "q0"
    assert evidence.committed is False


def test_execution_tool_error_keeps_the_already_charged_execution_record() -> None:
    class FailingEnvironment:
        def execute(self, _request: ExecutionRequest) -> object:
            raise ValueError("controlled executor failure")

    binding, model, _fixture = _runtime_parts()
    result = ReferenceSession(
        binding=binding, model=model, session_id="session-tool-error", run_id="run-tool-error",
        initial_summary="q0", resources=ResourceState.rounds(2),
    ).run(FailingEnvironment(), maximum_rounds=1)  # type: ignore[arg-type]

    assert result.stop_reason == "Stop-Error"
    assert result.state.resources.remaining == 1
    assert result.state.attempts == 1
    assert result.state.evidence[0].execution.effect_class == "UNKNOWN-EFFECT"
    assert result.state.evidence[0].charged_once is True
    assert result.state.context.q_status == "CONSERVATIVE-UNKNOWN"


def test_invalid_execution_identity_does_not_restore_the_pre_charge_state() -> None:
    class WrongIdentityEnvironment:
        def __init__(self, successor: SyntheticEnvironment) -> None:
            self.successor = successor

        def execute(self, _request: ExecutionRequest) -> EnvironmentExecution:
            return EnvironmentExecution(
                VisibleExecutionRecord(
                    execution_attempt_id="wrong-execution-id",
                    action_id="test-router",
                    effect_class="NONE",
                    observable="branch-alpha",
                    summary_confirmed=True,
                    post_summary="branch-alpha",
                    measurement_tick=0,
                    uncertainty_identity="synthetic-u-1",
                    evidence_ref="synthetic:wrong-execution-id:bad",
                ),
                self.successor,
            )

    binding, model, fixture = _runtime_parts()
    result = ReferenceSession(
        binding=binding, model=model, session_id="session-identity-error", run_id="run-identity-error",
        initial_summary="q0", resources=ResourceState.rounds(2),
    ).run(
        WrongIdentityEnvironment(SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"])),  # type: ignore[arg-type]
        maximum_rounds=1,
    )

    assert result.stop_reason == "Stop-Error"
    assert result.state.resources.remaining == 1
    assert result.state.attempts == 1
    assert result.state.context.q_status == "CONSERVATIVE-UNKNOWN"
    assert result.state.evidence[0].execution.execution_attempt_id == "run-identity-error:session-identity-error:execution:1"
    assert result.diagnostics[-1].code == "EXECUTION-IDENTITY-ERROR"


def test_conservative_hypothesis_is_retained_by_a_normal_visible_observation() -> None:
    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-conservative", run_id="run-conservative",
        initial_summary="q0", resources=ResourceState.rounds(2),
    )
    initial = session.initial_state
    history = HistoryHandle.initial(
        hypotheses=set(initial.frontiers),
        compatible_state_by_hypothesis={
            hypothesis: frontier.history_provenance[-1]
            for hypothesis, frontier in initial.frontiers.items()
        },
        status_by_hypothesis={
            hypothesis: "CONSERVATIVE-UNKNOWN" if hypothesis == "h3" else "KNOWN"
            for hypothesis in initial.frontiers
        },
    )
    state = SessionState(
        initial.context, history, initial.frontiers, initial.resources, 0, frozenset(), (),
    )
    result = session.step(state, SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]))

    assert result.state.history.hypotheses == {"h0", "h1", "h3"}
    assert result.state.history.status_by_hypothesis["h3"] == "CONSERVATIVE-UNKNOWN"


@pytest.mark.parametrize(
    ("altered_state", "expected_code"),
    [
        (
            lambda state: replace(
                state,
                context=replace(state.context, model_identity="foreign-model"),
            ),
            "SESSION-IDENTITY-MISMATCH",
        ),
        (
            lambda state: replace(state, history=replace(state.history, version=99)),
            "INVALID-INITIAL-HISTORY",
        ),
    ],
)
def test_resume_rejects_foreign_model_or_jump_history_before_charge(
    altered_state: object, expected_code: str,
) -> None:
    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-resume", run_id="run-resume",
        initial_summary="q0", resources=ResourceState.rounds(2),
    )
    state = altered_state(session.initial_state)  # type: ignore[operator]
    result = session.step(state, SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]))

    assert result.stop_reason == "Stop-Error"
    assert result.diagnostics[0].code == expected_code
    assert result.state.resources.remaining == 2
    assert result.state.evidence == ()


def test_resume_rejects_history_reference_not_owned_by_the_current_frontier() -> None:
    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-history", run_id="run-history",
        initial_summary="q0", resources=ResourceState.rounds(2),
    )
    initial = session.initial_state
    references = {
        hypothesis: frontier.history_provenance[-1]
        for hypothesis, frontier in initial.frontiers.items()
    }
    references["h0"] = "fabricated-provenance-reference"
    altered = replace(
        initial,
        history=HistoryHandle.initial(
            hypotheses=set(initial.frontiers),
            compatible_state_by_hypothesis=references,
        ),
    )
    result = session.step(altered, SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]))

    assert result.stop_reason == "Stop-Error"
    assert result.diagnostics[0].code == "HISTORY-PROVENANCE-MISMATCH"
    assert result.state.evidence == ()


def test_shared_uncertainty_changes_the_prediction_and_interpretation_boundary() -> None:
    binding, model, fixture = _runtime_parts()
    shifted_alpha = copy.deepcopy(fixture["environments"]["alpha"])
    shifted_alpha["states"]["private-a0"]["test-router"]["measurementTick"] = 1

    zero_result = ReferenceSession(
        binding=binding, model=model, session_id="session-u-zero", run_id="run-u-zero",
        initial_summary="q0", resources=ResourceState.rounds(1),
    ).run(SyntheticEnvironment.from_mapping(shifted_alpha), maximum_rounds=1)
    assert zero_result.stop_reason == "Stop-Error"
    assert zero_result.diagnostics[-1].code == "OBSERVATION-MEASUREMENT-OUTSIDE-UNCERTAINTY"
    assert zero_result.state.evidence[0].committed is False

    wide_data = copy.deepcopy(fixture["algorithmModel"])
    wide_data["uncertainty"] = {
        "id": "synthetic-u-wide", "clockId": "x", "timeUnit": "ticks", "maximumErrorTicks": 1,
    }
    wide_model = FiniteSessionModel.from_mapping(context=model.context, value=wide_data)
    shifted_alpha["uncertaintyIdentity"] = "synthetic-u-wide"
    wide_result = ReferenceSession(
        binding=binding, model=wide_model, session_id="session-u-wide", run_id="run-u-wide",
        initial_summary="q0", resources=ResourceState.rounds(1),
    ).run(SyntheticEnvironment.from_mapping(shifted_alpha), maximum_rounds=1)
    predicted = wide_model.predict(
        hypotheses=frozenset(wide_model.initial_frontiers), frontiers=wide_model.initial_frontiers,
        status_by_hypothesis={}, action_id="test-router",
    )
    alpha_class = next(item for item in predicted.classes if item.observable == "branch-alpha")

    assert alpha_class.measurement_windows["h0"].lower == -1
    assert alpha_class.measurement_windows["h0"].upper == 1
    assert wide_result.stop_reason == "Stop-Round-Limit"
    assert wide_result.state.evidence[0].committed is True


def test_interpretation_rejects_an_uncertainty_identity_not_frozen_at_selection() -> None:
    binding, model, fixture = _runtime_parts()
    wrong_identity = copy.deepcopy(fixture["environments"]["alpha"])
    wrong_identity["uncertaintyIdentity"] = "replaced-at-interpretation"
    result = ReferenceSession(
        binding=binding, model=model, session_id="session-u-mismatch", run_id="run-u-mismatch",
        initial_summary="q0", resources=ResourceState.rounds(1),
    ).run(SyntheticEnvironment.from_mapping(wrong_identity), maximum_rounds=1)

    assert result.stop_reason == "Stop-Error"
    assert result.diagnostics[-1].code == "UNCERTAINTY-SNAPSHOT-MISMATCH"
    assert result.state.resources.remaining == 0
    assert result.state.history.version == 0
    assert result.state.context.q_status == "CONSERVATIVE-UNKNOWN"
