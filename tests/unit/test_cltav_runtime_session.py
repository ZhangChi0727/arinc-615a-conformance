"""Two-round bounded session integration checks without an IUT or network."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess

import pytest

from cltav_runtime.bindings import RuntimeAuthorityBinding
from cltav_runtime.kernel import ContractSnapshot, ModelContext
from cltav_runtime.model import FiniteSessionModel
from cltav_runtime.session import ReferenceSession, ResourceState
from cltav_runtime.synthetic import ExecutionRequest, SyntheticEnvironment


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
        action_id="test-overlap",
    )
    gap = model.predict(
        hypotheses=frozenset(model.initial_frontiers),
        frontiers=model.initial_frontiers,
        action_id="test-gap",
    )

    assert {item.observable: item.hypotheses for item in overlap.classes}["overlap-shared"] == {"h0", "h2"}
    assert overlap.has_distinguishing_value is True
    assert gap.classes == ()


def test_unaffordable_best_test_and_no_information_test_do_not_displace_router() -> None:
    binding, model, fixture = _runtime_parts()
    result = ReferenceSession(
        binding=binding,
        model=model,
        session_id="session-affordability",
        run_id="run-affordability",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
    ).run(SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]), maximum_rounds=1)

    assert result.state.evidence[0].snapshot.action_id == "test-router"
    assert result.state.evidence[0].snapshot.action_id != "test-no-information"


def test_current_test_gap_is_named_and_eligible_prep_uses_the_same_admission_entry() -> None:
    binding, model, fixture = _runtime_parts()
    gap_only = copy.deepcopy(fixture["algorithmModel"])
    gap_only["actions"] = [
        item for item in gap_only["actions"] if item["id"] == "test-gap"
    ]
    gap_only["limits"]["actions"] = 1
    gap_model = FiniteSessionModel.from_mapping(context=model.context, value=gap_only)
    gap_result = ReferenceSession(
        binding=binding, model=gap_model, session_id="session-gap", run_id="run-gap",
        initial_summary="q0", resources=ResourceState.rounds(1),
    ).run(SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]), maximum_rounds=1)
    assert gap_result.stop_reason == "Stop-Prediction-Gap"

    with_prep = copy.deepcopy(gap_only)
    with_prep["actions"].append(
        {
            "id": "prep-after-gap",
            "kind": "PREP",
            "cost": 1,
            "detailCharges": {"acquisition": 0, "computation": 0, "preparation": 1, "recovery": 0, "retry": 0},
            "enabledSummaries": ["q0"],
            "transition": {"id": "tr-prep", "source": "q0", "target": "q0", "guardAst": {"tag": "TRUE"}, "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q0"}]},
            "observableByHypothesis": {"h0": "prep-summary", "h1": "prep-summary", "h2": "prep-summary", "h3": "prep-summary"},
        },
    )
    with_prep["limits"]["actions"] = 2
    prep_model = FiniteSessionModel.from_mapping(context=model.context, value=with_prep)
    prep_environment = SyntheticEnvironment.from_mapping(
        {
            "initialPrivateState": "private-prep",
            "states": {
                "private-prep": {
                    "prep-after-gap": {"effectClass": "NONE", "observable": "prep-summary", "summaryConfirmed": True, "nextPrivateState": "private-prep"}
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
