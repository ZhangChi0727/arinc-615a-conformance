"""B/C-2A public session tests for Prep, Recover, S7, S8, and S9.

These cases intentionally use the public :class:`ReferenceSession` boundary
and synthetic execution environment.  They do not exercise a private helper
or introduce evaluator truth: every branch is driven by a visible return from
the bounded synthetic adapter.
"""

from __future__ import annotations

import copy
from dataclasses import replace
from fractions import Fraction
import json
from pathlib import Path
import subprocess

import pytest

from cltav_runtime.bindings import RuntimeAuthorityBinding
from cltav_runtime.kernel import ContractSnapshot, ModelContext
from cltav_runtime.model import FiniteSessionModel
from cltav_runtime.session import ReferenceSession, ResourceState
from cltav_runtime.synthetic import (
    EnvironmentExecution,
    ExecutionRequest,
    PrepRecoverResult,
    SyntheticEnvironment,
    VisibleExecutionRecord,
)


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
    model = FiniteSessionModel.from_mapping(context=context, value=fixture["algorithmModel"])
    return binding, model, fixture


def _action(
    fixture: dict[str, object],
    source_id: str,
    *,
    action_id: str,
    kind: str,
    enabled_summaries: list[str],
    cost: int = 1,
    declared_target: str | None = None,
    recover_when_unknown: bool = False,
) -> dict[str, object]:
    """Build one deliberately small action from the controlled B/C-1 fixture."""

    algorithm = fixture["algorithmModel"]
    assert isinstance(algorithm, dict)
    raw_actions = algorithm["actions"]
    assert isinstance(raw_actions, list)
    result = copy.deepcopy(next(item for item in raw_actions if item["id"] == source_id))
    result["id"] = action_id
    result["kind"] = kind
    result["cost"] = cost
    result["enabledSummaries"] = enabled_summaries
    transition = result["transition"]
    assert isinstance(transition, dict)
    transition["id"] = f"tr-{action_id}"
    if kind in {"PREP", "RECOVER"}:
        assert declared_target is not None
        result["declaredTarget"] = declared_target
        result["recoverWhenUnknown"] = recover_when_unknown
        result["detailCharges"] = {
            "acquisition": 0,
            "computation": 0,
            "preparation": 1 if kind == "PREP" else 0,
            "recovery": 1 if kind == "RECOVER" else 0,
            "retry": 0,
        }
    return result


def _model_with(
    base: FiniteSessionModel,
    fixture: dict[str, object],
    actions: list[dict[str, object]],
) -> FiniteSessionModel:
    model_data = copy.deepcopy(fixture["algorithmModel"])
    assert isinstance(model_data, dict)
    model_data["actions"] = actions
    limits = model_data["limits"]
    assert isinstance(limits, dict)
    limits["actions"] = len(actions)
    return FiniteSessionModel.from_mapping(context=base.context, value=model_data)


def _environment(
    states: dict[str, dict[str, dict[str, object]]],
    *,
    initial: str = "private-0",
) -> SyntheticEnvironment:
    # The synthetic adapter deliberately validates a total declared private
    # state graph, even when a successor is terminal for this public session.
    # Supply unreachable self-loop declarations for such private successors;
    # the model never owns or selects this idle action.
    completed = copy.deepcopy(states)
    successors = {
        outcome["nextPrivateState"]
        for actions in completed.values()
        for outcome in actions.values()
    }
    for state in successors - set(completed):
        completed[state] = {"__synthetic-idle__": _not_sent(state)}
    return SyntheticEnvironment.from_mapping({
        "initialPrivateState": initial,
        "uncertaintyIdentity": "synthetic-u-1",
        "states": completed,
    })


def _normal(
    observable: str,
    summary: str,
    next_state: str,
    *,
    tick: int = 0,
) -> dict[str, object]:
    return {
        "effectClass": "NONE",
        "observable": observable,
        "summaryConfirmed": True,
        "postSummary": summary,
        "measurementTick": tick,
        "nextPrivateState": next_state,
    }


def _not_sent(next_state: str) -> dict[str, object]:
    return {
        "effectClass": "CONFIRMED-NOT-SENT",
        "observable": None,
        "summaryConfirmed": False,
        "postSummary": None,
        "measurementTick": None,
        "nextPrivateState": next_state,
    }


def _unknown(next_state: str) -> dict[str, object]:
    return {
        "effectClass": "UNKNOWN-EFFECT",
        "observable": None,
        "summaryConfirmed": False,
        "postSummary": None,
        "measurementTick": None,
        "nextPrivateState": next_state,
    }


def _prep_recover(
    *,
    target_confirmed: bool,
    summary_confirmed: bool,
    prep_error: bool,
    ineligible: bool,
    declared_target: str,
    evidence: str,
    post_summary: str | None,
    next_state: str,
    observable: str | None = None,
    tick: int | None = None,
) -> dict[str, object]:
    return {
        "effectClass": "NONE",
        "observable": observable,
        "summaryConfirmed": summary_confirmed,
        "postSummary": post_summary,
        "measurementTick": tick,
        "nextPrivateState": next_state,
        "prepRecover": {
            "targetConfirmed": target_confirmed,
            "summaryConfirmed": summary_confirmed,
            "prepError": prep_error,
            "ineligible": ineligible,
            "declaredTarget": declared_target,
            "evidence": evidence,
            "postSummary": post_summary,
        },
    }


def _gap_and_prep_model(
    binding: RuntimeAuthorityBinding,
    base: FiniteSessionModel,
    fixture: dict[str, object],
) -> FiniteSessionModel:
    # ``test-gap`` is deliberately inapplicable at q0 and creates the named
    # current prediction gap which admits the valid Prep fallback.
    gap = _action(fixture, "test-gap", action_id="test-gap-q0", kind="TEST", enabled_summaries=["q0"])
    prep = _action(
        fixture, "test-router", action_id="prep-q0", kind="PREP", enabled_summaries=["q0"],
        declared_target="prepared-q1",
    )
    next_test = _action(
        fixture, "test-router", action_id="test-q1", kind="TEST", enabled_summaries=["q1"],
    )
    return _model_with(base, fixture, [gap, prep, next_test])


def _router_recover_model(
    base: FiniteSessionModel,
    fixture: dict[str, object],
    *,
    recover_cost: int = 1,
    eligible: bool = True,
) -> FiniteSessionModel:
    router = _action(fixture, "test-router", action_id="test-q0", kind="TEST", enabled_summaries=["q0"])
    recover = _action(
        fixture, "test-router", action_id="recover-q", kind="RECOVER", enabled_summaries=["q0"],
        cost=recover_cost,
        declared_target="recovered-q1",
        recover_when_unknown=eligible,
    )
    return _model_with(base, fixture, [router, recover])


def test_prep_target_miss_with_confirmed_summary_commits_s9_and_next_round_reads_it() -> None:
    binding, base, fixture = _runtime_parts()
    model = _gap_and_prep_model(binding, base, fixture)
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-prep-summary", run_id="run-prep-summary",
        initial_summary="q0", resources=ResourceState.rounds(3), retry_cap=2,
    )
    environment = _environment({
        "private-0": {
            "prep-q0": _prep_recover(
                target_confirmed=False, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="prepared-q1", evidence="synthetic:prep:q1", post_summary="q1",
                next_state="private-1",
            ),
        },
        "private-1": {"test-q1": _normal("branch-alpha", "branch-alpha", "private-2")},
    })

    first = session.step(session.initial_state, environment)
    assert first.stop_reason is None
    assert first.state.evidence[0].snapshot.action_id == "prep-q0"
    assert first.state.evidence[0].resolution_code == "COMMIT"
    assert first.state.context.q_status == "KNOWN"
    assert first.state.context.current_summary == "q1"
    assert first.state.context.known_target is None
    assert first.state.history.hypotheses == session.initial_state.history.hypotheses
    assert first.state.history.version == 1
    # IF-HIST-UPDATE receives no Iz here: it advances the operation-history
    # version but must not fabricate a model path/provenance transition.
    assert first.state.history.compatible_state_by_hypothesis == session.initial_state.history.compatible_state_by_hypothesis
    assert first.state.frontiers == session.initial_state.frontiers

    # Public resumption must replay the ledger before the later selection; it
    # cannot continue to score against q0.
    second = session.step(first.state, first.environment)
    assert second.state.evidence[-1].snapshot.action_id == "test-q1"
    assert second.state.evidence[-1].snapshot.q_used_at_select == "q1"


def test_normal_test_commits_explicit_successor_summary_not_observation() -> None:
    binding, base, fixture = _runtime_parts()
    q0_test = _action(fixture, "test-router", action_id="test-q0", kind="TEST", enabled_summaries=["q0"])
    # The second action must still distinguish the two hypotheses left by
    # ``branch-alpha``; copying ``test-left`` ensures that q1 selection is
    # observable rather than ending legitimately at Stop-No-Action.
    q1_test = _action(fixture, "test-left", action_id="test-q1", kind="TEST", enabled_summaries=["q1"])
    model = _model_with(base, fixture, [q0_test, q1_test])
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-distinct-summary", run_id="run-distinct-summary",
        initial_summary="q0", resources=ResourceState.rounds(4), retry_cap=2,
    )
    environment = _environment({
        "private-0": {"test-q0": _normal("branch-alpha", "q1", "private-1")},
        "private-1": {"test-q1": _normal("branch-alpha", "q1", "private-2")},
    })

    first = session.step(session.initial_state, environment)
    assert first.stop_reason is None
    assert first.state.evidence[-1].execution.observable == "branch-alpha"
    assert first.state.evidence[-1].execution.post_summary == "q1"
    assert first.state.context.current_summary == "q1"

    # Public state replay must retain the explicit q1, not reconstruct q from
    # the distinct observation label.
    second = session.step(first.state, first.environment)
    assert second.stop_reason is None
    assert second.state.evidence[-1].snapshot.action_id == "test-q1"
    assert second.state.evidence[-1].snapshot.q_used_at_select == "q1"


def test_synthetic_normal_test_requires_an_explicit_successor_summary() -> None:
    with pytest.raises(ValueError, match="explicit successor summary"):
        SyntheticEnvironment.from_mapping({
            "initialPrivateState": "private-0",
            "uncertaintyIdentity": "synthetic-u-1",
            "states": {
                "private-0": {
                    "test-q0": {
                        "effectClass": "NONE", "observable": "branch-alpha",
                        "summaryConfirmed": True, "measurementTick": 0,
                        "nextPrivateState": "private-0",
                    },
                },
            },
        })


@pytest.mark.parametrize("target_confirmed", [False, True])
def test_unconfirmed_prep_uses_s7_and_keeps_candidates_for_recovery(target_confirmed: bool) -> None:
    binding, base, fixture = _runtime_parts()
    model = _gap_and_prep_model(binding, base, fixture)
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-prep-s7", run_id="run-prep-s7",
        initial_summary="q0", resources=ResourceState.rounds(2), retry_cap=2,
    )
    result = session.step(session.initial_state, _environment({
        "private-0": {
            "prep-q0": _prep_recover(
                target_confirmed=target_confirmed, summary_confirmed=False, prep_error=False, ineligible=False,
                declared_target="prepared-q1", evidence="synthetic:prep:unconfirmed", post_summary=None,
                next_state="private-1",
            ),
        },
    }))

    assert result.stop_reason is None
    assert result.diagnostics[-1].code == "PREP-SUMMARY-UNCONFIRMED"
    assert result.state.context.q_status == "UNKNOWN"
    assert result.state.context.current_summary is None
    assert result.state.context.retry_count == 1
    assert result.state.history.hypotheses == session.initial_state.history.hypotheses
    assert set(result.state.history.status_by_hypothesis.values()) == {"CONSERVATIVE-UNKNOWN"}
    assert result.state.evidence[0].resolution_code == "PREP-SUMMARY-UNCONFIRMED"


@pytest.mark.parametrize(("prep_error", "ineligible"), [(True, False), (False, True)])
def test_declared_prep_failure_or_ineligibility_uses_s7(
    prep_error: bool,
    ineligible: bool,
) -> None:
    binding, base, fixture = _runtime_parts()
    model = _gap_and_prep_model(binding, base, fixture)
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-prep-declared-error", run_id="run-prep-declared-error",
        initial_summary="q0", resources=ResourceState.rounds(2), retry_cap=2,
    )
    result = session.step(session.initial_state, _environment({
        "private-0": {
            "prep-q0": _prep_recover(
                target_confirmed=False, summary_confirmed=False, prep_error=prep_error, ineligible=ineligible,
                declared_target="prepared-q1", evidence="synthetic:prep:declared-error", post_summary=None,
                next_state="private-1",
            ),
        },
    }))

    assert result.stop_reason is None
    assert result.diagnostics[-1].code == "PREP-RECOVER-ERROR"
    assert result.state.evidence[-1].resolution_code == "PREP-RECOVER-ERROR"
    assert result.state.context.q_status == "UNKNOWN"
    assert result.state.context.current_summary is None
    assert result.state.history.hypotheses == session.initial_state.history.hypotheses
    assert set(result.state.history.status_by_hypothesis.values()) == {"CONSERVATIVE-UNKNOWN"}


def test_unknown_session_admits_confirmed_recover_and_only_s8_sets_target_evidence() -> None:
    binding, base, fixture = _runtime_parts()
    model = _router_recover_model(base, fixture)
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-recover", run_id="run-recover",
        initial_summary="q0", resources=ResourceState.rounds(3), retry_cap=2,
    )
    environment = _environment({
        "private-0": {"test-q0": _unknown("private-1")},
        "private-1": {
            "recover-q": _prep_recover(
                target_confirmed=True, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="recovered-q1", evidence="synthetic:recover:target", post_summary="q1",
                next_state="private-2",
            ),
        },
    })

    unknown = session.step(session.initial_state, environment)
    assert unknown.stop_reason is None
    assert unknown.state.context.q_status == "UNKNOWN"
    assert unknown.state.context.current_summary is None
    assert unknown.state.context.known_target is None

    recovered = session.step(unknown.state, unknown.environment)
    assert recovered.stop_reason is None
    evidence = recovered.state.evidence[-1]
    assert evidence.snapshot.action_id == "recover-q"
    assert evidence.snapshot.q_used_at_select is None
    assert evidence.resolution_code == "COMMIT"
    assert recovered.state.context.q_status == "KNOWN"
    assert recovered.state.context.current_summary == "q1"
    assert recovered.state.context.known_target == "recovered-q1"
    assert recovered.state.context.known_evidence == ("synthetic:recover:target",)
    # S8 restores session-level knownness only.  Without a valid Iz it must
    # retain the S7-conservative HistoryHandle/frontier provenance.
    assert recovered.state.history.compatible_state_by_hypothesis == unknown.state.history.compatible_state_by_hypothesis
    assert recovered.state.history.status_by_hypothesis == unknown.state.history.status_by_hypothesis
    assert recovered.state.frontiers == unknown.state.frontiers
    # A public continuation first replays this S8/S9 state.  The model has no
    # q1 action, so a normal admission stop (rather than lineage rejection)
    # proves the recovery result is a resumable public checkpoint.
    follow_on = session.step(recovered.state, recovered.environment)
    assert follow_on.stop_reason == "Stop-No-Action"

    class NoDispatchEnvironment:
        calls = 0

        def execute(self, _request: ExecutionRequest) -> object:
            self.calls += 1
            raise AssertionError("forged S8 ownership must be rejected before dispatch")

    forged = replace(
        recovered.state,
        context=replace(recovered.state.context, known_target="forged-target"),
    )
    no_dispatch = NoDispatchEnvironment()
    rejected = session.step(forged, no_dispatch)  # type: ignore[arg-type]
    assert rejected.stop_reason == "Stop-Error"
    assert rejected.state is forged
    assert rejected.diagnostics[0].code == "SESSION-LINEAGE-MISMATCH"
    assert no_dispatch.calls == 0


def test_unconfirmed_recover_stays_on_s7_and_cannot_write_s8_or_s9() -> None:
    binding, base, fixture = _runtime_parts()
    model = _router_recover_model(base, fixture)
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-recover-unconfirmed", run_id="run-recover-unconfirmed",
        initial_summary="q0", resources=ResourceState.rounds(3), retry_cap=3,
    )
    environment = _environment({
        "private-0": {"test-q0": _unknown("private-1")},
        "private-1": {
            # Prep is allowed to have this combination, but Recover is not:
            # it cannot restore KNOWN or commit the otherwise confirmed q1.
            "recover-q": _prep_recover(
                target_confirmed=False, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="recovered-q1", evidence="synthetic:recover:not-target", post_summary="q1",
                next_state="private-2",
            ),
        },
    })
    unknown = session.step(session.initial_state, environment)
    result = session.step(unknown.state, unknown.environment)

    assert result.stop_reason is None
    assert result.diagnostics[-1].code == "RECOVER-TARGET-UNCONFIRMED"
    assert result.state.evidence[-1].resolution_code == "RECOVER-TARGET-UNCONFIRMED"
    assert result.state.context.q_status == "UNKNOWN"
    assert result.state.context.current_summary is None
    assert result.state.context.known_target is None
    assert result.state.context.known_evidence == ()
    assert result.state.history.hypotheses == session.initial_state.history.hypotheses
    assert set(result.state.history.status_by_hypothesis.values()) == {"CONSERVATIVE-UNKNOWN"}


def test_target_only_recover_is_a_valid_unconfirmed_result_and_uses_s7() -> None:
    """Target confirmation alone is not malformed and cannot enter S8/S9."""

    binding, base, fixture = _runtime_parts()
    model = _router_recover_model(base, fixture)
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-recover-target-only", run_id="run-recover-target-only",
        initial_summary="q0", resources=ResourceState.rounds(3), retry_cap=3,
    )
    unknown = session.step(session.initial_state, _environment({
        "private-0": {"test-q0": _unknown("private-1")},
    }))

    class TargetOnlyRecoverEnvironment:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            return EnvironmentExecution(
                VisibleExecutionRecord(
                    execution_attempt_id=request.execution_attempt_id,
                    action_id=request.action_id,
                    effect_class="NONE",
                    observable=None,
                    summary_confirmed=False,
                    post_summary=None,
                    measurement_tick=None,
                    uncertainty_identity=None,
                    evidence_ref="synthetic:recover:target-only",
                    prep_recover=PrepRecoverResult(
                        target_confirmed=True,
                        summary_confirmed=False,
                        prep_error=False,
                        ineligible=False,
                        declared_target="recovered-q1",
                        evidence="synthetic:recover:target-only",
                        post_summary=None,
                    ),
                ),
                unknown.environment,
            )

    result = session.step(unknown.state, TargetOnlyRecoverEnvironment())  # type: ignore[arg-type]

    assert result.stop_reason is None
    assert result.diagnostics[-1].code == "RECOVER-TARGET-UNCONFIRMED"
    assert result.state.evidence[-1].resolution_code == "RECOVER-TARGET-UNCONFIRMED"
    assert result.state.context.q_status == "UNKNOWN"
    assert result.state.context.current_summary is None
    assert result.state.context.known_target is None
    assert result.state.context.known_evidence == ()
    assert result.state.history.hypotheses == unknown.state.history.hypotheses
    assert set(result.state.history.status_by_hypothesis.values()) == {"CONSERVATIVE-UNKNOWN"}


def test_synthetic_target_only_prep_is_a_valid_unconfirmed_result() -> None:
    """The JSON-like synthetic boundary also admits independent confirmations."""

    binding, base, fixture = _runtime_parts()
    model = _gap_and_prep_model(binding, base, fixture)
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-prep-target-only", run_id="run-prep-target-only",
        initial_summary="q0", resources=ResourceState.rounds(2), retry_cap=2,
    )
    result = session.step(session.initial_state, _environment({
        "private-0": {
            "prep-q0": _prep_recover(
                target_confirmed=True, summary_confirmed=False, prep_error=False, ineligible=False,
                declared_target="prepared-q1", evidence="synthetic:prep:target-only", post_summary=None,
                next_state="private-2",
            ),
        },
    }))

    assert result.stop_reason is None
    assert result.diagnostics[-1].code == "PREP-SUMMARY-UNCONFIRMED"
    assert result.state.evidence[-1].resolution_code == "PREP-SUMMARY-UNCONFIRMED"
    assert result.state.context.q_status == "UNKNOWN"
    assert result.state.context.current_summary is None
    assert set(result.state.history.status_by_hypothesis.values()) == {"CONSERVATIVE-UNKNOWN"}


def test_cross_kind_stale_delivery_is_deduplicated_before_admission() -> None:
    """A prior TEST delivery cannot trigger the later PREP action."""

    binding, base, fixture = _runtime_parts()
    q0_test = _action(
        fixture, "test-router", action_id="test-q0", kind="TEST", enabled_summaries=["q0"],
    )
    q1_prep = _action(
        fixture, "test-router", action_id="prep-q1", kind="PREP", enabled_summaries=["q1"],
        declared_target="prepared-q2",
    )
    model = _model_with(base, fixture, [q0_test, q1_prep])
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-cross-kind-duplicate", run_id="run-cross-kind-duplicate",
        initial_summary="q0", resources=ResourceState.rounds(2), retry_cap=2,
    )
    first = session.step(session.initial_state, _environment({
        "private-0": {"test-q0": _normal("branch-alpha", "q1", "private-1")},
    }))
    assert first.stop_reason is None

    stale_delivery = first.environment.with_pending_delivery(first.state.evidence[-1].execution)
    discarded = session.step(first.state, stale_delivery)

    assert discarded.stop_reason is None
    assert discarded.diagnostics[-1].code == "DUPLICATE-EXECUTION-EVIDENCE"
    assert discarded.state is first.state
    assert discarded.state.resources == first.state.resources
    assert discarded.state.history == first.state.history
    assert discarded.state.evidence == first.state.evidence


def test_misrouted_post_dispatch_record_is_charged_and_retains_actual_successor() -> None:
    """A bad return for a newly issued request is not an inbound duplicate."""

    binding, base, fixture = _runtime_parts()
    q0_test = _action(
        fixture, "test-router", action_id="test-q0", kind="TEST", enabled_summaries=["q0"],
    )
    q1_prep = _action(
        fixture, "test-router", action_id="prep-q1", kind="PREP", enabled_summaries=["q1"],
        declared_target="prepared-q2",
    )
    model = _model_with(base, fixture, [q0_test, q1_prep])
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-misrouted-return", run_id="run-misrouted-return",
        initial_summary="q0", resources=ResourceState.rounds(2), retry_cap=2,
    )
    environment = _environment({
        "private-0": {"test-q0": _normal("branch-alpha", "q1", "private-1")},
        "private-1": {
            "prep-q1": _prep_recover(
                target_confirmed=False, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="prepared-q2", evidence="synthetic:prep:q2", post_summary="q2",
                next_state="private-2",
            ),
        },
        "private-2": {"prep-q1": _not_sent("private-2")},
    })
    first = session.step(session.initial_state, environment)
    assert first.stop_reason is None

    class MisroutedPostDispatchAdapter:
        actual_successor: SyntheticEnvironment | None = None

        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            actual = first.environment.execute(request)
            self.actual_successor = actual.successor
            return EnvironmentExecution(first.state.evidence[-1].execution, actual.successor)

    adapter = MisroutedPostDispatchAdapter()
    rejected = session.step(first.state, adapter)  # type: ignore[arg-type]

    assert rejected.stop_reason is None
    assert rejected.diagnostics[-1].code == "INVALID-EXECUTION-RECORD"
    assert rejected.state.attempts == first.state.attempts + 1
    assert rejected.state.resources.remaining == first.state.resources.remaining - 1
    assert rejected.state.context.q_status == "UNKNOWN"
    assert rejected.environment is adapter.actual_successor


def test_unknown_recover_admission_distinguishes_a4_and_a5_without_second_charge() -> None:
    binding, base, fixture = _runtime_parts()
    router_only = _model_with(base, fixture, [
        _action(fixture, "test-router", action_id="test-q0", kind="TEST", enabled_summaries=["q0"]),
    ])
    a4 = ReferenceSession(
        binding=binding, model=router_only, session_id="session-a4", run_id="run-a4",
        initial_summary="q0", resources=ResourceState.rounds(2), retry_cap=2,
    )
    first_a4 = a4.step(a4.initial_state, _environment({"private-0": {"test-q0": _unknown("private-1")}}))
    no_recover = a4.step(first_a4.state, first_a4.environment)
    assert no_recover.stop_reason == "Stop-Error"
    assert no_recover.diagnostics[-1].code == "ADMISSION-A4-NO-ELIGIBLE-RECOVER"
    assert no_recover.state.attempts == 1
    assert no_recover.state.resources.remaining == 1

    costly_recover = _router_recover_model(base, fixture, recover_cost=2)
    a5 = ReferenceSession(
        binding=binding, model=costly_recover, session_id="session-a5", run_id="run-a5",
        initial_summary="q0", resources=ResourceState.budget(2), retry_cap=2,
    )
    first_a5 = a5.step(a5.initial_state, _environment({"private-0": {"test-q0": _unknown("private-1")}}))
    unaffordable = a5.step(first_a5.state, first_a5.environment)
    assert unaffordable.stop_reason == "Stop-Budget"
    assert unaffordable.diagnostics[-1].code == "ADMISSION-A5-UNAFFORDABLE-RECOVER"
    assert unaffordable.state.attempts == 1
    assert unaffordable.state.resources.remaining == 1


def test_confirmed_not_sent_bypasses_recover_confirmation_while_unknown() -> None:
    binding, base, fixture = _runtime_parts()
    model = _router_recover_model(base, fixture)
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-unknown-not-sent", run_id="run-unknown-not-sent",
        initial_summary="q0", resources=ResourceState.rounds(3), retry_cap=3,
    )
    environment = _environment({
        "private-0": {"test-q0": _unknown("private-1")},
        "private-1": {"recover-q": _not_sent("private-2")},
    })

    unknown = session.step(session.initial_state, environment)
    result = session.step(unknown.state, unknown.environment)

    assert result.stop_reason is None
    assert result.diagnostics[-1].code == "CONFIRMED-NOT-SENT"
    assert result.state.evidence[-1].execution.uncertainty_identity is None
    assert result.state.context.q_status == "UNKNOWN"
    assert result.state.context.current_summary is None
    assert result.state.context.retry_count == unknown.state.context.retry_count + 1
    assert result.state.history == unknown.state.history
    assert result.state.frontiers == unknown.state.frontiers
    assert result.state.resources.remaining == unknown.state.resources.remaining - 1


def test_confirmed_not_sent_preserves_known_summary_for_test_and_prep_until_retry_cap() -> None:
    binding, base, fixture = _runtime_parts()
    test_model = _model_with(base, fixture, [
        _action(fixture, "test-router", action_id="test-q0", kind="TEST", enabled_summaries=["q0"]),
    ])
    test_session = ReferenceSession(
        binding=binding, model=test_model, session_id="session-test-not-sent", run_id="run-test-not-sent",
        initial_summary="q0", resources=ResourceState.rounds(3), retry_cap=2,
    )
    test_first = test_session.step(test_session.initial_state, _environment({
        "private-0": {"test-q0": _not_sent("private-1")},
        "private-1": {"test-q0": _normal("branch-alpha", "branch-alpha", "private-2")},
    }))
    assert test_first.stop_reason is None
    assert test_first.state.context.q_status == "KNOWN"
    assert test_first.state.context.current_summary == "q0"
    assert test_first.state.history == test_session.initial_state.history
    test_second = test_session.step(test_first.state, test_first.environment)
    assert test_second.state.evidence[-1].snapshot.q_used_at_select == "q0"

    prep_model = _gap_and_prep_model(binding, base, fixture)
    prep_session = ReferenceSession(
        binding=binding, model=prep_model, session_id="session-prep-not-sent", run_id="run-prep-not-sent",
        initial_summary="q0", resources=ResourceState.rounds(2), retry_cap=2,
    )
    prep_first = prep_session.step(prep_session.initial_state, _environment({
        "private-0": {"prep-q0": _not_sent("private-1")},
        "private-1": {
            "prep-q0": _prep_recover(
                target_confirmed=False, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="prepared-q1", evidence="synthetic:prep:after-not-sent", post_summary="q1",
                next_state="private-2",
            ),
        },
    }))
    assert prep_first.stop_reason is None
    assert prep_first.state.context.q_status == "KNOWN"
    assert prep_first.state.context.current_summary == "q0"
    assert prep_first.state.history == prep_session.initial_state.history
    prep_second = prep_session.step(prep_first.state, prep_first.environment)
    assert prep_second.state.evidence[-1].snapshot.action_id == "prep-q0"
    assert prep_second.state.evidence[-1].snapshot.q_used_at_select == "q0"


def test_s7_retry_cap_and_recovery_boundary_are_closed_at_the_public_adapter() -> None:
    binding, base, fixture = _runtime_parts()
    model = _router_recover_model(base, fixture)
    cap_session = ReferenceSession(
        binding=binding, model=model, session_id="session-cap", run_id="run-cap",
        initial_summary="q0", resources=ResourceState.rounds(2), retry_cap=1,
    )
    capped = cap_session.step(cap_session.initial_state, _environment({"private-0": {"test-q0": _unknown("private-1")}}))
    assert capped.stop_reason == "Stop-Error"
    assert capped.state.context.retry_count == 1
    assert capped.state.resources.remaining == 1
    assert cap_session.step(capped.state, capped.environment).state.attempts == 1

    # The typed boundary cannot let a mismatched Recover declaration into S8
    # or S9.  It is charged once and resolved by the canonical S7 error path.
    class WrongTargetEnvironment:
        def __init__(self, successor: SyntheticEnvironment) -> None:
            self.successor = successor

        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            return EnvironmentExecution(
                VisibleExecutionRecord(
                    execution_attempt_id=request.execution_attempt_id,
                    action_id=request.action_id,
                    effect_class="NONE",
                    observable=None,
                    summary_confirmed=True,
                    post_summary="q1",
                    measurement_tick=None,
                    uncertainty_identity=None,
                    evidence_ref="synthetic:wrong-recover-target",
                    prep_recover=PrepRecoverResult(
                        target_confirmed=True,
                        summary_confirmed=True,
                        prep_error=False,
                        ineligible=False,
                        declared_target="forged-target",
                        evidence="synthetic:forged-target",
                        post_summary="q1",
                    ),
                ),
                self.successor,
            )

    initial_unknown = ReferenceSession(
        binding=binding, model=model, session_id="session-boundary", run_id="run-boundary",
        initial_summary="q0", resources=ResourceState.rounds(3), retry_cap=2,
    )
    unknown = initial_unknown.step(
        initial_unknown.initial_state,
        _environment({"private-0": {"test-q0": _unknown("private-1")}}),
    )
    bad = initial_unknown.step(
        unknown.state,
        WrongTargetEnvironment(unknown.environment),  # type: ignore[arg-type]
    )
    assert bad.stop_reason == "Stop-Error"
    assert bad.diagnostics[-1].code == "RECOVERY-TARGET-MISMATCH"
    assert bad.state.context.q_status == "UNKNOWN"
    assert bad.state.context.current_summary is None
    assert bad.state.context.known_target is None

    tampered = replace(
        unknown.state,
        evidence=(replace(unknown.state.evidence[0], resolution_code="COMMIT"),),
    )
    rejected = initial_unknown.step(tampered, unknown.environment)
    assert rejected.stop_reason == "Stop-Error"
    assert rejected.diagnostics[0].code == "EVIDENCE-UNKNOWN-MISMATCH"


def test_action_kind_cannot_smuggle_or_omit_recovery_contract_fields() -> None:
    _binding, base, fixture = _runtime_parts()
    test_with_null_recovery = _action(
        fixture, "test-router", action_id="test-q0", kind="TEST", enabled_summaries=["q0"],
    )
    test_with_null_recovery["declaredTarget"] = None
    with pytest.raises(ValueError, match="TEST action cannot declare"):
        _model_with(base, fixture, [test_with_null_recovery])

    missing_prep_target = _action(
        fixture, "test-router", action_id="prep-q0", kind="PREP", enabled_summaries=["q0"],
        declared_target="prepared-q1",
    )
    del missing_prep_target["declaredTarget"]
    with pytest.raises(ValueError, match="requires a declared target"):
        _model_with(base, fixture, [missing_prep_target])
