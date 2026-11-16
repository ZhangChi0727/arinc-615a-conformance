"""Production C-stage tests for the real B controller/session adapter.

These tests intentionally import the production adapter only.  They do not
reuse the A-stage canned `_LoaderScenarioEnvironment` feasibility seam.
"""

from __future__ import annotations

from dataclasses import fields, replace
from fractions import Fraction
import json
from pathlib import Path

import pytest

from cltav_615a import FaultVariant, LurStartController
from cltav_615a_adapter.contract import (
    C_OWNERSHIP_CANCEL_TYPE,
    C_OWNERSHIP_CONTRACT_ID,
    C_OWNERSHIP_KEY,
    C_OWNERSHIP_RESPONSE_TYPE,
    C_OWNERSHIP_SUPERSEDE_TYPE,
    C_OWNERSHIP_TRIGGER_TYPE,
    H_B_COMMIT,
    H_B_SCENARIO_GIT_BLOB_OID,
    H_B_SCENARIO_RAW_SHA256,
    INSPECT_ACTION_ID,
    ORDER_ACTION_ID,
    PREP_ACTION_ID,
    RECOVER_ACTION_ID,
    c_interpretation_contract,
    load_hb_session_contract,
)
from cltav_615a_adapter.session import (
    AppliedDeliveryEvidence,
    LurStartSessionEnvironment,
    OwnershipProjection,
    SessionAdapterError,
    ToolReadbackEvidence,
    build_lur_start_session,
)
import cltav_615a_adapter.session as session_adapter_module
from cltav_runtime.interpretation import (
    OwnershipEvent,
    OwnershipOrderBoundary,
    replay_ownership,
)
from cltav_runtime.session import ResourceState
from cltav_runtime.synthetic import EnvironmentExecution, ExecutionRequest


ROOT = Path(__file__).resolve().parents[2]


def _request(environment: LurStartSessionEnvironment, action_id: str, kind: str, attempt: str) -> ExecutionRequest:
    return ExecutionRequest(
        session_id=environment.checkpoint.session_id,
        execution_attempt_id=attempt,
        action_id=action_id,
        action_kind=kind,
    )


def _normal_after_prep() -> tuple[object, object, LurStartSessionEnvironment]:
    built = build_lur_start_session(repository=ROOT, controller=LurStartController())
    first = built.session.step(built.session.initial_state, built.environment)
    assert first.stop_reason is None
    second = built.session.step(first.state, first.environment)
    assert second.stop_reason is None
    assert isinstance(second.environment, LurStartSessionEnvironment)
    return built, second, second.environment


def test_c01_fixed_hb_source_identity_and_closed_adapter_identity() -> None:
    contract = load_hb_session_contract(ROOT)
    assert contract.scenario_input.commit == H_B_COMMIT
    assert contract.scenario_input.git_blob_oid == H_B_SCENARIO_GIT_BLOB_OID
    assert contract.scenario_input.raw_sha256 == H_B_SCENARIO_RAW_SHA256

    built = build_lur_start_session(repository=ROOT, controller=LurStartController())
    names = {item.name for item in fields(LurStartSessionEnvironment)}
    assert "controller_source_identity" in names
    assert "active_fault" not in names
    assert "evaluator_readback" not in names
    assert {item.path for item in built.adapter_source_identity.files} == {
        "src/cltav_615a_adapter/__init__.py",
        "src/cltav_615a_adapter/identity.py",
        "src/cltav_615a_adapter/contract.py",
        "src/cltav_615a_adapter/session.py",
    }


def test_c01_nested_hb_contract_cannot_mutate_a_real_list_only_successor() -> None:
    """The Git-bound contract must not expose a writable nested JSON alias."""

    contract = load_hb_session_contract(ROOT)
    outcomes = contract.action(INSPECT_ACTION_ID)["possibleOutcomes"]
    assert isinstance(outcomes, tuple)
    with pytest.raises(TypeError):
        outcomes[0]["postSummary"] = "Q-TARGET-READY"
    with pytest.raises(TypeError):
        contract.package["actionLibrary"][0]["possibleOutcomes"][0]["postSummary"] = "Q-TARGET-READY"

    # This is the actual C production path, not a synthetic outcome lookup:
    # one LIST-only finite inspection must retain its declared pre-READY
    # successor and cannot be escalated to the later READY summary.
    built = build_lur_start_session(repository=ROOT, controller=LurStartController())
    first = built.session.step(built.session.initial_state, built.environment)
    assert first.state.context.current_summary == "Q-PRE-READY-NO-WRQ"
    assert [event.kind for event in first.environment.protocol_snapshot.events] == [
        "LIST-SUBMISSION-PRECONDITION-RECORDED",
    ]


def test_c02_normal_real_multiround_loop_preserves_plural_h_then_selects_order() -> None:
    built = build_lur_start_session(repository=ROOT, controller=LurStartController())
    first = built.session.step(built.session.initial_state, built.environment)
    assert first.stop_reason is None
    assert first.state.context.current_summary == "Q-PRE-READY-NO-WRQ"
    assert first.state.history.hypotheses == frozenset({"NORMAL", "EARLY-DATA"})
    assert [event.kind for event in first.environment.protocol_snapshot.events] == [
        "LIST-SUBMISSION-PRECONDITION-RECORDED",
    ]

    second = built.session.step(first.state, first.environment)
    assert second.stop_reason is None
    assert second.state.context.current_summary == "Q-TARGET-READY"
    assert second.state.history.hypotheses == frozenset({"NORMAL", "EARLY-DATA"})
    assert second.state.history.version == first.state.history.version + 1
    assert [event.kind for event in second.environment.protocol_snapshot.events] == [
        "LIST-SUBMISSION-PRECONDITION-RECORDED", "EV_TH_LUS0001",
    ]

    third = built.session.step(second.state, second.environment)
    assert third.stop_reason == "Stop-Singleton"
    assert third.state.history.hypotheses == frozenset({"NORMAL"})
    assert [event.kind for event in third.environment.protocol_snapshot.events] == [
        "LIST-SUBMISSION-PRECONDITION-RECORDED", "EV_TH_LUS0001",
        "EV_DL_WRQ_LUR", "EV_TH_ACK_LUR", "EV_DL_DATA_LUR",
    ]


def test_c02_public_adapter_is_deterministic_without_predictor_or_evaluator_ingress() -> None:
    """Same public object stimulus cannot be altered by hidden C inputs."""

    left = build_lur_start_session(repository=ROOT, controller=LurStartController())
    right = build_lur_start_session(repository=ROOT, controller=LurStartController())
    left_result = left.session.run(left.environment, maximum_rounds=4)
    right_result = right.session.run(right.environment, maximum_rounds=4)

    assert left_result.stop_reason == right_result.stop_reason == "Stop-Singleton"
    assert [event.kind for event in left_result.environment.protocol_snapshot.events] == [
        event.kind for event in right_result.environment.protocol_snapshot.events
    ]
    assert [event.sequence_number for event in left_result.environment.protocol_snapshot.events] == [
        event.sequence_number for event in right_result.environment.protocol_snapshot.events
    ]
    assert left_result.state.history.hypotheses == right_result.state.history.hypotheses
    assert left_result.state.history.status_by_hypothesis == right_result.state.history.status_by_hypothesis
    assert left_result.state.context.current_summary == right_result.state.context.current_summary
    assert left_result.state.resources == right_result.state.resources
    adapter_field_names = {item.name.lower() for item in fields(LurStartSessionEnvironment)}
    assert not {"predictor", "evaluator", "candidate", "active_fault"} & adapter_field_names


def test_c03_three_variants_use_the_same_public_microstep_strategy() -> None:
    normal = build_lur_start_session(repository=ROOT, controller=LurStartController())
    n1 = normal.session.step(normal.session.initial_state, normal.environment)
    n2 = normal.session.step(n1.state, n1.environment)
    n3 = normal.session.step(n2.state, n2.environment)
    assert n3.state.history.hypotheses == frozenset({"NORMAL"})

    early_wrq_controller = LurStartController()
    assert early_wrq_controller.install_fault(FaultVariant.EARLY_WRQ).status.name == "INSTALLED"
    early_wrq = build_lur_start_session(repository=ROOT, controller=early_wrq_controller)
    wrq_round = early_wrq.session.step(early_wrq.session.initial_state, early_wrq.environment)
    assert wrq_round.stop_reason == "Stop-Singleton"
    assert wrq_round.state.history.hypotheses == frozenset({"EARLY-WRQ"})
    assert [event.kind for event in wrq_round.environment.protocol_snapshot.events] == [
        "LIST-SUBMISSION-PRECONDITION-RECORDED", "EV_DL_WRQ_LUR",
    ]

    early_data_controller = LurStartController()
    assert early_data_controller.install_fault(FaultVariant.EARLY_DATA).status.name == "INSTALLED"
    early_data = build_lur_start_session(repository=ROOT, controller=early_data_controller)
    d1 = early_data.session.step(early_data.session.initial_state, early_data.environment)
    d2 = early_data.session.step(d1.state, d1.environment)
    d3 = early_data.session.step(d2.state, d2.environment)
    assert d3.state.history.hypotheses == frozenset({"EARLY-DATA"})
    events = d3.environment.protocol_snapshot.events
    data = next(event for event in events if event.kind == "EV_DL_DATA_LUR")
    ack = next(event for event in events if event.kind == "EV_TH_ACK_LUR")
    assert data.tick == ack.tick
    assert data.sequence_number < ack.sequence_number
    assert ack.in_reply_to_event_id == next(event for event in events if event.kind == "EV_DL_WRQ_LUR").event_id
    projection = d3.environment.ownership_projections[-1]
    assert projection.trigger_event_id == next(event for event in events if event.kind == "EV_DL_WRQ_LUR").event_id
    assert projection.response_event_id == ack.event_id
    assert projection.response_in_reply_to_event_id == projection.trigger_event_id


def test_c04_predecessor_adapter_and_controller_are_not_mutated_by_successor() -> None:
    built = build_lur_start_session(repository=ROOT, controller=LurStartController())
    predecessor = built.environment
    predecessor_snapshot = predecessor.protocol_snapshot
    first = built.session.step(built.session.initial_state, predecessor)
    successor = first.environment
    assert isinstance(successor, LurStartSessionEnvironment)
    assert id(predecessor.controller) != id(successor.controller)
    assert predecessor.protocol_snapshot == predecessor_snapshot
    assert predecessor.controller.public_snapshot() == predecessor_snapshot
    assert len(successor.protocol_snapshot.events) > len(predecessor_snapshot.events)


def test_c04_completed_no_wrq_check_is_a_typed_nonempty_engineering_observation() -> None:
    """The finite pre-READY check is neither a timeout nor an empty symbol."""

    built = build_lur_start_session(repository=ROOT, controller=LurStartController())
    result = built.session.step(built.session.initial_state, built.environment)
    assert result.stop_reason is None
    environment = result.environment
    assert isinstance(environment, LurStartSessionEnvironment)
    assert len(environment.finite_checks) == 1
    assert len(environment.completed_receipts) == 1
    check = environment.finite_checks[-1]
    receipt = environment.completed_receipts[-1]
    assert check.observable == "NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001"
    assert check.receipt.completed is True
    assert receipt.completed is True
    assert len(receipt.event_ids) == 1
    assert receipt.event_ids[0].endswith(":event-0001")
    assert check.receipt.event_ids == receipt.event_ids
    assert result.state.evidence[-1].execution.observable == check.observable
    assert "TIMEOUT" not in check.observable


def test_c04_missing_completion_receipt_is_unknown_not_a_confirmed_observation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A finite predicate without its current receipt cannot reach S9."""

    monkeypatch.setattr(
        LurStartSessionEnvironment,
        "_completed_receipt",
        staticmethod(lambda controller, snapshot, label: None),
    )
    built = build_lur_start_session(repository=ROOT, controller=LurStartController(), retry_cap=2)
    result = built.session.step(built.session.initial_state, built.environment)

    assert result.stop_reason is None
    assert result.state.evidence[-1].execution.effect_class == "UNKNOWN-EFFECT"
    assert result.state.context.q_status == "UNKNOWN"
    assert result.state.context.current_summary is None
    assert result.state.history.hypotheses == built.session.initial_state.history.hypotheses
    assert set(result.state.history.status_by_hypothesis.values()) == {"CONSERVATIVE-UNKNOWN"}
    assert isinstance(result.environment, LurStartSessionEnvironment)
    assert len(result.environment.finite_checks) == 1
    assert not result.environment.completed_receipts
    assert any(item.code == "UNKNOWN-EFFECT" for item in result.diagnostics)


def test_c05_ready_emission_delayed_until_after_early_wrq_never_confirms_recover() -> None:
    controller = LurStartController()
    assert controller.install_fault(FaultVariant.EARLY_WRQ).status.name == "INSTALLED"
    assert controller.record_list_submission_precondition().accepted
    assert controller.deliver_next().accepted
    emitted_ready = controller.emit_target_lus_ready()
    assert emitted_ready.accepted and emitted_ready.event is not None
    emitted_wrq = controller.advance_loader()
    assert emitted_wrq.accepted and emitted_wrq.event is not None
    deliveries = controller.deliver_all()
    assert [item.accepted for item in deliveries] == [False, True]
    # The protocol journal contains READY then WRQ, but READY was rejected by
    # its peer.  There is deliberately no C application evidence to turn this
    # emitted event into Q-TARGET-READY.
    environment = LurStartSessionEnvironment.from_controller(
        controller=controller,
        contract=load_hb_session_contract(ROOT),
    )
    execution = environment.execute(_request(
        environment, RECOVER_ACTION_ID, "RECOVER", "recover-delayed-ready",
    ))
    assert execution.record.prep_recover is not None
    assert execution.record.prep_recover.target_confirmed is False
    assert execution.record.prep_recover.summary_confirmed is False
    assert execution.successor.protocol_snapshot == environment.protocol_snapshot
    assert not execution.successor.tool_readbacks


def test_c05_session_clears_known_state_when_ready_application_is_unconfirmed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A sent Prep with no confirmed application follows S7, not stale KNOWN."""

    original = LurStartSessionEnvironment._applied_delivery

    def reject_ready(*, controller, request, expected, adapter_identity):
        applied = original(
            controller=controller,
            request=request,
            expected=expected,
            adapter_identity=adapter_identity,
        )
        return None if expected.kind == "EV_TH_LUS0001" else applied

    monkeypatch.setattr(
        LurStartSessionEnvironment,
        "_applied_delivery",
        staticmethod(reject_ready),
    )
    built = build_lur_start_session(
        repository=ROOT,
        controller=LurStartController(),
        retry_cap=2,
    )
    first = built.session.step(built.session.initial_state, built.environment)
    second = built.session.step(first.state, first.environment)

    assert second.stop_reason is None
    # The B action was sent, so the typed record remains a normal execution
    # carrier; its false confirmation is what forces the session's S7
    # conservative UNKNOWN transition.
    assert second.state.evidence[-1].execution.effect_class == "NONE"
    assert second.state.evidence[-1].execution.prep_recover is not None
    assert second.state.evidence[-1].execution.prep_recover.summary_confirmed is False
    assert second.state.context.q_status == "UNKNOWN"
    assert second.state.context.current_summary is None
    assert second.state.context.known_target is None
    assert second.state.history.hypotheses == first.state.history.hypotheses
    assert set(second.state.history.status_by_hypothesis.values()) == {"CONSERVATIVE-UNKNOWN"}
    assert second.state.evidence[-1].resolution_code == "PREP-SUMMARY-UNCONFIRMED"


def test_c06_recover_is_non_emitting_and_order_continues_only_with_data() -> None:
    _built, _state, environment = _normal_after_prep()
    original = environment.protocol_snapshot
    recovered = environment.execute(_request(environment, RECOVER_ACTION_ID, "RECOVER", "recover-current"))
    assert recovered.record.prep_recover is not None
    assert recovered.record.prep_recover.target_confirmed is True
    assert recovered.record.prep_recover.summary_confirmed is True
    successor = recovered.successor
    assert successor.protocol_snapshot == original
    assert len(successor.tool_readbacks) == 1
    assert isinstance(successor.tool_readbacks[0], ToolReadbackEvidence)

    # A subsequent real order Test is still responsible for WRQ/ACK/DATA;
    # Recover itself neither replays nor emits a protocol event.
    ordered = successor.execute(_request(successor, ORDER_ACTION_ID, "TEST", "order-after-recover"))
    assert [event.kind for event in ordered.successor.protocol_snapshot.events][-3:] == [
        "EV_DL_WRQ_LUR", "EV_TH_ACK_LUR", "EV_DL_DATA_LUR",
    ]


@pytest.mark.parametrize("withheld_kind", [
    "EV_DL_WRQ_LUR",
    "EV_TH_ACK_LUR",
    "EV_DL_DATA_LUR",
])
@pytest.mark.parametrize(
    ("variant", "expected_observable", "expected_order", "resumed_delivery_expectations"),
    [
        (
            "NORMAL",
            "WRQ-ACK-DATA-IN-ORDER",
            ["EV_DL_WRQ_LUR", "EV_TH_ACK_LUR", "EV_DL_DATA_LUR"],
            {
                "EV_DL_WRQ_LUR": ["EV_DL_WRQ_LUR", "EV_TH_ACK_LUR", "EV_DL_DATA_LUR"],
                "EV_TH_ACK_LUR": ["EV_TH_ACK_LUR", "EV_DL_DATA_LUR"],
                "EV_DL_DATA_LUR": ["EV_DL_DATA_LUR"],
            },
        ),
        (
            "EARLY-DATA",
            "DATA-BEFORE-MATCHING-ACK",
            ["EV_DL_WRQ_LUR", "EV_DL_DATA_LUR", "EV_TH_ACK_LUR"],
            {
                "EV_DL_WRQ_LUR": ["EV_DL_WRQ_LUR", "EV_DL_DATA_LUR", "EV_TH_ACK_LUR"],
                "EV_TH_ACK_LUR": ["EV_TH_ACK_LUR"],
                "EV_DL_DATA_LUR": ["EV_DL_DATA_LUR", "EV_TH_ACK_LUR"],
            },
        ),
    ],
)
def test_c06_recover_continuation_delivers_each_original_pending_order_event(
    monkeypatch: pytest.MonkeyPatch,
    withheld_kind: str,
    variant: str,
    expected_observable: str,
    expected_order: list[str],
    resumed_delivery_expectations: dict[str, list[str]],
) -> None:
    """Each recorded WRQ/ACK/DATA event needs its own FIFO application proof."""

    original_delivery = LurStartSessionEnvironment._applied_delivery
    withheld = False

    def withhold_once_before_application(*, controller, request, expected, adapter_identity):
        nonlocal withheld
        if expected.kind == withheld_kind and not withheld:
            withheld = True
            # Do not call the B delivery operation: the actual event remains
            # at its original FIFO position, while its journal record proves
            # only emission.  This is a real boundary failure, not a replay.
            return None
        return original_delivery(
            controller=controller,
            request=request,
            expected=expected,
            adapter_identity=adapter_identity,
        )

    monkeypatch.setattr(
        LurStartSessionEnvironment,
        "_applied_delivery",
        staticmethod(withhold_once_before_application),
    )
    controller = LurStartController()
    if variant == "EARLY-DATA":
        assert controller.install_fault(FaultVariant.EARLY_DATA).status.name == "INSTALLED"
    built = build_lur_start_session(
        repository=ROOT,
        controller=controller,
        resources=ResourceState.rounds(8),
        retry_cap=4,
    )
    first = built.session.step(built.session.initial_state, built.environment)
    second = built.session.step(first.state, first.environment)
    unknown = built.session.step(second.state, second.environment)
    assert withheld is True
    assert unknown.state.context.q_status == "UNKNOWN"
    assert unknown.state.evidence[-1].execution.effect_class == "UNKNOWN-EFFECT"
    emitted = next(
        event for event in unknown.environment.protocol_snapshot.events
        if event.kind == withheld_kind
    )
    assert not any(item.event_id == emitted.event_id for item in unknown.environment.applied_deliveries)

    # Recover is deliberately non-emitting and re-establishes only the typed
    # READY basis.  The next actual TEST must therefore FIFO-deliver the
    # original pending event, not mint/replay it or treat emission as proof.
    monkeypatch.setattr(
        LurStartSessionEnvironment,
        "_applied_delivery",
        staticmethod(original_delivery),
    )
    recovered = built.session.step(unknown.state, unknown.environment)
    assert recovered.state.context.q_status == "KNOWN"
    assert recovered.state.context.current_summary == "Q-TARGET-READY"
    before_resume = recovered.environment.protocol_snapshot
    assert emitted in before_resume.events

    resumed_delivery_kinds: list[str] = []

    def record_resumed_delivery(*, controller, request, expected, adapter_identity):
        resumed_delivery_kinds.append(expected.kind)
        return original_delivery(
            controller=controller,
            request=request,
            expected=expected,
            adapter_identity=adapter_identity,
        )

    monkeypatch.setattr(
        LurStartSessionEnvironment,
        "_applied_delivery",
        staticmethod(record_resumed_delivery),
    )
    resumed = recovered.environment.execute(_request(
        recovered.environment, ORDER_ACTION_ID, "TEST", f"resume-{variant}-{withheld_kind}",
    ))
    assert resumed.record.effect_class == "NONE"
    assert resumed.record.observable == expected_observable
    assert resumed.record.summary_confirmed is True
    events = resumed.successor.protocol_snapshot.events
    assert [event for event in events if event.kind == withheld_kind] == [emitted]
    assert any(item.event_id == emitted.event_id for item in resumed.successor.applied_deliveries)
    assert [event.kind for event in events][-3:] == expected_order
    assert resumed_delivery_kinds == resumed_delivery_expectations[withheld_kind]

    # Recover truthfully re-confirms q from its qualified public basis but
    # must not promote the S7-conservative H.  With ample remaining ROUNDS,
    # the full coordinator therefore reports its named prediction gap without
    # dispatching/replaying any event.  The direct adapter continuation above
    # separately proves that the real FIFO successor itself is available.
    assert set(recovered.state.history.status_by_hypothesis.values()) == {
        "CONSERVATIVE-UNKNOWN",
    }
    terminal = built.session.step(recovered.state, recovered.environment)
    assert terminal.stop_reason == "Stop-Prediction-Gap"
    assert terminal.environment.protocol_snapshot == before_resume
    assert terminal.state.resources.remaining > 0
    assert {item.code for item in terminal.diagnostics} >= {
        "CONSERVATIVE-PREDICTION-GAP", "PREDICTION-GAP",
    }


def test_c06_unknown_session_admits_only_qualified_current_recover(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A prior READY application can be recovered only after S7 made q UNKNOWN."""

    original_outcome = session_adapter_module.action_outcome

    def unconfirmed_prep(contract, action_id, observable):
        outcome = original_outcome(contract, action_id, observable)
        if action_id == PREP_ACTION_ID:
            return {**outcome, "postSummary": None}
        return outcome

    built = build_lur_start_session(
        repository=ROOT,
        controller=LurStartController(),
        retry_cap=2,
    )
    first = built.session.step(built.session.initial_state, built.environment)
    monkeypatch.setattr(session_adapter_module, "action_outcome", unconfirmed_prep)
    unknown = built.session.step(first.state, first.environment)
    assert unknown.state.context.q_status == "UNKNOWN"
    assert unknown.environment.applied_deliveries
    monkeypatch.setattr(session_adapter_module, "action_outcome", original_outcome)

    recovered = built.session.step(unknown.state, unknown.environment)
    assert recovered.stop_reason is None
    assert recovered.state.evidence[-1].execution.action_id == RECOVER_ACTION_ID
    assert recovered.state.evidence[-1].execution.prep_recover is not None
    assert recovered.state.evidence[-1].execution.prep_recover.summary_confirmed is True
    assert recovered.state.context.q_status == "KNOWN"
    assert recovered.state.context.current_summary == "Q-TARGET-READY"

    # Recover itself remains non-emitting.  Its returned adapter can drive the
    # remaining declared FIFO order phase, but S7's conservative H is never
    # silently promoted merely because q was re-confirmed.
    continued = recovered.environment.execute(_request(
        recovered.environment, ORDER_ACTION_ID, "TEST", "recover-known-order-continuation",
    ))
    assert continued.record.effect_class == "NONE"
    assert continued.record.observable == "WRQ-ACK-DATA-IN-ORDER"
    assert [event.kind for event in continued.successor.protocol_snapshot.events][-3:] == [
        "EV_DL_WRQ_LUR", "EV_TH_ACK_LUR", "EV_DL_DATA_LUR",
    ]
    terminal = built.session.step(recovered.state, recovered.environment)
    assert terminal.stop_reason == "Stop-Prediction-Gap"
    assert set(terminal.state.history.status_by_hypothesis.values()) == {
        "CONSERVATIVE-UNKNOWN",
    }


def test_c07_recover_rejects_missing_or_duplicate_public_tool_basis() -> None:
    _built, _state, environment = _normal_after_prep()
    missing = LurStartSessionEnvironment(
        _state=environment._state,
        _uncertainty_identity=environment._uncertainty_identity,
        _states=environment._states,
        _pending_delivery=None,
        controller=environment.controller,
        contract=environment.contract,
        checkpoint=environment.checkpoint,
        adapter_source_identity=environment.adapter_source_identity,
        controller_source_identity=environment.controller_source_identity,
    )
    no_basis = missing.execute(_request(missing, RECOVER_ACTION_ID, "RECOVER", "recover-no-basis"))
    assert no_basis.record.prep_recover is not None
    assert no_basis.record.prep_recover.summary_confirmed is False

    succeeded = environment.execute(_request(environment, RECOVER_ACTION_ID, "RECOVER", "recover-once"))
    repeated = succeeded.successor.execute(_request(
        succeeded.successor, RECOVER_ACTION_ID, "RECOVER", "recover-once",
    ))
    assert repeated.record.prep_recover is not None
    assert repeated.record.prep_recover.summary_confirmed is False


def test_c07_confirmed_not_sent_and_issued_unknown_have_distinct_causal_outcomes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A stale preflight refusal is not a sent-but-unconfirmed C execution."""

    not_sent = build_lur_start_session(
        repository=ROOT,
        controller=LurStartController(),
        retry_cap=2,
    )
    assert not_sent.environment.controller.full_reset().success
    refused = not_sent.session.step(not_sent.session.initial_state, not_sent.environment)
    assert refused.state.evidence[-1].execution.effect_class == "CONFIRMED-NOT-SENT"
    assert refused.state.context.q_status == "KNOWN"
    assert refused.state.history == not_sent.session.initial_state.history
    assert any(item.code == "CONFIRMED-NOT-SENT" for item in refused.diagnostics)

    original_outcome = session_adapter_module.action_outcome

    def fail_after_send(contract, action_id, observable):
        outcome = original_outcome(contract, action_id, observable)
        if action_id == INSPECT_ACTION_ID:
            return {**outcome, "postSummary": None}
        return outcome

    issued = build_lur_start_session(
        repository=ROOT,
        controller=LurStartController(),
        retry_cap=2,
    )
    monkeypatch.setattr(session_adapter_module, "action_outcome", fail_after_send)
    unresolved = issued.session.step(issued.session.initial_state, issued.environment)
    assert unresolved.state.evidence[-1].execution.effect_class == "UNKNOWN-EFFECT"
    assert unresolved.state.context.q_status == "UNKNOWN"
    assert unresolved.state.history != issued.session.initial_state.history
    assert any(item.code == "UNKNOWN-EFFECT" for item in unresolved.diagnostics)


def test_c08_resource_refusal_is_pre_dispatch_and_keeps_real_object_unchanged() -> None:
    built = build_lur_start_session(
        repository=ROOT,
        controller=LurStartController(),
        resources=ResourceState.rounds(0),
    )
    before = built.environment.protocol_snapshot
    result = built.session.step(built.session.initial_state, built.environment)
    assert result.stop_reason == "Stop-Budget"
    assert result.environment.protocol_snapshot == before


def test_c08_frozen_uncertainty_identity_rejects_a_tampered_visible_record(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A C adapter cannot substitute a different U after S3 has frozen it."""

    built = build_lur_start_session(repository=ROOT, controller=LurStartController())
    original_execute = LurStartSessionEnvironment.execute

    def drift_u(
        environment: LurStartSessionEnvironment,
        request: ExecutionRequest,
    ) -> EnvironmentExecution:
        execution = original_execute(environment, request)
        return EnvironmentExecution(
            replace(execution.record, uncertainty_identity="U-FORGED-C-ADAPTER"),
            execution.successor,
        )

    monkeypatch.setattr(LurStartSessionEnvironment, "execute", drift_u)
    result = built.session.step(built.session.initial_state, built.environment)
    # The accepted runtime retains a charged, actual successor through S7;
    # it must never treat the forged U as an S9 commitment.  Consequently H
    # stays intact while the immutable history records conservative UNKNOWN
    # rather than advancing to the selected visible class.
    assert result.state.history.hypotheses == built.session.initial_state.history.hypotheses
    assert result.state.context.q_status == "UNKNOWN"
    assert result.state.evidence[-1].committed is False
    assert set(result.state.history.status_by_hypothesis.values()) == {"CONSERVATIVE-UNKNOWN"}
    assert any(item.code == "UNCERTAINTY-SNAPSHOT-MISMATCH" for item in result.diagnostics)


def test_c11_rounds_and_budget_are_distinct_pre_dispatch_admission_modes() -> None:
    """Both resource modes refuse before a real controller mutation occurs."""

    rounds = build_lur_start_session(
        repository=ROOT,
        controller=LurStartController(),
        resources=ResourceState.rounds(2),
    )
    r1 = rounds.session.step(rounds.session.initial_state, rounds.environment)
    r2 = rounds.session.step(r1.state, r1.environment)
    before_round_refusal = r2.environment.protocol_snapshot
    r3 = rounds.session.step(r2.state, r2.environment)
    assert r1.state.resources == ResourceState.rounds(1)
    assert r2.state.resources == ResourceState.rounds(0)
    assert r3.stop_reason == "Stop-Budget"
    assert r3.environment.protocol_snapshot == before_round_refusal

    budget = build_lur_start_session(
        repository=ROOT,
        controller=LurStartController(),
        resources=ResourceState.budget(3),
    )
    b1 = budget.session.step(budget.session.initial_state, budget.environment)
    before_budget_refusal = b1.environment.protocol_snapshot
    b2 = budget.session.step(b1.state, b1.environment)
    assert b1.state.resources == ResourceState.budget(1)
    assert b2.stop_reason == "Stop-Budget"
    assert b2.environment.protocol_snapshot == before_budget_refusal


def test_c12_terminal_stop_does_not_drive_the_real_object_again() -> None:
    """A singleton result ends execution rather than filling out a timeline."""

    built = build_lur_start_session(repository=ROOT, controller=LurStartController())
    first = built.session.step(built.session.initial_state, built.environment)
    second = built.session.step(first.state, first.environment)
    terminal = built.session.step(second.state, second.environment)
    assert terminal.stop_reason == "Stop-Singleton"
    before = terminal.environment.protocol_snapshot
    retained = built.session.step(terminal.state, terminal.environment)
    assert retained.stop_reason == "Stop-Singleton"
    assert retained.environment.protocol_snapshot == before


def test_c13_explicit_full_reset_is_a_new_setup_not_recover_or_replay() -> None:
    """Only an explicit B reset may create a fresh adapter/session boundary."""

    controller = LurStartController()
    first = build_lur_start_session(repository=ROOT, controller=controller)
    progressed = first.session.step(first.session.initial_state, first.environment)
    assert progressed.environment.protocol_snapshot.events
    old_reset = progressed.environment.protocol_snapshot.reset_id

    # Reset is driven only as independent setup.  The old adapter remains
    # stale and cannot issue a fresh action into the reset controller.
    assert progressed.environment.controller.full_reset().success
    stale = progressed.environment.execute(_request(
        progressed.environment, INSPECT_ACTION_ID, "TEST", "old-before-reset",
    ))
    assert stale.record.effect_class == "CONFIRMED-NOT-SENT"

    fresh = build_lur_start_session(repository=ROOT, controller=progressed.environment.controller)
    assert fresh.environment.protocol_snapshot.reset_id != old_reset
    again = fresh.session.step(fresh.session.initial_state, fresh.environment)
    assert again.stop_reason is None
    assert again.environment.protocol_snapshot.events

    failed_reset = build_lur_start_session(repository=ROOT, controller=LurStartController())
    failure = failed_reset.environment.controller.full_reset(force_revocation_failure=True)
    assert failure.success is False
    refused = failed_reset.session.step(
        failed_reset.session.initial_state,
        failed_reset.environment,
    )
    assert refused.state.evidence[-1].execution.effect_class == "CONFIRMED-NOT-SENT"
    assert refused.state.context.q_status == "KNOWN"
    assert refused.state.history == failed_reset.session.initial_state.history


def test_c14_adapter_keeps_the_declared_non_integrity_boundary() -> None:
    """This finite adapter must not silently claim a full UPLOAD capability."""

    package = json.loads(
        (ROOT / "configs/engineering/cltav_615a_scenarios.json").read_text(encoding="utf-8")
    )
    acceptance = package["sessionIntegration"]["productionAcceptance"]
    non_claim = acceptance["notEstablished"].lower()
    assert all(token in non_claim for token in ("iut", "protocol", "full upload", "experiment"))
    assert set(package["scope"]["notEvaluatedObligations"]) >= {
        "FULL-UPLOAD-COMPLETION",
        "LUR-PAYLOAD-INTEGRITY",
        "CRC-CHECK-VALUE-NAMING-CAPABILITY",
        "PROTOCOL-NO-RESPONSE-DEADLINE",
    }
    order = next(
        row for row in package["actionLibrary"] if row["id"] == ORDER_ACTION_ID
    )
    assert set(order["nonEvaluatedObligations"]) == {
        "LUR-PAYLOAD-INTEGRITY",
        "FULL-UPLOAD-COMPLETION",
    }
    contract = load_hb_session_contract(ROOT)
    assert set(contract.action_by_id) == {
        INSPECT_ACTION_ID,
        PREP_ACTION_ID,
        ORDER_ACTION_ID,
        RECOVER_ACTION_ID,
    }
    assert "INTEGRITY" not in " ".join(contract.action_by_id)


def test_c11_recover_is_charged_once_with_its_declared_cost_projection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A qualified Recover is a real one-round charge, not a free retry."""

    original_outcome = session_adapter_module.action_outcome

    def unconfirmed_prep(contract, action_id, observable):
        outcome = original_outcome(contract, action_id, observable)
        if action_id == PREP_ACTION_ID:
            return {**outcome, "postSummary": None}
        return outcome

    built = build_lur_start_session(
        repository=ROOT,
        controller=LurStartController(),
        resources=ResourceState.rounds(3),
        retry_cap=2,
    )
    inspected = built.session.step(built.session.initial_state, built.environment)
    monkeypatch.setattr(session_adapter_module, "action_outcome", unconfirmed_prep)
    unknown = built.session.step(inspected.state, inspected.environment)
    monkeypatch.setattr(session_adapter_module, "action_outcome", original_outcome)
    recovered = built.session.step(unknown.state, unknown.environment)

    recover_evidence = recovered.state.evidence[-1]
    declared = built.session.model.actions[RECOVER_ACTION_ID]
    assert recover_evidence.execution.action_id == RECOVER_ACTION_ID
    assert recover_evidence.detail_charges == declared.detail_charges
    assert recover_evidence.projected_cost == declared.projected_cost()
    assert recover_evidence.resource_before.remaining == 1
    assert recover_evidence.resource_after.remaining == 0
    assert recovered.state.resources == ResourceState.rounds(0)


def test_c15_real_public_timelines_match_independent_expected_sequences() -> None:
    """Check hand-readable normal and fault timelines against real logs."""

    normal = build_lur_start_session(repository=ROOT, controller=LurStartController())
    n1 = normal.session.step(normal.session.initial_state, normal.environment)
    n2 = normal.session.step(n1.state, n1.environment)
    n3 = normal.session.step(n2.state, n2.environment)
    assert [event.kind for event in n3.environment.protocol_snapshot.events] == [
        "LIST-SUBMISSION-PRECONDITION-RECORDED",
        "EV_TH_LUS0001",
        "EV_DL_WRQ_LUR",
        "EV_TH_ACK_LUR",
        "EV_DL_DATA_LUR",
    ]

    early_wrq_controller = LurStartController()
    assert early_wrq_controller.install_fault(FaultVariant.EARLY_WRQ).status.name == "INSTALLED"
    early_wrq = build_lur_start_session(repository=ROOT, controller=early_wrq_controller)
    w1 = early_wrq.session.step(early_wrq.session.initial_state, early_wrq.environment)
    assert [event.kind for event in w1.environment.protocol_snapshot.events] == [
        "LIST-SUBMISSION-PRECONDITION-RECORDED",
        "EV_DL_WRQ_LUR",
    ]

    early_data_controller = LurStartController()
    assert early_data_controller.install_fault(FaultVariant.EARLY_DATA).status.name == "INSTALLED"
    early_data = build_lur_start_session(repository=ROOT, controller=early_data_controller)
    d1 = early_data.session.step(early_data.session.initial_state, early_data.environment)
    d2 = early_data.session.step(d1.state, d1.environment)
    d3 = early_data.session.step(d2.state, d2.environment)
    assert [event.kind for event in d3.environment.protocol_snapshot.events] == [
        "LIST-SUBMISSION-PRECONDITION-RECORDED",
        "EV_TH_LUS0001",
        "EV_DL_WRQ_LUR",
        "EV_DL_DATA_LUR",
        "EV_TH_ACK_LUR",
    ]


def test_c15_unknown_recover_timeline_is_nonemitting_and_retains_current_prefix(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The hand-written UNKNOWN continuation has no hidden protocol replay."""

    original_outcome = session_adapter_module.action_outcome

    def unconfirmed_prep(contract, action_id, observable):
        outcome = original_outcome(contract, action_id, observable)
        if action_id == PREP_ACTION_ID:
            return {**outcome, "postSummary": None}
        return outcome

    built = build_lur_start_session(
        repository=ROOT,
        controller=LurStartController(),
        retry_cap=2,
    )
    first = built.session.step(built.session.initial_state, built.environment)
    monkeypatch.setattr(session_adapter_module, "action_outcome", unconfirmed_prep)
    unknown = built.session.step(first.state, first.environment)
    prefix_before_recover = tuple(
        event.kind for event in unknown.environment.protocol_snapshot.events
    )
    assert prefix_before_recover == (
        "LIST-SUBMISSION-PRECONDITION-RECORDED", "EV_TH_LUS0001",
    )
    monkeypatch.setattr(session_adapter_module, "action_outcome", original_outcome)

    recovered = built.session.step(unknown.state, unknown.environment)
    assert recovered.state.evidence[-1].execution.action_id == RECOVER_ACTION_ID
    assert tuple(event.kind for event in recovered.environment.protocol_snapshot.events) == prefix_before_recover
    assert len(recovered.environment.tool_readbacks) == 1


def test_c16_fixed_hb_source_is_required_at_the_production_entry(tmp_path: Path) -> None:
    """An arbitrary worktree cannot substitute for the fixed accepted input."""

    with pytest.raises(ValueError, match="controlled source Git object cannot be loaded"):
        load_hb_session_contract(tmp_path)


def test_c16_pre_driven_or_stale_object_is_rejected_without_new_public_drive() -> None:
    """C only accepts a fresh setup and never consumes a stale continuation."""

    pre_driven = LurStartController()
    assert pre_driven.record_list_submission_precondition().accepted
    assert pre_driven.deliver_next().accepted
    with pytest.raises(SessionAdapterError, match="INITIAL-OBJECT-MUST-BE-FRESH"):
        build_lur_start_session(repository=ROOT, controller=pre_driven)

    built = build_lur_start_session(repository=ROOT, controller=LurStartController())
    stale = built.environment
    assert stale.controller.full_reset().success
    before = stale.controller.public_snapshot()
    result = stale.execute(_request(
        stale, INSPECT_ACTION_ID, "TEST", "stale-production-entry",
    ))
    assert result.record.effect_class == "CONFIRMED-NOT-SENT"
    assert result.successor is stale
    assert stale.controller.public_snapshot() == before


def test_c16_stale_checkpoint_or_wrong_visible_action_cannot_be_consumed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """C rejects both a stale real-object predecessor and a forged public carrier."""

    stale = build_lur_start_session(repository=ROOT, controller=LurStartController())
    assert stale.environment.controller.record_list_submission_precondition().accepted
    stale_result = stale.session.step(stale.session.initial_state, stale.environment)
    assert stale_result.state.evidence[-1].execution.effect_class == "CONFIRMED-NOT-SENT"
    assert stale_result.state.history == stale.session.initial_state.history
    assert stale_result.state.context.current_summary == "SCENE-ENTRY"
    assert any(item.code == "CONFIRMED-NOT-SENT" for item in stale_result.diagnostics)

    original_execute = LurStartSessionEnvironment.execute

    def wrong_visible_action(
        environment: LurStartSessionEnvironment,
        request: ExecutionRequest,
    ) -> EnvironmentExecution:
        execution = original_execute(environment, request)
        return EnvironmentExecution(
            replace(execution.record, action_id=PREP_ACTION_ID),
            execution.successor,
        )

    monkeypatch.setattr(LurStartSessionEnvironment, "execute", wrong_visible_action)
    forged = build_lur_start_session(repository=ROOT, controller=LurStartController(), retry_cap=2)
    rejected = forged.session.step(forged.session.initial_state, forged.environment)
    assert rejected.state.context.q_status == "UNKNOWN"
    assert rejected.state.context.current_summary is None
    assert rejected.state.history.hypotheses == forged.session.initial_state.history.hypotheses
    assert any(item.code == "EXECUTION-IDENTITY-ERROR" for item in rejected.diagnostics)


def test_c09_adapter_uses_the_controlled_unique_key_ownership_contract() -> None:
    built = build_lur_start_session(repository=ROOT, controller=LurStartController())
    first = built.session.step(built.session.initial_state, built.environment)
    second = built.session.step(first.state, first.environment)
    third = built.session.step(second.state, second.environment)
    assert third.stop_reason == "Stop-Singleton"
    # The no-WRQ inspection is not an ownership response.  Ownership starts
    # only once actual B WRQ/ACK public events exist in the order TEST.
    assert not first.environment.ownership_projections
    assert third.environment.ownership_projections
    projection = third.environment.ownership_projections[-1]
    assert projection.ownership_contract_id == C_OWNERSHIP_CONTRACT_ID
    assert projection.ownership_policy == "UNIQUE-KEY"
    assert projection.protocol_event_ids == tuple(
        event.event_id for event in third.environment.protocol_snapshot.events
    )
    wrq = next(event for event in third.environment.protocol_snapshot.events if event.kind == "EV_DL_WRQ_LUR")
    ack = next(event for event in third.environment.protocol_snapshot.events if event.kind == "EV_TH_ACK_LUR")
    assert projection.trigger_event_id == wrq.event_id
    assert projection.response_event_id == ack.event_id
    assert projection.response_in_reply_to_event_id == wrq.event_id
    assert projection.trigger_tick == wrq.tick
    assert projection.response_tick == ack.tick
    assert projection.trigger_sequence < projection.response_sequence
    ownership_contract = c_interpretation_contract(built.contract)
    assert projection.clock_identity == ownership_contract.clock_identity
    assert projection.uncertainty_identity == ownership_contract.uncertainty_identity
    assert projection.error_budget_identity == ownership_contract.error_budget_identity
    assert projection.unit == ownership_contract.unit
    assert projection.engineering_horizon_ticks == 3
    replay = replay_ownership(
        (
            OwnershipEvent(wrq.event_id, wrq.sequence_number, "REQUEST", C_OWNERSHIP_KEY, C_OWNERSHIP_TRIGGER_TYPE, projection.trigger_tick),
            OwnershipEvent(ack.event_id, ack.sequence_number, "RESPONSE", C_OWNERSHIP_KEY, C_OWNERSHIP_RESPONSE_TYPE, projection.response_tick),
        ),
        ownership_contract,
    )
    assert not replay.diagnostics
    assert replay.response_resolutions[ack.event_id].owner_request_id == wrq.event_id
    assert built.session.interpretation_contract is None
    assert first.state.evidence[-1].execution.observation_input is None
    assert third.state.evidence[-1].execution.observation_input is None


def test_c09_foreign_or_duplicate_ownership_material_is_rejected_by_the_same_contract() -> None:
    built = build_lur_start_session(repository=ROOT, controller=LurStartController())
    first = built.session.step(built.session.initial_state, built.environment)
    second = built.session.step(first.state, first.environment)
    third = built.session.step(second.state, second.environment)
    projection = third.environment.ownership_projections[-1]
    contract = c_interpretation_contract(built.contract)
    request = OwnershipEvent(
        projection.trigger_event_id, projection.trigger_sequence, "REQUEST",
        C_OWNERSHIP_KEY, C_OWNERSHIP_TRIGGER_TYPE, projection.trigger_tick,
    )
    response = OwnershipEvent(
        projection.response_event_id, projection.response_sequence, "RESPONSE",
        C_OWNERSHIP_KEY, C_OWNERSHIP_RESPONSE_TYPE, projection.response_tick,
    )
    foreign = replay_ownership((request, OwnershipEvent(
        response.event_id, response.sequence, response.kind, "FOREIGN-CORRELATION",
        response.event_type, response.timestamp,
    )), contract)
    assert foreign.response_resolutions[response.event_id].status == "UNMATCHED"
    duplicate = replay_ownership((request, request), contract)
    assert any(item.code == "INVALID-OWNERSHIP-EVENT" for item in duplicate.diagnostics)
    replayed = replay_ownership(
        (request, response),
        contract,
        prior_order_boundary=OwnershipOrderBoundary(
            response.sequence,
            response.timestamp,
            frozenset({request.event_id, response.event_id}),
        ),
    )
    assert any(item.code == "RETAINED-OWNERSHIP-EVENT-REPLAY" for item in replayed.diagnostics)


def test_c09_controlled_interpreter_handles_termination_and_retained_active_continuation() -> None:
    """C's exact B projection shares the controlled ownership termination semantics.

    Cancellation and supersession are interpreter-only public ownership facts:
    they are deliberately never fabricated as extra B protocol events.  This
    test fixes their relationship to the actual WRQ/ACK projection and proves
    that an ACTIVE request can be retained into a later finite observation.
    """

    built = build_lur_start_session(repository=ROOT, controller=LurStartController())
    first = built.session.step(built.session.initial_state, built.environment)
    second = built.session.step(first.state, first.environment)
    third = built.session.step(second.state, second.environment)
    projection = third.environment.ownership_projections[-1]
    contract = c_interpretation_contract(built.contract)
    actual_request = OwnershipEvent(
        projection.trigger_event_id, projection.trigger_sequence, "REQUEST",
        C_OWNERSHIP_KEY, C_OWNERSHIP_TRIGGER_TYPE, projection.trigger_tick,
    )
    actual_response = OwnershipEvent(
        projection.response_event_id, projection.response_sequence, "RESPONSE",
        C_OWNERSHIP_KEY, C_OWNERSHIP_RESPONSE_TYPE, projection.response_tick,
    )
    actual = replay_ownership((actual_request, actual_response), contract)
    assert not actual.diagnostics
    assert actual.response_resolutions[actual_response.event_id].owner_request_id == actual_request.event_id

    request_a = OwnershipEvent(
        "c09-request-a", 10, "REQUEST", C_OWNERSHIP_KEY,
        C_OWNERSHIP_TRIGGER_TYPE, Fraction(0),
    )
    cancelled_response = OwnershipEvent(
        "c09-response-after-cancel", 12, "RESPONSE", C_OWNERSHIP_KEY,
        C_OWNERSHIP_RESPONSE_TYPE, Fraction(2),
    )
    cancelled = replay_ownership((
        request_a,
        OwnershipEvent(
            "c09-cancel-a", 11, "CANCEL", C_OWNERSHIP_KEY,
            C_OWNERSHIP_CANCEL_TYPE, Fraction(1), request_a.event_id,
        ),
        cancelled_response,
    ), contract)
    assert not cancelled.diagnostics
    assert cancelled.request_dispositions[request_a.event_id] == "CANCELLED"
    assert cancelled.response_resolutions[cancelled_response.event_id].status == "UNMATCHED"

    superseded_response = OwnershipEvent(
        "c09-response-b", 13, "RESPONSE", C_OWNERSHIP_KEY,
        C_OWNERSHIP_RESPONSE_TYPE, Fraction(3),
    )
    superseded = replay_ownership((
        request_a,
        OwnershipEvent(
            "c09-supersede-a", 11, "SUPERSEDE", C_OWNERSHIP_KEY,
            C_OWNERSHIP_SUPERSEDE_TYPE, Fraction(1), request_a.event_id,
        ),
        OwnershipEvent(
            "c09-request-b", 12, "REQUEST", C_OWNERSHIP_KEY,
            C_OWNERSHIP_TRIGGER_TYPE, Fraction(2),
        ),
        superseded_response,
    ), contract)
    assert not superseded.diagnostics
    assert superseded.request_dispositions[request_a.event_id] == "SUPERSEDED"
    assert superseded.response_resolutions[superseded_response.event_id].owner_request_id == "c09-request-b"

    seeded = replay_ownership((request_a,), contract)
    assert not seeded.diagnostics
    continued = replay_ownership(
        (OwnershipEvent(
            "c09-response-a", 11, "RESPONSE", C_OWNERSHIP_KEY,
            C_OWNERSHIP_RESPONSE_TYPE, Fraction(1),
        ),),
        contract,
        prior_active_requests={request_a.event_id: request_a},
        prior_order_boundary=OwnershipOrderBoundary(
            request_a.sequence, request_a.timestamp, frozenset({request_a.event_id}),
        ),
    )
    assert not continued.diagnostics
    assert continued.response_resolutions["c09-response-a"].owner_request_id == request_a.event_id


def test_c09_adapter_rejects_foreign_or_unmatched_ack_before_ownership_projection() -> None:
    _built, _state, environment = _normal_after_prep()
    ordered = environment.execute(_request(
        environment, ORDER_ACTION_ID, "TEST", "unmatched-ack-source",
    ))
    snapshot = ordered.successor.protocol_snapshot
    receipt = ordered.successor.completed_receipts[-1]
    wrq = next(event for event in snapshot.events if event.kind == "EV_DL_WRQ_LUR")
    ack = next(event for event in snapshot.events if event.kind == "EV_TH_ACK_LUR")
    request = _request(ordered.successor, ORDER_ACTION_ID, "TEST", "unmatched-ack-projection")
    assert ordered.successor._order_ownership_projection(
        request=request,
        snapshot=snapshot,
        receipt=receipt,
        wrq=wrq,
        ack=replace(ack, in_reply_to_event_id="other-wrq"),
    ) is None
    assert ordered.successor._order_ownership_projection(
        request=request,
        snapshot=snapshot,
        receipt=receipt,
        wrq=wrq,
        ack=replace(ack, correlation_id="foreign-correlation"),
    ) is None


def test_c09_cross_reset_stale_adapter_never_reuses_ownership_or_drives_the_object() -> None:
    built = build_lur_start_session(repository=ROOT, controller=LurStartController())
    environment = built.environment
    assert environment.controller.full_reset().success
    reset_snapshot = environment.controller.public_snapshot()
    result = environment.execute(_request(
        environment, INSPECT_ACTION_ID, "TEST", "stale-cross-reset",
    ))
    assert result.record.effect_class == "CONFIRMED-NOT-SENT"
    assert result.successor is environment
    assert environment.controller.public_snapshot() == reset_snapshot
    assert not environment.ownership_projections


def test_c09_same_tick_protocol_order_remains_a_stable_sequence_and_public_projection() -> None:
    built, _state, environment = _normal_after_prep()
    ordered = environment.execute(_request(
        environment, ORDER_ACTION_ID, "TEST", "same-tick-order",
    ))
    events = ordered.successor.protocol_snapshot.events
    wrq = next(event for event in events if event.kind == "EV_DL_WRQ_LUR")
    ack = next(event for event in events if event.kind == "EV_TH_ACK_LUR")
    data = next(event for event in events if event.kind == "EV_DL_DATA_LUR")
    assert wrq.tick == ack.tick == data.tick
    assert wrq.sequence_number < ack.sequence_number < data.sequence_number
    projection = ordered.successor.ownership_projections[-1]
    assert projection.protocol_event_ids[-3:] == (wrq.event_id, ack.event_id, data.event_id)
    assert projection.trigger_event_id == wrq.event_id
    assert projection.response_event_id == ack.event_id
    assert projection.response_in_reply_to_event_id == wrq.event_id
    assert projection.trigger_sequence < projection.response_sequence


def test_c09_adapter_does_not_publish_b_control_result_types() -> None:
    adapter_fields = {item.type for item in fields(AppliedDeliveryEvidence)} | {
        item.type for item in fields(ToolReadbackEvidence)
    } | {
        item.type for item in fields(OwnershipProjection)
    }
    rendered = " ".join(str(item) for item in adapter_fields)
    assert "DeliveryResult" not in rendered
    assert "OperationResult" not in rendered
    assert "RuntimeReadback" not in rendered


def test_c10_invalid_request_is_confirmed_not_sent_without_object_drive() -> None:
    built = build_lur_start_session(repository=ROOT, controller=LurStartController())
    environment = built.environment
    before = environment.protocol_snapshot
    result = environment.execute(ExecutionRequest(
        session_id=environment.checkpoint.session_id,
        execution_attempt_id="wrong-kind",
        action_id=INSPECT_ACTION_ID,
        action_kind="PREP",
    ))
    assert result.record.effect_class == "CONFIRMED-NOT-SENT"
    assert result.successor.protocol_snapshot == before


@pytest.mark.parametrize("action_id, kind", [
    (INSPECT_ACTION_ID, "TEST"),
    (PREP_ACTION_ID, "PREP"),
    (ORDER_ACTION_ID, "TEST"),
    (RECOVER_ACTION_ID, "RECOVER"),
])
def test_c11_action_identifiers_remain_the_accepted_four(action_id: str, kind: str) -> None:
    contract = load_hb_session_contract(ROOT)
    assert contract.action(action_id)["kind"] == kind
