"""Actual B-object to :class:`ReferenceSession` adapter for C-stage work.

This adapter is intentionally narrow.  It drives a copied continuation of the
accepted B ``LurStartController`` through declared finite microsteps, derives
records from public journal/receipt facts, and returns only the existing
runtime's typed execution record.  It never asks the controller for private
loader state, fault activation, evaluator audit, a predicted class, or a
session hypothesis set.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, ClassVar, Mapping

from cltav_615a.controller import LurStartController
from cltav_615a.objects import (
    EVENT_DL_DATA_LUR,
    EVENT_DL_WRQ_LUR,
    EVENT_LIST_PREPARED,
    EVENT_TH_ACK_LUR,
    EVENT_TH_LUS_READY,
    semantic_event_error,
)
from cltav_615a.types import CompletionReceipt, FiniteCheckResult, JournalSnapshot, PublicEvent
from cltav_runtime.interpretation import OwnershipEvent, replay_ownership
from cltav_runtime.session import ReferenceSession, ResourceState
from cltav_runtime.synthetic import (
    EnvironmentExecution,
    ExecutionRequest,
    PrepRecoverResult,
    SyntheticEnvironment,
    VisibleExecutionRecord,
)

from .contract import (
    ACTION_IDS,
    INSPECT_ACTION_ID,
    ORDER_ACTION_ID,
    PREP_ACTION_ID,
    RECOVER_ACTION_ID,
    C_OWNERSHIP_CONTRACT_ID,
    C_OWNERSHIP_KEY,
    C_OWNERSHIP_RESPONSE_TYPE,
    C_OWNERSHIP_TRIGGER_TYPE,
    ScenarioContractError,
    ScenarioSessionContract,
    action_horizon,
    action_outcome,
    action_receipt_label,
    c_interpretation_contract,
    load_hb_session_contract,
)
from .identity import AdapterSourceIdentity, loaded_adapter_source_identity, register_loaded_module


PROJECTION_VERSION = "CLTAV-615A-C-PUBLIC-PROJECTION-V1"
_INERT_STATE = "C-ADAPTER-ENVIRONMENT"
_INERT_STATES = MappingProxyType({_INERT_STATE: MappingProxyType({})})


class SessionAdapterError(ValueError):
    """Named C-adapter failure that must not leak B evaluator control data."""


@dataclass(frozen=True)
class AppliedDeliveryEvidence:
    """Minimal public proof that one recorded protocol event was applied.

    It is minted only at the adapter boundary after B has FIFO-delivered the
    exact recorded event and its receiver accepted it.  It deliberately has
    no ``DeliveryResult`` or rejection reason, no active-fault information and
    no evaluator state.  The full public snapshot remains available for later
    prefix validation.
    """

    event_id: str
    event_kind: str
    reset_id: str
    attempt_id: str
    session_id: str
    correlation_id: str
    execution_attempt_id: str
    sequence_number: int
    tick: int
    protocol_snapshot: JournalSnapshot
    protocol_prefix_digest: str
    projection_version: str


@dataclass(frozen=True)
class ToolReadbackEvidence:
    """C-layer non-protocol Recover evidence, separate from ``PublicEvent``.

    A readback is a fresh check of the current public controller prefix plus a
    prior successfully applied READY proof.  It never creates a sixth protocol
    journal event and it never reads B's evaluator-only runtime readback.
    """

    readback_id: str
    execution_attempt_id: str
    run_id: str
    reset_id: str
    attempt_id: str
    session_id: str
    correlation_id: str
    retained_protocol_prefix_digest: str
    retained_event_ids: tuple[str, ...]
    sampled_tick: int
    sampled_sequence: int
    projection_version: str
    completed: bool
    receipt: CompletionReceipt


@dataclass(frozen=True)
class OwnershipProjection:
    """Public B WRQ/ACK ownership material for one order TEST.

    The projection deliberately does **not** create a sixth protocol event.
    Its request and response identifiers, sequence numbers, and ticks are
    the actual immutable B public WRQ and matching ACK values.  The completed
    prefix receipt is only supporting evidence for the same public prefix.
    """

    projection_id: str
    execution_attempt_id: str
    action_id: str
    reset_id: str
    attempt_id: str
    session_id: str
    correlation_id: str
    trigger_event_id: str
    response_event_id: str
    trigger_sequence: int
    response_sequence: int
    trigger_tick: Fraction
    response_tick: Fraction
    protocol_event_ids: tuple[str, ...]
    protocol_prefix_digest: str
    receipt_id: str
    ownership_contract_id: str
    ownership_policy: str
    response_in_reply_to_event_id: str
    replay_diagnostic_codes: tuple[str, ...]
    # These are identity-only bindings to the exact frozen H-B uncertainty
    # snapshot.  They do not turn this order witness into a T5 measurement or
    # claim any protocol deadline.
    clock_identity: str
    uncertainty_identity: str
    error_budget_identity: str
    unit: str
    engineering_horizon_ticks: Fraction


@dataclass(frozen=True)
class LurStartSession:
    """One constructed C-stage finite session and its initial real adapter."""

    session: ReferenceSession
    environment: "LurStartSessionEnvironment"
    contract: ScenarioSessionContract
    adapter_source_identity: AdapterSourceIdentity


def _snapshot_payload(snapshot: JournalSnapshot) -> Mapping[str, Any]:
    return {
        "resetId": snapshot.reset_id,
        "attemptId": snapshot.attempt_id,
        "sessionId": snapshot.session_id,
        "correlationId": snapshot.correlation_id,
        "events": [asdict(event) for event in snapshot.events],
    }


def _snapshot_digest(snapshot: JournalSnapshot) -> str:
    return sha256(
        json.dumps(_snapshot_payload(snapshot), sort_keys=True, separators=(",", ":")).encode("utf-8"),
    ).hexdigest()


def _same_identity(left: JournalSnapshot, right: JournalSnapshot) -> bool:
    return (
        left.reset_id == right.reset_id
        and left.attempt_id == right.attempt_id
        and left.session_id == right.session_id
        and left.correlation_id == right.correlation_id
    )


def _event_by_id(snapshot: JournalSnapshot, event_id: str) -> PublicEvent | None:
    matches = [event for event in snapshot.events if event.event_id == event_id]
    return matches[0] if len(matches) == 1 else None


def _matching_ack(snapshot: JournalSnapshot, wrq: PublicEvent) -> PublicEvent | None:
    matches = [
        event for event in snapshot.events
        if event.kind == EVENT_TH_ACK_LUR and event.in_reply_to_event_id == wrq.event_id
    ]
    return matches[0] if len(matches) == 1 else None


def _first_event(snapshot: JournalSnapshot, kind: str) -> PublicEvent | None:
    return next((event for event in snapshot.events if event.kind == kind), None)


def _receipt_matches_snapshot(receipt: CompletionReceipt, snapshot: JournalSnapshot) -> bool:
    events = snapshot.events
    return (
        receipt.completed is True
        and receipt.reset_id == snapshot.reset_id
        and receipt.attempt_id == snapshot.attempt_id
        and receipt.session_id == snapshot.session_id
        and receipt.correlation_id == snapshot.correlation_id
        and receipt.event_ids == tuple(event.event_id for event in events)
        and receipt.start_sequence == (events[0].sequence_number if events else None)
        and receipt.end_sequence == (events[-1].sequence_number if events else None)
    )


@dataclass(frozen=True, kw_only=True)
class LurStartSessionEnvironment(SyntheticEnvironment):
    """Copy-on-write production adapter around one actual B controller.

    ``SyntheticEnvironment`` is used solely because it is the accepted narrow
    runtime executor carrier.  Its state-table fields are inert; this class
    overrides execution entirely.  Every ordinary dispatch deep-copies the B
    controller first, so a retained predecessor never shares a mutable object
    continuation with its returned successor.
    """

    controller: LurStartController
    contract: ScenarioSessionContract
    checkpoint: JournalSnapshot
    adapter_source_identity: AdapterSourceIdentity
    controller_source_identity: str
    completed_receipts: tuple[CompletionReceipt, ...] = ()
    finite_checks: tuple[FiniteCheckResult, ...] = ()
    applied_deliveries: tuple[AppliedDeliveryEvidence, ...] = ()
    tool_readbacks: tuple[ToolReadbackEvidence, ...] = ()
    ownership_projections: tuple[OwnershipProjection, ...] = ()
    consumed_readback_ids: frozenset[str] = frozenset()

    _MAX_INSPECT_CONTROLLER_CALLS: ClassVar[int] = 2
    _MAX_INSPECT_DELIVERIES: ClassVar[int] = 2
    _MAX_ORDER_CONTROLLER_CALLS: ClassVar[int] = 4
    _MAX_ORDER_DELIVERIES: ClassVar[int] = 4

    @classmethod
    def from_controller(
        cls,
        *,
        controller: LurStartController,
        contract: ScenarioSessionContract,
    ) -> "LurStartSessionEnvironment":
        if type(controller) is not LurStartController:
            raise SessionAdapterError("C-ADAPTER-CONTROLLER-TYPE-INVALID")
        adapter_identity = loaded_adapter_source_identity()
        snapshot = controller.public_snapshot()
        return cls(
            _state=_INERT_STATE,
            _uncertainty_identity=contract.uncertainty_identity,
            _states=_INERT_STATES,
            _pending_delivery=None,
            controller=controller,
            contract=contract,
            checkpoint=snapshot,
            adapter_source_identity=adapter_identity,
            controller_source_identity=controller.source_identity.identifier,
        )

    @property
    def protocol_snapshot(self) -> JournalSnapshot:
        """Return the frozen public checkpoint; never a private B readback."""

        return self.checkpoint

    def with_pending_delivery(self, record: VisibleExecutionRecord) -> "LurStartSessionEnvironment":
        """Reject synthetic ingress: C has no hidden replacement transport."""

        raise SessionAdapterError("C-ADAPTER-SYNTHETIC-PENDING-DELIVERY-FORBIDDEN")

    def take_pending_delivery(self) -> None:
        """The actual B queue is fully driven inside a bounded action plan."""

        return None

    def _next(
        self,
        *,
        controller: LurStartController,
        checkpoint: JournalSnapshot,
        receipt: CompletionReceipt | None = None,
        finite_check: FiniteCheckResult | None = None,
        applied: tuple[AppliedDeliveryEvidence, ...] = (),
        readback: ToolReadbackEvidence | None = None,
        ownership_projection: OwnershipProjection | None = None,
    ) -> "LurStartSessionEnvironment":
        return LurStartSessionEnvironment(
            _state=_INERT_STATE,
            _uncertainty_identity=self._uncertainty_identity,
            _states=_INERT_STATES,
            _pending_delivery=None,
            controller=controller,
            contract=self.contract,
            checkpoint=checkpoint,
            adapter_source_identity=self.adapter_source_identity,
            controller_source_identity=self.controller_source_identity,
            completed_receipts=self.completed_receipts + (() if receipt is None else (receipt,)),
            finite_checks=self.finite_checks + (() if finite_check is None else (finite_check,)),
            applied_deliveries=self.applied_deliveries + applied,
            tool_readbacks=self.tool_readbacks + (() if readback is None else (readback,)),
            ownership_projections=(
                self.ownership_projections
                + (() if ownership_projection is None else (ownership_projection,))
            ),
            consumed_readback_ids=(
                self.consumed_readback_ids
                if readback is None else self.consumed_readback_ids | {readback.readback_id}
            ),
        )

    def _preflight(self, request: ExecutionRequest) -> str | None:
        if type(request) is not ExecutionRequest:
            return "C-ADAPTER-REQUEST-TYPE-INVALID"
        if request.session_id != self.checkpoint.session_id or request.session_id != self.controller.session_id:
            return "C-ADAPTER-REQUEST-SESSION-MISMATCH"
        if request.action_id not in ACTION_IDS:
            return "C-ADAPTER-REQUEST-ACTION-UNKNOWN"
        action = self.contract.action(request.action_id)
        if request.action_kind != action.get("kind"):
            return "C-ADAPTER-REQUEST-KIND-MISMATCH"
        if not request.execution_attempt_id:
            return "C-ADAPTER-REQUEST-ATTEMPT-INVALID"
        if self.controller.source_identity.identifier != self.controller_source_identity:
            return "C-ADAPTER-B-SOURCE-IDENTITY-DRIFT"
        if self.controller.public_snapshot() != self.checkpoint:
            return "C-ADAPTER-PREDECESSOR-CHECKPOINT-STALE"
        return None

    def _record(
        self,
        request: ExecutionRequest,
        *,
        effect_class: str,
        observable: str | None = None,
        summary_confirmed: bool = False,
        post_summary: str | None = None,
        measurement_tick: Fraction | None = None,
        prep_recover: PrepRecoverResult | None = None,
        suffix: str,
    ) -> VisibleExecutionRecord:
        evidence_ref = f"c-adapter:{request.execution_attempt_id}:{suffix}"
        return VisibleExecutionRecord(
            execution_attempt_id=request.execution_attempt_id,
            action_id=request.action_id,
            effect_class=effect_class,
            observable=observable,
            summary_confirmed=summary_confirmed,
            post_summary=post_summary,
            measurement_tick=measurement_tick,
            uncertainty_identity=(
                self.contract.uncertainty_identity
                if effect_class == "NONE" and observable is not None else None
            ),
            evidence_ref=evidence_ref,
            prep_recover=prep_recover,
        )

    def _not_sent(self, request: ExecutionRequest) -> EnvironmentExecution:
        return EnvironmentExecution(
            self._record(request, effect_class="CONFIRMED-NOT-SENT", suffix="not-sent"),
            self,
        )

    def _unknown(
        self,
        request: ExecutionRequest,
        *,
        successor: "LurStartSessionEnvironment",
    ) -> EnvironmentExecution:
        return EnvironmentExecution(
            self._record(request, effect_class="UNKNOWN-EFFECT", suffix="unconfirmed"),
            successor,
        )

    @staticmethod
    def _completed_receipt(
        controller: LurStartController,
        snapshot: JournalSnapshot,
        label: str,
    ) -> CompletionReceipt | None:
        receipt = controller.inspect_current_prefix(receipt_label=label)
        verification = controller.complete_snapshot(snapshot)
        if not verification.complete or not _receipt_matches_snapshot(receipt, snapshot):
            return None
        return receipt

    def _order_ownership_projection(
        self,
        *,
        request: ExecutionRequest,
        snapshot: JournalSnapshot,
        receipt: CompletionReceipt,
        wrq: PublicEvent,
        ack: PublicEvent,
    ) -> OwnershipProjection | None:
        """Replay actual B WRQ/ACK facts under the controlled ownership rule.

        This is deliberately narrower than a generic protocol parser.  The
        only C ownership witness for the order Test is an exact public WRQ and
        the current-correlation ACK that names that WRQ in ``in_reply_to``.
        No controller-private state, fault identity, fabricated receipt event,
        or alternative pairing policy participates in the decision.
        """

        if not (
            _receipt_matches_snapshot(receipt, snapshot)
            and _same_identity(snapshot, JournalSnapshot(
                wrq.reset_id, wrq.attempt_id, wrq.session_id, wrq.correlation_id, (),
            ))
            and _same_identity(snapshot, JournalSnapshot(
                ack.reset_id, ack.attempt_id, ack.session_id, ack.correlation_id, (),
            ))
            and wrq.kind == EVENT_DL_WRQ_LUR
            and ack.kind == EVENT_TH_ACK_LUR
            and ack.in_reply_to_event_id == wrq.event_id
            and wrq.sequence_number < ack.sequence_number
            and wrq.tick <= ack.tick
            and _event_by_id(snapshot, wrq.event_id) == wrq
            and _event_by_id(snapshot, ack.event_id) == ack
            and semantic_event_error(wrq) is None
            and semantic_event_error(ack) is None
        ):
            return None
        ownership_contract = c_interpretation_contract(self.contract)
        if (
            ownership_contract.clock_identity != self.contract.virtual_clock_id
            or ownership_contract.uncertainty_identity != self.contract.uncertainty_identity
            or ownership_contract.error_budget_identity != self.contract.model.uncertainty.identity
            or ownership_contract.unit != self.contract.model.uncertainty.time_unit
        ):
            return None
        replay = replay_ownership(
            (
                OwnershipEvent(
                    event_id=wrq.event_id,
                    sequence=wrq.sequence_number,
                    kind="REQUEST",
                    key=C_OWNERSHIP_KEY,
                    event_type=C_OWNERSHIP_TRIGGER_TYPE,
                    timestamp=Fraction(wrq.tick),
                ),
                OwnershipEvent(
                    event_id=ack.event_id,
                    sequence=ack.sequence_number,
                    kind="RESPONSE",
                    key=C_OWNERSHIP_KEY,
                    event_type=C_OWNERSHIP_RESPONSE_TYPE,
                    timestamp=Fraction(ack.tick),
                ),
            ),
            ownership_contract,
        )
        resolution = replay.response_resolutions.get(ack.event_id)
        if (
            replay.diagnostics
            or resolution is None
            or resolution.status != "UNIQUE"
            or resolution.owner_request_id != wrq.event_id
        ):
            return None
        digest = _snapshot_digest(snapshot)
        projection_id = sha256(
            (
                f"{request.execution_attempt_id}|{wrq.event_id}|{ack.event_id}|"
                f"{receipt.receipt_id}|{digest}|{C_OWNERSHIP_CONTRACT_ID}"
            ).encode("utf-8"),
        ).hexdigest()
        return OwnershipProjection(
            projection_id=projection_id,
            execution_attempt_id=request.execution_attempt_id,
            action_id=request.action_id,
            reset_id=snapshot.reset_id,
            attempt_id=snapshot.attempt_id,
            session_id=snapshot.session_id,
            correlation_id=snapshot.correlation_id,
            trigger_event_id=wrq.event_id,
            response_event_id=ack.event_id,
            trigger_sequence=wrq.sequence_number,
            response_sequence=ack.sequence_number,
            trigger_tick=Fraction(wrq.tick),
            response_tick=Fraction(ack.tick),
            protocol_event_ids=tuple(event.event_id for event in snapshot.events),
            protocol_prefix_digest=digest,
            receipt_id=receipt.receipt_id,
            ownership_contract_id=C_OWNERSHIP_CONTRACT_ID,
            ownership_policy="UNIQUE-KEY",
            response_in_reply_to_event_id=ack.in_reply_to_event_id,
            replay_diagnostic_codes=tuple(item.code for item in replay.diagnostics),
            clock_identity=ownership_contract.clock_identity,
            uncertainty_identity=ownership_contract.uncertainty_identity,
            error_budget_identity=ownership_contract.error_budget_identity,
            unit=ownership_contract.unit,
            engineering_horizon_ticks=action_horizon(self.contract, request.action_id),
        )

    @staticmethod
    def _applied_delivery(
        *,
        controller: LurStartController,
        request: ExecutionRequest,
        expected: PublicEvent,
        adapter_identity: AdapterSourceIdentity,
    ) -> AppliedDeliveryEvidence | None:
        """Deliver exactly one expected event and project only a success fact."""

        raw = controller.deliver_next()
        if not (raw.delivered and raw.accepted and raw.event == expected):
            return None
        snapshot = controller.public_snapshot()
        recorded = _event_by_id(snapshot, expected.event_id)
        if (
            recorded != expected
            or semantic_event_error(expected) is not None
            or not _same_identity(snapshot, JournalSnapshot(
                expected.reset_id, expected.attempt_id, expected.session_id,
                expected.correlation_id, (),
            ))
        ):
            return None
        return AppliedDeliveryEvidence(
            event_id=expected.event_id,
            event_kind=expected.kind,
            reset_id=expected.reset_id,
            attempt_id=expected.attempt_id,
            session_id=expected.session_id,
            correlation_id=expected.correlation_id,
            execution_attempt_id=request.execution_attempt_id,
            sequence_number=expected.sequence_number,
            tick=expected.tick,
            protocol_snapshot=snapshot,
            protocol_prefix_digest=_snapshot_digest(snapshot),
            projection_version=f"{PROJECTION_VERSION}:{adapter_identity.digest}",
        )

    def _retained_application_for(
        self,
        *,
        controller: LurStartController,
        current: JournalSnapshot,
        event: PublicEvent,
        added: tuple[AppliedDeliveryEvidence, ...] = (),
    ) -> AppliedDeliveryEvidence | None:
        """Return a still-valid public application proof for ``event``.

        Presence in the immutable B journal proves that an event was emitted,
        not that its peer accepted FIFO delivery.  A later C action may use a
        previously emitted event only when its retained C projection proves
        successful application on the current public-prefix lineage.  If a
        pending event lacks such a proof, the caller may try to deliver that
        exact existing event; it must never mint or re-emit a replacement.
        """

        expected_projection = f"{PROJECTION_VERSION}:{self.adapter_source_identity.digest}"
        for evidence in reversed(self.applied_deliveries + added):
            if (
                evidence.event_id != event.event_id
                or evidence.event_kind != event.kind
                or evidence.reset_id != event.reset_id
                or evidence.attempt_id != event.attempt_id
                or evidence.session_id != event.session_id
                or evidence.correlation_id != event.correlation_id
                or evidence.sequence_number != event.sequence_number
                or evidence.tick != event.tick
                or evidence.projection_version != expected_projection
            ):
                continue
            if (
                _event_by_id(current, event.event_id) != event
                or _event_by_id(evidence.protocol_snapshot, event.event_id) != event
                or evidence.protocol_prefix_digest != _snapshot_digest(evidence.protocol_snapshot)
            ):
                continue
            retained = controller.validate_retained_prefix(evidence.protocol_snapshot)
            if retained.complete:
                return evidence
        return None

    def _ensure_event_application(
        self,
        *,
        controller: LurStartController,
        request: ExecutionRequest,
        event: PublicEvent,
        added: tuple[AppliedDeliveryEvidence, ...],
    ) -> tuple[bool, AppliedDeliveryEvidence | None]:
        """Require an existing event's current FIFO application proof.

        The boolean separates a verified pre-existing proof from an attempted
        delivery that did not yield a proof.  The latter is deliberately not
        collapsed into "already delivered": a public journal record describes
        emission only.  Callers retain the evolved successor on failure.
        """

        current = controller.public_snapshot()
        if self._retained_application_for(
            controller=controller,
            current=current,
            event=event,
            added=added,
        ) is not None:
            return True, None
        application = self._applied_delivery(
            controller=controller,
            request=request,
            expected=event,
            adapter_identity=self.adapter_source_identity,
        )
        return application is not None, application

    @staticmethod
    def _latest_event_from(
        before: JournalSnapshot,
        after: JournalSnapshot,
        *,
        required_kind: str,
    ) -> PublicEvent | None:
        if not _same_identity(before, after) or len(after.events) != len(before.events) + 1:
            return None
        event = after.events[-1]
        if event.kind != required_kind or semantic_event_error(event) is not None:
            return None
        return event

    def _drive_initial_inspection(
        self,
        request: ExecutionRequest,
        controller: LurStartController,
    ) -> EnvironmentExecution:
        # D01 fixed public microstep plan (maximum 2 controller calls and 2
        # FIFO deliveries): list preparation -> list delivery -> one Loader
        # opportunity before any READY -> optional WRQ delivery -> finite check.
        before = controller.public_snapshot()
        listed = controller.record_list_submission_precondition()
        after_list = controller.public_snapshot()
        list_event = self._latest_event_from(before, after_list, required_kind=EVENT_LIST_PREPARED)
        if not (listed.accepted and list_event is not None):
            return self._not_sent(request)
        list_delivery = self._applied_delivery(
            controller=controller,
            request=request,
            expected=list_event,
            adapter_identity=self.adapter_source_identity,
        )
        if list_delivery is None:
            snapshot = controller.public_snapshot()
            return self._unknown(request, successor=self._next(controller=controller, checkpoint=snapshot))
        prior = controller.public_snapshot()
        loader_step = controller.advance_loader()
        after_loader = controller.public_snapshot()
        emitted = self._latest_event_from(prior, after_loader, required_kind=EVENT_DL_WRQ_LUR)
        applications: tuple[AppliedDeliveryEvidence, ...] = (list_delivery,)
        if loader_step.accepted:
            if emitted is None:
                return self._unknown(request, successor=self._next(
                    controller=controller, checkpoint=after_loader, applied=applications,
                ))
            wrq_delivery = self._applied_delivery(
                controller=controller,
                request=request,
                expected=emitted,
                adapter_identity=self.adapter_source_identity,
            )
            if wrq_delivery is None:
                snapshot = controller.public_snapshot()
                return self._unknown(request, successor=self._next(
                    controller=controller, checkpoint=snapshot, applied=applications,
                ))
            applications += (wrq_delivery,)
        elif emitted is not None:
            return self._unknown(request, successor=self._next(
                controller=controller, checkpoint=after_loader, applied=applications,
            ))
        # The first action has a one-tick finite engineering observation
        # horizon.  It is not a protocol deadline; all preceding microsteps
        # may legitimately share tick zero and remain ordered by sequence.
        controller.advance_tick(1)
        snapshot = controller.public_snapshot()
        check = controller.check_no_wrq_before_ready()
        receipt = self._completed_receipt(controller, snapshot, action_receipt_label(self.contract, request.action_id))
        if receipt is None or not check.receipt.completed or check.observable not in {
            "NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001",
            "EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001",
        }:
            successor = self._next(
                controller=controller,
                checkpoint=snapshot,
                receipt=receipt,
                finite_check=check,
                applied=applications,
            )
            return self._unknown(request, successor=successor)
        successor = self._next(
            controller=controller,
            checkpoint=snapshot,
            receipt=receipt,
            finite_check=check,
            applied=applications,
        )
        outcome = action_outcome(self.contract, request.action_id, check.observable)
        summary = outcome.get("postSummary")
        if type(summary) is not str or not summary:
            return self._unknown(request, successor=successor)
        record = self._record(
            request,
            effect_class="NONE",
            observable=check.observable,
            summary_confirmed=True,
            post_summary=summary,
            measurement_tick=action_horizon(self.contract, request.action_id),
            suffix=f"finite:{receipt.receipt_id}",
        )
        return EnvironmentExecution(record, successor)

    def _drive_prep(
        self,
        request: ExecutionRequest,
        controller: LurStartController,
    ) -> EnvironmentExecution:
        before = controller.public_snapshot()
        emitted = controller.emit_target_lus_ready()
        after_emit = controller.public_snapshot()
        ready = self._latest_event_from(before, after_emit, required_kind=EVENT_TH_LUS_READY)
        if not emitted.accepted or ready is None:
            return self._not_sent(request)
        application = self._applied_delivery(
            controller=controller,
            request=request,
            expected=ready,
            adapter_identity=self.adapter_source_identity,
        )
        snapshot = controller.public_snapshot()
        receipt = self._completed_receipt(controller, snapshot, action_receipt_label(self.contract, request.action_id))
        successor = self._next(
            controller=controller,
            checkpoint=snapshot,
            receipt=receipt,
            applied=(() if application is None else (application,)),
        )
        # Target and summary confirmations are intentionally computed through
        # separate predicates.  A READY emission or journal receipt alone is
        # never a target confirmation; only an exact accepted delivery is.
        target_confirmed = application is not None and application.event_kind == EVENT_TH_LUS_READY
        summary_confirmed = target_confirmed and receipt is not None
        declared_target = action_receipt_label(self.contract, request.action_id)
        if not summary_confirmed:
            result = PrepRecoverResult(
                target_confirmed=target_confirmed,
                summary_confirmed=False,
                prep_error=False,
                ineligible=False,
                declared_target=declared_target,
                evidence="c-adapter:ready-application-unconfirmed",
                post_summary=None,
            )
            record = self._record(
                request,
                effect_class="NONE",
                prep_recover=result,
                suffix="prep-unconfirmed",
            )
            return EnvironmentExecution(record, successor)
        outcome = action_outcome(self.contract, request.action_id, "EV_TH_LUS0001")
        summary = outcome.get("postSummary")
        if type(summary) is not str or not summary:
            return self._unknown(request, successor=successor)
        result = PrepRecoverResult(
            target_confirmed=target_confirmed,
            summary_confirmed=True,
            prep_error=False,
            ineligible=False,
            declared_target=declared_target,
            evidence=f"c-adapter:ready-application:{application.event_id}",
            post_summary=summary,
        )
        record = self._record(
            request,
            effect_class="NONE",
            summary_confirmed=True,
            post_summary=summary,
            prep_recover=result,
            suffix=f"prep:{receipt.receipt_id}",
        )
        return EnvironmentExecution(record, successor)

    def _drive_order_test(
        self,
        request: ExecutionRequest,
        controller: LurStartController,
    ) -> EnvironmentExecution:
        """Run D01's bounded public microsteps without fault-dependent flow."""

        applications: tuple[AppliedDeliveryEvidence, ...] = ()
        snapshot = controller.public_snapshot()
        wrq = _first_event(snapshot, EVENT_DL_WRQ_LUR)

        # First establish (or resume) the actual WRQ.  A retained journal item
        # still needs its own successful C application proof: emission alone
        # does not establish the peer state that permits the matching ACK.
        if wrq is None:
            before = snapshot
            emitted = controller.advance_loader()
            snapshot = controller.public_snapshot()
            wrq = self._latest_event_from(before, snapshot, required_kind=EVENT_DL_WRQ_LUR)
            if not emitted.accepted or wrq is None:
                return self._unknown(request, successor=self._next(controller=controller, checkpoint=snapshot))

        wrq_applied, wrq_application = self._ensure_event_application(
            controller=controller,
            request=request,
            event=wrq,
            added=applications,
        )
        if not wrq_applied:
            snapshot = controller.public_snapshot()
            return self._unknown(request, successor=self._next(
                controller=controller, checkpoint=snapshot, applied=applications,
            ))
        if wrq_application is not None:
            applications += (wrq_application,)

        snapshot = controller.public_snapshot()
        ack = _matching_ack(snapshot, wrq)
        data = _first_event(snapshot, EVENT_DL_DATA_LUR)

        # Every variant gets exactly one public Loader opportunity before an
        # ACK has been emitted.  NORMAL waits; EARLY-DATA emits its named
        # event.  A resumption after a failed WRQ delivery gets the same
        # opportunity only after the original WRQ is successfully applied.
        if ack is None and data is None:
            before = snapshot
            early_data_step = controller.advance_loader()
            snapshot = controller.public_snapshot()
            data = self._latest_event_from(before, snapshot, required_kind=EVENT_DL_DATA_LUR)
            if early_data_step.accepted:
                if data is None:
                    return self._unknown(request, successor=self._next(
                        controller=controller, checkpoint=snapshot, applied=applications,
                    ))
            elif data is not None:
                return self._unknown(request, successor=self._next(
                    controller=controller, checkpoint=snapshot, applied=applications,
                ))

        snapshot = controller.public_snapshot()
        ack = _matching_ack(snapshot, wrq)
        data = _first_event(snapshot, EVENT_DL_DATA_LUR)

        # A named EARLY-DATA event precedes its later matching ACK in the
        # public journal and therefore must be delivered first.  Do not infer
        # that an event was applied merely because it was recorded.
        if data is not None and (ack is None or data.sequence_number < ack.sequence_number):
            data_applied, data_application = self._ensure_event_application(
                controller=controller,
                request=request,
                event=data,
                added=applications,
            )
            if not data_applied:
                snapshot = controller.public_snapshot()
                return self._unknown(request, successor=self._next(
                    controller=controller, checkpoint=snapshot, applied=applications,
                ))
            if data_application is not None:
                applications += (data_application,)

        # An ACK may already be journaled by an interrupted predecessor.  If
        # it lacks a retained success proof, deliver that exact pending FIFO
        # event once.  No C path emits a replacement ACK or reads B's private
        # pending queue to decide the phase.
        snapshot = controller.public_snapshot()
        ack = _matching_ack(snapshot, wrq)
        if ack is None:
            before = snapshot
            emitted_ack = controller.advance_target_hardware()
            snapshot = controller.public_snapshot()
            ack = self._latest_event_from(before, snapshot, required_kind=EVENT_TH_ACK_LUR)
            if not emitted_ack.accepted or ack is None or ack.in_reply_to_event_id != wrq.event_id:
                return self._unknown(request, successor=self._next(
                    controller=controller, checkpoint=snapshot, applied=applications,
                ))

        ack_applied, ack_application = self._ensure_event_application(
            controller=controller,
            request=request,
            event=ack,
            added=applications,
        )
        if not ack_applied:
            snapshot = controller.public_snapshot()
            return self._unknown(request, successor=self._next(
                controller=controller, checkpoint=snapshot, applied=applications,
            ))
        if ack_application is not None:
            applications += (ack_application,)

        snapshot = controller.public_snapshot()
        data = _first_event(snapshot, EVENT_DL_DATA_LUR)
        if data is None:
            before = snapshot
            emitted_data = controller.advance_loader()
            snapshot = controller.public_snapshot()
            data = self._latest_event_from(before, snapshot, required_kind=EVENT_DL_DATA_LUR)
            if not emitted_data.accepted or data is None:
                return self._unknown(request, successor=self._next(
                    controller=controller, checkpoint=snapshot, applied=applications,
                ))

        # The final DATA phase is likewise accepted only on an exact retained
        # FIFO application proof.  When it was a pre-ACK EARLY-DATA event the
        # earlier branch has already produced that proof and this is a no-op.
        data_applied, data_application = self._ensure_event_application(
            controller=controller,
            request=request,
            event=data,
            added=applications,
        )
        if not data_applied:
            snapshot = controller.public_snapshot()
            return self._unknown(request, successor=self._next(
                controller=controller, checkpoint=snapshot, applied=applications,
            ))
        if data_application is not None:
            applications += (data_application,)
        # The order action's declared three-tick finite horizon is reached at
        # an action boundary.  Its same-tick protocol events remain ordered by
        # their immutable sequence numbers, not by an invented physical time.
        controller.advance_tick(max(0, int(action_horizon(self.contract, request.action_id)) - controller.virtual_tick))
        snapshot = controller.public_snapshot()
        check = controller.check_lur_order()
        receipt = self._completed_receipt(controller, snapshot, action_receipt_label(self.contract, request.action_id))
        if receipt is None or not check.receipt.completed or check.observable not in {
            "WRQ-ACK-DATA-IN-ORDER", "DATA-BEFORE-MATCHING-ACK",
        }:
            successor = self._next(
                controller=controller,
                checkpoint=snapshot,
                receipt=receipt,
                finite_check=check,
                applied=applications,
            )
            return self._unknown(request, successor=successor)
        if wrq is None or ack is None:
            successor = self._next(
                controller=controller,
                checkpoint=snapshot,
                receipt=receipt,
                finite_check=check,
                applied=applications,
            )
            return self._unknown(request, successor=successor)
        ownership_projection = self._order_ownership_projection(
            request=request,
            snapshot=snapshot,
            receipt=receipt,
            wrq=wrq,
            ack=ack,
        )
        if ownership_projection is None:
            successor = self._next(
                controller=controller,
                checkpoint=snapshot,
                receipt=receipt,
                finite_check=check,
                applied=applications,
            )
            return self._unknown(request, successor=successor)
        successor = self._next(
            controller=controller,
            checkpoint=snapshot,
            receipt=receipt,
            finite_check=check,
            applied=applications,
            ownership_projection=ownership_projection,
        )
        outcome = action_outcome(self.contract, request.action_id, check.observable)
        summary = outcome.get("postSummary")
        if type(summary) is not str or not summary:
            return self._unknown(request, successor=successor)
        record = self._record(
            request,
            effect_class="NONE",
            observable=check.observable,
            summary_confirmed=True,
            post_summary=summary,
            measurement_tick=action_horizon(self.contract, request.action_id),
            suffix=f"finite:{receipt.receipt_id}",
        )
        return EnvironmentExecution(record, successor)

    def _eligible_ready_application(
        self,
        *,
        controller: LurStartController,
        current: JournalSnapshot,
    ) -> AppliedDeliveryEvidence | None:
        """Find a prior successful READY application valid for this successor."""

        for evidence in reversed(self.applied_deliveries):
            if evidence.event_kind != EVENT_TH_LUS_READY:
                continue
            if (
                evidence.reset_id != current.reset_id
                or evidence.attempt_id != current.attempt_id
                or evidence.session_id != current.session_id
                or evidence.correlation_id != current.correlation_id
                or evidence.projection_version != f"{PROJECTION_VERSION}:{self.adapter_source_identity.digest}"
            ):
                continue
            ready = _event_by_id(current, evidence.event_id)
            if ready is None or ready.kind != EVENT_TH_LUS_READY or semantic_event_error(ready) is not None:
                continue
            retained = controller.validate_retained_prefix(evidence.protocol_snapshot)
            if not retained.complete:
                continue
            if evidence.protocol_prefix_digest != _snapshot_digest(evidence.protocol_snapshot):
                continue
            return evidence
        return None

    def _drive_recover(
        self,
        request: ExecutionRequest,
        controller: LurStartController,
    ) -> EnvironmentExecution:
        # Recover is a non-emitting tool-layer check.  Copying the controller
        # preserves branch isolation, but no controller action, reset, queue
        # delivery or protocol event is issued in this function.
        current = controller.public_snapshot()
        receipt = self._completed_receipt(controller, current, action_receipt_label(self.contract, request.action_id))
        ready_application = self._eligible_ready_application(controller=controller, current=current)
        candidate_id = sha256(
            (
                f"{request.execution_attempt_id}|{_snapshot_digest(current)}|"
                f"{self.adapter_source_identity.identifier}|{PROJECTION_VERSION}"
            ).encode("utf-8"),
        ).hexdigest()
        eligible = (
            receipt is not None
            and ready_application is not None
            and candidate_id not in self.consumed_readback_ids
            and current.events == controller.public_snapshot().events
        )
        declared_target = action_receipt_label(self.contract, request.action_id)
        if not eligible:
            result = PrepRecoverResult(
                target_confirmed=False,
                summary_confirmed=False,
                prep_error=False,
                ineligible=False,
                declared_target=declared_target,
                evidence="c-adapter:recover-public-basis-unconfirmed",
                post_summary=None,
            )
            successor = self._next(controller=controller, checkpoint=current, receipt=receipt)
            record = self._record(
                request,
                effect_class="NONE",
                prep_recover=result,
                suffix="recover-unconfirmed",
            )
            return EnvironmentExecution(record, successor)
        assert receipt is not None
        readback = ToolReadbackEvidence(
            readback_id=candidate_id,
            execution_attempt_id=request.execution_attempt_id,
            run_id=controller.run_id,
            reset_id=current.reset_id,
            attempt_id=current.attempt_id,
            session_id=current.session_id,
            correlation_id=current.correlation_id,
            retained_protocol_prefix_digest=_snapshot_digest(current),
            retained_event_ids=tuple(event.event_id for event in current.events),
            sampled_tick=controller.virtual_tick,
            sampled_sequence=(current.events[-1].sequence_number if current.events else 0),
            projection_version=f"{PROJECTION_VERSION}:{self.adapter_source_identity.digest}",
            completed=True,
            receipt=receipt,
        )
        successor = self._next(
            controller=controller,
            checkpoint=current,
            receipt=receipt,
            readback=readback,
        )
        outcome = action_outcome(self.contract, request.action_id, "RECOVER-READY-READBACK")
        summary = outcome.get("postSummary")
        if type(summary) is not str or not summary:
            return self._unknown(request, successor=successor)
        result = PrepRecoverResult(
            target_confirmed=True,
            summary_confirmed=True,
            prep_error=False,
            ineligible=False,
            declared_target=declared_target,
            evidence=f"c-adapter:tool-readback:{readback.readback_id}",
            post_summary=summary,
        )
        record = self._record(
            request,
            effect_class="NONE",
            summary_confirmed=True,
            post_summary=summary,
            prep_recover=result,
            suffix=f"recover:{readback.readback_id}",
        )
        return EnvironmentExecution(record, successor)

    def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
        """Drive one selected action without receiving algorithm internals."""

        error = self._preflight(request)
        if error is not None:
            return self._not_sent(request) if type(request) is ExecutionRequest else EnvironmentExecution(
                VisibleExecutionRecord(
                    execution_attempt_id="c-adapter-invalid-request",
                    action_id="c-adapter-invalid-request",
                    effect_class="CONFIRMED-NOT-SENT",
                    observable=None,
                    summary_confirmed=False,
                    post_summary=None,
                    measurement_tick=None,
                    uncertainty_identity=None,
                    evidence_ref="c-adapter:invalid-request:not-sent",
                ),
                self,
            )
        assert type(request) is ExecutionRequest
        try:
            controller = deepcopy(self.controller)
            if request.action_id == INSPECT_ACTION_ID:
                return self._drive_initial_inspection(request, controller)
            if request.action_id == PREP_ACTION_ID:
                return self._drive_prep(request, controller)
            if request.action_id == ORDER_ACTION_ID:
                return self._drive_order_test(request, controller)
            if request.action_id == RECOVER_ACTION_ID:
                return self._drive_recover(request, controller)
        except (AttributeError, TypeError, ValueError, ScenarioContractError, SessionAdapterError):
            # A controller/tool boundary fault has no confirmed public summary,
            # but the copied continuation is retained when it exists.  Do not
            # convert it into a not-sent result or expose the raw reason.
            try:
                snapshot = controller.public_snapshot()
                successor = self._next(controller=controller, checkpoint=snapshot)
            except (AttributeError, UnboundLocalError):
                successor = self
            return self._unknown(request, successor=successor)
        raise SessionAdapterError("C-ADAPTER-ACTION-DISPATCH-UNREACHABLE")


def build_lur_start_session(
    *,
    repository: Path | str,
    controller: LurStartController,
    resources: ResourceState | None = None,
    retry_cap: int = 1,
) -> LurStartSession:
    """Build the production C-stage session on a fresh real B object.

    Setup is the only place where a fresh object is accepted.  A continuation
    is always represented by a returned adapter successor; callers cannot
    smuggle a pre-driven controller into a new ``SCENE-ENTRY`` session.
    """

    if type(controller) is not LurStartController:
        raise SessionAdapterError("C-ADAPTER-CONTROLLER-TYPE-INVALID")
    if controller.public_snapshot().events:
        raise SessionAdapterError("C-ADAPTER-INITIAL-OBJECT-MUST-BE-FRESH")
    contract = load_hb_session_contract(repository)
    environment = LurStartSessionEnvironment.from_controller(controller=controller, contract=contract)
    session = ReferenceSession(
        binding=contract.authority_binding,
        model=contract.model,
        session_id=controller.session_id,
        run_id=controller.run_id,
        experiment_attempt_id=controller.attempt_id,
        initial_summary="SCENE-ENTRY",
        resources=resources if resources is not None else ResourceState.rounds(4),
        retry_cap=retry_cap,
    )
    return LurStartSession(session, environment, contract, environment.adapter_source_identity)


register_loaded_module(__name__, __file__)
