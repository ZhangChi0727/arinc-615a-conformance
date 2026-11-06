"""A-stage feasibility witnesses for the bounded 615A scenario package.

The tests intentionally construct only a small, package-derived finite
projection. They do not implement a DATA-LOADER, target hardware, parser,
network, solver, or real experiment. The projection exists solely to prove
that the accepted session seam can consume the new package's actual action
IDs/public outcomes, retain a typed successor after a post-dispatch error, and
enter the honest P3-unavailable route.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
import json
from pathlib import Path

from cltav_runtime.bindings import RuntimeAuthorityBinding
from cltav_runtime.kernel import ContractSnapshot, ModelContext
from cltav_runtime.model import FiniteSessionModel
from cltav_runtime.session import ReferenceSession, ResourceState
from cltav_runtime.synthetic import EnvironmentExecution, ExecutionRequest, SyntheticEnvironment, VisibleExecutionRecord


ROOT = Path(__file__).resolve().parents[2]
SCENARIO_PACKAGE = ROOT / "configs/engineering/cltav_615a_scenarios.json"
DEVELOPMENT_PATH = "configs/engineering/cltav_development_contracts.json"
INTERFACE_PATH = "configs/research/cltav_interface_registry.json"
INSPECT_ACTION_ID = "ACT-INSPECT-NO-WRQ-BEFORE-READY"
RECOVER_ACTION_ID = "ACT-RECOVER-RECONFIRM-READY"


def _scenario_package() -> dict[str, object]:
    value = json.loads(SCENARIO_PACKAGE.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _require_mapping(value: object) -> dict[str, object]:
    assert isinstance(value, dict)
    return value


def _action(package: dict[str, object], action_id: str) -> dict[str, object]:
    actions = package.get("actionLibrary")
    assert isinstance(actions, list)
    result = next(item for item in actions if isinstance(item, dict) and item.get("id") == action_id)
    assert isinstance(result, dict)
    return result


def _outcome(action: dict[str, object], observable: str) -> dict[str, object]:
    outcomes = action.get("possibleOutcomes")
    assert isinstance(outcomes, list)
    result = next(item for item in outcomes if isinstance(item, dict) and item.get("observable") == observable)
    assert isinstance(result, dict)
    return result


def _members(package: dict[str, object]) -> list[dict[str, object]]:
    domain = _require_mapping(package.get("hypothesisDomain"))
    rows = domain.get("members")
    assert isinstance(rows, list) and rows
    result = [_require_mapping(row) for row in rows]
    assert all(isinstance(row.get("id"), str) and isinstance(row.get("kind"), str) for row in result)
    return result


def _authority_commit(package: dict[str, object]) -> str:
    identity = _require_mapping(package.get("identity"))
    value = identity.get("acceptedAuthorityCommit")
    assert isinstance(value, str) and len(value) == 40
    return value


def _action_cost(action: dict[str, object]) -> tuple[int, dict[str, int]]:
    declared = _require_mapping(action.get("cost"))
    charges = {
        "acquisition": declared.get("acquisition"),
        "computation": declared.get("computation"),
        "preparation": declared.get("preparation"),
        # The candidate package deliberately does not invent a separate
        # recovery accounting field. The existing seam projects its declared
        # preparation charge; this does not claim a real hardware cost.
        "recovery": 0,
        "retry": declared.get("retry"),
    }
    assert all(isinstance(value, int) and not isinstance(value, bool) and value >= 0 for value in charges.values())
    return max(1, sum(charges.values())), charges


def _finite_action(
    package: dict[str, object],
    action_id: str,
    *,
    state_id: str,
    member_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Map one declared scene action/outcome relation into the finite seam API."""

    declared = _action(package, action_id)
    inspection = _require_mapping(declared.get("inspection"))
    horizon = inspection.get("finiteHorizonTicks")
    assert isinstance(horizon, int) and not isinstance(horizon, bool) and horizon >= 0
    cost, charges = _action_cost(declared)
    outcomes = declared.get("possibleOutcomes")
    assert isinstance(outcomes, list) and outcomes
    emissions: dict[str, str] = {}
    for member in member_rows:
        member_id = member["id"]
        assert isinstance(member_id, str)
        matching = [
            candidate for candidate in outcomes
            if isinstance(candidate, dict) and member_id in candidate.get("compatibleHypotheses", [])
        ]
        # A summary-only Recover produces no classified observable at this
        # seam. The finite API nevertheless requires a total declaration for
        # every retained member, including the conservatively retained
        # EARLY-WRQ member. Its sole package outcome is therefore a typed
        # placeholder only; `_scenario_environment` deliberately returns no
        # observable for Recover and does not use it to classify H.
        if not matching and declared["kind"] == "RECOVER" and len(outcomes) == 1:
            matching = outcomes
        assert len(matching) == 1
        observable = matching[0].get("observable")
        assert isinstance(observable, str) and observable
        emissions[member_id] = observable
    finite: dict[str, object] = {
        "id": declared["id"],
        "kind": declared["kind"],
        "cost": cost,
        "detailCharges": charges,
        "enabledSummaries": ["SCENE-ENTRY"],
        "transition": {
            "id": f"TR-{declared['id']}",
            "source": state_id,
            "target": state_id,
            "guardAst": {"tag": "TRUE"},
            "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": state_id}],
        },
        "observableByHypothesis": emissions,
        "measurementTicksByHypothesis": {member_id: horizon for member_id in emissions},
    }
    if declared["kind"] in {"PREP", "RECOVER"}:
        receipt = inspection.get("completionReceipt")
        assert isinstance(receipt, str) and receipt
        finite["declaredTarget"] = receipt
        finite["recoverWhenUnknown"] = declared["kind"] == "RECOVER"
    return finite


def _scenario_runtime_parts(
    package: dict[str, object],
    *,
    include_recover: bool,
) -> tuple[RuntimeAuthorityBinding, FiniteSessionModel]:
    """Construct a real binding plus a package-only finite seam projection.

    No test fixture supplies H, states, actions, observables, clock identity or
    resource charges here. The locally necessary AST self-loop is just the
    finite test harness transition; all externally visible identifiers come
    from the controlled scenario package.
    """

    commit = _authority_commit(package)
    binding = RuntimeAuthorityBinding.from_git_objects(
        repository=ROOT,
        development_commit=commit,
        development_path=DEVELOPMENT_PATH,
        interface_commit=commit,
        interface_path=INTERFACE_PATH,
    )
    snapshot = ContractSnapshot.from_git_object(
        repository=ROOT,
        contract_commit=commit,
        contract_path=DEVELOPMENT_PATH,
    )
    time = _require_mapping(package.get("timeAndObservation"))
    clock_id = time.get("virtualClockId")
    uncertainty_id = time.get("uncertaintyIdentity")
    assert isinstance(clock_id, str) and clock_id
    assert isinstance(uncertainty_id, str) and uncertainty_id
    members = _members(package)
    identity = _require_mapping(package.get("identity"))
    family = identity.get("scenarioFamilyId")
    assert isinstance(family, str) and family
    state_id = f"S-{family}-ENTRY"
    kinds = sorted({str(row["kind"]) for row in members})
    model_declaration = {
        "stateIds": [state_id],
        "clockIds": [clock_id],
        "typedDomains": {"scenarioKind": kinds},
    }
    context = ModelContext.build(
        snapshot=snapshot,
        model={
            "stateIds": set(model_declaration["stateIds"]),
            "clockIds": set(model_declaration["clockIds"]),
            "typedDomains": {"scenarioKind": set(kinds)},
        },
        projection_clock=clock_id,
    )
    hypotheses = [
        {
            "id": row["id"],
            "controlStateId": state_id,
            "clockConstraint": {
                clock_id: {
                    "lower": {"numerator": 0, "positiveDenominator": 1},
                    "upper": {"numerator": 0, "positiveDenominator": 1},
                    "lowerClosed": True,
                    "upperClosed": True,
                },
            },
            "typedStore": {"scenarioKind": row["kind"]},
        }
        for row in members
    ]
    action_ids = [INSPECT_ACTION_ID] + ([RECOVER_ACTION_ID] if include_recover else [])
    actions = [
        _finite_action(package, action_id, state_id=state_id, member_rows=members)
        for action_id in action_ids
    ]
    model = {
        "model": model_declaration,
        "hypotheses": hypotheses,
        "actions": actions,
        "limits": {
            "pathLength": 2,
            "frontierStates": len(members),
            "hypotheses": len(members),
            "actions": len(actions),
            "observationClasses": len({
                observable
                for action in actions
                for observable in _require_mapping(action["observableByHypothesis"]).values()
            }),
        },
        "uncertainty": {
            "id": uncertainty_id,
            "clockId": clock_id,
            "timeUnit": "ticks",
            "maximumErrorTicks": 0,
        },
    }
    return binding, FiniteSessionModel.from_mapping(context=context, value=model)


@dataclass(frozen=True)
class _LoaderScenarioEnvironment(SyntheticEnvironment):
    """Constrained, immutable A seam; this is not the future object model.

    Separate loader and TH values prove that successor state is not smuggled
    through a mutable generic fixture. The class has no evaluator-fault label
    field: that private information cannot affect its public result.
    """

    public_journal: tuple[str, ...] = ()
    loader_state: str = ""
    target_hardware_state: str = ""
    current_session_ready_receipt: str | None = None
    force_post_dispatch_summary_error: bool = False

    def _next(
        self,
        *,
        state: str | None = None,
        pending: VisibleExecutionRecord | None = None,
        journal: tuple[str, ...] | None = None,
        loader_state: str | None = None,
        target_hardware_state: str | None = None,
        ready_receipt: str | None = None,
    ) -> "_LoaderScenarioEnvironment":
        return _LoaderScenarioEnvironment(
            state if state is not None else self._state,
            self._uncertainty_identity,
            self._states,
            pending,
            self.public_journal if journal is None else journal,
            self.loader_state if loader_state is None else loader_state,
            self.target_hardware_state if target_hardware_state is None else target_hardware_state,
            self.current_session_ready_receipt if ready_receipt is None else ready_receipt,
            self.force_post_dispatch_summary_error,
        )

    def with_pending_delivery(self, record: VisibleExecutionRecord) -> "_LoaderScenarioEnvironment":
        if self._pending_delivery is not None:
            raise ValueError("scenario seam already has an unconsumed pending delivery")
        return self._next(pending=record)

    def take_pending_delivery(self) -> tuple[VisibleExecutionRecord, "_LoaderScenarioEnvironment"] | None:
        if self._pending_delivery is None:
            return None
        return self._pending_delivery, self._next()

    def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
        execution = super().execute(request)
        record = execution.record
        ready_receipt = self.current_session_ready_receipt
        loader_state = self.loader_state
        target_state = self.target_hardware_state
        if request.action_id == RECOVER_ACTION_ID:
            ready_receipt = f"{request.session_id}:RECOVER-READY-READBACK-COMPLETED"
            loader_state = "LOADER-READY-RECONFIRMED"
            target_state = "TH-READY-READBACK-RETAINED"
        else:
            loader_state = "LOADER-INSPECTION-COMPLETE"
            target_state = "TH-STATE-PRESERVED-DURING-INSPECTION"
        successor = self._next(
            state=execution.successor._state,
            journal=self.public_journal + (record.evidence_ref,),
            loader_state=loader_state,
            target_hardware_state=target_state,
            ready_receipt=ready_receipt,
        )
        if self.force_post_dispatch_summary_error and request.action_id == INSPECT_ACTION_ID:
            # Deliberately emulate a returned adapter record that loses its
            # post-dispatch summary. The session must retain `successor`, not
            # roll back the loader/TH state before qualified Recover.
            record = replace(record, post_summary=None)
        return EnvironmentExecution(record, successor)


def _scenario_environment(
    package: dict[str, object],
    model: FiniteSessionModel,
    *,
    force_post_dispatch_summary_error: bool = False,
) -> _LoaderScenarioEnvironment:
    inspect = _action(package, INSPECT_ACTION_ID)
    inspect_outcome = _outcome(inspect, "NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001")
    recover = _action(package, RECOVER_ACTION_ID)
    recover_outcome = _outcome(recover, "RECOVER-READY-READBACK")
    recover_receipt = _require_mapping(recover["inspection"])["completionReceipt"]
    assert isinstance(recover_receipt, str)
    states = {
        "LOADER-PRE-READY": {
            INSPECT_ACTION_ID: {
                "effectClass": "NONE",
                "observable": inspect_outcome["observable"],
                "summaryConfirmed": True,
                "postSummary": inspect_outcome["postSummary"],
                "measurementTick": _require_mapping(inspect["inspection"])["finiteHorizonTicks"],
                "nextPrivateState": "LOADER-AFTER-INSPECTION",
            },
        },
        "LOADER-AFTER-INSPECTION": {
            RECOVER_ACTION_ID: {
                # This is the existing typed IF-PREP-RECOVER summary-only
                # return. Its receipt names the package's public read-back;
                # it does not claim a future B wire-event implementation.
                "effectClass": "NONE",
                "observable": None,
                "summaryConfirmed": True,
                "postSummary": recover_outcome["postSummary"],
                "measurementTick": None,
                "nextPrivateState": "LOADER-RECOVERED",
                "prepRecover": {
                    "targetConfirmed": True,
                    "summaryConfirmed": True,
                    "prepError": False,
                    "ineligible": False,
                    "declaredTarget": recover_receipt,
                    "evidence": f"current-session:{recover_outcome['observable']}:{recover_receipt}",
                    "postSummary": recover_outcome["postSummary"],
                },
            },
        },
        "LOADER-RECOVERED": {
            RECOVER_ACTION_ID: {
                "effectClass": "NONE",
                "observable": None,
                "summaryConfirmed": True,
                "postSummary": recover_outcome["postSummary"],
                "measurementTick": None,
                "nextPrivateState": "LOADER-RECOVERED",
                "prepRecover": {
                    "targetConfirmed": True,
                    "summaryConfirmed": True,
                    "prepError": False,
                    "ineligible": False,
                    "declaredTarget": recover_receipt,
                    "evidence": f"current-session:{recover_outcome['observable']}:{recover_receipt}",
                    "postSummary": recover_outcome["postSummary"],
                },
            },
        },
    }
    source = {
        "initialPrivateState": "LOADER-PRE-READY",
        "uncertaintyIdentity": model.uncertainty_identity,
        "states": states,
    }
    base = SyntheticEnvironment.from_mapping(source)
    return _LoaderScenarioEnvironment(
        base._state,
        base._uncertainty_identity,
        base._states,
        None,
        ("STIM-LIST-SUBMISSION-PRECONDITION",),
        "LOADER-LIST-OFFERED",
        "TH-AWAITING-CURRENT-SESSION-WRQ",
        None,
        force_post_dispatch_summary_error,
    )


def _run_normal_public_projection(package: dict[str, object]) -> tuple[object, ...]:
    """Run an output that has no evaluator-only label input or object field."""

    binding, model = _scenario_runtime_parts(package, include_recover=False)
    environment = _scenario_environment(package, model)
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="scenario-label-isolation",
        run_id="scenario-label-isolation",
        initial_summary="SCENE-ENTRY",
        resources=ResourceState.rounds(1),
        retry_cap=1,
    )
    result = session.step(session.initial_state, environment)
    evidence = result.state.evidence[-1]
    snapshot = evidence.snapshot
    # The tuple deliberately contains every A-level consumer-visible outcome,
    # not merely observable/postSummary: action/snapshot, H/eta, resource and
    # stop behavior all must remain independent of an evaluator-only label.
    return (
        evidence.execution.action_id,
        snapshot.action_id,
        tuple((item.observable, tuple(sorted(item.hypotheses))) for item in snapshot.classes),
        result.state.history.hypotheses,
        result.state.history.status_by_hypothesis,
        result.state.history.version,
        evidence.resource_before,
        evidence.resource_after,
        tuple(sorted(evidence.detail_charges.items())),
        tuple(sorted(evidence.projected_cost.items())),
        result.stop_reason,
        evidence.execution.observable,
        evidence.execution.post_summary,
        result.state.context.current_summary,
    )


def test_a11_finite_normal_test_returns_package_public_summary_and_exact_tick() -> None:
    package = _scenario_package()
    binding, model = _scenario_runtime_parts(package, include_recover=False)
    assert binding.development.contract_commit == _authority_commit(package)
    environment = _scenario_environment(package, model)
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="scenario-finite-test",
        run_id="scenario-finite-test",
        initial_summary="SCENE-ENTRY",
        resources=ResourceState.rounds(1),
        retry_cap=1,
    )
    result = session.step(session.initial_state, environment)
    evidence = result.state.evidence[-1]
    inspect = _action(package, INSPECT_ACTION_ID)
    no_wrq = _outcome(inspect, "NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001")
    assert evidence.execution.action_id == INSPECT_ACTION_ID
    assert evidence.execution.observable == no_wrq["observable"]
    assert evidence.execution.summary_confirmed is True
    assert evidence.execution.post_summary == no_wrq["postSummary"]
    assert evidence.execution.measurement_tick == Fraction(
        _require_mapping(inspect["inspection"])["finiteHorizonTicks"],
    )
    assert evidence.execution.response_id is None and evidence.execution.observation_input is None
    assert evidence.observation_assessment is None
    assert all("NO-RESPONSE" not in diagnostic.code for diagnostic in result.diagnostics)


def test_a12_public_projection_has_no_evaluator_label_input_and_preserves_full_result() -> None:
    package = _scenario_package()
    inspect = _action(package, INSPECT_ACTION_ID)
    derivation = _require_mapping(inspect["summaryDerivation"])
    forbidden = derivation.get("forbiddenPrivateSources")
    assert isinstance(forbidden, list) and "ACTIVE-FAULT-ID" in forbidden
    assert "evaluator_only_fault_label" not in _LoaderScenarioEnvironment.__dataclass_fields__

    # Labels are deliberately external test metadata. They cannot be passed to
    # the environment or its public-summary projection.
    labels = ("EARLY-WRQ", "EARLY-DATA")
    results = []
    for _evaluator_only_label in labels:
        results.append(_run_normal_public_projection(package))
    assert results[0] == results[1]


def test_a13_actual_package_bound_runtime_binding_keeps_p3_unavailable() -> None:
    package = _scenario_package()
    binding, model = _scenario_runtime_parts(package, include_recover=False)
    witness_rows = package.get("feasibilityWitnesses")
    assert isinstance(witness_rows, list)
    witness = next(row for row in witness_rows if isinstance(row, dict) and row.get("id") == "WIT-P3-UNAVAILABLE")
    assert INSPECT_ACTION_ID in model.actions
    assert "P3-UNAVAILABLE" in str(witness["claim"])
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="scenario-p3-unavailable",
        run_id="scenario-p3-unavailable",
        initial_summary="SCENE-ENTRY",
        resources=ResourceState.rounds(0),
        retry_cap=1,
    )

    class _NoDispatch:
        calls = 0

        def execute(self, _request: object) -> object:  # pragma: no cover - dispatch is the failure
            self.calls += 1
            raise AssertionError("P3-unavailable checkpoint must not dispatch")

    no_dispatch = _NoDispatch()
    result = session.step(session.initial_state, no_dispatch)  # type: ignore[arg-type]
    assert no_dispatch.calls == 0
    assert result.stop_reason == "Stop-Budget"
    assert result.stop_trace is not None
    assert result.stop_trace.applicability_status == "P3-UNAVAILABLE"
    assert result.stop_trace.applicability_context_id is None
    assert result.stop_trace.active_named_645_residuals == ()


def test_a14_post_dispatch_error_preserves_loader_th_successor_pending_and_qualified_recover() -> None:
    package = _scenario_package()
    binding, model = _scenario_runtime_parts(package, include_recover=True)
    clean = _scenario_environment(package, model)
    issued = clean.execute(ExecutionRequest("direct", "direct-1", INSPECT_ACTION_ID, "TEST"))
    assert type(issued.successor) is _LoaderScenarioEnvironment
    assert issued.successor.loader_state == "LOADER-INSPECTION-COMPLETE"
    assert issued.successor.target_hardware_state == "TH-STATE-PRESERVED-DURING-INSPECTION"
    assert clean.loader_state == "LOADER-LIST-OFFERED"
    pending = issued.successor.with_pending_delivery(issued.record)
    delivery = pending.take_pending_delivery()
    assert delivery is not None
    consumed, after_receive = delivery
    assert consumed is issued.record
    assert type(after_receive) is _LoaderScenarioEnvironment
    assert after_receive.public_journal == issued.successor.public_journal
    assert pending.public_journal == issued.successor.public_journal

    environment = _scenario_environment(package, model, force_post_dispatch_summary_error=True)
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="scenario-unknown-recover",
        run_id="scenario-unknown-recover",
        initial_summary="SCENE-ENTRY",
        resources=ResourceState.rounds(2),
        retry_cap=2,
    )
    first = session.step(session.initial_state, environment)
    assert first.stop_reason is None
    assert first.state.context.q_status == "UNKNOWN"
    assert first.state.evidence[-1].resolution_code == "SUMMARY-CONFIRMATION-ERROR"
    assert type(first.environment) is _LoaderScenarioEnvironment
    assert first.environment._state == "LOADER-AFTER-INSPECTION"
    assert first.environment.loader_state == "LOADER-INSPECTION-COMPLETE"
    assert first.environment.target_hardware_state == "TH-STATE-PRESERVED-DURING-INSPECTION"
    assert first.environment.public_journal != environment.public_journal
    assert first.environment.current_session_ready_receipt is None

    second = session.step(first.state, first.environment)
    recover = _action(package, RECOVER_ACTION_ID)
    recover_outcome = _outcome(recover, "RECOVER-READY-READBACK")
    assert second.state.evidence[-1].snapshot.action_id == RECOVER_ACTION_ID
    assert second.state.evidence[-1].resolution_code == "COMMIT"
    assert second.state.context.q_status == "KNOWN"
    assert second.state.context.current_summary == recover_outcome["postSummary"]
    assert type(second.environment) is _LoaderScenarioEnvironment
    assert second.environment._state == "LOADER-RECOVERED"
    assert second.environment.loader_state == "LOADER-READY-RECONFIRMED"
    assert second.environment.target_hardware_state == "TH-READY-READBACK-RETAINED"
    assert second.environment.current_session_ready_receipt == (
        "scenario-unknown-recover:RECOVER-READY-READBACK-COMPLETED"
    )
