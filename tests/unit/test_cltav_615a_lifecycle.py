"""B-stage direct-object acceptance matrix for the bounded 615A LUR slice.

These tests use the real new Loader/TH/controller objects.  They do not call
the A-stage ReferenceSession seam, construct an expected trace through the
object's transition helpers, or claim a protocol verdict.
"""

from __future__ import annotations

import ast
import builtins
from dataclasses import fields, replace
import importlib
import inspect
from pathlib import Path
import sys

import pytest

from cltav_615a import FaultVariant, LurStartController, PublicEvent
from cltav_615a.objects import (
    EVENT_DL_DATA_LUR,
    EVENT_DL_WRQ_LUR,
    EVENT_LIST_PREPARED,
    EVENT_TH_ACK_LUR,
    EVENT_TH_LUS_READY,
)
from cltav_615a.types import ActivationStatus, InstallationStatus


ROOT = Path(__file__).resolve().parents[2]


def _normal_to_current_wrq(controller: LurStartController) -> PublicEvent:
    """Drive the literal normal pre-DATA microsteps and return the emitted WRQ."""

    assert controller.record_list_submission_precondition().accepted
    assert controller.emit_target_lus_ready().accepted
    assert all(result.accepted for result in controller.deliver_all())
    wrq = controller.advance_loader()
    assert wrq.accepted and wrq.event is not None
    assert wrq.event.kind == EVENT_DL_WRQ_LUR
    delivered = controller.deliver_next()
    assert delivered.delivered and delivered.accepted
    return wrq.event


def _normal_complete(controller: LurStartController) -> tuple[PublicEvent, ...]:
    _normal_to_current_wrq(controller)
    ack = controller.advance_target_hardware()
    assert ack.accepted and ack.event is not None
    assert controller.deliver_next().accepted
    data = controller.advance_loader()
    assert data.accepted and data.event is not None
    assert data.event.kind == EVENT_DL_DATA_LUR
    assert controller.deliver_next().accepted
    return controller.public_snapshot().events


def _event_kinds(controller: LurStartController) -> list[str]:
    return [event.kind for event in controller.public_snapshot().events]


def test_b01_normal_guarded_chain_and_duplicate_policy() -> None:
    controller = LurStartController()
    initial = controller.evaluator_readback()
    assert initial.virtual_tick == 0
    assert not initial.list_offered and not initial.target_list_ready and not initial.list_accepted
    assert initial.journal_length == initial.pending_delivery_length == 0

    preparation = controller.record_list_submission_precondition()
    assert preparation.accepted and preparation.event is not None
    assert preparation.event.kind == EVENT_LIST_PREPARED
    assert preparation.event.layer == "APPLICATION"
    assert preparation.event.opcode is None and preparation.event.direction is None
    assert controller.evaluator_readback().list_offered
    assert not controller.evaluator_readback().target_list_ready

    before_ready = controller.advance_loader()
    assert not before_ready.accepted
    assert before_ready.reason == "WRQ-REJECTED-TARGET-NOT-READY"
    assert EVENT_DL_WRQ_LUR not in _event_kinds(controller)

    ready = controller.emit_target_lus_ready()
    assert ready.accepted and ready.event is not None
    assert ready.event.kind == EVENT_TH_LUS_READY and ready.event.opcode is None
    # Emission and delivery are separate microsteps: ready is not effective at
    # the Loader until the actual pending event is delivered.
    assert not controller.evaluator_readback().target_list_ready
    assert all(result.accepted for result in controller.deliver_all())
    after_ready = controller.evaluator_readback()
    assert after_ready.target_list_ready and not after_ready.list_accepted

    wrq_result = controller.advance_loader()
    assert wrq_result.accepted and wrq_result.event is not None
    assert controller.deliver_next().accepted
    ack_result = controller.advance_target_hardware()
    assert ack_result.accepted and ack_result.event is not None
    assert controller.deliver_next().accepted
    data_result = controller.advance_loader()
    assert data_result.accepted and data_result.event is not None
    assert controller.deliver_next().accepted
    events = controller.public_snapshot().events
    assert [event.kind for event in events] == [
        EVENT_LIST_PREPARED,
        EVENT_TH_LUS_READY,
        EVENT_DL_WRQ_LUR,
        EVENT_TH_ACK_LUR,
        EVENT_DL_DATA_LUR,
    ]
    wrq, ack, data = events[2:]
    assert (wrq.actor, wrq.receiver, wrq.direction, wrq.opcode, wrq.file_role) == (
        "DATA-LOADER",
        "TARGET-HARDWARE",
        "DL-TO-TH",
        "WRQ",
        "LUR",
    )
    assert (ack.actor, ack.receiver, ack.direction, ack.opcode, ack.file_role, ack.in_reply_to_event_id) == (
        "TARGET-HARDWARE",
        "DATA-LOADER",
        "TH-TO-DL",
        "ACK",
        "LUR",
        wrq.event_id,
    )
    assert data.in_reply_to_event_id == ack.event_id
    assert controller.advance_loader().reason == "LOADER-IGNORED-CONTROL-SLICE-COMPLETE"
    assert controller.record_list_submission_precondition().reason == "LIST-SUBMISSION-IGNORED-ALREADY-OFFERED"
    assert controller.emit_target_lus_ready().reason == "READY-REJECTED-LIST-ALREADY-ACCEPTED"
    assert _event_kinds(controller) == [event.kind for event in events]


def test_b02_early_wrq_is_a_real_narrow_bypass_and_installation_is_not_activation() -> None:
    installed_only = LurStartController()
    record = installed_only.install_fault(FaultVariant.EARLY_WRQ)
    assert record.status is InstallationStatus.INSTALLED
    assert not installed_only.evaluator_audit()[-1].activation_records
    assert installed_only.evaluator_fault_readback().activation_status is ActivationStatus.NOT_TRIGGERED
    assert installed_only.evaluator_audit()[-1].installation_records[-1].requested_fault is FaultVariant.EARLY_WRQ

    controller = LurStartController()
    assert controller.install_fault(FaultVariant.EARLY_WRQ).status is InstallationStatus.INSTALLED
    assert controller.advance_loader().reason == "LOADER-BLOCKED-LIST-NOT-OFFERED"
    assert controller.record_list_submission_precondition().accepted
    early_wrq = controller.advance_loader()
    assert early_wrq.accepted and early_wrq.event is not None
    assert early_wrq.event.kind == EVENT_DL_WRQ_LUR
    assert EVENT_TH_LUS_READY not in _event_kinds(controller)
    activation = controller.evaluator_audit()[-1].activation_records
    assert len(activation) == 1
    assert activation[0].fault is FaultVariant.EARLY_WRQ
    assert activation[0].public_event_id == early_wrq.event.event_id
    assert activation[0].status is ActivationStatus.TRIGGERED
    assert controller.advance_loader().reason == "DATA-WAIT-MATCHING-ACK"
    assert controller.emit_target_lus_ready().reason == "READY-REJECTED-LIST-ALREADY-ACCEPTED"
    assert "fault" not in PublicEvent.__dataclass_fields__
    assert "EARLY-WRQ" not in repr(early_wrq.event)


def test_b03_early_data_bypasses_only_matching_ack_and_late_ack_cannot_erase_it() -> None:
    normal = LurStartController()
    _normal_to_current_wrq(normal)
    before = normal.public_snapshot()
    wait = normal.advance_loader()
    assert not wait.accepted and wait.reason == "DATA-WAIT-MATCHING-ACK"
    assert normal.public_snapshot() == before

    controller = LurStartController()
    wrq = _normal_to_current_wrq(controller)
    assert controller.install_fault(FaultVariant.EARLY_DATA).status is InstallationStatus.INSTALLED
    early_data = controller.advance_loader()
    assert early_data.accepted and early_data.event is not None
    assert early_data.event.kind == EVENT_DL_DATA_LUR
    assert early_data.event.in_reply_to_event_id is None
    assert controller.deliver_next().accepted
    assert controller.check_lur_order().observable == "DATA-BEFORE-MATCHING-ACK"
    activation = controller.evaluator_audit()[-1].activation_records
    assert len(activation) == 1 and activation[0].public_event_id == early_data.event.event_id

    late_ack = controller.advance_target_hardware()
    assert late_ack.accepted and late_ack.event is not None
    assert late_ack.event.in_reply_to_event_id == wrq.event_id
    assert controller.deliver_next().accepted
    assert controller.check_lur_order().observable == "DATA-BEFORE-MATCHING-ACK"
    assert controller.advance_loader().reason == "LOADER-IGNORED-CONTROL-SLICE-COMPLETE"


def test_b04_direct_objects_neither_import_nor_consume_runtime_prediction() -> None:
    """Poison the protected runtime import while reloading the direct controller."""

    controller_module = importlib.import_module("cltav_615a.controller")
    original_import = builtins.__import__

    def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):  # type: ignore[no-untyped-def]
        if name.startswith(("cltav_runtime", "cltav_offline", "a615a_sim")):
            raise AssertionError(f"B object must not import protected runtime/network package: {name}")
        return original_import(name, globals, locals, fromlist, level)

    builtins.__import__ = guarded_import
    try:
        reloaded = importlib.reload(controller_module)
        controller = reloaded.LurStartController()
        events = controller.run_shared_control_script()
    finally:
        builtins.__import__ = original_import
        importlib.reload(controller_module)
    assert events
    public_methods = (
        reloaded.LurStartController.record_list_submission_precondition,
        reloaded.LurStartController.emit_target_lus_ready,
        reloaded.LurStartController.advance_loader,
        reloaded.LurStartController.advance_target_hardware,
    )
    for method in public_methods:
        assert not {"prediction", "expected", "hypotheses", "minimax", "history"} & set(inspect.signature(method).parameters)


def test_b05_public_projection_is_independent_of_private_installation_audit() -> None:
    normal = LurStartController()
    normal_events = _normal_complete(normal)
    variant = LurStartController()
    assert variant.install_fault(FaultVariant.EARLY_WRQ).status is InstallationStatus.INSTALLED
    variant_events = _normal_complete(variant)
    # EARLY-WRQ is installed but never needed after ready; it therefore stays
    # private NOT-TRIGGERED evidence while the public semantic sequence is equal.
    assert variant_events == normal_events
    assert normal.public_scene_configuration() == variant.public_scene_configuration()
    assert not variant.evaluator_audit()[-1].activation_records
    assert variant.evaluator_audit()[-1].installation_records[-1].requested_fault is FaultVariant.EARLY_WRQ
    public_field_names = {field.name for field in fields(PublicEvent)}
    forbidden = {"fault", "activation", "private_state", "code_identity", "expected_h", "prediction"}
    assert public_field_names.isdisjoint(forbidden)
    rendered = repr(variant.public_snapshot()) + repr(variant.inspect_current_prefix())
    assert "EARLY-WRQ" not in rendered and variant.implementation_identity not in rendered


def test_b06_full_reset_clears_active_state_but_retains_prior_evaluator_audit() -> None:
    controller = LurStartController(implementation_identity="test-object-identity")
    assert controller.install_fault(FaultVariant.EARLY_WRQ).status is InstallationStatus.INSTALLED
    assert controller.record_list_submission_precondition().accepted
    assert controller.advance_loader().accepted
    assert controller.deliver_next().accepted  # application record
    assert controller.deliver_next().accepted  # TH receives early WRQ
    assert controller.advance_target_hardware().accepted  # nonempty pending ACK
    controller.advance_tick(5)
    dirty = controller.evaluator_readback()
    assert dirty.virtual_tick == 5 and dirty.journal_length and dirty.pending_delivery_length
    old_events = controller.public_snapshot().events
    reset = controller.full_reset()
    assert reset.success and reset.before == dirty
    assert reset.code_identity == "test-object-identity"
    assert reset.cleared_scope == (
        "LOADER-STATE", "TH-STATE", "VIRTUAL-CLOCK", "EVENT-JOURNAL", "PENDING-DELIVERY",
        "CORRELATION-ID-SEQUENCE", "FAULT-INSTALLATION-STATE",
    )
    clean = reset.after
    assert clean is not None
    assert clean.virtual_tick == clean.journal_length == clean.pending_delivery_length == 0
    assert not clean.list_offered and not clean.target_list_ready and not clean.list_accepted
    assert clean.active_fault is FaultVariant.NORMAL
    assert controller.evaluator_audit()[0].journal == old_events
    assert controller.evaluator_audit()[0].activation_records
    first_new = controller.record_list_submission_precondition().event
    assert first_new is not None and first_new.event_id not in {event.event_id for event in old_events}
    second = controller.full_reset()
    assert second.success and second.attempt_id != reset.attempt_id
    assert controller.evaluator_readback().journal_length == 0
    assert "NOT-PROTOCOL-ABORT" in second.reason


def test_b07_stale_foreign_and_duplicate_ack_cannot_advance_the_new_attempt() -> None:
    controller = LurStartController()
    _normal_to_current_wrq(controller)
    old_ack = controller.advance_target_hardware().event
    assert old_ack is not None
    assert controller.deliver_next().accepted
    controller.full_reset()
    new_wrq = _normal_to_current_wrq(controller)
    before = controller.evaluator_readback()

    stale = controller.deliver_external_event(old_ack)
    assert stale.delivered and not stale.accepted and stale.reason == "ACK-REJECTED-STALE-ATTEMPT"
    foreign_session = replace(
        old_ack,
        reset_id=controller.evaluator_readback().reset_id,
        attempt_id=controller.attempt_id,
        session_id="foreign-session",
    )
    assert controller.deliver_external_event(foreign_session).reason == "ACK-REJECTED-SESSION-MISMATCH"
    foreign_correlation = replace(
        old_ack,
        reset_id=controller.evaluator_readback().reset_id,
        attempt_id=controller.attempt_id,
        session_id=controller.session_id,
        correlation_id="foreign-correlation",
    )
    assert controller.deliver_external_event(foreign_correlation).reason == "ACK-REJECTED-CORRELATION-MISMATCH"
    assert controller.evaluator_readback() == before

    current_ack = controller.advance_target_hardware().event
    assert current_ack is not None and current_ack.in_reply_to_event_id == new_wrq.event_id
    assert controller.deliver_next().accepted
    assert controller.deliver_external_event(current_ack).reason == "ACK-IGNORED-DUPLICATE"
    assert controller.advance_loader().accepted


def test_b08_fault_installation_lifecycle_records_failures_and_single_fault_limit() -> None:
    normal = LurStartController()
    assert normal.evaluator_audit()[-1].installation_records[-1].status is InstallationStatus.NOT_INSTALLED

    controller = LurStartController()
    installed = controller.install_fault(FaultVariant.EARLY_DATA)
    assert installed.status is InstallationStatus.INSTALLED
    rejected = controller.install_fault(FaultVariant.EARLY_WRQ)
    assert rejected.status is InstallationStatus.REJECTED
    assert rejected.reason == "FAULT-INSTALLATION-REJECTED-SINGLE-FAULT-LIMIT"
    assert controller.evaluator_readback().active_fault is FaultVariant.EARLY_DATA

    failed = LurStartController()
    record = failed.install_fault(FaultVariant.EARLY_WRQ, force_failure=True)
    assert record.status is InstallationStatus.FAILED
    assert failed.record_list_submission_precondition().reason == "CONTROL-UNCONFIRMED-ATTEMPT-NOT-DRIVABLE"
    assert failed.evaluator_audit()[-1].installation_records[-1].reason.endswith("UNCONFIRMED")

    reset_failed = LurStartController()
    assert reset_failed.install_fault(FaultVariant.EARLY_WRQ).status is InstallationStatus.INSTALLED
    failed_reset = reset_failed.full_reset(force_revocation_failure=True)
    assert not failed_reset.success and failed_reset.attempt_id is None
    assert reset_failed.advance_loader().reason == "CONTROL-UNCONFIRMED-ATTEMPT-NOT-DRIVABLE"
    recovered_reset = reset_failed.full_reset()
    assert recovered_reset.success and reset_failed.evaluator_readback().active_fault is FaultVariant.NORMAL


def test_b09_virtual_tick_sequence_and_finite_receipt_are_deterministic_engineering_only() -> None:
    baseline = LurStartController()
    baseline_events = _normal_complete(baseline)
    assert [event.tick for event in baseline_events] == [0, 0, 0, 0, 0]
    assert [event.sequence_number for event in baseline_events] == [1, 2, 3, 4, 5]
    receipt = baseline.inspect_current_prefix()
    assert receipt.completed and receipt.start_sequence == 1 and receipt.end_sequence == 5
    assert receipt.reason == "ENGINEERING-FINITE-JOURNAL-CHECK-NOT-PROTOCOL-DEADLINE"

    shifted = LurStartController()
    shifted.advance_tick(9)
    shifted_events = _normal_complete(shifted)
    assert [event.kind for event in shifted_events] == [event.kind for event in baseline_events]
    assert [event.tick - 9 for event in shifted_events] == [event.tick for event in baseline_events]
    assert [event.sequence_number for event in shifted_events] == [event.sequence_number for event in baseline_events]


def test_b10_public_prefix_is_append_only_immutable_and_cannot_fake_completion() -> None:
    controller = LurStartController()
    assert controller.record_list_submission_precondition().accepted
    old_snapshot = controller.public_snapshot()
    assert old_snapshot.events[0].kind == EVENT_LIST_PREPARED
    assert controller.emit_target_lus_ready().accepted
    assert len(old_snapshot.events) == 1  # frozen tuple, not in-place mutation

    retained = controller.validate_retained_prefix(old_snapshot)
    assert retained.complete and retained.reason == "PREFIX-RETAINED-AND-APPENDED"
    incomplete = controller.complete_snapshot(old_snapshot)
    assert not incomplete.complete and incomplete.reason == "CURRENT-PREFIX-INCOMPLETE-TRUNCATED"
    exact = controller.public_snapshot()
    assert controller.complete_snapshot(exact).complete

    before = controller.evaluator_readback()
    replacement = replace(exact, events=(replace(exact.events[0], kind="EV-REPLACED"), *exact.events[1:]))
    reordered = replace(exact, events=tuple(reversed(exact.events)))
    duplicate = replace(exact, events=(exact.events[0], *exact.events))
    cross_session = replace(exact, session_id="other-session")
    for candidate in (replacement, reordered, duplicate, cross_session):
        verdict = controller.validate_retained_prefix(candidate)
        assert not verdict.complete
        assert "INVALID" in verdict.reason
    assert controller.evaluator_readback() == before
    assert "events" not in inspect.signature(controller.inspect_current_prefix).parameters


def test_b11_early_events_remain_raw_semantic_records_and_documented_as_bounded() -> None:
    controller = LurStartController()
    assert controller.install_fault(FaultVariant.EARLY_WRQ).status is InstallationStatus.INSTALLED
    assert controller.record_list_submission_precondition().accepted
    assert controller.advance_loader().accepted
    events = controller.public_snapshot().events
    assert [event.kind for event in events] == [EVENT_LIST_PREPARED, EVENT_DL_WRQ_LUR]
    assert events[-1].opcode == "WRQ" and events[-1].file_role == "LUR"
    assert all("TOOL-ERROR" not in event.kind for event in events)
    assert all("EARLY" not in event.kind for event in events)
    assert all(event.opcode is None for event in events if event.layer == "APPLICATION")
    assert not controller._require_target().state.matching_lur_wrq_received  # not delivered, no auto-repair

    object_source = (ROOT / "src/cltav_615a/controller.py").read_text(encoding="utf-8")
    assert "not a protocol deadline" in object_source
    assert "ReferenceSession" in object_source  # boundary documentation, not an import/use
    imported = [node.module for node in ast.walk(ast.parse(object_source)) if isinstance(node, ast.ImportFrom)]
    assert not any(name and name.startswith("cltav_runtime") for name in imported)


def test_b12_existing_a_contract_remains_bound_and_direct_package_is_not_a_runtime_adapter() -> None:
    package = (ROOT / "configs/engineering/cltav_615a_scenarios.json").read_text(encoding="utf-8")
    assert '"acceptedAuthorityCommit": "c577f34e98b91083a69f0a731a990c01aa7fa08b"' in package
    assert '"stage": "A-CONTRACT-ONLY-NO-OBJECT-IMPLEMENTATION"' in package
    controller_source = (ROOT / "src/cltav_615a/controller.py").read_text(encoding="utf-8")
    imported = [node.module for node in ast.walk(ast.parse(controller_source)) if isinstance(node, ast.ImportFrom)]
    assert not any(
        name and name.startswith(("cltav_runtime", "cltav_offline", "a615a_sim"))
        for name in imported
    )
