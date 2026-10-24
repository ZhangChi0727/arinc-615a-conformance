"""Two-round bounded session integration checks without an IUT or network."""

from __future__ import annotations

import copy
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction
import json
from pathlib import Path
import subprocess

import pytest

from cltav_runtime.bindings import RuntimeAuthorityBinding
from cltav_runtime.kernel import ContractSnapshot, ModelContext, initial_entry, propagate_transition
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
                    "test-expensive-optimal": {"effectClass": "NONE", "observable": "e0", "summaryConfirmed": True, "postSummary": "e0", "measurementTick": 0, "nextPrivateState": "private-rounds"}
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


def test_invalid_resource_mode_is_rejected_at_the_typed_boundary() -> None:
    with pytest.raises(ValueError, match="exactly ROUNDS or BUDGET"):
        ResourceState("TYPO", 2)


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
            "declaredTarget": "prepared-q1",
            "recoverWhenUnknown": False,
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
                    "prep-after-gap": {
                        "effectClass": "NONE",
                        "observable": "prep-summary",
                        "summaryConfirmed": True,
                        "postSummary": "prep-summary",
                        "measurementTick": 0,
                        "nextPrivateState": "private-prep",
                        "prepRecover": {
                            "targetConfirmed": False,
                            "summaryConfirmed": True,
                            "prepError": False,
                            "ineligible": False,
                            "declaredTarget": "prepared-q1",
                            "evidence": "synthetic:prep-after-gap:summary",
                            "postSummary": "prep-summary",
                        },
                    }
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


@pytest.mark.parametrize("reverse_actions", [False, True])
def test_prediction_gap_revokes_an_unaffordable_test_score_before_a2(
    reverse_actions: bool,
) -> None:
    binding, model, fixture = _runtime_parts()
    model_data = copy.deepcopy(fixture["algorithmModel"])
    model_data["actions"] = [
        action for action in model_data["actions"]
        if action["id"] in {"test-gap", "test-router"}
    ]
    for action in model_data["actions"]:
        if action["id"] == "test-gap":
            action["enabledSummaries"] = ["q0"]
        if action["id"] == "test-router":
            action["cost"] = 3
    if reverse_actions:
        model_data["actions"].reverse()
    model_data["limits"]["actions"] = 2
    gap_model = FiniteSessionModel.from_mapping(context=model.context, value=model_data)
    result = ReferenceSession(
        binding=binding, model=gap_model, session_id=f"session-gap-score-{reverse_actions}",
        run_id=f"run-gap-score-{reverse_actions}", initial_summary="q0", resources=ResourceState.budget(1),
    ).run(SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]), maximum_rounds=1)

    assert result.stop_reason == "Stop-Prediction-Gap"
    assert result.diagnostics[-1].code == "PREDICTION-GAP"
    assert result.state.attempts == 0
    assert result.state.resources.remaining == 1


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
        retry_cap=1,
    ).run(SyntheticEnvironment.from_mapping(fixture["environments"]["notSent"]), maximum_rounds=1)

    assert result.stop_reason == "Stop-Error"
    evidence = result.state.evidence[0]
    assert evidence.execution.effect_class == "CONFIRMED-NOT-SENT"
    assert evidence.execution.uncertainty_identity is None
    assert evidence.issued_to_executor is True
    assert evidence.charged_once is True
    assert evidence.resource_before.remaining == 2
    assert evidence.resource_after.remaining == 1
    assert evidence.history_before is evidence.history_after
    assert evidence.summary_after == "q0"
    assert evidence.committed is False
    assert result.state.context.retry_count == 1
    assert result.state.context.resource_remainder == 1

    resumed = ReferenceSession(
        binding=binding, model=model, session_id="session-not-sent", run_id="run-not-sent",
        initial_summary="q0", resources=ResourceState.rounds(2),
    ).step(result.state, result.environment)
    assert resumed.stop_reason == "Stop-Error"
    assert resumed.diagnostics[0].code == "TERMINAL-SESSION-STATE"
    assert resumed.state.attempts == 1


@pytest.mark.parametrize("error_type", [ValueError, RuntimeError, OSError])
def test_execution_tool_error_keeps_the_already_charged_execution_record(error_type: type[Exception]) -> None:
    class FailingEnvironment:
        def execute(self, _request: ExecutionRequest) -> object:
            raise error_type("controlled executor failure")

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
    assert result.state.context.q_status == "UNKNOWN"


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
                    measurement_tick=Fraction(0),
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
    assert result.state.context.q_status == "UNKNOWN"
    assert result.state.evidence[0].execution.execution_attempt_id == "run-identity-error:session-identity-error:execution:1"
    assert result.state.evidence[0].rejected_response is not None
    assert result.state.evidence[0].rejected_response.execution_attempt_id == "wrong-execution-id"
    assert result.diagnostics[-1].code == "EXECUTION-IDENTITY-ERROR"


def test_confirmed_but_missing_post_summary_keeps_charge_and_real_environment_successor() -> None:
    class MissingSummaryEnvironment:
        def __init__(self, successor: SyntheticEnvironment) -> None:
            self.successor = successor

        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            return EnvironmentExecution(
                VisibleExecutionRecord(
                    execution_attempt_id=request.execution_attempt_id,
                    action_id=request.action_id,
                    effect_class="NONE",
                    observable="branch-alpha",
                    summary_confirmed=True,
                    post_summary=None,
                    measurement_tick=0,
                    uncertainty_identity="synthetic-u-1",
                    evidence_ref="synthetic:missing-summary",
                ),
                self.successor,
            )

    binding, model, fixture = _runtime_parts()
    successor = SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]).execute(
        ExecutionRequest("seed-session", "seed-execution", "test-router", "TEST"),
    ).successor
    result = ReferenceSession(
        binding=binding, model=model, session_id="session-summary-error", run_id="run-summary-error",
        initial_summary="q0", resources=ResourceState.rounds(2),
    ).run(MissingSummaryEnvironment(successor), maximum_rounds=1)  # type: ignore[arg-type]

    assert result.stop_reason == "Stop-Error"
    assert result.diagnostics[-1].code == "SUMMARY-CONFIRMATION-ERROR"
    assert result.state.resources.remaining == 1
    assert result.state.attempts == 1
    assert result.state.context.q_status == "UNKNOWN"
    assert result.environment._state == "private-a1"
    assert result.state.evidence[0].rejected_response is not None
    assert result.state.evidence[0].rejected_response.post_summary is None


def test_malformed_execution_record_keeps_a_typed_successor_environment() -> None:
    class MalformedRecordEnvironment:
        def __init__(self, successor: SyntheticEnvironment) -> None:
            self.successor = successor

        def execute(self, _request: ExecutionRequest) -> EnvironmentExecution:
            return EnvironmentExecution("not-a-visible-record", self.successor)  # type: ignore[arg-type]

    binding, model, fixture = _runtime_parts()
    successor = SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]).execute(
        ExecutionRequest("seed-session", "seed-execution", "test-router", "TEST"),
    ).successor
    result = ReferenceSession(
        binding=binding, model=model, session_id="session-record-type", run_id="run-record-type",
        initial_summary="q0", resources=ResourceState.rounds(2),
    ).run(MalformedRecordEnvironment(successor), maximum_rounds=1)  # type: ignore[arg-type]

    assert result.stop_reason == "Stop-Error"
    assert result.diagnostics[-1].code == "EXECUTION-RESULT-TYPE-ERROR"
    assert result.state.resources.remaining == 1
    assert result.environment._state == "private-a1"


def test_valid_visible_record_is_retained_when_the_returned_successor_is_invalid() -> None:
    class InvalidSuccessorEnvironment:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            return EnvironmentExecution(
                VisibleExecutionRecord(
                    execution_attempt_id=request.execution_attempt_id,
                    action_id=request.action_id,
                    effect_class="NONE",
                    observable="branch-alpha",
                    summary_confirmed=True,
                    post_summary="branch-alpha",
                    measurement_tick=Fraction(0),
                    uncertainty_identity="synthetic-u-1",
                    evidence_ref="synthetic:invalid-successor:visible-record",
                ),
                object(),  # type: ignore[arg-type]
            )

    binding, model, _fixture = _runtime_parts()
    result = ReferenceSession(
        binding=binding, model=model, session_id="session-invalid-successor", run_id="run-invalid-successor",
        initial_summary="q0", resources=ResourceState.rounds(2),
    ).run(InvalidSuccessorEnvironment(), maximum_rounds=1)  # type: ignore[arg-type]

    assert result.stop_reason == "Stop-Error"
    assert result.diagnostics[-1].code == "EXECUTION-RESULT-TYPE-ERROR"
    assert result.state.resources.remaining == 1
    assert result.state.evidence[0].rejected_response is not None
    assert result.state.evidence[0].rejected_response.evidence_ref == "synthetic:invalid-successor:visible-record"


@pytest.mark.parametrize(
    "replacement",
    [
        {"effect_class": "IMPROVISED"},
        {"effect_class": ["NONE"]},
        {"effect_class": "NONE", "summary_confirmed": False},
        {"effect_class": "NONE", "summary_confirmed": "false"},
        {"effect_class": "NONE", "summary_confirmed": 1},
        {"effect_class": "UNKNOWN-EFFECT", "observable": "invented-visible-outcome"},
        {"effect_class": "CONFIRMED-NOT-SENT", "measurement_tick": Fraction(0)},
        {"effect_class": "NONE", "uncertainty_identity": None},
        {"effect_class": "NONE", "evidence_ref": ""},
        {"effect_class": "NONE", "evidence_ref": " \t "},
        {"effect_class": "NONE", "evidence_ref": "\t\r\n"},
    ],
)
def test_malformed_visible_record_combinations_are_controlled_post_dispatch_errors(
    replacement: dict[str, object],
) -> None:
    class MalformedVisibleRecordEnvironment:
        def __init__(self, successor: SyntheticEnvironment) -> None:
            self.successor = successor

        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            values: dict[str, object] = {
                "execution_attempt_id": request.execution_attempt_id,
                "action_id": request.action_id,
                "effect_class": "NONE",
                "observable": "branch-alpha",
                "summary_confirmed": True,
                "post_summary": "branch-alpha",
                "measurement_tick": Fraction(0),
                "uncertainty_identity": "synthetic-u-1",
                "evidence_ref": "synthetic:malformed-visible-record",
            }
            values.update(replacement)
            return EnvironmentExecution(VisibleExecutionRecord(**values), self.successor)  # type: ignore[arg-type]

    binding, model, fixture = _runtime_parts()
    successor = SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]).execute(
        ExecutionRequest("seed-session", "seed-execution", "test-router", "TEST"),
    ).successor
    result = ReferenceSession(
        binding=binding, model=model, session_id="session-visible-combination", run_id="run-visible-combination",
        initial_summary="q0", resources=ResourceState.rounds(2),
    ).run(MalformedVisibleRecordEnvironment(successor), maximum_rounds=1)  # type: ignore[arg-type]

    assert result.stop_reason == "Stop-Error"
    assert result.diagnostics[-1].code == "INVALID-EXECUTION-RECORD"
    assert result.state.resources.remaining == 1
    assert result.state.history.version == 1
    assert result.state.context.q_status == "UNKNOWN"
    assert set(result.state.history.status_by_hypothesis.values()) == {"CONSERVATIVE-UNKNOWN"}
    assert result.environment._state == "private-a1"
    assert result.state.evidence[0].rejected_response is not None


@pytest.mark.parametrize("failure_site", ["record-validation", "interpretation", "commit-preparation"])
@pytest.mark.parametrize(
    ("resources", "expected_remaining"),
    [(ResourceState.rounds(2), 1), (ResourceState.budget(2), 1)],
)
def test_post_dispatch_faults_keep_the_issued_charge_and_successor(
    monkeypatch: pytest.MonkeyPatch,
    failure_site: str,
    resources: ResourceState,
    expected_remaining: int,
) -> None:
    def fail(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError(f"controlled {failure_site} fault")

    if failure_site == "record-validation":
        monkeypatch.setattr("cltav_runtime.session._incoming_record_error", fail)
    elif failure_site == "interpretation":
        monkeypatch.setattr("cltav_runtime.session._matching_class", fail)
    else:
        monkeypatch.setattr(HistoryHandle, "committed", fail)

    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id=f"session-post-{failure_site}-{resources.mode}",
        run_id=f"run-post-{failure_site}-{resources.mode}", initial_summary="q0", resources=resources,
    )
    result = session.step(
        session.initial_state,
        SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]),
    )

    assert result.stop_reason == "Stop-Error"
    assert result.diagnostics[-1].code == "POST-DISPATCH-ERROR"
    assert result.state.attempts == 1
    assert result.state.resources == ResourceState(resources.mode, expected_remaining)
    assert result.state.history.hypotheses == session.initial_state.history.hypotheses
    assert result.state.history.compatible_state_by_hypothesis == session.initial_state.history.compatible_state_by_hypothesis
    assert result.state.history.version == session.initial_state.history.version + 1
    assert set(result.state.history.status_by_hypothesis.values()) == {"CONSERVATIVE-UNKNOWN"}
    assert result.state.context.q_status == "UNKNOWN"
    assert result.state.evidence[0].committed is False
    assert result.state.evidence[0].execution.execution_attempt_id.endswith(":execution:1")
    assert result.state.evidence[0].rejected_response is not None
    assert result.environment._state == "private-a1"
    resumed = session.step(result.state, result.environment)
    assert resumed.stop_reason == "Stop-Error"
    assert resumed.diagnostics[0].code == "TERMINAL-SESSION-STATE"
    assert resumed.state.attempts == 1


def test_nonblank_evidence_reference_is_preserved_in_a_normal_commit() -> None:
    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-evidence-preserved", run_id="run-evidence-preserved",
        initial_summary="q0", resources=ResourceState.rounds(1),
    )
    result = session.step(
        session.initial_state,
        SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]),
    )

    assert result.state.evidence[0].committed is True
    assert result.state.evidence[0].execution.evidence_ref == "synthetic:run-evidence-preserved:session-evidence-preserved:execution:1:none"


@pytest.mark.parametrize(
    ("effect_class", "observable", "summary_confirmed", "post_summary", "measurement_tick"),
    [
        ("NONE", "branch-alpha", True, "branch-alpha", Fraction(0)),
        ("CONFIRMED-NOT-SENT", None, False, None, None),
        ("UNKNOWN-EFFECT", None, False, None, None),
    ],
)
def test_wrong_action_identity_cannot_use_any_effect_branch(
    effect_class: str,
    observable: str | None,
    summary_confirmed: bool,
    post_summary: str | None,
    measurement_tick: Fraction | None,
) -> None:
    class WrongActionEnvironment:
        def __init__(self, successor: SyntheticEnvironment) -> None:
            self.successor = successor

        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            return EnvironmentExecution(
                VisibleExecutionRecord(
                    execution_attempt_id=request.execution_attempt_id,
                    action_id="foreign-action",
                    effect_class=effect_class,
                    observable=observable,
                    summary_confirmed=summary_confirmed,
                    post_summary=post_summary,
                    measurement_tick=measurement_tick,
                    uncertainty_identity=("synthetic-u-1" if effect_class == "NONE" else None),
                    evidence_ref=f"synthetic:foreign-action:{effect_class}",
                ),
                self.successor,
            )

    binding, model, fixture = _runtime_parts()
    successor = SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]).execute(
        ExecutionRequest("seed-session", "seed-execution", "test-router", "TEST"),
    ).successor
    result = ReferenceSession(
        binding=binding, model=model, session_id="session-cns-action", run_id="run-cns-action",
        initial_summary="q0", resources=ResourceState.rounds(2),
    ).run(WrongActionEnvironment(successor), maximum_rounds=1)  # type: ignore[arg-type]

    assert result.stop_reason == "Stop-Error"
    assert result.diagnostics[-1].code == "EXECUTION-IDENTITY-ERROR"
    assert result.state.context.q_status == "UNKNOWN"
    assert result.state.evidence[0].rejected_response is not None
    assert result.state.evidence[0].rejected_response.action_id == "foreign-action"


def test_observation_class_limit_is_a_prediction_gap_not_a_synthetic_visible_label() -> None:
    binding, model, fixture = _runtime_parts()
    limited_data = copy.deepcopy(fixture["algorithmModel"])
    limited_data["limits"]["observationClasses"] = 1
    limited = FiniteSessionModel.from_mapping(context=model.context, value=limited_data)
    prediction = limited.predict(
        hypotheses=frozenset(limited.initial_frontiers), frontiers=limited.initial_frontiers,
        status_by_hypothesis={}, action_id="test-router",
    )
    result = ReferenceSession(
        binding=binding, model=limited, session_id="session-class-limit", run_id="run-class-limit",
        initial_summary="q0", resources=ResourceState.rounds(1),
    ).run(SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]), maximum_rounds=1)

    assert prediction.classes == ()
    assert prediction.diagnostics[-1].code == "OBSERVATION-CLASS-LIMIT"
    assert result.stop_reason == "Stop-Prediction-Gap"
    assert result.state.evidence == ()


def test_conservative_hypothesis_is_retained_by_a_normal_visible_observation() -> None:
    _binding, model, _fixture = _runtime_parts()
    prediction = model.predict(
        hypotheses=frozenset(model.initial_frontiers),
        frontiers=model.initial_frontiers,
        status_by_hypothesis={
            hypothesis: "CONSERVATIVE-UNKNOWN" if hypothesis == "h3" else "KNOWN"
            for hypothesis in model.initial_frontiers
        },
        action_id="test-router",
    )
    alpha = next(item for item in prediction.classes if item.observable == "branch-alpha")

    assert alpha.hypotheses == {"h0", "h1", "h3"}
    assert alpha.conservative_hypotheses == {"h3"}


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
            "INVALID-HISTORY-HANDLE",
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
        hypothesis: tuple(frontier.history_provenance[-1] for frontier in bundle)
        for hypothesis, bundle in initial.frontiers.items()
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


def test_resume_rejects_a_malformed_frontier_bundle_with_a_named_diagnostic() -> None:
    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-malformed-bundle", run_id="run-malformed-bundle",
        initial_summary="q0", resources=ResourceState.rounds(2),
    )
    bundles = dict(session.initial_state.frontiers)
    bundles["h0"] = ()
    malformed = replace(session.initial_state, frontiers=bundles)

    result = session.step(malformed, SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]))

    assert result.stop_reason == "Stop-Error"
    assert result.diagnostics[0].code == "INVALID-FRONTIER-BUNDLE"
    assert result.state.resources.remaining == 2


def test_resumed_s0_requires_the_exact_frozen_authority_and_seed_before_dispatch() -> None:
    class NoDispatchEnvironment:
        calls = 0

        def execute(self, _request: ExecutionRequest) -> object:
            self.calls += 1
            raise AssertionError("foreign S0 must be rejected before dispatch")

    binding, model, _fixture = _runtime_parts()
    head = _head_commit()
    previous = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD^"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()
    foreign_binding = RuntimeAuthorityBinding.from_git_objects(
        repository=ROOT,
        development_commit=head,
        development_path=DEVELOPMENT_PATH,
        interface_commit=previous,
        interface_path=INTERFACE_PATH,
    )
    target = ReferenceSession(
        binding=binding, model=model, session_id="session-authority", run_id="run-authority",
        initial_summary="q0", resources=ResourceState.rounds(2),
    )
    foreign = ReferenceSession(
        binding=foreign_binding, model=model, session_id="session-authority", run_id="run-authority",
        initial_summary="q0", resources=ResourceState.rounds(2),
    )
    assert binding.identities() != foreign_binding.identities()
    assert target.initial_state.context == foreign.initial_state.context
    assert target.initial_state.authority_identity != foreign.initial_state.authority_identity
    records_before = dict(model.context.provenance_store.records())
    environment = NoDispatchEnvironment()

    rejected = target.step(foreign.initial_state, environment)  # type: ignore[arg-type]

    assert rejected.stop_reason == "Stop-Error"
    assert rejected.diagnostics[0].code == "SESSION-AUTHORITY-MISMATCH"
    assert rejected.state is foreign.initial_state
    assert rejected.state.attempts == 0
    assert rejected.state.resources.remaining == 2
    assert environment.calls == 0
    assert dict(model.context.provenance_store.records()) == records_before

    initial = model.initial_frontiers["h0"]
    alternate = initial_entry(
        model.context,
        hypothesis_id="h0",
        control_state_id="q1",
        clocks=initial.clocks,
        typed_store=initial.typed_store,
        root_id="root:h0:authority-seed-alternate",
    )
    declared_seed = {hypothesis: (frontier,) for hypothesis, frontier in model.initial_frontiers.items()}
    declared_seed["h0"] = (initial, alternate)
    other_seed = ReferenceSession(
        binding=binding, model=model, session_id="session-authority", run_id="run-authority",
        initial_summary="q0", resources=ResourceState.rounds(2), initial_path_bundles=declared_seed,
    )
    declared_seed["h0"] = (alternate,)
    assert other_seed.initial_state.frontiers["h0"] == (initial, alternate)
    rejected_seed = target.step(other_seed.initial_state, environment)  # type: ignore[arg-type]
    assert rejected_seed.diagnostics[0].code == "SESSION-SEED-MISMATCH"
    assert environment.calls == 0

    equivalent = ReferenceSession(
        binding=binding, model=model, session_id="session-authority", run_id="run-authority",
        initial_summary="q0", resources=ResourceState.rounds(2),
    ).initial_state
    accepted = target.step(equivalent, SyntheticEnvironment.from_mapping(_fixture["environments"]["alpha"]))
    assert accepted.state.attempts == 1
    assert accepted.state.authority_identity == target.initial_state.authority_identity
    assert accepted.state.seed_identity == target.initial_state.seed_identity
    completed = target.step(accepted.state, accepted.environment)
    assert completed.state.attempts == 2
    assert completed.state.authority_identity == target.initial_state.authority_identity
    assert completed.state.seed_identity == target.initial_state.seed_identity


def test_resume_replays_evidence_lineage_before_any_new_dispatch() -> None:
    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-lineage", run_id="run-lineage",
        initial_summary="q0", resources=ResourceState.rounds(2),
    )
    first = session.step(
        session.initial_state,
        SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]),
    )
    assert first.stop_reason is None
    original_records = dict(model.context.provenance_store.records())
    assert session._state_error(first.state) is None
    assert dict(model.context.provenance_store.records()) == original_records
    resumed = session.step(first.state, first.environment)
    assert resumed.state.attempts == 2

    replaced_roots = {
        hypothesis: session.initial_state.frontiers[hypothesis]
        for hypothesis in first.state.history.hypotheses
    }
    replaced_history = HistoryHandle.committed(
        hypotheses=set(replaced_roots),
        compatible_state_by_hypothesis={
            hypothesis: tuple(entry.history_provenance[-1] for entry in bundle)
            for hypothesis, bundle in replaced_roots.items()
        },
        status_by_hypothesis={hypothesis: "KNOWN" for hypothesis in replaced_roots},
        version=first.state.history.version,
    )
    altered_states = {
        "summary": replace(first.state, context=replace(first.state.context, current_summary="q0")),
        "resource": replace(first.state, resources=ResourceState.rounds(100)),
        "status": replace(first.state, history=replace(first.state.history, status_by_hypothesis={
            hypothesis: "BOGUS" for hypothesis in first.state.history.hypotheses
        })),
        "frontier": replace(first.state, history=replaced_history, frontiers=replaced_roots),
        "evidence": replace(first.state, evidence=(replace(
            first.state.evidence[0], snapshot=replace(first.state.evidence[0].snapshot, action_id="test-overlap"),
        ),)),
    }
    for name, altered in altered_states.items():
        rejected = session.step(altered, first.environment)
        assert rejected.stop_reason == "Stop-Error", name
        assert rejected.state is altered
        assert rejected.state.resources == altered.resources
        assert rejected.environment is first.environment
        assert rejected.diagnostics[0].code in {
            "INVALID-HISTORY-HANDLE", "SESSION-LINEAGE-MISMATCH", "SNAPSHOT-IDENTITY-MISMATCH",
            "EVIDENCE-ADMISSION-MISMATCH", "RESOURCE-CONTEXT-MISMATCH",
        }, name


def test_equivalent_fresh_context_resumes_a_complete_public_checkpoint_without_cache_rehydration() -> None:
    source_binding, source_model, fixture = _runtime_parts()
    source = ReferenceSession(
        binding=source_binding, model=source_model, session_id="session-portable", run_id="run-portable",
        initial_summary="q0", resources=ResourceState.rounds(2),
    )
    first = source.step(
        source.initial_state,
        SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]),
    )
    assert first.stop_reason is None
    assert first.state.attempts == 1
    cached_resumed = source.step(first.state, first.environment)
    assert cached_resumed.stop_reason == "Stop-Singleton"

    # Build an equivalent authority/model context with a distinct local
    # provenance cache.  It owns the same S0 records but has not executed the
    # first round and therefore cannot contain the retained derived records.
    target_binding, target_model, _target_fixture = _runtime_parts()
    target = ReferenceSession(
        binding=target_binding, model=target_model, session_id="session-portable", run_id="run-portable",
        initial_summary="q0", resources=ResourceState.rounds(2),
    )
    assert target.initial_state.authority_identity == first.state.authority_identity
    assert target.initial_state.seed_identity == first.state.seed_identity
    target_records_before = dict(target_model.context.provenance_store.records())

    # Causal replay accepts the public checkpoint without rehydrating the
    # target's shared store.  Its actual successor calculation must use the
    # detached verified replay context, rather than treating the cache miss as
    # a prediction gap.
    assert target._state_error(first.state) is None
    assert dict(target_model.context.provenance_store.records()) == target_records_before
    resumed = target.step(first.state, first.environment)

    assert resumed.stop_reason == "Stop-Singleton"
    assert resumed.state.attempts == 2
    assert [item.snapshot.action_id for item in resumed.state.evidence] == ["test-router", "test-left"]
    assert resumed.state == cached_resumed.state
    assert target._state_error(resumed.state) is None
    assert dict(target_model.context.provenance_store.records()) == target_records_before


def test_fresh_context_rejects_truncated_or_forged_portable_checkpoint_before_dispatch() -> None:
    class NoDispatchEnvironment:
        calls = 0

        def execute(self, _request: ExecutionRequest) -> object:
            self.calls += 1
            raise AssertionError("invalid public checkpoint must be rejected before dispatch")

    source_binding, source_model, fixture = _runtime_parts()
    source = ReferenceSession(
        binding=source_binding, model=source_model, session_id="session-portable-negative", run_id="run-portable-negative",
        initial_summary="q0", resources=ResourceState.rounds(2),
    )
    first = source.step(
        source.initial_state,
        SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]),
    )
    target_binding, target_model, _target_fixture = _runtime_parts()
    target = ReferenceSession(
        binding=target_binding, model=target_model, session_id="session-portable-negative", run_id="run-portable-negative",
        initial_summary="q0", resources=ResourceState.rounds(2),
    )
    forged_bundles = dict(first.state.frontiers)
    original = forged_bundles["h0"][0]
    forged_bundles["h0"] = (replace(
        original,
        history_provenance=(original.history_provenance[0], "forged-portable-step-reference"),
    ),)
    forged_references = {
        hypothesis: tuple(entry.history_provenance[-1] for entry in bundle)
        for hypothesis, bundle in forged_bundles.items()
    }
    forged = replace(
        first.state,
        history=replace(first.state.history, compatible_state_by_hypothesis=forged_references),
        frontiers=forged_bundles,
    )
    # Coherently remove the causal round bookkeeping while retaining its
    # claimed post-round context/history/frontier state.  This reaches the
    # replay closure comparison rather than only a shape check.
    truncated = replace(
        first.state,
        attempts=0,
        processed_execution_attempt_ids=frozenset(),
        evidence=(),
    )
    target_records_before = dict(target_model.context.provenance_store.records())
    environment = NoDispatchEnvironment()

    for candidate in (truncated, forged):
        rejected = target.step(candidate, environment)  # type: ignore[arg-type]
        assert rejected.stop_reason == "Stop-Error"
        assert rejected.state is candidate
        assert rejected.diagnostics[0].code == "SESSION-LINEAGE-MISMATCH"

    assert environment.calls == 0
    assert dict(target_model.context.provenance_store.records()) == target_records_before


def test_duplicate_execution_evidence_is_rejected_before_another_charge_or_dispatch() -> None:
    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-duplicate-evidence", run_id="run-duplicate-evidence",
        initial_summary="q0", resources=ResourceState.rounds(2),
    )
    first = session.step(
        session.initial_state,
        SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]),
    )
    # A separately constructed but type-exact visible record is still the
    # same completed transport delivery.  This must not depend on object
    # identity or on whatever action would be admitted next.
    duplicate_delivery = first.environment.with_pending_delivery(replace(first.state.evidence[0].execution))
    discarded = session.step(first.state, duplicate_delivery)

    # The receipt is handled before S3/S4: no new request, charge or ledger
    # record exists.  The returned environment has consumed only the inbound
    # duplicate, so a subsequent call can issue the genuine next action.
    assert discarded.stop_reason is None
    assert discarded.state is first.state
    assert discarded.diagnostics[0].code == "DUPLICATE-EXECUTION-EVIDENCE"
    assert discarded.state.resources == first.state.resources
    assert discarded.state.history == first.state.history
    assert discarded.state.evidence == first.state.evidence

    continued = session.step(discarded.state, discarded.environment)
    assert len(continued.state.evidence) == len(first.state.evidence) + 1
    assert continued.state.resources.remaining == first.state.resources.remaining - 1


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("measurement_tick", 0),
        ("measurement_tick", 0.0),
        ("measurement_tick", False),
        ("summary_confirmed", 1),
    ],
)
def test_pending_duplicate_requires_type_exact_closed_record(
    field: str,
    value: object,
) -> None:
    """Python numeric equality cannot turn malformed ingress into a duplicate."""

    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-typed-duplicate", run_id="run-typed-duplicate",
        initial_summary="q0", resources=ResourceState.rounds(2),
    )
    first = session.step(
        session.initial_state,
        SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]),
    )
    canonical = first.state.evidence[0].execution
    forged = replace(canonical, **{field: value})
    # This deliberately documents the old bypass precondition.
    assert forged == canonical

    rejected = session.step(first.state, first.environment.with_pending_delivery(forged))

    assert rejected.stop_reason == "Stop-Error"
    assert rejected.diagnostics[0].code == "CONFLICTING-EXECUTION-DELIVERY"
    assert rejected.state is first.state
    assert rejected.state.resources == first.state.resources
    assert rejected.state.history == first.state.history
    assert rejected.state.evidence == first.state.evidence


def test_conflicting_pending_execution_delivery_is_rejected_without_admission_or_charge() -> None:
    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-conflicting-delivery", run_id="run-conflicting-delivery",
        initial_summary="q0", resources=ResourceState.rounds(2),
    )
    first = session.step(
        session.initial_state,
        SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]),
    )
    forged = replace(
        first.state.evidence[0].execution,
        observable="forged-observation",
        post_summary="forged-summary",
        evidence_ref="synthetic:forged-delivery",
    )

    rejected = session.step(first.state, first.environment.with_pending_delivery(forged))

    assert rejected.stop_reason == "Stop-Error"
    assert rejected.diagnostics[0].code == "CONFLICTING-EXECUTION-DELIVERY"
    assert rejected.state is first.state
    assert rejected.state.resources == first.state.resources
    assert rejected.state.history == first.state.history
    assert rejected.state.evidence == first.state.evidence


def test_terminal_ledger_refuses_even_an_exact_pending_duplicate_delivery() -> None:
    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-terminal-duplicate", run_id="run-terminal-duplicate",
        initial_summary="q0", resources=ResourceState.rounds(2), retry_cap=1,
    )
    terminal = session.step(
        session.initial_state,
        SyntheticEnvironment.from_mapping(fixture["environments"]["notSent"]),
    )
    assert terminal.stop_reason == "Stop-Error"
    pending_duplicate = terminal.environment.with_pending_delivery(terminal.state.evidence[0].execution)

    replayed = session.step(terminal.state, pending_duplicate)

    assert replayed.stop_reason == "Stop-Error"
    assert replayed.diagnostics[0].code == "TERMINAL-SESSION-STATE"
    assert replayed.state is terminal.state
    assert replayed.environment is pending_duplicate


def test_synthetic_environment_detaches_nested_measurement_configuration() -> None:
    declaration = {
        "initialPrivateState": "private-0",
        "uncertaintyIdentity": "synthetic-u-1",
        "states": {
            "private-0": {
                "test-router": {
                    "effectClass": "NONE",
                    "observable": "branch-alpha",
                    "summaryConfirmed": True,
                    "postSummary": "branch-alpha",
                    "measurementTick": {"numerator": 0, "positiveDenominator": 1},
                    "nextPrivateState": "private-0",
                },
            },
        },
    }
    environment = SyntheticEnvironment.from_mapping(declaration)
    declaration["states"]["private-0"]["test-router"]["measurementTick"]["numerator"] = 5

    execution = environment.execute(ExecutionRequest("session-freeze", "execution-freeze", "test-router", "TEST"))

    assert execution.record.measurement_tick == Fraction(0)


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
    assert result.state.history.version == 1
    assert result.state.context.q_status == "UNKNOWN"
    assert set(result.state.history.status_by_hypothesis.values()) == {"CONSERVATIVE-UNKNOWN"}


def test_one_infeasible_path_does_not_exclude_a_hypothesis_with_another_feasible_path() -> None:
    _binding, model, _fixture = _runtime_parts()
    h0 = model.initial_frontiers["h0"]
    alternate = initial_entry(
        model.context,
        hypothesis_id="h0",
        control_state_id="q1",
        clocks=h0.clocks,
        typed_store=h0.typed_store,
        root_id="root:h0:infeasible-router-path",
    )
    bundles = {hypothesis: (frontier,) for hypothesis, frontier in model.initial_frontiers.items()}
    bundles["h0"] = (h0, alternate)
    prediction = model.predict(
        hypotheses=frozenset(bundles), frontiers=bundles,
        status_by_hypothesis={}, action_id="test-router",
    )
    alpha = next(item for item in prediction.classes if item.observable == "branch-alpha")

    assert alpha.hypotheses == {"h0", "h1"}
    assert len(alpha.successors["h0"]) == 1


def test_declared_initial_multi_path_seed_is_bound_to_one_session() -> None:
    binding, model, fixture = _runtime_parts()
    initial = model.initial_frontiers["h0"]
    alternate = initial_entry(
        model.context,
        hypothesis_id="h0",
        control_state_id="q1",
        clocks=initial.clocks,
        typed_store=initial.typed_store,
        root_id="root:h0:declared-alternate",
    )
    seed = {hypothesis: (frontier,) for hypothesis, frontier in model.initial_frontiers.items()}
    seed["h0"] = (initial, alternate)
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-declared-seed", run_id="run-declared-seed",
        initial_summary="q0", resources=ResourceState.rounds(1), initial_path_bundles=seed,
    )

    result = session.step(session.initial_state, SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]))

    assert result.stop_reason is None
    assert result.state.history.hypotheses == {"h0", "h1"}
    assert len(result.state.frontiers["h0"]) == 1


def test_declared_initial_multi_path_seed_allows_verified_unequal_path_lengths() -> None:
    binding, model, _fixture = _runtime_parts()
    initial = model.initial_frontiers["h0"]
    advanced = propagate_transition(
        initial,
        model.actions["test-router"].transition_for_kernel(),
        state_ids=set(model.context.state_ids),
        clock_ids=set(model.context.clock_ids),
        typed_domains={key: set(value) for key, value in model.context.typed_domains.items()},
        context=model.context,
        path_limit=model.path_limit,
        frontier_limit=model.frontier_limit,
    )
    assert advanced.kind == "FEASIBLE"
    seed = {hypothesis: (frontier,) for hypothesis, frontier in model.initial_frontiers.items()}
    seed["h0"] = (initial, advanced.entries[0])
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-unequal-seed", run_id="run-unequal-seed",
        initial_summary="q0", resources=ResourceState.rounds(1), initial_path_bundles=seed,
    )

    assert [path.path_length for path in session.initial_state.frontiers["h0"]] == [0, 1]
    assert session._state_error(session.initial_state) is None


def test_unknown_path_is_retained_with_a_feasible_path_and_not_upgraded_to_known() -> None:
    _binding, model, _fixture = _runtime_parts()
    long_path = model.initial_frontiers["h0"]
    router_transition = model.actions["test-router"].transition_for_kernel()
    for _ in range(model.path_limit):
        propagated = propagate_transition(
            long_path,
            router_transition,
            state_ids=set(model.context.state_ids),
            clock_ids=set(model.context.clock_ids),
            typed_domains={key: set(value) for key, value in model.context.typed_domains.items()},
            context=model.context,
            path_limit=model.path_limit + 1,
            frontier_limit=model.frontier_limit,
        )
        assert propagated.kind == "FEASIBLE"
        long_path = propagated.entries[0]
    bundles = {hypothesis: (frontier,) for hypothesis, frontier in model.initial_frontiers.items()}
    bundles["h0"] = (model.initial_frontiers["h0"], long_path)
    prediction = model.predict(
        hypotheses=frozenset(bundles), frontiers=bundles,
        status_by_hypothesis={}, action_id="test-router",
    )
    alpha = next(item for item in prediction.classes if item.observable == "branch-alpha")

    assert alpha.hypotheses == {"h0", "h1"}
    assert alpha.conservative_hypotheses == {"h0"}
    assert len(alpha.successors["h0"]) == 2
