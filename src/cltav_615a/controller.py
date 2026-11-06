"""Direct deterministic controller for the bounded UPLOAD LUR-start slice.

This controller is intentionally a small engineering object driver.  It owns
event identity, the append-only public journal, delivery microsteps, virtual
time, evaluator-only fault audit, and full reset.  It neither imports nor
implements the CL-TAV runtime, prediction, history update, q/H summaries,
Recover, a network stack, or a protocol conformance verdict.
"""

from __future__ import annotations

from collections import deque
from types import MappingProxyType
from typing import Mapping

from .objects import (
    EVENT_DL_DATA_LUR,
    EVENT_DL_WRQ_LUR,
    EVENT_LIST_PREPARED,
    EVENT_TH_ACK_LUR,
    EVENT_TH_LUS_READY,
    LoaderSurrogate,
    TargetHardwareDriver,
)
from .types import (
    ActivationRecord,
    ActivationStatus,
    AttemptAudit,
    CompletionReceipt,
    DeliveryResult,
    EmissionDecision,
    FaultInstallationRecord,
    FaultLifecycleReadback,
    FaultVariant,
    FiniteCheckResult,
    InstallationStatus,
    JournalSnapshot,
    OperationResult,
    PrefixVerification,
    PublicEvent,
    ResetReadback,
    RuntimeReadback,
)


RESET_SCOPE = (
    "LOADER-STATE",
    "TH-STATE",
    "VIRTUAL-CLOCK",
    "EVENT-JOURNAL",
    "PENDING-DELIVERY",
    "CORRELATION-ID-SEQUENCE",
    "FAULT-INSTALLATION-STATE",
)


class LurStartController:
    """Own one resettable direct Loader/TH engineering attempt at a time.

    Calling a public method effects at most one semantic emission or one event
    delivery.  This makes the microstep boundary explicit:

    ``stimulus/request -> object guard/update -> public emission -> pending
    delivery -> peer update``.

    A caller can drive the normal slice or either permitted single-fault
    variant directly.  The controller never uses a predicted result, expected
    hypothesis set, a prebuilt event trace, or a ReferenceSession to decide an
    object emission.
    """

    _FAMILY_ID = "ENG-UPLOAD-LUR-START"

    def __init__(self, *, implementation_identity: str = "cltav_615a-b-candidate-source") -> None:
        if not isinstance(implementation_identity, str) or not implementation_identity.strip():
            raise ValueError("implementation_identity must be nonblank")
        self._implementation_identity = implementation_identity
        self._reset_counter = 0
        self._attempt_counter = 0
        self._receipt_counter = 0
        self._installation_counter = 0
        self._activation_counter = 0
        self._archives: list[AttemptAudit] = []
        self._reset_records: list[ResetReadback] = []
        self._loader: LoaderSurrogate | None = None
        self._target: TargetHardwareDriver | None = None
        self._journal: list[PublicEvent] = []
        self._pending: deque[PublicEvent] = deque()
        self._delivered_event_ids: list[str] = []
        self._installation_records: list[FaultInstallationRecord] = []
        self._activation_records: list[ActivationRecord] = []
        self._active_fault = FaultVariant.NORMAL
        self._attempt_blocked = False
        self._virtual_tick = 0
        self._next_sequence = 1
        self._reset_id = ""
        self._attempt_id = ""
        self._session_id = ""
        self._correlation_id = ""
        # Initialization is represented by the same full-reset semantics used
        # between attempts.  It has no old active attempt to archive.
        self.full_reset()

    @property
    def implementation_identity(self) -> str:
        """Evaluator-side source identity supplied for this bounded object."""

        return self._implementation_identity

    @property
    def attempt_id(self) -> str:
        return self._attempt_id

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def correlation_id(self) -> str:
        return self._correlation_id

    @property
    def virtual_tick(self) -> int:
        return self._virtual_tick

    @property
    def reset_history(self) -> tuple[ResetReadback, ...]:
        return tuple(self._reset_records)

    def evaluator_readback(self) -> RuntimeReadback:
        """Return evaluator-only state; never use this as a public projection."""

        loader = self._require_loader()
        target = self._require_target()
        loader_state = loader.state
        target_state = target.state
        return RuntimeReadback(
            reset_id=self._reset_id,
            attempt_id=self._attempt_id,
            session_id=self._session_id,
            correlation_id=self._correlation_id,
            virtual_tick=self._virtual_tick,
            list_offered=loader_state.list_offered,
            target_list_ready=loader_state.target_list_ready,
            list_accepted=loader_state.list_accepted,
            matching_lur_ack=loader_state.matching_lur_ack,
            th_matching_lur_wrq_received=target_state.matching_lur_wrq_received,
            journal_length=len(self._journal),
            pending_delivery_length=len(self._pending),
            delivered_event_count=len(self._delivered_event_ids),
            active_fault=self._active_fault,
            attempt_blocked=self._attempt_blocked,
        )

    def evaluator_audit(self) -> tuple[AttemptAudit, ...]:
        """Return retained old audit plus a snapshot of the active attempt."""

        current = AttemptAudit(
            reset_id=self._reset_id,
            attempt_id=self._attempt_id,
            journal=tuple(self._journal),
            installation_records=tuple(self._installation_records),
            activation_records=tuple(self._activation_records),
            final_readback=self.evaluator_readback(),
        )
        return (*self._archives, current)

    def evaluator_fault_readback(self) -> FaultLifecycleReadback:
        """Read installation and activation separately without exposing either publicly."""

        last_install = self._installation_records[-1] if self._installation_records else None
        activation = self._activation_records[-1] if self._activation_records else None
        installed_fault = self._active_fault
        return FaultLifecycleReadback(
            reset_id=self._reset_id,
            attempt_id=self._attempt_id,
            installed_fault=installed_fault,
            installation_status=(last_install.status if last_install is not None else InstallationStatus.NOT_INSTALLED),
            activation_status=(ActivationStatus.TRIGGERED if activation is not None else ActivationStatus.NOT_TRIGGERED),
            installation_record_id=(last_install.record_id if last_install is not None else None),
            activation_record_id=(activation.activation_id if activation is not None else None),
            code_identity=self._implementation_identity,
        )

    def public_scene_configuration(self) -> Mapping[str, str]:
        """Return the fixed public object configuration with no private fault data."""

        return MappingProxyType(
            {
                "scenarioFamilyId": self._FAMILY_ID,
                "objectKind": "IN-PROCESS-CONTROLLED-DATA-LOADER-SURROGATE",
                "peerKind": "IN-PROCESS-CONTROLLED-TARGET-HARDWARE-DRIVER",
                "payloadBoundary": "OPAQUE-NO-LUR-BYTE-PAYLOAD-OR-CHECKSUM-EVALUATED",
                "timeBoundary": "VIRTUAL-ENGINEERING-TICK-NOT-PROTOCOL-DEADLINE",
            }
        )

    def full_reset(self, *, force_revocation_failure: bool = False) -> ResetReadback:
        """Fully reset active state while retaining outer evaluator audit evidence.

        ``force_revocation_failure`` is a narrow synthetic controller-control
        seam used only to prove that a failed revocation cannot be relabelled as
        a clean normal attempt.  It is not another protocol fault variant.
        """

        before = self.evaluator_readback() if self._loader is not None else None
        if self._loader is not None and force_revocation_failure:
            self._attempt_blocked = True
            record = ResetReadback(
                reset_id=self._reset_id,
                previous_attempt_id=self._attempt_id,
                attempt_id=None,
                success=False,
                reason="RESET-FAILED-FAULT-REVOCATION",
                code_identity=self._implementation_identity,
                cleared_scope=(),
                before=before,
                after=self.evaluator_readback(),
            )
            self._reset_records.append(record)
            return record

        if self._loader is not None:
            self._archives.append(
                AttemptAudit(
                    reset_id=self._reset_id,
                    attempt_id=self._attempt_id,
                    journal=tuple(self._journal),
                    installation_records=tuple(self._installation_records),
                    activation_records=tuple(self._activation_records),
                    final_readback=before if before is not None else self.evaluator_readback(),
                )
            )

        previous_attempt_id = self._attempt_id or None
        self._reset_counter += 1
        self._attempt_counter += 1
        self._reset_id = f"reset-{self._reset_counter:04d}"
        self._attempt_id = f"attempt-{self._attempt_counter:04d}"
        self._session_id = f"upload-session-{self._attempt_counter:04d}"
        self._correlation_id = f"lur-operation-{self._attempt_counter:04d}"
        self._virtual_tick = 0
        self._next_sequence = 1
        self._journal = []
        self._pending = deque()
        self._delivered_event_ids = []
        self._activation_records = []
        self._active_fault = FaultVariant.NORMAL
        self._attempt_blocked = False
        self._loader = LoaderSurrogate(
            reset_id=self._reset_id,
            attempt_id=self._attempt_id,
            session_id=self._session_id,
            correlation_id=self._correlation_id,
        )
        self._target = TargetHardwareDriver(
            reset_id=self._reset_id,
            attempt_id=self._attempt_id,
            session_id=self._session_id,
            correlation_id=self._correlation_id,
        )
        self._installation_records = []
        self._new_installation_record(
            requested_fault=None,
            status=InstallationStatus.NOT_INSTALLED,
            reason="NO-PROTOCOL-FAULT-INSTALLED",
        )
        after = self.evaluator_readback()
        record = ResetReadback(
            reset_id=self._reset_id,
            previous_attempt_id=previous_attempt_id,
            attempt_id=self._attempt_id,
            success=True,
            reason="FULL-RESET-COMPLETED-NOT-PROTOCOL-ABORT",
            code_identity=self._implementation_identity,
            cleared_scope=RESET_SCOPE,
            before=before,
            after=after,
        )
        self._reset_records.append(record)
        return record

    def install_fault(
        self,
        fault: FaultVariant,
        *,
        force_failure: bool = False,
    ) -> FaultInstallationRecord:
        """Install exactly one eligible private fault variant for this attempt."""

        if not isinstance(fault, FaultVariant):
            return self._new_installation_record(
                requested_fault=None,
                status=InstallationStatus.REJECTED,
                reason="FAULT-INSTALLATION-REJECTED-UNKNOWN-VARIANT",
            )
        if self._attempt_blocked:
            return self._new_installation_record(
                requested_fault=fault,
                status=InstallationStatus.REJECTED,
                reason="FAULT-INSTALLATION-REJECTED-CONTROL-UNCONFIRMED",
            )
        if fault is FaultVariant.NORMAL:
            return self._new_installation_record(
                requested_fault=fault,
                status=InstallationStatus.REJECTED,
                reason="FAULT-INSTALLATION-REJECTED-NORMAL-REQUIRES-NO-INSTALL",
            )
        if self._active_fault is not FaultVariant.NORMAL:
            return self._new_installation_record(
                requested_fault=fault,
                status=InstallationStatus.REJECTED,
                reason="FAULT-INSTALLATION-REJECTED-SINGLE-FAULT-LIMIT",
            )
        if force_failure:
            self._attempt_blocked = True
            return self._new_installation_record(
                requested_fault=fault,
                status=InstallationStatus.FAILED,
                reason="FAULT-INSTALLATION-FAILED-READBACK-UNCONFIRMED",
            )
        self._active_fault = fault
        return self._new_installation_record(
            requested_fault=fault,
            status=InstallationStatus.INSTALLED,
            reason="FAULT-INSTALLATION-READBACK-CONFIRMED",
        )

    def record_list_submission_precondition(self) -> OperationResult:
        blocked = self._control_blocked_result()
        if blocked is not None:
            return blocked
        return self._emit_decision(self._require_loader().record_list_submission())

    def emit_target_lus_ready(self) -> OperationResult:
        """Request one current-session LUS-0001 readiness semantic stimulus."""

        blocked = self._control_blocked_result()
        if blocked is not None:
            return blocked
        loader_state = self._require_loader().state
        if not loader_state.list_offered:
            return OperationResult(False, "READY-REJECTED-LIST-NOT-OFFERED")
        if loader_state.list_accepted:
            return OperationResult(False, "READY-REJECTED-LIST-ALREADY-ACCEPTED")
        return self._emit_decision(self._require_target().emit_ready())

    def advance_loader(self) -> OperationResult:
        """Let the real Loader choose exactly its next locally enabled emission."""

        blocked = self._control_blocked_result()
        if blocked is not None:
            return blocked
        loader = self._require_loader()
        state = loader.state
        if not state.list_offered:
            return OperationResult(False, "LOADER-BLOCKED-LIST-NOT-OFFERED")
        if not state.list_accepted:
            return self._emit_decision(loader.request_wrq(self._active_fault), bind_wrq_identity=True)
        if not state.data_emitted:
            return self._emit_decision(loader.request_data(self._active_fault))
        return OperationResult(False, "LOADER-IGNORED-CONTROL-SLICE-COMPLETE")

    def advance_target_hardware(self) -> OperationResult:
        """Let TH emit an ACK only after it really received a current WRQ."""

        blocked = self._control_blocked_result()
        if blocked is not None:
            return blocked
        return self._emit_decision(self._require_target().emit_ack())

    def deliver_next(self) -> DeliveryResult:
        """Deliver the oldest emitted event without reordering or reminting it."""

        if self._attempt_blocked:
            return DeliveryResult(False, False, "DELIVERY-REJECTED-CONTROL-UNCONFIRMED", None)
        if not self._pending:
            return DeliveryResult(False, False, "DELIVERY-NO-PENDING-EVENT", None)
        event = self._pending.popleft()
        result = self._route_event(event)
        self._delivered_event_ids.append(event.event_id)
        return DeliveryResult(True, result.accepted, result.reason, event)

    def deliver_all(self) -> tuple[DeliveryResult, ...]:
        """Deliver the current queue in its real append order."""

        delivered: list[DeliveryResult] = []
        while self._pending:
            delivered.append(self.deliver_next())
        return tuple(delivered)

    def deliver_external_event(self, event: object) -> DeliveryResult:
        """Route a retained/foreign event without adding it to the new journal.

        This direct entry supports ownership tests for old attempts, wrong
        session/correlation material and duplicate delivery.  A foreign event
        therefore cannot be transformed into a freshly emitted public record.
        """

        if self._attempt_blocked:
            return DeliveryResult(False, False, "DELIVERY-REJECTED-CONTROL-UNCONFIRMED", None)
        if not isinstance(event, PublicEvent):
            return DeliveryResult(False, False, "DELIVERY-REJECTED-MALFORMED-EVENT", None)
        result = self._route_event(event)
        return DeliveryResult(True, result.accepted, result.reason, event)

    def advance_tick(self, steps: int = 1) -> int:
        """Advance deterministic engineering time; this is not a protocol deadline."""

        if not isinstance(steps, int) or isinstance(steps, bool) or steps < 0:
            raise ValueError("virtual tick advancement must be a nonnegative integer")
        self._virtual_tick += steps
        return self._virtual_tick

    def public_snapshot(self) -> JournalSnapshot:
        """Return an immutable value snapshot; future emissions cannot alter it."""

        return JournalSnapshot(
            reset_id=self._reset_id,
            attempt_id=self._attempt_id,
            session_id=self._session_id,
            correlation_id=self._correlation_id,
            events=tuple(self._journal),
        )

    def inspect_current_prefix(self, *, receipt_label: str = "CURRENT-JOURNAL-CHECK") -> CompletionReceipt:
        """Create a completed receipt from the object-owned current journal only."""

        if not isinstance(receipt_label, str) or not receipt_label.strip():
            raise ValueError("receipt_label must be nonblank")
        return self._receipt(receipt_label, tuple(self._journal), completed=not self._attempt_blocked)

    def validate_retained_prefix(self, snapshot: object) -> PrefixVerification:
        """Validate equal or true-append continuity without calling it a completion."""

        if not isinstance(snapshot, JournalSnapshot):
            return PrefixVerification(
                False,
                "PREFIX-INVALID-MALFORMED-SNAPSHOT",
                self._receipt("RETAINED-PREFIX-INVALID", (), completed=False),
            )
        if not self._same_attempt(snapshot):
            return PrefixVerification(
                False,
                "PREFIX-INVALID-CROSS-ATTEMPT-OR-SESSION",
                self._receipt("RETAINED-PREFIX-INVALID", snapshot.events, completed=False),
            )
        candidate = snapshot.events
        actual_prefix = tuple(self._journal[: len(candidate)])
        if candidate != actual_prefix:
            return PrefixVerification(
                False,
                "PREFIX-INVALID-REPLACED-REORDERED-OR-DISCONNECTED",
                self._receipt("RETAINED-PREFIX-INVALID", candidate, completed=False),
            )
        reason = "PREFIX-EQUAL-CURRENT-JOURNAL" if len(candidate) == len(self._journal) else "PREFIX-RETAINED-AND-APPENDED"
        return PrefixVerification(True, reason, self._receipt("RETAINED-PREFIX-VALID", candidate, completed=True))

    def complete_snapshot(self, snapshot: object) -> PrefixVerification:
        """Require an exact current snapshot before calling an inspection complete."""

        retained = self.validate_retained_prefix(snapshot)
        if not retained.complete:
            return retained
        if not isinstance(snapshot, JournalSnapshot):  # Narrowing for type checkers and defensive callers.
            return retained
        if len(snapshot.events) != len(self._journal):
            return PrefixVerification(
                False,
                "CURRENT-PREFIX-INCOMPLETE-TRUNCATED",
                self._receipt("CURRENT-PREFIX-INCOMPLETE", snapshot.events, completed=False),
            )
        return PrefixVerification(True, "CURRENT-PREFIX-COMPLETE", self._receipt("CURRENT-PREFIX-COMPLETE", snapshot.events, completed=True))

    def check_no_wrq_before_ready(self) -> FiniteCheckResult:
        """Read the real journal to classify only this finite engineering predicate."""

        events = tuple(self._journal)
        first_ready = next((event for event in events if event.kind == EVENT_TH_LUS_READY), None)
        first_wrq = next((event for event in events if event.kind == EVENT_DL_WRQ_LUR), None)
        early = first_wrq is not None and (
            first_ready is None or first_wrq.sequence_number < first_ready.sequence_number
        )
        observable = "EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001" if early else "NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001"
        return FiniteCheckResult(observable, self._receipt("FINITE-NO-WRQ-CHECK", events, completed=not self._attempt_blocked))

    def check_lur_order(self) -> FiniteCheckResult:
        """Read WRQ/ACK/DATA order from the real current-correlation journal."""

        events = tuple(
            event
            for event in self._journal
            if event.session_id == self._session_id and event.correlation_id == self._correlation_id
        )
        wrq = next((event for event in events if event.kind == EVENT_DL_WRQ_LUR), None)
        data = next((event for event in events if event.kind == EVENT_DL_DATA_LUR), None)
        matching_ack = next(
            (
                event
                for event in events
                if event.kind == EVENT_TH_ACK_LUR and wrq is not None and event.in_reply_to_event_id == wrq.event_id
            ),
            None,
        )
        if wrq is None:
            observable = "INCOMPLETE-NO-WRQ"
        elif data is None:
            observable = "INCOMPLETE-NO-DATA"
        elif matching_ack is None or data.sequence_number < matching_ack.sequence_number:
            observable = "DATA-BEFORE-MATCHING-ACK"
        else:
            observable = "WRQ-ACK-DATA-IN-ORDER"
        return FiniteCheckResult(observable, self._receipt("FINITE-LUR-ORDER-CHECK", events, completed=not self._attempt_blocked))

    def run_shared_control_script(self) -> tuple[OperationResult | DeliveryResult, ...]:
        """Drive one identical public stimulus sequence for all three variants.

        The script deliberately probes before ready and before ACK.  NORMAL
        therefore records named waits/rejections, EARLY-WRQ emits its actual
        early WRQ, and EARLY-DATA emits its actual early DATA.  No case-to-trace
        table or private fault value is copied into the public result.
        """

        results: list[OperationResult | DeliveryResult] = []
        results.append(self.record_list_submission_precondition())
        results.extend(self.deliver_all())
        results.append(self.advance_loader())
        results.extend(self.deliver_all())
        results.append(self.emit_target_lus_ready())
        results.extend(self.deliver_all())
        results.append(self.advance_loader())
        results.extend(self.deliver_all())
        results.append(self.advance_loader())
        results.extend(self.deliver_all())
        results.append(self.advance_target_hardware())
        results.extend(self.deliver_all())
        results.append(self.advance_loader())
        results.extend(self.deliver_all())
        return tuple(results)

    def _control_blocked_result(self) -> OperationResult | None:
        if self._attempt_blocked:
            return OperationResult(False, "CONTROL-UNCONFIRMED-ATTEMPT-NOT-DRIVABLE")
        return None

    def _emit_decision(self, decision: EmissionDecision, *, bind_wrq_identity: bool = False) -> OperationResult:
        if not decision.accepted:
            return OperationResult(False, decision.reason)
        required = (decision.kind, decision.layer, decision.actor, decision.receiver)
        if any(value is None for value in required):
            return OperationResult(False, "EMISSION-REJECTED-INCOMPLETE-OBJECT-DECISION")
        event = PublicEvent(
            event_id=(f"{self._reset_id}:{self._attempt_id}:event-{self._next_sequence:04d}"),
            reset_id=self._reset_id,
            attempt_id=self._attempt_id,
            session_id=self._session_id,
            correlation_id=self._correlation_id,
            layer=str(decision.layer),
            actor=str(decision.actor),
            receiver=str(decision.receiver),
            direction=decision.direction,
            kind=str(decision.kind),
            opcode=decision.opcode,
            file_role=decision.file_role,
            in_reply_to_event_id=decision.in_reply_to_event_id,
            tick=self._virtual_tick,
            sequence_number=self._next_sequence,
        )
        if bind_wrq_identity:
            bound = self._require_loader().record_wrq_event_identity(event)
            if not bound.accepted:
                return OperationResult(False, bound.reason)
        self._journal.append(event)
        self._pending.append(event)
        self._next_sequence += 1
        if decision.activation_fault is not None:
            self._activation_counter += 1
            self._activation_records.append(
                ActivationRecord(
                    activation_id=f"{self._attempt_id}:activation-{self._activation_counter:04d}",
                    reset_id=self._reset_id,
                    attempt_id=self._attempt_id,
                    fault=decision.activation_fault,
                    public_event_id=event.event_id,
                    execution_position=decision.activation_position or "UNSPECIFIED-BYPASS-POSITION",
                )
            )
        return OperationResult(True, decision.reason, event)

    def _route_event(self, event: PublicEvent) -> EmissionDecision:
        if event.kind == EVENT_TH_LUS_READY:
            return self._require_loader().receive_ready(event)
        if event.kind == EVENT_DL_WRQ_LUR:
            return self._require_target().receive_wrq(event)
        if event.kind == EVENT_TH_ACK_LUR:
            return self._require_loader().receive_ack(event)
        if event.kind in {EVENT_LIST_PREPARED, EVENT_DL_DATA_LUR}:
            return EmissionDecision(True, "DELIVERY-RECORDED-NO-ADDITIONAL-PEER-STATE")
        return EmissionDecision(False, "DELIVERY-REJECTED-UNKNOWN-SEMANTIC-EVENT")

    def _receipt(self, label: str, events: tuple[PublicEvent, ...], *, completed: bool) -> CompletionReceipt:
        self._receipt_counter += 1
        return CompletionReceipt(
            receipt_id=f"{self._attempt_id}:receipt-{self._receipt_counter:04d}:{label}",
            reset_id=self._reset_id,
            attempt_id=self._attempt_id,
            session_id=self._session_id,
            correlation_id=self._correlation_id,
            start_sequence=events[0].sequence_number if events else None,
            end_sequence=events[-1].sequence_number if events else None,
            event_ids=tuple(event.event_id for event in events),
            completed=completed,
            reason="ENGINEERING-FINITE-JOURNAL-CHECK-NOT-PROTOCOL-DEADLINE",
        )

    def _new_installation_record(
        self,
        *,
        requested_fault: FaultVariant | None,
        status: InstallationStatus,
        reason: str,
    ) -> FaultInstallationRecord:
        self._installation_counter += 1
        record = FaultInstallationRecord(
            record_id=f"{self._attempt_id}:installation-{self._installation_counter:04d}",
            reset_id=self._reset_id,
            attempt_id=self._attempt_id,
            requested_fault=requested_fault,
            status=status,
            code_identity=self._implementation_identity,
            reason=reason,
        )
        self._installation_records.append(record)
        return record

    def _same_attempt(self, snapshot: JournalSnapshot) -> bool:
        return (
            snapshot.reset_id == self._reset_id
            and snapshot.attempt_id == self._attempt_id
            and snapshot.session_id == self._session_id
            and snapshot.correlation_id == self._correlation_id
        )

    def _require_loader(self) -> LoaderSurrogate:
        if self._loader is None:
            raise RuntimeError("controller loader is not initialized")
        return self._loader

    def _require_target(self) -> TargetHardwareDriver:
        if self._target is None:
            raise RuntimeError("controller target hardware is not initialized")
        return self._target
