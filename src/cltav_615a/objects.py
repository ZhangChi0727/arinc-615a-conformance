"""Private state machines for the bounded semantic Loader/TH control slice."""

from __future__ import annotations

from dataclasses import dataclass

from .types import EmissionDecision, FaultVariant, PublicEvent
from .source_identity import register_loaded_module


EVENT_LIST_PREPARED = "LIST-SUBMISSION-PRECONDITION-RECORDED"
EVENT_TH_LUS_READY = "EV_TH_LUS0001"
EVENT_DL_WRQ_LUR = "EV_DL_WRQ_LUR"
EVENT_TH_ACK_LUR = "EV_TH_ACK_LUR"
EVENT_DL_DATA_LUR = "EV_DL_DATA_LUR"


def semantic_event_error(event: PublicEvent) -> str | None:
    """Validate the five bounded event types, not their protocol order."""

    expected = {
        EVENT_LIST_PREPARED: ("APPLICATION", "DLA", "TARGET-HARDWARE", None, None, "LOAD-LIST"),
        EVENT_TH_LUS_READY: ("SEMANTIC-PROTOCOL", "TARGET-HARDWARE", "DATA-LOADER", "TH-TO-DL", None, "LUS-0001"),
        EVENT_DL_WRQ_LUR: ("SEMANTIC-PROTOCOL", "DATA-LOADER", "TARGET-HARDWARE", "DL-TO-TH", "WRQ", "LUR"),
        EVENT_TH_ACK_LUR: ("SEMANTIC-PROTOCOL", "TARGET-HARDWARE", "DATA-LOADER", "TH-TO-DL", "ACK", "LUR"),
        EVENT_DL_DATA_LUR: ("SEMANTIC-PROTOCOL", "DATA-LOADER", "TARGET-HARDWARE", "DL-TO-TH", "DATA", "LUR"),
    }
    if event.kind not in expected:
        return "UNKNOWN-KIND"
    actual = (event.layer, event.actor, event.receiver, event.direction, event.opcode, event.file_role)
    if actual != expected[event.kind]:
        return "CONTRADICTORY-TUPLE"
    if event.kind in {EVENT_LIST_PREPARED, EVENT_TH_LUS_READY, EVENT_DL_WRQ_LUR} and event.in_reply_to_event_id is not None:
        return "UNEXPECTED-REPLY-REFERENCE"
    if event.kind == EVENT_TH_ACK_LUR and event.in_reply_to_event_id is None:
        return "MISSING-WRQ-REFERENCE"
    return None


@dataclass(frozen=True)
class LoaderState:
    """Private Loader state; it is exposed only through evaluator readback."""

    list_offered: bool
    target_list_ready: bool
    list_accepted: bool
    matching_lur_ack: bool
    wrq_correlation: str | None
    wrq_event_id: str | None
    matching_ack_event_id: str | None
    data_emitted: bool


@dataclass(frozen=True)
class TargetHardwareState:
    """Private TH state; it is exposed only through evaluator readback."""

    matching_lur_wrq_received: bool
    received_wrq_event_id: str | None
    ack_emitted: bool
    ready_emitted: bool


class LoaderSurrogate:
    """Real guard/update object for the limited DATA-LOADER slice.

    The object decides whether a stimulus can mutate its own state.  It does
    not create public event identities or journal entries; that responsibility
    belongs to the controller which owns the deterministic virtual scheduler.
    """

    def __init__(self, *, reset_id: str, attempt_id: str, session_id: str, correlation_id: str) -> None:
        self._reset_id = reset_id
        self._attempt_id = attempt_id
        self._session_id = session_id
        self._correlation_id = correlation_id
        self.reset()

    @property
    def state(self) -> LoaderState:
        return LoaderState(
            list_offered=self._list_offered,
            target_list_ready=self._target_list_ready,
            list_accepted=self._list_accepted,
            matching_lur_ack=self._matching_lur_ack,
            wrq_correlation=self._wrq_correlation,
            wrq_event_id=self._wrq_event_id,
            matching_ack_event_id=self._matching_ack_event_id,
            data_emitted=self._data_emitted,
        )

    def reset(self) -> None:
        self._list_offered = False
        self._target_list_ready = False
        self._list_accepted = False
        self._matching_lur_ack = False
        self._wrq_correlation: str | None = None
        self._wrq_event_id: str | None = None
        self._matching_ack_event_id: str | None = None
        self._data_emitted = False

    def record_list_submission(self) -> EmissionDecision:
        """Establish the named application preparation boundary once."""

        if self._list_offered:
            return EmissionDecision(False, "LIST-SUBMISSION-IGNORED-ALREADY-OFFERED")
        self._list_offered = True
        return EmissionDecision(
            True,
            "LIST-SUBMISSION-PRECONDITION-RECORDED",
            kind=EVENT_LIST_PREPARED,
            layer="APPLICATION",
            actor="DLA",
            receiver="TARGET-HARDWARE",
            direction=None,
            opcode=None,
            file_role="LOAD-LIST",
        )

    def record_wrq_event_identity(self, event: object) -> EmissionDecision:
        """Bind the emitted WRQ identity after the controller has minted it."""

        if not isinstance(event, PublicEvent):
            return EmissionDecision(False, "WRQ-IDENTITY-REJECTED-MALFORMED-EVENT")
        if event.kind != EVENT_DL_WRQ_LUR or event.correlation_id != self._correlation_id:
            return EmissionDecision(False, "WRQ-IDENTITY-REJECTED-NONCURRENT-EVENT")
        if self._wrq_correlation != self._correlation_id or not self._list_accepted:
            return EmissionDecision(False, "WRQ-IDENTITY-REJECTED-NO-CURRENT-WRQ")
        if self._wrq_event_id is not None:
            return EmissionDecision(False, "WRQ-IDENTITY-IGNORED-ALREADY-BOUND")
        self._wrq_event_id = event.event_id
        return EmissionDecision(True, "WRQ-IDENTITY-BOUND")

    def receive_ready(self, event: object) -> EmissionDecision:
        """Accept only a current-session TH LUS-0001 ready stimulus."""

        if not isinstance(event, PublicEvent):
            return EmissionDecision(False, "READY-REJECTED-MALFORMED-EVENT")
        if event.kind != EVENT_TH_LUS_READY or semantic_event_error(event) is not None:
            return EmissionDecision(False, "READY-REJECTED-UNEXPECTED-EVENT")
        if event.reset_id != self._reset_id or event.attempt_id != self._attempt_id:
            return EmissionDecision(False, "READY-REJECTED-STALE-ATTEMPT")
        if event.session_id != self._session_id:
            return EmissionDecision(False, "READY-REJECTED-SESSION-MISMATCH")
        if event.correlation_id != self._correlation_id:
            return EmissionDecision(False, "READY-REJECTED-CORRELATION-MISMATCH")
        if not self._list_offered:
            return EmissionDecision(False, "READY-REJECTED-LIST-NOT-OFFERED")
        if self._list_accepted:
            return EmissionDecision(False, "READY-REJECTED-LIST-ALREADY-ACCEPTED")
        if self._target_list_ready:
            return EmissionDecision(False, "READY-IGNORED-ALREADY-READY")
        self._target_list_ready = True
        return EmissionDecision(True, "READY-ACCEPTED")

    def request_wrq(self, active_fault: FaultVariant) -> EmissionDecision:
        """Evaluate the real Loader WRQ guard and only bypass readiness when named."""

        if not self._list_offered:
            return EmissionDecision(False, "WRQ-REJECTED-LIST-NOT-OFFERED")
        if self._list_accepted:
            return EmissionDecision(False, "WRQ-IGNORED-LIST-ALREADY-ACCEPTED")
        bypass = active_fault is FaultVariant.EARLY_WRQ and not self._target_list_ready
        if not self._target_list_ready and not bypass:
            return EmissionDecision(False, "WRQ-REJECTED-TARGET-NOT-READY")
        self._list_accepted = True
        self._wrq_correlation = self._correlation_id
        return EmissionDecision(
            True,
            "WRQ-EMITTED-READINESS-BYPASS" if bypass else "WRQ-EMITTED",
            kind=EVENT_DL_WRQ_LUR,
            layer="SEMANTIC-PROTOCOL",
            actor="DATA-LOADER",
            receiver="TARGET-HARDWARE",
            direction="DL-TO-TH",
            opcode="WRQ",
            file_role="LUR",
            activation_fault=FaultVariant.EARLY_WRQ if bypass else None,
            activation_position="LOADER.WRQ.READINESS-GUARD-BYPASS" if bypass else None,
        )

    def receive_ack(self, event: object) -> EmissionDecision:
        """Accept only a current matching TH ACK; stale evidence cannot advance state."""

        if not isinstance(event, PublicEvent):
            return EmissionDecision(False, "ACK-REJECTED-MALFORMED-EVENT")
        if (
            event.kind != EVENT_TH_ACK_LUR
            or semantic_event_error(event) is not None
            or event.actor != "TARGET-HARDWARE"
            or event.receiver != "DATA-LOADER"
            or event.direction != "TH-TO-DL"
            or event.opcode != "ACK"
            or event.file_role != "LUR"
        ):
            return EmissionDecision(False, "ACK-REJECTED-UNEXPECTED-EVENT")
        if event.reset_id != self._reset_id or event.attempt_id != self._attempt_id:
            return EmissionDecision(False, "ACK-REJECTED-STALE-ATTEMPT")
        if event.session_id != self._session_id:
            return EmissionDecision(False, "ACK-REJECTED-SESSION-MISMATCH")
        if event.correlation_id != self._correlation_id:
            return EmissionDecision(False, "ACK-REJECTED-CORRELATION-MISMATCH")
        if (
            not self._list_accepted
            or self._wrq_correlation != event.correlation_id
            or self._wrq_event_id is None
        ):
            return EmissionDecision(False, "ACK-REJECTED-NO-CURRENT-WRQ")
        if event.in_reply_to_event_id != self._wrq_event_id:
            return EmissionDecision(False, "ACK-REJECTED-WRQ-IDENTITY-MISMATCH")
        if self._matching_lur_ack:
            return EmissionDecision(False, "ACK-IGNORED-DUPLICATE")
        self._matching_lur_ack = True
        self._matching_ack_event_id = event.event_id
        return EmissionDecision(True, "ACK-ACCEPTED")

    def request_data(self, active_fault: FaultVariant) -> EmissionDecision:
        """Evaluate the real Loader DATA guard and only bypass matching ACK when named."""

        if (
            not self._list_accepted
            or self._wrq_correlation != self._correlation_id
            or self._wrq_event_id is None
        ):
            return EmissionDecision(False, "DATA-REJECTED-WRQ-NOT-EMITTED")
        if self._data_emitted:
            return EmissionDecision(False, "DATA-IGNORED-ALREADY-EMITTED")
        bypass = active_fault is FaultVariant.EARLY_DATA and not self._matching_lur_ack
        if not self._matching_lur_ack and not bypass:
            return EmissionDecision(False, "DATA-WAIT-MATCHING-ACK")
        self._data_emitted = True
        return EmissionDecision(
            True,
            "DATA-EMITTED-MATCHING-ACK-BYPASS" if bypass else "DATA-EMITTED",
            kind=EVENT_DL_DATA_LUR,
            layer="SEMANTIC-PROTOCOL",
            actor="DATA-LOADER",
            receiver="TARGET-HARDWARE",
            direction="DL-TO-TH",
            opcode="DATA",
            file_role="LUR",
            in_reply_to_event_id=self._matching_ack_event_id,
            activation_fault=FaultVariant.EARLY_DATA if bypass else None,
            activation_position="LOADER.DATA.MATCHING-ACK-GUARD-BYPASS" if bypass else None,
        )


class TargetHardwareDriver:
    """Current-session peer state for LUS-ready and matching LUR ACK emissions."""

    def __init__(self, *, reset_id: str, attempt_id: str, session_id: str, correlation_id: str) -> None:
        self._reset_id = reset_id
        self._attempt_id = attempt_id
        self._session_id = session_id
        self._correlation_id = correlation_id
        self.reset()

    @property
    def state(self) -> TargetHardwareState:
        return TargetHardwareState(
            matching_lur_wrq_received=self._matching_lur_wrq_received,
            received_wrq_event_id=self._received_wrq_event_id,
            ack_emitted=self._ack_emitted,
            ready_emitted=self._ready_emitted,
        )

    def reset(self) -> None:
        self._matching_lur_wrq_received = False
        self._received_wrq_event_id: str | None = None
        self._ack_emitted = False
        self._ready_emitted = False

    def emit_ready(self) -> EmissionDecision:
        if self._ready_emitted:
            return EmissionDecision(False, "READY-EMISSION-IGNORED-ALREADY-EMITTED")
        self._ready_emitted = True
        return EmissionDecision(
            True,
            "READY-EMITTED",
            kind=EVENT_TH_LUS_READY,
            layer="SEMANTIC-PROTOCOL",
            actor="TARGET-HARDWARE",
            receiver="DATA-LOADER",
            direction="TH-TO-DL",
            opcode=None,
            file_role="LUS-0001",
        )

    def receive_wrq(self, event: object) -> EmissionDecision:
        if not isinstance(event, PublicEvent):
            return EmissionDecision(False, "TH-WRQ-REJECTED-MALFORMED-EVENT")
        if (
            event.kind != EVENT_DL_WRQ_LUR
            or semantic_event_error(event) is not None
            or event.actor != "DATA-LOADER"
            or event.receiver != "TARGET-HARDWARE"
            or event.direction != "DL-TO-TH"
            or event.opcode != "WRQ"
            or event.file_role != "LUR"
        ):
            return EmissionDecision(False, "TH-WRQ-REJECTED-UNEXPECTED-EVENT")
        if event.reset_id != self._reset_id or event.attempt_id != self._attempt_id:
            return EmissionDecision(False, "TH-WRQ-REJECTED-STALE-ATTEMPT")
        if event.session_id != self._session_id:
            return EmissionDecision(False, "TH-WRQ-REJECTED-SESSION-MISMATCH")
        if event.correlation_id != self._correlation_id:
            return EmissionDecision(False, "TH-WRQ-REJECTED-CORRELATION-MISMATCH")
        if self._matching_lur_wrq_received:
            return EmissionDecision(False, "TH-WRQ-IGNORED-DUPLICATE")
        self._matching_lur_wrq_received = True
        self._received_wrq_event_id = event.event_id
        return EmissionDecision(True, "TH-WRQ-ACCEPTED")

    def emit_ack(self) -> EmissionDecision:
        if not self._matching_lur_wrq_received:
            return EmissionDecision(False, "ACK-REJECTED-NO-MATCHING-WRQ")
        if self._ack_emitted:
            return EmissionDecision(False, "ACK-IGNORED-ALREADY-EMITTED")
        self._ack_emitted = True
        return EmissionDecision(
            True,
            "ACK-EMITTED",
            kind=EVENT_TH_ACK_LUR,
            layer="SEMANTIC-PROTOCOL",
            actor="TARGET-HARDWARE",
            receiver="DATA-LOADER",
            direction="TH-TO-DL",
            opcode="ACK",
            file_role="LUR",
            in_reply_to_event_id=self._received_wrq_event_id,
        )


register_loaded_module(__name__, __file__)
