"""Two-round bounded session integration checks without an IUT or network."""

from __future__ import annotations

from collections.abc import Mapping as ABCMapping
import copy
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction
import json
from pathlib import Path
import subprocess
from types import MappingProxyType

import pytest

from cltav_runtime.bindings import RuntimeAuthorityBinding
from cltav_runtime.kernel import ContractSnapshot, Interval, ModelContext, initial_entry, propagate_transition
from cltav_runtime.interpretation import (
    InterpretationContract,
    ObservationInput,
    OwnershipEvent,
    assess_observation,
    bind_observation_input,
    observation_input_from_mapping,
)
from cltav_runtime.model import FiniteSessionModel
from cltav_runtime.session import (
    ReferenceSession,
    ResourceState,
    SessionState,
    _advance_observation_ledger,
    _event_identity_ledger_error,
    _observation_replay_conflict,
    _quarantine_conflicted_observation_ledger,
)
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


def _interval_mapping(
    lower: int, upper: int, *, lower_closed: bool = True, upper_closed: bool = True,
) -> dict[str, object]:
    return {"lower": lower, "upper": upper, "lowerClosed": lower_closed, "upperClosed": upper_closed}


def _runtime_interpretation_contract(
    model: FiniteSessionModel,
    *,
    requirement: Interval | None = None,
    physical: Interval | None = None,
    clock_valid: bool = True,
    error_budget_valid: bool = True,
    deadline_authority: str = "METHOD-ONLY",
    policy: str = "UNIQUE-KEY",
    concurrent_same_key: bool = False,
) -> InterpretationContract:
    """Controlled session contract; environment declarations cannot set it."""

    uncertainty = model.uncertainty
    effective_requirement = requirement or Interval(Fraction(0), Fraction(1), True, True)
    return InterpretationContract(
        "synthetic:bc2b:v1", "REQ", "RESP", "k", policy, concurrent_same_key,
        "CANCEL", "SUPERSEDE",
        physical or Interval(Fraction(-1), Fraction(1), True, True),
        effective_requirement,
        uncertainty.clock_id, uncertainty.uncertainty_id, uncertainty.identity,
        uncertainty.time_unit, clock_valid, error_budget_valid,
        deadline_authority,
        "method:synthetic:upper" if deadline_authority != "UNRESOLVED" else None,
        effective_requirement.upper if deadline_authority != "UNRESOLVED" else None,
        effective_requirement.upper_closed,
    )


def _runtime_observation_material(
    *,
    trigger_id: str = "request-1",
    response_id: str | None = "response-1",
    events: list[dict[str, object]] | None = None,
    measurement: dict[str, object] | None = None,
    horizon: bool = True,
    earliest: int | None = 6,
) -> dict[str, object]:
    """Only raw ordered material; no policy/deadline/verdict is accepted."""

    if events is None:
        events = [{
            "id": trigger_id, "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0,
        }]
        if response_id is not None:
            events.append({
                "id": response_id, "sequence": 2, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0,
            })
    return {
        "events": events,
        "triggerEventId": trigger_id,
        "responseId": response_id,
        "measurementInterval": measurement if response_id is not None else None,
        "observationEndQualified": horizon,
        "earliestElapsed": earliest,
        "clockIdentity": "x",
        "unit": "ticks",
    }


def _environment_with_observation_material(
    fixture: dict[str, object], observation_material: dict[str, object], *,
    state_id: str = "private-a0", action_id: str = "test-router",
    no_response: bool = False,
) -> SyntheticEnvironment:
    source = copy.deepcopy(fixture["environments"]["alpha"])
    assert isinstance(source, dict)
    states = source["states"]
    assert isinstance(states, dict)
    state = states[state_id]
    assert isinstance(state, dict)
    outcome = state[action_id]
    assert isinstance(outcome, dict)
    outcome["observationMaterial"] = observation_material
    if no_response:
        outcome.update({
            "observable": None,
            "summaryConfirmed": False,
            "postSummary": None,
            "measurementTick": None,
        })
    return SyntheticEnvironment.from_mapping(source)


def _two_round_observation_environment(
    fixture: dict[str, object],
    first_material: dict[str, object],
    second_material: dict[str, object],
    *,
    second_no_response: bool = False,
) -> SyntheticEnvironment:
    """Attach raw material to alpha's two public TEST rounds."""

    source = copy.deepcopy(fixture["environments"]["alpha"])
    assert isinstance(source, dict)
    states = source["states"]
    assert isinstance(states, dict)
    first = states["private-a0"]["test-router"]
    second = states["private-a1"]["test-left"]
    assert isinstance(first, dict) and isinstance(second, dict)
    first["observationMaterial"] = first_material
    second["observationMaterial"] = second_material
    if second_no_response:
        second.update({
            "observable": None,
            "summaryConfirmed": False,
            "postSummary": None,
            "measurementTick": None,
        })
    return SyntheticEnvironment.from_mapping(source)


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


@pytest.mark.parametrize(
    ("requirement", "clock_valid", "expected_verdict"),
    (
        (Interval(Fraction(0), Fraction(1), True, True), True, "PASS"),
        (Interval(Fraction(2), Fraction(3), True, True), True, "FAIL"),
        (Interval(Fraction(0), Fraction(1), True, True), False, "ERROR"),
    ),
)
def test_session_replays_bound_raw_ownership_timing_material_before_history_commit(
    requirement: Interval, clock_valid: bool, expected_verdict: str,
) -> None:
    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id=f"session-observation-{expected_verdict}",
        run_id=f"run-observation-{expected_verdict}", initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=_runtime_interpretation_contract(
            model, requirement=requirement, clock_valid=clock_valid,
        ),
    )
    result = session.run(
        _environment_with_observation_material(
            fixture,
            _runtime_observation_material(measurement=_interval_mapping(0, 0)),
        ),
        maximum_rounds=1,
    )
    evidence = result.state.evidence[0]
    assert evidence.observation_assessment is not None
    assert evidence.observation_assessment.verdict == expected_verdict
    if expected_verdict == "ERROR":
        assert result.stop_reason == "Stop-Error"
        assert evidence.committed is False
        assert evidence.rejected_response == evidence.execution
        assert evidence.resolution_code == "OBSERVATION-INTERPRETATION-ERROR"
        assert result.state.history.hypotheses == session.initial_state.history.hypotheses
        assert set(result.state.history.status_by_hypothesis.values()) == {"CONSERVATIVE-UNKNOWN"}
        assert result.state.context.q_status == "UNKNOWN"
        assert result.state.context.current_summary is None
        assert result.state.resources.remaining == 0
        assert result.state.context.retry_count == 1
        assert result.state.attempts == 1
    else:
        # PASS and FAIL are both interpretation evidence.  The compatible
        # history is determined by the selected observable class, not by a
        # timing verdict pretending to be a global candidate deletion.
        assert evidence.committed is True
        assert evidence.resolution_code == "COMMIT"
        assert evidence.observation_assessment.score_disposition == "ENGINEERING-WITNESS"
        assert evidence.observation_assessment.answered is False
        assert result.state.consumed_response_ids == {"response-1"}
        assert result.state.history.hypotheses == {"h0", "h1"}
        assert result.state.context.current_summary == "branch-alpha"
        resumed = session.step(result.state, result.environment)
        assert not any(diagnostic.code.startswith("EVIDENCE-") for diagnostic in resumed.diagnostics)


def test_session_rejects_forged_assessment_before_dispatch_or_second_charge() -> None:
    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-observation-forgery",
        run_id="run-observation-forgery", initial_summary="q0", resources=ResourceState.rounds(2),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    first = session.step(
        session.initial_state,
        _environment_with_observation_material(
            fixture, _runtime_observation_material(measurement=_interval_mapping(0, 0)),
        ),
    )
    assert first.state.evidence[0].observation_assessment is not None
    forged_assessment = replace(first.state.evidence[0].observation_assessment, verdict="FAIL")
    forged_evidence = replace(first.state.evidence[0], observation_assessment=forged_assessment)
    forged_state = replace(first.state, evidence=(forged_evidence,))

    class NoDispatchEnvironment:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:  # pragma: no cover - must not run
            raise AssertionError(f"forged evidence must be rejected before dispatch: {request}")

    rejected = session.step(forged_state, NoDispatchEnvironment())  # type: ignore[arg-type]
    assert rejected.stop_reason == "Stop-Error"
    assert rejected.state is forged_state
    assert rejected.diagnostics[0].code == "EVIDENCE-INTERPRETATION-MISMATCH"


def test_session_records_no_response_without_turning_method_only_deadline_into_scored_protocol_fail() -> None:
    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="session-method-only-silence",
        run_id="run-method-only-silence", initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    result = session.run(
        _environment_with_observation_material(
            fixture,
            _runtime_observation_material(response_id=None, earliest=99),
            no_response=True,
        ),
        maximum_rounds=1,
    )
    evidence = result.state.evidence[0]
    assert evidence.observation_assessment is not None
    assert evidence.observation_assessment.verdict == "INCONCLUSIVE"
    assert evidence.observation_assessment.score_disposition == "PENDING-DEADLINE"
    assert evidence.observation_assessment.answered is False
    assert evidence.committed is False
    assert evidence.resolution_code == "OBSERVATION-NO-RESPONSE"
    assert evidence.rejected_response is None
    assert result.state.history.hypotheses == session.initial_state.history.hypotheses
    assert result.state.context.current_summary is None
    assert result.state.consumed_response_ids == frozenset()
    assert result.state.terminal_trigger_event_ids == frozenset()
    resumed = session.step(result.state, result.environment)
    assert not any(diagnostic.code in {"SESSION-LINEAGE-MISMATCH", "EVIDENCE-NO-RESPONSE-MISMATCH"} for diagnostic in resumed.diagnostics)


def test_session_retains_unqualified_silence_without_an_elapsed_reading_as_a_portable_checkpoint() -> None:
    """An unfinished observation window is pending, not an S7 input error."""

    binding, model, fixture = _runtime_parts()
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": "session-pending-silence",
        "run_id": "run-pending-silence",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(1),
        "interpretation_contract": _runtime_interpretation_contract(model),
    }
    source = ReferenceSession(**kwargs)
    result = source.step(
        source.initial_state,
        _environment_with_observation_material(
            fixture,
            _runtime_observation_material(response_id=None, horizon=False, earliest=None),
            no_response=True,
        ),
    )
    evidence = result.state.evidence[0]
    assert evidence.resolution_code == "OBSERVATION-NO-RESPONSE"
    assert evidence.observation_assessment is not None
    assert evidence.observation_assessment.verdict == "INCONCLUSIVE"
    assert evidence.observation_assessment.score_disposition == "PENDING-HORIZON"
    assert evidence.committed is False
    assert result.state.active_trigger_event_ids == {"request-1"}

    target = ReferenceSession(**kwargs)
    assert target._state_error(result.state) is None


def test_synthetic_declaration_rejects_conflicting_silence_and_normal_response_fields() -> None:
    _binding, _model, fixture = _runtime_parts()
    # A raw no-response material declaration cannot coexist with a normal
    # observable/summary, so it never reaches a session S9 path.
    source = copy.deepcopy(fixture["environments"]["alpha"])
    assert isinstance(source, dict)
    outcome = source["states"]["private-a0"]["test-router"]
    assert isinstance(outcome, dict)
    outcome["observationMaterial"] = _runtime_observation_material(response_id=None)
    with pytest.raises(ValueError, match="response-free TEST"):
        SyntheticEnvironment.from_mapping(source)


def test_session_rejects_reviewed_deadline_and_mismatched_uncertainty_contract() -> None:
    binding, model, _fixture = _runtime_parts()
    with pytest.raises(ValueError, match="reviewed-deadline"):
        ReferenceSession(
            binding=binding, model=model, session_id="reviewed", run_id="reviewed", initial_summary="q0",
            resources=ResourceState.rounds(1),
            interpretation_contract=_runtime_interpretation_contract(model, deadline_authority="REVIEWED"),
        )
    contract = _runtime_interpretation_contract(model)
    with pytest.raises(ValueError, match="uncertainty"):
        ReferenceSession(
            binding=binding, model=model, session_id="mismatch", run_id="mismatch", initial_summary="q0",
            resources=ResourceState.rounds(1),
            interpretation_contract=replace(contract, unit="milliseconds"),
        )

    class StringSubclass(str):
        pass

    # Contract identity is a closed public input: ordinary Python string
    # equality must not let a subclass alter the canonical deadline identity.
    with pytest.raises(ValueError, match="invalid"):
        ReferenceSession(
            binding=binding, model=model, session_id="deadline-subclass", run_id="deadline-subclass",
            initial_summary="q0", resources=ResourceState.rounds(1),
            interpretation_contract=replace(contract, deadline_identity=StringSubclass("method:synthetic:upper")),
        )


def test_session_detaches_its_interpretation_contract_before_a_hostile_s4_adapter_runs() -> None:
    """A construction-time METHOD-ONLY boundary cannot be promoted during S4."""

    binding, model, fixture = _runtime_parts()
    contract = _runtime_interpretation_contract(model)
    session = ReferenceSession(
        binding=binding, model=model, session_id="contract-toctou", run_id="contract-toctou",
        initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=contract,
    )
    environment = _environment_with_observation_material(
        fixture,
        _runtime_observation_material(response_id=None, earliest=99),
        no_response=True,
    )

    class MutatingAdapter:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            object.__setattr__(contract, "deadline_authority", "REVIEWED")
            object.__setattr__(contract, "deadline_identity", "forged:reviewed:deadline")
            return environment.execute(request)

    result = session.step(session.initial_state, MutatingAdapter())  # type: ignore[arg-type]
    assessment = result.state.evidence[0].observation_assessment
    assert session.interpretation_contract is not contract
    assert session.interpretation_contract is not None
    assert session.interpretation_contract.deadline_authority == "METHOD-ONLY"
    assert assessment is not None
    assert assessment.verdict == "INCONCLUSIVE"
    assert assessment.score_disposition == "PENDING-DEADLINE"
    assert assessment.answered is False


def test_session_freezes_nested_contract_intervals_and_fraction_leaves_before_s4() -> None:
    """A caller cannot rewrite a parsed timing boundary through its leaf objects."""

    binding, model, fixture = _runtime_parts()
    contract = _runtime_interpretation_contract(model)
    session = ReferenceSession(
        binding=binding, model=model, session_id="nested-contract-toctou", run_id="nested-contract-toctou",
        initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=contract,
    )
    environment = _environment_with_observation_material(
        fixture, _runtime_observation_material(measurement=_interval_mapping(0, 0)),
    )

    class MutatingAdapter:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            # Both are exact Fraction leaves inside caller-owned frozen
            # contract values.  A shallow outer copy would turn the normal
            # [0,0] measurement into a false failure or a changed deadline.
            object.__setattr__(contract.physical_domain.lower, "_numerator", 99)
            object.__setattr__(contract.requirement_window.lower, "_numerator", 1)
            object.__setattr__(contract.upper_bound, "_numerator", 99)
            return environment.execute(request)

    result = session.step(session.initial_state, MutatingAdapter())  # type: ignore[arg-type]
    assessment = result.state.evidence[0].observation_assessment
    assert result.state.evidence[0].committed is True
    assert assessment is not None
    assert assessment.verdict == "PASS"
    assert assessment.physical_interval == Interval(Fraction(0), Fraction(0), True, True)
    assert assessment.requirement_window == Interval(Fraction(0), Fraction(1), True, True)
    target = ReferenceSession(
        binding=binding, model=model, session_id="nested-contract-toctou", run_id="nested-contract-toctou",
        initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    assert target._state_error(result.state) is None


def test_session_private_seed_survives_a_mutated_public_s0_context() -> None:
    """Same-session replay never treats the inspectable S0 object as its seed."""

    binding, model, fixture = _runtime_parts()
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": "public-s0-toctou",
        "run_id": "public-s0-toctou",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(2),
        "interpretation_contract": _runtime_interpretation_contract(model),
    }
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(measurement=_interval_mapping(0, 0)),
        _runtime_observation_material(
            trigger_id="request-2", response_id="response-2",
            events=[
                {"id": "request-2", "sequence": 3, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "response-2", "sequence": 4, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ], measurement=_interval_mapping(0, 0),
        ),
    )
    source = ReferenceSession(**kwargs)
    public_s0 = source.initial_state
    seed_clock_lower = Fraction(
        source._initial_seed_state.frontiers["h0"][0].clocks["x"].lower.numerator,
        source._initial_seed_state.frontiers["h0"][0].clocks["x"].lower.denominator,
    )

    class MutatingAdapter:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            object.__setattr__(public_s0.context, "current_summary", "poison-q")
            object.__setattr__(public_s0.history, "version", 99)
            object.__setattr__(public_s0.frontiers["h0"][0].clocks["x"].lower, "_numerator", 99)
            return environment.execute(request)

    first = source.step(public_s0, MutatingAdapter())  # type: ignore[arg-type]
    advanced = source.step(first.state, first.environment)
    assert source._initial_seed_state.context.current_summary == "q0"
    assert source._initial_seed_state.history.version == 0
    assert source._initial_seed_state.frontiers["h0"][0].clocks["x"].lower == seed_clock_lower
    assert first.state.evidence[-1].committed is True
    assert advanced.state.evidence[-1].committed is True
    target = ReferenceSession(**kwargs)
    assert target._state_error(advanced.state) is None


@pytest.mark.parametrize("resources", (ResourceState.rounds(2), ResourceState.budget(2)))
def test_session_freezes_model_authority_before_a_hostile_s4_adapter_runs(
    resources: ResourceState,
) -> None:
    """Caller-held action charges cannot diverge same and fresh replay."""

    binding, model, fixture = _runtime_parts()
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": f"model-authority-toctou-{resources.mode.lower()}",
        "run_id": f"model-authority-toctou-{resources.mode.lower()}",
        "initial_summary": "q0",
        "resources": resources,
    }
    source = ReferenceSession(**kwargs)
    environment = SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"])
    original_charge = model.actions["test-router"].detail_charges["computation"]

    class MutatingAdapter:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            if request.action_id == "test-router":
                forged_charges = dict(model.actions["test-router"].detail_charges)
                forged_charges["computation"] = original_charge + 76
                object.__setattr__(
                    model.actions["test-router"], "detail_charges", MappingProxyType(forged_charges),
                )
                # This second action must still be selected from the frozen
                # model, not from the caller object the adapter just mutated.
                object.__setattr__(model.actions["test-left"], "enabled_summaries", frozenset())
            return environment.execute(request)

    result = source.run(MutatingAdapter(), maximum_rounds=2)  # type: ignore[arg-type]

    assert [item.snapshot.action_id for item in result.state.evidence] == ["test-router", "test-left"]
    assert result.state.evidence[0].detail_charges["computation"] == original_charge
    assert result.state.resources.remaining == 0
    assert source._state_error(result.state) is None
    fresh_binding, fresh_model, _fresh_fixture = _runtime_parts()
    target = ReferenceSession(
        binding=fresh_binding, model=fresh_model,
        session_id=f"model-authority-toctou-{resources.mode.lower()}",
        run_id=f"model-authority-toctou-{resources.mode.lower()}",
        initial_summary="q0", resources=resources,
    )
    assert target._state_error(result.state) is None


@pytest.mark.parametrize("mutate_before_s3", (True, False))
def test_session_freezes_binding_identity_before_selection_and_s4(
    mutate_before_s3: bool,
) -> None:
    """Authority evidence comes from the construction snapshot, not caller aliases."""

    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model,
        session_id=f"binding-authority-{mutate_before_s3}",
        run_id=f"binding-authority-{mutate_before_s3}",
        initial_summary="q0", resources=ResourceState.rounds(1),
    )
    original_blob = session._authority_identities["interfaceRegistry"]["blobSha256"]
    forged_blob = "f" * 64
    environment = SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"])

    def mutate_binding() -> None:
        object.__setattr__(binding.interfaces, "blob_sha256", forged_blob)

    if mutate_before_s3:
        mutate_binding()

        class Adapter:
            def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
                return environment.execute(request)
    else:
        class Adapter:
            def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
                mutate_binding()
                return environment.execute(request)

    result = session.step(session.initial_state, Adapter())  # type: ignore[arg-type]

    assert result.state.evidence[0].committed is True
    assert result.state.evidence[0].snapshot.authority_identities["interfaceRegistry"]["blobSha256"] == original_blob
    assert original_blob != forged_blob
    assert session._state_error(result.state) is None
    fresh_binding, fresh_model, _fresh_fixture = _runtime_parts()
    target = ReferenceSession(
        binding=fresh_binding, model=fresh_model,
        session_id=f"binding-authority-{mutate_before_s3}",
        run_id=f"binding-authority-{mutate_before_s3}",
        initial_summary="q0", resources=ResourceState.rounds(1),
    )
    assert target._state_error(result.state) is None


@pytest.mark.parametrize(
    ("snapshot_name", "field_name", "forged_value"),
    (
        ("interfaces", "blob_sha256", "0" * 64),
        ("interfaces", "commit", "f" * 40),
        ("interfaces", "path", "configs/research/forged_registry.json"),
        ("development", "contract_blob_sha256", "0" * 64),
        ("development", "contract_commit", "f" * 40),
        ("development", "contract_path", "configs/engineering/forged_contract.json"),
    ),
)
def test_session_revalidates_raw_binding_snapshots_before_freezing_authority(
    snapshot_name: str,
    field_name: str,
    forged_value: str,
) -> None:
    """A token-bearing alias cannot mint an authority by rewriting its identity."""

    binding, model, _fixture = _runtime_parts()
    snapshot = getattr(binding, snapshot_name)
    object.__setattr__(snapshot, field_name, forged_value)

    with pytest.raises(ValueError, match="session runtime authority is invalid"):
        ReferenceSession(
            binding=binding,
            model=model,
            session_id=f"forged-binding-{snapshot_name}-{field_name}",
            run_id=f"forged-binding-{snapshot_name}-{field_name}",
            initial_summary="q0",
            resources=ResourceState.rounds(1),
        )


def test_session_rejects_a_duck_typed_binding_before_reading_its_identity() -> None:
    """Only a factory-issued RuntimeAuthorityBinding can cross the S0 boundary."""

    binding, model, _fixture = _runtime_parts()

    class DuckBinding:
        development = binding.development

        def identities(self):  # type: ignore[no-untyped-def]
            return binding.identities()

    with pytest.raises(ValueError, match="session runtime authority is invalid"):
        ReferenceSession(
            binding=DuckBinding(),  # type: ignore[arg-type]
            model=model,
            session_id="duck-binding",
            run_id="duck-binding",
            initial_summary="q0",
            resources=ResourceState.rounds(1),
        )


@pytest.mark.parametrize(
    "mutation",
    ("detail-charge", "enabled-summary", "transition", "uncertainty"),
)
def test_session_revalidates_model_semantics_before_freezing_authority(
    mutation: str,
) -> None:
    """A stale model identity cannot authorize rewritten finite semantics at S0."""

    binding, model, _fixture = _runtime_parts()
    action = model.actions["test-router"]
    if mutation == "detail-charge":
        charges = dict(action.detail_charges)
        charges["computation"] += 99
        object.__setattr__(action, "detail_charges", MappingProxyType(charges))
    elif mutation == "enabled-summary":
        object.__setattr__(action, "enabled_summaries", frozenset({"forged-summary"}))
    elif mutation == "transition":
        object.__setattr__(action, "transition_json", '{"id":"forged","guardAst":{"kind":"TRUE"},"updateAst":[]}')
    else:
        object.__setattr__(model.uncertainty, "maximum_error", Fraction(99))

    with pytest.raises(ValueError, match="session runtime authority is invalid"):
        ReferenceSession(
            binding=binding,
            model=model,
            session_id=f"forged-model-{mutation}",
            run_id=f"forged-model-{mutation}",
            initial_summary="q0",
            resources=ResourceState.rounds(1),
        )


def test_session_rebuilds_its_private_model_without_a_postcheck_action_map_read() -> None:
    """A changing public action map cannot race S0's model reconstruction."""

    binding, model, fixture = _runtime_parts()
    original_actions = dict(model.actions)
    original_charge = original_actions["test-router"].detail_charges["computation"]

    class SecondReadMutatesActions(ABCMapping[str, object]):
        """Return valid actions once, then forge a charge on a later read."""

        def __init__(self) -> None:
            self.calls = 0
            self.values = dict(original_actions)

        def __getitem__(self, key: str) -> object:
            return self.values[key]

        def __iter__(self):  # type: ignore[no-untyped-def]
            return iter(self.values)

        def __len__(self) -> int:
            return len(self.values)

        def items(self):  # type: ignore[no-untyped-def]
            self.calls += 1
            if self.calls == 2:
                forged = dict(original_actions["test-router"].detail_charges)
                forged["computation"] = original_charge + 99
                object.__setattr__(
                    original_actions["test-router"], "detail_charges", MappingProxyType(forged),
                )
            return self.values.items()

    racing_actions = SecondReadMutatesActions()
    object.__setattr__(model, "actions", racing_actions)
    session = ReferenceSession(
        binding=binding, model=model,
        session_id="model-source-race", run_id="model-source-race",
        initial_summary="q0", resources=ResourceState.budget(4),
    )
    result = session.run(
        SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"]), maximum_rounds=1,
    )

    # S0 inspected the public map once for malformed pre-existing state but
    # rebuilt the private runtime model from its canonical JSON.  The former
    # validate-then-copy shape would need a second map traversal and would
    # admit the forged charge into the private projection.
    assert racing_actions.calls == 1
    assert result.state.evidence[0].detail_charges["computation"] == original_charge
    assert session._model.actions["test-router"].detail_charges["computation"] == original_charge


def test_session_rejects_an_exact_looking_context_scalar_subclass() -> None:
    """Context authority cannot rely on an equality-compatible string alias."""

    binding, model, _fixture = _runtime_parts()

    class ExactLookingString(str):
        pass

    # The normal string representation leaves the old digest text unchanged,
    # so this specifically exercises the exact-carrier check rather than a
    # simple digest mismatch.
    object.__setattr__(model.context, "projection_clock", ExactLookingString("x"))

    with pytest.raises(ValueError, match="session runtime authority is invalid"):
        ReferenceSession(
            binding=binding, model=model,
            session_id="context-string-subclass", run_id="context-string-subclass",
            initial_summary="q0", resources=ResourceState.rounds(1),
        )


def test_session_rejects_a_duck_typed_model_before_reading_model_context() -> None:
    """A genuine binding cannot make an arbitrary model object authoritative."""

    binding, model, _fixture = _runtime_parts()

    class DuckModel:
        context = model.context

    with pytest.raises(ValueError, match="session runtime authority is invalid"):
        ReferenceSession(
            binding=binding,
            model=DuckModel(),  # type: ignore[arg-type]
            session_id="duck-model",
            run_id="duck-model",
            initial_summary="q0",
            resources=ResourceState.rounds(1),
        )


@pytest.mark.parametrize("resources", (ResourceState.rounds(2), ResourceState.budget(2)))
@pytest.mark.parametrize("outcome", ("CONFIRMED-NOT-SENT", "TOOL-ERROR"))
def test_session_keeps_the_frozen_model_charge_on_noncommit_paths(
    resources: ResourceState,
    outcome: str,
) -> None:
    """S4 model aliases cannot rewrite a CNS/tool-error one-charge receipt."""

    binding, model, fixture = _runtime_parts()
    session_id = f"frozen-charge-{outcome.lower()}-{resources.mode.lower()}"
    source = ReferenceSession(
        binding=binding, model=model, session_id=session_id, run_id=session_id,
        initial_summary="q0", resources=resources, retry_cap=1,
    )
    original_charge = model.actions["test-router"].detail_charges["computation"]
    not_sent = SyntheticEnvironment.from_mapping(fixture["environments"]["notSent"])

    class MutatingAdapter:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            forged_charges = dict(model.actions["test-router"].detail_charges)
            forged_charges["computation"] = original_charge + 76
            object.__setattr__(
                model.actions["test-router"], "detail_charges", MappingProxyType(forged_charges),
            )
            if outcome == "TOOL-ERROR":
                raise RuntimeError("controlled hostile adapter error")
            return not_sent.execute(request)

    result = source.step(source.initial_state, MutatingAdapter())  # type: ignore[arg-type]

    evidence = result.state.evidence[0]
    assert evidence.committed is False
    assert evidence.issued_to_executor is True
    assert evidence.charged_once is True
    assert evidence.detail_charges["computation"] == original_charge
    assert result.state.resources == ResourceState(resources.mode, resources.remaining - 1)
    assert outcome == evidence.execution.effect_class or (
        outcome == "TOOL-ERROR" and evidence.execution.effect_class == "UNKNOWN-EFFECT"
    )
    fresh_binding, fresh_model, _fresh_fixture = _runtime_parts()
    target = ReferenceSession(
        binding=fresh_binding, model=fresh_model, session_id=session_id, run_id=session_id,
        initial_summary="q0", resources=resources, retry_cap=1,
    )
    assert target._state_error(result.state) is None


def test_session_rejects_conflicting_silence_shape_at_the_public_adapter_boundary() -> None:
    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="adapter-silence", run_id="adapter-silence",
        initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    raw = observation_input_from_mapping(_runtime_observation_material(response_id=None))
    bound = bind_observation_input(
        raw,
        execution_attempt_id="adapter-silence:adapter-silence:execution:1",
        action_id="test-router",
        evidence_ref="adapter:silence:1",
        measurement_tick=None,
        uncertainty_identity=None,
    )
    record = VisibleExecutionRecord(
        execution_attempt_id="adapter-silence:adapter-silence:execution:1",
        action_id="test-router",
        effect_class="NONE",
        observable="branch-alpha",
        summary_confirmed=True,
        post_summary="branch-alpha",
        measurement_tick=Fraction(0),
        uncertainty_identity=model.uncertainty_identity,
        evidence_ref="adapter:silence:1",
        response_id=None,
        observation_input=bound,
    )
    successor = SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"])

    class Adapter:
        def execute(self, _request: ExecutionRequest) -> EnvironmentExecution:
            return EnvironmentExecution(record, successor)

    result = session.step(session.initial_state, Adapter())  # type: ignore[arg-type]
    evidence = result.state.evidence[0]
    assert evidence.committed is False
    assert evidence.resolution_code == "INVALID-EXECUTION-RECORD"
    assert evidence.summary_after is None


def test_session_consumes_a_response_identity_only_once_across_attempts() -> None:
    binding, model, fixture = _runtime_parts()
    source = copy.deepcopy(fixture["environments"]["alpha"])
    assert isinstance(source, dict)
    states = source["states"]
    assert isinstance(states, dict)
    first = states["private-a0"]["test-router"]
    second = states["private-a1"]["test-left"]
    assert isinstance(first, dict) and isinstance(second, dict)
    first["observationMaterial"] = _runtime_observation_material(measurement=_interval_mapping(0, 0))
    second["observationMaterial"] = _runtime_observation_material(
        trigger_id="request-2",
        response_id="response-1",
        measurement=_interval_mapping(0, 0),
        events=[
            # The exact historical receipt is not a new delta fact.  It must
            # remain a duplicate response rather than obtain a new pairing.
            {"id": "response-1", "sequence": 2, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
        ],
    )
    session = ReferenceSession(
        binding=binding, model=model, session_id="reused-response", run_id="reused-response",
        initial_summary="q0", resources=ResourceState.rounds(2), retry_cap=2,
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    first_result = session.step(session.initial_state, SyntheticEnvironment.from_mapping(source))
    assert first_result.state.evidence[0].committed is True
    second_result = session.step(first_result.state, first_result.environment)
    evidence = second_result.state.evidence[-1]
    assert evidence.observation_assessment is not None
    assert evidence.observation_assessment.response_id == "response-1"
    assert evidence.committed is False
    assert evidence.resolution_code == "DUPLICATE-OBSERVATION-RESPONSE"
    assert evidence.rejected_response == evidence.execution
    assert second_result.state.consumed_response_ids == {"response-1"}
    # A duplicate response is a cross-round replay conflict, not a fresh
    # response that may discharge the newly named request in this trace.
    assert second_result.state.terminal_trigger_event_ids == {"request-1"}
    assert "request-2" not in second_result.state.active_trigger_event_ids
    assert session._state_error(second_result.state) is None


def test_session_rejects_a_new_response_for_an_already_terminal_trigger_instance() -> None:
    binding, model, fixture = _runtime_parts()
    source = copy.deepcopy(fixture["environments"]["alpha"])
    assert isinstance(source, dict)
    states = source["states"]
    assert isinstance(states, dict)
    first = states["private-a0"]["test-router"]
    second = states["private-a1"]["test-left"]
    assert isinstance(first, dict) and isinstance(second, dict)
    first["observationMaterial"] = _runtime_observation_material(measurement=_interval_mapping(0, 0))
    second["observationMaterial"] = _runtime_observation_material(
        trigger_id="request-1",
        response_id="response-2",
        measurement=_interval_mapping(0, 0),
        events=[
            {"id": "request-1", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
            {"id": "response-2", "sequence": 3, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
        ],
    )
    session = ReferenceSession(
        binding=binding, model=model, session_id="reused-trigger", run_id="reused-trigger",
        initial_summary="q0", resources=ResourceState.rounds(2), retry_cap=2,
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    first_result = session.step(session.initial_state, SyntheticEnvironment.from_mapping(source))
    second_result = session.step(first_result.state, first_result.environment)
    evidence = second_result.state.evidence[-1]
    assert first_result.state.terminal_trigger_event_ids == {"request-1"}
    assert evidence.committed is False
    assert evidence.resolution_code == "DUPLICATE-OBSERVATION-TRIGGER"
    assert second_result.state.consumed_response_ids == {"response-1", "response-2"}
    assert second_result.state.terminal_trigger_event_ids == {"request-1"}
    resumed = session.step(second_result.state, second_result.environment)
    assert not any(diagnostic.code in {"SESSION-LINEAGE-MISMATCH", "EVIDENCE-DUPLICATE-TRIGGER-MISMATCH"} for diagnostic in resumed.diagnostics)


def test_session_terminally_records_an_ambiguous_response_token() -> None:
    binding, model, fixture = _runtime_parts()
    events = [
        {"id": "request-a", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "request-b", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "ambiguous-response", "sequence": 3, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    session = ReferenceSession(
        binding=binding, model=model, session_id="ambiguous-response", run_id="ambiguous-response",
        initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=_runtime_interpretation_contract(model, concurrent_same_key=True),
    )
    result = session.step(
        session.initial_state,
        _environment_with_observation_material(
            fixture,
            _runtime_observation_material(
                trigger_id="request-a", response_id="ambiguous-response",
                events=events, measurement=_interval_mapping(0, 0),
            ),
        ),
    )
    evidence = result.state.evidence[0]
    assert evidence.committed is False
    assert evidence.resolution_code == "OBSERVATION-INTERPRETATION-ERROR"
    assert result.state.consumed_response_ids == {"ambiguous-response"}
    assert result.state.terminal_trigger_event_ids == {"request-a", "request-b"}
    resumed = session.step(result.state, result.environment)
    assert not any(diagnostic.code in {"SESSION-LINEAGE-MISMATCH", "EVIDENCE-INTERPRETATION-MISMATCH"} for diagnostic in resumed.diagnostics)


def test_session_terminalises_an_owned_trigger_when_clock_validation_rejects_its_response() -> None:
    """An owned response cannot be rebound after a T5 clock-chain error."""

    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="clock-terminal", run_id="clock-terminal",
        initial_summary="q0", resources=ResourceState.rounds(2), retry_cap=2,
        interpretation_contract=_runtime_interpretation_contract(model, clock_valid=False),
    )
    result = session.step(
        session.initial_state,
        _environment_with_observation_material(
            fixture, _runtime_observation_material(measurement=_interval_mapping(0, 0)),
        ),
    )
    evidence = result.state.evidence[0]
    assert evidence.resolution_code == "OBSERVATION-INTERPRETATION-ERROR"
    assert evidence.observation_assessment is not None
    assert evidence.observation_assessment.diagnostics[0].code == "INVALID-CLOCK-CHAIN"
    assert result.state.consumed_response_ids == {"response-1"}
    assert result.state.terminal_trigger_event_ids == {"request-1"}

    # A resumed session must replay the same terminal ledger before it issues
    # any subsequent action; it must not re-open request-1 merely because the
    # response was rejected after ownership had been determined.
    resumed = session.step(result.state, result.environment)
    assert not any(
        diagnostic.code in {"SESSION-LINEAGE-MISMATCH", "EVIDENCE-INTERPRETATION-MISMATCH"}
        for diagnostic in resumed.diagnostics
    )


def test_session_lineage_rejects_type_coerced_observation_material_before_dispatch() -> None:
    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="strict-material", run_id="strict-material",
        initial_summary="q0", resources=ResourceState.rounds(2),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    first = session.step(
        session.initial_state,
        _environment_with_observation_material(
            fixture, _runtime_observation_material(measurement=_interval_mapping(0, 0)),
        ),
    )
    original = first.state.evidence[0]
    assert original.execution.observation_input is not None
    coerced_material = replace(original.execution.observation_input, observation_end_qualified=1)
    coerced_record = replace(original.execution, observation_input=coerced_material)
    coerced_evidence = replace(original, execution=coerced_record)
    coerced_state = replace(first.state, evidence=(coerced_evidence,))

    class NoDispatch:
        def execute(self, _request: ExecutionRequest) -> EnvironmentExecution:  # pragma: no cover - must not run
            raise AssertionError("invalid evidence must be rejected before dispatch")

    rejected = session.step(coerced_state, NoDispatch())  # type: ignore[arg-type]
    assert rejected.stop_reason == "Stop-Error"
    assert rejected.state is coerced_state
    assert rejected.diagnostics[0].code == "EVIDENCE-INTERPRETATION-MISMATCH"


def test_session_rejects_measurement_material_that_is_not_its_frozen_uncertainty_window() -> None:
    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="wrong-window", run_id="wrong-window",
        initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    result = session.step(
        session.initial_state,
        _environment_with_observation_material(
            fixture,
            _runtime_observation_material(measurement=_interval_mapping(0, 1)),
        ),
    )
    evidence = result.state.evidence[0]
    assert evidence.committed is False
    assert evidence.resolution_code == "OBSERVATION-UNCERTAINTY-WINDOW-MISMATCH"
    assert evidence.observation_assessment is not None
    assert evidence.observation_assessment.verdict == "ERROR"
    assert evidence.observation_assessment.diagnostics[-1].code == "OBSERVATION-UNCERTAINTY-WINDOW-MISMATCH"
    assert result.state.consumed_response_ids == {"response-1"}
    assert result.state.terminal_trigger_event_ids == {"request-1"}
    assert result.state.context.current_summary is None
    resumed = session.step(result.state, result.environment)
    assert not any(
        diagnostic.code in {"SESSION-LINEAGE-MISMATCH", "EVIDENCE-INTERPRETATION-MISMATCH"}
        for diagnostic in resumed.diagnostics
    )


def test_session_replays_every_fifo_trace_fact_and_preserves_the_one_active_request_at_checkpoint() -> None:
    """A selected response is not the extent of a FIFO observation trace."""

    binding, model, fixture = _runtime_parts()
    first_events = [
        {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "B", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    second_events = [
        {"id": "B", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "R2", "sequence": 11, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="A", response_id="R1", events=first_events, measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="B", response_id="R2", events=second_events, measurement=_interval_mapping(0, 0),
        ),
    )
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": "fifo-full-replay",
        "run_id": "fifo-full-replay",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(2),
        "interpretation_contract": _runtime_interpretation_contract(
            model, policy="FIFO", concurrent_same_key=True,
        ),
    }
    source = ReferenceSession(**kwargs)
    first = source.step(source.initial_state, environment)

    assert first.state.evidence[0].committed is True
    assert first.state.consumed_response_ids == {"R1"}
    assert first.state.terminal_trigger_event_ids == {"A"}
    assert first.state.active_trigger_event_ids == {"B"}
    assert set(first.state.event_identity_refs) == {"A", "B", "R1"}

    # A fresh equivalent coordinator proves that the retained active request
    # is a checkpoint fact, not an in-memory continuation shortcut.
    target = ReferenceSession(**kwargs)
    assert target._state_error(first.state) is None
    resumed = target.step(first.state, first.environment)
    assert resumed.state.evidence[-1].committed is True
    assert resumed.state.consumed_response_ids == {"R1", "R2"}
    assert resumed.state.terminal_trigger_event_ids == {"A", "B"}
    assert resumed.state.active_trigger_event_ids == frozenset()
    assert set(resumed.state.event_identity_refs) == {"A", "B", "R1", "R2"}
    assert target._state_error(resumed.state) is None


def test_session_uses_a_retained_fifo_active_request_for_an_incremental_next_observation() -> None:
    """A delta response is still matched against a retained FIFO obligation."""

    binding, model, fixture = _runtime_parts()
    first_events = [
        {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "B", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    # B remains ACTIVE after R1.  The next observation is a legal
    # *incremental* delta: terminal A/R1 and retained B need not be copied
    # again, but the response must still be matched against B.
    incremental_second_events = [
        {"id": "R2", "sequence": 11, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="A", response_id="R1", events=first_events, measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="B", response_id="R2", events=incremental_second_events, measurement=_interval_mapping(0, 0),
        ),
    )
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": "incremental-fifo",
        "run_id": "incremental-fifo",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(2),
        "retry_cap": 2,
        "interpretation_contract": _runtime_interpretation_contract(
            model, policy="FIFO", concurrent_same_key=True,
        ),
    }
    source = ReferenceSession(**kwargs)
    first = source.step(source.initial_state, environment)
    accepted = source.step(first.state, first.environment)

    assert accepted.state.evidence[-1].committed is True
    assert accepted.state.consumed_response_ids == {"R1", "R2"}
    assert accepted.state.terminal_trigger_event_ids == {"A", "B"}
    assert accepted.state.active_trigger_event_ids == frozenset()
    assert set(accepted.state.event_identity_refs) == {"A", "B", "R1", "R2"}

    # A portable checkpoint proves that B was a stateful ownership input,
    # rather than a continuation-only in-memory shortcut.
    target = ReferenceSession(**kwargs)
    assert target._state_error(accepted.state) is None


@pytest.mark.parametrize("retain_active", (True, False), ids=("active-seed", "empty-active-seed"))
@pytest.mark.parametrize("resource_mode", ("ROUNDS", "BUDGET"))
@pytest.mark.parametrize("resume_fresh", (False, True), ids=("same", "fresh"))
def test_session_rejects_a_backfilled_ownership_request_without_rewriting_the_checkpoint(
    retain_active: bool,
    resource_mode: str,
    resume_fresh: bool,
) -> None:
    """A next delta cannot insert C before a retained terminal response."""

    binding, model, fixture = _runtime_parts()
    first_events = [
        {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
    ]
    if retain_active:
        first_events.append(
            {"id": "B", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        )
    first_events.append(
        {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    )
    second_events = [
        {"id": "C", "sequence": 3, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "R2", "sequence": 11, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="B" if retain_active else "A",
            response_id="R1",
            events=first_events,
            measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="C", response_id="R2", events=second_events, measurement=_interval_mapping(0, 0),
        ),
    )
    resources = ResourceState.rounds(4) if resource_mode == "ROUNDS" else ResourceState.budget(12)
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": f"global-order-{retain_active}-{resource_mode}-{resume_fresh}",
        "run_id": f"global-order-{retain_active}-{resource_mode}-{resume_fresh}",
        "initial_summary": "q0",
        "resources": resources,
        "retry_cap": 3,
        "interpretation_contract": _runtime_interpretation_contract(
            model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    }
    source = ReferenceSession(**kwargs)
    first = source.step(source.initial_state, environment)
    assert first.state.evidence[-1].committed is True
    assert first.state.active_trigger_event_ids == ({"A"} if retain_active else frozenset())

    if resume_fresh:
        fresh_binding, fresh_model, _fresh_fixture = _runtime_parts()
        target = ReferenceSession(
            binding=fresh_binding,
            model=fresh_model,
            session_id=kwargs["session_id"],
            run_id=kwargs["run_id"],
            initial_summary="q0",
            resources=ResourceState.rounds(4) if resource_mode == "ROUNDS" else ResourceState.budget(12),
            retry_cap=3,
            interpretation_contract=_runtime_interpretation_contract(
                fresh_model, policy="MOST-RECENT", concurrent_same_key=True,
            ),
        )
    else:
        target = source
    rejected = target.step(first.state, first.environment)
    evidence = rejected.state.evidence[-1]

    assert evidence.committed is False
    assert evidence.resolution_code == "OBSERVATION-INTERPRETATION-ERROR"
    assert evidence.observation_assessment is not None
    assert "INSUFFICIENT-OWNERSHIP-CONTEXT" in {
        diagnostic.code for diagnostic in evidence.observation_assessment.diagnostics
    }
    assert rejected.state.history.hypotheses == first.state.history.hypotheses
    assert rejected.state.event_identity_refs == first.state.event_identity_refs
    assert rejected.state.consumed_response_ids == first.state.consumed_response_ids
    assert rejected.state.terminal_trigger_event_ids == first.state.terminal_trigger_event_ids
    assert rejected.state.active_trigger_event_ids == first.state.active_trigger_event_ids
    assert rejected.state.attempts == first.state.attempts + 1
    assert rejected.state.context.q_status == "UNKNOWN"
    assert rejected.state.context.current_summary is None
    assert evidence.rejected_response == evidence.execution
    assert rejected.environment._state == "private-a2"
    charged = target._model.actions[evidence.snapshot.action_id].cost
    assert rejected.state.resources.remaining == first.state.resources.remaining - (
        1 if resource_mode == "ROUNDS" else charged
    )
    assert len(rejected.state.evidence) == 2

    independent_binding, independent_model, _independent_fixture = _runtime_parts()
    independent = ReferenceSession(
        binding=independent_binding,
        model=independent_model,
        session_id=kwargs["session_id"],
        run_id=kwargs["run_id"],
        initial_summary="q0",
        resources=ResourceState.rounds(4) if resource_mode == "ROUNDS" else ResourceState.budget(12),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            independent_model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    )
    assert independent._state_error(rejected.state) is None


@pytest.mark.parametrize(
    ("kind", "event_type", "response_id", "target_request_id"),
    (
        ("RESPONSE", "RESP", "late-response", None),
        ("CANCEL", "CANCEL", None, "A"),
        ("SUPERSEDE", "SUPERSEDE", None, "A"),
    ),
)
def test_session_rejects_a_backfilled_response_or_termination_without_poisoning_the_ledger(
    kind: str,
    event_type: str,
    response_id: str | None,
    target_request_id: str | None,
) -> None:
    """Response and termination kinds cannot bypass the retained global frontier."""

    binding, model, fixture = _runtime_parts()
    second_event: dict[str, object] = {
        "id": "late-event",
        "sequence": 9,
        "kind": kind,
        "key": "k",
        "eventType": event_type,
        "timestamp": 0,
    }
    if target_request_id is not None:
        second_event["targetRequestId"] = target_request_id
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="A",
            response_id="R1",
            events=[
                {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="A",
            response_id=response_id,
            events=[second_event],
            measurement=None if response_id is None else _interval_mapping(0, 0),
        ),
        second_no_response=response_id is None,
    )
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": f"global-order-{kind.lower()}-backfill",
        "run_id": f"global-order-{kind.lower()}-backfill",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(2),
        "retry_cap": 3,
        "interpretation_contract": _runtime_interpretation_contract(
            model, policy="FIFO", concurrent_same_key=True,
        ),
    }
    source = ReferenceSession(**kwargs)
    first = source.step(source.initial_state, environment)
    rejected = source.step(first.state, first.environment)
    evidence = rejected.state.evidence[-1]

    assert first.state.evidence[-1].committed is True
    assert evidence.committed is False
    assert evidence.resolution_code == "OBSERVATION-INTERPRETATION-ERROR"
    assert evidence.observation_assessment is not None
    assert {diagnostic.code for diagnostic in evidence.observation_assessment.diagnostics} >= {
        "INSUFFICIENT-OWNERSHIP-CONTEXT",
    }
    assert rejected.state.event_identity_refs == first.state.event_identity_refs
    assert rejected.state.consumed_response_ids == first.state.consumed_response_ids
    assert rejected.state.terminal_trigger_event_ids == first.state.terminal_trigger_event_ids
    assert rejected.state.active_trigger_event_ids == first.state.active_trigger_event_ids
    assert rejected.state.history.hypotheses == first.state.history.hypotheses
    assert rejected.state.attempts == first.state.attempts + 1
    assert rejected.state.resources.remaining == first.state.resources.remaining - 1
    fresh_binding, fresh_model, _fresh_fixture = _runtime_parts()
    fresh = ReferenceSession(
        binding=fresh_binding,
        model=fresh_model,
        session_id=kwargs["session_id"],
        run_id=kwargs["run_id"],
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            fresh_model, policy="FIFO", concurrent_same_key=True,
        ),
    )
    assert fresh._state_error(rejected.state) is None


def test_session_gives_a_backfilled_order_error_precedence_over_a_terminal_receipt_replay() -> None:
    """A mixed duplicate/backfill delta must not quarantine its new late facts."""

    binding, model, fixture = _runtime_parts()
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="A",
            response_id="R1",
            events=[
                {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="C",
            response_id="R2",
            events=[
                {"id": "C", "sequence": 3, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
                {"id": "R2", "sequence": 11, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="global-order-mixed-replay",
        run_id="global-order-mixed-replay",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    )
    first = session.step(session.initial_state, environment)
    rejected = session.step(first.state, first.environment)
    assessment = rejected.state.evidence[-1].observation_assessment

    assert assessment is not None
    assert {diagnostic.code for diagnostic in assessment.diagnostics} >= {
        "RETAINED-OWNERSHIP-EVENT-REPLAY",
        "INSUFFICIENT-OWNERSHIP-CONTEXT",
    }
    assert rejected.state.event_identity_refs == first.state.event_identity_refs
    assert "C" not in rejected.state.event_identity_refs
    assert "R2" not in rejected.state.event_identity_refs
    assert session._state_error(rejected.state) is None


@pytest.mark.parametrize("masked_unit", (False, True), ids=("order-only", "wrong-unit"))
def test_session_does_not_admit_an_order_invalid_raw_delta_from_a_rejected_s4_record(
    masked_unit: bool,
) -> None:
    """The malformed-record path uses the same boundary and NONE ledger mode."""

    binding, model, fixture = _runtime_parts()
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="A",
            response_id="R1",
            events=[
                {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="C",
            response_id="R2",
            events=[
                {"id": "C", "sequence": 3, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R2", "sequence": 11, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="global-order-bound-s4",
        run_id="global-order-bound-s4",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    )
    first = session.step(session.initial_state, environment)

    class MalformedRecordEnvironment:
        def __init__(self, delegate: SyntheticEnvironment) -> None:
            self.delegate = delegate

        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            returned = self.delegate.execute(request)
            material = returned.record.observation_input
            assert material is not None
            return EnvironmentExecution(
                replace(
                    returned.record,
                    effect_class="CONFIRMED-NOT-SENT",
                    observation_input=(
                        replace(material, unit="wrong-unit") if masked_unit else material
                    ),
                ),
                returned.successor,
            )

    rejected = session.step(first.state, MalformedRecordEnvironment(first.environment))
    evidence = rejected.state.evidence[-1]

    assert first.state.evidence[-1].committed is True
    assert evidence.committed is False
    assert evidence.resolution_code == "INVALID-EXECUTION-RECORD"
    assert evidence.observation_assessment is not None
    expected_codes = {"INSUFFICIENT-OWNERSHIP-CONTEXT"}
    if masked_unit:
        expected_codes.add("OBSERVATION-CLOCK-UNIT-MISMATCH")
    assert {diagnostic.code for diagnostic in evidence.observation_assessment.diagnostics} >= expected_codes
    assert rejected.state.history.hypotheses == first.state.history.hypotheses
    assert rejected.state.event_identity_refs == first.state.event_identity_refs
    assert rejected.state.consumed_response_ids == first.state.consumed_response_ids
    assert rejected.state.terminal_trigger_event_ids == first.state.terminal_trigger_event_ids
    assert rejected.state.active_trigger_event_ids == first.state.active_trigger_event_ids
    assert rejected.state.resources.remaining == first.state.resources.remaining - 1
    assert rejected.state.attempts == first.state.attempts + 1
    fresh_binding, fresh_model, _fresh_fixture = _runtime_parts()
    fresh = ReferenceSession(
        binding=fresh_binding,
        model=fresh_model,
        session_id="global-order-bound-s4",
        run_id="global-order-bound-s4",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            fresh_model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    )
    assert fresh._state_error(rejected.state) is None


@pytest.mark.parametrize(
    ("field", "invalid_value", "expected_code", "expected_resolution"),
    (
        ("clock_identity", "wrong-clock", "OBSERVATION-CLOCK-UNIT-MISMATCH", "OBSERVATION-INTERPRETATION-ERROR"),
        ("unit", "wrong-unit", "OBSERVATION-CLOCK-UNIT-MISMATCH", "OBSERVATION-INTERPRETATION-ERROR"),
        ("measurement_interval", None, "INVALID-MEASUREMENT-INTERVAL", "OBSERVATION-UNCERTAINTY-WINDOW-MISMATCH"),
    ),
)
@pytest.mark.parametrize("retain_active", (True, False), ids=("active-seed", "empty-active-seed"))
@pytest.mark.parametrize("resource_mode", ("ROUNDS", "BUDGET"))
@pytest.mark.parametrize("resume_fresh", (False, True), ids=("same", "fresh"))
def test_session_does_not_admit_an_order_invalid_delta_when_an_input_error_masks_it(
    field: str,
    invalid_value: object,
    expected_code: str,
    expected_resolution: str,
    retain_active: bool,
    resource_mode: str,
    resume_fresh: bool,
) -> None:
    """An outer input error cannot turn a rejected backfill into a ledger fact."""

    binding, model, fixture = _runtime_parts()
    first_events: list[dict[str, object]] = [
        {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
    ]
    if retain_active:
        first_events.append(
            {"id": "B", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        )
    first_events.append(
        {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    )
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="B" if retain_active else "A",
            response_id="R1",
            events=first_events,
            measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="C",
            response_id="R2",
            events=[
                {"id": "C", "sequence": 3, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R2", "sequence": 11, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )
    resources = ResourceState.rounds(4) if resource_mode == "ROUNDS" else ResourceState.budget(12)
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": f"global-order-masked-{field}-{retain_active}-{resource_mode}-{resume_fresh}",
        "run_id": f"global-order-masked-{field}-{retain_active}-{resource_mode}-{resume_fresh}",
        "initial_summary": "q0",
        "resources": resources,
        "retry_cap": 3,
        "interpretation_contract": _runtime_interpretation_contract(
            model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    }
    source = ReferenceSession(**kwargs)
    first = source.step(source.initial_state, environment)
    assert first.state.active_trigger_event_ids == ({"A"} if retain_active else frozenset())

    if resume_fresh:
        fresh_binding, fresh_model, _fresh_fixture = _runtime_parts()
        target = ReferenceSession(
            binding=fresh_binding,
            model=fresh_model,
            session_id=kwargs["session_id"],
            run_id=kwargs["run_id"],
            initial_summary="q0",
            resources=ResourceState.rounds(4) if resource_mode == "ROUNDS" else ResourceState.budget(12),
            retry_cap=3,
            interpretation_contract=_runtime_interpretation_contract(
                fresh_model, policy="MOST-RECENT", concurrent_same_key=True,
            ),
        )
    else:
        target = source

    class MaskedInputEnvironment:
        def __init__(self, delegate: SyntheticEnvironment) -> None:
            self.delegate = delegate

        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            returned = self.delegate.execute(request)
            material = returned.record.observation_input
            assert material is not None
            return EnvironmentExecution(
                replace(returned.record, observation_input=replace(material, **{field: invalid_value})),
                returned.successor,
            )

    rejected = target.step(first.state, MaskedInputEnvironment(first.environment))
    evidence = rejected.state.evidence[-1]

    assert evidence.committed is False
    assert evidence.resolution_code == expected_resolution
    assert evidence.observation_assessment is not None
    assert {diagnostic.code for diagnostic in evidence.observation_assessment.diagnostics} >= {
        expected_code,
        "INSUFFICIENT-OWNERSHIP-CONTEXT",
    }
    assert rejected.state.history.hypotheses == first.state.history.hypotheses
    assert rejected.state.event_identity_refs == first.state.event_identity_refs
    assert rejected.state.consumed_response_ids == first.state.consumed_response_ids
    assert rejected.state.terminal_trigger_event_ids == first.state.terminal_trigger_event_ids
    assert rejected.state.active_trigger_event_ids == first.state.active_trigger_event_ids
    charged = target._model.actions[evidence.snapshot.action_id].cost
    assert rejected.state.resources.remaining == first.state.resources.remaining - (
        1 if resource_mode == "ROUNDS" else charged
    )
    assert rejected.state.attempts == first.state.attempts + 1
    assert rejected.environment._state == "private-a2"
    fresh_binding, fresh_model, _fresh_fixture = _runtime_parts()
    fresh = ReferenceSession(
        binding=fresh_binding,
        model=fresh_model,
        session_id=kwargs["session_id"],
        run_id=kwargs["run_id"],
        initial_summary="q0",
        resources=ResourceState.rounds(4) if resource_mode == "ROUNDS" else ResourceState.budget(12),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            fresh_model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    )
    assert fresh._state_error(rejected.state) is None


@pytest.mark.parametrize(
    ("tail_sequence", "tail_kind", "tail_event_type"),
    (
        (12, "NOT-A-KIND", "INVALID"),
        (11, "REQUEST", "REQ"),
    ),
    ids=("invalid-kind", "duplicate-sequence"),
)
def test_session_does_not_admit_an_order_invalid_prefix_when_a_malformed_tail_follows(
    tail_sequence: int,
    tail_kind: str,
    tail_event_type: str,
) -> None:
    """The parsed valid prefix is still subject to the global order frontier."""

    binding, model, fixture = _runtime_parts()
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="A",
            response_id="R1",
            events=[
                {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="C",
            response_id="R2",
            events=[
                {"id": "C", "sequence": 3, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R2", "sequence": 11, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="global-order-malformed-tail",
        run_id="global-order-malformed-tail",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    )
    first = session.step(session.initial_state, environment)

    class MalformedTailEnvironment:
        def __init__(self, delegate: SyntheticEnvironment) -> None:
            self.delegate = delegate

        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            returned = self.delegate.execute(request)
            material = returned.record.observation_input
            assert material is not None
            malformed_tail = OwnershipEvent(
                "invalid-tail", tail_sequence, tail_kind, "k", tail_event_type, Fraction(0),
            )
            return EnvironmentExecution(
                replace(returned.record, observation_input=replace(
                    material, events=material.events + (malformed_tail,),
                )),
                returned.successor,
            )

    rejected = session.step(first.state, MalformedTailEnvironment(first.environment))
    evidence = rejected.state.evidence[-1]

    assert evidence.committed is False
    assert evidence.resolution_code == "OBSERVATION-INTERPRETATION-ERROR"
    assert evidence.observation_assessment is not None
    assert {diagnostic.code for diagnostic in evidence.observation_assessment.diagnostics} >= {
        "INVALID-OWNERSHIP-EVENT",
        "INSUFFICIENT-OWNERSHIP-CONTEXT",
    }
    assert rejected.state.history.hypotheses == first.state.history.hypotheses
    assert rejected.state.event_identity_refs == first.state.event_identity_refs
    assert rejected.state.consumed_response_ids == first.state.consumed_response_ids
    assert rejected.state.terminal_trigger_event_ids == first.state.terminal_trigger_event_ids
    assert rejected.state.active_trigger_event_ids == first.state.active_trigger_event_ids
    assert rejected.state.resources.remaining == first.state.resources.remaining - 1
    assert rejected.state.attempts == first.state.attempts + 1
    fresh_binding, fresh_model, _fresh_fixture = _runtime_parts()
    fresh = ReferenceSession(
        binding=fresh_binding,
        model=fresh_model,
        session_id="global-order-malformed-tail",
        run_id="global-order-malformed-tail",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            fresh_model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    )
    assert fresh._state_error(rejected.state) is None


def test_session_retains_a_order_forward_bound_delta_despite_a_clock_error() -> None:
    """An input ERROR is not by itself a reason to discard verified raw facts."""

    binding, model, fixture = _runtime_parts()
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="A",
            response_id="R1",
            events=[
                {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="C",
            response_id="R2",
            events=[
                {"id": "C", "sequence": 11, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R2", "sequence": 12, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="global-order-forward-clock-error",
        run_id="global-order-forward-clock-error",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    )
    first = session.step(session.initial_state, environment)

    class ForwardClockErrorEnvironment:
        def __init__(self, delegate: SyntheticEnvironment) -> None:
            self.delegate = delegate

        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            returned = self.delegate.execute(request)
            material = returned.record.observation_input
            assert material is not None
            return EnvironmentExecution(
                replace(returned.record, observation_input=replace(material, clock_identity="wrong-clock")),
                returned.successor,
            )

    rejected = session.step(first.state, ForwardClockErrorEnvironment(first.environment))
    assessment = rejected.state.evidence[-1].observation_assessment

    assert assessment is not None
    assert {diagnostic.code for diagnostic in assessment.diagnostics} >= {
        "OBSERVATION-CLOCK-UNIT-MISMATCH",
    }
    assert "INSUFFICIENT-OWNERSHIP-CONTEXT" not in {
        diagnostic.code for diagnostic in assessment.replay.diagnostics
    }
    assert set(rejected.state.event_identity_refs) == {"A", "C", "R1", "R2"}
    assert rejected.state.consumed_response_ids == {"R1", "R2"}
    assert rejected.state.terminal_trigger_event_ids == {"A", "C"}
    assert rejected.state.active_trigger_event_ids == frozenset()
    assert rejected.state.history.hypotheses == first.state.history.hypotheses
    assert session._state_error(rejected.state) is None


@pytest.mark.parametrize("wrong_clock", (False, True), ids=("ordinary-error", "clock-error"))
@pytest.mark.parametrize("retain_active", (False, True), ids=("empty-active-seed", "active-seed"))
@pytest.mark.parametrize("resource_mode", ("ROUNDS", "BUDGET"))
@pytest.mark.parametrize(
    ("bad_sequence", "bad_kind", "bad_event_type"),
    (
        (3, "RESPONSE", "RESP"),
        (12, "NOT-A-KIND", "INVALID"),
    ),
    ids=("nonincreasing-sequence", "invalid-kind"),
)
def test_session_does_not_consume_a_selected_response_explicitly_rejected_by_parser(
    wrong_clock: bool,
    retain_active: bool,
    resource_mode: str,
    bad_sequence: object,
    bad_kind: object,
    bad_event_type: object,
) -> None:
    """FULL S7 keeps a verified prefix but never seals its rejected R2."""

    binding, model, fixture = _runtime_parts()
    first_events: list[dict[str, object]] = [
        {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
    ]
    if retain_active:
        first_events.append(
            {"id": "B", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        )
    first_events.append(
        {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    )
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="B" if retain_active else "A",
            response_id="R1",
            events=first_events,
            measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="C",
            response_id="R2",
            events=[
                {"id": "C", "sequence": 11, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R2", "sequence": 12, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id=(
            f"explicit-rejected-response-{bad_sequence}-{bad_kind}-"
            f"{resource_mode}-{retain_active}-{wrong_clock}"
        ),
        run_id=(
            f"explicit-rejected-response-{bad_sequence}-{bad_kind}-"
            f"{resource_mode}-{retain_active}-{wrong_clock}"
        ),
        initial_summary="q0",
        resources=(ResourceState.rounds(4) if resource_mode == "ROUNDS" else ResourceState.budget(12)),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    )
    first = session.step(session.initial_state, environment)

    class ExplicitRejectedResponseEnvironment:
        def __init__(self, delegate: SyntheticEnvironment) -> None:
            self.delegate = delegate

        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            returned = self.delegate.execute(request)
            material = returned.record.observation_input
            assert material is not None
            assert len(material.events) == 2
            return EnvironmentExecution(
                replace(
                    returned.record,
                    observation_input=replace(
                        material,
                        events=(
                            material.events[0],
                            OwnershipEvent(
                                "R2", bad_sequence, bad_kind, "k", bad_event_type, Fraction(0),
                            ),
                        ),
                        clock_identity="wrong-clock" if wrong_clock else material.clock_identity,
                    ),
                ),
                returned.successor,
            )

    rejected = session.step(first.state, ExplicitRejectedResponseEnvironment(first.environment))
    evidence = rejected.state.evidence[-1]
    assessment = evidence.observation_assessment

    assert evidence.committed is False
    assert evidence.resolution_code == "OBSERVATION-INTERPRETATION-ERROR"
    assert assessment is not None and assessment.replay is not None
    assert assessment.replay.rejected_event_ids == {"R2"}
    assert {diagnostic.code for diagnostic in assessment.diagnostics} >= {"INVALID-OWNERSHIP-EVENT"}
    if wrong_clock:
        assert "OBSERVATION-CLOCK-UNIT-MISMATCH" in {
            diagnostic.code for diagnostic in assessment.diagnostics
        }
    assert set(rejected.state.event_identity_refs) == (
        {"A", "C", "R1"} if not retain_active else {"A", "B", "C", "R1"}
    )
    assert rejected.state.consumed_response_ids == {"R1"}
    assert rejected.state.terminal_trigger_event_ids == ({"A"} if not retain_active else {"B"})
    assert rejected.state.active_trigger_event_ids == ({"A"} if retain_active else frozenset())
    assert rejected.state.history.hypotheses == first.state.history.hypotheses
    charged = session._model.actions[evidence.snapshot.action_id].cost
    assert rejected.state.resources.remaining == first.state.resources.remaining - (
        1 if resource_mode == "ROUNDS" else charged
    )
    assert rejected.state.attempts == first.state.attempts + 1
    assert rejected.environment._state == "private-a2"
    assert session._state_error(rejected.state) is None
    fresh_binding, fresh_model, _fresh_fixture = _runtime_parts()
    fresh = ReferenceSession(
        binding=fresh_binding,
        model=fresh_model,
        session_id=session.initial_state.context.session_id,
        run_id=session.initial_state.context.run_id,
        initial_summary="q0",
        resources=(ResourceState.rounds(4) if resource_mode == "ROUNDS" else ResourceState.budget(12)),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            fresh_model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    )
    assert fresh._state_error(rejected.state) is None


def test_session_quarantine_does_not_consume_an_explicitly_rejected_selected_response() -> None:
    """QUARANTINE retains C but not an explicitly rejected selected R2."""

    binding, model, fixture = _runtime_parts()
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="A",
            response_id="R1",
            events=[
                {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="C",
            response_id="R2",
            events=[
                {"id": "R1", "sequence": 11, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "C", "sequence": 12, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R2", "sequence": 13, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="quarantine-explicit-rejected-response",
        run_id="quarantine-explicit-rejected-response",
        initial_summary="q0",
        resources=ResourceState.rounds(3),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    )
    first = session.step(session.initial_state, environment)
    assert first.state.consumed_response_ids == {"R1"}
    assert first.state.terminal_trigger_event_ids == {"A"}

    class ConflictingAndRejectedResponseEnvironment:
        def __init__(self, delegate: SyntheticEnvironment) -> None:
            self.delegate = delegate

        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            returned = self.delegate.execute(request)
            material = returned.record.observation_input
            assert material is not None
            return EnvironmentExecution(
                replace(
                    returned.record,
                    observation_input=replace(
                        material,
                        events=(
                            OwnershipEvent("R1", 11, "REQUEST", "k", "REQ", Fraction(0)),
                            OwnershipEvent("C", 12, "REQUEST", "k", "REQ", Fraction(0)),
                            OwnershipEvent("R2", 3, "RESPONSE", "k", "RESP", Fraction(0)),
                        ),
                    ),
                ),
                returned.successor,
            )

    rejected = session.step(first.state, ConflictingAndRejectedResponseEnvironment(first.environment))
    evidence = rejected.state.evidence[-1]
    assessment = evidence.observation_assessment

    assert evidence.committed is False
    assert evidence.resolution_code == "OBSERVATION-EVENT-IDENTITY-CONFLICT"
    assert assessment is not None and assessment.replay is not None
    assert assessment.replay.rejected_event_ids == {"R2"}
    assert "INVALID-OWNERSHIP-EVENT" in {diagnostic.code for diagnostic in assessment.diagnostics}
    # R1 keeps its old response role, C is a distinct forward fact the
    # quarantine retains, and rejected R2 stays out of every formal ledger
    # role.  C's retention proves this is QUARANTINE rather than NONE.
    assert set(rejected.state.event_identity_refs) == {"A", "C", "R1"}
    assert rejected.state.consumed_response_ids == {"R1"}
    assert rejected.state.terminal_trigger_event_ids == {"A"}
    assert rejected.state.active_trigger_event_ids == frozenset()
    assert session._state_error(rejected.state) is None


def test_session_rejected_s4_record_does_not_consume_an_explicitly_rejected_response() -> None:
    """The safely bound malformed-record path uses the same sparse gate."""

    binding, model, fixture = _runtime_parts()
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="A",
            response_id="R1",
            events=[
                {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="C",
            response_id="R2",
            events=[
                {"id": "C", "sequence": 11, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R2", "sequence": 12, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="s4-explicit-rejected-response",
        run_id="s4-explicit-rejected-response",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    )
    first = session.step(session.initial_state, environment)

    class RejectedRecordWithRejectedResponseEnvironment:
        def __init__(self, delegate: SyntheticEnvironment) -> None:
            self.delegate = delegate

        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            returned = self.delegate.execute(request)
            material = returned.record.observation_input
            assert material is not None
            return EnvironmentExecution(
                replace(
                    returned.record,
                    effect_class="CONFIRMED-NOT-SENT",
                    observation_input=replace(
                        material,
                        events=(
                            material.events[0],
                            OwnershipEvent("R2", 3, "RESPONSE", "k", "RESP", Fraction(0)),
                        ),
                    ),
                ),
                returned.successor,
            )

    rejected = session.step(
        first.state,
        RejectedRecordWithRejectedResponseEnvironment(first.environment),
    )
    assessment = rejected.state.evidence[-1].observation_assessment

    assert rejected.state.evidence[-1].resolution_code == "INVALID-EXECUTION-RECORD"
    assert assessment is not None and assessment.replay is not None
    assert assessment.replay.rejected_event_ids == {"R2"}
    assert set(rejected.state.event_identity_refs) == {"A", "C", "R1"}
    assert rejected.state.consumed_response_ids == {"R1"}
    assert rejected.state.terminal_trigger_event_ids == {"A"}
    assert rejected.state.active_trigger_event_ids == frozenset()
    assert session._state_error(rejected.state) is None


@pytest.mark.parametrize("resource_mode", ("ROUNDS", "BUDGET"))
@pytest.mark.parametrize("response_sequence", (3, 12), ids=("order-invalid", "order-valid"))
@pytest.mark.parametrize("carrier_kind", ("list", "empty-tuple", "tuple-subclass"))
@pytest.mark.parametrize(
    "returned_effect",
    ("NONE", "CONFIRMED-NOT-SENT"),
    ids=("ordinary-record", "malformed-non-send-record"),
)
def test_session_rejects_unparseable_event_carrier_without_creating_a_sparse_receipt(
    resource_mode: str,
    response_sequence: int,
    carrier_kind: str,
    returned_effect: str,
) -> None:
    """Only a nonempty exact tuple can establish that selected R2 was absent."""

    binding, model, fixture = _runtime_parts()
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="A",
            response_id="R1",
            events=[
                {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="C",
            response_id="R2",
            events=[
                {"id": "C", "sequence": 11, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R2", "sequence": 12, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )
    initial_resources = (
        ResourceState.rounds(4) if resource_mode == "ROUNDS" else ResourceState.budget(12)
    )
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id=(
            f"carrier-{carrier_kind}-{resource_mode}-{response_sequence}-{returned_effect}"
        ),
        run_id=(
            f"carrier-{carrier_kind}-{resource_mode}-{response_sequence}-{returned_effect}"
        ),
        initial_summary="q0",
        resources=initial_resources,
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    )
    first = session.step(session.initial_state, environment)

    class UnsupportedCarrierEnvironment:
        def __init__(self, delegate: SyntheticEnvironment) -> None:
            self.delegate = delegate

        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            returned = self.delegate.execute(request)
            material = returned.record.observation_input
            assert material is not None and len(material.events) == 2
            if carrier_kind == "list":
                events: object = [
                    material.events[0],
                    replace(material.events[1], sequence=response_sequence),
                ]
            elif carrier_kind == "empty-tuple":
                events = ()
            else:
                class TupleSubclass(tuple):
                    pass

                events = TupleSubclass((
                    material.events[0],
                    replace(material.events[1], sequence=response_sequence),
                ))
            malformed_material = replace(
                material,
                events=events,
            )
            return EnvironmentExecution(
                replace(
                    returned.record,
                    effect_class=returned_effect,
                    observation_input=malformed_material,
                ),
                returned.successor,
            )

    rejected = session.step(first.state, UnsupportedCarrierEnvironment(first.environment))
    evidence = rejected.state.evidence[-1]

    assert evidence.committed is False
    assert evidence.resolution_code == "INVALID-OBSERVATION-EVENT-CARRIER"
    assert evidence.execution.effect_class == "UNKNOWN-EFFECT"
    assert evidence.observation_assessment is None
    # An unparseable outer carrier is normalized away after its issued charge.
    # It is not retained as a replayable trace/audit object which could later
    # be substituted for another malformed payload.
    assert evidence.rejected_response is None
    assert set(rejected.state.event_identity_refs) == {"A", "R1"}
    assert rejected.state.consumed_response_ids == {"R1"}
    assert rejected.state.terminal_trigger_event_ids == {"A"}
    assert rejected.state.active_trigger_event_ids == frozenset()
    assert rejected.state.history.hypotheses == first.state.history.hypotheses
    assert rejected.state.history.compatible_state_by_hypothesis == first.state.history.compatible_state_by_hypothesis
    assert set(rejected.state.history.status_by_hypothesis.values()) == {"CONSERVATIVE-UNKNOWN"}
    assert rejected.state.context.q_status == "UNKNOWN"
    assert rejected.state.context.current_summary is None
    charge = session._model.actions[evidence.snapshot.action_id].cost
    assert rejected.state.resources.remaining == first.state.resources.remaining - (
        1 if resource_mode == "ROUNDS" else charge
    )
    assert rejected.state.attempts == first.state.attempts + 1
    assert rejected.environment._state == "private-a2"
    assert session._state_error(rejected.state) is None

    fresh_binding, fresh_model, _fresh_fixture = _runtime_parts()
    fresh = ReferenceSession(
        binding=fresh_binding,
        model=fresh_model,
        session_id=session.initial_state.context.session_id,
        run_id=session.initial_state.context.run_id,
        initial_summary="q0",
        resources=initial_resources,
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            fresh_model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    )
    assert fresh._state_error(rejected.state) is None

    # A non-null interpretation result, or any newly inserted raw record,
    # would recreate the old unsafe evidence path.  An independently replaying
    # coordinator must refuse it before a third dispatch or charge.
    forged_assessment = assess_observation(
        first.state.evidence[-1].execution.observation_input,
        fresh._interpretation_contract,
    )
    forged_assessment_state = replace(
        rejected.state,
        evidence=rejected.state.evidence[:-1] + (
            replace(evidence, observation_assessment=forged_assessment),
        ),
    )
    assert fresh._state_error(forged_assessment_state).code == "EVIDENCE-ERROR-MISMATCH"

    forged_record_state = replace(
        rejected.state,
        evidence=rejected.state.evidence[:-1] + (
            replace(evidence, rejected_response=first.state.evidence[-1].execution),
        ),
    )
    assert fresh._state_error(forged_record_state).code == "EVIDENCE-ERROR-MISMATCH"

    class NoDispatch:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:  # pragma: no cover - must not run
            raise AssertionError(f"forged list-carrier evidence reached dispatch: {request}")

    blocked = fresh.step(forged_assessment_state, NoDispatch())  # type: ignore[arg-type]
    assert blocked.stop_reason == "Stop-Error"
    assert blocked.state is forged_assessment_state
    assert blocked.state.resources == forged_assessment_state.resources
    assert blocked.diagnostics[0].code == "EVIDENCE-ERROR-MISMATCH"

    # The genuine checkpoint itself can still be admitted by a fresh session.
    resumed = fresh.step(rejected.state, rejected.environment)
    assert not any(diagnostic.code.startswith("EVIDENCE-") for diagnostic in resumed.diagnostics)
    assert resumed.state.resources == rejected.state.resources
    assert resumed.state.evidence == rejected.state.evidence


def test_session_rejects_list_carrier_before_quarantine_can_admit_any_delta() -> None:
    """An illegal outer carrier cannot use the tuple QUARANTINE exception."""

    binding, model, fixture = _runtime_parts()
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="A",
            response_id="R1",
            events=[
                {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="C",
            response_id="R2",
            events=[
                {"id": "C", "sequence": 11, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R2", "sequence": 12, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="list-carrier-before-quarantine",
        run_id="list-carrier-before-quarantine",
        initial_summary="q0",
        resources=ResourceState.rounds(3),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    )
    first = session.step(session.initial_state, environment)

    class ListConflictEnvironment:
        def __init__(self, delegate: SyntheticEnvironment) -> None:
            self.delegate = delegate

        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            returned = self.delegate.execute(request)
            material = returned.record.observation_input
            assert material is not None
            return EnvironmentExecution(
                replace(
                    returned.record,
                    observation_input=replace(
                        material,
                        events=[
                            OwnershipEvent("R1", 11, "REQUEST", "k", "REQ", Fraction(0)),
                            OwnershipEvent("C", 12, "REQUEST", "k", "REQ", Fraction(0)),
                            OwnershipEvent("R2", 3, "RESPONSE", "k", "RESP", Fraction(0)),
                        ],
                    ),
                ),
                returned.successor,
            )

    rejected = session.step(first.state, ListConflictEnvironment(first.environment))
    evidence = rejected.state.evidence[-1]

    assert evidence.resolution_code == "INVALID-OBSERVATION-EVENT-CARRIER"
    assert evidence.observation_assessment is None
    assert set(rejected.state.event_identity_refs) == {"A", "R1"}
    assert rejected.state.consumed_response_ids == {"R1"}
    assert rejected.state.terminal_trigger_event_ids == {"A"}
    assert rejected.state.active_trigger_event_ids == frozenset()
    assert session._state_error(rejected.state) is None


def test_session_replays_an_unparseable_carrier_without_granting_raw_provenance_authority() -> None:
    """A raw/visible mismatch stays audit-only when the outer carrier is invalid."""

    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="list-carrier-provenance-unavailable",
        run_id="list-carrier-provenance-unavailable",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    environment = _environment_with_observation_material(
        fixture,
        _runtime_observation_material(
            trigger_id="A",
            response_id="R1",
            events=[
                {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R1", "sequence": 2, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )

    class ProvenanceUnavailableListCarrier:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            returned = environment.execute(request)
            material = returned.record.observation_input
            assert material is not None
            # Deliberately preserve raw evidence_ref while changing the
            # visible reference.  This cannot form a provenance-backed
            # ownership fact, and the invalid outer list carrier prevents it
            # from being interpreted as one.
            return EnvironmentExecution(
                replace(
                    returned.record,
                    evidence_ref="visible-provenance-mismatch",
                    observation_input=replace(material, events=list(material.events)),
                ),
                returned.successor,
            )

    rejected = session.step(session.initial_state, ProvenanceUnavailableListCarrier())
    evidence = rejected.state.evidence[-1]

    assert evidence.resolution_code == "INVALID-OBSERVATION-EVENT-CARRIER"
    assert evidence.observation_assessment is None
    assert evidence.rejected_response is None
    assert rejected.state.event_identity_refs == {}
    assert rejected.state.consumed_response_ids == frozenset()
    assert session._state_error(rejected.state) is None

    fresh_binding, fresh_model, _fresh_fixture = _runtime_parts()
    fresh = ReferenceSession(
        binding=fresh_binding,
        model=fresh_model,
        session_id="list-carrier-provenance-unavailable",
        run_id="list-carrier-provenance-unavailable",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(fresh_model),
    )
    assert fresh._state_error(rejected.state) is None


def test_session_normalizes_a_cyclic_unparseable_event_carrier_without_recursing() -> None:
    """An adversarial cyclic list must take the same finite canonical S4 path."""

    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="cyclic-list-carrier",
        run_id="cyclic-list-carrier",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    environment = _environment_with_observation_material(
        fixture,
        _runtime_observation_material(
            trigger_id="A",
            response_id="R1",
            events=[
                {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R1", "sequence": 2, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )

    class CyclicListCarrier:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            returned = environment.execute(request)
            material = returned.record.observation_input
            assert material is not None
            cyclic_events: list[object] = []
            cyclic_events.append(cyclic_events)
            return EnvironmentExecution(
                replace(
                    returned.record,
                    observation_input=replace(material, events=cyclic_events),
                ),
                returned.successor,
            )

    rejected = session.step(session.initial_state, CyclicListCarrier())
    evidence = rejected.state.evidence[-1]

    assert evidence.resolution_code == "INVALID-OBSERVATION-EVENT-CARRIER"
    assert evidence.rejected_response is None
    assert evidence.observation_assessment is None
    assert rejected.state.event_identity_refs == {}
    assert rejected.state.consumed_response_ids == frozenset()
    assert rejected.environment._state == "private-a1"
    assert session._state_error(rejected.state) is None

    fresh_binding, fresh_model, _fresh_fixture = _runtime_parts()
    fresh = ReferenceSession(
        binding=fresh_binding,
        model=fresh_model,
        session_id="cyclic-list-carrier",
        run_id="cyclic-list-carrier",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(fresh_model),
    )
    assert fresh._state_error(rejected.state) is None


def test_session_prioritizes_an_unparseable_carrier_over_compound_header_errors() -> None:
    """No adjacent S4 header fault may retain an invalid carrier as raw evidence."""

    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="compound-list-carrier",
        run_id="compound-list-carrier",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    environment = _environment_with_observation_material(
        fixture,
        _runtime_observation_material(
            trigger_id="A",
            response_id="R1",
            events=[
                {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R1", "sequence": 2, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )

    class CompoundInvalidCarrier:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            returned = environment.execute(request)
            material = returned.record.observation_input
            assert material is not None
            return EnvironmentExecution(
                replace(
                    returned.record,
                    evidence_ref="",
                    observation_input=replace(material, events=list(material.events)),
                ),
                returned.successor,
            )

    rejected = session.step(session.initial_state, CompoundInvalidCarrier())
    evidence = rejected.state.evidence[-1]

    assert evidence.resolution_code == "INVALID-OBSERVATION-EVENT-CARRIER"
    assert evidence.rejected_response is None
    assert evidence.observation_assessment is None
    assert rejected.state.event_identity_refs == {}
    assert rejected.state.resources.remaining == 1
    assert session._state_error(rejected.state) is None


def test_session_canonicalizes_a_foreign_unparseable_carrier_without_retaining_it() -> None:
    """Carrier rejection wins before a foreign raw record can enter evidence."""

    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="foreign-list-carrier",
        run_id="foreign-list-carrier",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    environment = _environment_with_observation_material(
        fixture,
        _runtime_observation_material(
            trigger_id="A",
            response_id="R1",
            events=[
                {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R1", "sequence": 2, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )

    class ForeignListCarrierEnvironment:
        returned_record: VisibleExecutionRecord | None = None

        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            returned = environment.execute(request)
            material = returned.record.observation_input
            assert material is not None
            foreign_record = replace(
                returned.record,
                execution_attempt_id="foreign-execution",
                action_id="foreign-action",
                evidence_ref="foreign-evidence",
                observation_input=replace(material, events=list(material.events)),
            )
            self.returned_record = foreign_record
            return EnvironmentExecution(
                foreign_record,
                returned.successor,
            )

    foreign_environment = ForeignListCarrierEnvironment()
    rejected = session.step(session.initial_state, foreign_environment)
    evidence = rejected.state.evidence[-1]

    assert evidence.resolution_code == "INVALID-OBSERVATION-EVENT-CARRIER"
    assert evidence.observation_assessment is None
    assert evidence.rejected_response is None
    assert set(rejected.state.event_identity_refs) == set()
    assert rejected.state.consumed_response_ids == frozenset()
    assert session._state_error(rejected.state) is None

    fresh_binding, fresh_model, _fresh_fixture = _runtime_parts()
    fresh = ReferenceSession(
        binding=fresh_binding,
        model=fresh_model,
        session_id="foreign-list-carrier",
        run_id="foreign-list-carrier",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(fresh_model),
    )
    assert fresh._state_error(rejected.state) is None

    # Coordinatedly relabeling the canonical carrier error as a foreign
    # identity error and restoring its raw list record must still fail before
    # a fresh session can issue or charge another action.
    foreign_record = foreign_environment.returned_record
    assert type(foreign_record) is VisibleExecutionRecord
    forged_context = replace(
        rejected.state.context,
        error_history=tuple(
            entry.replace(
                "INVALID-OBSERVATION-EVENT-CARRIER:",
                "EXECUTION-IDENTITY-ERROR:",
                1,
            )
            for entry in rejected.state.context.error_history
        ),
        unknown_history=tuple(
            entry.replace(
                "INVALID-OBSERVATION-EVENT-CARRIER:",
                "EXECUTION-IDENTITY-ERROR:",
                1,
            )
            for entry in rejected.state.context.unknown_history
        ),
    )
    forged_state = replace(
        rejected.state,
        context=forged_context,
        evidence=rejected.state.evidence[:-1] + (
            replace(
                evidence,
                resolution_code="EXECUTION-IDENTITY-ERROR",
                rejected_response=foreign_record,
            ),
        ),
    )
    assert fresh._state_error(forged_state).code == "EVIDENCE-ERROR-MISMATCH"

    class NoDispatch:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:  # pragma: no cover - must not run
            raise AssertionError(f"forged carrier checkpoint reached dispatch: {request}")

    blocked = fresh.step(forged_state, NoDispatch())  # type: ignore[arg-type]
    assert blocked.stop_reason == "Stop-Error"
    assert blocked.state is forged_state
    assert blocked.state.resources == forged_state.resources
    assert blocked.diagnostics[0].code == "EVIDENCE-ERROR-MISMATCH"


@pytest.mark.parametrize(
    ("resources", "expected_after_test", "expected_after_recover"),
    (
        (ResourceState.rounds(3), 2, 1),
        (ResourceState.budget(10), 9, 8),
    ),
    ids=("rounds", "budget"),
)
def test_session_rejects_a_coordinated_foreign_carrier_checkpoint_before_recover_dispatch(
    resources: ResourceState,
    expected_after_test: int,
    expected_after_recover: int,
) -> None:
    """A relabelled carrier error cannot enter the legal identity-error replay path.

    This is the C05 cross-boundary check: it keeps the live carrier priority
    reciprocal with state replay, including when the recovered checkpoint has
    a real, affordable Recover action.  The nearby exact-tuple identity error
    and canonical no-raw carrier checkpoint remain executable fresh-session
    controls rather than being blocked by an over-broad replay guard.
    """

    binding, base_model, fixture = _runtime_parts()

    def recovery_model(model: FiniteSessionModel) -> FiniteSessionModel:
        source = copy.deepcopy(fixture["algorithmModel"])
        assert isinstance(source, dict)
        raw_actions = source["actions"]
        assert isinstance(raw_actions, list)
        router = copy.deepcopy(next(item for item in raw_actions if item["id"] == "test-router"))
        recover = copy.deepcopy(router)
        recover.update({
            "id": "recover-q",
            "kind": "RECOVER",
            "declaredTarget": "recovered-q1",
            "recoverWhenUnknown": True,
            "detailCharges": {
                "acquisition": 0,
                "computation": 0,
                "preparation": 0,
                "recovery": 1,
                "retry": 0,
            },
        })
        transition = recover["transition"]
        assert isinstance(transition, dict)
        transition["id"] = "tr-recover-q"
        source["actions"] = [router, recover]
        limits = source["limits"]
        assert isinstance(limits, dict)
        limits["actions"] = 2
        return FiniteSessionModel.from_mapping(context=model.context, value=source)

    def recovery_environment() -> SyntheticEnvironment:
        source = copy.deepcopy(fixture["environments"]["alpha"])
        assert isinstance(source, dict)
        states = source["states"]
        assert isinstance(states, dict)
        first = states["private-a0"]
        assert isinstance(first, dict)
        router = first["test-router"]
        assert isinstance(router, dict)
        router["observationMaterial"] = _runtime_observation_material(
            trigger_id="A",
            response_id="R1",
            events=[
                {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R1", "sequence": 2, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        )
        second = states["private-a1"]
        assert isinstance(second, dict)
        second["recover-q"] = {
            "effectClass": "NONE",
            "observable": None,
            "summaryConfirmed": True,
            "postSummary": "q1",
            "measurementTick": None,
            "nextPrivateState": "private-a2",
            "prepRecover": {
                "targetConfirmed": True,
                "summaryConfirmed": True,
                "prepError": False,
                "ineligible": False,
                "declaredTarget": "recovered-q1",
                "evidence": "synthetic:carrier-replay:recover",
                "postSummary": "q1",
            },
        }
        return SyntheticEnvironment.from_mapping(source)

    def make_session(
        authority: RuntimeAuthorityBinding,
        model: FiniteSessionModel,
    ) -> ReferenceSession:
        return ReferenceSession(
            binding=authority,
            model=model,
            session_id=f"carrier-replay-{resources.mode.lower()}",
            run_id=f"carrier-replay-{resources.mode.lower()}",
            initial_summary="q0",
            resources=resources,
            retry_cap=3,
            interpretation_contract=_runtime_interpretation_contract(model),
        )

    class ForeignCarrierEnvironment:
        def __init__(self, delegate: SyntheticEnvironment, *, outer_events: object) -> None:
            self.delegate = delegate
            self.outer_events = outer_events
            self.calls = 0
            self.returned_record: VisibleExecutionRecord | None = None
            self.returned_successor: SyntheticEnvironment | None = None

        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            self.calls += 1
            returned = self.delegate.execute(request)
            material = returned.record.observation_input
            assert material is not None
            events = self.outer_events
            if events == "LIST":
                events = list(material.events)
            elif events == "TUPLE":
                events = material.events
            foreign_record = replace(
                returned.record,
                execution_attempt_id="foreign-execution",
                action_id="foreign-action",
                evidence_ref="foreign-evidence",
                observation_input=replace(material, events=events),
            )
            self.returned_record = foreign_record
            self.returned_successor = returned.successor
            return EnvironmentExecution(foreign_record, returned.successor)

    model = recovery_model(base_model)
    live = make_session(binding, model)
    list_environment = ForeignCarrierEnvironment(recovery_environment(), outer_events="LIST")
    canonical = live.step(live.initial_state, list_environment)  # type: ignore[arg-type]
    carrier_evidence = canonical.state.evidence[-1]

    # D01: both resource modes reach the canonical, charged carrier branch
    # while preserving the actual successor and without admitting raw facts.
    assert list_environment.calls == 1
    assert carrier_evidence.resolution_code == "INVALID-OBSERVATION-EVENT-CARRIER"
    assert carrier_evidence.rejected_response is None
    assert carrier_evidence.observation_assessment is None
    assert canonical.environment is list_environment.returned_successor
    assert canonical.state.resources.remaining == expected_after_test
    assert canonical.state.attempts == 1
    assert canonical.state.context.q_status == "UNKNOWN"
    assert live._state_error(canonical.state) is None

    fresh_binding, fresh_base_model, _fresh_fixture = _runtime_parts()
    fresh_model = recovery_model(fresh_base_model)

    # D05: the genuine no-raw carrier checkpoint is still replayable by an
    # independent coordinator and reaches its declared, charged Recover.
    genuine = make_session(fresh_binding, fresh_model)
    assert genuine._state_error(canonical.state) is None
    genuine_recover = genuine.step(canonical.state, canonical.environment)
    assert genuine_recover.stop_reason is None
    assert genuine_recover.state.evidence[-1].snapshot.action_id == "recover-q"
    assert genuine_recover.state.evidence[-1].resolution_code == "COMMIT"
    assert genuine_recover.state.context.q_status == "KNOWN"
    assert genuine_recover.state.context.current_summary == "q1"
    assert genuine_recover.state.resources.remaining == expected_after_recover
    assert genuine_recover.state.attempts == 2

    foreign_record = list_environment.returned_record
    assert type(foreign_record) is VisibleExecutionRecord
    assert type(foreign_record.observation_input) is ObservationInput
    assert type(foreign_record.observation_input.events) is list
    assert any(
        entry.startswith("INVALID-OBSERVATION-EVENT-CARRIER:")
        for entry in canonical.state.context.error_history
    )
    assert any(
        entry.startswith("INVALID-OBSERVATION-EVENT-CARRIER:")
        for entry in canonical.state.context.unknown_history
    )
    forged_context = replace(
        canonical.state.context,
        error_history=tuple(
            entry.replace(
                "INVALID-OBSERVATION-EVENT-CARRIER:",
                "EXECUTION-IDENTITY-ERROR:",
                1,
            )
            for entry in canonical.state.context.error_history
        ),
        unknown_history=tuple(
            entry.replace(
                "INVALID-OBSERVATION-EVENT-CARRIER:",
                "EXECUTION-IDENTITY-ERROR:",
                1,
            )
            for entry in canonical.state.context.unknown_history
        ),
    )
    assert forged_context.error_history != canonical.state.context.error_history
    assert forged_context.unknown_history != canonical.state.context.unknown_history
    assert all(
        not entry.startswith("INVALID-OBSERVATION-EVENT-CARRIER:")
        for entry in forged_context.error_history + forged_context.unknown_history
    )
    assert any(
        entry.startswith("EXECUTION-IDENTITY-ERROR:")
        for entry in forged_context.error_history
    )
    assert any(
        entry.startswith("EXECUTION-IDENTITY-ERROR:")
        for entry in forged_context.unknown_history
    )
    forged = replace(
        canonical.state,
        context=forged_context,
        evidence=canonical.state.evidence[:-1] + (
            replace(
                carrier_evidence,
                resolution_code="EXECUTION-IDENTITY-ERROR",
                rejected_response=foreign_record,
            ),
        ),
    )
    assert forged.evidence[-1].resolution_code == "EXECUTION-IDENTITY-ERROR"
    assert forged.evidence[-1].rejected_response is foreign_record

    # D02/D03: all four coordinated fields are changed.  Both a same-model
    # verifier and a genuinely fresh coordinator reject before the otherwise
    # affordable Recover can be issued or charged.
    same_error = live._state_error(forged)
    fresh_for_forgery = make_session(fresh_binding, fresh_model)
    fresh_error = fresh_for_forgery._state_error(forged)
    assert same_error is not None and same_error.code == "EVIDENCE-ERROR-MISMATCH"
    assert fresh_error is not None and fresh_error.code == "EVIDENCE-ERROR-MISMATCH"

    class NoDispatch:
        calls = 0

        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:  # pragma: no cover - must not run
            self.calls += 1
            raise AssertionError(f"coordinated carrier forgery reached Recover dispatch: {request}")

    no_dispatch = NoDispatch()
    blocked = fresh_for_forgery.step(forged, no_dispatch)  # type: ignore[arg-type]
    assert no_dispatch.calls == 0
    assert blocked.stop_reason == "Stop-Error"
    assert blocked.state is forged
    assert blocked.environment is no_dispatch
    assert blocked.state.resources == forged.resources
    assert blocked.state.attempts == forged.attempts
    assert blocked.state.evidence == forged.evidence
    assert blocked.state.context == forged.context
    assert blocked.diagnostics[0].code == "EVIDENCE-ERROR-MISMATCH"

    # D04: an actually foreign but fully parseable tuple remains the legal
    # identity-error witness and may be replayed through the same Recover.
    legal_live = make_session(binding, model)
    tuple_environment = ForeignCarrierEnvironment(recovery_environment(), outer_events="TUPLE")
    legal = legal_live.step(legal_live.initial_state, tuple_environment)  # type: ignore[arg-type]
    legal_evidence = legal.state.evidence[-1]
    assert legal_evidence.resolution_code == "EXECUTION-IDENTITY-ERROR"
    assert type(legal_evidence.rejected_response) is VisibleExecutionRecord
    assert type(legal_evidence.rejected_response.observation_input) is ObservationInput
    assert type(legal_evidence.rejected_response.observation_input.events) is tuple
    legal_fresh = make_session(fresh_binding, fresh_model)
    assert legal_fresh._state_error(legal.state) is None
    legal_recover = legal_fresh.step(legal.state, legal.environment)
    assert legal_recover.stop_reason is None
    assert legal_recover.state.evidence[-1].snapshot.action_id == "recover-q"
    assert legal_recover.state.evidence[-1].resolution_code == "COMMIT"
    assert legal_recover.state.context.q_status == "KNOWN"
    assert legal_recover.state.resources.remaining == expected_after_recover
    assert legal_recover.state.attempts == 2


def test_session_keeps_a_genuine_sparse_response_when_an_unrelated_raw_event_is_rejected() -> None:
    """Parser provenance fences its own ID, not every sparse receipt."""

    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="sparse-response-unrelated-rejection",
        run_id="sparse-response-unrelated-rejection",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    result = session.step(
        session.initial_state,
        _environment_with_observation_material(
            fixture,
            _runtime_observation_material(
                trigger_id="A",
                response_id="X",
                events=[
                    {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                    {"id": "Z", "sequence": 2, "kind": "NOT-A-KIND", "key": "k", "eventType": "RESP", "timestamp": 0},
                ],
                measurement=_interval_mapping(0, 0),
            ),
        ),
    )
    assessment = result.state.evidence[0].observation_assessment

    assert assessment is not None and assessment.replay is not None
    assert assessment.replay.rejected_event_ids == {"Z"}
    assert result.state.consumed_response_ids == {"X"}
    assert set(result.state.event_identity_refs) == {"A"}
    assert "Z" not in result.state.event_identity_refs
    assert session._state_error(result.state) is None


@pytest.mark.parametrize(
    ("policy", "expected_status", "expected_owner"),
    (("FIFO", "UNIQUE", "A"), ("MOST-RECENT", "UNIQUE", "C"), ("UNIQUE-KEY", "AMBIGUOUS", None)),
)
def test_incremental_global_forward_request_preserves_the_declared_ownership_policy(
    policy: str,
    expected_status: str,
    expected_owner: str | None,
) -> None:
    """A high-water boundary changes no legal FIFO/MR/UNIQUE decision."""

    from cltav_runtime.interpretation import OwnershipEvent, OwnershipOrderBoundary, replay_ownership

    active_a = OwnershipEvent("A", 1, "REQUEST", "k", "REQ", Fraction(0))
    replay = replay_ownership(
        (
            OwnershipEvent("C", 11, "REQUEST", "k", "REQ", Fraction(0)),
            OwnershipEvent("R2", 12, "RESPONSE", "k", "RESP", Fraction(0)),
        ),
        _runtime_interpretation_contract(
            _runtime_parts()[1], policy=policy, concurrent_same_key=True,
        ),
        prior_active_requests={"A": active_a},
        prior_order_boundary=OwnershipOrderBoundary(10, Fraction(0), frozenset({"A", "R1"})),
    )

    resolution = replay.response_resolutions["R2"]
    assert replay.diagnostics == ()
    assert resolution.status == expected_status
    assert resolution.owner_request_id == expected_owner


def test_session_rebuilds_the_order_frontier_from_evidence_not_a_mutable_ledger() -> None:
    """Removing retained event refs cannot re-open a processed ownership prefix."""

    binding, model, fixture = _runtime_parts()
    first_material = _runtime_observation_material(
        trigger_id="A",
        response_id="R1",
        events=[
            {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
            {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
        ],
        measurement=_interval_mapping(0, 0),
    )
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="global-order-ledger-tamper",
        run_id="global-order-ledger-tamper",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    )
    first = session.step(
        session.initial_state,
        _two_round_observation_environment(fixture, first_material, first_material),
    )
    assert first.state.evidence[-1].committed is True
    forged = replace(first.state, event_identity_refs=MappingProxyType({}))
    state_error = session._state_error(forged)
    assert state_error is not None
    assert state_error.code == "INVALID-OBSERVATION-EVENT-LEDGER"

    class NoDispatch:
        def execute(self, _request: ExecutionRequest) -> EnvironmentExecution:  # pragma: no cover - must not run
            raise AssertionError("a forged ownership frontier must be rejected before dispatch")

    rejected = session.step(forged, NoDispatch())  # type: ignore[arg-type]
    assert rejected.stop_reason == "Stop-Error"
    assert rejected.state is forged
    assert rejected.diagnostics[0].code == "INVALID-OBSERVATION-EVENT-LEDGER"


def test_session_does_not_let_an_unrelated_key_advance_the_ownership_frontier() -> None:
    """Other-key transactions stay in the identity ledger but do not fence this contract."""

    binding, model, fixture = _runtime_parts()
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="A",
            response_id="R1",
            events=[
                {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
                {"id": "other-request", "sequence": 100, "kind": "REQUEST", "key": "other", "eventType": "OTHER", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="C",
            response_id="R2",
            events=[
                {"id": "C", "sequence": 11, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "R2", "sequence": 12, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="global-order-foreign-key",
        run_id="global-order-foreign-key",
        initial_summary="q0",
        resources=ResourceState.rounds(3),
        retry_cap=3,
        interpretation_contract=_runtime_interpretation_contract(
            model, policy="MOST-RECENT", concurrent_same_key=True,
        ),
    )
    first = session.step(session.initial_state, environment)
    second = session.step(first.state, first.environment)

    assert first.state.evidence[-1].committed is True
    assert second.state.evidence[-1].committed is True
    assessment = second.state.evidence[-1].observation_assessment
    assert assessment is not None
    assert assessment.response_id == "R2"
    assert assessment.ownership is not None
    assert assessment.ownership.owner_request_id == "C"
    assert session._state_error(second.state) is None


def test_session_rejects_an_incremental_fifo_delta_when_it_selects_a_newer_request_over_retained_b() -> None:
    """Omitting B from raw material cannot make C own the next FIFO response."""

    binding, model, fixture = _runtime_parts()
    first_events = [
        {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "B", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "R1", "sequence": 3, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    # C is causally later than B, but FIFO still assigns R2 to retained B.
    # Naming C as the selected trigger must therefore enter the normal S7
    # interpretation-error path, not commit a singleton result for C.
    second_events = [
        {"id": "C", "sequence": 4, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "R2", "sequence": 5, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="A", response_id="R1", events=first_events, measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="C", response_id="R2", events=second_events, measurement=_interval_mapping(0, 0),
        ),
    )
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": "retained-fifo-owner",
        "run_id": "retained-fifo-owner",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(2),
        "retry_cap": 2,
        "interpretation_contract": _runtime_interpretation_contract(
            model, policy="FIFO", concurrent_same_key=True,
        ),
    }
    source = ReferenceSession(**kwargs)
    first = source.step(source.initial_state, environment)
    rejected = source.step(first.state, first.environment)

    assert rejected.state.evidence[-1].committed is False
    assert rejected.state.evidence[-1].resolution_code == "OBSERVATION-INTERPRETATION-ERROR"
    assert rejected.state.history.hypotheses == first.state.history.hypotheses
    assert rejected.state.terminal_trigger_event_ids == {"A", "B"}
    assert rejected.state.active_trigger_event_ids == {"C"}
    assert rejected.state.consumed_response_ids == {"R1", "R2"}


def test_session_replays_a_delta_only_cancellation_against_its_retained_active_ledger() -> None:
    """A portable active ledger makes B available to the next raw ownership delta."""

    binding, model, fixture = _runtime_parts()
    first_events = [
        {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "B", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "R1", "sequence": 10, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    cancellation_delta = [
        {"id": "T", "sequence": 11, "kind": "CANCEL", "key": "k", "eventType": "CANCEL", "timestamp": 1, "targetRequestId": "B"},
    ]
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="A", response_id="R1", events=first_events, measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="B", response_id=None, events=cancellation_delta, earliest=6,
        ),
        second_no_response=True,
    )
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": "incremental-timely-cancellation",
        "run_id": "incremental-timely-cancellation",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(2),
        "retry_cap": 2,
        "interpretation_contract": _runtime_interpretation_contract(
            model,
            policy="FIFO",
            concurrent_same_key=True,
        ),
    }
    source = ReferenceSession(**kwargs)
    first = source.step(source.initial_state, environment)
    assert first.state.active_trigger_event_ids == {"B"}

    cancelled = source.step(first.state, first.environment)
    assessment = cancelled.state.evidence[-1].observation_assessment
    assert cancelled.state.evidence[-1].resolution_code == "OBSERVATION-NO-RESPONSE"
    assert assessment is not None
    assert assessment.verdict == "INCONCLUSIVE"
    assert assessment.score_disposition == "NOT-APPLICABLE"
    assert assessment.diagnostics == ()
    assert cancelled.state.terminal_trigger_event_ids == {"A", "B"}
    assert cancelled.state.active_trigger_event_ids == frozenset()

    # The delta-only cancellation must survive a fresh session checkpoint,
    # proving that the retained trigger was part of the explicit state input.
    target = ReferenceSession(**kwargs)
    assert target._state_error(cancelled.state) is None


def test_session_quarantines_a_nonconcurrent_replacement_that_targets_a_stale_request() -> None:
    """A stale supersession target cannot admit a third non-concurrent request."""

    binding, model, fixture = _runtime_parts()
    events = [
        {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "B", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0, "targetRequestId": "A"},
        # A is already superseded by B.  C must not use that stale target to
        # bypass the non-concurrent obligation invariant.
        {"id": "C", "sequence": 3, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0, "targetRequestId": "A"},
        {"id": "R", "sequence": 4, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": "stale-replacement-target",
        "run_id": "stale-replacement-target",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(1),
        "interpretation_contract": _runtime_interpretation_contract(model),
    }
    source = ReferenceSession(**kwargs)
    result = source.step(
        source.initial_state,
        _environment_with_observation_material(
            fixture,
            _runtime_observation_material(
                trigger_id="C", response_id="R", events=events, measurement=_interval_mapping(0, 0),
            ),
        ),
    )

    evidence = result.state.evidence[-1]
    assert evidence.committed is False
    assert evidence.resolution_code == "OBSERVATION-INTERPRETATION-ERROR"
    assert evidence.observation_assessment is not None
    assert "INVALID-OWNERSHIP-TERMINATION" in {
        diagnostic.code for diagnostic in evidence.observation_assessment.diagnostics
    }
    # S7 still emits a portable, self-validating ledger rather than a partial
    # normal history commit.
    target = ReferenceSession(**kwargs)
    assert target._state_error(result.state) is None


@pytest.mark.parametrize(
    ("termination_kind", "termination_type"),
    (("CANCEL", "CANCEL"), ("SUPERSEDE", "SUPERSEDE")),
)
def test_session_ignores_a_complete_foreign_termination_transaction(
    termination_kind: str,
    termination_type: str,
) -> None:
    """A closed other-key transaction cannot pollute the selected contract."""

    binding, model, fixture = _runtime_parts()
    events = [
        {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "X", "sequence": 2, "kind": "REQUEST", "key": "other", "eventType": "REQ", "timestamp": 0},
        {"id": "T", "sequence": 3, "kind": termination_kind, "key": "other", "eventType": termination_type, "timestamp": 0, "targetRequestId": "X"},
        {"id": "R", "sequence": 4, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": f"foreign-{termination_kind.lower()}",
        "run_id": f"foreign-{termination_kind.lower()}",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(1),
        "interpretation_contract": _runtime_interpretation_contract(model),
    }
    source = ReferenceSession(**kwargs)
    result = source.step(
        source.initial_state,
        _environment_with_observation_material(
            fixture,
            _runtime_observation_material(
                trigger_id="A", response_id="R", events=events, measurement=_interval_mapping(0, 0),
            ),
        ),
    )

    evidence = result.state.evidence[-1]
    assert evidence.committed is True
    assert evidence.observation_assessment is not None
    assert evidence.observation_assessment.verdict == "PASS"
    target = ReferenceSession(**kwargs)
    assert target._state_error(result.state) is None


@pytest.mark.parametrize(
    ("termination_kind", "termination_type"),
    (("CANCEL", "CANCEL"), ("SUPERSEDE", "SUPERSEDE")),
)
def test_session_rejects_a_foreign_key_termination_that_targets_the_current_request(
    termination_kind: str,
    termination_type: str,
) -> None:
    """Other-key syntax does not excuse an attempt to terminate contract A."""

    binding, model, fixture = _runtime_parts()
    events = [
        {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "T", "sequence": 2, "kind": termination_kind, "key": "other", "eventType": termination_type, "timestamp": 0, "targetRequestId": "A"},
        {"id": "R", "sequence": 3, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    session = ReferenceSession(
        binding=binding, model=model,
        session_id=f"foreign-target-{termination_kind.lower()}",
        run_id=f"foreign-target-{termination_kind.lower()}",
        initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    result = session.step(
        session.initial_state,
        _environment_with_observation_material(
            fixture,
            _runtime_observation_material(
                trigger_id="A", response_id="R", events=events, measurement=_interval_mapping(0, 0),
            ),
        ),
    )

    evidence = result.state.evidence[-1]
    assert evidence.committed is False
    assert evidence.resolution_code == "OBSERVATION-INTERPRETATION-ERROR"
    assert evidence.observation_assessment is not None
    assert "INVALID-OWNERSHIP-TERMINATION" in {
        diagnostic.code for diagnostic in evidence.observation_assessment.diagnostics
    }


@pytest.mark.parametrize(
    ("termination_kind", "termination_type"),
    (("CANCEL", "CANCEL"), ("SUPERSEDE", "SUPERSEDE")),
)
def test_session_rejects_a_foreign_key_termination_that_precedes_its_controlled_target(
    termination_kind: str,
    termination_type: str,
) -> None:
    """A foreign event cannot evade validation by naming a future request."""

    binding, model, fixture = _runtime_parts()
    events = [
        {"id": "T", "sequence": 1, "kind": termination_kind, "key": "other", "eventType": termination_type, "timestamp": 0, "targetRequestId": "A"},
        {"id": "A", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "R", "sequence": 3, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": f"foreign-future-target-{termination_kind.lower()}",
        "run_id": f"foreign-future-target-{termination_kind.lower()}",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(1),
        "interpretation_contract": _runtime_interpretation_contract(model),
    }
    source = ReferenceSession(**kwargs)
    result = source.step(
        source.initial_state,
        _environment_with_observation_material(
            fixture,
            _runtime_observation_material(
                trigger_id="A", response_id="R", events=events, measurement=_interval_mapping(0, 0),
            ),
        ),
    )

    evidence = result.state.evidence[-1]
    assert evidence.committed is False
    assert evidence.resolution_code == "OBSERVATION-INTERPRETATION-ERROR"
    assert evidence.observation_assessment is not None
    assert "INVALID-OWNERSHIP-TERMINATION" in {
        diagnostic.code for diagnostic in evidence.observation_assessment.diagnostics
    }
    target = ReferenceSession(**kwargs)
    assert target._state_error(result.state) is None


def test_session_quarantines_new_response_facts_from_an_identity_conflict_and_replays_checkpoint() -> None:
    """A changed active request cannot make its fresh response reusable later."""

    binding, model, fixture = _runtime_parts()
    first_events = [
        {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "B", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "R1", "sequence": 3, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    # B is the one exact ACTIVE request that may recur.  Reusing its identity
    # with a changed timestamp is nevertheless a conflict; R2 is a new public
    # response fact in that same trace and must be quarantined/consumed.
    conflicting_events = [
        {"id": "B", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 1},
        {"id": "R2", "sequence": 4, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 1},
    ]
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="A", response_id="R1", events=first_events, measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="B", response_id="R2", events=conflicting_events, measurement=_interval_mapping(0, 0),
        ),
    )
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": "identity-quarantine",
        "run_id": "identity-quarantine",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(2),
        "retry_cap": 2,
        "interpretation_contract": _runtime_interpretation_contract(
            model, policy="FIFO", concurrent_same_key=True,
        ),
    }
    source = ReferenceSession(**kwargs)
    first = source.step(source.initial_state, environment)
    rejected = source.step(first.state, first.environment)

    assert rejected.state.evidence[-1].resolution_code == "OBSERVATION-EVENT-IDENTITY-CONFLICT"
    assert rejected.state.consumed_response_ids == {"R1", "R2"}
    assert rejected.state.terminal_trigger_event_ids == {"A"}
    assert rejected.state.active_trigger_event_ids == {"B"}
    assert rejected.state.event_identity_refs["B"].timestamp == 0
    assert rejected.state.event_identity_refs["R2"].kind == "RESPONSE"

    # The public S7 state remains a valid portable checkpoint.  With no
    # remaining round the fresh coordinator only validates it, rather than
    # issuing a synthetic recovery action.
    target = ReferenceSession(**kwargs)
    assert target._state_error(rejected.state) is None
    checkpoint = target.step(rejected.state, rejected.environment)
    assert not any(
        diagnostic.code.startswith(("SESSION-LINEAGE", "EVIDENCE-"))
        for diagnostic in checkpoint.diagnostics
    )


def test_session_preserves_bound_trace_facts_when_record_shape_and_frozen_window_both_fail() -> None:
    """S4 rejection cannot erase a response whose raw public facts are bound."""

    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="structural-window", run_id="structural-window",
        initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    raw = observation_input_from_mapping(
        _runtime_observation_material(measurement=_interval_mapping(0, 1)),
    )
    bound = bind_observation_input(
        raw,
        execution_attempt_id="structural-window:structural-window:execution:1",
        action_id="test-router",
        evidence_ref="structural-window:1",
        measurement_tick=Fraction(0),
        uncertainty_identity=model.uncertainty_identity,
    )
    malformed = VisibleExecutionRecord(
        execution_attempt_id="structural-window:structural-window:execution:1",
        action_id="test-router",
        effect_class="NONE",
        # A normal response record cannot omit its observable/S9 fields.
        observable=None,
        summary_confirmed=False,
        post_summary=None,
        measurement_tick=Fraction(0),
        uncertainty_identity=model.uncertainty_identity,
        evidence_ref="structural-window:1",
        response_id="response-1",
        observation_input=bound,
    )
    successor = SyntheticEnvironment.from_mapping(fixture["environments"]["alpha"])

    class Adapter:
        def execute(self, _request: ExecutionRequest) -> EnvironmentExecution:
            return EnvironmentExecution(malformed, successor)

    rejected = session.step(session.initial_state, Adapter())  # type: ignore[arg-type]
    evidence = rejected.state.evidence[0]
    assert evidence.resolution_code == "INVALID-EXECUTION-RECORD"
    assert evidence.observation_assessment is not None
    assert evidence.observation_assessment.verdict == "ERROR"
    assert "OBSERVATION-UNCERTAINTY-WINDOW-MISMATCH" in {
        diagnostic.code for diagnostic in evidence.observation_assessment.diagnostics
    }
    assert rejected.state.consumed_response_ids == {"response-1"}
    assert rejected.state.terminal_trigger_event_ids == {"request-1"}
    target = ReferenceSession(
        binding=binding, model=model, session_id="structural-window", run_id="structural-window",
        initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    assert target._state_error(rejected.state) is None
    checkpoint = target.step(rejected.state, rejected.environment)
    assert not any(
        diagnostic.code.startswith(("SESSION-LINEAGE", "EVIDENCE-"))
        for diagnostic in checkpoint.diagnostics
    )


def test_session_retains_declared_silence_response_facts_before_error_retry() -> None:
    """A response hidden behind a silence declaration stays consumed/terminal."""

    binding, model, fixture = _runtime_parts()
    events = [
        {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "R", "sequence": 2, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    session = ReferenceSession(
        binding=binding, model=model, session_id="declared-silence", run_id="declared-silence",
        initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    result = session.step(
        session.initial_state,
        _environment_with_observation_material(
            fixture,
            _runtime_observation_material(
                trigger_id="A", response_id=None, events=events, earliest=9,
            ),
            no_response=True,
        ),
    )
    evidence = result.state.evidence[0]
    assert evidence.resolution_code == "OBSERVATION-INTERPRETATION-ERROR"
    assert evidence.observation_assessment is not None
    assert evidence.observation_assessment.diagnostics[0].code == "RESPONSE-PRESENT-DECLARED-SILENCE"
    assert result.state.consumed_response_ids == {"R"}
    assert result.state.terminal_trigger_event_ids == {"A"}
    assert session._state_error(result.state) is None


def test_session_event_ledger_rejects_cross_kind_reuse_of_a_consumed_or_terminal_identifier() -> None:
    """A persisted set cannot silently change an orphan ID's public kind."""

    binding, model, _fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="ledger-kind", run_id="ledger-kind",
        initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    # Construct only a public checkpoint boundary here: the invariant must
    # reject a state whose scalar receipt set contradicts its typed event map
    # before any adapter can see it.
    request = observation_input_from_mapping(_runtime_observation_material()).events[0]
    invalid = replace(
        session.initial_state,
        consumed_response_ids=frozenset({"request-1"}),
        event_identity_refs=type(session.initial_state.event_identity_refs)({"request-1": request}),
    )

    class NoDispatch:
        def execute(self, _request: ExecutionRequest) -> EnvironmentExecution:  # pragma: no cover - must not run
            raise AssertionError("invalid event ledger must be rejected before dispatch")

    rejected = session.step(invalid, NoDispatch())  # type: ignore[arg-type]
    assert rejected.stop_reason == "Stop-Error"
    assert rejected.state is invalid
    assert rejected.diagnostics[0].code == "INVALID-OBSERVATION-EVENT-LEDGER"


def test_session_rejects_subclass_identity_receipts_before_dispatch() -> None:
    """Portable ledgers retain exact receipt types, not merely equal strings."""

    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="ledger-subclass", run_id="ledger-subclass",
        initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    accepted = session.step(
        session.initial_state,
        _environment_with_observation_material(
            fixture,
            _runtime_observation_material(measurement=_interval_mapping(0, 0)),
        ),
    )
    assert accepted.state.consumed_response_ids == {"response-1"}
    assert accepted.state.terminal_trigger_event_ids == {"request-1"}

    class StringSubclass(str):
        pass

    class FrozenSetSubclass(frozenset[str]):
        pass

    candidates = (
        (
            replace(
                accepted.state,
                consumed_response_ids=frozenset({StringSubclass("response-1")}),
            ),
            "INVALID-RESPONSE-IDENTITIES",
        ),
        (
            replace(
                accepted.state,
                terminal_trigger_event_ids=frozenset({StringSubclass("request-1")}),
            ),
            "INVALID-TRIGGER-IDENTITIES",
        ),
        (
            replace(
                accepted.state,
                consumed_response_ids=FrozenSetSubclass({"response-1"}),
            ),
            "INVALID-RESPONSE-IDENTITIES",
        ),
    )

    class NoDispatch:
        def execute(self, _request: ExecutionRequest) -> EnvironmentExecution:  # pragma: no cover - must not run
            raise AssertionError("subclassed checkpoint receipt must be rejected before dispatch")

    for forged, expected_code in candidates:
        state_error = session._state_error(forged)
        assert state_error is not None
        assert state_error.code == expected_code
        rejected = session.step(forged, NoDispatch())  # type: ignore[arg-type]
        assert rejected.stop_reason == "Stop-Error"
        assert rejected.state is forged
        assert rejected.diagnostics[0].code == expected_code


def test_session_detaches_event_ledger_from_a_checkpoint_backing_map_before_dispatch() -> None:
    """A hostile adapter cannot rewrite a validated S0 ledger during S4."""

    binding, model, fixture = _runtime_parts()
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": "ledger-toctou",
        "run_id": "ledger-toctou",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(2),
        "interpretation_contract": _runtime_interpretation_contract(model),
    }
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(measurement=_interval_mapping(0, 0)),
        _runtime_observation_material(
            trigger_id="request-2",
            response_id="response-2",
            events=[
                {"id": "request-2", "sequence": 3, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "response-2", "sequence": 4, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )
    source = ReferenceSession(**kwargs)
    first = source.step(source.initial_state, environment)
    assert first.state.evidence[-1].committed is True
    backing = dict(first.state.event_identity_refs)
    checkpoint = replace(first.state, event_identity_refs=MappingProxyType(backing))
    assert source._state_error(checkpoint) is None

    class MutatingAdapter:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            # This changes the caller-owned backing dictionary after the
            # session has validated its checkpoint but before S4 returns.
            backing["request-1"] = replace(backing["request-1"], timestamp=Fraction(99))
            return first.environment.execute(request)

    advanced = source.step(checkpoint, MutatingAdapter())  # type: ignore[arg-type]
    assert advanced.state.evidence[-1].committed is True
    assert advanced.state.event_identity_refs["request-1"].timestamp == Fraction(0)
    target = ReferenceSession(**kwargs)
    assert target._state_error(advanced.state) is None


def test_session_detaches_event_values_from_a_hostile_s4_checkpoint_reference() -> None:
    """A frozen event retained by an adapter cannot rewrite the S4 snapshot."""

    binding, model, fixture = _runtime_parts()
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": "ledger-event-toctou",
        "run_id": "ledger-event-toctou",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(2),
        "interpretation_contract": _runtime_interpretation_contract(model),
    }
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(measurement=_interval_mapping(0, 0)),
        _runtime_observation_material(
            trigger_id="request-2",
            response_id="response-2",
            events=[
                {"id": "request-2", "sequence": 3, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "response-2", "sequence": 4, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )
    source = ReferenceSession(**kwargs)
    first = source.step(source.initial_state, environment)
    assert first.state.evidence[-1].committed is True
    checkpoint = first.state
    assert source._state_error(checkpoint) is None

    class MutatingAdapter:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            # ``frozen=True`` does not defend against an adapter deliberately
            # using the object-level escape hatch on a retained public event.
            object.__setattr__(checkpoint.event_identity_refs["request-1"], "timestamp", Fraction(99))
            return first.environment.execute(request)

    advanced = source.step(checkpoint, MutatingAdapter())  # type: ignore[arg-type]
    assert advanced.state.evidence[-1].committed is True
    assert advanced.state.event_identity_refs["request-1"].timestamp == Fraction(0)
    target = ReferenceSession(**kwargs)
    assert target._state_error(advanced.state) is None


def test_session_detaches_fraction_leaves_inside_retained_events_before_second_dispatch() -> None:
    """A hostile adapter cannot alter an old typed timestamp in place."""

    binding, model, fixture = _runtime_parts()
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": "ledger-fraction-toctou",
        "run_id": "ledger-fraction-toctou",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(2),
        "interpretation_contract": _runtime_interpretation_contract(model),
    }
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(measurement=_interval_mapping(0, 0)),
        _runtime_observation_material(
            trigger_id="request-2", response_id="response-2",
            events=[
                {"id": "request-2", "sequence": 3, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "response-2", "sequence": 4, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ], measurement=_interval_mapping(0, 0),
        ),
    )
    source = ReferenceSession(**kwargs)
    first = source.step(source.initial_state, environment)
    checkpoint = first.state
    retained_timestamp = checkpoint.event_identity_refs["request-1"].timestamp

    class MutatingAdapter:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            object.__setattr__(retained_timestamp, "_numerator", 99)
            return first.environment.execute(request)

    advanced = source.step(checkpoint, MutatingAdapter())  # type: ignore[arg-type]
    assert advanced.state.evidence[-1].committed is True
    assert advanced.state.event_identity_refs["request-1"].timestamp == Fraction(0)
    target = ReferenceSession(**kwargs)
    assert target._state_error(advanced.state) is None


def test_session_detaches_general_mapping_values_inside_retained_evidence_before_s4() -> None:
    """A read-only Mapping wrapper cannot retain a mutable evidence alias."""

    binding, model, fixture = _runtime_parts()
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": "mapping-toctou",
        "run_id": "mapping-toctou",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(2),
        "interpretation_contract": _runtime_interpretation_contract(model),
    }
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(measurement=_interval_mapping(0, 0)),
        _runtime_observation_material(
            trigger_id="request-2", response_id="response-2",
            events=[
                {"id": "request-2", "sequence": 3, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "response-2", "sequence": 4, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ], measurement=_interval_mapping(0, 0),
        ),
    )
    source = ReferenceSession(**kwargs)
    first = source.step(source.initial_state, environment)
    backing = dict(first.state.evidence[0].detail_charges)

    class BackedMapping(ABCMapping[str, int]):
        def __iter__(self):
            return iter(backing)

        def __len__(self) -> int:
            return len(backing)

        def __getitem__(self, key: str) -> int:
            return backing[key]

    original_key = next(iter(backing))
    original_value = backing[original_key]
    checkpoint = replace(
        first.state,
        evidence=(replace(first.state.evidence[0], detail_charges=BackedMapping()),),
    )
    assert source._state_error(checkpoint) is None

    class MutatingAdapter:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            backing[original_key] = original_value + 98
            return first.environment.execute(request)

    advanced = source.step(checkpoint, MutatingAdapter())  # type: ignore[arg-type]
    assert advanced.state.evidence[-1].committed is True
    assert advanced.state.evidence[0].detail_charges[original_key] == original_value
    target = ReferenceSession(**kwargs)
    assert target._state_error(advanced.state) is None


def test_session_detaches_retained_observation_assessment_from_a_hostile_s4_reference() -> None:
    """An adapter cannot mutate historical assessment evidence during S4."""

    binding, model, fixture = _runtime_parts()
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": "assessment-toctou",
        "run_id": "assessment-toctou",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(2),
        "interpretation_contract": _runtime_interpretation_contract(model),
    }
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(measurement=_interval_mapping(0, 0)),
        _runtime_observation_material(
            trigger_id="request-2",
            response_id="response-2",
            events=[
                {"id": "request-2", "sequence": 3, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                {"id": "response-2", "sequence": 4, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
            ],
            measurement=_interval_mapping(0, 0),
        ),
    )
    source = ReferenceSession(**kwargs)
    first = source.step(source.initial_state, environment)
    assessment = first.state.evidence[0].observation_assessment
    assert assessment is not None
    assert assessment.verdict == "PASS"

    class MutatingAdapter:
        def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
            object.__setattr__(assessment, "verdict", "FAIL")
            return first.environment.execute(request)

    advanced = source.step(first.state, MutatingAdapter())  # type: ignore[arg-type]
    assert advanced.state.evidence[-1].committed is True
    retained = advanced.state.evidence[0].observation_assessment
    assert retained is not None
    assert retained.verdict == "PASS"
    target = ReferenceSession(**kwargs)
    assert target._state_error(advanced.state) is None


def test_session_does_not_reclassify_a_same_trace_request_as_a_consumed_response() -> None:
    """Malformed ``responseId=A`` cannot make the emitted S7 checkpoint invalid."""

    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="same-trace-role", run_id="same-trace-role",
        initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    result = session.step(
        session.initial_state,
        _environment_with_observation_material(
            fixture,
            _runtime_observation_material(
                trigger_id="A",
                response_id="A",
                events=[
                    {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                ],
                measurement=_interval_mapping(0, 0),
            ),
        ),
    )
    assert result.state.evidence[0].resolution_code == "OBSERVATION-INTERPRETATION-ERROR"
    assert result.state.consumed_response_ids == frozenset()
    assert result.state.active_trigger_event_ids == {"A"}
    assert result.state.event_identity_refs["A"].kind == "REQUEST"

    target = ReferenceSession(
        binding=binding, model=model, session_id="same-trace-role", run_id="same-trace-role",
        initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    assert target._state_error(result.state) is None
    checkpoint = target.step(result.state, result.environment)
    assert not any(diagnostic.code == "INVALID-OBSERVATION-EVENT-LEDGER" for diagnostic in checkpoint.diagnostics)


def test_session_rejects_sparse_response_id_reusing_an_earlier_active_request_before_ledger_write() -> None:
    """A later raw ``responseId`` cannot borrow an ACTIVE request identity."""

    binding, model, fixture = _runtime_parts()
    first_events = [
        {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "B", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "R1", "sequence": 3, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    second_events = [
        {"id": "C", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
    ]
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="A", response_id="R1", events=first_events, measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="C", response_id="B", events=second_events, measurement=_interval_mapping(0, 0),
        ),
    )
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": "sparse-response-role",
        "run_id": "sparse-response-role",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(2),
        "retry_cap": 2,
        "interpretation_contract": _runtime_interpretation_contract(
            model, policy="FIFO", concurrent_same_key=True,
        ),
    }
    source = ReferenceSession(**kwargs)
    first = source.step(source.initial_state, environment)
    rejected = source.step(first.state, first.environment)

    assert rejected.state.evidence[-1].resolution_code == "OBSERVATION-EVENT-IDENTITY-CONFLICT"
    assert rejected.state.consumed_response_ids == {"R1"}
    assert rejected.state.active_trigger_event_ids == {"B"}
    assert rejected.state.terminal_trigger_event_ids == {"A"}
    assert rejected.state.event_identity_refs["B"].kind == "REQUEST"
    target = ReferenceSession(**kwargs)
    assert target._state_error(rejected.state) is None
    checkpoint = target.step(rejected.state, rejected.environment)
    assert not any(
        diagnostic.code in {"INVALID-OBSERVATION-EVENT-LEDGER", "SESSION-LINEAGE-MISMATCH"}
        for diagnostic in checkpoint.diagnostics
    )


def test_session_quarantine_does_not_reclassify_a_new_request_named_as_the_selected_response() -> None:
    """An identity-conflicted trace can retain X:REQUEST without consuming X."""

    binding, model, fixture = _runtime_parts()
    first_events = [
        {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "B", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "R1", "sequence": 3, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    conflicted = [
        # This altered B starts the conflict; X is a separate new request
        # incorrectly named as responseId by malformed material.
        {"id": "B", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 1},
        # X is a genuinely later new fact.  It may remain quarantined when B
        # conflicts, but must not itself be a forbidden backfill.
        {"id": "X", "sequence": 4, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 1},
    ]
    environment = _two_round_observation_environment(
        fixture,
        _runtime_observation_material(
            trigger_id="A", response_id="R1", events=first_events, measurement=_interval_mapping(0, 0),
        ),
        _runtime_observation_material(
            trigger_id="X", response_id="X", events=conflicted, measurement=_interval_mapping(0, 0),
        ),
    )
    kwargs = {
        "binding": binding,
        "model": model,
        "session_id": "quarantine-role",
        "run_id": "quarantine-role",
        "initial_summary": "q0",
        "resources": ResourceState.rounds(2),
        "retry_cap": 2,
        "interpretation_contract": _runtime_interpretation_contract(
            model, policy="FIFO", concurrent_same_key=True,
        ),
    }
    source = ReferenceSession(**kwargs)
    first = source.step(source.initial_state, environment)
    rejected = source.step(first.state, first.environment)

    assert rejected.state.evidence[-1].resolution_code == "OBSERVATION-EVENT-IDENTITY-CONFLICT"
    assert rejected.state.event_identity_refs["X"].kind == "REQUEST"
    assert "X" not in rejected.state.consumed_response_ids
    assert "X" not in rejected.state.active_trigger_event_ids
    target = ReferenceSession(**kwargs)
    assert target._state_error(rejected.state) is None
    checkpoint = target.step(rejected.state, rejected.environment)
    assert not any(
        diagnostic.code in {"INVALID-OBSERVATION-EVENT-LEDGER", "SESSION-LINEAGE-MISMATCH"}
        for diagnostic in checkpoint.diagnostics
    )


def test_quarantine_keeps_fresh_response_but_skips_event_reusing_a_sparse_consumed_response_id() -> None:
    """One conflicted trace cannot turn an orphan response receipt into X:REQUEST."""

    _binding, model, _fixture = _runtime_parts()
    contract = _runtime_interpretation_contract(model)
    first = assess_observation(
        observation_input_from_mapping(
            _runtime_observation_material(
                trigger_id="A",
                response_id="X",
                events=[
                    {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                ],
                measurement=_interval_mapping(0, 0),
            ),
        ),
        contract,
    )
    consumed, terminal, refs, active = _advance_observation_ledger(
        frozenset(), frozenset(), frozenset(), {}, first,
    )
    # ``X`` is an orphan response receipt: the malformed first trace has no
    # X event to store, but the scalar receipt is still an immutable fact.
    assert consumed == {"X"}
    assert set(refs) == {"A"}
    assert active == {"A"}
    assert first.replay is not None
    assert first.replay.rejected_event_ids == frozenset()

    second = assess_observation(
        observation_input_from_mapping(
            _runtime_observation_material(
                trigger_id="X",
                response_id="Y",
                events=[
                    {"id": "X", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                    {"id": "Y", "sequence": 2, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
                ],
                measurement=_interval_mapping(0, 0),
            ),
        ),
        contract,
    )
    conflict = _observation_replay_conflict(refs, active, terminal, consumed, second)
    assert conflict is not None
    assert conflict.code == "OBSERVATION-EVENT-IDENTITY-CONFLICT"
    next_consumed, next_terminal, next_refs, next_active = _quarantine_conflicted_observation_ledger(
        consumed, terminal, refs, active, second,
    )
    # X keeps its original scalar response role; Y is an uncontested fresh
    # response and therefore remains sealed even though the trace is rejected.
    assert next_consumed == {"X", "Y"}
    assert "X" not in next_refs
    assert next_refs["Y"].kind == "RESPONSE"
    assert next_active == {"A"}
    assert _event_identity_ledger_error(next_refs, next_active, next_terminal, next_consumed) is None


def test_identity_conflict_precedes_same_trace_duplicate_response_and_quarantines_only_fresh_facts() -> None:
    """A duplicate must not mask a changed CANCEL/SUPERSEDE event identity."""

    _binding, model, _fixture = _runtime_parts()
    contract = _runtime_interpretation_contract(model)
    first = assess_observation(
        observation_input_from_mapping(
            _runtime_observation_material(
                trigger_id="A",
                response_id=None,
                events=[
                    {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                    {"id": "X", "sequence": 2, "kind": "CANCEL", "key": "k", "eventType": "CANCEL", "timestamp": 0, "targetRequestId": "A"},
                    {"id": "R1", "sequence": 3, "kind": "RESPONSE", "key": "other", "eventType": "RESP", "timestamp": 2},
                ],
                earliest=9,
            ),
        ),
        contract,
    )
    consumed, terminal, refs, active = _advance_observation_ledger(
        frozenset(), frozenset(), frozenset(), {}, first,
    )
    assert consumed == {"R1"}
    assert terminal == {"A"}
    assert refs["X"].kind == "CANCEL"

    second = assess_observation(
        observation_input_from_mapping(
            _runtime_observation_material(
                trigger_id="X",
                response_id="R2",
                events=[
                    # X changes from CANCEL to REQUEST while R1 is also a
                    # duplicate; the identity conflict must take precedence.
                    {"id": "X", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                    {"id": "R2", "sequence": 2, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 2},
                    {"id": "R1", "sequence": 3, "kind": "RESPONSE", "key": "other", "eventType": "RESP", "timestamp": 2},
                ],
                measurement=_interval_mapping(2, 2),
            ),
        ),
        contract,
    )
    conflict = _observation_replay_conflict(refs, active, terminal, consumed, second)
    assert conflict is not None
    assert conflict.code == "OBSERVATION-EVENT-IDENTITY-CONFLICT"
    next_consumed, next_terminal, next_refs, next_active = _quarantine_conflicted_observation_ledger(
        consumed, terminal, refs, active, second,
    )
    assert next_refs["X"].kind == "CANCEL"
    assert next_refs["R2"].kind == "RESPONSE"
    assert next_consumed == {"R1", "R2"}
    assert next_terminal == {"A"}
    assert next_active == frozenset()
    assert _event_identity_ledger_error(next_refs, next_active, next_terminal, next_consumed) is None


def test_quarantined_response_cannot_later_discharge_the_retained_active_request() -> None:
    """A response sealed during S7 cannot be repaired by a friendlier replay."""

    _binding, model, _fixture = _runtime_parts()
    contract = _runtime_interpretation_contract(
        model, policy="FIFO", concurrent_same_key=True,
    )
    first = assess_observation(
        observation_input_from_mapping(
            _runtime_observation_material(
                trigger_id="A",
                response_id="R1",
                events=[
                    {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                    {"id": "B", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                    {"id": "R1", "sequence": 3, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
                ],
                measurement=_interval_mapping(0, 0),
            ),
        ),
        contract,
    )
    consumed, terminal, refs, active = _advance_observation_ledger(
        frozenset(), frozenset(), frozenset(), {}, first,
    )
    assert terminal == {"A"}
    assert active == {"B"}

    conflicted = assess_observation(
        observation_input_from_mapping(
            _runtime_observation_material(
                trigger_id="B",
                response_id="R2",
                events=[
                    # B's changed timestamp makes this cross-round trace
                    # invalid, although R2 is a fresh public response fact.
                    {"id": "B", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 1},
                    {"id": "R2", "sequence": 3, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 1},
                ],
                measurement=_interval_mapping(0, 0),
            ),
        ),
        contract,
    )
    conflict = _observation_replay_conflict(refs, active, terminal, consumed, conflicted)
    assert conflict is not None
    assert conflict.code == "OBSERVATION-EVENT-IDENTITY-CONFLICT"
    consumed, terminal, refs, active = _quarantine_conflicted_observation_ledger(
        consumed, terminal, refs, active, conflicted,
    )
    assert consumed == {"R1", "R2"}
    assert terminal == {"A"}
    assert active == {"B"}

    repaired = assess_observation(
        observation_input_from_mapping(
            _runtime_observation_material(
                trigger_id="B",
                response_id="R2",
                events=[
                    # B is now byte-for-byte identical to its original
                    # active event, but R2 was already sealed by S7.
                    {"id": "B", "sequence": 2, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                    {"id": "R2", "sequence": 3, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 1},
                ],
                measurement=_interval_mapping(1, 1),
            ),
        ),
        contract,
    )
    duplicate = _observation_replay_conflict(refs, active, terminal, consumed, repaired)
    assert duplicate is not None
    assert duplicate.code == "DUPLICATE-OBSERVATION-RESPONSE"
    consumed, terminal, refs, active = _quarantine_conflicted_observation_ledger(
        consumed, terminal, refs, active, repaired,
    )
    assert consumed == {"R1", "R2"}
    assert terminal == {"A"}
    assert active == {"B"}
    assert _event_identity_ledger_error(refs, active, terminal, consumed) is None


@pytest.mark.parametrize(
    "replay_field",
    ("request_dispositions", "termination_refs", "response_resolutions", "event_refs"),
)
def test_session_lineage_rejects_str_subclass_keys_in_every_replay_mapping(replay_field: str) -> None:
    """Checkpoint replay never treats a string subclass as a canonical ID."""

    binding, model, fixture = _runtime_parts()
    events = [
        {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
        {"id": "C", "sequence": 2, "kind": "CANCEL", "key": "k", "eventType": "CANCEL", "timestamp": 0, "targetRequestId": "A"},
        {"id": "R", "sequence": 3, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
    ]
    session = ReferenceSession(
        binding=binding, model=model, session_id=f"subclass-{replay_field}",
        run_id=f"subclass-{replay_field}", initial_summary="q0", resources=ResourceState.rounds(2),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    first = session.step(
        session.initial_state,
        _environment_with_observation_material(
            fixture,
            _runtime_observation_material(
                trigger_id="A", response_id="R", events=events, measurement=_interval_mapping(0, 0),
            ),
        ),
    )
    assessment = first.state.evidence[0].observation_assessment
    assert assessment is not None and assessment.replay is not None
    entries = dict(getattr(assessment.replay, replay_field))
    assert entries
    original_key = next(iter(entries))

    class StringSubclass(str):
        pass

    entries[StringSubclass(original_key)] = entries.pop(original_key)
    forged_assessment = replace(
        assessment,
        replay=replace(assessment.replay, **{replay_field: entries}),
    )
    forged_state = replace(
        first.state,
        evidence=(replace(first.state.evidence[0], observation_assessment=forged_assessment),),
    )

    class NoDispatch:
        def execute(self, _request: ExecutionRequest) -> EnvironmentExecution:  # pragma: no cover - must not run
            raise AssertionError("forged replay must be rejected before dispatch")

    rejected = session.step(forged_state, NoDispatch())  # type: ignore[arg-type]
    assert rejected.stop_reason == "Stop-Error"
    assert rejected.state is forged_state
    assert rejected.diagnostics[0].code == "EVIDENCE-INTERPRETATION-MISMATCH"


def test_session_lineage_rejects_a_forged_rejected_raw_event_identity_set() -> None:
    """Parse-rejection provenance is a closed causal-evidence field."""

    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="forged-rejected-event-ids",
        run_id="forged-rejected-event-ids",
        initial_summary="q0",
        resources=ResourceState.rounds(2),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    first = session.step(
        session.initial_state,
        _environment_with_observation_material(
            fixture,
            _runtime_observation_material(
                trigger_id="A",
                response_id="R2",
                events=[
                    {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 0},
                    {"id": "R2", "sequence": 0, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 0},
                ],
                measurement=_interval_mapping(0, 0),
            ),
        ),
    )
    assessment = first.state.evidence[0].observation_assessment
    assert assessment is not None and assessment.replay is not None
    assert assessment.replay.rejected_event_ids == {"R2"}
    assert session._state_error(first.state) is None

    forged_assessment = replace(
        assessment,
        replay=replace(assessment.replay, rejected_event_ids=frozenset()),
    )
    forged_state = replace(
        first.state,
        evidence=(replace(first.state.evidence[0], observation_assessment=forged_assessment),),
    )

    class NoDispatch:
        def execute(self, _request: ExecutionRequest) -> EnvironmentExecution:  # pragma: no cover - must not run
            raise AssertionError("forged parser provenance must be rejected before dispatch")

    rejected = session.step(forged_state, NoDispatch())  # type: ignore[arg-type]
    assert rejected.stop_reason == "Stop-Error"
    assert rejected.state is forged_state
    assert rejected.diagnostics[0].code == "EVIDENCE-INTERPRETATION-MISMATCH"


def test_session_turns_a_timestamp_delta_mismatch_into_a_replayable_s7_ledger_record() -> None:
    """T5 timing closure survives live rejection and a fresh checkpoint audit."""

    binding, model, fixture = _runtime_parts()
    session = ReferenceSession(
        binding=binding, model=model, session_id="delta-s7", run_id="delta-s7",
        initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    events = [
        {"id": "A", "sequence": 1, "kind": "REQUEST", "key": "k", "eventType": "REQ", "timestamp": 7},
        {"id": "R", "sequence": 2, "kind": "RESPONSE", "key": "k", "eventType": "RESP", "timestamp": 8},
    ]
    result = session.step(
        session.initial_state,
        _environment_with_observation_material(
            fixture,
            _runtime_observation_material(
                trigger_id="A", response_id="R", events=events, measurement=_interval_mapping(0, 0),
            ),
        ),
    )
    evidence = result.state.evidence[0]
    assert evidence.resolution_code == "OBSERVATION-INTERPRETATION-ERROR"
    assert evidence.observation_assessment is not None
    assert evidence.observation_assessment.diagnostics[0].code == "MEASUREMENT-EVENT-DELTA-MISMATCH"
    assert result.state.consumed_response_ids == {"R"}
    assert result.state.terminal_trigger_event_ids == {"A"}
    target = ReferenceSession(
        binding=binding, model=model, session_id="delta-s7", run_id="delta-s7",
        initial_summary="q0", resources=ResourceState.rounds(1),
        interpretation_contract=_runtime_interpretation_contract(model),
    )
    assert target._state_error(result.state) is None
    checkpoint = target.step(result.state, result.environment)
    assert not any(
        diagnostic.code.startswith(("SESSION-LINEAGE", "EVIDENCE-"))
        for diagnostic in checkpoint.diagnostics
    )


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
    assert prep_result.stop_reason == "Stop-Budget"
    assert prep_result.stop_trace is not None
    assert prep_result.stop_trace.phase == "POST-UPDATE"

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
    assert wide_result.stop_reason == "Stop-Budget"
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

    assert result.stop_reason == "Stop-Budget"
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
