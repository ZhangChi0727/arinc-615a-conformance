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
from cltav_runtime.kernel import ContractSnapshot, FrontierEntry, Interval, ModelContext, initial_entry, propagate_transition
from cltav_runtime.model import FiniteSessionModel
from cltav_runtime.session import ReferenceSession, ResourceState
from cltav_runtime.synthetic import (
    EnvironmentExecution,
    ExecutionRequest,
    PrepRecoverResult,
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


def _seed_with_conservative_h2(
    model: FiniteSessionModel,
    *,
    root_id: str,
    retain_known_h2_path: bool = False,
) -> dict[str, tuple[FrontierEntry, ...]]:
    """Build a legal S0 seed whose optional status map is deliberately empty.

    `HistoryHandle.initial` permits the member-status map to be absent.  The
    explicit frontier entry remains a public conservative witness, so tests
    using this helper exercise the path-level status contract rather than a
    synthetic rewrite of a committed history.
    """

    seed = {
        hypothesis: (frontier,)
        for hypothesis, frontier in model.initial_frontiers.items()
    }
    h2 = model.initial_frontiers["h2"]
    conservative = initial_entry(
        model.context,
        hypothesis_id="h2",
        control_state_id="q0",
        clocks=h2.clocks,
        typed_store=h2.typed_store,
        root_id=root_id,
        status="CONSERVATIVE-UNKNOWN",
    )
    seed["h2"] = (h2, conservative) if retain_known_h2_path else (conservative,)
    return seed


def _model_with_declaration(model_data: dict[str, object]) -> FiniteSessionModel:
    """Build a detached verified context for a deliberately changed model declaration."""

    snapshot = ContractSnapshot.from_git_object(
        repository=ROOT, contract_commit=_head_commit(), contract_path=DEVELOPMENT_PATH,
    )
    declaration = model_data["model"]
    assert isinstance(declaration, dict)
    domains = declaration["typedDomains"]
    assert isinstance(domains, dict)
    context = ModelContext.build(
        snapshot=snapshot,
        model={
            "stateIds": set(declaration["stateIds"]),
            "clockIds": set(declaration["clockIds"]),
            "typedDomains": {name: set(domain) for name, domain in domains.items()},
        },
        projection_clock="x",
    )
    return FiniteSessionModel.from_mapping(context=context, value=model_data)


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


@pytest.mark.parametrize("target_confirmed", [False, True])
def test_confirmed_summary_only_prep_propagates_declared_model_successor(
    target_confirmed: bool,
) -> None:
    """S9 commits q while IF-HIST-UPDATE advances every retained q0 path."""

    binding, base, fixture = _runtime_parts()
    prep = _action(
        fixture, "test-router", action_id="prep-q0", kind="PREP",
        enabled_summaries=["initial-summary"], declared_target="prepared-target",
    )
    prep_transition = prep["transition"]
    assert isinstance(prep_transition, dict)
    prep_transition["target"] = "q1"
    prep_transition["simultaneousUpdates"] = [{"tag": "STATE-ASSIGN", "state": "q1"}]
    follow_up = _action(
        fixture, "test-router", action_id="test-q1", kind="TEST",
        enabled_summaries=["confirmed-successor-summary"],
    )
    follow_up_transition = follow_up["transition"]
    assert isinstance(follow_up_transition, dict)
    follow_up_transition["source"] = "q1"
    follow_up_transition["target"] = "q1"
    follow_up_transition["simultaneousUpdates"] = [{"tag": "STATE-ASSIGN", "state": "q1"}]
    model = _model_with(base, fixture, [prep, follow_up])
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-prep-summary", run_id="run-prep-summary",
        initial_summary="initial-summary", resources=ResourceState.rounds(3), retry_cap=2,
    )
    environment = _environment({
        "private-0": {
            "prep-q0": _prep_recover(
                target_confirmed=target_confirmed, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="prepared-target", evidence="synthetic:prep:q1",
                post_summary="confirmed-successor-summary",
                next_state="private-1",
            ),
        },
        "private-1": {
            "test-q1": _normal("branch-alpha", "confirmed-successor-summary", "private-2"),
        },
    })

    first = session.step(session.initial_state, environment)
    assert first.stop_reason is None
    assert first.state.evidence[0].snapshot.action_id == "prep-q0"
    assert first.state.evidence[0].resolution_code == "COMMIT"
    assert first.state.context.q_status == "KNOWN"
    assert first.state.context.current_summary == "confirmed-successor-summary"
    assert first.state.context.known_target is None
    assert first.state.history.hypotheses == session.initial_state.history.hypotheses
    assert first.state.history.version == 1
    assert set(first.state.history.status_by_hypothesis.values()) == {"KNOWN"}
    assert {
        path.control_state_id
        for paths in first.state.frontiers.values()
        for path in paths
    } == {"q1"}
    assert first.state.history.compatible_state_by_hypothesis != session.initial_state.history.compatible_state_by_hypothesis
    assert all(
        len(path.history_provenance) == len(session.initial_state.frontiers[hypothesis][0].history_provenance) + 1
        for hypothesis, paths in first.state.frontiers.items()
        for path in paths
    )

    # The distinct summary labels cannot be used to guess q1: continuation is
    # possible only because the executed finite q0->q1 transition was retained.
    second = session.step(first.state, first.environment)
    assert second.stop_reason is None
    assert second.state.attempts == 2
    assert second.state.evidence[-1].snapshot.action_id == "test-q1"
    assert second.state.evidence[-1].snapshot.q_used_at_select == "confirmed-successor-summary"


def test_summary_only_prep_propagates_typed_store_and_clock_reset_for_next_guard() -> None:
    """A confirmed summary-only successor carries the full finite model result."""

    binding, _base, fixture = _runtime_parts()
    model_data = copy.deepcopy(fixture["algorithmModel"])
    assert isinstance(model_data, dict)
    declaration = model_data["model"]
    hypotheses = model_data["hypotheses"]
    assert isinstance(declaration, dict) and isinstance(hypotheses, list)
    declaration["typedDomains"] = {"mode": ["normal", "recovery"]}
    exact_five = {
        "lower": {"numerator": 5, "positiveDenominator": 1},
        "upper": {"numerator": 5, "positiveDenominator": 1},
        "lowerClosed": True,
        "upperClosed": True,
    }
    for item in hypotheses:
        assert isinstance(item, dict)
        item["clockConstraint"] = {"x": copy.deepcopy(exact_five)}

    prep = _action(
        fixture, "test-router", action_id="prep-reset", kind="PREP",
        enabled_summaries=["initial-summary"], declared_target="prepared-target",
    )
    prep_transition = prep["transition"]
    assert isinstance(prep_transition, dict)
    prep_transition.update({
        "source": "q0",
        "target": "q1",
        "guardAst": {"tag": "STATE-EQUALS", "state": "q0"},
        "simultaneousUpdates": [
            {"tag": "STATE-ASSIGN", "state": "q1"},
            {"tag": "CLOCK-RESET-TO-ZERO", "clock": "x"},
            {"tag": "TYPED-FIELD-ASSIGN", "field": "mode", "value": "recovery"},
        ],
    })
    follow_up = _action(
        fixture, "test-router", action_id="test-after-reset", kind="TEST",
        enabled_summaries=["after-prep"],
    )
    follow_transition = follow_up["transition"]
    assert isinstance(follow_transition, dict)
    follow_transition.update({
        "source": "q1",
        "target": "q1",
        "guardAst": {
            "tag": "AND",
            "operands": [
                {"tag": "STATE-EQUALS", "state": "q1"},
                {"tag": "TYPED-FIELD-EQUALS", "field": "mode", "value": "recovery"},
                {
                    "tag": "RATIONAL-INTERVAL-CONTAINS",
                    "clock": "x",
                    "interval": {
                        "lower": {"numerator": 0, "positiveDenominator": 1},
                        "upper": {"numerator": 0, "positiveDenominator": 1},
                        "lowerClosed": True,
                        "upperClosed": True,
                    },
                },
            ],
        },
        "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q1"}],
    })
    model_data["actions"] = [prep, follow_up]
    limits = model_data["limits"]
    assert isinstance(limits, dict)
    limits["actions"] = 2
    model = _model_with_declaration(model_data)
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-prep-reset", run_id="run-prep-reset",
        initial_summary="initial-summary", resources=ResourceState.rounds(2), retry_cap=2,
    )
    environment = _environment({
        "private-0": {
            "prep-reset": _prep_recover(
                target_confirmed=True, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="prepared-target", evidence="synthetic:prep:reset",
                post_summary="after-prep", next_state="private-1",
            ),
        },
        "private-1": {
            "test-after-reset": _normal("branch-alpha", "after-test", "private-2"),
        },
    })

    first = session.step(session.initial_state, environment)
    assert first.stop_reason is None
    assert {
        (path.control_state_id, path.clocks["x"], path.typed_store["mode"])
        for paths in first.state.frontiers.values()
        for path in paths
    } == {("q1", Interval(Fraction(0), Fraction(0), True, True), "recovery")}

    second = session.step(first.state, first.environment)
    assert second.stop_reason is None
    assert second.state.evidence[-1].snapshot.action_id == "test-after-reset"


def test_summary_only_prep_retains_every_declared_seed_path_without_observation_filtering() -> None:
    """No ``I_z`` class may discard a concurrent path merely because it is unobserved."""

    binding, base, fixture = _runtime_parts()
    prep = _action(
        fixture, "test-router", action_id="prep-all-paths", kind="PREP",
        enabled_summaries=["q0"], declared_target="prepared-target",
    )
    transition = prep["transition"]
    assert isinstance(transition, dict)
    transition["target"] = "q1"
    transition["simultaneousUpdates"] = [{"tag": "STATE-ASSIGN", "state": "q1"}]
    model = _model_with(base, fixture, [prep])
    original = model.initial_frontiers["h0"]
    alternate = initial_entry(
        model.context,
        hypothesis_id="h0",
        control_state_id="q0",
        clocks=original.clocks,
        typed_store=original.typed_store,
        root_id="root:h0:summary-only-alternate",
    )
    seed = {hypothesis: (frontier,) for hypothesis, frontier in model.initial_frontiers.items()}
    seed["h0"] = (original, alternate)
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-prep-all-paths", run_id="run-prep-all-paths",
        initial_summary="q0", resources=ResourceState.rounds(1), initial_path_bundles=seed,
    )
    result = session.step(session.initial_state, _environment({
        "private-0": {
            "prep-all-paths": _prep_recover(
                target_confirmed=False, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="prepared-target", evidence="synthetic:prep:all-paths",
                post_summary="after-prep", next_state="private-1",
            ),
        },
    }))

    assert result.stop_reason is None
    assert result.state.history.hypotheses == frozenset(model.initial_frontiers)
    assert len(result.state.frontiers["h0"]) == 2
    assert {
        path.control_state_id
        for paths in result.state.frontiers.values()
        for path in paths
    } == {"q1"}


def test_summary_only_prep_accepts_a_legal_finite_self_loop() -> None:
    """The whole-history rule advances provenance even when state remains q0."""

    binding, base, fixture = _runtime_parts()
    model = _gap_and_prep_model(binding, base, fixture)
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-prep-self-loop", run_id="run-prep-self-loop",
        initial_summary="q0", resources=ResourceState.rounds(1), retry_cap=2,
    )
    result = session.step(session.initial_state, _environment({
        "private-0": {
            "prep-q0": _prep_recover(
                target_confirmed=False, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="prepared-q1", evidence="synthetic:prep:self-loop",
                post_summary="q1", next_state="private-1",
            ),
        },
    }))

    assert result.stop_reason is None
    assert result.state.history.hypotheses == session.initial_state.history.hypotheses
    assert set(result.state.history.status_by_hypothesis.values()) == {"KNOWN"}
    assert {
        path.control_state_id
        for paths in result.state.frontiers.values()
        for path in paths
    } == {"q0"}
    assert all(
        len(path.history_provenance) == len(session.initial_state.frontiers[hypothesis][0].history_provenance) + 1
        for hypothesis, paths in result.state.frontiers.items()
        for path in paths
    )


def test_summary_only_prep_never_revives_hypotheses_excluded_by_a_prior_observation() -> None:
    """A later summary confirmation preserves the current H, not the S0 seed."""

    binding, base, fixture = _runtime_parts()
    test_q0 = _action(
        fixture, "test-router", action_id="test-filter", kind="TEST", enabled_summaries=["q0"],
    )
    prep = _action(
        fixture, "test-router", action_id="prep-after-filter", kind="PREP",
        enabled_summaries=["branch-alpha"], declared_target="prepared-target",
    )
    transition = prep["transition"]
    assert isinstance(transition, dict)
    transition["target"] = "q1"
    transition["simultaneousUpdates"] = [{"tag": "STATE-ASSIGN", "state": "q1"}]
    model = _model_with(base, fixture, [test_q0, prep])
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-prep-no-revival", run_id="run-prep-no-revival",
        initial_summary="q0", resources=ResourceState.rounds(2), retry_cap=2,
    )
    environment = _environment({
        "private-0": {"test-filter": _normal("branch-alpha", "branch-alpha", "private-1")},
        "private-1": {
            "prep-after-filter": _prep_recover(
                target_confirmed=True, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="prepared-target", evidence="synthetic:prep:no-revival",
                post_summary="after-prep", next_state="private-2",
            ),
        },
    })
    filtered = session.step(session.initial_state, environment)
    assert filtered.state.history.hypotheses == {"h0", "h1"}

    result = session.step(filtered.state, filtered.environment)
    assert result.stop_reason is None
    assert result.state.history.hypotheses == {"h0", "h1"}
    assert set(result.state.frontiers) == {"h0", "h1"}
    assert all(path.control_state_id == "q1" for paths in result.state.frontiers.values() for path in paths)


def test_summary_only_prep_keeps_unresolved_members_as_named_conservative_paths() -> None:
    """A source mismatch is not a license to erase the current hypothesis."""

    binding, base, fixture = _runtime_parts()
    prep = _action(
        fixture, "test-router", action_id="prep-q1-only", kind="PREP",
        enabled_summaries=["q0"], declared_target="prepared-target",
    )
    transition = prep["transition"]
    assert isinstance(transition, dict)
    transition.update({
        "source": "q1",
        "target": "q1",
        "guardAst": {"tag": "STATE-EQUALS", "state": "q1"},
        "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q1"}],
    })
    model = _model_with(base, fixture, [prep])
    h0 = model.initial_frontiers["h0"]
    q1_h0 = initial_entry(
        model.context,
        hypothesis_id="h0",
        control_state_id="q1",
        clocks=h0.clocks,
        typed_store=h0.typed_store,
        root_id="root:h0:q1-summary-only",
    )
    seed = {hypothesis: (frontier,) for hypothesis, frontier in model.initial_frontiers.items()}
    seed["h0"] = (q1_h0,)
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-prep-conservative", run_id="run-prep-conservative",
        initial_summary="q0", resources=ResourceState.rounds(1), initial_path_bundles=seed,
    )
    result = session.step(session.initial_state, _environment({
        "private-0": {
            "prep-q1-only": _prep_recover(
                target_confirmed=False, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="prepared-target", evidence="synthetic:prep:conservative",
                post_summary="after-prep", next_state="private-1",
            ),
        },
    }))

    assert result.stop_reason is None
    assert result.state.history.hypotheses == frozenset(model.initial_frontiers)
    assert result.state.history.status_by_hypothesis["h0"] == "KNOWN"
    assert {
        hypothesis
        for hypothesis, status in result.state.history.status_by_hypothesis.items()
        if status == "CONSERVATIVE-UNKNOWN"
    } == {"h1", "h2", "h3"}
    assert any(item.code == "SUMMARY-ONLY-CONSERVATIVE-PATH" for item in result.diagnostics)


def test_summary_only_recover_advances_existing_conservative_paths_without_promoting_them() -> None:
    """S8 may restore session KNOWN without leaving a retained model path stale."""

    binding, base, fixture = _runtime_parts()
    test_q0 = _action(
        fixture, "test-router", action_id="test-q0", kind="TEST", enabled_summaries=["q0"],
    )
    recover = _action(
        fixture, "test-router", action_id="recover-q0-q1", kind="RECOVER",
        enabled_summaries=["q0"], declared_target="recovered-target", recover_when_unknown=True,
    )
    transition = recover["transition"]
    assert isinstance(transition, dict)
    transition.update({
        "source": "q0",
        "target": "q1",
        "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q1"}],
    })
    model = _model_with(base, fixture, [test_q0, recover])
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-recover-conservative", run_id="run-recover-conservative",
        initial_summary="q0", resources=ResourceState.rounds(2), retry_cap=2,
    )
    environment = _environment({
        "private-0": {"test-q0": _unknown("private-1")},
        "private-1": {
            "recover-q0-q1": _prep_recover(
                target_confirmed=True, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="recovered-target", evidence="synthetic:recover:advance-conservative",
                post_summary="q1", next_state="private-2",
            ),
        },
    })
    unknown = session.step(session.initial_state, environment)
    assert set(unknown.state.history.status_by_hypothesis.values()) == {"CONSERVATIVE-UNKNOWN"}
    assert {
        path.control_state_id
        for paths in unknown.state.frontiers.values()
        for path in paths
    } == {"q0"}

    recovered = session.step(unknown.state, unknown.environment)

    assert recovered.stop_reason is None
    assert recovered.state.context.q_status == "KNOWN"
    assert recovered.state.context.current_summary == "q1"
    assert set(recovered.state.history.status_by_hypothesis.values()) == {"CONSERVATIVE-UNKNOWN"}
    assert {
        path.control_state_id
        for paths in recovered.state.frontiers.values()
        for path in paths
    } == {"q1"}
    assert all(
        len(path.history_provenance) == len(unknown.state.frontiers[hypothesis][0].history_provenance) + 1
        for hypothesis, paths in recovered.state.frontiers.items()
        for path in paths
    )


def test_summary_only_prep_preserves_a_conservative_s0_frontier_without_a_status_map_entry() -> None:
    """An optional S0 status map cannot silently promote a C-U seed path.

    The initial HistoryHandle deliberately has no member-status entry.  The
    frontier entry itself is still a public conservative witness, so the
    summary-only q0→q1 transition must retain both its status and membership
    when the following q1 TEST emits a normal class.
    """

    binding, base, fixture = _runtime_parts()
    prep = _action(
        fixture, "test-router", action_id="prep-q0-q1", kind="PREP",
        enabled_summaries=["before"], declared_target="prepared-target",
    )
    prep_transition = prep["transition"]
    assert isinstance(prep_transition, dict)
    prep_transition.update({
        "target": "q1",
        "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q1"}],
    })
    follow_up = _action(
        fixture, "test-router", action_id="test-q1", kind="TEST",
        enabled_summaries=["after"],
    )
    follow_up_transition = follow_up["transition"]
    assert isinstance(follow_up_transition, dict)
    follow_up_transition.update({
        "source": "q1",
        "target": "q1",
        "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q1"}],
    })
    model = _model_with(base, fixture, [prep, follow_up])
    seed = _seed_with_conservative_h2(
        model, root_id="root:h2:conservative-s0-summary",
    )
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-s0-conservative-summary",
        run_id="run-s0-conservative-summary", initial_summary="before",
        resources=ResourceState.rounds(2), retry_cap=2, initial_path_bundles=seed,
    )
    assert session.initial_state.history.status_by_hypothesis == {}
    assert session.initial_state.frontiers["h2"][0].status == "CONSERVATIVE-UNKNOWN"
    environment = _environment({
        "private-0": {
            "prep-q0-q1": _prep_recover(
                target_confirmed=True, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="prepared-target", evidence="synthetic:prep:s0-conservative",
                post_summary="after", next_state="private-1",
            ),
        },
        "private-1": {"test-q1": _normal("branch-alpha", "after-test", "private-2")},
    })

    after_prep = session.step(session.initial_state, environment)
    assert after_prep.stop_reason is None
    assert after_prep.state.history.status_by_hypothesis["h2"] == "CONSERVATIVE-UNKNOWN"
    assert {
        path.control_state_id for path in after_prep.state.frontiers["h2"]
    } == {"q1"}
    assert {
        path.status for path in after_prep.state.frontiers["h2"]
    } == {"CONSERVATIVE-UNKNOWN"}
    assert all(
        status == "KNOWN"
        for hypothesis, status in after_prep.state.history.status_by_hypothesis.items()
        if hypothesis != "h2"
    )

    after_test = session.step(after_prep.state, after_prep.environment)
    assert after_test.stop_reason is None
    assert "h2" in after_test.state.history.hypotheses
    assert after_test.state.history.status_by_hypothesis["h2"] == "CONSERVATIVE-UNKNOWN"


def test_summary_only_prep_aggregates_mixed_known_and_conservative_s0_paths() -> None:
    """A known sibling cannot overwrite a retained conservative source path."""

    binding, base, fixture = _runtime_parts()
    prep = _action(
        fixture, "test-router", action_id="prep-q0-q1", kind="PREP",
        enabled_summaries=["before"], declared_target="prepared-target",
    )
    prep_transition = prep["transition"]
    assert isinstance(prep_transition, dict)
    prep_transition.update({
        "target": "q1",
        "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q1"}],
    })
    follow_up = _action(
        fixture, "test-router", action_id="test-q1", kind="TEST",
        enabled_summaries=["after"],
    )
    follow_up_transition = follow_up["transition"]
    assert isinstance(follow_up_transition, dict)
    follow_up_transition.update({
        "source": "q1",
        "target": "q1",
        "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q1"}],
    })
    model = _model_with(base, fixture, [prep, follow_up])
    seed = _seed_with_conservative_h2(
        model, root_id="root:h2:mixed-s0-summary", retain_known_h2_path=True,
    )
    source_roots = {path.history_provenance[0] for path in seed["h2"]}
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-mixed-s0-summary",
        run_id="run-mixed-s0-summary", initial_summary="before",
        resources=ResourceState.rounds(2), retry_cap=2, initial_path_bundles=seed,
    )
    environment = _environment({
        "private-0": {
            "prep-q0-q1": _prep_recover(
                target_confirmed=False, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="prepared-target", evidence="synthetic:prep:mixed-s0",
                post_summary="after", next_state="private-1",
            ),
        },
        "private-1": {"test-q1": _normal("branch-alpha", "after-test", "private-2")},
    })

    after_prep = session.step(session.initial_state, environment)
    assert after_prep.stop_reason is None
    assert after_prep.state.history.status_by_hypothesis["h2"] == "CONSERVATIVE-UNKNOWN"
    assert len(after_prep.state.frontiers["h2"]) == 2
    assert {path.control_state_id for path in after_prep.state.frontiers["h2"]} == {"q1"}
    assert {path.status for path in after_prep.state.frontiers["h2"]} == {
        "KNOWN", "CONSERVATIVE-UNKNOWN",
    }
    assert {path.history_provenance[0] for path in after_prep.state.frontiers["h2"]} == source_roots
    assert all(len(path.history_provenance) == 2 for path in after_prep.state.frontiers["h2"])

    # branch-alpha remains allowed to shrink ordinary known candidates, but
    # cannot use the C-U sibling to erase h2 as a whole.
    after_test = session.step(after_prep.state, after_prep.environment)
    assert after_test.stop_reason is None
    assert "h2" in after_test.state.history.hypotheses
    assert after_test.state.history.status_by_hypothesis["h2"] == "CONSERVATIVE-UNKNOWN"
    assert len(after_test.state.frontiers["h2"]) == 2
    assert {path.history_provenance[0] for path in after_test.state.frontiers["h2"]} == source_roots


def test_initial_conservative_s0_frontier_is_not_excluded_by_a_normal_observation() -> None:
    """The normal predictor consumes path-level C-U even before an S9 commit."""

    binding, base, fixture = _runtime_parts()
    test = _action(
        fixture, "test-router", action_id="test-q0", kind="TEST", enabled_summaries=["q0"],
    )
    model = _model_with(base, fixture, [test])
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-direct-s0-conservative",
        run_id="run-direct-s0-conservative", initial_summary="q0",
        resources=ResourceState.rounds(1), retry_cap=2,
        initial_path_bundles=_seed_with_conservative_h2(
            model, root_id="root:h2:direct-s0-conservative",
        ),
    )
    assert session.initial_state.history.status_by_hypothesis == {}

    result = session.step(session.initial_state, _environment({
        "private-0": {"test-q0": _normal("branch-alpha", "after-test", "private-1")},
    }))

    assert result.stop_reason is None
    assert "h2" in result.state.history.hypotheses
    assert result.state.history.status_by_hypothesis["h2"] == "CONSERVATIVE-UNKNOWN"
    assert all(
        status == "KNOWN"
        for hypothesis, status in result.state.history.status_by_hypothesis.items()
        if hypothesis != "h2"
    )


@pytest.mark.parametrize("condition", ["path-limit", "unsupported-guard"])
def test_summary_only_model_marks_bounded_or_unsupported_propagation_conservative(
    condition: str,
) -> None:
    """A completed summary never upgrades a member whose finite update is unresolved."""

    _binding, base, fixture = _runtime_parts()
    prep = _action(
        fixture, "test-router", action_id="prep-q0-q1", kind="PREP",
        enabled_summaries=["before"], declared_target="prepared-target",
    )
    transition = prep["transition"]
    assert isinstance(transition, dict)
    transition.update({
        "target": "q1",
        "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q1"}],
    })
    if condition == "unsupported-guard":
        transition["guardAst"] = {"tag": "UNSUPPORTED-GUARD"}

    model_data = copy.deepcopy(fixture["algorithmModel"])
    assert isinstance(model_data, dict)
    model_data["actions"] = [prep]
    limits = model_data["limits"]
    assert isinstance(limits, dict)
    limits["actions"] = 1
    if condition == "path-limit":
        limits["pathLength"] = 1
    model = FiniteSessionModel.from_mapping(context=base.context, value=model_data)

    seed = {hypothesis: (frontier,) for hypothesis, frontier in model.initial_frontiers.items()}
    if condition == "path-limit":
        # Build a source path with a real, verified one-step provenance chain
        # using a larger temporary calculation bound.  The model under test
        # then correctly treats that same path as bound-limited.
        advanced = propagate_transition(
            model.initial_frontiers["h2"],
            model.actions["prep-q0-q1"].transition_for_kernel(),
            state_ids=set(model.context.state_ids),
            clock_ids=set(model.context.clock_ids),
            typed_domains={key: set(domain) for key, domain in model.context.typed_domains.items()},
            context=model.context,
            path_limit=2,
            frontier_limit=model.frontier_limit,
        )
        assert advanced.kind == "FEASIBLE"
        seed["h2"] = (advanced.entries[0],)

    propagated = model.summary_only_successors(
        hypotheses=frozenset(seed), frontiers=seed, status_by_hypothesis={},
        action_id="prep-q0-q1",
    )

    assert "h2" in propagated.conservative_hypotheses
    assert propagated.successors["h2"]
    assert any(item.code.startswith("SUMMARY-ONLY-") for item in propagated.diagnostics)


def test_fresh_checkpoint_replays_and_executes_a_second_summary_only_prep_without_cache_writes() -> None:
    """Portable summary-only evidence must use the detached replay model end-to-end."""

    source_binding, source_base, fixture = _runtime_parts()
    first_prep = _action(
        fixture, "test-router", action_id="prep-q0-q1", kind="PREP",
        enabled_summaries=["q0"], declared_target="target-q1",
    )
    first_transition = first_prep["transition"]
    assert isinstance(first_transition, dict)
    first_transition.update({
        "source": "q0",
        "target": "q1",
        "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q1"}],
    })
    second_prep = _action(
        fixture, "test-router", action_id="prep-q1-q0", kind="PREP",
        enabled_summaries=["q1"], declared_target="target-q0",
    )
    second_transition = second_prep["transition"]
    assert isinstance(second_transition, dict)
    second_transition.update({
        "source": "q1",
        "target": "q0",
        "guardAst": {"tag": "STATE-EQUALS", "state": "q1"},
        "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q0"}],
    })
    source_model = _model_with(source_base, fixture, [first_prep, second_prep])
    source = ReferenceSession(
        binding=source_binding, model=source_model, session_id="session-portable-summary", run_id="run-portable-summary",
        initial_summary="q0", resources=ResourceState.rounds(2), retry_cap=2,
    )
    environment = _environment({
        "private-0": {
            "prep-q0-q1": _prep_recover(
                target_confirmed=False, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="target-q1", evidence="synthetic:prep:portable-one",
                post_summary="q1", next_state="private-1",
            ),
        },
        "private-1": {
            "prep-q1-q0": _prep_recover(
                target_confirmed=True, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="target-q0", evidence="synthetic:prep:portable-two",
                post_summary="q0", next_state="private-2",
            ),
        },
    })
    first = source.step(source.initial_state, environment)
    assert first.stop_reason is None
    expected = source.step(first.state, first.environment)
    assert expected.stop_reason is None

    target_binding, target_base, _target_fixture = _runtime_parts()
    target_model = _model_with(target_base, fixture, [first_prep, second_prep])
    target = ReferenceSession(
        binding=target_binding, model=target_model, session_id="session-portable-summary", run_id="run-portable-summary",
        initial_summary="q0", resources=ResourceState.rounds(2), retry_cap=2,
    )
    records_before = dict(target_model.context.provenance_store.records())
    assert target._state_error(first.state) is None

    resumed = target.step(first.state, first.environment)

    assert resumed.stop_reason is None
    assert resumed.state == expected.state
    assert resumed.state.evidence[-1].snapshot.action_id == "prep-q1-q0"
    assert {
        path.control_state_id
        for paths in resumed.state.frontiers.values()
        for path in paths
    } == {"q0"}
    assert dict(target_model.context.provenance_store.records()) == records_before
    assert target._state_error(resumed.state) is None


def test_fresh_checkpoint_replays_a_conservative_s0_summary_path_without_cache_writes() -> None:
    """Fresh replay must preserve the same C-U aggregation as the live path."""

    source_binding, source_base, fixture = _runtime_parts()
    prep = _action(
        fixture, "test-router", action_id="prep-q0-q1", kind="PREP",
        enabled_summaries=["before"], declared_target="prepared-target",
    )
    prep_transition = prep["transition"]
    assert isinstance(prep_transition, dict)
    prep_transition.update({
        "target": "q1",
        "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q1"}],
    })
    follow_up = _action(
        fixture, "test-router", action_id="test-q1", kind="TEST",
        enabled_summaries=["after"],
    )
    follow_up_transition = follow_up["transition"]
    assert isinstance(follow_up_transition, dict)
    follow_up_transition.update({
        "source": "q1",
        "target": "q1",
        "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q1"}],
    })
    source_model = _model_with(source_base, fixture, [prep, follow_up])
    source = ReferenceSession(
        binding=source_binding, model=source_model,
        session_id="session-portable-s0-conservative", run_id="run-portable-s0-conservative",
        initial_summary="before", resources=ResourceState.rounds(2), retry_cap=2,
        initial_path_bundles=_seed_with_conservative_h2(
            source_model, root_id="root:h2:portable-s0-conservative",
        ),
    )
    environment = _environment({
        "private-0": {
            "prep-q0-q1": _prep_recover(
                target_confirmed=False, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="prepared-target", evidence="synthetic:prep:portable-s0-cu",
                post_summary="after", next_state="private-1",
            ),
        },
        "private-1": {"test-q1": _normal("branch-alpha", "after-test", "private-2")},
    })
    first = source.step(source.initial_state, environment)
    assert first.stop_reason is None
    assert first.state.history.status_by_hypothesis["h2"] == "CONSERVATIVE-UNKNOWN"
    expected = source.step(first.state, first.environment)
    assert expected.stop_reason is None

    target_binding, target_base, _target_fixture = _runtime_parts()
    target_model = _model_with(target_base, fixture, [prep, follow_up])
    target = ReferenceSession(
        binding=target_binding, model=target_model,
        session_id="session-portable-s0-conservative", run_id="run-portable-s0-conservative",
        initial_summary="before", resources=ResourceState.rounds(2), retry_cap=2,
        initial_path_bundles=_seed_with_conservative_h2(
            target_model, root_id="root:h2:portable-s0-conservative",
        ),
    )
    records_before = dict(target_model.context.provenance_store.records())
    assert target._state_error(first.state) is None

    resumed = target.step(first.state, first.environment)

    assert resumed.stop_reason is None
    assert resumed.state == expected.state
    assert resumed.state.attempts == 2
    assert resumed.state.history.status_by_hypothesis["h2"] == "CONSERVATIVE-UNKNOWN"
    assert "h2" in resumed.state.history.hypotheses
    assert dict(target_model.context.provenance_store.records()) == records_before
    assert target._state_error(resumed.state) is None


def test_resumed_checkpoint_rejects_a_coordinated_conservative_status_promotion() -> None:
    """Changing both ledger and terminal history cannot promote a C-U member."""

    class NoDispatchEnvironment:
        calls = 0

        def execute(self, _request: ExecutionRequest) -> object:
            self.calls += 1
            raise AssertionError("tampered checkpoint must be rejected before dispatch")

    binding, base, fixture = _runtime_parts()
    prep = _action(
        fixture, "test-router", action_id="prep-q0-q1", kind="PREP",
        enabled_summaries=["before"], declared_target="prepared-target",
    )
    transition = prep["transition"]
    assert isinstance(transition, dict)
    transition.update({
        "target": "q1",
        "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q1"}],
    })
    model = _model_with(base, fixture, [prep])
    session = ReferenceSession(
        binding=binding, model=model,
        session_id="session-reject-conservative-promotion", run_id="run-reject-conservative-promotion",
        initial_summary="before", resources=ResourceState.rounds(1), retry_cap=2,
        initial_path_bundles=_seed_with_conservative_h2(
            model, root_id="root:h2:reject-conservative-promotion",
        ),
    )
    first = session.step(session.initial_state, _environment({
        "private-0": {
            "prep-q0-q1": _prep_recover(
                target_confirmed=True, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="prepared-target", evidence="synthetic:prep:reject-promotion",
                post_summary="after", next_state="private-1",
            ),
        },
    }))
    assert first.stop_reason is None
    assert first.state.history.status_by_hypothesis["h2"] == "CONSERVATIVE-UNKNOWN"

    forged_status = dict(first.state.history.status_by_hypothesis)
    forged_status["h2"] = "KNOWN"
    forged_history = HistoryHandle.committed(
        hypotheses=first.state.history.hypotheses,
        compatible_state_by_hypothesis=first.state.history.compatible_state_by_hypothesis,
        status_by_hypothesis=forged_status,
        version=first.state.history.version,
    )
    forged_evidence = replace(first.state.evidence[0], history_after=forged_history)
    forged_state = replace(
        first.state,
        history=forged_history,
        evidence=(forged_evidence,),
    )
    environment = NoDispatchEnvironment()

    rejected = session.step(forged_state, environment)  # type: ignore[arg-type]

    assert rejected.stop_reason == "Stop-Error"
    assert rejected.state is forged_state
    assert rejected.diagnostics[0].code == "EVIDENCE-COMMIT-MISMATCH"
    assert environment.calls == 0


@pytest.mark.parametrize(
    ("outcome", "label"),
    [
        (lambda: _not_sent("private-1"), "CONFIRMED-NOT-SENT"),
        (lambda: _unknown("private-1"), "UNKNOWN-EFFECT"),
    ],
)
def test_exact_cns_and_unknown_stale_deliveries_remain_idempotent(
    outcome: object,
    label: str,
) -> None:
    """Strict duplicate comparison must retain legitimate non-normal deliveries."""

    binding, base, fixture = _runtime_parts()
    model = _model_with(base, fixture, [
        _action(fixture, "test-router", action_id="test-q0", kind="TEST", enabled_summaries=["q0"]),
    ])
    session = ReferenceSession(
        binding=binding, model=model, session_id=f"session-duplicate-{label}", run_id=f"run-duplicate-{label}",
        initial_summary="q0", resources=ResourceState.rounds(3), retry_cap=3,
    )
    assert callable(outcome)
    first = session.step(session.initial_state, _environment({
        "private-0": {"test-q0": outcome()},
    }))
    assert first.stop_reason is None
    canonical = first.state.evidence[-1].execution
    assert canonical.effect_class == label

    replayed = session.step(first.state, first.environment.with_pending_delivery(replace(canonical)))

    assert replayed.stop_reason is None
    assert replayed.diagnostics[-1].code == "DUPLICATE-EXECUTION-EVIDENCE"
    assert replayed.state is first.state
    assert replayed.state.resources == first.state.resources
    assert replayed.state.evidence == first.state.evidence


def test_exact_prep_and_recover_stale_deliveries_remain_idempotent() -> None:
    """Strict ingress must not turn valid typed recovery results into conflicts."""

    binding, base, fixture = _runtime_parts()
    prep_model = _gap_and_prep_model(binding, base, fixture)
    prep_session = ReferenceSession(
        binding=binding, model=prep_model, session_id="session-duplicate-prep", run_id="run-duplicate-prep",
        initial_summary="q0", resources=ResourceState.rounds(3), retry_cap=2,
    )
    committed_prep = prep_session.step(prep_session.initial_state, _environment({
        "private-0": {
            "prep-q0": _prep_recover(
                target_confirmed=True, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="prepared-q1", evidence="synthetic:prep:duplicate",
                post_summary="q1", next_state="private-1",
            ),
        },
    }))
    prep_duplicate = replace(
        committed_prep.state.evidence[-1].execution,
        prep_recover=replace(committed_prep.state.evidence[-1].execution.prep_recover),
    )
    prep_replayed = prep_session.step(
        committed_prep.state,
        committed_prep.environment.with_pending_delivery(prep_duplicate),
    )
    assert prep_replayed.stop_reason is None
    assert prep_replayed.diagnostics[-1].code == "DUPLICATE-EXECUTION-EVIDENCE"
    assert prep_replayed.state is committed_prep.state

    recover_model = _router_recover_model(base, fixture)
    recover_session = ReferenceSession(
        binding=binding, model=recover_model, session_id="session-duplicate-recover", run_id="run-duplicate-recover",
        initial_summary="q0", resources=ResourceState.rounds(3), retry_cap=2,
    )
    unknown = recover_session.step(recover_session.initial_state, _environment({
        "private-0": {"test-q0": _unknown("private-1")},
        "private-1": {
            "recover-q": _prep_recover(
                target_confirmed=True, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="recovered-q1", evidence="synthetic:recover:duplicate",
                post_summary="q1", next_state="private-2",
            ),
        },
    }))
    committed_recover = recover_session.step(unknown.state, unknown.environment)
    recover_duplicate = replace(
        committed_recover.state.evidence[-1].execution,
        prep_recover=replace(committed_recover.state.evidence[-1].execution.prep_recover),
    )
    recover_replayed = recover_session.step(
        committed_recover.state,
        committed_recover.environment.with_pending_delivery(recover_duplicate),
    )
    assert recover_replayed.stop_reason is None
    assert recover_replayed.diagnostics[-1].code == "DUPLICATE-EXECUTION-EVIDENCE"
    assert recover_replayed.state is committed_recover.state


def test_blank_recovery_target_is_rejected_at_synthetic_ingress_direct_return_and_resume() -> None:
    """Blank-only declared targets cannot enter through any public boundary."""

    binding, base, fixture = _runtime_parts()
    model = _gap_and_prep_model(binding, base, fixture)
    with pytest.raises(ValueError, match="nonblank"):
        _environment({
            "private-0": {
                "prep-q0": _prep_recover(
                    target_confirmed=True, summary_confirmed=True, prep_error=False, ineligible=False,
                    declared_target="  ", evidence="synthetic:prep:blank", post_summary="q1",
                    next_state="private-1",
                ),
            },
        })

    session = ReferenceSession(
        binding=binding, model=model, session_id="session-blank-target", run_id="run-blank-target",
        initial_summary="q0", resources=ResourceState.rounds(2), retry_cap=2,
    )
    safe_successor = _environment({"private-0": {"prep-q0": _not_sent("private-0")}})

    class BlankReturnEnvironment:
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
                    evidence_ref="synthetic:prep:blank-direct",
                    prep_recover=PrepRecoverResult(
                        target_confirmed=True,
                        summary_confirmed=True,
                        prep_error=False,
                        ineligible=False,
                        declared_target="  ",
                        evidence="synthetic:prep:blank-direct",
                        post_summary="q1",
                    ),
                ),
                safe_successor,
            )

    rejected = session.step(session.initial_state, BlankReturnEnvironment())  # type: ignore[arg-type]
    assert rejected.stop_reason is None
    assert rejected.diagnostics[-1].code == "INVALID-EXECUTION-RECORD"
    assert rejected.state.context.q_status == "UNKNOWN"
    assert rejected.state.context.known_target is None

    blank_resume = replace(
        session.initial_state,
        context=replace(session.initial_state.context, known_target="  "),
    )
    resumed = session.step(blank_resume, safe_successor)
    assert resumed.stop_reason == "Stop-Error"
    assert resumed.state is blank_resume
    assert resumed.diagnostics[0].code == "INVALID-SESSION-CONTEXT"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("target_confirmed", 1),
        ("summary_confirmed", 1),
        ("prep_error", 0),
        ("ineligible", 0),
    ],
)
def test_pending_prep_duplicate_requires_recursive_boolean_types(
    field: str,
    value: object,
) -> None:
    """Nested Prep/Recover booleans cannot exploit bool/int equality."""

    binding, base, fixture = _runtime_parts()
    model = _gap_and_prep_model(binding, base, fixture)
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-nested-duplicate", run_id="run-nested-duplicate",
        initial_summary="q0", resources=ResourceState.rounds(3), retry_cap=2,
    )
    first = session.step(session.initial_state, _environment({
        "private-0": {
            "prep-q0": _prep_recover(
                target_confirmed=True, summary_confirmed=True, prep_error=False, ineligible=False,
                declared_target="prepared-q1", evidence="synthetic:prep:canonical", post_summary="q1",
                next_state="private-1",
            ),
        },
    }))
    canonical = first.state.evidence[-1].execution
    assert canonical.prep_recover is not None
    forged = replace(
        canonical,
        prep_recover=replace(canonical.prep_recover, **{field: value}),
    )
    assert forged == canonical

    rejected = session.step(first.state, first.environment.with_pending_delivery(forged))

    assert rejected.stop_reason == "Stop-Error"
    assert rejected.diagnostics[0].code == "CONFLICTING-EXECUTION-DELIVERY"
    assert rejected.state is first.state
    assert rejected.state.resources == first.state.resources
    assert rejected.state.history == first.state.history
    assert rejected.state.evidence == first.state.evidence


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
    # keep the S7-conservative member status, but the executed finite Recover
    # transition still advances every retained frontier/provenance path.
    assert recovered.state.history.hypotheses == unknown.state.history.hypotheses
    assert recovered.state.history.status_by_hypothesis == unknown.state.history.status_by_hypothesis
    assert {
        path.control_state_id
        for paths in recovered.state.frontiers.values()
        for path in paths
    } == {"q0"}
    assert all(
        len(path.history_provenance) == len(unknown.state.frontiers[hypothesis][0].history_provenance) + 1
        for hypothesis, paths in recovered.state.frontiers.items()
        for path in paths
    )
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
    with pytest.raises(ValueError, match="requires a nonblank declared target"):
        _model_with(base, fixture, [missing_prep_target])

    blank_prep_target = _action(
        fixture, "test-router", action_id="prep-blank", kind="PREP", enabled_summaries=["q0"],
        declared_target="prepared-q1",
    )
    blank_prep_target["declaredTarget"] = "   "
    with pytest.raises(ValueError, match="requires a nonblank declared target"):
        _model_with(base, fixture, [blank_prep_target])
