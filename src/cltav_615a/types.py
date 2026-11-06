"""Small immutable records shared by the bounded LUR-start objects.

``PublicEvent`` and the receipt records are intentionally independent of the
finite CL-TAV runtime.  They are semantic engineering records only: no UDP/IP
frame, LUR bytes, checksum, predicted hypothesis, expected result, or active
fault identifier is represented here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .source_identity import LoadedSourceIdentity, register_loaded_module


class FaultVariant(str, Enum):
    """The only protocol-behaviour variants permitted by the B-stage slice."""

    NORMAL = "NORMAL"
    EARLY_WRQ = "EARLY-WRQ"
    EARLY_DATA = "EARLY-DATA"


class InstallationStatus(str, Enum):
    """Evaluator-side disposition of a requested fault installation."""

    NOT_INSTALLED = "NOT-INSTALLED"
    INSTALLED = "INSTALLED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"
    CLEARED = "CLEARED"


class ActivationStatus(str, Enum):
    """Evaluator-side activation status; it is never a public event field."""

    NOT_TRIGGERED = "NOT-TRIGGERED"
    TRIGGERED = "TRIGGERED"


@dataclass(frozen=True)
class PublicEvent:
    """One append-only semantic event emitted by the direct object runtime.

    An event identity includes reset and attempt epochs even though the local
    sequence number is intentionally reset for every clean attempt.  ``opcode``
    and ``file_role`` are optional so that application preparation and the
    LUS-ready semantic stimulus do not acquire fabricated TFTP opcodes.
    """

    event_id: str
    reset_id: str
    attempt_id: str
    session_id: str
    correlation_id: str
    layer: str
    actor: str
    receiver: str
    direction: str | None
    kind: str
    opcode: str | None
    file_role: str | None
    in_reply_to_event_id: str | None
    tick: int
    sequence_number: int

    def __post_init__(self) -> None:
        for field_name in (
            "event_id",
            "reset_id",
            "attempt_id",
            "session_id",
            "correlation_id",
            "layer",
            "actor",
            "receiver",
            "kind",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"public event {field_name} must be nonblank")
        if not isinstance(self.tick, int) or isinstance(self.tick, bool) or self.tick < 0:
            raise ValueError("public event tick must be a nonnegative integer")
        if (
            not isinstance(self.sequence_number, int)
            or isinstance(self.sequence_number, bool)
            or self.sequence_number < 0
        ):
            raise ValueError("public event sequence_number must be a nonnegative integer")
        if self.direction is not None and (not isinstance(self.direction, str) or not self.direction.strip()):
            raise ValueError("public event direction must be nonblank when present")
        if self.opcode is not None and self.opcode not in {"WRQ", "ACK", "DATA"}:
            raise ValueError("public event opcode is outside the bounded semantic slice")
        if self.in_reply_to_event_id is not None and (
            not isinstance(self.in_reply_to_event_id, str) or not self.in_reply_to_event_id.strip()
        ):
            raise ValueError("public event in_reply_to_event_id must be nonblank when present")
        if self.layer == "APPLICATION" and self.opcode is not None:
            raise ValueError("application preparation records must not carry a TFTP opcode")


@dataclass(frozen=True)
class OperationResult:
    """Evaluator/control result; internal guard reasons are not public input.

    Only the owned event may be projected to the public journal.  In particular,
    bypass reasons must not be forwarded to a future algorithm adapter.
    """

    accepted: bool
    reason: str
    event: PublicEvent | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValueError("operation result requires a named reason")
        if self.event is not None and not self.accepted:
            raise ValueError("a rejected operation must not claim an emitted event")


@dataclass(frozen=True)
class DeliveryResult:
    """Control/evaluator delivery result, not an algorithm-facing projection."""

    delivered: bool
    accepted: bool
    reason: str
    event: PublicEvent | None

    def __post_init__(self) -> None:
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValueError("delivery result requires a named reason")
        if self.delivered and self.event is None:
            raise ValueError("a delivered result requires its event")
        if self.accepted and not self.delivered:
            raise ValueError("an accepted delivery must have reached a recipient")


@dataclass(frozen=True)
class JournalSnapshot:
    """Immutable public snapshot of the current attempt's cumulative journal."""

    reset_id: str
    attempt_id: str
    session_id: str
    correlation_id: str
    events: tuple[PublicEvent, ...]


@dataclass(frozen=True)
class CompletionReceipt:
    """A finite inspection receipt calculated from the controller's own journal."""

    receipt_id: str
    reset_id: str
    attempt_id: str
    session_id: str
    correlation_id: str
    start_sequence: int | None
    end_sequence: int | None
    event_ids: tuple[str, ...]
    completed: bool
    reason: str


@dataclass(frozen=True)
class FiniteCheckResult:
    """A public finite observation and its bounded receipt."""

    observable: str
    receipt: CompletionReceipt


@dataclass(frozen=True)
class PrefixVerification:
    """Result of comparing a candidate public snapshot with actual journal state."""

    complete: bool
    reason: str
    receipt: CompletionReceipt


@dataclass(frozen=True)
class RuntimeReadback:
    """Evaluator-only concrete state readback for reset/install evidence."""

    reset_id: str
    attempt_id: str
    session_id: str
    correlation_id: str
    virtual_tick: int
    list_offered: bool
    target_list_ready: bool
    list_accepted: bool
    matching_lur_ack: bool
    th_matching_lur_wrq_received: bool
    journal_length: int
    pending_delivery_length: int
    delivered_event_count: int
    active_fault: FaultVariant
    attempt_blocked: bool
    code_identity: str


@dataclass(frozen=True)
class FaultInstallationRecord:
    """Evaluator-only installation/readback record, separate from public events."""

    record_id: str
    reset_id: str
    attempt_id: str
    requested_fault: FaultVariant | None
    status: InstallationStatus
    code_identity: str
    reason: str


@dataclass(frozen=True)
class FaultLifecycleReadback:
    """Evaluator-only installation/activation readback for the active attempt."""

    reset_id: str
    attempt_id: str
    installed_fault: FaultVariant
    installation_status: InstallationStatus
    activation_status: ActivationStatus
    installation_record_id: str | None
    activation_record_id: str | None
    code_identity: str


@dataclass(frozen=True)
class ActivationRecord:
    """Evaluator-only evidence that a real bypass branch actually executed."""

    activation_id: str
    reset_id: str
    attempt_id: str
    fault: FaultVariant
    public_event_id: str
    execution_position: str
    code_identity: str
    status: ActivationStatus = ActivationStatus.TRIGGERED


@dataclass(frozen=True)
class ResetReadback:
    """Evaluator-only reset evidence retaining before/after state boundaries."""

    reset_id: str
    previous_attempt_id: str | None
    attempt_id: str | None
    success: bool
    reason: str
    code_identity: str
    cleared_scope: tuple[str, ...]
    before: RuntimeReadback | None
    after: RuntimeReadback | None


@dataclass(frozen=True)
class AttemptAudit:
    """Retained evaluator audit for an attempt which has left active runtime state."""

    reset_id: str
    attempt_id: str
    journal: tuple[PublicEvent, ...]
    installation_records: tuple[FaultInstallationRecord, ...]
    activation_records: tuple[ActivationRecord, ...]
    final_readback: RuntimeReadback
    code_identity: str
    source_identity: LoadedSourceIdentity


@dataclass(frozen=True)
class EmissionDecision:
    """Internal result of a Loader/TH guard evaluation before journal emission."""

    accepted: bool
    reason: str
    kind: str | None = None
    layer: str | None = None
    actor: str | None = None
    receiver: str | None = None
    direction: str | None = None
    opcode: str | None = None
    file_role: str | None = None
    in_reply_to_event_id: str | None = None
    activation_fault: FaultVariant | None = None
    activation_position: str | None = None


register_loaded_module(__name__, __file__)
