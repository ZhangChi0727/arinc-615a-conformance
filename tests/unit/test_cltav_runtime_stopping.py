"""Public B/C-2C stop and conservative-equivalence session tests.

These tests deliberately enter through :class:`ReferenceSession` rather than
calling the pure stop helper directly.  They lock the externally visible
EntryStop/PostUpdateStop contract, including causal replay of retained stop
evidence, without claiming a proof backend or a protocol verdict engine.
"""

from __future__ import annotations

import copy
from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from typing import Any, Callable, Mapping

import pytest

from cltav_runtime.bindings import RuntimeAuthorityBinding
from cltav_runtime.kernel import ContractSnapshot, FrontierEntry, ModelContext, initial_entry
from cltav_runtime.model import FiniteSessionModel
from cltav_runtime.session import ReferenceSession, ResourceState
from cltav_runtime.synthetic import SyntheticEnvironment


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "fixtures" / "cltav_runtime" / "two_round_scenarios.json"
DEVELOPMENT_PATH = "configs/engineering/cltav_development_contracts.json"
INTERFACE_PATH = "configs/research/cltav_interface_registry.json"
INTEGRITY_BASELINE_PATH = "configs/engineering/cltav_integrity_obligation_baseline.json"
APPLICABILITY_SCHEMA_PATH = "configs/engineering/cltav_runtime_applicability.schema.json"
APPLICABILITY_MANIFEST_PATH = "configs/engineering/cltav_runtime_applicability.json"
APPLICABILITY_FIXTURE_PATH = "configs/engineering/cltav_runtime_applicability_fixture.json"
_CONTROLLED_APPLICABILITY_PATHS = (
    DEVELOPMENT_PATH,
    INTERFACE_PATH,
    INTEGRITY_BASELINE_PATH,
    APPLICABILITY_SCHEMA_PATH,
    APPLICABILITY_MANIFEST_PATH,
    APPLICABILITY_FIXTURE_PATH,
)


def _head_commit() -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()


def _git_bytes(repository: Path, commit: str, relative_path: str) -> bytes:
    """Read an authority source from its Git object rather than checkout bytes."""

    return subprocess.run(
        ["git", "-C", str(repository), "show", f"{commit}:{relative_path}"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def _write_json(path: Path, value: Mapping[str, Any]) -> bytes:
    payload = (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    path.write_bytes(payload)
    return payload


def _commit_all(repository: Path, message: str) -> str:
    subprocess.run(
        ["git", "-C", str(repository), "add", "."],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    subprocess.run(
        [
            "git", "-C", str(repository), "-c", "user.name=CLTAV stop test",
            "-c", "user.email=stop@example.invalid", "commit", "-qm", message,
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    return subprocess.run(
        ["git", "-C", str(repository), "rev-parse", "HEAD"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()


def _applicability_model(
    repository: Path,
    commit: str,
    model_id: str,
) -> FiniteSessionModel:
    """Construct one fixture-declared model through the public raw-Git contract."""

    fixture = json.loads(_git_bytes(repository, commit, APPLICABILITY_FIXTURE_PATH).decode("utf-8"))
    assert isinstance(fixture, dict)
    models = fixture["models"]
    assert isinstance(models, list)
    row = next(item for item in models if item["id"] == model_id)
    assert isinstance(row, dict)
    algorithm = row["algorithmModel"]
    assert isinstance(algorithm, dict)
    public_model = algorithm["model"]
    assert isinstance(public_model, dict)
    typed_domains = public_model["typedDomains"]
    assert isinstance(typed_domains, dict)
    snapshot = ContractSnapshot.from_git_object(
        repository=repository,
        contract_commit=commit,
        contract_path=DEVELOPMENT_PATH,
    )
    context = ModelContext.build(
        snapshot=snapshot,
        model={
            "stateIds": set(public_model["stateIds"]),
            "clockIds": set(public_model["clockIds"]),
            "typedDomains": {name: set(domain) for name, domain in typed_domains.items()},
        },
        projection_clock="x",
    )
    return FiniteSessionModel.from_mapping(context=context, value=algorithm)


def _temporary_method_only_package(
    tmp_path: Path,
    *,
    mutate_algorithm: Callable[[dict[str, Any]], None],
) -> tuple[RuntimeAuthorityBinding, FiniteSessionModel]:
    """Build one Git-bound METHOD-ONLY package with a controlled model mutation.

    The package tests must exercise the same public source identity and
    applicability resolution as production.  The mutation is therefore
    committed with its manifest fixture hash rebound, instead of injecting a
    hand-built model into a normal binding.
    """

    repository = tmp_path / "method-only-package"
    repository.mkdir(parents=True)
    head = _head_commit()
    for relative_path in _CONTROLLED_APPLICABILITY_PATHS:
        destination = repository / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(_git_bytes(ROOT, head, relative_path))

    fixture_path = repository / APPLICABILITY_FIXTURE_PATH
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    models = fixture["models"]
    assert isinstance(models, list)
    method_only = next(item for item in models if item["id"] == "MODEL-METHOD-ONLY")
    assert isinstance(method_only, dict)
    algorithm = method_only["algorithmModel"]
    assert isinstance(algorithm, dict)
    mutate_algorithm(algorithm)
    fixture_bytes = _write_json(fixture_path, fixture)

    manifest_path = repository / APPLICABILITY_MANIFEST_PATH
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert isinstance(manifest, dict)
    source_bindings = manifest["sourceBindings"]
    assert isinstance(source_bindings, dict)
    fixture_binding = source_bindings["fixture"]
    assert isinstance(fixture_binding, dict)
    fixture_binding["blobSha256"] = sha256(fixture_bytes).hexdigest()
    _write_json(manifest_path, manifest)

    subprocess.run(
        ["git", "-C", str(repository), "init", "-q"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    subprocess.run(
        ["git", "-C", str(repository), "config", "core.autocrlf", "false"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    commit = _commit_all(repository, "controlled method-only stop model")
    binding = RuntimeAuthorityBinding.from_git_objects(
        repository=repository,
        development_commit=commit,
        development_path=DEVELOPMENT_PATH,
        interface_commit=commit,
        interface_path=INTERFACE_PATH,
        applicability_schema_commit=commit,
        applicability_schema_path=APPLICABILITY_SCHEMA_PATH,
        applicability_manifest_commit=commit,
        applicability_manifest_path=APPLICABILITY_MANIFEST_PATH,
        applicability_fixture_commit=commit,
        applicability_fixture_path=APPLICABILITY_FIXTURE_PATH,
        integrity_baseline_commit=commit,
        integrity_baseline_path=INTEGRITY_BASELINE_PATH,
    )
    return binding, _applicability_model(repository, commit, "MODEL-METHOD-ONLY")


def _method_only_session(
    binding: RuntimeAuthorityBinding,
    model: FiniteSessionModel,
    *,
    session_id: str,
    resources: ResourceState,
) -> ReferenceSession:
    return ReferenceSession(
        binding=binding,
        model=model,
        session_id=session_id,
        run_id=f"run-{session_id}",
        initial_summary="q0",
        resources=resources,
        retry_cap=1,
        applicability_context_id="CTX-METHOD-ONLY",
    )


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
        repository=ROOT,
        contract_commit=head,
        contract_path=DEVELOPMENT_PATH,
    )
    algorithm = fixture["algorithmModel"]
    assert isinstance(algorithm, dict)
    public_model = algorithm["model"]
    assert isinstance(public_model, dict)
    typed_domains = public_model["typedDomains"]
    assert isinstance(typed_domains, dict)
    context = ModelContext.build(
        snapshot=snapshot,
        model={
            "stateIds": set(public_model["stateIds"]),
            "clockIds": set(public_model["clockIds"]),
            "typedDomains": {name: set(domain) for name, domain in typed_domains.items()},
        },
        projection_clock="x",
    )
    return binding, FiniteSessionModel.from_mapping(context=context, value=algorithm), fixture


def _action(fixture: dict[str, object], action_id: str) -> dict[str, object]:
    algorithm = fixture["algorithmModel"]
    assert isinstance(algorithm, dict)
    actions = algorithm["actions"]
    assert isinstance(actions, list)
    return copy.deepcopy(next(item for item in actions if item["id"] == action_id))


def _model_with(
    base: FiniteSessionModel,
    fixture: dict[str, object],
    actions: list[dict[str, object]],
    *,
    mutate: Callable[[dict[str, object]], None] | None = None,
) -> FiniteSessionModel:
    algorithm = copy.deepcopy(fixture["algorithmModel"])
    assert isinstance(algorithm, dict)
    algorithm["actions"] = actions
    limits = algorithm["limits"]
    assert isinstance(limits, dict)
    limits["actions"] = len(actions)
    if mutate is not None:
        mutate(algorithm)
    return FiniteSessionModel.from_mapping(context=base.context, value=algorithm)


def _router_only_model(
    base: FiniteSessionModel,
    fixture: dict[str, object],
    *,
    declared_empty: bool = False,
    observation_limit: int | None = None,
    unsupported_guard: bool = False,
) -> FiniteSessionModel:
    router = _action(fixture, "test-router")
    if declared_empty:
        router["declaredEmptyObservableTicks"] = {"declared-empty": 0}
    transition = router["transition"]
    assert isinstance(transition, dict)
    if unsupported_guard:
        transition["guardAst"] = {"tag": "CALL", "name": "unsupported"}

    def mutate(algorithm: dict[str, object]) -> None:
        if observation_limit is not None:
            limits = algorithm["limits"]
            assert isinstance(limits, dict)
            limits["observationClasses"] = observation_limit

    return _model_with(base, fixture, [router], mutate=mutate)


def _single_hypothesis_router_model(
    base: FiniteSessionModel,
    fixture: dict[str, object],
) -> FiniteSessionModel:
    router = _action(fixture, "test-router")
    router["observableByHypothesis"] = {"h0": "branch-alpha"}
    router["measurementTicksByHypothesis"] = {"h0": 0}

    def mutate(algorithm: dict[str, object]) -> None:
        hypotheses = algorithm["hypotheses"]
        limits = algorithm["limits"]
        assert isinstance(hypotheses, list) and isinstance(limits, dict)
        algorithm["hypotheses"] = [item for item in hypotheses if item["id"] == "h0"]
        limits["hypotheses"] = 1

    return _model_with(base, fixture, [router], mutate=mutate)


def _environment(fixture: dict[str, object], name: str = "alpha") -> dict[str, object]:
    environments = fixture["environments"]
    assert isinstance(environments, dict)
    return copy.deepcopy(environments[name])


class _NoDispatch:
    def __init__(self) -> None:
        self.calls = 0

    def execute(self, request: object) -> object:  # pragma: no cover - must not run
        self.calls += 1
        raise AssertionError(f"unexpected S4 dispatch: {request}")


def _session(
    binding: RuntimeAuthorityBinding,
    model: FiniteSessionModel,
    *,
    session_id: str,
    resources: ResourceState,
    retry_cap: int = 1,
    applicability_context_id: str | None = None,
    scenario_id: object | None = None,
    named_645_residuals: object | None = None,
    initial_path_bundles: Mapping[str, tuple[FrontierEntry, ...]] | None = None,
) -> ReferenceSession:
    return ReferenceSession(
        binding=binding,
        model=model,
        session_id=session_id,
        run_id=f"run-{session_id}",
        initial_summary="q0",
        resources=resources,
        retry_cap=retry_cap,
        applicability_context_id=applicability_context_id,
        scenario_id=scenario_id,
        named_645_residuals=named_645_residuals,
        initial_path_bundles=initial_path_bundles,
    )


def test_stop_st01_declared_empty_observable_commits_then_wins_over_same_round_budget() -> None:
    """ST01: a typed declared-empty S4 output reaches processed Stop-Empty."""

    binding, base, fixture = _runtime_parts()
    model = _router_only_model(base, fixture, declared_empty=True)
    environment_data = _environment(fixture)
    states = environment_data["states"]
    assert isinstance(states, dict)
    outcome = states["private-a0"]["test-router"]
    assert isinstance(outcome, dict)
    outcome.update({
        "observable": "declared-empty",
        "measurementTick": 0,
        "postSummary": "empty-q",
    })
    environment = SyntheticEnvironment.from_mapping(environment_data)
    source = _session(binding, model, session_id="st01-empty", resources=ResourceState.rounds(1))

    result = source.step(source.initial_state, environment)

    assert result.stop_reason == "Stop-Empty"
    assert result.stop_trace is not None and result.stop_trace.phase == "POST-UPDATE"
    assert result.stop_trace.final_hypotheses == ()
    assert result.state.history.processed is True
    assert result.state.history.hypotheses == frozenset()
    assert dict(result.state.frontiers) == {}
    assert result.state.resources.remaining == 0
    assert all(item.observable != "declared-empty" for item in result.state.evidence[0].snapshot.classes)
    assert result.state.evidence[0].prediction.declared_empty_observations[0].observable == "declared-empty"

    same_no_dispatch = _NoDispatch()
    same = source.step(result.state, same_no_dispatch)  # type: ignore[arg-type]
    fresh = _session(binding, model, session_id="st01-empty", resources=ResourceState.rounds(1))
    fresh_no_dispatch = _NoDispatch()
    resumed = fresh.step(result.state, fresh_no_dispatch)  # type: ignore[arg-type]
    assert same.stop_reason == resumed.stop_reason == "Stop-Empty"
    assert same.state == resumed.state == result.state
    assert same_no_dispatch.calls == fresh_no_dispatch.calls == 0


def test_stop_st02_singleton_is_a_nonverdict_priority_terminal() -> None:
    """ST02: a normal singleton remains higher priority than a resource stop."""

    binding, base, fixture = _runtime_parts()
    singleton_model = _single_hypothesis_router_model(base, fixture)
    singleton = _session(
        binding,
        singleton_model,
        session_id="st02-singleton",
        resources=ResourceState.rounds(0),
    )
    no_dispatch = _NoDispatch()
    singleton_result = singleton.step(singleton.initial_state, no_dispatch)  # type: ignore[arg-type]
    assert singleton_result.stop_reason == "Stop-Singleton"
    assert singleton_result.stop_trace is not None
    assert singleton_result.stop_trace.final_hypotheses == ("h0",)
    assert no_dispatch.calls == 0


@pytest.mark.parametrize("resources", [ResourceState.rounds(0), ResourceState.budget(0)])
def test_stop_st04_zero_resources_block_dispatch_but_affordable_run_commits_then_stops(
    resources: ResourceState,
) -> None:
    """ST04/ST08: EntryStop has no dispatch; PostUpdate uses new H/resources."""

    binding, base, fixture = _runtime_parts()
    model = _router_only_model(base, fixture)
    entry = _session(binding, model, session_id=f"st04-{resources.mode}", resources=resources)
    entry_no_dispatch = _NoDispatch()
    entry_result = entry.step(entry.initial_state, entry_no_dispatch)  # type: ignore[arg-type]
    assert entry_result.stop_reason == "Stop-Budget"
    assert entry_result.stop_trace is not None and entry_result.stop_trace.phase == "ENTRY"
    assert entry_result.state == entry.initial_state
    assert entry_no_dispatch.calls == 0

    positive_resource = ResourceState.rounds(1) if resources.mode == "ROUNDS" else ResourceState.budget(1)
    executing = _session(binding, model, session_id=f"st04-run-{resources.mode}", resources=positive_resource)
    committed = executing.step(executing.initial_state, SyntheticEnvironment.from_mapping(_environment(fixture)))
    assert committed.stop_reason == "Stop-Budget"
    assert committed.stop_trace is not None and committed.stop_trace.phase == "POST-UPDATE"
    assert committed.stop_trace.final_hypotheses == ("h0", "h1")
    assert committed.stop_trace.resource_remaining == 0
    assert committed.state.evidence[0].snapshot.hypotheses == frozenset({"h0", "h1", "h2", "h3"})
    assert committed.state.evidence[0].stop_trace == committed.stop_trace
    assert entry_result.stop_trace.stop_class == committed.stop_trace.stop_class == "Stop-Budget"
    # The common terminal class does not erase the distinct causal phase: the
    # entry and post-update relations both apply P5 when P1--P4 do not hold.
    assert entry_result.stop_trace.reason == "RESOURCE-EXHAUSTED"
    assert committed.stop_trace.reason == "RESOURCE-EXHAUSTED"
    assert entry_result.stop_trace.active_named_645_residuals == committed.stop_trace.active_named_645_residuals == ()
    assert entry_result.stop_trace.equivalence.action_domain_identity == committed.stop_trace.equivalence.action_domain_identity


def test_stop_st05_retry_cap_error_has_priority_over_resource_exhaustion() -> None:
    """ST05: S7 retry-cap is an error terminal even when the charge reaches 0."""

    binding, base, fixture = _runtime_parts()
    model = _router_only_model(base, fixture)
    not_sent = SyntheticEnvironment.from_mapping(_environment(fixture, "notSent"))
    terminal_session = _session(
        binding, model, session_id="st05-terminal", resources=ResourceState.rounds(1), retry_cap=1,
    )
    terminal = terminal_session.step(terminal_session.initial_state, not_sent)
    assert terminal.stop_reason == "Stop-Error"
    assert terminal.stop_trace is not None
    assert terminal.stop_trace.phase == "RETRY"
    assert terminal.stop_trace.reason == "RETRY-CAP-EXHAUSTED"
    assert terminal.state.resources.remaining == 0
    assert terminal.state.history == terminal_session.initial_state.history
    same_no_dispatch = _NoDispatch()
    assert terminal_session.step(terminal.state, same_no_dispatch).stop_reason == "Stop-Error"  # type: ignore[arg-type]
    assert same_no_dispatch.calls == 0

    source = _session(
        binding, model, session_id="st05-under-cap-real", resources=ResourceState.rounds(2), retry_cap=2,
    )
    retained = source.step(source.initial_state, not_sent)
    assert retained.stop_reason is None
    assert retained.stop_trace is None
    assert retained.state.context.q_status == "KNOWN"
    assert retained.state.context.retry_count == 1
    assert retained.state.resources.remaining == 1

    unknown_data = _environment(fixture)
    unknown_states = unknown_data["states"]
    assert isinstance(unknown_states, dict)
    unknown_outcome = unknown_states["private-a0"]["test-router"]
    assert isinstance(unknown_outcome, dict)
    unknown_outcome.update({
        "effectClass": "UNKNOWN-EFFECT",
        "observable": None,
        "summaryConfirmed": False,
        "postSummary": None,
        "measurementTick": None,
        "nextPrivateState": "private-a1",
    })
    unknown_environment = SyntheticEnvironment.from_mapping(unknown_data)
    unknown_source = _session(
        binding, model, session_id="st05-under-cap-unknown", resources=ResourceState.rounds(2), retry_cap=2,
    )
    unknown_first = unknown_source.step(unknown_source.initial_state, unknown_environment)
    assert unknown_first.stop_reason is None
    assert unknown_first.state.context.q_status == "UNKNOWN"
    assert unknown_first.state.context.retry_count == 1
    assert unknown_first.state.history.hypotheses == unknown_source.initial_state.history.hypotheses
    assert set(unknown_first.state.history.status_by_hypothesis.values()) == {"CONSERVATIVE-UNKNOWN"}
    assert unknown_first.state.frontiers == unknown_source.initial_state.frontiers
    assert unknown_first.state.resources.remaining == 1


@pytest.mark.parametrize("resources", [ResourceState.rounds(1), ResourceState.budget(1)])
def test_stop_st05_nonterminal_not_sent_checkpoint_replays_entry_p5_after_exhaustion(
    resources: ResourceState,
) -> None:
    """ST05: a charged non-send checkpoint reaches the same P5 live and fresh."""

    binding, base, fixture = _runtime_parts()
    model = _router_only_model(base, fixture)
    source = _session(
        binding,
        model,
        session_id=f"st05-replay-p5-{resources.mode}",
        resources=resources,
        retry_cap=2,
    )
    first = source.step(source.initial_state, SyntheticEnvironment.from_mapping(_environment(fixture, "notSent")))

    assert first.stop_reason is None
    assert first.stop_trace is None
    assert first.state.attempts == 1
    assert len(first.state.evidence) == 1
    assert first.state.evidence[0].execution.effect_class == "CONFIRMED-NOT-SENT"
    assert first.state.resources.remaining == 0
    assert first.state.context.retry_count == 1

    same_no_dispatch = _NoDispatch()
    same = source.step(first.state, same_no_dispatch)  # type: ignore[arg-type]
    fresh = _session(
        binding,
        model,
        session_id=f"st05-replay-p5-{resources.mode}",
        resources=resources,
        retry_cap=2,
    )
    fresh_no_dispatch = _NoDispatch()
    replayed = fresh.step(first.state, fresh_no_dispatch)  # type: ignore[arg-type]

    assert same.stop_reason == replayed.stop_reason == "Stop-Budget"
    assert same.stop_trace is not None and replayed.stop_trace is not None
    assert same.stop_trace.phase == replayed.stop_trace.phase == "ENTRY"
    assert same.stop_trace.reason == replayed.stop_trace.reason == "RESOURCE-EXHAUSTED"
    assert same.state == replayed.state == first.state
    assert same_no_dispatch.calls == fresh_no_dispatch.calls == 0


def test_stop_st06_distinguishes_prep_a3_and_prediction_gap() -> None:
    """ST06: a real Prep can enable a later TEST; A3 and GAP stay separate."""

    binding, base, fixture = _runtime_parts()
    no_information = _action(fixture, "test-no-information")
    a3_model = _model_with(base, fixture, [no_information])
    a3 = _session(binding, a3_model, session_id="st06-a3", resources=ResourceState.rounds(1))
    a3_no_dispatch = _NoDispatch()
    a3_result = a3.step(a3.initial_state, a3_no_dispatch)  # type: ignore[arg-type]
    assert a3_result.stop_reason == "Stop-NoDistinguisher"
    assert a3_result.stop_trace is not None
    assert a3_result.stop_trace.equivalence.tag == "notEstablished"
    assert a3_no_dispatch.calls == 0

    gap = _action(fixture, "test-gap")
    gap["enabledSummaries"] = ["q0"]
    gap_model = _model_with(base, fixture, [gap])
    gap_session = _session(binding, gap_model, session_id="st06-gap", resources=ResourceState.rounds(1))
    gap_no_dispatch = _NoDispatch()
    gap_result = gap_session.step(gap_session.initial_state, gap_no_dispatch)  # type: ignore[arg-type]
    assert gap_result.stop_reason == "Stop-Prediction-Gap"
    assert gap_result.stop_trace is not None
    assert gap_result.stop_trace.equivalence.tag == "notEstablished"
    assert gap_no_dispatch.calls == 0

    router = _action(fixture, "test-router")
    router["enabledSummaries"] = ["prep-q1"]
    prep = _action(fixture, "test-router")
    prep.update({
        "id": "prep-for-distinguisher",
        "kind": "PREP",
        "enabledSummaries": ["q0"],
        "declaredTarget": "prepared-target",
        "recoverWhenUnknown": False,
        "detailCharges": {"acquisition": 0, "computation": 0, "preparation": 1, "recovery": 0, "retry": 0},
    })
    prep_transition = prep["transition"]
    assert isinstance(prep_transition, dict)
    prep_transition.update({
        "id": "tr-prep-for-distinguisher",
        "source": "q0",
        "target": "q0",
        "guardAst": {"tag": "TRUE"},
        "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q0"}],
    })
    prep_model = _model_with(base, fixture, [no_information, router, prep])
    environment = SyntheticEnvironment.from_mapping({
        "initialPrivateState": "p0",
        "uncertaintyIdentity": "synthetic-u-1",
        "states": {
            "p0": {
                "prep-for-distinguisher": {
                    "effectClass": "NONE",
                    "observable": None,
                    "summaryConfirmed": True,
                    "postSummary": "prep-q1",
                    "measurementTick": None,
                    "nextPrivateState": "p1",
                    "prepRecover": {
                        "targetConfirmed": False,
                        "summaryConfirmed": True,
                        "prepError": False,
                        "ineligible": False,
                        "declaredTarget": "prepared-target",
                        "evidence": "synthetic:st06:prep",
                        "postSummary": "prep-q1",
                    },
                },
            },
            "p1": {
                "test-router": {
                    "effectClass": "NONE",
                    "observable": "branch-alpha",
                    "summaryConfirmed": True,
                    "postSummary": "branch-alpha",
                    "measurementTick": 0,
                    "nextPrivateState": "p1",
                },
            },
        },
    })
    prep_session = _session(binding, prep_model, session_id="st06-prep", resources=ResourceState.rounds(3))
    first = prep_session.step(prep_session.initial_state, environment)
    second = prep_session.step(first.state, first.environment)
    assert first.stop_reason is None
    assert first.state.evidence[-1].snapshot.action_id == "prep-for-distinguisher"
    assert first.state.context.current_summary == "prep-q1"
    assert first.state.history.hypotheses == frozenset({"h0", "h1", "h2", "h3"})
    assert second.stop_reason is None
    assert second.state.evidence[-1].snapshot.action_id == "test-router"
    assert second.state.evidence[-1].snapshot.q_used_at_select == "prep-q1"
    assert second.state.history.hypotheses == frozenset({"h0", "h1"})


@pytest.mark.parametrize(
    "zero_resources, positive_resources",
    [
        (ResourceState.rounds(0), ResourceState.rounds(1)),
        (ResourceState.budget(0), ResourceState.budget(1)),
    ],
)
def test_stop_st06_method_only_p5_precedes_no_distinguisher_a3(
    tmp_path: Path,
    zero_resources: ResourceState,
    positive_resources: ResourceState,
) -> None:
    """ST06: a package P5 entry stop precedes A3 without rewriting A3."""

    def no_distinguisher(algorithm: dict[str, Any]) -> None:
        actions = algorithm["actions"]
        assert isinstance(actions, list) and len(actions) == 1
        action = actions[0]
        assert isinstance(action, dict)
        action["observableByHypothesis"] = {"m0": "same", "m1": "same"}
        action["measurementTicksByHypothesis"] = {"m0": 0, "m1": 0}

    binding, model = _temporary_method_only_package(
        tmp_path,
        mutate_algorithm=no_distinguisher,
    )
    zero = _method_only_session(
        binding,
        model,
        session_id=f"st06-package-a3-zero-{zero_resources.mode}",
        resources=zero_resources,
    )
    zero_no_dispatch = _NoDispatch()
    zero_result = zero.step(zero.initial_state, zero_no_dispatch)  # type: ignore[arg-type]

    assert zero_result.stop_reason == "Stop-Budget"
    assert zero_result.stop_trace is not None
    assert zero_result.stop_trace.phase == "ENTRY"
    assert zero_result.stop_trace.reason == "RESOURCE-EXHAUSTED"
    assert zero_result.stop_trace.applicability_status == "P3-METHOD-ONLY"
    assert zero_result.stop_trace.active_named_645_residuals == ()
    assert zero_result.state == zero.initial_state
    assert zero_result.state.attempts == 0
    assert zero_no_dispatch.calls == 0

    positive = _method_only_session(
        binding,
        model,
        session_id=f"st06-package-a3-positive-{zero_resources.mode}",
        resources=positive_resources,
    )
    positive_no_dispatch = _NoDispatch()
    positive_result = positive.step(positive.initial_state, positive_no_dispatch)  # type: ignore[arg-type]

    assert positive_result.stop_reason == "Stop-NoDistinguisher"
    assert positive_result.stop_trace is not None
    assert positive_result.stop_trace.phase == "ENTRY"
    assert positive_result.stop_trace.reason == "NO-ADMITTED-ACTION"
    assert positive_result.stop_trace.applicability_status == "P3-METHOD-ONLY"
    assert positive_result.state == positive.initial_state
    assert positive_result.state.attempts == 0
    assert positive_no_dispatch.calls == 0


@pytest.mark.parametrize(
    "zero_resources, positive_resources",
    [
        (ResourceState.rounds(0), ResourceState.rounds(1)),
        (ResourceState.budget(0), ResourceState.budget(1)),
    ],
)
def test_stop_st06_full_prediction_gap_p5_precedes_gap_for_package_and_legacy(
    tmp_path: Path,
    zero_resources: ResourceState,
    positive_resources: ResourceState,
) -> None:
    """ST06: P5 precedes a full GAP in both package and legacy bindings."""

    def unsupported_transition(algorithm: dict[str, Any]) -> None:
        actions = algorithm["actions"]
        assert isinstance(actions, list) and len(actions) == 1
        action = actions[0]
        assert isinstance(action, dict)
        transition = action["transition"]
        assert isinstance(transition, dict)
        transition["guardAst"] = {"tag": "CALL", "name": "unsupported"}

    package_binding, package_model = _temporary_method_only_package(
        tmp_path / "package",
        mutate_algorithm=unsupported_transition,
    )
    package_zero = _method_only_session(
        package_binding,
        package_model,
        session_id=f"st06-package-gap-zero-{zero_resources.mode}",
        resources=zero_resources,
    )
    package_zero_no_dispatch = _NoDispatch()
    package_zero_result = package_zero.step(package_zero.initial_state, package_zero_no_dispatch)  # type: ignore[arg-type]
    assert package_zero_result.stop_reason == "Stop-Budget"
    assert package_zero_result.stop_trace is not None
    assert package_zero_result.stop_trace.reason == "RESOURCE-EXHAUSTED"
    assert package_zero_result.state == package_zero.initial_state
    assert package_zero_no_dispatch.calls == 0

    package_positive = _method_only_session(
        package_binding,
        package_model,
        session_id=f"st06-package-gap-positive-{zero_resources.mode}",
        resources=positive_resources,
    )
    package_positive_no_dispatch = _NoDispatch()
    package_positive_result = package_positive.step(
        package_positive.initial_state,
        package_positive_no_dispatch,
    )  # type: ignore[arg-type]
    assert package_positive_result.stop_reason == "Stop-Prediction-Gap"
    assert package_positive_result.stop_trace is not None
    assert package_positive_result.stop_trace.reason == "PREDICTION-GAP"
    assert package_positive_result.state == package_positive.initial_state
    assert package_positive_no_dispatch.calls == 0

    legacy_binding, base, fixture = _runtime_parts()
    gap = _action(fixture, "test-gap")
    gap["enabledSummaries"] = ["q0"]
    legacy_model = _model_with(base, fixture, [gap])
    legacy_zero = _session(
        legacy_binding,
        legacy_model,
        session_id=f"st06-legacy-gap-zero-{zero_resources.mode}",
        resources=zero_resources,
    )
    legacy_zero_no_dispatch = _NoDispatch()
    legacy_zero_result = legacy_zero.step(legacy_zero.initial_state, legacy_zero_no_dispatch)  # type: ignore[arg-type]
    assert legacy_zero_result.stop_reason == "Stop-Budget"
    assert legacy_zero_result.stop_trace is not None
    assert legacy_zero_result.stop_trace.reason == "RESOURCE-EXHAUSTED"
    assert legacy_zero_result.stop_trace.applicability_status == "P3-UNAVAILABLE"
    assert legacy_zero_result.state == legacy_zero.initial_state
    assert legacy_zero_no_dispatch.calls == 0

    legacy_positive = _session(
        legacy_binding,
        legacy_model,
        session_id=f"st06-legacy-gap-positive-{zero_resources.mode}",
        resources=positive_resources,
    )
    legacy_positive_no_dispatch = _NoDispatch()
    legacy_positive_result = legacy_positive.step(
        legacy_positive.initial_state,
        legacy_positive_no_dispatch,
    )  # type: ignore[arg-type]
    assert legacy_positive_result.stop_reason == "Stop-Prediction-Gap"
    assert legacy_positive_result.stop_trace is not None
    assert legacy_positive_result.stop_trace.reason == "PREDICTION-GAP"
    assert legacy_positive_result.stop_trace.applicability_status == "P3-UNAVAILABLE"
    assert legacy_positive_result.state == legacy_positive.initial_state
    assert legacy_positive_no_dispatch.calls == 0


def test_stop_st07_exposes_conservative_equivalence_scope_for_limit_and_unsupported_ast() -> None:
    """ST07: bounded/unsupported calculation is unknown, never established."""

    binding, base, fixture = _runtime_parts()
    limit_model = _router_only_model(base, fixture, observation_limit=1)
    limit_session = _session(binding, limit_model, session_id="st07-limit", resources=ResourceState.rounds(1))
    limit_no_dispatch = _NoDispatch()
    limit = limit_session.step(limit_session.initial_state, limit_no_dispatch)  # type: ignore[arg-type]
    assert limit.stop_reason == "Stop-Prediction-Gap"
    assert limit.stop_trace is not None
    assert limit.stop_trace.equivalence.tag == "unknown"
    assert limit.stop_trace.equivalence.reason == "CALCULATION-OBSERVATION-CLASS-LIMIT"
    assert limit.stop_trace.equivalence.observation_class_limit == 1
    assert limit.stop_trace.equivalence.hypotheses == ("h0", "h1", "h2", "h3")
    assert limit.stop_trace.equivalence.history_version == 0
    assert limit.stop_trace.equivalence.action_domain_identity
    assert limit.state == limit_session.initial_state
    assert limit.state.history.hypotheses == frozenset({"h0", "h1", "h2", "h3"})
    assert set(limit.state.frontiers) == {"h0", "h1", "h2", "h3"}
    assert limit_no_dispatch.calls == 0

    unsupported_model = _router_only_model(base, fixture, unsupported_guard=True)
    unsupported_session = _session(
        binding, unsupported_model, session_id="st07-unsupported", resources=ResourceState.rounds(1),
    )
    unsupported_no_dispatch = _NoDispatch()
    unsupported = unsupported_session.step(unsupported_session.initial_state, unsupported_no_dispatch)  # type: ignore[arg-type]
    assert unsupported.stop_reason == "Stop-Prediction-Gap"
    assert unsupported.stop_trace is not None
    assert unsupported.stop_trace.equivalence.tag == "unknown"
    assert unsupported.stop_trace.equivalence.reason == "CALCULATION-UNSUPPORTED-GUARD-AST"
    assert "UNSUPPORTED-GUARD-AST" in unsupported.stop_trace.equivalence.calculation_diagnostic_codes
    assert unsupported.stop_reason != "Stop-Equivalent"
    assert unsupported.state == unsupported_session.initial_state
    assert unsupported.state.history.hypotheses == frozenset({"h0", "h1", "h2", "h3"})
    assert unsupported_no_dispatch.calls == 0

    singleton_model = _single_hypothesis_router_model(base, fixture)
    h0 = singleton_model.initial_frontiers["h0"]
    conservative_h0 = initial_entry(
        singleton_model.context,
        hypothesis_id="h0",
        control_state_id=h0.control_state_id,
        clocks=h0.clocks,
        typed_store=h0.typed_store,
        root_id="st07:conservative:h0",
        status="CONSERVATIVE-UNKNOWN",
    )
    conservative_session = _session(
        binding,
        singleton_model,
        session_id="st07-conservative-status",
        resources=ResourceState.rounds(1),
        initial_path_bundles={"h0": (conservative_h0,)},
    )
    conservative_no_dispatch = _NoDispatch()
    conservative = conservative_session.step(conservative_session.initial_state, conservative_no_dispatch)  # type: ignore[arg-type]
    assert conservative.stop_reason == "Stop-Singleton"
    assert conservative.stop_trace is not None
    assert conservative.stop_trace.equivalence.tag == "unknown"
    assert conservative.stop_trace.equivalence.reason == "CONSERVATIVE-UNKNOWN"
    assert conservative.state.frontiers["h0"][0].status == "CONSERVATIVE-UNKNOWN"
    assert conservative_no_dispatch.calls == 0


def test_stop_st08_terminal_same_and_fresh_resume_are_dispatch_idempotent() -> None:
    """ST08: singleton beats exhausted resource and survives portable replay."""

    binding, model, fixture = _runtime_parts()
    source = _session(binding, model, session_id="st08-terminal", resources=ResourceState.rounds(2))
    terminal = source.run(SyntheticEnvironment.from_mapping(_environment(fixture)), maximum_rounds=2)
    assert terminal.stop_reason == "Stop-Singleton"
    assert terminal.stop_trace is not None
    assert terminal.stop_trace.phase == "POST-UPDATE"
    assert terminal.stop_trace.final_hypotheses == ("h0",)
    assert terminal.state.resources.remaining == 0

    same_no_dispatch = _NoDispatch()
    same = source.step(terminal.state, same_no_dispatch)  # type: ignore[arg-type]
    fresh = _session(binding, model, session_id="st08-terminal", resources=ResourceState.rounds(2))
    fresh_no_dispatch = _NoDispatch()
    replayed = fresh.step(terminal.state, fresh_no_dispatch)  # type: ignore[arg-type]
    assert same.stop_reason == replayed.stop_reason == "Stop-Singleton"
    assert same.state == replayed.state == terminal.state
    assert same_no_dispatch.calls == fresh_no_dispatch.calls == 0
    assert same.state.attempts == replayed.state.attempts == terminal.state.attempts
    assert len(same.state.evidence) == len(replayed.state.evidence) == len(terminal.state.evidence)


def test_stop_st09_freezes_residual_inputs_and_rejects_coordinated_stop_trace_tampering() -> None:
    """ST09: causal replay rejects a coordinated terminal-trace forgery."""

    binding, base, fixture = _runtime_parts()
    terminal_source = _session(binding, base, session_id="st09-trace", resources=ResourceState.rounds(2))
    terminal = terminal_source.run(SyntheticEnvironment.from_mapping(_environment(fixture)), maximum_rounds=2)
    assert terminal.stop_reason == "Stop-Singleton"
    final_evidence = terminal.state.evidence[-1]
    assert final_evidence.stop_trace is not None
    forged_trace = replace(final_evidence.stop_trace, stop_class="Stop-Budget", reason="RESOURCE-EXHAUSTED")
    forged_state = replace(
        terminal.state,
        evidence=(terminal.state.evidence[0], replace(final_evidence, stop_reason="Stop-Budget", stop_trace=forged_trace)),
    )
    fresh = _session(binding, base, session_id="st09-trace", resources=ResourceState.rounds(2))
    forged_no_dispatch = _NoDispatch()
    rejected = fresh.step(forged_state, forged_no_dispatch)  # type: ignore[arg-type]
    assert rejected.stop_reason == "Stop-Error"
    assert rejected.diagnostics[0].code == "EVIDENCE-COMMIT-MISMATCH"
    assert forged_no_dispatch.calls == 0


def test_stop_st09_rejects_display_scenario_labels_before_session_creation() -> None:
    """A display scenario label cannot mint applicability for a base binding."""

    binding, base, _fixture = _runtime_parts()
    with pytest.raises(ValueError, match="APPLICABILITY-INPUT-ERROR"):
        _session(
            binding,
            base,
            session_id="st09-unknown-scenario",
            resources=ResourceState.rounds(0),
            scenario_id="SC-NOT-IN-CONTROLLED-CATALOGUE",
        )


def test_stop_st09_rejects_caller_supplied_residual_applicability() -> None:
    """Applicability is projected from the authority, never caller metadata."""

    binding, base, _fixture = _runtime_parts()
    with pytest.raises(ValueError, match="APPLICABILITY-INPUT-ERROR"):
        _session(
            binding,
            base,
            session_id="st09-forged-applicability",
            resources=ResourceState.rounds(0),
            named_645_residuals=(),
        )
